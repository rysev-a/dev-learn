import { scene } from "./alg.jsx";
import { Box, Tx, arrow, jc, slot } from "./jv.jsx";

/* Глава 8 книги «Современный Frontend»: классы, прототипы и итераторы. */

// 1. Объекты с поведением
export const V01 = scene({
  labels: ["Литерал", "Класс", "Что под ним"],
  caption: [
    "Литералами удобно создавать единичные объекты, но у многих объектов должно быть общее поведение",
    "Для этого в JavaScript есть классы — синтаксис знаком по Python и Java",
    "Под классом лежит собственная модель — цепочка прототипов; её понимание объясняет наследование и this",
  ],
  frames: [
    [
      jc(
        "c",
        40,
        44,
        ["const u = {", "  name: 'Ада',", "  hi() { … },", "};"],
        undefined,
        { w: 240, size: 11, lh: 20 },
      ),
    ],
    [
      jc(
        "c",
        40,
        40,
        [
          "class User {",
          "  constructor(name) {",
          "    this.name = name;",
          "  }",
          "  hi() { … }",
          "}",
        ],
        [0],
        { w: 260, size: 10.5, lh: 18 },
      ),
    ],
    [
      Box("i", 90, 60, 110, 30, "экземпляр", "b", { size: 10 }),
      arrow("e", 146, 60, 214, 60, "g"),
      Box("p", 270, 60, 110, 30, "прототип", "y", { size: 10 }),
      Tx("n", 180, 118, "ссылка на прототип у каждого объекта", { size: 9.5 }),
    ],
  ],
});

// 2. Цепочка прототипов
export const V02 = scene({
  labels: ["Цепочка", "Поиск поля", "Запись и затенение"],
  caption: [
    "У каждого объекта есть ссылка на прототип; цепочка заканчивается значением null",
    "Поле ищется в самом объекте, потом по цепочке вверх: так находится toString в Object.prototype",
    "Запись всегда идёт в сам объект, поэтому унаследованное значение можно затенить",
  ],
  frames: [
    [
      Box("a", 60, 76, 80, 30, "obj", "b", { size: 10 }),
      arrow("e1", 100, 76, 134, 76, "g"),
      Box("b", 180, 76, 80, 30, "proto", "y", { size: 10 }),
      arrow("e2", 220, 76, 254, 76, "g"),
      Box("c", 306, 76, 96, 30, "Object.prototype", "y", { size: 8.5 }),
      arrow("e3", 306, 94, 306, 124, "g"),
      Box("d", 306, 138, 50, 22, "null", "m", { size: 9 }),
    ],
    [
      Box("a", 60, 76, 80, 30, "obj", "b", { size: 10 }),
      arrow("e1", 100, 76, 134, 76, "g"),
      Box("b", 180, 76, 80, 30, "proto", "y", { size: 10 }),
      arrow("e2", 220, 76, 254, 76, "g"),
      Box("c", 306, 76, 96, 30, "Object.prototype", "g", { size: 8.5 }),
      Tx("n", 180, 130, "obj.toString() → найден здесь", {
        size: 9.5,
        mono: true,
      }),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "const base = { n: 1 };",
          "const o = Object.create(base);",
          "o.n         // 1 — из base",
          "o.n = 5;    // запись в o",
          "base.n      // 1 — не изменилось",
        ],
        [3, 4],
        { w: 330, size: 10, lh: 20 },
      ),
    ],
  ],
});

