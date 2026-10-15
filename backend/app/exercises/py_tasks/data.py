"""Задачи «Python как первый язык»: циклы, списки, словари, кортежи (главы 5–11)."""

TASKS: dict[int, list[dict]] = {
    5: [
        {
            "id": "letters",
            "mode": "stdout",
            "title": "Буквы по одной",
            "statement": (
                "Напечатайте каждую букву слова «привет» на отдельной строке. "
                "Используйте цикл for по строке."
            ),
            "starter": 'word = "привет"\n# for ... in ...:\n',
            "expected": ["п", "р", "и", "в", "е", "т"],
            "hint": "for ch in word: print(ch) — на каждом витке ch — очередная буква.",
        },
        {
            "id": "countdown",
            "mode": "stdout",
            "title": "Обратный отсчёт",
            "statement": (
                "Напечатайте числа от 5 до 1 — каждое на своей строке, а в конце "
                "строку «Старт!». Используйте цикл while и не забудьте уменьшать "
                "счётчик."
            ),
            "starter": "n = 5\n# while ...:\n",
            "expected": ["5", "4", "3", "2", "1", "Старт!"],
            "hint": "while n > 0: напечатать n, потом n -= 1. «Старт!» — после цикла, без отступа.",
        },
        {
            "id": "squares",
            "mode": "stdout",
            "title": "Квадраты чисел",
            "statement": (
                "Напечатайте квадраты чисел от 1 до 5 — каждый на своей строке. "
                "Числа получайте через range."
            ),
            "starter": "# for i in range(...):\n",
            "expected": ["1", "4", "9", "16", "25"],
            "hint": "range(1, 6) — шестёрка не входит. Внутри цикла: print(i * i).",
        },
        {
            "id": "sum-to",
            "mode": "func",
            "func": "sum_to",
            "title": "Сумма от 1 до n",
            "statement": (
                "Напишите функцию sum_to(n), которая возвращает сумму всех целых "
                "чисел от 1 до n включительно. Считайте циклом с накопителем, "
                "не по формуле. Для n = 0 сумма равна 0."
            ),
            "starter": "def sum_to(n):\n    total = 0\n    # цикл с накопителем\n    return total\n",
            "tests": [
                {"args": [1], "expected": 1},
                {"args": [4], "expected": 10},
                {"args": [100], "expected": 5050},
                {"args": [0], "expected": 0},
            ],
            "hint": "for i in range(1, n + 1): total += i — правую границу range нужно сдвинуть на единицу.",
        },
        {
            "id": "odds",
            "mode": "stdout",
            "title": "Только нечётные",
            "statement": (
                "Напечатайте нечётные числа от 1 до 10 — каждое на своей строке. "
                "Чётные пропускайте командой continue."
            ),
            "starter": "# for i in range(1, 11):\n#     если чётное — continue\n",
            "expected": ["1", "3", "5", "7", "9"],
            "hint": "if i % 2 == 0: continue — после неё до print дойдут только нечётные.",
        },
        {
            "id": "factorial",
            "mode": "func",
            "func": "factorial",
            "title": "Факториал",
            "statement": (
                "Напишите функцию factorial(n): произведение всех целых чисел от "
                "1 до n. Для n = 0 результат — 1. Накопитель для произведения "
                "стартует с единицы, а не с нуля."
            ),
            "starter": "def factorial(n):\n    result = 1\n    # цикл с накопителем\n    return result\n",
            "tests": [
                {"args": [0], "expected": 1},
                {"args": [1], "expected": 1},
                {"args": [5], "expected": 120},
                {"args": [10], "expected": 3628800},
            ],
            "hint": "for i in range(1, n + 1): result *= i. Ноль даст пустой цикл и ответ 1 — как и нужно.",
        },
        {
            "id": "first-digit",
            "mode": "func",
            "func": "first_digit",
            "title": "Первая цифра в строке",
            "statement": (
                "Напишите функцию first_digit(s), которая возвращает первый "
                "символ-цифру строки s (тоже строкой). Если цифр нет — верните "
                "None. Выйдите из цикла, как только цифра найдена. Проверить "
                "символ поможет метод ch.isdigit()."
            ),
            "starter": "def first_digit(s):\n    for ch in s:\n        pass\n    return None\n",
            "tests": [
                {"args": ["abc7d9"], "expected": "7"},
                {"args": ["сто1"], "expected": "1"},
                {"args": ["привет"], "expected": None},
                {"args": [""], "expected": None},
            ],
            "hint": "Внутри цикла: if ch.isdigit(): return ch — return тоже мгновенно завершает цикл.",
        },
        {
            "id": "reverse-word",
            "mode": "func",
            "func": "reverse_word",
            "title": "Слово наоборот",
            "statement": (
                "Напишите функцию reverse_word(s), которая возвращает строку s, "
                "записанную задом наперёд: из «привет» получается «тевирп». "
                "Собирайте результат циклом, приписывая очередную букву в НАЧАЛО "
                "накопителя. Готовым срезом [::-1] пользоваться нельзя."
            ),
            "starter": 'def reverse_word(s):\n    result = ""\n    # for ch in s: ...\n    return result\n',
            "tests": [
                {"args": ["привет"], "expected": "тевирп"},
                {"args": ["a"], "expected": "a"},
                {"args": [""], "expected": ""},
                {"args": ["abc"], "expected": "cba"},
            ],
            "hint": "result = ch + result — новая буква встаёт перед всем, что накоплено.",
        },
        {
            "id": "count-pairs",
            "mode": "func",
            "func": "count_pairs",
            "title": "Сколько пар",
            "statement": (
                "Напишите функцию count_pairs(n): сколько существует пар чисел "
                "(i, j), у которых 1 <= i < j <= n. Переберите пары двумя "
                "вложенными циклами и посчитайте их счётчиком."
            ),
            "starter": "def count_pairs(n):\n    count = 0\n    # внешний цикл по i, внутренний по j\n    return count\n",
            "tests": [
                {"args": [1], "expected": 0},
                {"args": [3], "expected": 3},
                {"args": [4], "expected": 6},
                {"args": [10], "expected": 45},
            ],
            "hint": "for i in range(1, n + 1): for j in range(i + 1, n + 1): count += 1 — внутренний цикл стартует с i + 1.",
        },
    ],
    6: [
        {
            "id": "build-list",
            "mode": "stdout",
            "title": "Первый список",
            "statement": (
                "Создайте список из чисел 10, 20, 30. Добавьте в конец 40 "
                "методом append, замените первый элемент на 99 и напечатайте "
                "список целиком. Должно получиться [99, 20, 30, 40]."
            ),
            "starter": "nums = [10, 20, 30]\n# append, присваивание по индексу, print\n",
            "expected": ["[99, 20, 30, 40]"],
            "hint": "nums.append(40); nums[0] = 99; print(nums).",
        },
        {
            "id": "first-last",
            "mode": "func",
            "func": "first_last",
            "title": "Первый и последний",
            "statement": (
                "Напишите функцию first_last(nums), которая возвращает список из "
                "двух элементов: первого и последнего элемента nums. Список "
                "непустой. Последний берите отрицательным индексом."
            ),
            "starter": "def first_last(nums):\n    pass\n",
            "tests": [
                {"args": [[10, 20, 30]], "expected": [10, 30]},
                {"args": [[5]], "expected": [5, 5]},
                {"args": [[1, 2]], "expected": [1, 2]},
                {"args": [[7, 8, 9, 10, 11]], "expected": [7, 11]},
            ],
            "hint": "return [nums[0], nums[-1]] — для списка из одного элемента оба индекса указывают на него.",
        },
        {
            "id": "total",
            "mode": "func",
            "func": "total",
            "title": "Сумма списка",
            "statement": (
                "Напишите функцию total(nums): сумма всех элементов списка. Для "
                "пустого списка — 0. Считайте циклом с накопителем, без готовой "
                "функции sum."
            ),
            "starter": "def total(nums):\n    result = 0\n    # for x in nums: ...\n    return result\n",
            "tests": [
                {"args": [[1, 2, 3]], "expected": 6},
                {"args": [[]], "expected": 0},
                {"args": [[-5, 5]], "expected": 0},
                {"args": [[10, 20, 30, 40]], "expected": 100},
            ],
            "hint": "for x in nums: result += x — тот же накопитель, что в главе про циклы.",
        },
        {
            "id": "biggest",
            "mode": "func",
            "func": "biggest",
            "title": "Наибольший элемент",
            "statement": (
                "Напишите функцию biggest(nums): наибольший элемент непустого "
                "списка. Без готовой функции max. Подсказка: начинайте не с "
                "нуля, а с первого элемента — иначе список из одних "
                "отрицательных чисел даст неверный ответ."
            ),
            "starter": "def biggest(nums):\n    best = nums[0]\n    # сравнивайте каждый элемент с best\n    return best\n",
            "tests": [
                {"args": [[3, 9, 2]], "expected": 9},
                {"args": [[-5, -1, -8]], "expected": -1},
                {"args": [[42]], "expected": 42},
                {"args": [[1, 7, 7, 3]], "expected": 7},
            ],
            "hint": "for x in nums: if x > best: best = x.",
        },
        {
            "id": "count-greater",
            "mode": "func",
            "func": "count_greater",
            "title": "Сколько больше порога",
            "statement": (
                "Напишите функцию count_greater(nums, limit): сколько элементов "
                "списка строго больше limit."
            ),
            "starter": "def count_greater(nums, limit):\n    pass\n",
            "tests": [
                {"args": [[1, 5, 10, 15], 5], "expected": 2},
                {"args": [[], 3], "expected": 0},
                {"args": [[2, 2, 2], 2], "expected": 0},
                {"args": [[-1, 0, 1], -5], "expected": 3},
            ],
            "hint": "Счётчик с нуля; if x > limit: count += 1.",
        },
        {
            "id": "evens",
            "mode": "func",
            "func": "evens",
            "title": "Отобрать чётные",
            "statement": (
                "Напишите функцию evens(nums), которая возвращает НОВЫЙ список "
                "из чётных элементов nums в исходном порядке. Заведите пустой "
                "список и наполняйте его через append."
            ),
            "starter": "def evens(nums):\n    result = []\n    # for x in nums: если чётное — append\n    return result\n",
            "tests": [
                {"args": [[1, 2, 3, 4, 5, 6]], "expected": [2, 4, 6]},
                {"args": [[1, 3, 5]], "expected": []},
                {"args": [[]], "expected": []},
                {"args": [[10, 0, -4]], "expected": [10, 0, -4]},
            ],
            "hint": "if x % 2 == 0: result.append(x).",
        },
        {
            "id": "squares-list",
            "mode": "func",
            "func": "squares",
            "title": "Список квадратов",
            "statement": (
                "Напишите функцию squares(nums): новый список, в котором каждый "
                "элемент — квадрат соответствующего элемента nums."
            ),
            "starter": "def squares(nums):\n    result = []\n    return result\n",
            "tests": [
                {"args": [[1, 2, 3]], "expected": [1, 4, 9]},
                {"args": [[]], "expected": []},
                {"args": [[-2, 0, 5]], "expected": [4, 0, 25]},
            ],
            "hint": "result.append(x * x) на каждом витке цикла.",
        },
        {
            "id": "average",
            "mode": "func",
            "func": "average",
            "title": "Среднее арифметическое",
            "statement": (
                "Напишите функцию average(nums): среднее арифметическое "
                "непустого списка — сумма, делённая на количество элементов. "
                "Результат — обычное деление (дробное число)."
            ),
            "starter": "def average(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3]], "expected": 2.0},
                {"args": [[10, 20]], "expected": 15.0},
                {"args": [[5]], "expected": 5.0},
                {"args": [[1, 2]], "expected": 1.5},
            ],
            "hint": "return sum(nums) / len(nums) — готовые sum и len здесь уместны.",
        },
        {
            "id": "without",
            "mode": "func",
            "func": "without",
            "title": "Список без значения",
            "statement": (
                "Напишите функцию without(nums, x): новый список со всеми "
                "элементами nums, кроме тех, что равны x (удалить нужно все "
                "вхождения, не только первое). Исходный порядок сохраняется."
            ),
            "starter": "def without(nums, x):\n    result = []\n    return result\n",
            "tests": [
                {"args": [[1, 2, 3, 2], 2], "expected": [1, 3]},
                {"args": [[5, 5, 5], 5], "expected": []},
                {"args": [[1, 2, 3], 9], "expected": [1, 2, 3]},
                {"args": [[], 1], "expected": []},
            ],
            "hint": "Не удаляйте из исходного списка — наполняйте новый: if item != x: result.append(item).",
        },
    ],
    7: [
        {
            "id": "numbered",
            "mode": "stdout",
            "title": "Нумерованный список",
            "statement": (
                "Напечатайте имена из списка с номерами, начиная с единицы, в "
                "виде «1. Аня». Используйте enumerate с параметром start."
            ),
            "starter": 'names = ["Аня", "Борис", "Вера"]\n# for ..., ... in enumerate(names, start=1):\n',
            "expected": ["1. Аня", "2. Борис", "3. Вера"],
            "hint": 'for i, name in enumerate(names, start=1): print(f"{i}. {name}").',
        },
        {
            "id": "index-of-max",
            "mode": "func",
            "func": "index_of_max",
            "title": "Где максимум",
            "statement": (
                "Напишите функцию index_of_max(nums): индекс наибольшего "
                "элемента непустого списка. Если наибольших несколько — "
                "верните индекс первого. Удобно перебирать через enumerate."
            ),
            "starter": "def index_of_max(nums):\n    best_i = 0\n    # for i, x in enumerate(nums): ...\n    return best_i\n",
            "tests": [
                {"args": [[3, 9, 2]], "expected": 1},
                {"args": [[7]], "expected": 0},
                {"args": [[5, 5, 1]], "expected": 0},
                {"args": [[-3, -1, -2]], "expected": 1},
            ],
            "hint": "Сравнивайте строго: if x > nums[best_i]: best_i = i — тогда при равенстве останется первый.",
        },
        {
            "id": "pair-sums",
            "mode": "func",
            "func": "pair_sums",
            "title": "Сумма попарно",
            "statement": (
                "Напишите функцию pair_sums(a, b): новый список, где i-й "
                "элемент — сумма a[i] и b[i]. Списки одной длины. Склеивайте "
                "их через zip."
            ),
            "starter": "def pair_sums(a, b):\n    result = []\n    # for x, y in zip(a, b): ...\n    return result\n",
            "tests": [
                {"args": [[1, 2, 3], [10, 20, 30]], "expected": [11, 22, 33]},
                {"args": [[], []], "expected": []},
                {"args": [[5], [-5]], "expected": [0]},
            ],
            "hint": "for x, y in zip(a, b): result.append(x + y).",
        },
        {
            "id": "interleave",
            "mode": "func",
            "func": "interleave",
            "title": "Через один",
            "statement": (
                "Напишите функцию interleave(a, b): список, в котором элементы "
                "двух списков (одной длины) чередуются: a[0], b[0], a[1], b[1] "
                "и так далее."
            ),
            "starter": "def interleave(a, b):\n    result = []\n    return result\n",
            "tests": [
                {"args": [[1, 2, 3], [10, 20, 30]], "expected": [1, 10, 2, 20, 3, 30]},
                {"args": [[], []], "expected": []},
                {"args": [["a"], ["b"]], "expected": ["a", "b"]},
            ],
            "hint": "На каждом витке zip — два append: сначала x, потом y.",
        },
        {
            "id": "flatten",
            "mode": "func",
            "func": "flatten",
            "title": "Выпрямить таблицу",
            "statement": (
                "Напишите функцию flatten(matrix): matrix — список списков "
                "чисел. Верните один плоский список со всеми числами по "
                "порядку: из [[1, 2], [3], []] получается [1, 2, 3]."
            ),
            "starter": "def flatten(matrix):\n    result = []\n    # внешний цикл по строкам, внутренний по числам\n    return result\n",
            "tests": [
                {"args": [[[1, 2], [3], []]], "expected": [1, 2, 3]},
                {"args": [[]], "expected": []},
                {"args": [[[1], [2], [3]]], "expected": [1, 2, 3]},
                {"args": [[[5, 6, 7]]], "expected": [5, 6, 7]},
            ],
            "hint": "for row in matrix: for x in row: result.append(x) — либо result.extend(row).",
        },
        {
            "id": "copy-demo",
            "mode": "stdout",
            "title": "Настоящая копия",
            "statement": (
                "Дан список a. Сделайте его НАСТОЯЩУЮ копию b (не просто второе "
                "имя), добавьте в b число 4 и напечатайте сначала a, потом b. "
                "Исходный список a должен остаться без четвёрки."
            ),
            "starter": "a = [1, 2, 3]\n# b = копия a\n# добавьте 4 в b\n# print(a), print(b)\n",
            "expected": ["[1, 2, 3]", "[1, 2, 3, 4]"],
            "hint": "b = a.copy() (или a[:]); b = a лишь повесит на список вторую табличку.",
        },
        {
            "id": "drop-negatives",
            "mode": "func",
            "func": "drop_negatives",
            "title": "Убрать отрицательные",
            "statement": (
                "Напишите функцию drop_negatives(nums): список без "
                "отрицательных чисел (ноль остаётся). Не удаляйте элементы из "
                "списка, по которому идёте циклом: подряд идущие отрицательные "
                "так пропускаются. Соберите новый список."
            ),
            "starter": "def drop_negatives(nums):\n    result = []\n    return result\n",
            "tests": [
                {"args": [[1, -2, 3, -4]], "expected": [1, 3]},
                {"args": [[-1, -2, 3]], "expected": [3]},
                {"args": [[-5, -6, -7]], "expected": []},
                {"args": [[0, 2]], "expected": [0, 2]},
            ],
            "hint": "if x >= 0: result.append(x).",
        },
    ],
    8: [
        {
            "id": "top3",
            "mode": "func",
            "func": "top3",
            "title": "Три наибольших",
            "statement": (
                "Напишите функцию top3(nums): список из трёх наибольших "
                "элементов по убыванию. Если элементов меньше трёх — верните "
                "сколько есть. Исходный список менять нельзя: используйте "
                "sorted, а не sort."
            ),
            "starter": "def top3(nums):\n    pass\n",
            "tests": [
                {"args": [[5, 1, 9, 3, 7]], "expected": [9, 7, 5]},
                {"args": [[2, 8]], "expected": [8, 2]},
                {"args": [[]], "expected": []},
                {"args": [[4, 4, 4, 1]], "expected": [4, 4, 4]},
            ],
            "hint": "sorted(nums, reverse=True)[:3] — срез безопасен и для коротких списков.",
        },
        {
            "id": "by-length",
            "mode": "func",
            "func": "by_length",
            "title": "По длине слов",
            "statement": (
                "Напишите функцию by_length(words): новый список слов, "
                "отсортированный по длине от коротких к длинным. Слова одной "
                "длины остаются в исходном порядке. Используйте параметр key."
            ),
            "starter": "def by_length(words):\n    pass\n",
            "tests": [
                {"args": [["ccc", "a", "bb"]], "expected": ["a", "bb", "ccc"]},
                {"args": [["bb", "aa", "c"]], "expected": ["c", "bb", "aa"]},
                {"args": [[]], "expected": []},
            ],
            "hint": "sorted(words, key=len) — сортировка устойчива: равные по длине не переставляются.",
        },
        {
            "id": "word-lengths",
            "mode": "func",
            "func": "word_lengths",
            "title": "Длины слов",
            "statement": (
                "Напишите функцию word_lengths(words): список длин слов в "
                "том же порядке. Запишите одной строкой — генератором списка."
            ),
            "starter": "def word_lengths(words):\n    return []\n",
            "tests": [
                {"args": [["привет", "мир"]], "expected": [6, 3]},
                {"args": [[]], "expected": []},
                {"args": [["", "a"]], "expected": [0, 1]},
            ],
            "hint": "return [len(w) for w in words].",
        },
        {
            "id": "even-squares",
            "mode": "func",
            "func": "even_squares",
            "title": "Квадраты чётных",
            "statement": (
                "Напишите функцию even_squares(nums): список квадратов только "
                "чётных элементов, в исходном порядке. Одним генератором "
                "списка с условием."
            ),
            "starter": "def even_squares(nums):\n    return []\n",
            "tests": [
                {"args": [[1, 2, 3, 4]], "expected": [4, 16]},
                {"args": [[1, 3]], "expected": []},
                {"args": [[]], "expected": []},
                {"args": [[0, -2]], "expected": [0, 4]},
            ],
            "hint": "[x * x for x in nums if x % 2 == 0] — if идёт после for.",
        },
        {
            "id": "all-even",
            "mode": "func",
            "func": "all_even",
            "title": "Все ли чётные",
            "statement": (
                "Напишите функцию all_even(nums): True, если все элементы "
                "чётные, иначе False. Для пустого списка — True. Попробуйте "
                "встроенную функцию all."
            ),
            "starter": "def all_even(nums):\n    pass\n",
            "tests": [
                {"args": [[2, 4, 6]], "expected": True},
                {"args": [[2, 3]], "expected": False},
                {"args": [[]], "expected": True},
                {"args": [[0]], "expected": True},
            ],
            "hint": "return all(x % 2 == 0 for x in nums).",
        },
        {
            "id": "unique-sorted",
            "mode": "func",
            "func": "unique_sorted",
            "title": "Без повторов, по порядку",
            "statement": (
                "Напишите функцию unique_sorted(nums): отсортированный по "
                "возрастанию список без повторов: из [3, 1, 3, 2, 1] получится "
                "[1, 2, 3]. Множества (set) пока не используйте: отбирайте "
                "новые элементы проверкой in."
            ),
            "starter": "def unique_sorted(nums):\n    seen = []\n    # если x ещё не в seen — добавить\n    return seen\n",
            "tests": [
                {"args": [[3, 1, 3, 2, 1]], "expected": [1, 2, 3]},
                {"args": [[]], "expected": []},
                {"args": [[5, 5, 5]], "expected": [5]},
                {"args": [[2, 1]], "expected": [1, 2]},
            ],
            "hint": "if x not in seen: seen.append(x); в конце seen.sort() и return seen.",
        },
        {
            "id": "balanced",
            "mode": "func",
            "func": "balanced",
            "title": "Скобки в порядке",
            "statement": (
                "Напишите функцию balanced(s): True, если круглые скобки в "
                "строке s расставлены правильно: у каждой «(» есть своя «)» "
                "правее, и ни одна «)» не стоит раньше пары. Остальные символы "
                "игнорируйте. Используйте список как стопку: append на «(», pop "
                "на «)»."
            ),
            "starter": "def balanced(s):\n    stack = []\n    # for ch in s: ...\n    return len(stack) == 0\n",
            "tests": [
                {"args": ["(())"], "expected": True},
                {"args": ["(()"], "expected": False},
                {"args": [")("], "expected": False},
                {"args": [""], "expected": True},
                {"args": ["a(b)c()"], "expected": True},
            ],
            "hint": "На «)» сначала проверьте, что стопка не пуста: если пуста, закрывать нечего — сразу return False (иначе pop упадёт с ошибкой).",
        },
        {
            "id": "second-largest",
            "mode": "func",
            "func": "second_largest",
            "title": "Второе по величине",
            "statement": (
                "Напишите функцию second_largest(nums): второе по величине "
                "РАЗНОЕ значение в списке из хотя бы двух различных чисел: для "
                "[3, 1, 4, 1, 5] — 4, для [10, 10, 5] — 5."
            ),
            "starter": "def second_largest(nums):\n    pass\n",
            "tests": [
                {"args": [[3, 1, 4, 1, 5]], "expected": 4},
                {"args": [[10, 10, 5]], "expected": 5},
                {"args": [[1, 2]], "expected": 1},
                {"args": [[-1, -5, -3]], "expected": -3},
            ],
            "hint": "Уберите повторы (как в unique_sorted), отсортируйте и возьмите предпоследний: items[-2].",
        },
    ],
    9: [
        {
            "id": "build-dict",
            "mode": "stdout",
            "title": "Первый словарь",
            "statement": (
                "Дан прайс {«яблоко»: 50, «банан»: 70}. Добавьте «киви» за 90, "
                "поднимите цену яблока до 55, удалите банан и напечатайте "
                "словарь целиком. Должно получиться "
                "{'яблоко': 55, 'киви': 90}."
            ),
            "starter": 'prices = {"яблоко": 50, "банан": 70}\n# добавить, изменить, удалить, print\n',
            "expected": ["{'яблоко': 55, 'киви': 90}"],
            "hint": 'prices["киви"] = 90; prices["яблоко"] = 55; del prices["банан"]; print(prices).',
        },
        {
            "id": "price-of",
            "mode": "func",
            "func": "price_of",
            "title": "Цена товара",
            "statement": (
                "Напишите функцию price_of(prices, name): цена товара name из "
                "словаря prices, а если такого товара нет — 0. Программа не "
                "должна падать на неизвестном товаре."
            ),
            "starter": "def price_of(prices, name):\n    pass\n",
            "tests": [
                {"args": [{"яблоко": 50}, "яблоко"], "expected": 50},
                {"args": [{"яблоко": 50}, "киви"], "expected": 0},
                {"args": [{}, "хлеб"], "expected": 0},
            ],
            "hint": "prices.get(name, 0) — второй аргумент и есть значение по умолчанию.",
        },
        {
            "id": "with-item",
            "mode": "func",
            "func": "with_item",
            "title": "Словарь с новой парой",
            "statement": (
                "Напишите функцию with_item(d, key, value): новый словарь — "
                "копия d с добавленной (или заменённой) парой key: value. "
                "Исходный словарь d менять нельзя."
            ),
            "starter": "def with_item(d, key, value):\n    result = d.copy()\n    return result\n",
            "tests": [
                {"args": [{"a": 1}, "b", 2], "expected": {"a": 1, "b": 2}},
                {"args": [{"a": 1}, "a", 5], "expected": {"a": 5}},
                {"args": [{}, "x", 0], "expected": {"x": 0}},
            ],
            "hint": "Скопируйте словарь, затем присвойте result[key] = value и верните result.",
        },
        {
            "id": "count-words",
            "mode": "func",
            "func": "count_words",
            "title": "Частоты слов",
            "statement": (
                "Напишите функцию count_words(words): словарь «слово → сколько "
                "раз оно встретилось в списке». Используйте шаблон "
                "counts.get(word, 0) + 1."
            ),
            "starter": "def count_words(words):\n    counts = {}\n    return counts\n",
            "tests": [
                {"args": [["да", "нет", "да"]], "expected": {"да": 2, "нет": 1}},
                {"args": [[]], "expected": {}},
                {"args": [["a", "a", "a"]], "expected": {"a": 3}},
            ],
            "hint": "for w in words: counts[w] = counts.get(w, 0) + 1.",
        },
        {
            "id": "total-price",
            "mode": "func",
            "func": "total_price",
            "title": "Стоимость корзины",
            "statement": (
                "Напишите функцию total_price(prices, cart): prices — цены "
                "товаров, cart — словарь «товар → количество штук». Верните "
                "общую стоимость. Товары, которых нет в прайсе, не стоят "
                "ничего."
            ),
            "starter": "def total_price(prices, cart):\n    total = 0\n    # for name, qty in cart.items(): ...\n    return total\n",
            "tests": [
                {"args": [{"a": 10, "b": 5}, {"a": 2, "b": 3}], "expected": 35},
                {"args": [{"a": 10}, {"zzz": 4}], "expected": 0},
                {"args": [{"a": 10}, {}], "expected": 0},
                {"args": [{"a": 1, "b": 2}, {"a": 1, "zzz": 9, "b": 1}], "expected": 3},
            ],
            "hint": "total += prices.get(name, 0) * qty на каждой паре из cart.items().",
        },
        {
            "id": "word-lengths-dict",
            "mode": "func",
            "func": "length_map",
            "title": "Слово → длина",
            "statement": (
                "Напишите функцию length_map(words): словарь, где ключ — слово "
                "из списка, а значение — его длина."
            ),
            "starter": "def length_map(words):\n    result = {}\n    return result\n",
            "tests": [
                {"args": [["привет", "мир"]], "expected": {"привет": 6, "мир": 3}},
                {"args": [[]], "expected": {}},
                {"args": [["a", "a"]], "expected": {"a": 1}},
            ],
            "hint": "result[word] = len(word) на каждом витке цикла.",
        },
        {
            "id": "has-value",
            "mode": "func",
            "func": "has_value",
            "title": "Есть ли такое значение",
            "statement": (
                "Напишите функцию has_value(d, value): True, если value "
                "встречается среди ЗНАЧЕНИЙ словаря d (а не среди ключей), "
                "иначе False."
            ),
            "starter": "def has_value(d, value):\n    pass\n",
            "tests": [
                {"args": [{"a": 1, "b": 2}, 2], "expected": True},
                {"args": [{"a": 1, "b": 2}, "a"], "expected": False},
                {"args": [{}, 1], "expected": False},
            ],
            "hint": "Слово in у самого словаря смотрит ключи; значения отдаёт d.values().",
        },
        {
            "id": "most-expensive",
            "mode": "func",
            "func": "most_expensive",
            "title": "Самый дорогой",
            "statement": (
                "Напишите функцию most_expensive(prices): название самого "
                "дорогого товара в непустом прайсе. Переберите пары циклом по "
                "prices.items() и запоминайте лучшую."
            ),
            "starter": "def most_expensive(prices):\n    best_name = None\n    best_price = None\n    # for name, price in prices.items(): ...\n    return best_name\n",
            "tests": [
                {"args": [{"a": 10, "b": 30, "c": 20}], "expected": "b"},
                {"args": [{"x": 5}], "expected": "x"},
                {"args": [{"a": -3, "b": -1}], "expected": "b"},
            ],
            "hint": "Если best_price is None или price > best_price — обновите обе переменные.",
        },
    ],
    10: [
        {
            "id": "merge",
            "mode": "func",
            "func": "merge",
            "title": "Слить настройки",
            "statement": (
                "Напишите функцию merge(defaults, custom): новый словарь, в "
                "котором есть все пары обоих словарей, а при совпадении ключей "
                "побеждает custom. Исходные словари менять нельзя."
            ),
            "starter": "def merge(defaults, custom):\n    pass\n",
            "tests": [
                {"args": [{"a": 1, "b": 2}, {"b": 20, "c": 30}], "expected": {"a": 1, "b": 20, "c": 30}},
                {"args": [{}, {"x": 1}], "expected": {"x": 1}},
                {"args": [{"x": 1}, {}], "expected": {"x": 1}},
            ],
            "hint": "defaults | custom — правый словарь перекрывает левый; либо copy + update.",
        },
        {
            "id": "to-dict",
            "mode": "func",
            "func": "to_dict",
            "title": "Словарь из двух списков",
            "statement": (
                "Напишите функцию to_dict(keys, values): словарь, где i-й ключ "
                "связан с i-м значением. Списки одной длины. Воспользуйтесь "
                "dict и zip."
            ),
            "starter": "def to_dict(keys, values):\n    pass\n",
            "tests": [
                {"args": [["a", "b"], [1, 2]], "expected": {"a": 1, "b": 2}},
                {"args": [[], []], "expected": {}},
                {"args": [["x"], [[1, 2]]], "expected": {"x": [1, 2]}},
            ],
            "hint": "return dict(zip(keys, values)).",
        },
        {
            "id": "invert",
            "mode": "func",
            "func": "invert",
            "title": "Перевернуть словарь",
            "statement": (
                "Напишите функцию invert(d): словарь, в котором ключи и "
                "значения поменялись местами. Значения исходного словаря "
                "уникальные строки. Одной записью — генератором словаря."
            ),
            "starter": "def invert(d):\n    return {}\n",
            "tests": [
                {"args": [{"a": "x", "b": "y"}], "expected": {"x": "a", "y": "b"}},
                {"args": [{}], "expected": {}},
                {"args": [{"one": "1"}], "expected": {"1": "one"}},
            ],
            "hint": "{value: key for key, value in d.items()}.",
        },
        {
            "id": "group-by-first",
            "mode": "func",
            "func": "group_by_first",
            "title": "Слова по первой букве",
            "statement": (
                "Напишите функцию group_by_first(words): словарь, где ключ — "
                "первая буква слова, а значение — список слов на эту букву в "
                "исходном порядке. Слова непустые."
            ),
            "starter": "def group_by_first(words):\n    groups = {}\n    return groups\n",
            "tests": [
                {"args": [["арбуз", "банан", "абрикос"]], "expected": {"а": ["арбуз", "абрикос"], "б": ["банан"]}},
                {"args": [[]], "expected": {}},
                {"args": [["ёж"]], "expected": {"ё": ["ёж"]}},
            ],
            "hint": "groups.setdefault(word[0], []).append(word).",
        },
        {
            "id": "most-common",
            "mode": "func",
            "func": "most_common",
            "title": "Самое частое слово",
            "statement": (
                "Напишите функцию most_common(words): самое частое слово "
                "непустого списка. Если таких несколько — то, что встретилось "
                "в списке раньше. Посчитайте частоты и найдите максимум по "
                "значению."
            ),
            "starter": "def most_common(words):\n    counts = {}\n    # посчитать частоты, затем max(counts, key=counts.get)\n",
            "tests": [
                {"args": [["да", "нет", "да"]], "expected": "да"},
                {"args": [["a", "b", "b", "a"]], "expected": "a"},
                {"args": [["один"]], "expected": "один"},
            ],
            "hint": "max(counts, key=counts.get) возвращает ключ с наибольшим значением, а при ничьей — первый.",
        },
        {
            "id": "adult-names",
            "mode": "func",
            "func": "adult_names",
            "title": "Имена взрослых",
            "statement": (
                "Напишите функцию adult_names(users): users — список словарей "
                "{'name': ..., 'age': ...}. Верните список имён тех, кому 18 "
                "или больше, в исходном порядке."
            ),
            "starter": "def adult_names(users):\n    pass\n",
            "tests": [
                {"args": [[{"name": "Аня", "age": 20}, {"name": "Боря", "age": 15}, {"name": "Вера", "age": 18}]], "expected": ["Аня", "Вера"]},
                {"args": [[]], "expected": []},
                {"args": [[{"name": "Гоша", "age": 5}]], "expected": []},
            ],
            "hint": "[u['name'] for u in users if u['age'] >= 18].",
        },
        {
            "id": "sort-by-age",
            "mode": "func",
            "func": "sort_by_age",
            "title": "Сортировка по возрасту",
            "statement": (
                "Напишите функцию sort_by_age(users): список тех же записей "
                "{'name': ..., 'age': ...}, отсортированный по возрасту от "
                "младшего к старшему. Для ключа сортировки определите "
                "маленькую функцию-помощник."
            ),
            "starter": "def get_age(user):\n    pass\n\n\ndef sort_by_age(users):\n    pass\n",
            "tests": [
                {"args": [[{"name": "А", "age": 30}, {"name": "Б", "age": 20}]], "expected": [{"name": "Б", "age": 20}, {"name": "А", "age": 30}]},
                {"args": [[]], "expected": []},
                {"args": [[{"name": "А", "age": 5}, {"name": "Б", "age": 5}]], "expected": [{"name": "А", "age": 5}, {"name": "Б", "age": 5}]},
            ],
            "hint": "def get_age(user): return user['age'] — и sorted(users, key=get_age).",
        },
        {
            "id": "grade-word",
            "mode": "func",
            "func": "grade_word",
            "title": "Оценка словом",
            "statement": (
                "Напишите функцию grade_word(grade): 5 → «отлично», 4 → "
                "«хорошо», 3 → «удовлетворительно», 2 → «плохо», всё "
                "остальное → «неизвестно». Без цепочки if — таблицей "
                "соответствий в словаре."
            ),
            "starter": "def grade_word(grade):\n    words = {}\n    pass\n",
            "tests": [
                {"args": [5], "expected": "отлично"},
                {"args": [4], "expected": "хорошо"},
                {"args": [3], "expected": "удовлетворительно"},
                {"args": [2], "expected": "плохо"},
                {"args": [7], "expected": "неизвестно"},
            ],
            "hint": "return words.get(grade, 'неизвестно') — в словаре words пары 5: 'отлично' и так далее.",
        },
    ],
    11: [
        {
            "id": "unpack-point",
            "mode": "stdout",
            "title": "Распаковка точки",
            "statement": (
                "Дан кортеж point с координатами. Распакуйте его в переменные "
                "x и y одной строкой и напечатайте их произведение."
            ),
            "starter": "point = (3, 4)\n# x, y = ...\n",
            "expected": ["12"],
            "hint": "x, y = point — затем print(x * y).",
        },
        {
            "id": "swap-pair",
            "mode": "func",
            "func": "swap_pair",
            "title": "Поменять местами",
            "statement": (
                "Напишите функцию swap_pair(p): принимает кортеж из двух "
                "элементов и возвращает новый кортеж, где элементы поменялись "
                "местами."
            ),
            "starter": "def swap_pair(p):\n    pass\n",
            "tests": [
                {"args": [(1, 2)], "expected": (2, 1)},
                {"args": [("a", "b")], "expected": ("b", "a")},
                {"args": [(5, 5)], "expected": (5, 5)},
            ],
            "hint": "a, b = p; return b, a — запятая в return собирает кортеж.",
        },
        {
            "id": "min-max",
            "mode": "func",
            "func": "min_max",
            "title": "Минимум и максимум",
            "statement": (
                "Напишите функцию min_max(nums): кортеж из наименьшего и "
                "наибольшего элементов непустого списка. Вернуть нужно именно "
                "кортеж, а не список."
            ),
            "starter": "def min_max(nums):\n    pass\n",
            "tests": [
                {"args": [[3, 1, 9, 4]], "expected": (1, 9)},
                {"args": [[7]], "expected": (7, 7)},
                {"args": [[-5, -2]], "expected": (-5, -2)},
            ],
            "hint": "return min(nums), max(nums).",
        },
        {
            "id": "div-mod",
            "mode": "func",
            "func": "div_mod",
            "title": "Деление с остатком",
            "statement": (
                "Напишите функцию div_mod(a, b): кортеж из целой части и "
                "остатка от деления a на b (b не ноль). Без готовой функции "
                "divmod: операторы // и %."
            ),
            "starter": "def div_mod(a, b):\n    pass\n",
            "tests": [
                {"args": [17, 5], "expected": (3, 2)},
                {"args": [10, 5], "expected": (2, 0)},
                {"args": [0, 3], "expected": (0, 0)},
            ],
            "hint": "return a // b, a % b.",
        },
        {
            "id": "split-first",
            "mode": "func",
            "func": "split_first",
            "title": "Голова и хвост",
            "statement": (
                "Напишите функцию split_first(items): кортеж из первого "
                "элемента и списка остальных. Список непустой. Для разбора "
                "используйте распаковку со звёздочкой."
            ),
            "starter": "def split_first(items):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3]], "expected": (1, [2, 3])},
                {"args": [[5]], "expected": (5, [])},
                {"args": [["a", "b"]], "expected": ("a", ["b"])},
            ],
            "hint": "first, *rest = items; return first, rest.",
        },
        {
            "id": "lookup-cell",
            "mode": "func",
            "func": "lookup",
            "title": "Клетка поля",
            "statement": (
                "Напишите функцию lookup(cells, row, col). cells — список "
                "кортежей (строка, столбец, значение). Постройте словарь, где "
                "ключ — кортеж (строка, столбец), и верните значение клетки "
                "(row, col) или None, если такой клетки нет."
            ),
            "starter": "def lookup(cells, row, col):\n    field = {}\n    # for r, c, value in cells: ...\n    return None\n",
            "tests": [
                {"args": [[(0, 0, "X"), (1, 2, "O")], 1, 2], "expected": "O"},
                {"args": [[(0, 0, "X")], 5, 5], "expected": None},
                {"args": [[], 0, 0], "expected": None},
            ],
            "hint": "field[(r, c)] = value при построении, затем field.get((row, col)).",
        },
        {
            "id": "sort-people",
            "mode": "func",
            "func": "sort_people",
            "title": "Старшие вперёд",
            "statement": (
                "Напишите функцию sort_people(people): people — список "
                "кортежей (имя, возраст). Верните новый список, "
                "отсортированный по возрасту от старшего к младшему, а при "
                "равном возрасте — по имени по алфавиту. Ключ сортировки — "
                "кортеж (минус возраст, имя)."
            ),
            "starter": "def by_key(person):\n    pass\n\n\ndef sort_people(people):\n    return sorted(people, key=by_key)\n",
            "tests": [
                {"args": [[("Аня", 20), ("Боря", 30)]], "expected": [("Боря", 30), ("Аня", 20)]},
                {"args": [[("Вера", 20), ("Аня", 20)]], "expected": [("Аня", 20), ("Вера", 20)]},
                {"args": [[]], "expected": []},
            ],
            "hint": "def by_key(person): name, age = person; return -age, name.",
        },
    ],
}
