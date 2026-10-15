"""Задачи книги «От assembler к языку C»: главы 1–5 (код компилируется gcc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {1: [{'id': 'c1-hello-return',
      'mode': 'c',
      'title': 'Первая программа: вывод и код возврата',
      'statement': 'Напишите функцию int run(void): она печатает строку «Hello, C!» с переводом строки и '
                   'возвращает число 3 (код завершения). Не забудьте подключить заголовок, в котором '
                   'объявлен printf.',
      'starter': 'int run(void) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int code = run();\n'
                '    printf("exit code: %d\\n", code);\n'
                '    return 0;\n'
                '}\n',
      'hint': '#include <stdio.h> в начале файла; printf("...\\n"); return 3;',
      'expected': ['Hello, C!', 'exit code: 3']},
     {'id': 'c1-sizes',
      'mode': 'c',
      'title': 'sizeof: размеры типов на этой платформе',
      'statement': 'Напишите void print_sizes(void): одной строкой через пробел напечатайте sizeof типов '
                   'char, short, int, long, long long, float, double и void * (метка для size_t — %zu), в '
                   'конце перевод строки.',
      'starter': '#include <stdio.h>\n\nvoid print_sizes(void) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    print_sizes();\n'
                '    return 0;\n'
                '}\n',
      'hint': 'sizeof(тип) возвращает size_t; печатайте его меткой %zu.',
      'expected': ['1 2 4 8 8 4 8 8']},
     {'id': 'c1-sum-wrap',
      'mode': 'c',
      'title': 'Беззнаковая сумма заворачивается',
      'statement': 'sum8(const uint8_t *p, size_t n) → uint8_t: сумма байтов, результат по модулю 256. '
                   'sum32(const uint8_t *p, size_t n) → uint32_t: сумма по модулю 2³². Типы из <stdint.h> '
                   'нужны, чтобы размер был ровно такой, какой требуется.',
      'starter': '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'uint8_t sum8(const uint8_t *p, size_t n) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'uint32_t sum32(const uint8_t *p, size_t n) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    uint8_t a[] = {200, 100, 50};\n'
                '    printf("%u %u\\n", sum8(a, 3), sum32(a, 3));\n'
                '    uint8_t b[300];\n'
                '    memset(b, 255, sizeof b);\n'
                '    printf("%u %u\\n", sum8(b, 300), sum32(b, 300));\n'
                '    printf("%u %u\\n", sum8(a, 0), sum32(a, 0));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Накапливайте сумму в переменной того же типа, что и результат: арифметика uint8_t '
              'заворачивается сама.',
      'expected': ['94 350', '212 76500', '0 0']},
     {'id': 'c1-floor-div',
      'mode': 'c',
      'title': 'Деление как в Python: пол и остаток',
      'statement': 'В C деление округляет к нулю, а % даёт остаток со знаком делимого. Напишите floor_div(a, '
                   'b) и floor_mod(a, b) с питонской семантикой (округление вниз; остаток имеет знак '
                   'делителя). b ≠ 0.',
      'starter': 'int floor_div(int a, int b) {\n'
                 '    return a / b;\n'
                 '}\n'
                 '\n'
                 'int floor_mod(int a, int b) {\n'
                 '    return a % b;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int cases[][2] = {{7, 2}, {-7, 2}, {7, -2}, {-7, -2}, {6, 3}, {-6, 3}, {0, 5}, {5, 7}, '
                '{-5, 7}};\n'
                '    for (int i = 0; i < 9; i++) {\n'
                '        int a = cases[i][0], b = cases[i][1];\n'
                '        printf("%d %d: %d %d\\n", a, b, floor_div(a, b), floor_mod(a, b));\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Если остаток не нулевой и знаки a и b различаются, частное нужно уменьшить на 1, а остаток '
              'увеличить на b.',
      'expected': ['7 2: 3 1',
                   '-7 2: -4 1',
                   '7 -2: -4 -1',
                   '-7 -2: 3 -1',
                   '6 3: 2 0',
                   '-6 3: -2 0',
                   '0 5: 0 0',
                   '5 7: 0 5',
                   '-5 7: -1 2']},
     {'id': 'c1-add-checked',
      'mode': 'c',
      'title': 'Сложение без неопределённого поведения',
      'statement': 'add_checked(int a, int b, int *out) → int: если a + b помещается в int — записать сумму '
                   'в *out и вернуть 1; иначе вернуть 0 и *out не менять. Проверять нужно ДО сложения: '
                   'переполнение знакового — неопределённое поведение. Встроенными функциями __builtin_* '
                   'пользоваться нельзя.',
      'starter': 'int add_checked(int a, int b, int *out) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
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
                '    int r = -1, ok;\n'
                '    ok = add_checked(1, 2, &r);                printf("%d %d\\n", ok, r);\n'
                '    ok = add_checked(INT_MAX, 1, &r);          printf("%d %d\\n", ok, r);\n'
                '    ok = add_checked(INT_MAX, 0, &r);          printf("%d %d\\n", ok, r);\n'
                '    ok = add_checked(INT_MIN, -1, &r);         printf("%d %d\\n", ok, r);\n'
                '    ok = add_checked(INT_MIN, INT_MAX, &r);    printf("%d %d\\n", ok, r);\n'
                '    ok = add_checked(-5, -7, &r);              printf("%d %d\\n", ok, r);\n'
                '    printf("builtins: %d\\n", src_count("__bu" "iltin"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Если b > 0, переполнение произойдёт при a > INT_MAX - b; для b < 0 — при a < INT_MIN - b. '
              'Вычитание тут безопасно.',
      'expected': ['1 3', '0 3', '1 2147483647', '0 2147483647', '1 -1', '1 -12', 'builtins: 0']},
     {'id': 'c1-wrap-add',
      'mode': 'c',
      'title': 'Заворачивание и приведение к знаковому',
      'statement': 'add_wrap(uint32_t a, uint32_t b) → uint32_t — сумма по модулю 2³². as_signed(uint32_t x) '
                   '→ int32_t — то же 32-битное слово, прочитанное как знаковое число (дополнительный код). '
                   'Именно так процессор видит один и тот же регистр.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t add_wrap(uint32_t a, uint32_t b) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int32_t as_signed(uint32_t x) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%u\\n", add_wrap(4000000000u, 500000000u));\n'
                '    printf("%u\\n", add_wrap(0, 0));\n'
                '    printf("%d %d %d\\n", as_signed(0xFFFFFFFFu), as_signed(0x80000000u), '
                'as_signed(0x7FFFFFFFu));\n'
                '    printf("%d\\n", as_signed(add_wrap(0x7FFFFFFFu, 1)));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Приведение (int32_t)x переинтерпретирует тот же набор бит в дополнительном коде; gcc '
              'определяет его именно так.',
      'expected': ['205032704', '0', '-1 -2147483648 2147483647', '-2147483648']},
     {'id': 'c1-popcount',
      'mode': 'c',
      'title': 'Число единичных битов',
      'statement': 'popcount(uint32_t x) → int — количество единичных битов. Напишите цикл, который каждый '
                   'раз сбрасывает младшую единицу (x &= x - 1). Встроенными функциями __builtin_* '
                   'пользоваться нельзя.',
      'starter': '#include <stdint.h>\n\nint popcount(uint32_t x) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
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
                '    uint32_t v[] = {0, 1, 2, 3, 255, 256, 0x80000000u, 0xFFFFFFFFu, 0xDEADBEEFu};\n'
                '    for (int i = 0; i < 9; i++) printf("%d ", popcount(v[i]));\n'
                '    printf("\\n");\n'
                '    printf("builtins: %d\\n", src_count("__bu" "iltin"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'x & (x - 1) обнуляет самую младшую единицу, поэтому число итераций равно числу единиц.',
      'expected': ['0 1 1 2 8 1 1 32 24', 'builtins: 0']},
     {'id': 'c1-bit-ops',
      'mode': 'c',
      'title': 'set / clear / toggle / test',
      'statement': 'Для uint32_t x и номера бита n (0..31): set_bit, clear_bit, toggle_bit возвращают новое '
                   'значение; test_bit возвращает 0 или 1.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t set_bit(uint32_t x, int n) {\n'
                 '    return x;\n'
                 '}\n'
                 '\n'
                 'uint32_t clear_bit(uint32_t x, int n) {\n'
                 '    return x;\n'
                 '}\n'
                 '\n'
                 'uint32_t toggle_bit(uint32_t x, int n) {\n'
                 '    return x;\n'
                 '}\n'
                 '\n'
                 'int test_bit(uint32_t x, int n) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    uint32_t x = 0;\n'
                '    x = set_bit(x, 0); x = set_bit(x, 31); x = set_bit(x, 4);\n'
                '    printf("%08x\\n", x);\n'
                '    x = clear_bit(x, 0); x = toggle_bit(x, 4); x = toggle_bit(x, 8);\n'
                '    printf("%08x\\n", x);\n'
                '    printf("%d %d %d\\n", test_bit(x, 31), test_bit(x, 8), test_bit(x, 0));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Используйте 1u << n (беззнаковую единицу), иначе сдвиг на 31 затронет знаковый бит.',
      'expected': ['80000011', '80000100', '1 1 0']},
     {'id': 'c1-bit-fields',
      'mode': 'c',
      'title': 'Выделить и вставить поле из битов',
      'statement': 'get_bits(x, lo, n) → uint32_t: n бит начиная с бита lo (1 ≤ n ≤ 32 − lo), сдвинутых к '
                   'нулю. set_bits(x, lo, n, v) → uint32_t: заменить это поле значением v (лишние старшие '
                   'биты v отбросить). Так устроены поля команд процессора.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t get_bits(uint32_t x, int lo, int n) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'uint32_t set_bits(uint32_t x, int lo, int n, uint32_t v) {\n'
                 '    return x;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    uint32_t x = 0xDEADBEEF;\n'
                '    printf("%x %x %x\\n", get_bits(x, 0, 4), get_bits(x, 4, 8), get_bits(x, 28, 4));\n'
                '    printf("%08x\\n", set_bits(x, 8, 8, 0x12));\n'
                '    printf("%08x\\n", set_bits(0, 5, 3, 0xFF));\n'
                '    printf("%x\\n", get_bits(0xFFFFFFFFu, 0, 32));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Маска из n единиц: (1u << n) - 1; для n = 32 сдвиг запрещён — обработайте отдельно.',
      'expected': ['f ee d', 'dead12ef', '000000e0', 'ffffffff']},
     {'id': 'c1-pow2',
      'mode': 'c',
      'title': 'Степени двойки',
      'statement': 'is_pow2(x) → int: 1, если x — степень двойки (x > 0). next_pow2(x) → uint32_t: '
                   'наименьшая степень двойки ≥ x (для 0 вернуть 1; значения больше 2³¹ не передаются). Без '
                   'циклов по всем степеням — битовыми приёмами.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'int is_pow2(uint32_t x) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'uint32_t next_pow2(uint32_t x) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    uint32_t v[] = {0, 1, 2, 3, 4, 5, 63, 64, 65, 1000, 0x40000000u, 0x7FFFFFFFu};\n'
                '    for (int i = 0; i < 12; i++) printf("%u:%d:%u\\n", v[i], is_pow2(v[i]), '
                'next_pow2(v[i]));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Степень двойки имеет ровно одну единицу: x & (x - 1) == 0. Для next_pow2 размножьте старшую '
              'единицу вправо и прибавьте 1.',
      'expected': ['0:0:1',
                   '1:1:1',
                   '2:1:2',
                   '3:0:4',
                   '4:1:4',
                   '5:0:8',
                   '63:0:64',
                   '64:1:64',
                   '65:0:128',
                   '1000:0:1024',
                   '1073741824:1:1073741824',
                   '2147483647:0:2147483648']},
     {'id': 'c1-rotate',
      'mode': 'c',
      'title': 'Циклический сдвиг',
      'statement': 'rotl32(x, n) и rotr32(x, n) — циклический сдвиг uint32_t на n разрядов; n может быть '
                   'любым (в том числе 0 и ≥ 32 — берите n mod 32). Сдвиг на 32 разряда в C — неопределённое '
                   'поведение, избегайте его.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t rotl32(uint32_t x, unsigned n) {\n'
                 '    return x;\n'
                 '}\n'
                 '\n'
                 'uint32_t rotr32(uint32_t x, unsigned n) {\n'
                 '    return x;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    uint32_t x = 0x80000001u;\n'
                '    printf("%08x %08x\\n", rotl32(x, 1), rotr32(x, 1));\n'
                '    printf("%08x %08x\\n", rotl32(x, 0), rotl32(x, 32));\n'
                '    printf("%08x %08x\\n", rotl32(0x12345678u, 8), rotr32(0x12345678u, 8));\n'
                '    printf("%08x\\n", rotl32(0x12345678u, 36));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'n &= 31; а при n == 0 вернуть x — иначе придётся сдвигать на 32.',
      'expected': ['00000003 c0000000', '80000001 80000001', '34567812 78123456', '23456781']},
     {'id': 'c1-endian',
      'mode': 'c',
      'title': 'Порядок байтов',
      'statement': 'is_little_endian(void) → int: определить порядок байтов, прочитав первый байт числа 1 '
                   'через указатель на unsigned char. bswap32(x) → uint32_t: развернуть порядок байтов слова '
                   '(0x11223344 → 0x44332211) без __builtin_bswap32.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'int is_little_endian(void) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'uint32_t bswap32(uint32_t x) {\n'
                 '    return x;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
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
                '    printf("%08x %08x %08x\\n", bswap32(0x11223344u), bswap32(0), bswap32(0xFF000001u));\n'
                '    printf("builtins: %d\\n", src_count("__bu" "iltin"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Доступ к байтам объекта допустим через unsigned char *: первый байт числа 1 равен 1 на '
              'little-endian машине.',
      'expected': ['1', '44332211 00000000 010000ff', 'builtins: 0']},
     {'id': 'c1-sign-extend',
      'mode': 'c',
      'title': 'Знаковое расширение, как у непосредственных RISC-V',
      'statement': 'sign_extend(uint32_t x, int bits) → int32_t: значение хранится в младших bits разрядах '
                   '(1 ≤ bits ≤ 32) в дополнительном коде; верните его как int32_t. Так расширяется '
                   '12-битная константа команды addi. Например, sign_extend(0xFFF, 12) = −1.',
      'starter': '#include <stdint.h>\n\nint32_t sign_extend(uint32_t x, int bits) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d\\n", sign_extend(0xFFF, 12), sign_extend(0x7FF, 12), '
                'sign_extend(0x800, 12));\n'
                '    printf("%d %d\\n", sign_extend(0xFF, 8), sign_extend(0x7F, 8));\n'
                '    printf("%d %d\\n", sign_extend(1, 1), sign_extend(0x80000000u, 32));\n'
                '    printf("%d\\n", sign_extend(0x1234FFF, 12));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Приём: (x ^ m) - m, где m = 1 << (bits - 1); предварительно обрежьте лишние старшие биты '
              'маской.',
      'expected': ['-1 2047 -2048', '-1 127', '-1 -2147483648', '-1']},
     {'id': 'c1-riscv-encode',
      'mode': 'c',
      'title': 'Собираем команду RISC-V addi',
      'statement': 'encode_addi(rd, rs1, imm) → uint32_t: 32-битное слово команды addi rd, rs1, imm (формат '
                   'I): imm[11:0] в битах 31..20, rs1 в 19..15, funct3 = 0 в 14..12, rd в 11..7, opcode 0x13 '
                   'в 6..0. decode_imm(instr) → int: знаковая 12-битная константа команды. Пример: addi a0, '
                   'a0, 1 = 0x00150513.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t encode_addi(int rd, int rs1, int imm) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int decode_imm(uint32_t instr) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%08x\\n", encode_addi(10, 10, 1));\n'
                '    printf("%08x\\n", encode_addi(2, 2, -16));\n'
                '    printf("%08x\\n", encode_addi(5, 0, 2047));\n'
                '    printf("%d %d %d\\n", decode_imm(0x00150513u), decode_imm(0xFF010113u), '
                'decode_imm(0x7FF00293u));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Константу imm (может быть отрицательной) обрежьте маской 0xFFF и сдвиньте на 20; поля '
              'складываются через |.',
      'expected': ['00150513', 'ff010113', '7ff00293', '1 -16 2047']},
     {'id': 'c1-printf-row',
      'mode': 'c',
      'title': 'printf: колонки',
      'statement': 'print_row(const char *name, int n): напечатайте одну строку: имя по левому краю в 8 '
                   'позициях, затем «|», число по правому краю в 6 позициях, «|», число в шестнадцатеричном '
                   'виде из восьми цифр с нулями слева, «|», символ с кодом n (если 32 ≤ n < 127, иначе '
                   '«.»). Например, print_row("abc", 65) → «abc     |    65|00000041|A».',
      'starter': '#include <stdio.h>\n\nvoid print_row(const char *name, int n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    print_row("abc", 65);\n'
                '    print_row("tab", 9);\n'
                '    print_row("long_name_x", 100000);\n'
                '    print_row("z", 126);\n'
                '    return 0;\n'
                '}\n',
      'hint': '%-8s — по левому краю, %6d — по правому, %08x — шестнадцатеричное с нулями; число передавайте '
              'как unsigned.',
      'expected': ['abc     |    65|00000041|A',
                   'tab     |     9|00000009|.',
                   'long_name_x|100000|000186a0|.',
                   'z       |   126|0000007e|~']},
     {'id': 'c1-show-number',
      'mode': 'c',
      'title': 'Одно число в разных видах',
      'statement': 'show_number(unsigned n): напечатайте в одной строке через пробел: десятичное, '
                   'шестнадцатеричное с префиксом 0x, восьмеричное с префиксом 0 и двоичное (8 разрядов, '
                   'если n < 256, иначе без ограничений на ширину, без ведущих нулей сверх 8). Двоичную '
                   'запись придётся построить самостоятельно: в printf нет метки для неё.',
      'starter': '#include <stdio.h>\n\nvoid show_number(unsigned n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    show_number(5);\n'
                '    show_number(255);\n'
                '    show_number(256);\n'
                '    show_number(0);\n'
                '    show_number(100000);\n'
                '    return 0;\n'
                '}\n',
      'hint': '%#x даёт 0x…, %#o даёт 0…; биты собирайте в массив младшим вперёд и печатайте в обратном '
              'порядке.',
      'expected': ['5 0x5 05 00000101',
                   '255 0xff 0377 11111111',
                   '256 0x100 0400 100000000',
                   '0 0 0 00000000',
                   '100000 0x186a0 0303240 11000011010100000']},
     {'id': 'c1-snprintf',
      'mode': 'c',
      'title': 'snprintf: безопасная запись в буфер',
      'statement': 'fmt_hex(char *buf, size_t cap, uint32_t v) → int: запишите в buf строку «0x» и восемь '
                   'шестнадцатеричных цифр (строчные) через snprintf; верните то, что вернул snprintf — '
                   'длину, которая была бы записана без ограничения cap (при нехватке места строка '
                   'обрезается, но остаётся корректной).',
      'starter': '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'int fmt_hex(char *buf, size_t cap, uint32_t v) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    char b[32];\n'
                '    int n = fmt_hex(b, sizeof b, 0xBEEF);\n'
                '    printf("%d [%s]\\n", n, b);\n'
                '    char s[6];\n'
                '    n = fmt_hex(s, sizeof s, 0xDEADBEEF);\n'
                '    printf("%d [%s] %d\\n", n, s, (int)strlen(s));\n'
                '    n = fmt_hex(s, 0, 1);\n'
                '    printf("%d\\n", n);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'snprintf(buf, cap, "0x%08x", v) возвращает длину полного результата, даже если он не '
              'поместился.',
      'expected': ['10 [0x0000beef]', '10 [0xdea] 5', '10']},
     {'id': 'c1-float-compare',
      'mode': 'c',
      'title': 'Сравнение дробных чисел',
      'statement': 'nearly_equal(double a, double b, double eps) → int: 1, если |a − b| ≤ eps · max(1, |a|, '
                   '|b|) (относительная точность для больших чисел, абсолютная для малых). Нужно для '
                   'проверки, что 0.1 + 0.2 «равно» 0.3.',
      'starter': '#include <math.h>\n'
                 '\n'
                 'int nearly_equal(double a, double b, double eps) {\n'
                 '    return a == b;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    double x = 0.1 + 0.2;\n'
                '    printf("%d %d\\n", x == 0.3, nearly_equal(x, 0.3, 1e-9));\n'
                '    printf("%d\\n", nearly_equal(1e10, 1e10 + 1, 1e-9));\n'
                '    printf("%d\\n", nearly_equal(1e10, 1e10 + 100, 1e-9));\n'
                '    printf("%d\\n", nearly_equal(0.0, 1e-12, 1e-9));\n'
                '    printf("%d\\n", nearly_equal(0.0, 1e-3, 1e-9));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'fabs и fmax — из <math.h>; не забудьте, что компоновка с математической библиотекой уже '
              'включена (-lm).',
      'expected': ['0 1', '1', '0', '1', '0']},
     {'id': 'c1-round',
      'mode': 'c',
      'title': 'Округление и усечение',
      'statement': 'round_half_up(double x) → int: ближайшее целое, половины — от нуля (2.5 → 3, −2.5 → −3), '
                   'только через приведение к int и сложение (без round из <math.h>). floor_int(double x) → '
                   'int: округление вниз (−2.5 → −3), тоже без floor. Помните, что (int) отбрасывает дробную '
                   'часть, то есть округляет к нулю.',
      'starter': 'int round_half_up(double x) {\n'
                 '    return (int)x;\n'
                 '}\n'
                 '\n'
                 'int floor_int(double x) {\n'
                 '    return (int)x;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
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
                '    double v[] = {2.5, -2.5, 2.4, -2.4, 0.5, -0.5, 7.0, -7.0, 0.49999};\n'
                '    for (int i = 0; i < 9; i++) printf("%d/%d ", round_half_up(v[i]), floor_int(v[i]));\n'
                '    printf("\\n");\n'
                '    printf("libm: %d %d\\n", src_count("rou" "nd("), src_count("flo" "or("));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для отрицательных чисел при округлении «от нуля» надо вычитать 0.5, а для floor учтите, что '
              '(int) уже округлил к нулю.',
      'expected': ['3/2 -3/-3 2/2 -2/-3 1/0 -1/-1 7/7 -7/-7 0/0', 'libm: 0 0']},
     {'id': 'c1-temp-table',
      'mode': 'c',
      'title': 'Таблица температур',
      'statement': 'print_table(void): напечатайте таблицу перевода из градусов Цельсия в Фаренгейта для '
                   '−40, −20, 0, …, 100 (шаг 20): в каждой строке «C = %4d  F = %6.1f» (Цельсий — целое в 4 '
                   'позициях, Фаренгейт — дробное в 6 позициях с одним знаком). F = C · 9 / 5 + 32.',
      'starter': '#include <stdio.h>\n\nvoid print_table(void) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    print_table();\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Умножайте на 9.0 / 5.0, а не на 9 / 5: целое деление дало бы 1.',
      'expected': ['C =  -40  F =  -40.0',
                   'C =  -20  F =   -4.0',
                   'C =    0  F =   32.0',
                   'C =   20  F =   68.0',
                   'C =   40  F =  104.0',
                   'C =   60  F =  140.0',
                   'C =   80  F =  176.0',
                   'C =  100  F =  212.0']},
     {'id': 'c1-min-branchless',
      'mode': 'c',
      'title': 'Минимум и максимум без ветвлений',
      'statement': 'min_bl(int a, int b) и max_bl(int a, int b) без if и тернарного оператора, через '
                   'побитовые операции и результат сравнения (0 или 1): min = b ^ ((a ^ b) & -(a < b)). '
                   'Слова if и «?» в коде использовать нельзя.',
      'starter': 'int min_bl(int a, int b) {\n'
                 '    return a;\n'
                 '}\n'
                 '\n'
                 'int max_bl(int a, int b) {\n'
                 '    return a;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
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
                '    int v[][2] = {{3, 5}, {5, 3}, {-1, 1}, {7, 7}, {INT_MIN, INT_MAX}, {-9, -4}};\n'
                '    for (int i = 0; i < 6; i++) printf("%d/%d ", min_bl(v[i][0], v[i][1]), max_bl(v[i][0], '
                'v[i][1]));\n'
                '    printf("\\n");\n'
                '    printf("branches: %d %d\\n", src_count("if" " ("), src_count(" " "? "));\n'
                '    return 0;\n'
                '}\n',
      'hint': '-(a < b) равно 0 или -1 (все единицы) — получается маска, выбирающая нужное из a ^ b.',
      'expected': ['3/5 3/5 -1/1 7/7 -2147483648/2147483647 -9/-4', 'branches: 0 0']},
     {'id': 'c1-macros',
      'mode': 'c',
      'title': 'Макросы с правильными скобками',
      'statement': 'Определите макросы (в начале решения): SQUARE(x) — квадрат; MAX(a, b) — большее из двух; '
                   'KB — 1024 (как выражение без знака), MB — KB * 1024; IS_ODD(x) — 1 для нечётного. '
                   'Макросы подставляются как текст: SQUARE(1 + 2) должен давать 9, а не 5; IS_ODD(7 - 2 * '
                   '4) — 1.',
      'starter': '/* ваши макросы */\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d\\n", SQUARE(1 + 2), SQUARE(-3));\n'
                '    printf("%d %d\\n", MAX(2, 7), MAX(1 + 5, 2 * 3 - 1));\n'
                '    printf("%u %u\\n", KB, MB);\n'
                '    printf("%d %d %d\\n", IS_ODD(7 - 2 * 4), IS_ODD(10), IS_ODD(3));\n'
                '    printf("%u\\n", 3 * MB / KB);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Каждый параметр оборачивайте в скобки и всё тело макроса тоже: ((x) * (x)).',
      'expected': ['9 9', '7 6', '1024 1048576', '1 0 1', '3072']},
     {'id': 'c1-enum',
      'mode': 'c',
      'title': 'enum: режимы и их имена',
      'statement': 'Опишите enum mode { MODE_OFF, MODE_ON, MODE_AUTO = 5, MODE_BOOST } и функцию const char '
                   '*mode_name(enum mode m), которая возвращает «off», «on», «auto», «boost» (для остальных '
                   'значений — «?»). Значения констант: 0, 1, 5, 6.',
      'starter': '/* enum и функция */\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d %d\\n", MODE_OFF, MODE_ON, MODE_AUTO, MODE_BOOST);\n'
                '    printf("%s %s %s %s %s\\n", mode_name(MODE_OFF), mode_name(MODE_ON), '
                'mode_name(MODE_AUTO), mode_name(MODE_BOOST), mode_name((enum mode)3));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'switch по enum с return в каждой ветке; после switch — возврат для неизвестных значений.',
      'expected': ['0 1 5 6', 'off on auto boost ?']},
     {'id': 'c1-mixed-compare',
      'mode': 'c',
      'title': 'Знаковое с беззнаковым',
      'statement': 'Две функции с хитрыми приведениями типов. less_mixed(int a, unsigned b) → int: просто '
                   'вернуть a < b (в C это сравнение беззнаковое: a преобразуется в unsigned!). '
                   'less_safe(int a, unsigned b) → int: правильное сравнение «математических» значений '
                   '(отрицательное всегда меньше). Драйвер покажет разницу.',
      'starter': 'int less_mixed(int a, unsigned b) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'int less_safe(int a, unsigned b) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {-1, 0, 5, -100};\n'
                '    unsigned b[] = {1, 1, 3, 4000000000u};\n'
                '    for (int i = 0; i < 4; i++) printf("%d %u: %d %d\\n", a[i], b[i], less_mixed(a[i], '
                'b[i]), less_safe(a[i], b[i]));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'В less_mixed ничего не нужно кроме a < b — именно это и есть «сюрприз»; в less_safe сначала '
              'проверьте знак a.',
      'expected': ['-1 1: 0 1', '0 1: 1 1', '5 3: 0 0', '-100 4000000000: 0 1']},
     {'id': 'c1-swap-halves',
      'mode': 'c',
      'title': 'Поменять половинки слова',
      'statement': 'swap_halves(uint32_t x) → uint32_t: поменять местами старшие и младшие 16 бит. '
                   'swap_bytes16(uint16_t x) → uint16_t: поменять два байта. Результат типа uint16_t нужно '
                   'корректно привести: арифметика идёт в int.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t swap_halves(uint32_t x) {\n'
                 '    return x;\n'
                 '}\n'
                 '\n'
                 'uint16_t swap_bytes16(uint16_t x) {\n'
                 '    return x;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%08x %08x\\n", swap_halves(0x12345678u), swap_halves(0xFFFF0000u));\n'
                '    printf("%04x %04x\\n", swap_bytes16(0x1234), swap_bytes16(0x00FF));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'В выражении x << 8 для uint16_t вычисление идёт в int; результат нужно привести обратно к '
              'uint16_t.',
      'expected': ['56781234 0000ffff', '3412 ff00']},
     {'id': 'c1-checksum16',
      'mode': 'c',
      'title': 'Контрольная сумма: сложение с переносом',
      'statement': 'checksum16(const uint16_t *w, size_t n) → uint16_t: сложите n 16-битных слов в 32-битной '
                   'переменной, затем сворачивайте перенос (старшие 16 бит прибавляйте к младшим) пока он '
                   'есть, и инвертируйте результат. Это поразрядное дополнение суммы по модулю 0xFFFF.',
      'starter': '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'uint16_t checksum16(const uint16_t *w, size_t n) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    uint16_t a[] = {0x4500, 0x0073, 0x0000, 0x4000, 0x4011, 0xc0a8, 0x0001, 0xc0a8, '
                '0x00c7};\n'
                '    printf("%04x\\n", checksum16(a, 9));\n'
                '    uint16_t b[] = {0xFFFF, 0xFFFF};\n'
                '    printf("%04x\\n", checksum16(b, 2));\n'
                '    printf("%04x\\n", checksum16(b, 0));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'После сложения: while (s >> 16) s = (s & 0xFFFF) + (s >> 16); в конце ~s, приведённое к '
              'uint16_t.',
      'expected': ['b861', '0000', 'ffff']},
     {'id': 'c1-crc8',
      'mode': 'c',
      'title': 'CRC-8 побитово',
      'statement': 'crc8(const uint8_t *p, size_t n) → uint8_t: контрольный код CRC-8 с полиномом 0x07, '
                   'начальное значение 0, без отражений. Для каждого байта: crc ^= байт; восемь раз: если '
                   'старший бит единица — сдвиг влево и XOR с 0x07, иначе просто сдвиг.',
      'starter': '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'uint8_t crc8(const uint8_t *p, size_t n) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%02x\\n", crc8((const uint8_t *)"123456789", 9));\n'
                '    printf("%02x\\n", crc8((const uint8_t *)"", 0));\n'
                '    uint8_t z[4] = {0, 0, 0, 0};\n'
                '    printf("%02x\\n", crc8(z, 4));\n'
                '    printf("%02x\\n", crc8((const uint8_t *)"hello", 5));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Результат сдвига uint8_t нужно приводить обратно к uint8_t: вычисления идут в int.',
      'expected': ['f4', '00', '00', '92']},
     {'id': 'c1-gray',
      'mode': 'c',
      'title': 'Код Грея',
      'statement': 'to_gray(uint32_t x) → uint32_t: x ^ (x >> 1). from_gray(uint32_t g) → uint32_t: обратное '
                   'преобразование (накопленный XOR сдвигов). Соседние числа в коде Грея отличаются одним '
                   'битом.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t to_gray(uint32_t x) {\n'
                 '    return x;\n'
                 '}\n'
                 '\n'
                 'uint32_t from_gray(uint32_t g) {\n'
                 '    return g;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (uint32_t i = 0; i < 8; i++) printf("%u:%u ", i, to_gray(i));\n'
                '    printf("\\n");\n'
                '    int ok = 1;\n'
                '    for (uint32_t i = 0; i < 100000; i++) if (from_gray(to_gray(i)) != i) ok = 0;\n'
                '    printf("%d %u\\n", ok, from_gray(to_gray(0xFFFFFFFFu)));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'from_gray: результат — XOR самого g и всех его сдвигов вправо.',
      'expected': ['0:0 1:1 2:3 3:2 4:6 5:7 6:5 7:4', '1 4294967295']},
     {'id': 'c1-safe-abs',
      'mode': 'c',
      'title': 'abs без UB',
      'statement': 'abs(INT_MIN) — неопределённое поведение (результата нет в int). safe_abs(int x, int '
                   '*out) → int: записать |x| в *out и вернуть 1; для INT_MIN вернуть 0, *out не менять. '
                   'abs_u(int x) → unsigned: модуль как беззнаковое число, корректный и для INT_MIN.',
      'starter': '#include <limits.h>\n'
                 '\n'
                 'int safe_abs(int x, int *out) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'unsigned abs_u(int x) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int r = 99;\n'
                '    printf("%d %d\\n", safe_abs(-5, &r), r);\n'
                '    printf("%d %d\\n", safe_abs(INT_MIN, &r), r);\n'
                '    printf("%d %d\\n", safe_abs(INT_MAX, &r), r);\n'
                '    printf("%u %u %u\\n", abs_u(-5), abs_u(INT_MIN), abs_u(7));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'В unsigned арифметика определена: 0u - (unsigned)x даёт модуль даже для INT_MIN.',
      'expected': ['1 5', '0 5', '1 2147483647', '5 2147483648 7']},
     {'id': 'c1-shifts',
      'mode': 'c',
      'title': 'Безопасные сдвиги',
      'statement': 'Сдвиг на число разрядов ≥ ширины типа — неопределённое поведение. shl_safe(uint32_t x, '
                   'unsigned n) → uint32_t: x << n, но 0 при n ≥ 32. asr(int32_t x, unsigned n) → int32_t: '
                   'арифметический сдвиг вправо (знак сохраняется) для любого n, при n ≥ 32 — 0 или −1 по '
                   'знаку. Опираться на поведение >> для отрицательных не нужно: реализуйте через деление '
                   'или битовую маску.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t shl_safe(uint32_t x, unsigned n) {\n'
                 '    return x;\n'
                 '}\n'
                 '\n'
                 'int32_t asr(int32_t x, unsigned n) {\n'
                 '    return x;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%u %u %u\\n", shl_safe(1, 31), shl_safe(1, 32), shl_safe(3, 100));\n'
                '    printf("%d %d %d %d\\n", asr(-8, 1), asr(-8, 3), asr(-8, 40), asr(8, 40));\n'
                '    printf("%d %d %d\\n", asr(-1, 0), asr(INT32_MIN, 31), asr(100, 2));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для отрицательных x: логический сдвиг, затем старшие n бит заполняем единицами маской ~0u << '
              '(32 - n); n == 0 — особый случай.',
      'expected': ['2147483648 0 0', '-4 -1 -1 0', '-1 -1 25']}],
 2: [{'id': 'c2-gcd',
      'mode': 'c',
      'title': 'НОД и НОК: алгоритм Евклида',
      'statement': 'gcd(unsigned long a, unsigned long b) → наибольший общий делитель по алгоритму Евклида '
                   '(gcd(a, 0) = a, gcd(0, 0) = 0). lcm(a, b) → наименьшее общее кратное (для нуля — 0). '
                   'Цикл, без рекурсии.',
      'starter': 'unsigned long gcd(unsigned long a, unsigned long b) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'unsigned long lcm(unsigned long a, unsigned long b) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%lu %lu %lu %lu\\n", gcd(12, 18), gcd(17, 5), gcd(0, 7), gcd(0, 0));\n'
                '    printf("%lu %lu %lu\\n", lcm(4, 6), lcm(0, 5), lcm(21, 6));\n'
                '    printf("%lu\\n", gcd(1071, 462));\n'
                '    printf("%lu\\n", lcm(1000000007UL, 998244353UL));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Пока b ≠ 0: (a, b) = (b, a % b). Для НОК сначала делите на НОД, чтобы не переполнить.',
      'expected': ['6 1 7 0', '12 0 42', '21', '998244359987710471']},
     {'id': 'c2-prime',
      'mode': 'c',
      'title': 'Простые числа',
      'statement': 'is_prime(unsigned n) → int: 1 для простых (проверка делителей до √n, без sqrt из math.h '
                   '— условие i * i <= n). count_primes(unsigned limit) → unsigned: количество простых '
                   'строго меньше limit.',
      'starter': 'int is_prime(unsigned n) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'unsigned count_primes(unsigned limit) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (unsigned n = 0; n < 20; n++) printf("%d", is_prime(n));\n'
                '    printf("\\n%d %d\\n", is_prime(1000003), is_prime(4294967291u));\n'
                '    printf("%u %u %u\\n", count_primes(10), count_primes(100), count_primes(200000));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Цикл по i, пока i * i <= n; произведение считайте в более широком типе, чтобы не переполнить.',
      'expected': ['00110101000101000101', '1 1', '4 25 17984']},
     {'id': 'c2-collatz',
      'mode': 'c',
      'title': 'Последовательность Коллатца',
      'statement': 'collatz_steps(unsigned long n) → число шагов до единицы (n чётное — n/2, нечётное — '
                   '3n+1; для 1 — 0). best_start(unsigned limit) → начальное n < limit с самой длинной '
                   'цепочкой (при равенстве — меньшее).',
      'starter': 'unsigned collatz_steps(unsigned long n) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'unsigned best_start(unsigned limit) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%u %u %u %u\\n", collatz_steps(1), collatz_steps(6), collatz_steps(27), '
                'collatz_steps(97));\n'
                '    printf("%u %u\\n", best_start(10), best_start(1000));\n'
                '    printf("%u\\n", best_start(300000));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Используйте unsigned long, чтобы 3n + 1 не переполнилось на длинных цепочках.',
      'expected': ['0 8 111 118', '9 871', '230631']},
     {'id': 'c2-digits',
      'mode': 'c',
      'title': 'Цифры числа: цикл do-while',
      'statement': 'digit_sum(unsigned n), reverse_digits(unsigned n) (1200 → 21) и count_digits(unsigned n) '
                   '(для 0 — 1 цифра), все через do-while / деление на 10. is_palindrome(unsigned n) — '
                   'читается ли число одинаково в обе стороны.',
      'starter': 'unsigned digit_sum(unsigned n) { return 0; }\n'
                 'unsigned reverse_digits(unsigned n) { return 0; }\n'
                 'int count_digits(unsigned n) { return 0; }\n'
                 'int is_palindrome(unsigned n) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    unsigned v[] = {0, 7, 1200, 12321, 4000000000u, 1001};\n'
                '    for (int i = 0; i < 6; i++)\n'
                '        printf("%u: %u %u %d %d\\n", v[i], digit_sum(v[i]), reverse_digits(v[i]), '
                'count_digits(v[i]), is_palindrome(v[i]));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Последняя цифра — n % 10, отбросить её — n /= 10. Для count_digits(0) нужен do-while, чтобы '
              'тело выполнилось хотя бы раз.',
      'expected': ['0: 0 0 1 1',
                   '7: 7 7 1 1',
                   '1200: 3 21 4 0',
                   '12321: 9 12321 5 1',
                   '4000000000: 4 4 10 0',
                   '1001: 2 1001 4 1']},
     {'id': 'c2-fib',
      'mode': 'c',
      'title': 'Фибоначчи без экспоненциальной рекурсии',
      'statement': 'fib(unsigned n) → uint64_t: n-е число Фибоначчи (fib(0)=0, fib(1)=1) для n ≤ 93 — '
                   'циклом. Наивная двойная рекурсия для n = 90 не уложится по времени. fib_mod(unsigned '
                   'long n, unsigned m) → число Фибоначчи по модулю m за O(n) без хранения всех значений.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint64_t fib(unsigned n) {\n'
                 '    return 0;\n'
                 '}\n'
                 '\n'
                 'unsigned fib_mod(unsigned long n, unsigned m) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (unsigned i = 0; i < 10; i++) printf("%llu ", (unsigned long long)fib(i));\n'
                '    printf("\\n%llu %llu\\n", (unsigned long long)fib(50), (unsigned long long)fib(90));\n'
                '    printf("%llu\\n", (unsigned long long)fib(93));\n'
                '    printf("%u %u %u\\n", fib_mod(10, 1000), fib_mod(100000000UL, 1000000007u), fib_mod(5, '
                '1));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Два накопителя a и b и сдвиг пары на каждом шаге: (a, b) = (b, a + b).',
      'expected': ['0 1 1 2 3 5 8 13 21 34',
                   '12586269025 2880067194370816120',
                   '12200160415121876738',
                   '55 908460138 0']},
     {'id': 'c2-powmod',
      'mode': 'c',
      'title': 'Быстрое возведение в степень по модулю',
      'statement': 'powmod(uint64_t b, uint64_t e, uint64_t m) → uint64_t: b^e mod m (m ≥ 1, m < 2³²) за '
                   'O(log e): цикл по битам e, квадраты основания. e может быть огромным (до 2⁶⁴ − 1).',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint64_t powmod(uint64_t b, uint64_t e, uint64_t m) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%llu %llu %llu\\n", (unsigned long long)powmod(2, 10, 1000), (unsigned long '
                'long)powmod(3, 0, 7), (unsigned long long)powmod(5, 3, 1));\n'
                '    printf("%llu\\n", (unsigned long long)powmod(2, 1000000000000ULL, 1000000007ULL));\n'
                '    printf("%llu\\n", (unsigned long long)powmod(7, UINT64_MAX, 998244353ULL));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Если младший бит e единица — умножьте результат на текущее основание; затем возведите '
              'основание в квадрат и сдвиньте e.',
      'expected': ['24 1 0', '959366170', '320018489']},
     {'id': 'c2-isqrt',
      'mode': 'c',
      'title': 'Целый квадратный корень',
      'statement': 'isqrt(uint64_t n) → uint64_t: наибольшее r с r·r ≤ n, без чисел с плавающей точкой '
                   '(никаких sqrt и double) — двоичным поиском; вычисление r·r не должно переполняться.',
      'starter': '#include <stdint.h>\n\nuint64_t isqrt(uint64_t n) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
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
                '    uint64_t v[] = {0, 1, 2, 3, 4, 15, 16, 17, 1000000, 999999999999ULL, UINT64_MAX};\n'
                '    for (int i = 0; i < 11; i++) printf("%llu ", (unsigned long long)isqrt(v[i]));\n'
                '    printf("\\nfloat: %d %d\\n", src_count(" sq" "rt(") + src_count("(sq" "rt("), '
                'src_count("dou" "ble"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Корень любого uint64_t не превосходит 2³² − 1; ищите наибольший mid, у которого mid * mid <= '
              'n (mid * mid помещается в uint64_t).',
      'expected': ['0 1 1 1 2 3 4 4 1000 999999 4294967295', 'float: 0 0']},
     {'id': 'c2-calendar',
      'mode': 'c',
      'title': 'Календарь: високосные годы и день недели',
      'statement': 'is_leap(y); days_in_month(y, m) (m = 1..12); day_of_week(y, m, d) → 0 = воскресенье … 6 '
                   '= суббота (григорианский календарь, y ≥ 1583; формула Зеллера или Сакамото). Проверьте '
                   'себя: 1 января 2000 — суббота.',
      'starter': 'int is_leap(int y) { return 0; }\n'
                 'int days_in_month(int y, int m) { return 0; }\n'
                 'int day_of_week(int y, int m, int d) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d %d\\n", is_leap(1900), is_leap(2000), is_leap(2024), is_leap(2023));\n'
                '    for (int m = 1; m <= 12; m++) printf("%d ", days_in_month(2024, m));\n'
                '    printf("\\n%d %d\\n", days_in_month(2023, 2), days_in_month(1900, 2));\n'
                '    printf("%d %d %d %d\\n", day_of_week(2000, 1, 1), day_of_week(2024, 2, 29), '
                'day_of_week(1999, 12, 31), day_of_week(2026, 10, 15));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Високосный год: делится на 4 и не на 100 — либо делится на 400. Для дня недели возьмите '
              'алгоритм Сакамото с таблицей сдвигов по месяцам.',
      'expected': ['0 1 1 0', '31 29 31 30 31 30 31 31 30 31 30 31', '28 28', '6 4 5 4']},
     {'id': 'c2-calc',
      'mode': 'c',
      'title': 'switch: калькулятор',
      'statement': 'calc(char op, long a, long b) → long: «+», «-», «*», «/», «%», «&», «|», «^» и «<» (a << '
                   'b, для 0 ≤ b < 63). При неизвестной операции, делении на ноль или недопустимом сдвиге '
                   'вернуть LONG_MIN. Одним switch.',
      'starter': '#include <limits.h>\n\nlong calc(char op, long a, long b) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    char ops[] = "+-*/%&|^<?";\n'
                '    for (int i = 0; ops[i]; i++) printf("%c:%ld ", ops[i], calc(ops[i], 12, 5));\n'
                '    printf("\\n%ld %ld %ld\\n", calc(\'/\', 1, 0), calc(\'%\', 1, 0), calc(\'<\', 1, 70));\n'
                '    printf("%ld %ld\\n", calc(\'/\', -7, 2), calc(\'%\', -7, 2));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'В каждой ветке return; для / и % проверяйте b == 0 до операции (деление на ноль — UB).',
      'expected': ['+:17 -:7 *:60 /:2 %:2 &:4 |:13 ^:9 <:384 ?:-9223372036854775808',
                   '-9223372036854775808 -9223372036854775808 -9223372036854775808',
                   '-3 -1']},
     {'id': 'c2-fix-fallthrough',
      'mode': 'c',
      'title': 'Исправьте: проваливание в switch',
      'statement': 'day_type(d) для d = 1..7 (понедельник…воскресенье) должна возвращать "weekday" или '
                   '"weekend", а для остальных чисел — "invalid". Сейчас из-за пропущенных break любое '
                   'значение даёт «invalid». Исправьте.',
      'starter': 'const char *day_type(int d) {\n'
                 '    const char *r;\n'
                 '    switch (d) {\n'
                 '    case 1: case 2: case 3: case 4: case 5:\n'
                 '        r = "weekday";\n'
                 '    case 6: case 7:\n'
                 '        r = "weekend";\n'
                 '    default:\n'
                 '        r = "invalid";\n'
                 '    }\n'
                 '    return r;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (int d = 0; d <= 8; d++) printf("%d:%s ", d, day_type(d));\n'
                '    printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'После присваивания в каждой группе case поставьте break; у default он не нужен — это '
              'последняя ветка.',
      'expected': ['0:invalid 1:weekday 2:weekday 3:weekday 4:weekday 5:weekday 6:weekend 7:weekend '
                   '8:invalid']},
     {'id': 'c2-fix-braces',
      'mode': 'c',
      'title': 'Исправьте: if без скобок',
      'statement': 'validate(a, b, c) возвращает 0, если любой из аргументов отрицательный, иначе 1. Отступы '
                   'обманывают: из-за отсутствия фигурных скобок функция всегда возвращает 0. Исправьте — '
                   'расставьте скобки так, как задумывал автор.',
      'starter': 'int validate(int a, int b, int c) {\n'
                 '    if (a < 0)\n'
                 '        return 0;\n'
                 '    if (b < 0)\n'
                 '        return 0;\n'
                 '        return 0;\n'
                 '    if (c < 0)\n'
                 '        return 0;\n'
                 '    return 1;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d %d\\n", validate(1, 2, 3), validate(-1, 2, 3), validate(1, -2, 3), '
                'validate(1, 2, -3));\n'
                '    printf("%d\\n", validate(0, 0, 0));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Лишняя строка «return 0;» без условия выполняется всегда — удалите её и поставьте скобки у '
              'каждого if.',
      'expected': ['1 0 0 0', '1']},
     {'id': 'c2-fix-size-t',
      'mode': 'c',
      'title': 'Исправьте: бесконечный цикл по size_t',
      'statement': 'sum_reversed(const int *a, size_t n) возвращает сумму a[i] · (n − i) по всем i, '
                   'перебирая индексы от последнего к первому. Цикл с size_t i >= 0 никогда не заканчивается '
                   '(программа завершится по таймауту). Перепишите цикл без смены типа параметров.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'long sum_reversed(const int *a, size_t n) {\n'
                 '    long s = 0;\n'
                 '    for (size_t i = n - 1; i >= 0; i--) {\n'
                 '        s += (long)a[i] * (long)(n - i);\n'
                 '    }\n'
                 '    return s;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {1, 2, 3, 4};\n'
                '    printf("%ld %ld\\n", sum_reversed(a, 4), sum_reversed(a, 1));\n'
                '    printf("%ld\\n", sum_reversed(a, 0));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Условие i-- > 0 сравнивает старое значение i с нулём, а затем уменьшает: на последней '
              'итерации i станет нулём внутри тела.',
      'expected': ['20 1', '0']},
     {'id': 'c2-factorial',
      'mode': 'c',
      'title': 'Рекурсия: факториал и его границы',
      'statement': 'fact(n) → uint64_t рекурсивно (n ≤ 20). fact_iter(n) — то же циклом. '
                   'first_overflow(void) → int: наименьшее n, для которого n! не помещается в uint64_t '
                   '(определите по проверке деления, без переполнения).',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint64_t fact(unsigned n) { return 0; }\n'
                 'uint64_t fact_iter(unsigned n) { return 0; }\n'
                 'int first_overflow(void) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (unsigned n = 0; n <= 5; n++) printf("%llu ", (unsigned long long)fact(n));\n'
                '    printf("\\n%llu %llu\\n", (unsigned long long)fact(20), (unsigned long '
                'long)fact_iter(20));\n'
                '    printf("%d\\n", first_overflow());\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Перед умножением на n проверьте, что f <= UINT64_MAX / n.',
      'expected': ['1 1 2 6 24 120', '2432902008176640000 2432902008176640000', '21']},
     {'id': 'c2-hanoi',
      'mode': 'c',
      'title': 'Ханойские башни',
      'statement': 'hanoi_moves(n) → unsigned long: число ходов (2ⁿ − 1). hanoi(n, from, to, via): '
                   "напечатайте каждый ход строкой «A->C» (диск номер не печатайте), стержни — символы 'A', "
                   "'B', 'C'.",
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'unsigned long hanoi_moves(int n) { return 0; }\n'
                 'void hanoi(int n, char from, char to, char via) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%lu %lu %lu\\n", hanoi_moves(1), hanoi_moves(3), hanoi_moves(20));\n'
                "    hanoi(3, 'A', 'C', 'B');\n"
                '    return 0;\n'
                '}\n',
      'hint': 'Перенести n−1 дисков на запасной стержень, переложить самый большой, затем снова n−1 на '
              'целевой.',
      'expected': ['1 7 1048575', 'A->C', 'A->B', 'C->B', 'A->C', 'B->A', 'B->C', 'A->C']},
     {'id': 'c2-ackermann',
      'mode': 'c',
      'title': 'Функция Аккермана',
      'statement': 'ackermann(m, n): A(0, n) = n + 1; A(m, 0) = A(m − 1, 1); A(m, n) = A(m − 1, A(m, n − '
                   '1)). Реализуйте рекурсивно — это хороший способ почувствовать кадры стека. Значения до m '
                   '= 3, n = 6 влезают в стек.',
      'starter': 'unsigned ackermann(unsigned m, unsigned n) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (unsigned m = 0; m <= 3; m++) {\n'
                '        for (unsigned n = 0; n <= 4; n++) printf("%u ", ackermann(m, n));\n'
                '        printf("\\n");\n'
                '    }\n'
                '    printf("%u\\n", ackermann(3, 6));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Три случая по определению; во втором и третьем — рекурсивные вызовы с меньшим m.',
      'expected': ['1 2 3 4 5', '2 3 4 5 6', '3 5 7 9 11', '5 13 29 61 125', '509']},
     {'id': 'c2-fix-prototype',
      'mode': 'c',
      'title': 'Исправьте: функция объявлена позже вызова',
      'statement': 'is_even и is_odd вызывают друг друга (взаимная рекурсия). Код не собирается, потому что '
                   'is_odd используется до объявления. Добавьте прототип, не меняя порядок определений.',
      'starter': 'int is_even(unsigned n) {\n'
                 '    if (n == 0) return 1;\n'
                 '    return is_odd(n - 1);\n'
                 '}\n'
                 '\n'
                 'int is_odd(unsigned n) {\n'
                 '    if (n == 0) return 0;\n'
                 '    return is_even(n - 1);\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (unsigned n = 0; n < 6; n++) printf("%u:%d%d ", n, is_even(n), is_odd(n));\n'
                '    printf("\\n%d %d\\n", is_even(1000), is_odd(1001));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'int is_odd(unsigned n); — прототип сообщает компилятору сигнатуру заранее.',
      'expected': ['0:10 1:01 2:10 3:01 4:10 5:01', '1 1']},
     {'id': 'c2-static-counter',
      'mode': 'c',
      'title': 'static внутри функции',
      'statement': 'next_id(void) → int: при каждом вызове возвращает следующее число, начиная с 1 (хранится '
                   'в static-переменной). calls_since_reset(void) → int и reset_ids(void): число вызовов '
                   'next_id после последнего сброса и сам сброс (следующий next_id снова вернёт 1). '
                   'Глобальных переменных кроме static внутри функций (или static на уровне файла) не нужно.',
      'starter': 'int next_id(void) { return 0; }\n'
                 'int calls_since_reset(void) { return 0; }\n'
                 'void reset_ids(void) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d\\n", next_id(), next_id(), next_id());\n'
                '    printf("%d\\n", calls_since_reset());\n'
                '    reset_ids();\n'
                '    printf("%d %d\\n", next_id(), calls_since_reset());\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Файловая static-переменная общая для нескольких функций и не видна из других файлов.',
      'expected': ['1 2 3', '3', '1 1']},
     {'id': 'c2-varargs-sum',
      'mode': 'c',
      'title': 'Функции с переменным числом аргументов',
      'statement': 'sum_n(int n, ...) → int: сумма n следующих аргументов типа int. avg_n(int n, ...) → '
                   'double: среднее n аргументов типа double (n ≥ 1). max_n(int n, ...) → int: наибольшее из '
                   'n аргументов типа int. Используйте stdarg.h.',
      'starter': '#include <stdarg.h>\n'
                 '\n'
                 'int sum_n(int n, ...) { return 0; }\n'
                 'double avg_n(int n, ...) { return 0; }\n'
                 'int max_n(int n, ...) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d\\n", sum_n(0), sum_n(3, 10, 20, 30), sum_n(1, -5));\n'
                '    printf("%.2f %.2f\\n", avg_n(2, 1.5, 2.5), avg_n(4, 1.0, 2.0, 3.0, 5.0));\n'
                '    printf("%d %d\\n", max_n(3, 4, 9, 2), max_n(2, -7, -3));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'va_arg(ap, double) — тип нужно указать точно: целые литералы вместо double дадут мусор, '
              'поэтому в драйвере везде 1.0, 2.5…',
      'expected': ['0 60 -5', '2.00 2.75', '9 -3']},
     {'id': 'c2-varargs-log',
      'mode': 'c',
      'title': 'Обёртка над printf: vprintf',
      'statement': 'log_msg(const char *level, const char *fmt, ...): печатает «[LEVEL] » (уровень '
                   'заглавными буквами, как передан), затем сообщение по формату fmt с аргументами и перевод '
                   'строки. Передайте аргументы через va_list функции vprintf.',
      'starter': '#include <stdio.h>\n'
                 '#include <stdarg.h>\n'
                 '\n'
                 'void log_msg(const char *level, const char *fmt, ...) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    log_msg("INFO", "started");\n'
                '    log_msg("WARN", "value=%d name=%s", 42, "x");\n'
                '    log_msg("ERROR", "%5.1f%%", 99.5);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'vprintf(fmt, ap) — версия printf, принимающая va_list; va_start вызывают от последнего '
              'именованного параметра fmt.',
      'expected': ['[INFO] started', '[WARN] value=42 name=x', '[ERROR]  99.5%']},
     {'id': 'c2-print-base',
      'mode': 'c',
      'title': 'Рекурсивная печать числа в системе счисления',
      'statement': 'print_base(unsigned n, unsigned base): напечатайте n в системе счисления base (2..36, '
                   'цифры 0-9 и строчные a-z) без пробелов и без перевода строки, не используя массивы и '
                   'printf с %x — рекурсией (старшие цифры печатаются первыми). Для 0 — «0».',
      'starter': '#include <stdio.h>\n\nvoid print_base(unsigned n, unsigned base) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    unsigned n[] = {0, 5, 255, 1000, 4294967295u};\n'
                '    unsigned b[] = {2, 10, 16, 36};\n'
                '    for (int i = 0; i < 5; i++) {\n'
                '        for (int j = 0; j < 4; j++) {\n'
                '            print_base(n[i], b[j]);\n'
                "            putchar(' ');\n"
                '        }\n'
                "        putchar('\\n');\n"
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сначала рекурсивный вызов для n / base (если число ещё не однозначное), затем печать '
              'последней цифры.',
      'expected': ['0 0 0 0',
                   '101 5 5 5',
                   '11111111 255 ff 73',
                   '1111101000 1000 3e8 rs',
                   '11111111111111111111111111111111 4294967295 ffffffff 1z141z3']},
     {'id': 'c2-bit-loops',
      'mode': 'c',
      'title': 'Биты циклами: обратный порядок, нули',
      'statement': 'reverse_bits(uint32_t x) — перевернуть порядок 32 бит. leading_zeros(uint32_t x) и '
                   'trailing_zeros(uint32_t x) — число нулей со старшей/младшей стороны (для 0 — 32). Циклы, '
                   'без __builtin_*.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint32_t reverse_bits(uint32_t x) { return x; }\n'
                 'int leading_zeros(uint32_t x) { return 0; }\n'
                 'int trailing_zeros(uint32_t x) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
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
                '    printf("%08x %08x %08x\\n", reverse_bits(1), reverse_bits(0xF0000000u), '
                'reverse_bits(0x12345678u));\n'
                '    printf("%d %d %d %d\\n", leading_zeros(1), leading_zeros(0x80000000u), '
                'leading_zeros(0), leading_zeros(256));\n'
                '    printf("%d %d %d %d\\n", trailing_zeros(1), trailing_zeros(0x80000000u), '
                'trailing_zeros(0), trailing_zeros(96));\n'
                '    printf("builtins: %d\\n", src_count("__bu" "iltin"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Условие цикла должно проверять границу i раньше, чем читать бит, чтобы не сдвигать на 32.',
      'expected': ['80000000 0000000f 1e6a2c48', '31 0 32 23', '0 31 32 5', 'builtins: 0']},
     {'id': 'c2-perfect',
      'mode': 'c',
      'title': 'Делители и совершенные числа',
      'statement': 'divisor_sum(unsigned n) → сумма собственных делителей (меньше n; для 1 — 0), за O(√n). '
                   'count_perfect(unsigned limit) → сколько совершенных чисел (n = сумме собственных '
                   'делителей) меньше limit; первые: 6, 28, 496, 8128.',
      'starter': 'unsigned divisor_sum(unsigned n) { return 0; }\n'
                 'unsigned count_perfect(unsigned limit) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%u %u %u %u %u\\n", divisor_sum(1), divisor_sum(6), divisor_sum(12), '
                'divisor_sum(28), divisor_sum(97));\n'
                '    printf("%u %u %u\\n", count_perfect(7), count_perfect(10000), count_perfect(1000000));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Делители идут парами (i, n / i); при i * i == n добавлять второй делитель не нужно.',
      'expected': ['0 6 16 28 1', '1 4 4']},
     {'id': 'c2-print-shapes',
      'mode': 'c',
      'title': 'Вложенные циклы: фигуры и таблица',
      'statement': 'print_triangle(n): n строк, в i-й строке i звёздочек (без пробелов в конце). '
                   'print_table(n): таблица умножения n × n, каждое число занимает 4 позиции по правому краю '
                   '(%4d), строки заканчиваются переводом строки. Выведите именно такой формат.',
      'starter': '#include <stdio.h>\n\nvoid print_triangle(int n) {\n}\nvoid print_table(int n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    print_triangle(4);\n'
                '    print_table(5);\n'
                '    print_triangle(0);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Внешний цикл — строки, внутренний — столбцы; перевод строки после внутреннего цикла.',
      'expected': ['*',
                   '**',
                   '***',
                   '****',
                   '   1   2   3   4   5',
                   '   2   4   6   8  10',
                   '   3   6   9  12  15',
                   '   4   8  12  16  20',
                   '   5  10  15  20  25']},
     {'id': 'c2-pythagorean',
      'mode': 'c',
      'title': 'Пифагоровы тройки: два цикла вместо трёх',
      'statement': 'count_triples(int limit) → число троек a < b < c ≤ limit с a² + b² = c² (целые). Тройной '
                   'цикл при limit = 3000 не успеет: перебирайте a, b и проверяйте c через целый квадратный '
                   'корень.',
      'starter': 'int count_triples(int limit) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d\\n", count_triples(5), count_triples(20));\n'
                '    printf("%d\\n", count_triples(3000));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'c = (long)sqrt((double)s) с поправками на неточность, затем проверьте c * c == s и c <= '
              'limit.',
      'expected': ['1 6', '3172']},
     {'id': 'c2-happy',
      'mode': 'c',
      'title': 'Счастливые числа и цифровой корень',
      'statement': 'digital_root(unsigned n) → однозначное число, получаемое повторным сложением цифр (для 0 '
                   '— 0). is_happy(unsigned n) → 1, если последовательность «сумма квадратов цифр» приходит '
                   'к 1 (иначе зацикливается: используйте то, что цикл всегда заходит в 4).',
      'starter': 'unsigned digital_root(unsigned n) { return 0; }\nint is_happy(unsigned n) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%u %u %u %u\\n", digital_root(0), digital_root(9875), '
                'digital_root(4294967295u), digital_root(10));\n'
                '    int c = 0;\n'
                '    for (unsigned n = 1; n <= 50; n++) if (is_happy(n)) { printf("%u ", n); c++; }\n'
                '    printf("\\n%d %d\\n", c, is_happy(1000000));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Цикл несчастливых чисел всегда проходит через 4, поэтому достаточно остановиться на 1 или 4.',
      'expected': ['0 2 3 1', '1 7 10 13 19 23 28 31 32 44 49', '11 1']},
     {'id': 'c2-sum-multiples',
      'mode': 'c',
      'title': 'Формула вместо цикла',
      'statement': 'sum_multiples(uint64_t n) → сумма всех натуральных чисел меньше n, кратных 3 или 5 (n до '
                   '10¹²). Цикл до 10¹² не успеет: примените формулу суммы арифметической прогрессии и '
                   'принцип включения-исключения (кратные 15 учтены дважды).',
      'starter': '#include <stdint.h>\n\nuint64_t sum_multiples(uint64_t n) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%llu %llu %llu\\n", (unsigned long long)sum_multiples(0), (unsigned long '
                'long)sum_multiples(10), (unsigned long long)sum_multiples(1000));\n'
                '    printf("%llu\\n", (unsigned long long)sum_multiples(1000000000000ULL));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Кратных k меньше n ровно m = (n − 1) / k; их сумма k · m · (m + 1) / 2.',
      'expected': ['0 23 233168', '467544814548275884']},
     {'id': 'c2-goto-cleanup',
      'mode': 'c',
      'title': 'goto для очистки: идиома ядра',
      'statement': 'step(k, fail_at) уже есть в драйвере: печатает «step k» и возвращает 1, если k == '
                   'fail_at (ошибка), иначе 0. Напишите run_steps(int fail_at) → int: выполните шаги 1, 2, 3 '
                   'по порядку; при ошибке шага k выполните откат в обратном порядке (печатая «undo j» для '
                   'каждого успешно выполненного j < k) и верните −k; при успехе всех трёх верните 0. '
                   'Используйте goto на метки очистки, как принято в системном коде.',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'int step(int k, int fail_at);\n'
                 '\n'
                 'int run_steps(int fail_at) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int step(int k, int fail_at) {\n'
                '    printf("step %d\\n", k);\n'
                '    return k == fail_at;\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    for (int f = 0; f <= 3; f++) {\n'
                '        int r = run_steps(f);\n'
                '        printf("-> %d\\n", r);\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Метки идут в обратном порядке: err3 печатает undo 2 и проваливается в err2 (undo 1), затем в '
              'err1 — return.',
      'expected': ['step 1',
                   'step 2',
                   'step 3',
                   '-> 0',
                   'step 1',
                   '-> -1',
                   'step 1',
                   'step 2',
                   'undo 1',
                   '-> -2',
                   'step 1',
                   'step 2',
                   'step 3',
                   'undo 2',
                   'undo 1',
                   '-> -3']},
     {'id': 'c2-traffic-light',
      'mode': 'c',
      'title': 'Автомат на enum и switch',
      'statement': 'enum light { RED, GREEN, YELLOW }. next(enum light) → следующий цвет '
                   '(RED→GREEN→YELLOW→RED); duration(enum light) → длительность в секундах (RED 30, GREEN '
                   '25, YELLOW 5); color_at(int t) → цвет через t секунд после начала красного (t ≥ 0, цикл '
                   '60 секунд).',
      'starter': 'enum light { RED, GREEN, YELLOW };\n'
                 '\n'
                 'enum light next(enum light l) { return l; }\n'
                 'int duration(enum light l) { return 0; }\n'
                 'enum light color_at(int t) { return RED; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (enum light l = RED, i = 0; i < 4; i++, l = next(l)) printf("%d:%d ", l, '
                'duration(l));\n'
                '    printf("\\n");\n'
                '    int t[] = {0, 29, 30, 54, 55, 59, 60, 61, 125, 1000000};\n'
                '    for (int i = 0; i < 10; i++) printf("%d ", color_at(t[i]));\n'
                '    printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'color_at: возьмите t % 60 и вычитайте длительности цветов, переходя к следующему, пока t не '
              'окажется внутри текущего.',
      'expected': ['0:30 1:25 2:5 0:30', '0 0 1 1 2 2 0 0 0 1']},
     {'id': 'c2-lcg',
      'mode': 'c',
      'title': 'Генератор псевдослучайных чисел',
      'statement': 'Линейный конгруэнтный генератор: state = state · 1103515245 + 12345 (mod 2³²), результат '
                   '— (state >> 16) & 0x7FFF. seed_rand(unsigned s) задаёт состояние, next_rand(void) → int '
                   'возвращает следующее значение. Состояние хранится в static-переменной. rand_range(int '
                   'lo, int hi) → число lo..hi включительно (через next_rand() % (hi − lo + 1)).',
      'starter': 'void seed_rand(unsigned s) {\n'
                 '}\n'
                 'int next_rand(void) { return 0; }\n'
                 'int rand_range(int lo, int hi) { return lo; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    seed_rand(1);\n'
                '    for (int i = 0; i < 5; i++) printf("%d ", next_rand());\n'
                '    printf("\\n");\n'
                '    seed_rand(42);\n'
                '    int hist[6] = {0};\n'
                '    for (int i = 0; i < 6000; i++) hist[rand_range(1, 6) - 1]++;\n'
                '    for (int i = 0; i < 6; i++) printf("%d ", hist[i]);\n'
                '    printf("\\n");\n'
                '    seed_rand(7);\n'
                '    printf("%d %d\\n", rand_range(10, 10), rand_range(-5, 5));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Арифметику состояния делайте в unsigned — переполнение там определено и даёт нужное «по '
              'модулю 2³²».',
      'expected': ['16838 5758 10113 17515 31051', '1066 1029 942 1035 978 950', '10 0']},
     {'id': 'c2-roman',
      'mode': 'c',
      'title': 'Римские числа',
      'statement': 'print_roman(int n): напечатайте римскую запись числа 1 ≤ n ≤ 3999 (M, CM, D, CD, C, XC, '
                   'L, XL, X, IX, V, IV, I) и перевод строки. roman_value(char c) → значение символа (I=1, '
                   'V=5, X=10, L=50, C=100, D=500, M=1000, иначе 0).',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'void print_roman(int n) {\n'
                 '}\n'
                 'int roman_value(char c) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    int n[] = {1, 4, 9, 14, 40, 90, 400, 1994, 2024, 3999};\n'
                '    for (int i = 0; i < 10; i++) print_roman(n[i]);\n'
                '    printf("%d %d %d\\n", roman_value(\'M\'), roman_value(\'v\'), roman_value(\'C\'));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Жадно вычитайте значения из таблицы в порядке убывания, включая вычитательные пары 900, 400, '
              '90, 40, 9, 4.',
      'expected': ['I',
                   'IV',
                   'IX',
                   'XIV',
                   'XL',
                   'XC',
                   'CD',
                   'MCMXCIV',
                   'MMXXIV',
                   'MMMCMXCIX',
                   '1000 0 100']}],
 3: [{'id': 'c3-swap',
      'mode': 'c',
      'title': 'Обмен через указатели',
      'statement': 'swap_int(int *a, int *b) — поменять значения двух переменных. swap_ptr(int **a, int **b) '
                   '— поменять местами сами указатели (кто куда указывает), значения при этом не копируются.',
      'starter': 'void swap_int(int *a, int *b) {\n}\n\nvoid swap_ptr(int **a, int **b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int x = 1, y = 2;\n'
                '    swap_int(&x, &y);\n'
                '    printf("%d %d\\n", x, y);\n'
                '    int *p = &x, *q = &y;\n'
                '    swap_ptr(&p, &q);\n'
                '    printf("%d %d %d %d\\n", *p, *q, x, y);\n'
                '    *p = 99;\n'
                '    printf("%d %d\\n", x, y);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'В swap_ptr временная переменная имеет тип int *: меняются адреса, а не числа.',
      'expected': ['2 1', '1 2 2 1', '2 99']},
     {'id': 'c3-minmax',
      'mode': 'c',
      'title': 'Несколько результатов через указатели',
      'statement': 'minmax(const int *a, size_t n, int *mn, int *mx): записать наименьший и наибольший '
                   'элементы (n ≥ 1). divmod(int a, int b, int *q, int *r): частное и остаток, оба через '
                   'указатели; возвращает 0 при b == 0 (указатели не трогать), иначе 1.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void minmax(const int *a, size_t n, int *mn, int *mx) {\n'
                 '}\n'
                 '\n'
                 'int divmod(int a, int b, int *q, int *r) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {5, -3, 9, 0, 9, -3};\n'
                '    int lo, hi;\n'
                '    minmax(a, 6, &lo, &hi);\n'
                '    printf("%d %d\\n", lo, hi);\n'
                '    minmax(a, 1, &lo, &hi);\n'
                '    printf("%d %d\\n", lo, hi);\n'
                '    int q = -1, r = -1;\n'
                '    int ok = divmod(17, 5, &q, &r);\n'
                '    printf("%d %d %d\\n", ok, q, r);\n'
                '    ok = divmod(1, 0, &q, &r);\n'
                '    printf("%d %d %d\\n", ok, q, r);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Инициализируйте *mn и *mx первым элементом, затем сравнивайте в цикле.',
      'expected': ['-3 9', '5 5', '1 3 2', '0 3 2']},
     {'id': 'c3-stats',
      'mode': 'c',
      'title': 'Массив и размер: sum, mean, argmax',
      'statement': 'sum(const int *a, size_t n) → long long, mean(const int *a, size_t n) → double (для n = '
                   '0 — 0.0), argmax(const int *a, size_t n) → size_t: индекс первого наибольшего (для n = 0 '
                   '— 0).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'long long sum(const int *a, size_t n) { return 0; }\n'
                 'double mean(const int *a, size_t n) { return 0; }\n'
                 'size_t argmax(const int *a, size_t n) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {3, 9, 2, 9, -4};\n'
                '    size_t n = sizeof a / sizeof a[0];\n'
                '    printf("%lld %.2f %zu\\n", sum(a, n), mean(a, n), argmax(a, n));\n'
                '    printf("%lld %.2f %zu\\n", sum(a, 0), mean(a, 0), argmax(a, 0));\n'
                '    int big[] = {INT_MAX, INT_MAX, INT_MAX};\n'
                '    printf("%lld\\n", sum(big, 3));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сумму копите в long long: int переполнится на больших значениях.',
      'expected': ['19 3.80 1', '0 0.00 0', '6442450941']},
     {'id': 'c3-reverse',
      'mode': 'c',
      'title': 'Разворот массива на месте',
      'statement': 'reverse(int *a, size_t n) — развернуть массив на месте двумя указателями (без '
                   'дополнительной памяти). reverse_range(int *a, size_t lo, size_t hi) — развернуть часть '
                   'a[lo..hi] включительно.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void reverse(int *a, size_t n) {\n'
                 '}\n'
                 'void reverse_range(int *a, size_t lo, size_t hi) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {1, 2, 3, 4, 5, 6};\n'
                '    reverse(a, 6);\n'
                '    for (size_t i = 0; i < 6; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    reverse_range(a, 1, 3);\n'
                '    for (size_t i = 0; i < 6; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    reverse(a, 0);\n'
                '    reverse(a, 1);\n'
                '    for (size_t i = 0; i < 6; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Пока lo < hi: поменять a[lo] и a[hi], сдвинуть оба индекса навстречу. Осторожно с hi при n = '
              '0 (беззнаковый).',
      'expected': ['6 5 4 3 2 1', '6 3 4 5 2 1', '6 3 4 5 2 1']},
     {'id': 'c3-rotate',
      'mode': 'c',
      'title': 'Циклический сдвиг массива без лишней памяти',
      'statement': 'rotate_left(int *a, size_t n, size_t k) — циклически сдвинуть массив влево на k позиций '
                   'за O(n) времени и O(1) памяти (тремя разворотами; k может быть любым, в том числе больше '
                   'n). Массив из миллиона элементов должен обрабатываться мгновенно.',
      'starter': '#include <stddef.h>\n\nvoid rotate_left(int *a, size_t n, size_t k) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {1, 2, 3, 4, 5, 6, 7};\n'
                '    rotate_left(a, 7, 3);\n'
                '    for (size_t i = 0; i < 7; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    rotate_left(a, 7, 7 * 100 + 1);\n'
                '    for (size_t i = 0; i < 7; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    rotate_left(a, 7, 0);\n'
                '    for (size_t i = 0; i < 7; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    size_t n = 1000000;\n'
                '    int *big = malloc(n * sizeof *big);\n'
                '    for (size_t i = 0; i < n; i++) big[i] = (int)i;\n'
                '    rotate_left(big, n, 123457);\n'
                '    printf("%d %d %d\\n", big[0], big[n - 1], big[n - 123457]);\n'
                '    free(big);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Развернуть первые k, развернуть остальные, затем развернуть весь массив целиком.',
      'expected': ['4 5 6 7 1 2 3', '5 6 7 1 2 3 4', '5 6 7 1 2 3 4', '123457 123456 0']},
     {'id': 'c3-lower-bound',
      'mode': 'c',
      'title': 'Двоичный поиск: lower_bound и upper_bound',
      'statement': 'lower_bound(const int *a, size_t n, int x) → индекс первого элемента ≥ x (n, если такого '
                   'нет); upper_bound — первого > x. Массив отсортирован по возрастанию, возможны повторы. '
                   'Входы большие: линейный поиск не пройдёт по времени.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t lower_bound(const int *a, size_t n, int x) { return 0; }\n'
                 'size_t upper_bound(const int *a, size_t n, int x) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {1, 2, 2, 2, 5, 8, 8};\n'
                '    int q[] = {0, 1, 2, 3, 5, 8, 9};\n'
                '    for (int i = 0; i < 7; i++) printf("%d:%zu/%zu ", q[i], lower_bound(a, 7, q[i]), '
                'upper_bound(a, 7, q[i]));\n'
                '    printf("\\n%zu %zu\\n", lower_bound(a, 0, 1), upper_bound(a, 0, 1));\n'
                '    size_t n = 5000000;\n'
                '    int *big = malloc(n * sizeof *big);\n'
                '    for (size_t i = 0; i < n; i++) big[i] = (int)(i / 3);\n'
                '    long long acc = 0;\n'
                '    for (int t = 0; t < 2000000; t++) acc += (long long)lower_bound(big, n, t % 1700000);\n'
                '    printf("%lld\\n", acc);\n'
                '    free(big);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Инвариант: ответ лежит в [lo, hi]. Середину берите как lo + (hi - lo) / 2, чтобы не '
              'переполнить.',
      'expected': ['0:0/0 1:0/1 2:1/4 3:4/4 5:4/5 8:5/7 9:7/7', '0 0', '4468330383333']},
     {'id': 'c3-insertion-sort',
      'mode': 'c',
      'title': 'Сортировка вставками',
      'statement': 'insertion_sort(int *a, size_t n) — отсортировать по возрастанию на месте (устойчиво). '
                   'is_sorted(const int *a, size_t n) → 1/0. Сортировка 3000 элементов должна занимать доли '
                   'секунды.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void insertion_sort(int *a, size_t n) {\n'
                 '}\n'
                 'int is_sorted(const int *a, size_t n) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {5, 2, 9, 1, 5, 6, -3, 0};\n'
                '    printf("%d\\n", is_sorted(a, 8));\n'
                '    insertion_sort(a, 8);\n'
                '    for (size_t i = 0; i < 8; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    printf("%d\\n", is_sorted(a, 8));\n'
                '    int b[3000];\n'
                '    unsigned s = 12345;\n'
                '    for (int i = 0; i < 3000; i++) { s = s * 1103515245u + 12345u; b[i] = (int)((s >> 16) % '
                '1000) - 500; }\n'
                '    insertion_sort(b, 3000);\n'
                '    printf("%d %d %d %d\\n", is_sorted(b, 3000), b[0], b[1500], b[2999]);\n'
                '    insertion_sort(b, 0);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Внутренний цикл сдвигает большие элементы вправо; индекс j должен быть беззнаковым осторожно: '
              'условие j > 0 стоит первым.',
      'expected': ['0', '-3 0 1 2 5 5 6 9', '1', '1 -500 4 499']},
     {'id': 'c3-partition',
      'mode': 'c',
      'title': 'Разбиение массива по опорному значению',
      'statement': 'partition(int *a, size_t n, int pivot) → size_t: переставьте элементы так, чтобы все '
                   'элементы < pivot оказались слева; верните их количество k. Порядок внутри групп не важен '
                   '(но результат проверяется как множество каждой стороны). Одним проходом, на месте.',
      'starter': '#include <stddef.h>\n\nsize_t partition(int *a, size_t n, int pivot) {\n    return 0;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'static int cmp(const void *x, const void *y) { return *(const int *)x - *(const int *)y; }\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {7, 1, 9, 3, 5, 3, 8, 2};\n'
                '    size_t k = partition(a, 8, 5);\n'
                '    int ok = 1;\n'
                '    for (size_t i = 0; i < 8; i++) if ((i < k) != (a[i] < 5)) ok = 0;\n'
                '    qsort(a, k, sizeof a[0], cmp);\n'
                '    qsort(a + k, 8 - k, sizeof a[0], cmp);\n'
                '    printf("%zu %d\\n", k, ok);\n'
                '    for (size_t i = 0; i < 8; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    int b[] = {1, 2, 3};\n'
                '    printf("%zu %zu\\n", partition(b, 3, 0), partition(b, 3, 100));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Указатель k отмечает границу «меньших»: каждый найденный меньший обменивается с элементом на '
              'позиции k.',
      'expected': ['4 1', '1 2 3 3 5 7 8 9', '0 3']},
     {'id': 'c3-merge',
      'mode': 'c',
      'title': 'Слияние двух отсортированных массивов',
      'statement': 'merge(const int *a, size_t na, const int *b, size_t nb, int *out) → size_t: слить два '
                   'отсортированных массива в out (длина na + nb), вернуть na + nb. При равных элементах '
                   'сначала берётся элемент из a. dedup_sorted(int *a, size_t n) → size_t: убрать повторы из '
                   'отсортированного массива на месте, вернуть новую длину.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t merge(const int *a, size_t na, const int *b, size_t nb, int *out) { return 0; }\n'
                 'size_t dedup_sorted(int *a, size_t n) { return n; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {1, 3, 5, 7}, b[] = {2, 3, 4, 8, 9}, out[9];\n'
                '    size_t n = merge(a, 4, b, 5, out);\n'
                '    printf("%zu: ", n);\n'
                '    for (size_t i = 0; i < n; i++) printf("%d ", out[i]); printf("\\n");\n'
                '    n = dedup_sorted(out, n);\n'
                '    printf("%zu: ", n);\n'
                '    for (size_t i = 0; i < n; i++) printf("%d ", out[i]); printf("\\n");\n'
                '    printf("%zu %zu\\n", merge(a, 0, b, 0, out), dedup_sorted(out, 0));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Два указателя-индекса идут по входным массивам; в dedup_sorted запись идёт на позицию w, '
              'чтение — на позицию i.',
      'expected': ['9: 1 2 3 3 4 5 7 8 9', '8: 1 2 3 4 5 7 8 9', '0 0']},
     {'id': 'c3-prefix-sums',
      'mode': 'c',
      'title': 'Префиксные суммы',
      'statement': 'build_prefix(const int *a, size_t n, long long *p) — заполнить p (длины n + 1): p[0] = '
                   '0, p[i + 1] = a[0] + … + a[i]. range_sum(const long long *p, size_t l, size_t r) → сумма '
                   'a[l..r) за O(1). Миллион запросов должен выполняться мгновенно.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void build_prefix(const int *a, size_t n, long long *p) {\n'
                 '}\n'
                 'long long range_sum(const long long *p, size_t l, size_t r) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {3, -1, 4, 1, -5, 9};\n'
                '    long long p[7];\n'
                '    build_prefix(a, 6, p);\n'
                '    printf("%lld %lld %lld %lld\\n", range_sum(p, 0, 6), range_sum(p, 1, 4), range_sum(p, '
                '2, 2), range_sum(p, 5, 6));\n'
                '    size_t n = 1000000;\n'
                '    int *big = malloc(n * sizeof *big);\n'
                '    long long *pp = malloc((n + 1) * sizeof *pp);\n'
                '    for (size_t i = 0; i < n; i++) big[i] = (int)(i % 7) - 3;\n'
                '    build_prefix(big, n, pp);\n'
                '    long long acc = 0;\n'
                '    for (size_t q = 0; q < 20000000; q++) acc += range_sum(pp, q % 1000, n - q % 999);\n'
                '    printf("%lld\\n", acc);\n'
                '    free(big); free(pp);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сумма отрезка — разность двух префиксных сумм: p[r] - p[l].',
      'expected': ['11 4 0 9', '80061']},
     {'id': 'c3-pointer-diff',
      'mode': 'c',
      'title': 'Указатели вместо индексов',
      'statement': 'find_ptr(const int *a, size_t n, int x) → const int *: указатель на первое вхождение x '
                   'или NULL. count_between(const int *first, const int *last) → число элементов в '
                   'полуинтервале [first, last). index_of(const int *a, size_t n, int x) → индекс или −1, '
                   'получаемый вычитанием указателей.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'const int *find_ptr(const int *a, size_t n, int x) { return NULL; }\n'
                 'size_t count_between(const int *first, const int *last) { return 0; }\n'
                 'long index_of(const int *a, size_t n, int x) { return -2; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {4, 8, 15, 16, 23, 42};\n'
                '    const int *p = find_ptr(a, 6, 16);\n'
                '    printf("%d %d\\n", p == a + 3, find_ptr(a, 6, 7) == NULL);\n'
                '    printf("%zu %zu %zu\\n", count_between(a, a + 6), count_between(a + 2, a + 5), '
                'count_between(a, a));\n'
                '    printf("%ld %ld %ld\\n", index_of(a, 6, 4), index_of(a, 6, 42), index_of(a, 6, 0));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Разность указателей на элементы одного массива — число элементов (тип ptrdiff_t).',
      'expected': ['1 1', '6 3 0', '0 5 -1']},
     {'id': 'c3-pointer-walk',
      'mode': 'c',
      'title': 'Обход указателем без индексации',
      'statement': 'sum_ptr(const int *a, size_t n) → long: сумма элементов; count_zeros(const int *a, '
                   'size_t n) → size_t; copy_ints(const int *src, int *dst, size_t n). Во всех трёх обходите '
                   'массив только арифметикой указателей: символ «[» в коде использовать нельзя.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'long sum_ptr(const int *a, size_t n) { return 0; }\n'
                 'size_t count_zeros(const int *a, size_t n) { return 0; }\n'
                 'void copy_ints(const int *src, int *dst, size_t n) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
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
                '    int a[] = {0, 5, 0, -2, 7, 0};\n'
                '    int b[6] = {9, 9, 9, 9, 9, 9};\n'
                '    printf("%ld %zu\\n", sum_ptr(a, 6), count_zeros(a, 6));\n'
                '    copy_ints(a, b, 6);\n'
                '    for (size_t i = 0; i < 6; i++) printf("%d ", b[i]); printf("\\n");\n'
                '    printf("%ld %zu\\n", sum_ptr(a, 0), count_zeros(a, 0));\n'
                '    printf("brackets: %d\\n", src_count("" "["));\n'
                '    return 0;\n'
                '}\n',
      'hint': '*p++ читает элемент и сдвигает указатель; конец цикла — сравнение с a + n.',
      'expected': ['10 3', '0 5 0 -2 7 0', '0 0', 'brackets: 0']},
     {'id': 'c3-matrix-flat',
      'mode': 'c',
      'title': 'Матрицы в плоском массиве',
      'statement': 'Матрица rows × cols хранится построчно в одном массиве. transpose(const int *a, size_t '
                   'rows, size_t cols, int *out) — транспонирование (out имеет размер cols × rows). '
                   'mat_mul(const int *a, const int *b, int *out, size_t n, size_t m, size_t p) — '
                   'произведение матриц n × m на m × p.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void transpose(const int *a, size_t rows, size_t cols, int *out) {\n'
                 '}\n'
                 'void mat_mul(const int *a, const int *b, int *out, size_t n, size_t m, size_t p) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {1, 2, 3, 4, 5, 6}, t[6];\n'
                '    transpose(a, 2, 3, t);\n'
                '    for (size_t i = 0; i < 6; i++) printf("%d ", t[i]); printf("\\n");\n'
                '    int b[] = {1, 0, 2, 1, 0, 3}, c[4];\n'
                '    mat_mul(a, b, c, 2, 3, 2);\n'
                '    for (size_t i = 0; i < 4; i++) printf("%d ", c[i]); printf("\\n");\n'
                '    int id[] = {1, 0, 0, 1}, d[4];\n'
                '    mat_mul(c, id, d, 2, 2, 2);\n'
                '    for (size_t i = 0; i < 4; i++) printf("%d ", d[i]); printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Элемент (i, j) матрицы с cols столбцами лежит по индексу i * cols + j.',
      'expected': ['1 4 2 5 3 6', '5 11 14 23', '5 11 14 23']},
     {'id': 'c3-array-2d',
      'mode': 'c',
      'title': 'Двумерный массив с фиксированным числом столбцов',
      'statement': 'Для массивов вида int a[][4]: row_sums(const int a[][4], size_t rows, long *out) — суммы '
                   'строк; col_max(const int a[][4], size_t rows, int *out) — максимумы столбцов (rows ≥ 1); '
                   'trace(const int a[4][4]) → int — сумма главной диагонали.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void row_sums(const int a[][4], size_t rows, long *out) {\n'
                 '}\n'
                 'void col_max(const int a[][4], size_t rows, int *out) {\n'
                 '}\n'
                 'int trace(const int a[4][4]) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[3][4] = {{1, 2, 3, 4}, {5, -6, 7, 8}, {9, 10, 11, -12}};\n'
                '    long rs[3];\n'
                '    int cm[4];\n'
                '    row_sums(a, 3, rs);\n'
                '    col_max(a, 3, cm);\n'
                '    printf("%ld %ld %ld\\n", rs[0], rs[1], rs[2]);\n'
                '    printf("%d %d %d %d\\n", cm[0], cm[1], cm[2], cm[3]);\n'
                '    int sq[4][4] = {{1, 0, 0, 0}, {0, 2, 0, 0}, {0, 0, 3, 0}, {0, 0, 0, 4}};\n'
                '    printf("%d\\n", trace(sq));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'В параметре двумерного массива число столбцов обязательно: const int a[][4].',
      'expected': ['10 14 18', '9 10 11 8', '10']},
     {'id': 'c3-spiral',
      'mode': 'c',
      'title': 'Обход матрицы по спирали',
      'statement': 'spiral(const int *a, size_t rows, size_t cols, int *out): записать элементы матрицы '
                   '(построчно хранимой) в порядке обхода по спирали по часовой стрелке, начиная с левого '
                   'верхнего угла.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void spiral(const int *a, size_t rows, size_t cols, int *out) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[12], out[12];\n'
                '    for (int i = 0; i < 12; i++) a[i] = i + 1;\n'
                '    spiral(a, 3, 4, out);\n'
                '    for (size_t i = 0; i < 12; i++) printf("%d ", out[i]); printf("\\n");\n'
                '    spiral(a, 4, 3, out);\n'
                '    for (size_t i = 0; i < 12; i++) printf("%d ", out[i]); printf("\\n");\n'
                '    spiral(a, 1, 5, out);\n'
                '    for (size_t i = 0; i < 5; i++) printf("%d ", out[i]); printf("\\n");\n'
                '    spiral(a, 5, 1, out);\n'
                '    for (size_t i = 0; i < 5; i++) printf("%d ", out[i]); printf("\\n");\n'
                '    spiral(a, 2, 2, out);\n'
                '    for (size_t i = 0; i < 4; i++) printf("%d ", out[i]); printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Четыре границы (top, bottom, left, right) сжимаются после каждой стороны; не забудьте '
              'проверить пересечение границ после каждого прохода.',
      'expected': ['1 2 3 4 8 12 11 10 9 5 6 7',
                   '1 2 3 6 9 12 11 10 7 4 5 8',
                   '1 2 3 4 5',
                   '1 2 3 4 5',
                   '1 2 4 3']},
     {'id': 'c3-pascal',
      'mode': 'c',
      'title': 'Треугольник Паскаля в двумерном массиве',
      'statement': 'pascal(int n, unsigned long t[][21]) — заполнить первые n (≤ 21) строк: t[i][j] — '
                   'биномиальный коэффициент C(i, j) для j ≤ i; остальное не трогать. binom(int n, int k, '
                   'unsigned long t[][21]) → t[n][k], если k ≤ n, иначе 0.',
      'starter': 'void pascal(int n, unsigned long t[][21]) {\n'
                 '}\n'
                 'unsigned long binom(int n, int k, unsigned long t[][21]) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    static unsigned long t[21][21];\n'
                '    pascal(21, t);\n'
                '    for (int i = 0; i < 6; i++) {\n'
                '        for (int j = 0; j <= i; j++) printf("%lu ", t[i][j]);\n'
                '        printf("\\n");\n'
                '    }\n'
                '    printf("%lu %lu %lu\\n", binom(20, 10, t), binom(5, 7, t), binom(0, 0, t));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Каждый внутренний элемент — сумма двух соседей строкой выше; края равны 1.',
      'expected': ['1', '1 1', '1 2 1', '1 3 3 1', '1 4 6 4 1', '1 5 10 10 5 1', '184756 0 1']},
     {'id': 'c3-skip-ptr',
      'mode': 'c',
      'title': 'Указатель на указатель: сдвиг по тексту',
      'statement': 'Строка читается через const char *s. skip_spaces(const char **p) — сдвинуть *p за все '
                   'пробелы; skip_digits(const char **p) → число пропущенных цифр; take_int(const char **p, '
                   'int *out) → 1, если сразу (после пробелов) идёт целое число (необязательный знак «-» или '
                   '«+»): записать его, сдвинуть *p за число; иначе 0 и *p не двигать.',
      'starter': 'void skip_spaces(const char **p) {\n'
                 '}\n'
                 'int skip_digits(const char **p) { return 0; }\n'
                 'int take_int(const char **p, int *out) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    const char *s = "   123abc";\n'
                '    skip_spaces(&s);\n'
                '    printf("[%s] ", s);\n'
                '    printf("%d [%s]\\n", skip_digits(&s), s);\n'
                '    const char *t = "  -42, 7 x";\n'
                '    int v;\n'
                '    while (take_int(&t, &v)) {\n'
                '        printf("%d|", v);\n'
                "        while (*t == ',') t++;\n"
                '    }\n'
                '    printf("[%s]\\n", t);\n'
                '    const char *u = "abc";\n'
                '    printf("%d %d [%s]\\n", take_int(&u, &v), skip_digits(&u), u);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Чтобы сдвинуть чужой указатель, разыменуйте его: (*p)++. В take_int работайте с локальной '
              'копией, а *p меняйте только при успехе.',
      'expected': ['[123abc] 3 [abc]', '-42|7|[ x]', '0 0 [abc]']},
     {'id': 'c3-ptr-table',
      'mode': 'c',
      'title': 'Массив указателей: таблица строк',
      'statement': 'day_name(int d) → const char *: d = 0..6 — «Mon» … «Sun» (из статического массива '
                   'указателей), иначе «?». table_len(void) → размер таблицы, вычисленный через sizeof. '
                   'longest_name(void) → индекс самого длинного названия из таблицы месяцев (Jan, Feb, …, '
                   'Dec; при равенстве — первое) и month_name(int m).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'const char *day_name(int d) { return ""; }\n'
                 'size_t table_len(void) { return 0; }\n'
                 'int longest_name(void) { return 0; }\n'
                 'const char *month_name(int m) { return ""; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    for (int d = -1; d <= 7; d++) printf("%s ", day_name(d));\n'
                '    printf("\\n%zu %d %s %s\\n", table_len(), longest_name(), month_name(longest_name()), '
                'month_name(12));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'static const char *t[] = {...}; число элементов — sizeof t / sizeof t[0]. Для самого длинного '
              'названия сравнивайте strlen.',
      'expected': ['? Mon Tue Wed Thu Fri Sat Sun ?', '7 5 June ?']},
     {'id': 'c3-my-mem',
      'mode': 'c',
      'title': 'Свои memcpy / memmove / memset / memcmp',
      'statement': 'Реализуйте my_memcpy, my_memmove (корректно при пересечении: копирование вперёд или '
                   'назад в зависимости от взаимного положения), my_memset и my_memcmp для void-указателей и '
                   'размера в байтах (unsigned char внутри). Библиотечные функции из <string.h> использовать '
                   'нельзя.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void *my_memcpy(void *dst, const void *src, size_t n) { return dst; }\n'
                 'void *my_memmove(void *dst, const void *src, size_t n) { return dst; }\n'
                 'void *my_memset(void *p, int c, size_t n) { return p; }\n'
                 'int my_memcmp(const void *a, const void *b, size_t n) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
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
                '    char buf[16] = "abcdefghij";\n'
                '    my_memmove(buf + 2, buf, 6);\n'
                '    printf("%.10s\\n", buf);\n'
                '    char b2[16] = "abcdefghij";\n'
                '    my_memmove(b2, b2 + 3, 6);\n'
                '    printf("%.10s\\n", b2);\n'
                '    char c[8];\n'
                "    my_memset(c, 'x', 7);\n"
                '    c[7] = 0;\n'
                '    printf("%s\\n", c);\n'
                '    int a[] = {1, 2, 3}, b[3];\n'
                '    my_memcpy(b, a, sizeof a);\n'
                '    printf("%d %d %d\\n", b[0], b[1], b[2]);\n'
                '    printf("%d %d %d\\n", my_memcmp("abc", "abd", 3), my_memcmp("abd", "abc", 3), '
                'my_memcmp("abc", "abx", 2));\n'
                '    printf("libc: %d\\n", src_count(" mem" "cpy(") + src_count(" mem" "move(") + '
                'src_count(" mem" "set(") + src_count(" mem" "cmp("));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'my_memmove: если dst < src — копируйте вперёд, иначе — с конца назад; так пересечение не '
              'портит ещё не скопированное.',
      'expected': ['ababcdefij', 'defghighij', 'xxxxxxx', '1 2 3', '-1 1 0', 'libc: 0']},
     {'id': 'c3-generic',
      'mode': 'c',
      'title': 'Универсальные функции на void *',
      'statement': 'swap_bytes(void *a, void *b, size_t n) — поменять местами два объекта размером n байт. '
                   'reverse_generic(void *base, size_t count, size_t size) — развернуть массив из count '
                   'элементов любого размера. find_elem(const void *base, size_t count, size_t size, const '
                   'void *key) → void *: указатель на первый элемент, побайтово равный *key, или NULL.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void swap_bytes(void *a, void *b, size_t n) {\n'
                 '}\n'
                 'void reverse_generic(void *base, size_t count, size_t size) {\n'
                 '}\n'
                 'void *find_elem(const void *base, size_t count, size_t size, const void *key) { return '
                 'NULL; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'struct pt { short x, y; };\n'
                '\n'
                'int main(void) {\n'
                '    double u = 1.5, v = -2.5;\n'
                '    swap_bytes(&u, &v, sizeof u);\n'
                '    printf("%.1f %.1f\\n", u, v);\n'
                '    int a[] = {1, 2, 3, 4, 5};\n'
                '    reverse_generic(a, 5, sizeof a[0]);\n'
                '    for (size_t i = 0; i < 5; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    struct pt s[3] = {{1, 2}, {3, 4}, {5, 6}};\n'
                '    reverse_generic(s, 3, sizeof s[0]);\n'
                '    printf("%d %d %d\\n", s[0].x, s[1].x, s[2].x);\n'
                '    char c[] = "hello";\n'
                '    reverse_generic(c, 5, 1);\n'
                '    printf("%s\\n", c);\n'
                '    int key = 4;\n'
                '    int *f = find_elem(a, 5, sizeof a[0], &key);\n'
                '    printf("%ld ", f ? (long)(f - a) : -1L);\n'
                '    key = 9;\n'
                '    printf("%d\\n", find_elem(a, 5, sizeof a[0], &key) == NULL);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для арифметики с void * приведите его к unsigned char * и умножайте индекс на size.',
      'expected': ['-2.5 1.5', '5 4 3 2 1', '5 3 1', 'olleh', '1 1']},
     {'id': 'c3-bitset',
      'mode': 'c',
      'title': 'Битовое множество в массиве байтов',
      'statement': 'Множество чисел 0..n−1 хранится в массиве uint8_t (по 8 чисел в байте). bs_set(uint8_t '
                   '*s, size_t i), bs_clear, bs_test(const uint8_t *s, size_t i) → 0/1, bs_count(const '
                   'uint8_t *s, size_t nbytes) → число элементов, bs_first(const uint8_t *s, size_t nbits) → '
                   'индекс первого элемента или nbits. Массив нужной длины создаёт вызывающий.',
      'starter': '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'void bs_set(uint8_t *s, size_t i) {}\n'
                 'void bs_clear(uint8_t *s, size_t i) {}\n'
                 'int bs_test(const uint8_t *s, size_t i) { return 0; }\n'
                 'size_t bs_count(const uint8_t *s, size_t nbytes) { return 0; }\n'
                 'size_t bs_first(const uint8_t *s, size_t nbits) { return nbits; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    uint8_t s[4] = {0};\n'
                '    size_t v[] = {3, 8, 9, 31, 17, 3};\n'
                '    for (int i = 0; i < 6; i++) bs_set(s, v[i]);\n'
                '    printf("%zu %zu\\n", bs_count(s, 4), bs_first(s, 32));\n'
                '    bs_clear(s, 3);\n'
                '    printf("%d %d %d %zu\\n", bs_test(s, 3), bs_test(s, 8), bs_test(s, 30), bs_first(s, '
                '32));\n'
                '    uint8_t e[2] = {0};\n'
                '    printf("%zu %zu\\n", bs_count(e, 2), bs_first(e, 16));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Номер байта — i / 8, номер бита в нём — i % 8; число единиц считайте приёмом b &= b - 1.',
      'expected': ['5 3', '0 1 0 8', '0 16']},
     {'id': 'c3-histogram',
      'mode': 'c',
      'title': 'Гистограмма байтов',
      'statement': 'histogram(const unsigned char *data, size_t n, size_t hist[256]) — подсчитать, сколько '
                   'раз встречается каждое значение байта (массив hist предварительно обнулять надо внутри '
                   'функции). mode_byte(const unsigned char *data, size_t n) → int: самый частый байт (при '
                   'равенстве — меньший), −1 для n = 0.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void histogram(const unsigned char *data, size_t n, size_t hist[256]) {\n'
                 '}\n'
                 'int mode_byte(const unsigned char *data, size_t n) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    unsigned char d[] = {1, 2, 2, 3, 3, 3, 255, 255, 255, 0};\n'
                '    size_t h[256];\n'
                '    histogram(d, sizeof d, h);\n'
                '    printf("%zu %zu %zu %zu %zu\\n", h[0], h[1], h[2], h[3], h[255]);\n'
                '    printf("%d %d\\n", mode_byte(d, sizeof d), mode_byte(d, 0));\n'
                '    unsigned char t[] = {7, 7, 9, 9};\n'
                '    printf("%d\\n", mode_byte(t, 4));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Значение байта (unsigned char) — готовый индекс в массиве счётчиков из 256 элементов.',
      'expected': ['1 1 2 3 3', '3 -1', '7']},
     {'id': 'c3-fix-sizeof',
      'mode': 'c',
      'title': 'Исправьте: sizeof параметра-массива',
      'statement': 'mean(a) считает среднее массива через sizeof(a) / sizeof(a[0]) внутри функции, но там a '
                   '— указатель, и результат неверен. Исправьте сигнатуру: пусть длина передаётся вторым '
                   'параметром size_t n (драйвер уже вызывает mean(a, n)).',
      'starter': 'double mean(const int a[]) {\n'
                 '    long s = 0;\n'
                 '    size_t n = sizeof(a) / sizeof(a[0]);\n'
                 '    for (size_t i = 0; i < n; i++) s += a[i];\n'
                 '    return (double)s / n;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {2, 4, 6, 8, 10, 12};\n'
                '    printf("%.2f %.2f\\n", mean(a, 6), mean(a, 3));\n'
                '    printf("%.2f\\n", mean(a, 0));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'int mean(const int a[], size_t n): размер массива известен только там, где он объявлен, '
              'поэтому его передают.',
      'expected': ['7.00 4.00', '0.00']},
     {'id': 'c3-fix-const',
      'mode': 'c',
      'title': 'Исправьте: запись через указатель на const',
      'statement': 'fill(a, n, v) должна записать v во все n элементов, но параметр объявлен как const int '
                   '*a, и компилятор запрещает запись. Исправьте сигнатуру. А sum_all остаётся только '
                   'читающей — для неё const нужен.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void fill(const int *a, size_t n, int v) {\n'
                 '    for (size_t i = 0; i < n; i++) a[i] = v;\n'
                 '}\n'
                 '\n'
                 'long sum_all(int *a, size_t n) {\n'
                 '    long s = 0;\n'
                 '    for (size_t i = 0; i < n; i++) s += a[i];\n'
                 '    return s;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[5] = {0};\n'
                '    fill(a, 5, 7);\n'
                '    const int *ca = a;\n'
                '    printf("%ld %d\\n", sum_all(ca, 5), a[4]);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Пишущей функции нужен int *, читающей — const int *; тогда ей можно передать и const-массив '
              '(драйвер так и делает).',
      'expected': ['35 7']},
     {'id': 'c3-fix-overflow',
      'mode': 'c',
      'title': 'Исправьте: выход за границу массива',
      'statement': 'copy_reversed(src, dst, n) копирует src в dst в обратном порядке. Из-за границы i <= n '
                   'функция пишет за пределы dst. Программа запускается с AddressSanitizer — он остановит '
                   'её. Исправьте границы цикла.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'void copy_reversed(const int *src, int *dst, size_t n) {\n'
                 '    for (size_t i = 0; i <= n; i++) {\n'
                 '        dst[i] = src[n - 1 - i];\n'
                 '    }\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int s[4] = {1, 2, 3, 4};\n'
                '    int d[4];\n'
                '    copy_reversed(s, d, 4);\n'
                '    for (size_t i = 0; i < 4; i++) printf("%d ", d[i]); printf("\\n");\n'
                '    copy_reversed(s, d, 0);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Индексы массива из n элементов — от 0 до n − 1: условие i < n.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['4 3 2 1']},
     {'id': 'c3-fix-local-address',
      'mode': 'c',
      'title': 'Исправьте: адрес локального массива',
      'statement': 'make_squares(n) строит массив квадратов и возвращает указатель на локальный массив — '
                   'после возврата он недействителен. Исправьте: функция должна записывать результат в '
                   'массив, который передаёт вызывающий (параметр out), и возвращать число записанных '
                   'элементов. Компиляция идёт с -Werror=return-local-addr.',
      'starter': 'int *make_squares(int n) {\n'
                 '    int a[16];\n'
                 '    for (int i = 0; i < n && i < 16; i++) a[i] = i * i;\n'
                 '    return a;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int out[16];\n'
                '    int c = make_squares(5, out);\n'
                '    printf("%d:", c);\n'
                '    for (int i = 0; i < c; i++) printf(" %d", out[i]);\n'
                '    printf("\\n%d\\n", make_squares(100, out));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сигнатура int make_squares(int n, int *out): память под результат принадлежит вызывающему.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -Werror=return-local-addr',
      'expected': ['5: 0 1 4 9 16', '16']},
     {'id': 'c3-fix-read-past',
      'mode': 'c',
      'title': 'Исправьте: чтение за концом массива',
      'statement': 'max_of(a, n) ищет наибольший элемент, но в цикле читает a[n], а это уже чужая память. '
                   'Программа запускается с AddressSanitizer. Исправьте так, чтобы читались только a[0]…a[n '
                   '− 1].',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int max_of(const int *a, size_t n) {\n'
                 '    int m = a[0];\n'
                 '    for (size_t i = 1; i <= n; i++) {\n'
                 '        if (a[i] > m) m = a[i];\n'
                 '    }\n'
                 '    return m;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[5] = {3, 8, 1, 9, 2};\n'
                '    printf("%d %d\\n", max_of(a, 5), max_of(a, 2));\n'
                '    int one[1] = {-5};\n'
                '    printf("%d\\n", max_of(one, 1));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Условие продолжения цикла — i < n, а не i <= n.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['9 8', '-5']},
     {'id': 'c3-two-pointers',
      'mode': 'c',
      'title': 'Два указателя по отсортированному массиву',
      'statement': 'two_sum_sorted(const int *a, size_t n, int target, size_t *i, size_t *j) → int: в '
                   'отсортированном по возрастанию массиве найти индексы i < j с a[i] + a[j] == target; '
                   'вернуть 1 и записать индексы, или 0. Один проход двумя указателями, O(n): массив из '
                   'миллиона элементов при двойном цикле не успеет.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int two_sum_sorted(const int *a, size_t n, int target, size_t *i, size_t *j) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {1, 3, 4, 6, 9, 11};\n'
                '    size_t i = 99, j = 99;\n'
                '    int ok = two_sum_sorted(a, 6, 10, &i, &j);\n'
                '    printf("%d %zu %zu\\n", ok, i, j);\n'
                '    ok = two_sum_sorted(a, 6, 100, &i, &j);\n'
                '    printf("%d %zu %zu\\n", ok, i, j);\n'
                '    size_t n = 1000000;\n'
                '    int *big = malloc(n * sizeof *big);\n'
                '    for (size_t k = 0; k < n; k++) big[k] = (int)(2 * k);\n'
                '    ok = two_sum_sorted(big, n, (int)(2 * (n - 2) + 2 * (n - 1)), &i, &j);\n'
                '    printf("%d %zu %zu\\n", ok, i, j);\n'
                '    ok = two_sum_sorted(big, n, 1, &i, &j);\n'
                '    printf("%d\\n", ok);\n'
                '    free(big);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сумма меньше цели — двигайте левый указатель вправо, больше — правый влево.',
      'expected': ['1 0 4', '0 0 4', '1 999998 999999', '0']},
     {'id': 'c3-dutch-flag',
      'mode': 'c',
      'title': 'Три цвета за один проход',
      'statement': 'sort012(int *a, size_t n): массив содержит только 0, 1 и 2; отсортируйте его на месте за '
                   'один проход (три указателя: границы нулей и двоек, текущая позиция), без подсчёта и без '
                   'qsort.',
      'starter': '#include <stddef.h>\n\nvoid sort012(int *a, size_t n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
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
                '    int a[] = {2, 0, 2, 1, 1, 0, 0, 2, 1};\n'
                '    sort012(a, 9);\n'
                '    for (size_t i = 0; i < 9; i++) printf("%d ", a[i]); printf("\\n");\n'
                '    size_t n = 2000000;\n'
                '    int *b = malloc(n * sizeof *b);\n'
                '    unsigned s = 7;\n'
                '    for (size_t i = 0; i < n; i++) { s = s * 1664525u + 1013904223u; b[i] = (int)((s >> 24) '
                '% 3); }\n'
                '    sort012(b, n);\n'
                '    int ok = 1;\n'
                '    for (size_t i = 1; i < n; i++) if (b[i - 1] > b[i]) ok = 0;\n'
                '    printf("%d %d %d\\n", ok, b[0], b[n - 1]);\n'
                '    free(b);\n'
                '    printf("qsort: %d\\n", src_count("qso" "rt("));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Инвариант: [0, lo) — нули, [lo, mid) — единицы, [hi, n) — двойки; при обмене с правой '
              'границей mid не увеличивается.',
      'expected': ['0 0 0 1 1 1 2 2 2', '1 0 2', 'qsort: 0']},
     {'id': 'c3-kadane',
      'mode': 'c',
      'title': 'Наибольшая сумма подмассива',
      'statement': 'max_subarray(const int *a, size_t n, size_t *start, size_t *len) → long long: наибольшая '
                   'сумма непустого подмассива подряд идущих элементов; в *start и *len — первое такое '
                   'решение с наименьшим start (при равных суммах — более короткое). n ≥ 1. За один проход.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'long long max_subarray(const int *a, size_t n, size_t *start, size_t *len) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {-2, 1, -3, 4, -1, 2, 1, -5, 4};\n'
                '    size_t s, l;\n'
                '    long long r = max_subarray(a, 9, &s, &l);\n'
                '    printf("%lld %zu %zu\\n", r, s, l);\n'
                '    int b[] = {-5, -2, -9};\n'
                '    r = max_subarray(b, 3, &s, &l);\n'
                '    printf("%lld %zu %zu\\n", r, s, l);\n'
                '    int c[] = {3};\n'
                '    r = max_subarray(c, 1, &s, &l);\n'
                '    printf("%lld %zu %zu\\n", r, s, l);\n'
                '    size_t n = 3000000;\n'
                '    int *big = malloc(n * sizeof *big);\n'
                '    for (size_t i = 0; i < n; i++) big[i] = (i % 5 == 0) ? -7 : 2;\n'
                '    r = max_subarray(big, n, &s, &l);\n'
                '    printf("%lld %zu %zu\\n", r, s, l);\n'
                '    free(big);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Если накопленная сумма стала отрицательной — начинайте новый подмассив с текущего элемента '
              '(алгоритм Кадане).',
      'expected': ['6 3 4', '-2 1 1', '3 0 1', '600007 1 2999999']}],
 4: [{'id': 'c4-str-basic',
      'mode': 'c',
      'title': 'Свои strlen, strcpy, strcat, strcmp',
      'statement': 'Реализуйте my_strlen, my_strcpy (копирует вместе с нулём, возвращает dst), my_strcat '
                   '(дописывает src в конец dst, возвращает dst) и my_strcmp (отрицательное, нуль или '
                   'положительное; сравнение по unsigned char). Функции из <string.h> использовать нельзя.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t my_strlen(const char *s) { return 0; }\n'
                 'char *my_strcpy(char *dst, const char *src) { return dst; }\n'
                 'char *my_strcat(char *dst, const char *src) { return dst; }\n'
                 'int my_strcmp(const char *a, const char *b) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
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
                '    char buf[32];\n'
                '    my_strcpy(buf, "foo");\n'
                '    my_strcat(buf, "bar");\n'
                '    printf("%s %zu %zu\\n", buf, my_strlen(buf), my_strlen(""));\n'
                '    printf("%d %d %d %d\\n", my_strcmp("abc", "abc") == 0, my_strcmp("abc", "abd") < 0, '
                'my_strcmp("b", "a") > 0, my_strcmp("ab", "abc") < 0);\n'
                '    printf("%d\\n", my_strcmp("\\xff", "a") > 0);\n'
                '    printf("libc: %d\\n", src_count(" str" "len(") + src_count(" str" "cpy(") + src_count(" '
                'str" "cmp("));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Копирование: while ((*d++ = *src++)); — присваивание сразу завершается, когда скопирован '
              'нуль.',
      'expected': ['foobar 6 0', '1 1 1 1', '1', 'libc: 0']},
     {'id': 'c4-str-search',
      'mode': 'c',
      'title': 'Поиск в строке: strchr, strrchr, strstr',
      'statement': 'my_strchr(s, c) — указатель на первое вхождение символа (в том числе завершающего нуля, '
                   'если c == 0) или NULL; my_strrchr — на последнее; my_strstr(hay, needle) — на первое '
                   'вхождение подстроки (пустая — сама hay) или NULL.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'char *my_strchr(const char *s, int c) { return NULL; }\n'
                 'char *my_strrchr(const char *s, int c) { return NULL; }\n'
                 'char *my_strstr(const char *hay, const char *needle) { return NULL; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    const char *s = "hello, world";\n'
                '    printf("%ld %ld %ld\\n", (long)(my_strchr(s, \'o\') - s), (long)(my_strrchr(s, \'o\') - '
                's), (long)(my_strchr(s, 0) - s));\n'
                '    printf("%d %d\\n", my_strchr(s, \'z\') == NULL, my_strrchr(s, \'z\') == NULL);\n'
                '    printf("%ld %ld %ld\\n", (long)(my_strstr(s, "world") - s), (long)(my_strstr(s, "") - '
                's), (long)(my_strstr(s, "lo, w") - s));\n'
                '    printf("%d %d\\n", my_strstr(s, "worlds") == NULL, my_strstr("aab", "ab") != NULL);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для strchr цикл должен останавливаться и на нуле: нуль — тоже допустимый искомый символ.',
      'expected': ['4 8 12', '1 1', '7 0 3', '1 1']},
     {'id': 'c4-str-palindrome',
      'mode': 'c',
      'title': 'Разворот и палиндромы',
      'statement': 'reverse_str(char *s) — развернуть строку на месте. is_pal(const char *s) → 1, если '
                   'строка — палиндром, игнорируя регистр и все символы, кроме латинских букв и цифр '
                   '(ASCII).',
      'starter': 'void reverse_str(char *s) {\n}\nint is_pal(const char *s) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char a[] = "hello";\n'
                '    char b[] = "";\n'
                '    char c[] = "x";\n'
                '    reverse_str(a); reverse_str(b); reverse_str(c);\n'
                '    printf("%s [%s] %s\\n", a, b, c);\n'
                '    printf("%d %d %d %d\\n", is_pal("A man, a plan, a canal: Panama"), is_pal("hello"), '
                'is_pal(""), is_pal("Was it a car or a cat I saw?"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Два указателя — с начала и с конца: пропускайте небуквенные символы с обеих сторон и '
              'сравнивайте в нижнем регистре.',
      'expected': ['olleh [] x', '1 0 1 1']},
     {'id': 'c4-str-case',
      'mode': 'c',
      'title': 'Регистр: upper, lower, capitalize',
      'statement': 'to_upper(char *s) и to_lower(char *s) — на месте, только латинские буквы ASCII. '
                   'capitalize_words(char *s) — первая буква каждого слова (слова разделены пробелами) '
                   'заглавная, остальные строчные.',
      'starter': 'void to_upper(char *s) {\n'
                 '}\n'
                 'void to_lower(char *s) {\n'
                 '}\n'
                 'void capitalize_words(char *s) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char a[] = "Hello, World 123!";\n'
                '    to_upper(a); printf("%s\\n", a);\n'
                '    to_lower(a); printf("%s\\n", a);\n'
                '    char b[] = "tHE qUICK  bROWN fox";\n'
                '    capitalize_words(b); printf("%s\\n", b);\n'
                '    char c[] = "";\n'
                '    capitalize_words(c); printf("[%s]\\n", c);\n'
                '    return 0;\n'
                '}\n',
      'hint': "Разница между 'a' и 'A' постоянна (32): s -= 'a' - 'A' превращает строчную букву в заглавную.",
      'expected': ['HELLO, WORLD 123!', 'hello, world 123!', 'The Quick  Brown Fox', '[]']},
     {'id': 'c4-trim',
      'mode': 'c',
      'title': 'Обрезка пробелов на месте',
      'statement': 'trim(char *s) → char *: убрать пробельные символы (пробел, \\t, \\n, \\r) с обоих '
                   'концов; вернуть указатель на первый непробельный символ внутри той же строки, а '
                   'завершающий нуль переставить так, чтобы хвост был отрезан. Память не выделять.',
      'starter': 'char *trim(char *s) {\n    return s;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char a[] = "  \\t hello world \\n ";\n'
                '    char b[] = "   ";\n'
                '    char c[] = "x";\n'
                '    char d[] = "";\n'
                '    printf("[%s] [%s] [%s] [%s]\\n", trim(a), trim(b), trim(c), trim(d));\n'
                '    char e[] = "  a b  ";\n'
                '    char *t = trim(e);\n'
                '    printf("%d [%s]\\n", (int)(t - e), t);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сначала сдвиньте указатель начала, затем сдвигайте конец назад и запишите нуль на новое '
              'место.',
      'expected': ['[hello world] [] [x] []', '2 [a b]']},
     {'id': 'c4-count-words',
      'mode': 'c',
      'title': 'Слова и символы в тексте',
      'statement': 'count_words(const char *s) → число слов (слова разделены любым числом пробелов, '
                   'табуляций и переводов строк). longest_word_len(const char *s) → длина самого длинного '
                   'слова. count_char(const char *s, char c) → сколько раз встречается c.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t count_words(const char *s) { return 0; }\n'
                 'size_t longest_word_len(const char *s) { return 0; }\n'
                 'size_t count_char(const char *s, char c) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    const char *t = "  the quick\\tbrown\\nfox   jumps ";\n'
                '    printf("%zu %zu %zu\\n", count_words(t), longest_word_len(t), count_char(t, \'o\'));\n'
                '    printf("%zu %zu %zu\\n", count_words(""), count_words("   "), longest_word_len(""));\n'
                '    printf("%zu\\n", count_words("one"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Слово начинается там, где непробельный символ идёт после пробельного (или после начала '
              'строки).',
      'expected': ['5 5 2', '0 0 0', '1']},
     {'id': 'c4-parse-int',
      'mode': 'c',
      'title': 'Разбор целого вручную',
      'statement': 'parse_int(const char *s, int *out) → int: пробелы в начале игнорировать; необязательный '
                   'знак; затем одна или более цифр до конца строки (хвост запрещён). Коды: 0 — успех (число '
                   'записано), −1 — не число, −2 — не помещается в int. Проверку переполнения делайте до '
                   'умножения, без long long и без стандартных strtol/atoi.',
      'starter': 'int parse_int(const char *s, int *out) {\n    return -1;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
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
                '    const char *t[] = {"42", "  -17", "+5", "", "-", "12x", "2147483647", "2147483648", '
                '"-2147483648", "-2147483649", "99999999999999999999", " 007"};\n'
                '    for (int i = 0; i < 12; i++) {\n'
                '        int v = 12345;\n'
                '        int r = parse_int(t[i], &v);\n'
                '        printf("[%s] %d %d\\n", t[i], r, r == 0 ? v : 12345);\n'
                '    }\n'
                '    printf("libc: %d\\n", src_count("str" "tol") + src_count("at" "oi"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для положительных проверяйте v > (INT_MAX - d) / 10 перед v * 10 + d; отрицательные '
              'накапливайте вниз, чтобы поместился INT_MIN.',
      'expected': ['[42] 0 42',
                   '[  -17] 0 -17',
                   '[+5] 0 5',
                   '[] -1 12345',
                   '[-] -1 12345',
                   '[12x] -1 12345',
                   '[2147483647] 0 2147483647',
                   '[2147483648] -2 12345',
                   '[-2147483648] 0 -2147483648',
                   '[-2147483649] -2 12345',
                   '[99999999999999999999] -2 12345',
                   '[ 007] 0 7',
                   'libc: 0']},
     {'id': 'c4-strtol',
      'mode': 'c',
      'title': 'strtol: надёжный разбор',
      'statement': 'safe_parse(const char *s, long *out) → int: через strtol, основание 10. 0 — успех; 1 — '
                   'пустая строка или нет ни одной цифры; 2 — после числа есть лишние символы; 3 — число не '
                   'помещается в long (errno == ERANGE). Пробелы в начале допустимы (так делает strtol). '
                   'errno перед вызовом сбрасывайте.',
      'starter': '#include <errno.h>\n'
                 '#include <stdlib.h>\n'
                 '\n'
                 'int safe_parse(const char *s, long *out) {\n'
                 '    return 1;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    const char *t[] = {"123", "  -45", "", "abc", "12abc", "9223372036854775807", '
                '"9223372036854775808", "-9223372036854775808", "0x10", "  "};\n'
                '    for (int i = 0; i < 10; i++) {\n'
                '        long v = -1;\n'
                '        int r = safe_parse(t[i], &v);\n'
                '        printf("[%s] %d %ld\\n", t[i], r, r == 0 ? v : -1L);\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Порядок проверок: end == s (ничего не разобрано) → ERANGE → хвост *end != 0.',
      'expected': ['[123] 0 123',
                   '[  -45] 0 -45',
                   '[] 1 -1',
                   '[abc] 1 -1',
                   '[12abc] 2 -1',
                   '[9223372036854775807] 0 9223372036854775807',
                   '[9223372036854775808] 3 -1',
                   '[-9223372036854775808] 0 -9223372036854775808',
                   '[0x10] 2 -1',
                   '[  ] 1 -1']},
     {'id': 'c4-itoa',
      'mode': 'c',
      'title': 'Число в строку: свой itoa',
      'statement': 'int_to_str(long long v, char *buf, size_t cap) → int: записать десятичное представление '
                   'в buf (с завершающим нулём) и вернуть длину строки; если строка с нулём не помещается в '
                   'cap — вернуть −1 и записать в buf[0] нуль (если cap > 0). Корректно обработайте '
                   'LLONG_MIN и 0. snprintf и sprintf использовать нельзя.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int int_to_str(long long v, char *buf, size_t cap) {\n'
                 '    return -1;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
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
                '    char b[32];\n'
                '    long long v[] = {0, 7, -7, 1234567890123LL, LLONG_MAX, LLONG_MIN};\n'
                '    for (int i = 0; i < 6; i++) {\n'
                '        int n = int_to_str(v[i], b, sizeof b);\n'
                '        printf("%d %s\\n", n, b);\n'
                '    }\n'
                '    char s[4];\n'
                '    printf("%d %d\\n", int_to_str(999, s, 4), int_to_str(1000, s, 4));\n'
                '    printf("[%s] %d\\n", s, int_to_str(5, s, 0));\n'
                '    printf("printf: %d\\n", src_count("pri" "ntf(") );\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Работайте с unsigned long long: модуль LLONG_MIN в знаковом типе не помещается. Цифры '
              'получаются младшими вперёд — разверните.',
      'expected': ['1 0',
                   '1 7',
                   '2 -7',
                   '13 1234567890123',
                   '19 9223372036854775807',
                   '20 -9223372036854775808',
                   '3 -1',
                   '[] -1',
                   'printf: 0']},
     {'id': 'c4-base-conv',
      'mode': 'c',
      'title': 'Системы счисления',
      'statement': 'to_base(unsigned long n, unsigned base, char *buf) — записать n в системе base (2..36, '
                   'цифры 0-9a-z, без ведущих нулей, для 0 — «0»). from_base(const char *s, unsigned base) → '
                   'long: прочитать число (допускаются цифры и буквы любого регистра), −1 при неверном '
                   'символе или пустой строке.',
      'starter': 'void to_base(unsigned long n, unsigned base, char *buf) {\n'
                 '}\n'
                 'long from_base(const char *s, unsigned base) { return -1; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char b[80];\n'
                '    unsigned long n[] = {0, 255, 1000, 123456789};\n'
                '    unsigned base[] = {2, 8, 16, 36};\n'
                '    for (int i = 0; i < 4; i++) {\n'
                '        for (int j = 0; j < 4; j++) {\n'
                '            to_base(n[i], base[j], b);\n'
                '            printf("%s ", b);\n'
                '        }\n'
                '        printf("\\n");\n'
                '    }\n'
                '    printf("%ld %ld %ld %ld %ld\\n", from_base("ff", 16), from_base("FF", 16), '
                'from_base("102", 2), from_base("", 10), from_base("zz", 36));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Цифры собираются от младшей к старшей — запишите их во временный массив и разверните.',
      'expected': ['0 0 0 0',
                   '11111111 377 ff 73',
                   '1111101000 1750 3e8 rs',
                   '111010110111100110100010101 726746425 75bcd15 21i3v9',
                   '255 255 -1 -1 1295']},
     {'id': 'c4-split',
      'mode': 'c',
      'title': 'Разбиение строки на месте',
      'statement': 'split(char *s, char sep, char **out, size_t max) → size_t: заменить каждый sep на нуль и '
                   'записать в out указатели на начала полей (пустые поля сохраняются); не более max полей. '
                   'Вернуть число полей. Памяти не выделять.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t split(char *s, char sep, char **out, size_t max) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char a[] = "a,bb,,ccc,";\n'
                '    char *f[8];\n'
                "    size_t n = split(a, ',', f, 8);\n"
                '    printf("%zu:", n);\n'
                '    for (size_t i = 0; i < n; i++) printf(" [%s]", f[i]);\n'
                '    printf("\\n");\n'
                '    char b[] = "x y z";\n'
                "    n = split(b, ' ', f, 2);\n"
                '    printf("%zu: [%s] [%s]\\n", n, f[0], f[1]);\n'
                '    char c[] = "";\n'
                "    n = split(c, ',', f, 8);\n"
                '    printf("%zu [%s]\\n", n, f[0]);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Поле начинается после каждого разделителя; пустая строка — одно пустое поле.',
      'expected': ['5: [a] [bb] [] [ccc] []', '2: [x] [y]', '1 []']},
     {'id': 'c4-kv-parse',
      'mode': 'c',
      'title': 'Разбор «ключ=значение» в буферы',
      'statement': 'parse_kv(const char *line, char *key, size_t kcap, char *val, size_t vcap) → int: '
                   'разделить строку по первому «=» на ключ и значение; пробелы по краям обрезать; результат '
                   'в key и val с завершающим нулём. Вернуть 1, если «=» есть и ключ не пуст; 0 иначе. Если '
                   'ключ или значение не помещаются, они обрезаются (нуль всегда на месте).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int parse_kv(const char *line, char *key, size_t kcap, char *val, size_t vcap) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char k[8], v[8];\n'
                '    const char *t[] = {"name = rust", "  a=1", "novalue", "=x", "long_key_name = '
                'long_value_text", "k=  spaced out  ", "a=b=c"};\n'
                '    for (int i = 0; i < 7; i++) {\n'
                '        int r = parse_kv(t[i], k, sizeof k, v, sizeof v);\n'
                '        printf("%d [%s] [%s]\\n", r, r ? k : "", r ? v : "");\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Найдите «=» через strchr; ключ — левая часть, значение — всё справа до конца строки; '
              'копируйте не больше cap − 1 байт.',
      'expected': ['1 [name] [rust]',
                   '1 [a] [1]',
                   '0 [] []',
                   '0 [] []',
                   '1 [long_ke] [long_va]',
                   '1 [k] [spaced ]',
                   '1 [a] [b=c]']},
     {'id': 'c4-rle',
      'mode': 'c',
      'title': 'Кодирование повторов (RLE)',
      'statement': 'rle_encode(const char *s, char *out, size_t cap) → int: «aaabcc» → «a3b1c2» (символ и '
                   'десятичное число повторов, повтор считается для любых символов, кроме цифр на входе — на '
                   'входе только не-цифры). Вернуть длину результата или −1, если результат с нулём не '
                   'помещается в cap. rle_decode(const char *s, char *out, size_t cap) → int: обратное '
                   'преобразование; те же правила возврата.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int rle_encode(const char *s, char *out, size_t cap) { return -1; }\n'
                 'int rle_decode(const char *s, char *out, size_t cap) { return -1; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char e[64], d[64];\n'
                '    const char *t[] = {"aaabcc", "", "z", "abcdef", "xxxxxxxxxxxx"};\n'
                '    for (int i = 0; i < 5; i++) {\n'
                '        int n = rle_encode(t[i], e, sizeof e);\n'
                '        int m = rle_decode(e, d, sizeof d);\n'
                '        printf("%d [%s] %d %d\\n", n, e, m, m >= 0 && strcmp(d, t[i]) == 0);\n'
                '    }\n'
                '    char tiny[4];\n'
                '    printf("%d %d\\n", rle_encode("aaabcc", tiny, sizeof tiny), rle_decode("a9", tiny, '
                'sizeof tiny));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Считайте длину серии внутренним циклом; число повторов можно напечатать через snprintf во '
              'временный буфер.',
      'expected': ['6 [a3b1c2] 6 1',
                   '0 [] 0 1',
                   '2 [z1] 1 1',
                   '12 [a1b1c1d1e1f1] 6 1',
                   '3 [x12] 12 1',
                   '-1 -1']},
     {'id': 'c4-vigenere',
      'mode': 'c',
      'title': 'Шифр Виженера',
      'statement': 'vigenere(char *s, const char *key, int decrypt): шифрует (decrypt = 0) или '
                   'расшифровывает латинские буквы строки на месте; ключ — строчные латинские буквы (сдвиги '
                   'a=0…z=25), ключ используется по кругу, продвигаясь только на буквах; остальные символы '
                   'не меняются, регистр сохраняется.',
      'starter': 'void vigenere(char *s, const char *key, int decrypt) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char a[] = "Attack at Dawn!";\n'
                '    vigenere(a, "lemon", 0);\n'
                '    printf("%s\\n", a);\n'
                '    vigenere(a, "lemon", 1);\n'
                '    printf("%s\\n", a);\n'
                '    char b[] = "xyz";\n'
                '    vigenere(b, "b", 0);\n'
                '    printf("%s\\n", b);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сдвиг при расшифровке — 26 − сдвиг; указатель на букву ключа двигается только после '
              'обработанной буквы текста.',
      'expected': ['Lxfopv ef Rnhr!', 'Attack at Dawn!', 'yza']},
     {'id': 'c4-join',
      'mode': 'c',
      'title': 'Склейка строк через snprintf',
      'statement': 'join(char *out, size_t cap, const char *const *parts, size_t n, const char *sep) → '
                   'size_t: записать parts[0] sep parts[1] sep … в out без переполнения (результат всегда '
                   'завершён нулём, если cap > 0) и вернуть длину полной строки, которая получилась бы при '
                   'неограниченном буфере. Каждая часть добавляется через snprintf.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t join(char *out, size_t cap, const char *const *parts, size_t n, const char *sep) {\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    const char *p[] = {"alpha", "beta", "gamma"};\n'
                '    char b[64];\n'
                '    size_t n = join(b, sizeof b, p, 3, ", ");\n'
                '    printf("%zu [%s]\\n", n, b);\n'
                '    char s[10];\n'
                '    n = join(s, sizeof s, p, 3, "-");\n'
                '    printf("%zu [%s]\\n", n, s);\n'
                '    n = join(s, sizeof s, p, 0, "-");\n'
                '    printf("%zu [%s]\\n", n, s);\n'
                '    n = join(s, 0, p, 3, "-");\n'
                '    printf("%zu\\n", n);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Следите за тем, сколько уже записано: если места нет, snprintf не вызывайте, но длину всё '
              'равно учитывайте.',
      'expected': ['18 [alpha, beta, gamma]', '16 [alpha-bet]', '0 []', '16']},
     {'id': 'c4-fix-strcpy',
      'mode': 'c',
      'title': 'Исправьте: переполнение буфера в greet',
      'statement': 'greet(name, out, cap) должна записать в out строку «Hello, <name>!» без выхода за '
                   'границы (cap — размер out; если не помещается — обрезать, нуль в конце обязателен). '
                   'Заготовка использует strcpy и strcat и ломает память (запуск с AddressSanitizer). '
                   'Перепишите через snprintf.',
      'starter': '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '\n'
                 'void greet(const char *name, char *out, size_t cap) {\n'
                 '    strcpy(out, "Hello, ");\n'
                 '    strcat(out, name);\n'
                 '    strcat(out, "!");\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char a[32], b[12];\n'
                '    greet("Rust", a, sizeof a);\n'
                '    printf("%s\\n", a);\n'
                '    greet("a very long name indeed", b, sizeof b);\n'
                '    printf("%s %zu\\n", b, strlen(b));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'snprintf(out, cap, "Hello, %s!", name) сам не выйдет за cap и всегда поставит нуль.',
      'expected': ['Hello, Rust!', 'Hello, a ve 11']},
     {'id': 'c4-fix-strncpy',
      'mode': 'c',
      'title': 'Исправьте: strncpy без завершающего нуля',
      'statement': 'copy_name(dst, cap, src) должна скопировать src в dst, обрезав по размеру, и всегда '
                   'оставить в dst корректную строку. Сейчас, если src не помещается, нуля нет, и печать '
                   'читает мусор. Исправьте, не используя snprintf.',
      'starter': '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '\n'
                 'void copy_name(char *dst, size_t cap, const char *src) {\n'
                 '    strncpy(dst, src, cap);\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
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
                '    char a[6];\n'
                "    memset(a, 'x', sizeof a);\n"
                '    copy_name(a, sizeof a, "abcdefghij");\n'
                '    printf("%s %zu\\n", a, strlen(a));\n'
                "    memset(a, 'x', sizeof a);\n"
                '    copy_name(a, sizeof a, "hi");\n'
                '    printf("%s %zu\\n", a, strlen(a));\n'
                "    char z[1] = {'q'};\n"
                '    copy_name(z, 0, "abc");\n'
                '    printf("%c\\n", z[0]);\n'
                '    printf("snprintf: %d\\n", src_count("snpr" "intf"));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Копируйте не больше cap − 1 байт и всегда ставьте dst[cap − 1] = 0; при cap == 0 ничего не '
              'делайте.',
      'expected': ['abcde 5', 'hi 2', 'q', 'snprintf: 0']},
     {'id': 'c4-geometry',
      'mode': 'c',
      'title': 'Структуры по значению: точки и векторы',
      'statement': 'struct point { double x, y; }. dist2(a, b) → квадрат расстояния; midpoint(a, b) → '
                   'середина; rotate90(p) → поворот на 90° против часовой стрелки вокруг начала координат; '
                   'cross(a, b, c) → векторное произведение (b − a) × (c − a); collinear(a, b, c) → 1, если '
                   'cross == 0. Всё принимается и возвращается по значению.',
      'starter': 'struct point { double x, y; };\n'
                 '\n'
                 'double dist2(struct point a, struct point b) { return 0; }\n'
                 'struct point midpoint(struct point a, struct point b) { return a; }\n'
                 'struct point rotate90(struct point p) { return p; }\n'
                 'double cross(struct point a, struct point b, struct point c) { return 0; }\n'
                 'int collinear(struct point a, struct point b, struct point c) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct point a = {0, 0}, b = {3, 4}, c = {6, 8}, d = {1, 5};\n'
                '    printf("%.1f %.1f\\n", dist2(a, b), dist2(b, b));\n'
                '    struct point m = midpoint(a, c);\n'
                '    printf("%.1f %.1f\\n", m.x, m.y);\n'
                '    struct point r = rotate90(b);\n'
                '    printf("%.1f %.1f\\n", r.x, r.y);\n'
                '    printf("%.1f %d %d\\n", cross(a, b, d), collinear(a, b, c), collinear(a, b, d));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Поворот на 90°: (x, y) → (−y, x). Структуру можно вернуть из функции, собрав её из значений.',
      'expected': ['25.0 0.0', '3.0 4.0', '-4.0 3.0', '11.0 1 0']},
     {'id': 'c4-rect',
      'mode': 'c',
      'title': 'Прямоугольники: пересечение и охватывающий',
      'statement': 'struct rect { int x, y, w, h; } (левый верхний угол и размеры, w, h ≥ 0). area(r), '
                   'contains(r, px, py) (границы: левая и верхняя включительно, правая и нижняя — нет), '
                   'intersect(a, b) → прямоугольник пересечения (w = h = 0, если пересечения нет) и '
                   'bounding(a, b) → наименьший охватывающий прямоугольник.',
      'starter': 'struct rect { int x, y, w, h; };\n'
                 '\n'
                 'int area(struct rect r) { return 0; }\n'
                 'int contains(struct rect r, int px, int py) { return 0; }\n'
                 'struct rect intersect(struct rect a, struct rect b) { return a; }\n'
                 'struct rect bounding(struct rect a, struct rect b) { return a; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'static void pr(struct rect r) { printf("(%d,%d %dx%d) ", r.x, r.y, r.w, r.h); }\n'
                '\n'
                'int main(void) {\n'
                '    struct rect a = {0, 0, 4, 3}, b = {2, 1, 5, 5}, c = {10, 10, 1, 1};\n'
                '    printf("%d %d %d\\n", area(a), area(b), area(c));\n'
                '    printf("%d %d %d %d\\n", contains(a, 0, 0), contains(a, 3, 2), contains(a, 4, 2), '
                'contains(a, 1, 3));\n'
                '    pr(intersect(a, b)); pr(intersect(a, c)); pr(bounding(a, b)); pr(bounding(a, c));\n'
                '    printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Пересечение: максимум левых и верхних границ, минимум правых и нижних; если правая граница не '
              'больше левой — пересечения нет.',
      'expected': ['12 25 1', '1 1 0 0', '(2,1 2x2) (0,0 0x0) (0,0 7x6) (0,0 11x11)']},
     {'id': 'c4-complex',
      'mode': 'c',
      'title': 'Комплексные числа',
      'statement': 'typedef struct { double re, im; } cx. cx_add, cx_mul, cx_conj, cx_abs2 (квадрат модуля), '
                   'cx_pow(c, n) → c в целой степени n ≥ 0 быстрым возведением (cx_pow(c, 0) = 1).',
      'starter': 'typedef struct { double re, im; } cx;\n'
                 '\n'
                 'cx cx_add(cx a, cx b) { return a; }\n'
                 'cx cx_mul(cx a, cx b) { return a; }\n'
                 'cx cx_conj(cx a) { return a; }\n'
                 'double cx_abs2(cx a) { return 0; }\n'
                 'cx cx_pow(cx c, unsigned n) { return c; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    cx a = {1, 2}, b = {3, -1};\n'
                '    cx s = cx_add(a, b), p = cx_mul(a, b), c = cx_conj(a);\n'
                '    printf("%.0f%+.0fi %.0f%+.0fi %.0f%+.0fi %.0f\\n", s.re, s.im, p.re, p.im, c.re, c.im, '
                'cx_abs2(a));\n'
                '    cx i = {0, 1};\n'
                '    cx i4 = cx_pow(i, 4), i3 = cx_pow(i, 3), z = cx_pow(a, 0);\n'
                '    printf("%.0f%+.0fi %.0f%+.0fi %.0f%+.0fi\\n", i4.re + 0.0, i4.im + 0.0, i3.re + 0.0, '
                'i3.im + 0.0, z.re + 0.0, z.im + 0.0);\n'
                '    cx big = cx_pow(a, 5);\n'
                '    printf("%.0f%+.0fi\\n", big.re, big.im);\n'
                '    return 0;\n'
                '}\n',
      'hint': '(a + bi)(c + di) = (ac − bd) + (ad + bc)i; степень — как powmod, но с умножением комплексных.',
      'expected': ['4+1i 5+5i 1-2i 5', '1+0i 0-1i 1+0i', '41-38i']},
     {'id': 'c4-fraction',
      'mode': 'c',
      'title': 'Рациональные числа',
      'statement': 'struct frac { long n, d; } (d > 0 после нормализации). frac_make(n, d) → сократить по '
                   'НОД и перенести знак в числитель (d ≠ 0); frac_add, frac_mul; frac_cmp(a, b) → −1/0/1 '
                   '(без деления: перекрёстным умножением); frac_to_double.',
      'starter': 'struct frac { long n, d; };\n'
                 '\n'
                 'struct frac frac_make(long n, long d) { struct frac f = {0, 1}; return f; }\n'
                 'struct frac frac_add(struct frac a, struct frac b) { return a; }\n'
                 'struct frac frac_mul(struct frac a, struct frac b) { return a; }\n'
                 'int frac_cmp(struct frac a, struct frac b) { return 0; }\n'
                 'double frac_to_double(struct frac a) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct frac a = frac_make(6, -8), b = frac_make(1, 3), z = frac_make(0, 5);\n'
                '    printf("%ld/%ld %ld/%ld %ld/%ld\\n", a.n, a.d, b.n, b.d, z.n, z.d);\n'
                '    struct frac s = frac_add(a, b), p = frac_mul(a, b);\n'
                '    printf("%ld/%ld %ld/%ld\\n", s.n, s.d, p.n, p.d);\n'
                '    printf("%d %d %d\\n", frac_cmp(a, b), frac_cmp(b, a), frac_cmp(frac_make(2, 6), b));\n'
                '    printf("%.4f\\n", frac_to_double(a));\n'
                '    struct frac h = {0, 1};\n'
                '    for (int i = 1; i <= 10; i++) h = frac_add(h, frac_make(1, i));\n'
                '    printf("%ld/%ld\\n", h.n, h.d);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'gcd вычисляйте по модулям; после сокращения знак живёт в числителе, а знаменатель '
              'положителен.',
      'expected': ['-3/4 1/3 0/1', '-5/12 -1/4', '-1 1 0', '-0.7500', '7381/2520']},
     {'id': 'c4-date',
      'mode': 'c',
      'title': 'Даты как структуры',
      'statement': 'struct date { int y, m, d; }. date_valid(d) → 1/0 (григорианский календарь, y ≥ 1); '
                   'date_cmp(a, b) → −1/0/1; days_from_civil(d) → число дней от 1970-01-01 (может быть '
                   'отрицательным); date_add(d, n) → дата через n дней (n может быть отрицательным); '
                   'weekday(d) → 0 = воскресенье … 6. Для 1970-01-01 — четверг.',
      'starter': 'struct date { int y, m, d; };\n'
                 '\n'
                 'int date_valid(struct date d) { return 0; }\n'
                 'int date_cmp(struct date a, struct date b) { return 0; }\n'
                 'long days_from_civil(struct date d) { return 0; }\n'
                 'struct date date_add(struct date d, long n) { return d; }\n'
                 'int weekday(struct date d) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'static void pd(struct date d) { printf("%04d-%02d-%02d ", d.y, d.m, d.d); }\n'
                '\n'
                'int main(void) {\n'
                '    struct date a = {2024, 2, 29}, b = {2023, 2, 29}, e = {1970, 1, 1};\n'
                '    printf("%d %d %d\\n", date_valid(a), date_valid(b), date_valid((struct date){2100, 2, '
                '29}));\n'
                '    printf("%d %d %d\\n", date_cmp(a, e), date_cmp(e, a), date_cmp(a, a));\n'
                '    printf("%ld %ld %ld\\n", days_from_civil(e), days_from_civil(a), '
                'days_from_civil((struct date){1969, 12, 31}));\n'
                '    pd(date_add(a, 1)); pd(date_add(a, 365)); pd(date_add(e, -1)); pd(date_add(a, -60)); '
                'pd(date_add(e, 20000));\n'
                '    printf("\\n%d %d %d\\n", weekday(e), weekday(a), weekday((struct date){2000, 1, 1}));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Используйте алгоритм days_from_civil: счёт дней от эпохи через «эры» по 400 лет и сдвиг года '
              'к марту.',
      'expected': ['1 0 0',
                   '1 -1 0',
                   '0 19782 -1',
                   '2024-03-01 2025-02-28 1969-12-31 2023-12-31 2024-10-04',
                   '4 4 6']},
     {'id': 'c4-students',
      'mode': 'c',
      'title': 'Массив структур: журнал оценок',
      'statement': 'struct student { char name[16]; int score[3]; }. average(const struct student *s) → '
                   'double; best(const struct student *a, size_t n) → индекс студента с наибольшим средним '
                   '(при равенстве — первый, n ≥ 1); rename(struct student *s, const char *name) — записать '
                   'имя с обрезанием до 15 символов; total_by_subject(const struct student *a, size_t n, int '
                   'subj) → сумма оценок по предмету.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct student { char name[16]; int score[3]; };\n'
                 '\n'
                 'double average(const struct student *s) { return 0; }\n'
                 'size_t best(const struct student *a, size_t n) { return 0; }\n'
                 'void rename_student(struct student *s, const char *name) {\n'
                 '}\n'
                 'int total_by_subject(const struct student *a, size_t n, int subj) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct student cls[3] = {{"Ann", {5, 4, 5}}, {"Bob", {5, 5, 5}}, {"Cat", {5, 5, 5}}};\n'
                '    printf("%.2f %.2f\\n", average(&cls[0]), average(&cls[1]));\n'
                '    printf("%zu %d %d %d\\n", best(cls, 3), total_by_subject(cls, 3, 0), '
                'total_by_subject(cls, 3, 1), total_by_subject(cls, 3, 2));\n'
                '    rename_student(&cls[0], "Alexandra-the-Very-Long");\n'
                '    printf("%s %zu\\n", cls[0].name, strlen(cls[0].name));\n'
                '    rename_student(&cls[1], "Bo");\n'
                '    printf("%s %zu\\n", cls[1].name, sizeof cls[1]);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'a[i].score[subj] — поле элемента массива; в rename_student копируйте не больше sizeof name − '
              '1 байт и ставьте нуль.',
      'expected': ['4.67 5.00', '1 15 14 15', 'Alexandra-the-V 15', 'Bo 28']},
     {'id': 'c4-layout',
      'mode': 'c',
      'title': 'Раскладка структур: размер и смещения',
      'statement': 'Измените порядок полей так, чтобы sizeof(struct small) стал 8 (поля: char a; int b; char '
                   'c), а sizeof(struct mixed) — 16 (char a; double d; short s; int i). Поля переименовывать '
                   'нельзя, набор тот же. Драйвер выведет размеры и смещения первых полей.',
      'starter': 'struct small {\n'
                 '    char a;\n'
                 '    int b;\n'
                 '    char c;\n'
                 '};\n'
                 '\n'
                 'struct mixed {\n'
                 '    char a;\n'
                 '    double d;\n'
                 '    short s;\n'
                 '    int i;\n'
                 '};\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                '#include <stddef.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%zu %zu\\n", sizeof(struct small), sizeof(struct mixed));\n'
                '    printf("%zu %zu %zu\\n", offsetof(struct small, b), offsetof(struct mixed, d), '
                'offsetof(struct mixed, i));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Расставляйте поля от крупных к мелким: double, затем int, short, char.',
      'expected': ['8 16', '0 0 8']},
     {'id': 'c4-rgb565',
      'mode': 'c',
      'title': 'Упаковка цвета в 16 бит',
      'statement': 'pack565(r, g, b) → uint16_t: старшие 5 бит красного, 6 бит зелёного и 5 бит синего '
                   '(значения 0..255 на входе) в формате rrrrrggg gggbbbbb. unpack565(c, *r, *g, *b): '
                   'восстановить 8-битные значения, дополнив младшие биты старшими (r = (r5 << 3) | (r5 >> '
                   '2) и т. д.).',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'uint16_t pack565(int r, int g, int b) { return 0; }\n'
                 'void unpack565(uint16_t c, int *r, int *g, int *b) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    int cols[][3] = {{255, 255, 255}, {0, 0, 0}, {255, 0, 0}, {0, 255, 0}, {0, 0, 255}, '
                '{200, 100, 50}};\n'
                '    for (int i = 0; i < 6; i++) {\n'
                '        uint16_t c = pack565(cols[i][0], cols[i][1], cols[i][2]);\n'
                '        int r, g, b;\n'
                '        unpack565(c, &r, &g, &b);\n'
                '        printf("%04x %d %d %d\\n", c, r, g, b);\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Маски: красный (c >> 11) & 31, зелёный (c >> 5) & 63, синий c & 31.',
      'expected': ['ffff 255 255 255',
                   '0000 0 0 0',
                   'f800 255 0 0',
                   '07e0 0 255 0',
                   '001f 0 0 255',
                   'cb26 206 101 49']},
     {'id': 'c4-float-bits',
      'mode': 'c',
      'title': 'Разбор float через union',
      'statement': 'union fbits { float f; uint32_t u; }. float_parts(float f, unsigned *sign, unsigned '
                   '*exp, unsigned *mant): записать знак (1 бит), порядок (8 бит) и мантиссу (23 бита). '
                   'float_from_parts(sign, exp, mant) → float. is_nan_bits(uint32_t u) → 1, если порядок 255 '
                   'и мантисса ≠ 0.',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'union fbits { float f; uint32_t u; };\n'
                 '\n'
                 'void float_parts(float f, unsigned *sign, unsigned *exp, unsigned *mant) {\n'
                 '}\n'
                 'float float_from_parts(unsigned sign, unsigned exp, unsigned mant) { return 0; }\n'
                 'int is_nan_bits(uint32_t u) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    float v[] = {1.0f, -2.5f, 0.1f, 0.0f, 1e-45f};\n'
                '    for (int i = 0; i < 5; i++) {\n'
                '        unsigned s, e, m;\n'
                '        float_parts(v[i], &s, &e, &m);\n'
                '        printf("%u %u %06x\\n", s, e, m);\n'
                '    }\n'
                '    printf("%.1f %.2f\\n", float_from_parts(0, 127, 0), float_from_parts(1, 128, '
                '0x200000));\n'
                '    printf("%d %d %d\\n", is_nan_bits(0x7FC00000u), is_nan_bits(0x7F800000u), '
                'is_nan_bits(0x3F800000u));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Запишите в одно поле union, прочитайте другое; порядок хранится со смещением 127.',
      'expected': ['0 127 000000',
                   '1 128 200000',
                   '0 123 4ccccd',
                   '0 0 000000',
                   '0 0 000001',
                   '1.0 -2.50',
                   '1 0 0']},
     {'id': 'c4-tagged-value',
      'mode': 'c',
      'title': 'Помеченное объединение: динамическое значение',
      'statement': 'struct value { enum { V_INT, V_DBL, V_STR } tag; union { long i; double d; const char '
                   '*s; } as; }. v_int, v_dbl, v_str — конструкторы. v_add(a, b): int+int → int, int+double '
                   'и double+double → double; со строкой — строка-результат отсутствует: вернуть v_int(0) '
                   '(ошибка). v_repr(v, buf, cap) → записать «42», «3.5» (%g) или «"text"» через snprintf.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct value { enum { V_INT, V_DBL, V_STR } tag; union { long i; double d; const char *s; '
                 '} as; };\n'
                 '\n'
                 'struct value v_int(long i) { struct value v = {V_INT, {0}}; return v; }\n'
                 'struct value v_dbl(double d) { struct value v = {V_INT, {0}}; return v; }\n'
                 'struct value v_str(const char *s) { struct value v = {V_INT, {0}}; return v; }\n'
                 'struct value v_add(struct value a, struct value b) { return a; }\n'
                 'void v_repr(struct value v, char *buf, size_t cap) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'static void show(struct value v) {\n'
                '    char b[32];\n'
                '    v_repr(v, b, sizeof b);\n'
                '    printf("%s ", b);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    show(v_int(42)); show(v_dbl(3.5)); show(v_str("hi"));\n'
                '    show(v_add(v_int(2), v_int(3))); show(v_add(v_int(2), v_dbl(0.5))); '
                'show(v_add(v_dbl(1.25), v_dbl(1.25)));\n'
                '    show(v_add(v_str("x"), v_int(1)));\n'
                '    printf("\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Каждая функция смотрит на tag и обращается к соответствующему полю union; при смешанных '
              'числах приводите int к double.',
      'expected': ['42 3.5 "hi" 5 2.5 2.5 0']},
     {'id': 'c4-flags',
      'mode': 'c',
      'title': 'Флаги из строки и обратно',
      'statement': 'enum { F_BOLD = 1, F_ITALIC = 2, F_UNDERLINE = 4, F_STRIKE = 8 }. parse_flags(const char '
                   '*csv) → unsigned: «bold,italic» → маска (неизвестные слова игнорировать, пробелы вокруг '
                   'слов допустимы). format_flags(unsigned m, char *out, size_t cap): слова через запятую в '
                   'порядке битов, пустая маска — «none».',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'enum { F_BOLD = 1, F_ITALIC = 2, F_UNDERLINE = 4, F_STRIKE = 8 };\n'
                 '\n'
                 'unsigned parse_flags(const char *csv) { return 0; }\n'
                 'void format_flags(unsigned m, char *out, size_t cap) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    char b[64];\n'
                '    const char *t[] = {"bold,italic", " strike , bold ", "", "blink,bold,bold", '
                '"underline,strike,italic,bold"};\n'
                '    for (int i = 0; i < 5; i++) {\n'
                '        unsigned m = parse_flags(t[i]);\n'
                '        format_flags(m, b, sizeof b);\n'
                '        printf("%u [%s]\\n", m, b);\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Слово сравнивайте с названиями по длине и содержимому; бит i соответствует i-му названию.',
      'expected': ['3 [bold,italic]',
                   '9 [bold,strike]',
                   '0 [none]',
                   '1 [bold]',
                   '15 [bold,italic,underline,strike]']},
     {'id': 'c4-serialize',
      'mode': 'c',
      'title': 'Сериализация в big-endian',
      'statement': 'struct header { uint8_t ver; uint16_t len; uint32_t id; } (в структуре заполнитель, а в '
                   'потоке 7 байт без него). put16(buf, v), put32(buf, v) пишут в big-endian, get16, get32 '
                   'читают. header_encode(const struct header *h, uint8_t *out) → 7; header_decode(const '
                   'uint8_t *in, struct header *h) → 7. Порядок полей: ver, len (BE), id (BE).',
      'starter': '#include <stdint.h>\n'
                 '\n'
                 'struct header { uint8_t ver; uint16_t len; uint32_t id; };\n'
                 '\n'
                 'void put16(uint8_t *b, uint16_t v) {}\n'
                 'void put32(uint8_t *b, uint32_t v) {}\n'
                 'uint16_t get16(const uint8_t *b) { return 0; }\n'
                 'uint32_t get32(const uint8_t *b) { return 0; }\n'
                 'int header_encode(const struct header *h, uint8_t *out) { return 0; }\n'
                 'int header_decode(const uint8_t *in, struct header *h) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct header h = {2, 0x1234, 0xCAFEBABE}, g;\n'
                '    uint8_t b[16];\n'
                '    memset(b, 0xEE, sizeof b);\n'
                '    int n = header_encode(&h, b);\n'
                '    printf("%d:", n);\n'
                '    for (int i = 0; i < 9; i++) printf(" %02x", b[i]);\n'
                '    printf("\\n");\n'
                '    memset(&g, 0, sizeof g);\n'
                '    n = header_decode(b, &g);\n'
                '    printf("%d %u %04x %08x sizeof=%zu\\n", n, g.ver, g.len, g.id, sizeof h);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Старший байт — первым: b[0] = v >> 24 и так далее; собирайте обратно сдвигами и «или».',
      'expected': ['7: 02 12 34 ca fe ba be ee ee', '7 2 1234 cafebabe sizeof=8']},
     {'id': 'c4-fix-compare',
      'mode': 'c',
      'title': 'Исправьте: сравнение структур через memcmp',
      'statement': 'same_item(a, b) должна сравнивать две структуры по полям. Заготовка использует memcmp и '
                   'ошибается, потому что в заполнителе между полями лежит разный мусор. Сравните поля по '
                   'отдельности.',
      'starter': '#include <string.h>\n'
                 '\n'
                 'struct item { char tag; int qty; char unit; };\n'
                 '\n'
                 'int same_item(const struct item *a, const struct item *b) {\n'
                 '    return memcmp(a, b, sizeof *a) == 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct item a, b;\n'
                '    memset(&a, 0xAA, sizeof a);\n'
                '    memset(&b, 0x55, sizeof b);\n'
                "    a.tag = b.tag = 'x'; a.qty = b.qty = 3; a.unit = b.unit = 'k';\n"
                '    printf("%d\\n", same_item(&a, &b));\n'
                '    b.qty = 4;\n'
                '    printf("%d\\n", same_item(&a, &b));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сравнивайте a->tag == b->tag && …; в заполнитель драйвер нарочно записал разные значения.',
      'expected': ['1', '0']}],
 5: [{'id': 'c5-dynarray',
      'mode': 'c',
      'title': 'Динамический массив',
      'statement': 'struct vec { int *data; size_t len, cap; }. vec_init(v) — пустой; vec_push(v, x) → 0/−1: '
                   'добавить в конец (ёмкость растёт вдвое, начальная — 4); vec_pop(v, *out) → 1/0; '
                   'vec_get(v, i, *out) → 1/0 (проверка границ); vec_free(v) — освободить буфер и обнулить '
                   'поля. Программа запускается с AddressSanitizer: утечка или выход за границы остановят '
                   'её.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct vec { int *data; size_t len, cap; };\n'
                 '\n'
                 'void vec_init(struct vec *v) {}\n'
                 'int vec_push(struct vec *v, int x) { return -1; }\n'
                 'int vec_pop(struct vec *v, int *out) { return 0; }\n'
                 'int vec_get(const struct vec *v, size_t i, int *out) { return 0; }\n'
                 'void vec_free(struct vec *v) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct vec v;\n'
                '    vec_init(&v);\n'
                '    for (int i = 0; i < 100; i++) vec_push(&v, i * i);\n'
                '    int x;\n'
                '    printf("%zu %zu\\n", v.len, v.cap);\n'
                '    printf("%d %d %d\\n", vec_get(&v, 99, &x), x, vec_get(&v, 100, &x));\n'
                '    int s = 0;\n'
                '    while (vec_pop(&v, &x)) s += x;\n'
                '    printf("%d %zu %d\\n", s, v.len, vec_pop(&v, &x));\n'
                '    vec_free(&v);\n'
                '    printf("%d %zu\\n", v.data == NULL, v.cap);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Перед записью проверьте len == cap; результат realloc кладите во временную переменную t.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['100 128', '1 9801 0', '328350 0 0', '1 0']},
     {'id': 'c5-vec-ops',
      'mode': 'c',
      'title': 'Вставка и удаление в середине вектора',
      'statement': 'struct vec как в прошлой задаче (готов). vec_insert(v, at, x) → 0/−1: вставить x на '
                   'позицию at ≤ len, сдвинув хвост (memmove). vec_erase(v, at) → 0/−1: удалить элемент at < '
                   'len. vec_reserve(v, n) → 0/−1: гарантировать ёмкость ≥ n. vec_shrink(v): уменьшить '
                   'ёмкость до len (для len = 0 — освободить буфер).',
      'starter': '#include <stddef.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <string.h>\n'
                 '\n'
                 'struct vec { int *data; size_t len, cap; };\n'
                 '\n'
                 'int vec_insert(struct vec *v, size_t at, int x) { return -1; }\n'
                 'int vec_erase(struct vec *v, size_t at) { return -1; }\n'
                 'int vec_reserve(struct vec *v, size_t n) { return -1; }\n'
                 'void vec_shrink(struct vec *v) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'static void show(const struct vec *v) {\n'
                '    for (size_t i = 0; i < v->len; i++) printf("%d ", v->data[i]);\n'
                '    printf("| %zu/%zu\\n", v->len, v->cap);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    struct vec v = {NULL, 0, 0};\n'
                '    for (int i = 1; i <= 5; i++) vec_insert(&v, v.len, i);\n'
                '    show(&v);\n'
                '    vec_insert(&v, 0, 100);\n'
                '    vec_insert(&v, 3, 200);\n'
                '    show(&v);\n'
                '    printf("%d %d\\n", vec_insert(&v, 99, 1), vec_erase(&v, 99));\n'
                '    vec_erase(&v, 0);\n'
                '    vec_erase(&v, v.len - 1);\n'
                '    show(&v);\n'
                '    vec_reserve(&v, 50);\n'
                '    show(&v);\n'
                '    vec_shrink(&v);\n'
                '    show(&v);\n'
                '    while (v.len) vec_erase(&v, 0);\n'
                '    vec_shrink(&v);\n'
                '    printf("%d %zu\\n", v.data == NULL, v.cap);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для вставки сдвиньте memmove(data + at + 1, data + at, (len - at) * sizeof *data); область '
              'пересекается, поэтому нужен memmove.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 2 3 4 5 | 5/8',
                   '100 1 2 200 3 4 5 | 7/8',
                   '-1 -1',
                   '1 2 200 3 4 | 5/8',
                   '1 2 200 3 4 | 5/50',
                   '1 2 200 3 4 | 5/5',
                   '1 0']},
     {'id': 'c5-str-alloc',
      'mode': 'c',
      'title': 'Строки в куче: dup, concat, repeat, join',
      'statement': 'my_strdup(s) → новая копия; concat(a, b) → новая строка a+b; repeat(s, n) → s '
                   'повторённая n раз (n = 0 — пустая строка); join(parts, n, sep) → строки через '
                   'разделитель. Все функции возвращают память из malloc (NULL при ошибке), освобождает '
                   'вызывающий. Запуск с AddressSanitizer.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'char *my_strdup(const char *s) { return NULL; }\n'
                 'char *concat(const char *a, const char *b) { return NULL; }\n'
                 'char *repeat(const char *s, size_t n) { return NULL; }\n'
                 'char *join(const char *const *parts, size_t n, const char *sep) { return NULL; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    char *a = my_strdup("hello");\n'
                '    char *b = concat(a, ", world");\n'
                '    char *c = repeat("ab", 3);\n'
                '    char *d = repeat("x", 0);\n'
                '    const char *parts[] = {"a", "bb", "ccc"};\n'
                '    char *e = join(parts, 3, "--");\n'
                '    char *f = join(parts, 0, "--");\n'
                '    printf("%s|%s|%s|%s|%s|%s\\n", a, b, c, d, e, f);\n'
                "    a[0] = 'J';\n"
                '    printf("%s\\n", b);\n'
                '    free(a); free(b); free(c); free(d); free(e); free(f);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Размер буфера — длина + 1 под завершающий нуль; для копирования используйте memcpy, зная '
              'длины.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['hello|hello, world|ababab||a--bb--ccc|', 'hello, world']},
     {'id': 'c5-fix-leak',
      'mode': 'c',
      'title': 'Исправьте: утечка на пути ошибки',
      'statement': 'make_pair(a, b) выделяет два буфера и возвращает 0, но при ошибке второго шага (когда b '
                   'пуста) возвращает −1 и забывает освободить первый. Исправьте так, чтобы при любом выходе '
                   'память не текла (проверяет LeakSanitizer). При успехе буферы отдаются в out1 и out2.',
      'starter': '#include <stdlib.h>\n'
                 '#include <string.h>\n'
                 '\n'
                 'int make_pair(const char *a, const char *b, char **out1, char **out2) {\n'
                 '    char *x = malloc(strlen(a) + 1);\n'
                 '    if (!x) return -1;\n'
                 '    strcpy(x, a);\n'
                 '    if (b[0] == 0) return -1;\n'
                 '    char *y = malloc(strlen(b) + 1);\n'
                 '    if (!y) return -1;\n'
                 '    strcpy(y, b);\n'
                 '    *out1 = x;\n'
                 '    *out2 = y;\n'
                 '    return 0;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    char *p, *q;\n'
                '    printf("%d\\n", make_pair("one", "two", &p, &q));\n'
                '    printf("%s %s\\n", p, q);\n'
                '    free(p); free(q);\n'
                '    printf("%d\\n", make_pair("one", "", &p, &q));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Освобождайте x на всех путях ошибки — удобно через общую метку goto fail в конце функции.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['0', 'one two', '-1']},
     {'id': 'c5-fix-double-free',
      'mode': 'c',
      'title': 'Исправьте: двойное освобождение',
      'statement': 'list_clear(head) освобождает список, но для последнего узла вызывает free дважды. '
                   'AddressSanitizer остановит программу. Исправьте цикл: каждый узел освобождается ровно '
                   'один раз, next читается до free.',
      'starter': '#include <stdlib.h>\n'
                 '\n'
                 'struct node { int v; struct node *next; };\n'
                 '\n'
                 'void list_clear(struct node *head) {\n'
                 '    struct node *p = head;\n'
                 '    while (p) {\n'
                 '        struct node *next = p->next;\n'
                 '        free(p);\n'
                 '        p = next;\n'
                 '    }\n'
                 '    free(p);\n'
                 '    if (head) free(head);\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct node *h = NULL;\n'
                '    for (int i = 0; i < 5; i++) {\n'
                '        struct node *n = malloc(sizeof *n);\n'
                '        n->v = i; n->next = h; h = n;\n'
                '    }\n'
                '    list_clear(h);\n'
                '    list_clear(NULL);\n'
                '    printf("ok\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'После цикла p уже NULL, а head освобождён внутри цикла: оба лишних free нужно убрать.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['ok']},
     {'id': 'c5-fix-uaf',
      'mode': 'c',
      'title': 'Исправьте: чтение после free',
      'statement': 'sum_and_free(head) должна вернуть сумму значений списка и освободить все узлы. Заготовка '
                   'читает p->next уже после free(p). Исправьте порядок действий.',
      'starter': '#include <stdlib.h>\n'
                 '\n'
                 'struct node { int v; struct node *next; };\n'
                 '\n'
                 'long sum_and_free(struct node *head) {\n'
                 '    long s = 0;\n'
                 '    for (struct node *p = head; p; p = p->next) {\n'
                 '        s += p->v;\n'
                 '        free(p);\n'
                 '    }\n'
                 '    return s;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct node *h = NULL;\n'
                '    for (int i = 1; i <= 10; i++) {\n'
                '        struct node *n = malloc(sizeof *n);\n'
                '        n->v = i; n->next = h; h = n;\n'
                '    }\n'
                '    printf("%ld %ld\\n", sum_and_free(h), sum_and_free(NULL));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сохраните p->next в локальной переменной до free(p).',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['55 0']},
     {'id': 'c5-fix-realloc-stale',
      'mode': 'c',
      'title': 'Исправьте: указатель после realloc',
      'statement': 'append_all(base, n, extra, m) расширяет массив и копирует extra в конец, но продолжает '
                   'использовать старый указатель после realloc (блок мог переехать). Исправьте функцию: она '
                   'возвращает новый указатель (NULL при ошибке — старый блок остаётся у вызывающего).',
      'starter': '#include <stdlib.h>\n'
                 '#include <string.h>\n'
                 '\n'
                 'int *append_all(int *base, size_t n, const int *extra, size_t m) {\n'
                 '    int *p = realloc(base, (n + m) * sizeof *base);\n'
                 '    if (!p) return NULL;\n'
                 '    memcpy(base + n, extra, m * sizeof *extra);\n'
                 '    return p;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int *a = malloc(3 * sizeof *a);\n'
                '    a[0] = 1; a[1] = 2; a[2] = 3;\n'
                '    int e[] = {4, 5, 6, 7};\n'
                '    a = append_all(a, 3, e, 4);\n'
                '    for (int i = 0; i < 7; i++) printf("%d ", a[i]);\n'
                '    printf("\\n");\n'
                '    free(a);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'После успешного realloc работайте только с новым указателем p: старый мог быть освобождён.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 2 3 4 5 6 7']},
     {'id': 'c5-list-basic',
      'mode': 'c',
      'title': 'Односвязный список: основы',
      'statement': 'struct node { int v; struct node *next; }. push_front(&head, x), push_back(&head, x), '
                   'pop_front(&head, *out) → 1/0, list_len(head), list_free(&head) — освободить и обнулить '
                   'голову. Возвращаемые 0/−1 при ошибке выделения для push_*.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct node { int v; struct node *next; };\n'
                 '\n'
                 'int push_front(struct node **head, int x) { return -1; }\n'
                 'int push_back(struct node **head, int x) { return -1; }\n'
                 'int pop_front(struct node **head, int *out) { return 0; }\n'
                 'size_t list_len(const struct node *head) { return 0; }\n'
                 'void list_free(struct node **head) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'static void show(const struct node *h) {\n'
                '    for (; h; h = h->next) printf("%d ", h->v);\n'
                '    printf("(%zu)\\n", list_len(h));\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    struct node *h = NULL;\n'
                '    push_back(&h, 1); push_back(&h, 2); push_front(&h, 0); push_back(&h, 3);\n'
                '    show(h);\n'
                '    int x;\n'
                '    printf("%d %d\\n", pop_front(&h, &x), x);\n'
                '    show(h);\n'
                '    list_free(&h);\n'
                '    printf("%d %d\\n", h == NULL, pop_front(&h, &x));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'push_back удобно писать через указатель на указатель: идите по &(*pp)->next, пока *pp не '
              'станет NULL.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['0 1 2 3 (0)', '1 0', '1 2 3 (0)', '1 0']},
     {'id': 'c5-list-reverse',
      'mode': 'c',
      'title': 'Разворот списка и поиск середины',
      'statement': 'list_reverse(head) → новая голова (узлы переставляются, не создаются). list_middle(head) '
                   '→ второй из двух средних узлов для чётной длины (NULL для пустого списка), за один '
                   'проход двумя указателями. nth_from_end(head, k) → узел k-й с конца (k = 1 — последний) '
                   'или NULL.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct node { int v; struct node *next; };\n'
                 '\n'
                 'struct node *list_reverse(struct node *head) { return head; }\n'
                 'struct node *list_middle(struct node *head) { return NULL; }\n'
                 'struct node *nth_from_end(struct node *head, size_t k) { return NULL; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'static struct node *build(int n) {\n'
                '    struct node *h = NULL;\n'
                '    for (int i = n; i >= 1; i--) {\n'
                '        struct node *x = malloc(sizeof *x);\n'
                '        x->v = i; x->next = h; h = x;\n'
                '    }\n'
                '    return h;\n'
                '}\n'
                '\n'
                'static void show_free(struct node *h) {\n'
                '    while (h) { printf("%d ", h->v); struct node *t = h; h = h->next; free(t); }\n'
                '    printf("\\n");\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    struct node *h = build(6);\n'
                '    printf("%d %d %d\\n", list_middle(h)->v, nth_from_end(h, 1)->v, nth_from_end(h, '
                '6)->v);\n'
                '    printf("%d\\n", nth_from_end(h, 7) == NULL);\n'
                '    h = list_reverse(h);\n'
                '    show_free(h);\n'
                '    struct node *o = build(5);\n'
                '    printf("%d\\n", list_middle(o)->v);\n'
                '    show_free(list_reverse(o));\n'
                '    printf("%d %d\\n", list_middle(NULL) == NULL, list_reverse(NULL) == NULL);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для середины — «быстрый» и «медленный» указатели; для k-го с конца — сначала уведите '
              '«ведущего» на k узлов вперёд.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['4 6 1', '1', '6 5 4 3 2 1', '3', '5 4 3 2 1', '1 1']},
     {'id': 'c5-list-cycle',
      'mode': 'c',
      'title': 'Цикл в списке: алгоритм Флойда',
      'statement': 'has_cycle(head) → 1/0 за O(n) времени и O(1) памяти (два указателя разной скорости). '
                   'cycle_start(head) → первый узел цикла или NULL. cycle_length(head) → длина цикла (0, '
                   'если его нет).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct node { int v; struct node *next; };\n'
                 '\n'
                 'int has_cycle(struct node *head) { return 0; }\n'
                 'struct node *cycle_start(struct node *head) { return NULL; }\n'
                 'int cycle_length(struct node *head) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    enum { N = 200000 };\n'
                '    struct node *a = malloc(N * sizeof *a);\n'
                '    for (int i = 0; i < N; i++) { a[i].v = i; a[i].next = i + 1 < N ? &a[i + 1] : NULL; }\n'
                '    printf("%d %d %d\\n", has_cycle(a), cycle_start(a) == NULL, cycle_length(a));\n'
                '    a[N - 1].next = &a[1234];\n'
                '    printf("%d %d %d\\n", has_cycle(a), cycle_start(a)->v, cycle_length(a));\n'
                '    a[N - 1].next = a;\n'
                '    printf("%d %d %d\\n", has_cycle(a), cycle_start(a)->v, cycle_length(a));\n'
                '    a[N - 1].next = &a[N - 1];\n'
                '    printf("%d %d %d\\n", has_cycle(a), cycle_start(a)->v, cycle_length(a));\n'
                '    printf("%d %d\\n", has_cycle(NULL), cycle_length(NULL));\n'
                '    free(a);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Когда медленный и быстрый указатели встретились, поставьте один на голову: двигая оба по '
              'одному шагу, они сойдутся в начале цикла.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['0 1 0', '1 1234 198766', '1 0 200000', '1 199999 1', '0 0']},
     {'id': 'c5-list-remove',
      'mode': 'c',
      'title': 'Удаление из списка через указатель на указатель',
      'statement': 'remove_all(&head, x) → сколько узлов с v == x удалено и освобождено; '
                   'remove_dups_sorted(head) — убрать повторы в отсортированном списке (освободить лишние '
                   'узлы); insert_sorted(&head, x) — вставить x, сохраняя порядок по возрастанию (перед '
                   'равными). Без особых случаев для головы.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct node { int v; struct node *next; };\n'
                 '\n'
                 'int remove_all(struct node **head, int x) { return 0; }\n'
                 'void remove_dups_sorted(struct node *head) {}\n'
                 'int insert_sorted(struct node **head, int x) { return -1; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'static void show_free(struct node *h) {\n'
                '    while (h) { printf("%d ", h->v); struct node *t = h; h = h->next; free(t); }\n'
                '    printf("\\n");\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    struct node *h = NULL;\n'
                '    int in[] = {5, 1, 3, 3, 9, 1, 5, 3};\n'
                '    for (int i = 0; i < 8; i++) insert_sorted(&h, in[i]);\n'
                '    for (struct node *p = h; p; p = p->next) printf("%d ", p->v);\n'
                '    printf("\\n");\n'
                '    remove_dups_sorted(h);\n'
                '    for (struct node *p = h; p; p = p->next) printf("%d ", p->v);\n'
                '    printf("\\n%d %d\\n", remove_all(&h, 1), remove_all(&h, 7));\n'
                '    printf("%d\\n", remove_all(&h, 9));\n'
                '    show_free(h);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'В remove_all указатель pp ходит по «слотам» (голова и поля next): при удалении слот '
              'переписывается, при пропуске — pp = &(*pp)->next.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 1 3 3 3 5 5 9', '1 3 5 9', '1 0', '1', '3 5']},
     {'id': 'c5-list-sort',
      'mode': 'c',
      'title': 'Сортировка слиянием списка',
      'statement': 'list_sort(head) → новая голова: отсортировать односвязный список по возрастанию за O(n '
                   'log n) (устойчиво), без выделения новых узлов — делением пополам (медленный/быстрый '
                   'указатели) и слиянием. Список из 200 000 узлов не должен обрабатываться «вставками за '
                   'O(n²)».',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct node { int v; struct node *next; };\n'
                 '\n'
                 'struct node *list_sort(struct node *head) { return head; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    enum { N = 200000 };\n'
                '    struct node *pool = malloc(N * sizeof *pool), *h = NULL;\n'
                '    unsigned s = 99;\n'
                '    for (int i = 0; i < N; i++) {\n'
                '        s = s * 1664525u + 1013904223u;\n'
                '        pool[i].v = (int)(s >> 20) % 5000;\n'
                '        pool[i].next = h;\n'
                '        h = &pool[i];\n'
                '    }\n'
                '    h = list_sort(h);\n'
                '    int ok = 1, n = 0;\n'
                '    for (struct node *p = h; p; p = p->next) {\n'
                '        n++;\n'
                '        if (p->next && p->v > p->next->v) ok = 0;\n'
                '    }\n'
                '    printf("%d %d %d %d\\n", ok, n, h->v, pool[0].v >= 0);\n'
                '    printf("%d\\n", list_sort(NULL) == NULL);\n'
                '    free(pool);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Разделите список на две половины, рекурсивно отсортируйте каждую, затем слейте с фиктивным '
              'узлом dummy в начале результата.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 200000 0 1', '1']},
     {'id': 'c5-dlist',
      'mode': 'c',
      'title': 'Двусвязный список с сигнальным узлом',
      'statement': 'struct dnode { int v; struct dnode *prev, *next; }; список — кольцо с сигнальным узлом '
                   '(head.prev/next указывают на себя, если пуст). dl_init(h), dl_push_front(h, x), '
                   'dl_push_back(h, x) → 0/−1, dl_remove(n) — вырезать узел и освободить, dl_pop_front(h, '
                   '*out) → 1/0, dl_move_to_front(h, n), dl_free(h) — освободить все узлы.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct dnode { int v; struct dnode *prev, *next; };\n'
                 '\n'
                 'void dl_init(struct dnode *h) {}\n'
                 'int dl_push_front(struct dnode *h, int x) { return -1; }\n'
                 'int dl_push_back(struct dnode *h, int x) { return -1; }\n'
                 'void dl_remove(struct dnode *n) {}\n'
                 'int dl_pop_front(struct dnode *h, int *out) { return 0; }\n'
                 'void dl_move_to_front(struct dnode *h, struct dnode *n) {}\n'
                 'void dl_free(struct dnode *h) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'static void show(struct dnode *h) {\n'
                '    for (struct dnode *p = h->next; p != h; p = p->next) printf("%d ", p->v);\n'
                '    printf("| ");\n'
                '    for (struct dnode *p = h->prev; p != h; p = p->prev) printf("%d ", p->v);\n'
                '    printf("\\n");\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    struct dnode h;\n'
                '    dl_init(&h);\n'
                '    for (int i = 1; i <= 4; i++) dl_push_back(&h, i);\n'
                '    dl_push_front(&h, 0);\n'
                '    show(&h);\n'
                '    struct dnode *three = h.next->next->next->next;\n'
                '    dl_move_to_front(&h, three);\n'
                '    show(&h);\n'
                '    dl_remove(h.next->next);\n'
                '    int x;\n'
                '    printf("%d %d\\n", dl_pop_front(&h, &x), x);\n'
                '    show(&h);\n'
                '    dl_free(&h);\n'
                '    printf("%d %d\\n", h.next == &h && h.prev == &h, dl_pop_front(&h, &x));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сигнальный узел убирает все проверки на NULL: вставка и удаление — одни и те же четыре '
              'присваивания в любом месте.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['0 1 2 3 4 | 4 3 2 1 0', '3 0 1 2 4 | 4 2 1 0 3', '1 3', '1 2 4 | 4 2 1', '1 0']},
     {'id': 'c5-lru',
      'mode': 'c',
      'title': 'Кэш LRU на двусвязном списке',
      'statement': 'Кэш из cap пар (ключ, значение). lru_new(cap), lru_get(c, key, *out) → 1/0 (попадание '
                   'делает запись самой свежей), lru_put(c, key, value) (при переполнении выбрасывается '
                   'самая давняя), lru_size(c), lru_free(c). Допустим линейный поиск по списку; свежие — в '
                   'начале. Выделяйте записи через malloc, освобождайте всё в lru_free.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct lru;\n'
                 '\n'
                 'struct lru *lru_new(size_t cap) { return 0; }\n'
                 'int lru_get(struct lru *c, int key, int *out) { return 0; }\n'
                 'void lru_put(struct lru *c, int key, int value) {}\n'
                 'size_t lru_size(const struct lru *c) { return 0; }\n'
                 'void lru_free(struct lru *c) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct lru *c = lru_new(3);\n'
                '    int v;\n'
                '    lru_put(c, 1, 10); lru_put(c, 2, 20); lru_put(c, 3, 30);\n'
                '    printf("%d %d\\n", lru_get(c, 1, &v), v);\n'
                '    lru_put(c, 4, 40);\n'
                '    printf("%d %d %d\\n", lru_get(c, 2, &v), lru_get(c, 3, &v), lru_get(c, 4, &v));\n'
                '    lru_put(c, 1, 11);\n'
                '    lru_put(c, 5, 50);\n'
                '    printf("%d %d %d %zu\\n", lru_get(c, 1, &v), v, lru_get(c, 3, &v), lru_size(c));\n'
                '    lru_free(c);\n'
                '    struct lru *z = lru_new(0);\n'
                '    lru_put(z, 1, 1);\n'
                '    printf("%zu\\n", lru_size(z));\n'
                '    lru_free(z);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Список от свежих к давним: при обращении запись переносится в начало, при переполнении '
              'удаляется последняя.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 10', '0 1 1', '1 11 0 3', '0']},
     {'id': 'c5-stack-balance',
      'mode': 'c',
      'title': 'Стек: скобки и обратная польская запись',
      'statement': 'Динамический стек символов уже не нужен — используйте свой массив/список. balanced(const '
                   'char *s) → 1/0: скобки (), [], {} расставлены правильно (прочие символы игнорируются). '
                   'eval_rpn(const char *s, long *out) → 1/0: выражение из чисел и + − * / через пробелы '
                   '(стек значений в куче); 0 при ошибке (мало операндов, деление на ноль, лишние числа, '
                   'неизвестный токен).',
      'starter': 'int balanced(const char *s) { return 0; }\n'
                 'int eval_rpn(const char *s, long *out) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    const char *b[] = {"", "([]{})", "(]", "((", "a(b)c[d]{e}", "}{", "([)]"};\n'
                '    for (int i = 0; i < 7; i++) printf("%d", balanced(b[i]));\n'
                '    printf("\\n");\n'
                '    const char *e[] = {"3 4 + 2 *", "5 1 2 + 4 * + 3 -", "1 +", "4 0 /", "1 2", "2 x +", '
                '"-3 4 *", ""};\n'
                '    for (int i = 0; i < 8; i++) {\n'
                '        long v = 0;\n'
                '        int r = eval_rpn(e[i], &v);\n'
                '        printf("%d %ld\\n", r, r ? v : 0L);\n'
                '    }\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для скобок кладите открывающие в стек и сверяйте с закрывающими; в конце стек должен быть '
              'пуст.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1100100', '1 14', '1 14', '0 0', '0 0', '0 0', '0 0', '1 -12', '0 0']},
     {'id': 'c5-ring',
      'mode': 'c',
      'title': 'Кольцевой буфер очереди',
      'statement': 'struct ring { int *buf; size_t cap, head, count; }. ring_init(r, cap) → 0/−1 (буфер из '
                   'malloc), ring_push(r, x) → 1 / 0 если полон, ring_pop(r, *out) → 1/0 если пуст, '
                   'ring_peek, ring_free. Индексы заворачиваются по модулю cap; счётчик count различает '
                   'пустой и полный.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct ring { int *buf; size_t cap, head, count; };\n'
                 '\n'
                 'int ring_init(struct ring *r, size_t cap) { return -1; }\n'
                 'int ring_push(struct ring *r, int x) { return 0; }\n'
                 'int ring_pop(struct ring *r, int *out) { return 0; }\n'
                 'int ring_peek(const struct ring *r, int *out) { return 0; }\n'
                 'void ring_free(struct ring *r) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct ring r;\n'
                '    ring_init(&r, 4);\n'
                '    int x;\n'
                '    for (int i = 1; i <= 5; i++) printf("%d", ring_push(&r, i));\n'
                '    printf("\\n%d %d\\n", ring_pop(&r, &x), x);\n'
                '    printf("%d %d\\n", ring_pop(&r, &x), x);\n'
                '    printf("%d %d\\n", ring_push(&r, 10), ring_push(&r, 11));\n'
                '    printf("%d %d %zu\\n", ring_peek(&r, &x), x, r.head);\n'
                '    while (ring_pop(&r, &x)) printf("%d ", x);\n'
                '    printf("\\n%d\\n", ring_pop(&r, &x));\n'
                '    for (int i = 0; i < 1000; i++) { ring_push(&r, i); ring_pop(&r, &x); }\n'
                '    printf("%zu %d\\n", r.head, x);\n'
                '    ring_free(&r);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Позиция записи — (head + count) % cap; чтение — head, затем head = (head + 1) % cap.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['11110', '1 1', '1 2', '1 1', '1 3 2', '3 4 10 11', '0', '2 999']},
     {'id': 'c5-two-stack-queue',
      'mode': 'c',
      'title': 'Очередь из двух стеков',
      'statement': 'struct queue { int *in, *out; size_t nin, nout, cap; } — два динамических стека. '
                   'q_init(q), q_push(q, x) → 0/−1 (кладёт во входной), q_pop(q, *out) → 1/0 (если выходной '
                   'пуст — переложить всё из входного, обратив порядок), q_len(q), q_free(q). Каждый элемент '
                   'перекладывается не более одного раза: миллион операций должен выполняться быстро.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct queue { int *in, *out; size_t nin, nout, cap; };\n'
                 '\n'
                 'void q_init(struct queue *q) {}\n'
                 'int q_push(struct queue *q, int x) { return -1; }\n'
                 'int q_pop(struct queue *q, int *out) { return 0; }\n'
                 'size_t q_len(const struct queue *q) { return 0; }\n'
                 'void q_free(struct queue *q) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct queue q;\n'
                '    q_init(&q);\n'
                '    int x;\n'
                '    for (int i = 1; i <= 3; i++) q_push(&q, i);\n'
                '    printf("%d %d\\n", q_pop(&q, &x), x);\n'
                '    q_push(&q, 4);\n'
                '    printf("%zu\\n", q_len(&q));\n'
                '    while (q_pop(&q, &x)) printf("%d ", x);\n'
                '    printf("\\n%d\\n", q_pop(&q, &x));\n'
                '    long long s = 0;\n'
                '    for (int i = 0; i < 1000000; i++) { q_push(&q, i); if (i % 3 == 2) { q_pop(&q, &x); s '
                '+= x; } }\n'
                '    while (q_pop(&q, &x)) s += x;\n'
                '    printf("%lld\\n", s);\n'
                '    q_free(&q);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Выходной стек хранит элементы в «обратном» порядке; перекладывайте входной в выходной только '
              'когда выходной пуст.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 1', '3', '2 3 4', '0', '499999500000']},
     {'id': 'c5-bst-basic',
      'mode': 'c',
      'title': 'Дерево поиска: вставка, поиск, высота',
      'statement': 'struct tnode { int key; struct tnode *l, *r; }. bst_insert(&root, key) → 1 если '
                   'добавлен, 0 если ключ уже есть (повторы не хранятся), −1 при ошибке памяти; '
                   'bst_find(root, key) → узел или NULL; bst_height(root) → высота (пустое — 0, один узел — '
                   '1); bst_size(root); bst_min/bst_max(root) → узел или NULL; bst_free(root) — освободить '
                   'все узлы без рекурсии глубиной по числу узлов не требуется.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct tnode { int key; struct tnode *l, *r; };\n'
                 '\n'
                 'int bst_insert(struct tnode **root, int key) { return -1; }\n'
                 'struct tnode *bst_find(struct tnode *root, int key) { return NULL; }\n'
                 'int bst_height(const struct tnode *root) { return 0; }\n'
                 'size_t bst_size(const struct tnode *root) { return 0; }\n'
                 'struct tnode *bst_min(struct tnode *root) { return NULL; }\n'
                 'struct tnode *bst_max(struct tnode *root) { return NULL; }\n'
                 'void bst_free(struct tnode *root) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct tnode *t = NULL;\n'
                '    int k[] = {8, 3, 10, 1, 6, 14, 4, 7, 13, 6, 8};\n'
                '    int added = 0;\n'
                '    for (int i = 0; i < 11; i++) added += bst_insert(&t, k[i]) == 1;\n'
                '    printf("%d %zu %d\\n", added, bst_size(t), bst_height(t));\n'
                '    printf("%d %d %d %d\\n", bst_find(t, 7) != NULL, bst_find(t, 5) == NULL, '
                'bst_min(t)->key, bst_max(t)->key);\n'
                '    bst_free(t);\n'
                '    struct tnode *deg = NULL;\n'
                '    for (int i = 0; i < 1500; i++) bst_insert(&deg, i);\n'
                '    printf("%zu %d %d\\n", bst_size(deg), bst_height(deg), bst_max(deg)->key);\n'
                '    bst_free(deg);\n'
                '    printf("%d %d\\n", bst_height(NULL), bst_min(NULL) == NULL);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Вставку удобно писать через указатель на указатель: идти вниз, пока слот не станет NULL, и '
              'записать в него новый узел.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['9 9 4', '1 1 1 14', '1500 1500 1499', '0 1']},
     {'id': 'c5-bst-walk',
      'mode': 'c',
      'title': 'Обходы дерева: in/pre/post-order и по уровням',
      'statement': 'Дерево строится драйвером. inorder(root, out) → n записанных ключей (по возрастанию); '
                   'preorder и postorder — аналогично; levelorder(root, out) — по уровням слева направо '
                   '(используйте очередь на массиве указателей). Все четыре заполняют массив out достаточной '
                   'длины и возвращают число ключей.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct tnode { int key; struct tnode *l, *r; };\n'
                 '\n'
                 'size_t inorder(const struct tnode *t, int *out) { return 0; }\n'
                 'size_t preorder(const struct tnode *t, int *out) { return 0; }\n'
                 'size_t postorder(const struct tnode *t, int *out) { return 0; }\n'
                 'size_t levelorder(const struct tnode *t, int *out) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'static struct tnode *ins(struct tnode *t, int k) {\n'
                '    if (!t) { t = calloc(1, sizeof *t); t->key = k; return t; }\n'
                '    if (k < t->key) t->l = ins(t->l, k); else t->r = ins(t->r, k);\n'
                '    return t;\n'
                '}\n'
                '\n'
                'static void fr(struct tnode *t) { if (t) { fr(t->l); fr(t->r); free(t); } }\n'
                '\n'
                'static void pr(size_t n, const int *a) { for (size_t i = 0; i < n; i++) printf("%d ", '
                'a[i]); printf("\\n"); }\n'
                '\n'
                'int main(void) {\n'
                '    struct tnode *t = NULL;\n'
                '    int k[] = {8, 3, 10, 1, 6, 14, 4, 7, 13};\n'
                '    for (int i = 0; i < 9; i++) t = ins(t, k[i]);\n'
                '    int out[16];\n'
                '    pr(inorder(t, out), out);\n'
                '    pr(preorder(t, out), out);\n'
                '    pr(postorder(t, out), out);\n'
                '    pr(levelorder(t, out), out);\n'
                '    fr(t);\n'
                '    printf("%zu %zu\\n", inorder(NULL, out), levelorder(NULL, out));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для обхода по уровням: очередь указателей, читаем узел с головы и добавляем его потомков в '
              'хвост.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 3 4 6 7 8 10 13 14',
                   '8 3 1 6 4 7 10 14 13',
                   '1 4 7 6 3 13 14 10 8',
                   '8 3 10 1 6 14 4 7 13',
                   '0 0']},
     {'id': 'c5-bst-delete',
      'mode': 'c',
      'title': 'Удаление из дерева поиска',
      'statement': 'bst_delete(&root, key) → 1, если ключ найден и узел удалён (три случая: нет детей, один '
                   'ребёнок, два — заменить ключ минимумом правого поддерева и удалить его), иначе 0. '
                   'is_bst(root) → 1, если для каждого узла все левые ключи меньше, все правые больше '
                   '(проверка границ). Память освобождается корректно (запуск с AddressSanitizer).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct tnode { int key; struct tnode *l, *r; };\n'
                 '\n'
                 'int bst_delete(struct tnode **root, int key) { return 0; }\n'
                 'int is_bst(const struct tnode *root) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'static struct tnode *ins(struct tnode *t, int k) {\n'
                '    if (!t) { t = calloc(1, sizeof *t); t->key = k; return t; }\n'
                '    if (k < t->key) t->l = ins(t->l, k); else t->r = ins(t->r, k);\n'
                '    return t;\n'
                '}\n'
                '\n'
                'static void walk(const struct tnode *t) { if (t) { walk(t->l); printf("%d ", t->key); '
                'walk(t->r); } }\n'
                'static void fr(struct tnode *t) { if (t) { fr(t->l); fr(t->r); free(t); } }\n'
                '\n'
                'int main(void) {\n'
                '    struct tnode *t = NULL;\n'
                '    int k[] = {8, 3, 10, 1, 6, 14, 4, 7, 13};\n'
                '    for (int i = 0; i < 9; i++) t = ins(t, k[i]);\n'
                '    int del[] = {1, 14, 3, 8, 99, 10};\n'
                '    for (int i = 0; i < 6; i++) {\n'
                '        printf("%d:%d ", del[i], bst_delete(&t, del[i]));\n'
                '        printf("[");\n'
                '        walk(t);\n'
                '        printf("] %d\\n", is_bst(t));\n'
                '    }\n'
                '    fr(t);\n'
                '    struct tnode bad = {5, NULL, NULL}, l = {7, NULL, NULL};\n'
                '    bad.l = &l;\n'
                '    printf("%d\\n", is_bst(&bad));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для узла с двумя детьми найдите минимум правого поддерева, скопируйте его ключ в узел и '
              'удалите минимум (у него нет левого ребёнка).',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1:1 [3 4 6 7 8 10 13 14 ] 1',
                   '14:1 [3 4 6 7 8 10 13 ] 1',
                   '3:1 [4 6 7 8 10 13 ] 1',
                   '8:1 [4 6 7 10 13 ] 1',
                   '99:0 [4 6 7 10 13 ] 1',
                   '10:1 [4 6 7 13 ] 1',
                   '0']},
     {'id': 'c5-heap',
      'mode': 'c',
      'title': 'Двоичная куча на массиве',
      'statement': 'struct heap { int *a; size_t len, cap; } — минимум в корне. heap_init, heap_push(h, x) → '
                   '0/−1 (sift-up), heap_pop(h, *out) → 1/0 (sift-down), heap_peek, heap_free. heap_sort(int '
                   '*a, size_t n) — отсортировать массив по возрастанию через кучу (500 000 элементов должны '
                   'сортироваться быстро).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct heap { int *a; size_t len, cap; };\n'
                 '\n'
                 'void heap_init(struct heap *h) {}\n'
                 'int heap_push(struct heap *h, int x) { return -1; }\n'
                 'int heap_pop(struct heap *h, int *out) { return 0; }\n'
                 'int heap_peek(const struct heap *h, int *out) { return 0; }\n'
                 'void heap_free(struct heap *h) {}\n'
                 'void heap_sort(int *a, size_t n) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct heap h;\n'
                '    heap_init(&h);\n'
                '    int in[] = {5, 3, 8, 1, 9, 2, 7};\n'
                '    for (int i = 0; i < 7; i++) heap_push(&h, in[i]);\n'
                '    int x;\n'
                '    printf("%d %d\\n", heap_peek(&h, &x), x);\n'
                '    while (heap_pop(&h, &x)) printf("%d ", x);\n'
                '    printf("\\n%d\\n", heap_pop(&h, &x));\n'
                '    heap_free(&h);\n'
                '    size_t n = 500000;\n'
                '    int *a = malloc(n * sizeof *a);\n'
                '    unsigned s = 5;\n'
                '    for (size_t i = 0; i < n; i++) { s = s * 1664525u + 1013904223u; a[i] = (int)(s >> 8); '
                '}\n'
                '    heap_sort(a, n);\n'
                '    int ok = 1;\n'
                '    for (size_t i = 1; i < n; i++) if (a[i - 1] > a[i]) ok = 0;\n'
                '    printf("%d\\n", ok);\n'
                '    free(a);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Родитель элемента i — (i − 1) / 2, дети — 2i + 1 и 2i + 2. При pop последний элемент ставится '
              'в корень и «просеивается» вниз.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 1', '1 2 3 5 7 8 9', '0', '1']},
     {'id': 'c5-hash-table',
      'mode': 'c',
      'title': 'Хеш-таблица строка → число',
      'statement': 'struct ht — таблица с цепочками (корзины — односвязные списки), ключи — копии строк '
                   '(malloc). ht_new() → таблица (начально 8 корзин), ht_put(t, key, val) → 1 новый ключ / 0 '
                   'обновление / −1 ошибка, ht_get(t, key, *out) → 1/0, ht_del(t, key) → 1/0, ht_count(t), '
                   'ht_free(t). Когда записей больше, чем 3/4 числа корзин, таблица удваивается и записи '
                   'переразмещаются. Хеш — FNV-1a (32 бита). 200 000 вставок должны выполняться быстро.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct ht;\n'
                 '\n'
                 'struct ht *ht_new(void) { return 0; }\n'
                 'int ht_put(struct ht *t, const char *key, int val) { return -1; }\n'
                 'int ht_get(const struct ht *t, const char *key, int *out) { return 0; }\n'
                 'int ht_del(struct ht *t, const char *key) { return 0; }\n'
                 'size_t ht_count(const struct ht *t) { return 0; }\n'
                 'void ht_free(struct ht *t) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct ht *t = ht_new();\n'
                '    int v;\n'
                '    printf("%d %d %d\\n", ht_put(t, "one", 1), ht_put(t, "two", 2), ht_put(t, "one", 11));\n'
                '    printf("%d %d %d %zu\\n", ht_get(t, "one", &v), v, ht_get(t, "three", &v), '
                'ht_count(t));\n'
                '    printf("%d %d %zu\\n", ht_del(t, "two"), ht_del(t, "two"), ht_count(t));\n'
                '    char key[32];\n'
                '    for (int i = 0; i < 200000; i++) { snprintf(key, sizeof key, "key-%d", i); ht_put(t, '
                'key, i); }\n'
                '    long long sum = 0;\n'
                '    for (int i = 0; i < 200000; i += 7) { snprintf(key, sizeof key, "key-%d", i); if '
                '(ht_get(t, key, &v)) sum += v; }\n'
                '    printf("%zu %lld\\n", ht_count(t), sum);\n'
                '    for (int i = 0; i < 200000; i += 2) { snprintf(key, sizeof key, "key-%d", i); ht_del(t, '
                'key); }\n'
                '    printf("%zu %d\\n", ht_count(t), ht_get(t, "key-4", &v));\n'
                '    ht_free(t);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'При высокой загрузке создайте массив вдвое больше и переместите узлы цепочек (не копируйте '
              'строки). Освобождайте и ключ, и запись.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 1 0', '1 11 0 2', '1 0 1', '200001 2857157142', '100001 0']},
     {'id': 'c5-word-freq',
      'mode': 'c',
      'title': 'Частоты слов на хеш-таблице',
      'statement': 'word_freq(text) использует собственную хеш-таблицу (достаточно таблицы фиксированного '
                   'размера на 4096 корзин с цепочками): слова — последовательности ASCII-букв без учёта '
                   'регистра. Функции: wf_new(), wf_add(wf, text) — учесть все слова текста, wf_count(wf, '
                   'word) → число вхождений, wf_unique(wf), wf_top(wf, k, out_words, out_counts) → записать '
                   'k самых частых (при равенстве — по алфавиту), wf_free(wf).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct wf;\n'
                 '\n'
                 'struct wf *wf_new(void) { return 0; }\n'
                 'void wf_add(struct wf *w, const char *text) {}\n'
                 'int wf_count(const struct wf *w, const char *word) { return 0; }\n'
                 'size_t wf_unique(const struct wf *w) { return 0; }\n'
                 'size_t wf_top(const struct wf *w, size_t k, const char **words, int *counts) { return 0; '
                 '}\n'
                 'void wf_free(struct wf *w) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct wf *w = wf_new();\n'
                '    wf_add(w, "The quick brown fox. The lazy dog; the FOX jumps over the lazy dog!");\n'
                '    wf_add(w, "A fox, a dog, and the end");\n'
                '    printf("%d %d %d %d %zu\\n", wf_count(w, "the"), wf_count(w, "FOX"), wf_count(w, '
                '"cat"), wf_count(w, "a"), wf_unique(w));\n'
                '    const char *words[4];\n'
                '    int counts[4];\n'
                '    size_t n = wf_top(w, 4, words, counts);\n'
                '    for (size_t i = 0; i < n; i++) printf("%s:%d ", words[i], counts[i]);\n'
                '    printf("\\n");\n'
                '    wf_free(w);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Хешируйте слово в нижнем регистре; при добавлении проверяйте цепочку корзины на уже '
              'существующее слово.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['5 3 0 2 11', 'the:5 dog:3 fox:3 a:2']},
     {'id': 'c5-arena',
      'mode': 'c',
      'title': 'Арена: выделение сдвигом указателя',
      'statement': 'struct arena { unsigned char *base; size_t cap, used; }. arena_init(a, buf, cap) — арена '
                   'поверх чужого буфера. arena_alloc(a, n, align) → указатель, выровненный по align '
                   '(степень двойки), или NULL, если места нет; arena_reset(a) — освободить всё разом; '
                   'arena_used(a). Выделения идут подряд с минимальным заполнителем для выравнивания.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct arena { unsigned char *base; size_t cap, used; };\n'
                 '\n'
                 'void arena_init(struct arena *a, void *buf, size_t cap) {}\n'
                 'void *arena_alloc(struct arena *a, size_t n, size_t align) { return NULL; }\n'
                 'void arena_reset(struct arena *a) {}\n'
                 'size_t arena_used(const struct arena *a) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    static _Alignas(16) unsigned char buf[256];\n'
                '    struct arena a;\n'
                '    arena_init(&a, buf, sizeof buf);\n'
                '    char *c = arena_alloc(&a, 1, 1);\n'
                '    int *i = arena_alloc(&a, 4, 4);\n'
                '    double *d = arena_alloc(&a, 8, 8);\n'
                '    void *z = arena_alloc(&a, 16, 16);\n'
                '    printf("%d %d %d %d\\n", c == (char *)buf, (uintptr_t)i % 4 == 0, (uintptr_t)d % 8 == '
                '0, (uintptr_t)z % 16 == 0);\n'
                '    printf("%zu %td %td\\n", arena_used(&a), (unsigned char *)i - buf, (unsigned char *)d - '
                'buf);\n'
                '    printf("%d\\n", arena_alloc(&a, 1000, 1) == NULL);\n'
                '    printf("%d %zu\\n", arena_alloc(&a, 256 - arena_used(&a), 1) != NULL, arena_used(&a));\n'
                '    printf("%d\\n", arena_alloc(&a, 1, 1) == NULL);\n'
                '    arena_reset(&a);\n'
                '    printf("%zu %d\\n", arena_used(&a), arena_alloc(&a, 256, 1) == (void *)buf);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Выровняйте адрес: aligned = (cur + align − 1) & ~(align − 1); место проверяйте без '
              'переполнения size_t.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 1 1 1', '32 4 8', '1', '1 256', '1', '0 1']},
     {'id': 'c5-pool',
      'mode': 'c',
      'title': 'Пул блоков одного размера',
      'statement': 'struct pool { void *mem; size_t blk, n; void *free_list; }. pool_init(p, mem, blk, n) — '
                   'разбить mem (n блоков по blk ≥ sizeof(void *) байт, выровнены) на список свободных; '
                   'pool_get(p) → блок или NULL; pool_put(p, blk) — вернуть блок; pool_free_count(p) → '
                   'сколько блоков свободно. Список свободных хранится внутри самих блоков.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct pool { void *mem; size_t blk, n; void *free_list; };\n'
                 '\n'
                 'void pool_init(struct pool *p, void *mem, size_t blk, size_t n) {}\n'
                 'void *pool_get(struct pool *p) { return NULL; }\n'
                 'void pool_put(struct pool *p, void *b) {}\n'
                 'size_t pool_free_count(const struct pool *p) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    static _Alignas(16) unsigned char mem[10 * 32];\n'
                '    struct pool p;\n'
                '    pool_init(&p, mem, 32, 10);\n'
                '    void *b[10];\n'
                '    for (int i = 0; i < 10; i++) b[i] = pool_get(&p);\n'
                '    printf("%zu %d\\n", pool_free_count(&p), pool_get(&p) == NULL);\n'
                '    int distinct = 1;\n'
                '    for (int i = 0; i < 10; i++) {\n'
                '        if ((unsigned char *)b[i] < mem || (unsigned char *)b[i] >= mem + sizeof mem) '
                'distinct = 0;\n'
                '        for (int j = 0; j < i; j++) if (b[i] == b[j]) distinct = 0;\n'
                '    }\n'
                '    printf("%d\\n", distinct);\n'
                '    pool_put(&p, b[3]);\n'
                '    pool_put(&p, b[7]);\n'
                '    printf("%zu %d\\n", pool_free_count(&p), pool_get(&p) == b[7]);\n'
                '    for (int r = 0; r < 100000; r++) { void *x = pool_get(&p); pool_put(&p, x); }\n'
                '    printf("%zu\\n", pool_free_count(&p));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Свободный блок хранит в первых байтах указатель на следующий свободный: pool_get снимает '
              'голову списка, pool_put ставит блок в голову.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['0 1', '1', '2 1', '1']},
     {'id': 'c5-generic-vec',
      'mode': 'c',
      'title': 'Универсальный вектор на void *',
      'statement': 'struct gvec { void *data; size_t elem, len, cap; }. gv_init(v, elem_size), gv_push(v, '
                   'const void *x) → 0/−1 (копирует elem байт), gv_at(v, i) → указатель на элемент или NULL, '
                   'gv_pop(v, void *out) → 1/0, gv_remove(v, i) — удалить элемент со сдвигом, gv_free(v). '
                   'Работает для int, структур и строк-указателей одинаково.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct gvec { void *data; size_t elem, len, cap; };\n'
                 '\n'
                 'void gv_init(struct gvec *v, size_t elem) {}\n'
                 'int gv_push(struct gvec *v, const void *x) { return -1; }\n'
                 'void *gv_at(struct gvec *v, size_t i) { return NULL; }\n'
                 'int gv_pop(struct gvec *v, void *out) { return 0; }\n'
                 'void gv_remove(struct gvec *v, size_t i) {}\n'
                 'void gv_free(struct gvec *v) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'struct pt { double x, y; short tag; };\n'
                '\n'
                'int main(void) {\n'
                '    struct gvec a, b, c;\n'
                '    gv_init(&a, sizeof(int));\n'
                '    gv_init(&b, sizeof(struct pt));\n'
                '    gv_init(&c, sizeof(const char *));\n'
                '    for (int i = 0; i < 10; i++) gv_push(&a, &i);\n'
                '    for (int i = 0; i < 6; i++) { struct pt p = {i * 1.5, -i, (short)(i * 10)}; gv_push(&b, '
                '&p); }\n'
                '    const char *w[] = {"alpha", "beta", "gamma"};\n'
                '    for (int i = 0; i < 3; i++) gv_push(&c, &w[i]);\n'
                '    gv_remove(&a, 0);\n'
                '    gv_remove(&a, 8);\n'
                '    int x;\n'
                '    printf("%zu %d %d\\n", a.len, *(int *)gv_at(&a, 0), *(int *)gv_at(&a, 7));\n'
                '    struct pt *q = gv_at(&b, 4);\n'
                '    printf("%.1f %.0f %d\\n", q->x, q->y, q->tag);\n'
                '    gv_remove(&b, 0);\n'
                '    printf("%.1f %d\\n", ((struct pt *)gv_at(&b, 0))->x, gv_at(&b, 5) == NULL);\n'
                '    printf("%s\\n", *(const char **)gv_at(&c, 2));\n'
                '    const char *s;\n'
                '    printf("%d %s %d\\n", gv_pop(&c, &s), s, gv_pop(&a, &x));\n'
                '    gv_free(&a); gv_free(&b); gv_free(&c);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Элемент i лежит по адресу (unsigned char *)data + i * elem; копируйте и сдвигайте блоки через '
              'memcpy / memmove.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['8 1 8', '6.0 -4 40', '1.5 1', 'gamma', '1 gamma 1']},
     {'id': 'c5-matrix-dyn',
      'mode': 'c',
      'title': 'Динамическая матрица двумя способами',
      'statement': 'mat_new_rows(r, c) → int **: массив указателей на строки, каждая строка выделена '
                   'отдельно (нули); mat_free_rows(m, r). mat_new_flat(r, c) → int * одним блоком (нули), '
                   'доступ m[i * c + j]. mat_transpose_flat(m, r, c) → новая матрица c × r в одном блоке. '
                   'Освобождает вызывающий; проверка AddressSanitizer.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int **mat_new_rows(size_t r, size_t c) { return NULL; }\n'
                 'void mat_free_rows(int **m, size_t r) {}\n'
                 'int *mat_new_flat(size_t r, size_t c) { return NULL; }\n'
                 'int *mat_transpose_flat(const int *m, size_t r, size_t c) { return NULL; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    int **m = mat_new_rows(3, 4);\n'
                '    for (int i = 0; i < 3; i++) for (int j = 0; j < 4; j++) m[i][j] += i * 4 + j;\n'
                '    printf("%d %d %d\\n", m[0][0], m[1][2], m[2][3]);\n'
                '    mat_free_rows(m, 3);\n'
                '    int *f = mat_new_flat(2, 3);\n'
                '    for (int i = 0; i < 6; i++) f[i] = i + 1;\n'
                '    int *t = mat_transpose_flat(f, 2, 3);\n'
                '    for (int i = 0; i < 6; i++) printf("%d ", t[i]);\n'
                '    printf("\\n");\n'
                '    free(f); free(t);\n'
                '    int *z = mat_new_flat(1000, 1000);\n'
                '    long s = 0;\n'
                '    for (int i = 0; i < 1000000; i++) s += z[i];\n'
                '    printf("%ld\\n", s);\n'
                '    free(z);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для массива строк при ошибке выделения на i-й строке освободите уже выделенные строки и сам '
              'массив указателей.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['0 6 11', '1 4 2 5 3 6', '0']},
     {'id': 'c5-string-builder',
      'mode': 'c',
      'title': 'Построитель строки',
      'statement': 'struct sb { char *buf; size_t len, cap; }. sb_init(sb), sb_append(sb, s) → 0/−1, '
                   'sb_appendc(sb, c), sb_appendf(sb, fmt, ...) → 0/−1 (через vsnprintf, длину определяйте '
                   'двумя вызовами), sb_str(sb) → const char * (всегда завершена нулём, даже для пустого), '
                   'sb_free(sb). Буфер растёт вдвое; десять тысяч добавлений не должны копировать всё каждый '
                   'раз.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct sb { char *buf; size_t len, cap; };\n'
                 '\n'
                 'void sb_init(struct sb *s) {}\n'
                 'int sb_append(struct sb *s, const char *t) { return -1; }\n'
                 'int sb_appendc(struct sb *s, char c) { return -1; }\n'
                 'int sb_appendf(struct sb *s, const char *fmt, ...) { return -1; }\n'
                 'const char *sb_str(const struct sb *s) { return ""; }\n'
                 'void sb_free(struct sb *s) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    struct sb s;\n'
                '    sb_init(&s);\n'
                '    printf("[%s]\\n", sb_str(&s));\n'
                '    sb_append(&s, "Hello");\n'
                "    sb_appendc(&s, ',');\n"
                "    sb_appendc(&s, ' ');\n"
                '    sb_appendf(&s, "%s #%d (%.2f)", "world", 42, 3.14159);\n'
                '    printf("[%s] %zu\\n", sb_str(&s), s.len);\n'
                '    sb_free(&s);\n'
                '    for (int i = 0; i < 10000; i++) sb_appendf(&s, "%d,", i);\n'
                '    printf("%zu %zu %c\\n", s.len, strlen(sb_str(&s)), sb_str(&s)[s.len - 2]);\n'
                '    sb_free(&s);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'vsnprintf(NULL, 0, fmt, ap) возвращает нужную длину; для второго вызова скопируйте va_list '
              'через va_copy.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['[]', '[Hello, world #42 (3.14)] 23', '48890 48890 9']},
     {'id': 'c5-sieve-bitmap',
      'mode': 'c',
      'title': 'Решето Эратосфена на битовой карте',
      'statement': 'count_primes(unsigned n) → число простых ≤ n (n до 50 000 000), используя битовую карту '
                   'в куче (calloc, по одному биту на число; чётные можно не хранить). nth_prime(unsigned k) '
                   '→ k-е простое (k = 1 → 2), решето нужного размера подберите сами (k до 2 000 000). '
                   'Должно выполняться за секунды.',
      'starter': 'unsigned count_primes(unsigned n) { return 0; }\n'
                 'unsigned nth_prime(unsigned k) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%u %u %u %u\\n", count_primes(1), count_primes(2), count_primes(100), '
                'count_primes(1000000));\n'
                '    printf("%u\\n", count_primes(50000000));\n'
                '    printf("%u %u %u %u\\n", nth_prime(1), nth_prime(6), nth_prime(1000), '
                'nth_prime(2000000));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для n-го простого подойдёт верхняя оценка k · (ln k + ln ln k) при k ≥ 6.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['0 1 25 78498', '3001134', '2 13 7919 32452843']},
     {'id': 'c5-intrusive',
      'mode': 'c',
      'title': 'Встраиваемый список и макрос owner_of',
      'statement': 'struct link { struct link *next, *prev; } встраивается в любую структуру. Макрос '
                   'owner_of(ptr, type, member) — указатель на объемлющую структуру по указателю на её поле '
                   '(через offsetof). Реализуйте кольцевой список со сигнальным узлом: link_init(h), '
                   'link_add_tail(h, n), link_del(n), link_empty(h). Драйвер встраивает link в структуры '
                   'разного размера и обходит список через owner_of.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct link { struct link *next, *prev; };\n'
                 '\n'
                 '/* owner_of(ptr, type, member) */\n'
                 'void link_init(struct link *h) {}\n'
                 'void link_add_tail(struct link *h, struct link *n) {}\n'
                 'void link_del(struct link *n) {}\n'
                 'int link_empty(const struct link *h) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '\n'
                'struct task { int id; char name[8]; struct link node; double load; };\n'
                'struct file { struct link node; int fd; };\n'
                '\n'
                'int main(void) {\n'
                '    struct link tasks, files;\n'
                '    link_init(&tasks);\n'
                '    link_init(&files);\n'
                '    struct task t[3] = {{1, "init", {0}, 0.5}, {2, "shell", {0}, 1.5}, {3, "cron", {0}, '
                '0.25}};\n'
                '    struct file f[2] = {{{0}, 10}, {{0}, 11}};\n'
                '    for (int i = 0; i < 3; i++) link_add_tail(&tasks, &t[i].node);\n'
                '    for (int i = 0; i < 2; i++) link_add_tail(&files, &f[i].node);\n'
                '    for (struct link *p = tasks.next; p != &tasks; p = p->next) {\n'
                '        struct task *x = owner_of(p, struct task, node);\n'
                '        printf("%d:%s:%.2f ", x->id, x->name, x->load);\n'
                '    }\n'
                '    printf("\\n");\n'
                '    link_del(&t[1].node);\n'
                '    for (struct link *p = tasks.prev; p != &tasks; p = p->prev) printf("%d ", owner_of(p, '
                'struct task, node)->id);\n'
                '    printf("\\n%d %d\\n", owner_of(files.next, struct file, node)->fd, owner_of(files.prev, '
                'struct file, node)->fd);\n'
                '    printf("%d %d\\n", link_empty(&tasks), link_empty(&files));\n'
                '    link_del(&t[0].node); link_del(&t[2].node);\n'
                '    printf("%d %d\\n", link_empty(&tasks), owner_of(&t[1].node, struct task, node) == '
                '&t[1]);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'owner_of: вычтите из адреса поля его смещение внутри структуры, offsetof(type, member); '
              'арифметику делайте на char *.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1:init:0.50 2:shell:1.50 3:cron:0.25', '3 1', '10 11', '0 0', '1 1']}]}
