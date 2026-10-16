"""Задачи «Python как первый язык»: проекты и инструменты (главы 50–51) — пакеты, окружения, uv, качество кода и шаблоны.

Ключ — номер главы. Режим stdout со скрытым driver.
"""

TASKS: dict[int, list[dict]] = {
    50: [
        {
            "id": "pj-parse-requirement",
            "mode": "stdout",
            "title": "Разбор строки зависимости",
            "statement": (
                'Напишите parse_requirement(text): из строки вида «requests>=2.31,<3» верните кортеж (имя, список пар (оператор, версия)). Пробелы вокруг частей игнорируйте, «extras» в квадратных скобках отбрасывайте. Операторы: ==, !=, <=, >=, ~=, <, >. Строку, которую нельзя разобрать, отвергайте ValueError.'
            ),
            "starter": (
                'import re\n'
                '\n'
                '\n'
                'def parse_requirement(text):\n'
                '    pass\n'
            ),
            "driver": (
                'print(parse_requirement("requests>=2.31,<3"))\n'
                'print(parse_requirement("flask"))\n'
                'print(parse_requirement("  httpx[http2] ~= 0.27.2 "))\n'
                'print(parse_requirement("pkg == 1.0 , != 1.0.1"))\n'
                'for bad in ("bad name!", "", ">=1.0"):\n'
                '    try:\n'
                '        parse_requirement(bad)\n'
                '    except ValueError:\n'
                '        print("ValueError")\n'
            ),
            "expected": ["('requests', [('>=', '2.31'), ('<', '3')])", "('flask', [])", "('httpx', [('~=', '0.27.2')])", "('pkg', [('==', '1.0'), ('!=', '1.0.1')])", 'ValueError', 'ValueError', 'ValueError'],
            "hint": (
                'Регулярка для имени ^([A-Za-z0-9._-]+)(?:\\[[^\\]]*\\])?(.*)$, остаток разбейте по запятым и разберите оператор и версию.'
            ),
        },
        {
            "id": "pj-compare-versions",
            "mode": "stdout",
            "title": "Сравнение версий",
            "statement": (
                'Напишите compare_versions(a, b): -1, 0 или 1 для версий вида «1.10.2». Сравнивайте по числам, а не по строкам («1.10» новее «1.2»), недостающие части считайте нулями («1.0» равно «1.0.0»).'
            ),
            "starter": (
                'def compare_versions(a, b):\n'
                '    pass\n'
            ),
            "driver": (
                'import functools\n'
                '\n'
                'print(compare_versions("1.10", "1.2"), compare_versions("1.0", "1.0.0"), compare_versions("2.0.1", "2.1"))\n'
                'vs = ["1.10", "1.2", "1.9.5", "1.2.1", "0.9"]\n'
                'print(sorted(vs, key=functools.cmp_to_key(compare_versions)))\n'
                'print(sorted(vs))\n'
            ),
            "expected": ['1 0 -1', "['0.9', '1.2', '1.2.1', '1.9.5', '1.10']", "['0.9', '1.10', '1.2', '1.2.1', '1.9.5']"],
            "hint": "Разбейте по точкам в списки int, дополните нулями до одной длины и сравните списки.",
        },
        {
            "id": "pj-satisfies",
            "mode": "stdout",
            "title": "Подходит ли версия под условие",
            "statement": (
                'Функция compare_versions уже есть. Напишите satisfies(version, spec): spec — несколько условий через запятую (>=, >, <=, <, ==, !=, ~=). Совместимый выпуск ~=1.4.2 значит «>=1.4.2 и версия начинается с 1.4», а ~=1.4 — «>=1.4 и начинается с 1».'
            ),
            "starter": (
                'def compare_versions(a, b):\n'
                '    pa = [int(x) for x in a.split(".")]\n'
                '    pb = [int(x) for x in b.split(".")]\n'
                '    n = max(len(pa), len(pb))\n'
                '    pa += [0] * (n - len(pa))\n'
                '    pb += [0] * (n - len(pb))\n'
                '    return (pa > pb) - (pa < pb)\n'
                '\n'
                '\n'
                'def satisfies(version, spec):\n'
                '    pass\n'
            ),
            "driver": (
                'print(satisfies("1.5", ">=1.2,<2"), satisfies("2.0", ">=1.2,<2"), satisfies("1.0", ">1.0"))\n'
                'print(satisfies("1.4.9", "~=1.4.2"), satisfies("1.5.0", "~=1.4.2"), satisfies("1.4.1", "~=1.4.2"))\n'
                'print(satisfies("1.9", "~=1.4"), satisfies("2.0", "~=1.4"))\n'
                'print(satisfies("1.0.0", "==1.0"), satisfies("1.2", "!=1.2"))\n'
            ),
            "expected": ['True False False', 'True False False', 'True False', 'True False'],
            "hint": (
                'Для ~=: нижняя граница >= spec и совпадение всех частей версии, кроме последней части spec.'
            ),
        },
        {
            "id": "pj-read-pyproject",
            "mode": "stdout",
            "title": "Чтение pyproject.toml",
            "statement": (
                'Напишите project_info(text): разберите TOML модулем tomllib и верните кортеж (имя, версия, требуемый Python, список зависимостей) из раздела [project]. Если какого-то поля нет — подставляйте None (для зависимостей — пустой список).'
            ),
            "starter": (
                'import tomllib\n'
                '\n'
                '\n'
                'def project_info(text):\n'
                '    pass\n'
            ),
            "driver": (
                "text = '''\n"
                '[project]\n'
                'name = "shop"\n'
                'version = "0.3.0"\n'
                'requires-python = ">=3.12"\n'
                'dependencies = ["httpx>=0.27", "rich"]\n'
                '\n'
                '[tool.ruff]\n'
                'line-length = 100\n'
                "'''\n"
                'print(project_info(text))\n'
                'print(project_info("[project]\\nname = \'x\'"))\n'
                'print(project_info(""))\n'
            ),
            "expected": ["('shop', '0.3.0', '>=3.12', ['httpx>=0.27', 'rich'])", "('x', None, None, [])", '(None, None, None, [])'],
            "hint": 'data = tomllib.loads(text).get("project", {}); data.get("name") и так далее.',
        },
        {
            "id": "pj-entry-point",
            "mode": "stdout",
            "title": "Точка входа",
            "statement": (
                'Напишите resolve_entry_point(spec): строка вида «пакет.модуль:функция» (как в [project.scripts]) превращается в вызываемый объект; допускается вложенное имя через точку после двоеточия. Формат без двоеточия — ValueError; несуществующий модуль — ImportError, несуществующее имя — AttributeError.'
            ),
            "starter": (
                'import importlib\n'
                '\n'
                '\n'
                'def resolve_entry_point(spec):\n'
                '    pass\n'
            ),
            "driver": (
                'print(resolve_entry_point("json:dumps")({"a": 1}))\n'
                'print(resolve_entry_point("os.path:join")("a", "b"))\n'
                'print(resolve_entry_point("collections:OrderedDict.fromkeys")("ab"))\n'
                'for bad, exc in (("json", ValueError), ("nomod_zz:f", ImportError), ("json:zzz", AttributeError)):\n'
                '    try:\n'
                '        resolve_entry_point(bad)\n'
                '    except exc:\n'
                '        print(exc.__name__)\n'
            ),
            "expected": ['{"a": 1}', 'a/b', "OrderedDict({'a': None, 'b': None})", 'ValueError', 'ImportError', 'AttributeError'],
            "hint": (
                'module, sep, attr = spec.partition(":"); если нет sep — ValueError; затем import_module и getattr по частям attr.split(".").'
            ),
        },
        {
            "id": "pj-find-packages",
            "mode": "stdout",
            "title": "Поиск пакетов в каталоге",
            "statement": (
                'Напишите find_packages(root): отсортированный список полных имён пакетов в каталоге root — каталогов с __init__.py. Вглубь заходите только внутрь пакетов (если родитель не пакет, вложенные не считаются).'
            ),
            "starter": (
                'import os\n'
                '\n'
                '\n'
                'def find_packages(root):\n'
                '    pass\n'
            ),
            "driver": (
                'import pathlib\n'
                'import tempfile\n'
                '\n'
                'with tempfile.TemporaryDirectory() as tmp:\n'
                '    base = pathlib.Path(tmp)\n'
                '    for rel in ["shop/__init__.py", "shop/utils/__init__.py", "shop/data/readme.txt", "tests/test_a.py", "other/__init__.py", "shop/data/sub/__init__.py", "shop/utils/deep/__init__.py"]:\n'
                '        f = base / rel\n'
                '        f.parent.mkdir(parents=True, exist_ok=True)\n'
                '        f.write_text("")\n'
                '    print(find_packages(str(base)))\n'
                '    print(find_packages(str(base / "tests")))\n'
            ),
            "expected": ["['other', 'shop', 'shop.utils', 'shop.utils.deep']", '[]'],
            "hint": (
                'Рекурсивная функция: для каждого подкаталога с __init__.py добавьте имя и спуститесь внутрь с префиксом.'
            ),
        },
        {
            "id": "pj-cli-main",
            "mode": "stdout",
            "title": "Командная строка проекта",
            "statement": (
                'Напишите main(argv=None): argparse с обязательным --name, необязательным --times (целое, по умолчанию 1) и флагом --shout. Печатает приветствие «Здравствуйте, <name>!» нужное число раз (с --shout — в верхнем регистре) и возвращает 0. Ошибка аргументов — обычное поведение argparse (SystemExit с кодом 2).'
            ),
            "starter": (
                'import argparse\n'
                '\n'
                '\n'
                'def main(argv=None):\n'
                '    pass\n'
            ),
            "driver": (
                'print(main(["--name", "Аня"]))\n'
                'print(main(["--name", "Борис", "--times", "2", "--shout"]))\n'
                'import contextlib, io\n'
                'buf = io.StringIO()\n'
                'with contextlib.redirect_stderr(buf):\n'
                '    try:\n'
                '        main(["--times", "x"])\n'
                '    except SystemExit as e:\n'
                '        print("SystemExit", e.code)\n'
            ),
            "expected": ['Здравствуйте, Аня!', '0', 'ЗДРАВСТВУЙТЕ, БОРИС!', 'ЗДРАВСТВУЙТЕ, БОРИС!', '0', 'SystemExit 2'],
            "hint": (
                'parser = argparse.ArgumentParser(); parser.add_argument("--name", required=True); --times type=int default=1; --shout action="store_true".'
            ),
        },
        {
            "id": "pj-lock-diff",
            "mode": "stdout",
            "title": "Что изменилось в блокировке",
            "statement": (
                'Напишите lock_diff(old, new): old и new — словари «пакет → версия». Верните кортеж из трёх отсортированных списков строк: добавленные («+ имя версия»), удалённые («- имя версия») и обновлённые («~ имя старая → новая»).'
            ),
            "starter": (
                'def lock_diff(old, new):\n'
                '    pass\n'
            ),
            "driver": (
                'old = {"httpx": "0.27.0", "anyio": "4.3.0", "idna": "3.6"}\n'
                'new = {"httpx": "0.27.2", "anyio": "4.3.0", "certifi": "2024.8"}\n'
                'added, removed, changed = lock_diff(old, new)\n'
                'print(added)\n'
                'print(removed)\n'
                'print(changed)\n'
                'print(lock_diff({}, {}))\n'
            ),
            "expected": ["['+ certifi 2024.8']", "['- idna 3.6']", "['~ httpx 0.27.0 → 0.27.2']", '([], [], [])'],
            "hint": (
                'Сравнивайте множества ключей: new - old, old - new и пересечение с различающимися значениями.'
            ),
        },
        {
            "id": "pj-env-settings",
            "mode": "stdout",
            "title": "Настройки из окружения",
            "statement": (
                'Напишите load_settings(environ): словарь настроек из переменных окружения (environ — обычный словарь): DEBUG («1», «true», «yes» без учёта регистра — True, иначе False), PORT (целое, по умолчанию 8000; не число или вне 1..65535 — ValueError), HOSTS (список из значения через запятую без пробелов по краям, по умолчанию ["localhost"]).'
            ),
            "starter": (
                'def load_settings(environ):\n'
                '    pass\n'
            ),
            "driver": (
                'print(load_settings({}))\n'
                'print(load_settings({"DEBUG": "TRUE", "PORT": "8080", "HOSTS": "a.com, b.com ,c.com"}))\n'
                'for bad in ({"PORT": "x"}, {"PORT": "70000"}, {"PORT": "0"}):\n'
                '    try:\n'
                '        load_settings(bad)\n'
                '    except ValueError:\n'
                '        print("ValueError")\n'
                'print(load_settings({"DEBUG": "0", "HOSTS": ""}))\n'
            ),
            "expected": ["{'debug': False, 'port': 8000, 'hosts': ['localhost']}", "{'debug': True, 'port': 8080, 'hosts': ['a.com', 'b.com', 'c.com']}", 'ValueError', 'ValueError', 'ValueError', "{'debug': False, 'port': 8000, 'hosts': ['localhost']}"],
            "hint": "Пустой HOSTS считайте отсутствующим; PORT проверьте int(...) и диапазон.",
        },
    ],
    51: [
        {
            "id": "qa-doctest",
            "mode": "stdout",
            "title": "Функция с проверяемыми примерами",
            "statement": (
                'Напишите fizzbuzz(n): для n, кратного 15, «FizzBuzz»; кратного 3 — «Fizz»; кратного 5 — «Buzz»; иначе число в виде строки. В строке документации приведите не меньше четырёх примеров в формате doctest (>>> …), и все они должны проходить.'
            ),
            "starter": (
                'def fizzbuzz(n):\n'
                '    pass\n'
            ),
            "driver": (
                'import doctest\n'
                '\n'
                'finder = doctest.DocTestFinder()\n'
                'runner = doctest.DocTestRunner(verbose=False)\n'
                'examples = 0\n'
                'for test in finder.find(fizzbuzz, "fizzbuzz", globs={"fizzbuzz": fizzbuzz}):\n'
                '    examples += len(test.examples)\n'
                '    runner.run(test)\n'
                'print(runner.failures == 0, examples >= 4)\n'
                'print(fizzbuzz(15), fizzbuzz(9), fizzbuzz(10), fizzbuzz(7))\n'
            ),
            "expected": ['True True', 'FizzBuzz Fizz Buzz 7'],
            "hint": (
                "В docstring: >>> fizzbuzz(15), следующей строкой — 'FizzBuzz' (с кавычками, как repr строки)."
            ),
        },
        {
            "id": "qa-table-cases",
            "mode": "stdout",
            "title": "Табличные тесты",
            "statement": (
                'Напишите run_cases(func, cases): cases — список пар (аргументы, ожидаемое) (аргументы — кортеж). Верните список описаний провалов в порядке случаев: «func(аргументы): ожидали X, получили Y»; если функция упала с исключением — «func(аргументы): исключение ИмяТипа». Успешные случаи пропускайте.'
            ),
            "starter": (
                'def run_cases(func, cases):\n'
                '    pass\n'
            ),
            "driver": (
                'def half(x):\n'
                '    return x // 2\n'
                '\n'
                '\n'
                'cases = [((4,), 2), ((5,), 2), ((7,), 4), (("a",), 1)]\n'
                'for line in run_cases(half, cases):\n'
                '    print(line)\n'
                'print(run_cases(half, [((2,), 1)]))\n'
            ),
            "expected": ['half((7,)): ожидали 4, получили 3', "half(('a',)): исключение TypeError", '[]'],
            "hint": (
                'for args, want in cases: try: got = func(*args) except Exception as e: ...; if got != want: ...'
            ),
        },
        {
            "id": "qa-mock",
            "mode": "stdout",
            "title": "Тест с Mock",
            "statement": (
                'Функция greet(user_id, fetch) возвращает «Привет, <имя>», где имя получено вызовом fetch(user_id). Напишите check_greet(): создайте Mock (unittest.mock) с return_value="Аня", вызовите greet(7, mock), проверьте результат и что mock вызван ровно один раз с аргументом 7; верните True, если всё верно, и False иначе.'
            ),
            "starter": (
                'from unittest.mock import Mock\n'
                '\n'
                '\n'
                'def greet(user_id, fetch):\n'
                '    return f"Привет, {fetch(user_id)}"\n'
                '\n'
                '\n'
                'def check_greet():\n'
                '    pass\n'
            ),
            "driver": "print(check_greet())\n",
            "expected": ['True'],
            "hint": (
                'fetch = Mock(return_value="Аня"); text = greet(7, fetch); fetch.assert_called_once_with(7) внутри try/except AssertionError.'
            ),
        },
        {
            "id": "qa-logging",
            "mode": "stdout",
            "title": "Настройка журнала",
            "statement": (
                'Напишите setup_logger(stream): логгер с именем «app», уровнем INFO, одним обработчиком, пишущим в stream в формате «УРОВЕНЬ:сообщение» (%(levelname)s:%(message)s). Повторный вызов не должен добавлять второй обработчик. Распространение записей родительским логгерам отключите.'
            ),
            "starter": (
                'import logging\n'
                '\n'
                '\n'
                'def setup_logger(stream):\n'
                '    pass\n'
            ),
            "driver": (
                'import io\n'
                '\n'
                'buf = io.StringIO()\n'
                'log = setup_logger(buf)\n'
                'log = setup_logger(buf)\n'
                'log.debug("скрыто")\n'
                'log.info("заказ %s создан", 7)\n'
                'log.warning("медленно")\n'
                'print(buf.getvalue(), end="")\n'
                'print(len(log.handlers), log.name, log.propagate)\n'
            ),
            "expected": ['INFO:заказ 7 создан', 'WARNING:медленно', '1 app False'],
            "hint": (
                'logger = logging.getLogger("app"); если нет обработчиков — StreamHandler(stream) с Formatter; level INFO; propagate = False.'
            ),
        },
        {
            "id": "qa-exceptions",
            "mode": "stdout",
            "title": "Иерархия исключений приложения",
            "statement": (
                'Создайте исключения: AppError(Exception), NotFound(AppError) и ValidationError(AppError). NotFound принимает имя сущности и ключ и формирует сообщение «<имя> не найден: <ключ>»; ValidationError хранит поле (атрибут field) и сообщение. Напишите find_user(users, user_id): возвращает пользователя из словаря или поднимает NotFound("user", user_id).'
            ),
            "starter": (
                'class AppError(Exception):\n'
                '    pass\n'
            ),
            "driver": (
                'users = {1: "Аня"}\n'
                'print(find_user(users, 1))\n'
                'try:\n'
                '    find_user(users, 2)\n'
                'except AppError as e:\n'
                '    print(type(e).__name__, e)\n'
                'err = ValidationError("age", "должен быть числом")\n'
                'print(err.field, err, isinstance(err, AppError), issubclass(NotFound, ValidationError))\n'
            ),
            "expected": ['Аня', 'NotFound user не найден: 2', 'age age: должен быть числом True False'],
            "hint": (
                'NotFound.__init__(self, entity, key): super().__init__(f"{entity} не найден: {key}"); у ValidationError — сообщение f"{field}: {message}" и self.field.'
            ),
        },
        {
            "id": "qa-strategy",
            "mode": "stdout",
            "title": "Скидки как стратегии",
            "statement": (
                'Напишите make_discount(spec): по строке возвращает функцию цены. «none» — без скидки; «percent:10» — скидка 10% (результат округляйте до копеек, round(…, 2)); «fixed:5» — минус 5, но не ниже нуля. Неизвестная схема — ValueError.'
            ),
            "starter": (
                'def make_discount(spec):\n'
                '    pass\n'
            ),
            "driver": (
                'for spec in ("none", "percent:10", "fixed:5"):\n'
                '    f = make_discount(spec)\n'
                '    print(spec, f(100), f(3))\n'
                'try:\n'
                '    make_discount("coupon:7")\n'
                'except ValueError:\n'
                '    print("ValueError")\n'
            ),
            "expected": ['none 100 3', 'percent:10 90.0 2.7', 'fixed:5 95 0', 'ValueError'],
            "hint": (
                'kind, _, arg = spec.partition(":"); для каждого kind верните свою функцию (замыкание над числом).'
            ),
        },
        {
            "id": "qa-observer",
            "mode": "stdout",
            "title": "Шина событий",
            "statement": (
                'Напишите EventBus: subscribe(event, handler), unsubscribe(event, handler) и emit(event, *args) — вызывает обработчики события в порядке подписки и возвращает их число. Отписка от неподписанного обработчика не должна падать. Подписка одной и той же функции дважды вызывает её дважды.'
            ),
            "starter": (
                'class EventBus:\n'
                '    pass\n'
            ),
            "driver": (
                'bus = EventBus()\n'
                'log = []\n'
                '\n'
                '\n'
                'def a(x):\n'
                '    log.append(("a", x))\n'
                '\n'
                '\n'
                'def b(x):\n'
                '    log.append(("b", x))\n'
                '\n'
                '\n'
                'bus.subscribe("save", a)\n'
                'bus.subscribe("save", b)\n'
                'bus.subscribe("save", a)\n'
                'print(bus.emit("save", 1), log)\n'
                'bus.unsubscribe("save", a)\n'
                'log.clear()\n'
                'print(bus.emit("save", 2), log)\n'
                'bus.unsubscribe("save", a)\n'
                'bus.unsubscribe("x", a)\n'
                'print(bus.emit("none", 0))\n'
            ),
            "expected": ["3 [('a', 1), ('b', 1), ('a', 1)]", "2 [('b', 2), ('a', 2)]", '0'],
            "hint": (
                'словарь событие → список обработчиков; в unsubscribe удаляйте первое вхождение (list.remove) с try/except ValueError.'
            ),
        },
        {
            "id": "qa-idioms",
            "mode": "stdout",
            "title": "Перепишите по-питоновски",
            "statement": (
                'Функция pairs_report(names, scores) работает верно, но написана с индексами (range(len(...)), ручная сборка списка). Перепишите её идиоматично — через zip и включение, без range(len(...)) и без метода append. Результат: строки «<имя>: <балл>» для баллов не ниже 50.'
            ),
            "starter": (
                'def pairs_report(names, scores):\n'
                '    result = []\n'
                '    for i in range(len(names)):\n'
                '        if scores[i] >= 50:\n'
                '            result.append(names[i] + ": " + str(scores[i]))\n'
                '    return result\n'
            ),
            "driver": (
                'import ast\n'
                '\n'
                'src = open("/sandbox/solution.py", encoding="utf-8").read()\n'
                'tree = ast.parse(src)\n'
                'bad_range = any(\n'
                '    isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "range"\n'
                '    and n.args and isinstance(n.args[0], ast.Call) and getattr(n.args[0].func, "id", "") == "len"\n'
                '    for n in ast.walk(tree)\n'
                ')\n'
                'bad_append = any(isinstance(n, ast.Attribute) and n.attr == "append" for n in ast.walk(tree))\n'
                'print(pairs_report(["Аня", "Борис", "Вера"], [90, 40, 50]))\n'
                'print(pairs_report([], []))\n'
                'print("range(len)" if bad_range else "без range(len)", "append" if bad_append else "без append")\n'
            ),
            "expected": ["['Аня: 90', 'Вера: 50']", '[]', 'без range(len) без append'],
            "hint": 'return [f"{n}: {s}" for n, s in zip(names, scores) if s >= 50].',
        },
        {
            "id": "qa-property-check",
            "mode": "stdout",
            "title": "Мини-проверка свойств",
            "statement": (
                'Напишите check_property(prop, gen, trials=200, seed=0): создайте random.Random(seed), trials раз вызовите gen(rng) для получения входа и prop(вход); верните первый вход, на котором prop вернул ложь (или упал с исключением), либо None, если контрпримера не нашлось.'
            ),
            "starter": (
                'import random\n'
                '\n'
                '\n'
                'def check_property(prop, gen, trials=200, seed=0):\n'
                '    pass\n'
            ),
            "driver": (
                'def gen_list(rng):\n'
                '    return [rng.randint(-5, 5) for _ in range(rng.randint(0, 6))]\n'
                '\n'
                '\n'
                'def good_sort(xs):\n'
                '    return sorted(xs)\n'
                '\n'
                '\n'
                'def bad_sort(xs):\n'
                '    return sorted(set(xs))\n'
                '\n'
                '\n'
                'def keeps_items(sort):\n'
                '    return lambda xs: sorted(sort(xs)) == sorted(xs)\n'
                '\n'
                '\n'
                'print(check_property(keeps_items(good_sort), gen_list))\n'
                'ce = check_property(keeps_items(bad_sort), gen_list)\n'
                'print(ce is not None and len(ce) != len(set(ce)))\n'
                'print(check_property(lambda xs: 1 / len(xs) > 0, gen_list) == [])\n'
                'print(check_property(keeps_items(bad_sort), gen_list, seed=1) is not None)\n'
            ),
            "expected": ['None', 'True', 'True', 'True'],
            "hint": (
                'rng = random.Random(seed); for _ in range(trials): case = gen(rng); try: ok = prop(case) except Exception: return case; if not ok: return case; в конце return None.'
            ),
        },
    ],
}
