// Слайды для «Изучаем Rust», глава 40 — «Файлы, процессы и сокеты».
// Тот же дизайн-код, что и в главах 1–5: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

const RS_KW = new Set([
  "fn", "let", "mut", "pub", "struct", "enum", "impl", "match", "if", "else",
  "for", "while", "loop", "return", "use", "mod", "crate", "self", "Self",
  "move", "ref", "const", "static", "type", "where", "async", "await",
  "unsafe", "trait", "dyn", "in", "as", "break", "continue",
]);
const RS_TY = new Set([
  "i8", "i16", "i32", "i64", "i128", "isize", "u8", "u16", "u32", "u64",
  "u128", "usize", "f32", "f64", "bool", "char", "str", "String", "Vec",
  "Option", "Result", "Box", "Rc", "Arc", "RefCell", "HashMap",
]);

// Крошечный токенизатор Rust: комментарии, строки, времена жизни, ключевые
// слова, типы, макросы, числа, вызовы функций. Достаточно для слайдов.
function rsSpan(src) {
  const out = [];
  const re =
    /(\/\/[^\n]*)|("(?:[^"\\]|\\.)*")|('(\w+)\b)|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*!)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, life, num, mac, word] = m;
    if (com) out.push(<span key={out.length} className="rs-com">{tok}</span>);
    else if (str) out.push(<span key={out.length} className="rs-str">{tok}</span>);
    else if (life) out.push(<span key={out.length} className="rs-life">{tok}</span>);
    else if (num) out.push(<span key={out.length} className="rs-num">{tok}</span>);
    else if (mac) out.push(<span key={out.length} className="rs-mac">{tok}</span>);
    else if (word) {
      let cls = "";
      if (RS_KW.has(word)) cls = "rs-kw";
      else if (RS_TY.has(word)) cls = "rs-ty";
      else if (/^[A-Z]/.test(word)) cls = "rs-ty";
      else if (src[re.lastIndex] === "(") cls = "rs-fn";
      out.push(
        cls ? (
          <span key={out.length} className={cls}>{word}</span>
        ) : (
          <span key={out.length}>{word}</span>
        ),
      );
    } else out.push(<span key={out.length}>{tok}</span>);
  }
  return out;
}

function PyCode({ children }) {
  return <pre className="rs-code">{rsSpan(children)}</pre>;
}

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / ПРИМЕНЯЕМ: ОПЕРАЦИОННЫЕ СИСТЕМЫ / ГЛАВА 40</span>
      <span>{String(n).padStart(2, "0")} / 13</span>
    </div>
  );
}

function Slide({ n, title, sub, main, children }) {
  return (
    <div className="slide">
      <Rubric n={n} />
      <h3 className="s-title">{title}</h3>
      {sub && <p className="s-sub">{sub}</p>}
      <div className="s-divider" />
      <div className="s-body">{children}</div>
      {main && (
        <div className="s-main">
          <span className="s-main-label">ГЛАВНОЕ</span>
          <span className="s-main-text">{main}</span>
        </div>
      )}
    </div>
  );
}

function Node({ mono, title, sub, kind }) {
  return (
    <div className={`s-node ${kind || ""}`}>
      <span className={mono ? "s-node-mono" : "s-node-title"}>{title}</span>
      {sub && <span className="s-node-sub">{sub}</span>}
    </div>
  );
}

