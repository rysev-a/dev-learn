"""Задачи книги «Архитектура компьютера»: главы 4–5."""

from app.exercises.arch_tasks._sim import TOY_SIM

TASKS: dict[int, list[dict]] = {
    4: [
        {
            "id": "pack-instruction",
            "mode": "func",
            "func": "pack_instr",
            "title": "Упаковка команды",
            "statement": (
                "Команда учебного процессора занимает 16 бит: [код операции "
                "4 бита][приёмник 2 бита][источник 2 бита][число 8 бит]. "
                "Напишите функцию pack_instr(op, rd, rs, imm), которая "
                "собирает слово. Поля гарантированно помещаются в свои биты."
            ),
            "starter": "def pack_instr(op, rd, rs, imm):\n    pass\n",
            "tests": [
                {"args": [2, 1, 2, 42], "expected": 0x262A},
                {"args": [0, 0, 0, 0], "expected": 0},
                {"args": [15, 3, 3, 255], "expected": 0xFFFF},
                {"args": [1, 0, 0, 255], "expected": 0x10FF},
                {"args": [8, 2, 1, 7], "expected": 0x8907},
            ],
            "hint": "(op << 12) | (rd << 10) | (rs << 8) | imm.",
        },
        {
            "id": "unpack-instruction",
            "mode": "func",
            "func": "unpack_instr",
            "title": "Разбор команды",
            "statement": (
                "Напишите функцию unpack_instr(word): по 16-битному слову "
                "верните кортеж (op, rd, rs, imm) — формат тот же: "
                "[op 4][rd 2][rs 2][imm 8]."
            ),
            "starter": "def unpack_instr(word):\n    pass\n",
            "tests": [
                {"args": [0x262A], "expected": (2, 1, 2, 42)},
                {"args": [0], "expected": (0, 0, 0, 0)},
                {"args": [0xFFFF], "expected": (15, 3, 3, 255)},
                {"args": [0x10FF], "expected": (1, 0, 0, 255)},
                {"args": [0x8907], "expected": (8, 2, 1, 7)},
            ],
            "hint": "op = word >> 12; rd = (word >> 10) & 3; rs = (word >> 8) & 3; imm = word & 0xFF.",
        },
        {
            "id": "alu-flags",
            "mode": "func",
            "func": "alu_flags",
            "title": "АЛУ с флагами Z N C V",
            "statement": (
                "Напишите функцию alu_flags(op, a, b) для 8-битных "
                "операндов (0…255), op — 'ADD' или 'SUB'. Верните кортеж "
                "(результат, Z, N, C, V): результат — 8 бит; Z — результат "
                "нулевой; N — старший бит результата; C — перенос при "
                "сложении или заём (a < b) при вычитании; V — знаковое "
                "переполнение (операнды как числа в дополнительном коде). "
                "Все флаги — 0 или 1."
            ),
            "starter": "def alu_flags(op, a, b):\n    pass\n",
            "tests": [
                {"args": ["ADD", 100, 100], "expected": (200, 0, 1, 0, 1)},
                {"args": ["ADD", 255, 1], "expected": (0, 1, 0, 1, 0)},
                {"args": ["ADD", 127, 1], "expected": (128, 0, 1, 0, 1)},
                {"args": ["ADD", 128, 128], "expected": (0, 1, 0, 1, 1)},
                {"args": ["SUB", 5, 7], "expected": (254, 0, 1, 1, 0)},
                {"args": ["SUB", 128, 1], "expected": (127, 0, 0, 0, 1)},
                {"args": ["SUB", 0, 0], "expected": (0, 1, 0, 0, 0)},
                {"args": ["SUB", 127, 255], "expected": (128, 0, 1, 1, 1)},
            ],
            "hint": "Переполнение при сложении: знаки a и b совпадают, а знак результата другой. При вычитании: знаки a и b разные, а знак результата отличается от знака a.",
        },
        {
            "id": "toy-cpu-run",
            "mode": "func",
            "func": "toy_run",
            "title": "Напишите процессор",
            "statement": (
                "Реализуйте функцию toy_run(program, regs, memory) — "
                "симулятор учебного процессора. program — список команд "
                "вида [имя, аргументы…]; регистры R0..R3 по 8 бит "
                "(результаты обрезаются до 0…255), начальные значения "
                "берутся из словаря regs (остальные — нули); memory — "
                "список байтов или None (тогда 256 нулей). Команды: "
                "LDI rd imm; MOV rd rs; ADD/SUB/AND/OR/XOR rd rs; "
                "CMP rd rs (как SUB, но без записи); SHL rd, SHR rd (сдвиг "
                "на бит); LD rd addr; ST rs addr; JMP/JZ/JNZ/JC/JN addr; HLT. "
                "Флаги меняют ADD, SUB, CMP, AND, OR, XOR, SHL, SHR: "
                "Z — результат нулевой, N — его старший бит, C — перенос "
                "при ADD, заём (a < b) при SUB/CMP, выдвинутый бит при "
                "сдвигах, 0 для AND/OR/XOR. LDI, MOV, LD, ST флаги не "
                "трогают. Счётчик команд начинается с нуля; HLT тоже "
                "считается выполненной командой. Верните кортеж "
                "([R0, R1, R2, R3], число_выполненных_команд)."
            ),
            "starter": "def toy_run(program, regs, memory):\n    pass\n",
            "tests": [
                {"args": [[["LDI", "R0", 0], ["LDI", "R1", 5], ["LDI", "R2", 1], ["ADD", "R0", "R1"], ["SUB", "R1", "R2"], ["JNZ", 3], ["HLT"]], {}, None], "expected": ([15, 0, 1, 0], 19)},
                {"args": [[["LDI", "R0", 250], ["LDI", "R1", 10], ["ADD", "R0", "R1"], ["HLT"]], {}, None], "expected": ([4, 10, 0, 0], 4)},
                {"args": [[["LDI", "R0", 7], ["ST", "R0", 10], ["LDI", "R0", 0], ["LD", "R1", 10], ["HLT"]], {}, None], "expected": ([0, 7, 0, 0], 5)},
                {"args": [[["LDI", "R0", 200], ["LDI", "R1", 100], ["ADD", "R0", "R1"], ["JC", 5], ["LDI", "R3", 1], ["LDI", "R3", 9], ["HLT"]], {}, None], "expected": ([44, 100, 0, 9], 6)},
                {"args": [[["LDI", "R0", 12], ["LDI", "R1", 10], ["MOV", "R2", "R0"], ["AND", "R2", "R1"], ["MOV", "R3", "R0"], ["XOR", "R3", "R1"], ["SHL", "R0"], ["SHR", "R1"], ["HLT"]], {}, None], "expected": ([24, 5, 8, 6], 9)},
                {"args": [[["LDI", "R0", 3], ["LDI", "R1", 5], ["SUB", "R0", "R1"], ["JN", 5], ["LDI", "R2", 1], ["HLT"]], {}, None], "expected": ([254, 5, 0, 0], 5)},
                {"args": [[["LDI", "R0", 4], ["LDI", "R1", 4], ["CMP", "R0", "R1"], ["JZ", 5], ["LDI", "R2", 1], ["LDI", "R3", 7], ["HLT"]], {}, None], "expected": ([4, 4, 0, 7], 6)},
                {"args": [[["HLT"]], {}, None], "expected": ([0, 0, 0, 0], 1)},
                {"args": [[["ADD", "R0", "R1"], ["HLT"]], {"R0": 20, "R1": 22}, None], "expected": ([42, 22, 0, 0], 2)},
                {"args": [[["LD", "R0", 2], ["LD", "R1", 3], ["OR", "R0", "R1"], ["ST", "R0", 0], ["LD", "R3", 0], ["HLT"]], {}, [0, 0, 5, 64]], "expected": ([69, 64, 0, 69], 6)},
                {"args": [[["JMP", 2], ["LDI", "R0", 99], ["LDI", "R1", 1], ["HLT"]], {}, None], "expected": ([0, 1, 0, 0], 3)},
                {"args": [[["LDI", "R0", 129], ["SHL", "R0"], ["JC", 4], ["LDI", "R1", 5], ["LDI", "R2", 6], ["HLT"]], {}, None], "expected": ([2, 0, 6, 0], 5)},
            ],
            "hint": "Цикл: op, *a = program[pc]; pc += 1; steps += 1; затем if/elif по op. Флаги храните в переменных z, n, c; для условных переходов смотрите на них.",
        },
        {
            "id": "cpi-time",
            "mode": "func",
            "func": "cpu_time",
            "title": "Такты, CPI и время",
            "statement": (
                "Напишите функцию cpu_time(trace, table, ghz): trace — "
                "список выполненных команд (имена), table — словарь «имя → "
                "число тактов», ghz — частота в гигагерцах. Верните кортеж "
                "(всего_тактов, CPI, время_в_нс), где CPI и время округлены "
                "до двух знаков (round). Для пустой трассы — (0, 0.0, 0.0)."
            ),
            "starter": "def cpu_time(trace, table, ghz):\n    pass\n",
            "tests": [
                {"args": [["LDI", "LD", "ADD", "JNZ", "ADD", "JNZ"], {"LDI": 1, "ADD": 1, "LD": 3, "JNZ": 2}, 3], "expected": (10, 1.67, 3.33)},
                {"args": [[], {"LDI": 1}, 2], "expected": (0, 0.0, 0.0)},
                {"args": [["A", "A", "A", "A"], {"A": 2}, 1], "expected": (8, 2.0, 8.0)},
                {"args": [["MUL", "ADD"], {"MUL": 4, "ADD": 1}, 2.5], "expected": (5, 2.5, 2.0)},
                {"args": [["DIV"], {"DIV": 20}, 4], "expected": (20, 20.0, 5.0)},
            ],
            "hint": "Один такт длится 1 / ghz наносекунд; время = всего_тактов / ghz.",
        },
        {
            "id": "program-multiply",
            "mode": "stdout",
            "title": "Умножение без MUL",
            "statement": (
                "В нашем процессоре нет команды умножения. Напишите "
                "программу — список PROGRAM в формате команд из задачи "
                "«Напишите процессор» — которая вычисляет R0 = R1 × R2 "
                "(значения R1 и R2 заданы заранее, результат по модулю 256), "
                "в конце HLT. Использовать можно любые регистры. Программа "
                "должна работать и при R2 = 0."
            ),
            "starter": "PROGRAM = [\n    [\"HLT\"],\n]\n",
            "driver": TOY_SIM + (
                "def check(a, b):\n"
                "    r, _, steps = toy_run(PROGRAM, {'R1': a, 'R2': b})\n"
                "    return r['R0']\n"
                "print(check(3, 4), check(0, 5), check(7, 0), check(15, 17), check(16, 16), check(1, 200))\n"
                "r, _, steps = toy_run(PROGRAM, {'R1': 9, 'R2': 20})\n"
                "print(r['R0'], r['R1'], r['R2'] in (0, 20))\n"
            ),
            "expected": ["12 0 0 255 0 200", "180 9 True"],
            "hint": "Цикл: пока R2 != 0 — R0 += R1; R2 -= 1. Проверка нуля без перехода: MOV R3 R2; AND R3 R3 выставляет флаг Z.",
        },
        {
            "id": "program-max",
            "mode": "stdout",
            "title": "Максимум двух чисел",
            "statement": (
                "Напишите программу PROGRAM для учебного процессора: "
                "R0 = max(R1, R2), числа беззнаковые 0…255. В конце HLT. "
                "Подсказка: CMP выставляет флаг переноса, если первое число "
                "меньше второго."
            ),
            "starter": "PROGRAM = [\n    [\"HLT\"],\n]\n",
            "driver": TOY_SIM + (
                "def check(a, b):\n"
                "    r, _, steps = toy_run(PROGRAM, {'R1': a, 'R2': b})\n"
                "    return r['R0']\n"
                "print(check(3, 4), check(4, 3), check(5, 5), check(0, 255), check(255, 0), check(127, 128))\n"
            ),
            "expected": ["4 4 5 255 255 128"],
            "hint": "MOV R0 R1; CMP R0 R2; JC на команду MOV R0 R2; иначе HLT.",
        },
        {
            "id": "program-fibonacci",
            "mode": "stdout",
            "title": "Числа Фибоначчи на ассемблере",
            "statement": (
                "Напишите программу PROGRAM: R0 = F(R1), где F(0) = 0, "
                "F(1) = 1, F(n) = F(n - 1) + F(n - 2), а R1 лежит в "
                "диапазоне 0…13 (результат помещается в байт). В конце HLT. "
                "Программа должна работать и для R1 = 0."
            ),
            "starter": "PROGRAM = [\n    [\"HLT\"],\n]\n",
            "driver": TOY_SIM + (
                "def fib(n):\n    r, _, steps = toy_run(PROGRAM, {'R1': n})\n    return r['R0']\n"
                "print([fib(n) for n in range(14)])\n"
            ),
            "expected": ["[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]"],
            "hint": "Три регистра: a, b и временный t. Цикл n раз: t = a + b; a = b; b = t. Проверку n == 0 сделайте через AND.",
        },
        {
            "id": "mem-size",
            "mode": "func",
            "func": "mem_size",
            "title": "Объём адресуемой памяти",
            "statement": (
                "Напишите функцию mem_size(addr_bits): строка с объёмом "
                "памяти, который можно адресовать (по байту на адрес): "
                "2**addr_bits байт, записанный в самых крупных единицах, "
                "где число остаётся целым: 'B', 'KiB', 'MiB', 'GiB', 'TiB', "
                "'PiB', 'EiB' (степени 1024). Формат: '4 GiB'."
            ),
            "starter": "def mem_size(addr_bits):\n    pass\n",
            "tests": [
                {"args": [8], "expected": "256 B"},
                {"args": [10], "expected": "1 KiB"},
                {"args": [12], "expected": "4 KiB"},
                {"args": [16], "expected": "64 KiB"},
                {"args": [20], "expected": "1 MiB"},
                {"args": [32], "expected": "4 GiB"},
                {"args": [36], "expected": "64 GiB"},
                {"args": [48], "expected": "256 TiB"},
                {"args": [64], "expected": "16 EiB"},
                {"args": [0], "expected": "1 B"},
            ],
            "hint": "Каждые 10 бит адреса — множитель 1024: units[addr_bits // 10], число 2 ** (addr_bits % 10).",
        },
    ],
    5: [
        {
            "id": "assembler-two-pass",
            "mode": "func",
            "func": "assemble",
            "title": "Двухпроходный ассемблер",
            "statement": (
                "Напишите функцию assemble(text): текст программы на "
                "ассемблере учебного процессора -> список команд, каждая — "
                "список [мнемоника, аргументы…]. Правила: одна команда на "
                "строку, аргументы разделены пробелами; всё после ';' — "
                "комментарий; пустые строки игнорируются; строка вида "
                "'имя:' объявляет метку на следующей команде. В "
                "аргументах метка заменяется номером команды (метка может "
                "быть объявлена ниже использования), числа — десятичные "
                "или шестнадцатеричные (0x2A) — преобразуются в int, "
                "остальное (R0..R3) остаётся строкой."
            ),
            "starter": "def assemble(text):\n    pass\n",
            "tests": [
                {"args": ["    LDI R0 0\n    LDI R1 3\n    LDI R2 1\nloop:\n    ADD R0 R1\n    SUB R1 R2\n    JNZ loop\n    HLT\n"], "expected": [["LDI", "R0", 0], ["LDI", "R1", 3], ["LDI", "R2", 1], ["ADD", "R0", "R1"], ["SUB", "R1", "R2"], ["JNZ", 3], ["HLT"]]},
                {"args": ["JMP end ; пропуск\n  LDI R0 1\n\nend:\n  HLT"], "expected": [["JMP", 2], ["LDI", "R0", 1], ["HLT"]]},
                {"args": ["a:\nb:\n HLT\n JMP a\n JMP b"], "expected": [["HLT"], ["JMP", 0], ["JMP", 0]]},
                {"args": ["LDI R3 0x2A\nLDI R0 255 ; максимум"], "expected": [["LDI", "R3", 42], ["LDI", "R0", 255]]},
                {"args": [""], "expected": []},
                {"args": ["; только комментарий\n\n"], "expected": []},
            ],
            "hint": "Первый проход: пройдите по строкам, строки с ':' в конце запоминайте как метки (адрес = число команд к этому моменту). Второй: для каждого аргумента — метка, число (int(a, 0) понимает 0x), иначе строка.",
        },
        {
            "id": "encode-program",
            "mode": "func",
            "func": "encode_program",
            "title": "Ассемблер в машинный код",
            "statement": (
                "Напишите функцию encode_program(prog): prog — список команд "
                "[имя, аргументы…], результат — список 16-битных слов. "
                "Коды операций: HLT 0, LDI 1, MOV 2, ADD 3, SUB 4, AND 5, "
                "OR 6, XOR 7, CMP 8, LD 9, ST 10, JMP 11, JZ 12, JNZ 13, "
                "JC 14, JN 15. Номера регистров: R0..R3 — 0..3. Формат: "
                "LDI rd imm: op<<12 | rd<<10 | imm; MOV/ADD/SUB/AND/OR/"
                "XOR/CMP rd rs: op<<12 | rd<<10 | rs<<8; LD rd addr и "
                "ST rs addr: op<<12 | reg<<10 | addr; JMP/JZ/JNZ/JC/JN addr: "
                "op<<12 | addr; HLT: 0."
            ),
            "starter": "def encode_program(prog):\n    pass\n",
            "tests": [
                {"args": [[["LDI", "R1", 5], ["ADD", "R0", "R1"], ["SUB", "R1", "R2"], ["JNZ", 3], ["HLT"]]], "expected": [0x1405, 0x3100, 0x4600, 0xD003, 0x0000]},
                {"args": [[]], "expected": []},
                {"args": [[["LD", "R2", 200], ["ST", "R3", 17]]], "expected": [0x98C8, 0xAC11]},
                {"args": [[["MOV", "R3", "R0"], ["CMP", "R1", "R2"], ["JZ", 7], ["JC", 255], ["JN", 0], ["JMP", 10]]], "expected": [0x2C00, 0x8600, 0xC007, 0xE0FF, 0xF000, 0xB00A]},
                {"args": [[["AND", "R0", "R3"], ["OR", "R1", "R1"], ["XOR", "R2", "R0"]]], "expected": [0x5300, 0x6500, 0x7800]},
            ],
            "hint": "Заведите словари кодов операций и регистров и функцию, выбирающую шаблон по имени команды.",
        },
        {
            "id": "decode-program",
            "mode": "func",
            "func": "decode_program",
            "title": "Дизассемблер",
            "statement": (
                "Напишите функцию decode_program(words): обратное "
                "преобразование к encode_program — список 16-битных слов "
                "в список команд [имя, аргументы…] (регистры — строками "
                "'R0'..'R3', остальное — целыми). Коды операций и форматы "
                "те же: HLT 0, LDI 1, MOV 2, ADD 3, SUB 4, AND 5, OR 6, "
                "XOR 7, CMP 8, LD 9, ST 10, JMP 11, JZ 12, JNZ 13, JC 14, "
                "JN 15."
            ),
            "starter": "def decode_program(words):\n    pass\n",
            "tests": [
                {"args": [[0x1405, 0x3100, 0x4600, 0xD003, 0x0000]], "expected": [["LDI", "R1", 5], ["ADD", "R0", "R1"], ["SUB", "R1", "R2"], ["JNZ", 3], ["HLT"]]},
                {"args": [[]], "expected": []},
                {"args": [[0x98C8, 0xAC11]], "expected": [["LD", "R2", 200], ["ST", "R3", 17]]},
                {"args": [[0x2C00, 0x8600, 0xC007, 0xE0FF, 0xF000, 0xB00A]], "expected": [["MOV", "R3", "R0"], ["CMP", "R1", "R2"], ["JZ", 7], ["JC", 255], ["JN", 0], ["JMP", 10]]},
                {"args": [[0x5300, 0x6500, 0x7800]], "expected": [["AND", "R0", "R3"], ["OR", "R1", "R1"], ["XOR", "R2", "R0"]]},
            ],
            "hint": "op = w >> 12; rd = (w >> 10) & 3; rs = (w >> 8) & 3; imm/addr = w & 0xFF. Какая форма — зависит от операции.",
        },
        {
            "id": "addressing-modes",
            "mode": "func",
            "func": "operand_value",
            "title": "Режимы адресации",
            "statement": (
                "Напишите функцию operand_value(mode, operand, regs, mem): "
                "вернуть значение операнда. Режимы: 'imm' — само число "
                "operand; 'reg' — regs[operand] (operand — имя регистра); "
                "'direct' — mem[operand]; 'reg_indirect' — "
                "mem[regs[operand]]; 'mem_indirect' — mem[mem[operand]]; "
                "'indexed' — operand это [смещение, имя_регистра], значение "
                "mem[смещение + regs[имя_регистра]]."
            ),
            "starter": "def operand_value(mode, operand, regs, mem):\n    pass\n",
            "tests": [
                {"args": ["imm", 5, {"R1": 2}, [10, 20, 30, 40]], "expected": 5},
                {"args": ["reg", "R1", {"R1": 2}, [10, 20, 30, 40]], "expected": 2},
                {"args": ["direct", 1, {"R1": 2}, [10, 20, 30, 40]], "expected": 20},
                {"args": ["reg_indirect", "R1", {"R1": 2}, [10, 20, 30, 40]], "expected": 30},
                {"args": ["mem_indirect", 0, {}, [3, 20, 30, 40]], "expected": 40},
                {"args": ["indexed", [1, "R1"], {"R1": 2}, [10, 20, 30, 40]], "expected": 40},
                {"args": ["indexed", [0, "R0"], {"R0": 0}, [7]], "expected": 7},
            ],
            "hint": "Одна цепочка if/elif по режиму; в косвенной адресации чтение памяти выполняется дважды.",
        },
        {
            "id": "stack-machine-eval",
            "mode": "func",
            "func": "run_stack",
            "title": "Стековая машина",
            "statement": (
                "Напишите функцию run_stack(code): code — список команд "
                "[имя, аргументы…] стековой машины: PUSH n (положить), ADD, "
                "SUB, MUL, DIV (целочисленное деление //), NEG (сменить "
                "знак вершины), DUP (продублировать вершину), SWAP (поменять "
                "две верхние). Бинарные операции берут два верхних значения "
                "(x — глубже, y — на вершине) и кладут x ∘ y. Верните "
                "итоговый стек (список, вершина — последний элемент)."
            ),
            "starter": "def run_stack(code):\n    pass\n",
            "tests": [
                {"args": [[["PUSH", 1], ["PUSH", 2], ["ADD"], ["PUSH", 3], ["MUL"]]], "expected": [9]},
                {"args": [[["PUSH", 10], ["PUSH", 4], ["SUB"]]], "expected": [6]},
                {"args": [[["PUSH", 7], ["PUSH", 2], ["DIV"], ["NEG"]]], "expected": [-3]},
                {"args": [[["PUSH", 5], ["DUP"], ["MUL"]]], "expected": [25]},
                {"args": [[["PUSH", 1], ["PUSH", 2], ["SWAP"]]], "expected": [2, 1]},
                {"args": [[]], "expected": []},
                {"args": [[["PUSH", 8], ["PUSH", 2], ["SWAP"], ["DIV"]]], "expected": [0]},
            ],
            "hint": "Для бинарной операции: y = stack.pop(); x = stack.pop(); stack.append(x + y) и т. д.",
        },
        {
            "id": "compile-expression",
            "mode": "func",
            "func": "compile_expr",
            "title": "Компилятор выражений",
            "statement": (
                "Напишите функцию compile_expr(text): строка с целыми "
                "числами, операциями + - * /, скобками и пробелами -> "
                "код для стековой машины: список [['PUSH', n], …, ['ADD'], …] "
                "(ADD, SUB, MUL, DIV). Учитывайте приоритет (* и / выше "
                "+ и -) и левую ассоциативность. Унарного минуса нет. "
                "Подсказка: алгоритм сортировочной станции."
            ),
            "starter": "def compile_expr(text):\n    pass\n",
            "tests": [
                {"args": ["1 + 2 * 3"], "expected": [["PUSH", 1], ["PUSH", 2], ["PUSH", 3], ["MUL"], ["ADD"]]},
                {"args": ["(1 + 2) * 3"], "expected": [["PUSH", 1], ["PUSH", 2], ["ADD"], ["PUSH", 3], ["MUL"]]},
                {"args": ["10 - 4 - 3"], "expected": [["PUSH", 10], ["PUSH", 4], ["SUB"], ["PUSH", 3], ["SUB"]]},
                {"args": ["8 / 2 / 2"], "expected": [["PUSH", 8], ["PUSH", 2], ["DIV"], ["PUSH", 2], ["DIV"]]},
                {"args": ["42"], "expected": [["PUSH", 42]]},
                {"args": ["2*(3+(4-1))"], "expected": [["PUSH", 2], ["PUSH", 3], ["PUSH", 4], ["PUSH", 1], ["SUB"], ["ADD"], ["MUL"]]},
                {"args": ["1 - 2 * 3 + 4"], "expected": [["PUSH", 1], ["PUSH", 2], ["PUSH", 3], ["MUL"], ["SUB"], ["PUSH", 4], ["ADD"]]},
            ],
            "hint": "Числа сразу выводите в результат; операции держите на стеке: перед помещением новой операции выведите со стека все с приоритетом не ниже (левая ассоциативность). '(' кладётся, ')' выводит всё до '('.",
        },
        {
            "id": "call-depth",
            "mode": "func",
            "func": "call_depth",
            "title": "Глубина стека вызовов",
            "statement": (
                "Напишите функцию call_depth(events): events — список строк "
                "'call' и 'ret'. Верните кортеж (максимальная_глубина, "
                "итоговая_глубина), а если какой-то 'ret' выполняется при "
                "пустом стеке — строку 'underflow'."
            ),
            "starter": "def call_depth(events):\n    pass\n",
            "tests": [
                {"args": [["call", "call", "ret", "call", "call", "call", "ret", "ret", "ret", "ret"]], "expected": (4, 0)},
                {"args": [[]], "expected": (0, 0)},
                {"args": [["call", "ret", "ret"]], "expected": "underflow"},
                {"args": [["call", "call", "call"]], "expected": (3, 3)},
                {"args": [["ret"]], "expected": "underflow"},
            ],
            "hint": "Счётчик depth: call увеличивает, ret уменьшает; перед уменьшением проверьте, что он больше нуля.",
        },
        {
            "id": "sum-nested-iterative",
            "mode": "stdout",
            "title": "Глубокая вложенность без рекурсии",
            "statement": (
                "Напишите функцию sum_nested(data): сумма всех чисел во "
                "вложенных списках произвольной глубины. Проверка подаёт "
                "вложенность 200 000 уровней — рекурсивное решение "
                "переполнит стек. Используйте собственный стек."
            ),
            "starter": "def sum_nested(data):\n    pass\n",
            "driver": (
                "print(sum_nested([1, [2, [3, [4]]], 5]), sum_nested([]), sum_nested([[], [[]]]), sum_nested([7]))\n"
                "x = [1]\nfor _ in range(200000):\n    x = [x, 1]\nprint(sum_nested(x))\n"
            ),
            "expected": ["15 0 0 7", "200001"],
            "hint": "stack = [data]; пока он не пуст — достаньте элемент: список разверните в стек, число прибавьте к сумме.",
        },
        {
            "id": "program-popcount",
            "mode": "stdout",
            "title": "Подсчёт битов на ассемблере",
            "statement": (
                "Напишите программу PROGRAM для учебного процессора "
                "(формат команд как в главе 4: список [имя, аргументы…]; "
                "SHR сдвигает вправо и записывает выдвинутый бит во флаг "
                "переноса): R0 = число единичных битов в R1. В конце HLT. "
                "R1 можно разрушать."
            ),
            "starter": "PROGRAM = [\n    [\"HLT\"],\n]\n",
            "driver": TOY_SIM + (
                "def pc(n):\n    r, _, steps = toy_run(PROGRAM, {'R1': n})\n    return r['R0']\n"
                "print([pc(n) for n in (0, 1, 7, 128, 170, 255, 64, 129)])\n"
            ),
            "expected": ["[0, 1, 3, 1, 4, 8, 1, 2]"],
            "hint": "Цикл: если R1 == 0 — конец; SHR R1; если перенос — R0 += 1. Ноль проверяйте так: MOV R2 R1; AND R2 R2; JZ.",
        },
    ],
}
