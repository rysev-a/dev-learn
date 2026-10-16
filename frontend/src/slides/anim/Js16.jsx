import { scene } from "./alg.tsx";
import { Box, Tx, arrow, jc } from "./jv.tsx";

/* Глава 16 книги «Современный Frontend»: события. */

// Цепочка предков: window → … → button
const chain = (hl = -1, c = "b") =>
  ["window", "document", "div#app", "ul.list", "li", "button"].map((n, i) =>
    Box(`n${i}`, 70, 20 + i * 26, 100, 20, n, i === hl ? "y" : c, {
      size: 8.5,
      mono: true,
    }),
  );

// 1. Реакции страницы
export const V01 = scene({
  labels: ["Что-то случилось", "Подписчики", "Путь по дереву"],
  caption: [
    "Страница живёт реакциями: пользователь нажал, ввёл, прокрутил, сеть ответила, таймер сработал — всё это события",
    "Объект сообщает, что что-то случилось, а подписчики получают уведомление и реагируют",
    "В браузере у события есть путь по дереву и действие по умолчанию, которое можно отменить",
  ],
  frames: [
    [
      Box("a", 90, 70, 100, 34, "клик", "y", { size: 11 }),
      Box("b", 270, 70, 100, 34, "событие", "g", { size: 11 }),
      arrow("e", 140, 70, 222, 70, "g"),
    ],
    [
      Box("s", 90, 70, 100, 34, "источник", "y", { size: 10.5 }),
      ...[0, 1, 2].map((i) =>
        Box(`h${i}`, 280, 40 + i * 30, 100, 22, `обработчик ${i + 1}`, "g", {
          size: 9,
        }),
      ),
      ...[0, 1, 2].map((i) => arrow(`e${i}`, 140, 70, 228, 40 + i * 30, "g")),
    ],
    [
      ...chain(5),
      Tx("n", 270, 76, "событие идёт\nпо цепочке\nпредков", { size: 10 }),
    ],
  ],
});

// 2. Подписка
export const V02 = scene({
  labels: ["addEventListener", "Параметры", "Объект события"],
  caption: [
    "addEventListener(имя, функция); удалить можно только по той же ссылке, поэтому анонимную стрелку не снять",
    "once — выполнить один раз, passive — обещание не отменять действие по умолчанию, signal — отписать сразу многих через AbortController",
    "Свойство onclick хранит только одну функцию, атрибут смешивает разметку и код — используем листенеры; обработчик получает объект события",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "function onClick(e) { … }",
          "btn.addEventListener('click', onClick);",
          "btn.removeEventListener('click', onClick);",
        ],
        [1, 2],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "const ac = new AbortController();",
          "el.addEventListener('scroll', f, {",
          "  passive: true, signal: ac.signal });",
          "ac.abort();   // снимет всех",
        ],
        [2, 3],
        { w: 330, size: 10, lh: 22 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "btn.onclick = f;   // одна функция",
          "btn.onclick = g;   // f потеряна",
          "btn.addEventListener('click', (e) => {",
          "  console.log(e.type, e.target);",
          "});",
        ],
        [3],
        { w: 330, size: 9.5, lh: 20 },
      ),
    ],
  ],
});

