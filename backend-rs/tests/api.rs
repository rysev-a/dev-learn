//! Сквозные проверки API на базе SurrealDB в памяти: сид из настоящих исходников курса, вход, прогресс, квизы,
//! ответы, очередь проверок и внутренний API воркера.

use axum::{
    body::Body,
    http::{header, Method, Request, StatusCode},
    Router,
};
use http_body_util::BodyExt;
use say_backend::{build, config::Config, db};
use serde_json::{json, Value};
use tower::ServiceExt;

async fn app(worker_token: &str) -> Router {
    let cfg = Config {
        bind: "127.0.0.1:0".into(),
        surreal_url: "memory".into(),
        data_dir: std::path::PathBuf::from("../backend/app/data"),
        audio_dir: std::env::temp_dir().join("say-rs-test-audio"),
        static_dir: None,
        worker_token: worker_token.into(),
        seed: "auto".into(),
    };
    let database = db::memory().await.unwrap();
    build(database, cfg).await.unwrap().0
}

async fn call(app: &Router, method: Method, uri: &str, token: Option<&str>, body: Option<Value>) -> (StatusCode, Value) {
    let mut req = Request::builder().method(method).uri(uri);
    if let Some(t) = token {
        req = req.header(header::AUTHORIZATION, format!("Bearer {t}"));
    }
    let req = match body {
        Some(b) => req.header(header::CONTENT_TYPE, "application/json").body(Body::from(b.to_string())).unwrap(),
        None => req.body(Body::empty()).unwrap(),
    };
    let res = app.clone().oneshot(req).await.unwrap();
    let status = res.status();
    let bytes = res.into_body().collect().await.unwrap().to_bytes();
    (status, serde_json::from_slice(&bytes).unwrap_or(Value::Null))
}

async fn sign_in(app: &Router, email: &str) -> String {
    let (st, _) = call(app, Method::POST, "/api/auth/signup", None, Some(json!({ "email": email, "password": "correct-horse-1", "name": "Тест" }))).await;
    assert_eq!(st, StatusCode::CREATED);
    let (st, body) = call(app, Method::POST, "/api/auth/login", None, Some(json!({ "email": email, "password": "correct-horse-1" }))).await;
    assert_eq!(st, StatusCode::OK);
    body["token"].as_str().unwrap().to_string()
}

#[tokio::test]
async fn course_content_matches_the_python_backend() {
    let app = app("").await;
    let (st, books) = call(&app, Method::GET, "/api/books", None, None).await;
    assert_eq!(st, StatusCode::OK);
    let books = books.as_array().unwrap();
    assert_eq!(books.len(), 12);
    assert_eq!(books[0]["slug"], "dm");
    assert!(books.iter().all(|b| b["parts_count"].as_i64().unwrap() > 0));

    let (_, course) = call(&app, Method::GET, "/api/books/18/course", None, None).await;
    let last = course.as_array().unwrap().last().unwrap()["chapters"].as_array().unwrap().last().unwrap().clone();
    assert_eq!(last["num"], 24);
    let (st, chapter) = call(&app, Method::GET, &format!("/api/chapters/{}", last["id"]), None, None).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(chapter["lessons"].as_array().unwrap().len(), 13);
    assert_eq!(chapter["lessons"][0]["ord"], 0);
    assert!(chapter["lessons"][0]["audio"].as_str().unwrap().starts_with("/api/lesson/"));
    assert_eq!(call(&app, Method::GET, "/api/chapters/99999", None, None).await.0, StatusCode::NOT_FOUND);

    let (_, tasks) = call(&app, Method::GET, "/api/exercises/13/0", None, None).await;
    assert!(tasks["tasks"].as_array().unwrap().iter().any(|t| t["id"] == "intro-variable"));
    // SQL-задачи приходят вместе с описанием учебных баз
    let (_, sql) = call(&app, Method::GET, "/api/exercises/9/2", None, None).await;
    let first = &sql["tasks"][0];
    assert_eq!(first["mode"], "sql");
    let key = first["dataset"].as_str().unwrap();
    assert!(!sql["datasets"][key]["tables"].as_array().unwrap().is_empty());
    assert_eq!(call(&app, Method::GET, "/api/exercises/9/99", None, None).await.0, StatusCode::NOT_FOUND);
    assert_eq!(call(&app, Method::GET, "/api/nope", None, None).await.0, StatusCode::NOT_FOUND);

    // защищённые маршруты без сессии
    for uri in ["/api/progress", "/api/quizzes/18/24", "/api/answers/12/1", "/api/exercises/13/0/state"] {
        assert_eq!(call(&app, Method::GET, uri, None, None).await.0, StatusCode::UNAUTHORIZED, "{uri}");
    }
}

