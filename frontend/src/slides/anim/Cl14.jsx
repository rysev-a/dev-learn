import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, asm, cc } from "./cl.tsx";

/* Глава 14 книги «От assembler к языку C»: современный C — C11 и C23. */

// 1. Редакции
export const V01 = scene({
  labels: ["Редакции языка", "Ключ -std", "Расширения GNU"],
  caption: [
    "C89 → C99 → C11 → C17 → C23: стандарты добавляют возможности и сохраняют совместимость",
    "Редакцию выбирают ключом: -std=c11, -std=c17, -std=c23 (в старых компиляторах c2x)",
    "-std=gnu11 разрешает ещё и расширения компилятора: typeof, выражения-операторы, __builtin_*",
  ],
  frames: [
    [
      ...["C89", "C99", "C11", "C17", "C23"].map((t, i) =>
        Box(
          `e${i}`,
          50 + i * 65,
          76,
          58,
          30,
          t,
          i === 2 || i === 4 ? "g" : "b",
          { size: 10 },
        ),
      ),
      ...[0, 1, 2, 3].map((i) =>
        arrow(`a${i}`, 78 + i * 65, 76, 86 + i * 65, 76, "g"),
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "gcc -std=c11 -Wall -Wextra -Wpedantic main.c",
          "gcc -std=c23 main.c   # gcc 14+",
        ],
        [0],
        { w: 330, size: 9.5, lh: 28 },
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "#define MAX(a, b) ({ typeof(a) _a = (a); … })",
          "// только -std=gnu11, не -std=c11 -pedantic",
        ],
        [0],
        { w: 330, size: 9.5, lh: 28 },
      ),
    ],
  ],
});

// 2. Наследие C99
export const V02 = scene({
  labels: ["Объявления где нужно", "Типы и макросы", "VLA не обязательны"],
  caption: [
    "Переменные объявляют там, где нужны, в том числе в заголовке цикла; однострочные комментарии",
    "bool из <stdbool.h>, типы <stdint.h>, long long, static inline, snprintf, макросы с переменным числом аргументов",
    "restrict — обещание отсутствия алиасинга; массивы переменной длины в C11 сделали необязательными: стек переполняется",
  ],
  frames: [
    [
      cc(
        "c",
        20,
        40,
        [
          "for (int i = 0; i < n; i++) {   // C99",
          "    int sq = i * i;            // здесь, а не в начале",
          "}",
        ],
        [0],
        { w: 330, size: 10, lh: 26 },
      ),
    ],
    [
      cc(
        "c",
        20,
        30,
        [
          "#include <stdbool.h>",
          "#include <stdint.h>",
          "bool ok = true;  uint32_t id = 7;",
        ],
        undefined,
        { w: 330, size: 10.5, lh: 24 },
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "void copy(int *restrict d, const int *restrict s, size_t n);",
          "int a[n];   // VLA — лучше malloc",
        ],
        [0],
        { w: 335, size: 9, lh: 28 },
      ),
    ],
  ],
});

// 3. Составные литералы
export const V03 = scene({
  labels: ["Назначенные инициализаторы", "Составной литерал", "Время жизни"],
  caption: [
    "{.x = 1, .y = 2} называет поля, остальные обнуляются; для массивов — [3] = 5",
    "(struct pt){.x = 1, .y = 2} создаёт временную структуру прямо в выражении — удобно для параметров по умолчанию",
    "Составной литерал живёт до конца блока: возвращать указатель на него из функции нельзя; {} — пустой инициализатор (C23)",
  ],
  frames: [
    [
      cc(
        "c",
        20,
        30,
        [
          "struct pt p = {.y = 2, .x = 1};",
          "int t[8] = {[3] = 5, [6] = 7};",
          "// остальное — нули",
        ],
        [0, 1],
        { w: 330, size: 10, lh: 26 },
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "draw(&(struct opt){.w = 80, .color = RED});",
          "int *a = (int[]){1, 2, 3};",
        ],
        [0],
        { w: 335, size: 9.5, lh: 28 },
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "int *f(void) {",
          "    return (int[]){1, 2};   // ✕ умрёт с блоком",
          "}",
        ],
        undefined,
        { w: 320, size: 10.5, lh: 26, bad: [1] },
      ),
    ],
  ],
});

