//! Модель размещения машин по узлам NUMA (глава 11).
//!
//! На хосте несколько узлов (в упражнении — два по 8 ядер и 32 ГиБ). У машины выбирают, где работают её vCPU и где лежит
//! память: узел, либо «растянуть» (пополам). Доля удалённых обращений: свой узел — 0; процессоры и память на разных узлах — 1;
//! что-то растянуто, а другое нет — 0,5; растянуто всё — 0,5, а с виртуальной топологией NUMA гость сам размещает данные
//! ближе — 0,25.
//!
//! Цель — по одной на сценарий: принятое размещение помещается в узлы, а средняя (по vCPU) доля удалённых обращений
//! не больше [`Scenario::max`].

use std::collections::BTreeMap;
use std::fmt;

use serde::{Deserialize, Serialize};

use crate::error::SpecError;
use crate::goal::Goal;

/// Узел хоста.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Node {
    /// Ядер на узле.
    pub cores: u32,
    /// Памяти на узле, ГиБ.
    pub mem: u32,
}

/// Виртуальная машина сценария.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Vm {
    /// Имя машины.
    pub name: String,
    /// Число vCPU.
    pub vcpus: u32,
    /// Память, ГиБ.
    pub mem: u32,
}

/// Куда поставлены процессоры или память машины.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
pub enum Place {
    /// Узел с таким номером.
    Node(u8),
    /// Растянуть пополам по всем узлам.
    Wide,
}

impl From<Place> for String {
    fn from(p: Place) -> String {
        match p {
            Place::Node(i) => i.to_string(),
            Place::Wide => "wide".to_string(),
        }
    }
}

impl TryFrom<String> for Place {
    type Error = String;
    fn try_from(s: String) -> Result<Place, String> {
        if s == "wide" {
            return Ok(Place::Wide);
        }
        s.parse::<u8>().map(Place::Node).map_err(|_| format!("размещение «{s}»: ожидается номер узла или «wide»"))
    }
}

impl fmt::Display for Place {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Place::Node(i) => write!(f, "{i}"),
            Place::Wide => f.write_str("wide"),
        }
    }
}

/// Размещение одной машины.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Placement {
    /// Где работают vCPU.
    pub cpu: Place,
    /// Где лежит память.
    pub mem: Place,
    /// Виртуальная топология NUMA для растянутой машины.
    pub vnuma: bool,
}

/// Размещение всех машин сценария: имя → размещение.
pub type Plan = BTreeMap<String, Placement>;

/// Сценарий: машины, цель и допустимая доля удалённых обращений.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Scenario {
    /// Идентификатор (он же идентификатор цели).
    pub id: String,
    /// Название вкладки.
    pub title: String,
    /// Машины.
    pub vms: Vec<Vm>,
    /// Текст цели.
    pub goal: String,
    /// Допустимая средняя доля удалённых обращений (0…1).
    pub max: f64,
}

impl Scenario {
    /// Цель упражнения по этому сценарию.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.goal.clone())
    }
}

/// Загрузка узла.
#[derive(Clone, Copy, Debug, PartialEq, Serialize, Deserialize)]
pub struct Load {
    /// Занято ядер.
    pub cores: f64,
    /// Занято памяти, ГиБ.
    pub mem: f64,
}

/// Оценка размещения.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Evaluation {
    /// Загрузка узлов.
    pub load: Vec<Load>,
    /// Какой-то узел перегружен (ядра или память).
    pub over: bool,
    /// Доля удалённых обращений каждой машины (в порядке машин сценария).
    pub per: Vec<(String, f64)>,
    /// Средняя доля удалённых обращений, взвешенная по vCPU.
    pub avg: f64,
}

/// Доля удалённых обращений для размещения (`vnuma` — виртуальная топология).
pub fn remote(cpu: Place, mem: Place, vnuma: bool) -> f64 {
    match (cpu, mem) {
        (Place::Wide, Place::Wide) => {
            if vnuma {
                0.25
            } else {
                0.5
            }
        }
        (Place::Wide, _) | (_, Place::Wide) => 0.5,
        (a, b) => {
            if a == b {
                0.0
            } else {
                1.0
            }
        }
    }
}

