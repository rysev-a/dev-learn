//! Подсветка кода по строкам: лексер без зависимостей. Виды токенов отображаются в цвета темы (`--s-*`) там, где их рисуют:
//! в схемах слайдов (`scene`) и в редакторе упражнений.

/// Язык врезки кода. В данных слайдов записывается строчными буквами (`"rust"`, `"python"`, `"sql"` …).
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize), serde(rename_all = "lowercase"))]
pub enum Lang {
    #[default]
    Plain,
    Python,
    C,
    Asm,
    Rust,
    Sql,
    Js,
    Css,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    Plain,
    Comment,
    Str,
    Number,
    Keyword,
    /// встроенные функции, типы, регистры
    Builtin,
    /// вызываемые имена, директивы, метки
    Accent,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Token {
    pub text: String,
    pub kind: Kind,
}

impl Kind {
    /// Цвет токена (`None` — обычный цвет строки).
    pub fn css(self) -> Option<&'static str> {
        match self {
            Kind::Plain => None,
            Kind::Comment => Some("var(--s-muted)"),
            Kind::Str => Some("var(--s-amber)"),
            Kind::Number => Some("var(--s-red)"),
            Kind::Keyword => Some("var(--s-blue)"),
            Kind::Builtin => Some("var(--s-violet)"),
            Kind::Accent => Some("var(--s-accent)"),
        }
    }
}

const PY_KW: &str = "def class if elif else for while in not and or return import from as with try except finally raise lambda yield pass break continue None True False is del global async await";
const PY_BI: &str = "print len range int str float bool list dict set tuple type input sum max min sorted enumerate zip open abs round self isinstance";
const RS_KW: &str = "fn let mut pub struct enum impl match if else for while loop return use mod self Self move const static type where async await unsafe trait dyn in as break continue ref";
const RS_TY: &str = "i8 i16 i32 i64 i128 isize u8 u16 u32 u64 u128 usize f32 f64 bool char str String Vec Option Result Box Rc Arc RefCell HashMap Some None Ok Err";
const C_KW: &str = "if else for while do switch case default break continue return goto sizeof typedef struct union enum static const volatile extern register inline restrict";
const SQL_KW: &str = "select from where group by having order limit offset join inner left right full outer cross on using as and or not in is null like between exists case when then else end union all distinct insert into values update set delete create table index primary key foreign references unique check default begin commit rollback with recursive over partition returning asc desc explain analyze view alter add drop column constraint if true false cascade";
const SQL_FN: &str = "count sum avg min max coalesce nullif round length lower upper substr row_number rank dense_rank lag lead now date strftime cast";
const JS_KW: &str = "const let var function return if else for while do switch case default break continue new class extends super this typeof instanceof in of import export from async await try catch finally throw yield static get set delete void";
const JS_LIT: &str = "true false null undefined NaN Infinity";
const C_TY: &str = "int char short long float double void unsigned signed size_t ssize_t ptrdiff_t bool FILE NULL true false uint8_t uint16_t uint32_t uint64_t int8_t int16_t int32_t int64_t uintptr_t";

fn has(set: &str, word: &str) -> bool {
    set.split(' ').any(|w| w == word)
}

fn is_word_start(c: char) -> bool {
    c.is_ascii_alphabetic() || c == '_'
}

fn is_word(c: char) -> bool {
    c.is_ascii_alphanumeric() || c == '_'
}

/// Курсор по символам строки.
struct Scan<'a> {
    chars: Vec<char>,
    pos: usize,
    out: Vec<Token>,
    _src: &'a str,
}