// 4. Гибкий член массива
export const V04 = scene({
  labels: ["Структура с хвостом", "Выделение", "Что нельзя"],
  caption: [
    "Последний член — массив без длины: data[]; данные лежат сразу за полями, одним блоком",
    "malloc(sizeof(struct buf) + n): честный размер вместо старого приёма с data[1]",
    "sizeof структуры не включает хвост; присваивание копирует только заголовок — копируйте блок целиком memcpy",
  ],
  frames: [
    [
      cc(
        "c",
        20,
        40,
        [
          "struct buf {",
          "    size_t n;",
          "    char data[];   // гибкий член",
          "};",
        ],
        [2],
        { w: 320, size: 11, lh: 22 },
      ),
    ],
    [
      Box("h", 90, 76, 70, 30, "n = 5", "b", { size: 10 }),
      ...cells2(),
      Tx("t", 180, 120, "malloc(sizeof *b + 5)", { size: 9.5, mono: true }),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "struct buf a = *b;   // ✕ без хвоста",
          "memcpy(c, b, sizeof *b + b->n);   // ✓",
        ],
        [1],
        { w: 335, size: 9.5, lh: 28, bad: [0] },
      ),
    ],
  ],
});

function cells2() {
  return ["h", "e", "l", "l", "o"].map((t, i) =>
    Box(`c${i}`, 150 + i * 36, 76, 34, 30, t, "g", { size: 10 }),
  );
}

// 5. restrict и inline
export const V05 = scene({
  labels: ["restrict", "memcpy и memmove", "static inline"],
  caption: [
    "restrict — обещание: через этот указатель память никто другой не изменит; компилятор оптимизирует смелее",
    "memcpy объявлена с restrict: пересекающиеся области — UB; memmove — для пересекающихся",
    "В заголовках пишут static inline: у каждого файла своя копия, компилятор решает, подставлять ли тело",
  ],
  frames: [
    [
      cc(
        "c",
        20,
        40,
        [
          "void add(int *restrict a, const int *restrict b) {",
          "    *a += *b;   // можно держать *b в регистре",
          "}",
        ],
        [0],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "void *memcpy(void *restrict d, const void *restrict s, size_t n);",
          "void *memmove(void *d, const void *s, size_t n);",
        ],
        undefined,
        { w: 340, size: 8.5, lh: 30 },
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        ["static inline int sq(int x) {", "    return x * x;", "}"],
        [0],
        { w: 320, size: 11, lh: 24 },
      ),
    ],
  ],
});

// 6. Проверки C11
export const V06 = scene({
  labels: ["_Static_assert", "_Alignas и _Alignof", "Анонимные члены"],
  caption: [
    '_Static_assert(условие, "текст") останавливает сборку: размер структуры, ширина типа, константы',
    "_Alignas(n) задаёт выравнивание объекта, _Alignof(T) его узнаёт; _Noreturn — функция не возвращает управление",
    "Анонимные структуры и объединения: поля вложенного становятся полями внешней структуры",
  ],
  frames: [
    [
      cc(
        "c",
        10,
        40,
        [
          "_Static_assert(sizeof(struct hdr) == 8,",
          '                "hdr: лишние прокладки");',
        ],
        [0],
        { w: 345, size: 10, lh: 28 },
      ),
    ],
    [
      cc(
        "c",
        20,
        30,
        [
          "_Alignas(64) char cache_line[64];",
          "size_t a = _Alignof(double);   // 8",
          "_Noreturn void die(const char *m);",
        ],
        undefined,
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      cc(
        "c",
        20,
        30,
        [
          "struct v {",
          "    union { float f; uint32_t bits; };   // анонимное",
          "};",
          "v.bits = 0;   // без v.u.bits",
        ],
        [1, 3],
        { w: 335, size: 9.5, lh: 22 },
      ),
    ],
  ],
});

// 7. Атомики
export const V07 = scene({
  labels: ["Атомарный тип", "fetch_add и CAS", "Гонка данных"],
  caption: [
    "atomic_int гарантирует: чтение и запись происходят целиком; atomic_load, atomic_store",
    "atomic_fetch_add и compare_exchange — неделимое чтение-изменение-запись; на RISC-V это amoadd и пара lr / sc",
    "Обычная переменная, которую двое потоков читают и пишут одновременно, — гонка данных и неопределённое поведение",
  ],
  frames: [
    [
      cc(
        "c",
        20,
        40,
        [
          "#include <stdatomic.h>",
          "atomic_int counter = 0;",
          "atomic_store(&counter, 5);",
        ],
        [1],
        { w: 320, size: 10.5, lh: 26 },
      ),
    ],
    [
      cc(
        "c",
        10,
        36,
        [
          "atomic_fetch_add(&counter, 1);",
          "int e = 5;",
          "atomic_compare_exchange_strong(&counter, &e, 9);",
        ],
        [0, 2],
        { w: 345, size: 9, lh: 26 },
      ),
      asm("a", 220, 118, ["amoadd.w a5, a4, (a0)"], undefined, {
        w: 135,
        size: 7.5,
        lh: 14,
      }),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "int plain = 0;               // поток A: plain++",
          "                             // поток B: plain++",
          "// ✕ гонка данных → UB",
        ],
        undefined,
        { w: 335, size: 9, lh: 26, bad: [0, 1] },
      ),
    ],
  ],
});

