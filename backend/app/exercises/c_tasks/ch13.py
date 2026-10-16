"""Задачи книги «От assembler к языку C»: глава 13 (код компилируется gcc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {13: [{'id': 'c13-mini-framework',
       'mode': 'c',
       'title': 'Свой минимальный фреймворк юнит-тестов',
       'statement': 'struct tcase { const char *name; void (*fn)(void); }. Макросы (внутри тестов): '
                    'EXPECT_TRUE(c), EXPECT_EQ(a, b) (значения как long long, каждый аргумент вычисляется '
                    'один раз), EXPECT_STREQ(a, b) (строки, NULL допустим и равен только NULL), '
                    'EXPECT_NEAR(a, b, eps) (double). При провале печатается строка «  FAIL: <текст '
                    'выражения> (<подробности>)» — для EXPECT_TRUE «  FAIL: c», для EXPECT_EQ «  FAIL: a == '
                    'b (X vs Y)», для EXPECT_STREQ «  FAIL: a == b ("x" vs "y")» (NULL печатается как NULL), '
                    'для EXPECT_NEAR «  FAIL: |a - b| <= eps (X vs Y)» — и счётчик ошибок текущего теста '
                    'растёт; тест не прерывается. run_tests(cases, n) → число упавших тестов; для каждого '
                    'теста печатает «[ RUN  ] имя», затем «[  OK  ] имя» или «[ FAIL ] имя (N)»; в конце '
                    '«<P> passed, <F> failed». Числа double — «%g».',
       'starter': '#include <stdio.h>\n'
                  '#include <string.h>\n'
                  '#include <math.h>\n'
                  '\n'
                  'struct tcase { const char *name; void (*fn)(void); };\n'
                  '\n'
                  'static int cur_failures;\n'
                  '\n'
                  '#define EXPECT_TRUE(c)\n'
                  '#define EXPECT_EQ(a, b)\n'
                  '#define EXPECT_STREQ(a, b)\n'
                  '#define EXPECT_NEAR(a, b, eps)\n'
                  '\n'
                  'int run_tests(const struct tcase *cases, int n) {\n'
                  '    return -1;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int calls;\n'
                 'static int tick(void) { return ++calls; }\n'
                 '\n'
                 'static void t_pass(void) {\n'
                 '    EXPECT_TRUE(1 + 1 == 2);\n'
                 '    EXPECT_EQ(2 * 3, 6);\n'
                 '    EXPECT_STREQ("abc", "abc");\n'
                 '    EXPECT_NEAR(0.1 + 0.2, 0.3, 1e-9);\n'
                 '}\n'
                 'static void t_eq(void) {\n'
                 '    EXPECT_EQ(2 + 2, 5);\n'
                 '    EXPECT_EQ(tick(), 1);\n'
                 '    EXPECT_EQ(tick(), 3);\n'
                 "    EXPECT_EQ('a', 97);\n"
                 '}\n'
                 'static void t_str(void) {\n'
                 '    const char *n = NULL;\n'
                 '    EXPECT_STREQ("abc", "abd");\n'
                 '    EXPECT_STREQ(n, "x");\n'
                 '    EXPECT_STREQ(n, NULL);\n'
                 '    EXPECT_STREQ("", "");\n'
                 '}\n'
                 'static void t_near(void) {\n'
                 '    EXPECT_NEAR(1.0, 1.5, 0.1);\n'
                 '    EXPECT_NEAR(2.0, 2.05, 0.1);\n'
                 '    EXPECT_TRUE(calls == 99);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct tcase cases[] = {{"pass", t_pass}, {"eq", t_eq}, {"str", t_str}, {"near", '
                 't_near}};\n'
                 '    int failed = run_tests(cases, 4);\n'
                 '    printf("=> %d calls=%d\\n", failed, calls);\n'
                 '    printf("=> %d\\n", run_tests(cases, 1));\n'
                 '    printf("=> %d\\n", run_tests(cases, 0));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Счётчик cur_failures обнуляется перед каждым тестом. Макросы — do { … } while (0) с '
               'временными переменными; в EXPECT_NEAR сравнение через !(fabs(…) <= eps), чтобы NaN считался '
               'провалом.',
       'expected': ['[ RUN  ] pass',
                    '[  OK  ] pass',
                    '[ RUN  ] eq',
                    '  FAIL: 2 + 2 == 5 (4 vs 5)',
                    '  FAIL: tick() == 3 (2 vs 3)',
                    '[ FAIL ] eq (2)',
                    '[ RUN  ] str',
                    '  FAIL: "abc" == "abd" ("abc" vs "abd")',
                    '  FAIL: n == "x" (NULL vs "x")',
                    '[ FAIL ] str (2)',
                    '[ RUN  ] near',
                    '  FAIL: |1.0 - 1.5| <= 0.1 (1 vs 1.5)',
                    '  FAIL: calls == 99',
                    '[ FAIL ] near (2)',
                    '1 passed, 3 failed',
                    '=> 3 calls=2',
                    '[ RUN  ] pass',
                    '[  OK  ] pass',
                    '1 passed, 0 failed',
                    '=> 0',
                    '0 passed, 0 failed',
                    '=> 0']},
      {'id': 'c13-table-tests',
       'mode': 'c',
       'title': 'Табличный запуск тестов',
       'statement': 'struct row { const char *name; int in; int want; }. run_table(rows, n, f, report, cap) '
                    'вызывает f(rows[i].in) для каждой строки и сравнивает с want; для каждого расхождения '
                    'дописывает в report строку «<name>: f(<in>) = <got>, want <want>\\n» (report — '
                    'C-строка, cap — размер буфера; при нехватке места строки не обрезаются посреди: запись '
                    'пропускается целиком, но подсчёт ошибок идёт). Возвращает число расхождений. report '
                    'может быть NULL (cap = 0) — тогда только подсчёт. Дополнительно: first_failure(rows, n, '
                    'f) → индекс первого расхождения или −1; all_names_unique(rows, n) → 1, если названия '
                    'случаев различны.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct row { const char *name; int in; int want; };\n'
                  '\n'
                  'int run_table(const struct row *rows, int n, int (*f)(int), char *report, size_t cap) { '
                  'return -1; }\n'
                  'int first_failure(const struct row *rows, int n, int (*f)(int)) { return -2; }\n'
                  'int all_names_unique(const struct row *rows, int n) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int sign(int x) { return (x > 0) - (x < 0); }\n'
                 'static int buggy_sign(int x) { return x >= 0 ? 1 : -1; }\n'
                 'static int abs_(int x) { return x < 0 ? -x : x; }\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct row rows[] = {{"neg", -5, -1}, {"zero", 0, 0}, {"pos", 7, 1}, {"big", 1000, '
                 '1}};\n'
                 '    char rep[256];\n'
                 '    printf("%d [%s]\\n", run_table(rows, 4, sign, rep, sizeof rep), rep);\n'
                 '    int n = run_table(rows, 4, buggy_sign, rep, sizeof rep);\n'
                 '    printf("%d [%s]\\n", n, rep);\n'
                 '    char small[40];\n'
                 '    n = run_table(rows, 4, abs_, small, sizeof small);\n'
                 '    printf("%d [%s] %zu\\n", n, small, strlen(small));\n'
                 '    printf("%d\\n", run_table(rows, 4, abs_, NULL, 0));\n'
                 '    printf("%d %d %d\\n", first_failure(rows, 4, sign), first_failure(rows, 4, '
                 'buggy_sign), first_failure(rows, 4, abs_));\n'
                 '    struct row dup[] = {{"a", 1, 1}, {"b", 2, 2}, {"a", 3, 3}};\n'
                 '    printf("%d %d %d\\n", all_names_unique(rows, 4), all_names_unique(dup, 3), '
                 'all_names_unique(dup, 2));\n'
                 '    printf("%d\\n", run_table(rows, 0, sign, rep, sizeof rep));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Сначала формируйте строку отчёта во временном буфере, затем добавляйте её, только если '
               'помещается целиком (с учётом нуля).',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 []',
                    '1 [zero: f(0) = 1, want 0',
                    ']',
                    '3 [neg: f(-5) = 5, want -1',
                    '] 24',
                    '3',
                    '-1 1 0',
                    '1 0 1',
                    '0']},
      {'id': 'c13-boundary-values',
       'mode': 'c',
       'title': 'Генерация граничных значений',
       'statement': 'boundaries(lo, hi, out) → записать в out (long) граничные значения диапазона [lo, hi] '
                    '(lo ≤ hi, int): lo − 1, lo, lo + 1, середина (lo + hi) / 2 с округлением вниз, hi − 1, '
                    'hi, hi + 1 — по возрастанию, без повторов; возвращает число значений (до 7); значения '
                    'считаются в long (без переполнения int). buffer_sizes(len, out) → интересные ёмкости '
                    'буфера для строки длины len: 0, 1, len − 1 (если len ≥ 2), len, len + 1, len + 2 — по '
                    'возрастанию без повторов; возвращает число. int_limits_cases(bits, is_signed, out) → '
                    'значения для типа ширины bits (1…32): min, min + 1, −1 (для знаковых), 0, 1, max − 1, '
                    'max — по возрастанию без повторов, как long long.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'size_t boundaries(int lo, int hi, long *out) { return 0; }\n'
                  'size_t buffer_sizes(size_t len, size_t *out) { return 0; }\n'
                  'size_t int_limits_cases(int bits, int is_signed, long long *out) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static void show_l(const long *v, size_t n) {\n'
                 '    printf("%zu:", n);\n'
                 '    for (size_t i = 0; i < n; i++) printf(" %ld", v[i]);\n'
                 '    printf("\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    long o[8];\n'
                 '    show_l(o, boundaries(0, 100, o));\n'
                 '    show_l(o, boundaries(5, 5, o));\n'
                 '    show_l(o, boundaries(1, 2, o));\n'
                 '    show_l(o, boundaries(-10, 10, o));\n'
                 '    show_l(o, boundaries(INT_MIN, INT_MAX, o));\n'
                 '    show_l(o, boundaries(-7, -2, o));\n'
                 '    size_t b[8];\n'
                 '    size_t n = buffer_sizes(5, b);\n'
                 '    printf("%zu:", n);\n'
                 '    for (size_t i = 0; i < n; i++) printf(" %zu", b[i]);\n'
                 '    printf("\\n");\n'
                 '    n = buffer_sizes(0, b);\n'
                 '    printf("%zu:", n);\n'
                 '    for (size_t i = 0; i < n; i++) printf(" %zu", b[i]);\n'
                 '    printf("\\n");\n'
                 '    n = buffer_sizes(1, b);\n'
                 '    printf("%zu:", n);\n'
                 '    for (size_t i = 0; i < n; i++) printf(" %zu", b[i]);\n'
                 '    printf("\\n");\n'
                 '    long long l[8];\n'
                 '    int cfg[][2] = {{8, 1}, {8, 0}, {1, 1}, {1, 0}, {16, 1}, {32, 0}, {32, 1}};\n'
                 '    for (int i = 0; i < 7; i++) {\n'
                 '        n = int_limits_cases(cfg[i][0], cfg[i][1], l);\n'
                 '        printf("%d/%d %zu:", cfg[i][0], cfg[i][1], n);\n'
                 '        for (size_t k = 0; k < n; k++) printf(" %lld", l[k]);\n'
                 '        printf("\\n");\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Соберите кандидатов в массив long long, отсортируйте и уберите повторы. Середину '
               'отрицательной суммы округляйте вниз (к −∞).',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['7: -1 0 1 50 99 100 101',
                    '3: 4 5 6',
                    '4: 0 1 2 3',
                    '7: -11 -10 -9 0 9 10 11',
                    '7: -2147483649 -2147483648 -2147483647 -1 2147483646 2147483647 2147483648',
                    '7: -8 -7 -6 -5 -3 -2 -1',
                    '6: 0 1 4 5 6 7',
                    '3: 0 1 2',
                    '4: 0 1 2 3',
                    '8/1 7: -128 -127 -1 0 1 126 127',
                    '8/0 4: 0 1 254 255',
                    '1/1 3: -1 0 1',
                    '1/0 2: 0 1',
                    '16/1 7: -32768 -32767 -1 0 1 32766 32767',
                    '32/0 4: 0 1 4294967294 4294967295',
                    '32/1 7: -2147483648 -2147483647 -1 0 1 2147483646 2147483647']},
      {'id': 'c13-assert-messages',
       'mode': 'c',
       'title': 'Сообщения о провале проверок',
       'statement': 'fmt_eq_int(out, cap, expr, got, want) → «<expr>: expected <want>, got <got>»; '
                    'fmt_eq_str(out, cap, expr, got, want) → «<expr>: expected "<want>", got "<got>" '
                    '(differs at index N)» (N — первое различие; NULL печатается как NULL без кавычек и без '
                    '«differs…»; если одна строка — префикс другой, индекс — длина короткой); '
                    'fmt_eq_mem(out, cap, expr, got, want, n) → «<expr>: byte N: 0x<got> != 0x<want>» для '
                    'первого различающегося байта (две строчные hex-цифры) или «<expr>: equal (n bytes)»; '
                    'fmt_near(out, cap, expr, got, want, eps) → «<expr>: |<got> - <want>| = <d> > <eps>» '
                    '(числа «%g») или «<expr>: within <eps>». Все функции возвращают длину как snprintf (в '
                    'том числе при усечении) и не пишут за cap.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int fmt_eq_int(char *out, size_t cap, const char *expr, long long got, long long want) { '
                  'return -1; }\n'
                  'int fmt_eq_str(char *out, size_t cap, const char *expr, const char *got, const char '
                  '*want) { return -1; }\n'
                  'int fmt_eq_mem(char *out, size_t cap, const char *expr, const void *got, const void '
                  '*want, size_t n) { return -1; }\n'
                  'int fmt_near(char *out, size_t cap, const char *expr, double got, double want, double '
                  'eps) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char b[200];\n'
                 '    int n = fmt_eq_int(b, sizeof b, "add(2, 2)", 5, 4);\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    n = fmt_eq_str(b, sizeof b, "name", "hello", "help");\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    n = fmt_eq_str(b, sizeof b, "name", "he", "hello");\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    n = fmt_eq_str(b, sizeof b, "s", NULL, "x");\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    n = fmt_eq_str(b, sizeof b, "s", "x", NULL);\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    n = fmt_eq_str(b, sizeof b, "s", "", "a");\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    unsigned char x[] = {1, 2, 3, 0xAB}, y[] = {1, 2, 3, 0xAC};\n'
                 '    n = fmt_eq_mem(b, sizeof b, "buf", x, y, 4);\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    n = fmt_eq_mem(b, sizeof b, "buf", x, y, 3);\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    n = fmt_near(b, sizeof b, "pi", 3.14, 3.14159, 0.001);\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    n = fmt_near(b, sizeof b, "pi", 3.14159, 3.14, 0.01);\n'
                 '    printf("%d %s\\n", n, b);\n'
                 '    char small[16];\n'
                 '    n = fmt_eq_int(small, sizeof small, "long_expression_name", 1, 2);\n'
                 '    printf("%d [%s]\\n", n, small);\n'
                 '    n = fmt_eq_int(NULL, 0, "e", 1, 2);\n'
                 '    printf("%d\\n", n);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Везде — snprintf(out, cap, …) с возвратом его результата. Для строк найдите первый индекс '
               'несовпадения (в том числе когда одна — префикс другой).',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['28 add(2, 2): expected 4, got 5',
                    '55 name: expected "help", got "hello" (differs at index 3)',
                    '53 name: expected "hello", got "he" (differs at index 2)',
                    '25 s: expected "x", got NULL',
                    '25 s: expected NULL, got "x"',
                    '44 s: expected "a", got "" (differs at index 0)',
                    '25 buf: byte 3: 0xab != 0xac',
                    '20 buf: equal (3 bytes)',
                    '38 pi: |3.14 - 3.14159| = 0.00159 > 0.001',
                    '15 pi: within 0.01',
                    '39 [long_expression]',
                    '20']},
      {'id': 'c13-clock-injection',
       'mode': 'c',
       'title': 'Внедрение часов: ограничитель частоты и таймер',
       'statement': 'struct clock { long (*now)(void *ctx); void *ctx; } — источник времени (мс). struct '
                    'limiter { long cap, tokens, last, interval; } — ведро токенов: ёмкость cap, изначально '
                    'полное, один токен добавляется каждые interval мс. lim_init(l, clk, cap, interval); '
                    'lim_allow(l, clk) → 1 и расход токена, если токены есть, иначе 0: перед проверкой '
                    'пополнение — добавить (now − last) / interval целых токенов (не выше cap), а last '
                    'сдвинуть на добавленное число интервалов (остаток времени не теряется; при заполненном '
                    'ведре last = now). struct timer { long deadline; int armed; }: timer_start(t, clk, ms) '
                    '— дедлайн = now + ms; timer_expired(t, clk) → 1, если взведён и now ≥ deadline; '
                    'timer_remaining(t, clk) → max(0, deadline − now) или −1, если не взведён; '
                    'timer_stop(t).',
       'starter': 'struct clock { long (*now)(void *ctx); void *ctx; };\n'
                  'struct limiter { long cap, tokens, last, interval; };\n'
                  'struct timer { long deadline; int armed; };\n'
                  '\n'
                  'void lim_init(struct limiter *l, struct clock *clk, long cap, long interval) {}\n'
                  'int lim_allow(struct limiter *l, struct clock *clk) { return -1; }\n'
                  'void timer_start(struct timer *t, struct clock *clk, long ms) {}\n'
                  'int timer_expired(const struct timer *t, struct clock *clk) { return -1; }\n'
                  'long timer_remaining(const struct timer *t, struct clock *clk) { return -2; }\n'
                  'void timer_stop(struct timer *t) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static long fake_now;\n'
                 'static long fake(void *ctx) { (void)ctx; return fake_now; }\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct clock clk = {fake, NULL};\n'
                 '    struct limiter l;\n'
                 '    fake_now = 1000;\n'
                 '    lim_init(&l, &clk, 3, 100);\n'
                 '    int r[8];\n'
                 '    for (int i = 0; i < 5; i++) r[i] = lim_allow(&l, &clk);\n'
                 '    printf("%d %d %d %d %d\\n", r[0], r[1], r[2], r[3], r[4]);\n'
                 '    fake_now = 1099;\n'
                 '    int a = lim_allow(&l, &clk);\n'
                 '    fake_now = 1100;\n'
                 '    int b = lim_allow(&l, &clk);\n'
                 '    int c = lim_allow(&l, &clk);\n'
                 '    printf("%d %d %d\\n", a, b, c);\n'
                 '    fake_now = 1350;\n'
                 '    int d = lim_allow(&l, &clk), e = lim_allow(&l, &clk);\n'
                 '    int f = lim_allow(&l, &clk);\n'
                 '    printf("%d %d %d tokens=%ld last=%ld\\n", d, e, f, l.tokens, l.last);\n'
                 '    fake_now = 1000000;\n'
                 '    for (int i = 0; i < 5; i++) r[i] = lim_allow(&l, &clk);\n'
                 '    printf("%d %d %d %d %d\\n", r[0], r[1], r[2], r[3], r[4]);\n'
                 '    struct timer t = {0, 0};\n'
                 '    printf("%d %ld\\n", timer_expired(&t, &clk), timer_remaining(&t, &clk));\n'
                 '    fake_now = 5000;\n'
                 '    timer_start(&t, &clk, 250);\n'
                 '    printf("%d %ld\\n", timer_expired(&t, &clk), timer_remaining(&t, &clk));\n'
                 '    fake_now = 5249;\n'
                 '    printf("%d %ld\\n", timer_expired(&t, &clk), timer_remaining(&t, &clk));\n'
                 '    fake_now = 5250;\n'
                 '    printf("%d %ld\\n", timer_expired(&t, &clk), timer_remaining(&t, &clk));\n'
                 '    fake_now = 9999;\n'
                 '    printf("%d %ld\\n", timer_expired(&t, &clk), timer_remaining(&t, &clk));\n'
                 '    timer_stop(&t);\n'
                 '    printf("%d %ld\\n", timer_expired(&t, &clk), timer_remaining(&t, &clk));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Все обращения ко времени — только через clk->now(clk->ctx). Пополнение: add = (now − last) / '
               'interval; last += add · interval (если ведро переполнилось — last = now).',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 1 1 0 0',
                    '0 1 0',
                    '1 1 0 tokens=0 last=1300',
                    '1 1 1 0 0',
                    '0 -1',
                    '0 250',
                    '0 1',
                    '1 0',
                    '1 0',
                    '0 -1']},
      {'id': 'c13-reader-injection',
       'mode': 'c',
       'title': 'Внедрение читателя: разбор конфигурации',
       'statement': 'struct reader { int (*next)(void *ctx, char *line, size_t cap); void *ctx; } — next '
                    'записывает очередную строку (без \\n) в line и возвращает 1, или 0 в конце. struct cfg '
                    '{ int width; char name[16]; int verbose; }. parse_config(r, c) сначала задаёт значения '
                    'по умолчанию (width = 80, name = «default», verbose = 0), затем читает строки '
                    '«ключ=значение»: пробелы вокруг ключа и значения отбрасываются, пустые строки и строки '
                    'с «#» первым непробельным символом пропускаются; width — целое 1…1000; name — не '
                    'длиннее 15 символов, не пусто; verbose — 0, 1, true или false. Любая ошибка '
                    '(неизвестный ключ, нет «=», неверное значение) увеличивает счётчик ошибок, строка '
                    'пропускается. Возвращает число ошибок.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct reader { int (*next)(void *ctx, char *line, size_t cap); void *ctx; };\n'
                  'struct cfg { int width; char name[16]; int verbose; };\n'
                  '\n'
                  'int parse_config(struct reader *r, struct cfg *c) {\n'
                  '    return -1;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'struct fake { const char *const *lines; int n, pos; };\n'
                 '\n'
                 'static int next_line(void *ctx, char *line, size_t cap) {\n'
                 '    struct fake *f = ctx;\n'
                 '    if (f->pos >= f->n) return 0;\n'
                 '    snprintf(line, cap, "%s", f->lines[f->pos++]);\n'
                 '    return 1;\n'
                 '}\n'
                 '\n'
                 'static void run(const char *label, const char *const *lines, int n) {\n'
                 '    struct fake f = {lines, n, 0};\n'
                 '    struct reader r = {next_line, &f};\n'
                 '    struct cfg c = {-1, "?", -1};\n'
                 '    int e = parse_config(&r, &c);\n'
                 '    printf("%s: errors=%d width=%d name=[%s] verbose=%d\\n", label, e, c.width, c.name, '
                 'c.verbose);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    const char *a[] = {"# comment", "width = 120", "", "  name=  server1  ", '
                 '"verbose=true"};\n'
                 '    run("ok", a, 5);\n'
                 '    run("empty", a, 0);\n'
                 '    const char *b[] = {"width=0", "width=1001", "width=abc", "width=", "name=", '
                 '"name=averyveryverylongname", "verbose=yes", "color=red", "novalue", "=5"};\n'
                 '    run("bad", b, 10);\n'
                 '    const char *c[] = {"width=5", "width=7", "verbose=1", "verbose=false"};\n'
                 '    run("repeat", c, 4);\n'
                 '    const char *d[] = {"  # indented comment", "\\twidth\\t=\\t42\\t", "name=a=b"};\n'
                 '    run("ws", d, 3);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Для каждой строки: trim → пропуск пустых и # → поиск «=» → ключ/значение с trim → проверка '
               'по ключу. Значения по умолчанию задавайте до чтения строк.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['ok: errors=0 width=120 name=[server1] verbose=1',
                    'empty: errors=0 width=80 name=[default] verbose=0',
                    'bad: errors=10 width=80 name=[default] verbose=0',
                    'repeat: errors=0 width=7 name=[default] verbose=0',
                    'ws: errors=0 width=42 name=[a=b] verbose=0']},
      {'id': 'c13-alloc-fault',
       'mode': 'c',
       'title': 'Внедрение отказов аллокатора: нет утечек на путях ошибки',
       'statement': 'struct alloc { void *(*malloc)(size_t); void (*free)(void *); } — аллокатор, '
                    'передаваемый явно. person_make(a, name, scores, n, *out) → 0 и объект struct person { '
                    'char *name; int *scores; size_t n; } (три выделения: сам объект, копия имени, копия '
                    'оценок), либо −1 при отказе любого выделения — тогда всё выделенное освобождается через '
                    'a->free и *out не меняется. person_free(a, p) освобождает все три блока. join_words(a, '
                    'w1, w2, sep, *out) → 0 и новая строка «w1 sep w2» (два выделения: временная копия w1 + '
                    'sep и итоговая; временную освободить), либо −1 с освобождением всего. matrix_new(a, '
                    'rows, cols, *out) → 0 и struct matrix { double **row; size_t rows, cols; } (выделений: '
                    'сама структура, массив указателей, затем каждая строка — rows + 2 штуки; при отказе '
                    'освободить всё выделенное), matrix_free(a, m). Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct alloc { void *(*malloc)(size_t); void (*free)(void *); };\n'
                  'struct person { char *name; int *scores; size_t n; };\n'
                  'struct matrix { double **row; size_t rows, cols; };\n'
                  '\n'
                  'int person_make(const struct alloc *a, const char *name, const int *scores, size_t n, '
                  'struct person **out) { return -9; }\n'
                  'void person_free(const struct alloc *a, struct person *p) {}\n'
                  'int join_words(const struct alloc *a, const char *w1, const char *w2, const char *sep, '
                  'char **out) { return -9; }\n'
                  'int matrix_new(const struct alloc *a, size_t rows, size_t cols, struct matrix **out) { '
                  'return -9; }\n'
                  'void matrix_free(const struct alloc *a, struct matrix *m) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int calls, fail_at, live, total_allocs;\n'
                 '\n'
                 'static void *f_malloc(size_t n) {\n'
                 '    calls++;\n'
                 '    if (calls == fail_at) return NULL;\n'
                 '    void *p = malloc(n);\n'
                 '    if (p) { live++; total_allocs++; }\n'
                 '    return p;\n'
                 '}\n'
                 'static void f_free(void *p) {\n'
                 '    if (p) { live--; free(p); }\n'
                 '}\n'
                 '\n'
                 'static struct alloc A = {f_malloc, f_free};\n'
                 '\n'
                 'static void reset(int at) { calls = 0; fail_at = at; live = 0; total_allocs = 0; }\n'
                 '\n'
                 'int main(void) {\n'
                 '    int sc[] = {90, 80, 70};\n'
                 '    struct person *p = NULL;\n'
                 '    reset(0);\n'
                 '    int rc = person_make(&A, "Ann", sc, 3, &p);\n'
                 '    printf("ok: %d allocs=%d live=%d %s %d\\n", rc, total_allocs, live, p->name, '
                 'p->scores[2]);\n'
                 '    person_free(&A, p);\n'
                 '    printf("after free: live=%d\\n", live);\n'
                 '    int sweep_bad = 0;\n'
                 '    for (int k = 1; k <= 3; k++) {\n'
                 '        struct person *q = (struct person *)0x1;\n'
                 '        reset(k);\n'
                 '        rc = person_make(&A, "Bob", sc, 3, &q);\n'
                 '        printf("fail@%d: rc=%d live=%d out_untouched=%d\\n", k, rc, live, q == (struct '
                 'person *)0x1);\n'
                 '        sweep_bad += (rc == 0 || live != 0);\n'
                 '    }\n'
                 '    char *s = NULL;\n'
                 '    reset(0);\n'
                 '    rc = join_words(&A, "hello", "world", ", ", &s);\n'
                 '    printf("join: %d [%s] live=%d allocs=%d\\n", rc, s, live, total_allocs);\n'
                 '    A.free(s);\n'
                 '    for (int k = 1; k <= 2; k++) {\n'
                 '        char *t = (char *)0x1;\n'
                 '        reset(k);\n'
                 '        rc = join_words(&A, "a", "b", "-", &t);\n'
                 '        printf("join fail@%d: rc=%d live=%d\\n", k, rc, live);\n'
                 '    }\n'
                 '    struct matrix *m = NULL;\n'
                 '    reset(0);\n'
                 '    rc = matrix_new(&A, 4, 3, &m);\n'
                 '    printf("matrix: %d allocs=%d live=%d %.1f\\n", rc, total_allocs, live, m->row[3][2]);\n'
                 '    matrix_free(&A, m);\n'
                 '    printf("freed live=%d\\n", live);\n'
                 '    int bad = 0;\n'
                 '    for (int k = 1; k <= 6; k++) {\n'
                 '        struct matrix *q = NULL;\n'
                 '        reset(k);\n'
                 '        rc = matrix_new(&A, 4, 3, &q);\n'
                 '        if (rc == 0 || live != 0) bad++;\n'
                 '    }\n'
                 '    printf("matrix sweep bad=%d\\n", bad);\n'
                 '    reset(0);\n'
                 '    rc = matrix_new(&A, 0, 0, &m);\n'
                 '    printf("empty: %d live=%d\\n", rc, live);\n'
                 '    matrix_free(&A, m);\n'
                 '    printf("live=%d sweep_bad=%d\\n", live, sweep_bad);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Каждое выделение проверяйте, и при отказе освобождайте в обратном порядке всё, что уже '
               'выделено. Единый блок очистки (goto cleanup) особенно удобен для таких функций.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['ok: 0 allocs=3 live=3 Ann 70',
                    'after free: live=0',
                    'fail@1: rc=-1 live=0 out_untouched=1',
                    'fail@2: rc=-1 live=0 out_untouched=1',
                    'fail@3: rc=-1 live=0 out_untouched=1',
                    'join: 0 [hello, world] live=1 allocs=2',
                    'join fail@1: rc=-1 live=0',
                    'join fail@2: rc=-1 live=0',
                    'matrix: 0 allocs=6 live=6 0.0',
                    'freed live=0',
                    'matrix sweep bad=0',
                    'empty: 0 live=2',
                    'live=0 sweep_bad=0']},
      {'id': 'c13-spy-calls',
       'mode': 'c',
       'title': 'Шпион: запись и проверка последовательности вызовов',
       'statement': 'struct spy { char log[16][32]; int n; } — шпион хранит до 16 записей вида '
                    '«имя(аргумент)». spy_init(s); spy_call(s, name, arg) → дописать «name(arg)» (аргумент — '
                    'int, «%d»), возвращает 1, при переполнении 0; spy_verify(s, expected, ne) → −1, если '
                    'записанная последовательность в точности равна expected (ne строк), иначе индекс '
                    'первого расхождения (если одна последовательность — префикс другой, индекс = длина '
                    'короткой); spy_count(s, name) → сколько раз вызывалась функция с таким именем (любой '
                    'аргумент); spy_args(s, name, out) → число вызовов и значения аргументов в порядке '
                    'вызовов; spy_called_before(s, a, b) → 1, если первый вызов a произошёл раньше первого '
                    'вызова b (оба должны быть); spy_last(s, buf) → последняя запись.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct spy { char log[16][32]; int n; };\n'
                  '\n'
                  'void spy_init(struct spy *s) { s->n = 0; }\n'
                  'int spy_call(struct spy *s, const char *name, int arg) { return -1; }\n'
                  'int spy_verify(const struct spy *s, const char *const *expected, int ne) { return -2; }\n'
                  'int spy_count(const struct spy *s, const char *name) { return -1; }\n'
                  'int spy_args(const struct spy *s, const char *name, int *out) { return -1; }\n'
                  'int spy_called_before(const struct spy *s, const char *a, const char *b) { return -1; }\n'
                  'int spy_last(const struct spy *s, char *buf) { buf[0] = 0; return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct spy s;\n'
                 '    spy_init(&s);\n'
                 '    spy_call(&s, "open", 3);\n'
                 '    spy_call(&s, "write", 10);\n'
                 '    spy_call(&s, "write", -20);\n'
                 '    spy_call(&s, "close", 3);\n'
                 '    const char *ok[] = {"open(3)", "write(10)", "write(-20)", "close(3)"};\n'
                 '    const char *bad[] = {"open(3)", "write(11)", "write(-20)", "close(3)"};\n'
                 '    const char *shortv[] = {"open(3)", "write(10)"};\n'
                 '    const char *longv[] = {"open(3)", "write(10)", "write(-20)", "close(3)", "extra(0)"};\n'
                 '    printf("%d %d %d %d %d\\n", spy_verify(&s, ok, 4), spy_verify(&s, bad, 4), '
                 'spy_verify(&s, shortv, 2), spy_verify(&s, longv, 5), spy_verify(&s, ok, 0));\n'
                 '    printf("%d %d %d\\n", spy_count(&s, "write"), spy_count(&s, "close"), spy_count(&s, '
                 '"writ"));\n'
                 '    int a[8];\n'
                 '    int k = spy_args(&s, "write", a);\n'
                 '    printf("%d: %d %d\\n", k, a[0], a[1]);\n'
                 '    printf("%d %d %d %d\\n", spy_called_before(&s, "open", "close"), spy_called_before(&s, '
                 '"close", "open"), spy_called_before(&s, "open", "nothing"), spy_called_before(&s, "write", '
                 '"write"));\n'
                 '    char last[32];\n'
                 '    int h = spy_last(&s, last);\n'
                 '    printf("%d %s\\n", h, last);\n'
                 '    int added = 0;\n'
                 '    for (int i = 0; i < 20; i++) added += spy_call(&s, "tick", i);\n'
                 '    printf("%d %d\\n", added, s.n);\n'
                 '    struct spy e;\n'
                 '    spy_init(&e);\n'
                 '    printf("%d %d\\n", spy_last(&e, last), spy_verify(&e, ok, 0));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Запись — snprintf(log[n], 32, "%s(%d)", name, arg). Для подсчёта по имени сверяйте префикс '
               'до «(», чтобы «writ» не совпадал с «write».',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['-1 1 2 4 0', '2 1 0', '2: 10 -20', '1 0 0 0', '1 close(3)', '12 16', '0 -1']},
      {'id': 'c13-mock-expectations',
       'mode': 'c',
       'title': 'Мини-библиотека моков: ожидания и проверка',
       'statement': 'Хранилище ожиданий (до 16): mock_reset(); mock_expect(name, ret) — ожидается один вызов '
                    'функции name, которая вернёт ret; mock_set_ordered(on) — строгий порядок (по умолчанию '
                    'выключен). mock_call(name) → ret первого ещё не использованного ожидания с этим именем '
                    '(в обычном режиме); в строгом режиме вызов должен совпадать с ближайшим '
                    'неиспользованным ожиданием (по порядку добавления), иначе он «неожиданный». Неожиданный '
                    'вызов (нет подходящего ожидания) возвращает −1 и считается ошибкой. mock_verify() → '
                    'число проблем: неожиданные вызовы + ожидания, не получившие вызова. mock_unexpected() и '
                    'mock_pending() — отдельные счётчики. Имена — до 31 символа.',
       'starter': 'void mock_reset(void) {}\n'
                  'void mock_set_ordered(int on) {}\n'
                  'void mock_expect(const char *name, int ret) {}\n'
                  'int mock_call(const char *name) { return -9; }\n'
                  'int mock_verify(void) { return -1; }\n'
                  'int mock_unexpected(void) { return -1; }\n'
                  'int mock_pending(void) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    mock_reset();\n'
                 '    mock_expect("read", 5);\n'
                 '    mock_expect("write", 7);\n'
                 '    mock_expect("read", 9);\n'
                 '    int a = mock_call("read"), b = mock_call("read"), c = mock_call("write");\n'
                 '    printf("%d %d %d | %d %d %d\\n", a, b, c, mock_verify(), mock_unexpected(), '
                 'mock_pending());\n'
                 '    int d = mock_call("read");\n'
                 '    printf("%d | %d %d %d\\n", d, mock_verify(), mock_unexpected(), mock_pending());\n'
                 '    mock_reset();\n'
                 '    mock_expect("open", 3);\n'
                 '    mock_expect("close", 0);\n'
                 '    printf("%d %d\\n", mock_pending(), mock_verify());\n'
                 '    mock_call("open");\n'
                 '    printf("%d %d\\n", mock_pending(), mock_verify());\n'
                 '    mock_reset();\n'
                 '    mock_set_ordered(1);\n'
                 '    mock_expect("a", 1);\n'
                 '    mock_expect("b", 2);\n'
                 '    mock_expect("c", 3);\n'
                 '    int x = mock_call("b");\n'
                 '    int y = mock_call("a");\n'
                 '    int z = mock_call("b");\n'
                 '    int w = mock_call("c");\n'
                 '    printf("%d %d %d %d | %d %d %d\\n", x, y, z, w, mock_verify(), mock_unexpected(), '
                 'mock_pending());\n'
                 '    mock_reset();\n'
                 '    printf("%d %d %d\\n", mock_call("anything"), mock_verify(), mock_unexpected());\n'
                 '    mock_reset();\n'
                 '    for (int i = 0; i < 20; i++) mock_expect("x", i);\n'
                 '    int sum = 0;\n'
                 '    for (int i = 0; i < 20; i++) sum += mock_call("x");\n'
                 '    printf("%d %d %d\\n", sum, mock_verify(), mock_unexpected());\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Список ожиданий с флагом used. В строгом режиме просматривайте только первое '
               'неиспользованное ожидание; в обычном — первое неиспользованное с тем же именем. Максимум 16 '
               'ожиданий.',
       'expected': ['5 9 7 | 0 0 0', '-1 | 1 1 0', '2 2', '1 1', '-1 1 2 3 | 1 1 0', '-1 1 1', '116 4 4']},
      {'id': 'c13-coverage-counter',
       'mode': 'c',
       'title': 'Свой счётчик покрытия',
       'statement': 'Макрос COV(id) отмечает «точку покрытия» с номером id (0…31): cov_hits[id]++ (счётчики '
                    '— глобальный массив). cov_reset(total) задаёт, что точек total (≤ 32) и обнуляет '
                    'счётчики; cov_percent() → процент покрытых точек среди total (целый, вниз; при total = '
                    '0 → 100); cov_uncovered(out) → число непокрытых точек и их номера по возрастанию; '
                    'cov_report(buf, cap) → строка «covered K/N (P%)\\n» и, если есть непокрытые, строка '
                    '«missing: 2 4 7\\n» (номера через пробел); возвращает длину отчёта или −1, если не '
                    'помещается; cov_hit_count(id); cov_hottest() → номер самой посещаемой точки (при '
                    'равенстве — наименьший номер) или −1, если ни одна не посещена.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int cov_hits[32];\n'
                  'static int cov_total;\n'
                  '\n'
                  '#define COV(id)\n'
                  '\n'
                  'void cov_reset(int total) {}\n'
                  'int cov_percent(void) { return -1; }\n'
                  'int cov_uncovered(int *out) { return -1; }\n'
                  'int cov_report(char *buf, size_t cap) { return -1; }\n'
                  'int cov_hit_count(int id) { return -1; }\n'
                  'int cov_hottest(void) { return -2; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int classify(int x) {\n'
                 '    COV(0);\n'
                 '    if (x < 0) { COV(1); return -1; }\n'
                 '    if (x == 0) { COV(2); return 0; }\n'
                 '    COV(3);\n'
                 '    if (x > 1000) { COV(4); return 2; }\n'
                 '    return 1;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    cov_reset(5);\n'
                 '    char rep[128];\n'
                 '    printf("%d %d\\n", cov_percent(), cov_hottest());\n'
                 '    int n = cov_report(rep, sizeof rep);\n'
                 '    printf("%d\\n%s", n, rep);\n'
                 '    classify(5);\n'
                 '    classify(5);\n'
                 '    classify(-3);\n'
                 '    n = cov_report(rep, sizeof rep);\n'
                 '    printf("%d %d\\n%s", n, cov_percent(), rep);\n'
                 '    int miss[32];\n'
                 '    int k = cov_uncovered(miss);\n'
                 '    printf("%d:", k);\n'
                 '    for (int i = 0; i < k; i++) printf(" %d", miss[i]);\n'
                 '    printf("\\n%d %d %d\\n", cov_hit_count(0), cov_hit_count(3), cov_hottest());\n'
                 '    classify(0);\n'
                 '    classify(2000);\n'
                 '    n = cov_report(rep, sizeof rep);\n'
                 '    printf("%d %d\\n%s", n, cov_percent(), rep);\n'
                 '    printf("%d\\n", cov_report(rep, 10));\n'
                 '    cov_reset(0);\n'
                 '    printf("%d %d\\n", cov_percent(), cov_report(rep, sizeof rep));\n'
                 '    cov_reset(3);\n'
                 '    COV(1); COV(1); COV(2); COV(2);\n'
                 '    printf("%d %d %d\\n", cov_percent(), cov_hottest(), cov_hit_count(2));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'COV(id) — просто увеличение счётчика. Отчёт формируйте во временном буфере и копируйте, если '
               'помещается вместе с нулём.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 -1',
                    '36',
                    'covered 0/5 (0%)',
                    'missing: 0 1 2 3 4',
                    '31 60',
                    'covered 3/5 (60%)',
                    'missing: 2 4',
                    '2: 2 4',
                    '3 2 0',
                    '19 100',
                    'covered 5/5 (100%)',
                    '-1',
                    '100 19',
                    '66 1 2']},
      {'id': 'c13-mutation-score',
       'mode': 'c',
       'title': 'Мутационное тестирование: сколько мутантов убито',
       'statement': 'struct tc { int in; int want; } — тесты. mutation_score(orig, mutants, nm, tests, nt, '
                    '*killed_mask) → число убитых мутантов (мутант убит, если хотя бы на одном тесте '
                    'результат ≠ want); в *killed_mask — бит i установлен для убитого мутанта i (nm ≤ 31). '
                    'Если оригинальная функция не проходит все тесты, результат −1 (маска не меняется). '
                    'survivors(mutants, nm, tests, nt, out) → индексы выживших мутантов по возрастанию '
                    '(число). equivalent_pair(f, g, lo, hi) → 1, если f(x) == g(x) для всех x из [lo, hi]. '
                    'weakest_test(mutants, nm, tests, nt) → индекс теста, убивающего наименьшее число '
                    'мутантов (при равенстве — наименьший индекс; тест, убивающий 0 мутантов, — '
                    '«бесполезный»), −1 при nt = 0.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct tc { int in; int want; };\n'
                  '\n'
                  'int mutation_score(int (*orig)(int), int (*const *mutants)(int), int nm, const struct tc '
                  '*tests, int nt, unsigned *killed_mask) { return -9; }\n'
                  'int survivors(int (*const *mutants)(int), int nm, const struct tc *tests, int nt, int '
                  '*out) { return -9; }\n'
                  'int equivalent_pair(int (*f)(int), int (*g)(int), int lo, int hi) { return -9; }\n'
                  'int weakest_test(int (*const *mutants)(int), int nm, const struct tc *tests, int nt) { '
                  'return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int clamp10(int x) { return x < 0 ? 0 : x > 10 ? 10 : x; }\n'
                 'static int m_lt_le(int x) { return x <= 0 ? 0 : x > 10 ? 10 : x; }\n'
                 'static int m_gt_ge(int x) { return x < 0 ? 0 : x >= 10 ? 10 : x; }\n'
                 'static int m_swap(int x) { return x < 0 ? 10 : x > 10 ? 0 : x; }\n'
                 'static int m_const(int x) { return x < 0 ? 0 : x > 10 ? 11 : x; }\n'
                 'static int m_equiv(int x) { return x < 0 ? 0 : x > 10 ? 10 : x + 0; }\n'
                 'static int m_id(int x) { return x; }\n'
                 '\n'
                 'int main(void) {\n'
                 '    int (*mut[])(int) = {m_lt_le, m_gt_ge, m_swap, m_const, m_equiv, m_id};\n'
                 '    struct tc weak[] = {{5, 5}, {-5, 0}};\n'
                 '    struct tc strong[] = {{5, 5}, {-5, 0}, {0, 0}, {10, 10}, {11, 10}, {100, 10}};\n'
                 '    unsigned mask = 0xFFFF;\n'
                 '    int k = mutation_score(clamp10, mut, 6, weak, 2, &mask);\n'
                 '    printf("%d %#x\\n", k, mask);\n'
                 '    k = mutation_score(clamp10, mut, 6, strong, 6, &mask);\n'
                 '    printf("%d %#x\\n", k, mask);\n'
                 '    mask = 0x77;\n'
                 '    struct tc wrong[] = {{5, 6}};\n'
                 '    int msw = mutation_score(clamp10, mut, 6, wrong, 1, &mask);\n'
                 '    printf("%d %#x\\n", msw, mask);\n'
                 '    int s[8];\n'
                 '    int n = survivors(mut, 6, weak, 2, s);\n'
                 '    printf("%d:", n);\n'
                 '    for (int i = 0; i < n; i++) printf(" %d", s[i]);\n'
                 '    n = survivors(mut, 6, strong, 6, s);\n'
                 '    printf(" | %d:", n);\n'
                 '    for (int i = 0; i < n; i++) printf(" %d", s[i]);\n'
                 '    printf("\\n%d %d %d\\n", equivalent_pair(clamp10, m_equiv, -1000, 1000), '
                 'equivalent_pair(clamp10, m_lt_le, -5, 5), equivalent_pair(clamp10, m_lt_le, 1, 20));\n'
                 '    printf("%d %d %d\\n", weakest_test(mut, 6, strong, 6), weakest_test(mut, 6, weak, 2), '
                 'weakest_test(mut, 6, strong, 0));\n'
                 '    unsigned none = 5;\n'
                 '    int ms = mutation_score(clamp10, mut, 0, strong, 6, &none);\n'
                 '    printf("%d %#x\\n", ms, none);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Мутант убит, если хотя бы один тест даёт результат, отличный от ожидаемого. Сначала '
               'убедитесь, что оригинал проходит все тесты.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['2 0x24', '3 0x2c', '-1 0x77', '4: 0 1 3 4 | 3: 0 1 4', '1 1 1', '0 0 -1', '0 0']},
      {'id': 'c13-property-runner',
       'mode': 'c',
       'title': 'Запуск тестов свойств с детерминированным генератором',
       'statement': 'struct pres { int runs, failures; long first_fail; unsigned first_seed; }. '
                    'prop_run(gen, prop, seed, runs, *res): для i = 0…runs−1 состояние генератора st = seed '
                    '+ i; gen(&st, buf, &len) заполняет int-массив buf (до 64) и его длину; prop(buf, len) → '
                    '1 (свойство выполнено) или 0. res: runs = runs, failures — число нарушений, first_fail '
                    '— номер первого нарушения i (−1, если нет), first_seed — seed + i этого прогона. '
                    'lcg_next(&st) → следующее псевдослучайное значение (st = st · 1664525 + 1013904223, '
                    'возвращает st >> 8, uint32_t); gen_small_ints(&st, buf, &len) — длина 0…15 (lcg % 16), '
                    'элементы lcg % 21 − 10. replay(gen, seed_i, buf, *len) — воспроизвести вход прогона по '
                    'его seed (то же, что делает prop_run для этого прогона).',
       'starter': '#include <stdint.h>\n'
                  '\n'
                  'struct pres { int runs, failures; long first_fail; unsigned first_seed; };\n'
                  '\n'
                  'uint32_t lcg_next(uint32_t *st) { return 0; }\n'
                  'void gen_small_ints(uint32_t *st, int *buf, int *len) { *len = 0; }\n'
                  'void prop_run(void (*gen)(uint32_t *, int *, int *), int (*prop)(const int *, int), '
                  'uint32_t seed, int runs, struct pres *res) {}\n'
                  'void replay(void (*gen)(uint32_t *, int *, int *), uint32_t seed_i, int *buf, int *len) '
                  '{}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int sorted_ok(const int *a, int n) {\n'
                 '    int b[64];\n'
                 '    memcpy(b, a, sizeof(int) * (size_t)n);\n'
                 '    for (int i = 1; i < n; i++)\n'
                 '        for (int j = i; j > 0 && b[j - 1] > b[j]; j--) { int t = b[j]; b[j] = b[j - 1]; '
                 'b[j - 1] = t; }\n'
                 '    for (int i = 1; i < n; i++) if (b[i - 1] > b[i]) return 0;\n'
                 '    return 1;\n'
                 '}\n'
                 'static int never_big(const int *a, int n) {\n'
                 '    for (int i = 0; i < n; i++) if (a[i] >= 9) return 0;\n'
                 '    return 1;\n'
                 '}\n'
                 'static int short_only(const int *a, int n) { (void)a; return n < 14; }\n'
                 'static int always(const int *a, int n) { (void)a; (void)n; return 1; }\n'
                 '\n'
                 'int main(void) {\n'
                 '    uint32_t st = 1;\n'
                 '    uint32_t v1 = lcg_next(&st);\n'
                 '    uint32_t v2 = lcg_next(&st);\n'
                 '    uint32_t v3 = lcg_next(&st);\n'
                 '    printf("%u %u %u\\n", v1, v2, v3);\n'
                 '    st = 42;\n'
                 '    int buf[64], len;\n'
                 '    gen_small_ints(&st, buf, &len);\n'
                 '    printf("%d:", len);\n'
                 '    for (int i = 0; i < len; i++) printf(" %d", buf[i]);\n'
                 '    printf("\\n");\n'
                 '    struct pres r;\n'
                 '    prop_run(gen_small_ints, always, 100, 50, &r);\n'
                 '    printf("%d %d %ld %u\\n", r.runs, r.failures, r.first_fail, r.first_seed);\n'
                 '    prop_run(gen_small_ints, sorted_ok, 7, 200, &r);\n'
                 '    printf("%d %d %ld %u\\n", r.runs, r.failures, r.first_fail, r.first_seed);\n'
                 '    prop_run(gen_small_ints, never_big, 0, 100, &r);\n'
                 '    printf("%d %d %ld %u\\n", r.runs, r.failures, r.first_fail, r.first_seed);\n'
                 '    prop_run(gen_small_ints, short_only, 5, 300, &r);\n'
                 '    printf("%d %d %ld %u\\n", r.runs, r.failures, r.first_fail, r.first_seed);\n'
                 '    replay(gen_small_ints, r.first_seed, buf, &len);\n'
                 '    printf("%d %d\\n", len, short_only(buf, len));\n'
                 '    prop_run(gen_small_ints, always, 0, 0, &r);\n'
                 '    printf("%d %d %ld\\n", r.runs, r.failures, r.first_fail);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'В prop_run каждый прогон начинается с состояния seed + i. lcg_next меняет состояние и '
               'возвращает его старшие 24 бита (st >> 8).',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['3967065 6195333 8459777',
                    '1: -2',
                    '50 0 -1 0',
                    '200 0 -1 0',
                    '100 46 0 0',
                    '300 38 5 10',
                    '15 0',
                    '0 0 -1']},
      {'id': 'c13-shrink',
       'mode': 'c',
       'title': 'Сокращение падающего входа',
       'statement': 'shrink(a, n, fails) → новая длина n: массив a сокращается так, чтобы fails(a, n) '
                    'по-прежнему возвращала ненулевое значение (изначально — ненулевое). Алгоритм: повторять '
                    'до отсутствия изменений: (1) для размера куска c = n / 2, n / 4, … до 1 (деление '
                    'целочисленное, c ≥ 1): слева направо пробовать удалять куски по c элементов (последний '
                    'кусок может быть короче), оставляя удаление, если fails сохраняется (после удаления '
                    'start не двигается); (2) для каждого i слева направо: пробовать заменить a[i] на 0, '
                    'затем (если не вышло и a[i] ≠ 0) на a[i] / 2 (деление к нулю), оставляя замену, если '
                    'fails сохраняется. Возвращается результат; вызовов fails — не более 5000.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int shrink(int *a, int n, int (*fails)(const int *, int)) { return n; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int has_neg_and_big(const int *a, int n) {\n'
                 '    int neg = 0, big = 0;\n'
                 '    for (int i = 0; i < n; i++) { neg |= a[i] < 0; big |= a[i] > 50; }\n'
                 '    return neg && big;\n'
                 '}\n'
                 'static int sum_over_100(const int *a, int n) {\n'
                 '    long s = 0;\n'
                 '    for (int i = 0; i < n; i++) s += a[i];\n'
                 '    return s > 100;\n'
                 '}\n'
                 'static int dup_adjacent(const int *a, int n) {\n'
                 '    for (int i = 1; i < n; i++) if (a[i] == a[i - 1] && a[i] != 0) return 1;\n'
                 '    return 0;\n'
                 '}\n'
                 'static int three_odd(const int *a, int n) {\n'
                 '    int c = 0;\n'
                 '    for (int i = 0; i < n; i++) c += (a[i] & 1) != 0;\n'
                 '    return c >= 3;\n'
                 '}\n'
                 '\n'
                 'static void run(const char *label, int *a, int n, int (*f)(const int *, int)) {\n'
                 '    int m = shrink(a, n, f);\n'
                 '    printf("%s: %d:", label, m);\n'
                 '    for (int i = 0; i < m; i++) printf(" %d", a[i]);\n'
                 '    printf(" fails=%d\\n", f(a, m) != 0);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    int a1[] = {5, 80, 3, -7, 12, 99, 4, 4, 0};\n'
                 '    run("neg+big", a1, 9, has_neg_and_big);\n'
                 '    int a2[] = {40, 40, 40, 40, 5};\n'
                 '    run("sum", a2, 5, sum_over_100);\n'
                 '    int a3[] = {1, 2, 3, 3, 4, 5, 5, 6};\n'
                 '    run("dup", a3, 8, dup_adjacent);\n'
                 '    int a4[] = {2, 4, 7, 6, 9, 8, 11, 10, 13, 12};\n'
                 '    run("odd", a4, 10, three_odd);\n'
                 '    int a5[] = {101};\n'
                 '    run("one", a5, 1, sum_over_100);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Следуйте алгоритму буквально: сначала удаление кусков (размеры от n/2 вниз), затем упрощение '
               'значений; повторяйте, пока что-то меняется. После успешного удаления start не меняется.',
       'expected': ['neg+big: 2: 80 -1 fails=1',
                    'sum: 3: 40 40 40 fails=1',
                    'dup: 2: 5 5 fails=1',
                    'odd: 3: 9 5 13 fails=1',
                    'one: 1: 101 fails=1']},
      {'id': 'c13-fuzz-mutator',
       'mode': 'c',
       'title': 'Детерминированный мутатор для фаззинга',
       'statement': 'rng_next(&st) → st = st · 1664525 + 1013904223; возвращает st >> 8. mutate(buf, len, '
                    'cap, *rng) → новая длина: op = rng_next % 4: 0 — переворот бита: pos = rng_next % (len '
                    '· 8) (len = 0 — без изменений), buf[pos / 8] ^= 1 << (pos % 8); 1 — замена байта: pos = '
                    'rng_next % len, buf[pos] = rng_next & 255 (len = 0 — без изменений); 2 — вставка байта '
                    '(если len < cap): pos = rng_next % (len + 1), значение rng_next & 255, хвост '
                    'сдвигается; 3 — удаление (если len > 1): pos = rng_next % len, хвост сдвигается влево. '
                    'Если операция неприменима — буфер не меняется (аргументы rng_next при этом всё равно '
                    'потребляются в указанном порядке до проверки применимости: сначала op, затем остальные '
                    'значения в порядке записи). fuzz(target, seed_buf, seed_len, iters, rng_seed, *crashes, '
                    '*first_iter): для каждой итерации копия seed_buf мутируется mutations раз = 1 + '
                    'rng_next % 4 (cap = 64) и передаётся target(buf, len); ненулевой результат — «падение»; '
                    'crashes — число падений, first_iter — номер первой итерации (−1, если нет).',
       'starter': '#include <stddef.h>\n'
                  '#include <stdint.h>\n'
                  '\n'
                  'uint32_t rng_next(uint32_t *st) { return 0; }\n'
                  'size_t mutate(unsigned char *buf, size_t len, size_t cap, uint32_t *rng) { return len; }\n'
                  'void fuzz(int (*target)(const unsigned char *, size_t), const unsigned char *seed_buf, '
                  'size_t seed_len, int iters, uint32_t rng_seed, int *crashes, int *first_iter) { *crashes '
                  '= -1; *first_iter = -2; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int crash_on_magic(const unsigned char *b, size_t n) {\n'
                 "    return n >= 3 && b[0] == 'F' && b[1] == 'U' && b[2] == 'Z';\n"
                 '}\n'
                 'static int crash_on_long(const unsigned char *b, size_t n) { (void)b; return n >= 9; }\n'
                 'static int never(const unsigned char *b, size_t n) { (void)b; (void)n; return 0; }\n'
                 '\n'
                 'int main(void) {\n'
                 '    uint32_t st = 1;\n'
                 '    uint32_t w1 = rng_next(&st);\n'
                 '    uint32_t w2 = rng_next(&st);\n'
                 '    printf("%u %u\\n", w1, w2);\n'
                 '    unsigned char buf[64] = "hello";\n'
                 '    size_t len = 5;\n'
                 '    uint32_t rng = 7;\n'
                 '    for (int i = 0; i < 6; i++) {\n'
                 '        len = mutate(buf, len, 64, &rng);\n'
                 '        printf("%zu:", len);\n'
                 '        for (size_t k = 0; k < len; k++) printf(" %02x", buf[k]);\n'
                 '        printf("\\n");\n'
                 '    }\n'
                 '    unsigned char e[64];\n'
                 '    uint32_t r2 = 3;\n'
                 '    size_t el = 0;\n'
                 '    for (int i = 0; i < 20; i++) el = mutate(e, el, 64, &r2);\n'
                 '    printf("%zu %u\\n", el, r2);\n'
                 '    unsigned char one[64] = {1};\n'
                 '    size_t ol = 1;\n'
                 '    uint32_t r3 = 9;\n'
                 '    for (int i = 0; i < 30; i++) ol = mutate(one, ol, 64, &r3);\n'
                 '    printf("%zu\\n", ol);\n'
                 '    int crashes, first;\n'
                 '    fuzz(never, (const unsigned char *)"FUZ", 3, 500, 1, &crashes, &first);\n'
                 '    printf("%d %d\\n", crashes, first);\n'
                 '    fuzz(crash_on_magic, (const unsigned char *)"FUZ", 3, 500, 1, &crashes, &first);\n'
                 '    printf("%d %d\\n", crashes, first);\n'
                 '    fuzz(crash_on_long, (const unsigned char *)"abcdefgh", 8, 300, 42, &crashes, &first);\n'
                 '    printf("%d %d\\n", crashes, first);\n'
                 '    fuzz(crash_on_long, (const unsigned char *)"abc", 3, 300, 42, &crashes, &first);\n'
                 '    printf("%d %d\\n", crashes, first);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Порядок потребления значений генератора — как в условии: сначала op, затем (если применимо) '
               'позиция и значение. Для вставки/удаления сдвигайте хвост memmove.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['3967065 6195333',
                    '5: 68 65 6c 40 6f',
                    '5: e8 65 6c 40 6f',
                    '5: 60 65 6c 40 6f',
                    '5: 68 65 6c 40 6f',
                    '5: 68 65 6c 60 6f',
                    '5: 68 65 64 60 6f',
                    '4 694762905',
                    '1',
                    '0 -1',
                    '15 17',
                    '100 1',
                    '0 -1']},
      {'id': 'c13-golden-normalize',
       'mode': 'c',
       'title': 'Эталонные выводы: нормализация и сравнение',
       'statement': 'normalize(text, out, cap) → длина результата или −1, если не помещается: окончания '
                    'строк \\r\\n и одиночный \\r превращаются в \\n; пробелы и табуляции в конце каждой '
                    'строки удаляются; пустые строки в начале и в конце текста удаляются; подряд идущие '
                    'пустые строки схлопываются в одну; непустой результат заканчивается ровно одним \\n; из '
                    'пустого текста получается пустая строка. golden_diff(expected, actual) → 0, если '
                    'нормализованные тексты равны, иначе 1-based номер первой отличающейся строки (если один '
                    'текст — префикс другого по строкам, номер = число строк короткого + 1). '
                    'line_count(text) — число строк нормализованного текста.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int normalize(const char *text, char *out, size_t cap) { return -9; }\n'
                  'int golden_diff(const char *expected, const char *actual) { return -9; }\n'
                  'int line_count(const char *text) { return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static void n(const char *s) {\n'
                 '    char out[128];\n'
                 '    int k = normalize(s, out, sizeof out);\n'
                 '    printf("%d [", k);\n'
                 '    for (int i = 0; i < k; i++) printf("%c", out[i] == \'\\n\' ? \'|\' : out[i]);\n'
                 '    printf("]\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    n("hello\\r\\nworld  \\r\\n");\n'
                 '    n("\\n\\n  \\nfirst\\n\\n\\n\\nsecond\\t\\n\\n\\n");\n'
                 '    n("a\\rb\\r\\rc");\n'
                 '    n("");\n'
                 '    n("   \\n\\t\\n");\n'
                 '    n("single");\n'
                 '    n("x\\n\\ny");\n'
                 '    char tiny[6];\n'
                 '    printf("%d %d\\n", normalize("abcd", tiny, sizeof tiny), normalize("abcde", tiny, '
                 'sizeof tiny));\n'
                 '    printf("%d %d %d\\n", golden_diff("a\\nb\\nc\\n", "a\\nb\\nc\\n"), '
                 'golden_diff("a\\nb\\nc", "a\\r\\nb  \\r\\nc\\n\\n\\n"), golden_diff("a\\nb\\nc\\n", '
                 '"a\\nX\\nc\\n"));\n'
                 '    printf("%d %d %d\\n", golden_diff("a\\nb\\n", "a\\nb\\nc\\n"), '
                 'golden_diff("a\\nb\\nc\\n", "a\\nb\\n"), golden_diff("", ""));\n'
                 '    printf("%d %d\\n", golden_diff("a\\n\\n\\nb", "a\\n\\nb"), golden_diff("a\\nb", '
                 '"a\\n\\nb"));\n'
                 '    printf("%d %d %d\\n", line_count(""), line_count("a\\n\\n\\nb\\n\\n"), '
                 'line_count("one"));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Нормализуйте построчно: уберите хвостовые пробелы, пропускайте пустые строки в начале, а '
               'встреченную пустую строку запоминайте и добавляйте перед следующей непустой.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['12 [hello|world|]',
                    '14 [first||second|]',
                    '7 [a|b||c|]',
                    '0 []',
                    '0 []',
                    '7 [single|]',
                    '5 [x||y|]',
                    '5 -1',
                    '0 0 2',
                    '3 3 0',
                    '0 2',
                    '0 3 1']},
      {'id': 'c13-tap-output',
       'mode': 'c',
       'title': 'Формат TAP: отчёт о тестах',
       'statement': 'struct result { const char *name; int status; const char *message; } — status: 0 '
                    'прошёл, 1 упал, 2 пропущен. tap_output(r, n, out, cap) строит отчёт в формате TAP 13: '
                    'строка «TAP version 13», затем «1..n»; для прошедшего — «ok <i> - <name>»; для упавшего '
                    '— «not ok <i> - <name>» и блок «  ---», «  message: <message>» (если message не NULL), '
                    '«  ...»; для пропущенного — «ok <i> - <name> # SKIP <message>» (message может быть NULL '
                    '— тогда «# SKIP»). i считается с 1; все строки оканчиваются \\n. Возврат — длина или '
                    '−1, если не помещается. tap_summary(r, n, out) — «# pass P fail F skip S\\n»; '
                    'tap_exit_code(r, n) → 0, если нет упавших, иначе число упавших (не больше 255).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct result { const char *name; int status; const char *message; };\n'
                  '\n'
                  'int tap_output(const struct result *r, int n, char *out, size_t cap) { return -9; }\n'
                  'void tap_summary(const struct result *r, int n, char *out) { out[0] = 0; }\n'
                  'int tap_exit_code(const struct result *r, int n) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct result r[] = {\n'
                 '        {"add works", 0, NULL},\n'
                 '        {"sub overflow", 1, "expected -1, got 0"},\n'
                 '        {"network", 2, "no network in sandbox"},\n'
                 '        {"flaky", 2, NULL},\n'
                 '        {"crash", 1, NULL},\n'
                 '    };\n'
                 '    char out[1024];\n'
                 '    int n = tap_output(r, 5, out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    char sum[64];\n'
                 '    tap_summary(r, 5, sum);\n'
                 '    printf("%s%d\\n", sum, tap_exit_code(r, 5));\n'
                 '    n = tap_output(r, 0, out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    tap_summary(r, 0, sum);\n'
                 '    printf("%s%d\\n", sum, tap_exit_code(r, 0));\n'
                 '    char small[40];\n'
                 '    printf("%d %d\\n", tap_output(r, 1, small, sizeof small), tap_output(r, 5, small, '
                 'sizeof small));\n'
                 '    struct result many[300];\n'
                 '    for (int i = 0; i < 300; i++) { many[i].name = "t"; many[i].status = 1; '
                 'many[i].message = "x"; }\n'
                 '    printf("%d\\n", tap_exit_code(many, 300));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Формируйте каждую строку snprintf и добавляйте в отчёт, пока помещается (с нулём). '
               'Пропущенный тест — «ok» с директивой SKIP.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['196',
                    'TAP version 13',
                    '1..5',
                    'ok 1 - add works',
                    'not ok 2 - sub overflow',
                    '  ---',
                    '  message: expected -1, got 0',
                    '  ...',
                    'ok 3 - network # SKIP no network in sandbox',
                    'ok 4 - flaky # SKIP',
                    'not ok 5 - crash',
                    '  ---',
                    '  ...',
                    '# pass 1 fail 2 skip 2',
                    '2',
                    '20',
                    'TAP version 13',
                    '1..0',
                    '# pass 0 fail 0 skip 0',
                    '0',
                    '37 -1',
                    '255']},
      {'id': 'c13-reindent',
       'mode': 'c',
       'title': 'Мини-форматтер: отступы по скобкам',
       'statement': 'reindent(src, out, cap, width) → длина результата или −1: каждая строка '
                    'перепечатывается с отступом depth · width пробелов, где depth — число открытых «{» на '
                    'момент начала строки (строка, начинающаяся с «}», уменьшает глубину до печати); прежние '
                    'отступы (пробелы и табуляции в начале) и хвостовые пробелы отбрасываются; пустые строки '
                    'остаются пустыми (без пробелов); строки препроцессора («#» первым символом) печатаются '
                    'без отступа. Скобки внутри строковых литералов "…", символьных констант \'…\', '
                    'комментариев // и /* … */ (в том числе многострочных) не считаются. Последний перевод '
                    'строки сохраняется, если был. Глубина не уходит ниже нуля.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int reindent(const char *src, char *out, size_t cap, int width) { return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static void t(const char *src, int w) {\n'
                 '    char out[512];\n'
                 '    int n = reindent(src, out, sizeof out, w);\n'
                 '    printf("%d\\n", n);\n'
                 '    for (const char *p = out; *p; p++) printf("%c", *p == \' \' ? \'.\' : *p);\n'
                 '    if (n > 0 && out[n - 1] != \'\\n\') printf("\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t("int main(void) {\\nint x = 1;\\n  if (x) {\\n\\t\\treturn 0;\\n  }\\nreturn '
                 '1;\\n}\\n", 4);\n'
                 '    t("void f(void)\\n{\\nputs(\\"{ not a brace }\\");\\nchar c = \'{\';\\n// { '
                 'comment\\n/* { multi\\n} line */\\nx = 1;\\n}\\n", 2);\n'
                 '    t("#define X 1\\nvoid g(void) {\\n#ifdef X\\n  a();\\n#endif\\n}\\n}\\n}\\nint y;", '
                 '3);\n'
                 '    t("struct s {\\nint a;\\n\\n\\n   int b;   \\n};", 4);\n'
                 '    t("", 4);\n'
                 '    t("a {\\n b {\\n  c {\\n   d;\\n  }\\n }\\n}", 1);\n'
                 '    char tiny[8];\n'
                 '    printf("%d %d\\n", reindent("x;\\n", tiny, sizeof tiny, 4), '
                 'reindent("{\\n{\\n{\\nx;\\n", tiny, sizeof tiny, 4));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Идите по строкам: вычислите отступ по текущей глубине (если строка начинается с «}» — на '
               'единицу меньше), затем пройдите по символам строки, учитывая состояние «в строке / в символе '
               '/ в комментарии», и обновите глубину.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['85',
                    'int.main(void).{',
                    '....int.x.=.1;',
                    '....if.(x).{',
                    '........return.0;',
                    '....}',
                    '....return.1;',
                    '}',
                    '109',
                    'void.f(void)',
                    '{',
                    '..puts("{.not.a.brace.}");',
                    "..char.c.=.'{';",
                    '..//.{.comment',
                    '../*.{.multi',
                    '..}.line.*/',
                    '..x.=.1;',
                    '}',
                    '63',
                    '#define.X.1',
                    'void.g(void).{',
                    '#ifdef.X',
                    '...a();',
                    '#endif',
                    '}',
                    '}',
                    '}',
                    'int.y;',
                    '37',
                    'struct.s.{',
                    '....int.a;',
                    '',
                    '',
                    '....int.b;',
                    '};',
                    '0',
                    '29',
                    'a.{',
                    '.b.{',
                    '..c.{',
                    '...d;',
                    '..}',
                    '.}',
                    '}',
                    '3 -1']},
      {'id': 'c13-naming-checker',
       'mode': 'c',
       'title': 'Проверка имён по правилам стиля',
       'statement': 'name_ok(kind, name, prefix) → 0, если имя подходит, иначе код: 1 — неверный регистр или '
                    'недопустимые символы, 2 — нет обязательного префикса, 3 — зарезервированное имя '
                    '(начинается с «_» + заглавная, содержит «__» или начинается с «_» на верхнем уровне — у '
                    'любого вида), 4 — слишком длинное (> 31 символа). Виды: K_FUNC, K_VAR, K_TYPE — '
                    'snake_case (строчные буквы, цифры и одиночные «_» между ними, начинается с буквы, не '
                    'кончается «_»); K_MACRO, K_CONST — UPPER_SNAKE (то же заглавными); K_ENUM — '
                    'UPPER_SNAKE; prefix (может быть NULL или «») обязателен для K_FUNC, K_TYPE, K_MACRO, '
                    'K_ENUM: имя должно начинаться с prefix, за которым идёт «_» (для макросов и констант '
                    'prefix проверяется в верхнем регистре, для остальных — как записан). Порядок проверок: '
                    'зарезервированное (3) → длина (4) → регистр и символы (1) → префикс (2). K_VAR и '
                    'K_CONST префикса не требуют. suggest(kind, name, out) — превращает имя к виду kind: '
                    'CamelCase и camelCase → snake_case, для макросов — заглавные.',
       'starter': 'enum { K_FUNC, K_VAR, K_TYPE, K_MACRO, K_CONST, K_ENUM };\n'
                  '\n'
                  'int name_ok(int kind, const char *name, const char *prefix) { return -9; }\n'
                  'void suggest(int kind, const char *name, char *out) { out[0] = 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static void t(int kind, const char *name, const char *prefix) {\n'
                 '    printf("%d %s/%s -> %d\\n", kind, name, prefix ? prefix : "-", name_ok(kind, name, '
                 'prefix));\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t(K_FUNC, "list_push", "list");\n'
                 '    t(K_FUNC, "listPush", "list");\n'
                 '    t(K_FUNC, "push", "list");\n'
                 '    t(K_FUNC, "list_Push", "list");\n'
                 '    t(K_FUNC, "list_", "list");\n'
                 '    t(K_FUNC, "list__push", "list");\n'
                 '    t(K_FUNC, "_list_push", "list");\n'
                 '    t(K_FUNC, "_List", NULL);\n'
                 '    t(K_FUNC, "list2_push", "list2");\n'
                 '    t(K_FUNC, "listx_push", "list");\n'
                 '    t(K_VAR, "item_count", NULL);\n'
                 '    t(K_VAR, "ItemCount", NULL);\n'
                 '    t(K_VAR, "n", "");\n'
                 '    t(K_VAR, "1st", NULL);\n'
                 '    t(K_TYPE, "list_node", "list");\n'
                 '    t(K_TYPE, "ListNode", "list");\n'
                 '    t(K_MACRO, "LIST_MAX", "list");\n'
                 '    t(K_MACRO, "LIST_max", "list");\n'
                 '    t(K_MACRO, "MAX_LIST", "list");\n'
                 '    t(K_CONST, "MAX_RETRIES", NULL);\n'
                 '    t(K_CONST, "max_retries", NULL);\n'
                 '    t(K_ENUM, "LIST_OK", "list");\n'
                 '    t(K_ENUM, "OK", "list");\n'
                 '    t(K_FUNC, "this_name_is_way_too_long_for_the_style", "this");\n'
                 '    t(K_VAR, "this_name_is_exactly_31_chars_x", NULL);\n'
                 '    t(K_VAR, "", NULL);\n'
                 '    char out[64];\n'
                 '    const char *cs[] = {"listPushBack", "ListNode", "HTTPServer", "parse2Int", '
                 '"already_snake", "XMLHttpRequest", "a"};\n'
                 '    for (int i = 0; i < 7; i++) {\n'
                 '        suggest(K_FUNC, cs[i], out);\n'
                 '        printf("%s -> %s", cs[i], out);\n'
                 '        suggest(K_MACRO, cs[i], out);\n'
                 '        printf(" | %s\\n", out);\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Проверяйте в указанном порядке: зарезервированное, длина, символы и регистр, префикс. Для '
               'snake_case: не допускайте двойных подчёркиваний и подчёркивания на краях.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 list_push/list -> 0',
                    '0 listPush/list -> 1',
                    '0 push/list -> 2',
                    '0 list_Push/list -> 1',
                    '0 list_/list -> 1',
                    '0 list__push/list -> 3',
                    '0 _list_push/list -> 3',
                    '0 _List/- -> 3',
                    '0 list2_push/list2 -> 0',
                    '0 listx_push/list -> 2',
                    '1 item_count/- -> 0',
                    '1 ItemCount/- -> 1',
                    '1 n/ -> 0',
                    '1 1st/- -> 1',
                    '2 list_node/list -> 0',
                    '2 ListNode/list -> 1',
                    '3 LIST_MAX/list -> 0',
                    '3 LIST_max/list -> 1',
                    '3 MAX_LIST/list -> 2',
                    '4 MAX_RETRIES/- -> 0',
                    '4 max_retries/- -> 1',
                    '5 LIST_OK/list -> 0',
                    '5 OK/list -> 2',
                    '0 this_name_is_way_too_long_for_the_style/this -> 4',
                    '1 this_name_is_exactly_31_chars_x/- -> 0',
                    '1 /- -> 1',
                    'listPushBack -> list_push_back | LIST_PUSH_BACK',
                    'ListNode -> list_node | LIST_NODE',
                    'HTTPServer -> http_server | HTTP_SERVER',
                    'parse2Int -> parse2_int | PARSE2_INT',
                    'already_snake -> already_snake | ALREADY_SNAKE',
                    'XMLHttpRequest -> xml_http_request | XML_HTTP_REQUEST',
                    'a -> a | A']},
      {'id': 'c13-line-lint',
       'mode': 'c',
       'title': 'Линтер строк: длина, пробелы, табуляции, TODO',
       'statement': 'lint_lines(text, msgs, max) → список сообщений вида «line N: …» в порядке строк (внутри '
                    'строки — в порядке правил): «line N: too long (L > 80)» — длина строки без перевода '
                    'строки больше 80 символов (L — длина); «line N: trailing whitespace» — пробел или '
                    'табуляция в конце; «line N: tab character» — в строке есть символ табуляции (в любом '
                    'месте, даже если он же хвостовой: оба сообщения выдаются); «line N: TODO without owner» '
                    '— «TODO» не в форме TODO(имя); «line N: CRLF» — строка заканчивается \\r. После всех '
                    'строк: «EOF: no newline at end of file», если текст не пуст и не заканчивается \\n; '
                    '«EOF: extra blank lines», если текст заканчивается двумя и более пустыми строками '
                    '(\\n\\n\\n и больше). Возврат — число сообщений (не больше max).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int lint_lines(const char *text, char msgs[][64], int max) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static void t(const char *label, const char *s) {\n'
                 '    char m[16][64];\n'
                 '    int n = lint_lines(s, m, 16);\n'
                 '    printf("%s: %d\\n", label, n);\n'
                 '    for (int i = 0; i < n; i++) printf("  %s\\n", m[i]);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t("clean", "int x;\\n// TODO(ann): fix\\nreturn 0;\\n");\n'
                 '    char longl[120];\n'
                 "    memset(longl, 'a', 90);\n"
                 '    longl[90] = 0;\n'
                 '    char buf[256];\n'
                 '    sprintf(buf, "%s\\nshort\\n", longl);\n'
                 '    t("long", buf);\n'
                 "    memset(longl, 'b', 80);\n"
                 '    longl[80] = 0;\n'
                 '    sprintf(buf, "%s\\n", longl);\n'
                 '    t("exact80", buf);\n'
                 '    t("trail", "a \\nb\\t\\nc\\n");\n'
                 '    t("tabs", "\\tindent\\nmid\\tdle\\n");\n'
                 '    t("todo", "// TODO fix\\n// TODO(): x\\n// TODO(bob): ok\\n/* TODO */\\n");\n'
                 '    t("crlf", "a\\r\\nb\\r\\n");\n'
                 '    t("eof", "last line");\n'
                 '    t("blank", "a\\n\\n\\n");\n'
                 '    t("blank2", "a\\n\\n");\n'
                 '    t("empty", "");\n'
                 '    t("mix", "x = 1; \\t\\n    TODO\\n\\n\\n");\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Идите по строкам; длину считайте без \\r и \\n. «TODO(имя)» допустимо, если после TODO сразу '
               '«(», внутри скобок есть хотя бы один символ и есть «)».',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['clean: 0',
                    'long: 1',
                    '  line 1: too long (90 > 80)',
                    'exact80: 0',
                    'trail: 3',
                    '  line 1: trailing whitespace',
                    '  line 2: trailing whitespace',
                    '  line 2: tab character',
                    'tabs: 2',
                    '  line 1: tab character',
                    '  line 2: tab character',
                    'todo: 3',
                    '  line 1: TODO without owner',
                    '  line 2: TODO without owner',
                    '  line 4: TODO without owner',
                    'crlf: 2',
                    '  line 1: CRLF',
                    '  line 2: CRLF',
                    'eof: 1',
                    '  EOF: no newline at end of file',
                    'blank: 1',
                    '  EOF: extra blank lines',
                    'blank2: 0',
                    'empty: 0',
                    'mix: 4',
                    '  line 1: trailing whitespace',
                    '  line 1: tab character',
                    '  line 2: TODO without owner',
                    '  EOF: extra blank lines']},
      {'id': 'c13-func-metrics',
       'mode': 'c',
       'title': 'Метрики функций: длина и цикломатическая сложность',
       'statement': 'struct fm { char name[32]; int lines; int complexity; }. analyze(src, out, max) находит '
                    'определения функций верхнего уровня (имя перед «(» на строке, заканчивающейся «)» или '
                    '«) {»; открывающая «{» на этой же или следующей строке; глубина фигурных скобок вне '
                    'функции равна 0) и для каждой записывает имя, число строк от строки сигнатуры до строки '
                    'с закрывающей «}» включительно и сложность = 1 + число токенов if, for, while, case, '
                    '&&, ||, ? в теле (в сигнатуре не считаются; внутри строк, символов и комментариев не '
                    'считаются; «else if» даёт один if; «do { } while (…);» даёт один while). Возвращает '
                    'число функций (не больше max). Объявления struct/enum/union и инициализаторы глобальных '
                    'данных функциями не считаются. worst(out, n) → индекс самой сложной функции (при '
                    'равенстве — самой длинной, затем первой).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct fm { char name[32]; int lines; int complexity; };\n'
                  '\n'
                  'int analyze(const char *src, struct fm *out, int max) { return 0; }\n'
                  'int worst(const struct fm *f, int n) { return -2; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    const char *src =\n'
                 '        "#include <stdio.h>\\n"\n'
                 '        "struct pt { int x, y; };\\n"\n'
                 '        "static int table[] = {1, 2, 3};\\n"\n'
                 '        "\\n"\n'
                 '        "int add(int a, int b) {\\n"\n'
                 '        "    return a + b;\\n"\n'
                 '        "}\\n"\n'
                 '        "\\n"\n'
                 '        "/* if while for in comment */\\n"\n'
                 '        "static int classify(int x)\\n"\n'
                 '        "{\\n"\n'
                 '        "    if (x < 0 && x > -10) return -1;   // if inside comment\\n"\n'
                 '        "    else if (x == 0 || x == 1) return 0;\\n"\n'
                 '        "    for (int i = 0; i < x; i++) {\\n"\n'
                 '        "        while (i > 100) i--;\\n"\n'
                 '        "    }\\n"\n'
                 '        "    switch (x) {\\n"\n'
                 '        "    case 5: return 5;\\n"\n'
                 '        "    case 6: return x > 3 ? 6 : 7;\\n"\n'
                 '        "    }\\n"\n'
                 '        "    puts(\\"if (while) for\\");\\n"\n'
                 '        "    return 2;\\n"\n'
                 '        "}\\n"\n'
                 '        "void tiny(void) { }\\n"\n'
                 '        "int loop(int n) {\\n"\n'
                 '        "    do { n--; } while (n > 0);\\n"\n'
                 '        "    return n;\\n"\n'
                 '        "}\\n";\n'
                 '    struct fm f[8];\n'
                 '    int n = analyze(src, f, 8);\n'
                 '    printf("%d\\n", n);\n'
                 '    for (int i = 0; i < n; i++) printf("%s lines=%d cx=%d\\n", f[i].name, f[i].lines, '
                 'f[i].complexity);\n'
                 '    printf("%d\\n", worst(f, n));\n'
                 '    printf("%d %d\\n", analyze(src, f, 2), analyze("", f, 8));\n'
                 '    printf("%d\\n", worst(f, 0));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Сначала замените комментарии и строки пробелами (переводы строк сохраните), затем идите по '
               'символам, отслеживая глубину скобок: «{» на глубине 0 после «)» открывает функцию.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['4',
                    'add lines=3 cx=1',
                    'classify lines=14 cx=10',
                    'tiny lines=1 cx=1',
                    'loop lines=4 cx=2',
                    '1',
                    '2 0',
                    '-1']},
      {'id': 'c13-comment-checker',
       'mode': 'c',
       'title': 'Проверка комментариев: TODO, закомментированный код, документация',
       'statement': 'check_comments(src, msgs, max) → сообщения «line N: …» в порядке строк: «line N: TODO» '
                    '— строка содержит TODO или FIXME внутри комментария (// или /* … */); «line N: '
                    'commented-out code» — строка целиком — комментарий «//», текст после «//» (без пробелов '
                    'по краям) непустой и заканчивается «;», «{» или «}»; «line N: function without comment» '
                    '— строка начинается с идентификатора (в начале строки, без пробелов), содержит «(» и '
                    'заканчивается «)» или «) {», это определение функции (следующая значимая строка — «{» '
                    'или строка оканчивается «{»), а предыдущая строка не является комментарием (не '
                    'начинается с «//», «/*» или «*» и не заканчивается «*/»). Первые строки проверяются без '
                    'предыдущей (считается, что комментария нет). Возврат — число сообщений (не больше max).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int check_comments(const char *src, char msgs[][64], int max) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static void t(const char *label, const char *s) {\n'
                 '    char m[16][64];\n'
                 '    int n = check_comments(s, m, 16);\n'
                 '    printf("%s: %d\\n", label, n);\n'
                 '    for (int i = 0; i < n; i++) printf("  %s\\n", m[i]);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t("doc", "/* adds numbers */\\nint add(int a, int b) {\\n    return a + b;\\n}\\n");\n'
                 '    t("nodoc", "int add(int a, int b) {\\n    return a + b;\\n}\\n");\n'
                 '    t("allman", "// sub\\nint sub(int a, int b)\\n{\\n    return a - b;\\n}\\nint mul(int '
                 'a, int b)\\n{\\n    return a * b;\\n}\\n");\n'
                 '    t("proto", "int add(int a, int b);\\nstatic void f(void);\\n");\n'
                 '    t("todo", "// TODO: fix\\nint x; /* FIXME later */\\n/* long\\n   TODO '
                 'inside\\n*/\\nint y; // fine\\n");\n'
                 '    t("code", "// x = 5;\\n// if (x) {\\n//   }\\n// explanation of things\\n//\\n// '
                 'call(x)\\n");\n'
                 '    t("call", "void run(void) {\\n    helper(1);\\n}\\n");\n'
                 '    t("block", "/**\\n * doc\\n */\\nint documented(void) {\\n    return 1;\\n}\\n");\n'
                 '    t("indent", "    helper(1);\\nstatic int s(int a) {\\n    return a;\\n}\\n");\n'
                 '    t("empty", "");\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Разберите текст на строки; следите за состоянием «внутри /* … */». Для определения функции: '
               'строка начинается не с пробела, содержит «(», оканчивается на «)» или «) {», а скобка «{» '
               'стоит на ней или на следующей значимой строке.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['doc: 0',
                    'nodoc: 1',
                    '  line 1: function without comment',
                    'allman: 1',
                    '  line 6: function without comment',
                    'proto: 0',
                    'todo: 3',
                    '  line 1: TODO',
                    '  line 2: TODO',
                    '  line 4: TODO',
                    'code: 3',
                    '  line 1: commented-out code',
                    '  line 2: commented-out code',
                    '  line 3: commented-out code',
                    'call: 1',
                    '  line 1: function without comment',
                    'block: 0',
                    'indent: 1',
                    '  line 2: function without comment',
                    'empty: 0']},
      {'id': 'c13-header-hygiene',
       'mode': 'c',
       'title': 'Гигиена заголовочных файлов',
       'statement': 'check_header(text, msgs, max) → сообщения о заголовке (в порядке строк, затем '
                    "итоговые): «line N: definition of 'x' in header» — на верхнем уровне (вне фигурных "
                    'скобок) строка вида «тип имя;» или «тип имя = …;» без extern, static, typedef, '
                    'struct/union/enum-объявления без имени переменной и без «(» (это объявление функции); '
                    '«line N: function body in header» — определение функции (строка оканчивается «) {» или '
                    '«)» с «{» на следующей строке) без static/inline перед ней; «line N: include after '
                    'code» — #include после первой строки, не являющейся комментарием, пустой, директивой '
                    'или include; в конце: «no include guard» — нет ни «#pragma once», ни пары '
                    '#ifndef/#define в начале. Допустимо одно сообщение каждого вида на строку. Возврат — '
                    'число сообщений (до max).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int check_header(const char *text, char msgs[][64], int max) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static void t(const char *label, const char *s) {\n'
                 '    char m[16][64];\n'
                 '    int n = check_header(s, m, 16);\n'
                 '    printf("%s: %d\\n", label, n);\n'
                 '    for (int i = 0; i < n; i++) printf("  %s\\n", m[i]);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t("good", "#ifndef FOO_H\\n#define FOO_H\\n#include <stddef.h>\\n\\n/* api */\\nextern '
                 'int counter;\\nint add(int a, int b);\\nstruct node;\\ntypedef struct node '
                 'node_t;\\nstatic inline int twice(int x) {\\n    return 2 * x;\\n}\\n#endif\\n");\n'
                 '    t("noguard", "int add(int a, int b);\\n");\n'
                 '    t("pragma", "#pragma once\\nextern const char *names[];\\n");\n'
                 '    t("defs", "#ifndef X_H\\n#define X_H\\nint counter = 0;\\nint total;\\nstatic int '
                 'hidden = 1;\\nconst char *name = \\"x\\";\\nint table[10];\\n#endif\\n");\n'
                 '    t("body", "#pragma once\\nint add(int a, int b) {\\n    return a + b;\\n}\\nvoid '
                 'noop(void)\\n{\\n}\\nstatic inline int ok(void) { return 1; }\\n");\n'
                 '    t("late", "#pragma once\\n#include <stdio.h>\\nint f(void);\\n#include '
                 '<stdlib.h>\\n");\n'
                 '    t("nested", "#ifndef Y_H\\n#define Y_H\\nstruct s {\\n    int field;\\n    int '
                 'other;\\n};\\nenum e { A, B };\\n#endif\\n");\n'
                 '    t("empty", "");\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Идите по строкам, отслеживая глубину скобок: нужны только строки на глубине 0. Переменная — '
               'строка без «(», без extern/static/typedef и заканчивающаяся «;»; функция с телом — строка с '
               '«(» и «{» на ней или на следующей.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['good: 0',
                    'noguard: 1',
                    '  no include guard',
                    'pragma: 0',
                    'defs: 4',
                    "  line 3: definition of 'counter' in header",
                    "  line 4: definition of 'total' in header",
                    "  line 6: definition of 'name' in header",
                    "  line 7: definition of 'table' in header",
                    'body: 2',
                    '  line 2: function body in header',
                    '  line 5: function body in header',
                    'late: 1',
                    '  line 4: include after code',
                    'nested: 0',
                    'empty: 1',
                    '  no include guard']},
      {'id': 'c13-cleanup-goto',
       'mode': 'c',
       'title': 'Единый блок очистки: goto cleanup',
       'statement': 'struct alloc { void *(*malloc)(size_t); void (*free)(void *); } (как в задаче про '
                    'отказы аллокатора). build_report(a, title, vals, n, *out) → 0 и строка «title: v1, v2, '
                    '…, vn» (для n = 0 — «title: (none)»), либо −1 при любом отказе выделения, причём *out '
                    'не меняется и ничего не утекает. Выделений три: временный массив строк-чисел (n строк '
                    'по 12 байт), буфер формата для всего отчёта и итоговая строка (отчёт собирается во '
                    'временный буфер, затем копируется в итоговый блок точного размера). Оформите функцию с '
                    'единым блоком очистки (goto cleanup) в конце. summary(a, vals, n, *out) → 0 и строка '
                    '«min=… max=… sum=…» (для n = 0 — «empty»), два выделения (временный блок под числа и '
                    'итоговая строка), тоже с блоком очистки.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct alloc { void *(*malloc)(size_t); void (*free)(void *); };\n'
                  '\n'
                  'int build_report(const struct alloc *a, const char *title, const int *vals, size_t n, '
                  'char **out) { return -9; }\n'
                  'int summary(const struct alloc *a, const int *vals, size_t n, char **out) { return -9; '
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int calls, fail_at, live, total;\n'
                 '\n'
                 'static void *f_malloc(size_t n) {\n'
                 '    calls++;\n'
                 '    if (calls == fail_at) return NULL;\n'
                 '    void *p = malloc(n);\n'
                 '    if (p) { live++; total++; }\n'
                 '    return p;\n'
                 '}\n'
                 'static void f_free(void *p) { if (p) { live--; free(p); } }\n'
                 '\n'
                 'static const struct alloc A = {f_malloc, f_free};\n'
                 'static void reset(int at) { calls = 0; fail_at = at; live = 0; total = 0; }\n'
                 '\n'
                 'int main(void) {\n'
                 '    int v[] = {3, -1, 4, 1, -5, 9};\n'
                 '    char *s = NULL;\n'
                 '    reset(0);\n'
                 '    int rc = build_report(&A, "scores", v, 6, &s);\n'
                 '    printf("%d [%s] live=%d allocs=%d\\n", rc, s, live, total);\n'
                 '    A.free(s);\n'
                 '    for (int k = 1; k <= 3; k++) {\n'
                 '        char *t = (char *)0x1;\n'
                 '        reset(k);\n'
                 '        rc = build_report(&A, "scores", v, 6, &t);\n'
                 '        printf("fail@%d: %d live=%d untouched=%d\\n", k, rc, live, t == (char *)0x1);\n'
                 '    }\n'
                 '    reset(0);\n'
                 '    rc = build_report(&A, "none", v, 0, &s);\n'
                 '    printf("%d [%s]\\n", rc, s);\n'
                 '    A.free(s);\n'
                 '    reset(0);\n'
                 '    rc = build_report(&A, "one", v, 1, &s);\n'
                 '    printf("%d [%s]\\n", rc, s);\n'
                 '    A.free(s);\n'
                 '    reset(0);\n'
                 '    rc = summary(&A, v, 6, &s);\n'
                 '    printf("%d [%s] live=%d allocs=%d\\n", rc, s, live, total);\n'
                 '    A.free(s);\n'
                 '    for (int k = 1; k <= 2; k++) {\n'
                 '        char *t = (char *)0x1;\n'
                 '        reset(k);\n'
                 '        rc = summary(&A, v, 6, &t);\n'
                 '        printf("summary fail@%d: %d live=%d untouched=%d\\n", k, rc, live, t == (char '
                 '*)0x1);\n'
                 '    }\n'
                 '    reset(0);\n'
                 '    rc = summary(&A, v, 0, &s);\n'
                 '    printf("%d [%s]\\n", rc, s);\n'
                 '    A.free(s);\n'
                 '    printf("%d\\n", live);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Объявите все указатели NULL в начале, при любой ошибке — goto cleanup; в cleanup '
               'освобождайте всё (free(NULL) безопасен). Отдавая результат вызывающему, обнулите локальный '
               'указатель, чтобы не освободить его.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 [scores: 3, -1, 4, 1, -5, 9] live=1 allocs=3',
                    'fail@1: -1 live=0 untouched=1',
                    'fail@2: -1 live=0 untouched=1',
                    'fail@3: -1 live=0 untouched=1',
                    '0 [none: (none)]',
                    '0 [one: 3]',
                    '0 [min=-5 max=9 sum=11] live=1 allocs=2',
                    'summary fail@1: -1 live=0 untouched=1',
                    'summary fail@2: -1 live=0 untouched=1',
                    '0 [empty]',
                    '0']},
      {'id': 'c13-fix-const',
       'mode': 'c',
       'title': 'Исправьте: const-корректность',
       'statement': 'Программа собирается с -Wall -Wextra -Werror -Wcast-qual -Wwrite-strings и не '
                    'компилируется: функции count_char, sum и first_word_len принимают неконстантные '
                    'указатели, хотя только читают данные, find_char отбрасывает const приведением типа, а '
                    'greeting возвращает строковый литерал как char *. Исправьте сигнатуры: параметры, '
                    'которые функции не меняют, — const; find_char возвращает const char *; greeting — const '
                    'char *. Поведение функций не меняется.',
       'starter': '#include <stddef.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'size_t count_char(char *s, char c) {\n'
                  '    size_t n = 0;\n'
                  '    for (; *s; s++) n += *s == c;\n'
                  '    return n;\n'
                  '}\n'
                  '\n'
                  'long sum(int *a, size_t n) {\n'
                  '    long s = 0;\n'
                  '    for (size_t i = 0; i < n; i++) s += a[i];\n'
                  '    return s;\n'
                  '}\n'
                  '\n'
                  'char *find_char(const char *s, char c) {\n'
                  '    for (; *s; s++)\n'
                  '        if (*s == c) return (char *)s;\n'
                  '    return NULL;\n'
                  '}\n'
                  '\n'
                  'size_t first_word_len(char *s) {\n'
                  '    size_t n = 0;\n'
                  "    while (s[n] && s[n] != ' ') n++;\n"
                  '    return n;\n'
                  '}\n'
                  '\n'
                  'char *greeting(void) {\n'
                  '    return "hello";\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    const char *text = "hello big world";\n'
                 '    const int arr[] = {1, 2, 3, 4};\n'
                 '    printf("%zu %ld\\n", count_char(text, \'l\'), sum(arr, 4));\n'
                 "    const char *r = find_char(text, 'b');\n"
                 '    printf("%s %d\\n", r, find_char(text, \'z\') == NULL);\n'
                 '    printf("%zu %zu\\n", first_word_len(text), first_word_len(""));\n'
                 '    const char *g = greeting();\n'
                 '    printf("%s %zu\\n", g, strlen(g));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'const char * для входных строк и const int * для входных массивов. Результат поиска внутри '
               'константной строки — тоже const char *: приведение к char * не нужно.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -Wextra -Werror -Wcast-qual -Wwrite-strings -Wdiscarded-qualifiers',
       'expected': ['3 10', 'big world 1', '5 0', 'hello 5']},
      {'id': 'c13-fix-warnings',
       'mode': 'c',
       'title': 'Исправьте: сборка без предупреждений (-Werror)',
       'statement': 'Код компилируется с -Wall -Wextra -Wshadow -Wformat=2 -Werror и не проходит: в нём '
                    'неиспользуемые параметры и переменные, затенённое имя, неверный формат printf, '
                    'сравнение знакового с беззнаковым, отсутствие возврата в ветке и неявный проход в '
                    'switch. Исправьте так, чтобы сборка шла без предупреждений, а результаты остались '
                    'прежними (описаны в комментариях над функциями).',
       'starter': '#include <stddef.h>\n'
                  '#include <stdio.h>\n'
                  '\n'
                  '/* сумма чисел до n включительно */\n'
                  'int sum_to(int n, int unused) {\n'
                  '    int total = 0;\n'
                  '    int i;\n'
                  '    for (i = 1; i <= n; i++) {\n'
                  '        int total = i;\n'
                  '        (void)total;\n'
                  '    }\n'
                  '    for (i = 1; i <= n; i++) total += i;\n'
                  '    return total;\n'
                  '}\n'
                  '\n'
                  '/* индекс первого элемента > limit или -1 */\n'
                  'int first_above(const int *a, size_t n, int limit) {\n'
                  '    for (int i = 0; i < n; i++)\n'
                  '        if (a[i] > limit) return i;\n'
                  '}\n'
                  '\n'
                  '/* печать числа и размера в буфер */\n'
                  'void describe(char *buf, size_t cap, long value, size_t size) {\n'
                  '    snprintf(buf, cap, "v=%d size=%d", value, size);\n'
                  '}\n'
                  '\n'
                  '/* оценка: 0 — A, 1 — B, 2 — C, иначе F */\n'
                  'char grade(int level) {\n'
                  "    char g = 'F';\n"
                  '    switch (level) {\n'
                  '    case 0:\n'
                  "        g = 'A';\n"
                  '    case 1:\n'
                  "        g = 'B';\n"
                  '        break;\n'
                  '    case 2:\n'
                  "        g = 'C';\n"
                  '        break;\n'
                  '    }\n'
                  '    return g;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%d %d %d\\n", sum_to(10, 0), sum_to(0, 5), sum_to(100, 1));\n'
                 '    int a[] = {1, 5, 3, 9, 2};\n'
                 '    printf("%d %d %d\\n", first_above(a, 5, 4), first_above(a, 5, 100), first_above(a, 0, '
                 '0));\n'
                 '    char buf[64];\n'
                 '    describe(buf, sizeof buf, -123456789012L, 42);\n'
                 '    printf("%s\\n", buf);\n'
                 '    printf("%c %c %c %c\\n", grade(0), grade(1), grade(2), grade(7));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Неиспользуемый параметр — (void)unused; затенённую переменную уберите; счётчик цикла — '
               'size_t; формат для long — %ld, для size_t — %zu; в switch — break в каждой ветке и default.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -Wextra -Wshadow -Wformat=2 -Werror',
       'expected': ['55 0 5050', '1 -1 -1', 'v=-123456789012 size=42', 'A B C F']},
      {'id': 'c13-fix-risky',
       'mode': 'c',
       'title': 'Исправьте: опасные конструкции (присваивание в условии, пустое тело, провал)',
       'statement': 'Код не проходит сборку с -Wall -Wextra -Werror -Wparentheses -Wimplicit-fallthrough '
                    '-Wswitch-default -Wmisleading-indentation -Wempty-body: присваивание вместо сравнения в '
                    'условии, пустое тело после if и while, вводящие в заблуждение отступы, неявный проход в '
                    'switch. Исправьте так, чтобы предупреждений не было, а функции работали так, как '
                    'описано в комментариях; severity: коды 1 и 2 дают 3 (2 + 1), код 3 даёт 1, остальные 0.',
       'starter': '/* 1, если x равно 5 */\n'
                  'int is_five(int x) {\n'
                  '    if (x = 5) return 1;\n'
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  '/* число символов до первого пробела */\n'
                  'int word_len(const char *s) {\n'
                  '    int n = 0;\n'
                  "    while (s[n] && s[n] != ' ');\n"
                  '        n++;\n'
                  '    return n;\n'
                  '}\n'
                  '\n'
                  '/* сумма чётных элементов */\n'
                  'int sum_even(const int *a, int n) {\n'
                  '    int s = 0;\n'
                  '    for (int i = 0; i < n; i++)\n'
                  '        if (a[i] % 2 == 0);\n'
                  '            s += a[i];\n'
                  '    return s;\n'
                  '}\n'
                  '\n'
                  '/* количество дней в месяце (не високосный год) */\n'
                  'int days_in_month(int m) {\n'
                  '    int d = 0;\n'
                  '    switch (m) {\n'
                  '    case 2:\n'
                  '        d = 28;\n'
                  '        break;\n'
                  '    case 4: case 6: case 9: case 11:\n'
                  '        d = 30;\n'
                  '        break;\n'
                  '    case 1: case 3: case 5: case 7: case 8: case 10: case 12:\n'
                  '        d = 31;\n'
                  '    }\n'
                  '    return d;\n'
                  '}\n'
                  '\n'
                  '/* коды 1 и 2 дают 3 (2 + 1), код 3 даёт 1, остальные 0 */\n'
                  'int severity(int code) {\n'
                  '    int level = 0;\n'
                  '    switch (code) {\n'
                  '    case 1:\n'
                  '    case 2:\n'
                  '        level = 2;\n'
                  '    case 3:\n'
                  '        level += 1;\n'
                  '        break;\n'
                  '    }\n'
                  '    return level;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%d %d %d\\n", is_five(5), is_five(4), is_five(0));\n'
                 '    printf("%d %d %d\\n", word_len("hello world"), word_len(""), word_len("x"));\n'
                 '    int a[] = {1, 2, 3, 4, 6, 7};\n'
                 '    printf("%d %d\\n", sum_even(a, 6), sum_even(a, 0));\n'
                 '    for (int m = 0; m <= 13; m++) printf("%d ", days_in_month(m));\n'
                 '    printf("\\n");\n'
                 '    for (int c = 0; c <= 4; c++) printf("%d ", severity(c));\n'
                 '    printf("\\n");\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Сравнение — «==»; точка с запятой после if/while превращает тело в пустое — уберите её и '
               'поставьте скобки. В severity проход из case 1/2 в case 3 давал 3: перепишите явно (2 + 1) и '
               'добавьте break и default.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -Wextra -Werror -Wparentheses -Wimplicit-fallthrough '
                '-Wswitch-default -Wmisleading-indentation -Wempty-body',
       'expected': ['1 0 0', '5 0 1', '12 0', '0 31 28 31 30 31 30 31 31 30 31 30 31 0', '0 3 3 1 0']},
      {'id': 'c13-safe-strings',
       'mode': 'c',
       'title': 'Безопасные строковые функции с размером',
       'statement': 'str_copy(dst, size, src) → длина src (как strlcpy): копирует не более size − 1 символа, '
                    'всегда ставит ноль (при size > 0). str_cat(dst, size, src) → длина, которая получилась '
                    'бы без усечения (strlen(dst) + strlen(src)); если в dst нет нуля в пределах size — '
                    'возвращает size + strlen(src) и ничего не пишет. str_trim(s) → новая длина: убирает '
                    'пробельные символы (isspace) с обоих концов на месте. str_split_n(s, delim, out, max) → '
                    'число полей: разделяет строку на месте по символу delim (пустые поля сохраняются), в '
                    'out — указатели; когда набрано max полей, остаток строки (вместе с разделителями) '
                    'остаётся в последнем поле. str_starts(s, p), str_ends(s, p) → 1/0; str_repeat(dst, '
                    'size, s, k) → длина, которая получилась бы (s повторена k раз), запись усечена до size '
                    '− 1. Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'size_t str_copy(char *dst, size_t size, const char *src) { return 0; }\n'
                  'size_t str_cat(char *dst, size_t size, const char *src) { return 0; }\n'
                  'size_t str_trim(char *s) { return 99; }\n'
                  'int str_split_n(char *s, char delim, char **out, int max) { return -1; }\n'
                  'int str_starts(const char *s, const char *p) { return -1; }\n'
                  'int str_ends(const char *s, const char *p) { return -1; }\n'
                  'size_t str_repeat(char *dst, size_t size, const char *s, int k) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char *b = malloc(8);\n'
                 '    size_t n = str_copy(b, 8, "hello");\n'
                 '    printf("%zu [%s] ", n, b);\n'
                 '    n = str_copy(b, 4, "hello world");\n'
                 '    printf("%zu [%s] ", n, b);\n'
                 "    b[0] = 'x';\n"
                 '    n = str_copy(b, 0, "abc");\n'
                 '    printf("%zu %c\\n", n, b[0]);\n'
                 '    n = str_copy(b, 8, "ab");\n'
                 '    n = str_cat(b, 8, "cdefghij");\n'
                 '    printf("%zu [%s]\\n", n, b);\n'
                 '    n = str_copy(b, 8, "");\n'
                 '    n = str_cat(b, 8, "xyz");\n'
                 '    printf("%zu [%s]\\n", n, b);\n'
                 "    char full[4] = {'a', 'b', 'c', 'd'};\n"
                 '    printf("%zu\\n", str_cat(full, 4, "zz"));\n'
                 '    free(b);\n'
                 '    char t1[] = "  hello \\t\\n", t2[] = "no-trim", t3[] = "   ", t4[] = "";\n'
                 '    printf("%zu [%s] %zu [%s] %zu [%s] %zu [%s]\\n", str_trim(t1), t1, str_trim(t2), t2, '
                 'str_trim(t3), t3, str_trim(t4), t4);\n'
                 '    char s1[] = "a,b,,c,", *f[8];\n'
                 "    int k = str_split_n(s1, ',', f, 8);\n"
                 '    printf("%d:", k);\n'
                 '    for (int i = 0; i < k; i++) printf(" [%s]", f[i]);\n'
                 '    printf("\\n");\n'
                 '    char s2[] = "a,b,c,d,e";\n'
                 "    k = str_split_n(s2, ',', f, 3);\n"
                 '    printf("%d: [%s] [%s] [%s]\\n", k, f[0], f[1], f[2]);\n'
                 '    char s3[] = "single";\n'
                 "    k = str_split_n(s3, ',', f, 4);\n"
                 '    printf("%d [%s]\\n", k, f[0]);\n'
                 '    char s4[] = "";\n'
                 '    printf("%d %d\\n", str_split_n(s4, \',\', f, 4), str_split_n(s4, \',\', f, 0));\n'
                 '    printf("%d %d %d %d\\n", str_starts("foobar", "foo"), str_starts("foo", "foobar"), '
                 'str_starts("x", ""), str_ends("foobar", "bar"));\n'
                 '    printf("%d %d %d\\n", str_ends("bar", "foobar"), str_ends("x", ""), str_ends("abc", '
                 '"bc"));\n'
                 '    char r[10];\n'
                 '    n = str_repeat(r, sizeof r, "ab", 3);\n'
                 '    printf("%zu [%s] ", n, r);\n'
                 '    n = str_repeat(r, sizeof r, "abcd", 5);\n'
                 '    printf("%zu [%s] ", n, r);\n'
                 '    n = str_repeat(r, sizeof r, "x", 0);\n'
                 '    printf("%zu [%s]\\n", n, r);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'str_copy возвращает длину src всегда — по ней вызывающий узнаёт об усечении. str_cat: '
               'найдите конец dst в пределах size и дальше пользуйтесь str_copy.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['5 [hello] 11 [hel] 3 x',
                    '10 [abcdefg]',
                    '3 [xyz]',
                    '6',
                    '5 [hello] 7 [no-trim] 0 [] 0 []',
                    '5: [a] [b] [] [c] []',
                    '3: [a] [b] [c,d,e]',
                    '1 [single]',
                    '1 0',
                    '1 0 1 1',
                    '0 1 1',
                    '6 [ababab] 20 [abcdabcda] 0 []']},
      {'id': 'c13-contracts',
       'mode': 'c',
       'title': 'Контракты: REQUIRE, ENSURE, INVARIANT с обработчиком',
       'statement': 'typedef void (*contract_fn)(const char *kind, const char *expr). '
                    'contract_set_handler(h) (NULL — вернуть обработчик по умолчанию), contract_violations() '
                    '— число нарушений, contract_last_kind(), contract_last_expr() — вид и текст последнего '
                    'нарушения (пока ничего не нарушено — «»), contract_reset(). Макросы: REQUIRE(c), '
                    'ENSURE(c), INVARIANT(c) — при ложном условии вызывают обработчик с видом '
                    '«require»/«ensure»/«invariant» и текстом условия (#c), увеличивают счётчик, и '
                    'выполнение продолжается. Обработчик по умолчанию только запоминает вид и текст. struct '
                    'stk { int a[4]; int n; } с функциями: stk_init; stk_push(s, v) → 0, REQUIRE(s->n < 4) — '
                    'при нарушении возвращает −1 без записи; stk_pop(s, *out) → 0, REQUIRE(s->n > 0) — иначе '
                    '−1 (*out не меняется); обе операции в конце делают INVARIANT(s->n >= 0 && s->n <= 4) и '
                    'ENSURE (push: ENSURE(s->a[s->n - 1] == v); pop: ENSURE(*out == прежнему верхнему '
                    'элементу)).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'typedef void (*contract_fn)(const char *kind, const char *expr);\n'
                  '\n'
                  'void contract_set_handler(contract_fn h) {}\n'
                  'int contract_violations(void) { return -1; }\n'
                  'const char *contract_last_kind(void) { return "?"; }\n'
                  'const char *contract_last_expr(void) { return "?"; }\n'
                  'void contract_reset(void) {}\n'
                  '\n'
                  '#define REQUIRE(c)\n'
                  '#define ENSURE(c)\n'
                  '#define INVARIANT(c)\n'
                  '\n'
                  'struct stk { int a[4]; int n; };\n'
                  'void stk_init(struct stk *s) { s->n = 0; }\n'
                  'int stk_push(struct stk *s, int v) { return -9; }\n'
                  'int stk_pop(struct stk *s, int *out) { return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static int hcalls;\n'
                 'static char hlog[8][64];\n'
                 'static void my_handler(const char *kind, const char *expr) {\n'
                 '    if (hcalls < 8) snprintf(hlog[hcalls], 64, "%s: %s", kind, expr);\n'
                 '    hcalls++;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct stk s;\n'
                 '    stk_init(&s);\n'
                 '    int v = -1;\n'
                 '    int r1 = stk_pop(&s, &v);\n'
                 '    printf("%d %d | %d [%s] [%s]\\n", r1, v, contract_violations(), contract_last_kind(), '
                 'contract_last_expr());\n'
                 '    for (int i = 1; i <= 4; i++) stk_push(&s, i * 10);\n'
                 '    printf("%d %d\\n", s.n, contract_violations());\n'
                 '    int r2 = stk_push(&s, 99);\n'
                 '    printf("%d %d %d [%s]\\n", r2, s.n, contract_violations(), contract_last_expr());\n'
                 '    int top = 0;\n'
                 '    int r3 = stk_pop(&s, &top);\n'
                 '    printf("%d %d %d\\n", r3, top, s.n);\n'
                 '    contract_set_handler(my_handler);\n'
                 '    contract_reset();\n'
                 '    printf("%d [%s]\\n", contract_violations(), contract_last_kind());\n'
                 '    stk_init(&s);\n'
                 '    stk_pop(&s, &v);\n'
                 '    for (int i = 0; i < 6; i++) stk_push(&s, i);\n'
                 '    printf("%d %d\\n", hcalls, contract_violations());\n'
                 '    for (int i = 0; i < hcalls; i++) printf("  %s\\n", hlog[i]);\n'
                 '    contract_set_handler(NULL);\n'
                 '    hcalls = 0;\n'
                 '    stk_pop(&s, &v);\n'
                 '    stk_pop(&s, &v);\n'
                 '    stk_pop(&s, &v);\n'
                 '    stk_pop(&s, &v);\n'
                 '    stk_pop(&s, &v);\n'
                 '    printf("%d %d [%s] [%s]\\n", hcalls, contract_violations(), contract_last_kind(), '
                 'contract_last_expr());\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Один внутренний макрос CHECK_(kind, c) с do { if (!(c)) fail(kind, #c); } while (0); fail '
               'увеличивает счётчик, запоминает вид и текст и вызывает пользовательский обработчик (если '
               'задан).',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['-1 -1 | 1 [require] [s->n > 0]',
                    '4 1',
                    '-1 4 2 [s->n < 4]',
                    '0 40 3',
                    '0 []',
                    '3 3',
                    '  require: s->n > 0',
                    '  require: s->n < 4',
                    '  require: s->n < 4',
                    '0 4 [require] [s->n > 0]']},
      {'id': 'c13-arg-parser',
       'mode': 'c',
       'title': 'Разбор аргументов командной строки',
       'statement': 'struct opts { int verbose, help, count; const char *name; const char *files[8]; int '
                    'nfiles; }. parse_args(argc, argv, o, err, cap) → 0 или код ошибки; argv[0] — имя '
                    'программы (пропускается). Значения по умолчанию: count = 1, остальное — 0/NULL. '
                    'Поддерживаются: -v/--verbose, -h/--help (можно объединять булевы короткие: -vh); -n '
                    'ЧИСЛО, -nЧИСЛО, --count=ЧИСЛО, --count ЧИСЛО (целое 1…1000); --name=ИМЯ и --name ИМЯ; '
                    '«--» — дальше всё позиционные; всё без «-» в начале (и одиночный «-») — позиционные в '
                    'files (до 8). Ошибки (разбор останавливается, текст — в err): −1 «unknown option: '
                    '<арг>», −2 «missing value for <опция>» (опция последняя или значение — следующий '
                    'аргумент отсутствует), −3 «invalid number: <значение>», −4 «too many files».',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct opts { int verbose, help, count; const char *name; const char *files[8]; int '
                  'nfiles; };\n'
                  '\n'
                  'int parse_args(int argc, char **argv, struct opts *o, char *err, size_t cap) { return -9; '
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'static void t(int argc, char **argv) {\n'
                 '    struct opts o;\n'
                 '    char err[64];\n'
                 '    int rc = parse_args(argc, argv, &o, err, sizeof err);\n'
                 '    printf("%d [%s] v=%d h=%d n=%d name=%s files=%d:", rc, err, o.verbose, o.help, '
                 'o.count, o.name ? o.name : "-", o.nfiles);\n'
                 '    for (int i = 0; i < o.nfiles; i++) printf(" %s", o.files[i]);\n'
                 '    printf("\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    char *a1[] = {"prog", "-v", "file.txt", "--name=alice", "-n", "5", "other"};\n'
                 '    t(7, a1);\n'
                 '    char *a2[] = {"prog", "-vh", "--count", "12", "--name", "bob", "--", "-x", "--y"};\n'
                 '    t(9, a2);\n'
                 '    char *a3[] = {"prog"};\n'
                 '    t(1, a3);\n'
                 '    char *a4[] = {"prog", "-n10", "--count=7", "-"};\n'
                 '    t(4, a4);\n'
                 '    char *a5[] = {"prog", "--bogus"};\n'
                 '    t(2, a5);\n'
                 '    char *a6[] = {"prog", "-vq"};\n'
                 '    t(2, a6);\n'
                 '    char *a7[] = {"prog", "-n"};\n'
                 '    t(2, a7);\n'
                 '    char *a8[] = {"prog", "--name"};\n'
                 '    t(2, a8);\n'
                 '    char *a9[] = {"prog", "-n", "abc"};\n'
                 '    t(3, a9);\n'
                 '    char *a10[] = {"prog", "--count=0"};\n'
                 '    t(2, a10);\n'
                 '    char *a11[] = {"prog", "--count=1001"};\n'
                 '    t(2, a11);\n'
                 '    char *a12[] = {"prog", "1", "2", "3", "4", "5", "6", "7", "8", "9"};\n'
                 '    t(10, a12);\n'
                 '    char *a13[] = {"prog", "--verbose", "--help", "--vervose"};\n'
                 '    t(4, a13);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Один цикл по аргументам с флагом «после --». Для опций со значением значение либо после «=», '
               'либо в следующем аргументе. Короткие булевы флаги в одном аргументе разбирайте по символам; '
               '-n забирает остаток аргумента или следующий.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 [] v=1 h=0 n=5 name=alice files=2: file.txt other',
                    '0 [] v=1 h=1 n=12 name=bob files=2: -x --y',
                    '0 [] v=0 h=0 n=1 name=- files=0:',
                    '0 [] v=0 h=0 n=7 name=- files=1: -',
                    '-1 [unknown option: --bogus] v=0 h=0 n=1 name=- files=0:',
                    '-1 [unknown option: -q] v=1 h=0 n=1 name=- files=0:',
                    '-2 [missing value for -n] v=0 h=0 n=1 name=- files=0:',
                    '-2 [missing value for --name] v=0 h=0 n=1 name=- files=0:',
                    '-3 [invalid number: abc] v=0 h=0 n=1 name=- files=0:',
                    '-3 [invalid number: 0] v=0 h=0 n=1 name=- files=0:',
                    '-3 [invalid number: 1001] v=0 h=0 n=1 name=- files=0:',
                    '-4 [too many files] v=0 h=0 n=1 name=- files=8: 1 2 3 4 5 6 7 8',
                    '-1 [unknown option: --vervose] v=1 h=1 n=1 name=- files=0:']},
      {'id': 'c13-ci-matrix',
       'mode': 'c',
       'title': 'Матрица конфигураций сборки для CI',
       'statement': 'make_matrix(compilers, nc, opts, no, sans, ns, out, max) → число конфигураций (строк в '
                    'out[][96], не больше max): для каждого компилятора, для каждого уровня оптимизации, для '
                    'каждого санитайзера (в этом порядке) строка «<cc> -O<opt> -g» (если санитайзер «none») '
                    'или «<cc> -O<opt> -g -fsanitize=<san>». Исключаются комбинации: санитайзер «memory» — '
                    'только для компилятора, имя которого начинается с «clang»; комбинация «address» и '
                    '«thread» в одной конфигурации (например, «address+thread») недопустима; '
                    '«thread+undefined» допустима, «address+undefined» допустима; пустое имя санитайзера '
                    'недопустимо. excluded_count(…) → сколько комбинаций исключено; describe_exclusions(…, '
                    'out) — по строке «<cc> -O<opt> <san>: <причина>» для каждой исключённой (причины: '
                    '«memory needs clang», «address+thread conflict», «empty sanitizer»).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'size_t make_matrix(const char *const *compilers, int nc, const char *const *opts, int no, '
                  'const char *const *sans, int ns, char out[][96], size_t max) { return 0; }\n'
                  'int excluded_count(const char *const *compilers, int nc, const char *const *opts, int no, '
                  'const char *const *sans, int ns) { return -1; }\n'
                  'int describe_exclusions(const char *const *compilers, int nc, const char *const *opts, '
                  'int no, const char *const *sans, int ns, char out[][96], int max) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <math.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    const char *cc[] = {"gcc", "clang"};\n'
                 '    const char *op[] = {"0", "2"};\n'
                 '    const char *sa[] = {"none", "address", "undefined", "address+undefined", "memory", '
                 '"thread", "address+thread", ""};\n'
                 '    char out[64][96];\n'
                 '    size_t n = make_matrix(cc, 2, op, 2, sa, 8, out, 64);\n'
                 '    printf("%zu %d\\n", n, excluded_count(cc, 2, op, 2, sa, 8));\n'
                 '    for (size_t i = 0; i < n; i++) printf("%s\\n", out[i]);\n'
                 '    int e = describe_exclusions(cc, 2, op, 2, sa, 8, out, 64);\n'
                 '    printf("%d\\n", e);\n'
                 '    for (int i = 0; i < e; i++) printf("%s\\n", out[i]);\n'
                 '    printf("%zu\\n", make_matrix(cc, 2, op, 2, sa, 8, out, 5));\n'
                 '    const char *one[] = {"gcc"};\n'
                 '    const char *z[] = {"0"};\n'
                 '    const char *none[] = {"none"};\n'
                 '    n = make_matrix(one, 1, z, 1, none, 1, out, 64);\n'
                 '    printf("%zu %s\\n", n, out[0]);\n'
                 '    printf("%zu %d\\n", make_matrix(cc, 0, op, 2, sa, 8, out, 64), excluded_count(cc, 0, '
                 'op, 2, sa, 8));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Отдельная функция reason(cc, san) возвращает причину исключения или NULL; три функции '
               'используют её и обходят тройной цикл в одном порядке: компилятор, оптимизация, санитайзер.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['22 10',
                    'gcc -O0 -g',
                    'gcc -O0 -g -fsanitize=address',
                    'gcc -O0 -g -fsanitize=undefined',
                    'gcc -O0 -g -fsanitize=address+undefined',
                    'gcc -O0 -g -fsanitize=thread',
                    'gcc -O2 -g',
                    'gcc -O2 -g -fsanitize=address',
                    'gcc -O2 -g -fsanitize=undefined',
                    'gcc -O2 -g -fsanitize=address+undefined',
                    'gcc -O2 -g -fsanitize=thread',
                    'clang -O0 -g',
                    'clang -O0 -g -fsanitize=address',
                    'clang -O0 -g -fsanitize=undefined',
                    'clang -O0 -g -fsanitize=address+undefined',
                    'clang -O0 -g -fsanitize=memory',
                    'clang -O0 -g -fsanitize=thread',
                    'clang -O2 -g',
                    'clang -O2 -g -fsanitize=address',
                    'clang -O2 -g -fsanitize=undefined',
                    'clang -O2 -g -fsanitize=address+undefined',
                    'clang -O2 -g -fsanitize=memory',
                    'clang -O2 -g -fsanitize=thread',
                    '10',
                    'gcc -O0 memory: memory needs clang',
                    'gcc -O0 address+thread: address+thread conflict',
                    'gcc -O0 : empty sanitizer',
                    'gcc -O2 memory: memory needs clang',
                    'gcc -O2 address+thread: address+thread conflict',
                    'gcc -O2 : empty sanitizer',
                    'clang -O0 address+thread: address+thread conflict',
                    'clang -O0 : empty sanitizer',
                    'clang -O2 address+thread: address+thread conflict',
                    'clang -O2 : empty sanitizer',
                    '5',
                    '1 gcc -O0 -g',
                    '0 0']}]}
