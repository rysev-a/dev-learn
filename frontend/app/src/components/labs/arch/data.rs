//! Данные лаборатории на клиенте: сценарии всех глав со схемами (из них собираются блоки и подсказки о закрытых
//! элементах) и решённое учеником в других главах (аналог `hydrate.ts` в React: составные блоки собираются из
//! решённых упражнений, а палитра открывает составные элементы).
//!
//! Сценарии одинаковы для всех — кэшируются до перезагрузки страницы; прогресс кэшируется по токену сессии и
//! обновляется, когда ученик решает упражнение. Запросы идут параллельно (`join_all`).

use std::{
    cell::RefCell,
    collections::HashSet,
    future::Future,
    pin::Pin,
    sync::Arc,
    task::Poll,
};

use api::{ApiError, Client};
use archlab::{
    exercise::{LabChapter, Spec, Task, ARCH_BOOK},
    registry, ArchLab, DraftStore,
};
use leptos::{prelude::*, task::spawn_local};

use super::common::Lib;
use crate::{hooks::{client, Load}, session::Session};

/// Все будущие одновременно; результаты — в порядке запросов.
pub async fn join_all<T, F: Future<Output = T>>(futures: Vec<F>) -> Vec<T> {
    let mut futures: Vec<Pin<Box<F>>> = futures.into_iter().map(Box::pin).collect();
    let mut done: Vec<Option<T>> = futures.iter().map(|_| None).collect();
    std::future::poll_fn(move |cx| {
        let mut pending = false;
        for (f, slot) in futures.iter_mut().zip(done.iter_mut()) {
            if slot.is_none() {
                match f.as_mut().poll(cx) {
                    Poll::Ready(v) => *slot = Some(v),
                    Poll::Pending => pending = true,
                }
            }
        }
        if pending {
            Poll::Pending
        } else {
            Poll::Ready(done.iter_mut().filter_map(Option::take).collect())
        }
    })
    .await
}

/// Что известно о решённом: упражнения `(раздел, id)` со статусом «выполнено» и их решения-черновики `(глава, id, JSON)`.
#[derive(Clone, Default, Debug)]
pub struct Progress {
    pub solved: HashSet<(String, String)>,
    pub drafts: Vec<(u32, String, String)>,
}

impl Progress {
    /// Запомнить решённое упражнение главы `chapter` и его схему.
    fn add(&mut self, chapter: u32, slug: &str, id: &str, json: &str) {
        self.solved.insert((slug.to_string(), id.to_string()));
        self.drafts.retain(|(c, i, _)| !(*c == chapter && i == id));
        self.drafts.push((chapter, id.to_string(), json.to_string()));
    }
}

#[derive(Default)]
struct Cache {
    lab: Option<Arc<ArchLab>>,
    progress: Option<(Option<String>, Progress)>,
}

thread_local! {
    static CACHE: RefCell<Cache> = RefCell::new(Cache::default());
}

/// Главы со схемами (6–14): в них лежат блоки и составные элементы.
fn circuit_chapters() -> Vec<u32> {
    registry::SECTIONS.iter().map(|s| s.chapter).collect()
}

fn broken(what: &str, e: impl std::fmt::Display) -> ApiError {
    ApiError { status: 0, message: format!("{what}: {e}") }
}

/// Движок из сценариев глав, которые прислал сервер (`(номер главы, глава)`): упражнения разбираются в `archlab::Task`.
pub fn build_lab(chapters: Vec<(u32, api::dto::LabChapter)>) -> Result<ArchLab, ApiError> {
    let mut list = Vec::new();
    for (n, ch) in chapters {
        let mut tasks = Vec::new();
        for t in ch.tasks {
            let spec: Spec = serde_json::from_value(t.spec).map_err(|e| broken(&format!("Сценарий «{}» повреждён", t.id), e))?;
            tasks.push(Task { id: t.id, title: t.title, statement: t.statement, hint: t.hint, spec });
        }
        list.push(LabChapter { book: ARCH_BOOK, chapter: n, lab: "arch".into(), tasks });
    }
    ArchLab::from_chapters(list).map_err(|e| broken("Сценарии лаборатории", e))
}

