import { scene } from "./alg.jsx";
import { Box, Tx, arrow, jc } from "./jv.jsx";

/* Глава 14 книги «Современный Frontend»: дерево DOM. */

const nd = (id, x, y, text, c = "b", w = 52) =>
  Box(id, x, y, w, 22, text, c, { size: 9, mono: true });

// 1. Разметка → дерево
export const V01 = scene({
  labels: ["Разметка", "Дерево", "API"],
  caption: [
    "Браузер превращает разметку в дерево объектов; изменение дерева сразу отражается на экране",
    "Каждый элемент — узел: у него есть родитель, дети и соседи",
    "JavaScript читает и меняет страницу через программный интерфейс DOM — им же пользуются и фреймворки",
  ],
  frames: [
    [
      jc(
        "c",
        40,
        44,
        ['<ul id="list">', "  <li>раз</li>", "  <li>два</li>", "</ul>"],
        undefined,
        { w: 280, size: 11, lh: 22 },
      ),
    ],
    [
      nd("u", 180, 36, "ul", "y"),
      nd("a", 120, 84, "li", "b"),
      nd("b", 240, 84, "li", "b"),
      nd("t1", 120, 130, "раз", "g"),
      nd("t2", 240, 130, "два", "g"),
      arrow("e1", 180, 48, 130, 72, "g"),
      arrow("e2", 180, 48, 230, 72, "g"),
      arrow("e3", 120, 96, 120, 118, "g"),
      arrow("e4", 240, 96, 240, 118, "g"),
    ],
    [
      jc(
        "c",
        30,
        44,
        [
          "const li = document.createElement('li');",
          "li.textContent = 'три';",
          "list.append(li);",
        ],
        [2],
        { w: 310, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 2. Типы узлов
export const V02 = scene({
  labels: ["Типы", "children и childNodes", "Живые и статические"],
  caption: [
    "Документ, элементы, текстовые узлы, комментарии и фрагмент документа; nodeType возвращает число-тип",
    "children — только элементы, childNodes — все узлы, включая пробелы между тегами: первый ребёнок часто оказывается текстом",
    "getElementsByClassName возвращает живую коллекцию, querySelectorAll — снимок на момент вызова",
  ],
  frames: [
    [
      ...["document 9", "element 1", "text 3", "comment 8", "fragment 11"].map(
        (n, i) =>
          Box(
            `t${i}`,
            66 + (i % 3) * 114,
            56 + Math.floor(i / 3) * 46,
            100,
            28,
            n,
            "b",
            { size: 9.5, mono: true },
          ),
      ),
    ],
    [
      nd("p", 180, 40, "div", "y"),
      nd("a", 100, 100, "' '", "m"),
      nd("b", 180, 100, "span", "g"),
      nd("c", 260, 100, "' '", "m"),
      arrow("e1", 150, 50, 108, 90, "g"),
      arrow("e2", 180, 52, 180, 90, "g"),
      arrow("e3", 210, 50, 252, 90, "g"),
      Tx("n", 180, 140, "children → [span]   childNodes → 3", { size: 9.5 }),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "const live = div.getElementsByClassName('x');",
          "const snap = div.querySelectorAll('.x');",
          "div.append(newX);",
          "// live.length растёт, snap — нет",
        ],
        [3],
        { w: 330, size: 9, lh: 22 },
      ),
    ],
  ],
});

// 3. Поиск
export const V03 = scene({
  labels: ["getElementById", "querySelector", "matches и closest"],
  caption: [
    "getElementById находит один элемент по идентификатору быстрее всего",
    "querySelector принимает любой CSS-селектор и возвращает первый совпавший, querySelectorAll — все в порядке документа; искать можно внутри элемента",
    "matches проверяет сам элемент, closest поднимается вверх по предкам и возвращает ближайшего — основа делегирования",
  ],
  frames: [
    [
      jc(
        "c",
        40,
        50,
        [
          "const list = document.getElementById('list');",
          "// или: document.querySelector('#list')",
        ],
        [0],
        { w: 290, size: 10, lh: 26 },
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "document.querySelector('ul > li.active');",
          "box.querySelectorAll('[data-id]');",
          "// тег, #id, .класс, [attr], потомок,",
          "// > ребёнок, + сосед",
        ],
        [0, 1],
        { w: 330, size: 10, lh: 22 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "btn.matches('.primary')       // true/false",
          "btn.closest('form')           // ближайший предок",
          "btn.closest('.card')?.remove();",
        ],
        [1],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 4. Содержимое и безопасность
export const V04 = scene({
  labels: ["textContent", "innerHTML и XSS", "Правило"],
  caption: [
    "textContent даёт и принимает обычный текст; присваивание безопасно — угловые скобки станут буквами",
    "innerHTML разбирает строку как разметку: присвоить туда ввод пользователя — прямая дорога к межсайтовому скриптингу",
    "Текст вставляйте через textContent, разметку — только из доверенных источников или через санитайзер; Trusted Types усиливают политику",
  ],
  frames: [
    [
      jc(
        "c",
        30,
        50,
        [
          "el.textContent = '<b>привет</b>';",
          "// на экране: <b>привет</b> — как текст",
        ],
        [0],
        { w: 310, size: 10.5, lh: 26 },
      ),
    ],
    [
      jc(
        "c",
        20,
        44,
        [
          "el.innerHTML = userInput;",
          "// '<img src=x onerror=steal()>'",
          "//  → выполнит код злоумышленника",
        ],
        [0, 2],
        { w: 330, size: 10.5, lh: 24, bad: [0, 2] },
      ),
    ],
    [
      Box("a", 90, 60, 120, 30, "textContent", "g", { size: 10.5 }),
      Box("b", 250, 60, 120, 30, "innerHTML ← доверенное", "y", { size: 9 }),
      Box("c", 170, 116, 200, 28, "санитайзер, CSP, Trusted Types", "b", {
        size: 9.5,
      }),
    ],
  ],
});

// 5. Создание и вставка
export const V05 = scene({
  labels: ["createElement", "Методы вставки", "DocumentFragment"],
  caption: [
    "createElement возвращает пустой элемент, createTextNode — текстовый; cloneNode(true) копирует узел с потомками",
    "append, prepend, before, after, replaceWith, remove принимают несколько узлов и строк; insertAdjacentHTML — четыре позиции рядом с элементом",
    "Много элементов собирают в DocumentFragment и вставляют одним действием: дерево страницы меняется один раз",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "const li = document.createElement('li');",
          "li.className = 'item';",
          "li.append('текст', strongEl);",
        ],
        [0],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      ...["beforebegin", "afterbegin", "beforeend", "afterend"].map((n, i) =>
        Box(
          `p${i}`,
          66 + (i % 2) * 130,
          56 + Math.floor(i / 2) * 44,
          116,
          26,
          n,
          "b",
          { size: 9.5, mono: true },
        ),
      ),
      Tx("n", 180, 140, "el.insertAdjacentHTML(позиция, html)", {
        size: 9,
        mono: true,
      }),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "const frag = document.createDocumentFragment();",
          "for (const x of items) {",
          "  frag.append(row(x));",
          "}",
          "list.append(frag);   // одна вставка",
        ],
        [4],
        { w: 330, size: 9.5, lh: 20 },
      ),
    ],
  ],
});

// 6. Атрибуты и свойства
export const V06 = scene({
  labels: ["Не одно и то же", "Булевы атрибуты", "classList, dataset, style"],
  caption: [
    "Атрибут — то, что написано в разметке, всегда строка; свойство — поле объекта любого типа; value меняется при вводе, атрибут хранит начальное значение",
    'Булев атрибут работает по наличию: даже disabled="false" отключает элемент; управляйте свойством disabled',
    "Классы — через classList (add, remove, toggle), данные — через dataset, стили — style и getComputedStyle для итоговых значений",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "input.getAttribute('value')   // 'начало'",
          "input.value                  // 'что ввёл'",
          "a.getAttribute('href')        // '/x'",
          "a.href                       // 'https://…/x'",
        ],
        [1, 3],
        { w: 330, size: 9.5, lh: 22 },
      ),
    ],
    [
      jc(
        "c",
        20,
        44,
        [
          '<button disabled="false">   // отключена!',
          "",
          "btn.disabled = false;       // включена",
        ],
        [2],
        { w: 320, size: 10, lh: 24, bad: [0] },
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "el.classList.toggle('open');",
          "el.dataset.userId = '7';   // data-user-id",
          "el.style.color = 'red';",
          "getComputedStyle(el).width",
        ],
        [0, 1],
        { w: 330, size: 10, lh: 22 },
      ),
    ],
  ],
});

