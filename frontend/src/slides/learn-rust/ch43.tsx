import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, Node, RsCode } from "../widgets.tsx";
// Слайды для «Изучаем Rust», глава 43 — «Данные и PostgreSQL».
// Тот же дизайн-код, что и в главах 1–5: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

const Slide = makeSlide("ИЗУЧАЕМ RUST / ВЕБ-СЕРВЕР / ГЛАВА 43", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Как Rust говорит с Postgres"}
      sub={"Глава 43 · Веб-сервер"}
      main={"Под библиотеками — бинарный протокол, отображение строк в типы, пул, транзакции и миграции."}
    >
      <div className="s-grid2">
        {([["метка · длина · тело", "Протокол", "Сообщения в сетевом порядке"], ["FromColumn", "Типы", "NULL — это Option"], ["$1, $2", "Параметры", "Никакой склейки значений"], ["Pool · Tx · migrate", "Инфраструктура", "RAII и версии схемы"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Строка результата — структура"}
      sub={"Типизация вместо текста"}
      main={"Колонка, где допустим NULL, — Option<T>: забыть про пропуск компилятор не даст."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"id  BIGINT NOT NULL"} sub={"i64"} />
        <Node kind="green" mono={true} title={"name  TEXT NOT NULL"} sub={"String"} />
        <Node kind="" mono={true} title={"age  INT NULL"} sub={"Option<i32>"} />
      </div>
      <div className="s-note">{"Библиотеки генерируют отображение макросом (#[derive(FromRow)]); ниже мы напишем его руками."}</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Сообщения протокола"}
      sub={"Стартовое сообщение и простой запрос"}
      main={"Клиентское сообщение: метка, длина (включая себя), тело; строки — с нулевым байтом на конце."}
    >
      <RsCode>{`fn startup_message(user: &str, db: &str) -> Vec<u8> {
    let mut body = Vec::new();
    body.extend_from_slice(&196608u32.to_be_bytes());
    for (k, v) in [("user", user), ("database", db)] {
        body.extend_from_slice(k.as_bytes());
        body.push(0);
        body.extend_from_slice(v.as_bytes());
        body.push(0);
    }
    body.push(0);
    let mut msg = ((body.len() + 4) as u32).to_be_bytes().to_vec();
    msg.extend(body);
    msg
}

fn query_message(sql: &str) -> Vec<u8> {
    let mut msg = vec![b'Q'];
    msg.extend_from_slice(&((sql.len() + 5) as u32).to_be_bytes());
    msg.extend_from_slice(sql.as_bytes());
    msg.push(0);
    msg
}

fn main() {
    let s = startup_message("app", "shop");
    println!("{} {:?}", s.len(), &s[..8]);
    let q = query_message("SELECT 1");
    println!("{:?} {}", q[0] as char, q.len());
    println!("{:?}", &q[1..5]);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"32 [0, 0, 0, 32, 0, 3, 0, 0]\n'Q' 14\n[0, 0, 0, 13]"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Ответ сервера"}
      sub={"DataRow: длины значений и NULL"}
      main={"Длина −1 — NULL; неполное сообщение — повод дочитать, а не ошибка."}
    >
      <RsCode>{`fn read_message(buf: &[u8]) -> Option<(u8, &[u8], usize)> {
    if buf.len() < 5 {
        return None;
    }
    let len = u32::from_be_bytes([buf[1], buf[2], buf[3], buf[4]]) as usize;
    if buf.len() < 1 + len {
        return None;
    }
    Some((buf[0], &buf[5..1 + len], 1 + len))
}

fn data_row(payload: &[u8]) -> Vec<Option<String>> {
    let n = i16::from_be_bytes([payload[0], payload[1]]) as usize;
    let mut pos = 2;
    let mut cols = Vec::new();
    for _ in 0..n {
        let len = i32::from_be_bytes(payload[pos..pos + 4].try_into().unwrap());
        pos += 4;
        if len < 0 {
            cols.push(None);
        } else {
            cols.push(Some(String::from_utf8_lossy(&payload[pos..pos + len as usize]).into_owned()));
            pos += len as usize;
        }
    }
    cols
}

fn main() {
    let mut p = vec![0, 3];
    for c in [Some("42"), None, Some("ok")] {
        match c {
            Some(s) => {
                p.extend_from_slice(&(s.len() as i32).to_be_bytes());
                p.extend_from_slice(s.as_bytes());
            }
            None => p.extend_from_slice(&(-1i32).to_be_bytes()),
        }
    }
    let mut msg = vec![b'D'];
    msg.extend_from_slice(&((p.len() + 4) as u32).to_be_bytes());
    msg.extend(p);
    msg.extend_from_slice(b"Z\\0\\0\\0\\x05I");
    let (tag, payload, used) = read_message(&msg).unwrap();
    println!("{} {:?}", tag as char, data_row(payload));
    let (tag2, p2, _) = read_message(&msg[used..]).unwrap();
    println!("{} {:?}", tag2 as char, p2);
    println!("{:?}", read_message(&msg[..10]).map(|m| m.0));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"D [Some(\"42\"), None, Some(\"ok\")]\nZ [73]\nNone"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Отображение в типы"}
      sub={"Трейт FromColumn"}
      main={"Один трейт — для i64, bool, String и Option<T> над любым из них."}
    >
      <RsCode>{`trait FromColumn: Sized {
    fn from_col(c: Option<&str>) -> Result<Self, String>;
}

impl FromColumn for i64 {
    fn from_col(c: Option<&str>) -> Result<i64, String> {
        c.ok_or("NULL")?.parse().map_err(|e| format!("{}", e))
    }
}
impl FromColumn for bool {
    fn from_col(c: Option<&str>) -> Result<bool, String> {
        match c {
            Some("t") => Ok(true),
            Some("f") => Ok(false),
            other => Err(format!("bad bool {:?}", other)),
        }
    }
}
impl FromColumn for String {
    fn from_col(c: Option<&str>) -> Result<String, String> {
        c.map(|s| s.to_string()).ok_or("NULL".to_string())
    }
}
impl<T: FromColumn> FromColumn for Option<T> {
    fn from_col(c: Option<&str>) -> Result<Option<T>, String> {
        match c {
            None => Ok(None),
            some => T::from_col(some).map(Some),
        }
    }
}

#[derive(Debug)]
struct User {
    id: i64,
    name: String,
    active: bool,
    age: Option<i64>,
}

fn user_from_row(row: &[Option<&str>]) -> Result<User, String> {
    Ok(User {
        id: i64::from_col(row[0])?,
        name: String::from_col(row[1])?,
        active: bool::from_col(row[2])?,
        age: Option::<i64>::from_col(row[3])?,
    })
}

fn main() {
    println!("{:?}", user_from_row(&[Some("7"), Some("Ann"), Some("t"), None]));
    println!("{:?}", user_from_row(&[Some("8"), Some("Bob"), Some("f"), Some("41")]));
    println!("{:?}", user_from_row(&[Some("x"), Some("Eve"), Some("t"), None]));
    println!("{:?}", user_from_row(&[Some("9"), None, Some("t"), None]));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Ok(User { id: 7, name: \"Ann\", active: true, age: None })\nOk(User { id: 8, name: \"Bob\", active: false, age: Some(41) })\nErr(\"invalid digit found in string\")\nErr(\"NULL\")"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Внедрение SQL"}
      sub={"Склейка против параметров"}
      main={"Параметры передаются отдельно от текста запроса — сервер никогда не смешивает их с кодом."}
    >
      <RsCode>{`fn quote_literal(s: &str) -> String {
    format!("'{}'", s.replace('\\'', "''"))
}

fn naive(name: &str) -> String {
    format!("SELECT * FROM users WHERE name = '{}'", name)
}

fn main() {
    let evil = "x' OR '1'='1";
    println!("{}", naive(evil));
    println!("SELECT * FROM users WHERE name = {}", quote_literal(evil));
    println!("SELECT * FROM users WHERE name = $1 AND age > $2");
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"SELECT * FROM users WHERE name = 'x' OR '1'='1'\nSELECT * FROM users WHERE name = 'x'' OR ''1''=''1'\nSELECT * FROM users WHERE name = $1 AND age > $2"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Построитель запросов"}
      sub={"Текст отдельно, параметры отдельно"}
      main={"Значения — только через параметры; имена таблиц и колонок берите из заранее известного набора."}
    >
      <RsCode>{`struct Select {
    table: String,
    conds: Vec<String>,
    params: Vec<String>,
    order: Option<String>,
    limit: Option<u32>,
}

impl Select {
    fn from(table: &str) -> Select {
        Select { table: table.into(), conds: vec![], params: vec![], order: None, limit: None }
    }
    fn filter(mut self, col: &str, op: &str, value: &str) -> Select {
        self.params.push(value.to_string());
        self.conds.push(format!("{} {} \${}", col, op, self.params.len()));
        self
    }
    fn order_by(mut self, col: &str, desc: bool) -> Select {
        self.order = Some(format!("{} {}", col, if desc { "DESC" } else { "ASC" }));
        self
    }
    fn limit(mut self, n: u32) -> Select {
        self.limit = Some(n);
        self
    }
    fn build(&self) -> (String, &[String]) {
        let mut sql = format!("SELECT * FROM {}", self.table);
        if !self.conds.is_empty() {
            sql += &format!(" WHERE {}", self.conds.join(" AND "));
        }
        if let Some(o) = &self.order {
            sql += &format!(" ORDER BY {}", o);
        }
        if let Some(n) = self.limit {
            sql += &format!(" LIMIT {}", n);
        }
        (sql, &self.params)
    }
}

fn main() {
    let q = Select::from("users")
        .filter("age", ">", "18")
        .filter("city", "=", "Moscow")
        .order_by("name", false)
        .limit(10);
    let (sql, params) = q.build();
    println!("{}", sql);
    println!("{:?}", params);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"SELECT * FROM users WHERE age > $1 AND city = $2 ORDER BY name ASC LIMIT 10\n[\"18\", \"Moscow\"]"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Пул соединений"}
      sub={"Mutex + Condvar + Drop"}
      main={"Обёртка соединения возвращает его в пул в Drop — вернуть забыть нельзя."}
    >
      <RsCode>{`use std::sync::{Arc, Condvar, Mutex};
use std::thread;

struct Pool {
    conns: Mutex<Vec<u32>>,
    cv: Condvar,
}

struct PooledConn {
    id: u32,
    pool: Arc<Pool>,
}

impl Pool {
    fn new(n: u32) -> Arc<Pool> {
        Arc::new(Pool { conns: Mutex::new((1..=n).collect()), cv: Condvar::new() })
    }
    fn get(self: &Arc<Self>) -> PooledConn {
        let mut c = self.conns.lock().unwrap();
        while c.is_empty() {
            c = self.cv.wait(c).unwrap();
        }
        PooledConn { id: c.pop().unwrap(), pool: Arc::clone(self) }
    }
}

impl Drop for PooledConn {
    fn drop(&mut self) {
        self.pool.conns.lock().unwrap().push(self.id);
        self.pool.cv.notify_one();
    }
}

fn main() {
    let pool = Pool::new(2);
    let hs: Vec<_> = (0..6)
        .map(|i| {
            let p = Arc::clone(&pool);
            thread::spawn(move || {
                let c = p.get();
                thread::sleep(std::time::Duration::from_millis(5));
                (i, c.id <= 2)
            })
        })
        .collect();
    let ok = hs.into_iter().map(|h| h.join().unwrap()).all(|(_, ok)| ok);
    println!("{} {}", ok, pool.conns.lock().unwrap().len());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"true 2"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Транзакция с автооткатом"}
      sub={"Охранный объект и Drop"}
      main={"Выход по ошибке уничтожает Tx без commit — деструктор сам отправляет ROLLBACK."}
    >
      <RsCode>{`use std::cell::RefCell;

struct Conn {
    log: RefCell<Vec<String>>,
}

impl Conn {
    fn exec(&self, sql: &str) {
        self.log.borrow_mut().push(sql.to_string());
    }
}

struct Tx<'a> {
    conn: &'a Conn,
    done: bool,
}

impl<'a> Tx<'a> {
    fn begin(conn: &'a Conn) -> Tx<'a> {
        conn.exec("BEGIN");
        Tx { conn, done: false }
    }
    fn commit(mut self) {
        self.conn.exec("COMMIT");
        self.done = true;
    }
}

impl<'a> Drop for Tx<'a> {
    fn drop(&mut self) {
        if !self.done {
            self.conn.exec("ROLLBACK");
        }
    }
}

fn transfer(conn: &Conn, fail: bool) -> Result<(), String> {
    let tx = Tx::begin(conn);
    conn.exec("UPDATE accounts SET balance = balance - 10 WHERE id = 1");
    if fail {
        return Err("boom".to_string());
    }
    conn.exec("UPDATE accounts SET balance = balance + 10 WHERE id = 2");
    tx.commit();
    Ok(())
}

fn main() {
    let c = Conn { log: RefCell::new(vec![]) };
    println!("{:?}", transfer(&c, false));
    println!("{:?}", transfer(&c, true));
    for l in c.log.borrow().iter() {
        println!("{}", l);
    }
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Ok(())\nErr(\"boom\")\nBEGIN\nUPDATE accounts SET balance = balance - 10 WHERE id = 1\nUPDATE accounts SET balance = balance + 10 WHERE id = 2\nCOMMIT\nBEGIN\nUPDATE accounts SET balance = balance - 10 WHERE id = 1\nROLLBACK"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Миграции"}
      sub={"Версии применяются один раз и по порядку"}
      main={"Повторный запуск ничего не делает — миграции идемпотентны и безопасны на каждом старте."}
    >
      <RsCode>{`struct Migration {
    version: u32,
    sql: &'static str,
}

fn migrate(applied: &mut Vec<u32>, log: &mut Vec<String>, migrations: &[Migration]) -> usize {
    let mut n = 0;
    let mut sorted: Vec<&Migration> = migrations.iter().collect();
    sorted.sort_by_key(|m| m.version);
    for m in sorted {
        if applied.contains(&m.version) {
            continue;
        }
        log.push(format!("apply {}: {}", m.version, m.sql));
        applied.push(m.version);
        n += 1;
    }
    n
}

fn main() {
    let ms = [
        Migration { version: 2, sql: "ALTER TABLE users ADD age INT" },
        Migration { version: 1, sql: "CREATE TABLE users (id SERIAL, name TEXT)" },
        Migration { version: 3, sql: "CREATE INDEX ON users (name)" },
    ];
    let (mut applied, mut log) = (vec![1], Vec::new());
    println!("{}", migrate(&mut applied, &mut log, &ms));
    println!("{}", migrate(&mut applied, &mut log, &ms));
    println!("{:?}", applied);
    for l in &log {
        println!("{}", l);
    }
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2\n0\n[1, 2, 3]\napply 2: ALTER TABLE users ADD age INT\napply 3: CREATE INDEX ON users (name)"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Репозиторий"}
      sub={"Бизнес-логика без базы"}
      main={"Логика принимает любой UserRepo — в тестах это таблица в памяти, в продакшене — Postgres."}
    >
      <RsCode>{`use std::collections::BTreeMap;

trait UserRepo {
    fn add(&mut self, name: &str) -> u32;
    fn find(&self, id: u32) -> Option<String>;
}

struct MemRepo {
    next: u32,
    rows: BTreeMap<u32, String>,
}

impl UserRepo for MemRepo {
    fn add(&mut self, name: &str) -> u32 {
        self.next += 1;
        self.rows.insert(self.next, name.to_string());
        self.next
    }
    fn find(&self, id: u32) -> Option<String> {
        self.rows.get(&id).cloned()
    }
}

fn register(repo: &mut impl UserRepo, name: &str) -> Result<u32, String> {
    if name.trim().is_empty() {
        return Err("empty name".to_string());
    }
    Ok(repo.add(name.trim()))
}

fn main() {
    let mut repo = MemRepo { next: 0, rows: BTreeMap::new() };
    println!("{:?} {:?}", register(&mut repo, " Ann "), register(&mut repo, "  "));
    println!("{:?} {:?}", repo.find(1), repo.find(5));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Ok(1) Err(\"empty name\")\nSome(\"Ann\") None"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Адрес подключения"}
      sub={"DATABASE_URL"}
      main={"Пароль — из окружения, а не из кода; порт по умолчанию — 5432."}
    >
      <RsCode>{`#[derive(Debug, PartialEq)]
struct DbUrl {
    user: String,
    password: String,
    host: String,
    port: u16,
    db: String,
}

fn parse_url(url: &str) -> Result<DbUrl, String> {
    let rest = url.strip_prefix("postgres://").ok_or("bad scheme")?;
    let (cred, rest) = rest.split_once('@').ok_or("missing @")?;
    let (user, password) = cred.split_once(':').unwrap_or((cred, ""));
    let (hostport, db) = rest.split_once('/').ok_or("missing database")?;
    let (host, port) = match hostport.split_once(':') {
        Some((h, p)) => (h, p.parse::<u16>().map_err(|_| "bad port")?),
        None => (hostport, 5432),
    };
    Ok(DbUrl { user: user.into(), password: password.into(), host: host.into(), port, db: db.into() })
}

fn main() {
    println!("{:?}", parse_url("postgres://app:secret@db.local:6543/shop"));
    println!("{:?}", parse_url("postgres://app@localhost/shop").map(|u| (u.port, u.password)));
    println!("{:?} {:?}", parse_url("mysql://x"), parse_url("postgres://a:b@h:xx/d"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Ok(DbUrl { user: \"app\", password: \"secret\", host: \"db.local\", port: 6543, db: \"shop\" })\nOk((5432, \"\"))\nErr(\"bad scheme\") Err(\"bad port\")"}</Cmd>
      <div className="s-note">{"С sqlx: let pool = PgPoolOptions::new().connect(&url).await?; sqlx::query_as::<_, User>(\"SELECT * FROM users WHERE id = $1\").bind(id).fetch_one(&pool).await?"}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Библиотеки работы с БД — это протокол, типы, параметры, пул, транзакции и миграции: теперь вы их понимаете."}
    >
      <div className="s-grid2">
        {([["tag · len · body", "Протокол", "Сообщения Postgres"], ["FromColumn", "Типы", "NULL → Option"], ["$1 · Select", "Запросы", "Параметры и построитель"], ["Tx · Pool · repo", "Надёжность", "RAII и тестируемость"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R43 = {
  "10:43": [
    S01,
    S02,
    S03,
    S04,
    S05,
    S06,
    S07,
    S08,
    S09,
    S10,
    S11,
    S12,
    S13,
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R43).
export const SLIDE_TITLES_R43 = {
  "10:43": [
    "Данные и PostgreSQL",
    "Строка → структура",
    "Сообщения",
    "Ответ сервера",
    "FromColumn",
    "SQL-инъекции",
    "Построитель запросов",
    "Пул соединений",
    "Транзакции",
    "Миграции",
    "Репозиторий",
    "Адрес подключения",
    "Итоги",
  ],
};