impl<'a> Scan<'a> {
    fn new(src: &'a str) -> Self {
        Self { chars: src.chars().collect(), pos: 0, out: Vec::new(), _src: src }
    }
    fn peek(&self, off: usize) -> Option<char> {
        self.chars.get(self.pos + off).copied()
    }
    fn done(&self) -> bool {
        self.pos >= self.chars.len()
    }
    fn take_while(&mut self, f: impl Fn(char) -> bool) -> String {
        let start = self.pos;
        while self.peek(0).is_some_and(&f) {
            self.pos += 1;
        }
        self.chars[start..self.pos].iter().collect()
    }
    fn rest(&mut self) -> String {
        let s: String = self.chars[self.pos..].iter().collect();
        self.pos = self.chars.len();
        s
    }
    fn push(&mut self, text: String, kind: Kind) {
        if text.is_empty() {
            return;
        }
        // подряд идущие обычные куски склеиваются: меньше узлов в SVG
        if kind == Kind::Plain {
            if let Some(last) = self.out.last_mut().filter(|t| t.kind == Kind::Plain) {
                last.text.push_str(&text);
                return;
            }
        }
        self.out.push(Token { text, kind });
    }
    /// Строка в кавычках `q` с экранированием; незакрытая тянется до конца строки.
    fn quoted(&mut self, prefix: String, q: char) -> String {
        let mut s = prefix;
        s.push(q);
        self.pos += 1;
        while let Some(c) = self.peek(0) {
            s.push(c);
            self.pos += 1;
            if c == '\\' {
                if let Some(n) = self.peek(0) {
                    s.push(n);
                    self.pos += 1;
                }
            } else if c == q {
                break;
            }
        }
        s
    }
    /// Число: десятичное или `0x…`, затем суффиксы (если указаны); следом не должно идти слово (иначе это не число).
    fn number(&mut self, allow_dot: bool, hex: bool, suffix: &str, underscores: bool) -> Option<String> {
        let start = self.pos;
        if hex && self.peek(0) == Some('0') && matches!(self.peek(1), Some('x' | 'X')) && self.peek(2).is_some_and(|c| c.is_ascii_hexdigit()) {
            self.pos += 2;
            self.take_while(|c| c.is_ascii_hexdigit());
        } else {
            self.take_while(|c| c.is_ascii_digit() || (underscores && c == '_'));
            if allow_dot && self.peek(0) == Some('.') && self.peek(1).is_some_and(|c| c.is_ascii_digit()) {
                self.pos += 1;
                self.take_while(|c| c.is_ascii_digit());
            }
        }
        self.take_while(|c| suffix.contains(c));
        if self.peek(0).is_some_and(is_word) {
            self.pos = start;
            return None;
        }
        Some(self.chars[start..self.pos].iter().collect())
    }
}

fn python(src: &str) -> Vec<Token> {
    let mut sc = Scan::new(src);
    while !sc.done() {
        let c = sc.peek(0).unwrap_or(' ');
        let prev_word = sc.pos > 0 && is_word(sc.chars[sc.pos - 1]);
        if c == '#' {
            let t = sc.rest();
            sc.push(t, Kind::Comment);
        } else if c == '"' || c == '\'' {
            let s = sc.quoted(String::new(), c);
            sc.push(s, Kind::Str);
        } else if matches!(c, 'f' | 'F' | 'r' | 'R' | 'b' | 'B') && matches!(sc.peek(1), Some('"' | '\'')) && !prev_word {
            let q = sc.peek(1).unwrap_or('"');
            sc.pos += 1;
            let s = sc.quoted(c.to_string(), q);
            sc.push(s, Kind::Str);
        } else if c.is_ascii_digit() && !prev_word {
            match sc.number(true, false, "", true) {
                Some(n) => sc.push(n, Kind::Number),
                None => {
                    sc.pos += 1;
                    sc.push(c.to_string(), Kind::Plain);
                }
            }
        } else if is_word_start(c) {
            let w = sc.take_while(is_word);
            let kind = if has(PY_KW, &w) {
                Kind::Keyword
            } else if has(PY_BI, &w) {
                Kind::Builtin
            } else if sc.peek(0) == Some('(') {
                Kind::Accent
            } else {
                Kind::Plain
            };
            sc.push(w, kind);
        } else {
            sc.pos += 1;
            sc.push(c.to_string(), Kind::Plain);
        }
    }
    sc.out
}

