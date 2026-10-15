"""Задачи «Python как первый язык»: введение (глава 0) — по одной на каждый «кирпичик»."""

TASKS: dict[int, list[dict]] = {
    0: [
        {
            "id": "intro-variable",
            "mode": "stdout",
            "title": "Переменная",
            "statement": (
                "Создайте переменную year со значением 1991 (год, когда появился "
                "Python) и выведите её значение командой print."
            ),
            "starter": "# Имя = значение\n",
            "expected": ["1991"],
            "hint": "year = 1991, затем print(year).",
        },
        {
            "id": "intro-types",
            "mode": "stdout",
            "title": "Типы значений",
            "statement": (
                "Выведите по одной строке названия типов значений 5, 2.5, "
                "\"привет\" и True (в таком порядке): int, float, str, bool. "
                "Получите их функцией type, а не вписывайте слова вручную."
            ),
            "starter": "# type(значение).__name__ даёт имя типа\n",
            "expected": ["int", "float", "str", "bool"],
            "hint": "print(type(5).__name__) — и так для каждого значения.",
        },
        {
            "id": "intro-parity",
            "mode": "func",
            "func": "parity",
            "title": "Условие",
            "statement": (
                "Напишите функцию parity(n), которая возвращает строку «чётное», "
                "если n делится на 2 без остатка, и «нечётное» в остальных случаях."
            ),
            "starter": "def parity(n):\n    pass\n",
            "tests": [
                {"args": [4], "expected": "чётное"},
                {"args": [7], "expected": "нечётное"},
                {"args": [0], "expected": "чётное"},
                {"args": [-3], "expected": "нечётное"},
            ],
            "hint": "if n % 2 == 0: return \"чётное\"; иначе — «нечётное».",
        },
        {
            "id": "intro-loop",
            "mode": "stdout",
            "title": "Цикл",
            "statement": (
                "Выведите числа от 1 до 5, каждое на своей строке, с помощью "
                "цикла for (пять строк print писать нельзя — результат должен "
                "получиться циклом)."
            ),
            "starter": "# for i in range(...):\n",
            "expected": ["1", "2", "3", "4", "5"],
            "hint": "for i in range(1, 6): print(i).",
        },
        {
            "id": "intro-function",
            "mode": "func",
            "func": "circle_area",
            "title": "Функция",
            "statement": (
                "Напишите функцию circle_area(r), которая возвращает площадь "
                "круга радиуса r: 3.14 * r * r."
            ),
            "starter": "def circle_area(r):\n    pass\n",
            "tests": [
                {"args": [1], "expected": 3.14},
                {"args": [2], "expected": 12.56},
                {"args": [0], "expected": 0.0},
            ],
            "hint": "return 3.14 * r * r.",
        },
        {
            "id": "intro-class",
            "mode": "stdout",
            "title": "Класс",
            "statement": (
                "Опишите класс Dog: при создании Dog(\"Рекс\") сохраняется имя, "
                "а метод speak() возвращает строку «Рекс: гав» (имя подставляется). "
                "Ничего не печатайте — проверка вызовет ваш класс сама."
            ),
            "starter": "class Dog:\n    pass\n",
            "driver": 'd = Dog("Рекс")\nprint(d.speak())\nprint(Dog("Шарик").speak())\n',
            "expected": ["Рекс: гав", "Шарик: гав"],
            "hint": "В __init__ сохраните self.name; в speak верните f\"{self.name}: гав\".",
        },
    ],
}
