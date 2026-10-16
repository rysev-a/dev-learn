"""Задачи книги «Изучаем Rust»: глава 41 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {41: [{'id': 'r41-parse-request',
       'mode': 'rust',
       'title': 'Разбор HTTP-запроса целиком',
       'statement': 'Напишите parse_request(raw: &str) -> Result<Request, String> (структура Request дана): '
                    'стартовая строка (3 части, иначе Err("bad request line")), заголовки (ключ → значение; '
                    'имена в нижнем регистре, значения без пробелов по краям; строка без \':\' — Err("bad '
                    'header")), параметры из query после \'?\' (без декодирования: пары \'a=b\', без \'=\' — '
                    'значение пустое), тело — всё после пустой строки; Content-Length должен быть числом '
                    '(иначе Err("bad content-length")) и не больше длины тела в байтах (иначе '
                    'Err("incomplete body")); тело обрезается до этой длины.',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'struct Request {\n'
                  '    method: String,\n'
                  '    path: String,\n'
                  '    query: BTreeMap<String, String>,\n'
                  '    headers: BTreeMap<String, String>,\n'
                  '    body: String,\n'
                  '}\n'
                  '\n'
                  'fn parse_request(raw: &str) -> Result<Request, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let r = parse_request("POST /items?id=7&flag&x= HTTP/1.1\\r\\nHost: '
                 'Example\\r\\nContent-Length: 5\\r\\n\\r\\nhello EXTRA").unwrap();\n'
                 '    println!("{} {} {:?} {:?} {:?}", r.method, r.path, r.query, r.headers, r.body);\n'
                 '    println!("{:?}", parse_request("GET / HTTP/1.1\\r\\n\\r\\n").map(|r| (r.path, '
                 'r.body)));\n'
                 '    for raw in ["GET /\\r\\n\\r\\n", "GET / HTTP/1.1\\r\\nbroken\\r\\n\\r\\n", "POST / '
                 'HTTP/1.1\\r\\nContent-Length: x\\r\\n\\r\\n", "POST / HTTP/1.1\\r\\nContent-Length: '
                 '9\\r\\n\\r\\nshort", ""] {\n'
                 '        println!("{:?}", parse_request(raw).err());\n'
                 '    }\n'
                 '}\n',
       'expected': ['POST /items {"flag": "", "id": "7", "x": ""} {"content-length": "5", "host": "Example"} '
                    '"hello"',
                    'Ok(("/", ""))',
                    'Some("bad request line")',
                    'Some("bad header")',
                    'Some("bad content-length")',
                    'Some("incomplete body")',
                    'Some("bad request line")'],
       'hint': 'Начните с split_once("\\r\\n\\r\\n"); проверки делайте в порядке: стартовая строка, '
               'заголовки, длина тела.'},
      {'id': 'r41-percent',
       'mode': 'rust',
       'title': 'Процентное кодирование',
       'statement': 'Напишите percent_encode(s: &str) -> String: байты A–Z a–z 0–9 - _ . ~ остаются, '
                    'остальные байты UTF-8 заменяются на %XX (заглавные цифры); и percent_decode(s: &str) -> '
                    "String: '+' → пробел, %XX → байт; некорректная последовательность (нет двух "
                    'шестнадцатеричных цифр) остаётся как есть; итог собирается из байтов с заменой '
                    'недопустимых UTF-8 последовательностей (from_utf8_lossy).',
       'starter': 'fn percent_encode(s: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn percent_decode(s: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["hello world", "a/b?c=d&e", "Москва", "safe-_.~", "100%", ""] {\n'
                 '        let e = percent_encode(s);\n'
                 '        println!("{:?} -> {} -> {}", s, e, percent_decode(&e) == s);\n'
                 '    }\n'
                 '    println!("{:?} {:?} {:?}", percent_decode("a+b%20c"), percent_decode("%zz%4"), '
                 'percent_decode("%D0%9F"));\n'
                 '}\n',
       'expected': ['"hello world" -> hello%20world -> true',
                    '"a/b?c=d&e" -> a%2Fb%3Fc%3Dd%26e -> true',
                    '"Москва" -> %D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0 -> true',
                    '"safe-_.~" -> safe-_.~ -> true',
                    '"100%" -> 100%25 -> true',
                    '"" ->  -> true',
                    '"a b c" "%zz%4" "П"'],
       'hint': 'Кодируйте по байтам (s.as_bytes()), формат {:02X}; при декодировании накапливайте Vec<u8> и '
               'только в конце превращайте в строку.'},
      {'id': 'r41-build-response',
       'mode': 'rust',
       'title': 'Сборка ответа',
       'statement': 'Напишите build_response(status: u16, headers: &[(&str, &str)], body: &[u8]) -> Vec<u8>: '
                    "стартовая строка 'HTTP/1.1 КОД ПОЯСНЕНИЕ' (пояснения: 200 OK, 201 Created, 204 No "
                    'Content, 400 Bad Request, 404 Not Found, 405 Method Not Allowed, 413 Payload Too Large, '
                    "500 Internal Server Error; для прочих кодов — 'Unknown'), переданные заголовки в "
                    "порядке, затем автоматически 'Content-Length: N' (N — байты тела) и 'Connection: "
                    "close', пустая строка и тело. Концы строк — \\r\\n.",
       'starter': 'fn build_response(status: u16, headers: &[(&str, &str)], body: &[u8]) -> Vec<u8> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn show(b: &[u8]) -> String {\n'
                 '    String::from_utf8_lossy(b).replace("\\r\\n", "|")\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    println!("{}", show(&build_response(200, &[("Content-Type", "text/plain")], '
                 '"привет".as_bytes())));\n'
                 '    println!("{}", show(&build_response(404, &[], b"")));\n'
                 '    println!("{}", show(&build_response(418, &[("X-A", "1"), ("X-B", "2")], b"tea")));\n'
                 '    println!("{}", build_response(204, &[], b"").len());\n'
                 '}\n',
       'expected': ['HTTP/1.1 200 OK|Content-Type: text/plain|Content-Length: 12|Connection: close||привет',
                    'HTTP/1.1 404 Not Found|Content-Length: 0|Connection: close||',
                    'HTTP/1.1 418 Unknown|X-A: 1|X-B: 2|Content-Length: 3|Connection: close||tea',
                    '65'],
       'hint': 'body.len() — байты; собирайте заголовок строкой, потом превращайте в байты и дописывайте '
               'тело.'},
      {'id': 'r41-json-encode',
       'mode': 'rust',
       'title': 'Кодирование JSON',
       'statement': 'Для enum Json { Null, Bool(bool), Num(f64), Str(String), Arr(Vec<Json>), '
                    'Obj(Vec<(String, Json)>) } напишите to_json(v: &Json) -> String (компактно, без '
                    'пробелов, порядок ключей как в Vec). Числа: целые значения без дробной части (3.0 → 3), '
                    'иначе стандартный вывод {}; строки экранируются: \\" \\\\ \\n \\r \\t, прочие '
                    'управляющие символы (< 0x20) — \\u00XX строчными шестнадцатеричными цифрами.',
       'starter': 'enum Json {\n'
                  '    Null,\n'
                  '    Bool(bool),\n'
                  '    Num(f64),\n'
                  '    Str(String),\n'
                  '    Arr(Vec<Json>),\n'
                  '    Obj(Vec<(String, Json)>),\n'
                  '}\n'
                  '\n'
                  'fn to_json(v: &Json) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v = Json::Obj(vec![\n'
                 '        ("name".to_string(), Json::Str("Ann \\"A\\"\\nLee\\t\\u{1}".to_string())),\n'
                 '        ("age".to_string(), Json::Num(31.0)),\n'
                 '        ("score".to_string(), Json::Num(4.5)),\n'
                 '        ("tags".to_string(), Json::Arr(vec![Json::Str("a\\\\b".to_string()), Json::Null, '
                 'Json::Bool(true)])),\n'
                 '        ("nested".to_string(), Json::Obj(vec![("empty".to_string(), '
                 'Json::Arr(vec![]))])),\n'
                 '        ("neg".to_string(), Json::Num(-0.25)),\n'
                 '    ]);\n'
                 '    println!("{}", to_json(&v));\n'
                 '    println!("{} {}", to_json(&Json::Null), to_json(&Json::Obj(vec![])));\n'
                 '}\n',
       'expected': ['{"name":"Ann '
                    '\\"A\\"\\nLee\\t\\u0001","age":31,"score":4.5,"tags":["a\\\\b",null,true],"nested":{"empty":[]},"neg":-0.25}',
                    'null {}'],
       'hint': 'Рекурсия по вариантам; целое число — через as i64, чтобы не печатать «31.0».'},
      {'id': 'r41-json-parse',
       'mode': 'rust',
       'title': 'Разбор JSON',
       'statement': 'Напишите parse_json(s: &str) -> Result<Json, String> (enum Json дан): null, true/false, '
                    'числа (как у f64::from_str; без ведущих плюсов), строки с экранированием \\" \\\\ \\/ '
                    '\\n \\r \\t \\uXXXX (только базовая плоскость), массивы и объекты; пробелы между '
                    'элементами игнорируются. Любая ошибка синтаксиса или лишние символы после значения — '
                    'Err("parse error"). Глубина вложенности в тестах небольшая.',
       'starter': '#[derive(Debug, PartialEq)]\n'
                  'enum Json {\n'
                  '    Null,\n'
                  '    Bool(bool),\n'
                  '    Num(f64),\n'
                  '    Str(String),\n'
                  '    Arr(Vec<Json>),\n'
                  '    Obj(Vec<(String, Json)>),\n'
                  '}\n'
                  '\n'
                  'fn parse_json(s: &str) -> Result<Json, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_json(r#"{"a": 1, "b": [true, null, "x\\ny"], "c": {"d": '
                 '-2.5e1}}"#));\n'
                 '    println!("{:?} {:?}", parse_json("  [ ]  "), parse_json("{}"));\n'
                 '    println!("{:?}", parse_json(r#""Aé \\"q\\" \\/""#));\n'
                 '    for bad in ["", "[1,", "{\\"a\\" 1}", "tru", "[1] x", "\\"abc", "+1", "{\'a\':1}", "[1 '
                 '2]"] {\n'
                 '        println!("{:?} {:?}", bad, parse_json(bad));\n'
                 '    }\n'
                 '}\n',
       'expected': ['Ok(Obj([("a", Num(1.0)), ("b", Arr([Bool(true), Null, Str("x\\ny")])), ("c", Obj([("d", '
                    'Num(-25.0))]))]))',
                    'Ok(Arr([])) Ok(Obj([]))',
                    'Ok(Str("Aé \\"q\\" /"))',
                    '"" Err("parse error")',
                    '"[1," Err("parse error")',
                    '"{\\"a\\" 1}" Err("parse error")',
                    '"tru" Err("parse error")',
                    '"[1] x" Err("parse error")',
                    '"\\"abc" Err("parse error")',
                    '"+1" Err("parse error")',
                    '"{\'a\':1}" Err("parse error")',
                    '"[1 2]" Err("parse error")'],
       'hint': 'Рекурсивный спуск: структура с позицией i; value() смотрит на первый байт и выбирает ветку; '
               'после значения останутся только пробелы.'},
      {'id': 'r41-safe-path',
       'mode': 'rust',
       'title': 'Безопасный путь и тип содержимого',
       'statement': 'Напишите safe_join(root: &str, url_path: &str) -> Option<String>: путь из запроса (без '
                    "query) присоединяется к корню; допустимы только обычные компоненты, пустые и '.' "
                    "пропускаются, любой '..' или обратная косая черта в компоненте — None; процентное "
                    "кодирование НЕ декодируется (но компонент '%2e%2e' — тоже None). Результат — root + '/' "
                    "+ компоненты через '/'. И mime(path: &str) -> &'static str: html → text/html; css → "
                    'text/css; js → text/javascript; json → application/json; png → image/png; txt → '
                    'text/plain; прочее — application/octet-stream (регистр расширения не важен).',
       'starter': 'fn safe_join(root: &str, url_path: &str) -> Option<String> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn mime(path: &str) -> &'static str {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for p in ["/index.html", "/a/./b//c.css", "/", "/../etc/passwd", "/a/../../x", '
                 '"/a\\\\..\\\\b", "/%2E%2e/x", "/ok/..hidden"] {\n'
                 '        println!("{:?} -> {:?}", p, safe_join("/srv/www/", p));\n'
                 '    }\n'
                 '    for f in ["a.HTML", "x/y.js", "data.json", "logo.PNG", "README", "archive.tar.gz", '
                 '".txt", "a.b/c"] {\n'
                 '        println!("{} {}", f, mime(f));\n'
                 '    }\n'
                 '}\n',
       'expected': ['"/index.html" -> Some("/srv/www/index.html")',
                    '"/a/./b//c.css" -> Some("/srv/www/a/b/c.css")',
                    '"/" -> Some("/srv/www")',
                    '"/../etc/passwd" -> None',
                    '"/a/../../x" -> None',
                    '"/a\\\\..\\\\b" -> None',
                    '"/%2E%2e/x" -> None',
                    '"/ok/..hidden" -> Some("/srv/www/ok/..hidden")',
                    'a.HTML text/html',
                    'x/y.js text/javascript',
                    'data.json application/json',
                    'logo.PNG image/png',
                    'README application/octet-stream',
                    'archive.tar.gz application/octet-stream',
                    '.txt text/plain',
                    'a.b/c application/octet-stream'],
       'hint': 'Проверяйте каждый компонент отдельно; «..» запрещён всегда, даже если в итоге не выходит за '
               'корень.'},
      {'id': 'r41-range',
       'mode': 'rust',
       'title': 'Заголовок Range',
       'statement': 'Напишите parse_range(header: &str, size: u64) -> Option<(u64, u64)>: значение '
                    "'bytes=START-END' для файла размером size → включительные границы (первый, последний). "
                    "'bytes=500-' — до конца файла; 'bytes=-100' — последние 100 байт (если файл короче — "
                    'весь файл); END больше размера обрезается до size − 1; None — если формат неверный, '
                    'START ≥ size, START > END, size = 0 или диапазонов несколько (запятая).',
       'starter': 'fn parse_range(header: &str, size: u64) -> Option<(u64, u64)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for h in ["bytes=0-99", "bytes=500-", "bytes=-100", "bytes=-5000", "bytes=900-2000", '
                 '"bytes=1000-1005", "bytes=50-10", "bytes=0-1,5-6", "items=0-1", "bytes=", "bytes=a-b", '
                 '"bytes=-0", "bytes=-"] {\n'
                 '        println!("{} {:?}", h, parse_range(h, 1000));\n'
                 '    }\n'
                 '    println!("{:?}", parse_range("bytes=0-0", 0));\n'
                 '}\n',
       'expected': ['bytes=0-99 Some((0, 99))',
                    'bytes=500- Some((500, 999))',
                    'bytes=-100 Some((900, 999))',
                    'bytes=-5000 Some((0, 999))',
                    'bytes=900-2000 Some((900, 999))',
                    'bytes=1000-1005 None',
                    'bytes=50-10 None',
                    'bytes=0-1,5-6 None',
                    'items=0-1 None',
                    'bytes= None',
                    'bytes=a-b None',
                    'bytes=-0 None',
                    'bytes=- None',
                    'None'],
       'hint': 'Три формы: «a-b», «a-» и «-n»; последнюю считайте через saturating_sub.'},
      {'id': 'r41-cookies',
       'mode': 'rust',
       'title': 'Cookie',
       'statement': "Напишите parse_cookies(header: &str) -> BTreeMap<String, String> (формат 'a=1; b=two; "
                    "flag'; пробелы вокруг имён и значений обрезаются; пара без '=' — пустое значение; "
                    'пустые части пропускаются; при повторе побеждает последнее) и set_cookie(name: &str, '
                    "value: &str, max_age: Option<u32>, http_only: bool) -> String: 'name=value' + '; "
                    "Max-Age=N' (если задан) + '; HttpOnly' (если нужно) + всегда '; Path=/'. Порядок "
                    'частей: Max-Age, Path, HttpOnly.',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn parse_cookies(header: &str) -> BTreeMap<String, String> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn set_cookie(name: &str, value: &str, max_age: Option<u32>, http_only: bool) -> String '
                  '{\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_cookies("a=1; b = two ;flag; ; a=3; c=x=y"));\n'
                 '    println!("{:?} {:?}", parse_cookies(""), parse_cookies(" ; "));\n'
                 '    println!("{}", set_cookie("sid", "abc123", Some(3600), true));\n'
                 '    println!("{}", set_cookie("theme", "dark", None, false));\n'
                 '}\n',
       'expected': ['{"a": "3", "b": "two", "c": "x=y", "flag": ""}',
                    '{} {}',
                    'sid=abc123; Max-Age=3600; Path=/; HttpOnly',
                    'theme=dark; Path=/'],
       'hint': "split(';'), trim, split_once('=') — значение может содержать '=' (берётся всё после "
               'первого).'},
      {'id': 'r41-serve-one',
       'mode': 'rust',
       'title': 'Мини-сервер: один запрос',
       'statement': 'Напишите serve_one(stream: TcpStream) -> io::Result<()>: прочитайте один '
                    'HTTP/1.1-запрос (заголовки до пустой строки, тело по Content-Length), отправьте ответ и '
                    'закройте соединение (Connection: close; Content-Length в байтах). Маршруты: GET '
                    '/hello?name=X → 200 text/plain "Hello, X!" (X без декодирования; без параметра — '
                    '"Hello, world!"); POST /echo → 200 с телом запроса; любой другой путь → 404 "not '
                    'found"; для /hello и /echo с неверным методом → 405 "method not allowed"; неразборчивая '
                    'стартовая строка → 400 "bad request". Тело ответа — текст.',
       'starter': 'use std::io;\n'
                  'use std::net::TcpStream;\n'
                  '\n'
                  'fn serve_one(stream: TcpStream) -> io::Result<()> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'use std::io::{Read, Write};\n'
                 'use std::net::{TcpListener, TcpStream};\n'
                 'use std::thread;\n'
                 '\n'
                 'fn call(addr: std::net::SocketAddr, raw: &str) -> (String, String) {\n'
                 '    let mut c = TcpStream::connect(addr).unwrap();\n'
                 '    for chunk in raw.as_bytes().chunks(7) {\n'
                 '        c.write_all(chunk).unwrap();\n'
                 '        c.flush().unwrap();\n'
                 '    }\n'
                 '    let mut out = String::new();\n'
                 '    c.read_to_string(&mut out).unwrap();\n'
                 '    let (head, body) = out.split_once("\\r\\n\\r\\n").unwrap();\n'
                 '    let status = head.lines().next().unwrap().to_string();\n'
                 '    let clen: usize = head.lines().find_map(|l| l.strip_prefix("Content-Length: '
                 '")).unwrap().parse().unwrap();\n'
                 '    assert_eq!(clen, body.len());\n'
                 '    (status, body.to_string())\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let l = TcpListener::bind("127.0.0.1:0").unwrap();\n'
                 '    let addr = l.local_addr().unwrap();\n'
                 '    let reqs = [\n'
                 '        "GET /hello?name=Ann HTTP/1.1\\r\\nHost: x\\r\\n\\r\\n",\n'
                 '        "GET /hello HTTP/1.1\\r\\nHost: x\\r\\n\\r\\n",\n'
                 '        "POST /echo HTTP/1.1\\r\\nHost: x\\r\\nContent-Length: 21\\r\\n\\r\\nпривет, '
                 'мир\\n",\n'
                 '        "DELETE /echo HTTP/1.1\\r\\n\\r\\n",\n'
                 '        "GET /nope HTTP/1.1\\r\\n\\r\\n",\n'
                 '        "BROKEN\\r\\n\\r\\n",\n'
                 '    ];\n'
                 '    let n = reqs.len();\n'
                 '    let srv = thread::spawn(move || {\n'
                 '        for s in l.incoming().take(n) {\n'
                 '            serve_one(s.unwrap()).unwrap();\n'
                 '        }\n'
                 '    });\n'
                 '    for r in reqs {\n'
                 '        println!("{:?}", call(addr, r));\n'
                 '    }\n'
                 '    srv.join().unwrap();\n'
                 '}\n',
       'expected': ['("HTTP/1.1 200 OK", "Hello, Ann!")',
                    '("HTTP/1.1 200 OK", "Hello, world!")',
                    '("HTTP/1.1 200 OK", "привет, мир\\n")',
                    '("HTTP/1.1 405 Method Not Allowed", "method not allowed")',
                    '("HTTP/1.1 404 Not Found", "not found")',
                    '("HTTP/1.1 400 Bad Request", "bad request")'],
       'hint': 'Читайте через BufReader: read_line для стартовой строки и заголовков, read_exact для тела; '
               'ответ собирайте одной строкой и пишите write!.'}]}
