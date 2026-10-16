"""Задачи «Python как первый язык»: проектирование классов (главы 40–42) — абстрактные классы, протоколы и обобщения, множественное наследование и MRO.

Ключ — номер главы. Режим stdout со скрытым driver.
"""

TASKS: dict[int, list[dict]] = {
    40: [
        {
            "id": "abc-shape",
            "mode": "stdout",
            "title": "Абстрактная фигура",
            "statement": (
                'Напишите абстрактный класс Shape (от ABC) с обязательным методом area(), а также классы Rect(w, h) и Circle(r) (площадь круга — 3.14 * r * r). Создать Shape напрямую нельзя.'
            ),
            "starter": "from abc import ABC, abstractmethod\n",
            "driver": (
                'try:\n'
                '    Shape()\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
                'shapes = [Rect(2, 3), Circle(1)]\n'
                'print([s.area() for s in shapes])\n'
                'print(all(isinstance(s, Shape) for s in shapes))\n'
            ),
            "expected": ['TypeError', '[6, 3.14]', 'True'],
            "hint": "class Shape(ABC): @abstractmethod def area(self): ...; наследники реализуют area.",
        },
        {
            "id": "abc-exporter",
            "mode": "stdout",
            "title": "Контракт экспортёра",
            "statement": (
                'Напишите абстрактный Exporter: обязательный метод export(data) и обязательное свойство extension. Класс, где не реализовано что-то одно, создать нельзя; полный наследник создаётся и работает.'
            ),
            "starter": "from abc import ABC, abstractmethod\n",
            "driver": (
                'class Csv(Exporter):\n'
                '    extension = "csv"\n'
                '\n'
                '    def export(self, data):\n'
                '        return ",".join(map(str, data))\n'
                '\n'
                '\n'
                'class NoExt(Exporter):\n'
                '    def export(self, data):\n'
                '        return ""\n'
                '\n'
                '\n'
                'class NoExport(Exporter):\n'
                '    @property\n'
                '    def extension(self):\n'
                '        return "x"\n'
                '\n'
                '\n'
                'c = Csv()\n'
                'print(c.export([1, 2, 3]), c.extension)\n'
                'for cls in (NoExt, NoExport):\n'
                '    try:\n'
                '        cls()\n'
                '    except TypeError:\n'
                '        print("TypeError", cls.__name__)\n'
            ),
            "expected": ['1,2,3 csv', 'TypeError NoExt', 'TypeError NoExport'],
            "hint": (
                'Свойство: @property над @abstractmethod. Атрибут класса extension = "csv" тоже закрывает абстрактное свойство.'
            ),
        },
        {
            "id": "abc-template",
            "mode": "stdout",
            "title": "Шаблонный метод отчёта",
            "statement": (
                'Напишите абстрактный Report с готовым методом render(): он собирает строку из header(), body() и footer(). header и footer реализованы (возвращают «== отчёт ==» и «== конец ==»), а body — абстрактный шаг. Части склеиваются через перевод строки.'
            ),
            "starter": "from abc import ABC, abstractmethod\n",
            "driver": (
                'class Sales(Report):\n'
                '    def body(self):\n'
                '        return "продажи: 42"\n'
                '\n'
                '\n'
                'class Users(Report):\n'
                '    def body(self):\n'
                '        return "пользователей: 7"\n'
                '\n'
                '    def footer(self):\n'
                '        return "-- конец --"\n'
                '\n'
                '\n'
                'print(Sales().render())\n'
                'print(Users().render())\n'
                'try:\n'
                '    Report()\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
            ),
            "expected": ['== отчёт ==', 'продажи: 42', '== конец ==', '== отчёт ==', 'пользователей: 7', '-- конец --', 'TypeError'],
            "hint": 'def render(self): return "\\n".join([self.header(), self.body(), self.footer()]).',
        },
        {
            "id": "abc-factory",
            "mode": "stdout",
            "title": "Абстрактная фабрика",
            "statement": (
                'Напишите абстрактный Animal: абстрактный классовый метод create() и абстрактный метод speak(). Для каждого наследника создавайте объект через create(); Animal создать напрямую нельзя.'
            ),
            "starter": "from abc import ABC, abstractmethod\n",
            "driver": (
                'class Dog(Animal):\n'
                '    @classmethod\n'
                '    def create(cls):\n'
                '        return cls()\n'
                '\n'
                '    def speak(self):\n'
                '        return "гав"\n'
                '\n'
                '\n'
                'class Cat(Animal):\n'
                '    @classmethod\n'
                '    def create(cls):\n'
                '        return cls()\n'
                '\n'
                '    def speak(self):\n'
                '        return "мяу"\n'
                '\n'
                '\n'
                'print([cls.create().speak() for cls in (Dog, Cat)])\n'
                'try:\n'
                '    Animal.create()\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
                'try:\n'
                '    class Bad(Animal):\n'
                '        def speak(self):\n'
                '            return "?"\n'
                '    Bad()\n'
                'except TypeError:\n'
                '    print("TypeError Bad")\n'
            ),
            "expected": ["['гав', 'мяу']", 'TypeError', 'TypeError Bad'],
            "hint": (
                '@classmethod над @abstractmethod; тело create() в базовом классе может быть пустым или возвращать cls().'
            ),
        },
        {
            "id": "abc-subclasshook",
            "mode": "stdout",
            "title": "Автоматический «подкласс»",
            "statement": (
                'Напишите ABC-класс HasLen: любой класс, у которого есть метод __len__, автоматически считается его подклассом (через __subclasshook__), без явного наследования. Проверьте, что isinstance работает для списков и для собственных классов с __len__, но не для чисел.'
            ),
            "starter": (
                'from abc import ABC\n'
                '\n'
                '\n'
                'class HasLen(ABC):\n'
                '    pass\n'
            ),
            "driver": (
                'class Box:\n'
                '    def __len__(self):\n'
                '        return 3\n'
                '\n'
                '\n'
                'class Empty:\n'
                '    pass\n'
                '\n'
                '\n'
                'print(isinstance([], HasLen), isinstance(Box(), HasLen))\n'
                'print(isinstance(5, HasLen), isinstance(Empty(), HasLen))\n'
                'print(issubclass(str, HasLen))\n'
            ),
            "expected": ['True True', 'False False', 'True'],
            "hint": (
                '@classmethod def __subclasshook__(cls, C): if cls is HasLen: return hasattr(C, "__len__"); return NotImplemented.'
            ),
        },
        {
            "id": "abc-register",
            "mode": "stdout",
            "title": "Виртуальный подкласс",
            "statement": (
                'Класс Duck уже есть и ни от кого не наследуется. Напишите абстрактный Quacker и зарегистрируйте Duck как его виртуальный подкласс, чтобы isinstance(Duck(), Quacker) было истинным, а для Dog — нет.'
            ),
            "starter": (
                'from abc import ABC\n'
                '\n'
                '\n'
                'class Duck:\n'
                '    def quack(self):\n'
                '        return "кря"\n'
                '\n'
                '\n'
                'class Dog:\n'
                '    pass\n'
            ),
            "driver": (
                'print(isinstance(Duck(), Quacker), isinstance(Dog(), Quacker))\n'
                'print(issubclass(Duck, Quacker), Duck.__mro__[0].__name__, Quacker in Duck.__mro__)\n'
            ),
            "expected": ['True False', 'True Duck False'],
            "hint": "class Quacker(ABC): pass; Quacker.register(Duck).",
        },
        {
            "id": "abc-sequence",
            "mode": "stdout",
            "title": "Последовательность на двух методах",
            "statement": (
                'Напишите Countdown(n) — наследника collections.abc.Sequence, содержащего числа n, n-1, …, 1. Реализуйте только __len__ и __getitem__ (индекс вне диапазона — IndexError): остальное приходит от базового класса.'
            ),
            "starter": "from collections.abc import Sequence\n",
            "driver": (
                'c = Countdown(4)\n'
                'print(len(c), c[0], c[-1])\n'
                'print(list(c), list(reversed(c)))\n'
                'print(3 in c, 9 in c, c.index(2), c.count(1))\n'
                'print(c[1:3] if isinstance(c[1:3], (list, tuple, range)) else "срез")\n'
            ),
            "expected": ['4 4 1', '[4, 3, 2, 1] [1, 2, 3, 4]', 'True False 2 1', '[3, 2]'],
            "hint": (
                '__getitem__(self, i): if isinstance(i, slice): return [self[k] for k in range(*i.indices(len(self)))]; иначе проверьте границы и верните self.n - i (для отрицательных сначала i += len(self)).'
            ),
        },
        {
            "id": "abc-storage-copy",
            "mode": "stdout",
            "title": "Хранилища и подмена",
            "statement": (
                'Напишите абстрактный Storage (методы read(key) и write(key, value)), реализацию MemoryStorage на словаре (read несуществующего ключа даёт KeyError) и функцию copy_all(src, dst, keys), копирующую значения по ключам из src в dst. Функция должна работать с любыми Storage.'
            ),
            "starter": "from abc import ABC, abstractmethod\n",
            "driver": (
                'class Upper(Storage):\n'
                '    def __init__(self):\n'
                '        self.data = {}\n'
                '\n'
                '    def read(self, key):\n'
                '        return self.data[key]\n'
                '\n'
                '    def write(self, key, value):\n'
                '        self.data[key] = value.upper()\n'
                '\n'
                '\n'
                'a = MemoryStorage()\n'
                'a.write("x", "привет")\n'
                'a.write("y", "мир")\n'
                'b = Upper()\n'
                'copy_all(a, b, ["x", "y"])\n'
                'print(b.read("x"), b.read("y"))\n'
                'try:\n'
                '    a.read("z")\n'
                'except KeyError:\n'
                '    print("KeyError")\n'
                'try:\n'
                '    Storage()\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
            ),
            "expected": ['ПРИВЕТ МИР', 'KeyError', 'TypeError'],
            "hint": "copy_all: for key in keys: dst.write(key, src.read(key)).",
        },
        {
            "id": "abc-describe",
            "mode": "stdout",
            "title": "Вид значения по абстрактным классам",
            "statement": (
                'Напишите describe(x): «строка» для str; «отображение» для Mapping; «последовательность» для Sequence; «итерируемое» для прочих Iterable; «число» для numbers.Number; иначе «прочее». Порядок проверок важен: строка — тоже последовательность.'
            ),
            "starter": (
                'import numbers\n'
                'from collections.abc import Iterable, Mapping, Sequence\n'
                '\n'
                '\n'
                'def describe(x):\n'
                '    pass\n'
            ),
            "driver": (
                'for v in ["abc", {}, [1], (1, 2), {1}, range(3), 5, 3.5, True, None, (i for i in range(2))]:\n'
                '    print(describe(v))\n'
            ),
            "expected": ['строка', 'отображение', 'последовательность', 'последовательность', 'итерируемое', 'последовательность', 'число', 'число', 'число', 'прочее', 'итерируемое'],
            "hint": "Проверяйте по очереди: str, Mapping, Sequence, Iterable, numbers.Number.",
        },
    ],
    41: [
        {
            "id": "tp-closeable",
            "mode": "stdout",
            "title": "Протокол Closeable",
            "statement": (
                'Напишите Protocol Closeable с методом close() (с декоратором runtime_checkable) и функцию close_all(items): она закрывает всё, что подходит под протокол, и возвращает, сколько объектов закрыто. Остальные пропускайте.'
            ),
            "starter": "from typing import Protocol, runtime_checkable\n",
            "driver": (
                'import io\n'
                '\n'
                '\n'
                'class Res:\n'
                '    def close(self):\n'
                '        print("Res закрыт")\n'
                '\n'
                '\n'
                'class Plain:\n'
                '    pass\n'
                '\n'
                '\n'
                'print(close_all([Res(), Plain(), io.StringIO(), 5]))\n'
                'print(isinstance(Res(), Closeable), isinstance(Plain(), Closeable))\n'
            ),
            "expected": ['Res закрыт', '2', 'True False'],
            "hint": (
                '@runtime_checkable class Closeable(Protocol): def close(self) -> None: ...; в close_all: if isinstance(item, Closeable): item.close().'
            ),
        },
        {
            "id": "tp-data-protocol",
            "mode": "stdout",
            "title": "Протокол с атрибутом",
            "statement": (
                'Напишите runtime_checkable-протокол HasName с атрибутом name: str и функцию names(items): список значений name у объектов, которые подходят под протокол (остальные пропускаются).'
            ),
            "starter": "from typing import Protocol, runtime_checkable\n",
            "driver": (
                'class User:\n'
                '    def __init__(self, name):\n'
                '        self.name = name\n'
                '\n'
                '\n'
                'class Pet:\n'
                '    name = "Барсик"\n'
                '\n'
                '\n'
                'class Thing:\n'
                '    pass\n'
                '\n'
                '\n'
                'print(names([User("Аня"), Thing(), Pet(), 5]))\n'
                'print(isinstance(User("x"), HasName), isinstance(Thing(), HasName))\n'
            ),
            "expected": ["['Аня', 'Барсик']", 'True False'],
            "hint": (
                'class HasName(Protocol): name: str — и @runtime_checkable; в names: [x.name for x in items if isinstance(x, HasName)].'
            ),
        },
        {
            "id": "tp-generic-stack",
            "mode": "stdout",
            "title": "Обобщённый стек",
            "statement": (
                'Напишите обобщённый Stack(Generic[T]) с методами push(x), pop() (на пустом стеке — IndexError), peek() и __len__. Запись Stack[int]() тоже должна создавать рабочий стек.'
            ),
            "starter": (
                'from typing import Generic, TypeVar\n'
                '\n'
                'T = TypeVar("T")\n'
            ),
            "driver": (
                's = Stack[int]()\n'
                's.push(1)\n'
                's.push(2)\n'
                'print(len(s), s.peek(), s.pop(), s.pop(), len(s))\n'
                'try:\n'
                '    s.pop()\n'
                'except IndexError:\n'
                '    print("IndexError")\n'
                'print(Stack.__parameters__[0].__name__)\n'
                'print(Stack[str].__origin__ is Stack)\n'
            ),
            "expected": ['2 2 2 1 0', 'IndexError', 'T', 'True'],
            "hint": (
                'class Stack(Generic[T]) со списком внутри; pop() у пустого списка и так поднимает IndexError.'
            ),
        },
        {
            "id": "tp-pep695-box",
            "mode": "stdout",
            "title": "Box в новом синтаксисе",
            "statement": (
                'Напишите класс Box[T] с новым синтаксисом параметров типа (Python 3.12+, без Generic и TypeVar): поле value, метод map(f) — возвращает новый Box со значением f(value), и __repr__ вида Box(3).'
            ),
            "starter": "# class Box[T]: ...\n",
            "driver": (
                'b = Box(3)\n'
                'print(b, b.map(str), b.map(lambda x: x * 2).map(str))\n'
                'print([p.__name__ for p in Box.__type_params__])\n'
                'print(b.map(str).value == "3")\n'
            ),
            "expected": ["Box(3) Box('3') Box('6')", "['T']", 'True'],
            "hint": (
                'class Box[T]: def __init__(self, value: T): ...; def map[U](self, f) -> "Box[U]": return Box(f(self.value)).'
            ),
        },
        {
            "id": "tp-typevar-bound",
            "mode": "stdout",
            "title": "TypeVar с границей",
            "statement": (
                'Опишите протокол Comparable (метод __lt__(self, other) -> bool), переменную типа T = TypeVar("T", bound=Comparable) и функцию biggest(items: list[T]) -> T, возвращающую наибольший элемент.'
            ),
            "starter": "from typing import Protocol, TypeVar\n",
            "driver": (
                'print(biggest([3, 1, 2]), biggest(["b", "a"]), biggest([2.5, 1.5]))\n'
                'print(T.__bound__.__name__, T.__name__)\n'
                'print(biggest.__annotations__["return"] is T)\n'
            ),
            "expected": ['3 b 2.5', 'Comparable T', 'True'],
            "hint": (
                'class Comparable(Protocol): def __lt__(self, other) -> bool: ...; T = TypeVar("T", bound=Comparable).'
            ),
        },
        {
            "id": "tp-overload",
            "mode": "stdout",
            "title": "Перегрузка для проверки типов",
            "statement": (
                'Опишите функцию first двумя заглушками @overload (str → str и list[int] → int) и одной настоящей реализацией, возвращающей первый элемент. typing.get_overloads(first) должен видеть две заглушки.'
            ),
            "starter": (
                'import typing\n'
                'from typing import overload\n'
            ),
            "driver": (
                'print(first("abc"), first([5, 6]))\n'
                'print(len(typing.get_overloads(first)))\n'
            ),
            "expected": ['a 5', '2'],
            "hint": (
                '@overload def first(x: str) -> str: ...; @overload def first(x: list[int]) -> int: ...; затем def first(x): return x[0].'
            ),
        },
        {
            "id": "tp-self-builder",
            "mode": "stdout",
            "title": "Цепочки вызовов с Self",
            "statement": (
                'Напишите класс Query с методами where(cond) и limit(n): оба сохраняют настройки в экземпляре, возвращают self и аннотированы результатом typing.Self (чтобы наследники сохраняли свой тип). Метод build() возвращает строку вида «WHERE a AND b LIMIT 3».'
            ),
            "starter": "from typing import Self\n",
            "driver": (
                'class SqlQuery(Query):\n'
                '    pass\n'
                '\n'
                '\n'
                'q = SqlQuery().where("a").where("b").limit(3)\n'
                'print(type(q).__name__, q.build())\n'
                'print(Query().build() == "")\n'
                'print(Query.where.__annotations__["return"] is Self, Query.limit.__annotations__["return"] is Self)\n'
            ),
            "expected": ['SqlQuery WHERE a AND b LIMIT 3', 'True', 'True True'],
            "hint": (
                'build: части = []; если conds — "WHERE " + " AND ".join(conds); если limit не None — "LIMIT n"; соединить пробелом.'
            ),
        },
        {
            "id": "tp-typeddict-validate",
            "mode": "stdout",
            "title": "Проверка словаря по TypedDict",
            "statement": (
                'Напишите validate(data, schema): по подсказкам TypedDict (typing.get_type_hints(schema)) верните отсортированный список ошибок: «нет ключа K», «лишний ключ K», «K: ожидался T» (имя типа), если значение не того типа.'
            ),
            "starter": (
                'import typing\n'
                '\n'
                '\n'
                'def validate(data, schema):\n'
                '    pass\n'
            ),
            "driver": (
                'class User(typing.TypedDict):\n'
                '    name: str\n'
                '    age: int\n'
                '\n'
                '\n'
                'print(validate({"name": "Ann", "age": 3}, User))\n'
                'print(validate({"name": 5, "extra": 1}, User))\n'
                'print(validate({}, User))\n'
            ),
            "expected": ['[]', "['name: ожидался str', 'лишний ключ extra', 'нет ключа age']", "['нет ключа age', 'нет ключа name']"],
            "hint": "hints = typing.get_type_hints(schema); пройдите по ключам hints и по ключам data.",
        },
        {
            "id": "tp-describe-type",
            "mode": "stdout",
            "title": "Тип словами",
            "statement": (
                'Напишите describe_type(tp): строка вроде «list[int]», «dict[str, list[int]]», «int | None» по аннотации (используйте typing.get_origin и get_args; для обычных классов — имя класса, для NoneType — «None», для объединений — через « | »).'
            ),
            "starter": (
                'import types\n'
                'import typing\n'
                '\n'
                '\n'
                'def describe_type(tp):\n'
                '    pass\n'
            ),
            "driver": (
                'from typing import Optional\n'
                '\n'
                'for t in [int, list[int], dict[str, list[int]], int | None, Optional[str], tuple[int, ...], type(None)]:\n'
                '    print(describe_type(t))\n'
            ),
            "expected": ['int', 'list[int]', 'dict[str, list[int]]', 'int | None', 'str | None', 'tuple[int, ...]', 'None'],
            "hint": (
                'origin = typing.get_origin(tp); args = typing.get_args(tp); для Union и UnionType — join через " | "; Ellipsis выводите как «...».'
            ),
        },
    ],
    42: [
        {
            "id": "mro-names",
            "mode": "stdout",
            "title": "Порядок разрешения методов",
            "statement": (
                'Напишите mro_names(cls): список имён классов в порядке разрешения методов (без object). Используйте cls.__mro__.'
            ),
            "starter": (
                'def mro_names(cls):\n'
                '    pass\n'
            ),
            "driver": (
                'class A: pass\n'
                'class B(A): pass\n'
                'class C(A): pass\n'
                'class D(B, C): pass\n'
                'class E(C, B): pass\n'
                '\n'
                '\n'
                'print(mro_names(D))\n'
                'print(mro_names(E))\n'
                'print(mro_names(A))\n'
            ),
            "expected": ["['D', 'B', 'C', 'A']", "['E', 'C', 'B', 'A']", "['A']"],
            "hint": "[c.__name__ for c in cls.__mro__ if c is not object].",
        },
        {
            "id": "mro-super-chain",
            "mode": "stdout",
            "title": "Кооперативная цепочка в ромбе",
            "statement": (
                'Класс A уже написан (печатает «A» и ничего не вызывает дальше). Напишите B(A), C(A) и D(B, C): метод hello() каждого печатает своё имя и вызывает super().hello(), так что при D().hello() каждый класс отработает ровно один раз в порядке D, B, C, A.'
            ),
            "starter": (
                'class A:\n'
                '    def hello(self):\n'
                '        print("A")\n'
            ),
            "driver": (
                'D().hello()\n'
                'print("--")\n'
                'B().hello()\n'
                'print([c.__name__ for c in D.__mro__])\n'
            ),
            "expected": ['D', 'B', 'C', 'A', '--', 'B', 'A', "['D', 'B', 'C', 'A', 'object']"],
            "hint": 'В каждом hello: print("X"); super().hello(). Ромб будет пройден по MRO D, B, C, A.',
        },
        {
            "id": "mro-can-combine",
            "mode": "stdout",
            "title": "Можно ли объединить базы",
            "statement": (
                'Напишите can_combine(*bases): True, если можно создать класс с этими базами (в таком порядке), и False, если Питон не может построить согласованный MRO (TypeError).'
            ),
            "starter": (
                'def can_combine(*bases):\n'
                '    pass\n'
            ),
            "driver": (
                'class A: pass\n'
                'class B(A): pass\n'
                'class C(A): pass\n'
                '\n'
                '\n'
                'print(can_combine(B, C), can_combine(B, A), can_combine(A, B))\n'
                'print(can_combine(C, B), can_combine())\n'
            ),
            "expected": ['True True False', 'True True'],
            "hint": 'try: type("X", bases, {}) except TypeError: return False; return True.',
        },
        {
            "id": "mro-coop-init",
            "mode": "stdout",
            "title": "Кооперативный __init__",
            "statement": (
                'Напишите NameMixin и AgeMixin: каждый принимает свой именованный параметр (name или age), сохраняет его и передаёт остальные параметры дальше через super().__init__(**kwargs). Базовый Base уже «гасит» оставшиеся параметры в поле extra. Порядок баз в Person не должен влиять на результат.'
            ),
            "starter": (
                'class Base:\n'
                '    def __init__(self, **kwargs):\n'
                '        self.extra = kwargs\n'
            ),
            "driver": (
                'class Person(NameMixin, AgeMixin, Base):\n'
                '    pass\n'
                '\n'
                '\n'
                'class Other(AgeMixin, NameMixin, Base):\n'
                '    pass\n'
                '\n'
                '\n'
                'for cls in (Person, Other):\n'
                '    p = cls(name="Аня", age=3, city="Омск")\n'
                '    print(p.name, p.age, p.extra)\n'
            ),
            "expected": ["Аня 3 {'city': 'Омск'}", "Аня 3 {'city': 'Омск'}"],
            "hint": "def __init__(self, *, name, **kwargs): super().__init__(**kwargs); self.name = name.",
        },
        {
            "id": "mro-repr-mixin",
            "mode": "stdout",
            "title": "Миксин ReprMixin",
            "statement": (
                'Напишите миксин ReprMixin: __repr__ выдаёт имя класса и пары «поле=значение» атрибутов экземпляра в порядке создания (Point(x=1, y=2)). Он должен работать в сочетании с любым классом без собственного __init__.'
            ),
            "starter": (
                'class ReprMixin:\n'
                '    pass\n'
            ),
            "driver": (
                'class Point(ReprMixin):\n'
                '    def __init__(self, x, y):\n'
                '        self.x, self.y = x, y\n'
                '\n'
                '\n'
                'class Base:\n'
                '    def __init__(self):\n'
                '        self.id = 7\n'
                '\n'
                '\n'
                'class Item(ReprMixin, Base):\n'
                '    pass\n'
                '\n'
                '\n'
                'print(Point(1, 2))\n'
                'print(Item())\n'
                'print([Point(0, 0)])\n'
            ),
            "expected": ['Point(x=1, y=2)', 'Item(id=7)', '[Point(x=0, y=0)]'],
            "hint": '", ".join(f"{k}={v!r}" for k, v in vars(self).items()).',
        },
        {
            "id": "mro-json-mixin",
            "mode": "stdout",
            "title": "Миксин JsonMixin",
            "statement": (
                'Напишите JsonMixin с методом to_json(): JSON-строка из атрибутов экземпляра с отсортированными ключами (json.dumps(..., sort_keys=True, ensure_ascii=False)) и классовым методом from_json(text), создающим объект без вызова __init__ и записывающим в него поля из JSON.'
            ),
            "starter": (
                'import json\n'
                '\n'
                '\n'
                'class JsonMixin:\n'
                '    pass\n'
            ),
            "driver": (
                'class User(JsonMixin):\n'
                '    def __init__(self, name, age):\n'
                '        self.name = name\n'
                '        self.age = age\n'
                '\n'
                '\n'
                'u = User("Аня", 30)\n'
                'text = u.to_json()\n'
                'print(text)\n'
                'v = User.from_json(text)\n'
                'print(type(v).__name__, v.name, v.age)\n'
            ),
            "expected": ['{"age": 30, "name": "Аня"}', 'User Аня 30'],
            "hint": "from_json: obj = cls.__new__(cls); obj.__dict__.update(json.loads(text)); return obj.",
        },
        {
            "id": "mro-logging-mixin",
            "mode": "stdout",
            "title": "Миксин-обёртка через super",
            "statement": (
                'Класс Model уже умеет save() (возвращает «сохранено»). Напишите LoggingMixin: его save() записывает в список LOG строку «перед save», вызывает super().save(), записывает «после save» и возвращает результат. Миксин нужно ставить слева от Model.'
            ),
            "starter": (
                'LOG = []\n'
                '\n'
                '\n'
                'class Model:\n'
                '    def save(self):\n'
                '        return "сохранено"\n'
            ),
            "driver": (
                'class Logged(LoggingMixin, Model):\n'
                '    pass\n'
                '\n'
                '\n'
                'class WrongOrder(Model, LoggingMixin):\n'
                '    pass\n'
                '\n'
                '\n'
                'print(Logged().save(), LOG)\n'
                'LOG.clear()\n'
                'print(WrongOrder().save(), LOG)\n'
            ),
            "expected": ["сохранено ['перед save', 'после save']", 'сохранено []'],
            "hint": (
                'class LoggingMixin: def save(self): LOG.append(...); result = super().save(); LOG.append(...); return result.'
            ),
        },
        {
            "id": "mro-where-defined",
            "mode": "stdout",
            "title": "Где определён метод",
            "statement": (
                'Напишите where_defined(cls, name): имя первого класса в MRO, у которого имя name есть в собственном __dict__, или None, если нигде нет. А также chain(cls, name): список имён всех классов в MRO, определяющих это имя (в порядке MRO).'
            ),
            "starter": (
                'def where_defined(cls, name):\n'
                '    pass\n'
                '\n'
                '\n'
                'def chain(cls, name):\n'
                '    pass\n'
            ),
            "driver": (
                'class A:\n'
                '    def f(self): ...\n'
                '    def g(self): ...\n'
                '\n'
                '\n'
                'class B(A):\n'
                '    def f(self): ...\n'
                '\n'
                '\n'
                'class C(A):\n'
                '    def f(self): ...\n'
                '    def h(self): ...\n'
                '\n'
                '\n'
                'class D(B, C):\n'
                '    pass\n'
                '\n'
                '\n'
                'print(where_defined(D, "f"), where_defined(D, "g"), where_defined(D, "h"), where_defined(D, "zzz"))\n'
                'print(chain(D, "f"), chain(D, "h"))\n'
            ),
            "expected": ['B A C None', "['B', 'C', 'A'] ['C']"],
            "hint": "for c in cls.__mro__: if name in vars(c): ...",
        },
        {
            "id": "mro-validators",
            "mode": "stdout",
            "title": "Проверки на миксинах",
            "statement": (
                'Базовый Validator.validate(value) возвращает пустой список. Напишите NotEmpty (ошибка «пусто» для пустой строки) и NoDigits (ошибка «цифры» если в строке есть цифра): каждый вызывает super().validate(value) и добавляет свою ошибку. Классы собираются в любом сочетании.'
            ),
            "starter": (
                'class Validator:\n'
                '    def validate(self, value):\n'
                '        return []\n'
            ),
            "driver": (
                'class Name(NotEmpty, NoDigits, Validator):\n'
                '    pass\n'
                '\n'
                '\n'
                'class OnlyDigits(NoDigits, Validator):\n'
                '    pass\n'
                '\n'
                '\n'
                'print(Name().validate("Аня"))\n'
                'print(Name().validate(""))\n'
                'print(Name().validate("a1"))\n'
                'print(OnlyDigits().validate("x9"), OnlyDigits().validate(""))\n'
            ),
            "expected": ['[]', "['пусто']", "['цифры']", "['цифры'] []"],
            "hint": (
                'errors = super().validate(value); if не value: errors = errors + ["пусто"]; return errors.'
            ),
        },
    ],
}
