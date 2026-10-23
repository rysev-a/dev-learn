//! Сцена: описание ([`SceneSpec`] — это данные, их хранит бэкенд) и компиляция ([`Scene`] — состояние каждого элемента на
//! каждом шаге, готовое к отрисовке).
//!
//! `frames[k]` — элементы, видимые на шаге `k`. Элемент с тем же `id` в соседних кадрах — один и тот же объект на экране:
//! он плавно переезжает, меняет цвет и гаснет (если в кадре его нет); всё это делают CSS-переходы (`.a-t`).

use std::collections::HashMap;
use std::fmt;

use serde::{Deserialize, Serialize};

use crate::item::Item;

/// Кадр: список элементов, видимых на шаге.
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

/// Описание сцены: так она хранится в базе и приходит клиенту.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct SceneSpec {
    /// названия шагов (кнопки над схемой)
    pub labels: Vec<String>,
    /// подпись каждого шага (под схемой)
    pub captions: Vec<String>,
    pub frames: Vec<Frame>,
    /// элементы, которые есть в каждом кадре (если кадр не переопределил их по `id`)
    #[serde(default, skip_serializing_if = "is_empty_frame")]
    pub base: Frame,
    /// секунды от начала абзаца, когда наступают шаги 1, 2, …; по умолчанию 5, 13, 21 …
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cues: Option<Vec<f64>>,
    /// длительность шага без озвучки, мс
    #[serde(default = "step_ms", skip_serializing_if = "is_default_ms")]
    pub step_ms: u32,
    /// высота холста (ширина всегда 360)
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

/// Ошибка в данных сцены — ошибка автора: её находят тесты содержимого и проверка при сиде.
#[derive(Clone, Debug, PartialEq)]
pub struct SceneError(pub String);

impl fmt::Display for SceneError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for SceneError {}

/// Скомпилированная сцена: для каждого шага — состояние каждого элемента (в порядке первого появления).
#[derive(Clone, Debug, PartialEq)]
pub struct Scene {
    pub labels: Vec<String>,
    pub captions: Vec<String>,
    pub cues: Vec<f64>,
    pub step_ms: u32,
    pub height: f64,
    /// `states[k][i]` — элемент `i` на шаге `k`
    pub states: Vec<Vec<Item>>,
}

fn default_cues(steps: usize) -> Vec<f64> {
    (0..steps.saturating_sub(1)).map(|i| 5.0 + i as f64 * 8.0).collect()
}

