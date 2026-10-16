"""Задачи книги «Изучаем Rust»: глава 22 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {22: [{'id': 'r22-fix-visibility',
       'mode': 'rust',
       'title': 'Исправьте: приватная функция модуля',
       'statement': 'В модуле bank функции new_account и deposit не помечены pub, и код вне модуля не '
                    'собирается (E0603). Откройте наружу ровно то, что нужно драйверу: new_account и '
                    'deposit. Поле balance закрытым оставьте: читать баланс можно только через audit.',
       'starter': 'mod bank {\n'
                  '    pub struct Account {\n'
                  '        balance: i64,\n'
                  '    }\n'
                  '\n'
                  '    fn new_account(initial: i64) -> Account {\n'
                  '        Account { balance: initial }\n'
                  '    }\n'
                  '\n'
                  '    fn deposit(a: &mut Account, n: i64) {\n'
                  '        a.balance += n;\n'
                  '    }\n'
                  '\n'
                  '    pub fn audit(a: &Account) -> String {\n'
                  '        format!("balance={}", a.balance)\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = bank::new_account(10);\n'
                 '    bank::deposit(&mut a, 5);\n'
                 '    println!("{}", bank::audit(&a));\n'
                 '}\n',
       'hint': 'Слово pub перед fn: new_account и deposit станут видимы снаружи модуля.',
       'expected': ['balance=15']},
      {'id': 'r22-fix-field',
       'mode': 'rust',
       'title': 'Закрытые поля: конструктор и геттеры',
       'statement': 'Поля Rect закрыты, поэтому снаружи структуру не собрать и не прочитать. Напишите new(w, '
                    'h) → Result<Rect, String> (стороны должны быть > 0, иначе «сторона должна быть '
                    'положительной»), width(), height(), area() и scale(&self, k: u32) → Rect.',
       'starter': 'mod shapes {\n'
                  '    pub struct Rect {\n'
                  '        w: u32,\n'
                  '        h: u32,\n'
                  '    }\n'
                  '\n'
                  '    impl Rect {\n'
                  '        // new, width, height, area, scale\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let r = shapes::Rect::new(3, 4).unwrap();\n'
                 '    println!("{} {} {}", r.width(), r.height(), r.area());\n'
                 '    let big = r.scale(3);\n'
                 '    println!("{}x{} {}", big.width(), big.height(), big.area());\n'
                 '    println!("{:?}", shapes::Rect::new(0, 5).err());\n'
                 '    println!("{:?}", shapes::Rect::new(2, 0).err());\n'
                 '}\n',
       'hint': 'Конструктор — единственный способ получить Rect снаружи; поэтому внутри него можно '
               'гарантировать w > 0 и h > 0.',
       'expected': ['3 4 12',
                    '9x12 108',
                    'Some("сторона должна быть положительной")',
                    'Some("сторона должна быть положительной")']},
      {'id': 'r22-fix-use-trait',
       'mode': 'rust',
       'title': 'Исправьте: трейт не в области видимости',
       'statement': 'Трейт Shout реализован для str в модуле text, но метод shout() в функции loud вызвать '
                    'нельзя: имя трейта не подключено (E0599). Исправьте одной строкой use.',
       'starter': 'mod text {\n'
                  '    pub trait Shout {\n'
                  '        fn shout(&self) -> String;\n'
                  '    }\n'
                  '\n'
                  '    impl Shout for str {\n'
                  '        fn shout(&self) -> String {\n'
                  '            format!("{}!", self.to_uppercase())\n'
                  '        }\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn loud(s: &str) -> String {\n'
                  '    s.shout()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{}", loud("привет"));\n    println!("{}", loud("rust"));\n}\n',
       'hint': 'Методы трейта доступны, только если сам трейт подключён: use text::Shout;',
       'expected': ['ПРИВЕТ!', 'RUST!']},
      {'id': 'r22-reexport',
       'mode': 'rust',
       'title': 'pub use: плоский публичный интерфейс',
       'statement': 'Типы Circle и Rect лежат глубоко: shapes::circle::Circle и shapes::rect::Rect, а трейт '
                    'Shape — в shapes::Shape. Сделайте так, чтобы из корня крейта были доступны Circle, Rect '
                    'и Shape (pub use), а также модуль prelude с теми же тремя именами.',
       'starter': 'mod shapes {\n'
                  '    pub trait Shape {\n'
                  '        fn area(&self) -> f64;\n'
                  '    }\n'
                  '\n'
                  '    pub mod circle {\n'
                  '        pub struct Circle(pub f64);\n'
                  '        impl super::Shape for Circle {\n'
                  '            fn area(&self) -> f64 {\n'
                  '                3.0 * self.0 * self.0\n'
                  '            }\n'
                  '        }\n'
                  '    }\n'
                  '\n'
                  '    pub mod rect {\n'
                  '        pub struct Rect(pub f64, pub f64);\n'
                  '        impl super::Shape for Rect {\n'
                  '            fn area(&self) -> f64 {\n'
                  '                self.0 * self.1\n'
                  '            }\n'
                  '        }\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  '// pub use и mod prelude\n',
       'driver': 'fn main() {\n'
                 '    let c = Circle(2.0);\n'
                 '    let r = Rect(3.0, 4.0);\n'
                 '    println!("{} {}", c.area(), r.area());\n'
                 '    use prelude::*;\n'
                 '    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Circle(1.0)), Box::new(Rect(1.0, '
                 '2.0))];\n'
                 '    println!("{}", shapes.iter().map(|s| s.area()).sum::<f64>());\n'
                 '}\n',
       'hint': 'В корне: pub use shapes::circle::Circle; и так далее; prelude — модуль с pub use crate::{…}.',
       'expected': ['12 12', '5']},
      {'id': 'r22-paths-super',
       'mode': 'rust',
       'title': 'Пути: crate, self, super',
       'statement': 'Три вложенных модуля. util::double(x) → x * 2. engine::run(x) → util::double(x) + 1 '
                    '(путь от корня). engine::fast::run(x) → engine::run(x) через super, а fast::twice(x) → '
                    'self::step(x) * 2. Реализуйте функции, используя ровно такие пути: crate::, super::, '
                    'self::.',
       'starter': 'mod util {\n'
                  '    pub fn double(x: i32) -> i32 {\n'
                  '        x * 2\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'mod engine {\n'
                  '    pub fn run(x: i32) -> i32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    pub mod fast {\n'
                  '        fn step(x: i32) -> i32 {\n'
                  '            x + 10\n'
                  '        }\n'
                  '\n'
                  '        pub fn run(x: i32) -> i32 {\n'
                  '            todo!()\n'
                  '        }\n'
                  '\n'
                  '        pub fn twice(x: i32) -> i32 {\n'
                  '            todo!()\n'
                  '        }\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!("crate", "::util")).count();\n'
                 '    let bad1 = src.matches(concat!("super", "::run")).count();\n'
                 '    let bad2 = src.matches(concat!("self:", ":step")).count();\n'
                 '    println!("{} {}", engine::run(5), engine::fast::run(5));\n'
                 '    println!("{}", engine::fast::twice(1));\n'
                 '    println!("paths: {} {} {}", bad0, bad1, bad2);\n'
                 '}\n',
       'hint': 'Три разных начала пути: crate::util::double, super::run, self::step — каждое по разу.',
       'expected': ['11 11', '22', 'paths: 1 1 1']},
      {'id': 'r22-fmt-write',
       'mode': 'rust',
       'title': 'use std::fmt::Write для String',
       'statement': 'render_table(rows: &[(&str, i32)]) → String: строки «имя<пробелы до 8>|<число по '
                    'правому краю в 5>» с переводом строки; в конце строка «итого» с суммой. Формируйте '
                    'результат через writeln! прямо в String (для этого нужно подключить трейт '
                    'std::fmt::Write).',
       'starter': 'fn render_table(rows: &[(&str, i32)]) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    print!("{}", render_table(&[("хлеб", 40), ("молоко", 95), ("сыр", 310)]));\n'
                 '    print!("{}", render_table(&[]));\n'
                 '}\n',
       'hint': 'writeln!(out, "...") доступен у String, только если подключён use std::fmt::Write; результат '
               'нужно unwrap() или ?.',
       'expected': ['хлеб    |   40',
                    'молоко  |   95',
                    'сыр     |  310',
                    'итого   |  445',
                    'итого   |    0']},
      {'id': 'r22-invariant-ctor',
       'mode': 'rust',
       'title': 'Инвариант в конструкторе: Kelvin',
       'statement': 'В модуле temp тип Kelvin(f64) с закрытым полем. new(k) → Result<Kelvin, String> («ниже '
                    'абсолютного нуля: K»), from_celsius(c) → Result, kelvin(), celsius(), add(&self, delta: '
                    'f64) → Result<Kelvin, String> (сумма не должна выйти ниже нуля). Снаружи значения ниже '
                    'нуля получить невозможно.',
       'starter': 'mod temp {\n'
                  '    pub struct Kelvin(f64);\n'
                  '\n'
                  '    impl Kelvin {\n'
                  '        // new, from_celsius, kelvin, celsius, add\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let t = temp::Kelvin::from_celsius(25.0).unwrap();\n'
                 '    println!("{:.2} {:.2}", t.kelvin(), t.celsius());\n'
                 '    println!("{:?}", temp::Kelvin::new(-1.0).err());\n'
                 '    println!("{:?}", temp::Kelvin::from_celsius(-300.0).err().map(|e| '
                 'e.starts_with("ниже")));\n'
                 '    println!("{:?}", t.add(-400.0).err());\n'
                 '    println!("{:.1}", t.add(10.0).unwrap().kelvin());\n'
                 '}\n',
       'hint': 'Все пути создания значения проходят через new: там проверка k >= 0.',
       'expected': ['298.15 25.00',
                    'Some("ниже абсолютного нуля: -1")',
                    'Some(true)',
                    'Some("ниже абсолютного нуля: -101.85000000000002")',
                    '308.1']},
      {'id': 'r22-builder',
       'mode': 'rust',
       'title': 'Строитель с проверкой в build()',
       'statement': 'Config { host, port, tls, timeout_ms }. ConfigBuilder::new(host) с умолчаниями (port '
                    '80, tls false, timeout 1000); методы port(self, p), tls(self, on), timeout_ms(self, t) '
                    'возвращают Self; build(self) → Result<Config, String>: «пустой хост», «порт 0», '
                    '«таймаут больше 60000»; при tls = true и порте 80 порт автоматически становится 443.',
       'starter': '#[derive(Debug, PartialEq)]\n'
                  'struct Config {\n'
                  '    host: String,\n'
                  '    port: u16,\n'
                  '    tls: bool,\n'
                  '    timeout_ms: u32,\n'
                  '}\n'
                  '\n'
                  'struct ConfigBuilder {\n'
                  '    host: String,\n'
                  '    port: u16,\n'
                  '    tls: bool,\n'
                  '    timeout_ms: u32,\n'
                  '}\n'
                  '\n'
                  'impl ConfigBuilder {\n'
                  '    fn new(host: &str) -> ConfigBuilder {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn port(mut self, p: u16) -> ConfigBuilder {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn tls(mut self, on: bool) -> ConfigBuilder {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn timeout_ms(mut self, t: u32) -> ConfigBuilder {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn build(self) -> Result<Config, String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", ConfigBuilder::new("example.org").build());\n'
                 '    println!("{:?}", ConfigBuilder::new("a.b").tls(true).build());\n'
                 '    println!("{:?}", '
                 'ConfigBuilder::new("a.b").tls(true).port(8443).timeout_ms(250).build());\n'
                 '    println!("{:?}", ConfigBuilder::new(" ").build());\n'
                 '    println!("{:?}", ConfigBuilder::new("x").port(0).build());\n'
                 '    println!("{:?}", ConfigBuilder::new("x").timeout_ms(70000).build());\n'
                 '}\n',
       'hint': 'Методы-настройки возвращают self, а все проверки собраны в build.',
       'expected': ['Ok(Config { host: "example.org", port: 80, tls: false, timeout_ms: 1000 })',
                    'Ok(Config { host: "a.b", port: 443, tls: true, timeout_ms: 1000 })',
                    'Ok(Config { host: "a.b", port: 8443, tls: true, timeout_ms: 250 })',
                    'Err("пустой хост")',
                    'Err("порт 0")',
                    'Err("таймаут больше 60000")']},
      {'id': 'r22-default-config',
       'mode': 'rust',
       'title': 'Default и обновление структуры',
       'statement': 'Config { name, retries, verbose, ratio, tags }. Реализуйте Default вручную: name «app», '
                    'retries 3, verbose false, ratio 0.5, tags пусто. overridden(base, retries: Option<u32>, '
                    'verbose: Option<bool>) → Config — подставить заданные значения поверх base (None — '
                    'оставить как было).',
       'starter': '#[derive(Debug, Clone, PartialEq)]\n'
                  'struct Config {\n'
                  '    name: String,\n'
                  '    retries: u32,\n'
                  '    verbose: bool,\n'
                  '    ratio: f64,\n'
                  '    tags: Vec<String>,\n'
                  '}\n'
                  '\n'
                  '// impl Default for Config\n'
                  '\n'
                  'fn overridden(base: Config, retries: Option<u32>, verbose: Option<bool>) -> Config {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let d = Config::default();\n'
                 '    println!("{:?}", d);\n'
                 '    println!("{:?}", overridden(d.clone(), Some(10), None));\n'
                 '    println!("{:?}", overridden(d.clone(), None, Some(true)).verbose);\n'
                 '    let custom = Config { name: "svc".into(), tags: vec!["x".into()], ..Default::default() '
                 '};\n'
                 '    println!("{:?}", custom);\n'
                 '    println!("{}", overridden(custom.clone(), None, None) == custom);\n'
                 '}\n',
       'hint': 'Config { retries: …, verbose: …, ..base } — остальные поля берутся из base (в том числе '
               'строка и вектор — они переезжают).',
       'expected': ['Config { name: "app", retries: 3, verbose: false, ratio: 0.5, tags: [] }',
                    'Config { name: "app", retries: 10, verbose: false, ratio: 0.5, tags: [] }',
                    'true',
                    'Config { name: "svc", retries: 3, verbose: false, ratio: 0.5, tags: ["x"] }',
                    'true']},
      {'id': 'r22-fromstr-version',
       'mode': 'rust',
       'title': 'Version: разбор, порядок, вывод',
       'statement': 'Version { major, minor, patch } (u32). Реализуйте FromStr для «1.2.3» (ровно три числа, '
                    'иначе Err со словом «формат»; нечисло → Err «число: <часть>»), Display «1.2.3» и '
                    'порядок (derive Ord по полям major, minor, patch). Тогда sort() и max() работают.',
       'starter': 'use std::fmt;\n'
                  'use std::str::FromStr;\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]\n'
                  'struct Version {\n'
                  '    major: u32,\n'
                  '    minor: u32,\n'
                  '    patch: u32,\n'
                  '}\n'
                  '\n'
                  '// impl FromStr и Display\n',
       'driver': 'fn main() {\n'
                 '    let mut v: Vec<Version> = ["1.10.0", "1.2.9", "0.9.9", "1.2.10"].iter().map(|s| '
                 's.parse().unwrap()).collect();\n'
                 '    v.sort();\n'
                 '    println!("{}", v.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" < "));\n'
                 '    println!("{}", v.iter().max().unwrap());\n'
                 '    println!("{:?}", "1.2".parse::<Version>());\n'
                 '    println!("{:?}", "1.x.3".parse::<Version>());\n'
                 '    println!("{:?}", "1.2.3.4".parse::<Version>().is_err());\n'
                 '}\n',
       'hint': "split('.') и проверка длины; числа разбирайте замыканием с map_err и оператором ?.",
       'expected': ['0.9.9 < 1.2.9 < 1.2.10 < 1.10.0',
                    '1.10.0',
                    'Err("формат: ожидалось X.Y.Z, получено \\"1.2\\"")',
                    'Err("число: x")',
                    'true']},
      {'id': 'r22-semver-req',
       'mode': 'rust',
       'title': 'Требования версий: ^, ~, =, >=',
       'statement': 'Req::parse(s) → Option<Req> и matches(&self, v: &Version) → bool. «^1.2.3»: ≥1.2.3 и '
                    '<2.0.0 (для 0.x: «^0.2.3» — <0.3.0, «^0.0.3» — только 0.0.3); «~1.2.3»: ≥1.2.3 и '
                    '<1.3.0; «=1.2.3» — точно; «>=1.2.3»; «*» — любая. Version и разбор версии уже готовы.',
       'starter': '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]\n'
                  'struct Version {\n'
                  '    major: u32,\n'
                  '    minor: u32,\n'
                  '    patch: u32,\n'
                  '}\n'
                  '\n'
                  'fn v(s: &str) -> Option<Version> {\n'
                  "    let mut it = s.split('.').map(|p| p.parse::<u32>().ok());\n"
                  '    let (a, b, c) = (it.next()??, it.next()??, it.next()??);\n'
                  '    if it.next().is_some() {\n'
                  '        return None;\n'
                  '    }\n'
                  '    Some(Version { major: a, minor: b, patch: c })\n'
                  '}\n'
                  '\n'
                  'enum Req {\n'
                  '    Any,\n'
                  '    Exact(Version),\n'
                  '    AtLeast(Version),\n'
                  '    Caret(Version),\n'
                  '    Tilde(Version),\n'
                  '}\n'
                  '\n'
                  'impl Req {\n'
                  '    fn parse(s: &str) -> Option<Req> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn matches(&self, ver: &Version) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let vers: Vec<Version> = ["0.0.3", "0.2.3", "0.2.9", "0.3.0", "1.2.2", "1.2.3", '
                 '"1.9.0", "2.0.0"].iter().map(|s| v(s).unwrap()).collect();\n'
                 '    for r in ["^1.2.3", "^0.2.3", "^0.0.3", "~1.2.3", "=1.2.3", ">=1.2.3", "*"] {\n'
                 '        let req = Req::parse(r).unwrap();\n'
                 '        let ok: Vec<String> = vers.iter().filter(|x| req.matches(x)).map(|x| '
                 'format!("{}.{}.{}", x.major, x.minor, x.patch)).collect();\n'
                 '        println!("{r}: {}", ok.join(" "));\n'
                 '    }\n'
                 '    println!("{} {}", Req::parse("^x").is_none(), Req::parse("1.2.3").is_none());\n'
                 '}\n',
       'hint': 'Для каретки три случая: major > 0 — совпадает major; иначе minor > 0 — совпадают 0 и minor; '
               'иначе — только точная.',
       'expected': ['^1.2.3: 1.2.3 1.9.0',
                    '^0.2.3: 0.2.3 0.2.9',
                    '^0.0.3: 0.0.3',
                    '~1.2.3: 1.2.3',
                    '=1.2.3: 1.2.3',
                    '>=1.2.3: 1.2.3 1.9.0 2.0.0',
                    '*: 0.0.3 0.2.3 0.2.9 0.3.0 1.2.2 1.2.3 1.9.0 2.0.0',
                    'true true']},
      {'id': 'r22-semver-bump',
       'mode': 'rust',
       'title': 'Повышение версии и совместимость',
       'statement': 'bump(v: Version, kind: &str) → Option<Version>: «major» (minor и patch → 0), «minor» '
                    '(patch → 0), «patch»; другое слово — None. breaking(old, new) → bool: true, если major '
                    'вырос, либо major = 0 и вырос minor. sort_desc(Vec<Version>) → Vec<Version> — от новых '
                    'к старым.',
       'starter': '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]\n'
                  'struct Version {\n'
                  '    major: u32,\n'
                  '    minor: u32,\n'
                  '    patch: u32,\n'
                  '}\n'
                  '\n'
                  'fn bump(v: Version, kind: &str) -> Option<Version> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn breaking(old: Version, new: Version) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn sort_desc(mut v: Vec<Version>) -> Vec<Version> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v = |a, b, c| Version { major: a, minor: b, patch: c };\n'
                 '    println!("{:?}", bump(v(1, 2, 3), "major"));\n'
                 '    println!("{:?}", bump(v(1, 2, 3), "minor"));\n'
                 '    println!("{:?}", bump(v(1, 2, 3), "patch"));\n'
                 '    println!("{:?}", bump(v(1, 2, 3), "huge"));\n'
                 '    println!("{} {} {}", breaking(v(1, 5, 0), v(2, 0, 0)), breaking(v(0, 2, 0), v(0, 3, '
                 '0)), breaking(v(1, 2, 0), v(1, 9, 9)));\n'
                 '    println!("{:?}", sort_desc(vec![v(1, 0, 0), v(0, 9, 9), v(1, 0, 1)]));\n'
                 '}\n',
       'hint': 'Структурное обновление Version { patch: …, ..v } меняет только указанные поля.',
       'expected': ['Some(Version { major: 2, minor: 0, patch: 0 })',
                    'Some(Version { major: 1, minor: 3, patch: 0 })',
                    'Some(Version { major: 1, minor: 2, patch: 4 })',
                    'None',
                    'true true false',
                    '[Version { major: 1, minor: 0, patch: 1 }, Version { major: 1, minor: 0, patch: 0 }, '
                    'Version { major: 0, minor: 9, patch: 9 }]']},
      {'id': 'r22-cargo-toml-parse',
       'mode': 'rust',
       'title': 'Разбор Cargo.toml',
       'statement': 'parse_manifest(text) → Result<Manifest, String>. Manifest { name, version, deps: '
                    'BTreeMap<String, String> }. Секции [package] (name, version — в кавычках) и '
                    '[dependencies] («имя = "версия"» или «имя = { version = "версия", … }»). Комментарии '
                    '«#» и пустые строки пропускать; другие секции игнорировать. Нет name или version → '
                    'Err("нет name") / Err("нет version").',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'struct Manifest {\n'
                  '    name: String,\n'
                  '    version: String,\n'
                  '    deps: BTreeMap<String, String>,\n'
                  '}\n'
                  '\n'
                  'fn parse_manifest(text: &str) -> Result<Manifest, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let t = "# мой проект\\n[package]\\nname = \\"hello\\"\\nversion = '
                 '\\"0.3.1\\"\\nedition = \\"2021\\"\\n\\n[dependencies]\\nserde = \\"1.0\\"\\nrand = { '
                 'version = \\"0.8\\", features = [\\"small_rng\\"] }\\n\\n[dev-dependencies]\\ntempfile = '
                 '\\"3\\"\\n";\n'
                 '    println!("{:?}", parse_manifest(t));\n'
                 '    println!("{:?}", parse_manifest("[package]\\nversion = \\"1.0.0\\"\\n"));\n'
                 '    println!("{:?}", parse_manifest("[package]\\nname = \\"x\\"\\n"));\n'
                 '    println!("{:?}", parse_manifest("[package]\\nname = \\"x\\"\\nversion = '
                 '\\"0.1.0\\"\\n").map(|m| m.deps.len()));\n'
                 '}\n',
       'hint': 'Запоминайте текущую секцию в переменной; значение в кавычках — через strip_prefix(\'"\') и '
               'strip_suffix(\'"\').',
       'expected': ['Ok(Manifest { name: "hello", version: "0.3.1", deps: {"rand": "0.8", "serde": "1.0"} })',
                    'Err("нет name")',
                    'Err("нет version")',
                    'Ok(0)']},
      {'id': 'r22-dep-graph',
       'mode': 'rust',
       'title': 'Порядок сборки крейтов',
       'statement': 'build_order(deps: &[(&str, &[&str])]) → Result<Vec<String>, String>: каждая пара — '
                    'крейт и его зависимости. Сначала собираются зависимости; из готовых к сборке крейтов '
                    'берите по алфавиту. Зависимость, которой нет в списке, считается внешней и '
                    'игнорируется. Цикл → Err("цикл: a b c") с оставшимися крейтами по алфавиту.',
       'starter': 'fn build_order(deps: &[(&str, &[&str])]) -> Result<Vec<String>, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", build_order(&[("app", &["net", "log"]), ("net", &["log", "libc"]), '
                 '("log", &[]), ("tools", &["log"])]));\n'
                 '    println!("{:?}", build_order(&[("a", &["b"]), ("b", &["c"]), ("c", &["a"]), ("d", '
                 '&[])]));\n'
                 '    println!("{:?}", build_order(&[]));\n'
                 '    println!("{:?}", build_order(&[("z", &[]), ("a", &[])]));\n'
                 '}\n',
       'hint': 'Ключи BTreeMap идут по алфавиту — первый крейт без оставшихся зависимостей и есть следующий.',
       'expected': ['Ok(["log", "net", "app", "tools"])', 'Err("цикл: a b c")', 'Ok([])', 'Ok(["a", "z"])']},
      {'id': 'r22-features-closure',
       'mode': 'rust',
       'title': 'Features: замыкание включённых',
       'statement': 'resolve(features: &[(&str, &[&str])], requested: &[&str]) → Result<Vec<String>, '
                    'String>. Каждый feature включает другие. Результат — все включённые features по '
                    'алфавиту (включая вложенные); «default» включается всегда, если он описан. Неизвестное '
                    'имя в requested или в зависимости → Err("нет feature X").',
       'starter': 'fn resolve(features: &[(&str, &[&str])], requested: &[&str]) -> Result<Vec<String>, '
                  'String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let f: [(&str, &[&str]); 5] = [("default", &["json"]), ("json", &["alloc"]), ("alloc", '
                 '&[]), ("tls", &["alloc", "net"]), ("net", &[])];\n'
                 '    println!("{:?}", resolve(&f, &[]));\n'
                 '    println!("{:?}", resolve(&f, &["tls"]));\n'
                 '    println!("{:?}", resolve(&f, &["ghost"]));\n'
                 '    println!("{:?}", resolve(&[("a", &["zzz"])], &["a"]));\n'
                 '    println!("{:?}", resolve(&[], &[]));\n'
                 '}\n',
       'hint': 'Обход со стеком и множеством уже включённых; на неизвестное имя возвращайте ошибку сразу.',
       'expected': ['Ok(["alloc", "default", "json"])',
                    'Ok(["alloc", "default", "json", "net", "tls"])',
                    'Err("нет feature ghost")',
                    'Err("нет feature zzz")',
                    'Ok([])']},
      {'id': 'r22-lockfile-diff',
       'mode': 'rust',
       'title': 'Сравнение Cargo.lock',
       'statement': 'diff(old, new: &[(&str, &str)]) → Vec<String> — пары (крейт, версия). По алфавиту '
                    'крейтов: «+ имя версия» — появился; «- имя версия» — исчез; «~ имя старая -> новая» — '
                    'версия изменилась. Неизменившиеся не выводить.',
       'starter': 'fn diff(old: &[(&str, &str)], new: &[(&str, &str)]) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let old = [("serde", "1.0.1"), ("rand", "0.8.0"), ("log", "0.4.1")];\n'
                 '    let new = [("serde", "1.0.9"), ("log", "0.4.1"), ("tokio", "1.2.0")];\n'
                 '    for l in diff(&old, &new) {\n'
                 '        println!("{l}");\n'
                 '    }\n'
                 '    println!("{:?}", diff(&new, &new));\n'
                 '    println!("{:?}", diff(&[], &[("a", "1")]));\n'
                 '}\n',
       'hint': 'Объедините имена двух списков в BTreeSet — получите алфавитный порядок; затем match по паре '
               'Option.',
       'expected': ['- rand 0.8.0', '~ serde 1.0.1 -> 1.0.9', '+ tokio 1.2.0', '[]', '["+ a 1"]']},
      {'id': 'r22-cfg-info',
       'mode': 'rust',
       'title': 'cfg!: что известно при сборке',
       'statement': 'build_info() → String вида «mode=<debug|release> os=<linux|other> ptr=<32|64> '
                    'endian=<little|big> unix=<yes|no>». Используйте макрос cfg! (debug_assertions, '
                    'target_os = "linux", target_pointer_width, target_endian, unix). Проверка собрана с '
                    'оптимизацией.',
       'starter': 'fn build_info() -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", build_info());\n'
                 '    println!("{}", std::mem::size_of::<usize>() * 8);\n'
                 '}\n',
       'hint': 'cfg!(условие) — обычное булево выражение, вычисляемое при сборке; пары вида target_os = '
               '"linux".',
       'expected': ['mode=release os=linux ptr=64 endian=little unix=yes', '64']},
      {'id': 'r22-atomic-oncelock',
       'mode': 'rust',
       'title': 'Глобальное состояние: AtomicUsize и OnceLock',
       'statement': 'static NEXT: AtomicUsize — next_id() выдаёт 1, 2, 3, … (fetch_add), reset_ids() '
                    'обнуляет, peek_id() показывает следующий без выдачи. static NAME: OnceLock<String> — '
                    "init_name(s) → bool: true, если это первая инициализация; name() → Option<&'static "
                    'str>.',
       'starter': 'use std::sync::atomic::{AtomicUsize, Ordering};\n'
                  'use std::sync::OnceLock;\n'
                  '\n'
                  'static NEXT: AtomicUsize = AtomicUsize::new(1);\n'
                  'static NAME: OnceLock<String> = OnceLock::new();\n'
                  '\n'
                  'fn next_id() -> usize {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn peek_id() -> usize {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn reset_ids() {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn init_name(s: &str) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn name() -> Option<&'static str> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {} {}", next_id(), next_id(), next_id());\n'
                 '    println!("{}", peek_id());\n'
                 '    reset_ids();\n'
                 '    println!("{} {}", next_id(), peek_id());\n'
                 '    println!("{:?}", name());\n'
                 '    println!("{} {}", init_name("первое"), init_name("второе"));\n'
                 '    println!("{:?}", name());\n'
                 '}\n',
       'hint': 'fetch_add возвращает прежнее значение; OnceLock::set возвращает Err, если значение уже '
               'задано.',
       'expected': ['1 2 3', '4', '1 2', 'None', 'true false', 'Some("первое")']},
      {'id': 'r22-const-fn',
       'mode': 'rust',
       'title': 'const fn: таблицы при сборке',
       'statement': 'const fn fact(n: u32) → u64 (цикл while внутри const fn разрешён). const FACTS: [u64; '
                    '11] — факториалы 0..=10, заполненные при сборке через const-блок. const fn gcd(a, b) → '
                    'u64 (Евклид). const fn is_pow2(x: u32) → bool. Таблица и функции вычисляются '
                    'компилятором.',
       'starter': 'const fn fact(n: u32) -> u64 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'const fn gcd(a: u64, b: u64) -> u64 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'const fn is_pow2(x: u32) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  '// const FACTS: [u64; 11] = ...\n',
       'driver': 'const G: u64 = gcd(84, 36);\n'
                 'const P: bool = is_pow2(1024);\n'
                 '\n'
                 'fn main() {\n'
                 '    println!("{:?}", FACTS);\n'
                 '    println!("{} {}", G, P);\n'
                 '    println!("{} {}", is_pow2(0), is_pow2(96));\n'
                 '    println!("{}", gcd(17, 5));\n'
                 '    let a = [0u8; FACTS.len()];\n'
                 '    println!("{}", a.len());\n'
                 '}\n',
       'hint': 'В const fn нет for и замыканий — только while, let mut и арифметика; таблицу заполняет '
               'блок-константа.',
       'expected': ['[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]',
                    '12 true',
                    'false false',
                    '1',
                    '11']},
      {'id': 'r22-doc-extractor',
       'mode': 'rust',
       'title': 'Мини-rustdoc: извлечь документацию',
       'statement': 'extract_docs(src: &str) → Vec<(String, String)>: для каждой функции (fn имя(… или pub '
                    'fn имя(…) собрать текст идущих перед ней строк «///» (без «///» и пробела после, '
                    'склеенных через пробел). Функции без документации пропускать. Порядок — как в '
                    'исходнике.',
       'starter': 'fn extract_docs(src: &str) -> Vec<(String, String)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let src = "/// Складывает.\\n/// Два числа.\\npub fn add(a: i32, b: i32) -> i32 { a + '
                 'b }\\n\\nfn hidden() {}\\n\\n/// Печатает.\\n#[inline]\\nfn show() {}\\n\\n/// Висит в '
                 'воздухе\\nstruct S;\\nfn after() {}\\n";\n'
                 '    for (n, d) in extract_docs(src) {\n'
                 '        println!("{n}: {d}");\n'
                 '    }\n'
                 '    println!("{}", extract_docs("fn a() {}").len());\n'
                 '}\n',
       'hint': 'Копите строки /// в вектор; на строке с fn — сохраните и очистите; атрибут #[...] между '
               'документацией и функцией её не сбрасывает.',
       'expected': ['add: Складывает. Два числа.', 'show: Печатает.', '0']},
      {'id': 'r22-mini-test-runner',
       'mode': 'rust',
       'title': 'Мини-раннер тестов',
       'statement': 'type TestFn = fn() → Result<(), String>. run_tests(tests: &[(&str, TestFn)]) → (usize, '
                    'usize, Vec<String>): число прошедших, число упавших и строки отчёта «test <имя> ... ok» '
                    '/ «test <имя> ... FAILED: <сообщение>». Паника внутри теста — тоже провал: «FAILED: '
                    'panicked» (ловите через std::panic::catch_unwind). Раннер не должен падать сам.',
       'starter': 'type TestFn = fn() -> Result<(), String>;\n'
                  '\n'
                  'fn run_tests(tests: &[(&str, TestFn)]) -> (usize, usize, Vec<String>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn good() -> Result<(), String> {\n'
                 '    Ok(())\n'
                 '}\n'
                 'fn bad() -> Result<(), String> {\n'
                 '    Err("1 != 2".to_string())\n'
                 '}\n'
                 'fn boom() -> Result<(), String> {\n'
                 '    let v: Vec<i32> = vec![];\n'
                 '    let _ = v[3];\n'
                 '    Ok(())\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    std::panic::set_hook(Box::new(|_| {}));\n'
                 '    let (p, f, rep) = run_tests(&[("good", good), ("bad", bad), ("boom", boom), ("good2", '
                 'good)]);\n'
                 '    for l in &rep {\n'
                 '        println!("{l}");\n'
                 '    }\n'
                 '    println!("{p} passed, {f} failed");\n'
                 '    println!("{:?}", run_tests(&[]));\n'
                 '}\n',
       'hint': 'catch_unwind(*t) возвращает Result<Result<(), String>, Box<dyn Any + Send>>: три случая — '
               'ok, Err и паника.',
       'expected': ['test good ... ok',
                    'test bad ... FAILED: 1 != 2',
                    'test boom ... FAILED: panicked',
                    'test good2 ... ok',
                    '2 passed, 2 failed',
                    '(0, 0, [])']},
      {'id': 'r22-assert-helpers',
       'mode': 'rust',
       'title': 'Свои проверки, возвращающие Result',
       'statement': 'check_eq<T: PartialEq + Debug>(left, right) → Result<(), String> «left: <l:?>, right: '
                    '<r:?>» при неравенстве. check_close(a, b, eps) → Result<(), String> «|a-b| = <d> > '
                    '<eps>». check_sorted<T: PartialOrd + Debug>(v) → Result<(), String> «не отсортировано '
                    'на позиции <i>: <a:?> > <b:?>» (индекс первого нарушения пары). Все проверки — функции, '
                    'не паникуют.',
       'starter': 'use std::fmt::Debug;\n'
                  '\n'
                  'fn check_eq<T: PartialEq + Debug>(left: T, right: T) -> Result<(), String> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn check_close(a: f64, b: f64, eps: f64) -> Result<(), String> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn check_sorted<T: PartialOrd + Debug>(v: &[T]) -> Result<(), String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", check_eq(2 + 2, 4));\n'
                 '    println!("{:?}", check_eq("a", "b"));\n'
                 '    println!("{:?}", check_eq(vec![1, 2], vec![1, 3]));\n'
                 '    println!("{:?} {:?}", check_close(0.1 + 0.2, 0.3, 1e-9), check_close(1.0, 1.5, 0.1));\n'
                 '    println!("{:?} {:?}", check_sorted(&[1, 2, 2, 5]), check_sorted(&[1, 3, 2, 4]));\n'
                 '    println!("{:?}", check_sorted::<i32>(&[]));\n'
                 '}\n',
       'hint': 'Сообщение собирайте format!-ом с {:?}; пара окон windows(2) даёт индекс первого нарушения.',
       'expected': ['Ok(())',
                    'Err("left: \\"a\\", right: \\"b\\"")',
                    'Err("left: [1, 2], right: [1, 3]")',
                    'Ok(()) Err("|a-b| = 0.5 > 0.1")',
                    'Ok(()) Err("не отсортировано на позиции 1: 3 > 2")',
                    'Ok(())']},
      {'id': 'r22-write-tests-abs',
       'mode': 'rust',
       'title': 'Напишите тесты: abs и её мутанты',
       'statement': 'Вам нужно написать failures_abs(f: &dyn Fn(i32) → i32) → usize — набор проверок для '
                    'функции абсолютного значения: вернуть число не прошедших проверок. Драйвер запускает '
                    'ваш набор на верной реализации (должно быть 0 провалов) и на пяти сломанных — каждая '
                    'обязана быть поймана хотя бы одним провалом.',
       'starter': 'fn failures_abs(f: &dyn Fn(i32) -> i32) -> usize {\n'
                  '    let mut fails = 0;\n'
                  '    // добавляйте проверки: if f(вход) != ожидаемое { fails += 1; }\n'
                  '    fails\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let good = |x: i32| x.wrapping_abs();\n'
                 '    println!("good: {}", failures_abs(&good));\n'
                 '    let m1 = |x: i32| x;\n'
                 '    let m2 = |x: i32| if x < 0 { x } else { -x };\n'
                 '    let m3 = |x: i32| if x < -1 { -x } else { x };\n'
                 '    let m4 = |x: i32| if x == 0 { 1 } else { x.abs() };\n'
                 '    let m5 = |x: i32| x.abs().min(1000);\n'
                 '    let names = ["identity", "negate", "minus-one", "zero", "clamp"];\n'
                 '    let ms: [&dyn Fn(i32) -> i32; 5] = [&m1, &m2, &m3, &m4, &m5];\n'
                 '    for (n, m) in names.iter().zip(ms.iter()) {\n'
                 '        let f = failures_abs(*m);\n'
                 '        println!("{n}: {}", if f > 0 { "caught" } else { "SURVIVED" });\n'
                 '    }\n'
                 '}\n',
       'hint': 'Проверьте ноль, плюс и минус единицу, обычные числа обоих знаков и очень большие по модулю — '
               'каждый мутант ломается на своей границе.',
       'expected': ['good: 0',
                    'identity: caught',
                    'negate: caught',
                    'minus-one: caught',
                    'zero: caught',
                    'clamp: caught']},
      {'id': 'r22-write-tests-leap',
       'mode': 'rust',
       'title': 'Напишите тесты: високосный год',
       'statement': 'failures_leap(f: &dyn Fn(i32) → bool) → usize — проверки is_leap_year. Верная '
                    'реализация: делится на 4, кроме кратных 100, кроме кратных 400. Драйвер проверяет, что '
                    'на верной реализации провалов 0, а все четыре мутанта пойманы.',
       'starter': 'fn failures_leap(f: &dyn Fn(i32) -> bool) -> usize {\n'
                  '    let mut fails = 0;\n'
                  '    // if f(год) != ожидаемое { fails += 1; }\n'
                  '    fails\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let good = |y: i32| (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;\n'
                 '    println!("good: {}", failures_leap(&good));\n'
                 '    let m1 = |y: i32| y % 4 == 0;\n'
                 '    let m2 = |y: i32| y % 4 == 0 && y % 100 != 0;\n'
                 '    let m3 = |y: i32| y % 4 == 0 && (y % 100 != 0 || y % 200 == 0);\n'
                 '    let m4 = |y: i32| (y % 4 == 0 && y % 100 != 0) || y % 100 == 0;\n'
                 '    let ms: [&dyn Fn(i32) -> bool; 4] = [&m1, &m2, &m3, &m4];\n'
                 '    let names = ["only-4", "no-400", "200-rule", "100-always"];\n'
                 '    for (n, m) in names.iter().zip(ms.iter()) {\n'
                 '        println!("{n}: {}", if failures_leap(*m) > 0 { "caught" } else { "SURVIVED" });\n'
                 '    }\n'
                 '}\n',
       'hint': 'Нужны годы разных видов: обычный високосный, обычный невисокосный, кратный 100, кратный 400 '
               'и кратный 200, но не 400.',
       'expected': ['good: 0', 'only-4: caught', 'no-400: caught', '200-rule: caught', '100-always: caught']},
      {'id': 'r22-write-tests-clamp',
       'mode': 'rust',
       'title': 'Напишите тесты: clamp(x, lo, hi)',
       'statement': 'failures_clamp(f: &dyn Fn(i32, i32, i32) → i32) → usize — проверки clamp(x, lo, hi) = '
                    'x, обрезанный в [lo, hi] (считайте lo ≤ hi). Верная реализация даёт 0 провалов; четыре '
                    'мутанта обязаны быть пойманы.',
       'starter': 'fn failures_clamp(f: &dyn Fn(i32, i32, i32) -> i32) -> usize {\n'
                  '    let mut fails = 0;\n'
                  '    // if f(x, lo, hi) != ожидаемое { fails += 1; }\n'
                  '    fails\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let good = |x: i32, lo: i32, hi: i32| x.max(lo).min(hi);\n'
                 '    println!("good: {}", failures_clamp(&good));\n'
                 '    let m1 = |x: i32, lo: i32, _hi: i32| x.max(lo);\n'
                 '    let m2 = |x: i32, _lo: i32, hi: i32| x.min(hi);\n'
                 '    let m3 = |x: i32, lo: i32, hi: i32| if x < lo { lo } else if x > hi { hi - 1 } else { '
                 'x };\n'
                 '    let m4 = |x: i32, lo: i32, hi: i32| if x <= lo { lo + 1 } else if x > hi { hi } else { '
                 'x };\n'
                 '    let ms: [&dyn Fn(i32, i32, i32) -> i32; 4] = [&m1, &m2, &m3, &m4];\n'
                 '    let names = ["no-upper", "no-lower", "off-by-one-hi", "off-by-one-lo"];\n'
                 '    for (n, m) in names.iter().zip(ms.iter()) {\n'
                 '        println!("{n}: {}", if failures_clamp(*m) > 0 { "caught" } else { "SURVIVED" });\n'
                 '    }\n'
                 '}\n',
       'hint': 'Проверяйте внутри диапазона, ровно на обеих границах, за каждой границей, вырожденный '
               'диапазон lo = hi и отрицательные границы.',
       'expected': ['good: 0',
                    'no-upper: caught',
                    'no-lower: caught',
                    'off-by-one-hi: caught',
                    'off-by-one-lo: caught']},
      {'id': 'r22-write-tests-stack',
       'mode': 'rust',
       'title': 'Напишите тесты: реализации стека',
       'statement': 'Трейт StackLike: new() → Self, push(&mut self, i32), pop(&mut self) → Option<i32>, '
                    'peek(&self) → Option<i32>, len(&self) → usize. Напишите failures<S: StackLike>() → '
                    'usize: проверки любой реализации. Драйвер даёт верный стек и три сломанных (очередь '
                    'вместо стека; pop не уменьшает длину; peek снимает элемент) — все должны быть пойманы.',
       'starter': 'trait StackLike {\n'
                  '    fn new() -> Self;\n'
                  '    fn push(&mut self, x: i32);\n'
                  '    fn pop(&mut self) -> Option<i32>;\n'
                  '    fn peek(&self) -> Option<i32>;\n'
                  '    fn len(&self) -> usize;\n'
                  '}\n'
                  '\n'
                  'fn failures<S: StackLike>() -> usize {\n'
                  '    let mut fails = 0;\n'
                  '    // let mut s = S::new(); ... if условие_нарушено { fails += 1; }\n'
                  '    fails\n'
                  '}\n',
       'driver': 'struct Good(Vec<i32>);\n'
                 'impl StackLike for Good {\n'
                 '    fn new() -> Good { Good(vec![]) }\n'
                 '    fn push(&mut self, x: i32) { self.0.push(x) }\n'
                 '    fn pop(&mut self) -> Option<i32> { self.0.pop() }\n'
                 '    fn peek(&self) -> Option<i32> { self.0.last().copied() }\n'
                 '    fn len(&self) -> usize { self.0.len() }\n'
                 '}\n'
                 'struct Fifo(Vec<i32>);\n'
                 'impl StackLike for Fifo {\n'
                 '    fn new() -> Fifo { Fifo(vec![]) }\n'
                 '    fn push(&mut self, x: i32) { self.0.push(x) }\n'
                 '    fn pop(&mut self) -> Option<i32> { if self.0.is_empty() { None } else { '
                 'Some(self.0.remove(0)) } }\n'
                 '    fn peek(&self) -> Option<i32> { self.0.first().copied() }\n'
                 '    fn len(&self) -> usize { self.0.len() }\n'
                 '}\n'
                 'struct NoShrink(Vec<i32>, usize);\n'
                 'impl StackLike for NoShrink {\n'
                 '    fn new() -> NoShrink { NoShrink(vec![], 0) }\n'
                 '    fn push(&mut self, x: i32) { self.0.push(x); self.1 += 1 }\n'
                 '    fn pop(&mut self) -> Option<i32> { self.0.pop() }\n'
                 '    fn peek(&self) -> Option<i32> { self.0.last().copied() }\n'
                 '    fn len(&self) -> usize { self.1 }\n'
                 '}\n'
                 'struct PeekPops(Vec<i32>);\n'
                 'impl StackLike for PeekPops {\n'
                 '    fn new() -> PeekPops { PeekPops(vec![]) }\n'
                 '    fn push(&mut self, x: i32) { self.0.push(x) }\n'
                 '    fn pop(&mut self) -> Option<i32> { self.0.pop() }\n'
                 '    fn peek(&self) -> Option<i32> { self.0.last().copied().map(|x| x + 0) }\n'
                 '    fn len(&self) -> usize { if self.0.len() > 2 { self.0.len() - 1 } else { self.0.len() '
                 '} }\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    println!("good: {}", failures::<Good>());\n'
                 '    for (n, f) in [("fifo", failures::<Fifo>()), ("no-shrink", failures::<NoShrink>()), '
                 '("len-bug", failures::<PeekPops>())] {\n'
                 '        println!("{n}: {}", if f > 0 { "caught" } else { "SURVIVED" });\n'
                 '    }\n'
                 '}\n',
       'hint': 'Проверяйте порядок LIFO на нескольких элементах, длину после каждой операции, пустой стек и '
               'то, что peek ничего не удаляет.',
       'expected': ['good: 0', 'fifo: caught', 'no-shrink: caught', 'len-bug: caught']},
      {'id': 'r22-parse-duration',
       'mode': 'rust',
       'title': 'Разбор «1h30m15s»: таблица случаев',
       'statement': 'parse_duration(s) → Option<u64> — секунды: единицы h (3600), m (60), s (1), каждая не '
                    'более одного раза и в порядке h, m, s; число без знака, не пустое. «90s» → 90, '
                    '«1h30m15s» → 5415, «2h» → 7200. Пустая строка, число без единицы, неизвестная единица, '
                    'повтор или неправильный порядок → None.',
       'starter': 'fn parse_duration(s: &str) -> Option<u64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let cases = ["1h30m15s", "90s", "2h", "45m", "0s", "", "15", "h", "1x", "1m1h", '
                 '"1h1h", "12m3", "5s5s", "003m"];\n'
                 '    for c in cases {\n'
                 '        println!("{:>10} -> {:?}", format!("{:?}", c), parse_duration(c));\n'
                 '    }\n'
                 '}\n',
       'hint': 'Копите цифры в строке; встретили букву — переводите накопленное число в секунды и проверяйте '
               'порядок единиц.',
       'expected': ['"1h30m15s" -> Some(5415)',
                    '     "90s" -> Some(90)',
                    '      "2h" -> Some(7200)',
                    '     "45m" -> Some(2700)',
                    '      "0s" -> Some(0)',
                    '        "" -> None',
                    '      "15" -> None',
                    '       "h" -> None',
                    '      "1x" -> None',
                    '    "1m1h" -> None',
                    '    "1h1h" -> None',
                    '    "12m3" -> None',
                    '    "5s5s" -> None',
                    '    "003m" -> Some(180)']},
      {'id': 'r22-error-api',
       'mode': 'rust',
       'title': 'Ошибки библиотеки: enum, Display, Error, From',
       'statement': 'ConfigError: Missing(String) — нет ключа, BadNumber { key: String, source: '
                    'ParseIntError }. Реализуйте Display («нет ключа X» / «ключ X: неверное число»), '
                    'std::error::Error с методом source (для BadNumber — причина, для Missing — None). '
                    'load(text) → Result<Settings, ConfigError>: строки «ключ=значение»; обязательны port и '
                    'workers (числа u16 и u8).',
       'starter': 'use std::error::Error;\n'
                  'use std::fmt;\n'
                  'use std::num::ParseIntError;\n'
                  '\n'
                  '#[derive(Debug)]\n'
                  'enum ConfigError {\n'
                  '    Missing(String),\n'
                  '    BadNumber { key: String, source: ParseIntError },\n'
                  '}\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'struct Settings {\n'
                  '    port: u16,\n'
                  '    workers: u8,\n'
                  '}\n'
                  '\n'
                  '// impl Display и Error для ConfigError\n'
                  '\n'
                  'fn load(text: &str) -> Result<Settings, ConfigError> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", load("port = 8080\\nworkers=4"));\n'
                 '    for t in ["workers=4", "port=80", "port=70000\\nworkers=1", "port=1\\nworkers=abc"] {\n'
                 '        match load(t) {\n'
                 '            Ok(s) => println!("ok {:?}", s),\n'
                 '            Err(e) => println!("{} | причина: {:?}", e, e.source().map(|s| '
                 's.to_string())),\n'
                 '        }\n'
                 '    }\n'
                 '}\n',
       'hint': 'source() возвращает Some(source) как &dyn Error; для u16 и u8 число 70000 и 256 — это уже '
               'ошибка разбора.',
       'expected': ['Ok(Settings { port: 8080, workers: 4 })',
                    'нет ключа port | причина: None',
                    'нет ключа workers | причина: None',
                    'ключ port: неверное число | причина: Some("number too large to fit in target type")',
                    'ключ workers: неверное число | причина: Some("invalid digit found in string")']},
      {'id': 'r22-module-tree',
       'mode': 'rust',
       'title': 'Дерево модулей из путей',
       'statement': 'render_tree(paths: &[&str]) → String: пути вида «net::tcp::connect» собираются в '
                    'дерево; каждый уровень — на отдельной строке с отступом в два пробела на глубину, дети '
                    'по алфавиту, повторы объединяются. Пустой список — пустая строка.',
       'starter': 'fn render_tree(paths: &[&str]) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    print!("{}", render_tree(&["net::tcp::connect", "net::udp", "db::query", '
                 '"net::tcp::listen", "net::tcp::connect", "app"]));\n'
                 '    println!("[{}]", render_tree(&[]));\n'
                 '}\n',
       'hint': 'Дерево — вложенные BTreeMap (или узел с BTreeMap детей); entry(...).or_default() создаёт '
               'недостающие уровни.',
       'expected': ['app', 'db', '  query', 'net', '  tcp', '    connect', '    listen', '  udp', '[]']},
      {'id': 'r22-public-surface',
       'mode': 'rust',
       'title': 'Публичная поверхность: что видно снаружи',
       'statement': 'Элемент описан путём и видимостью каждого сегмента: Item { path: &str (через ::), vis: '
                    'Vec<Vis> } с Vis ∈ {Private, Crate, Pub} (длины равны). surface(items) → (Vec<String>, '
                    'Vec<String>): первое — элементы, видимые другим крейтам (все сегменты Pub), второе — '
                    'только внутри крейта (нет Private, но есть Crate). Оба списка по алфавиту.',
       'starter': '#[derive(Clone, Copy, PartialEq)]\n'
                  'enum Vis {\n'
                  '    Private,\n'
                  '    Crate,\n'
                  '    Pub,\n'
                  '}\n'
                  '\n'
                  'struct Item {\n'
                  "    path: &'static str,\n"
                  '    vis: Vec<Vis>,\n'
                  '}\n'
                  '\n'
                  'fn surface(items: &[Item]) -> (Vec<String>, Vec<String>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use Vis::*;\n'
                 '    let items = vec![\n'
                 '        Item { path: "net::connect", vis: vec![Pub, Pub] },\n'
                 '        Item { path: "net::tcp::listen", vis: vec![Pub, Crate, Pub] },\n'
                 '        Item { path: "net::tcp::raw", vis: vec![Pub, Pub, Private] },\n'
                 '        Item { path: "db::query", vis: vec![Pub, Pub] },\n'
                 '        Item { path: "util::hash", vis: vec![Crate, Pub] },\n'
                 '        Item { path: "secret::key", vis: vec![Private, Pub] },\n'
                 '    ];\n'
                 '    let (p, c) = surface(&items);\n'
                 '    println!("{:?}", p);\n'
                 '    println!("{:?}", c);\n'
                 '    println!("{:?}", surface(&[]));\n'
                 '}\n',
       'hint': 'Элемент виден снаружи, только если открыты все сегменты пути: достаточно одного закрытого '
               'родителя, чтобы спрятать потомка.',
       'expected': ['["db::query", "net::connect"]', '["net::tcp::listen", "util::hash"]', '([], [])']}]}
