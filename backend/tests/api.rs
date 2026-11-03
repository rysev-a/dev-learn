//! End-to-end API checks on in-memory SurrealDB: seed from the real course sources, sign-in, progress, quizzes,
//! answers, the check queue and the internal worker API.

use axum::{
    body::Body,
    http::{header, Method, Request, StatusCode},
    Router,
};
use http_body_util::BodyExt;
use cs_core_backend::{build, config::Config, db};
use serde_json::{json, Value};
use tower::ServiceExt;

async fn app(worker_token: &str) -> Router {
    let cfg = Config {
        bind: "127.0.0.1:0".into(),
        surreal_url: "memory".into(),
        data_dir: std::path::PathBuf::from("data"),
        audio_dir: std::env::temp_dir().join("cs-core-rs-test-audio"),
        records_dir: std::env::temp_dir().join("cs-core-rs-test-records"),
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
    let (st, _) = call(app, Method::POST, "/api/auth/signup", None, Some(json!({ "email": email, "password": "correct-horse-1", "name": "Test" }))).await;
    assert_eq!(st, StatusCode::CREATED);
    let (st, body) = call(app, Method::POST, "/api/auth/login", None, Some(json!({ "email": email, "password": "correct-horse-1" }))).await;
    assert_eq!(st, StatusCode::OK);
    body["token"].as_str().unwrap().to_string()
}

#[tokio::test]
async fn course_content_is_seeded() {
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
    // SQL tasks come with the description of the practice databases
    let (_, sql) = call(&app, Method::GET, "/api/exercises/9/2", None, None).await;
    let first = &sql["tasks"][0];
    assert_eq!(first["mode"], "sql");
    let key = first["dataset"].as_str().unwrap();
    assert!(!sql["datasets"][key]["tables"].as_array().unwrap().is_empty());
    assert_eq!(call(&app, Method::GET, "/api/exercises/9/99", None, None).await.0, StatusCode::NOT_FOUND);
    // chapters 17+ have practice databases with foreign keys filled in arbitrary order: the schema is still built
    for chapter in 1..=32 {
        let (st, _) = call(&app, Method::GET, &format!("/api/exercises/9/{chapter}"), None, None).await;
        assert_eq!(st, StatusCode::OK, "chapter {chapter} of book 9");
    }
    assert_eq!(call(&app, Method::GET, "/api/nope", None, None).await.0, StatusCode::NOT_FOUND);

    // protected routes without a session
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
    let files = std::fs::read_dir("data/slides").unwrap().count();
    assert_eq!(list.len(), files, "every chapter file made it into the database");
    assert!(list.iter().any(|c| c["book"] == 13 && c["chapter"] == 0));

    // system design diagram: a scene made of frames arrives as data
    let (st, ch) = call(&app, Method::GET, "/api/slides/18/24", None, None).await;
    assert_eq!(st, StatusCode::OK);
    let slides = ch["slides"].as_array().unwrap();
    assert_eq!(slides.len(), 13);
    assert!(ch["rubric"].as_str().unwrap().contains("ГЛАВА 24"));
    let scene = slides[0]["body"].as_array().unwrap().iter().find(|b| b["t"] == "scene").expect("the slide has a scene");
    assert!(!scene["frames"].as_array().unwrap().is_empty());
    assert_eq!(scene["labels"].as_array().unwrap().len(), scene["frames"].as_array().unwrap().len());

    // old format: blocks instead of a scene
    let (_, py) = call(&app, Method::GET, "/api/slides/13/5", None, None).await;
    let kinds: Vec<&str> = py["slides"][1]["body"].as_array().unwrap().iter().map(|b| b["t"].as_str().unwrap()).collect();
    assert_eq!(kinds, ["code", "label", "cmd", "note"]);

    // Discrete math: diagrams are written by Rust generators and stored in the data like the rest
    let (st, dm) = call(&app, Method::GET, "/api/slides/12/1", None, None).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(dm["slides"].as_array().unwrap().len(), 13);
    assert_eq!(call(&app, Method::GET, "/api/slides/99/1", None, None).await.0, StatusCode::NOT_FOUND);
}

#[tokio::test]
async fn lab_solutions_are_checked_by_the_server_engine() {
    let app = app("").await;
    let token = sign_in(&app, "student@mail.com").await;
    // the scenario arrives without the reference solution
    let (st, lab) = call(&app, Method::GET, "/api/labs/18/2", None, None).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(lab["lab"], "sd");
    let first = &lab["tasks"][0];
    assert!(first["spec"].get("solution").is_none(), "the reference is not sent to the client");
    assert!(first["spec"]["goals"].as_array().is_some_and(|g| !g.is_empty()));
    assert_eq!(call(&app, Method::GET, "/api/labs/18/99", None, None).await.0, StatusCode::NOT_FOUND);

    // the reference and the starting diagram from the data file
    let file: Value = serde_json::from_slice(&std::fs::read("data/labs/sd/18-02.json").unwrap()).unwrap();
    let task = &file["tasks"][0];
    let id = task["id"].as_str().unwrap();
    let uri = format!("/api/exercises/18/2/{id}/solved");
    let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": task["spec"]["start"].to_string() }))).await;
    assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "the starting diagram does not solve the exercise: {body}");
    let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": task["spec"]["solution"].to_string() }))).await;
    assert_eq!(st, StatusCode::NO_CONTENT, "{body}");
}

