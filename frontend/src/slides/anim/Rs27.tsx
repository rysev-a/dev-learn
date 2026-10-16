import { scene } from "./alg.tsx";
import { Box, rs } from "./rs.tsx";

/* Глава 27 книги «Изучаем Rust»: ввод-вывод и файлы. */

const pair = (a: string, b: string, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];
const row = (pre: string, items: (string|number)[], c = "g", y = 66, size = 10.5) =>
  items.map((t: string|number, i: number) =>
    Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }),
  );

// 1. Введение
export const V01 = scene({
  labels: ["Read и Write", "Один интерфейс", "io::Result"],
  caption: [
    "Источники байтов — Read, приёмники — Write",
    "Файл, сокет, stdin, срез и вектор реализуют один интерфейс — код проверяется на данных в памяти",
    "Все операции возвращают io::Result: ошибки обрабатываются, как любые другие",
  ],
  frames: [
    [...pair("Read\nисточник", "Write\nприёмник", "b", "g")],
    [...row("a", ["File", "TcpStream", "stdin", "&[u8]"], "b", 66, 9.5)],
    [
      rs(
        "c",
        20,
        50,
        [
          "fn f() -> io::Result<()> {",
          '    let s = fs::read_to_string("a")?;',
          "    Ok(())",
          "}",
        ],
        [1],
        { w: 340, size: 10, lh: 22 },
      ),
    ],
  ],
});

// 2. Read
export const V02 = scene({
  labels: ["read", "read_to_string, read_exact", "take, chain, Cursor"],
  caption: [
    "read(&mut buf) заполняет буфер и возвращает число байтов; 0 — конец потока",
    "read_to_string и read_to_end читают всё; read_exact заполняет буфер ровно",
    "take(n) ограничивает, chain склеивает; Cursor — источник с позицией над вектором; &[u8] сам Read",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["let n = r.read(&mut buf)?;", "// n == 0 → конец потока"],
        [0],
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut s = String::new();",
          "r.read_to_string(&mut s)?;",
          "r.read_exact(&mut buf4)?;",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          'let mut c = Cursor::new(b"hello".to_vec());',
          "let mut first = c.by_ref().take(2);",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
  ],
});