/// Сценарии глав со схемами с сервера и сборка движка.
async fn fetch_lab(c: Client) -> Result<Arc<ArchLab>, ApiError> {
    if let Some(lab) = CACHE.with(|k| k.borrow().lab.clone()) {
        return Ok(lab);
    }
    let reqs = circuit_chapters().into_iter().map(|n| {
        let c = c.clone();
        async move { c.lab_chapter(i64::from(ARCH_BOOK), i64::from(n)).await.map(|ch| (n, ch)) }
    });
    let chapters = join_all(reqs.collect()).await.into_iter().collect::<Result<Vec<_>, _>>()?;
    let lab = Arc::new(build_lab(chapters)?);
    CACHE.with(|k| k.borrow_mut().lab = Some(lab.clone()));
    Ok(lab)
}

/// Статусы и решения ученика по главам со схемами (только выполненные упражнения).
async fn fetch_progress(c: Client, user: Option<String>) -> Result<Progress, ApiError> {
    if let Some((u, p)) = CACHE.with(|k| k.borrow().progress.clone()) {
        if u == user {
            return Ok(p);
        }
    }
    let reqs = circuit_chapters().into_iter().map(|n| {
        let c = c.clone();
        async move { c.chapter_state(i64::from(ARCH_BOOK), i64::from(n)).await.map(|s| (n, s)) }
    });
    let mut progress = Progress::default();
    for res in join_all(reqs.collect()).await {
        let (n, state) = res?;
        let Some(section) = registry::section_of_chapter(n) else { continue };
        for (id, status) in &state.status {
            if status != "ok" {
                continue;
            }
            progress.solved.insert((section.slug.to_string(), id.clone()));
            if let Some(draft) = state.drafts.get(id) {
                progress.drafts.push((n, id.clone(), draft.clone()));
            }
        }
    }
    CACHE.with(|k| k.borrow_mut().progress = Some((user, progress.clone())));
    Ok(progress)
}

/// Движок лаборатории и прогресс ученика: общие для всех упражнений на экране.
#[derive(Clone, Copy)]
pub struct ArchData {
    lab: StoredValue<Arc<ArchLab>>,
    solved: RwSignal<HashSet<(String, String)>>,
    store: RwSignal<DraftStore>,
    user: StoredValue<Option<String>>,
    /// библиотека блоков: открыты те, чьи упражнения решены (пересчитывается при новом решении)
    pub library: Memo<Lib>,
}

impl ArchData {
    fn new(lab: Arc<ArchLab>, progress: Progress, user: Option<String>) -> Self {
        let store = RwSignal::new(DraftStore::from_drafts(&lab, progress.drafts.iter().map(|(c, i, d)| (*c, i.as_str(), d.as_str()))));
        let solved = RwSignal::new(progress.solved);
        let lab = StoredValue::new(lab);
        let library = Memo::new(move |_| Lib(Arc::new(lab.with_value(|l| store.with(|s| l.library(s))))));
        Self { lab, solved, store, user: StoredValue::new(user), library }
    }

    /// Движок (сценарии глав, подсказки).
    pub fn lab(&self) -> Arc<ArchLab> {
        self.lab.get_value()
    }

    /// Решено ли упражнение `id` раздела `slug` (в реактивном контексте — подписка на новые решения).
    pub fn is_solved(&self, slug: &str, id: &str) -> bool {
        self.solved.with(|s| s.contains(&(slug.to_string(), id.to_string())))
    }

    /// Ученик решил упражнение: схема попадает в библиотеку блоков, составные элементы открываются.
    pub fn mark_solved(&self, chapter: u32, slug: &str, id: &str, json: &str) {
        self.solved.update(|s| {
            s.insert((slug.to_string(), id.to_string()));
        });
        self.store.update(|s| {
            s.add(slug, id, json);
        });
        let user = self.user.get_value();
        CACHE.with(|k| {
            let mut k = k.borrow_mut();
            if let Some((u, p)) = k.progress.as_mut() {
                if *u == user {
                    p.add(chapter, slug, id, json);
                }
            }
        });
    }
}

