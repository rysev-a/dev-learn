//! Данные упражнений книги «Компьютерные сети» и серверная проверка присланного решения.
//!
//! Файл данных главы — `labs/net/<книга>-<глава:02>.json` ([`LabChapter`]): у каждого упражнения условие, подсказка и
//! `spec` — исходная сеть, цели, шаги эталонного решения и разрешённые инструменты. Клиенту `spec.solution`
//! не отдаётся; сервер проверяет присланное состояние сети функцией [`verify`].

use crate::check::{apply_ops, check_goals, Goal, GoalResult, Step};
use crate::types::*;
use serde::{Deserialize, Serialize};
use std::path::Path;

/// Номер книги «Компьютерные сети».
pub const NET_BOOK: u32 = 15;

fn is_false(b: &bool) -> bool {
    !*b
}

/// Инструменты, открытые в упражнении (формы в карточке устройства и панель «Кабель»).
#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
pub struct Tools {
    #[serde(default, skip_serializing_if = "is_false")]
    pub cable: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub nat: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub fw: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub dns: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub http: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub tls: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub tcp: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub queue: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub proxy: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub lb: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub rproxy: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub ssh: bool,
    #[serde(default, skip_serializing_if = "is_false")]
    pub vpn: bool,
}

impl Tools {
    /// Включить инструмент по имени; `false` — такого инструмента нет.
    pub fn set(&mut self, name: &str, on: bool) -> bool {
        let slot = match name {
            "cable" => &mut self.cable,
            "nat" => &mut self.nat,
            "fw" => &mut self.fw,
            "dns" => &mut self.dns,
            "http" => &mut self.http,
            "tls" => &mut self.tls,
            "tcp" => &mut self.tcp,
            "queue" => &mut self.queue,
            "proxy" => &mut self.proxy,
            "lb" => &mut self.lb,
            "rproxy" => &mut self.rproxy,
            "ssh" => &mut self.ssh,
            "vpn" => &mut self.vpn,
            _ => return false,
        };
        *slot = on;
        true
    }
}

/// Содержимое упражнения: исходная сеть, цели и эталонное решение.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct NetSpec {
    #[serde(default)]
    pub tools: Tools,
    pub start: NetState,
    pub goals: Vec<Goal>,
    /// Шаги эталона; клиенту сервер их не отдаёт, поэтому поле необязательно.
    #[serde(default)]
    pub solution: Vec<Step>,
}

/// Упражнение главы.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub title: String,
    pub statement: String,
    pub hint: String,
    pub spec: NetSpec,
}

/// Файл данных главы.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct LabChapter {
    pub book: u32,
    pub chapter: u32,
    /// Вид лаборатории: «net».
    pub lab: String,
    pub tasks: Vec<Task>,
}

impl LabChapter {
    /// Разобрать файл данных.
    pub fn from_json(s: &str) -> Result<LabChapter, String> {
        let c: LabChapter = serde_json::from_str(s).map_err(|e| format!("файл главы: {e}"))?;
        if c.lab != "net" {
            return Err(format!("файл главы: ожидалась лаборатория «net», а не «{}»", c.lab));
        }
        Ok(c)
    }

    /// Прочитать файл данных с диска.
    pub fn load(path: &Path) -> Result<LabChapter, String> {
        let s = std::fs::read_to_string(path).map_err(|e| format!("{}: {e}", path.display()))?;
        Self::from_json(&s).map_err(|e| format!("{}: {e}", path.display()))
    }

    /// Имя файла главы: `15-03.json`.
    pub fn file_name(&self) -> String {
        format!("{}-{:02}.json", self.book, self.chapter)
    }

    /// Упражнение по id.
    pub fn task(&self, id: &str) -> Option<&Task> {
        self.tasks.iter().find(|t| t.id == id)
    }
}

/// Прочитать все главы каталога данных (`*.json`), по порядку глав.
pub fn load_dir(dir: &Path) -> Result<Vec<LabChapter>, String> {
    let mut files: Vec<_> = std::fs::read_dir(dir)
        .map_err(|e| format!("{}: {e}", dir.display()))?
        .filter_map(|e| e.ok())
        .map(|e| e.path())
        .filter(|p| p.extension().map(|x| x == "json").unwrap_or(false))
        .collect();
    files.sort();
    let mut out = Vec::new();
    for f in files {
        out.push(LabChapter::load(&f)?);
    }
    out.sort_by_key(|c| (c.book, c.chapter));
    Ok(out)
}