// 3. Write
export const V03 = scene({
  labels: ["write_all", "flush", "Vec<u8> и write!"],
  caption: [
    "write(&buf) возвращает, сколько записано; write_all повторяет, пока не отправит всё",
    "flush доводит буферизованное до приёмника; перед чтением ответа его вызывают обязательно",
    "Vec<u8> — Write: в него можно «печатать»; write! и writeln! работают с любым Write; eprintln! — в stderr",
  ],
  frames: [
    [
      rs("c", 20, 50, ['w.write_all(b"привет")?;'], [0], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
    [
      rs("c", 20, 50, ['print!("> ");', "io::stdout().flush()?;"], [1], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut buf: Vec<u8> = Vec::new();",
          'writeln!(buf, "x = {}", 5)?;',
          "let s = String::from_utf8(buf)?;",
        ],
        [1],
        { w: 340, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 4. Буферизация
export const V04 = scene({
  labels: ["Системные вызовы", "BufReader", "BufWriter"],
  caption: [
    "Каждый read и write без буфера — системный вызов; мелкие порции дороги",
    "BufReader читает крупно и отдаёт частями; BufRead: read_line, lines, read_until",
    "BufWriter копирует в буфер и пишет пачкой, при drop сбрасывает остаток; LineWriter — по строкам",
  ],
  frames: [
    [...pair("1 байт = 1 вызов", "буфер 8 КБ", "r", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          'let f = File::open("log.txt")?;',
          "for line in BufReader::new(f).lines() { }",
        ],
        [1],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut out = BufWriter::new(stdout().lock());",
          'for i in 0..1_000_000 { writeln!(out, "{}", i)?; }',
        ],
        undefined,
        { w: 340, size: 8.5, lh: 28 },
      ),
    ],
  ],
});

// 5. stdin/stdout
export const V05 = scene({
  labels: ["read_line", "lock и lines", "Быстрый вывод"],
  caption: [
    "stdin().read_line(&mut s) дописывает строку вместе с «\\n»; trim() убирает",
    "stdin().lock() даёт BufRead: for line in stdin.lock().lines() — быстрый ввод",
    "Много строк — stdout().lock() в BufWriter; приглашение без «\\n» — flush",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut s = String::new();",
          "io::stdin().read_line(&mut s)?;",
          "let n: i32 = s.trim().parse()?;",
        ],
        [1],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "for line in io::stdin().lock().lines() {",
          "    let line = line?;",
          "}",
        ],
        [0],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["let out = io::stdout();", "let mut w = BufWriter::new(out.lock());"],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
  ],
});

// 6. Файлы
export const V06 = scene({
  labels: ["Одной строкой", "OpenOptions", "Каталоги"],
  caption: [
    "fs::read_to_string, fs::write, fs::read, fs::copy, fs::rename, fs::remove_file",
    "File::open, File::create, OpenOptions::new().append(true).create(true).open(…) — тонкая настройка",
    "create_dir_all, read_dir, metadata — каталоги и сведения; файл закрывается сам по Drop",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ['let s = fs::read_to_string("a.txt")?;', 'fs::write("b.txt", s)?;'],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let f = OpenOptions::new()",
          "    .append(true).create(true)",
          '    .open("log.txt")?;',
        ],
        [1],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['fs::create_dir_all("a/b/c")?;', 'for e in fs::read_dir(".")? { }'],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
  ],
});

// 7. Пути
export const V07 = scene({
  labels: ["Path и PathBuf", "Методы", "Не всегда Unicode"],
  caption: [
    "Path — ссылка на путь, PathBuf — владеющая версия, как &str и String",
    "join, parent, file_name, file_stem, extension, with_extension, components, is_absolute, exists",
    "Имена файлов в ОС — байты, не обязательно Unicode: для печати — path.display()",
  ],
  frames: [
    [...pair("Path\n(&str)", "PathBuf\n(String)", "b", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          'let p = Path::new("/a/b.txt");',
          'p.parent()      // Some("/a")',
          'p.extension()   // Some("txt")',
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ['println!("{}", p.display());', "p.to_str()   // Option<&str>"],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
  ],
});

// 8. Ошибки
export const V08 = scene({
  labels: ["ErrorKind", "?", "Box<dyn Error>"],
  caption: [
    "io::Error несёт код ОС и вид: NotFound, PermissionDenied, AlreadyExists, UnexpectedEof, Interrupted",
    "Оператор ? пробрасывает наверх; на верхнем уровне fn main() -> Result<(), Box<dyn Error>>",
    "Box<dyn Error> принимает любую ошибку; пакет anyhow добавляет контекст; в программах для людей — понятное сообщение, а не panic",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "match File::open(p) {",
          "    Err(e) if e.kind() == ErrorKind::NotFound => { }",
          "    …",
          "}",
        ],
        [1],
        { w: 340, size: 9, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "fn main() -> Result<(), Box<dyn Error>> {",
          '    let s = fs::read_to_string("a")?;',
          "    Ok(())",
          "}",
        ],
        [0],
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ['fs::read(p).with_context(|| format!("читаю {}", p))?;'],
        undefined,
        { w: 340, size: 9, lh: 28 },
      ),
    ],
  ],
});

// 9. Seek
export const V09 = scene({
  labels: ["Seek", "SeekFrom", "Размер и sync"],
  caption: [
    "Seek: перейти на любую позицию — для таблиц смещений, баз данных, хвоста лога",
    "SeekFrom::Start(n), End(−n), Current(±n); File и Cursor реализуют Seek",
    "set_len меняет размер файла, sync_all сбрасывает данные на диск; для гигабайтов — отображение в память (memmap2)",
  ],
  frames: [
    [...cells_hint()],
    [
      rs(
        "c",
        20,
        40,
        [
          "f.seek(SeekFrom::Start(100))?;",
          "f.seek(SeekFrom::End(-10))?;",
          "f.seek(SeekFrom::Current(5))?;",
        ],
        undefined,
        { w: 340, size: 10, lh: 24 },
      ),
    ],
    [
      rs("c", 20, 50, ["f.set_len(0)?;", "f.sync_all()?;"], undefined, {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
  ],
});
function cells_hint() {
  return [0, 1, 2, 3, 4, 5].map((i) =>
    Box(`b${i}`, 50 + i * 52, 66, 46, 32, String(i * 10), i === 3 ? "y" : "b", {
      size: 11,
    }),
  );
}

// 10. Обобщённый код
export const V10 = scene({
  labels: ["R: BufRead, W: Write", "Тест на Cursor", "main"],
  caption: [
    "fn run<R: BufRead, W: Write>(input: R, output: &mut W) — работает с файлом, сокетом и памятью одинаково",
    "В тесте: Cursor на байтах и Vec<u8> на выходе — без диска и временных файлов",
    "В main подставляют stdin().lock() и stdout().lock()",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "fn run<R: BufRead, W: Write>(",
          "    input: R, out: &mut W) -> io::Result<()> { … }",
        ],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut out = Vec::new();",
          'run(Cursor::new("1\\n2\\n"), &mut out)?;',
        ],
        [1],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["run(stdin().lock(), &mut stdout().lock())?;"],
        undefined,
        { w: 340, size: 10, lh: 28 },
      ),
    ],
  ],
});