/// Rust: ключевые слова, типы (и любые имена с заглавной), макросы `name!`, времена жизни `'a`.
fn rust(src: &str) -> Vec<Token> {
    let mut sc = Scan::new(src);
    while !sc.done() {
        let c = sc.peek(0).unwrap_or(' ');
        let prev_word = sc.pos > 0 && is_word(sc.chars[sc.pos - 1]);
        if c == '/' && sc.peek(1) == Some('/') {
            let t = sc.rest();
            sc.push(t, Kind::Comment);
        } else if c == '"' {
            let s = sc.quoted(String::new(), c);
            sc.push(s, Kind::Str);
        } else if c == '\'' && sc.peek(1).is_some_and(is_word_start) && !prev_word {
            // время жизни `'a`, но не символ `'a'`
            let start = sc.pos;
            sc.pos += 1;
            sc.take_while(is_word);
            if sc.peek(0) == Some('\'') {
                sc.pos += 1;
                let t: String = sc.chars[start..sc.pos].iter().collect();
                sc.push(t, Kind::Str);
            } else {
                let t: String = sc.chars[start..sc.pos].iter().collect();
                sc.push(t, Kind::Builtin);
            }
        } else if c == '\'' {
            let s = sc.quoted(String::new(), c);
            sc.push(s, Kind::Str);
        } else if c.is_ascii_digit() && !prev_word {
            match sc.number(true, false, "", true) {
                Some(n) => sc.push(n, Kind::Number),
                None => {
                    sc.pos += 1;
                    sc.push(c.to_string(), Kind::Plain);
                }
            }
        } else if is_word_start(c) {
            let mut w = sc.take_while(is_word);
            let kind = if sc.peek(0) == Some('!') {
                w.push('!');
                sc.pos += 1;
                Kind::Accent
            } else if has(RS_KW, &w) {
                Kind::Keyword
            } else if has(RS_TY, &w) || w.chars().next().is_some_and(|ch| ch.is_ascii_uppercase()) {
                Kind::Builtin
            } else {
                Kind::Plain
            };
            sc.push(w, kind);
        } else {
            sc.pos += 1;
            sc.push(c.to_string(), Kind::Plain);
        }
    }
    sc.out
}

fn c_lang(src: &str) -> Vec<Token> {
    let mut sc = Scan::new(src);
    // директива препроцессора: в начале строки `#include`, `#define` …
    let indent = src.chars().take_while(|c| c.is_whitespace()).count();
    if src.chars().nth(indent) == Some('#') {
        sc.pos = indent;
        sc.pos += 1;
        sc.take_while(char::is_whitespace);
        sc.take_while(is_word);
        let head: String = sc.chars[..sc.pos].iter().collect();
        let (lead, directive) = head.split_at(head.len().min(indent));
        sc.push(lead.to_string(), Kind::Plain);
        sc.push(directive.to_string(), Kind::Accent);
    }
    while !sc.done() {
        let c = sc.peek(0).unwrap_or(' ');
        let prev_word = sc.pos > 0 && is_word(sc.chars[sc.pos - 1]);
        if c == '/' && sc.peek(1) == Some('/') {
            let t = sc.rest();
            sc.push(t, Kind::Comment);
        } else if c == '/' && sc.peek(1) == Some('*') {
            let start = sc.pos;
            sc.pos += 2;
            while !sc.done() && !(sc.peek(0) == Some('*') && sc.peek(1) == Some('/')) {
                sc.pos += 1;
            }
            sc.pos = (sc.pos + 2).min(sc.chars.len());
            let t: String = sc.chars[start..sc.pos].iter().collect();
            sc.push(t, Kind::Comment);
        } else if c == '"' || c == '\'' {
            let s = sc.quoted(String::new(), c);
            sc.push(s, Kind::Str);
        } else if c.is_ascii_digit() && !prev_word {
            match sc.number(false, true, "uUlL", false) {
                Some(n) => sc.push(n, Kind::Number),
                None => {
                    sc.pos += 1;
                    sc.push(c.to_string(), Kind::Plain);
                }
            }
        } else if is_word_start(c) {
            let w = sc.take_while(is_word);
            let kind = if has(C_KW, &w) {
                Kind::Keyword
            } else if has(C_TY, &w) || w.ends_with("_t") {
                Kind::Builtin
            } else {
                Kind::Plain
            };
            sc.push(w, kind);
        } else {
            sc.pos += 1;
            sc.push(c.to_string(), Kind::Plain);
        }
    }
    sc.out
}

