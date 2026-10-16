"""Задачи книги «Современный Frontend», глава 16 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {16: [{'id': 'j16-dispatch',
       'mode': 'js',
       'title': 'Путь события: погружение, цель, всплытие',
       'statement': 'Узел: { id, parent, listeners: [{ type, fn, capture, once, passive }] }. Напишите '
                    'функцию dispatch(target, event): event = { type, bubbles = true, cancelable = true }. '
                    'Сначала путь от корня к target; фаза погружения: слушатели с capture === true на '
                    'предках (сверху вниз); фаза цели: все слушатели target (сначала capture, затем '
                    'остальные, в порядке добавления); фаза всплытия (если bubbles): слушатели без capture '
                    'на предках снизу вверх. Каждому fn передаётся объект e: { type, target, currentTarget, '
                    'eventPhase (1, 2, 3), defaultPrevented, preventDefault() (только если cancelable и '
                    'обработчик не passive), stopPropagation(), stopImmediatePropagation() }. once-слушатель '
                    'удаляется перед вызовом. Возвращает true, если preventDefault не вызван.',
       'starter': 'function dispatch(target, event) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const node = (id, parent = null) => ({ id, parent, listeners: [] });\n'
                 'const on = (n, type, fn, opts = {}) => n.listeners.push({ type, fn, capture: '
                 '!!opts.capture, once: !!opts.once, passive: !!opts.passive });\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const win = node("window"), div = node("div", win), ul = node("ul", div), li = node("li", '
                 'ul), btn = node("button", li);\n'
                 'const log = [];\n'
                 'const h = (name) => (e) => '
                 'log.push(`${name}[${e.eventPhase}:${e.target.id}>${e.currentTarget.id}]`);\n'
                 'on(win, "click", h("win-cap"), { capture: true }); on(div, "click", h("div-bub")); on(ul, '
                 '"click", h("ul-cap"), { capture: true }); on(ul, "click", h("ul-bub"));\n'
                 'on(btn, "click", h("btn-bub")); on(btn, "click", h("btn-cap"), { capture: true }); on(btn, '
                 '"click", h("btn-once"), { once: true }); on(li, "focus", h("не тот тип"));\n'
                 'console.log(dispatch(btn, { type: "click" }));\n'
                 'console.log(log.join(" "));\n'
                 'log.length = 0; dispatch(btn, { type: "click" }); console.log(log.length, '
                 'log.includes("btn-once[2:button>button]"));\n'
                 'log.length = 0; dispatch(btn, { type: "click", bubbles: false }); console.log(log.join(" '
                 '"));\n'
                 'log.length = 0;\n'
                 'on(li, "click", (e) => { log.push("li-stop"); e.stopPropagation(); }); on(li, "click", '
                 'h("li-second"));\n'
                 'dispatch(btn, { type: "click" }); console.log(log.join(" "));\n'
                 'const n2 = node("n2", node("p2")); log.length = 0;\n'
                 'on(n2, "x", (e) => { log.push("1"); e.stopImmediatePropagation(); }); on(n2, "x", () => '
                 'log.push("2")); on(n2.parent, "x", () => log.push("parent"));\n'
                 'dispatch(n2, { type: "x" }); console.log(log.join());\n'
                 'const a = node("a"); on(a, "submit", (e) => e.preventDefault()); on(a, "submit", (e) => '
                 'e.preventDefault(), { passive: true });\n'
                 'console.log(dispatch(a, { type: "submit" }), dispatch(a, { type: "submit", cancelable: '
                 'false }));\n'
                 'const b = node("b"); on(b, "scroll", (e) => e.preventDefault(), { passive: true }); '
                 'console.log(dispatch(b, { type: "scroll" }));\n',
       'hint': 'Путь = предки от корня; три прохода: capture на предках, цель, bubble на предках; флаги '
               'остановки проверяйте после каждого обработчика.',
       'expected': ['true',
                    'win-cap[1:button>window] ul-cap[1:button>ul] btn-cap[2:button>button] '
                    'btn-bub[2:button>button] btn-once[2:button>button] ul-bub[3:button>ul] '
                    'div-bub[3:button>div]',
                    '6 false',
                    'win-cap[1:button>window] ul-cap[1:button>ul] btn-cap[2:button>button] '
                    'btn-bub[2:button>button]',
                    'win-cap[1:button>window] ul-cap[1:button>ul] btn-cap[2:button>button] '
                    'btn-bub[2:button>button] li-stop li-second[3:button>li]',
                    '1',
                    'false true',
                    'true']},
      {'id': 'j16-event-target',
       'mode': 'js',
       'title': 'Свой EventTarget',
       'statement': 'Напишите класс MyEventTarget: addEventListener(type, fn, options) (options — boolean '
                    '(capture) или { once, signal, capture }); одинаковая тройка (type, fn, capture) '
                    'повторно не добавляется; signal — при abort слушатель снимается (если signal уже '
                    'отменён — не добавляется); removeEventListener(type, fn, options); dispatchEvent(event) '
                    '→ true, если не отменён (event.preventDefault() выставляет event.defaultPrevented = '
                    'true для cancelable событий): вызывает копию списка слушателей на момент начала '
                    'dispatch; снятый во время dispatch и ещё не вызванный слушатель не вызывается; fn может '
                    'быть функцией или объектом с handleEvent; event получает target и currentTarget. '
                    'Capture-флаг не влияет на порядок (для простого EventTarget все слушатели вызываются в '
                    'порядке добавления).',
       'starter': 'class MyEventTarget {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const t = new MyEventTarget();\n'
                 'const log = [];\n'
                 'const a = () => log.push("a"), b = () => log.push("b");\n'
                 't.addEventListener("x", a); t.addEventListener("x", a); t.addEventListener("x", b);\n'
                 't.dispatchEvent({ type: "x" }); console.log(log.join());\n'
                 'log.length = 0; t.removeEventListener("x", a); t.dispatchEvent({ type: "x" }); '
                 'console.log(log.join());\n'
                 'log.length = 0; t.addEventListener("x", () => log.push("once"), { once: true }); '
                 't.dispatchEvent({ type: "x" }); t.dispatchEvent({ type: "x" }); console.log(log.join());\n'
                 'log.length = 0; const c = new MyEventTarget();\n'
                 'const first = () => { log.push("first"); c.removeEventListener("y", second); }; const '
                 'second = () => log.push("second");\n'
                 'c.addEventListener("y", first); c.addEventListener("y", second); c.dispatchEvent({ type: '
                 '"y" }); console.log(log.join());\n'
                 'log.length = 0; const d = new MyEventTarget(); const ac = new AbortController();\n'
                 'd.addEventListener("z", () => log.push("z1"), { signal: ac.signal }); '
                 'd.addEventListener("z", () => log.push("z2"), { signal: ac.signal });\n'
                 'd.dispatchEvent({ type: "z" }); ac.abort(); d.dispatchEvent({ type: "z" }); '
                 'd.addEventListener("z", () => log.push("поздно"), { signal: ac.signal }); '
                 'd.dispatchEvent({ type: "z" }); console.log(log.join());\n'
                 'd.addEventListener("w", (e) => e.preventDefault());\n'
                 'console.log(d.dispatchEvent({ type: "w" }), d.dispatchEvent({ type: "w", cancelable: false '
                 '}), d.dispatchEvent({ type: "nobody" }));\n'
                 'const obj = { handleEvent(e) { log.push("obj:" + e.type + ":" + (e.target === d)); } }; '
                 'log.length = 0; d.addEventListener("q", obj); d.dispatchEvent({ type: "q" }); '
                 'console.log(log.join());\n'
                 'd.addEventListener("cap", a, true); d.addEventListener("cap", a, false); log.length = 0; '
                 'd.dispatchEvent({ type: "cap" }); console.log(log.length); d.removeEventListener("cap", a, '
                 'true); log.length = 0; d.dispatchEvent({ type: "cap" }); console.log(log.length);\n',
       'hint': 'Список слушателей; dispatch работает с копией, но перед вызовом проверяет, что слушатель ещё '
               'на месте.',
       'expected': ['a,b', 'b', 'b,once,b', 'first', 'z1,z2', 'false true true', 'obj:q:true', '2', '1']},
      {'id': 'j16-delegate',
       'mode': 'js',
       'title': 'Делегирование событий',
       'statement': 'Узлы — { tag, attrs, children, parent } (как в главе про DOM). Напишите функцию '
                    'delegate(container, matcher, handler) → функция listener(event): event = { target }: '
                    'поднимается от event.target до container (не включая container) и находит ближайший '
                    'узел, подходящий под matcher (функция или строка «тег», «.класс», «[атрибут]»); если '
                    'нашёл и узел лежит внутри container — вызывает handler(event, matchedNode) и возвращает '
                    'true, иначе false. Подходящий узел — только элемент (текстовые узлы {type: "text"} при '
                    'подъёме пропускаются).',
       'starter': 'function delegate(container, matcher, handler) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const el = (tag, attrs = {}, ...kids) => { const n = { type: "element", tag, attrs, '
                 'children: [], parent: null }; for (const k of kids) { const c = typeof k === "string" ? { '
                 'type: "text", text: k, parent: null } : k; c.parent = n; n.children.push(c); } return n; '
                 '};\n'
                 'const outer = el("section", { class: "outside" }, el("button", { "data-action": "out" }, '
                 '"вне"));\n'
                 'const list = el("ul", { id: "list" }, el("li", {}, el("button", { "data-action": "save" }, '
                 'el("i", { class: "icon" }, "★"), "Сохранить")), el("li", {}, el("button", { "data-action": '
                 '"del" }, "Удалить")), el("li", { class: "plain" }, "текст"));\n'
                 'const root = el("div", {}, outer, list);\n'
                 'const log = [];\n'
                 'const l1 = delegate(list, "button", (e, n) => log.push(n.attrs["data-action"]));\n'
                 'const icon = list.children[0].children[0].children[0], iconText = icon.children[0], del = '
                 'list.children[1].children[0], plain = list.children[2], plainText = plain.children[0];\n'
                 'console.log(l1({ target: icon }), l1({ target: iconText }), l1({ target: del }), l1({ '
                 'target: plain }), l1({ target: plainText }), l1({ target: list }), l1({ target: '
                 'outer.children[0] }), log.join());\n'
                 'log.length = 0;\n'
                 'const l2 = delegate(list, ".plain", (e, n) => log.push("plain")); console.log(l2({ target: '
                 'plainText }), l2({ target: del }), log.join());\n'
                 'const l3 = delegate(list, "[data-action]", (e, n) => log.push(n.tag)); console.log(l3({ '
                 'target: iconText }), log.at(-1));\n'
                 'const l4 = delegate(root, (n) => n.tag === "li", (e, n) => log.push("li:" + '
                 'n.children.length)); console.log(l4({ target: iconText }), log.at(-1));\n'
                 'const added = el("li", {}, el("button", { "data-action": "new" }, "+")); added.parent = '
                 'list; list.children.push(added);\n'
                 'log.length = 0; l1({ target: added.children[0] }); console.log(log.join());\n',
       'hint': 'Поднимайтесь по parent до контейнера (не включая), пропуская текстовые узлы.',
       'expected': ['true true true false false false true save,save,del,out',
                    'true false plain',
                    'true button',
                    'true li:1',
                    'new']},
      {'id': 'j16-shortcut-parse',
       'mode': 'js',
       'title': 'Горячие клавиши: разбор и сравнение',
       'statement': 'Напишите функцию parseShortcut(str) → { ctrl, shift, alt, meta, key } (key — в нижнем '
                    'регистре; регистр модификаторов и пробелы вокруг «+» не важны; «Ctrl», «Control», '
                    '«Cmd»/«Command»/«Meta», «Option»/«Alt», «Mod» = meta на Mac и ctrl иначе — параметр '
                    'isMac второй функции) и matches(event, shortcut, isMac = false): event = { key, '
                    'ctrlKey, shiftKey, altKey, metaKey }; совпадение требует точного набора модификаторов '
                    '(лишние нажатые — несовпадение) и совпадения key без учёта регистра; для shortcut с '
                    '«Mod» — meta при isMac, иначе ctrl. Неизвестная конструкция (пустой key, два key) — '
                    'Error.',
       'starter': 'function parseShortcut(str) {\n}\nfunction matches(event, shortcut, isMac) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const P = (s) => { try { const r = parseShortcut(s); console.log(JSON.stringify([r.ctrl, '
                 'r.shift, r.alt, r.meta, !!r.mod, r.key])); return r; } catch (e) { console.log("ошибка"); '
                 '} };\n'
                 'const save = P("Ctrl+S"), a = P("ctrl + shift + Z"), mod = P("Mod+K"), cmd = '
                 'P("Cmd+Option+i"), esc = P("Escape"), plus = P("Ctrl+=");\n'
                 'for (const s of ["", "Ctrl+", "S+K", "+"]) P(s);\n'
                 'const ev = (key, m = {}) => ({ key, ctrlKey: false, shiftKey: false, altKey: false, '
                 'metaKey: false, ...m });\n'
                 'console.log(matches(ev("s", { ctrlKey: true }), save), matches(ev("S", { ctrlKey: true }), '
                 'save), matches(ev("s", { ctrlKey: true, shiftKey: true }), save), matches(ev("s"), save), '
                 'matches(ev("z", { ctrlKey: true, shiftKey: true }), a));\n'
                 'console.log(matches(ev("k", { ctrlKey: true }), mod), matches(ev("k", { metaKey: true }), '
                 'mod), matches(ev("k", { metaKey: true }), mod, true), matches(ev("k", { ctrlKey: true }), '
                 'mod, true), matches(ev("i", { metaKey: true, altKey: true }), cmd), matches(ev("Escape"), '
                 'esc), matches(ev("="), P("="), false));\n',
       'hint': 'Разберите по «+»; Mod — особый модификатор, раскрывающийся при сравнении.',
       'expected': ['[true,false,false,false,false,"s"]',
                    '[true,true,false,false,false,"z"]',
                    '[false,false,false,false,true,"k"]',
                    '[false,false,true,true,false,"i"]',
                    '[false,false,false,false,false,"escape"]',
                    '[true,false,false,false,false,"="]',
                    'ошибка',
                    'ошибка',
                    'ошибка',
                    'ошибка',
                    'true true false false true',
                    '[false,false,false,false,false,"="]',
                    'true false true false true true true']},
      {'id': 'j16-key-sequences',
       'mode': 'js',
       'title': 'Многоклавишные комбинации (аккорды)',
       'statement': 'Напишите функцию createHotkeys(now, timeout = 1000): возвращает объект { bind(sequence, '
                    'fn), press(key) → boolean (true, если нажатие поглощено — совпало начало или целая '
                    'последовательность), reset() }. sequence — строка клавиш через пробел («g i», «g g», '
                    '«Escape»); между нажатиями не больше timeout мс (now() — часы); при неверной клавише '
                    'последовательность сбрасывается, но эта клавиша сама может начать новую; если одна '
                    'последовательность — начало другой, срабатывает более короткая только после паузы '
                    'timeout? — упростим: срабатывает сразу при полном совпадении; fn вызывается с '
                    'последовательностью.',
       'starter': 'function createHotkeys(now, timeout) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let t = 0;\n'
                 'const hk = createHotkeys(() => t, 500);\n'
                 'const log = [];\n'
                 'hk.bind("g i", (s) => log.push(s)); hk.bind("g g", (s) => log.push(s)); hk.bind("Escape", '
                 '(s) => log.push(s)); hk.bind("a b c", (s) => log.push(s));\n'
                 'const press = (k, dt = 100) => { t += dt; return hk.press(k); };\n'
                 'console.log(press("g"), press("i"), log.join());\n'
                 'console.log(press("g"), press("g"), press("g"), log.join());\n'
                 'console.log(press("x"), press("Escape"), log.join());\n'
                 'console.log(press("a"), press("b"), press("c"), log.join());\n'
                 't += 0; console.log(press("g"), press("i", 600), log.join());\n'
                 'console.log(press("g"), press("a"), press("b"), press("c"), log.join());\n'
                 'console.log(press("g"), press("q"), press("g"), press("g"), log.join());\n'
                 'hk.reset(); console.log(press("i"), press("z"));\n',
       'hint': 'Буфер нажатых клавиш; сравнение со всеми привязками как с префиксами; тайм-аут сбрасывает '
               'буфер.',
       'expected': ['true true g i',
                    'true true true g i,g g',
                    'false true g i,g g,Escape',
                    'true true true g i,g g,Escape,a b c',
                    'true false g i,g g,Escape,a b c',
                    'true true true true g i,g g,Escape,a b c,a b c',
                    'true false true true g i,g g,Escape,a b c,a b c,g g',
                    'false false']},
      {'id': 'j16-debounce',
       'mode': 'js',
       'title': 'debounce с leading/trailing',
       'statement': 'Дана фабрика FAKE() — виртуальные часы {now, setTimeout, clearTimeout, advance}. '
                    'Напишите функцию debounce(fn, ms, { leading = false, trailing = true } = {}, timers): '
                    'возвращает функцию-обёртку; trailing — вызов через ms после последнего обращения с '
                    'аргументами последнего; leading — вызов сразу при первом обращении в «серии» (серия '
                    'кончается, когда прошло ms без обращений); если и leading, и trailing: trailing-вызов '
                    'происходит только если было больше одного обращения в серии. У обёртки методы cancel() '
                    '(отменить ожидающий вызов) и flush() (выполнить ожидающий вызов немедленно, если он '
                    'есть). timers — объект с setTimeout/clearTimeout.',
       'starter': 'function debounce(fn, ms, options, timers) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const node = (id, parent = null) => ({ id, parent, listeners: [] });\n'
                 'const on = (n, type, fn, opts = {}) => n.listeners.push({ type, fn, capture: '
                 '!!opts.capture, once: !!opts.once, passive: !!opts.passive });\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const run = (opts, script) => { const c = FAKE(); const log = []; const f = debounce((x) '
                 '=> log.push(x + "@" + c.now()), 100, opts, c); script(f, c); return log.join(" "); };\n'
                 'console.log(run({}, (f, c) => { f(1); c.advance(50); f(2); c.advance(50); f(3); '
                 'c.advance(99); c.advance(1); f(4); c.advance(100); }));\n'
                 'console.log(run({ leading: true, trailing: false }, (f, c) => { f(1); c.advance(50); f(2); '
                 'c.advance(200); f(3); c.advance(10); f(4); c.advance(300); }));\n'
                 'console.log(run({ leading: true, trailing: true }, (f, c) => { f(1); c.advance(50); f(2); '
                 'c.advance(200); f(3); c.advance(300); }));\n'
                 'console.log(run({ leading: true }, (f, c) => { f(1); c.advance(500); }));\n'
                 'console.log(run({}, (f, c) => { f(1); f.cancel(); c.advance(500); f(2); c.advance(100); '
                 '}));\n'
                 'console.log(run({}, (f, c) => { f(1); c.advance(10); f.flush(); f.flush(); c.advance(500); '
                 '}));\n'
                 'console.log(run({ trailing: false }, (f, c) => { f(1); c.advance(500); }), "|");\n',
       'hint': 'Один таймер: при каждом вызове сбрасывайте его; leading — вызов в начале серии, trailing — в '
               'конце.',
       'expected': ['3@200 4@300', '1@0 3@250', '1@0 2@150 3@250', '1@0', '2@600', '1@10', ' |']},
      {'id': 'j16-throttle',
       'mode': 'js',
       'title': 'throttle',
       'statement': 'Напишите функцию throttle(fn, ms, { leading = true, trailing = true } = {}, timers): fn '
                    'вызывается не чаще раза в ms; leading — вызов сразу при первом обращении (если с '
                    'прошлого вызова прошло ≥ ms); trailing — последний «пропущенный» вызов выполняется по '
                    'окончании интервала с последними аргументами. timers — { now, setTimeout, clearTimeout '
                    '}. Метод cancel() сбрасывает состояние.',
       'starter': 'function throttle(fn, ms, options, timers) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const node = (id, parent = null) => ({ id, parent, listeners: [] });\n'
                 'const on = (n, type, fn, opts = {}) => n.listeners.push({ type, fn, capture: '
                 '!!opts.capture, once: !!opts.once, passive: !!opts.passive });\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const run = (opts, script) => { const c = FAKE(); const log = []; const f = throttle((x) '
                 '=> log.push(x + "@" + c.now()), 100, opts, c); script(f, c); return log.join(" "); };\n'
                 'console.log(run({}, (f, c) => { f(1); c.advance(30); f(2); c.advance(30); f(3); '
                 'c.advance(200); f(4); c.advance(300); }));\n'
                 'console.log(run({ trailing: false }, (f, c) => { f(1); c.advance(30); f(2); c.advance(80); '
                 'f(3); c.advance(50); f(4); c.advance(200); }));\n'
                 'console.log(run({ leading: false }, (f, c) => { f(1); c.advance(30); f(2); c.advance(200); '
                 'f(3); c.advance(200); }));\n'
                 'console.log(run({}, (f, c) => { for (let i = 1; i <= 10; i++) { f(i); c.advance(25); } '
                 'c.advance(500); }));\n'
                 'console.log(run({}, (f, c) => { f(1); f.cancel(); c.advance(500); f(2); c.advance(500); '
                 '}));\n',
       'hint': 'Следите за временем последнего вызова и за одним отложенным «хвостовым» вызовом.',
       'expected': ['1@0 3@100 4@260', '1@0 3@110', '2@100 3@230', '1@0 4@100 8@200 10@300', '1@0 2@500']},
      {'id': 'j16-raf-throttle',
       'mode': 'js',
       'title': 'Обработка не чаще раза за кадр',
       'statement': 'Дан планировщик кадров sched = { requestAnimationFrame(cb) → id, '
                    'cancelAnimationFrame(id) }. Напишите функцию rafThrottle(fn, sched): возвращает '
                    'функцию-обёртку, которая запоминает последние аргументы и вызывает fn(...args) один раз '
                    'в ближайшем кадре (если за кадр было несколько обращений — вызов с последними '
                    'аргументами); wrapped.cancel() отменяет запланированный вызов. Возвращаемое значение fn '
                    'не нужно.',
       'starter': 'function rafThrottle(fn, sched) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'function makeSched() { let q = []; let n = 0; return { requestAnimationFrame(cb) { const '
                 'id = ++n; q.push({ id, cb }); return id; }, cancelAnimationFrame(id) { q = q.filter((x) => '
                 'x.id !== id); }, frame() { const r = q; q = []; r.forEach((x) => x.cb()); return r.length; '
                 '}, pending: () => q.length }; }\n'
                 'const s = makeSched();\n'
                 'const log = [];\n'
                 'const onMove = rafThrottle((x, y) => log.push(`${x},${y}`), s);\n'
                 'for (let i = 0; i < 100; i++) onMove(i, i * 2);\n'
                 'console.log(s.pending(), log.length);\n'
                 'console.log(s.frame(), log.join());\n'
                 'onMove(1, 1); s.frame(); onMove(2, 2); onMove(3, 3); s.frame(); s.frame(); '
                 'console.log(log.join(" "));\n'
                 'onMove(9, 9); onMove.cancel(); console.log(s.pending(), s.frame(), log.length);\n'
                 'onMove(7, 7); console.log(s.pending());\n',
       'hint': 'Один запланированный кадр; при обращении обновляйте последние аргументы.',
       'expected': ['1 0', '1 99,198', '99,198 1,1 3,3', '0 0 3', '1']},
      {'id': 'j16-drag-fsm',
       'mode': 'js',
       'title': 'Перетаскивание как автомат',
       'statement': 'Напишите функцию createDrag({ threshold = 5, onStart, onMove, onDrop, onCancel }) → '
                    'объект с методом handle(e), где e = { type: "down"|"move"|"up"|"key", x, y, key? }. '
                    'Состояния: idle → pressed (down) → dragging (move с расстоянием от точки down ≥ '
                    'threshold: вызывается onStart({x, y, startX, startY}), затем onMove({x, y, dx, dy}) для '
                    'этого и следующих move); up в pressed — просто возврат в idle (клик, колбэков нет); up '
                    'в dragging — onDrop({x, y}) и idle; key = "Escape" в pressed/dragging — onCancel() (в '
                    'dragging) и idle. Метод state возвращает имя состояния. move/up/key в idle '
                    'игнорируются.',
       'starter': 'function createDrag(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const log = [];\n'
                 'const mk = () => createDrag({ threshold: 5, onStart: (p) => log.push(`start ${p.x},${p.y} '
                 'from ${p.startX},${p.startY}`), onMove: (p) => log.push(`move ${p.dx},${p.dy}`), onDrop: '
                 '(p) => log.push(`drop ${p.x},${p.y}`), onCancel: () => log.push("cancel") });\n'
                 'const d = mk();\n'
                 'const send = (...evs) => { for (const e of evs) d.handle(e); console.log(d.state, "|", '
                 'log.join(" ; ")); log.length = 0; };\n'
                 'send({ type: "move", x: 1, y: 1 }, { type: "up", x: 1, y: 1 });\n'
                 'send({ type: "down", x: 10, y: 10 }, { type: "move", x: 12, y: 13 });\n'
                 'send({ type: "move", x: 20, y: 10 }, { type: "move", x: 30, y: 40 });\n'
                 'send({ type: "up", x: 31, y: 41 });\n'
                 'send({ type: "down", x: 0, y: 0 }, { type: "up", x: 0, y: 0 });\n'
                 'send({ type: "down", x: 0, y: 0 }, { type: "move", x: 0, y: 9 }, { type: "key", key: '
                 '"Enter" }, { type: "key", key: "Escape" });\n'
                 'send({ type: "down", x: 0, y: 0 }, { type: "key", key: "Escape" }, { type: "move", x: 50, '
                 'y: 50 });\n'
                 'send({ type: "down", x: 5, y: 5 }, { type: "down", x: 100, y: 100 }, { type: "move", x: 8, '
                 'y: 9 });\n',
       'hint': 'Состояние и точка нажатия в замыкании; порог расстояния — Math.hypot.',
       'expected': ['idle |',
                    'pressed |',
                    'dragging | start 20,10 from 10,10 ; move 10,0 ; move 20,30',
                    'idle | drop 31,41',
                    'idle |',
                    'idle | start 0,9 from 0,0 ; move 0,9 ; cancel',
                    'idle |',
                    'dragging | start 8,9 from 5,5 ; move 3,4']},
      {'id': 'j16-swipe',
       'mode': 'js',
       'title': 'Распознавание свайпа',
       'statement': 'Напишите функцию detectSwipe(points, { minDistance = 50, maxTime = 600, maxOffAxis = '
                    '0.5 }): points — массив { x, y, t } одного касания (по времени); возвращает { '
                    'direction: "left"|"right"|"up"|"down", distance, duration, velocity (px/мс, 3 знака) } '
                    'или null: расстояние между первой и последней точками ≥ minDistance, время ≤ maxTime, а '
                    'смещение по второстепенной оси не больше maxOffAxis от смещения по главной (иначе это '
                    'диагональ и не свайп). Для менее чем двух точек — null.',
       'starter': 'function detectSwipe(points, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const P = (...xs) => xs.map(([x, y, t]) => ({ x, y, t }));\n'
                 'const show = (pts, o) => console.log(JSON.stringify(detectSwipe(pts, o)));\n'
                 'show(P([0, 0, 0], [60, 5, 100], [120, 10, 200]));\n'
                 'show(P([200, 50, 0], [100, 55, 80]));\n'
                 'show(P([0, 0, 0], [5, 100, 150]));\n'
                 'show(P([0, 100, 0], [0, 0, 400]));\n'
                 'show(P([0, 0, 0], [30, 0, 100]));\n'
                 'show(P([0, 0, 0], [100, 0, 900]));\n'
                 'show(P([0, 0, 0], [100, 80, 200]));\n'
                 'show(P([0, 0, 0], [100, 40, 200]));\n'
                 'show(P([0, 0, 0]));\n'
                 'show([], {});\n'
                 'show(P([0, 0, 0], [40, 0, 50]), { minDistance: 30 });\n'
                 'show(P([0, 0, 5], [60, 0, 5]));\n',
       'hint': 'Главная ось — с большим смещением; второстепенное не больше доли главного.',
       'expected': ['{"direction":"right","distance":120,"duration":200,"velocity":0.6}',
                    '{"direction":"left","distance":100,"duration":80,"velocity":1.25}',
                    '{"direction":"down","distance":100,"duration":150,"velocity":0.667}',
                    '{"direction":"up","distance":100,"duration":400,"velocity":0.25}',
                    'null',
                    'null',
                    'null',
                    '{"direction":"right","distance":100,"duration":200,"velocity":0.5}',
                    'null',
                    'null',
                    '{"direction":"right","distance":40,"duration":50,"velocity":0.8}',
                    'null']},
      {'id': 'j16-long-press',
       'mode': 'js',
       'title': 'Долгое нажатие',
       'statement': 'Напишите функцию createLongPress({ delay = 500, tolerance = 10, onLongPress, onTap }, '
                    'timers): timers = { setTimeout, clearTimeout }. Возвращает объект { down(x, y), move(x, '
                    'y), up() }: down запускает таймер на delay; move дальше tolerance (евклидово расстояние '
                    'от точки down) отменяет жест (ни onLongPress, ни onTap); когда таймер сработал — '
                    'onLongPress({x, y}) один раз; up до срабатывания — onTap({x, y}); up после срабатывания '
                    'ничего не вызывает; повторный down во время жеста игнорируется.',
       'starter': 'function createLongPress(options, timers) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const node = (id, parent = null) => ({ id, parent, listeners: [] });\n'
                 'const on = (n, type, fn, opts = {}) => n.listeners.push({ type, fn, capture: '
                 '!!opts.capture, once: !!opts.once, passive: !!opts.passive });\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const c = FAKE(); const log = [];\n'
                 'const lp = createLongPress({ delay: 500, tolerance: 10, onLongPress: (p) => log.push(`long '
                 '${p.x},${p.y}`), onTap: (p) => log.push(`tap ${p.x},${p.y}`) }, c);\n'
                 'const show = (label) => { console.log(label, "|", log.join(" ; "), "|", c.pending()); '
                 'log.length = 0; };\n'
                 'lp.down(5, 5); c.advance(200); lp.up(); show("быстрый тап");\n'
                 'lp.down(5, 5); c.advance(600); lp.up(); show("долгое");\n'
                 'lp.down(5, 5); c.advance(100); lp.move(8, 9); c.advance(1000); lp.up(); show("в '
                 'допуске");\n'
                 'lp.down(5, 5); c.advance(100); lp.move(30, 5); c.advance(1000); lp.up(); show("сдвиг");\n'
                 'lp.down(1, 1); lp.down(50, 50); c.advance(600); lp.up(); show("повторный down");\n'
                 'lp.move(1, 1); lp.up(); show("без нажатия");\n'
                 'lp.down(7, 7); c.advance(499); lp.up(); lp.down(8, 8); c.advance(500); show("граница");\n',
       'hint': 'Состояния: idle, pressed, fired, cancelled; таймер запускается при down.',
       'expected': ['быстрый тап | tap 5,5 | 0',
                    'долгое | long 5,5 | 0',
                    'в допуске | long 5,5 | 0',
                    'сдвиг |  | 0',
                    'повторный down | long 1,1 | 0',
                    'без нажатия |  | 0',
                    'граница | tap 7,7 ; long 8,8 | 0']},
      {'id': 'j16-double-click',
       'mode': 'js',
       'title': 'Одиночный и двойной клик',
       'statement': 'Напишите функцию createClickClassifier({ interval = 300, distance = 10, onSingle, '
                    'onDouble }, timers): click(x, y) — регистрирует клик: если предыдущий клик был не '
                    'дальше distance и не раньше interval мс назад, вместо одиночного вызывается '
                    'onDouble({x, y}) (точка второго клика) и жест завершён (третий клик начинает новый); '
                    'иначе (второй клик далеко или первого не было) ожидающий предыдущий клик, если он есть, '
                    'немедленно выдаётся как onSingle(его точка), а текущий начинает ожидание interval мс: '
                    'если за это время второго клика не было — вызывается onSingle({x, y}). Одиночный клик '
                    'отложен, а не мгновенный. timers = { setTimeout, clearTimeout }.',
       'starter': 'function createClickClassifier(options, timers) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const node = (id, parent = null) => ({ id, parent, listeners: [] });\n'
                 'const on = (n, type, fn, opts = {}) => n.listeners.push({ type, fn, capture: '
                 '!!opts.capture, once: !!opts.once, passive: !!opts.passive });\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const c = FAKE(); const log = [];\n'
                 'const cc = createClickClassifier({ interval: 300, distance: 10, onSingle: (p) => '
                 'log.push(`single ${p.x},${p.y}`), onDouble: (p) => log.push(`double ${p.x},${p.y}`) }, '
                 'c);\n'
                 'const show = (label) => { console.log(label, "|", log.join(" ; "), "|", c.pending()); '
                 'log.length = 0; };\n'
                 'cc.click(1, 1); show("сразу после"); c.advance(299); show("299"); c.advance(1); '
                 'show("300");\n'
                 'cc.click(5, 5); c.advance(100); cc.click(8, 8); show("двойной"); c.advance(1000); '
                 'show("тихо");\n'
                 'cc.click(0, 0); c.advance(100); cc.click(100, 100); show("далеко"); c.advance(1000); '
                 'show("потом");\n'
                 'cc.click(2, 2); c.advance(100); cc.click(3, 3); cc.click(4, 4); show("тройной"); '
                 'c.advance(1000); show("итог");\n'
                 'cc.click(9, 9); c.advance(350); cc.click(9, 9); show("поздно"); c.advance(350); '
                 'show("второй одиночный");\n',
       'hint': 'Хранится один «ожидающий» клик с таймером; второй клик рядом отменяет таймер и даёт double.',
       'expected': ['сразу после |  | 1',
                    '299 |  | 1',
                    '300 | single 1,1 | 0',
                    'двойной | double 8,8 | 0',
                    'тихо |  | 0',
                    'далеко | single 0,0 | 1',
                    'потом | single 100,100 | 0',
                    'тройной | double 3,3 | 1',
                    'итог | single 4,4 | 0',
                    'поздно | single 9,9 | 1',
                    'второй одиночный | single 9,9 | 0']},
      {'id': 'j16-pinch',
       'mode': 'js',
       'title': 'Щипок: масштаб и центр',
       'statement': 'Два указателя заданы позициями { x, y }. Напишите класс PinchTracker: pointerDown(id, '
                    'x, y), pointerMove(id, x, y), pointerUp(id); пока нажаты ровно два указателя — метод '
                    'state() возвращает { scale, cx, cy, rotation } относительно момента, когда нажался '
                    'второй: scale = текущее расстояние / начальное (3 знака), центр — середина между '
                    'указателями (cx, cy), rotation — изменение угла в градусах (−180…180, 1 знак); при ином '
                    'числе указателей state() = null; отпускание одного сбрасывает базу (следующее нажатие '
                    'начнёт новый жест).',
       'starter': 'class PinchTracker {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const t = new PinchTracker();\n'
                 'console.log(t.state());\n'
                 't.pointerDown(1, 100, 100); console.log(t.state());\n'
                 't.pointerDown(2, 200, 100); console.log(JSON.stringify(t.state()));\n'
                 't.pointerMove(2, 300, 100); console.log(JSON.stringify(t.state()));\n'
                 't.pointerMove(1, 150, 150); t.pointerMove(2, 250, 150); '
                 'console.log(JSON.stringify(t.state()));\n'
                 't.pointerMove(1, 200, 100); t.pointerMove(2, 200, 200); '
                 'console.log(JSON.stringify(t.state()));\n'
                 't.pointerUp(2); console.log(t.state());\n'
                 't.pointerDown(3, 0, 0); t.pointerMove(3, 0, 50); console.log(JSON.stringify(t.state()));\n'
                 't.pointerDown(4, 10, 10); console.log(t.state());\n',
       'hint': 'База — расстояние и угол в момент второго нажатия; текущие значения сравниваются с базой.',
       'expected': ['null',
                    'null',
                    '{"scale":1,"cx":150,"cy":100,"rotation":0}',
                    '{"scale":2,"cx":200,"cy":100,"rotation":0}',
                    '{"scale":1,"cx":200,"cy":150,"rotation":0}',
                    '{"scale":1,"cx":200,"cy":150,"rotation":90}',
                    'null',
                    '{"scale":0.922,"cx":100,"cy":75,"rotation":-12.5}',
                    'null']},
      {'id': 'j16-hit-test',
       'mode': 'js',
       'title': 'Hit testing: какой элемент под курсором',
       'statement': 'Элементы: { id, x, y, w, h, z = 0, pointerEvents = "auto"|"none", parent? (id '
                    'родителя), clip? (true — обрезает потомков по своим границам) }. Напишите функцию '
                    'hitTest(elements, px, py): возвращает массив id от самого верхнего элемента к нижнему '
                    '(по z-index, при равенстве — позднее в списке выше), которые содержат точку (границы '
                    'включаются слева/сверху, исключаются справа/снизу), пропуская pointerEvents = none; '
                    'потомок обрезается, если у какого-либо предка clip = true и точка вне предка. Первый '
                    'элемент результата — target; для пустого пересечения — [].',
       'starter': 'function hitTest(elements, px, py) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const els = [\n'
                 '  { id: "page", x: 0, y: 0, w: 500, h: 500 },\n'
                 '  { id: "card", x: 50, y: 50, w: 200, h: 200, clip: true, parent: "page" },\n'
                 '  { id: "button", x: 100, y: 100, w: 100, h: 50, parent: "card" },\n'
                 '  { id: "tooltip", x: 180, y: 120, w: 150, h: 60, z: 10, pointerEvents: "none", parent: '
                 '"button" },\n'
                 '  { id: "overflow", x: 240, y: 60, w: 100, h: 30, parent: "card" },\n'
                 '  { id: "modal", x: 300, y: 300, w: 100, h: 100, z: 100 },\n'
                 '  { id: "toast", x: 350, y: 350, w: 100, h: 100, z: 100 },\n'
                 '];\n'
                 'for (const [x, y] of [[120, 120], [190, 130], [245, 70], [260, 70], [50, 50], [250, 250], '
                 '[320, 320], [360, 360], [450, 450], [499, 499], [500, 500]]) console.log(x, y, '
                 'JSON.stringify(hitTest(els, x, y)));\n'
                 'console.log(JSON.stringify(hitTest([], 1, 1)));\n',
       'hint': 'Фильтры: содержит точку, не pointer-events: none, не обрезан предком; сортировка по z и '
               'порядку.',
       'expected': ['120 120 ["button","card","page"]',
                    '190 130 ["button","card","page"]',
                    '245 70 ["overflow","card","page"]',
                    '260 70 ["page"]',
                    '50 50 ["card","page"]',
                    '250 250 ["page"]',
                    '320 320 ["modal","page"]',
                    '360 360 ["toast","modal","page"]',
                    '450 450 ["page"]',
                    '499 499 ["page"]',
                    '500 500 []',
                    '[]']},
      {'id': 'j16-pointer-capture',
       'mode': 'js',
       'title': 'Захват указателя',
       'statement': 'Напишите функцию createPointerRouter(hit): hit(x, y) → id верхнего элемента под точкой '
                    'или null (функция передаётся снаружи). Возвращает объект: setCapture(pointerId, '
                    'elementId), releaseCapture(pointerId), route(pointerId, type, x, y) → id получателя '
                    'события: если у указателя есть захват — захвативший элемент (независимо от позиции); '
                    'иначе — hit(x, y); при событии «pointerup» и «pointercancel» захват автоматически '
                    'снимается после доставки; состояние лежит по pointerId отдельно у каждого указателя; '
                    'получатель null — событие никому. Метод captured(pointerId) → id или null.',
       'starter': 'function createPointerRouter(hit) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const hit = (x, y) => (x < 100 ? "left" : x < 200 ? "right" : null);\n'
                 'const r = createPointerRouter(hit);\n'
                 'const s = (pid, type, x, y) => r.route(pid, type, x, y);\n'
                 'console.log(s(1, "pointerdown", 50, 0), s(1, "pointermove", 150, 0), s(1, "pointermove", '
                 '300, 0));\n'
                 'r.setCapture(1, "left");\n'
                 'console.log(r.captured(1), s(1, "pointermove", 150, 0), s(1, "pointermove", 999, 0), s(2, '
                 '"pointermove", 150, 0), r.captured(2));\n'
                 'console.log(s(1, "pointerup", 150, 0), r.captured(1), s(1, "pointermove", 150, 0));\n'
                 'r.setCapture(3, "knob"); r.setCapture(4, "slider"); console.log(s(3, "pointermove", 1, 1), '
                 's(4, "pointermove", 1, 1), s(3, "pointercancel", 1, 1), r.captured(3), r.captured(4));\n'
                 'r.releaseCapture(4); console.log(r.captured(4), s(4, "pointermove", 20, 0));\n',
       'hint': 'Map «pointerId → элемент»; при up и cancel захват снимается после определения получателя.',
       'expected': ['left right null',
                    'left left left right null',
                    'left null right',
                    'knob slider knob null slider',
                    'null left']},
      {'id': 'j16-coords',
       'mode': 'js',
       'title': 'Координаты событий',
       'statement': 'Элемент: { left, top, width, height } (в координатах окна — getBoundingClientRect), '
                    'scroll = { x, y } — прокрутка документа, scale — коэффициент масштаба элемента (CSS '
                    'transform: scale). Напишите функции pageToClient(p, scroll) / clientToPage(p, scroll), '
                    'clientToElement(p, rect, scale = 1) → { x, y } в локальных координатах (без масштаба: '
                    'делится на scale; для элемента с transform-origin: top left), и relative(p, rect) → { '
                    'rx, ry } в долях 0–1 от размера (с ограничением в диапазон 0–1) — для ползунков: rx — '
                    'доля слева направо.',
       'starter': 'function pageToClient(p, scroll) {\n'
                  '}\n'
                  'function clientToPage(p, scroll) {\n'
                  '}\n'
                  'function clientToElement(p, rect, scale) {\n'
                  '}\n'
                  'function relative(p, rect) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const rect = { left: 100, top: 50, width: 200, height: 100 };\n'
                 'console.log(JSON.stringify(pageToClient({ x: 500, y: 900 }, { x: 0, y: 800 })), '
                 'JSON.stringify(clientToPage({ x: 40, y: 20 }, { x: 10, y: 800 })));\n'
                 'console.log(JSON.stringify(clientToElement({ x: 150, y: 70 }, rect)), '
                 'JSON.stringify(clientToElement({ x: 300, y: 150 }, rect, 2)), '
                 'JSON.stringify(clientToElement({ x: 50, y: 10 }, rect)));\n'
                 'console.log(JSON.stringify(relative({ x: 200, y: 100 }, rect)), JSON.stringify(relative({ '
                 'x: 0, y: 500 }, rect)), JSON.stringify(relative({ x: 300, y: 50 }, rect)));\n'
                 'const p = clientToPage({ x: 5, y: 5 }, { x: 3, y: 4 }); '
                 'console.log(JSON.stringify(pageToClient(p, { x: 3, y: 4 })));\n',
       'hint': 'Простая арифметика; для масштаба делите на scale.',
       'expected': ['{"x":500,"y":100} {"x":50,"y":820}',
                    '{"x":50,"y":20} {"x":100,"y":50} {"x":-50,"y":-40}',
                    '{"rx":0.5,"ry":0.5} {"rx":0,"ry":1} {"rx":1,"ry":0}',
                    '{"x":5,"y":5}']},
      {'id': 'j16-hover-enter-leave',
       'mode': 'js',
       'title': 'mouseenter и mouseleave из перемещений',
       'statement': 'Элементы — дерево с parent-связями. Напишите функцию hoverEvents(prev, next): prev и '
                    'next — узлы под курсором до и после перемещения (или null). Возвращает массив событий в '
                    'порядке отправки: сначала mouseout для prev (всплывает) и mouseleave для каждого узла, '
                    'который курсор покинул (от самого внутреннего к внешнему; не всплывают), затем '
                    'mouseover для next и mouseenter для каждого вошедшего узла (от внешнего к внутреннему). '
                    'Формат: «тип:id». Если prev === next — пусто. Общий предок prev и next остаётся '
                    '«наведённым» (для него событий нет).',
       'starter': 'function hoverEvents(prev, next) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const node = (id, parent = null) => ({ id, parent, listeners: [] });\n'
                 'const on = (n, type, fn, opts = {}) => n.listeners.push({ type, fn, capture: '
                 '!!opts.capture, once: !!opts.once, passive: !!opts.passive });\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const root = node("root"), menu = node("menu", root), item = node("item", menu), sub = '
                 'node("sub", item), other = node("other", root), deep = node("deep", other);\n'
                 'const show = (p, n) => console.log(`${p?.id ?? "∅"} → ${n?.id ?? "∅"}:`, hoverEvents(p, '
                 'n).join(" "));\n'
                 'show(null, root); show(null, sub); show(sub, null); show(item, sub); show(sub, item); '
                 'show(sub, deep); show(sub, sub); show(menu, other); show(deep, root); show(root, deep);\n',
       'hint': 'Цепочки предков prev и next; общие узлы отбрасываются; порядок: leave изнутри наружу, enter '
               'снаружи внутрь.',
       'expected': ['∅ → root: mouseover:root mouseenter:root',
                    '∅ → sub: mouseover:sub mouseenter:root mouseenter:menu mouseenter:item mouseenter:sub',
                    'sub → ∅: mouseout:sub mouseleave:sub mouseleave:item mouseleave:menu mouseleave:root',
                    'item → sub: mouseout:item mouseover:sub mouseenter:sub',
                    'sub → item: mouseout:sub mouseleave:sub mouseover:item',
                    'sub → deep: mouseout:sub mouseleave:sub mouseleave:item mouseleave:menu mouseover:deep '
                    'mouseenter:other mouseenter:deep',
                    'sub → sub:',
                    'menu → other: mouseout:menu mouseleave:menu mouseover:other mouseenter:other',
                    'deep → root: mouseout:deep mouseleave:deep mouseleave:other mouseover:root',
                    'root → deep: mouseout:root mouseover:deep mouseenter:other mouseenter:deep']},
      {'id': 'j16-focus-trap',
       'mode': 'js',
       'title': 'Ловушка фокуса в модальном окне',
       'statement': 'Фокусируемые элементы заданы массивом id в порядке Tab внутри модального окна; focus — '
                    'текущий id или null (фокус снаружи). Напишите функцию trapFocus(items, focus, shiftKey) '
                    '→ id, на который перейдёт фокус при нажатии Tab (shiftKey — Shift+Tab): по кругу внутри '
                    'окна; если фокус снаружи (null или id не из списка) — первый элемент (при Shift — '
                    'последний); если список пуст — null. И функцию restoreFocus(stack) → id, куда вернуть '
                    'фокус при закрытии верхнего окна: stack — массив id элементов, которые были в фокусе в '
                    'момент открытия окон (последний — для верхнего окна); возвращает последний и удаляет '
                    'его из массива (изменяет stack), или null.',
       'starter': 'function trapFocus(items, focus, shiftKey) {\n}\nfunction restoreFocus(stack) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const items = ["close", "name", "email", "ok"];\n'
                 'console.log(trapFocus(items, "name", false), trapFocus(items, "ok", false), '
                 'trapFocus(items, "close", true), trapFocus(items, null, false), trapFocus(items, null, '
                 'true), trapFocus(items, "outside", false), trapFocus([], "x", false), trapFocus(["only"], '
                 '"only", false), trapFocus(["only"], "only", true));\n'
                 'const st = ["open-btn", "menu-item"];\n'
                 'console.log(restoreFocus(st), restoreFocus(st), restoreFocus(st), st.length);\n',
       'hint': 'Индекс по кругу; для фокуса снаружи — первый или последний.',
       'expected': ['email close ok close ok close null only only', 'menu-item open-btn null 0']},
      {'id': 'j16-listbox-nav',
       'mode': 'js',
       'title': 'Клавиатурная навигация по списку',
       'statement': 'Напишите функцию listboxKey(state, key): state = { items: [строки], active: индекс или '
                    '-1, typed: "", typedAt: 0 } (поле now передаётся третьим аргументом: время мс). '
                    'Клавиши: ArrowDown/ArrowUp (по кругу? нет — упираются в границы; из -1 ArrowDown даёт '
                    '0, ArrowUp — последний), Home, End, одиночный печатный символ — «поиск набором»: если с '
                    'последнего символа прошло меньше 500 мс, символы склеиваются в строку поиска, иначе '
                    'начинается новая; активным становится первый (начиная с active + 1 по кругу, если '
                    'набран один символ; для строки из нескольких — с текущего) элемент, чьё начало '
                    'совпадает без учёта регистра; если не найден — active не меняется. Возвращает новое '
                    'состояние (исходное не меняется): { ...state, active, typed, typedAt }.',
       'starter': 'function listboxKey(state, key, now) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const items = Object.freeze(["Алматы", "Берлин", "Бостон", "Брюссель", "Варшава", '
                 '"Вена"]);\n'
                 'let s = { items, active: -1, typed: "", typedAt: 0 };\n'
                 'const k = (key, now) => { s = listboxKey(s, key, now); console.log(key.padEnd(10), '
                 's.active, JSON.stringify(s.typed)); };\n'
                 'k("ArrowDown", 0); k("ArrowDown", 0); k("End", 0); k("ArrowDown", 0); k("ArrowUp", 0); '
                 'k("Home", 0); k("ArrowUp", 0);\n'
                 'k("б", 1000); k("б", 1600); k("о", 1800); k("ю", 2000); k("в", 3000); k("в", 3100); k("ф", '
                 '4000); k("а", 9000);\n'
                 'console.log(listboxKey({ items: [], active: -1, typed: "", typedAt: 0 }, "ArrowDown", '
                 '0).active, JSON.stringify(items));\n'
                 'const t = { items, active: -1, typed: "", typedAt: 0 }; listboxKey(t, "ArrowDown", 0); '
                 'console.log(t.active);\n',
       'hint': 'Поиск набором: накапливайте строку, если пауза меньше 500 мс; ищите по кругу от нужной '
               'позиции.',
       'expected': ['ArrowDown  0 ""',
                    'ArrowDown  1 ""',
                    'End        5 ""',
                    'ArrowDown  5 ""',
                    'ArrowUp    4 ""',
                    'Home       0 ""',
                    'ArrowUp    0 ""',
                    'б          1 "б"',
                    'б          2 "б"',
                    'о          2 "бо"',
                    'ю          2 "бою"',
                    'в          4 "в"',
                    'в          4 "вв"',
                    'ф          4 "ф"',
                    'а          0 "а"',
                    '-1 ["Алматы","Берлин","Бостон","Брюссель","Варшава","Вена"]',
                    '-1']},
      {'id': 'j16-click-outside',
       'mode': 'js',
       'title': 'Клик вне компонента',
       'statement': 'Напишите функцию createOutsideClick(isInside, onOutside): isInside(node) → boolean — '
                    'лежит ли узел внутри компонента. Возвращает { pointerDown(event), pointerUp(event), '
                    'click(event) } (event = { target, composedPath? [узлы] }): внешним считается клик, у '
                    'которого и нажатие, и отпускание были вне компонента (чтобы выделение мышью, начатое '
                    'внутри и закончившееся снаружи, не закрывало окно); при composedPath проверяется любой '
                    'узел пути (тень DOM), иначе target. Если по тому же клику внутри сработал '
                    'stopPropagation (event.cancelBubble === true на момент click), закрытие всё равно '
                    'срабатывает — но не срабатывает, если event.defaultPrevented. onOutside(event) '
                    'вызывается из click.',
       'starter': 'function createOutsideClick(isInside, onOutside) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const inside = new Set(["panel", "panel-btn"]);\n'
                 'const log = [];\n'
                 'const o = createOutsideClick((n) => inside.has(n), (e) => log.push("close:" + e.target));\n'
                 'const E = (target, extra = {}) => ({ target, ...extra });\n'
                 'const cycle = (down, up, click) => { o.pointerDown(down); o.pointerUp(up); o.click(click); '
                 'const r = log.join(); log.length = 0; return r || "—"; };\n'
                 'console.log(cycle(E("page"), E("page"), E("page")));\n'
                 'console.log(cycle(E("panel"), E("panel"), E("panel")));\n'
                 'console.log(cycle(E("panel"), E("page"), E("page")));\n'
                 'console.log(cycle(E("page"), E("panel"), E("panel")));\n'
                 'console.log(cycle(E("page"), E("page"), E("page", { defaultPrevented: true })));\n'
                 'console.log(cycle(E("host", { composedPath: ["shadow-child", "panel", "host"] }), '
                 'E("host", { composedPath: ["panel"] }), E("host")));\n'
                 'console.log(cycle(E("page", { composedPath: ["page", "body"] }), E("page", { composedPath: '
                 '["page"] }), E("page")));\n'
                 'o.pointerDown(E("page")); o.pointerUp(E("page")); o.click(E("x")); log.length = 0; '
                 'console.log(cycle(E("panel"), E("panel"), E("page")));\n',
       'hint': 'Запоминайте, где было нажатие и где отпускание; click сравнивает оба и сбрасывает флаги.',
       'expected': ['close:page', '—', '—', '—', '—', '—', 'close:page', '—']},
      {'id': 'j16-event-bus',
       'mode': 'js',
       'title': 'Шина событий с подстановками',
       'statement': 'Напишите функцию createBus(): возвращает { on(pattern, fn) → off, once(pattern, fn), '
                    'emit(topic, payload) → число вызванных обработчиков, off(pattern, fn), clear() }. Темы '
                    '— «user.login», «cart.item.added»; pattern: точная тема, «user.*» (одна часть вместо '
                    'звёздочки), «user.**» (одна или больше частей), «**» (любая). Обработчики вызываются в '
                    'порядке подписки; fn(payload, topic); исключение в одном не мешает остальным и копится: '
                    'emit после всех вызовов бросает AggregateError с ошибками (если они были).',
       'starter': 'function createBus() {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const bus = createBus();\n'
                 'const log = [];\n'
                 'const h = (n) => (p, t) => log.push(`${n}:${t}:${p}`);\n'
                 'bus.on("user.login", h("exact")); bus.on("user.*", h("star")); bus.on("user.**", '
                 'h("deep")); bus.on("**", h("all")); bus.once("cart.add", h("once"));\n'
                 'console.log(bus.emit("user.login", 1), log.join(" ")); log.length = 0;\n'
                 'console.log(bus.emit("user.profile.update", 2), log.join(" ")); log.length = 0;\n'
                 'console.log(bus.emit("cart.add", 3), bus.emit("cart.add", 4), log.join(" ")); log.length = '
                 '0;\n'
                 'console.log(bus.emit("user", 5), bus.emit("nothing.here", 6), log.join(" ")); log.length = '
                 '0;\n'
                 'const off = bus.on("a.b", h("tmp")); bus.emit("a.b", 1); off(); bus.emit("a.b", 2); '
                 'console.log(log.filter((x) => x.startsWith("tmp")).length);\n'
                 'const f = h("f"); bus.on("x", f); bus.off("x", f); log.length = 0; bus.emit("x", 0); '
                 'console.log(log.filter((x) => x.startsWith("f:")).length);\n'
                 'bus.on("err", () => { throw new Error("A"); }); bus.on("err", h("после ошибки")); '
                 'bus.on("err", () => { throw new Error("B"); });\n'
                 'log.length = 0; try { bus.emit("err", 1); } catch (e) { console.log(e.name, '
                 'e.errors.map((x) => x.message).join(), log.filter((x) => x.startsWith("после")).length); '
                 '}\n'
                 'bus.clear(); console.log(bus.emit("user.login", 9));\n',
       'hint': 'Превращайте шаблон в регулярное выражение: * — одна часть, ** — одна или больше; ошибки '
               'копите в массив.',
       'expected': ['4 exact:user.login:1 star:user.login:1 deep:user.login:1 all:user.login:1',
                    '2 deep:user.profile.update:2 all:user.profile.update:2',
                    '2 1 all:cart.add:3 once:cart.add:3 all:cart.add:4',
                    '1 1 all:user:5 all:nothing.here:6',
                    '1',
                    '0',
                    'AggregateError A,B 1',
                    '0']},
      {'id': 'j16-wheel',
       'mode': 'js',
       'title': 'Нормализация колеса мыши',
       'statement': 'Событие wheel имеет deltaMode: 0 — пиксели, 1 — строки, 2 — страницы. Напишите функцию '
                    'normalizeWheel(e, { lineHeight = 16, pageHeight = 800 }): e = { deltaX, deltaY, '
                    'deltaMode, shiftKey? } → { x, y } в пикселях; если shiftKey и deltaX = 0 — вертикальная '
                    'прокрутка превращается в горизонтальную (x = y пересчитанное, y = 0). И функцию '
                    'accumulate(events, threshold): прокрутка тачпадом даёт мелкие значения; accumulate '
                    'накапливает deltaY (после нормализации) и возвращает массив шагов: каждый раз при '
                    'накоплении ≥ threshold (по модулю) выдаёт шаг ±1 и вычитает threshold (остаток '
                    'сохраняется).',
       'starter': 'function normalizeWheel(e, options) {\n}\nfunction accumulate(events, threshold) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const W = (deltaY, extra = {}) => ({ deltaX: 0, deltaY, deltaMode: 0, ...extra });\n'
                 'for (const e of [W(100), W(3, { deltaMode: 1 }), W(1, { deltaMode: 2 }), W(-50, { '
                 'shiftKey: true }), W(10, { deltaX: 5, shiftKey: true }), { deltaX: 20, deltaY: 0, '
                 'deltaMode: 1 }]) console.log(JSON.stringify(normalizeWheel(e)));\n'
                 'console.log(JSON.stringify(normalizeWheel(W(2, { deltaMode: 1 }), { lineHeight: 20 })), '
                 'JSON.stringify(normalizeWheel(W(1, { deltaMode: 2 }), { pageHeight: 600 })));\n'
                 'console.log(JSON.stringify(accumulate([W(10), W(10), W(10), W(10)], 25)), '
                 'JSON.stringify(accumulate([W(100)], 30)), JSON.stringify(accumulate([W(-40), W(-40)], '
                 '50)), JSON.stringify(accumulate([W(20), W(-20), W(20)], 30)), '
                 'JSON.stringify(accumulate([], 10)));\n',
       'hint': 'deltaMode задаёт множитель в пикселях; накопление — остаток после вычитания шага.',
       'expected': ['{"x":0,"y":100}',
                    '{"x":0,"y":48}',
                    '{"x":0,"y":800}',
                    '{"x":-50,"y":0}',
                    '{"x":5,"y":10}',
                    '{"x":320,"y":0}',
                    '{"x":0,"y":40} {"x":0,"y":600}',
                    '[1] [1,1,1] [-1] [] []']},
      {'id': 'j16-key-repeat',
       'mode': 'js',
       'title': 'Автоповтор клавиш',
       'statement': 'Поток событий клавиатуры: { type: "down"|"up", code, t }. Браузер при удержании клавиши '
                    'шлёт повторные keydown (repeat: true) без keyup. Напишите функцию processKeys(events): '
                    'возвращает { actions: [«code:down»/«code:up» только для первых нажатий и отпусканий], '
                    'repeats: число подавленных повторов, held: отсортированный массив code, оставшихся '
                    'нажатыми в конце }. Повторный down той же клавиши без up считается повтором; up без '
                    'предшествующего down игнорируется (не попадает в actions).',
       'starter': 'function processKeys(events) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const ev = (s) => s.split(" ").map((x, i) => { const [type, code] = x.split(":"); return { '
                 'type, code, t: i * 10 }; });\n'
                 'console.log(JSON.stringify(processKeys(ev("down:KeyA down:KeyA down:KeyA up:KeyA"))));\n'
                 'console.log(JSON.stringify(processKeys(ev("down:ShiftLeft down:KeyA down:KeyA up:KeyA '
                 'up:ShiftLeft"))));\n'
                 'console.log(JSON.stringify(processKeys(ev("up:KeyX down:KeyB down:KeyC up:KeyB"))));\n'
                 'console.log(JSON.stringify(processKeys(ev("down:Space down:Space"))), '
                 'JSON.stringify(processKeys([])));\n'
                 'console.log(JSON.stringify(processKeys(ev("down:KeyA up:KeyA down:KeyA up:KeyA '
                 'up:KeyA"))));\n',
       'hint': 'Множество нажатых клавиш: down для уже нажатой — повтор.',
       'expected': ['{"actions":["KeyA:down","KeyA:up"],"repeats":2,"held":[]}',
                    '{"actions":["ShiftLeft:down","KeyA:down","KeyA:up","ShiftLeft:up"],"repeats":1,"held":[]}',
                    '{"actions":["KeyB:down","KeyC:down","KeyB:up"],"repeats":0,"held":["KeyC"]}',
                    '{"actions":["Space:down"],"repeats":1,"held":["Space"]} '
                    '{"actions":[],"repeats":0,"held":[]}',
                    '{"actions":["KeyA:down","KeyA:up","KeyA:down","KeyA:up"],"repeats":0,"held":[]}']},
      {'id': 'j16-composition',
       'mode': 'js',
       'title': 'Ввод через IME',
       'statement': 'Напишите функцию createInputProcessor(onCommit): метод handle(e), где e = { type: '
                    '"compositionstart"|"compositionupdate"|"compositionend"|"input"|"keydown", data?, key? '
                    '}. Пока идёт композиция, события input и keydown не обрабатываются как ввод текста '
                    '(игнорируются), а при compositionend итоговый текст data коммитится: onCommit(data) '
                    'один раз; вне композиции input с data коммитит data, keydown с key длиной 1 (без '
                    'модификаторов) коммитит key, Enter коммитит "\\n". Метод state() — { composing, preedit '
                    '} (preedit — последний data из compositionupdate; пусто вне композиции). Событие '
                    'compositionend, после которого сразу приходит input с тем же data (как в части '
                    'браузеров), не должно коммитить дважды.',
       'starter': 'function createInputProcessor(onCommit) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const out = [];\n'
                 'const p = createInputProcessor((t) => out.push(JSON.stringify(t)));\n'
                 'const feed = (...es) => { for (const e of es) p.handle(typeof e === "string" ? { type: e } '
                 ': e); };\n'
                 'feed({ type: "keydown", key: "a" }, { type: "keydown", key: "Enter" }, { type: "keydown", '
                 'key: "Shift" }, { type: "keydown", key: "c", ctrlKey: true }, { type: "input", data: "z" '
                 '});\n'
                 'console.log(out.join(" "), JSON.stringify(p.state())); out.length = 0;\n'
                 'feed("compositionstart", { type: "compositionupdate", data: "ni" }, { type: "keydown", '
                 'key: "i" }, { type: "input", data: "ni" });\n'
                 'console.log(out.length, JSON.stringify(p.state()));\n'
                 'feed({ type: "compositionupdate", data: "你" }, { type: "compositionend", data: "你" }, { '
                 'type: "input", data: "你" });\n'
                 'console.log(out.join(" "), JSON.stringify(p.state())); out.length = 0;\n'
                 'feed({ type: "input", data: "你" });\n'
                 'console.log(out.join(" "));\n'
                 'feed("compositionstart", { type: "compositionend", data: "" });\n'
                 'console.log(out.length, JSON.stringify(p.state()));\n'
                 'feed({ type: "compositionstart" }, { type: "compositionend", data: "好" }, { type: '
                 '"keydown", key: "x" }, { type: "input", data: "好" });\n'
                 'console.log(out.join(" "));\n',
       'hint': 'Флаг composing и «последний закоммиченный» текст для подавления дубля input после '
               'compositionend.',
       'expected': ['"a" "\\n" "z" {"composing":false,"preedit":""}',
                    '0 {"composing":true,"preedit":"ni"}',
                    '"你" {"composing":false,"preedit":""}',
                    '"你"',
                    '1 {"composing":false,"preedit":""}',
                    '"你" "好" "x" "好"']},
      {'id': 'j16-phone-mask',
       'mode': 'js',
       'title': 'Маска ввода телефона',
       'statement': 'Напишите функцию formatPhone(raw): из любых введённых символов берутся цифры; ведущая '
                    '«8» или «7» заменяется на «7» (российский номер); результат — «+7 (999) 123-45-67» по '
                    'мере ввода: «+7», «+7 (9», «+7 (999», «+7 (999) 1», …, «+7 (999) 123-45-67»; лишние '
                    'цифры после 11-й отбрасываются; пустой ввод — пустая строка. И функцию '
                    'nextCaret(formatted, digitsBefore) → индекс каретки в отформатированной строке после '
                    'заданного числа цифр (для пересчёта позиции при редактировании).',
       'starter': 'function formatPhone(raw) {\n}\nfunction nextCaret(formatted, digitsBefore) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const r of ["", "8", "89", "89991", "8999", "89991234567", "+7 (999) 123-45-67", '
                 '"9991234567", "7 999 123 45 67 89", "abc", "+7", "(999)"]) console.log(JSON.stringify(r), '
                 '"→", JSON.stringify(formatPhone(r)));\n'
                 'const f = formatPhone("89991234567");\n'
                 'console.log(nextCaret(f, 0), nextCaret(f, 1), nextCaret(f, 2), nextCaret(f, 4), '
                 'nextCaret(f, 7), nextCaret(f, 11), nextCaret(f, 99), nextCaret("", 3));\n',
       'hint': 'Оставьте цифры, уберите ведущую 7/8, затем добавляйте разделители по длине.',
       'expected': ['"" → ""',
                    '"8" → "+7"',
                    '"89" → "+7 (9"',
                    '"89991" → "+7 (999) 1"',
                    '"8999" → "+7 (999)"',
                    '"89991234567" → "+7 (999) 123-45-67"',
                    '"+7 (999) 123-45-67" → "+7 (999) 123-45-67"',
                    '"9991234567" → "+7 (999) 123-45-67"',
                    '"7 999 123 45 67 89" → "+7 (999) 123-45-67"',
                    '"abc" → ""',
                    '"+7" → "+7"',
                    '"(999)" → "+7 (999)"',
                    '0 2 5 7 12 18 18 0']},
      {'id': 'j16-disposables',
       'mode': 'js',
       'title': 'Подписки на компонент и их снятие',
       'statement': 'Напишите класс Disposables: add(fn) (регистрирует функцию очистки; возвращает её же), '
                    'listen(target, type, handler, options) (target.addEventListener и регистрация снятия '
                    'через removeEventListener с теми же options), interval(fn, ms, timers) (setInterval '
                    'через timers = { setInterval, clearInterval }; снятие — clearInterval), и dispose() — '
                    'вызывает все очистки в обратном порядке, один раз (повторный dispose ничего не делает); '
                    'ошибка в одной очистке не мешает остальным и собирается: после всех бросается '
                    'AggregateError. Свойство size — число зарегистрированных очисток.',
       'starter': 'class Disposables {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import { EventEmitter } from "node:events";\n'
                 'const target = { e: new EventEmitter(), addEventListener(t, h, o) { this.e.on(t, h); }, '
                 'removeEventListener(t, h, o) { this.e.off(t, h); } };\n'
                 'const intervals = new Set(); let nid = 0;\n'
                 'const timers = { setInterval: (fn, ms) => { const id = ++nid; intervals.add(id); return '
                 'id; }, clearInterval: (id) => intervals.delete(id) };\n'
                 'const log = [];\n'
                 'const d = new Disposables();\n'
                 'd.listen(target, "click", () => log.push("click")); d.listen(target, "key", () => '
                 'log.push("key"));\n'
                 'd.interval(() => {}, 100, timers);\n'
                 'd.add(() => log.push("очистка 1"));\n'
                 'console.log(d.size, target.e.listenerCount("click"), target.e.listenerCount("key"), '
                 'intervals.size);\n'
                 'd.dispose();\n'
                 'console.log(target.e.listenerCount("click"), target.e.listenerCount("key"), '
                 'intervals.size, log.join(), d.size);\n'
                 'd.dispose(); console.log(log.length);\n'
                 'const e = new Disposables();\n'
                 'e.add(() => log.push("a")); e.add(() => { throw new Error("сбой 1"); }); e.add(() => '
                 'log.push("b")); e.add(() => { throw new Error("сбой 2"); });\n'
                 'log.length = 0;\n'
                 'try { e.dispose(); } catch (x) { console.log(x.name, x.errors.map((y) => '
                 'y.message).join(), log.join()); }\n'
                 'console.log(typeof new Disposables().add(() => 1));\n',
       'hint': 'Массив функций очистки; dispose идёт с конца и собирает исключения.',
       'expected': ['4 1 1 1', '0 0 0 очистка 1 0', '1', 'AggregateError сбой 2,сбой 1 b,a', 'function']},
      {'id': 'j16-recorder',
       'mode': 'js',
       'title': 'Запись и воспроизведение событий',
       'statement': 'Напишите функцию createRecorder(now): возвращает { record(event), stop() → массив '
                    'записей { event, dt (мс с начала записи) }, } и функцию replay(log, dispatch, timers, '
                    'speed = 1): планирует вызов dispatch(event) через setTimeout в моменты dt / speed '
                    '(timers = { setTimeout }); возвращает функцию cancel(), отменяющую ещё не выполненные. '
                    'record до start игнорируется: запись идёт между первым record (момент 0) и stop; после '
                    'stop record игнорируется.',
       'starter': 'function createRecorder(now) {\n}\nfunction replay(log, dispatch, timers, speed) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const node = (id, parent = null) => ({ id, parent, listeners: [] });\n'
                 'const on = (n, type, fn, opts = {}) => n.listeners.push({ type, fn, capture: '
                 '!!opts.capture, once: !!opts.once, passive: !!opts.passive });\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'let t = 1000;\n'
                 'const rec = createRecorder(() => t);\n'
                 'rec.record({ type: "down", x: 1 }); t += 40; rec.record({ type: "move", x: 5 }); t += 60; '
                 'rec.record({ type: "up", x: 9 });\n'
                 'const log = rec.stop(); t += 500; rec.record({ type: "late" });\n'
                 'console.log(JSON.stringify(log), rec.stop().length, createRecorder(() => '
                 '0).stop().length);\n'
                 'const c = FAKE(); const out = [];\n'
                 'replay(log, (e) => out.push(e.type + "@" + c.now()), c, 1); c.advance(1000); '
                 'console.log(out.join(" "));\n'
                 'out.length = 0; replay(log, (e) => out.push(e.type + "@" + c.now()), c, 2); '
                 'c.advance(1000); console.log(out.join(" "));\n'
                 'out.length = 0; const cancel = replay(log, (e) => out.push(e.type), c, 1); c.advance(50); '
                 'cancel(); c.advance(1000); console.log(out.join(" "), c.pending());\n',
       'hint': 'dt считается от первого record; replay ставит таймеры с делением на скорость.',
       'expected': ['[{"event":{"type":"down","x":1},"dt":0},{"event":{"type":"move","x":5},"dt":40},{"event":{"type":"up","x":9},"dt":100}] '
                    '3 0',
                    'down@0 move@40 up@100',
                    'down@1000 move@1020 up@1050',
                    'down move 0']},
      {'id': 'j16-tap-vs-scroll',
       'mode': 'js',
       'title': 'Касание: тап, прокрутка или удержание',
       'statement': 'Напишите функцию classifyTouch(points, { tapMaxMove = 10, tapMaxTime = 300 }): points — '
                    'массив { x, y, t } одного касания (первая — touchstart, последняя — touchend). '
                    'Результат: «tap» (движение от начальной точки не больше tapMaxMove на протяжении всего '
                    'касания и общее время ≤ tapMaxTime), «long-press» (движение небольшое, время больше '
                    'tapMaxTime), «scroll-v» (максимальное смещение по вертикали больше tapMaxMove и больше '
                    'по модулю смещения по горизонтали), «scroll-h» (аналогично по горизонтали). Для одной '
                    'точки — «tap».',
       'starter': 'function classifyTouch(points, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const P = (...xs) => xs.map(([x, y, t]) => ({ x, y, t }));\n'
                 'for (const pts of [P([5, 5, 0]), P([5, 5, 0], [6, 6, 100]), P([5, 5, 0], [6, 6, 301]), '
                 'P([5, 5, 0], [5, 60, 100]), P([5, 5, 0], [80, 20, 100]), P([5, 5, 0], [5, 30, 50], [5, 5, '
                 '120]), P([0, 0, 0], [10, 0, 300]), P([0, 0, 0], [11, 0, 300]), P([0, 0, 0], [30, 30, '
                 '100]), P([0, 0, 0], [-40, 5, 200])]) console.log(classifyTouch(pts));\n'
                 'console.log(classifyTouch(P([0, 0, 0], [3, 3, 500]), { tapMaxTime: 1000 }), '
                 'classifyTouch(P([0, 0, 0], [20, 0, 10]), { tapMaxMove: 30 }));\n',
       'hint': 'Максимальное отклонение от начальной точки за всё касание, затем время.',
       'expected': ['tap',
                    'tap',
                    'long-press',
                    'scroll-v',
                    'scroll-h',
                    'scroll-v',
                    'tap',
                    'scroll-h',
                    'scroll-v',
                    'scroll-h',
                    'tap tap']},
      {'id': 'j16-activate',
       'mode': 'js',
       'title': 'Клавиатурная активация «кнопки»',
       'statement': 'Элемент с role="button" должен вести себя как <button>: Enter вызывает действие на '
                    'keydown (и повторяется при удержании, если repeat), Space — на keyup (и только если '
                    'keydown Space был на этом же элементе), при этом на keydown пробела нужно отменить '
                    'прокрутку страницы (preventDefault). Напишите функцию createButtonKeys(activate): '
                    'возвращает { keydown(e), keyup(e) } с e = { key, repeat?, preventDefault() }; '
                    'activate() вызывается как у настоящей кнопки; Space во время удержания (keydown подряд) '
                    'не активирует; потеря фокуса — метод blur() сбрасывает ожидание пробела. Другие клавиши '
                    'игнорируются (preventDefault не вызывается).',
       'starter': 'function createButtonKeys(activate) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let n = 0, prevented = 0;\n'
                 'const k = createButtonKeys(() => n++);\n'
                 'const e = (key, extra = {}) => ({ key, preventDefault: () => prevented++, ...extra });\n'
                 'k.keydown(e("Enter")); console.log(n, prevented);\n'
                 'k.keydown(e("Enter", { repeat: true })); console.log(n);\n'
                 'k.keydown(e(" ")); console.log(n, prevented);\n'
                 'k.keydown(e(" ", { repeat: true })); console.log(n);\n'
                 'k.keyup(e(" ")); console.log(n);\n'
                 'k.keyup(e(" ")); console.log(n);\n'
                 'k.keydown(e("a")); k.keyup(e("a")); console.log(n, prevented);\n'
                 'k.keyup(e(" ")); console.log("keyup без keydown:", n);\n'
                 'k.keydown(e(" ")); k.blur(); k.keyup(e(" ")); console.log("после blur:", n);\n'
                 'k.keyup(e("Enter")); console.log(n);\n',
       'hint': 'Флаг «пробел нажат» ставится на keydown и снимается на keyup/blur.',
       'expected': ['1 1', '2', '2 3', '2', '3', '3', '3 4', 'keyup без keydown: 3', 'после blur: 3', '3']},
      {'id': 'j16-drag-sort',
       'mode': 'js',
       'title': 'Сортировка перетаскиванием',
       'statement': 'Элементы списка в столбик, высота каждого — heights[i]. Напишите функцию '
                    'dropIndex(heights, from, y): индекс, на который попадёт перетаскиваемый элемент from, '
                    'если его отпустили с центром в точке y (отсчёт от верха списка, пока элемент вынут из '
                    'списка): считается положение центров оставшихся элементов; элемент встаёт перед первым '
                    'элементом, центр которого ниже y, иначе в конец. И reorder(items, from, to) → новый '
                    'массив с элементом, перенесённым на позицию to (индекс в итоговом списке); исходный не '
                    'меняется.',
       'starter': 'function dropIndex(heights, from, y) {\n}\nfunction reorder(items, from, to) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const h = [40, 40, 40, 40];\n'
                 'console.log([0, 19, 20, 21, 60, 100, 140, 1000, -50].map((y) => dropIndex(h, 0, '
                 'y)).join());\n'
                 'console.log([0, 50, 90].map((y) => dropIndex(h, 3, y)).join(), dropIndex([30, 60, 30], 1, '
                 '40), dropIndex([30, 60, 30], 1, 44), dropIndex([30], 0, 5), dropIndex([], 0, 5));\n'
                 'const a = Object.freeze(["a", "b", "c", "d"]);\n'
                 'console.log(JSON.stringify(reorder(a, 0, 2)), JSON.stringify(reorder(a, 3, 0)), '
                 'JSON.stringify(reorder(a, 1, 1)), JSON.stringify(a));\n'
                 'const from = 1; const to = dropIndex([10, 10, 10, 10], from, 35);\n'
                 'console.log(to, JSON.stringify(reorder(a, from, to)));\n',
       'hint': 'Выкиньте перетаскиваемый элемент из расчёта и ищите первый центр ниже y.',
       'expected': ['0,0,1,1,2,3,3,3,0',
                    '0,1,2 1 1 0 0',
                    '["b","c","a","d"] ["d","a","b","c"] ["a","b","c","d"] ["a","b","c","d"]',
                    '3 ["a","c","d","b"]']}]}
