"""Задачи книги «Современный Frontend»: глава 29."""

TASKS: dict[int, list[dict]] = {29: [{'id': 'j29-h',
  'mode': 'js',
  'title': 'Функция h',
  'statement': 'Напишите h(type, props, ...children) → { type, props, key, children }. props — '
               'null или объект: результат содержит копию свойств без key; key берётся из '
               'props.key (или undefined). Дети нормализуются: вложенные массивы раскрываются '
               'рекурсивно; null, undefined, true, false отбрасываются; строки и числа '
               "превращаются в { type: '#text', text: String(значение) } (0 сохраняется); объекты "
               '(уже готовые vnode) добавляются как есть. Входной props не изменяется.',
  'starter': 'function h(type, props, ...children) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (v) => console.log(JSON.stringify(v));\n'
            'show(h("div", { id: "a", key: "k1" }, "hi", 0, [1, [null, "x"]], false, undefined, '
            'true));\n'
            'show(h("br"));\n'
            'const p = { class: "c", key: 5 };\n'
            'const v = h("p", p, h("b", null, "bold"));\n'
            'show(v); console.log(JSON.stringify(p), v.children[0].type, v.key);\n'
            'show(h("span", null, [[], []], ""));\n',
  'hint': 'Вспомогательная add(c) с рекурсией по массивам; key вынимается из копии свойств.',
  'expected': ['{"type":"div","props":{"id":"a"},"key":"k1","children":[{"type":"#text","text":"hi"},{"type":"#text","text":"0"},{"type":"#text","text":"1"},{"type":"#text","text":"x"}]}',
               '{"type":"br","props":{},"children":[]}',
               '{"type":"p","props":{"class":"c"},"key":5,"children":[{"type":"b","props":{},"children":[{"type":"#text","text":"bold"}]}]}',
               '{"class":"c","key":5} b 5',
               '{"type":"span","props":{},"children":[{"type":"#text","text":""}]}']},
 {'id': 'j29-class-names',
  'mode': 'js',
  'title': 'classNames',
  'statement': 'Напишите classNames(...args): собирает строку классов. Аргументы: строки и числа — '
               'как есть (непустые; 0 пропускается как ложное), массивы — рекурсивно, объекты — '
               'ключи с истинными значениями; null, undefined, false, пустые строки — '
               'пропускаются. Результат — классы через один пробел в порядке появления; дубликаты '
               'не удаляются.',
  'starter': 'function classNames(...args) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(JSON.stringify(classNames("a", "b")));\n'
            'console.log(JSON.stringify(classNames("a", null, false, undefined, "", 0, "b")));\n'
            'console.log(JSON.stringify(classNames(["a", ["b", { c: true, d: false }]], { e: 1, f: '
            '0 }, 5)));\n'
            'console.log(JSON.stringify(classNames()));\n'
            'console.log(JSON.stringify(classNames("a", "a", { a: true })));\n',
  'hint': 'Внутренняя add(a) с разбором по типам.',
  'expected': ['"a b"', '"a b"', '"a b c e 5"', '""', '"a a a"']},
 {'id': 'j29-style-string',
  'mode': 'js',
  'title': 'Объект стиля → строка',
  'statement': 'Напишите styleToString(style): свойства объекта в порядке ключей превращаются в '
               '«имя:значение» через «;» (без пробелов и без завершающего «;»). Имена camelCase → '
               'kebab-case (backgroundColor → background-color). Числа получают «px», кроме нуля и '
               'безразмерных свойств (opacity, zIndex, lineHeight, flex, flexGrow, flexShrink, '
               'order, fontWeight). Значения null, undefined и false пропускаются. Пустой объект — '
               'пустая строка.',
  'starter': 'function styleToString(style) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(styleToString({ fontSize: 12, color: "red", marginTop: 0, opacity: 0.5, '
            'zIndex: 3, lineHeight: 1.5 }));\n'
            'console.log(styleToString({ backgroundColor: "#fff", width: "50%", height: null, '
            'border: false, flexGrow: 2, borderTopWidth: 1 }));\n'
            'console.log(JSON.stringify(styleToString({})));\n'
            'console.log(styleToString({ fontWeight: 700, padding: -4 }));\n',
  'hint': 'Replace по /[A-Z]/ для имён; множество безразмерных свойств.',
  'expected': ['font-size:12px;color:red;margin-top:0;opacity:0.5;z-index:3;line-height:1.5',
               'background-color:#fff;width:50%;flex-grow:2;border-top-width:1px',
               '""',
               'font-weight:700;padding:-4px']},
 {'id': 'j29-render-string',
  'mode': 'js',
  'title': 'Рендер в строку HTML',
  'statement': 'Функция h уже есть. Напишите renderToString(vnode): текст экранируется (& < > → '
               '&amp; &lt; &gt;); элемент — «<тип атрибуты>дети</тип>»; пустые элементы (area, br, '
               'col, hr, img, input, link, meta, source) — «<тип атрибуты>» без закрывающего тега '
               'и без детей. Атрибуты — в порядке свойств: значения экранируются (& < > "), true — '
               'атрибут без значения (только имя), false/null/undefined и свойства-обработчики on* '
               'пропускаются; class — строка или массив строк (через пробел); style — объект: '
               '«имя:значение» через «;» (camelCase → kebab, числа без «px» — для простоты не '
               'добавляйте единицы). Пробел перед атрибутами ставится только если они есть.',
  'starter': '// Готово: создание виртуального узла (не изменяйте)\n'
             'function h(type, props, ...children) {\n'
             '  const flat = [];\n'
             '  const add = (c) => {\n'
             '    if (Array.isArray(c)) c.forEach(add);\n'
             '    else if (c === null || c === undefined || c === true || c === false) return;\n'
             '    else if (typeof c === "object") flat.push(c);\n'
             '    else flat.push({ type: "#text", text: String(c) });\n'
             '  };\n'
             '  children.forEach(add);\n'
             '  const p = { ...(props || {}) };\n'
             '  const key = p.key;\n'
             '  delete p.key;\n'
             '  return { type, props: p, key, children: flat };\n'
             '}\n'
             'function renderToString(vnode) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const r = (v) => console.log(renderToString(v));\n'
            'r(h("p", { id: "x", class: ["a", "b"] }, "a < b & c"));\n'
            'r(h("div", { hidden: true, title: \'say "hi"\', onClick: () => 1, data: null, style: '
            '{ fontSize: 12, backgroundColor: "red" } }, h("br"), h("img", { src: "a.png", alt: '
            '"x" }), "tail"));\n'
            'r(h("ul", null, h("li", null, 1), h("li", null, 0)));\n'
            'r(h("input", { type: "text", disabled: false, value: "<v>" }));\n'
            'r(h("span", null));\n',
  'hint': 'Рекурсия: текст → escape, элемент → собрать attrs и children.',
  'expected': ['<p id="x" class="a b">a &lt; b &amp; c</p>',
               '<div hidden title="say &quot;hi&quot;" '
               'style="font-size:12;background-color:red"><br><img src="a.png" alt="x">tail</div>',
               '<ul><li>1</li><li>0</li></ul>',
               '<input type="text" value="&lt;v&gt;">',
               '<span></span>']},
 {'id': 'j29-parse-html',
  'mode': 'js',
  'title': 'Разбор HTML в vnode',
  'statement': 'Функция h уже есть. Напишите parseHtml(html) → массив vnode верхнего уровня '
               '(созданных через h). Поддерживается: теги с атрибутами (значения в двойных или '
               'одинарных кавычках, без кавычек — до пробела или «>», булев атрибут — true), '
               'пустые элементы (area, br, col, hr, img, input, link, meta, source), «<тег/>» — '
               'самозакрывающийся, текст, сущности &amp; &lt; &gt; &quot; в тексте и значениях. '
               'Текстовые узлы, состоящие только из пробельных символов, отбрасываются; у '
               'остальных пробелы по краям сохраняются как есть. Закрывающий тег должен совпадать '
               "с открытым — иначе Error('Mismatched closing tag </x>'). Незакрытый тег в конце — "
               "Error('Unclosed tag <x>').",
  'starter': '// Готово: создание виртуального узла (не изменяйте)\n'
             'function h(type, props, ...children) {\n'
             '  const flat = [];\n'
             '  const add = (c) => {\n'
             '    if (Array.isArray(c)) c.forEach(add);\n'
             '    else if (c === null || c === undefined || c === true || c === false) return;\n'
             '    else if (typeof c === "object") flat.push(c);\n'
             '    else flat.push({ type: "#text", text: String(c) });\n'
             '  };\n'
             '  children.forEach(add);\n'
             '  const p = { ...(props || {}) };\n'
             '  const key = p.key;\n'
             '  delete p.key;\n'
             '  return { type, props: p, key, children: flat };\n'
             '}\n'
             'function parseHtml(html) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (s) => { try { console.log(JSON.stringify(parseHtml(s))); } catch (e) { '
            'console.log("!" + e.message); } };\n'
            'show(\'<div id="a" class=\\\'b c\\\'><p>Hello &amp; <b>bold</b></p><br><img src=x.png '
            "alt></div>');\n"
            'show("<ul>\\n  <li>one</li>\\n  <li>two</li>\\n</ul>");\n'
            'show("text <i>it</i> tail");\n'
            'show("<input disabled/><span/>");\n'
            'show("<div></span>");\n'
            'show("<div><p>open</div>");\n'
            'show("<div>");\n'
            'show("");\n',
  'hint': 'Токенизация регулярным выражением: <!?/?имя ...>|текст; стек открытых элементов.',
  'expected': ['[{"type":"div","props":{"id":"a","class":"b '
               'c"},"children":[{"type":"p","props":{},"children":[{"type":"#text","text":"Hello & '
               '"},{"type":"b","props":{},"children":[{"type":"#text","text":"bold"}]}]},{"type":"br","props":{},"children":[]},{"type":"img","props":{"src":"x.png","alt":true},"children":[]}]}]',
               '[{"type":"ul","props":{},"children":[{"type":"li","props":{},"children":[{"type":"#text","text":"one"}]},{"type":"li","props":{},"children":[{"type":"#text","text":"two"}]}]}]',
               '[{"type":"#text","text":"text '
               '"},{"type":"i","props":{},"children":[{"type":"#text","text":"it"}]},{"type":"#text","text":" '
               'tail"}]',
               '[{"type":"input","props":{"disabled":true},"children":[]},{"type":"span","props":{},"children":[]}]',
               '!Mismatched closing tag </span>',
               '!Mismatched closing tag </div>',
               '!Unclosed tag <div>',
               '[]']},
 {'id': 'j29-interpolate',
  'mode': 'js',
  'title': 'Шаблон с {{ }} и фильтрами',
  'statement': "Напишите interpolate(template, data). Выражение «{{ путь | фильтр | фильтр:'арг' "
               '}}» заменяется значением: путь — ключи через точку (индексы массивов — числами: '
               'items.0.name); нет значения — пустая строка. Фильтры слева направо: upper, lower, '
               "trim, default:'текст' (если значение undefined, null или '' — подставить текст), "
               'raw (отключает экранирование). Остальное значение приводится String(). После '
               'фильтров результат экранируется (& < > " → сущности), если не было raw. Пробелы '
               "внутри скобок и вокруг «|» игнорируются. Неизвестный фильтр — Error('Unknown "
               "filter: имя').",
  'starter': 'function interpolate(template, data) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const data = { user: { name: "Ann", bio: "" }, items: [{ n: "<b>x</b>" }, { n: "y" '
            '}], n: 0, empty: null, html: "<i>ok</i>" };\n'
            'const t = (s) => { try { console.log(JSON.stringify(interpolate(s, data))); } catch '
            '(e) { console.log("!" + e.message); } };\n'
            't("Hello, {{ user.name }}!");\n'
            't("{{ user.name | upper }} {{user.name|lower}}");\n'
            't("[{{ user.bio | default:\'n/a\' }}] [{{ empty | default:\'none\' }}] [{{ missing '
            '}}] [{{ n }}]");\n'
            't("{{ items.0.n }} / {{ items.1.n | upper }}");\n'
            't("{{ html }} vs {{ html | raw }}");\n'
            't("{{ user.name | trim | upper | default:\'x\' }}");\n'
            't("{{ user.name | reverse }}");\n'
            't("no placeholders");\n',
  'hint': "replace(/\\{\\{(.*?)\\}\\}/g, …); путь разбирайте по точкам; фильтры — split('|').",
  'expected': ['"Hello, Ann!"',
               '"ANN ann"',
               '"[n/a] [none] [] [0]"',
               '"&lt;b&gt;x&lt;/b&gt; / Y"',
               '"&lt;i&gt;ok&lt;/i&gt; vs <i>ok</i>"',
               '"ANN"',
               '!Unknown filter: reverse',
               '"no placeholders"']},
 {'id': 'j29-create-dom',
  'mode': 'js',
  'title': 'Из vnode в узлы DOM',
  'statement': 'Модель DOM (MiniNode, doc, dump), функция h, classNames и styleToString уже есть. '
               'Напишите createDom(vnode, doc) → MiniNode. Текст — doc.createText(text). Элемент — '
               'doc.createElement(type): свойства в порядке ключей: null, undefined, false '
               'пропускаются; on* (onClick…) — el.addListener(имя события строчными без «on», '
               "функция); class — setAttr('class', classNames(значение)); style-объект — "
               "setAttr('style', styleToString(...)); true — setAttr(имя, ''); прочее — "
               'setAttr(имя, значение). Затем дети создаются рекурсивно и добавляются через '
               'append.',
  'starter': '// Готово: модель DOM для упражнений (не изменяйте)\n'
             'class MiniNode {\n'
             '  constructor(tag, text = null) { this.tag = tag; this.text = text; this.attrs = {}; '
             'this.children = []; this.listeners = {}; this.parent = null; }\n'
             '  append(c) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.push(c); return c; }\n'
             '  insertAt(c, i) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.splice(i, 0, c); return c; }\n'
             '  remove(c) { const i = this.children.indexOf(c); if (i >= 0) { '
             'this.children.splice(i, 1); c.parent = null; } return c; }\n'
             '  replaceChild(n, o) { const i = this.children.indexOf(o); this.children[i] = n; '
             'n.parent = this; o.parent = null; return o; }\n'
             '  setAttr(k, v) { this.attrs[k] = String(v); }\n'
             '  removeAttr(k) { delete this.attrs[k]; }\n'
             '  addListener(ev, fn) { (this.listeners[ev] ||= []).push(fn); }\n'
             '  removeListener(ev, fn) { const a = this.listeners[ev] || []; const i = '
             'a.indexOf(fn); if (i >= 0) a.splice(i, 1); }\n'
             '}\n'
             'const doc = { createElement: (tag) => new MiniNode(tag), createText: (t) => new '
             'MiniNode("#text", t) };\n'
             'function dump(n) {\n'
             '  if (n.tag === "#text") return JSON.stringify(n.text);\n'
             '  const attrs = Object.keys(n.attrs).sort().map((k) => ` '
             '${k}=${n.attrs[k]}`).join("");\n'
             '  const ev = Object.keys(n.listeners).filter((k) => '
             'n.listeners[k].length).sort().map((k) => ` @${k}`).join("");\n'
             '  return n.tag + attrs + ev + (n.children.length ? "(" + n.children.map(dump).join(" '
             '") + ")" : "");\n'
             '}\n'
             '// Готово: создание виртуального узла (не изменяйте)\n'
             'function h(type, props, ...children) {\n'
             '  const flat = [];\n'
             '  const add = (c) => {\n'
             '    if (Array.isArray(c)) c.forEach(add);\n'
             '    else if (c === null || c === undefined || c === true || c === false) return;\n'
             '    else if (typeof c === "object") flat.push(c);\n'
             '    else flat.push({ type: "#text", text: String(c) });\n'
             '  };\n'
             '  children.forEach(add);\n'
             '  const p = { ...(props || {}) };\n'
             '  const key = p.key;\n'
             '  delete p.key;\n'
             '  return { type, props: p, key, children: flat };\n'
             '}\n'
             'function classNames(...args) {\n'
             '  const out = [];\n'
             '  const add = (a) => {\n'
             '    if (!a) return;\n'
             '    if (typeof a === "string" || typeof a === "number") out.push(String(a));\n'
             '    else if (Array.isArray(a)) a.forEach(add);\n'
             '    else if (typeof a === "object") for (const k of Object.keys(a)) if (a[k]) '
             'out.push(k);\n'
             '  };\n'
             '  args.forEach(add);\n'
             '  return out.join(" ");\n'
             '}\n'
             'const UNITLESS = new Set(["opacity", "zIndex", "lineHeight", "flex", "flexGrow", '
             '"flexShrink", "order", "fontWeight"]);\n'
             'function styleToString(style) {\n'
             '  return Object.keys(style)\n'
             '    .filter((k) => style[k] !== null && style[k] !== undefined && style[k] !== '
             'false)\n'
             '    .map((k) => {\n'
             '      const prop = k.replace(/[A-Z]/g, (c) => "-" + c.toLowerCase());\n'
             '      const v = style[k];\n'
             '      return `${prop}:${typeof v === "number" && v !== 0 && !UNITLESS.has(k) ? v + '
             '"px" : v}`;\n'
             '    })\n'
             '    .join(";");\n'
             '}\n'
             'function createDom(vnode, doc) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const tree = h("div", { id: "app", class: ["box", { hot: true }], style: { fontSize: '
            '14, color: "red" }, hidden: true, title: null, onClick: () => 1 },\n'
            '  h("h1", null, "Title"), h("ul", null, h("li", { key: "a" }, 1), h("li", null, '
            '"two")), "tail");\n'
            'const dom = createDom(tree, doc);\n'
            'console.log(dump(dom));\n'
            'console.log(dom.children.length, dom.children[1].children[0].parent === '
            'dom.children[1], dom.listeners.click.length);\n'
            'console.log(dump(createDom(h("br"), doc)), dump(createDom({ type: "#text", text: "hi" '
            '}, doc)));\n',
  'hint': 'Разберите свойства по правилам и рекурсивно добавьте детей.',
  'expected': ['div class=box hot hidden= id=app style=font-size:14px;color:red @click(h1("Title") '
               'ul(li("1") li("two")) "tail")',
               '3 true 1',
               'br "hi"']},
 {'id': 'j29-diff-props',
  'mode': 'js',
  'title': 'Разница свойств',
  'statement': 'Напишите diffProps(oldProps, newProps) → массив операций. Сначала операции '
               "удаления { op: 'remove', name } для ключей, которых нет в новых свойствах (по "
               "алфавиту), затем { op: 'set', name, value } для новых ключей и ключей с "
               'изменившимся значением (Object.is) — тоже по алфавиту. Значение функции '
               'сравнивается по ссылке. Одинаковые значения операций не порождают.',
  'starter': 'function diffProps(oldProps, newProps) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const f = () => 1, g = () => 1;\n'
            'const show = (a, b) => console.log(JSON.stringify(diffProps(a, b).map((o) => o.op + '
            '":" + o.name + (o.op === "set" ? "=" + (typeof o.value === "function" ? "fn" : '
            'o.value) : ""))));\n'
            'show({ id: "a", title: "t" }, { id: "b" });\n'
            'show({}, { z: 1, a: 2 });\n'
            'show({ x: 1, y: 2 }, { x: 1, y: 2 });\n'
            'show({ onClick: f }, { onClick: f });\n'
            'show({ onClick: f }, { onClick: g });\n'
            'show({ a: 1, b: 2, c: 3 }, { b: 5, d: 4 });\n'
            'show({ n: NaN }, { n: NaN });\n',
  'hint': 'Два прохода по отсортированным ключам.',
  'expected': ['["remove:title","set:id=b"]',
               '["set:a=2","set:z=1"]',
               '[]',
               '[]',
               '["set:onClick=fn"]',
               '["remove:a","remove:c","set:b=5","set:d=4"]',
               '[]']},
 {'id': 'j29-diff',
  'mode': 'js',
  'title': 'Сравнение деревьев',
  'statement': 'Функция diffProps уже есть (операции remove/set). Напишите diff(oldV, newV) → патч '
               'или null (нет изменений). Правила: нет старого (null/undefined) — { type: '
               "'CREATE', node: new } (если и нового нет — null); нет нового — { type: 'REMOVE' }; "
               "тип или ключ различаются — { type: 'REPLACE', node: new }; оба текстовые: если "
               "текст отличается — { type: 'TEXT', text }, иначе null; иначе (тот же тип и ключ): "
               'props = diffProps(old.props, new.props), children — массив патчей по индексам '
               '(длина — максимум из длин; null для неизменных). Если props пуст и все children — '
               "null, результат null; иначе { type: 'UPDATE', props, children }.",
  'starter': 'function diffProps(oldProps, newProps) {\n'
             '  const ops = [];\n'
             '  for (const name of Object.keys(oldProps).sort()) if (!(name in newProps)) '
             'ops.push({ op: "remove", name });\n'
             '  for (const name of Object.keys(newProps).sort()) if (!(name in oldProps) || '
             '!Object.is(oldProps[name], newProps[name])) ops.push({ op: "set", name, value: '
             'newProps[name] });\n'
             '  return ops;\n'
             '}\n'
             'function diff(oldV, newV) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            'function h(type, props, ...children) {\n'
            '  const flat = [];\n'
            '  const add = (c) => {\n'
            '    if (Array.isArray(c)) c.forEach(add);\n'
            '    else if (c === null || c === undefined || c === true || c === false) return;\n'
            '    else if (typeof c === "object") flat.push(c);\n'
            '    else flat.push({ type: "#text", text: String(c) });\n'
            '  };\n'
            '  children.forEach(add);\n'
            '  const p = { ...(props || {}) };\n'
            '  const key = p.key;\n'
            '  delete p.key;\n'
            '  return { type, props: p, key, children: flat };\n'
            '}\n'
            '\n'
            'const show = (a, b) => console.log(JSON.stringify(diff(a, b), (k, v) => (typeof v === '
            '"function" ? "fn" : v)));\n'
            'show(null, h("p", null, "x")); show(h("p"), null); show(null, null);\n'
            'show(h("div", null, "a"), h("span", null, "a"));\n'
            'show(h("li", { key: 1 }), h("li", { key: 2 }));\n'
            'show({ type: "#text", text: "a" }, { type: "#text", text: "a" });\n'
            'show({ type: "#text", text: "a" }, { type: "#text", text: "b" });\n'
            'show(h("p", { class: "x" }, "t"), h("p", { class: "x" }, "t"));\n'
            'show(h("p", { class: "x" }, "t"), h("p", { class: "y", id: "i" }, "t"));\n'
            'show(h("ul", null, h("li", null, "a"), h("li", null, "b")), h("ul", null, h("li", '
            'null, "a"), h("li", null, "c"), h("li", null, "d")));\n'
            'show(h("ul", null, h("li", null, "a"), h("li", null, "b")), h("ul", null, h("li", '
            'null, "a")));\n',
  'hint': 'Рекурсивно сравнивайте детей по индексу; сначала проверки CREATE/REMOVE/REPLACE.',
  'expected': ['{"type":"CREATE","node":{"type":"p","props":{},"children":[{"type":"#text","text":"x"}]}}',
               '{"type":"REMOVE"}',
               'null',
               '{"type":"REPLACE","node":{"type":"span","props":{},"children":[{"type":"#text","text":"a"}]}}',
               '{"type":"REPLACE","node":{"type":"li","props":{},"key":2,"children":[]}}',
               'null',
               '{"type":"TEXT","text":"b"}',
               'null',
               '{"type":"UPDATE","props":[{"op":"set","name":"class","value":"y"},{"op":"set","name":"id","value":"i"}],"children":[null]}',
               '{"type":"UPDATE","props":[],"children":[null,{"type":"UPDATE","props":[],"children":[{"type":"TEXT","text":"c"}]},{"type":"CREATE","node":{"type":"li","props":{},"children":[{"type":"#text","text":"d"}]}}]}',
               '{"type":"UPDATE","props":[],"children":[null,{"type":"REMOVE"}]}']},
 {'id': 'j29-apply-patch',
  'mode': 'js',
  'title': 'Применение патчей к DOM',
  'statement': 'Модель DOM (MiniNode, doc, dump), h, createDom и diff уже есть в заготовке. '
               'Напишите applyPatch(parent, index, patch, doc): применяет патч (формат diff) к '
               'узлу parent.children[index]. CREATE — вставить createDom(node) в позицию index '
               '(insertAt); REMOVE — удалить parent.children[index]; REPLACE — заменить на '
               'createDom(node) (replaceChild); TEXT — заменить поле text узла; UPDATE — применить '
               'props к узлу (set: on* — отписать старую функцию (если была в свойствах нельзя '
               'узнать — храните в node.__props) и подписать новую; class/style как в createDom; '
               "true → ''; false/null/undefined — убрать атрибут; remove — убрать атрибут и "
               'обработчик) и затем применить патчи детей: сначала все не-REMOVE по возрастанию '
               'индекса, затем REMOVE по убыванию индекса. null-патчи пропускаются. Для старых '
               'свойств используйте node.__props — createDom в заготовке его заполняет.',
  'starter': '// Готово: модель DOM для упражнений (не изменяйте)\n'
             'class MiniNode {\n'
             '  constructor(tag, text = null) { this.tag = tag; this.text = text; this.attrs = {}; '
             'this.children = []; this.listeners = {}; this.parent = null; }\n'
             '  append(c) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.push(c); return c; }\n'
             '  insertAt(c, i) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.splice(i, 0, c); return c; }\n'
             '  remove(c) { const i = this.children.indexOf(c); if (i >= 0) { '
             'this.children.splice(i, 1); c.parent = null; } return c; }\n'
             '  replaceChild(n, o) { const i = this.children.indexOf(o); this.children[i] = n; '
             'n.parent = this; o.parent = null; return o; }\n'
             '  setAttr(k, v) { this.attrs[k] = String(v); }\n'
             '  removeAttr(k) { delete this.attrs[k]; }\n'
             '  addListener(ev, fn) { (this.listeners[ev] ||= []).push(fn); }\n'
             '  removeListener(ev, fn) { const a = this.listeners[ev] || []; const i = '
             'a.indexOf(fn); if (i >= 0) a.splice(i, 1); }\n'
             '}\n'
             'const doc = { createElement: (tag) => new MiniNode(tag), createText: (t) => new '
             'MiniNode("#text", t) };\n'
             'function dump(n) {\n'
             '  if (n.tag === "#text") return JSON.stringify(n.text);\n'
             '  const attrs = Object.keys(n.attrs).sort().map((k) => ` '
             '${k}=${n.attrs[k]}`).join("");\n'
             '  const ev = Object.keys(n.listeners).filter((k) => '
             'n.listeners[k].length).sort().map((k) => ` @${k}`).join("");\n'
             '  return n.tag + attrs + ev + (n.children.length ? "(" + n.children.map(dump).join(" '
             '") + ")" : "");\n'
             '}\n'
             '// Готово: создание виртуального узла (не изменяйте)\n'
             'function h(type, props, ...children) {\n'
             '  const flat = [];\n'
             '  const add = (c) => {\n'
             '    if (Array.isArray(c)) c.forEach(add);\n'
             '    else if (c === null || c === undefined || c === true || c === false) return;\n'
             '    else if (typeof c === "object") flat.push(c);\n'
             '    else flat.push({ type: "#text", text: String(c) });\n'
             '  };\n'
             '  children.forEach(add);\n'
             '  const p = { ...(props || {}) };\n'
             '  const key = p.key;\n'
             '  delete p.key;\n'
             '  return { type, props: p, key, children: flat };\n'
             '}\n'
             'function classNames(...args) {\n'
             '  const out = [];\n'
             '  const add = (a) => {\n'
             '    if (!a) return;\n'
             '    if (typeof a === "string" || typeof a === "number") out.push(String(a));\n'
             '    else if (Array.isArray(a)) a.forEach(add);\n'
             '    else if (typeof a === "object") for (const k of Object.keys(a)) if (a[k]) '
             'out.push(k);\n'
             '  };\n'
             '  args.forEach(add);\n'
             '  return out.join(" ");\n'
             '}\n'
             'const UNITLESS = new Set(["opacity", "zIndex", "lineHeight", "flex", "flexGrow", '
             '"flexShrink", "order", "fontWeight"]);\n'
             'function styleToString(style) {\n'
             '  return Object.keys(style)\n'
             '    .filter((k) => style[k] !== null && style[k] !== undefined && style[k] !== '
             'false)\n'
             '    .map((k) => {\n'
             '      const prop = k.replace(/[A-Z]/g, (c) => "-" + c.toLowerCase());\n'
             '      const v = style[k];\n'
             '      return `${prop}:${typeof v === "number" && v !== 0 && !UNITLESS.has(k) ? v + '
             '"px" : v}`;\n'
             '    })\n'
             '    .join(";");\n'
             '}\n'
             'function createDom(vnode, doc) {\n'
             '  if (vnode.type === "#text") return doc.createText(vnode.text);\n'
             '  const el = doc.createElement(vnode.type);\n'
             '  el.__props = { ...vnode.props };\n'
             '  for (const [name, value] of Object.entries(vnode.props)) {\n'
             '    if (value === null || value === undefined || value === false) continue;\n'
             '    if (/^on[A-Z]/.test(name)) el.addListener(name.slice(2).toLowerCase(), value);\n'
             '    else if (name === "class") el.setAttr("class", classNames(value));\n'
             '    else if (name === "style" && typeof value === "object") el.setAttr("style", '
             'styleToString(value));\n'
             '    else el.setAttr(name, value === true ? "" : value);\n'
             '  }\n'
             '  for (const c of vnode.children) el.append(createDom(c, doc));\n'
             '  return el;\n'
             '}\n'
             'function diffProps(oldProps, newProps) {\n'
             '  const ops = [];\n'
             '  for (const name of Object.keys(oldProps).sort()) if (!(name in newProps)) '
             'ops.push({ op: "remove", name });\n'
             '  for (const name of Object.keys(newProps).sort()) if (!(name in oldProps) || '
             '!Object.is(oldProps[name], newProps[name])) ops.push({ op: "set", name, value: '
             'newProps[name] });\n'
             '  return ops;\n'
             '}\n'
             'function diff(oldV, newV) {\n'
             '  if (oldV === null || oldV === undefined) return newV === null || newV === '
             'undefined ? null : { type: "CREATE", node: newV };\n'
             '  if (newV === null || newV === undefined) return { type: "REMOVE" };\n'
             '  if (oldV.type !== newV.type || oldV.key !== newV.key) return { type: "REPLACE", '
             'node: newV };\n'
             '  if (oldV.type === "#text") return oldV.text === newV.text ? null : { type: "TEXT", '
             'text: newV.text };\n'
             '  const props = diffProps(oldV.props, newV.props);\n'
             '  const n = Math.max(oldV.children.length, newV.children.length);\n'
             '  const children = [];\n'
             '  for (let i = 0; i < n; i++) children.push(diff(oldV.children[i], '
             'newV.children[i]));\n'
             '  if (!props.length && children.every((c) => c === null)) return null;\n'
             '  return { type: "UPDATE", props, children };\n'
             '}\n'
             'function applyPatch(parent, index, patch, doc) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const apply = (rootV1, rootV2) => {\n'
            '  const host = doc.createElement("host");\n'
            '  host.append(createDom(rootV1, doc));\n'
            '  const before = host.children[0];\n'
            '  const patch = diff(rootV1, rootV2);\n'
            '  if (patch) applyPatch(host, 0, patch, doc);\n'
            '  console.log(dump(host.children[0]), host.children[0] === before);\n'
            '  return host;\n'
            '};\n'
            'const f = () => 1;\n'
            'apply(h("ul", { class: "a" }, h("li", null, "a"), h("li", null, "b"), h("li", null, '
            '"c")), h("ul", { class: ["b"], id: "x" }, h("li", null, "A"), h("li", null, "c")));\n'
            'apply(h("p", { onClick: f }, "x"), h("p", {}, "x"));\n'
            'apply(h("div", null, h("span", null, "1")), h("div", null, h("b", null, "1"), "tail", '
            'h("i")));\n'
            'apply(h("a", { href: "/" }, "x"), h("a", { href: "/", hidden: true, style: { color: '
            '"red" } }, "x"));\n'
            'apply(h("div", null, "a", "b", "c", "d"), h("div", null, "a"));\n'
            'apply(h("p", null, "same"), h("p", null, "same"));\n'
            'apply(h("p"), h("section"));\n'
            'const host = doc.createElement("host");\n'
            'applyPatch(host, 0, { type: "CREATE", node: h("p", { id: "n" }, "new") }, doc);\n'
            'console.log(dump(host));\n'
            'applyPatch(host, 0, { type: "REMOVE" }, doc);\n'
            'console.log(host.children.length);\n',
  'hint': 'Для UPDATE: получите node = parent.children[index]; обработайте props; потом children в '
          'нужном порядке рекурсивно (родитель — node).',
  'expected': ['ul class=b id=x(li("A") li("c")) true',
               'p("x") true',
               'div(b("1") "tail" i) true',
               'a hidden= href=/ style=color:red("x") true',
               'div("a") true',
               'p("same") true',
               'section false',
               'host(p id=n("new"))',
               '0']},
 {'id': 'j29-keyed-reconcile',
  'mode': 'js',
  'title': 'Сопоставление списков по ключам',
  'statement': 'Напишите reconcileKeys(oldKeys, newKeys) → { removed, created, moves }. removed — '
               'ключи, которых нет в новом списке (в порядке старого списка); created — новые '
               'ключи, которых не было (в порядке нового списка); moves — перемещаемые элементы по '
               'алгоритму «индекс последнего размещённого» (как в React): идём по новому списку; '
               'для ключа, который был в старом, берём его индекс в старом списке oldIndex; если '
               'oldIndex < lastPlaced — элемент нужно переместить: добавляем { key, to: индекс в '
               'новом списке }; иначе lastPlaced = oldIndex. Новые ключи на lastPlaced не влияют. '
               'Ключи уникальны.',
  'starter': 'function reconcileKeys(oldKeys, newKeys) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (a, b) => console.log(a.join("") + " → " + b.join(""), '
            'JSON.stringify(reconcileKeys(a, b)));\n'
            'show(["a", "b", "c"], ["a", "b", "c"]);\n'
            'show(["a", "b", "c"], ["x", "a", "b", "c"]);\n'
            'show(["a", "b", "c", "d"], ["c", "a", "b", "d"]);\n'
            'show(["a", "b", "c", "d"], ["d", "c", "b", "a"]);\n'
            'show(["a", "b", "c"], ["b"]);\n'
            'show(["a", "b"], ["y", "x"]);\n'
            'show([], ["a"]);\n'
            'show(["a", "b", "c", "d", "e"], ["b", "e", "x", "a", "d"]);\n',
  'hint': 'Map ключ → старый индекс; один проход по newKeys.',
  'expected': ['abc → abc {"removed":[],"created":[],"moves":[]}',
               'abc → xabc {"removed":[],"created":["x"],"moves":[]}',
               'abcd → cabd '
               '{"removed":[],"created":[],"moves":[{"key":"a","to":1},{"key":"b","to":2}]}',
               'abcd → dcba '
               '{"removed":[],"created":[],"moves":[{"key":"c","to":1},{"key":"b","to":2},{"key":"a","to":3}]}',
               'abc → b {"removed":["a","c"],"created":[],"moves":[]}',
               'ab → yx {"removed":["a","b"],"created":["y","x"],"moves":[]}',
               ' → a {"removed":[],"created":["a"],"moves":[]}',
               'abcde → bexad '
               '{"removed":["c"],"created":["x"],"moves":[{"key":"a","to":3},{"key":"d","to":4}]}']},
 {'id': 'j29-lis',
  'mode': 'js',
  'title': 'Наибольшая возрастающая подпоследовательность',
  'statement': 'Напишите lis(arr): возвращает массив индексов (по возрастанию) самой длинной '
               'строго возрастающей подпоследовательности массива чисел. Если таких несколько — '
               'та, чья последовательность индексов лексикографически наименьшая (то есть сначала '
               'берите самый ранний возможный первый индекс, затем самый ранний возможный второй и '
               'т. д.). Пустой массив — [].',
  'starter': 'function lis(arr) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (a) => console.log(JSON.stringify(a), JSON.stringify(lis(a)));\n'
            't([]); t([5]); t([1, 2, 3]); t([3, 2, 1]); t([10, 9, 2, 5, 3, 7, 101, 18]); t([0, 8, '
            '4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]);\n'
            't([2, 2, 2]); t([1, 3, 2, 3]); t([4, 5, 1, 2, 3]); t([1, 2, 1, 2]);\n',
  'hint': 'f[i] — длина LIS, начинающейся в i (с конца); затем жадно выбирайте самые ранние '
          'индексы с нужной f.',
  'expected': ['[] []',
               '[5] [0]',
               '[1,2,3] [0,1,2]',
               '[3,2,1] [0]',
               '[10,9,2,5,3,7,101,18] [2,3,5,6]',
               '[0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15] [0,2,6,9,11,15]',
               '[2,2,2] [0]',
               '[1,3,2,3] [0,2,3]',
               '[4,5,1,2,3] [2,3,4]',
               '[1,2,1,2] [0,1]']},
 {'id': 'j29-min-moves',
  'mode': 'js',
  'title': 'Минимум перемещений',
  'statement': 'Функция lis(arr) (индексы самой длинной строго возрастающей подпоследовательности, '
               'при равных — лексикографически наименьшие индексы) уже есть. Напишите '
               'minMoves(oldKeys, newKeys) → массив ключей, которые нужно переместить, в порядке '
               'нового списка. Рассматриваются только ключи, присутствующие в обоих списках: '
               'возьмите их в порядке нового списка, превратите в старые индексы, найдите LIS по '
               'этим индексам — соответствующие ключи остаются на месте, все прочие ключи (из '
               'общих) нужно переместить. Ключи только в одном из списков не учитываются.',
  'starter': 'function lis(arr) {\n'
             '  const n = arr.length;\n'
             '  const f = new Array(n).fill(1);\n'
             '  for (let i = n - 1; i >= 0; i--) for (let j = i + 1; j < n; j++) if (arr[j] > '
             'arr[i]) f[i] = Math.max(f[i], f[j] + 1);\n'
             '  const best = Math.max(0, ...f);\n'
             '  const out = [];\n'
             '  let need = best, last = -1;\n'
             '  for (let i = 0; i < n && need > 0; i++) {\n'
             '    if (f[i] === need && (last < 0 || arr[i] > arr[last]) && i > last) { '
             'out.push(i); last = i; need--; }\n'
             '  }\n'
             '  return out;\n'
             '}\n'
             'function minMoves(oldKeys, newKeys) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (a, b) => console.log(a.join("") + " → " + b.join(""), '
            'JSON.stringify(minMoves(a, b)));\n'
            't(["a", "b", "c", "d"], ["c", "a", "b", "d"]);\n'
            't(["a", "b", "c", "d"], ["d", "c", "b", "a"]);\n'
            't(["a", "b", "c"], ["a", "b", "c"]);\n'
            't(["a", "b", "c"], ["x", "c", "y", "a"]);\n'
            't(["a", "b", "c", "d", "e"], ["b", "e", "x", "a", "d"]);\n'
            't([], ["a"]); t(["a"], []);\n'
            't(["a", "b", "c", "d", "e", "f"], ["f", "a", "b", "c", "d", "e"]);\n',
  'hint': 'common = newKeys.filter(в старом); idx = common.map(k => oldKeys.indexOf(k)); stay = '
          'lis(idx).',
  'expected': ['abcd → cabd ["c"]',
               'abcd → dcba ["c","b","a"]',
               'abc → abc []',
               'abc → xcya ["a"]',
               'abcde → bexad ["a","d"]',
               ' → a []',
               'a →  []',
               'abcdef → fabcde ["f"]']},
 {'id': 'j29-events-sync',
  'mode': 'js',
  'title': 'Синхронизация обработчиков',
  'statement': 'Модель DOM (MiniNode с addListener/removeListener) есть в заготовке. Напишите '
               'syncEvents(node, oldProps, newProps): для каждого свойства-обработчика (имя вида '
               'onЗаглавная…: onClick, onInput) приведите слушатели узла в соответствие. Имя '
               'события — часть после «on» строчными (onClick → click). Если функция изменилась '
               '(по ссылке): старую (если была) отписать, новую (если есть функция) подписать. '
               'Свойство удалено — отписать. Свойства, не являющиеся обработчиками, игнорируются. '
               'Функция не должна вызываться для обработчиков, которые не изменились (число '
               'слушателей не растёт).',
  'starter': '// Готово: модель DOM для упражнений (не изменяйте)\n'
             'class MiniNode {\n'
             '  constructor(tag, text = null) { this.tag = tag; this.text = text; this.attrs = {}; '
             'this.children = []; this.listeners = {}; this.parent = null; }\n'
             '  append(c) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.push(c); return c; }\n'
             '  insertAt(c, i) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.splice(i, 0, c); return c; }\n'
             '  remove(c) { const i = this.children.indexOf(c); if (i >= 0) { '
             'this.children.splice(i, 1); c.parent = null; } return c; }\n'
             '  replaceChild(n, o) { const i = this.children.indexOf(o); this.children[i] = n; '
             'n.parent = this; o.parent = null; return o; }\n'
             '  setAttr(k, v) { this.attrs[k] = String(v); }\n'
             '  removeAttr(k) { delete this.attrs[k]; }\n'
             '  addListener(ev, fn) { (this.listeners[ev] ||= []).push(fn); }\n'
             '  removeListener(ev, fn) { const a = this.listeners[ev] || []; const i = '
             'a.indexOf(fn); if (i >= 0) a.splice(i, 1); }\n'
             '}\n'
             'const doc = { createElement: (tag) => new MiniNode(tag), createText: (t) => new '
             'MiniNode("#text", t) };\n'
             'function dump(n) {\n'
             '  if (n.tag === "#text") return JSON.stringify(n.text);\n'
             '  const attrs = Object.keys(n.attrs).sort().map((k) => ` '
             '${k}=${n.attrs[k]}`).join("");\n'
             '  const ev = Object.keys(n.listeners).filter((k) => '
             'n.listeners[k].length).sort().map((k) => ` @${k}`).join("");\n'
             '  return n.tag + attrs + ev + (n.children.length ? "(" + n.children.map(dump).join(" '
             '") + ")" : "");\n'
             '}\n'
             'function syncEvents(node, oldProps, newProps) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const node = doc.createElement("button");\n'
            'const a = () => 1, b = () => 2, c = () => 3;\n'
            'const count = () => Object.fromEntries(Object.entries(node.listeners).map(([k, v]) => '
            '[k, v.length]));\n'
            'syncEvents(node, {}, { onClick: a, onInput: b, id: "x" });\n'
            'console.log(JSON.stringify(count()), node.listeners.click[0] === a);\n'
            'syncEvents(node, { onClick: a, onInput: b }, { onClick: a, onInput: c });\n'
            'console.log(JSON.stringify(count()), node.listeners.input[0] === c);\n'
            'syncEvents(node, { onClick: a, onInput: c }, { onClick: b });\n'
            'console.log(JSON.stringify(count()), node.listeners.click[0] === b);\n'
            'syncEvents(node, { onClick: b }, {});\n'
            'console.log(JSON.stringify(count()));\n'
            'syncEvents(node, {}, { onMouseDown: a, onclick: b, on: c, title: "t" });\n'
            'console.log(JSON.stringify(count()));\n',
  'hint': 'Обойдите объединение ключей; для on* сравните старую и новую функции.',
  'expected': ['{"click":1,"input":1} true',
               '{"click":1,"input":1} true',
               '{"click":1,"input":0} true',
               '{"click":0,"input":0}',
               '{"click":0,"input":0,"mousedown":1}']},
 {'id': 'j29-memo',
  'mode': 'js',
  'title': 'memo для компонентов',
  'statement': 'Напишите memo(component, equals = shallowEqual): оборачивает функцию-компонент '
               'component(props). Обёртка W(props) возвращает результат component(props), но если '
               'props равны (equals) предыдущим переданным (при первом вызове сравнивать не с '
               'чем), вместо вызова возвращает прежний результат (ту же ссылку). У W есть счётчик '
               'W.renders — сколько раз реально вызывался component, и W.reset() — забыть кэш. '
               'shallowEqual(a, b) задайте сами: совпадение набора ключей и значений по Object.is '
               '(вложенное — по ссылке).',
  'starter': 'function shallowEqual(a, b) {\n'
             '}\n'
             'function memo(component, equals = shallowEqual) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const Row = memo((p) => ({ type: "li", text: p.item.name + (p.selected ? "*" : "") '
            '}));\n'
            'const item = { name: "a" };\n'
            'const r1 = Row({ item, selected: false });\n'
            'const r2 = Row({ item, selected: false });\n'
            'console.log(r1 === r2, Row.renders);\n'
            'const r3 = Row({ item, selected: true });\n'
            'console.log(r3 === r2, r3.text, Row.renders);\n'
            'const r4 = Row({ item: { name: "a" }, selected: true });\n'
            'console.log(r4 === r3, Row.renders);\n'
            'Row.reset();\n'
            'Row({ item, selected: false });\n'
            'console.log(Row.renders);\n'
            'const custom = memo((p) => ({ v: p.a.x }), (a, b) => a.a.x === b.a.x);\n'
            'const c1 = custom({ a: { x: 1 } }), c2 = custom({ a: { x: 1 } });\n'
            'console.log(c1 === c2, custom.renders);\n'
            'console.log(shallowEqual({ a: 1 }, { a: 1 }), shallowEqual({ a: 1 }, { a: 1, b: '
            'undefined }), shallowEqual({ a: NaN }, { a: NaN }));\n',
  'hint': 'Храните lastProps и lastResult; при reset очищайте.',
  'expected': ['true 1', 'false a* 2', 'false 3', '4', 'true 1', 'true false true']},
 {'id': 'j29-hooks',
  'mode': 'js',
  'title': 'Мини-хуки: useState и useMemo',
  'statement': 'Напишите createRuntime(): { render(Component, props), update(), useState, useMemo '
               '}. render(Component, props) запоминает компонент и свойства, вызывает '
               'Component(props) с «текущим runtime» и возвращает результат. Внутри компонента '
               'хуки работают по порядку вызовов (слоты сохраняются между render/update): '
               'useState(initial) → [значение, setState] (initial может быть функцией — вызывается '
               'один раз; setState(v | fn(prev)) записывает значение, и если оно изменилось '
               '(Object.is), помечает runtime «грязным»); useMemo(fn, deps) — пересчитывает fn '
               'только если deps изменились (по Object.is поэлементно; первый вызов всегда '
               'считает) и возвращает значение. update() — если runtime грязный, повторно вызывает '
               'последний компонент с теми же props, сбрасывает флаг и возвращает новый результат; '
               "иначе возвращает null. Хуки вне render — Error('Hooks can only be called inside a "
               "component').",
  'starter': 'function createRuntime() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const rt = createRuntime();\n'
            'let memoCalls = 0;\n'
            'let set;\n'
            'const Counter = (props) => {\n'
            '  const [n, setN] = rt.useState(() => props.start);\n'
            '  const [name] = rt.useState("c");\n'
            '  const doubled = rt.useMemo(() => { memoCalls++; return n * 2; }, [n]);\n'
            '  set = setN;\n'
            '  return `${name}:${n}:${doubled}`;\n'
            '};\n'
            'console.log(rt.render(Counter, { start: 5 }), memoCalls);\n'
            'console.log(rt.update());\n'
            'set(6);\n'
            'console.log(rt.update(), memoCalls);\n'
            'console.log(rt.update());\n'
            'set(6); console.log(rt.update());\n'
            'set((p) => p + 1); set((p) => p + 1);\n'
            'console.log(rt.update(), memoCalls);\n'
            'try { rt.useState(1); } catch (e) { console.log(e.message); }\n',
  'hint': 'Массив слотов и индекс, обнуляемый перед каждым вызовом компонента; useState/useMemo '
          'берут слот по индексу.',
  'expected': ['c:5:10 1',
               'null',
               'c:6:12 2',
               'null',
               'null',
               'c:8:16 3',
               'Hooks can only be called inside a component']},
 {'id': 'j29-duplicate-keys',
  'mode': 'js',
  'title': 'Повторяющиеся ключи',
  'statement': 'Функция h уже есть. Напишите findDuplicateKeys(vnode) → массив { path, key }: для '
               'каждого узла с детьми найдите дочерние узлы, у которых key !== undefined и ключ '
               'повторяется среди его детей. Для каждого повторяющегося ключа — одна запись (при '
               'трёх одинаковых — всё равно одна). path — строка индексов от корня через точку '
               '(«root», «root.0», «root.0.2»: индекс ребёнка в родителе), указывающая на '
               'родителя. Порядок обхода — в глубину слева направо; для одного родителя записи '
               'идут в порядке первого появления дубликата.',
  'starter': '// Готово: создание виртуального узла (не изменяйте)\n'
             'function h(type, props, ...children) {\n'
             '  const flat = [];\n'
             '  const add = (c) => {\n'
             '    if (Array.isArray(c)) c.forEach(add);\n'
             '    else if (c === null || c === undefined || c === true || c === false) return;\n'
             '    else if (typeof c === "object") flat.push(c);\n'
             '    else flat.push({ type: "#text", text: String(c) });\n'
             '  };\n'
             '  children.forEach(add);\n'
             '  const p = { ...(props || {}) };\n'
             '  const key = p.key;\n'
             '  delete p.key;\n'
             '  return { type, props: p, key, children: flat };\n'
             '}\n'
             'function findDuplicateKeys(vnode) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (v) => console.log(JSON.stringify(findDuplicateKeys(v)));\n'
            't(h("ul", null, h("li", { key: "a" }), h("li", { key: "b" }), h("li", { key: "a" '
            '})));\n'
            't(h("div", null, h("ul", null, h("li", { key: 1 }), h("li", { key: 1 }), h("li", { '
            'key: 1 })), h("ol", null, h("li", { key: "x" }), h("li", { key: "y" }))));\n'
            't(h("div", null, h("p"), h("p"), h("p", { key: 0 }), h("p", { key: 0 })));\n'
            't(h("div", null, h("ul", null, h("li", { key: 1 })), h("ul", null, h("li", { key: 1 '
            '}))));\n'
            't(h("div", null, h("i", { key: "k" }), h("b", { key: "k" }), h("i", { key: "m" }), '
            'h("b", { key: "m" })));\n'
            't(h("br"));\n',
  'hint': 'Рекурсия с path; Map ключ → количество среди детей.',
  'expected': ['[{"path":"root","key":"a"}]',
               '[{"path":"root.0","key":1}]',
               '[{"path":"root","key":0}]',
               '[]',
               '[{"path":"root","key":"k"},{"path":"root","key":"m"}]',
               '[]']},
 {'id': 'j29-text-diff',
  'mode': 'js',
  'title': 'Минимальная правка текста',
  'statement': 'Напишите diffText(a, b) → { start, deleteCount, insert }: единственная правка, '
               'превращающая a в b — заменить a.slice(start, start + deleteCount) на строку '
               'insert. Найдите общий префикс, затем общий суффикс (не пересекающийся с префиксом) '
               'и верните то, что между ними. Если строки равны — { start: a.length, deleteCount: '
               "0, insert: '' }. Префикс всегда берётся максимальным.",
  'starter': 'function diffText(a, b) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (a, b) => { const d = diffText(a, b); console.log(JSON.stringify(a), '
            'JSON.stringify(b), JSON.stringify(d), a.slice(0, d.start) + d.insert + '
            'a.slice(d.start + d.deleteCount) === b); };\n'
            't("hello", "hello"); t("hello", "help"); t("abc", "abXc"); t("abc", "ac"); t("", '
            '"x"); t("x", ""); t("aaa", "aa"); t("abcabc", "abcXabc"); t("abab", "ab"); t("ab", '
            '"abab");\n',
  'hint': 'Сначала i — длина префикса; затем j — длина суффикса, не заходящего за префикс.',
  'expected': ['"hello" "hello" {"start":5,"deleteCount":0,"insert":""} true',
               '"hello" "help" {"start":3,"deleteCount":2,"insert":"p"} true',
               '"abc" "abXc" {"start":2,"deleteCount":0,"insert":"X"} true',
               '"abc" "ac" {"start":1,"deleteCount":1,"insert":""} true',
               '"" "x" {"start":0,"deleteCount":0,"insert":"x"} true',
               '"x" "" {"start":0,"deleteCount":1,"insert":""} true',
               '"aaa" "aa" {"start":2,"deleteCount":1,"insert":""} true',
               '"abcabc" "abcXabc" {"start":3,"deleteCount":0,"insert":"X"} true',
               '"abab" "ab" {"start":2,"deleteCount":2,"insert":""} true',
               '"ab" "abab" {"start":2,"deleteCount":0,"insert":"ab"} true']},
 {'id': 'j29-keyed-apply',
  'mode': 'js',
  'title': 'Применение перестановок к списку DOM',
  'statement': 'Модель DOM (MiniNode, doc, dump) и reconcileKeys(oldKeys, newKeys) (возвращает { '
               'removed, created, moves }) уже есть. Напишите patchList(list, newKeys, doc): list '
               '— MiniNode-список, дети — «li» с атрибутом data-key и текстовым ребёнком (ключ). '
               'Приведите детей к порядку newKeys, сохраняя существующие узлы (по data-key): '
               "удалите узлы из removed; создайте узлы для created (createElement('li'), data-key "
               '= ключ, один текстовый ребёнок с ключом); затем расставьте детей так, чтобы '
               'порядок совпал с newKeys, вызывая insertAt только для тех узлов, которые не стоят '
               'на нужной позиции (узлы, уже стоящие правильно, не трогать). Верните { created: '
               'число созданных, moved: число вызовов insertAt (включая вставки новых)}.',
  'starter': '// Готово: модель DOM для упражнений (не изменяйте)\n'
             'class MiniNode {\n'
             '  constructor(tag, text = null) { this.tag = tag; this.text = text; this.attrs = {}; '
             'this.children = []; this.listeners = {}; this.parent = null; }\n'
             '  append(c) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.push(c); return c; }\n'
             '  insertAt(c, i) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.splice(i, 0, c); return c; }\n'
             '  remove(c) { const i = this.children.indexOf(c); if (i >= 0) { '
             'this.children.splice(i, 1); c.parent = null; } return c; }\n'
             '  replaceChild(n, o) { const i = this.children.indexOf(o); this.children[i] = n; '
             'n.parent = this; o.parent = null; return o; }\n'
             '  setAttr(k, v) { this.attrs[k] = String(v); }\n'
             '  removeAttr(k) { delete this.attrs[k]; }\n'
             '  addListener(ev, fn) { (this.listeners[ev] ||= []).push(fn); }\n'
             '  removeListener(ev, fn) { const a = this.listeners[ev] || []; const i = '
             'a.indexOf(fn); if (i >= 0) a.splice(i, 1); }\n'
             '}\n'
             'const doc = { createElement: (tag) => new MiniNode(tag), createText: (t) => new '
             'MiniNode("#text", t) };\n'
             'function dump(n) {\n'
             '  if (n.tag === "#text") return JSON.stringify(n.text);\n'
             '  const attrs = Object.keys(n.attrs).sort().map((k) => ` '
             '${k}=${n.attrs[k]}`).join("");\n'
             '  const ev = Object.keys(n.listeners).filter((k) => '
             'n.listeners[k].length).sort().map((k) => ` @${k}`).join("");\n'
             '  return n.tag + attrs + ev + (n.children.length ? "(" + n.children.map(dump).join(" '
             '") + ")" : "");\n'
             '}\n'
             'function reconcileKeys(oldKeys, newKeys) {\n'
             '  const oldIndex = new Map(oldKeys.map((k, i) => [k, i]));\n'
             '  const newSet = new Set(newKeys);\n'
             '  const removed = oldKeys.filter((k) => !newSet.has(k));\n'
             '  const created = newKeys.filter((k) => !oldIndex.has(k));\n'
             '  const moves = [];\n'
             '  let lastPlaced = 0;\n'
             '  newKeys.forEach((key, to) => {\n'
             '    if (!oldIndex.has(key)) return;\n'
             '    const oi = oldIndex.get(key);\n'
             '    if (oi < lastPlaced) moves.push({ key, to });\n'
             '    else lastPlaced = oi;\n'
             '  });\n'
             '  return { removed, created, moves };\n'
             '}\n'
             'function patchList(list, newKeys, doc) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const mk = (keys) => { const ul = doc.createElement("ul"); for (const k of keys) { '
            'const li = doc.createElement("li"); li.setAttr("data-key", k); '
            'li.append(doc.createText(k)); ul.append(li); } return ul; };\n'
            'const order = (ul) => ul.children.map((c) => c.attrs["data-key"]).join("");\n'
            'const run = (oldKeys, newKeys) => {\n'
            '  const ul = mk(oldKeys);\n'
            '  const nodes = Object.fromEntries(ul.children.map((c) => [c.attrs["data-key"], '
            'c]));\n'
            '  const r = patchList(ul, newKeys, doc);\n'
            '  const same = Object.keys(nodes).filter((k) => newKeys.includes(k)).every((k) => '
            'ul.children.includes(nodes[k]));\n'
            '  console.log(oldKeys.join("") + "→" + newKeys.join(""), order(ul), '
            'JSON.stringify(r), same, ul.children.every((c) => c.children[0].text === '
            'c.attrs["data-key"]));\n'
            '};\n'
            'run(["a", "b", "c"], ["a", "b", "c"]);\n'
            'run(["a", "b", "c"], ["x", "a", "b", "c"]);\n'
            'run(["a", "b", "c", "d"], ["c", "a", "b", "d"]);\n'
            'run(["a", "b", "c", "d"], ["d", "c", "b", "a"]);\n'
            'run(["a", "b", "c"], ["c"]);\n'
            'run(["a", "b"], ["y", "x"]);\n'
            'run([], ["p", "q"]);\n'
            'run(["a", "b", "c", "d", "e"], ["b", "e", "x", "a", "d"]);\n',
  'hint': 'Соберите Map ключ → узел; затем идите по newKeys и для позиции i проверяйте '
          'list.children[i] === узел.',
  'expected': ['abc→abc abc {"created":0,"moved":0} true true',
               'abc→xabc xabc {"created":1,"moved":1} true true',
               'abcd→cabd cabd {"created":0,"moved":1} true true',
               'abcd→dcba dcba {"created":0,"moved":3} true true',
               'abc→c c {"created":0,"moved":0} true true',
               'ab→yx yx {"created":2,"moved":2} true true',
               '→pq pq {"created":2,"moved":2} true true',
               'abcde→bexad bexad {"created":1,"moved":3} true true']},
 {'id': 'j29-hydrate',
  'mode': 'js',
  'title': 'Проверка гидратации',
  'statement': 'Напишите hydrateCheck(node, vnode): node — MiniNode (разметка с сервера: поля tag, '
               'text, attrs, children), vnode — клиентское описание ({ type, props, children }, '
               "текстовые — { type: '#text', text }). Верните массив расхождений (строк) в порядке "
               'обхода в глубину, путь — индексы от корня через точку, корень — «0». Проверки узла '
               'по порядку: тип/тег («ПУТЬ: tag mismatch (div vs span)» — node.tag vs vnode.type; '
               'при расхождении дети не проверяются); для текста — «ПУТЬ: text mismatch ("а" vs '
               '"б")» (JSON-кавычки); для элементов — атрибуты: для каждого не-обработчика (не '
               'on*) свойства vnode со значением не null/undefined/false — ожидаемая строка (true '
               "→ '', class-массив — через пробел) должна совпасть с node.attrs[имя], иначе «ПУТЬ: "
               'attribute id mismatch ("a" vs "b")» (отсутствующий — JSON null); затем число детей '
               '«ПУТЬ: child count mismatch (2 vs 3)» (сначала сервер, потом клиент) — и дети '
               'проверяются попарно до минимума. Атрибуты в порядке ключей props.',
  'starter': '// Готово: модель DOM для упражнений (не изменяйте)\n'
             'class MiniNode {\n'
             '  constructor(tag, text = null) { this.tag = tag; this.text = text; this.attrs = {}; '
             'this.children = []; this.listeners = {}; this.parent = null; }\n'
             '  append(c) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.push(c); return c; }\n'
             '  insertAt(c, i) { if (c.parent) c.parent.remove(c); c.parent = this; '
             'this.children.splice(i, 0, c); return c; }\n'
             '  remove(c) { const i = this.children.indexOf(c); if (i >= 0) { '
             'this.children.splice(i, 1); c.parent = null; } return c; }\n'
             '  replaceChild(n, o) { const i = this.children.indexOf(o); this.children[i] = n; '
             'n.parent = this; o.parent = null; return o; }\n'
             '  setAttr(k, v) { this.attrs[k] = String(v); }\n'
             '  removeAttr(k) { delete this.attrs[k]; }\n'
             '  addListener(ev, fn) { (this.listeners[ev] ||= []).push(fn); }\n'
             '  removeListener(ev, fn) { const a = this.listeners[ev] || []; const i = '
             'a.indexOf(fn); if (i >= 0) a.splice(i, 1); }\n'
             '}\n'
             'const doc = { createElement: (tag) => new MiniNode(tag), createText: (t) => new '
             'MiniNode("#text", t) };\n'
             'function dump(n) {\n'
             '  if (n.tag === "#text") return JSON.stringify(n.text);\n'
             '  const attrs = Object.keys(n.attrs).sort().map((k) => ` '
             '${k}=${n.attrs[k]}`).join("");\n'
             '  const ev = Object.keys(n.listeners).filter((k) => '
             'n.listeners[k].length).sort().map((k) => ` @${k}`).join("");\n'
             '  return n.tag + attrs + ev + (n.children.length ? "(" + n.children.map(dump).join(" '
             '") + ")" : "");\n'
             '}\n'
             '// Готово: создание виртуального узла (не изменяйте)\n'
             'function h(type, props, ...children) {\n'
             '  const flat = [];\n'
             '  const add = (c) => {\n'
             '    if (Array.isArray(c)) c.forEach(add);\n'
             '    else if (c === null || c === undefined || c === true || c === false) return;\n'
             '    else if (typeof c === "object") flat.push(c);\n'
             '    else flat.push({ type: "#text", text: String(c) });\n'
             '  };\n'
             '  children.forEach(add);\n'
             '  const p = { ...(props || {}) };\n'
             '  const key = p.key;\n'
             '  delete p.key;\n'
             '  return { type, props: p, key, children: flat };\n'
             '}\n'
             'function hydrateCheck(node, vnode) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const el = (tag, attrs = {}, kids = []) => { const n = doc.createElement(tag); for '
            '(const [k, v] of Object.entries(attrs)) n.setAttr(k, v); for (const c of kids) '
            'n.append(c); return n; };\n'
            'const txt = (t) => doc.createText(t);\n'
            'const server = el("div", { id: "app", class: "a b" }, [el("p", {}, [txt("hello")]), '
            'el("ul", {}, [el("li", {}, [txt("1")]), el("li", {}, [txt("2")])])]);\n'
            'const same = h("div", { id: "app", class: ["a", "b"], onClick: () => 1 }, h("p", '
            'null, "hello"), h("ul", null, h("li", null, "1"), h("li", null, "2")));\n'
            'console.log(JSON.stringify(hydrateCheck(server, same)));\n'
            'const bad = h("div", { id: "other", class: ["a", "b"], title: "t", hidden: true }, '
            'h("span", null, "hello"), h("ul", null, h("li", null, "1"), h("li", null, "x"), '
            'h("li", null, "3")));\n'
            'console.log(hydrateCheck(server, bad).join("\\n"));\n'
            'console.log(JSON.stringify(hydrateCheck(txt("a"), { type: "#text", text: "b" })));\n'
            'console.log(JSON.stringify(hydrateCheck(el("p"), h("p", { id: false, x: null }))));\n',
  'hint': 'Рекурсивная функция с path; сначала tag, потом attrs, потом count, потом дети.',
  'expected': ['[]',
               '0: attribute id mismatch ("app" vs "other")',
               '0: attribute title mismatch (null vs "t")',
               '0: attribute hidden mismatch (null vs "")',
               '0.0: tag mismatch (p vs span)',
               '0.1: child count mismatch (2 vs 3)',
               '0.1.1.0: text mismatch ("2" vs "x")',
               '["0: text mismatch (\\"a\\" vs \\"b\\")"]',
               '[]']},
 {'id': 'j29-batcher',
  'mode': 'js',
  'title': 'Пакетный планировщик обновлений',
  'statement': 'Напишите createBatcher(applyFn): возвращает функцию enqueue(update) → Promise. '
               'update — любое значение (например, функция). enqueue накапливает обновления; в '
               'ближайшей микрозадаче (queueMicrotask) applyFn вызывается один раз с массивом всех '
               'накопленных обновлений в порядке постановки, после чего все промисы этой пачки '
               'завершаются значением, которое вернул applyFn. Обновления, поставленные после '
               'срабатывания, попадают в следующую пачку (новый вызов applyFn). Исключение в '
               'applyFn отклоняет промисы пачки (но следующая пачка работает как обычно).',
  'starter': 'function createBatcher(applyFn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const calls = [];\n'
            'const enqueue = createBatcher((updates) => { calls.push(updates.join(",")); return '
            'updates.length; });\n'
            'const p1 = enqueue("a"), p2 = enqueue("b"), p3 = enqueue("c");\n'
            'console.log(calls.length);\n'
            'console.log(await Promise.all([p1, p2, p3]), calls.join(" | "));\n'
            'const p4 = enqueue("d");\n'
            'await p4;\n'
            'const p5 = enqueue("e"), p6 = enqueue("f");\n'
            'await Promise.all([p5, p6]);\n'
            'console.log(calls.join(" | "));\n'
            'let boom = true;\n'
            'const e2 = createBatcher((u) => { if (boom) { boom = false; throw new Error("bad " + '
            'u.length); } return "ok"; });\n'
            'const r1 = e2(1).catch((e) => e.message), r2 = e2(2).catch((e) => e.message);\n'
            'console.log(await r1, await r2, await e2(3));\n',
  'hint': 'queue и флаг scheduled; в микрозадаче вынуть очередь и вызвать applyFn с try/catch.',
  'expected': ['0', '[ 3, 3, 3 ] a,b,c', 'a,b,c | d | e,f', 'bad 2 bad 2 ok']},
 {'id': 'j29-lifecycle',
  'mode': 'js',
  'title': 'События жизненного цикла',
  'statement': 'Функция h уже есть. Напишите lifecycleEvents(oldTree, newTree) → массив строк. '
               'Деревья — vnode; интересуют только узлы-компоненты (type — функция; имя — '
               'type.name). Сопоставление: на одной позиции (индекс ребёнка) и при одинаковом type '
               '— «update ИМЯ»; иначе старый компонент — «unmount ИМЯ», новый — «mount ИМЯ». '
               'Порядок событий: сначала все unmount (обход старого дерева в обратном порядке — '
               'дети раньше родителя, справа налево... нет: постфиксный обход слева направо), '
               'затем mount и update в префиксном порядке обхода нового дерева. Дети '
               'сопоставляются по индексу; у компонента детьми считаются children его vnode '
               '(результат функции вызывать не нужно). Нет старого дерева (null) — только mount; '
               'нет нового — только unmount. Элементы-не-компоненты не порождают событий, но их '
               'дети сопоставляются дальше.',
  'starter': '// Готово: создание виртуального узла (не изменяйте)\n'
             'function h(type, props, ...children) {\n'
             '  const flat = [];\n'
             '  const add = (c) => {\n'
             '    if (Array.isArray(c)) c.forEach(add);\n'
             '    else if (c === null || c === undefined || c === true || c === false) return;\n'
             '    else if (typeof c === "object") flat.push(c);\n'
             '    else flat.push({ type: "#text", text: String(c) });\n'
             '  };\n'
             '  children.forEach(add);\n'
             '  const p = { ...(props || {}) };\n'
             '  const key = p.key;\n'
             '  delete p.key;\n'
             '  return { type, props: p, key, children: flat };\n'
             '}\n'
             'function lifecycleEvents(oldTree, newTree) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const A = () => null, B = () => null, C = () => null;\n'
            'const show = (o, n) => console.log(lifecycleEvents(o, n).join(" | "));\n'
            'show(null, h(A, null, h(B)));\n'
            'show(h(A, null, h(B)), null);\n'
            'show(h(A, null, h(B), h(C)), h(A, null, h(B), h(C)));\n'
            'show(h(A, null, h(B), h(C)), h(A, null, h(C)));\n'
            'show(h("div", null, h(A, null, h(B)), h(C)), h("div", null, h(A, null, h(C)), '
            'h(B)));\n'
            'show(h(A, null, h("p", null, h(B))), h(C, null, h("p", null, h(B))));\n'
            'show(h("div", null, h(A), h(B)), h("div", null, h(A)));\n',
  'hint': 'Две фазы: collectUnmounts(old, new) по постфиксному обходу и collectMountsUpdates(old, '
          'new) по префиксному.',
  'expected': ['mount A | mount B',
               'unmount B | unmount A',
               'update A | update B | update C',
               'unmount B | unmount C | update A | mount C',
               'unmount B | unmount C | update A | mount C | mount B',
               'unmount B | unmount A | mount C | mount B',
               'unmount B | update A']},
 {'id': 'j29-fragments',
  'mode': 'js',
  'title': 'Фрагменты',
  'statement': "Напишите Fragment (уникальный Symbol('Fragment')), h(type, props, ...children) и "
               'flatten(vnode). h — как обычно: { type, props, key, children } с нормализацией '
               'детей (массивы раскрываются, null/undefined/true/false отбрасываются, строки и '
               "числа → { type: '#text', text }). flatten(vnode) возвращает новое дерево, в "
               'котором фрагменты внутри детей заменены своими детьми (рекурсивно, в том же '
               'порядке), а корень-фрагмент возвращается как массив узлов; обычные элементы '
               'остаются элементами с очищенными детьми. Текстовые узлы возвращаются как есть. '
               'flatten не изменяет исходное дерево.',
  'starter': 'const Fragment = Symbol("Fragment");\n'
             'function h(type, props, ...children) {\n'
             '}\n'
             'function flatten(vnode) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(flatten(h("ul", null, h("li", null, "a"), h(Fragment, null, h("li", null, "b"), '
            'h(Fragment, null, h("li", null, "c"), "d")), h("li", null, "e"))));\n'
            'show(flatten(h(Fragment, null, h("p", null, "1"), h("p", null, "2"))));\n'
            'show(flatten(h(Fragment, null)));\n'
            'show(flatten({ type: "#text", text: "x" }));\n'
            'const src = h("div", null, h(Fragment, null, "z"));\n'
            'flatten(src);\n'
            'console.log(src.children[0].type === Fragment, typeof Fragment);\n',
  'hint': 'flattenChildren(children) раскрывает вложенные фрагменты; корневой фрагмент — '
          'flattenChildren(vnode.children).',
  'expected': ['{"type":"ul","props":{},"children":[{"type":"li","props":{},"children":[{"type":"#text","text":"a"}]},{"type":"li","props":{},"children":[{"type":"#text","text":"b"}]},{"type":"li","props":{},"children":[{"type":"#text","text":"c"}]},{"type":"#text","text":"d"},{"type":"li","props":{},"children":[{"type":"#text","text":"e"}]}]}',
               '[{"type":"p","props":{},"children":[{"type":"#text","text":"1"}]},{"type":"p","props":{},"children":[{"type":"#text","text":"2"}]}]',
               '[]',
               '{"type":"#text","text":"x"}',
               'true symbol']},
 {'id': 'j29-each-when',
  'mode': 'js',
  'title': 'Хелперы each и when',
  'statement': 'Функция h уже есть. Напишите each(list, keyFn, renderFn), when(cond, thunk, '
               'otherwise = null) и match(value, cases, fallback = null). each возвращает массив '
               'vnode: для каждого элемента (item, index) результат renderFn(item, index), у '
               'которого поле key выставлено в keyFn(item, index) (результат renderFn — vnode; его '
               "key переопределяется); повторяющийся ключ — Error('Duplicate key: КЛЮЧ'). when: "
               'cond истинно — thunk(), иначе otherwise (значение или null; если otherwise — '
               'функция, вызвать её). match: cases — объект «значение → thunk»; если ключ value '
               '(String(value)) есть в cases — вызвать thunk, иначе fallback (функция вызывается, '
               'иначе возвращается как есть).',
  'starter': '// Готово: создание виртуального узла (не изменяйте)\n'
             'function h(type, props, ...children) {\n'
             '  const flat = [];\n'
             '  const add = (c) => {\n'
             '    if (Array.isArray(c)) c.forEach(add);\n'
             '    else if (c === null || c === undefined || c === true || c === false) return;\n'
             '    else if (typeof c === "object") flat.push(c);\n'
             '    else flat.push({ type: "#text", text: String(c) });\n'
             '  };\n'
             '  children.forEach(add);\n'
             '  const p = { ...(props || {}) };\n'
             '  const key = p.key;\n'
             '  delete p.key;\n'
             '  return { type, props: p, key, children: flat };\n'
             '}\n'
             'function each(list, keyFn, renderFn) {\n'
             '}\n'
             'function when(cond, thunk, otherwise = null) {\n'
             '}\n'
             'function match(value, cases, fallback = null) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const items = [{ id: 1, n: "a" }, { id: 2, n: "b" }];\n'
            'const rows = each(items, (x) => "row" + x.id, (x, i) => h("li", { class: "r" + i }, '
            'x.n));\n'
            'console.log(JSON.stringify(rows.map((r) => [r.key, r.props.class, '
            'r.children[0].text])));\n'
            'try { each([1, 1], (x) => x, (x) => h("i", null, x)); } catch (e) { '
            'console.log(e.message); }\n'
            'console.log(each([], (x) => x, () => h("b")).length);\n'
            'console.log(JSON.stringify(when(true, () => "yes")), when(false, () => "yes"), '
            'when(false, () => "yes", "no"), when(0, () => "y", () => "lazy"));\n'
            'const cases = { loading: () => h("p", null, "..."), error: () => "E", 0: () => "zero" '
            '};\n'
            'console.log(JSON.stringify(match("loading", cases)), match("error", cases), match(0, '
            'cases), match("other", cases), match("other", cases, () => "dflt"), match("x", cases, '
            '"plain"));\n',
  'hint': "Set для проверки ключей; вспомогательная call(x) = typeof x === 'function' ? x() : x.",
  'expected': ['[["row1","r0","a"],["row2","r1","b"]]',
               'Duplicate key: 1',
               '0',
               '"yes" null no lazy',
               '{"type":"p","props":{},"children":[{"type":"#text","text":"..."}]} E zero null '
               'dflt plain']},
 {'id': 'j29-sanitize',
  'mode': 'js',
  'title': 'Санитайзер HTML',
  'statement': 'Напишите sanitizeHtml(html, { tags, attrs }): tags — массив разрешённых тегов '
               "(строчные), attrs — объект «тег → разрешённые атрибуты» (ключ '*' — для всех "
               'тегов). Вход — простая разметка: теги с атрибутами в двойных кавычках и текст. '
               'Правила: тег не из списка — удаляется (открывающий и закрывающий), внутренний '
               'текст и разрешённые вложенные теги остаются; исключение — script и style: '
               'удаляются вместе с содержимым. Атрибут не из разрешённых удаляется; атрибуты, '
               'начинающиеся с «on», удаляются всегда; значения href и src, начинающиеся (после '
               'обрезки пробелов, без учёта регистра) с «javascript:», «data:» или «vbscript:», '
               'удаляются вместе с атрибутом. Остальные атрибуты сохраняются в исходном порядке и '
               'форме (имя="значение"). Текст не изменяется. Закрывающие теги разрешённых '
               'элементов сохраняются как есть.',
  'starter': 'function sanitizeHtml(html, policy) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const policy = { tags: ["p", "b", "a", "img", "i"], attrs: { "*": ["title"], a: '
            '["href"], img: ["src", "alt"] } };\n'
            'const t = (s) => console.log(sanitizeHtml(s, policy));\n'
            't(\'<p title="t" id="x">Hello <b>world</b></p>\');\n'
            "t('<div><p>in div</p><span>text</span></div>');\n"
            't(\'<a href="https://ok.example" onclick="evil()">link</a>\');\n'
            't(\'<a href=" JavaScript:alert(1)" title="x">bad</a>\');\n'
            't(\'<img src="data:text/html,x" alt="a"><img src="/a.png" alt="b" width="9">\');\n'
            "t('before<script>alert(1)</script>after<style>p{}</style>end');\n"
            "t('<p>unclosed <i>italic');\n"
            "t('<table><tr><td>cell</td></tr></table>');\n"
            't("plain text only");\n',
  'hint': 'Токенизируйте регулярным выражением /<\\/?[a-zA-Z][^>]*>|[^<]+/g; для script/style '
          'пропускайте всё до закрывающего.',
  'expected': ['<p title="t">Hello <b>world</b></p>',
               '<p>in div</p>text',
               '<a href="https://ok.example">link</a>',
               '<a title="x">bad</a>',
               '<img alt="a"><img src="/a.png" alt="b">',
               'beforeafterend',
               '<p>unclosed <i>italic',
               'cell',
               'plain text only']},
 {'id': 'j29-count-ops',
  'mode': 'js',
  'title': 'Сводка патчей',
  'statement': "Формат патчей как у diff: null | { type: 'CREATE', node } | { type: 'REMOVE' } | { "
               "type: 'REPLACE', node } | { type: 'TEXT', text } | { type: 'UPDATE', props: [{ op: "
               "'set'|'remove', name, value? }], children: [патчи] }. Напишите countOps(patch) → "
               'объект счётчиков { CREATE, REMOVE, REPLACE, TEXT, UPDATE, SET, UNSET } — все ключи '
               'всегда присутствуют (в этом порядке): суммы по всему дереву; SET и UNSET считают '
               'операции props (set и remove). null — все нули. Затем напишите isCheap(patch, '
               'limit): true, если общее число операций (CREATE + REMOVE + REPLACE + TEXT + SET + '
               'UNSET, UPDATE не считается) не больше limit.',
  'starter': 'function countOps(patch) {\n}\nfunction isCheap(patch, limit) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const patch = { type: "UPDATE", props: [{ op: "set", name: "class", value: "x" }, { '
            'op: "remove", name: "id" }], children: [\n'
            '  null,\n'
            '  { type: "TEXT", text: "t" },\n'
            '  { type: "UPDATE", props: [{ op: "set", name: "a", value: 1 }], children: [{ type: '
            '"CREATE", node: {} }, { type: "REMOVE" }, null, { type: "REPLACE", node: {} }] },\n'
            '  { type: "REMOVE" },\n'
            '] };\n'
            'console.log(JSON.stringify(countOps(patch)));\n'
            'console.log(JSON.stringify(countOps(null)), JSON.stringify(countOps({ type: "TEXT", '
            'text: "x" })));\n'
            'console.log(isCheap(patch, 8), isCheap(patch, 7), isCheap(null, 0), isCheap({ type: '
            '"UPDATE", props: [], children: [] }, 0));\n',
  'hint': 'Рекурсия по children; счётчики в одном объекте.',
  'expected': ['{"CREATE":1,"REMOVE":2,"REPLACE":1,"TEXT":1,"UPDATE":2,"SET":2,"UNSET":1}',
               '{"CREATE":0,"REMOVE":0,"REPLACE":0,"TEXT":0,"UPDATE":0,"SET":0,"UNSET":0} '
               '{"CREATE":0,"REMOVE":0,"REPLACE":0,"TEXT":1,"UPDATE":0,"SET":0,"UNSET":0}',
               'true false true true']},
 {'id': 'j29-patch-paths',
  'mode': 'js',
  'title': 'Патчи по путям',
  'statement': 'Патчи как у diff (null | CREATE | REMOVE | REPLACE | TEXT | UPDATE { props, '
               'children }). Напишите flattenPatches(patch): массив записей { path, type, ... } в '
               'порядке обхода в глубину (родитель раньше детей). path — массив индексов детей от '
               "корня (корень — []). Для UPDATE с непустым props — запись { path, type: 'PROPS', "
               'ops: props }; затем рекурсивно записи детей (path + [i]). Для CREATE, REMOVE, '
               'REPLACE, TEXT — одна запись { path, type } плюс поле node (для CREATE/REPLACE) или '
               'text (для TEXT). null не порождает записей. UPDATE без props и без значимых детей '
               'записей не даёт.',
  'starter': 'function flattenPatches(patch) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const n1 = { type: "p" };\n'
            'const patch = { type: "UPDATE", props: [{ op: "set", name: "id", value: "x" }], '
            'children: [\n'
            '  null,\n'
            '  { type: "UPDATE", props: [], children: [{ type: "TEXT", text: "hi" }, null, { type: '
            '"CREATE", node: n1 }] },\n'
            '  { type: "REMOVE" },\n'
            '  { type: "UPDATE", props: [{ op: "remove", name: "a" }], children: [{ type: '
            '"REPLACE", node: n1 }] },\n'
            '] };\n'
            'const r = flattenPatches(patch);\n'
            'console.log(JSON.stringify(r, (k, v) => (k === "node" ? "node" : v)));\n'
            'console.log(JSON.stringify(flattenPatches(null)), JSON.stringify(flattenPatches({ '
            'type: "TEXT", text: "t" })));\n'
            'console.log(JSON.stringify(flattenPatches({ type: "UPDATE", props: [], children: '
            '[null, null] })));\n',
  'hint': 'Рекурсивная функция с накопителем и текущим path.',
  'expected': ['[{"path":[],"type":"PROPS","ops":[{"op":"set","name":"id","value":"x"}]},{"path":[1,0],"type":"TEXT","text":"hi"},{"path":[1,2],"type":"CREATE","node":"node"},{"path":[2],"type":"REMOVE"},{"path":[3],"type":"PROPS","ops":[{"op":"remove","name":"a"}]},{"path":[3,0],"type":"REPLACE","node":"node"}]',
               '[] [{"path":[],"type":"TEXT","text":"t"}]',
               '[]']},
 {'id': 'j29-should-update',
  'mode': 'js',
  'title': 'Когда перерисовывать',
  'statement': 'Напишите shouldUpdate(prev, next, opts = {}) → boolean. Сравнение свойств: набор '
               'ключей должен совпадать; значения по Object.is, кроме: ключи из opts.ignore — '
               'пропускаются; ключи из opts.deep — сравниваются глубоко (массивы поэлементно, '
               'объекты по ключам, примитивы по Object.is; циклов нет); функции сравниваются по '
               'ссылке, если не задан opts.ignoreFunctions === true (тогда любые функции считаются '
               'равными). Возвращает true, если нужен перерендер (свойства различаются).',
  'starter': 'function shouldUpdate(prev, next, opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const f = () => 1, g = () => 1;\n'
            'const t = (a, b, o) => console.log(shouldUpdate(a, b, o));\n'
            't({ a: 1 }, { a: 1 }); t({ a: 1 }, { a: 2 }); t({ a: 1 }, { a: 1, b: 2 }); t({ f }, { '
            'f }); t({ f }, { f: g }); t({ f }, { f: g }, { ignoreFunctions: true });\n'
            't({ items: [1, 2] }, { items: [1, 2] }); t({ items: [1, 2] }, { items: [1, 2] }, { '
            'deep: ["items"] }); t({ items: [1, 2] }, { items: [1, 3] }, { deep: ["items"] });\n'
            't({ o: { x: { y: 1 } } }, { o: { x: { y: 1 } } }, { deep: ["o"] }); t({ o: { x: 1 } '
            '}, { o: { x: 1, z: 2 } }, { deep: ["o"] });\n'
            't({ time: 1, n: 5 }, { time: 2, n: 5 }, { ignore: ["time"] }); t({ time: 1, n: 5 }, { '
            'time: 2, n: 6 }, { ignore: ["time"] });\n'
            't({ a: NaN }, { a: NaN }); t({}, {});\n',
  'hint': 'Внутренняя deepEq; перебор объединения ключей с учётом ignore/deep.',
  'expected': ['false',
               'true',
               'true',
               'false',
               'true',
               'false',
               'true',
               'false',
               'true',
               'false',
               'true',
               'false',
               'true',
               'false',
               'false']},
 {'id': 'j29-serialize',
  'mode': 'js',
  'title': 'Сериализация vnode',
  'statement': 'Напишите serializeVnode(vnode) → строка JSON и deserializeVnode(str). '
               'Сериализация: ключи объекта vnode и props — в порядке { type, props, key, children '
               '} и по алфавиту для props; значения-функции заменяются объектом { "$fn": имя } '
               '(имя функции или \'anonymous\'); значения Symbol — { "$sym": описание }; undefined '
               'в свойствах и key — опускаются (у vnode без key ключа key нет); дети — рекурсивно. '
               'Строка — JSON.stringify без пробелов. deserializeVnode превращает строку в объект '
               '(JSON.parse), функции и символы остаются маркерами. Отступов нет.',
  'starter': 'function serializeVnode(vnode) {\n}\nfunction deserializeVnode(str) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const Frag = Symbol("Fragment");\n'
            'function onSave() {}\n'
            'const v = { type: "div", props: { onClick: onSave, id: "a", hidden: undefined, '
            'handler: () => 1, tag: Frag, class: ["x"] }, key: undefined, children: [\n'
            '  { type: "#text", text: "hi" }, { type: Frag, props: {}, key: "k", children: [] }, { '
            'type: function Comp() {}, props: { z: 1, a: 2 }, children: [] },\n'
            '] };\n'
            'const s = serializeVnode(v);\n'
            'console.log(s);\n'
            'const back = deserializeVnode(s);\n'
            'console.log(back.type, JSON.stringify(back.props), back.children.length, '
            'back.children[1].key, JSON.stringify(back.children[1].type), '
            'JSON.stringify(back.children[2].type));\n'
            'console.log(serializeVnode({ type: "br", props: {}, children: [] }));\n',
  'hint': 'Рекурсивное преобразование с проверкой typeof; в конце JSON.stringify.',
  'expected': ['{"type":"div","props":{"class":["x"],"handler":{"$fn":"handler"},"id":"a","onClick":{"$fn":"onSave"},"tag":{"$sym":"Fragment"}},"children":[{"type":"#text","text":"hi"},{"type":{"$sym":"Fragment"},"props":{},"key":"k","children":[]},{"type":{"$fn":"Comp"},"props":{"a":2,"z":1},"children":[]}]}',
               'div '
               '{"class":["x"],"handler":{"$fn":"handler"},"id":"a","onClick":{"$fn":"onSave"},"tag":{"$sym":"Fragment"}} '
               '3 k {"$sym":"Fragment"} {"$fn":"Comp"}',
               '{"type":"br","props":{},"children":[]}']},
 {'id': 'j29-normalize-props',
  'mode': 'js',
  'title': 'Нормализация свойств в атрибуты',
  'statement': 'Напишите normalizeProps(props) → { attrs, events, style }. Правила в порядке '
               'ключей: className → атрибут class (строка, массив или объект — собрать как в '
               'classNames: ложные пропускаются, пустой результат — атрибута нет); htmlFor → for; '
               'tabIndex → tabindex; readOnly → readonly; httpEquiv → http-equiv; остальные — как '
               "есть (data-*, aria-* и т. п.). Булевы: true → атрибут со значением '' ; false, "
               'null, undefined — атрибут не создаётся. Числа и строки — в строку. Ключ key и ref '
               'пропускаются. Свойства-обработчики onЗаглавная… попадают в events: { имя события '
               'строчными без «on»: функция }. style: если это объект — возвращается в поле style '
               'как есть, не в attrs; если строка — attrs.style. Поле style — null, если не задан '
               'объект.',
  'starter': 'function normalizeProps(props) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const f = () => 1;\n'
            'const r = normalizeProps({ className: ["a", { b: true, c: false }], htmlFor: "x", '
            'tabIndex: 0, readOnly: true, disabled: false, "data-id": 7, title: null, onClick: f, '
            'onMouseDown: f, key: "k", ref: 1, style: { color: "red" }, "aria-label": "L" });\n'
            'console.log(JSON.stringify(r), r.events.click === f, r.events.mousedown === f);\n'
            'console.log(JSON.stringify(normalizeProps({ style: "color:red", className: "" })));\n'
            'console.log(JSON.stringify(normalizeProps({})));\n'
            'console.log(JSON.stringify(normalizeProps({ className: { x: false }, httpEquiv: '
            '"refresh", hidden: true, onInput: f })), JSON.stringify(Object.keys(normalizeProps({ '
            'onInput: f }).events)));\n',
  'hint': 'Таблица переименований; для class — собственная сборка строки.',
  'expected': ['{"attrs":{"class":"a '
               'b","for":"x","tabindex":"0","readonly":"","data-id":"7","aria-label":"L"},"events":{},"style":{"color":"red"}} '
               'true true',
               '{"attrs":{"style":"color:red"},"events":{},"style":null}',
               '{"attrs":{},"events":{},"style":null}',
               '{"attrs":{"http-equiv":"refresh","hidden":""},"events":{},"style":null} '
               '["input"]']}]}
