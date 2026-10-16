import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, RsCode } from "../widgets.tsx";
// Слайды для «Изучаем Rust», глава 41 — «HTTP по байтам».
// Тот же дизайн-код, что и в главах 1–5: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

const Slide = makeSlide("ИЗУЧАЕМ RUST / ВЕБ-СЕРВЕР / ГЛАВА 41", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Протокол из текста"}
      sub={"Глава 41 · Веб-сервер"}
      main={"HTTP — текст поверх потока байтов: его можно разобрать, собрать и проверить без библиотек."}
    >
      <div className="s-grid2">
        {[["GET / HTTP/1.1", "Запрос", "Строка, заголовки, тело"], ["Content-Length", "Тело", "Читать ровно столько"], ["200 OK", "Ответ", "Код, заголовки, байты"], ["../", "Безопасность", "Не выходить из корня"]].map(([big, t, d]) => (
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
      title={"Анатомия запроса"}
      sub={"Стартовая строка, заголовки, пустая строка"}
      main={"Конец строки — \\r\\n; пустая строка отделяет заголовки от тела."}
    >
      <RsCode>{`fn main() {
    let req = "GET /hello?name=Ann HTTP/1.1\\r\\nHost: example.org\\r\\nAccept: text/html\\r\\n\\r\\n";
    let (head, body) = req.split_once("\\r\\n\\r\\n").unwrap();
    let mut lines = head.split("\\r\\n");
    println!("{}", lines.next().unwrap());
    println!("{} headers, body {:?}", lines.count(), body);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"GET /hello?name=Ann HTTP/1.1\n2 headers, body \"\""}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Разбор заголовков"}
      sub={"Структура Request"}
      main={"Имена заголовков регистронезависимы — приводим к нижнему регистру; три части в стартовой строке — обязательно."}
    >
      <RsCode>{`use std::collections::HashMap;

#[derive(Debug)]
struct Request {
    method: String,
    path: String,
    version: String,
    headers: HashMap<String, String>,
}

fn parse_head(head: &str) -> Result<Request, String> {
    let mut lines = head.split("\\r\\n");
    let first = lines.next().ok_or("empty")?;
    let parts: Vec<&str> = first.split(' ').collect();
    if parts.len() != 3 {
        return Err(format!("bad request line: {}", first));
    }
    let mut headers = HashMap::new();
    for l in lines {
        let (k, v) = l.split_once(':').ok_or_else(|| format!("bad header: {}", l))?;
        headers.insert(k.trim().to_ascii_lowercase(), v.trim().to_string());
    }
    Ok(Request { method: parts[0].into(), path: parts[1].into(), version: parts[2].into(), headers })
}

fn main() {
    let r = parse_head("POST /items HTTP/1.1\\r\\nHost: x\\r\\nContent-Length: 5").unwrap();
    println!("{} {} {} {:?}", r.method, r.path, r.version, r.headers.get("content-length"));
    println!("{:?}", parse_head("BROKEN\\r\\n").err());
    println!("{:?}", parse_head("GET / HTTP/1.1\\r\\nnocolon").err());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"POST /items HTTP/1.1 Some(\"5\")\nSome(\"bad request line: BROKEN\")\nSome(\"bad header: nocolon\")"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Тело по Content-Length"}
      sub={"read_exact"}
      main={"Читайте ровно заявленную длину: лишнее принадлежит следующему запросу; длину ограничивайте сверху."}
    >
      <RsCode>{`use std::io::{BufRead, BufReader, Cursor, Read};

fn read_request<R: Read>(r: R) -> std::io::Result<(String, Vec<String>, Vec<u8>)> {
    let mut reader = BufReader::new(r);
    let mut first = String::new();
    reader.read_line(&mut first)?;
    let mut headers = Vec::new();
    let mut len = 0usize;
    loop {
        let mut line = String::new();
        reader.read_line(&mut line)?;
        let line = line.trim_end().to_string();
        if line.is_empty() {
            break;
        }
        if let Some((k, v)) = line.split_once(':') {
            if k.eq_ignore_ascii_case("content-length") {
                len = v.trim().parse().unwrap_or(0);
            }
        }
        headers.push(line);
    }
    let mut body = vec![0; len];
    reader.read_exact(&mut body)?;
    Ok((first.trim_end().to_string(), headers, body))
}

fn main() {
    let raw = "POST /echo HTTP/1.1\\r\\nHost: x\\r\\nContent-Length: 11\\r\\n\\r\\nhello world EXTRA";
    let (first, headers, body) = read_request(Cursor::new(raw)).unwrap();
    println!("{} | {} | {:?}", first, headers.len(), String::from_utf8(body).unwrap());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"POST /echo HTTP/1.1 | 2 | \"hello world\""}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Сборка ответа"}
      sub={"Длина — в байтах"}
      main={"Content-Length считают в байтах, не в символах: «привет» — это 12."}
    >
      <RsCode>{`fn response(status: u16, reason: &str, ctype: &str, body: &str) -> String {
    format!(
        "HTTP/1.1 {} {}\\r\\nContent-Type: {}\\r\\nContent-Length: {}\\r\\nConnection: close\\r\\n\\r\\n{}",
        status, reason, ctype, body.len(), body
    )
}

fn main() {
    let r = response(200, "OK", "text/plain; charset=utf-8", "привет");
    println!("{}", r.replace("\\r\\n", "\\\\r\\\\n\\n"));
    println!("{}", "привет".len());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"HTTP/1.1 200 OK\\r\\n\nContent-Type: text/plain; charset=utf-8\\r\\n\nContent-Length: 12\\r\\n\nConnection: close\\r\\n\n\\r\\n\nпривет\n12"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Параметры адреса"}
      sub={"Процентное кодирование"}
      main={"+ — пробел, %XX — байт; русские буквы в UTF-8 — по два байта."}
    >
      <RsCode>{`use std::collections::BTreeMap;

fn percent_decode(s: &str) -> String {
    let b = s.as_bytes();
    let mut out = Vec::new();
    let mut i = 0;
    while i < b.len() {
        match b[i] {
            b'+' => {
                out.push(b' ');
                i += 1;
            }
            b'%' => match s.get(i + 1..i + 3).and_then(|h| u8::from_str_radix(h, 16).ok()) {
                Some(v) => {
                    out.push(v);
                    i += 3;
                }
                None => {
                    out.push(b'%');
                    i += 1;
                }
            },
            c => {
                out.push(c);
                i += 1;
            }
        }
    }
    String::from_utf8_lossy(&out).into_owned()
}

fn parse_query(q: &str) -> BTreeMap<String, String> {
    q.split('&')
        .filter(|p| !p.is_empty())
        .map(|p| {
            let (k, v) = p.split_once('=').unwrap_or((p, ""));
            (percent_decode(k), percent_decode(v))
        })
        .collect()
}

fn main() {
    println!("{:?}", parse_query("name=Ann+Lee&city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&flag&x=%zz"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{\"city\": \"Москва\", \"flag\": \"\", \"name\": \"Ann Lee\", \"x\": \"%zz\"}"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Методы и статусы"}
      sub={"Перечисления вместо строк"}
      main={"Приведение варианта к числу даёт код; неизвестный метод — None → ответ 405."}
    >
      <RsCode>{`#[derive(Debug, PartialEq, Clone, Copy)]
enum Method {
    Get,
    Post,
    Put,
    Delete,
}

impl Method {
    fn parse(s: &str) -> Option<Method> {
        match s {
            "GET" => Some(Method::Get),
            "POST" => Some(Method::Post),
            "PUT" => Some(Method::Put),
            "DELETE" => Some(Method::Delete),
            _ => None,
        }
    }
}

#[derive(Clone, Copy)]
enum Status {
    Ok = 200,
    Created = 201,
    BadRequest = 400,
    NotFound = 404,
    MethodNotAllowed = 405,
    Internal = 500,
}

impl Status {
    fn reason(self) -> &'static str {
        match self {
            Status::Ok => "OK",
            Status::Created => "Created",
            Status::BadRequest => "Bad Request",
            Status::NotFound => "Not Found",
            Status::MethodNotAllowed => "Method Not Allowed",
            Status::Internal => "Internal Server Error",
        }
    }
    fn line(self) -> String {
        format!("HTTP/1.1 {} {}", self as u16, self.reason())
    }
}

fn main() {
    println!("{:?} {:?}", Method::parse("PUT"), Method::parse("PATCH"));
    println!("{} | {}", Status::NotFound.line(), Status::Created.line());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Some(Put) None\nHTTP/1.1 404 Not Found | HTTP/1.1 201 Created"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Первый сервер"}
      sub={"Клиент и сервер в одной программе"}
      main={"Тот же обмен, что у браузера и сервера, — в одном процессе и под тестом."}
    >
      <RsCode>{`use std::io::{BufRead, BufReader, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

fn handle(mut s: TcpStream) {
    let mut first = String::new();
    BufReader::new(s.try_clone().unwrap()).read_line(&mut first).unwrap();
    let path = first.split(' ').nth(1).unwrap_or("/");
    let (status, body) = if path == "/" { ("200 OK", "home") } else { ("404 Not Found", "nope") };
    write!(s, "HTTP/1.1 {}\\r\\nContent-Length: {}\\r\\nConnection: close\\r\\n\\r\\n{}", status, body.len(), body).unwrap();
}

fn get(addr: std::net::SocketAddr, path: &str) -> String {
    let mut c = TcpStream::connect(addr).unwrap();
    c.write_all(format!("GET {} HTTP/1.1\\r\\nHost: x\\r\\n\\r\\n", path).as_bytes()).unwrap();
    let mut out = String::new();
    c.read_to_string(&mut out).unwrap();
    out
}

fn main() {
    let l = TcpListener::bind("127.0.0.1:0").unwrap();
    let addr = l.local_addr().unwrap();
    let srv = thread::spawn(move || {
        for s in l.incoming().take(2) {
            handle(s.unwrap());
        }
    });
    for p in ["/", "/zzz"] {
        let r = get(addr, p);
        let (head, body) = r.split_once("\\r\\n\\r\\n").unwrap();
        println!("{} | {}", head.lines().next().unwrap(), body);
    }
    srv.join().unwrap();
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"HTTP/1.1 200 OK | home\nHTTP/1.1 404 Not Found | nope"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Данные приходят кусками"}
      sub={"Накопление до \\r\\n\\r\\n"}
      main={"Накапливайте байты и ищите конец заголовков после каждой порции; ставьте предел размера."}
    >
      <RsCode>{`use std::io::Read;

struct Trickle<'a> {
    data: &'a [u8],
    pos: usize,
}

impl<'a> Read for Trickle<'a> {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        let n = 3.min(buf.len()).min(self.data.len() - self.pos);
        buf[..n].copy_from_slice(&self.data[self.pos..self.pos + n]);
        self.pos += n;
        Ok(n)
    }
}

fn read_head<R: Read>(r: &mut R) -> Option<String> {
    let mut acc = Vec::new();
    let mut chunk = [0u8; 8];
    loop {
        let n = r.read(&mut chunk).ok()?;
        if n == 0 {
            return None;
        }
        acc.extend_from_slice(&chunk[..n]);
        if let Some(i) = acc.windows(4).position(|w| w == b"\\r\\n\\r\\n") {
            return Some(String::from_utf8_lossy(&acc[..i]).into_owned());
        }
        if acc.len() > 8192 {
            return None;
        }
    }
}

fn main() {
    let raw = b"GET /a HTTP/1.1\\r\\nHost: h\\r\\n\\r\\nBODY";
    let mut t = Trickle { data: raw, pos: 0 };
    println!("{:?}", read_head(&mut t));
    let mut cut = Trickle { data: b"GET /a HTTP/1.1\\r\\nHo", pos: 0 };
    println!("{:?}", read_head(&mut cut));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Some(\"GET /a HTTP/1.1\\r\\nHost: h\")\nNone"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"JSON вручную"}
      sub={"Экранирование и объекты"}
      main={"Строки экранируют, числа и bool пишут как есть; в реальном проекте берут проверенную библиотеку."}
    >
      <RsCode>{`fn json_escape(s: &str) -> String {
    let mut out = String::from("\\"");
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\\\\""),
            '\\\\' => out.push_str("\\\\\\\\"),
            '\\n' => out.push_str("\\\\n"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
    out
}

fn json_object(pairs: &[(&str, String)]) -> String {
    let body: Vec<String> = pairs.iter().map(|(k, v)| format!("{}:{}", json_escape(k), v)).collect();
    format!("{{{}}}", body.join(","))
}

fn main() {
    let o = json_object(&[("name", json_escape("Ann \\"A\\"\\nLee")), ("age", 31.to_string()), ("ok", true.to_string())]);
    println!("{}", o);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{\"name\":\"Ann \\\"A\\\"\\nLee\",\"age\":31,\"ok\":true}"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Файлы и безопасность пути"}
      sub={"Защита от ../"}
      main={"Допускаем только обычные компоненты пути; любой «..» или корень — отказ целиком."}
    >
      <RsCode>{`use std::path::{Component, Path, PathBuf};

fn safe_join(root: &Path, url_path: &str) -> Option<PathBuf> {
    let mut out = root.to_path_buf();
    for c in Path::new(url_path.trim_start_matches('/')).components() {
        match c {
            Component::Normal(p) => out.push(p),
            Component::CurDir => {}
            _ => return None,
        }
    }
    Some(out)
}

fn mime(path: &str) -> &'static str {
    match path.rsplit('.').next() {
        Some("html") => "text/html",
        Some("css") => "text/css",
        Some("js") => "text/javascript",
        Some("png") => "image/png",
        Some("json") => "application/json",
        _ => "application/octet-stream",
    }
}

fn main() {
    let root = Path::new("/srv/www");
    for p in ["/index.html", "/a/./b.css", "/../etc/passwd", "/a/../../x"] {
        println!("{} -> {:?}", p, safe_join(root, p));
    }
    println!("{} {} {}", mime("app.js"), mime("logo.png"), mime("README"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"/index.html -> Some(\"/srv/www/index.html\")\n/a/./b.css -> Some(\"/srv/www/a/b.css\")\n/../etc/passwd -> None\n/a/../../x -> None\ntext/javascript image/png application/octet-stream"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Ошибки — в коды ответа"}
      sub={"Перечисление ошибок"}
      main={"Одна точка преобразования «ошибка → статус»; детали — в журнал, клиенту — только код."}
    >
      <RsCode>{`#[derive(Debug)]
enum HttpError {
    BadRequest(String),
    NotFound,
    MethodNotAllowed,
    TooLarge,
}

impl HttpError {
    fn status(&self) -> u16 {
        match self {
            HttpError::BadRequest(_) => 400,
            HttpError::NotFound => 404,
            HttpError::MethodNotAllowed => 405,
            HttpError::TooLarge => 413,
        }
    }
}

fn check(method: &str, path: &str, len: usize) -> Result<&'static str, HttpError> {
    if len > 1024 {
        return Err(HttpError::TooLarge);
    }
    if !path.starts_with('/') {
        return Err(HttpError::BadRequest(format!("bad path {}", path)));
    }
    match (method, path) {
        ("GET", "/") => Ok("home"),
        ("GET", _) => Err(HttpError::NotFound),
        ("POST", "/") => Ok("posted"),
        _ => Err(HttpError::MethodNotAllowed),
    }
}

fn main() {
    for (m, p, n) in [("GET", "/", 0), ("GET", "/x", 0), ("DELETE", "/", 0), ("POST", "/", 5000), ("GET", "x", 0)] {
        match check(m, p, n) {
            Ok(b) => println!("200 {}", b),
            Err(e) => println!("{} {:?}", e.status(), e),
        }
    }
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"200 home\n404 NotFound\n405 MethodNotAllowed\n413 TooLarge\n400 BadRequest(\"bad path x\")"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"HTTP-сервер из std: аккуратный разбор, ограничения, перечисления и безопасные пути."}
    >
      <div className="s-grid2">
        {[["split_once", "Разбор", "Заголовки и стартовая строка"], ["read_exact", "Тело", "Ровно N байт, с пределом"], ["enum Status", "Типы", "Методы, статусы, ошибки"], ["safe_join", "Безопасность", "Без выхода из корня"]].map(([big, t, d]) => (
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
export const SLIDES_R41 = {
  "10:41": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R41).
export const SLIDE_TITLES_R41 = {
  "10:41": [
    "HTTP по байтам",
    "Анатомия",
    "Разбор запроса",
    "Тело запроса",
    "Ответ",
    "Query-параметры",
    "Методы и статусы",
    "Минимальный сервер",
    "Частичные чтения",
    "JSON",
    "Статические файлы",
    "Ошибки и коды",
    "Итоги",
  ],
};