impl Scene {
    /// Компиляция с проверкой данных: число названий и подписей равно числу кадров, у `id` не меняется вид элемента,
    /// числа конечны, метки шагов возрастают.
    pub fn compile(spec: &SceneSpec) -> Result<Scene, SceneError> {
        let name = spec.labels.first().map_or("?", String::as_str);
        let err = |msg: String| SceneError(format!("сцена «{name}…»: {msg}"));
        if spec.frames.is_empty() {
            return Err(err("нет кадров".into()));
        }
        if spec.labels.len() != spec.frames.len() {
            return Err(err(format!("названий шагов {}, кадров {}", spec.labels.len(), spec.frames.len())));
        }
        if spec.captions.len() != spec.frames.len() {
            return Err(err(format!("подписей {}, кадров {}", spec.captions.len(), spec.frames.len())));
        }
        if let Some(c) = &spec.cues {
            if c.len() + 1 < spec.frames.len() || c.windows(2).any(|w| w[0] >= w[1]) {
                return Err(err(format!("метки шагов {c:?} не подходят к {} кадрам", spec.frames.len())));
            }
        }

        let in_frame = |f: &Frame| spec.base.0.iter().chain(f.0.iter()).cloned().collect::<Vec<_>>();
        // кадр = base + элементы кадра; повторный id перекрывает предыдущий
        let mut full: Vec<HashMap<String, Item>> = Vec::with_capacity(spec.frames.len());
        let mut order: Vec<String> = Vec::new();
        let mut first: HashMap<String, Item> = HashMap::new();
        for (k, f) in spec.frames.iter().enumerate() {
            let mut m = HashMap::new();
            for it in in_frame(f) {
                if let Some((key, v)) = it.numbers().into_iter().find(|(_, v)| !v.is_finite()) {
                    return Err(err(format!("кадр {k}, элемент {}: {key} = {v}", it.id())));
                }
                let id = it.id().to_string();
                match first.get(&id) {
                    None => {
                        first.insert(id.clone(), it.clone());
                        order.push(id.clone());
                    }
                    Some(prev) if prev.kind() != it.kind() => {
                        return Err(err(format!("кадр {k}: у id «{id}» меняется вид элемента ({} → {})", prev.kind(), it.kind())));
                    }
                    Some(_) => {}
                }
                m.insert(id, it);
            }
            full.push(m);
        }
        // чего нет в кадре: последнее показанное состояние, но невидимое; до первого появления — первое состояние, невидимое
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

    /// Компиляция для авторов сцен: ошибка в данных — паника с понятным сообщением.
    pub fn new(spec: SceneSpec) -> Scene {
        Scene::compile(&spec).unwrap_or_else(|e| panic!("{e}"))
    }

    pub fn steps(&self) -> usize {
        self.states.len()
    }

    /// Сколько элементов в сцене (по `id`).
    pub fn item_count(&self) -> usize {
        self.states.first().map_or(0, Vec::len)
    }
}

/// Ширина строки моноширинным шрифтом `size` (приблизительно: 0,6 от кегля на символ).
fn text_width(text: &str, size: f64) -> f64 {
    text.split('\n').map(|l| l.chars().count()).max().unwrap_or(0) as f64 * size * 0.56
}

impl Scene {
    /// Проверка раскладки «текст влезает в ячейки, ничего не за холстом»: приблизительная, по ширине символов.
    /// Возвращает замечания (пусто — всё в порядке); элементы с нулевой прозрачностью не проверяются.
    pub fn lint(&self) -> Vec<String> {
        let mut out = Vec::new();
        let name = self.labels.first().map_or("?", String::as_str);
        for (k, row) in self.states.iter().enumerate() {
            for it in row.iter().filter(|i| i.opacity() > 0.0) {
                let mut warn = |msg: String| out.push(format!("сцена «{name}…», шаг {k}, «{}»: {msg}", it.id()));
                match it {
                    Item::Cell(c) => {
                        let (need, have) = (text_width(&c.text, c.size), c.w);
                        if need > have + 8.0 {
                            warn(format!("подпись «{}» шире ячейки ({need:.0} > {have:.0})", c.text.replace('\n', "/")));
                        }
                        if c.x - c.w / 2.0 < -2.0 || c.x + c.w / 2.0 > 362.0 || c.y - c.h / 2.0 < -2.0 || c.y + c.h / 2.0 > self.height + 2.0 {
                            warn("ячейка выходит за холст".into());
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
                            warn(format!("подпись «{}» выходит за холст по ширине ({l:.0}…{r:.0})", t.text.replace('\n', "/")));
                        }
                        if t.y < 0.0 || t.y > self.height + 4.0 {
                            warn("подпись выходит за холст по высоте".into());
                        }
                    }
                    Item::Dot(d) if d.x - d.r < -2.0 || d.x + d.r > 362.0 || d.y - d.r < -2.0 || d.y + d.r > self.height + 2.0 => warn("круг выходит за холст".into()),
                    Item::Code(c) => {
                        let w = c.lines.iter().map(|l| text_width(l, c.size)).fold(0.0, f64::max);
                        if c.x + w > 364.0 {
                            warn(format!("код шире холста ({:.0})", c.x + w));
                        }
                        if c.y + c.lines.len() as f64 * c.lh > self.height + 6.0 {
                            warn("код ниже холста".into());
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
            &["раз", "два"],
            &["первый", "второй"],
            vec![
                Frame::new().with(cell("a", 10.0, 10.0, "A")).with(text("t", 5.0, 5.0, "только в первом")),
                Frame::new().with(cell("a", 50.0, 10.0, "A").tone(G)).with(arrow("e", 0.0, 0.0, 9.0, 9.0)),
            ],
        ))
    }

    #[test]
    fn same_id_is_one_object_and_missing_ones_fade_in_place() {
        let s = two_frames();
        assert_eq!(s.steps(), 2);
        assert_eq!(s.item_count(), 3, "a, t и e — по одному разу");
        let at = |k: usize, id: &str| s.states[k].iter().find(|i| i.id() == id).cloned().unwrap();
        match at(1, "a") {
            Item::Cell(c) => assert_eq!((c.x, c.tone), (50.0, G)),
            other => panic!("{other:?}"),
        }
        // «t» нет во втором кадре: остаётся на месте, но невидим
        match at(1, "t") {
            Item::Text(t) => assert_eq!((t.x, t.o), (5.0, 0.0)),
            other => panic!("{other:?}"),
        }
        // «e» ещё не появилась в первом кадре: невидима
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
        fails(SceneSpec::new(&["a", "b"], &["one"], vec![Frame::new(), Frame::new()]), "подписей 1, кадров 2");
        fails(SceneSpec::new(&["a", "b"], &["1", "2"], vec![Frame::new().with(cell("x", 0.0, 0.0, "")), Frame::new().with(text("x", 0.0, 0.0, ""))]), "меняется вид элемента");
        fails(SceneSpec::new(&["a"], &["1"], vec![Frame::new().with(cell("x", f64::NAN, 0.0, ""))]), "x = NaN");
        fails(SceneSpec::new(&["a", "b"], &["1", "2"], vec![Frame::new(), Frame::new()]).cues(&[]), "метки шагов");
    }

    #[test]
    fn lint_finds_overflowing_text_and_items_off_canvas() {
        let ok = Scene::new(SceneSpec::new(&["a"], &["1"], vec![Frame::new().with(cell("a", 50.0, 50.0, "ok")).with(text("t", 180.0, 20.0, "коротко"))]));
        assert!(ok.lint().is_empty(), "{:?}", ok.lint());
        let bad = Scene::new(SceneSpec::new(
            &["a"],
            &["1"],
            vec![Frame::new().with(cell("w", 50.0, 50.0, "очень длинная подпись")).with(text("t", 5.0, 20.0, "подпись у самого края холста, не влезает")).with(cell("o", 400.0, 50.0, "x"))],
        ));
        let l = bad.lint();
        assert_eq!(l.len(), 3, "{l:?}");
        assert!(l.iter().any(|m| m.contains("шире ячейки")) && l.iter().any(|m| m.contains("за холст")));
    }

    #[test]
    fn spec_survives_json() {
        let spec = SceneSpec::new(&["раз"], &["один"], vec![Frame::new().with(cell("a", 1.0, 2.0, "A").tone(G))]).height(200.0);
        let json = serde_json::to_string(&spec).unwrap();
        assert!(!json.contains("step_ms"), "умолчания не пишутся: {json}");
        assert_eq!(serde_json::from_str::<SceneSpec>(&json).unwrap(), spec);
    }
}
