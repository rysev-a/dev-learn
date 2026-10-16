"""Задачи книги «От assembler к языку C»: глава 14 (код компилируется gcc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {14: [{'id': 'c14-designated-init',
       'mode': 'c',
       'title': 'Назначенные инициализаторы и таблицы с пропусками',
       'statement': 'struct config { int width, height; const char *title; bool fullscreen; double scale; }. '
                    'default_config() → конфигурация: width 800, height 600, title «untitled», fullscreen '
                    'false, scale 1.0 (одним назначенным инициализатором, без присваиваний полей); '
                    'with_size(c, w, h) → копия c с новыми width и height (составной литерал не нужен — но '
                    'поля не названные в инициализаторе должны браться из c); level_name(n) → «TRACE», '
                    '«DEBUG», «INFO», «WARN», «ERROR» для 0…4 по таблице static const char *const names[] с '
                    'назначенными индексами (индексы 5 и 6 в таблице — «FATAL» и «PANIC» тоже должны '
                    'работать), для других n → «?»; days(m, leap) → число дней по таблице с назначенными '
                    'индексами [1] … [12]; нулевой индекс таблицы — 0.',
       'starter': '#include <stdbool.h>\n'
                  '\n'
                  'struct config { int width, height; const char *title; bool fullscreen; double scale; };\n'
                  '\n'
                  'struct config default_config(void) { struct config c = {0}; return c; }\n'
                  'struct config with_size(struct config c, int w, int h) { return c; }\n'
                  'const char *level_name(int n) { return "?"; }\n'
                  'int days(int m, bool leap) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
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
                 '    struct config c = default_config();\n'
                 '    printf("%d %d %s %d %.1f\\n", c.width, c.height, c.title, c.fullscreen, c.scale);\n'
                 '    c.fullscreen = true;\n'
                 '    c.scale = 2.5;\n'
                 '    struct config d = with_size(c, 1920, 1080);\n'
                 '    printf("%d %d %s %d %.1f\\n", d.width, d.height, d.title, d.fullscreen, d.scale);\n'
                 '    for (int i = -1; i <= 7; i++) printf("%s ", level_name(i));\n'
                 '    printf("\\n");\n'
                 '    for (int m = 0; m <= 13; m++) printf("%d ", days(m, false));\n'
                 '    printf("\\n%d %d %d\\n", days(2, true), days(2, false), days(12, true));\n'
                 '    printf("designated: %d\\n", src_count(".wi" "dth") >= 1);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'return (struct config){ .width = 800, … }; для таблицы: static const char *const names[] = { '
               '[0] = "TRACE", … }. Поля, которые не назвали, обнуляются.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['800 600 untitled 0 1.0',
                    '1920 1080 untitled 1 2.5',
                    '? TRACE DEBUG INFO WARN ERROR FATAL PANIC ?',
                    '0 31 28 31 30 31 30 31 31 30 31 30 31 0',
                    '29 28 31',
                    'designated: 1']},
      {'id': 'c14-compound-literals',
       'mode': 'c',
       'title': 'Составные литералы: временные значения в выражениях',
       'statement': 'struct pt { int x, y; }; struct rect { struct pt min, max; }. midpoint(a, b) → середина '
                    '(целое деление к нулю); rect_area(r) (r — по значению); rect_contains(r, p) → p внутри '
                    '(границы включены); rect_union(a, b) → наименьший прямоугольник, содержащий оба; '
                    'sum_ints(const int *a, size_t n); max_ints(const int *a, size_t n). Затем определите '
                    'макросы: PT(x, y) → составной литерал struct pt; RECT(x0, y0, x1, y1) → struct rect; '
                    'INTS(…) → составной литерал массива int из перечисленных значений (чтобы можно было '
                    'писать sum_ints(INTS(1, 2, 3), 3)); COUNT_INTS(...) → число значений в INTS (до 8; '
                    'через sizeof).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct pt { int x, y; };\n'
                  'struct rect { struct pt min, max; };\n'
                  '\n'
                  'struct pt midpoint(struct pt a, struct pt b) { return a; }\n'
                  'long rect_area(struct rect r) { return 0; }\n'
                  'int rect_contains(struct rect r, struct pt p) { return -1; }\n'
                  'struct rect rect_union(struct rect a, struct rect b) { return a; }\n'
                  'long sum_ints(const int *a, size_t n) { return 0; }\n'
                  'int max_ints(const int *a, size_t n) { return 0; }\n'
                  '\n'
                  '#define PT(x, y) ((struct pt){0, 0})\n'
                  '#define RECT(x0, y0, x1, y1) ((struct rect){{0, 0}, {0, 0}})\n'
                  '#define INTS(...) ((const int[]){0})\n'
                  '#define COUNT_INTS(...) 0\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct pt m = midpoint(PT(0, 0), PT(10, -7));\n'
                 '    printf("%d %d\\n", m.x, m.y);\n'
                 '    struct rect r = RECT(0, 0, 4, 3);\n'
                 '    printf("%ld %d %d %d\\n", rect_area(r), rect_contains(r, PT(4, 3)), rect_contains(r, '
                 'PT(5, 3)), rect_contains(r, PT(-1, 0)));\n'
                 '    struct rect u = rect_union(r, RECT(-2, 1, 3, 9));\n'
                 '    printf("%d %d %d %d %ld\\n", u.min.x, u.min.y, u.max.x, u.max.y, rect_area(u));\n'
                 '    printf("%ld %d\\n", sum_ints(INTS(1, 2, 3, 4), COUNT_INTS(1, 2, 3, 4)), '
                 'max_ints(INTS(5, -1, 9, 2), 4));\n'
                 '    printf("%zu %zu\\n", COUNT_INTS(7), COUNT_INTS(1, 2, 3, 4, 5, 6, 7, 8));\n'
                 '    printf("%ld\\n", sum_ints(INTS(10, 20), 2) + rect_area(RECT(1, 1, 3, 3)));\n'
                 '    int x = 5;\n'
                 '    struct pt p = PT(x + 1, x * 2);\n'
                 '    printf("%d %d\\n", p.x, p.y);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Составной литерал: ((struct pt){ (x), (y) }); массив: ((const int[]){ __VA_ARGS__ }); число '
               'элементов — sizeof(литерал) / sizeof(int).',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['5 -3', '12 1 0 0', '-2 0 4 9 54', '10 9', '1 8', '34', '6 10']},
      {'id': 'c14-flexible-str',
       'mode': 'c',
       'title': 'Строка с длиной на гибком члене массива',
       'statement': 'struct str { size_t len; char data[]; } — длина и символы одним блоком (data всегда '
                    'оканчивается нулём, но len его не включает). str_new(s) → новая строка (копия s); '
                    'str_from(buf, n) — из n байтов (в том числе с нулями внутри); str_cat(a, b) → новая '
                    'строка a + b; str_slice(s, from, n) → подстрока (обрезается по границам; from > len → '
                    'пустая); str_eq(a, b) → 1/0 (сравнение по len и содержимому); str_find(s, ch) → индекс '
                    'первого вхождения или −1; str_free(s); str_size(s) → число байтов блока (sizeof(struct '
                    'str) + len + 1). Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct str { size_t len; char data[]; };\n'
                  '\n'
                  'struct str *str_new(const char *s) { return 0; }\n'
                  'struct str *str_from(const char *buf, size_t n) { return 0; }\n'
                  'struct str *str_cat(const struct str *a, const struct str *b) { return 0; }\n'
                  'struct str *str_slice(const struct str *s, size_t from, size_t n) { return 0; }\n'
                  'int str_eq(const struct str *a, const struct str *b) { return -1; }\n'
                  'long str_find(const struct str *s, char ch) { return -2; }\n'
                  'void str_free(struct str *s) {}\n'
                  'size_t str_size(const struct str *s) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct str *a = str_new("hello"), *b = str_new(", world");\n'
                 '    struct str *c = str_cat(a, b);\n'
                 '    printf("%zu [%s] %zu\\n", c->len, c->data, str_size(c));\n'
                 '    struct str *s1 = str_slice(c, 7, 5), *s2 = str_slice(c, 3, 100), *s3 = str_slice(c, '
                 '50, 2), *s4 = str_slice(c, 0, 0);\n'
                 '    printf("[%s] [%s] [%s] [%s] %zu\\n", s1->data, s2->data, s3->data, s4->data, '
                 's3->len);\n'
                 '    struct str *z = str_from("a\\0b\\0c", 5);\n'
                 '    printf("%zu %d %d %d %d\\n", z->len, z->data[1], z->data[2], z->data[5], str_eq(z, '
                 'z));\n'
                 '    struct str *e1 = str_new(""), *e2 = str_from("x", 0);\n'
                 '    struct str *first5 = str_slice(c, 0, 5);\n'
                 '    printf("%d %d %d\\n", str_eq(e1, e2), str_eq(a, b), str_eq(a, first5));\n'
                 '    str_free(first5);\n'
                 '    printf("%ld %ld %ld %ld\\n", str_find(c, \'o\'), str_find(c, \'w\'), str_find(c, '
                 "'z'), str_find(z, 'c'));\n"
                 '    printf("%zu %zu\\n", str_size(e1), sizeof(struct str));\n'
                 '    struct str *big = str_from(NULL, 0);\n'
                 '    printf("%zu\\n", big->len);\n'
                 '    struct str *parts[] = {a, b, c, s1, s2, s3, s4, z, e1, e2, big};\n'
                 '    for (int i = 0; i < 11; i++) str_free(parts[i]);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'malloc(sizeof *s + n + 1): заголовок, данные и завершающий ноль. sizeof структуры с гибким '
               'членом не включает хвост.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['12 [hello, world] 21',
                    '[world] [lo, world] [] [] 0',
                    '5 0 98 0 1',
                    '1 0 1',
                    '4 7 -1 4',
                    '9 8',
                    '0']},
      {'id': 'c14-packet-flex',
       'mode': 'c',
       'title': 'Пакеты переменной длины: сериализация и разбор',
       'statement': 'struct packet { uint8_t type; uint16_t len; uint8_t payload[]; } — заголовок на проводе '
                    '3 байта: type, len (big-endian, длина payload ≤ 1000), затем payload. pkt_new(type, '
                    'data, len) → пакет в куче (len > 1000 → NULL); pkt_wire_size(p) → 3 + len; '
                    'pkt_encode(p, out, cap) → число байт или 0, если не помещается; pkt_decode(buf, n, '
                    '*consumed) → пакет из начала буфера (возвращает NULL, если данных недостаточно, len > '
                    '1000 или заголовок неполон; *consumed = байт съедено при успехе); pkt_stream_count(buf, '
                    'n) → сколько полных пакетов подряд лежит в буфере (разбор прекращается на первом '
                    'неполном или неверном); pkt_free(p). Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '#include <stdint.h>\n'
                  '\n'
                  'struct packet { uint8_t type; uint16_t len; uint8_t payload[]; };\n'
                  '\n'
                  'struct packet *pkt_new(uint8_t type, const void *data, uint16_t len) { return 0; }\n'
                  'size_t pkt_wire_size(const struct packet *p) { return 0; }\n'
                  'size_t pkt_encode(const struct packet *p, uint8_t *out, size_t cap) { return 99; }\n'
                  'struct packet *pkt_decode(const uint8_t *buf, size_t n, size_t *consumed) { return 0; }\n'
                  'int pkt_stream_count(const uint8_t *buf, size_t n) { return -1; }\n'
                  'void pkt_free(struct packet *p) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct packet *a = pkt_new(7, "hello", 5), *b = pkt_new(9, NULL, 0), *c = pkt_new(1, '
                 '"xy", 2);\n'
                 '    printf("%zu %zu %zu\\n", pkt_wire_size(a), pkt_wire_size(b), sizeof(struct packet));\n'
                 '    uint8_t buf[64];\n'
                 '    size_t n = 0;\n'
                 '    n += pkt_encode(a, buf + n, sizeof buf - n);\n'
                 '    n += pkt_encode(b, buf + n, sizeof buf - n);\n'
                 '    n += pkt_encode(c, buf + n, sizeof buf - n);\n'
                 '    printf("%zu:", n);\n'
                 '    for (size_t i = 0; i < n; i++) printf(" %02x", buf[i]);\n'
                 '    printf("\\n");\n'
                 '    printf("%zu %zu\\n", pkt_encode(a, buf, 7), pkt_encode(a, buf, 8));\n'
                 '    size_t used = 0;\n'
                 '    struct packet *d = pkt_decode(buf, n, &used);\n'
                 '    printf("%u %u %.*s %zu\\n", d->type, d->len, d->len, d->payload, used);\n'
                 '    printf("%d %d %d %d\\n", pkt_stream_count(buf, n), pkt_stream_count(buf, n - 1), '
                 'pkt_stream_count(buf, 3), pkt_stream_count(buf, 0));\n'
                 '    uint8_t bad[] = {1, 0x0F, 0xFF, 1, 2};\n'
                 '    printf("%d %d\\n", pkt_decode(bad, 5, &used) == NULL, pkt_stream_count(bad, 5));\n'
                 '    static uint8_t zeros[1001];\n'
                 '    struct packet *p1 = pkt_new(1, zeros, 1001), *p2 = pkt_new(1, zeros, 1000);\n'
                 '    printf("%d %d\\n", p1 == NULL, p2 != NULL);\n'
                 '    pkt_free(p1);\n'
                 '    pkt_free(p2);\n'
                 '    uint8_t *big = malloc(1003);\n'
                 "    memset(big, 'z', 1003);\n"
                 '    big[0] = 5; big[1] = 0x03; big[2] = 0xE8;\n'
                 '    struct packet *e = pkt_decode(big, 1003, &used);\n'
                 '    printf("%u %u %zu\\n", e->type, e->len, used);\n'
                 '    pkt_free(a); pkt_free(b); pkt_free(c); pkt_free(d); pkt_free(e);\n'
                 '    free(big);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Размер выделения — sizeof *p + len. Длину на проводе читайте как (buf[1] << 8) | buf[2]; '
               'перед копированием проверяйте, что в буфере достаточно байт.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['8 3 4',
                    '16: 07 00 05 68 65 6c 6c 6f 09 00 00 01 00 02 78 79',
                    '0 8',
                    '7 5 hello 8',
                    '3 2 0 0',
                    '1 0',
                    '1 1',
                    '5 1000 1003']},
      {'id': 'c14-restrict-overlap',
       'mode': 'c',
       'title': 'restrict и пересекающиеся области',
       'statement': 'scale(out, in, n, k) и vec_add(out, a, b, n) объявлены с restrict: области не '
                    'пересекаются. regions_overlap(a, na, b, nb) → 1, если байтовые области [a, a + na) и '
                    '[b, b + nb) пересекаются (пустые не пересекаются ни с чем). safe_copy(dst, src, n) — '
                    'копирует n байт и корректно работает при пересечении (memcpy нельзя вызывать для '
                    'пересекающихся); возвращает 1, если области пересекались, иначе 0. shift_left(a, n, k) '
                    '— сдвигает массив int влево на k позиций (элементы справа заполняются нулями), '
                    'shift_right(a, n, k) — вправо; k может быть ≥ n. Для сдвигов — одна область (restrict '
                    'не используется).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'void scale(double *restrict out, const double *restrict in, size_t n, double k) {}\n'
                  'void vec_add(double *restrict out, const double *restrict a, const double *restrict b, '
                  'size_t n) {}\n'
                  'int regions_overlap(const void *a, size_t na, const void *b, size_t nb) { return -1; }\n'
                  'int safe_copy(void *dst, const void *src, size_t n) { return -1; }\n'
                  'void shift_left(int *a, size_t n, size_t k) {}\n'
                  'void shift_right(int *a, size_t n, size_t k) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    double in[4] = {1, 2, 3, 4}, out[4], a[4] = {1, 1, 1, 1};\n'
                 '    scale(out, in, 4, 2.5);\n'
                 '    printf("%.1f %.1f %.1f %.1f\\n", out[0], out[1], out[2], out[3]);\n'
                 '    vec_add(out, in, a, 4);\n'
                 '    printf("%.1f %.1f %.1f %.1f\\n", out[0], out[1], out[2], out[3]);\n'
                 '    char buf[16] = "abcdefghijklmno";\n'
                 '    printf("%d %d %d %d %d\\n", regions_overlap(buf, 8, buf + 4, 8), regions_overlap(buf, '
                 '4, buf + 4, 4), regions_overlap(buf, 5, buf + 4, 4), regions_overlap(buf, 0, buf, 4), '
                 'regions_overlap(buf + 3, 1, buf, 16));\n'
                 '    char t[16];\n'
                 '    strcpy(t, buf);\n'
                 '    int ov1 = safe_copy(t + 2, t, 8);\n'
                 '    printf("%d %.12s\\n", ov1, t);\n'
                 '    strcpy(t, buf);\n'
                 '    int ov2 = safe_copy(t, t + 2, 8);\n'
                 '    printf("%d %.12s\\n", ov2, t);\n'
                 '    char u[16] = "0123456789";\n'
                 '    int ov3 = safe_copy(u + 8, u, 8);\n'
                 '    printf("%d %.16s\\n", ov3, u);\n'
                 '    char w[8] = "QWERTY", z[8];\n'
                 '    int ov4 = safe_copy(z, w, 7);\n'
                 '    printf("%d %s\\n", ov4, z);\n'
                 '    int v[6] = {1, 2, 3, 4, 5, 6};\n'
                 '    shift_left(v, 6, 2);\n'
                 '    printf("%d %d %d %d %d %d\\n", v[0], v[1], v[2], v[3], v[4], v[5]);\n'
                 '    shift_right(v, 6, 3);\n'
                 '    printf("%d %d %d %d %d %d\\n", v[0], v[1], v[2], v[3], v[4], v[5]);\n'
                 '    shift_left(v, 6, 10);\n'
                 '    shift_right(v, 0, 1);\n'
                 '    printf("%d %d\\n", v[0], v[5]);\n'
                 '    int q[3] = {7, 8, 9};\n'
                 '    shift_right(q, 3, 3);\n'
                 '    shift_left(q, 3, 0);\n'
                 '    printf("%d %d %d\\n", q[0], q[1], q[2]);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Пересечение: x < y + nb && y < x + na для адресов как uintptr_t. Для пересекающихся областей '
               '— memmove; сдвиги массива — тоже memmove.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['2.5 5.0 7.5 10.0',
                    '2.0 3.0 4.0 5.0',
                    '1 0 1 0 1',
                    '1 ababcdefghkl',
                    '1 cdefghijijkl',
                    '0 0123456701234567',
                    '0 QWERTY',
                    '3 4 5 6 0 0',
                    '0 0 0 3 4 5',
                    '0 0',
                    '0 0 0']},
      {'id': 'c14-static-assert-layout',
       'mode': 'c',
       'title': 'Структуры под проверки _Static_assert',
       'statement': 'В starter уже записаны проверки _Static_assert для структур протокола. Определите '
                    'структуры так, чтобы ВСЕ проверки проходили (сейчас программа не компилируется): struct '
                    'hdr (8 байт: uint8_t ver, uint8_t flags, uint16_t len, uint32_t id; смещения 0, 1, 2, '
                    '4), struct sample (16 байт, выравнивание 8: первым double value, затем uint32_t ts, '
                    'uint16_t seq, uint8_t quality), struct rec (ровно 12 байт и выравнивание 4: char '
                    'tag[4], int32_t a, uint16_t b, uint8_t c, uint8_t d), union cell (8 байт: int64_t i, '
                    'double d, char bytes[8]). Затем напишите hdr_size_ok() → 1.',
       'starter': '#include <stddef.h>\n'
                  '#include <stdint.h>\n'
                  '\n'
                  '/* определите структуры ниже */\n'
                  '\n'
                  '_Static_assert(sizeof(struct hdr) == 8, "hdr size");\n'
                  '_Static_assert(offsetof(struct hdr, flags) == 1, "hdr.flags offset");\n'
                  '_Static_assert(offsetof(struct hdr, len) == 2, "hdr.len offset");\n'
                  '_Static_assert(offsetof(struct hdr, id) == 4, "hdr.id offset");\n'
                  '_Static_assert(sizeof(struct sample) == 16, "sample size");\n'
                  '_Static_assert(_Alignof(struct sample) == 8, "sample align");\n'
                  '_Static_assert(offsetof(struct sample, value) == 0, "sample.value first");\n'
                  '_Static_assert(sizeof(struct rec) == 12, "rec size");\n'
                  '_Static_assert(_Alignof(struct rec) == 4, "rec align");\n'
                  '_Static_assert(offsetof(struct rec, b) == 8, "rec.b offset");\n'
                  '_Static_assert(sizeof(union cell) == 8, "cell size");\n'
                  '\n'
                  'int hdr_size_ok(void) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%zu %zu %zu %zu\\n", sizeof(struct hdr), sizeof(struct sample), sizeof(struct '
                 'rec), sizeof(union cell));\n'
                 '    printf("%zu %zu %zu %zu\\n", offsetof(struct hdr, flags), offsetof(struct hdr, len), '
                 'offsetof(struct hdr, id), offsetof(struct sample, ts));\n'
                 '    printf("%zu %zu %zu\\n", offsetof(struct sample, seq), offsetof(struct sample, '
                 'quality), offsetof(struct rec, a));\n'
                 '    printf("%d\\n", hdr_size_ok());\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Порядок полей определяет прокладки: hdr — байтовые поля, затем uint16_t, затем uint32_t. '
               'sample: double первым, затем uint32_t, uint16_t, uint8_t (размер 16 — хвост до выравнивания '
               '8). rec: tag[4], int32_t, uint16_t, два байта.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['8 16 12 8', '1 2 4 8', '12 14 4', '1']},
      {'id': 'c14-generic-dispatch',
       'mode': 'c',
       'title': '_Generic: диспетчеризация по типу',
       'statement': 'Напишите функции max_int, max_long, max_double, max_u32 (наибольшее из двух) и макрос '
                    'MAX(a, b), выбирающий функцию по типу первого аргумента через _Generic (int, long, '
                    'double, unsigned). FMT(x) → строка формата printf для типа x: «%d» для int, «%ld» long, '
                    '«%u» unsigned, «%g» double, «%s» для char *, «%c» для char (тип char выбирайте по '
                    'значению переменной, не литерала), «%p» для void *; для прочих — «%?». SHOW(buf, cap, '
                    'x) → snprintf(buf, cap, FMT(x), x). TYPE_NAME(x) → «int», «long», «unsigned», «double», '
                    '«char *», «char», «other». ZERO_OF(x) → нулевое значение того же типа (0, 0L, 0u, 0.0).',
       'starter': '#include <stdio.h>\n'
                  '\n'
                  'int max_int(int a, int b) { return 0; }\n'
                  'long max_long(long a, long b) { return 0; }\n'
                  'double max_double(double a, double b) { return 0; }\n'
                  'unsigned max_u32(unsigned a, unsigned b) { return 0; }\n'
                  '\n'
                  '#define MAX(a, b) (a)\n'
                  '#define FMT(x) "%?"\n'
                  '#define SHOW(buf, cap, x) 0\n'
                  '#define TYPE_NAME(x) "other"\n'
                  '#define ZERO_OF(x) (x)\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    int i = 3, j = 9;\n'
                 '    long l = 100000L, m = -5;\n'
                 '    double d = 2.5, e = 1.5;\n'
                 '    unsigned u = 7, v = 4000000000u;\n'
                 '    printf("%d %ld %g %u\\n", MAX(i, j), MAX(l, m), MAX(d, e), MAX(u, v));\n'
                 '    char buf[64];\n'
                 "    char c = 'x';\n"
                 '    char *s = "text";\n'
                 '    void *p = NULL;\n'
                 '    SHOW(buf, sizeof buf, i); printf("[%s] ", buf);\n'
                 '    SHOW(buf, sizeof buf, l); printf("[%s] ", buf);\n'
                 '    SHOW(buf, sizeof buf, d); printf("[%s] ", buf);\n'
                 '    SHOW(buf, sizeof buf, u); printf("[%s] ", buf);\n'
                 '    SHOW(buf, sizeof buf, s); printf("[%s] ", buf);\n'
                 '    SHOW(buf, sizeof buf, c); printf("[%s]\\n", buf);\n'
                 '    printf("%s %s %s %s %s %s %s\\n", TYPE_NAME(i), TYPE_NAME(l), TYPE_NAME(u), '
                 'TYPE_NAME(d), TYPE_NAME(s), TYPE_NAME(c), TYPE_NAME(p));\n'
                 '    printf("%s %s\\n", FMT(p), FMT(1.5f));\n'
                 '    printf("%d %ld %u %g\\n", ZERO_OF(i), ZERO_OF(l), ZERO_OF(u), ZERO_OF(d));\n'
                 '    printf("%zu %zu %zu\\n", sizeof(ZERO_OF(i)), sizeof(ZERO_OF(l)), sizeof(ZERO_OF(d)));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': '_Generic((x), int: "%d", long: "%ld", …, default: "%?"). Для MAX выбирайте имя функции и '
               'вызывайте результат: _Generic(…)(a, b).',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['9 100000 2.5 4000000000',
                    '[3] [100000] [2.5] [7] [text] [x]',
                    'int long unsigned double char * char other',
                    '%p %?',
                    '0 0 0 0',
                    '4 8 8']},
      {'id': 'c14-anonymous-members',
       'mode': 'c',
       'title': 'Анонимные структуры и объединения',
       'statement': 'struct value { enum { V_INT, V_DBL, V_STR } tag; union { long i; double d; struct { '
                    'const char *ptr; size_t len; }; }; } — анонимное объединение с анонимной структурой '
                    'внутри (обращение v.i, v.d, v.ptr, v.len без промежуточных имён). v_int, v_dbl, '
                    'v_str(s) (len = strlen) — конструкторы; v_show(v, buf, cap) → «i:42», «d:2.50», '
                    '«s:text(4)» (длина в скобках); v_equal(a, b) (строки — по содержимому), v_len(v) → для '
                    'строки len, иначе 0. struct vec3 { union { struct { float x, y, z; }; float v[3]; }; }: '
                    'vec3_dot(a, b), vec3_cross(a, b), vec3_get(a, i) (через v[i]), vec3_sum(a) — сумма '
                    'через цикл по v[].',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct value { int tag; long i; };\n'
                  'struct vec3 { float x, y, z; };\n'
                  '\n'
                  'struct value v_int(long i) { struct value v = {0, i}; return v; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct value a = v_int(42), b = v_dbl(2.5), c = v_str("text"), d = v_str("text");\n'
                 '    char buf[32];\n'
                 '    int n1 = v_show(a, buf, sizeof buf); printf("%d %s | ", n1, buf);\n'
                 '    int n2 = v_show(b, buf, sizeof buf); printf("%d %s | ", n2, buf);\n'
                 '    int n3 = v_show(c, buf, sizeof buf); printf("%d %s\\n", n3, buf);\n'
                 '    printf("%d %d %d %d\\n", v_equal(a, a), v_equal(a, b), v_equal(c, d), v_equal(c, '
                 'v_str("tex")));\n'
                 '    printf("%zu %zu %zu\\n", v_len(a), v_len(c), v_len(v_str("")));\n'
                 '    printf("%d %d\\n", c.tag == V_STR, (int)c.len);\n'
                 '    struct vec3 p = {.x = 1, .y = 2, .z = 3}, q = {.v = {4, 5, 6}};\n'
                 '    struct vec3 r = vec3_cross(p, q);\n'
                 '    printf("%g %g %g %g\\n", vec3_dot(p, q), r.x, r.y, r.z);\n'
                 '    printf("%g %g %g %g %g\\n", vec3_get(q, 0), vec3_get(q, 2), vec3_sum(p), q.x + q.y, '
                 'p.v[1]);\n'
                 '    printf("%zu %zu\\n", sizeof(struct vec3), sizeof(struct value) <= 24);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Вложенные безымянные struct и union без имени поля: поля попадают прямо во внешнюю '
               'структуру. vec3 — объединение структуры {x, y, z} и массива v[3].',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['4 i:42 | 6 d:2.50 | 9 s:text(4)',
                    '1 0 1 0',
                    '0 4 0',
                    '1 4',
                    '32 -3 6 -3',
                    '4 6 6 9 2',
                    '12 1']},
      {'id': 'c14-aligned-alloc',
       'mode': 'c',
       'title': 'Выравнивание: _Alignas, _Alignof и свой aligned_alloc',
       'statement': 'is_aligned(p, a) → 1, если адрес p кратен a (a — степень двойки); align_up(n, a) → n, '
                    'округлённое вверх до кратного a; aligned_alloc2(size, align) → указатель, выровненный '
                    'по align (степень двойки, ≤ 4096), на size байт: выделить malloc(size + align + '
                    'sizeof(void *)), выровнять и сохранить исходный указатель непосредственно перед '
                    'возвращаемым адресом; aligned_free2(p) освобождает его (NULL допустим). '
                    'alignment_report(out) → строка «char=1 short=2 int=4 long=8 double=8 ptr=8 maxalign=16» '
                    '(значения _Alignof; размер ptr — _Alignof(void *); maxalign — _Alignof(max_align_t)). '
                    'Объект с _Alignas(64) char cache[64] объявлен в драйвере. Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '#include <stdalign.h>\n'
                  '#include <stdbool.h>\n'
                  '\n'
                  'bool is_aligned(const void *p, size_t a) { return false; }\n'
                  'size_t align_up(size_t n, size_t a) { return n; }\n'
                  'void *aligned_alloc2(size_t size, size_t align) { return 0; }\n'
                  'void aligned_free2(void *p) {}\n'
                  'void alignment_report(char *out) { out[0] = 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 '#include <stdalign.h>\n'
                 '\n'
                 'alignas(64) static char cache[64];\n'
                 '_Alignas(32) static int vec8[8];\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%d %d %d\\n", is_aligned(cache, 64), is_aligned(vec8, 32), is_aligned(cache + '
                 '1, 2));\n'
                 '    printf("%d %d %d\\n", is_aligned((void *)64, 64), is_aligned((void *)0, 8), '
                 'is_aligned((void *)12, 8));\n'
                 '    printf("%zu %zu %zu %zu %zu\\n", align_up(0, 8), align_up(1, 8), align_up(8, 8), '
                 'align_up(13, 16), align_up(4097, 4096));\n'
                 '    size_t aligns[] = {1, 2, 8, 16, 64, 256, 4096};\n'
                 '    int ok = 1;\n'
                 '    for (int i = 0; i < 7; i++) {\n'
                 '        char *p = aligned_alloc2(100 + (size_t)i, aligns[i]);\n'
                 '        ok &= p != NULL && is_aligned(p, aligns[i]);\n'
                 '        memset(p, 0xAB, 100 + (size_t)i);\n'
                 '        aligned_free2(p);\n'
                 '    }\n'
                 '    printf("%d\\n", ok);\n'
                 '    aligned_free2(NULL);\n'
                 '    char *many[20];\n'
                 '    int all = 1;\n'
                 '    for (int i = 0; i < 20; i++) { many[i] = aligned_alloc2(1, 64); all &= '
                 'is_aligned(many[i], 64); }\n'
                 '    printf("%d\\n", all);\n'
                 '    for (int i = 0; i < 20; i++) aligned_free2(many[i]);\n'
                 '    char rep[128];\n'
                 '    alignment_report(rep);\n'
                 '    printf("%s\\n", rep);\n'
                 '    printf("%zu %zu\\n", alignof(cache), alignof(vec8));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Выделите size + align + sizeof(void *), округлите адрес (raw + sizeof(void *)) вверх до '
               'align и положите raw в ячейку перед результатом: ((void **)p)[-1].',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 1 0',
                    '1 1 0',
                    '0 8 8 16 8192',
                    '1',
                    '1',
                    'char=1 short=2 int=4 long=8 double=8 ptr=8 maxalign=16',
                    '64 32']},
      {'id': 'c14-atomic-counter-lock',
       'mode': 'c',
       'title': 'Атомарный счётчик и спинлок на stdatomic',
       'statement': 'struct spin { atomic_flag f; } — спинлок: spin_init, spin_lock (цикл '
                    'atomic_flag_test_and_set_explicit с acquire), spin_trylock → 1/0, spin_unlock (clear с '
                    'release). struct counter { atomic_long v; }: counter_init(c, x), counter_add(c, d) → '
                    'прежнее значение (fetch_add), counter_get(c), counter_max(c, x) — установить максимум '
                    '(CAS-цикл), counter_cas(c, expected, desired) → 1/0 (strong). Драйвер запускает '
                    'несколько потоков <threads.h>: обычная переменная под спинлоком и атомарный счётчик; '
                    'итоги должны быть точными.',
       'starter': '#include <stdatomic.h>\n'
                  '\n'
                  'struct spin { atomic_flag f; };\n'
                  'struct counter { atomic_long v; };\n'
                  '\n'
                  'void spin_init(struct spin *s) {}\n'
                  'void spin_lock(struct spin *s) {}\n'
                  'int spin_trylock(struct spin *s) { return -1; }\n'
                  'void spin_unlock(struct spin *s) {}\n'
                  'void counter_init(struct counter *c, long x) {}\n'
                  'long counter_add(struct counter *c, long d) { return -9; }\n'
                  'long counter_get(struct counter *c) { return -9; }\n'
                  'void counter_max(struct counter *c, long x) {}\n'
                  'int counter_cas(struct counter *c, long expected, long desired) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 '#include <threads.h>\n'
                 '\n'
                 'static struct spin lock;\n'
                 'static struct counter cnt, mx;\n'
                 'static long plain;\n'
                 '\n'
                 'static int worker(void *arg) {\n'
                 '    long id = (long)(intptr_t)arg;\n'
                 '    for (int i = 0; i < 20000; i++) {\n'
                 '        spin_lock(&lock);\n'
                 '        plain++;\n'
                 '        spin_unlock(&lock);\n'
                 '        counter_add(&cnt, 1);\n'
                 '        counter_max(&mx, id * 1000 + i % 1000);\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    spin_init(&lock);\n'
                 '    int tl1 = spin_trylock(&lock);\n'
                 '    int tl2 = spin_trylock(&lock);\n'
                 '    printf("%d %d\\n", tl1, tl2);\n'
                 '    spin_unlock(&lock);\n'
                 '    printf("%d\\n", spin_trylock(&lock));\n'
                 '    spin_unlock(&lock);\n'
                 '    counter_init(&cnt, 0);\n'
                 '    counter_init(&mx, -1);\n'
                 '    long old = counter_add(&cnt, 5);\n'
                 '    printf("%ld %ld\\n", old, counter_get(&cnt));\n'
                 '    counter_max(&mx, 10);\n'
                 '    counter_max(&mx, 3);\n'
                 '    printf("%ld\\n", counter_get(&mx));\n'
                 '    int cs1 = counter_cas(&cnt, 5, 50);\n'
                 '    int cs2 = counter_cas(&cnt, 5, 99);\n'
                 '    printf("%d %d %ld\\n", cs1, cs2, counter_get(&cnt));\n'
                 '    counter_init(&cnt, 0);\n'
                 '    counter_init(&mx, -1);\n'
                 '    thrd_t t[4];\n'
                 '    for (int i = 0; i < 4; i++) thrd_create(&t[i], worker, (void *)(intptr_t)(i + 1));\n'
                 '    for (int i = 0; i < 4; i++) thrd_join(t[i], NULL);\n'
                 '    printf("%ld %ld %ld\\n", plain, counter_get(&cnt), counter_get(&mx));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Спинлок: while (atomic_flag_test_and_set_explicit(&f, memory_order_acquire)); unlock — clear '
               'с memory_order_release. counter_max: читаем old, пока old < x, пробуем CAS.',
       'flags': '-std=c11 -pthread -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 0', '1', '0 5', '10', '1 0 50', '80000 80000 4999']},
      {'id': 'c14-treiber-stack',
       'mode': 'c',
       'title': 'Стек без блокировок (CAS)',
       'statement': 'struct lfnode { struct lfnode *next; int value; }; struct lfstack { _Atomic(struct '
                    'lfnode *) head; }. lf_init(s); lf_push(s, node) — вставка узла в вершину циклом '
                    'compare_exchange_weak (node->next = текущая голова); lf_pop(s) → снятый узел или NULL '
                    '(CAS-цикл по голове; узлы после pop освобождает вызывающий); lf_peek(s) → вершина или '
                    'NULL (без снятия); lf_size(s) → число узлов, обход цепочки (только когда другие потоки '
                    'не работают). Узлы выделяет драйвер. Многопоточная проверка: несколько потоков '
                    'одновременно вставляют свои узлы, затем один поток снимает всё.',
       'starter': '#include <stdatomic.h>\n'
                  '#include <stddef.h>\n'
                  '\n'
                  'struct lfnode { struct lfnode *next; int value; };\n'
                  'struct lfstack { _Atomic(struct lfnode *) head; };\n'
                  '\n'
                  'void lf_init(struct lfstack *s) {}\n'
                  'void lf_push(struct lfstack *s, struct lfnode *n) {}\n'
                  'struct lfnode *lf_pop(struct lfstack *s) { return 0; }\n'
                  'struct lfnode *lf_peek(struct lfstack *s) { return 0; }\n'
                  'size_t lf_size(struct lfstack *s) { return 99; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 '#include <threads.h>\n'
                 '\n'
                 'enum { PER = 2000, NT = 4 };\n'
                 'static struct lfstack st;\n'
                 'static struct lfnode *nodes;\n'
                 '\n'
                 'static int pusher(void *arg) {\n'
                 '    int id = (int)(intptr_t)arg;\n'
                 '    for (int i = 0; i < PER; i++) {\n'
                 '        struct lfnode *n = &nodes[id * PER + i];\n'
                 '        n->value = id * PER + i;\n'
                 '        lf_push(&st, n);\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    lf_init(&st);\n'
                 '    struct lfnode a = {0, 1}, b = {0, 2}, c = {0, 3};\n'
                 '    printf("%d %zu\\n", lf_pop(&st) == NULL, lf_size(&st));\n'
                 '    lf_push(&st, &a); lf_push(&st, &b); lf_push(&st, &c);\n'
                 '    printf("%d %zu\\n", lf_peek(&st)->value, lf_size(&st));\n'
                 '    int p1 = lf_pop(&st)->value;\n'
                 '    int p2 = lf_pop(&st)->value;\n'
                 '    int p3 = lf_pop(&st)->value;\n'
                 '    int p4 = lf_pop(&st) == NULL;\n'
                 '    printf("%d %d %d %d\\n", p1, p2, p3, p4);\n'
                 '    nodes = malloc(sizeof(struct lfnode) * PER * NT);\n'
                 '    thrd_t t[NT];\n'
                 '    for (int i = 0; i < NT; i++) thrd_create(&t[i], pusher, (void *)(intptr_t)i);\n'
                 '    for (int i = 0; i < NT; i++) thrd_join(t[i], NULL);\n'
                 '    printf("%zu\\n", lf_size(&st));\n'
                 '    char *seen = calloc(PER * NT, 1);\n'
                 '    long sum = 0;\n'
                 '    int dup = 0, cnt = 0;\n'
                 '    struct lfnode *n;\n'
                 '    while ((n = lf_pop(&st)) != NULL) {\n'
                 '        if (seen[n->value]) dup++;\n'
                 '        seen[n->value] = 1;\n'
                 '        sum += n->value;\n'
                 '        cnt++;\n'
                 '    }\n'
                 '    printf("%d %d %ld %zu\\n", cnt, dup, sum, lf_size(&st));\n'
                 '    free(seen);\n'
                 '    free(nodes);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'push: old = голова; цикл: node->next = old; CAS(голова: old → node) — при неудаче old '
               'обновляется автоматически. pop: CAS(голова: old → old->next) для непустой головы.',
       'flags': '-std=c11 -pthread -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 0', '3 3', '3 2 1 1', '8000', '8000 0 31996000 0']},
      {'id': 'c14-release-acquire',
       'mode': 'c',
       'title': 'Передача данных между потоками: release и acquire',
       'statement': 'struct mailbox { int data[16]; int n; atomic_int ready; }. mb_init(m); mb_publish(m, '
                    'values, n) — записать данные и n (n ≤ 16), затем сохранить ready = 1 с '
                    'memory_order_release; mb_consume(m, out) → число значений: ждать (спин) пока ready == '
                    '1, прочитав его с memory_order_acquire, затем скопировать данные в out и вернуть n; '
                    'mb_reset(m) — ready = 0 (вызывается после чтения). mb_try_consume(m, out) → число '
                    'значений или −1, если пока не готово (без ожидания). Данные не помечаются атомарными: '
                    'корректный порядок обеспечивают release/acquire.',
       'starter': '#include <stdatomic.h>\n'
                  '\n'
                  'struct mailbox { int data[16]; int n; atomic_int ready; };\n'
                  '\n'
                  'void mb_init(struct mailbox *m) {}\n'
                  'void mb_publish(struct mailbox *m, const int *values, int n) {}\n'
                  'int mb_consume(struct mailbox *m, int *out) { return -9; }\n'
                  'int mb_try_consume(struct mailbox *m, int *out) { return -9; }\n'
                  'void mb_reset(struct mailbox *m) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 '#include <threads.h>\n'
                 '\n'
                 'static struct mailbox box;\n'
                 'static atomic_int done;\n'
                 'static long total;\n'
                 '\n'
                 'static int producer(void *arg) {\n'
                 '    (void)arg;\n'
                 '    for (int round = 0; round < 200; round++) {\n'
                 '        while (atomic_load(&done) != round) {}\n'
                 '        int v[16];\n'
                 '        int n = 1 + round % 16;\n'
                 '        for (int i = 0; i < n; i++) v[i] = round * 100 + i;\n'
                 '        mb_publish(&box, v, n);\n'
                 '        while (atomic_load(&done) == round) {}\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    mb_init(&box);\n'
                 '    int out[16];\n'
                 '    printf("%d\\n", mb_try_consume(&box, out));\n'
                 '    int vals[] = {5, 6, 7};\n'
                 '    mb_publish(&box, vals, 3);\n'
                 '    int n = mb_try_consume(&box, out);\n'
                 '    printf("%d %d %d %d\\n", n, out[0], out[1], out[2]);\n'
                 '    mb_reset(&box);\n'
                 '    printf("%d\\n", mb_try_consume(&box, out));\n'
                 '    atomic_init(&done, 0);\n'
                 '    thrd_t t;\n'
                 '    thrd_create(&t, producer, NULL);\n'
                 '    int bad = 0;\n'
                 '    for (int round = 0; round < 200; round++) {\n'
                 '        int k = mb_consume(&box, out);\n'
                 '        if (k != 1 + round % 16) bad++;\n'
                 '        for (int i = 0; i < k; i++) {\n'
                 '            if (out[i] != round * 100 + i) bad++;\n'
                 '            total += out[i];\n'
                 '        }\n'
                 '        mb_reset(&box);\n'
                 '        atomic_store(&done, round + 1);\n'
                 '    }\n'
                 '    thrd_join(t, NULL);\n'
                 '    printf("%d %ld\\n", bad, total);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Публикация: сначала обычные записи данных, затем atomic_store_explicit(&ready, 1, '
               'memory_order_release). Чтение: atomic_load_explicit(&ready, memory_order_acquire) и только '
               'после этого — чтение данных.',
       'flags': '-std=c11 -pthread -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['-1', '3 5 6 7', '-1', '0 16709844']},
      {'id': 'c14-call-once',
       'mode': 'c',
       'title': 'Однократная инициализация: call_once на атомиках',
       'statement': 'struct once { atomic_int state; } (0 — не начата, 1 — выполняется, 2 — завершена). '
                    'once_init(o); once_call(o, fn, arg): если состояние 0 — перевести CAS в 1, выполнить '
                    'fn(arg), записать 2 с release; если 1 — ждать завершения (спин с acquire); если 2 — '
                    'вернуться сразу. Функция fn выполняется не более одного раза за всё время, и все вызовы '
                    'once_call возвращаются только после её завершения. once_done(o) → 1, если состояние 2. '
                    'once_reset(o) — вернуть в 0 (только когда никто не работает). Драйвер вызывает '
                    'once_call из нескольких потоков одновременно и проверяет, что инициализация выполнена '
                    'единожды и результаты видны всем.',
       'starter': '#include <stdatomic.h>\n'
                  '\n'
                  'struct once { atomic_int state; };\n'
                  '\n'
                  'void once_init(struct once *o) {}\n'
                  'void once_call(struct once *o, void (*fn)(void *), void *arg) {}\n'
                  'int once_done(struct once *o) { return -1; }\n'
                  'void once_reset(struct once *o) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 '#include <threads.h>\n'
                 '\n'
                 'static struct once once;\n'
                 'static int inits;\n'
                 'static int table[64];\n'
                 'static atomic_int bad;\n'
                 '\n'
                 'static void init(void *arg) {\n'
                 '    inits++;\n'
                 '    for (int i = 0; i < 64; i++) table[i] = i * (int)(intptr_t)arg;\n'
                 '}\n'
                 '\n'
                 'static int worker(void *arg) {\n'
                 '    (void)arg;\n'
                 '    for (int round = 0; round < 3; round++) {\n'
                 '        once_call(&once, init, (void *)(intptr_t)3);\n'
                 '        for (int i = 0; i < 64; i++) if (table[i] != i * 3) atomic_fetch_add(&bad, 1);\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    once_init(&once);\n'
                 '    printf("%d\\n", once_done(&once));\n'
                 '    once_call(&once, init, (void *)(intptr_t)2);\n'
                 '    once_call(&once, init, (void *)(intptr_t)2);\n'
                 '    printf("%d %d %d\\n", inits, once_done(&once), table[10]);\n'
                 '    once_reset(&once);\n'
                 '    inits = 0;\n'
                 '    for (int round = 0; round < 20; round++) {\n'
                 '        thrd_t t[6];\n'
                 '        once_reset(&once);\n'
                 '        for (int i = 0; i < 6; i++) thrd_create(&t[i], worker, NULL);\n'
                 '        for (int i = 0; i < 6; i++) thrd_join(t[i], NULL);\n'
                 '    }\n'
                 '    printf("%d %d %d\\n", inits, atomic_load(&bad), once_done(&once));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'CAS 0 → 1 выбирает одного исполнителя. Остальные ждут, пока состояние не станет 2 (acquire). '
               'Запись 2 — с release после fn.',
       'flags': '-std=c11 -pthread -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0', '1 1 20', '20 0 1']},
      {'id': 'c14-spsc-ring',
       'mode': 'c',
       'title': 'Кольцевой буфер «один производитель — один потребитель»',
       'statement': 'struct spsc { int buf[64]; atomic_size_t head, tail; } — ёмкость 64, индексы head '
                    '(читает потребитель) и tail (пишет производитель) растут без модуля, индекс ячейки — по '
                    'модулю 64. spsc_init(r); spsc_push(r, v) → 1, если записано, 0, если полно (tail − head '
                    '== 64): записать значение, затем tail + 1 с release; spsc_pop(r, *v) → 1/0 (пусто): '
                    'прочитать tail с acquire, взять значение, затем head + 1 с release; spsc_size(r) → tail '
                    '− head; Драйвер запускает два потока: производитель кладёт 100000 чисел подряд (ждёт '
                    'при переполнении), потребитель забирает и проверяет порядок.',
       'starter': '#include <stdatomic.h>\n'
                  '#include <stddef.h>\n'
                  '\n'
                  'struct spsc { int buf[64]; atomic_size_t head, tail; };\n'
                  '\n'
                  'void spsc_init(struct spsc *r) {}\n'
                  'int spsc_push(struct spsc *r, int v) { return -1; }\n'
                  'int spsc_pop(struct spsc *r, int *v) { return -1; }\n'
                  'size_t spsc_size(struct spsc *r) { return 99; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 '#include <threads.h>\n'
                 '\n'
                 'static struct spsc ring;\n'
                 'enum { N = 100000 };\n'
                 '\n'
                 'static int producer(void *arg) {\n'
                 '    (void)arg;\n'
                 '    for (int i = 0; i < N; i++)\n'
                 '        while (!spsc_push(&ring, i)) {}\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    spsc_init(&ring);\n'
                 '    int v = -1;\n'
                 '    printf("%d %zu\\n", spsc_pop(&ring, &v), spsc_size(&ring));\n'
                 '    int pushed = 0;\n'
                 '    for (int i = 0; i < 70; i++) pushed += spsc_push(&ring, i * 2);\n'
                 '    printf("%d %zu\\n", pushed, spsc_size(&ring));\n'
                 '    int popped[3];\n'
                 '    for (int i = 0; i < 3; i++) { spsc_pop(&ring, &v); popped[i] = v; }\n'
                 '    printf("%d %d %d %zu\\n", popped[0], popped[1], popped[2], spsc_size(&ring));\n'
                 '    printf("%d %d\\n", spsc_push(&ring, 7), spsc_push(&ring, 8));\n'
                 '    while (spsc_pop(&ring, &v)) {}\n'
                 '    printf("%zu\\n", spsc_size(&ring));\n'
                 '    thrd_t t;\n'
                 '    thrd_create(&t, producer, NULL);\n'
                 '    int expect = 0, bad = 0;\n'
                 '    while (expect < N) {\n'
                 '        if (spsc_pop(&ring, &v)) {\n'
                 '            if (v != expect) bad++;\n'
                 '            expect++;\n'
                 '        }\n'
                 '    }\n'
                 '    thrd_join(t, NULL);\n'
                 '    printf("%d %d %zu\\n", expect, bad, spsc_size(&ring));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Производитель владеет tail, потребитель — head. Запись данных до store(tail, release); '
               'чтение tail (acquire) до чтения данных. Полно, когда tail − head == 64.',
       'flags': '-std=c11 -pthread -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 0', '64 64', '0 2 4 61', '1 1', '0', '100000 0 0']},
      {'id': 'c14-utf32-utf16',
       'mode': 'c',
       'title': 'char32_t и char16_t: UTF-8 ↔ UTF-32 ↔ UTF-16',
       'statement': 'utf8_to_utf32(s, out, max) → число кодовых точек (char32_t) или −1 при неверном UTF-8 '
                    '(оборванные и избыточные последовательности, суррогаты, > 0x10FFFF); если результат не '
                    'помещается в max — −2. utf32_to_utf8(in, n, out, cap) → число байт без завершающего '
                    'нуля (и ноль на конце, если есть место) или −1 (недопустимая точка), −2 (не '
                    'помещается). utf32_to_utf16(in, n, out, max) → число char16_t (с суррогатными парами '
                    'для точек ≥ 0x10000), utf16_to_utf32(in, n, out, max) → число точек (одиночный или '
                    'перевёрнутый суррогат — −1). utf16_len(s32, n) → сколько char16_t понадобится.',
       'starter': '#include <stddef.h>\n'
                  '#include <stdint.h>\n'
                  '#include <uchar.h>\n'
                  '\n'
                  'long utf8_to_utf32(const char *s, char32_t *out, size_t max) { return -9; }\n'
                  'long utf32_to_utf8(const char32_t *in, size_t n, char *out, size_t cap) { return -9; }\n'
                  'long utf32_to_utf16(const char32_t *in, size_t n, char16_t *out, size_t max) { return -9; '
                  '}\n'
                  'long utf16_to_utf32(const char16_t *in, size_t n, char32_t *out, size_t max) { return -9; '
                  '}\n'
                  'size_t utf16_len(const char32_t *s32, size_t n) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 '#include <uchar.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char32_t u[32];\n'
                 '    char16_t w[32];\n'
                 '    char b[64];\n'
                 '    const char *s = "Aé€😀я";\n'
                 '    long n = utf8_to_utf32(s, u, 32);\n'
                 '    printf("%ld:", n);\n'
                 '    for (long i = 0; i < n; i++) printf(" %X", (unsigned)u[i]);\n'
                 '    printf("\\n");\n'
                 '    long k = utf32_to_utf16(u, (size_t)n, w, 32);\n'
                 '    printf("%ld %zu:", k, utf16_len(u, (size_t)n));\n'
                 '    for (long i = 0; i < k; i++) printf(" %X", (unsigned)w[i]);\n'
                 '    printf("\\n");\n'
                 '    char32_t back[32];\n'
                 '    long m = utf16_to_utf32(w, (size_t)k, back, 32);\n'
                 '    printf("%ld %d\\n", m, memcmp(u, back, (size_t)n * sizeof(char32_t)) == 0);\n'
                 '    long q = utf32_to_utf8(u, (size_t)n, b, sizeof b);\n'
                 '    printf("%ld %d %s\\n", q, strcmp(b, s) == 0, b);\n'
                 '    printf("%ld %ld %ld\\n", utf8_to_utf32("\\xC0\\x80", u, 32), '
                 'utf8_to_utf32("\\xED\\xA0\\x80", u, 32), utf8_to_utf32("ab\\xE2\\x82", u, 32));\n'
                 '    printf("%ld %ld\\n", utf8_to_utf32(s, u, 3), utf8_to_utf32("", u, 0));\n'
                 '    char32_t bad1[] = {0xD800}, bad2[] = {0x110000}, ok1[] = {0x10FFFF};\n'
                 '    printf("%ld %ld %ld\\n", utf32_to_utf8(bad1, 1, b, 64), utf32_to_utf8(bad2, 1, b, 64), '
                 'utf32_to_utf8(ok1, 1, b, 64));\n'
                 '    printf("%ld %ld\\n", utf32_to_utf8(u, (size_t)n, b, 5), utf32_to_utf16(u, (size_t)n, '
                 'w, 4));\n'
                 '    char16_t lone[] = {0xD83D}, rev[] = {0xDE00, 0xD83D}, pair[] = {0xD83D, 0xDE00};\n'
                 '    printf("%ld %ld %ld\\n", utf16_to_utf32(lone, 1, back, 8), utf16_to_utf32(rev, 2, '
                 'back, 8), utf16_to_utf32(pair, 2, back, 8));\n'
                 '    printf("%X\\n", (unsigned)back[0]);\n'
                 '    printf("%ld %zu\\n", utf16_to_utf32(pair, 2, back, 0), utf16_len(NULL, 0));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Суррогатная пара: c − 0x10000 → старшие 10 бит + 0xD800 и младшие 10 бит + 0xDC00. '
               'Декодирование — обратное; одиночные и перевёрнутые суррогаты — ошибка.',
       'flags': '-std=c23 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['5: 41 E9 20AC 1F600 44F',
                    '6 6: 41 E9 20AC D83D DE00 44F',
                    '5 1',
                    '12 1 Aé€😀я',
                    '-1 -1 -1',
                    '-2 0',
                    '-1 -1 4',
                    '-2 -2',
                    '-1 -1 1',
                    '1F600',
                    '-2 0']},
      {'id': 'c14-cyrillic-case',
       'mode': 'c',
       'title': 'Регистр букв в UTF-8: ASCII и русский алфавит',
       'statement': 'Строки — UTF-8. utf8_upper(s, out, cap) и utf8_lower(s, out, cap) → длина результата в '
                    'байтах (или −1, если не помещается с нулём; −2 при неверном UTF-8): латинские a–z ↔ '
                    'A–Z, русские а–я (U+0430…U+044F) ↔ А–Я (U+0410…U+042F), ё (U+0451) ↔ Ё (U+0401); '
                    'остальные символы не меняются. Длина символа в байтах для этих букв не меняется. '
                    'utf8_equal_fold(a, b) → 1, если строки равны без учёта регистра (в тех же правилах); '
                    'utf8_title(s, out, cap) — первая буква каждого слова (слова разделены пробелами) — '
                    'заглавная, остальные — строчные; count_letters(s, *latin, *cyrillic) — число латинских '
                    'и русских букв (любого регистра).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'long utf8_upper(const char *s, char *out, size_t cap) { return -9; }\n'
                  'long utf8_lower(const char *s, char *out, size_t cap) { return -9; }\n'
                  'int utf8_equal_fold(const char *a, const char *b) { return -1; }\n'
                  'long utf8_title(const char *s, char *out, size_t cap) { return -9; }\n'
                  'void count_letters(const char *s, int *latin, int *cyrillic) { *latin = *cyrillic = -1; '
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    char b[128];\n'
                 '    const char *t[] = {"Hello, Мир! ёжик Ёлка", "ПРИВЕТ привет", "ß é ü 123", "", "αβγ"};\n'
                 '    for (int i = 0; i < 5; i++) {\n'
                 '        long u = utf8_upper(t[i], b, sizeof b);\n'
                 '        printf("%ld %s | ", u, b);\n'
                 '        long l = utf8_lower(t[i], b, sizeof b);\n'
                 '        printf("%ld %s\\n", l, b);\n'
                 '    }\n'
                 '    printf("%d %d %d %d\\n", utf8_equal_fold("Привет", "пРИВЕТ"), utf8_equal_fold("ёлка", '
                 '"ЁЛКА"), utf8_equal_fold("abc", "abd"), utf8_equal_fold("abc", "abcd"));\n'
                 '    long tt = utf8_title("hello wORLD привет МИР", b, sizeof b);\n'
                 '    printf("%ld %s\\n", tt, b);\n'
                 '    tt = utf8_title("  два  слова ", b, sizeof b);\n'
                 '    printf("%ld [%s]\\n", tt, b);\n'
                 '    int lat, cyr;\n'
                 '    count_letters("Hello Мир ёж 42", &lat, &cyr);\n'
                 '    printf("%d %d\\n", lat, cyr);\n'
                 '    char small[8];\n'
                 '    printf("%ld %ld %ld\\n", utf8_upper("Привет", small, sizeof small), utf8_upper("При", '
                 'small, sizeof small), utf8_lower("\\xff", small, sizeof small));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Раскодируйте символ, преобразуйте кодовую точку (сдвиг на 32 для а–я/А–Я и a–z/A–Z; ё и Ё — '
               'отдельно) и закодируйте обратно: длина в байтах для этих букв сохраняется.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['32 HELLO, МИР! ЁЖИК ЁЛКА | 32 hello, мир! ёжик ёлка',
                    '25 ПРИВЕТ ПРИВЕТ | 25 привет привет',
                    '12 ß é ü 123 | 12 ß é ü 123',
                    '0  | 0',
                    '6 αβγ | 6 αβγ',
                    '1 1 0 0',
                    '31 Hello World Привет Мир',
                    '21 [  Два  Слова ]',
                    '5 5',
                    '-1 6 -2']},
      {'id': 'c14-c23-syntax',
       'mode': 'c',
       'title': 'Синтаксис C23 на практике',
       'statement': 'Напишите на C23 (компилируется с -std=c23): constexpr int MAX_ITEMS = 8; '
                    'find_first_neg(a, n) → указатель на первый отрицательный элемент или nullptr '
                    "(используйте nullptr, не NULL); parse_bits(s) → целое из строки из символов '0'/'1' (до "
                    '32 символов, иначе −1) — для проверки используйте двоичный литерал 0b… ; '
                    "big_numbers(out) → записать в out[3] значения 1'000, 0b1010'1010, 0xFF'FF (разделители "
                    'разрядов обязательны в тексте программы); swap_any(a, b) — макрос через typeof (без '
                    'расширений GNU); first_or(a, n, dflt) — через auto и bool; sum_limit(a, n) → сумма '
                    "первых MAX_ITEMS элементов; fallthrough_demo(x) → x == 1: 'A' + 'B', x == 2: 'B', иначе "
                    '0 с [[fallthrough]]. В исходном тексте должны встретиться nullptr, constexpr, typeof, '
                    'auto, bool, [[fallthrough]] и разделитель разрядов.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int *find_first_neg(int *a, int n) { return 0; }\n'
                  'long parse_bits(const char *s) { return -2; }\n'
                  'void big_numbers(long *out) {}\n'
                  '#define swap_any(a, b)\n'
                  'int first_or(const int *a, int n, int dflt) { return dflt; }\n'
                  'long sum_limit(const int *a, int n) { return 0; }\n'
                  'int fallthrough_demo(int x) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
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
                 '    int a[] = {3, 5, -2, 7, -9};\n'
                 '    int *p = find_first_neg(a, 5);\n'
                 '    printf("%d %d %d\\n", p != nullptr, *p, find_first_neg(a, 2) == nullptr);\n'
                 '    printf("%ld %ld %ld %ld\\n", parse_bits("1010"), parse_bits(""), parse_bits("102"), '
                 'parse_bits("11111111111111111111111111111111"));\n'
                 '    printf("%ld %ld\\n", parse_bits("111111111111111111111111111111111"), '
                 'parse_bits("0"));\n'
                 '    long big[3];\n'
                 '    big_numbers(big);\n'
                 '    printf("%ld %ld %ld\\n", big[0], big[1], big[2]);\n'
                 '    int x = 1, y = 2;\n'
                 '    swap_any(x, y);\n'
                 '    double d = 1.5, e = 2.5;\n'
                 '    swap_any(d, e);\n'
                 '    printf("%d %d %g %g\\n", x, y, d, e);\n'
                 '    int z[] = {-1, 0, 4, 9};\n'
                 '    printf("%d %d\\n", first_or(z, 4, -100), first_or(z, 2, -100));\n'
                 '    int big_arr[12] = {1, 1, 1, 1, 1, 1, 1, 1, 100, 100, 100, 100};\n'
                 '    printf("%ld\\n", sum_limit(big_arr, 12));\n'
                 '    printf("%d %d %d\\n", fallthrough_demo(1), fallthrough_demo(2), fallthrough_demo(3));\n'
                 '    printf("tokens: %d %d %d %d %d %d %d\\n",\n'
                 '           src_count("nul" "lptr") > 0, src_count("cons" "texpr") > 0, src_count("typ" '
                 '"eof") > 0,\n'
                 '           src_count("au" "to ") > 0, src_count("bo" "ol ") > 0, src_count("[[fallt" '
                 '"hrough]]") > 0,\n'
                 '           src_count("" "\'") > 0);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': "constexpr int MAX_ITEMS = 8; return nullptr; typeof(a) _t = (a); auto x = …; 0b1010'1010; "
               '[[fallthrough]]; перед следующим case.',
       'flags': '-std=c23 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 -2 1',
                    '10 0 -1 4294967295',
                    '-1 0',
                    '1000 170 65535',
                    '2 1 2.5 1.5',
                    '4 -100',
                    '8',
                    '131 66 0',
                    'tokens: 1 1 1 1 1 1 1']},
      {'id': 'c14-fix-attributes',
       'mode': 'c',
       'title': 'Исправьте: предупреждения — через атрибуты и стандартные средства',
       'statement': 'Код C23 собирается с -Wall -Wextra -Werror -Wimplicit-fallthrough -Wunused-parameter '
                    '-Wunused-function -Wsuggest-attribute=noreturn и не проходит: проход в switch без '
                    'пометки, неиспользуемый параметр callback, неиспользуемая статическая функция '
                    'debug_dump, функция fatal, которая не возвращается, но не помечена, и параметр '
                    'callback, который функции ничего не даёт. Исправьте стандартными атрибутами '
                    '([[fallthrough]], [[maybe_unused]], [[noreturn]], [[nodiscard]]) так, чтобы сборка шла '
                    'чисто, а поведение не менялось. Функция checked_div должна быть [[nodiscard]] (драйвер '
                    'использует её результат).',
       'starter': '#include <stdio.h>\n'
                  '#include <stdlib.h>\n'
                  '\n'
                  'static void debug_dump(int x) {\n'
                  '    printf("dump %d\\n", x);\n'
                  '}\n'
                  '\n'
                  'void fatal(const char *msg) {\n'
                  '    printf("fatal: %s\\n", msg);\n'
                  '    exit(0);\n'
                  '}\n'
                  '\n'
                  'int on_event(int code, void *ctx) {\n'
                  '    return code * 2;\n'
                  '}\n'
                  '\n'
                  'int checked_div(int a, int b) {\n'
                  '    if (b == 0) fatal("division by zero");\n'
                  '    return a / b;\n'
                  '}\n'
                  '\n'
                  'int classify(int x) {\n'
                  '    int r = 0;\n'
                  '    switch (x) {\n'
                  '    case 0:\n'
                  '        r = 10;\n'
                  '    case 1:\n'
                  '        r += 1;\n'
                  '        break;\n'
                  '    default:\n'
                  '        r = -1;\n'
                  '    }\n'
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
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%d %d %d\\n", classify(0), classify(1), classify(5));\n'
                 '    printf("%d %d\\n", on_event(21, NULL), on_event(-1, NULL));\n'
                 '    int q = checked_div(84, 2);\n'
                 '    printf("%d\\n", q);\n'
                 '    int r = checked_div(1, 0);\n'
                 '    printf("unreachable %d\\n", r);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': '[[fallthrough]]; перед case, [[maybe_unused]] для параметра и статической функции, '
               '[[noreturn]] у fatal, [[nodiscard]] у checked_div. (Программа в конце вызывает fatal, '
               'которая завершает её штатно — это ожидаемо.)',
       'flags': '-std=c23 -O1 -g0 -Wall -Wextra -Werror -Wimplicit-fallthrough -Wunused-parameter '
                '-Wunused-function',
       'expected': ['11 1 -1', '42 -2', '42', 'fatal: division by zero']},
      {'id': 'c14-ckd-arith',
       'mode': 'c',
       'title': 'stdckdint.h: арифметика с проверкой переполнения',
       'statement': 'Используйте <stdckdint.h> (C23): ckd_add, ckd_sub, ckd_mul (возвращают true при '
                    'переполнении, результат пишут по первому адресу). add_u32(a, b, *out) → 0 при успехе, '
                    '−1 при переполнении uint32_t; sub_size(a, b, *out) для size_t (a − b < 0 — '
                    'переполнение); sum_checked(a, n, *out) → 0/−1 для int; factorial(n, *out) → n! для '
                    'uint64_t (−1, если переполнение; n ≥ 0), pow_checked(base, exp, *out) для int64_t; '
                    'alloc_size(count, elem, extra, *out) → count · elem + extra как size_t (−1 при '
                    'переполнении) — для выделения памяти; mixed_add(int8_t a, uint8_t b, *out int16_t) → '
                    '0/−1 — результат вписывается в int16_t при разных типах.',
       'starter': '#include <stddef.h>\n'
                  '#include <stdint.h>\n'
                  '\n'
                  'int add_u32(uint32_t a, uint32_t b, uint32_t *out) { return -9; }\n'
                  'int sub_size(size_t a, size_t b, size_t *out) { return -9; }\n'
                  'int sum_checked(const int *a, int n, int *out) { return -9; }\n'
                  'int factorial(int n, uint64_t *out) { return -9; }\n'
                  'int pow_checked(int64_t base, int exp, int64_t *out) { return -9; }\n'
                  'int alloc_size(size_t count, size_t elem, size_t extra, size_t *out) { return -9; }\n'
                  'int mixed_add(int8_t a, uint8_t b, int16_t *out) { return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    uint32_t u = 7;\n'
                 '    int r1 = add_u32(4000000000u, 294967295u, &u);\n'
                 '    printf("%d %u | ", r1, u);\n'
                 '    r1 = add_u32(4000000000u, 294967296u, &u);\n'
                 '    printf("%d %u | ", r1, u);\n'
                 '    r1 = add_u32(0, 0, &u);\n'
                 '    printf("%d %u\\n", r1, u);\n'
                 '    size_t z = 77;\n'
                 '    int s1 = sub_size(10, 3, &z);\n'
                 '    printf("%d %zu ", s1, z);\n'
                 '    int s2 = sub_size(3, 10, &z);\n'
                 '    printf("%d %zu\\n", s2, z);\n'
                 '    int a[] = {INT_MAX - 5, 3, 2}, r = 0;\n'
                 '    int c1 = sum_checked(a, 3, &r);\n'
                 '    printf("%d %d ", c1, r);\n'
                 '    int c2 = sum_checked(a, 2, &r);\n'
                 '    printf("%d %d ", c2, r);\n'
                 '    int neg[] = {INT_MIN, -1};\n'
                 '    int c3 = sum_checked(neg, 2, &r);\n'
                 '    printf("%d %d\\n", c3, r);\n'
                 '    uint64_t f = 0;\n'
                 '    int f1 = factorial(20, &f);\n'
                 '    printf("%d %llu ", f1, (unsigned long long)f);\n'
                 '    int f2 = factorial(21, &f);\n'
                 '    printf("%d %llu\\n", f2, (unsigned long long)f);\n'
                 '    int64_t p = 0;\n'
                 '    int p1 = pow_checked(2, 62, &p);\n'
                 '    printf("%d %lld ", p1, (long long)p);\n'
                 '    int p2 = pow_checked(2, 63, &p);\n'
                 '    printf("%d %lld ", p2, (long long)p);\n'
                 '    int p3 = pow_checked(-2, 63, &p);\n'
                 '    printf("%d %lld ", p3, (long long)p);\n'
                 '    int p4 = pow_checked(10, 0, &p);\n'
                 '    printf("%d %lld\\n", p4, (long long)p);\n'
                 '    size_t as = 0;\n'
                 '    int a1 = alloc_size(1000, 8, 16, &as);\n'
                 '    printf("%d %zu ", a1, as);\n'
                 '    int a2 = alloc_size(SIZE_MAX / 2, 3, 0, &as);\n'
                 '    printf("%d ", a2);\n'
                 '    int a3 = alloc_size(SIZE_MAX / 8, 8, 100, &as);\n'
                 '    printf("%d\\n", a3);\n'
                 '    int16_t m = 0;\n'
                 '    int m1 = mixed_add(127, 255, &m);\n'
                 '    printf("%d %d ", m1, m);\n'
                 '    int m2 = mixed_add(-128, 0, &m);\n'
                 '    printf("%d %d ", m2, m);\n'
                 '    int m3 = mixed_add(-128, 255, &m);\n'
                 '    printf("%d %d\\n", m3, m);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'if (ckd_add(&r, a, b)) return −1; — тип результата определяет r, а не операнды. Записывайте '
               'в *out только при успехе.',
       'flags': '-std=c23 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 4294967295 | -1 4294967295 | 0 0',
                    '0 7 -1 7',
                    '0 2147483647 0 2147483645 -1 2147483645',
                    '0 2432902008176640000 -1 2432902008176640000',
                    '0 4611686018427387904 -1 4611686018427387904 0 -9223372036854775808 0 1',
                    '0 8016 -1 -1',
                    '0 382 0 -128 0 127']},
      {'id': 'c14-stdbit-utils',
       'mode': 'c',
       'title': 'stdbit.h: битовые функции C23',
       'statement': 'Используйте <stdbit.h> (C23): stdc_count_ones, stdc_count_zeros, stdc_leading_zeros, '
                    'stdc_trailing_zeros, stdc_first_leading_one / stdc_first_trailing_one, stdc_bit_width, '
                    'stdc_bit_floor, stdc_bit_ceil, stdc_has_single_bit. popcount32(x), parity(x) (1, если '
                    'число единиц нечётно), ctz32(x) (для 0 — 32), clz32(x) (для 0 — 32), ilog2(x) (для x > '
                    '0, иначе −1), next_pow2(x) (для 0 → 1; если не помещается в 32 бита — 0), prev_pow2(x) '
                    '(для 0 → 0), is_pow2(x), bit_width64(x) → сколько бит нужно для записи x (0 → 0), '
                    'rotl32(x, r), rotr32(x, r) через stdc_rotate_left / stdc_rotate_right (r любое '
                    'неотрицательное)? — нет: в стандарте таких функций нет, поэтому rotl32 и rotr32 пишите '
                    'сами, без UB при r = 0 или r ≥ 32.',
       'starter': '#include <stdint.h>\n'
                  '\n'
                  'int popcount32(uint32_t x) { return -1; }\n'
                  'int parity(uint32_t x) { return -1; }\n'
                  'int ctz32(uint32_t x) { return -1; }\n'
                  'int clz32(uint32_t x) { return -1; }\n'
                  'int ilog2(uint32_t x) { return -9; }\n'
                  'uint32_t next_pow2(uint32_t x) { return 7; }\n'
                  'uint32_t prev_pow2(uint32_t x) { return 7; }\n'
                  'int is_pow2(uint32_t x) { return -1; }\n'
                  'int bit_width64(uint64_t x) { return -1; }\n'
                  'uint32_t rotl32(uint32_t x, unsigned r) { return 7; }\n'
                  'uint32_t rotr32(uint32_t x, unsigned r) { return 7; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    uint32_t v[] = {0, 1, 2, 3, 255, 256, 0x80000000u, 0xFFFFFFFFu, 12345678u};\n'
                 '    for (int i = 0; i < 9; i++) {\n'
                 '        uint32_t x = v[i];\n'
                 '        printf("%#x: pop=%d par=%d ctz=%d clz=%d lg=%d pow2=%d np=%u pp=%u\\n", x, '
                 'popcount32(x), parity(x), ctz32(x), clz32(x), ilog2(x), is_pow2(x), next_pow2(x), '
                 'prev_pow2(x));\n'
                 '    }\n'
                 '    printf("%u %u %u\\n", next_pow2(0x80000001u), next_pow2(0x7FFFFFFFu), '
                 'next_pow2(1000));\n'
                 '    printf("%d %d %d %d\\n", bit_width64(0), bit_width64(1), bit_width64(255), '
                 'bit_width64(0xFFFFFFFFFFFFFFFFULL));\n'
                 '    printf("%#x %#x %#x %#x\\n", rotl32(0x80000001u, 1), rotl32(0x12345678u, 0), '
                 'rotl32(0x12345678u, 36), rotr32(0x12345678u, 4));\n'
                 '    printf("%#x %#x\\n", rotr32(0x80000001u, 33), rotr32(1, 32));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Каждая функция — тонкая обёртка над stdc_*: stdc_count_ones, stdc_trailing_zeros, '
               'stdc_leading_zeros, stdc_bit_width, stdc_bit_ceil, stdc_bit_floor, stdc_has_single_bit. Для '
               'поворотов — свой код.',
       'flags': '-std=c23 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0: pop=0 par=0 ctz=32 clz=32 lg=-1 pow2=0 np=1 pp=0',
                    '0x1: pop=1 par=1 ctz=0 clz=31 lg=0 pow2=1 np=1 pp=1',
                    '0x2: pop=1 par=1 ctz=1 clz=30 lg=1 pow2=1 np=2 pp=2',
                    '0x3: pop=2 par=0 ctz=0 clz=30 lg=1 pow2=0 np=4 pp=2',
                    '0xff: pop=8 par=0 ctz=0 clz=24 lg=7 pow2=0 np=256 pp=128',
                    '0x100: pop=1 par=1 ctz=8 clz=23 lg=8 pow2=1 np=256 pp=256',
                    '0x80000000: pop=1 par=1 ctz=31 clz=0 lg=31 pow2=1 np=2147483648 pp=2147483648',
                    '0xffffffff: pop=32 par=0 ctz=0 clz=0 lg=31 pow2=0 np=0 pp=2147483648',
                    '0xbc614e: pop=12 par=0 ctz=1 clz=8 lg=23 pow2=0 np=16777216 pp=8388608',
                    '0 2147483648 1024',
                    '0 1 8 64',
                    '0x3 0x12345678 0x23456781 0x81234567',
                    '0xc0000000 0x1']},
      {'id': 'c14-typed-enum-flags',
       'mode': 'c',
       'title': 'enum с базовым типом и битовые флаги',
       'statement': 'enum perm : uint8_t { P_NONE = 0, P_READ = 1, P_WRITE = 2, P_EXEC = 4, P_ALL = 7 } '
                    '(C23: фиксированный базовый тип); enum level : int8_t { L_LOW = -1, L_MID = 0, L_HIGH = '
                    '1 }. perm_has(p, flag) → 1/0; perm_add(p, flag), perm_remove(p, flag), perm_toggle(p, '
                    'flag) → новое значение; perm_str(p, out) → «rwx» (отсутствующие права — «-», например '
                    '«r-x»); perm_parse(s) → права из строки вида «rwx», «r--», «-w-» (неверная строка → '
                    '−1); perm_count(p) — число прав; level_clamp(int v) → ближайший level из диапазона; '
                    'sizes(out) → записать в out sizeof(enum perm) и sizeof(enum level) (по условию — 1 и '
                    '1).',
       'starter': '#include <stdint.h>\n'
                  '\n'
                  'enum perm : uint8_t { P_NONE = 0, P_READ = 1, P_WRITE = 2, P_EXEC = 4, P_ALL = 7 };\n'
                  'enum level : int8_t { L_LOW = -1, L_MID = 0, L_HIGH = 1 };\n'
                  '\n'
                  'int perm_has(enum perm p, enum perm flag) { return -1; }\n'
                  'enum perm perm_add(enum perm p, enum perm flag) { return p; }\n'
                  'enum perm perm_remove(enum perm p, enum perm flag) { return p; }\n'
                  'enum perm perm_toggle(enum perm p, enum perm flag) { return p; }\n'
                  'void perm_str(enum perm p, char *out) { out[0] = 0; }\n'
                  'int perm_parse(const char *s) { return -2; }\n'
                  'int perm_count(enum perm p) { return -1; }\n'
                  'enum level level_clamp(int v) { return L_MID; }\n'
                  'void sizes(unsigned *out) { out[0] = out[1] = 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    enum perm p = P_READ;\n'
                 '    p = perm_add(p, P_EXEC);\n'
                 '    char s[8];\n'
                 '    perm_str(p, s);\n'
                 '    printf("%d %s %d %d\\n", p, s, perm_has(p, P_READ), perm_has(p, P_WRITE));\n'
                 '    p = perm_toggle(p, P_WRITE);\n'
                 '    perm_str(p, s);\n'
                 '    printf("%d %s %d\\n", p, s, perm_count(p));\n'
                 '    p = perm_remove(p, P_READ | P_EXEC);\n'
                 '    perm_str(p, s);\n'
                 '    printf("%d %s\\n", p, s);\n'
                 '    printf("%d %d %d\\n", perm_has(P_ALL, P_READ | P_WRITE), perm_has(P_READ, P_READ | '
                 'P_WRITE), perm_has(P_ALL, P_NONE));\n'
                 '    printf("%d %d %d %d %d %d\\n", perm_parse("rwx"), perm_parse("r--"), '
                 'perm_parse("-w-"), perm_parse("---"), perm_parse("rw"), perm_parse("rwz"));\n'
                 '    printf("%d %d %d\\n", perm_count(P_NONE), perm_count(P_ALL), perm_count(P_WRITE));\n'
                 '    printf("%d %d %d %d %d\\n", level_clamp(-100), level_clamp(-1), level_clamp(0), '
                 'level_clamp(1), level_clamp(100));\n'
                 '    unsigned sz[2];\n'
                 '    sizes(sz);\n'
                 '    printf("%u %u %zu\\n", sz[0], sz[1], sizeof(enum perm));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'enum perm : uint8_t — базовый тип задан явно, поэтому sizeof равен 1. Битовые операции '
               'приводите обратно к (enum perm), маскируя P_ALL.',
       'flags': '-std=c23 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['5 r-x 1 0',
                    '7 rwx 3',
                    '2 -w-',
                    '1 0 0',
                    '7 1 2 0 -1 -1',
                    '0 3 1',
                    '-1 -1 0 1 1',
                    '1 1 1']},
      {'id': 'c14-bitint',
       'mode': 'c',
       'title': '_BitInt: целые произвольной ширины',
       'statement': 'Используйте _BitInt(N) (C23, gcc 14+): adc_add(a, b) — сложение 12-битных беззнаковых '
                    'отсчётов АЦП (unsigned _BitInt(12)) с переполнением по модулю 4096 (параметры и '
                    'результат — uint16_t); adc_to_mv(x) — перевод 12-битного значения в милливольты (x · '
                    '3300 / 4095, округление вниз) через _BitInt(24); sample24_sat_add(a, b) — сложение '
                    'знаковых 24-битных отсчётов звука (int32_t в диапазоне −8388608…8388607) с насыщением; '
                    'sample24_mul(a, b, shift) — произведение отсчётов с правым арифметическим сдвигом на '
                    'shift (до 24 бит) без переполнения (через _BitInt(48)); counter48_inc(c, n) — 48-битный '
                    'счётчик (uint64_t в младших 48 битах) с переходом через 0; bits_needed(x) — наименьшее '
                    'число бит (1…64) для записи беззнакового x (0 — 1 бит).',
       'starter': '#include <stdint.h>\n'
                  '\n'
                  'uint16_t adc_add(uint16_t a, uint16_t b) { return 0; }\n'
                  'uint32_t adc_to_mv(uint16_t x) { return 0; }\n'
                  'int32_t sample24_sat_add(int32_t a, int32_t b) { return 0; }\n'
                  'int32_t sample24_mul(int32_t a, int32_t b, int shift) { return 0; }\n'
                  'uint64_t counter48_inc(uint64_t c, uint64_t n) { return 0; }\n'
                  'int bits_needed(uint64_t x) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%u %u %u %u\\n", adc_add(1000, 2000), adc_add(4000, 200), adc_add(4095, 1), '
                 'adc_add(0, 0));\n'
                 '    printf("%u %u %u %u\\n", adc_to_mv(0), adc_to_mv(4095), adc_to_mv(2048), '
                 'adc_to_mv(1));\n'
                 '    printf("%d %d %d %d\\n", sample24_sat_add(8000000, 1000000), '
                 'sample24_sat_add(-8000000, -1000000), sample24_sat_add(100, -300), '
                 'sample24_sat_add(8388607, 1));\n'
                 '    printf("%d %d %d\\n", sample24_mul(1000, 2000, 0), sample24_mul(8388607, 8388607, 23), '
                 'sample24_mul(-8388608, 8388607, 23));\n'
                 '    printf("%d %d\\n", sample24_mul(8388607, 8388607, 0), sample24_mul(-1000, 3, 1));\n'
                 '    printf("%llu %llu %llu\\n", (unsigned long long)counter48_inc(0, 1), (unsigned long '
                 'long)counter48_inc(0xFFFFFFFFFFFFULL, 1), (unsigned long '
                 'long)counter48_inc(0xFFFFFFFFFFFEULL, 5));\n'
                 '    printf("%d %d %d %d %d %d\\n", bits_needed(0), bits_needed(1), bits_needed(255), '
                 'bits_needed(256), bits_needed(0x8000000000000000ULL), '
                 'bits_needed(0xFFFFFFFFFFFFFFFFULL));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'unsigned _BitInt(12) x = a; x + y автоматически сворачивается по модулю 4096 при '
               'присваивании в тип той же ширины. Для сложения 24-битных значений без потерь берите '
               '_BitInt(26) или шире.',
       'flags': '-std=c23 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['3000 104 0 0',
                    '0 3300 1650 0',
                    '8388607 -8388608 -200 8388607',
                    '2000000 8388606 -8388607',
                    '8388607 -1500',
                    '1 0 3',
                    '1 1 8 9 64 64']},
      {'id': 'c14-va-opt-logging',
       'mode': 'c',
       'title': 'Макросы журнала: __VA_OPT__ и условная компиляция C23',
       'statement': 'С -std=c23 макрос LOG(fmt, ...) должен работать и без дополнительных аргументов: '
                    'LOG("start") и LOG("x=%d", 5) — оба печатают «[LOG] <сообщение>\\n» (используйте '
                    '__VA_OPT__). LOGF(level, fmt, ...) — то же с уровнем: «[<level>] …». COUNT(...) → число '
                    'аргументов (0…4) через __VA_OPT__ и вспомогательные макросы. Условная компиляция: '
                    'feature_name() → «has-embed», если определено __has_embed; иначе «has-include», если '
                    'определено __has_include и существует <stdio.h> (__has_include(<stdio.h>)); иначе '
                    '«plain». fn_mode() → «debug», если определён макрос DEBUG; «release», если определён '
                    'RELEASE; иначе «default» (директивы #ifdef / #elifdef / #else). Сами определите в '
                    'исходнике #define RELEASE 1, а DEBUG не определяйте.',
       'starter': '#include <stdio.h>\n'
                  '\n'
                  '#define LOG(fmt, ...)\n'
                  '#define LOGF(level, fmt, ...)\n'
                  '#define COUNT(...) 0\n'
                  '\n'
                  'const char *feature_name(void) { return ""; }\n'
                  'const char *fn_mode(void) { return ""; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    LOG("start");\n'
                 '    LOG("x=%d", 5);\n'
                 '    LOG("%s and %s", "a", "b");\n'
                 '    LOGF("WARN", "disk %d%%", 93);\n'
                 '    LOGF("INFO", "plain");\n'
                 '    printf("%d %d %d %d %d\\n", COUNT(), COUNT(a), COUNT(a, b), COUNT(a, b, c), COUNT(a, '
                 'b, c, d));\n'
                 '    printf("%s %s\\n", feature_name(), fn_mode());\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'printf("[LOG] " fmt "\\n" __VA_OPT__(,) __VA_ARGS__): запятая появляется только при наличии '
               'аргументов. COUNT: подсчёт сдвигом списка с __VA_OPT__ для пустого случая.',
       'flags': '-std=c23 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['[LOG] start',
                    '[LOG] x=5',
                    '[LOG] a and b',
                    '[WARN] disk 93%',
                    '[INFO] plain',
                    '0 1 2 3 4',
                    'has-include release']},
      {'id': 'c14-vec-templates',
       'mode': 'c',
       'title': '«Шаблоны» на макросах и _Generic: вектор для любого типа',
       'statement': 'Макрос VEC_DEFINE(T, name) генерирует тип struct vec_<name> { T *data; size_t len, cap; '
                    '} и функции vec_<name>_init(v), vec_<name>_push(v, x) → 0/−1 (ёмкость 4, рост вдвое), '
                    'vec_<name>_get(v, i) → значение (индекс должен быть < len), vec_<name>_pop(v, *out) → '
                    '1/0, vec_<name>_free(v). Сделайте определения для int (name int), double (name double) '
                    'и char (name char). Макрос VEC_PUSH(v, x) выбирает нужную функцию по типу вектора через '
                    '_Generic: vec_int_push для struct vec_int *, и так далее; VEC_LEN(v) — длина (для '
                    'любого вектора); VEC_FOR(i, v) — цикл по индексам. sum_ints(v) → сумма вектора int, '
                    'mean_doubles(v) → среднее вектора double (0.0 для пустого), to_string(v, out) → вектор '
                    'char как строка. Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '#include <stdlib.h>\n'
                  '\n'
                  '#define VEC_DEFINE(T, name)\n'
                  '#define VEC_PUSH(v, x) (-1)\n'
                  '#define VEC_LEN(v) ((size_t)0)\n'
                  '#define VEC_FOR(i, v) for (size_t i = 0; i < 0; i++)\n'
                  '\n'
                  'long sum_ints(void *v) { return 0; }\n'
                  'double mean_doubles(void *v) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct vec_int vi;\n'
                 '    struct vec_double vd;\n'
                 '    struct vec_char vc;\n'
                 '    vec_int_init(&vi);\n'
                 '    vec_double_init(&vd);\n'
                 '    vec_char_init(&vc);\n'
                 '    for (int i = 1; i <= 10; i++) VEC_PUSH(&vi, i * i);\n'
                 '    for (int i = 0; i < 5; i++) VEC_PUSH(&vd, i + 0.5);\n'
                 '    for (const char *p = "hello"; *p; p++) VEC_PUSH(&vc, *p);\n'
                 '    printf("%zu %zu %zu %zu %zu\\n", VEC_LEN(&vi), VEC_LEN(&vd), VEC_LEN(&vc), vi.cap, '
                 'vc.cap);\n'
                 '    printf("%ld %.2f\\n", sum_ints(&vi), mean_doubles(&vd));\n'
                 '    char s[16];\n'
                 '    to_string(&vc, s);\n'
                 '    printf("%s %d %g %d\\n", s, vec_int_get(&vi, 3), vec_double_get(&vd, 4), '
                 'vec_char_get(&vc, 1));\n'
                 '    int x;\n'
                 '    int pops = 0;\n'
                 '    while (vec_int_pop(&vi, &x)) pops += x == (10 - pops) * (10 - pops);\n'
                 '    printf("%d %zu\\n", pops, VEC_LEN(&vi));\n'
                 '    struct vec_double e;\n'
                 '    vec_double_init(&e);\n'
                 '    printf("%.1f %d\\n", mean_doubles(&e), vec_double_pop(&e, &(double){0}));\n'
                 '    size_t cnt = 0;\n'
                 '    VEC_FOR(i, &vc) cnt += (size_t)vc.data[i];\n'
                 '    printf("%zu\\n", cnt);\n'
                 '    vec_int_free(&vi);\n'
                 '    vec_double_free(&vd);\n'
                 '    vec_char_free(&vc);\n'
                 '    vec_double_free(&e);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Генератор — один макрос с вызовами ##name; VEC_PUSH — _Generic по типу указателя на вектор с '
               'выбором функции и вызовом (v, x). В VEC_FOR используйте v->len.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['10 5 5 16 8', '385 2.50', 'hello 16 4.5 101', '10 0', '0.0 0', '532']},
      {'id': 'c14-thread-local',
       'mode': 'c',
       'title': '_Thread_local и потоки <threads.h>',
       'statement': '_Thread_local int tl_counter — у каждого потока своя копия. tl_inc() → увеличить копию '
                    'текущего потока и вернуть новое значение; tl_get(); tl_reset(). run_threads(n, iters, '
                    'results) — запустить n потоков (n ≤ 8), каждый вызывает tl_inc() iters раз и возвращает '
                    'итог своей копии (результат записывается в results[i]); главный поток после этого '
                    'проверяет, что его собственная копия не изменилась; возвращает 0 при успехе, −1 при '
                    'ошибке создания потока. shared_sum(n, iters) → сумма результатов потоков, где каждый '
                    'поток прибавляет свои значения к общему atomic_long (через atomic_fetch_add) — '
                    'проверка, что итог точен: n · iters. thread_ids_distinct(n) → 1, если у n потоков '
                    'thrd_current() попарно различны (сравнивайте через thrd_equal).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int tl_inc(void) { return -1; }\n'
                  'int tl_get(void) { return -1; }\n'
                  'void tl_reset(void) {}\n'
                  'int run_threads(int n, int iters, int *results) { return -9; }\n'
                  'long shared_sum(int n, int iters) { return -1; }\n'
                  'int thread_ids_distinct(int n) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    printf("%d %d %d\\n", tl_inc(), tl_inc(), tl_get());\n'
                 '    int res[8] = {0};\n'
                 '    int rc = run_threads(4, 1000, res);\n'
                 '    printf("%d: %d %d %d %d | main=%d\\n", rc, res[0], res[1], res[2], res[3], tl_get());\n'
                 '    tl_reset();\n'
                 '    printf("%d %d\\n", tl_get(), tl_inc());\n'
                 '    rc = run_threads(1, 5, res);\n'
                 '    printf("%d %d %d\\n", rc, res[0], tl_get());\n'
                 '    printf("%ld %ld\\n", shared_sum(4, 25000), shared_sum(8, 1000));\n'
                 '    printf("%d %d\\n", thread_ids_distinct(2), thread_ids_distinct(6));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'static _Thread_local int tl_counter; каждый поток обнуляет и считает свою копию; главный '
               'поток свою не трогает. Общий счётчик — atomic_long и atomic_fetch_add.',
       'flags': '-std=c11 -pthread -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 2 2', '0: 1000 1001 1002 1003 | main=2', '0 1', '0 5 1', '100000 8000', '1 1']},
      {'id': 'c14-flexible-matrix',
       'mode': 'c',
       'title': 'Матрица на гибком члене массива',
       'statement': 'struct mat { int rows, cols; double d[]; } — элементы подряд построчно в хвосте. '
                    'mat_new(r, c) → матрица, заполненная нулями (r, c ≥ 1; иначе NULL); mat_get(m, i, j), '
                    'mat_set(m, i, j, v); mat_identity(n); mat_mul(a, b) → a·b (NULL, если размеры не '
                    'согласованы); mat_transpose(m); mat_trace(m) (для квадратной, иначе 0); mat_equal(a, b, '
                    'eps) → 1/0; mat_clone(m); mat_free(m); mat_pow(m, k) → m^k для квадратной (k ≥ 0, k = 0 '
                    '— единичная) быстрым возведением. Под AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct mat { int rows, cols; double d[]; };\n'
                  '\n'
                  'struct mat *mat_new(int r, int c) { return 0; }\n'
                  'double mat_get(const struct mat *m, int i, int j) { return 0; }\n'
                  'void mat_set(struct mat *m, int i, int j, double v) {}\n'
                  'struct mat *mat_identity(int n) { return 0; }\n'
                  'struct mat *mat_mul(const struct mat *a, const struct mat *b) { return 0; }\n'
                  'struct mat *mat_transpose(const struct mat *m) { return 0; }\n'
                  'double mat_trace(const struct mat *m) { return 0; }\n'
                  'int mat_equal(const struct mat *a, const struct mat *b, double eps) { return -1; }\n'
                  'struct mat *mat_clone(const struct mat *m) { return 0; }\n'
                  'struct mat *mat_pow(const struct mat *m, unsigned k) { return 0; }\n'
                  'void mat_free(struct mat *m) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'static void show(const struct mat *m) {\n'
                 '    for (int i = 0; i < m->rows; i++) {\n'
                 '        for (int j = 0; j < m->cols; j++) printf("%g ", mat_get(m, i, j));\n'
                 '        printf("| ");\n'
                 '    }\n'
                 '    printf("\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct mat *a = mat_new(2, 3), *b = mat_new(3, 2);\n'
                 '    for (int i = 0; i < 2; i++) for (int j = 0; j < 3; j++) { mat_set(a, i, j, i * 3 + j + '
                 '1); mat_set(b, j, i, (j + 1) * (i + 1)); }\n'
                 '    show(a);\n'
                 '    show(b);\n'
                 '    struct mat *c = mat_mul(a, b);\n'
                 '    show(c);\n'
                 '    printf("%g %d %d\\n", mat_trace(c), mat_mul(a, a) == NULL, mat_new(0, 3) == NULL);\n'
                 '    struct mat *t = mat_transpose(a);\n'
                 '    show(t);\n'
                 '    struct mat *tt = mat_transpose(t);\n'
                 '    printf("%d %d\\n", mat_equal(a, tt, 0), mat_equal(a, t, 0));\n'
                 '    struct mat *f = mat_new(2, 2);\n'
                 '    mat_set(f, 0, 0, 1); mat_set(f, 0, 1, 1); mat_set(f, 1, 0, 1);\n'
                 '    struct mat *f10 = mat_pow(f, 10), *f0 = mat_pow(f, 0), *f1 = mat_pow(f, 1);\n'
                 '    show(f10);\n'
                 '    show(f0);\n'
                 '    printf("%d\\n", mat_equal(f1, f, 1e-12));\n'
                 '    struct mat *i3 = mat_identity(3), *cl = mat_clone(a);\n'
                 '    printf("%g %d\\n", mat_trace(i3), mat_equal(cl, a, 0));\n'
                 '    mat_set(cl, 0, 0, 99);\n'
                 '    printf("%g %g\\n", mat_get(a, 0, 0), mat_get(cl, 0, 0));\n'
                 '    struct mat *p = mat_pow(a, 2);\n'
                 '    printf("%d\\n", p == NULL);\n'
                 '    struct mat *all[] = {a, b, c, t, tt, f, f10, f0, f1, i3, cl};\n'
                 '    for (int i = 0; i < 11; i++) mat_free(all[i]);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Один блок: calloc(1, sizeof *m + r·c·sizeof(double)). Для клона копируйте весь блок (memcpy '
               'с учётом хвоста), а не только структуру.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 2 3 | 4 5 6 |',
                    '1 2 | 2 4 | 3 6 |',
                    '14 28 | 32 64 |',
                    '78 1 1',
                    '1 4 | 2 5 | 3 6 |',
                    '1 0',
                    '89 55 | 55 34 |',
                    '1 0 | 0 1 |',
                    '1',
                    '3 1',
                    '1 99',
                    '1']},
      {'id': 'c14-typeof-macros',
       'mode': 'c',
       'title': 'typeof в стандарте C23: безопасные макросы',
       'statement': 'Только стандартные средства C23 (typeof, auto, constexpr; без выражений-операторов GNU '
                    '— они запрещены в тексте программы: «({»): SWAP(a, b) — обмен двух переменных одного '
                    'типа (do { … } while (0), временная переменная typeof(a)); ARRAY_LEN(a) → число '
                    'элементов массива (size_t); CLAMP(x, lo, hi) (каждый аргумент — переменная или '
                    'константа без побочных эффектов; тип результата — тип x); IS_SAME_TYPE(a, b) → 1, если '
                    'typeof(a) и typeof(b) один и тот же тип (через _Generic по __typeof__ или typeof); '
                    'SIGN(x) → −1, 0, 1 для любого арифметического типа; ABS(x) — модуль для int/long/double '
                    'через _Generic. clamp_array(a, n, lo, hi) — ограничить все элементы int массива.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  '#define SWAP(a, b)\n'
                  '#define ARRAY_LEN(a) ((size_t)0)\n'
                  '#define CLAMP(x, lo, hi) (x)\n'
                  '#define IS_SAME_TYPE(a, b) 0\n'
                  '#define SIGN(x) 0\n'
                  '#define ABS(x) (x)\n'
                  '\n'
                  'void clamp_array(int *a, size_t n, int lo, int hi) {}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
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
                 '    int a = 1, b = 2;\n'
                 '    SWAP(a, b);\n'
                 '    double d = 1.5, e = 2.5;\n'
                 '    SWAP(d, e);\n'
                 '    char *p = "left", *q = "right";\n'
                 '    SWAP(p, q);\n'
                 '    printf("%d %d %g %g %s %s\\n", a, b, d, e, p, q);\n'
                 '    int arr[7];\n'
                 '    double darr[3];\n'
                 '    printf("%zu %zu %zu\\n", ARRAY_LEN(arr), ARRAY_LEN(darr), ARRAY_LEN("hello"));\n'
                 '    int x = 15, lo = 0, hi = 10;\n'
                 '    double y = -0.5;\n'
                 '    printf("%d %g %d\\n", CLAMP(x, lo, hi), CLAMP(y, 0.0, 1.0), CLAMP(5, 1, 9));\n'
                 '    long l = 5;\n'
                 '    printf("%d %d %d %d\\n", IS_SAME_TYPE(a, b), IS_SAME_TYPE(a, l), IS_SAME_TYPE(d, a), '
                 'IS_SAME_TYPE(p, q));\n'
                 '    printf("%d %d %d %d %d\\n", SIGN(-7), SIGN(0), SIGN(3L), SIGN(-0.5), SIGN(2.5f));\n'
                 '    printf("%d %ld %g\\n", ABS(-3), ABS(-4L), ABS(-2.5));\n'
                 '    int v[] = {-5, 3, 12, 7, 20};\n'
                 '    clamp_array(v, ARRAY_LEN(v), 0, 10);\n'
                 '    printf("%d %d %d %d %d\\n", v[0], v[1], v[2], v[3], v[4]);\n'
                 '    printf("gnu: %d\\n", src_count("(" "{"));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'SWAP: do { typeof(a) _t = (a); (a) = (b); (b) = _t; } while (0). Сравнение типов: '
               '_Generic((typeof(a) *)0, typeof(b) *: 1, default: 0).',
       'flags': '-std=c23 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['2 1 2.5 1.5 right left',
                    '7 3 6',
                    '10 0 5',
                    '1 0 0 1',
                    '-1 0 1 -1 1',
                    '3 4 2.5',
                    '0 3 10 7 10',
                    'gnu: 0']},
      {'id': 'c14-feature-table',
       'mode': 'c',
       'title': 'Какая возможность с какой редакции: таблица и проверка',
       'statement': 'Редакции задаются значением __STDC_VERSION__: C89 → 0 (макрос не определён), C95 → '
                    '199409, C99 → 199901, C11 → 201112, C17 → 201710, C23 → 202311. std_name(ver) → «C89», '
                    '«C95», «C99», «C11», «C17», «C23» для точного значения, иначе по ближайшей меньшей '
                    'редакции с приставкой «>=» (например, 201500 → «>=C99»); ver < 199409 (но не 0) → '
                    '«<C95». supports(feature, ver) → 1, если возможность есть в редакции ver, 0 если нет, '
                    '−1, если возможность неизвестна. Таблица (минимальная версия): «inline» 199901, '
                    '«restrict» 199901, «bool» 199901 (макрос в stdbool; ключевое слово — «bool_keyword» '
                    '202311), «long_long» 199901, «vla» 199901 (необязательно с 201112, но поддерживается — '
                    'считать как есть), «designated_init» 199901, «compound_literal» 199901, «static_assert» '
                    '201112, «generic» 201112, «atomics» 201112, «threads» 201112, «alignas» 201112, '
                    '«noreturn» 201112, «typeof» 202311, «nullptr» 202311, «constexpr» 202311, '
                    '«binary_literal» 202311, «attributes» 202311, «embed» 202311, «ckd» 202311, «stdbit» '
                    '202311. min_std(feature) → строка с названием первой редакции («C99», «C11», «C23») или '
                    '«?»; features_added(ver, out) → список возможностей, добавленных именно в редакции ver '
                    '(по порядку таблицы), и их число.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'const char *std_name(long ver) { return "?"; }\n'
                  'int supports(const char *feature, long ver) { return -9; }\n'
                  'const char *min_std(const char *feature) { return "?"; }\n'
                  'int features_added(long ver, const char **out) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    long vs[] = {0, 199409, 199901, 201112, 201710, 202311, 199000, 200000, 201500, '
                 '202000, 300000};\n'
                 '    for (int i = 0; i < 11; i++) printf("%ld=%s ", vs[i], std_name(vs[i]));\n'
                 '    printf("\\n");\n'
                 '    const char *fs[] = {"inline", "static_assert", "typeof", "nullptr", "bool_keyword", '
                 '"threads", "nonexistent", "vla"};\n'
                 '    long chk[] = {199901, 201112, 201710, 202311};\n'
                 '    for (int f = 0; f < 8; f++) {\n'
                 '        printf("%s:", fs[f]);\n'
                 '        for (int v = 0; v < 4; v++) printf(" %d", supports(fs[f], chk[v]));\n'
                 '        printf(" %s\\n", min_std(fs[f]));\n'
                 '    }\n'
                 '    const char *out[32];\n'
                 '    long ev[] = {199901, 201112, 201710, 202311, 0};\n'
                 '    for (int i = 0; i < 5; i++) {\n'
                 '        int n = features_added(ev[i], out);\n'
                 '        printf("%ld %d:", ev[i], n);\n'
                 '        for (int k = 0; k < n && k < 4; k++) printf(" %s", out[k]);\n'
                 '        printf("\\n");\n'
                 '    }\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Таблица структур {имя, минимальная версия}; supports = ver >= min; min_std — обратное '
               'отображение числа в имя редакции; std_name для промежуточных значений берёт ближайшую '
               'меньшую.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0=C89 199409=C95 199901=C99 201112=C11 201710=C17 202311=C23 199000=<C95 200000=>=C99 '
                    '201500=>=C11 202000=>=C17 300000=>=C23',
                    'inline: 1 1 1 1 C99',
                    'static_assert: 0 1 1 1 C11',
                    'typeof: 0 0 0 1 C23',
                    'nullptr: 0 0 0 1 C23',
                    'bool_keyword: 0 0 0 1 C23',
                    'threads: 0 1 1 1 C11',
                    'nonexistent: -1 -1 -1 -1 ?',
                    'vla: 1 1 1 1 C99',
                    '199901 7: inline restrict bool long_long',
                    '201112 6: static_assert generic atomics threads',
                    '201710 0:',
                    '202311 9: typeof nullptr constexpr binary_literal',
                    '0 0:']},
      {'id': 'c14-fix-lifetime-literal',
       'mode': 'c',
       'title': 'Исправьте: время жизни составных литералов и гибких массивов',
       'statement': 'make_origin() возвращает указатель на составной литерал блока функции; make_point(x, y) '
                    '— на локальную структуру; copy_msg(m) копирует структуру с гибким членом присваиванием '
                    '(хвост не копируется); get_scores() возвращает указатель на массив из составного '
                    'литерала. Исправьте: make_origin и make_point должны возвращать структуру по значению '
                    '(struct pt make_origin(void), struct pt make_point(int, int)); get_scores — указатель '
                    'на static-массив; copy_msg — копия блока целиком (malloc + memcpy с учётом хвоста '
                    'длиной m->len + 1). Под AddressSanitizer (use-after-scope / return-local / overflow).',
       'starter': '#include <stdlib.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'struct pt { int x, y; };\n'
                  'struct msg { size_t len; char text[]; };\n'
                  '\n'
                  'const struct pt *make_origin(void) {\n'
                  '    return &(struct pt){0, 0};\n'
                  '}\n'
                  '\n'
                  'const struct pt *make_point(int x, int y) {\n'
                  '    struct pt p = {x, y};\n'
                  '    return &p;\n'
                  '}\n'
                  '\n'
                  'const int *get_scores(void) {\n'
                  '    return (const int[]){90, 80, 70};\n'
                  '}\n'
                  '\n'
                  'struct msg *copy_msg(const struct msg *m) {\n'
                  '    struct msg *c = malloc(sizeof *c + m->len + 1);\n'
                  '    *c = *m;\n'
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
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct pt o = make_origin();\n'
                 '    struct pt p = make_point(3, 4);\n'
                 '    struct pt q = make_point(-1, 7);\n'
                 '    printf("%d %d | %d %d | %d %d\\n", o.x, o.y, p.x, p.y, q.x, q.y);\n'
                 '    const int *s = get_scores();\n'
                 '    char tmp[200];\n'
                 '    memset(tmp, 0xEE, sizeof tmp);\n'
                 '    printf("%d %d %d\\n", s[0], s[1], s[2]);\n'
                 '    struct msg *m = malloc(sizeof *m + 6);\n'
                 '    m->len = 5;\n'
                 '    memcpy(m->text, "hello", 6);\n'
                 '    struct msg *c = copy_msg(m);\n'
                 "    m->text[0] = 'J';\n"
                 '    printf("%zu %s %s\\n", c->len, c->text, m->text);\n'
                 '    free(m);\n'
                 '    free(c);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Возвращайте структуры по значению; для массива — static const; копию структуры с гибким '
               'членом делайте memcpy на весь блок: sizeof *m + m->len + 1.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 0 | 3 4 | -1 7', '90 80 70', '5 hello Jello']},
      {'id': 'c14-generic-print',
       'mode': 'c',
       'title': '_Generic: универсальная печать и приведение',
       'statement': 'Макрос TYPE_NAME(x) → строка с названием типа выражения: «int», «unsigned», «long», '
                    '«double», «float», «char», «char*», «const char*», «bool» (для _Bool), «other» для '
                    'остальных (через _Generic). fmt_value(x, out) — записать в out значение выражения как '
                    'текст: int → «%d», unsigned → «%u», long → «%ld», double → «%g», char → символ в '
                    "апострофах («'a'»), const char*/char* → в кавычках; макрос PRINT_VAL(x, out) вызывает "
                    'нужную функцию (fmt_int, fmt_uint, fmt_long, fmt_double, fmt_char, fmt_str — все '
                    'объявляйте сами) по типу. to_double(x) — приведение любого арифметического значения к '
                    'double; max_of(a, b) — максимум для int/long/double (результат типа по _Generic по '
                    'обоим аргументам).',
       'starter': '#include <stdio.h>\n'
                  '\n'
                  '#define TYPE_NAME(x) "other"\n'
                  '#define PRINT_VAL(x, out) ((void)0)\n'
                  '#define to_double(x) 0.0\n'
                  '#define max_of(a, b) (a)\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '#include <stdbool.h>\n'
                 '\n'
                 'int main(void) {\n'
                 "    int i = 5; unsigned u = 7; long l = 9; double d = 1.5; float f = 2.5f; char c = 'q'; "
                 '_Bool b = 1;\n'
                 '    char buf[8] = "ab"; const char *cs = "xy";\n'
                 '    printf("%s %s %s %s %s %s %s %s %s %s\\n", TYPE_NAME(i), TYPE_NAME(u), TYPE_NAME(l), '
                 'TYPE_NAME(d), TYPE_NAME(f), TYPE_NAME(c), TYPE_NAME((char *)buf), TYPE_NAME(cs), '
                 'TYPE_NAME(b), TYPE_NAME(3LL));\n'
                 '    char o[32];\n'
                 '    PRINT_VAL(i, o); printf("%s ", o);\n'
                 '    PRINT_VAL(u, o); printf("%s ", o);\n'
                 '    PRINT_VAL(l, o); printf("%s ", o);\n'
                 '    PRINT_VAL(d, o); printf("%s ", o);\n'
                 '    PRINT_VAL(c, o); printf("%s ", o);\n'
                 '    PRINT_VAL(cs, o); printf("%s\\n", o);\n'
                 '    printf("%g %g %g\\n", to_double(i), to_double(u / 2), to_double(l * 2.5));\n'
                 '    printf("%d %ld %g %g\\n", max_of(3, 8), max_of(5L, 2L), max_of(1.5, 0.5), max_of(2, '
                 '3.5));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': '_Generic((x), int: "int", unsigned: "unsigned", ..., default: "other"). Для PRINT_VAL — '
               'выбор имени функции и сразу вызов (…)((x), (out)). Для max_of выбирайте по типу a + b.',
       'flags': '-std=c11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['int unsigned long double float char char* const char* bool other',
                    '5 7 9 1.5 \'q\' "xy"',
                    '5 3 22.5',
                    '8 5 1.5 3.5']}]}