#[tokio::test]
async fn ovirt_simulators_are_verified_by_the_server() {
    use virtlab::ovirt_dc::{Action as A, Net};

    let app = app("").await;
    let token = sign_in(&app, "ovirt@mail.com").await;
    let put = |chapter: u32, task: &str, solution: Value| {
        let (app, token) = (app.clone(), token.clone());
        let uri = format!("/api/exercises/17/{chapter}/{task}/solved");
        async move { call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": solution.to_string() }))).await }
    };
    for (chapter, task) in [(17, "virt-sim-ovirt-dc"), (19, "virt-sim-ovirt-fence"), (22, "virt-sim-ovirt-sched")] {
        let (st, lab) = call(&app, Method::GET, &format!("/api/labs/17/{chapter}"), None, None).await;
        assert_eq!(st, StatusCode::OK);
        assert_eq!(lab["tasks"][0]["id"], task);
        // nothing is submitted: the exercise is not solved
        assert_eq!(put(chapter, task, json!({})).await.0, StatusCode::UNPROCESSABLE_ENTITY, "{task}: empty solution");
    }

    // chapter 17: a session of actions replayed by the server
    let mut trace = vec![
        A::AddCluster,
        A::AddHost { host: 1 },
        A::AddHost { host: 2 },
        A::CreateNetwork,
        A::AssignNetwork { host: 1 },
        A::AssignNetwork { host: 2 },
        A::CreateDomain,
        A::AttachDomain,
        A::ActivateDomain,
        A::CreateVm { net: Net::VmNet },
        A::RunVm,
    ];
    let all = |trace: &[A]| json!({ "dc_up": { "trace": trace }, "vm_net": { "trace": trace }, "migrate": { "trace": trace } });
    let (st, _) = put(17, "virt-sim-ovirt-dc", all(&trace)).await;
    assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "no maintenance, no migration");
    trace.push(A::Maintenance { host: 1 });
    let (st, body) = put(17, "virt-sim-ovirt-dc", all(&trace)).await;
    assert_eq!(st, StatusCode::NO_CONTENT, "{body}");

    // the boards (chapters 17, 20, 21): the reference boards are accepted, the starting ones and boards that break a rule are not
    let mut boards: Vec<(u32, String)> = vec![];
    for entry in std::fs::read_dir("data/labs/virt").unwrap() {
        let path = entry.unwrap().path();
        let chapter: u32 = path.file_stem().unwrap().to_str().unwrap().trim_start_matches("17-").parse().unwrap();
        let file: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        for t in file["tasks"].as_array().unwrap() {
            if t["spec"]["sim"] == "ovirt_topo" {
                boards.push((chapter, t["id"].as_str().unwrap().to_string()));
            }
        }
    }
    boards.sort();
    assert!(boards.len() >= 11, "every board exercise is found: {boards:?}");
    for (chapter, task) in boards.iter().map(|(c, t)| (*c, t.as_str())) {
        let (_, lab) = call(&app, Method::GET, &format!("/api/labs/17/{chapter}"), None, None).await;
        let public = lab["tasks"].as_array().unwrap().iter().find(|t| t["id"] == task).expect("the board exercise");
        assert!(public["spec"].get("solution").is_none(), "{task}: the reference boards are not sent to the client");
        let file: Value = serde_json::from_slice(&std::fs::read(format!("data/labs/virt/17-{chapter}.json")).unwrap()).unwrap();
        let spec = &file["tasks"].as_array().unwrap().iter().find(|t| t["id"] == task).unwrap()["spec"];
        let reference = spec["solution"].clone();
        let scenarios = spec["scenarios"].as_array().unwrap();
        assert_eq!(reference.as_object().map(|m| m.len()), Some(scenarios.len()));
        let starts: serde_json::Map<String, Value> = scenarios.iter().map(|s| (s["id"].as_str().unwrap().to_string(), s["start"].clone())).collect();
        let (st, _) = put(chapter, task, Value::Object(starts)).await;
        assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "{task}: the starting boards do not solve the exercise");
        let first = scenarios[0]["id"].as_str().unwrap();
        let mut broken = reference.clone();
        let link = broken[first]["edges"][0].clone();
        broken[first]["edges"].as_array_mut().unwrap().push(link);
        let (st, _) = put(chapter, task, broken).await;
        assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "{task}: a duplicate link breaks a rule of the board");
        let mut missing = reference.clone();
        missing.as_object_mut().unwrap().remove(first);
        assert_eq!(put(chapter, task, missing).await.0, StatusCode::UNPROCESSABLE_ENTITY, "{task}: every scenario has to be solved");
        let (st, body) = put(chapter, task, reference).await;
        assert_eq!(st, StatusCode::NO_CONTENT, "{task}: {body}");
    }

    // chapter 19: the settings are simulated again on every situation
    let fence = json!({ "soft": true, "power": true, "skip_lease": true, "skip_connectivity": true, "threshold": 50, "vm_leases": true });
    let solution: serde_json::Map<String, Value> = ["hung", "dead", "mgmt", "switch", "bmc"].iter().map(|id| ((*id).to_string(), fence.clone())).collect();
    let (st, body) = put(19, "virt-sim-ovirt-fence", Value::Object(solution.clone())).await;
    assert_eq!(st, StatusCode::NO_CONTENT, "{body}");
    let mut weak = solution;
    weak.insert("switch".into(), json!({ "soft": true, "power": true, "skip_lease": true, "skip_connectivity": false, "threshold": 50, "vm_leases": true }));
    assert_eq!(put(19, "virt-sim-ovirt-fence", Value::Object(weak)).await.0, StatusCode::UNPROCESSABLE_ENTITY, "the share of unreachable hosts is ignored");

    // chapter 22: the policy is used for placing the VMs again
    let policy = |memory, network, affinity, even, pack| json!({ "memory": memory, "network": network, "affinity": affinity, "even": even, "free_mem": 0, "pack": pack });
    let good = json!({ "even": policy(false, false, false, 1, 0), "nets": policy(false, true, false, 1, 0), "anti": policy(false, false, true, 1, 0), "pack": policy(true, false, false, 0, 0) });
    let (st, body) = put(22, "virt-sim-ovirt-sched", good.clone()).await;
    assert_eq!(st, StatusCode::NO_CONTENT, "{body}");
    let mut bad = good;
    bad["anti"] = policy(false, false, false, 1, 0);
    assert_eq!(put(22, "virt-sim-ovirt-sched", bad).await.0, StatusCode::UNPROCESSABLE_ENTITY, "anti-affinity filter is off");
}