fn is_asm_register(w: &str) -> bool {
    matches!(w, "zero" | "ra" | "sp" | "gp" | "tp" | "fp" | "pc")
        || {
            let (head, tail) = w.split_at(w.len().min(1));
            matches!(head, "x" | "f" | "a") && !tail.is_empty() && tail.chars().all(|c| c.is_ascii_digit())
        }
        || {
            let (head, tail) = w.split_at(w.len().min(1));
            head == "t" && matches!(tail, "0" | "1" | "2" | "3" | "4" | "5" | "6")
        }
        || {
            let (head, tail) = w.split_at(w.len().min(1));
            head == "s" && matches!(tail, "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10" | "11")
        }
}

/// Ассемблер RISC-V: первое слово строки — инструкция, регистры, директивы `.name`, метки `name:`.
fn asm(src: &str) -> Vec<Token> {
    let mut sc = Scan::new(src);
    let indent = src.chars().take_while(|c| c.is_whitespace()).count();
    // метка в начале строки: `loop:` / `.L1:`
    let label_len = src[src.char_indices().nth(indent).map_or(src.len(), |(i, _)| i)..].find(':').filter(|n| {
        let head = &src[src.char_indices().nth(indent).map_or(src.len(), |(i, _)| i)..][..*n];
        !head.is_empty() && head.chars().all(|c| is_word(c) || c == '.' || c == '$')
    });
    let first_instruction = true;
    let mut first = first_instruction;
    if let Some(n) = label_len {
        let upto = indent + src.chars().skip(indent).take(n + 1).count();
        let head: String = sc.chars[..upto].iter().collect();
        let (lead, label) = head.split_at(indent);
        sc.push(lead.to_string(), Kind::Plain);
        sc.push(label.to_string(), Kind::Accent);
        sc.pos = upto; // после метки на той же строке может идти инструкция: `first` остаётся истинным
    }
    while !sc.done() {
        let c = sc.peek(0).unwrap_or(' ');
        let neg_num = c == '-' && sc.peek(1).is_some_and(|d| d.is_ascii_digit());
        if c == '#' {
            let t = sc.rest();
            sc.push(t, Kind::Comment);
        } else if (c.is_ascii_digit() || neg_num) && !(sc.pos > 0 && is_word(sc.chars[sc.pos - 1])) {
            let start = sc.pos;
            if neg_num {
                sc.pos += 1;
            }
            match sc.number(false, true, "", false) {
                Some(n) => {
                    let sign: String = sc.chars[start..sc.pos - n.chars().count()].iter().collect();
                    sc.push(format!("{sign}{n}"), Kind::Number);
                }
                None => {
                    sc.pos = start + 1;
                    sc.push(c.to_string(), Kind::Plain);
                }
            }
        } else if is_word_start(c) || c == '.' {
            let w = sc.take_while(|ch| is_word(ch) || ch == '.');
            let kind = if is_asm_register(&w) {
                Kind::Builtin
            } else if first {
                Kind::Keyword
            } else if w.starts_with('.') {
                Kind::Accent
            } else {
                Kind::Plain
            };
            first = false;
            sc.push(w, kind);
        } else {
            sc.pos += 1;
            sc.push(c.to_string(), Kind::Plain);
        }
    }
    sc.out
}