// Какая доля машины приходится на узел `i`.
fn share(nodes: usize, place: Place, i: usize) -> f64 {
    match place {
        Place::Wide => 1.0 / nodes as f64,
        Place::Node(n) => {
            if usize::from(n) == i {
                1.0
            } else {
                0.0
            }
        }
    }
}

/// Оценить размещение `plan` машин `vms` на узлах `nodes`.
/// Ошибка — для машины нет размещения или оно указывает на несуществующий узел.
pub fn evaluate(nodes: &[Node], vms: &[Vm], plan: &Plan) -> Result<Evaluation, SpecError> {
    let mut load = vec![Load { cores: 0.0, mem: 0.0 }; nodes.len()];
    let mut weighted = 0.0;
    let mut total = 0.0;
    let mut per = Vec::with_capacity(vms.len());
    for vm in vms {
        let p = plan.get(&vm.name).ok_or_else(|| SpecError::new(format!("нет размещения машины {}", vm.name)))?;
        for place in [p.cpu, p.mem] {
            if let Place::Node(n) = place {
                if usize::from(n) >= nodes.len() {
                    return Err(SpecError::new(format!("машина {}: нет узла {n}", vm.name)));
                }
            }
        }
        for (i, l) in load.iter_mut().enumerate() {
            l.cores += f64::from(vm.vcpus) * share(nodes.len(), p.cpu, i);
            l.mem += f64::from(vm.mem) * share(nodes.len(), p.mem, i);
        }
        let r = remote(p.cpu, p.mem, p.vnuma);
        per.push((vm.name.clone(), r));
        weighted += r * f64::from(vm.vcpus);
        total += f64::from(vm.vcpus);
    }
    let over = load.iter().zip(nodes).any(|(l, n)| l.cores > f64::from(n.cores) || l.mem > f64::from(n.mem));
    Ok(Evaluation { load, over, per, avg: if total != 0.0 { weighted / total } else { 0.0 } })
}

/// Размещение по умолчанию: всё на узле 0.
pub fn default_plan(vms: &[Vm]) -> Plan {
    vms.iter().map(|v| (v.name.clone(), Placement { cpu: Place::Node(0), mem: Place::Node(0), vnuma: false })).collect()
}

/// Исход кнопки «Принять размещение».
#[derive(Clone, Debug, PartialEq)]
pub enum Accept {
    /// Не помещается: на каком-то узле не хватает ядер или памяти.
    Over,
    /// Слишком много удалённых обращений.
    TooRemote {
        /// Доля удалённых обращений.
        avg: f64,
        /// Допустимая доля.
        max: f64,
    },
    /// Принято.
    Ok {
        /// Доля удалённых обращений.
        avg: f64,
    },
}

/// Принять размещение сценария: цель достигнута при [`Accept::Ok`].
pub fn accept(nodes: &[Node], sc: &Scenario, plan: &Plan) -> Result<Accept, SpecError> {
    let ev = evaluate(nodes, &sc.vms, plan)?;
    Ok(if ev.over {
        Accept::Over
    } else if ev.avg > sc.max + 1e-9 {
        Accept::TooRemote { avg: ev.avg, max: sc.max }
    } else {
        Accept::Ok { avg: ev.avg }
    })
}

/// Узлы упражнения по умолчанию: два по 8 ядер и 32 ГиБ.
pub fn default_nodes() -> Vec<Node> {
    vec![Node { cores: 8, mem: 32 }; 2]
}

/// Сценарии по умолчанию (упражнение главы 11).
pub fn default_scenarios() -> Vec<Scenario> {
    let vm = |name: &str, vcpus: u32, mem: u32| Vm { name: name.into(), vcpus, mem };
    vec![
        Scenario {
            id: "small".into(),
            title: "Четыре небольшие машины".into(),
            vms: vec![vm("A", 4, 16), vm("B", 4, 12), vm("C", 4, 16), vm("D", 4, 12)],
            goal: "Всё помещается, и удалённых обращений нет совсем (0%)".into(),
            max: 0.0,
        },
        Scenario {
            id: "wide".into(),
            title: "Большая машина".into(),
            vms: vec![vm("E", 12, 40), vm("F", 2, 8), vm("G", 2, 8)],
            goal: "Всё помещается, а средняя доля удалённых обращений (по vCPU) не больше 20%".into(),
            max: 0.2,
        },
    ]
}
