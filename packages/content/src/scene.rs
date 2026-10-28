//! Scene: the description ([`SceneSpec`] is the data stored by the backend) and the compilation ([`Scene`] is the state of every element at
//! every step, ready for rendering).
//!
//! `frames[k]` are the elements visible at step `k`. An element with the same `id` in adjacent frames is the same object on screen:
//! it smoothly moves, changes color and fades out (if the frame lacks it); all of this is done by CSS transitions (`.a-t`).

use std::collections::HashMap;
use std::fmt;

use serde::{Deserialize, Serialize};

use crate::item::Item;

/// Frame: the list of elements visible at a step.
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
#[serde(transparent)]
pub struct Frame(pub Vec<Item>);

impl Frame {
    pub fn new() -> Self {
        Self::default()
    }
    pub fn with(mut self, item: impl Into<Item>) -> Self {
        self.0.push(item.into());
        self
    }
    pub fn with_all<I: Into<Item>>(mut self, items: impl IntoIterator<Item = I>) -> Self {
        self.0.extend(items.into_iter().map(Into::into));
        self
    }
    pub fn items(&self) -> &[Item] {
        &self.0
    }
}

impl<I: Into<Item>> FromIterator<I> for Frame {
    fn from_iter<T: IntoIterator<Item = I>>(iter: T) -> Self {
        Frame(iter.into_iter().map(Into::into).collect())
    }
}

fn is_empty_frame(f: &Frame) -> bool {
    f.0.is_empty()
}
fn step_ms() -> u32 {
    2800
}
fn is_default_ms(v: &u32) -> bool {
    *v == 2800
}
fn height() -> f64 {
    170.0
}
fn is_default_height(v: &f64) -> bool {
    *v == 170.0
}

/// Scene description: this is how it is stored in the database and sent to the client.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct SceneSpec {
    /// step names (buttons above the diagram)
    pub labels: Vec<String>,
    /// caption of each step (below the diagram)
    pub captions: Vec<String>,
    pub frames: Vec<Frame>,
    /// elements present in every frame (unless a frame overrides them by `id`)
    #[serde(default, skip_serializing_if = "is_empty_frame")]
    pub base: Frame,
    /// seconds from the start of the paragraph at which steps 1, 2, … begin; defaults to 5, 13, 21 …
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cues: Option<Vec<f64>>,
    /// step duration without narration, ms
    #[serde(default = "step_ms", skip_serializing_if = "is_default_ms")]
    pub step_ms: u32,
    /// canvas height (the width is always 360)
    #[serde(default = "height", skip_serializing_if = "is_default_height")]
    pub height: f64,
}

impl SceneSpec {
    pub fn new(labels: &[&str], captions: &[&str], frames: Vec<Frame>) -> Self {
        Self {
            labels: labels.iter().map(|s| (*s).to_string()).collect(),
            captions: captions.iter().map(|s| (*s).to_string()).collect(),
            frames,
            base: Frame::new(),
            cues: None,
            step_ms: step_ms(),
            height: height(),
        }
    }
    pub fn base(mut self, base: Frame) -> Self {
        self.base = base;
        self
    }
    pub fn cues(mut self, cues: &[f64]) -> Self {
        self.cues = Some(cues.to_vec());
        self
    }
    pub fn step_ms(mut self, ms: u32) -> Self {
        self.step_ms = ms;
        self
    }
    pub fn height(mut self, h: f64) -> Self {
        self.height = h;
        self
    }
}

/// An error in scene data is an author's error: it is caught by the content tests and by the check at seed time.
#[derive(Clone, Debug, PartialEq)]
pub struct SceneError(pub String);

impl fmt::Display for SceneError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for SceneError {}

/// Compiled scene: for every step, the state of every element (in order of first appearance).
#[derive(Clone, Debug, PartialEq)]
pub struct Scene {
    pub labels: Vec<String>,
    pub captions: Vec<String>,
    pub cues: Vec<f64>,
    pub step_ms: u32,
    pub height: f64,
    /// `states[k][i]` is element `i` at step `k`
    pub states: Vec<Vec<Item>>,
}

fn default_cues(steps: usize) -> Vec<f64> {
    (0..steps.saturating_sub(1)).map(|i| 5.0 + i as f64 * 8.0).collect()
}

