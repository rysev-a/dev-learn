//! Отладка расхождений с TypeScript: печатает вывод «краевых» команд для упражнения в том же виде, что
//! `node scripts/net-export.mjs --edge <id>`. Запуск: `cargo run --example edge -- <id>`; затем `diff` двух выводов.

use netlab::lab::load_dir;
use netlab::term::exec;
use std::path::PathBuf;

fn main() {
    let id = std::env::args().nth(1).expect("id упражнения");
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let gold: serde_json::Value =
        serde_json::from_str(&std::fs::read_to_string(root.join("tests/golden.json")).expect("golden")).expect("json");
    let template: Vec<String> =
        gold["edge_template"].as_array().expect("шаблон").iter().map(|v| v.as_str().unwrap_or("").to_string()).collect();
    let chapters = load_dir(&root.join("../../backend/data/labs/net")).expect("данные");
    let task = chapters.iter().flat_map(|c| c.tasks.iter()).find(|t| t.id == id).expect("нет такого упражнения");
    let mut s = task.spec.start_state();
    for run in gold["scenarios"][&id]["edge"].as_array().expect("edge") {
        let dev = run["dev"].as_str().unwrap_or("");
        let var = |k: &str| run["vars"][k].as_str().unwrap_or("").to_string();
        for t in &template {
            let line = t.replace("{if}", &var("if")).replace("{ip}", &var("ip")).replace("{own}", &var("own")).replace("{gw}", &var("gw"));
            let r = exec(&mut s, dev, &line);
            let tag = match r.changed {
                None => "u",
                Some(true) => "t",
                Some(false) => "f",
            };
            println!("{dev}$ {line}\n[{tag}] {}\n", r.out);
        }
    }
}