#[tokio::test]
async fn riscv_programs_are_checked_by_running_them() {
    let app = app("").await;
    let token = sign_in(&app, "riscv@mail.com").await;
    let (st, lab) = call(&app, Method::GET, "/api/labs/14/16", None, None).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(lab["lab"], "riscv");
    assert!(lab["tasks"][0]["spec"].get("reference").is_none(), "the reference program is not sent to the client");
    let file: Value = serde_json::from_slice(&std::fs::read("data/labs/arch/14-16.json").unwrap()).unwrap();
    let task = &file["tasks"][0];
    let uri = format!("/api/exercises/14/16/{}/solved", task["id"].as_str().unwrap());
    let (st, _) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": "" }))).await;
    assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "an empty program does not solve it");
    let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": task["spec"]["reference"] }))).await;
    assert_eq!(st, StatusCode::NO_CONTENT, "{body}");
}

#[tokio::test]
async fn architecture_lab_accepts_every_reference_solution_in_course_order() {
    let app = app("").await;
    let token = sign_in(&app, "arch@mail.com").await;
    let (mut solved, mut empty_rejected) = (0, 0);
    for chapter in 6..=15 {
        let path = format!("data/labs/arch/14-{chapter:02}.json");
        let file: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        for task in file["tasks"].as_array().unwrap() {
            let uri = format!("/api/exercises/14/{chapter}/{}/solved", task["id"].as_str().unwrap());
            let reference = match &task["spec"]["solution"] {
                Value::String(text) => text.clone(),
                other => other.to_string(),
            };
            // composite blocks are unlocked by the student's own solutions: course order matters
            let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": reference }))).await;
            assert_eq!(st, StatusCode::NO_CONTENT, "{chapter}/{}: {body}", task["id"]);
            solved += 1;
            let (st, _) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": "{\"gates\":[],\"wires\":[]}" }))).await;
            empty_rejected += usize::from(st == StatusCode::UNPROCESSABLE_ENTITY);
        }
    }
    assert_eq!(solved, 103);
    assert!(empty_rejected > 90, "an empty diagram does not solve the exercise (rejected {empty_rejected})");
}