#[tokio::test]
async fn slides_are_stored_as_data_and_served_per_chapter() {
    let app = app("").await;
    let (st, list) = call(&app, Method::GET, "/api/slides", None, None).await;
    assert_eq!(st, StatusCode::OK);
    let list = list.as_array().unwrap();
    let files = std::fs::read_dir("../backend/app/data/slides").unwrap().count();
    assert_eq!(list.len(), files, "каждый файл главы попал в базу");
    assert!(list.iter().any(|c| c["book"] == 13 && c["chapter"] == 0));

    // схема системного дизайна: сцена из кадров приходит как данные
    let (st, ch) = call(&app, Method::GET, "/api/slides/18/24", None, None).await;
    assert_eq!(st, StatusCode::OK);
    let slides = ch["slides"].as_array().unwrap();
    assert_eq!(slides.len(), 13);
    assert!(ch["rubric"].as_str().unwrap().contains("ГЛАВА 24"));
    let scene = slides[0]["body"].as_array().unwrap().iter().find(|b| b["t"] == "scene").expect("в слайде есть сцена");
    assert!(!scene["frames"].as_array().unwrap().is_empty());
    assert_eq!(scene["labels"].as_array().unwrap().len(), scene["frames"].as_array().unwrap().len());

    // старый формат: блоки вместо сцены
    let (_, py) = call(&app, Method::GET, "/api/slides/13/5", None, None).await;
    let kinds: Vec<&str> = py["slides"][1]["body"].as_array().unwrap().iter().map(|b| b["t"].as_str().unwrap()).collect();
    assert_eq!(kinds, ["code", "label", "cmd", "note"]);

    // ДМ: схемы написаны генераторами на Rust и лежат в данных наравне с остальными
    let (st, dm) = call(&app, Method::GET, "/api/slides/12/1", None, None).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(dm["slides"].as_array().unwrap().len(), 13);
    assert_eq!(call(&app, Method::GET, "/api/slides/99/1", None, None).await.0, StatusCode::NOT_FOUND);
}

#[tokio::test]
async fn lab_solutions_are_checked_by_the_server_engine() {
    let app = app("").await;
    let token = sign_in(&app, "student@mail.com").await;
    // сценарий приходит без эталона
    let (st, lab) = call(&app, Method::GET, "/api/labs/18/2", None, None).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(lab["lab"], "sd");
    let first = &lab["tasks"][0];
    assert!(first["spec"].get("solution").is_none(), "эталон не уходит клиенту");
    assert!(first["spec"]["goals"].as_array().is_some_and(|g| !g.is_empty()));
    assert_eq!(call(&app, Method::GET, "/api/labs/18/99", None, None).await.0, StatusCode::NOT_FOUND);

    // эталон и исходная схема из файла данных
    let file: Value = serde_json::from_slice(&std::fs::read("../backend/app/data/labs/sd/18-02.json").unwrap()).unwrap();
    let task = &file["tasks"][0];
    let id = task["id"].as_str().unwrap();
    let uri = format!("/api/exercises/18/2/{id}/solved");
    let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": task["spec"]["start"].to_string() }))).await;
    assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "исходная схема не решает упражнение: {body}");
    let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": task["spec"]["solution"].to_string() }))).await;
    assert_eq!(st, StatusCode::NO_CONTENT, "{body}");
}

#[tokio::test]
async fn riscv_programs_are_checked_by_running_them() {
    let app = app("").await;
    let token = sign_in(&app, "riscv@mail.com").await;
    let (st, lab) = call(&app, Method::GET, "/api/labs/14/16", None, None).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(lab["lab"], "riscv");
    assert!(lab["tasks"][0]["spec"].get("reference").is_none(), "эталонная программа не уходит клиенту");
    let file: Value = serde_json::from_slice(&std::fs::read("../backend/app/data/labs/arch/14-16.json").unwrap()).unwrap();
    let task = &file["tasks"][0];
    let uri = format!("/api/exercises/14/16/{}/solved", task["id"].as_str().unwrap());
    let (st, _) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": "" }))).await;
    assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "пустая программа не решает");
    let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": task["spec"]["reference"] }))).await;
    assert_eq!(st, StatusCode::NO_CONTENT, "{body}");
}