// 3. Конструктор и new
export const V03 = scene({
  labels: ["Конструктор", "Что делает new", "instanceof"],
  caption: [
    "До классов объекты создавали функциями-конструкторами; методы клали в поле prototype",
    "new создаёт пустой объект, связывает его прототип, вызывает функцию с this и возвращает объект",
    "instanceof проверяет, есть ли prototype конструктора в цепочке объекта; забытый new — частая ошибка",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        30,
        [
          "function User(name) {",
          "  this.name = name;",
          "}",
          "User.prototype.hi = function () {",
          "  return 'Привет, ' + this.name;",
          "};",
        ],
        [3],
        { w: 330, size: 9.5, lh: 18 },
      ),
    ],
    [
      ...[
        "1. пустой объект",
        "2. связать прототип",
        "3. вызвать с this",
        "4. вернуть объект",
      ].map((t, i) =>
        Box(`s${i}`, 180, 34 + i * 34, 200, 26, t, i === 3 ? "g" : "b", {
          size: 10,
        }),
      ),
    ],
    [
      jc(
        "c",
        30,
        36,
        [
          "const u = new User('Ада');",
          "u instanceof User    // true",
          "u instanceof Object  // true",
          "User('Б')  // без new → ошибка",
        ],
        [1, 2],
        { w: 310, size: 10, lh: 20, bad: [3] },
      ),
    ],
  ],
});

// 4. class
export const V04 = scene({
  labels: ["Класс", "Это функция", "Не поднимается"],
  caption: [
    "Внутри класса — конструктор и методы; методы попадают в прототип и не перечисляются в циклах",
    "typeof класса — «function»: класс и есть функция-конструктор; без new его не вызвать",
    "Класс не поднимается: объявляйте до использования; тело класса всегда в строгом режиме",
  ],
  frames: [
    [
      jc(
        "c",
        30,
        30,
        [
          "class Point {",
          "  constructor(x, y) {",
          "    this.x = x; this.y = y;",
          "  }",
          "  len() { return Math.hypot(this.x, this.y); }",
          "}",
        ],
        [4],
        { w: 320, size: 9.5, lh: 18 },
      ),
    ],
    [
      jc(
        "c",
        30,
        40,
        [
          "typeof Point           // 'function'",
          "Point(1, 2)",
          "// TypeError: Class constructor",
          "//   Point cannot be invoked without 'new'",
        ],
        [1, 2],
        { w: 320, size: 9.5, lh: 20, bad: [1, 2] },
      ),
    ],
    [
      jc(
        "c",
        30,
        40,
        ["const p = new Point(1, 2);  // ReferenceError", "class Point { … }"],
        [0],
        { w: 310, size: 10, lh: 24, bad: [0] },
      ),
    ],
  ],
});

// 5. Поля, приватность, static, accessors
export const V05 = scene({
  labels: ["Поля и #private", "static", "get и set"],
  caption: [
    "Поля объявляются в теле класса; имя с решёткой — приватное: снаружи недоступно даже через [ ]",
    "static создаёт методы и поля самого класса, а не экземпляров — для фабрик и счётчиков",
    "Геттеры и сеттеры выглядят как поля, но выполняют код: вычисляемые свойства и проверка при записи",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        30,
        [
          "class Acc {",
          "  #balance = 0;",
          "  deposit(x) { this.#balance += x; }",
          "}",
          "new Acc().#balance  // SyntaxError",
        ],
        [1],
        { w: 330, size: 9.5, lh: 20, bad: [4] },
      ),
    ],
    [
      jc(
        "c",
        30,
        36,
        [
          "class Id {",
          "  static next = 1;",
          "  static make() { return Id.next++; }",
          "}",
          "Id.make()   // 1",
        ],
        [1, 2],
        { w: 310, size: 10, lh: 20 },
      ),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "class Temp {",
          "  #c = 0;",
          "  get f() { return this.#c * 9 / 5 + 32; }",
          "  set c(v) {",
          "    if (v < -273) throw new RangeError();",
          "    this.#c = v;",
          "  }",
          "}",
        ],
        [2, 3],
        { w: 335, size: 9.5, lh: 15 },
      ),
    ],
  ],
});

