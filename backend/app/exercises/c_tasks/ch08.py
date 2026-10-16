"""Задачи книги «От assembler к языку C»: глава 8 (код компилируется gcc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {8: [{'id': 'c8-fmt-row',
      'mode': 'c',
      'title': 'Таблица фиксированной ширины',
      'statement': 'print_row(out, name, qty, price) печатает строку «%-10s|%5d|%8.2f» и перевод строки; '
                   'название длиннее 10 символов обрезается до 10 (без нарушения таблицы). print_total(out, '
                   'n, sum) печатает «ИТОГО: n позиций на S» (S с двумя знаками), причём «позиций» в виде «1 '
                   'позиция», «2 позиции», «5 позиций» по правилам русского языка (ед.: 1, 21…; 2–4; '
                   'остальные; 11–14 — «позиций»).',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'void print_row(FILE *out, const char *name, int qty, double price) {\n'
                 '}\n'
                 '\n'
                 'void print_total(FILE *out, int n, double sum) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    CAP_BEGIN(o);\n'
                '    print_row(o, "bolt", 12, 0.5);\n'
                '    print_row(o, "washer-extra-long", 1000, 12345.678);\n'
                '    print_row(o, "", -3, -1.005);\n'
                '    print_total(o, 1, 10);\n'
                '    print_total(o, 2, 20.5);\n'
                '    print_total(o, 5, 0.125);\n'
                '    print_total(o, 11, 1);\n'
                '    print_total(o, 21, 2);\n'
                '    print_total(o, 112, 3);\n'
                '    print_total(o, 24, 4);\n'
                '    fputs(CAP_END(o), stdout);\n'
                '    return 0;\n'
                '}\n',
      'hint': '«%-10.10s» одновременно выравнивает по левому краю и обрезает строку до 10 символов. Для '
              'окончаний смотрите на n % 100 и n % 10.',
      'expected': ['bolt      |   12|    0.50',
                   'washer-ext| 1000|12345.68',
                   '          |   -3|   -1.00',
                   'ИТОГО: 1 позиция на 10.00',
                   'ИТОГО: 2 позиции на 20.50',
                   'ИТОГО: 5 позиций на 0.12',
                   'ИТОГО: 11 позиций на 1.00',
                   'ИТОГО: 21 позиция на 2.00',
                   'ИТОГО: 112 позиций на 3.00',
                   'ИТОГО: 24 позиции на 4.00']},
     {'id': 'c8-hex-dump',
      'mode': 'c',
      'title': 'Шестнадцатеричный дамп памяти',
      'statement': 'hex_dump(out, p, n) печатает байты по 16 в строке в формате «0000: 48 65 6c 6c 6f 2c 20 '
                   '57 6f 72 6c 64 21 0a 00 ff  |Hello, World!...|»: смещение четырьмя шестнадцатеричными '
                   'цифрами, двоеточие, пробел, 16 байт «%02x» через пробел (в неполной последней строке '
                   'недостающие позиции заполняют пробелами, чтобы колонка ASCII не сдвигалась), два '
                   'пробела, «|», символы (непечатаемые — точка), «|».',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'void hex_dump(FILE *out, const unsigned char *p, size_t n) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    CAP_BEGIN(o);\n'
                '    const unsigned char a[] = "Hello, World!\\n";\n'
                '    hex_dump(o, a, sizeof a);\n'
                '    unsigned char b[40];\n'
                '    for (int i = 0; i < 40; i++) b[i] = (unsigned char)(i * 7 + 30);\n'
                '    hex_dump(o, b, 40);\n'
                '    hex_dump(o, b, 0);\n'
                '    hex_dump(o, b, 16);\n'
                '    fputs(CAP_END(o), stdout);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Внешний цикл по строкам (шаг 16), в нём два внутренних: шестнадцатеричные байты (с «   » для '
              'пустых мест) и ASCII-колонка.',
      'expected': ['0000: 48 65 6c 6c 6f 2c 20 57 6f 72 6c 64 21 0a 00     |Hello, World!..|',
                   '0000: 1e 25 2c 33 3a 41 48 4f 56 5d 64 6b 72 79 80 87  |.%,3:AHOV]dkry..|',
                   '0010: 8e 95 9c a3 aa b1 b8 bf c6 cd d4 db e2 e9 f0 f7  |................|',
                   '0020: fe 05 0c 13 1a 21 28 2f                          |.....!(/|',
                   '0000: 1e 25 2c 33 3a 41 48 4f 56 5d 64 6b 72 79 80 87  |.%,3:AHOV]dkry..|']},
     {'id': 'c8-money',
      'mode': 'c',
      'title': 'Деньги с разделителями разрядов',
      'statement': 'fmt_money(buf, size, cents) записывает сумму в копейках как «$1,234.56» (разделитель '
                   'тысяч — запятая; для отрицательных — «-$5.07»; нуль — «$0.00»; копейки — всегда две '
                   'цифры) и возвращает длину полного результата без завершающего нуля, как snprintf. При '
                   'нехватке места текст усекается, завершающий ноль ставится всегда (если size > 0). '
                   'Допустимы значения вплоть до LLONG_MIN.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t fmt_money(char *buf, size_t size, long long cents) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void show(long long c) {\n'
                '    char b[40];\n'
                '    size_t n = fmt_money(b, sizeof b, c);\n'
                '    printf("%s %zu\\n", b, n);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    long long v[] = {0, 5, 99, 100, 123456, -507, 100000000, -123456789, 99999999999LL, '
                '1000, 100099};\n'
                '    for (size_t i = 0; i < sizeof v / sizeof v[0]; i++) show(v[i]);\n'
                '    show(LLONG_MIN);\n'
                '    char small[6];\n'
                '    size_t n = fmt_money(small, sizeof small, 123456789);\n'
                '    printf("%s %zu\\n", small, n);\n'
                "    char one[1] = {'x'};\n"
                '    n = fmt_money(one, 1, 1234);\n'
                '    printf("%d %zu\\n", one[0], n);\n'
                '    n = fmt_money(NULL, 0, 1234);\n'
                '    printf("%zu\\n", n);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Разберите число на целую и дробную части (в unsigned long long — для LLONG_MIN), сгруппируйте '
              'цифры по три справа налево, соберите результат во временном буфере и скопируйте не больше '
              'size − 1 байта.',
      'expected': ['$0.00 5',
                   '$0.05 5',
                   '$0.99 5',
                   '$1.00 5',
                   '$1,234.56 9',
                   '-$5.07 6',
                   '$1,000,000.00 13',
                   '-$1,234,567.89 14',
                   '$999,999,999.99 15',
                   '$10.00 6',
                   '$1,000.99 9',
                   '-$92,233,720,368,547,758.08 27',
                   '$1,23 13',
                   '0 6',
                   '6']},
     {'id': 'c8-join-ints',
      'mode': 'c',
      'title': 'Склейка чисел в строку без переполнения',
      'statement': 'join_ints(buf, size, a, n, sep) записывает числа через разделитель («1, 2, 3» при sep = '
                   '", ") и возвращает длину полного результата без завершающего нуля — как snprintf. Если '
                   'места не хватает, текст усекается, но завершающий ноль на месте (при size > 0), а '
                   'возвращаемое значение остаётся полной длиной. Пустой массив → пустая строка. Используйте '
                   'только snprintf.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t join_ints(char *buf, size_t size, const int *a, size_t n, const char *sep) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void run(const int *a, size_t n, const char *sep, size_t size) {\n'
                '    char *b = malloc(size ? size : 1);\n'
                '    size_t r = join_ints(b, size, a, n, sep);\n'
                '    printf("[%s] %zu\\n", size ? b : "-", r);\n'
                '    free(b);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    int a[] = {1, -22, 333, 4444, 5};\n'
                '    run(a, 5, ", ", 64);\n'
                '    run(a, 5, "", 64);\n'
                '    run(a, 5, ", ", 12);\n'
                '    run(a, 5, ", ", 3);\n'
                '    run(a, 5, ", ", 1);\n'
                '    run(a, 0, ", ", 8);\n'
                '    run(a, 1, ", ", 3);\n'
                "    char tail[3] = {'x', 'y', 'z'};\n"
                '    join_ints(tail, 0, a, 5, ",");\n'
                '    printf("%c%c%c\\n", tail[0], tail[1], tail[2]);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Накапливайте total как сумму значений, которые вернул snprintf; в snprintf передавайте '
              'оставшееся место (или 0 и NULL, если буфер уже исчерпан).',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['[1, -22, 333, 4444, 5] 20',
                   '[1-2233344445] 12',
                   '[1, -22, 333] 20',
                   '[1,] 20',
                   '[] 20',
                   '[] 0',
                   '[1] 1',
                   'xyz']},
     {'id': 'c8-fmt-len',
      'mode': 'c',
      'title': 'Длина результата printf и свой asprintf',
      'statement': 'fmt_len(fmt, …) → число символов, которое напечатал бы printf с такими аргументами, без '
                   'печати (через vsnprintf с буфером NULL). xasprintf(fmt, …) → строка, выделенная malloc, '
                   'нужной длины (или NULL при ошибке); вызывающий освобождает её сам. Программа запускается '
                   'с AddressSanitizer.',
      'starter': '#include <stdarg.h>\n'
                 '#include <stdio.h>\n'
                 '#include <stdlib.h>\n'
                 '\n'
                 'int fmt_len(const char *fmt, ...) {\n'
                 '    return -1;\n'
                 '}\n'
                 '\n'
                 'char *xasprintf(const char *fmt, ...) {\n'
                 '    return NULL;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d\\n", fmt_len("hello"), fmt_len("%d|%5s|%-4d|", 12345, "ab", 7), '
                'fmt_len("%08.3f", 3.14159));\n'
                '    printf("%d %d\\n", fmt_len(""), fmt_len("%s", "длинная строка"));\n'
                '    char *s = xasprintf("%s=%d (%c) %.2f", "answer", 42, \'x\', 2.5);\n'
                '    printf("%s %zu\\n", s, strlen(s));\n'
                '    free(s);\n'
                '    char *e = xasprintf("");\n'
                '    printf("[%s]\\n", e);\n'
                '    free(e);\n'
                '    char big[300];\n'
                "    memset(big, 'z', 299);\n"
                '    big[299] = 0;\n'
                '    char *b = xasprintf("<%s>", big);\n'
                '    printf("%zu %c %c\\n", strlen(b), b[0], b[300]);\n'
                '    free(b);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'vsnprintf(NULL, 0, fmt, ap) возвращает нужную длину. Список аргументов можно использовать '
              'только один раз — для второго прохода сделайте va_copy.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['5 17 8', '0 27', 'answer=42 (x) 2.50 18', '[]', '301 < >']},
     {'id': 'c8-my-printf',
      'mode': 'c',
      'title': 'Свой printf: %d %u %x %c %s %%',
      'statement': 'my_printf(out, fmt, …) → число записанных символов: обычные символы копируются, а «%d» '
                   '(int), «%u» (unsigned), «%x» (unsigned, строчные цифры), «%c», «%s» (NULL печатается как '
                   '«(null)») и «%%» обрабатываются вручную. Ширину и флаги поддерживать не нужно; '
                   'неизвестный спецификатор печатается как есть (вместе с процентом). Вызывать '
                   'printf-семейство (fprintf, vfprintf, snprintf…) нельзя — только fputc и fputs.',
      'starter': '#include <stdarg.h>\n'
                 '#include <stdio.h>\n'
                 '\n'
                 'int my_printf(FILE *out, const char *fmt, ...) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
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
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    CAP_BEGIN(o);\n'
                '    int n1 = my_printf(o, "int %d %d %d|", 0, -17, INT_MIN);\n'
                '    int n2 = my_printf(o, "uns %u %u|hex %x %x %x|", 4000000000u, 0u, 255u, 0u, '
                '0xDEADBEEFu);\n'
                '    int n3 = my_printf(o, "ch %c%c str %s %s 100%%|%q|%", \'o\', \'k\', "text", NULL);\n'
                '    int n4 = my_printf(o, "");\n'
                '    fputs(CAP_END(o), stdout);\n'
                '    printf("\\n%d %d %d %d\\n", n1, n2, n3, n4);\n'
                '    printf("lib: %d\\n", src_count("fpri" "ntf(") + src_count("snpr" "intf(") + '
                'src_count("vfpr" "intf("));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Цикл по формату: обычный символ — fputc; после «%» смотрим следующую букву и достаём аргумент '
              'через va_arg. Цифры собирайте в массив в обратном порядке.',
      'expected': ['int 0 -17 -2147483648|uns 4000000000 0|hex ff 0 deadbeef|ch ok str text (null) 100%|%q|%',
                   '22 35 31 0',
                   'lib: 0']},
     {'id': 'c8-log-wrapper',
      'mode': 'c',
      'title': 'Журнал с уровнями через vfprintf',
      'statement': 'struct logger { FILE *out; int min_level; int written; }. log_init(l, out, min_level); '
                   'logf(l, level, fmt, …) — если level ≥ min_level, печатает «[LEVEL] сообщение» и перевод '
                   'строки и увеличивает written; названия уровней: 0 DEBUG, 1 INFO, 2 WARN, 3 ERROR (прочие '
                   '— «LEVEL?»); функция возвращает 1, если сообщение выведено, иначе 0. Для печати '
                   'используйте vfprintf.',
      'starter': '#include <stdarg.h>\n'
                 '#include <stdio.h>\n'
                 '\n'
                 'struct logger { FILE *out; int min_level; int written; };\n'
                 '\n'
                 'void log_init(struct logger *l, FILE *out, int min_level) {}\n'
                 '\n'
                 'int logf_(struct logger *l, int level, const char *fmt, ...) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    CAP_BEGIN(o);\n'
                '    struct logger l;\n'
                '    log_init(&l, o, 1);\n'
                '    int r[6];\n'
                '    r[0] = logf_(&l, 0, "hidden %d", 1);\n'
                '    r[1] = logf_(&l, 1, "start");\n'
                '    r[2] = logf_(&l, 2, "disk %d%% used on %s", 93, "/dev/sda");\n'
                '    r[3] = logf_(&l, 3, "%s: %05.1f", "temp", 7.25);\n'
                '    r[4] = logf_(&l, 9, "odd level");\n'
                '    log_init(&l, o, 3);\n'
                '    r[5] = logf_(&l, 2, "skipped");\n'
                '    fputs(CAP_END(o), stdout);\n'
                '    printf("%d %d %d %d %d %d %d\\n", r[0], r[1], r[2], r[3], r[4], r[5], l.written);\n'
                '    return 0;\n'
                '}\n',
      'hint': "fprintf для префикса, затем vfprintf(l->out, fmt, ap) с va_list, затем fputc('\\n').",
      'expected': ['[INFO] start',
                   '[WARN] disk 93% used on /dev/sda',
                   '[ERROR] temp: 007.2',
                   '[LEVEL?] odd level',
                   '0 1 1 1 1 0 0']},
     {'id': 'c8-varargs-utils',
      'mode': 'c',
      'title': 'Функции с переменным числом аргументов',
      'statement': 'sum_ints(n, …) — сумма n чисел int; avg(n, …) — среднее n чисел double (n > 0, иначе '
                   '0.0); concat_all(first, …) — склейка строк, список заканчивается NULL; результат — '
                   'строка из malloc (вызывающий освобождает), для одного NULL → пустая строка; max_of(n, …) '
                   '— максимум n чисел int. Не обращайтесь к va_arg больше, чем передано. Под '
                   'AddressSanitizer.',
      'starter': '#include <stdarg.h>\n'
                 '#include <stdlib.h>\n'
                 '\n'
                 'int sum_ints(int n, ...) { return 0; }\n'
                 'double avg(int n, ...) { return 0; }\n'
                 'char *concat_all(const char *first, ...) { return NULL; }\n'
                 'int max_of(int n, ...) { return 0; }\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    printf("%d %d %d\\n", sum_ints(0), sum_ints(1, 5), sum_ints(5, 1, 2, 3, 4, 5));\n'
                '    printf("%.3f %.3f %.3f\\n", avg(0), avg(1, 2.5), avg(4, 1.0, 2.0, 3.0, 10.5));\n'
                '    char *a = concat_all("alpha", "-", "beta", "-", "gamma", NULL);\n'
                '    char *b = concat_all(NULL);\n'
                '    char *c = concat_all("single", NULL);\n'
                '    printf("%s|%s|%s\\n", a, b, c);\n'
                '    free(a);\n'
                '    free(b);\n'
                '    free(c);\n'
                '    printf("%d %d %d\\n", max_of(1, -4), max_of(3, 7, 99, -1), max_of(4, -9, -8, -7, -6));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для concat_all двух проходов по va_list достаточно: считаем длину, затем va_end и снова '
              'va_start для копирования.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['0 5 15', '0.000 2.500 4.125', 'alpha-beta-gamma||single', '-4 99 -6']},
     {'id': 'c8-sscanf-record',
      'mode': 'c',
      'title': 'Разбор записи «имя:возраст:оценка»',
      'statement': 'struct rec { char name[16]; int age; double score; }. parse_rec(line, *r) → 0 при '
                   'успехе, −1 при ошибке: строка должна быть вида «имя:возраст:оценка» (имя — до 15 '
                   'символов без двоеточия, не пустое; возраст — целое; оценка — число с точкой), после '
                   'оценки допустим только пробельный хвост (пробелы, перевод строки). Используйте sscanf с '
                   'ограничением ширины и проверкой результата; при ошибке структура не должна меняться.',
      'starter': 'struct rec { char name[16]; int age; double score; };\n'
                 '\n'
                 'int parse_rec(const char *line, struct rec *r) {\n'
                 '    return -2;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void t(const char *s) {\n'
                '    struct rec r = {"keep", -1, -1.0};\n'
                '    int rc = parse_rec(s, &r);\n'
                '    printf("%d %s %d %.2f\\n", rc, r.name, r.age, r.score);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    t("anna:30:4.5");\n'
                '    t("bob:7:3\\n");\n'
                '    t("charlie the great:44:5.0  \\n");\n'
                '    t("verylongname12345:20:1.0");\n'
                '    t(":5:1.0");\n'
                '    t("dave:x:1.0");\n'
                '    t("eve:20");\n'
                '    t("frank:20:3.5 extra");\n'
                '    t("");\n'
                '    t("g:-5:-2.25");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Формат «%15[^:]:%d:%lf%n»: %n записывает, сколько символов использовано; проверьте k == 3 и '
              'что после used идут только пробелы.',
      'expected': ['0 anna 30 4.50',
                   '0 bob 7 3.00',
                   '-1 keep -1 -1.00',
                   '-1 keep -1 -1.00',
                   '-1 keep -1 -1.00',
                   '-1 keep -1 -1.00',
                   '-1 keep -1 -1.00',
                   '-1 keep -1 -1.00',
                   '-1 keep -1 -1.00',
                   '0 g -5 -2.25']},
     {'id': 'c8-strtol-safe',
      'mode': 'c',
      'title': 'Безопасный разбор чисел: parse_int и parse_double',
      'statement': 'parse_int(s, base, *out) → 0 при успехе; −1 — нет цифр (в том числе пустая строка и '
                   '«-»); −2 — после числа есть посторонние символы (пробельный хвост допустим, начальные '
                   'пробелы допустимы); −3 — выход за диапазон long (errno == ERANGE). При ошибке *out не '
                   'меняется. parse_double(s, *out) → 0, −1 или −2 по тем же правилам (бесконечности и NaN — '
                   'как ошибка −1).',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'int parse_int(const char *s, int base, long *out) {\n'
                 '    return -9;\n'
                 '}\n'
                 '\n'
                 'int parse_double(const char *s, double *out) {\n'
                 '    return -9;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void ti(const char *s, int base) {\n'
                '    long v = 777;\n'
                '    int rc = parse_int(s, base, &v);\n'
                '    printf("int [%s] %d -> %d %ld\\n", s, base, rc, v);\n'
                '}\n'
                'static void td(const char *s) {\n'
                '    double v = 777;\n'
                '    int rc = parse_double(s, &v);\n'
                '    printf("dbl [%s] -> %d %g\\n", s, rc, v);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    ti("42", 10);\n'
                '    ti("  -17  ", 10);\n'
                '    ti("0x1F", 16);\n'
                '    ti("0x1F", 0);\n'
                '    ti("077", 0);\n'
                '    ti("101", 2);\n'
                '    ti("", 10);\n'
                '    ti("-", 10);\n'
                '    ti("12ab", 10);\n'
                '    ti("ff", 10);\n'
                '    ti("99999999999999999999", 10);\n'
                '    ti("-99999999999999999999", 10);\n'
                '    td("3.25");\n'
                '    td(" -1e3 ");\n'
                '    td("1.5.2");\n'
                '    td("abc");\n'
                '    td("");\n'
                '    td("inf");\n'
                '    td("nan");\n'
                '    td("1e999");\n'
                '    td(".5");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'errno = 0 перед вызовом; end == s — цифр не было; затем errno == ERANGE; затем остаток строки '
              'должен состоять из пробелов.',
      'expected': ['int [42] 10 -> 0 42',
                   'int [  -17  ] 10 -> 0 -17',
                   'int [0x1F] 16 -> 0 31',
                   'int [0x1F] 0 -> 0 31',
                   'int [077] 0 -> 0 63',
                   'int [101] 2 -> 0 5',
                   'int [] 10 -> -1 777',
                   'int [-] 10 -> -1 777',
                   'int [12ab] 10 -> -2 777',
                   'int [ff] 10 -> -1 777',
                   'int [99999999999999999999] 10 -> -3 777',
                   'int [-99999999999999999999] 10 -> -3 777',
                   'dbl [3.25] -> 0 3.25',
                   'dbl [ -1e3 ] -> 0 -1000',
                   'dbl [1.5.2] -> -2 777',
                   'dbl [abc] -> -1 777',
                   'dbl [] -> -1 777',
                   'dbl [inf] -> -1 777',
                   'dbl [nan] -> -1 777',
                   'dbl [1e999] -> -1 777',
                   'dbl [.5] -> 0 0.5']},
     {'id': 'c8-read-lines',
      'mode': 'c',
      'title': 'Чтение строк в массив фиксированных строк',
      'statement': 'read_lines(in, lines, max) читает строки из потока в массив char lines[][32]: перевод '
                   'строки (и возможный "\\r") убирается; строки длиннее 31 символа обрезаются до 31, а '
                   'остаток строки пропускается (не превращается в новую строку); пустые строки сохраняются; '
                   'последняя строка без перевода строки тоже считается. Возвращает число прочитанных строк '
                   '(не больше max). Используйте fgets.',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'size_t read_lines(FILE *in, char lines[][32], size_t max) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'static void run(const char *txt, size_t max) {\n'
                '    FILE *f = from_str(txt);\n'
                '    char lines[8][32];\n'
                '    size_t n = read_lines(f, lines, max);\n'
                '    fclose(f);\n'
                '    printf("%zu:", n);\n'
                '    for (size_t i = 0; i < n; i++) printf(" [%s]", lines[i]);\n'
                '    printf("\\n");\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("one\\ntwo\\nthree\\n", 8);\n'
                '    run("one\\ntwo\\nthree", 8);\n'
                '    run("a\\n\\nb\\n\\n", 8);\n'
                '    run("win\\r\\nlines\\r\\n", 8);\n'
                '    run("1234567890123456789012345678901\\nnext\\n", 8);\n'
                '    run("12345678901234567890123456789012345678901234567890\\nnext\\n", 8);\n'
                '    run("123456789012345678901234567890\\nnext\\n", 8);\n'
                '    run("a\\nb\\nc\\nd\\n", 2);\n'
                '    run("", 8);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Читайте fgets в буфер на 32 байта: если перевода строки нет и строка не кончилась — это '
              'начало слишком длинной строки; остаток пропускайте, пока не встретите перевод строки.',
      'expected': ['3: [one] [two] [three]',
                   '3: [one] [two] [three]',
                   '4: [a] [] [b] []',
                   '2: [win] [lines]',
                   '2: [1234567890123456789012345678901] [next]',
                   '2: [1234567890123456789012345678901] [next]',
                   '2: [123456789012345678901234567890] [next]',
                   '2: [a] [b]',
                   '0:']},
     {'id': 'c8-read-line-alloc',
      'mode': 'c',
      'title': 'Строка произвольной длины',
      'statement': 'read_line(in) → строка из malloc без перевода строки (и без возможного "\\r" перед ним) '
                   'либо NULL, если читать больше нечего; последняя строка без перевода строки возвращается '
                   'как есть; пустая строка между переводами — пустая строка (не NULL). Длина строки не '
                   'ограничена: буфер растёт вдвое с 4 байт. Под AddressSanitizer: утечки и выходы за '
                   'границы запрещены.',
      'starter': '#include <stdio.h>\n'
                 '#include <stdlib.h>\n'
                 '\n'
                 'char *read_line(FILE *in) {\n'
                 '    return NULL;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    char *big = malloc(5001);\n'
                "    memset(big, 'q', 5000);\n"
                '    big[5000] = 0;\n'
                '    char *txt = malloc(5100);\n'
                '    sprintf(txt, "short\\n\\n%s\\nwin\\r\\nlast", big);\n'
                '    FILE *f = from_str(txt);\n'
                '    char *l;\n'
                '    int k = 0;\n'
                '    while ((l = read_line(f)) != NULL) {\n'
                '        printf("%d: len=%zu first=%c\\n", ++k, strlen(l), l[0] ? l[0] : \'-\');\n'
                '        free(l);\n'
                '    }\n'
                '    printf("%d\\n", read_line(f) == NULL);\n'
                '    fclose(f);\n'
                '    FILE *e = from_str("");\n'
                '    printf("%d\\n", read_line(e) == NULL);\n'
                '    fclose(e);\n'
                '    FILE *g = from_str("only\\n");\n'
                '    l = read_line(g);\n'
                '    printf("%s %d\\n", l, read_line(g) == NULL);\n'
                '    free(l);\n'
                '    fclose(g);\n'
                '    free(big);\n'
                '    free(txt);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Читайте fgetc в int; следите за «cap» с запасом под завершающий ноль. Пустой поток отличается '
              'от потока из одного перевода строки: во втором случае возвращается пустая строка.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1: len=5 first=s',
                   '2: len=0 first=-',
                   '3: len=5000 first=q',
                   '4: len=3 first=w',
                   '5: len=4 first=l',
                   '1',
                   '1',
                   'only 1']},
     {'id': 'c8-wc',
      'mode': 'c',
      'title': 'wc: строки, слова, символы',
      'statement': 'struct counts { size_t lines, words, chars; }. count_stream(in, *c) читает поток '
                   'посимвольно (fgetc) и считает: chars — все прочитанные байты; lines — число переводов '
                   'строки; words — число слов (последовательностей непробельных символов; пробельные — '
                   'isspace). Последняя строка без перевода строки в lines не входит (как у wc). Функция '
                   'обнуляет структуру в начале.',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'struct counts { size_t lines, words, chars; };\n'
                 '\n'
                 'void count_stream(FILE *in, struct counts *c) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'static void run(const char *s) {\n'
                '    FILE *f = from_str(s);\n'
                '    struct counts c = {99, 99, 99};\n'
                '    count_stream(f, &c);\n'
                '    fclose(f);\n'
                '    printf("%zu %zu %zu\\n", c.lines, c.words, c.chars);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("");\n'
                '    run("hello world\\n");\n'
                '    run("hello world");\n'
                '    run("  a  b\\tc \\n\\n d\\n");\n'
                '    run("\\n\\n\\n");\n'
                '    run("one-word");\n'
                "    unsigned char bin[] = {0xFF, ' ', 0x80, 'x', '\\n', 0};\n"
                '    FILE *f = from_bytes(bin, sizeof bin);\n'
                '    struct counts c;\n'
                '    count_stream(f, &c);\n'
                '    fclose(f);\n'
                '    printf("%zu %zu %zu\\n", c.lines, c.words, c.chars);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Состояние «внутри слова»: слово начинается при переходе от пробельного символа к '
              'непробельному. fgetc возвращает int; в isspace передавайте само значение.',
      'expected': ['0 0 0', '1 2 12', '0 2 11', '3 4 14', '3 0 3', '0 1 8', '1 3 6']},
     {'id': 'c8-csv-write',
      'mode': 'c',
      'title': 'Запись CSV с кавычками',
      'statement': 'write_csv_field(out, s) печатает поле: если в нём есть запятая, двойная кавычка или '
                   'перевод строки (\\n или \\r) — поле берётся в двойные кавычки, а внутренние кавычки '
                   'удваиваются; иначе — как есть. write_csv_row(out, fields, n) печатает n полей через '
                   'запятую и завершает строку символом \\n. Пустое поле — пусто. Для вывода пользуйтесь '
                   'fputc/fputs.',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'void write_csv_field(FILE *out, const char *s) {\n'
                 '}\n'
                 '\n'
                 'void write_csv_row(FILE *out, const char *const *fields, size_t n) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    CAP_BEGIN(o);\n'
                '    const char *r1[] = {"id", "name", "note"};\n'
                '    const char *r2[] = {"1", "Smith, John", "said \\"hi\\""};\n'
                '    const char *r3[] = {"", "multi\\nline", " spaced "};\n'
                '    const char *r4[] = {"\\"", ",", "a\\"b\\"c"};\n'
                '    write_csv_row(o, r1, 3);\n'
                '    write_csv_row(o, r2, 3);\n'
                '    write_csv_row(o, r3, 3);\n'
                '    write_csv_row(o, r4, 3);\n'
                '    write_csv_row(o, r1, 0);\n'
                '    write_csv_row(o, r1, 1);\n'
                '    fputs(CAP_END(o), stdout);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'strpbrk(s, ",\\"\\r\\n") подсказывает, нужны ли кавычки; внутри кавычек каждую двойную '
              'кавычку пишите дважды.',
      'expected': ['id,name,note',
                   '1,"Smith, John","said ""hi"""',
                   ',"multi',
                   'line", spaced',
                   '"""",",","a""b""c"',
                   '',
                   'id']},
     {'id': 'c8-csv-parse',
      'mode': 'c',
      'title': 'Разбор строки CSV',
      'statement': 'parse_csv(line, fields, max) разбирает одну строку CSV в массив char fields[][32] и '
                   'возвращает число полей (не больше max). Поля разделяет запятая; поле в двойных кавычках '
                   'может содержать запятые, а «""» внутри кавычек означает одну кавычку; пробелы '
                   'сохраняются; завершающий перевод строки (\\n, \\r\\n) отбрасывается; пустая строка — '
                   'одно пустое поле. Слишком длинные поля обрезаются до 31 символа.',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'size_t parse_csv(const char *line, char fields[][32], size_t max) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void t(const char *s) {\n'
                '    char f[6][32];\n'
                '    size_t n = parse_csv(s, f, 6);\n'
                '    printf("%zu:", n);\n'
                '    for (size_t i = 0; i < n; i++) printf(" [%s]", f[i]);\n'
                '    printf("\\n");\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    t("a,b,c");\n'
                '    t("a,b,c\\n");\n'
                '    t("1,\\"Smith, John\\",x\\r\\n");\n'
                '    t("\\"say \\"\\"hi\\"\\"\\",2");\n'
                '    t(",,");\n'
                '    t("");\n'
                '    t("only");\n'
                '    t("a, b ,c");\n'
                '    t("\\"\\",x");\n'
                '    t("1,2,3,4,5,6,7,8");\n'
                '    t("abcdefghijklmnopqrstuvwxyz0123456789ABCDEF,z");\n'
                '    t("x,");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Состояния: «обычное поле» (до запятой) и «в кавычках» (до одиночной кавычки, «""» → «"»). '
              'После закрывающей кавычки пропустите всё до запятой.',
      'expected': ['3: [a] [b] [c]',
                   '3: [a] [b] [c]',
                   '3: [1] [Smith, John] [x]',
                   '2: [say "hi"] [2]',
                   '3: [] [] []',
                   '1: []',
                   '1: [only]',
                   '3: [a] [ b ] [c]',
                   '2: [] [x]',
                   '6: [1] [2] [3] [4] [5] [6]',
                   '2: [abcdefghijklmnopqrstuvwxyz01234] [z]',
                   '2: [x] []']},
     {'id': 'c8-copy-stream',
      'mode': 'c',
      'title': 'Копирование потоков блоками',
      'statement': 'copy_stream(in, out) копирует все данные из in в out блоками по 7 байт через '
                   'fread/fwrite (размер блока взят нарочно нечётным) и возвращает число скопированных байт '
                   'либо −1, если запись или чтение завершились ошибкой (запись меньшего числа байт, чем '
                   'прочитано). copy_n(in, out, n) копирует не более n байт и возвращает число реально '
                   'скопированных. Двоичные данные (в том числе нулевые байты) должны проходить без '
                   'изменений.',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'long copy_stream(FILE *in, FILE *out) {\n'
                 '    return -9;\n'
                 '}\n'
                 '\n'
                 'size_t copy_n(FILE *in, FILE *out, size_t n) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    unsigned char data[100];\n'
                '    for (int i = 0; i < 100; i++) data[i] = (unsigned char)(i % 5 == 0 ? 0 : i * 3);\n'
                '    FILE *in = from_bytes(data, 100);\n'
                '    FILE *out = tmpfile();\n'
                '    long n = copy_stream(in, out);\n'
                '    rewind(out);\n'
                '    unsigned char back[100] = {0};\n'
                '    size_t r = fread(back, 1, 100, out);\n'
                '    printf("%ld %zu %d\\n", n, r, memcmp(data, back, 100) == 0);\n'
                '    fclose(in);\n'
                '    fclose(out);\n'
                '    in = from_bytes(data, 100);\n'
                '    out = tmpfile();\n'
                '    size_t a = copy_n(in, out, 10);\n'
                '    size_t b = copy_n(in, out, 30);\n'
                '    size_t c = copy_n(in, out, 1000);\n'
                '    size_t d = copy_n(in, out, 5);\n'
                '    printf("%zu %zu %zu %zu\\n", a, b, c, d);\n'
                '    rewind(out);\n'
                '    memset(back, 0, sizeof back);\n'
                '    r = fread(back, 1, 100, out);\n'
                '    printf("%zu %d\\n", r, memcmp(data, back, 100) == 0);\n'
                '    fclose(in);\n'
                '    fclose(out);\n'
                '    in = from_bytes(data, 0);\n'
                '    out = tmpfile();\n'
                '    printf("%ld %zu\\n", copy_stream(in, out), copy_n(in, out, 5));\n'
                '    FILE *ro = fopen("/dev/null", "r");\n'
                '    in = from_bytes(data, 10);\n'
                '    printf("%ld\\n", ro ? copy_stream(in, ro) : -1L);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Цикл: k = fread(buf, 1, sizeof buf, in); если k == 0 — конец; fwrite(buf, 1, k, out) должна '
              'записать ровно k.',
      'expected': ['100 100 1', '10 30 60 0', '100 1', '0 0', '-1']},
     {'id': 'c8-binary-records',
      'mode': 'c',
      'title': 'Двоичные записи фиксированного формата',
      'statement': 'struct rec { uint32_t id; char name[8]; uint16_t score; }. Формат записи — ровно 14 '
                   'байт: id (4 байта, little-endian), name (8 байт, добивается нулями; длинные имена '
                   'обрезаются до 8 без завершающего нуля), score (2 байта, little-endian). write_rec(f, r) '
                   '→ 0/−1; read_rec(f, *r) → 1 при успехе, 0 на конце файла или при неполной записи '
                   '(структура при этом не меняется); name в структуре всегда завершён нулём (читаются 8 '
                   'байт + нуль в 9-м элементе — поэтому в структуре name[9]).',
      'starter': '#include <stdint.h>\n'
                 '#include <stdio.h>\n'
                 '\n'
                 'struct rec { uint32_t id; char name[9]; uint16_t score; };\n'
                 '\n'
                 'int write_rec(FILE *f, const struct rec *r) {\n'
                 '    return -1;\n'
                 '}\n'
                 '\n'
                 'int read_rec(FILE *f, struct rec *r) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    FILE *f = tmpfile();\n'
                '    struct rec a = {0x01020304, "abc", 513};\n'
                '    struct rec b = {7, "exactly8", 65535};\n'
                '    struct rec c = {0xFFFFFFFF, "waytoolongname", 0};\n'
                '    printf("%d %d %d\\n", write_rec(f, &a), write_rec(f, &b), write_rec(f, &c));\n'
                '    fflush(f);\n'
                '    printf("%ld\\n", ftell(f));\n'
                '    rewind(f);\n'
                '    unsigned char raw[14];\n'
                '    fread(raw, 1, 14, f);\n'
                '    for (int i = 0; i < 14; i++) printf("%02x", raw[i]);\n'
                '    printf("\\n");\n'
                '    rewind(f);\n'
                '    struct rec r;\n'
                '    while (read_rec(f, &r)) printf("%u [%s] %u\\n", (unsigned)r.id, r.name, '
                '(unsigned)r.score);\n'
                '    struct rec keep = {5, "keep", 5};\n'
                '    printf("%d %u\\n", read_rec(f, &keep), (unsigned)keep.id);\n'
                '    FILE *g = tmpfile();\n'
                "    unsigned char part[10] = {1, 2, 3, 4, 'x', 0, 0, 0, 0, 0};\n"
                '    fwrite(part, 1, 10, g);\n'
                '    rewind(g);\n'
                '    printf("%d %u [%s]\\n", read_rec(g, &keep), (unsigned)keep.id, keep.name);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Собирайте и разбирайте 14 байт вручную: сдвиги по байтам для id и score, memcpy для name. '
              'fwrite структуры целиком — ошибка: выравнивание.',
      'expected': ['0 0 0',
                   '42',
                   '0403020161626300000000000102',
                   '16909060 [abc] 513',
                   '7 [exactly8] 65535',
                   '4294967295 [waytoolo] 0',
                   '0 5',
                   '0 5 [keep]']},
     {'id': 'c8-file-ops',
      'mode': 'c',
      'title': 'Размер файла, чтение со смещения, хвост',
      'statement': 'file_size(f) → размер потока в байтах, не меняя текущую позицию (fseek/ftell и возврат); '
                   'read_at(f, off, buf, n) → 0, если прочитано ровно n байт со смещения off, иначе −1; '
                   'tail_bytes(f, n, buf) → число байт, записанных в buf: последние n байт файла (или весь '
                   'файл, если он короче). Позицию потока после вызовов не требуется сохранять, кроме '
                   'file_size.',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'long file_size(FILE *f) {\n'
                 '    return -2;\n'
                 '}\n'
                 '\n'
                 'int read_at(FILE *f, long off, void *buf, size_t n) {\n'
                 '    return -2;\n'
                 '}\n'
                 '\n'
                 'size_t tail_bytes(FILE *f, size_t n, unsigned char *buf) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    FILE *f = from_str("0123456789abcdefghij");\n'
                '    char c4[5] = {0};\n'
                '    fread(c4, 1, 4, f);\n'
                '    printf("%ld %ld %s\\n", file_size(f), ftell(f), c4);\n'
                '    char b[8] = {0};\n'
                '    printf("%d %.*s\\n", read_at(f, 10, b, 5), 5, b);\n'
                '    printf("%d\\n", read_at(f, 18, b, 5));\n'
                '    printf("%d\\n", read_at(f, -1, b, 1));\n'
                '    printf("%d\\n", read_at(f, 20, b, 0));\n'
                '    unsigned char t[32] = {0};\n'
                '    size_t n = tail_bytes(f, 6, t);\n'
                '    printf("%zu %.*s\\n", n, (int)n, t);\n'
                '    n = tail_bytes(f, 100, t);\n'
                '    printf("%zu %.*s\\n", n, (int)n, t);\n'
                '    n = tail_bytes(f, 0, t);\n'
                '    printf("%zu\\n", n);\n'
                '    FILE *e = from_str("");\n'
                '    printf("%ld %zu\\n", file_size(e), tail_bytes(e, 5, t));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'file_size: запомнить ftell, fseek(SEEK_END), ftell, вернуться. tail_bytes: start = size − n '
              '(или 0), fseek, fread.',
      'expected': ['20 4 0123',
                   '0 abcde',
                   '-1',
                   '-1',
                   '0',
                   '6 efghij',
                   '20 0123456789abcdefghij',
                   '0',
                   '0 0']},
     {'id': 'c8-tokenizer',
      'mode': 'c',
      'title': 'Слова из потока посимвольно',
      'statement': 'next_token(in, buf, size) читает из потока следующее слово (последовательность '
                   'непробельных символов; пробельные — isspace) и записывает его в buf; возвращает длину '
                   'слова (до size − 1), а если слов больше нет — −1. Слишком длинное слово обрезается до '
                   'size − 1 символа, остальные его символы пропускаются (они не становятся следующим '
                   'словом). Используйте fgetc и ungetc при необходимости.',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'int next_token(FILE *in, char *buf, size_t size) {\n'
                 '    return -9;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'static void run(const char *s, size_t size) {\n'
                '    FILE *f = from_str(s);\n'
                '    char b[16];\n'
                '    int n;\n'
                '    printf("size %zu:", size);\n'
                '    while ((n = next_token(f, b, size)) >= 0) printf(" [%s]%d", b, n);\n'
                '    printf("\\n");\n'
                '    fclose(f);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("  hello   world \\n\\tfoo\\n", 16);\n'
                '    run("abcdefghij kl", 5);\n'
                '    run("", 16);\n'
                '    run("   \\n  ", 16);\n'
                '    run("x", 16);\n'
                '    run("a b c", 2);\n'
                '    run("tail-no-space", 16);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Сначала пропустите пробельные; затем читайте до пробельного символа, сохраняя не более size − '
              '1 символа. Прочитанный разделитель можно вернуть ungetc.',
      'expected': ['size 16: [hello]5 [world]5 [foo]3',
                   'size 5: [abcd]4 [kl]2',
                   'size 16:',
                   'size 16:',
                   'size 16: [x]1',
                   'size 2: [a]1 [b]1 [c]1',
                   'size 16: [tail-no-space]13']},
     {'id': 'c8-fix-feof',
      'mode': 'c',
      'title': 'Исправьте: цикл по feof',
      'statement': 'sum_lines читает числа по одному на строку и суммирует их, а longest_line возвращает '
                   'длину самой длинной строки (без перевода строки). Обе функции используют цикл while '
                   '(!feof(f)) и обрабатывают последнюю строку дважды. Исправьте циклы: проверяйте результат '
                   'fgets.',
      'starter': '#include <stdio.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <string.h>\n'
                 '\n'
                 'int sum_lines(FILE *f) {\n'
                 '    int total = 0;\n'
                 '    char line[32] = "";\n'
                 '    while (!feof(f)) {\n'
                 '        fgets(line, sizeof line, f);\n'
                 '        total += atoi(line);\n'
                 '    }\n'
                 '    return total;\n'
                 '}\n'
                 '\n'
                 'size_t longest_line(FILE *f) {\n'
                 '    size_t best = 0;\n'
                 '    char line[64] = "";\n'
                 '    while (!feof(f)) {\n'
                 '        fgets(line, sizeof line, f);\n'
                 '        size_t n = strcspn(line, "\\n");\n'
                 '        if (n > best) best = n;\n'
                 '    }\n'
                 '    return best;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    const char *t[] = {"1\\n2\\n3\\n", "1\\n2\\n3", "10\\n", "", "7"};\n'
                '    for (int i = 0; i < 5; i++) {\n'
                '        FILE *f = from_str(t[i]);\n'
                '        int s = sum_lines(f);\n'
                '        fclose(f);\n'
                '        f = from_str(t[i]);\n'
                '        size_t l = longest_line(f);\n'
                '        fclose(f);\n'
                '        printf("%d %zu\\n", s, l);\n'
                '    }\n'
                '    FILE *f = from_str("abc\\nlongest line\\nxy\\nlast");\n'
                '    printf("%zu\\n", longest_line(f));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'while (fgets(line, sizeof line, f)) { … } — тело выполняется только если чтение удалось.',
      'expected': ['6 1', '6 1', '10 2', '0 0', '7 1', '12']},
     {'id': 'c8-fix-format',
      'mode': 'c',
      'title': 'Исправьте: спецификаторы printf',
      'statement': 'print_stats печатает «total=… n=… flags=… avg=… big=…» с неверными спецификаторами: для '
                   'long, size_t, unsigned char, double и long long выбраны не те, и вывод искажается (и это '
                   'неопределённое поведение). Подберите правильные спецификаторы: avg — с двумя знаками '
                   'после запятой; flags — как число (unsigned char).',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'void print_stats(FILE *out, long total, size_t n, unsigned char flags, double avg, long '
                 'long big) {\n'
                 '    fprintf(out, "total=%d n=%d flags=%c avg=%d big=%d\\n", total, n, flags, avg, big);\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    CAP_BEGIN(o);\n'
                '    print_stats(o, 5000000000L, 7, 200, 3.14159, -9000000000000LL);\n'
                '    print_stats(o, -1, 0, 0, 0.005, 1);\n'
                '    print_stats(o, 123456789012L, (size_t)1 << 40, 65, 1e6, 0);\n'
                '    fputs(CAP_END(o), stdout);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'long → %ld, size_t → %zu, unsigned char (приведите к unsigned) → %u, double → %.2f, long long '
              '→ %lld.',
      'expected': ['total=5000000000 n=7 flags=200 avg=3.14 big=-9000000000000',
                   'total=-1 n=0 flags=0 avg=0.01 big=1',
                   'total=123456789012 n=1099511627776 flags=65 avg=1000000.00 big=0']},
     {'id': 'c8-fix-sprintf',
      'mode': 'c',
      'title': 'Исправьте: sprintf без размера',
      'statement': 'make_label(out, size, name, id) должна записать в out метку «имя-NNNN» (id с четырьмя '
                   'цифрами с ведущими нулями) и вернуть 1, если метка поместилась целиком, иначе 0 (в out '
                   'при этом — усечённый текст с завершающим нулём). Сейчас функция использует sprintf и '
                   'портит память при длинных именах. Перепишите её на snprintf. Под AddressSanitizer.',
      'starter': '#include <stdio.h>\n'
                 '#include <string.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'int make_label(char *out, size_t size, const char *name, int id) {\n'
                 '    char tmp[16];\n'
                 '    sprintf(tmp, "%s-%04d", name, id);\n'
                 '    strcpy(out, tmp);\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void run(const char *name, int id, size_t size) {\n'
                '    char *buf = malloc(size);\n'
                '    int ok = make_label(buf, size, name, id);\n'
                '    printf("%d [%s]\\n", ok, buf);\n'
                '    free(buf);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("disk", 7, 16);\n'
                '    run("disk", 12345, 16);\n'
                '    run("a-very-long-device-name", 5, 16);\n'
                '    run("a-very-long-device-name", 5, 40);\n'
                '    run("x", 1, 7);\n'
                '    run("x", 1, 6);\n'
                '    run("x", 1, 1);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'snprintf возвращает длину полного результата: метка поместилась, если она меньше size.',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['1 [disk-0007]',
                   '1 [disk-12345]',
                   '0 [a-very-long-dev]',
                   '1 [a-very-long-device-name-0005]',
                   '1 [x-0001]',
                   '0 [x-000]',
                   '0 []']},
     {'id': 'c8-fix-scanf-width',
      'mode': 'c',
      'title': 'Исправьте: sscanf без ширины',
      'statement': 'parse_pair(s, *p) читает из строки два слова «ключ значение» в struct pair { char '
                   'key[8]; char val[8]; } и возвращает число прочитанных полей (0–2). Сейчас формат «%s %s» '
                   'без ширины переполняет поля при длинных словах. Исправьте формат, задав ширину каждого '
                   'поля: не больше 7 символов. Длинные слова при этом читаются кусками по 7 символов — это '
                   'нормальное поведение sscanf, главное, что память не портится. Под AddressSanitizer.',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'struct pair { char key[8]; char val[8]; };\n'
                 '\n'
                 'int parse_pair(const char *s, struct pair *p) {\n'
                 '    return sscanf(s, "%s %s", p->key, p->val);\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void run(const char *s) {\n'
                '    struct pair *p = calloc(1, sizeof *p);\n'
                '    int k = parse_pair(s, p);\n'
                '    printf("%d [%s] [%s]\\n", k, p->key, p->val);\n'
                '    free(p);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("name Anna");\n'
                '    run("short x");\n'
                '    run("averyverylongkey value");\n'
                '    run("k averyverylongvalue");\n'
                '    run("onlykey");\n'
                '    run("");\n'
                '    run("  spaced   out  ");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Формат «%7s %7s»: ширина — число символов без завершающего нуля (для char[8] — 7).',
      'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
      'expected': ['2 [name] [Anna]',
                   '2 [short] [x]',
                   '2 [averyve] [rylongk]',
                   '2 [k] [averyve]',
                   '1 [onlykey] []',
                   '-1 [] []',
                   '2 [spaced] [out]']},
     {'id': 'c8-fix-atoi',
      'mode': 'c',
      'title': 'Исправьте: порт через atoi',
      'statement': 'get_port(s) должна вернуть номер порта 1…65535 или −1 при ошибке. Допустима только '
                   'строка из десятичных цифр целиком (без пробелов, знака и посторонних символов); значения '
                   'вне диапазона и переполнение — ошибка. Сейчас используется atoi, которая принимает '
                   '«80abc», пробелы и переполняется. Перепишите функцию на strtol с полной проверкой.',
      'starter': '#include <stdlib.h>\n'
                 '\n'
                 'int get_port(const char *s) {\n'
                 '    int p = atoi(s);\n'
                 '    if (p < 1 || p > 65535) return -1;\n'
                 '    return p;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'int main(void) {\n'
                '    const char *t[] = {"80", "8080", "65535", "65536", "0", "1", "00022", "80abc", " 80", '
                '"80 ", "+80", "-5", "", "abc", "99999999999999999999", "4294967376", "1.5"};\n'
                '    for (size_t i = 0; i < sizeof t / sizeof t[0]; i++) printf("[%s] %d\\n", t[i], '
                'get_port(t[i]));\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Проверьте первый символ isdigit, затем strtol с errno и *end == 0, затем диапазон. '
              '«4294967376» — это 2^32 + 80: atoi/int дадут 80.',
      'expected': ['[80] 80',
                   '[8080] 8080',
                   '[65535] 65535',
                   '[65536] -1',
                   '[0] -1',
                   '[1] 1',
                   '[00022] 22',
                   '[80abc] -1',
                   '[ 80] -1',
                   '[80 ] -1',
                   '[+80] -1',
                   '[-5] -1',
                   '[] -1',
                   '[abc] -1',
                   '[99999999999999999999] -1',
                   '[4294967376] -1',
                   '[1.5] -1']},
     {'id': 'c8-fix-newline',
      'mode': 'c',
      'title': 'Исправьте: команды с символом перевода строки',
      'statement': 'run_commands(in, out) читает команды по одной в строке: «add N» (прибавить число к '
                   'итогу), «show» (напечатать «total=T»), «quit» (остановиться), пустая строка '
                   'игнорируется, остальное печатает «?». Функция возвращает число прочитанных строк '
                   '(включая quit). Из-за непрочитанного символа перевода строки команды show и quit никогда '
                   'не распознаются. Исправьте: уберите перевод строки (и возможный \\r) из line после '
                   'fgets.',
      'starter': '#include <stdio.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <string.h>\n'
                 '\n'
                 'int run_commands(FILE *in, FILE *out) {\n'
                 '    char line[64];\n'
                 '    int total = 0, lines = 0;\n'
                 '    while (fgets(line, sizeof line, in)) {\n'
                 '        lines++;\n'
                 '        if (strcmp(line, "quit") == 0) break;\n'
                 '        if (strncmp(line, "add ", 4) == 0) total += atoi(line + 4);\n'
                 '        else if (strcmp(line, "show") == 0) fprintf(out, "total=%d\\n", total);\n'
                 '        else if (line[0] != 0) fprintf(out, "?\\n");\n'
                 '    }\n'
                 '    return lines;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'static void run(const char *s) {\n'
                '    CAP_BEGIN(o);\n'
                '    FILE *in = from_str(s);\n'
                '    int n = run_commands(in, o);\n'
                '    char *r = CAP_END(o);\n'
                '    printf("%d:", n);\n'
                '    for (char *p = r; *p; p++) printf("%c", *p == \'\\n\' ? \'|\' : *p);\n'
                '    printf("\\n");\n'
                '    free(r);\n'
                '    fclose(in);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("add 5\\nadd 7\\nshow\\nquit\\nadd 100\\nshow\\n");\n'
                '    run("show\\n");\n'
                '    run("add 1\\r\\nshow\\r\\nquit\\r\\n");\n'
                '    run("\\n\\nfoo\\n\\nshow");\n'
                '    run("");\n'
                '    run("quit\\nshow\\n");\n'
                '    return 0;\n'
                '}\n',
      'hint': 'line[strcspn(line, "\\r\\n")] = 0; — сразу после fgets.',
      'expected': ['4:total=12|', '1:total=0|', '3:total=1|', '5:?|total=0|', '0:', '1:']},
     {'id': 'c8-buffered-writer',
      'mode': 'c',
      'title': 'Свой буферизованный писатель',
      'statement': 'struct bw { FILE *f; unsigned char buf[16]; size_t n; unsigned flushes; }. bw_init(w, '
                   'f). bw_write(w, data, len): если len ≥ 16 — сначала сбросить накопленное (если оно '
                   'есть), затем записать data прямо в f; если накопленное + len > 16 — сбросить накопленное '
                   'и положить data в буфер; иначе просто добавить в буфер. bw_flush(w): если в буфере есть '
                   'данные — записать их в f одним fwrite и обнулить n. Каждый вызов fwrite к f увеличивает '
                   'flushes на 1. Данные не должны теряться или переставляться.',
      'starter': '#include <stdio.h>\n'
                 '#include <stddef.h>\n'
                 '\n'
                 'struct bw { FILE *f; unsigned char buf[16]; size_t n; unsigned flushes; };\n'
                 '\n'
                 'void bw_init(struct bw *w, FILE *f) {}\n'
                 'void bw_write(struct bw *w, const void *data, size_t len) {}\n'
                 'void bw_flush(struct bw *w) {}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'int main(void) {\n'
                '    FILE *f = tmpfile();\n'
                '    struct bw w;\n'
                '    bw_init(&w, f);\n'
                '    bw_write(&w, "abcde", 5);\n'
                '    bw_write(&w, "fghij", 5);\n'
                '    printf("%zu %u\\n", w.n, w.flushes);\n'
                '    bw_write(&w, "klmnopq", 7);\n'
                '    printf("%zu %u\\n", w.n, w.flushes);\n'
                '    bw_write(&w, "0123456789ABCDEFGHIJ", 20);\n'
                '    printf("%zu %u\\n", w.n, w.flushes);\n'
                '    bw_write(&w, "xy", 2);\n'
                '    bw_write(&w, "", 0);\n'
                '    printf("%zu %u\\n", w.n, w.flushes);\n'
                '    bw_flush(&w);\n'
                '    bw_flush(&w);\n'
                '    printf("%zu %u\\n", w.n, w.flushes);\n'
                '    bw_write(&w, "0123456789abcdef", 16);\n'
                '    bw_write(&w, "z", 1);\n'
                '    bw_flush(&w);\n'
                '    printf("%zu %u\\n", w.n, w.flushes);\n'
                '    rewind(f);\n'
                '    char all[128] = {0};\n'
                '    size_t n = fread(all, 1, 127, f);\n'
                '    printf("%zu %s\\n", n, all);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Три случая в bw_write: большой кусок (сброс + прямая запись), кусок не помещается (сброс + '
              'буфер), помещается (в буфер).',
      'expected': ['10 0',
                   '7 1',
                   '0 3',
                   '2 3',
                   '0 4',
                   '0 6',
                   '56 abcdefghijklmnopq0123456789ABCDEFGHIJxy0123456789abcdefz']},
     {'id': 'c8-tail-lines',
      'mode': 'c',
      'title': 'tail: последние n строк',
      'statement': 'tail_lines(in, out, n) печатает последние n строк потока (n от 0 до 16) в исходном '
                   'порядке; каждая строка в выводе заканчивается переводом строки (даже последняя, если в '
                   'исходном тексте его не было). Хранить можно не больше 16 строк по 64 байта (строки '
                   'длиннее 63 символов в тестах не встречаются). Если строк меньше n — печатаются все.',
      'starter': '#include <stdio.h>\n\nvoid tail_lines(FILE *in, FILE *out, int n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'static void run(const char *s, int n) {\n'
                '    CAP_BEGIN(o);\n'
                '    FILE *in = from_str(s);\n'
                '    tail_lines(in, o, n);\n'
                '    char *r = CAP_END(o);\n'
                '    printf("n=%d:", n);\n'
                '    for (char *p = r; *p; p++) printf("%c", *p == \'\\n\' ? \'|\' : *p);\n'
                '    printf("\\n");\n'
                '    free(r);\n'
                '    fclose(in);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("1\\n2\\n3\\n4\\n5\\n", 2);\n'
                '    run("1\\n2\\n3\\n4\\n5\\n", 5);\n'
                '    run("1\\n2\\n3\\n4\\n5", 3);\n'
                '    run("1\\n2\\n", 10);\n'
                '    run("1\\n2\\n", 0);\n'
                '    run("", 3);\n'
                '    run("only", 1);\n'
                '    run("a\\n\\n\\nb\\n", 3);\n'
                '    char big[400] = "";\n'
                '    for (int i = 1; i <= 40; i++) sprintf(big + strlen(big), "L%d\\n", i);\n'
                '    run(big, 16);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Кольцевой буфер из n строк: строка номер k лежит в ячейке k % n; после чтения печатаем от '
              'count − n до count − 1.',
      'expected': ['n=2:4|5|',
                   'n=5:1|2|3|4|5|',
                   'n=3:3|4|5|',
                   'n=10:1|2|',
                   'n=0:',
                   'n=3:',
                   'n=1:only|',
                   'n=3:||b|',
                   'n=16:L25|L26|L27|L28|L29|L30|L31|L32|L33|L34|L35|L36|L37|L38|L39|L40|']},
     {'id': 'c8-grep-lite',
      'mode': 'c',
      'title': 'grep с флагами -v, -i, -n',
      'statement': 'grep_stream(in, out, pat, flags) печатает строки потока, содержащие подстроку pat. '
                   'flags: GREP_INVERT (1) — печатать строки, где pat нет; GREP_ICASE (2) — не различать '
                   'регистр ASCII; GREP_NUMBERS (4) — перед строкой печатать «номер:» (нумерация с 1 по всем '
                   'прочитанным строкам). Строка выводится без изменений, с переводом строки в конце. '
                   'Возвращает число напечатанных строк. Строки не длиннее 255 символов. Пустой pat '
                   'совпадает с любой строкой.',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 '#define GREP_INVERT 1\n'
                 '#define GREP_ICASE 2\n'
                 '#define GREP_NUMBERS 4\n'
                 '\n'
                 'int grep_stream(FILE *in, FILE *out, const char *pat, int flags) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'static void run(const char *pat, int flags) {\n'
                '    const char *txt = "Hello World\\nhello there\\nbye bye\\n\\nHELLO again\\nlast hello";\n'
                '    CAP_BEGIN(o);\n'
                '    FILE *in = from_str(txt);\n'
                '    int n = grep_stream(in, o, pat, flags);\n'
                '    char *r = CAP_END(o);\n'
                '    printf("%d (%d):", n, flags);\n'
                '    for (char *p = r; *p; p++) printf("%c", *p == \'\\n\' ? \'|\' : *p);\n'
                '    printf("\\n");\n'
                '    free(r);\n'
                '    fclose(in);\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("hello", 0);\n'
                '    run("hello", GREP_ICASE);\n'
                '    run("hello", GREP_INVERT);\n'
                '    run("hello", GREP_ICASE | GREP_INVERT);\n'
                '    run("hello", GREP_NUMBERS);\n'
                '    run("hello", GREP_ICASE | GREP_NUMBERS);\n'
                '    run("bye", GREP_NUMBERS | GREP_INVERT);\n'
                '    run("zzz", 0);\n'
                '    run("", 0);\n'
                '    run("", GREP_INVERT);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Для -i приведите к нижнему регистру и строку, и образец (копии, исходная строка остаётся для '
              'вывода). Номер строки увеличивайте для каждой прочитанной строки.',
      'expected': ['2 (0):hello there|last hello|',
                   '4 (2):Hello World|hello there|HELLO again|last hello|',
                   '4 (1):Hello World|bye bye||HELLO again|',
                   '2 (3):bye bye||',
                   '2 (4):2:hello there|6:last hello|',
                   '4 (6):1:Hello World|2:hello there|5:HELLO again|6:last hello|',
                   '5 (5):1:Hello World|2:hello there|4:|5:HELLO again|6:last hello|',
                   '0 (0):',
                   '6 (0):Hello World|hello there|bye bye||HELLO again|last hello|',
                   '0 (1):']},
     {'id': 'c8-parse-kv',
      'mode': 'c',
      'title': 'Разбор «ключ=значение; …»',
      'statement': 'struct kv { char key[8]; int val; }. parse_kv(s, out, max) → число разобранных пар. '
                   'Формат: «ключ=число», пары разделены точкой с запятой, пробелы вокруг ключа, знака '
                   'равенства, числа и точки с запятой допустимы; завершающая «;» допустима. Ключ — до 7 '
                   'символов из букв, цифр и «_». Разбор останавливается на первой неверной паре (остальное '
                   'игнорируется); результат — не больше max пар. Используйте sscanf с «%n».',
      'starter': '#include <stddef.h>\n'
                 '\n'
                 'struct kv { char key[8]; int val; };\n'
                 '\n'
                 'size_t parse_kv(const char *s, struct kv *out, size_t max) {\n'
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
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                'static void run(const char *s, size_t max) {\n'
                '    struct kv kv[6];\n'
                '    size_t n = parse_kv(s, kv, max);\n'
                '    printf("%zu:", n);\n'
                '    for (size_t i = 0; i < n; i++) printf(" %s=%d", kv[i].key, kv[i].val);\n'
                '    printf("\\n");\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("a=1; b=22;c = 333", 6);\n'
                '    run("x=-5;y=+7;", 6);\n'
                '    run("  speed = 100 ; hp=9 ;  ", 6);\n'
                '    run("a=1;b=;c=3", 6);\n'
                '    run("a=1 b=2", 6);\n'
                '    run("a=1;b=2;c=3;d=4", 2);\n'
                '    run("", 6);\n'
                '    run("verylongkey=1", 6);\n'
                '    run("k1=10;K_2=20;", 6);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Формат «%7[A-Za-z0-9_] = %d %n» (пробелы в формате — любые пробельные); после пары ожидайте '
              '«;» либо конец. %n записывает число использованных символов.',
      'expected': ['3: a=1 b=22 c=333',
                   '2: x=-5 y=7',
                   '2: speed=100 hp=9',
                   '1: a=1',
                   '1: a=1',
                   '2: a=1 b=2',
                   '0:',
                   '0:',
                   '2: k1=10 K_2=20']},
     {'id': 'c8-read-matrix',
      'mode': 'c',
      'title': 'Матрица целых из потока',
      'statement': 'read_matrix(in, m, max_rows, max_cols, *rows, *cols) читает строки с целыми числами '
                   '(разделитель — пробелы) в массив m построчно (row-major, шаг — реальное число столбцов). '
                   'Пустые (из пробелов) строки пропускаются. Результат: 0 — успех (rows, cols заданы); −1 — '
                   'в строке не число; −2 — строки разной длины; −3 — больше max_rows строк или max_cols '
                   'столбцов; −4 — нет ни одной строки. Строка не длиннее 255 символов; используйте strtol.',
      'starter': '#include <stdio.h>\n'
                 '\n'
                 'int read_matrix(FILE *in, int *m, int max_rows, int max_cols, int *rows, int *cols) {\n'
                 '    return -9;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                '#include <stdio.h>\n'
                '#include <stdint.h>\n'
                '#include <stddef.h>\n'
                '#include <string.h>\n'
                '#include <stdlib.h>\n'
                '#include <limits.h>\n'
                '#include <errno.h>\n'
                '#include <stdarg.h>\n'
                '#include <ctype.h>\n'
                '#include <math.h>\n'
                '\n'
                '\n'
                'static FILE *from_bytes(const void *p, size_t n) {\n'
                '    FILE *f = tmpfile();\n'
                '    if (n) fwrite(p, 1, n, f);\n'
                '    rewind(f);\n'
                '    return f;\n'
                '}\n'
                'static FILE *from_str(const char *s) { return from_bytes(s, strlen(s)); }\n'
                '#define CAP_BEGIN(fp) char *_cb_##fp = NULL; size_t _cs_##fp = 0; FILE *fp = '
                'open_memstream(&_cb_##fp, &_cs_##fp)\n'
                '#define CAP_END(fp) (fclose(fp), _cb_##fp)\n'
                'static void run(const char *s, int max_rows, int max_cols) {\n'
                '    int m[64] = {0}, rows = -1, cols = -1;\n'
                '    FILE *f = from_str(s);\n'
                '    int rc = read_matrix(f, m, max_rows, max_cols, &rows, &cols);\n'
                '    fclose(f);\n'
                '    printf("%d %d %d:", rc, rows, cols);\n'
                '    if (rc == 0)\n'
                '        for (int i = 0; i < rows * cols; i++) printf(" %d", m[i]);\n'
                '    printf("\\n");\n'
                '}\n'
                '\n'
                'int main(void) {\n'
                '    run("1 2 3\\n4 5 6\\n", 4, 4);\n'
                '    run("  1   2\\n\\n3 4\\n   \\n5 6", 4, 4);\n'
                '    run("7\\n8\\n9\\n", 4, 4);\n'
                '    run("1 2\\n3\\n", 4, 4);\n'
                '    run("1 2\\nx 4\\n", 4, 4);\n'
                '    run("1 2 3\\n4 5 6\\n7 8 9\\n", 2, 4);\n'
                '    run("1 2 3 4 5\\n", 4, 4);\n'
                '    run("\\n  \\n", 4, 4);\n'
                '    run("", 4, 4);\n'
                '    run("-1 +2\\n0x10 3\\n", 4, 4);\n'
                '    return 0;\n'
                '}\n',
      'hint': 'Столбцов заранее неизвестно, поэтому сначала читайте строку в локальный массив, считая числа; '
              'лишь потом копируйте в m с реальным шагом.',
      'expected': ['0 2 3: 1 2 3 4 5 6',
                   '0 3 2: 1 2 3 4 5 6',
                   '0 3 1: 7 8 9',
                   '-2 -1 -1:',
                   '-1 -1 -1:',
                   '-3 -1 -1:',
                   '-3 -1 -1:',
                   '-4 -1 -1:',
                   '-4 -1 -1:',
                   '-1 -1 -1:']}]}