// 7. Обход дерева
export const V07 = scene({
  labels: ["Рекурсия", "TreeWalker", "contains"],
  caption: [
    "Обход дерева пишут рекурсивно; поиск селектором внутри небольшого контейнера лучше, чем по всему документу",
    "TreeWalker ходит по узлам с фильтром по типам и функцией отбора",
    "contains проверяет, лежит ли узел внутри другого; compareDocumentPosition — взаимное расположение: до, после, предок, потомок",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "function walk(node, visit) {",
          "  visit(node);",
          "  for (const c of node.children) walk(c, visit);",
          "}",
        ],
        [2],
        { w: 330, size: 10, lh: 22 },
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "const w = document.createTreeWalker(",
          "  root, NodeFilter.SHOW_TEXT);",
          "while (w.nextNode()) log(w.currentNode.data);",
        ],
        [2],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "panel.contains(event.target)",
          "a.compareDocumentPosition(b)",
          "// DOCUMENT_POSITION_FOLLOWING = 4",
        ],
        [0, 1],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 8. Веб-компоненты
export const V08 = scene({
  labels: ["Custom Element", "Shadow DOM", "Слоты"],
  caption: [
    "customElements.define регистрирует свой тег (в имени обязательно дефис); connectedCallback, disconnectedCallback, attributeChangedCallback — этапы жизни",
    "Теневой DOM создаёт изолированное поддерево: стили и селекторы снаружи в него не проникают, а изнутри не видят страницу",
    "Слоты определяют, куда в теневом дереве попадут дети элемента — так делают независимые виджеты",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        30,
        [
          "class MyCard extends HTMLElement {",
          "  connectedCallback() { … }",
          "  static observedAttributes = ['title'];",
          "}",
          "customElements.define('my-card', MyCard);",
        ],
        [4],
        { w: 330, size: 9.5, lh: 21 },
      ),
    ],
    [
      Box("h", 90, 76, 100, 40, "<my-card>", "y", { size: 10, mono: true }),
      Box(
        "s",
        270,
        76,
        130,
        56,
        "#shadow-root\n<style>…</style>\n<div>…</div>",
        "g",
        { size: 8.5, mono: true },
      ),
      arrow("e", 140, 76, 202, 76, "g"),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "// в теневом дереве:",
          '<slot name="title"></slot>',
          "// в разметке страницы:",
          '<my-card><h2 slot="title">…</h2></my-card>',
        ],
        [1, 3],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 9. Наблюдатели
export const V09 = scene({
  labels: ["MutationObserver", "IntersectionObserver", "ResizeObserver"],
  caption: [
    "MutationObserver сообщает об изменении узлов, атрибутов и текста; записи доставляются пачкой как микрозадача",
    "IntersectionObserver показывает, насколько элемент виден в окне — для ленивой загрузки картинок и бесконечной ленты",
    "ResizeObserver сообщает об изменении размеров элемента; все три работают асинхронно и не вызывают принудительный пересчёт раскладки",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "new MutationObserver((records) => {",
          "  records.forEach(handle);",
          "}).observe(root, { childList: true, subtree: true });",
        ],
        [2],
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
    [
      Box("w", 180, 76, 200, 100, "", "m", { size: 9 }),
      Tx("t", 180, 36, "окно просмотра", { size: 9, c: "m" }),
      Box("a", 180, 92, 120, 40, "элемент 60%", "g", { size: 10 }),
      Box("b", 180, 150, 120, 22, "ниже — 0%", "r", { size: 9 }),
    ],
    [
      jc(
        "c",
        20,
        44,
        [
          "new ResizeObserver(([e]) => {",
          "  console.log(e.contentRect.width);",
          "}).observe(box);",
        ],
        [1],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 10. Производительность DOM
export const V10 = scene({
  labels: ["Пакеты", "Только видимое", "Virtual DOM"],
  caption: [
    "Не читайте геометрию между записями, собирайте изменения пакетами, используйте фрагменты и классы вместо десятка отдельных стилей",
    "Живые коллекции дороже массивов — превращайте их в массив перед обходом; для длинных списков создавайте только видимую часть",
    "Фреймворки сравнивают описание нового состояния со старым и применяют лишь разницу — мы напишем такой алгоритм в последней части",
  ],
  frames: [
    [
      Box("a", 90, 60, 110, 28, "читать ×N", "g", { size: 10 }),
      Box("b", 250, 60, 110, 28, "писать ×N", "y", { size: 10 }),
      Box("c", 170, 116, 220, 28, "не чередовать чтение и запись", "b", {
        size: 9.5,
      }),
    ],
    [
      ...Array.from({ length: 8 }, (_, i) =>
        Box(
          `r${i}`,
          60 + (i % 4) * 78,
          44 + Math.floor(i / 4) * 40,
          66,
          24,
          i >= 2 && i <= 5 ? "в окне" : "—",
          i >= 2 && i <= 5 ? "g" : "m",
          { size: 9 },
        ),
      ),
      Tx("n", 180, 140, "10 000 строк → создаём ~20", { size: 9.5 }),
    ],
    [
      Box("a", 90, 70, 100, 34, "старое\nописание", "b", { size: 9.5 }),
      Box("b", 270, 70, 100, 34, "новое\nописание", "g", { size: 9.5 }),
      arrow("e", 146, 70, 214, 70, "y"),
      Tx("n", 180, 120, "разница → минимум операций с DOM", { size: 9.5 }),
    ],
  ],
});

// 11. Разбор и сериализация
export const V11 = scene({
  labels: ["Парсер исправляет", "DOMParser", "Range и Selection"],
  caption: [
    "Парсер исправляет ошибки: незакрытые теги, таблицы без тела — в дереве появится <tbody>, которого не было в тексте",
    "DOMParser разбирает строку в отдельный документ; outerHTML — обратная операция, сериализация узла в разметку",
    "Range и Selection указывают позиции внутри текстовых узлов — на них держатся редакторы и копирование",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        44,
        [
          "<table><tr><td>1</td></tr></table>",
          "",
          "// DOM: table > tbody > tr > td",
        ],
        [2],
        { w: 330, size: 10, lh: 26 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "const doc = new DOMParser()",
          "  .parseFromString(html, 'text/html');",
          "doc.body.outerHTML",
        ],
        [1, 2],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "const r = document.createRange();",
          "r.setStart(textNode, 2);",
          "r.setEnd(textNode, 7);",
          "r.toString()   // символы с 2 по 7",
        ],
        [3],
        { w: 330, size: 10, lh: 22 },
      ),
    ],
  ],
});

// 12. Доступность
export const V12 = scene({
  labels: ["Дерево доступности", "Семантика", "Фокус и имя"],
  caption: [
    "Из DOM браузер строит дерево доступности, которое читают программы экранного доступа",
    "Семантические теги — button, ul, h1, form — уже несут роль и поведение; <div onclick> роли не имеет",
    "Собственный «кнопочный» элемент требует role, ARIA, tabindex и управления фокусом; доступное имя берётся из aria-label, подписи или содержимого",
  ],
  frames: [
    [
      Box("d", 90, 70, 100, 34, "DOM", "b", { size: 11 }),
      arrow("e", 146, 70, 214, 70, "g"),
      Box("a", 270, 70, 110, 34, "accessibility\ntree", "y", { size: 9.5 }),
    ],
    [
      jc(
        "c",
        20,
        44,
        [
          "<button>Сохранить</button>   // роль, клавиатура",
          '<div onclick="save()">Сохранить</div>',
        ],
        [0],
        { w: 330, size: 9.5, lh: 30, bad: [1] },
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          '<div role="button" tabindex="0"',
          '     aria-label="Закрыть">',
          "  ✕",
          "</div>",
        ],
        [0, 1],
        { w: 330, size: 10, lh: 22 },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Узлы и поиск", "Содержимое и атрибуты", "Дальше"],
  caption: [
    "Дерево узлов разных типов: children и childNodes различаются; поиск — querySelector, matches, closest",
    "Текст — через textContent, разметка — из доверенных источников; атрибуты — строки, свойства — состояние; пакеты вставок и наблюдатели",
    "Дальше — оформление: каскад, flexbox и grid",
  ],
  frames: [
    [
      Box("a", 90, 60, 120, 30, "children ≠ childNodes", "y", { size: 9 }),
      Box("b", 240, 60, 130, 30, "querySelector", "b", { size: 10 }),
      Box("c", 160, 116, 190, 28, "matches · closest", "g", { size: 10 }),
    ],
    [
      Box("a", 90, 60, 120, 30, "textContent", "g", { size: 10.5 }),
      Box("b", 240, 60, 130, 30, "атрибут ≠ свойство", "y", { size: 9.5 }),
      Box("c", 160, 116, 190, 28, "наблюдатели", "b", { size: 10 }),
    ],
    [
      jc(
        "c",
        40,
        44,
        [".card {", "  display: flex;", "  gap: 1rem;", "}"],
        undefined,
        { w: 240, size: 12, lh: 24 },
      ),
      Tx("n", 180, 140, "глава 15: CSS для программиста", { size: 9.5 }),
    ],
  ],
});