/// SQL: ключевые слова (без учёта регистра) и функции; комментарии `--`, строки `'…'` с удвоенной кавычкой.
fn sql(src: &str) -> Vec<Token> {
    let mut sc = Scan::new(src);
    while !sc.done() {
        let c = sc.peek(0).unwrap_or(' ');
        let prev_word = sc.pos > 0 && is_word(sc.chars[sc.pos - 1]);
        if c == '-' && sc.peek(1) == Some('-') {
            let t = sc.rest();
            sc.push(t, Kind::Comment);
        } else if c == '\'' {
            // `''` внутри строки — одна кавычка
            let mut t = String::from("'");
            sc.pos += 1;
            while let Some(ch) = sc.peek(0) {
                t.push(ch);
                sc.pos += 1;
                if ch == '\'' {
                    if sc.peek(0) == Some('\'') {
                        t.push('\'');
                        sc.pos += 1;
                    } else {
                        break;
                    }
                }
            }
            sc.push(t, Kind::Str);
        } else if c.is_ascii_digit() && !prev_word {
            match sc.number(true, false, "", false) {
                Some(n) => sc.push(n, Kind::Number),
                None => {
                    sc.pos += 1;
                    sc.push(c.to_string(), Kind::Plain);
                }
            }
        } else if is_word_start(c) {
            let w = sc.take_while(is_word);
            let lower = w.to_lowercase();
            let kind = if has(SQL_KW, &lower) {
                Kind::Keyword
            } else if has(SQL_FN, &lower) {
                Kind::Builtin
            } else {
                Kind::Plain
            };
            sc.push(w, kind);
        } else {
            sc.pos += 1;
            sc.push(c.to_string(), Kind::Plain);
        }
    }
    sc.out
}

/// JavaScript: ключевые слова, литералы (цветом чисел), имена с заглавной (классы), стрелка `=>`.
fn js(src: &str) -> Vec<Token> {
    let mut sc = Scan::new(src);
    while !sc.done() {
        let c = sc.peek(0).unwrap_or(' ');
        let prev_word = sc.pos > 0 && (is_word(sc.chars[sc.pos - 1]) || sc.chars[sc.pos - 1] == '$');
        if c == '/' && sc.peek(1) == Some('/') {
            let t = sc.rest();
            sc.push(t, Kind::Comment);
        } else if c == '"' || c == '\'' || c == '`' {
            let s = sc.quoted(String::new(), c);
            sc.push(s, Kind::Str);
        } else if c == '=' && sc.peek(1) == Some('>') {
            sc.pos += 2;
            sc.push("=>".into(), Kind::Accent);
        } else if c.is_ascii_digit() && !prev_word {
            match sc.number(true, false, "n", true) {
                Some(n) => sc.push(n, Kind::Number),
                None => {
                    sc.pos += 1;
                    sc.push(c.to_string(), Kind::Plain);
                }
            }
        } else if is_word_start(c) || c == '$' {
            let w = sc.take_while(|ch| is_word(ch) || ch == '$');
            let kind = if has(JS_KW, &w) {
                Kind::Keyword
            } else if has(JS_LIT, &w) {
                Kind::Number
            } else if w.chars().next().is_some_and(|ch| ch.is_ascii_uppercase()) {
                Kind::Builtin
            } else {
                Kind::Plain
            };
            sc.push(w, kind);
        } else {
            sc.pos += 1;
            sc.push(c.to_string(), Kind::Plain);
        }
    }
    sc.out
}