#[tokio::test]
async fn architecture_lab_accepts_every_reference_solution_in_course_order() {
    let app = app("").await;
    let token = sign_in(&app, "arch@mail.com").await;
    let (mut solved, mut empty_rejected) = (0, 0);
    for chapter in 6..=15 {
        let path = format!("../backend/app/data/labs/arch/14-{chapter:02}.json");
        let file: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        for task in file["tasks"].as_array().unwrap() {
            let uri = format!("/api/exercises/14/{chapter}/{}/solved", task["id"].as_str().unwrap());
            let reference = match &task["spec"]["solution"] {
                Value::String(text) => text.clone(),
                other => other.to_string(),
            };
            // составные блоки открываются решениями самого ученика: порядок курса важен
            let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": reference }))).await;
            assert_eq!(st, StatusCode::NO_CONTENT, "{chapter}/{}: {body}", task["id"]);
            solved += 1;
            let (st, _) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": "{\"gates\":[],\"wires\":[]}" }))).await;
            empty_rejected += usize::from(st == StatusCode::UNPROCESSABLE_ENTITY);
        }
    }
    assert_eq!(solved, 103);
    assert!(empty_rejected > 90, "пустая схема не решает упражнение (отклонено {empty_rejected})");
}

#[tokio::test]
async fn network_lab_accepts_solved_networks_and_rejects_the_starting_ones() {
    let app = app("").await;
    let token = sign_in(&app, "net@mail.com").await;
    let mut dir: Vec<_> = std::fs::read_dir("../backend/app/data/labs/net").unwrap().map(|e| e.unwrap().path()).collect();
    dir.sort();
    let (mut accepted, mut rejected) = (0, 0);
    for path in dir {
        let file: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        let chapter = file["chapter"].as_i64().unwrap();
        for task in file["tasks"].as_array().unwrap() {
            let spec: netlab::NetSpec = serde_json::from_value(task["spec"].clone()).unwrap();
            let uri = format!("/api/exercises/15/{chapter}/{}/solved", task["id"].as_str().unwrap());
            let solved = serde_json::to_string(&spec.solved_state().unwrap()).unwrap();
            let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": solved }))).await;
            assert_eq!(st, StatusCode::NO_CONTENT, "{chapter}/{}: {body}", task["id"]);
            accepted += 1;
            let start = serde_json::to_string(&spec.start_state()).unwrap();
            let (st, _) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": start }))).await;
            rejected += usize::from(st == StatusCode::UNPROCESSABLE_ENTITY);
        }
    }
    assert_eq!(accepted, 79);
    assert_eq!(rejected, 79, "исходная сеть не решает ни одного упражнения");
}