// 3. Фазы
export const V03 = scene({
  labels: ["Погружение", "Цель и всплытие", "target и currentTarget"],
  caption: [
    "Сначала погружение: от окна вниз по предкам к цели — на нём срабатывают подписки с capture: true",
    "Затем фаза цели, потом всплытие обратно вверх до окна — обычные подписки слушают именно его",
    "target — где событие возникло, currentTarget — чей обработчик выполняется; focus и blur не всплывают — у них есть парные focusin и focusout",
  ],
  frames: [
    [
      ...chain(-1),
      ...[0, 1, 2, 3, 4].map((i) =>
        arrow(`d${i}`, 124, 28 + i * 26, 124, 38 + i * 26, "y"),
      ),
      Tx("n", 270, 76, "1. capture ↓", { size: 11, c: "y" }),
    ],
    [
      ...chain(5, "g"),
      ...[0, 1, 2, 3, 4].map((i) =>
        arrow(`u${i}`, 16, 124 - i * 26, 16, 108 - i * 26, "g"),
      ),
      Tx("n", 270, 76, "2. цель\n3. bubble ↑", { size: 11, c: "g" }),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "ul.addEventListener('click', (e) => {",
          "  e.target         // span внутри кнопки",
          "  e.currentTarget  // ul",
          "});",
        ],
        [1, 2],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 4. Остановка
export const V04 = scene({
  labels: ["stopPropagation", "stopImmediatePropagation", "Осторожно"],
  caption: [
    "stopPropagation: события не пойдут дальше по цепочке, но остальные обработчики на текущем элементе выполнятся",
    "stopImmediatePropagation останавливает и их",
    "Злоупотреблять остановкой не стоит: она ломает чужие обработчики и аналитику, которые рассчитывают на всплытие",
  ],
  frames: [
    [
      Box("a", 90, 40, 100, 24, "button", "b", { size: 10, mono: true }),
      Box("b", 90, 80, 100, 24, "li ✕", "r", { size: 10, mono: true }),
      Box("c", 90, 120, 100, 24, "ul", "m", { size: 10, mono: true }),
      arrow("e1", 90, 52, 90, 68, "g"),
      arrow("e2", 90, 92, 90, 108, "m"),
      Tx("n", 270, 80, "stopPropagation()\nвыше не идёт", { size: 10 }),
    ],
    [
      Box("a", 110, 50, 120, 24, "handler 1  stopImm.", "r", { size: 8.5 }),
      Box("b", 110, 90, 120, 24, "handler 2  — не вызван", "m", { size: 8.5 }),
      Box("c", 110, 130, 120, 24, "родитель  — не вызван", "m", { size: 8.5 }),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "// плохо:",
          "e.stopPropagation();   // аналитика не узнает",
          "// лучше — свой признак:",
          "if (e.defaultPrevented) return;",
        ],
        [1, 3],
        { w: 330, size: 10, lh: 24, bad: [1] },
      ),
    ],
  ],
});

// 5. Делегирование
export const V05 = scene({
  labels: ["Один обработчик", "closest", "Динамика"],
  caption: [
    "Вместо сотни обработчиков на сотне кнопок — один на общем родителе: по target выясняют, куда попали",
    "Событие может прийти от значка внутри кнопки — поднимаемся до нужного элемента методом closest",
    "Элементы, добавленные позже, работают без новой подписки; действие хранят в data-action, а цель должна лежать внутри контейнера",
  ],
  frames: [
    [
      Box("u", 110, 40, 110, 24, "ul (1 обработчик)", "y", { size: 9 }),
      ...[0, 1, 2].map((i) =>
        Box(`l${i}`, 70 + i * 50, 100, 40, 24, `li ${i + 1}`, "b", {
          size: 9,
          mono: true,
        }),
      ),
      ...[0, 1, 2].map((i) => arrow(`e${i}`, 70 + i * 50, 88, 110, 52, "g")),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "list.addEventListener('click', (e) => {",
          "  const btn = e.target.closest('button');",
          "  if (!btn || !list.contains(btn)) return;",
          "  run(btn.dataset.action);",
          "});",
        ],
        [1, 2],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      Box("u", 110, 50, 110, 24, "ul", "y", { size: 10 }),
      Box("a", 70, 100, 40, 24, "li", "b", { size: 9 }),
      Box("b", 120, 100, 40, 24, "li", "b", { size: 9 }),
      Box("n", 170, 100, 40, 24, "+ li", "g", { size: 9 }),
      Tx("t", 290, 76, "новый li\nработает сразу", { size: 10 }),
    ],
  ],
});

// 6. Действие по умолчанию
export const V06 = scene({
  labels: ["preventDefault", "passive", "Что имеет поведение"],
  caption: [
    "Клик по ссылке переходит, отправка формы перезагружает страницу — preventDefault отменяет, если событие отменяемое (cancelable)",
    "Пассивные слушатели scroll и touch не ждут обработчика, чтобы начать прокрутку; вызвать preventDefault из них уже нельзя",
    "Стандартное поведение есть у выделения текста, контекстного меню, перетаскивания; return false в onclick — устаревшая привычка",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "form.addEventListener('submit', (e) => {",
          "  e.preventDefault();",
          "  send(new FormData(form));",
          "});",
        ],
        [1],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      jc(
        "c",
        20,
        44,
        [
          "window.addEventListener('touchstart', f, {",
          "  passive: true,",
          "});",
          "// preventDefault() внутри f — не сработает",
        ],
        [1],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      ...["ссылка", "форма", "пробел", "контекстное меню", "drag"].map((n, i) =>
        Box(
          `p${i}`,
          66 + (i % 3) * 114,
          56 + Math.floor(i / 3) * 44,
          100,
          28,
          n,
          "b",
          { size: 9.5 },
        ),
      ),
    ],
  ],
});

