"""Задачи «Python как первый язык»: исключения и файлы (главы 15–17).

Файловые задачи работают во временных папках (tempfile.mkdtemp в драйвере):
в песочнице пишется только /tmp.
"""

TASKS: dict[int, list[dict]] = {
    15: [
        {
            "id": "safe-int",
            "mode": "func",
            "func": "safe_int",
            "title": "Число или запасное значение",
            "statement": (
                "Напишите функцию safe_int(text, default=0): переводит строку "
                "в целое число, а если это не получается — возвращает default. "
                "Используйте try/except ValueError."
            ),
            "starter": "def safe_int(text, default=0):\n    pass\n",
            "tests": [
                {"args": ["42"], "expected": 42},
                {"args": ["abc"], "expected": 0},
                {"args": ["abc", -1], "expected": -1},
                {"args": [""], "expected": 0},
                {"args": [" 7 "], "expected": 7},
            ],
            "hint": "try: return int(text) / except ValueError: return default.",
        },
        {
            "id": "safe-divide",
            "mode": "func",
            "func": "safe_divide",
            "title": "Безопасное деление",
            "statement": (
                "Напишите функцию safe_divide(a, b): a / b, а при делении на "
                "ноль — None."
            ),
            "starter": "def safe_divide(a, b):\n    pass\n",
            "tests": [
                {"args": [6, 3], "expected": 2.0},
                {"args": [1, 0], "expected": None},
                {"args": [0, 5], "expected": 0.0},
                {"args": [-9, 3], "expected": -3.0},
            ],
            "hint": "Поймайте именно ZeroDivisionError, остальное пусть падает.",
        },
        {
            "id": "parse-age",
            "mode": "stdout",
            "title": "Возраст с проверкой",
            "statement": (
                "Напишите функцию parse_age(text): возвращает целый возраст из "
                "строки. Если число отрицательное — поднимите ValueError с "
                "любым сообщением. Нечисловую строку int() отвергнет сам."
            ),
            "starter": "def parse_age(text):\n    pass\n",
            "driver": (
                'print(parse_age("20"))\n'
                'try:\n    parse_age("-5")\nexcept ValueError:\n    print("отрицательный")\n'
                'try:\n    parse_age("abc")\nexcept ValueError:\n    print("не число")\n'
            ),
            "expected": ["20", "отрицательный", "не число"],
            "hint": "age = int(text); if age < 0: raise ValueError(...); return age.",
        },
        {
            "id": "custom-error",
            "mode": "stdout",
            "title": "Своё исключение",
            "statement": (
                "Опишите исключение NotEnoughMoney (наследник Exception) и "
                "функцию withdraw(balance, amount): если amount больше "
                "balance — поднимите NotEnoughMoney с сообщением «не хватает "
                "<сколько>», иначе верните остаток."
            ),
            "starter": "class NotEnoughMoney(Exception):\n    pass\n\n\ndef withdraw(balance, amount):\n    pass\n",
            "driver": (
                "print(withdraw(100, 30))\n"
                "try:\n    withdraw(100, 150)\nexcept NotEnoughMoney as e:\n    print(e)\n"
                "print(issubclass(NotEnoughMoney, Exception))\n"
            ),
            "expected": ["70", "не хватает 50", "True"],
            "hint": 'raise NotEnoughMoney(f"не хватает {amount - balance}").',
        },
        {
            "id": "first-int",
            "mode": "func",
            "func": "first_int",
            "title": "Первое число в списке",
            "statement": (
                "Напишите функцию first_int(items): items — список строк. "
                "Верните первое значение, которое удаётся превратить в целое "
                "число (уже как int), или None, если таких нет."
            ),
            "starter": "def first_int(items):\n    pass\n",
            "tests": [
                {"args": [["а", "б", "12", "7"]], "expected": 12},
                {"args": [["x", "y"]], "expected": None},
                {"args": [[]], "expected": None},
                {"args": [["5"]], "expected": 5},
            ],
            "hint": "В цикле: try: return int(x) / except ValueError: continue; после цикла return None.",
        },
        {
            "id": "finally-log",
            "mode": "stdout",
            "title": "Журнал и finally",
            "statement": (
                "Напишите функцию process(items, log): добавьте в список log "
                "строку «start»; вычислите и верните список 100 / x для "
                "каждого x из items; но если встретится ноль — верните None. "
                "В любом случае, даже при ошибке, в конце добавьте в log "
                "строку «end» (блок finally)."
            ),
            "starter": "def process(items, log):\n    pass\n",
            "driver": (
                "log = []\nprint(process([1, 4], log))\nprint(log)\n"
                "log = []\nprint(process([2, 0], log))\nprint(log)\n"
            ),
            "expected": ["[100.0, 25.0]", "['start', 'end']", "None", "['start', 'end']"],
            "hint": "try: return [100 / x for x in items] / except ZeroDivisionError: return None / finally: log.append('end').",
        },
        {
            "id": "raise-from",
            "mode": "stdout",
            "title": "Понятная ошибка",
            "statement": (
                "Напишите функцию get_port(config): возвращает config[\"port\"], "
                "а если ключа нет — поднимает RuntimeError(\"нет порта\") "
                "ИЗ исходной ошибки (raise ... from e)."
            ),
            "starter": "def get_port(config):\n    pass\n",
            "driver": (
                'print(get_port({"port": 8080}))\n'
                "try:\n    get_port({})\nexcept RuntimeError as e:\n"
                "    print(e, type(e.__cause__).__name__)\n"
            ),
            "expected": ["8080", "нет порта KeyError"],
            "hint": 'try: return config["port"] / except KeyError as e: raise RuntimeError("нет порта") from e.',
        },
        {
            "id": "eafp-get",
            "mode": "func",
            "func": "get_or_default",
            "title": "EAFP вместо get",
            "statement": (
                "Напишите функцию get_or_default(d, key, default): значение "
                "по ключу или default. Метод get и слово in использовать "
                "нельзя — только try/except KeyError."
            ),
            "starter": "def get_or_default(d, key, default):\n    pass\n",
            "tests": [
                {"args": [{"a": 1}, "a", 0], "expected": 1},
                {"args": [{"a": 1}, "b", 0], "expected": 0},
                {"args": [{}, "x", "нет"], "expected": "нет"},
            ],
            "hint": "try: return d[key] / except KeyError: return default.",
        },
    ],
    16: [
        {
            "id": "write-lines",
            "mode": "stdout",
            "title": "Запись строк в файл",
            "statement": (
                "Напишите функцию write_lines(path, lines): записывает каждую "
                "строку списка в файл по своей строке (кодировка utf-8)."
            ),
            "starter": "def write_lines(path, lines):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 'a.txt')\n"
                "write_lines(p, ['привет', 'мир', 'ещё'])\n"
                "print(open(p, encoding='utf-8').read().split('\\n'))\n"
            ),
            "expected": ["['привет', 'мир', 'ещё', '']"],
            "hint": "with open(path, 'w', encoding='utf-8') as f: for line in lines: f.write(line + '\\n').",
        },
        {
            "id": "read-lines",
            "mode": "stdout",
            "title": "Чтение строк",
            "statement": (
                "Напишите функцию read_lines(path): список строк файла без "
                "символов перевода строки."
            ),
            "starter": "def read_lines(path):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 'a.txt')\n"
                "open(p, 'w', encoding='utf-8').write('один\\nдва\\nтри\\n')\n"
                "print(read_lines(p))\n"
            ),
            "expected": ["['один', 'два', 'три']"],
            "hint": "with open(...) as f: return [line.strip() for line in f] — либо read().splitlines().",
        },
        {
            "id": "count-words-file",
            "mode": "stdout",
            "title": "Слова в файле",
            "statement": (
                "Напишите функцию count_words(path): сколько всего слов в "
                "файле (слова разделены пробелами и переводами строк)."
            ),
            "starter": "def count_words(path):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 'a.txt')\n"
                "open(p, 'w', encoding='utf-8').write('раз два\\nтри четыре пять\\n\\nшесть\\n')\n"
                "print(count_words(p))\n"
            ),
            "expected": ["6"],
            "hint": "На каждой строке прибавляйте len(line.split()).",
        },
        {
            "id": "append-log",
            "mode": "stdout",
            "title": "Журнал",
            "statement": (
                "Напишите функцию append_log(path, text): дописывает text и "
                "перевод строки в конец файла, не затирая предыдущее."
            ),
            "starter": "def append_log(path, text):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 'log.txt')\n"
                "append_log(p, 'старт')\nappend_log(p, 'работа')\nappend_log(p, 'финиш')\n"
                "print(open(p, encoding='utf-8').read().splitlines())\n"
            ),
            "expected": ["['старт', 'работа', 'финиш']"],
            "hint": "Режим 'a' дописывает; 'w' затёр бы всё.",
        },
        {
            "id": "word-freq-file",
            "mode": "stdout",
            "title": "Частоты слов в файле",
            "statement": (
                "Напишите функцию word_freq(path): словарь «слово → сколько "
                "раз» для слов файла без учёта регистра (приводите к нижнему)."
            ),
            "starter": "def word_freq(path):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 'a.txt')\n"
                "open(p, 'w', encoding='utf-8').write('Да нет да\\nНЕТ да\\n')\n"
                "print(sorted(word_freq(p).items()))\n"
            ),
            "expected": ["[('да', 3), ('нет', 2)]"],
            "hint": "counts[w] = counts.get(w, 0) + 1 для каждого слова line.lower().split().",
        },
        {
            "id": "safe-read",
            "mode": "stdout",
            "title": "Чтение без падения",
            "statement": (
                "Напишите функцию safe_read(path): текст файла или None, если "
                "файла нет (FileNotFoundError)."
            ),
            "starter": "def safe_read(path):\n    pass\n",
            "driver": (
                "import os, tempfile\nd = tempfile.mkdtemp()\np = os.path.join(d, 'a.txt')\n"
                "open(p, 'w', encoding='utf-8').write('данные')\n"
                "print(safe_read(p))\nprint(safe_read(os.path.join(d, 'нет.txt')))\n"
            ),
            "expected": ["данные", "None"],
            "hint": "try: with open(...) as f: return f.read() / except FileNotFoundError: return None.",
        },
        {
            "id": "copy-upper",
            "mode": "stdout",
            "title": "Копия заглавными",
            "statement": (
                "Напишите функцию copy_upper(src, dst): читает файл src и "
                "записывает в dst те же строки, но заглавными буквами. Оба "
                "файла открывайте одним with."
            ),
            "starter": "def copy_upper(src, dst):\n    pass\n",
            "driver": (
                "import os, tempfile\nd = tempfile.mkdtemp()\n"
                "a, b = os.path.join(d, 'a.txt'), os.path.join(d, 'b.txt')\n"
                "open(a, 'w', encoding='utf-8').write('привет\\nмир\\n')\n"
                "copy_upper(a, b)\nprint(open(b, encoding='utf-8').read().splitlines())\n"
            ),
            "expected": ["['ПРИВЕТ', 'МИР']"],
            "hint": "with open(src, encoding='utf-8') as r, open(dst, 'w', encoding='utf-8') as w: ...",
        },
        {
            "id": "longest-line",
            "mode": "stdout",
            "title": "Самая длинная строка",
            "statement": (
                "Напишите функцию longest_line(path): самая длинная строка "
                "файла без перевода строки (при равной длине — первая). "
                "Файл не пустой."
            ),
            "starter": "def longest_line(path):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 'a.txt')\n"
                "open(p, 'w', encoding='utf-8').write('коротко\\nчуть подлиннее\\nсредне\\nодинаково-ок\\n')\n"
                "print(longest_line(p))\n"
            ),
            "expected": ["чуть подлиннее"],
            "hint": "Идите по строкам и обновляйте лучшую только при строго большей длине.",
        },
    ],
    17: [
        {
            "id": "file-info",
            "mode": "func",
            "func": "file_info",
            "title": "Части пути",
            "statement": (
                "Напишите функцию file_info(path): кортеж (имя файла, имя без "
                "расширения, расширение) для пути-строки. Используйте pathlib. "
                "Диск не нужен."
            ),
            "starter": "from pathlib import Path\n\n\ndef file_info(path):\n    pass\n",
            "tests": [
                {"args": ["data/reports/2024.csv"], "expected": ("2024.csv", "2024", ".csv")},
                {"args": ["notes.txt"], "expected": ("notes.txt", "notes", ".txt")},
                {"args": ["/home/user/archive.tar.gz"], "expected": ("archive.tar.gz", "archive.tar", ".gz")},
            ],
            "hint": "p = Path(path); return p.name, p.stem, p.suffix.",
        },
        {
            "id": "join-path",
            "mode": "func",
            "func": "join_path",
            "title": "Склейка пути",
            "statement": (
                "Напишите функцию join_path(parts): склеивает список частей "
                "в путь через pathlib и возвращает его СТРОКОЙ."
            ),
            "starter": "from pathlib import Path\n\n\ndef join_path(parts):\n    pass\n",
            "tests": [
                {"args": [["data", "reports", "a.csv"]], "expected": "data/reports/a.csv"},
                {"args": [["x"]], "expected": "x"},
                {"args": [["/", "tmp", "f.txt"]], "expected": "/tmp/f.txt"},
            ],
            "hint": "str(Path(*parts)) — звёздочка раскладывает список в аргументы.",
        },
        {
            "id": "json-roundtrip",
            "mode": "stdout",
            "title": "Сохранить и загрузить JSON",
            "statement": (
                "Напишите функции save_json(path, data) и load_json(path): "
                "сохранение словаря в файл (utf-8, русские буквы без кодов) и "
                "чтение обратно."
            ),
            "starter": "import json\n\n\ndef save_json(path, data):\n    pass\n\n\ndef load_json(path):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 'd.json')\n"
                "data = {'имя': 'Аня', 'возраст': 20, 'теги': ['а', 'б']}\n"
                "save_json(p, data)\nprint(load_json(p) == data)\n"
                "print('Аня' in open(p, encoding='utf-8').read())\n"
            ),
            "expected": ["True", "True"],
            "hint": "json.dump(data, f, ensure_ascii=False) и json.load(f) внутри with open(..., encoding='utf-8').",
        },
        {
            "id": "csv-column-sum",
            "mode": "stdout",
            "title": "Сумма столбца CSV",
            "statement": (
                "Напишите функцию column_sum(path, column): сумма чисел в "
                "столбце column CSV-файла с заголовком (значения целые)."
            ),
            "starter": "import csv\n\n\ndef column_sum(path, column):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 't.csv')\n"
                "open(p, 'w', encoding='utf-8', newline='').write('имя,цена,штук\\nчай,100,2\\nкофе,250,1\\nсок,80,5\\n')\n"
                "print(column_sum(p, 'цена'))\nprint(column_sum(p, 'штук'))\n"
            ),
            "expected": ["430", "8"],
            "hint": "csv.DictReader; на каждой строке int(row[column]).",
        },
        {
            "id": "csv-group-sum",
            "mode": "stdout",
            "title": "Итоги по отделам",
            "statement": (
                "Напишите функцию sum_by(path, key_col, value_col): словарь "
                "«значение из key_col → сумма значений value_col» по CSV с "
                "заголовком (value_col — целые числа)."
            ),
            "starter": "import csv\n\n\ndef sum_by(path, key_col, value_col):\n    pass\n",
            "driver": (
                "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), 't.csv')\n"
                "open(p, 'w', encoding='utf-8', newline='').write('отдел,зарплата\\nИТ,100\\nHR,70\\nИТ,120\\nHR,80\\nКУ,90\\n')\n"
                "print(sorted(sum_by(p, 'отдел', 'зарплата').items()))\n"
            ),
            "expected": ["[('HR', 150), ('ИТ', 220), ('КУ', 90)]"],
            "hint": "totals[k] = totals.get(k, 0) + int(row[value_col]).",
        },
        {
            "id": "csv-write-table",
            "mode": "stdout",
            "title": "Запись таблицы",
            "statement": (
                "Напишите функцию write_table(path, header, rows): записывает "
                "в CSV строку заголовка и затем строки таблицы (utf-8, "
                "newline=''). Затем в проверке файл читается и разбирается."
            ),
            "starter": "import csv\n\n\ndef write_table(path, header, rows):\n    pass\n",
            "driver": (
                "import csv, os, tempfile\np = os.path.join(tempfile.mkdtemp(), 't.csv')\n"
                "write_table(p, ['имя', 'возраст'], [['Аня', 20], ['Боря, мл.', 31]])\n"
                "with open(p, encoding='utf-8', newline='') as f:\n    print(list(csv.reader(f)))\n"
            ),
            "expected": ["[['имя', 'возраст'], ['Аня', '20'], ['Боря, мл.', '31']]"],
            "hint": "w = csv.writer(f); w.writerow(header); w.writerows(rows).",
        },
        {
            "id": "atomic-write",
            "mode": "stdout",
            "title": "Атомарная запись",
            "statement": (
                "Напишите функцию atomic_write(path, text): сначала запишите "
                "текст во временный файл рядом (path + '.tmp'), затем "
                "замените им целевой файл через os.replace. Временного файла "
                "после работы остаться не должно."
            ),
            "starter": "import os\n\n\ndef atomic_write(path, text):\n    pass\n",
            "driver": (
                "import os, tempfile\nd = tempfile.mkdtemp()\np = os.path.join(d, 'state.txt')\n"
                "atomic_write(p, 'первая версия')\natomic_write(p, 'вторая версия')\n"
                "print(open(p, encoding='utf-8').read())\nprint(sorted(os.listdir(d)))\n"
            ),
            "expected": ["вторая версия", "['state.txt']"],
            "hint": "tmp = path + '.tmp'; запишите в tmp; os.replace(tmp, path).",
        },
        {
            "id": "list-txt",
            "mode": "stdout",
            "title": "Файлы txt в папке",
            "statement": (
                "Напишите функцию list_txt(folder): отсортированный список "
                "ИМЁН файлов с расширением .txt в папке (без вложенных "
                "папок). Используйте pathlib."
            ),
            "starter": "from pathlib import Path\n\n\ndef list_txt(folder):\n    pass\n",
            "driver": (
                "import tempfile\nfrom pathlib import Path\nd = Path(tempfile.mkdtemp())\n"
                "for name in ['b.txt', 'a.txt', 'c.csv', 'd.TXT.bak']:\n    (d / name).write_text('x', encoding='utf-8')\n"
                "(d / 'sub').mkdir()\n(d / 'sub' / 'z.txt').write_text('x', encoding='utf-8')\n"
                "print(list_txt(d))\n"
            ),
            "expected": ["['a.txt', 'b.txt']"],
            "hint": "sorted(p.name for p in Path(folder).glob('*.txt')) — glob без rglob не заходит во вложенные.",
        },
    ],
}
