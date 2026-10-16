"""Задачи «Python как первый язык»: метапрограммирование (главы 29–32) — декораторы, интроспекция, метаклассы, ast/exec/dis.

Ключ — номер главы. Режим stdout со скрытым driver.
"""

TASKS: dict[int, list[dict]] = {
    29: [
        {
            "id": "dc-tag-stack",
            "mode": "stdout",
            "title": "Теги и порядок декораторов",
            "statement": (
                'Напишите декоратор tag(name): он оборачивает строку, которую возвращает функция, в <name>…</name>. Два тега подряд должны вкладываться так, что верхний оказывается снаружи.'
            ),
            "starter": (
                'def tag(name):\n'
                '    pass\n'
            ),
            "driver": (
                '@tag("b")\n'
                '@tag("i")\n'
                'def text():\n'
                '    return "привет"\n'
                '\n'
                '\n'
                'print(text())\n'
                '\n'
                '\n'
                '@tag("p")\n'
                'def greet(name):\n'
                '    return f"Здравствуйте, {name}"\n'
                '\n'
                '\n'
                'print(greet("Аня"))\n'
            ),
            "expected": ['<b><i>привет</i></b>', '<p>Здравствуйте, Аня</p>'],
            "hint": (
                'tag возвращает decorator(func), тот возвращает wrapper(*args, **kwargs): return f"<{name}>{func(*args, **kwargs)}</{name}>".'
            ),
        },
        {
            "id": "dc-repeat-optional",
            "mode": "stdout",
            "title": "repeat: со скобками и без",
            "statement": (
                'Напишите декоратор repeat, который работает в двух формах: @repeat (два вызова функции) и @repeat(times=3) (заданное число вызовов). Он возвращает результат последнего вызова. Параметр times — только по имени.'
            ),
            "starter": (
                'def repeat(func=None, *, times=2):\n'
                '    pass\n'
            ),
            "driver": (
                'calls = []\n'
                '\n'
                '\n'
                '@repeat\n'
                'def a():\n'
                '    calls.append("a")\n'
                '    return len(calls)\n'
                '\n'
                '\n'
                '@repeat(times=3)\n'
                'def b():\n'
                '    calls.append("b")\n'
                '    return len(calls)\n'
                '\n'
                '\n'
                'print(a(), calls)\n'
                'print(b(), calls)\n'
            ),
            "expected": ["2 ['a', 'a']", "5 ['a', 'a', 'b', 'b', 'b']"],
            "hint": "Если func is not None — return decorate(func); иначе return decorate.",
        },
        {
            "id": "dc-counted-wraps",
            "mode": "stdout",
            "title": "Счётчик вызовов и метаданные",
            "statement": (
                'Напишите декоратор counted: он считает вызовы в атрибуте wrapper.calls (начинается с нуля), сохраняет имя и документацию оригинала и ссылку __wrapped__ на него.'
            ),
            "starter": (
                'def counted(func):\n'
                '    pass\n'
            ),
            "driver": (
                '@counted\n'
                'def add(a, b):\n'
                '    """Складывает числа."""\n'
                '    return a + b\n'
                '\n'
                '\n'
                'print(add(1, 2), add(3, 4), add.calls)\n'
                'print(add.__name__, add.__doc__)\n'
                'print(add.__wrapped__(10, 20))\n'
                'print(add.calls)\n'
            ),
            "expected": ['3 7 2', 'add Складывает числа.', '30', '2'],
            "hint": (
                '@functools.wraps(func) даёт имя, документацию и __wrapped__; счётчик — wrapper.calls = 0 после определения wrapper.'
            ),
        },
        {
            "id": "dc-class-plugin",
            "mode": "stdout",
            "title": "Реестр плагинов (декоратор класса)",
            "statement": (
                'Напишите декоратор класса plugin: он добавляет класс в словарь PLUGINS под именем в нижнем регистре и возвращает класс без изменений.'
            ),
            "starter": (
                'PLUGINS = {}\n'
                '\n'
                '\n'
                'def plugin(cls):\n'
                '    pass\n'
            ),
            "driver": (
                '@plugin\n'
                'class Json:\n'
                '    pass\n'
                '\n'
                '\n'
                '@plugin\n'
                'class Csv:\n'
                '    pass\n'
                '\n'
                '\n'
                'print(sorted(PLUGINS))\n'
                'print(PLUGINS["json"] is Json, Json.__name__)\n'
            ),
            "expected": ["['csv', 'json']", 'True Json'],
            "hint": "PLUGINS[cls.__name__.lower()] = cls; return cls.",
        },
        {
            "id": "dc-auto-repr",
            "mode": "stdout",
            "title": "Декоратор класса auto_repr",
            "statement": (
                'Напишите декоратор класса auto_repr: он добавляет классу метод __repr__, который печатает имя класса и атрибуты экземпляра в порядке создания: Point(x=1, y=2).'
            ),
            "starter": (
                'def auto_repr(cls):\n'
                '    pass\n'
            ),
            "driver": (
                '@auto_repr\n'
                'class Point:\n'
                '    def __init__(self, x, y):\n'
                '        self.x = x\n'
                '        self.y = y\n'
                '\n'
                '\n'
                'print(Point(1, 2))\n'
                'print([Point(0, -1)])\n'
            ),
            "expected": ['Point(x=1, y=2)', '[Point(x=0, y=-1)]'],
            "hint": (
                'def __repr__(self): fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items()); cls.__repr__ = __repr__; return cls.'
            ),
        },
        {
            "id": "dc-retry",
            "mode": "stdout",
            "title": "Повтор при ошибке",
            "statement": (
                'Напишите декоратор retry(times, exceptions=(Exception,)): вызывает функцию до times раз; если очередной вызов поднял одно из exceptions — пробует снова; после последней неудачи пробрасывает ошибку. Успешный результат возвращается сразу.'
            ),
            "starter": (
                'def retry(times, exceptions=(Exception,)):\n'
                '    pass\n'
            ),
            "driver": (
                'attempts = []\n'
                '\n'
                '\n'
                '@retry(3, (ConnectionError,))\n'
                'def flaky():\n'
                '    attempts.append(1)\n'
                '    if len(attempts) < 3:\n'
                '        raise ConnectionError("сбой")\n'
                '    return "ок"\n'
                '\n'
                '\n'
                'print(flaky(), len(attempts))\n'
                '\n'
                '\n'
                '@retry(2)\n'
                'def broken():\n'
                '    raise ValueError("всегда")\n'
                '\n'
                '\n'
                'try:\n'
                '    broken()\n'
                'except ValueError as e:\n'
                '    print("ValueError", e)\n'
                '\n'
                '\n'
                '@retry(3, (KeyError,))\n'
                'def other():\n'
                '    raise TypeError("не наша")\n'
                '\n'
                '\n'
                'try:\n'
                '    other()\n'
                'except TypeError:\n'
                '    print("TypeError без повторов")\n'
            ),
            "expected": ['ок 3', 'ValueError всегда', 'TypeError без повторов'],
            "hint": (
                'for attempt in range(times): try: return func(...) except exceptions: if attempt == times - 1: raise.'
            ),
        },
        {
            "id": "dc-async-aware",
            "mode": "stdout",
            "title": "Декоратор для sync и async",
            "statement": (
                'Напишите декоратор traced: он печатает «вызов <имя>» перед выполнением и «готово <имя>» после — и для обычных функций, и для async def (для них обёртка должна быть асинхронной и дожидаться результата).'
            ),
            "starter": (
                'import inspect\n'
                '\n'
                '\n'
                'def traced(func):\n'
                '    pass\n'
            ),
            "driver": (
                'import asyncio\n'
                '\n'
                '\n'
                '@traced\n'
                'def plain(x):\n'
                '    return x + 1\n'
                '\n'
                '\n'
                '@traced\n'
                'async def fetch(x):\n'
                '    await asyncio.sleep(0)\n'
                '    return x * 2\n'
                '\n'
                '\n'
                'print(plain(1))\n'
                'print(asyncio.run(fetch(5)))\n'
                'print(inspect.iscoroutinefunction(fetch), inspect.iscoroutinefunction(plain))\n'
            ),
            "expected": ['вызов plain', 'готово plain', '2', 'вызов fetch', 'готово fetch', '10', 'True False'],
            "hint": (
                'if inspect.iscoroutinefunction(func): async def wrapper(...): ... result = await func(...); иначе обычная обёртка.'
            ),
        },
        {
            "id": "dc-callcounter-class",
            "mode": "stdout",
            "title": "Класс-декоратор для функций и методов",
            "statement": (
                'Допишите класс-декоратор CallCounter: он считает вызовы в атрибуте calls, сохраняет метаданные оригинала (functools.update_wrapper) и работает не только на функциях, но и на методах — для этого добавьте __get__ (при обращении через класс возвращайте сам счётчик).'
            ),
            "starter": (
                'import functools\n'
                'import types\n'
                '\n'
                '\n'
                'class CallCounter:\n'
                '    def __init__(self, func):\n'
                '        self.func = func\n'
                '        self.calls = 0\n'
            ),
            "driver": (
                '@CallCounter\n'
                'def hello(name):\n'
                '    return f"hi {name}"\n'
                '\n'
                '\n'
                'class A:\n'
                '    @CallCounter\n'
                '    def m(self, x):\n'
                '        return x * 2\n'
                '\n'
                '\n'
                'print(hello("a"), hello("b"), hello.calls)\n'
                'a = A()\n'
                'print(a.m(2), a.m(3), A.m.calls)\n'
                'print(hello.__name__)\n'
            ),
            "expected": ['hi a hi b 2', '4 6 2', 'hello'],
            "hint": (
                '__call__ увеличивает calls; __get__(self, obj, objtype=None): if obj is None: return self; return types.MethodType(self, obj).'
            ),
        },
        {
            "id": "dc-checked-annotations",
            "mode": "stdout",
            "title": "Проверка аргументов по аннотациям",
            "statement": (
                'Напишите декоратор checked: перед вызовом он привязывает аргументы к подписи функции (inspect.signature(...).bind) и для каждого параметра с аннотацией-типом проверяет isinstance; при несовпадении поднимает TypeError. Параметры без аннотаций не проверяются.'
            ),
            "starter": (
                'import inspect\n'
                '\n'
                '\n'
                'def checked(func):\n'
                '    pass\n'
            ),
            "driver": (
                '@checked\n'
                'def add(a: int, b: int, note=None):\n'
                '    return a + b\n'
                '\n'
                '\n'
                'print(add(1, 2))\n'
                'print(add(a=3, b=4, note="x"))\n'
                'try:\n'
                '    add(1, "2")\n'
                'except TypeError as e:\n'
                '    print("TypeError")\n'
                'try:\n'
                '    add(1.5, 2)\n'
                'except TypeError:\n'
                '    print("TypeError float")\n'
            ),
            "expected": ['3', '7', 'TypeError', 'TypeError float'],
            "hint": (
                'bound = sig.bind(*args, **kwargs); for name, value in bound.arguments.items(): ann = sig.parameters[name].annotation; if ann is not inspect.Parameter.empty and not isinstance(value, ann): raise TypeError.'
            ),
        },
    ],
    30: [
        {
            "id": "rf-public-data",
            "mode": "stdout",
            "title": "Публичные данные объекта",
            "statement": (
                'Напишите public_data(obj): отсортированный список имён атрибутов объекта (включая атрибуты класса), которые не начинаются с подчёркивания и не являются вызываемыми.'
            ),
            "starter": (
                'def public_data(obj):\n'
                '    pass\n'
            ),
            "driver": (
                'class A:\n'
                '    kind = "x"\n'
                '\n'
                '    def __init__(self):\n'
                '        self.a = 1\n'
                '        self._hidden = 2\n'
                '        self.fn = lambda: 0\n'
                '\n'
                '    def method(self):\n'
                '        return 1\n'
                '\n'
                '\n'
                'print(public_data(A()))\n'
                'print(public_data(object()))\n'
            ),
            "expected": ["['a', 'kind']", '[]'],
            "hint": 'for name in dir(obj): if not name.startswith("_") and not callable(getattr(obj, name)).',
        },
        {
            "id": "rf-dispatch",
            "mode": "stdout",
            "title": "Диспетчер команд по имени",
            "statement": (
                'Напишите dispatch(obj, command, *args): вызывает метод obj с именем cmd_<command> и возвращает результат. Если такого метода нет, поднимайте ValueError("неизвестная команда: <command>"). Доступ только к методам с префиксом cmd_.'
            ),
            "starter": (
                'def dispatch(obj, command, *args):\n'
                '    pass\n'
            ),
            "driver": (
                'class Shell:\n'
                '    def cmd_add(self, a, b):\n'
                '        return a + b\n'
                '\n'
                '    def cmd_echo(self, text):\n'
                '        return text\n'
                '\n'
                '    def secret(self):\n'
                '        return "не должно вызываться"\n'
                '\n'
                '\n'
                'sh = Shell()\n'
                'print(dispatch(sh, "add", 2, 3))\n'
                'print(dispatch(sh, "echo", "привет"))\n'
                'for bad in ("secret", "mul"):\n'
                '    try:\n'
                '        dispatch(sh, bad)\n'
                '    except ValueError as e:\n'
                '        print(e)\n'
            ),
            "expected": ['5', 'привет', 'неизвестная команда: secret', 'неизвестная команда: mul'],
            "hint": 'handler = getattr(obj, "cmd_" + command, None); если None — ValueError.',
        },
        {
            "id": "rf-param-info",
            "mode": "stdout",
            "title": "Описание параметров функции",
            "statement": (
                'Напишите param_info(func): список кортежей (имя, вид, есть_значение_по_умолчанию) для каждого параметра функции по её подписи. Вид — имя элемента inspect.Parameter.kind (например, KEYWORD_ONLY).'
            ),
            "starter": (
                'import inspect\n'
                '\n'
                '\n'
                'def param_info(func):\n'
                '    pass\n'
            ),
            "driver": (
                'def f(a, /, b, c=1, *args, d, e=2, **kw):\n'
                '    pass\n'
                '\n'
                '\n'
                'for row in param_info(f):\n'
                '    print(row)\n'
            ),
            "expected": ["('a', 'POSITIONAL_ONLY', False)", "('b', 'POSITIONAL_OR_KEYWORD', False)", "('c', 'POSITIONAL_OR_KEYWORD', True)", "('args', 'VAR_POSITIONAL', False)", "('d', 'KEYWORD_ONLY', False)", "('e', 'KEYWORD_ONLY', True)", "('kw', 'VAR_KEYWORD', False)"],
            "hint": (
                'for p in inspect.signature(func).parameters.values(): p.name, p.kind.name, p.default is not inspect.Parameter.empty.'
            ),
        },
        {
            "id": "rf-resolve-args",
            "mode": "stdout",
            "title": "Какие значения достались параметрам",
            "statement": (
                'Напишите resolve_args(func, *args, **kwargs): привяжите вызов к подписи функции (bind), добавьте значения по умолчанию и верните обычный словарь «параметр → значение». Некорректный вызов должен поднимать TypeError.'
            ),
            "starter": (
                'import inspect\n'
                '\n'
                '\n'
                'def resolve_args(func, *args, **kwargs):\n'
                '    pass\n'
            ),
            "driver": (
                'def f(a, b=2, *rest, k=5):\n'
                '    pass\n'
                '\n'
                '\n'
                'print(resolve_args(f, 1))\n'
                'print(resolve_args(f, 1, 3, 4, k=0))\n'
                'try:\n'
                '    resolve_args(f)\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
            ),
            "expected": ["{'a': 1, 'b': 2, 'rest': (), 'k': 5}", "{'a': 1, 'b': 3, 'rest': (4,), 'k': 0}", 'TypeError'],
            "hint": (
                'bound = inspect.signature(func).bind(*args, **kwargs); bound.apply_defaults(); return dict(bound.arguments).'
            ),
        },
        {
            "id": "rf-closure-vars",
            "mode": "stdout",
            "title": "Что унесла вложенная функция",
            "statement": (
                'Напишите captured(func): словарь «имя свободной переменной → её значение» для замыкания (используйте __code__.co_freevars и __closure__). У функции без замыкания результат — пустой словарь.'
            ),
            "starter": (
                'def captured(func):\n'
                '    pass\n'
            ),
            "driver": (
                'def make(a, b):\n'
                '    def f(x):\n'
                '        return x * a + b\n'
                '    return f\n'
                '\n'
                '\n'
                'def plain(x):\n'
                '    return x\n'
                '\n'
                '\n'
                'print(sorted(captured(make(2, 3)).items()))\n'
                'print(captured(plain))\n'
            ),
            "expected": ["[('a', 2), ('b', 3)]", '{}'],
            "hint": "dict(zip(func.__code__.co_freevars, (c.cell_contents for c in func.__closure__ or ()))).",
        },
        {
            "id": "rf-all-subclasses",
            "mode": "stdout",
            "title": "Все потомки класса",
            "statement": (
                'Напишите all_subclasses(cls): отсортированный список имён всех прямых и косвенных потомков класса (без повторов, даже при ромбовидном наследовании).'
            ),
            "starter": (
                'def all_subclasses(cls):\n'
                '    pass\n'
            ),
            "driver": (
                'class Base: pass\n'
                'class A(Base): pass\n'
                'class B(Base): pass\n'
                'class C(A, B): pass\n'
                'class D(C): pass\n'
                '\n'
                '\n'
                'print(all_subclasses(Base))\n'
                'print(all_subclasses(C))\n'
                'print(all_subclasses(D))\n'
            ),
            "expected": ["['A', 'B', 'C', 'D']", "['D']", '[]'],
            "hint": "Рекурсивно обходите cls.__subclasses__() и собирайте имена во множество.",
        },
        {
            "id": "rf-to-dict",
            "mode": "stdout",
            "title": "Объект в словарь",
            "statement": (
                'Напишите to_dict(obj): словарь из атрибутов экземпляра (vars). Вложенные объекты с атрибутами превращайте рекурсивно, списки и кортежи обрабатывайте поэлементно (как списки), простые значения оставляйте как есть.'
            ),
            "starter": (
                'def to_dict(obj):\n'
                '    pass\n'
            ),
            "driver": (
                'class Address:\n'
                '    def __init__(self, city, zip_code):\n'
                '        self.city = city\n'
                '        self.zip = zip_code\n'
                '\n'
                '\n'
                'class Person:\n'
                '    def __init__(self, name, address, tags):\n'
                '        self.name = name\n'
                '        self.address = address\n'
                '        self.tags = tags\n'
                '\n'
                '\n'
                'p = Person("Ann", Address("Омск", 644000), ["a", "b"])\n'
                'print(to_dict(p))\n'
                'print(to_dict(Address("Тула", 1)))\n'
            ),
            "expected": ["{'name': 'Ann', 'address': {'city': 'Омск', 'zip': 644000}, 'tags': ['a', 'b']}", "{'city': 'Тула', 'zip': 1}"],
            "hint": (
                'Вспомогательная функция convert(value): если у значения есть __dict__ — to_dict, если list/tuple — [convert(x) ...], иначе значение.'
            ),
        },
        {
            "id": "rf-caller-name",
            "mode": "stdout",
            "title": "Имя вызвавшей функции",
            "statement": (
                'Напишите caller_name(): возвращает имя функции, из которой её вызвали (на уровне модуля — «<module>»). Используйте inspect.currentframe() и f_back; не забудьте удалить ссылку на кадр.'
            ),
            "starter": (
                'import inspect\n'
                '\n'
                '\n'
                'def caller_name():\n'
                '    pass\n'
            ),
            "driver": (
                'def outer():\n'
                '    return caller_name()\n'
                '\n'
                '\n'
                'def other():\n'
                '    return outer()\n'
                '\n'
                '\n'
                'print(outer())\n'
                'print(other())\n'
                'print(caller_name())\n'
            ),
            "expected": ['outer', 'outer', '<module>'],
            "hint": (
                'frame = inspect.currentframe().f_back; name = frame.f_code.co_name; del frame; return name.'
            ),
        },
        {
            "id": "rf-load-by-name",
            "mode": "stdout",
            "title": "Загрузка объекта по строке",
            "statement": (
                'Напишите load(path): по строке вида «пакет.модуль.имя» подключает модуль (importlib.import_module) и возвращает объект с этим именем. Нет модуля — ImportError, нет имени — AttributeError.'
            ),
            "starter": (
                'import importlib\n'
                '\n'
                '\n'
                'def load(path):\n'
                '    pass\n'
            ),
            "driver": (
                'print(load("math.sqrt")(16))\n'
                'print(load("os.path.join")("a", "b"))\n'
                'print(load("json.dumps")({"k": 1}))\n'
                'for bad in ("json.nope", "nomodule_zz.x"):\n'
                '    try:\n'
                '        load(bad)\n'
                '    except AttributeError:\n'
                '        print("AttributeError")\n'
                '    except ImportError:\n'
                '        print("ImportError")\n'
            ),
            "expected": ['4.0', 'a/b', '{"k": 1}', 'AttributeError', 'ImportError'],
            "hint": (
                'module_path, _, name = path.rpartition("."); getattr(importlib.import_module(module_path), name).'
            ),
        },
    ],
    31: [
        {
            "id": "mc-make-class",
            "mode": "stdout",
            "title": "Класс по описанию полей",
            "statement": (
                'Напишите make_class(name, fields): с помощью type(...) создайте класс с данным именем, __init__(self, *values) (число значений обязано совпадать с числом полей, иначе TypeError) и __repr__ вида P(x=1, y=2).'
            ),
            "starter": (
                'def make_class(name, fields):\n'
                '    pass\n'
            ),
            "driver": (
                'P = make_class("P", ["x", "y"])\n'
                'p = P(1, 2)\n'
                'print(p)\n'
                'print(P.__name__, type(P).__name__)\n'
                'try:\n'
                '    P(1)\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
                'print(p.x + p.y)\n'
            ),
            "expected": ['P(x=1, y=2)', 'P type', 'TypeError', '3'],
            "hint": (
                'Определите init и repr как вложенные функции и верните type(name, (), {"__init__": init, "__repr__": repr_}).'
            ),
        },
        {
            "id": "mc-registry",
            "mode": "stdout",
            "title": "Реестр потомков (__init_subclass__)",
            "statement": (
                'Допишите базовый класс Plugin: каждый потомок автоматически попадает в словарь Plugin.registry. Ключ — аргумент name из class-оператора (class Json(Plugin, name="json")) или имя класса в нижнем регистре.'
            ),
            "starter": (
                'class Plugin:\n'
                '    registry = {}\n'
            ),
            "driver": (
                'class Json(Plugin, name="json"):\n'
                '    pass\n'
                '\n'
                '\n'
                'class CsvReader(Plugin):\n'
                '    pass\n'
                '\n'
                '\n'
                'print(sorted(Plugin.registry))\n'
                'print(Plugin.registry["json"] is Json, Plugin.registry["csvreader"] is CsvReader)\n'
            ),
            "expected": ["['csvreader', 'json']", 'True True'],
            "hint": (
                'def __init_subclass__(cls, name=None, **kwargs): super().__init_subclass__(**kwargs); Plugin.registry[name or cls.__name__.lower()] = cls.'
            ),
        },
        {
            "id": "mc-required-attrs",
            "mode": "stdout",
            "title": "Обязательный атрибут потомка",
            "statement": (
                'Допишите Shape: у каждого потомка при создании класса должен быть целочисленный атрибут sides; если его нет или он не int — поднимайте TypeError прямо в момент определения класса.'
            ),
            "starter": (
                'class Shape:\n'
                '    pass\n'
            ),
            "driver": (
                'class Tri(Shape):\n'
                '    sides = 3\n'
                '\n'
                '\n'
                'print(Tri.sides)\n'
                'try:\n'
                '    class Bad(Shape):\n'
                '        pass\n'
                'except TypeError:\n'
                '    print("TypeError без sides")\n'
                'try:\n'
                '    class Worse(Shape):\n'
                '        sides = "три"\n'
                'except TypeError:\n'
                '    print("TypeError не int")\n'
            ),
            "expected": ['3', 'TypeError без sides', 'TypeError не int'],
            "hint": (
                '__init_subclass__: if not isinstance(getattr(cls, "sides", None), int): raise TypeError(...).'
            ),
        },
        {
            "id": "mc-singleton",
            "mode": "stdout",
            "title": "Одиночка через метакласс",
            "statement": (
                'Напишите метакласс Singleton: у каждого класса с этим метаклассом существует не более одного экземпляра — повторный вызов класса возвращает уже созданный, а __init__ выполняется один раз. Разные классы получают разные экземпляры.'
            ),
            "starter": (
                'class Singleton(type):\n'
                '    pass\n'
            ),
            "driver": (
                'class Config(metaclass=Singleton):\n'
                '    def __init__(self):\n'
                '        print("init")\n'
                '\n'
                '\n'
                'class Other(metaclass=Singleton):\n'
                '    pass\n'
                '\n'
                '\n'
                'a = Config()\n'
                'b = Config()\n'
                'print(a is b)\n'
                'print(Other() is Other(), Other() is a)\n'
            ),
            "expected": ['init', 'True', 'True False'],
            "hint": (
                'Храните словарь экземпляров в метаклассе; __call__(cls, *args, **kwargs): если cls нет в словаре — создайте через super().__call__.'
            ),
        },
        {
            "id": "mc-commands",
            "mode": "stdout",
            "title": "Метакласс собирает команды",
            "statement": (
                'Напишите метакласс CommandMeta: при создании класса он собирает функции с префиксом cmd_ в словарь commands (ключ — имя без префикса) и кладёт его в класс. Остальные атрибуты остаются как есть.'
            ),
            "starter": (
                'class CommandMeta(type):\n'
                '    pass\n'
            ),
            "driver": (
                'class Bot(metaclass=CommandMeta):\n'
                '    def cmd_hi(self):\n'
                '        return "привет"\n'
                '\n'
                '    def cmd_bye(self):\n'
                '        return "пока"\n'
                '\n'
                '    def helper(self):\n'
                '        return "служебная"\n'
                '\n'
                '\n'
                'print(sorted(Bot.commands))\n'
                'b = Bot()\n'
                'print(Bot.commands["hi"](b), b.helper())\n'
                'print(Bot.commands == {k[4:]: v for k, v in vars(Bot).items() if k.startswith("cmd_")})\n'
            ),
            "expected": ["['bye', 'hi']", 'привет служебная', 'True'],
            "hint": (
                'В __new__: ns["commands"] = {k[4:]: v for k, v in ns.items() if k.startswith("cmd_") and callable(v)}; return super().__new__(mcs, name, bases, ns).'
            ),
        },
        {
            "id": "mc-final",
            "mode": "stdout",
            "title": "Запрет наследования",
            "statement": (
                'Напишите метакласс FinalMeta: если у какого-либо родителя нового класса есть атрибут __final__ со значением True, создание класса должно завершаться TypeError (наследовать такой класс нельзя).'
            ),
            "starter": (
                'class FinalMeta(type):\n'
                '    pass\n'
            ),
            "driver": (
                'class A(metaclass=FinalMeta):\n'
                '    __final__ = True\n'
                '\n'
                '\n'
                'try:\n'
                '    class B(A):\n'
                '        pass\n'
                'except TypeError:\n'
                '    print("наследовать нельзя")\n'
                '\n'
                '\n'
                'class C(metaclass=FinalMeta):\n'
                '    pass\n'
                '\n'
                '\n'
                'class D(C):\n'
                '    pass\n'
                '\n'
                '\n'
                'print(D.__mro__[1].__name__, A.__final__)\n'
            ),
            "expected": ['наследовать нельзя', 'C True'],
            "hint": (
                'В __new__: if any(getattr(base, "__final__", False) for base in bases): raise TypeError(...).'
            ),
        },
        {
            "id": "mc-class-getitem",
            "mode": "stdout",
            "title": "Box[int] как обобщённый тип",
            "statement": (
                'Научите класс Box поддерживать запись Box[int] (и Box[str, int]): метод __class_getitem__ возвращает types.GenericAlias с исходным классом и аргументами.'
            ),
            "starter": (
                'import types\n'
                '\n'
                '\n'
                'class Box:\n'
                '    pass\n'
            ),
            "driver": (
                'alias = Box[int]\n'
                'print(alias.__origin__ is Box, alias.__args__[0].__name__)\n'
                'print([t.__name__ for t in Box[str, int].__args__])\n'
                'print(Box() is not None)\n'
            ),
            "expected": ['True int', "['str', 'int']", 'True'],
            "hint": "def __class_getitem__(cls, item): return types.GenericAlias(cls, item).",
        },
        {
            "id": "mc-prepare-nodup",
            "mode": "stdout",
            "title": "Запрет повторных имён в теле класса",
            "statement": (
                'Напишите метакласс NoDupMeta: с помощью __prepare__ он подставляет собственное пространство имён (подкласс dict), которое поднимает TypeError, если имя (кроме специальных, начинающихся с двух подчёркиваний) определено в теле класса дважды. Класс должен создаваться обычным образом.'
            ),
            "starter": (
                'class NoDupMeta(type):\n'
                '    pass\n'
            ),
            "driver": (
                'class Ok(metaclass=NoDupMeta):\n'
                '    def a(self):\n'
                '        return 1\n'
                '\n'
                '    def b(self):\n'
                '        return 2\n'
                '\n'
                '\n'
                'print(Ok().a(), Ok().b())\n'
                'try:\n'
                '    class Bad(metaclass=NoDupMeta):\n'
                '        def a(self):\n'
                '            return 1\n'
                '\n'
                '        def a(self):\n'
                '            return 2\n'
                '    print("ошибки нет")\n'
                'except TypeError:\n'
                '    print("TypeError")\n'
            ),
            "expected": ['1 2', 'TypeError'],
            "hint": (
                '__prepare__ — метод класса метакласса: верните экземпляр dict-наследника с __setitem__; в __new__ передайте dict(ns) в super().__new__.'
            ),
        },
        {
            "id": "mc-counted",
            "mode": "stdout",
            "title": "Учёт экземпляров по классам",
            "statement": (
                'Напишите метакласс Counted: у каждого класса с этим метаклассом (и у каждого потомка отдельно) есть атрибут instances — сколько экземпляров создано именно этим классом.'
            ),
            "starter": (
                'class Counted(type):\n'
                '    pass\n'
            ),
            "driver": (
                'class A(metaclass=Counted):\n'
                '    pass\n'
                '\n'
                '\n'
                'class B(A):\n'
                '    pass\n'
                '\n'
                '\n'
                'A()\n'
                'A()\n'
                'B()\n'
                'print(A.instances, B.instances)\n'
            ),
            "expected": ['2 1'],
            "hint": (
                'В __init__ метакласса: cls.instances = 0; в __call__: cls.instances += 1; return super().__call__(*args, **kwargs).'
            ),
        },
    ],
    32: [
        {
            "id": "ast-calc",
            "mode": "stdout",
            "title": "Безопасный калькулятор",
            "statement": (
                'Напишите calc(expr): разберите строку через ast.parse(expr, mode="eval") и вычислите её рекурсивно, допуская только числа (int, float), унарные + и −, бинарные + − * / // % **. Всё остальное (вызовы, имена, строки) — ValueError. Таблицы OPS и UNARY уже есть.'
            ),
            "starter": (
                'import ast\n'
                'import operator\n'
                '\n'
                'OPS = {\n'
                '    ast.Add: operator.add,\n'
                '    ast.Sub: operator.sub,\n'
                '    ast.Mult: operator.mul,\n'
                '    ast.Div: operator.truediv,\n'
                '    ast.FloorDiv: operator.floordiv,\n'
                '    ast.Mod: operator.mod,\n'
                '    ast.Pow: operator.pow,\n'
                '}\n'
                'UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos}\n'
                '\n'
                '\n'
                'def calc(expr):\n'
                '    pass\n'
            ),
            "driver": (
                'print(calc("2 + 3 * 4"))\n'
                'print(calc("-(2 + 3) ** 2"))\n'
                'print(calc("10 / 4"), calc("7 // 2"))\n'
                'for bad in ["__import__(\'os\')", "abs(-1)", "x + 1", "\'a\' * 3"]:\n'
                '    try:\n'
                '        calc(bad)\n'
                '    except ValueError:\n'
                '        print("ValueError")\n'
            ),
            "expected": ['14', '-25', '2.5 3', 'ValueError', 'ValueError', 'ValueError', 'ValueError'],
            "hint": (
                'Рекурсивная функция по узлам: Constant → значение, BinOp → OPS[type(node.op)](...), UnaryOp → UNARY[...](...), иначе raise ValueError.'
            ),
        },
        {
            "id": "ast-literal-config",
            "mode": "stdout",
            "title": "Настройки только из литералов",
            "statement": (
                'Напишите parse_config(text): превратите строку в значение функцией ast.literal_eval. Если в строке не литерал (вызов, выражение) или синтаксическая ошибка — поднимайте ValueError("некорректная настройка").'
            ),
            "starter": (
                'import ast\n'
                '\n'
                '\n'
                'def parse_config(text):\n'
                '    pass\n'
            ),
            "driver": (
                'print(parse_config("{\'a\': [1, 2], \'b\': (3, 4.5), \'c\': None}"))\n'
                'for bad in ["__import__(\'os\')", "{\'a\': 1+}", "[x for x in range(3)]"]:\n'
                '    try:\n'
                '        parse_config(bad)\n'
                '    except ValueError as e:\n'
                '        print("ValueError", e)\n'
            ),
            "expected": ["{'a': [1, 2], 'b': (3, 4.5), 'c': None}", 'ValueError некорректная настройка', 'ValueError некорректная настройка', 'ValueError некорректная настройка'],
            "hint": (
                'try: return ast.literal_eval(text) except (ValueError, SyntaxError): raise ValueError("некорректная настройка").'
            ),
        },
        {
            "id": "ast-called-names",
            "mode": "stdout",
            "title": "Какие функции вызывает код",
            "statement": (
                'Напишите called_names(source): отсортированный список имён функций, вызываемых по простому имени (print(...), foo(...)). Вызовы методов вида obj.method() не учитывайте. Используйте ast.NodeVisitor и не забывайте обходить вложенные вызовы.'
            ),
            "starter": (
                'import ast\n'
                '\n'
                '\n'
                'def called_names(source):\n'
                '    pass\n'
            ),
            "driver": (
                'src = "print(len(x))\\nresult = foo(bar(1), baz.qux())\\nobj.method()\\n"\n'
                'print(called_names(src))\n'
                'print(called_names("x = 1"))\n'
            ),
            "expected": ["['bar', 'foo', 'len', 'print']", '[]'],
            "hint": (
                'В visit_Call: if isinstance(node.func, ast.Name): names.add(node.func.id); затем self.generic_visit(node).'
            ),
        },
        {
            "id": "ast-count-functions",
            "mode": "stdout",
            "title": "Сколько функций определено",
            "statement": (
                'Напишите count_functions(source): число определений функций и методов (def и async def, включая вложенные); lambda не считаются.'
            ),
            "starter": (
                'import ast\n'
                '\n'
                '\n'
                'def count_functions(source):\n'
                '    pass\n'
            ),
            "driver": (
                "src = '''\n"
                'def a(): pass\n'
                'class K:\n'
                '    def m(self):\n'
                '        def inner(): pass\n'
                '    async def n(self): pass\n'
                'f = lambda x: x\n'
                "'''\n"
                'print(count_functions(src))\n'
                'print(count_functions("x = 1"))\n'
            ),
            "expected": ['4', '0'],
            "hint": "sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree)).",
        },
        {
            "id": "ast-imports",
            "mode": "stdout",
            "title": "Какие модули импортирует код",
            "statement": (
                'Напишите imported_modules(source): отсортированный список имён модулей верхнего уровня, которые импортирует исходник (import a.b → a, from c.d import e → c). Относительные импорты (from . import x) пропускайте.'
            ),
            "starter": (
                'import ast\n'
                '\n'
                '\n'
                'def imported_modules(source):\n'
                '    pass\n'
            ),
            "driver": (
                'src = "import os.path\\nimport sys as s, json\\nfrom collections.abc import Mapping\\nfrom . import local\\nfrom .pkg import y\\n"\n'
                'print(imported_modules(src))\n'
                'print(imported_modules("x = 1"))\n'
            ),
            "expected": ["['collections', 'json', 'os', 'sys']", '[]'],
            "hint": (
                "ast.Import: node.names[i].name.split('.')[0]; ast.ImportFrom: если node.level == 0 — node.module.split('.')[0]."
            ),
        },
        {
            "id": "ast-rename-var",
            "mode": "stdout",
            "title": "Переименование переменной",
            "statement": (
                'Напишите rename_var(source, old, new): с помощью ast.NodeTransformer переименуйте все обращения к имени old (узлы Name и параметры функций arg) и верните текст через ast.unparse.'
            ),
            "starter": (
                'import ast\n'
                '\n'
                '\n'
                'def rename_var(source, old, new):\n'
                '    pass\n'
            ),
            "driver": (
                'print(rename_var("x = 1\\ny = x + 2\\nprint(y)", "x", "t"))\n'
                'print(rename_var("def f(x):\\n    return x * 2", "x", "n"))\n'
            ),
            "expected": ['t = 1', 'y = t + 2', 'print(y)', 'def f(n):', '    return n * 2'],
            "hint": (
                'visit_Name: if node.id == old: node.id = new; return node. Для параметров — visit_arg: node.arg.'
            ),
        },
        {
            "id": "ast-fold-constants",
            "mode": "stdout",
            "title": "Вычисление констант заранее",
            "statement": (
                'Напишите fold_constants(source): NodeTransformer заменяет бинарные операции +, − и * над двумя числовыми константами на одну константу — в том числе вложенные. Результат верните через ast.unparse.'
            ),
            "starter": (
                'import ast\n'
                '\n'
                '\n'
                'def fold_constants(source):\n'
                '    pass\n'
            ),
            "driver": (
                'print(fold_constants("a = 2 * 3 + b"))\n'
                'print(fold_constants("x = (1 + 2) * (3 + 4)"))\n'
                'print(fold_constants("y = n * 2 + 3 * 4"))\n'
                'print(fold_constants("z = a + b"))\n'
            ),
            "expected": ['a = 6 + b', 'x = 21', 'y = n * 2 + 12', 'z = a + b'],
            "hint": (
                'В visit_BinOp сначала self.generic_visit(node); если left и right — ast.Constant, а op — Add/Sub/Mult, вычислите и верните ast.Constant(value).'
            ),
        },
        {
            "id": "ast-exec-namespace",
            "mode": "stdout",
            "title": "exec в собственном пространстве имён",
            "statement": (
                'Напишите build(source, name): выполните исходник через exec в новом пустом словаре и верните из него объект с именем name. Глобальные имена вашей программы при этом не должны меняться; если имени нет — KeyError.'
            ),
            "starter": (
                'def build(source, name):\n'
                '    pass\n'
            ),
            "driver": (
                'fn = build("def add(a, b):\\n    return a + b\\n", "add")\n'
                'print(fn(2, 3))\n'
                'print("add" in globals())\n'
                'print(fn.__globals__ is globals())\n'
                'try:\n'
                '    build("x = 1", "nothing")\n'
                'except KeyError:\n'
                '    print("KeyError")\n'
            ),
            "expected": ['5', 'False', 'False', 'KeyError'],
            "hint": "ns = {}; exec(source, ns); return ns[name].",
        },
        {
            "id": "ast-dis-count",
            "mode": "stdout",
            "title": "Вызовы и циклы в байт-коде",
            "statement": (
                'Напишите count_calls(func) — число команд вызова (CALL, CALL_KW, CALL_FUNCTION_EX) в байт-коде функции — и has_loop(func), которая сообщает, есть ли команда FOR_ITER. Используйте dis.get_instructions.'
            ),
            "starter": (
                'import dis\n'
                '\n'
                '\n'
                'def count_calls(func):\n'
                '    pass\n'
                '\n'
                '\n'
                'def has_loop(func):\n'
                '    pass\n'
            ),
            "driver": (
                'def f(x):\n'
                '    return len(x) + abs(x[0])\n'
                '\n'
                '\n'
                'def g():\n'
                '    return 42\n'
                '\n'
                '\n'
                'def h(a):\n'
                '    return sorted(a, key=len)\n'
                '\n'
                '\n'
                'def loop(xs):\n'
                '    for x in xs:\n'
                '        print(x)\n'
                '\n'
                '\n'
                'print(count_calls(f), count_calls(g), count_calls(h), count_calls(loop))\n'
                'print(has_loop(f), has_loop(loop))\n'
            ),
            "expected": ['2 0 1 1', 'False True'],
            "hint": (
                'ops = [i.opname for i in dis.get_instructions(func)]; считайте элементы из набора {"CALL", "CALL_KW", "CALL_FUNCTION_EX"}.'
            ),
        },
    ],
}