#[tokio::test]
async fn network_lab_accepts_solved_networks_and_rejects_the_starting_ones() {
    let app = app("").await;
    let token = sign_in(&app, "net@mail.com").await;
    let mut dir: Vec<_> = std::fs::read_dir("data/labs/net").unwrap().map(|e| e.unwrap().path()).collect();
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
    assert_eq!(rejected, 79, "the starting network solves no exercise");
}

#[tokio::test]
async fn composite_gates_stay_locked_until_the_student_builds_them() {
    let app = app("").await;
    let token = sign_in(&app, "locks@mail.com").await;
    // the "half adder" uses XOR, which is unlocked by building "xor" by hand
    let file: Value = serde_json::from_slice(&std::fs::read("data/labs/arch/14-09.json").unwrap()).unwrap();
    let task = file["tasks"].as_array().unwrap().iter().find(|t| t["id"] == "half-adder").unwrap();
    let uri = "/api/exercises/14/9/half-adder/solved";
    let (st, body) = call(&app, Method::PUT, uri, Some(&token), Some(json!({ "solution": task["spec"]["solution"].to_string() }))).await;
    assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "XOR is locked: {body}");
    assert!(body["detail"].as_str().unwrap().contains("XOR"), "{body}");
    // an unsolved draft must not unlock the element
    let (st, _) = call(&app, Method::PUT, "/api/exercises/14/6/xor-gate/draft", Some(&token), Some(json!({ "code": "{}" }))).await;
    assert!(st == StatusCode::NO_CONTENT || st == StatusCode::NOT_FOUND);
    let (st, _) = call(&app, Method::PUT, uri, Some(&token), Some(json!({ "solution": task["spec"]["solution"].to_string() }))).await;
    assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY);
}

#[tokio::test]
async fn progress_quiz_and_answers() {
    let app = app("").await;
    let token = sign_in(&app, "student@example.com").await;
    let t = Some(token.as_str());

    assert_eq!(call(&app, Method::POST, "/api/progress/slides", t, Some(json!({ "book": 18, "chapter": 24, "slide": 2 }))).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::POST, "/api/progress/slides", t, Some(json!({ "book": 18, "chapter": 24, "slide": 2 }))).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::POST, "/api/progress/slides", t, Some(json!({ "book": 0, "chapter": 24, "slide": 2 }))).await.0, StatusCode::UNPROCESSABLE_ENTITY);
    // "Python" and "Unix" have a chapter zero (introduction): its slides are saved too
    assert_eq!(call(&app, Method::POST, "/api/progress/slides", t, Some(json!({ "book": 13, "chapter": 0, "slide": 1 }))).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::GET, "/api/progress", t, None).await.1["slides"]["13:0"], json!([1]));

    // quiz: questions without answers, each question is answered once
    let (_, quiz) = call(&app, Method::GET, "/api/quizzes/18/24", t, None).await;
    assert_eq!(quiz["questions"].as_array().unwrap().len(), 5);
    assert!(quiz["questions"][0].get("answer").is_none());
    assert!(quiz["reveal"][0].is_null());
    let (st, first) = call(&app, Method::POST, "/api/quizzes/18/24/answer", t, Some(json!({ "question": 0, "pick": 0 }))).await;
    assert_eq!(st, StatusCode::OK);
    let (_, again) = call(&app, Method::POST, "/api/quizzes/18/24/answer", t, Some(json!({ "question": 0, "pick": 3 }))).await;
    assert_eq!(again["pick"], first["pick"], "a repeated answer changes nothing");
    assert_eq!(call(&app, Method::POST, "/api/quizzes/18/24/answer", t, Some(json!({ "question": 0, "pick": 40 }))).await.0, StatusCode::UNPROCESSABLE_ENTITY);
    let (_, quiz) = call(&app, Method::GET, "/api/quizzes/18/24", t, None).await;
    assert!(quiz["reveal"][0]["expl"].as_str().is_some());

    // typed answers: a correct one is remembered, a wrong one reveals nothing
    let (_, bad) = call(&app, Method::POST, "/api/answers/12/1/check", t, Some(json!({ "task": 0, "value": "999" }))).await;
    assert_eq!(bad, json!({ "ok": false }));
    let (_, good) = call(&app, Method::POST, "/api/answers/12/1/check", t, Some(json!({ "task": 0, "value": " 1 " }))).await;
    assert_eq!(good, json!({ "ok": true }));

    let (_, progress) = call(&app, Method::GET, "/api/progress", t, None).await;
    assert_eq!(progress["slides"]["18:24"], json!([2]));
    assert_eq!(progress["quiz"]["18:24"][0], first["pick"]);
    assert_eq!(progress["quizRight"]["18:24"], first["right"]);
    assert_eq!(progress["answers"]["12:1"]["0"], "1");

    // resets
    assert_eq!(call(&app, Method::DELETE, "/api/progress/quiz?book=18&chapter=24", t, None).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::DELETE, "/api/progress?scope=practice", t, None).await.0, StatusCode::NO_CONTENT);
    let (_, progress) = call(&app, Method::GET, "/api/progress", t, None).await;
    assert_eq!(progress["quiz"], json!({}));
    assert_eq!(progress["answers"], json!({}));
    assert_eq!(progress["slides"]["18:24"], json!([2]), "scope=practice does not touch slides");
    assert_eq!(call(&app, Method::DELETE, "/api/progress?scope=zzz", t, None).await.0, StatusCode::UNPROCESSABLE_ENTITY);
}

