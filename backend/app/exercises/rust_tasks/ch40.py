"""Задачи книги «Изучаем Rust»: глава 40 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {40: [{'id': 'r40-wc',
       'mode': 'rust',
       'title': 'wc: строки, слова, байты',
       'statement': 'Напишите count_stats<R: std::io::Read>(r: R) -> std::io::Result<(usize, usize, usize)>: '
                    "число строк (символов '\\n' плюс последняя строка без перевода), слов (по пробельным "
                    'символам) и байтов. Читайте буферизованно: проверка подаёт 20 МБ.',
       'starter': 'use std::io::Read;\n'
                  '\n'
                  'fn count_stats<R: Read>(r: R) -> std::io::Result<(usize, usize, usize)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'use std::io::Cursor;\n'
                 '\n'
                 'fn main() {\n'
                 '    println!("{:?}", count_stats(Cursor::new("one two\\nthree\\n\\nfour five '
                 'six")).unwrap());\n'
                 '    println!("{:?} {:?}", count_stats(Cursor::new("")).unwrap(), '
                 'count_stats(Cursor::new("\\n")).unwrap());\n'
                 '    println!("{:?}", count_stats(Cursor::new("привет мир\\n")).unwrap());\n'
                 '    let big = "lorem ipsum dolor sit amet\\n".repeat(750_000);\n'
                 '    println!("{:?}", count_stats(Cursor::new(big)).unwrap());\n'
                 '}\n',
       'expected': ['(4, 6, 28)', '(0, 0, 0) (1, 0, 1)', '(1, 2, 20)', '(750000, 3750000, 20250000)'],
       'hint': "read_until(b'\\n', &mut buf) читает строку вместе с переводом; считайте байты по числу "
               'прочитанного.'},
      {'id': 'r40-paths',
       'mode': 'rust',
       'title': 'Лексический разбор путей',
       'statement': 'Напишите без обращения к файловой системе: normalize(path: &str) -> String (как в курсе '
                    "по ОС: убрать '.', повторные '/', обработать '..', результат абсолютный; для "
                    "относительного пути '..' выше начала сохраняются) и ext_of(path: &str) -> "
                    "Option<String> (расширение без точки; None для имён без точки или вида '.bashrc').",
       'starter': 'fn normalize(path: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn ext_of(path: &str) -> Option<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for p in ["/usr/./bin/../lib//x/", "/", "/../..", "a/b/../../c", "../x/./y", "a/..", '
                 '"", "./", "../../a/../b"] {\n'
                 '        println!("{:?} -> {:?}", p, normalize(p));\n'
                 '    }\n'
                 '    for p in ["/a/report.final.txt", "Makefile", "/a/.bashrc", "archive.tar.gz", '
                 '"dir.d/file", "trailing."] {\n'
                 '        println!("{:?} {:?}", p, ext_of(p));\n'
                 '    }\n'
                 '}\n',
       'expected': ['"/usr/./bin/../lib//x/" -> "/usr/lib/x"',
                    '"/" -> "/"',
                    '"/../.." -> "/"',
                    '"a/b/../../c" -> "c"',
                    '"../x/./y" -> "../x/y"',
                    '"a/.." -> "."',
                    '"" -> "."',
                    '"./" -> "."',
                    '"../../a/../b" -> "../../b"',
                    '"/a/report.final.txt" Some("txt")',
                    '"Makefile" None',
                    '"/a/.bashrc" None',
                    '"archive.tar.gz" Some("gz")',
                    '"dir.d/file" None',
                    '"trailing." None'],
       'hint': "Стек компонентов; '..' снимает предыдущий компонент, но не другой '..'; в абсолютном пути "
               'выше корня подняться нельзя.'},
      {'id': 'r40-list-tree',
       'mode': 'rust',
       'title': 'Дерево каталогов',
       'statement': 'Напишите list_tree(root: &Path) -> io::Result<Vec<String>>: относительные пути всех '
                    "файлов и каталогов внутри root (каталоги — с '/' на конце), отсортированные по полному "
                    'пути как строке.',
       'starter': 'use std::io;\n'
                  'use std::path::Path;\n'
                  '\n'
                  'fn list_tree(root: &Path) -> io::Result<Vec<String>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn tmp_dir(name: &str) -> std::path::PathBuf {\n'
                 '    let d = std::env::temp_dir().join(format!("say13-{}-{}", name, std::process::id()));\n'
                 '    let _ = std::fs::remove_dir_all(&d);\n'
                 '    std::fs::create_dir_all(&d).unwrap();\n'
                 '    d\n'
                 '}\n'
                 'use std::fs;\n'
                 '\n'
                 'fn main() {\n'
                 '    let root = tmp_dir("tree");\n'
                 '    fs::create_dir_all(root.join("src/util")).unwrap();\n'
                 '    fs::create_dir_all(root.join("empty")).unwrap();\n'
                 '    fs::write(root.join("Cargo.toml"), "x").unwrap();\n'
                 '    fs::write(root.join("src/main.rs"), "m").unwrap();\n'
                 '    fs::write(root.join("src/util/mod.rs"), "").unwrap();\n'
                 '    println!("{:?}", list_tree(&root).unwrap());\n'
                 '    println!("{:?}", list_tree(&root.join("empty")).unwrap());\n'
                 '    println!("{:?}", list_tree(&root.join("nope")).map_err(|e| e.kind()));\n'
                 '    fs::remove_dir_all(&root).unwrap();\n'
                 '}\n',
       'expected': ['["Cargo.toml", "empty/", "src/", "src/main.rs", "src/util/", "src/util/mod.rs"]',
                    '[]',
                    'Err(NotFound)'],
       'hint': 'Рекурсия с префиксом пути; тип записи — e.file_type()?.is_dir(); в конце sort().'},
      {'id': 'r40-dir-size',
       'mode': 'rust',
       'title': 'Размер каталога',
       'statement': 'Напишите dir_size(root: &Path) -> io::Result<u64>: суммарный размер всех обычных файлов '
                    'внутри root (рекурсивно). Символические ссылки не разыменовывайте (не заходите и не '
                    'считайте).',
       'starter': 'use std::io;\n'
                  'use std::path::Path;\n'
                  '\n'
                  'fn dir_size(root: &Path) -> io::Result<u64> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn tmp_dir(name: &str) -> std::path::PathBuf {\n'
                 '    let d = std::env::temp_dir().join(format!("say13-{}-{}", name, std::process::id()));\n'
                 '    let _ = std::fs::remove_dir_all(&d);\n'
                 '    std::fs::create_dir_all(&d).unwrap();\n'
                 '    d\n'
                 '}\n'
                 'use std::fs;\n'
                 '\n'
                 'fn main() {\n'
                 '    let root = tmp_dir("size");\n'
                 '    fs::create_dir_all(root.join("a/b")).unwrap();\n'
                 '    fs::write(root.join("one"), vec![0u8; 100]).unwrap();\n'
                 '    fs::write(root.join("a/two"), vec![0u8; 2000]).unwrap();\n'
                 '    fs::write(root.join("a/b/three"), vec![1u8; 30]).unwrap();\n'
                 '    #[cfg(unix)]\n'
                 '    std::os::unix::fs::symlink(&root, root.join("a/loop")).unwrap();\n'
                 '    println!("{}", dir_size(&root).unwrap());\n'
                 '    println!("{}", dir_size(&root.join("a/b")).unwrap());\n'
                 '    println!("{:?}", dir_size(&root.join("zzz")).map_err(|e| e.kind()));\n'
                 '    fs::remove_dir_all(&root).unwrap();\n'
                 '}\n',
       'expected': ['2130', '30', 'Err(NotFound)'],
       'hint': 'e.file_type() не следует по ссылкам (в отличие от fs::metadata): is_file / is_dir у ссылки '
               'ложны.'},
      {'id': 'r40-grep-file',
       'mode': 'rust',
       'title': 'grep по файлу',
       'statement': 'Напишите grep_file(path: &Path, needle: &str) -> io::Result<Vec<(usize, String)>>: пары '
                    '(номер строки с единицы, строка), содержащие подстроку needle. Читайте построчно через '
                    'BufReader.',
       'starter': 'use std::io;\n'
                  'use std::path::Path;\n'
                  '\n'
                  'fn grep_file(path: &Path, needle: &str) -> io::Result<Vec<(usize, String)>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn tmp_dir(name: &str) -> std::path::PathBuf {\n'
                 '    let d = std::env::temp_dir().join(format!("say13-{}-{}", name, std::process::id()));\n'
                 '    let _ = std::fs::remove_dir_all(&d);\n'
                 '    std::fs::create_dir_all(&d).unwrap();\n'
                 '    d\n'
                 '}\n'
                 'use std::fs;\n'
                 '\n'
                 'fn main() {\n'
                 '    let dir = tmp_dir("grep");\n'
                 '    let f = dir.join("log.txt");\n'
                 '    fs::write(&f, "start\\nERROR disk full\\nok\\nERROR timeout\\n\\nend '
                 'ERROR").unwrap();\n'
                 '    println!("{:?}", grep_file(&f, "ERROR").unwrap());\n'
                 '    println!("{:?} {:?}", grep_file(&f, "nothing").unwrap(), grep_file(&f, '
                 '"").unwrap().len());\n'
                 '    println!("{:?}", grep_file(&dir.join("missing"), "x").map_err(|e| e.kind()));\n'
                 '    fs::remove_dir_all(&dir).unwrap();\n'
                 '}\n',
       'expected': ['[(2, "ERROR disk full"), (4, "ERROR timeout"), (6, "end ERROR")]',
                    '[] 6',
                    'Err(NotFound)'],
       'hint': 'lines() даёт Result<String>; enumerate() — номера с нуля, прибавьте единицу.'},
      {'id': 'r40-copy-filtered',
       'mode': 'rust',
       'title': 'Копирование с фильтром',
       'statement': 'Напишите copy_filtered(src: &Path, dst: &Path, keep: impl Fn(&str) -> bool) -> '
                    'io::Result<usize>: читает src построчно, записывает в dst (через BufWriter, каждая '
                    "строка заканчивается '\\n') только строки, для которых keep вернул true; возвращает "
                    'число записанных строк.',
       'starter': 'use std::io;\n'
                  'use std::path::Path;\n'
                  '\n'
                  'fn copy_filtered(src: &Path, dst: &Path, keep: impl Fn(&str) -> bool) -> '
                  'io::Result<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn tmp_dir(name: &str) -> std::path::PathBuf {\n'
                 '    let d = std::env::temp_dir().join(format!("say13-{}-{}", name, std::process::id()));\n'
                 '    let _ = std::fs::remove_dir_all(&d);\n'
                 '    std::fs::create_dir_all(&d).unwrap();\n'
                 '    d\n'
                 '}\n'
                 'use std::fs;\n'
                 '\n'
                 'fn main() {\n'
                 '    let dir = tmp_dir("copy");\n'
                 '    let (a, b) = (dir.join("in.txt"), dir.join("out.txt"));\n'
                 '    fs::write(&a, "# comment\\nkey=1\\n\\nkey=2\\n# other\\nlast").unwrap();\n'
                 "    let n = copy_filtered(&a, &b, |l| !l.is_empty() && !l.starts_with('#')).unwrap();\n"
                 '    println!("{} {:?}", n, fs::read_to_string(&b).unwrap());\n'
                 '    println!("{:?}", copy_filtered(&dir.join("none"), &b, |_| true).map_err(|e| '
                 'e.kind()));\n'
                 '    let big = dir.join("big.txt");\n'
                 '    fs::write(&big, "line\\n".repeat(300_000)).unwrap();\n'
                 '    println!("{}", copy_filtered(&big, &dir.join("big2.txt"), |_| true).unwrap());\n'
                 '    fs::remove_dir_all(&dir).unwrap();\n'
                 '}\n',
       'expected': ['3 "key=1\\nkey=2\\nlast\\n"', 'Err(NotFound)', '300000'],
       'hint': 'BufWriter сам сбросится при уничтожении, но flush() явно возвращает ошибку записи — лучше '
               'вызвать его.'},
      {'id': 'r40-run-capture',
       'mode': 'rust',
       'title': 'Запуск программы с отчётом',
       'statement': 'Напишите run_capture(cmd: &str, args: &[&str]) -> Result<(String, i32), String>: '
                    'запускает программу и возвращает (stdout без перевода строки в конце, код возврата). '
                    'Если программы нет — Err("not found: <cmd>"); если процесс убит сигналом (кода нет) — '
                    'код −1; другие ошибки запуска — Err(текст ошибки).',
       'starter': 'use std::process::Command;\n'
                  '\n'
                  'fn run_capture(cmd: &str, args: &[&str]) -> Result<(String, i32), String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", run_capture("echo", &["hi", "there"]));\n'
                 '    println!("{:?}", run_capture("sh", &["-c", "echo partial; exit 4"]));\n'
                 '    println!("{:?}", run_capture("sh", &["-c", "kill -9 $$"]));\n'
                 '    println!("{:?}", run_capture("no-such-program-xyz", &[]));\n'
                 '    println!("{:?}", run_capture("printf", &["a\\\\nb\\\\n\\\\n"]));\n'
                 '}\n',
       'expected': ['Ok(("hi there", 0))',
                    'Ok(("partial", 4))',
                    'Ok(("", -1))',
                    'Err("not found: no-such-program-xyz")',
                    'Ok(("a\\nb", 0))'],
       'hint': 'output() возвращает Err, только если процесс не удалось запустить; ненулевой код — это Ok со '
               'статусом.'},
      {'id': 'r40-sort-process',
       'mode': 'rust',
       'title': 'Сортировка внешней программой',
       'statement': 'Напишите sort_with_process(lines: &[&str]) -> io::Result<Vec<String>>: отправьте строки '
                    'на стандартный ввод программы sort, закройте ввод и верните строки её вывода.',
       'starter': 'use std::io;\n'
                  '\n'
                  'fn sort_with_process(lines: &[&str]) -> io::Result<Vec<String>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", sort_with_process(&["pear", "apple", "fig", "banana"]).unwrap());\n'
                 '    println!("{:?}", sort_with_process(&[]).unwrap());\n'
                 '    let many: Vec<String> = (0..50_000).map(|i| format!("{:06}", (i * 7919) % '
                 '50_000)).collect();\n'
                 '    let refs: Vec<&str> = many.iter().map(|s| s.as_str()).collect();\n'
                 '    let r = sort_with_process(&refs).unwrap();\n'
                 '    println!("{} {} {}", r.len(), r[0], r[r.len() - 1]);\n'
                 '}\n',
       'expected': ['["apple", "banana", "fig", "pear"]', '[]', '50000 000000 049999'],
       'hint': 'Стандартный ввод дочернего процесса нужно закрыть (уничтожить владельца) до '
               'wait_with_output.'},
      {'id': 'r40-kv-server',
       'mode': 'rust',
       'title': 'Сервер ключ-значение',
       'statement': 'Напишите handle_kv(stream: TcpStream, store: Arc<Mutex<HashMap<String, String>>>) -> '
                    "io::Result<()>: читает команды по одной в строке и отвечает строкой: 'SET k v' (v — "
                    "остаток строки, может содержать пробелы) → 'OK'; 'GET k' → значение или 'NIL'; 'DEL k' "
                    "→ 'OK' или 'NIL' (если ключа не было); 'INCR k' → новое число (отсутствующий ключ — 0, "
                    "значение не число — 'ERR'); всё остальное → 'ERR'. Заканчивайте, когда клиент закрыл "
                    'соединение.',
       'starter': 'use std::collections::HashMap;\n'
                  'use std::io;\n'
                  'use std::net::TcpStream;\n'
                  'use std::sync::{Arc, Mutex};\n'
                  '\n'
                  'fn handle_kv(stream: TcpStream, store: Arc<Mutex<HashMap<String, String>>>) -> '
                  'io::Result<()> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'use std::io::{BufRead, BufReader, Write};\n'
                 'use std::net::{TcpListener, TcpStream};\n'
                 'use std::thread;\n'
                 '\n'
                 'fn session(addr: std::net::SocketAddr, cmds: &[&str]) -> Vec<String> {\n'
                 '    let mut c = TcpStream::connect(addr).unwrap();\n'
                 '    let mut r = BufReader::new(c.try_clone().unwrap());\n'
                 '    let mut out = Vec::new();\n'
                 '    for cmd in cmds {\n'
                 '        writeln!(c, "{}", cmd).unwrap();\n'
                 '        let mut line = String::new();\n'
                 '        r.read_line(&mut line).unwrap();\n'
                 '        out.push(line.trim_end().to_string());\n'
                 '    }\n'
                 '    out\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let listener = TcpListener::bind("127.0.0.1:0").unwrap();\n'
                 '    let addr = listener.local_addr().unwrap();\n'
                 '    let store = Arc::new(Mutex::new(HashMap::new()));\n'
                 '    let st = Arc::clone(&store);\n'
                 '    let server = thread::spawn(move || {\n'
                 '        for _ in 0..2 {\n'
                 '            let (s, _) = listener.accept().unwrap();\n'
                 '            handle_kv(s, Arc::clone(&st)).unwrap();\n'
                 '        }\n'
                 '    });\n'
                 '    println!("{:?}", session(addr, &["SET greeting hello big world", "GET greeting", "GET '
                 'x", "INCR n", "INCR n", "SET s abc", "INCR s", "DEL n", "DEL n", "FOO", "SET onlykey"]));\n'
                 '    println!("{:?}", session(addr, &["GET greeting", "GET n"]));\n'
                 '    server.join().unwrap();\n'
                 '    println!("{}", store.lock().unwrap().len());\n'
                 '}\n',
       'expected': ['["OK", "hello big world", "NIL", "1", "2", "OK", "ERR", "OK", "NIL", "ERR", "ERR"]',
                    '["hello big world", "NIL"]',
                    '2'],
       'hint': 'Один Mutex на всю обработку команды — просто и корректно; клиент закрывает соединение, и '
               'lines() заканчивается.'},
      {'id': 'r40-udp-reverse',
       'mode': 'rust',
       'title': 'UDP: ответ задом наперёд',
       'statement': 'Напишите udp_reverse_once(sock: &UdpSocket) -> io::Result<usize>: принять одну '
                    'дейтаграмму (до 1024 байт), отправить обратно отправителю те же байты в обратном '
                    'порядке и вернуть длину. Если за 500 мс ничего не пришло — вернуть ошибку вида TimedOut '
                    'или WouldBlock (установите таймаут чтения на сокете).',
       'starter': 'use std::io;\n'
                  'use std::net::UdpSocket;\n'
                  '\n'
                  'fn udp_reverse_once(sock: &UdpSocket) -> io::Result<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'use std::net::UdpSocket;\n'
                 'use std::thread;\n'
                 'use std::time::Duration;\n'
                 '\n'
                 'fn main() {\n'
                 '    let server = UdpSocket::bind("127.0.0.1:0").unwrap();\n'
                 '    let addr = server.local_addr().unwrap();\n'
                 '    let h = thread::spawn(move || {\n'
                 '        let a = udp_reverse_once(&server).map_err(|e| e.kind());\n'
                 '        let b = udp_reverse_once(&server).map_err(|e| e.kind());\n'
                 '        let kind_ok = matches!(b, Err(std::io::ErrorKind::TimedOut) | '
                 'Err(std::io::ErrorKind::WouldBlock));\n'
                 '        (a, kind_ok)\n'
                 '    });\n'
                 '    let c = UdpSocket::bind("127.0.0.1:0").unwrap();\n'
                 '    c.set_read_timeout(Some(Duration::from_secs(2))).unwrap();\n'
                 '    c.send_to(b"abc123", addr).unwrap();\n'
                 '    let mut buf = [0u8; 64];\n'
                 '    let (n, _) = c.recv_from(&mut buf).unwrap();\n'
                 '    println!("{}", String::from_utf8_lossy(&buf[..n]));\n'
                 '    println!("{:?}", h.join().unwrap());\n'
                 '}\n',
       'expected': ['321cba', '(Ok(6), true)'],
       'hint': 'recv_from возвращает размер и адрес отправителя; send_to ему же.'}]}