// 11. Процессы
export const V11 = scene({
  labels: ["Command::output", "spawn и pipes", "Код выхода"],
  caption: [
    'Command::new("ls").arg("-l").output() — код выхода, stdout и stderr',
    "spawn() — дочерний процесс; Stdio::piped() даёт доступ к его входу и выходу; wait() ждёт",
    "process::exit(n) или fn main() -> Result<…>: ошибка → ненулевой код и сообщение в stderr",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          'let out = Command::new("ls").arg("-l").output()?;',
          "String::from_utf8_lossy(&out.stdout)",
        ],
        [0],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          'let mut ch = Command::new("cat")',
          "    .stdin(Stdio::piped()).spawn()?;",
          "ch.wait()?;",
        ],
        [1],
        { w: 340, size: 10, lh: 24 },
      ),
    ],
    [
      rs("c", 20, 50, ["std::process::exit(2);"], undefined, {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
  ],
});

// 12. Двоичные данные
export const V12 = scene({
  labels: ["from_le_bytes", "byteorder", "serde"],
  caption: [
    "u32::from_le_bytes(buf) и from_be_bytes — порядок байтов задаёт формат",
    "Пакет byteorder: rdr.read_u32::<LittleEndian>()?; пакет bytes и кодеки — для протоколов",
    "Структуры не пишут сырыми байтами: serde с JSON, bincode, MessagePack — переносимо между платформами",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["let n = u32::from_le_bytes([2, 1, 0, 0]);   // 258"],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs("c", 20, 50, ["let n = rdr.read_u32::<LittleEndian>()?;"], [0], {
        w: 340,
        size: 10.5,
        lh: 28,
      }),
    ],
    [...pair("сырые байты\nструктуры ✕", "serde\nJSON, bincode", "r", "g")],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "Read и Write; BufReader и BufWriter; fs — одной строкой; Path и PathBuf; io::Error с видом",
    "Seek, Command, явный порядок байтов; обобщённый код проверяется на Cursor и Vec<u8>",
    "Следующая глава — время, числа и память: Duration, Instant, num, mem",
  ],
  frames: [
    [...row("a", ["Read", "Write", "BufRead", "Path"], "g")],
    [
      rs(
        "c",
        20,
        40,
        ["let s = fs::read_to_string(p)?;", "for line in s.lines() { }"],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [
      Box("a", 180, 60, 250, 34, "Duration · Instant · num · mem", "b", {
        size: 11,
      }),
    ],
  ],
});
