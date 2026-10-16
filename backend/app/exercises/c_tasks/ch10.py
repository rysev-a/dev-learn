"""Задачи книги «От assembler к языку C»: глава 10 (код компилируется gcc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {10: [{'id': 'c10-identifiers',
       'mode': 'c',
       'title': 'Идентификаторы C: допустимые, ключевые, зарезервированные',
       'statement': 'is_keyword(s) → 1 для ключевых слов C11 (auto break case char const continue default do '
                    'double else enum extern float for goto if inline int long register restrict return '
                    'short signed sizeof static struct switch typedef union unsigned void volatile while '
                    '_Alignas _Alignof _Atomic _Bool _Complex _Generic _Imaginary _Noreturn _Static_assert '
                    '_Thread_local). is_identifier(s) → 1, если s — допустимое имя (начинается с буквы или '
                    '«_», дальше буквы, цифры, «_»; ASCII) и не ключевое слово. is_reserved(s) → 1, если имя '
                    'зарезервировано для реализации: начинается с «__» или с «_» и заглавной буквы. '
                    'has_prefix(s, p) → 1, если s начинается с p и затем идёт «_» (например, list_init и '
                    'префикс list).',
       'starter': 'int is_keyword(const char *s) { return -1; }\n'
                  'int is_identifier(const char *s) { return -1; }\n'
                  'int is_reserved(const char *s) { return -1; }\n'
                  'int has_prefix(const char *s, const char *p) { return -1; }\n',
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
                 '    const char *t[] = {"x", "_x", "x1", "1x", "", "int", "Int", "_Bool", "a-b", "a b", '
                 '"while", "__builtin", "_Foo", "_foo", "__", "_", "list_init", "listinit", "a_"};\n'
                 '    for (size_t i = 0; i < sizeof t / sizeof t[0]; i++)\n'
                 '        printf("[%s] kw=%d id=%d res=%d lp=%d\\n", t[i], is_keyword(t[i]), '
                 'is_identifier(t[i]), is_reserved(t[i]), has_prefix(t[i], "list"));\n'
                 '    printf("%d %d %d\\n", has_prefix("list_", "list"), has_prefix("list", "list"), '
                 'has_prefix("a_b", ""));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': "Список ключевых слов — массив строк; зарезервированные: s[0] == '_' и (s[1] == '_' или "
               'заглавная буква).',
       'expected': ['[x] kw=0 id=1 res=0 lp=0',
                    '[_x] kw=0 id=1 res=0 lp=0',
                    '[x1] kw=0 id=1 res=0 lp=0',
                    '[1x] kw=0 id=0 res=0 lp=0',
                    '[] kw=0 id=0 res=0 lp=0',
                    '[int] kw=1 id=0 res=0 lp=0',
                    '[Int] kw=0 id=1 res=0 lp=0',
                    '[_Bool] kw=1 id=0 res=1 lp=0',
                    '[a-b] kw=0 id=0 res=0 lp=0',
                    '[a b] kw=0 id=0 res=0 lp=0',
                    '[while] kw=1 id=0 res=0 lp=0',
                    '[__builtin] kw=0 id=1 res=1 lp=0',
                    '[_Foo] kw=0 id=1 res=1 lp=0',
                    '[_foo] kw=0 id=1 res=0 lp=0',
                    '[__] kw=0 id=1 res=1 lp=0',
                    '[_] kw=0 id=1 res=0 lp=0',
                    '[list_init] kw=0 id=1 res=0 lp=1',
                    '[listinit] kw=0 id=1 res=0 lp=0',
                    '[a_] kw=0 id=1 res=0 lp=0',
                    '1 0 0']},
      {'id': 'c10-include-scan',
       'mode': 'c',
       'title': 'Поиск директив #include',
       'statement': 'struct inc { char name[32]; int system; }. scan_includes(src, out, max) → число '
                    'найденных директив #include <имя> (system = 1) и #include "имя" (system = 0) в порядке '
                    'появления (не больше max). Директива — строка, где перед # только пробелы/табуляции, '
                    'между # и include допустимы пробелы; закомментированные (// … и /* … */ в том числе '
                    'многострочные) не считаются; имя длиннее 31 символа пропускается; #include МАКРОС '
                    'игнорируется.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct inc { char name[32]; int system; };\n'
                  '\n'
                  'size_t scan_includes(const char *src, struct inc *out, size_t max) {\n'
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
                 '    const char *src =\n'
                 '        "#include <stdio.h>\\n"\n'
                 '        "  #  include \\"util.h\\"\\n"\n'
                 '        "// #include <commented.h>\\n"\n'
                 '        "/* #include <block.h> */\\n"\n'
                 '        "/*\\n#include <multi.h>\\n*/\\n"\n'
                 '        "#include <sys/types.h> // tail\\n"\n'
                 '        "#define X 1\\n"\n'
                 '        "#include MACRO\\n"\n'
                 '        "int x; /* a */ #include <notfirst.h>\\n"\n'
                 '        "#include \\"a_very_long_header_name_that_exceeds_the_limit.h\\"\\n"\n'
                 '        "\\t#include<tight.h>\\n"\n'
                 '        "#includes <bad.h>\\n"\n'
                 '        "#include \\"last.h\\"";\n'
                 '    struct inc inc[16];\n'
                 '    size_t n = scan_includes(src, inc, 16);\n'
                 '    printf("%zu\\n", n);\n'
                 '    for (size_t i = 0; i < n; i++) printf("%s %d\\n", inc[i].name, inc[i].system);\n'
                 '    printf("%zu %zu\\n", scan_includes(src, inc, 2), scan_includes("", inc, 4));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Сначала вырежьте комментарии (с запоминанием состояния «внутри /* … */» между строками), '
               'затем разберите строку: #, пробелы, include, пробелы, < или ".',
       'expected': ['5', 'stdio.h 1', 'util.h 0', 'sys/types.h 1', 'tight.h 1', 'last.h 0', '2 0']},
      {'id': 'c10-guard-check',
       'mode': 'c',
       'title': 'Проверка сторожа включения',
       'statement': 'check_guard(header, name) анализирует текст заголовка: пропускает пустые строки и '
                    'комментарии (// и /* */), первая директива должна быть «#pragma once» (→ 1, name '
                    'пустое) или «#ifndef ИМЯ» с «#define ИМЯ» следом (→ 0, имя копируется в name); иначе −1 '
                    '(сторожа нет); имена в #ifndef и #define разные → −2; последняя непустая строка не '
                    'начинается с #endif → −3. Директивы допускают пробелы после #.',
       'starter': 'int check_guard(const char *header, char *name) {\n    name[0] = 0;\n    return -9;\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static void t(const char *h) {\n'
                 '    char name[64] = "xx";\n'
                 '    int r = check_guard(h, name);\n'
                 '    printf("%d [%s]\\n", r, name);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t("#ifndef FOO_H\\n#define FOO_H\\nint f(void);\\n#endif");\n'
                 '    t("// comment\\n\\n/* block\\n   comment */\\n#ifndef BAR_H\\n# define BAR_H\\nint '
                 'g;\\n#endif /* BAR_H */\\n\\n");\n'
                 '    t("#pragma once\\nint x;\\n");\n'
                 '    t("int x;\\n");\n'
                 '    t("");\n'
                 '    t("#ifndef A_H\\n#define B_H\\n#endif\\n");\n'
                 '    t("#ifndef A_H\\n#define A_H\\nint x;\\n");\n'
                 '    t("#ifndef A_H\\nint x;\\n#endif\\n");\n'
                 '    t("  #  ifndef  SP_H  \\n  #define SP_H\\n#endif\\n");\n'
                 '    t("#ifndef X\\n#define X\\n#ifdef Y\\n#endif\\nint z;\\n#endif // end\\n");\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Приведите текст к списку значимых строк (без комментариев и пустых), затем проверьте первые '
               'две и последнюю.',
       'expected': ['0 [FOO_H]',
                    '0 [BAR_H]',
                    '1 []',
                    '-1 []',
                    '-1 []',
                    '-2 []',
                    '-3 []',
                    '-1 []',
                    '0 [SP_H]',
                    '0 [X]']},
      {'id': 'c10-decl-classify',
       'mode': 'c',
       'title': 'Классификация объявлений: определение или объявление, связывание',
       'statement': 'classify(line) разбирает однострочное объявление верхнего уровня и возвращает строку '
                    '«вид статус связывание»: вид — var, func, typedef, type; статус — def или decl; '
                    'связывание — external, internal или none. Примеры: «extern int x;» → «var decl '
                    'external»; «int x;» и «int x = 5;» → «var def external»; «static int x;» → «var def '
                    'internal»; «int f(void);» → «func decl external»; «int f(void) { return 0; }» → «func '
                    'def external»; «static int f(void);» → «func decl internal»; «static inline int g(void) '
                    '{ return 1; }» → «func def internal»; «typedef int T;» → «typedef decl none»; «struct '
                    'S;» → «type decl none»; «struct S { int a; };» → «type def none». Возвращаемую строку '
                    'хранит функция (статический буфер или литерал).',
       'starter': 'const char *classify(const char *line) {\n    return "";\n}\n',
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
                 '    const char *t[] = {\n'
                 '        "extern int x;", "int x;", "int x = 5;", "static int x;", "static int count = 3;", '
                 '"int f(void);", "int f(void) { return 0; }",\n'
                 '        "static int f(void);", "static inline int g(void) { return 1; }", "typedef int '
                 'T;", "struct S;", "struct S { int a; };",\n'
                 '        "const char *names[] = { \\"a\\", \\"b\\" };", "extern const char *names[];", '
                 '"static const int K = 7;", "void h(int a, int b);",\n'
                 '        "struct S s;", "unsigned long total;", "extern void run(void);",\n'
                 '    };\n'
                 '    for (size_t i = 0; i < sizeof t / sizeof t[0]; i++) printf("%s => %s\\n", t[i], '
                 'classify(t[i]));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Порядок разбора: typedef; struct/union/enum без скобок и без имени переменной; затем есть ли '
               '«(» (функция) и «{» (определение); static/extern — как слова.',
       'expected': ['extern int x; => var decl external',
                    'int x; => var def external',
                    'int x = 5; => var def external',
                    'static int x; => var def internal',
                    'static int count = 3; => var def internal',
                    'int f(void); => func decl external',
                    'int f(void) { return 0; } => func def external',
                    'static int f(void); => func decl internal',
                    'static inline int g(void) { return 1; } => func def internal',
                    'typedef int T; => typedef decl none',
                    'struct S; => type decl none',
                    'struct S { int a; }; => type def none',
                    'const char *names[] = { "a", "b" }; => var def external',
                    'extern const char *names[]; => var decl external',
                    'static const int K = 7; => var def internal',
                    'void h(int a, int b); => func decl external',
                    'struct S s; => var def external',
                    'unsigned long total; => var def external',
                    'extern void run(void); => func decl external']},
      {'id': 'c10-link-resolve',
       'mode': 'c',
       'title': 'Модель компоновщика: определения и ссылки',
       'statement': 'struct object { const char *name; const char *def[6]; int ndef; const char *undef[6]; '
                    'int nundef; } — объектный файл: определяемые и требуемые символы. link_objects(objs, n, '
                    'err, errsz) → 0, если программа собирается; иначе код ошибки и текст в err: −1 '
                    "«multiple definition of `X' in A and B» (A — первый определивший, B — второй; объекты и "
                    'символы просматриваются по порядку; ошибки определений проверяются раньше ссылок); −2 '
                    "«undefined reference to `X' in A» (первый по порядку объект, чей требуемый символ нигде "
                    'не определён); если ошибок нет, но символа main нет — −3 «undefined reference to '
                    "`main'».",
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct object { const char *name; const char *def[6]; int ndef; const char *undef[6]; int '
                  'nundef; };\n'
                  '\n'
                  'int link_objects(const struct object *objs, int n, char *err, size_t errsz) {\n'
                  '    err[0] = 0;\n'
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
                 'static void t(const char *label, const struct object *o, int n) {\n'
                 '    char err[128];\n'
                 '    int r = link_objects(o, n, err, sizeof err);\n'
                 '    printf("%s: %d %s\\n", label, r, err);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct object ok[] = {\n'
                 '        {"main.o", {"main"}, 1, {"add", "printf"}, 2},\n'
                 '        {"util.o", {"add", "sub"}, 2, {"helper"}, 1},\n'
                 '        {"help.o", {"helper"}, 1, {0}, 0},\n'
                 '        {"libc.o", {"printf"}, 1, {0}, 0},\n'
                 '    };\n'
                 '    t("ok", ok, 4);\n'
                 '    struct object dup[] = {\n'
                 '        {"a.o", {"main", "init"}, 2, {0}, 0},\n'
                 '        {"b.o", {"f", "init"}, 2, {0}, 0},\n'
                 '        {"c.o", {"f"}, 1, {0}, 0},\n'
                 '    };\n'
                 '    t("dup", dup, 3);\n'
                 '    struct object und[] = {\n'
                 '        {"a.o", {"main"}, 1, {"x", "y"}, 2},\n'
                 '        {"b.o", {"x"}, 1, {"z"}, 1},\n'
                 '    };\n'
                 '    t("und", und, 2);\n'
                 '    struct object nomain[] = {{"a.o", {"f"}, 1, {0}, 0}};\n'
                 '    t("nomain", nomain, 1);\n'
                 '    struct object both[] = {\n'
                 '        {"a.o", {"main"}, 1, {"q"}, 1},\n'
                 '        {"b.o", {"main"}, 1, {0}, 0},\n'
                 '    };\n'
                 '    t("both", both, 2);\n'
                 '    struct object self[] = {{"a.o", {"main", "f"}, 2, {"f"}, 1}};\n'
                 '    t("self", self, 1);\n'
                 '    t("empty", ok, 0);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Две проверки по порядку: попарно ищем совпадающие определения (второй найденный — вторая '
               'сторона), затем для каждой ссылки ищем определение среди всех объектов.',
       'expected': ['ok: 0',
                    "dup: -1 multiple definition of `init' in a.o and b.o",
                    "und: -2 undefined reference to `y' in a.o",
                    "nomain: -3 undefined reference to `main'",
                    "both: -1 multiple definition of `main' in a.o and b.o",
                    'self: 0',
                    "empty: -3 undefined reference to `main'"]},
      {'id': 'c10-archive-pull',
       'mode': 'c',
       'title': 'Извлечение объектов из статической библиотеки',
       'statement': 'struct object — как в модели компоновщика (def/undef-символы). pull_members(objs, n, '
                    'lib, m, group, order, *unresolved): множество неопределённых символов начинается с '
                    'требований objs (минус то, что они сами определяют). Библиотека просматривается слева '
                    'направо: член извлекается, если определяет хотя бы один сейчас неопределённый символ; '
                    'его определения закрывают символы, а его требования добавляются (если не определены). '
                    'При group = 0 просмотр один, при group = 1 — повторяется, пока что-то извлекается. '
                    'order[] — индексы извлечённых членов в порядке извлечения; результат — их число; '
                    '*unresolved — сколько символов осталось неопределёнными.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct object { const char *name; const char *def[6]; int ndef; const char *undef[6]; int '
                  'nundef; };\n'
                  '\n'
                  'int pull_members(const struct object *objs, int n, const struct object *lib, int m, int '
                  'group, int *order, int *unresolved) {\n'
                  '    *unresolved = -1;\n'
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
                 'static void t(const char *label, const struct object *o, int n, const struct object *lib, '
                 'int m, int group) {\n'
                 '    int order[16], unres = -1;\n'
                 '    int k = pull_members(o, n, lib, m, group, order, &unres);\n'
                 '    printf("%s g=%d: %d [", label, group, k);\n'
                 '    for (int i = 0; i < k; i++) printf("%s%s", i ? " " : "", lib[order[i]].name);\n'
                 '    printf("] unresolved=%d\\n", unres);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct object main_o[] = {{"main.o", {"main"}, 1, {"a", "x"}, 2}};\n'
                 '    struct object lib1[] = {\n'
                 '        {"a.o", {"a"}, 1, {"b"}, 1},\n'
                 '        {"b.o", {"b"}, 1, {0}, 0},\n'
                 '        {"unused.o", {"zzz"}, 1, {0}, 0},\n'
                 '        {"x.o", {"x"}, 1, {0}, 0},\n'
                 '    };\n'
                 '    t("fwd", main_o, 1, lib1, 4, 0);\n'
                 '    struct object lib2[] = {\n'
                 '        {"b.o", {"b"}, 1, {0}, 0},\n'
                 '        {"a.o", {"a"}, 1, {"b"}, 1},\n'
                 '        {"x.o", {"x"}, 1, {0}, 0},\n'
                 '    };\n'
                 '    t("back", main_o, 1, lib2, 3, 0);\n'
                 '    t("back", main_o, 1, lib2, 3, 1);\n'
                 '    struct object lib3[] = {\n'
                 '        {"p.o", {"p"}, 1, {"q"}, 1},\n'
                 '        {"q.o", {"q"}, 1, {"r"}, 1},\n'
                 '        {"r.o", {"r", "a"}, 2, {0}, 0},\n'
                 '        {"x.o", {"x"}, 1, {0}, 0},\n'
                 '    };\n'
                 '    t("chain", main_o, 1, lib3, 4, 0);\n'
                 '    struct object main2[] = {{"main.o", {"main"}, 1, {"p"}, 1}};\n'
                 '    t("chain2", main2, 1, lib3, 4, 0);\n'
                 '    t("chain2", main2, 1, lib3, 4, 1);\n'
                 '    struct object none[] = {{"m.o", {"main"}, 1, {0}, 0}};\n'
                 '    t("none", none, 1, lib1, 4, 1);\n'
                 '    struct object multi[] = {{"m.o", {"main"}, 1, {"k"}, 1}, {"n.o", {"f"}, 1, {"k", '
                 '"main"}, 2}};\n'
                 '    struct object lib4[] = {{"k.o", {"k", "k2"}, 2, {0}, 0}};\n'
                 '    t("multi", multi, 2, lib4, 1, 0);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Множества «определено» и «не определено» — маленькие массивы указателей; извлечение члена = '
               'определить его символы и потребовать его ссылки; цикл по библиотеке повторяйте, пока group и '
               'что-то извлекается.',
       'expected': ['fwd g=0: 3 [a.o b.o x.o] unresolved=0',
                    'back g=0: 2 [a.o x.o] unresolved=1',
                    'back g=1: 3 [a.o x.o b.o] unresolved=0',
                    'chain g=0: 2 [r.o x.o] unresolved=0',
                    'chain2 g=0: 3 [p.o q.o r.o] unresolved=0',
                    'chain2 g=1: 3 [p.o q.o r.o] unresolved=0',
                    'none g=1: 0 [] unresolved=0',
                    'multi g=0: 1 [k.o] unresolved=0']},
      {'id': 'c10-section-layout',
       'mode': 'c',
       'title': 'Раскладка секций по адресам',
       'statement': 'struct sect_obj { size_t text, data, bss, text_align, data_align, bss_align; } — '
                    'размеры секций объектного файла и выравнивания (степени двойки). layout_sections(o, n, '
                    'base, *L): все .text подряд, начиная с base (каждая секция выравнивается вверх до '
                    'своего выравнивания), затем .data, затем .bss; начало каждой области — адрес, '
                    'выровненный вверх до 16 после конца предыдущей (область .text начинается с base как '
                    'есть). В L записать text_addr[i], data_addr[i], bss_addr[i] (n ≤ 8) и общие концы '
                    'end_text, end_data, end_bss (адрес сразу за последней секцией области; у пустой области '
                    '— её начало). sym_addr(L, i, sect, off): адрес символа со смещением off в секции sect '
                    '(0 — text, 1 — data, 2 — bss) объекта i.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct sect_obj { size_t text, data, bss, text_align, data_align, bss_align; };\n'
                  'struct layout { size_t text_addr[8], data_addr[8], bss_addr[8]; size_t end_text, '
                  'end_data, end_bss; };\n'
                  '\n'
                  'void layout_sections(const struct sect_obj *o, int n, size_t base, struct layout *L) {}\n'
                  'size_t sym_addr(const struct layout *L, int i, int sect, size_t off) { return 0; }\n',
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
                 '    struct sect_obj o[] = {\n'
                 '        {100, 10, 20, 16, 4, 8},\n'
                 '        {33, 5, 0, 1, 1, 1},\n'
                 '        {64, 0, 40, 32, 1, 16},\n'
                 '    };\n'
                 '    struct layout L;\n'
                 '    layout_sections(o, 3, 0x10000, &L);\n'
                 '    for (int i = 0; i < 3; i++) printf("%d: %#zx %#zx %#zx\\n", i, L.text_addr[i], '
                 'L.data_addr[i], L.bss_addr[i]);\n'
                 '    printf("%#zx %#zx %#zx\\n", L.end_text, L.end_data, L.end_bss);\n'
                 '    printf("%#zx %#zx %#zx\\n", sym_addr(&L, 0, 0, 8), sym_addr(&L, 1, 1, 2), sym_addr(&L, '
                 '2, 2, 39));\n'
                 '    struct layout M;\n'
                 '    layout_sections(o, 0, 0x1003, &M);\n'
                 '    printf("%#zx %#zx %#zx\\n", M.end_text, M.end_data, M.end_bss);\n'
                 '    struct sect_obj p[] = {{1, 1, 1, 1, 1, 1}, {1, 1, 1, 8, 8, 8}};\n'
                 '    layout_sections(p, 2, 0x100, &L);\n'
                 '    printf("%#zx %#zx | %#zx %#zx | %#zx %#zx\\n", L.text_addr[0], L.text_addr[1], '
                 'L.data_addr[0], L.data_addr[1], L.bss_addr[0], L.bss_addr[1]);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Курсор cur: для каждой секции cur = up(cur, align); addr = cur; cur += size. Между областями '
               '— округление вверх до 16.',
       'expected': ['0: 0x10000 0x100e0 0x100f0',
                    '1: 0x10064 0x100ea 0x10104',
                    '2: 0x100a0 0x100ef 0x10110',
                    '0x100e0 0x100ef 0x10138',
                    '0x10008 0x100ec 0x10137',
                    '0x1003 0x1010 0x1010',
                    '0x100 0x108 | 0x110 0x118 | 0x120 0x128']},
      {'id': 'c10-relocations',
       'mode': 'c',
       'title': 'Применение релокаций',
       'statement': 'enum { R_ABS32, R_PC32, R_ABS64 }; struct reloc { size_t offset; int type; int64_t '
                    'sym_addr; int64_t addend; }. apply_relocs(image, size, base, r, n) записывает значения '
                    'прямо в образ (порядок байтов — little-endian): R_ABS32 — 4 байта S + A (должно '
                    'помещаться в uint32, иначе ошибка); R_PC32 — 4 байта S + A − P, где P = base + offset '
                    '(результат должен помещаться в int32); R_ABS64 — 8 байт S + A. Возврат: 0 — успех; −1 — '
                    'поле выходит за образ; −2 — переполнение поля. При ошибке остановиться (предыдущие '
                    'релокации остаются применёнными).',
       'starter': '#include <stddef.h>\n'
                  '#include <stdint.h>\n'
                  '\n'
                  'enum { R_ABS32, R_PC32, R_ABS64 };\n'
                  'struct reloc { size_t offset; int type; int64_t sym_addr; int64_t addend; };\n'
                  '\n'
                  'int apply_relocs(unsigned char *image, size_t size, uint64_t base, const struct reloc *r, '
                  'int n) {\n'
                  '    return -9;\n'
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
                 'static void dump(const unsigned char *p, size_t n) {\n'
                 '    for (size_t i = 0; i < n; i++) printf("%02x", p[i]);\n'
                 '    printf("\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    unsigned char img[24];\n'
                 '    memset(img, 0xEE, sizeof img);\n'
                 '    struct reloc r[] = {\n'
                 '        {0, R_ABS32, 0x400100, 0x10},\n'
                 '        {4, R_PC32, 0x400200, -4},\n'
                 '        {8, R_ABS64, 0x7fff00000000LL, 0x123},\n'
                 '        {16, R_PC32, 0x400000, 0},\n'
                 '    };\n'
                 '    int rc = apply_relocs(img, sizeof img, 0x400000, r, 4);\n'
                 '    printf("%d\\n", rc);\n'
                 '    dump(img, 24);\n'
                 '    unsigned char small[6] = {0};\n'
                 '    struct reloc e1[] = {{3, R_ABS32, 1, 0}};\n'
                 '    struct reloc e2[] = {{2, R_ABS32, 0x100000000LL, 0}};\n'
                 '    struct reloc e3[] = {{0, R_PC32, 0x7fffffffffLL, 0}};\n'
                 '    struct reloc e4[] = {{0, R_ABS32, 5, 0}, {1, R_ABS32, -1, 0}};\n'
                 '    struct reloc e5[] = {{2, R_ABS64, 1, 0}};\n'
                 '    printf("%d %d %d %d %d\\n", apply_relocs(small, 6, 0, e1, 1), apply_relocs(small, 6, '
                 '0, e2, 1), apply_relocs(small, 6, 0, e3, 1), apply_relocs(small, 6, 0, e4, 2), '
                 'apply_relocs(small, 6, 0, e5, 1));\n'
                 '    dump(small, 6);\n'
                 '    printf("%d\\n", apply_relocs(small, 6, 0, e1, 0));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Для PC32: значение = S + A − (base + offset). Проверьте границы образа до записи, затем '
               'диапазон поля; записывайте байты по одному (little-endian).',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0',
                    '10014000f801000023010000ff7f0000f0ffffffeeeeeeee',
                    '-1 -2 -2 -2 -1',
                    '050000000000',
                    '0']},
      {'id': 'c10-make-parse',
       'mode': 'c',
       'title': 'Разбор Makefile',
       'statement': 'struct rule { char target[32]; char deps[8][32]; int ndeps; char recipe[4][64]; int '
                    'nrecipe; }. parse_make(text, rules, max) → число правил. Поддерживается: комментарии (# '
                    'до конца строки; в строках команд они остаются), переменные «ИМЯ = значение» и '
                    'подстановки $(ИМЯ) / ${ИМЯ} в целях, зависимостях и командах (автоматические переменные '
                    '$@ $< $^ остаются как есть; $$ → $; неизвестная переменная → пусто); продолжение строки '
                    'обратной косой чертой в конце; правило «цель: зависимости» (одна цель); команды — '
                    'строки, начинающиеся с символа табуляции (табуляция отбрасывается), относятся к '
                    'последнему правилу. Пустые строки пропускаются.',
       'starter': 'struct rule { char target[32]; char deps[8][32]; int ndeps; char recipe[4][64]; int '
                  'nrecipe; };\n'
                  '\n'
                  'int parse_make(const char *text, struct rule *rules, int max) {\n'
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
                 'static void show(const struct rule *r, int n) {\n'
                 '    for (int i = 0; i < n; i++) {\n'
                 '        printf("%s <-", r[i].target);\n'
                 '        for (int d = 0; d < r[i].ndeps; d++) printf(" %s", r[i].deps[d]);\n'
                 '        printf(" | %d\\n", r[i].nrecipe);\n'
                 '        for (int c = 0; c < r[i].nrecipe; c++) printf("    [%s]\\n", r[i].recipe[c]);\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    const char *mk =\n'
                 '        "# сборка\\n"\n'
                 '        "CC = gcc\\n"\n'
                 '        "CFLAGS = -Wall -O2   # флаги\\n"\n'
                 '        "OBJ = main.o util.o\\n"\n'
                 '        "\\n"\n'
                 '        "app: $(OBJ)\\n"\n'
                 '        "\\t$(CC) $^ -o $@\\n"\n'
                 '        "\\n"\n'
                 '        "main.o: main.c util.h \\\\\\n"\n'
                 '        "    config.h\\n"\n'
                 '        "\\t$(CC) $(CFLAGS) -c main.c\\n"\n'
                 '        "\\techo cost $$5 # not a comment\\n"\n'
                 '        "util.o: util.c\\n"\n'
                 '        "\\t$(CC) -c util.c ${CFLAGS} $(NOPE)\\n"\n'
                 '        "clean:\\n"\n'
                 '        "\\trm -f $(OBJ) app\\n";\n'
                 '    struct rule r[8];\n'
                 '    int n = parse_make(mk, r, 8);\n'
                 '    printf("%d\\n", n);\n'
                 '    show(r, n);\n'
                 '    n = parse_make("a: b c\\n\\techo 1\\nb:\\n", r, 8);\n'
                 '    printf("%d\\n", n);\n'
                 '    show(r, n);\n'
                 '    n = parse_make("x:\\ny:\\nz:\\n", r, 2);\n'
                 '    printf("%d\\n", n);\n'
                 '    n = parse_make("", r, 8);\n'
                 '    printf("%d\\n", n);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Читайте логические строки (склеивая «\\\\» + перевод строки), команды отличайте по '
               'табуляции. Переменные — маленькая таблица имя→значение; подстановку делайте функцией expand.',
       'expected': ['4',
                    'app <- main.o util.o | 1',
                    '    [gcc $^ -o $@]',
                    'main.o <- main.c util.h config.h | 2',
                    '    [gcc -Wall -O2 -c main.c]',
                    '    [echo cost $5 # not a comment]',
                    'util.o <- util.c | 1',
                    '    [gcc -c util.c -Wall -O2 ]',
                    'clean <- | 1',
                    '    [rm -f main.o util.o app]',
                    '2',
                    'a <- b c | 1',
                    '    [echo 1]',
                    'b <- | 0',
                    '2',
                    '0']},
      {'id': 'c10-make-order',
       'mode': 'c',
       'title': 'make: порядок сборки по графу зависимостей',
       'statement': 'Для правил struct rule (как в разборе Makefile) build_order(rules, nrules, goal, exist, '
                    'nexist, order, max) строит порядок выполнения правил для цели goal, если пересобирать '
                    'нужно всё: сначала зависимости (в порядке перечисления), затем цель; каждая цель — один '
                    'раз. Зависимость, у которой нет правила, должна существовать как файл (список exist), '
                    'иначе результат −2. Цикл зависимостей → −1. Иначе результат — число целей в order (не '
                    'больше max, иначе −3). Цель goal без правила и не существующая → −2; если она '
                    'существует — результат 0.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct rule { char target[32]; char deps[8][32]; int ndeps; char recipe[4][64]; int '
                  'nrecipe; };\n'
                  '\n'
                  'int build_order(const struct rule *rules, int nrules, const char *goal, const char '
                  '**exist, int nexist, char order[][32], int max) {\n'
                  '    return -9;\n'
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
                 'static struct rule mk(const char *t, int nd, const char *d0, const char *d1, const char '
                 '*d2) {\n'
                 '    struct rule r;\n'
                 '    memset(&r, 0, sizeof r);\n'
                 '    strcpy(r.target, t);\n'
                 '    const char *ds[3] = {d0, d1, d2};\n'
                 '    for (int i = 0; i < nd; i++) strcpy(r.deps[r.ndeps++], ds[i]);\n'
                 '    return r;\n'
                 '}\n'
                 '\n'
                 'static void run(const char *label, const struct rule *r, int n, const char *goal, const '
                 'char **ex, int nex, int max) {\n'
                 '    char order[16][32];\n'
                 '    int k = build_order(r, n, goal, ex, nex, order, max);\n'
                 '    printf("%s: %d", label, k);\n'
                 '    for (int i = 0; i < k && i < 16; i++) printf(" %s", order[i]);\n'
                 '    printf("\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct rule r[] = {\n'
                 '        mk("app", 2, "main.o", "util.o", 0),\n'
                 '        mk("main.o", 2, "main.c", "util.h", 0),\n'
                 '        mk("util.o", 2, "util.c", "util.h", 0),\n'
                 '        mk("all", 2, "app", "docs", 0),\n'
                 '        mk("docs", 1, "util.h", 0, 0),\n'
                 '    };\n'
                 '    const char *ex[] = {"main.c", "util.c", "util.h"};\n'
                 '    run("app", r, 5, "app", ex, 3, 16);\n'
                 '    run("all", r, 5, "all", ex, 3, 16);\n'
                 '    run("nofile", r, 5, "app", ex, 2, 16);\n'
                 '    run("leaf", r, 5, "util.h", ex, 3, 16);\n'
                 '    run("missing", r, 5, "zzz", ex, 3, 16);\n'
                 '    run("small", r, 5, "all", ex, 3, 3);\n'
                 '    struct rule c[] = {mk("a", 1, "b", 0, 0), mk("b", 1, "c", 0, 0), mk("c", 1, "a", 0, '
                 '0)};\n'
                 '    run("cycle", c, 3, "a", ex, 3, 16);\n'
                 '    struct rule self[] = {mk("s", 1, "s", 0, 0)};\n'
                 '    run("self", self, 1, "s", ex, 3, 16);\n'
                 '    struct rule dia[] = {mk("top", 2, "l", "r", 0), mk("l", 1, "base", 0, 0), mk("r", 1, '
                 '"base", 0, 0), mk("base", 0, 0, 0, 0)};\n'
                 '    run("diamond", dia, 4, "top", ex, 3, 16);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Обход в глубину: пометка «в стеке» для поиска цикла и список «уже выполнено» для '
               'единственного вхождения; лист без правила проверяется по списку существующих файлов.',
       'expected': ['app: 3 main.o util.o app',
                    'all: 5 main.o util.o app docs all',
                    'nofile: -2',
                    'leaf: 0',
                    'missing: -2',
                    'small: -3',
                    'cycle: -1',
                    'self: -1',
                    'diamond: 4 base l r top']},
      {'id': 'c10-make-run',
       'mode': 'c',
       'title': 'Моделирование запуска make: что пересобирается',
       'statement': 'struct ftime { char name[32]; long t; } — время изменения файла (0 или отсутствие в '
                    'списке — файла нет). Правила — struct rule. make_run(rules, nrules, goal, files, '
                    '*nfiles, maxfiles, ran, maxran) моделирует make: для цели сначала собираются '
                    'зависимости (у которых есть правила), затем цель пересобирается, если файла нет, или он '
                    'старше (t меньше) любой зависимости, или у правила нет зависимостей и файла нет; цель, '
                    'указанная в правиле «.PHONY», пересобирается всегда и считается «новее» всех. '
                    'Пересборка = цель попадает в ran (по порядку выполнения) и её время становится «часами» '
                    '(часы стартуют с максимума времён в files и растут на 1 при каждой пересборке). '
                    'Зависимость без правила и без файла → результат −1. Возврат — число пересобранных.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct rule { char target[32]; char deps[8][32]; int ndeps; char recipe[4][64]; int '
                  'nrecipe; };\n'
                  'struct ftime { char name[32]; long t; };\n'
                  '\n'
                  'int make_run(const struct rule *rules, int nrules, const char *goal, struct ftime *files, '
                  'int *nfiles, int maxfiles, char ran[][32], int maxran) {\n'
                  '    return -9;\n'
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
                 'static struct rule mk(const char *t, int nd, const char *d0, const char *d1) {\n'
                 '    struct rule r;\n'
                 '    memset(&r, 0, sizeof r);\n'
                 '    strcpy(r.target, t);\n'
                 '    const char *ds[2] = {d0, d1};\n'
                 '    for (int i = 0; i < nd; i++) strcpy(r.deps[r.ndeps++], ds[i]);\n'
                 '    return r;\n'
                 '}\n'
                 '\n'
                 'static void set(struct ftime *f, int *n, const char *name, long t) {\n'
                 '    strcpy(f[*n].name, name);\n'
                 '    f[*n].t = t;\n'
                 '    (*n)++;\n'
                 '}\n'
                 '\n'
                 'static void run(const char *label, const struct rule *r, int nr, const char *goal, struct '
                 'ftime *f, int nf) {\n'
                 '    char ran[16][32];\n'
                 '    int k = make_run(r, nr, goal, f, &nf, 16, ran, 16);\n'
                 '    printf("%s: %d", label, k);\n'
                 '    for (int i = 0; i < k && i < 16; i++) printf(" %s", ran[i]);\n'
                 '    printf("\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct rule r[] = {\n'
                 '        mk("app", 2, "main.o", "util.o"),\n'
                 '        mk("main.o", 2, "main.c", "util.h"),\n'
                 '        mk("util.o", 2, "util.c", "util.h"),\n'
                 '        mk("clean", 0, 0, 0),\n'
                 '        mk(".PHONY", 1, "clean", 0),\n'
                 '    };\n'
                 '    struct ftime f[16];\n'
                 '    int n = 0;\n'
                 '    set(f, &n, "main.c", 10); set(f, &n, "util.c", 10); set(f, &n, "util.h", 10);\n'
                 '    run("fresh", r, 5, "app", f, n);\n'
                 '    n = 0;\n'
                 '    set(f, &n, "main.c", 10); set(f, &n, "util.c", 10); set(f, &n, "util.h", 10);\n'
                 '    set(f, &n, "main.o", 20); set(f, &n, "util.o", 21); set(f, &n, "app", 22);\n'
                 '    run("uptodate", r, 5, "app", f, n);\n'
                 '    f[2].t = 30;\n'
                 '    run("header", r, 5, "app", f, n);\n'
                 '    n = 0;\n'
                 '    set(f, &n, "main.c", 10); set(f, &n, "util.c", 25); set(f, &n, "util.h", 10);\n'
                 '    set(f, &n, "main.o", 20); set(f, &n, "util.o", 21); set(f, &n, "app", 22);\n'
                 '    run("util.c", r, 5, "app", f, n);\n'
                 '    n = 0;\n'
                 '    set(f, &n, "main.c", 10); set(f, &n, "util.c", 10); set(f, &n, "util.h", 10);\n'
                 '    set(f, &n, "main.o", 20); set(f, &n, "util.o", 21); set(f, &n, "app", 22);\n'
                 '    run("clean", r, 5, "clean", f, n);\n'
                 '    run("clean2", r, 5, "clean", f, n);\n'
                 '    n = 0;\n'
                 '    set(f, &n, "main.c", 10); set(f, &n, "util.h", 10);\n'
                 '    run("nofile", r, 5, "app", f, n);\n'
                 '    n = 0;\n'
                 '    set(f, &n, "main.c", 10); set(f, &n, "util.c", 10); set(f, &n, "util.h", 10);\n'
                 '    set(f, &n, "main.o", 10); set(f, &n, "util.o", 10); set(f, &n, "app", 10);\n'
                 '    run("equal", r, 5, "app", f, n);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Рекурсивная функция возвращает «цель стала новее»: пересборка или phony-цель. Цель '
               'пересобирается, если файла нет, он старше самой новой зависимости или любая зависимость '
               'стала новее.',
       'expected': ['fresh: 3 main.o util.o app',
                    'uptodate: 0',
                    'header: 3 main.o util.o app',
                    'util.c: 2 util.o app',
                    'clean: 1 clean',
                    'clean2: 1 clean',
                    'nofile: -1',
                    'equal: 0']},
      {'id': 'c10-make-recipe',
       'mode': 'c',
       'title': 'Шаблоны % и автоматические переменные',
       'statement': 'match_pattern(pat, name, stem) → 1, если имя подходит под шаблон с одним «%» (например, '
                    '«%.o» и «build/%.o»), и записывает в stem то, что скрывается за «%»; иначе 0. '
                    'subst_pattern(pat, stem, out) подставляет stem вместо «%». expand_recipe(recipe, '
                    'target, deps, ndeps, stem, out, cap) подставляет $@ (цель), $< (первая зависимость; нет '
                    'зависимостей → пусто), $^ (все зависимости без повторов, через пробел), $+ (все, с '
                    'повторами), $* (stem), $$ → $; прочие «$x» остаются как есть. Возвращает длину '
                    'результата или −1, если он не помещается в cap (с учётом завершающего нуля).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int match_pattern(const char *pat, const char *name, char *stem) { return -1; }\n'
                  'void subst_pattern(const char *pat, const char *stem, char *out) { out[0] = 0; }\n'
                  'int expand_recipe(const char *recipe, const char *target, const char deps[][32], int '
                  'ndeps, const char *stem, char *out, size_t cap) { return -9; }\n',
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
                 '    char stem[32];\n'
                 '    const char *pats[] = {"%.o", "build/%.o", "lib%.a", "%", "main.o", "a%b"};\n'
                 '    const char *names[] = {"main.o", "build/util.o", "libfoo.a", "xyz", "main.o", "ab"};\n'
                 '    for (int i = 0; i < 6; i++) {\n'
                 '        int m = match_pattern(pats[i], names[i], stem);\n'
                 '        printf("%s ~ %s: %d [%s]\\n", pats[i], names[i], m, m ? stem : "-");\n'
                 '    }\n'
                 '    printf("%d %d %d\\n", match_pattern("%.o", "main.c", stem), match_pattern("build/%.o", '
                 '"main.o", stem), match_pattern("a%b", "a", stem));\n'
                 '    char out[64];\n'
                 '    subst_pattern("%.c", "util", out);\n'
                 '    printf("%s\\n", out);\n'
                 '    subst_pattern("src/%/%.c", "x", out);\n'
                 '    printf("%s\\n", out);\n'
                 '    char deps[3][32] = {"main.c", "util.h", "main.c"};\n'
                 '    char buf[128];\n'
                 '    int n = expand_recipe("$(CC) -c $< -o $@ # $* $$HOME $x", "main.o", deps, 3, "main", '
                 'buf, sizeof buf);\n'
                 '    printf("%d [%s]\\n", n, buf);\n'
                 '    n = expand_recipe("link $^ | $+", "app", deps, 3, "", buf, sizeof buf);\n'
                 '    printf("%d [%s]\\n", n, buf);\n'
                 '    n = expand_recipe("echo $< $^", "t", deps, 0, "", buf, sizeof buf);\n'
                 '    printf("%d [%s]\\n", n, buf);\n'
                 '    char tiny[8];\n'
                 '    n = expand_recipe("gcc -c $< -o $@", "main.o", deps, 1, "main", tiny, sizeof tiny);\n'
                 '    printf("%d\\n", n);\n'
                 '    n = expand_recipe("exactly", "t", deps, 0, "", tiny, sizeof tiny);\n'
                 '    printf("%d [%s]\\n", n, tiny);\n'
                 '    n = expand_recipe("exactly8", "t", deps, 0, "", tiny, sizeof tiny);\n'
                 '    printf("%d\\n", n);\n'
                 '    n = expand_recipe("end$", "t", deps, 0, "", buf, sizeof buf);\n'
                 '    printf("%d [%s]\\n", n, buf);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'match_pattern: до «%» — префикс, после — суффикс; имя должно начинаться с префикса и '
               'кончаться суффиксом, середина — stem. В expand_recipe аккуратно считайте место: последний '
               'байт — под ноль.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['%.o ~ main.o: 1 [main]',
                    'build/%.o ~ build/util.o: 1 [util]',
                    'lib%.a ~ libfoo.a: 1 [foo]',
                    '% ~ xyz: 1 [xyz]',
                    'main.o ~ main.o: 1 []',
                    'a%b ~ ab: 1 []',
                    '0 0 0',
                    'util.c',
                    'src/x/x.c',
                    '41 [$(CC) -c main.c -o main.o # main $HOME $x]',
                    '41 [link main.c util.h | main.c util.h main.c]',
                    '6 [echo  ]',
                    '-1',
                    '7 [exactly]',
                    '-1',
                    '4 [end$]']},
      {'id': 'c10-make-vars',
       'mode': 'c',
       'title': 'Переменные make: =, :=, += и подстановки',
       'statement': 'struct vars (до 16 переменных; имя ≤ 15, значение ≤ 127 символов). var_set(v, line) '
                    'обрабатывает строку «ИМЯ = знач» (рекурсивная: значение хранится как текст и '
                    'подставляется при использовании), «ИМЯ := знач» (простая: подстановки выполняются '
                    'сразу), «ИМЯ += знач» (дописать через пробел; тип переменной сохраняется, а если её не '
                    'было — создаётся рекурсивной), «ИМЯ ?= знач» (задать, только если не определена). '
                    'Пробелы вокруг оператора и в концах значения отбрасываются. Возвращает 0 или −1 '
                    '(неверная строка/нет места). var_expand(v, s, out, cap) подставляет $(X) и ${X} '
                    '(рекурсивно), «$$» → «$»; неизвестная → пусто; зацикливание (A = $(B), B = $(A)) → −1; '
                    'результат не помещается → −2; иначе длина результата.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct vars { char name[16][16]; char val[16][128]; int simple[16]; int n; };\n'
                  '\n'
                  'void vars_init(struct vars *v) { v->n = 0; }\n'
                  'int var_set(struct vars *v, const char *line) { return -9; }\n'
                  'int var_expand(const struct vars *v, const char *s, char *out, size_t cap) { return -9; '
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
                 'static void ex(const struct vars *v, const char *s) {\n'
                 '    char out[64];\n'
                 '    int n = var_expand(v, s, out, sizeof out);\n'
                 '    printf("%d [%s]\\n", n, n >= 0 ? out : "-");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct vars v;\n'
                 '    vars_init(&v);\n'
                 '    int r1 = var_set(&v, "CC = gcc");\n'
                 '    int r2 = var_set(&v, "CFLAGS := -O2 -Wall");\n'
                 '    int r3 = var_set(&v, "OBJ = main.o");\n'
                 '    int r4 = var_set(&v, "OBJ += util.o");\n'
                 '    int r5 = var_set(&v, "NOPE");\n'
                 '    printf("%d %d %d %d %d\\n", r1, r2, r3, r4, r5);\n'
                 '    ex(&v, "$(CC) $(CFLAGS) $(OBJ) -o app");\n'
                 '    printf("%d\\n", var_set(&v, "CFLAGS += -g"));\n'
                 '    ex(&v, "${CFLAGS}|$(MISSING)|$$HOME");\n'
                 '    int q1 = var_set(&v, "CC ?= clang");\n'
                 '    int q2 = var_set(&v, "AR ?= ar");\n'
                 '    printf("%d %d\\n", q1, q2);\n'
                 '    ex(&v, "$(CC) $(AR)");\n'
                 '    printf("%d\\n", var_set(&v, "LATE = $(CC)"));\n'
                 '    printf("%d\\n", var_set(&v, "SNAP := $(CC)"));\n'
                 '    printf("%d\\n", var_set(&v, "CC = tcc"));\n'
                 '    ex(&v, "$(LATE) $(SNAP)");\n'
                 '    var_set(&v, "A = $(B)");\n'
                 '    var_set(&v, "B = $(A)");\n'
                 '    ex(&v, "x $(A) y");\n'
                 '    var_set(&v, "SELF = $(SELF) more");\n'
                 '    ex(&v, "$(SELF)");\n'
                 '    var_set(&v, "LONG = 0123456789012345678901234567890123456789");\n'
                 '    ex(&v, "$(LONG)$(LONG)");\n'
                 '    ex(&v, "$(UNCLOSED");\n'
                 '    ex(&v, "");\n'
                 '    var_set(&v, "  SPACED   :=   a   b  ");\n'
                 '    ex(&v, "[$(SPACED)]");\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Храните для каждой переменной флаг «простая». При использовании рекурсивной — раскрывайте её '
               'значение с ограничением глубины (зацикливание → −1). := раскрывает значение сразу.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 0 0 0 -1',
                    '34 [gcc -O2 -Wall main.o util.o -o app]',
                    '0',
                    '19 [-O2 -Wall -g||$HOME]',
                    '0 0',
                    '6 [gcc ar]',
                    '0',
                    '0',
                    '0',
                    '7 [tcc gcc]',
                    '-1 [-]',
                    '-1 [-]',
                    '-2 [-]',
                    '-1 [-]',
                    '0 []',
                    '7 [[a   b]]']},
      {'id': 'c10-dep-file',
       'mode': 'c',
       'title': 'Файлы зависимостей .d (gcc -MMD)',
       'statement': 'parse_dep(text, target, deps, max) разбирает вывод gcc -MMD: «build/main.o: src/main.c '
                    '\\\\⏎ include/util.h include/config.h⏎»; продолжения строк с обратной косой чертой '
                    'склеиваются; записывает цель в target (без двоеточия) и зависимости в deps[][48] (до '
                    'max); возвращает их число или −1 при отсутствии двоеточия. Строки после первой '
                    '(фиктивные цели «util.h:» от -MP) игнорируются. rebuild_set(dep_texts, n, changed, out, '
                    'max) → какие цели нужно пересобрать, если изменился файл changed (он присутствует в '
                    'списке зависимостей цели), в порядке входных данных; возвращает их число.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int parse_dep(const char *text, char *target, char deps[][48], int max) { return -9; }\n'
                  'int rebuild_set(const char *const *dep_texts, int n, const char *changed, char out[][48], '
                  'int max) { return -9; }\n',
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
                 '    char target[48], deps[8][48];\n'
                 '    const char *d1 = "build/main.o: src/main.c \\\\\\n include/util.h   '
                 'include/config.h\\n\\ninclude/util.h:\\n\\ninclude/config.h:\\n";\n'
                 '    int n = parse_dep(d1, target, deps, 8);\n'
                 '    printf("%d %s |", n, target);\n'
                 '    for (int i = 0; i < n; i++) printf(" %s", deps[i]);\n'
                 '    printf("\\n");\n'
                 '    n = parse_dep("a.o: a.c", target, deps, 8);\n'
                 '    printf("%d %s | %s\\n", n, target, deps[0]);\n'
                 '    n = parse_dep("a.o:\\n", target, deps, 8);\n'
                 '    printf("%d %s\\n", n, target);\n'
                 '    n = parse_dep("no colon here\\n", target, deps, 8);\n'
                 '    printf("%d\\n", n);\n'
                 '    n = parse_dep("x.o: 1.h 2.h 3.h 4.h \\\\\\n 5.h\\n", target, deps, 3);\n'
                 '    printf("%d %s %s\\n", n, target, deps[2]);\n'
                 '    const char *texts[] = {\n'
                 '        "build/main.o: src/main.c include/util.h include/config.h\\n",\n'
                 '        "build/util.o: src/util.c include/util.h\\n",\n'
                 '        "build/io.o: src/io.c \\\\\\n  include/io.h\\n",\n'
                 '        "build/cfg.o: src/cfg.c include/config.h\\n",\n'
                 '    };\n'
                 '    char out[8][48];\n'
                 '    const char *ch[] = {"include/util.h", "include/config.h", "src/io.c", "include/io.h", '
                 '"nothing.h"};\n'
                 '    for (int i = 0; i < 5; i++) {\n'
                 '        int k = rebuild_set(texts, 4, ch[i], out, 8);\n'
                 '        printf("%s:", ch[i]);\n'
                 '        for (int j = 0; j < k; j++) printf(" %s", out[j]);\n'
                 '        printf("\\n");\n'
                 '    }\n'
                 '    printf("%d\\n", rebuild_set(texts, 4, "include/util.h", out, 1));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Склейте логическую строку (обратная косая + перевод строки → пробел), отделите цель по '
               'двоеточию, остальное разбейте по пробелам.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['3 build/main.o | src/main.c include/util.h include/config.h',
                    '1 a.o | a.c',
                    '0 a.o',
                    '-1',
                    '3 x.o 3.h',
                    'include/util.h: build/main.o build/util.o',
                    'include/config.h: build/main.o build/cfg.o',
                    'src/io.c: build/io.o',
                    'include/io.h: build/io.o',
                    'nothing.h:',
                    '1']},
      {'id': 'c10-include-graph',
       'mode': 'c',
       'title': 'Граф включений: что пересобирать при правке заголовка',
       'statement': 'struct file { const char *name; const char *inc[6]; int ninc; } — файл и то, что он '
                    'включает напрямую. affected(f, n, changed, out, max) → список файлов, которые зависят '
                    'от changed прямо или косвенно (включая цепочки заголовков); только трансляции — имена, '
                    'оканчивающиеся на «.c»; порядок — как во входном списке; changed сам не входит; '
                    'возвращает число (не больше max). has_cycle(f, n) → 1, если во включениях есть цикл '
                    '(учитываются только файлы из списка). include_depth(f, n, name) → максимальная глубина '
                    'цепочки включений от name (файл без включений — 0); при цикле — −1.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct file { const char *name; const char *inc[6]; int ninc; };\n'
                  '\n'
                  'int affected(const struct file *f, int n, const char *changed, const char **out, int max) '
                  '{ return -9; }\n'
                  'int has_cycle(const struct file *f, int n) { return -9; }\n'
                  'int include_depth(const struct file *f, int n, const char *name) { return -9; }\n',
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
                 '    struct file f[] = {\n'
                 '        {"main.c", {"app.h", "stdio.h"}, 2},\n'
                 '        {"util.c", {"util.h"}, 1},\n'
                 '        {"io.c", {"io.h", "config.h"}, 2},\n'
                 '        {"app.h", {"util.h", "types.h"}, 2},\n'
                 '        {"util.h", {"types.h"}, 1},\n'
                 '        {"io.h", {"types.h"}, 1},\n'
                 '        {"types.h", {0}, 0},\n'
                 '        {"config.h", {0}, 0},\n'
                 '        {"test.c", {"util.c"}, 1},\n'
                 '    };\n'
                 '    const char *ch[] = {"types.h", "util.h", "app.h", "config.h", "main.c", "stdio.h", '
                 '"nothing"};\n'
                 '    const char *out[10];\n'
                 '    for (int i = 0; i < 7; i++) {\n'
                 '        int k = affected(f, 9, ch[i], out, 10);\n'
                 '        printf("%s:", ch[i]);\n'
                 '        for (int j = 0; j < k; j++) printf(" %s", out[j]);\n'
                 '        printf("\\n");\n'
                 '    }\n'
                 '    printf("%d\\n", affected(f, 9, "types.h", out, 2));\n'
                 '    printf("%d\\n", has_cycle(f, 9));\n'
                 '    printf("%d %d %d %d %d\\n", include_depth(f, 9, "main.c"), include_depth(f, 9, '
                 '"types.h"), include_depth(f, 9, "app.h"), include_depth(f, 9, "io.c"), include_depth(f, 9, '
                 '"unknown"));\n'
                 '    struct file c[] = {\n'
                 '        {"a.h", {"b.h"}, 1},\n'
                 '        {"b.h", {"c.h"}, 1},\n'
                 '        {"c.h", {"a.h"}, 1},\n'
                 '        {"x.c", {"a.h"}, 1},\n'
                 '    };\n'
                 '    printf("%d %d %d\\n", has_cycle(c, 4), include_depth(c, 4, "x.c"), include_depth(c, 4, '
                 '"c.h"));\n'
                 '    const char *o2[4];\n'
                 '    printf("%d\\n", affected(c, 4, "b.h", o2, 4));\n'
                 '    struct file self[] = {{"s.h", {"s.h"}, 1}};\n'
                 '    printf("%d\\n", has_cycle(self, 1));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Достижимость в графе включений поиском в глубину с пометками посещённых; для цикла — три '
               'цвета (белый, серый, чёрный).',
       'expected': ['types.h: main.c util.c io.c test.c',
                    'util.h: main.c util.c test.c',
                    'app.h: main.c',
                    'config.h: io.c',
                    'main.c:',
                    'stdio.h: main.c',
                    'nothing:',
                    '2',
                    '0',
                    '3 0 2 2 0',
                    '1 -1 -1',
                    '1',
                    '1']},
      {'id': 'c10-cmdline-split',
       'mode': 'c',
       'title': 'Разбор командной строки с кавычками и экранированием',
       'statement': 'split_args(cmd, buf, cap, argv, max) разбирает строку как оболочка: пробелы разделяют '
                    'аргументы; одинарные кавычки сохраняют всё буквально; в двойных кавычках обратная косая '
                    'экранирует только \\" \\\\ и \\$; вне кавычек обратная косая экранирует любой следующий '
                    'символ; пустые кавычки дают пустой аргумент. Аргументы записываются в buf подряд, '
                    'каждый с завершающим нулём; argv[i] указывают в buf; возврат — argc, −1 — незакрытая '
                    'кавычка или обратная косая в конце, −2 — не помещается в cap или в max. quote_arg(s, '
                    'out, cap) → строка для вставки в командную строку: если все символы из набора '
                    "[A-Za-z0-9_@%+=:,./-] — как есть, пустая → '', иначе в одинарных кавычках (внутренний ' "
                    "заменяется на '\\'' ); возвращает длину или −1.",
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int split_args(const char *cmd, char *buf, size_t cap, char **argv, int max) { return -9; '
                  '}\n'
                  'int quote_arg(const char *s, char *out, size_t cap) { return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static void t(const char *cmd) {\n'
                 '    char buf[128];\n'
                 '    char *argv[16];\n'
                 '    int n = split_args(cmd, buf, sizeof buf, argv, 16);\n'
                 '    printf("%d:", n);\n'
                 '    for (int i = 0; i < n; i++) printf(" <%s>", argv[i]);\n'
                 '    printf("\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t("gcc -c main.c -o main.o");\n'
                 '    t("  gcc   -Wall\\t-O2  ");\n'
                 '    t("echo \'hello  world\' \\"a b\\" c\\\\ d");\n'
                 '    t("cc -DNAME=\\"my app\\" -DX=\'1 2\' -o \'out dir/app\'");\n'
                 '    t("echo \\"quote \\\\\\" and \\\\\\\\ and \\\\$HOME and \\\\n\\"");\n'
                 '    t("empty \'\' \\"\\" x");\n'
                 '    t("glue\'a b\'\\"c d\\"e");\n'
                 '    t("");\n'
                 '    t("   ");\n'
                 '    t("unclosed \'single");\n'
                 '    t("unclosed \\"double");\n'
                 '    t("trailing\\\\");\n'
                 '    t("a\\\\ b\\\\\'c");\n'
                 '    char buf[8];\n'
                 '    char *argv[4];\n'
                 '    printf("%d %d\\n", split_args("abc def", buf, sizeof buf, argv, 4), split_args("abc '
                 'defgh", buf, sizeof buf, argv, 4));\n'
                 '    printf("%d\\n", split_args("a b c d e", buf, 32, argv, 4));\n'
                 '    char q[64];\n'
                 '    const char *s[] = {"main.c", "a b", "it\'s", "", "x=1,y:2/z-3", "$HOME", "semi;colon", '
                 '"tab\\there"};\n'
                 '    for (size_t i = 0; i < sizeof s / sizeof s[0]; i++) {\n'
                 '        int n = quote_arg(s[i], q, sizeof q);\n'
                 '        printf("%d %s\\n", n, q);\n'
                 '    }\n'
                 '    printf("%d %d\\n", quote_arg("abcdef", q, 6), quote_arg("abcde", q, 6));\n'
                 '    printf("%d\\n", quote_arg("a b", q, 4));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Состояния: вне кавычек, в одинарных, в двойных; обратная косая вне кавычек берёт следующий '
               'символ буквально. Следите за cap при каждой записи.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['5: <gcc> <-c> <main.c> <-o> <main.o>',
                    '3: <gcc> <-Wall> <-O2>',
                    '4: <echo> <hello  world> <a b> <c d>',
                    '5: <cc> <-DNAME=my app> <-DX=1 2> <-o> <out dir/app>',
                    '2: <echo> <quote " and \\ and $HOME and \\n>',
                    '4: <empty> <> <> <x>',
                    '1: <gluea bc de>',
                    '0:',
                    '0:',
                    '-1:',
                    '-1:',
                    '-1:',
                    "1: <a b'c>",
                    '2 -2',
                    '-2',
                    '6 main.c',
                    "5 'a b'",
                    "9 'it'\\''s'",
                    "2 ''",
                    '11 x=1,y:2/z-3',
                    "7 '$HOME'",
                    "12 'semi;colon'",
                    "10 'tab\there'",
                    '-1 5',
                    '-1']},
      {'id': 'c10-build-cmd',
       'mode': 'c',
       'title': 'Сборка командной строки компилятора',
       'statement': 'struct build { const char *cc, *std; int opt; int warn; const char *defs[4]; int ndefs; '
                    'const char *incs[4]; int nincs; const char *srcs[4]; int nsrcs; const char *out; const '
                    'char *libdirs[2]; int nlibdirs; const char *libs[3]; int nlibs; }. build_cmd(b, out, '
                    'cap) → строка: «cc -std=STD -ON -Wall -Wextra -DX -Iпуть исходники -o out -Lдир -lлиб» '
                    '(части опускаются, если не заданы; opt < 0 — без -O, иначе -O<opt>; warn ≠ 0 — -Wall '
                    '-Wextra). Порядок строгий: компилятор, std, оптимизация, предупреждения, -D, -I, '
                    'исходники, «-o out», -L, -l (библиотеки после исходников). Любой аргумент с пробелом, '
                    "кавычкой или другими спецсимволами заключается в одинарные кавычки (внутренний ' → "
                    "'\\'' ). Возврат — длина или −1, если не помещается в cap.",
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct build { const char *cc, *std; int opt; int warn; const char *defs[4]; int ndefs; '
                  'const char *incs[4]; int nincs; const char *srcs[4]; int nsrcs; const char *out; const '
                  'char *libdirs[2]; int nlibdirs; const char *libs[3]; int nlibs; };\n'
                  '\n'
                  'int build_cmd(const struct build *b, char *out, size_t cap) { return -9; }\n',
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
                 '    char out[256];\n'
                 '    struct build b = {"gcc", "c11", 2, 1, {"DEBUG", "NAME=\\"my app\\""}, 2, {"include", '
                 '"third party/inc"}, 2, {"main.c", "util.c"}, 2, "bin/app", {"lib"}, 1, {"m", "pthread"}, '
                 '2};\n'
                 '    int n = build_cmd(&b, out, sizeof out);\n'
                 '    printf("%d %s\\n", n, out);\n'
                 '    struct build m = {"cc", 0, -1, 0, {0}, 0, {0}, 0, {"a.c"}, 1, 0, {0}, 0, {0}, 0};\n'
                 '    n = build_cmd(&m, out, sizeof out);\n'
                 '    printf("%d %s\\n", n, out);\n'
                 '    struct build q = {"gcc", "gnu11", 0, 0, {"Q=it\'s"}, 1, {0}, 0, {"my file.c"}, 1, '
                 '"out", {0}, 0, {"z"}, 1};\n'
                 '    n = build_cmd(&q, out, sizeof out);\n'
                 '    printf("%d %s\\n", n, out);\n'
                 '    char small[20];\n'
                 '    printf("%d %d\\n", build_cmd(&m, small, sizeof small), build_cmd(&b, small, sizeof '
                 'small));\n'
                 '    printf("%d\\n", build_cmd(&m, small, 6));\n'
                 '    printf("%d\\n", build_cmd(&m, small, 7));\n'
                 '    struct build e = {"gcc", 0, -1, 0, {0}, 0, {0}, 0, {0}, 0, 0, {0}, 0, {0}, 0};\n'
                 '    n = build_cmd(&e, out, sizeof out);\n'
                 '    printf("%d [%s]\\n", n, out);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Накапливайте строку функцией add_arg(prefix, значение): сама ставит пробел, префикс и при '
               'необходимости кавычки. Библиотеки -l — последними.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['131 gcc -std=c11 -O2 -Wall -Wextra -DDEBUG -D\'NAME="my app"\' -Iinclude -I\'third '
                    "party/inc' main.c util.c -o bin/app -Llib -lm -lpthread",
                    '6 cc a.c',
                    "55 gcc -std=gnu11 -O0 -D'Q=it'\\''s' 'my file.c' -o out -lz",
                    '6 -1',
                    '-1',
                    '6',
                    '3 [gcc]']},
      {'id': 'c10-static-state',
       'mode': 'c',
       'title': 'Состояние внутри функций: static и статический буфер',
       'statement': 'next_id() → 1, 2, 3, … (счётчик в static-переменной), reset_id(start) — следующим '
                    'вернётся start; fib_next() → 0, 1, 1, 2, 3, 5, … по одному числу за вызов, fib_reset(); '
                    'ordinal(n) → указатель на статический буфер с порядковым числительным («1st», «2nd», '
                    '«3rd», «4th», «11th», «12th», «13th», «21st», «102nd»), при следующем вызове буфер '
                    'перезаписывается; ordinal_r(n, buf, size) — то же в буфер вызывающего (возвращает buf). '
                    'calls() → сколько раз вызвана сама calls (счётчик в static).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int next_id(void) { return 0; }\n'
                  'void reset_id(int start) {}\n'
                  'long fib_next(void) { return 0; }\n'
                  'void fib_reset(void) {}\n'
                  'const char *ordinal(int n) { return ""; }\n'
                  'char *ordinal_r(int n, char *buf, size_t size) { return buf; }\n'
                  'int calls(void) { return 0; }\n',
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
                 '    int i1 = next_id();\n'
                 '    int i2 = next_id();\n'
                 '    int i3 = next_id();\n'
                 '    printf("%d %d %d\\n", i1, i2, i3);\n'
                 '    reset_id(100);\n'
                 '    i1 = next_id();\n'
                 '    i2 = next_id();\n'
                 '    printf("%d %d\\n", i1, i2);\n'
                 '    reset_id(1);\n'
                 '    printf("%d\\n", next_id());\n'
                 '    for (int i = 0; i < 10; i++) printf("%ld ", fib_next());\n'
                 '    printf("\\n");\n'
                 '    fib_reset();\n'
                 '    long f1 = fib_next();\n'
                 '    long f2 = fib_next();\n'
                 '    long f3 = fib_next();\n'
                 '    printf("%ld %ld %ld\\n", f1, f2, f3);\n'
                 '    int ns[] = {1, 2, 3, 4, 10, 11, 12, 13, 21, 22, 23, 101, 102, 111, 112, 1000};\n'
                 '    for (size_t i = 0; i < sizeof ns / sizeof ns[0]; i++) printf("%s ", ordinal(ns[i]));\n'
                 '    printf("\\n");\n'
                 '    const char *a = ordinal(1);\n'
                 '    const char *b = ordinal(2);\n'
                 '    printf("%d %s\\n", a == b, a);\n'
                 '    char x[16], y[16];\n'
                 '    ordinal_r(5, x, sizeof x);\n'
                 '    ordinal_r(6, y, sizeof y);\n'
                 '    printf("%s %s\\n", x, y);\n'
                 '    char tiny[4];\n'
                 '    printf("%s\\n", ordinal_r(1000, tiny, sizeof tiny));\n'
                 '    int c1 = calls();\n'
                 '    int c2 = calls();\n'
                 '    int c3 = calls();\n'
                 '    printf("%d %d %d\\n", c1, c2, c3);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'static int counter внутри функции или на уровне файла; для ordinal — static char buf[24] и '
               'общий код с ordinal_r.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['1 2 3',
                    '100 101',
                    '1',
                    '0 1 1 2 3 5 8 13 21 34',
                    '0 1 1',
                    '1st 2nd 3rd 4th 10th 11th 12th 13th 21st 22nd 23rd 101st 102nd 111th 112th 1000th',
                    '1 2nd',
                    '5th 6th',
                    '100',
                    '1 2 3']},
      {'id': 'c10-strtok-r',
       'mode': 'c',
       'title': 'Разбор на слова: strtok_r и strtok на статическом состоянии',
       'statement': 'my_strtok_r(s, delims, save) — как strtok_r: s ≠ NULL — начать новую строку, s == NULL '
                    '— продолжить с *save; пропускает ведущие разделители, возвращает указатель на слово (в '
                    'исходной строке заменяет разделитель после слова нулём) или NULL, когда слов нет. '
                    'my_strtok(s, delims) — вариант со статическим внутренним состоянием (на основе '
                    'my_strtok_r). Вызывать strtok и strtok_r из библиотеки нельзя. Для вложенного разбора '
                    '(внешний цикл по строкам, внутренний по словам) подходит только вариант _r.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'char *my_strtok_r(char *s, const char *delims, char **save) { return 0; }\n'
                  'char *my_strtok(char *s, const char *delims) { return 0; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
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
                 '    char a[] = "  alpha, beta;;gamma  ,delta ";\n'
                 '    char *save;\n'
                 '    for (char *t = my_strtok_r(a, " ,;", &save); t; t = my_strtok_r(NULL, " ,;", &save)) '
                 'printf("[%s]", t);\n'
                 '    printf("\\n");\n'
                 '    char b[] = "one two\\nthree four five\\nsix";\n'
                 '    char *outer_save, *inner_save;\n'
                 '    for (char *line = my_strtok_r(b, "\\n", &outer_save); line; line = my_strtok_r(NULL, '
                 '"\\n", &outer_save)) {\n'
                 '        int n = 0;\n'
                 '        for (char *w = my_strtok_r(line, " ", &inner_save); w; w = my_strtok_r(NULL, " ", '
                 '&inner_save)) n++;\n'
                 '        printf("%d ", n);\n'
                 '    }\n'
                 '    printf("\\n");\n'
                 '    char c[] = "x:y::z";\n'
                 '    for (char *t = my_strtok(c, ":"); t; t = my_strtok(NULL, ":")) printf("<%s>", t);\n'
                 '    printf("\\n");\n'
                 '    char d[] = ",,,";\n'
                 '    printf("%d\\n", my_strtok(d, ",") == NULL);\n'
                 '    char e[] = "";\n'
                 '    printf("%d\\n", my_strtok_r(e, ",", &save) == NULL);\n'
                 '    char f[] = "single";\n'
                 '    char *t1 = my_strtok(f, " ");\n'
                 '    char *t2 = my_strtok(NULL, " ");\n'
                 '    printf("%s %d\\n", t1, t2 == NULL);\n'
                 '    printf("libc: %d\\n", src_count("str" "tok(") > 0);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'strspn пропускает разделители в начале, strcspn находит конец слова. Разделитель после слова '
               'заменяется нулём, а *save указывает за ним.',
       'expected': ['[alpha][beta][gamma][delta]', '2 3 1', '<x><y><z>', '1', '1', 'single 1', 'libc: 1']},
      {'id': 'c10-opaque-stack',
       'mode': 'c',
       'title': 'Непрозрачный тип: стек за интерфейсом',
       'statement': 'В «заголовке» объявлено только struct stack; (его устройство скрыто). Реализуйте: '
                    'stack_new(), stack_push(s, v) → 0/−1, stack_pop(s, *out) → 1/0, stack_peek(s, *out) → '
                    '1/0, stack_size(s), stack_clone(s) — независимая копия (с теми же элементами), '
                    'stack_reverse(s) — перевернуть порядок элементов, stack_free(s) (допускается NULL). '
                    'Устройство структуры — на ваше усмотрение (динамический массив или список). Под '
                    'AddressSanitizer.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  '/* публичная часть */\n'
                  'struct stack;\n'
                  'struct stack *stack_new(void);\n'
                  'int stack_push(struct stack *s, int v);\n'
                  'int stack_pop(struct stack *s, int *out);\n'
                  'int stack_peek(const struct stack *s, int *out);\n'
                  'size_t stack_size(const struct stack *s);\n'
                  'struct stack *stack_clone(const struct stack *s);\n'
                  'void stack_reverse(struct stack *s);\n'
                  'void stack_free(struct stack *s);\n'
                  '\n'
                  '/* закрытая часть: определите здесь struct stack и функции */\n',
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
                 '    struct stack *s = stack_new();\n'
                 '    int x;\n'
                 '    int p0 = stack_pop(s, &x);\n'
                 '    int k0 = stack_peek(s, &x);\n'
                 '    printf("%d %d %zu\\n", p0, k0, stack_size(s));\n'
                 '    for (int i = 1; i <= 10; i++) stack_push(s, i * i);\n'
                 '    int k1 = stack_peek(s, &x);\n'
                 '    printf("%zu %d %d\\n", stack_size(s), k1, x);\n'
                 '    struct stack *c = stack_clone(s);\n'
                 '    stack_push(s, 999);\n'
                 '    stack_pop(c, &x);\n'
                 '    printf("%zu %zu %d\\n", stack_size(s), stack_size(c), x);\n'
                 '    stack_reverse(c);\n'
                 '    printf("%d", stack_pop(c, &x));\n'
                 '    printf(" %d ", x);\n'
                 '    stack_reverse(c);\n'
                 '    printf("%d %d\\n", stack_pop(c, &x), x);\n'
                 '    int sum = 0;\n'
                 '    while (stack_pop(s, &x)) sum += x;\n'
                 '    printf("%d %zu\\n", sum, stack_size(s));\n'
                 '    stack_free(s);\n'
                 '    stack_free(c);\n'
                 '    stack_free(NULL);\n'
                 '    struct stack *e = stack_new();\n'
                 '    stack_reverse(e);\n'
                 '    struct stack *ec = stack_clone(e);\n'
                 '    printf("%zu %zu\\n", stack_size(e), stack_size(ec));\n'
                 '    stack_free(e);\n'
                 '    stack_free(ec);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Определите struct stack ниже прототипов (например, динамический массив с ёмкостью): '
               'клиентский код видит только указатель.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 0 0', '10 1 100', '11 9 100', '1 1 1 81', '1384 0', '0 0']},
      {'id': 'c10-semver',
       'mode': 'c',
       'title': 'Версии библиотек: разбор и сравнение',
       'statement': 'struct ver { int major, minor, patch; char pre[16]; }. ver_parse(s, *v) → 0 или −1: '
                    'формат «[v]MAJOR.MINOR[.PATCH][-ПРЕДВАРИТЕЛЬНАЯ]» (числа без знаков и пробелов, PATCH '
                    'по умолчанию 0, суффикс — буквы, цифры, точки, не длиннее 15). ver_cmp(a, b) → −1/0/1 '
                    'по старшинству: major, minor, patch; версия с суффиксом младше той же без суффикса; два '
                    'суффикса сравниваются как строки (strcmp). ver_compatible(have, want) → 1, если '
                    'библиотека have подходит для требуемой want: тот же major, have ≥ want, и (для major 0) '
                    'тот же minor; предварительные версии подходят только если want тоже предварительная той '
                    'же версии.',
       'starter': 'struct ver { int major, minor, patch; char pre[16]; };\n'
                  '\n'
                  'int ver_parse(const char *s, struct ver *v) { return -9; }\n'
                  'int ver_cmp(const struct ver *a, const struct ver *b) { return 0; }\n'
                  'int ver_compatible(const struct ver *have, const struct ver *want) { return -1; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static void p(const char *s) {\n'
                 '    struct ver v = {-1, -1, -1, "keep"};\n'
                 '    int r = ver_parse(s, &v);\n'
                 '    printf("[%s] %d %d.%d.%d [%s]\\n", s, r, v.major, v.minor, v.patch, v.pre);\n'
                 '}\n'
                 '\n'
                 'static struct ver V(const char *s) {\n'
                 '    struct ver v = {0, 0, 0, ""};\n'
                 '    ver_parse(s, &v);\n'
                 '    return v;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    p("1.2.3"); p("v2.10"); p("1.0.0-rc.1"); p("0.9.12-beta"); p("1"); p("1.2.3.4"); '
                 'p("1.x"); p("");\n'
                 '    p("1.2.-1"); p("1.2.3-"); p("1.2.3-rc 1"); p(" 1.2.3"); p("1.2.3-0123456789abcdef"); '
                 'p("1.2.3-0123456789abcde");\n'
                 '    const char *o[] = {"1.0.0", "1.0.1", "1.1.0", "2.0.0", "1.0.0-alpha", "1.0.0-beta", '
                 '"0.9.9"};\n'
                 '    for (int i = 0; i < 7; i++) {\n'
                 '        for (int j = 0; j < 7; j++) {\n'
                 '            struct ver a = V(o[i]), b = V(o[j]);\n'
                 '            printf("%2d", ver_cmp(&a, &b));\n'
                 '        }\n'
                 '        printf("\\n");\n'
                 '    }\n'
                 '    struct ver h = V("1.4.2"), w1 = V("1.3.0"), w2 = V("1.5.0"), w3 = V("2.0.0"), w4 = '
                 'V("1.4.2");\n'
                 '    printf("%d %d %d %d\\n", ver_compatible(&h, &w1), ver_compatible(&h, &w2), '
                 'ver_compatible(&h, &w3), ver_compatible(&h, &w4));\n'
                 '    struct ver z1 = V("0.3.5"), z2 = V("0.3.1"), z3 = V("0.4.0");\n'
                 '    printf("%d %d\\n", ver_compatible(&z1, &z2), ver_compatible(&z1, &z3));\n'
                 '    struct ver pre = V("1.5.0-rc1"), pw = V("1.5.0-rc1"), pn = V("1.4.0"), pw2 = '
                 'V("1.5.0");\n'
                 '    printf("%d %d %d\\n", ver_compatible(&pre, &pw), ver_compatible(&pre, &pn), '
                 'ver_compatible(&pre, &pw2));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Разбор — по символам через вспомогательную функцию чтения числа. Сравнение: числа, затем '
               'наличие суффикса (его отсутствие — «больше»), затем strcmp.',
       'expected': ['[1.2.3] 0 1.2.3 []',
                    '[v2.10] 0 2.10.0 []',
                    '[1.0.0-rc.1] 0 1.0.0 [rc.1]',
                    '[0.9.12-beta] 0 0.9.12 [beta]',
                    '[1] -1 -1.-1.-1 [keep]',
                    '[1.2.3.4] -1 -1.-1.-1 [keep]',
                    '[1.x] -1 -1.-1.-1 [keep]',
                    '[] -1 -1.-1.-1 [keep]',
                    '[1.2.-1] -1 -1.-1.-1 [keep]',
                    '[1.2.3-] -1 -1.-1.-1 [keep]',
                    '[1.2.3-rc 1] -1 -1.-1.-1 [keep]',
                    '[ 1.2.3] -1 -1.-1.-1 [keep]',
                    '[1.2.3-0123456789abcdef] -1 -1.-1.-1 [keep]',
                    '[1.2.3-0123456789abcde] 0 1.2.3 [0123456789abcde]',
                    ' 0-1-1-1 1 1 1',
                    ' 1 0-1-1 1 1 1',
                    ' 1 1 0-1 1 1 1',
                    ' 1 1 1 0 1 1 1',
                    '-1-1-1-1 0-1 1',
                    '-1-1-1-1 1 0 1',
                    '-1-1-1-1-1-1 0',
                    '1 0 0 1',
                    '1 0',
                    '1 0 0']},
      {'id': 'c10-symtab',
       'mode': 'c',
       'title': 'Таблица символов компоновщика: сильные, слабые, common',
       'statement': 'struct symtab (до 32 символов; имя ≤ 15). Виды: SYM_UNDEF 0, SYM_STRONG 1, SYM_WEAK 2, '
                    'SYM_COMMON 3. st_add(t, name, kind, size, obj) → 0 или −1 (два сильных определения; '
                    'сообщение не нужно). Правила: сильное побеждает слабое и common; слабое побеждает '
                    'common и «неопределён»; два слабых — остаётся первое; два common — остаётся больший '
                    'размер (у размера победившего — кто больше; при равных — первый); неопределённый символ '
                    'ничего не меняет у уже определённого (а вне таблицы появляется как SYM_UNDEF). '
                    'st_kind(t, name) → итоговый вид или −1, если символа нет; st_size(t, name); st_owner(t, '
                    'name) → obj победившего определения; st_undefined(t, out, max) → имена, оставшиеся '
                    'неопределёнными (в порядке появления).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'enum { SYM_UNDEF, SYM_STRONG, SYM_WEAK, SYM_COMMON };\n'
                  'struct sym { char name[16]; int kind; long size; int obj; };\n'
                  'struct symtab { struct sym s[32]; int n; };\n'
                  '\n'
                  'void st_init(struct symtab *t) { t->n = 0; }\n'
                  'int st_add(struct symtab *t, const char *name, int kind, long size, int obj) { return -9; '
                  '}\n'
                  'int st_kind(const struct symtab *t, const char *name) { return -9; }\n'
                  'long st_size(const struct symtab *t, const char *name) { return -9; }\n'
                  'int st_owner(const struct symtab *t, const char *name) { return -9; }\n'
                  'int st_undefined(const struct symtab *t, char out[][16], int max) { return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static void show(const struct symtab *t, const char *n) {\n'
                 '    printf("%s: kind=%d size=%ld owner=%d\\n", n, st_kind(t, n), st_size(t, n), '
                 'st_owner(t, n));\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct symtab t;\n'
                 '    st_init(&t);\n'
                 '    printf("%d ", st_add(&t, "main", SYM_UNDEF, 0, 0));\n'
                 '    printf("%d ", st_add(&t, "main", SYM_STRONG, 0, 1));\n'
                 '    printf("%d ", st_add(&t, "main", SYM_STRONG, 0, 2));\n'
                 '    printf("%d\\n", st_add(&t, "main", SYM_UNDEF, 0, 3));\n'
                 '    show(&t, "main");\n'
                 '    st_add(&t, "w", SYM_WEAK, 8, 1);\n'
                 '    st_add(&t, "w", SYM_WEAK, 16, 2);\n'
                 '    show(&t, "w");\n'
                 '    st_add(&t, "w", SYM_STRONG, 24, 3);\n'
                 '    show(&t, "w");\n'
                 '    st_add(&t, "w", SYM_WEAK, 4, 4);\n'
                 '    show(&t, "w");\n'
                 '    st_add(&t, "c", SYM_COMMON, 4, 1);\n'
                 '    st_add(&t, "c", SYM_COMMON, 40, 2);\n'
                 '    st_add(&t, "c", SYM_COMMON, 40, 3);\n'
                 '    st_add(&t, "c", SYM_COMMON, 8, 4);\n'
                 '    show(&t, "c");\n'
                 '    st_add(&t, "c", SYM_WEAK, 2, 5);\n'
                 '    show(&t, "c");\n'
                 '    st_add(&t, "d", SYM_COMMON, 4, 1);\n'
                 '    st_add(&t, "d", SYM_STRONG, 4, 2);\n'
                 '    st_add(&t, "d", SYM_COMMON, 99, 3);\n'
                 '    show(&t, "d");\n'
                 '    st_add(&t, "u1", SYM_UNDEF, 0, 1);\n'
                 '    st_add(&t, "u2", SYM_UNDEF, 0, 1);\n'
                 '    st_add(&t, "u2", SYM_UNDEF, 0, 2);\n'
                 '    st_add(&t, "u1", SYM_WEAK, 1, 3);\n'
                 '    char out[8][16];\n'
                 '    int k = st_undefined(&t, out, 8);\n'
                 '    printf("%d", k);\n'
                 '    for (int i = 0; i < k; i++) printf(" %s", out[i]);\n'
                 '    printf("\\n");\n'
                 '    printf("%d %ld %d\\n", st_kind(&t, "zzz"), st_size(&t, "zzz"), st_owner(&t, "zzz"));\n'
                 '    char name[16];\n'
                 '    int full = 0;\n'
                 '    for (int i = 0; i < 40; i++) {\n'
                 '        sprintf(name, "s%d", i);\n'
                 '        full += st_add(&t, name, SYM_STRONG, 0, i) != 0;\n'
                 '    }\n'
                 '    printf("%d\\n", full);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Приоритет: strong > weak > common > undef. Исключение: два common — по размеру; два strong — '
               'ошибка; два weak — первое.',
       'expected': ['0 0 -1 0',
                    'main: kind=1 size=0 owner=1',
                    'w: kind=2 size=8 owner=1',
                    'w: kind=1 size=24 owner=3',
                    'w: kind=1 size=24 owner=3',
                    'c: kind=3 size=40 owner=2',
                    'c: kind=2 size=2 owner=5',
                    'd: kind=1 size=4 owner=2',
                    '1 u2',
                    '-1 -1 -1',
                    '14']},
      {'id': 'c10-fix-make-time',
       'mode': 'c',
       'title': 'Исправьте: make пересобирает лишнее и пропускает нужное',
       'statement': 'needs_rebuild(target_time, dep_times, n, phony) решает, нужно ли пересобрать цель: '
                    'время ≤ 0 означает, что файла нет (пересобирать); цель старше любой зависимости '
                    '(target_time < dep_time) — пересобирать; при равных временах — не пересобирать; phony — '
                    'пересобирать всегда. count_stale(targets, deps...) — вспомогательная. Сейчас сравнение '
                    'написано с ошибкой (≤ вместо <), отсутствие файла не учтено, phony игнорируется. '
                    'Исправьте needs_rebuild; newest(dep_times, n) → наибольшее время (0 для пустого списка) '
                    'и stale_count(times, n, dep_time) → сколько целей старше зависимости — тоже должны '
                    'работать правильно.',
       'starter': 'int needs_rebuild(long target_time, const long *dep_times, int n, int phony) {\n'
                  '    for (int i = 0; i < n; i++)\n'
                  '        if (dep_times[i] >= target_time) return 1;\n'
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  'long newest(const long *dep_times, int n) {\n'
                  '    long m = dep_times[0];\n'
                  '    for (int i = 1; i < n; i++)\n'
                  '        if (dep_times[i] > m) m = dep_times[i];\n'
                  '    return m;\n'
                  '}\n'
                  '\n'
                  'int stale_count(const long *times, int n, long dep_time) {\n'
                  '    int c = 0;\n'
                  '    for (int i = 0; i < n; i++)\n'
                  '        if (times[i] <= dep_time) c++;\n'
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
                 '    long d[] = {10, 30, 20};\n'
                 '    printf("%d %d %d %d\\n", needs_rebuild(40, d, 3, 0), needs_rebuild(25, d, 3, 0), '
                 'needs_rebuild(30, d, 3, 0), needs_rebuild(31, d, 3, 0));\n'
                 '    printf("%d %d %d\\n", needs_rebuild(0, d, 3, 0), needs_rebuild(-1, d, 3, 0), '
                 'needs_rebuild(100, d, 3, 1));\n'
                 '    printf("%d %d\\n", needs_rebuild(5, d, 0, 0), needs_rebuild(0, d, 0, 0));\n'
                 '    printf("%ld %ld %ld\\n", newest(d, 3), newest(d, 0), newest(d, 1));\n'
                 '    long t[] = {5, 10, 15, 10, 20};\n'
                 '    printf("%d %d %d %d\\n", stale_count(t, 5, 10), stale_count(t, 5, 21), stale_count(t, '
                 '5, 5), stale_count(t, 0, 10));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Строго «<»/«>» для сравнения времён; отсутствие файла (время ≤ 0) и phony — отдельные '
               'условия в начале. newest пустого списка не должна читать массив.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['0 1 0 0', '1 1 1', '0 1', '30 0 10', '1 5 0 0']},
      {'id': 'c10-fix-archive-order',
       'mode': 'c',
       'title': 'Исправьте: библиотеки с зависимостями «назад»',
       'statement': 'pull_all(libs, n, undefined_in, nu, order) должна вытащить из набора архивов все '
                    'объекты, нужные для закрытия неопределённых символов, даже если нужный объект стоит в '
                    'архиве раньше того, кто на него ссылается. Объект: struct obj { name; def[4]; ndef; '
                    'undef[4]; nundef } (имена символов — строки). Сейчас функция делает один проход и '
                    'теряет такие зависимости. Исправьте: повторяйте просмотр, пока что-то извлекается. '
                    'Результат — число извлечённых, их индексы — в order в порядке извлечения; остальная '
                    'логика (объект извлекается, если определяет хотя бы один сейчас неопределённый символ; '
                    'его требования добавляются) уже верна.',
       'starter': '#include <stddef.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'struct obj { const char *name; const char *def[4]; int ndef; const char *undef[4]; int '
                  'nundef; };\n'
                  '\n'
                  'static int is_defined(const char **defd, int nd, const char *s) {\n'
                  '    for (int i = 0; i < nd; i++) if (strcmp(defd[i], s) == 0) return 1;\n'
                  '    return 0;\n'
                  '}\n'
                  '\n'
                  'int pull_all(const struct obj *libs, int n, const char **undefined_in, int nu, int '
                  '*order) {\n'
                  '    const char *need[64];\n'
                  '    int nn = 0;\n'
                  '    for (int i = 0; i < nu; i++) need[nn++] = undefined_in[i];\n'
                  '    const char *defd[64];\n'
                  '    int nd = 0, cnt = 0;\n'
                  '    char pulled[32] = {0};\n'
                  '    for (int i = 0; i < n; i++) {\n'
                  '        int hit = 0;\n'
                  '        for (int d = 0; d < libs[i].ndef && !hit; d++)\n'
                  '            for (int k = 0; k < nn; k++)\n'
                  '                if (strcmp(need[k], libs[i].def[d]) == 0) hit = 1;\n'
                  '        if (!hit) continue;\n'
                  '        pulled[i] = 1;\n'
                  '        order[cnt++] = i;\n'
                  '        for (int d = 0; d < libs[i].ndef; d++) defd[nd++] = libs[i].def[d];\n'
                  '        for (int u = 0; u < libs[i].nundef; u++) {\n'
                  '            const char *s = libs[i].undef[u];\n'
                  '            if (!is_defined(defd, nd, s)) need[nn++] = s;\n'
                  '        }\n'
                  '    }\n'
                  '    return cnt;\n'
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
                 'static void t(const char *label, const struct obj *l, int n, const char **u, int nu) {\n'
                 '    int order[16];\n'
                 '    int k = pull_all(l, n, u, nu, order);\n'
                 '    printf("%s: %d [", label, k);\n'
                 '    for (int i = 0; i < k; i++) printf("%s%s", i ? " " : "", l[order[i]].name);\n'
                 '    printf("]\\n");\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct obj lib[] = {\n'
                 '        {"c.o", {"c"}, 1, {0}, 0},\n'
                 '        {"b.o", {"b"}, 1, {"c"}, 1},\n'
                 '        {"a.o", {"a"}, 1, {"b"}, 1},\n'
                 '        {"z.o", {"z"}, 1, {0}, 0},\n'
                 '    };\n'
                 '    const char *u1[] = {"a"};\n'
                 '    t("chain", lib, 4, u1, 1);\n'
                 '    const char *u2[] = {"z", "a"};\n'
                 '    t("two", lib, 4, u2, 2);\n'
                 '    const char *u3[] = {"q"};\n'
                 '    t("none", lib, 4, u3, 1);\n'
                 '    struct obj ring[] = {\n'
                 '        {"x.o", {"x"}, 1, {"y"}, 1},\n'
                 '        {"y.o", {"y"}, 1, {"x"}, 1},\n'
                 '    };\n'
                 '    const char *u4[] = {"y"};\n'
                 '    t("ring", ring, 2, u4, 1);\n'
                 '    t("empty", lib, 4, u1, 0);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Оберните просмотр в цикл do { changed = 0; … } while (changed); не извлекайте повторно уже '
               'извлечённые объекты.',
       'expected': ['chain: 3 [a.o b.o c.o]',
                    'two: 4 [a.o z.o b.o c.o]',
                    'none: 0 []',
                    'ring: 2 [y.o x.o]',
                    'empty: 0 []']},
      {'id': 'c10-fix-static-buffer',
       'mode': 'c',
       'title': 'Исправьте: статический буфер в двух вызовах',
       'statement': 'fmt_pair(a, b) возвращает строку «(a, b)» из статического буфера: в printf("%s %s", '
                    'fmt_pair(1, 2), fmt_pair(3, 4)) обе подстановки показывают одно и то же. Не меняя '
                    'сигнатуру, перепишите так, чтобы последовательные вызовы (хотя бы четыре подряд) не '
                    'затирали друг друга: используйте кольцо из нескольких статических буферов. Результат — '
                    'строка до 31 символа; для остального поведение прежнее. size_str(bytes) → «1.5K», '
                    '«2.0M», … («1023», «1.0K», «1.5M», «2.0G») с тем же ограничением — тоже должна '
                    'возвращать строку из кольца.',
       'starter': '#include <stdio.h>\n'
                  '\n'
                  'const char *fmt_pair(int a, int b) {\n'
                  '    static char buf[32];\n'
                  '    snprintf(buf, sizeof buf, "(%d, %d)", a, b);\n'
                  '    return buf;\n'
                  '}\n'
                  '\n'
                  'const char *size_str(long bytes) {\n'
                  '    static char buf[32];\n'
                  '    if (bytes < 1024) snprintf(buf, sizeof buf, "%ld", bytes);\n'
                  '    else if (bytes < 1024 * 1024) snprintf(buf, sizeof buf, "%.1fK", bytes / 1024.0);\n'
                  '    else if (bytes < 1024L * 1024 * 1024) snprintf(buf, sizeof buf, "%.1fM", bytes / '
                  '(1024.0 * 1024));\n'
                  '    else snprintf(buf, sizeof buf, "%.1fG", bytes / (1024.0 * 1024 * 1024));\n'
                  '    return buf;\n'
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
                 '    const char *a = fmt_pair(1, 2);\n'
                 '    const char *b = fmt_pair(3, 4);\n'
                 '    const char *c = fmt_pair(5, 6);\n'
                 '    const char *d = size_str(1536);\n'
                 '    printf("%s %s %s %s\\n", a, b, c, d);\n'
                 '    printf("%s %s %s %s\\n", size_str(1023), size_str(1024), size_str(3 * 1024 * 1024 / '
                 '2), size_str(2L * 1024 * 1024 * 1024));\n'
                 '    printf("%s\\n", fmt_pair(-1, 1000000));\n'
                 '    printf("%s %s\\n", size_str(0), fmt_pair(0, 0));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Кольцо: static char ring[4][32]; static unsigned idx; каждый вызов берёт ring[idx++ % 4].',
       'expected': ['(1, 2) (3, 4) (5, 6) 1.5K', '1023 1.0K 1.5M 2.0G', '(-1, 1000000)', '0 (0, 0)']},
      {'id': 'c10-fix-quote',
       'mode': 'c',
       'title': 'Исправьте: кавычки в аргументах командной строки',
       'statement': 'quote_arg(s, out, cap) должна возвращать безопасную для оболочки запись аргумента: «как '
                    'есть», если все символы из набора [A-Za-z0-9_@%+=:,./-] (и строка не пуста), иначе — в '
                    "одинарных кавычках, внутренний ' записывается как '\\'' ; пустая → ''. Сейчас она "
                    'оборачивает в кавычки только строки с пробелом и не экранирует одинарную кавычку '
                    'внутри. Исправьте. Возврат — длина результата или −1, если не помещается (с учётом '
                    'завершающего нуля).',
       'starter': '#include <stddef.h>\n'
                  '#include <string.h>\n'
                  '\n'
                  'int quote_arg(const char *s, char *out, size_t cap) {\n'
                  "    int need = strchr(s, ' ') != NULL;\n"
                  '    size_t k = 0;\n'
                  "    if (need && k + 1 < cap) out[k++] = '\\'';\n"
                  '    for (; *s && k + 1 < cap; s++) out[k++] = *s;\n'
                  "    if (need && k + 1 < cap) out[k++] = '\\'';\n"
                  '    if (k >= cap) return -1;\n'
                  '    out[k] = 0;\n'
                  '    return (int)k;\n'
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
                 '    char q[64];\n'
                 '    const char *s[] = {"main.c", "a b", "it\'s", "", "x=1,y:2/z-3", "$HOME", "semi;colon", '
                 '"tab\\there", "a\\"b", "~/file", "*.c", "a&b", "\'", "\'\'"};\n'
                 '    for (size_t i = 0; i < sizeof s / sizeof s[0]; i++) {\n'
                 '        int n = quote_arg(s[i], q, sizeof q);\n'
                 '        printf("%d %s\\n", n, q);\n'
                 '    }\n'
                 '    printf("%d %d %d\\n", quote_arg("abcdef", q, 6), quote_arg("abcde", q, 6), '
                 'quote_arg("a b", q, 4));\n'
                 '    printf("%d %d\\n", quote_arg("a b", q, 5), quote_arg("", q, 2));\n'
                 '    printf("%d %d\\n", quote_arg("", q, 3), quote_arg("\'", q, 6));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': '«Безопасные» символы — небольшой набор; всё остальное требует кавычек. Внутри одинарных '
               "кавычек сам символ ' закрывает кавычку, вставляет \\' и открывает новую: '\\''.",
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['6 main.c',
                    "5 'a b'",
                    "9 'it'\\''s'",
                    "2 ''",
                    '11 x=1,y:2/z-3',
                    "7 '$HOME'",
                    "12 'semi;colon'",
                    "10 'tab\there'",
                    '5 \'a"b\'',
                    "8 '~/file'",
                    "5 '*.c'",
                    "5 'a&b'",
                    "6 ''\\'''",
                    "10 ''\\'''\\'''",
                    '-1 5 -1',
                    '-1 -1',
                    '2 -1']},
      {'id': 'c10-amalgamate',
       'mode': 'c',
       'title': 'Объединение файлов в один (амальгама)',
       'statement': 'struct src { const char *name; const char *text; }. amalgamate(files, n, root, out, '
                    'cap) строит один файл из root: строки вида #include "имя", где имя есть среди files, '
                    'заменяются содержимым этого файла (рекурсивно), причём каждый файл вставляется не '
                    'больше одного раза (как под защитой include guard); остальные строки копируются; строки '
                    '«#pragma once» отбрасываются; #include <…> и «имя» не из files остаются как есть. '
                    'Каждая вставка окружена комментариями «/* begin имя */» и «/* end имя */» на отдельных '
                    'строках; root тоже обёрнут. Содержимое заканчивается переводом строки (если нет — '
                    'добавьте). Возврат — длина результата или −1, если не помещается в cap, или −2, если '
                    'root не найден.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct src { const char *name; const char *text; };\n'
                  '\n'
                  'int amalgamate(const struct src *files, int n, const char *root, char *out, size_t cap) '
                  '{\n'
                  '    return -9;\n'
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
                 '    struct src f[] = {\n'
                 '        {"main.c", "#include <stdio.h>\\n#include \\"util.h\\"\\n#include '
                 '\\"config.h\\"\\nint main(void) { return util(); }\\n"},\n'
                 '        {"util.h", "#pragma once\\n#include \\"config.h\\"\\nint util(void);\\n"},\n'
                 '        {"config.h", "#ifndef CONFIG_H\\n#define CONFIG_H\\n#define N '
                 '3\\n#endif\\n#include \\"missing.h\\"\\n"},\n'
                 '        {"loop_a.h", "#include \\"loop_b.h\\"\\nint a;\\n"},\n'
                 '        {"loop_b.h", "#include \\"loop_a.h\\"\\nint b;"},\n'
                 '    };\n'
                 '    char out[1024];\n'
                 '    int n = amalgamate(f, 5, "main.c", out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    n = amalgamate(f, 5, "loop_a.h", out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    printf("%d\\n", amalgamate(f, 5, "nope.c", out, sizeof out));\n'
                 '    printf("%d\\n", amalgamate(f, 5, "main.c", out, 50));\n'
                 '    n = amalgamate(f, 5, "config.h", out, sizeof out);\n'
                 '    printf("%d\\n", n);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Рекурсивная emit(файл): отметить файл как вставленный, вывести begin, построчно '
               'скопировать/развернуть include, вывести end. Строки с #pragma once пропустить.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['255',
                    '/* begin main.c */',
                    '#include <stdio.h>',
                    '/* begin util.h */',
                    '/* begin config.h */',
                    '#ifndef CONFIG_H',
                    '#define CONFIG_H',
                    '#define N 3',
                    '#endif',
                    '#include "missing.h"',
                    '/* end config.h */',
                    'int util(void);',
                    '/* end util.h */',
                    'int main(void) { return util(); }',
                    '/* end main.c */',
                    '94',
                    '/* begin loop_a.h */',
                    '/* begin loop_b.h */',
                    'int b;',
                    '/* end loop_b.h */',
                    'int a;',
                    '/* end loop_a.h */',
                    '-2',
                    '-1',
                    '114']},
      {'id': 'c10-name-prefix',
       'mode': 'c',
       'title': 'Добавление префикса к именам модуля',
       'statement': 'prefix_symbols(src, names, nnames, prefix, out, cap) копирует исходный текст в out, '
                    'добавляя prefix перед каждым вхождением идентификатора из names (целое слово, а не '
                    'часть другого слова: init не меняет init_all и reinit), но только в коде — не внутри '
                    'строковых литералов "…", символьных констант \'…\' и комментариев (// и /* */). '
                    'Возвращает длину результата или −1, если не помещается в cap (с учётом нуля).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int prefix_symbols(const char *src, const char *const *names, int nnames, const char '
                  '*prefix, char *out, size_t cap) {\n'
                  '    return -9;\n'
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
                 '    const char *names[] = {"init", "push", "count"};\n'
                 '    const char *src =\n'
                 '        "int count;\\n"\n'
                 '        "void init(void) { count = 0; }\\n"\n'
                 '        "void push(int x) { /* push to count */ count += x; }\\n"\n'
                 '        "void init_all(void) { init(); reinit(); } // init here\\n"\n'
                 '        "const char *s = \\"init push \\\\\\"count\\\\\\"\\";\\n"\n'
                 '        "char c = \'x\'; int count2 = 10, v = 0x1f;\\n"\n'
                 '        "#define COUNT count\\n"\n'
                 '        "x->count = y.init;\\n";\n'
                 '    char out[512];\n'
                 '    int n = prefix_symbols(src, names, 3, "st_", out, sizeof out);\n'
                 '    printf("%d\\n%s", n, out);\n'
                 '    n = prefix_symbols("init", names, 3, "", out, sizeof out);\n'
                 '    printf("%d %s\\n", n, out);\n'
                 '    n = prefix_symbols("a init b", names, 0, "p_", out, sizeof out);\n'
                 '    printf("%d %s\\n", n, out);\n'
                 '    n = prefix_symbols("init init", names, 3, "pre_", out, 16);\n'
                 '    printf("%d\\n", n);\n'
                 '    n = prefix_symbols("init", names, 3, "pre_", out, 9);\n'
                 '    printf("%d\\n", n);\n'
                 '    n = prefix_symbols("init", names, 3, "pre_", out, 10);\n'
                 '    printf("%d %s\\n", n, out);\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Разберите текст конечным автоматом: обычный код, строка, символ, строчный и блочный '
               'комментарий; в коде читайте слово целиком и сравнивайте со списком.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['296',
                    'int st_count;',
                    'void st_init(void) { st_count = 0; }',
                    'void st_push(int x) { /* push to count */ st_count += x; }',
                    'void init_all(void) { st_init(); reinit(); } // init here',
                    'const char *s = "init push \\"count\\"";',
                    "char c = 'x'; int count2 = 10, v = 0x1f;",
                    '#define COUNT st_count',
                    'x->st_count = y.st_init;',
                    '4 init',
                    '8 a init b',
                    '-1',
                    '8',
                    '8 pre_init']},
      {'id': 'c10-makefile-lint',
       'mode': 'c',
       'title': 'Проверка Makefile: типичные ошибки',
       'statement': 'lint_make(text, msgs, max) → список сообщений (до max, строки по ≤ 63 символов) в '
                    'порядке строк; формат «line N: …»: 1) строка команды начинается с пробелов, а не с '
                    'табуляции — сразу после строки правила или другой команды: «line N: recipe needs TAB»; '
                    '2) цель из набора {all, clean, test, install} без объявления в «.PHONY» (объявление '
                    'может быть где угодно в файле): «line N: add X to .PHONY» (сообщение — по строке '
                    'правила); 3) использование $(ИМЯ) / ${ИМЯ}, не определённой строкой «ИМЯ = …» (или :=, '
                    '+=, ?=) выше по тексту и не из встроенных CC, CXX, RM, AR, MAKE, CFLAGS, LDFLAGS, '
                    'LDLIBS: «line N: undefined variable ИМЯ» (каждое использование); 4) повторное правило '
                    'для той же цели: «line N: duplicate rule for ЦЕЛЬ». Строки-комментарии (#…) '
                    'пропускаются. Возврат — число сообщений (не больше max).',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'int lint_make(const char *text, char msgs[][64], int max) {\n'
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
                 'static void t(const char *label, const char *mk) {\n'
                 '    char msgs[16][64];\n'
                 '    int n = lint_make(mk, msgs, 16);\n'
                 '    printf("%s: %d\\n", label, n);\n'
                 '    for (int i = 0; i < n; i++) printf("  %s\\n", msgs[i]);\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    t("ok", "CC = gcc\\nOBJ = a.o b.o\\n.PHONY: all clean\\nall: app\\napp: '
                 '$(OBJ)\\n\\t$(CC) $^ -o $@\\nclean:\\n\\t$(RM) $(OBJ)\\n");\n'
                 '    t("space", "app: a.o\\n    $(CC) a.o -o app\\n");\n'
                 '    t("undef", "app: $(OBJS)\\n\\t$(CC) $(OBJS) -o app $(LIBS)\\n");\n'
                 '    t("dup", "a: b\\n\\techo 1\\nb:\\n\\techo 2\\na: c\\n");\n'
                 '    t("comment", "# $(NOPE)\\nx = 1\\ny: $(x)\\n");\n'
                 '    t("later", "app: $(OBJ)\\nOBJ = a.o\\n");\n'
                 '    t("phony", "all: app\\napp:\\n\\ttrue\\nclean:\\n\\trm -f app\\ntest: app\\n.PHONY: '
                 'clean\\n");\n'
                 '    t("clean", "");\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'Идите по строкам, помня: определённые переменные, цели, был ли предыдущей строкой правило. '
               'Проверьте каждое $(…) по списку определённых и встроенных.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['ok: 0',
                    'space: 1',
                    '  line 2: recipe needs TAB',
                    'undef: 3',
                    '  line 1: undefined variable OBJS',
                    '  line 2: undefined variable OBJS',
                    '  line 2: undefined variable LIBS',
                    'dup: 1',
                    '  line 5: duplicate rule for a',
                    'comment: 0',
                    'later: 1',
                    '  line 1: undefined variable OBJ',
                    'phony: 2',
                    '  line 1: add all to .PHONY',
                    '  line 6: add test to .PHONY',
                    'clean: 0']},
      {'id': 'c10-build-levels',
       'mode': 'c',
       'title': 'Уровни сборки и критический путь',
       'statement': 'Правила struct rule (цель, зависимости). level_of(rules, n, target): цель без правила — '
                    '0; цель с правилом без зависимостей — 1; иначе 1 + наибольший уровень зависимостей; '
                    'цикл → −1. critical_path(rules, n, goal, path, max) → самый длинный путь цели вниз по '
                    'зависимостям: path[0] = goal, затем зависимость с наибольшим уровнем (при равенстве — '
                    'первая в списке) и так до цели без правила; возвращает число элементов пути, −1 при '
                    'цикле. jobs_per_level(rules, n, goal, counts, max) → число уровней L и сколько '
                    'различных целей с правилами лежит на каждом уровне 1…L (counts[0] — уровень 1) среди '
                    'достижимых из goal (включая goal); при цикле −1.',
       'starter': '#include <stddef.h>\n'
                  '\n'
                  'struct rule { char target[32]; char deps[8][32]; int ndeps; char recipe[4][64]; int '
                  'nrecipe; };\n'
                  '\n'
                  'int level_of(const struct rule *rules, int n, const char *target) { return -9; }\n'
                  'int critical_path(const struct rule *rules, int n, const char *goal, char path[][32], int '
                  'max) { return -9; }\n'
                  'int jobs_per_level(const struct rule *rules, int n, const char *goal, int *counts, int '
                  'max) { return -9; }\n',
       'driver': '/*__DRIVER__*/\n'
                 '#include <stdio.h>\n'
                 '#include <stdint.h>\n'
                 '#include <stddef.h>\n'
                 '#include <string.h>\n'
                 '#include <stdlib.h>\n'
                 '#include <limits.h>\n'
                 '#include <ctype.h>\n'
                 '\n'
                 'static struct rule mk(const char *t, int nd, const char *d0, const char *d1, const char '
                 '*d2) {\n'
                 '    struct rule r;\n'
                 '    memset(&r, 0, sizeof r);\n'
                 '    strcpy(r.target, t);\n'
                 '    const char *ds[3] = {d0, d1, d2};\n'
                 '    for (int i = 0; i < nd; i++) strcpy(r.deps[r.ndeps++], ds[i]);\n'
                 '    return r;\n'
                 '}\n'
                 '\n'
                 'int main(void) {\n'
                 '    struct rule r[] = {\n'
                 '        mk("app", 3, "main.o", "util.o", "lib.a"),\n'
                 '        mk("main.o", 2, "main.c", "config.h", 0),\n'
                 '        mk("util.o", 1, "util.c", 0, 0),\n'
                 '        mk("lib.a", 2, "a.o", "b.o", 0),\n'
                 '        mk("a.o", 1, "a.c", 0, 0),\n'
                 '        mk("b.o", 1, "gen.c", 0, 0),\n'
                 '        mk("gen.c", 1, "gen.py", 0, 0),\n'
                 '        mk("docs", 0, 0, 0, 0),\n'
                 '    };\n'
                 '    const char *ts[] = {"app", "main.o", "lib.a", "b.o", "gen.c", "docs", "main.c", '
                 '"zzz"};\n'
                 '    for (int i = 0; i < 8; i++) printf("%s=%d ", ts[i], level_of(r, 8, ts[i]));\n'
                 '    printf("\\n");\n'
                 '    char path[8][32];\n'
                 '    int k = critical_path(r, 8, "app", path, 8);\n'
                 '    printf("%d:", k);\n'
                 '    for (int i = 0; i < k; i++) printf(" %s", path[i]);\n'
                 '    printf("\\n");\n'
                 '    k = critical_path(r, 8, "util.o", path, 8);\n'
                 '    printf("%d: %s %s\\n", k, path[0], path[1]);\n'
                 '    k = critical_path(r, 8, "main.c", path, 8);\n'
                 '    printf("%d: %s\\n", k, path[0]);\n'
                 '    k = critical_path(r, 8, "app", path, 2);\n'
                 '    printf("%d\\n", k);\n'
                 '    int counts[8];\n'
                 '    int L = jobs_per_level(r, 8, "app", counts, 8);\n'
                 '    printf("%d:", L);\n'
                 '    for (int i = 0; i < L; i++) printf(" %d", counts[i]);\n'
                 '    printf("\\n");\n'
                 '    L = jobs_per_level(r, 8, "lib.a", counts, 8);\n'
                 '    printf("%d: %d %d %d\\n", L, counts[0], counts[1], counts[2]);\n'
                 '    L = jobs_per_level(r, 8, "docs", counts, 8);\n'
                 '    printf("%d: %d\\n", L, counts[0]);\n'
                 '    struct rule c[] = {mk("a", 1, "b", 0, 0), mk("b", 1, "a", 0, 0)};\n'
                 '    printf("%d %d %d\\n", level_of(c, 2, "a"), critical_path(c, 2, "a", path, 8), '
                 'jobs_per_level(c, 2, "a", counts, 8));\n'
                 '    return 0;\n'
                 '}\n',
       'hint': 'level_of — рекурсия с защитой от цикла по глубине. Критический путь — на каждом шаге идём в '
               'зависимость с наибольшим уровнем.',
       'flags': '-std=gnu11 -O1 -g0 -Wall -fsanitize=address,undefined -fno-sanitize-recover=all',
       'expected': ['app=4 main.o=1 lib.a=3 b.o=2 gen.c=1 docs=1 main.c=0 zzz=0',
                    '5: app lib.a b.o gen.c gen.py',
                    '2: util.o util.c',
                    '1: main.c',
                    '2',
                    '4: 4 1 1 1',
                    '3: 2 1 1',
                    '1: 1',
                    '-1 -1 -1']}]}
