"""Задачи книги «Современный Frontend», глава 14 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {14: [{'id': 'j14-tree-ops',
       'mode': 'js',
       'title': 'Мини-DOM: appendChild, insertBefore, removeChild',
       'statement': 'Узлы — объекты { type, tag?, children?, parent }. Напишите функции appendChild(parent, '
                    'child) (если у child уже был родитель — сначала удаляется оттуда; возвращает child), '
                    'insertBefore(parent, child, ref) (ref === null — в конец; если ref не потомок parent — '
                    'Error("ref не потомок")), removeChild(parent, child) (если child не потомок — Error("не '
                    'потомок"); возвращает child, parent обнуляется), replaceChild(parent, newChild, '
                    'oldChild). Инвариант: child.parent всегда равен реальному родителю.',
       'starter': 'function appendChild(parent, child) {\n'
                  '}\n'
                  'function insertBefore(parent, child, ref) {\n'
                  '}\n'
                  'function removeChild(parent, child) {\n'
                  '}\n'
                  'function replaceChild(parent, newChild, oldChild) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const ul = el("ul", {}), a = el("li", {}, "a"), b = el("li", {}, "b"), c = el("li", {}, '
                 '"c");\n'
                 'appendChild(ul, a); appendChild(ul, b); insertBefore(ul, c, b);\n'
                 'const order = () => ul.children.map((n) => n.children[0].text).join("");\n'
                 'console.log(order(), c.parent === ul);\n'
                 'const other = el("ol", {});\n'
                 'appendChild(other, a);\n'
                 'console.log(order(), other.children.length, a.parent === other);\n'
                 'insertBefore(ul, a, null);\n'
                 'console.log(order(), other.children.length);\n'
                 'console.log(removeChild(ul, b) === b, order(), b.parent);\n'
                 'const d = el("li", {}, "d");\n'
                 'console.log(replaceChild(ul, d, c) === c, order(), c.parent, d.parent === ul);\n'
                 'for (const f of [() => removeChild(ul, b), () => insertBefore(ul, el("x"), b), () => '
                 'replaceChild(ul, el("y"), b)]) { try { f(); } catch (e) { console.log(e.message); } }\n'
                 'appendChild(ul, d);\n'
                 'console.log(order(), ul.children.length);\n',
       'hint': 'Универсальный detach(n) убирает узел из прежнего родителя; затем вставка по индексу.',
       'expected': ['acb true',
                    'cb 1 true',
                    'cba 0',
                    'true ca null',
                    'true da null true',
                    'не потомок',
                    'ref не потомок',
                    'не потомок',
                    'ad 2']},
      {'id': 'j14-traverse',
       'mode': 'js',
       'title': 'Обход и соседи',
       'statement': 'Напишите функции: walk(root, visit) (обход в глубину в порядке документа: узел раньше '
                    'потомков; visit(node, depth)), firstChild(n), lastChild(n), nextSibling(n), '
                    'previousSibling(n) (null, если нет), childElements(n) (только элементы), depthOf(n) '
                    '(корень — 0), path(n) → массив индексов от корня к узлу, и nodeAt(root, path).',
       'starter': 'function walk(root, visit) {\n'
                  '}\n'
                  'function firstChild(n) {\n'
                  '}\n'
                  'function lastChild(n) {\n'
                  '}\n'
                  'function nextSibling(n) {\n'
                  '}\n'
                  'function previousSibling(n) {\n'
                  '}\n'
                  'function childElements(n) {\n'
                  '}\n'
                  'function depthOf(n) {\n'
                  '}\n'
                  'function path(n) {\n'
                  '}\n'
                  'function nodeAt(root, p) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const root = page();\n'
                 'const out = [];\n'
                 'walk(root, (n, d) => { if (n.type === "element") out.push("  ".repeat(d) + n.tag); });\n'
                 'console.log(out.join("\\n"));\n'
                 'const list = nodeAt(root, [1, 0]);\n'
                 'console.log(list.tag, list.attrs.id, firstChild(list).tag, '
                 'lastChild(list).children[0].tag);\n'
                 'const second = list.children[1];\n'
                 'console.log(nextSibling(second).attrs.class, previousSibling(second).attrs.class, '
                 'nextSibling(lastChild(list)), previousSibling(firstChild(list)), nextSibling(root));\n'
                 'console.log(childElements(list.children[2]).map((n) => n.tag).join(), '
                 'childElements(second).length, depthOf(root), depthOf(second), '
                 'depthOf(second.children[0]));\n'
                 'console.log(JSON.stringify(path(second)), JSON.stringify(path(root)), nodeAt(root, '
                 'path(second)) === second, nodeAt(root, [9]), firstChild(second.children[0]));\n'
                 'let n = 0; walk(root, () => n++); console.log(n);\n',
       'hint': 'Соседей ищите через индекс в parent.children; путь — список индексов от корня.',
       'expected': ['div',
                    '  header',
                    '    h1',
                    '    nav',
                    '      a',
                    '      a',
                    '  main',
                    '    ul',
                    '      li',
                    '      li',
                    '      li',
                    '        span',
                    '    p',
                    'ul list li span',
                    'item item null null null',
                    'span 0 0 3 4',
                    '[1,0,1] [] true null null',
                    '20']},
      {'id': 'j14-text-content',
       'mode': 'js',
       'title': 'textContent',
       'statement': 'Напишите функции getTextContent(node) (склейка текста всех текстовых потомков в порядке '
                    'документа; для текстового узла — его текст) и setTextContent(node, text) (удаляет всех '
                    'детей элемента и, если text не пуст, добавляет один текстовый узел; у удалённых детей '
                    'parent = null). Для текстового узла setTextContent меняет его text.',
       'starter': 'function getTextContent(node) {\n}\nfunction setTextContent(node, text) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const p = el("p", {}, "Привет, ", el("b", {}, "мир"), "!", el("i", {}, el("u", {}, '
                 '"…")));\n'
                 'console.log(getTextContent(p), "|", getTextContent(p.children[1]), "|", '
                 'getTextContent(tx("т")), "|", JSON.stringify(getTextContent(el("div"))));\n'
                 'const old = p.children[1];\n'
                 'setTextContent(p, "новый <b>текст</b>");\n'
                 'console.log(p.children.length, p.children[0].text, p.children[0].parent === p, old.parent, '
                 'getTextContent(p));\n'
                 'setTextContent(p, "");\n'
                 'console.log(p.children.length);\n'
                 'const t = tx("старый"); setTextContent(t, "новый"); console.log(t.text);\n',
       'hint': 'Рекурсивная склейка; при записи — отсоединить прежних детей.',
       'expected': ['Привет, мир!… | мир | т | ""',
                    '1 новый <b>текст</b> true null новый <b>текст</b>',
                    '0',
                    'новый']},
      {'id': 'j14-serialize',
       'mode': 'js',
       'title': 'outerHTML: сериализация',
       'statement': 'Напишите функции escapeText(s) (& < > → &amp; &lt; &gt;), escapeAttr(s) (& < > " → '
                    '&amp; &lt; &gt; &quot;) и outerHTML(node): <тег атрибуты>дети</тег>; атрибуты — в '
                    'порядке объекта как name="value" (булев атрибут со значением true выводится одним '
                    'именем; false и null — пропускаются); пустые (void) теги br, hr, img, input, meta, link '
                    '— без закрывающего и без детей; текст экранируется (кроме содержимого script и style).',
       'starter': 'function escapeText(s) {\n}\nfunction escapeAttr(s) {\n}\nfunction outerHTML(node) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'console.log(escapeText("a < b && c > d"), "|", escapeAttr(\'он сказал "да" & <ушёл>\'));\n'
                 'console.log(outerHTML(el("p", { class: "a b", title: \'x"y\' }, "1 < 2 & ", el("b", {}, '
                 '"жирный"), el("br"), "конец")));\n'
                 'console.log(outerHTML(el("input", { type: "checkbox", checked: true, disabled: false, '
                 'hidden: null })));\n'
                 'console.log(outerHTML(el("div", {}, el("img", { src: "a.png", alt: "" }), el("hr"), '
                 'el("script", {}, "if (a < b && c) {}"))));\n'
                 'console.log(outerHTML(el("ul", {}, el("li", {}, "a"), el("li", {}, ""))), '
                 'outerHTML(tx("<текст>")));\n',
       'hint': 'Рекурсия; в script/style текст не экранируется.',
       'expected': ['a &lt; b &amp;&amp; c &gt; d | он сказал &quot;да&quot; &amp; &lt;ушёл&gt;',
                    '<p class="a b" title="x&quot;y">1 &lt; 2 &amp; <b>жирный</b><br>конец</p>',
                    '<input type="checkbox" checked>',
                    '<div><img src="a.png" alt=""><hr><script>if (a < b && c) {}</script></div>',
                    '<ul><li>a</li><li></li></ul> &lt;текст&gt;']},
      {'id': 'j14-parse-html',
       'mode': 'js',
       'title': 'Разбор HTML в дерево',
       'statement': 'Напишите функцию parseHTML(html) для упрощённого HTML: теги с атрибутами (name="value", '
                    "name='value', name=value, name без значения → true), void-теги (br, hr, img, input, "
                    'meta, link — без закрывающего), текст (с декодированием &amp; &lt; &gt; &quot;), '
                    'комментарии <!-- … --> пропускаются. Возвращает фрагмент: узел { type: "fragment", '
                    'children } — потомки с корректными parent. Лишний закрывающий тег игнорируется, '
                    'незакрытые закрываются в конце. Имена тегов — в нижнем регистре.',
       'starter': 'function parseHTML(html) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const dump = (n, d = 0) => (n.type === "text" ? "  ".repeat(d) + JSON.stringify(n.text) : '
                 'n.type === "fragment" ? n.children.map((c) => dump(c, d)).join("\\n") : "  ".repeat(d) + '
                 'n.tag + JSON.stringify(n.attrs) + (n.children.length ? "\\n" + n.children.map((c) => '
                 'dump(c, d + 1)).join("\\n") : ""));\n'
                 'const f = parseHTML(\'<div id=main class="a b" data-x=\\\'1\\\' hidden><p>1 &lt; 2 &amp; '
                 '3</p><!-- коммент --><br><img src=a.png alt=""><INPUT type=text disabled></div>\');\n'
                 'console.log(dump(f));\n'
                 'console.log(f.type, f.children[0].parent === f, f.children[0].children[0].parent === '
                 'f.children[0]);\n'
                 'console.log(dump(parseHTML("текст <b>жирный <i>курсив</b> хвост</i>")));\n'
                 'console.log(dump(parseHTML("</div><p>лишний закрывающий</p><span>незакрытый")));\n'
                 'console.log(parseHTML("").children.length);\n',
       'hint': 'Один проход регулярным выражением: комментарий, закрывающий тег, открывающий тег с '
               'атрибутами, текст; стек открытых элементов.',
       'expected': ['div{"id":"main","class":"a b","data-x":"1","hidden":true}',
                    '  p{}',
                    '    "1 < 2 & 3"',
                    '  br{}',
                    '  img{"src":"a.png","alt":""}',
                    '  input{"type":"text","disabled":true}',
                    'fragment true true',
                    '"текст "',
                    'b{}',
                    '  "жирный "',
                    '  i{}',
                    '    "курсив"',
                    '" хвост"',
                    'p{}',
                    '  "лишний закрывающий"',
                    'span{}',
                    '  "незакрытый"',
                    '0']},
      {'id': 'j14-selector-parse',
       'mode': 'js',
       'title': 'Разбор CSS-селектора',
       'statement': 'Напишите функцию parseSelector(str): поддерживаются составные селекторы: тег, #id, '
                    '.класс (несколько), [атрибут], [атрибут=значение] (значение в кавычках или без), * и '
                    'комбинаторы: пробел (потомок), > (ребёнок), + (следующий сосед); запятая — список. '
                    'Результат: массив альтернатив; альтернатива — массив шагов { combinator: " " | ">" | '
                    '"+" | null (для первого), tag?, id?, classes: [], attrs: [{ name, value? }] }. Для '
                    'некорректного селектора бросьте SyntaxError.',
       'starter': 'function parseSelector(str) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const show = (s) => { try { console.log(JSON.stringify(canon(parseSelector(s)))); } catch '
                 '(e) { console.log(e.name, e.message); } };\n'
                 'show("div");\n'
                 'show("ul > li.item.done");\n'
                 'show("nav a[href=\'/b\']:");\n'
                 'show("#root .menu a, p.note");\n'
                 'show("input[type=text][disabled]");\n'
                 'show("h1 + p");\n'
                 'show("*");\n'
                 'show("a >");\n'
                 'show("> a");\n'
                 'show("");\n',
       'hint': 'Разбейте на альтернативы по запятым, на шаги по комбинаторам, а составной селектор '
               'разбирайте регулярными выражениями по префиксу.',
       'expected': ['[[{"attrs":[],"classes":[],"combinator":null,"tag":"div"}]]',
                    '[[{"attrs":[],"classes":[],"combinator":null,"tag":"ul"},{"attrs":[],"classes":["item","done"],"combinator":">","tag":"li"}]]',
                    "SyntaxError Неверный селектор: a[href='/b']:",
                    '[[{"attrs":[],"classes":[],"combinator":null,"id":"root"},{"attrs":[],"classes":["menu"],"combinator":" '
                    '"},{"attrs":[],"classes":[],"combinator":" '
                    '","tag":"a"}],[{"attrs":[],"classes":["note"],"combinator":null,"tag":"p"}]]',
                    '[[{"attrs":[{"name":"type","value":"text"},{"name":"disabled"}],"classes":[],"combinator":null,"tag":"input"}]]',
                    '[[{"attrs":[],"classes":[],"combinator":null,"tag":"h1"},{"attrs":[],"classes":[],"combinator":"+","tag":"p"}]]',
                    '[[{"attrs":[],"classes":[],"combinator":null}]]',
                    'SyntaxError Комбинатор без правой части',
                    'SyntaxError Лишний комбинатор',
                    'SyntaxError Пустой селектор']},
      {'id': 'j14-matches',
       'mode': 'js',
       'title': 'matches и querySelectorAll',
       'statement': 'Селектор — уже разобранный список альтернатив (как в предыдущей задаче; формат: [[{ '
                    'combinator, tag?, id?, classes, attrs }, …], …]). Напишите matches(node, '
                    'selectorAlternatives) (узел-элемент подходит, если подходит хотя бы одна альтернатива; '
                    'комбинаторы: " " — потомок, ">" — ребёнок, "+" — непосредственный следующий '
                    'сосед-элемент) и querySelectorAll(root, selectorAlternatives) → элементы-потомки root '
                    '(сам root не включается) в порядке документа; querySelector — первый или null.',
       'starter': 'function matches(node, alts) {\n'
                  '}\n'
                  'function querySelectorAll(root, alts) {\n'
                  '}\n'
                  'function querySelector(root, alts) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const S = (tag, extra = {}) => ({ combinator: null, tag, classes: [], attrs: [], ...extra '
                 '});\n'
                 'const desc = (t, e = {}) => ({ ...S(t, e), combinator: " " }), child = (t, e = {}) => ({ '
                 '...S(t, e), combinator: ">" }), adj = (t, e = {}) => ({ ...S(t, e), combinator: "+" });\n'
                 'const root = page();\n'
                 'const q = (alts) => names(querySelectorAll(root, alts));\n'
                 'console.log(q([[S("li")]]));\n'
                 'console.log(q([[S("ul", { id: "list" }), child("li", { classes: ["item"] })]]));\n'
                 'console.log(q([[S("main"), desc("span")]]));\n'
                 'console.log(q([[S("header"), child("a")]]), "|", q([[S("nav"), child("a")]]));\n'
                 'console.log(q([[S("li", { classes: ["item", "done"] })], [S("p")]]));\n'
                 'console.log(q([[S("a", { attrs: [{ name: "href", value: "/b" }] })]]), "|", q([[S("a", { '
                 'attrs: [{ name: "href" }] })]]));\n'
                 'console.log(q([[S("a", { classes: ["link"] }), adj("a")]]), "|", q([[S("ul"), adj("p")]]), '
                 '"|", q([[S("h1"), adj("nav")]]));\n'
                 'const first = querySelector(root, [[S("li")]]);\n'
                 'console.log(first.children[0].text, querySelector(root, [[S("section")]]), matches(first, '
                 '[[S("ul"), child("li")]]), matches(first, [[S("div"), child("li")]]), matches(root, '
                 '[[S("div", { id: "root" })]]));\n'
                 'console.log(q([[S("div", { id: "root" })]]));\n',
       'hint': 'Сопоставляйте селектор справа налево: сначала последний шаг с самим узлом, затем комбинатор '
               'ведёт к родителю/предку/соседу.',
       'expected': ['li.item li.item.done li.item',
                    'li.item li.item.done li.item',
                    'span',
                    ' | a.link.active a.link',
                    'li.item.done p.note',
                    'a.link | a.link.active a.link',
                    'a.link | p.note | nav.menu',
                    'один null true false true']},
      {'id': 'j14-closest-delegate',
       'mode': 'js',
       'title': 'closest и делегирование',
       'statement': 'Напишите функции closest(node, pred) (сам узел или ближайший предок, для которого '
                    'pred(n) истинно; иначе null) и findTarget(node, root, pred): поднимается от node до '
                    'root (включительно не нужно: root исключается) и возвращает ближайший узел, для '
                    'которого pred истинно, но только если он лежит внутри root; иначе null. И функцию '
                    'path(node) → массив тегов от корня к узлу (для отладки).',
       'starter': 'function closest(node, pred) {\n'
                  '}\n'
                  'function findTarget(node, root, pred) {\n'
                  '}\n'
                  'function tagPath(node) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const root = page();\n'
                 'const list = root.children[1].children[0];\n'
                 'const span = list.children[2].children[0];\n'
                 'const text = span.children[0];\n'
                 'const isLi = (n) => n.tag === "li";\n'
                 'console.log(closest(span, isLi).attrs.class, closest(list.children[0], isLi) === '
                 'list.children[0], closest(text, isLi) === list.children[2], closest(text, (n) => n.tag === '
                 '"table"), closest(root, (n) => n.tag === "div") === root);\n'
                 'console.log(findTarget(text, list, isLi) === list.children[2], findTarget(text, '
                 'list.children[2], isLi), findTarget(text, root, (n) => n.tag === "header"), '
                 'findTarget(root.children[0].children[0], list, isLi));\n'
                 'console.log(tagPath(text).join(">"), tagPath(root).join(">"));\n',
       'hint': 'Подъём по parent в цикле; для делегирования остановитесь на root.',
       'expected': ['item true true null true', 'true null null null', 'div>main>ul>li>span>#text div']},
      {'id': 'j14-live-collection',
       'mode': 'js',
       'title': 'Живая коллекция',
       'statement': 'Напишите функцию getElementsByClassName(root, cls) → объект-«живая» коллекция: свойство '
                    'length и метод item(i), а также [Symbol.iterator]; при каждом обращении она заново ищет '
                    'элементы-потомки root (в порядке документа) с классом cls, поэтому отражает изменения '
                    'дерева. И snapshot(root, cls) → обычный массив на момент вызова.',
       'starter': 'function getElementsByClassName(root, cls) {\n}\nfunction snapshot(root, cls) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const root = page();\n'
                 'const list = root.children[1].children[0];\n'
                 'const live = getElementsByClassName(root, "item");\n'
                 'const snap = snapshot(root, "item");\n'
                 'console.log(live.length, snap.length, live.item(1).children[0].text, live.item(9));\n'
                 'const li = el("li", { class: "item" }, "четыре");\n'
                 'li.parent = list; list.children.push(li);\n'
                 'console.log(live.length, snap.length, [...live].map((n) => n.children[0].text ?? '
                 '"?").join());\n'
                 'list.children.shift().parent = null;\n'
                 'console.log(live.length, snap.length, live.item(0).children[0].text);\n'
                 'console.log(getElementsByClassName(root, "nothing").length, getElementsByClassName(root, '
                 '"link").length);\n',
       'hint': 'Каждый раз пересчитывайте список через обход дерева.',
       'expected': ['3 3 два null', '4 3 один,два,?,четыре', '3 3 два', '0 2']},
      {'id': 'j14-classlist',
       'mode': 'js',
       'title': 'classList',
       'statement': 'Напишите функцию classList(el) → объект с методами add(...names), remove(...names), '
                    'toggle(name, force?) (возвращает итоговое наличие), contains(name), replace(old, new) '
                    '(true/false), item(i), length и toString(); хранит состояние прямо в el.attrs.class '
                    '(строка, имена через пробел, без дубликатов; порядок добавления сохраняется). Пустое '
                    'имя или имя с пробелом — бросьте SyntaxError.',
       'starter': 'function classList(el) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const e = el("div", { class: "a  b" });\n'
                 'const cl = classList(e);\n'
                 'cl.add("c", "a", "d");\n'
                 'console.log(e.attrs.class, cl.length, cl.contains("b"), cl.contains("z"), cl.item(2), '
                 'cl.item(9));\n'
                 'cl.remove("b", "zzz"); console.log(String(cl));\n'
                 'console.log(cl.toggle("x"), cl.toggle("x"), cl.toggle("y", true), cl.toggle("y", true), '
                 'cl.toggle("a", false), cl.toggle("q", false), String(cl));\n'
                 'console.log(cl.replace("c", "C"), cl.replace("zz", "k"), cl.replace("d", "C"), '
                 'String(cl));\n'
                 'const bare = el("p", {});\n'
                 'classList(bare).add("one");\n'
                 'console.log(bare.attrs.class);\n'
                 'for (const bad of ["", "a b"]) { try { cl.add(bad); } catch (x) { console.log(x.name); } '
                 '}\n',
       'hint': 'Состояние — строка в el.attrs.class: разбирайте и собирайте при каждой операции.',
       'expected': ['a b c d 4 true false c null',
                    'a c d',
                    'true false true true false false c d y',
                    'true false true C y',
                    'one',
                    'SyntaxError',
                    'SyntaxError']},
      {'id': 'j14-dataset',
       'mode': 'js',
       'title': 'dataset и имена атрибутов',
       'statement': 'Напишите функции toDataAttr(prop) («userId» → «data-user-id»), fromDataAttr(attr) '
                    '(«data-user-id» → «userId»; для не data-атрибута — null) и dataset(el) → объект-прокси: '
                    'чтение/запись/удаление свойств (user.id → атрибут data-user-id), перечисление ключей '
                    '(Object.keys) — только data-атрибутов в порядке атрибутов; значения — строки (запись '
                    'приводит к строке).',
       'starter': 'function toDataAttr(prop) {\n'
                  '}\n'
                  'function fromDataAttr(attr) {\n'
                  '}\n'
                  'function dataset(el) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'console.log(toDataAttr("userId"), toDataAttr("id"), toDataAttr("someLongName"), '
                 'fromDataAttr("data-user-id"), fromDataAttr("data-x"), fromDataAttr("class"), '
                 'fromDataAttr("data-"));\n'
                 'const e = el("div", { id: "x", "data-user-id": "7", class: "c", "data-theme-color": "red" '
                 '});\n'
                 'const d = dataset(e);\n'
                 'console.log(d.userId, d.themeColor, d.nope, "userId" in d, "id" in d, '
                 'JSON.stringify(Object.keys(d)));\n'
                 'd.count = 5; d.userId = 8;\n'
                 'console.log(e.attrs["data-count"], typeof e.attrs["data-count"], e.attrs["data-user-id"], '
                 'JSON.stringify(Object.keys(d)));\n'
                 'delete d.themeColor;\n'
                 'console.log(JSON.stringify(e.attrs), JSON.stringify({ ...d }));\n',
       'hint': 'Proxy с ловушками get/set/deleteProperty/has/ownKeys.',
       'expected': ['data-user-id data-id data-some-long-name userId x null',
                    '7 red undefined true false ["userId","themeColor"]',
                    '5 string 8 ["userId","themeColor","count"]',
                    '{"id":"x","data-user-id":"8","class":"c","data-count":"5"} {"userId":"8","count":"5"}']},
      {'id': 'j14-style',
       'mode': 'js',
       'title': 'style: разбор и сборка cssText',
       'statement': 'Напишите функции parseStyle(cssText) → объект { свойство: значение } (свойства с '
                    'дефисами в camelCase: font-size → fontSize; пробелы по краям обрезаются; пустые '
                    'объявления пропускаются; значения с «;» внутри кавычек и url(…) учитывайте), '
                    'stringifyStyle(obj) → «font-size: 12px; color: red;» (camelCase → дефисы, объявления '
                    'через пробел, в конце «;»; значения null/undefined/пустые пропускаются) и setStyle(el, '
                    'prop, value) (изменяет el.attrs.style, пустое значение удаляет свойство).',
       'starter': 'function parseStyle(cssText) {\n'
                  '}\n'
                  'function stringifyStyle(obj) {\n'
                  '}\n'
                  'function setStyle(el, prop, value) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'console.log(JSON.stringify(parseStyle("font-size: 12px; COLOR:red;; background-image: '
                 'url(a;b.png); content: \'x;y\'; margin:0 auto ;")));\n'
                 'console.log(JSON.stringify(parseStyle("")), JSON.stringify(parseStyle("bad; : x; y:")));\n'
                 'console.log(stringifyStyle({ fontSize: "12px", color: "red", zIndex: 3, empty: "", n: null '
                 '}), "|", JSON.stringify(stringifyStyle({})));\n'
                 'const e = el("p", { style: "color: red; margin: 0" });\n'
                 'setStyle(e, "fontSize", "14px"); console.log(e.attrs.style);\n'
                 'setStyle(e, "color", ""); console.log(e.attrs.style);\n'
                 'setStyle(e, "margin", "1em 2em"); setStyle(e, "margin", ""); setStyle(e, "fontSize", ""); '
                 'console.log(JSON.stringify(e.attrs.style));\n'
                 'const f = el("p", {}); setStyle(f, "width", 100); console.log(f.attrs.style);\n',
       'hint': 'Не режьте по «;» вслепую: учитывайте кавычки и скобки (регулярное выражение с '
               'альтернативами).',
       'expected': ['{"fontSize":"12px","COLOR":"red","backgroundImage":"url(a;b.png)","content":"\'x;y\'","margin":"0 '
                    'auto"}',
                    '{} {}',
                    'font-size: 12px; color: red; z-index: 3; | ""',
                    'color: red; margin: 0; font-size: 14px;',
                    'margin: 0; font-size: 14px;',
                    '""',
                    'width: 100;']},
      {'id': 'j14-attr-prop',
       'mode': 'js',
       'title': 'Атрибуты и свойства',
       'statement': 'Напишите функцию reflect(el) → объект-«представление» DOM-свойств над атрибутами: id '
                    '(строка, читает/пишет attrs.id; по умолчанию ""), className (строка из attrs.class), '
                    'disabled и checked (булевы: чтение — есть ли атрибут (true или любая строка) / запись '
                    'true — атрибут true, false — атрибут удаляется), href (для a: абсолютный адрес — '
                    'разрешите относительный через new URL(attr, "https://example.com/dir/page"); без '
                    'атрибута ""), tabIndex (число из attrs.tabindex; по умолчанию 0 для button/a/input и -1 '
                    'для остальных). Исходные attrs меняются при записи.',
       'starter': 'function reflect(el) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const a = el("a", { href: "../x/y?q=1#h", class: "link", tabindex: "3" });\n'
                 'const p = reflect(a);\n'
                 'console.log(p.href, p.className, p.tabIndex, p.id === "", p.disabled);\n'
                 'const b = el("button", { disabled: "disabled" });\n'
                 'const pb = reflect(b);\n'
                 'console.log(pb.disabled, pb.tabIndex, pb.checked);\n'
                 'pb.disabled = false; pb.checked = true; pb.id = "go"; pb.className = "btn primary";\n'
                 'console.log(JSON.stringify(b.attrs), pb.disabled, pb.checked);\n'
                 'pb.disabled = true; console.log(b.attrs.disabled);\n'
                 'console.log(reflect(el("a", { href: "/abs" })).href, reflect(el("a", { href: '
                 '"https://other.org/z" })).href, reflect(el("a", {})).href === "", reflect(el("div", '
                 '{})).tabIndex, reflect(el("input", {})).tabIndex);\n',
       'hint': 'Это геттеры и сеттеры над el.attrs; булевы — по наличию.',
       'expected': ['https://example.com/x/y?q=1#h link 3 true false',
                    'true 0 false',
                    '{"checked":true,"id":"go","class":"btn primary"} false true',
                    'true',
                    'https://example.com/abs https://other.org/z true -1 0']},
      {'id': 'j14-fragment',
       'mode': 'js',
       'title': 'DocumentFragment и replaceWith',
       'statement': 'Напишите функции: createFragment(...nodes) (узел { type: "fragment", children, parent: '
                    'null }; дети получают parent = фрагмент), appendFragment(parent, frag) (переносит всех '
                    'детей фрагмента в конец parent; фрагмент остаётся пустым; возвращает число '
                    'вставленных), append(parent, ...items) (items — узлы, строки (→ текстовые узлы) или '
                    'фрагменты (разворачиваются)), before(node, ...items), after(node, ...items), '
                    'replaceWith(node, ...items), remove(node). Все операции поддерживают parent-связи и '
                    'перенос узла из прежнего места.',
       'starter': 'function createFragment(...nodes) {\n'
                  '}\n'
                  'function appendFragment(parent, frag) {\n'
                  '}\n'
                  'function append(parent, ...items) {\n'
                  '}\n'
                  'function before(node, ...items) {\n'
                  '}\n'
                  'function after(node, ...items) {\n'
                  '}\n'
                  'function replaceWith(node, ...items) {\n'
                  '}\n'
                  'function remove(node) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const ul = el("ul", {}, el("li", {}, "a"), el("li", {}, "d"));\n'
                 'const frag = createFragment(el("li", {}, "b"), el("li", {}, "c"));\n'
                 'console.log(frag.type, frag.children.length, frag.children[0].parent === frag);\n'
                 'const [d] = [ul.children[1]];\n'
                 'before(d, frag);\n'
                 'const order = () => ul.children.map((n) => (n.type === "text" ? "\'" + n.text + "\'" : '
                 'n.children[0].text)).join("");\n'
                 'console.log(order(), frag.children.length, ul.children.every((n) => n.parent === ul));\n'
                 'const f2 = createFragment(el("li", {}, "x"), el("li", {}, "y"));\n'
                 'console.log(appendFragment(ul, f2), order(), f2.children.length);\n'
                 'append(ul, "текст", createFragment(el("li", {}, "z")));\n'
                 'after(ul.children[0], "!");\n'
                 'console.log(order());\n'
                 'replaceWith(ul.children[1], el("li", {}, "A"), "?");\n'
                 'console.log(order());\n'
                 'remove(ul.children[0]); console.log(order());\n'
                 'const li = ul.children[ul.children.length - 1];\n'
                 'const other = el("ol", {}); append(other, li);\n'
                 'console.log(order(), other.children.length, li.parent === other);\n',
       'hint': 'Единый helper detach и insertAt; фрагмент «разворачивается» и опустошается.',
       'expected': ['fragment 2 true',
                    'abcd 0 true',
                    '2 abcdxy 0',
                    "a'!'bcdxy'текст'z",
                    "aA'?'bcdxy'текст'z",
                    "A'?'bcdxy'текст'z",
                    "A'?'bcdxy'текст' 1 true"]},
      {'id': 'j14-clone',
       'mode': 'js',
       'title': 'cloneNode',
       'statement': 'Напишите функцию cloneNode(node, deep = false): создаёт копию узла: тот же '
                    'тип/тег/текст, копия attrs (независимый объект), parent = null; при deep = true '
                    'копируются и потомки (с корректными parent), иначе — без детей. Пользовательские поля, '
                    'начинающиеся на «on» (обработчики, например onclick), не копируются. Затем '
                    'isEqualNode(a, b) → структурное равенство (тип, тег, attrs, дети, текст; parent не '
                    'учитывается).',
       'starter': 'function cloneNode(node, deep) {\n}\nfunction isEqualNode(a, b) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const src = el("li", { class: "item", id: "x" }, "текст ", el("b", {}, "жирный"));\n'
                 'src.onclick = () => 1;\n'
                 'const shallow = cloneNode(src), deep = cloneNode(src, true);\n'
                 'console.log(shallow.children.length, deep.children.length, shallow.parent, '
                 'deep.children[1].parent === deep, deep.onclick, shallow.attrs !== src.attrs);\n'
                 'deep.attrs.class = "changed"; deep.children[1].children[0].text = "другой";\n'
                 'console.log(src.attrs.class, src.children[1].children[0].text);\n'
                 'console.log(isEqualNode(src, cloneNode(src, true)), isEqualNode(src, deep), '
                 'isEqualNode(src, shallow), isEqualNode(tx("a"), tx("a")), isEqualNode(tx("a"), el("a")));\n'
                 'console.log(isEqualNode(el("p", { a: "1", b: "2" }), el("p", { b: "2", a: "1" })), '
                 'isEqualNode(el("p", {}, "a"), el("p", {}, "a", "")));\n',
       'hint': 'Копируйте attrs spread-ом; для deep — рекурсивный клон детей с установкой parent.',
       'expected': ['0 2 null true undefined true',
                    'item жирный',
                    'true false false true false',
                    'true false']},
      {'id': 'j14-document-position',
       'mode': 'js',
       'title': 'contains и compareDocumentPosition',
       'statement': 'Напишите функции contains(a, b) (b — потомок a или сам a), compareDocumentPosition(a, '
                    'b) → битовая маска как в DOM относительно a: 1 — разные деревья, 2 — b предшествует a, '
                    '4 — b следует за a, 8 — b содержит a (b — предок), 16 — b содержится в a (потомок); '
                    'предок/потомок комбинируются: b предок a → 8 | 2 = 10, b потомок a → 16 | 4 = 20; для a '
                    '=== b → 0. И sortDocumentOrder(nodes) → новый массив в порядке документа (узлы одного '
                    'дерева).',
       'starter': 'function contains(a, b) {\n'
                  '}\n'
                  'function compareDocumentPosition(a, b) {\n'
                  '}\n'
                  'function sortDocumentOrder(nodes) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const root = page();\n'
                 'const header = root.children[0], h1 = header.children[0], nav = header.children[1], a1 = '
                 'nav.children[0];\n'
                 'const main = root.children[1], list = main.children[0], li3 = list.children[2], span = '
                 'li3.children[0], note = main.children[1];\n'
                 'console.log(contains(root, span), contains(span, root), contains(span, span), '
                 'contains(list, note));\n'
                 'console.log(compareDocumentPosition(h1, nav), compareDocumentPosition(nav, h1), '
                 'compareDocumentPosition(a1, header), compareDocumentPosition(header, a1), '
                 'compareDocumentPosition(span, span), compareDocumentPosition(a1, note), '
                 'compareDocumentPosition(note, a1));\n'
                 'console.log(compareDocumentPosition(h1, el("div")), compareDocumentPosition(root, span), '
                 'compareDocumentPosition(span, root));\n'
                 'console.log(names(sortDocumentOrder([note, span, a1, root, h1, list, li3])));\n',
       'hint': 'Сравните цепочки предков: найдите первое расхождение и сравните индексы братьев.',
       'expected': ['true false true false',
                    '4 2 10 20 0 4 2',
                    '1 20 10',
                    'div#root.app h1 a.link.active ul#list li.item span p.note']},
      {'id': 'j14-tree-walker',
       'mode': 'js',
       'title': 'TreeWalker с фильтром',
       'statement': 'Напишите функцию createTreeWalker(root, whatToShow, filter): whatToShow — маска (1 — '
                    'элементы, 4 — текст; 5 — оба; 0xFFFFFFFF — все); filter(node) → "accept" (1), "reject" '
                    '(2: узел и всё его поддерево пропускаются) или "skip" (3: сам узел пропускается, '
                    'потомки рассматриваются); filter необязателен. Возвращает объект с currentNode (сначала '
                    'root) и методами nextNode() (следующий принятый узел в порядке документа внутри root, '
                    'либо null — currentNode не меняется), reset().',
       'starter': 'function createTreeWalker(root, whatToShow, filter) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const root = page();\n'
                 'const collect = (w) => { const out = []; for (let n; (n = w.nextNode()); ) out.push(n.type '
                 '=== "text" ? JSON.stringify(n.text) : n.tag); return out.join(" "); };\n'
                 'console.log(collect(createTreeWalker(root, 1)));\n'
                 'console.log(collect(createTreeWalker(root, 4)));\n'
                 'console.log(collect(createTreeWalker(root, 5, (n) => (n.type === "element" && n.tag === '
                 '"nav" ? "reject" : "accept"))));\n'
                 'console.log(collect(createTreeWalker(root, 1, (n) => (n.tag === "ul" || n.tag === "main" ? '
                 '"skip" : "accept"))));\n'
                 'console.log(collect(createTreeWalker(root, 4, (n) => (n.text.length > 3 ? "accept" : '
                 '"skip"))));\n'
                 'const w = createTreeWalker(root, 1, (n) => (n.tag === "li" ? "accept" : "skip"));\n'
                 'console.log(w.currentNode === root, w.nextNode().attrs.class, w.currentNode.attrs.class, '
                 'w.nextNode().attrs.class);\n'
                 'w.nextNode(); console.log(w.nextNode(), w.currentNode.children[0].tag);\n'
                 'w.reset(); console.log(w.currentNode === root, w.nextNode().children[0].text);\n'
                 'console.log(collect(createTreeWalker(el("div"), 0xffffffff)), '
                 'collect(createTreeWalker(el("p", {}, "т", el("b", {}), "у"), 0xffffffff)));\n',
       'hint': 'Обход в порядке документа с учётом вердиктов: reject пропускает поддерево, skip — только '
               'узел.',
       'expected': ['header h1 nav a a main ul li li li span p',
                    '"Заголовок" "А" "Б" "один" "два" "три" "заметка"',
                    'header h1 "Заголовок" main ul li "один" li "два" li span "три" p "заметка"',
                    'header h1 nav a a li li li span p',
                    '"Заголовок" "один" "заметка"',
                    'true item item item done',
                    'null span',
                    'true один',
                    ' "т" b "у"']},
      {'id': 'j14-insert-adjacent',
       'mode': 'js',
       'title': 'insertAdjacentHTML',
       'statement': 'Дана функция parse(html) → массив узлов (определена в тестовом окружении, разбирает '
                    'разметку). Напишите insertAdjacent(el, position, html): position — «beforebegin» (перед '
                    'el в родителе), «afterbegin» (первыми детьми el), «beforeend» (последними), «afterend» '
                    '(после el в родителе). Для beforebegin/afterend без родителя бросьте Error("нет '
                    'родителя"); неизвестная позиция — SyntaxError. Все parent-связи должны быть корректны.',
       'starter': 'function insertAdjacent(el, position, html) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'function parse(html) {\n'
                 '  const root = { type: "fragment", children: [] };\n'
                 '  const stack = [root];\n'
                 '  for (const m of html.matchAll(/<\\/(\\w+)>|<(\\w+)>|([^<]+)/g)) {\n'
                 '    const top = stack.at(-1);\n'
                 '    if (m[3] !== undefined) top.children.push({ type: "text", text: m[3], parent: top });\n'
                 '    else if (m[1]) stack.pop();\n'
                 '    else { const n = { type: "element", tag: m[2], attrs: {}, children: [], parent: top }; '
                 'top.children.push(n); if (m[2] !== "br") stack.push(n); }\n'
                 '  }\n'
                 '  return root.children;\n'
                 '}\n'
                 'const ul = el("ul", {}, el("li", {}, "середина"));\n'
                 'const outer = el("div", {}, ul);\n'
                 'const show = () => outer.children.map((n) => n.tag).join() + " / " + ul.children.map((n) '
                 '=> n.tag + ":" + (n.children[0]?.text ?? "")).join();\n'
                 'insertAdjacent(ul, "afterbegin", "<li>первый</li>");\n'
                 'insertAdjacent(ul, "beforeend", "<li>последний</li><li>ещё</li>");\n'
                 'console.log(show());\n'
                 'insertAdjacent(ul, "beforebegin", "<h2>до</h2>"); insertAdjacent(ul, "afterend", "<p>после '
                 '<b>жирный</b></p>");\n'
                 'console.log(show(), outer.children.every((n) => n.parent === outer), ul.children.every((n) '
                 '=> n.parent === ul));\n'
                 'console.log(outer.children[2].children[1].parent === outer.children[2]);\n'
                 'for (const f of [() => insertAdjacent(outer, "beforebegin", "<i>x</i>"), () => '
                 'insertAdjacent(outer, "inside", "<i>x</i>")]) { try { f(); } catch (e) { '
                 'console.log(e.name, e.message); } }\n'
                 'insertAdjacent(outer, "beforeend", "голый текст"); '
                 'console.log(outer.children.at(-1).text);\n',
       'hint': 'Разберите html, затем вставьте узлы в нужное место и проставьте parent.',
       'expected': ['ul / li:первый,li:середина,li:последний,li:ещё',
                    'h2,ul,p / li:первый,li:середина,li:последний,li:ещё true true',
                    'true',
                    'Error нет родителя',
                    'SyntaxError Неизвестная позиция',
                    'голый текст']},
      {'id': 'j14-template',
       'mode': 'js',
       'title': 'Шаблон с подстановкой',
       'statement': 'Напишите функцию render(template, data): в строке шаблона {{путь}} заменяется значением '
                    'из data по пути через точку («user.name», «items.0»); значения экранируются как текст '
                    'HTML (&, <, >, "); {{{путь}}} — без экранирования; если значения нет (undefined/null) — '
                    'пустая строка; пробелы внутри скобок допустимы: «{{ user.name }}». Блоки {{#each '
                    'список}}…{{/each}} повторяют содержимое для каждого элемента (внутри доступен {{this}} '
                    'и поля элемента; индекс — {{@index}}).',
       'starter': 'function render(template, data) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const data = { user: { name: "Ада <b>", site: "<a href=\'x\'>сайт</a>" }, items: ["один", '
                 '"два & три"], people: [{ n: "Борис", age: 30 }, { n: "Вера", age: 25 }], title: "Привет", '
                 'empty: null };\n'
                 'console.log(render("{{title}}, {{ user.name }}!", data));\n'
                 'console.log(render("{{{user.site}}} | {{user.site}}", data));\n'
                 'console.log(render("{{items.1}} {{nope}}{{empty}}{{user.zzz.q}}.", data));\n'
                 'console.log(render("<ul>{{#each items}}<li>{{@index}}: {{this}}</li>{{/each}}</ul>", '
                 'data));\n'
                 'console.log(render("{{#each people}}{{n}} ({{age}}); {{/each}}", data));\n'
                 'console.log(render("{{#each missing}}x{{/each}}пусто", data), render("без подстановок", '
                 'data));\n',
       'hint': 'Регулярные выражения для блоков each и для подстановок; экранирование — для двойных скобок.',
       'expected': ['Привет, Ада &lt;b&gt;!',
                    "<a href='x'>сайт</a> | &lt;a href='x'&gt;сайт&lt;/a&gt;",
                    'два &amp; три .',
                    '<ul><li>0: один</li><li>1: два &amp; три</li></ul>',
                    'Борис (30); Вера (25);',
                    'пусто без подстановок']},
      {'id': 'j14-sanitize',
       'mode': 'js',
       'title': 'Санитайзер HTML',
       'statement': 'Напишите функцию sanitize(nodes, { allowedTags, allowedAttrs }): nodes — массив узлов '
                    '(элементы { type, tag, attrs, children }, текст { type: "text", text }); возвращает '
                    'новое дерево, из которого убрано всё лишнее: элементы с тегом не из allowedTags '
                    'заменяются своими (очищенными) потомками; script, style и iframe удаляются вместе с '
                    'содержимым; атрибуты не из allowedAttrs[tag] ∪ allowedAttrs["*"] удаляются; атрибуты, '
                    'начинающиеся на «on», удаляются всегда; в href и src значения со схемой javascript:, '
                    'data: и vbscript: (без учёта регистра, пробелов и управляющих символов) — удаляются. '
                    'Исходные узлы не меняются.',
       'starter': 'function sanitize(nodes, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const E = (tag, attrs = {}, ...children) => ({ type: "element", tag, attrs, children: '
                 'children.map((c) => (typeof c === "string" ? { type: "text", text: c } : c)) });\n'
                 'const ser = (n) => (n.type === "text" ? n.text : '
                 '`<${n.tag}${Object.entries(n.attrs).map(([k, v]) => ` '
                 '${k}="${v}"`).join("")}>${n.children.map(ser).join("")}</${n.tag}>`);\n'
                 'const opts = { allowedTags: ["p", "a", "b", "img", "div"], allowedAttrs: { a: ["href", '
                 '"title"], img: ["src", "alt"], "*": ["class"] } };\n'
                 'const dirty = [E("p", { class: "x", onclick: "steal()", style: "color:red" }, "привет ", '
                 'E("script", {}, "alert(1)"), E("b", {}, "жирный"), E("font", { color: "red" }, "шрифт ", '
                 'E("i", {}, "курсив"))), E("a", { href: " JaVaScript:alert(1)", title: "t" }, "ссылка"), '
                 'E("a", { href: "https://ok.ru/" }, "ок"), E("img", { src: "data:text/html,x", alt: "a", '
                 'onerror: "x()" }), E("iframe", { src: "evil" }, "x"), "голый текст"];\n'
                 'const orig = JSON.stringify(dirty);\n'
                 'console.log(sanitize(dirty, opts).map(ser).join("\\n"));\n'
                 'console.log(orig === JSON.stringify(dirty), JSON.stringify(sanitize([], opts)));\n'
                 'console.log(sanitize([E("div", { class: "a", id: "i" }, E("span", {}, E("em", {}, '
                 '"глубоко")))], opts).map(ser).join());\n',
       'hint': 'Рекурсивно: тег вне белого списка заменяется потомками, опасные атрибуты отбрасываются.',
       'expected': ['<p class="x">привет <b>жирный</b>шрифт курсив</p>',
                    '<a title="t">ссылка</a>',
                    '<a href="https://ok.ru/">ок</a>',
                    '<img alt="a"></img>',
                    'true []',
                    '<div class="a">глубоко</div>']},
      {'id': 'j14-tree-diff',
       'mode': 'js',
       'title': 'Различие двух деревьев',
       'statement': 'Напишите функцию diffTrees(a, b): деревья описаны так же, как в предыдущих задачах '
                    '(элементы { type, tag, attrs, children }, текст { type: "text", text }); возвращает '
                    'список операций в порядке обхода: { op: "replace", path } (другой тип или тег — '
                    'заменить узел целиком), { op: "text", path, text } (изменился текст), { op: "setAttr", '
                    'path, name, value }, { op: "removeAttr", path, name }, { op: "append", path (родитель), '
                    'index, node } (b имеет больше детей), { op: "remove", path (родитель), index } (меньше; '
                    'удалять с конца). Путь — массив индексов детей от корня. Дети сравниваются по позициям.',
       'starter': 'function diffTrees(a, b) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const E = (tag, attrs = {}, ...children) => ({ type: "element", tag, attrs, children: '
                 'children.map((c) => (typeof c === "string" ? { type: "text", text: c } : c)) });\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const show = (a, b) => console.log(JSON.stringify(canon(diffTrees(a, b).map((o) => (o.node '
                 '? { ...o, node: o.node.type === "text" ? o.node.text : o.node.tag } : o)))));\n'
                 'show(E("p", {}, "а"), E("p", {}, "а"));\n'
                 'show(E("p", { class: "x" }, "а"), E("p", { class: "y", id: "i" }, "б"));\n'
                 'show(E("ul", {}, E("li", {}, "1"), E("li", {}, "2")), E("ul", {}, E("li", {}, "1"), '
                 'E("li", {}, "2"), E("li", {}, "3")));\n'
                 'show(E("ul", {}, E("li", {}, "1"), E("li", {}, "2"), E("li", {}, "3")), E("ul", {}, '
                 'E("li", {}, "1")));\n'
                 'show(E("div", {}, E("p", {}, "x")), E("div", {}, E("span", {}, "x")));\n'
                 'show(E("div", { a: "1", b: "2" }), E("div", { b: "2" }));\n'
                 'show(E("a", {}, "т"), { type: "text", text: "т" });\n',
       'hint': 'Рекурсия по позициям детей; для разных тегов — replace; лишние — append/remove.',
       'expected': ['[]',
                    '[{"name":"class","op":"setAttr","path":[],"value":"y"},{"name":"id","op":"setAttr","path":[],"value":"i"},{"op":"text","path":[0],"text":"б"}]',
                    '[{"index":2,"node":"li","op":"append","path":[]}]',
                    '[{"index":2,"op":"remove","path":[]},{"index":1,"op":"remove","path":[]}]',
                    '[{"op":"replace","path":[0]}]',
                    '[{"name":"a","op":"removeAttr","path":[]}]',
                    '[{"op":"replace","path":[]}]']},
      {'id': 'j14-mutation-records',
       'mode': 'js',
       'title': 'MutationObserver: записи изменений',
       'statement': 'Напишите функцию observe(root, options, callback): options = { childList?, attributes?, '
                    'characterData?, subtree? }; возвращает объект с методами setAttribute(node, name, '
                    'value), removeAttribute(node, name), appendChild(parent, child), removeChild(parent, '
                    'child), setText(textNode, text) — они меняют дерево и добавляют запись в очередь, если '
                    'узел находится под наблюдением (root или, при subtree, его потомок): { type: '
                    '"attributes"|"childList"|"characterData", target, attributeName?, oldValue? (для '
                    'attributes и characterData), addedNodes?, removedNodes? }. Записи доставляются пачкой '
                    'callback(records) как микрозадача (queueMicrotask) после текущего кода. Опции, которые '
                    'не включены, записей не создают.',
       'starter': 'function observe(root, options, callback) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const root = page();\n'
                 'const list = root.children[1].children[0];\n'
                 'const recs = [];\n'
                 'const o = observe(root, { childList: true, attributes: true, subtree: true }, (rs) => '
                 'recs.push(...rs.map((r) => `${r.type}:${r.target.tag ?? "#text"}${r.attributeName ? ":" + '
                 'r.attributeName + "(" + r.oldValue + ")" : ""}${r.addedNodes?.length ? "+" + '
                 'r.addedNodes.length : ""}${r.removedNodes?.length ? "-" + r.removedNodes.length : '
                 '""}`)));\n'
                 'o.setAttribute(list, "class", "big"); o.setAttribute(list, "class", "bigger"); '
                 'o.removeAttribute(list, "id");\n'
                 'o.appendChild(list, el("li", {}, "новый")); o.removeChild(list, list.children[0]);\n'
                 'o.setText(list.children[0].children[0], "изменён");\n'
                 'console.log(recs.length);\n'
                 'await Promise.resolve();\n'
                 'console.log(recs.join(" | "));\n'
                 'recs.length = 0;\n'
                 'const shallow = observe(list, { attributes: true }, (rs) => recs.push(rs.length));\n'
                 'shallow.setAttribute(list, "a", "1"); shallow.setAttribute(list.children[0], "b", "2"); '
                 'shallow.appendChild(list, el("li"));\n'
                 'await Promise.resolve();\n'
                 'console.log(JSON.stringify(recs));\n'
                 'const cd = observe(root, { characterData: true, subtree: true }, (rs) => '
                 'recs.push(rs.map((r) => r.oldValue).join()));\n'
                 'cd.setText(list.children[0].children[0], "ещё раз"); '
                 'cd.setText(list.children[0].children[0], "и ещё");\n'
                 'await Promise.resolve();\n'
                 'console.log(JSON.stringify(recs));\n',
       'hint': 'Очередь записей и один флаг запланированной доставки; проверка «под наблюдением» с учётом '
               'subtree.',
       'expected': ['0',
                    'attributes:ul:class(null) | attributes:ul:class(big) | attributes:ul:id(list) | '
                    'childList:ul+1 | childList:ul-1',
                    '[1]',
                    '[1,"изменён,ещё раз"]']},
      {'id': 'j14-intersection',
       'mode': 'js',
       'title': 'IntersectionObserver: расчёт видимости',
       'statement': 'Прямоугольники — { top, left, width, height }. Напишите функцию intersection(target, '
                    'viewport) → { isIntersecting, ratio, rect }: rect — пересечение (или нулевой '
                    'прямоугольник), ratio — площадь пересечения / площадь target (0 для нулевой площади), '
                    'isIntersecting — пересечение ненулевой площади или касание (граница совпала, площадь 0, '
                    'но ratio === 0 и стороны пересекаются включительно — считайте isIntersecting = true для '
                    'касания, как в спецификации). И функцию thresholdCrossings(ratios, thresholds): для '
                    'последовательности значений ratio — индексы, на которых пересечён хотя бы один порог '
                    '(изменился индекс «ведра» порогов относительно предыдущего значения; для первого '
                    'значения — всегда, если ratio > 0 или в наблюдателе первый вызов); возвращает массив '
                    'индексов значений, при которых колбэк вызывается.',
       'starter': 'function intersection(target, viewport) {\n'
                  '}\n'
                  'function thresholdCrossings(ratios, thresholds) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const vp = { top: 0, left: 0, width: 100, height: 100 };\n'
                 'for (const t of [{ top: 10, left: 10, width: 50, height: 50 }, { top: 80, left: 0, width: '
                 '100, height: 40 }, { top: 100, left: 0, width: 50, height: 50 }, { top: 150, left: 0, '
                 'width: 50, height: 50 }, { top: -50, left: -50, width: 100, height: 100 }, { top: 0, left: '
                 '0, width: 0, height: 0 }]) console.log(JSON.stringify(canon(intersection(t, vp))));\n'
                 'console.log(JSON.stringify(thresholdCrossings([0, 0.1, 0.3, 0.6, 0.55, 1, 0.9], [0, 0.5, '
                 '1])));\n'
                 'console.log(JSON.stringify(thresholdCrossings([0, 0, 0], [0, 0.5])), '
                 'JSON.stringify(thresholdCrossings([], [0])), JSON.stringify(thresholdCrossings([0.2, 0.4, '
                 '0.45], [0.25, 0.5])));\n',
       'hint': 'Пересечение — max левых/верхних и min правых/нижних границ; корзина порога — число порогов '
               'не больше ratio.',
       'expected': ['{"isIntersecting":true,"ratio":1,"rect":{"height":50,"left":10,"top":10,"width":50}}',
                    '{"isIntersecting":true,"ratio":0.5,"rect":{"height":20,"left":0,"top":80,"width":100}}',
                    '{"isIntersecting":true,"ratio":0,"rect":{"height":0,"left":0,"top":100,"width":50}}',
                    '{"isIntersecting":false,"ratio":0,"rect":{"height":0,"left":0,"top":0,"width":0}}',
                    '{"isIntersecting":true,"ratio":0.25,"rect":{"height":50,"left":0,"top":0,"width":50}}',
                    '{"isIntersecting":true,"ratio":0,"rect":{"height":0,"left":0,"top":0,"width":0}}',
                    '[0,3,5,6]',
                    '[0] [] [0,1]']},
      {'id': 'j14-resize',
       'mode': 'js',
       'title': 'ResizeObserver: изменения размеров',
       'statement': 'Напишите функцию createResizeObserver(callback): возвращает { observe(el, size), '
                    'unobserve(el), update(el, size), flush() }; size = { width, height }; update запоминает '
                    'новый размер, flush() вызывает callback(entries) один раз для всех наблюдаемых '
                    'элементов, размер которых изменился с прошлой доставки (при первом observe — всегда '
                    'доставляется начальный размер); entries — [{ target, contentRect: { width, height } }] '
                    'в порядке наблюдения; изменение менее чем на 0.5 px по каждой оси не считается '
                    'изменением. unobserve прекращает наблюдение.',
       'starter': 'function createResizeObserver(callback) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const log = [];\n'
                 'const ro = createResizeObserver((es) => log.push(es.map((e) => '
                 '`${e.target}:${e.contentRect.width}x${e.contentRect.height}`).join(",")));\n'
                 'ro.observe("a", { width: 100, height: 50 }); ro.observe("b", { width: 10, height: 10 });\n'
                 'ro.flush(); console.log(JSON.stringify(log));\n'
                 'ro.flush(); console.log(log.length);\n'
                 'ro.update("a", { width: 100.3, height: 50 }); ro.flush(); console.log(log.length);\n'
                 'ro.update("a", { width: 120, height: 50 }); ro.update("b", { width: 10, height: 20 }); '
                 'ro.flush(); console.log(log.at(-1));\n'
                 'ro.unobserve("b"); ro.update("a", { width: 130, height: 60 }); ro.update("b", { width: 1, '
                 'height: 1 }); ro.flush(); console.log(log.at(-1), log.length);\n'
                 'ro.update("a", { width: 130.4, height: 60.4 }); ro.flush(); console.log(log.length);\n'
                 'ro.update("a", { width: 130.6, height: 60 }); ro.flush(); console.log(log.at(-1));\n',
       'hint': 'Храните размер и последний доставленный размер; flush сравнивает их с допуском 0.5.',
       'expected': ['["a:100x50,b:10x10"]', '1', '1', 'a:120x50,b:10x20', 'a:130x60 3', '3', 'a:130.6x60']},
      {'id': 'j14-custom-elements',
       'mode': 'js',
       'title': 'Реестр Custom Elements',
       'statement': 'Напишите класс CustomElementRegistry: define(name, ctor) (имя — строчные буквы, цифры, '
                    'дефисы, обязательно с дефисом и не начинается с цифры; дубликат имени или конструктора '
                    '— Error «уже определён»; неверное имя — SyntaxError), get(name), and upgrade(root): '
                    'обходит дерево (элементы { tag, attrs, children, parent }), для каждого элемента с '
                    'зарегистрированным тегом создаёт экземпляр new ctor(el) (поле el), и при подключении '
                    'вызывает instance.connectedCallback(); для каждого имени из ctor.observedAttributes, '
                    'присутствующего в attrs, вызывает instance.attributeChangedCallback(name, null, value) '
                    '— до connectedCallback. Каждый элемент апгрейдится один раз (el.__upgraded). Метод '
                    'setAttribute(el, name, value) вызывает attributeChangedCallback(name, old, value) '
                    'только для наблюдаемых атрибутов уже апгрейженного элемента; remove(el) вызывает '
                    'disconnectedCallback.',
       'starter': 'class CustomElementRegistry {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const log = [];\n'
                 'class MyCard { static observedAttributes = ["title"]; constructor(el) { this.el = el; '
                 'log.push("ctor"); } connectedCallback() { log.push("connected"); } disconnectedCallback() '
                 '{ log.push("disconnected"); } attributeChangedCallback(n, o, v) { log.push(`attr ${n}: '
                 '${o}→${v}`); } }\n'
                 'const reg = new CustomElementRegistry();\n'
                 'for (const bad of ["card", "My-card", "1-a", "a--", "-a", "my_card"]) { try { '
                 'reg.define(bad, class {}); console.log("принято?", bad); } catch (e) { '
                 'console.log(e.name); } }\n'
                 'reg.define("my-card", MyCard);\n'
                 'try { reg.define("my-card", class {}); } catch (e) { console.log(e.message); }\n'
                 'try { reg.define("other-card", MyCard); } catch (e) { console.log(e.message); }\n'
                 'console.log(reg.get("my-card") === MyCard, reg.get("nope"));\n'
                 'const card = el("my-card", { title: "Привет", other: "x" }, el("p", {}, "тело"));\n'
                 'const root = el("div", {}, card, el("my-card", {}));\n'
                 'reg.upgrade(root); reg.upgrade(root);\n'
                 'console.log(log.join(" | "));\n'
                 'log.length = 0;\n'
                 'reg.setAttribute(card, "title", "Новый"); reg.setAttribute(card, "other", "y");\n'
                 'console.log(log.join(" | "));\n'
                 'log.length = 0;\n'
                 'reg.remove(card);\n'
                 'console.log(log.join(" | "), root.children.length);\n',
       'hint': 'Проверка имени регулярным выражением; апгрейд — обход дерева; наблюдаемые атрибуты — из '
               'static observedAttributes.',
       'expected': ['SyntaxError',
                    'SyntaxError',
                    'SyntaxError',
                    'SyntaxError',
                    'SyntaxError',
                    'SyntaxError',
                    'уже определён',
                    'уже определён',
                    'true undefined',
                    'ctor | attr title: null→Привет | connected | ctor | connected',
                    'attr title: Привет→Новый',
                    'disconnected 1']},
      {'id': 'j14-shadow-slots',
       'mode': 'js',
       'title': 'Shadow DOM: селекторы и слоты',
       'statement': 'Элемент-хост может иметь shadowRoot — узел { type: "shadow", children }. Напишите '
                    'функции: queryAll(root, pred) — все элементы-потомки root, подходящие под pred, в '
                    'порядке документа, НЕ заходя в теневые деревья (ни в shadowRoot хоста, и дальше); '
                    'queryDeep(root, pred) — то же, но заходя и в теневые деревья (shadowRoot хоста '
                    'обходится сразу после самого хоста, до его светлых детей); assignedNodes(host, '
                    'slotName) — светлые дети хоста, назначенные слоту: элемент с атрибутом slot="имя" '
                    'попадает в слот с этим именем, остальные (включая текст) — в безымянный слот (slotName '
                    '= "" или undefined).',
       'starter': 'function queryAll(root, pred) {\n'
                  '}\n'
                  'function queryDeep(root, pred) {\n'
                  '}\n'
                  'function assignedNodes(host, slotName) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const host = el("my-widget", {}, el("h2", { slot: "title" }, "Заголовок"), el("p", {}, '
                 '"содержимое"), tx("текст"), el("span", { slot: "title" }, "ещё"), el("b", { slot: "footer" '
                 '}, "низ"));\n'
                 'host.shadowRoot = { type: "shadow", children: [el("div", { class: "inner" }, el("slot", { '
                 'name: "title" }), el("slot", {}), el("p", { class: "shadow-p" }, "из тени"))] };\n'
                 'const root = el("body", {}, host, el("p", { class: "light-p" }, "светлый"));\n'
                 'const isP = (n) => n.tag === "p";\n'
                 'console.log(names(queryAll(root, isP)), "|", names(queryDeep(root, isP)));\n'
                 'console.log(names(queryAll(root, (n) => n.tag === "slot")).length, names(queryDeep(root, '
                 '(n) => n.tag === "slot")));\n'
                 'const show = (ns) => ns.map((n) => (n.type === "text" ? JSON.stringify(n.text) : '
                 'n.tag)).join();\n'
                 'console.log(show(assignedNodes(host, "title")), "|", show(assignedNodes(host)), "|", '
                 'show(assignedNodes(host, "")), "|", show(assignedNodes(host, "footer")), "|", '
                 'show(assignedNodes(host, "none")));\n',
       'hint': 'В queryDeep при встрече хоста сразу обойдите его shadowRoot, затем светлых детей.',
       'expected': ['p p.light-p | p.shadow-p p p.light-p',
                    '0 slot slot',
                    'h2,span | p,"текст" | p,"текст" | b |']},
      {'id': 'j14-range-text',
       'mode': 'js',
       'title': 'Range: текст между позициями',
       'statement': 'Позиция — { node (текстовый узел), offset }. Напишите функцию rangeToString(root, '
                    'start, end) → текст между позициями (включительно слева, исключительно справа) по всем '
                    'текстовым узлам root в порядке документа; если start позже end — позиции меняются '
                    'местами; позиции в разных узлах учитывают узлы между ними целиком. И функцию '
                    'extractRange(root, start, end) → { text, root }: удаляет этот текст из соответствующих '
                    'текстовых узлов (пустые текстовые узлы удаляются из дерева).',
       'starter': 'function rangeToString(root, start, end) {\n'
                  '}\n'
                  'function extractRange(root, start, end) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const mk = () => { const p = el("p", {}, "Привет, ", el("b", {}, "дорогой"), " мир", '
                 'el("i", {}, el("u", {}, "!!!")), " конец"); return { p, t: [p.children[0], '
                 'p.children[1].children[0], p.children[2], p.children[3].children[0].children[0], '
                 'p.children[4]] }; };\n'
                 'const { p, t } = mk();\n'
                 'const pos = (node, offset) => ({ node, offset });\n'
                 'console.log(JSON.stringify(rangeToString(p, pos(t[0], 3), pos(t[0], 6))), '
                 'JSON.stringify(rangeToString(p, pos(t[0], 4), pos(t[2], 4))), '
                 'JSON.stringify(rangeToString(p, pos(t[2], 4), pos(t[0], 4))));\n'
                 'console.log(JSON.stringify(rangeToString(p, pos(t[1], 0), pos(t[3], 2))), '
                 'JSON.stringify(rangeToString(p, pos(t[0], 0), pos(t[4], 6))), '
                 'JSON.stringify(rangeToString(p, pos(t[1], 2), pos(t[1], 2))));\n'
                 'const r = extractRange(p, pos(t[0], 4), pos(t[3], 1));\n'
                 'console.log(JSON.stringify(r.text), r.root === p, p.children.map((c) => (c.type === "text" '
                 '? JSON.stringify(c.text) : c.tag + ":" + c.children.length)).join(" "));\n'
                 'const q = mk();\n'
                 'extractRange(q.p, pos(q.t[1], 0), pos(q.t[1], 7));\n'
                 'console.log(q.p.children.length, q.p.children.map((c) => c.tag ?? "#").join(), t[1].parent '
                 '!== null);\n',
       'hint': 'Соберите все текстовые узлы в порядке документа и работайте по их индексам.',
       'expected': ['"вет" "ет, дорогой мир" "ет, дорогой мир"',
                    '"дорогой мир!!" "Привет, дорогой мир!!! конец" ""',
                    '"ет, дорогой мир!" true "Прив" b:0 i:1 " конец"',
                    '5 #,b,#,i,# false']},
      {'id': 'j14-accessible-name',
       'mode': 'js',
       'title': 'Доступное имя элемента',
       'statement': 'Напишите функцию accessibleName(el, root): вычисляет имя по упрощённому алгоритму: 1) '
                    'aria-labelledby (список id через пробел → тексты этих элементов в root, через пробел); '
                    '2) aria-label; 3) для img — alt; для input/select/textarea — текст <label for=id> с '
                    'этим id (если есть), затем title; 4) для button, a, h1–h6, li — текстовое содержимое; '
                    '5) title; иначе пустая строка. Пробелы нормализуйте (trim и склейка повторов). И '
                    'функцию roleOf(el): явный role иначе по тегу: button→button, a[href]→link, '
                    'h1…h6→heading, img→img, ul/ol→list, li→listitem, input[type=checkbox]→checkbox, '
                    'input[type=text|не указан]→textbox, nav→navigation, main→main, иначе null.',
       'starter': 'function accessibleName(el, root) {\n}\nfunction roleOf(el) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const root = el("div", {}, el("h1", { id: "t" }, "  Главная   страница "), el("button", { '
                 '"aria-labelledby": "t x" }, "ок"), el("span", { id: "x" }, "доп"), el("button", { '
                 '"aria-label": "Закрыть" }, "✕"), el("label", { for: "n" }, "Ваше ", el("b", {}, "имя")), '
                 'el("input", { id: "n", type: "text", title: "поле" }), el("input", { id: "z", title: "без '
                 'подписи" }), el("img", { alt: "логотип", src: "a" }), el("img", { src: "b" }), el("a", { '
                 'href: "/x" }, "ссылка ", el("i", {}, "внутри")), el("a", {}, "якорь"), el("div", { title: '
                 '"подсказка" }), el("div", {}), el("div", { role: "alert" }), el("input", { type: '
                 '"checkbox" }), el("nav"), el("ul", {}, el("li", {}, "пункт")), el("h3", {}, "заг"));\n'
                 'const k = root.children;\n'
                 'console.log([0, 1, 3, 5, 6, 7, 8, 9, 10, 11, 12].map((i) => '
                 'JSON.stringify(accessibleName(k[i], root))).join(" "));\n'
                 'console.log(k.filter((n) => n.tag !== "label" && n.tag !== "span").map((n) => '
                 'roleOf(n)).join());\n',
       'hint': 'Последовательность источников имени: labelledby, label, alt/label/title, содержимое, title.',
       'expected': ['"Главная страница" "Главная страница доп" "Закрыть" "Ваше имя" "без подписи" "логотип" '
                    '"" "ссылка внутри" "якорь" "подсказка" ""',
                    'heading,button,button,textbox,textbox,img,img,link,,,,alert,checkbox,navigation,list,heading']},
      {'id': 'j14-tab-order',
       'mode': 'js',
       'title': 'Порядок табуляции',
       'statement': 'Элементы — { id, tag, attrs } в порядке документа. Напишите функцию tabOrder(elements): '
                    'возвращает массив id в порядке перехода клавишей Tab: фокусируемые — a[href], button, '
                    'input (кроме type=hidden), select, textarea, и любые элементы с tabindex; исключаются '
                    'disabled (для button/input/select/textarea), hidden-атрибут, элементы с tabindex < 0; '
                    'сначала идут элементы с положительным tabindex по возрастанию (при равенстве — в '
                    'порядке документа), затем остальные (tabindex="0" и естественно фокусируемые) в порядке '
                    'документа. И функцию nextFocus(order, currentId, shift) → следующий id по кругу (shift '
                    '— назад); если currentId не в списке — первый (или последний при shift).',
       'starter': 'function tabOrder(elements) {\n}\nfunction nextFocus(order, currentId, shift) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const els = [\n'
                 '  { id: "a", tag: "a", attrs: { href: "/" } }, { id: "b", tag: "button", attrs: {} }, { '
                 'id: "c", tag: "button", attrs: { disabled: "" } },\n'
                 '  { id: "d", tag: "div", attrs: { tabindex: "0" } }, { id: "e", tag: "div", attrs: {} }, { '
                 'id: "f", tag: "input", attrs: { tabindex: "2" } },\n'
                 '  { id: "g", tag: "input", attrs: { type: "hidden" } }, { id: "h", tag: "a", attrs: {} }, '
                 '{ id: "i", tag: "span", attrs: { tabindex: "-1" } },\n'
                 '  { id: "j", tag: "select", attrs: { tabindex: "1" } }, { id: "k", tag: "textarea", attrs: '
                 '{ hidden: true } }, { id: "l", tag: "button", attrs: { tabindex: "2" } },\n'
                 '  { id: "m", tag: "input", attrs: { type: "text" } },\n'
                 '];\n'
                 'const o = tabOrder(els);\n'
                 'console.log(o.join());\n'
                 'console.log(nextFocus(o, "j"), nextFocus(o, "m"), nextFocus(o, "j", true), nextFocus(o, '
                 '"zzz"), nextFocus(o, "zzz", true), nextFocus([], "a"), nextFocus(["x"], "x"));\n'
                 'console.log(tabOrder([]).length);\n',
       'hint': 'Отфильтруйте фокусируемые, затем положительные tabindex по возрастанию, затем остальные по '
               'порядку документа.',
       'expected': ['j,f,l,a,b,d,m', 'f j m j m null x', '0']},
      {'id': 'j14-testing-queries',
       'mode': 'js',
       'title': 'Запросы как в Testing Library',
       'statement': 'Напишите функции для поиска элементов так, как их видит пользователь: getByText(root, '
                    'matcher, { exact = true } = {}) — элементы, чей собственный текст (склейка прямых '
                    'текстовых детей, trim, нормализация пробелов) совпадает: matcher — строка (при '
                    'exact=false — подстрока без учёта регистра) или RegExp; getByRole(root, role, { name } '
                    '= {}) — элементы с ролью (явный role или неявная: button→button, a[href]→link, '
                    'h1–h6→heading, input[type=checkbox]→checkbox, input без type→textbox, ul→list, '
                    'li→listitem), опционально с именем (текст содержимого или aria-label; строка — точное '
                    'совпадение, RegExp — проверка); getByLabelText(root, text) — элемент по связанной '
                    'подписи (<label for=id>); queryOne(list, what) — единственный элемент из списка или '
                    'null; если элементов больше одного — бросьте Error("найдено несколько: N"), если ноль — '
                    'Error("не найдено: <what>").',
       'starter': 'function getByText(root, matcher, options) {\n'
                  '}\n'
                  'function getByRole(root, role, options) {\n'
                  '}\n'
                  'function getByLabelText(root, text) {\n'
                  '}\n'
                  'function queryOne(list, what) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const tx = (text) => ({ type: "text", text, parent: null });\n'
                 'const page = () => el("div", { id: "root", class: "app" },\n'
                 '  el("header", { class: "top" }, el("h1", {}, "Заголовок"), el("nav", { class: "menu" }, '
                 'el("a", { href: "/a", class: "link active" }, "А"), el("a", { href: "/b", class: "link" }, '
                 '"Б"))),\n'
                 '  el("main", {}, el("ul", { id: "list" }, el("li", { class: "item" }, "один"), el("li", { '
                 'class: "item done" }, "два"), el("li", { class: "item" }, el("span", {}, "три"))), el("p", '
                 '{ class: "note" }, "заметка")),\n'
                 ');\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const names = (nodes) => nodes.map((n) => n.tag + (n.attrs.id ? "#" + n.attrs.id : "") + '
                 '(n.attrs.class ? "." + n.attrs.class.split(" ").join(".") : "")).join(" ");\n'
                 'const root = el("main", {}, el("h1", {}, "Корзина"), el("ul", {}, el("li", {}, "Хлеб ", '
                 'el("button", { "aria-label": "Убрать хлеб" }, "×")), el("li", {}, "  Сыр ", el("button", '
                 '{}, "Убрать")), el("li", {}, "Хлеб")), el("label", { for: "q" }, "Количество"), '
                 'el("input", { id: "q" }), el("a", { href: "/pay" }, "Оплатить"), el("button", {}, '
                 '"Оплатить ", el("b", {}, "сейчас")), el("input", { type: "checkbox", id: "c" }), '
                 'el("label", { for: "c" }, "Согласен"));\n'
                 'const show = (ns) => ns.map((n) => n.tag).join() || "—";\n'
                 'console.log(show(getByText(root, "Хлеб")), show(getByText(root, "хлеб", { exact: false '
                 '})), show(getByText(root, /^Сыр$/)), show(getByText(root, "нет")), show(getByText(root, '
                 '"Оплатить")));\n'
                 'console.log(show(getByRole(root, "button")), show(getByRole(root, "button", { name: '
                 '"Убрать хлеб" })), show(getByRole(root, "button", { name: /Оплатить/ })), '
                 'show(getByRole(root, "heading")), show(getByRole(root, "link")), show(getByRole(root, '
                 '"listitem")), show(getByRole(root, "checkbox")), show(getByRole(root, "textbox")));\n'
                 'console.log(show(getByLabelText(root, "Количество")), show(getByLabelText(root, '
                 '"Согласен")), getByLabelText(root, "x").length);\n'
                 'console.log(queryOne(getByRole(root, "heading"), "заголовок").tag);\n'
                 'for (const [f, w] of [[() => getByRole(root, "button"), "кнопка"], [() => getByText(root, '
                 '"нет"), "текст «нет»"]]) { try { queryOne(f(), w); } catch (e) { console.log(e.message); } '
                 '}\n',
       'hint': 'Собственный текст — только прямые текстовые дети; роль — явная или по тегу.',
       'expected': ['li,li li,li li — a,button',
                    'button,button,button button button h1 a li,li,li input input',
                    'input input 0',
                    'h1',
                    'найдено несколько: 3',
                    'не найдено: текст «нет»']}]}
