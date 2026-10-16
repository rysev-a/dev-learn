"""Задачи книги «От assembler к языку C»: глава 7 (код компилируется gcc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {7: [{'id': 'c7-sq-parens',
      'mode': 'c',
      'title': 'Макросы без сюрпризов: SQ, CUBE, ABS, MIN, MAX',
      'statement': 'Напишите макросы SQ(x), CUBE(x), ABS(x), MIN(a, b), MAX(a, b). Они должны правильно '
                   'работать с любыми выражениями в аргументах: SQ(a + 1), 100 / SQ(2), -ABS(5), MAX(1, 2) * '
                   '10. Подсказка: скобки вокруг каждого параметра и вокруг всего тела.',
      'starter': '#define SQ(x) 0\n'
                 '#define CUBE(x) 0\n'
                 '#define ABS(x) 0\n'
                 '#define MIN(a, b) 0\n'
                 '#define MAX(a, b) 0\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a = 4, b = -7, c = 3, d = 5;\n'
                '    printf("%d %d %d\\n", SQ(a + 1), SQ(1 + 2), 100 / SQ(2));\n'
                '    printf("%d %d %d\\n", CUBE(1 + 1), CUBE(a - c), -SQ(3));\n'
                '    printf("%d %d %d\\n", ABS(b + 1), -ABS(5), ABS(a - 10) + 1);\n'
                '    printf("%d %d %d\\n", MIN(a + c, d), MIN(a, b) * 2, MAX(a + b, c * d));\n'
                '    printf("%d %d\\n", MAX(1, 2) * 10, MIN(3, 4) == 3 ? 1 : 0);\n'
                '    printf("%.2f %.2f\\n", SQ(1.5 + 1.0), ABS(-2.5));\n'
                '    return 0;\n'
                '}\n',
      'hint': '#define SQ(x) ((x) * (x)) — параметры в скобках и всё тело в скобках; для ABS/MIN/MAX '
              'тернарный оператор тоже целиком в скобках.',
      'expected': ['25 9 25', '8 1 -9', '6 -5 7', '5 -14 15', '20 1', '6.25 2.50']},
     {'id': 'c7-clamp-sign',
      'mode': 'c',
      'title': 'CLAMP, SIGN и IN_RANGE',
      'statement': 'CLAMP(x, lo, hi) — ограничить значение отрезком [lo, hi]; SIGN(x) → −1, 0 или 1 (для int '
                   'и double); IN_RANGE(x, lo, hi) → 1, если lo ≤ x ≤ hi, иначе 0. Аргументы — произвольные '
                   'выражения без побочных эффектов; макросы должны работать вложенно: CLAMP(CLAMP(x, 0, 5), '
                   '2, 3).',
      'starter': '#define CLAMP(x, lo, hi) 0\n#define SIGN(x) 0\n#define IN_RANGE(x, lo, hi) 0\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a = 7, b = 5;\n'
                '    printf("%d %d %d\\n", CLAMP(a + b, 0, 10), CLAMP(a - b, 3, 9), CLAMP(-4, -2, 2));\n'
                '    printf("%d %d\\n", CLAMP(CLAMP(100, 0, 5), 2, 3), CLAMP(CLAMP(-100, 0, 5), 2, 3));\n'
                '    printf("%.1f %.1f\\n", CLAMP(2.5, 0.0, 1.0), CLAMP(-0.5, 0.0, 1.0));\n'
                '    printf("%d %d %d %d\\n", SIGN(a - b), SIGN(b - a), SIGN(a - 7), SIGN(-3.5));\n'
                '    printf("%d %d %d %d\\n", IN_RANGE(5, 1, 5), IN_RANGE(a, 8, 9), IN_RANGE(a + b, 12, 12), '
                'IN_RANGE(0, -1, 1) + IN_RANGE(2, 0, 1));\n'
                '    printf("%d\\n", 10 * SIGN(b) + IN_RANGE(b, 0, 9));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Каждый параметр в скобках. SIGN: ((x) > 0) - ((x) < 0). Вложенный CLAMP работает, если все '
              'тернарные операторы в скобках.',
      'expected': ['10 3 -2', '3 2', '1.0 0.0', '1 -1 0 -1', '1 0 1 1', '11']},
     {'id': 'c7-array-macros',
      'mode': 'c',
      'title': 'Макросы над массивами: ARRAY_SIZE, LAST, FILL, ZERO',
      'statement': 'ARRAY_SIZE(a) — число элементов массива; LAST(a) — последний элемент (можно присваивать: '
                   'LAST(a) = 5); FILL(a, v) — записать v во все элементы; ZERO(a) — обнулить массив '
                   'целиком. Макросы должны работать с массивами любых типов, в том числе структур; ZERO — '
                   'без цикла.',
      'starter': '#include <string.h>\n'
                 '\n'
                 '#define ARRAY_SIZE(a) 0\n'
                 '#define LAST(a) (a)[0]\n'
                 '#define FILL(a, v)\n'
                 '#define ZERO(a)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'struct pt { int x, y; };\n'
                '\n'
                'int main(void) {\n'
                '    int a[7];\n'
                '    double d[3] = {1.5, 2.5, 3.5};\n'
                '    char s[16] = "hello";\n'
                '    struct pt p[4] = {{1, 2}, {3, 4}, {5, 6}, {7, 8}};\n'
                '    printf("%zu %zu %zu %zu\\n", ARRAY_SIZE(a), ARRAY_SIZE(d), ARRAY_SIZE(s), '
                'ARRAY_SIZE(p));\n'
                '    FILL(a, 9);\n'
                '    LAST(a) = 1;\n'
                '    for (size_t i = 0; i < ARRAY_SIZE(a); i++) printf("%d ", a[i]);\n'
                '    printf("\\n%.1f %d\\n", LAST(d), LAST(p).y);\n'
                '    LAST(p) = (struct pt){0, -1};\n'
                '    printf("%d %d\\n", p[3].x, p[3].y);\n'
                '    ZERO(p);\n'
                '    printf("%d %d %d\\n", p[0].x, p[2].y, p[3].y);\n'
                '    ZERO(s);\n'
                '    printf("%zu %d\\n", strlen(s), s[15]);\n'
                '    if (ARRAY_SIZE(a) > 3) FILL(d, 0.25); else FILL(d, 8);\n'
                '    printf("%.2f %.2f\\n", d[0], d[2]);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'ARRAY_SIZE — sizeof(a) / sizeof((a)[0]). FILL оборачивайте в do { … } while (0) — драйвер '
              'использует его в if/else.',
      'expected': ['7 3 16 4', '9 9 9 9 9 9 1', '3.5 8', '0 -1', '0 0 0', '0 0', '0.25 0.25']},
     {'id': 'c7-bit-macros',
      'mode': 'c',
      'title': 'Битовые макросы',
      'statement': 'BIT(n) = 1u << n; SET_BIT(x, n), CLEAR_BIT(x, n), TOGGLE_BIT(x, n) — меняют переменную x '
                   'на месте; TEST_BIT(x, n) → 0 или 1; LOW_MASK(n) — n младших единиц (0 ≤ n ≤ 31); '
                   'GET_BITS(x, lo, n) — n бит, начиная с бита lo (сдвинутых вниз). x — unsigned. '
                   'Аргументы-выражения вроде i + 1 должны работать.',
      'starter': '#define BIT(n) 0u\n'
                 '#define SET_BIT(x, n)\n'
                 '#define CLEAR_BIT(x, n)\n'
                 '#define TOGGLE_BIT(x, n)\n'
                 '#define TEST_BIT(x, n) 0\n'
                 '#define LOW_MASK(n) 0u\n'
                 '#define GET_BITS(x, lo, n) 0u\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    unsigned x = 0;\n'
                '    for (int i = 0; i < 4; i++) SET_BIT(x, i * 2);\n'
                '    printf("%u %#x\\n", x, x);\n'
                '    CLEAR_BIT(x, 2 + 2);\n'
                '    TOGGLE_BIT(x, 1);\n'
                '    TOGGLE_BIT(x, 0);\n'
                '    printf("%#x\\n", x);\n'
                '    printf("%u %u %u %u\\n", TEST_BIT(x, 1), TEST_BIT(x, 0), TEST_BIT(x, 4), TEST_BIT(x + '
                '1, 0));\n'
                '    printf("%u %u %u\\n", LOW_MASK(0), LOW_MASK(5), LOW_MASK(8 + 8));\n'
                '    unsigned v = 0xDEADBEEF;\n'
                '    printf("%x %x %x\\n", GET_BITS(v, 0, 8), GET_BITS(v, 16, 8), GET_BITS(v, 28, 4));\n'
                '    printf("%u\\n", BIT(31) >> 31);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'TEST_BIT: ((x) >> (n)) & 1u. LOW_MASK(n) = BIT(n) − 1. Всегда скобки вокруг n и x.',
      'expected': ['85 0x55', '0x46', '1 0 0 1', '0 31 65535', 'ef ad d', '1']},
     {'id': 'c7-swap-macro',
      'mode': 'c',
      'title': 'SWAP для любого типа',
      'statement': 'SWAP(a, b) — поменять местами две переменные одного типа (int, double, указатели, '
                   'структуры) через временную переменную типа __typeof__(a). Макрос должен работать в '
                   'if/else без фигурных скобок и не ломаться, если в вызывающем коде есть переменные с '
                   '«обычными» именами t, tmp или _t.',
      'starter': '#define SWAP(a, b)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'struct pt { int x, y; };\n'
                '\n'
                'int main(void) {\n'
                '    int t = 1, u = 2, tmp = 3, _t = 4;\n'
                '    SWAP(t, u);\n'
                '    SWAP(tmp, _t);\n'
                '    printf("%d %d %d %d\\n", t, u, tmp, _t);\n'
                '    double d = 1.5, e = -2.5;\n'
                '    SWAP(d, e);\n'
                '    printf("%.1f %.1f\\n", d, e);\n'
                '    char *p = "left", *q = "right";\n'
                '    SWAP(p, q);\n'
                '    printf("%s %s\\n", p, q);\n'
                '    struct pt a = {1, 2}, b = {3, 4};\n'
                '    SWAP(a, b);\n'
                '    printf("%d %d %d %d\\n", a.x, a.y, b.x, b.y);\n'
                '    int v[3] = {10, 20, 30};\n'
                '    int i = 0, j = 2;\n'
                '    if (v[i] < v[j]) SWAP(v[i], v[j]); else puts("no swap");\n'
                '    if (v[i] < v[j]) SWAP(v[i], v[j]); else puts("no swap");\n'
                '    printf("%d %d %d\\n", v[0], v[1], v[2]);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'do { __typeof__(a) _swap_tmp_ = (a); (a) = (b); (b) = _swap_tmp_; } while (0) — уникальное '
              'имя временной переменной и одна «операторная» обёртка.',
      'expected': ['2 1 4 3', '-2.5 1.5', 'right left', '3 4 1 2', 'no swap', '30 20 10']},
     {'id': 'c7-eval-once',
      'mode': 'c',
      'title': 'Аргумент вычисляется один раз: MAX3 и MIN3',
      'statement': 'MAX3(a, b, c) и MIN3(a, b, c) — наибольшее и наименьшее из трёх значений. Каждый '
                   'аргумент должен вычисляться ровно один раз (в аргументах бывают вызовы функций с '
                   'побочными эффектами): используйте выражение-оператор GNU ({ … }) и __typeof__. Макросы '
                   'должны работать и с double.',
      'starter': '#define MAX3(a, b, c) 0\n#define MIN3(a, b, c) 0\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static int calls;\n'
                'static int next(int v) { calls++; return v; }\n'
                'static double nextd(double v) { calls++; return v; }\n'
                '\n'
                'int main(void) {\n'
                '    int r = MAX3(next(5), next(9), next(2));\n'
                '    printf("%d %d\\n", r, calls);\n'
                '    calls = 0;\n'
                '    r = MIN3(next(5), next(9), next(2));\n'
                '    printf("%d %d\\n", r, calls);\n'
                '    calls = 0;\n'
                '    r = MAX3(next(1), next(1), next(1)) + MIN3(next(4), next(3), next(8));\n'
                '    printf("%d %d\\n", r, calls);\n'
                '    double d = MAX3(nextd(1.5), 2.25, nextd(-1));\n'
                '    printf("%.2f\\n", d);\n'
                '    int a = 3, b = 3, c = 3;\n'
                '    int m = MAX3(a++, b++, c++);\n'
                '    printf("%d %d\\n", m, a + b + c);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Внутри ({ … }) заведите _a = (a), _b = (b), _c = (c): каждое выражение вычисляется единожды; '
              'последнее выражение в скобках — результат.',
      'expected': ['9 3', '2 3', '4 6', '2.25', '3 12']},
     {'id': 'c7-stringify',
      'mode': 'c',
      'title': 'Строкизация: STR, XSTR, SHOW и VERSION',
      'statement': 'STR(x) → строковый литерал из текста аргумента без раскрытия макросов; XSTR(x) — то же, '
                   'но сначала раскрывает макрос в аргументе (два уровня); SHOW(e) — печатает '
                   '«текст_выражения = значение» (значение приведите к int, формат «%d»); VERSION — строка '
                   '«vМАЖОР.МИНОР» из готовых макросов MAJOR и MINOR (склейкой литералов, без sprintf).',
      'starter': '#define MAJOR 2\n'
                 '#define MINOR 7\n'
                 '\n'
                 '#define STR(x) ""\n'
                 '#define XSTR(x) ""\n'
                 '#define SHOW(e)\n'
                 '#define VERSION ""\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                '#define LIMIT 100\n'
                '\n'
                'int main(void) {\n'
                '    printf("%s %s %s\\n", STR(hello), STR(a + b), STR(LIMIT));\n'
                '    printf("%s %s %s\\n", XSTR(LIMIT), XSTR(MAJOR), XSTR(LIMIT + 1));\n'
                '    int a = 6, b = 7;\n'
                '    SHOW(a * b);\n'
                '    SHOW(a   +   b);\n'
                '    SHOW(3 * (4 + 5));\n'
                '    SHOW(a > b);\n'
                '    SHOW(LIMIT / 3);\n'
                '    printf("%s %zu\\n", VERSION, strlen(VERSION));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'STR(x) #x; XSTR(x) STR(x) — второй уровень заставляет препроцессор раскрыть макрос до '
              'строкизации. SHOW: printf(#e " = %d\\n", (int)(e)).',
      'expected': ['hello a + b LIMIT',
                   '100 2 100 + 1',
                   'a * b = 42',
                   'a + b = 13',
                   '3 * (4 + 5) = 27',
                   'a > b = 0',
                   'LIMIT / 3 = 33',
                   'v2.7 4']},
     {'id': 'c7-token-paste',
      'mode': 'c',
      'title': 'Генерация функций склейкой имён',
      'statement': 'CAT(a, b) — склеить два токена (с раскрытием макросов: CAT(x, __LINE__)-подобных вещей '
                   'не нужно, достаточно двух уровней). DEFINE_ADDER(n) — определяет функцию int add_<n>(int '
                   'x), возвращающую x + n; DEFINE_CMP(type) — функцию int cmp_<type>(const void *, const '
                   'void *) для qsort по возрастанию. Сделайте вызовы: DEFINE_ADDER для 1, 5 и 100; '
                   'DEFINE_CMP для int, long и double.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 '#define CAT_(a, b) a ## b\n'
                 '#define CAT(a, b) CAT_(a, b)\n'
                 '#define DEFINE_ADDER(n)\n'
                 '#define DEFINE_CMP(type)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d\\n", add_1(10), add_5(10), add_100(-100));\n'
                '    int a[] = {5, -2, 9, 0, 3};\n'
                '    long b[] = {1000000000000L, -5, 42};\n'
                '    double c[] = {2.5, -1.25, 2.25, 0};\n'
                '    qsort(a, 5, sizeof a[0], cmp_int);\n'
                '    qsort(b, 3, sizeof b[0], cmp_long);\n'
                '    qsort(c, 4, sizeof c[0], cmp_double);\n'
                '    for (int i = 0; i < 5; i++) printf("%d ", a[i]);\n'
                '    printf("\\n");\n'
                '    for (int i = 0; i < 3; i++) printf("%ld ", b[i]);\n'
                '    printf("\\n");\n'
                '    for (int i = 0; i < 4; i++) printf("%.2f ", c[i]);\n'
                '    printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'int CAT(add_, n)(int x) { return x + (n); } — CAT с двумя уровнями склеивает add_ и число. Не '
              'забудьте сами вызовы DEFINE_… после определений макросов.',
      'expected': ['11 15 0', '-2 0 3 5 9', '-5 42 1000000000000', '-1.25 0.00 2.25 2.50']},
     {'id': 'c7-x-enum',
      'mode': 'c',
      'title': 'X-макрос: цвета в одном списке',
      'statement': 'В одном списке COLORS(X) с элементами X(RED, "red", 0xFF0000), X(GREEN, "green", '
                   '0x00FF00), X(BLUE, "blue", 0x0000FF), X(YELLOW, "yellow", 0xFFFF00), X(BLACK, "black", '
                   '0x000000) постройте: enum color (элементы RED… и COLOR_COUNT), color_name(c) → строка '
                   'или "?" для неверного значения, color_rgb(c) → число или −1, color_from_name(s) → '
                   'значение enum или −1.',
      'starter': '#include <string.h>\n'
                 '\n'
                 'enum color { COLOR_COUNT };\n'
                 '\n'
                 'const char *color_name(int c) { return ""; }\n'
                 'long color_rgb(int c) { return 0; }\n'
                 'int color_from_name(const char *s) { return -2; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static int src_count(const char *pat) {\n'
                '    FILE *f = fopen("/sandbox/main.c", "r");\n'
                '    static char buf[1 << 17];\n'
                '    size_t n = fread(buf, 1, sizeof buf - 1, f);\n'
                '    buf[n] = 0;\n'
                '    char *mk = strstr(buf, "/*__" "DRIVER__*/");\n'
                '    if (mk) *mk = 0;\n'
                '    fclose(f);\n'
                '    int c = 0;\n'
                '    for (char *p = buf; (p = strstr(p, pat)) != NULL; p += strlen(pat)) c++;\n'
                '    return c;\n'
                '}\n'
                'int main(void) {\n'
                '    printf("%d %d %d %d %d %d\\n", RED, GREEN, BLUE, YELLOW, BLACK, COLOR_COUNT);\n'
                '    for (int c = -1; c <= COLOR_COUNT; c++) printf("%d:%s:%ld ", c, color_name(c), '
                'color_rgb(c));\n'
                '    printf("\\n");\n'
                '    printf("%d %d %d %d\\n", color_from_name("blue"), color_from_name("red"), '
                'color_from_name("pink"), color_from_name(""));\n'
                '    printf("list-once: %d\\n", src_count("yel" "low") == 1);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Один список COLORS(X); разные определения X: AS_ENUM → id, ; AS_NAME → [id] = name, ; AS_RGB '
              '→ [id] = rgb, — и каждый раз COLORS(AS_…).',
      'expected': ['0 1 2 3 4 5',
                   '-1:?:-1 0:red:16711680 1:green:65280 2:blue:255 3:yellow:16776960 4:black:0 5:?:-1',
                   '2 0 -1 -1',
                   'list-once: 1']},
     {'id': 'c7-x-struct',
      'mode': 'c',
      'title': 'X-макрос: структура и печать из списка полей',
      'statement': 'Список полей FIELDS(X): X(int, id, "%d"), X(double, score, "%.1f"), X(char, grade, '
                   '"%c"), X(long, big, "%ld"). Постройте из него struct rec, функцию rec_print(const struct '
                   'rec *) (печатает «id=1 score=2.5 grade=A big=7» одной строкой, поля через пробел, затем '
                   'перевод строки) и константу FIELD_COUNT — число полей (вычислите макросом, например, '
                   'через сумму единиц).',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'struct rec { int id; };\n'
                 '\n'
                 'void rec_print(const struct rec *r) {}\n'
                 '\n'
                 'enum { FIELD_COUNT = 0 };\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                "    struct rec a = {1, 2.5, 'A', 7};\n"
                "    struct rec b = {-5, 100.04, 'z', 1234567890123L};\n"
                '    rec_print(&a);\n'
                '    rec_print(&b);\n'
                '    printf("%d %zu\\n", FIELD_COUNT, sizeof(struct rec) >= sizeof(int) + sizeof(double) + '
                'sizeof(char) + sizeof(long));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Один список; DECL(type, name, fmt) → type name; PRINT → printf(#name "=" fmt, …); ONE → +1 '
              'для счётчика.',
      'expected': ['id=1 score=2.5 grade=A big=7', 'id=-5 score=100.0 grade=z big=1234567890123', '4 1']},
     {'id': 'c7-loop-macros',
      'mode': 'c',
      'title': 'Макросы-циклы: FOR, REPEAT, FOREACH, FOR_RANGE',
      'statement': 'FOR(i, n) — цикл i от 0 до n−1; REPEAT(n) — повторить тело n раз (без видимой '
                   'переменной); FOR_RANGE(i, a, b) — i от a до b − 1 включительно; FOREACH(p, arr) — p '
                   'пробегает указатели на элементы массива arr (число элементов — через ARRAY_SIZE, макрос '
                   'готов). Тело — следующий оператор или блок; n вычисляется один раз.',
      'starter': '#define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))\n'
                 '\n'
                 '#define FOR(i, n)\n'
                 '#define REPEAT(n)\n'
                 '#define FOR_RANGE(i, a, b)\n'
                 '#define FOREACH(p, arr)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static int calls;\n'
                'static int five(void) { calls++; return 5; }\n'
                '\n'
                'int main(void) {\n'
                '    FOR(i, 4) printf("%d ", i);\n'
                '    printf("\\n");\n'
                '    FOR(i, five()) printf("%d ", i * i);\n'
                '    printf("%d\\n", calls);\n'
                '    int s = 0;\n'
                '    REPEAT(3) s += 10;\n'
                '    REPEAT(0) s += 1000;\n'
                '    printf("%d\\n", s);\n'
                '    FOR_RANGE(k, 3, 7) printf("%d ", k);\n'
                '    printf("\\n");\n'
                '    FOR_RANGE(k, 5, 5) printf("never");\n'
                '    int n = 0;\n'
                '    FOR_RANGE(a, -2, 2) {\n'
                '        FOR_RANGE(b, a, 2) n++;\n'
                '    }\n'
                '    printf("%d\\n", n);\n'
                '    int v[] = {3, 1, 4, 1, 5};\n'
                '    FOREACH(p, v) *p *= 2;\n'
                '    FOREACH(q, v) printf("%d ", *q);\n'
                '    printf("\\n");\n'
                '    const char *w[] = {"x", "yy", "zzz"};\n'
                '    FOREACH(pw, w) printf("%s:%zu ", *pw, strlen(*pw));\n'
                '    printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Цикл с объявлением счётчика и «замороженной» границей: for (int i = 0, _n_##i = (n); i < '
              '_n_##i; i++). FOREACH: указатель от начала до arr + ARRAY_SIZE(arr).',
      'expected': ['0 1 2 3', '0 1 4 9 16 1', '30', '3 4 5 6', '10', '6 2 8 2 10', 'x:1 yy:2 zzz:3']},
     {'id': 'c7-log-macro',
      'mode': 'c',
      'title': 'Макрос журнала с переменным числом аргументов',
      'statement': 'LOG(fmt, ...) печатает «[имя_функции] сообщение» и перевод строки (имя — __func__); '
                   'сообщение — форматная строка и любые аргументы, в том числе ни одного: LOG("start"). '
                   'LOGL(level, fmt, ...) — то же, но с уровнем (его текст берётся строкизацией): «[INFO '
                   'имя_функции] сообщение». Аргументы fmt — всегда строковые литералы.',
      'starter': '#include <stdio.h>\n\n#define LOG(fmt, ...)\n#define LOGL(level, fmt, ...)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static int compute(int a, int b) {\n'
                '    LOG("compute(%d, %d)", a, b);\n'
                '    int r = a * b;\n'
                '    LOGL(DEBUG, "result=%d", r);\n'
                '    return r;\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    LOG("start");\n'
                '    int r = compute(6, 7);\n'
                '    LOGL(INFO, "got %d and %s", r, "done");\n'
                '    LOGL(WARN, "no args");\n'
                '    if (r > 40) LOG("big: %d", r); else LOG("small");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'printf("[%s] " fmt "\\n", __func__, ##__VA_ARGS__) — ## перед __VA_ARGS__ убирает запятую, '
              'когда аргументов нет. Уровень: #level.',
      'expected': ['[main] start',
                   '[compute] compute(6, 7)',
                   '[DEBUG compute] result=42',
                   '[INFO main] got 42 and done',
                   '[WARN main] no args',
                   '[main] big: 42']},
     {'id': 'c7-my-assert',
      'mode': 'c',
      'title': 'Свой ASSERT с текстом условия',
      'statement': 'Напишите счётчики проверок (g_passed, g_failed), макросы CHECK(cond) и CHECK_EQ(a, b) и '
                   'функцию report(). CHECK при провале печатает «FAIL: текст_условия», CHECK_EQ — «FAIL: a '
                   '== b (получили X, ожидали Y)» (значения как long long). report() печатает «passed P, '
                   'failed F». Макросы не должны завершать программу и должны вычислять аргументы один раз.',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'static int g_passed, g_failed;\n'
                 '\n'
                 '#define CHECK(cond)\n'
                 '#define CHECK_EQ(a, b)\n'
                 '\n'
                 'void report(void) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static int calls;\n'
                'static int tick(void) { return ++calls; }\n'
                'static int sq(int x) { return x * x; }\n'
                '\n'
                'int main(void) {\n'
                '    CHECK(1 + 1 == 2);\n'
                '    CHECK(sq(3) == 8);\n'
                '    CHECK_EQ(sq(4), 16);\n'
                '    CHECK_EQ(sq(5), 24);\n'
                '    CHECK_EQ(tick(), 1);\n'
                '    CHECK(tick() == 2);\n'
                '    printf("calls=%d\\n", calls);\n'
                '    if (calls > 5) CHECK(0); else CHECK_EQ(10 / 3, 3);\n'
                "    CHECK_EQ('a' + 1, 'b');\n"
                '    CHECK_EQ(sizeof(int), 8);\n'
                '    report();\n'
                '    return 0;\n'
                '}\n',
      'hint': '#cond даёт текст условия. Оборачивайте в do { … } while (0): драйвер использует макросы в '
              'if/else. В CHECK_EQ сохраните a и b во временные long long.',
      'expected': ['FAIL: sq(3) == 8',
                   'FAIL: sq(5) == 24 (получили 25, ожидали 24)',
                   'calls=2',
                   'FAIL: sizeof(int) == 8 (получили 4, ожидали 8)',
                   'passed 6, failed 3']},
     {'id': 'c7-platform',
      'mode': 'c',
      'title': 'Условная компиляция: платформа, разрядность, стандарт',
      'statement': 'Напишите функции, выбирающие значение директивами #if/#ifdef/#elif (не вычислением во '
                   'время работы): os_name() → "linux" (если определён __linux__), "windows" (_WIN32), "mac" '
                   '(__APPLE__), иначе "other"; ptr_bits() → 64 или 32 по __SIZEOF_POINTER__; c_year() → '
                   '1999, 2011, 2017 или 2023 по __STDC_VERSION__ (иначе 1990); compiler() → "gcc" (__GNUC__ '
                   'без __clang__), "clang" или "unknown". Используйте не менее трёх директив условной '
                   'компиляции.',
      'starter': 'const char *os_name(void) { return ""; }\n'
                 'int ptr_bits(void) { return 0; }\n'
                 'int c_year(void) { return 0; }\n'
                 'const char *compiler(void) { return ""; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static int src_count(const char *pat) {\n'
                '    FILE *f = fopen("/sandbox/main.c", "r");\n'
                '    static char buf[1 << 17];\n'
                '    size_t n = fread(buf, 1, sizeof buf - 1, f);\n'
                '    buf[n] = 0;\n'
                '    char *mk = strstr(buf, "/*__" "DRIVER__*/");\n'
                '    if (mk) *mk = 0;\n'
                '    fclose(f);\n'
                '    int c = 0;\n'
                '    for (char *p = buf; (p = strstr(p, pat)) != NULL; p += strlen(pat)) c++;\n'
                '    return c;\n'
                '}\n'
                'int main(void) {\n'
                '    printf("%s %d %d %s\\n", os_name(), ptr_bits(), c_year(), compiler());\n'
                '    int dirs = src_count("#" "if") + src_count("#e" "lif");\n'
                '    printf("directives: %d\\n", dirs >= 3);\n'
                '    return 0;\n'
                '}\n',
      'hint': '#if defined(__linux__) … #elif … #else … #endif прямо внутри функции; в каждой ветке свой '
              'return.',
      'expected': ['linux 64 2011 gcc', 'directives: 1']},
     {'id': 'c7-fix-parens',
      'mode': 'c',
      'title': 'Исправьте: скобки в макросах',
      'statement': 'Макросы SQ, DOUBLE, DIFF и AVG определены без нужных скобок и дают неверные результаты '
                   'на выражениях. Исправьте определения (только скобки — смысл макросов тот же): SQ(x) — '
                   'квадрат, DOUBLE(x) — x + x, DIFF(a, b) — a − b, AVG(a, b) — (a + b) / 2.',
      'starter': '#define SQ(x) x * x\n'
                 '#define DOUBLE(x) x + x\n'
                 '#define DIFF(a, b) a - b\n'
                 '#define AVG(a, b) a + b / 2\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a = 3, b = 4;\n'
                '    printf("%d %d %d\\n", SQ(a + b), SQ(a - b), 20 / SQ(2));\n'
                '    printf("%d %d %d\\n", DOUBLE(a) * 3, DOUBLE(a + b), 100 - DOUBLE(10));\n'
                '    printf("%d %d %d\\n", DIFF(a, b), 10 - DIFF(a, b), DIFF(a, b - 1));\n'
                '    printf("%d %d %d\\n", AVG(a, b), AVG(10, 20), AVG(a + 1, b + 1) * 2);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Правило: каждый параметр в теле — в скобках, и всё тело целиком — в скобках.',
      'expected': ['49 1 5', '18 14 80', '-1 11 0', '3 15 8']},
     {'id': 'c7-fix-double-eval',
      'mode': 'c',
      'title': 'Исправьте: MAX вычисляет аргумент дважды',
      'statement': 'MAX и MIN вычисляют каждый аргумент дважды — вызовы функций с побочными эффектами '
                   'выполняются лишний раз. Перепишите их так, чтобы каждый аргумент вычислялся один раз '
                   '(выражение-оператор GNU или статические встраиваемые функции для int и double — драйвер '
                   'вызывает макросы и с int, и с double).',
      'starter': '#define MAX(a, b) ((a) > (b) ? (a) : (b))\n#define MIN(a, b) ((a) < (b) ? (a) : (b))\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static int calls;\n'
                'static int val(int x) { calls++; return x; }\n'
                'static double vald(double x) { calls++; return x; }\n'
                '\n'
                'int main(void) {\n'
                '    int m = MAX(val(3), val(8));\n'
                '    printf("%d %d\\n", m, calls);\n'
                '    calls = 0;\n'
                '    m = MIN(val(3), val(8));\n'
                '    printf("%d %d\\n", m, calls);\n'
                '    calls = 0;\n'
                '    double d = MAX(vald(1.5), vald(0.5));\n'
                '    printf("%.1f %d\\n", d, calls);\n'
                '    int i = 5, j = 2;\n'
                '    int r = MAX(i++, j);\n'
                '    printf("%d %d %d\\n", r, i, j);\n'
                '    r = MIN(--i, j + 10);\n'
                '    printf("%d %d\\n", r, i);\n'
                '    return 0;\n'
                '}\n',
      'hint': '({ __typeof__(a) _a = (a); __typeof__(b) _b = (b); _a > _b ? _a : _b; })',
      'expected': ['8 2', '3 2', '1.5 2', '5 6 2', '5 5']},
     {'id': 'c7-fix-swap-scope',
      'mode': 'c',
      'title': 'Исправьте: SWAP ломается в if/else',
      'statement': 'SWAP определён как три отдельных оператора с переменной t: он не компилируется в if/else '
                   'без фигурных скобок, а если в вызывающем коде уже есть t, результат неверен. Исправьте '
                   'макрос: одна «операторная» обёртка и уникальное имя временной переменной (тип — '
                   '__typeof__(a)).',
      'starter': '#define SWAP(a, b) __typeof__(a) t = a; a = b; b = t;\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int t = 10, u = 20;\n'
                '    SWAP(t, u);\n'
                '    printf("%d %d\\n", t, u);\n'
                '    int x = 1, y = 2;\n'
                '    if (x < y) SWAP(x, y); else x = 0;\n'
                '    printf("%d %d\\n", x, y);\n'
                '    if (x < y) SWAP(x, y); else x = 100;\n'
                '    printf("%d %d\\n", x, y);\n'
                '    for (int i = 0; i < 3; i++) SWAP(x, y);\n'
                '    printf("%d %d\\n", x, y);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'do { … } while (0) и имя вроде _swap_t. Точка с запятой в самом макросе не нужна.',
      'expected': ['20 10', '2 1', '100 1', '1 100']},
     {'id': 'c7-fix-xstr',
      'mode': 'c',
      'title': 'Исправьте: номер версии в строке',
      'statement': 'VERSION_STR должна давать строку из макросов VMAJOR и VMINOR («3.14»), а даёт '
                   '«VMAJOR.VMINOR». Исправьте STR (добавьте уровень, раскрывающий макросы) и определение '
                   'VERSION_STR; BUILD_TAG(x) должен давать строку «build-» и числовое значение макроса '
                   'BUILD_NO (например, «build-742»).',
      'starter': '#define VMAJOR 3\n'
                 '#define VMINOR 14\n'
                 '#define BUILD_NO 742\n'
                 '\n'
                 '#define STR(x) #x\n'
                 '#define VERSION_STR STR(VMAJOR) "." STR(VMINOR)\n'
                 '#define BUILD_TAG "build-" STR(BUILD_NO)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%s\\n%s\\n", VERSION_STR, BUILD_TAG);\n'
                '    printf("%zu %zu\\n", strlen(VERSION_STR), strlen(BUILD_TAG));\n'
                '    printf("%s %s\\n", STR(VMAJOR), STR(a b));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Нужны два макроса: STR_(x) #x и STR(x) STR_(x) — внешний раскрывает аргумент, внутренний '
              'превращает в строку.',
      'expected': ['3.14', 'build-742', '4 9', '3 a b']},
     {'id': 'c7-fix-semicolon',
      'mode': 'c',
      'title': 'Исправьте: лишняя точка с запятой и два оператора',
      'statement': 'PRINT_INT и ALLOC_ZERO определены с ошибками: PRINT_INT заканчивается точкой с запятой '
                   '(ломает if/else), ALLOC_ZERO — два оператора без обёртки (второй выполняется вне '
                   'условия). Исправьте оба макроса: вызов с «;» снаружи должен работать в if/else; '
                   'ALLOC_ZERO(p, n) выделяет n элементов типа *p через calloc.',
      'starter': '#include <stdio.h>\n'
                 '#include <stdlib.h>\n'
                 '\n'
                 '#define PRINT_INT(x) printf("%d\\n", x);\n'
                 '#define ALLOC_ZERO(p, n) p = calloc(n, sizeof *p); allocs++\n'
                 '\n'
                 'static int allocs;\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int c = 1;\n'
                '    if (c) PRINT_INT(1); else PRINT_INT(2);\n'
                '    if (!c) PRINT_INT(3); else PRINT_INT(4);\n'
                '    int *a = NULL, *b = NULL;\n'
                '    if (!c) ALLOC_ZERO(a, 10);\n'
                '    if (c) ALLOC_ZERO(b, 5); else ALLOC_ZERO(a, 7);\n'
                '    printf("%d %d %d\\n", a == NULL, b != NULL, allocs);\n'
                '    printf("%d %d\\n", b[0], b[4]);\n'
                '    free(b);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'PRINT_INT без завершающей «;»; ALLOC_ZERO — do { … } while (0).',
      'expected': ['1', '4', '1 1 1', '0 0']},
     {'id': 'c7-generic-macros',
      'mode': 'c',
      'title': '_Generic: ABS и TYPE_NAME',
      'statement': 'ABS(x) — модуль для int, long, long long, float и double (выбор функции по типу через '
                   '_Generic: abs, labs, llabs, fabsf, fabs). TYPE_NAME(x) → строка с названием типа: "int", '
                   '"long", "double", "float", "char *", "unsigned", иначе "other". IS_FLOAT(x) → 1 для '
                   'float и double, иначе 0.',
      'starter': '#include <stdlib.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 '#define ABS(x) (x)\n'
                 '#define TYPE_NAME(x) ""\n'
                 '#define IS_FLOAT(x) 0\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int i = -5;\n'
                '    long l = -5000000000L;\n'
                '    long long ll = -9000000000000LL;\n'
                '    float f = -2.5f;\n'
                '    double d = -0.125;\n'
                '    printf("%d %ld %lld %.1f %.3f\\n", ABS(i), ABS(l), ABS(ll), ABS(f), ABS(d));\n'
                '    printf("%d %.1f\\n", ABS(-7), ABS(-7.5));\n'
                '    char *s = "x";\n'
                '    unsigned u = 3;\n'
                '    short sh = 1;\n'
                '    printf("%s %s %s %s %s %s %s\\n", TYPE_NAME(i), TYPE_NAME(l), TYPE_NAME(d), '
                'TYPE_NAME(f), TYPE_NAME(s), TYPE_NAME(u), TYPE_NAME(&sh));\n'
                '    printf("%s %s\\n", TYPE_NAME(1 + 2), TYPE_NAME(1.0 * 2));\n'
                '    printf("%d %d %d %d\\n", IS_FLOAT(f), IS_FLOAT(d), IS_FLOAT(i), IS_FLOAT(s));\n'
                '    return 0;\n'
                '}\n',
      'hint': '_Generic((x), int: abs, long: labs, …)(x) — выбирается функция, затем она вызывается. Для '
              'TYPE_NAME — ветки со строками и default.',
      'expected': ['5 5000000000 9000000000000 2.5 0.125',
                   '7 7.5',
                   'int long double float char * unsigned other',
                   'int double',
                   '1 1 0 0']},
     {'id': 'c7-container-of',
      'mode': 'c',
      'title': 'Свой offsetof и container_of',
      'statement': 'MY_OFFSETOF(type, member) → смещение поля в байтах (типа size_t; без offsetof из '
                   'stddef.h — через нулевой указатель); CONTAINER_OF(ptr, type, member) → указатель на '
                   'структуру type, внутри которой лежит поле member по адресу ptr. Используйте их для '
                   'списка, встроенного в структуры.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 '#define MY_OFFSETOF(type, member) ((size_t)0)\n'
                 '#define CONTAINER_OF(ptr, type, member) ((type *)0)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static int src_count(const char *pat) {\n'
                '    FILE *f = fopen("/sandbox/main.c", "r");\n'
                '    static char buf[1 << 17];\n'
                '    size_t n = fread(buf, 1, sizeof buf - 1, f);\n'
                '    buf[n] = 0;\n'
                '    char *mk = strstr(buf, "/*__" "DRIVER__*/");\n'
                '    if (mk) *mk = 0;\n'
                '    fclose(f);\n'
                '    int c = 0;\n'
                '    for (char *p = buf; (p = strstr(p, pat)) != NULL; p += strlen(pat)) c++;\n'
                '    return c;\n'
                '}\n'
                'struct list { struct list *next; };\n'
                'struct task { int id; char name[10]; struct list link; double w; };\n'
                'struct pair { char c; struct { int a; int b; } in; long l; };\n'
                '\n'
                'int main(void) {\n'
                '    printf("%zu %zu %zu\\n", MY_OFFSETOF(struct task, id), MY_OFFSETOF(struct task, name), '
                'MY_OFFSETOF(struct task, link));\n'
                '    printf("%zu %zu\\n", MY_OFFSETOF(struct task, w), MY_OFFSETOF(struct pair, l));\n'
                '    printf("%d\\n", MY_OFFSETOF(struct task, link) == offsetof(struct task, link) && '
                'MY_OFFSETOF(struct pair, in.b) == offsetof(struct pair, in.b));\n'
                '    struct task t1 = {1, "one", {NULL}, 1.5}, t2 = {2, "two", {NULL}, 2.5};\n'
                '    t1.link.next = &t2.link;\n'
                '    for (struct list *p = &t1.link; p; p = p->next) {\n'
                '        struct task *t = CONTAINER_OF(p, struct task, link);\n'
                '        printf("%d:%s:%.1f ", t->id, t->name, t->w);\n'
                '    }\n'
                '    printf("\\n");\n'
                '    int *pb = &t2.id;\n'
                '    struct task *back = CONTAINER_OF(pb, struct task, id);\n'
                '    printf("%d\\n", back == &t2);\n'
                '    printf("builtin: %d\\n", src_count("offs" "etof("));\n'
                '    return 0;\n'
                '}\n',
      'hint': '(size_t)&((type *)0)->member — адрес поля у «нулевой» структуры равен смещению. CONTAINER_OF: '
              '(type *)((char *)(ptr) − смещение).',
      'expected': ['0 4 16', '24 16', '1', '1:one:1.5 2:two:2.5', '1', 'builtin: 0']},
     {'id': 'c7-count-args',
      'mode': 'c',
      'title': 'Подсчёт аргументов макроса',
      'statement': 'COUNT_ARGS(...) → число аргументов (от 1 до 8) — приём со сдвигом списка; FIRST(...) → '
                   'первый аргумент; IS_SINGLE(...) → 1, если аргумент ровно один, иначе 0. Запятые внутри '
                   'круглых скобок аргумента (вызов f(1, 2)) не считаются разделителями.',
      'starter': '#define COUNT_ARGS(...) 0\n#define FIRST(...) 0\n#define IS_SINGLE(...) 0\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static int f(int a, int b) { return a * 10 + b; }\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d %d\\n", COUNT_ARGS(a), COUNT_ARGS(a, b), COUNT_ARGS(1, 2, 3), '
                'COUNT_ARGS(1, 2, 3, 4, 5, 6, 7, 8));\n'
                '    printf("%d %d\\n", COUNT_ARGS(f(1, 2), 3), COUNT_ARGS((1, 2, 3)));\n'
                '    printf("%d %d %d\\n", FIRST(7, 8, 9), FIRST(42), FIRST(f(3, 4), 5));\n'
                '    printf("%d %d %d\\n", IS_SINGLE(x), IS_SINGLE(x, y), IS_SINGLE((1, 2)));\n'
                '    int arr[] = { 10, 20, 30, 40 };\n'
                '    printf("%d\\n", sizeof(arr) / sizeof(arr[0]) == COUNT_ARGS(10, 20, 30, 40));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'COUNT_N(_1, …, _8, N, …) N: перед списком чисел вставляется __VA_ARGS__, и N «съезжает» на '
              'число аргументов.',
      'expected': ['1 2 3 8', '2 1', '7 42 34', '1 0 1', '1']},
     {'id': 'c7-vararg-sum',
      'mode': 'c',
      'title': 'SUM, MAXOF, MEAN от списка аргументов',
      'statement': 'COUNT_ARGS(...) уже готов (1…8 аргументов). Напишите функции sum_ints(const int *a, int '
                   'n), max_ints(const int *a, int n), mean_ints(const int *a, int n) → double и макросы '
                   'SUM(...), MAXOF(...), MEAN(...), которые передают список аргументов в функцию через '
                   'составной литерал (int[]){…} и число аргументов через COUNT_ARGS.',
      'starter': '#define COUNT_N(_1, _2, _3, _4, _5, _6, _7, _8, N, ...) N\n'
                 '#define COUNT_ARGS(...) COUNT_N(__VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0)\n'
                 '\n'
                 'int sum_ints(const int *a, int n) { return 0; }\n'
                 'int max_ints(const int *a, int n) { return 0; }\n'
                 'double mean_ints(const int *a, int n) { return 0; }\n'
                 '\n'
                 '#define SUM(...) 0\n'
                 '#define MAXOF(...) 0\n'
                 '#define MEAN(...) 0.0\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a = 4, b = -9;\n'
                '    printf("%d %d %d\\n", SUM(1), SUM(1, 2, 3, 4), SUM(a, b, a * b));\n'
                '    printf("%d %d %d\\n", MAXOF(5), MAXOF(3, 9, 2), MAXOF(a, b, 0, -100, 3));\n'
                '    printf("%.2f %.2f %.3f\\n", MEAN(7), MEAN(1, 2), MEAN(1, 1, 2, 3, 5, 8, 13, 21));\n'
                '    printf("%d\\n", SUM(1, 2, 3, 4, 5, 6, 7, 8) - MAXOF(1, 2, 3, 4, 5, 6, 7, 8));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Составной литерал (int[]){ __VA_ARGS__ } создаёт безымянный массив прямо в выражении.',
      'expected': ['1 10 -41', '5 9 4', '7.00 1.50 6.750', '28']},
     {'id': 'c7-overload',
      'mode': 'c',
      'title': '«Перегрузка» макроса по числу аргументов',
      'statement': 'COUNT_ARGS готов. Напишите макрос CAT (с двумя уровнями), макросы ADD1, ADD2, ADD3 и '
                   'общий ADD(...), выбирающий нужный по числу аргументов: ADD(a) → a, ADD(a, b) → a + b, '
                   'ADD(a, b, c) → a + b + c. Затем POINT(...): struct pt { int x, y, z; } — POINT(x) → {x, '
                   '0, 0}, POINT(x, y) → {x, y, 0}, POINT(x, y, z) → {x, y, z} (составные литералы).',
      'starter': '#define COUNT_N(_1, _2, _3, N, ...) N\n'
                 '#define COUNT_ARGS(...) COUNT_N(__VA_ARGS__, 3, 2, 1, 0)\n'
                 '\n'
                 'struct pt { int x, y, z; };\n'
                 '\n'
                 '#define ADD(...) 0\n'
                 '#define POINT(...) ((struct pt){0})\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a = 5, b = 6;\n'
                '    printf("%d %d %d\\n", ADD(a), ADD(a, b), ADD(a, b, a * b));\n'
                '    printf("%d\\n", 2 * ADD(1, 2) + ADD(10));\n'
                '    struct pt p = POINT(1), q = POINT(a, b), r = POINT(a + 1, b + 1, 9);\n'
                '    printf("%d %d %d / %d %d %d / %d %d %d\\n", p.x, p.y, p.z, q.x, q.y, q.z, r.x, r.y, '
                'r.z);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'ADD(...) CAT(ADD, COUNT_ARGS(__VA_ARGS__))(__VA_ARGS__) — выбираем имя макроса склейкой ADD и '
              'числа аргументов.',
      'expected': ['5 11 41', '16', '1 0 0 / 5 6 0 / 6 7 9']},
     {'id': 'c7-x-ops',
      'mode': 'c',
      'title': 'X-макрос: операции, таблица функций и имена',
      'statement': 'В одном списке OPS(X) опишите операции: X(ADD, "add", a + b), X(SUB, "sub", a - b), '
                   'X(MUL, "mul", a * b), X(DIV, "div", b ? a / b : 0), X(MOD, "mod", b ? a % b : 0). Из '
                   'него постройте enum op (OP_ADD, … и OP_COUNT), функции op_add…, таблицу указателей на '
                   'них, таблицу имён; exec(op, a, b, *ok) — выполнить (ok = 0 для неверного кода, результат '
                   '0); op_by_name(s) → код или −1.',
      'starter': '#include <string.h>\n'
                 '\n'
                 'enum op { OP_COUNT };\n'
                 '\n'
                 'int exec(int op, int a, int b, int *ok) {\n'
                 '    *ok = 0;\n'
                 '    return 0;\n'
                 '}\n'
                 'int op_by_name(const char *s) { return -2; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static int src_count(const char *pat) {\n'
                '    FILE *f = fopen("/sandbox/main.c", "r");\n'
                '    static char buf[1 << 17];\n'
                '    size_t n = fread(buf, 1, sizeof buf - 1, f);\n'
                '    buf[n] = 0;\n'
                '    char *mk = strstr(buf, "/*__" "DRIVER__*/");\n'
                '    if (mk) *mk = 0;\n'
                '    fclose(f);\n'
                '    int c = 0;\n'
                '    for (char *p = buf; (p = strstr(p, pat)) != NULL; p += strlen(pat)) c++;\n'
                '    return c;\n'
                '}\n'
                'int main(void) {\n'
                '    printf("%d %d %d %d %d %d\\n", OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD, OP_COUNT);\n'
                '    const char *n[] = {"add", "sub", "mul", "div", "mod", "pow", ""};\n'
                '    for (int i = 0; i < 7; i++) {\n'
                '        int code = op_by_name(n[i]);\n'
                '        int ok;\n'
                '        int r = exec(code, 17, 5, &ok);\n'
                '        printf("%s %d %d %d\\n", n[i], code, ok, r);\n'
                '    }\n'
                '    int ok;\n'
                '    int r = exec(OP_DIV, 9, 0, &ok);\n'
                '    printf("%d %d\\n", r, ok);\n'
                '    r = exec(99, 1, 1, &ok);\n'
                '    printf("%d %d\\n", r, ok);\n'
                '    r = exec(-1, 1, 1, &ok);\n'
                '    printf("%d %d\\n", r, ok);\n'
                '    printf("list-once: %d\\n", src_count("m" "od") == 1);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Один список OPS(X): AS_ENUM → OP_##id, ; AS_FUNC → static int op_##id(int a, int b) { return '
              'expr; } ; AS_PTR и AS_NAME → элементы таблиц с [OP_##id] = …',
      'expected': ['0 1 2 3 4 5',
                   'add 0 1 22',
                   'sub 1 1 12',
                   'mul 2 1 85',
                   'div 3 1 3',
                   'mod 4 1 2',
                   'pow -1 0 0',
                   ' -1 0 0',
                   '0 1',
                   '0 0',
                   '0 0',
                   'list-once: 1']},
     {'id': 'c7-field-dump',
      'mode': 'c',
      'title': 'Макросы для печати полей структуры',
      'statement': 'FIELD(s, f) — печатает «f=значение» (поле int структуры s, доступ через точку), '
                   'FIELDP(p, f) — то же для указателя (доступ через ->). DUMP2(s, a, b) и DUMP3(s, a, b, c) '
                   '— печатают «{a=1, b=2}» и «{a=1, b=2, c=3}» и перевод строки; имена полей берутся из '
                   'текста аргументов (строкизация). Структуры — только с полями int.',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 '#define FIELD(s, f)\n'
                 '#define FIELDP(p, f)\n'
                 '#define DUMP2(s, a, b)\n'
                 '#define DUMP3(s, a, b, c)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'struct point { int x, y, z; };\n'
                'struct dev { int id, irq, base; };\n'
                '\n'
                'int main(void) {\n'
                '    struct point p = {1, -2, 3};\n'
                '    struct dev d = {7, 11, 4096};\n'
                '    struct dev *pd = &d;\n'
                '    FIELD(p, y);\n'
                '    printf("\\n");\n'
                '    FIELDP(pd, base);\n'
                '    printf("\\n");\n'
                '    DUMP3(p, x, y, z);\n'
                '    DUMP2(d, irq, id);\n'
                '    DUMP2(*pd, base, irq);\n'
                '    if (p.x > 0) DUMP2(p, z, x); else DUMP3(p, x, y, z);\n'
                '    return 0;\n'
                '}\n',
      'hint': '#f превращает имя поля в строку; (s).f — доступ к полю по имени из аргумента. DUMP — do { … } '
              'while (0).',
      'expected': ['y=-2',
                   'base=4096',
                   '{x=1, y=-2, z=3}',
                   '{irq=11, id=7}',
                   '{base=4096, irq=11}',
                   '{z=3, x=1}']},
     {'id': 'c7-mini-test',
      'mode': 'c',
      'title': 'Мини-фреймворк тестов на макросах',
      'statement': 'Напишите макросы TEST(name) — определяет static void test_<name>(void); RUN(name) — '
                   'печатает «run name», вызывает тест, затем «ok name» или «FAILED name (N)», где N — число '
                   'провалов в этом тесте; EXPECT(cond) — при провале печатает «  fail: текст_условия» и '
                   'увеличивает счётчик; EXPECT_EQ(a, b) — «  fail: a == b (X != Y)» (значения как long '
                   'long, каждый аргумент вычисляется раз); summary() печатает «tests T, failed F» (F — '
                   'число упавших тестов).',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'static int cur_failed, tests, tests_failed;\n'
                 '\n'
                 '#define TEST(name)\n'
                 '#define RUN(name)\n'
                 '#define EXPECT(cond)\n'
                 '#define EXPECT_EQ(a, b)\n'
                 '\n'
                 'void summary(void) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static int calls;\n'
                'static int tick(void) { return ++calls; }\n'
                '\n'
                'TEST(arith) {\n'
                '    EXPECT(2 + 2 == 4);\n'
                '    EXPECT_EQ(3 * 3, 9);\n'
                '}\n'
                '\n'
                'TEST(broken) {\n'
                '    EXPECT(1 > 2);\n'
                '    EXPECT_EQ(10 / 3, 4);\n'
                '    EXPECT_EQ(7 % 4, 3);\n'
                '}\n'
                '\n'
                'TEST(once) {\n'
                '    EXPECT_EQ(tick(), 1);\n'
                '    EXPECT_EQ(tick(), 3);\n'
                '    EXPECT(calls == 2);\n'
                '}\n'
                '\n'
                'TEST(empty) {\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    RUN(arith);\n'
                '    RUN(broken);\n'
                '    RUN(once);\n'
                '    if (calls) RUN(empty); else RUN(arith);\n'
                '    summary();\n'
                '    return 0;\n'
                '}\n',
      'hint': 'TEST(name) → static void test_##name(void); в RUN используйте #name и test_##name. Счётчики — '
              'статические переменные выше макросов.',
      'expected': ['run arith',
                   'ok arith',
                   'run broken',
                   '  fail: 1 > 2',
                   '  fail: 10 / 3 == 4 (3 != 4)',
                   'FAILED broken (2)',
                   'run once',
                   '  fail: tick() == 3 (2 != 3)',
                   'FAILED once (1)',
                   'run empty',
                   'ok empty',
                   'tests 4, failed 2']},
     {'id': 'c7-genmask',
      'mode': 'c',
      'title': 'Битовые поля регистра: GENMASK, FIELD_PREP, FIELD_GET',
      'statement': 'GENMASK(h, l) — 32-битная маска с единицами в битах от h до l включительно (0 ≤ l ≤ h ≤ '
                   '31, unsigned); FIELD_PREP(mask, val) — поместить val в позицию поля (val сдвигается к '
                   'младшему биту маски и обрезается маской); FIELD_GET(mask, reg) — извлечь поле из reg; '
                   'FIELD_MAX(mask) — наибольшее значение поля. Для сдвига пользуйтесь __builtin_ctz(mask).',
      'starter': '#define GENMASK(h, l) 0u\n'
                 '#define FIELD_PREP(mask, val) 0u\n'
                 '#define FIELD_GET(mask, reg) 0u\n'
                 '#define FIELD_MAX(mask) 0u\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                '#define REG_VER GENMASK(31, 24)\n'
                '#define REG_MODE GENMASK(7, 4)\n'
                '#define REG_EN GENMASK(0, 0)\n'
                '\n'
                'int main(void) {\n'
                '    printf("%#x %#x %#x %#x\\n", GENMASK(7, 0), GENMASK(31, 0), GENMASK(15, 8), GENMASK(31, '
                '31));\n'
                '    printf("%#x %#x %#x\\n", REG_VER, REG_MODE, REG_EN);\n'
                '    unsigned reg = FIELD_PREP(REG_VER, 0x42) | FIELD_PREP(REG_MODE, 5) | FIELD_PREP(REG_EN, '
                '1);\n'
                '    printf("%#x\\n", reg);\n'
                '    printf("%#x %u %u\\n", FIELD_GET(REG_VER, reg), FIELD_GET(REG_MODE, reg), '
                'FIELD_GET(REG_EN, reg));\n'
                '    printf("%#x\\n", FIELD_PREP(REG_MODE, 0xFF));\n'
                '    printf("%u %u %#x\\n", FIELD_MAX(REG_MODE), FIELD_MAX(REG_EN), FIELD_MAX(GENMASK(31, '
                '16)));\n'
                '    reg = (reg & ~REG_MODE) | FIELD_PREP(REG_MODE, 9);\n'
                '    printf("%#x %u\\n", reg, FIELD_GET(REG_MODE, reg));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'GENMASK: ((~0u) << l) & (~0u >> (31 − h)). FIELD_PREP: (val << ctz(mask)) & mask. FIELD_GET: '
              '(reg & mask) >> ctz(mask).',
      'expected': ['0xff 0xffffffff 0xff00 0x80000000',
                   '0xff000000 0xf0 0x1',
                   '0x42000051',
                   '0x42 5 1',
                   '0xf0',
                   '15 1 0xffff',
                   '0x42000091 9']},
     {'id': 'c7-try-macros',
      'mode': 'c',
      'title': 'Макросы TRY, CHECK и TRY_GOTO для обработки ошибок',
      'statement': 'Коды ошибок — отрицательные числа. TRY(expr): вычислить выражение один раз и, если '
                   'результат < 0, сразу вернуть его из функции. CHECK(cond, err): если условие ложно — '
                   'вернуть err. RET_IF_NULL(p, err): если p == NULL — вернуть err. TRY_GOTO(expr, label): '
                   'результат — в переменную rc (объявлена в вызывающей функции), при rc < 0 — переход на '
                   'label. Макросы работают как обычные операторы (в том числе в if/else).',
      'starter': '#define TRY(expr)\n'
                 '#define CHECK(cond, err)\n'
                 '#define RET_IF_NULL(p, err)\n'
                 '#define TRY_GOTO(expr, label)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static int calls;\n'
                'static int step(int x) { calls++; return x; }\n'
                '\n'
                'static int pipeline(int a, int b, int c) {\n'
                '    TRY(step(a));\n'
                '    TRY(step(b));\n'
                '    CHECK(c != 13, -13);\n'
                '    if (c > 100) TRY(step(-c)); else TRY(step(c));\n'
                '    return step(a + b + c);\n'
                '}\n'
                '\n'
                'static int first_char(const char *s) {\n'
                '    RET_IF_NULL(s, -1);\n'
                "    CHECK(*s != '\\0', -2);\n"
                '    return *s;\n'
                '}\n'
                '\n'
                'static int resources;\n'
                '\n'
                'static int with_cleanup(int a, int b) {\n'
                '    int rc = 0;\n'
                '    resources++;\n'
                '    TRY_GOTO(step(a), fail);\n'
                '    resources++;\n'
                '    TRY_GOTO(step(b), fail);\n'
                '    rc = a + b;\n'
                'fail:\n'
                '    resources = 0;\n'
                '    return rc;\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    int r = pipeline(1, 2, 3);\n'
                '    printf("%d %d\\n", r, calls);\n'
                '    calls = 0;\n'
                '    r = pipeline(1, -5, 3);\n'
                '    printf("%d %d\\n", r, calls);\n'
                '    calls = 0;\n'
                '    r = pipeline(1, 2, 13);\n'
                '    printf("%d %d\\n", r, calls);\n'
                '    calls = 0;\n'
                '    r = pipeline(1, 2, 200);\n'
                '    printf("%d %d\\n", r, calls);\n'
                '    printf("%d %d %d\\n", first_char("xyz"), first_char(""), first_char(NULL));\n'
                '    calls = 0;\n'
                '    int r1 = with_cleanup(4, 5);\n'
                '    int r2 = with_cleanup(-3, 5);\n'
                '    int r3 = with_cleanup(2, -9);\n'
                '    printf("%d %d %d %d %d\\n", r1, r2, r3, calls, resources);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'do { int _rc = (expr); if (_rc < 0) return _rc; } while (0) — выражение вычисляется один раз; '
              'TRY_GOTO присваивает rc и делает goto label.',
      'expected': ['6 4', '-5 2', '-13 2', '-200 3', '120 -2 -1', '9 -3 -9 5 0']},
     {'id': 'c7-with-scope',
      'mode': 'c',
      'title': 'WITH: пара «начало — конец» вокруг блока',
      'statement': 'WITH(init, fini) — выполнить init, затем следующий оператор (или блок) ровно один раз, '
                   'затем fini; пишется как for-цикл с одним проходом (ни goto, ни setjmp). LOCKED(l) — '
                   'частный случай: WITH(acquire(&l), release(&l)). Макросы вкладываются; init и fini '
                   'вычисляются по одному разу; тело выполняется один раз.',
      'starter': '#define WITH(init, fini)\n#define LOCKED(l)\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'struct lock { int held, acquired, released; };\n'
                'static char trace[128];\n'
                '\n'
                'static void acquire(struct lock *l) { l->held = 1; l->acquired++; strcat(trace, "A"); }\n'
                'static void release(struct lock *l) { l->held = 0; l->released++; strcat(trace, "R"); }\n'
                'static void say(const char *s) { strcat(trace, s); }\n'
                '\n'
                'int main(void) {\n'
                '    struct lock a = {0, 0, 0}, b = {0, 0, 0};\n'
                '    int counter = 0;\n'
                '    LOCKED(a) {\n'
                '        counter += a.held * 10;\n'
                '        say("body");\n'
                '    }\n'
                '    printf("%s %d %d %d %d\\n", trace, counter, a.held, a.acquired, a.released);\n'
                '    trace[0] = 0;\n'
                '    LOCKED(a) LOCKED(b) {\n'
                '        say("(");\n'
                '        counter += a.held + b.held;\n'
                '        say(")");\n'
                '    }\n'
                '    printf("%s %d %d %d\\n", trace, counter, a.acquired, b.released);\n'
                '    trace[0] = 0;\n'
                '    int n = 0;\n'
                '    WITH(say("<"), say(">")) n++;\n'
                '    WITH(say("["), say("]")) { n += 10; say("x"); }\n'
                '    printf("%s %d\\n", trace, n);\n'
                '    trace[0] = 0;\n'
                '    if (n > 5) LOCKED(a) say("then"); else say("else");\n'
                '    printf("%s\\n", trace);\n'
                '    for (int i = 0; i < 2; i++) WITH(say("{"), say("}")) say("i");\n'
                '    printf("%s\\n", trace);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'for (int _once = ((init), 1); _once; _once = 0, (fini)) — тело выполнится один раз, fini '
              'стоит в «приращении» цикла.',
      'expected': ['AbodyR 10 0 1 1', 'AA()RR 12 2 1', '<>[x] 11', 'AthenR', 'AthenR{i}{i}']}]}
