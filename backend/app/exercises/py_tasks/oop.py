"""Задачи «Изучаем Python»: классы (главы 12–14).

Ученик пишет классы; скрытый "driver" выполняется после его кода в том же
пространстве имён и печатает то, что сравнивается с "expected".
"""

TASKS: dict[int, list[dict]] = {
    12: [
        {
            "id": "counter-class",
            "mode": "stdout",
            "title": "Класс-счётчик",
            "statement": (
                "Опишите класс Counter: у нового счётчика атрибут value равен "
                "0; метод inc() увеличивает value на 1; метод reset() "
                "сбрасывает value в 0. Ничего не печатайте — проверка вызовет "
                "ваш класс сама."
            ),
            "starter": "class Counter:\n    pass\n",
            "driver": (
                "c = Counter()\nc.inc()\nc.inc()\nc.inc()\nprint(c.value)\n"
                "c.reset()\nprint(c.value)\nd = Counter()\nprint(d.value)\n"
            ),
            "expected": ["3", "0", "0"],
            "hint": "В __init__ задайте self.value = 0; в методах меняйте self.value.",
        },
        {
            "id": "rectangle-class",
            "mode": "stdout",
            "title": "Прямоугольник",
            "statement": (
                "Опишите класс Rectangle(w, h) с методами area() — площадь, "
                "perimeter() — периметр и is_square() — True, если стороны "
                "равны."
            ),
            "starter": "class Rectangle:\n    def __init__(self, w, h):\n        pass\n",
            "driver": (
                "r = Rectangle(3, 4)\nprint(r.area())\nprint(r.perimeter())\n"
                "print(r.is_square())\nprint(Rectangle(5, 5).is_square())\n"
            ),
            "expected": ["12", "14", "False", "True"],
            "hint": "Сохраните self.w и self.h; в методах используйте их.",
        },
        {
            "id": "dog-str",
            "mode": "stdout",
            "title": "Собака с описанием",
            "statement": (
                "Опишите класс Dog(name, age) с методом __str__, который "
                "возвращает «Собака Рекс, 5 лет» (имя и возраст подставляются), "
                "и методом birthday(), который увеличивает возраст на 1."
            ),
            "starter": "class Dog:\n    def __init__(self, name, age):\n        pass\n",
            "driver": 'd = Dog("Рекс", 5)\nprint(d)\nd.birthday()\nprint(d)\n',
            "expected": ["Собака Рекс, 5 лет", "Собака Рекс, 6 лет"],
            "hint": 'def __str__(self): return f"Собака {self.name}, {self.age} лет".',
        },
        {
            "id": "bank-account",
            "mode": "stdout",
            "title": "Банковский счёт",
            "statement": (
                "Опишите класс BankAccount(balance=0): атрибут balance; метод "
                "deposit(x) пополняет счёт (x должно быть больше 0, иначе "
                "ValueError); метод withdraw(x) снимает деньги (x больше 0 и не "
                "больше баланса, иначе ValueError)."
            ),
            "starter": "class BankAccount:\n    def __init__(self, balance=0):\n        pass\n",
            "driver": (
                "a = BankAccount(100)\na.deposit(50)\nprint(a.balance)\n"
                "try:\n    a.withdraw(500)\nexcept ValueError:\n    print('недостаточно средств')\n"
                "a.withdraw(30)\nprint(a.balance)\n"
                "try:\n    a.deposit(-1)\nexcept ValueError:\n    print('неверная сумма')\n"
                "print(BankAccount().balance)\n"
            ),
            "expected": ["150", "недостаточно средств", "120", "неверная сумма", "0"],
            "hint": "В начале каждого метода проверьте условие и сделайте raise ValueError(...), потом меняйте баланс.",
        },
        {
            "id": "stack-class",
            "mode": "stdout",
            "title": "Свой стек",
            "statement": (
                "Опишите класс Stack с методами push(x), pop() (снимает и "
                "возвращает верхний элемент), peek() (возвращает верхний, не "
                "снимая), is_empty() и size(). Хранить элементы нужно в "
                "списке внутри объекта."
            ),
            "starter": "class Stack:\n    def __init__(self):\n        pass\n",
            "driver": (
                "s = Stack()\nprint(s.is_empty())\ns.push(1)\ns.push(2)\ns.push(3)\n"
                "print(s.size())\nprint(s.peek())\nprint(s.pop())\nprint(s.pop())\n"
                "print(s.size())\nprint(s.is_empty())\n"
            ),
            "expected": ["True", "3", "3", "3", "2", "1", "False"],
            "hint": "self._items = [] в __init__; peek — это self._items[-1].",
        },
        {
            "id": "best-student",
            "mode": "stdout",
            "title": "Лучший ученик",
            "statement": (
                "Опишите класс Student(name, grade) и функцию "
                "best_student(students): она получает список объектов Student "
                "и возвращает ИМЯ ученика с наибольшей оценкой (при равных — "
                "того, кто раньше в списке)."
            ),
            "starter": "class Student:\n    def __init__(self, name, grade):\n        pass\n\n\ndef best_student(students):\n    pass\n",
            "driver": (
                'a = [Student("Аня", 4), Student("Боря", 5), Student("Вера", 5)]\n'
                "print(best_student(a))\nprint(best_student([Student('Гоша', 3)]))\n"
            ),
            "expected": ["Боря", "Гоша"],
            "hint": "Идите по списку и обновляйте лучшего только при строго большей оценке.",
        },
        {
            "id": "team-members",
            "mode": "stdout",
            "title": "Команда без общего списка",
            "statement": (
                "Опишите класс Team: метод add(name) добавляет участника, "
                "метод size() возвращает их число. У каждой команды свой "
                "список — не делайте его атрибутом класса."
            ),
            "starter": "class Team:\n    pass\n",
            "driver": (
                'a = Team()\nb = Team()\na.add("х")\na.add("у")\nprint(a.size(), b.size())\n'
            ),
            "expected": ["2 0"],
            "hint": "self.members = [] — внутри __init__, чтобы список был у каждого экземпляра свой.",
        },
    ],
    13: [
        {
            "id": "vector-class",
            "mode": "stdout",
            "title": "Вектор",
            "statement": (
                "Опишите класс Vector(x, y) с операторами: + (сложение), - "
                "(вычитание), * на число (масштабирование), == (равенство по "
                "значению) и методом __repr__, который возвращает "
                "«Vector(1, 2)». Операторы возвращают НОВЫЕ векторы."
            ),
            "starter": "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n",
            "driver": (
                "a = Vector(1, 2)\nb = Vector(3, 5)\nprint(a + b)\nprint(b - a)\nprint(a * 3)\n"
                "print(a == Vector(1, 2), a == b)\nprint(a)\n"
            ),
            "expected": ["Vector(4, 7)", "Vector(2, 3)", "Vector(3, 6)", "True False", "Vector(1, 2)"],
            "hint": "__add__, __sub__, __mul__, __eq__, __repr__ — каждый возвращает результат, а не меняет self.",
        },
        {
            "id": "money-class",
            "mode": "stdout",
            "title": "Деньги",
            "statement": (
                "Опишите класс Money(amount): объекты равны, если равны суммы "
                "(__eq__); их можно сортировать (__lt__); их можно "
                "использовать как ключи словаря (__hash__)."
            ),
            "starter": "class Money:\n    def __init__(self, amount):\n        self.amount = amount\n",
            "driver": (
                "ms = [Money(5), Money(1), Money(3)]\nprint([m.amount for m in sorted(ms)])\n"
                "print(Money(2) == Money(2))\nd = {Money(2): 'два'}\nprint(Money(2) in d)\n"
                "print(max(ms).amount)\n"
            ),
            "expected": ["[1, 3, 5]", "True", "True", "5"],
            "hint": "__hash__: return hash(self.amount); __lt__: сравните суммы.",
        },
        {
            "id": "playlist-class",
            "mode": "stdout",
            "title": "Плейлист",
            "statement": (
                "Опишите класс Playlist(songs): len(p) возвращает число песен, "
                "p[i] — песню по номеру, «название in p» проверяет наличие. "
                "Пустой плейлист в условии должен считаться ложью."
            ),
            "starter": "class Playlist:\n    def __init__(self, songs):\n        self._songs = list(songs)\n",
            "driver": (
                'p = Playlist(["а", "б", "в"])\nprint(len(p))\nprint(p[1])\nprint("в" in p, "я" in p)\n'
                "print(bool(p), bool(Playlist([])))\n"
            ),
            "expected": ["3", "б", "True False", "True False"],
            "hint": "__len__, __getitem__ и __contains__; bool() сам опирается на __len__.",
        },
        {
            "id": "temperature-class",
            "mode": "stdout",
            "title": "Температура",
            "statement": (
                "Опишите класс Temperature(celsius): свойство celsius с "
                "проверкой (ниже -273.15 — ValueError, в том числе при "
                "создании объекта) и вычисляемое свойство fahrenheit только "
                "для чтения: celsius * 9 / 5 + 32."
            ),
            "starter": "class Temperature:\n    def __init__(self, celsius):\n        pass\n",
            "driver": (
                "t = Temperature(100)\nprint(t.fahrenheit)\nt.celsius = 0\nprint(t.fahrenheit)\n"
                "try:\n    t.celsius = -300\nexcept ValueError:\n    print('слишком холодно')\n"
                "print(t.celsius)\n"
                "try:\n    Temperature(-500)\nexcept ValueError:\n    print('нельзя создать')\n"
            ),
            "expected": ["212.0", "32.0", "слишком холодно", "0", "нельзя создать"],
            "hint": "В __init__ присваивайте self.celsius = celsius — так сработает сеттер; хранить в self._celsius.",
        },
        {
            "id": "person-from-string",
            "mode": "stdout",
            "title": "Человек из строки",
            "statement": (
                "Опишите класс Person(name, age) и метод класса "
                "from_string(s), который разбирает строку «Аня,20» и "
                "возвращает Person (возраст — число). Метод __str__ "
                "возвращает «Аня (20)»."
            ),
            "starter": "class Person:\n    def __init__(self, name, age):\n        pass\n",
            "driver": 'p = Person.from_string("Аня,20")\nprint(p)\nprint(p.age + 1)\n',
            "expected": ["Аня (20)", "21"],
            "hint": "@classmethod def from_string(cls, s): name, age = s.split(','); return cls(name, int(age)).",
        },
        {
            "id": "circle-property",
            "mode": "stdout",
            "title": "Круг",
            "statement": (
                "Опишите класс Circle(radius): свойство radius (больше 0, "
                "иначе ValueError) и свойство только для чтения area — "
                "3.14159 * radius ** 2."
            ),
            "starter": "class Circle:\n    def __init__(self, radius):\n        pass\n",
            "driver": (
                "c = Circle(2)\nprint(round(c.area, 2))\nc.radius = 1\nprint(round(c.area, 2))\n"
                "try:\n    c.radius = -5\nexcept ValueError:\n    print('радиус должен быть положительным')\n"
                "try:\n    c.area = 1\nexcept AttributeError:\n    print('area только для чтения')\n"
            ),
            "expected": ["12.57", "3.14", "радиус должен быть положительным", "area только для чтения"],
            "hint": "Свойство без сеттера нельзя присвоить — Питон сам поднимет AttributeError.",
        },
        {
            "id": "version-class",
            "mode": "stdout",
            "title": "Версии",
            "statement": (
                "Опишите класс Version(text): text — строка вида «1.2.10». "
                "Версии сравниваются по числам, а не по тексту: 1.2.10 больше "
                "1.2.9. Нужны __lt__, __eq__ и __str__ (возвращает исходную "
                "строку)."
            ),
            "starter": "class Version:\n    def __init__(self, text):\n        self.text = text\n",
            "driver": (
                'vs = [Version("1.10.0"), Version("1.2.10"), Version("1.2.9")]\n'
                "print([str(v) for v in sorted(vs)])\nprint(Version('2.0') == Version('2.0'))\n"
                "print(Version('1.10') > Version('1.9'))\n"
            ),
            "expected": ["['1.2.9', '1.2.10', '1.10.0']", "True", "True"],
            "hint": "Сравнивайте кортежи чисел: tuple(int(p) for p in self.text.split('.')); для > Питон сам обратит __lt__.",
        },
    ],
    14: [
        {
            "id": "animals-polymorphism",
            "mode": "stdout",
            "title": "Животные",
            "statement": (
                "Опишите Animal(name) с методом speak() (возвращает «...») и "
                "describe() (возвращает «<имя>: <звук>» — звук берётся из "
                "speak). Наследники Dog и Cat переопределяют speak: «Гав!» и "
                "«Мяу!». describe() переопределять не нужно."
            ),
            "starter": "class Animal:\n    def __init__(self, name):\n        pass\n\n\nclass Dog(Animal):\n    pass\n\n\nclass Cat(Animal):\n    pass\n",
            "driver": (
                'for a in [Dog("Шарик"), Cat("Мурка"), Animal("Нечто")]:\n    print(a.describe())\n'
            ),
            "expected": ["Шарик: Гав!", "Мурка: Мяу!", "Нечто: ..."],
            "hint": "В Animal: describe возвращает f'{self.name}: {self.speak()}' — self.speak() вызовет версию потомка.",
        },
        {
            "id": "employee-manager",
            "mode": "stdout",
            "title": "Сотрудник и менеджер",
            "statement": (
                "Опишите Employee(name, salary) с методом pay() (зарплата) и "
                "наследника Manager(name, salary, bonus), у которого pay() "
                "возвращает зарплату плюс бонус. Используйте super() и в "
                "конструкторе, и в pay()."
            ),
            "starter": "class Employee:\n    def __init__(self, name, salary):\n        pass\n\n\nclass Manager(Employee):\n    pass\n",
            "driver": (
                'e = Employee("Аня", 100)\nm = Manager("Боря", 200, 50)\nprint(e.pay())\nprint(m.pay())\n'
                "print(m.name, m.bonus)\nprint(isinstance(m, Employee))\n"
            ),
            "expected": ["100", "250", "Боря 50", "True"],
            "hint": "В Manager: super().__init__(name, salary); self.bonus = bonus; pay: return super().pay() + self.bonus.",
        },
        {
            "id": "shapes-abstract",
            "mode": "stdout",
            "title": "Абстрактная фигура",
            "statement": (
                "Опишите абстрактный класс Shape (модуль abc) с абстрактным "
                "методом area(); Circle(r) с площадью 3.14159 * r ** 2 и "
                "Rect(w, h); а также функцию total_area(shapes) — сумму "
                "площадей. Создать Shape напрямую нельзя."
            ),
            "starter": "from abc import ABC, abstractmethod\n\n\nclass Shape(ABC):\n    pass\n\n\ndef total_area(shapes):\n    pass\n",
            "driver": (
                "shapes = [Circle(1), Rect(2, 3)]\nprint(round(total_area(shapes), 2))\n"
                "try:\n    Shape()\nexcept TypeError:\n    print('нельзя создать')\n"
                "print(isinstance(Rect(1, 1), Shape))\n"
            ),
            "expected": ["9.14", "нельзя создать", "True"],
            "hint": "@abstractmethod над def area(self); Circle и Rect наследуют от Shape и реализуют area.",
        },
        {
            "id": "car-composition",
            "mode": "stdout",
            "title": "Автомобиль и двигатель",
            "statement": (
                "Опишите Engine(power) с методом start() — возвращает «двигатель "
                "<мощность> л.с. запущен» — и Car(engine), у которого метод go() "
                "возвращает результат engine.start(), к которому добавлено "
                "«, поехали». Car хранит двигатель как атрибут (композиция)."
            ),
            "starter": "class Engine:\n    def __init__(self, power):\n        pass\n\n\nclass Car:\n    def __init__(self, engine):\n        pass\n",
            "driver": (
                "car = Car(Engine(150))\nprint(car.go())\ncar.engine = Engine(300)\nprint(car.go())\n"
            ),
            "expected": ["двигатель 150 л.с. запущен, поехали", "двигатель 300 л.с. запущен, поехали"],
            "hint": 'Car.go: return self.engine.start() + ", поехали".',
        },
        {
            "id": "greet-mixin",
            "mode": "stdout",
            "title": "Примесь «поздороваться»",
            "statement": (
                "Опишите примесь GreetMixin с методом greet(), который "
                "возвращает «Привет, я <имя>» (имя берётся из self.name), и "
                "классы Person(name) и Robot(name), которые её подмешивают."
            ),
            "starter": "class GreetMixin:\n    pass\n\n\nclass Person(GreetMixin):\n    def __init__(self, name):\n        pass\n\n\nclass Robot(GreetMixin):\n    def __init__(self, name):\n        pass\n",
            "driver": 'print(Person("Аня").greet())\nprint(Robot("R2").greet())\n',
            "expected": ["Привет, я Аня", "Привет, я R2"],
            "hint": "greet — в GreetMixin; Person и Robot лишь задают self.name.",
        },
        {
            "id": "count-dogs",
            "mode": "stdout",
            "title": "Сколько собак",
            "statement": (
                "Даны классы Animal, Dog(Animal), Puppy(Dog) и Cat(Animal) "
                "(уже описаны в проверке). Напишите функцию count_dogs(animals): "
                "сколько объектов в списке являются собаками — включая щенков. "
                "Используйте isinstance."
            ),
            "starter": "def count_dogs(animals):\n    pass\n",
            "driver": (
                "class Animal: pass\nclass Dog(Animal): pass\nclass Puppy(Dog): pass\nclass Cat(Animal): pass\n"
                "zoo = [Dog(), Puppy(), Cat(), Animal(), Dog()]\nprint(count_dogs(zoo))\nprint(count_dogs([]))\n"
            ),
            "expected": ["3", "0"],
            "hint": "type(x) is Dog не посчитает щенков; isinstance(x, Dog) — посчитает.",
        },
        {
            "id": "base-repr",
            "mode": "stdout",
            "title": "Универсальный repr",
            "statement": (
                "Опишите класс Base(x) с методом __repr__, который возвращает "
                "«<ИмяКласса>(<x>)» и работает для любых наследников без "
                "переопределения: Base(1) -> «Base(1)», а у наследника "
                "Child(2) -> «Child(2)»."
            ),
            "starter": "class Base:\n    def __init__(self, x):\n        pass\n",
            "driver": "class Child(Base):\n    pass\n\nprint(Base(1))\nprint(Child(2))\nprint([Child(3), Base(4)])\n",
            "expected": ["Base(1)", "Child(2)", "[Child(3), Base(4)]"],
            "hint": 'return f"{type(self).__name__}({self.x})".',
        },
    ],
}