impl Scene {
    /// Compilation with data validation: the number of names and captions equals the number of frames, an `id` never changes its element kind,
    /// numbers are finite, step cues increase.
    pub fn compile(spec: &SceneSpec) -> Result<Scene, SceneError> {
        let name = spec.labels.first().map_or("?", String::as_str);
        let err = |msg: String| SceneError(format!("scene '{name}…': {msg}"));
        if spec.frames.is_empty() {
            return Err(err("no frames".into()));
        }
        if spec.labels.len() != spec.frames.len() {
            return Err(err(format!("step labels {}, frames {}", spec.labels.len(), spec.frames.len())));
        }
        if spec.captions.len() != spec.frames.len() {
            return Err(err(format!("captions {}, frames {}", spec.captions.len(), spec.frames.len())));
        }
        if let Some(c) = &spec.cues {
            if c.len() + 1 < spec.frames.len() || c.windows(2).any(|w| w[0] >= w[1]) {
                return Err(err(format!("step cues {c:?} do not fit {} frames", spec.frames.len())));
            }
        }

        let in_frame = |f: &Frame| spec.base.0.iter().chain(f.0.iter()).cloned().collect::<Vec<_>>();
        // frame = base + the frame's elements; a repeated id overrides the previous one
        let mut full: Vec<HashMap<String, Item>> = Vec::with_capacity(spec.frames.len());
        let mut order: Vec<String> = Vec::new();
        let mut first: HashMap<String, Item> = HashMap::new();
        for (k, f) in spec.frames.iter().enumerate() {
            let mut m = HashMap::new();
            for it in in_frame(f) {
                if let Some((key, v)) = it.numbers().into_iter().find(|(_, v)| !v.is_finite()) {
                    return Err(err(format!("frame {k}, item {}: {key} = {v}", it.id())));
                }
                let id = it.id().to_string();
                match first.get(&id) {
                    None => {
                        first.insert(id.clone(), it.clone());
                        order.push(id.clone());
                    }
                    Some(prev) if prev.kind() != it.kind() => {
                        return Err(err(format!("frame {k}: id '{id}' changes item kind ({} → {})", prev.kind(), it.kind())));
                    }
                    Some(_) => {}
                }
                m.insert(id, it);
            }
            full.push(m);
        }
        // what the frame lacks: the last shown state, but hidden; before the first appearance, the first state, hidden
        let mut last_seen: HashMap<&str, &Item> = HashMap::new();
        let mut states = Vec::with_capacity(full.len());
        for m in &full {
            let mut row = Vec::with_capacity(order.len());
            for id in &order {
                match m.get(id) {
                    Some(it) => {
                        last_seen.insert(id, it);
                        row.push(it.clone());
                    }
                    None => row.push(last_seen.get(id.as_str()).map_or_else(|| first[id].hidden(), |it| it.hidden())),
                }
            }
            states.push(row);
        }
        let cues = spec.cues.clone().unwrap_or_else(|| default_cues(spec.frames.len()));
        Ok(Scene { labels: spec.labels.clone(), captions: spec.captions.clone(), cues, step_ms: spec.step_ms, height: spec.height, states })
    }

    /// Compilation for scene authors: an error in the data panics with a clear message.
    pub fn new(spec: SceneSpec) -> Scene {
        Scene::compile(&spec).unwrap_or_else(|e| panic!("{e}"))
    }

    pub fn steps(&self) -> usize {
        self.states.len()
    }

    /// Number of elements in the scene (by `id`).
    pub fn item_count(&self) -> usize {
        self.states.first().map_or(0, Vec::len)
    }
}

/// Width of a line in a monospace font of size `size` (approximately 0.6 of the font size per character).
fn text_width(text: &str, size: f64) -> f64 {
    text.split('\n').map(|l| l.chars().count()).max().unwrap_or(0) as f64 * size * 0.56
}

