import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs, slot } from "./rs.tsx";

/* Глава 28 книги «Изучаем Rust»: время, числа и память. */

const pair = (a, b, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];
const row = (pre, items, c = "g", y = 66, size = 10.5) =>
  items.map((t, i) =>
    Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }),
  );

// 1. Введение
export const V01 = scene({
  labels: ["Время", "Числа", "Память"],
  caption: [
    "Duration и Instant — длительность и момент как отдельные типы",
    "Сотни методов у целых и дробных; особые типы Wrapping, Saturating, NonZero",
    "size_of, align_of и модуль mem; календарь, большие числа, случайность — во внешних пакетах",
  ],
  frames: [
    [...pair("Duration", "Instant", "b", "g")],
    [...row("a", ["i32", "f64", "Wrapping", "NonZero"], "g", 66, 10)],
    [...row("a", ["size_of", "mem", "chrono", "rand"], "y", 66, 10)],
  ],
});

// 2. Duration
export const V02 = scene({
  labels: ["Создание", "Чтение и арифметика", "Безопасность"],
  caption: [
    "Duration::from_secs, from_millis, from_micros, from_nanos, from_secs_f64",
    "as_secs, as_millis, as_secs_f64, subsec_nanos; + − × число и сравнение",
    "checked_add, checked_sub, saturating_sub; отрицательных длительностей нет; {:?} печатает «1.5s»",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "Duration::from_secs(90)",
          "Duration::from_millis(1500)",
          "Duration::from_secs_f64(0.25)",
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
        ["d.as_secs_f64()   // 1.5", "d * 2 + Duration::from_secs(1)", "a > b"],
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
          "a.checked_sub(b)         // Option",
          "a.saturating_sub(b)      // 0 при b > a",
        ],
        undefined,
        { w: 340, size: 10, lh: 28 },
      ),
    ],
  ],
});

// 3. Instant и SystemTime
export const V03 = scene({
  labels: ["Instant", "SystemTime", "Календарь"],
  caption: [
    "Instant — монотонные часы: только вперёд, для замеров; elapsed() возвращает Duration",
    "SystemTime — настенные часы, могут скакать; duration_since(UNIX_EPOCH) — секунды с 1970 года",
    "Календарь, часовые пояса, форматирование дат — chrono или time; в std их нет",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "let t = Instant::now();",
          "work();",
          'println!("{:?}", t.elapsed());',
        ],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["SystemTime::now()", "    .duration_since(UNIX_EPOCH)?"],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [...pair("замеры\nInstant", "даты\nchrono / time", "g", "y")],
  ],
});

// 4. Паузы и замеры
export const V04 = scene({
  labels: ["sleep", "Таймаут", "black_box"],
  caption: [
    "thread::sleep(d) усыпляет поток; в async — асинхронный сон, иначе встанет весь исполнитель",
    "Таймаут: запомнить Instant::now() и проверять elapsed() < предел",
    "Компилятор убирает неиспользуемые вычисления: std::hint::black_box; серьёзные замеры — criterion",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["thread::sleep(Duration::from_millis(100));"],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let start = Instant::now();", "while start.elapsed() < limit { }"],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "let r = black_box(compute());",
          "// criterion: много прогонов, статистика",
        ],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
  ],
});