/// Загружает данные лаборатории (параллельно) при открытии упражнения.
pub fn use_arch_data() -> ReadSignal<Load<ArchData>> {
    let (state, set) = signal(Load::<ArchData>::Loading);
    let user = use_context::<Session>().and_then(|s| s.token.get_untracked());
    let c = client();
    spawn_local(async move {
        let (lab, progress) = (fetch_lab(c.clone()).await, fetch_progress(c, user.clone()).await);
        // упражнение могли закрыть, пока шли запросы — тогда записывать некуда
        set.try_set(match (lab, progress) {
            (Ok(lab), Ok(progress)) => Load::Ready(ArchData::new(lab, progress, user)),
            (Err(e), _) | (_, Err(e)) => Load::Failed(e.message),
        });
    });
    state
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_solution_replaces_the_old_draft_of_the_same_exercise() {
        let mut p = Progress::default();
        p.add(6, "simple-circuits", "xor", "{\"a\":1}");
        p.add(6, "simple-circuits", "xor", "{\"a\":2}");
        p.add(6, "simple-circuits", "nand", "{}");
        assert_eq!(p.drafts.len(), 2);
        assert_eq!(p.drafts.iter().find(|d| d.1 == "xor").map(|d| d.2.as_str()), Some("{\"a\":2}"));
        assert!(p.solved.contains(&("simple-circuits".to_string(), "nand".to_string())));
    }

    /// Главы так, как их отдаёт сервер: из сценария убрано эталонное решение.
    fn server_chapters() -> Vec<(u32, api::dto::LabChapter)> {
        let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/arch");
        circuit_chapters()
            .into_iter()
            .map(|n| {
                let text = std::fs::read_to_string(dir.join(format!("14-{n:02}.json"))).expect("файл главы");
                let mut v: serde_json::Value = serde_json::from_str(&text).expect("JSON главы");
                let tasks = v["tasks"].as_array_mut().expect("упражнения");
                for t in tasks.iter_mut() {
                    t["spec"].as_object_mut().expect("сценарий").remove("solution");
                }
                (n, serde_json::from_value(v).expect("глава как её читает клиент"))
            })
            .collect()
    }

    #[test]
    fn client_builds_the_engine_from_what_the_server_sends() {
        let lab = build_lab(server_chapters()).expect("движок собрался");
        assert_eq!(lab.chapters().count(), 9);
        let nand = lab.circuit_task("simple-circuits", "nand").expect("упражнение про NAND");
        assert!(nand.1.solution.is_none(), "эталона у клиента нет");
        assert!(lab.gate_lock_hint(archlab::model::GateType::Xor).contains("Соберите"));
    }

    #[test]
    fn blocks_open_from_the_students_own_solutions_and_the_processor_exercise_accepts_them() {
        use archlab::blocks::Solution;
        // эталонные решения как «решения ученика»: JSON, как их хранит кабинет
        let reference = ArchLab::load_dir(&std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../backend/data/labs/arch")).expect("данные");
        let lab = build_lab(server_chapters()).expect("движок");
        let mut drafts: Vec<(u32, String, String)> = Vec::new();
        for ch in reference.chapters().filter(|c| c.chapter <= 14) {
            for t in &ch.tasks {
                if let Spec::Circuit(c) = &t.spec {
                    if let Some(sol) = &c.solution {
                        drafts.push((ch.chapter, t.id.clone(), serde_json::to_string(sol).expect("JSON решения")));
                    }
                }
            }
        }
        let closed = lab.library(&DraftStore::new());
        assert!(!closed.available("fetch"), "без решений составной блок закрыт");
        let store = DraftStore::from_drafts(&lab, drafts.iter().map(|(c, i, d)| (*c, i.as_str(), d.as_str())));
        let library = lab.library(&store);
        assert!(library.available("fetch") && library.available("sequencer"));
        // процессор из блоков по решению ученика проходит ту же проверку, что на сервере
        let cpu = reference.task(14, "cpu").expect("упражнение «процессор»");
        let Spec::Circuit(spec) = &cpu.spec else { panic!("схема") };
        let Some(Solution::Block(_)) = &spec.solution else { panic!("эталон из блоков") };
        let json = serde_json::to_string(spec.solution.as_ref().expect("эталон")).expect("JSON");
        let verdict = archlab::verify(lab.task(14, "cpu").expect("у клиента тоже есть"), &json, &library);
        assert!(verdict.ok, "{}", verdict.message);
    }

    #[test]
    fn join_all_collects_results_in_order() {
        let futs: Vec<_> = (0..4).map(|i| async move { i * 2 }).collect();
        let out = futures_lite_block_on(join_all(futs));
        assert_eq!(out, vec![0, 2, 4, 6]);
    }

    /// Минимальный исполнитель для готовых будущих (в тесте ничего не ждёт).
    fn futures_lite_block_on<T>(fut: impl Future<Output = T>) -> T {
        let mut cx = std::task::Context::from_waker(std::task::Waker::noop());
        let mut fut = Box::pin(fut);
        loop {
            if let Poll::Ready(v) = fut.as_mut().poll(&mut cx) {
                return v;
            }
        }
    }
}
