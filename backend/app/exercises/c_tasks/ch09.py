"""Задачи книги «От assembler к языку C»: глава 9 (код компилируется gcc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {9: [{'id': 'c9-endian',
      'mode': 'c',
      'title': 'Порядок байтов: определение и перестановка',
      'statement': 'is_little_endian() → 1/0 (проверка чтением первого байта числа); bswap16, bswap32, '
                   'bswap64 — перестановка байт сдвигами и масками (без __builtin и без приведения '
                   'указателей); read_be32(p), read_le32(p) — прочитать 32-битное число из байтов в нужном '
                   'порядке (p может быть невыровненным); write_be32(p, v), write_le32(p, v) — записать.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'int is_little_endian(void) { return -1; }\n'
                 'uint16_t bswap16(uint16_t x) { return 0; }\n'
                 'uint32_t bswap32(uint32_t x) { return 0; }\n'
                 'uint64_t bswap64(uint64_t x) { return 0; }\n'
                 'uint32_t read_be32(const unsigned char *p) { return 0; }\n'
                 'uint32_t read_le32(const unsigned char *p) { return 0; }\n'
                 'void write_be32(unsigned char *p, uint32_t v) {}\n'
                 'void write_le32(unsigned char *p, uint32_t v) {}\n',
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
                '    printf("%d\\n", is_little_endian());\n'
                '    printf("%#x %#x %#x\\n", bswap16(0x1234), bswap32(0x01020304), bswap32(0xFF));\n'
                '    printf("%#llx\\n", (unsigned long long)bswap64(0x0102030405060708ULL));\n'
                '    unsigned char buf[8] = {0xAA, 0x12, 0x34, 0x56, 0x78, 0xBB, 0, 0};\n'
                '    printf("%#x %#x\\n", read_be32(buf + 1), read_le32(buf + 1));\n'
                '    unsigned char out[6] = {0};\n'
                '    write_be32(out + 1, 0xDEADBEEF);\n'
                '    printf("%02x %02x %02x %02x %02x\\n", out[1], out[2], out[3], out[4], out[5]);\n'
                '    write_le32(out + 1, 0xDEADBEEF);\n'
                '    printf("%02x %02x %02x %02x %02x\\n", out[1], out[2], out[3], out[4], out[5]);\n'
                '    printf("%d\\n", bswap32(bswap32(0xCAFEBABE)) == 0xCAFEBABE);\n'
                '    printf("builtin: %d\\n", src_count("__bu" "iltin"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'bswap32: четыре байта сдвигами: x >> 24 | (x >> 8 & 0xFF00) | (x << 8 & 0xFF0000) | x << 24. '
              'Читать/писать — по одному байту с явными сдвигами.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['1',
                   '0x3412 0x4030201 0xff000000',
                   '0x807060504030201',
                   '0x12345678 0x78563412',
                   'de ad be ef 00',
                   'ef be ad de 00',
                   '1',
                   'builtin: 0']},
     {'id': 'c9-int-limits',
      'mode': 'c',
      'title': 'Границы целых типов без limits.h',
      'statement': 'max_signed(bits), min_signed(bits) → границы знакового типа в bits бит (1 ≤ bits ≤ 64) в '
                   'виде long long; max_unsigned(bits) → граница беззнакового (unsigned long long). '
                   'fits_signed(v, bits), fits_unsigned(v, bits) → 1, если значение v помещается в тип такой '
                   'ширины. Определять сдвигами и дополнительным кодом, без limits.h и без неопределённых '
                   'сдвигов (ширина 64 допустима).',
      'starter': 'long long max_signed(int bits) { return 0; }\n'
                 'long long min_signed(int bits) { return 0; }\n'
                 'unsigned long long max_unsigned(int bits) { return 0; }\n'
                 'int fits_signed(long long v, int bits) { return -1; }\n'
                 'int fits_unsigned(long long v, int bits) { return -1; }\n',
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
                '    int b[] = {1, 2, 7, 8, 16, 31, 32, 63, 64};\n'
                '    for (int i = 0; i < 9; i++)\n'
                '        printf("%d: %lld %lld %llu\\n", b[i], min_signed(b[i]), max_signed(b[i]), '
                'max_unsigned(b[i]));\n'
                '    printf("%d %d %d %d\\n", fits_signed(127, 8), fits_signed(128, 8), fits_signed(-128, '
                '8), fits_signed(-129, 8));\n'
                '    printf("%d %d %d %d\\n", fits_unsigned(255, 8), fits_unsigned(256, 8), '
                'fits_unsigned(-1, 8), fits_unsigned(0, 1));\n'
                '    printf("%d %d\\n", fits_signed(LLONG_MIN, 64), fits_unsigned(LLONG_MAX, 64));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'max_unsigned(bits) = (1ULL << bits) − 1, но для bits = 64 такой сдвиг неопределён — особый '
              'случай. Знаковый максимум = беззнаковый максимум для bits − 1.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['1: -1 0 1',
                   '2: -2 1 3',
                   '7: -64 63 127',
                   '8: -128 127 255',
                   '16: -32768 32767 65535',
                   '31: -1073741824 1073741823 2147483647',
                   '32: -2147483648 2147483647 4294967295',
                   '63: -4611686018427387904 4611686018427387903 9223372036854775807',
                   '64: -9223372036854775808 9223372036854775807 18446744073709551615',
                   '1 0 1 0',
                   '1 0 0 1',
                   '1 1']},
     {'id': 'c9-checked-arith',
      'mode': 'c',
      'title': 'Проверка переполнения без неопределённого поведения',
      'statement': 'add_ok(a, b, *out), sub_ok(a, b, *out), mul_ok(a, b, *out) для int → 1 и результат, если '
                   'вычисление не переполняется, иначе 0 (*out не меняется); проверка должна происходить ДО '
                   'операции — переполнение знаковых int неопределено. mul_size(a, b, *out) для size_t → 1/0 '
                   '(проверка перед malloc(a * b)); neg_ok(a, *out) — отрицание (INT_MIN нельзя), abs_ok(a, '
                   '*out).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int add_ok(int a, int b, int *out) { return -1; }\n'
                 'int sub_ok(int a, int b, int *out) { return -1; }\n'
                 'int mul_ok(int a, int b, int *out) { return -1; }\n'
                 'int mul_size(size_t a, size_t b, size_t *out) { return -1; }\n'
                 'int neg_ok(int a, int *out) { return -1; }\n'
                 'int abs_ok(int a, int *out) { return -1; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void t3(const char *n, int (*f)(int, int, int *), int a, int b) {\n'
                '    int r = 12345;\n'
                '    int ok = f(a, b, &r);\n'
                '    printf("%s(%d, %d) = %d %d\\n", n, a, b, ok, r);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    t3("add", add_ok, INT_MAX, 1);\n'
                '    t3("add", add_ok, INT_MAX, 0);\n'
                '    t3("add", add_ok, INT_MIN, -1);\n'
                '    t3("add", add_ok, INT_MIN, INT_MAX);\n'
                '    t3("add", add_ok, 100, 200);\n'
                '    t3("sub", sub_ok, INT_MIN, 1);\n'
                '    t3("sub", sub_ok, 0, INT_MIN);\n'
                '    t3("sub", sub_ok, -1, INT_MIN);\n'
                '    t3("sub", sub_ok, INT_MAX, -1);\n'
                '    t3("sub", sub_ok, 5, 7);\n'
                '    t3("mul", mul_ok, 65536, 32768);\n'
                '    t3("mul", mul_ok, 65536, 65536);\n'
                '    t3("mul", mul_ok, -65536, 32768);\n'
                '    t3("mul", mul_ok, INT_MIN, -1);\n'
                '    t3("mul", mul_ok, 46341, 46341);\n'
                '    t3("mul", mul_ok, 0, INT_MIN);\n'
                '    size_t s = 99;\n'
                '    printf("%d %zu\\n", mul_size(SIZE_MAX / 2, 2, &s), s);\n'
                '    printf("%d %zu\\n", mul_size(SIZE_MAX / 2 + 1, 2, &s), s);\n'
                '    printf("%d %zu\\n", mul_size(0, SIZE_MAX, &s), s);\n'
                '    printf("%d %zu\\n", mul_size(1000, 1000, &s), s);\n'
                '    int r = 7;\n'
                '    printf("%d %d | ", neg_ok(INT_MIN, &r), r);\n'
                '    printf("%d %d | ", neg_ok(INT_MAX, &r), r);\n'
                '    printf("%d %d\\n", abs_ok(-5, &r), r);\n'
                '    printf("%d\\n", abs_ok(INT_MIN, &r));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'add: проверьте a > INT_MAX − b (при b > 0) и a < INT_MIN − b (при b < 0) до сложения. '
              'Умножение удобно считать в long long. Для size_t: b > SIZE_MAX / a.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['add(2147483647, 1) = 0 12345',
                   'add(2147483647, 0) = 1 2147483647',
                   'add(-2147483648, -1) = 0 12345',
                   'add(-2147483648, 2147483647) = 1 -1',
                   'add(100, 200) = 1 300',
                   'sub(-2147483648, 1) = 0 12345',
                   'sub(0, -2147483648) = 0 12345',
                   'sub(-1, -2147483648) = 1 2147483647',
                   'sub(2147483647, -1) = 0 12345',
                   'sub(5, 7) = 1 -2',
                   'mul(65536, 32768) = 0 12345',
                   'mul(65536, 65536) = 0 12345',
                   'mul(-65536, 32768) = 1 -2147483648',
                   'mul(-2147483648, -1) = 0 12345',
                   'mul(46341, 46341) = 0 12345',
                   'mul(0, -2147483648) = 1 0',
                   '1 18446744073709551614',
                   '0 18446744073709551614',
                   '1 0',
                   '1 1000000',
                   '0 7 | 1 -2147483647 | 1 5',
                   '0']},
     {'id': 'c9-saturating',
      'mode': 'c',
      'title': 'Арифметика с насыщением',
      'statement': 'sat_add_i8, sat_sub_i8 (int8_t), sat_add_u8, sat_sub_u8 (uint8_t), sat_add_i32 '
                   '(int32_t), sat_mul_i32 (int32_t) — результат вместо переполнения упирается в границу '
                   'типа (−128…127, 0…255, INT32_MIN…INT32_MAX). Промежуточные вычисления не должны давать '
                   'неопределённого поведения.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'int8_t sat_add_i8(int8_t a, int8_t b) { return 0; }\n'
                 'int8_t sat_sub_i8(int8_t a, int8_t b) { return 0; }\n'
                 'uint8_t sat_add_u8(uint8_t a, uint8_t b) { return 0; }\n'
                 'uint8_t sat_sub_u8(uint8_t a, uint8_t b) { return 0; }\n'
                 'int32_t sat_add_i32(int32_t a, int32_t b) { return 0; }\n'
                 'int32_t sat_mul_i32(int32_t a, int32_t b) { return 0; }\n',
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
                '    printf("%d %d %d %d\\n", sat_add_i8(100, 27), sat_add_i8(100, 28), sat_add_i8(-100, '
                '-29), sat_add_i8(-100, -28));\n'
                '    printf("%d %d %d %d\\n", sat_sub_i8(-100, 28), sat_sub_i8(-100, 29), sat_sub_i8(100, '
                '-27), sat_sub_i8(100, -28));\n'
                '    printf("%d %d %d %d\\n", sat_add_u8(200, 55), sat_add_u8(200, 56), sat_sub_u8(10, 10), '
                'sat_sub_u8(10, 11));\n'
                '    printf("%d %d %d\\n", sat_add_i32(INT32_MAX, 1), sat_add_i32(INT32_MIN, -1), '
                'sat_add_i32(1000, -2000));\n'
                '    printf("%d %d %d %d\\n", sat_mul_i32(65536, 32767), sat_mul_i32(65536, 32768), '
                'sat_mul_i32(-65536, 32769), sat_mul_i32(INT32_MIN, -1));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Вычисляйте в более широком типе (int для 8-битных, long long для 32-битных) и ограничивайте '
              'результат.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['127 127 -128 -128',
                   '-128 -128 127 127',
                   '255 255 0 0',
                   '2147483647 -2147483648 -1000',
                   '2147418112 2147483647 -2147483648 2147483647']},
     {'id': 'c9-bit-tricks',
      'mode': 'c',
      'title': 'Битовые приёмы своими руками',
      'statement': 'Без встроенных функций __builtin_*: popcount32(x); parity32(x) → 1, если число единиц '
                   'нечётно; ctz32(x), clz32(x) (для x = 0 — 32); ilog2(x) (для x > 0; x = 0 → −1); '
                   'is_pow2(x), next_pow2(x) (для x = 0 → 1; для x > 2³¹ → 0); lowest_bit(x) — младший '
                   'единичный бит как число; rotl32(x, r), rotr32(x, r) (r любое от 0 до 63); reverse32(x) — '
                   'перестановка битов.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'int popcount32(uint32_t x) { return -1; }\n'
                 'int parity32(uint32_t x) { return -1; }\n'
                 'int ctz32(uint32_t x) { return -1; }\n'
                 'int clz32(uint32_t x) { return -1; }\n'
                 'int ilog2(uint32_t x) { return -2; }\n'
                 'int is_pow2(uint32_t x) { return -1; }\n'
                 'uint32_t next_pow2(uint32_t x) { return 7; }\n'
                 'uint32_t lowest_bit(uint32_t x) { return 7; }\n'
                 'uint32_t rotl32(uint32_t x, unsigned r) { return 7; }\n'
                 'uint32_t rotr32(uint32_t x, unsigned r) { return 7; }\n'
                 'uint32_t reverse32(uint32_t x) { return 7; }\n',
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
                '    uint32_t v[] = {0, 1, 2, 6, 255, 0x80000000u, 0xFFFFFFFFu, 0x00F00F00u, 12345678u};\n'
                '    for (int i = 0; i < 9; i++) {\n'
                '        uint32_t x = v[i];\n'
                '        printf("%#x: pop=%d par=%d ctz=%d clz=%d lg=%d pow2=%d low=%#x\\n", x, '
                'popcount32(x), parity32(x), ctz32(x), clz32(x), ilog2(x), is_pow2(x), lowest_bit(x));\n'
                '    }\n'
                '    uint32_t n[] = {0, 1, 2, 3, 5, 1000, 0x80000000u, 0x80000001u};\n'
                '    for (int i = 0; i < 8; i++) printf("%u -> %u\\n", n[i], next_pow2(n[i]));\n'
                '    printf("%#x %#x %#x %#x\\n", rotl32(0x80000001u, 1), rotl32(0x12345678u, 8), '
                'rotl32(0x12345678u, 0), rotl32(0x12345678u, 36));\n'
                '    printf("%#x %#x %#x\\n", rotr32(0x80000001u, 1), rotr32(0x12345678u, 8), '
                'rotr32(0x12345678u, 32));\n'
                '    printf("%#x %#x %#x\\n", reverse32(1), reverse32(0xF0u), reverse32(0x12345678u));\n'
                '    printf("builtin: %d\\n", src_count("__bu" "iltin"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сдвиги на 32 неопределены: rotl с r = 0 обрабатывайте отдельно (или r &= 31 и ветка). x & (x '
              '− 1) сбрасывает младшую единицу.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['0: pop=0 par=0 ctz=32 clz=32 lg=-1 pow2=0 low=0',
                   '0x1: pop=1 par=1 ctz=0 clz=31 lg=0 pow2=1 low=0x1',
                   '0x2: pop=1 par=1 ctz=1 clz=30 lg=1 pow2=1 low=0x2',
                   '0x6: pop=2 par=0 ctz=1 clz=29 lg=2 pow2=0 low=0x2',
                   '0xff: pop=8 par=0 ctz=0 clz=24 lg=7 pow2=0 low=0x1',
                   '0x80000000: pop=1 par=1 ctz=31 clz=0 lg=31 pow2=1 low=0x80000000',
                   '0xffffffff: pop=32 par=0 ctz=0 clz=0 lg=31 pow2=0 low=0x1',
                   '0xf00f00: pop=8 par=0 ctz=8 clz=8 lg=23 pow2=0 low=0x100',
                   '0xbc614e: pop=12 par=0 ctz=1 clz=8 lg=23 pow2=0 low=0x2',
                   '0 -> 1',
                   '1 -> 1',
                   '2 -> 2',
                   '3 -> 4',
                   '5 -> 8',
                   '1000 -> 1024',
                   '2147483648 -> 2147483648',
                   '2147483649 -> 0',
                   '0x3 0x34567812 0x12345678 0x23456781',
                   '0xc0000000 0x78123456 0x12345678',
                   '0x80000000 0xf000000 0x1e6a2c48',
                   'builtin: 0']},
     {'id': 'c9-bitset',
      'mode': 'c',
      'title': 'Битовое множество',
      'statement': 'struct bitset { uint64_t *w; size_t nbits; }. bs_new(nbits) → указатель (всё нули) или '
                   'NULL; bs_set, bs_clear, bs_flip, bs_test (за границей → 0, set/clear игнорируются); '
                   'bs_count(b) — число единиц; bs_next(b, from) → индекс ближайшего установленного бита ≥ '
                   'from или nbits, если такого нет; bs_or(a, b), bs_and(a, b) — результат в a (размеры '
                   'равны); bs_free. Под AddressSanitizer.',
      'starter': '#include <stddef.h>\n'
                 '#include <stdint.h>\n'
                 '\n'
                 'struct bitset { uint64_t *w; size_t nbits; };\n'
                 '\n'
                 'struct bitset *bs_new(size_t nbits) { return 0; }\n'
                 'void bs_set(struct bitset *b, size_t i) {}\n'
                 'void bs_clear(struct bitset *b, size_t i) {}\n'
                 'void bs_flip(struct bitset *b, size_t i) {}\n'
                 'int bs_test(const struct bitset *b, size_t i) { return -1; }\n'
                 'size_t bs_count(const struct bitset *b) { return 0; }\n'
                 'size_t bs_next(const struct bitset *b, size_t from) { return 0; }\n'
                 'void bs_or(struct bitset *a, const struct bitset *b) {}\n'
                 'void bs_and(struct bitset *a, const struct bitset *b) {}\n'
                 'void bs_free(struct bitset *b) {}\n',
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
                '    struct bitset *a = bs_new(200), *b = bs_new(200);\n'
                '    size_t ia[] = {0, 1, 63, 64, 65, 127, 128, 199};\n'
                '    for (int i = 0; i < 8; i++) bs_set(a, ia[i]);\n'
                '    bs_set(a, 200);\n'
                '    bs_set(a, 100000);\n'
                '    printf("%zu %d %d %d %d\\n", bs_count(a), bs_test(a, 63), bs_test(a, 62), bs_test(a, '
                '200), bs_test(a, 199));\n'
                '    bs_clear(a, 63);\n'
                '    bs_flip(a, 62);\n'
                '    bs_flip(a, 1);\n'
                '    printf("%zu %d %d %d\\n", bs_count(a), bs_test(a, 63), bs_test(a, 62), bs_test(a, 1));\n'
                '    for (size_t i = bs_next(a, 0); i < 200; i = bs_next(a, i + 1)) printf("%zu ", i);\n'
                '    printf("\\n%zu %zu %zu\\n", bs_next(a, 129), bs_next(a, 199), bs_next(a, 200));\n'
                '    for (size_t i = 100; i < 140; i += 2) bs_set(b, i);\n'
                '    bs_and(b, a);\n'
                '    printf("%zu\\n", bs_count(b));\n'
                '    bs_or(b, a);\n'
                '    printf("%zu\\n", bs_count(b));\n'
                '    struct bitset *z = bs_new(0);\n'
                '    printf("%zu %zu\\n", bs_count(z), bs_next(z, 0));\n'
                '    bs_free(a); bs_free(b); bs_free(z);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Слово i / 64, бит i % 64; при установке/сбросе проверяйте границу. Для подсчёта единиц в '
              'слове — x &= x − 1.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['8 1 0 0 1', '7 0 1 0', '0 62 64 65 127 128 199', '199 199 200', '1', '7', '0 0']},
     {'id': 'c9-dos-date',
      'mode': 'c',
      'title': 'Упаковка даты и времени в 16 бит',
      'statement': 'Формат MS-DOS: дата — uint16: год − 1980 (7 бит, старшие), месяц 1–12 (4 бита), день '
                   '1–31 (5 бит, младшие); время — uint16: часы (5 бит), минуты (6 бит), секунды / 2 (5 '
                   'бит). pack_date(y, m, d), pack_time(h, mi, s) → uint16_t; unpack_date(v, *y, *m, *d), '
                   'unpack_time(v, *h, *mi, *s); valid_date(v) → 1, если месяц и день допустимы (с учётом '
                   'числа дней в месяце и високосных лет); date_cmp(a, b) — сравнение двух упакованных дат '
                   '(достаточно сравнить числа).',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint16_t pack_date(int y, int m, int d) { return 0; }\n'
                 'uint16_t pack_time(int h, int mi, int s) { return 0; }\n'
                 'void unpack_date(uint16_t v, int *y, int *m, int *d) {}\n'
                 'void unpack_time(uint16_t v, int *h, int *mi, int *s) {}\n'
                 'int valid_date(uint16_t v) { return -1; }\n'
                 'int date_cmp(uint16_t a, uint16_t b) { return 0; }\n',
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
                '    uint16_t d = pack_date(2024, 2, 29), t = pack_time(13, 45, 58);\n'
                '    printf("%#x %#x\\n", d, t);\n'
                '    int y, m, dd, h, mi, s;\n'
                '    unpack_date(d, &y, &m, &dd);\n'
                '    unpack_time(t, &h, &mi, &s);\n'
                '    printf("%d-%02d-%02d %02d:%02d:%02d\\n", y, m, dd, h, mi, s);\n'
                '    printf("%d %d %d %d\\n", valid_date(d), valid_date(pack_date(2023, 2, 29)), '
                'valid_date(pack_date(2100, 2, 29)), valid_date(pack_date(2000, 2, 29)));\n'
                '    printf("%d %d %d %d\\n", valid_date(pack_date(2020, 13, 1)), valid_date(pack_date(2020, '
                '4, 31)), valid_date(pack_date(2020, 12, 31)), valid_date(pack_date(2020, 1, 0)));\n'
                '    printf("%d %d %d\\n", date_cmp(pack_date(2020, 1, 1), pack_date(2020, 1, 2)), '
                'date_cmp(pack_date(2021, 1, 1), pack_date(2020, 12, 31)), date_cmp(d, d));\n'
                '    printf("%#x %#x\\n", pack_date(1980, 1, 1), pack_date(2107, 12, 31));\n'
                '    unpack_time(pack_time(23, 59, 59), &h, &mi, &s);\n'
                '    printf("%d:%d:%d\\n", h, mi, s);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Поля складываются сдвигами: (год − 1980) << 9 | месяц << 5 | день. Секунды хранятся с шагом '
              '2, поэтому 59 → 58.',
      'expected': ['0x585d 0x6dbd',
                   '2024-02-29 13:45:58',
                   '1 0 0 1',
                   '0 0 1 0',
                   '-1 1 0',
                   '0x21 0xff9f',
                   '23:59:58']},
     {'id': 'c9-float-parts',
      'mode': 'c',
      'title': 'Устройство float: знак, порядок, мантисса',
      'statement': 'float_parts(f, *sign, *exp, *mant) — разобрать float по битам (через memcpy): sign 0/1, '
                   'exp — поле порядка 0…255 (не смещённое), mant — 23 бита. make_float(sign, exp, mant) — '
                   'собрать обратно. float_class(f) → строка: "zero", "denormal", "normal", "inf", "nan". '
                   'unbiased_exp(f) → степень двойки нормализованного числа (exp − 127) или −127 для '
                   'денормализованных и нуля, 128 для inf/nan. Функции классификации из math.h использовать '
                   'нельзя.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'void float_parts(float f, int *sign, int *exp, uint32_t *mant) {}\n'
                 'float make_float(int sign, int exp, uint32_t mant) { return 0; }\n'
                 'const char *float_class(float f) { return ""; }\n'
                 'int unbiased_exp(float f) { return -999; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void show(float f) {\n'
                '    int s, e;\n'
                '    uint32_t m;\n'
                '    float_parts(f, &s, &e, &m);\n'
                '    printf("%s s=%d e=%d m=%#x class=%s ue=%d\\n", "f", s, e, m, float_class(f), '
                'unbiased_exp(f));\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    float vals[] = {1.0f, -2.5f, 0.1f, 0.0f, -0.0f, 1e-40f, 3.4028235e38f, 1.0f / 0.0f, '
                '-1.0f / 0.0f, 0.0f / 0.0f, 0.5f, 100.0f};\n'
                '    for (size_t i = 0; i < sizeof vals / sizeof vals[0]; i++) show(vals[i]);\n'
                '    printf("%g %g %g\\n", make_float(0, 127, 0), make_float(1, 128, 0x200000), '
                'make_float(0, 0, 1));\n'
                '    printf("%d %d\\n", make_float(0, 255, 0) == 1.0f / 0.0f, make_float(0, 255, 1) != '
                'make_float(0, 255, 1));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'uint32_t u; memcpy(&u, &f, 4); sign = u >> 31; exp = u >> 23 & 0xFF; mant = u & 0x7FFFFF. '
              'Класс определяется по exp и mant.',
      'expected': ['f s=0 e=127 m=0 class=normal ue=0',
                   'f s=1 e=128 m=0x200000 class=normal ue=1',
                   'f s=0 e=123 m=0x4ccccd class=normal ue=-4',
                   'f s=0 e=0 m=0 class=zero ue=-127',
                   'f s=1 e=0 m=0 class=zero ue=-127',
                   'f s=0 e=0 m=0x116c2 class=denormal ue=-127',
                   'f s=0 e=254 m=0x7fffff class=normal ue=127',
                   'f s=0 e=255 m=0 class=inf ue=128',
                   'f s=1 e=255 m=0 class=inf ue=128',
                   'f s=0 e=255 m=0x400000 class=nan ue=128',
                   'f s=0 e=126 m=0 class=normal ue=-1',
                   'f s=0 e=133 m=0x480000 class=normal ue=6',
                   '1 -2.5 1.4013e-45',
                   '1 1']},
     {'id': 'c9-ulp',
      'mode': 'c',
      'title': 'Расстояние в ulp и соседние числа',
      'statement': 'float_key(f) → uint32_t, монотонно возрастающий вместе со значением float (отрицательные '
                   'числа ниже положительных; −0.0 и +0.0 соседние: допустимо считать равными ключами не '
                   'нужно — используйте стандартный приём: для отрицательных инвертировать все биты, для '
                   'положительных — старший бит). ulp_distance(a, b) → число представимых float между a и b '
                   '(|key(a) − key(b)|, как uint32_t); next_up(f), next_down(f) — соседнее большее и меньшее '
                   'число (для NaN — то же число; next_up(+inf) = +inf; next_up(−0.0) = наименьшее '
                   'положительное денормализованное). Без nextafterf.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t float_key(float f) { return 0; }\n'
                 'uint32_t ulp_distance(float a, float b) { return 0; }\n'
                 'float next_up(float f) { return f; }\n'
                 'float next_down(float f) { return f; }\n',
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
                '    float a = 1.0f, b = next_up(a), c = next_up(b);\n'
                '    printf("%d %d %d\\n", b > a, c > b, ulp_distance(a, c));\n'
                '    printf("%u %u %u\\n", ulp_distance(a, b), ulp_distance(a, a), ulp_distance(b, a));\n'
                '    printf("%.9g %.9g\\n", next_up(1.0f), next_down(1.0f));\n'
                '    printf("%.9g %.9g\\n", next_up(-1.0f), next_down(-1.0f));\n'
                '    printf("%.9g %.9g\\n", next_up(0.0f), next_down(0.0f));\n'
                '    printf("%.9g %.9g\\n", next_up(-0.0f), next_down(-0.0f));\n'
                '    printf("%.9g %.9g\\n", next_up(3.4028235e38f), next_down(-3.4028235e38f));\n'
                '    printf("%.9g %.9g\\n", next_up(1.0f / 0.0f), next_down(-1.0f / 0.0f));\n'
                '    float n = 0.0f / 0.0f;\n'
                '    printf("%d %d\\n", next_up(n) != next_up(n), next_down(n) != next_down(n));\n'
                '    printf("%u %u\\n", ulp_distance(0.1f + 0.2f, 0.3f), ulp_distance(-1.0f, 1.0f));\n'
                '    printf("%d %d\\n", float_key(-2.0f) < float_key(-1.0f), float_key(1.0f) < '
                'float_key(2.0f));\n'
                '    printf("%d %d\\n", float_key(-1.0f) < float_key(1.0f), float_key(-1e-40f) < '
                'float_key(1e-40f));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Ключ: если знаковый бит установлен — ~bits, иначе bits | 0x80000000. Тогда сравнение ключей '
              'как беззнаковых чисел совпадает со сравнением float.',
      'expected': ['1 1 2',
                   '1 0 1',
                   '1.00000012 0.99999994',
                   '-0.99999994 -1.00000012',
                   '1.40129846e-45 -1.40129846e-45',
                   '1.40129846e-45 -1.40129846e-45',
                   'inf -inf',
                   'inf -inf',
                   '1 1',
                   '0 2130706433',
                   '1 1',
                   '1 1']},
     {'id': 'c9-near-equal',
      'mode': 'c',
      'title': 'Сравнение дробных чисел с допуском',
      'statement': 'nearly_equal(a, b, abs_eps, rel_eps) → 1, если |a − b| ≤ abs_eps или |a − b| ≤ rel_eps · '
                   'max(|a|, |b|); бесконечности равны только одинаковые; NaN не равен ничему (включая NaN); '
                   'approx_zero(x, eps) → |x| ≤ eps; clamp_unit(x) — ограничить [0, 1] (NaN → 0); '
                   'sum_close(a, n, expected, eps) — сумма массива близка к expected с относительным '
                   'допуском eps. Функции из math.h (fabs, isnan, isinf, fmax) допустимы.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int nearly_equal(double a, double b, double abs_eps, double rel_eps) { return -1; }\n'
                 'int approx_zero(double x, double eps) { return -1; }\n'
                 'double clamp_unit(double x) { return -9; }\n'
                 'int sum_close(const double *a, size_t n, double expected, double eps) { return -1; }\n',
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
                '    printf("%d %d\\n", 0.1 + 0.2 == 0.3, nearly_equal(0.1 + 0.2, 0.3, 1e-12, 1e-12));\n'
                '    printf("%d %d\\n", nearly_equal(1e-20, 0, 1e-12, 1e-9), nearly_equal(1e-20, 0, 0, '
                '1e-9));\n'
                '    printf("%d %d\\n", nearly_equal(1e10, 1e10 + 1, 1e-9, 1e-9), nearly_equal(1e10, 1e10 + '
                '100, 1e-9, 1e-9));\n'
                '    printf("%d %d\\n", nearly_equal(1.0 / 0.0, 1.0 / 0.0, 1, 1), nearly_equal(1.0 / 0.0, '
                '-1.0 / 0.0, 1, 1));\n'
                '    printf("%d %d\\n", nearly_equal(0.0 / 0.0, 0.0 / 0.0, 1, 1), nearly_equal(1.0, 0.0 / '
                '0.0, 1, 1));\n'
                '    printf("%d %d %d\\n", nearly_equal(1.0 / 0.0, 1e308, 1e300, 1), nearly_equal(-0.0, 0.0, '
                '0, 0), nearly_equal(5, 5.5, 0.5, 0));\n'
                '    printf("%d %d\\n", approx_zero(-1e-10, 1e-9), approx_zero(1e-8, 1e-9));\n'
                '    printf("%g %g %g %g\\n", clamp_unit(-3), clamp_unit(0.25), clamp_unit(7), '
                'clamp_unit(0.0 / 0.0));\n'
                '    double a[10];\n'
                '    for (int i = 0; i < 10; i++) a[i] = 0.1;\n'
                '    printf("%d %d\\n", sum_close(a, 10, 1.0, 1e-12), sum_close(a, 10, 1.001, 1e-6));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сначала особые значения (NaN, бесконечности), затем d = |a − b| и две проверки: абсолютная и '
              'относительная.',
      'expected': ['0 1', '1 0', '1 0', '1 0', '0 0', '0 1 1', '1 0', '0 0.25 1 0', '1 0']},
     {'id': 'c9-kahan',
      'mode': 'c',
      'title': 'Суммирование: простое, Кэхэна и попарное',
      'statement': 'sum_naive(a, n) — обычная сумма слева направо; sum_kahan(a, n) — компенсированное '
                   'суммирование Кэхэна (результат: накопленная сумма с поправкой c = (t − sum) − y); '
                   'sum_pairwise(a, n) — рекурсивное попарное: сумма половин (для n ≤ 2 — прямая); '
                   'dot_kahan(x, y, n) — скалярное произведение с компенсацией. Не используйте long double и '
                   'опции быстрой математики.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'double sum_naive(const double *a, size_t n) { return 0; }\n'
                 'double sum_kahan(const double *a, size_t n) { return 0; }\n'
                 'double sum_pairwise(const double *a, size_t n) { return 0; }\n'
                 'double dot_kahan(const double *x, const double *y, size_t n) { return 0; }\n',
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
                '    enum { N = 1000000 };\n'
                '    double *a = malloc(N * sizeof *a);\n'
                '    for (int i = 0; i < N; i++) a[i] = 0.1;\n'
                '    printf("naive err %d\\n", sum_naive(a, N) != 100000.0);\n'
                '    printf("kahan %.10f\\n", sum_kahan(a, N));\n'
                '    printf("pairwise %.6f\\n", sum_pairwise(a, N));\n'
                '    double b[12] = {1e16, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1e16};\n'
                '    printf("%.1f %.1f %.1f\\n", sum_naive(b, 12), sum_kahan(b, 12), sum_pairwise(b, 12));\n'
                '    double c[3] = {0.1, 0.2, 0.3};\n'
                '    printf("%.17g %.17g\\n", sum_naive(c, 3), sum_kahan(c, 3));\n'
                '    printf("%.1f %.1f %.1f\\n", sum_naive(c, 0), sum_kahan(c, 0), sum_pairwise(c, 0));\n'
                '    double x[4] = {1e8, 1, 1e8, 1}, y[4] = {1e8, 1, -1e8, 1};\n'
                '    printf("%.1f\\n", dot_kahan(x, y, 4));\n'
                '    free(a);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Кэхэн: y = a[i] − c; t = sum + y; c = (t − sum) − y; sum = t. Попарное: делим массив пополам, '
              'складываем результаты.',
      'expected': ['naive err 1',
                   'kahan 100000.0000000000',
                   'pairwise 100000.000000',
                   '0.0 10.0 8.0',
                   '0.60000000000000009 0.59999999999999998',
                   '0.0 0.0 0.0',
                   '1.0']},
     {'id': 'c9-fixed-point',
      'mode': 'c',
      'title': 'Числа с фиксированной точкой Q16.16',
      'statement': 'typedef int32_t fx — число Q16.16 (значение = raw / 65536). fx_from_int(n), '
                   'fx_from_double(d) (с округлением к ближайшему), fx_to_double(x), fx_to_int(x) '
                   '(отбрасывание дробной части к нулю), fx_add, fx_sub, fx_mul (через int64_t, с '
                   'округлением к ближайшему; ничего не переполняется внутри), fx_div (деление на 0 → '
                   'INT32_MAX или INT32_MIN по знаку делимого, для 0/0 → 0), fx_mul_sat — умножение с '
                   'насыщением до границ int32.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'typedef int32_t fx;\n'
                 '\n'
                 'fx fx_from_int(int n) { return 0; }\n'
                 'fx fx_from_double(double d) { return 0; }\n'
                 'double fx_to_double(fx x) { return 0; }\n'
                 'int fx_to_int(fx x) { return 0; }\n'
                 'fx fx_add(fx a, fx b) { return 0; }\n'
                 'fx fx_sub(fx a, fx b) { return 0; }\n'
                 'fx fx_mul(fx a, fx b) { return 0; }\n'
                 'fx fx_div(fx a, fx b) { return 0; }\n'
                 'fx fx_mul_sat(fx a, fx b) { return 0; }\n',
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
                '    fx a = fx_from_double(1.5), b = fx_from_double(-2.25), c = fx_from_int(3);\n'
                '    printf("%d %d %d\\n", a, b, c);\n'
                '    printf("%.5f %.5f %.5f\\n", fx_to_double(fx_add(a, b)), fx_to_double(fx_sub(a, b)), '
                'fx_to_double(fx_mul(a, b)));\n'
                '    printf("%.5f %.5f\\n", fx_to_double(fx_div(a, b)), fx_to_double(fx_div(c, '
                'fx_from_int(7))));\n'
                '    printf("%d %d %d\\n", fx_to_int(a), fx_to_int(b), fx_to_int(fx_from_double(-0.99)));\n'
                '    printf("%d %d %d\\n", fx_div(a, 0), fx_div(b, 0), fx_div(0, 0));\n'
                '    printf("%d\\n", fx_mul(fx_from_double(0.00002), fx_from_double(0.5)));\n'
                '    printf("%d %d\\n", fx_mul_sat(fx_from_int(30000), fx_from_int(30000)), '
                'fx_mul_sat(fx_from_int(-30000), fx_from_int(30000)));\n'
                '    printf("%d %d\\n", fx_mul_sat(fx_from_int(100), fx_from_int(100)), '
                'fx_mul(fx_from_int(100), fx_from_int(100)));\n'
                '    double r = 0;\n'
                '    for (int i = 0; i < 100; i++) r += fx_to_double(fx_mul(fx_from_double(0.01 * i), '
                'fx_from_double(0.5)));\n'
                '    printf("%.3f\\n", r);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Q16.16: raw = value · 65536. Произведение двух raw нужно считать в int64_t и сдвигать на 16 с '
              'округлением; для деления числитель умножают на 65536 заранее.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['98304 -147456 196608',
                   '-0.75000 3.75000 -3.37500',
                   '-0.66667 0.42857',
                   '1 -2 0',
                   '2147483647 -2147483648 0',
                   '1',
                   '2147483647 -2147483648',
                   '655360000 655360000',
                   '24.750']},
     {'id': 'c9-half-float',
      'mode': 'c',
      'title': 'Половинная точность IEEE 754 (binary16)',
      'statement': 'float_to_half(f) → uint16_t и half_to_float(h) → float. Формат: 1 бит знака, 5 бит '
                   'порядка (смещение 15), 10 бит мантиссы. float_to_half округляет к ближайшему чётному; '
                   'слишком большие → бесконечность (0x7C00 со знаком), слишком малые → ноль или '
                   'денормализованное; NaN → 0x7E00; бесконечность → 0x7C00/0xFC00. half_to_float должна '
                   'точно восстанавливать значение, включая денормализованные числа и бесконечности (NaN → '
                   'NaN).',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint16_t float_to_half(float f) { return 0; }\n'
                 'float half_to_float(uint16_t h) { return 0; }\n',
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
                '    float t[] = {0.0f, -0.0f, 1.0f, -2.5f, 0.1f, 65504.0f, 65519.0f, 65520.0f, 1e6f, '
                '6.1035156e-5f, 5.9604645e-8f, 2.9802322e-8f, 3e-8f, 1e-9f, 1.0009765625f, 1.00146484375f, '
                '1.0f / 0.0f, -1.0f / 0.0f, 3.14159265f};\n'
                '    for (size_t i = 0; i < sizeof t / sizeof t[0]; i++) {\n'
                '        uint16_t h = float_to_half(t[i]);\n'
                '        printf("%#06x %.9g\\n", h, half_to_float(h));\n'
                '    }\n'
                '    printf("%#06x %d\\n", float_to_half(0.0f / 0.0f), half_to_float(0x7E00) != '
                'half_to_float(0x7E00));\n'
                '    int bad = 0;\n'
                '    for (uint32_t h = 0; h < 65536; h++) {\n'
                '        if ((h & 0x7C00) == 0x7C00 && (h & 0x3FF)) continue;\n'
                '        if (float_to_half(half_to_float((uint16_t)h)) != h) bad++;\n'
                '    }\n'
                '    printf("roundtrip bad=%d\\n", bad);\n'
                '    printf("%g %g %g\\n", half_to_float(0x3C00), half_to_float(0xC000), '
                'half_to_float(0x0001));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Нормализованные: порядок e = exp − 127 + 15, мантисса сдвигается на 13 с округлением к '
              'чётному по остатку. Денормализованные — добавьте неявную единицу и сдвиньте дальше.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['000000 0',
                   '0x8000 -0',
                   '0x3c00 1',
                   '0xc100 -2.5',
                   '0x2e66 0.0999755859',
                   '0x7bff 65504',
                   '0x7bff 65504',
                   '0x7c00 inf',
                   '0x7c00 inf',
                   '0x0400 6.10351562e-05',
                   '0x0001 5.96046448e-08',
                   '000000 0',
                   '0x0001 5.96046448e-08',
                   '000000 0',
                   '0x3c01 1.00097656',
                   '0x3c02 1.00195312',
                   '0x7c00 inf',
                   '0xfc00 -inf',
                   '0x4248 3.140625',
                   '0x7e00 1',
                   'roundtrip bad=0',
                   '1 -2 5.96046e-08']},
     {'id': 'c9-int-division',
      'mode': 'c',
      'title': 'Деление и остаток: C и математика',
      'statement': 'В C деление округляет к нулю, а остаток имеет знак делимого. Напишите: floor_div(a, b) и '
                   'floor_mod(a, b) (округление к −∞, остаток со знаком делителя), euclid_mod(a, b) (всегда '
                   '≥ 0), ceil_div(a, b), round_div(a, b) (к ближайшему, половина — от нуля); wrap_index(i, '
                   'n) — индекс в кольцевом буфере длины n для любого целого i (в том числе отрицательного). '
                   'Делитель всегда ненулевой; значения без переполнения (INT_MIN / −1 не проверяется).',
      'starter': 'int floor_div(int a, int b) { return 0; }\n'
                 'int floor_mod(int a, int b) { return 0; }\n'
                 'int euclid_mod(int a, int b) { return 0; }\n'
                 'int ceil_div(int a, int b) { return 0; }\n'
                 'int round_div(int a, int b) { return 0; }\n'
                 'int wrap_index(int i, int n) { return 0; }\n',
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
                '    int as[] = {7, -7, 7, -7, 0, 6, -6, 5};\n'
                '    int bs[] = {2, 2, -2, -2, 3, 3, 3, 5};\n'
                '    for (int i = 0; i < 8; i++) {\n'
                '        int a = as[i], b = bs[i];\n'
                '        printf("%d/%d: c=%d %d fl=%d %d eu=%d ce=%d ro=%d\\n", a, b, a / b, a % b, '
                'floor_div(a, b), floor_mod(a, b), euclid_mod(a, b), ceil_div(a, b), round_div(a, b));\n'
                '    }\n'
                '    printf("%d %d %d %d\\n", round_div(5, 2), round_div(-5, 2), round_div(4, 3), '
                'round_div(-4, 3));\n'
                '    printf("%d %d %d %d %d\\n", wrap_index(0, 5), wrap_index(7, 5), wrap_index(-1, 5), '
                'wrap_index(-11, 5), wrap_index(10, 5));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Остаток C имеет знак делимого. Для floor — поправляйте результат, когда остаток не нулевой и '
              'знаки остатка и делителя различаются.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['7/2: c=3 1 fl=3 1 eu=1 ce=4 ro=4',
                   '-7/2: c=-3 -1 fl=-4 1 eu=1 ce=-3 ro=-4',
                   '7/-2: c=-3 1 fl=-4 -1 eu=1 ce=-3 ro=-4',
                   '-7/-2: c=3 -1 fl=3 -1 eu=1 ce=4 ro=4',
                   '0/3: c=0 0 fl=0 0 eu=0 ce=0 ro=0',
                   '6/3: c=2 0 fl=2 0 eu=0 ce=2 ro=2',
                   '-6/3: c=-2 0 fl=-2 0 eu=0 ce=-2 ro=-2',
                   '5/5: c=1 0 fl=1 0 eu=0 ce=1 ro=1',
                   '3 -3 1 -1',
                   '0 2 4 4 0']},
     {'id': 'c9-utf8-codec',
      'mode': 'c',
      'title': 'Кодирование и декодирование UTF-8',
      'statement': 'utf8_encode(cp, out) → длина 1…4 и байты в out[0..3], либо 0, если кодовая точка '
                   'недопустима (> 0x10FFFF или суррогат 0xD800…0xDFFF). utf8_decode(s, n, *cp) → число '
                   'прочитанных байт (1…4) и кодовая точка, либо 0, если последовательность неверна: пустая, '
                   'оборвана, неверный байт продолжения, «избыточная» (overlong) форма, суррогат, > '
                   '0x10FFFF.',
      'starter': '#include <stddef.h>\n'
                 '#include <stdint.h>\n'
                 '\n'
                 'int utf8_encode(uint32_t cp, unsigned char out[4]) { return -1; }\n'
                 'int utf8_decode(const unsigned char *s, size_t n, uint32_t *cp) { return -1; }\n',
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
                '    uint32_t cps[] = {0x41, 0x7F, 0x80, 0x7FF, 0x800, 0x20AC, 0xFFFF, 0x10000, 0x1F600, '
                '0x10FFFF, 0x110000, 0xD800, 0xDFFF};\n'
                '    for (size_t i = 0; i < sizeof cps / sizeof cps[0]; i++) {\n'
                '        unsigned char b[4] = {0};\n'
                '        int n = utf8_encode(cps[i], b);\n'
                '        printf("U+%04X %d:", cps[i], n);\n'
                '        for (int k = 0; k < n; k++) printf(" %02X", b[k]);\n'
                '        uint32_t back = 0;\n'
                '        int m = n ? utf8_decode(b, n, &back) : 0;\n'
                '        printf(" -> %d %#x\\n", m, back);\n'
                '    }\n'
                '    struct { const char *name; unsigned char b[5]; size_t n; } bad[] = {\n'
                '        {"empty", {0}, 0}, {"cont", {0x80}, 1}, {"trunc2", {0xC3}, 1}, {"trunc3", {0xE2, '
                '0x82}, 2}, {"overlong", {0xC0, 0x80}, 2},\n'
                '        {"overlong3", {0xE0, 0x80, 0x80}, 3}, {"surr", {0xED, 0xA0, 0x80}, 3}, {"big", '
                '{0xF4, 0x90, 0x80, 0x80}, 4}, {"badcont", {0xE2, 0x41, 0xAC}, 3}, {"ff", {0xFF}, 1},\n'
                '        {"ok2", {0xC3, 0xA9}, 2}, {"extra", {0xC3, 0xA9, 0x41}, 3},\n'
                '    };\n'
                '    for (size_t i = 0; i < sizeof bad / sizeof bad[0]; i++) {\n'
                '        uint32_t cp = 0;\n'
                '        int n = utf8_decode(bad[i].b, bad[i].n, &cp);\n'
                '        printf("%s: %d %#x\\n", bad[i].name, n, n ? cp : 0);\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Кодирование: ведущий байт 110xxxxx / 1110xxxx / 11110xxx и байты продолжения 10xxxxxx по 6 '
              'бит. При декодировании проверьте длину, байты продолжения и минимальное значение для данной '
              'длины (иначе — избыточная форма).',
      'expected': ['U+0041 1: 41 -> 1 0x41',
                   'U+007F 1: 7F -> 1 0x7f',
                   'U+0080 2: C2 80 -> 2 0x80',
                   'U+07FF 2: DF BF -> 2 0x7ff',
                   'U+0800 3: E0 A0 80 -> 3 0x800',
                   'U+20AC 3: E2 82 AC -> 3 0x20ac',
                   'U+FFFF 3: EF BF BF -> 3 0xffff',
                   'U+10000 4: F0 90 80 80 -> 4 0x10000',
                   'U+1F600 4: F0 9F 98 80 -> 4 0x1f600',
                   'U+10FFFF 4: F4 8F BF BF -> 4 0x10ffff',
                   'U+110000 0: -> 0 0',
                   'U+D800 0: -> 0 0',
                   'U+DFFF 0: -> 0 0',
                   'empty: 0 0',
                   'cont: 0 0',
                   'trunc2: 0 0',
                   'trunc3: 0 0',
                   'overlong: 0 0',
                   'overlong3: 0 0',
                   'surr: 0 0',
                   'big: 0 0',
                   'badcont: 0 0',
                   'ff: 0 0',
                   'ok2: 2 0xe9',
                   'extra: 2 0xe9']},
     {'id': 'c9-utf8-string',
      'mode': 'c',
      'title': 'Строки UTF-8: длина, проверка, разворот',
      'statement': 'utf8_len(s) → число кодовых точек (считая байты, не являющиеся продолжением 10xxxxxx; '
                   'строка предполагается корректной); utf8_valid(s) → 1, если вся строка корректный UTF-8 '
                   '(по правилам: без избыточных форм, суррогатов и значений > 0x10FFFF); utf8_offset(s, k) '
                   '→ смещение в байтах k-й кодовой точки (k = utf8_len → длина в байтах; дальше — −1); '
                   'utf8_reverse(s) — развернуть строку по кодовым точкам на месте (для корректной строки).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t utf8_len(const char *s) { return 0; }\n'
                 'int utf8_valid(const char *s) { return -1; }\n'
                 'long utf8_offset(const char *s, size_t k) { return -2; }\n'
                 'void utf8_reverse(char *s) {}\n',
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
                '    const char *s = "aé€😀z";\n'
                '    printf("%zu %zu %d\\n", strlen(s), utf8_len(s), utf8_valid(s));\n'
                '    printf("%ld %ld %ld %ld %ld %ld %ld\\n", utf8_offset(s, 0), utf8_offset(s, 1), '
                'utf8_offset(s, 2), utf8_offset(s, 3), utf8_offset(s, 4), utf8_offset(s, 5), utf8_offset(s, '
                '6));\n'
                '    char buf[32];\n'
                '    strcpy(buf, s);\n'
                '    utf8_reverse(buf);\n'
                '    printf("%s %d\\n", buf, strcmp(buf, "z😀€éa") == 0);\n'
                '    utf8_reverse(buf);\n'
                '    printf("%d\\n", strcmp(buf, s) == 0);\n'
                '    strcpy(buf, "");\n'
                '    utf8_reverse(buf);\n'
                '    printf("[%s] %zu\\n", buf, utf8_len(buf));\n'
                '    const char *bad[] = {"ok", "\\xC3", "\\xC0\\x80", "a\\xE2\\x82", "\\xED\\xA0\\x80", '
                '"\\xF4\\x90\\x80\\x80", "\\x80", "привет", "\\xFF"};\n'
                '    for (int i = 0; i < 9; i++) printf("%d ", utf8_valid(bad[i]));\n'
                '    printf("\\n");\n'
                '    char cyr[32] = "привет мир";\n'
                '    utf8_reverse(cyr);\n'
                '    printf("%s %zu\\n", cyr, utf8_len(cyr));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Разворот: сначала разверните байты всей строки, затем каждую многобайтовую последовательность '
              '(она оказалась задом наперёд) — обратно.',
      'expected': ['11 5 1',
                   '0 1 3 6 10 11 -1',
                   'z😀€éa 1',
                   '1',
                   '[] 0',
                   '1 0 0 0 0 0 0 1 0',
                   'рим тевирп 10']},
     {'id': 'c9-varint',
      'mode': 'c',
      'title': 'Целые переменной длины (varint) и zigzag',
      'statement': 'varint_encode(v, out) → число байт (1…10): по 7 бит на байт, младшие группы первыми, '
                   'старший бит 0x80 — «есть продолжение». varint_decode(in, n, *v) → число прочитанных '
                   'байт, либо 0, если данные оборваны или число длиннее 10 байт/не помещается в 64 бита. '
                   'zigzag_encode(int64_t) → uint64_t (0, −1, 1, −2, … → 0, 1, 2, 3, …), zigzag_decode. '
                   'encoded_size(v) → сколько байт займёт v.',
      'starter': '#include <stddef.h>\n'
                 '#include <stdint.h>\n'
                 '\n'
                 'size_t varint_encode(uint64_t v, uint8_t *out) { return 0; }\n'
                 'size_t varint_decode(const uint8_t *in, size_t n, uint64_t *v) { return 99; }\n'
                 'uint64_t zigzag_encode(int64_t x) { return 0; }\n'
                 'int64_t zigzag_decode(uint64_t u) { return 0; }\n'
                 'size_t encoded_size(uint64_t v) { return 0; }\n',
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
                '    uint64_t vs[] = {0, 1, 127, 128, 300, 16383, 16384, 0xFFFFFFFFu, 0x7FFFFFFFFFFFFFFFULL, '
                '0xFFFFFFFFFFFFFFFFULL};\n'
                '    for (size_t i = 0; i < sizeof vs / sizeof vs[0]; i++) {\n'
                '        uint8_t b[16] = {0};\n'
                '        size_t n = varint_encode(vs[i], b);\n'
                '        uint64_t back = 0;\n'
                '        size_t m = varint_decode(b, n, &back);\n'
                '        printf("%llu: %zu %zu", (unsigned long long)vs[i], n, encoded_size(vs[i]));\n'
                '        for (size_t k = 0; k < n; k++) printf(" %02x", b[k]);\n'
                '        printf(" -> %zu %d\\n", m, back == vs[i]);\n'
                '    }\n'
                '    uint8_t trunc[] = {0x80, 0x80};\n'
                '    uint8_t toolong[] = {0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, '
                '0x01};\n'
                '    uint8_t overflow[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x02};\n'
                '    uint64_t v = 0;\n'
                '    printf("%zu %zu %zu %zu\\n", varint_decode(trunc, 2, &v), varint_decode(toolong, 11, '
                '&v), varint_decode(overflow, 10, &v), varint_decode(trunc, 0, &v));\n'
                '    int64_t xs[] = {0, -1, 1, -2, 2, 2147483647, -2147483648LL, INT64_MAX, INT64_MIN};\n'
                '    for (size_t i = 0; i < sizeof xs / sizeof xs[0]; i++) {\n'
                '        uint64_t z = zigzag_encode(xs[i]);\n'
                '        printf("%lld -> %llu %d\\n", (long long)xs[i], (unsigned long long)z, '
                'zigzag_decode(z) == xs[i]);\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Пока v ≥ 128: пишем младшие 7 бит с флагом 0x80 и сдвигаем v на 7. Zigzag: (x << 1) ^ (x >> '
              '63) — арифметический сдвиг знакового; все сдвиги влево делайте над беззнаковым.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['0: 1 1 00 -> 1 1',
                   '1: 1 1 01 -> 1 1',
                   '127: 1 1 7f -> 1 1',
                   '128: 2 2 80 01 -> 2 1',
                   '300: 2 2 ac 02 -> 2 1',
                   '16383: 2 2 ff 7f -> 2 1',
                   '16384: 3 3 80 80 01 -> 3 1',
                   '4294967295: 5 5 ff ff ff ff 0f -> 5 1',
                   '9223372036854775807: 9 9 ff ff ff ff ff ff ff ff 7f -> 9 1',
                   '18446744073709551615: 10 10 ff ff ff ff ff ff ff ff ff 01 -> 10 1',
                   '0 0 0 0',
                   '0 -> 0 1',
                   '-1 -> 1 1',
                   '1 -> 2 1',
                   '-2 -> 3 1',
                   '2 -> 4 1',
                   '2147483647 -> 4294967294 1',
                   '-2147483648 -> 4294967295 1',
                   '9223372036854775807 -> 18446744073709551614 1',
                   '-9223372036854775808 -> 18446744073709551615 1']},
     {'id': 'c9-hex-base64',
      'mode': 'c',
      'title': 'Hex и base64',
      'statement': 'hex_encode(data, n, out) → записывает 2n строчных шестнадцатеричных цифр и завершающий '
                   'ноль; hex_decode(s, out, max) → число байт либо −1 (нечётная длина, недопустимый символ, '
                   'не помещается в max); допустимы цифры любого регистра. b64_encode(data, n, out) — '
                   'стандартный алфавит с «=»-дополнением, завершающий ноль, возвращает длину; b64_decode(s, '
                   'out, max) → число байт либо −1 (длина не кратна 4, недопустимые символы, «=» не в конце, '
                   'не помещается).',
      'starter': '#include <stddef.h>\n'
                 '#include <stdint.h>\n'
                 '\n'
                 'void hex_encode(const uint8_t *data, size_t n, char *out) {}\n'
                 'long hex_decode(const char *s, uint8_t *out, size_t max) { return -9; }\n'
                 'size_t b64_encode(const uint8_t *data, size_t n, char *out) { return 0; }\n'
                 'long b64_decode(const char *s, uint8_t *out, size_t max) { return -9; }\n',
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
                '    const uint8_t d[] = {0x00, 0xFF, 0x10, 0xAB, 0xCD};\n'
                '    char h[16];\n'
                '    hex_encode(d, 5, h);\n'
                '    printf("%s\\n", h);\n'
                '    uint8_t back[8] = {0};\n'
                '    printf("%ld %d\\n", hex_decode("00ff10ABcd", back, 8), memcmp(back, d, 5) == 0);\n'
                '    printf("%ld %ld %ld %ld %ld\\n", hex_decode("abc", back, 8), hex_decode("zz", back, 8), '
                'hex_decode("0011", back, 1), hex_decode("", back, 8), hex_decode("0g", back, 8));\n'
                '    const char *words[] = {"", "f", "fo", "foo", "foob", "fooba", "foobar"};\n'
                '    for (int i = 0; i < 7; i++) {\n'
                '        char e[32];\n'
                '        size_t n = b64_encode((const uint8_t *)words[i], strlen(words[i]), e);\n'
                '        uint8_t dec[16] = {0};\n'
                '        long m = b64_decode(e, dec, 16);\n'
                '        printf("[%s] %zu %ld %d\\n", e, n, m, m == (long)strlen(words[i]) && memcmp(dec, '
                'words[i], (size_t)m) == 0);\n'
                '    }\n'
                '    uint8_t bin[256];\n'
                '    for (int i = 0; i < 256; i++) bin[i] = (uint8_t)i;\n'
                '    char big[400];\n'
                '    b64_encode(bin, 256, big);\n'
                '    uint8_t out[256];\n'
                '    printf("%ld %d %.12s\\n", b64_decode(big, out, 256), memcmp(bin, out, 256) == 0, big);\n'
                '    printf("%ld %ld %ld %ld %ld %ld\\n", b64_decode("Zm9", out, 8), b64_decode("Zm9v!A==", '
                'out, 8), b64_decode("Zg=A", out, 8), b64_decode("=m9v", out, 8), b64_decode("Zm9vYg==", '
                'out, 2), b64_decode("Zm9vYmFy", out, 6));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'base64: три байта → 24 бита → четыре группы по 6 бит; дополнение «=» нужно, если в последнем '
              'блоке меньше трёх байт. Декодирование строго: проверяйте символы и положение «=».',
      'expected': ['00ff10abcd',
                   '5 1',
                   '-1 -1 -1 0 -1',
                   '[] 0 0 1',
                   '[Zg==] 4 1 1',
                   '[Zm8=] 4 2 1',
                   '[Zm9v] 4 3 1',
                   '[Zm9vYg==] 8 4 1',
                   '[Zm9vYmE=] 8 5 1',
                   '[Zm9vYmFy] 8 6 1',
                   '256 1 AAECAwQFBgcI',
                   '-1 -1 -1 -1 -1 6']},
     {'id': 'c9-crc-checksums',
      'mode': 'c',
      'title': 'Контрольные суммы: CRC-32, Adler-32, Fletcher-16',
      'statement': 'crc32_update(crc, data, n) — продолжить подсчёт CRC-32 (полином 0xEDB88320, отражённый; '
                   'начальное значение 0xFFFFFFFF и итоговая инверсия делаются в crc32(data, n) = '
                   'crc32_update(0, data, n): то есть crc32_update принимает и возвращает «готовое» '
                   'значение, а внутри инвертирует). Для строки «123456789» результат 0xCBF43926. '
                   'adler32(data, n) (модуль 65521, начальные a = 1, b = 0), fletcher16(data, n) (модуль '
                   '255).',
      'starter': '#include <stddef.h>\n'
                 '#include <stdint.h>\n'
                 '\n'
                 'uint32_t crc32_update(uint32_t crc, const void *data, size_t n) { return 0; }\n'
                 'uint32_t crc32(const void *data, size_t n) { return 0; }\n'
                 'uint32_t adler32(const void *data, size_t n) { return 0; }\n'
                 'uint16_t fletcher16(const void *data, size_t n) { return 0; }\n',
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
                '    const char *s = "123456789";\n'
                '    printf("%#x %#x %#x\\n", crc32(s, 9), adler32(s, 9), fletcher16(s, 9));\n'
                '    printf("%#x %#x %#x\\n", crc32("", 0), adler32("", 0), fletcher16("", 0));\n'
                '    uint32_t c = crc32_update(0, "12345", 5);\n'
                '    c = crc32_update(c, "6789", 4);\n'
                '    printf("%d\\n", c == crc32(s, 9));\n'
                '    printf("%#x %#x\\n", crc32("a", 1), crc32("The quick brown fox jumps over the lazy '
                'dog", 43));\n'
                '    printf("%#x %#x\\n", adler32("Wikipedia", 9), fletcher16("abcde", 5));\n'
                '    unsigned char z[1000] = {0};\n'
                '    printf("%#x %#x\\n", crc32(z, 1000), adler32(z, 1000));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Побитовый CRC: crc ^= байт; восемь раз: если младший бит — crc = crc >> 1 ^ 0xEDB88320, иначе '
              'crc >>= 1. Инверсия до и после делает «готовое» значение продолжаемым.',
      'expected': ['0xcbf43926 0x91e01de 0x1ede',
                   '0 0x1 0',
                   '1',
                   '0xe8b7be43 0x414fa339',
                   '0x11e60398 0xc8f0',
                   '0x60b1780 0x3e80001']},
     {'id': 'c9-hamming74',
      'mode': 'c',
      'title': 'Код Хэмминга (7,4): исправление одной ошибки',
      'statement': 'hamming_encode(nibble) → 7-битное кодовое слово (в младших 7 битах): позиции 1…7, где '
                   'позиции 1, 2, 4 — проверочные (чётность), 3, 5, 6, 7 — данные d1, d2, d3, d4 (d1 — '
                   'младший бит nibble). Бит позиции p — это бит (p − 1) слова. hamming_decode(word, '
                   '*nibble) → 0, если ошибок нет; k (1…7), если исправлена ошибка в позиции k (*nibble — '
                   'исправленные данные); для word вне 7 бит старшие биты игнорируются.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint8_t hamming_encode(uint8_t nibble) { return 0; }\n'
                 'int hamming_decode(uint8_t word, uint8_t *nibble) { return -1; }\n',
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
                '    for (int n = 0; n < 16; n++) printf("%x:%02x ", n, hamming_encode((uint8_t)n));\n'
                '    printf("\\n");\n'
                '    int ok = 0, fixed = 0, total = 0;\n'
                '    for (int n = 0; n < 16; n++) {\n'
                '        uint8_t w = hamming_encode((uint8_t)n), out = 99;\n'
                '        if (hamming_decode(w, &out) == 0 && out == n) ok++;\n'
                '        for (int p = 1; p <= 7; p++) {\n'
                '            uint8_t bad = (uint8_t)(w ^ (1 << (p - 1))), o2 = 99;\n'
                '            int r = hamming_decode(bad, &o2);\n'
                '            total++;\n'
                '            if (r == p && o2 == n) fixed++;\n'
                '        }\n'
                '    }\n'
                '    printf("%d %d %d\\n", ok, fixed, total);\n'
                '    uint8_t o;\n'
                '    printf("%d %d\\n", hamming_decode(0x80 | hamming_encode(5), &o), o);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Проверочные биты: p1 — позиции 1,3,5,7; p2 — 2,3,6,7; p4 — 4,5,6,7. Синдром (s4 s2 s1) '
              'указывает позицию ошибки; 0 — ошибки нет.',
      'expected': ['0:00 1:07 2:19 3:1e 4:2a 5:2d 6:33 7:34 8:4b 9:4c a:52 b:55 c:61 d:66 e:78 f:7f',
                   '16 112 112',
                   '0 5']},
     {'id': 'c9-struct-layout',
      'mode': 'c',
      'title': 'Раскладка структуры: смещения и размер',
      'statement': "Типы полей заданы строкой символов: 'c' — char (1/1), 's' — short (2/2), 'i' — int "
                   "(4/4), 'l' — long (8/8), 'd' — double (8/8), 'p' — указатель (8/8); размер/выравнивание. "
                   'layout(types, offsets, *align) → размер структуры с прокладками (в том числе '
                   'хвостовыми), заполняет offsets[i] и *align (наибольшее выравнивание); пустая строка → 0, '
                   'align = 1. best_order(types, out) → записывает те же типы, переставленные для '
                   'минимального размера (по убыванию выравнивания; при равенстве — по порядку в строке), '
                   'возвращает размер. padding(types) → число байт прокладок.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t layout(const char *types, size_t *offsets, size_t *align) { return 0; }\n'
                 'size_t best_order(const char *types, char *out) { return 0; }\n'
                 'size_t padding(const char *types) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void show(const char *t) {\n'
                '    size_t off[16] = {0}, al = 0;\n'
                '    size_t size = layout(t, off, &al);\n'
                '    printf("%-8s size=%zu align=%zu pad=%zu offs:", t, size, al, padding(t));\n'
                '    for (size_t i = 0; t[i]; i++) printf(" %zu", off[i]);\n'
                '    char best[16];\n'
                '    size_t bs = best_order(t, best);\n'
                '    printf(" | best=%s %zu\\n", best, bs);\n'
                '}\n'
                '\n'
                'struct a { char c; int i; char d; };\n'
                'struct b { char c; double d; short s; };\n'
                'struct c { short s; char c; long l; int i; };\n'
                '\n'
                'int main(void) {\n'
                '    show("");\n'
                '    show("c");\n'
                '    show("cic");\n'
                '    show("cds");\n'
                '    show("scli");\n'
                '    show("ccccc");\n'
                '    show("cip");\n'
                '    show("dcsci");\n'
                '    show("pcpc");\n'
                '    printf("%zu %zu %zu\\n", sizeof(struct a), sizeof(struct b), sizeof(struct c));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Смещение каждого поля округляется вверх до кратного его выравниванию; итоговый размер — до '
              'кратного наибольшему выравниванию. Для best_order упорядочьте по убыванию выравнивания '
              '(устойчиво).',
      'expected': ['         size=0 align=1 pad=0 offs: | best= 0',
                   'c        size=1 align=1 pad=0 offs: 0 | best=c 1',
                   'cic      size=12 align=4 pad=6 offs: 0 4 8 | best=icc 8',
                   'cds      size=24 align=8 pad=13 offs: 0 8 16 | best=dsc 16',
                   'scli     size=24 align=8 pad=9 offs: 0 2 8 16 | best=lisc 16',
                   'ccccc    size=5 align=1 pad=0 offs: 0 1 2 3 4 | best=ccccc 5',
                   'cip      size=16 align=8 pad=3 offs: 0 4 8 | best=pic 16',
                   'dcsci    size=24 align=8 pad=8 offs: 0 8 10 12 16 | best=discc 16',
                   'pcpc     size=32 align=8 pad=14 offs: 0 8 16 24 | best=ppcc 24',
                   '12 24 24']},
     {'id': 'c9-msg-pack',
      'mode': 'c',
      'title': 'Сериализация сообщения в сетевом порядке',
      'statement': 'struct msg { uint8_t type; uint16_t len; uint32_t id; int16_t delta; int32_t value; }. '
                   'Формат: 13 байт, поля подряд в порядке big-endian (type 1, len 2, id 4, delta 2 в '
                   'дополнительном коде, value 4 в дополнительном коде). msg_pack(m, out, cap) → 13 или 0, '
                   'если cap < 13; msg_unpack(in, n, *m) → 13 или 0, если n < 13 (структура не меняется). '
                   'Знаковые поля восстанавливаются с правильным знаком. Прямая запись структуры и '
                   'приведение указателей запрещены.',
      'starter': '#include <stddef.h>\n'
                 '#include <stdint.h>\n'
                 '\n'
                 'struct msg { uint8_t type; uint16_t len; uint32_t id; int16_t delta; int32_t value; };\n'
                 '\n'
                 'size_t msg_pack(const struct msg *m, uint8_t *out, size_t cap) { return 99; }\n'
                 'size_t msg_unpack(const uint8_t *in, size_t n, struct msg *m) { return 99; }\n',
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
                '    struct msg m = {7, 0x1234, 0xDEADBEEF, -2, -100000};\n'
                '    uint8_t buf[20];\n'
                '    memset(buf, 0xEE, sizeof buf);\n'
                '    size_t n = msg_pack(&m, buf, sizeof buf);\n'
                '    printf("%zu:", n);\n'
                '    for (size_t i = 0; i < 16; i++) printf(" %02x", buf[i]);\n'
                '    printf("\\n");\n'
                '    struct msg r = {0};\n'
                '    printf("%zu %u %#x %#x %d %d\\n", msg_unpack(buf, n, &r), r.type, r.len, r.id, r.delta, '
                'r.value);\n'
                '    struct msg k = {1, 2, 3, 4, 5};\n'
                '    printf("%zu %zu %u\\n", msg_pack(&m, buf, 12), msg_unpack(buf, 12, &k), k.id);\n'
                '    struct msg e = {255, 65535, 0xFFFFFFFFu, INT16_MIN, INT32_MIN};\n'
                '    msg_pack(&e, buf, 13);\n'
                '    struct msg f = {0};\n'
                '    msg_unpack(buf, 13, &f);\n'
                '    printf("%u %u %u %d %d\\n", f.type, f.len, f.id, f.delta, f.value);\n'
                '    struct msg p = {0, 0, 0, INT16_MAX, INT32_MAX};\n'
                '    msg_pack(&p, buf, 13);\n'
                '    msg_unpack(buf, 13, &f);\n'
                '    printf("%d %d\\n", f.delta, f.value);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Пишите байты сдвигами от старшего к младшему; знаковые поля предварительно приводите к '
              'беззнаковому типу той же ширины. При чтении: собрать беззнаковое и привести обратно к '
              'знаковому типу.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['13: 07 12 34 de ad be ef ff fe ff fe 79 60 ee ee ee',
                   '13 7 0x1234 0xdeadbeef -2 -100000',
                   '0 0 3',
                   '255 65535 4294967295 -32768 -2147483648',
                   '32767 2147483647']},
     {'id': 'c9-gray-gosper',
      'mode': 'c',
      'title': 'Код Грея и перебор масок: приём Госпера',
      'statement': 'gray(n) → код Грея (n ^ (n >> 1)); ungray(g) → обратное преобразование; hamming_dist(a, '
                   'b) → число отличающихся бит; next_same_popcount(x) → следующее по возрастанию число с '
                   'тем же числом единичных бит (приём Госпера: c = x & −x; r = x + c; (((r ^ x) >> 2) / c) '
                   '| r) или 0, если нет в 32 битах; count_masks(n, k) → число n-битных масок с ровно k '
                   'единицами, перебирая их приёмом Госпера (n ≤ 20).',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t gray(uint32_t n) { return 0; }\n'
                 'uint32_t ungray(uint32_t g) { return 0; }\n'
                 'int hamming_dist(uint32_t a, uint32_t b) { return -1; }\n'
                 'uint32_t next_same_popcount(uint32_t x) { return 7; }\n'
                 'int count_masks(int n, int k) { return -1; }\n',
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
                '    for (uint32_t i = 0; i < 8; i++) printf("%u:%u ", i, gray(i));\n'
                '    printf("\\n");\n'
                '    int ok = 1, adjacent = 1;\n'
                '    for (uint32_t i = 0; i < 100000; i++) {\n'
                '        if (ungray(gray(i)) != i) ok = 0;\n'
                '        if (hamming_dist(gray(i), gray(i + 1)) != 1) adjacent = 0;\n'
                '    }\n'
                '    printf("%d %d %d\\n", ok, adjacent, ungray(gray(0xFFFFFFFFu)) == 0xFFFFFFFFu);\n'
                '    printf("%d %d %d\\n", hamming_dist(0, 0), hamming_dist(0xFF, 0), '
                'hamming_dist(0xAAAAAAAAu, 0x55555555u));\n'
                '    uint32_t x = 7;\n'
                '    for (int i = 0; i < 8; i++) { printf("%u ", x); x = next_same_popcount(x); }\n'
                '    printf("\\n%u %u %u\\n", next_same_popcount(0), next_same_popcount(0xE0000000u), '
                'next_same_popcount(1));\n'
                '    printf("%d %d %d %d %d %d\\n", count_masks(4, 2), count_masks(6, 3), count_masks(10, '
                '0), count_masks(10, 10), count_masks(5, 6), count_masks(20, 10));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Госпер: c = x & −x; r = x + c; next = (((r ^ x) >> 2) / c) | r. Проверьте переполнение при x '
              '+ c.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['0:0 1:1 2:3 3:2 4:6 5:7 6:5 7:4',
                   '1 1 1',
                   '0 8 32',
                   '7 11 13 14 19 21 22 25',
                   '0 0 2',
                   '6 20 1 1 0 184756']},
     {'id': 'c9-subsets',
      'mode': 'c',
      'title': 'Подмножества масками: суммы и XOR',
      'statement': 'n ≤ 20 элементов массива перебираются битовыми масками. count_subset_sum(a, n, target) → '
                   'число непустых подмножеств с суммой target; best_subset_sum(a, n, limit) → наибольшая '
                   'сумма подмножества, не превосходящая limit (пустое — 0); max_subset_xor(a, n) → '
                   'наибольший XOR по всем подмножествам (≥ 0, пустое — 0) перебором; subset_mask_of(a, n, '
                   'target) → маска первого (с наименьшей маской) подмножества с суммой target или −1 '
                   '(пустое не учитывать).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int count_subset_sum(const int *a, int n, int target) { return -1; }\n'
                 'int best_subset_sum(const int *a, int n, int limit) { return -1; }\n'
                 'int max_subset_xor(const int *a, int n) { return -1; }\n'
                 'long subset_mask_of(const int *a, int n, int target) { return -2; }\n',
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
                '    int a[] = {3, 34, 4, 12, 5, 2};\n'
                '    printf("%d %d %d\\n", count_subset_sum(a, 6, 9), count_subset_sum(a, 6, 100), '
                'count_subset_sum(a, 6, 7));\n'
                '    printf("%d %d %d\\n", best_subset_sum(a, 6, 30), best_subset_sum(a, 6, 1), '
                'best_subset_sum(a, 6, 1000));\n'
                '    int b[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512};\n'
                '    printf("%d %ld %ld\\n", max_subset_xor(b, 10), subset_mask_of(b, 10, 1023), '
                'subset_mask_of(b, 10, 5000));\n'
                '    int c[] = {5, 1, 2, 12, 7, 3, 9, 11, 14, 6, 8, 10, 15, 4, 13, 20, 19, 18, 17, 16};\n'
                '    printf("%d %d\\n", count_subset_sum(c, 20, 100), max_subset_xor(c, 20));\n'
                '    printf("%d %d %ld\\n", count_subset_sum(a, 0, 0), max_subset_xor(a, 0), '
                'subset_mask_of(a, 6, 3));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Внешний цикл m от 1 до 2ⁿ − 1; внутренний — по битам маски. Сумму накапливайте в long long.',
      'expected': ['2 0 2', '26 0 60', '1023 1023 -1', '15029 31', '0 0 1']},
     {'id': 'c9-bit-matrix',
      'mode': 'c',
      'title': 'Битовая матрица 8×8 в одном uint64_t',
      'statement': 'Матрица 8×8 хранится в uint64_t: бит (r, c) — это бит номер r·8 + c (r — строка, c — '
                   'столбец, 0…7). bm_get(m, r, c), bm_set(m, r, c, v) → новая матрица; bm_transpose(m) — '
                   'транспонирование; bm_row(m, r) → байт строки; bm_col(m, c) → байт столбца (бит r — '
                   'строка r); bm_rotate90(m) — поворот по часовой стрелке; bm_flip_h(m) — отражение по '
                   'горизонтали (строка справа налево). Без циклов по 64 клеткам допустимо, но корректность '
                   'важнее.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'int bm_get(uint64_t m, int r, int c) { return -1; }\n'
                 'uint64_t bm_set(uint64_t m, int r, int c, int v) { return 0; }\n'
                 'uint64_t bm_transpose(uint64_t m) { return 0; }\n'
                 'uint8_t bm_row(uint64_t m, int r) { return 0; }\n'
                 'uint8_t bm_col(uint64_t m, int c) { return 0; }\n'
                 'uint64_t bm_rotate90(uint64_t m) { return 0; }\n'
                 'uint64_t bm_flip_h(uint64_t m) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void show(uint64_t m) {\n'
                '    for (int r = 0; r < 8; r++) {\n'
                "        for (int c = 0; c < 8; c++) putchar(bm_get(m, r, c) ? '#' : '.');\n"
                "        putchar('\\n');\n"
                '    }\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    uint64_t m = 0;\n'
                '    m = bm_set(m, 0, 0, 1);\n'
                '    m = bm_set(m, 0, 7, 1);\n'
                '    m = bm_set(m, 3, 2, 1);\n'
                '    m = bm_set(m, 7, 5, 1);\n'
                '    m = bm_set(m, 3, 2, 0);\n'
                '    m = bm_set(m, 1, 1, 1);\n'
                '    m = bm_set(m, 1, 2, 1);\n'
                '    m = bm_set(m, 1, 3, 1);\n'
                '    printf("%#llx\\n", (unsigned long long)m);\n'
                '    show(m);\n'
                '    printf("--\\n");\n'
                '    show(bm_transpose(m));\n'
                '    printf("--\\n");\n'
                '    show(bm_rotate90(m));\n'
                '    printf("--\\n");\n'
                '    show(bm_flip_h(m));\n'
                '    printf("%#x %#x %#x\\n", bm_row(m, 1), bm_col(m, 0), bm_col(m, 7));\n'
                '    printf("%d %d\\n", bm_transpose(bm_transpose(m)) == m, '
                'bm_rotate90(bm_rotate90(bm_rotate90(bm_rotate90(m)))) == m);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Номер бита (r, c) = r·8 + c. Транспонирование — обмен r и c; поворот на 90° по часовой: новая '
              'клетка (c, 7 − r) получает старую (r, c).',
      'expected': ['0x2000000000000e81',
                   '#......#',
                   '.###....',
                   '........',
                   '........',
                   '........',
                   '........',
                   '........',
                   '.....#..',
                   '--',
                   '#.......',
                   '.#......',
                   '.#......',
                   '.#......',
                   '........',
                   '.......#',
                   '........',
                   '#.......',
                   '--',
                   '.......#',
                   '......#.',
                   '......#.',
                   '......#.',
                   '........',
                   '#.......',
                   '........',
                   '.......#',
                   '--',
                   '#......#',
                   '....###.',
                   '........',
                   '........',
                   '........',
                   '........',
                   '........',
                   '..#.....',
                   '0xe 0x1 0x1',
                   '1 1']},
     {'id': 'c9-fix-shift',
      'mode': 'c',
      'title': 'Исправьте: неопределённые сдвиги',
      'statement': 'mask_low(n) (n от 0 до 32 единичных младших бит), sign_extend(v, bits) (расширить знаком '
                   'число из bits бит, 1 ≤ bits ≤ 32) и rotl(x, r) (r от 0 до 64, циклический сдвиг '
                   'uint32_t) написаны с неопределёнными сдвигами (сдвиг на ширину типа и отрицательного '
                   'значения). Программа запускается с UBSan и останавливается. Исправьте функции так, чтобы '
                   'не было UB для всех допустимых аргументов.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t mask_low(int n) {\n'
                 '    return (1u << n) - 1;\n'
                 '}\n'
                 '\n'
                 'int32_t sign_extend(uint32_t v, int bits) {\n'
                 '    return (int32_t)(v << (32 - bits)) >> (32 - bits);\n'
                 '}\n'
                 '\n'
                 'uint32_t rotl(uint32_t x, unsigned r) {\n'
                 '    return x << r | x >> (32 - r);\n'
                 '}\n',
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
                '    for (int n = 0; n <= 32; n += 8) printf("%#x ", mask_low(n));\n'
                '    printf("%#x %#x\\n", mask_low(1), mask_low(31));\n'
                '    printf("%d %d %d %d\\n", sign_extend(0xFF, 8), sign_extend(0x7F, 8), sign_extend(0x80, '
                '8), sign_extend(0x1FF, 8));\n'
                '    printf("%d %d %d\\n", sign_extend(0xFFFFFFFFu, 32), sign_extend(0x80000000u, 32), '
                'sign_extend(1, 1));\n'
                '    printf("%d %d\\n", sign_extend(0x800, 12), sign_extend(0x7FF, 12));\n'
                '    printf("%#x %#x %#x %#x\\n", rotl(0x80000001u, 0), rotl(0x80000001u, 1), '
                'rotl(0x12345678u, 32), rotl(0x12345678u, 64));\n'
                '    printf("%#x %#x\\n", rotl(0x12345678u, 4), rotl(0x12345678u, 36));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'mask_low(32) отдельно; sign_extend — через маску и проверку знакового бита без сдвигов '
              'отрицательных значений; rotl: r %= 32 и случай r == 0.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['0 0xff 0xffff 0xffffff 0xffffffff 0x1 0x7fffffff',
                   '-1 127 -128 -1',
                   '-1 -2147483648 -1',
                   '-2048 2047',
                   '0x80000001 0x3 0x12345678 0x12345678',
                   '0x23456781 0x23456781']},
     {'id': 'c9-fix-endian-read',
      'mode': 'c',
      'title': 'Исправьте: чтение чисел из буфера',
      'statement': 'read_u16_le, read_u32_le и read_u32_be читают числа из байтового буфера через приведение '
                   'указателей. Это неверно на «обратном» порядке байтов, нарушает выравнивание и строгий '
                   'алиасинг (под UBSan — остановка на невыровненном адресе). Перепишите функции на '
                   'побайтовое чтение со сдвигами; результат не должен зависеть от платформы.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint16_t read_u16_le(const unsigned char *p) {\n'
                 '    return *(const uint16_t *)p;\n'
                 '}\n'
                 '\n'
                 'uint32_t read_u32_le(const unsigned char *p) {\n'
                 '    return *(const uint32_t *)p;\n'
                 '}\n'
                 '\n'
                 'uint32_t read_u32_be(const unsigned char *p) {\n'
                 '    uint32_t v = *(const uint32_t *)p;\n'
                 '    return (v >> 24) | (v >> 8 & 0xFF00) | (v << 8 & 0xFF0000) | (v << 24);\n'
                 '}\n',
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
                '    unsigned char buf[16] = {0xAA, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0xFF, '
                '0xFE, 0xFD, 0xFC, 0x80, 0, 0};\n'
                '    for (int off = 0; off < 5; off++) {\n'
                '        printf("%d: %#x %#x %#x\\n", off, read_u16_le(buf + off), read_u32_le(buf + off), '
                'read_u32_be(buf + off));\n'
                '    }\n'
                '    printf("%#x %#x\\n", read_u32_le(buf + 9), read_u32_be(buf + 9));\n'
                '    printf("%u %u\\n", read_u16_le(buf + 12), read_u32_be(buf + 10));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'p[0] | p[1] << 8 | … — байты приводите к uint32_t до сдвига, иначе p[3] << 24 вылезет в '
              'знаковый int.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['0: 0x1aa 0x30201aa 0xaa010203',
                   '1: 0x201 0x4030201 0x1020304',
                   '2: 0x302 0x5040302 0x2030405',
                   '3: 0x403 0x6050403 0x3040506',
                   '4: 0x504 0x7060504 0x4050607',
                   '0xfcfdfeff 0xfffefdfc',
                   '33020 4278058112']},
     {'id': 'c9-fix-signed-compare',
      'mode': 'c',
      'title': 'Исправьте: знаковое и беззнаковое в сравнениях',
      'statement': 'in_range(x, lo, hi), has_more_than(s, n) (длина строки больше n; n может быть '
                   'отрицательным), last_n_sum(a, len, n) (сумма последних n элементов; n может быть больше '
                   'len; при n ≤ 0 — 0) и prev_index(i) (индекс i − 1, а для 0 — −1) написаны со смешанными '
                   'знаковыми и беззнаковыми типами и дают неверные результаты на границах. Исправьте их '
                   '(типы параметров менять нельзя).',
      'starter': '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '\n'
                 'int in_range(int x, unsigned lo, unsigned hi) {\n'
                 '    return x >= lo && x <= hi;\n'
                 '}\n'
                 '\n'
                 'int has_more_than(const char *s, int n) {\n'
                 '    return strlen(s) > n;\n'
                 '}\n'
                 '\n'
                 'long last_n_sum(const int *a, size_t len, int n) {\n'
                 '    long s = 0;\n'
                 '    for (size_t i = len - n; i < len; i++) s += a[i];\n'
                 '    return s;\n'
                 '}\n'
                 '\n'
                 'long prev_index(size_t i) {\n'
                 '    return i - 1;\n'
                 '}\n',
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
                '    printf("%d %d %d %d\\n", in_range(5, 1, 10), in_range(-1, 0, 10), in_range(-1, 0, '
                '0xFFFFFFFFu), in_range(0, 0, 0));\n'
                '    printf("%d %d %d %d\\n", has_more_than("abc", 2), has_more_than("abc", 3), '
                'has_more_than("abc", -1), has_more_than("", -1));\n'
                '    int a[] = {1, 2, 3, 4, 5};\n'
                '    printf("%ld %ld %ld %ld %ld\\n", last_n_sum(a, 5, 2), last_n_sum(a, 5, 5), '
                'last_n_sum(a, 5, 9), last_n_sum(a, 5, 0), last_n_sum(a, 5, -3));\n'
                '    printf("%ld %ld\\n", last_n_sum(a, 0, 3), last_n_sum(a, 1, 1));\n'
                '    printf("%ld %ld %ld\\n", prev_index(0), prev_index(1), prev_index(100));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сначала разберите отрицательные значения, затем приводите к size_t/unsigned явно; i − 1 для '
              'size_t при i = 0 даёт огромное число.',
      'expected': ['1 0 0 1', '1 0 1 1', '9 15 15 0 0', '0 1', '-1 0 99']},
     {'id': 'c9-float-bits-string',
      'mode': 'c',
      'title': 'Двоичная запись float и double строкой',
      'statement': 'float_bits_str(f, buf) пишет в buf (не менее 36 байт) строку «s eeeeeeee '
                   'mmmmmmmmmmmmmmmmmmmmmmm» (знак, пробел, 8 бит порядка, пробел, 23 бита мантиссы; всего '
                   '34 символа) и завершающий ноль; double_bits_str(d, buf) — «s eeeeeeeeeee mmmm…» (1, 11 и '
                   '52 бита). from_bits_str(buf) → float по такой строке (пробелы игнорируются; строка '
                   'корректна). Используйте memcpy, а не приведение указателей.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'void float_bits_str(float f, char *buf) {}\n'
                 'void double_bits_str(double d, char *buf) {}\n'
                 'float from_bits_str(const char *buf) { return 0; }\n',
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
                '    char b[100];\n'
                '    float fs[] = {1.0f, -2.5f, 0.1f, 0.0f, -0.0f, 1e-40f, 1.0f / 0.0f};\n'
                '    for (size_t i = 0; i < sizeof fs / sizeof fs[0]; i++) {\n'
                '        float_bits_str(fs[i], b);\n'
                '        printf("%s %zu %d\\n", b, strlen(b), from_bits_str(b) == fs[i]);\n'
                '    }\n'
                '    double ds[] = {1.0, -0.1, 3.141592653589793, 0.0};\n'
                '    for (size_t i = 0; i < sizeof ds / sizeof ds[0]; i++) {\n'
                '        double_bits_str(ds[i], b);\n'
                '        printf("%s %zu\\n", b, strlen(b));\n'
                '    }\n'
                '    printf("%g %g\\n", from_bits_str("0 10000001 01000000000000000000000"), '
                'from_bits_str("1 01111110 00000000000000000000000"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Выводите биты от старшего к младшему; пробел вставляйте после знакового бита и после поля '
              'порядка. Для обратного преобразования соберите 32 бита в uint32_t и скопируйте memcpy.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=undefined -fno-sanitize-recover=all',
      'expected': ['0 01111111 00000000000000000000000 34 1',
                   '1 10000000 01000000000000000000000 34 1',
                   '0 01111011 10011001100110011001101 34 1',
                   '0 00000000 00000000000000000000000 34 1',
                   '1 00000000 00000000000000000000000 34 1',
                   '0 00000000 00000010001011011000010 34 1',
                   '0 11111111 00000000000000000000000 34 1',
                   '0 01111111111 0000000000000000000000000000000000000000000000000000 66',
                   '1 01111111011 1001100110011001100110011001100110011001100110011010 66',
                   '0 10000000000 1001001000011111101101010100010001000010110100011000 66',
                   '0 00000000000 0000000000000000000000000000000000000000000000000000 66',
                   '5 -0.5']},
     {'id': 'c9-tagged-union',
      'mode': 'c',
      'title': 'Размеченное объединение значений',
      'statement': 'struct value { enum { V_INT, V_DBL, V_STR } tag; union { long i; double d; const char '
                   '*s; } u; }. Конструкторы v_int, v_dbl, v_str; v_add(a, b): int + int → int; если хотя бы '
                   'один операнд double — результат double; если любой операнд — строка, результат v_int(−1) '
                   '(ошибка). v_equal(a, b): значения равны, если теги совпадают и содержимое равно (строки '
                   '— по содержимому), либо одно int, другое double и числа равны. v_format(v, buf, size) — '
                   'записать «i:42», «d:2.50» (два знака) или «s:текст»; возвращает длину как snprintf.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct value { enum { V_INT, V_DBL, V_STR } tag; union { long i; double d; const char *s; '
                 '} u; };\n'
                 '\n'
                 'struct value v_int(long i) { struct value v = {V_INT, {0}}; return v; }\n'
                 'struct value v_dbl(double d) { struct value v = {V_INT, {0}}; return v; }\n'
                 'struct value v_str(const char *s) { struct value v = {V_INT, {0}}; return v; }\n'
                 'struct value v_add(struct value a, struct value b) { return v_int(-9); }\n'
                 'int v_equal(struct value a, struct value b) { return -1; }\n'
                 'size_t v_format(struct value v, char *buf, size_t size) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void show(struct value v) {\n'
                '    char b[32];\n'
                '    size_t n = v_format(v, b, sizeof b);\n'
                '    printf("%s(%zu) ", b, n);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    struct value a = v_int(40), b = v_int(2), c = v_dbl(2.5), s = v_str("hi"), s2 = '
                'v_str("hi");\n'
                '    show(v_add(a, b)); show(v_add(a, c)); show(v_add(c, c)); show(v_add(s, a)); '
                'show(v_add(c, s));\n'
                '    printf("\\n");\n'
                '    printf("%d %d %d %d\\n", v_equal(a, a), v_equal(a, b), v_equal(v_int(3), v_dbl(3.0)), '
                'v_equal(v_dbl(3.5), v_int(3)));\n'
                '    printf("%d %d %d\\n", v_equal(s, s2), v_equal(s, v_str("ho")), v_equal(s, a));\n'
                '    char tiny[4];\n'
                '    size_t n = v_format(v_str("long string here"), tiny, sizeof tiny);\n'
                '    printf("[%s] %zu\\n", tiny, n);\n'
                '    printf("%d\\n", sizeof(struct value) <= 16);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'union хранит одно из значений; тег говорит какое. Для v_format — snprintf по тегу; '
              'возвращайте длину полного результата.',
      'expected': ['i:42(4) d:42.50(7) d:5.00(6) i:-1(4) i:-1(4)', '1 0 1 0', '1 0 0', '[s:l] 18', '1']}]}