// 8. Модель памяти
export const V08 = scene({
  labels: ["Порядки", "release / acquire", "CAS-цикл"],
  caption: [
    "relaxed — только неделимость; acquire и release создают связь «после записи — до чтения»; seq_cst — самый строгий и по умолчанию",
    "Поток A готовит данные и пишет флаг с release; поток B читает флаг с acquire — и безопасно видит данные",
    "Свои неделимые операции строят циклом: читаем, считаем новое, пробуем заменить, при неудаче повторяем",
  ],
  frames: [
    [
      Box("a", 90, 40, 110, 26, "relaxed", "b", { size: 10 }),
      Box("b", 90, 76, 110, 26, "acquire / release", "g", { size: 9.5 }),
      Box("c", 90, 112, 110, 26, "seq_cst", "y", { size: 10 }),
      Tx("n", 280, 76, "слабее →\nстрже", { size: 9.5 }),
    ],
    [
      cc(
        "c",
        10,
        28,
        [
          "// A:  data = 42;",
          "       atomic_store_explicit(&ready, 1, memory_order_release);",
          "// B:  while (!atomic_load_explicit(&ready, memory_order_acquire));",
          "       use(data);   // видит 42",
        ],
        [1, 2],
        { w: 350, size: 8, lh: 24 },
      ),
    ],
    [
      cc(
        "c",
        10,
        30,
        [
          "int old = atomic_load(&x);",
          "while (!atomic_compare_exchange_weak(&x, &old, old * 2))",
          "    ;   // old обновился — повторяем",
        ],
        [1],
        { w: 345, size: 9, lh: 24 },
      ),
    ],
  ],
});

// 9. Юникод
export const V09 = scene({
  labels: ["char16_t, char32_t", "u8-литералы", "Байты ≠ символы"],
  caption: [
    "<uchar.h>: char16_t и char32_t; wchar_t зависит от платформы и для обмена данными не годится",
    "u8\"…\" гарантирует UTF-8; в C23 появился тип char8_t и литералы u8'a'",
    "Строка в C — массив байтов: длина в байтах не равна числу символов (глава о представлении данных)",
  ],
  frames: [
    [
      cc(
        "c",
        20,
        40,
        [
          "#include <uchar.h>",
          "char32_t c = U'€';   // 0x20AC",
          'char16_t s[] = u"é";',
        ],
        [1],
        { w: 320, size: 10.5, lh: 26 },
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        ['const char *a = u8"héllo";', "char8_t c = u8'a';     // C23"],
        [0, 1],
        { w: 330, size: 10.5, lh: 28 },
      ),
    ],
    [
      Box("a", 90, 70, 100, 28, '"é" = 2 байта', "y", { size: 10 }),
      Box("b", 250, 70, 100, 28, "1 символ", "g", { size: 10 }),
    ],
  ],
});

// 10. C23: язык
export const V10 = scene({
  labels: ["nullptr, bool", "constexpr, typeof, auto", "Атрибуты и литералы"],
  caption: [
    "nullptr — отдельный тип нулевого указателя; bool, true и false стали ключевыми словами",
    "constexpr — именованные константы для выражений; typeof и ограниченный auto выводят тип из инициализатора",
    "[[nodiscard]], [[maybe_unused]], [[fallthrough]]; двоичные литералы 0b1010, разделитель разрядов 1'000'000; #embed вставляет файл как массив байтов",
  ],
  frames: [
    [
      cc(
        "c",
        20,
        40,
        ["int *p = nullptr;", "bool ok = true;   // без <stdbool.h>"],
        [0, 1],
        { w: 330, size: 10.5, lh: 28 },
      ),
    ],
    [
      cc(
        "c",
        20,
        30,
        [
          "constexpr int N = 8;",
          "int buf[N];",
          "typeof(N) k = N;",
          "auto x = 3.5;   // double",
        ],
        [0, 3],
        { w: 330, size: 10.5, lh: 22 },
      ),
    ],
    [
      cc(
        "c",
        10,
        30,
        [
          "[[nodiscard]] int parse(const char *);",
          "int mask = 0b1010;   long big = 1'000'000;",
          "switch (k) { case 1: f(); [[fallthrough]]; case 2: … }",
        ],
        [0, 1],
        { w: 350, size: 8.5, lh: 24 },
      ),
    ],
  ],
});