impl Scene {
    /// Layout check "text fits in cells, nothing is outside the canvas": approximate, based on character widths.
    /// Returns remarks (empty means all is fine); elements with zero opacity are not checked.
    pub fn lint(&self) -> Vec<String> {
        let mut out = Vec::new();
        let name = self.labels.first().map_or("?", String::as_str);
        for (k, row) in self.states.iter().enumerate() {
            for it in row.iter().filter(|i| i.opacity() > 0.0) {
                let mut warn = |msg: String| out.push(format!("scene '{name}…', step {k}, '{}': {msg}", it.id()));
                match it {
                    Item::Cell(c) => {
                        let (need, have) = (text_width(&c.text, c.size), c.w);
                        if need > have + 8.0 {
                            warn(format!("label '{}' is wider than the cell ({need:.0} > {have:.0})", c.text.replace('\n', "/")));
                        }
                        if c.x - c.w / 2.0 < -2.0 || c.x + c.w / 2.0 > 362.0 || c.y - c.h / 2.0 < -2.0 || c.y + c.h / 2.0 > self.height + 2.0 {
                            warn("cell is off the canvas".into());
                        }
                    }
                    Item::Text(t) => {
                        let w = text_width(&t.text, t.size) * if t.mono { 1.0 } else { 0.92 };
                        let (l, r) = match t.anchor {
                            crate::item::Anchor::Start => (t.x, t.x + w),
                            crate::item::Anchor::Middle => (t.x - w / 2.0, t.x + w / 2.0),
                            crate::item::Anchor::End => (t.x - w, t.x),
                        };
                        if l < -4.0 || r > 364.0 {
                            warn(format!("label '{}' is off the canvas horizontally ({l:.0}…{r:.0})", t.text.replace('\n', "/")));
                        }
                        if t.y < 0.0 || t.y > self.height + 4.0 {
                            warn("label is off the canvas vertically".into());
                        }
                    }
                    Item::Dot(d) if d.x - d.r < -2.0 || d.x + d.r > 362.0 || d.y - d.r < -2.0 || d.y + d.r > self.height + 2.0 => warn("circle is off the canvas".into()),
                    Item::Code(c) => {
                        let w = c.lines.iter().map(|l| text_width(l, c.size)).fold(0.0, f64::max);
                        if c.x + w > 364.0 {
                            warn(format!("code is wider than the canvas ({:.0})", c.x + w));
                        }
                        if c.y + c.lines.len() as f64 * c.lh > self.height + 6.0 {
                            warn("code is below the canvas".into());
                        }
                    }
                    _ => {}
                }
            }
        }
        out.dedup();
        out
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::dsl::{arrow, cell, text};
    use crate::tone::{B, G};

    fn two_frames() -> Scene {
        Scene::new(SceneSpec::new(
            &["one", "two"],
            &["first", "second"],
            vec![
                Frame::new().with(cell("a", 10.0, 10.0, "A")).with(text("t", 5.0, 5.0, "first only")),
                Frame::new().with(cell("a", 50.0, 10.0, "A").tone(G)).with(arrow("e", 0.0, 0.0, 9.0, 9.0)),
            ],
        ))
    }

    #[test]
    fn same_id_is_one_object_and_missing_ones_fade_in_place() {
        let s = two_frames();
        assert_eq!(s.steps(), 2);
        assert_eq!(s.item_count(), 3, "a, t and e once each");
        let at = |k: usize, id: &str| s.states[k].iter().find(|i| i.id() == id).cloned().unwrap();
        match at(1, "a") {
            Item::Cell(c) => assert_eq!((c.x, c.tone), (50.0, G)),
            other => panic!("{other:?}"),
        }
        // "t" is absent from the second frame: stays in place but hidden
        match at(1, "t") {
            Item::Text(t) => assert_eq!((t.x, t.o), (5.0, 0.0)),
            other => panic!("{other:?}"),
        }
        // "e" has not yet appeared in the first frame: hidden
        match at(0, "e") {
            Item::Line(l) => assert_eq!(l.o, 0.0),
            other => panic!("{other:?}"),
        }
    }

    #[test]
    fn base_items_are_in_every_frame_and_can_be_overridden() {
        let s = Scene::new(
            SceneSpec::new(&["a", "b"], &["1", "2"], vec![Frame::new(), Frame::new().with(cell("k", 9.0, 9.0, "new").tone(B))]).base(Frame::new().with(cell("k", 1.0, 1.0, "base"))),
        );
        let x = |k: usize| match &s.states[k][0] {
            Item::Cell(c) => (c.x, c.text.clone()),
            _ => unreachable!(),
        };
        assert_eq!(x(0), (1.0, "base".into()));
        assert_eq!(x(1), (9.0, "new".into()));
    }

    #[test]
    fn default_cues_leave_room_for_every_step() {
        assert_eq!(two_frames().cues, vec![5.0]);
        assert_eq!(default_cues(4), vec![5.0, 13.0, 21.0]);
        assert!(default_cues(1).is_empty());
    }

    fn fails(spec: SceneSpec, needle: &str) {
        let e = Scene::compile(&spec).unwrap_err().0;
        assert!(e.contains(needle), "{e}");
    }

    #[test]
    fn data_errors_are_reported_not_hidden() {
        fails(SceneSpec::new(&["a", "b"], &["one"], vec![Frame::new(), Frame::new()]), "captions 1, frames 2");
        fails(SceneSpec::new(&["a", "b"], &["1", "2"], vec![Frame::new().with(cell("x", 0.0, 0.0, "")), Frame::new().with(text("x", 0.0, 0.0, ""))]), "changes item kind");
        fails(SceneSpec::new(&["a"], &["1"], vec![Frame::new().with(cell("x", f64::NAN, 0.0, ""))]), "x = NaN");
        fails(SceneSpec::new(&["a", "b"], &["1", "2"], vec![Frame::new(), Frame::new()]).cues(&[]), "step cues");
    }

    #[test]
    fn lint_finds_overflowing_text_and_items_off_canvas() {
        let ok = Scene::new(SceneSpec::new(&["a"], &["1"], vec![Frame::new().with(cell("a", 50.0, 50.0, "ok")).with(text("t", 180.0, 20.0, "short"))]));
        assert!(ok.lint().is_empty(), "{:?}", ok.lint());
        let bad = Scene::new(SceneSpec::new(
            &["a"],
            &["1"],
            vec![Frame::new().with(cell("w", 50.0, 50.0, "very long caption")).with(text("t", 5.0, 20.0, "caption at the edge холста, не влезает")).with(cell("o", 400.0, 50.0, "x"))],
        ));
        let l = bad.lint();
        assert_eq!(l.len(), 3, "{l:?}");
        assert!(l.iter().any(|m| m.contains("wider than the cell")) && l.iter().any(|m| m.contains("off the canvas")));
    }

    #[test]
    fn spec_survives_json() {
        let spec = SceneSpec::new(&["one"], &["uno"], vec![Frame::new().with(cell("a", 1.0, 2.0, "A").tone(G))]).height(200.0);
        let json = serde_json::to_string(&spec).unwrap();
        assert!(!json.contains("step_ms"), "defaults are not written: {json}");
        assert_eq!(serde_json::from_str::<SceneSpec>(&json).unwrap(), spec);
    }
}
