"""Задачи книги «Архитектура компьютера»: главы 1–3."""

TASKS: dict[int, list[dict]] = {
    1: [
        {
            "id": "gates-from-nand",
            "mode": "stdout",
            "title": "НЕ, И, ИЛИ из одного NAND",
            "statement": (
                "Вентиль nand(a, b) уже написан. Реализуйте через него — и "
                "только через него — функции not_(a), and_(a, b) и "
                "or_(a, b) для битов 0 и 1. Проверка считает вызовы nand: "
                "not_ должна обращаться к нему один раз, and_ — два, or_ — три."
            ),
            "starter": (
                "def nand(a, b):\n    return 1 - (a & b)\n\n\n"
                "def not_(a):\n    pass\n\n\n"
                "def and_(a, b):\n    pass\n\n\n"
                "def or_(a, b):\n    pass\n"
            ),
            "driver": (
                "calls = []\n"
                "def nand(a, b):\n    calls.append(1)\n    return 1 - (a & b)\n"
                "def run(f, *args):\n    calls.clear()\n    r = f(*args)\n    return r, len(calls)\n"
                "pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]\n"
                "r = [run(not_, a) for a in (0, 1)]\n"
                "print(r[0][0], r[1][0], 'calls', max(c for _, c in r))\n"
                "r = [run(and_, a, b) for a, b in pairs]\n"
                "print(*[x for x, _ in r], 'calls', max(c for _, c in r))\n"
                "r = [run(or_, a, b) for a, b in pairs]\n"
                "print(*[x for x, _ in r], 'calls', max(c for _, c in r))\n"
            ),
            "expected": ["1 0 calls 1", "0 0 0 1 calls 2", "0 1 1 1 calls 3"],
            "hint": "NOT(a) = NAND(a, a). AND — это NOT от NAND. OR = NAND(NOT a, NOT b) (закон Де Моргана).",
        },
        {
            "id": "xor-from-nand",
            "mode": "stdout",
            "title": "XOR из четырёх NAND",
            "statement": (
                "Реализуйте xor_(a, b) только через nand — ровно за четыре "
                "вызова. Подсказка: пусть m = nand(a, b); результат — nand "
                "от nand(a, m) и nand(b, m)."
            ),
            "starter": "def nand(a, b):\n    return 1 - (a & b)\n\n\ndef xor_(a, b):\n    pass\n",
            "driver": (
                "calls = []\n"
                "def nand(a, b):\n    calls.append(1)\n    return 1 - (a & b)\n"
                "out = []\n"
                "for a in (0, 1):\n    for b in (0, 1):\n        calls.clear()\n        out.append((xor_(a, b), len(calls)))\n"
                "print(*[x for x, _ in out])\nprint(max(c for _, c in out))\n"
            ),
            "expected": ["0 1 1 0", "4"],
            "hint": "m = nand(a, b); return nand(nand(a, m), nand(b, m)).",
        },
        {
            "id": "full-adder",
            "mode": "func",
            "func": "full_adder",
            "title": "Полный сумматор",
            "statement": (
                "Напишите функцию full_adder(a, b, cin): три бита на входе, "
                "кортеж (сумма, перенос) на выходе. Используйте только "
                "битовые операции &, |, ^ — без сложения."
            ),
            "starter": "def full_adder(a, b, cin):\n    pass\n",
            "tests": [
                {"args": [0, 0, 0], "expected": (0, 0)},
                {"args": [1, 0, 0], "expected": (1, 0)},
                {"args": [1, 1, 0], "expected": (0, 1)},
                {"args": [1, 1, 1], "expected": (1, 1)},
                {"args": [0, 1, 1], "expected": (0, 1)},
                {"args": [1, 0, 1], "expected": (0, 1)},
            ],
            "hint": "сумма = a ^ b ^ cin; перенос = (a & b) | (cin & (a ^ b)).",
        },
        {
            "id": "ripple-carry-add",
            "mode": "func",
            "func": "add_bits",
            "title": "Сумматор со сквозным переносом",
            "statement": (
                "Напишите функцию add_bits(x, y, width): сложите два "
                "беззнаковых числа в width разрядах, как цепочка полных "
                "сумматоров. Верните кортеж (результат, перенос_из_старшего). "
                "Результат не должен выходить за width бит."
            ),
            "starter": "def add_bits(x, y, width):\n    pass\n",
            "tests": [
                {"args": [5, 3, 4], "expected": (8, 0)},
                {"args": [9, 9, 4], "expected": (2, 1)},
                {"args": [15, 1, 4], "expected": (0, 1)},
                {"args": [200, 100, 8], "expected": (44, 1)},
                {"args": [0, 0, 8], "expected": (0, 0)},
                {"args": [65535, 65535, 16], "expected": (65534, 1)},
                {"args": [1, 2, 1], "expected": (1, 0)},
            ],
            "hint": "Идите по разрядам i = 0..width-1: s = a ^ b ^ carry; carry = (a & b) | (carry & (a ^ b)); складывайте s << i в результат.",
        },
        {
            "id": "mux4",
            "mode": "func",
            "func": "mux4",
            "title": "Мультиплексор на четыре входа",
            "statement": (
                "Напишите функцию mux4(sel, bits): sel — число от 0 до 3 "
                "(два управляющих бита), bits — список из четырёх битов. "
                "Верните бит с номером sel. Соберите его из мультиплексоров "
                "на два входа: mux(s, a, b) = (a & (1 - s)) | (b & s)."
            ),
            "starter": "def mux(s, a, b):\n    return (a & (1 - s)) | (b & s)\n\n\ndef mux4(sel, bits):\n    pass\n",
            "tests": [
                {"args": [0, [1, 0, 0, 0]], "expected": 1},
                {"args": [1, [1, 0, 1, 1]], "expected": 0},
                {"args": [2, [0, 0, 1, 0]], "expected": 1},
                {"args": [3, [0, 0, 0, 1]], "expected": 1},
                {"args": [3, [1, 1, 1, 0]], "expected": 0},
                {"args": [2, [1, 1, 0, 1]], "expected": 0},
            ],
            "hint": "Два мультиплексора по младшему биту sel & 1 выбирают пары (0, 1) и (2, 3), третий по старшему биту sel >> 1 выбирает из них.",
        },
        {
            "id": "sr-latch-run",
            "mode": "func",
            "func": "latch_run",
            "title": "Защёлка на вентилях NOR",
            "statement": (
                "Напишите функцию latch_run(events): events — список пар "
                "(s, r). Смоделируйте SR-защёлку из двух NOR с обратной "
                "связью (q = nor(r, nq), nq = nor(s, q)), в начале q = 0, "
                "nq = 1. На каждое событие повторите обновление несколько "
                "раз, чтобы схема установилась, и запишите q. Пара (1, 1) "
                "не встречается. Верните список значений q."
            ),
            "starter": "def latch_run(events):\n    pass\n",
            "tests": [
                {"args": [[[1, 0], [0, 0], [0, 1], [0, 0]]], "expected": [1, 1, 0, 0]},
                {"args": [[[0, 0], [0, 0]]], "expected": [0, 0]},
                {"args": [[[1, 0], [0, 0], [0, 0], [0, 1], [1, 0], [0, 0]]], "expected": [1, 1, 1, 0, 1, 1]},
                {"args": [[]], "expected": []},
                {"args": [[[0, 1], [0, 0], [1, 0], [0, 0], [0, 1]]], "expected": [0, 0, 1, 1, 0]},
            ],
            "hint": "for _ in range(4): q, nq = nor(r, nq), nor(s, q) — повторяйте, пока значения не перестанут меняться.",
        },
        {
            "id": "decoder",
            "mode": "func",
            "func": "decoder",
            "title": "Дешифратор",
            "statement": (
                "Напишите функцию decoder(n, value): n — число входных "
                "битов, value — число от 0 до 2**n - 1. Верните список из "
                "2**n выходов, в котором единица стоит только на позиции "
                "value, остальные нули. Дешифраторы выбирают ячейку памяти "
                "по адресу."
            ),
            "starter": "def decoder(n, value):\n    pass\n",
            "tests": [
                {"args": [1, 0], "expected": [1, 0]},
                {"args": [2, 2], "expected": [0, 0, 1, 0]},
                {"args": [3, 5], "expected": [0, 0, 0, 0, 0, 1, 0, 0]},
                {"args": [3, 0], "expected": [1, 0, 0, 0, 0, 0, 0, 0]},
                {"args": [0, 0], "expected": [1]},
                {"args": [4, 15], "expected": [0] * 15 + [1]},
            ],
            "hint": "Для каждого выхода i проверьте: совпадает ли i с value — каждый бит сравнивается XOR (равенство = нет различий).",
        },
        {
            "id": "mini-alu",
            "mode": "func",
            "func": "alu",
            "title": "Мини-АЛУ с флагами",
            "statement": (
                "Напишите функцию alu(op, a, b) для 8-битных беззнаковых "
                "чисел. Операции: 'ADD', 'SUB', 'AND', 'OR', 'XOR', 'SHL' "
                "(a << 1), 'SHR' (a >> 1; b не используется). Верните "
                "кортеж (результат, нулевой, перенос): результат — 8 бит; "
                "нулевой — 1, если результат 0, иначе 0; перенос — для ADD "
                "1, если сумма не влезла в 8 бит, для SUB 1, если a < b "
                "(заём), для SHL — выдвинутый старший бит, для остальных 0."
            ),
            "starter": "def alu(op, a, b):\n    pass\n",
            "tests": [
                {"args": ["ADD", 200, 100], "expected": (44, 0, 1)},
                {"args": ["ADD", 1, 2], "expected": (3, 0, 0)},
                {"args": ["ADD", 255, 1], "expected": (0, 1, 1)},
                {"args": ["SUB", 5, 7], "expected": (254, 0, 1)},
                {"args": ["SUB", 7, 7], "expected": (0, 1, 0)},
                {"args": ["AND", 12, 10], "expected": (8, 0, 0)},
                {"args": ["OR", 12, 10], "expected": (14, 0, 0)},
                {"args": ["XOR", 15, 15], "expected": (0, 1, 0)},
                {"args": ["SHL", 129, 0], "expected": (2, 0, 1)},
                {"args": ["SHR", 129, 0], "expected": (64, 0, 0)},
            ],
            "hint": "Вычислите сырой результат, перенос возьмите из бита выше восьмого (raw >> 8 & 1) или из сравнения a < b, результат — raw & 255.",
        },
    ],
    2: [
        {
            "id": "to-base",
            "mode": "func",
            "func": "to_base",
            "title": "Перевод в систему счисления",
            "statement": (
                "Напишите функцию to_base(n, base): строка с записью "
                "неотрицательного числа n в системе счисления с основанием "
                "от 2 до 16 (цифры — 0-9 и заглавные A-F). Для нуля — '0'. "
                "Готовые bin/hex/format использовать нельзя — делите и "
                "собирайте остатки."
            ),
            "starter": "def to_base(n, base):\n    pass\n",
            "tests": [
                {"args": [13, 2], "expected": "1101"},
                {"args": [255, 16], "expected": "FF"},
                {"args": [0, 2], "expected": "0"},
                {"args": [100, 8], "expected": "144"},
                {"args": [48879, 16], "expected": "BEEF"},
                {"args": [1023, 2], "expected": "1111111111"},
                {"args": [35, 12], "expected": "2B"},
            ],
            "hint": "Пока n > 0: остаток n % base — очередная цифра (младшая первой), n //= base; в конце переверните.",
        },
        {
            "id": "twos-encode",
            "mode": "func",
            "func": "to_twos",
            "title": "Запись в дополнительном коде",
            "statement": (
                "Напишите функцию to_twos(n, width): строка из width нулей и "
                "единиц — запись целого n в дополнительном коде. Гарантируется, "
                "что число помещается в диапазон -2**(width-1) … 2**(width-1) - 1."
            ),
            "starter": "def to_twos(n, width):\n    pass\n",
            "tests": [
                {"args": [5, 8], "expected": "00000101"},
                {"args": [-5, 8], "expected": "11111011"},
                {"args": [-128, 8], "expected": "10000000"},
                {"args": [127, 8], "expected": "01111111"},
                {"args": [0, 4], "expected": "0000"},
                {"args": [-1, 16], "expected": "1111111111111111"},
                {"args": [-2, 3], "expected": "110"},
            ],
            "hint": "Отрицательное число n в width битах — это n + 2**width; маска n & ((1 << width) - 1) делает это автоматически; format(..., '0{}b').",
        },
        {
            "id": "twos-decode",
            "mode": "func",
            "func": "from_twos",
            "title": "Чтение дополнительного кода",
            "statement": (
                "Напишите функцию from_twos(bits): bits — строка из нулей и "
                "единиц (старший бит первый), число в дополнительном коде. "
                "Верните знаковое целое."
            ),
            "starter": "def from_twos(bits):\n    pass\n",
            "tests": [
                {"args": ["00000101"], "expected": 5},
                {"args": ["11111011"], "expected": -5},
                {"args": ["10000000"], "expected": -128},
                {"args": ["01111111"], "expected": 127},
                {"args": ["1"], "expected": -1},
                {"args": ["110"], "expected": -2},
                {"args": ["0"], "expected": 0},
            ],
            "hint": "value = int(bits, 2); если старший бит единица, вычтите 2**len(bits).",
        },
        {
            "id": "signed-add-overflow",
            "mode": "func",
            "func": "add_signed",
            "title": "Знаковое сложение с переполнением",
            "statement": (
                "Напишите функцию add_signed(a, b, width): a и b — знаковые "
                "числа, помещающиеся в width бит. Сложите их так, как это "
                "сделает процессор: результат урезается до width бит и "
                "читается как знаковое. Верните кортеж (результат, "
                "переполнение), где переполнение — True, если настоящая "
                "сумма не помещается в диапазон."
            ),
            "starter": "def add_signed(a, b, width):\n    pass\n",
            "tests": [
                {"args": [100, 100, 8], "expected": (-56, True)},
                {"args": [100, 20, 8], "expected": (120, False)},
                {"args": [-100, -100, 8], "expected": (56, True)},
                {"args": [-128, -1, 8], "expected": (127, True)},
                {"args": [127, 1, 8], "expected": (-128, True)},
                {"args": [-5, 5, 8], "expected": (0, False)},
                {"args": [7, 7, 4], "expected": (-2, True)},
            ],
            "hint": "raw = (a + b) & mask; если старший бит raw установлен — вычтите 2**width; переполнение — когда результат не равен a + b.",
        },
        {
            "id": "bit-ops-sequence",
            "mode": "func",
            "func": "apply_ops",
            "title": "Операции над битами",
            "statement": (
                "Напишите функцию apply_ops(value, ops): ops — список пар "
                "[имя, номер_бита], где имя — 'set' (включить бит), 'clear' "
                "(выключить) или 'toggle' (переключить). Номера битов "
                "считаются с нуля, справа. Верните итоговое значение."
            ),
            "starter": "def apply_ops(value, ops):\n    pass\n",
            "tests": [
                {"args": [0, [["set", 3], ["set", 0]]], "expected": 9},
                {"args": [9, [["clear", 3]]], "expected": 1},
                {"args": [1, [["toggle", 7], ["toggle", 0]]], "expected": 128},
                {"args": [255, [["clear", 0], ["clear", 7], ["clear", 7]]], "expected": 126},
                {"args": [5, []], "expected": 5},
                {"args": [0, [["set", 40]]], "expected": 1099511627776},
            ],
            "hint": "set: value |= 1 << i; clear: value &= ~(1 << i); toggle: value ^= 1 << i.",
        },
        {
            "id": "popcount-fast",
            "mode": "stdout",
            "title": "Подсчёт единичных битов",
            "statement": (
                "Напишите функцию popcount(n): число единичных битов в "
                "неотрицательном целом. Решение должно работать за число "
                "итераций, равное числу единиц (трюк n &= n - 1 сбрасывает "
                "младшую единицу): проверка подаёт число с миллионом "
                "нулевых битов подряд."
            ),
            "starter": "def popcount(n):\n    pass\n",
            "driver": (
                "print(popcount(0), popcount(255), popcount(2 ** 64 - 1), popcount(1 << 100))\n"
                "print(popcount((1 << 1000000) | 1), popcount((1 << 1000000) | (1 << 500000) | 1))\n"
            ),
            "expected": ["0 8 64 1", "2 3"],
            "hint": "while n: n &= n - 1; count += 1. Строки и bin() даже с миллионом бит справятся, но этот вариант не зависит от длины числа.",
        },
        {
            "id": "float32-decode",
            "mode": "func",
            "func": "float32_value",
            "title": "Расшифровка IEEE 754",
            "statement": (
                "Напишите функцию float32_value(bits): bits — 32-битное "
                "целое, в котором закодировано число формата binary32. "
                "Верните значение как обычный float, вычислив его по "
                "формуле вручную (без struct). Нужно обработать обычные "
                "числа, ноль и денормализованные (порядок 0): "
                "(-1)^знак × (1 + мантисса/2²³) × 2^(порядок − 127); для "
                "порядка 0 — (-1)^знак × (мантисса/2²³) × 2^(−126). "
                "Бесконечности и NaN в тестах нет."
            ),
            "starter": "def float32_value(bits):\n    pass\n",
            "tests": [
                {"args": [0x3F800000], "expected": 1.0},
                {"args": [0xC0200000], "expected": -2.5},
                {"args": [0x00000000], "expected": 0.0},
                {"args": [0x40490FDB], "expected": 3.1415927410125732},
                {"args": [0x3DCCCCCD], "expected": 0.10000000149011612},
                {"args": [0x00000001], "expected": 1.401298464324817e-45},
                {"args": [0x42F60000], "expected": 123.0},
            ],
            "hint": "sign = bits >> 31; exp = (bits >> 23) & 0xFF; frac = bits & 0x7FFFFF; для exp > 0 добавьте скрытую единицу: (1 + frac / 2**23) * 2**(exp - 127).",
        },
        {
            "id": "swap-endian",
            "mode": "func",
            "func": "swap_endian32",
            "title": "Смена порядка байтов",
            "statement": (
                "Напишите функцию swap_endian32(n): n — 32-битное беззнаковое "
                "число. Верните число с обратным порядком байтов (из big-endian "
                "в little-endian и наоборот). Используйте сдвиги и маски."
            ),
            "starter": "def swap_endian32(n):\n    pass\n",
            "tests": [
                {"args": [0x12345678], "expected": 0x78563412},
                {"args": [0], "expected": 0},
                {"args": [0xFF], "expected": 0xFF000000},
                {"args": [0xAABBCCDD], "expected": 0xDDCCBBAA},
                {"args": [0x01020304], "expected": 0x04030201},
                {"args": [0xFFFFFFFF], "expected": 0xFFFFFFFF},
            ],
            "hint": "((n & 0xFF) << 24) | ((n >> 8 & 0xFF) << 16) | ((n >> 16 & 0xFF) << 8) | (n >> 24).",
        },
        {
            "id": "fixed-point-mul",
            "mode": "func",
            "func": "fx_mul",
            "title": "Умножение чисел с фиксированной точкой",
            "statement": (
                "В формате Q8.8 число x хранится как целое x·256 (восемь "
                "бит дробной части). Напишите функцию fx_mul(a, b): a и b — "
                "числа в Q8.8, результат — их произведение в том же формате "
                "(дробные биты, которые не помещаются, отбрасываются сдвигом "
                "вправо — то есть округление вниз)."
            ),
            "starter": "def fx_mul(a, b):\n    pass\n",
            "tests": [
                {"args": [384, 576], "expected": 864},
                {"args": [256, 256], "expected": 256},
                {"args": [3, 3], "expected": 0},
                {"args": [-3, 3], "expected": -1},
                {"args": [-384, 576], "expected": -864},
                {"args": [0, 12345], "expected": 0},
            ],
            "hint": "(a * b) >> 8 — произведение двух Q8.8 имеет 16 дробных бит, лишние восемь нужно отбросить.",
        },
    ],
    3: [
        {
            "id": "utf8-encode",
            "mode": "func",
            "func": "utf8_encode",
            "title": "Кодируем символ в UTF-8",
            "statement": (
                "Напишите функцию utf8_encode(cp): cp — кодовая точка "
                "(0…0x10FFFF, суррогатов в тестах нет). Верните список "
                "байтов (чисел 0…255) UTF-8 без использования str.encode "
                "и bytes: через сдвиги и маски по шаблонам 0xxxxxxx, "
                "110xxxxx 10xxxxxx, 1110xxxx 10xxxxxx 10xxxxxx, "
                "11110xxx 10xxxxxx 10xxxxxx 10xxxxxx."
            ),
            "starter": "def utf8_encode(cp):\n    pass\n",
            "tests": [
                {"args": [0x41], "expected": [65]},
                {"args": [0x7F], "expected": [127]},
                {"args": [0x80], "expected": [194, 128]},
                {"args": [0x416], "expected": [208, 150]},
                {"args": [0x7FF], "expected": [223, 191]},
                {"args": [0x800], "expected": [224, 160, 128]},
                {"args": [0x20AC], "expected": [226, 130, 172]},
                {"args": [0xFFFF], "expected": [239, 191, 191]},
                {"args": [0x1F600], "expected": [240, 159, 152, 128]},
                {"args": [0x10FFFF], "expected": [244, 143, 191, 191]},
            ],
            "hint": "Выберите шаблон по диапазону: <0x80, <0x800, <0x10000, иначе. Старшие биты идут в первый байт, по шесть младших — в продолжающие (10xxxxxx).",
        },
        {
            "id": "utf8-decode",
            "mode": "func",
            "func": "utf8_decode",
            "title": "Декодируем UTF-8 вручную",
            "statement": (
                "Напишите функцию utf8_decode(data): data — список байтов "
                "корректного UTF-8. Верните строку, собрав кодовые точки "
                "самостоятельно (bytes.decode и подобное использовать нельзя): "
                "по старшим битам первого байта определите длину символа и "
                "соберите шесть бит из каждого продолжающего байта."
            ),
            "starter": "def utf8_decode(data):\n    pass\n",
            "tests": [
                {"args": [[208, 159, 209, 128, 208, 184, 208, 178, 208, 181, 209, 130]], "expected": "Привет"},
                {"args": [[97, 226, 130, 172, 240, 159, 152, 128]], "expected": "a€😀"},
                {"args": [[]], "expected": ""},
                {"args": [[72, 105]], "expected": "Hi"},
                {"args": [[244, 143, 191, 191]], "expected": "\U0010ffff"},
                {"args": [[194, 128, 223, 191]], "expected": "\u0080߿"},
            ],
            "hint": "Первый байт: <0x80 — один байт; >>5 == 0b110 — два; >>4 == 0b1110 — три; иначе четыре. Данные первого байта — маска 0x1F/0x0F/0x07, дальше cp = (cp << 6) | (b & 0x3F).",
        },
        {
            "id": "utf8-count-chars",
            "mode": "stdout",
            "title": "Сколько символов в байтах",
            "statement": (
                "Напишите функцию count_chars(data): data — список байтов "
                "корректного UTF-8. Верните число символов, не декодируя "
                "строку: достаточно посчитать байты, которые не являются "
                "продолжающими (не начинаются с битов 10). Проверка подаёт "
                "миллион байтов."
            ),
            "starter": "def count_chars(data):\n    pass\n",
            "driver": (
                "print(count_chars([]), count_chars([97, 98]), count_chars(list('привет'.encode())), count_chars(list('a€😀'.encode())))\n"
                "big = list(('Ж€😀x' * 100000).encode())\nprint(len(big), count_chars(big))\n"
            ),
            "expected": ["0 2 6 3", "1000000 400000"],
            "hint": "Продолжающие байты имеют вид 10xxxxxx: (b & 0xC0) == 0x80. Все остальные байты — начало символа.",
        },
        {
            "id": "parity-errors",
            "mode": "func",
            "func": "parity_errors",
            "title": "Проверка чётности",
            "statement": (
                "Напишите функцию parity_errors(words): words — список "
                "строк из нулей и единиц, каждая — слово с битом чётности "
                "(общее число единиц должно быть чётным). Верните список "
                "индексов слов, в которых чётность нарушена."
            ),
            "starter": "def parity_errors(words):\n    pass\n",
            "tests": [
                {"args": [["10110010", "10110011", "00000000", "11111111"]], "expected": [1]},
                {"args": [["1", "0", "11", "111"]], "expected": [0, 3]},
                {"args": [[]], "expected": []},
                {"args": [["0110", "0111", "1000", "1001"]], "expected": [1, 2]},
            ],
            "hint": "Слово верно, если word.count('1') % 2 == 0.",
        },
        {
            "id": "fletcher16",
            "mode": "func",
            "func": "fletcher16",
            "title": "Контрольная сумма Флетчера",
            "statement": (
                "Контрольная сумма Флетчера-16 чувствительна к порядку "
                "байтов. Напишите функцию fletcher16(data): data — список "
                "байтов. s1 = s2 = 0; для каждого байта b: s1 = (s1 + b) % 255; "
                "s2 = (s2 + s1) % 255. Результат: (s2 << 8) | s1."
            ),
            "starter": "def fletcher16(data):\n    pass\n",
            "tests": [
                {"args": [[97, 98, 99, 100, 101]], "expected": 51440},
                {"args": [[97, 98, 99, 100, 101, 102]], "expected": 8279},
                {"args": [[97, 98, 99, 100, 101, 102, 103, 104]], "expected": 1575},
                {"args": [[]], "expected": 0},
                {"args": [[1, 2]], "expected": 1027},
                {"args": [[2, 1]], "expected": 1283},
            ],
            "hint": "Обратите внимание: перестановка байтов [1, 2] и [2, 1] даёт разные значения — в отличие от простой суммы.",
        },
        {
            "id": "crc8-poly07",
            "mode": "func",
            "func": "crc8",
            "title": "CRC-8",
            "statement": (
                "Напишите функцию crc8(data): data — список байтов. "
                "crc = 0; для каждого байта: crc ^= byte; затем восемь "
                "раз: если старший бит crc установлен — crc = ((crc << 1) "
                "^ 0x07) & 0xFF, иначе crc = (crc << 1) & 0xFF. Верните crc."
            ),
            "starter": "def crc8(data):\n    pass\n",
            "tests": [
                {"args": [[49, 50, 51, 52, 53, 54, 55, 56, 57]], "expected": 244},
                {"args": [[]], "expected": 0},
                {"args": [[0]], "expected": 0},
                {"args": [[255]], "expected": 243},
                {"args": [[104, 101, 108, 108, 111]], "expected": 146},
                {"args": [[1, 2, 3]], "expected": 72},
            ],
            "hint": "Это деление многочленов без переносов: сдвиг и иксор с многочленом 0x07, когда выдвигается единица.",
        },
        {
            "id": "hamming74-encode",
            "mode": "func",
            "func": "hamming_encode",
            "title": "Кодирование по Хэммингу (7,4)",
            "statement": (
                "Напишите функцию hamming_encode(d): d — список из четырёх "
                "информационных битов [d1, d2, d3, d4]. Верните список из "
                "семи битов [p1, p2, d1, p3, d2, d3, d4], где p1 = d1^d2^d4, "
                "p2 = d1^d3^d4, p3 = d2^d3^d4."
            ),
            "starter": "def hamming_encode(d):\n    pass\n",
            "tests": [
                {"args": [[1, 0, 1, 1]], "expected": [0, 1, 1, 0, 0, 1, 1]},
                {"args": [[0, 0, 0, 0]], "expected": [0, 0, 0, 0, 0, 0, 0]},
                {"args": [[1, 1, 1, 1]], "expected": [1, 1, 1, 1, 1, 1, 1]},
                {"args": [[0, 1, 0, 1]], "expected": [0, 1, 0, 0, 1, 0, 1]},
                {"args": [[1, 0, 0, 0]], "expected": [1, 1, 1, 0, 0, 0, 0]},
            ],
            "hint": "Позиции битов с 1 по 7: проверочные — на степенях двойки (1, 2, 4), данные — на 3, 5, 6, 7.",
        },
        {
            "id": "hamming74-decode",
            "mode": "func",
            "func": "hamming_decode",
            "title": "Исправление ошибки по Хэммингу",
            "statement": (
                "Напишите функцию hamming_decode(w): w — слово из семи "
                "битов, возможно с одним перевёрнутым. Посчитайте синдром "
                "(s1 = w1^w3^w5^w7, s2 = w2^w3^w6^w7, s3 = w4^w5^w6^w7 — "
                "номера с единицы), позиция ошибки pos = s1 + 2·s2 + 4·s3. "
                "Исправьте бит (если pos > 0) и верните кортеж "
                "(информационные биты [w3, w5, w6, w7], pos)."
            ),
            "starter": "def hamming_decode(w):\n    pass\n",
            "tests": [
                {"args": [[0, 1, 1, 0, 0, 1, 1]], "expected": ([1, 0, 1, 1], 0)},
                {"args": [[1, 1, 1, 0, 0, 1, 1]], "expected": ([1, 0, 1, 1], 1)},
                {"args": [[0, 1, 0, 0, 0, 1, 1]], "expected": ([1, 0, 1, 1], 3)},
                {"args": [[0, 1, 1, 0, 0, 1, 0]], "expected": ([1, 0, 1, 1], 7)},
                {"args": [[0, 1, 0, 0, 0, 0, 1]], "expected": ([0, 1, 0, 1], 5)},
                {"args": [[0, 0, 0, 0, 0, 0, 0]], "expected": ([0, 0, 0, 0], 0)},
            ],
            "hint": "Не меняйте входной список — сделайте копию; исправляется элемент с индексом pos - 1.",
        },
        {
            "id": "min-hamming-distance",
            "mode": "stdout",
            "title": "Минимальное расстояние кода",
            "statement": (
                "Расстояние Хэмминга — число различающихся позиций. Напишите "
                "функцию min_distance(words): words — список целых чисел "
                "(кодовых слов). Верните наименьшее расстояние между двумя "
                "разными словами или -1, если слов меньше двух. Код "
                "исправляет t ошибок, если расстояние не меньше 2t + 1. "
                "Проверка подаёт 3000 слов."
            ),
            "starter": "def min_distance(words):\n    pass\n",
            "driver": (
                "print(min_distance([0b0110011, 0b0000000, 0b1111111]), min_distance([0, 1, 3]), min_distance([5]), min_distance([]))\n"
                "words = [0b0000000, 0b1110100, 0b0111010, 0b0011101, 0b1001110, 0b0100111, 0b1010011, 0b1101001]\nprint(min_distance(words))\n"
                "import random\nrandom.seed(5)\nbig = random.sample(range(1 << 30), 3000)\nprint(min_distance(big))\n"
            ),
            "expected": ["3 1 -1 -1", "4", "2"],
            "hint": "Для каждой пары: bin(a ^ b).count('1'). 3000 слов — это 4,5 млн пар, укладывается в лимит, если держать цикл простым.",
        },
    ],
}
