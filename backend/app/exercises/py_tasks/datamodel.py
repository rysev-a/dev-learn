"""Задачи «Python как первый язык»: модель данных (главы 18–21) — специальные методы, операторы, контейнеры и дескрипторы.

Ключ — номер главы. Все задачи в режиме stdout со скрытым driver: ученик пишет класс, а проверка его использует.
"""

TASKS: dict[int, list[dict]] = {
    18: [
        {
            "id": "dm-repr-point",
            "mode": "stdout",
            "title": "Точка с понятным repr",
            "statement": (
                'Допишите в класс Point метод __repr__, который возвращает строку вида Point(1, 2) — так, как точку записали бы в коде. Проверка печатает repr точки и список из точки.'
            ),
            "starter": (
                'class Point:\n'
                '    def __init__(self, x, y):\n'
                '        self.x = x\n'
                '        self.y = y\n'
            ),
            "driver": (
                'p = Point(1, 2)\n'
                'print(repr(p))\n'
                'print([Point(-3, 4)])\n'
            ),
            "expected": ['Point(1, 2)', '[Point(-3, 4)]'],
            "hint": 'return f"Point({self.x}, {self.y})". Список показывает элементы через repr.',
        },
        {
            "id": "dm-str-money",
            "mode": "stdout",
            "title": "Деньги: str и repr",
            "statement": (
                'Класс Money хранит сумму amount. Для пользователя __str__ должен давать «5.00 ₽» (две цифры после точки), а __repr__ — Money(5). Напишите оба метода.'
            ),
            "starter": (
                'class Money:\n'
                '    def __init__(self, amount):\n'
                '        self.amount = amount\n'
            ),
            "driver": (
                'm = Money(5)\n'
                'print(m)\n'
                'print(repr(m))\n'
                'print(f"{m}")\n'
                'print([m])\n'
            ),
            "expected": ['5.00 ₽', 'Money(5)', '5.00 ₽', '[Money(5)]'],
            "hint": '__str__: f"{self.amount:.2f} ₽"; __repr__: f"Money({self.amount})".',
        },
        {
            "id": "dm-bool-account",
            "mode": "stdout",
            "title": "Пустой счёт — ложь",
            "statement": (
                'Допишите Account так, чтобы счёт с положительным остатком считался истинным, а с нулевым или отрицательным — ложным (условие if account: должно работать).'
            ),
            "starter": (
                'class Account:\n'
                '    def __init__(self, balance):\n'
                '        self.balance = balance\n'
            ),
            "driver": (
                'print(bool(Account(10)))\n'
                'print(bool(Account(0)))\n'
                'print("есть" if Account(5) else "пусто")\n'
                'print(bool(Account(-1)))\n'
            ),
            "expected": ['True', 'False', 'есть', 'False'],
            "hint": "def __bool__(self): return self.balance > 0.",
        },
        {
            "id": "dm-len-basket",
            "mode": "stdout",
            "title": "Длина корзины",
            "statement": (
                'В Basket уже есть метод add. Добавьте __len__, чтобы len(basket) возвращало число товаров, а пустая корзина была ложью (без отдельного __bool__).'
            ),
            "starter": (
                'class Basket:\n'
                '    def __init__(self):\n'
                '        self.items = []\n'
                '\n'
                '    def add(self, item):\n'
                '        self.items.append(item)\n'
            ),
            "driver": (
                'b = Basket()\n'
                'print(len(b), bool(b))\n'
                'b.add("хлеб")\n'
                'b.add("сыр")\n'
                'print(len(b), bool(b))\n'
            ),
            "expected": ['0 False', '2 True'],
            "hint": "def __len__(self): return len(self.items). Истинность Питон возьмёт из длины.",
        },
        {
            "id": "dm-eq-hash-version",
            "mode": "stdout",
            "title": "Равенство и хеш версий",
            "statement": (
                'Напишите для Version(major, minor) методы __eq__ и __hash__: версии с одинаковыми числами равны, их можно класть в множество и использовать как ключи. Сравнение с объектом другого типа (например, со строкой) должно просто давать False, а не ошибку.'
            ),
            "starter": (
                'class Version:\n'
                '    def __init__(self, major, minor):\n'
                '        self.major = major\n'
                '        self.minor = minor\n'
            ),
            "driver": (
                'a = Version(1, 2)\n'
                'b = Version(1, 2)\n'
                'c = Version(2, 0)\n'
                'print(a == b, a == c, a != c)\n'
                'print(len({a, b, c}))\n'
                'd = {a: "x"}\n'
                'print(d[b])\n'
                'print(a == "1.2")\n'
            ),
            "expected": ['True False True', '2', 'x', 'False'],
            "hint": (
                'В __eq__: if not isinstance(other, Version): return NotImplemented. __hash__: hash((self.major, self.minor)).'
            ),
        },
        {
            "id": "dm-order-version",
            "mode": "stdout",
            "title": "Порядок версий",
            "statement": (
                'Класс Version уже умеет проверять равенство и использует @total_ordering. Допишите __lt__ так, чтобы версии сравнивались по (major, minor), а сравнение с чужим типом возвращало NotImplemented (тогда Питон сам поднимет TypeError).'
            ),
            "starter": (
                'from functools import total_ordering\n'
                '\n'
                '\n'
                '@total_ordering\n'
                'class Version:\n'
                '    def __init__(self, major, minor):\n'
                '        self.major = major\n'
                '        self.minor = minor\n'
                '\n'
                '    def __eq__(self, other):\n'
                '        if not isinstance(other, Version):\n'
                '            return NotImplemented\n'
                '        return (self.major, self.minor) == (other.major, other.minor)\n'
                '\n'
                '    # допишите __lt__\n'
            ),
            "driver": (
                'vs = [Version(1, 10), Version(1, 2), Version(0, 9)]\n'
                'print([(v.major, v.minor) for v in sorted(vs)])\n'
                'print(Version(1, 2) < Version(1, 10), Version(1, 2) >= Version(1, 10), max(vs).minor)\n'
                'try:\n'
                '    Version(1, 0) < 5\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
            ),
            "expected": ['[(0, 9), (1, 2), (1, 10)]', 'True False 10', 'TypeError'],
            "hint": (
                'if not isinstance(other, Version): return NotImplemented; затем сравните кортежи (major, minor).'
            ),
        },
        {
            "id": "dm-format-temp",
            "mode": "stdout",
            "title": "Свой формат температуры",
            "statement": (
                'Напишите Temperature.__format__(spec): спецификация «c» (и пустая) даёт «21.0 °C», спецификация «f» — градусы Фаренгейта с одним знаком («69.8 °F»). Любую другую спецификацию отвергайте ValueError.'
            ),
            "starter": (
                'class Temperature:\n'
                '    def __init__(self, celsius):\n'
                '        self.celsius = celsius\n'
            ),
            "driver": (
                't = Temperature(21)\n'
                'print(f"{t:c}")\n'
                'print(f"{t:f}")\n'
                'print(f"{t}")\n'
                'try:\n'
                '    print(f"{t:x}")\n'
                'except ValueError:\n'
                '    print("ValueError")\n'
            ),
            "expected": ['21.0 °C', '69.8 °F', '21.0 °C', 'ValueError'],
            "hint": 'F = C * 9 / 5 + 32. Форматируйте числа как f"{value:.1f}".',
        },
        {
            "id": "dm-getattr-config",
            "mode": "stdout",
            "title": "Настройки как атрибуты",
            "statement": (
                'Config хранит словарь в self._data. Допишите __getattr__ так, чтобы config.host возвращало значение ключа «host». Если ключа нет, поднимайте AttributeError (тогда hasattr и getattr с запасным значением работают правильно).'
            ),
            "starter": (
                'class Config:\n'
                '    def __init__(self, data):\n'
                '        self._data = dict(data)\n'
            ),
            "driver": (
                'c = Config({"host": "localhost", "port": 8080})\n'
                'print(c.host, c.port)\n'
                'print(hasattr(c, "user"))\n'
                'print(getattr(c, "user", "нет"))\n'
            ),
            "expected": ['localhost 8080', 'False', 'нет'],
            "hint": "try: return self._data[name]; except KeyError: raise AttributeError(name).",
        },
        {
            "id": "dm-readonly-id",
            "mode": "stdout",
            "title": "Неизменяемый номер заказа",
            "statement": (
                'У Order поле id нельзя менять после создания, а total — можно. Напишите __setattr__: первую запись id пропускайте, повторную — отвергайте AttributeError. Остальные атрибуты пишутся как обычно (через super().__setattr__, чтобы не уйти в рекурсию).'
            ),
            "starter": (
                'class Order:\n'
                '    def __init__(self, id, total):\n'
                '        self.id = id\n'
                '        self.total = total\n'
            ),
            "driver": (
                'o = Order(7, 100)\n'
                'o.total = 150\n'
                'print(o.id, o.total)\n'
                'try:\n'
                '    o.id = 8\n'
                'except AttributeError:\n'
                '    print("запрещено")\n'
                'print(o.id)\n'
            ),
            "expected": ['7 150', 'запрещено', '7'],
            "hint": (
                'if name == "id" and "id" in self.__dict__: raise AttributeError(...); затем super().__setattr__(name, value).'
            ),
        },
    ],
    19: [
        {
            "id": "ops-vector-add",
            "mode": "stdout",
            "title": "Сложение и вычитание векторов",
            "statement": (
                'Допишите в Vector методы __add__ и __sub__: оба возвращают новый вектор, а исходные не меняют.'
            ),
            "starter": (
                'class Vector:\n'
                '    def __init__(self, x, y):\n'
                '        self.x = x\n'
                '        self.y = y\n'
                '\n'
                '    def __repr__(self):\n'
                '        return f"Vector({self.x}, {self.y})"\n'
            ),
            "driver": (
                'a = Vector(1, 2)\n'
                'b = Vector(3, 4)\n'
                'print(a + b)\n'
                'print(b - a)\n'
                'print(a)\n'
            ),
            "expected": ['Vector(4, 6)', 'Vector(2, 2)', 'Vector(1, 2)'],
            "hint": "return Vector(self.x + other.x, self.y + other.y) — и так же для вычитания.",
        },
        {
            "id": "ops-vector-scalar",
            "mode": "stdout",
            "title": "Умножение на число с обеих сторон",
            "statement": (
                'Научите Vector умножаться на число и слева, и справа: v * 3 и 3 * v дают один результат. Если второй операнд не число (int или float), метод должен вернуть NotImplemented, чтобы Питон поднял TypeError.'
            ),
            "starter": (
                'class Vector:\n'
                '    def __init__(self, x, y):\n'
                '        self.x = x\n'
                '        self.y = y\n'
                '\n'
                '    def __repr__(self):\n'
                '        return f"Vector({self.x}, {self.y})"\n'
            ),
            "driver": (
                'v = Vector(1, 2)\n'
                'print(v * 3, 3 * v)\n'
                'print(v * 0.5)\n'
                'try:\n'
                '    v * "a"\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
            ),
            "expected": ['Vector(3, 6) Vector(3, 6)', 'Vector(0.5, 1.0)', 'TypeError'],
            "hint": (
                '__mul__: if not isinstance(k, (int, float)): return NotImplemented. А __rmul__ может просто вернуть self * k.'
            ),
        },
        {
            "id": "ops-money-sum",
            "mode": "stdout",
            "title": "Деньги под sum()",
            "statement": (
                'Money хранит копейки cents. Напишите __add__ (складывает только Money, иначе NotImplemented) и __radd__ так, чтобы sum([Money(150), Money(250)]) работала (sum начинает с нуля).'
            ),
            "starter": (
                'class Money:\n'
                '    def __init__(self, cents):\n'
                '        self.cents = cents\n'
                '\n'
                '    def __repr__(self):\n'
                '        return f"Money({self.cents})"\n'
            ),
            "driver": (
                'print(sum([Money(150), Money(250), Money(100)]))\n'
                'print(Money(1) + Money(2))\n'
                'try:\n'
                '    Money(1) + 5\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
            ),
            "expected": ['Money(500)', 'Money(3)', 'TypeError'],
            "hint": "__radd__(self, other): if other == 0: return self; иначе NotImplemented.",
        },
        {
            "id": "ops-bag-iadd",
            "mode": "stdout",
            "title": "Оператор += на месте",
            "statement": (
                'У Bag уже есть __add__ (возвращает новый мешок). Допишите __iadd__ так, чтобы a += other изменял сам объект a (дописывал элементы other) и возвращал его же.'
            ),
            "starter": (
                'class Bag:\n'
                '    def __init__(self, items):\n'
                '        self.items = list(items)\n'
                '\n'
                '    def __add__(self, other):\n'
                '        return Bag(self.items + other.items)\n'
            ),
            "driver": (
                'a = Bag([1])\n'
                'alias = a\n'
                'a += Bag([2, 3])\n'
                'print(alias is a, a.items)\n'
                'b = a + Bag([9])\n'
                'print(a.items, b.items)\n'
            ),
            "expected": ['True [1, 2, 3]', '[1, 2, 3] [1, 2, 3, 9]'],
            "hint": "self.items.extend(other.items); return self.",
        },
        {
            "id": "ops-vector-unary",
            "mode": "stdout",
            "title": "Отрицание и длина вектора",
            "statement": (
                'Допишите Vector: -v возвращает вектор с противоположными координатами, а abs(v) — длину вектора (math.hypot).'
            ),
            "starter": (
                'import math\n'
                '\n'
                '\n'
                'class Vector:\n'
                '    def __init__(self, x, y):\n'
                '        self.x = x\n'
                '        self.y = y\n'
                '\n'
                '    def __repr__(self):\n'
                '        return f"Vector({self.x}, {self.y})"\n'
            ),
            "driver": (
                'v = Vector(3, 4)\n'
                'print(-v)\n'
                'print(abs(v))\n'
                'print(abs(Vector(0, 0)) == 0)\n'
            ),
            "expected": ['Vector(-3, -4)', '5.0', 'True'],
            "hint": "__neg__: Vector(-self.x, -self.y); __abs__: math.hypot(self.x, self.y).",
        },
        {
            "id": "ops-index-step",
            "mode": "stdout",
            "title": "Объект как индекс",
            "statement": (
                'Сделайте Step пригодным везде, где нужно целое по природе: индекс списка, срез, hex(), range(). Для этого достаточно одного метода.'
            ),
            "starter": (
                'class Step:\n'
                '    def __init__(self, n):\n'
                '        self.n = n\n'
            ),
            "driver": (
                'items = ["a", "b", "c", "d"]\n'
                'print(items[Step(2)])\n'
                'print(hex(Step(255)))\n'
                'print(list(range(Step(3))))\n'
                'print(items[Step(1):Step(3)])\n'
            ),
            "expected": ['c', '0xff', '[0, 1, 2]', "['b', 'c']"],
            "hint": "def __index__(self): return self.n.",
        },
        {
            "id": "ops-matmul",
            "mode": "stdout",
            "title": "Умножение матриц знаком @",
            "statement": (
                'Допишите __matmul__ для Matrix (хранит список строк rows): строка i результата — сумма произведений строки i левой матрицы на столбец j правой. Результат — новая Matrix.'
            ),
            "starter": (
                'class Matrix:\n'
                '    def __init__(self, rows):\n'
                '        self.rows = [list(r) for r in rows]\n'
                '\n'
                '    def __eq__(self, other):\n'
                '        return self.rows == other.rows\n'
                '\n'
                '    def __repr__(self):\n'
                '        return f"Matrix({self.rows})"\n'
            ),
            "driver": (
                'a = Matrix([[1, 2], [3, 4]])\n'
                'b = Matrix([[0, 1], [1, 0]])\n'
                'print(a @ b)\n'
                'print(a @ Matrix([[1, 0], [0, 1]]) == a)\n'
            ),
            "expected": ['Matrix([[2, 1], [4, 3]])', 'True'],
            "hint": (
                'Для каждой строки r и каждого индекса j: sum(r[k] * other.rows[k][j] for k in range(len(r))).'
            ),
        },
        {
            "id": "ops-url-div",
            "mode": "stdout",
            "title": "Адрес через косую черту",
            "statement": (
                'Научите Url собираться оператором /: Url("example.com") / "api" / "v1/" даёт «example.com/api/v1» (лишние косые на стыках убираются). Если справа не строка, возвращайте NotImplemented.'
            ),
            "starter": (
                'class Url:\n'
                '    def __init__(self, base):\n'
                '        self.base = base\n'
                '\n'
                '    def __str__(self):\n'
                '        return self.base\n'
            ),
            "driver": (
                'u = Url("example.com") / "api" / "v1/"\n'
                'print(u)\n'
                'print(Url("a/") / "/b")\n'
                'try:\n'
                '    Url("a") / 5\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
            ),
            "expected": ['example.com/api/v1', 'a/b', 'TypeError'],
            "hint": 'Url(self.base.rstrip("/") + "/" + part.strip("/")).',
        },
        {
            "id": "ops-perm-flags",
            "mode": "stdout",
            "title": "Флаги прав",
            "statement": (
                'Perm хранит набор прав в трёх младших битах (4 — чтение, 2 — запись, 1 — запуск). Напишите __or__ (объединение), __and__ (пересечение) и __invert__ (дополнение до семи); каждый возвращает новый Perm.'
            ),
            "starter": (
                'class Perm:\n'
                '    def __init__(self, bits):\n'
                '        self.bits = bits\n'
                '\n'
                '    def __eq__(self, other):\n'
                '        return self.bits == other.bits\n'
                '\n'
                '    def __repr__(self):\n'
                '        return f"Perm({self.bits})"\n'
            ),
            "driver": (
                'R, W, X = Perm(4), Perm(2), Perm(1)\n'
                'rw = R | W\n'
                'print(rw)\n'
                'print((rw & W) == W)\n'
                'print(~rw)\n'
                'print(rw & X)\n'
            ),
            "expected": ['Perm(6)', 'True', 'Perm(1)', 'Perm(0)'],
            "hint": "Perm(self.bits | other.bits), Perm(self.bits & other.bits), Perm(7 ^ self.bits).",
        },
    ],
    20: [
        {
            "id": "ct-playlist",
            "mode": "stdout",
            "title": "Плейлист как последовательность",
            "statement": (
                'Playlist хранит треки во внутреннем списке _tracks. Допишите __len__ и __getitem__ так, чтобы работали len, индексы (в том числе отрицательные), цикл for, проверка in и reversed — без собственных __iter__ и __contains__.'
            ),
            "starter": (
                'class Playlist:\n'
                '    def __init__(self, tracks):\n'
                '        self._tracks = list(tracks)\n'
            ),
            "driver": (
                'p = Playlist(["a", "b", "c"])\n'
                'print(len(p), p[0], p[-1])\n'
                'print([t.upper() for t in p])\n'
                'print("b" in p, "z" in p)\n'
                'print(list(reversed(p)))\n'
            ),
            "expected": ['3 a c', "['A', 'B', 'C']", 'True False', "['c', 'b', 'a']"],
            "hint": "__len__ возвращает len(self._tracks); __getitem__ — self._tracks[index].",
        },
        {
            "id": "ct-slice-type",
            "mode": "stdout",
            "title": "Срез возвращает Deck",
            "statement": (
                'У Deck уже есть __len__. Напишите __getitem__: при целом индексе он возвращает карту, а при срезе — новый Deck (а не список).'
            ),
            "starter": (
                'class Deck:\n'
                '    def __init__(self, cards):\n'
                '        self._cards = list(cards)\n'
                '\n'
                '    def __len__(self):\n'
                '        return len(self._cards)\n'
                '\n'
                '    def __repr__(self):\n'
                '        return f"Deck({self._cards})"\n'
            ),
            "driver": (
                'd = Deck(["7", "8", "9", "10"])\n'
                'print(d[1])\n'
                'print(d[1:3])\n'
                'print(type(d[::2]).__name__, d[::-1])\n'
            ),
            "expected": ['8', "Deck(['8', '9'])", "Deck Deck(['10', '9', '8', '7'])"],
            "hint": "if isinstance(key, slice): return Deck(self._cards[key]); иначе return self._cards[key].",
        },
        {
            "id": "ct-registry",
            "mode": "stdout",
            "title": "Реестр со строгими ключами",
            "statement": (
                'Допишите Registry: ключи — только строки (иначе TypeError при записи), чтение по несуществующему ключу даёт KeyError, удаление через del и проверка in тоже должны работать.'
            ),
            "starter": (
                'class Registry:\n'
                '    def __init__(self):\n'
                '        self._d = {}\n'
            ),
            "driver": (
                'r = Registry()\n'
                'r["a"] = 1\n'
                'print(r["a"], "a" in r, "b" in r)\n'
                'try:\n'
                '    r[5] = 2\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
                'del r["a"]\n'
                'print("a" in r)\n'
                'try:\n'
                '    r["a"]\n'
                'except KeyError:\n'
                '    print("KeyError")\n'
            ),
            "expected": ['1 True False', 'TypeError', 'False', 'KeyError'],
            "hint": (
                '__setitem__ проверяет isinstance(key, str); __getitem__, __delitem__ и __contains__ работают с self._d.'
            ),
        },
        {
            "id": "ct-grid",
            "mode": "stdout",
            "title": "Поле с координатами",
            "statement": (
                'Grid(w, h) хранит клетки в self._cells (список строк, изначально «.»). Напишите __getitem__ и __setitem__ по кортежу (x, y), а также __contains__ для проверки координат. Выход за поле — IndexError.'
            ),
            "starter": (
                'class Grid:\n'
                '    def __init__(self, w, h):\n'
                '        self.w, self.h = w, h\n'
                '        self._cells = [["."] * w for _ in range(h)]\n'
            ),
            "driver": (
                'g = Grid(3, 2)\n'
                'g[1, 0] = "#"\n'
                'print(g[1, 0], g[0, 0])\n'
                'print((2, 1) in g, (3, 0) in g, (0, -1) in g)\n'
                'try:\n'
                '    g[3, 0]\n'
                'except IndexError:\n'
                '    print("IndexError")\n'
                'print(["".join(r) for r in g._cells])\n'
            ),
            "expected": ['# .', 'True False False', 'IndexError', "['.#.', '...']"],
            "hint": "x, y = pos; if not (0 <= x < self.w and 0 <= y < self.h): raise IndexError(pos).",
        },
        {
            "id": "ct-missing",
            "mode": "stdout",
            "title": "Словарь с __missing__",
            "statement": (
                'Допишите наследника dict Squares: если ключа n нет, __missing__ вычисляет n * n, сохраняет в словаре и возвращает.'
            ),
            "starter": (
                'class Squares(dict):\n'
                '    pass\n'
            ),
            "driver": (
                's = Squares()\n'
                'print(s[4], s[5])\n'
                'print(sorted(s.items()))\n'
                'print(4 in s, 6 in s)\n'
            ),
            "expected": ['16 25', '[(4, 16), (5, 25)]', 'True False'],
            "hint": "def __missing__(self, key): self[key] = key * key; return self[key].",
        },
        {
            "id": "ct-mapping-abc",
            "mode": "stdout",
            "title": "Отображение без учёта регистра",
            "statement": (
                'Класс CaseInsensitive наследует Mapping и хранит данные в self._d с ключами в нижнем регистре. Реализуйте __getitem__, __iter__ и __len__: обращение m["A"] и m["a"] даёт одно и то же, а keys, items, get, in и == работают бесплатно.'
            ),
            "starter": (
                'from collections.abc import Mapping\n'
                '\n'
                '\n'
                'class CaseInsensitive(Mapping):\n'
                '    def __init__(self, data):\n'
                '        self._d = {k.lower(): v for k, v in data.items()}\n'
            ),
            "driver": (
                'm = CaseInsensitive({"Host": "x", "PORT": 80})\n'
                'print(m["HOST"], m.get("port"), len(m))\n'
                'print(sorted(m.items()))\n'
                'print("host" in m, m == {"host": "x", "port": 80})\n'
            ),
            "expected": ['x 80 2', "[('host', 'x'), ('port', 80)]", 'True True'],
            "hint": (
                '__getitem__: self._d[key.lower()]; __iter__: iter(self._d); __len__: len(self._d). Тогда get и in работают через __getitem__.'
            ),
        },
        {
            "id": "ct-call-counter",
            "mode": "stdout",
            "title": "Счётчик-функция",
            "statement": (
                'Допишите Counter(start=0, step=1): каждый вызов counter() увеличивает значение на step и возвращает новое. Счётчик должен быть вызываемым и помнить состояние между вызовами.'
            ),
            "starter": (
                'class Counter:\n'
                '    def __init__(self, start=0, step=1):\n'
                '        self.value = start\n'
                '        self.step = step\n'
            ),
            "driver": (
                'c = Counter()\n'
                'print(c(), c(), c())\n'
                'd = Counter(10, 5)\n'
                'print(d(), d())\n'
                'print(callable(c), c.value)\n'
            ),
            "expected": ['1 2 3', '15 20', 'True 3'],
            "hint": "def __call__(self): self.value += self.step; return self.value.",
        },
        {
            "id": "ct-suppress",
            "mode": "stdout",
            "title": "Свой suppress",
            "statement": (
                'Напишите менеджер контекста Suppress(*types): внутри with он подавляет исключения перечисленных типов (и их потомков), а остальные пропускает дальше.'
            ),
            "starter": (
                'class Suppress:\n'
                '    def __init__(self, *types):\n'
                '        self.types = types\n'
            ),
            "driver": (
                'with Suppress(KeyError):\n'
                '    {}["x"]\n'
                '    print("не дойдём")\n'
                'print("после первого")\n'
                'with Suppress(KeyError, ValueError):\n'
                '    int("не число")\n'
                'print("после второго")\n'
                'try:\n'
                '    with Suppress(KeyError):\n'
                '        1 / 0\n'
                'except ZeroDivisionError:\n'
                '    print("ZeroDivisionError прошёл")\n'
            ),
            "expected": ['после первого', 'после второго', 'ZeroDivisionError прошёл'],
            "hint": (
                '__enter__ возвращает self; __exit__(self, exc_type, exc, tb): return exc_type is not None and issubclass(exc_type, self.types).'
            ),
        },
        {
            "id": "ct-tag-manager",
            "mode": "stdout",
            "title": "Парные теги через contextmanager",
            "statement": (
                'Напишите менеджер tag(name) на @contextmanager: при входе печатает <name>, при выходе </name> — в том числе когда внутри блока случилась ошибка.'
            ),
            "starter": "from contextlib import contextmanager\n\n\n",
            "driver": (
                'with tag("b"):\n'
                '    print("текст")\n'
                'try:\n'
                '    with tag("i"):\n'
                '        raise ValueError\n'
                'except ValueError:\n'
                '    print("ошибка")\n'
            ),
            "expected": ['<b>', 'текст', '</b>', '<i>', '</i>', 'ошибка'],
            "hint": "print вход; try: yield; finally: print выход.",
        },
    ],
    21: [
        {
            "id": "ds-fahrenheit",
            "mode": "stdout",
            "title": "Температура: свойство fahrenheit",
            "statement": (
                'Добавьте в Temperature свойство fahrenheit: чтение даёт градусы Фаренгейта по формуле C * 9 / 5 + 32, а запись пересчитывает и сохраняет значение в celsius.'
            ),
            "starter": (
                'class Temperature:\n'
                '    def __init__(self, celsius):\n'
                '        self.celsius = celsius\n'
            ),
            "driver": (
                't = Temperature(100)\n'
                'print(t.fahrenheit)\n'
                't.fahrenheit = 32\n'
                'print(t.celsius)\n'
            ),
            "expected": ['212.0', '0.0'],
            "hint": (
                '@property def fahrenheit(self); @fahrenheit.setter def fahrenheit(self, value): self.celsius = (value - 32) * 5 / 9.'
            ),
        },
        {
            "id": "ds-age-validated",
            "mode": "stdout",
            "title": "Возраст с проверкой",
            "statement": (
                'Превратите age в свойство: значение должно быть целым и неотрицательным, иначе ValueError. Проверка обязана работать и при создании объекта (в __init__ пишите через self.age), и при последующей записи.'
            ),
            "starter": (
                'class Person:\n'
                '    def __init__(self, name, age):\n'
                '        self.name = name\n'
                '        self.age = age\n'
            ),
            "driver": (
                'p = Person("Ann", 30)\n'
                'print(p.age)\n'
                'try:\n'
                '    p.age = -1\n'
                'except ValueError:\n'
                '    print("ValueError")\n'
                'try:\n'
                '    Person("Bob", -5)\n'
                'except ValueError:\n'
                '    print("ValueError при создании")\n'
                'p.age = 31\n'
                'print(p.age)\n'
            ),
            "expected": ['30', 'ValueError', 'ValueError при создании', '31'],
            "hint": (
                'Храните число в self._age; сеттер: if not isinstance(value, int) or value < 0: raise ValueError.'
            ),
        },
        {
            "id": "ds-readonly-area",
            "mode": "stdout",
            "title": "Только для чтения",
            "statement": (
                'Добавьте в Rect вычисляемые свойства area (площадь) и perimeter (периметр) без сеттеров: они всегда пересчитываются по w и h, а попытка присвоить area поднимает AttributeError.'
            ),
            "starter": (
                'class Rect:\n'
                '    def __init__(self, w, h):\n'
                '        self.w = w\n'
                '        self.h = h\n'
            ),
            "driver": (
                'r = Rect(3, 4)\n'
                'print(r.area, r.perimeter)\n'
                'r.w = 5\n'
                'print(r.area, r.perimeter)\n'
                'try:\n'
                '    r.area = 1\n'
                'except AttributeError:\n'
                '    print("AttributeError")\n'
            ),
            "expected": ['12 14', '20 18', 'AttributeError'],
            "hint": "@property def area(self): return self.w * self.h.",
        },
        {
            "id": "ds-positive",
            "mode": "stdout",
            "title": "Дескриптор Positive",
            "statement": (
                'Напишите дескриптор данных Positive: значение должно быть положительным числом, иначе ValueError. Храните его в экземпляре под именем поля (подскажет __set_name__), чтобы у разных объектов значения не смешивались; при обращении через класс возвращайте сам дескриптор.'
            ),
            "starter": (
                'class Positive:\n'
                '    pass\n'
            ),
            "driver": (
                'class Item:\n'
                '    price = Positive()\n'
                '    qty = Positive()\n'
                '\n'
                '    def __init__(self, price, qty):\n'
                '        self.price = price\n'
                '        self.qty = qty\n'
                '\n'
                '\n'
                'i = Item(5, 2)\n'
                'j = Item(7, 3)\n'
                'print(i.price, i.qty, j.price)\n'
                'try:\n'
                '    Item(-1, 1)\n'
                'except ValueError:\n'
                '    print("ValueError")\n'
                'try:\n'
                '    i.qty = 0\n'
                'except ValueError:\n'
                '    print("ValueError qty")\n'
                'print(type(Item.price).__name__)\n'
            ),
            "expected": ['5 2 7', 'ValueError', 'ValueError qty', 'Positive'],
            "hint": (
                '__set_name__(self, owner, name): self.name = name; __set__: obj.__dict__[self.name] = value; __get__: если obj is None — return self.'
            ),
        },
        {
            "id": "ds-typed",
            "mode": "stdout",
            "title": "Дескриптор Typed",
            "statement": (
                'Напишите дескриптор данных Typed(expected_type): при записи проверяет isinstance и поднимает TypeError, если тип не тот. Значения хранятся в экземплярах (в obj.__dict__ под именем поля).'
            ),
            "starter": (
                'class Typed:\n'
                '    def __init__(self, expected_type):\n'
                '        self.expected_type = expected_type\n'
            ),
            "driver": (
                'class Person:\n'
                '    name = Typed(str)\n'
                '    age = Typed(int)\n'
                '\n'
                '    def __init__(self, name, age):\n'
                '        self.name = name\n'
                '        self.age = age\n'
                '\n'
                '\n'
                'p = Person("Ann", 30)\n'
                'print(p.name, p.age)\n'
                'try:\n'
                '    Person("Bob", "x")\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
                'try:\n'
                '    p.age = 3.5\n'
                'except TypeError:\n'
                '    print("TypeError float")\n'
                'q = Person("Eve", 20)\n'
                'print(p.name, q.name)\n'
            ),
            "expected": ['Ann 30', 'TypeError', 'TypeError float', 'Ann Eve'],
            "hint": (
                'В __set__: if not isinstance(value, self.expected_type): raise TypeError(...). __get__: return obj.__dict__[self.name].'
            ),
        },
        {
            "id": "ds-lazy",
            "mode": "stdout",
            "title": "Ленивый атрибут",
            "statement": (
                'Напишите дескриптор без данных lazy (применяется как декоратор): при первом обращении вызывает функцию, кладёт результат в obj.__dict__ под тем же именем и возвращает его — дальше функция не запускается. Если обратиться через класс, возвращайте сам дескриптор.'
            ),
            "starter": (
                'class lazy:\n'
                '    def __init__(self, func):\n'
                '        self.func = func\n'
            ),
            "driver": (
                'class Data:\n'
                '    calls = 0\n'
                '\n'
                '    def __init__(self, items):\n'
                '        self.items = items\n'
                '\n'
                '    @lazy\n'
                '    def total(self):\n'
                '        Data.calls += 1\n'
                '        return sum(self.items)\n'
                '\n'
                '\n'
                'd = Data([1, 2, 3])\n'
                'print(d.total, d.total, Data.calls)\n'
                'print("total" in d.__dict__)\n'
                'del d.total\n'
                'print(d.total, Data.calls)\n'
                'print(type(Data.total).__name__)\n'
            ),
            "expected": ['6 6 1', 'True', '6 2', 'lazy'],
            "hint": (
                '__set_name__ запомнит имя; в __get__: value = self.func(obj); obj.__dict__[self.name] = value; return value. Метода __set__ быть не должно.'
            ),
        },
        {
            "id": "ds-classmethod",
            "mode": "stdout",
            "title": "Свой classmethod",
            "statement": (
                'Напишите дескриптор MyClassMethod — упрощённый classmethod. В __get__ он возвращает связанный метод, в который первым аргументом подставлен класс (тот, через который обратились, даже если вызвали через наследника или экземпляр).'
            ),
            "starter": (
                'import types\n'
                '\n'
                '\n'
                'class MyClassMethod:\n'
                '    def __init__(self, func):\n'
                '        self.func = func\n'
            ),
            "driver": (
                'class A:\n'
                '    @MyClassMethod\n'
                '    def make(cls):\n'
                '        return cls()\n'
                '\n'
                '\n'
                'class B(A):\n'
                '    pass\n'
                '\n'
                '\n'
                'print(type(A.make()).__name__)\n'
                'print(type(B.make()).__name__)\n'
                'print(type(B().make()).__name__)\n'
            ),
            "expected": ['A', 'B', 'B'],
            "hint": (
                'def __get__(self, obj, owner=None): if owner is None: owner = type(obj); return types.MethodType(self.func, owner).'
            ),
        },
        {
            "id": "ds-slots-point",
            "mode": "stdout",
            "title": "Слоты для Point",
            "statement": (
                'Добавьте в Point атрибут __slots__ с полями x и y, чтобы у экземпляров не было __dict__ и нельзя было добавлять новые атрибуты.'
            ),
            "starter": (
                'class Point:\n'
                '    def __init__(self, x, y):\n'
                '        self.x = x\n'
                '        self.y = y\n'
            ),
            "driver": (
                'p = Point(1, 2)\n'
                'print(p.x + p.y)\n'
                'print(hasattr(p, "__dict__"))\n'
                'try:\n'
                '    p.z = 3\n'
                'except AttributeError:\n'
                '    print("нельзя")\n'
            ),
            "expected": ['3', 'False', 'нельзя'],
            "hint": '__slots__ = ("x", "y") — в теле класса, до __init__.',
        },
        {
            "id": "ds-cached-report",
            "mode": "stdout",
            "title": "Кэшируем тяжёлую сумму",
            "statement": (
                'Report.total считает сумму значений при каждом обращении (счётчик calls растёт). Сделайте так, чтобы сумма вычислялась один раз для экземпляра, не меняя вызов r.total.'
            ),
            "starter": (
                'class Report:\n'
                '    calls = 0\n'
                '\n'
                '    def __init__(self, values):\n'
                '        self.values = values\n'
                '\n'
                '    @property\n'
                '    def total(self):\n'
                '        Report.calls += 1\n'
                '        return sum(self.values)\n'
            ),
            "driver": (
                'r = Report([1, 2, 3])\n'
                'print(r.total, r.total, r.total)\n'
                'print(Report.calls)\n'
                'print(Report([5]).total, Report.calls)\n'
            ),
            "expected": ['6 6 6', '1', '5 2'],
            "hint": "from functools import cached_property и заменить @property на @cached_property.",
        },
    ],
}
