"""Задачи книги «Изучаем Rust»: глава 43 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {43: [{'id': 'r43-encode-messages',
       'mode': 'rust',
       'title': 'Сообщения клиента Postgres',
       'statement': 'Напишите startup_message(params: &[(&str, &str)]) -> Vec<u8> (длина i32 включая себя; '
                    "версия протокола 196608 (3.0) как i32; затем пары 'имя\\0значение\\0'; в конце ещё один "
                    "нулевой байт), query_message(sql: &str) -> Vec<u8> ('Q', длина i32 = 4 + байты sql + 1, "
                    "текст, нулевой байт), terminate_message() -> Vec<u8> ('X', длина 4) и "
                    "password_message(pw: &str) -> Vec<u8> ('p', длина, пароль и нулевой байт). Все числа — "
                    'старшим байтом вперёд.',
       'starter': 'fn startup_message(params: &[(&str, &str)]) -> Vec<u8> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn query_message(sql: &str) -> Vec<u8> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn terminate_message() -> Vec<u8> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn password_message(pw: &str) -> Vec<u8> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let s = startup_message(&[("user", "app"), ("database", "shop")]);\n'
                 '    println!("{} {:?}", s.len(), &s[..8]);\n'
                 '    println!("{:?}", String::from_utf8_lossy(&s[8..]).replace(\'\\0\', "|"));\n'
                 '    println!("{:?}", startup_message(&[]));\n'
                 '    println!("{:?}", query_message("SELECT 1"));\n'
                 '    println!("{:?} {:?}", terminate_message(), password_message("pw"));\n'
                 '    let q = query_message("SELECT \'привет\'");\n'
                 '    println!("{} {}", q.len(), u32::from_be_bytes([q[1], q[2], q[3], q[4]]));\n'
                 '}\n',
       'expected': ['32 [0, 0, 0, 32, 0, 3, 0, 0]',
                    '"user|app|database|shop||"',
                    '[0, 0, 0, 9, 0, 3, 0, 0, 0]',
                    '[81, 0, 0, 0, 13, 83, 69, 76, 69, 67, 84, 32, 49, 0]',
                    '[88, 0, 0, 0, 4] [112, 0, 0, 0, 7, 112, 119, 0]',
                    '27 26'],
       'hint': 'Общий помощник: метка + (длина тела + 4) как u32::to_be_bytes + тело.'},
      {'id': 'r43-decode-messages',
       'mode': 'rust',
       'title': 'Сообщения сервера Postgres',
       'statement': 'Напишите read_message(buf: &[u8]) -> Option<(u8, Vec<u8>, usize)> (метка, содержимое, '
                    'сколько байтов занято; None — если сообщение неполное), data_row(payload: &[u8]) -> '
                    'Result<Vec<Option<String>>, String> (число колонок i16, для каждой длина i32 и байты; '
                    '−1 — NULL; ошибка "truncated", если данных не хватает) и error_fields(payload: &[u8]) '
                    "-> BTreeMap<char, String> (ErrorResponse: пары 'метка-байт, строка с нулём', "
                    'завершается нулевым байтом).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn read_message(buf: &[u8]) -> Option<(u8, Vec<u8>, usize)> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn data_row(payload: &[u8]) -> Result<Vec<Option<String>>, String> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn error_fields(payload: &[u8]) -> BTreeMap<char, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn msg(tag: u8, payload: &[u8]) -> Vec<u8> {\n'
                 '    let mut m = vec![tag];\n'
                 '    m.extend_from_slice(&((payload.len() + 4) as u32).to_be_bytes());\n'
                 '    m.extend_from_slice(payload);\n'
                 '    m\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let mut row = vec![0, 3];\n'
                 '    for c in [Some("42"), None, Some("привет")] {\n'
                 '        match c {\n'
                 '            Some(s) => {\n'
                 '                row.extend_from_slice(&(s.len() as i32).to_be_bytes());\n'
                 '                row.extend_from_slice(s.as_bytes());\n'
                 '            }\n'
                 '            None => row.extend_from_slice(&(-1i32).to_be_bytes()),\n'
                 '        }\n'
                 '    }\n'
                 "    let mut stream = msg(b'D', &row);\n"
                 '    stream.extend(msg(b\'C\', b"SELECT 1\\0"));\n'
                 '    stream.extend(msg(b\'Z\', b"I"));\n'
                 '    let mut off = 0;\n'
                 '    while let Some((tag, payload, used)) = read_message(&stream[off..]) {\n'
                 '        println!("{} {} {}", tag as char, payload.len(), used);\n'
                 '        off += used;\n'
                 '    }\n'
                 '    println!("{}", off == stream.len());\n'
                 '    let (_, p, _) = read_message(&stream).unwrap();\n'
                 '    println!("{:?}", data_row(&p));\n'
                 '    println!("{:?} {:?}", data_row(&p[..10]), data_row(&[0, 1, 0, 0, 0, 9, 1]));\n'
                 '    println!("{:?} {:?}", read_message(&stream[..4]), read_message(&stream[..8]).map(|m| '
                 'm.0));\n'
                 '    let err = b"SERROR\\0C42P01\\0Mrelation \\"users\\" does not exist\\0\\0";\n'
                 '    println!("{:?}", error_fields(err));\n'
                 '}\n',
       'expected': ['D 28 33',
                    'C 9 14',
                    'Z 1 6',
                    'true',
                    'Ok([Some("42"), None, Some("привет")])',
                    'Err("truncated") Err("truncated")',
                    'None None',
                    '{\'C\': "42P01", \'M\': "relation \\"users\\" does not exist", \'S\': "ERROR"}'],
       'hint': 'Проверяйте границы всегда через get(..) — неполные данные не должны вызывать панику.'},
      {'id': 'r43-from-column',
       'mode': 'rust',
       'title': 'Отображение колонок в типы',
       'statement': 'Трейт FromColumn с методом from_col(c: Option<&str>) -> Result<Self, String> дан. '
                    'Реализуйте его для i32 (NULL → Err("NULL"), нечисло → Err("bad int: ТЕКСТ")), f64 '
                    '(аналогично "bad float: ТЕКСТ"), bool (\'t\'/\'f\'; иное — Err("bad bool: ТЕКСТ")), '
                    'String и Option<T> (для любого T: FromColumn; None → Ok(None)). Затем напишите '
                    'product_from_row(row: &[Option<&str>]) -> Result<Product, String>; ошибки колонки '
                    'оформляются как "column N: ошибка" (N с нуля).',
       'starter': 'trait FromColumn: Sized {\n'
                  '    fn from_col(c: Option<&str>) -> Result<Self, String>;\n'
                  '}\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'struct Product {\n'
                  '    id: i32,\n'
                  '    title: String,\n'
                  '    price: f64,\n'
                  '    in_stock: bool,\n'
                  '    discount: Option<f64>,\n'
                  '}\n'
                  '\n'
                  '// impl FromColumn for i32, f64, bool, String, Option<T> ...\n'
                  '\n'
                  'fn product_from_row(row: &[Option<&str>]) -> Result<Product, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", product_from_row(&[Some("1"), Some("Laptop"), Some("999.5"), '
                 'Some("t"), None]));\n'
                 '    println!("{:?}", product_from_row(&[Some("2"), Some("Mouse"), Some("15"), Some("f"), '
                 'Some("0.1")]));\n'
                 '    println!("{:?}", product_from_row(&[Some("x"), Some("A"), Some("1"), Some("t"), '
                 'None]));\n'
                 '    println!("{:?}", product_from_row(&[Some("3"), None, Some("1"), Some("t"), None]));\n'
                 '    println!("{:?}", product_from_row(&[Some("3"), Some("B"), Some("1.x"), Some("t"), '
                 'None]));\n'
                 '    println!("{:?}", product_from_row(&[Some("3"), Some("B"), Some("1"), Some("yes"), '
                 'None]));\n'
                 '    println!("{:?}", product_from_row(&[Some("3"), Some("B"), Some("1"), Some("t"), '
                 'Some("zz")]));\n'
                 '    println!("{:?}", product_from_row(&[Some("3")]));\n'
                 '}\n',
       'expected': ['Ok(Product { id: 1, title: "Laptop", price: 999.5, in_stock: true, discount: None })',
                    'Ok(Product { id: 2, title: "Mouse", price: 15.0, in_stock: false, discount: Some(0.1) '
                    '})',
                    'Err("column 0: bad int: x")',
                    'Err("column 1: NULL")',
                    'Err("column 2: bad float: 1.x")',
                    'Err("column 3: bad bool: yes")',
                    'Err("column 4: bad float: zz")',
                    'Err("column 1: NULL")'],
       'hint': 'Вспомогательная обобщённая функция col::<T>(row, i) собирает префикс «column N: » к любой '
               'ошибке.'},
      {'id': 'r43-render-query',
       'mode': 'rust',
       'title': 'Подстановка параметров для журнала',
       'statement': 'Для лога запросов напишите quote_literal(s: &str) -> String (кавычки вокруг, внутренние '
                    "' удваиваются) и render_query(sql: &str, params: &[Option<&str>]) -> String: каждое $N "
                    '(N — число из одной или нескольких цифр, нумерация с единицы) заменяется на NULL для '
                    "None и quote_literal для Some; $N с номером вне списка и одиночный '$' остаются как "
                    'есть. Внутри строковых литералов в sql замен не делайте (текст между одинарными '
                    "кавычками копируется без изменений; '' внутри — экранированная кавычка).",
       'starter': 'fn quote_literal(s: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn render_query(sql: &str, params: &[Option<&str>]) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", quote_literal("O\'Brien"));\n'
                 '    println!("{}", render_query("SELECT * FROM u WHERE name = $1 AND age > $2 AND note IS '
                 'NOT DISTINCT FROM $3", &[Some("x\' OR \'1\'=\'1"), Some("18"), None]));\n'
                 '    println!("{}", render_query("SELECT $1, $10, $2, \'$1 stays\', $5, $", &[Some("a"), '
                 'Some("b")]));\n'
                 '    let many: Vec<String> = (1..=10).map(|i| format!("v{}", i)).collect();\n'
                 '    let refs: Vec<Option<&str>> = many.iter().map(|s| Some(s.as_str())).collect();\n'
                 '    println!("{}", render_query("$1 $10 $2", &refs));\n'
                 '    println!("{}", render_query("SELECT \'it\'\'s $1\' || $1", &[Some("z")]));\n'
                 '}\n',
       'expected': ["'O''Brien'",
                    "SELECT * FROM u WHERE name = 'x'' OR ''1''=''1' AND age > '18' AND note IS NOT DISTINCT "
                    'FROM NULL',
                    "SELECT 'a', $10, 'b', '$1 stays', $5, $",
                    "'v1' 'v10' 'v2'",
                    "SELECT 'it''s $1' || 'z'"],
       'hint': "Идите по символам, помните, внутри ли вы строкового литерала; число после '$' читайте до "
               "конца цифр, чтобы $10 не превратился в $1 и '0'."},
      {'id': 'r43-select-builder',
       'mode': 'rust',
       'title': 'Построитель SELECT',
       'statement': 'Реализуйте Select: from(table), filter(mut self, col, op, value) (добавляет «col op '
                    '$N»), filter_in(mut self, col, values: &[&str]) («col IN ($N, $N+1, …)»; пустой список '
                    '— условие «FALSE»), order_by(mut self, col, desc: bool), limit(mut self, n), offset(mut '
                    "self, n) и build(&self) -> (String, Vec<String>): 'SELECT * FROM t' + ' WHERE a AND b' "
                    "+ ' ORDER BY col ASC|DESC' + ' LIMIT n' + ' OFFSET n'; параметры — в порядке нумерации.",
       'starter': 'struct Select {\n'
                  '    table: String,\n'
                  '    conds: Vec<String>,\n'
                  '    params: Vec<String>,\n'
                  '    order: Option<String>,\n'
                  '    limit: Option<u32>,\n'
                  '    offset: Option<u32>,\n'
                  '}\n'
                  '\n'
                  'impl Select {\n'
                  '    fn from(table: &str) -> Select {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn filter(mut self, col: &str, op: &str, value: &str) -> Select {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn filter_in(mut self, col: &str, values: &[&str]) -> Select {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn order_by(mut self, col: &str, desc: bool) -> Select {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn limit(mut self, n: u32) -> Select {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn offset(mut self, n: u32) -> Select {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn build(&self) -> (String, Vec<String>) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let (sql, p) = Select::from("users").build();\n'
                 '    println!("{} {:?}", sql, p);\n'
                 '    let q = Select::from("orders")\n'
                 '        .filter("total", ">", "100")\n'
                 '        .filter_in("status", &["new", "paid", "shipped"])\n'
                 '        .filter("city", "=", "Moscow")\n'
                 '        .order_by("created_at", true)\n'
                 '        .limit(20)\n'
                 '        .offset(40);\n'
                 '    let (sql, p) = q.build();\n'
                 '    println!("{}", sql);\n'
                 '    println!("{:?}", p);\n'
                 '    let (sql, p) = Select::from("t").filter_in("id", &[]).limit(1).build();\n'
                 '    println!("{} {:?}", sql, p);\n'
                 '}\n',
       'expected': ['SELECT * FROM users []',
                    'SELECT * FROM orders WHERE total > $1 AND status IN ($2, $3, $4) AND city = $5 ORDER BY '
                    'created_at DESC LIMIT 20 OFFSET 40',
                    '["100", "new", "paid", "shipped", "Moscow"]',
                    'SELECT * FROM t WHERE FALSE LIMIT 1 []'],
       'hint': 'Номер параметра = длина списка params после добавления; filter_in добавляет сразу '
               'несколько.'},
      {'id': 'r43-pool-timeout',
       'mode': 'rust',
       'title': 'Пул соединений с таймаутом',
       'statement': 'Реализуйте Pool: new(n: u32) -> Arc<Pool> (соединения 1…n), get(self: &Arc<Self>, '
                    'timeout: Duration) -> Option<PooledConn> (ждёт свободного соединения, но не дольше '
                    'timeout; None по истечении) и Drop для PooledConn, возвращающий соединение и будящий '
                    'ожидающего. Метод idle(&self) -> usize — сколько соединений свободно.',
       'starter': 'use std::sync::{Arc, Condvar, Mutex};\n'
                  'use std::time::Duration;\n'
                  '\n'
                  'struct Pool {\n'
                  '    conns: Mutex<Vec<u32>>,\n'
                  '    cv: Condvar,\n'
                  '}\n'
                  '\n'
                  'struct PooledConn {\n'
                  '    id: u32,\n'
                  '    pool: Arc<Pool>,\n'
                  '}\n'
                  '\n'
                  'impl Pool {\n'
                  '    fn new(n: u32) -> Arc<Pool> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn get(self: &Arc<Self>, timeout: Duration) -> Option<PooledConn> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn idle(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Drop for PooledConn {\n'
                  '    fn drop(&mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'use std::thread;\n'
                 'use std::time::{Duration, Instant};\n'
                 '\n'
                 'fn main() {\n'
                 '    let pool = Pool::new(2);\n'
                 '    let a = pool.get(Duration::from_millis(10)).unwrap();\n'
                 '    let b = pool.get(Duration::from_millis(10)).unwrap();\n'
                 '    println!("{} {} {}", pool.idle(), a.id != b.id, a.id + b.id);\n'
                 '    let t = Instant::now();\n'
                 '    let none = pool.get(Duration::from_millis(60));\n'
                 '    println!("{} {}", none.is_none(), t.elapsed() >= Duration::from_millis(55));\n'
                 '    let p2 = Arc::clone(&pool);\n'
                 '    let waiter = thread::spawn(move || p2.get(Duration::from_secs(5)).map(|c| c.id));\n'
                 '    thread::sleep(Duration::from_millis(30));\n'
                 '    let a_id = a.id;\n'
                 '    drop(a);\n'
                 '    println!("{}", waiter.join().unwrap() == Some(a_id));\n'
                 '    drop(b);\n'
                 '    println!("{}", pool.idle());\n'
                 '    let workers: Vec<_> = (0..8)\n'
                 '        .map(|_| {\n'
                 '            let p = Arc::clone(&pool);\n'
                 '            thread::spawn(move || {\n'
                 '                let mut got = 0;\n'
                 '                for _ in 0..20 {\n'
                 '                    if let Some(c) = p.get(Duration::from_secs(5)) {\n'
                 '                        thread::sleep(Duration::from_millis(1));\n'
                 '                        got += (c.id > 0) as u32;\n'
                 '                    }\n'
                 '                }\n'
                 '                got\n'
                 '            })\n'
                 '        })\n'
                 '        .collect();\n'
                 '    let total: u32 = workers.into_iter().map(|h| h.join().unwrap()).sum();\n'
                 '    println!("{} {}", total, pool.idle());\n'
                 '}\n',
       'expected': ['0 true 3', 'true true', 'true', '2', '160 2'],
       'hint': 'Condvar::wait_timeout(guard, остаток) возвращает защитник; пересчитывайте остаток времени в '
               'цикле — возможны ложные пробуждения.'},
      {'id': 'r43-tx-savepoint',
       'mode': 'rust',
       'title': 'Транзакции и точки сохранения',
       'statement': "Дано Conn (журнал команд). Реализуйте Tx<'a>: begin(conn) → 'BEGIN'; commit(self) → "
                    "'COMMIT'; rollback(self) → 'ROLLBACK'; Drop без commit/rollback → 'ROLLBACK'. Метод "
                    "savepoint(&mut self, name: &str) -> Savepoint<'_, 'a> шлёт 'SAVEPOINT name'; у "
                    "Savepoint метод release(self) шлёт 'RELEASE SAVEPOINT name', а Drop без release — "
                    "'ROLLBACK TO SAVEPOINT name'.",
       'starter': 'use std::cell::RefCell;\n'
                  '\n'
                  'struct Conn {\n'
                  '    log: RefCell<Vec<String>>,\n'
                  '}\n'
                  '\n'
                  'impl Conn {\n'
                  '    fn exec(&self, sql: &str) {\n'
                  '        self.log.borrow_mut().push(sql.to_string());\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  "struct Tx<'a> {\n"
                  "    conn: &'a Conn,\n"
                  '    done: bool,\n'
                  '}\n'
                  '\n'
                  "struct Savepoint<'t, 'a> {\n"
                  "    tx: &'t Tx<'a>,\n"
                  '    name: String,\n'
                  '    done: bool,\n'
                  '}\n'
                  '\n'
                  "impl<'a> Tx<'a> {\n"
                  "    fn begin(conn: &'a Conn) -> Tx<'a> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '    fn commit(mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn rollback(mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  "    fn savepoint<'t>(&'t mut self, name: &str) -> Savepoint<'t, 'a> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  "impl<'a> Drop for Tx<'a> {\n"
                  '    fn drop(&mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  "impl<'t, 'a> Savepoint<'t, 'a> {\n"
                  '    fn release(mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  "impl<'t, 'a> Drop for Savepoint<'t, 'a> {\n"
                  '    fn drop(&mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn work(conn: &Conn, fail_inner: bool, fail_outer: bool) -> Result<(), String> {\n'
                 '    let mut tx = Tx::begin(conn);\n'
                 '    conn.exec("INSERT a");\n'
                 '    {\n'
                 '        let sp = tx.savepoint("s1");\n'
                 '        conn.exec("INSERT b");\n'
                 '        if fail_inner {\n'
                 '            return_inner(&sp)?;\n'
                 '        }\n'
                 '        sp.release();\n'
                 '    }\n'
                 '    if fail_outer {\n'
                 '        return Err("outer".to_string());\n'
                 '    }\n'
                 '    tx.commit();\n'
                 '    Ok(())\n'
                 '}\n'
                 '\n'
                 'fn return_inner(_sp: &Savepoint) -> Result<(), String> {\n'
                 '    Err("inner".to_string())\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let c = Conn { log: RefCell::new(vec![]) };\n'
                 '    println!("{:?}", work(&c, false, false));\n'
                 '    println!("{:?}", work(&c, true, false));\n'
                 '    println!("{:?}", work(&c, false, true));\n'
                 '    let tx = Tx::begin(&c);\n'
                 '    tx.rollback();\n'
                 '    for l in c.log.borrow().iter() {\n'
                 '        println!("{}", l);\n'
                 '    }\n'
                 '}\n',
       'expected': ['Ok(())',
                    'Err("inner")',
                    'Err("outer")',
                    'BEGIN',
                    'INSERT a',
                    'SAVEPOINT s1',
                    'INSERT b',
                    'RELEASE SAVEPOINT s1',
                    'COMMIT',
                    'BEGIN',
                    'INSERT a',
                    'SAVEPOINT s1',
                    'INSERT b',
                    'ROLLBACK TO SAVEPOINT s1',
                    'ROLLBACK',
                    'BEGIN',
                    'INSERT a',
                    'SAVEPOINT s1',
                    'INSERT b',
                    'RELEASE SAVEPOINT s1',
                    'ROLLBACK',
                    'BEGIN',
                    'ROLLBACK'],
       'hint': 'Флаг done у обоих охранных объектов; commit/rollback/release забирают self по значению и '
               'помечают done, чтобы Drop ничего не отправил.'},
      {'id': 'r43-migrations',
       'mode': 'rust',
       'title': 'Запуск миграций',
       'statement': 'Напишите run_migrations(applied: &mut Vec<u32>, migrations: &[Migration], exec: &mut '
                    'dyn FnMut(&str) -> Result<(), String>) -> Result<Vec<u32>, String>: миграции '
                    'сортируются по версии; если у двух одинаковая версия — Err("duplicate version N") до '
                    'выполнения чего-либо; уже применённые (есть в applied) пропускаются; остальные '
                    'выполняются по одной через exec(sql); после успеха версия добавляется в applied и в '
                    'результат; при ошибке — остановка и Err("migration N failed: ТЕКСТ"), уже выполненные '
                    'остаются в applied. Результат — список новых версий по порядку.',
       'starter': 'struct Migration {\n'
                  '    version: u32,\n'
                  "    sql: &'static str,\n"
                  '}\n'
                  '\n'
                  'fn run_migrations(applied: &mut Vec<u32>, migrations: &[Migration], exec: &mut dyn '
                  'FnMut(&str) -> Result<(), String>) -> Result<Vec<u32>, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let ms = [\n'
                 '        Migration { version: 3, sql: "CREATE INDEX i" },\n'
                 '        Migration { version: 1, sql: "CREATE TABLE t" },\n'
                 '        Migration { version: 2, sql: "ALTER TABLE t" },\n'
                 '        Migration { version: 4, sql: "BROKEN" },\n'
                 '        Migration { version: 5, sql: "DROP TABLE x" },\n'
                 '    ];\n'
                 '    let mut executed: Vec<String> = Vec::new();\n'
                 '    let mut applied = vec![1];\n'
                 '    let mut exec = |sql: &str| -> Result<(), String> {\n'
                 '        if sql == "BROKEN" {\n'
                 '            Err("syntax error".to_string())\n'
                 '        } else {\n'
                 '            executed.push(sql.to_string());\n'
                 '            Ok(())\n'
                 '        }\n'
                 '    };\n'
                 '    println!("{:?}", run_migrations(&mut applied, &ms, &mut exec));\n'
                 '    println!("{:?}", applied);\n'
                 '    println!("{:?}", run_migrations(&mut applied, &ms[..3], &mut exec));\n'
                 '    let dup = [Migration { version: 1, sql: "A" }, Migration { version: 1, sql: "B" }];\n'
                 '    println!("{:?}", run_migrations(&mut applied, &dup, &mut exec));\n'
                 '    println!("{:?}", executed);\n'
                 '}\n',
       'expected': ['Err("migration 4 failed: syntax error")',
                    '[1, 2, 3]',
                    'Ok([])',
                    'Err("duplicate version 1")',
                    '["ALTER TABLE t", "CREATE INDEX i"]'],
       'hint': 'Сначала проверка дубликатов на отсортированном списке (windows(2)); дальше цикл с ранним '
               'выходом по ошибке.'},
      {'id': 'r43-db-url',
       'mode': 'rust',
       'title': 'Адрес подключения',
       'statement': 'Напишите parse_url(url: &str) -> Result<DbUrl, String> для '
                    "'postgres://[user[:password]@]host[:port]/db[?k=v&k2=v2]' (также допустима схема "
                    "'postgresql://'): пароль и пользователь декодируются из процентного кодирования; порт "
                    "по умолчанию 5432; IPv6-хост в квадратных скобках ('[::1]') возвращается без скобок; "
                    'параметры запроса — в BTreeMap. Ошибки: "bad scheme", "missing host", "missing '
                    'database", "bad port".',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'struct DbUrl {\n'
                  '    user: String,\n'
                  '    password: String,\n'
                  '    host: String,\n'
                  '    port: u16,\n'
                  '    db: String,\n'
                  '    params: BTreeMap<String, String>,\n'
                  '}\n'
                  '\n'
                  'fn parse_url(url: &str) -> Result<DbUrl, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", '
                 'parse_url("postgres://app:p%40ss%3Aw@db.local:6543/shop?sslmode=require&connect_timeout=5"));\n'
                 '    println!("{:?}", parse_url("postgresql://localhost/mydb"));\n'
                 '    println!("{:?}", parse_url("postgres://u@[::1]:5433/d"));\n'
                 '    println!("{:?}", parse_url("postgres://u:pw@[2001:db8::1]/d?x"));\n'
                 '    for bad in ["mysql://a@b/c", "postgres://u@h", "postgres://u@h/", '
                 '"postgres://u@:5432/d", "postgres://u@h:99999/d", "postgres://u@[::1/d"] {\n'
                 '        println!("{:?}", parse_url(bad).err());\n'
                 '    }\n'
                 '}\n',
       'expected': ['Ok(DbUrl { user: "app", password: "p@ss:w", host: "db.local", port: 6543, db: "shop", '
                    'params: {"connect_timeout": "5", "sslmode": "require"} })',
                    'Ok(DbUrl { user: "", password: "", host: "localhost", port: 5432, db: "mydb", params: '
                    '{} })',
                    'Ok(DbUrl { user: "u", password: "", host: "::1", port: 5433, db: "d", params: {} })',
                    'Ok(DbUrl { user: "u", password: "pw", host: "2001:db8::1", port: 5432, db: "d", params: '
                    '{"x": ""} })',
                    'Some("bad scheme")',
                    'Some("missing database")',
                    'Some("missing database")',
                    'Some("missing host")',
                    'Some("bad port")',
                    'Some("missing host")'],
       'hint': "Разбирайте с конца к началу: сначала query, затем учётные данные (rsplit_once('@') — пароль "
               "может содержать '@' в закодированном виде), потом хост и база."},
      {'id': 'r43-aggregate',
       'mode': 'rust',
       'title': 'Агрегирование строк результата',
       'statement': 'Напишите aggregate(rows: &[Vec<Option<String>>], key: usize, val: usize) -> '
                    'BTreeMap<String, (i64, usize)>: для каждой строки ключ — колонка key (строки с NULL в '
                    'ключе пропускаются), значение — колонка val как i64 (NULL и не число пропускаются, но '
                    'строка всё равно учитывается как существующая группа). Результат: ключ → (сумма '
                    'значений, число учтённых значений).',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn aggregate(rows: &[Vec<Option<String>>], key: usize, val: usize) -> BTreeMap<String, '
                  '(i64, usize)> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn row(cells: &[Option<&str>]) -> Vec<Option<String>> {\n'
                 '    cells.iter().map(|c| c.map(|s| s.to_string())).collect()\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let rows = vec![\n'
                 '        row(&[Some("north"), Some("10")]),\n'
                 '        row(&[Some("south"), Some("5")]),\n'
                 '        row(&[Some("north"), Some("7")]),\n'
                 '        row(&[None, Some("100")]),\n'
                 '        row(&[Some("west"), None]),\n'
                 '        row(&[Some("south"), Some("x")]),\n'
                 '        row(&[Some("south")]),\n'
                 '        row(&[Some("north"), Some("-2")]),\n'
                 '    ];\n'
                 '    println!("{:?}", aggregate(&rows, 0, 1));\n'
                 '    println!("{:?}", aggregate(&[], 0, 1));\n'
                 '    println!("{:?}", aggregate(&rows, 5, 1));\n'
                 '}\n',
       'expected': ['{"north": (15, 3), "south": (5, 1), "west": (0, 0)}', '{}', '{}'],
       'hint': 'entry(ключ).or_insert((0, 0)) создаёт группу даже если значение не удалось разобрать; get(i) '
               'защищает от коротких строк.'}]}