impl NetSpec {
    /// Исходная сеть упражнения (чистая копия без кэшей).
    pub fn start_state(&self) -> NetState {
        self.start.stripped()
    }

    /// Сеть после шагов эталонного решения.
    pub fn solved_state(&self) -> Result<NetState, String> {
        let mut s = self.start_state();
        apply_ops(&mut s, &self.solution)?;
        Ok(s)
    }
}

/// Итог проверки по одной цели.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct GoalVerdict {
    pub id: String,
    pub text: String,
    pub ok: bool,
    pub detail: String,
}

/// Итог проверки решения: все ли цели выполнены и что с каждой.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Verdict {
    pub ok: bool,
    /// Присланное решение не годится вообще (чужие устройства, испорченный JSON) — текст причины.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
    pub goals: Vec<GoalVerdict>,
}

impl Verdict {
    fn rejected(e: impl Into<String>) -> Verdict {
        Verdict { ok: false, error: Some(e.into()), goals: vec![] }
    }

    fn from_results(rs: Vec<GoalResult>) -> Verdict {
        let ok = !rs.is_empty() && rs.iter().all(|r| r.ok);
        Verdict {
            ok,
            error: None,
            goals: rs.into_iter().map(|r| GoalVerdict { id: r.id, text: r.text, ok: r.ok, detail: r.detail }).collect(),
        }
    }
}

fn default_cable(l: &Link) -> bool {
    l.km == 0.01 && l.mbps == 1000.0 && l.mtu.is_none() && l.loss.is_none()
}

/// Присланное состояние — то же упражнение: те же устройства, закрытые устройства не тронуты, кабели меняются
/// только при открытом инструменте «Кабель» (и только обычными кабелями).
pub fn check_integrity(spec: &NetSpec, sub: &NetState) -> Result<(), String> {
    sub.validate()?;
    let start = &spec.start;
    if sub.devices.len() != start.devices.len() {
        return Err("набор устройств не совпадает с упражнением".into());
    }
    for d0 in start.devices.iter() {
        let Some(d) = sub.devices.get(&d0.id) else { return Err(format!("нет устройства «{}»", d0.id)) };
        if d.kind != d0.kind || d.name != d0.name {
            return Err(format!("устройство «{}» подменено", d0.id));
        }
        if d0.locked {
            let mut same = d.clone();
            same.x = d0.x;
            same.y = d0.y;
            // знание хоста об SSH-ключах — состояние клиента, а не настройка
            same.known_hosts = d0.known_hosts.clone();
            if same != *d0 {
                return Err(format!("устройство «{}» закрыто для настройки, а его изменили", d0.name));
            }
        }
    }
    if sub.pki != start.pki {
        return Err("инфраструктура ключей изменена".into());
    }
    let same_links = sub.links.len() == start.links.len() && start.links.iter().all(|l| sub.links.contains(l));
    if !same_links {
        if !spec.tools.cable {
            return Err("в этом упражнении кабели менять нельзя".into());
        }
        for l in &sub.links {
            if !start.links.contains(l) && !default_cable(l) {
                return Err("кабель с необычными свойствами".into());
            }
        }
    }
    Ok(())
}

/// Проверить присланное решение: целостность и цели на чистой копии сети.
pub fn verify(spec: &NetSpec, submitted: &NetState) -> Verdict {
    if let Err(e) = check_integrity(spec, submitted) {
        return Verdict::rejected(e);
    }
    Verdict::from_results(check_goals(submitted, &spec.goals))
}

/// То же для JSON-строки (то, что клиент шлёт на `PUT /api/exercises/15/<глава>/<id>/solved`).
pub fn verify_json(spec: &NetSpec, solution: &str) -> Verdict {
    match crate::model::state_from_json(solution) {
        Ok(s) => verify(spec, &s),
        Err(e) => Verdict::rejected(e),
    }
}
