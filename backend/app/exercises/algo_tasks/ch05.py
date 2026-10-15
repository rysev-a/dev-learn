"""Задачи книги «Алгоритмы и структуры данных»: глава 5."""

TASKS: dict[int, list[dict]] = {
    5: [
        {
            "id": "poly-string-hash",
            "mode": "func",
            "func": "poly_hash",
            "title": "Полиномиальный хеш строки",
            "statement": (
                "Напишите функцию poly_hash(s, base, mod): хеш строки по схеме h = "
                "0; для каждого символа h = (h * base + ord(символ)) % mod. Пустая "
                "строка даёт 0."
            ),
            "starter": "def poly_hash(s, base, mod):\n    pass\n",
            "tests": [
                {"args": ["abc", 31, 1000000007], "expected": 96354},
                {"args": ["", 31, 997], "expected": 0},
                {"args": ["a", 31, 2], "expected": 1},
                {"args": ["hello", 31, 1000000007], "expected": 99162322},
                {"args": ["abc", 31, 100], "expected": 54},
                {"args": ["яблоко", 257, 1000003], "expected": 286210},
                {"args": ["ba", 31, 1000000007], "expected": 3135},
                {"args": ["ab", 31, 1000000007], "expected": 3105},
            ],
            "hint": "Один цикл по символам; остаток берите на каждом шаге — число остаётся небольшим.",
        },
        {
            "id": "window-hashes",
            "mode": "stdout",
            "title": "Хеши всех окон",
            "statement": (
                "Напишите функцию window_hashes(s, k, base, mod): список "
                "полиномиальных хешей (h = h * base + ord(символ), по модулю mod) "
                "всех подстрок длины k слева направо. Для k больше длины строки — "
                "пустой список. Хеш следующего окна считайте из предыдущего за O(1) "
                "(скользящий хеш): проверка подаёт 500 000 символов и окно из 1000."
            ),
            "starter": "def window_hashes(s, k, base, mod):\n    pass\n",
            "driver": (
                "print(window_hashes(\"abcab\", 2, 31, 1000000007))\n"
                "print(window_hashes(\"abc\", 5, 31, 1000000007), window_hashes(\"abc\", 3, 31, 1000000007))\n"
                "text = \"\".join(chr(97 + (i * i + 3 * i) % 26) for i in range(500000))\n"
                "hs = window_hashes(text, 1000, 257, 1000000007)\n"
                "print(len(hs), hs[0], hs[-1], sum(hs) % 1000000007)\n"
            ),
            "expected": ["[3105, 3137, 3166, 3105]", "[] [96354]", "499001 792260583 281438055 700002660"],
            "hint": "Хеш окна — многочлен: вычитаем вклад ушедшего символа ord(s[i-k]) * base**(k-1), умножаем на base и прибавляем код нового. Степень посчитайте один раз: pow(base, k-1, mod).",
        },
        {
            "id": "int-hash-spread",
            "mode": "func",
            "func": "max_bucket",
            "title": "Деление или умножение",
            "statement": (
                "Напишите функцию max_bucket(keys, m, method): разложите целые "
                "ключи по m ячейкам и верните размер самой заполненной. method = "
                "'division' — номер ключа key % m; method = 'multiplication' — "
                "((key * 2654435769) % 4294967296) * m // 4294967296 (константа — "
                "2³² / золотое сечение)."
            ),
            "starter": "def max_bucket(keys, m, method):\n    pass\n",
            "tests": [
                {"args": [[0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120], 8, "division"], "expected": 16},
                {"args": [[0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120], 8, "multiplication"], "expected": 3},
                {"args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99], 10, "division"], "expected": 10},
                {"args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99], 10, "multiplication"], "expected": 11},
                {"args": [[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000, 101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000, 110000, 111000, 112000, 113000, 114000, 115000, 116000, 117000, 118000, 119000, 120000, 121000, 122000, 123000, 124000, 125000, 126000, 127000, 128000, 129000, 130000, 131000, 132000, 133000, 134000, 135000, 136000, 137000, 138000, 139000, 140000, 141000, 142000, 143000, 144000, 145000, 146000, 147000, 148000, 149000, 150000, 151000, 152000, 153000, 154000, 155000, 156000, 157000, 158000, 159000, 160000, 161000, 162000, 163000, 164000, 165000, 166000, 167000, 168000, 169000, 170000, 171000, 172000, 173000, 174000, 175000, 176000, 177000, 178000, 179000, 180000, 181000, 182000, 183000, 184000, 185000, 186000, 187000, 188000, 189000, 190000, 191000, 192000, 193000, 194000, 195000, 196000, 197000, 198000, 199000, 200000, 201000, 202000, 203000, 204000, 205000, 206000, 207000, 208000, 209000, 210000, 211000, 212000, 213000, 214000, 215000, 216000, 217000, 218000, 219000, 220000, 221000, 222000, 223000, 224000, 225000, 226000, 227000, 228000, 229000, 230000, 231000, 232000, 233000, 234000, 235000, 236000, 237000, 238000, 239000, 240000, 241000, 242000, 243000, 244000, 245000, 246000, 247000, 248000, 249000, 250000, 251000, 252000, 253000, 254000, 255000, 256000, 257000, 258000, 259000, 260000, 261000, 262000, 263000, 264000, 265000, 266000, 267000, 268000, 269000, 270000, 271000, 272000, 273000, 274000, 275000, 276000, 277000, 278000, 279000, 280000, 281000, 282000, 283000, 284000, 285000, 286000, 287000, 288000, 289000, 290000, 291000, 292000, 293000, 294000, 295000, 296000, 297000, 298000, 299000, 300000, 301000, 302000, 303000, 304000, 305000, 306000, 307000, 308000, 309000, 310000, 311000, 312000, 313000, 314000, 315000, 316000, 317000, 318000, 319000, 320000, 321000, 322000, 323000, 324000, 325000, 326000, 327000, 328000, 329000, 330000, 331000, 332000, 333000, 334000, 335000, 336000, 337000, 338000, 339000, 340000, 341000, 342000, 343000, 344000, 345000, 346000, 347000, 348000, 349000, 350000, 351000, 352000, 353000, 354000, 355000, 356000, 357000, 358000, 359000, 360000, 361000, 362000, 363000, 364000, 365000, 366000, 367000, 368000, 369000, 370000, 371000, 372000, 373000, 374000, 375000, 376000, 377000, 378000, 379000, 380000, 381000, 382000, 383000, 384000, 385000, 386000, 387000, 388000, 389000, 390000, 391000, 392000, 393000, 394000, 395000, 396000, 397000, 398000, 399000, 400000, 401000, 402000, 403000, 404000, 405000, 406000, 407000, 408000, 409000, 410000, 411000, 412000, 413000, 414000, 415000, 416000, 417000, 418000, 419000, 420000, 421000, 422000, 423000, 424000, 425000, 426000, 427000, 428000, 429000, 430000, 431000, 432000, 433000, 434000, 435000, 436000, 437000, 438000, 439000, 440000, 441000, 442000, 443000, 444000, 445000, 446000, 447000, 448000, 449000, 450000, 451000, 452000, 453000, 454000, 455000, 456000, 457000, 458000, 459000, 460000, 461000, 462000, 463000, 464000, 465000, 466000, 467000, 468000, 469000, 470000, 471000, 472000, 473000, 474000, 475000, 476000, 477000, 478000, 479000, 480000, 481000, 482000, 483000, 484000, 485000, 486000, 487000, 488000, 489000, 490000, 491000, 492000, 493000, 494000, 495000, 496000, 497000, 498000, 499000], 1000, "division"], "expected": 500},
                {"args": [[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000, 101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000, 110000, 111000, 112000, 113000, 114000, 115000, 116000, 117000, 118000, 119000, 120000, 121000, 122000, 123000, 124000, 125000, 126000, 127000, 128000, 129000, 130000, 131000, 132000, 133000, 134000, 135000, 136000, 137000, 138000, 139000, 140000, 141000, 142000, 143000, 144000, 145000, 146000, 147000, 148000, 149000, 150000, 151000, 152000, 153000, 154000, 155000, 156000, 157000, 158000, 159000, 160000, 161000, 162000, 163000, 164000, 165000, 166000, 167000, 168000, 169000, 170000, 171000, 172000, 173000, 174000, 175000, 176000, 177000, 178000, 179000, 180000, 181000, 182000, 183000, 184000, 185000, 186000, 187000, 188000, 189000, 190000, 191000, 192000, 193000, 194000, 195000, 196000, 197000, 198000, 199000, 200000, 201000, 202000, 203000, 204000, 205000, 206000, 207000, 208000, 209000, 210000, 211000, 212000, 213000, 214000, 215000, 216000, 217000, 218000, 219000, 220000, 221000, 222000, 223000, 224000, 225000, 226000, 227000, 228000, 229000, 230000, 231000, 232000, 233000, 234000, 235000, 236000, 237000, 238000, 239000, 240000, 241000, 242000, 243000, 244000, 245000, 246000, 247000, 248000, 249000, 250000, 251000, 252000, 253000, 254000, 255000, 256000, 257000, 258000, 259000, 260000, 261000, 262000, 263000, 264000, 265000, 266000, 267000, 268000, 269000, 270000, 271000, 272000, 273000, 274000, 275000, 276000, 277000, 278000, 279000, 280000, 281000, 282000, 283000, 284000, 285000, 286000, 287000, 288000, 289000, 290000, 291000, 292000, 293000, 294000, 295000, 296000, 297000, 298000, 299000, 300000, 301000, 302000, 303000, 304000, 305000, 306000, 307000, 308000, 309000, 310000, 311000, 312000, 313000, 314000, 315000, 316000, 317000, 318000, 319000, 320000, 321000, 322000, 323000, 324000, 325000, 326000, 327000, 328000, 329000, 330000, 331000, 332000, 333000, 334000, 335000, 336000, 337000, 338000, 339000, 340000, 341000, 342000, 343000, 344000, 345000, 346000, 347000, 348000, 349000, 350000, 351000, 352000, 353000, 354000, 355000, 356000, 357000, 358000, 359000, 360000, 361000, 362000, 363000, 364000, 365000, 366000, 367000, 368000, 369000, 370000, 371000, 372000, 373000, 374000, 375000, 376000, 377000, 378000, 379000, 380000, 381000, 382000, 383000, 384000, 385000, 386000, 387000, 388000, 389000, 390000, 391000, 392000, 393000, 394000, 395000, 396000, 397000, 398000, 399000, 400000, 401000, 402000, 403000, 404000, 405000, 406000, 407000, 408000, 409000, 410000, 411000, 412000, 413000, 414000, 415000, 416000, 417000, 418000, 419000, 420000, 421000, 422000, 423000, 424000, 425000, 426000, 427000, 428000, 429000, 430000, 431000, 432000, 433000, 434000, 435000, 436000, 437000, 438000, 439000, 440000, 441000, 442000, 443000, 444000, 445000, 446000, 447000, 448000, 449000, 450000, 451000, 452000, 453000, 454000, 455000, 456000, 457000, 458000, 459000, 460000, 461000, 462000, 463000, 464000, 465000, 466000, 467000, 468000, 469000, 470000, 471000, 472000, 473000, 474000, 475000, 476000, 477000, 478000, 479000, 480000, 481000, 482000, 483000, 484000, 485000, 486000, 487000, 488000, 489000, 490000, 491000, 492000, 493000, 494000, 495000, 496000, 497000, 498000, 499000], 1000, "multiplication"], "expected": 1},
                {"args": [[], 4, "division"], "expected": 0},
                {"args": [[5], 4, "multiplication"], "expected": 1},
            ],
            "hint": "Заведите список счётчиков длины m; для каждого ключа вычислите номер выбранным способом и прибавьте единицу. Ответ — max(счётчики).",
        },
        {
            "id": "chained-hashmap",
            "mode": "stdout",
            "title": "Хеш-таблица с цепочками",
            "statement": (
                "Реализуйте класс ChainedHashMap(capacity=8, hash_fn=None) — "
                "таблицу с цепочками. Корзины — список списков пар [ключ, "
                "значение]; номер корзины hash_fn(key) % capacity (по умолчанию "
                "hash). Методы: put(key, value) (новый ключ — в конец цепочки, "
                "существующий — обновить), get(key, default=None), remove(key) → "
                "True/False, key in m, len(m), keys(), свойство capacity и "
                "max_chain() — длина самой длинной цепочки. Рост: после вставки "
                "НОВОГО ключа, если len(m) > 0.75 * capacity, вдвое увеличьте число "
                "корзин и вставьте все пары заново (перебирая старые корзины по "
                "порядку, цепочки — слева направо)."
            ),
            "starter": "class ChainedHashMap:\n    def __init__(self, capacity=8, hash_fn=None):\n        self.hash_fn = hash_fn or hash\n        self.buckets = [[] for _ in range(capacity)]\n        self.size = 0\n\n    @property\n    def capacity(self):\n        return len(self.buckets)\n\n    def __len__(self):\n        return self.size\n\n    # put, get, remove, __contains__, keys, max_chain\n",
            "driver": (
                "m = ChainedHashMap(4, hash_fn=lambda k: k)\n"
                "for k in (1, 5, 9, 2):\n"
                "    m.put(k, k * 10)\n"
                "print(m.capacity, len(m), m.max_chain(), m.keys())\n"
                "m.put(5, 55)\n"
                "print(m.get(5), m.get(7), m.get(7, \"нет\"), 9 in m, 3 in m)\n"
                "print(m.remove(9), m.remove(9), len(m), m.keys())\n"
                "m.put(3, 30)\n"
                "print(m.capacity, m.keys())\n"
                "caps = []\n"
                "big = ChainedHashMap()\n"
                "for i in range(2000):\n"
                "    big.put((\"k\", i), i)\n"
                "    if not caps or caps[-1] != big.capacity:\n"
                "        caps.append(big.capacity)\n"
                "print(caps, len(big), big.get((\"k\", 1999)), big.max_chain() < 12)\n"
                "bad = ChainedHashMap(8, hash_fn=lambda k: 0)\n"
                "for i in range(300):\n"
                "    bad.put(i, i)\n"
                "print(bad.max_chain(), all(bad.get(i) == i for i in range(300)))\n"
            ),
            "expected": ["8 4 2 [1, 9, 2, 5]", "55 None нет True False", "True False 3 [1, 2, 5]", "8 [1, 2, 3, 5]", "[8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096] 2000 1999 True", "300 True"],
            "hint": "Рост: соберите все пары, создайте вдвое больше пустых корзин и вставьте пары заново (без повторной проверки роста), иначе порядок и размер разойдутся с эталоном.",
        },
        {
            "id": "linear-probing-map",
            "mode": "stdout",
            "title": "Линейное пробирование",
            "statement": (
                "Реализуйте класс LinearProbingMap(capacity=8, hash_fn=None) — "
                "открытая адресация с линейным пробированием: ячейки start, "
                "start+1, start+2, … по кругу, где start = hash_fn(key) % capacity. "
                "Ячейки — список self.slots: None (пусто), TOMB (надгробие) или "
                "кортеж (ключ, значение). Поля: size — живые ключи, used — живые "
                "ключи плюс надгробия, probes — счётчик осмотренных ячеек. Каждый "
                "осмотр ячейки в get / put / remove увеличивает probes на 1 (от "
                "стартовой до найденного ключа или до первой пустой ячейки "
                "включительно). get идёт мимо надгробий и останавливается на None. "
                "put сначала убеждается, что ключа нет (доходит до None), и "
                "вставляет в первое встретившееся надгробие, а если его не было — в "
                "пустую ячейку (тогда used += 1); существующий ключ обновляется. "
                "remove ставит надгробие (size -= 1). Рост: после вставки НОВОГО "
                "ключа в пустую ячейку (не в надгробие), если used * 2 > capacity, "
                "перестройте таблицу вдвое большего размера: пройдите по старым "
                "ячейкам по возрастанию индекса и вставьте живые пары (надгробия "
                "выбрасываются; probes при перестройке не меняется)."
            ),
            "starter": "TOMB = object()\n\n\nclass LinearProbingMap:\n    def __init__(self, capacity=8, hash_fn=None):\n        self.hash_fn = hash_fn or hash\n        self.slots = [None] * capacity\n        self.size = 0\n        self.used = 0\n        self.probes = 0\n\n    def __len__(self):\n        return self.size\n\n    # put, get, remove, __contains__\n",
            "driver": (
                "def layout(m):\n"
                "    return [(\"T\" if s is TOMB else None if s is None else s[0]) for s in m.slots]\n"
                "\n"
                "\n"
                "m = LinearProbingMap(8, hash_fn=lambda k: k)\n"
                "for k in (5, 13, 21):\n"
                "    m.put(k, k * 10)\n"
                "print(layout(m), m.probes, len(m))\n"
                "m.probes = 0\n"
                "print(m.get(21), m.probes)\n"
                "m.probes = 0\n"
                "print(m.get(29), m.probes)\n"
                "m.probes = 0\n"
                "print(m.remove(13), m.probes, layout(m))\n"
                "m.probes = 0\n"
                "print(m.get(21), m.probes)\n"
                "m.probes = 0\n"
                "m.put(29, 290)\n"
                "print(m.probes, layout(m), len(m), m.used)\n"
                "m.put(6, 60)\n"
                "print(layout(m), len(m), m.used)\n"
                "m = LinearProbingMap(4, hash_fn=lambda k: k)\n"
                "caps = []\n"
                "for k in range(10):\n"
                "    m.put(k, k)\n"
                "    caps.append(len(m.slots))\n"
                "print(caps)\n"
                "for k in range(10):\n"
                "    m.remove(k)\n"
                "print(len(m), len(m.slots), 3 in m)\n"
                "big = LinearProbingMap()\n"
                "x = 1\n"
                "for i in range(100000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    k = x % 5000\n"
                "    if x % 3 == 0:\n"
                "        big.remove(k)\n"
                "    else:\n"
                "        big.put(k, i)\n"
                "print(len(big), len(big.slots), sum(1 for k in range(5000) if k in big))\n"
            ),
            "expected": ["[None, None, None, None, None, 5, 13, 21] 6 3", "210 3", "None 4", "True 2 [None, None, None, None, None, 5, 'T', 21]", "210 3", "4 [None, None, None, None, None, 5, 29, 21] 3 3", "[6, None, None, None, None, 5, 29, 21] 4 4", "[4, 4, 8, 8, 16, 16, 16, 16, 32, 32]", "0 32 False", "3283 16384 3283"],
            "hint": "Один метод поиска _find(key), который возвращает индекс ключа, первого надгробия и пустой ячейки, избавит от дублирования в get/put/remove. Не забывайте считать probes при каждом осмотре ячейки.",
        },
        {
            "id": "quadratic-probing-map",
            "mode": "stdout",
            "title": "Квадратичное пробирование",
            "statement": (
                "Реализуйте класс QuadraticProbingMap(capacity=8, hash_fn=None) — "
                "как LinearProbingMap, но на шаге i (i = 0, 1, 2, …) проверяется "
                "ячейка (start + i·(i+1)//2) % capacity — треугольные смещения 0, "
                "1, 3, 6, 10…; для размера, равного степени двойки, они обходят все "
                "ячейки. Ячейки — список self.slots: None (пусто), TOMB (надгробие) "
                "или кортеж (ключ, значение). Поля: size — живые ключи, used — "
                "живые ключи плюс надгробия, probes — счётчик осмотренных ячеек. "
                "Каждый осмотр ячейки в get / put / remove увеличивает probes на 1 "
                "(от стартовой до найденного ключа или до первой пустой ячейки "
                "включительно). get идёт мимо надгробий и останавливается на None. "
                "put сначала убеждается, что ключа нет (доходит до None), и "
                "вставляет в первое встретившееся надгробие, а если его не было — в "
                "пустую ячейку (тогда used += 1); существующий ключ обновляется. "
                "remove ставит надгробие (size -= 1). Рост: после вставки НОВОГО "
                "ключа в пустую ячейку, если used * 2 > capacity, перестройте "
                "таблицу вдвое большего размера (старые ячейки по возрастанию "
                "индекса, надгробия выбрасываются, probes не меняется)."
            ),
            "starter": "TOMB = object()\n\n\nclass QuadraticProbingMap:\n    def __init__(self, capacity=8, hash_fn=None):\n        self.hash_fn = hash_fn or hash\n        self.slots = [None] * capacity\n        self.size = 0\n        self.used = 0\n        self.probes = 0\n\n    def __len__(self):\n        return self.size\n\n    # put, get, remove, __contains__\n",
            "driver": (
                "def layout(m):\n"
                "    return [(\"T\" if s is TOMB else None if s is None else s[0]) for s in m.slots]\n"
                "\n"
                "\n"
                "m = QuadraticProbingMap(16, hash_fn=lambda k: k)\n"
                "for k in (3, 19, 35, 51, 4):\n"
                "    m.put(k, k)\n"
                "print(layout(m), m.probes)\n"
                "m.probes = 0\n"
                "print(m.get(51), m.probes)\n"
                "m.probes = 0\n"
                "print(m.get(67), m.probes)\n"
                "m.probes = 0\n"
                "print(m.remove(19), layout(m))\n"
                "m.probes = 0\n"
                "print(m.get(35), m.probes, m.get(51), m.probes)\n"
                "m.put(67, 1)\n"
                "print(layout(m), len(m), m.used)\n"
                "m = QuadraticProbingMap(4, hash_fn=lambda k: k)\n"
                "caps = []\n"
                "for k in range(0, 40, 4):\n"
                "    m.put(k, k)\n"
                "    caps.append(len(m.slots))\n"
                "print(caps, len(m))\n"
                "big = QuadraticProbingMap()\n"
                "x = 7\n"
                "for i in range(100000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    k = x % 8000\n"
                "    if x % 4 == 0:\n"
                "        big.remove(k)\n"
                "    else:\n"
                "        big.put(k, i)\n"
                "print(len(big), len(big.slots), sum(1 for k in range(8000) if k in big))\n"
            ),
            "expected": ["[None, None, None, 3, 19, 4, 35, None, None, 51, None, None, None, None, None, None] 12", "51 4", "None 5", "True [None, None, None, 3, 'T', 4, 35, None, None, 51, None, None, None, None, None, None]", "35 3 51 7", "[None, None, None, 3, 67, 4, 35, None, None, 51, None, None, None, None, None, None] 5 5", "[4, 4, 8, 8, 16, 16, 16, 16, 32, 32] 10", "6000 16384 6000"],
            "hint": "Тот же каркас, что и у линейного пробирования, меняется только формула индекса на шаге i: (start + i * (i + 1) // 2) % capacity.",
        },
        {
            "id": "double-hashing-map",
            "mode": "stdout",
            "title": "Двойное хеширование",
            "statement": (
                "Реализуйте класс DoubleHashMap(capacity=11, hash_fn=None) "
                "фиксированного простого размера: на шаге i (i = 0, 1, 2, …) "
                "проверяется ячейка (h + i·step) % capacity, где h = hash_fn(key), "
                "step = 1 + h % (capacity − 1) — второй хеш. Ячейки — список "
                "self.slots: None (пусто), TOMB (надгробие) или кортеж (ключ, "
                "значение). Поля: size — живые ключи, used — живые ключи плюс "
                "надгробия, probes — счётчик осмотренных ячеек. Каждый осмотр "
                "ячейки в get / put / remove увеличивает probes на 1 (от стартовой "
                "до найденного ключа или до первой пустой ячейки включительно). get "
                "идёт мимо надгробий и останавливается на None. put сначала "
                "убеждается, что ключа нет (доходит до None), и вставляет в первое "
                "встретившееся надгробие, а если его не было — в пустую ячейку "
                "(тогда used += 1); существующий ключ обновляется. remove ставит "
                "надгробие (size -= 1). Рост не предусмотрен: если свободной ячейки "
                "(пустой или надгробия) не нашлось и ключа нет — поднимите "
                "OverflowError."
            ),
            "starter": "TOMB = object()\n\n\nclass DoubleHashMap:\n    def __init__(self, capacity=11, hash_fn=None):\n        self.hash_fn = hash_fn or hash\n        self.slots = [None] * capacity\n        self.size = 0\n        self.used = 0\n        self.probes = 0\n\n    def __len__(self):\n        return self.size\n\n    # put, get, remove, __contains__\n",
            "driver": (
                "def layout(m):\n"
                "    return [(\"T\" if s is TOMB else None if s is None else s[0]) for s in m.slots]\n"
                "\n"
                "\n"
                "m = DoubleHashMap(11, hash_fn=lambda k: k)\n"
                "for k in (3, 14, 25, 36):\n"
                "    m.put(k, k)\n"
                "print(layout(m), m.probes)\n"
                "m.probes = 0\n"
                "print(m.get(36), m.probes, m.get(47), m.probes)\n"
                "m.probes = 0\n"
                "print(m.remove(14), layout(m))\n"
                "m.probes = 0\n"
                "print(m.get(25), m.probes)\n"
                "m.put(47, 0)\n"
                "print(layout(m), len(m))\n"
                "for k in range(100, 110):\n"
                "    try:\n"
                "        m.put(k, k)\n"
                "    except OverflowError:\n"
                "        print(\"полна на\", k)\n"
                "        break\n"
                "print(len(m), sum(1 for s in m.slots if s is None))\n"
            ),
            "expected": ["[None, None, None, 3, None, None, None, None, 14, 25, 36] 7", "36 2 None 4", "True [None, None, None, 3, None, None, None, None, 'T', 25, 36]", "25 2", "[47, None, None, 3, None, None, None, None, 'T', 25, 36] 4", "полна на 107", "11 0"],
            "hint": "Шаг второй функции не нулевой и взаимно прост с простым размером, поэтому за capacity проб обходятся все ячейки.",
        },
        {
            "id": "robin-hood-map",
            "mode": "stdout",
            "title": "Хеш-таблица Робин Гуда",
            "statement": (
                "Реализуйте класс RobinHoodMap(capacity=8, hash_fn=None) для целых "
                "ключей: фиксированный размер, линейное пробирование от start = "
                "hash_fn(key) % capacity. Ячейка — None или список [ключ, значение, "
                "d], где d — расстояние до родной ячейки. put: идём по ячейкам с d "
                "= 0, 1, 2, …; пустая — кладём; тот же ключ — обновляем значение; "
                "если d у хозяина ячейки МЕНЬШЕ нашего — меняемся местами и "
                "продолжаем вставлять вытесненного (его d в следующей ячейке — на 1 "
                "больше). get: останавливаемся на пустой ячейке или когда d хозяина "
                "меньше нашего (ключа нет). remove: найдя ключ, сдвиньте назад "
                "следующие ячейки, пока не встретится пустая или ячейка с d = 0. "
                "Каждый осмотр ячейки в put и get прибавляет 1 к probes. При put "
                "нового ключа в полную таблицу — OverflowError (таблица не "
                "меняется)."
            ),
            "starter": "class RobinHoodMap:\n    def __init__(self, capacity=8, hash_fn=None):\n        self.hash_fn = hash_fn or hash\n        self.slots = [None] * capacity\n        self.size = 0\n        self.probes = 0\n\n    def __len__(self):\n        return self.size\n\n    # put, get, remove, __contains__\n",
            "driver": (
                "def layout(m):\n"
                "    return [None if s is None else (s[0], s[2]) for s in m.slots]\n"
                "\n"
                "\n"
                "m = RobinHoodMap(8, hash_fn=lambda k: k)\n"
                "for k in (8, 16, 2, 10, 24):\n"
                "    m.put(k, k)\n"
                "print(layout(m), m.probes, len(m))\n"
                "m.probes = 0\n"
                "print(m.get(24), m.probes, m.get(18), m.probes)\n"
                "m.probes = 0\n"
                "print(m.get(3), m.probes)\n"
                "print(m.remove(16), layout(m), len(m))\n"
                "print(m.remove(99), m.remove(8), layout(m))\n"
                "m.put(24, \"x\")\n"
                "print(m.get(24), len(m))\n"
                "f = RobinHoodMap(4, hash_fn=lambda k: k)\n"
                "for k in (0, 4, 8, 12):\n"
                "    f.put(k, k)\n"
                "print(layout(f))\n"
                "try:\n"
                "    f.put(16, 1)\n"
                "except OverflowError:\n"
                "    print(\"полна\")\n"
                "f.put(8, \"обновили\")\n"
                "print(f.get(8), len(f))\n"
                "big = RobinHoodMap(1024, hash_fn=lambda k: k * 7)\n"
                "x = 5\n"
                "for i in range(700):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    big.put(x % 100000, i)\n"
                "mx = max(s[2] for s in big.slots if s is not None)\n"
                "print(len(big), mx, sum(1 for s in big.slots if s is not None))\n"
                "for k in range(0, 100000, 3):\n"
                "    big.remove(k)\n"
                "print(len(big), all(s is None or (s[0] % 3 != 0) for s in big.slots))\n"
            ),
            "expected": ["[(8, 0), (16, 1), (24, 2), (10, 1), (2, 2), None, None, None] 11 5", "24 3 None 7", "None 3", "True [(8, 0), (24, 1), (10, 0), (2, 1), None, None, None, None] 4", "False True [(24, 0), None, (10, 0), (2, 1), None, None, None, None]", "x 3", "[(0, 0), (4, 1), (8, 2), (12, 3)]", "полна", "обновили 4", "698 7 698", "484 True"],
            "hint": "В put у вытесненного хозяина d относится к ячейке, откуда его выбросили; в следующей ячейке он будет на d + 1. В remove после нахождения ключа тяните назад следующие ячейки, уменьшая их d на 1.",
        },
        {
            "id": "cuckoo-hash",
            "mode": "stdout",
            "title": "Кукушкино хеширование",
            "statement": (
                "Реализуйте класс CuckooHash(capacity=8) для неотрицательных целых "
                "ключей: две таблицы t1 и t2 (списки длины capacity из None или пар "
                "[ключ, значение]); h1(k) = k % capacity, h2(k) = (k // capacity) % "
                "capacity. put: если ключ уже есть — обновить; иначе класть в "
                "t1[h1], выселяя жильца в его t2[h2], выселенного оттуда — обратно "
                "в t1 и так далее, не более 32 выселений; если не получилось — "
                "удвойте capacity и вставьте всё заново (включая оставшегося без "
                "дома). get(key, default=None) проверяет t1[h1], затем t2[h2]; "
                "каждая проверка ячейки увеличивает self.probes, так что поиск "
                "стоит не больше двух проб. Нужны также remove(key) → True/False, "
                "key in m и len(m)."
            ),
            "starter": "class CuckooHash:\n    def __init__(self, capacity=8):\n        self.capacity = capacity\n        self.t1 = [None] * capacity\n        self.t2 = [None] * capacity\n        self.size = 0\n        self.probes = 0\n\n    def __len__(self):\n        return self.size\n\n    # put, get, remove, __contains__\n",
            "driver": (
                "m = CuckooHash(8)\n"
                "n = 3000\n"
                "for k in range(0, n * 7, 7):\n"
                "    m.put(k, k + 1)\n"
                "print(len(m))\n"
                "print(all(m.get(k) == k + 1 for k in range(0, n * 7, 7)))\n"
                "print(all(m.get(k) is None for k in range(1, 2000, 7)))\n"
                "mx = 0\n"
                "for k in list(range(0, 600, 7)) + list(range(1, 600, 7)):\n"
                "    m.probes = 0\n"
                "    m.get(k)\n"
                "    mx = max(mx, m.probes)\n"
                "print(mx <= 2)\n"
                "m.put(0, \"x\")\n"
                "print(m.get(0), len(m), 7 in m, 8 in m)\n"
                "print(m.remove(7), m.remove(7), 7 in m, len(m))\n"
                "w = CuckooHash(4)\n"
                "for k in (0, 16, 32, 48, 64, 80, 96, 112, 128):\n"
                "    w.put(k, k)\n"
                "print(len(w), all(w.get(k) == k for k in (0, 16, 32, 48, 64, 80, 96, 112, 128)))\n"
            ),
            "expected": ["3000", "True", "True", "True", "x 3000 True False", "True False False 2999", "9 True"],
            "hint": "Цикл выселений: item, t1[i] = t1[i], item; если item стал None — готово; иначе то же с t2 по h2(item). После 32 кругов — удвойте capacity и вставьте всё заново, не забыв item.",
        },
        {
            "id": "hashset-on-map",
            "mode": "stdout",
            "title": "Множество на своей таблице",
            "statement": (
                "Хеш-таблица HashMap уже лежит в заготовке (она из предыдущих "
                "упражнений). Постройте на ней класс HashSet: add(x), remove(x) → "
                "True/False, x in s, len(s), union(other), intersection(other), "
                "difference(other) (каждая возвращает НОВЫЙ HashSet) и "
                "to_sorted_list(). Встроенные set, dict и импорты запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\nclass HashSet:\n    def __init__(self):\n        self._map = HashMap()\n\n    # add, remove, __contains__, __len__, union, intersection, difference, to_sorted_list\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "a = HashSet()\n"
                "b = HashSet()\n"
                "for x in [1, 2, 3, 4, 2, 2]:\n"
                "    a.add(x)\n"
                "for x in [3, 4, 5, 6]:\n"
                "    b.add(x)\n"
                "print(len(a), a.to_sorted_list(), 2 in a, 9 in a)\n"
                "print(a.union(b).to_sorted_list(), a.intersection(b).to_sorted_list(), a.difference(b).to_sorted_list(), b.difference(a).to_sorted_list())\n"
                "print(a.remove(1), a.remove(1), a.to_sorted_list())\n"
                "big = HashSet()\n"
                "for i in range(100000):\n"
                "    big.add(i * 3 % 100003)\n"
                "print(len(big), big.intersection(a).to_sorted_list())\n"
            ),
            "expected": ["словари и множества не использованы", "4 [1, 2, 3, 4] True False", "[1, 2, 3, 4, 5, 6] [3, 4] [1, 2] [5, 6]", "True False [2, 3, 4]", "100000 [2, 3, 4]"],
            "hint": "Множество — это таблица, где значение не важно: add кладёт пару (x, True), остальное делегируется таблице. Новые множества стройте, перебирая keys().",
        },
        {
            "id": "word-frequencies",
            "mode": "stdout",
            "title": "Частоты слов",
            "statement": (
                "Напишите функцию word_frequencies(text): частота каждого слова "
                "текста (слова разделены пробелами и переводами строк, регистр "
                "различается) — список пар (слово, число), отсортированный по "
                "убыванию числа, а при равенстве — по слову. Готовая таблица "
                "HashMap лежит в заготовке — используйте только её put / get / "
                "remove / in / len / keys / items. Литералы словарей и множеств, "
                "dict(), set() и импорты запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef word_frequencies(text):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(word_frequencies(\"a b a c b a\"))\n"
                "print(word_frequencies(\"\"), word_frequencies(\"x\"))\n"
                "text = \" \".join(\"w\" + str(i % 1000) for i in range(300000))\n"
                "r = word_frequencies(text)\n"
                "print(len(r), r[0], r[-1])\n"
            ),
            "expected": ["словари и множества не использованы", "[('a', 3), ('b', 2), ('c', 1)]", "[] [('x', 1)]", "1000 ('w0', 300) ('w999', 300)"],
            "hint": "m.put(w, m.get(w, 0) + 1) — вся суть. Затем sorted(m.items(), key=lambda kv: (-kv[1], kv[0])).",
        },
        {
            "id": "two-sum-own-map",
            "mode": "stdout",
            "title": "Два числа с суммой (на своей таблице)",
            "statement": (
                "Напишите функцию two_sum(nums, target): пару индексов (i, j), i < "
                "j, где nums[i] + nums[j] == target. Если пар несколько — берите "
                "ту, у которой наименьший j, а при равенстве — наименьший i. Если "
                "пары нет — None. Проверка подаёт 200 000 чисел: вложенные циклы не "
                "успеют. Готовая таблица HashMap лежит в заготовке — используйте "
                "только её put / get / remove / in / len / keys / items. Литералы "
                "словарей и множеств, dict(), set() и импорты запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef two_sum(nums, target):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(two_sum([2, 7, 11, 15], 9), two_sum([3, 2, 4], 6), two_sum([3, 3], 6), two_sum([5, 5, 1], 6), two_sum([1, 2], 10), two_sum([], 1))\n"
                "big = list(range(200000))\n"
                "print(two_sum(big, 399997), two_sum(big, 500000))\n"
            ),
            "expected": ["словари и множества не использованы", "(0, 1) (1, 2) (0, 1) (0, 2) None None", "(199998, 199999) None"],
            "hint": "Идём слева направо: нужное «target − x» уже встречалось? Тогда пара найдена. Иначе запоминаем x → индекс (только первое вхождение).",
        },
        {
            "id": "first-unique-own-map",
            "mode": "stdout",
            "title": "Первая уникальная буква",
            "statement": (
                "Напишите функцию first_unique(s): индекс первого символа, который "
                "встречается в строке ровно один раз, или −1. Проверка подаёт 500 "
                "000 символов. Готовая таблица HashMap лежит в заготовке — "
                "используйте только её put / get / remove / in / len / keys / "
                "items. Литералы словарей и множеств, dict(), set() и импорты "
                "запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef first_unique(s):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(first_unique(\"leetcode\"), first_unique(\"loveleetcode\"), first_unique(\"aabb\"), first_unique(\"\"), first_unique(\"z\"))\n"
                "s = \"\".join(chr(97 + i % 20) for i in range(250000)) * 2 + \"Z\"\n"
                "print(first_unique(s))\n"
            ),
            "expected": ["словари и множества не использованы", "0 2 -1 -1 0", "500000"],
            "hint": "Два прохода: первый считает частоты, второй возвращает индекс первого символа с частотой 1.",
        },
        {
            "id": "group-anagrams-own-map",
            "mode": "stdout",
            "title": "Группы анаграмм",
            "statement": (
                "Напишите функцию group_anagrams(words): разбейте слова на группы "
                "анаграмм. Результат — список групп; внутри группы слова "
                "отсортированы, группы отсортированы между собой (как списки). "
                "Готовая таблица HashMap лежит в заготовке — используйте только её "
                "put / get / remove / in / len / keys / items. Литералы словарей и "
                "множеств, dict(), set() и импорты запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef group_anagrams(words):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(group_anagrams([\"eat\", \"tea\", \"tan\", \"ate\", \"nat\", \"bat\"]))\n"
                "print(group_anagrams([\"\"]), group_anagrams([\"a\"]), group_anagrams([]))\n"
                "words = [\"\".join(sorted(str(i))) + \"x\" if False else str(i) for i in range(30000)]\n"
                "r = group_anagrams(words)\n"
                "print(len(r), max(len(g) for g in r))\n"
            ),
            "expected": ["словари и множества не использованы", "[['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]", "[['']] [['a']] []", "2207 48"],
            "hint": "Ключ группы — отсортированные буквы слова: «eat» и «tea» дают «aet». Значение — список слов; список можно положить в таблицу и дописывать.",
        },
        {
            "id": "subarray-sum-k-own-map",
            "mode": "stdout",
            "title": "Подмассивы с суммой k",
            "statement": (
                "Напишите функцию count_subarrays(nums, k): сколько непустых подряд "
                "идущих подмассивов имеют сумму k (числа могут быть "
                "отрицательными). Проверка подаёт 200 000 чисел. Готовая таблица "
                "HashMap лежит в заготовке — используйте только её put / get / "
                "remove / in / len / keys / items. Литералы словарей и множеств, "
                "dict(), set() и импорты запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef count_subarrays(nums, k):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(count_subarrays([1, 1, 1], 2), count_subarrays([1, 2, 3], 3), count_subarrays([1, -1, 0], 0), count_subarrays([], 0), count_subarrays([5], 5))\n"
                "x = 3\n"
                "nums = []\n"
                "for _ in range(200000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    nums.append(x % 5 - 2)\n"
                "print(count_subarrays(nums, 3), count_subarrays(nums, 0))\n"
            ),
            "expected": ["словари и множества не использованы", "2 2 3 0 1", "30030654 30462315"],
            "hint": "Префиксная сумма total; нужный подмассив заканчивается здесь, если раньше встречалась префиксная сумма total − k. Таблица хранит, сколько раз встречалась каждая префиксная сумма (сначала 0 встречалась один раз).",
        },
        {
            "id": "longest-consecutive-own-map",
            "mode": "stdout",
            "title": "Самая длинная серия подряд",
            "statement": (
                "Напишите функцию longest_consecutive(nums): длина самой длинной "
                "серии подряд идущих целых (например, 100, 4, 200, 1, 3, 2 → серия "
                "1, 2, 3, 4 длиной 4). Порядок в массиве не важен, дубликаты "
                "возможны. Нужно линейное время: сортировкой не обойдётся — "
                "проверка подаёт 300 000 чисел, а сама серия строится от каждого "
                "начала ровно один раз. Готовая таблица HashMap лежит в заготовке — "
                "используйте только её put / get / remove / in / len / keys / "
                "items. Литералы словарей и множеств, dict(), set() и импорты "
                "запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef longest_consecutive(nums):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(longest_consecutive([100, 4, 200, 1, 3, 2]), longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), longest_consecutive([]), longest_consecutive([5]), longest_consecutive([1, 1, 1]))\n"
                "nums = [(i * 7919) % 300007 for i in range(300000)]\n"
                "print(longest_consecutive(nums))\n"
            ),
            "expected": ["словари и множества не использованы", "4 9 0 1 1", "244574"],
            "hint": "Положите все числа в таблицу. Серию начинайте только с числа, у которого нет x − 1: тогда каждое число посещается не больше двух раз.",
        },
        {
            "id": "isomorphic-own-map",
            "mode": "stdout",
            "title": "Изоморфные строки",
            "statement": (
                "Напишите функцию is_isomorphic(s, t): True, если буквы строки s "
                "можно заменить так, чтобы получилась t, причём каждая буква "
                "заменяется одной и той же буквой, а разные буквы — разными "
                "(взаимно однозначно). Строки одной длины. Нужны две таблицы: s→t и "
                "t→s. Готовая таблица HashMap лежит в заготовке — используйте "
                "только её put / get / remove / in / len / keys / items. Литералы "
                "словарей и множеств, dict(), set() и импорты запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef is_isomorphic(s, t):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(is_isomorphic(\"egg\", \"add\"), is_isomorphic(\"foo\", \"bar\"), is_isomorphic(\"paper\", \"title\"), is_isomorphic(\"ab\", \"aa\"), is_isomorphic(\"\", \"\"), is_isomorphic(\"a\", \"ab\"))\n"
                "s = \"\".join(chr(97 + i % 26) for i in range(300000))\n"
                "t = \"\".join(chr(65 + i % 26) for i in range(300000))\n"
                "print(is_isomorphic(s, t), is_isomorphic(s, t[:-1] + \"a\"))\n"
            ),
            "expected": ["словари и множества не использованы", "True False True False True False", "True False"],
            "hint": "Достаточно двух таблиц: что стоит на месте буквы x в t (a) и что стоит на месте буквы y в s (b); любое противоречие — False.",
        },
        {
            "id": "lru-own-map",
            "mode": "stdout",
            "title": "LRU-кэш на своей таблице",
            "statement": (
                "Реализуйте класс LRUCache(capacity): get(key) → значение или −1 "
                "(обращение делает ключ самым свежим); put(key, value) — добавить "
                "или обновить (тоже освежает); при превышении capacity вытесняется "
                "самый давний ключ. Обе операции за O(1): таблица HashMap хранит "
                "узлы двусвязного списка DNode, список упорядочивает ключи по "
                "свежести (дозорные в начале и в конце помогут). Готовая таблица "
                "HashMap лежит в заготовке — используйте только её put / get / "
                "remove / in / len / keys / items. Литералы словарей и множеств, "
                "dict(), set() и импорты запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\nclass DNode:\n    def __init__(self, key=None, value=None):\n        self.key = key\n        self.value = value\n        self.prev = None\n        self.next = None\n\n\nclass LRUCache:\n    def __init__(self, capacity):\n        self.capacity = capacity\n        self.table = HashMap()\n        self.head = DNode()\n        self.tail = DNode()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n\n    # get, put (и вспомогательные методы работы со списком)\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "c = LRUCache(2)\n"
                "c.put(1, 1)\n"
                "c.put(2, 2)\n"
                "print(c.get(1))\n"
                "c.put(3, 3)\n"
                "print(c.get(2))\n"
                "c.put(4, 4)\n"
                "print(c.get(1), c.get(3), c.get(4))\n"
                "c.put(4, 40)\n"
                "print(c.get(4), len(c.table))\n"
                "big = LRUCache(1000)\n"
                "x = 11\n"
                "total = 0\n"
                "for i in range(200000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    k = x % 1500\n"
                "    if x % 2:\n"
                "        big.put(k, i)\n"
                "    else:\n"
                "        total += big.get(k)\n"
                "print(total, len(big.table))\n"
            ),
            "expected": ["словари и множества не использованы", "1", "-1", "-1 3 4", "40 2", "-100000 750"],
            "hint": "get: найти узел в таблице, вырезать из списка, вставить после head. put: если ключ есть — обновить и освежить; иначе при переполнении удалить tail.prev (и из списка, и из таблицы), затем вставить новый узел.",
        },
        {
            "id": "top-k-own-map",
            "mode": "stdout",
            "title": "k самых частых",
            "statement": (
                "Напишите функцию top_k(nums, k): k самых частых значений массива в "
                "порядке убывания частоты, при равенстве частот — по возрастанию "
                "значения. Гарантируется, что k не больше числа различных значений. "
                "Считайте частоты в таблице. Проверка подаёт 300 000 чисел. Готовая "
                "таблица HashMap лежит в заготовке — используйте только её put / "
                "get / remove / in / len / keys / items. Литералы словарей и "
                "множеств, dict(), set() и импорты запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef top_k(nums, k):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(top_k([1, 1, 1, 2, 2, 3], 2), top_k([4], 1), top_k([5, 5, 6, 6, 7], 3))\n"
                "nums = [(i * i) % 997 for i in range(300000)]\n"
                "print(top_k(nums, 5))\n"
            ),
            "expected": ["словари и множества не использованы", "[1, 2] [4] [5, 6, 7]", "[3, 10, 12, 13, 14]"],
            "hint": "Частоты — в таблице; затем отсортируйте items() по (−частота, значение) и возьмите первые k значений.",
        },
        {
            "id": "nearby-duplicate-own-map",
            "mode": "stdout",
            "title": "Близкие дубликаты",
            "statement": (
                "Напишите функцию contains_nearby_duplicate(nums, k): True, если "
                "есть два разных индекса i и j с nums[i] == nums[j] и |i − j| ≤ k. "
                "Таблица хранит последний индекс каждого значения. Проверка подаёт "
                "400 000 чисел. Готовая таблица HashMap лежит в заготовке — "
                "используйте только её put / get / remove / in / len / keys / "
                "items. Литералы словарей и множеств, dict(), set() и импорты "
                "запрещены."
            ),
            "starter": "class HashMap:\n    \"\"\"Хеш-таблица с цепочками: put / get / remove / in / len / keys / items.\"\"\"\n\n    def __init__(self, capacity=8):\n        self._buckets = [[] for _ in range(capacity)]\n        self._size = 0\n\n    def _bucket(self, key):\n        return self._buckets[hash(key) % len(self._buckets)]\n\n    def put(self, key, value):\n        bucket = self._bucket(key)\n        for pair in bucket:\n            if pair[0] == key:\n                pair[1] = value\n                return\n        bucket.append([key, value])\n        self._size += 1\n        if self._size > 0.75 * len(self._buckets):\n            self._grow()\n\n    def get(self, key, default=None):\n        for k, v in self._bucket(key):\n            if k == key:\n                return v\n        return default\n\n    def remove(self, key):\n        bucket = self._bucket(key)\n        for i, pair in enumerate(bucket):\n            if pair[0] == key:\n                del bucket[i]\n                self._size -= 1\n                return True\n        return False\n\n    def __contains__(self, key):\n        for k, _ in self._bucket(key):\n            if k == key:\n                return True\n        return False\n\n    def __len__(self):\n        return self._size\n\n    def keys(self):\n        return [k for b in self._buckets for k, _ in b]\n\n    def items(self):\n        return [(k, v) for b in self._buckets for k, v in b]\n\n    def _grow(self):\n        old = self.items()\n        self._buckets = [[] for _ in range(2 * len(self._buckets))]\n        self._size = 0\n        for k, v in old:\n            self.put(k, v)\n\n\ndef contains_nearby_duplicate(nums, k):\n    pass\n",
            "driver": (
                "import ast as _ast\n"
                "try:\n"
                "    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n"
                "except OSError:\n"
                "    _src = \"\"\n"
                "_bad = set()\n"
                "for _top in _ast.parse(_src).body:\n"
                "    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n"
                "        continue\n"
                "    for _n in _ast.walk(_top):\n"
                "        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n"
                "            _bad.add(\"литерал словаря или множества\")\n"
                "        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n"
                "            _bad.add(_n.func.id + \"()\")\n"
                "        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n"
                "            _bad.add(\"import\")\n"
                "print(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\n"
                "print(contains_nearby_duplicate([1, 2, 3, 1], 3), contains_nearby_duplicate([1, 0, 1, 1], 1), contains_nearby_duplicate([1, 2, 3, 1, 2, 3], 2), contains_nearby_duplicate([], 5), contains_nearby_duplicate([7], 0))\n"
                "nums = list(range(400000))\n"
                "print(contains_nearby_duplicate(nums, 100000), contains_nearby_duplicate(nums + [0], 399999), contains_nearby_duplicate(nums + [0], 400000))\n"
            ),
            "expected": ["словари и множества не использованы", "True True False False False", "False False True"],
            "hint": "Идём по массиву и помним последний индекс каждого значения. Нашли значение, виденное не дальше k шагов назад — ответ True.",
        },
    ],
}