#[tokio::test]
async fn code_jobs_go_through_the_worker_api() {
    let app = app("secret").await;
    let token = sign_in(&app, "coder@example.com").await;
    let t = Some(token.as_str());
    let run = json!({ "book": 13, "chapter": 0, "task": "intro-variable", "code": "year = 1991\nprint(year)" });

    // no workers: checking is unavailable
    assert_eq!(call(&app, Method::POST, "/api/exercises/run", t, Some(run.clone())).await.0, StatusCode::SERVICE_UNAVAILABLE);
    // worker token
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

    // enqueue -> queue -> worker picks up -> result -> attempt and status recorded
    let (st, queued) = call(&app, Method::POST, "/api/exercises/run", t, Some(run.clone())).await;
    assert_eq!(st, StatusCode::ACCEPTED);
    assert_eq!(queued["state"], "queued");
    let id = queued["id"].as_str().unwrap().to_string();
    assert_eq!(call(&app, Method::POST, "/api/exercises/run", t, Some(run.clone())).await.0, StatusCode::TOO_MANY_REQUESTS, "one check per user");

    let (st, job) = w(Method::POST, "/internal/worker/claim", Some("secret"), json!({ "name": "w1", "lanes": ["light"], "wait": 0 })).await;
    assert_eq!(st, StatusCode::OK);
    assert_eq!(job["id"], id);
    assert_eq!(job["task"]["id"], "intro-variable");
    assert!(job["task"]["expected"].is_array(), "the worker job includes the spec: {job}");
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

    // the same solution a second time comes from the cache, without a worker
    let (st, cached) = call(&app, Method::POST, "/api/exercises/run", t, Some(run)).await;
    assert_eq!(st, StatusCode::ACCEPTED);
    assert_eq!(cached["state"], "done");
    assert_eq!(cached["solved"], true);
    let (_, attempts) = call(&app, Method::GET, "/api/exercises/13/0/intro-variable/attempts", t, None).await;
    assert_eq!(attempts["attempts"].as_array().unwrap().len(), 2, "the cache does not skip recording the attempt");

    // drafts; other people's and nonexistent tasks
    assert_eq!(call(&app, Method::PUT, "/api/exercises/13/0/intro-variable/draft", t, Some(json!({ "code": "x = 1" }))).await.0, StatusCode::NO_CONTENT);
    assert_eq!(call(&app, Method::GET, "/api/exercises/13/0/state", t, None).await.1["drafts"]["intro-variable"], "x = 1");
    assert_eq!(call(&app, Method::PUT, "/api/exercises/13/0/nope/draft", t, Some(json!({ "code": "x" }))).await.0, StatusCode::NOT_FOUND);
    assert_eq!(call(&app, Method::POST, "/api/exercises/run", t, Some(json!({ "book": 13, "chapter": 0, "task": "intro-variable", "code": "  " }))).await.0, StatusCode::UNPROCESSABLE_ENTITY);

    // a lab exercise is accepted without a sandbox, but only if the lab engine accepts the solution
    let lab = call(&app, Method::GET, "/api/exercises/14/6", None, None).await.1["tasks"][0]["id"].as_str().unwrap().to_string();
    let solved_uri = format!("/api/exercises/14/6/{lab}/solved");
    assert_eq!(call(&app, Method::PUT, &solved_uri, t, Some(json!({ "solution": "{}" }))).await.0, StatusCode::UNPROCESSABLE_ENTITY, "an empty solution is not accepted");
    let file: Value = serde_json::from_slice(&std::fs::read("data/labs/arch/14-06.json").unwrap()).unwrap();
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

#[tokio::test]
async fn web_lab_accepts_references_and_rejects_starters() {
    let app = app("").await;
    let token = sign_in(&app, "web@mail.com").await;
    let mut checked = 0;
    for entry in std::fs::read_dir("data/labs/web").unwrap() {
        let path = entry.unwrap().path();
        let file: Value = serde_json::from_slice(&std::fs::read(&path).unwrap()).unwrap();
        let (book, chapter) = (file["book"].as_i64().unwrap(), file["chapter"].as_i64().unwrap());
        // the task arrives without the reference
        let (st, lab) = call(&app, Method::GET, &format!("/api/labs/{book}/{chapter}"), None, None).await;
        assert_eq!(st, StatusCode::OK, "GET /api/labs/{book}/{chapter}");
        assert_eq!(lab["lab"], "web");
        assert!(lab["tasks"].as_array().unwrap().iter().all(|t| t["spec"].get("reference").is_none()), "the reference is not sent to the client");
        for task in file["tasks"].as_array().unwrap() {
            let spec = &task["spec"];
            let uri = format!("/api/exercises/{book}/{chapter}/{}/solved", task["id"].as_str().unwrap());
            let start = json!({ "html": spec["starter_html"], "css": spec["starter_css"] });
            let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": start.to_string() }))).await;
            assert_eq!(st, StatusCode::UNPROCESSABLE_ENTITY, "{}: the starter must not solve it: {body}", task["id"]);
            let r = &spec["reference"];
            let good = match spec["kind"].as_str().unwrap() {
                "html" => json!({ "html": r["html"], "css": "" }),
                "css" => json!({ "html": "", "css": r["css"] }),
                _ => json!({ "html": "", "css": r["selector"] }),
            };
            let (st, body) = call(&app, Method::PUT, &uri, Some(&token), Some(json!({ "solution": good.to_string() }))).await;
            assert_eq!(st, StatusCode::NO_CONTENT, "{}: the reference must be accepted: {body}", task["id"]);
            checked += 1;
        }
    }
    assert!(checked >= 21, "exercises checked: {checked}");
}

async fn call_lang(app: &Router, lang: &str, method: Method, uri: &str, token: Option<&str>, body: Option<Value>) -> (StatusCode, Value) {
    let mut req = Request::builder().method(method).uri(uri).header(header::ACCEPT_LANGUAGE, lang);
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

#[tokio::test]
async fn translated_books_are_served_in_english_and_the_rest_in_russian() {
    let app = app("").await;

    // book list: a translated book has the English title and both languages, the others have the Russian title and Russian only
    let (_, books) = call_lang(&app, "en-US,en;q=0.9", Method::GET, "/api/books", None, None).await;
    let books = books.as_array().unwrap();
    let dm = books.iter().find(|b| b["id"] == 12).unwrap();
    assert_eq!(dm["title"], "Discrete Mathematics");
    assert_eq!(dm["langs"], json!(["ru", "en"]));
    let py = books.iter().find(|b| b["id"] == 13).unwrap();
    assert_eq!(py["langs"], json!(["ru", "en"]));
    assert_eq!(py["title"], "Python as a First Language");
    for (id, title) in [(14, "Computer Architecture"), (15, "Computer Networks"), (17, "Virtualization"), (11, "Modern Frontend"), (18, "System Design")] {
        let book = books.iter().find(|b| b["id"] == id).unwrap();
        assert_eq!(book["langs"], json!(["ru", "en"]), "book {id}");
        assert_eq!(book["title"], title);
    }
    assert!(books.iter().all(|b| b["langs"] == json!(["ru", "en"])), "all course books are translated");
    let (_, ru_books) = call_lang(&app, "ru", Method::GET, "/api/books", None, None).await;
    assert_eq!(ru_books.as_array().unwrap().iter().find(|b| b["id"] == 12).unwrap()["title"], "Дискретная математика");

    // table of contents and chapter text: same ids, English text, same number of paragraphs
    let (_, ru_course) = call_lang(&app, "ru", Method::GET, "/api/books/12/course", None, None).await;
    let (_, en_course) = call_lang(&app, "en", Method::GET, "/api/books/12/course", None, None).await;
    assert_eq!(en_course[0]["title"], "The language of mathematics");
    assert_eq!(ru_course[0]["id"], en_course[0]["id"]);
    let chapter_id = en_course[0]["chapters"][0]["id"].clone();
    assert_eq!(ru_course[0]["chapters"][0]["id"], chapter_id, "the chapter address does not depend on the language");
    let (_, en_chapter) = call_lang(&app, "en", Method::GET, &format!("/api/chapters/{chapter_id}"), None, None).await;
    let (_, ru_chapter) = call_lang(&app, "ru", Method::GET, &format!("/api/chapters/{chapter_id}"), None, None).await;
    assert!(en_chapter["lessons"][0]["text"].as_str().unwrap().starts_with("Discrete mathematics. Chapter 1."));
    assert!(ru_chapter["lessons"][0]["text"].as_str().unwrap().starts_with("Дискретная математика. Глава 1."));
    assert_eq!(en_chapter["lessons"].as_array().unwrap().len(), ru_chapter["lessons"].as_array().unwrap().len());
    assert_ne!(en_chapter["lessons"][0]["id"], ru_chapter["lessons"][0]["id"], "each language has its own lesson parts (and its own audio)");

    // slides: English for a translated book, Russian for the others
    let (_, en_slides) = call_lang(&app, "en", Method::GET, "/api/slides/12/1", None, None).await;
    assert!(en_slides["rubric"].as_str().unwrap().starts_with("DISCRETE MATHEMATICS"));
    assert_eq!(en_slides["slides"].as_array().unwrap().len(), 13);
    let (_, py_slides) = call_lang(&app, "en", Method::GET, "/api/slides/13/5", None, None).await;
    assert_eq!(py_slides["rubric"], "PYTHON AS A FIRST LANGUAGE / DATA AND LOOPS / CHAPTER 5");
    let (_, arch_slides) = call_lang(&app, "en", Method::GET, "/api/slides/14/1", None, None).await;
    assert!(arch_slides["rubric"].as_str().unwrap().starts_with("THE COMPUTER AND THE TRANSISTOR"));

    // quiz: same answer and number of options, text in the request language
    let token = sign_in(&app, "lang@example.com").await;
    let (_, en_quiz) = call_lang(&app, "en", Method::GET, "/api/quizzes/12/1", Some(&token), None).await;
    let (_, ru_quiz) = call_lang(&app, "ru", Method::GET, "/api/quizzes/12/1", Some(&token), None).await;
    assert_eq!(en_quiz["title"], "Quiz: sets");
    assert_eq!(en_quiz["questions"][0]["q"], "How does a set differ from a list?");
    assert_eq!(en_quiz["questions"][0]["options"].as_array().unwrap().len(), ru_quiz["questions"][0]["options"].as_array().unwrap().len());
    let (_, en_answer) = call_lang(&app, "en", Method::POST, "/api/quizzes/12/1/answer", Some(&token), Some(json!({ "question": 0, "pick": 1 }))).await;
    assert_eq!(en_answer["answer"], 1);
    assert!(en_answer["expl"].as_str().unwrap().starts_with("A list is a contract"));

    // typed answers: "да" means yes/true, and vice versa
    let (_, en_set) = call_lang(&app, "en", Method::GET, "/api/answers/12/1", Some(&token), None).await;
    assert_eq!(en_set["tasks"][0]["q"], "How many subsets does the empty set have?");
    let check = |lang: &'static str, value: &'static str| {
        let app = app.clone();
        let token = token.clone();
        async move { call_lang(&app, lang, Method::POST, "/api/answers/12/1/check", Some(&token), Some(json!({ "task": 4, "value": value }))).await.1["ok"].clone() }
    };
    assert_eq!(check("en", "Yes").await, json!(true));
    assert_eq!(check("en", "да").await, json!(false));
    assert_eq!(check("ru", "да").await, json!(true));
    assert_eq!(check("ru", "yes").await, json!(false));

    // code tasks: statements in the request language, tests and driver shared
    let (_, en_tasks) = call_lang(&app, "en", Method::GET, "/api/exercises/13/5", Some(&token), None).await;
    let (_, ru_tasks) = call_lang(&app, "ru", Method::GET, "/api/exercises/13/5", Some(&token), None).await;
    let (en_list, ru_list) = (en_tasks["tasks"].as_array().unwrap(), ru_tasks["tasks"].as_array().unwrap());
    assert_eq!(en_list.len(), ru_list.len());
    assert_eq!(en_list[0]["id"], ru_list[0]["id"]);
    assert_ne!(en_list[0]["statement"], ru_list[0]["statement"]);
    assert!(!en_list[0]["statement"].as_str().unwrap().is_empty());
}

/// Recording for a slide: the whole request body, the type in `Content-Type`.
async fn upload(app: &Router, token: &str, uri: &str, content_type: &str, bytes: &[u8]) -> (StatusCode, Value) {
    let req = Request::builder().method(Method::POST).uri(uri).header(header::AUTHORIZATION, format!("Bearer {token}")).header(header::CONTENT_TYPE, content_type).body(Body::from(bytes.to_vec())).unwrap();
    let res = app.clone().oneshot(req).await.unwrap();
    let status = res.status();
    let bytes = res.into_body().collect().await.unwrap().to_bytes();
    (status, serde_json::from_slice(&bytes).unwrap_or(Value::Null))
}

#[tokio::test]
async fn slide_recordings_are_saved_by_administrators_only() {
    let dir = std::env::temp_dir().join(format!("cs-core-records-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&dir);
    let cfg = Config {
        bind: "127.0.0.1:0".into(),
        surreal_url: "memory".into(),
        data_dir: std::path::PathBuf::from("data"),
        audio_dir: std::env::temp_dir().join("cs-core-rs-test-audio"),
        records_dir: dir.clone(),
        static_dir: None,
        worker_token: "".into(),
        seed: "auto".into(),
    };
    let database = db::memory().await.unwrap();
    let app = build(database.clone(), cfg).await.unwrap().0;
    auth::Auth::new(database).ensure_admin("author@mail.com", "correct-horse-1").await.unwrap();
    let (st, body) = call(&app, Method::POST, "/api/auth/login", None, Some(json!({ "email": "author@mail.com", "password": "correct-horse-1" }))).await;
    assert_eq!(st, StatusCode::OK);
    let admin = body["token"].as_str().unwrap().to_string();
    let student = sign_in(&app, "student@mail.com").await;

    // students and guests cannot write to disk
    assert_eq!(upload(&app, &student, "/api/records/13/1/2", "audio/webm;codecs=opus", b"webm").await.0, StatusCode::FORBIDDEN);
    assert_eq!(call(&app, Method::POST, "/api/records/13/1/2", None, None).await.0, StatusCode::UNAUTHORIZED);

    // admin: the file goes to <book>/<chapter>/<slide>.<extension by type>
    let (st, saved) = upload(&app, &admin, "/api/records/13/1/2", "audio/webm;codecs=opus", b"webm-bytes").await;
    assert_eq!(st, StatusCode::OK, "{saved}");
    let path = dir.join("13").join("1").join("2.webm");
    assert_eq!(saved["path"].as_str().unwrap(), path.to_string_lossy());
    assert_eq!(saved["bytes"], 10);
    assert_eq!(std::fs::read(&path).unwrap(), b"webm-bytes");

    // a slide has one file: a new recording in another container replaces the old one
    assert_eq!(upload(&app, &admin, "/api/records/13/1/2", "audio/mp4", b"m4a").await.0, StatusCode::OK);
    assert!(!path.exists(), "the old webm is removed");
    assert_eq!(std::fs::read(dir.join("13").join("1").join("2.m4a")).unwrap(), b"m4a");

    // an unknown type and an empty body are rejected
    assert_eq!(upload(&app, &admin, "/api/records/13/1/3", "text/plain", b"x").await.0, StatusCode::UNPROCESSABLE_ENTITY);
    assert_eq!(upload(&app, &admin, "/api/records/13/1/3", "audio/webm", b"").await.0, StatusCode::UNPROCESSABLE_ENTITY);
    assert_eq!(upload(&app, &admin, "/api/records/0/1/3", "audio/webm", b"x").await.0, StatusCode::UNPROCESSABLE_ENTITY);
    let _ = std::fs::remove_dir_all(&dir);
}