// 6. Наследование
export const V06 = scene({
  labels: ["extends и super", "Цепочка", "Свои ошибки"],
  caption: [
    "Дочерний класс получает методы родителя, переопределяет их и вызывает родительскую версию через super",
    "В конструкторе дочернего класса super() нужно вызвать до первого обращения к this",
    "Свои ошибки делают наследниками Error: тогда instanceof и стек вызовов работают как у стандартных",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        30,
        [
          "class Animal {",
          "  speak() { return '...'; }",
          "}",
          "class Dog extends Animal {",
          "  speak() { return super.speak() + ' гав'; }",
          "}",
        ],
        [3, 4],
        { w: 330, size: 9.5, lh: 18 },
      ),
    ],
    [
      Box("a", 70, 90, 100, 28, "Dog.prototype", "b", { size: 9.5 }),
      arrow("e1", 120, 90, 150, 90, "g"),
      Box("b", 210, 90, 110, 28, "Animal.prototype", "y", { size: 9 }),
      arrow("e2", 266, 90, 296, 90, "g"),
      Box("c", 330, 90, 56, 28, "Object", "y", { size: 9 }),
      Tx("n", 180, 140, "constructor(): super() до this", {
        size: 9.5,
        mono: true,
      }),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "class HttpError extends Error {",
          "  constructor(status, msg) {",
          "    super(msg);",
          "    this.name = 'HttpError';",
          "    this.status = status;",
          "  }",
          "}",
        ],
        [2],
        { w: 330, size: 9.5, lh: 18 },
      ),
    ],
  ],
});

// 7. Потеря this
export const V07 = scene({
  labels: ["Колбэк теряет this", "bind и стрелка-поле", "Обёртка"],
  caption: [
    "Метод, переданный как колбэк, теряет объект: обращение к полю падает с TypeError",
    "Решения: привязать в конструкторе через bind или объявить метод полем-стрелкой — но копия на каждый объект",
    "Третий путь — оборачивать вызов в стрелку при передаче: () => obj.method()",
  ],
  frames: [
    [
      jc(
        "c",
        30,
        40,
        [
          "button.onclick = timer.tick;",
          "// TypeError: Cannot read properties",
          "//   of undefined (reading 'n')",
        ],
        [0],
        { w: 310, size: 10, lh: 22, bad: [1, 2] },
      ),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "constructor() {",
          "  this.tick = this.tick.bind(this);",
          "}",
          "// или поле:",
          "tick = () => { this.n++; };",
        ],
        [1, 4],
        { w: 330, size: 9.5, lh: 20 },
      ),
    ],
    [
      jc(
        "c",
        30,
        40,
        [
          "button.onclick = () => timer.tick();",
          "setTimeout(() => timer.tick(), 0);",
        ],
        [0, 1],
        { w: 320, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 8. Композиция
export const V08 = scene({
  labels: ["Глубокая иерархия", "Композиция", "Подмешивание"],
  caption: [
    "Глубокие иерархии хрупки: изменение родителя ломает потомков",
    "Лучше собирать объект из возможностей: «умеет летать», «умеет плавать» — отдельными функциями",
    "Подмешивают через Object.assign или spread; в JavaScript важно, есть ли нужный метод, а не от кого он унаследован",
  ],
  frames: [
    [
      Box("a", 180, 30, 100, 24, "Животное", "b", { size: 9.5 }),
      Box("b", 180, 66, 100, 24, "Птица", "b", { size: 9.5 }),
      Box("c", 180, 102, 100, 24, "Пингвин", "r", { size: 9.5 }),
      arrow("e1", 180, 54, 180, 60, "g"),
      arrow("e2", 180, 90, 180, 96, "g"),
      Tx("n", 180, 148, "пингвин, который «летает»?", { size: 9.5, c: "r" }),
    ],
    [
      Box("f", 80, 60, 100, 26, "canFly", "y", { size: 10 }),
      Box("s", 80, 100, 100, 26, "canSwim", "y", { size: 10 }),
      Box("p", 290, 80, 100, 36, "пингвин", "g", { size: 10 }),
      arrow("e1", 130, 66, 238, 74, "g"),
      arrow("e2", 130, 100, 238, 88, "g"),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "const canSwim = { swim() { … } };",
          "const penguin = {",
          "  ...canSwim, walk() { … },",
          "};",
          "penguin.swim?.()",
        ],
        [2, 4],
        { w: 330, size: 9.5, lh: 20 },
      ),
    ],
  ],
});

// 9. Дескрипторы
export const V09 = scene({
  labels: ["Три флага", "defineProperty", "freeze и seal"],
  caption: [
    "У каждого свойства есть флаги: writable — запись, enumerable — видимость в циклах, configurable — удаление",
    "Object.defineProperty задаёт флаги вручную, getOwnPropertyDescriptor показывает их",
    "freeze запрещает запись и удаление, seal запечатывает набор свойств, preventExtensions запрещает только добавление",
  ],
  frames: [
    [
      Box("w", 70, 76, 100, 36, "writable\nзапись", "b", { size: 9.5 }),
      Box("e", 180, 76, 100, 36, "enumerable\nв циклах", "b", { size: 9.5 }),
      Box("c", 290, 76, 100, 36, "configurable\nудаление", "b", { size: 9.5 }),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "Object.defineProperty(o, 'id', {",
          "  value: 7,",
          "  writable: false,",
          "  enumerable: false,",
          "});",
          "o.id = 9;   // молча игнорируется",
        ],
        [2, 3],
        { w: 330, size: 9.5, lh: 18 },
      ),
    ],
    [
      Box("a", 70, 56, 100, 26, "preventExtensions", "b", { size: 8 }),
      Box("b", 180, 56, 80, 26, "seal", "y", { size: 9.5 }),
      Box("c", 290, 56, 100, 26, "freeze", "g", { size: 9.5 }),
      Tx("t1", 70, 90, "нельзя\nдобавлять", { size: 8.5 }),
      Tx("t2", 180, 90, "+ нельзя\nудалять", { size: 8.5 }),
      Tx("t3", 290, 90, "+ нельзя\nменять", { size: 8.5 }),
      Tx("n", 180, 140, "заморозка поверхностная", { size: 9.5, c: "y" }),
    ],
  ],
});