// 7. Указатели
export const V07 = scene({
  labels: ["Pointer Events", "Захват указателя", "Координаты"],
  caption: [
    "pointerdown, pointermove, pointerup, pointercancel работают одинаково для мыши, пера и пальца; у каждого указателя свой pointerId",
    "setPointerCapture направляет все события указателя в элемент, даже когда курсор ушёл за его границы — так строят перетаскивание и ползунки",
    "clientX — от окна, pageX — от документа, offsetX — от элемента: их легко перепутать; тач-события нужны для жестов вроде щипка",
  ],
  frames: [
    [
      ...["down", "move", "up", "cancel"].map((n, i) =>
        Box(`p${i}`, 56 + i * 86, 70, 76, 30, `pointer${n}`, "g", {
          size: 8,
          mono: true,
        }),
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "knob.addEventListener('pointerdown', (e) => {",
          "  knob.setPointerCapture(e.pointerId);",
          "});",
          "knob.addEventListener('pointermove', drag);",
        ],
        [1],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      ...["clientX", "pageX", "offsetX"].map((n, i) =>
        Box(`c${i}`, 66 + i * 114, 60, 100, 28, n, ["b", "y", "g"][i], {
          size: 10,
          mono: true,
        }),
      ),
      Tx("t", 180, 116, "окно · документ · элемент", { size: 9.5 }),
    ],
  ],
});

// 8. Клавиатура
export const V08 = scene({
  labels: ["keydown и keyup", "key и code", "Композиция"],
  caption: [
    "keydown и keyup; keypress устарел; свойство repeat показывает автоповтор при удерживании; модификаторы — ctrlKey, shiftKey, altKey, metaKey",
    "key — какой символ получится с учётом раскладки, code — физическая клавиша: для горячих клавиш обычно нужен code",
    "События композиции сообщают о наборе через редактор ввода (IME): реагировать на keydown в такие моменты нельзя; интерактивный элемент должен управляться и клавиатурой",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "document.addEventListener('keydown', (e) => {",
          "  if (e.repeat) return;",
          "  if (e.ctrlKey && e.code === 'KeyS') save();",
          "});",
        ],
        [1, 2],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      Box("a", 110, 60, 130, 30, "key: «ы»", "b", { size: 11 }),
      Box("b", 110, 110, 130, 30, "code: KeyS", "g", { size: 11 }),
      Tx("n", 280, 85, "раскладка\nRU", { size: 10 }),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "input.addEventListener('compositionstart', …);",
          "input.addEventListener('compositionend', …);",
          "if (e.isComposing) return;",
        ],
        [2],
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
  ],
});

// 9. Формы и фокус
export const V09 = scene({
  labels: ["focus и blur", "input и change", "submit и буфер"],
  caption: [
    "focus и blur срабатывают при входе и выходе из поля и не всплывают; программно — метод focus, порядок Tab — tabindex и структура документа",
    "input возникает при каждом изменении значения, change — при завершении изменения (обычно при потере фокуса)",
    "submit приходит на форму и перехватывается; beforeinput проверяет ввод заранее; события copy, cut и paste меняют то, что попадёт в буфер",
  ],
  frames: [
    [
      Box("a", 90, 70, 110, 30, "focus ▸", "g", { size: 11 }),
      Box("b", 270, 70, 110, 30, "◂ blur", "r", { size: 11 }),
      Tx("n", 180, 118, "не всплывают → focusin / focusout", { size: 9.5 }),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "input.oninput  // 'а', 'ав', 'авт'…",
          "input.onchange // при уходе из поля",
        ],
        [0],
        { w: 330, size: 10.5, lh: 28 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "form.addEventListener('submit', onSubmit);",
          "input.addEventListener('beforeinput', check);",
          "el.addEventListener('paste', (e) => …);",
        ],
        [0, 1, 2],
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
  ],
});

// 10. Свои события
export const V10 = scene({
  labels: ["CustomEvent", "EventTarget", "Осторожно"],
  caption: [
    "new CustomEvent(имя, { detail, bubbles, composed }); отправляют dispatchEvent; composed позволяет выйти за границы теневого DOM",
    "Любой объект можно сделать целью событий, унаследовав от EventTarget; в Node.js для этого — EventEmitter",
    "Шина событий развязывает части приложения, но превращается в клубок невидимых связей; подписки снимайте, когда компонент уходит",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "el.dispatchEvent(new CustomEvent('selected', {",
          "  detail: { id: 7 }, bubbles: true,",
          "}));",
          "el.addEventListener('selected', (e) => e.detail.id);",
        ],
        [0, 3],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      jc(
        "c",
        20,
        44,
        [
          "class Store extends EventTarget {",
          "  set(v) { this.v = v;",
          "    this.dispatchEvent(new Event('change')); }",
          "}",
        ],
        [0],
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
    [
      ...["A", "B", "C", "D"].map((n, i) =>
        Box(
          `n${i}`,
          70 + (i % 2) * 90,
          52 + Math.floor(i / 2) * 50,
          56,
          28,
          n,
          "b",
          { size: 11 },
        ),
      ),
      Box("bus", 280, 76, 90, 40, "шина", "y", { size: 11 }),
      Tx("t", 180, 140, "невидимые связи", { size: 9.5, c: "r" }),
    ],
  ],
});

