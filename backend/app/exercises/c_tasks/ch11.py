"""Задачи книги «От assembler к языку C»: глава 11 (код компилируется gcc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {11: [{'id': 'c11-fix-off-by-one',
       'mode': 'c',
       'title': 'Исправьте: выход за границу массива на единицу',
       'statement': 'sum_array, max_array и count_equal обходят массив из n элементов циклом с лишней '
                    'итерацией (i <= n) и читают один элемент за границей. Под AddressSanitizer программа '
                    'останавливается. Исправьте циклы; для n = 0 функции должны работать без чтения: сумма '
                    '0, max_array(…, 0) → INT_MIN, count_equal → 0.',
       'starter': '#include <stddef.h>\n'
                  '#include <limits.h>\n'
                  '\n'
                  'long sum_array(const int *a, size_t n) {\n'
                  '    long s = 0;\n'
                  '    for (size_t i = 0; i <= n; i++) s += a[i];\n'
                  '    return s;\n'
                  '}\n'
                  '\n'
                  'int max_array(const int *a, size_t n) {\n'
                  '    int m = INT_MIN;\n'
                  '    for (size_t i = 0; i <= n; i++)\n'
                  '        if (a[i] > m) m = a[i];\n'
                  '    return m;\n'
                  '}\n'
                  '\n'
                  'size_t count_equal(const int *a, size_t n, int v) {\n'
                  '    size_t c = 0;\n'
                  '    for (size_t i = 0; i <= n; i++)\n'
                  '        if (a[i] == v) c++;\n'
                  '    return c;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    size_t n = 6;\n'
                 '    int *a = malloc(n * sizeof *a);\n'
                 '    int src[] = {4, -2, 9, 4, 0, 4};\n'
                 '    memcpy(a, src, sizeof src);\n'
                 '    printf("%ld %d %zu\\n", sum_array(a, n), max_array(a, n), count_equal(a, n, 4));\n'
                 '    printf("%ld %d %zu\\n", sum_array(a, 0), max_array(a, 0), count_equal(a, 0, 4));\n'
                 '    free(a);\n'
                 '    int *one = malloc(sizeof *one);\n'
                 '    *one = -7;\n'
                 '    printf("%ld %d %zu\\n", sum_array(one, 1), max_array(one, 1), count_equal(one, 1, '
                 '-7));\n'
                 '    free(one);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Условие продолжения цикла — i < n. Массив из n элементов имеет индексы 0 … n − 1.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['19 9 3', '0 -2147483648 0', '-7 -7 1']},
      {'id': 'c11-fix-strcpy-nul',
       'mode': 'c',
       'title': 'Исправьте: забытый завершающий ноль в malloc',
       'statement': 'dup_string(s) и join(a, sep, b) выделяют память без учёта завершающего нуля, и '
                    'strcpy/strcat пишут на байт за блок. Исправьте: dup_string возвращает копию строки; '
                    'join — «a» + sep + «b» в новой строке; repeat(s, k) — строка s, повторённая k раз (k ≥ '
                    '0, при k = 0 — пустая строка). Все результаты освобождает вызывающий.',
       'starter': '#include <stdlib.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'char *dup_string(const char *s) {\n'
                  '    char *r = malloc(strlen(s));\n'
                  '    if (!r) return NULL;\n'
                  '    strcpy(r, s);\n'
                  '    return r;\n'
                  '}\n'
                  '\n'
                  'char *join(const char *a, const char *sep, const char *b) {\n'
                  '    char *r = malloc(strlen(a) + strlen(sep) + strlen(b));\n'
                  '    if (!r) return NULL;\n'
                  '    strcpy(r, a);\n'
                  '    strcat(r, sep);\n'
                  '    strcat(r, b);\n'
                  '    return r;\n'
                  '}\n'
                  '\n'
                  'char *repeat(const char *s, int k) {\n'
                  '    char *r = malloc(strlen(s) * (size_t)k);\n'
                  '    if (!r) return NULL;\n'
                  '    r[0] = 0;\n'
                  '    for (int i = 0; i < k; i++) strcat(r, s);\n'
                  '    return r;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char *a = dup_string("hello");\n'
                 '    char *e = dup_string("");\n'
                 '    char *j = join("left", " + ", "right");\n'
                 '    char *j2 = join("", "", "");\n'
                 '    char *r = repeat("ab", 3);\n'
                 '    char *r0 = repeat("xyz", 0);\n'
                 '    printf("[%s] [%s] [%s] [%s] [%s] [%s]\\n", a, e, j, j2, r, r0);\n'
                 '    printf("%zu %zu %zu\\n", strlen(a), strlen(j), strlen(r));\n'
                 '    free(a); free(e); free(j); free(j2); free(r); free(r0);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Всегда +1 под завершающий ноль. Для repeat — длина s · k + 1; при k = 0 всё равно нужен один '
               'байт.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['[hello] [] [left + right] [] [ababab] []', '5 12 6']},
      {'id': 'c11-fix-uaf-list',
       'mode': 'c',
       'title': 'Исправьте: чтение узла после free',
       'statement': 'struct node { int v; struct node *next; }. list_free(h) освобождает весь список, а '
                    'list_remove_all(h, v) удаляет из списка все узлы со значением v и возвращает новую '
                    'голову. Сейчас обе функции читают поле next уже освобождённого узла. Исправьте. Под '
                    'AddressSanitizer.',
       'starter': '#include <stdlib.h>\n'
                  '\n'
                  'struct node { int v; struct node *next; };\n'
                  '\n'
                  'void list_free(struct node *h) {\n'
                  '    while (h) {\n'
                  '        free(h);\n'
                  '        h = h->next;\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'struct node *list_remove_all(struct node *h, int v) {\n'
                  '    struct node **pp = &h;\n'
                  '    while (*pp) {\n'
                  '        if ((*pp)->v == v) {\n'
                  '            free(*pp);\n'
                  '            *pp = (*pp)->next;\n'
                  '        } else {\n'
                  '            pp = &(*pp)->next;\n'
                  '        }\n'
                  '    }\n'
                  '    return h;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static struct node *build(const int *v, int n) {\n'
                 '    struct node *h = NULL, **tail = &h;\n'
                 '    for (int i = 0; i < n; i++) {\n'
                 '        struct node *x = malloc(sizeof *x);\n'
                 '        x->v = v[i];\n'
                 '        x->next = NULL;\n'
                 '        *tail = x;\n'
                 '        tail = &x->next;\n'
                 '    }\n'
                 '    return h;\n'
                 '}\n'
                 '\n'
                 'static void show(const struct node *h) {\n'
                 '    for (; h; h = h->next) printf("%d ", h->v);\n'
                 '    printf("|\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    int a[] = {3, 7, 3, 3, 5, 7, 3};\n'
                 '    struct node *h = build(a, 7);\n'
                 '    h = list_remove_all(h, 3);\n'
                 '    show(h);\n'
                 '    h = list_remove_all(h, 7);\n'
                 '    show(h);\n'
                 '    h = list_remove_all(h, 9);\n'
                 '    show(h);\n'
                 '    h = list_remove_all(h, 5);\n'
                 '    show(h);\n'
                 '    h = list_remove_all(h, 5);\n'
                 '    show(h);\n'
                 '    struct node *g = build(a, 7);\n'
                 '    list_free(g);\n'
                 '    list_free(NULL);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Прежде чем free(узел), сохраните его next в переменную; при удалении — сначала переключите '
               'указатель, потом освобождайте.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['7 5 7 |', '5 |', '5 |', '|', '|']},
      {'id': 'c11-fix-double-free',
       'mode': 'c',
       'title': 'Исправьте: двойное освобождение на пути ошибки',
       'statement': 'process(text, *result) разбирает строку «число число число» в массив из двух буферов и '
                    'возвращает 0 при успехе (*result — массив long из malloc, их количество — в *count) или '
                    'код ошибки (−1 нет памяти не моделируем; −2 в тексте не число; −3 пустой текст), при '
                    'ошибке *result не трогается. На пути ошибки буфер освобождается дважды (в ветке ошибки '
                    'и в общей очистке). Исправьте так, чтобы каждый блок освобождался ровно один раз. Под '
                    'AddressSanitizer.',
       'starter': '#include <stdlib.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'int process(const char *text, long **result, size_t *count) {\n'
                  '    long *buf = malloc(16 * sizeof *buf);\n'
                  '    size_t n = 0;\n'
                  '    int rc = 0;\n'
                  '    char *copy = malloc(strlen(text) + 1);\n'
                  '    strcpy(copy, text);\n'
                  '    for (char *t = strtok(copy, " "); t; t = strtok(NULL, " ")) {\n'
                  '        char *end;\n'
                  '        long v = strtol(t, &end, 10);\n'
                  '        if (*end) {\n'
                  '            free(buf);\n'
                  '            rc = -2;\n'
                  '            goto done;\n'
                  '        }\n'
                  '        if (n < 16) buf[n++] = v;\n'
                  '    }\n'
                  '    if (n == 0) {\n'
                  '        free(buf);\n'
                  '        rc = -3;\n'
                  '        goto done;\n'
                  '    }\n'
                  '    *result = buf;\n'
                  '    *count = n;\n'
                  'done:\n'
                  '    free(copy);\n'
                  '    if (rc) free(buf);\n'
                  '    return rc;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static void t(const char *s) {\n'
                 '    long *r = NULL;\n'
                 '    size_t n = 0;\n'
                 '    int rc = process(s, &r, &n);\n'
                 '    printf("[%s] rc=%d n=%zu r=%d:", s, rc, n, r != NULL);\n'
                 '    for (size_t i = 0; r && i < n; i++) printf(" %ld", r[i]);\n'
                 '    printf("\\n");\n'
                 '    free(r);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t("1 2 3");\n'
                 '    t("10 x 30");\n'
                 '    t("");\n'
                 '    t("   ");\n'
                 '    t("-5");\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Освобождение — только в общем блоке очистки (done), и один раз: убрать free(buf) из веток '
               'ошибок.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['[1 2 3] rc=0 n=3 r=1: 1 2 3',
                    '[10 x 30] rc=-2 n=0 r=0:',
                    '[] rc=-3 n=0 r=0:',
                    '[   ] rc=-3 n=0 r=0:',
                    '[-5] rc=0 n=1 r=1: -5']},
      {'id': 'c11-fix-leak',
       'mode': 'c',
       'title': 'Исправьте: утечка на ранних выходах',
       'statement': 'load_pair(text, *out) разбирает «имя:значение» в struct pair { char *name; int value; } '
                    '(имя копируется в malloc) и возвращает 0 при успехе, иначе −1 (нет двоеточия), −2 '
                    '(пустое имя), −3 (значение не число). На ошибочных путях выделенная память теряется. '
                    'Исправьте. pair_free(p) освобождает поля. Под AddressSanitizer (LeakSanitizer ловит '
                    'утечки при выходе).',
       'starter': '#include <stdlib.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'struct pair { char *name; int value; };\n'
                  '\n'
                  'int load_pair(const char *text, struct pair *out) {\n'
                  "    const char *colon = strchr(text, ':');\n"
                  '    if (!colon) return -1;\n'
                  '    size_t n = (size_t)(colon - text);\n'
                  '    char *name = malloc(n + 1);\n'
                  '    memcpy(name, text, n);\n'
                  '    name[n] = 0;\n'
                  '    if (n == 0) return -2;\n'
                  '    char *end;\n'
                  '    long v = strtol(colon + 1, &end, 10);\n'
                  '    if (end == colon + 1 || *end) return -3;\n'
                  '    out->name = name;\n'
                  '    out->value = (int)v;\n'
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  'void pair_free(struct pair *p) {\n'
                  '    free(p->name);\n'
                  '    p->name = NULL;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    const char *t[] = {"alpha:10", "nocolon", ":5", "x:", "beta:12z", "gamma:-7", '
                 '"d:+3"};\n'
                 '    for (int i = 0; i < 7; i++) {\n'
                 '        struct pair p = {NULL, 0};\n'
                 '        int rc = load_pair(t[i], &p);\n'
                 '        printf("%s -> %d %s %d\\n", t[i], rc, p.name ? p.name : "-", p.value);\n'
                 '        if (rc == 0) pair_free(&p);\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Выделяйте память после всех проверок — тогда на ранних выходах освобождать нечего. Или '
               'освобождайте на каждом выходе.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['alpha:10 -> 0 alpha 10',
                    'nocolon -> -1 - 0',
                    ':5 -> -2 - 0',
                    'x: -> -3 - 0',
                    'beta:12z -> -3 - 0',
                    'gamma:-7 -> 0 gamma -7',
                    'd:+3 -> 0 d 3']},
      {'id': 'c11-fix-uninit',
       'mode': 'c',
       'title': 'Исправьте: чтение неинициализированных переменных',
       'statement': 'count_positive(a, n), mean(a, n) → double (0.0 для n = 0), first_negative(a, n) → '
                    'индекс первого отрицательного или −1, histogram(a, n, bins) заполняют результат, '
                    'используя локальные переменные без начального значения. Драйвер заранее «загрязняет» '
                    'стек, поэтому результат случайный. Инициализируйте переменные (и массив бинов нулями) '
                    'так, чтобы результат был правильным всегда. histogram(a, n, bins[4]): bins[0] — число '
                    'значений < 0, bins[1] — от 0 до 9, bins[2] — от 10 до 99, bins[3] — остальные (≥ 100).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int count_positive(const int *a, int n) {\n'
                  '    int cnt;\n'
                  '    for (int i = 0; i < n; i++)\n'
                  '        if (a[i] > 0) cnt++;\n'
                  '    return cnt;\n'
                  '}\n'
                  '\n'
                  'double mean(const int *a, int n) {\n'
                  '    double sum;\n'
                  '    for (int i = 0; i < n; i++) sum += a[i];\n'
                  '    return n ? sum / n : 0.0;\n'
                  '}\n'
                  '\n'
                  'int first_negative(const int *a, int n) {\n'
                  '    int idx;\n'
                  '    for (int i = 0; i < n; i++)\n'
                  '        if (a[i] < 0) { idx = i; break; }\n'
                  '    return idx;\n'
                  '}\n'
                  '\n'
                  'void histogram(const int *a, int n, int bins[4]) {\n'
                  '    for (int i = 0; i < n; i++) {\n'
                  '        int b = a[i] < 0 ? 0 : a[i] < 10 ? 1 : a[i] < 100 ? 2 : 3;\n'
                  '        bins[b]++;\n'
                  '    }\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static void poison(void) {\n'
                 '    volatile unsigned char b[4096];\n'
                 '    for (int i = 0; i < 4096; i++) b[i] = 0xAB;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    int a[] = {5, -3, 12, 0, 150, -1, 7};\n'
                 '    int e[] = {1};\n'
                 '    int r1, r3;\n'
                 '    double r2;\n'
                 '    int bins[4];\n'
                 '    poison();\n'
                 '    r1 = count_positive(a, 7);\n'
                 '    poison();\n'
                 '    r2 = mean(a, 7);\n'
                 '    poison();\n'
                 '    r3 = first_negative(a, 7);\n'
                 '    printf("%d %.4f %d\\n", r1, r2, r3);\n'
                 '    poison();\n'
                 '    r1 = count_positive(a, 0);\n'
                 '    poison();\n'
                 '    r3 = first_negative(e, 1);\n'
                 '    printf("%d %d\\n", r1, r3);\n'
                 '    poison();\n'
                 '    memset(bins, 0x7F, sizeof bins);\n'
                 '    histogram(a, 7, bins);\n'
                 '    printf("%d %d %d %d\\n", bins[0], bins[1], bins[2], bins[3]);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'int cnt = 0; double sum = 0; int idx = −1; и обнулите bins перед накоплением.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['4 24.2857 1', '0 -1', '2 3 1 1']},
      {'id': 'c11-fix-return-local',
       'mode': 'c',
       'title': 'Исправьте: возврат адреса локальной переменной',
       'statement': 'day_name(d) возвращает название дня недели (0 — Mon … 6 — Sun, иначе «???»), '
                    'month_name(m) — название месяца (1 — Jan … 12 — Dec, иначе «???»), make_range_label(lo, '
                    'hi) → строка «lo..hi» (память из malloc). Сейчас они возвращают указатели на локальные '
                    'массивы. Исправьте: day_name и month_name — указатели на строковые константы, '
                    'make_range_label — строка в куче (освобождает вызывающий).',
       'starter': '#include <stdio.h>\n'
                  '#include <stdlib.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'const char *day_name(int d) {\n'
                  '    char names[7][4] = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};\n'
                  '    if (d < 0 || d > 6) return "???";\n'
                  '    return names[d];\n'
                  '}\n'
                  '\n'
                  'const char *month_name(int m) {\n'
                  '    char buf[8];\n'
                  '    static const char *const t[] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", '
                  '"Aug", "Sep", "Oct", "Nov", "Dec"};\n'
                  '    if (m < 1 || m > 12) strcpy(buf, "???");\n'
                  '    else strcpy(buf, t[m - 1]);\n'
                  '    return buf;\n'
                  '}\n'
                  '\n'
                  'char *make_range_label(int lo, int hi) {\n'
                  '    char label[32];\n'
                  '    snprintf(label, sizeof label, "%d..%d", lo, hi);\n'
                  '    return label;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    const char *a = day_name(0), *b = day_name(6), *c = day_name(9);\n'
                 '    const char *m1 = month_name(1), *m2 = month_name(12), *m3 = month_name(0);\n'
                 '    char *l1 = make_range_label(1, 10), *l2 = make_range_label(-5, 5);\n'
                 '    printf("%s %s %s | %s %s %s | %s %s\\n", a, b, c, m1, m2, m3, l1, l2);\n'
                 '    free(l1);\n'
                 '    free(l2);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Названия — static const массив указателей на строки (живёт всю программу). Метку из '
               'локального буфера скопируйте в malloc.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['Mon Sun ??? | Jan Dec ??? | 1..10 -5..5']},
      {'id': 'c11-fix-midpoint',
       'mode': 'c',
       'title': 'Исправьте: переполнение при вычислении середины',
       'statement': 'midpoint(lo, hi) → середина отрезка (lo + hi) / 2 с округлением вниз к lo (для lo ≤ hi, '
                    'значения int любые, включая INT_MIN и INT_MAX); first_true(lo, hi, pred) → наименьшее x '
                    'из [lo, hi), для которого pred(x) ≠ 0, при условии что pred монотонна (сначала ложь, '
                    'потом истина), либо hi, если истины нет; avg_int(a, b) → среднее двух int, округлённое '
                    'к −∞. Сейчас вычисления через (lo + hi) / 2 переполняются и под UBSan программа '
                    'останавливается.',
       'starter': 'int midpoint(int lo, int hi) {\n'
                  '    return (lo + hi) / 2;\n'
                  '}\n'
                  '\n'
                  'int first_true(int lo, int hi, int (*pred)(int)) {\n'
                  '    while (lo < hi) {\n'
                  '        int mid = (lo + hi) / 2;\n'
                  '        if (pred(mid)) hi = mid;\n'
                  '        else lo = mid + 1;\n'
                  '    }\n'
                  '    return lo;\n'
                  '}\n'
                  '\n'
                  'int avg_int(int a, int b) {\n'
                  '    return (a + b) / 2;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static int big_threshold;\n'
                 'static int ge(int x) { return x >= big_threshold; }\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%d %d %d\\n", midpoint(2, 10), midpoint(INT_MAX - 2, INT_MAX), '
                 'midpoint(INT_MIN, INT_MIN + 2));\n'
                 '    printf("%d %d %d\\n", midpoint(INT_MIN, INT_MAX), midpoint(-3, 0), midpoint(5, 5));\n'
                 '    printf("%d %d %d\\n", avg_int(7, 8), avg_int(-7, -8), avg_int(INT_MAX, INT_MAX));\n'
                 '    big_threshold = 2000000000;\n'
                 '    printf("%d\\n", first_true(1000000000, INT_MAX, ge));\n'
                 '    big_threshold = INT_MAX;\n'
                 '    printf("%d\\n", first_true(0, INT_MAX, ge));\n'
                 '    big_threshold = 0;\n'
                 '    printf("%d\\n", first_true(INT_MIN, INT_MAX, ge));\n'
                 '    big_threshold = 7;\n'
                 '    printf("%d %d\\n", first_true(0, 5, ge), first_true(10, 10, ge));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Считайте в более широком типе (long long) или через lo + (hi − lo) / 2 с беззнаковой '
               'разностью. Округление вниз для отрицательных сумм — отдельный случай.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['6 2147483646 -2147483647',
                    '-1 -2 5',
                    '7 -8 2147483647',
                    '2000000000',
                    '2147483647',
                    '0',
                    '5 10']},
      {'id': 'c11-fix-shifts',
       'mode': 'c',
       'title': 'Исправьте: сдвиги на отрицательных и больших значениях',
       'statement': 'scale_pow2(x, k) → x · 2^k для k ≥ 0 и x / 2^|k| с округлением к −∞ для k < 0 (|k| < 31 '
                    'допустимо, для k < −30 → 0 или −1 по знаку x; для k > 30 при x ≠ 0 → результат не '
                    'определяем: вернуть INT_MAX или INT_MIN по знаку; x = 0 → 0). get_bits(v, lo, n) → n '
                    'бит, начиная с lo (n от 0 до 32, lo + n ≤ 32); set_bits(v, lo, n, val) → v с заменённым '
                    'полем. Сейчас сдвиги неопределены (отрицательные значения, ширина 32, сдвиг '
                    'отрицательного влево).',
       'starter': '#include <stdint.h>\n'
                  '\n'
                  'int scale_pow2(int x, int k) {\n'
                  '    return k >= 0 ? x << k : x >> -k;\n'
                  '}\n'
                  '\n'
                  'uint32_t get_bits(uint32_t v, int lo, int n) {\n'
                  '    return (v >> lo) & ((1u << n) - 1);\n'
                  '}\n'
                  '\n'
                  'uint32_t set_bits(uint32_t v, int lo, int n, uint32_t val) {\n'
                  '    uint32_t mask = ((1u << n) - 1) << lo;\n'
                  '    return (v & ~mask) | ((val << lo) & mask);\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%d %d %d %d\\n", scale_pow2(5, 3), scale_pow2(-5, 3), scale_pow2(40, -3), '
                 'scale_pow2(-41, -3));\n'
                 '    printf("%d %d %d %d\\n", scale_pow2(1, 30), scale_pow2(1, 31), scale_pow2(-1, 31), '
                 'scale_pow2(0, 40));\n'
                 '    printf("%d %d %d %d\\n", scale_pow2(123, -31), scale_pow2(-123, -31), '
                 'scale_pow2(INT_MAX, 1), scale_pow2(INT_MIN, -1));\n'
                 '    printf("%d %d\\n", scale_pow2(-1, -1), scale_pow2(-8, -3));\n'
                 '    printf("%#x %#x %#x %#x\\n", get_bits(0xDEADBEEF, 0, 32), get_bits(0xDEADBEEF, 16, '
                 '16), get_bits(0xDEADBEEF, 4, 0), get_bits(0xDEADBEEF, 28, 4));\n'
                 '    printf("%#x %#x %#x\\n", set_bits(0, 0, 32, 0x12345678), set_bits(0xFFFFFFFF, 8, 8, '
                 '0), set_bits(0xFFFF0000, 0, 0, 5));\n'
                 '    printf("%#x %#x\\n", set_bits(0, 28, 4, 0x1F), set_bits(0x12345678, 4, 8, 0xAB));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Сдвиг на 32 неопределён: для n = 32 маска — отдельный случай. Отрицательные значения сдвигам '
               'не передавайте — считайте умножением/делением в long long.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['40 -40 5 -6',
                    '1073741824 2147483647 -2147483648 0',
                    '0 -1 2147483647 -1073741824',
                    '-1 -1',
                    '0xdeadbeef 0xdead 0 0xd',
                    '0x12345678 0xffff00ff 0xffff0000',
                    '0xf0000000 0x12345ab8']},
      {'id': 'c11-fix-null-order',
       'mode': 'c',
       'title': 'Исправьте: проверка указателя после разыменования',
       'statement': 'struct str { const char *data; size_t len; }. str_len(s) → длина (NULL → 0), '
                    'str_first(s) → первый символ или 0 для пустой/NULL, str_equal(a, b) → 1 для равных (две '
                    'NULL равны, NULL равна пустой), get_or(p, dflt) → *p или dflt для NULL. Сейчас поля '
                    'читаются ДО проверки указателя на NULL — под UBSan программа останавливается (а '
                    'оптимизатор вправе удалить проверку). Исправьте порядок.',
       'starter': '#include <stddef.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'struct str { const char *data; size_t len; };\n'
                  '\n'
                  'size_t str_len(const struct str *s) {\n'
                  '    size_t n = s->len;\n'
                  '    if (!s) return 0;\n'
                  '    return n;\n'
                  '}\n'
                  '\n'
                  'char str_first(const struct str *s) {\n'
                  '    char c = s->data ? s->data[0] : 0;\n'
                  '    if (!s || s->len == 0) return 0;\n'
                  '    return c;\n'
                  '}\n'
                  '\n'
                  'int str_equal(const struct str *a, const struct str *b) {\n'
                  '    size_t la = a->len, lb = b->len;\n'
                  '    if (!a || !b) return (!a || la == 0) && (!b || lb == 0);\n'
                  '    return la == lb && (la == 0 || memcmp(a->data, b->data, la) == 0);\n'
                  '}\n'
                  '\n'
                  'int get_or(const int *p, int dflt) {\n'
                  '    int v = *p;\n'
                  '    return p ? v : dflt;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct str a = {"hello", 5}, b = {"hello", 5}, c = {"help", 4}, e = {"", 0}, e2 = '
                 '{NULL, 0};\n'
                 '    printf("%zu %zu %zu\\n", str_len(&a), str_len(NULL), str_len(&e));\n'
                 '    printf("%d %d %d %d\\n", str_first(&a), str_first(NULL), str_first(&e), '
                 'str_first(&e2));\n'
                 '    printf("%d %d %d %d %d %d\\n", str_equal(&a, &b), str_equal(&a, &c), str_equal(NULL, '
                 'NULL), str_equal(NULL, &e), str_equal(&a, NULL), str_equal(&e, &e2));\n'
                 '    int v = 9;\n'
                 '    printf("%d %d\\n", get_or(&v, 1), get_or(NULL, 1));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Любое обращение к s->… — только после проверки s. Для str_equal сначала вычислите длины с '
               'учётом NULL.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['5 0 0', '104 0 0 0', '1 0 1 1 0 1', '9 1']},
      {'id': 'c11-fix-misaligned',
       'mode': 'c',
       'title': 'Исправьте: невыровненные чтения через приведение указателей',
       'statement': 'read_u32(buf, off), read_u16(buf, off), write_u32(buf, off, v) читают и пишут числа в '
                    'произвольном месте байтового буфера (порядок байтов — как у платформы) через приведение '
                    'указателя к uint32_t * — это нарушает выравнивание. Перепишите через memcpy. '
                    'checksum32(buf, n) — сумма всех слов uint32_t по порядку из байтового буфера (последние '
                    'неполные байты не учитываются), тоже без приведения указателей.',
       'starter': '#include <stddef.h>\n'
                  '#include <stdint.h>\n'
                  '\n'
                  'uint32_t read_u32(const uint8_t *buf, size_t off) {\n'
                  '    return *(const uint32_t *)(buf + off);\n'
                  '}\n'
                  '\n'
                  'uint16_t read_u16(const uint8_t *buf, size_t off) {\n'
                  '    return *(const uint16_t *)(buf + off);\n'
                  '}\n'
                  '\n'
                  'void write_u32(uint8_t *buf, size_t off, uint32_t v) {\n'
                  '    *(uint32_t *)(buf + off) = v;\n'
                  '}\n'
                  '\n'
                  'uint32_t checksum32(const uint8_t *buf, size_t n) {\n'
                  '    uint32_t s = 0;\n'
                  '    for (size_t i = 0; i + 4 <= n; i += 4) s += *(const uint32_t *)(buf + i);\n'
                  '    return s;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    uint8_t *buf = malloc(32);\n'
                 '    for (int i = 0; i < 32; i++) buf[i] = (uint8_t)(i * 5 + 1);\n'
                 '    for (size_t off = 0; off < 5; off++) printf("%zu: %#x %#x\\n", off, read_u32(buf, '
                 'off), read_u16(buf, off + 1));\n'
                 '    write_u32(buf, 3, 0xA1B2C3D4);\n'
                 '    write_u32(buf, 9, 0x01020304);\n'
                 '    printf("%#x %#x %#x\\n", read_u32(buf, 3), buf[3], buf[6]);\n'
                 '    printf("%#x %#x %#x\\n", checksum32(buf, 32), checksum32(buf, 31), checksum32(buf, '
                 '3));\n'
                 '    free(buf);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'uint32_t v; memcpy(&v, buf + off, sizeof v); — компилятор сам сделает безопасное чтение '
               'нужной ширины.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0: 0x100b0601 0xb06',
                    '1: 0x15100b06 0x100b',
                    '2: 0x1a15100b 0x1510',
                    '3: 0x1f1a1510 0x1a15',
                    '4: 0x241f1a15 0x1f1a',
                    '0xa1b2c3d4 0xd4 0xa1',
                    '0x40dcd0aa 0xa4453e1d 0']},
      {'id': 'c11-fix-div-zero',
       'mode': 'c',
       'title': 'Исправьте: деление на ноль и INT_MIN / −1',
       'statement': 'safe_div(a, b, *out) → 0 и частное, если деление определено; иначе −1 при b = 0 и −2 '
                    'при INT_MIN / −1 (*out не меняется). safe_mod(a, b, *out) — то же для остатка (INT_MIN '
                    '% −1 — это тоже UB в C). percent(part, total) → целый процент, округлённый к ближайшему '
                    '(половина — вверх), либо −1, если total = 0; average(a, n) → среднее по массиву '
                    '(округление к нулю), для n = 0 — 0. Сейчас функции делят без проверки.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int safe_div(int a, int b, int *out) {\n'
                  '    *out = a / b;\n'
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  'int safe_mod(int a, int b, int *out) {\n'
                  '    *out = a % b;\n'
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  'int percent(int part, int total) {\n'
                  '    return (part * 100 + total / 2) / total;\n'
                  '}\n'
                  '\n'
                  'int average(const int *a, size_t n) {\n'
                  '    long long s = 0;\n'
                  '    for (size_t i = 0; i < n; i++) s += a[i];\n'
                  '    return (int)(s / (long long)n);\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    int r = 77, rc;\n'
                 '    rc = safe_div(17, 5, &r); printf("%d %d\\n", rc, r);\n'
                 '    rc = safe_div(-17, 5, &r); printf("%d %d\\n", rc, r);\n'
                 '    r = 77;\n'
                 '    rc = safe_div(1, 0, &r); printf("%d %d\\n", rc, r);\n'
                 '    rc = safe_div(INT_MIN, -1, &r); printf("%d %d\\n", rc, r);\n'
                 '    rc = safe_div(INT_MIN, 1, &r); printf("%d %d\\n", rc, r);\n'
                 '    r = 77;\n'
                 '    rc = safe_mod(17, 5, &r); printf("%d %d\\n", rc, r);\n'
                 '    rc = safe_mod(INT_MIN, -1, &r); printf("%d %d\\n", rc, r);\n'
                 '    rc = safe_mod(5, 0, &r); printf("%d %d\\n", rc, r);\n'
                 '    printf("%d %d %d %d\\n", percent(1, 3), percent(2, 3), percent(1, 8), percent(5, 0));\n'
                 '    printf("%d %d\\n", percent(INT_MAX, INT_MAX), percent(3, 2));\n'
                 '    int a[] = {INT_MAX, INT_MAX, INT_MAX, -5};\n'
                 '    printf("%d %d %d\\n", average(a, 4), average(a, 0), average(a + 3, 1));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Проверьте делитель и случай INT_MIN / −1 до деления; в percent используйте long long для '
               'part · 100.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 3',
                    '0 -3',
                    '-1 77',
                    '-2 77',
                    '0 -2147483648',
                    '0 2',
                    '-2 2',
                    '-1 2',
                    '33 67 13 -1',
                    '100 150',
                    '1610612734 0 -5']},
      {'id': 'c11-fix-array-index',
       'mode': 'c',
       'title': 'Исправьте: индекс за границей статического массива',
       'statement': 'В таблице static int table[8] = {2, 3, 5, 7, 11, 13, 17, 19} функция lookup(i) → '
                    'table[i] или −1, если индекс вне 0…7; update(i, v) → 0 при успехе или −1 (индекс '
                    'неверный); prime_at(n) → n-е простое число (с 1) из таблицы или −1; next_slot(cur) → '
                    '(cur + 1) по кругу (после 7 — 0, для неверного cur — −1). Сейчас проверка допускает i '
                    '== 8 (≤) и отрицательные индексы.',
       'starter': 'static int table[8] = {2, 3, 5, 7, 11, 13, 17, 19};\n'
                  '\n'
                  'int lookup(int i) {\n'
                  '    if (i > 8) return -1;\n'
                  '    return table[i];\n'
                  '}\n'
                  '\n'
                  'int update(int i, int v) {\n'
                  '    if (i > 8) return -1;\n'
                  '    table[i] = v;\n'
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  'int prime_at(int n) {\n'
                  '    return table[n];\n'
                  '}\n'
                  '\n'
                  'int next_slot(int cur) {\n'
                  '    return table[cur] ? (cur + 1) % 8 : 0;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%d %d %d %d %d\\n", lookup(0), lookup(7), lookup(8), lookup(-1), '
                 'lookup(100));\n'
                 '    printf("%d %d %d\\n", update(3, 70), update(8, 1), update(-5, 1));\n'
                 '    printf("%d %d %d %d %d\\n", lookup(3), prime_at(1), prime_at(8), prime_at(0), '
                 'prime_at(9));\n'
                 '    printf("%d %d %d %d\\n", next_slot(0), next_slot(7), next_slot(8), next_slot(-1));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Допустимые индексы: 0 ≤ i ≤ 7 (то есть i < 8). Для prime_at — индекс n − 1.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['2 19 -1 -1 -1', '0 -1 -1', '70 2 19 -1 -1', '1 0 -1 -1']},
      {'id': 'c11-fix-stack-overflow',
       'mode': 'c',
       'title': 'Исправьте: переполнение буфера на стеке',
       'statement': 'format_id(id, out, cap) записывает в out строку «ID-» и число минимум из четырёх цифр с '
                    'ведущими нулями (как «ID-%04d»), возвращая длину полного результата, как snprintf; '
                    'hexify(bytes, n, out, cap) → строчные шестнадцатеричные пары «aabbcc…»: пары не '
                    'разрываются — записывается столько целых пар, сколько помещается вместе с завершающим '
                    'нулём (при cap = 0 ничего не пишется); fill_pattern(out, n) → записывает n символов по '
                    'кругу «abc…» и завершающий ноль (out рассчитан на n + 1 байт). Сейчас функции собирают '
                    'результат в локальный буфер фиксированного размера без проверок — на длинных данных '
                    'возникает stack-buffer-overflow. Исправьте.',
       'starter': '#include <stdio.h>\n'
                  '#include <string.h>\n'
                  '#include <stddef.h>\n'
                  '\n'
                  'int format_id(int id, char *out, size_t cap) {\n'
                  '    char buf[8];\n'
                  '    sprintf(buf, "ID-%04d", id);\n'
                  '    snprintf(out, cap, "%s", buf);\n'
                  '    return (int)strlen(buf);\n'
                  '}\n'
                  '\n'
                  'void hexify(const unsigned char *bytes, size_t n, char *out, size_t cap) {\n'
                  '    char tmp[16];\n'
                  '    for (size_t i = 0; i < n; i++) sprintf(tmp + 2 * i, "%02x", bytes[i]);\n'
                  '    snprintf(out, cap, "%s", tmp);\n'
                  '}\n'
                  '\n'
                  'void fill_pattern(char *out, size_t n) {\n'
                  '    char tmp[10];\n'
                  "    for (size_t i = 0; i < n; i++) tmp[i] = (char)('a' + i % 3);\n"
                  '    tmp[n] = 0;\n'
                  '    strcpy(out, tmp);\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char out[64];\n'
                 '    int n = format_id(7, out, sizeof out);\n'
                 '    printf("%d %s\\n", n, out);\n'
                 '    n = format_id(123456789, out, sizeof out);\n'
                 '    printf("%d %s\\n", n, out);\n'
                 '    char small[6];\n'
                 '    n = format_id(123456789, small, sizeof small);\n'
                 '    printf("%d %s\\n", n, small);\n'
                 '    unsigned char b[] = {0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, '
                 '0x08, 0x09, 0x0A};\n'
                 '    hexify(b, 14, out, sizeof out);\n'
                 '    printf("%s\\n", out);\n'
                 '    hexify(b, 14, small, sizeof small);\n'
                 '    printf("%s\\n", small);\n'
                 "    char one[1] = {'x'};\n"
                 '    hexify(b, 3, one, 1);\n'
                 '    printf("%d\\n", one[0]);\n'
                 '    char *p = malloc(41);\n'
                 '    fill_pattern(p, 40);\n'
                 '    printf("%s %zu\\n", p, strlen(p));\n'
                 '    free(p);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Пишите сразу в out с учётом cap (snprintf), без промежуточных буферов фиксированного '
               'размера. В hexify следите за остатком cap − k.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['7 ID-0007',
                    '12 ID-123456789',
                    '12 ID-12',
                    'deadbeef0102030405060708090a',
                    'dead',
                    '0',
                    'abcabcabcabcabcabcabcabcabcabcabcabcabca 40']},
      {'id': 'c11-fix-realloc-dangling',
       'mode': 'c',
       'title': 'Исправьте: указатель на элемент после realloc',
       'statement': 'struct vec { int *data; size_t len, cap; }. vec_push_get(v, x) добавляет x и возвращает '
                    'указатель на добавленный элемент; vec_first_after_push(v, x) → значение первого '
                    'элемента вектора после добавления x (нужно прочитать после возможной перевыделения '
                    'памяти); vec_extend(v, other) добавляет все элементы other (который может быть тем же '
                    'вектором: v.extend(v) — удвоение содержимого). Сейчас указатели берутся до realloc и '
                    'используются после — use-after-free. Исправьте.',
       'starter': '#include <stdlib.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'struct vec { int *data; size_t len, cap; };\n'
                  '\n'
                  'static int grow(struct vec *v) {\n'
                  '    if (v->len < v->cap) return 0;\n'
                  '    size_t nc = v->cap ? v->cap * 2 : 2;\n'
                  '    int *t = realloc(v->data, nc * sizeof *t);\n'
                  '    if (!t) return -1;\n'
                  '    v->data = t;\n'
                  '    v->cap = nc;\n'
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  'int *vec_push_get(struct vec *v, int x) {\n'
                  '    int *end = v->data + v->len;\n'
                  '    if (grow(v)) return NULL;\n'
                  '    *end = x;\n'
                  '    v->len++;\n'
                  '    return end;\n'
                  '}\n'
                  '\n'
                  'int vec_first_after_push(struct vec *v, int x) {\n'
                  '    int *first = v->data;\n'
                  '    if (grow(v)) return -1;\n'
                  '    v->data[v->len++] = x;\n'
                  '    return *first;\n'
                  '}\n'
                  '\n'
                  'int vec_extend(struct vec *v, const struct vec *other) {\n'
                  '    const int *src = other->data;\n'
                  '    for (size_t i = 0; i < other->len; i++) {\n'
                  '        if (grow(v)) return -1;\n'
                  '        v->data[v->len++] = src[i];\n'
                  '    }\n'
                  '    return 0;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct vec v = {NULL, 0, 0};\n'
                 '    for (int i = 1; i <= 5; i++) {\n'
                 '        int *p = vec_push_get(&v, i * 10);\n'
                 '        printf("%d@%zu ", *p, (size_t)(p - v.data));\n'
                 '    }\n'
                 '    printf("\\n%zu %zu\\n", v.len, v.cap);\n'
                 '    printf("%d\\n", vec_first_after_push(&v, 99));\n'
                 '    struct vec w = {NULL, 0, 0};\n'
                 '    for (int i = 0; i < 3; i++) vec_push_get(&w, i);\n'
                 '    printf("%d\\n", vec_extend(&w, &w));\n'
                 '    for (size_t i = 0; i < w.len; i++) printf("%d ", w.data[i]);\n'
                 '    printf("\\n");\n'
                 '    printf("%d %zu\\n", vec_extend(&v, &w), v.len);\n'
                 '    free(v.data);\n'
                 '    free(w.data);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Адреса внутри буфера берите после grow(); при v.extend(v) копируйте число элементов и '
               'значение до роста буфера.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['10@0 20@1 30@2 40@3 50@4', '5 8', '10', '0', '0 1 2 0 1 2', '0 12']},
      {'id': 'c11-fix-memcpy-overlap',
       'mode': 'c',
       'title': 'Исправьте: memcpy на пересекающихся областях',
       'statement': 'erase_range(s, from, n) удаляет n символов начиная с from (хвост сдвигается влево, '
                    'строка укорачивается); insert_gap(s, at, n, cap) вставляет n пробелов в позицию at '
                    '(хвост сдвигается вправо; всё должно поместиться в cap, иначе −1, строка не меняется); '
                    'rotate_left(s, k) — циклически сдвигает строку влево на k (k может быть больше длины). '
                    'Используются memcpy на пересекающихся областях — UB (ASan ловит memcpy-param-overlap). '
                    'Исправьте.',
       'starter': '#include <string.h>\n'
                  '#include <stddef.h>\n'
                  '\n'
                  'void erase_range(char *s, size_t from, size_t n) {\n'
                  '    size_t len = strlen(s);\n'
                  '    if (from >= len) return;\n'
                  '    if (n > len - from) n = len - from;\n'
                  '    memcpy(s + from, s + from + n, len - from - n + 1);\n'
                  '}\n'
                  '\n'
                  'int insert_gap(char *s, size_t at, size_t n, size_t cap) {\n'
                  '    size_t len = strlen(s);\n'
                  '    if (at > len || len + n + 1 > cap) return -1;\n'
                  '    memcpy(s + at + n, s + at, len - at + 1);\n'
                  "    memset(s + at, ' ', n);\n"
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  'void rotate_left(char *s, size_t k) {\n'
                  '    size_t len = strlen(s);\n'
                  '    if (len == 0) return;\n'
                  '    k %= len;\n'
                  '    char first[64];\n'
                  '    memcpy(first, s, k);\n'
                  '    memcpy(s, s + k, len - k);\n'
                  '    memcpy(s + len - k, first, k);\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char a[32] = "0123456789";\n'
                 '    erase_range(a, 2, 3);\n'
                 '    printf("[%s]\\n", a);\n'
                 '    erase_range(a, 5, 100);\n'
                 '    printf("[%s]\\n", a);\n'
                 '    erase_range(a, 50, 1);\n'
                 '    erase_range(a, 0, 0);\n'
                 '    printf("[%s]\\n", a);\n'
                 '    char b[16] = "abcdef";\n'
                 '    printf("%d ", insert_gap(b, 2, 3, sizeof b));\n'
                 '    printf("[%s] ", b);\n'
                 '    printf("%d ", insert_gap(b, 9, 1, sizeof b));\n'
                 '    printf("%d ", insert_gap(b, 0, 7, sizeof b));\n'
                 '    printf("%d [%s]\\n", insert_gap(b, 9, 6, sizeof b), b);\n'
                 '    char c[16] = "abcdefgh";\n'
                 '    rotate_left(c, 3);\n'
                 '    printf("[%s] ", c);\n'
                 '    rotate_left(c, 8);\n'
                 '    printf("[%s] ", c);\n'
                 '    rotate_left(c, 11);\n'
                 '    printf("[%s]\\n", c);\n'
                 '    char e[4] = "";\n'
                 '    rotate_left(e, 5);\n'
                 '    printf("[%s]\\n", e);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'memmove — для областей, которые могут пересекаться (сдвиг внутри одного массива); memcpy — '
               'только для непересекающихся.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['[0156789]',
                    '[01567]',
                    '[01567]',
                    '0 [ab   cdef] 0 -1 -1 [ab   cdef ]',
                    '[defghabc] [defghabc] [ghabcdef]',
                    '[]']},
      {'id': 'c11-fix-string-literal',
       'mode': 'c',
       'title': 'Исправьте: изменение строкового литерала',
       'statement': 'make_greeting() возвращает строку «hello, world», которую вызывающий потом изменяет '
                    '(меняет первую букву на заглавную и дописывает «!» заменой точки); title_case(s) '
                    'переводит первые буквы слов в верхний регистр на месте; default_name() → строка по '
                    'умолчанию «anonymous», которую вызывающий может править. Сейчас функции возвращают '
                    'указатели на строковые литералы — запись в них приводит к аварии. Исправьте: '
                    'возвращайте новую копию в куче (освобождает вызывающий).',
       'starter': '#include <ctype.h>\n'
                  '#include <stdlib.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'char *make_greeting(void) {\n'
                  '    return "hello, world.";\n'
                  '}\n'
                  '\n'
                  'char *default_name(void) {\n'
                  '    char *s = "anonymous";\n'
                  '    return s;\n'
                  '}\n'
                  '\n'
                  'void title_case(char *s) {\n'
                  '    int start = 1;\n'
                  '    for (; *s; s++) {\n'
                  '        if (start && isalpha((unsigned char)*s)) *s = (char)toupper((unsigned char)*s);\n'
                  "        start = *s == ' ';\n"
                  '    }\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char *g = make_greeting();\n'
                 "    g[0] = 'H';\n"
                 "    g[strlen(g) - 1] = '!';\n"
                 '    printf("%s\\n", g);\n'
                 '    char *n = default_name();\n'
                 "    n[0] = 'A';\n"
                 '    printf("%s\\n", n);\n'
                 '    char *g2 = make_greeting();\n'
                 '    printf("%s %d\\n", g2, g != g2);\n'
                 '    title_case(g2);\n'
                 '    printf("%s\\n", g2);\n'
                 '    char buf[] = "the quick  brown fox";\n'
                 '    title_case(buf);\n'
                 '    printf("%s\\n", buf);\n'
                 '    free(g); free(n); free(g2);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Строковый литерал нельзя менять. Выделите память malloc(strlen + 1) и скопируйте текст; '
               'вызывающий освободит блок.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['Hello, world!',
                    'Anonymous',
                    'hello, world. 1',
                    'Hello, World.',
                    'The Quick  Brown Fox']},
      {'id': 'c11-fix-promotion',
       'mode': 'c',
       'title': 'Исправьте: целочисленное повышение даёт знаковое переполнение',
       'statement': 'mul16(a, b) → a · b как uint32_t для 16-битных a, b; shl16(a) → a << 16 как uint32_t; '
                    'pack32(a, b, c, d) → (a << 24) | (b << 16) | (c << 8) | d для байтов; sq16(x) → x · x '
                    '(uint32_t); neg8(x) → дополнение (uint8_t)(−x). Операнды меньше int повышаются до '
                    'знакового int, поэтому 65535 · 65535 и 0xFF << 24 переполняют int — неопределённое '
                    'поведение (UBSan останавливает программу). Исправьте, приведя операнды к uint32_t до '
                    'операции.',
       'starter': '#include <stdint.h>\n'
                  '\n'
                  'uint32_t mul16(uint16_t a, uint16_t b) {\n'
                  '    return a * b;\n'
                  '}\n'
                  '\n'
                  'uint32_t shl16(uint16_t a) {\n'
                  '    return a << 16;\n'
                  '}\n'
                  '\n'
                  'uint32_t pack32(uint8_t a, uint8_t b, uint8_t c, uint8_t d) {\n'
                  '    return a << 24 | b << 16 | c << 8 | d;\n'
                  '}\n'
                  '\n'
                  'uint32_t sq16(uint16_t x) {\n'
                  '    return x * x;\n'
                  '}\n'
                  '\n'
                  'uint8_t neg8(uint8_t x) {\n'
                  '    return (uint8_t)-x;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%u %u %u\\n", mul16(65535, 65535), mul16(300, 400), mul16(0, 65535));\n'
                 '    printf("%#x %#x %#x\\n", shl16(0xFFFF), shl16(0x8000), shl16(1));\n'
                 '    printf("%#x %#x %#x\\n", pack32(0xFF, 0xFF, 0xFF, 0xFF), pack32(0x80, 0, 0, 1), '
                 'pack32(1, 2, 3, 4));\n'
                 '    printf("%u %u\\n", sq16(65535), sq16(46341));\n'
                 '    printf("%d %d %d\\n", neg8(1), neg8(0), neg8(128));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': '(uint32_t)a * b: после приведения одного операнда второй тоже станет uint32_t; байты и '
               '16-битные значения до сдвига приводите к uint32_t.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['4294836225 120000 0',
                    '0xffff0000 0x80000000 0x10000',
                    '0xffffffff 0x80000001 0x1020304',
                    '4294836225 2147488281',
                    '255 0 128']},
      {'id': 'c11-fix-vla',
       'mode': 'c',
       'title': 'Исправьте: массив переменной длины с неверной длиной',
       'statement': 'sum_prefix(a, n, k) → сумма первых k элементов; reverse_copy(a, n, out) — копирует '
                    'массив в обратном порядке через временный VLA; max_window(a, n, w) → наибольшая сумма '
                    'окна из w подряд идущих элементов (или −1, если w < 1 или w > n). Сейчас VLA создаётся '
                    'с длиной ≤ 0 или слишком большой (стек!). Исправьте: проверяйте длины, а для '
                    'потенциально больших данных не используйте VLA (malloc).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'long sum_prefix(const int *a, int n, int k) {\n'
                  '    long pref[k];\n'
                  '    long s = 0;\n'
                  '    for (int i = 0; i < k; i++) { s += a[i]; pref[i] = s; }\n'
                  '    return pref[k - 1];\n'
                  '}\n'
                  '\n'
                  'void reverse_copy(const int *a, int n, int *out) {\n'
                  '    int tmp[n];\n'
                  '    for (int i = 0; i < n; i++) tmp[n - 1 - i] = a[i];\n'
                  '    for (int i = 0; i < n; i++) out[i] = tmp[i];\n'
                  '}\n'
                  '\n'
                  'long max_window(const int *a, int n, int w) {\n'
                  '    long sums[n - w + 1];\n'
                  '    long cur = 0;\n'
                  '    for (int i = 0; i < w; i++) cur += a[i];\n'
                  '    sums[0] = cur;\n'
                  '    for (int i = w; i < n; i++) { cur += a[i] - a[i - w]; sums[i - w + 1] = cur; }\n'
                  '    long best = sums[0];\n'
                  '    for (int i = 1; i <= n - w; i++) if (sums[i] > best) best = sums[i];\n'
                  '    return best;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    int a[] = {3, -1, 4, 1, -5, 9, 2, 6};\n'
                 '    printf("%ld %ld %ld %ld\\n", sum_prefix(a, 8, 3), sum_prefix(a, 8, 0), sum_prefix(a, '
                 '8, 20), sum_prefix(a, 8, -4));\n'
                 '    int out[8] = {0};\n'
                 '    reverse_copy(a, 8, out);\n'
                 '    for (int i = 0; i < 8; i++) printf("%d ", out[i]);\n'
                 '    printf("\\n");\n'
                 '    reverse_copy(a, 0, out);\n'
                 '    int n = 600000;\n'
                 '    int *big = malloc((size_t)n * sizeof *big);\n'
                 '    int *res = malloc((size_t)n * sizeof *res);\n'
                 '    for (int i = 0; i < n; i++) big[i] = i % 100;\n'
                 '    reverse_copy(big, n, res);\n'
                 '    printf("%d %d\\n", res[0], res[n - 1]);\n'
                 '    printf("%ld %ld %ld %ld\\n", max_window(a, 8, 3), max_window(a, 8, 1), max_window(a, '
                 '8, 8), max_window(a, 8, 9));\n'
                 '    printf("%ld %ld\\n", max_window(a, 8, 0), max_window(a, 0, 1));\n'
                 '    printf("%ld\\n", max_window(big, n, 1000));\n'
                 '    free(big);\n'
                 '    free(res);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Длина VLA должна быть положительной и небольшой. Для больших n — malloc/free. Окно: '
               'скользящая сумма без массива сумм.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['6 0 19 0', '6 2 9 -5 1 4 -1 3', '99 0', '17 9 19 -1', '-1 -1', '49500']},
      {'id': 'c11-fix-eval-order',
       'mode': 'c',
       'title': 'Исправьте: несколько изменений одной переменной в выражении',
       'statement': 'fill_index(a, n) должна записать a[i] = i для i = 0…n−1; pair_sum(p) → сумма *p (после '
                    'чего *p увеличивается на 1) и ещё *p (после чего *p увеличивается на 1): при *p = 5 → 5 '
                    '+ 6 = 11, итог *p = 7; make_code(counter) → (первое значение счётчика) · 100 + (второе '
                    'значение счётчика), каждый раз увеличивая счётчик: при *counter = 3 → 3 · 100 + 4 = '
                    '304, итог *counter = 5; next_two(it, out) → записывает в out[0] и out[1] два следующих '
                    'значения счётчика it (1-е, затем 2-е). Сейчас в одном выражении переменная меняется '
                    'несколько раз без последовательности — результат не определён. Разбейте выражения на '
                    'отдельные операторы.',
       'starter': 'int fill_index(int *a, int n) {\n'
                  '    int i = 0;\n'
                  '    while (i < n) a[i] = i++;\n'
                  '    return i;\n'
                  '}\n'
                  '\n'
                  'int pair_sum(int *p) {\n'
                  '    return (*p)++ + (*p)++;\n'
                  '}\n'
                  '\n'
                  'int make_code(int *counter) {\n'
                  '    return (*counter)++ * 100 + (*counter)++;\n'
                  '}\n'
                  '\n'
                  'void next_two(int *it, int *out) {\n'
                  '    out[0] = (*it)++, out[1] = (*it)++;\n'
                  '    int i = 0;\n'
                  '    out[i] = i++;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    int a[6] = {9, 9, 9, 9, 9, 9};\n'
                 '    int r = fill_index(a, 6);\n'
                 '    printf("%d:", r);\n'
                 '    for (int i = 0; i < 6; i++) printf(" %d", a[i]);\n'
                 '    printf("\\n");\n'
                 '    int p = 5;\n'
                 '    int s = pair_sum(&p);\n'
                 '    printf("%d %d\\n", s, p);\n'
                 '    int c = 3;\n'
                 '    int code = make_code(&c);\n'
                 '    printf("%d %d\\n", code, c);\n'
                 '    int it = 10, out[2] = {0, 0};\n'
                 '    next_two(&it, out);\n'
                 '    printf("%d %d %d\\n", out[0], out[1], it);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Каждое изменение переменной — отдельным оператором с временной переменной: int first = '
               '(*p)++; int second = (*p)++; return first + second;',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['6: 0 1 2 3 4 5', '11 7', '304 5', '10 11 12']},
      {'id': 'c11-checked-vector',
       'mode': 'c',
       'title': 'Вектор с проверкой границ и обработчиком нарушений',
       'statement': 'struct cvec { int *data; size_t len, cap; void (*on_violation)(const char *what, size_t '
                    'index, size_t len); size_t violations; }. cvec_init(v, handler) (handler может быть '
                    'NULL); cvec_push(v, x) → 0/−1; cvec_get(v, i, *out) → 0, либо −1 при i ≥ len '
                    '(обработчик вызывается с «get», индексом и длиной, violations растёт на 1, *out не '
                    'меняется); cvec_set(v, i, x) — то же с «set»; cvec_remove(v, i) — удаляет элемент со '
                    'сдвигом хвоста, нарушение — «remove»; cvec_pop(v, *out) → 0 или −1 («pop», index = 0). '
                    'cvec_free(v). Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct cvec { int *data; size_t len, cap; void (*on_violation)(const char *what, size_t '
                  'index, size_t len); size_t violations; };\n'
                  '\n'
                  'void cvec_init(struct cvec *v, void (*handler)(const char *, size_t, size_t)) {}\n'
                  'int cvec_push(struct cvec *v, int x) { return -1; }\n'
                  'int cvec_get(struct cvec *v, size_t i, int *out) { return -1; }\n'
                  'int cvec_set(struct cvec *v, size_t i, int x) { return -1; }\n'
                  'int cvec_remove(struct cvec *v, size_t i) { return -1; }\n'
                  'int cvec_pop(struct cvec *v, int *out) { return -1; }\n'
                  'void cvec_free(struct cvec *v) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static char log[8][40];\n'
                 'static int nlog;\n'
                 'static void handler(const char *what, size_t i, size_t len) {\n'
                 '    if (nlog < 8) snprintf(log[nlog++], 40, "%s idx=%zu len=%zu", what, i, len);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct cvec v;\n'
                 '    cvec_init(&v, handler);\n'
                 '    for (int i = 0; i < 5; i++) cvec_push(&v, i * 11);\n'
                 '    int x = -1;\n'
                 '    int g = cvec_get(&v, 2, &x);\n'
                 '    printf("%d %d\\n", g, x);\n'
                 '    x = -1;\n'
                 '    int r1 = cvec_get(&v, 5, &x);\n'
                 '    int r2 = cvec_set(&v, 99, 1);\n'
                 '    int r3 = cvec_remove(&v, 5);\n'
                 '    printf("%d %d %d %d %zu\\n", r1, r2, r3, x, v.violations);\n'
                 '    cvec_remove(&v, 1);\n'
                 '    cvec_set(&v, 0, -5);\n'
                 '    int p;\n'
                 '    while (cvec_pop(&v, &p) == 0) printf("%d ", p);\n'
                 '    printf("\\n%zu %zu\\n", v.len, v.violations);\n'
                 '    for (int i = 0; i < nlog; i++) printf("%s\\n", log[i]);\n'
                 '    struct cvec w;\n'
                 '    cvec_init(&w, NULL);\n'
                 '    printf("%d %zu\\n", cvec_get(&w, 0, &x), w.violations);\n'
                 '    cvec_free(&v);\n'
                 '    cvec_free(&w);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Единая функция violate() увеличивает счётчик, вызывает обработчик (если задан) и возвращает '
               '−1. Проверяйте i >= len до любого обращения к data.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 22',
                    '-1 -1 -1 -1 3',
                    '44 33 22 -5',
                    '0 4',
                    'get idx=5 len=5',
                    'set idx=99 len=5',
                    'remove idx=5 len=5',
                    'pop idx=0 len=0',
                    '-1 1']},
      {'id': 'c11-alloc-tracker',
       'mode': 'c',
       'title': 'Свой «LeakSanitizer»: учёт выделений памяти',
       'statement': 'tmalloc(n), tcalloc(k, size), trealloc(p, n), tfree(p) — обёртки над '
                    'malloc/calloc/realloc/free с учётом блоков (до 64 одновременно живых записей истории). '
                    'tfree → 0 при успехе, −1 — повторное освобождение (блок освобождён ранее), −2 — '
                    'указатель не из этого учёта; tfree(NULL) → 0. t_live_blocks(), t_live_bytes(), '
                    't_total_allocs() (число успешных выделений за всё время, realloc считается как новое '
                    'выделение), t_peak_bytes() — максимум одновременно занятых байт. t_report(buf, cap) → '
                    'строка вида «leak #<номер выделения>: <n> bytes» на каждый живой блок в порядке '
                    'выделения (по строке на блок, с \\n), возвращает длину. t_reset() — освободить все '
                    'живые блоки и обнулить статистику. Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'void *tmalloc(size_t n) { return 0; }\n'
                  'void *tcalloc(size_t k, size_t size) { return 0; }\n'
                  'void *trealloc(void *p, size_t n) { return 0; }\n'
                  'int tfree(void *p) { return -9; }\n'
                  'size_t t_live_blocks(void) { return 99; }\n'
                  'size_t t_live_bytes(void) { return 99; }\n'
                  'size_t t_total_allocs(void) { return 99; }\n'
                  'size_t t_peak_bytes(void) { return 99; }\n'
                  'size_t t_report(char *buf, size_t cap) { return 0; }\n'
                  'void t_reset(void) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char *a = tmalloc(100);\n'
                 '    int *b = tcalloc(10, sizeof *b);\n'
                 '    char *c = tmalloc(5);\n'
                 '    printf("%d %d\\n", b[0] == 0 && b[9] == 0, a != NULL);\n'
                 '    printf("%zu %zu %zu %zu\\n", t_live_blocks(), t_live_bytes(), t_total_allocs(), '
                 't_peak_bytes());\n'
                 '    int f1 = tfree(a);\n'
                 '    int f2 = tfree(a);\n'
                 '    printf("%d %d\\n", f1, f2);\n'
                 '    printf("%d %d\\n", tfree(NULL), tfree(&printf));\n'
                 '    c = trealloc(c, 50);\n'
                 '    strcpy(c, "grown");\n'
                 '    printf("%s %zu %zu %zu\\n", c, t_live_blocks(), t_live_bytes(), t_total_allocs());\n'
                 '    char rep[256];\n'
                 '    size_t n = t_report(rep, sizeof rep);\n'
                 '    printf("%zu\\n%s", n, rep);\n'
                 '    printf("%zu\\n", t_peak_bytes());\n'
                 '    tfree(b);\n'
                 '    tfree(c);\n'
                 '    printf("%zu %zu\\n", t_live_blocks(), t_live_bytes());\n'
                 '    n = t_report(rep, sizeof rep);\n'
                 '    printf("%zu [%s]\\n", n, rep);\n'
                 '    char *d = tmalloc(8);\n'
                 '    (void)d;\n'
                 '    t_reset();\n'
                 '    printf("%zu %zu %zu\\n", t_live_blocks(), t_total_allocs(), t_peak_bytes());\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Журнал структур {ptr, size, id, live}. tfree ищет запись: нет — −2, уже не живая — −1, иначе '
               'освобождает. realloc — выделить новый блок, скопировать, освободить старый и записать как '
               'новое выделение.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 1',
                    '3 145 3 145',
                    '0 -1',
                    '0 -2',
                    'grown 2 90 4',
                    '36',
                    'leak #2: 40 bytes',
                    'leak #4: 50 bytes',
                    '145',
                    '0 0',
                    '0 []',
                    '0 0 0']},
      {'id': 'c11-redzones',
       'mode': 'c',
       'title': 'Свой AddressSanitizer: красные зоны вокруг блоков',
       'statement': 'gmalloc(n) выделяет блок и возвращает указатель на n байт пользователя; перед ними и '
                    'после них — красные зоны по 8 байт, заполненные 0xAB; пользовательская часть '
                    'заполняется 0xCD. gcheck(p) → 0 — зоны целы, 1 — испорчена передняя, 2 — задняя, 3 — '
                    'обе. gfree(p) → то же, что gcheck, и освобождает блок; gsize(p) → n; gfree(NULL) → 0. '
                    'После освобождения доступ не проверяется. Под AddressSanitizer (сам ваш код не должен '
                    'выходить за границы).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'void *gmalloc(size_t n) { return 0; }\n'
                  'int gcheck(const void *p) { return -1; }\n'
                  'int gfree(void *p) { return -1; }\n'
                  'size_t gsize(const void *p) { return 99; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    unsigned char *a = gmalloc(16);\n'
                 '    printf("%zu %d %d %d\\n", gsize(a), gcheck(a), a[0], a[15]);\n'
                 '    a[16] = 1;\n'
                 '    printf("%d\\n", gcheck(a));\n'
                 '    a[16] = 0xAB;\n'
                 '    a[-1] = 7;\n'
                 '    printf("%d\\n", gcheck(a));\n'
                 '    a[16] = 9;\n'
                 '    printf("%d\\n", gcheck(a));\n'
                 '    printf("%d\\n", gfree(a));\n'
                 '    unsigned char *b = gmalloc(0);\n'
                 '    printf("%zu %d\\n", gsize(b), gcheck(b));\n'
                 '    b[-3] = 0;\n'
                 '    b[2] = 1;\n'
                 '    printf("%d\\n", gfree(b));\n'
                 '    unsigned char *c = gmalloc(100);\n'
                 '    memset(c, 1, 100);\n'
                 '    int g1 = gcheck(c);\n'
                 '    int g2 = gfree(c);\n'
                 '    printf("%d %d\\n", g1, g2);\n'
                 '    printf("%d\\n", gfree(NULL));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Выделите raw = malloc(заголовок + 8 + n + 8) и разметьте: размер, зона, данные, зона. Размер '
               'читайте memcpy из-под указателя пользователя минус зона.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['16 0 205 205', '2', '1', '3', '3', '0 0', '3', '0 0', '0']},
      {'id': 'c11-poison-pool',
       'mode': 'c',
       'title': 'Пул с отравлением освобождённых блоков',
       'statement': 'Пул из 8 блоков по 32 байта в статическом массиве. pool_alloc() → указатель на блок '
                    '(все 32 байта обнулены) или NULL, если пул пуст; pool_free(p) → 0 при успехе, −1 — блок '
                    'уже свободен (двойное освобождение), −2 — указатель не из пула (в том числе не на '
                    'границе блока); освобождённый блок заполняется 0xDD. pool_is_poisoned(p) → 1, если все '
                    '32 байта блока равны 0xDD и блок свободен. pool_live() — число занятых блоков; '
                    'pool_index(p) → номер блока 0…7 или −1. Блоки выдаются в порядке возрастания номеров '
                    '(первый свободный).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'void *pool_alloc(void) { return 0; }\n'
                  'int pool_free(void *p) { return -9; }\n'
                  'int pool_is_poisoned(const void *p) { return -1; }\n'
                  'int pool_live(void) { return -1; }\n'
                  'int pool_index(const void *p) { return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    void *p[9];\n'
                 '    for (int i = 0; i < 9; i++) p[i] = pool_alloc();\n'
                 '    printf("%d %d\\n", pool_live(), p[8] == NULL);\n'
                 '    printf("%d %d %d\\n", pool_index(p[0]), pool_index(p[7]), pool_index(p[0] + 5));\n'
                 '    unsigned char *q = p[3];\n'
                 '    memset(q, 0x11, 32);\n'
                 '    int pf1 = pool_free(p[3]);\n'
                 '    int pf2 = pool_free(p[3]);\n'
                 '    printf("%d %d\\n", pf1, pf2);\n'
                 '    printf("%d %d %d\\n", pool_is_poisoned(p[3]), pool_is_poisoned(p[4]), pool_live());\n'
                 '    int x;\n'
                 '    printf("%d %d\\n", pool_free(&x), pool_free((char *)p[4] + 1));\n'
                 '    printf("%d\\n", pool_free(NULL));\n'
                 '    void *again = pool_alloc();\n'
                 '    printf("%d %d %d\\n", again == p[3], pool_is_poisoned(again), ((unsigned char '
                 '*)again)[31]);\n'
                 '    pool_free(p[0]);\n'
                 '    pool_free(p[1]);\n'
                 '    void *z = pool_alloc();\n'
                 '    printf("%d %d\\n", z == p[0], pool_live());\n'
                 '    q = p[5];\n'
                 '    q[0] = 1;\n'
                 '    pool_free(q);\n'
                 '    printf("%d %d\\n", q[0], q[31]);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Состояние занятости — массив флагов; номер блока = (адрес − начало) / 32 и только при точном '
               'совпадении границы. При free — memset(…, 0xDD, 32).',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['8 1', '0 7 -1', '0 -1', '1 0 7', '-2 -2', '-2', '1 0 0', '1 7', '221 221']},
      {'id': 'c11-assert-lib',
       'mode': 'c',
       'title': 'Библиотека проверок: ASSERT, REQUIRE, UNREACHABLE',
       'statement': 'Напишите счётчики и макросы без остановки программы: ASSERT(cond) — при нарушении '
                    'увеличивает chk_failed и сохраняет текст условия в chk_last (буфер 64 байта, обрезка); '
                    'REQUIRE(cond, retval) — при нарушении делает то же и возвращает retval из функции; '
                    'ASSERT_EQ(a, b) — проверка равенства (значения long long), в chk_last — «a == b (X != '
                    'Y)»; IN_RANGE_ASSERT(x, lo, hi) — проверка lo ≤ x ≤ hi; UNREACHABLE() — увеличивает '
                    'chk_unreachable и сохраняет «unreachable»; chk_reset() сбрасывает всё; chk_passed '
                    'считает успешные проверки. Каждое выражение вычисляется один раз.',
       'starter': '#include <stdio.h>\n'
                  '\n'
                  'int chk_failed, chk_passed, chk_unreachable;\n'
                  'char chk_last[64];\n'
                  '\n'
                  'void chk_reset(void) {}\n'
                  '\n'
                  '#define ASSERT(cond)\n'
                  '#define REQUIRE(cond, retval)\n'
                  '#define ASSERT_EQ(a, b)\n'
                  '#define IN_RANGE_ASSERT(x, lo, hi)\n'
                  '#define UNREACHABLE()\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static int calls;\n'
                 'static int tick(void) { return ++calls; }\n'
                 '\n'
                 'static int safe_div(int a, int b) {\n'
                 '    REQUIRE(b != 0, -1);\n'
                 '    return a / b;\n'
                 '}\n'
                 '\n'
                 'static const char *name(int k) {\n'
                 '    switch (k) {\n'
                 '    case 0: return "zero";\n'
                 '    case 1: return "one";\n'
                 '    default: UNREACHABLE(); return "?";\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    ASSERT(1 + 1 == 2);\n'
                 '    ASSERT(2 * 2 == 5);\n'
                 '    printf("%d %d [%s]\\n", chk_passed, chk_failed, chk_last);\n'
                 '    ASSERT_EQ(tick(), 1);\n'
                 '    ASSERT_EQ(tick(), 5);\n'
                 '    printf("%d %d %d [%s]\\n", chk_passed, chk_failed, calls, chk_last);\n'
                 '    IN_RANGE_ASSERT(5, 1, 10);\n'
                 '    IN_RANGE_ASSERT(11 + calls, 1, 10);\n'
                 '    printf("%d %d [%s]\\n", chk_passed, chk_failed, chk_last);\n'
                 '    printf("%d %d\\n", safe_div(10, 2), safe_div(1, 0));\n'
                 '    printf("%d %d [%s]\\n", chk_passed, chk_failed, chk_last);\n'
                 '    const char *n0 = name(0), *n1 = name(1), *n7 = name(7);\n'
                 '    printf("%s %s %s %d\\n", n0, n1, n7, chk_unreachable);\n'
                 '    printf("[%s]\\n", chk_last);\n'
                 '    chk_reset();\n'
                 '    printf("%d %d %d [%s]\\n", chk_passed, chk_failed, chk_unreachable, chk_last);\n'
                 '    if (chk_failed == 0) ASSERT(0); else ASSERT(1);\n'
                 '    printf("%d %d\\n", chk_passed, chk_failed);\n'
                 '    ASSERT(strlen("a very long condition text that exceeds the sixty-four byte limit of '
                 'the buffer") > 1000);\n'
                 '    printf("%zu\\n", strlen(chk_last));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Каждый макрос — do { … } while (0). В ASSERT_EQ и IN_RANGE_ASSERT сохраняйте значения во '
               'временные long long: аргумент вычисляется один раз.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 1 [2 * 2 == 5]',
                    '2 2 2 [tick() == 5 (2 != 5)]',
                    '3 3 [11 + calls in [1, 10] (got 13)]',
                    '5 -1',
                    '4 4 [b != 0]',
                    'zero one ? 1',
                    '[unreachable]',
                    '0 0 0 []',
                    '0 1',
                    '63']},
      {'id': 'c11-canary-model',
       'mode': 'c',
       'title': 'Модель защиты стека: канарейка',
       'statement': 'Кадр моделируется массивом uint8_t frame[32]: буфер — байты 0…15, канарейка — байты '
                    '16…19 (little-endian uint32), «сохранённый адрес возврата» — байты 20…27, остальное '
                    '(28…31) — прочие данные. frame_init(frame, canary, ret) заполняет кадр: буфер нулями, '
                    'канарейку и адрес возврата (uint64) в little-endian, остальное 0xEE. frame_write(frame, '
                    'off, data, n) → записывает данные с позиции off без проверки внутри кадра (как '
                    'небезопасный strcpy), но не выходит за 32 байта (лишнее отбрасывается), возвращает '
                    'число записанных байт. frame_check(frame, canary) → 0 — всё цело; 1 — испорчена '
                    'канарейка; 2 — канарейка цела, но испорчен адрес возврата; 3 — испорчены оба. '
                    'frame_safe_write(frame, data, n) → записывает не больше 16 байт в буфер, возвращает '
                    'число записанных.',
       'starter': '#include <stddef.h>\n'
                  '#include <stdint.h>\n'
                  '\n'
                  'void frame_init(uint8_t *frame, uint32_t canary, uint64_t ret) {}\n'
                  'size_t frame_write(uint8_t *frame, size_t off, const void *data, size_t n) { return 0; }\n'
                  'int frame_check(const uint8_t *frame, uint32_t canary, uint64_t ret) { return -1; }\n'
                  'size_t frame_safe_write(uint8_t *frame, const void *data, size_t n) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    uint8_t f[32];\n'
                 '    frame_init(f, 0xDEADC0DE, 0x00007FFF12345678ULL);\n'
                 '    for (int i = 0; i < 32; i++) printf("%02x", f[i]);\n'
                 '    printf("\\n%d\\n", frame_check(f, 0xDEADC0DE, 0x00007FFF12345678ULL));\n'
                 '    size_t w = frame_write(f, 0, "0123456789abcdef", 16);\n'
                 '    int ck = frame_check(f, 0xDEADC0DE, 0x00007FFF12345678ULL);\n'
                 '    printf("%zu %d\\n", w, ck);\n'
                 '    w = frame_write(f, 14, "XYZ", 3);\n'
                 '    ck = frame_check(f, 0xDEADC0DE, 0x00007FFF12345678ULL);\n'
                 '    printf("%zu %d\\n", w, ck);\n'
                 '    frame_init(f, 0xDEADC0DE, 0x00007FFF12345678ULL);\n'
                 '    w = frame_write(f, 20, "RRRR", 4);\n'
                 '    ck = frame_check(f, 0xDEADC0DE, 0x00007FFF12345678ULL);\n'
                 '    printf("%zu %d\\n", w, ck);\n'
                 '    frame_init(f, 0xDEADC0DE, 0x00007FFF12345678ULL);\n'
                 '    w = frame_write(f, 0, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", 44);\n'
                 '    ck = frame_check(f, 0xDEADC0DE, 0x00007FFF12345678ULL);\n'
                 '    printf("%zu %d\\n", w, ck);\n'
                 '    size_t w1 = frame_write(f, 40, "x", 1);\n'
                 '    size_t w2 = frame_write(f, 31, "xyz", 3);\n'
                 '    printf("%zu %zu\\n", w1, w2);\n'
                 '    frame_init(f, 0x11223344, 7);\n'
                 '    w = frame_safe_write(f, "this is a long overflowing input string", 40);\n'
                 '    ck = frame_check(f, 0x11223344, 7);\n'
                 '    printf("%zu %d\\n", w, ck);\n'
                 '    printf("%.16s %02x\\n", f, f[16]);\n'
                 '    printf("%zu\\n", frame_safe_write(f, "ab", 2));\n'
                 '    printf("%d %d\\n", frame_check(f, 0x11223345, 7), frame_check(f, 0x11223344, 8));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Канарейка — 4 байта little-endian по смещению 16; адрес возврата — 8 байт по смещению 20. '
               'frame_write — memcpy с ограничением по границе 32.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['00000000000000000000000000000000dec0adde78563412ff7f0000eeeeeeee',
                    '0',
                    '16 0',
                    '3 1',
                    '4 2',
                    '32 3',
                    '0 1',
                    '16 0',
                    'this is a long o 44',
                    '2',
                    '1 2']},
      {'id': 'c11-ddmin',
       'mode': 'c',
       'title': 'Минимизация ошибочного входа (delta debugging)',
       'statement': 'minimize(buf, n, fails) → новая длина: в buf остаётся наименьшая подпоследовательность '
                    'исходных байтов, на которой fails(buf, len) по-прежнему возвращает ненулевое значение '
                    '(изначально fails(buf, n) ≠ 0). Алгоритм: пока что-то удаётся — для размера куска от '
                    'n/2 вниз до 1 пробуйте удалять по одному куску (слева направо) и оставляйте удаление, '
                    'если ошибка сохраняется. Результат должен быть 1-минимальным: удаление любого одного '
                    'байта делает ошибку невоспроизводимой. calls_made() → сколько раз за всё время '
                    'вызывалась fails (счётчик ведёт сама minimize); reset_calls().',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'size_t minimize(char *buf, size_t n, int (*fails)(const char *, size_t)) { return n; }\n'
                  'size_t calls_made(void) { return 0; }\n'
                  'void reset_calls(void) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static int has_both(const char *s, size_t n) {\n'
                 '    int a = 0, z = 0;\n'
                 "    for (size_t i = 0; i < n; i++) { a |= s[i] == 'a'; z |= s[i] == 'z'; }\n"
                 '    return a && z;\n'
                 '}\n'
                 'static int has_substr(const char *s, size_t n) {\n'
                 '    for (size_t i = 0; i + 3 <= n; i++) if (memcmp(s + i, "BUG", 3) == 0) return 1;\n'
                 '    return 0;\n'
                 '}\n'
                 'static int too_many_x(const char *s, size_t n) {\n'
                 '    int c = 0;\n'
                 "    for (size_t i = 0; i < n; i++) c += s[i] == 'x';\n"
                 '    return c >= 3;\n'
                 '}\n'
                 'static int starts_ends(const char *s, size_t n) {\n'
                 "    return n >= 2 && s[0] == '<' && s[n - 1] == '>';\n"
                 '}\n'
                 '\n'
                 'static void run(const char *label, const char *in, int (*f)(const char *, size_t)) {\n'
                 '    char buf[256];\n'
                 '    size_t n = strlen(in);\n'
                 '    memcpy(buf, in, n);\n'
                 '    reset_calls();\n'
                 '    size_t m = minimize(buf, n, f);\n'
                 '    printf("%s: %zu [%.*s] fails=%d\\n", label, m, (int)m, buf, f(buf, m) != 0);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    run("both", "qqqqaqqqqqqqzqqqqq", has_both);\n'
                 '    run("both2", "zaz", has_both);\n'
                 '    run("substr", "hello world BUG in the middle of text", has_substr);\n'
                 '    run("substr-min", "BUG", has_substr);\n'
                 '    run("x3", "axbxcxdxe", too_many_x);\n'
                 '    run("ends", "<abc def ghi>", starts_ends);\n'
                 '    char buf[256];\n'
                 '    memcpy(buf, "azzzzzzzzzzzzzzzzzzzzzzzzzzzzzz", 31);\n'
                 '    reset_calls();\n'
                 '    minimize(buf, 31, has_both);\n'
                 '    printf("%d\\n", calls_made() < 200);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Для каждого размера куска пробуйте удалять куски слева направо; при успешном удалении не '
               'двигайте start (на его место встал следующий кусок). Повторяйте проходы, пока что-то '
               'удаляется.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['both: 2 [az] fails=1',
                    'both2: 2 [az] fails=1',
                    'substr: 3 [BUG] fails=1',
                    'substr-min: 3 [BUG] fails=1',
                    'x3: 3 [xxx] fails=1',
                    'ends: 2 [<>] fails=1',
                    '1']},
      {'id': 'c11-bisect',
       'mode': 'c',
       'title': 'Двоичный поиск первой плохой версии',
       'statement': 'first_bad(lo, hi, is_bad, *tests) → наименьшая версия v из [lo, hi], для которой '
                    'is_bad(v) ≠ 0, при условии, что версии «хорошие, … хорошие, плохие, … плохие» '
                    '(монотонно); если is_bad(hi) == 0 — результат −1. *tests — число вызовов is_bad; их '
                    'должно быть не больше ⌈log₂(hi − lo + 1)⌉ + 1. Версии — int в любом диапазоне (в том '
                    'числе близком к INT_MAX); is_bad вызывается только для версий из [lo, hi]. '
                    'culprit(commits, n, is_bad_commit) — то же по массиву коммитов (имена) и функции, '
                    'принимающей имя: → индекс первого плохого или −1.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int first_bad(int lo, int hi, int (*is_bad)(int), int *tests) {\n'
                  '    *tests = 0;\n'
                  '    return -2;\n'
                  '}\n'
                  'int culprit(const char *const *commits, int n, int (*is_bad_commit)(const char *)) { '
                  'return -2; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static int first;\n'
                 'static int bad_from(int v) { return v >= first; }\n'
                 'static int calls_seen[64], ncs;\n'
                 'static int bad_logged(int v) { if (ncs < 64) calls_seen[ncs++] = v; return v >= first; }\n'
                 '\n'
                 'static const char *names[] = {"c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", '
                 '"c9"};\n'
                 'static const char *badfrom_name;\n'
                 'static int bad_commit(const char *c) {\n'
                 '    for (int i = 0; i < 10; i++) {\n'
                 '        if (names[i] == c) return i >= 6;\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    int tests;\n'
                 '    first = 37;\n'
                 '    printf("%d ", first_bad(1, 100, bad_from, &tests));\n'
                 '    printf("%d\\n", tests <= 8);\n'
                 '    first = 1;\n'
                 '    printf("%d ", first_bad(1, 100, bad_from, &tests));\n'
                 '    printf("%d\\n", tests <= 8);\n'
                 '    first = 100;\n'
                 '    printf("%d ", first_bad(1, 100, bad_from, &tests));\n'
                 '    printf("%d\\n", tests <= 8);\n'
                 '    first = 101;\n'
                 '    int fb = first_bad(1, 100, bad_from, &tests);\n'
                 '    printf("%d %d\\n", fb, tests);\n'
                 '    first = 5;\n'
                 '    fb = first_bad(5, 5, bad_from, &tests);\n'
                 '    printf("%d %d\\n", fb, tests);\n'
                 '    first = INT_MAX - 3;\n'
                 '    printf("%d %d\\n", first_bad(0, INT_MAX, bad_from, &tests), tests <= 33);\n'
                 '    first = INT_MIN + 10;\n'
                 '    printf("%d %d\\n", first_bad(INT_MIN, INT_MAX, bad_from, &tests), tests <= 34);\n'
                 '    first = 50;\n'
                 '    ncs = 0;\n'
                 '    first_bad(10, 90, bad_logged, &tests);\n'
                 '    int inside = 1;\n'
                 '    for (int i = 0; i < ncs; i++) if (calls_seen[i] < 10 || calls_seen[i] > 90) inside = '
                 '0;\n'
                 '    printf("%d %d\\n", inside, tests == ncs);\n'
                 '    printf("%d %d\\n", culprit(names, 10, bad_commit), culprit(names, 5, bad_commit));\n'
                 '    printf("%d\\n", culprit(names, 0, bad_commit));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'mid = lo + (hi − lo) / 2 (в long long, чтобы не переполнить). Сначала проверьте hi: если он '
               '«хороший» — плохих нет.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['37 1',
                    '1 1',
                    '100 1',
                    '-1 1',
                    '5 1',
                    '2147483644 1',
                    '-2147483638 1',
                    '1 1',
                    '6 -1',
                    '-1']},
      {'id': 'c11-hexdiff',
       'mode': 'c',
       'title': 'Сравнение буферов: первое отличие и отчёт',
       'statement': 'first_diff(a, b, n) → смещение первого различающегося байта или −1. diff_count(a, b, n) '
                    '→ число различающихся байтов. diff_report(a, b, n, out, cap) → записывает отчёт: для '
                    "каждого различия (не более 5) строка «@<смещение>: 0x<A> '<c>' != 0x<B> '<c>'» (байты "
                    'двумя шестнадцатеричными цифрами строчными, символ — сам, если ASCII 32…126, иначе «.»; '
                    'смещение десятичное), затем итоговую строку «N differences» (или «identical» при '
                    'совпадении; если различий больше пяти — строка «… and K more» перед итогом). Все строки '
                    'оканчиваются \\n. Возвращает длину отчёта или −1, если не помещается.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'long first_diff(const void *a, const void *b, size_t n) { return -2; }\n'
                  'size_t diff_count(const void *a, const void *b, size_t n) { return 99; }\n'
                  'int diff_report(const void *a, const void *b, size_t n, char *out, size_t cap) { return '
                  '-9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    const char *a = "hello, world";\n'
                 '    const char *b = "hellO, w0rld";\n'
                 '    printf("%ld %zu %ld %zu\\n", first_diff(a, b, 12), diff_count(a, b, 12), first_diff(a, '
                 'a, 12), diff_count(a, a, 12));\n'
                 '    printf("%ld %zu\\n", first_diff(a, b, 4), diff_count(a, b, 0));\n'
                 '    char out[512];\n'
                 '    int n = diff_report(a, b, 12, out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    n = diff_report(a, a, 12, out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    unsigned char x[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, y[10] = {1, 1, 3, 3, 5, 5, 7, 7, '
                 '9, 200};\n'
                 '    n = diff_report(x, y, 10, out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    printf("%d %d\\n", diff_report(x, y, 10, out, 20), diff_report(a, a, 12, out, 10));\n'
                 '    printf("%d\\n", diff_report(a, a, 12, out, 11));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Порядок отчёта: до пяти строк различий, затем (если больше пяти) «… and K more», затем итог. '
               'Размер результата проверяйте перед каждой записью.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['4 2 -1 0',
                    '-1 0',
                    '64',
                    "@4: 0x6f 'o' != 0x4f 'O'",
                    "@8: 0x6f 'o' != 0x30 '0'",
                    '2 differences',
                    '10',
                    'identical',
                    '154',
                    "@0: 0x00 '.' != 0x01 '.'",
                    "@2: 0x02 '.' != 0x03 '.'",
                    "@4: 0x04 '.' != 0x05 '.'",
                    "@6: 0x06 '.' != 0x07 '.'",
                    "@8: 0x08 '.' != 0x09 '.'",
                    '... and 1 more',
                    '6 differences',
                    '-1 -1',
                    '10']},
      {'id': 'c11-trace-ring',
       'mode': 'c',
       'title': '«Чёрный ящик»: кольцевой журнал событий',
       'statement': 'Кольцо на 8 записей по 31 символу. trace(fmt, …) добавляет запись '
                    '(printf-форматирование, обрезка до 31 символа) с монотонным номером 1, 2, 3…; при '
                    'заполнении перезаписывается самая старая. trace_count() → число записей в кольце (≤ 8), '
                    'trace_total() → сколько записей добавлено всего, trace_dump(out, cap) → строки '
                    '«#<номер> <текст>\\n» от старой к новой (длина результата или −1 при нехватке места; '
                    'при cap = 0 → −1), trace_last(k, out) → k-я с конца запись (0 — последняя) → 1 и текст '
                    'в out (≥ 32 байт), либо 0, если такой нет. trace_clear() — очистить кольцо (счётчик '
                    'номеров не сбрасывается).',
       'starter': '#include <stdarg.h>\n'
                  '#include <stddef.h>\n'
                  '\n'
                  'void trace(const char *fmt, ...) {}\n'
                  'size_t trace_count(void) { return 99; }\n'
                  'unsigned trace_total(void) { return 99; }\n'
                  'int trace_dump(char *out, size_t cap) { return -9; }\n'
                  'int trace_last(int k, char *out) { return -9; }\n'
                  'void trace_clear(void) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char out[512], one[32];\n'
                 '    trace("start");\n'
                 '    trace("open %s fd=%d", "/tmp/x", 3);\n'
                 '    printf("%zu %u\\n", trace_count(), trace_total());\n'
                 '    int n = trace_dump(out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    for (int i = 0; i < 10; i++) trace("event %d", i);\n'
                 '    printf("%zu %u\\n", trace_count(), trace_total());\n'
                 '    n = trace_dump(out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    printf("%d [%s] ", trace_last(0, one), one);\n'
                 '    printf("%d [%s] ", trace_last(7, one), one);\n'
                 '    printf("%d %d\\n", trace_last(8, one), trace_last(-1, one));\n'
                 '    trace("a very long message that does not fit into thirty-one characters");\n'
                 '    trace_last(0, one);\n'
                 '    printf("%zu %s\\n", strlen(one), one);\n'
                 '    printf("%d %d\\n", trace_dump(out, 10), trace_dump(out, 0));\n'
                 '    trace_clear();\n'
                 '    printf("%zu %u %d %d\\n", trace_count(), trace_total(), trace_last(0, one), '
                 'trace_dump(out, sizeof out));\n'
                 '    trace("after");\n'
                 '    n = trace_dump(out, sizeof out);\n'
                 '    printf("%d %s", n, out);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Номер записи k хранится в ячейке (k − 1) % 8; при дампе идите от самой старой из оставшихся '
               '(total − count + 1) к последней.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['2 2',
                    '29',
                    '#1 start',
                    '#2 open /tmp/x fd=3',
                    '8 12',
                    '91',
                    '#5 event 2',
                    '#6 event 3',
                    '#7 event 4',
                    '#8 event 5',
                    '#9 event 6',
                    '#10 event 7',
                    '#11 event 8',
                    '#12 event 9',
                    '1 [event 9] 1 [event 2] 0 0',
                    '31 a very long message that does n',
                    '-1 -1',
                    '0 13 0 0',
                    '10 #14 after']}]}