// 10. Символы и протоколы
export const V10 = scene({
  labels: ["Symbol", "Известные символы", "Протокол"],
  caption: [
    "Символ — уникальное значение; как ключ он не конфликтует ни с какими строковыми именами",
    "Встроенные символы — Symbol.iterator, Symbol.toPrimitive, Symbol.toStringTag — управляют поведением языка",
    "Если у объекта есть метод с ключом Symbol.iterator, его принимают for…of, spread, деструктурирование и Array.from",
  ],
  frames: [
    [
      jc(
        "c",
        30,
        36,
        [
          "const id = Symbol('id');",
          "const o = { [id]: 1, id: 2 };",
          "Symbol('id') === Symbol('id')  // false",
        ],
        [2],
        { w: 310, size: 10, lh: 22 },
      ),
    ],
    [
      jc(
        "c",
        30,
        36,
        [
          "obj[Symbol.iterator]     // перебор",
          "obj[Symbol.toPrimitive]   // приведение",
          "obj[Symbol.toStringTag]   // подпись",
        ],
        undefined,
        { w: 310, size: 10, lh: 22 },
      ),
    ],
    [
      Box("o", 80, 76, 100, 30, "свой объект\n[Symbol.iterator]", "y", {
        size: 8,
      }),
      arrow("e", 130, 76, 196, 76, "g"),
      ...["for…of", "[...x]", "Array.from", "[a, b] = x"].map((t, i) =>
        Box(`u${i}`, 270, 38 + i * 32, 100, 24, t, "g", {
          size: 9.5,
          mono: true,
        }),
      ),
    ],
  ],
});