// 11. Частые события
export const V11 = scene({
  labels: ["Дебаунс", "Троттлинг", "Лучше события не слушать"],
  caption: [
    "Дебаунс откладывает вызов до паузы в событиях — подходит для поиска при вводе",
    "Троттлинг пропускает не чаще заданного интервала — подходит для прокрутки; для анимаций — requestAnimationFrame",
    "Для слежения за видимостью лучше IntersectionObserver, чем обработчик scroll; пассивные слушатели и один AbortController на компонент",
  ],
  frames: [
    [
      ...Array.from({ length: 8 }, (_, i) =>
        Box(`e${i}`, 40 + i * 40, 60, 30, 22, "·", "m", { size: 12 }),
      ),
      Box("d", 330, 60, 40, 22, "▲", "g", { size: 11 }),
      Tx("n", 180, 110, "вызов — только после паузы", { size: 10 }),
    ],
    [
      ...Array.from({ length: 8 }, (_, i) =>
        Box(
          `e${i}`,
          40 + i * 40,
          60,
          30,
          22,
          i % 3 === 0 ? "▲" : "·",
          i % 3 === 0 ? "g" : "m",
          { size: 11 },
        ),
      ),
      Tx("n", 180, 110, "не чаще раза в интервал", { size: 10 }),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "new IntersectionObserver(([e]) => {",
          "  if (e.isIntersecting) load();",
          "}).observe(el);",
          "// вместо window.onscroll",
        ],
        [3],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 12. Порядок и автоматы
export const V12 = scene({
  labels: ["Синхронный dispatch", "Автомат", "Жесты"],
  caption: [
    "Обработчики пользовательских событий — задачи; но click() и dispatchEvent выполняют их синхронно, внутри вашего вызова: микрозадачи ещё не обработаны",
    "Перетаскивание, долгое нажатие, двойное касание, свайп удобно описывать конечными автоматами: состояние и переходы по событиям",
    "Логика отделена от обработчиков, а крайние случаи — например, отмену перетаскивания клавишей Escape — видно сразу",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "btn.addEventListener('click', () => log('a'));",
          "Promise.resolve().then(() => log('микро'));",
          "btn.click();   // 'a' — прямо здесь",
          "log('после');",
        ],
        [2],
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
    [
      Box("i", 70, 70, 60, 28, "idle", "b", { size: 10 }),
      Box("p", 180, 70, 70, 28, "pressed", "y", { size: 10 }),
      Box("d", 290, 70, 70, 28, "dragging", "g", { size: 10 }),
      arrow("e1", 100, 70, 142, 70, "g"),
      arrow("e2", 214, 70, 252, 70, "g"),
      Tx("a", 120, 54, "down", { size: 8.5, mono: true }),
      Tx("b", 232, 54, "move>5px", { size: 8.5, mono: true }),
    ],
    [
      ...["долгое нажатие", "свайп", "двойной тап", "щипок"].map((n, i) =>
        Box(
          `g${i}`,
          66 + (i % 2) * 130,
          56 + Math.floor(i / 2) * 44,
          116,
          28,
          n,
          "b",
          { size: 9.5 },
        ),
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Путь", "Практика", "Дальше"],
  caption: [
    "Погружение → цель → всплытие; target и currentTarget различаются; делегирование ставит один обработчик на контейнер и использует closest",
    "preventDefault, passive, Pointer Events, code для горячих клавиш; CustomEvent и EventTarget; дебаунс и троттлинг; сложные жесты — автоматы",
    "Дальше — формы и хранилища данных",
  ],
  frames: [
    [
      Box("a", 90, 60, 120, 30, "capture ↓ target ↑", "y", { size: 9.5 }),
      Box("b", 240, 60, 130, 30, "делегирование", "b", { size: 10.5 }),
      Box("c", 160, 116, 190, 28, "closest()", "g", { size: 10.5, mono: true }),
    ],
    [
      Box("a", 90, 60, 120, 30, "pointer · code", "y", { size: 10.5 }),
      Box("b", 240, 60, 130, 30, "CustomEvent", "b", { size: 10.5 }),
      Box("c", 160, 116, 190, 28, "debounce · throttle", "g", { size: 10 }),
    ],
    [
      jc(
        "c",
        30,
        40,
        [
          "localStorage.setItem('theme', 'dark');",
          "history.pushState({}, '', '/about');",
        ],
        undefined,
        { w: 310, size: 10.5, lh: 26 },
      ),
      Tx("n", 180, 120, "глава 17: формы и хранилища", { size: 9.5 }),
    ],
  ],
});