// 5. Целые
export const V05 = scene({
  labels: ["checked, wrapping…", "Биты", "Степени двойки"],
  caption: [
    "checked_*, wrapping_*, saturating_*, overflowing_*; abs_diff, rem_euclid, pow, checked_pow",
    "count_ones, leading_zeros, trailing_zeros, rotate_left, swap_bytes, reverse_bits, to_be_bytes",
    "is_power_of_two, next_power_of_two; isqrt, ilog2 — целые корень и логарифм",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "a.checked_add(b)",
          "a.wrapping_mul(b)",
          "a.abs_diff(b)",
          "a.rem_euclid(m)",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "x.count_ones()",
          "x.leading_zeros()",
          "x.rotate_left(3)",
          "x.to_be_bytes()",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "x.is_power_of_two()",
          "x.next_power_of_two()",
          "n.isqrt()   n.ilog2()",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 6. Дробные
export const V06 = scene({
  labels: ["Округление", "Функции", "Проверки"],
  caption: [
    "floor, ceil, round, trunc, fract; powi, powf, sqrt, cbrt, hypot, mul_add",
    "exp, ln, log10, log2; sin, cos, tan, asin, acos, atan2; константы в std::f64::consts",
    "is_nan, is_finite, is_infinite; EPSILON, MIN, MAX, INFINITY; to_bits; total_cmp — полный порядок",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "x.floor()  x.ceil()  x.round()",
          "x.trunc()  x.fract()",
          "x.powi(3)   x.sqrt()   a.hypot(b)",
        ],
        undefined,
        { w: 340, size: 10, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "x.exp()   x.ln()   x.log10()",
          "x.sin()   x.cos()   y.atan2(x)",
          "std::f64::consts::PI",
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
          "x.is_nan()   x.is_finite()",
          "f64::EPSILON   f64::MAX",
          "a.total_cmp(&b)",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 7. Чего нет
export const V07 = scene({
  labels: ["Нет Number", "num-*", "rand"],
  caption: [
    "Нет общего трейта «число»: обобщённый код пишут через трейты Add, Mul и т. п.",
    "num-traits (Zero, One, Num), num-bigint, num-rational, num-complex — отдельные пакеты",
    "Случайность — пакет rand: нужен источник энтропии ОС; в std нет",
  ],
  frames: [
    [...pair("trait Number ✕", "Add + Mul + Copy", "r", "g")],
    [...row("a", ["num-traits", "bigint", "rational", "complex"], "b", 66, 9)],
    [Box("a", 180, 60, 230, 34, "rand — вне std", "y", { size: 12 })],
  ],
});

// 8. Особые типы
export const V08 = scene({
  labels: ["Wrapping, Saturating", "NonZero", "Niche"],
  caption: [
    "Wrapping(255u8) + Wrapping(1) = Wrapping(0) всегда, даже в debug; Saturating — упирается в границу",
    "NonZeroU32 не бывает нулём: ноль освобождён для «нет»; Option<NonZeroU32> — столько же, сколько u32",
    "Ниша работает с ссылками, Box, некоторыми enum; ошибки: ParseIntError, TryFromIntError",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "Wrapping(255u8) + Wrapping(1)   // 0",
          "Saturating(250u8) + Saturating(10)   // 255",
        ],
        undefined,
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [...pair("u32 · 4 байта", "Option<NonZero>\n4 байта", "b", "g")],
    [
      ...pair(
        "Option<&T>\n= размер &T",
        "Option<Box<T>>\n= размер Box",
        "g",
        "g",
      ),
    ],
  ],
});

// 9. Размеры
export const V09 = scene({
  labels: ["Размеры типов", "Раскладка", "Кэш"],
  caption: [
    "&T — 1 слово; &[T], &str — 2; String, Vec — 3; Box<dyn Trait> — 2 (указатель и таблица методов)",
    "enum — самый большой вариант + метка (метку прячут в нишу); поля структуры переставляются; repr(C) запрещает",
    "Структуры, помещающиеся в строку кэша (64 байта), обрабатываются в разы быстрее",
  ],
  frames: [
    [...row("a", ["&T 8", "&str 16", "String 24", "dyn 16"], "b", 66, 10)],
    [
      rs(
        "c",
        20,
        50,
        ["size_of::<Option<u8>>()    // 2", "size_of::<Option<&u8>>()   // 8"],
        undefined,
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [Box("a", 180, 60, 240, 34, "64 байта = строка кэша", "y", { size: 12 })],
  ],
});

// 10. Низкоуровневое
export const V10 = scene({
  labels: ["transmute", "ManuallyDrop, MaybeUninit", "discriminant"],
  caption: [
    "transmute переинтерпретирует байты и требует unsafe; почти всегда есть безопасная замена (from_bits, to_ne_bytes)",
    "ManuallyDrop отключает автоматический деструктор; MaybeUninit — значение без инициализации",
    "mem::discriminant(&e) — номер варианта без разбора данных; unsafe не отключает проверку типов",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "unsafe { std::mem::transmute::<u32, f32>(x) }",
          "f32::from_bits(x)   // безопасно",
        ],
        [1],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [...pair("ManuallyDrop", "MaybeUninit", "r", "r")],
    [
      rs(
        "c",
        20,
        50,
        ["mem::discriminant(&a) == mem::discriminant(&b)"],
        undefined,
        { w: 340, size: 9, lh: 28 },
      ),
    ],
  ],
});

// 11. Хеш и случайность
export const V11 = scene({
  labels: ["Hasher", "Стабильный хеш", "Свой генератор"],
  caption: [
    "std::hash: Hash и Hasher; SipHash защищён от атак",
    "Результат SipHash меняется от запуска к запуску — не сохраняйте; для стабильных хешей — blake3, sha2, fxhash",
    "Линейный конгруэнтный генератор — 5 строк и wrapping_mul; для тестов принимайте генератор параметром",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "let mut h = DefaultHasher::new();",
          "x.hash(&mut h);   let v = h.finish();",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [...pair("SipHash\nслучайная соль", "blake3, sha2\nстабильно", "y", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          "state = state.wrapping_mul(6364136223846793005)",
          "    .wrapping_add(1442695040888963407);",
        ],
        undefined,
        { w: 340, size: 8, lh: 28 },
      ),
    ],
  ],
});

// 12. Выделение памяти
export const V12 = scene({
  labels: ["Куча", "Свой аллокатор", "Арены"],
  caption: [
    "Box, Vec, String живут в куче; выделяет её глобальный аллокатор",
    "#[global_allocator] подменяет его: jemalloc, mimalloc ускоряют многие программы",
    "Много мелких объектов — арена: одно большое выделение и смещения (bumpalo, typed-arena)",
  ],
  frames: [
    [...pair("стек\nбыстро, мало", "куча\nгибко", "g", "b")],
    [
      rs(
        "c",
        20,
        50,
        [
          "#[global_allocator]",
          "static A: mimalloc::MiMalloc = mimalloc::MiMalloc;",
        ],
        [0],
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
    [
      ...pair(
        "тысяча Box\nтысяча выделений",
        "арена\nодно выделение",
        "r",
        "g",
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "Instant — замеры, SystemTime — метки; Duration без отрицательных значений",
    "Целые и дробные — сотни методов; Wrapping, Saturating, NonZero; size_of; num и rand — внешние",
    "Следующая глава — каталог трейтов: Clone, Copy, Default, Eq, Ord, Hash, From, AsRef и другие",
  ],
  frames: [
    [...row("a", ["Duration", "Instant", "num", "mem"], "g")],
    [
      rs(
        "c",
        20,
        40,
        ["let t = Instant::now();", "let s = n.checked_mul(m)?;"],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [
      Box(
        "a",
        180,
        60,
        250,
        34,
        "Clone · Copy · Default · Eq · Ord · Hash",
        "b",
        { size: 9.5 },
      ),
    ],
  ],
});