#[tokio::test]
async fn progress_quiz_and_answers() {
    let app = app("").await;
    let token = sign_in(&app, "student@example.com").await;
    let t = Some(token.as_str());

    assert_eq!(call(&app, Method::POST, "/api/progress/slides", t, Some(json!({ "book": 18, "chapter": 24, "slide": 2 }))).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::POST, "/api/progress/slides", t, Some(json!({ "book": 18, "chapter": 24, "slide": 2 }))).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::POST, "/api/progress/slides", t, Some(json!({ "book": 0, "chapter": 24, "slide": 2 }))).await.0, StatusCode::UNPROCESSABLE_ENTITY);

    // квиз: вопросы без ответов, на вопрос отвечают один раз
    let (_, quiz) = call(&app, Method::GET, "/api/quizzes/18/24", t, None).await;
    assert_eq!(quiz["questions"].as_array().unwrap().len(), 5);
    assert!(quiz["questions"][0].get("answer").is_none());
    assert!(quiz["reveal"][0].is_null());
    let (st, first) = call(&app, Method::POST, "/api/quizzes/18/24/answer", t, Some(json!({ "question": 0, "pick": 0 }))).await;
    assert_eq!(st, StatusCode::OK);
    let (_, again) = call(&app, Method::POST, "/api/quizzes/18/24/answer", t, Some(json!({ "question": 0, "pick": 3 }))).await;
    assert_eq!(again["pick"], first["pick"], "повторный ответ ничего не меняет");
    assert_eq!(call(&app, Method::POST, "/api/quizzes/18/24/answer", t, Some(json!({ "question": 0, "pick": 40 }))).await.0, StatusCode::UNPROCESSABLE_ENTITY);
    let (_, quiz) = call(&app, Method::GET, "/api/quizzes/18/24", t, None).await;
    assert!(quiz["reveal"][0]["expl"].as_str().is_some());

    // ответы с вводом: верный запоминается, неверный ничего не раскрывает
    let (_, bad) = call(&app, Method::POST, "/api/answers/12/1/check", t, Some(json!({ "task": 0, "value": "999" }))).await;
    assert_eq!(bad, json!({ "ok": false }));
    let (_, good) = call(&app, Method::POST, "/api/answers/12/1/check", t, Some(json!({ "task": 0, "value": " 1 " }))).await;
    assert_eq!(good, json!({ "ok": true }));

    let (_, progress) = call(&app, Method::GET, "/api/progress", t, None).await;
    assert_eq!(progress["slides"]["18:24"], json!([2]));
    assert_eq!(progress["quiz"]["18:24"][0], first["pick"]);
    assert_eq!(progress["quizRight"]["18:24"], first["right"]);
    assert_eq!(progress["answers"]["12:1"]["0"], "1");

    // сбросы
    assert_eq!(call(&app, Method::DELETE, "/api/progress/quiz?book=18&chapter=24", t, None).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::DELETE, "/api/progress?scope=practice", t, None).await.0, StatusCode::NO_CONTENT);
    let (_, progress) = call(&app, Method::GET, "/api/progress", t, None).await;
    assert_eq!(progress["quiz"], json!({}));
    assert_eq!(progress["answers"], json!({}));
    assert_eq!(progress["slides"]["18:24"], json!([2]), "scope=practice слайды не трогает");
    assert_eq!(call(&app, Method::DELETE, "/api/progress?scope=zzz", t, None).await.0, StatusCode::UNPROCESSABLE_ENTITY);
}

