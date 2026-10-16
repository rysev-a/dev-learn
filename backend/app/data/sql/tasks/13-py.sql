-- Упражнения книги 13 «py — Python как первый язык». Файл строит export_tasks.py — руками не правьте.

INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 0, 'intro-variable', 0, 'stdout', 'Переменная', 'Создайте переменную year со значением 1991 (год, когда появился Python) и выведите её значение командой print.', '# Имя = значение
', 'year = 1991, затем print(year).', '{"expected": ["1991"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 0, 'intro-types', 1, 'stdout', 'Типы значений', 'Выведите по одной строке названия типов значений 5, 2.5, "привет" и True (в таком порядке): int, float, str, bool. Получите их функцией type, а не вписывайте слова вручную.', '# type(значение).__name__ даёт имя типа
', 'print(type(5).__name__) — и так для каждого значения.', '{"expected": ["int", "float", "str", "bool"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 0, 'intro-parity', 2, 'func', 'Условие', 'Напишите функцию parity(n), которая возвращает строку «чётное», если n делится на 2 без остатка, и «нечётное» в остальных случаях.', 'def parity(n):
    pass
', 'if n % 2 == 0: return "чётное"; иначе — «нечётное».', '{"func": "parity", "tests": [{"args": [4], "expected": "чётное"}, {"args": [7], "expected": "нечётное"}, {"args": [0], "expected": "чётное"}, {"args": [-3], "expected": "нечётное"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 0, 'intro-loop', 3, 'stdout', 'Цикл', 'Выведите числа от 1 до 5, каждое на своей строке, с помощью цикла for (пять строк print писать нельзя — результат должен получиться циклом).', '# for i in range(...):
', 'for i in range(1, 6): print(i).', '{"expected": ["1", "2", "3", "4", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 0, 'intro-function', 4, 'func', 'Функция', 'Напишите функцию circle_area(r), которая возвращает площадь круга радиуса r: 3.14 * r * r.', 'def circle_area(r):
    pass
', 'return 3.14 * r * r.', '{"func": "circle_area", "tests": [{"args": [1], "expected": 3.14}, {"args": [2], "expected": 12.56}, {"args": [0], "expected": 0.0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 0, 'intro-class', 5, 'stdout', 'Класс', 'Опишите класс Dog: при создании Dog("Рекс") сохраняется имя, а метод speak() возвращает строку «Рекс: гав» (имя подставляется). Ничего не печатайте — проверка вызовет ваш класс сама.', 'class Dog:
    pass
', 'В __init__ сохраните self.name; в speak верните f"{self.name}: гав".', '{"driver": "d = Dog(\"Рекс\")\nprint(d.speak())\nprint(Dog(\"Шарик\").speak())\n", "expected": ["Рекс: гав", "Шарик: гав"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 1, 'hello', 0, 'stdout', 'Первая строка', 'Напишите программу, которая печатает ровно одну строку: Привет, Python!', '# Ваша первая программа
', 'Одна команда print, текст — в кавычках внутри скобок.', '{"expected": ["Привет, Python!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 1, 'two-lines', 1, 'stdout', 'Две строки', 'Выведите две строки друг за другом: сначала «Меня зовут Python», потом «Мне 34 года».', '# Две команды print
', 'Каждая строка — своя команда print; они выполняются сверху вниз.', '{"expected": ["Меня зовут Python", "Мне 34 года"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 1, 'calc', 2, 'stdout', 'Считает print', 'Печатайте результат умножения шести на семь — но посчитайте его прямо внутри print, а не готовым числом в кавычках.', '# Пусть Python посчитает сам
', 'Внутри скобок print можно написать арифметику: print(6 * 7).', '{"expected": ["42"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 1, 'repeat', 3, 'stdout', 'Повтор строки', 'Выведите «ляляля» — но получите эту строку умножением строки «ля» на три, а не вписыванием готового слова.', '# Умножение строки
', 'Звёздочка повторяет строку: «ля» * 3.', '{"expected": ["ляляля"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 1, 'repeat-big', 4, 'stdout', 'Повтор всерьёз', 'Выведите строку i234_34$ ровно 344 раза подряд — одной строкой, без пробелов и переносов. Умножением строки на число: вручную такое не перепечатать.', '# Без копипасты: строка * число
', 'print(''i234_34$'' * 344) — звёздочка повторит строку нужное число раз.', '{"expected": ["i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$i234_34$"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 2, 'greet', 0, 'func', 'Приветствие', 'Напишите функцию greet(name), которая возвращает строку вида «Привет, Аня!» — то есть «Привет, » + имя + восклицательный знак. Используйте f-строку.', 'def greet(name):
    # верните f-строку с именем внутри
    pass
', 'f"Привет, {name}!" — фигурные скобки подставят значение.', '{"func": "greet", "tests": [{"args": ["Аня"], "expected": "Привет, Аня!"}, {"args": ["Python"], "expected": "Привет, Python!"}, {"args": ["world"], "expected": "Привет, world!"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 2, 'area', 1, 'func', 'Площадь прямоугольника', 'Напишите функцию area(a, b), которая возвращает площадь прямоугольника со сторонами a и b.', 'def area(a, b):
    pass
', 'Площадь — произведение сторон: return a * b.', '{"func": "area", "tests": [{"args": [3, 4], "expected": 12}, {"args": [5, 5], "expected": 25}, {"args": [2, 10], "expected": 20}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 2, 'to-celsius', 2, 'func', 'Фаренгейты в цельсии', 'Напишите функцию to_celsius(f), которая переводит температуру из Фаренгейтов в Цельсии по формуле (f - 32) * 5 / 9 и возвращает результат.', 'def to_celsius(f):
    pass
', 'Формула уже в условии: return (f - 32) * 5 / 9. В Python скобки задают порядок.', '{"func": "to_celsius", "tests": [{"args": [32], "expected": 0.0}, {"args": [212], "expected": 100.0}, {"args": [50], "expected": 10.0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 3, 'sign', 0, 'func', 'Знак числа', 'Напишите функцию sign(x), которая возвращает слово «положительное» для x > 0, «отрицательное» для x < 0 и «ноль» для x = 0.', 'def sign(x):
    # if / elif / else — три дороги
    pass
', 'Три ветки: if x > 0: ... elif x < 0: ... else: ...', '{"func": "sign", "tests": [{"args": [5], "expected": "положительное"}, {"args": [-3], "expected": "отрицательное"}, {"args": [0], "expected": "ноль"}, {"args": [100], "expected": "положительное"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 3, 'is-even', 1, 'func', 'Чётное ли число', 'Напишите функцию is_even(n), которая возвращает True, если n чётное, и False — если нечётное. Подсказка: остаток от деления — оператор %.', 'def is_even(n):
    pass
', 'Сравнение само даёт bool: return n % 2 == 0.', '{"func": "is_even", "tests": [{"args": [4], "expected": true}, {"args": [7], "expected": false}, {"args": [0], "expected": true}, {"args": [13], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 3, 'max2', 2, 'func', 'Максимум из двух', 'Напишите функцию max2(a, b), которая возвращает большее из двух чисел. Встроенную функцию max() использовать нельзя — только if и else.', 'def max2(a, b):
    pass
', 'if a > b: вернуть a, иначе — вернуть b. Равные числа: подойдёт любая ветка else.', '{"func": "max2", "tests": [{"args": [3, 7], "expected": 7}, {"args": [10, 2], "expected": 10}, {"args": [5, 5], "expected": 5}, {"args": [-1, -9], "expected": -1}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 3, 'ticket-price', 3, 'func', 'Цена билета', 'Кинотеатр ставит цену по возрасту: до 7 лет включительно — 0, от 8 до 17 включительно — 200, от 18 и старше — 400. Напишите функцию ticket_price(age), возвращающую цену.', 'def ticket_price(age):
    # цепочка if / elif / else
    pass
', 'Проверяйте сверху вниз от младших: if age <= 7 ... elif age <= 17 ... else ...', '{"func": "ticket_price", "tests": [{"args": [3], "expected": 0}, {"args": [7], "expected": 0}, {"args": [8], "expected": 200}, {"args": [17], "expected": 200}, {"args": [18], "expected": 400}, {"args": [65], "expected": 400}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 4, 'hello-twice', 0, 'stdout', 'Своя функция', 'Опишите функцию hello(name), которая печатает «Привет, <имя>!», и вызовите её дважды: для «Аня» и для «Борис».', '# def hello(name): ...
# два вызова
', 'def hello(name): print(f"Привет, {name}!") — а ниже hello("Аня") и hello("Борис").', '{"expected": ["Привет, Аня!", "Привет, Борис!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 4, 'average3', 1, 'func', 'Среднее трёх', 'Напишите функцию average3(a, b, c): среднее арифметическое трёх чисел. Функция должна вернуть результат, а не печатать его.', 'def average3(a, b, c):
    pass
', 'return (a + b + c) / 3 — именно return, а не print.', '{"func": "average3", "tests": [{"args": [1, 2, 3], "expected": 2.0}, {"args": [10, 20, 30], "expected": 20.0}, {"args": [0, 0, 1], "expected": 0.3333333333333333}, {"args": [-3, 3, 0], "expected": 0.0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 4, 'clamp', 2, 'func', 'Ограничить число', 'Напишите функцию clamp(x, low, high): если x меньше low — верните low, если больше high — high, иначе сам x.', 'def clamp(x, low, high):
    pass
', 'Два ранних выхода: if x < low: return low; if x > high: return high; затем return x.', '{"func": "clamp", "tests": [{"args": [5, 0, 10], "expected": 5}, {"args": [-3, 0, 10], "expected": 0}, {"args": [42, 0, 10], "expected": 10}, {"args": [10, 0, 10], "expected": 10}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 4, 'power-default', 3, 'func', 'Степень с умолчанием', 'Напишите функцию power(x, n=2): x в степени n. Если n не передали, возводим в квадрат.', 'def power(x, n=2):
    pass
', 'return x ** n — значение по умолчанию уже стоит в заголовке.', '{"func": "power", "tests": [{"args": [5], "expected": 25}, {"args": [2, 10], "expected": 1024}, {"args": [3, 0], "expected": 1}, {"args": [-2, 3], "expected": -8}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 4, 'is-leap', 4, 'func', 'Високосный год', 'Напишите функцию is_leap(year): True для високосного года. Год високосный, если он делится на 4, кроме годов, которые делятся на 100, но не делятся на 400.', 'def is_leap(year):
    pass
', 'return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0).', '{"func": "is_leap", "tests": [{"args": [2024], "expected": true}, {"args": [2023], "expected": false}, {"args": [1900], "expected": false}, {"args": [2000], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 4, 'fizzbuzz', 5, 'func', 'Физзбазз', 'Напишите функцию fizzbuzz(n): «FizzBuzz», если n делится на 3 и на 5; «Fizz», если только на 3; «Buzz», если только на 5; иначе — само число в виде строки.', 'def fizzbuzz(n):
    pass
', 'Сначала самый строгий случай (оба), потом по одному; в конце return str(n).', '{"func": "fizzbuzz", "tests": [{"args": [15], "expected": "FizzBuzz"}, {"args": [9], "expected": "Fizz"}, {"args": [10], "expected": "Buzz"}, {"args": [7], "expected": "7"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 4, 'triangle-kind', 6, 'func', 'Вид треугольника', 'Напишите функцию triangle_kind(a, b, c): «равносторонний», если все три стороны равны, «равнобедренный», если равны ровно две, иначе «разносторонний».', 'def triangle_kind(a, b, c):
    pass
', 'Сначала проверьте a == b == c, затем «хоть одна пара равна»: a == b or b == c or a == c.', '{"func": "triangle_kind", "tests": [{"args": [3, 3, 3], "expected": "равносторонний"}, {"args": [3, 3, 5], "expected": "равнобедренный"}, {"args": [3, 5, 3], "expected": "равнобедренный"}, {"args": [3, 4, 5], "expected": "разносторонний"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 4, 'factorial-rec', 7, 'func', 'Факториал рекурсией', 'Напишите функцию fact(n): факториал n, но через рекурсию — функция должна вызывать саму себя. Базовый случай: fact(0) = 1.', 'def fact(n):
    pass
', 'if n == 0: return 1; иначе return n * fact(n - 1).', '{"func": "fact", "tests": [{"args": [0], "expected": 1}, {"args": [1], "expected": 1}, {"args": [5], "expected": 120}, {"args": [8], "expected": 40320}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'letters', 0, 'stdout', 'Буквы по одной', 'Напечатайте каждую букву слова «привет» на отдельной строке. Используйте цикл for по строке.', 'word = "привет"
# for ... in ...:
', 'for ch in word: print(ch) — на каждом витке ch — очередная буква.', '{"expected": ["п", "р", "и", "в", "е", "т"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'countdown', 1, 'stdout', 'Обратный отсчёт', 'Напечатайте числа от 5 до 1 — каждое на своей строке, а в конце строку «Старт!». Используйте цикл while и не забудьте уменьшать счётчик.', 'n = 5
# while ...:
', 'while n > 0: напечатать n, потом n -= 1. «Старт!» — после цикла, без отступа.', '{"expected": ["5", "4", "3", "2", "1", "Старт!"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'squares', 2, 'stdout', 'Квадраты чисел', 'Напечатайте квадраты чисел от 1 до 5 — каждый на своей строке. Числа получайте через range.', '# for i in range(...):
', 'range(1, 6) — шестёрка не входит. Внутри цикла: print(i * i).', '{"expected": ["1", "4", "9", "16", "25"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'sum-to', 3, 'func', 'Сумма от 1 до n', 'Напишите функцию sum_to(n), которая возвращает сумму всех целых чисел от 1 до n включительно. Считайте циклом с накопителем, не по формуле. Для n = 0 сумма равна 0.', 'def sum_to(n):
    total = 0
    # цикл с накопителем
    return total
', 'for i in range(1, n + 1): total += i — правую границу range нужно сдвинуть на единицу.', '{"func": "sum_to", "tests": [{"args": [1], "expected": 1}, {"args": [4], "expected": 10}, {"args": [100], "expected": 5050}, {"args": [0], "expected": 0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'odds', 4, 'stdout', 'Только нечётные', 'Напечатайте нечётные числа от 1 до 10 — каждое на своей строке. Чётные пропускайте командой continue.', '# for i in range(1, 11):
#     если чётное — continue
', 'if i % 2 == 0: continue — после неё до print дойдут только нечётные.', '{"expected": ["1", "3", "5", "7", "9"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'factorial', 5, 'func', 'Факториал', 'Напишите функцию factorial(n): произведение всех целых чисел от 1 до n. Для n = 0 результат — 1. Накопитель для произведения стартует с единицы, а не с нуля.', 'def factorial(n):
    result = 1
    # цикл с накопителем
    return result
', 'for i in range(1, n + 1): result *= i. Ноль даст пустой цикл и ответ 1 — как и нужно.', '{"func": "factorial", "tests": [{"args": [0], "expected": 1}, {"args": [1], "expected": 1}, {"args": [5], "expected": 120}, {"args": [10], "expected": 3628800}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'first-digit', 6, 'func', 'Первая цифра в строке', 'Напишите функцию first_digit(s), которая возвращает первый символ-цифру строки s (тоже строкой). Если цифр нет — верните None. Выйдите из цикла, как только цифра найдена. Проверить символ поможет метод ch.isdigit().', 'def first_digit(s):
    for ch in s:
        pass
    return None
', 'Внутри цикла: if ch.isdigit(): return ch — return тоже мгновенно завершает цикл.', '{"func": "first_digit", "tests": [{"args": ["abc7d9"], "expected": "7"}, {"args": ["сто1"], "expected": "1"}, {"args": ["привет"], "expected": null}, {"args": [""], "expected": null}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'reverse-word', 7, 'func', 'Слово наоборот', 'Напишите функцию reverse_word(s), которая возвращает строку s, записанную задом наперёд: из «привет» получается «тевирп». Собирайте результат циклом, приписывая очередную букву в НАЧАЛО накопителя. Готовым срезом [::-1] пользоваться нельзя.', 'def reverse_word(s):
    result = ""
    # for ch in s: ...
    return result
', 'result = ch + result — новая буква встаёт перед всем, что накоплено.', '{"func": "reverse_word", "tests": [{"args": ["привет"], "expected": "тевирп"}, {"args": ["a"], "expected": "a"}, {"args": [""], "expected": ""}, {"args": ["abc"], "expected": "cba"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 5, 'count-pairs', 8, 'func', 'Сколько пар', 'Напишите функцию count_pairs(n): сколько существует пар чисел (i, j), у которых 1 <= i < j <= n. Переберите пары двумя вложенными циклами и посчитайте их счётчиком.', 'def count_pairs(n):
    count = 0
    # внешний цикл по i, внутренний по j
    return count
', 'for i in range(1, n + 1): for j in range(i + 1, n + 1): count += 1 — внутренний цикл стартует с i + 1.', '{"func": "count_pairs", "tests": [{"args": [1], "expected": 0}, {"args": [3], "expected": 3}, {"args": [4], "expected": 6}, {"args": [10], "expected": 45}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'build-list', 0, 'stdout', 'Первый список', 'Создайте список из чисел 10, 20, 30. Добавьте в конец 40 методом append, замените первый элемент на 99 и напечатайте список целиком. Должно получиться [99, 20, 30, 40].', 'nums = [10, 20, 30]
# append, присваивание по индексу, print
', 'nums.append(40); nums[0] = 99; print(nums).', '{"expected": ["[99, 20, 30, 40]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'first-last', 1, 'func', 'Первый и последний', 'Напишите функцию first_last(nums), которая возвращает список из двух элементов: первого и последнего элемента nums. Список непустой. Последний берите отрицательным индексом.', 'def first_last(nums):
    pass
', 'return [nums[0], nums[-1]] — для списка из одного элемента оба индекса указывают на него.', '{"func": "first_last", "tests": [{"args": [[10, 20, 30]], "expected": [10, 30]}, {"args": [[5]], "expected": [5, 5]}, {"args": [[1, 2]], "expected": [1, 2]}, {"args": [[7, 8, 9, 10, 11]], "expected": [7, 11]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'total', 2, 'func', 'Сумма списка', 'Напишите функцию total(nums): сумма всех элементов списка. Для пустого списка — 0. Считайте циклом с накопителем, без готовой функции sum.', 'def total(nums):
    result = 0
    # for x in nums: ...
    return result
', 'for x in nums: result += x — тот же накопитель, что в главе про циклы.', '{"func": "total", "tests": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}, {"args": [[-5, 5]], "expected": 0}, {"args": [[10, 20, 30, 40]], "expected": 100}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'biggest', 3, 'func', 'Наибольший элемент', 'Напишите функцию biggest(nums): наибольший элемент непустого списка. Без готовой функции max. Подсказка: начинайте не с нуля, а с первого элемента — иначе список из одних отрицательных чисел даст неверный ответ.', 'def biggest(nums):
    best = nums[0]
    # сравнивайте каждый элемент с best
    return best
', 'for x in nums: if x > best: best = x.', '{"func": "biggest", "tests": [{"args": [[3, 9, 2]], "expected": 9}, {"args": [[-5, -1, -8]], "expected": -1}, {"args": [[42]], "expected": 42}, {"args": [[1, 7, 7, 3]], "expected": 7}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'count-greater', 4, 'func', 'Сколько больше порога', 'Напишите функцию count_greater(nums, limit): сколько элементов списка строго больше limit.', 'def count_greater(nums, limit):
    pass
', 'Счётчик с нуля; if x > limit: count += 1.', '{"func": "count_greater", "tests": [{"args": [[1, 5, 10, 15], 5], "expected": 2}, {"args": [[], 3], "expected": 0}, {"args": [[2, 2, 2], 2], "expected": 0}, {"args": [[-1, 0, 1], -5], "expected": 3}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'evens', 5, 'func', 'Отобрать чётные', 'Напишите функцию evens(nums), которая возвращает НОВЫЙ список из чётных элементов nums в исходном порядке. Заведите пустой список и наполняйте его через append.', 'def evens(nums):
    result = []
    # for x in nums: если чётное — append
    return result
', 'if x % 2 == 0: result.append(x).', '{"func": "evens", "tests": [{"args": [[1, 2, 3, 4, 5, 6]], "expected": [2, 4, 6]}, {"args": [[1, 3, 5]], "expected": []}, {"args": [[]], "expected": []}, {"args": [[10, 0, -4]], "expected": [10, 0, -4]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'squares-list', 6, 'func', 'Список квадратов', 'Напишите функцию squares(nums): новый список, в котором каждый элемент — квадрат соответствующего элемента nums.', 'def squares(nums):
    result = []
    return result
', 'result.append(x * x) на каждом витке цикла.', '{"func": "squares", "tests": [{"args": [[1, 2, 3]], "expected": [1, 4, 9]}, {"args": [[]], "expected": []}, {"args": [[-2, 0, 5]], "expected": [4, 0, 25]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'average', 7, 'func', 'Среднее арифметическое', 'Напишите функцию average(nums): среднее арифметическое непустого списка — сумма, делённая на количество элементов. Результат — обычное деление (дробное число).', 'def average(nums):
    pass
', 'return sum(nums) / len(nums) — готовые sum и len здесь уместны.', '{"func": "average", "tests": [{"args": [[1, 2, 3]], "expected": 2.0}, {"args": [[10, 20]], "expected": 15.0}, {"args": [[5]], "expected": 5.0}, {"args": [[1, 2]], "expected": 1.5}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 6, 'without', 8, 'func', 'Список без значения', 'Напишите функцию without(nums, x): новый список со всеми элементами nums, кроме тех, что равны x (удалить нужно все вхождения, не только первое). Исходный порядок сохраняется.', 'def without(nums, x):
    result = []
    return result
', 'Не удаляйте из исходного списка — наполняйте новый: if item != x: result.append(item).', '{"func": "without", "tests": [{"args": [[1, 2, 3, 2], 2], "expected": [1, 3]}, {"args": [[5, 5, 5], 5], "expected": []}, {"args": [[1, 2, 3], 9], "expected": [1, 2, 3]}, {"args": [[], 1], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 7, 'numbered', 0, 'stdout', 'Нумерованный список', 'Напечатайте имена из списка с номерами, начиная с единицы, в виде «1. Аня». Используйте enumerate с параметром start.', 'names = ["Аня", "Борис", "Вера"]
# for ..., ... in enumerate(names, start=1):
', 'for i, name in enumerate(names, start=1): print(f"{i}. {name}").', '{"expected": ["1. Аня", "2. Борис", "3. Вера"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 7, 'index-of-max', 1, 'func', 'Где максимум', 'Напишите функцию index_of_max(nums): индекс наибольшего элемента непустого списка. Если наибольших несколько — верните индекс первого. Удобно перебирать через enumerate.', 'def index_of_max(nums):
    best_i = 0
    # for i, x in enumerate(nums): ...
    return best_i
', 'Сравнивайте строго: if x > nums[best_i]: best_i = i — тогда при равенстве останется первый.', '{"func": "index_of_max", "tests": [{"args": [[3, 9, 2]], "expected": 1}, {"args": [[7]], "expected": 0}, {"args": [[5, 5, 1]], "expected": 0}, {"args": [[-3, -1, -2]], "expected": 1}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 7, 'pair-sums', 2, 'func', 'Сумма попарно', 'Напишите функцию pair_sums(a, b): новый список, где i-й элемент — сумма a[i] и b[i]. Списки одной длины. Склеивайте их через zip.', 'def pair_sums(a, b):
    result = []
    # for x, y in zip(a, b): ...
    return result
', 'for x, y in zip(a, b): result.append(x + y).', '{"func": "pair_sums", "tests": [{"args": [[1, 2, 3], [10, 20, 30]], "expected": [11, 22, 33]}, {"args": [[], []], "expected": []}, {"args": [[5], [-5]], "expected": [0]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 7, 'interleave', 3, 'func', 'Через один', 'Напишите функцию interleave(a, b): список, в котором элементы двух списков (одной длины) чередуются: a[0], b[0], a[1], b[1] и так далее.', 'def interleave(a, b):
    result = []
    return result
', 'На каждом витке zip — два append: сначала x, потом y.', '{"func": "interleave", "tests": [{"args": [[1, 2, 3], [10, 20, 30]], "expected": [1, 10, 2, 20, 3, 30]}, {"args": [[], []], "expected": []}, {"args": [["a"], ["b"]], "expected": ["a", "b"]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 7, 'flatten', 4, 'func', 'Выпрямить таблицу', 'Напишите функцию flatten(matrix): matrix — список списков чисел. Верните один плоский список со всеми числами по порядку: из [[1, 2], [3], []] получается [1, 2, 3].', 'def flatten(matrix):
    result = []
    # внешний цикл по строкам, внутренний по числам
    return result
', 'for row in matrix: for x in row: result.append(x) — либо result.extend(row).', '{"func": "flatten", "tests": [{"args": [[[1, 2], [3], []]], "expected": [1, 2, 3]}, {"args": [[]], "expected": []}, {"args": [[[1], [2], [3]]], "expected": [1, 2, 3]}, {"args": [[[5, 6, 7]]], "expected": [5, 6, 7]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 7, 'copy-demo', 5, 'stdout', 'Настоящая копия', 'Дан список a. Сделайте его НАСТОЯЩУЮ копию b (не просто второе имя), добавьте в b число 4 и напечатайте сначала a, потом b. Исходный список a должен остаться без четвёрки.', 'a = [1, 2, 3]
# b = копия a
# добавьте 4 в b
# print(a), print(b)
', 'b = a.copy() (или a[:]); b = a лишь повесит на список вторую табличку.', '{"expected": ["[1, 2, 3]", "[1, 2, 3, 4]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 7, 'drop-negatives', 6, 'func', 'Убрать отрицательные', 'Напишите функцию drop_negatives(nums): список без отрицательных чисел (ноль остаётся). Не удаляйте элементы из списка, по которому идёте циклом: подряд идущие отрицательные так пропускаются. Соберите новый список.', 'def drop_negatives(nums):
    result = []
    return result
', 'if x >= 0: result.append(x).', '{"func": "drop_negatives", "tests": [{"args": [[1, -2, 3, -4]], "expected": [1, 3]}, {"args": [[-1, -2, 3]], "expected": [3]}, {"args": [[-5, -6, -7]], "expected": []}, {"args": [[0, 2]], "expected": [0, 2]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 8, 'top3', 0, 'func', 'Три наибольших', 'Напишите функцию top3(nums): список из трёх наибольших элементов по убыванию. Если элементов меньше трёх — верните сколько есть. Исходный список менять нельзя: используйте sorted, а не sort.', 'def top3(nums):
    pass
', 'sorted(nums, reverse=True)[:3] — срез безопасен и для коротких списков.', '{"func": "top3", "tests": [{"args": [[5, 1, 9, 3, 7]], "expected": [9, 7, 5]}, {"args": [[2, 8]], "expected": [8, 2]}, {"args": [[]], "expected": []}, {"args": [[4, 4, 4, 1]], "expected": [4, 4, 4]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 8, 'by-length', 1, 'func', 'По длине слов', 'Напишите функцию by_length(words): новый список слов, отсортированный по длине от коротких к длинным. Слова одной длины остаются в исходном порядке. Используйте параметр key.', 'def by_length(words):
    pass
', 'sorted(words, key=len) — сортировка устойчива: равные по длине не переставляются.', '{"func": "by_length", "tests": [{"args": [["ccc", "a", "bb"]], "expected": ["a", "bb", "ccc"]}, {"args": [["bb", "aa", "c"]], "expected": ["c", "bb", "aa"]}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 8, 'word-lengths', 2, 'func', 'Длины слов', 'Напишите функцию word_lengths(words): список длин слов в том же порядке. Запишите одной строкой — генератором списка.', 'def word_lengths(words):
    return []
', 'return [len(w) for w in words].', '{"func": "word_lengths", "tests": [{"args": [["привет", "мир"]], "expected": [6, 3]}, {"args": [[]], "expected": []}, {"args": [["", "a"]], "expected": [0, 1]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 8, 'even-squares', 3, 'func', 'Квадраты чётных', 'Напишите функцию even_squares(nums): список квадратов только чётных элементов, в исходном порядке. Одним генератором списка с условием.', 'def even_squares(nums):
    return []
', '[x * x for x in nums if x % 2 == 0] — if идёт после for.', '{"func": "even_squares", "tests": [{"args": [[1, 2, 3, 4]], "expected": [4, 16]}, {"args": [[1, 3]], "expected": []}, {"args": [[]], "expected": []}, {"args": [[0, -2]], "expected": [0, 4]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 8, 'all-even', 4, 'func', 'Все ли чётные', 'Напишите функцию all_even(nums): True, если все элементы чётные, иначе False. Для пустого списка — True. Попробуйте встроенную функцию all.', 'def all_even(nums):
    pass
', 'return all(x % 2 == 0 for x in nums).', '{"func": "all_even", "tests": [{"args": [[2, 4, 6]], "expected": true}, {"args": [[2, 3]], "expected": false}, {"args": [[]], "expected": true}, {"args": [[0]], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 8, 'unique-sorted', 5, 'func', 'Без повторов, по порядку', 'Напишите функцию unique_sorted(nums): отсортированный по возрастанию список без повторов: из [3, 1, 3, 2, 1] получится [1, 2, 3]. Множества (set) пока не используйте: отбирайте новые элементы проверкой in.', 'def unique_sorted(nums):
    seen = []
    # если x ещё не в seen — добавить
    return seen
', 'if x not in seen: seen.append(x); в конце seen.sort() и return seen.', '{"func": "unique_sorted", "tests": [{"args": [[3, 1, 3, 2, 1]], "expected": [1, 2, 3]}, {"args": [[]], "expected": []}, {"args": [[5, 5, 5]], "expected": [5]}, {"args": [[2, 1]], "expected": [1, 2]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 8, 'balanced', 6, 'func', 'Скобки в порядке', 'Напишите функцию balanced(s): True, если круглые скобки в строке s расставлены правильно: у каждой «(» есть своя «)» правее, и ни одна «)» не стоит раньше пары. Остальные символы игнорируйте. Используйте список как стопку: append на «(», pop на «)».', 'def balanced(s):
    stack = []
    # for ch in s: ...
    return len(stack) == 0
', 'На «)» сначала проверьте, что стопка не пуста: если пуста, закрывать нечего — сразу return False (иначе pop упадёт с ошибкой).', '{"func": "balanced", "tests": [{"args": ["(())"], "expected": true}, {"args": ["(()"], "expected": false}, {"args": [")("], "expected": false}, {"args": [""], "expected": true}, {"args": ["a(b)c()"], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 8, 'second-largest', 7, 'func', 'Второе по величине', 'Напишите функцию second_largest(nums): второе по величине РАЗНОЕ значение в списке из хотя бы двух различных чисел: для [3, 1, 4, 1, 5] — 4, для [10, 10, 5] — 5.', 'def second_largest(nums):
    pass
', 'Уберите повторы (как в unique_sorted), отсортируйте и возьмите предпоследний: items[-2].', '{"func": "second_largest", "tests": [{"args": [[3, 1, 4, 1, 5]], "expected": 4}, {"args": [[10, 10, 5]], "expected": 5}, {"args": [[1, 2]], "expected": 1}, {"args": [[-1, -5, -3]], "expected": -3}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 9, 'build-dict', 0, 'stdout', 'Первый словарь', 'Дан прайс {«яблоко»: 50, «банан»: 70}. Добавьте «киви» за 90, поднимите цену яблока до 55, удалите банан и напечатайте словарь целиком. Должно получиться {''яблоко'': 55, ''киви'': 90}.', 'prices = {"яблоко": 50, "банан": 70}
# добавить, изменить, удалить, print
', 'prices["киви"] = 90; prices["яблоко"] = 55; del prices["банан"]; print(prices).', '{"expected": ["{''яблоко'': 55, ''киви'': 90}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 9, 'price-of', 1, 'func', 'Цена товара', 'Напишите функцию price_of(prices, name): цена товара name из словаря prices, а если такого товара нет — 0. Программа не должна падать на неизвестном товаре.', 'def price_of(prices, name):
    pass
', 'prices.get(name, 0) — второй аргумент и есть значение по умолчанию.', '{"func": "price_of", "tests": [{"args": [{"яблоко": 50}, "яблоко"], "expected": 50}, {"args": [{"яблоко": 50}, "киви"], "expected": 0}, {"args": [{}, "хлеб"], "expected": 0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 9, 'with-item', 2, 'func', 'Словарь с новой парой', 'Напишите функцию with_item(d, key, value): новый словарь — копия d с добавленной (или заменённой) парой key: value. Исходный словарь d менять нельзя.', 'def with_item(d, key, value):
    result = d.copy()
    return result
', 'Скопируйте словарь, затем присвойте result[key] = value и верните result.', '{"func": "with_item", "tests": [{"args": [{"a": 1}, "b", 2], "expected": {"a": 1, "b": 2}}, {"args": [{"a": 1}, "a", 5], "expected": {"a": 5}}, {"args": [{}, "x", 0], "expected": {"x": 0}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 9, 'count-words', 3, 'func', 'Частоты слов', 'Напишите функцию count_words(words): словарь «слово → сколько раз оно встретилось в списке». Используйте шаблон counts.get(word, 0) + 1.', 'def count_words(words):
    counts = {}
    return counts
', 'for w in words: counts[w] = counts.get(w, 0) + 1.', '{"func": "count_words", "tests": [{"args": [["да", "нет", "да"]], "expected": {"да": 2, "нет": 1}}, {"args": [[]], "expected": {}}, {"args": [["a", "a", "a"]], "expected": {"a": 3}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 9, 'total-price', 4, 'func', 'Стоимость корзины', 'Напишите функцию total_price(prices, cart): prices — цены товаров, cart — словарь «товар → количество штук». Верните общую стоимость. Товары, которых нет в прайсе, не стоят ничего.', 'def total_price(prices, cart):
    total = 0
    # for name, qty in cart.items(): ...
    return total
', 'total += prices.get(name, 0) * qty на каждой паре из cart.items().', '{"func": "total_price", "tests": [{"args": [{"a": 10, "b": 5}, {"a": 2, "b": 3}], "expected": 35}, {"args": [{"a": 10}, {"zzz": 4}], "expected": 0}, {"args": [{"a": 10}, {}], "expected": 0}, {"args": [{"a": 1, "b": 2}, {"a": 1, "b": 1, "zzz": 9}], "expected": 3}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 9, 'word-lengths-dict', 5, 'func', 'Слово → длина', 'Напишите функцию length_map(words): словарь, где ключ — слово из списка, а значение — его длина.', 'def length_map(words):
    result = {}
    return result
', 'result[word] = len(word) на каждом витке цикла.', '{"func": "length_map", "tests": [{"args": [["привет", "мир"]], "expected": {"мир": 3, "привет": 6}}, {"args": [[]], "expected": {}}, {"args": [["a", "a"]], "expected": {"a": 1}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 9, 'has-value', 6, 'func', 'Есть ли такое значение', 'Напишите функцию has_value(d, value): True, если value встречается среди ЗНАЧЕНИЙ словаря d (а не среди ключей), иначе False.', 'def has_value(d, value):
    pass
', 'Слово in у самого словаря смотрит ключи; значения отдаёт d.values().', '{"func": "has_value", "tests": [{"args": [{"a": 1, "b": 2}, 2], "expected": true}, {"args": [{"a": 1, "b": 2}, "a"], "expected": false}, {"args": [{}, 1], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 9, 'most-expensive', 7, 'func', 'Самый дорогой', 'Напишите функцию most_expensive(prices): название самого дорогого товара в непустом прайсе. Переберите пары циклом по prices.items() и запоминайте лучшую.', 'def most_expensive(prices):
    best_name = None
    best_price = None
    # for name, price in prices.items(): ...
    return best_name
', 'Если best_price is None или price > best_price — обновите обе переменные.', '{"func": "most_expensive", "tests": [{"args": [{"a": 10, "b": 30, "c": 20}], "expected": "b"}, {"args": [{"x": 5}], "expected": "x"}, {"args": [{"a": -3, "b": -1}], "expected": "b"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 10, 'merge', 0, 'func', 'Слить настройки', 'Напишите функцию merge(defaults, custom): новый словарь, в котором есть все пары обоих словарей, а при совпадении ключей побеждает custom. Исходные словари менять нельзя.', 'def merge(defaults, custom):
    pass
', 'defaults | custom — правый словарь перекрывает левый; либо copy + update.', '{"func": "merge", "tests": [{"args": [{"a": 1, "b": 2}, {"b": 20, "c": 30}], "expected": {"a": 1, "b": 20, "c": 30}}, {"args": [{}, {"x": 1}], "expected": {"x": 1}}, {"args": [{"x": 1}, {}], "expected": {"x": 1}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 10, 'to-dict', 1, 'func', 'Словарь из двух списков', 'Напишите функцию to_dict(keys, values): словарь, где i-й ключ связан с i-м значением. Списки одной длины. Воспользуйтесь dict и zip.', 'def to_dict(keys, values):
    pass
', 'return dict(zip(keys, values)).', '{"func": "to_dict", "tests": [{"args": [["a", "b"], [1, 2]], "expected": {"a": 1, "b": 2}}, {"args": [[], []], "expected": {}}, {"args": [["x"], [[1, 2]]], "expected": {"x": [1, 2]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 10, 'invert', 2, 'func', 'Перевернуть словарь', 'Напишите функцию invert(d): словарь, в котором ключи и значения поменялись местами. Значения исходного словаря уникальные строки. Одной записью — генератором словаря.', 'def invert(d):
    return {}
', '{value: key for key, value in d.items()}.', '{"func": "invert", "tests": [{"args": [{"a": "x", "b": "y"}], "expected": {"x": "a", "y": "b"}}, {"args": [{}], "expected": {}}, {"args": [{"one": "1"}], "expected": {"1": "one"}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 10, 'group-by-first', 3, 'func', 'Слова по первой букве', 'Напишите функцию group_by_first(words): словарь, где ключ — первая буква слова, а значение — список слов на эту букву в исходном порядке. Слова непустые.', 'def group_by_first(words):
    groups = {}
    return groups
', 'groups.setdefault(word[0], []).append(word).', '{"func": "group_by_first", "tests": [{"args": [["арбуз", "банан", "абрикос"]], "expected": {"а": ["арбуз", "абрикос"], "б": ["банан"]}}, {"args": [[]], "expected": {}}, {"args": [["ёж"]], "expected": {"ё": ["ёж"]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 10, 'most-common', 4, 'func', 'Самое частое слово', 'Напишите функцию most_common(words): самое частое слово непустого списка. Если таких несколько — то, что встретилось в списке раньше. Посчитайте частоты и найдите максимум по значению.', 'def most_common(words):
    counts = {}
    # посчитать частоты, затем max(counts, key=counts.get)
', 'max(counts, key=counts.get) возвращает ключ с наибольшим значением, а при ничьей — первый.', '{"func": "most_common", "tests": [{"args": [["да", "нет", "да"]], "expected": "да"}, {"args": [["a", "b", "b", "a"]], "expected": "a"}, {"args": [["один"]], "expected": "один"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 10, 'adult-names', 5, 'func', 'Имена взрослых', 'Напишите функцию adult_names(users): users — список словарей {''name'': ..., ''age'': ...}. Верните список имён тех, кому 18 или больше, в исходном порядке.', 'def adult_names(users):
    pass
', '[u[''name''] for u in users if u[''age''] >= 18].', '{"func": "adult_names", "tests": [{"args": [[{"age": 20, "name": "Аня"}, {"age": 15, "name": "Боря"}, {"age": 18, "name": "Вера"}]], "expected": ["Аня", "Вера"]}, {"args": [[]], "expected": []}, {"args": [[{"age": 5, "name": "Гоша"}]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 10, 'sort-by-age', 6, 'func', 'Сортировка по возрасту', 'Напишите функцию sort_by_age(users): список тех же записей {''name'': ..., ''age'': ...}, отсортированный по возрасту от младшего к старшему. Для ключа сортировки определите маленькую функцию-помощник.', 'def get_age(user):
    pass


def sort_by_age(users):
    pass
', 'def get_age(user): return user[''age''] — и sorted(users, key=get_age).', '{"func": "sort_by_age", "tests": [{"args": [[{"age": 30, "name": "А"}, {"age": 20, "name": "Б"}]], "expected": [{"age": 20, "name": "Б"}, {"age": 30, "name": "А"}]}, {"args": [[]], "expected": []}, {"args": [[{"age": 5, "name": "А"}, {"age": 5, "name": "Б"}]], "expected": [{"age": 5, "name": "А"}, {"age": 5, "name": "Б"}]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 10, 'grade-word', 7, 'func', 'Оценка словом', 'Напишите функцию grade_word(grade): 5 → «отлично», 4 → «хорошо», 3 → «удовлетворительно», 2 → «плохо», всё остальное → «неизвестно». Без цепочки if — таблицей соответствий в словаре.', 'def grade_word(grade):
    words = {}
    pass
', 'return words.get(grade, ''неизвестно'') — в словаре words пары 5: ''отлично'' и так далее.', '{"func": "grade_word", "tests": [{"args": [5], "expected": "отлично"}, {"args": [4], "expected": "хорошо"}, {"args": [3], "expected": "удовлетворительно"}, {"args": [2], "expected": "плохо"}, {"args": [7], "expected": "неизвестно"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 11, 'unpack-point', 0, 'stdout', 'Распаковка точки', 'Дан кортеж point с координатами. Распакуйте его в переменные x и y одной строкой и напечатайте их произведение.', 'point = (3, 4)
# x, y = ...
', 'x, y = point — затем print(x * y).', '{"expected": ["12"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 11, 'swap-pair', 1, 'func', 'Поменять местами', 'Напишите функцию swap_pair(p): принимает кортеж из двух элементов и возвращает новый кортеж, где элементы поменялись местами.', 'def swap_pair(p):
    pass
', 'a, b = p; return b, a — запятая в return собирает кортеж.', '{"func": "swap_pair", "tests": [{"args": [{"__tuple__": [1, 2]}], "expected": {"__tuple__": [2, 1]}}, {"args": [{"__tuple__": ["a", "b"]}], "expected": {"__tuple__": ["b", "a"]}}, {"args": [{"__tuple__": [5, 5]}], "expected": {"__tuple__": [5, 5]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 11, 'min-max', 2, 'func', 'Минимум и максимум', 'Напишите функцию min_max(nums): кортеж из наименьшего и наибольшего элементов непустого списка. Вернуть нужно именно кортеж, а не список.', 'def min_max(nums):
    pass
', 'return min(nums), max(nums).', '{"func": "min_max", "tests": [{"args": [[3, 1, 9, 4]], "expected": {"__tuple__": [1, 9]}}, {"args": [[7]], "expected": {"__tuple__": [7, 7]}}, {"args": [[-5, -2]], "expected": {"__tuple__": [-5, -2]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 11, 'div-mod', 3, 'func', 'Деление с остатком', 'Напишите функцию div_mod(a, b): кортеж из целой части и остатка от деления a на b (b не ноль). Без готовой функции divmod: операторы // и %.', 'def div_mod(a, b):
    pass
', 'return a // b, a % b.', '{"func": "div_mod", "tests": [{"args": [17, 5], "expected": {"__tuple__": [3, 2]}}, {"args": [10, 5], "expected": {"__tuple__": [2, 0]}}, {"args": [0, 3], "expected": {"__tuple__": [0, 0]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 11, 'split-first', 4, 'func', 'Голова и хвост', 'Напишите функцию split_first(items): кортеж из первого элемента и списка остальных. Список непустой. Для разбора используйте распаковку со звёздочкой.', 'def split_first(items):
    pass
', 'first, *rest = items; return first, rest.', '{"func": "split_first", "tests": [{"args": [[1, 2, 3]], "expected": {"__tuple__": [1, [2, 3]]}}, {"args": [[5]], "expected": {"__tuple__": [5, []]}}, {"args": [["a", "b"]], "expected": {"__tuple__": ["a", ["b"]]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 11, 'lookup-cell', 5, 'func', 'Клетка поля', 'Напишите функцию lookup(cells, row, col). cells — список кортежей (строка, столбец, значение). Постройте словарь, где ключ — кортеж (строка, столбец), и верните значение клетки (row, col) или None, если такой клетки нет.', 'def lookup(cells, row, col):
    field = {}
    # for r, c, value in cells: ...
    return None
', 'field[(r, c)] = value при построении, затем field.get((row, col)).', '{"func": "lookup", "tests": [{"args": [[{"__tuple__": [0, 0, "X"]}, {"__tuple__": [1, 2, "O"]}], 1, 2], "expected": "O"}, {"args": [[{"__tuple__": [0, 0, "X"]}], 5, 5], "expected": null}, {"args": [[], 0, 0], "expected": null}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 11, 'sort-people', 6, 'func', 'Старшие вперёд', 'Напишите функцию sort_people(people): people — список кортежей (имя, возраст). Верните новый список, отсортированный по возрасту от старшего к младшему, а при равном возрасте — по имени по алфавиту. Ключ сортировки — кортеж (минус возраст, имя).', 'def by_key(person):
    pass


def sort_people(people):
    return sorted(people, key=by_key)
', 'def by_key(person): name, age = person; return -age, name.', '{"func": "sort_people", "tests": [{"args": [[{"__tuple__": ["Аня", 20]}, {"__tuple__": ["Боря", 30]}]], "expected": [{"__tuple__": ["Боря", 30]}, {"__tuple__": ["Аня", 20]}]}, {"args": [[{"__tuple__": ["Вера", 20]}, {"__tuple__": ["Аня", 20]}]], "expected": [{"__tuple__": ["Аня", 20]}, {"__tuple__": ["Вера", 20]}]}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 12, 'counter-class', 0, 'stdout', 'Класс-счётчик', 'Опишите класс Counter: у нового счётчика атрибут value равен 0; метод inc() увеличивает value на 1; метод reset() сбрасывает value в 0. Ничего не печатайте — проверка вызовет ваш класс сама.', 'class Counter:
    pass
', 'В __init__ задайте self.value = 0; в методах меняйте self.value.', '{"driver": "c = Counter()\nc.inc()\nc.inc()\nc.inc()\nprint(c.value)\nc.reset()\nprint(c.value)\nd = Counter()\nprint(d.value)\n", "expected": ["3", "0", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 12, 'rectangle-class', 1, 'stdout', 'Прямоугольник', 'Опишите класс Rectangle(w, h) с методами area() — площадь, perimeter() — периметр и is_square() — True, если стороны равны.', 'class Rectangle:
    def __init__(self, w, h):
        pass
', 'Сохраните self.w и self.h; в методах используйте их.', '{"driver": "r = Rectangle(3, 4)\nprint(r.area())\nprint(r.perimeter())\nprint(r.is_square())\nprint(Rectangle(5, 5).is_square())\n", "expected": ["12", "14", "False", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 12, 'dog-str', 2, 'stdout', 'Собака с описанием', 'Опишите класс Dog(name, age) с методом __str__, который возвращает «Собака Рекс, 5 лет» (имя и возраст подставляются), и методом birthday(), который увеличивает возраст на 1.', 'class Dog:
    def __init__(self, name, age):
        pass
', 'def __str__(self): return f"Собака {self.name}, {self.age} лет".', '{"driver": "d = Dog(\"Рекс\", 5)\nprint(d)\nd.birthday()\nprint(d)\n", "expected": ["Собака Рекс, 5 лет", "Собака Рекс, 6 лет"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 12, 'bank-account', 3, 'stdout', 'Банковский счёт', 'Опишите класс BankAccount(balance=0): атрибут balance; метод deposit(x) пополняет счёт (x должно быть больше 0, иначе ValueError); метод withdraw(x) снимает деньги (x больше 0 и не больше баланса, иначе ValueError).', 'class BankAccount:
    def __init__(self, balance=0):
        pass
', 'В начале каждого метода проверьте условие и сделайте raise ValueError(...), потом меняйте баланс.', '{"driver": "a = BankAccount(100)\na.deposit(50)\nprint(a.balance)\ntry:\n    a.withdraw(500)\nexcept ValueError:\n    print(''недостаточно средств'')\na.withdraw(30)\nprint(a.balance)\ntry:\n    a.deposit(-1)\nexcept ValueError:\n    print(''неверная сумма'')\nprint(BankAccount().balance)\n", "expected": ["150", "недостаточно средств", "120", "неверная сумма", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 12, 'stack-class', 4, 'stdout', 'Свой стек', 'Опишите класс Stack с методами push(x), pop() (снимает и возвращает верхний элемент), peek() (возвращает верхний, не снимая), is_empty() и size(). Хранить элементы нужно в списке внутри объекта.', 'class Stack:
    def __init__(self):
        pass
', 'self._items = [] в __init__; peek — это self._items[-1].', '{"driver": "s = Stack()\nprint(s.is_empty())\ns.push(1)\ns.push(2)\ns.push(3)\nprint(s.size())\nprint(s.peek())\nprint(s.pop())\nprint(s.pop())\nprint(s.size())\nprint(s.is_empty())\n", "expected": ["True", "3", "3", "3", "2", "1", "False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 12, 'best-student', 5, 'stdout', 'Лучший ученик', 'Опишите класс Student(name, grade) и функцию best_student(students): она получает список объектов Student и возвращает ИМЯ ученика с наибольшей оценкой (при равных — того, кто раньше в списке).', 'class Student:
    def __init__(self, name, grade):
        pass


def best_student(students):
    pass
', 'Идите по списку и обновляйте лучшего только при строго большей оценке.', '{"driver": "a = [Student(\"Аня\", 4), Student(\"Боря\", 5), Student(\"Вера\", 5)]\nprint(best_student(a))\nprint(best_student([Student(''Гоша'', 3)]))\n", "expected": ["Боря", "Гоша"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 12, 'team-members', 6, 'stdout', 'Команда без общего списка', 'Опишите класс Team: метод add(name) добавляет участника, метод size() возвращает их число. У каждой команды свой список — не делайте его атрибутом класса.', 'class Team:
    pass
', 'self.members = [] — внутри __init__, чтобы список был у каждого экземпляра свой.', '{"driver": "a = Team()\nb = Team()\na.add(\"х\")\na.add(\"у\")\nprint(a.size(), b.size())\n", "expected": ["2 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 13, 'vector-class', 0, 'stdout', 'Вектор', 'Опишите класс Vector(x, y) с операторами: + (сложение), - (вычитание), * на число (масштабирование), == (равенство по значению) и методом __repr__, который возвращает «Vector(1, 2)». Операторы возвращают НОВЫЕ векторы.', 'class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
', '__add__, __sub__, __mul__, __eq__, __repr__ — каждый возвращает результат, а не меняет self.', '{"driver": "a = Vector(1, 2)\nb = Vector(3, 5)\nprint(a + b)\nprint(b - a)\nprint(a * 3)\nprint(a == Vector(1, 2), a == b)\nprint(a)\n", "expected": ["Vector(4, 7)", "Vector(2, 3)", "Vector(3, 6)", "True False", "Vector(1, 2)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 13, 'money-class', 1, 'stdout', 'Деньги', 'Опишите класс Money(amount): объекты равны, если равны суммы (__eq__); их можно сортировать (__lt__); их можно использовать как ключи словаря (__hash__).', 'class Money:
    def __init__(self, amount):
        self.amount = amount
', '__hash__: return hash(self.amount); __lt__: сравните суммы.', '{"driver": "ms = [Money(5), Money(1), Money(3)]\nprint([m.amount for m in sorted(ms)])\nprint(Money(2) == Money(2))\nd = {Money(2): ''два''}\nprint(Money(2) in d)\nprint(max(ms).amount)\n", "expected": ["[1, 3, 5]", "True", "True", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 13, 'playlist-class', 2, 'stdout', 'Плейлист', 'Опишите класс Playlist(songs): len(p) возвращает число песен, p[i] — песню по номеру, «название in p» проверяет наличие. Пустой плейлист в условии должен считаться ложью.', 'class Playlist:
    def __init__(self, songs):
        self._songs = list(songs)
', '__len__, __getitem__ и __contains__; bool() сам опирается на __len__.', '{"driver": "p = Playlist([\"а\", \"б\", \"в\"])\nprint(len(p))\nprint(p[1])\nprint(\"в\" in p, \"я\" in p)\nprint(bool(p), bool(Playlist([])))\n", "expected": ["3", "б", "True False", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 13, 'temperature-class', 3, 'stdout', 'Температура', 'Опишите класс Temperature(celsius): свойство celsius с проверкой (ниже -273.15 — ValueError, в том числе при создании объекта) и вычисляемое свойство fahrenheit только для чтения: celsius * 9 / 5 + 32.', 'class Temperature:
    def __init__(self, celsius):
        pass
', 'В __init__ присваивайте self.celsius = celsius — так сработает сеттер; хранить в self._celsius.', '{"driver": "t = Temperature(100)\nprint(t.fahrenheit)\nt.celsius = 0\nprint(t.fahrenheit)\ntry:\n    t.celsius = -300\nexcept ValueError:\n    print(''слишком холодно'')\nprint(t.celsius)\ntry:\n    Temperature(-500)\nexcept ValueError:\n    print(''нельзя создать'')\n", "expected": ["212.0", "32.0", "слишком холодно", "0", "нельзя создать"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 13, 'person-from-string', 4, 'stdout', 'Человек из строки', 'Опишите класс Person(name, age) и метод класса from_string(s), который разбирает строку «Аня,20» и возвращает Person (возраст — число). Метод __str__ возвращает «Аня (20)».', 'class Person:
    def __init__(self, name, age):
        pass
', '@classmethod def from_string(cls, s): name, age = s.split('',''); return cls(name, int(age)).', '{"driver": "p = Person.from_string(\"Аня,20\")\nprint(p)\nprint(p.age + 1)\n", "expected": ["Аня (20)", "21"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 13, 'circle-property', 5, 'stdout', 'Круг', 'Опишите класс Circle(radius): свойство radius (больше 0, иначе ValueError) и свойство только для чтения area — 3.14159 * radius ** 2.', 'class Circle:
    def __init__(self, radius):
        pass
', 'Свойство без сеттера нельзя присвоить — Питон сам поднимет AttributeError.', '{"driver": "c = Circle(2)\nprint(round(c.area, 2))\nc.radius = 1\nprint(round(c.area, 2))\ntry:\n    c.radius = -5\nexcept ValueError:\n    print(''радиус должен быть положительным'')\ntry:\n    c.area = 1\nexcept AttributeError:\n    print(''area только для чтения'')\n", "expected": ["12.57", "3.14", "радиус должен быть положительным", "area только для чтения"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 13, 'version-class', 6, 'stdout', 'Версии', 'Опишите класс Version(text): text — строка вида «1.2.10». Версии сравниваются по числам, а не по тексту: 1.2.10 больше 1.2.9. Нужны __lt__, __eq__ и __str__ (возвращает исходную строку).', 'class Version:
    def __init__(self, text):
        self.text = text
', 'Сравнивайте кортежи чисел: tuple(int(p) for p in self.text.split(''.'')); для > Питон сам обратит __lt__.', '{"driver": "vs = [Version(\"1.10.0\"), Version(\"1.2.10\"), Version(\"1.2.9\")]\nprint([str(v) for v in sorted(vs)])\nprint(Version(''2.0'') == Version(''2.0''))\nprint(Version(''1.10'') > Version(''1.9''))\n", "expected": ["[''1.2.9'', ''1.2.10'', ''1.10.0'']", "True", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 14, 'animals-polymorphism', 0, 'stdout', 'Животные', 'Опишите Animal(name) с методом speak() (возвращает «...») и describe() (возвращает «<имя>: <звук>» — звук берётся из speak). Наследники Dog и Cat переопределяют speak: «Гав!» и «Мяу!». describe() переопределять не нужно.', 'class Animal:
    def __init__(self, name):
        pass


class Dog(Animal):
    pass


class Cat(Animal):
    pass
', 'В Animal: describe возвращает f''{self.name}: {self.speak()}'' — self.speak() вызовет версию потомка.', '{"driver": "for a in [Dog(\"Шарик\"), Cat(\"Мурка\"), Animal(\"Нечто\")]:\n    print(a.describe())\n", "expected": ["Шарик: Гав!", "Мурка: Мяу!", "Нечто: ..."]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 14, 'employee-manager', 1, 'stdout', 'Сотрудник и менеджер', 'Опишите Employee(name, salary) с методом pay() (зарплата) и наследника Manager(name, salary, bonus), у которого pay() возвращает зарплату плюс бонус. Используйте super() и в конструкторе, и в pay().', 'class Employee:
    def __init__(self, name, salary):
        pass


class Manager(Employee):
    pass
', 'В Manager: super().__init__(name, salary); self.bonus = bonus; pay: return super().pay() + self.bonus.', '{"driver": "e = Employee(\"Аня\", 100)\nm = Manager(\"Боря\", 200, 50)\nprint(e.pay())\nprint(m.pay())\nprint(m.name, m.bonus)\nprint(isinstance(m, Employee))\n", "expected": ["100", "250", "Боря 50", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 14, 'shapes-abstract', 2, 'stdout', 'Абстрактная фигура', 'Опишите абстрактный класс Shape (модуль abc) с абстрактным методом area(); Circle(r) с площадью 3.14159 * r ** 2 и Rect(w, h); а также функцию total_area(shapes) — сумму площадей. Создать Shape напрямую нельзя.', 'from abc import ABC, abstractmethod


class Shape(ABC):
    pass


def total_area(shapes):
    pass
', '@abstractmethod над def area(self); Circle и Rect наследуют от Shape и реализуют area.', '{"driver": "shapes = [Circle(1), Rect(2, 3)]\nprint(round(total_area(shapes), 2))\ntry:\n    Shape()\nexcept TypeError:\n    print(''нельзя создать'')\nprint(isinstance(Rect(1, 1), Shape))\n", "expected": ["9.14", "нельзя создать", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 14, 'car-composition', 3, 'stdout', 'Автомобиль и двигатель', 'Опишите Engine(power) с методом start() — возвращает «двигатель <мощность> л.с. запущен» — и Car(engine), у которого метод go() возвращает результат engine.start(), к которому добавлено «, поехали». Car хранит двигатель как атрибут (композиция).', 'class Engine:
    def __init__(self, power):
        pass


class Car:
    def __init__(self, engine):
        pass
', 'Car.go: return self.engine.start() + ", поехали".', '{"driver": "car = Car(Engine(150))\nprint(car.go())\ncar.engine = Engine(300)\nprint(car.go())\n", "expected": ["двигатель 150 л.с. запущен, поехали", "двигатель 300 л.с. запущен, поехали"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 14, 'greet-mixin', 4, 'stdout', 'Примесь «поздороваться»', 'Опишите примесь GreetMixin с методом greet(), который возвращает «Привет, я <имя>» (имя берётся из self.name), и классы Person(name) и Robot(name), которые её подмешивают.', 'class GreetMixin:
    pass


class Person(GreetMixin):
    def __init__(self, name):
        pass


class Robot(GreetMixin):
    def __init__(self, name):
        pass
', 'greet — в GreetMixin; Person и Robot лишь задают self.name.', '{"driver": "print(Person(\"Аня\").greet())\nprint(Robot(\"R2\").greet())\n", "expected": ["Привет, я Аня", "Привет, я R2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 14, 'count-dogs', 5, 'stdout', 'Сколько собак', 'Даны классы Animal, Dog(Animal), Puppy(Dog) и Cat(Animal) (уже описаны в проверке). Напишите функцию count_dogs(animals): сколько объектов в списке являются собаками — включая щенков. Используйте isinstance.', 'def count_dogs(animals):
    pass
', 'type(x) is Dog не посчитает щенков; isinstance(x, Dog) — посчитает.', '{"driver": "class Animal: pass\nclass Dog(Animal): pass\nclass Puppy(Dog): pass\nclass Cat(Animal): pass\nzoo = [Dog(), Puppy(), Cat(), Animal(), Dog()]\nprint(count_dogs(zoo))\nprint(count_dogs([]))\n", "expected": ["3", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 14, 'base-repr', 6, 'stdout', 'Универсальный repr', 'Опишите класс Base(x) с методом __repr__, который возвращает «<ИмяКласса>(<x>)» и работает для любых наследников без переопределения: Base(1) -> «Base(1)», а у наследника Child(2) -> «Child(2)».', 'class Base:
    def __init__(self, x):
        pass
', 'return f"{type(self).__name__}({self.x})".', '{"driver": "class Child(Base):\n    pass\n\nprint(Base(1))\nprint(Child(2))\nprint([Child(3), Base(4)])\n", "expected": ["Base(1)", "Child(2)", "[Child(3), Base(4)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 15, 'safe-int', 0, 'func', 'Число или запасное значение', 'Напишите функцию safe_int(text, default=0): переводит строку в целое число, а если это не получается — возвращает default. Используйте try/except ValueError.', 'def safe_int(text, default=0):
    pass
', 'try: return int(text) / except ValueError: return default.', '{"func": "safe_int", "tests": [{"args": ["42"], "expected": 42}, {"args": ["abc"], "expected": 0}, {"args": ["abc", -1], "expected": -1}, {"args": [""], "expected": 0}, {"args": [" 7 "], "expected": 7}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 15, 'safe-divide', 1, 'func', 'Безопасное деление', 'Напишите функцию safe_divide(a, b): a / b, а при делении на ноль — None.', 'def safe_divide(a, b):
    pass
', 'Поймайте именно ZeroDivisionError, остальное пусть падает.', '{"func": "safe_divide", "tests": [{"args": [6, 3], "expected": 2.0}, {"args": [1, 0], "expected": null}, {"args": [0, 5], "expected": 0.0}, {"args": [-9, 3], "expected": -3.0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 15, 'parse-age', 2, 'stdout', 'Возраст с проверкой', 'Напишите функцию parse_age(text): возвращает целый возраст из строки. Если число отрицательное — поднимите ValueError с любым сообщением. Нечисловую строку int() отвергнет сам.', 'def parse_age(text):
    pass
', 'age = int(text); if age < 0: raise ValueError(...); return age.', '{"driver": "print(parse_age(\"20\"))\ntry:\n    parse_age(\"-5\")\nexcept ValueError:\n    print(\"отрицательный\")\ntry:\n    parse_age(\"abc\")\nexcept ValueError:\n    print(\"не число\")\n", "expected": ["20", "отрицательный", "не число"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 15, 'custom-error', 3, 'stdout', 'Своё исключение', 'Опишите исключение NotEnoughMoney (наследник Exception) и функцию withdraw(balance, amount): если amount больше balance — поднимите NotEnoughMoney с сообщением «не хватает <сколько>», иначе верните остаток.', 'class NotEnoughMoney(Exception):
    pass


def withdraw(balance, amount):
    pass
', 'raise NotEnoughMoney(f"не хватает {amount - balance}").', '{"driver": "print(withdraw(100, 30))\ntry:\n    withdraw(100, 150)\nexcept NotEnoughMoney as e:\n    print(e)\nprint(issubclass(NotEnoughMoney, Exception))\n", "expected": ["70", "не хватает 50", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 15, 'first-int', 4, 'func', 'Первое число в списке', 'Напишите функцию first_int(items): items — список строк. Верните первое значение, которое удаётся превратить в целое число (уже как int), или None, если таких нет.', 'def first_int(items):
    pass
', 'В цикле: try: return int(x) / except ValueError: continue; после цикла return None.', '{"func": "first_int", "tests": [{"args": [["а", "б", "12", "7"]], "expected": 12}, {"args": [["x", "y"]], "expected": null}, {"args": [[]], "expected": null}, {"args": [["5"]], "expected": 5}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 15, 'finally-log', 5, 'stdout', 'Журнал и finally', 'Напишите функцию process(items, log): добавьте в список log строку «start»; вычислите и верните список 100 / x для каждого x из items; но если встретится ноль — верните None. В любом случае, даже при ошибке, в конце добавьте в log строку «end» (блок finally).', 'def process(items, log):
    pass
', 'try: return [100 / x for x in items] / except ZeroDivisionError: return None / finally: log.append(''end'').', '{"driver": "log = []\nprint(process([1, 4], log))\nprint(log)\nlog = []\nprint(process([2, 0], log))\nprint(log)\n", "expected": ["[100.0, 25.0]", "[''start'', ''end'']", "None", "[''start'', ''end'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 15, 'raise-from', 6, 'stdout', 'Понятная ошибка', 'Напишите функцию get_port(config): возвращает config["port"], а если ключа нет — поднимает RuntimeError("нет порта") ИЗ исходной ошибки (raise ... from e).', 'def get_port(config):
    pass
', 'try: return config["port"] / except KeyError as e: raise RuntimeError("нет порта") from e.', '{"driver": "print(get_port({\"port\": 8080}))\ntry:\n    get_port({})\nexcept RuntimeError as e:\n    print(e, type(e.__cause__).__name__)\n", "expected": ["8080", "нет порта KeyError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 15, 'eafp-get', 7, 'func', 'EAFP вместо get', 'Напишите функцию get_or_default(d, key, default): значение по ключу или default. Метод get и слово in использовать нельзя — только try/except KeyError.', 'def get_or_default(d, key, default):
    pass
', 'try: return d[key] / except KeyError: return default.', '{"func": "get_or_default", "tests": [{"args": [{"a": 1}, "a", 0], "expected": 1}, {"args": [{"a": 1}, "b", 0], "expected": 0}, {"args": [{}, "x", "нет"], "expected": "нет"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 16, 'write-lines', 0, 'stdout', 'Запись строк в файл', 'Напишите функцию write_lines(path, lines): записывает каждую строку списка в файл по своей строке (кодировка utf-8).', 'def write_lines(path, lines):
    pass
', 'with open(path, ''w'', encoding=''utf-8'') as f: for line in lines: f.write(line + ''\n'').', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''a.txt'')\nwrite_lines(p, [''привет'', ''мир'', ''ещё''])\nprint(open(p, encoding=''utf-8'').read().split(''\\n''))\n", "expected": ["[''привет'', ''мир'', ''ещё'', '''']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 16, 'read-lines', 1, 'stdout', 'Чтение строк', 'Напишите функцию read_lines(path): список строк файла без символов перевода строки.', 'def read_lines(path):
    pass
', 'with open(...) as f: return [line.strip() for line in f] — либо read().splitlines().', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''a.txt'')\nopen(p, ''w'', encoding=''utf-8'').write(''один\\nдва\\nтри\\n'')\nprint(read_lines(p))\n", "expected": ["[''один'', ''два'', ''три'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 16, 'count-words-file', 2, 'stdout', 'Слова в файле', 'Напишите функцию count_words(path): сколько всего слов в файле (слова разделены пробелами и переводами строк).', 'def count_words(path):
    pass
', 'На каждой строке прибавляйте len(line.split()).', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''a.txt'')\nopen(p, ''w'', encoding=''utf-8'').write(''раз два\\nтри четыре пять\\n\\nшесть\\n'')\nprint(count_words(p))\n", "expected": ["6"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 16, 'append-log', 3, 'stdout', 'Журнал', 'Напишите функцию append_log(path, text): дописывает text и перевод строки в конец файла, не затирая предыдущее.', 'def append_log(path, text):
    pass
', 'Режим ''a'' дописывает; ''w'' затёр бы всё.', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''log.txt'')\nappend_log(p, ''старт'')\nappend_log(p, ''работа'')\nappend_log(p, ''финиш'')\nprint(open(p, encoding=''utf-8'').read().splitlines())\n", "expected": ["[''старт'', ''работа'', ''финиш'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 16, 'word-freq-file', 4, 'stdout', 'Частоты слов в файле', 'Напишите функцию word_freq(path): словарь «слово → сколько раз» для слов файла без учёта регистра (приводите к нижнему).', 'def word_freq(path):
    pass
', 'counts[w] = counts.get(w, 0) + 1 для каждого слова line.lower().split().', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''a.txt'')\nopen(p, ''w'', encoding=''utf-8'').write(''Да нет да\\nНЕТ да\\n'')\nprint(sorted(word_freq(p).items()))\n", "expected": ["[(''да'', 3), (''нет'', 2)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 16, 'safe-read', 5, 'stdout', 'Чтение без падения', 'Напишите функцию safe_read(path): текст файла или None, если файла нет (FileNotFoundError).', 'def safe_read(path):
    pass
', 'try: with open(...) as f: return f.read() / except FileNotFoundError: return None.', '{"driver": "import os, tempfile\nd = tempfile.mkdtemp()\np = os.path.join(d, ''a.txt'')\nopen(p, ''w'', encoding=''utf-8'').write(''данные'')\nprint(safe_read(p))\nprint(safe_read(os.path.join(d, ''нет.txt'')))\n", "expected": ["данные", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 16, 'copy-upper', 6, 'stdout', 'Копия заглавными', 'Напишите функцию copy_upper(src, dst): читает файл src и записывает в dst те же строки, но заглавными буквами. Оба файла открывайте одним with.', 'def copy_upper(src, dst):
    pass
', 'with open(src, encoding=''utf-8'') as r, open(dst, ''w'', encoding=''utf-8'') as w: ...', '{"driver": "import os, tempfile\nd = tempfile.mkdtemp()\na, b = os.path.join(d, ''a.txt''), os.path.join(d, ''b.txt'')\nopen(a, ''w'', encoding=''utf-8'').write(''привет\\nмир\\n'')\ncopy_upper(a, b)\nprint(open(b, encoding=''utf-8'').read().splitlines())\n", "expected": ["[''ПРИВЕТ'', ''МИР'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 16, 'longest-line', 7, 'stdout', 'Самая длинная строка', 'Напишите функцию longest_line(path): самая длинная строка файла без перевода строки (при равной длине — первая). Файл не пустой.', 'def longest_line(path):
    pass
', 'Идите по строкам и обновляйте лучшую только при строго большей длине.', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''a.txt'')\nopen(p, ''w'', encoding=''utf-8'').write(''коротко\\nчуть подлиннее\\nсредне\\nодинаково-ок\\n'')\nprint(longest_line(p))\n", "expected": ["чуть подлиннее"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 17, 'file-info', 0, 'func', 'Части пути', 'Напишите функцию file_info(path): кортеж (имя файла, имя без расширения, расширение) для пути-строки. Используйте pathlib. Диск не нужен.', 'from pathlib import Path


def file_info(path):
    pass
', 'p = Path(path); return p.name, p.stem, p.suffix.', '{"func": "file_info", "tests": [{"args": ["data/reports/2024.csv"], "expected": {"__tuple__": ["2024.csv", "2024", ".csv"]}}, {"args": ["notes.txt"], "expected": {"__tuple__": ["notes.txt", "notes", ".txt"]}}, {"args": ["/home/user/archive.tar.gz"], "expected": {"__tuple__": ["archive.tar.gz", "archive.tar", ".gz"]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 17, 'join-path', 1, 'func', 'Склейка пути', 'Напишите функцию join_path(parts): склеивает список частей в путь через pathlib и возвращает его СТРОКОЙ.', 'from pathlib import Path


def join_path(parts):
    pass
', 'str(Path(*parts)) — звёздочка раскладывает список в аргументы.', '{"func": "join_path", "tests": [{"args": [["data", "reports", "a.csv"]], "expected": "data/reports/a.csv"}, {"args": [["x"]], "expected": "x"}, {"args": [["/", "tmp", "f.txt"]], "expected": "/tmp/f.txt"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 17, 'json-roundtrip', 2, 'stdout', 'Сохранить и загрузить JSON', 'Напишите функции save_json(path, data) и load_json(path): сохранение словаря в файл (utf-8, русские буквы без кодов) и чтение обратно.', 'import json


def save_json(path, data):
    pass


def load_json(path):
    pass
', 'json.dump(data, f, ensure_ascii=False) и json.load(f) внутри with open(..., encoding=''utf-8'').', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''d.json'')\ndata = {''имя'': ''Аня'', ''возраст'': 20, ''теги'': [''а'', ''б'']}\nsave_json(p, data)\nprint(load_json(p) == data)\nprint(''Аня'' in open(p, encoding=''utf-8'').read())\n", "expected": ["True", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 17, 'csv-column-sum', 3, 'stdout', 'Сумма столбца CSV', 'Напишите функцию column_sum(path, column): сумма чисел в столбце column CSV-файла с заголовком (значения целые).', 'import csv


def column_sum(path, column):
    pass
', 'csv.DictReader; на каждой строке int(row[column]).', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''t.csv'')\nopen(p, ''w'', encoding=''utf-8'', newline='''').write(''имя,цена,штук\\nчай,100,2\\nкофе,250,1\\nсок,80,5\\n'')\nprint(column_sum(p, ''цена''))\nprint(column_sum(p, ''штук''))\n", "expected": ["430", "8"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 17, 'csv-group-sum', 4, 'stdout', 'Итоги по отделам', 'Напишите функцию sum_by(path, key_col, value_col): словарь «значение из key_col → сумма значений value_col» по CSV с заголовком (value_col — целые числа).', 'import csv


def sum_by(path, key_col, value_col):
    pass
', 'totals[k] = totals.get(k, 0) + int(row[value_col]).', '{"driver": "import os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''t.csv'')\nopen(p, ''w'', encoding=''utf-8'', newline='''').write(''отдел,зарплата\\nИТ,100\\nHR,70\\nИТ,120\\nHR,80\\nКУ,90\\n'')\nprint(sorted(sum_by(p, ''отдел'', ''зарплата'').items()))\n", "expected": ["[(''HR'', 150), (''ИТ'', 220), (''КУ'', 90)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 17, 'csv-write-table', 5, 'stdout', 'Запись таблицы', 'Напишите функцию write_table(path, header, rows): записывает в CSV строку заголовка и затем строки таблицы (utf-8, newline=''''). Затем в проверке файл читается и разбирается.', 'import csv


def write_table(path, header, rows):
    pass
', 'w = csv.writer(f); w.writerow(header); w.writerows(rows).', '{"driver": "import csv, os, tempfile\np = os.path.join(tempfile.mkdtemp(), ''t.csv'')\nwrite_table(p, [''имя'', ''возраст''], [[''Аня'', 20], [''Боря, мл.'', 31]])\nwith open(p, encoding=''utf-8'', newline='''') as f:\n    print(list(csv.reader(f)))\n", "expected": ["[[''имя'', ''возраст''], [''Аня'', ''20''], [''Боря, мл.'', ''31'']]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 17, 'atomic-write', 6, 'stdout', 'Атомарная запись', 'Напишите функцию atomic_write(path, text): сначала запишите текст во временный файл рядом (path + ''.tmp''), затем замените им целевой файл через os.replace. Временного файла после работы остаться не должно.', 'import os


def atomic_write(path, text):
    pass
', 'tmp = path + ''.tmp''; запишите в tmp; os.replace(tmp, path).', '{"driver": "import os, tempfile\nd = tempfile.mkdtemp()\np = os.path.join(d, ''state.txt'')\natomic_write(p, ''первая версия'')\natomic_write(p, ''вторая версия'')\nprint(open(p, encoding=''utf-8'').read())\nprint(sorted(os.listdir(d)))\n", "expected": ["вторая версия", "[''state.txt'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 17, 'list-txt', 7, 'stdout', 'Файлы txt в папке', 'Напишите функцию list_txt(folder): отсортированный список ИМЁН файлов с расширением .txt в папке (без вложенных папок). Используйте pathlib.', 'from pathlib import Path


def list_txt(folder):
    pass
', 'sorted(p.name for p in Path(folder).glob(''*.txt'')) — glob без rglob не заходит во вложенные.', '{"driver": "import tempfile\nfrom pathlib import Path\nd = Path(tempfile.mkdtemp())\nfor name in [''b.txt'', ''a.txt'', ''c.csv'', ''d.TXT.bak'']:\n    (d / name).write_text(''x'', encoding=''utf-8'')\n(d / ''sub'').mkdir()\n(d / ''sub'' / ''z.txt'').write_text(''x'', encoding=''utf-8'')\nprint(list_txt(d))\n", "expected": ["[''a.txt'', ''b.txt'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-repr-point', 0, 'stdout', 'Точка с понятным repr', 'Допишите в класс Point метод __repr__, который возвращает строку вида Point(1, 2) — так, как точку записали бы в коде. Проверка печатает repr точки и список из точки.', 'class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
', 'return f"Point({self.x}, {self.y})". Список показывает элементы через repr.', '{"driver": "p = Point(1, 2)\nprint(repr(p))\nprint([Point(-3, 4)])\n", "expected": ["Point(1, 2)", "[Point(-3, 4)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-str-money', 1, 'stdout', 'Деньги: str и repr', 'Класс Money хранит сумму amount. Для пользователя __str__ должен давать «5.00 ₽» (две цифры после точки), а __repr__ — Money(5). Напишите оба метода.', 'class Money:
    def __init__(self, amount):
        self.amount = amount
', '__str__: f"{self.amount:.2f} ₽"; __repr__: f"Money({self.amount})".', '{"driver": "m = Money(5)\nprint(m)\nprint(repr(m))\nprint(f\"{m}\")\nprint([m])\n", "expected": ["5.00 ₽", "Money(5)", "5.00 ₽", "[Money(5)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-bool-account', 2, 'stdout', 'Пустой счёт — ложь', 'Допишите Account так, чтобы счёт с положительным остатком считался истинным, а с нулевым или отрицательным — ложным (условие if account: должно работать).', 'class Account:
    def __init__(self, balance):
        self.balance = balance
', 'def __bool__(self): return self.balance > 0.', '{"driver": "print(bool(Account(10)))\nprint(bool(Account(0)))\nprint(\"есть\" if Account(5) else \"пусто\")\nprint(bool(Account(-1)))\n", "expected": ["True", "False", "есть", "False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-len-basket', 3, 'stdout', 'Длина корзины', 'В Basket уже есть метод add. Добавьте __len__, чтобы len(basket) возвращало число товаров, а пустая корзина была ложью (без отдельного __bool__).', 'class Basket:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
', 'def __len__(self): return len(self.items). Истинность Питон возьмёт из длины.', '{"driver": "b = Basket()\nprint(len(b), bool(b))\nb.add(\"хлеб\")\nb.add(\"сыр\")\nprint(len(b), bool(b))\n", "expected": ["0 False", "2 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-eq-hash-version', 4, 'stdout', 'Равенство и хеш версий', 'Напишите для Version(major, minor) методы __eq__ и __hash__: версии с одинаковыми числами равны, их можно класть в множество и использовать как ключи. Сравнение с объектом другого типа (например, со строкой) должно просто давать False, а не ошибку.', 'class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor
', 'В __eq__: if not isinstance(other, Version): return NotImplemented. __hash__: hash((self.major, self.minor)).', '{"driver": "a = Version(1, 2)\nb = Version(1, 2)\nc = Version(2, 0)\nprint(a == b, a == c, a != c)\nprint(len({a, b, c}))\nd = {a: \"x\"}\nprint(d[b])\nprint(a == \"1.2\")\n", "expected": ["True False True", "2", "x", "False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-order-version', 5, 'stdout', 'Порядок версий', 'Класс Version уже умеет проверять равенство и использует @total_ordering. Допишите __lt__ так, чтобы версии сравнивались по (major, minor), а сравнение с чужим типом возвращало NotImplemented (тогда Питон сам поднимет TypeError).', 'from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) == (other.major, other.minor)

    # допишите __lt__
', 'if not isinstance(other, Version): return NotImplemented; затем сравните кортежи (major, minor).', '{"driver": "vs = [Version(1, 10), Version(1, 2), Version(0, 9)]\nprint([(v.major, v.minor) for v in sorted(vs)])\nprint(Version(1, 2) < Version(1, 10), Version(1, 2) >= Version(1, 10), max(vs).minor)\ntry:\n    Version(1, 0) < 5\nexcept TypeError:\n    print(\"TypeError\")\n", "expected": ["[(0, 9), (1, 2), (1, 10)]", "True False 10", "TypeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-format-temp', 6, 'stdout', 'Свой формат температуры', 'Напишите Temperature.__format__(spec): спецификация «c» (и пустая) даёт «21.0 °C», спецификация «f» — градусы Фаренгейта с одним знаком («69.8 °F»). Любую другую спецификацию отвергайте ValueError.', 'class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
', 'F = C * 9 / 5 + 32. Форматируйте числа как f"{value:.1f}".', '{"driver": "t = Temperature(21)\nprint(f\"{t:c}\")\nprint(f\"{t:f}\")\nprint(f\"{t}\")\ntry:\n    print(f\"{t:x}\")\nexcept ValueError:\n    print(\"ValueError\")\n", "expected": ["21.0 °C", "69.8 °F", "21.0 °C", "ValueError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-getattr-config', 7, 'stdout', 'Настройки как атрибуты', 'Config хранит словарь в self._data. Допишите __getattr__ так, чтобы config.host возвращало значение ключа «host». Если ключа нет, поднимайте AttributeError (тогда hasattr и getattr с запасным значением работают правильно).', 'class Config:
    def __init__(self, data):
        self._data = dict(data)
', 'try: return self._data[name]; except KeyError: raise AttributeError(name).', '{"driver": "c = Config({\"host\": \"localhost\", \"port\": 8080})\nprint(c.host, c.port)\nprint(hasattr(c, \"user\"))\nprint(getattr(c, \"user\", \"нет\"))\n", "expected": ["localhost 8080", "False", "нет"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 18, 'dm-readonly-id', 8, 'stdout', 'Неизменяемый номер заказа', 'У Order поле id нельзя менять после создания, а total — можно. Напишите __setattr__: первую запись id пропускайте, повторную — отвергайте AttributeError. Остальные атрибуты пишутся как обычно (через super().__setattr__, чтобы не уйти в рекурсию).', 'class Order:
    def __init__(self, id, total):
        self.id = id
        self.total = total
', 'if name == "id" and "id" in self.__dict__: raise AttributeError(...); затем super().__setattr__(name, value).', '{"driver": "o = Order(7, 100)\no.total = 150\nprint(o.id, o.total)\ntry:\n    o.id = 8\nexcept AttributeError:\n    print(\"запрещено\")\nprint(o.id)\n", "expected": ["7 150", "запрещено", "7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-vector-add', 0, 'stdout', 'Сложение и вычитание векторов', 'Допишите в Vector методы __add__ и __sub__: оба возвращают новый вектор, а исходные не меняют.', 'class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
', 'return Vector(self.x + other.x, self.y + other.y) — и так же для вычитания.', '{"driver": "a = Vector(1, 2)\nb = Vector(3, 4)\nprint(a + b)\nprint(b - a)\nprint(a)\n", "expected": ["Vector(4, 6)", "Vector(2, 2)", "Vector(1, 2)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-vector-scalar', 1, 'stdout', 'Умножение на число с обеих сторон', 'Научите Vector умножаться на число и слева, и справа: v * 3 и 3 * v дают один результат. Если второй операнд не число (int или float), метод должен вернуть NotImplemented, чтобы Питон поднял TypeError.', 'class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
', '__mul__: if not isinstance(k, (int, float)): return NotImplemented. А __rmul__ может просто вернуть self * k.', '{"driver": "v = Vector(1, 2)\nprint(v * 3, 3 * v)\nprint(v * 0.5)\ntry:\n    v * \"a\"\nexcept TypeError:\n    print(\"TypeError\")\n", "expected": ["Vector(3, 6) Vector(3, 6)", "Vector(0.5, 1.0)", "TypeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-money-sum', 2, 'stdout', 'Деньги под sum()', 'Money хранит копейки cents. Напишите __add__ (складывает только Money, иначе NotImplemented) и __radd__ так, чтобы sum([Money(150), Money(250)]) работала (sum начинает с нуля).', 'class Money:
    def __init__(self, cents):
        self.cents = cents

    def __repr__(self):
        return f"Money({self.cents})"
', '__radd__(self, other): if other == 0: return self; иначе NotImplemented.', '{"driver": "print(sum([Money(150), Money(250), Money(100)]))\nprint(Money(1) + Money(2))\ntry:\n    Money(1) + 5\nexcept TypeError:\n    print(\"TypeError\")\n", "expected": ["Money(500)", "Money(3)", "TypeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-bag-iadd', 3, 'stdout', 'Оператор += на месте', 'У Bag уже есть __add__ (возвращает новый мешок). Допишите __iadd__ так, чтобы a += other изменял сам объект a (дописывал элементы other) и возвращал его же.', 'class Bag:
    def __init__(self, items):
        self.items = list(items)

    def __add__(self, other):
        return Bag(self.items + other.items)
', 'self.items.extend(other.items); return self.', '{"driver": "a = Bag([1])\nalias = a\na += Bag([2, 3])\nprint(alias is a, a.items)\nb = a + Bag([9])\nprint(a.items, b.items)\n", "expected": ["True [1, 2, 3]", "[1, 2, 3] [1, 2, 3, 9]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-vector-unary', 4, 'stdout', 'Отрицание и длина вектора', 'Допишите Vector: -v возвращает вектор с противоположными координатами, а abs(v) — длину вектора (math.hypot).', 'import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
', '__neg__: Vector(-self.x, -self.y); __abs__: math.hypot(self.x, self.y).', '{"driver": "v = Vector(3, 4)\nprint(-v)\nprint(abs(v))\nprint(abs(Vector(0, 0)) == 0)\n", "expected": ["Vector(-3, -4)", "5.0", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-index-step', 5, 'stdout', 'Объект как индекс', 'Сделайте Step пригодным везде, где нужно целое по природе: индекс списка, срез, hex(), range(). Для этого достаточно одного метода.', 'class Step:
    def __init__(self, n):
        self.n = n
', 'def __index__(self): return self.n.', '{"driver": "items = [\"a\", \"b\", \"c\", \"d\"]\nprint(items[Step(2)])\nprint(hex(Step(255)))\nprint(list(range(Step(3))))\nprint(items[Step(1):Step(3)])\n", "expected": ["c", "0xff", "[0, 1, 2]", "[''b'', ''c'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-matmul', 6, 'stdout', 'Умножение матриц знаком @', 'Допишите __matmul__ для Matrix (хранит список строк rows): строка i результата — сумма произведений строки i левой матрицы на столбец j правой. Результат — новая Matrix.', 'class Matrix:
    def __init__(self, rows):
        self.rows = [list(r) for r in rows]

    def __eq__(self, other):
        return self.rows == other.rows

    def __repr__(self):
        return f"Matrix({self.rows})"
', 'Для каждой строки r и каждого индекса j: sum(r[k] * other.rows[k][j] for k in range(len(r))).', '{"driver": "a = Matrix([[1, 2], [3, 4]])\nb = Matrix([[0, 1], [1, 0]])\nprint(a @ b)\nprint(a @ Matrix([[1, 0], [0, 1]]) == a)\n", "expected": ["Matrix([[2, 1], [4, 3]])", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-url-div', 7, 'stdout', 'Адрес через косую черту', 'Научите Url собираться оператором /: Url("example.com") / "api" / "v1/" даёт «example.com/api/v1» (лишние косые на стыках убираются). Если справа не строка, возвращайте NotImplemented.', 'class Url:
    def __init__(self, base):
        self.base = base

    def __str__(self):
        return self.base
', 'Url(self.base.rstrip("/") + "/" + part.strip("/")).', '{"driver": "u = Url(\"example.com\") / \"api\" / \"v1/\"\nprint(u)\nprint(Url(\"a/\") / \"/b\")\ntry:\n    Url(\"a\") / 5\nexcept TypeError:\n    print(\"TypeError\")\n", "expected": ["example.com/api/v1", "a/b", "TypeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 19, 'ops-perm-flags', 8, 'stdout', 'Флаги прав', 'Perm хранит набор прав в трёх младших битах (4 — чтение, 2 — запись, 1 — запуск). Напишите __or__ (объединение), __and__ (пересечение) и __invert__ (дополнение до семи); каждый возвращает новый Perm.', 'class Perm:
    def __init__(self, bits):
        self.bits = bits

    def __eq__(self, other):
        return self.bits == other.bits

    def __repr__(self):
        return f"Perm({self.bits})"
', 'Perm(self.bits | other.bits), Perm(self.bits & other.bits), Perm(7 ^ self.bits).', '{"driver": "R, W, X = Perm(4), Perm(2), Perm(1)\nrw = R | W\nprint(rw)\nprint((rw & W) == W)\nprint(~rw)\nprint(rw & X)\n", "expected": ["Perm(6)", "True", "Perm(1)", "Perm(0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-playlist', 0, 'stdout', 'Плейлист как последовательность', 'Playlist хранит треки во внутреннем списке _tracks. Допишите __len__ и __getitem__ так, чтобы работали len, индексы (в том числе отрицательные), цикл for, проверка in и reversed — без собственных __iter__ и __contains__.', 'class Playlist:
    def __init__(self, tracks):
        self._tracks = list(tracks)
', '__len__ возвращает len(self._tracks); __getitem__ — self._tracks[index].', '{"driver": "p = Playlist([\"a\", \"b\", \"c\"])\nprint(len(p), p[0], p[-1])\nprint([t.upper() for t in p])\nprint(\"b\" in p, \"z\" in p)\nprint(list(reversed(p)))\n", "expected": ["3 a c", "[''A'', ''B'', ''C'']", "True False", "[''c'', ''b'', ''a'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-slice-type', 1, 'stdout', 'Срез возвращает Deck', 'У Deck уже есть __len__. Напишите __getitem__: при целом индексе он возвращает карту, а при срезе — новый Deck (а не список).', 'class Deck:
    def __init__(self, cards):
        self._cards = list(cards)

    def __len__(self):
        return len(self._cards)

    def __repr__(self):
        return f"Deck({self._cards})"
', 'if isinstance(key, slice): return Deck(self._cards[key]); иначе return self._cards[key].', '{"driver": "d = Deck([\"7\", \"8\", \"9\", \"10\"])\nprint(d[1])\nprint(d[1:3])\nprint(type(d[::2]).__name__, d[::-1])\n", "expected": ["8", "Deck([''8'', ''9''])", "Deck Deck([''10'', ''9'', ''8'', ''7''])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-registry', 2, 'stdout', 'Реестр со строгими ключами', 'Допишите Registry: ключи — только строки (иначе TypeError при записи), чтение по несуществующему ключу даёт KeyError, удаление через del и проверка in тоже должны работать.', 'class Registry:
    def __init__(self):
        self._d = {}
', '__setitem__ проверяет isinstance(key, str); __getitem__, __delitem__ и __contains__ работают с self._d.', '{"driver": "r = Registry()\nr[\"a\"] = 1\nprint(r[\"a\"], \"a\" in r, \"b\" in r)\ntry:\n    r[5] = 2\nexcept TypeError:\n    print(\"TypeError\")\ndel r[\"a\"]\nprint(\"a\" in r)\ntry:\n    r[\"a\"]\nexcept KeyError:\n    print(\"KeyError\")\n", "expected": ["1 True False", "TypeError", "False", "KeyError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-grid', 3, 'stdout', 'Поле с координатами', 'Grid(w, h) хранит клетки в self._cells (список строк, изначально «.»). Напишите __getitem__ и __setitem__ по кортежу (x, y), а также __contains__ для проверки координат. Выход за поле — IndexError.', 'class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self._cells = [["."] * w for _ in range(h)]
', 'x, y = pos; if not (0 <= x < self.w and 0 <= y < self.h): raise IndexError(pos).', '{"driver": "g = Grid(3, 2)\ng[1, 0] = \"#\"\nprint(g[1, 0], g[0, 0])\nprint((2, 1) in g, (3, 0) in g, (0, -1) in g)\ntry:\n    g[3, 0]\nexcept IndexError:\n    print(\"IndexError\")\nprint([\"\".join(r) for r in g._cells])\n", "expected": ["# .", "True False False", "IndexError", "[''.#.'', ''...'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-missing', 4, 'stdout', 'Словарь с __missing__', 'Допишите наследника dict Squares: если ключа n нет, __missing__ вычисляет n * n, сохраняет в словаре и возвращает.', 'class Squares(dict):
    pass
', 'def __missing__(self, key): self[key] = key * key; return self[key].', '{"driver": "s = Squares()\nprint(s[4], s[5])\nprint(sorted(s.items()))\nprint(4 in s, 6 in s)\n", "expected": ["16 25", "[(4, 16), (5, 25)]", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-mapping-abc', 5, 'stdout', 'Отображение без учёта регистра', 'Класс CaseInsensitive наследует Mapping и хранит данные в self._d с ключами в нижнем регистре. Реализуйте __getitem__, __iter__ и __len__: обращение m["A"] и m["a"] даёт одно и то же, а keys, items, get, in и == работают бесплатно.', 'from collections.abc import Mapping


class CaseInsensitive(Mapping):
    def __init__(self, data):
        self._d = {k.lower(): v for k, v in data.items()}
', '__getitem__: self._d[key.lower()]; __iter__: iter(self._d); __len__: len(self._d). Тогда get и in работают через __getitem__.', '{"driver": "m = CaseInsensitive({\"Host\": \"x\", \"PORT\": 80})\nprint(m[\"HOST\"], m.get(\"port\"), len(m))\nprint(sorted(m.items()))\nprint(\"host\" in m, m == {\"host\": \"x\", \"port\": 80})\n", "expected": ["x 80 2", "[(''host'', ''x''), (''port'', 80)]", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-call-counter', 6, 'stdout', 'Счётчик-функция', 'Допишите Counter(start=0, step=1): каждый вызов counter() увеличивает значение на step и возвращает новое. Счётчик должен быть вызываемым и помнить состояние между вызовами.', 'class Counter:
    def __init__(self, start=0, step=1):
        self.value = start
        self.step = step
', 'def __call__(self): self.value += self.step; return self.value.', '{"driver": "c = Counter()\nprint(c(), c(), c())\nd = Counter(10, 5)\nprint(d(), d())\nprint(callable(c), c.value)\n", "expected": ["1 2 3", "15 20", "True 3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-suppress', 7, 'stdout', 'Свой suppress', 'Напишите менеджер контекста Suppress(*types): внутри with он подавляет исключения перечисленных типов (и их потомков), а остальные пропускает дальше.', 'class Suppress:
    def __init__(self, *types):
        self.types = types
', '__enter__ возвращает self; __exit__(self, exc_type, exc, tb): return exc_type is not None and issubclass(exc_type, self.types).', '{"driver": "with Suppress(KeyError):\n    {}[\"x\"]\n    print(\"не дойдём\")\nprint(\"после первого\")\nwith Suppress(KeyError, ValueError):\n    int(\"не число\")\nprint(\"после второго\")\ntry:\n    with Suppress(KeyError):\n        1 / 0\nexcept ZeroDivisionError:\n    print(\"ZeroDivisionError прошёл\")\n", "expected": ["после первого", "после второго", "ZeroDivisionError прошёл"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 20, 'ct-tag-manager', 8, 'stdout', 'Парные теги через contextmanager', 'Напишите менеджер tag(name) на @contextmanager: при входе печатает <name>, при выходе </name> — в том числе когда внутри блока случилась ошибка.', 'from contextlib import contextmanager


', 'print вход; try: yield; finally: print выход.', '{"driver": "with tag(\"b\"):\n    print(\"текст\")\ntry:\n    with tag(\"i\"):\n        raise ValueError\nexcept ValueError:\n    print(\"ошибка\")\n", "expected": ["<b>", "текст", "</b>", "<i>", "</i>", "ошибка"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-fahrenheit', 0, 'stdout', 'Температура: свойство fahrenheit', 'Добавьте в Temperature свойство fahrenheit: чтение даёт градусы Фаренгейта по формуле C * 9 / 5 + 32, а запись пересчитывает и сохраняет значение в celsius.', 'class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
', '@property def fahrenheit(self); @fahrenheit.setter def fahrenheit(self, value): self.celsius = (value - 32) * 5 / 9.', '{"driver": "t = Temperature(100)\nprint(t.fahrenheit)\nt.fahrenheit = 32\nprint(t.celsius)\n", "expected": ["212.0", "0.0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-age-validated', 1, 'stdout', 'Возраст с проверкой', 'Превратите age в свойство: значение должно быть целым и неотрицательным, иначе ValueError. Проверка обязана работать и при создании объекта (в __init__ пишите через self.age), и при последующей записи.', 'class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
', 'Храните число в self._age; сеттер: if not isinstance(value, int) or value < 0: raise ValueError.', '{"driver": "p = Person(\"Ann\", 30)\nprint(p.age)\ntry:\n    p.age = -1\nexcept ValueError:\n    print(\"ValueError\")\ntry:\n    Person(\"Bob\", -5)\nexcept ValueError:\n    print(\"ValueError при создании\")\np.age = 31\nprint(p.age)\n", "expected": ["30", "ValueError", "ValueError при создании", "31"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-readonly-area', 2, 'stdout', 'Только для чтения', 'Добавьте в Rect вычисляемые свойства area (площадь) и perimeter (периметр) без сеттеров: они всегда пересчитываются по w и h, а попытка присвоить area поднимает AttributeError.', 'class Rect:
    def __init__(self, w, h):
        self.w = w
        self.h = h
', '@property def area(self): return self.w * self.h.', '{"driver": "r = Rect(3, 4)\nprint(r.area, r.perimeter)\nr.w = 5\nprint(r.area, r.perimeter)\ntry:\n    r.area = 1\nexcept AttributeError:\n    print(\"AttributeError\")\n", "expected": ["12 14", "20 18", "AttributeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-positive', 3, 'stdout', 'Дескриптор Positive', 'Напишите дескриптор данных Positive: значение должно быть положительным числом, иначе ValueError. Храните его в экземпляре под именем поля (подскажет __set_name__), чтобы у разных объектов значения не смешивались; при обращении через класс возвращайте сам дескриптор.', 'class Positive:
    pass
', '__set_name__(self, owner, name): self.name = name; __set__: obj.__dict__[self.name] = value; __get__: если obj is None — return self.', '{"driver": "class Item:\n    price = Positive()\n    qty = Positive()\n\n    def __init__(self, price, qty):\n        self.price = price\n        self.qty = qty\n\n\ni = Item(5, 2)\nj = Item(7, 3)\nprint(i.price, i.qty, j.price)\ntry:\n    Item(-1, 1)\nexcept ValueError:\n    print(\"ValueError\")\ntry:\n    i.qty = 0\nexcept ValueError:\n    print(\"ValueError qty\")\nprint(type(Item.price).__name__)\n", "expected": ["5 2 7", "ValueError", "ValueError qty", "Positive"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-typed', 4, 'stdout', 'Дескриптор Typed', 'Напишите дескриптор данных Typed(expected_type): при записи проверяет isinstance и поднимает TypeError, если тип не тот. Значения хранятся в экземплярах (в obj.__dict__ под именем поля).', 'class Typed:
    def __init__(self, expected_type):
        self.expected_type = expected_type
', 'В __set__: if not isinstance(value, self.expected_type): raise TypeError(...). __get__: return obj.__dict__[self.name].', '{"driver": "class Person:\n    name = Typed(str)\n    age = Typed(int)\n\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n\np = Person(\"Ann\", 30)\nprint(p.name, p.age)\ntry:\n    Person(\"Bob\", \"x\")\nexcept TypeError:\n    print(\"TypeError\")\ntry:\n    p.age = 3.5\nexcept TypeError:\n    print(\"TypeError float\")\nq = Person(\"Eve\", 20)\nprint(p.name, q.name)\n", "expected": ["Ann 30", "TypeError", "TypeError float", "Ann Eve"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-lazy', 5, 'stdout', 'Ленивый атрибут', 'Напишите дескриптор без данных lazy (применяется как декоратор): при первом обращении вызывает функцию, кладёт результат в obj.__dict__ под тем же именем и возвращает его — дальше функция не запускается. Если обратиться через класс, возвращайте сам дескриптор.', 'class lazy:
    def __init__(self, func):
        self.func = func
', '__set_name__ запомнит имя; в __get__: value = self.func(obj); obj.__dict__[self.name] = value; return value. Метода __set__ быть не должно.', '{"driver": "class Data:\n    calls = 0\n\n    def __init__(self, items):\n        self.items = items\n\n    @lazy\n    def total(self):\n        Data.calls += 1\n        return sum(self.items)\n\n\nd = Data([1, 2, 3])\nprint(d.total, d.total, Data.calls)\nprint(\"total\" in d.__dict__)\ndel d.total\nprint(d.total, Data.calls)\nprint(type(Data.total).__name__)\n", "expected": ["6 6 1", "True", "6 2", "lazy"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-classmethod', 6, 'stdout', 'Свой classmethod', 'Напишите дескриптор MyClassMethod — упрощённый classmethod. В __get__ он возвращает связанный метод, в который первым аргументом подставлен класс (тот, через который обратились, даже если вызвали через наследника или экземпляр).', 'import types


class MyClassMethod:
    def __init__(self, func):
        self.func = func
', 'def __get__(self, obj, owner=None): if owner is None: owner = type(obj); return types.MethodType(self.func, owner).', '{"driver": "class A:\n    @MyClassMethod\n    def make(cls):\n        return cls()\n\n\nclass B(A):\n    pass\n\n\nprint(type(A.make()).__name__)\nprint(type(B.make()).__name__)\nprint(type(B().make()).__name__)\n", "expected": ["A", "B", "B"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-slots-point', 7, 'stdout', 'Слоты для Point', 'Добавьте в Point атрибут __slots__ с полями x и y, чтобы у экземпляров не было __dict__ и нельзя было добавлять новые атрибуты.', 'class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
', '__slots__ = ("x", "y") — в теле класса, до __init__.', '{"driver": "p = Point(1, 2)\nprint(p.x + p.y)\nprint(hasattr(p, \"__dict__\"))\ntry:\n    p.z = 3\nexcept AttributeError:\n    print(\"нельзя\")\n", "expected": ["3", "False", "нельзя"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 21, 'ds-cached-report', 8, 'stdout', 'Кэшируем тяжёлую сумму', 'Report.total считает сумму значений при каждом обращении (счётчик calls растёт). Сделайте так, чтобы сумма вычислялась один раз для экземпляра, не меняя вызов r.total.', 'class Report:
    calls = 0

    def __init__(self, values):
        self.values = values

    @property
    def total(self):
        Report.calls += 1
        return sum(self.values)
', 'from functools import cached_property и заменить @property на @cached_property.', '{"driver": "r = Report([1, 2, 3])\nprint(r.total, r.total, r.total)\nprint(Report.calls)\nprint(Report([5]).total, Report.calls)\n", "expected": ["6 6 6", "1", "5 2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 22, 'countdown-iterator', 0, 'stdout', 'Итератор-отсчёт', 'Опишите класс Countdown(n): итератор (методы __iter__ и __next__), который выдаёт числа от n до 1 и затем останавливается (StopIteration). Для n = 0 — сразу пусто.', 'class Countdown:
    def __init__(self, n):
        pass
', '__iter__ возвращает self; в __next__: если self.n <= 0 — raise StopIteration, иначе уменьшить и вернуть прежнее.', '{"driver": "print(list(Countdown(3)))\nprint(list(Countdown(0)))\nc = Countdown(2)\nprint(list(c), list(c))\nfor x in Countdown(2):\n    print(x)\n", "expected": ["[3, 2, 1]", "[]", "[2, 1] []", "2", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 22, 'repeater-iterable', 1, 'stdout', 'Многоразовый итерируемый', 'Опишите класс Repeater(word, times): его можно перебирать много раз, и каждый раз он выдаёт слово word ровно times раз. __iter__ должен каждый раз возвращать НОВЫЙ итератор.', 'class Repeater:
    def __init__(self, word, times):
        pass
', 'def __iter__(self): return iter([self.word] * self.times) — каждый вызов строит новый итератор.', '{"driver": "r = Repeater(\"а\", 3)\nprint(list(r))\nprint(list(r))\nprint(len(list(Repeater(''б'', 0))))\n", "expected": ["[''а'', ''а'', ''а'']", "[''а'', ''а'', ''а'']", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 22, 'take-n', 2, 'stdout', 'Взять первые n', 'Напишите функцию take(iterator, n): список из первых n элементов итератора (или меньше, если элементов не хватило). Используйте next с запасным значением или цикл по итератору.', 'def take(iterator, n):
    pass
', 'n раз пробуйте next(iterator) внутри try; на StopIteration выходите из цикла.', '{"driver": "print(take(iter(range(10)), 3))\nprint(take(iter([1]), 5))\nit = iter(''abcdef'')\nprint(take(it, 2), take(it, 2))\nprint(take(iter([]), 3))\n", "expected": ["[0, 1, 2]", "[1]", "[''a'', ''b''] [''c'', ''d'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 22, 'first-even', 3, 'func', 'Первое чётное', 'Напишите функцию first_even(nums): первое чётное число в списке или None. Используйте next со значением по умолчанию и генераторное выражение — без цикла и без индексов.', 'def first_even(nums):
    pass
', 'next((x for x in nums if x % 2 == 0), None).', '{"func": "first_even", "tests": [{"args": [[1, 3, 4, 6]], "expected": 4}, {"args": [[1, 3, 5]], "expected": null}, {"args": [[]], "expected": null}, {"args": [[2]], "expected": 2}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 22, 'fib-iterator', 4, 'stdout', 'Бесконечный итератор Фибоначчи', 'Опишите класс Fib: бесконечный итератор, который выдаёт числа Фибоначчи 1, 1, 2, 3, 5, 8, …', 'class Fib:
    def __init__(self):
        pass
', 'Храните два числа a, b; в __next__: a, b = b, a + b; return a (стартуйте с a=0, b=1).', '{"driver": "res = []\nfor i, x in enumerate(Fib()):\n    if i == 10:\n        break\n    res.append(x)\nprint(res)\nit = iter(Fib())\nprint(next(it), next(it), next(it))\n", "expected": ["[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]", "1 1 2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 22, 'evens-iterator', 5, 'stdout', 'Чётные до предела', 'Опишите класс Evens(limit): итератор чётных неотрицательных чисел 0, 2, 4, … строго меньше limit.', 'class Evens:
    def __init__(self, limit):
        pass
', 'Храните текущее число; в __next__: если оно >= limit — StopIteration, иначе вернуть и прибавить 2.', '{"driver": "print(list(Evens(9)))\nprint(list(Evens(1)))\nprint(list(Evens(0)))\nprint(sum(Evens(11)))\n", "expected": ["[0, 2, 4, 6, 8]", "[0]", "[]", "30"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 22, 'count-items', 6, 'stdout', 'Сколько элементов', 'Напишите функцию count_items(iterable): сколько элементов выдаёт любой итерируемый объект (список, рэндж, генератор, файл). len использовать нельзя — работайте циклом.', 'def count_items(iterable):
    pass
', 'n = 0; for _ in iterable: n += 1; return n.', '{"driver": "print(count_items([1, 2, 3]))\nprint(count_items(range(5)))\nprint(count_items(c for c in ''привет'' if c != ''в''))\nprint(count_items(iter([])))\n", "expected": ["3", "5", "5", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 23, 'countdown-gen', 0, 'stdout', 'Генератор отсчёта', 'Напишите генераторную функцию countdown(n): отдаёт числа от n до 1 (для n = 0 — ничего). Используйте yield.', 'def countdown(n):
    pass
', 'while n > 0: yield n; n -= 1.', '{"driver": "print(list(countdown(3)))\nprint(list(countdown(0)))\ng = countdown(2)\nprint(next(g), next(g))\n", "expected": ["[3, 2, 1]", "[]", "2 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 23, 'fib-gen', 1, 'stdout', 'Генератор Фибоначчи', 'Напишите бесконечный генератор fib_gen(): числа Фибоначчи 0, 1, 1, 2, 3, 5, …', 'def fib_gen():
    pass
', 'a, b = 0, 1; while True: yield a; a, b = b, a + b.', '{"driver": "res = []\nfor i, x in enumerate(fib_gen()):\n    if i == 10:\n        break\n    res.append(x)\nprint(res)\n", "expected": ["[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 23, 'evens-gen', 2, 'stdout', 'Чётные до предела', 'Напишите генератор evens(limit): чётные неотрицательные числа строго меньше limit.', 'def evens(limit):
    pass
', 'for x in range(0, limit, 2): yield x.', '{"driver": "print(list(evens(9)))\nprint(list(evens(0)))\nprint(sum(evens(11)))\n", "expected": ["[0, 2, 4, 6, 8]", "[]", "30"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 23, 'chunks-gen', 3, 'stdout', 'Пачки', 'Напишите генератор chunks(items, n): отдаёт список по частям по n элементов (последняя может быть короче).', 'def chunks(items, n):
    pass
', 'for i in range(0, len(items), n): yield items[i:i + n].', '{"driver": "print(list(chunks([1, 2, 3, 4, 5], 2)))\nprint(list(chunks([], 3)))\nprint(list(chunks(''abcdef'', 3)))\n", "expected": ["[[1, 2], [3, 4], [5]]", "[]", "[''abc'', ''def'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 23, 'flatten-gen', 4, 'stdout', 'Выпрямить вложенные списки', 'Напишите генератор flatten(items): отдаёт все не-списковые элементы произвольно вложенных списков по порядку. Используйте yield from и рекурсию.', 'def flatten(items):
    pass
', 'if isinstance(x, list): yield from flatten(x); else: yield x.', '{"driver": "print(list(flatten([1, [2, [3, [4]], 5], [], 6])))\nprint(list(flatten([])))\nprint(list(flatten([[[''а'']]])))\n", "expected": ["[1, 2, 3, 4, 5, 6]", "[]", "[''а'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 23, 'read-numbers', 5, 'stdout', 'Числа из строк', 'Напишите генератор read_numbers(lines): из последовательности строк отдаёт целые числа. Пустые строки и строки, которые не являются числом (после strip состоят не только из цифр), пропускаются.', 'def read_numbers(lines):
    pass
', 's = line.strip(); if s.isdigit(): yield int(s).', '{"driver": "print(list(read_numbers([''1'', '''', '' 2 '', ''x'', ''3'', ''4a''])))\ng = read_numbers(iter([''10'', ''20'']))\nprint(next(g), next(g))\n", "expected": ["[1, 2, 3]", "10 20"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 23, 'running-sum', 6, 'stdout', 'Накопленные суммы', 'Напишите генератор running_sum(nums): после каждого элемента отдаёт сумму всех элементов до него включительно: для 1, 2, 3, 4 — 1, 3, 6, 10.', 'def running_sum(nums):
    pass
', 'total = 0; for x in nums: total += x; yield total.', '{"driver": "print(list(running_sum([1, 2, 3, 4])))\nprint(list(running_sum([])))\nprint(list(running_sum(range(1, 6))))\n", "expected": ["[1, 3, 6, 10]", "[]", "[1, 3, 6, 10, 15]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 23, 'tag-manager', 7, 'stdout', 'Свой менеджер контекста', 'С помощью декоратора contextmanager из contextlib опишите менеджер tag(name): при входе печатает «<name>», при выходе (даже при ошибке) — «</name>».', 'from contextlib import contextmanager


def tag(name):
    pass
', '@contextmanager; print вход; try: yield; finally: print выход.', '{"driver": "with tag(''p''):\n    print(''текст'')\ntry:\n    with tag(''b''):\n        raise ValueError(''сбой'')\nexcept ValueError:\n    print(''поймали'')\n", "expected": ["<p>", "текст", "</p>", "<b>", "</b>", "поймали"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-averager', 0, 'stdout', 'Скользящее среднее', 'Напишите корутину averager(): она принимает числа через send и после каждого отдаёт текущее среднее всех присланных чисел. Первый next возвращает None (чисел ещё нет).', 'def averager():
    pass
', 'Заведите total, count, average = None; в цикле: x = yield average; обновите total, count и average.', '{"driver": "avg = averager()\nprint(next(avg))\nprint(avg.send(10), avg.send(20), avg.send(30))\n", "expected": ["None", "10.0 15.0 20.0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-primed', 1, 'stdout', 'Декоратор primed', 'Напишите декоратор primed: он оборачивает генераторную функцию так, что вызов возвращает уже «заведённый» генератор (первый next уже сделан), и можно сразу делать send.', 'def primed(func):
    pass
', 'Внутри обёртки: gen = func(*args, **kwargs); next(gen); return gen.', '{"driver": "import inspect\n\n\n@primed\ndef collector():\n    items = []\n    while True:\n        item = yield items\n        items.append(item)\n\n\nc = collector()\nprint(c.send(\"a\"))\nprint(c.send(\"b\"))\nprint(inspect.getgeneratorstate(c))\n", "expected": ["[''a'']", "[''a'', ''b'']", "GEN_SUSPENDED"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-throw-reset', 2, 'stdout', 'Счётчик со сбросом через throw', 'Напишите генератор counter(): отдаёт 0, 1, 2, … Если снаружи вбросили ValueError (gen.throw(ValueError)), счётчик сбрасывается в 0 и продолжает с нуля. Другие исключения не перехватывайте.', 'def counter():
    pass
', 'while True: try: yield n; n += 1; except ValueError: n = 0.', '{"driver": "c = counter()\nprint(next(c), next(c), next(c))\nprint(c.throw(ValueError))\nprint(next(c))\ntry:\n    c.throw(KeyError)\nexcept KeyError:\n    print(\"KeyError пролетел\")\n", "expected": ["0 1 2", "0", "1", "KeyError пролетел"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-close-cleanup', 3, 'stdout', 'Уборка при close', 'Напишите генератор lines(items): при первом запросе печатает «открыто», затем отдаёт элементы по одному, а при любом завершении — в том числе досрочном через close() — печатает «закрыто».', 'def lines(items):
    pass
', 'print("открыто"); try: for item in items: yield item; finally: print("закрыто").', '{"driver": "g = lines([\"a\", \"b\", \"c\"])\nprint(next(g))\ng.close()\nprint(\"после close\")\nfor x in lines([\"z\"]):\n    print(x)\n", "expected": ["открыто", "a", "закрыто", "после close", "открыто", "z", "закрыто"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-return-value', 4, 'stdout', 'Генератор с итогом', 'Напишите генератор summing(items): он отдаёт каждый элемент как есть, а в конце возвращает (return) сумму всех элементов — она окажется в StopIteration.value.', 'def summing(items):
    pass
', 'total = 0; for x in items: total += x; yield x; в конце return total.', '{"driver": "g = summing([1, 2, 3])\nitems = []\ntry:\n    while True:\n        items.append(next(g))\nexcept StopIteration as e:\n    print(items, e.value)\n", "expected": ["[1, 2, 3] 6"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-chain-sum', 5, 'stdout', 'Делегирование через yield from', 'Генератор summing уже написан (отдаёт элементы и возвращает сумму). Напишите chain_sum(a, b): через yield from отдаёт элементы a, затем b, а возвращает общую сумму обоих списков.', 'def summing(items):
    total = 0
    for x in items:
        total += x
        yield x
    return total


def chain_sum(a, b):
    pass
', 'first = yield from summing(a); second = yield from summing(b); return first + second.', '{"driver": "g = chain_sum([1, 2], [3, 4])\nitems = []\ntry:\n    while True:\n        items.append(next(g))\nexcept StopIteration as e:\n    print(items, e.value)\n", "expected": ["[1, 2, 3, 4] 10"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-flatten', 6, 'stdout', 'Разворачиваем вложенные списки', 'Напишите генератор flatten(items): рекурсивно отдаёт все элементы вложенных списков и кортежей по порядку. Строки считайте листьями (не разбирайте на символы). Используйте yield from.', 'def flatten(items):
    pass
', 'for x in items: if isinstance(x, (list, tuple)): yield from flatten(x); else: yield x.', '{"driver": "print(list(flatten([1, [2, [3, 4]], \"ab\", [[5]], (6, 7)])))\nprint(list(flatten([])))\n", "expected": ["[1, 2, 3, 4, ''ab'', 5, 6, 7]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-filter-stage', 7, 'stdout', 'Стадия конвейера', 'Напишите корутину keep(pred, target): она принимает значения через send и передаёт в target.send(...) только те, для которых pred(значение) истинно. Первый next (заведение корутины) сделает проверка.', 'def keep(pred, target):
    pass
', 'while True: item = yield; if pred(item): target.send(item).', '{"driver": "got = []\n\n\ndef sink():\n    while True:\n        got.append((yield))\n\n\ns = sink()\nnext(s)\nf = keep(lambda x: x % 2 == 0, s)\nnext(f)\nfor i in range(7):\n    f.send(i)\nprint(got)\n", "expected": ["[0, 2, 4, 6]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 24, 'gx-round-robin', 8, 'stdout', 'Планировщик по кругу', 'Напишите run(tasks): список генераторов-задач выполняется по кругу — на каждом шаге берётся первая задача, запрашивается одно значение (next), оно добавляется в результат, а незавершённая задача уходит в конец очереди. Завершившаяся (StopIteration) убирается. Верните список полученных значений.', 'from collections import deque


def run(tasks):
    pass
', 'queue = deque(tasks); пока queue: task = queue.popleft(); try: out.append(next(task)); queue.append(task); except StopIteration: pass.', '{"driver": "def worker(name, n):\n    for i in range(n):\n        yield f\"{name}{i}\"\n\n\nprint(run([worker(\"a\", 2), worker(\"b\", 3), worker(\"c\", 1)]))\nprint(run([]))\n", "expected": ["[''a0'', ''b0'', ''c0'', ''a1'', ''b1'', ''b2'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 25, 'apply-all', 0, 'stdout', 'Применить все функции', 'Напишите функцию apply_all(funcs, x): список результатов вызова каждой функции из funcs от x, в том же порядке.', 'def apply_all(funcs, x):
    pass
', 'Функции — обычные значения: [f(x) for f in funcs].', '{"driver": "print(apply_all([abs, float, str], -3))\nprint(apply_all([], 5))\nprint(apply_all([str.upper, str.title, len], ''привет мир''))\n", "expected": ["[3, -3.0, ''-3'']", "[]", "[''ПРИВЕТ МИР'', ''Привет Мир'', 10]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 25, 'sort-length-desc', 1, 'func', 'Самые длинные вперёд', 'Напишите функцию by_length_desc(words): слова от самых длинных к самым коротким; слова одной длины остаются в исходном порядке. Используйте sorted и lambda.', 'def by_length_desc(words):
    pass
', 'sorted(words, key=lambda w: len(w), reverse=True) — сортировка устойчива и с reverse.', '{"func": "by_length_desc", "tests": [{"args": [["bb", "a", "ccc"]], "expected": ["ccc", "bb", "a"]}, {"args": [["aa", "b", "cc"]], "expected": ["aa", "cc", "b"]}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 25, 'oldest-user', 2, 'func', 'Самый старший', 'Напишите функцию oldest(users): users — список словарей {''name'': ..., ''age'': ...}. Верните имя самого старшего. Список не пустой. Используйте max с параметром key.', 'def oldest(users):
    pass
', 'max(users, key=lambda u: u[''age''])[''name''].', '{"func": "oldest", "tests": [{"args": [[{"age": 31, "name": "Аня"}, {"age": 25, "name": "Боря"}]], "expected": "Аня"}, {"args": [[{"age": 5, "name": "Вера"}]], "expected": "Вера"}, {"args": [[{"age": 20, "name": "А"}, {"age": 40, "name": "Б"}, {"age": 30, "name": "В"}]], "expected": "Б"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 25, 'even-squares-map', 3, 'func', 'map и filter', 'Напишите функцию even_squares(nums): СПИСОК квадратов чётных чисел, в исходном порядке. Решите через filter и map (с lambda), а затем оберните результат в list.', 'def even_squares(nums):
    pass
', 'list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums))).', '{"func": "even_squares", "tests": [{"args": [[1, 2, 3, 4]], "expected": [4, 16]}, {"args": [[1, 3]], "expected": []}, {"args": [[]], "expected": []}, {"args": [[0, -2, 5]], "expected": [0, 4]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 25, 'compose-fn', 4, 'stdout', 'Композиция функций', 'Напишите функцию compose(f, g): возвращает новую функцию, которая сначала применяет g, затем f к результату: compose(f, g)(x) == f(g(x)).', 'def compose(f, g):
    pass
', 'return lambda x: f(g(x)).', '{"driver": "clean = compose(str.strip, str.lower)\nprint(repr(clean(''  АБВ '')))\ninc_then_double = compose(lambda x: x * 2, lambda x: x + 1)\nprint(inc_then_double(5))\nprint(compose(len, str)(12345))\n", "expected": ["''абв''", "12", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 25, 'count-args', 5, 'stdout', 'Сколько аргументов', 'Напишите функцию describe(*args, **kwargs): возвращает строку вида «2 позиционных, 1 именованных» — сколько позиционных и сколько именованных аргументов получено.', 'def describe(*args, **kwargs):
    pass
', 'return f"{len(args)} позиционных, {len(kwargs)} именованных".', '{"driver": "print(describe(1, 2, a=3))\nprint(describe())\nprint(describe(''x'', ''y'', ''z''))\nprint(describe(k=1, m=2))\nprint(describe(*[1, 2, 3], **{''q'': 1}))\n", "expected": ["2 позиционных, 1 именованных", "0 позиционных, 0 именованных", "3 позиционных, 0 именованных", "0 позиционных, 2 именованных", "3 позиционных, 1 именованных"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 25, 'pure-append', 6, 'stdout', 'Чистое добавление', 'Напишите чистую функцию pure_append(items, x): возвращает НОВЫЙ список с добавленным x, не меняя исходный.', 'def pure_append(items, x):
    pass
', 'return items + [x] — оператор плюс создаёт новый список.', '{"driver": "a = [1, 2]\nb = pure_append(a, 3)\nprint(a, b)\nprint(a is b)\nprint(pure_append([], ''x''))\n", "expected": ["[1, 2] [1, 2, 3]", "False", "[''x'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 25, 'product-reduce', 7, 'func', 'Произведение через reduce', 'Напишите функцию product(nums): произведение всех чисел списка, для пустого списка — 1. Используйте reduce из functools с начальным значением.', 'from functools import reduce


def product(nums):
    pass
', 'reduce(lambda acc, x: acc * x, nums, 1) — единица как начальное значение даёт 1 для пустого списка.', '{"func": "product", "tests": [{"args": [[1, 2, 3, 4]], "expected": 24}, {"args": [[]], "expected": 1}, {"args": [[5]], "expected": 5}, {"args": [[2, -3]], "expected": -6}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 26, 'make-multiplier', 0, 'stdout', 'Фабрика умножителей', 'Напишите функцию make_multiplier(n): возвращает функцию, умножающую свой аргумент на n.', 'def make_multiplier(n):
    pass
', 'Опишите внутри def mul(x): return x * n и верните mul.', '{"driver": "triple = make_multiplier(3)\nfive = make_multiplier(5)\nprint(triple(10), five(10), triple(0))\nprint(make_multiplier(-1)(7))\n", "expected": ["30 50 0", "-7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 26, 'make-counter', 1, 'stdout', 'Счётчик с состоянием', 'Напишите функцию make_counter(start=0): возвращает функцию, каждый вызов которой возвращает следующее число, начиная с start + 1. Состояние хранится в замыкании (nonlocal); у каждого счётчика своё.', 'def make_counter(start=0):
    pass
', 'count = start; внутри inner: nonlocal count; count += 1; return count.', '{"driver": "a = make_counter()\nb = make_counter(10)\nprint(a(), a(), a())\nprint(b(), b())\nprint(a())\n", "expected": ["1 2 3", "11 12", "4"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 26, 'make-accumulator', 2, 'stdout', 'Накопитель', 'Напишите функцию make_accumulator(): возвращает функцию, которая принимает число, прибавляет его к накопленной сумме (в замыкании) и возвращает текущую сумму.', 'def make_accumulator():
    pass
', 'total = 0 во внешней функции; nonlocal total во внутренней.', '{"driver": "acc = make_accumulator()\nprint(acc(10), acc(5), acc(-3))\nother = make_accumulator()\nprint(other(1), acc(0))\n", "expected": ["10 15 12", "1 12"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 26, 'count-calls-deco', 3, 'stdout', 'Декоратор-счётчик вызовов', 'Напишите декоратор count_calls: после каждого вызова декорированной функции атрибут wrapper.calls увеличивается на единицу (начиная с 0). Результат и аргументы функции должны сохраняться.', 'def count_calls(func):
    pass
', 'Заведите wrapper.calls = 0 после описания wrapper; внутри wrapper: wrapper.calls += 1.', '{"driver": "@count_calls\ndef add(a, b=0):\n    return a + b\n\nprint(add.calls)\nprint(add(1, b=2), add(5))\nprint(add.calls)\n", "expected": ["0", "3 5", "2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 26, 'logged-deco', 4, 'stdout', 'Декоратор с журналом', 'Напишите декоратор logged: перед каждым вызовом печатает «вызов <имя функции>», затем вызывает функцию и возвращает её результат. Имя и докстринг функции должны сохраняться (functools.wraps).', 'from functools import wraps


def logged(func):
    pass
', '@wraps(func) над wrapper(*args, **kwargs); print(f''вызов {func.__name__}''); return func(*args, **kwargs).', '{"driver": "@logged\ndef greet(name):\n    \"\"\"Поздороваться.\"\"\"\n    return f''Привет, {name}!''\n\nprint(greet(''Аня''))\nprint(greet.__name__, greet.__doc__)\n", "expected": ["вызов greet", "Привет, Аня!", "greet Поздороваться."]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 26, 'repeat-deco', 5, 'stdout', 'Декоратор с параметром', 'Напишите декоратор repeat(times): вызывает функцию times раз подряд и возвращает результат последнего вызова.', 'def repeat(times):
    pass
', 'Три уровня: repeat(times) -> decorator(func) -> wrapper(*args, **kwargs).', '{"driver": "@repeat(3)\ndef hello(name):\n    print(''привет,'', name)\n    return name.upper()\n\nprint(hello(''аня''))\n", "expected": ["привет, аня", "привет, аня", "привет, аня", "АНЯ"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 26, 'memoize-deco', 6, 'stdout', 'Кеширование', 'Напишите декоратор memoize: запоминает результаты функции одного аргумента в словаре; повторный вызов с тем же аргументом не вызывает функцию заново.', 'def memoize(func):
    pass
', 'cache = {} в декораторе; в wrapper: if n not in cache: cache[n] = func(n); return cache[n].', '{"driver": "calls = []\n\n@memoize\ndef slow(n):\n    calls.append(n)\n    return n * n\n\nprint(slow(4), slow(4), slow(5), slow(4))\nprint(calls)\n", "expected": ["16 16 25 16", "[4, 5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 26, 'positive-args-deco', 7, 'stdout', 'Только положительные', 'Напишите декоратор positive_only: если хотя бы один позиционный аргумент меньше нуля, поднимает ValueError, иначе вызывает функцию и возвращает результат.', 'def positive_only(func):
    pass
', 'В wrapper: for a in args: if a < 0: raise ValueError(...).', '{"driver": "@positive_only\ndef total(*nums):\n    return sum(nums)\n\nprint(total(1, 2, 3))\ntry:\n    total(1, -2)\nexcept ValueError:\n    print(''отрицательное'')\nprint(total())\n", "expected": ["6", "отрицательное", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 27, 'merge-dicts-reduce', 0, 'func', 'Слить много словарей', 'Напишите функцию merge_all(dicts): сливает список словарей в один; при совпадении ключей побеждает словарь, который стоит позже в списке. Используйте reduce (начальное значение — пустой словарь).', 'from functools import reduce


def merge_all(dicts):
    pass
', 'reduce(lambda acc, d: {**acc, **d}, dicts, {}).', '{"func": "merge_all", "tests": [{"args": [[{"a": 1}, {"b": 2}, {"a": 3}]], "expected": {"a": 3, "b": 2}}, {"args": [[]], "expected": {}}, {"args": [[{"x": 1}]], "expected": {"x": 1}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 27, 'int-parser-partial', 1, 'stdout', 'Парсер чисел', 'Напишите функцию int_parser(base): возвращает функцию, которая переводит строку в целое по основанию base. Используйте functools.partial.', 'from functools import partial


def int_parser(base):
    pass
', 'return partial(int, base=base).', '{"driver": "from_bin = int_parser(2)\nfrom_hex = int_parser(16)\nprint(from_bin(''1010''), from_hex(''ff''), from_hex(''10''))\nprint(list(map(int_parser(8), [''7'', ''10'', ''17''])))\n", "expected": ["10 255 16", "[7, 8, 15]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 27, 'fib-cache', 2, 'func', 'Быстрый Фибоначчи', 'Напишите рекурсивную функцию fib(n): n-е число Фибоначчи (fib(0) = 0, fib(1) = 1). Без кеша она не уложится во время на больших n — добавьте декоратор lru_cache.', 'from functools import lru_cache


def fib(n):
    pass
', '@lru_cache(maxsize=None) над def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2).', '{"func": "fib", "tests": [{"args": [10], "expected": 55}, {"args": [50], "expected": 12586269025}, {"args": [80], "expected": 23416728348467685}, {"args": [0], "expected": 0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 27, 'sort-by-fields', 3, 'func', 'Сортировка по двум полям', 'Напишите функцию sort_people(people): people — список словарей {''city'': ..., ''age'': ...}. Отсортируйте по городу (по алфавиту), а при равных городах — по возрасту (по возрастанию). Используйте operator.itemgetter с двумя ключами.', 'from operator import itemgetter


def sort_people(people):
    pass
', 'sorted(people, key=itemgetter("city", "age")).', '{"func": "sort_people", "tests": [{"args": [[{"age": 30, "city": "Омск"}, {"age": 20, "city": "Тверь"}, {"age": 25, "city": "Омск"}]], "expected": [{"age": 25, "city": "Омск"}, {"age": 30, "city": "Омск"}, {"age": 20, "city": "Тверь"}]}, {"args": [[]], "expected": []}, {"args": [[{"age": 1, "city": "А"}]], "expected": [{"age": 1, "city": "А"}]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 27, 'total-ordering-class', 4, 'stdout', 'Класс с total_ordering', 'Опишите класс Card(rank) с декоратором total_ordering: определите только __eq__ и __lt__ (по рангу), а остальные сравнения (<=, >, >=) должны заработать сами.', 'from functools import total_ordering


class Card:
    def __init__(self, rank):
        self.rank = rank
', '@total_ordering над class; __eq__: сравнить ранги; __lt__: self.rank < other.rank.', '{"driver": "a, b = Card(3), Card(7)\nprint(a < b, a <= b, a > b, a >= b, a == Card(3))\nprint(max(a, b).rank, sorted([b, a, Card(5)])[1].rank)\n", "expected": ["True True False False True", "7 5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 27, 'single-dispatch-describe', 5, 'stdout', 'Перегрузка по типу', 'Напишите функцию describe(x) на singledispatch: для int — «целое <x>», для str — «строка из <n> символов», для list — «список из <n> элементов», для остальных — «что-то».', 'from functools import singledispatch


def describe(x):
    pass
', '@singledispatch над базовой describe; @describe.register(int) def _(x): ... — и так для str и list.', '{"driver": "print(describe(5))\nprint(describe(''привет''))\nprint(describe([1, 2, 3]))\nprint(describe(2.5))\n", "expected": ["целое 5", "строка из 6 символов", "список из 3 элементов", "что-то"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 27, 'cmp-to-key-sort', 6, 'func', 'Сортировка через сравнение', 'Напишите функцию sort_words(words): сначала короткие слова, при равной длине — по алфавиту. Реализуйте через функцию сравнения двух слов и functools.cmp_to_key.', 'from functools import cmp_to_key


def compare(a, b):
    pass


def sort_words(words):
    pass
', 'compare возвращает отрицательное, 0 или положительное число; sorted(words, key=cmp_to_key(compare)).', '{"func": "sort_words", "tests": [{"args": [["bb", "a", "cc", "b"]], "expected": ["a", "b", "bb", "cc"]}, {"args": [["ccc", "aa", "b", "aaa"]], "expected": ["b", "aa", "aaa", "ccc"]}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 27, 'column-itemgetter', 7, 'func', 'Столбец таблицы', 'Напишите функцию column(rows, i): список значений i-го столбца таблицы (rows — список списков). Используйте map и operator.itemgetter.', 'from operator import itemgetter


def column(rows, i):
    pass
', 'list(map(itemgetter(i), rows)).', '{"func": "column", "tests": [{"args": [[[1, 2, 3], [4, 5, 6]], 1], "expected": [2, 5]}, {"args": [[[1, "а"], [2, "б"]], 0], "expected": [1, 2]}, {"args": [[], 0], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'first-squares', 0, 'func', 'Первые квадраты', 'Напишите функцию first_squares(n): список первых n квадратов натуральных чисел: 1, 4, 9, … Используйте itertools.count и islice.', 'from itertools import count, islice


def first_squares(n):
    pass
', 'list(islice((x * x for x in count(1)), n)).', '{"func": "first_squares", "tests": [{"args": [4], "expected": [1, 4, 9, 16]}, {"args": [0], "expected": []}, {"args": [1], "expected": [1]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'chain-all', 1, 'func', 'Склеить списки', 'Напишите функцию chain_all(*lists): один список из элементов всех переданных списков по порядку. Используйте itertools.chain.', 'from itertools import chain


def chain_all(*lists):
    pass
', 'list(chain(*lists)) — звёздочка раскладывает аргументы дальше.', '{"func": "chain_all", "tests": [{"args": [[1, 2], [3], []], "expected": [1, 2, 3]}, {"args": [], "expected": []}, {"args": [["а"], ["б", "в"]], "expected": ["а", "б", "в"]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'running-max', 2, 'func', 'Рекорды по ходу', 'Напишите функцию running_max(nums): список нарастающего максимума: для 3, 1, 4, 1, 5 — 3, 3, 4, 4, 5. Используйте accumulate с функцией max.', 'from itertools import accumulate


def running_max(nums):
    pass
', 'list(accumulate(nums, max)).', '{"func": "running_max", "tests": [{"args": [[3, 1, 4, 1, 5]], "expected": [3, 3, 4, 4, 5]}, {"args": [[]], "expected": []}, {"args": [[5, 4, 3]], "expected": [5, 5, 5]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'group-sizes', 3, 'func', 'Размеры групп', 'Напишите функцию group_sizes(words): словарь «первая буква → сколько слов начинается с неё». Используйте groupby — помните, что данные нужно отсортировать.', 'from itertools import groupby


def group_sizes(words):
    pass
', 'for k, g in groupby(sorted(words), key=lambda w: w[0]): result[k] = len(list(g)).', '{"func": "group_sizes", "tests": [{"args": [["арбуз", "банан", "абрикос", "берёза", "вишня"]], "expected": {"а": 2, "б": 2, "в": 1}}, {"args": [[]], "expected": {}}, {"args": [["я"]], "expected": {"я": 1}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'all-pairs', 4, 'func', 'Все пары', 'Напишите функцию all_pairs(items): список всех пар разных элементов (каждая пара один раз, порядок как в списке) — кортежами. Используйте itertools.combinations.', 'from itertools import combinations


def all_pairs(items):
    pass
', 'list(combinations(items, 2)).', '{"func": "all_pairs", "tests": [{"args": [["а", "б", "в"]], "expected": [{"__tuple__": ["а", "б"]}, {"__tuple__": ["а", "в"]}, {"__tuple__": ["б", "в"]}]}, {"args": [[1]], "expected": []}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'passwords-product', 5, 'func', 'Все пароли', 'Напишите функцию passwords(alphabet, length): список всех строк заданной длины из символов alphabet (с повторами), в лексикографическом порядке алфавита. Используйте itertools.product.', 'from itertools import product


def passwords(alphabet, length):
    pass
', '["".join(p) for p in product(alphabet, repeat=length)].', '{"func": "passwords", "tests": [{"args": ["ab", 2], "expected": ["aa", "ab", "ba", "bb"]}, {"args": ["xy", 1], "expected": ["x", "y"]}, {"args": ["01", 3], "expected": ["000", "001", "010", "011", "100", "101", "110", "111"]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'rle-groupby', 6, 'func', 'Сжатие повторов', 'Напишите функцию rle(s): сжатие подряд идущих повторов строки — список кортежей (символ, сколько раз подряд): для «aaabcc» — [(''a'', 3), (''b'', 1), (''c'', 2)]. Используйте groupby без сортировки.', 'from itertools import groupby


def rle(s):
    pass
', '[(k, len(list(g))) for k, g in groupby(s)].', '{"func": "rle", "tests": [{"args": ["aaabcc"], "expected": [{"__tuple__": ["a", 3]}, {"__tuple__": ["b", 1]}, {"__tuple__": ["c", 2]}]}, {"args": [""], "expected": []}, {"args": ["abab"], "expected": [{"__tuple__": ["a", 1]}, {"__tuple__": ["b", 1]}, {"__tuple__": ["a", 1]}, {"__tuple__": ["b", 1]}]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'pairwise-diffs', 7, 'func', 'Разности соседних', 'Напишите функцию diffs(nums): список разностей соседних элементов: для 1, 4, 9, 16 — 3, 5, 7. Используйте itertools.pairwise.', 'from itertools import pairwise


def diffs(nums):
    pass
', '[b - a for a, b in pairwise(nums)].', '{"func": "diffs", "tests": [{"args": [[1, 4, 9, 16]], "expected": [3, 5, 7]}, {"args": [[5]], "expected": []}, {"args": [[10, 7]], "expected": [-3]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 28, 'small-prefix', 8, 'func', 'Пока числа маленькие', 'Напишите функцию small_prefix(nums, limit): начальный кусок списка, пока элементы меньше limit; на первом большем или равном — стоп. Используйте itertools.takewhile.', 'from itertools import takewhile


def small_prefix(nums, limit):
    pass
', 'list(takewhile(lambda x: x < limit, nums)).', '{"func": "small_prefix", "tests": [{"args": [[1, 2, 9, 3], 5], "expected": [1, 2]}, {"args": [[10, 1], 5], "expected": []}, {"args": [[1, 2], 5], "expected": [1, 2]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-tag-stack', 0, 'stdout', 'Теги и порядок декораторов', 'Напишите декоратор tag(name): он оборачивает строку, которую возвращает функция, в <name>…</name>. Два тега подряд должны вкладываться так, что верхний оказывается снаружи.', 'def tag(name):
    pass
', 'tag возвращает decorator(func), тот возвращает wrapper(*args, **kwargs): return f"<{name}>{func(*args, **kwargs)}</{name}>".', '{"driver": "@tag(\"b\")\n@tag(\"i\")\ndef text():\n    return \"привет\"\n\n\nprint(text())\n\n\n@tag(\"p\")\ndef greet(name):\n    return f\"Здравствуйте, {name}\"\n\n\nprint(greet(\"Аня\"))\n", "expected": ["<b><i>привет</i></b>", "<p>Здравствуйте, Аня</p>"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-repeat-optional', 1, 'stdout', 'repeat: со скобками и без', 'Напишите декоратор repeat, который работает в двух формах: @repeat (два вызова функции) и @repeat(times=3) (заданное число вызовов). Он возвращает результат последнего вызова. Параметр times — только по имени.', 'def repeat(func=None, *, times=2):
    pass
', 'Если func is not None — return decorate(func); иначе return decorate.', '{"driver": "calls = []\n\n\n@repeat\ndef a():\n    calls.append(\"a\")\n    return len(calls)\n\n\n@repeat(times=3)\ndef b():\n    calls.append(\"b\")\n    return len(calls)\n\n\nprint(a(), calls)\nprint(b(), calls)\n", "expected": ["2 [''a'', ''a'']", "5 [''a'', ''a'', ''b'', ''b'', ''b'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-counted-wraps', 2, 'stdout', 'Счётчик вызовов и метаданные', 'Напишите декоратор counted: он считает вызовы в атрибуте wrapper.calls (начинается с нуля), сохраняет имя и документацию оригинала и ссылку __wrapped__ на него.', 'def counted(func):
    pass
', '@functools.wraps(func) даёт имя, документацию и __wrapped__; счётчик — wrapper.calls = 0 после определения wrapper.', '{"driver": "@counted\ndef add(a, b):\n    \"\"\"Складывает числа.\"\"\"\n    return a + b\n\n\nprint(add(1, 2), add(3, 4), add.calls)\nprint(add.__name__, add.__doc__)\nprint(add.__wrapped__(10, 20))\nprint(add.calls)\n", "expected": ["3 7 2", "add Складывает числа.", "30", "2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-class-plugin', 3, 'stdout', 'Реестр плагинов (декоратор класса)', 'Напишите декоратор класса plugin: он добавляет класс в словарь PLUGINS под именем в нижнем регистре и возвращает класс без изменений.', 'PLUGINS = {}


def plugin(cls):
    pass
', 'PLUGINS[cls.__name__.lower()] = cls; return cls.', '{"driver": "@plugin\nclass Json:\n    pass\n\n\n@plugin\nclass Csv:\n    pass\n\n\nprint(sorted(PLUGINS))\nprint(PLUGINS[\"json\"] is Json, Json.__name__)\n", "expected": ["[''csv'', ''json'']", "True Json"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-auto-repr', 4, 'stdout', 'Декоратор класса auto_repr', 'Напишите декоратор класса auto_repr: он добавляет классу метод __repr__, который печатает имя класса и атрибуты экземпляра в порядке создания: Point(x=1, y=2).', 'def auto_repr(cls):
    pass
', 'def __repr__(self): fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items()); cls.__repr__ = __repr__; return cls.', '{"driver": "@auto_repr\nclass Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n\nprint(Point(1, 2))\nprint([Point(0, -1)])\n", "expected": ["Point(x=1, y=2)", "[Point(x=0, y=-1)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-retry', 5, 'stdout', 'Повтор при ошибке', 'Напишите декоратор retry(times, exceptions=(Exception,)): вызывает функцию до times раз; если очередной вызов поднял одно из exceptions — пробует снова; после последней неудачи пробрасывает ошибку. Успешный результат возвращается сразу.', 'def retry(times, exceptions=(Exception,)):
    pass
', 'for attempt in range(times): try: return func(...) except exceptions: if attempt == times - 1: raise.', '{"driver": "attempts = []\n\n\n@retry(3, (ConnectionError,))\ndef flaky():\n    attempts.append(1)\n    if len(attempts) < 3:\n        raise ConnectionError(\"сбой\")\n    return \"ок\"\n\n\nprint(flaky(), len(attempts))\n\n\n@retry(2)\ndef broken():\n    raise ValueError(\"всегда\")\n\n\ntry:\n    broken()\nexcept ValueError as e:\n    print(\"ValueError\", e)\n\n\n@retry(3, (KeyError,))\ndef other():\n    raise TypeError(\"не наша\")\n\n\ntry:\n    other()\nexcept TypeError:\n    print(\"TypeError без повторов\")\n", "expected": ["ок 3", "ValueError всегда", "TypeError без повторов"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-async-aware', 6, 'stdout', 'Декоратор для sync и async', 'Напишите декоратор traced: он печатает «вызов <имя>» перед выполнением и «готово <имя>» после — и для обычных функций, и для async def (для них обёртка должна быть асинхронной и дожидаться результата).', 'import inspect


def traced(func):
    pass
', 'if inspect.iscoroutinefunction(func): async def wrapper(...): ... result = await func(...); иначе обычная обёртка.', '{"driver": "import asyncio\n\n\n@traced\ndef plain(x):\n    return x + 1\n\n\n@traced\nasync def fetch(x):\n    await asyncio.sleep(0)\n    return x * 2\n\n\nprint(plain(1))\nprint(asyncio.run(fetch(5)))\nprint(inspect.iscoroutinefunction(fetch), inspect.iscoroutinefunction(plain))\n", "expected": ["вызов plain", "готово plain", "2", "вызов fetch", "готово fetch", "10", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-callcounter-class', 7, 'stdout', 'Класс-декоратор для функций и методов', 'Допишите класс-декоратор CallCounter: он считает вызовы в атрибуте calls, сохраняет метаданные оригинала (functools.update_wrapper) и работает не только на функциях, но и на методах — для этого добавьте __get__ (при обращении через класс возвращайте сам счётчик).', 'import functools
import types


class CallCounter:
    def __init__(self, func):
        self.func = func
        self.calls = 0
', '__call__ увеличивает calls; __get__(self, obj, objtype=None): if obj is None: return self; return types.MethodType(self, obj).', '{"driver": "@CallCounter\ndef hello(name):\n    return f\"hi {name}\"\n\n\nclass A:\n    @CallCounter\n    def m(self, x):\n        return x * 2\n\n\nprint(hello(\"a\"), hello(\"b\"), hello.calls)\na = A()\nprint(a.m(2), a.m(3), A.m.calls)\nprint(hello.__name__)\n", "expected": ["hi a hi b 2", "4 6 2", "hello"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 29, 'dc-checked-annotations', 8, 'stdout', 'Проверка аргументов по аннотациям', 'Напишите декоратор checked: перед вызовом он привязывает аргументы к подписи функции (inspect.signature(...).bind) и для каждого параметра с аннотацией-типом проверяет isinstance; при несовпадении поднимает TypeError. Параметры без аннотаций не проверяются.', 'import inspect


def checked(func):
    pass
', 'bound = sig.bind(*args, **kwargs); for name, value in bound.arguments.items(): ann = sig.parameters[name].annotation; if ann is not inspect.Parameter.empty and not isinstance(value, ann): raise TypeError.', '{"driver": "@checked\ndef add(a: int, b: int, note=None):\n    return a + b\n\n\nprint(add(1, 2))\nprint(add(a=3, b=4, note=\"x\"))\ntry:\n    add(1, \"2\")\nexcept TypeError as e:\n    print(\"TypeError\")\ntry:\n    add(1.5, 2)\nexcept TypeError:\n    print(\"TypeError float\")\n", "expected": ["3", "7", "TypeError", "TypeError float"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-public-data', 0, 'stdout', 'Публичные данные объекта', 'Напишите public_data(obj): отсортированный список имён атрибутов объекта (включая атрибуты класса), которые не начинаются с подчёркивания и не являются вызываемыми.', 'def public_data(obj):
    pass
', 'for name in dir(obj): if not name.startswith("_") and not callable(getattr(obj, name)).', '{"driver": "class A:\n    kind = \"x\"\n\n    def __init__(self):\n        self.a = 1\n        self._hidden = 2\n        self.fn = lambda: 0\n\n    def method(self):\n        return 1\n\n\nprint(public_data(A()))\nprint(public_data(object()))\n", "expected": ["[''a'', ''kind'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-dispatch', 1, 'stdout', 'Диспетчер команд по имени', 'Напишите dispatch(obj, command, *args): вызывает метод obj с именем cmd_<command> и возвращает результат. Если такого метода нет, поднимайте ValueError("неизвестная команда: <command>"). Доступ только к методам с префиксом cmd_.', 'def dispatch(obj, command, *args):
    pass
', 'handler = getattr(obj, "cmd_" + command, None); если None — ValueError.', '{"driver": "class Shell:\n    def cmd_add(self, a, b):\n        return a + b\n\n    def cmd_echo(self, text):\n        return text\n\n    def secret(self):\n        return \"не должно вызываться\"\n\n\nsh = Shell()\nprint(dispatch(sh, \"add\", 2, 3))\nprint(dispatch(sh, \"echo\", \"привет\"))\nfor bad in (\"secret\", \"mul\"):\n    try:\n        dispatch(sh, bad)\n    except ValueError as e:\n        print(e)\n", "expected": ["5", "привет", "неизвестная команда: secret", "неизвестная команда: mul"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-param-info', 2, 'stdout', 'Описание параметров функции', 'Напишите param_info(func): список кортежей (имя, вид, есть_значение_по_умолчанию) для каждого параметра функции по её подписи. Вид — имя элемента inspect.Parameter.kind (например, KEYWORD_ONLY).', 'import inspect


def param_info(func):
    pass
', 'for p in inspect.signature(func).parameters.values(): p.name, p.kind.name, p.default is not inspect.Parameter.empty.', '{"driver": "def f(a, /, b, c=1, *args, d, e=2, **kw):\n    pass\n\n\nfor row in param_info(f):\n    print(row)\n", "expected": ["(''a'', ''POSITIONAL_ONLY'', False)", "(''b'', ''POSITIONAL_OR_KEYWORD'', False)", "(''c'', ''POSITIONAL_OR_KEYWORD'', True)", "(''args'', ''VAR_POSITIONAL'', False)", "(''d'', ''KEYWORD_ONLY'', False)", "(''e'', ''KEYWORD_ONLY'', True)", "(''kw'', ''VAR_KEYWORD'', False)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-resolve-args', 3, 'stdout', 'Какие значения достались параметрам', 'Напишите resolve_args(func, *args, **kwargs): привяжите вызов к подписи функции (bind), добавьте значения по умолчанию и верните обычный словарь «параметр → значение». Некорректный вызов должен поднимать TypeError.', 'import inspect


def resolve_args(func, *args, **kwargs):
    pass
', 'bound = inspect.signature(func).bind(*args, **kwargs); bound.apply_defaults(); return dict(bound.arguments).', '{"driver": "def f(a, b=2, *rest, k=5):\n    pass\n\n\nprint(resolve_args(f, 1))\nprint(resolve_args(f, 1, 3, 4, k=0))\ntry:\n    resolve_args(f)\nexcept TypeError:\n    print(\"TypeError\")\n", "expected": ["{''a'': 1, ''b'': 2, ''rest'': (), ''k'': 5}", "{''a'': 1, ''b'': 3, ''rest'': (4,), ''k'': 0}", "TypeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-closure-vars', 4, 'stdout', 'Что унесла вложенная функция', 'Напишите captured(func): словарь «имя свободной переменной → её значение» для замыкания (используйте __code__.co_freevars и __closure__). У функции без замыкания результат — пустой словарь.', 'def captured(func):
    pass
', 'dict(zip(func.__code__.co_freevars, (c.cell_contents for c in func.__closure__ or ()))).', '{"driver": "def make(a, b):\n    def f(x):\n        return x * a + b\n    return f\n\n\ndef plain(x):\n    return x\n\n\nprint(sorted(captured(make(2, 3)).items()))\nprint(captured(plain))\n", "expected": ["[(''a'', 2), (''b'', 3)]", "{}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-all-subclasses', 5, 'stdout', 'Все потомки класса', 'Напишите all_subclasses(cls): отсортированный список имён всех прямых и косвенных потомков класса (без повторов, даже при ромбовидном наследовании).', 'def all_subclasses(cls):
    pass
', 'Рекурсивно обходите cls.__subclasses__() и собирайте имена во множество.', '{"driver": "class Base: pass\nclass A(Base): pass\nclass B(Base): pass\nclass C(A, B): pass\nclass D(C): pass\n\n\nprint(all_subclasses(Base))\nprint(all_subclasses(C))\nprint(all_subclasses(D))\n", "expected": ["[''A'', ''B'', ''C'', ''D'']", "[''D'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-to-dict', 6, 'stdout', 'Объект в словарь', 'Напишите to_dict(obj): словарь из атрибутов экземпляра (vars). Вложенные объекты с атрибутами превращайте рекурсивно, списки и кортежи обрабатывайте поэлементно (как списки), простые значения оставляйте как есть.', 'def to_dict(obj):
    pass
', 'Вспомогательная функция convert(value): если у значения есть __dict__ — to_dict, если list/tuple — [convert(x) ...], иначе значение.', '{"driver": "class Address:\n    def __init__(self, city, zip_code):\n        self.city = city\n        self.zip = zip_code\n\n\nclass Person:\n    def __init__(self, name, address, tags):\n        self.name = name\n        self.address = address\n        self.tags = tags\n\n\np = Person(\"Ann\", Address(\"Омск\", 644000), [\"a\", \"b\"])\nprint(to_dict(p))\nprint(to_dict(Address(\"Тула\", 1)))\n", "expected": ["{''name'': ''Ann'', ''address'': {''city'': ''Омск'', ''zip'': 644000}, ''tags'': [''a'', ''b'']}", "{''city'': ''Тула'', ''zip'': 1}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-caller-name', 7, 'stdout', 'Имя вызвавшей функции', 'Напишите caller_name(): возвращает имя функции, из которой её вызвали (на уровне модуля — «<module>»). Используйте inspect.currentframe() и f_back; не забудьте удалить ссылку на кадр.', 'import inspect


def caller_name():
    pass
', 'frame = inspect.currentframe().f_back; name = frame.f_code.co_name; del frame; return name.', '{"driver": "def outer():\n    return caller_name()\n\n\ndef other():\n    return outer()\n\n\nprint(outer())\nprint(other())\nprint(caller_name())\n", "expected": ["outer", "outer", "<module>"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 30, 'rf-load-by-name', 8, 'stdout', 'Загрузка объекта по строке', 'Напишите load(path): по строке вида «пакет.модуль.имя» подключает модуль (importlib.import_module) и возвращает объект с этим именем. Нет модуля — ImportError, нет имени — AttributeError.', 'import importlib


def load(path):
    pass
', 'module_path, _, name = path.rpartition("."); getattr(importlib.import_module(module_path), name).', '{"driver": "print(load(\"math.sqrt\")(16))\nprint(load(\"os.path.join\")(\"a\", \"b\"))\nprint(load(\"json.dumps\")({\"k\": 1}))\nfor bad in (\"json.nope\", \"nomodule_zz.x\"):\n    try:\n        load(bad)\n    except AttributeError:\n        print(\"AttributeError\")\n    except ImportError:\n        print(\"ImportError\")\n", "expected": ["4.0", "a/b", "{\"k\": 1}", "AttributeError", "ImportError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-make-class', 0, 'stdout', 'Класс по описанию полей', 'Напишите make_class(name, fields): с помощью type(...) создайте класс с данным именем, __init__(self, *values) (число значений обязано совпадать с числом полей, иначе TypeError) и __repr__ вида P(x=1, y=2).', 'def make_class(name, fields):
    pass
', 'Определите init и repr как вложенные функции и верните type(name, (), {"__init__": init, "__repr__": repr_}).', '{"driver": "P = make_class(\"P\", [\"x\", \"y\"])\np = P(1, 2)\nprint(p)\nprint(P.__name__, type(P).__name__)\ntry:\n    P(1)\nexcept TypeError:\n    print(\"TypeError\")\nprint(p.x + p.y)\n", "expected": ["P(x=1, y=2)", "P type", "TypeError", "3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-registry', 1, 'stdout', 'Реестр потомков (__init_subclass__)', 'Допишите базовый класс Plugin: каждый потомок автоматически попадает в словарь Plugin.registry. Ключ — аргумент name из class-оператора (class Json(Plugin, name="json")) или имя класса в нижнем регистре.', 'class Plugin:
    registry = {}
', 'def __init_subclass__(cls, name=None, **kwargs): super().__init_subclass__(**kwargs); Plugin.registry[name or cls.__name__.lower()] = cls.', '{"driver": "class Json(Plugin, name=\"json\"):\n    pass\n\n\nclass CsvReader(Plugin):\n    pass\n\n\nprint(sorted(Plugin.registry))\nprint(Plugin.registry[\"json\"] is Json, Plugin.registry[\"csvreader\"] is CsvReader)\n", "expected": ["[''csvreader'', ''json'']", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-required-attrs', 2, 'stdout', 'Обязательный атрибут потомка', 'Допишите Shape: у каждого потомка при создании класса должен быть целочисленный атрибут sides; если его нет или он не int — поднимайте TypeError прямо в момент определения класса.', 'class Shape:
    pass
', '__init_subclass__: if not isinstance(getattr(cls, "sides", None), int): raise TypeError(...).', '{"driver": "class Tri(Shape):\n    sides = 3\n\n\nprint(Tri.sides)\ntry:\n    class Bad(Shape):\n        pass\nexcept TypeError:\n    print(\"TypeError без sides\")\ntry:\n    class Worse(Shape):\n        sides = \"три\"\nexcept TypeError:\n    print(\"TypeError не int\")\n", "expected": ["3", "TypeError без sides", "TypeError не int"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-singleton', 3, 'stdout', 'Одиночка через метакласс', 'Напишите метакласс Singleton: у каждого класса с этим метаклассом существует не более одного экземпляра — повторный вызов класса возвращает уже созданный, а __init__ выполняется один раз. Разные классы получают разные экземпляры.', 'class Singleton(type):
    pass
', 'Храните словарь экземпляров в метаклассе; __call__(cls, *args, **kwargs): если cls нет в словаре — создайте через super().__call__.', '{"driver": "class Config(metaclass=Singleton):\n    def __init__(self):\n        print(\"init\")\n\n\nclass Other(metaclass=Singleton):\n    pass\n\n\na = Config()\nb = Config()\nprint(a is b)\nprint(Other() is Other(), Other() is a)\n", "expected": ["init", "True", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-commands', 4, 'stdout', 'Метакласс собирает команды', 'Напишите метакласс CommandMeta: при создании класса он собирает функции с префиксом cmd_ в словарь commands (ключ — имя без префикса) и кладёт его в класс. Остальные атрибуты остаются как есть.', 'class CommandMeta(type):
    pass
', 'В __new__: ns["commands"] = {k[4:]: v for k, v in ns.items() if k.startswith("cmd_") and callable(v)}; return super().__new__(mcs, name, bases, ns).', '{"driver": "class Bot(metaclass=CommandMeta):\n    def cmd_hi(self):\n        return \"привет\"\n\n    def cmd_bye(self):\n        return \"пока\"\n\n    def helper(self):\n        return \"служебная\"\n\n\nprint(sorted(Bot.commands))\nb = Bot()\nprint(Bot.commands[\"hi\"](b), b.helper())\nprint(Bot.commands == {k[4:]: v for k, v in vars(Bot).items() if k.startswith(\"cmd_\")})\n", "expected": ["[''bye'', ''hi'']", "привет служебная", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-final', 5, 'stdout', 'Запрет наследования', 'Напишите метакласс FinalMeta: если у какого-либо родителя нового класса есть атрибут __final__ со значением True, создание класса должно завершаться TypeError (наследовать такой класс нельзя).', 'class FinalMeta(type):
    pass
', 'В __new__: if any(getattr(base, "__final__", False) for base in bases): raise TypeError(...).', '{"driver": "class A(metaclass=FinalMeta):\n    __final__ = True\n\n\ntry:\n    class B(A):\n        pass\nexcept TypeError:\n    print(\"наследовать нельзя\")\n\n\nclass C(metaclass=FinalMeta):\n    pass\n\n\nclass D(C):\n    pass\n\n\nprint(D.__mro__[1].__name__, A.__final__)\n", "expected": ["наследовать нельзя", "C True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-class-getitem', 6, 'stdout', 'Box[int] как обобщённый тип', 'Научите класс Box поддерживать запись Box[int] (и Box[str, int]): метод __class_getitem__ возвращает types.GenericAlias с исходным классом и аргументами.', 'import types


class Box:
    pass
', 'def __class_getitem__(cls, item): return types.GenericAlias(cls, item).', '{"driver": "alias = Box[int]\nprint(alias.__origin__ is Box, alias.__args__[0].__name__)\nprint([t.__name__ for t in Box[str, int].__args__])\nprint(Box() is not None)\n", "expected": ["True int", "[''str'', ''int'']", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-prepare-nodup', 7, 'stdout', 'Запрет повторных имён в теле класса', 'Напишите метакласс NoDupMeta: с помощью __prepare__ он подставляет собственное пространство имён (подкласс dict), которое поднимает TypeError, если имя (кроме специальных, начинающихся с двух подчёркиваний) определено в теле класса дважды. Класс должен создаваться обычным образом.', 'class NoDupMeta(type):
    pass
', '__prepare__ — метод класса метакласса: верните экземпляр dict-наследника с __setitem__; в __new__ передайте dict(ns) в super().__new__.', '{"driver": "class Ok(metaclass=NoDupMeta):\n    def a(self):\n        return 1\n\n    def b(self):\n        return 2\n\n\nprint(Ok().a(), Ok().b())\ntry:\n    class Bad(metaclass=NoDupMeta):\n        def a(self):\n            return 1\n\n        def a(self):\n            return 2\n    print(\"ошибки нет\")\nexcept TypeError:\n    print(\"TypeError\")\n", "expected": ["1 2", "TypeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 31, 'mc-counted', 8, 'stdout', 'Учёт экземпляров по классам', 'Напишите метакласс Counted: у каждого класса с этим метаклассом (и у каждого потомка отдельно) есть атрибут instances — сколько экземпляров создано именно этим классом.', 'class Counted(type):
    pass
', 'В __init__ метакласса: cls.instances = 0; в __call__: cls.instances += 1; return super().__call__(*args, **kwargs).', '{"driver": "class A(metaclass=Counted):\n    pass\n\n\nclass B(A):\n    pass\n\n\nA()\nA()\nB()\nprint(A.instances, B.instances)\n", "expected": ["2 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-calc', 0, 'stdout', 'Безопасный калькулятор', 'Напишите calc(expr): разберите строку через ast.parse(expr, mode="eval") и вычислите её рекурсивно, допуская только числа (int, float), унарные + и −, бинарные + − * / // % **. Всё остальное (вызовы, имена, строки) — ValueError. Таблицы OPS и UNARY уже есть.', 'import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos}


def calc(expr):
    pass
', 'Рекурсивная функция по узлам: Constant → значение, BinOp → OPS[type(node.op)](...), UnaryOp → UNARY[...](...), иначе raise ValueError.', '{"driver": "print(calc(\"2 + 3 * 4\"))\nprint(calc(\"-(2 + 3) ** 2\"))\nprint(calc(\"10 / 4\"), calc(\"7 // 2\"))\nfor bad in [\"__import__(''os'')\", \"abs(-1)\", \"x + 1\", \"''a'' * 3\"]:\n    try:\n        calc(bad)\n    except ValueError:\n        print(\"ValueError\")\n", "expected": ["14", "-25", "2.5 3", "ValueError", "ValueError", "ValueError", "ValueError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-literal-config', 1, 'stdout', 'Настройки только из литералов', 'Напишите parse_config(text): превратите строку в значение функцией ast.literal_eval. Если в строке не литерал (вызов, выражение) или синтаксическая ошибка — поднимайте ValueError("некорректная настройка").', 'import ast


def parse_config(text):
    pass
', 'try: return ast.literal_eval(text) except (ValueError, SyntaxError): raise ValueError("некорректная настройка").', '{"driver": "print(parse_config(\"{''a'': [1, 2], ''b'': (3, 4.5), ''c'': None}\"))\nfor bad in [\"__import__(''os'')\", \"{''a'': 1+}\", \"[x for x in range(3)]\"]:\n    try:\n        parse_config(bad)\n    except ValueError as e:\n        print(\"ValueError\", e)\n", "expected": ["{''a'': [1, 2], ''b'': (3, 4.5), ''c'': None}", "ValueError некорректная настройка", "ValueError некорректная настройка", "ValueError некорректная настройка"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-called-names', 2, 'stdout', 'Какие функции вызывает код', 'Напишите called_names(source): отсортированный список имён функций, вызываемых по простому имени (print(...), foo(...)). Вызовы методов вида obj.method() не учитывайте. Используйте ast.NodeVisitor и не забывайте обходить вложенные вызовы.', 'import ast


def called_names(source):
    pass
', 'В visit_Call: if isinstance(node.func, ast.Name): names.add(node.func.id); затем self.generic_visit(node).', '{"driver": "src = \"print(len(x))\\nresult = foo(bar(1), baz.qux())\\nobj.method()\\n\"\nprint(called_names(src))\nprint(called_names(\"x = 1\"))\n", "expected": ["[''bar'', ''foo'', ''len'', ''print'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-count-functions', 3, 'stdout', 'Сколько функций определено', 'Напишите count_functions(source): число определений функций и методов (def и async def, включая вложенные); lambda не считаются.', 'import ast


def count_functions(source):
    pass
', 'sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree)).', '{"driver": "src = ''''''\ndef a(): pass\nclass K:\n    def m(self):\n        def inner(): pass\n    async def n(self): pass\nf = lambda x: x\n''''''\nprint(count_functions(src))\nprint(count_functions(\"x = 1\"))\n", "expected": ["4", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-imports', 4, 'stdout', 'Какие модули импортирует код', 'Напишите imported_modules(source): отсортированный список имён модулей верхнего уровня, которые импортирует исходник (import a.b → a, from c.d import e → c). Относительные импорты (from . import x) пропускайте.', 'import ast


def imported_modules(source):
    pass
', 'ast.Import: node.names[i].name.split(''.'')[0]; ast.ImportFrom: если node.level == 0 — node.module.split(''.'')[0].', '{"driver": "src = \"import os.path\\nimport sys as s, json\\nfrom collections.abc import Mapping\\nfrom . import local\\nfrom .pkg import y\\n\"\nprint(imported_modules(src))\nprint(imported_modules(\"x = 1\"))\n", "expected": ["[''collections'', ''json'', ''os'', ''sys'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-rename-var', 5, 'stdout', 'Переименование переменной', 'Напишите rename_var(source, old, new): с помощью ast.NodeTransformer переименуйте все обращения к имени old (узлы Name и параметры функций arg) и верните текст через ast.unparse.', 'import ast


def rename_var(source, old, new):
    pass
', 'visit_Name: if node.id == old: node.id = new; return node. Для параметров — visit_arg: node.arg.', '{"driver": "print(rename_var(\"x = 1\\ny = x + 2\\nprint(y)\", \"x\", \"t\"))\nprint(rename_var(\"def f(x):\\n    return x * 2\", \"x\", \"n\"))\n", "expected": ["t = 1", "y = t + 2", "print(y)", "def f(n):", "    return n * 2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-fold-constants', 6, 'stdout', 'Вычисление констант заранее', 'Напишите fold_constants(source): NodeTransformer заменяет бинарные операции +, − и * над двумя числовыми константами на одну константу — в том числе вложенные. Результат верните через ast.unparse.', 'import ast


def fold_constants(source):
    pass
', 'В visit_BinOp сначала self.generic_visit(node); если left и right — ast.Constant, а op — Add/Sub/Mult, вычислите и верните ast.Constant(value).', '{"driver": "print(fold_constants(\"a = 2 * 3 + b\"))\nprint(fold_constants(\"x = (1 + 2) * (3 + 4)\"))\nprint(fold_constants(\"y = n * 2 + 3 * 4\"))\nprint(fold_constants(\"z = a + b\"))\n", "expected": ["a = 6 + b", "x = 21", "y = n * 2 + 12", "z = a + b"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-exec-namespace', 7, 'stdout', 'exec в собственном пространстве имён', 'Напишите build(source, name): выполните исходник через exec в новом пустом словаре и верните из него объект с именем name. Глобальные имена вашей программы при этом не должны меняться; если имени нет — KeyError.', 'def build(source, name):
    pass
', 'ns = {}; exec(source, ns); return ns[name].', '{"driver": "fn = build(\"def add(a, b):\\n    return a + b\\n\", \"add\")\nprint(fn(2, 3))\nprint(\"add\" in globals())\nprint(fn.__globals__ is globals())\ntry:\n    build(\"x = 1\", \"nothing\")\nexcept KeyError:\n    print(\"KeyError\")\n", "expected": ["5", "False", "False", "KeyError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 32, 'ast-dis-count', 8, 'stdout', 'Вызовы и циклы в байт-коде', 'Напишите count_calls(func) — число команд вызова (CALL, CALL_KW, CALL_FUNCTION_EX) в байт-коде функции — и has_loop(func), которая сообщает, есть ли команда FOR_ITER. Используйте dis.get_instructions.', 'import dis


def count_calls(func):
    pass


def has_loop(func):
    pass
', 'ops = [i.opname for i in dis.get_instructions(func)]; считайте элементы из набора {"CALL", "CALL_KW", "CALL_FUNCTION_EX"}.', '{"driver": "def f(x):\n    return len(x) + abs(x[0])\n\n\ndef g():\n    return 42\n\n\ndef h(a):\n    return sorted(a, key=len)\n\n\ndef loop(xs):\n    for x in xs:\n        print(x)\n\n\nprint(count_calls(f), count_calls(g), count_calls(h), count_calls(loop))\nprint(has_loop(f), has_loop(loop))\n", "expected": ["2 0 1 1", "False True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'top-words', 0, 'func', 'Самые частые слова', 'Напишите функцию top_words(text, n): список из n самых частых слов текста (слова разделены пробелами, регистр не учитывать) в виде кортежей (слово, сколько раз) по убыванию частоты. Используйте Counter.', 'from collections import Counter


def top_words(text, n):
    pass
', 'Counter(text.lower().split()).most_common(n).', '{"func": "top_words", "tests": [{"args": ["да нет Да нет ДА может", 2], "expected": [{"__tuple__": ["да", 3]}, {"__tuple__": ["нет", 2]}]}, {"args": ["а б б в в в", 1], "expected": [{"__tuple__": ["в", 3]}]}, {"args": ["", 3], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'anagram-counter', 1, 'func', 'Анаграммы', 'Напишите функцию is_anagram(a, b): True, если слова состоят из одних и тех же букв (регистр и пробелы не важны). Сравните счётчики букв.', 'from collections import Counter


def is_anagram(a, b):
    pass
', 'Приведите к нижнему регистру, уберите пробелы и сравните Counter(a) == Counter(b).', '{"func": "is_anagram", "tests": [{"args": ["Лотос", "столо"], "expected": true}, {"args": ["кот", "ток "], "expected": true}, {"args": ["кот", "кит"], "expected": false}, {"args": ["аа", "а"], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'group-by-length', 2, 'stdout', 'Группы по длине', 'Напишите функцию group_by_length(words): словарь «длина → список слов этой длины» в исходном порядке. Используйте defaultdict(list) и верните обычный dict.', 'from collections import defaultdict


def group_by_length(words):
    pass
', 'groups[len(w)].append(w); в конце return dict(groups).', '{"driver": "r = group_by_length([''кот'', ''пёс'', ''слон'', ''мышь'', ''жук''])\nprint(sorted(r.items()))\nprint(type(r).__name__)\nprint(group_by_length([]))\n", "expected": ["[(3, [''кот'', ''пёс'', ''жук'']), (4, [''слон'', ''мышь''])]", "dict", "{}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'moving-average', 3, 'func', 'Скользящее среднее', 'Напишите функцию moving_average(nums, k): среднее каждого окна из k подряд идущих чисел (только полные окна). Используйте deque с maxlen=k.', 'from collections import deque


def moving_average(nums, k):
    pass
', 'window = deque(maxlen=k); на каждом x: append; если len(window) == k — добавить sum(window) / k.', '{"func": "moving_average", "tests": [{"args": [[1, 2, 3, 4], 2], "expected": [1.5, 2.5, 3.5]}, {"args": [[10, 20, 30], 3], "expected": [20.0]}, {"args": [[1, 2], 3], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'bfs-order', 4, 'func', 'Обход в ширину', 'Напишите функцию bfs_order(graph, start): порядок вершин при обходе графа в ширину. graph — словарь «вершина → список соседей». Используйте deque; каждую вершину посещайте один раз.', 'from collections import deque


def bfs_order(graph, start):
    pass
', 'queue = deque([start]); seen — словарь посещённых; popleft, добавить соседей, которых ещё не было.', '{"func": "bfs_order", "tests": [{"args": [{"А": ["Б", "В"], "Б": ["Г"], "В": ["Г"], "Г": []}, "А"], "expected": ["А", "Б", "В", "Г"]}, {"args": [{"1": ["2"], "2": ["1"]}, "1"], "expected": ["1", "2"]}, {"args": [{"x": []}, "x"], "expected": ["x"]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'namedtuple-distance', 5, 'stdout', 'Точка как namedtuple', 'Создайте именованный кортеж Point с полями x и y и функцию distance(p, q) — евклидово расстояние между двумя точками (используйте math.hypot).', 'from collections import namedtuple
import math

Point = None


def distance(p, q):
    pass
', 'Point = namedtuple("Point", ["x", "y"]); distance: math.hypot(p.x - q.x, p.y - q.y).', '{"driver": "p = Point(3, 4)\nprint(p, p.x, p.y)\nprint(distance(Point(0, 0), p))\nprint(p == (3, 4), p._replace(y=0))\n", "expected": ["Point(x=3, y=4) 3 4", "5.0", "True Point(x=3, y=0)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'k-largest-heap', 6, 'func', 'k наибольших', 'Напишите функцию k_largest(nums, k): k наибольших чисел по убыванию. Используйте модуль heapq.', 'import heapq


def k_largest(nums, k):
    pass
', 'heapq.nlargest(k, nums) уже возвращает по убыванию.', '{"func": "k_largest", "tests": [{"args": [[5, 1, 9, 3, 7, 8], 3], "expected": [9, 8, 7]}, {"args": [[4, 4, 1], 2], "expected": [4, 4]}, {"args": [[1, 2], 5], "expected": [2, 1]}, {"args": [[], 2], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'grade-bisect', 7, 'func', 'Оценка по баллам', 'Напишите функцию grade(score): 0–59 → «E», 60–69 → «D», 70–79 → «C», 80–89 → «B», 90–100 → «A». Используйте bisect и список границ — без цепочки if.', 'import bisect


def grade(score):
    pass
', 'bounds = [60, 70, 80, 90]; "EDCBA"[bisect.bisect(bounds, score)].', '{"func": "grade", "tests": [{"args": [59], "expected": "E"}, {"args": [60], "expected": "D"}, {"args": [79], "expected": "C"}, {"args": [80], "expected": "B"}, {"args": [100], "expected": "A"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 33, 'merge-sorted-heap', 8, 'func', 'Слить отсортированные', 'Напишите функцию merge_sorted(lists): один отсортированный список из нескольких уже отсортированных. Используйте heapq.merge.', 'import heapq


def merge_sorted(lists):
    pass
', 'list(heapq.merge(*lists)).', '{"func": "merge_sorted", "tests": [{"args": [[[1, 4, 7], [2, 5], [3, 6]]], "expected": [1, 2, 3, 4, 5, 6, 7]}, {"args": [[[], [1]]], "expected": [1]}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'lcm-all', 0, 'func', 'Общее кратное списка', 'Напишите функцию lcm_all(nums): наименьшее общее кратное всех чисел списка; для пустого списка — 1. Используйте math.lcm.', 'import math


def lcm_all(nums):
    pass
', 'math.lcm(*nums) — у lcm без аргументов результат 1.', '{"func": "lcm_all", "tests": [{"args": [[4, 6]], "expected": 12}, {"args": [[2, 3, 5]], "expected": 30}, {"args": [[]], "expected": 1}, {"args": [[7]], "expected": 7}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'nearly-equal', 1, 'func', 'Почти равны', 'Напишите функцию nearly_equal(a, b): True, если дробные числа равны с учётом погрешности (math.isclose).', 'import math


def nearly_equal(a, b):
    pass
', 'return math.isclose(a, b).', '{"func": "nearly_equal", "tests": [{"args": [0.30000000000000004, 0.3], "expected": true}, {"args": [1.0, 1.1], "expected": false}, {"args": [1e-12, 0.0], "expected": false}, {"args": [100.0, 100.0], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'round-half-up', 2, 'func', 'Школьное округление', 'Напишите функцию round_half_up(text, digits): число задано СТРОКОЙ; верните строку, округлённую до digits знаков после запятой по школьным правилам (0.5 — вверх). Используйте Decimal и quantize с ROUND_HALF_UP.', 'from decimal import Decimal, ROUND_HALF_UP


def round_half_up(text, digits):
    pass
', 'str(Decimal(text).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)) — либо Decimal("0.01") для двух знаков.', '{"func": "round_half_up", "tests": [{"args": ["2.675", 2], "expected": "2.68"}, {"args": ["2.5", 0], "expected": "3"}, {"args": ["3.14159", 3], "expected": "3.142"}, {"args": ["1.005", 2], "expected": "1.01"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'total-decimal', 3, 'func', 'Сумма чека', 'Напишите функцию total_price(prices): prices — список цен СТРОКАМИ («19.99»). Верните сумму строкой с двумя знаками после запятой. Используйте Decimal (никаких float).', 'from decimal import Decimal


def total_price(prices):
    pass
', 'total = sum((Decimal(p) for p in prices), Decimal("0")); str(total.quantize(Decimal("0.01"))).', '{"func": "total_price", "tests": [{"args": [["19.99", "0.01"]], "expected": "20.00"}, {"args": [["0.1", "0.2"]], "expected": "0.30"}, {"args": [[]], "expected": "0.00"}, {"args": [["100", "2.5", "0.25"]], "expected": "102.75"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'fraction-sum', 4, 'func', 'Сумма дробей', 'Напишите функцию fraction_sum(pairs): pairs — список пар [числитель, знаменатель]. Верните сумму дробей строкой в несократимом виде («1/2» или «3» для целого). Используйте Fraction.', 'from fractions import Fraction


def fraction_sum(pairs):
    pass
', 'str(sum((Fraction(a, b) for a, b in pairs), Fraction(0))) — Fraction сам сокращает и печатает целое без знаменателя.', '{"func": "fraction_sum", "tests": [{"args": [[[1, 3], [1, 6]]], "expected": "1/2"}, {"args": [[[1, 2], [1, 2]]], "expected": "1"}, {"args": [[]], "expected": "0"}, {"args": [[[2, 4], [3, 4]]], "expected": "5/4"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'roll-dice-seed', 5, 'stdout', 'Повторяемые кубики', 'Напишите функцию roll_dice(n, seed): список из n бросков кубика (числа 1–6). Одно и то же seed должно давать один и тот же результат: задайте зерно через random.seed.', 'import random


def roll_dice(n, seed):
    pass
', 'random.seed(seed); return [random.randint(1, 6) for _ in range(n)].', '{"driver": "a = roll_dice(10, 5)\nb = roll_dice(10, 5)\nc = roll_dice(10, 6)\nprint(a == b, len(a), all(1 <= x <= 6 for x in a))\nprint(roll_dice(0, 1))\n", "expected": ["True 10 True", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'stats-summary', 6, 'func', 'Сводка по данным', 'Напишите функцию stats_summary(data): кортеж (среднее, медиана, мода) списка чисел. Используйте модуль statistics.', 'import statistics


def stats_summary(data):
    pass
', 'return statistics.mean(data), statistics.median(data), statistics.mode(data).', '{"func": "stats_summary", "tests": [{"args": [[2, 4, 4, 4, 5, 5, 7, 9]], "expected": {"__tuple__": [5, 4.5, 4]}}, {"args": [[1, 2, 3]], "expected": {"__tuple__": [2, 2, 1]}}, {"args": [[10]], "expected": {"__tuple__": [10, 10, 10]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'random-password', 7, 'stdout', 'Безопасный пароль', 'Напишите функцию make_password(length): строка из length случайных символов — латинские буквы и цифры. Для безопасности используйте модуль secrets, а не random.', 'import secrets
import string


def make_password(length):
    pass
', '"".join(secrets.choice(alphabet) for _ in range(length)) — alphabet = string.ascii_letters + string.digits.', '{"driver": "import string\nok = set(string.ascii_letters + string.digits)\np = make_password(16)\nprint(len(p), all(c in ok for c in p))\nprint(make_password(16) != make_password(16), make_password(0) == '''')\n", "expected": ["16 True", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 34, 'binary-info', 8, 'func', 'Двоичная запись', 'Напишите функцию binary_info(n): кортеж (двоичная запись числа n БЕЗ префикса 0b, количество единиц в ней) для неотрицательного n.', 'def binary_info(n):
    pass
', 'b = f"{n:b}"; return b, b.count("1").', '{"func": "binary_info", "tests": [{"args": [10], "expected": {"__tuple__": ["1010", 2]}}, {"args": [0], "expected": {"__tuple__": ["0", 0]}}, {"args": [255], "expected": {"__tuple__": ["11111111", 8]}}, {"args": [1], "expected": {"__tuple__": ["1", 1]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'days-between', 0, 'func', 'Дней между датами', 'Напишите функцию days_between(a, b): сколько дней от даты a до даты b (может быть отрицательным). Даты — строки «ГГГГ-ММ-ДД».', 'from datetime import date


def days_between(a, b):
    pass
', '(date.fromisoformat(b) - date.fromisoformat(a)).days.', '{"func": "days_between", "tests": [{"args": ["2024-12-25", "2025-01-01"], "expected": 7}, {"args": ["2024-03-01", "2023-03-01"], "expected": -366}, {"args": ["2024-05-05", "2024-05-05"], "expected": 0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'add-days', 1, 'func', 'Прибавить дни', 'Напишите функцию add_days(day, n): дата через n дней (n может быть отрицательным). Вход и результат — строки «ГГГГ-ММ-ДД».', 'from datetime import date, timedelta


def add_days(day, n):
    pass
', '(date.fromisoformat(day) + timedelta(days=n)).isoformat().', '{"func": "add_days", "tests": [{"args": ["2024-02-28", 2], "expected": "2024-03-01"}, {"args": ["2023-02-28", 2], "expected": "2023-03-02"}, {"args": ["2024-01-01", -1], "expected": "2023-12-31"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'format-date-ru', 2, 'func', 'Дата по-русски', 'Напишите функцию format_ru(day): из «ГГГГ-ММ-ДД» получите «ДД.ММ.ГГГГ». Используйте datetime и strftime.', 'from datetime import date


def format_ru(day):
    pass
', 'date.fromisoformat(day).strftime("%d.%m.%Y").', '{"func": "format_ru", "tests": [{"args": ["2024-03-05"], "expected": "05.03.2024"}, {"args": ["1999-12-31"], "expected": "31.12.1999"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'weekday-name', 3, 'func', 'День недели', 'Напишите функцию weekday_name(day): название дня недели по-русски («понедельник», «вторник», …) для даты «ГГГГ-ММ-ДД».', 'from datetime import date

NAMES = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]


def weekday_name(day):
    pass
', 'NAMES[date.fromisoformat(day).weekday()].', '{"func": "weekday_name", "tests": [{"args": ["2000-01-01"], "expected": "суббота"}, {"args": ["2024-02-29"], "expected": "четверг"}, {"args": ["2024-03-04"], "expected": "понедельник"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'age-years', 4, 'func', 'Возраст', 'Напишите функцию age(born, today): полных лет между датой рождения и датой «сегодня» (строки «ГГГГ-ММ-ДД»). Если день рождения в этом году ещё не наступил, год не засчитывается.', 'from datetime import date


def age(born, today):
    pass
', 'years = today.year - born.year; если (today.month, today.day) < (born.month, born.day) — вычесть 1.', '{"func": "age", "tests": [{"args": ["2000-06-15", "2024-06-14"], "expected": 23}, {"args": ["2000-06-15", "2024-06-15"], "expected": 24}, {"args": ["2000-02-29", "2024-02-28"], "expected": 23}, {"args": ["2024-01-01", "2024-01-01"], "expected": 0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'workdays-count', 5, 'func', 'Рабочие дни', 'Напишите функцию workdays(start, end): сколько будних дней (пн–пт) в промежутке от start до end включительно. Даты — строки «ГГГГ-ММ-ДД».', 'from datetime import date, timedelta


def workdays(start, end):
    pass
', 'Идите циклом от start до end и считайте дни, у которых weekday() < 5.', '{"func": "workdays", "tests": [{"args": ["2024-03-01", "2024-03-10"], "expected": 6}, {"args": ["2024-03-02", "2024-03-03"], "expected": 0}, {"args": ["2024-03-04", "2024-03-04"], "expected": 1}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'last-day-month', 6, 'func', 'Последний день месяца', 'Напишите функцию last_day(year, month): число дней в месяце. Используйте модуль calendar.', 'import calendar


def last_day(year, month):
    pass
', 'calendar.monthrange(year, month)[1].', '{"func": "last_day", "tests": [{"args": [2024, 2], "expected": 29}, {"args": [2023, 2], "expected": 28}, {"args": [2024, 12], "expected": 31}, {"args": [2024, 4], "expected": 30}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'utc-to-offset', 7, 'func', 'Из UTC в местное', 'Напишите функцию to_offset(iso_utc, hours): время «ГГГГ-ММ-ДДTЧЧ:ММ», заданное в UTC, переведите в пояс со смещением hours часов и верните строкой «ГГГГ-ММ-ДД ЧЧ:ММ». Используйте timezone и timedelta.', 'from datetime import datetime, timedelta, timezone


def to_offset(iso_utc, hours):
    pass
', 'dt = datetime.fromisoformat(s).replace(tzinfo=timezone.utc); dt.astimezone(timezone(timedelta(hours=hours))).strftime(...).', '{"func": "to_offset", "tests": [{"args": ["2024-06-01T12:00", 3], "expected": "2024-06-01 15:00"}, {"args": ["2024-06-01T23:30", 3], "expected": "2024-06-02 02:30"}, {"args": ["2024-01-01T01:00", -5], "expected": "2023-12-31 20:00"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 35, 'parse-log-line', 8, 'func', 'Строка журнала', 'Напишите функцию parse_log(line): строка журнала вида «2024-03-05 09:07:03 ERROR сбой диска». Верните кортеж (время в формате ISO с буквой T, уровень).', 'from datetime import datetime


def parse_log(line):
    pass
', 'date_part, time_part, level, *_ = line.split(); datetime.fromisoformat(date_part + '' '' + time_part).isoformat().', '{"func": "parse_log", "tests": [{"args": ["2024-03-05 09:07:03 ERROR сбой диска"], "expected": {"__tuple__": ["2024-03-05T09:07:03", "ERROR"]}}, {"args": ["2023-12-31 23:59:59 INFO ok"], "expected": {"__tuple__": ["2023-12-31T23:59:59", "INFO"]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'is-phone', 0, 'func', 'Номер телефона', 'Напишите функцию is_phone(s): True, если вся строка — номер вида «+7-900-123-45-67» (после +7 четыре группы через дефис: 3, 3, 2 и 2 цифры). Используйте re.fullmatch.', 'import re


def is_phone(s):
    pass
', 'bool(re.fullmatch(r"\+7-\d{3}-\d{3}-\d{2}-\d{2}", s)).', '{"func": "is_phone", "tests": [{"args": ["+7-900-123-45-67"], "expected": true}, {"args": ["+7-900-123-45-6"], "expected": false}, {"args": ["8-900-123-45-67"], "expected": false}, {"args": ["тел +7-900-123-45-67"], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'find-numbers', 1, 'func', 'Числа из текста', 'Напишите функцию find_numbers(text): список всех целых чисел в тексте, как int; перед числом может стоять минус.', 'import re


def find_numbers(text):
    pass
', '[int(x) for x in re.findall(r"-?\d+", text)].', '{"func": "find_numbers", "tests": [{"args": ["у меня 3 яблока и -12 груш, а 100 — много"], "expected": [3, -12, 100]}, {"args": ["нет чисел"], "expected": []}, {"args": ["a1b22c333"], "expected": [1, 22, 333]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'extract-emails', 2, 'func', 'Адреса почты', 'Напишите функцию extract_emails(text): список адресов вида имя@домен.зона (латиница, цифры, точки и подчёркивания в имени и домене) в порядке появления.', 'import re


def extract_emails(text):
    pass
', 're.findall(r"[\w.]+@[\w.]+\w", text).', '{"func": "extract_emails", "tests": [{"args": ["пишите на ivan@mail.ru или olga_1@ya.ru!"], "expected": ["ivan@mail.ru", "olga_1@ya.ru"]}, {"args": ["почты нет"], "expected": []}, {"args": ["a.b@c.d.org, x"], "expected": ["a.b@c.d.org"]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'collapse-spaces', 3, 'func', 'Лишние пробелы', 'Напишите функцию collapse_spaces(text): подряд идущие пробельные символы (пробелы, табуляции, переводы строк) заменить одним пробелом и убрать пробелы по краям.', 'import re


def collapse_spaces(text):
    pass
', 're.sub(r"\s+", " ", text).strip().', '{"func": "collapse_spaces", "tests": [{"args": ["много   пробелов\n тут"], "expected": "много пробелов тут"}, {"args": ["   край   "], "expected": "край"}, {"args": ["а\t\tб"], "expected": "а б"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'parse-date-groups', 4, 'func', 'Разбор даты', 'Напишите функцию parse_date(s): из строки «ДД.ММ.ГГГГ» верните кортеж чисел (год, месяц, день). Если строка не соответствует формату целиком — None.', 'import re


def parse_date(s):
    pass
', 'm = re.fullmatch(r"(\d\d)\.(\d\d)\.(\d{4})", s); если m — int(m[3]), int(m[2]), int(m[1]).', '{"func": "parse_date", "tests": [{"args": ["05.03.2024"], "expected": {"__tuple__": [2024, 3, 5]}}, {"args": ["31.12.1999"], "expected": {"__tuple__": [1999, 12, 31]}}, {"args": ["5.3.2024"], "expected": null}, {"args": ["дата 05.03.2024"], "expected": null}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'hashtags', 5, 'func', 'Хештеги', 'Напишите функцию hashtags(text): список хештегов (слово после #, буквы, цифры и подчёркивания) без символа #, в нижнем регистре.', 'import re


def hashtags(text):
    pass
', '[t.lower() for t in re.findall(r"#(\w+)", text)].', '{"func": "hashtags", "tests": [{"args": ["Привет #Питон и #regex_101, не # тег"], "expected": ["питон", "regex_101"]}, {"args": ["нет"], "expected": []}, {"args": ["#А#Б"], "expected": ["а", "б"]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'split-words-re', 6, 'func', 'Слова без знаков', 'Напишите функцию split_words(text): список слов текста (буквы и цифры), без знаков препинания и пустых элементов. Используйте re.findall.', 'import re


def split_words(text):
    pass
', 're.findall(r"\w+", text).', '{"func": "split_words", "tests": [{"args": ["Привет, мир! Как дела?"], "expected": ["Привет", "мир", "Как", "дела"]}, {"args": ["...!!!"], "expected": []}, {"args": ["a1-b2"], "expected": ["a1", "b2"]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'censor-words', 7, 'func', 'Цензура', 'Напишите функцию censor(text, bad): замените каждое слово из списка bad (целиком, без учёта регистра) на «***». Части других слов не трогайте: «кот» не должно портить «котёл».', 'import re


def censor(text, bad):
    pass
', 'Соберите шаблон r"\b(?:" + "|".join(map(re.escape, bad)) + r")\b" и вызовите re.sub с флагом re.I.', '{"func": "censor", "tests": [{"args": ["Кот и котёл, КОТ!", ["кот"]], "expected": "*** и котёл, ***!"}, {"args": ["ничего", ["плохо"]], "expected": "ничего"}, {"args": ["раз два три", ["два", "три"]], "expected": "раз *** ***"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 36, 'parse-log-dict', 8, 'func', 'Журнал в словарь', 'Напишите функцию parse_log(line): строка «2024-03-05 09:07:03 ERROR сбой диска» → словарь с ключами «date», «time», «level», «msg». Если строка не подходит — None. Используйте именованные группы.', 'import re


def parse_log(line):
    pass
', '(?P<date>\d{4}-\d\d-\d\d) (?P<time>[\d:]{8}) (?P<level>[A-Z]+) (?P<msg>.*); m.groupdict().', '{"func": "parse_log", "tests": [{"args": ["2024-03-05 09:07:03 ERROR сбой диска"], "expected": {"date": "2024-03-05", "level": "ERROR", "msg": "сбой диска", "time": "09:07:03"}}, {"args": ["2023-12-31 23:59:59 INFO ok"], "expected": {"date": "2023-12-31", "level": "INFO", "msg": "ok", "time": "23:59:59"}}, {"args": ["мусор"], "expected": null}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 37, 'parse-cli-args', 0, 'func', 'Разбор аргументов', 'Напишите функцию parse_cli(argv): с помощью argparse разберите список аргументов командной строки: позиционный text, необязательный --count (целое, по умолчанию 1) и флаг --upper. Верните кортеж (text, count, upper).', 'import argparse


def parse_cli(argv):
    pass
', 'p.add_argument(''text''); p.add_argument(''--count'', type=int, default=1); p.add_argument(''--upper'', action=''store_true'').', '{"func": "parse_cli", "tests": [{"args": [["привет", "--count", "3", "--upper"]], "expected": {"__tuple__": ["привет", 3, true]}}, {"args": [["мир"]], "expected": {"__tuple__": ["мир", 1, false]}}, {"args": [["--count", "2", "а"]], "expected": {"__tuple__": ["а", 2, false]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 37, 'sum-cli-main', 1, 'stdout', 'Утилита-сумматор', 'Напишите функцию main(argv): аргументы argv — числа (argparse, nargs=''*'', type=int). Если чисел нет — напечатайте в stderr «нет чисел» и верните 1; иначе напечатайте сумму и верните 0.', 'import argparse
import sys


def main(argv=None):
    pass
', 'p = argparse.ArgumentParser(); p.add_argument(''nums'', nargs=''*'', type=int); args = p.parse_args(argv).', '{"driver": "print(''код'', main([''1'', ''2'', ''3'']))\nprint(''код'', main([]))\nprint(''код'', main([''-5'', ''5'']))\n", "expected": ["6", "код 0", "код 1", "0", "код 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 37, 'env-or-default', 2, 'stdout', 'Настройка из окружения', 'Напишите функцию get_port(): значение переменной окружения PORT как целое число; если переменной нет — 8000.', 'import os


def get_port():
    pass
', 'int(os.environ.get(''PORT'', 8000)).', '{"driver": "import os\nos.environ.pop(''PORT'', None)\nprint(get_port())\nos.environ[''PORT''] = ''9090''\nprint(get_port(), type(get_port()).__name__)\n", "expected": ["8000", "9090 int"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 37, 'make-logger', 3, 'stdout', 'Свой логгер', 'Напишите функцию make_logger(stream): логгер с именем «app», который пишет в переданный поток сообщения уровня INFO и выше в формате «УРОВЕНЬ: сообщение» (propagate выключите).', 'import logging


def make_logger(stream):
    pass
', 'StreamHandler(stream) + Formatter(''%(levelname)s: %(message)s''); logger.setLevel(logging.INFO); logger.propagate = False.', '{"driver": "import io\nbuf = io.StringIO()\nlog = make_logger(buf)\nlog.debug(''скрыто'')\nlog.info(''старт'')\nlog.warning(''внимание'')\nlog.error(''сбой'')\nprint(buf.getvalue().splitlines())\n", "expected": ["[''INFO: старт'', ''WARNING: внимание'', ''ERROR: сбой'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 37, 'run-python-subprocess', 4, 'stdout', 'Запуск процесса', 'Напишите функцию run_python(code): запускает дочерний интерпретатор (sys.executable) с кодом code и возвращает кортеж (код возврата, вывод без пробелов по краям). Используйте subprocess.run, capture_output и text.', 'import subprocess
import sys


def run_python(code):
    pass
', 'r = subprocess.run([sys.executable, ''-c'', code], capture_output=True, text=True); return r.returncode, r.stdout.strip().', '{"driver": "print(run_python(''print(2 + 2)''))\nprint(run_python(''raise SystemExit(5)''))\nprint(run_python(''import sys; print(\"привет\"); sys.exit(1)''))\n", "expected": ["(0, ''4'')", "(5, '''')", "(1, ''привет'')"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 37, 'run-with-timeout', 5, 'stdout', 'Процесс с таймаутом', 'Напишите функцию run_limited(code, seconds): запускает код в дочернем интерпретаторе; если он не уложился в seconds секунд — верните строку «таймаут», иначе — его вывод без пробелов по краям.', 'import subprocess
import sys


def run_limited(code, seconds):
    pass
', 'try: subprocess.run(..., timeout=seconds) / except subprocess.TimeoutExpired: return ''таймаут''.', '{"driver": "print(run_limited(''print(1)'', 5))\nprint(run_limited(''import time; time.sleep(10)'', 0.3))\n", "expected": ["1", "таймаут"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 37, 'count-nonempty-stream', 6, 'stdout', 'Строки из потока', 'Напишите функцию count_lines(stream): сколько непустых строк (после strip) в файловом объекте stream. Работайте с потоком так же, как со стандартным вводом: перебирайте его циклом.', 'def count_lines(stream):
    pass
', 'n = 0; for line in stream: if line.strip(): n += 1.', '{"driver": "import io\nprint(count_lines(io.StringIO(''а\\n\\nб\\n   \\nв\\n'')))\nprint(count_lines(io.StringIO('''')))\nprint(count_lines(io.StringIO(''одна'')))\n", "expected": ["3", "0", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 38, 'point-dataclass', 0, 'stdout', 'Точка-датакласс', 'Опишите датакласс Point с полями x и y (числа, по умолчанию 0) и методом distance_to(other) — расстояние до другой точки (math.hypot).', 'from dataclasses import dataclass
import math


class Point:
    pass
', '@dataclass над class Point; x: float = 0; y: float = 0.', '{"driver": "p = Point(3, 4)\nprint(p)\nprint(Point())\nprint(p == Point(3, 4), p == Point(4, 3))\nprint(Point().distance_to(p))\n", "expected": ["Point(x=3, y=4)", "Point(x=0, y=0)", "True False", "5.0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 38, 'playlist-default-factory', 1, 'stdout', 'Плейлист без общего списка', 'Опишите датакласс Playlist с полями name (строка) и songs (список, по умолчанию пустой — но свой у каждого экземпляра) и методом add(song), который добавляет песню.', 'from dataclasses import dataclass, field


class Playlist:
    pass
', 'songs: list = field(default_factory=list).', '{"driver": "a = Playlist(''а'')\nb = Playlist(''б'')\na.add(''песня 1'')\na.add(''песня 2'')\nprint(a)\nprint(b.songs)\nprint(a.songs is b.songs)\n", "expected": ["Playlist(name=''а'', songs=[''песня 1'', ''песня 2''])", "[]", "False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 38, 'money-frozen', 2, 'stdout', 'Неизменяемые деньги', 'Опишите неизменяемый (frozen) датакласс Money с полями amount (число) и currency (строка), сравниваемый по порядку полей (order=True).', 'from dataclasses import dataclass


class Money:
    pass
', '@dataclass(frozen=True, order=True) — и заморозка, и сортировка, и хеш.', '{"driver": "a, b = Money(5, ''RUB''), Money(3, ''RUB'')\nprint(sorted([a, b]))\nprint({a: ''пять''}[Money(5, ''RUB'')])\ntry:\n    a.amount = 1\nexcept Exception as e:\n    print(type(e).__name__)\n", "expected": ["[Money(amount=3, currency=''RUB''), Money(amount=5, currency=''RUB'')]", "пять", "FrozenInstanceError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 38, 'status-enum', 3, 'stdout', 'Статус заказа', 'Опишите перечисление Status с членами NEW = ''new'', PAID = ''paid'', SHIPPED = ''shipped'' и методом is_active() — True для NEW и PAID, False для SHIPPED.', 'from enum import Enum


class Status(Enum):
    pass
', 'NEW = ''new'' и так далее; is_active: return self in (Status.NEW, Status.PAID).', '{"driver": "print(Status(''paid''), Status.NEW.value, Status[''SHIPPED''].name)\nprint([s.is_active() for s in Status])\ntry:\n    Status(''lost'')\nexcept ValueError:\n    print(''нет такого статуса'')\n", "expected": ["Status.PAID new SHIPPED", "[True, True, False]", "нет такого статуса"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 38, 'perm-flag', 4, 'stdout', 'Права доступа', 'Опишите Flag-перечисление Perm с членами R, W, X (через auto) и функцию describe(p): строка из трёх символов, например «rw-» для R|W и «r-x» для R|X.', 'from enum import Flag, auto


class Perm(Flag):
    pass


def describe(p):
    pass
', '(''r'' if Perm.R in p else ''-'') + ... для W и X.', '{"driver": "print(describe(Perm.R | Perm.W))\nprint(describe(Perm.R | Perm.X))\nprint(describe(Perm.R | Perm.W | Perm.X))\nprint(describe(Perm(0)))\n", "expected": ["rw-", "r-x", "rwx", "---"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 38, 'annotated-average', 5, 'stdout', 'Функция с подсказками', 'Напишите функцию average(nums, default) с подсказками типов: nums — list[float], default — float (по умолчанию 0.0), результат — float. Возвращает среднее, а для пустого списка — default.', 'def average(nums, default=0.0):
    pass
', 'def average(nums: list[float], default: float = 0.0) -> float:', '{"driver": "print(average([1, 2, 3]), average([], 9.5))\nprint(sorted(average.__annotations__))\nprint(average.__annotations__[''return''].__name__)\n", "expected": ["2.0 9.5", "[''default'', ''nums'', ''return'']", "float"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 38, 'match-shape', 6, 'func', 'Площадь через match', 'Напишите функцию area(shape): shape — список [''circle'', r], [''rect'', w, h] или [''square'', a]. Верните площадь (для круга 3 * r * r, чтобы не зависеть от π). Для остальных форм — None. Используйте match/case.', 'def area(shape):
    pass
', 'case ["circle", r]: return 3 * r * r; case ["rect", w, h]: ...; case _: return None.', '{"func": "area", "tests": [{"args": [["circle", 2]], "expected": 12}, {"args": [["rect", 3, 4]], "expected": 12}, {"args": [["square", 5]], "expected": 25}, {"args": [["triangle", 1, 2, 3]], "expected": null}, {"args": [[]], "expected": null}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 38, 'deepcopy-matrix', 7, 'stdout', 'Независимая копия', 'Напишите функцию clone_and_fill(matrix, value): возвращает копию списка списков, в которой ВСЕ числа заменены на value. Исходная таблица не должна измениться — используйте copy.deepcopy и вложенный цикл.', 'import copy


def clone_and_fill(matrix, value):
    pass
', 'result = copy.deepcopy(matrix); for row in result: for j in range(len(row)): row[j] = value.', '{"driver": "m = [[1, 2], [3, 4]]\nr = clone_and_fill(m, 0)\nprint(m)\nprint(r)\nprint(r is m, r[0] is m[0])\n", "expected": ["[[1, 2], [3, 4]]", "[[0, 0], [0, 0]]", "False False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 39, 'tests-for-leap', 0, 'stdout', 'Тесты для високосного года', 'Допишите класс TestLeap (unittest): тесты функции is_leap(year). Проверка запустит ваши тесты против верной реализации (они должны ПРОЙТИ) и против трёх сломанных (они должны УПАСТЬ). Покройте типичный год, года-века и года, кратные 400.', 'import unittest


class TestLeap(unittest.TestCase):
    def test_example(self):
        pass  # вызывайте is_leap(год)
', 'assertTrue(is_leap(2024)), assertFalse(is_leap(2023)), assertFalse(is_leap(1900)), assertTrue(is_leap(2000)).', '{"driver": "import io\ndef run():\n    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestLeap))\n    return r.wasSuccessful() and r.testsRun > 0\ndef good(y): return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)\ndef bad1(y): return y % 4 == 0\ndef bad2(y): return y % 4 == 0 and y % 100 != 0\ndef bad3(y): return y % 400 == 0\nfor name, f in [(''верная'', good), (''ошибка 1'', bad1), (''ошибка 2'', bad2), (''ошибка 3'', bad3)]:\n    is_leap = f\n    print(name, ''тесты прошли'' if run() else ''тесты упали'')\n", "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 39, 'tests-for-clamp', 1, 'stdout', 'Тесты для clamp', 'Допишите класс TestClamp: тесты функции clamp(x, low, high) — ограничивает x диапазоном [low, high]. Ваши тесты должны пройти на верной реализации и упасть на каждой из трёх сломанных. Проверьте значения внутри, ниже, выше и на границах.', 'import unittest


class TestClamp(unittest.TestCase):
    def test_example(self):
        pass  # вызывайте clamp(x, low, high)
', 'clamp(5, 0, 10) == 5; clamp(-3, 0, 10) == 0; clamp(42, 0, 10) == 10; и сами границы.', '{"driver": "import io\ndef run():\n    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestClamp))\n    return r.wasSuccessful() and r.testsRun > 0\ndef good(x, lo, hi): return min(max(x, lo), hi)\ndef bad1(x, lo, hi): return max(x, lo)\ndef bad2(x, lo, hi): return min(x, hi)\ndef bad3(x, lo, hi):\n    if x < lo: return lo\n    if x > hi: return hi - 1\n    return x\nfor name, f in [(''верная'', good), (''ошибка 1'', bad1), (''ошибка 2'', bad2), (''ошибка 3'', bad3)]:\n    clamp = f\n    print(name, ''тесты прошли'' if run() else ''тесты упали'')\n", "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 39, 'tests-for-divide', 2, 'stdout', 'Тесты для divide', 'Допишите класс TestDivide: тесты функции divide(a, b) — обычное деление; при b == 0 она должна поднимать ValueError. Ваши тесты должны пройти на верной реализации и упасть на трёх сломанных. Не забудьте assertRaises.', 'import unittest


class TestDivide(unittest.TestCase):
    def test_example(self):
        pass  # вызывайте divide(a, b)
', 'self.assertEqual(divide(7, 2), 3.5); with self.assertRaises(ValueError): divide(1, 0).', '{"driver": "import io\ndef run():\n    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestDivide))\n    return r.wasSuccessful() and r.testsRun > 0\ndef good(a, b):\n    if b == 0: raise ValueError(''ноль'')\n    return a / b\ndef bad1(a, b):\n    if b == 0: return None\n    return a / b\ndef bad2(a, b):\n    return a / b\ndef bad3(a, b):\n    if b == 0: raise ValueError(''ноль'')\n    return a // b\nfor name, f in [(''верная'', good), (''ошибка 1'', bad1), (''ошибка 2'', bad2), (''ошибка 3'', bad3)]:\n    divide = f\n    print(name, ''тесты прошли'' if run() else ''тесты упали'')\n", "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 39, 'tests-for-fizzbuzz', 3, 'stdout', 'Тесты для fizzbuzz', 'Допишите класс TestFizz: тесты функции fizzbuzz(n): «FizzBuzz» для кратных 15, «Fizz» для кратных 3, «Buzz» для кратных 5, иначе число строкой. Ваши тесты должны пройти на верной реализации и упасть на трёх сломанных.', 'import unittest


class TestFizz(unittest.TestCase):
    def test_example(self):
        pass  # вызывайте fizzbuzz(n)
', 'assertEqual(fizzbuzz(15), "FizzBuzz"), 9, 5, 10 (для Buzz — и нечётное, и чётное кратное), 7 → "7".', '{"driver": "import io\ndef run():\n    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestFizz))\n    return r.wasSuccessful() and r.testsRun > 0\ndef good(n):\n    if n % 15 == 0: return ''FizzBuzz''\n    if n % 3 == 0: return ''Fizz''\n    if n % 5 == 0: return ''Buzz''\n    return str(n)\ndef bad1(n):\n    if n % 3 == 0: return ''Fizz''\n    if n % 5 == 0: return ''Buzz''\n    return str(n)\ndef bad2(n):\n    if n % 15 == 0: return ''FizzBuzz''\n    if n % 3 == 0: return ''Fizz''\n    if n % 10 == 0: return ''Buzz''\n    return str(n)\ndef bad3(n):\n    if n % 15 == 0: return ''FizzBuzz''\n    if n % 3 == 0: return ''Fizz''\n    if n % 5 == 0: return ''Buzz''\n    return n\nfor name, f in [(''верная'', good), (''ошибка 1'', bad1), (''ошибка 2'', bad2), (''ошибка 3'', bad3)]:\n    fizzbuzz = f\n    print(name, ''тесты прошли'' if run() else ''тесты упали'')\n", "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 39, 'tests-for-stack', 4, 'stdout', 'Тесты для стека', 'Допишите класс TestStack: тесты класса Stack с методами push(x), pop() (снимает верхний; на пустом стеке — IndexError), peek() (верхний без снятия) и size(). Тесты должны пройти на верной реализации и упасть на трёх сломанных.', 'import unittest


class TestStack(unittest.TestCase):
    def setUp(self):
        self.s = Stack()

    def test_example(self):
        pass
', 'Положите 1, 2, 3: pop() == 3, peek() == 2, size() == 2; на пустом: with self.assertRaises(IndexError): self.s.pop().', '{"driver": "import io\ndef run():\n    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestStack))\n    return r.wasSuccessful() and r.testsRun > 0\nclass Good:\n    def __init__(self): self.a = []\n    def push(self, x): self.a.append(x)\n    def pop(self): return self.a.pop()\n    def peek(self): return self.a[-1]\n    def size(self): return len(self.a)\nclass Bad1(Good):\n    def pop(self): return self.a.pop(0)\nclass Bad2(Good):\n    def pop(self): return self.a.pop() if self.a else None\nclass Bad3(Good):\n    def size(self): return len(self.a) + 1\nfor name, c in [(''верная'', Good), (''ошибка 1'', Bad1), (''ошибка 2'', Bad2), (''ошибка 3'', Bad3)]:\n    Stack = c\n    print(name, ''тесты прошли'' if run() else ''тесты упали'')\n", "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 39, 'doctest-abs-diff', 5, 'stdout', 'Функция с doctest', 'Напишите функцию abs_diff(a, b) — модуль разности чисел — и снабдите её докстринг не менее чем тремя doctest-примерами (формат «>>> abs_diff(5, 8)» и ответ на следующей строке). Проверка выполнит ваши примеры.', 'def abs_diff(a, b):
    """Модуль разности.

    Добавьте примеры в формате doctest.
    """
    pass
', '>>> abs_diff(5, 8)\n    3 — каждый пример: строка с >>> и строка с ожидаемым результатом.', '{"driver": "import doctest\nrunner = doctest.DocTestRunner(verbose=False)\nfor t in doctest.DocTestFinder().find(abs_diff, ''abs_diff'', globs={''abs_diff'': abs_diff}):\n    runner.run(t)\nres = runner.summarize(verbose=False)\nprint(res.failed, res.attempted >= 3)\nprint(abs_diff(5, 8), abs_diff(8, 5), abs_diff(2, 2))\n", "expected": ["0 True", "3 3 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 39, 'total-cost-mock', 6, 'stdout', 'Сумма через клиента', 'Напишите функцию total_cost(client, items): сумма цен всех товаров списка items; цену каждого возвращает client.get_price(item). Клиент передаётся параметром — так его можно подменить в тесте.', 'def total_cost(client, items):
    pass
', 'sum(client.get_price(i) for i in items).', '{"driver": "from unittest.mock import Mock, call\nm = Mock()\nm.get_price.side_effect = lambda item: {''а'': 10, ''б'': 25}[item]\nprint(total_cost(m, [''а'', ''б'', ''а'']))\nprint(m.get_price.call_count, m.get_price.call_args_list == [call(''а''), call(''б''), call(''а'')])\nprint(total_cost(Mock(), []))\n", "expected": ["45", "3 True", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 39, 'greeting-injected-time', 7, 'stdout', 'Время параметром', 'Напишите функцию greeting(now): now — объект datetime. До 12 часов — «Доброе утро», с 12 до 18 — «Добрый день», позже — «Добрый вечер». Текущее время внутри не вызывайте.', 'def greeting(now):
    pass
', 'if now.hour < 12: ...; elif now.hour < 18: ...; else: ...', '{"driver": "from datetime import datetime\nfor h in (6, 11, 12, 17, 18, 23):\n    print(h, greeting(datetime(2024, 1, 1, h)))\n", "expected": ["6 Доброе утро", "11 Доброе утро", "12 Добрый день", "17 Добрый день", "18 Добрый вечер", "23 Добрый вечер"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-shape', 0, 'stdout', 'Абстрактная фигура', 'Напишите абстрактный класс Shape (от ABC) с обязательным методом area(), а также классы Rect(w, h) и Circle(r) (площадь круга — 3.14 * r * r). Создать Shape напрямую нельзя.', 'from abc import ABC, abstractmethod
', 'class Shape(ABC): @abstractmethod def area(self): ...; наследники реализуют area.', '{"driver": "try:\n    Shape()\nexcept TypeError:\n    print(\"TypeError\")\nshapes = [Rect(2, 3), Circle(1)]\nprint([s.area() for s in shapes])\nprint(all(isinstance(s, Shape) for s in shapes))\n", "expected": ["TypeError", "[6, 3.14]", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-exporter', 1, 'stdout', 'Контракт экспортёра', 'Напишите абстрактный Exporter: обязательный метод export(data) и обязательное свойство extension. Класс, где не реализовано что-то одно, создать нельзя; полный наследник создаётся и работает.', 'from abc import ABC, abstractmethod
', 'Свойство: @property над @abstractmethod. Атрибут класса extension = "csv" тоже закрывает абстрактное свойство.', '{"driver": "class Csv(Exporter):\n    extension = \"csv\"\n\n    def export(self, data):\n        return \",\".join(map(str, data))\n\n\nclass NoExt(Exporter):\n    def export(self, data):\n        return \"\"\n\n\nclass NoExport(Exporter):\n    @property\n    def extension(self):\n        return \"x\"\n\n\nc = Csv()\nprint(c.export([1, 2, 3]), c.extension)\nfor cls in (NoExt, NoExport):\n    try:\n        cls()\n    except TypeError:\n        print(\"TypeError\", cls.__name__)\n", "expected": ["1,2,3 csv", "TypeError NoExt", "TypeError NoExport"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-template', 2, 'stdout', 'Шаблонный метод отчёта', 'Напишите абстрактный Report с готовым методом render(): он собирает строку из header(), body() и footer(). header и footer реализованы (возвращают «== отчёт ==» и «== конец ==»), а body — абстрактный шаг. Части склеиваются через перевод строки.', 'from abc import ABC, abstractmethod
', 'def render(self): return "\n".join([self.header(), self.body(), self.footer()]).', '{"driver": "class Sales(Report):\n    def body(self):\n        return \"продажи: 42\"\n\n\nclass Users(Report):\n    def body(self):\n        return \"пользователей: 7\"\n\n    def footer(self):\n        return \"-- конец --\"\n\n\nprint(Sales().render())\nprint(Users().render())\ntry:\n    Report()\nexcept TypeError:\n    print(\"TypeError\")\n", "expected": ["== отчёт ==", "продажи: 42", "== конец ==", "== отчёт ==", "пользователей: 7", "-- конец --", "TypeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-factory', 3, 'stdout', 'Абстрактная фабрика', 'Напишите абстрактный Animal: абстрактный классовый метод create() и абстрактный метод speak(). Для каждого наследника создавайте объект через create(); Animal создать напрямую нельзя.', 'from abc import ABC, abstractmethod
', '@classmethod над @abstractmethod; тело create() в базовом классе может быть пустым или возвращать cls().', '{"driver": "class Dog(Animal):\n    @classmethod\n    def create(cls):\n        return cls()\n\n    def speak(self):\n        return \"гав\"\n\n\nclass Cat(Animal):\n    @classmethod\n    def create(cls):\n        return cls()\n\n    def speak(self):\n        return \"мяу\"\n\n\nprint([cls.create().speak() for cls in (Dog, Cat)])\ntry:\n    Animal.create()\nexcept TypeError:\n    print(\"TypeError\")\ntry:\n    class Bad(Animal):\n        def speak(self):\n            return \"?\"\n    Bad()\nexcept TypeError:\n    print(\"TypeError Bad\")\n", "expected": ["[''гав'', ''мяу'']", "TypeError", "TypeError Bad"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-subclasshook', 4, 'stdout', 'Автоматический «подкласс»', 'Напишите ABC-класс HasLen: любой класс, у которого есть метод __len__, автоматически считается его подклассом (через __subclasshook__), без явного наследования. Проверьте, что isinstance работает для списков и для собственных классов с __len__, но не для чисел.', 'from abc import ABC


class HasLen(ABC):
    pass
', '@classmethod def __subclasshook__(cls, C): if cls is HasLen: return hasattr(C, "__len__"); return NotImplemented.', '{"driver": "class Box:\n    def __len__(self):\n        return 3\n\n\nclass Empty:\n    pass\n\n\nprint(isinstance([], HasLen), isinstance(Box(), HasLen))\nprint(isinstance(5, HasLen), isinstance(Empty(), HasLen))\nprint(issubclass(str, HasLen))\n", "expected": ["True True", "False False", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-register', 5, 'stdout', 'Виртуальный подкласс', 'Класс Duck уже есть и ни от кого не наследуется. Напишите абстрактный Quacker и зарегистрируйте Duck как его виртуальный подкласс, чтобы isinstance(Duck(), Quacker) было истинным, а для Dog — нет.', 'from abc import ABC


class Duck:
    def quack(self):
        return "кря"


class Dog:
    pass
', 'class Quacker(ABC): pass; Quacker.register(Duck).', '{"driver": "print(isinstance(Duck(), Quacker), isinstance(Dog(), Quacker))\nprint(issubclass(Duck, Quacker), Duck.__mro__[0].__name__, Quacker in Duck.__mro__)\n", "expected": ["True False", "True Duck False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-sequence', 6, 'stdout', 'Последовательность на двух методах', 'Напишите Countdown(n) — наследника collections.abc.Sequence, содержащего числа n, n-1, …, 1. Реализуйте только __len__ и __getitem__ (индекс вне диапазона — IndexError): остальное приходит от базового класса.', 'from collections.abc import Sequence
', '__getitem__(self, i): if isinstance(i, slice): return [self[k] for k in range(*i.indices(len(self)))]; иначе проверьте границы и верните self.n - i (для отрицательных сначала i += len(self)).', '{"driver": "c = Countdown(4)\nprint(len(c), c[0], c[-1])\nprint(list(c), list(reversed(c)))\nprint(3 in c, 9 in c, c.index(2), c.count(1))\nprint(c[1:3] if isinstance(c[1:3], (list, tuple, range)) else \"срез\")\n", "expected": ["4 4 1", "[4, 3, 2, 1] [1, 2, 3, 4]", "True False 2 1", "[3, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-storage-copy', 7, 'stdout', 'Хранилища и подмена', 'Напишите абстрактный Storage (методы read(key) и write(key, value)), реализацию MemoryStorage на словаре (read несуществующего ключа даёт KeyError) и функцию copy_all(src, dst, keys), копирующую значения по ключам из src в dst. Функция должна работать с любыми Storage.', 'from abc import ABC, abstractmethod
', 'copy_all: for key in keys: dst.write(key, src.read(key)).', '{"driver": "class Upper(Storage):\n    def __init__(self):\n        self.data = {}\n\n    def read(self, key):\n        return self.data[key]\n\n    def write(self, key, value):\n        self.data[key] = value.upper()\n\n\na = MemoryStorage()\na.write(\"x\", \"привет\")\na.write(\"y\", \"мир\")\nb = Upper()\ncopy_all(a, b, [\"x\", \"y\"])\nprint(b.read(\"x\"), b.read(\"y\"))\ntry:\n    a.read(\"z\")\nexcept KeyError:\n    print(\"KeyError\")\ntry:\n    Storage()\nexcept TypeError:\n    print(\"TypeError\")\n", "expected": ["ПРИВЕТ МИР", "KeyError", "TypeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 40, 'abc-describe', 8, 'stdout', 'Вид значения по абстрактным классам', 'Напишите describe(x): «строка» для str; «отображение» для Mapping; «последовательность» для Sequence; «итерируемое» для прочих Iterable; «число» для numbers.Number; иначе «прочее». Порядок проверок важен: строка — тоже последовательность.', 'import numbers
from collections.abc import Iterable, Mapping, Sequence


def describe(x):
    pass
', 'Проверяйте по очереди: str, Mapping, Sequence, Iterable, numbers.Number.', '{"driver": "for v in [\"abc\", {}, [1], (1, 2), {1}, range(3), 5, 3.5, True, None, (i for i in range(2))]:\n    print(describe(v))\n", "expected": ["строка", "отображение", "последовательность", "последовательность", "итерируемое", "последовательность", "число", "число", "число", "прочее", "итерируемое"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-closeable', 0, 'stdout', 'Протокол Closeable', 'Напишите Protocol Closeable с методом close() (с декоратором runtime_checkable) и функцию close_all(items): она закрывает всё, что подходит под протокол, и возвращает, сколько объектов закрыто. Остальные пропускайте.', 'from typing import Protocol, runtime_checkable
', '@runtime_checkable class Closeable(Protocol): def close(self) -> None: ...; в close_all: if isinstance(item, Closeable): item.close().', '{"driver": "import io\n\n\nclass Res:\n    def close(self):\n        print(\"Res закрыт\")\n\n\nclass Plain:\n    pass\n\n\nprint(close_all([Res(), Plain(), io.StringIO(), 5]))\nprint(isinstance(Res(), Closeable), isinstance(Plain(), Closeable))\n", "expected": ["Res закрыт", "2", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-data-protocol', 1, 'stdout', 'Протокол с атрибутом', 'Напишите runtime_checkable-протокол HasName с атрибутом name: str и функцию names(items): список значений name у объектов, которые подходят под протокол (остальные пропускаются).', 'from typing import Protocol, runtime_checkable
', 'class HasName(Protocol): name: str — и @runtime_checkable; в names: [x.name for x in items if isinstance(x, HasName)].', '{"driver": "class User:\n    def __init__(self, name):\n        self.name = name\n\n\nclass Pet:\n    name = \"Барсик\"\n\n\nclass Thing:\n    pass\n\n\nprint(names([User(\"Аня\"), Thing(), Pet(), 5]))\nprint(isinstance(User(\"x\"), HasName), isinstance(Thing(), HasName))\n", "expected": ["[''Аня'', ''Барсик'']", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-generic-stack', 2, 'stdout', 'Обобщённый стек', 'Напишите обобщённый Stack(Generic[T]) с методами push(x), pop() (на пустом стеке — IndexError), peek() и __len__. Запись Stack[int]() тоже должна создавать рабочий стек.', 'from typing import Generic, TypeVar

T = TypeVar("T")
', 'class Stack(Generic[T]) со списком внутри; pop() у пустого списка и так поднимает IndexError.', '{"driver": "s = Stack[int]()\ns.push(1)\ns.push(2)\nprint(len(s), s.peek(), s.pop(), s.pop(), len(s))\ntry:\n    s.pop()\nexcept IndexError:\n    print(\"IndexError\")\nprint(Stack.__parameters__[0].__name__)\nprint(Stack[str].__origin__ is Stack)\n", "expected": ["2 2 2 1 0", "IndexError", "T", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-pep695-box', 3, 'stdout', 'Box в новом синтаксисе', 'Напишите класс Box[T] с новым синтаксисом параметров типа (Python 3.12+, без Generic и TypeVar): поле value, метод map(f) — возвращает новый Box со значением f(value), и __repr__ вида Box(3).', '# class Box[T]: ...
', 'class Box[T]: def __init__(self, value: T): ...; def map[U](self, f) -> "Box[U]": return Box(f(self.value)).', '{"driver": "b = Box(3)\nprint(b, b.map(str), b.map(lambda x: x * 2).map(str))\nprint([p.__name__ for p in Box.__type_params__])\nprint(b.map(str).value == \"3\")\n", "expected": ["Box(3) Box(''3'') Box(''6'')", "[''T'']", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-typevar-bound', 4, 'stdout', 'TypeVar с границей', 'Опишите протокол Comparable (метод __lt__(self, other) -> bool), переменную типа T = TypeVar("T", bound=Comparable) и функцию biggest(items: list[T]) -> T, возвращающую наибольший элемент.', 'from typing import Protocol, TypeVar
', 'class Comparable(Protocol): def __lt__(self, other) -> bool: ...; T = TypeVar("T", bound=Comparable).', '{"driver": "print(biggest([3, 1, 2]), biggest([\"b\", \"a\"]), biggest([2.5, 1.5]))\nprint(T.__bound__.__name__, T.__name__)\nprint(biggest.__annotations__[\"return\"] is T)\n", "expected": ["3 b 2.5", "Comparable T", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-overload', 5, 'stdout', 'Перегрузка для проверки типов', 'Опишите функцию first двумя заглушками @overload (str → str и list[int] → int) и одной настоящей реализацией, возвращающей первый элемент. typing.get_overloads(first) должен видеть две заглушки.', 'import typing
from typing import overload
', '@overload def first(x: str) -> str: ...; @overload def first(x: list[int]) -> int: ...; затем def first(x): return x[0].', '{"driver": "print(first(\"abc\"), first([5, 6]))\nprint(len(typing.get_overloads(first)))\n", "expected": ["a 5", "2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-self-builder', 6, 'stdout', 'Цепочки вызовов с Self', 'Напишите класс Query с методами where(cond) и limit(n): оба сохраняют настройки в экземпляре, возвращают self и аннотированы результатом typing.Self (чтобы наследники сохраняли свой тип). Метод build() возвращает строку вида «WHERE a AND b LIMIT 3».', 'from typing import Self
', 'build: части = []; если conds — "WHERE " + " AND ".join(conds); если limit не None — "LIMIT n"; соединить пробелом.', '{"driver": "class SqlQuery(Query):\n    pass\n\n\nq = SqlQuery().where(\"a\").where(\"b\").limit(3)\nprint(type(q).__name__, q.build())\nprint(Query().build() == \"\")\nprint(Query.where.__annotations__[\"return\"] is Self, Query.limit.__annotations__[\"return\"] is Self)\n", "expected": ["SqlQuery WHERE a AND b LIMIT 3", "True", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-typeddict-validate', 7, 'stdout', 'Проверка словаря по TypedDict', 'Напишите validate(data, schema): по подсказкам TypedDict (typing.get_type_hints(schema)) верните отсортированный список ошибок: «нет ключа K», «лишний ключ K», «K: ожидался T» (имя типа), если значение не того типа.', 'import typing


def validate(data, schema):
    pass
', 'hints = typing.get_type_hints(schema); пройдите по ключам hints и по ключам data.', '{"driver": "class User(typing.TypedDict):\n    name: str\n    age: int\n\n\nprint(validate({\"name\": \"Ann\", \"age\": 3}, User))\nprint(validate({\"name\": 5, \"extra\": 1}, User))\nprint(validate({}, User))\n", "expected": ["[]", "[''name: ожидался str'', ''лишний ключ extra'', ''нет ключа age'']", "[''нет ключа age'', ''нет ключа name'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 41, 'tp-describe-type', 8, 'stdout', 'Тип словами', 'Напишите describe_type(tp): строка вроде «list[int]», «dict[str, list[int]]», «int | None» по аннотации (используйте typing.get_origin и get_args; для обычных классов — имя класса, для NoneType — «None», для объединений — через « | »).', 'import types
import typing


def describe_type(tp):
    pass
', 'origin = typing.get_origin(tp); args = typing.get_args(tp); для Union и UnionType — join через " | "; Ellipsis выводите как «...».', '{"driver": "from typing import Optional\n\nfor t in [int, list[int], dict[str, list[int]], int | None, Optional[str], tuple[int, ...], type(None)]:\n    print(describe_type(t))\n", "expected": ["int", "list[int]", "dict[str, list[int]]", "int | None", "str | None", "tuple[int, ...]", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-names', 0, 'stdout', 'Порядок разрешения методов', 'Напишите mro_names(cls): список имён классов в порядке разрешения методов (без object). Используйте cls.__mro__.', 'def mro_names(cls):
    pass
', '[c.__name__ for c in cls.__mro__ if c is not object].', '{"driver": "class A: pass\nclass B(A): pass\nclass C(A): pass\nclass D(B, C): pass\nclass E(C, B): pass\n\n\nprint(mro_names(D))\nprint(mro_names(E))\nprint(mro_names(A))\n", "expected": ["[''D'', ''B'', ''C'', ''A'']", "[''E'', ''C'', ''B'', ''A'']", "[''A'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-super-chain', 1, 'stdout', 'Кооперативная цепочка в ромбе', 'Класс A уже написан (печатает «A» и ничего не вызывает дальше). Напишите B(A), C(A) и D(B, C): метод hello() каждого печатает своё имя и вызывает super().hello(), так что при D().hello() каждый класс отработает ровно один раз в порядке D, B, C, A.', 'class A:
    def hello(self):
        print("A")
', 'В каждом hello: print("X"); super().hello(). Ромб будет пройден по MRO D, B, C, A.', '{"driver": "D().hello()\nprint(\"--\")\nB().hello()\nprint([c.__name__ for c in D.__mro__])\n", "expected": ["D", "B", "C", "A", "--", "B", "A", "[''D'', ''B'', ''C'', ''A'', ''object'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-can-combine', 2, 'stdout', 'Можно ли объединить базы', 'Напишите can_combine(*bases): True, если можно создать класс с этими базами (в таком порядке), и False, если Питон не может построить согласованный MRO (TypeError).', 'def can_combine(*bases):
    pass
', 'try: type("X", bases, {}) except TypeError: return False; return True.', '{"driver": "class A: pass\nclass B(A): pass\nclass C(A): pass\n\n\nprint(can_combine(B, C), can_combine(B, A), can_combine(A, B))\nprint(can_combine(C, B), can_combine())\n", "expected": ["True True False", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-coop-init', 3, 'stdout', 'Кооперативный __init__', 'Напишите NameMixin и AgeMixin: каждый принимает свой именованный параметр (name или age), сохраняет его и передаёт остальные параметры дальше через super().__init__(**kwargs). Базовый Base уже «гасит» оставшиеся параметры в поле extra. Порядок баз в Person не должен влиять на результат.', 'class Base:
    def __init__(self, **kwargs):
        self.extra = kwargs
', 'def __init__(self, *, name, **kwargs): super().__init__(**kwargs); self.name = name.', '{"driver": "class Person(NameMixin, AgeMixin, Base):\n    pass\n\n\nclass Other(AgeMixin, NameMixin, Base):\n    pass\n\n\nfor cls in (Person, Other):\n    p = cls(name=\"Аня\", age=3, city=\"Омск\")\n    print(p.name, p.age, p.extra)\n", "expected": ["Аня 3 {''city'': ''Омск''}", "Аня 3 {''city'': ''Омск''}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-repr-mixin', 4, 'stdout', 'Миксин ReprMixin', 'Напишите миксин ReprMixin: __repr__ выдаёт имя класса и пары «поле=значение» атрибутов экземпляра в порядке создания (Point(x=1, y=2)). Он должен работать в сочетании с любым классом без собственного __init__.', 'class ReprMixin:
    pass
', '", ".join(f"{k}={v!r}" for k, v in vars(self).items()).', '{"driver": "class Point(ReprMixin):\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\n\nclass Base:\n    def __init__(self):\n        self.id = 7\n\n\nclass Item(ReprMixin, Base):\n    pass\n\n\nprint(Point(1, 2))\nprint(Item())\nprint([Point(0, 0)])\n", "expected": ["Point(x=1, y=2)", "Item(id=7)", "[Point(x=0, y=0)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-json-mixin', 5, 'stdout', 'Миксин JsonMixin', 'Напишите JsonMixin с методом to_json(): JSON-строка из атрибутов экземпляра с отсортированными ключами (json.dumps(..., sort_keys=True, ensure_ascii=False)) и классовым методом from_json(text), создающим объект без вызова __init__ и записывающим в него поля из JSON.', 'import json


class JsonMixin:
    pass
', 'from_json: obj = cls.__new__(cls); obj.__dict__.update(json.loads(text)); return obj.', '{"driver": "class User(JsonMixin):\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n\nu = User(\"Аня\", 30)\ntext = u.to_json()\nprint(text)\nv = User.from_json(text)\nprint(type(v).__name__, v.name, v.age)\n", "expected": ["{\"age\": 30, \"name\": \"Аня\"}", "User Аня 30"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-logging-mixin', 6, 'stdout', 'Миксин-обёртка через super', 'Класс Model уже умеет save() (возвращает «сохранено»). Напишите LoggingMixin: его save() записывает в список LOG строку «перед save», вызывает super().save(), записывает «после save» и возвращает результат. Миксин нужно ставить слева от Model.', 'LOG = []


class Model:
    def save(self):
        return "сохранено"
', 'class LoggingMixin: def save(self): LOG.append(...); result = super().save(); LOG.append(...); return result.', '{"driver": "class Logged(LoggingMixin, Model):\n    pass\n\n\nclass WrongOrder(Model, LoggingMixin):\n    pass\n\n\nprint(Logged().save(), LOG)\nLOG.clear()\nprint(WrongOrder().save(), LOG)\n", "expected": ["сохранено [''перед save'', ''после save'']", "сохранено []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-where-defined', 7, 'stdout', 'Где определён метод', 'Напишите where_defined(cls, name): имя первого класса в MRO, у которого имя name есть в собственном __dict__, или None, если нигде нет. А также chain(cls, name): список имён всех классов в MRO, определяющих это имя (в порядке MRO).', 'def where_defined(cls, name):
    pass


def chain(cls, name):
    pass
', 'for c in cls.__mro__: if name in vars(c): ...', '{"driver": "class A:\n    def f(self): ...\n    def g(self): ...\n\n\nclass B(A):\n    def f(self): ...\n\n\nclass C(A):\n    def f(self): ...\n    def h(self): ...\n\n\nclass D(B, C):\n    pass\n\n\nprint(where_defined(D, \"f\"), where_defined(D, \"g\"), where_defined(D, \"h\"), where_defined(D, \"zzz\"))\nprint(chain(D, \"f\"), chain(D, \"h\"))\n", "expected": ["B A C None", "[''B'', ''C'', ''A''] [''C'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 42, 'mro-validators', 8, 'stdout', 'Проверки на миксинах', 'Базовый Validator.validate(value) возвращает пустой список. Напишите NotEmpty (ошибка «пусто» для пустой строки) и NoDigits (ошибка «цифры» если в строке есть цифра): каждый вызывает super().validate(value) и добавляет свою ошибку. Классы собираются в любом сочетании.', 'class Validator:
    def validate(self, value):
        return []
', 'errors = super().validate(value); if не value: errors = errors + ["пусто"]; return errors.', '{"driver": "class Name(NotEmpty, NoDigits, Validator):\n    pass\n\n\nclass OnlyDigits(NoDigits, Validator):\n    pass\n\n\nprint(Name().validate(\"Аня\"))\nprint(Name().validate(\"\"))\nprint(Name().validate(\"a1\"))\nprint(OnlyDigits().validate(\"x9\"), OnlyDigits().validate(\"\"))\n", "expected": ["[]", "[''пусто'']", "[''цифры'']", "[''цифры''] []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 43, 'parallel-map-threads', 0, 'stdout', 'Параллельный map на потоках', 'Напишите функцию parallel_map(func, items, workers): применяет func к каждому элементу в пуле из workers потоков и возвращает список результатов В ИСХОДНОМ порядке. Используйте ThreadPoolExecutor.', 'from concurrent.futures import ThreadPoolExecutor


def parallel_map(func, items, workers):
    pass
', 'with ThreadPoolExecutor(max_workers=workers) as pool: return list(pool.map(func, items)).', '{"driver": "import time\ndef slow_square(x):\n    time.sleep(0.1)\n    return x * x\nt0 = time.perf_counter()\nres = parallel_map(slow_square, list(range(8)), 8)\nel = time.perf_counter() - t0\nprint(res)\nprint(el < 0.5)\nprint(parallel_map(str, [], 3))\n", "expected": ["[0, 1, 4, 9, 16, 25, 36, 49]", "True", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 43, 'locked-counter', 1, 'stdout', 'Счётчик под замком', 'Напишите функцию count_in_threads(threads, per_thread): запускает threads потоков, каждый из которых увеличивает общий счётчик на 1 ровно per_thread раз, и возвращает итоговое значение. Защитите счётчик замком Lock.', 'import threading


def count_in_threads(threads, per_thread):
    pass
', 'Общий счётчик — в списке или через nonlocal; внутри цикла: with lock: counter += 1; в конце join всех потоков.', '{"driver": "print(count_in_threads(4, 25000))\nprint(count_in_threads(1, 10))\nprint(count_in_threads(8, 0))\n", "expected": ["100000", "10", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 43, 'queue-worker', 2, 'stdout', 'Производитель и потребитель', 'Напишите функцию process_with_queue(items): главный поток кладёт элементы в queue.Queue, один рабочий поток берёт их и складывает в результат квадраты. Верните список квадратов в порядке поступления. Для остановки рабочего используйте сигнальное значение None.', 'import queue
import threading


def process_with_queue(items):
    pass
', 'while True: item = q.get(); if item is None: break; results.append(item * item) — после всех элементов положите None и сделайте join.', '{"driver": "print(process_with_queue([1, 2, 3, 4]))\nprint(process_with_queue([]))\nprint(process_with_queue(range(5)))\n", "expected": ["[1, 4, 9, 16]", "[]", "[0, 1, 4, 9, 16]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 43, 'first-completed', 3, 'stdout', 'Кто быстрее', 'Напишите функцию first_done(funcs): запускает все функции (без аргументов) в пуле потоков и возвращает результат той, что завершилась ПЕРВОЙ. Используйте as_completed.', 'from concurrent.futures import ThreadPoolExecutor, as_completed


def first_done(funcs):
    pass
', 'with ThreadPoolExecutor(len(funcs)) as pool: futures = [pool.submit(f) for f in funcs]; for fut in as_completed(futures): return fut.result().', '{"driver": "import time\ndef make(label, delay):\n    def f():\n        time.sleep(delay)\n        return label\n    return f\nprint(first_done([make(''медленная'', 0.3), make(''быстрая'', 0.05), make(''средняя'', 0.15)]))\nprint(first_done([make(''одна'', 0.01)]))\n", "expected": ["быстрая", "одна"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 43, 'stoppable-ticker', 4, 'stdout', 'Останавливаемый фоновый поток', 'Опишите класс Ticker: start() запускает фоновый поток, который каждые 0.02 секунды увеличивает атрибут ticks на 1; stop() останавливает его (через threading.Event) и дожидается завершения. После stop() тики больше не растут.', 'import threading


class Ticker:
    def __init__(self):
        self.ticks = 0
', 'self._stop = threading.Event(); в потоке: while not self._stop.is_set(): self.ticks += 1; self._stop.wait(0.02).', '{"driver": "import time\nt = Ticker()\nt.start()\ntime.sleep(0.25)\nt.stop()\nn = t.ticks\ntime.sleep(0.1)\nprint(n >= 3, t.ticks == n)\nprint(Ticker().ticks)\n", "expected": ["True True", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 43, 'limited-parallel', 5, 'stdout', 'Не больше N одновременно', 'Напишите функцию run_limited(tasks, limit): запускает все функции из tasks в потоках, но не позволяет работать одновременно более limit из них (Semaphore). Дождитесь завершения всех.', 'import threading


def run_limited(tasks, limit):
    pass
', 'sem = threading.Semaphore(limit); обёртка: with sem: task(); на каждую задачу — свой поток, затем join.', '{"driver": "import threading, time\nlock = threading.Lock()\nstate = {''now'': 0, ''max'': 0, ''done'': 0}\ndef task():\n    with lock:\n        state[''now''] += 1\n        state[''max''] = max(state[''max''], state[''now''])\n    time.sleep(0.05)\n    with lock:\n        state[''now''] -= 1\n        state[''done''] += 1\nrun_limited([task] * 10, 3)\nprint(state[''done''], state[''max''])\n", "expected": ["10 3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 43, 'collect-with-errors', 6, 'stdout', 'Результаты и ошибки', 'Напишите функцию run_all(funcs): запускает функции в пуле потоков и возвращает список в исходном порядке: для успешной — (''ok'', значение), для упавшей — (''error'', текст исключения).', 'from concurrent.futures import ThreadPoolExecutor


def run_all(funcs):
    pass
', 'futures = [pool.submit(f) for f in funcs]; затем try: (''ok'', fut.result()) / except Exception as e: (''error'', str(e)).', '{"driver": "def good():\n    return 42\ndef bad():\n    raise ValueError(''сбой'')\ndef zero():\n    return 1 / 0\nprint(run_all([good, bad, zero]))\nprint(run_all([]))\n", "expected": ["[(''ok'', 42), (''error'', ''сбой''), (''error'', ''division by zero'')]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 44, 'async-add-later', 0, 'stdout', 'Первая корутина', 'Напишите корутину add_later(a, b, delay=0.01): ждёт delay секунд (asyncio.sleep) и возвращает a + b.', 'import asyncio


async def add_later(a, b, delay=0.01):
    pass
', 'await asyncio.sleep(delay); return a + b.', '{"driver": "import asyncio\nprint(asyncio.run(add_later(2, 3)))\nprint(asyncio.run(add_later(''а'', ''б'', delay=0)))\nprint(type(add_later(1, 1)).__name__)\nasync def main():\n    return await add_later(10, 5)\nprint(asyncio.run(main()))\n", "expected": ["5", "аб", "coroutine", "15"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 44, 'async-fetch-all', 1, 'stdout', 'Все сразу', 'Напишите корутину fetch_all(delays): для каждой задержки из списка запускает корутину, которая ждёт столько секунд и возвращает строку «готово <i>» (i — номер с нуля). Все ожидания должны идти одновременно (gather); результаты — в порядке списка.', 'import asyncio


async def fetch_all(delays):
    pass
', 'Опишите вложенную async def one(i, d): await asyncio.sleep(d); return f''готово {i}'' и верните await asyncio.gather(*(one(i, d) for i, d in enumerate(delays))).', '{"driver": "import asyncio, time\nt0 = time.perf_counter()\nres = asyncio.run(fetch_all([0.3, 0.1, 0.2]))\nel = time.perf_counter() - t0\nprint(res)\nprint(el < 0.5)\nprint(asyncio.run(fetch_all([])))\n", "expected": ["[''готово 0'', ''готово 1'', ''готово 2'']", "True", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 44, 'async-with-timeout', 2, 'stdout', 'Ограничение по времени', 'Напишите корутину with_timeout(coro, seconds): ждёт результат корутины coro не дольше seconds секунд; если не уложилась — возвращает строку «таймаут».', 'import asyncio


async def with_timeout(coro, seconds):
    pass
', 'try: return await asyncio.wait_for(coro, seconds) / except TimeoutError: return ''таймаут''.', '{"driver": "import asyncio\nasync def job(delay, value):\n    await asyncio.sleep(delay)\n    return value\nprint(asyncio.run(with_timeout(job(0.05, ''успел''), 1)))\nprint(asyncio.run(with_timeout(job(5, ''не успел''), 0.1)))\n", "expected": ["успел", "таймаут"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 44, 'async-safe-all', 3, 'stdout', 'Результаты и ошибки', 'Напишите корутину run_safely(coros): запускает корутины конкурентно и возвращает список в исходном порядке: (''ok'', значение) для успешных и (''error'', текст) для упавших. Используйте gather с return_exceptions=True.', 'import asyncio


async def run_safely(coros):
    pass
', 'results = await asyncio.gather(*coros, return_exceptions=True); исключения — экземпляры BaseException.', '{"driver": "import asyncio\nasync def good(x):\n    await asyncio.sleep(0.01)\n    return x\nasync def bad():\n    raise ValueError(''сбой'')\nprint(asyncio.run(run_safely([good(1), bad(), good(3)])))\nprint(asyncio.run(run_safely([])))\n", "expected": ["[(''ok'', 1), (''error'', ''сбой''), (''ok'', 3)]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 44, 'async-bounded-gather', 4, 'stdout', 'Не больше N сразу', 'Напишите корутину bounded_gather(funcs, limit): funcs — список функций без аргументов, каждая возвращает корутину. Запустите их конкурентно, но так, чтобы одновременно выполнялось не больше limit (asyncio.Semaphore). Верните результаты в исходном порядке.', 'import asyncio


async def bounded_gather(funcs, limit):
    pass
', 'sem = asyncio.Semaphore(limit); async def run(f): async with sem: return await f(); затем gather(*(run(f) for f in funcs)).', '{"driver": "import asyncio\nstate = {''now'': 0, ''peak'': 0}\ndef make(i):\n    async def job():\n        state[''now''] += 1\n        state[''peak''] = max(state[''peak''], state[''now''])\n        await asyncio.sleep(0.02)\n        state[''now''] -= 1\n        return i * i\n    return job\nres = asyncio.run(bounded_gather([make(i) for i in range(10)], 3))\nprint(res)\nprint(state[''peak''])\n", "expected": ["[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]", "3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 44, 'async-generator-range', 5, 'stdout', 'Асинхронный генератор', 'Напишите асинхронный генератор async_range(n, delay): отдаёт числа от 0 до n - 1, ожидая delay секунд (asyncio.sleep) перед каждым.', 'import asyncio


async def async_range(n, delay=0.01):
    pass
', 'async def с yield внутри: for i in range(n): await asyncio.sleep(delay); yield i.', '{"driver": "import asyncio\nasync def main():\n    out = []\n    async for x in async_range(4):\n        out.append(x)\n    print(out)\n    print([x async for x in async_range(0)])\n    print(sum([x async for x in async_range(5, 0)]))\nasyncio.run(main())\n", "expected": ["[0, 1, 2, 3]", "[]", "10"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 44, 'async-queue-workers', 6, 'stdout', 'Пул воркеров', 'Напишите корутину process_all(items, workers): положите items в asyncio.Queue и обработайте их workers корутинами-воркерами (каждый берёт задание, ждёт 0.01 с и кладёт в результат квадрат). Верните отсортированный список квадратов. Воркеров после работы остановите.', 'import asyncio


async def process_all(items, workers):
    pass
', 'workers = [asyncio.create_task(worker()) ...]; await q.join(); затем cancel() у воркеров.', '{"driver": "import asyncio, time\nt0 = time.perf_counter()\nprint(asyncio.run(process_all(list(range(10)), 5)))\nprint(time.perf_counter() - t0 < 0.5)\nprint(asyncio.run(process_all([], 2)))\n", "expected": ["[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]", "True", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 44, 'async-retry', 7, 'stdout', 'Повторные попытки', 'Напишите корутину retry(make_coro, attempts, delay=0.01): вызывает make_coro() (возвращает корутину), и если она падает с исключением — ждёт delay и пробует снова, всего attempts раз. Если все попытки неудачны — поднимает последнее исключение.', 'import asyncio


async def retry(make_coro, attempts, delay=0.01):
    pass
', 'for i in range(attempts): try: return await make_coro() / except Exception as e: last = e; await asyncio.sleep(delay); после цикла raise last.', '{"driver": "import asyncio\ncalls = {''n'': 0}\nasync def flaky():\n    calls[''n''] += 1\n    if calls[''n''] < 3:\n        raise ConnectionError(''нет связи'')\n    return ''успех''\nprint(asyncio.run(retry(flaky, 5)), calls[''n''])\nasync def always_bad():\n    raise ValueError(''вечный сбой'')\ntry:\n    asyncio.run(retry(always_bad, 3))\nexcept ValueError as e:\n    print(''сдались:'', e)\n", "expected": ["успех 3", "сдались: вечный сбой"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 45, 'tcp-roundtrip', 0, 'stdout', 'Свой TCP-сервер', 'Напишите корутину shout(text): поднимите asyncio-сервер на 127.0.0.1 (порт 0), который читает строку, отвечает ею же заглавными буквами; подключитесь клиентом, отправьте text + перевод строки и верните ответ сервера (без перевода строки).', 'import asyncio


async def shout(text):
    pass
', 'start_server(handle, ''127.0.0.1'', 0); порт — server.sockets[0].getsockname()[1]; не забудьте drain и закрытие writer.', '{"driver": "import asyncio\nprint(asyncio.run(shout(''привет'')))\nprint(asyncio.run(shout(''abc def'')))\n", "expected": ["ПРИВЕТ", "ABC DEF"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 45, 'async-run-commands', 1, 'stdout', 'Команды одновременно', 'Напишите корутину run_codes(codes): для каждой строки кода запускает дочерний интерпретатор (sys.executable, ''-c'', код) через asyncio.create_subprocess_exec, и возвращает список выводов (stdout без пробелов по краям) в исходном порядке. Все процессы должны идти одновременно.', 'import asyncio
import sys


async def run_codes(codes):
    pass
', 'async def one(code): proc = await asyncio.create_subprocess_exec(sys.executable, ''-c'', code, stdout=asyncio.subprocess.PIPE); out, _ = await proc.communicate(); return out.decode().strip().', '{"driver": "import asyncio\nprint(asyncio.run(run_codes([''print(1 + 1)'', ''print(\"привет\")'', ''print(sum(range(5)))''])))\nprint(asyncio.run(run_codes([])))\n", "expected": ["[''2'', ''привет'', ''10'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 45, 'async-first-success', 2, 'stdout', 'Кто первый', 'Напишите корутину first_of(coros): запускает корутины конкурентно, возвращает результат ПЕРВОЙ завершившейся и отменяет остальные (asyncio.wait, FIRST_COMPLETED).', 'import asyncio


async def first_of(coros):
    pass
', 'tasks = [asyncio.create_task(c) for c in coros]; done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED); отмените pending и дождитесь их (gather с return_exceptions).', '{"driver": "import asyncio\nfinished = []\nasync def src(name, delay):\n    try:\n        await asyncio.sleep(delay)\n        finished.append(name)\n        return name\n    except asyncio.CancelledError:\n        finished.append(''отменён '' + name)\n        raise\nprint(asyncio.run(first_of([src(''медленный'', 0.4), src(''быстрый'', 0.05), src(''средний'', 0.2)])))\nprint(sorted(finished))\n", "expected": ["быстрый", "[''быстрый'', ''отменён медленный'', ''отменён средний'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 45, 'backoff-delays', 3, 'stdout', 'Растущая задержка', 'Напишите корутину retry_backoff(func, tries, base): вызывает корутинную функцию func(); при исключении ConnectionError ждёт base * 2 ** i секунд (i — номер неудачной попытки с нуля) через asyncio.sleep и пробует снова; на последней неудаче поднимает исключение.', 'import asyncio


async def retry_backoff(func, tries, base):
    pass
', 'for i in range(tries): try: return await func() / except ConnectionError: if i == tries - 1: raise; await asyncio.sleep(base * 2 ** i).', '{"driver": "import asyncio\ndelays = []\n_real = asyncio.sleep\nasync def fake_sleep(d, *a, **k):\n    delays.append(d)\nasyncio.sleep = fake_sleep\ncalls = {''n'': 0}\nasync def flaky():\n    calls[''n''] += 1\n    if calls[''n''] < 4:\n        raise ConnectionError(''нет'')\n    return ''ок''\nprint(asyncio.run(retry_backoff(flaky, 6, 0.5)), calls[''n''], delays)\ndelays.clear()\nasync def bad():\n    raise ConnectionError(''вечно'')\ntry:\n    asyncio.run(retry_backoff(bad, 3, 1))\nexcept ConnectionError as e:\n    print(''сдались'', e, delays)\nasyncio.sleep = _real\n", "expected": ["ок 4 [0.5, 1.0, 2.0]", "сдались вечно [1, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 45, 'graceful-workers', 4, 'stdout', 'Аккуратная остановка', 'Напишите корутину run_workers(names, duration): запустите по корутине-воркеру на каждое имя; воркер в цикле делает await asyncio.sleep(0.01), пока не поставлено событие остановки, а при завершении (в finally) добавляет своё имя в список. Через duration секунд поставьте событие и верните отсортированный список имён остановившихся воркеров.', 'import asyncio


async def run_workers(names, duration):
    pass
', 'stop = asyncio.Event(); async with asyncio.TaskGroup() as tg: создать задачи; await asyncio.sleep(duration); stop.set().', '{"driver": "import asyncio\nprint(asyncio.run(run_workers([''в'', ''а'', ''б''], 0.1)))\nprint(asyncio.run(run_workers([], 0.05)))\n", "expected": ["[''а'', ''б'', ''в'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 45, 'ctxvar-request-id', 5, 'stdout', 'Номер запроса в контексте', 'Опишите переменную request_id = contextvars.ContextVar(…, default=''-'') и корутину handle(rid): сохраняет rid в request_id, ждёт 0.01 с и возвращает строку «<rid>:<значение request_id>». Параллельные обработчики не должны мешать друг другу.', 'import asyncio
import contextvars

request_id = None


async def handle(rid):
    pass
', 'request_id = contextvars.ContextVar("request_id", default="-"); gather оборачивает каждую корутину в задачу с копией контекста.', '{"driver": "import asyncio\nasync def main():\n    r = await asyncio.gather(handle(''a''), handle(''b''), handle(''c''))\n    print(r)\n    print(request_id.get())\nasyncio.run(main())\n", "expected": ["[''a:a'', ''b:b'', ''c:c'']", "-"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 45, 'async-tests-for-total', 6, 'stdout', 'Тесты для асинхронной функции', 'Допишите класс TestTotal (unittest.IsolatedAsyncioTestCase): тесты корутины total(prices) — сумма чисел списка (для пустого — 0). Тесты должны пройти на верной реализации и упасть на каждой из трёх сломанных. Корутину вызывайте через await.', 'import unittest


class TestTotal(unittest.IsolatedAsyncioTestCase):
    async def test_example(self):
        pass  # await total([...])
', 'assertEqual(await total([1, 2, 3]), 6); пустой список → 0; отрицательные числа: await total([5, -3]) == 2; ещё один элемент в начале.', '{"driver": "import io\nimport asyncio\ndef run():\n    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestTotal))\n    return r.wasSuccessful() and r.testsRun > 0\nasync def good(p):\n    await asyncio.sleep(0)\n    return sum(p)\nasync def bad1(p):\n    return sum(p[1:])\nasync def bad2(p):\n    return sum(p) if p else None\nasync def bad3(p):\n    return sum(abs(x) for x in p)\nfor name, f in [(''верная'', good), (''ошибка 1'', bad1), (''ошибка 2'', bad2), (''ошибка 3'', bad3)]:\n    total = f\n    print(name, ''тесты прошли'' if run() else ''тесты упали'')\n", "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-countdown', 0, 'stdout', 'Асинхронный итератор-класс', 'Напишите класс AsyncCountdown(n): асинхронный итератор, который отдаёт n, n-1, …, 1 (перед каждым значением делает await asyncio.sleep(0)) и затем поднимает StopAsyncIteration. Используйте __aiter__ и __anext__.', 'import asyncio


class AsyncCountdown:
    def __init__(self, n):
        self.n = n
', '__aiter__ возвращает self; async def __anext__: если n <= 0 — raise StopAsyncIteration; иначе await asyncio.sleep(0), уменьшить n и вернуть значение.', '{"driver": "async def main():\n    out = []\n    async for x in AsyncCountdown(3):\n        out.append(x)\n    print(out)\n    it = aiter(AsyncCountdown(2))\n    print(await anext(it), await anext(it))\n    try:\n        await anext(it)\n    except StopAsyncIteration:\n        print(\"конец\")\n\n\nasyncio.run(main())\n", "expected": ["[3, 2, 1]", "2 1", "конец"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-agen-pages', 1, 'stdout', 'Постраничный генератор', 'Напишите асинхронный генератор items(fetch): fetch(page) — корутина, возвращающая список элементов страницы (страницы нумеруются с 1); пустой список означает конец. Генератор отдаёт элементы по одному и не запрашивает лишних страниц.', 'import asyncio


async def items(fetch):
    pass
', 'page = 1; while True: batch = await fetch(page); if not batch: return; for x in batch: yield x; page += 1.', '{"driver": "calls = []\n\n\nasync def fetch(page):\n    calls.append(page)\n    await asyncio.sleep(0)\n    data = {1: [\"a\", \"b\"], 2: [\"c\"], 3: []}\n    return data.get(page, [])\n\n\nasync def main():\n    out = []\n    async for x in items(fetch):\n        out.append(x)\n    print(out, calls)\n    calls.clear()\n    async for x in items(fetch):\n        break\n    print(calls)\n\n\nasyncio.run(main())\n", "expected": ["[''a'', ''b'', ''c''] [1, 2, 3]", "[1]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-filter-comp', 2, 'stdout', 'Асинхронное включение', 'Напишите async-функцию evens_squared(source): верните список квадратов чётных значений асинхронного источника, используя асинхронное включение списка.', 'import asyncio


async def evens_squared(source):
    pass
', 'return [x * x async for x in source if x % 2 == 0].', '{"driver": "async def numbers(n):\n    for i in range(n):\n        await asyncio.sleep(0)\n        yield i\n\n\nasync def main():\n    print(await evens_squared(numbers(7)))\n    print(await evens_squared(numbers(1)))\n\n\nasyncio.run(main())\n", "expected": ["[0, 4, 16, 36]", "[0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-async-with', 3, 'stdout', 'Класс-менеджер async with', 'Напишите класс Resource: __aenter__ печатает «открыт» и возвращает self (после await asyncio.sleep(0)), __aexit__ печатает «закрыт» и подавляет только KeyError (возвращает True), остальные исключения пропускает.', 'import asyncio


class Resource:
    pass
', 'async def __aexit__(self, et, ev, tb): print("закрыт"); return et is not None and issubclass(et, KeyError).', '{"driver": "async def main():\n    async with Resource() as r:\n        print(type(r).__name__)\n    async with Resource():\n        raise KeyError(\"x\")\n    print(\"KeyError подавлен\")\n    try:\n        async with Resource():\n            raise ValueError(\"y\")\n    except ValueError:\n        print(\"ValueError прошёл\")\n\n\nasyncio.run(main())\n", "expected": ["открыт", "Resource", "закрыт", "открыт", "закрыт", "KeyError подавлен", "открыт", "закрыт", "ValueError прошёл"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-asynccontextmanager', 4, 'stdout', '@asynccontextmanager', 'Напишите менеджер connection(name) через @asynccontextmanager: при входе печатает «открыто <name>» и отдаёт словарь {"name": name}, при выходе — в том числе при ошибке в блоке — печатает «закрыто <name>».', 'import asyncio
from contextlib import asynccontextmanager
', 'print вход; try: yield {...}; finally: print выход.', '{"driver": "async def main():\n    async with connection(\"db\") as c:\n        print(c)\n    try:\n        async with connection(\"cache\"):\n            raise RuntimeError(\"сбой\")\n    except RuntimeError as e:\n        print(\"ошибка:\", e)\n\n\nasyncio.run(main())\n", "expected": ["открыто db", "{''name'': ''db''}", "закрыто db", "открыто cache", "закрыто cache", "ошибка: сбой"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-take-aclosing', 5, 'stdout', 'Взять первые n и закрыть генератор', 'Напишите async-функцию take(agen, n): верните список первых n элементов асинхронного генератора и гарантируйте, что генератор закрыт к моменту возврата (его блок finally уже выполнен) — используйте contextlib.aclosing.', 'import asyncio
from contextlib import aclosing


async def take(agen, n):
    pass
', 'async with aclosing(agen) as g: out = []; async for x in g: if len(out) == n: break; out.append(x). Длину out проверяйте до добавления элемента.', '{"driver": "async def numbers():\n    try:\n        i = 0\n        while True:\n            await asyncio.sleep(0)\n            yield i\n            i += 1\n    finally:\n        print(\"очистка\")\n\n\nasync def main():\n    first = await take(numbers(), 2)\n    print(first)\n    print(await take(numbers(), 0))\n\n\nasyncio.run(main())\n", "expected": ["очистка", "[0, 1]", "очистка", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-interleave', 6, 'stdout', 'Чередование потоков', 'Напишите асинхронный генератор interleave(*sources): по кругу берёт по одному элементу из каждого непустого асинхронного источника (через anext) и отдаёт их; источники, исчерпавшие элементы, пропускаются; работа заканчивается, когда исчерпаны все.', 'import asyncio


async def interleave(*sources):
    pass
', 'active = list(sources); пока active: для каждого источника попробуйте await anext(src); при StopAsyncIteration уберите его из списка.', '{"driver": "async def gen(name, n):\n    for i in range(n):\n        await asyncio.sleep(0)\n        yield f\"{name}{i}\"\n\n\nasync def main():\n    print([x async for x in interleave(gen(\"a\", 2), gen(\"b\", 3), gen(\"c\", 1))])\n    print([x async for x in interleave()])\n\n\nasyncio.run(main())\n", "expected": ["[''a0'', ''b0'', ''c0'', ''a1'', ''b1'', ''b2'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-batched', 7, 'stdout', 'Пачки из асинхронного потока', 'Напишите асинхронный генератор batched(source, n): собирает элементы источника в списки по n штук и отдаёт их; последняя пачка может быть короче. n ≥ 1.', 'import asyncio


async def batched(source, n):
    pass
    yield
', 'batch = []; async for x in source: batch.append(x); если len == n — yield batch; batch = []; в конце, если batch не пуст — yield batch.', '{"driver": "async def numbers(k):\n    for i in range(k):\n        await asyncio.sleep(0)\n        yield i\n\n\nasync def main():\n    print([b async for b in batched(numbers(7), 3)])\n    print([b async for b in batched(numbers(4), 2)])\n    print([b async for b in batched(numbers(0), 5)])\n\n\nasyncio.run(main())\n", "expected": ["[[0, 1, 2], [3, 4, 5], [6]]", "[[0, 1], [2, 3]]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 46, 'aio-limiter', 8, 'stdout', 'Ограничитель параллелизма', 'Напишите класс Limiter(n) — асинхронный менеджер контекста, который пускает внутрь блока не больше n корутин одновременно (на основе asyncio.Semaphore). __aenter__ захватывает место, __aexit__ освобождает.', 'import asyncio


class Limiter:
    def __init__(self, n):
        pass
', 'self._sem = asyncio.Semaphore(n); async def __aenter__(self): await self._sem.acquire(); async def __aexit__(...): self._sem.release().', '{"driver": "active = 0\npeak = 0\n\n\nasync def job(limiter, i):\n    global active, peak\n    async with limiter:\n        active += 1\n        peak = max(peak, active)\n        await asyncio.sleep(0)\n        await asyncio.sleep(0)\n        active -= 1\n    return i\n\n\nasync def main():\n    limiter = Limiter(2)\n    results = await asyncio.gather(*(job(limiter, i) for i in range(5)))\n    print(results, peak)\n\n\nasyncio.run(main())\n", "expected": ["[0, 1, 2, 3, 4] 2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-weak-cache', 0, 'stdout', 'Кэш без утечек', 'Напишите ObjectCache на WeakValueDictionary: метод get(key, factory) возвращает кэшированный объект, а если его нет (или он уже умер), создаёт через factory() и запоминает; __len__ — число живых записей. Кэш не должен продлевать жизнь объектов.', 'import weakref


class ObjectCache:
    pass
', 'self._data = weakref.WeakValueDictionary(); get: obj = self._data.get(key); если None — создать и положить.', '{"driver": "import gc\n\n\nclass Thing:\n    pass\n\n\nc = ObjectCache()\na = c.get(\"x\", Thing)\nb = c.get(\"x\", Thing)\nprint(a is b, len(c))\ndel a, b\ngc.collect()\nprint(len(c))\n", "expected": ["True 1", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-weak-callback', 1, 'stdout', 'Слабая ссылка с обратным вызовом', 'Напишите watch(obj, callback): возвращает слабую ссылку на obj, которая при смерти объекта вызывает callback(имя_типа), где имя_типа — type(obj).__name__, запомненное заранее.', 'import weakref


def watch(obj, callback):
    pass
', 'name = type(obj).__name__; return weakref.ref(obj, lambda _ref: callback(name)).', '{"driver": "class Thing:\n    pass\n\n\nlog = []\nt = Thing()\nr = watch(t, log.append)\nprint(r() is t, log)\ndel t\nprint(log, r())\n", "expected": ["True []", "[''Thing''] None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-finalize', 2, 'stdout', 'finalize вместо __del__', 'Напишите track(name, log): создаёт и возвращает объект Handle, а через weakref.finalize регистрирует запись «закрыт <name>» в список log при смерти объекта. Класс Handle без __del__.', 'import weakref


class Handle:
    pass


def track(name, log):
    pass
', 'h = Handle(); weakref.finalize(h, log.append, f"закрыт {name}"); return h.', '{"driver": "log = []\nh = track(\"a\", log)\nprint(log)\ndel h\nprint(log)\nh2 = track(\"b\", log)\nprint(log, type(h2).__name__, hasattr(Handle, \"__del__\"))\n", "expected": ["[]", "[''закрыт a'']", "[''закрыт a''] Handle False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-cycle-gc', 3, 'stdout', 'Цикл и сборщик мусора', 'Напишите cycle_demo(): отключите сборщик (gc.disable()), создайте два объекта Node, ссылающихся друг на друга, возьмите слабую ссылку на первый и удалите оба имени; верните кортеж (жив_до_сборки, жив_после_сборки), где «после» — после gc.collect(). В конце включите сборщик обратно.', 'import gc
import weakref


class Node:
    pass


def cycle_demo():
    pass
', 'a.other = b; b.other = a; ref = weakref.ref(a); del a, b; before = ref() is not None; gc.collect(); after = ref() is not None; в finally — gc.enable().', '{"driver": "print(cycle_demo())\nprint(gc.isenabled())\n", "expected": ["(True, False)", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-deepcopy-protocol', 4, 'stdout', 'Свой __deepcopy__', 'У Document есть текст, кэш (словарь) и список дочерних документов. Напишите __deepcopy__(self, memo): текст и дочерние документы копируются глубоко (передайте memo), а кэш в копии должен быть новым пустым словарём.', 'class Document:
    def __init__(self, text, children=None):
        self.text = text
        self.children = children or []
        self.cache = {}
', 'new = type(self)(self.text, copy.deepcopy(self.children, memo)); return new (кэш создаётся пустым в __init__). Не забудьте import copy.', '{"driver": "import copy\n\nd = Document(\"root\", [Document(\"child\")])\nd.cache[\"k\"] = 1\nd.children[0].cache[\"z\"] = 2\nc = copy.deepcopy(d)\nprint(c.text, c.children[0].text, c.cache, c.children[0].cache)\nprint(c is not d, c.children[0] is not d.children[0], d.cache)\n", "expected": ["root child {} {}", "True True {''k'': 1}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-peak-bytes', 5, 'stdout', 'Пик памяти через tracemalloc', 'Напишите peak_bytes(func): запустите tracemalloc, вызовите func(), верните пиковое число выделенных байт (get_traced_memory()[1]) и остановите tracemalloc.', 'import tracemalloc


def peak_bytes(func):
    pass
', 'tracemalloc.start(); func(); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop(); return peak.', '{"driver": "big = peak_bytes(lambda: [0] * 100000)\nsmall = peak_bytes(lambda: None)\nprint(big > 700000, small < 5000)\nprint(tracemalloc.is_tracing())\n", "expected": ["True True", "False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-lazy-sum', 6, 'stdout', 'Сумма квадратов без списка', 'Функция sum_squares(n) считает сумму квадратов 0..n-1, но строит для этого весь список. Перепишите её так, чтобы лишние данные в памяти не накапливались (генераторное выражение), результат не должен измениться.', 'def sum_squares(n):
    squares = [i * i for i in range(n)]
    return sum(squares)
', 'return sum(i * i for i in range(n)).', '{"driver": "import tracemalloc\n\ntracemalloc.start()\nresult = sum_squares(100000)\npeak = tracemalloc.get_traced_memory()[1]\ntracemalloc.stop()\nprint(result)\nprint(peak < 50000)\n", "expected": ["333328333350000", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-lru-bound', 7, 'stdout', 'Ограничить кэш', 'slow_square кэширует результаты без ограничения (maxsize=None), поэтому память растёт вечно. Ограничьте кэш 128 записями, чтобы последние вызовы по-прежнему попадали в кэш.', 'from functools import lru_cache


@lru_cache(maxsize=None)
def slow_square(n):
    return n * n
', '@lru_cache(maxsize=128).', '{"driver": "for i in range(1000):\n    slow_square(i)\ninfo = slow_square.cache_info()\nprint(info.currsize, info.maxsize)\nslow_square(999)\nprint(slow_square.cache_info().hits)\n", "expected": ["128 128", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 47, 'mem-memoryview', 8, 'stdout', 'Срез без копирования', 'Напишите middle(data, start, stop): верните срез буфера data[start:stop] как memoryview (без копирования), чтобы изменения в исходном bytearray были видны через срез, а запись через срез меняла исходный буфер.', 'def middle(data, start, stop):
    pass
', 'return memoryview(data)[start:stop].', '{"driver": "data = bytearray(b\"abcdef\")\nv = middle(data, 1, 4)\nprint(bytes(v))\ndata[2] = ord(\"X\")\nprint(bytes(v))\nv[0] = ord(\"B\")\nprint(data)\nprint(v.obj is data)\n", "expected": ["b''bcd''", "b''bXd''", "bytearray(b''aBXdef'')", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-pyc-path', 0, 'stdout', 'Где лежит .pyc', 'Напишите pyc_path(source): путь к файлу кэша байт-кода для исходника (используйте importlib.util.cache_from_source). Для /app/mod.py это /app/__pycache__/mod.<метка-версии>.pyc.', 'import importlib.util


def pyc_path(source):
    pass
', 'importlib.util.cache_from_source(source).', '{"driver": "import sys\n\np = pyc_path(\"/app/mod.py\")\nprint(p == f\"/app/__pycache__/mod.{sys.implementation.cache_tag}.pyc\")\nprint(p.startswith(\"/app/__pycache__/\"), p.endswith(\".pyc\"))\n", "expected": ["True", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-switch-interval', 1, 'stdout', 'Временный интервал переключения', 'Напишите менеджер контекста switch_interval(value): внутри блока sys.getswitchinterval() равен value, а после выхода (даже при ошибке) возвращается прежнее значение. Реализуйте через @contextmanager и sys.setswitchinterval.', 'import sys
from contextlib import contextmanager
', 'old = sys.getswitchinterval(); sys.setswitchinterval(value); try: yield; finally: sys.setswitchinterval(old).', '{"driver": "before = sys.getswitchinterval()\nwith switch_interval(0.001):\n    inside = sys.getswitchinterval()\nafter = sys.getswitchinterval()\nprint(inside, after == before)\ntry:\n    with switch_interval(0.02):\n        raise RuntimeError\nexcept RuntimeError:\n    print(sys.getswitchinterval() == before)\n", "expected": ["0.001 True", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-locked-account', 2, 'stdout', 'Замок против гонки', 'В Account метод deposit читает баланс, «задумывается» (time.sleep(0) отдаёт управление другому потоку) и записывает результат — из-за этого параллельные вклады теряются. Исправьте класс замком threading.Lock, чтобы 4 потока по 100 вкладов дали ровно 400.', 'import threading
import time


class Account:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        current = self.balance
        time.sleep(0)
        self.balance = current + amount
', 'self._lock = threading.Lock() в __init__; в deposit: with self._lock: ...', '{"driver": "acc = Account()\n\n\ndef work():\n    for _ in range(100):\n        acc.deposit(1)\n\n\nthreads = [threading.Thread(target=work) for _ in range(4)]\nfor t in threads:\n    t.start()\nfor t in threads:\n    t.join()\nprint(acc.balance)\n", "expected": ["400"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-parallel-map', 3, 'stdout', 'Параллельный map на потоках', 'Напишите parallel_map(func, items, workers=4): примените func к элементам в пуле потоков (ThreadPoolExecutor) и верните список результатов в порядке входа. Исключение из func должно пробрасываться вызывающему.', 'from concurrent.futures import ThreadPoolExecutor


def parallel_map(func, items, workers=4):
    pass
', 'with ThreadPoolExecutor(workers) as pool: return list(pool.map(func, items)).', '{"driver": "import time\n\n\ndef slow(x):\n    time.sleep(0.01 * (5 - x))\n    return x * x\n\n\nprint(parallel_map(slow, range(5)))\nprint(parallel_map(str, []))\n\n\ndef bad(x):\n    if x == 2:\n        raise ValueError(\"два\")\n    return x\n\n\ntry:\n    parallel_map(bad, range(4))\nexcept ValueError as e:\n    print(\"ValueError\", e)\n", "expected": ["[0, 1, 4, 9, 16]", "[]", "ValueError два"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-queue-pipeline', 4, 'stdout', 'Производитель и потребитель', 'Напишите consume_sum(items): поток-производитель кладёт числа в queue.Queue, а в конце — признак окончания None; поток-потребитель суммирует числа до None. Верните сумму. Общие данные передаются только через очередь.', 'import queue
import threading


def consume_sum(items):
    pass
', 'q = queue.Queue(); производитель: for x in items: q.put(x); q.put(None); потребитель: while (x := q.get()) is not None: total += x.', '{"driver": "print(consume_sum(range(1, 101)))\nprint(consume_sum([]))\nprint(consume_sum([5]))\n", "expected": ["5050", "0", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-global-names', 5, 'stdout', 'Какие глобальные имена читает функция', 'Напишите global_names(func): отсортированный список имён, которые функция читает как глобальные (команды LOAD_GLOBAL из dis.get_instructions); параметры и локальные имена не считаются.', 'import dis


def global_names(func):
    pass
', '{i.argval for i in dis.get_instructions(func) if i.opname == "LOAD_GLOBAL"}.', '{"driver": "def helper(x):\n    return x\n\n\ndef f(x, y):\n    z = len(x) + helper(y)\n    return z\n\n\ndef g(a):\n    b = a + 1\n    return b\n\n\nprint(global_names(f))\nprint(global_names(g))\n", "expected": ["[''helper'', ''len'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-runtime-info', 6, 'stdout', 'Паспорт интерпретатора', 'Напишите runtime_info(): словарь с ключами gil_enabled (sys._is_gil_enabled(), а если функции нет — True), free_threaded_build (bool от sysconfig.get_config_var("Py_GIL_DISABLED")) и switch_interval (sys.getswitchinterval()).', 'import sys
import sysconfig


def runtime_info():
    pass
', 'check = getattr(sys, "_is_gil_enabled", lambda: True); bool(sysconfig.get_config_var("Py_GIL_DISABLED")).', '{"driver": "info = runtime_info()\nprint(sorted(info))\nprint(info[\"gil_enabled\"], info[\"free_threaded_build\"], info[\"switch_interval\"])\n", "expected": ["[''free_threaded_build'', ''gil_enabled'', ''switch_interval'']", "True False 0.005"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-compile-run', 7, 'stdout', 'Скомпилировать один раз, выполнить много', 'Напишите compile_expr(source): скомпилируйте выражение один раз (compile с режимом eval, имя файла «<expr>») и верните функцию evaluate(**names), которая вычисляет его при заданных значениях переменных, не разбирая текст заново.', 'def compile_expr(source):
    pass
', 'code = compile(source, "<expr>", "eval"); def evaluate(**names): return eval(code, {"__builtins__": {}}, names).', '{"driver": "ev = compile_expr(\"x * 2 + y\")\nprint(ev(x=1, y=1), ev(x=5, y=0), ev(x=10, y=-3))\ntry:\n    ev(x=1)\nexcept NameError:\n    print(\"NameError\")\ntry:\n    compile_expr(\"1 +\")\nexcept SyntaxError:\n    print(\"SyntaxError\")\n", "expected": ["3 10 17", "NameError", "SyntaxError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 48, 'in-thread-local', 8, 'stdout', 'Свои данные у каждого потока', 'Функция worker_values(n) запускает n потоков: каждый записывает в общий объект state своё число (индекс), ждёт и читает его обратно. Сейчас state общий, поэтому потоки перетирают друг друга. Замените state на threading.local(), чтобы у каждого потока были свои данные и результат совпал с индексами.', 'import threading
import time

state = type("Shared", (), {})()


def worker_values(n):
    results = [None] * n

    def work(i):
        state.value = i
        time.sleep(0.02)
        results[i] = state.value

    threads = [threading.Thread(target=work, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results
', 'state = threading.local() — атрибуты такого объекта у каждого потока свои.', '{"driver": "print(worker_values(5))\nprint(worker_values(1))\nprint(isinstance(state, threading.local))\n", "expected": ["[0, 1, 2, 3, 4]", "[0]", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-dedupe', 0, 'stdout', 'Дубликаты за линейное время', 'Функция dedupe(items) убирает повторы, сохраняя порядок первых вхождений. Сейчас она работает квадратично и не укладывается во время на больших данных. Ускорьте её (используйте множество уже увиденных элементов).', 'def dedupe(items):
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out
', 'seen = set(); для каждого x: если x не в seen — добавить в seen и в результат.', '{"driver": "data = list(range(150000)) + list(range(50000))\nresult = dedupe(data)\nprint(len(result), result[:3], result[-1])\nprint(dedupe([3, 1, 3, 2, 1]))\n", "expected": ["150000 [0, 1, 2] 149999", "[3, 1, 2]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-top-words', 1, 'stdout', 'Самые частые слова', 'top_words(words, k) возвращает k самых частых слов в виде пар (слово, число) — по убыванию числа, при равенстве по алфавиту. Текущая версия для каждого слова считает words.count и не укладывается во время на большом входе. Ускорьте её (collections.Counter).', 'def top_words(words, k):
    counts = [(w, words.count(w)) for w in set(words)]
    counts.sort(key=lambda p: (-p[1], p[0]))
    return counts[:k]
', 'Counter(words).items(), затем sorted с ключом (-число, слово) и срез [:k].', '{"driver": "words = [f\"w{i % 50000}\" for i in range(200000)] + [\"w7\"] * 5 + [\"w3\"] * 3\nprint(top_words(words, 3))\nprint(top_words([\"b\", \"a\", \"b\", \"a\", \"c\"], 2))\nprint(top_words([], 5))\n", "expected": ["[(''w7'', 9), (''w3'', 7), (''w0'', 4)]", "[(''a'', 2), (''b'', 2)]", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-fib-cache', 2, 'stdout', 'Фибоначчи с кэшем', 'Рекурсивная fib(n) пересчитывает одно и то же и не укладывается во время даже для n = 90. Добавьте кэширование (functools.cache), не меняя логику.', 'def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
', 'from functools import cache и @cache над def fib.', '{"driver": "print(fib(90))\nprint(fib(10), fib(1), fib(0))\n", "expected": ["2880067194370816120", "55 1 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-bisect-count', 3, 'stdout', 'Сколько чисел в диапазонах', 'count_in_ranges(nums, queries): nums — отсортированный список, queries — пары (lo, hi); для каждой верните, сколько чисел nums лежит в [lo, hi]. Текущая версия сканирует список для каждого запроса и слишком медленна. Используйте модуль bisect.', 'def count_in_ranges(nums, queries):
    return [sum(1 for x in nums if lo <= x <= hi) for lo, hi in queries]
', 'bisect_right(nums, hi) - bisect_left(nums, lo).', '{"driver": "nums = sorted((i * 7919) % 200003 for i in range(200000))\nqueries = [((i * 37) % 100000, (i * 37) % 100000 + 50000) for i in range(5000)]\nres = count_in_ranges(nums, queries)\nprint(len(res), sum(res))\nprint(res[:3] == [sum(1 for x in nums if lo <= x <= hi) for lo, hi in queries[:3]])\nprint(count_in_ranges([1, 2, 2, 3], [(2, 2), (0, 10), (5, 6)]))\n", "expected": ["5000 250005000", "True", "[2, 4, 0]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-window-max', 4, 'stdout', 'Максимум в скользящем окне', 'window_max(nums, k) возвращает максимумы всех окон длины k. Текущая версия берёт max от среза для каждого окна и слишком медленна при большом k. Ускорьте (монотонная очередь collections.deque с индексами).', 'def window_max(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
', 'deque хранит индексы по убыванию значений: убирайте с конца меньшие новому, с начала — выпавшие из окна.', '{"driver": "nums = [(i * 31337) % 1000003 for i in range(200000)]\nres = window_max(nums, 20000)\nprint(len(res), res[0], res[-1])\nprint(res[:3] == [max(nums[i:i + 20000]) for i in range(3)])\nprint(window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))\n", "expected": ["180001 999937 1000002", "True", "[3, 3, 5, 5, 6, 7]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-range-sum', 5, 'stdout', 'Суммы на отрезках', 'Класс RangeSum(data) отвечает на запросы query(l, r) — сумма data[l:r]. Сейчас каждый запрос считает сумму заново и слишком медленен при множестве запросов. Подготовьте префиксные суммы в __init__, чтобы запрос выполнялся за константу.', 'class RangeSum:
    def __init__(self, data):
        self.data = list(data)

    def query(self, l, r):
        return sum(self.data[l:r])
', 'prefix[i] = сумма первых i элементов; ответ prefix[r] - prefix[l]; itertools.accumulate с начальным 0.', '{"driver": "rs = RangeSum(range(200000))\ntotal = sum(rs.query(i % 1000, 100000 + i % 1000) for i in range(200000))\nprint(total)\nprint(rs.query(0, 5), rs.query(10, 10), rs.query(3, 4))\n", "expected": ["1009980000000000", "10 0 3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-call-counts', 6, 'stdout', 'Число вызовов через cProfile', 'Напишите call_counts(func): запустите func() под cProfile и верните словарь «имя функции → число вызовов» только для функций, определённых в том же файле, что и func (сравнивайте func.__code__.co_filename с именем файла в статистике).', 'import cProfile
import pstats


def call_counts(func):
    pass
', 'pr = cProfile.Profile(); pr.runcall(func); stats = pstats.Stats(pr).stats; ключи — (файл, строка, имя), значения — (cc, nc, tt, ct, callers).', '{"driver": "def helper(x):\n    return x + 1\n\n\ndef other():\n    pass\n\n\ndef work():\n    for i in range(5):\n        helper(i)\n    other()\n    other()\n\n\nprint(sorted(call_counts(work).items()))\n", "expected": ["[(''helper'', 5), (''other'', 2), (''work'', 1)]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-bench', 7, 'stdout', 'Свой замер времени', 'Напишите bench(func, repeat=5, number=20): с помощью timeit.repeat запустите func по number раз в каждой из repeat серий и верните минимальное время одного вызова (в секундах, число с плавающей точкой).', 'import timeit


def bench(func, repeat=5, number=20):
    pass
', 'min(timeit.repeat(func, repeat=repeat, number=number)) / number.', '{"driver": "fast = bench(lambda: sum(range(10)))\nslow = bench(lambda: sum(range(100000)))\nprint(isinstance(fast, float), fast > 0, slow > fast * 20)\ncalls = []\nbench(lambda: calls.append(1), repeat=3, number=4)\nprint(len(calls))\n", "expected": ["True True True", "12"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 49, 'pf-two-sum', 8, 'stdout', 'Два числа с заданной суммой', 'two_sum(nums, target): индексы (i, j), i < j, двух чисел с суммой target, или None, если такой пары нет. Двойной цикл на больших данных не укладывается во время: используйте словарь «значение → индекс» и один проход.', 'def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None
', 'seen = {}; для каждого i: need = target - nums[i]; если need в seen — вернуть (seen[need], i); иначе seen[nums[i]] = i.', '{"driver": "nums = list(range(0, 200000, 2))\nprint(two_sum(nums, nums[-1] + nums[-2]))\nprint(two_sum(nums, 1))\nprint(two_sum([3, 2, 4], 6), two_sum([1], 2))\n", "expected": ["(99998, 99999)", "None", "(1, 2) None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-parse-requirement', 0, 'stdout', 'Разбор строки зависимости', 'Напишите parse_requirement(text): из строки вида «requests>=2.31,<3» верните кортеж (имя, список пар (оператор, версия)). Пробелы вокруг частей игнорируйте, «extras» в квадратных скобках отбрасывайте. Операторы: ==, !=, <=, >=, ~=, <, >. Строку, которую нельзя разобрать, отвергайте ValueError.', 'import re


def parse_requirement(text):
    pass
', 'Регулярка для имени ^([A-Za-z0-9._-]+)(?:\[[^\]]*\])?(.*)$, остаток разбейте по запятым и разберите оператор и версию.', '{"driver": "print(parse_requirement(\"requests>=2.31,<3\"))\nprint(parse_requirement(\"flask\"))\nprint(parse_requirement(\"  httpx[http2] ~= 0.27.2 \"))\nprint(parse_requirement(\"pkg == 1.0 , != 1.0.1\"))\nfor bad in (\"bad name!\", \"\", \">=1.0\"):\n    try:\n        parse_requirement(bad)\n    except ValueError:\n        print(\"ValueError\")\n", "expected": ["(''requests'', [(''>='', ''2.31''), (''<'', ''3'')])", "(''flask'', [])", "(''httpx'', [(''~='', ''0.27.2'')])", "(''pkg'', [(''=='', ''1.0''), (''!='', ''1.0.1'')])", "ValueError", "ValueError", "ValueError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-compare-versions', 1, 'stdout', 'Сравнение версий', 'Напишите compare_versions(a, b): -1, 0 или 1 для версий вида «1.10.2». Сравнивайте по числам, а не по строкам («1.10» новее «1.2»), недостающие части считайте нулями («1.0» равно «1.0.0»).', 'def compare_versions(a, b):
    pass
', 'Разбейте по точкам в списки int, дополните нулями до одной длины и сравните списки.', '{"driver": "import functools\n\nprint(compare_versions(\"1.10\", \"1.2\"), compare_versions(\"1.0\", \"1.0.0\"), compare_versions(\"2.0.1\", \"2.1\"))\nvs = [\"1.10\", \"1.2\", \"1.9.5\", \"1.2.1\", \"0.9\"]\nprint(sorted(vs, key=functools.cmp_to_key(compare_versions)))\nprint(sorted(vs))\n", "expected": ["1 0 -1", "[''0.9'', ''1.2'', ''1.2.1'', ''1.9.5'', ''1.10'']", "[''0.9'', ''1.10'', ''1.2'', ''1.2.1'', ''1.9.5'']"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-satisfies', 2, 'stdout', 'Подходит ли версия под условие', 'Функция compare_versions уже есть. Напишите satisfies(version, spec): spec — несколько условий через запятую (>=, >, <=, <, ==, !=, ~=). Совместимый выпуск ~=1.4.2 значит «>=1.4.2 и версия начинается с 1.4», а ~=1.4 — «>=1.4 и начинается с 1».', 'def compare_versions(a, b):
    pa = [int(x) for x in a.split(".")]
    pb = [int(x) for x in b.split(".")]
    n = max(len(pa), len(pb))
    pa += [0] * (n - len(pa))
    pb += [0] * (n - len(pb))
    return (pa > pb) - (pa < pb)


def satisfies(version, spec):
    pass
', 'Для ~=: нижняя граница >= spec и совпадение всех частей версии, кроме последней части spec.', '{"driver": "print(satisfies(\"1.5\", \">=1.2,<2\"), satisfies(\"2.0\", \">=1.2,<2\"), satisfies(\"1.0\", \">1.0\"))\nprint(satisfies(\"1.4.9\", \"~=1.4.2\"), satisfies(\"1.5.0\", \"~=1.4.2\"), satisfies(\"1.4.1\", \"~=1.4.2\"))\nprint(satisfies(\"1.9\", \"~=1.4\"), satisfies(\"2.0\", \"~=1.4\"))\nprint(satisfies(\"1.0.0\", \"==1.0\"), satisfies(\"1.2\", \"!=1.2\"))\n", "expected": ["True False False", "True False False", "True False", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-read-pyproject', 3, 'stdout', 'Чтение pyproject.toml', 'Напишите project_info(text): разберите TOML модулем tomllib и верните кортеж (имя, версия, требуемый Python, список зависимостей) из раздела [project]. Если какого-то поля нет — подставляйте None (для зависимостей — пустой список).', 'import tomllib


def project_info(text):
    pass
', 'data = tomllib.loads(text).get("project", {}); data.get("name") и так далее.', '{"driver": "text = ''''''\n[project]\nname = \"shop\"\nversion = \"0.3.0\"\nrequires-python = \">=3.12\"\ndependencies = [\"httpx>=0.27\", \"rich\"]\n\n[tool.ruff]\nline-length = 100\n''''''\nprint(project_info(text))\nprint(project_info(\"[project]\\nname = ''x''\"))\nprint(project_info(\"\"))\n", "expected": ["(''shop'', ''0.3.0'', ''>=3.12'', [''httpx>=0.27'', ''rich''])", "(''x'', None, None, [])", "(None, None, None, [])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-entry-point', 4, 'stdout', 'Точка входа', 'Напишите resolve_entry_point(spec): строка вида «пакет.модуль:функция» (как в [project.scripts]) превращается в вызываемый объект; допускается вложенное имя через точку после двоеточия. Формат без двоеточия — ValueError; несуществующий модуль — ImportError, несуществующее имя — AttributeError.', 'import importlib


def resolve_entry_point(spec):
    pass
', 'module, sep, attr = spec.partition(":"); если нет sep — ValueError; затем import_module и getattr по частям attr.split(".").', '{"driver": "print(resolve_entry_point(\"json:dumps\")({\"a\": 1}))\nprint(resolve_entry_point(\"os.path:join\")(\"a\", \"b\"))\nprint(resolve_entry_point(\"collections:OrderedDict.fromkeys\")(\"ab\"))\nfor bad, exc in ((\"json\", ValueError), (\"nomod_zz:f\", ImportError), (\"json:zzz\", AttributeError)):\n    try:\n        resolve_entry_point(bad)\n    except exc:\n        print(exc.__name__)\n", "expected": ["{\"a\": 1}", "a/b", "OrderedDict({''a'': None, ''b'': None})", "ValueError", "ImportError", "AttributeError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-find-packages', 5, 'stdout', 'Поиск пакетов в каталоге', 'Напишите find_packages(root): отсортированный список полных имён пакетов в каталоге root — каталогов с __init__.py. Вглубь заходите только внутрь пакетов (если родитель не пакет, вложенные не считаются).', 'import os


def find_packages(root):
    pass
', 'Рекурсивная функция: для каждого подкаталога с __init__.py добавьте имя и спуститесь внутрь с префиксом.', '{"driver": "import pathlib\nimport tempfile\n\nwith tempfile.TemporaryDirectory() as tmp:\n    base = pathlib.Path(tmp)\n    for rel in [\"shop/__init__.py\", \"shop/utils/__init__.py\", \"shop/data/readme.txt\", \"tests/test_a.py\", \"other/__init__.py\", \"shop/data/sub/__init__.py\", \"shop/utils/deep/__init__.py\"]:\n        f = base / rel\n        f.parent.mkdir(parents=True, exist_ok=True)\n        f.write_text(\"\")\n    print(find_packages(str(base)))\n    print(find_packages(str(base / \"tests\")))\n", "expected": ["[''other'', ''shop'', ''shop.utils'', ''shop.utils.deep'']", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-cli-main', 6, 'stdout', 'Командная строка проекта', 'Напишите main(argv=None): argparse с обязательным --name, необязательным --times (целое, по умолчанию 1) и флагом --shout. Печатает приветствие «Здравствуйте, <name>!» нужное число раз (с --shout — в верхнем регистре) и возвращает 0. Ошибка аргументов — обычное поведение argparse (SystemExit с кодом 2).', 'import argparse


def main(argv=None):
    pass
', 'parser = argparse.ArgumentParser(); parser.add_argument("--name", required=True); --times type=int default=1; --shout action="store_true".', '{"driver": "print(main([\"--name\", \"Аня\"]))\nprint(main([\"--name\", \"Борис\", \"--times\", \"2\", \"--shout\"]))\nimport contextlib, io\nbuf = io.StringIO()\nwith contextlib.redirect_stderr(buf):\n    try:\n        main([\"--times\", \"x\"])\n    except SystemExit as e:\n        print(\"SystemExit\", e.code)\n", "expected": ["Здравствуйте, Аня!", "0", "ЗДРАВСТВУЙТЕ, БОРИС!", "ЗДРАВСТВУЙТЕ, БОРИС!", "0", "SystemExit 2"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-lock-diff', 7, 'stdout', 'Что изменилось в блокировке', 'Напишите lock_diff(old, new): old и new — словари «пакет → версия». Верните кортеж из трёх отсортированных списков строк: добавленные («+ имя версия»), удалённые («- имя версия») и обновлённые («~ имя старая → новая»).', 'def lock_diff(old, new):
    pass
', 'Сравнивайте множества ключей: new - old, old - new и пересечение с различающимися значениями.', '{"driver": "old = {\"httpx\": \"0.27.0\", \"anyio\": \"4.3.0\", \"idna\": \"3.6\"}\nnew = {\"httpx\": \"0.27.2\", \"anyio\": \"4.3.0\", \"certifi\": \"2024.8\"}\nadded, removed, changed = lock_diff(old, new)\nprint(added)\nprint(removed)\nprint(changed)\nprint(lock_diff({}, {}))\n", "expected": ["[''+ certifi 2024.8'']", "[''- idna 3.6'']", "[''~ httpx 0.27.0 → 0.27.2'']", "([], [], [])"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 50, 'pj-env-settings', 8, 'stdout', 'Настройки из окружения', 'Напишите load_settings(environ): словарь настроек из переменных окружения (environ — обычный словарь): DEBUG («1», «true», «yes» без учёта регистра — True, иначе False), PORT (целое, по умолчанию 8000; не число или вне 1..65535 — ValueError), HOSTS (список из значения через запятую без пробелов по краям, по умолчанию ["localhost"]).', 'def load_settings(environ):
    pass
', 'Пустой HOSTS считайте отсутствующим; PORT проверьте int(...) и диапазон.', '{"driver": "print(load_settings({}))\nprint(load_settings({\"DEBUG\": \"TRUE\", \"PORT\": \"8080\", \"HOSTS\": \"a.com, b.com ,c.com\"}))\nfor bad in ({\"PORT\": \"x\"}, {\"PORT\": \"70000\"}, {\"PORT\": \"0\"}):\n    try:\n        load_settings(bad)\n    except ValueError:\n        print(\"ValueError\")\nprint(load_settings({\"DEBUG\": \"0\", \"HOSTS\": \"\"}))\n", "expected": ["{''debug'': False, ''port'': 8000, ''hosts'': [''localhost'']}", "{''debug'': True, ''port'': 8080, ''hosts'': [''a.com'', ''b.com'', ''c.com'']}", "ValueError", "ValueError", "ValueError", "{''debug'': False, ''port'': 8000, ''hosts'': [''localhost'']}"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-doctest', 0, 'stdout', 'Функция с проверяемыми примерами', 'Напишите fizzbuzz(n): для n, кратного 15, «FizzBuzz»; кратного 3 — «Fizz»; кратного 5 — «Buzz»; иначе число в виде строки. В строке документации приведите не меньше четырёх примеров в формате doctest (>>> …), и все они должны проходить.', 'def fizzbuzz(n):
    pass
', 'В docstring: >>> fizzbuzz(15), следующей строкой — ''FizzBuzz'' (с кавычками, как repr строки).', '{"driver": "import doctest\n\nfinder = doctest.DocTestFinder()\nrunner = doctest.DocTestRunner(verbose=False)\nexamples = 0\nfor test in finder.find(fizzbuzz, \"fizzbuzz\", globs={\"fizzbuzz\": fizzbuzz}):\n    examples += len(test.examples)\n    runner.run(test)\nprint(runner.failures == 0, examples >= 4)\nprint(fizzbuzz(15), fizzbuzz(9), fizzbuzz(10), fizzbuzz(7))\n", "expected": ["True True", "FizzBuzz Fizz Buzz 7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-table-cases', 1, 'stdout', 'Табличные тесты', 'Напишите run_cases(func, cases): cases — список пар (аргументы, ожидаемое) (аргументы — кортеж). Верните список описаний провалов в порядке случаев: «func(аргументы): ожидали X, получили Y»; если функция упала с исключением — «func(аргументы): исключение ИмяТипа». Успешные случаи пропускайте.', 'def run_cases(func, cases):
    pass
', 'for args, want in cases: try: got = func(*args) except Exception as e: ...; if got != want: ...', '{"driver": "def half(x):\n    return x // 2\n\n\ncases = [((4,), 2), ((5,), 2), ((7,), 4), ((\"a\",), 1)]\nfor line in run_cases(half, cases):\n    print(line)\nprint(run_cases(half, [((2,), 1)]))\n", "expected": ["half((7,)): ожидали 4, получили 3", "half((''a'',)): исключение TypeError", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-mock', 2, 'stdout', 'Тест с Mock', 'Функция greet(user_id, fetch) возвращает «Привет, <имя>», где имя получено вызовом fetch(user_id). Напишите check_greet(): создайте Mock (unittest.mock) с return_value="Аня", вызовите greet(7, mock), проверьте результат и что mock вызван ровно один раз с аргументом 7; верните True, если всё верно, и False иначе.', 'from unittest.mock import Mock


def greet(user_id, fetch):
    return f"Привет, {fetch(user_id)}"


def check_greet():
    pass
', 'fetch = Mock(return_value="Аня"); text = greet(7, fetch); fetch.assert_called_once_with(7) внутри try/except AssertionError.', '{"driver": "print(check_greet())\n", "expected": ["True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-logging', 3, 'stdout', 'Настройка журнала', 'Напишите setup_logger(stream): логгер с именем «app», уровнем INFO, одним обработчиком, пишущим в stream в формате «УРОВЕНЬ:сообщение» (%(levelname)s:%(message)s). Повторный вызов не должен добавлять второй обработчик. Распространение записей родительским логгерам отключите.', 'import logging


def setup_logger(stream):
    pass
', 'logger = logging.getLogger("app"); если нет обработчиков — StreamHandler(stream) с Formatter; level INFO; propagate = False.', '{"driver": "import io\n\nbuf = io.StringIO()\nlog = setup_logger(buf)\nlog = setup_logger(buf)\nlog.debug(\"скрыто\")\nlog.info(\"заказ %s создан\", 7)\nlog.warning(\"медленно\")\nprint(buf.getvalue(), end=\"\")\nprint(len(log.handlers), log.name, log.propagate)\n", "expected": ["INFO:заказ 7 создан", "WARNING:медленно", "1 app False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-exceptions', 4, 'stdout', 'Иерархия исключений приложения', 'Создайте исключения: AppError(Exception), NotFound(AppError) и ValidationError(AppError). NotFound принимает имя сущности и ключ и формирует сообщение «<имя> не найден: <ключ>»; ValidationError хранит поле (атрибут field) и сообщение. Напишите find_user(users, user_id): возвращает пользователя из словаря или поднимает NotFound("user", user_id).', 'class AppError(Exception):
    pass
', 'NotFound.__init__(self, entity, key): super().__init__(f"{entity} не найден: {key}"); у ValidationError — сообщение f"{field}: {message}" и self.field.', '{"driver": "users = {1: \"Аня\"}\nprint(find_user(users, 1))\ntry:\n    find_user(users, 2)\nexcept AppError as e:\n    print(type(e).__name__, e)\nerr = ValidationError(\"age\", \"должен быть числом\")\nprint(err.field, err, isinstance(err, AppError), issubclass(NotFound, ValidationError))\n", "expected": ["Аня", "NotFound user не найден: 2", "age age: должен быть числом True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-strategy', 5, 'stdout', 'Скидки как стратегии', 'Напишите make_discount(spec): по строке возвращает функцию цены. «none» — без скидки; «percent:10» — скидка 10% (результат округляйте до копеек, round(…, 2)); «fixed:5» — минус 5, но не ниже нуля. Неизвестная схема — ValueError.', 'def make_discount(spec):
    pass
', 'kind, _, arg = spec.partition(":"); для каждого kind верните свою функцию (замыкание над числом).', '{"driver": "for spec in (\"none\", \"percent:10\", \"fixed:5\"):\n    f = make_discount(spec)\n    print(spec, f(100), f(3))\ntry:\n    make_discount(\"coupon:7\")\nexcept ValueError:\n    print(\"ValueError\")\n", "expected": ["none 100 3", "percent:10 90.0 2.7", "fixed:5 95 0", "ValueError"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-observer', 6, 'stdout', 'Шина событий', 'Напишите EventBus: subscribe(event, handler), unsubscribe(event, handler) и emit(event, *args) — вызывает обработчики события в порядке подписки и возвращает их число. Отписка от неподписанного обработчика не должна падать. Подписка одной и той же функции дважды вызывает её дважды.', 'class EventBus:
    pass
', 'словарь событие → список обработчиков; в unsubscribe удаляйте первое вхождение (list.remove) с try/except ValueError.', '{"driver": "bus = EventBus()\nlog = []\n\n\ndef a(x):\n    log.append((\"a\", x))\n\n\ndef b(x):\n    log.append((\"b\", x))\n\n\nbus.subscribe(\"save\", a)\nbus.subscribe(\"save\", b)\nbus.subscribe(\"save\", a)\nprint(bus.emit(\"save\", 1), log)\nbus.unsubscribe(\"save\", a)\nlog.clear()\nprint(bus.emit(\"save\", 2), log)\nbus.unsubscribe(\"save\", a)\nbus.unsubscribe(\"x\", a)\nprint(bus.emit(\"none\", 0))\n", "expected": ["3 [(''a'', 1), (''b'', 1), (''a'', 1)]", "2 [(''b'', 2), (''a'', 2)]", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-idioms', 7, 'stdout', 'Перепишите по-питоновски', 'Функция pairs_report(names, scores) работает верно, но написана с индексами (range(len(...)), ручная сборка списка). Перепишите её идиоматично — через zip и включение, без range(len(...)) и без метода append. Результат: строки «<имя>: <балл>» для баллов не ниже 50.', 'def pairs_report(names, scores):
    result = []
    for i in range(len(names)):
        if scores[i] >= 50:
            result.append(names[i] + ": " + str(scores[i]))
    return result
', 'return [f"{n}: {s}" for n, s in zip(names, scores) if s >= 50].', '{"driver": "import ast\n\nsrc = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\ntree = ast.parse(src)\nbad_range = any(\n    isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == \"range\"\n    and n.args and isinstance(n.args[0], ast.Call) and getattr(n.args[0].func, \"id\", \"\") == \"len\"\n    for n in ast.walk(tree)\n)\nbad_append = any(isinstance(n, ast.Attribute) and n.attr == \"append\" for n in ast.walk(tree))\nprint(pairs_report([\"Аня\", \"Борис\", \"Вера\"], [90, 40, 50]))\nprint(pairs_report([], []))\nprint(\"range(len)\" if bad_range else \"без range(len)\", \"append\" if bad_append else \"без append\")\n", "expected": ["[''Аня: 90'', ''Вера: 50'']", "[]", "без range(len) без append"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (13, 51, 'qa-property-check', 8, 'stdout', 'Мини-проверка свойств', 'Напишите check_property(prop, gen, trials=200, seed=0): создайте random.Random(seed), trials раз вызовите gen(rng) для получения входа и prop(вход); верните первый вход, на котором prop вернул ложь (или упал с исключением), либо None, если контрпримера не нашлось.', 'import random


def check_property(prop, gen, trials=200, seed=0):
    pass
', 'rng = random.Random(seed); for _ in range(trials): case = gen(rng); try: ok = prop(case) except Exception: return case; if not ok: return case; в конце return None.', '{"driver": "def gen_list(rng):\n    return [rng.randint(-5, 5) for _ in range(rng.randint(0, 6))]\n\n\ndef good_sort(xs):\n    return sorted(xs)\n\n\ndef bad_sort(xs):\n    return sorted(set(xs))\n\n\ndef keeps_items(sort):\n    return lambda xs: sorted(sort(xs)) == sorted(xs)\n\n\nprint(check_property(keeps_items(good_sort), gen_list))\nce = check_property(keeps_items(bad_sort), gen_list)\nprint(ce is not None and len(ce) != len(set(ce)))\nprint(check_property(lambda xs: 1 / len(xs) > 0, gen_list) == [])\nprint(check_property(keeps_items(bad_sort), gen_list, seed=1) is not None)\n", "expected": ["None", "True", "True", "True"]}');