/// CSS: комментарии, строки, числа с единицами и `#цвета`, `--переменные`, `@правила`, имена свойств (слово перед `:`).
fn css(src: &str) -> Vec<Token> {
    let mut sc = Scan::new(src);
    let is_css_word = |ch: char| ch.is_ascii_alphanumeric() || ch == '_' || ch == '-';
    while !sc.done() {
        let c = sc.peek(0).unwrap_or(' ');
        if c == '/' && sc.peek(1) == Some('*') {
            let start = sc.pos;
            sc.pos += 2;
            while !sc.done() && !(sc.peek(0) == Some('*') && sc.peek(1) == Some('/')) {
                sc.pos += 1;
            }
            sc.pos = (sc.pos + 2).min(sc.chars.len());
            let t: String = sc.chars[start..sc.pos].iter().collect();
            sc.push(t, Kind::Comment);
        } else if c == '/' && sc.peek(1) == Some('/') {
            let t = sc.rest();
            sc.push(t, Kind::Comment);
        } else if c == '"' || c == '\'' {
            let s = sc.quoted(String::new(), c);
            sc.push(s, Kind::Str);
        } else if c == '#' && sc.peek(1).is_some_and(|d| d.is_ascii_hexdigit()) {
            sc.pos += 1;
            let h = sc.take_while(|d| d.is_ascii_hexdigit());
            sc.push(format!("#{h}"), Kind::Number);
        } else if c == '-' && sc.peek(1) == Some('-') {
            let w = sc.take_while(is_css_word);
            sc.push(w, Kind::Builtin);
        } else if c == '@' {
            sc.pos += 1;
            let w = sc.take_while(is_css_word);
            sc.push(format!("@{w}"), Kind::Accent);
        } else if c.is_ascii_digit() || (c == '.' && sc.peek(1).is_some_and(|d| d.is_ascii_digit())) || (c == '-' && sc.peek(1).is_some_and(|d| d.is_ascii_digit())) {
            let start = sc.pos;
            if c == '-' {
                sc.pos += 1;
            }
            sc.take_while(|d| d.is_ascii_digit() || d == '.');
            // единицы измерения
            sc.take_while(|d| d.is_ascii_alphabetic() || d == '%');
            let t: String = sc.chars[start..sc.pos].iter().collect();
            sc.push(t, Kind::Number);
        } else if is_css_word(c) && !c.is_ascii_digit() {
            let w = sc.take_while(is_css_word);
            let mut look = sc.pos;
            while sc.chars.get(look).is_some_and(|ch| ch.is_whitespace()) {
                look += 1;
            }
            let property = sc.chars.get(look) == Some(&':') && sc.chars.get(look + 1) != Some(&':');
            sc.push(w, if property { Kind::Keyword } else { Kind::Plain });
        } else {
            sc.pos += 1;
            sc.push(c.to_string(), Kind::Plain);
        }
    }
    sc.out
}