function Cmd({ children }) {
  return (
    <div className="s-cmd">
      <pre>{children}</pre>
    </div>
  );
}

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Rust и операционная система"}
      sub={"Глава 40 · Применяем: ОС"}
      main={"Файлы, процессы и сокеты — типы стандартной библиотеки, а идеи — те же, что в курсе по ОС."}
    >
      <div className="s-grid2">
        {[["fs · io::Read/Write", "Файлы", "Потоки и буферы"], ["Path · PathBuf", "Пути", "Отдельные типы"], ["Command", "Процессы", "Аргументы списком, коды возврата"], ["TcpListener · UdpSocket", "Сеть", "Только std, loopback"]].map(([big, t, d]) => (
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
      title={"Файлы"}
      sub={"fs::write, read_to_string, metadata"}
      main={"Короткие функции — тонкие обёртки над системными вызовами; каждая возвращает Result."}
    >
      <PyCode>{`use std::fs;

fn main() -> std::io::Result<()> {
    let dir = std::env::temp_dir().join(format!("say13-a-{}", std::process::id()));
    fs::create_dir_all(&dir)?;
    let file = dir.join("notes.txt");
    fs::write(&file, "first\\nsecond\\n")?;
    let text = fs::read_to_string(&file)?;
    println!("{:?} {}", text, fs::metadata(&file)?.len());
    println!("{} {}", file.exists(), dir.join("nope").exists());
    fs::remove_dir_all(&dir)?;
    Ok(())
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"\"first\\nsecond\\n\" 13\ntrue false"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Read, Write и буферы"}
      sub={"Cursor, BufReader, BufWriter"}
      main={"Файл, сокет и буфер в памяти — один интерфейс; буфер сокращает число системных вызовов."}
    >
      <PyCode>{`use std::io::{BufRead, BufReader, BufWriter, Cursor, Read, Write};

fn main() -> std::io::Result<()> {
    let data = "alpha\\nbeta\\n\\ngamma";
    let reader = BufReader::new(Cursor::new(data));
    let lines: Vec<String> = reader.lines().collect::<Result<_, _>>()?;
    println!("{:?}", lines);
    let mut buf = Vec::new();
    {
        let mut w = BufWriter::new(&mut buf);
        write!(w, "{}-{}", 1, 2)?;
        writeln!(w, "!")?;
        w.flush()?;
    }
    println!("{:?}", String::from_utf8(buf).unwrap());
    let mut s = String::new();
    Cursor::new("xyz").take(2).read_to_string(&mut s)?;
    println!("{}", s);
    Ok(())
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[\"alpha\", \"beta\", \"\", \"gamma\"]\n\"1-2!\\n\"\nxy"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Пути"}
      sub={"Path и PathBuf"}
      main={"Путь — не строка: имя, расширение, родитель и компоненты — методами."}
    >
      <PyCode>{`use std::path::{Path, PathBuf};

fn main() {
    let p = Path::new("/home/ann/docs/report.final.txt");
    println!("{:?} {:?} {:?}", p.file_name().unwrap(), p.extension().unwrap(), p.file_stem().unwrap());
    println!("{:?}", p.parent().unwrap());
    let mut b = PathBuf::from("/srv");
    b.push("app");
    b.push("config.toml");
    b.set_extension("json");
    println!("{}", b.display());
    println!("{}", p.components().count());
    println!("{} {}", p.starts_with("/home"), Path::new("a/b").join("../c").display());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"\"report.final.txt\" \"txt\" \"report.final\"\n\"/home/ann/docs\"\n/srv/app/config.json\n5\ntrue a/b/../c"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Обход каталога"}
      sub={"read_dir + сортировка"}
      main={"Порядок записей зависит от файловой системы — сортируйте для воспроизводимости."}
    >
      <PyCode>{`use std::fs;
use std::path::Path;

fn walk(dir: &Path, depth: usize, out: &mut Vec<String>) -> std::io::Result<()> {
    let mut entries: Vec<_> = fs::read_dir(dir)?.collect::<Result<_, _>>()?;
    entries.sort_by_key(|e| e.file_name());
    for e in entries {
        let name = e.file_name().to_string_lossy().to_string();
        let is_dir = e.file_type()?.is_dir();
        out.push(format!("{}{}{}", "  ".repeat(depth), name, if is_dir { "/" } else { "" }));
        if is_dir {
            walk(&e.path(), depth + 1, out)?;
        }
    }
    Ok(())
}

fn main() -> std::io::Result<()> {
    let root = std::env::temp_dir().join(format!("say13-b-{}", std::process::id()));
    fs::create_dir_all(root.join("src/util"))?;
    fs::write(root.join("Cargo.toml"), "x")?;
    fs::write(root.join("src/main.rs"), "fn main() {}")?;
    fs::write(root.join("src/util/mod.rs"), "")?;
    let mut out = Vec::new();
    walk(&root, 0, &mut out)?;
    println!("{}", out.join("\\n"));
    fs::remove_dir_all(&root)
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Cargo.toml\nsrc/\n  main.rs\n  util/\n    mod.rs"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Виды ошибок ввода-вывода"}
      sub={"ErrorKind"}
      main={"Сопоставляйте вид ошибки — и пишите понятное сообщение вместо номера errno."}
    >
      <PyCode>{`use std::fs::File;
use std::io::{self, ErrorKind, Read};

fn read_config(path: &str) -> Result<String, String> {
    let mut f = File::open(path).map_err(|e| match e.kind() {
        ErrorKind::NotFound => format!("{}: no such file", path),
        ErrorKind::PermissionDenied => format!("{}: permission denied", path),
        _ => format!("{}: {}", path, e),
    })?;
    let mut s = String::new();
    f.read_to_string(&mut s).map_err(|e: io::Error| e.to_string())?;
    Ok(s)
}

fn main() {
    println!("{:?}", read_config("/definitely/not/here.conf"));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Err(\"/definitely/not/here.conf: no such file\")"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Окружение и коды выхода"}
      sub={"env::var, args, exit"}
      main={"0 — успех, остальное — ошибка: так работают условные команды шелла и CI."}
    >
      <PyCode>{`use std::env;

fn main() {
    println!("{:?}", env::var("SAY_NOT_SET_VAR"));
    let args: Vec<String> = env::args().collect();
    println!("{}", args.len());
    println!("{}", env::var("SAY_NOT_SET_VAR").unwrap_or_else(|_| "default".to_string()));
    let code = if args.len() > 1 { 2 } else { 0 };
    println!("exit with {}", code);
    std::process::exit(code);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Err(NotPresent)\n1\ndefault\nexit with 0"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Запуск программ"}
      sub={"Command: output, status"}
      main={"Аргументы — списком, а не строкой для шелла; stdout и stderr раздельно; код возврата из status."}
    >
      <PyCode>{`use std::process::Command;

fn main() {
    let out = Command::new("echo").arg("hello").arg("world").output().unwrap();
    println!("{:?} {}", String::from_utf8_lossy(&out.stdout), out.status.success());
    let st = Command::new("sh").args(["-c", "exit 3"]).status().unwrap();
    println!("{:?}", st.code());
    let e = Command::new("definitely-not-a-program").output();
    println!("{:?}", e.map_err(|e| e.kind()));
    let sh = Command::new("sh").args(["-c", "echo err >&2; echo out"]).output().unwrap();
    println!("{:?} {:?}", String::from_utf8_lossy(&sh.stdout), String::from_utf8_lossy(&sh.stderr));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"\"hello world\\n\" true\nSome(3)\nErr(NotFound)\n\"out\\n\" \"err\\n\""}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Каналы между процессами"}
      sub={"Stdio::piped"}
      main={"Закрытие входа сообщает программе «данных больше нет» — иначе она ждёт вечно."}
    >
      <PyCode>{`use std::io::Write;
use std::process::{Command, Stdio};

fn main() {
    let mut child = Command::new("sort")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    child.stdin.take().unwrap().write_all(b"pear\\napple\\nfig\\n").unwrap();
    let out = child.wait_with_output().unwrap();
    println!("{:?}", String::from_utf8_lossy(&out.stdout));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"\"apple\\nfig\\npear\\n\""}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"TCP: сервер-эхо"}
      sub={"bind, accept, connect"}
      main={"Порт 0 — любой свободный; сервер в отдельном потоке, клиент читает до закрытия."}
    >
      <PyCode>{`use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?;
    let addr = listener.local_addr()?;
    let server = thread::spawn(move || {
        let (mut s, _) = listener.accept().unwrap();
        let mut buf = [0u8; 64];
        let n = s.read(&mut buf).unwrap();
        s.write_all(&buf[..n].to_ascii_uppercase()).unwrap();
    });
    let mut c = TcpStream::connect(addr)?;
    c.write_all(b"hello tcp")?;
    let mut reply = String::new();
    c.read_to_string(&mut reply)?;
    println!("{}", reply);
    server.join().unwrap();
    Ok(())
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"HELLO TCP"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Протокол поверх TCP"}
      sub={"Одна команда — одна строка"}
      main={"TCP — поток байтов без границ сообщений: протоколу нужны свои (здесь — перевод строки)."}
    >
      <PyCode>{`use std::collections::HashMap;
use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

fn handle(stream: TcpStream) {
    let mut store: HashMap<String, String> = HashMap::new();
    let mut out = stream.try_clone().unwrap();
    for line in BufReader::new(stream).lines() {
        let line = line.unwrap();
        let parts: Vec<&str> = line.splitn(3, ' ').collect();
        let reply = match parts.as_slice() {
            ["SET", k, v] => {
                store.insert(k.to_string(), v.to_string());
                "OK".to_string()
            }
            ["GET", k] => store.get(*k).cloned().unwrap_or_else(|| "NIL".to_string()),
            _ => "ERR".to_string(),
        };
        writeln!(out, "{}", reply).unwrap();
    }
}

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0")?;
    let addr = listener.local_addr()?;
    let srv = thread::spawn(move || handle(listener.accept().unwrap().0));
    let mut c = TcpStream::connect(addr)?;
    let mut r = BufReader::new(c.try_clone()?);
    for cmd in ["SET lang rust", "GET lang", "GET x", "BAD"] {
        writeln!(c, "{}", cmd)?;
        let mut line = String::new();
        r.read_line(&mut line)?;
        println!("{} -> {}", cmd, line.trim_end());
    }
    drop(c);
    drop(r);
    srv.join().unwrap();
    Ok(())
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"SET lang rust -> OK\nGET lang -> rust\nGET x -> NIL\nBAD -> ERR"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"UDP и таймауты"}
      sub={"Дейтаграммы без соединения"}
      main={"Любое сетевое ожидание ограничивайте таймаутом — иначе зависший сосед повесит вашу программу."}
    >
      <PyCode>{`use std::net::UdpSocket;
use std::time::Duration;

fn main() -> std::io::Result<()> {
    let server = UdpSocket::bind("127.0.0.1:0")?;
    let client = UdpSocket::bind("127.0.0.1:0")?;
    client.send_to(b"ping", server.local_addr()?)?;
    let mut buf = [0u8; 16];
    let (n, from) = server.recv_from(&mut buf)?;
    println!("{} {}", String::from_utf8_lossy(&buf[..n]), from == client.local_addr()?);
    client.set_read_timeout(Some(Duration::from_millis(50)))?;
    let err = client.recv_from(&mut buf).unwrap_err();
    println!("{}", matches!(err.kind(), std::io::ErrorKind::WouldBlock | std::io::ErrorKind::TimedOut));
    Ok(())
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"ping true\ntrue"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Ввод-вывод в Rust — это Result, трейты Read/Write и явные виды ошибок."}
    >
      <div className="s-grid2">
        {[["Result<_, io::Error>", "Файлы", "kind() вместо errno"], ["Command", "Процессы", "Статус и каналы"], ["TcpStream", "Сокеты", "Протокол на строках"], ["timeout", "Надёжность", "Всегда ограничивайте ожидание"]].map(([big, t, d]) => (
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
export const SLIDES_R40 = {
  "10:40": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R40).
export const SLIDE_TITLES_R40 = {
  "10:40": [
    "Rust и ОС",
    "Файлы",
    "Read и Write",
    "Пути",
    "Обход каталога",
    "ErrorKind",
    "Окружение",
    "Command",
    "Каналы процессов",
    "TCP-эхо",
    "Строчный протокол",
    "UDP и таймауты",
    "Итоги",
  ],
};