// 11. Протокол итератора
export const V11 = scene({
  labels: ["next()", "Ручной итератор", "Ленивость"],
  caption: [
    "Итератор — объект с методом next(), который возвращает { value, done }; done: true означает конец",
    "for…of вызывает next() снова и снова; свой итератор нужно писать с хранением состояния",
    "Элементы вычисляются по запросу, поэтому так можно описать бесконечную последовательность; break вызывает return()",
  ],
  frames: [
    [
      ...[
        ["{ value: 1, done: false }", "g"],
        ["{ value: 2, done: false }", "g"],
        ["{ value: undefined, done: true }", "y"],
      ].map(([t, c], i) =>
        Box(`n${i}`, 180, 36 + i * 40, 230, 28, t, c, {
          size: 9.5,
          mono: true,
        }),
      ),
      Tx("t", 60, 76, "next()", { size: 10, mono: true }),
    ],
    [
      jc(
        "c",
        20,
        24,
        [
          "const range = {",
          "  from: 1, to: 3,",
          "  [Symbol.iterator]() {",
          "    let n = this.from, to = this.to;",
          "    return { next: () =>",
          "      n <= to ? { value: n++, done: false }",
          "              : { value: undefined, done: true } };",
          "  },",
          "};",
        ],
        [2, 4],
        { w: 340, size: 8.5, lh: 15 },
      ),
    ],
    [
      jc(
        "c",
        30,
        40,
        [
          "for (const x of naturals()) {",
          "  if (x > 3) break;   // вызов return()",
          "  console.log(x);",
          "}",
        ],
        [1],
        { w: 310, size: 10, lh: 22 },
      ),
      Tx("n", 180, 140, "бесконечная последовательность — не проблема", {
        size: 9.5,
      }),
    ],
  ],
});

// 12. Генераторы
export const V12 = scene({
  labels: ["function*", "yield", "yield*"],
  caption: [
    "Функция со звёздочкой при вызове не выполняется, а возвращает объект-генератор",
    "Каждый yield приостанавливает выполнение и отдаёт значение; следующий next() продолжает с того же места",
    "yield* делегирует перебор другому итерируемому объекту; на генераторах построены и async-функции",
  ],
  frames: [
    [
      jc(
        "c",
        30,
        36,
        [
          "function* gen() {",
          "  yield 1;",
          "  yield 2;",
          "}",
          "const g = gen();   // ничего не выполнено",
        ],
        [0, 4],
        { w: 310, size: 10, lh: 20 },
      ),
    ],
    [
      jc(
        "c",
        20,
        24,
        [
          "function* fib() {",
          "  let [a, b] = [0, 1];",
          "  while (true) {",
          "    yield a;",
          "    [a, b] = [b, a + b];",
          "  }",
          "}",
          "[...take(fib(), 6)]  // 0 1 1 2 3 5",
        ],
        [3],
        { w: 330, size: 9.5, lh: 18 },
      ),
    ],
    [
      jc(
        "c",
        30,
        40,
        [
          "function* walk(t) {",
          "  if (!t) return;",
          "  yield* walk(t.left);",
          "  yield t.value;",
          "  yield* walk(t.right);",
          "}",
        ],
        [2, 4],
        { w: 310, size: 10, lh: 20 },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Классы", "Итераторы", "Дальше"],
  caption: [
    "Каждый объект ссылается на прототип; класс — запись конструктора и прототипа; поля с #, static, get и set",
    "Наследование — extends и super, но композиция часто надёжнее; итераторы питают for…of и spread, а генераторы пишут их коротко",
    "Дальше — модули и ошибки, а затем асинхронность: промисы, async и await",
  ],
  frames: [
    [
      Box("a", 90, 60, 120, 30, "прототип", "y", { size: 10.5 }),
      Box("b", 240, 60, 130, 30, "class #поле", "b", { size: 10.5 }),
      Box("c", 160, 116, 190, 28, "this теряется — привязывайте", "g", {
        size: 9.5,
      }),
    ],
    [
      Box("a", 90, 60, 120, 30, "extends / super", "b", { size: 10 }),
      Box("b", 240, 60, 130, 30, "Symbol.iterator", "y", { size: 10 }),
      Box("c", 160, 116, 190, 28, "function* и yield", "g", { size: 10 }),
    ],
    [
      jc(
        "c",
        40,
        40,
        [
          "console.log('1');",
          "setTimeout(() => console.log('2'), 0);",
          "console.log('3');",
        ],
        undefined,
        { w: 290, size: 10.5, lh: 22 },
      ),
      Tx("n", 180, 140, "глава 9: модули и ошибки", { size: 9.5 }),
    ],
  ],
});