// 11. C23: библиотека
export const V11 = scene({
  labels: ["stdckdint.h", "stdbit.h", "Прочее"],
  caption: [
    "ckd_add, ckd_sub, ckd_mul: арифметика с проверкой переполнения — возвращает признак, результат пишет по адресу",
    "<stdbit.h>: stdc_count_ones, stdc_leading_zeros, stdc_trailing_zeros, повороты — вместо самодельных __builtin_*",
    "enum с базовым типом, _BitInt(N), strdup/strndup в стандарте, #elifdef, __VA_OPT__, пустой инициализатор {}",
  ],
  frames: [
    [
      cc(
        "c",
        20,
        40,
        [
          "#include <stdckdint.h>",
          "int r;",
          "if (ckd_add(&r, a, b)) /* переполнение */;",
        ],
        [2],
        { w: 335, size: 10, lh: 26 },
      ),
    ],
    [
      cc(
        "c",
        20,
        40,
        [
          "#include <stdbit.h>",
          "stdc_count_ones(0xFFu)       // 8",
          "stdc_leading_zeros(1u)       // 31",
        ],
        [1, 2],
        { w: 335, size: 10, lh: 26 },
      ),
    ],
    [
      cc(
        "c",
        20,
        30,
        [
          "enum color : unsigned char { RED, GREEN };",
          "unsigned _BitInt(12) x = 4095;",
          "struct s v = {};",
        ],
        [0, 1],
        { w: 335, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 12. Практика
export const V12 = scene({
  labels: ["Что включать", "Чего избегать", "Переносимость"],
  caption: [
    "Стандарт не ниже C11; -Wall -Wextra -Wpedantic; stdint и bool; size_t для размеров; designated initializers, const, restrict, static_assert, атрибуты",
    "VLA, register, gets и небезопасные strcpy/sprintf; расширения компилятора там, где нужна переносимость",
    "Для C23 проверяйте поддержку каждой возможности: компиляторы внедряют её постепенно",
  ],
  frames: [
    [
      Box("a", 90, 50, 120, 26, "-std=c11 -Wall -Wextra", "g", { size: 9 }),
      Box("b", 90, 86, 120, 26, "stdint, bool, size_t", "g", { size: 9.5 }),
      Box("c", 90, 122, 120, 26, "static_assert, const", "g", { size: 9.5 }),
    ],
    [
      Box("a", 90, 50, 120, 26, "VLA, register", "r", { size: 10 }),
      Box("b", 90, 86, 120, 26, "gets, strcpy, sprintf", "r", { size: 9.5 }),
      Box("c", 90, 122, 120, 26, "расширения везде", "y", { size: 9.5 }),
    ],
    [
      cc(
        "c",
        20,
        40,
        ["#if __STDC_VERSION__ >= 202311L", "    /* C23 */", "#endif"],
        [0],
        { w: 330, size: 10.5, lh: 26 },
      ),
    ],
  ],
});

// 13. Итоги книги
export const V13 = scene({
  labels: ["Путь книги", "Инструменты", "Дальше"],
  caption: [
    "Ассемблер → типы и операторы → функции и указатели → строки и структуры → динамическая память и структуры данных",
    "Препроцессор и модули, ввод-вывод, представление данных, сборка и библиотеки, санитайзеры и отладчик, тестирование и стиль, современный C",
    "Дальше — Unix: C встречается с операционной системой; затем сети, виртуализация и Rust для безопасного системного кода",
  ],
  frames: [
    [
      Box("a", 60, 40, 80, 26, "ассемблер", "b", { size: 10 }),
      Box("b", 150, 40, 80, 26, "типы, указатели", "b", { size: 9 }),
      Box("c", 250, 40, 90, 26, "память, структуры", "b", { size: 9 }),
      arrow("e1", 100, 40, 110, 40, "g"),
      arrow("e2", 190, 40, 205, 40, "g"),
      Box("d", 180, 100, 160, 28, "язык C", "g", { size: 11 }),
    ],
    [
      Box("a", 70, 50, 100, 26, "препроцессор", "b", { size: 9.5 }),
      Box("b", 190, 50, 100, 26, "ввод-вывод, данные", "b", { size: 9 }),
      Box("c", 310, 50, 100, 26, "make, библиотеки", "b", { size: 9 }),
      Box("d", 70, 100, 100, 26, "санитайзеры", "g", { size: 10 }),
      Box("e", 190, 100, 100, 26, "тесты и стиль", "g", { size: 10 }),
      Box("f", 310, 100, 100, 26, "C11 и C23", "y", { size: 10 }),
    ],
    [
      Tx("a", 180, 50, "Unix · сети · виртуализация · Rust", {
        size: 11,
        c: "g",
        mono: true,
      }),
      Tx("b", 180, 100, "следующие книги курса", { size: 10 }),
    ],
  ],
});
