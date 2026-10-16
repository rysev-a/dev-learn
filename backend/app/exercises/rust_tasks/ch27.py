"""Задачи книги «Изучаем Rust»: глава 27 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {27: [{'id': 'r27-read-all',
       'mode': 'rust',
       'title': 'Прочитать всё',
       'statement': 'Напишите slurp<R: Read>(mut r: R) -> io::Result<String>: прочитать источник целиком в '
                    'строку.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn slurp<R: Read>(mut r: R) -> io::Result<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", slurp("привет".as_bytes()).unwrap());\n'
                 '    println!("{:?}", slurp(Cursor::new(Vec::<u8>::new())).unwrap());\n'
                 '    println!("{}", slurp(Cursor::new(vec![0xff, 0xfe])).is_err());\n'
                 '}\n',
       'hint': '&[u8] и Cursor реализуют Read; ошибка UTF-8 приходит как io::Error.',
       'expected': ['"привет"', '""', 'true']},
      {'id': 'r27-count-lines',
       'mode': 'rust',
       'title': 'Строки и слова',
       'statement': 'Напишите wc<R: BufRead>(r: R) -> io::Result<(usize, usize, usize)>: число строк, слов '
                    '(split_whitespace) и байтов (с символами конца строки) в потоке.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn wc<R: BufRead>(mut r: R) -> io::Result<(usize, usize, usize)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", wc(Cursor::new("раз два\\nтри\\n\\nчетыре пять шесть")).unwrap());\n'
                 '    println!("{:?}", wc(Cursor::new("")).unwrap());\n'
                 '}\n',
       'hint': 'read_line возвращает число прочитанных байтов; 0 — конец.',
       'expected': ['(4, 6, 54)', '(0, 0, 0)']},
      {'id': 'r27-sum-input',
       'mode': 'rust',
       'title': 'Сумма чисел из ввода',
       'statement': 'Напишите sum_input<R: BufRead>(r: R) -> io::Result<i64>: сумма целых по одному на '
                    'строке; пустые строки пропускать, некорректные — ошибка InvalidData.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn sum_input<R: BufRead>(r: R) -> io::Result<i64> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", sum_input(Cursor::new("1\\n2\\n\\n -3 \\n")).unwrap());\n'
                 '    let e = sum_input(Cursor::new("1\\nx\\n")).unwrap_err();\n'
                 '    println!("{:?}", e.kind());\n'
                 '}\n',
       'hint': 'io::Error::new(ErrorKind::InvalidData, e)',
       'expected': ['0', 'InvalidData']},
      {'id': 'r27-copy-upper',
       'mode': 'rust',
       'title': 'Копирование с преобразованием',
       'statement': 'Напишите shout<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()>: каждую строку '
                    'входа записать в выход в верхнем регистре с «!» на конце и переводом строки.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn shout<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut out: Vec<u8> = Vec::new();\n'
                 '    shout(Cursor::new("привет\\nrust\\n"), &mut out).unwrap();\n'
                 '    print!("{}", String::from_utf8(out).unwrap());\n'
                 '}\n',
       'hint': 'writeln!(w, …) пишет в любой Write.',
       'expected': ['ПРИВЕТ!', 'RUST!']},
      {'id': 'r27-tee',
       'mode': 'rust',
       'title': 'Двойная запись',
       'statement': 'Напишите tee<R: Read, A: Write, B: Write>(mut r: R, a: &mut A, b: &mut B) -> '
                    'io::Result<usize>: читать из r блоками по 4 байта и каждый блок писать и в a, и в b; '
                    'вернуть число байтов.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn tee<R: Read, A: Write, B: Write>(mut r: R, a: &mut A, b: &mut B) -> io::Result<usize> '
                  '{\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let (mut a, mut b) = (Vec::new(), Vec::new());\n'
                 '    let n = tee("0123456789".as_bytes(), &mut a, &mut b).unwrap();\n'
                 '    println!("{} {} {}", n, String::from_utf8(a).unwrap(), '
                 'String::from_utf8(b).unwrap());\n'
                 '}\n',
       'hint': 'read возвращает меньше байтов, чем размер буфера, — пишите buf[..n].',
       'expected': ['10 0123456789 0123456789']},
      {'id': 'r27-take',
       'mode': 'rust',
       'title': 'Ограничить чтение',
       'statement': 'Напишите head(r: impl Read, n: u64) -> io::Result<String>: первые n байтов (метод '
                    'take), как строка (lossy).',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn head(r: impl Read, n: u64) -> io::Result<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", head("hello world".as_bytes(), 5).unwrap());\n'
                 '    println!("{:?}", head("abc".as_bytes(), 10).unwrap());\n'
                 '    println!("{:?}", head("abc".as_bytes(), 0).unwrap());\n'
                 '}\n',
       'hint': 'r.take(n).read_to_end(&mut buf)',
       'expected': ['"hello"', '"abc"', '""']},
      {'id': 'r27-chain',
       'mode': 'rust',
       'title': 'Склейка потоков',
       'statement': 'Напишите joined(a: &str, b: &str) -> String: прочитайте два источника подряд через '
                    'chain как один и верните результат.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn joined(a: &str, b: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", joined("раз, ", "два"));\n'
                 '    println!("[{}]", joined("", ""));\n'
                 '}\n',
       'hint': 'Read::chain склеивает два источника.',
       'expected': ['раз, два', '[]']},
      {'id': 'r27-read-exact',
       'mode': 'rust',
       'title': 'Заголовок фиксированной длины',
       'statement': 'Напишите read_header<R: Read>(mut r: R) -> io::Result<(u16, u32)>: прочитать 6 байт — '
                    'два байта u16 и четыре байта u32 в порядке little-endian; при коротких данных вернуть '
                    'ошибку UnexpectedEof (read_exact).',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn read_header<R: Read>(mut r: R) -> io::Result<(u16, u32)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", read_header(&[1u8, 0, 2, 0, 0, 0][..]).unwrap());\n'
                 '    println!("{:?}", read_header(&[1u8, 1, 1][..]).unwrap_err().kind());\n'
                 '}\n',
       'hint': 'from_le_bytes для каждого поля.',
       'expected': ['(1, 2)', 'UnexpectedEof']},
      {'id': 'r27-write-numbers',
       'mode': 'rust',
       'title': 'Двоичная запись',
       'statement': 'Напишите write_u32s<W: Write>(w: &mut W, v: &[u32]) -> io::Result<()>: записать числа '
                    'big-endian подряд (to_be_bytes).',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn write_u32s<W: Write>(w: &mut W, v: &[u32]) -> io::Result<()> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut out = Vec::new();\n'
                 '    write_u32s(&mut out, &[1, 258, 0xDEADBEEF]).unwrap();\n'
                 '    println!("{:?}", out);\n'
                 '}\n',
       'hint': 'x.to_be_bytes() возвращает [u8; 4].',
       'expected': ['[0, 0, 0, 1, 0, 0, 1, 2, 222, 173, 190, 239]']},
      {'id': 'r27-seek-tail',
       'mode': 'rust',
       'title': 'Хвост файла',
       'statement': 'Напишите tail_bytes<R: Read + Seek>(mut r: R, n: u64) -> io::Result<Vec<u8>>: последние '
                    'n байтов (или всё, если данных меньше). Seek::seek(SeekFrom::End(…)).',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn tail_bytes<R: Read + Seek>(mut r: R, n: u64) -> io::Result<Vec<u8>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", tail_bytes(Cursor::new(b"0123456789".to_vec()), 3).unwrap());\n'
                 '    println!("{:?}", tail_bytes(Cursor::new(b"ab".to_vec()), 10).unwrap());\n'
                 '    println!("{:?}", tail_bytes(Cursor::new(Vec::new()), 4).unwrap());\n'
                 '}\n',
       'hint': 'seek(End(0)) возвращает размер.',
       'expected': ['[55, 56, 57]', '[97, 98]', '[]']},
      {'id': 'r27-seek-patch',
       'mode': 'rust',
       'title': 'Правка по смещению',
       'statement': 'Напишите patch<S: Read + Write + Seek>(mut s: S, pos: u64, data: &[u8]) -> '
                    'io::Result<Vec<u8>>: записать data с позиции pos и вернуть всё содержимое после правки.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn patch<S: Read + Write + Seek>(mut s: S, pos: u64, data: &[u8]) -> io::Result<Vec<u8>> '
                  '{\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let c = Cursor::new(b"0123456789".to_vec());\n'
                 '    println!("{:?}", String::from_utf8(patch(c, 3, b"ABC").unwrap()).unwrap());\n'
                 '}\n',
       'hint': 'Курсор над вектором реализует Read, Write и Seek сразу.',
       'expected': ['"012ABC6789"']},
      {'id': 'r27-bufwriter',
       'mode': 'rust',
       'title': 'BufWriter',
       'statement': 'Напишите write_squares<W: Write>(w: W, n: u32) -> io::Result<()>: обернув w в '
                    'BufWriter, записать квадраты чисел 1…n по одному на строке.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn write_squares<W: Write>(w: W, n: u32) -> io::Result<()> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v: Vec<u8> = Vec::new();\n'
                 '    write_squares(&mut v, 5).unwrap();\n'
                 '    print!("{}", String::from_utf8(v).unwrap());\n'
                 '    let mut big: Vec<u8> = Vec::new();\n'
                 '    write_squares(&mut big, 100000).unwrap();\n'
                 '    println!("{}", big.len());\n'
                 '}\n',
       'hint': 'BufWriter::new(w) и flush() в конце.',
       'expected': ['1', '4', '9', '16', '25', '1039834']},
      {'id': 'r27-read-until',
       'mode': 'rust',
       'title': 'read_until',
       'statement': 'Напишите records<R: BufRead>(mut r: R) -> io::Result<Vec<String>>: записи, разделённые '
                    'символом «;» (read_until); разделитель в запись не входит, пустые записи пропускаются.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn records<R: BufRead>(mut r: R) -> io::Result<Vec<String>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", records(Cursor::new("a; b ;;c")).unwrap());\n'
                 '    println!("{:?}", records(Cursor::new("")).unwrap());\n'
                 '}\n',
       'hint': 'read_until включает разделитель в буфер — уберите его.',
       'expected': ['["a", "b", "c"]', '[]']},
      {'id': 'r27-parse-grid',
       'mode': 'rust',
       'title': 'Прочитать сетку',
       'statement': 'Напишите read_grid<R: BufRead>(r: R) -> io::Result<Vec<Vec<i32>>>: первая строка — «N '
                    'M», далее N строк по M чисел через пробел. Если не хватает строк или чисел — ошибка '
                    'InvalidData.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn read_grid<R: BufRead>(r: R) -> io::Result<Vec<Vec<i32>>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", read_grid(Cursor::new("2 3\\n1 2 3\\n4 5 6\\n")).unwrap());\n'
                 '    println!("{}", read_grid(Cursor::new("2 2\\n1 2\\n")).is_err());\n'
                 '    println!("{}", read_grid(Cursor::new("1 2\\n1 x\\n")).is_err());\n'
                 '    println!("{}", read_grid(Cursor::new("")).is_err());\n'
                 '}\n',
       'hint': 'Определите замыкание bad() для создания ошибки.',
       'expected': ['[[1, 2, 3], [4, 5, 6]]', 'true', 'true', 'true']},
      {'id': 'r27-path-parts',
       'mode': 'rust',
       'title': 'Части пути',
       'statement': 'Напишите describe(p: &str) -> String: «каталог=…, имя=…, расширение=…» (parent, '
                    'file_stem, extension; отсутствующее — «-»).',
       'starter': 'fn describe(p: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", describe("/home/user/report.final.pdf"));\n'
                 '    println!("{}", describe("notes.txt"));\n'
                 '    println!("{}", describe("/etc/hosts"));\n'
                 '    println!("{}", describe("dir/.hidden"));\n'
                 '}\n',
       'hint': 'Path::new(p).parent(), file_stem(), extension() — все возвращают Option.',
       'expected': ['каталог=/home/user, имя=report.final, расширение=pdf',
                    'каталог=-, имя=notes, расширение=txt',
                    'каталог=/etc, имя=hosts, расширение=-',
                    'каталог=dir, имя=.hidden, расширение=-']},
      {'id': 'r27-path-join',
       'mode': 'rust',
       'title': 'Склейка путей',
       'statement': 'Напишите build_path(parts: &[&str]) -> String: склейте части в путь через PathBuf::push '
                    '(абсолютная часть заменяет всё предыдущее); результат — строка. Для ["/a", "b", '
                    '"c.txt"] это «/a/b/c.txt».',
       'starter': 'fn build_path(parts: &[&str]) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", build_path(&["/a", "b", "c.txt"]));\n'
                 '    println!("{}", build_path(&["a", "/b", "c"]));\n'
                 '    println!("[{}]", build_path(&[]));\n'
                 '}\n',
       'hint': 'push с абсолютным путём заменяет накопленное.',
       'expected': ['/a/b/c.txt', '/b/c', '[]']},
      {'id': 'r27-ext-change',
       'mode': 'rust',
       'title': 'Сменить расширение',
       'statement': 'Напишите to_bak(name: &str) -> String: заменить расширение на «bak» (with_extension), а '
                    'для имени без расширения — добавить.',
       'starter': 'fn to_bak(name: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", to_bak("data.csv"));\n'
                 '    println!("{}", to_bak("README"));\n'
                 '    println!("{}", to_bak("a/b/c.tar.gz"));\n'
                 '}\n',
       'hint': 'with_extension заменяет последнее расширение.',
       'expected': ['data.bak', 'README.bak', 'a/b/c.tar.bak']},
      {'id': 'r27-file-roundtrip',
       'mode': 'rust',
       'title': 'Файл: запись и чтение',
       'statement': 'Напишите roundtrip(text: &str) -> io::Result<String>: запишите text во временный файл в '
                    'каталоге std::env::temp_dir() (имя с номером процесса), прочитайте обратно, удалите '
                    'файл и верните прочитанное.',
       'starter': 'use std::io;\n\nfn roundtrip(text: &str) -> io::Result<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", roundtrip("привет\\nмир").unwrap());\n'
                 '    println!("{:?}", roundtrip("").unwrap());\n'
                 '}\n',
       'hint': 'fs::write, fs::read_to_string, fs::remove_file.',
       'expected': ['"привет\\nмир"', '""']},
      {'id': 'r27-file-append',
       'mode': 'rust',
       'title': 'Дозапись в файл',
       'statement': 'Напишите append_lines(lines: &[&str]) -> io::Result<usize>: во временный файл '
                    '(std::env::temp_dir(), имя с номером процесса) дозаписать строки по одной (OpenOptions '
                    'append) двумя разными открытиями; вернуть число строк в файле; файл удалить.',
       'starter': 'use std::io::{self, Write};\n'
                  '\n'
                  'fn append_lines(lines: &[&str]) -> io::Result<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", append_lines(&["a", "b", "c", "d", "e"]).unwrap());\n'
                 '    println!("{}", append_lines(&[]).unwrap());\n'
                 '}\n',
       'hint': 'OpenOptions::new().append(true).create(true).open(&p)',
       'expected': ['5', '0']},
      {'id': 'r27-dir-walk',
       'mode': 'rust',
       'title': 'Обход каталога',
       'statement': 'Напишите make_and_list() -> io::Result<Vec<String>>: создайте во временном каталоге '
                    '(temp_dir + имя с номером процесса) каталог с файлами c.txt, a.txt, b.log (пустые), '
                    'прочитайте его read_dir, верните имена по алфавиту и удалите каталог со всем содержимым '
                    '(remove_dir_all).',
       'starter': 'use std::io;\n\nfn make_and_list() -> io::Result<Vec<String>> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?}", make_and_list().unwrap());\n}\n',
       'hint': 'read_dir возвращает итератор io::Result<DirEntry>; порядок не определён — сортируйте.',
       'expected': ['["a.txt", "b.log", "c.txt"]']},
      {'id': 'r27-error-kind',
       'mode': 'rust',
       'title': 'Вид ошибки',
       'statement': 'Напишите open_kind(path: &str) -> String: попытайтесь открыть файл; верните «ok» при '
                    'успехе, «нет файла» для NotFound, «нет доступа» для PermissionDenied и «ошибка» для '
                    'остальных.',
       'starter': 'use std::io;\n\nfn open_kind(path: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", open_kind("/этого/файла/нет"));\n'
                 '    println!("{}", open_kind("/"));\n'
                 '}\n',
       'hint': 'e.kind() возвращает ErrorKind. Каталог можно открыть для чтения, а вот читать его нельзя.',
       'expected': ['нет файла', 'ok']},
      {'id': 'r27-custom-error',
       'mode': 'rust',
       'title': 'Свой тип ошибки',
       'statement': 'Объявите enum AppError { Io(io::Error), Parse(std::num::ParseIntError) } с '
                    'derive(Debug) и реализуйте From для обоих вариантов. Тогда функция read_num(r: impl '
                    'Read) -> Result<i32, AppError> читает строку и разбирает число одним ? на каждом шаге.',
       'starter': 'use std::io::{self, Read};\n'
                  '\n'
                  'fn read_num(mut r: impl Read) -> Result<i32, AppError> {\n'
                  '    let mut s = String::new();\n'
                  '    r.read_to_string(&mut s)?;\n'
                  '    Ok(s.trim().parse()?)\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", read_num(" 42\\n".as_bytes()).ok());\n'
                 '    println!("{}", matches!(read_num("x".as_bytes()), Err(AppError::Parse(_))));\n'
                 '    println!("{}", matches!(read_num(&[0xffu8][..]), Err(AppError::Io(_))));\n'
                 '}\n',
       'hint': 'impl From<…> for AppError — тело: AppError::Вариант(e).',
       'expected': ['Some(42)', 'true', 'true']},
      {'id': 'r27-line-numbers',
       'mode': 'rust',
       'title': 'Номера строк',
       'statement': 'Напишите number_lines<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()>: '
                    'записывать каждую строку с номером (с 1) в формате «   1: текст» (номер вправо в поле '
                    '4).',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn number_lines<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut out = Vec::new();\n'
                 '    number_lines(Cursor::new("a\\nb\\n\\nd"), &mut out).unwrap();\n'
                 '    print!("{}", String::from_utf8(out).unwrap());\n'
                 '}\n',
       'hint': 'enumerate() над lines().',
       'expected': ['   1: a', '   2: b', '   3:', '   4: d']},
      {'id': 'r27-grep',
       'mode': 'rust',
       'title': 'grep',
       'statement': 'Напишите grep<R: BufRead>(r: R, pat: &str, ignore_case: bool) -> io::Result<Vec<(usize, '
                    'String)>>: номера (с 1) и тексты строк, содержащих pat (при ignore_case — без учёта '
                    'регистра).',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn grep<R: BufRead>(r: R, pat: &str, ignore_case: bool) -> io::Result<Vec<(usize, '
                  'String)>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let t = "Rust is fast\\nrust is safe\\nGo is simple\\n";\n'
                 '    println!("{:?}", grep(Cursor::new(t), "Rust", false).unwrap());\n'
                 '    println!("{:?}", grep(Cursor::new(t), "rust", true).unwrap());\n'
                 '    println!("{:?}", grep(Cursor::new(t), "java", true).unwrap());\n'
                 '}\n',
       'hint': 'Приводите и шаблон, и строку к нижнему регистру.',
       'expected': ['[(1, "Rust is fast")]', '[(1, "Rust is fast"), (2, "rust is safe")]', '[]']},
      {'id': 'r27-csv-sum',
       'mode': 'rust',
       'title': 'Колонка CSV',
       'statement': 'Напишите column_sum<R: BufRead>(r: R, col: usize) -> io::Result<f64>: сумма чисел в '
                    'столбце col (с 0) строк вида «a,1.5,b»; первая строка — заголовок и пропускается; '
                    'пустые поля считаются нулём; нечисловое — ошибка InvalidData.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn column_sum<R: BufRead>(r: R, col: usize) -> io::Result<f64> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let t = "имя,цена,кол\\nхлеб,50.5,2\\nмолоко,,1\\nсыр,300,3\\n";\n'
                 '    println!("{:?}", column_sum(Cursor::new(t), 1).unwrap());\n'
                 '    println!("{:?}", column_sum(Cursor::new(t), 2).unwrap());\n'
                 '    println!("{}", column_sum(Cursor::new("a,b\\nx,y\\n"), 1).is_err());\n'
                 '}\n',
       'hint': "split(',').nth(col) — нужное поле.",
       'expected': ['350.5', '6.0', 'true']},
      {'id': 'r27-hexdump',
       'mode': 'rust',
       'title': 'Hex-дамп',
       'statement': 'Напишите hexdump(data: &[u8]) -> Vec<String>: строки по 8 байт «смещение(4 цифры hex): '
                    'байты через пробел» (последняя строка может быть короче): «0000: 48 65 6c …».',
       'starter': 'fn hexdump(data: &[u8]) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for l in hexdump(b"Hello, Rust language!") {\n'
                 '        println!("{}", l);\n'
                 '    }\n'
                 '    println!("{}", hexdump(&[]).len());\n'
                 '}\n',
       'hint': 'chunks(8) и enumerate; смещение — i * 8.',
       'expected': ['0000: 48 65 6c 6c 6f 2c 20 52',
                    '0008: 75 73 74 20 6c 61 6e 67',
                    '0010: 75 61 67 65 21',
                    '0']},
      {'id': 'r27-run-command',
       'mode': 'rust',
       'title': 'Запуск программы',
       'statement': 'Напишите echo_via_shell(word: &str) -> String: запустите команду «echo» с аргументом '
                    'word через std::process::Command и верните её вывод без завершающего перевода строки. '
                    '(В песочнице есть /bin/echo.)',
       'starter': 'fn echo_via_shell(word: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", echo_via_shell("привет"));\n'
                 '    println!("[{}]", echo_via_shell(""));\n'
                 '}\n',
       'hint': 'Command::new("echo").arg(word).output()',
       'expected': ['привет', '[]']},
      {'id': 'r27-stdout-bytes',
       'mode': 'rust',
       'title': 'Сколько байтов напечатано',
       'statement': 'Напишите counted(f: impl Fn(&mut dyn Write)) -> usize: вызовите f, передав ему в '
                    'качестве Write вектор байтов, и верните число записанных байтов.',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn counted(f: impl Fn(&mut dyn Write)) -> usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", counted(|w| { write!(w, "привет").unwrap(); }));\n'
                 '    println!("{}", counted(|w| { writeln!(w, "a").unwrap(); writeln!(w, "b").unwrap(); '
                 '}));\n'
                 '    println!("{}", counted(|_| {}));\n'
                 '}\n',
       'hint': '&mut Vec<u8> приводится к &mut dyn Write.',
       'expected': ['12', '4', '0']},
      {'id': 'r27-reverse-lines',
       'mode': 'rust',
       'title': 'Строки в обратном порядке',
       'statement': 'Напишите reverse_lines<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()>: '
                    'записать строки входа в обратном порядке (по одной на строку).',
       'starter': 'use std::io::{self, BufRead, BufReader, BufWriter, Cursor, Read, Seek, SeekFrom, Write};\n'
                  '\n'
                  'fn reverse_lines<R: BufRead, W: Write>(r: R, w: &mut W) -> io::Result<()> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut out = Vec::new();\n'
                 '    reverse_lines(Cursor::new("раз\\nдва\\nтри\\n"), &mut out).unwrap();\n'
                 '    print!("{}", String::from_utf8(out).unwrap());\n'
                 '}\n',
       'hint': 'lines().collect::<Result<Vec<_>, _>>()?',
       'expected': ['три', 'два', 'раз']},
      {'id': 'r27-parse-args',
       'mode': 'rust',
       'title': 'Разбор аргументов',
       'statement': 'Напишите parse_args(args: &[&str]) -> (bool, Option<String>, Vec<String>): флаг «-v» '
                    '(verbose), опция «-o <файл>» (выход) и остальные слова как позиционные аргументы; как у '
                    'простых консольных утилит.',
       'starter': 'fn parse_args(args: &[&str]) -> (bool, Option<String>, Vec<String>) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_args(&["-v", "a.txt", "-o", "out.txt", "b.txt"]));\n'
                 '    println!("{:?}", parse_args(&[]));\n'
                 '    println!("{:?}", parse_args(&["-o"]));\n'
                 '}\n',
       'hint': 'Итератор по аргументам: после «-o» берём следующий элемент.',
       'expected': ['(true, Some("out.txt"), ["a.txt", "b.txt"])',
                    '(false, None, [])',
                    '(false, None, [])']}]}
