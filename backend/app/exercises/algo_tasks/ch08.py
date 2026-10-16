"""Задачи книги «Алгоритмы и структуры данных»: глава 8."""

TASKS: dict[int, list[dict]] = {
    8: [
        {'id': 'str-find-first',
         'mode': 'func',
         'func': 'find_first',
         'title': 'Первое вхождение: наивный поиск',
         'statement': 'Напишите функцию find_first(text, pat): индекс первого вхождения образца pat в '
                      'строку text или -1, если его нет. Пустой образец встречается в позиции 0. Решите '
                      'двумя вложенными циклами: сдвиг и посимвольное сравнение, без find, index и in.',
         'starter': 'def find_first(text, pat):\n    pass\n',
         'tests': [{'args': ['hello world', 'o w'], 'expected': 4},
                   {'args': ['aaa', 'aaaa'], 'expected': -1},
                   {'args': ['abc', ''], 'expected': 0},
                   {'args': ['', 'a'], 'expected': -1},
                   {'args': ['abcabcd', 'abcd'], 'expected': 3},
                   {'args': ['aaaaab', 'aab'], 'expected': 3}],
         'hint': 'Для каждого сдвига i сравнивайте text[i + j] и pat[j], пока символы равны; дошли до '
                 'длины образца — нашли.'},
        {'id': 'str-common-prefix',
         'mode': 'func',
         'func': 'common_prefix',
         'title': 'Общее начало слов',
         'statement': 'Напишите функцию common_prefix(words): наибольшее общее начало всех слов списка. '
                      'Для пустого списка или если общего начала нет — пустая строка.',
         'starter': 'def common_prefix(words):\n    pass\n',
         'tests': [{'args': [['flower', 'flow', 'flight']], 'expected': 'fl'},
                   {'args': [['dog', 'racecar']], 'expected': ''},
                   {'args': [[]], 'expected': ''},
                   {'args': [['same', 'same']], 'expected': 'same'},
                   {'args': [['a']], 'expected': 'a'},
                   {'args': [['ab', 'abc', 'a']], 'expected': 'a'}],
         'hint': 'Возьмите первое слово как образец и укорачивайте длину общего начала по каждому '
                 'следующему слову.'},
        {'id': 'str-count-overlap',
         'mode': 'func',
         'func': 'count_overlapping',
         'title': 'Сколько раз встречается, включая перекрытия',
         'statement': 'Напишите функцию count_overlapping(text, pat): число вхождений образца pat (он '
                      'непустой) в text, при этом вхождения могут перекрываться: в «aaaa» образец «aa» '
                      'встречается три раза.',
         'starter': 'def count_overlapping(text, pat):\n    pass\n',
         'tests': [{'args': ['aaaa', 'aa'], 'expected': 3},
                   {'args': ['abababa', 'aba'], 'expected': 3},
                   {'args': ['abc', 'd'], 'expected': 0},
                   {'args': ['a', 'a'], 'expected': 1},
                   {'args': ['mississippi', 'issi'], 'expected': 2},
                   {'args': ['xyz', 'xyzxyz'], 'expected': 0}],
         'hint': 'После каждого найденного вхождения сдвигайтесь всего на одну позицию, а не на длину '
                 'образца.'},
        {'id': 'str-prefix-function',
         'mode': 'func',
         'func': 'prefix_function',
         'title': 'Префикс-функция',
         'statement': 'Напишите функцию prefix_function(s): список p той же длины, где p[i] — длина '
                      'наибольшего собственного префикса подстроки s[0..i], совпадающего с её суффиксом. '
                      'Для «abacaba» ответ [0, 0, 1, 0, 1, 2, 3]. Время — линейное.',
         'starter': 'def prefix_function(s):\n    pass\n',
         'tests': [{'args': ['abacaba'], 'expected': [0, 0, 1, 0, 1, 2, 3]},
                   {'args': ['aaaa'], 'expected': [0, 1, 2, 3]},
                   {'args': ['abcd'], 'expected': [0, 0, 0, 0]},
                   {'args': ['abababab'], 'expected': [0, 0, 1, 2, 3, 4, 5, 6]},
                   {'args': [''], 'expected': []},
                   {'args': ['a'], 'expected': [0]},
                   {'args': ['aabaaab'], 'expected': [0, 1, 0, 1, 2, 2, 3]}],
         'hint': 'Держите k — текущую длину совпадения; при несовпадении откатывайтесь: k = p[k - 1].'},
        {'id': 'str-longest-border',
         'mode': 'func',
         'func': 'longest_border',
         'title': 'Самая длинная граница',
         'statement': 'Граница строки — собственный префикс, равный суффиксу. Напишите функцию '
                      'longest_border(s): самая длинная граница в виде строки (пустая, если границ нет). '
                      'Для «abacaba» это «aba».',
         'starter': 'def longest_border(s):\n    pass\n',
         'tests': [{'args': ['abacaba'], 'expected': 'aba'},
                   {'args': ['abcd'], 'expected': ''},
                   {'args': ['aaaa'], 'expected': 'aaa'},
                   {'args': ['abab'], 'expected': 'ab'},
                   {'args': [''], 'expected': ''},
                   {'args': ['xyxyxyx'], 'expected': 'xyxyx'}],
         'hint': 'Последнее значение префикс-функции — длина самой длинной границы.'},
        {'id': 'str-min-period',
         'mode': 'func',
         'func': 'min_period',
         'title': 'Наименьший период',
         'statement': 'Напишите функцию min_period(s): наименьшая длина p, при которой строка целиком '
                      'состоит из повторений своих первых p символов (p делит длину). Если такого p меньше '
                      'длины нет, ответ — длина строки; для пустой строки — 0. Например, для «abcabcabc» '
                      'ответ 3, для «abcab» — 5.',
         'starter': 'def min_period(s):\n    pass\n',
         'tests': [{'args': ['abcabcabc'], 'expected': 3},
                   {'args': ['abcab'], 'expected': 5},
                   {'args': ['aaaa'], 'expected': 1},
                   {'args': ['abab'], 'expected': 2},
                   {'args': ['a'], 'expected': 1},
                   {'args': [''], 'expected': 0},
                   {'args': ['abaaba'], 'expected': 3},
                   {'args': ['abaab'], 'expected': 5}],
         'hint': 'Кандидат в периоды — длина минус последнее значение префикс-функции; проверьте, что он '
                 'делит длину.'},
        {'id': 'str-kmp-search',
         'mode': 'stdout',
         'title': 'Поиск Кнута — Морриса — Пратта',
         'statement': 'Напишите функцию find_all(text, pat): список начал всех вхождений образца в текст '
                      '(с перекрытиями) по возрастанию. Пустой образец встречается в каждой позиции от 0 '
                      'до len(text). Время — порядка n + m: проверка подаёт текст в миллион символов и '
                      'образец в триста тысяч. Запрещены find, index, count, startswith, split, replace, '
                      'in и re.',
         'starter': 'def find_all(text, pat):\n    pass\n',
         'driver': 'import ast as _ast\n'
                   '_src = open("/sandbox/solution.py", encoding="utf-8").read()\n'
                   '_bad = set()\n'
                   'for _n in _ast.walk(_ast.parse(_src)):\n'
                   "    if isinstance(_n, _ast.Attribute) and _n.attr in {'endswith', 'find', 'replace', "
                   "'rfind', 'split', 'rindex', 'partition', 'startswith', 'index', 'count'}:\n"
                   '        _bad.add("." + _n.attr + "()")\n'
                   '    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, '
                   '_ast.NotIn)) for _o in _n.ops):\n'
                   '        _bad.add("in")\n'
                   '    elif False and isinstance(_n, _ast.Slice):\n'
                   '        _bad.add("срезы")\n'
                   '    elif isinstance(_n, _ast.Import) and any(_a.name.split(".")[0] in {\'re\'} for _a '
                   'in _n.names):\n'
                   '        _bad.add("import")\n'
                   '    elif isinstance(_n, _ast.ImportFrom) and (_n.module or "").split(".")[0] in '
                   "{'re'}:\n"
                   '        _bad.add("import")\n'
                   'if _bad:\n'
                   '    print("запрещённые приёмы:", ", ".join(sorted(_bad)))\n'
                   'else:\n'
                   '    print(find_all("abracadabra", "abra"), find_all("aaaa", "aa"), find_all("abc", '
                   '"d"), find_all("abc", ""))\n'
                   '    big = "a" * 1000000\n'
                   '    print(len(find_all(big, "a" * 300000 + "b")))\n'
                   '    r = find_all(big, "a" * 300000)\n'
                   '    print(len(r), r[0], r[-1])\n'
                   '    r = find_all("ab" * 400000, "abab")\n'
                   '    print(len(r), r[1], r[-1])\n',
         'expected': ['[0, 7] [0, 1, 2] [] [0, 1, 2, 3]', '0', '700001 0 700000', '399999 2 799996'],
         'hint': 'Постройте префикс-функцию образца, затем идите по тексту: указатель по тексту не '
                 'возвращается, k откатывается по таблице.'},
        {'id': 'str-prefix-occurrences',
         'mode': 'func',
         'func': 'prefix_occurrences',
         'title': 'Сколько раз встречается каждый префикс',
         'statement': 'Напишите функцию prefix_occurrences(s): список ans, где ans[l - 1] — сколько раз '
                      'префикс длины l встречается в s как подстрока (с перекрытиями). Для «abab» ответ '
                      '[2, 2, 1, 1]. Время — линейное.',
         'starter': 'def prefix_occurrences(s):\n    pass\n',
         'tests': [{'args': ['abab'], 'expected': [2, 2, 1, 1]},
                   {'args': ['aaa'], 'expected': [3, 2, 1]},
                   {'args': ['abc'], 'expected': [1, 1, 1]},
                   {'args': ['abacaba'], 'expected': [4, 2, 2, 1, 1, 1, 1]},
                   {'args': [''], 'expected': []},
                   {'args': ['a'], 'expected': [1]},
                   {'args': ['aabaab'], 'expected': [4, 2, 2, 1, 1, 1]}],
         'hint': 'Каждое значение префикс-функции — вхождение префикса этой длины; затем «протолкните» '
                 'счётчики по цепочке p[l - 1].'},
        {'id': 'str-is-rotation',
         'mode': 'stdout',
         'title': 'Циклический сдвиг',
         'statement': 'Напишите функцию is_rotation(a, b): можно ли получить b циклическим сдвигом a. '
                      'Время — линейное: проверка подаёт строки по пятьсот тысяч символов. Запрещены '
                      'срезы, find, index, count, startswith, split, replace, in и re.',
         'starter': 'def is_rotation(a, b):\n    pass\n',
         'driver': 'import ast as _ast\n'
                   '_src = open("/sandbox/solution.py", encoding="utf-8").read()\n'
                   '_bad = set()\n'
                   'for _n in _ast.walk(_ast.parse(_src)):\n'
                   "    if isinstance(_n, _ast.Attribute) and _n.attr in {'endswith', 'find', 'replace', "
                   "'rfind', 'split', 'rindex', 'partition', 'startswith', 'index', 'count'}:\n"
                   '        _bad.add("." + _n.attr + "()")\n'
                   '    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, '
                   '_ast.NotIn)) for _o in _n.ops):\n'
                   '        _bad.add("in")\n'
                   '    elif True and isinstance(_n, _ast.Slice):\n'
                   '        _bad.add("срезы")\n'
                   '    elif isinstance(_n, _ast.Import) and any(_a.name.split(".")[0] in {\'re\'} for _a '
                   'in _n.names):\n'
                   '        _bad.add("import")\n'
                   '    elif isinstance(_n, _ast.ImportFrom) and (_n.module or "").split(".")[0] in '
                   "{'re'}:\n"
                   '        _bad.add("import")\n'
                   'if _bad:\n'
                   '    print("запрещённые приёмы:", ", ".join(sorted(_bad)))\n'
                   'else:\n'
                   '    print(is_rotation("abcde", "cdeab"), is_rotation("abcde", "abced"), '
                   'is_rotation("", ""), is_rotation("a", "ab"))\n'
                   '    a = "a" * 500000 + "b"\n'
                   '    print(is_rotation(a, "a" * 300000 + "b" + "a" * 200000))\n'
                   '    print(is_rotation(a, "a" * 500000 + "c"))\n'
                   '    print(is_rotation("ab" * 250000, "ba" * 250000))\n',
         'expected': ['True False True False', 'True', 'False', 'True'],
         'hint': 'b — сдвиг a, если b встречается в склейке a + a; ищите её префикс-функцией, не создавая '
                 'лишних копий.'},
        {'id': 'str-shortest-palindrome',
         'mode': 'stdout',
         'title': 'Кратчайший палиндром приписыванием',
         'statement': 'Напишите функцию shortest_palindrome(s): припишите к s слева минимальное число '
                      'символов так, чтобы получился палиндром, и верните результат. Для «abcd» ответ '
                      '«dcbabcd». Время — линейное: проверка подаёт строку в четыреста тысяч символов. '
                      'Запрещены find, index, count, startswith, split, replace, in и re.',
         'starter': 'def shortest_palindrome(s):\n    pass\n',
         'driver': 'import ast as _ast\n'
                   '_src = open("/sandbox/solution.py", encoding="utf-8").read()\n'
                   '_bad = set()\n'
                   'for _n in _ast.walk(_ast.parse(_src)):\n'
                   "    if isinstance(_n, _ast.Attribute) and _n.attr in {'endswith', 'find', 'replace', "
                   "'rfind', 'split', 'rindex', 'partition', 'startswith', 'index', 'count'}:\n"
                   '        _bad.add("." + _n.attr + "()")\n'
                   '    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, '
                   '_ast.NotIn)) for _o in _n.ops):\n'
                   '        _bad.add("in")\n'
                   '    elif False and isinstance(_n, _ast.Slice):\n'
                   '        _bad.add("срезы")\n'
                   '    elif isinstance(_n, _ast.Import) and any(_a.name.split(".")[0] in {\'re\'} for _a '
                   'in _n.names):\n'
                   '        _bad.add("import")\n'
                   '    elif isinstance(_n, _ast.ImportFrom) and (_n.module or "").split(".")[0] in '
                   "{'re'}:\n"
                   '        _bad.add("import")\n'
                   'if _bad:\n'
                   '    print("запрещённые приёмы:", ", ".join(sorted(_bad)))\n'
                   'else:\n'
                   '    print(shortest_palindrome("aacecaaa"), shortest_palindrome("abcd"), '
                   'repr(shortest_palindrome("")), shortest_palindrome("a"))\n'
                   '    r = shortest_palindrome("abcd" * 100000)\n'
                   '    print(len(r), r[:6], r[-6:])\n'
                   '    r = shortest_palindrome("a" * 200000 + "b")\n'
                   '    print(len(r), r[:3], r[-3:])\n',
         'expected': ["aaacecaaa dcbabcd '' a", '799999 dcbadc cdabcd', '200002 baa aab'],
         'hint': 'Найдите самый длинный палиндромный префикс: префикс-функция строки s + разделитель + '
                 'развёрнутая s.'},
        {'id': 'str-z-function',
         'mode': 'func',
         'func': 'z_function',
         'title': 'Зет-функция',
         'statement': 'Напишите функцию z_function(s): список z, где z[i] — длина наибольшего общего '
                      'начала строки s и её суффикса, начинающегося в позиции i. Значение z[0] считаем '
                      'равным 0. Для «aabxaab» ответ [0, 1, 0, 0, 3, 1, 0]. Время — линейное.',
         'starter': 'def z_function(s):\n    pass\n',
         'tests': [{'args': ['aabxaab'], 'expected': [0, 1, 0, 0, 3, 1, 0]},
                   {'args': ['aaaa'], 'expected': [0, 3, 2, 1]},
                   {'args': ['abc'], 'expected': [0, 0, 0]},
                   {'args': [''], 'expected': []},
                   {'args': ['a'], 'expected': [0]},
                   {'args': ['abababab'], 'expected': [0, 0, 6, 0, 4, 0, 2, 0]},
                   {'args': ['aabaaab'], 'expected': [0, 1, 0, 2, 3, 1, 0]}],
         'hint': 'Храните зет-блок [l, r): внутри него начинайте с min(r − i, z[i − l]), затем расширяйте '
                 'посимвольно.'},
        {'id': 'str-z-search',
         'mode': 'stdout',
         'title': 'Поиск через зет-функцию',
         'statement': 'Напишите функцию z_count(text, pat): число вхождений непустого образца в текст (с '
                      'перекрытиями) через зет-функцию склейки pat + разделитель + text. Время — линейное: '
                      'проверка подаёт текст в миллион символов. Запрещены find, index, count, startswith, '
                      'split, replace, in и re.',
         'starter': 'def z_count(text, pat):\n    pass\n',
         'driver': 'import ast as _ast\n'
                   '_src = open("/sandbox/solution.py", encoding="utf-8").read()\n'
                   '_bad = set()\n'
                   'for _n in _ast.walk(_ast.parse(_src)):\n'
                   "    if isinstance(_n, _ast.Attribute) and _n.attr in {'endswith', 'find', 'replace', "
                   "'rfind', 'split', 'rindex', 'partition', 'startswith', 'index', 'count'}:\n"
                   '        _bad.add("." + _n.attr + "()")\n'
                   '    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, '
                   '_ast.NotIn)) for _o in _n.ops):\n'
                   '        _bad.add("in")\n'
                   '    elif False and isinstance(_n, _ast.Slice):\n'
                   '        _bad.add("срезы")\n'
                   '    elif isinstance(_n, _ast.Import) and any(_a.name.split(".")[0] in {\'re\'} for _a '
                   'in _n.names):\n'
                   '        _bad.add("import")\n'
                   '    elif isinstance(_n, _ast.ImportFrom) and (_n.module or "").split(".")[0] in '
                   "{'re'}:\n"
                   '        _bad.add("import")\n'
                   'if _bad:\n'
                   '    print("запрещённые приёмы:", ", ".join(sorted(_bad)))\n'
                   'else:\n'
                   '    print(z_count("abracadabra", "abra"), z_count("aaaa", "aa"), z_count("abc", "d"))\n'
                   '    big = "a" * 1000000\n'
                   '    print(z_count(big, "a" * 300000), z_count(big, "a" * 300000 + "b"))\n'
                   '    print(z_count("ab" * 500000, "abab"))\n',
         'expected': ['2 3 0', '700001 0', '499999'],
         'hint': 'z[i] == len(pat) на позиции i > len(pat) означает вхождение; разделитель не даёт z '
                 'вырасти больше длины образца.'},
        {'id': 'str-hash-substring',
         'mode': 'stdout',
         'title': 'Хеш подстроки за константу',
         'statement': 'Напишите класс SubHash: конструктор SubHash(s) считает хеши префиксов; метод get(l, '
                      'r) возвращает хеш подстроки s[l:r] за O(1), метод same(l1, l2, length) — True, если '
                      'подстроки s[l1:l1+length] и s[l2:l2+length] равны (сравнение по хешам, без срезов). '
                      'Используйте большой модуль, например 2^61 − 1. Проверка: строка в девятьсот тысяч '
                      'символов и двести тысяч запросов. Запрещены срезы, find, index, count, startswith, '
                      'split, replace, in и re.',
         'starter': 'class SubHash:\n'
                    '    def __init__(self, s):\n'
                    '        pass\n'
                    '\n'
                    '    def get(self, l, r):\n'
                    '        pass\n'
                    '\n'
                    '    def same(self, l1, l2, length):\n'
                    '        pass\n',
         'driver': 'import ast as _ast\n'
                   '_src = open("/sandbox/solution.py", encoding="utf-8").read()\n'
                   '_bad = set()\n'
                   'for _n in _ast.walk(_ast.parse(_src)):\n'
                   "    if isinstance(_n, _ast.Attribute) and _n.attr in {'endswith', 'find', 'replace', "
                   "'rfind', 'split', 'rindex', 'partition', 'startswith', 'index', 'count'}:\n"
                   '        _bad.add("." + _n.attr + "()")\n'
                   '    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, '
                   '_ast.NotIn)) for _o in _n.ops):\n'
                   '        _bad.add("in")\n'
                   '    elif True and isinstance(_n, _ast.Slice):\n'
                   '        _bad.add("срезы")\n'
                   '    elif isinstance(_n, _ast.Import) and any(_a.name.split(".")[0] in {\'re\'} for _a '
                   'in _n.names):\n'
                   '        _bad.add("import")\n'
                   '    elif isinstance(_n, _ast.ImportFrom) and (_n.module or "").split(".")[0] in '
                   "{'re'}:\n"
                   '        _bad.add("import")\n'
                   'if _bad:\n'
                   '    print("запрещённые приёмы:", ", ".join(sorted(_bad)))\n'
                   'else:\n'
                   '    t = SubHash("abracadabra")\n'
                   '    print(t.same(0, 7, 4), t.same(1, 8, 3), t.same(0, 3, 2), t.same(2, 9, 0))\n'
                   '    def nxt(x):\n'
                   '        x ^= (x << 13) & 0xFFFFFFFF\n'
                   '        x ^= x >> 17\n'
                   '        x ^= (x << 5) & 0xFFFFFFFF\n'
                   '        return x\n'
                   '    s = "abc" * 300000\n'
                   '    h = SubHash(s)\n'
                   '    n = len(s)\n'
                   '    x = 12345\n'
                   '    total = 0\n'
                   '    for _ in range(200000):\n'
                   '        x = nxt(x)\n'
                   '        l1 = x % n\n'
                   '        x = nxt(x)\n'
                   '        l2 = x % n\n'
                   '        x = nxt(x)\n'
                   '        length = x % (n - max(l1, l2) + 1)\n'
                   '        if h.same(l1, l2, length):\n'
                   '            total += 1\n'
                   '    print(total)\n',
         'expected': ['True True False True', '66636'],
         'hint': 'H[i + 1] = (H[i] · B + код символа) mod M; хеш [l, r) = H[r] − H[l] · B^(r − l) mod M.'},
        {'id': 'str-rabin-karp',
         'mode': 'stdout',
         'title': 'Алгоритм Рабина — Карпа',
         'statement': 'Напишите функцию rabin_karp(text, pat): индекс первого вхождения pat в text или -1; '
                      'пустой образец — 0. Считайте хеш образца и скользящий хеш окна (модуль большой, '
                      'например 2^61 − 1), а при равенстве хешей сверяйте строки. Проверка: текст в '
                      'миллион символов и образец в триста тысяч. Запрещены срезы, find, index, count, '
                      'startswith, split, replace, in и re.',
         'starter': 'def rabin_karp(text, pat):\n    pass\n',
         'driver': 'import ast as _ast\n'
                   '_src = open("/sandbox/solution.py", encoding="utf-8").read()\n'
                   '_bad = set()\n'
                   'for _n in _ast.walk(_ast.parse(_src)):\n'
                   "    if isinstance(_n, _ast.Attribute) and _n.attr in {'endswith', 'find', 'replace', "
                   "'rfind', 'split', 'rindex', 'partition', 'startswith', 'index', 'count'}:\n"
                   '        _bad.add("." + _n.attr + "()")\n'
                   '    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, '
                   '_ast.NotIn)) for _o in _n.ops):\n'
                   '        _bad.add("in")\n'
                   '    elif True and isinstance(_n, _ast.Slice):\n'
                   '        _bad.add("срезы")\n'
                   '    elif isinstance(_n, _ast.Import) and any(_a.name.split(".")[0] in {\'re\'} for _a '
                   'in _n.names):\n'
                   '        _bad.add("import")\n'
                   '    elif isinstance(_n, _ast.ImportFrom) and (_n.module or "").split(".")[0] in '
                   "{'re'}:\n"
                   '        _bad.add("import")\n'
                   'if _bad:\n'
                   '    print("запрещённые приёмы:", ", ".join(sorted(_bad)))\n'
                   'else:\n'
                   '    print(rabin_karp("hello world", "o w"), rabin_karp("abc", "abcd"), '
                   'rabin_karp("abc", ""), rabin_karp("abcabc", "cab"))\n'
                   '    big = "a" * 1000000\n'
                   '    print(rabin_karp(big, "a" * 300000 + "b"))\n'
                   '    print(rabin_karp(big + "b", "a" * 300000 + "b"))\n'
                   '    print(rabin_karp("ab" * 400000 + "c", "abababc"))\n',
         'expected': ['4 -1 0 2', '-1', '700000', '799994'],
         'hint': 'Окно: ht = ((ht − код ушедшего · B^(m−1)) · B + код нового) mod M; не забывайте брать '
                 'остаток после вычитания.'},
        {'id': 'str-trie',
         'mode': 'stdout',
         'title': 'Префиксное дерево',
         'statement': 'Напишите класс Trie с методами insert(word), contains(word) → bool и '
                      'count_prefix(prefix) → сколько различных вставленных слов начинается с prefix '
                      '(пустая приставка — все слова). Повторная вставка слова ничего не меняет. Проверка: '
                      'сто тысяч слов и сто тысяч запросов — перебор списка не уложится.',
         'starter': 'class Trie:\n'
                    '    def __init__(self):\n'
                    '        pass\n'
                    '\n'
                    '    def insert(self, word):\n'
                    '        pass\n'
                    '\n'
                    '    def contains(self, word):\n'
                    '        pass\n'
                    '\n'
                    '    def count_prefix(self, prefix):\n'
                    '        pass\n',
         'driver': 't = Trie()\n'
                   'for w in ["to", "tea", "ten", "in", "to"]:\n'
                   '    t.insert(w)\n'
                   'print(t.contains("te"), t.contains("ten"), t.count_prefix("te"), t.count_prefix(""), '
                   't.count_prefix("x"))\n'
                   'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'x = 777\n'
                   'def rnd():\n'
                   '    global x\n'
                   '    x = nxt(x)\n'
                   '    return x\n'
                   'words = []\n'
                   'big = Trie()\n'
                   'for _ in range(100000):\n'
                   '    w = "".join("abcdefgh"[rnd() % 8] for _ in range(1 + rnd() % 12))\n'
                   '    words.append(w)\n'
                   '    big.insert(w)\n'
                   'print(sum(big.contains(words[rnd() % 100000]) for _ in range(20000)))\n'
                   'total = 0\n'
                   'for _ in range(100000):\n'
                   '    w = words[rnd() % 100000]\n'
                   '    total += big.count_prefix(w[: 1 + rnd() % 6])\n'
                   'print(total, big.count_prefix(""))\n',
         'expected': ['False True 2 4 0', '20000', '229381066 69785'],
         'hint': 'В узле храните словарь детей, признак конца слова и сколько слов проходит через узел.'},
        {'id': 'str-autocomplete',
         'mode': 'func',
         'func': 'autocomplete',
         'title': 'Автодополнение',
         'statement': 'Напишите функцию autocomplete(words, prefix, k): первые k слов (без повторов) из '
                      'списка words, которые начинаются с prefix, в алфавитном порядке. Если таких слов '
                      'меньше k — вернуть сколько есть.',
         'starter': 'def autocomplete(words, prefix, k):\n    pass\n',
         'tests': [{'args': [['tea', 'ten', 'to', 'in', 'tea'], 'te', 5], 'expected': ['tea', 'ten']},
                   {'args': [['tea', 'ten', 'to', 'in'], 't', 2], 'expected': ['tea', 'ten']},
                   {'args': [['a', 'b'], 'c', 3], 'expected': []},
                   {'args': [['b', 'ab', 'a'], '', 2], 'expected': ['a', 'ab']},
                   {'args': [[], 'x', 1], 'expected': []}],
         'hint': 'Спуститесь в бор по приставке и обойдите поддерево, посещая детей по алфавиту, пока не '
                 'наберёте k слов.'},
        {'id': 'str-edit-distance',
         'mode': 'func',
         'func': 'edit_distance',
         'title': 'Расстояние Левенштейна',
         'statement': 'Напишите функцию edit_distance(a, b): минимальное число вставок, удалений и замен '
                      'символа, которое превращает a в b. Для «kitten» и «sitting» ответ 3. Время — '
                      'порядка len(a) · len(b).',
         'starter': 'def edit_distance(a, b):\n    pass\n',
         'tests': [{'args': ['kitten', 'sitting'], 'expected': 3},
                   {'args': ['', 'abc'], 'expected': 3},
                   {'args': ['abc', 'abc'], 'expected': 0},
                   {'args': ['flaw', 'lawn'], 'expected': 2},
                   {'args': ['intention', 'execution'], 'expected': 5},
                   {'args': ['abc', ''], 'expected': 3},
                   {'args': ['a', 'b'], 'expected': 1}],
         'hint': 'd[i][j] = d[i − 1][j − 1], если символы равны; иначе 1 + min из трёх соседей. Хватит '
                 'двух строк таблицы.'},
        {'id': 'str-one-edit',
         'mode': 'func',
         'func': 'one_edit_away',
         'title': 'Одна правка',
         'statement': 'Напишите функцию one_edit_away(a, b): True, если a можно превратить в b не более '
                      'чем одной вставкой, удалением или заменой символа (строки равны — тоже True). Время '
                      '— линейное, без таблицы.',
         'starter': 'def one_edit_away(a, b):\n    pass\n',
         'tests': [{'args': ['pale', 'ple'], 'expected': True},
                   {'args': ['pales', 'pale'], 'expected': True},
                   {'args': ['pale', 'bale'], 'expected': True},
                   {'args': ['pale', 'bake'], 'expected': False},
                   {'args': ['same', 'same'], 'expected': True},
                   {'args': ['', 'a'], 'expected': True},
                   {'args': ['', 'ab'], 'expected': False},
                   {'args': ['abc', 'ab'], 'expected': True}],
         'hint': 'Найдите первую позицию, где строки расходятся, и проверьте оставшиеся хвосты для трёх '
                 'случаев длины.'},
        {'id': 'str-lcs',
         'mode': 'func',
         'func': 'lcs_length',
         'title': 'Наибольшая общая подпоследовательность',
         'statement': 'Напишите функцию lcs_length(a, b): длина наибольшей общей подпоследовательности '
                      'двух строк — символы идут в том же порядке, но не обязательно подряд. Для «abcde» и '
                      '«ace» ответ 3.',
         'starter': 'def lcs_length(a, b):\n    pass\n',
         'tests': [{'args': ['abcde', 'ace'], 'expected': 3},
                   {'args': ['abc', 'def'], 'expected': 0},
                   {'args': ['', 'a'], 'expected': 0},
                   {'args': ['AGGTAB', 'GXTXAYB'], 'expected': 4},
                   {'args': ['aaaa', 'aa'], 'expected': 2},
                   {'args': ['abc', 'abc'], 'expected': 3}],
         'hint': 'Совпали последние символы — длина на единицу больше, чем у префиксов; иначе максимум из '
                 '«без последнего в a» и «без последнего в b».'},
        {'id': 'str-distinct-substrings',
         'mode': 'stdout',
         'title': 'Сколько различных подстрок',
         'statement': 'Напишите функцию count_distinct(s): число различных непустых подстрок строки s. Для '
                      '«aaa» ответ 3, для «abab» — 7. Хранить все подстроки нельзя: проверка подаёт строки '
                      'в две тысячи символов, а память песочницы ограничена. Идея: при дописывании символа '
                      'к префиксу длины i появляются новые подстроки — суффиксы, которых раньше не было. '
                      'Их число равно i минус наибольшее значение префикс-функции развёрнутого префикса.',
         'starter': 'def count_distinct(s):\n    pass\n',
         'driver': 'print(count_distinct("aaa"), count_distinct("abab"), count_distinct("abc"), '
                   'count_distinct(""))\n'
                   'print(count_distinct("a" * 2000), count_distinct("ab" * 1000))\n'
                   'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'x = 99\n'
                   's = []\n'
                   'for _ in range(1500):\n'
                   '    x = nxt(x)\n'
                   '    s.append("abc"[(x >> 10) % 3])\n'
                   'print(count_distinct("".join(s)))\n',
         'expected': ['3 7 6 0', '2000 3999', '1117153'],
         'hint': 'Новые подстроки при дописывании символа — это суффиксы, ещё не встречавшиеся раньше; их '
                 'длина — i минус максимум π развёрнутого префикса.'},
    ],
}