#[tokio::test]
async fn code_jobs_go_through_the_worker_api() {
    let app = app("secret").await;
    let token = sign_in(&app, "coder@example.com").await;
    let t = Some(token.as_str());
    let run = json!({ "book": 13, "chapter": 0, "task": "intro-variable", "code": "year = 1991\nprint(year)" });

    // воркеров нет — проверка недоступна
    assert_eq!(call(&app, Method::POST, "/api/exercises/run", t, Some(run.clone())).await.0, StatusCode::SERVICE_UNAVAILABLE);
    // токен воркера
    let w = |m: Method, uri: &str, tok: Option<&str>, body: Value| {
        let app = app.clone();
        let uri = uri.to_string();
        let tok = tok.map(String::from);
        async move { call(&app, m, &uri, tok.as_deref(), Some(body)).await }
    };
    assert_eq!(w(Method::POST, "/internal/worker/ping", None, json!({ "name": "w1", "lanes": ["light"] })).await.0, StatusCode::UNAUTHORIZED);
    assert_eq!(w(Method::POST, "/internal/worker/ping", Some("wrong"), json!({ "name": "w1", "lanes": ["light"] })).await.0, StatusCode::UNAUTHORIZED);
    assert_eq!(w(Method::POST, "/internal/worker/ping", Some("secret"), json!({ "name": "w1", "lanes": ["light", "heavy"], "slots": 2 })).await.0, StatusCode::NO_CONTENT);
    let (_, status) = call(&app, Method::GET, "/api/exercises/runner/status", None, None).await;
    assert_eq!(status, json!({ "available": true, "queued": 0, "running": 0, "workers": 1 }));

    // постановка → очередь → воркер забирает → результат → попытка и статус записаны
    let (st, queued) = call(&app, Method::POST, "/api/exercises/run", t, Some(run.clone())).await;
    assert_eq!(st, StatusCode::ACCEPTED);
    assert_eq!(queued["state"], "queued");
    let id = queued["id"].as_str().unwrap().to_string();
    assert_eq!(call(&app, Method::POST, "/api/exercises/run", t, Some(run.clone())).await.0, StatusCode::TOO_MANY_REQUESTS, "одна проверка на пользователя");

    let (st, job) = w(Method::POST, "/internal/worker/claim", Some("secret"), json!({ "name": "w1", "lanes": ["light"], "wait": 0 })).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(job["id"], id);
    assert_eq!(job["task"]["id"], "intro-variable");
    assert!(job["task"]["expected"].is_array(), "в задание для воркера попадает spec: {job}");
    assert_eq!(call(&app, Method::GET, &format!("/api/exercises/run/{id}"), t, None).await.1["state"], "running");
    assert_eq!(w(Method::POST, "/internal/worker/jobs/zzz/result", Some("secret"), json!({ "name": "w1", "result": {} })).await.0, StatusCode::CONFLICT);
    assert_eq!(w(Method::POST, &format!("/internal/worker/jobs/{id}/result"), Some("secret"), json!({ "name": "other", "result": {} })).await.0, StatusCode::CONFLICT);
    let result = json!({ "status": "ok", "results": [{ "ok": true, "got": "1991\n", "expected": "1991\n", "error": null }], "stdout": "", "stderr": "" });
    assert_eq!(w(Method::POST, &format!("/internal/worker/jobs/{id}/result"), Some("secret"), json!({ "name": "w1", "result": result })).await.0, StatusCode::NO_CONTENT);

    let (_, done) = call(&app, Method::GET, &format!("/api/exercises/run/{id}"), t, None).await;
    assert_eq!(done["state"], "done");
    assert_eq!(done["solved"], true);
    assert_eq!(done["attempt"]["status"], "ok");
    let (_, state) = call(&app, Method::GET, "/api/exercises/13/0/state", t, None).await;
    assert_eq!(state["status"]["intro-variable"], "ok");
    let (_, attempts) = call(&app, Method::GET, "/api/exercises/13/0/intro-variable/attempts", t, None).await;
    assert_eq!(attempts["attempts"].as_array().unwrap().len(), 1);

    // то же решение второй раз — из кэша, без воркера
    let (st, cached) = call(&app, Method::POST, "/api/exercises/run", t, Some(run)).await;
    assert_eq!(st, StatusCode::ACCEPTED);
    assert_eq!(cached["state"], "done");
    assert_eq!(cached["solved"], true);
    let (_, attempts) = call(&app, Method::GET, "/api/exercises/13/0/intro-variable/attempts", t, None).await;
    assert_eq!(attempts["attempts"].as_array().unwrap().len(), 2, "кэш не отменяет записи попытки");

    // черновики; чужие и несуществующие задачи
    assert_eq!(call(&app, Method::PUT, "/api/exercises/13/0/intro-variable/draft", t, Some(json!({ "code": "x = 1" }))).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::GET, "/api/exercises/13/0/state", t, None).await.1["drafts"]["intro-variable"], "x = 1");
    assert_eq!(call(&app, Method::PUT, "/api/exercises/13/0/nope/draft", t, Some(json!({ "code": "x" }))).await.0, StatusCode::NOT_FOUND);
    assert_eq!(call(&app, Method::POST, "/api/exercises/run", t, Some(json!({ "book": 13, "chapter": 0, "task": "intro-variable", "code": "  " }))).await.0, StatusCode::UNPROCESSABLE_ENTITY);

    // лабораторное упражнение засчитывается без песочницы, но только если решение проходит проверку движком лаборатории
    let lab = call(&app, Method::GET, "/api/exercises/14/6", None, None).await.1["tasks"][0]["id"].as_str().unwrap().to_string();
    let solved_uri = format!("/api/exercises/14/6/{lab}/solved");
    assert_eq!(call(&app, Method::PUT, &solved_uri, t, Some(json!({ "solution": "{}" }))).await.0, StatusCode::UNPROCESSABLE_ENTITY, "пустое решение не засчитывается");
    let file: Value = serde_json::from_slice(&std::fs::read("../backend/app/data/labs/arch/14-06.json").unwrap()).unwrap();
    let reference = file["tasks"][0]["spec"]["solution"].to_string();
    assert_eq!(call(&app, Method::PUT, &solved_uri, t, Some(json!({ "solution": reference }))).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::GET, "/api/exercises/14/6/state", t, None).await.1["status"][&lab], "ok");
    assert_eq!(call(&app, Method::PUT, "/api/exercises/13/0/intro-variable/solved", t, Some(json!({ "solution": "x" }))).await.0, StatusCode::NOT_FOUND);
}

#[tokio::test]
async fn worker_api_is_closed_without_a_token() {
    let app = app("").await;
    assert_eq!(call(&app, Method::POST, "/internal/worker/ping", None, Some(json!({ "name": "w", "lanes": [] }))).await.0, StatusCode::NOT_FOUND);
}