/// Токены одной строки кода.
pub fn highlight(lang: Lang, line: &str) -> Vec<Token> {
    match lang {
        Lang::Plain => vec![Token { text: line.to_string(), kind: Kind::Plain }],
        Lang::Python => python(line),
        Lang::C => c_lang(line),
        Lang::Asm => asm(line),
        Lang::Rust => rust(line),
        Lang::Sql => sql(line),
        Lang::Js => js(line),
        Lang::Css => css(line),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn kinds(lang: Lang, src: &str) -> Vec<(String, Kind)> {
        highlight(lang, src).into_iter().map(|t| (t.text, t.kind)).collect()
    }

    #[test]
    fn tokens_always_rebuild_the_source() {
        for (lang, src) in [
            (Lang::Python, "def area(r):  # круг"),
            (Lang::Python, "    return 3.14 * r * r"),
            (Lang::Python, "s = f\"привет {x}\" + 'a\\'b'"),
            (Lang::C, "#include <stdio.h>"),
            (Lang::C, "  int count = 0x1F; /* c */ // end"),
            (Lang::Asm, "loop: addi a0, a0, -1   # шаг"),
            (Lang::Asm, "    .text"),
            (Lang::Rust, "let s: &'a str = println!(\"x\"); // c"),
            (Lang::Sql, "SELECT name, COUNT(*) FROM t WHERE n > 10 -- итог"),
            (Lang::Sql, "WHERE s = 'it''s' AND x IS NULL"),
            (Lang::Js, "const f = (a) => a * 2n; // c"),
            (Lang::Js, "return `x ${y}` + \"s\" + new Map()"),
            (Lang::Css, "  --gap: 8px; color: #1a2b3c; /* c */ margin: -4px 1.5rem;"),
            (Lang::Css, "@media (min-width: 600px) { a:hover { top: 0 } }"),
            (Lang::Plain, "что угодно"),
        ] {
            let joined: String = highlight(lang, src).into_iter().map(|t| t.text).collect();
            assert_eq!(joined, src, "{lang:?}");
        }
    }

    #[test]
    fn python_keywords_builtins_calls_numbers_strings_comments() {
        let k = kinds(Lang::Python, "if x > 10: print(len(name), 'ok')  # конец");
        let get = |t: &str| k.iter().find(|(s, _)| s == t).map(|(_, k)| *k);
        assert_eq!(get("if"), Some(Kind::Keyword));
        assert_eq!(get("print"), Some(Kind::Builtin));
        assert_eq!(get("10"), Some(Kind::Number));
        assert_eq!(get("'ok'"), Some(Kind::Str));
        assert_eq!(get("# конец"), Some(Kind::Comment));
        assert!(k.iter().any(|(s, kind)| *kind == Kind::Plain && s.contains('x')));
        let call = kinds(Lang::Python, "area(5)");
        assert_eq!(call[0], ("area".into(), Kind::Accent), "имя перед скобкой — вызов");
    }

    #[test]
    fn digits_inside_words_are_not_numbers() {
        let k = kinds(Lang::Python, "x1 = 2");
        assert_eq!(k.iter().filter(|(_, kind)| *kind == Kind::Number).count(), 1);
        assert!(k.iter().any(|(s, kind)| s == "2" && *kind == Kind::Number));
    }

    #[test]
    fn c_directives_types_and_suffixed_numbers() {
        let k = kinds(Lang::C, "#include <stdio.h>");
        assert_eq!(k[0], ("#include".into(), Kind::Accent));
        let k = kinds(Lang::C, "uint8_t n = 5UL;");
        assert!(k.contains(&("uint8_t".into(), Kind::Builtin)));
        assert!(k.contains(&("5UL".into(), Kind::Number)));
        let k = kinds(Lang::C, "size_t len; // длина");
        assert!(k.contains(&("size_t".into(), Kind::Builtin)));
        assert!(k.contains(&("// длина".into(), Kind::Comment)));
    }

    #[test]
    fn rust_keywords_types_macros_lifetimes() {
        let k = kinds(Lang::Rust, "fn f<'a>(s: &'a str) { println!(\"x\", 5); }");
        assert!(k.contains(&("fn".into(), Kind::Keyword)));
        assert!(k.contains(&("str".into(), Kind::Builtin)));
        assert!(k.contains(&("println!".into(), Kind::Accent)));
        assert!(k.contains(&("'a".into(), Kind::Builtin)));
        assert!(k.contains(&("5".into(), Kind::Number)));
    }

    #[test]
    fn asm_instruction_registers_labels_numbers() {
        let k = kinds(Lang::Asm, "loop: addi a0, a0, -1");
        assert_eq!(k[0], ("loop:".into(), Kind::Accent));
        assert!(k.contains(&("addi".into(), Kind::Keyword)));
        assert!(k.contains(&("a0".into(), Kind::Builtin)));
        assert!(k.contains(&("-1".into(), Kind::Number)));
        let k = kinds(Lang::Asm, "    mv   a2, a0");
        assert!(k.contains(&("mv".into(), Kind::Keyword)));
        assert!(k.contains(&("a2".into(), Kind::Builtin)));
    }

    #[test]
    fn sql_js_css_kinds() {
        let k = kinds(Lang::Sql, "select Count(*) from t");
        assert!(k.contains(&("select".into(), Kind::Keyword)));
        assert!(k.contains(&("Count".into(), Kind::Builtin)), "функции без учёта регистра");
        let k = kinds(Lang::Js, "const x = null; class A {}");
        assert!(k.contains(&("const".into(), Kind::Keyword)));
        assert!(k.contains(&("null".into(), Kind::Number)));
        assert!(k.contains(&("A".into(), Kind::Builtin)));
        let k = kinds(Lang::Css, "a { color: #fff; --x: 1 }");
        assert!(k.contains(&("color".into(), Kind::Keyword)), "свойство — слово перед двоеточием");
        assert!(k.contains(&("#fff".into(), Kind::Number)));
        assert!(k.contains(&("--x".into(), Kind::Builtin)));
    }
}
