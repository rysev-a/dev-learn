"""Задачи книги «Современный Frontend», глава 8 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {8: [{'id': 'j8-point',
      'mode': 'js',
      'title': 'Класс Point',
      'statement': 'Напишите класс Point с конструктором (x, y), методом distanceTo(other) (евклидово '
                   'расстояние до другой точки) и методом toString(), возвращающим «(x, y)».',
      'starter': 'class Point {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const a = new Point(0, 0);\n'
                'const b = new Point(3, 4);\n'
                'console.log(a.distanceTo(b));\n'
                'console.log(String(b));\n'
                'console.log(`${a}`);\n'
                'console.log(b instanceof Point, typeof Point);\n',
      'hint': 'Math.hypot(dx, dy); toString возвращает шаблонную строку.',
      'expected': ['5', '(3, 4)', '(0, 0)', 'true function']},
     {'id': 'j8-counter-static',
      'mode': 'js',
      'title': 'Счётчик экземпляров (static)',
      'statement': 'Напишите класс Widget: каждый новый экземпляр получает поле id (1, 2, 3, …); статическое '
                   'поле count хранит общее число созданных экземпляров, статический метод reset() обнуляет '
                   'счёт (следующий id снова 1).',
      'starter': 'class Widget {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const a = new Widget();\n'
                'const b = new Widget();\n'
                'console.log(a.id, b.id, Widget.count);\n'
                'Widget.reset();\n'
                'console.log(Widget.count);\n'
                'console.log(new Widget().id);\n'
                'console.log(a.count, Object.hasOwn(a, "count"));\n',
      'hint': 'static count = 0; this.id = ++Widget.count;',
      'expected': ['1 2 2', '0', '1', 'undefined false']},
     {'id': 'j8-account',
      'mode': 'js',
      'title': 'Счёт с приватным полем',
      'statement': 'Напишите класс Account с приватным полем #balance (начальное значение — параметр '
                   'конструктора, по умолчанию 0), методами deposit(x) и withdraw(x) (RangeError, если '
                   'средств не хватает) и геттером balance.',
      'starter': 'class Account {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'const a = new Account(100);\n'
                'a.deposit(50);\n'
                'a.withdraw(30);\n'
                'console.log(a.balance);\n'
                'try { a.withdraw(1000); } catch (e) { console.log(e.name, a.balance); }\n'
                'try { a.balance = 5; } catch (e) { console.log(e.name); }\n'
                'console.log(a.balance);\n'
                'console.log(JSON.stringify(Object.keys(a)));\n'
                'console.log(new Account().balance);\n'
                'console.log(__count("#" + "balance") >= 3);\n',
      'hint': 'Приватное поле #balance; get balance() без сеттера — запись молча игнорируется.',
      'expected': ['120', 'RangeError 120', 'TypeError', '120', '[]', '0', 'true']},
     {'id': 'j8-temperature',
      'mode': 'js',
      'title': 'Геттеры и сеттеры температуры',
      'statement': 'Напишите класс Temperature: хранит градусы Цельсия; геттер/сеттер celsius (сеттер '
                   'бросает RangeError, если значение ниже -273.15), геттер fahrenheit (c * 9 / 5 + 32) и '
                   'статический метод fromFahrenheit(f), возвращающий экземпляр.',
      'starter': 'class Temperature {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = new Temperature(100);\n'
                'console.log(t.celsius, t.fahrenheit);\n'
                't.celsius = 0;\n'
                'console.log(t.fahrenheit);\n'
                'try { t.celsius = -300; } catch (e) { console.log(e.name, t.celsius); }\n'
                'console.log(Temperature.fromFahrenheit(212).celsius);\n'
                'console.log(Temperature.fromFahrenheit(32) instanceof Temperature);\n'
                'try { new Temperature(-500); } catch (e) { console.log(e.name); }\n',
      'hint': 'Конструктор может присваивать this.celsius = c — тогда проверка сеттера сработает и при '
              'создании.',
      'expected': ['100 212', '32', 'RangeError 0', '100', 'true', 'RangeError']},
     {'id': 'j8-stack-class',
      'mode': 'js',
      'title': 'Класс Stack',
      'statement': 'Напишите класс Stack: приватный массив элементов, методы push(x), pop() (undefined для '
                   'пустого), peek() и геттер size. Метод push возвращает this, чтобы вызовы можно было '
                   'цеплять.',
      'starter': 'class Stack {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const s = new Stack().push(1).push(2).push(3);\n'
                'console.log(s.size, s.peek(), s.pop(), s.pop(), s.size);\n'
                'console.log(s.pop(), s.pop(), s.peek(), s.size);\n'
                'console.log(Object.keys(s).length);\n',
      'hint': 'Каждый метод, который «меняет и возвращает себя», завершается return this.',
      'expected': ['3 3 3 2 1', '1 undefined undefined 0', '0']},
     {'id': 'j8-queue-class',
      'mode': 'js',
      'title': 'Очередь на кольцевом буфере',
      'statement': 'Напишите класс Queue(capacity): очередь фиксированной ёмкости на массиве; методы '
                   'enqueue(x) (false, если очередь полна; иначе true), dequeue() (undefined для пустой), '
                   'геттеры size и isFull. Элементы не сдвигаются: храните индексы головы и хвоста.',
      'starter': 'class Queue {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'const q = new Queue(3);\n'
                'console.log(q.enqueue(1), q.enqueue(2), q.enqueue(3), q.enqueue(4));\n'
                'console.log(q.size, q.isFull);\n'
                'console.log(q.dequeue(), q.dequeue());\n'
                'console.log(q.enqueue(5), q.enqueue(6), q.enqueue(7));\n'
                'console.log(q.dequeue(), q.dequeue(), q.dequeue(), q.dequeue());\n'
                'console.log(q.size, q.isFull);\n'
                'console.log(__count(".sh" + "ift(") + __count(".uns" + "hift("));\n',
      'hint': 'Индекс записи — (head + size) % capacity; чтение сдвигает head по модулю.',
      'expected': ['true true true false',
                   '3 true',
                   '1 2',
                   'true true false',
                   '3 5 6 undefined',
                   '0 false',
                   '0']},
     {'id': 'j8-dog',
      'mode': 'js',
      'title': 'Наследование и super',
      'statement': 'Напишите класс Animal(name) с методом speak() → «<name> издаёт звук» и класс Dog extends '
                   'Animal с переопределением speak(): «<родительская строка>: гав!» (вызовите родительскую '
                   'версию через super).',
      'starter': 'class Animal {\n}\n\nclass Dog extends Animal {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const a = new Animal("Зверь");\n'
                'const d = new Dog("Бобик");\n'
                'console.log(a.speak());\n'
                'console.log(d.speak());\n'
                'console.log(d instanceof Dog, d instanceof Animal, a instanceof Dog);\n'
                'console.log(Object.getPrototypeOf(Dog.prototype) === Animal.prototype);\n',
      'hint': 'В Dog конструктор не нужен: он унаследуется. Вызов родителя: super.speak().',
      'expected': ['Зверь издаёт звук', 'Бобик издаёт звук: гав!', 'true true false', 'true']},
     {'id': 'j8-shapes',
      'mode': 'js',
      'title': 'Фигуры: полиморфизм',
      'statement': 'Напишите базовый класс Shape с методом area(), бросающим Error("не реализовано"), а '
                   'также классы Rect(w, h) и Circle(r), переопределяющие area(). Затем функцию '
                   'totalArea(shapes) — сумма площадей (для Circle — Math.PI * r ** 2).',
      'starter': 'class Shape {\n}\n\nfunction totalArea(shapes) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(totalArea([new Rect(2, 3), new Rect(1, 1)]));\n'
                'console.log(totalArea([new Circle(1)]).toFixed(4));\n'
                'console.log(totalArea([]));\n'
                'try { new Shape().area(); } catch (e) { console.log(e.message); }\n'
                'console.log(new Rect(2, 2) instanceof Shape, new Circle(1) instanceof Shape);\n',
      'hint': 'Каждый наследник вызывает super() в конструкторе перед использованием this.',
      'expected': ['7', '3.1416', '0', 'не реализовано', 'true true']},
     {'id': 'j8-validation-error',
      'mode': 'js',
      'title': 'Своя ошибка ValidationError',
      'statement': 'Напишите класс ValidationError extends Error: конструктор (field, message) задаёт '
                   'this.name = "ValidationError", this.field и сообщение. И функцию validateUser(u): '
                   'бросает ValidationError для пустого name (field "name") и для age вне диапазона 0–150 '
                   '(field "age"); иначе возвращает true.',
      'starter': 'class ValidationError extends Error {\n}\n\nfunction validateUser(u) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(validateUser({ name: "Ада", age: 36 }));\n'
                'for (const u of [{ name: "", age: 5 }, { name: "Б", age: -1 }, { name: "В", age: 200 }, { '
                'name: "Г" }, { name: " ", age: 1 }]) {\n'
                '  try { validateUser(u); } catch (e) {\n'
                '    console.log(e.name, e.field, e.message, e instanceof ValidationError, e instanceof '
                'Error);\n'
                '  }\n'
                '}\n'
                'const e = new ValidationError("x", "msg");\n'
                'console.log(typeof e.stack, String(e));\n',
      'hint': 'super(message); затем name и field. Условие для age пишите так, чтобы NaN и undefined не '
              'проходили.',
      'expected': ['true',
                   'ValidationError name Имя обязательно true true',
                   'ValidationError age Недопустимый возраст true true',
                   'ValidationError age Недопустимый возраст true true',
                   'ValidationError age Недопустимый возраст true true',
                   'ValidationError name Имя обязательно true true',
                   'string ValidationError: msg']},
     {'id': 'j8-http-error',
      'mode': 'js',
      'title': 'Иерархия ошибок HTTP',
      'statement': 'Напишите класс HttpError extends Error (status, message; name = «HttpError») и его '
                   'наследника NotFoundError (message по умолчанию «Не найдено», status = 404, name = '
                   '«NotFoundError»). Функция describe(err) возвращает «<name> <status>: <message>» для '
                   'HttpError и «Ошибка: <message>» для остальных.',
      'starter': 'class HttpError extends Error {\n'
                 '}\n'
                 '\n'
                 'class NotFoundError extends HttpError {\n'
                 '}\n'
                 '\n'
                 'function describe(err) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(describe(new HttpError(500, "Сбой")));\n'
                'console.log(describe(new NotFoundError()));\n'
                'console.log(describe(new NotFoundError("Нет пользователя")));\n'
                'console.log(describe(new TypeError("плохо")));\n'
                'const e = new NotFoundError();\n'
                'console.log(e instanceof NotFoundError, e instanceof HttpError, e instanceof Error);\n',
      'hint': 'Наследник вызывает super(404, message) и затем меняет this.name.',
      'expected': ['HttpError 500: Сбой',
                   'NotFoundError 404: Не найдено',
                   'NotFoundError 404: Нет пользователя',
                   'Ошибка: плохо',
                   'true true true']},
     {'id': 'j8-fix-this-class',
      'mode': 'js',
      'title': 'Исправьте: метод теряет this',
      'statement': 'Класс Clicker считает клики: метод click() увеличивает this.count. Но когда его передают '
                   'как колбэк (handler = obj.click; handler()), он падает. Исправьте класс так, чтобы click '
                   'работал и отдельно от объекта (подойдёт bind в конструкторе или поле-стрелка).',
      'starter': 'class Clicker {\n'
                 '  count = 0;\n'
                 '  click() {\n'
                 '    this.count++;\n'
                 '    return this.count;\n'
                 '  }\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const c = new Clicker();\n'
                'const handler = c.click;\n'
                'console.log(handler());\n'
                'console.log(handler());\n'
                'console.log(c.count);\n'
                'const list = [1, 2, 3].map(c.click);\n'
                'console.log(JSON.stringify(list), c.count);\n',
      'hint': 'click = () => { … } — стрелка запоминает this экземпляра.',
      'expected': ['1', '2', '2', '[3,4,5] 5']},
     {'id': 'j8-fix-super',
      'mode': 'js',
      'title': 'Исправьте: забытый super()',
      'statement': 'Класс Admin наследует User, но его конструктор падает с ReferenceError: Must call super '
                   'constructor. Исправьте конструктор так, чтобы Admin получал name от родителя и добавлял '
                   'своё поле level.',
      'starter': 'class User {\n'
                 '  constructor(name) {\n'
                 '    this.name = name;\n'
                 '  }\n'
                 '}\n'
                 '\n'
                 'class Admin extends User {\n'
                 '  constructor(name, level) {\n'
                 '    this.level = level;\n'
                 '  }\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const a = new Admin("Ада", 3);\n'
                'console.log(a.name, a.level);\n'
                'console.log(a instanceof User);\n'
                'console.log(JSON.stringify(a));\n',
      'hint': 'super(name) до первого обращения к this.',
      'expected': ['Ада 3', 'true', '{"name":"Ада","level":3}']},
     {'id': 'j8-proto-depth',
      'mode': 'js',
      'title': 'Глубина цепочки прототипов',
      'statement': 'Напишите функцию protoDepth(obj): возвращает число прототипов в цепочке объекта до null. '
                   'Например, для {} это 1 (Object.prototype), а для [] — 2.',
      'starter': 'function protoDepth(obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'class A {}\n'
                'class B extends A {}\n'
                'console.log(protoDepth({}), protoDepth([]), protoDepth(Object.create(null)));\n'
                'console.log(protoDepth(new A()), protoDepth(new B()));\n'
                'console.log(protoDepth(() => 1), protoDepth(new Error("x")));\n'
                'console.log(protoDepth(Object.create({})));\n',
      'hint': 'Object.getPrototypeOf(p) в цикле, пока не получите null.',
      'expected': ['1 2 0', '2 3', '2 2', '2']},
     {'id': 'j8-create-child',
      'mode': 'js',
      'title': 'Object.create: наследование объектов',
      'statement': 'Напишите функцию extend(parent, props): создаёт новый объект с прототипом parent и '
                   'копирует в него собственные поля props. Исходные объекты не меняются.',
      'starter': 'function extend(parent, props) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const base = { kind: "base", hello() { return "Привет, " + this.name; } };\n'
                'const child = extend(base, { name: "Ада" });\n'
                'console.log(child.hello());\n'
                'console.log(child.kind, Object.hasOwn(child, "kind"), Object.hasOwn(child, "name"));\n'
                'console.log(Object.getPrototypeOf(child) === base);\n'
                'child.kind = "own";\n'
                'console.log(base.kind, child.kind);\n'
                'console.log(JSON.stringify(Object.keys(child)));\n',
      'hint': 'Object.assign(Object.create(parent), props)',
      'expected': ['Привет, Ада', 'base false true', 'true', 'base own', '["name","kind"]']},
     {'id': 'j8-my-new',
      'mode': 'js',
      'title': 'Реализуйте new вручную',
      'statement': 'Напишите функцию myNew(Ctor, ...args): повторяет работу оператора new для '
                   'функции-конструктора: создаёт объект с прототипом Ctor.prototype, вызывает Ctor с этим '
                   'объектом как this и аргументами; если конструктор вернул объект — вернуть его, иначе '
                   'созданный. Оператор new использовать нельзя.',
      'starter': 'function myNew(Ctor, ...args) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'function Person(name) { this.name = name; }\n'
                'Person.prototype.hi = function () { return "Привет, " + this.name; };\n'
                'const p = myNew(Person, "Ада");\n'
                'console.log(p.hi(), p instanceof Person);\n'
                'function Weird() { this.a = 1; return { b: 2 }; }\n'
                'console.log(JSON.stringify(myNew(Weird)));\n'
                'function Prim() { this.z = 5; return 42; }\n'
                'console.log(JSON.stringify(myNew(Prim)));\n'
                'console.log(__count("ne" + "w "));\n',
      'hint': 'Object.create(Ctor.prototype), затем Ctor.apply(obj, args) и проверка типа результата.',
      'expected': ['Привет, Ада true', '{"b":2}', '{"z":5}', '0']},
     {'id': 'j8-emitter',
      'mode': 'js',
      'title': 'Эмиттер событий',
      'statement': 'Напишите класс Emitter с методами on(name, fn) (подписка), off(name, fn) (отписка) и '
                   'emit(name, ...args) (вызывает подписчиков в порядке подписки, возвращает число '
                   'вызванных). on возвращает функцию отписки.',
      'starter': 'class Emitter {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const e = new Emitter();\n'
                'const log = [];\n'
                'const off = e.on("msg", (x) => log.push("a" + x));\n'
                'e.on("msg", (x) => log.push("b" + x));\n'
                'console.log(e.emit("msg", 1));\n'
                'off();\n'
                'console.log(e.emit("msg", 2));\n'
                'console.log(e.emit("none"));\n'
                'console.log(log.join(","));\n'
                'const f = () => log.push("f");\n'
                'e.on("x", f);\n'
                'e.off("x", f);\n'
                'console.log(e.emit("x"));\n',
      'hint': 'Map: имя → массив функций. Копируйте массив перед обходом — подписчик может отписаться во '
              'время emit.',
      'expected': ['2', '1', '0', 'a1,b1,b2', '0']},
     {'id': 'j8-compose-robot',
      'mode': 'js',
      'title': 'Композиция вместо наследования',
      'statement': 'Напишите функции-способности walker(state) и talker(state), каждая возвращает объект с '
                   'одним методом: walker → walk() даёт «<name> идёт», talker → talk() даёт «<name>: '
                   'привет». И функцию makeRobot(name, ...abilities), собирающую объект: { name } плюс '
                   'методы переданных способностей (абилити получает state = { name }).',
      'starter': 'function walker(state) {\n'
                 '}\n'
                 'function talker(state) {\n'
                 '}\n'
                 'function makeRobot(name, ...abilities) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const r1 = makeRobot("Р1", walker, talker);\n'
                'console.log(r1.walk(), r1.talk());\n'
                'const r2 = makeRobot("Р2", talker);\n'
                'console.log(r2.talk(), typeof r2.walk);\n'
                'const r3 = makeRobot("Р3");\n'
                'console.log(JSON.stringify(Object.keys(r3)));\n'
                'console.log(JSON.stringify(Object.keys(r1).sort()));\n',
      'hint': 'Object.assign({ name }, ...abilities.map((a) => a(state)))',
      'expected': ['Р1 идёт Р1: привет', 'Р2: привет undefined', '["name"]', '["name","talk","walk"]']},
     {'id': 'j8-readonly',
      'mode': 'js',
      'title': 'Неизменяемое поле через defineProperty',
      'statement': 'Напишите функцию defineConst(obj, key, value): определяет в объекте свойство key со '
                   'значением value так, чтобы его нельзя было ни перезаписать, ни удалить, и оно не '
                   'попадало в Object.keys. Возвращает obj. Работайте в строгом режиме драйвера: попытка '
                   'записи должна бросать TypeError.',
      'starter': 'function defineConst(obj, key, value) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '"use strict";\n'
                'const o = defineConst({ a: 1 }, "id", 7);\n'
                'console.log(o.id, JSON.stringify(Object.keys(o)));\n'
                'try { o.id = 9; } catch (e) { console.log(e.name); }\n'
                'try { delete o.id; } catch (e) { console.log(e.name); }\n'
                'console.log(o.id);\n'
                'console.log(JSON.stringify(Object.getOwnPropertyDescriptor(o, "id")));\n',
      'hint': 'Object.defineProperty(obj, key, { value, writable: false, enumerable: false, configurable: '
              'false })',
      'expected': ['7 ["a"]',
                   'TypeError',
                   'TypeError',
                   '7',
                   '{"value":7,"writable":false,"enumerable":false,"configurable":false}']},
     {'id': 'j8-deep-freeze',
      'mode': 'js',
      'title': 'Глубокая заморозка',
      'statement': 'Напишите функцию deepFreeze(obj): замораживает объект и все вложенные объекты и массивы '
                   '(рекурсивно) и возвращает его. После этого записи в любой уровень должны быть невозможны '
                   '(в строгом режиме — TypeError).',
      'starter': 'function deepFreeze(obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '"use strict";\n'
                'const o = deepFreeze({ a: 1, in: { b: [1, 2, { c: 3 }] } });\n'
                'for (const f of [() => { o.a = 2; }, () => { o.in.b.push(3); }, () => { o.in.b[2].c = 9; }, '
                '() => { o.x = 1; }]) {\n'
                '  try { f(); console.log("записано"); } catch (e) { console.log(e.name); }\n'
                '}\n'
                'console.log(JSON.stringify(o));\n'
                'console.log(Object.isFrozen(o.in.b[2]));\n',
      'hint': 'Сначала заморозьте вложенное, потом сам объект; для примитивов ничего не делайте.',
      'expected': ['TypeError',
                   'TypeError',
                   'TypeError',
                   'TypeError',
                   '{"a":1,"in":{"b":[1,2,{"c":3}]}}',
                   'true']},
     {'id': 'j8-money-toprimitive',
      'mode': 'js',
      'title': 'Money с Symbol.toPrimitive',
      'statement': 'Напишите класс Money(cents) с методом [Symbol.toPrimitive](hint): для hint "number" '
                   'возвращает копейки, для "string" — строку вида «12.34 ₽», для "default" — копейки. Так '
                   'Money работает в арифметике и в шаблонах.',
      'starter': 'class Money {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const m = new Money(1234);\n'
                'console.log(m * 2);\n'
                'console.log(`${m}`);\n'
                'console.log(m + 1);\n'
                'console.log(String(new Money(5)));\n'
                'console.log(new Money(100) > new Money(99));\n'
                'console.log(+new Money(7));\n',
      'hint': 'В шаблонной строке и String() hint равен "string"; в сложении и сравнении — '
              '"default"/"number".',
      'expected': ['2468', '12.34 ₽', '1235', '0.05 ₽', 'true', '7']},
     {'id': 'j8-range-iterable',
      'mode': 'js',
      'title': 'Итерируемый диапазон',
      'statement': 'Напишите класс Range(from, to, step = 1): итерируемый объект, который выдаёт числа от '
                   'from до to включительно с шагом step (step > 0) — протоколом [Symbol.iterator]() и '
                   'итератором с next(), без генераторов (function*).',
      'starter': 'class Range {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log([...new Range(1, 5)].join());\n'
                'console.log([...new Range(0, 10, 5)].join());\n'
                'console.log([...new Range(3, 1)].length);\n'
                'const r = new Range(1, 3);\n'
                'console.log([...r].join(), [...r].join());\n'
                'const [a, b] = new Range(7, 100);\n'
                'console.log(a, b, Array.from(new Range(1, 3), (x) => x * x).join());\n'
                'let n = 0;\n'
                'for (const x of new Range(1, 1000000)) { if (x > 3) break; n++; }\n'
                'console.log(n);\n'
                'console.log(__count("function" + "*") + __count("yield"));\n',
      'hint': 'Состояние (текущее число) держите внутри итератора, а не внутри Range, чтобы обход можно было '
              'повторить.',
      'expected': ['1,2,3,4,5', '0,5,10', '0', '1,2,3 1,2,3', '7 8 1,4,9', '3', '0']},
     {'id': 'j8-gen-range',
      'mode': 'js',
      'title': 'Генератор range',
      'statement': 'Напишите генератор range(start, end, step = 1): лениво выдаёт числа от start до end (не '
                   'включая) с шагом step; при отрицательном шаге идёт вниз; при шаге 0 бросает RangeError.',
      'starter': 'function* range(start, end, step = 1) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log([...range(0, 5)].join());\n'
                'console.log([...range(5, 0, -2)].join());\n'
                'console.log([...range(1, 1)].length);\n'
                'const g = range(0, 1e9);\n'
                'console.log(g.next().value, g.next().value, typeof g[Symbol.iterator]);\n'
                'try { [...range(0, 5, 0)]; } catch (e) { console.log(e.name); }\n',
      'hint': 'Два цикла for с yield; бесконечные/гигантские диапазоны безопасны, пока их не разворачивают '
              'целиком.',
      'expected': ['0,1,2,3,4', '5,3,1', '0', '0 1 function', 'RangeError']},
     {'id': 'j8-gen-fib',
      'mode': 'js',
      'title': 'Бесконечный генератор Фибоначчи',
      'statement': 'Напишите генератор fibs(), выдающий бесконечно числа Фибоначчи 0, 1, 1, 2, 3, … И '
                   'функцию take(iter, n): возвращает массив первых n значений любого итерируемого объекта '
                   '(ленивая: после n значений остановка, без бесконечного цикла).',
      'starter': 'function* fibs() {\n}\n\nfunction take(iter, n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(take(fibs(), 10).join());\n'
                'console.log(take(fibs(), 0).length);\n'
                'console.log(take([1, 2, 3], 5).join());\n'
                'console.log(take("abcdef", 3).join(""));\n'
                'console.log(take(fibs(), 80)[79]);\n',
      'hint': 'В take обходите iter циклом for…of и выходите по break при достижении n.',
      'expected': ['0,1,1,2,3,5,8,13,21,34', '0', '1,2,3', 'abc', '14472334024676220']},
     {'id': 'j8-lazy-pipeline',
      'mode': 'js',
      'title': 'Ленивый конвейер',
      'statement': 'Напишите генераторы lazyMap(iter, fn) и lazyFilter(iter, pred) — они ничего не '
                   'вычисляют, пока их не переберут, — и функцию firstN(iter, n) → массив первых n значений. '
                   'Проверьте на бесконечной последовательности чисел.',
      'starter': 'function* lazyMap(iter, fn) {\n'
                 '}\n'
                 '\n'
                 'function* lazyFilter(iter, pred) {\n'
                 '}\n'
                 '\n'
                 'function firstN(iter, n) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'function* naturals() { let n = 1; while (true) yield n++; }\n'
                'let calls = 0;\n'
                'const sq = lazyMap(naturals(), (x) => { calls++; return x * x; });\n'
                'console.log(calls);\n'
                'const evens = lazyFilter(sq, (x) => x % 2 === 0);\n'
                'console.log(calls);\n'
                'console.log(firstN(evens, 4).join());\n'
                'console.log(calls);\n'
                'console.log(firstN(lazyMap([1, 2, 3], (x) => x + 1), 10).join());\n',
      'hint': 'Каждый шаг — генератор поверх for…of; вычисления идут только при запросе следующего значения.',
      'expected': ['0', '0', '4,16,36,64', '8', '2,3,4']},
     {'id': 'j8-tree-inorder',
      'mode': 'js',
      'title': 'Обход дерева генератором',
      'statement': 'Дерево поиска задано объектами { value, left, right } (left/right могут быть null). '
                   'Напишите генератор inorder(node): выдаёт значения в порядке «левое поддерево — узел — '
                   'правое поддерево», используя yield*.',
      'starter': 'function* inorder(node) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'const t = { value: 4, left: { value: 2, left: { value: 1, left: null, right: null }, right: '
                '{ value: 3, left: null, right: null } }, right: { value: 6, left: { value: 5, left: null, '
                'right: null }, right: null } };\n'
                'console.log([...inorder(t)].join());\n'
                'console.log([...inorder(null)].length);\n'
                'console.log([...inorder({ value: 9, left: null, right: null })].join());\n'
                'console.log(Math.max(...inorder(t)));\n'
                'console.log(__count("yield" + "*") >= 2);\n',
      'hint': 'yield* inorder(node.left); yield node.value; yield* inorder(node.right);',
      'expected': ['1,2,3,4,5,6', '0', '9', '6', 'true']},
     {'id': 'j8-chunks-gen',
      'mode': 'js',
      'title': 'Генератор кусков',
      'statement': 'Напишите генератор chunked(iter, n): принимает любой итерируемый объект и лениво выдаёт '
                   'массивы по n элементов (последний — короче).',
      'starter': 'function* chunked(iter, n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify([...chunked([1, 2, 3, 4, 5], 2)]));\n'
                'console.log(JSON.stringify([...chunked("abcd", 2)]));\n'
                'console.log(JSON.stringify([...chunked([], 3)]));\n'
                'function* inf() { let i = 0; while (true) yield i++; }\n'
                'const g = chunked(inf(), 3);\n'
                'console.log(JSON.stringify(g.next().value), JSON.stringify(g.next().value));\n',
      'hint': 'Накапливайте буфер; отдавайте его при заполнении и в конце, если остаток не пуст.',
      'expected': ['[[1,2],[3,4],[5]]', '[["a","b"],["c","d"]]', '[]', '[0,1,2] [3,4,5]']},
     {'id': 'j8-linked-list',
      'mode': 'js',
      'title': 'Связный список с итератором',
      'statement': 'Напишите класс LinkedList: методы add(x) (в конец, возвращает this) и геттер size, а '
                   'также итератор [Symbol.iterator]() (генератором или объектом), чтобы список работал в '
                   'for…of, spread и Array.from. Узлы — объекты { value, next }.',
      'starter': 'class LinkedList {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const l = new LinkedList().add(1).add(2).add(3);\n'
                'console.log(l.size, [...l].join());\n'
                'for (const x of l) console.log(x);\n'
                'console.log(Array.from(l, (x) => x * 10).join());\n'
                'const [a, ...rest] = l;\n'
                'console.log(a, rest.join());\n'
                'console.log([...new LinkedList()].length);\n'
                'console.log([...l].length);\n',
      'hint': 'Метод-генератор: *[Symbol.iterator]() { … yield … }',
      'expected': ['3 1,2,3', '1', '2', '3', '10,20,30', '1 2,3', '0', '3']},
     {'id': 'j8-zip-iter',
      'mode': 'js',
      'title': 'Склейка итераторов вручную',
      'statement': 'Напишите генератор zipIter(a, b): принимает два итерируемых объекта и выдаёт пары [x, '
                   'y], пока есть значения в обоих; работайте с итераторами напрямую через '
                   'a[Symbol.iterator]() и next(), цикл for…of по a и b не используйте.',
      'starter': 'function* zipIter(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify([...zipIter([1, 2, 3], "ab")]));\n'
                'console.log(JSON.stringify([...zipIter([], [1])]));\n'
                'function* inf() { let i = 0; while (true) yield i++; }\n'
                'console.log(JSON.stringify([...zipIter(inf(), ["a", "b", "c"])]));\n'
                'console.log(JSON.stringify([...zipIter(new Set([1, 2]), new Map([[1, "x"], [2, '
                '"y"]]))]));\n',
      'hint': 'const ia = a[Symbol.iterator](); const x = ia.next(); проверьте x.done.',
      'expected': ['[[1,"a"],[2,"b"]]', '[]', '[[0,"a"],[1,"b"],[2,"c"]]', '[[1,[1,"x"]],[2,[2,"y"]]]']},
     {'id': 'j8-static-factory',
      'mode': 'js',
      'title': 'Статическая фабрика и toJSON',
      'statement': 'Напишите класс User(name, email) со статическим методом fromJSON(text) (создаёт User из '
                   'JSON-строки вида {"name":…,"email":…}) и методом toJSON(), который исключает поле email, '
                   'оставляя только name и поле type: "user". Так JSON.stringify(user) не раскрывает почту.',
      'starter': 'class User {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const u = User.fromJSON(\'{"name":"Ада","email":"ada@example.com"}\');\n'
                'console.log(u instanceof User, u.email);\n'
                'console.log(JSON.stringify(u));\n'
                'console.log(JSON.stringify([u, u]));\n'
                'console.log(JSON.stringify({ user: new User("Б", "b@x") }));\n',
      'hint': 'toJSON() возвращает объект, который и попадёт в результат JSON.stringify.',
      'expected': ['true ada@example.com',
                   '{"name":"Ада","type":"user"}',
                   '[{"name":"Ада","type":"user"},{"name":"Ада","type":"user"}]',
                   '{"user":{"name":"Б","type":"user"}}']},
     {'id': 'j8-to-string-tag',
      'mode': 'js',
      'title': 'Подпись объекта: Symbol.toStringTag',
      'statement': 'Напишите класс Token(kind, text) с геттером [Symbol.toStringTag], возвращающим '
                   '«Token:<kind>». Тогда Object.prototype.toString.call(token) даёт «[object '
                   'Token:<kind>]». Добавьте метод toString(), возвращающий text.',
      'starter': 'class Token {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = new Token("num", "42");\n'
                'console.log(Object.prototype.toString.call(t));\n'
                'console.log(String(t), `${t}`);\n'
                'console.log(Object.prototype.toString.call(new Token("id", "x")));\n'
                'console.log(Object.prototype.toString.call([]), Object.prototype.toString.call(null));\n',
      'hint': 'get [Symbol.toStringTag]() { return … }',
      'expected': ['[object Token:num]', '42 42', '[object Token:id]', '[object Array] [object Null]']}]}
