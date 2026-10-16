"""Задачи книги «Алгоритмы и структуры данных»: глава 17."""

TASKS: dict[int, list[dict]] = {
    17: [
        {'id': 'dsu-basic',
         'mode': 'stdout',
         'title': 'Система непересекающихся множеств',
         'statement': 'Напишите класс DSU: DSU(n) — n элементов, каждый в своей группе; find(x) — '
                      'представитель группы; union(a, b) объединяет группы и возвращает True, если они '
                      'были разными, иначе False; connected(a, b) — в одной ли группе; size(x) — размер '
                      'группы x; count() — число групп. Используйте сжатие путей и объединение по размеру. '
                      'Проверка подаёт цепочку union(i, i + 1) из двухсот тысяч элементов и двести тысяч '
                      'запросов connected: без оптимизаций это квадрат.',
         'starter': 'class DSU:\n'
                    '    def __init__(self, n):\n'
                    '        pass\n'
                    '\n'
                    '    def find(self, x):\n'
                    '        pass\n'
                    '\n'
                    '    def union(self, a, b):\n'
                    '        pass\n'
                    '\n'
                    '    def connected(self, a, b):\n'
                    '        pass\n'
                    '\n'
                    '    def size(self, x):\n'
                    '        pass\n'
                    '\n'
                    '    def count(self):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'd = DSU(6)\n'
                   'print(d.union(0, 1), d.union(1, 2), d.union(0, 2), d.connected(0, 2), d.connected(0, '
                   '5), d.size(1), d.count())\n'
                   'n = 200000\n'
                   'd = DSU(n)\n'
                   'for i in range(n - 1):\n'
                   '    d.union(i, i + 1)\n'
                   'print(d.count(), d.size(0), d.connected(0, n - 1))\n'
                   'ok = 0\n'
                   'for _ in range(n):\n'
                   '    ok += d.connected(0, n - 1)\n'
                   'print(ok)\n'
                   'm = 1000000\n'
                   'd = DSU(m)\n'
                   'x = 12345\n'
                   'for _ in range(500000):\n'
                   '    x = nxt(x)\n'
                   '    a = x % m\n'
                   '    x = nxt(x)\n'
                   '    d.union(a, x % m)\n'
                   'print(d.count(), d.size(0) > 0)\n',
         'expected': ['True True False True False 3 4', '1 200000 True', '200000', '500001 True'],
         'hint': 'p[x] — родитель; find поднимается до корня и перевешивает пройденных на корень; union '
                 'подвешивает меньшее дерево под большее.'},
        {'id': 'dsu-components',
         'mode': 'func',
         'func': 'count_components',
         'title': 'Число компонент связности',
         'statement': 'Напишите функцию count_components(n, edges): число компонент связности '
                      'неориентированного графа из n вершин (0…n−1) и списка рёбер [a, b]. Каждое успешное '
                      'объединение уменьшает число групп на один.',
         'starter': 'def count_components(n, edges):\n    pass\n',
         'tests': [{'args': [5, [[0, 1], [1, 2], [3, 4]]], 'expected': 2},
                   {'args': [4, []], 'expected': 4},
                   {'args': [1, []], 'expected': 1},
                   {'args': [6, [[0, 1], [1, 0], [2, 3], [3, 4], [4, 2]]], 'expected': 3},
                   {'args': [3, [[0, 1], [1, 2], [0, 2]]], 'expected': 1},
                   {'args': [0, []], 'expected': 0}],
         'hint': 'Начните с n групп; на каждом ребре, которое объединило разные группы, вычитайте единицу.'},
        {'id': 'dsu-cycle',
         'mode': 'func',
         'func': 'has_cycle',
         'title': 'Есть ли цикл',
         'statement': 'Напишите функцию has_cycle(n, edges): True, если в неориентированном графе есть '
                      'цикл (параллельные рёбра между одной парой вершин — тоже цикл; петля [a, a] — '
                      'цикл).',
         'starter': 'def has_cycle(n, edges):\n    pass\n',
         'tests': [{'args': [4, [[0, 1], [1, 2], [2, 3]]], 'expected': False},
                   {'args': [3, [[0, 1], [1, 2], [2, 0]]], 'expected': True},
                   {'args': [2, [[0, 1], [1, 0]]], 'expected': True},
                   {'args': [3, [[1, 1]]], 'expected': True},
                   {'args': [5, []], 'expected': False},
                   {'args': [6, [[0, 1], [2, 3], [4, 5], [1, 2], [3, 4]]], 'expected': False}],
         'hint': 'Ребро, концы которого уже в одной группе, замыкает цикл.'},
        {'id': 'dsu-redundant',
         'mode': 'func',
         'func': 'redundant_edge',
         'title': 'Лишнее ребро',
         'statement': 'Напишите функцию redundant_edge(n, edges): первое по порядку ребро (в виде списка '
                      '[a, b]), которое замыкает цикл — на момент его добавления концы уже в одной группе. '
                      'Если циклов нет — пустой список.',
         'starter': 'def redundant_edge(n, edges):\n    pass\n',
         'tests': [{'args': [4, [[0, 1], [1, 2], [2, 3], [3, 1]]], 'expected': [3, 1]},
                   {'args': [3, [[0, 1], [1, 2]]], 'expected': []},
                   {'args': [3, [[0, 1], [1, 2], [2, 0], [0, 1]]], 'expected': [2, 0]},
                   {'args': [2, [[1, 0], [0, 1]]], 'expected': [0, 1]},
                   {'args': [0, []], 'expected': []}],
         'hint': 'Обрабатывайте рёбра по порядку и верните первое, для которого union вернул False.'},
        {'id': 'dsu-islands',
         'mode': 'stdout',
         'title': 'Количество островов',
         'statement': 'Напишите функцию count_islands(grid): grid — список строк из «1» (суша) и «0» '
                      '(вода) одинаковой длины; остров — группа клеток суши, соседних по стороне (по '
                      'горизонтали или вертикали). Верните число островов. Проверка подаёт карту, где один '
                      'остров вьётся змейкой на сотни тысяч клеток: рекурсивный обход упрётся в лимит '
                      'глубины — используйте систему непересекающихся множеств или обход со стеком.',
         'starter': 'def count_islands(grid):\n    pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'print(count_islands(["11000", "11000", "00100", "00011"]), count_islands([]), '
                   'count_islands(["0"]), count_islands(["1"]))\n'
                   'w, h = 700, 700\n'
                   'g = []\n'
                   'x = 7\n'
                   'for r in range(h):\n'
                   '    row = []\n'
                   '    for c in range(w):\n'
                   '        x = nxt(x)\n'
                   '        row.append("1" if x % 100 < 45 else "0")\n'
                   '    g.append("".join(row))\n'
                   'print(count_islands(g))\n'
                   'w, h = 501, 501\n'
                   'snake = []\n'
                   'for r in range(h):\n'
                   '    if r % 2 == 0:\n'
                   '        snake.append("1" * w)\n'
                   '    elif r % 4 == 1:\n'
                   '        snake.append("0" * (w - 1) + "1")\n'
                   '    else:\n'
                   '        snake.append("1" + "0" * (w - 1))\n'
                   'print(count_islands(snake))\n',
         'expected': ['3 0 0 1', '43116', '1'],
         'hint': 'Для каждой клетки суши объедините её с правым и нижним соседом; в конце посчитайте '
                 'различные корни.'},
        {'id': 'dsu-kruskal',
         'mode': 'func',
         'func': 'mst_weight',
         'title': 'Минимальный остов (Краскал)',
         'statement': 'Напишите функцию mst_weight(n, edges): вес минимального остовного дерева связного '
                      'неориентированного графа; edges — список троек [a, b, вес]. Если граф несвязный — '
                      'верните -1. Алгоритм Краскала: рёбра по возрастанию веса, берём те, что соединяют '
                      'разные группы.',
         'starter': 'def mst_weight(n, edges):\n    pass\n',
         'tests': [{'args': [4, [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10], [0, 2, 4]]], 'expected': 6},
                   {'args': [3, [[0, 1, 5]]], 'expected': -1},
                   {'args': [1, []], 'expected': 0},
                   {'args': [4, [[0, 1, 2], [1, 2, 3], [2, 3, 1], [3, 0, 4], [0, 2, 5], [1, 3, 6]]],
                    'expected': 6},
                   {'args': [2, [[0, 1, 7], [0, 1, 3]]], 'expected': 3}],
         'hint': 'Отсортируйте рёбра по весу; каждое, для которого union вернул True, добавьте к сумме; в '
                 'остове n − 1 ребро.'},
        {'id': 'dsu-equations',
         'mode': 'func',
         'func': 'equations_possible',
         'title': 'Равенства и неравенства',
         'statement': 'Напишите функцию equations_possible(eqs): eqs — список строк вида «a==b» или «a!=b» '
                      '(однобуквенные переменные). Верните True, если переменным можно подобрать значения, '
                      'при которых выполняются все условия.',
         'starter': 'def equations_possible(eqs):\n    pass\n',
         'tests': [{'args': [['a==b', 'b!=a']], 'expected': False},
                   {'args': [['a==b', 'b==c', 'a==c']], 'expected': True},
                   {'args': [['a==b', 'b!=c', 'c==a']], 'expected': False},
                   {'args': [['c==c', 'b==d', 'x!=z']], 'expected': True},
                   {'args': [['a!=a']], 'expected': False},
                   {'args': [[]], 'expected': True}],
         'hint': 'Сначала объедините все равенства, затем проверьте, что ни одно неравенство не попало в '
                 'одну группу.'},
        {'id': 'dsu-weighted',
         'mode': 'stdout',
         'title': 'Непересекающиеся множества с разностями',
         'statement': 'Напишите класс WeightedDSU: WeightedDSU(n) — n неизвестных; union(a, b, d) сообщает '
                      'условие x[a] − x[b] = d и возвращает False, если оно противоречит уже известным '
                      '(иначе True и запоминает); diff(a, b) возвращает x[a] − x[b], если эта разность '
                      'выводится из условий, иначе None. Храните в каждом элементе смещение относительно '
                      'родителя. Проверка — триста тысяч условий на двухстах тысячах неизвестных.',
         'starter': 'class WeightedDSU:\n'
                    '    def __init__(self, n):\n'
                    '        pass\n'
                    '\n'
                    '    def union(self, a, b, d):\n'
                    '        pass\n'
                    '\n'
                    '    def diff(self, a, b):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'w = WeightedDSU(5)\n'
                   'print(w.union(0, 1, 3), w.union(1, 2, 4), w.diff(0, 2), w.diff(2, 0), w.diff(0, 3), '
                   'w.union(0, 2, 7), w.union(0, 2, 8), w.union(3, 4, -1), w.union(4, 0, 2), w.diff(3, '
                   '1))\n'
                   'n = 200000\n'
                   'x = 5\n'
                   'val = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    val.append(x % 1000)\n'
                   'w = WeightedDSU(n)\n'
                   'ok = bad = 0\n'
                   'for q in range(300000):\n'
                   '    x = nxt(x)\n'
                   '    a = x % n\n'
                   '    x = nxt(x)\n'
                   '    b = x % n\n'
                   '    if q % 7 == 6:\n'
                   '        d = val[a] - val[b] + 1\n'
                   '    else:\n'
                   '        d = val[a] - val[b]\n'
                   '    if w.union(a, b, d):\n'
                   '        ok += 1\n'
                   '    else:\n'
                   '        bad += 1\n'
                   'print(ok, bad)\n'
                   'x = 99\n'
                   'total = 0\n'
                   'known = 0\n'
                   'for _ in range(100000):\n'
                   '    x = nxt(x)\n'
                   '    a = x % n\n'
                   '    x = nxt(x)\n'
                   '    r = w.diff(a, x % n)\n'
                   '    if r is not None:\n'
                   '        known += 1\n'
                   '        total += r\n'
                   'print(known, total)\n',
         'expected': ['True True 7 -7 None True False True True 4', '202506 97494', '88578 -41710'],
         'hint': 'Если корни совпали, сравните смещения; иначе подвесьте один корень под другой, подобрав '
                 'смещение из условия.'},
        {'id': 'dsu-offline',
         'mode': 'stdout',
         'title': 'Удаление рёбер: идём с конца',
         'statement': 'Напишите функцию components_after_removals(n, edges, order): из графа по очереди '
                      'удаляют рёбра с номерами order[0], order[1], … (номера в списке edges, без '
                      'повторов). Верните список res, где res[k] — число компонент связности после k + 1 '
                      'удалений. Система непересекающихся множеств не умеет разделять, поэтому '
                      'обрабатывайте удаления в обратном порядке как добавления. Проверка — двести тысяч '
                      'рёбер и сто тысяч удалений.',
         'starter': 'def components_after_removals(n, edges, order):\n    pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'print(components_after_removals(4, [[0, 1], [1, 2], [2, 3], [0, 3]], [0, 3, 1]), '
                   'components_after_removals(3, [], []))\n'
                   'n = 200000\n'
                   'x = 321\n'
                   'edges = []\n'
                   'for _ in range(200000):\n'
                   '    x = nxt(x)\n'
                   '    a = x % n\n'
                   '    x = nxt(x)\n'
                   '    edges.append([a, x % n])\n'
                   'idx = list(range(len(edges)))\n'
                   'for i in range(100000):\n'
                   '    x = nxt(x)\n'
                   '    j = i + x % (len(idx) - i)\n'
                   '    idx[i], idx[j] = idx[j], idx[i]\n'
                   'res = components_after_removals(n, edges, idx[:100000])\n'
                   'print(sum(res) % 1000003, res[0], res[-1])\n',
         'expected': ['[1, 2, 3] []', '100061 32334 100002'],
         'hint': 'Постройте систему из рёбер, которые не удаляют; затем идите по order с конца: запишите '
                 'число компонент и верните ребро в граф.'},
        {'id': 'dsu-accounts',
         'mode': 'func',
         'func': 'merge_accounts',
         'title': 'Слияние аккаунтов',
         'statement': 'Напишите функцию merge_accounts(accounts): accounts — список [имя, почта1, почта2, '
                      '…]. Два аккаунта — один человек, если у них есть общая почта (имена могут совпадать '
                      'у разных людей). Верните список объединённых аккаунтов в виде [имя, почты по '
                      'возрастанию…], отсортированный по самому списку.',
         'starter': 'def merge_accounts(accounts):\n    pass\n',
         'tests': [{'args': [[['Иван', 'a@x', 'b@x'],
                              ['Иван', 'c@x'],
                              ['Иван', 'b@x', 'd@x'],
                              ['Пётр', 'a@x']]],
                    'expected': [['Иван', 'a@x', 'b@x', 'd@x'], ['Иван', 'c@x']]},
                   {'args': [[['А', '1@m']]], 'expected': [['А', '1@m']]},
                   {'args': [[]], 'expected': []},
                   {'args': [[['А', 'x@y', 'z@y'], ['Б', 'z@y'], ['А', 'w@y']]],
                    'expected': [['А', 'w@y'], ['Б', 'x@y', 'z@y']]}],
         'hint': 'Для каждой почты запомните первый аккаунт с ней; встретили снова — объедините аккаунты. '
                 'Затем соберите почты по корням.'},
        {'id': 'bt-subsets',
         'mode': 'stdout',
         'title': 'Все подмножества',
         'statement': 'Напишите функцию subsets(nums): список всех подмножеств списка различных чисел '
                      '(каждое — список, элементы в порядке входа; порядок самих подмножеств не важен). '
                      'Используйте шаблон «выбрать, исследовать, отменить» и не забывайте копировать '
                      'текущий путь.',
         'starter': 'def subsets(nums):\n    pass\n',
         'driver': 'print(sorted(sorted(s) for s in subsets([1, 2, 3])), subsets([]))\n'
                   'big = subsets(list(range(16)))\n'
                   'print(len(big), len({tuple(s) for s in big}), sum(len(s) for s in big))\n',
         'expected': ['[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]] [[]]', '65536 65536 524288'],
         'hint': 'На каждом элементе два ветвления: не брать и взять; после возврата удалите взятый '
                 'элемент (pop).'},
        {'id': 'bt-subsets-dups',
         'mode': 'stdout',
         'title': 'Подмножества с повторами',
         'statement': 'Напишите функцию subsets_unique(nums): все различные подмножества списка, в котором '
                      'есть повторяющиеся числа (каждое подмножество — отсортированный список; порядок '
                      'подмножеств не важен). Одинаковые подмножества в ответе повторяться не должны. '
                      'Подсказка: отсортируйте вход и пропускайте число, равное предыдущему на этом '
                      'уровне.',
         'starter': 'def subsets_unique(nums):\n    pass\n',
         'driver': 'print(sorted(subsets_unique([2, 1, 2])), subsets_unique([]))\n'
                   'r = subsets_unique([1] * 8 + [2] * 8 + [3] * 4)\n'
                   'print(len(r), len({tuple(sorted(s)) for s in r}))\n',
         'expected': ['[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]] [[]]', '405 405'],
         'hint': 'Отсортируйте nums; в цикле по start: если i > start и nums[i] == nums[i − 1], '
                 'пропустите.'},
        {'id': 'bt-permutations',
         'mode': 'stdout',
         'title': 'Все перестановки',
         'statement': 'Напишите функцию permutations(nums): все перестановки списка различных чисел '
                      '(список списков; порядок не важен). Помечайте использованные элементы массивом used '
                      'и снимайте пометку при откате. Без itertools.',
         'starter': 'def permutations(nums):\n    pass\n',
         'driver': 'print(sorted(permutations([1, 2, 3])), permutations([]))\n'
                   'r = permutations(list(range(8)))\n'
                   'print(len(r), len({tuple(p) for p in r}), sum(p[0] for p in r))\n',
         'expected': ['[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]] [[]]',
                      '40320 40320 141120'],
         'hint': 'На каждом шаге цикл по индексам: если used[i], пропустите; иначе выберите, спуститесь, '
                 'отмените.'},
        {'id': 'bt-perm-dups',
         'mode': 'stdout',
         'title': 'Перестановки с повторами',
         'statement': 'Напишите функцию permutations_unique(nums): все различные перестановки списка с '
                      'повторяющимися числами (порядок не важен, одинаковые перестановки не повторяются). '
                      'Не генерируйте лишнее: проверка подаёт список из девяти чисел с повторами — 9! '
                      'перестановок слишком много, различных намного меньше.',
         'starter': 'def permutations_unique(nums):\n    pass\n',
         'driver': 'print(sorted(permutations_unique([1, 1, 2])), permutations_unique([]))\n'
                   'r = permutations_unique([1, 1, 2, 2, 3, 3, 4, 4, 5])\n'
                   'print(len(r), len({tuple(p) for p in r}))\n'
                   'r = permutations_unique([1] * 7 + [2] * 6)\n'
                   'print(len(r))\n',
         'expected': ['[[1, 1, 2], [1, 2, 1], [2, 1, 1]] [[]]', '22680 22680', '1716'],
         'hint': 'Отсортируйте и пропускайте элемент, равный предыдущему, если предыдущий ещё не '
                 'использован.'},
        {'id': 'bt-combinations',
         'mode': 'stdout',
         'title': 'Сочетания',
         'statement': 'Напишите функцию combine(n, k): все сочетания по k чисел из 1…n (каждое — '
                      'возрастающий список; порядок не важен). Отсекайте ветки, где оставшихся чисел не '
                      'хватит на нужное количество.',
         'starter': 'def combine(n, k):\n    pass\n',
         'driver': 'print(sorted(combine(4, 2)), combine(3, 0), combine(2, 3))\n'
                   'r = combine(22, 11)\n'
                   'print(len(r), r[0], sum(c[0] for c in r))\n',
         'expected': ['[[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]] [[]] []',
                      '705432 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] 1352078'],
         'hint': 'go(start): берите v от start; если чисел от v до n не хватает до k — выходите из цикла '
                 'досрочно.'},
        {'id': 'bt-combination-sum',
         'mode': 'stdout',
         'title': 'Сумма сочетаний с повторами',
         'statement': 'Напишите функцию combination_sum(candidates, target): все различные наборы чисел из '
                      'candidates (различные положительные), в сумме дающие target; одно число можно брать '
                      'сколько угодно раз. Каждый набор — неубывающий список; порядок наборов не важен. '
                      'Отсортируйте числа и прерывайте цикл, когда число больше остатка.',
         'starter': 'def combination_sum(candidates, target):\n    pass\n',
         'driver': 'print(sorted(combination_sum([2, 3, 6, 7], 7)), sorted(combination_sum([2, 3, 5], 8)), '
                   'combination_sum([5], 3), combination_sum([1], 0))\n'
                   'r = combination_sum([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], 120)\n'
                   'print(len(r), max(len(c) for c in r), len({tuple(c) for c in r}))\n',
         'expected': ['[[2, 2, 3], [7]] [[2, 2, 2, 2], [2, 3, 3], [3, 5]] [] [[]]', '84685 60 84685'],
         'hint': 'go(i, rest): для j от i: если nums[j] > rest — break; иначе берите число, вызывайте '
                 'go(j, rest − nums[j]).'},
        {'id': 'bt-n-queens',
         'mode': 'stdout',
         'title': 'Расстановка ферзей',
         'statement': 'Напишите функцию n_queens(n): сколько способов расставить n ферзей на доске n × n '
                      'так, чтобы они не били друг друга. Ставьте по ферзю в каждую строку и проверяйте '
                      'занятость столбцов и двух диагоналей за константу (множества или битовые маски). '
                      'Проверка доходит до n = 11.',
         'starter': 'def n_queens(n):\n    pass\n',
         'driver': 'print([n_queens(n) for n in range(1, 10)])\nprint(n_queens(10), n_queens(11))\n',
         'expected': ['[1, 0, 0, 2, 10, 4, 40, 92, 352]', '724 2680'],
         'hint': 'Диагонали: r − c и r + c постоянны на каждой; храните занятые в множествах и снимайте '
                 'при откате.'},
        {'id': 'bt-sudoku',
         'mode': 'stdout',
         'title': 'Судоку',
         'statement': 'Напишите функцию solve_sudoku(rows): rows — девять строк по девять символов, цифры '
                      '«1»–«9» и «.» для пустой клетки; решение единственное. Верните девять строк '
                      'решённой доски или None, если решить нельзя. Проверка включает головоломку, на '
                      'которой перебор клеток подряд работает минуты: выбирайте клетку с наименьшим числом '
                      'вариантов и храните занятые цифры в строках, столбцах и блоках масками.',
         'starter': 'def solve_sudoku(rows):\n    pass\n',
         'driver': 'def rows(s):\n'
                   '    return [s[i * 9:(i + 1) * 9] for i in range(9)]\n'
                   'for puzzle in '
                   "('53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79', "
                   "'..............3.85..1.2.......5.7.....4...1...9.......5......73..2.1........4...9'):\n"
                   '    ans = solve_sudoku(rows(puzzle))\n'
                   '    ok = all(sorted(r) == list("123456789") for r in ans) and all(sorted(ans[r][c] for '
                   'r in range(9)) == list("123456789") for c in range(9))\n'
                   '    ok = ok and all(sorted(ans[r][c] for r in range(br, br + 3) for c in range(bc, bc '
                   '+ 3)) == list("123456789") for br in (0, 3, 6) for bc in (0, 3, 6))\n'
                   '    ok = ok and all(p == "." or p == ans[i // 9][i % 9] for i, p in '
                   'enumerate(puzzle))\n'
                   '    print(ok, ans[0], ans[8])\n'
                   'print(solve_sudoku(rows("12345678." + "........9" + "." * 63)))\n',
         'expected': ['True 534678912 345286179', 'True 987654321 863745219', 'None'],
         'hint': 'Выбирайте клетку с минимумом кандидатов (ноль — тупик, откат); кандидаты — это ~(строка '
                 '| столбец | блок) & 0b1111111110.'},
        {'id': 'bt-word-search',
         'mode': 'func',
         'func': 'exist',
         'title': 'Слово на сетке',
         'statement': 'Напишите функцию exist(board, word): board — список строк-рядов; можно ли составить '
                      'слово word, идя по соседним по стороне клеткам, не используя одну клетку дважды? '
                      'Пустое слово — True. Отмечайте клетку посещённой перед спуском и снимайте отметку '
                      'при возврате.',
         'starter': 'def exist(board, word):\n    pass\n',
         'tests': [{'args': [['ABCE', 'SFCS', 'ADEE'], 'ABCCED'], 'expected': True},
                   {'args': [['ABCE', 'SFCS', 'ADEE'], 'SEE'], 'expected': True},
                   {'args': [['ABCE', 'SFCS', 'ADEE'], 'ABCB'], 'expected': False},
                   {'args': [['a'], 'a'], 'expected': True},
                   {'args': [['a'], 'b'], 'expected': False},
                   {'args': [['aa'], 'aaa'], 'expected': False},
                   {'args': [['ab', 'cd'], 'acdb'], 'expected': True},
                   {'args': [['ABCE', 'SFCS', 'ADEE'], ''], 'expected': True},
                   {'args': [['ABCD', 'EFGH'], 'AFGD'], 'expected': False}],
         'hint': 'go(r, c, i): клетка должна совпасть с word[i]; пометьте её, попробуйте четыре соседа, '
                 'снимите пометку.'},
        {'id': 'bt-meet-in-middle',
         'mode': 'stdout',
         'title': 'Встреча посередине',
         'statement': 'Напишите функцию count_subsets_sum(nums, target): сколько подмножеств (по позициям, '
                      'то есть одинаковые числа на разных местах — разные подмножества, пустое тоже '
                      'считается) списка nums имеют сумму target. В списке до 36 чисел: перебор 2³⁶ '
                      'подмножеств не уложится. Разделите список пополам, переберите суммы каждой половины '
                      '(2¹⁸ штук) и соедините их через словарь счётчиков.',
         'starter': 'def count_subsets_sum(nums, target):\n    pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'print(count_subsets_sum([1, 2, 3], 3), count_subsets_sum([], 0), count_subsets_sum([0, '
                   '0], 0), count_subsets_sum([5], 3))\n'
                   'x = 202\n'
                   'nums = []\n'
                   'for _ in range(36):\n'
                   '    x = nxt(x)\n'
                   '    nums.append(x % 1000)\n'
                   'print(count_subsets_sum(nums, sum(nums) // 2), count_subsets_sum(nums, 1234), '
                   'count_subsets_sum(nums, -1))\n'
                   'nums = [1] * 20 + [2] * 16\n'
                   'print(count_subsets_sum(nums, 18))\n',
         'expected': ['2 1 4 0', '13046942 16 0', '1330038610'],
         'hint': 'Суммы половины строят удвоением: sums += [s + v for s in sums]; затем для каждой суммы '
                 'левой половины ищите target − s в словаре правой.'},
    ],
}
