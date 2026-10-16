"""Задачи книги «Изучаем Rust»: глава 16 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {16: [{'id': 'r16-count-vowels',
       'mode': 'rust',
       'title': 'Заём для чтения: &str',
       'statement': 'Напишите count_vowels(s: &str) -> usize: сколько в строке гласных. Гласные — русские а '
                    'е ё и о у ы э ю я и латинские a e i o u, регистр не важен. Функция только читает: после '
                    'вызова строка остаётся у владельца.',
       'starter': 'fn count_vowels(s: &str) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let s = String::from("Привет, Rust");\n'
                 '    println!("{}", count_vowels(&s));\n'
                 '    println!("{s}");\n'
                 '    println!("{} {}", count_vowels("ЁЖ AEIOU"), count_vowels(""));\n'
                 '}\n',
       'hint': 's.chars() перебирает символы; to_lowercase() у char возвращает итератор — возьмите первый '
               'символ через .next().unwrap().',
       'expected': ['3', 'Привет, Rust', '6 0']},
      {'id': 'r16-add-all',
       'mode': 'rust',
       'title': '&mut Vec и срез: пишем через ссылку',
       'statement': 'Напишите add_all(dst: &mut Vec<i32>, extra: &[i32]): дописать в конец dst все элементы '
                    'среза extra (копируя числа). Вызывающий передаёт &mut v и &[..]: в вызове сразу видно, '
                    'кто читается, а кто меняется.',
       'starter': 'fn add_all(dst: &mut Vec<i32>, extra: &[i32]) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1];\n'
                 '    add_all(&mut v, &[2, 3]);\n'
                 '    add_all(&mut v, &[]);\n'
                 '    let more = vec![4, 5];\n'
                 '    add_all(&mut v, &more);\n'
                 '    println!("{:?} {:?}", v, more);\n'
                 '}\n',
       'hint': 'for &x in extra даёт числа по значению (i32 — Copy); затем dst.push(x).',
       'expected': ['[1, 2, 3, 4, 5] [4, 5]']},
      {'id': 'r16-swap-ends',
       'mode': 'rust',
       'title': 'Меняем концы среза',
       'statement': 'Напишите swap_ends(v: &mut [i32]): поменять местами первый и последний элементы среза. '
                    'Для пустого среза и среза из одного элемента ничего не делать. Функция должна принимать '
                    'и массив, и вектор, и часть вектора.',
       'starter': 'fn swap_ends(v: &mut [i32]) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = [1, 2, 3, 4];\n'
                 '    swap_ends(&mut a);\n'
                 '    let mut v = vec![10, 20, 30];\n'
                 '    swap_ends(&mut v);\n'
                 '    swap_ends(&mut v[1..]);\n'
                 '    let mut one = [7];\n'
                 '    swap_ends(&mut one);\n'
                 '    let mut none: [i32; 0] = [];\n'
                 '    swap_ends(&mut none);\n'
                 '    println!("{:?} {:?} {:?} {:?}", a, v, one, none);\n'
                 '}\n',
       'hint': 'У среза есть метод swap(i, j); не забудьте про длину меньше двух.',
       'expected': ['[4, 2, 3, 1] [30, 10, 20] [7] []']},
      {'id': 'r16-fix-two-mut',
       'mode': 'rust',
       'title': 'Исправьте: две изменяемые ссылки сразу',
       'statement': 'Компилятор не даёт держать две изменяемые ссылки на один вектор одновременно. Исправьте '
                    'build так, чтобы он возвращал [1, 2], оставив работу через &mut: заём должен '
                    'закончиться до того, как начнётся следующий.',
       'starter': 'fn build() -> Vec<i32> {\n'
                  '    let mut v = Vec::new();\n'
                  '    let a = &mut v;\n'
                  '    let b = &mut v;\n'
                  '    a.push(1);\n'
                  '    b.push(2);\n'
                  '    v\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{:?}", build());\n}\n',
       'hint': 'Первая ссылка живёт до последнего использования: используйте её полностью, и только потом '
               'берите вторую.',
       'expected': ['[1, 2]']},
      {'id': 'r16-fix-read-push',
       'mode': 'rust',
       'title': 'Исправьте: ссылка на элемент и push',
       'statement': 'grow_with_first должна дописать в конец вектора сначала число 100, а затем копию его '
                    'первого элемента. Код не компилируется: ссылка first ещё жива, когда вызывается '
                    'push(100). Исправьте минимально: число можно скопировать из-под ссылки.',
       'starter': 'fn grow_with_first(v: &mut Vec<i32>) {\n'
                  '    let first = &v[0];\n'
                  '    v.push(100);\n'
                  '    v.push(*first);\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![5, 7];\n'
                 '    grow_with_first(&mut v);\n'
                 '    println!("{:?}", v);\n'
                 '    grow_with_first(&mut v);\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'let first = v[0]; — i32 копируется, заём сразу заканчивается.',
       'expected': ['[5, 7, 100, 5]', '[5, 7, 100, 5, 100, 5]']},
      {'id': 'r16-fix-dangle',
       'mode': 'rust',
       'title': 'Исправьте: ссылка на локальную строку',
       'statement': 'greeting строит строку «Привет, <имя>!» и пытается вернуть ссылку на неё, но локальная '
                    'строка уничтожается при выходе из функции. Исправьте: верните владение, а не ссылку.',
       'starter': 'fn greeting(name: &str) -> &str {\n    let s = format!("Привет, {name}!");\n    &s\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", greeting("Rust"));\n'
                 '    let g = greeting("мир");\n'
                 '    println!("{} ({} байт)", g, g.len());\n'
                 '}\n',
       'hint': 'Тип результата — String; последнее выражение функции может быть самим format!.',
       'expected': ['Привет, Rust!', 'Привет, мир! (21 байт)']},
      {'id': 'r16-longest',
       'mode': 'rust',
       'title': 'Время жизни: longest',
       'statement': "Напишите longest<'a>(a: &'a str, b: &'a str) -> &'a str: вернуть более длинную строку "
                    '(по байтам); при равной длине — первую. Результат — ссылка на один из аргументов, а не '
                    'новая строка.',
       'starter': "fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {\n    todo!()\n}\n",
       'driver': 'fn main() {\n'
                 '    let s1 = String::from("abcd");\n'
                 '    let n;\n'
                 '    {\n'
                 '        let s2 = String::from("xyz");\n'
                 '        n = longest(&s1, &s2).len();\n'
                 '    }\n'
                 '    println!("{n}");\n'
                 '    println!("{} {}", longest("aa", "bb"), longest("привет", "hello"));\n'
                 '}\n',
       'hint': "Сравните len() и верните ту ссылку, которая подходит; аннотации 'a уже в сигнатуре.",
       'expected': ['4', 'aa привет']},
      {'id': 'r16-first-word',
       'mode': 'rust',
       'title': 'Срез первого слова',
       'statement': 'Напишите first_word(s: &str) -> &str: первое слово — подряд идущие непробельные '
                    'символы; ведущие пробельные символы пропускаются; если слов нет, вернуть пустую строку. '
                    'Результат — срез исходной строки, а не новая строка.',
       'starter': 'fn first_word(s: &str) -> &str {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["hello world", "  padded  text", "", "   ", "один", "тут много слов"] {\n'
                 '        println!("{:?}", first_word(s));\n'
                 '    }\n'
                 '    let owned = String::from("take me home");\n'
                 '    let w = first_word(&owned);\n'
                 '    println!("{} {}", w, w.as_ptr() == owned.as_ptr());\n'
                 '}\n',
       'hint': 'split_whitespace().next() возвращает Option<&str>; unwrap_or("") даёт пустой срез.',
       'expected': ['"hello"', '"padded"', '""', '""', '"один"', '"тут"', 'take true']},
      {'id': 'r16-lifetime-fix',
       'mode': 'rust',
       'title': 'Исправьте: нет времени жизни у результата',
       'statement': 'pick(a, b, first) возвращает a или b в зависимости от флага. Компилятор не знает, к '
                    'какому аргументу привязан результат. Допишите параметр времени жизни в сигнатуру.',
       'starter': 'fn pick(a: &str, b: &str, first: bool) -> &str {\n    if first { a } else { b }\n}\n',
       'driver': 'fn main() {\n'
                 '    let x = String::from("левая");\n'
                 '    let y = String::from("правая");\n'
                 '    println!("{} {}", pick(&x, &y, true), pick(&x, &y, false));\n'
                 '}\n',
       'hint': "fn pick<'a>(a: &'a str, b: &'a str, first: bool) -> &'a str.",
       'expected': ['левая правая']},
      {'id': 'r16-slice-split',
       'mode': 'rust',
       'title': 'Две половины одного среза',
       'statement': 'Напишите halves(v: &[i32]) -> (&[i32], &[i32]): левая половина длиной len/2 (округление '
                    'вниз) и остаток. Данные не копируются: обе части — срезы исходного.',
       'starter': 'fn halves(v: &[i32]) -> (&[i32], &[i32]) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let v = vec![1, 2, 3, 4, 5];\n'
                 '    let (l, r) = halves(&v);\n'
                 '    println!("{:?} {:?}", l, r);\n'
                 '    println!("{} {}", l.as_ptr() == v.as_ptr(), r.as_ptr() == v[2..].as_ptr());\n'
                 '    println!("{:?}", halves(&[]));\n'
                 '    println!("{:?}", halves(&[9]));\n'
                 '}\n',
       'hint': 'У среза есть метод split_at(mid), который возвращает пару срезов.',
       'expected': ['[1, 2] [3, 4, 5]', 'true true', '([], [])', '([], [9])']},
      {'id': 'r16-max-mut',
       'mode': 'rust',
       'title': 'Option<&mut T>: ссылка на максимум',
       'statement': 'Напишите max_mut(v: &mut [i32]) -> Option<&mut i32>: изменяемая ссылка на наибольший '
                    'элемент (None для пустого среза). Через неё вызывающий сможет записать в массив новое '
                    'значение.',
       'starter': 'fn max_mut(v: &mut [i32]) -> Option<&mut i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = [3, 9, 2];\n'
                 '    if let Some(m) = max_mut(&mut v) {\n'
                 '        *m = 0;\n'
                 '    }\n'
                 '    println!("{:?}", v);\n'
                 '    if let Some(m) = max_mut(&mut v) {\n'
                 '        *m += 100;\n'
                 '    }\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{:?}", max_mut(&mut []));\n'
                 '}\n',
       'hint': 'iter_mut() выдаёт &mut i32; max_by_key(|x| **x) выбирает наибольший, не копируя элементы.',
       'expected': ['[3, 0, 2]', '[103, 0, 2]', 'None']},
      {'id': 'r16-fix-nll',
       'mode': 'rust',
       'title': 'Исправьте: прочитали, а потом push',
       'statement': 'log_and_grow возвращает последний элемент вектора и добавляет в конец 100. Ссылка last '
                    'ещё нужна, когда вызывается push. Исправьте так, чтобы функция вернула последний '
                    'элемент ДО добавления (для [1, 2] вернуть 2).',
       'starter': 'fn log_and_grow(v: &mut Vec<i32>) -> i32 {\n'
                  '    let last = v.last().unwrap();\n'
                  '    v.push(100);\n'
                  '    *last\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2];\n'
                 '    println!("{}", log_and_grow(&mut v));\n'
                 '    println!("{}", log_and_grow(&mut v));\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'Достаточно разыменовать сразу: let last = *v.last().unwrap(); — заём закончится на этой '
               'строке.',
       'expected': ['2', '100', '[1, 2, 100, 100]']},
      {'id': 'r16-iter-kinds',
       'mode': 'rust',
       'title': 'Три способа обойти вектор',
       'statement': 'sum_ref(v: &Vec<i32>) → сумма (цикл по ссылке); double_in_place(v: &mut Vec<i32>) — '
                    'удвоить все элементы на месте (изменяемые ссылки); consume(v: Vec<i32>) → i32 — сумма с '
                    'забором элементов (вектор уничтожается).',
       'starter': 'fn sum_ref(v: &Vec<i32>) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn double_in_place(v: &mut Vec<i32>) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn consume(v: Vec<i32>) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2, 3];\n'
                 '    println!("{}", sum_ref(&v));\n'
                 '    double_in_place(&mut v);\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{}", consume(v));\n'
                 '}\n',
       'hint': 'for x in v (v: &Vec) даёт &i32; v.iter_mut() — &mut i32 (значение меняют через *x); for x in '
               'v (v: Vec) — i32.',
       'expected': ['6', '[2, 4, 6]', '12']},
      {'id': 'r16-parser',
       'mode': 'rust',
       'title': "Структура со ссылкой: Parser<'a>",
       'statement': 'Parser хранит срез текста и позицию. Parser::new(text) создаёт разборщик; '
                    'next_word(&mut self) возвращает следующее слово (непробельные символы) как срез '
                    'ИСХОДНОГО текста или None, когда слов больше нет. Слова должны жить столько же, сколько '
                    "текст, а не столько, сколько сам разборщик (&'a str в результате).",
       'starter': "struct Parser<'a> {\n"
                  "    text: &'a str,\n"
                  '    pos: usize,\n'
                  '}\n'
                  '\n'
                  "impl<'a> Parser<'a> {\n"
                  "    fn new(text: &'a str) -> Parser<'a> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  "    fn next_word(&mut self) -> Option<&'a str> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let text = String::from("  hello   rust world ");\n'
                 '    let mut words = Vec::new();\n'
                 '    {\n'
                 '        let mut p = Parser::new(&text);\n'
                 '        while let Some(w) = p.next_word() {\n'
                 '            words.push(w);\n'
                 '        }\n'
                 '    }\n'
                 '    println!("{:?}", words);\n'
                 '    let mut q = Parser::new("привет мир");\n'
                 '    println!("{:?} {:?} {:?}", q.next_word(), q.next_word(), q.next_word());\n'
                 '    println!("{:?}", Parser::new("   ").next_word());\n'
                 '}\n',
       'hint': 'Ищите начало слова после trim_start, конец — по первому пробельному символу; сдвигайте '
               'self.pos за слово.',
       'expected': ['["hello", "rust", "world"]', 'Some("привет") Some("мир") None', 'None']},
      {'id': 'r16-method-forms',
       'mode': 'rust',
       'title': 'Три формы self',
       'statement': 'Counter считает события. new() — со нулём; get(&self) читает значение; inc(&mut self) '
                    'увеличивает на 1; finish(self) забирает счётчик и возвращает итог. Выберите для каждого '
                    'метода нужную форму: после finish использовать счётчик уже нельзя.',
       'starter': 'struct Counter {\n'
                  '    n: u32,\n'
                  '}\n'
                  '\n'
                  'impl Counter {\n'
                  '    fn new() -> Counter {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn get(&self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn inc(&mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn finish(self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut c = Counter::new();\n'
                 '    println!("{}", c.get());\n'
                 '    c.inc();\n'
                 '    c.inc();\n'
                 '    c.inc();\n'
                 '    println!("{}", c.get());\n'
                 '    println!("{}", c.finish());\n'
                 '}\n',
       'hint': 'Сигнатуры уже даны: &self читает, &mut self меняет поле через self.n += 1, self передаёт '
               'поле дальше.',
       'expected': ['0', '3', '3']},
      {'id': 'r16-fix-method-self',
       'mode': 'rust',
       'title': 'Исправьте: метод меняет поле через &self',
       'statement': 'add должен увеличить количество монет, но метод принимает &self — менять поле через '
                    'разделяемую ссылку нельзя. Исправьте сигнатуру метода (вызывающий код уже использует '
                    'let mut).',
       'starter': 'struct Wallet {\n'
                  '    coins: u32,\n'
                  '}\n'
                  '\n'
                  'impl Wallet {\n'
                  '    fn add(&self, n: u32) {\n'
                  '        self.coins += n;\n'
                  '    }\n'
                  '\n'
                  '    fn total(&self) -> u32 {\n'
                  '        self.coins\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut w = Wallet { coins: 1 };\n'
                 '    w.add(4);\n'
                 '    w.add(5);\n'
                 '    println!("{}", w.total());\n'
                 '}\n',
       'hint': 'fn add(&mut self, n: u32) — изменяемая ссылка на self.',
       'expected': ['10']},
      {'id': 'r16-swap-values',
       'mode': 'rust',
       'title': 'Обмен через две &mut без mem::swap',
       'statement': 'Напишите swap_values(a: &mut i32, b: &mut i32): поменять значения местами, не используя '
                    'std::mem::swap и метод swap. Две &mut на РАЗНЫЕ значения проверщик допускает; в '
                    'вызывающем коде обе переменные объявлены mut.',
       'starter': 'fn swap_values(a: &mut i32, b: &mut i32) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!("sw", "ap(")).count();\n'
                 '    let mut x = 1;\n'
                 '    let mut y = 2;\n'
                 '    swap_values(&mut x, &mut y);\n'
                 '    println!("{x} {y}");\n'
                 '    swap_values(&mut x, &mut y);\n'
                 '    println!("{x} {y}");\n'
                 '    println!("swap calls: {}", bad0);\n'
                 '}\n',
       'hint': 'Нужна временная переменная: tmp = *a; *a = *b; *b = tmp;',
       'expected': ['2 1', '1 2', 'swap calls: 0']},
      {'id': 'r16-reborrow',
       'mode': 'rust',
       'title': 'Перезаимствование: передаём &mut дальше',
       'statement': 'bump(x: &mut i32) прибавляет единицу — он уже готов. Напишите bump_n(x: &mut i32, n: '
                    'u32): вызвать bump ровно n раз с тем же x. &mut не копируется, но передача в функцию '
                    'создаёт временный заём, и x можно использовать снова.',
       'starter': 'fn bump(x: &mut i32) {\n'
                  '    *x += 1;\n'
                  '}\n'
                  '\n'
                  'fn bump_n(x: &mut i32, n: u32) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = 10;\n'
                 '    bump_n(&mut v, 5);\n'
                 '    println!("{v}");\n'
                 '    bump_n(&mut v, 0);\n'
                 '    bump(&mut v);\n'
                 '    println!("{v}");\n'
                 '}\n',
       'hint': 'В цикле просто пишите bump(x); — каждый вызов заимствует x на время вызова.',
       'expected': ['15', '16']},
      {'id': 'r16-split-halves-mut',
       'mode': 'rust',
       'title': 'split_at_mut: два писателя, разные части',
       'statement': 'Напишите reshape(v: &mut [i32]): левую половину (len/2 элементов) обнулить, а каждый '
                    'элемент правой половины заменить суммой соответствующих исходных элементов левой и '
                    'правой (для пары i: right[i] = left_old[i] + right_old[i]; если правая половина '
                    'длиннее, лишний последний остаётся прежним). Используйте split_at_mut: две изменяемые '
                    'ссылки на непересекающиеся части разрешены.',
       'starter': 'fn reshape(v: &mut [i32]) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = [1, 2, 3, 4, 5, 6];\n'
                 '    reshape(&mut a);\n'
                 '    println!("{:?}", a);\n'
                 '    let mut b = vec![5, 6, 7];\n'
                 '    reshape(&mut b);\n'
                 '    println!("{:?}", b);\n'
                 '    let mut c: Vec<i32> = vec![];\n'
                 '    reshape(&mut c);\n'
                 '    println!("{:?}", c);\n'
                 '}\n',
       'hint': 'let (left, right) = v.split_at_mut(mid); — обе части можно менять одновременно.',
       'expected': ['[0, 0, 0, 5, 7, 9]', '[0, 11, 7]', '[]']},
      {'id': 'r16-fix-iter-invalidate',
       'mode': 'rust',
       'title': 'Исправьте: изменяем вектор во время обхода',
       'statement': 'dup_evens дописывает в конец вектора копии всех чётных чисел (порядок: исходные '
                    'элементы, затем копии чётных в исходном порядке). Цикл по &v держит заём, а push меняет '
                    'вектор — не компилируется. Исправьте: сначала соберите копии, потом добавьте.',
       'starter': 'fn dup_evens(mut v: Vec<i32>) -> Vec<i32> {\n'
                  '    for x in &v {\n'
                  '        if x % 2 == 0 {\n'
                  '            v.push(*x);\n'
                  '        }\n'
                  '    }\n'
                  '    v\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", dup_evens(vec![1, 2, 3, 4]));\n'
                 '    println!("{:?}", dup_evens(vec![]));\n'
                 '    println!("{:?}", dup_evens(vec![7, 9]));\n'
                 '}\n',
       'hint': 'Заведите отдельный вектор extra, заполните его в цикле, а после цикла вызовите '
               'v.extend(extra).',
       'expected': ['[1, 2, 3, 4, 2, 4]', '[]', '[7, 9]']},
      {'id': 'r16-initial-char',
       'mode': 'rust',
       'title': 'Срез по границе символа',
       'statement': 'initial(s: &str) -> &str возвращает первый символ строки как срез (пустая строка → '
                    'пустой срез). Заготовка берёт один БАЙТ и падает на кириллице: границы среза обязаны '
                    'попадать на границу символа UTF-8. Исправьте.',
       'starter': 'fn initial(s: &str) -> &str {\n    &s[..1]\n}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["rust", "привет", "Ёж", "", "я"] {\n'
                 '        println!("{:?}", initial(s));\n'
                 '    }\n'
                 '}\n',
       'hint': 'char_indices() выдаёт пары (байтовое смещение, символ): смещение второго символа — конец '
               'первого; если второго нет, подойдёт вся строка.',
       'expected': ['"r"', '"п"', '"Ё"', '""', '"я"']},
      {'id': 'r16-stack-addr',
       'mode': 'rust',
       'title': 'Стек растёт вниз',
       'statement': 'Напишите inner(outer: usize) -> bool с атрибутом #[inline(never)]: заведите локальную '
                    'переменную, получите её адрес (as *const u64 as usize) и верните, меньше ли он адреса '
                    'outer. И grows_down() -> bool: локальная переменная, её адрес передаётся в inner. '
                    'Результат должен быть true: кадр вложенного вызова лежит ниже. Значения оберните в '
                    'std::hint::black_box, чтобы оптимизатор их не убрал.',
       'starter': '#[inline(never)]\n'
                  'fn inner(outer: usize) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn grows_down() -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{}", grows_down());\n}\n',
       'hint': 'let y = black_box(0u64); let ay = &y as *const u64 as usize; — то же в grows_down; в inner '
               'сравнивайте ay < outer.',
       'expected': ['true']},
      {'id': 'r16-ptr-eq',
       'mode': 'rust',
       'title': 'Равны значения или это один объект',
       'statement': 'same_text(a, b) — true, если строки равны по содержимому (==). same_object(a, b) — '
                    'true, только если обе ссылки указывают на ОДИН объект в памяти (std::ptr::eq). Это '
                    'аналоги == и is из питона.',
       'starter': 'fn same_text(a: &String, b: &String) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn same_object(a: &String, b: &String) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let x = String::from("hi");\n'
                 '    let y = String::from("hi");\n'
                 '    println!("{} {}", same_text(&x, &y), same_object(&x, &y));\n'
                 '    println!("{} {}", same_text(&x, &x), same_object(&x, &x));\n'
                 '}\n',
       'hint': 'a == b сравнивает значения за ссылками; ptr::eq(a, b) — сами адреса.',
       'expected': ['true false', 'true true']},
      {'id': 'r16-trim-all',
       'mode': 'rust',
       'title': 'Срезы в векторе: trim_all',
       'statement': "Напишите trim_all<'a>(lines: &[&'a str]) -> Vec<&'a str>: вектор срезов, каждый обрезан "
                    'по краям от пробельных символов. Новых строк не создаётся — только срезы исходных '
                    "строк, поэтому результат живёт столько же, сколько исходные тексты (время жизни 'a).",
       'starter': "fn trim_all<'a>(lines: &[&'a str]) -> Vec<&'a str> {\n    todo!()\n}\n",
       'driver': 'fn main() {\n'
                 '    let text = String::from("  alpha \\n beta\\t");\n'
                 "    let parts: Vec<&str> = text.split('\\n').collect();\n"
                 '    let t = trim_all(&parts);\n'
                 '    println!("{:?}", t);\n'
                 '    println!("{:?}", trim_all(&["  ", "x ", ""]));\n'
                 '}\n',
       'hint': "s.trim() у &'a str возвращает &'a str; соберите результат через map(...).collect().",
       'expected': ['["alpha", "beta"]', '["", "x", ""]']},
      {'id': 'r16-longest-word',
       'mode': 'rust',
       'title': 'Самое длинное слово',
       'statement': 'Напишите longest_word(text: &str) -> &str: самое длинное слово текста (слова разделены '
                    'пробельными символами; длина — в символах, не в байтах; при равенстве — первое; пустой '
                    'текст → ""). Верните срез текста.',
       'starter': 'fn longest_word(text: &str) -> &str {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", longest_word("a bb ccc dd"));\n'
                 '    println!("{:?}", longest_word("привет мир кот"));\n'
                 '    println!("{:?}", longest_word("ab cd"));\n'
                 '    println!("{:?}", longest_word("  "));\n'
                 '}\n',
       'hint': 'Храните лучший срез в переменной типа &str и заменяйте её, когда нашли слово длиннее по '
               'chars().count().',
       'expected': ['"ccc"', '"привет"', '"ab"', '""']},
      {'id': 'r16-struct-ref-fix',
       'mode': 'rust',
       'title': 'Исправьте: у структуры со ссылкой нет времени жизни',
       'statement': 'Highlight хранит срез текста и смещение, mark(text, from, to) строит выделение. '
                    'Компилятор требует указать время жизни. Допишите параметры в определение структуры и в '
                    'сигнатуру функции.',
       'starter': 'struct Highlight {\n'
                  '    text: &str,\n'
                  '    start: usize,\n'
                  '}\n'
                  '\n'
                  'fn mark(text: &str, from: usize, to: usize) -> Highlight {\n'
                  '    Highlight { text: &text[from..to], start: from }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let doc = String::from("borrow checker is strict");\n'
                 '    let h = mark(&doc, 7, 14);\n'
                 '    println!("{} @ {}", h.text, h.start);\n'
                 '}\n',
       'hint': "struct Highlight<'a> { text: &'a str, … } и fn mark<'a>(text: &'a str, …) -> Highlight<'a>.",
       'expected': ['checker @ 7']},
      {'id': 'r16-fix-outlive',
       'mode': 'rust',
       'title': 'Исправьте: значение живёт недостаточно долго',
       'statement': 'outer_len сравнивает входную строку с временной строкой и возвращает длину большей. '
                    'Ссылка result переживает временную строку b, и компилятор отказывается собирать код. '
                    'Исправьте, не меняя longest и не выводя b за пределы блока: длину нужно взять, пока b '
                    'ещё жива.',
       'starter': "fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {\n"
                  '    if a.len() >= b.len() { a } else { b }\n'
                  '}\n'
                  '\n'
                  'fn outer_len(a: &str) -> usize {\n'
                  '    let result;\n'
                  '    {\n'
                  '        let b = String::from("temporary");\n'
                  '        result = longest(a, &b);\n'
                  '    }\n'
                  '    result.len()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", outer_len("hi"));\n'
                 '    println!("{}", outer_len("a longer phrase here"));\n'
                 '}\n',
       'hint': 'Замените result на число: n = longest(a, &b).len(); внутри блока.',
       'expected': ['9', '20']},
      {'id': 'r16-longest-row',
       'mode': 'rust',
       'title': 'Ссылка на самую длинную строку сетки',
       'statement': 'grid — вектор строк (векторов). longest_row(grid: &[Vec<i32>]) -> Option<&Vec<i32>> '
                    'возвращает ссылку на самую длинную строку (при равенстве — первую; пустая сетка → '
                    'None). push_to_longest(grid: &mut [Vec<i32>], x) добавляет x в конец той же самой '
                    'строки (первой из самых длинных).',
       'starter': 'fn longest_row(grid: &[Vec<i32>]) -> Option<&Vec<i32>> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn push_to_longest(grid: &mut [Vec<i32>], x: i32) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut grid = vec![vec![1], vec![2, 3], vec![4, 5], vec![]];\n'
                 '    println!("{:?}", longest_row(&grid));\n'
                 '    push_to_longest(&mut grid, 9);\n'
                 '    println!("{:?}", grid);\n'
                 '    println!("{:?}", longest_row(&[]));\n'
                 '    let mut empty: Vec<Vec<i32>> = vec![];\n'
                 '    push_to_longest(&mut empty, 1);\n'
                 '    println!("{:?}", empty);\n'
                 '}\n',
       'hint': 'Для push нужен индекс: найдите его читающим обходом (заём закончится), а потом возьмите &mut '
               'grid[i].',
       'expected': ['Some([2, 3])', '[[1], [2, 3, 9], [4, 5], []]', 'None', '[]']},
      {'id': 'r16-first-negative',
       'mode': 'rust',
       'title': 'Option<&mut i32>: первое отрицательное',
       'statement': 'Напишите first_negative(v: &mut [i32]) -> Option<&mut i32>: изменяемая ссылка на первый '
                    'отрицательный элемент (None, если таких нет). Через неё вызывающий исправляет значение '
                    'прямо в массиве.',
       'starter': 'fn first_negative(v: &mut [i32]) -> Option<&mut i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = [3, -1, 4, -5];\n'
                 '    while let Some(x) = first_negative(&mut v) {\n'
                 '        *x = 0;\n'
                 '    }\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{:?}", first_negative(&mut [1, 2]));\n'
                 '}\n',
       'hint': 'iter_mut().find(|x| **x < 0): в замыкании x имеет тип &&mut i32, поэтому две звёздочки.',
       'expected': ['[3, 0, 4, 0]', 'None']},
      {'id': 'r16-fix-report',
       'mode': 'rust',
       'title': 'Исправьте: ссылка на первый элемент и clear',
       'statement': 'report(names) возвращает строку «первое — <имя>; осталось <N>» и очищает вектор. Ссылка '
                    'first на элемент вектора ещё нужна, когда вектор очищается. Исправьте: сделайте '
                    'независимую копию имени.',
       'starter': 'fn report(names: &mut Vec<String>) -> String {\n'
                  '    let first = &names[0];\n'
                  '    names.clear();\n'
                  '    format!("первое — {}; осталось {}", first, names.len())\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut names = vec![String::from("anna"), String::from("bob")];\n'
                 '    println!("{}", report(&mut names));\n'
                 '    println!("{:?}", names);\n'
                 '}\n',
       'hint': 'names[0].clone() даёт новую String, не связанную с вектором.',
       'expected': ['первое — anna; осталось 0', '[]']}]}
