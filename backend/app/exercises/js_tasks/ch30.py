"""Задачи книги «Современный Frontend»: глава 30."""

TASKS: dict[int, list[dict]] = {30: [{'id': 'j30-emit',
  'mode': 'js',
  'title': 'События компонента',
  'statement': 'Напишите createComponent({ props, emits }): возвращает { emit(name, ...args) }. '
               'Имя обработчика: «on» + имя события, где слова через «-» превращаются в camelCase '
               'с заглавной первой буквой (save → onSave, item-select → onItemSelect, update:value '
               '→ onUpdate:value — двоеточие сохраняется, а слово после него остаётся как есть). '
               'Если emits задан (массив) и name в нём нет — Error(\'Event "name" is not '
               "declared'). emit вызывает props[обработчик](...args), если это функция, и "
               'возвращает число вызванных обработчиков (0 или 1). Исключение обработчика '
               'пробрасывается.',
  'starter': 'function createComponent({ props, emits }) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const c = createComponent({ props: { onSave: (x) => log.push("save:" + x), '
            'onItemSelect: (a, b) => log.push(`sel:${a}${b}`), "onUpdate:value": (v) => '
            'log.push("v:" + v) }, emits: ["save", "item-select", "update:value", "close"] });\n'
            'console.log(c.emit("save", 1), c.emit("item-select", "a", "b"), '
            'c.emit("update:value", 5), c.emit("close"));\n'
            'console.log(log.join(" "));\n'
            'try { c.emit("other"); } catch (e) { console.log(e.message); }\n'
            'const free = createComponent({ props: {} });\n'
            'console.log(free.emit("anything", 1));\n'
            'try { createComponent({ props: { onBoom() { throw new Error("handler"); } } '
            '}).emit("boom"); } catch (e) { console.log(e.message); }\n',
  'hint': 'Разбейте имя по «-»: первое слово с заглавной, остальные тоже; для «update:value» — '
          'часть до двоеточия по тем же правилам.',
  'expected': ['1 1 1 0', 'save:1 sel:ab v:5', 'Event "other" is not declared', '0', 'handler']},
 {'id': 'j30-props',
  'mode': 'js',
  'title': 'Проверка и значения по умолчанию',
  'statement': 'Напишите resolveProps(schema, given): schema — { имя: { type, required, default, '
               "validator } }, type — 'string' | 'number' | 'boolean' | 'array' | 'object' | "
               "'function'. Результат { props, errors }. Для каждого имени схемы (в порядке "
               'схемы): значение given[имя]; если undefined — default (функция по умолчанию для '
               "array/object вызывается, для 'function' возвращается как есть), иначе если "
               'required — ошибка «Missing required prop: имя». Значение, не прошедшее проверку '
               "типа (null — не object; array — только 'array'; NaN — не number), — «Invalid prop: "
               'имя expected ТИП got ФАКТ» (ФАКТ: null/array/typeof), при этом в props попадает '
               'значение по умолчанию (если есть) или undefined. validator(value) false — «Invalid '
               'prop: имя failed custom validator». Свойства вне схемы переносятся в props как '
               'есть после известных.',
  'starter': 'function resolveProps(schema, given) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const schema = {\n'
            '  title: { type: "string", required: true },\n'
            '  size: { type: "string", default: "m", validator: (v) => ["s", "m", "l"].includes(v) '
            '},\n'
            '  count: { type: "number", default: 0 },\n'
            '  items: { type: "array", default: () => [] },\n'
            '  onSave: { type: "function" },\n'
            '  meta: { type: "object" },\n'
            '};\n'
            'const show = (g) => { const r = resolveProps(schema, g); '
            'console.log(JSON.stringify(r)); };\n'
            'show({ title: "T" });\n'
            'show({});\n'
            'show({ title: 5, size: "xl", count: NaN, items: {}, meta: [], extra: 1 });\n'
            'show({ title: "T", meta: null, count: "3" });\n'
            'show({ title: "T", items: [1], onSave: () => 1 });\n'
            'const a = resolveProps(schema, { title: "x" }).props.items, b = resolveProps(schema, '
            '{ title: "x" }).props.items;\n'
            'console.log(a !== b);\n',
  'hint': 'Функция kindOf(v); порядок: undefined → default/required, потом тип, потом валидатор.',
  'expected': ['{"props":{"title":"T","size":"m","count":0,"items":[]},"errors":[]}',
               '{"props":{"size":"m","count":0,"items":[]},"errors":["Missing required prop: '
               'title"]}',
               '{"props":{"size":"xl","count":0,"items":[],"extra":1},"errors":["Invalid prop: '
               'title expected string got number","Invalid prop: size failed custom '
               'validator","Invalid prop: count expected number got number","Invalid prop: items '
               'expected array got object","Invalid prop: meta expected object got array"]}',
               '{"props":{"title":"T","size":"m","count":0,"items":[]},"errors":["Invalid prop: '
               'count expected number got string","Invalid prop: meta expected object got null"]}',
               '{"props":{"title":"T","size":"m","count":0,"items":[1]},"errors":[]}',
               'true']},
 {'id': 'j30-slots',
  'mode': 'js',
  'title': 'Слоты',
  'statement': 'Напишите renderSlots(template, slots): template — строка с метками слотов: '
               '«<slot/>» или «<slot></slot>» — слот по умолчанию; «<slot name="имя"/>» или «<slot '
               'name="имя"></slot>» — именованный; у слота может быть запасное содержимое между '
               'тегами: «<slot name="a">запас</slot>». slots — объект «имя → строка»; слот по '
               "умолчанию — ключ 'default'. Метка заменяется содержимым слота, если оно задано и "
               'непустое (строка длиной > 0); иначе — запасным содержимым (пустая строка для '
               'самозакрывающихся). Остальной текст не меняется. Одинаковые слоты можно '
               'использовать несколько раз.',
  'starter': 'function renderSlots(template, slots) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const tpl = \'<div class="card"><header><slot '
            'name="header">Заголовок</slot></header><main><slot/></main><footer><slot '
            'name="footer"></slot></footer></div>\';\n'
            'console.log(renderSlots(tpl, { header: "H", default: "тело" }));\n'
            'console.log(renderSlots(tpl, {}));\n'
            'console.log(renderSlots(tpl, { header: "", footer: "F", default: "x" }));\n'
            'console.log(renderSlots("<slot/>|<slot name=\\"a\\"/>|<slot '
            'name=\\"a\\">fb</slot>|<slot>dflt</slot>", { a: "A" }));\n'
            'console.log(renderSlots("no slots here", { default: "x" }));\n',
  'hint': 'Одна replace с регулярным выражением '
          '/<slot(?:\\s+name="([^"]*)")?\\s*(?:\\/>|>([\\s\\S]*?)<\\/slot>)/g.',
  'expected': ['<div class="card"><header>H</header><main>тело</main><footer></footer></div>',
               '<div class="card"><header>Заголовок</header><main></main><footer></footer></div>',
               '<div class="card"><header>Заголовок</header><main>x</main><footer>F</footer></div>',
               '|A|A|dflt',
               'no slots here']},
 {'id': 'j30-context',
  'mode': 'js',
  'title': 'Контекст provide / inject',
  'statement': 'Напишите createNode(parent = null) → узел дерева компонентов с методами '
               'provide(key, value) и inject(key, fallback). provide записывает значение на узле. '
               'inject ищет значение, начиная с самого узла, затем у родителей вверх (ближайшее '
               'побеждает, в том числе значение undefined, если оно было явно предоставлено); если '
               'не найдено — fallback (если аргумент передан, даже undefined), иначе Error(`No '
               'provider for "key"`). Метод node.child() — создать дочерний узел. У узла есть поле '
               'parent.',
  'starter': 'function createNode(parent = null) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const root = createNode();\n'
            'root.provide("theme", "dark"); root.provide("lang", "en");\n'
            'const page = root.child(); page.provide("theme", "light");\n'
            'const button = page.child(); const other = root.child();\n'
            'console.log(button.inject("theme"), other.inject("theme"), button.inject("lang"), '
            'page.parent === root);\n'
            'try { button.inject("missing"); } catch (e) { console.log(e.message); }\n'
            'console.log(button.inject("missing", "dflt"), button.inject("missing", undefined));\n'
            'page.provide("flag", undefined);\n'
            'console.log(button.inject("flag", "dflt"), other.inject("flag", "dflt"));\n'
            'const solo = createNode(); console.log(solo.parent, solo.child().parent === solo);\n',
  'hint': 'Map значений на узле; различайте «fallback не передан» по arguments.length.',
  'expected': ['light dark en true',
               'No provider for "missing"',
               'dflt undefined',
               'undefined dflt',
               'null true']},
 {'id': 'j30-lifecycle',
  'mode': 'js',
  'title': 'Менеджер жизненного цикла',
  'statement': 'Напишите createInstance(setup): setup(ctx) вызывается один раз при создании и '
               'получает ctx = { onMount(fn), onUpdate(fn), onUnmount(fn) } для регистрации '
               'обратных вызовов. Экземпляр: { mount(), update(), unmount() }. mount() вызывает '
               'все onMount по порядку регистрации; если callback вернул функцию — она сохраняется '
               'как очистка. update() вызывает onUpdate по порядку. unmount() вызывает в обратном '
               'порядке регистрации (стек) все onUnmount-callbacks и очистки, возвращённые из '
               'onMount (очистка из onMount попадает в стек в момент mount, после тех onUnmount, '
               'что были зарегистрированы в setup). Повторный mount до unmount или unmount без '
               "mount — Error('Invalid state: ...') — mount дважды: 'already mounted', unmount без "
               "mount: 'not mounted'. update без mount — тоже 'not mounted'. После unmount можно "
               'смонтировать снова.',
  'starter': 'function createInstance(setup) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const inst = createInstance((ctx) => {\n'
            '  ctx.onMount(() => { log.push("mount1"); return () => log.push("cleanup1"); });\n'
            '  ctx.onUnmount(() => log.push("unmountA"));\n'
            '  ctx.onMount(() => { log.push("mount2"); });\n'
            '  ctx.onUpdate(() => log.push("update1"));\n'
            '  ctx.onMount(() => { log.push("mount3"); return () => log.push("cleanup3"); });\n'
            '  ctx.onUnmount(() => log.push("unmountB"));\n'
            '  ctx.onUpdate(() => log.push("update2"));\n'
            '});\n'
            'const t = (f) => { try { f(); } catch (e) { log.push("!" + e.message); } };\n'
            't(() => inst.update()); t(() => inst.unmount());\n'
            'inst.mount(); t(() => inst.mount());\n'
            'inst.update(); inst.update();\n'
            'inst.unmount();\n'
            'console.log(log.join(" "));\n'
            'log.length = 0;\n'
            'inst.mount(); inst.unmount();\n'
            'console.log(log.join(" "));\n',
  'hint': 'Состояние mounted, массивы хуков, стек очисток; unmount проходит стек с конца.',
  'expected': ['!Invalid state: not mounted !Invalid state: not mounted mount1 mount2 mount3 '
               '!Invalid state: already mounted update1 update2 update1 update2 cleanup3 cleanup1 '
               'unmountB unmountA',
               'mount1 mount2 mount3 cleanup3 cleanup1 unmountB unmountA']},
 {'id': 'j30-dispatch',
  'mode': 'js',
  'title': 'Всплытие событий',
  'statement': 'Напишите dispatchEvent(tree, targetId, type, payload): tree — { id, handlers?: { '
               'тип: [функции] }, children?: [...] }. Найдите путь от корня к узлу targetId (нет — '
               "Error('Target not found: id')). Событие всплывает от цели к корню (цель первой). "
               'На каждом узле вызываются обработчики данного типа в порядке массива, каждому '
               'передаётся объект события e = { type, target (id цели), currentTarget (id узла), '
               'payload, stopPropagation(), stopImmediatePropagation(), preventDefault(), '
               'defaultPrevented }. stopPropagation останавливает всплытие после обработчиков '
               'текущего узла; stopImmediatePropagation — немедленно (остальные обработчики узла '
               'тоже не вызываются). Возврат: { defaultPrevented, visited } — visited: id узлов, у '
               'которых вызван хотя бы один обработчик, в порядке вызова.',
  'starter': 'function dispatchEvent(tree, targetId, type, payload) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const h = (name, fn) => (e) => { log.push(`${name}@${e.currentTarget}`); if (fn) '
            'fn(e); };\n'
            'const tree = { id: "root", handlers: { click: [h("r1")] }, children: [\n'
            '  { id: "list", handlers: { click: [h("l1"), h("l2", (e) => e.stopPropagation()), '
            'h("l3")] }, children: [\n'
            '    { id: "item", handlers: { click: [h("i1", (e) => e.preventDefault())], input: '
            '[h("in")] }, children: [] },\n'
            '    { id: "plain", children: [{ id: "leaf", handlers: { click: [h("f1", (e) => '
            'e.stopImmediatePropagation()), h("f2")] } }] },\n'
            '  ] },\n'
            '] };\n'
            'const run = (id, type = "click") => { log.length = 0; const r = dispatchEvent(tree, '
            'id, type, { n: 1 }); console.log(id, JSON.stringify(r), log.join(" ")); };\n'
            'run("item"); run("leaf"); run("root"); run("item", "input"); run("plain", "other");\n'
            'try { dispatchEvent(tree, "ghost", "click"); } catch (e) { console.log(e.message); }\n'
            'let seen; dispatchEvent({ id: "a", handlers: { x: [(e) => { seen = [e.target, '
            'e.currentTarget, e.type, e.payload]; }] } }, "a", "x", 42); '
            'console.log(JSON.stringify(seen));\n',
  'hint': 'Рекурсивный поиск пути; цикл от конца пути к началу с флагами остановки.',
  'expected': ['item {"defaultPrevented":true,"visited":["item","list"]} i1@item l1@list l2@list '
               'l3@list',
               'leaf {"defaultPrevented":false,"visited":["leaf"]} f1@leaf',
               'root {"defaultPrevented":false,"visited":["root"]} r1@root',
               'item {"defaultPrevented":false,"visited":["item"]} in@item',
               'plain {"defaultPrevented":false,"visited":[]}',
               'Target not found: ghost',
               '["a","a","x",42]']},
 {'id': 'j30-delegate',
  'mode': 'js',
  'title': 'Делегирование событий',
  'statement': 'Модель узлов: { tag, id?, classes?: [..], parent, children }. Напишите '
               'closest(node, selector, root): поднимается от node к предкам (включая сам node) до '
               'root включительно и возвращает первый узел, подходящий под selector: «тег», '
               '«.класс», «#id» или комбинация без пробелов «тег.класс#id». Нет — null. Затем '
               'createDelegate(root): { on(selector, handler), dispatch(target) }: '
               'dispatch(target) для каждого зарегистрированного (в порядке регистрации) селектора '
               'находит closest(target, selector, root) и, если найден, вызывает handler(найденный '
               'узел, target). Возвращает число вызванных обработчиков.',
  'starter': 'function closest(node, selector, root) {\n}\nfunction createDelegate(root) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const n = (tag, extra = {}, kids = []) => { const node = { tag, ...extra, children: '
            'kids, parent: null }; kids.forEach((k) => (k.parent = node)); return node; };\n'
            'const icon = n("i", { classes: ["icon"] });\n'
            'const btn = n("button", { classes: ["btn", "primary"], id: "save" }, [icon]);\n'
            'const row = n("li", { classes: ["row"] }, [btn, n("span", { classes: ["label"] })]);\n'
            'const root = n("ul", { id: "list" }, [row]);\n'
            'const outside = n("div", { classes: ["btn"] }, [n("b")]);\n'
            'const sel = (s, node = icon, r = root) => { const c = closest(node, s, r); return c ? '
            'c.tag + (c.id ? "#" + c.id : "") : null; };\n'
            'console.log(sel("button"), sel(".btn"), sel("button.btn.primary#save"), sel("#save"), '
            'sel("li"), sel(".label"), sel("ul"), sel("#nope"), sel("div"));\n'
            'console.log(sel("li", outside.children[0], root), sel(".btn", outside.children[0], '
            'outside));\n'
            'const log = [];\n'
            'const d = createDelegate(root);\n'
            'd.on("button", (el, t) => log.push(`button(${el.tag}) from ${t.tag}`));\n'
            'd.on(".row", (el) => log.push("row"));\n'
            'd.on(".missing", () => log.push("never"));\n'
            'console.log(d.dispatch(icon), d.dispatch(row.children[1]), d.dispatch(root), '
            'log.join(" | "));\n',
  'hint': 'Разберите селектор регулярным выражением: ^([a-z0-9]*)((?:\\.[\\w-]+)*)(#[\\w-]+)?$.',
  'expected': ['button#save button#save button#save button#save li null ul#list null null',
               'null div',
               '2 1 0 button(button) from i | row | row']},
 {'id': 'j30-store',
  'mode': 'js',
  'title': 'Хранилище в стиле Redux',
  'statement': 'Напишите createStore(reducer, preloaded): { getState, dispatch, subscribe }. При '
               "создании состояние = reducer(preloaded, { type: '@@init' }). dispatch(action): "
               "action — объект со строковым type, иначе Error('Actions must be plain objects with "
               "a string type'); вызывает reducer(state, action); если результат !== прежнему "
               'состоянию — сохраняет и вызывает подписчиков (в порядке подписки; подписчики на '
               'момент начала рассылки); возвращает action. Диспетчеризация изнутри редьюсера '
               "запрещена — Error('Reducers may not dispatch actions'). subscribe(fn) возвращает "
               'функцию отписки (повторный вызов безвреден); отписка во время рассылки не влияет '
               'на текущую рассылку.',
  'starter': 'function createStore(reducer, preloaded) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const reducer = (state = { n: 0 }, action) => {\n'
            '  if (action.type === "inc") return { n: state.n + (action.by || 1) };\n'
            '  if (action.type === "nop") return state;\n'
            '  if (action.type === "bad") store.dispatch({ type: "inc" });\n'
            '  return state;\n'
            '};\n'
            'const store = createStore(reducer);\n'
            'const log = [];\n'
            'const off1 = store.subscribe(() => log.push("A:" + store.getState().n));\n'
            'const off2 = store.subscribe(() => { log.push("B:" + store.getState().n); off1(); '
            '});\n'
            'console.log(JSON.stringify(store.getState()));\n'
            'store.dispatch({ type: "inc" }); store.dispatch({ type: "nop" }); store.dispatch({ '
            'type: "inc", by: 5 });\n'
            'console.log(log.join(" "), JSON.stringify(store.getState()));\n'
            'off2(); off2(); store.dispatch({ type: "inc" });\n'
            'console.log(log.length, store.getState().n);\n'
            'for (const bad of [null, "inc", { type: 1 }, {}]) { try { store.dispatch(bad); } '
            'catch (e) { console.log(e.message); } }\n'
            'try { store.dispatch({ type: "bad" }); } catch (e) { console.log(e.message); }\n'
            'console.log(JSON.stringify(createStore(reducer, { n: 100 }).getState()));\n',
  'hint': 'Флаг isReducing; снимок подписчиков перед рассылкой.',
  'expected': ['{"n":0}',
               'A:1 B:1 B:6 {"n":6}',
               '3 7',
               'Actions must be plain objects with a string type',
               'Actions must be plain objects with a string type',
               'Actions must be plain objects with a string type',
               'Actions must be plain objects with a string type',
               'Reducers may not dispatch actions',
               '{"n":100}']},
 {'id': 'j30-combine-reducers',
  'mode': 'js',
  'title': 'combineReducers',
  'statement': 'Напишите combineReducers(reducers): возвращает редьюсер (state = {}, action). Для '
               'каждого ключа вызывается reducers[ключ](state[ключ], action); результат undefined '
               '— Error(`Reducer "ключ" returned undefined`). Если все срезы вернули те же ссылки, '
               'а набор ключей состояния не изменился (в state нет лишних ключей сверх reducers), '
               'возвращается прежний state (та же ссылка); иначе — новый объект только с ключами '
               'reducers (в порядке reducers). Лишние ключи входного state отбрасываются, и это '
               'считается изменением.',
  'starter': 'function combineReducers(reducers) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const counter = (s = 0, a) => (a.type === "inc" ? s + 1 : s);\n'
            'const todos = (s = [], a) => (a.type === "add" ? [...s, a.t] : s);\n'
            'const root = combineReducers({ counter, todos });\n'
            'const s0 = root(undefined, { type: "@@init" });\n'
            'console.log(JSON.stringify(s0));\n'
            'const s1 = root(s0, { type: "other" });\n'
            'console.log(s1 === s0);\n'
            'const s2 = root(s0, { type: "inc" });\n'
            'console.log(JSON.stringify(s2), s2 !== s0, s2.todos === s0.todos);\n'
            'const s3 = root({ counter: 5, todos: [], junk: 1 }, { type: "other" });\n'
            'console.log(JSON.stringify(s3));\n'
            'const s4 = root(s2, { type: "add", t: "x" });\n'
            'console.log(JSON.stringify(s4), s4.counter === s2.counter);\n'
            'try { combineReducers({ bad: () => undefined })({}, { type: "x" }); } catch (e) { '
            'console.log(e.message); }\n',
  'hint': 'Соберите next-объект и сравнивайте ссылки; проверьте количество ключей.',
  'expected': ['{"counter":0,"todos":[]}',
               'true',
               '{"counter":1,"todos":[]} true true',
               '{"counter":5,"todos":[]}',
               '{"counter":1,"todos":["x"]} true',
               'Reducer "bad" returned undefined']},
 {'id': 'j30-middleware',
  'mode': 'js',
  'title': 'Middleware: logger и thunk',
  'statement': 'createStore(reducer, preloaded) (getState, dispatch, subscribe) уже есть. Напишите '
               'applyMiddleware(...middlewares): возвращает функцию (createStore) => (reducer, '
               'preloaded) => store. Middleware имеет вид ({ getState, dispatch }) => next => '
               'action => …, где dispatch внутри middleware — полный (проходит всю цепочку '
               'заново). Цепочка вызывается слева направо: первая middleware оборачивает '
               'следующие. Итоговый store содержит getState, subscribe и dispatch (с цепочкой). '
               'Затем напишите thunk — middleware: если action — функция, вызвать action(dispatch, '
               'getState) и вернуть её результат; иначе передать дальше. И logger(log) — '
               "middleware, который перед передачей дальше вызывает log('→ ' + action.type), после "
               "— log('← ' + JSON.stringify(getState())).",
  'starter': 'function createStore(reducer, preloaded) {\n'
             '  let state = reducer(preloaded, { type: "@@init" });\n'
             '  const subs = new Set();\n'
             '  return {\n'
             '    getState: () => state,\n'
             '    dispatch(action) {\n'
             '      const next = reducer(state, action);\n'
             '      if (next !== state) { state = next; for (const s of [...subs]) s(); }\n'
             '      return action;\n'
             '    },\n'
             '    subscribe(fn) { subs.add(fn); return () => subs.delete(fn); },\n'
             '  };\n'
             '}\n'
             'function applyMiddleware(...middlewares) {\n'
             '}\n'
             'const thunk = null;\n'
             'function logger(log) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const reducer = (s = { n: 0 }, a) => (a.type === "inc" ? { n: s.n + 1 } : s);\n'
            'const out = [];\n'
            'const store = applyMiddleware(logger((m) => out.push(m)), '
            'thunk)(createStore)(reducer);\n'
            'store.dispatch({ type: "inc" });\n'
            'console.log(out.join(" | "), JSON.stringify(store.getState()));\n'
            'out.length = 0;\n'
            'const r = store.dispatch((dispatch, getState) => { dispatch({ type: "inc" }); return '
            '"thunk:" + getState().n; });\n'
            'console.log(r, out.join(" | "));\n'
            'const ping = store.dispatch(async (dispatch) => { await null; dispatch({ type: "inc" '
            '}); return "async"; });\n'
            'console.log(typeof ping.then, await ping, store.getState().n);\n'
            'const calls = [];\n'
            'const order = (name) => () => (next) => (action) => { calls.push(name + "-in"); const '
            'r = next(action); calls.push(name + "-out"); return r; };\n'
            'const s2 = applyMiddleware(order("A"), order("B"))(createStore)(reducer);\n'
            's2.dispatch({ type: "inc" });\n'
            'console.log(calls.join(" "));\n'
            'let seen = 0; const unsub = s2.subscribe(() => seen++); s2.dispatch({ type: "inc" }); '
            'unsub(); s2.dispatch({ type: "inc" }); console.log(seen);\n',
  'hint': 'Соберите chain = middlewares.map(m => m(api)); compose справа налево над '
          'store.dispatch.',
  'expected': ['→ inc | ← {"n":1} {"n":1}',
               'thunk:2 → undefined | → inc | ← {"n":2} | ← {"n":2}',
               'function async 3',
               'A-in B-in B-out A-out',
               '1']},
 {'id': 'j30-nested-routes',
  'mode': 'js',
  'title': 'Вложенные маршруты',
  'statement': 'Напишите matchRoutes(routes, path): routes — [{ path, name?, children? }]. Путь '
               'маршрута относительный к родителю: сегменты через «/», «:имя» — параметр, «*» в '
               "конце — остаток, пустая строка '' — индексный маршрут (совпадает, когда остаток "
               'пути пуст). Путь запроса — без query/hash, ведущие/хвостовые «/» игнорируются. '
               'Алгоритм: для маршрутов по порядку — маршрут совпадает, если его шаблон является '
               'префиксом оставшегося пути (для маршрута с детьми) либо полностью совпадает с '
               'оставшимся путём; затем рекурсивно по детям; побеждает первая совпавшая цепочка, в '
               'которой оставшийся путь израсходован. Результат — массив { route, params } от '
               'корня к листу, params у каждого — накопленные параметры (родительские + свои) на '
               'этом шаге; нет совпадения — null. Параметры декодируются decodeURIComponent.',
  'starter': 'function matchRoutes(routes, path) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const routes = [\n'
            '  { path: "", name: "home" },\n'
            '  { path: "users", name: "users", children: [{ path: "", name: "users-index" }, { '
            'path: "new", name: "users-new" }, { path: ":id", name: "user", children: [{ path: "", '
            'name: "user-index" }, { path: "posts/:pid", name: "post" }] }] },\n'
            '  { path: "files/*", name: "files" },\n'
            '  { path: "*", name: "not-found" },\n'
            '];\n'
            'const t = (p) => { const r = matchRoutes(routes, p); console.log(p, r ? r.map((x) => '
            'x.route.name + JSON.stringify(x.params)).join(" > ") : null); };\n'
            't("/"); t("/users"); t("/users/"); t("/users/new"); t("/users/42"); '
            't("/users/42/posts/7"); t("/users/a%20b/posts/x"); t("/files/a/b.txt"); '
            't("/nope/deep");\n'
            'console.log(JSON.stringify(matchRoutes([{ path: "a", children: [{ path: "b" }] }], '
            '"/a")), JSON.stringify(matchRoutes([], "/")));\n',
  'hint': 'Рекурсивная функция match(routes, segments, params): для каждого маршрута попробуйте '
          'взять префикс сегментов.',
  'expected': ['/ home{}',
               '/users users{} > users-index{}',
               '/users/ users{} > users-index{}',
               '/users/new users{} > users-new{}',
               '/users/42 users{} > user{"id":"42"} > user-index{"id":"42"}',
               '/users/42/posts/7 users{} > user{"id":"42"} > post{"id":"42","pid":"7"}',
               '/users/a%20b/posts/x users{} > user{"id":"a b"} > post{"id":"a b","pid":"x"}',
               '/files/a/b.txt files{"*":"a/b.txt"}',
               '/nope/deep not-found{"*":"nope/deep"}',
               'null null']},
 {'id': 'j30-parse-url',
  'mode': 'js',
  'title': 'Разбор адреса',
  'statement': 'Напишите parseUrl(url) → { path, query, hash }. url — относительный адрес вида '
               '«/путь?a=1&b=2#якорь» (без схемы и хоста). path — часть до «?» или «#» (как есть; '
               'пустой путь — «/»). hash — после «#» без самого «#» (декодирование не нужно; нет — '
               'пустая строка). query — объект: пары через «&»; «+» → пробел; значения и ключи '
               'декодируются decodeURIComponent; повторяющиеся ключи собираются в массив в порядке '
               'появления; ключ без «=» → пустая строка; пустые части пропускаются; некорректная '
               'процентная последовательность оставляется как есть.',
  'starter': 'function parseUrl(url) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (u) => console.log(JSON.stringify(u), JSON.stringify(parseUrl(u)));\n'
            'show("/users/42?tab=info&sort=desc#top");\n'
            'show("/a?x=1&x=2&x=3&y=%D0%B0+b");\n'
            'show("/search?q=hello+world&flag&empty=&&k=v#h");\n'
            'show("?only=query");\n'
            'show("#only-hash");\n'
            'show("");\n'
            'show("/p?bad=%E0%A4%A&ok=1");\n'
            'show("/p#a?b=c");\n',
  'hint': 'Сначала отделите hash, затем query; для декодирования — try/catch вокруг '
          'decodeURIComponent.',
  'expected': ['"/users/42?tab=info&sort=desc#top" '
               '{"path":"/users/42","query":{"tab":"info","sort":"desc"},"hash":"top"}',
               '"/a?x=1&x=2&x=3&y=%D0%B0+b" {"path":"/a","query":{"x":["1","2","3"],"y":"а '
               'b"},"hash":""}',
               '"/search?q=hello+world&flag&empty=&&k=v#h" {"path":"/search","query":{"q":"hello '
               'world","flag":"","empty":"","k":"v"},"hash":"h"}',
               '"?only=query" {"path":"/","query":{"only":"query"},"hash":""}',
               '"#only-hash" {"path":"/","query":{},"hash":"only-hash"}',
               '"" {"path":"/","query":{},"hash":""}',
               '"/p?bad=%E0%A4%A&ok=1" {"path":"/p","query":{"bad":"%E0%A4%A","ok":"1"},"hash":""}',
               '"/p#a?b=c" {"path":"/p","query":{},"hash":"a?b=c"}']},
 {'id': 'j30-build-url',
  'mode': 'js',
  'title': 'Сборка адреса по шаблону',
  'statement': "Напишите buildUrl(pattern, params = {}, query = {}, hash = ''). В шаблоне «:имя» "
               'заменяется на encodeURIComponent(String(params[имя])); если параметра нет '
               "(undefined/null) — Error('Missing param: имя'). Лишние params игнорируются. query: "
               'ключи по алфавиту; значение-массив — повторяющийся ключ в исходном порядке; null и '
               'undefined пропускаются (в том числе внутри массива); пары кодируются '
               'encodeURIComponent, пробел — как %20; булевы и числа — String. Строка запроса '
               'добавляется после «?», только если пары есть. hash (если непустой) добавляется как '
               '«#» + hash. Завершающий «/» шаблона сохраняется.',
  'starter': 'function buildUrl(pattern, params = {}, query = {}, hash = "") {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (...a) => { try { console.log(buildUrl(...a)); } catch (e) { '
            'console.log("!" + e.message); } };\n'
            't("/users/:id", { id: 42 });\n'
            't("/users/:id/posts/:pid/", { id: "a b", pid: "x/y", extra: 1 });\n'
            't("/users/:id", {});\n'
            't("/search", {}, { q: "hello world", tag: ["b", "a", null], page: 2, empty: '
            'undefined, ok: true });\n'
            't("/p", {}, { a: null, b: undefined });\n'
            't("/docs/:slug", { slug: "intro" }, {}, "install");\n'
            't("/x", {}, { "k y": "а&б=в" }, "h");\n'
            't("/", {});\n',
  'hint': 'replace(/:([A-Za-z_]\\w*)/g, …); query — сортировка ключей и flatMap.',
  'expected': ['/users/42',
               '/users/a%20b/posts/x%2Fy/',
               '!Missing param: id',
               '/search?ok=true&page=2&q=hello%20world&tag=b&tag=a',
               '/p',
               '/docs/intro#install',
               '/x?k%20y=%D0%B0%26%D0%B1%3D%D0%B2#h',
               '/']},
 {'id': 'j30-history',
  'mode': 'js',
  'title': 'История переходов',
  'statement': "Напишите createMemoryHistory(initial = ['/'], index = initial.length - 1): { "
               'location, push, replace, back, forward, go, listen, length }. location() — текущий '
               'путь. push(path): отбрасывает записи после текущей, добавляет новую, index++, '
               "событие 'PUSH'. replace(path): заменяет текущую запись, событие 'REPLACE'. go(n): "
               'сдвигает index на n в пределах [0, длина − 1] (если сдвиг невозможен — ничего не '
               "происходит и событий нет), событие 'POP'; back() = go(-1), forward() = go(1). "
               'listen(fn) вызывается как fn(location, action) после каждого изменения и '
               'возвращает отписку. length() — число записей.',
  'starter': 'function createMemoryHistory(initial = ["/"], index = initial.length - 1) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const h = createMemoryHistory(["/"]);\n'
            'const log = [];\n'
            'const off = h.listen((loc, act) => log.push(`${act}:${loc}`));\n'
            'h.push("/a"); h.push("/b"); h.back(); h.back();\n'
            'console.log(h.location(), h.length());\n'
            'h.back(); h.forward(); h.push("/c");\n'
            'console.log(h.location(), h.length(), log.join(" "));\n'
            'h.forward(); h.go(-5); h.go(0);\n'
            'console.log(h.location(), log.length);\n'
            'h.replace("/r");\n'
            'console.log(h.location(), h.length(), log[log.length - 1]);\n'
            'off(); h.push("/z");\n'
            'console.log(log.length, h.location());\n'
            'const h2 = createMemoryHistory(["/x", "/y", "/z"], 1);\n'
            'console.log(h2.location(), h2.length()); h2.go(1); console.log(h2.location());\n',
  'hint': 'entries и index; notify(action) после изменения; go проверяет границы заранее.',
  'expected': ['/ 3',
               '/c 3 PUSH:/a PUSH:/b POP:/a POP:/ POP:/a PUSH:/c',
               '/c 6',
               '/r 3 REPLACE:/r',
               '7 /z',
               '/y 3',
               '/z']},
 {'id': 'j30-link-intercept',
  'mode': 'js',
  'title': 'Перехват кликов по ссылкам',
  'statement': 'Напишите shouldIntercept(event, anchor, origin): event = { button, metaKey, '
               'ctrlKey, shiftKey, altKey, defaultPrevented }, anchor = { href, target?, '
               'download?, rel? }, origin — адрес сайта («https://site.example»). Вернуть true, '
               'если клик должен обрабатывать маршрутизатор: левая кнопка (button === 0), нет '
               "модификаторов, не defaultPrevented; target не задан или '' или '_self'; нет "
               "атрибута download (undefined/false; пустая строка '' — это тоже download); rel не "
               'содержит слова external; href (относительный или абсолютный, разрешается через new '
               'URL(href, origin)) — того же origin и протокола http: или https:. Некорректный '
               'href — false. Ссылка-«только якорь» («#top») — тоже перехватывается (true).',
  'starter': 'function shouldIntercept(event, anchor, origin) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const ev = (o = {}) => ({ button: 0, metaKey: false, ctrlKey: false, shiftKey: false, '
            'altKey: false, defaultPrevented: false, ...o });\n'
            'const O = "https://site.example";\n'
            'const t = (e, a) => console.log(JSON.stringify(a).slice(0, 60), '
            'JSON.stringify(e).replace(/"(\\w+)":false,?/g, "").slice(0, 30), shouldIntercept(e, '
            'a, O));\n'
            't(ev(), { href: "/users" }); t(ev(), { href: "https://site.example/a?b=1" }); t(ev(), '
            '{ href: "#top" }); t(ev(), { href: "page" });\n'
            't(ev({ button: 1 }), { href: "/x" }); t(ev({ ctrlKey: true }), { href: "/x" }); '
            't(ev({ shiftKey: true }), { href: "/x" }); t(ev({ metaKey: true }), { href: "/x" }); '
            't(ev({ altKey: true }), { href: "/x" });\n'
            't(ev({ defaultPrevented: true }), { href: "/x" });\n'
            't(ev(), { href: "/x", target: "_blank" }); t(ev(), { href: "/x", target: "_self" }); '
            't(ev(), { href: "/x", target: "" });\n'
            't(ev(), { href: "/x", download: "" }); t(ev(), { href: "/x", download: false }); '
            't(ev(), { href: "/x", rel: "noopener external" }); t(ev(), { href: "/x", rel: '
            '"noopener" });\n'
            't(ev(), { href: "https://other.example/x" }); t(ev(), { href: "http://site.example/x" '
            '}); t(ev(), { href: "mailto:a@b.c" }); t(ev(), { href: "javascript:void(0)" }); '
            't(ev(), { href: "http://[bad" });\n',
  'hint': 'Проверки по очереди; для rel используйте split(/\\s+/).',
  'expected': ['{"href":"/users"} {"button":0,} true',
               '{"href":"https://site.example/a?b=1"} {"button":0,} true',
               '{"href":"#top"} {"button":0,} true',
               '{"href":"page"} {"button":0,} true',
               '{"href":"/x"} {"button":1,} false',
               '{"href":"/x"} {"button":0,"ctrlKey":true,} false',
               '{"href":"/x"} {"button":0,"shiftKey":true,} false',
               '{"href":"/x"} {"button":0,"metaKey":true,} false',
               '{"href":"/x"} {"button":0,"altKey":true,} false',
               '{"href":"/x"} {"button":0,"defaultPrevented" false',
               '{"href":"/x","target":"_blank"} {"button":0,} false',
               '{"href":"/x","target":"_self"} {"button":0,} true',
               '{"href":"/x","target":""} {"button":0,} true',
               '{"href":"/x","download":""} {"button":0,} false',
               '{"href":"/x","download":false} {"button":0,} true',
               '{"href":"/x","rel":"noopener external"} {"button":0,} false',
               '{"href":"/x","rel":"noopener"} {"button":0,} true',
               '{"href":"https://other.example/x"} {"button":0,} false',
               '{"href":"http://site.example/x"} {"button":0,} false',
               '{"href":"mailto:a@b.c"} {"button":0,} false',
               '{"href":"javascript:void(0)"} {"button":0,} false',
               '{"href":"http://[bad"} {"button":0,} false']},
 {'id': 'j30-guards',
  'mode': 'js',
  'title': 'Охранники навигации',
  'statement': 'Напишите createRouter(): { beforeEach(guard), navigate(path), current() }. '
               'Охранники — функции (to, from) → true/undefined (разрешить), false (отменить) или '
               'строка (редирект); могут быть async. navigate(path) (async): охранники вызываются '
               'по очереди в порядке регистрации. Все разрешили — current() = path, результат { '
               "ok: true, path }. false — { ok: false, reason: 'cancelled' }. Строка — перейти "
               'туда (рекурсивно с теми же правилами), не более 10 редиректов подряд, иначе '
               "бросить Error('Too many redirects'). Если во время ожидания охранников началась "
               'новая навигация — прежняя после завершения охранника возвращает { ok: false, '
               "reason: 'superseded' } и не меняет current. Начальный current() = '/'.",
  'starter': 'function createRouter() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
            'const r = createRouter();\n'
            'const log = [];\n'
            'r.beforeEach((to, from) => { log.push(`g1 ${from}->${to}`); if (to === "/admin") '
            'return "/login"; });\n'
            'r.beforeEach(async (to) => { await sleep(to === "/slow" ? 40 : 1); log.push("g2 " + '
            'to); if (to === "/blocked") return false; return true; });\n'
            'console.log(JSON.stringify(await r.navigate("/home")), r.current());\n'
            'console.log(JSON.stringify(await r.navigate("/blocked")), r.current());\n'
            'console.log(JSON.stringify(await r.navigate("/admin")), r.current());\n'
            'const slow = r.navigate("/slow");\n'
            'await sleep(5);\n'
            'const fast = r.navigate("/fast");\n'
            'console.log(JSON.stringify(await slow), JSON.stringify(await fast), r.current());\n'
            'console.log(log.length);\n'
            'const loop = createRouter(); loop.beforeEach((to) => (to === "/a" ? "/b" : "/a"));\n'
            'try { await loop.navigate("/a"); } catch (e) { console.log(e.message); }\n',
  'hint': 'Счётчик навигаций id; после каждого await проверяйте, что id всё ещё актуален.',
  'expected': ['{"ok":true,"path":"/home"} /home',
               '{"ok":false,"reason":"cancelled"} /home',
               '{"ok":true,"path":"/login"} /login',
               '{"ok":false,"reason":"superseded"} {"ok":true,"path":"/fast"} /fast',
               '11',
               'Too many redirects']},
 {'id': 'j30-redirects',
  'mode': 'js',
  'title': 'Правила редиректов',
  'statement': 'Напишите resolveRedirects(path, rules, maxDepth = 10). rules — { откуда: куда }; '
               '«откуда» — точный путь или шаблон с параметрами «/old/:id»; «куда» может '
               'подставлять те же параметры («/new/:id»). Применяйте правила повторно к '
               'результату, пока ни одно не совпадёт; приоритет — точное совпадение раньше '
               'шаблонов, затем порядок правил. Возвращает конечный путь. Если путь повторился '
               "(цикл) — Error('Redirect loop: a -> b -> a') (цепочка от начала до повтора); если "
               "шагов больше maxDepth — Error('Too many redirects'). Путь сравнивается без "
               'завершающего «/» (кроме корня).',
  'starter': 'function resolveRedirects(path, rules, maxDepth = 10) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const rules = { "/old": "/new", "/new": "/newer", "/blog/:slug": "/posts/:slug", '
            '"/posts/:slug/amp": "/posts/:slug", "/a": "/b", "/b": "/a", "/x/:id/y/:z": '
            '"/z/:z/:id" };\n'
            'const t = (p, d) => { try { console.log(p, "→", resolveRedirects(p, rules, d)); } '
            'catch (e) { console.log(p, "!", e.message); } };\n'
            't("/old"); t("/old/"); t("/blog/hello"); t("/blog/hello/"); t("/posts/hello/amp"); '
            't("/nothing"); t("/a"); t("/x/1/y/2"); t("/old", 1); t("/old", 2); t("/");\n',
  'hint': 'Функция apply(path) возвращает новый путь или null; цепочка visited для обнаружения '
          'цикла.',
  'expected': ['/old → /newer',
               '/old/ → /newer',
               '/blog/hello → /posts/hello',
               '/blog/hello/ → /posts/hello',
               '/posts/hello/amp → /posts/hello',
               '/nothing → /nothing',
               '/a ! Redirect loop: /a -> /b -> /a',
               '/x/1/y/2 → /z/2/1',
               '/old ! Too many redirects',
               '/old → /newer',
               '/ → /']},
 {'id': 'j30-active-link',
  'mode': 'js',
  'title': 'Активная ссылка',
  'statement': 'Напишите isActive(current, target, { exact = false } = {}) и '
               'activeClasses(current, items). Пути нормализуются: отбрасываются query и hash, '
               'схлопываются «//», убирается завершающий «/» (корень остаётся «/»). exact: '
               'активна, только если пути равны. Не exact: пути равны или current начинается с '
               'target + «/» (target «/» активна только при точном совпадении, иначе корень был бы '
               'активен всегда). activeClasses(current, items): items — [{ href, label, exact? }]; '
               "вернуть массив имён классов в порядке items: 'active' если isActive, иначе ''; при "
               "этом среди неточных совпадений 'active' получает только самая длинная (по длине "
               "нормализованного target) подходящая ссылка — остальные неточные подходящие дают '' "
               '(точные учитываются независимо).',
  'starter': 'function isActive(current, target, opts = {}) {\n'
             '}\n'
             'function activeClasses(current, items) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (c, tg, o) => console.log(c, tg, JSON.stringify(o ?? {}), isActive(c, tg, '
            'o));\n'
            't("/users/42", "/users"); t("/users/42", "/users", { exact: true }); t("/users", '
            '"/users/"); t("/usersx", "/users"); t("/", "/"); t("/users", "/");\n'
            't("/users/?a=1#b", "/users", { exact: true }); t("//a//b/", "/a/b"); t("/a/b", '
            '"/a/b/c");\n'
            'const items = [{ href: "/", label: "Home", exact: true }, { href: "/docs" }, { href: '
            '"/docs/api" }, { href: "/blog" }, { href: "/docs/api", exact: true }];\n'
            'console.log(JSON.stringify(activeClasses("/docs/api/fetch", items)));\n'
            'console.log(JSON.stringify(activeClasses("/docs/api", items)));\n'
            'console.log(JSON.stringify(activeClasses("/", items)), '
            'JSON.stringify(activeClasses("/x", items)), JSON.stringify(activeClasses("/blog/1", '
            '[])));\n',
  'hint': 'Функция norm(p); для activeClasses сначала найдите самую длинную подходящую неточную '
          'ссылку.',
  'expected': ['/users/42 /users {} true',
               '/users/42 /users {"exact":true} false',
               '/users /users/ {} true',
               '/usersx /users {} false',
               '/ / {} true',
               '/users / {} false',
               '/users/?a=1#b /users {"exact":true} true',
               '//a//b/ /a/b {} true',
               '/a/b /a/b/c {} false',
               '["","","active","",""]',
               '["","","active","","active"]',
               '["active","","","",""] ["","","","",""] []']},
 {'id': 'j30-scroll',
  'mode': 'js',
  'title': 'Восстановление прокрутки',
  'statement': 'Напишите createScrollManager(): { save(key, pos), onNavigate(action, fromKey, '
               'toKey, hash, currentPos) }. save запоминает позицию { x, y } для ключа записи '
               'истории. onNavigate вызывается при переходе: сначала запоминает currentPos под '
               'ключом fromKey (если fromKey задан), затем возвращает позицию для показа: для '
               "'PUSH' и 'REPLACE' — если hash непустой, { anchor: hash }, иначе { x: 0, y: 0 }; "
               "для 'POP' — сохранённая позиция toKey, а если её нет — { x: 0, y: 0 } (hash при "
               'POP не учитывается). Возвращаемые объекты — копии (изменение результата не должно '
               'влиять на сохранённое).',
  'starter': 'function createScrollManager() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const sm = createScrollManager();\n'
            'console.log(JSON.stringify(sm.onNavigate("PUSH", "k1", "k2", "", { x: 0, y: 500 '
            '})));\n'
            'console.log(JSON.stringify(sm.onNavigate("PUSH", "k2", "k3", "section", { x: 0, y: '
            '120 })));\n'
            'console.log(JSON.stringify(sm.onNavigate("POP", "k3", "k1", "ignored", { x: 0, y: 10 '
            '})));\n'
            'const back = sm.onNavigate("POP", "k1", "k2", "", { x: 5, y: 700 });\n'
            'console.log(JSON.stringify(back));\n'
            'back.y = 99999;\n'
            'console.log(JSON.stringify(sm.onNavigate("POP", "k2", "k1", "", { x: 0, y: 0 })), '
            'JSON.stringify(sm.onNavigate("POP", "k1", "k2", "", { x: 0, y: 1 })));\n'
            'console.log(JSON.stringify(sm.onNavigate("REPLACE", "k2", "k2b", "", { x: 0, y: 3 '
            '})), JSON.stringify(sm.onNavigate("POP", "k2b", "unknown", "", { x: 0, y: 4 })));\n'
            'sm.save("manual", { x: 1, y: 2 });\n'
            'console.log(JSON.stringify(sm.onNavigate("POP", undefined, "manual", "", { x: 0, y: 0 '
            '})));\n',
  'hint': 'Map ключ → позиция; возвращайте {...pos}.',
  'expected': ['{"x":0,"y":0}',
               '{"anchor":"section"}',
               '{"x":0,"y":500}',
               '{"x":0,"y":120}',
               '{"x":5,"y":700} {"x":0,"y":0}',
               '{"x":0,"y":0} {"x":0,"y":0}',
               '{"x":1,"y":2}']},
 {'id': 'j30-lazy',
  'mode': 'js',
  'title': 'Ленивая загрузка маршрута',
  'statement': 'Напишите createLazy(loader): loader — async-функция без аргументов (динамический '
               "import). Возвращает { load, preload, state, value, error }. state() — 'idle' (не "
               "начинали), 'loading', 'ready', 'error'. load() возвращает промис результата; "
               'одновременные вызовы делят один запрос; после успеха результат кэшируется (loader '
               'вызывается один раз, повторный load() возвращает значение немедленно через уже '
               "готовый промис). При ошибке state() = 'error', error() — ошибка, load() "
               'отклоняется; следующий вызов load() запускает loader заново (ошибка не кэшируется '
               'навсегда). preload() — запускает load(), но проглатывает ошибку (не бросает), '
               'возвращает тот же промис с обработанной ошибкой (результат undefined). value() — '
               'результат или undefined.',
  'starter': 'function createLazy(loader) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'let calls = 0, fail = true;\n'
            'const lazy = createLazy(async () => { calls++; await new Promise((r) => setTimeout(r, '
            '5)); if (fail) { fail = false; throw new Error("net"); } return { default: "Page" }; '
            '});\n'
            'console.log(lazy.state(), lazy.value());\n'
            'const p1 = lazy.load(), p2 = lazy.load();\n'
            'console.log(lazy.state(), p1 === p2 || "shared?");\n'
            'try { await p1; } catch (e) { console.log("!" + e.message); }\n'
            'console.log(lazy.state(), lazy.error().message, calls);\n'
            'const r = await lazy.load();\n'
            'console.log(lazy.state(), JSON.stringify(r), calls, lazy.error());\n'
            'await lazy.load(); await lazy.load();\n'
            'console.log(calls, JSON.stringify(lazy.value()));\n'
            'let c2 = 0;\n'
            'const l2 = createLazy(async () => { c2++; throw new Error("boom"); });\n'
            'console.log(await l2.preload(), l2.state(), c2);\n'
            'console.log(await l2.preload(), c2);\n',
  'hint': 'Храните promise в полёте, сбрасывайте при ошибке.',
  'expected': ['idle undefined',
               'loading true',
               '!net',
               'error net 1',
               'ready {"default":"Page"} 2 undefined',
               '2 {"default":"Page"}',
               'undefined error 1',
               'undefined 2']},
 {'id': 'j30-breadcrumbs',
  'mode': 'js',
  'title': 'Хлебные крошки',
  'statement': 'Напишите breadcrumbs(chain): chain — цепочка совпавших маршрутов [{ route: { path, '
               'meta? }, params }] от корня к листу (path относителен родителю, как в matchRoutes; '
               "'' — индексный). Для каждого элемента накапливайте абсолютный путь: к пути "
               'родителя добавляется path маршрута, где «:имя» заменяется значением из params '
               'этого элемента (с encodeURIComponent). Крошка создаётся для элементов с '
               'meta.title: title — строка или функция (params) → строка; результат { title, path '
               "}. path корня — «/». Пустые path ('') не меняют накопленный путь; завершающие «/» "
               'не должны дублироваться.',
  'starter': 'function breadcrumbs(chain) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const chain = [\n'
            '  { route: { path: "", meta: { title: "Home" } }, params: {} },\n'
            '  { route: { path: "users", meta: { title: "Users" } }, params: {} },\n'
            '  { route: { path: ":id", meta: { title: (p) => "User " + p.id } }, params: { id: "a '
            'b" } },\n'
            '  { route: { path: "" }, params: { id: "a b" } },\n'
            '  { route: { path: "posts/:pid", meta: { title: "Post" } }, params: { id: "a b", pid: '
            '7 } },\n'
            '];\n'
            'console.log(JSON.stringify(breadcrumbs(chain)));\n'
            'console.log(JSON.stringify(breadcrumbs([])), JSON.stringify(breadcrumbs([{ route: { '
            'path: "x" }, params: {} }])));\n'
            'console.log(JSON.stringify(breadcrumbs([{ route: { path: "", meta: { title: "Root" } '
            '}, params: {} }, { route: { path: "a/b/", meta: { title: "AB" } }, params: {} '
            '}])));\n',
  'hint': "Накапливайте сегменты массивом и собирайте '/' + join('/').",
  'expected': ['[{"title":"Home","path":"/"},{"title":"Users","path":"/users"},{"title":"User a '
               'b","path":"/users/a%20b"},{"title":"Post","path":"/users/a%20b/posts/7"}]',
               '[] []',
               '[{"title":"Root","path":"/"},{"title":"AB","path":"/a/b"}]']},
 {'id': 'j30-title',
  'mode': 'js',
  'title': 'Заголовок страницы',
  'statement': "Напишите computeTitle(chain, { appName, separator = ' · ' }): chain — [{ route: { "
               'meta? }, params }] (как в breadcrumbs). Заголовки берутся из meta.title (строка '
               'или функция(params)); пустые, undefined и не строки пропускаются. Порядок — от '
               'листа к корню (самый глубокий первым), затем appName в конце. Одинаковые подряд '
               'идущие заголовки схлопываются в один. Если заголовков нет — просто appName. '
               'appName может быть пустым — тогда его в конец не добавляют (если и заголовков нет '
               '— пустая строка).',
  'starter': 'function computeTitle(chain, { appName, separator = " · " } = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const chain = [\n'
            '  { route: { meta: { title: "Admin" } }, params: {} },\n'
            '  { route: { meta: { title: "Users" } }, params: {} },\n'
            '  { route: { meta: { title: (p) => `User ${p.id}` } }, params: { id: 7 } },\n'
            '  { route: {}, params: {} },\n'
            '];\n'
            'console.log(computeTitle(chain, { appName: "Shop" }));\n'
            'console.log(computeTitle(chain, { appName: "Shop", separator: " | " }));\n'
            'console.log(computeTitle([{ route: { meta: { title: "A" } }, params: {} }, { route: { '
            'meta: { title: "A" } }, params: {} }, { route: { meta: { title: "B" } }, params: {} '
            '}, { route: { meta: { title: "A" } }, params: {} }], { appName: "X" }));\n'
            'console.log(JSON.stringify(computeTitle([], { appName: "Shop" })), '
            'JSON.stringify(computeTitle([], { appName: "" })), JSON.stringify(computeTitle([{ '
            'route: { meta: { title: "T" } }, params: {} }], { appName: "" })));\n'
            'console.log(computeTitle([{ route: { meta: { title: "" } }, params: {} }, { route: { '
            'meta: { title: 5 } }, params: {} }], { appName: "A" }));\n',
  'hint': 'Соберите массив заголовков, разверните, схлопните повторы подряд, добавьте appName.',
  'expected': ['User 7 · Users · Admin · Shop',
               'User 7 | Users | Admin | Shop',
               'A · B · A · X',
               '"Shop" "" "T"',
               'A']},
 {'id': 'j30-query-state',
  'mode': 'js',
  'title': 'Состояние в адресе (query)',
  'statement': 'Напишите parseQueryState(schema, search) и serializeQueryState(schema, state). '
               "schema — { имя: { type, default, enum? } }, type: 'string' | 'number' | 'boolean' "
               "| 'array'. search — строка запроса с «?» или без. parse: значение берётся из query "
               '(повторяющиеся ключи — массив); string — строка (если задан enum и значения там '
               "нет — default); number — Number(...), нечисло — default; boolean — 'true' или '1' "
               "→ true, 'false' или '0' → false, иначе default; array — все значения массивом "
               '(одно — массив из одного; нет — default или []). Отсутствующее — default '
               '(undefined, если не задан; для array — []). serialize: только поля, отличающиеся '
               'от default (массивы — по содержимому; пустой массив и default undefined — '
               'опускаются); ключи по алфавиту; массивы — повторяющийся ключ; boolean — '
               'true/false; кодирование encodeURIComponent; результат начинается с «?» либо пуст.',
  'starter': 'function parseQueryState(schema, search) {\n'
             '}\n'
             'function serializeQueryState(schema, state) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const schema = { page: { type: "number", default: 1 }, sort: { type: "string", '
            'default: "name", enum: ["name", "date"] }, tags: { type: "array" }, open: { type: '
            '"boolean", default: false }, q: { type: "string" } };\n'
            'const t = (s) => { const st = parseQueryState(schema, s); '
            'console.log(JSON.stringify(s), JSON.stringify(st), '
            'JSON.stringify(serializeQueryState(schema, st))); };\n'
            't(""); t("?page=3&sort=date&tags=a&tags=b&open=true&q=hello+world"); '
            't("page=abc&sort=bogus&open=maybe"); t("?tags=solo&open=1&page=1&sort=name"); '
            't("?open=0&q=%D0%B0");\n'
            'console.log(serializeQueryState(schema, { page: 2, tags: ["x y"], open: true }), '
            'JSON.stringify(serializeQueryState(schema, { page: 1, sort: "name", tags: [], open: '
            'false })));\n',
  'hint': 'URLSearchParams для разбора; сравнение с default — JSON.stringify.',
  'expected': ['"" {"page":1,"sort":"name","tags":[],"open":false} ""',
               '"?page=3&sort=date&tags=a&tags=b&open=true&q=hello+world" '
               '{"page":3,"sort":"date","tags":["a","b"],"open":true,"q":"hello world"} '
               '"?open=true&page=3&q=hello%20world&sort=date&tags=a&tags=b"',
               '"page=abc&sort=bogus&open=maybe" {"page":1,"sort":"name","tags":[],"open":false} '
               '""',
               '"?tags=solo&open=1&page=1&sort=name" '
               '{"page":1,"sort":"name","tags":["solo"],"open":true} "?open=true&tags=solo"',
               '"?open=0&q=%D0%B0" {"page":1,"sort":"name","tags":[],"open":false,"q":"а"} '
               '"?q=%D0%B0"',
               '?open=true&page=2&tags=x%20y ""']},
 {'id': 'j30-base-path',
  'mode': 'js',
  'title': 'Базовый путь приложения',
  'statement': 'Напишите stripBase(base, path) и withBase(base, path). base — префикс приложения '
               "(«/app», «/app/», '' или '/'): нормализуйте — без завершающего «/» (пустая строка "
               'для корня). stripBase возвращает путь внутри приложения: если path равен base или '
               'начинается с base + «/» (после отбрасывания query/hash они сохраняются в '
               'результате) — остаток, а при пустом остатке «/»; иначе null (например, '
               '«/application» не под «/app»). withBase добавляет base к пути приложения (путь '
               'должен начинаться с «/»; query/hash сохраняются); для корня приложения «/» '
               'результат — base + «/» (для пустого base — «/»).',
  'starter': 'function stripBase(base, path) {\n}\nfunction withBase(base, path) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (b, p) => console.log(JSON.stringify(b), p, JSON.stringify(stripBase(b, '
            'p)));\n'
            't("/app", "/app"); t("/app", "/app/"); t("/app", "/app/users/1"); t("/app/", '
            '"/app/users"); t("/app", "/application"); t("/app", "/other"); t("/app", '
            '"/app?x=1#h"); t("/app", "/app/a?x=1#h");\n'
            't("", "/users"); t("/", "/users"); t("/a/b", "/a/b/c"); t("/a/b", "/a");\n'
            'const w = (b, p) => console.log(JSON.stringify(b), p, withBase(b, p));\n'
            'w("/app", "/"); w("/app", "/users?x=1"); w("/app/", "/users"); w("", "/users"); '
            'w("/", "/"); w("/app", "/#top");\n',
  'hint': "Разделите path на путь и хвост (query/hash); сравнивайте с base + '/'.",
  'expected': ['"/app" /app "/"',
               '"/app" /app/ "/"',
               '"/app" /app/users/1 "/users/1"',
               '"/app/" /app/users "/users"',
               '"/app" /application null',
               '"/app" /other null',
               '"/app" /app?x=1#h "/?x=1#h"',
               '"/app" /app/a?x=1#h "/a?x=1#h"',
               '"" /users "/users"',
               '"/" /users "/users"',
               '"/a/b" /a/b/c "/c"',
               '"/a/b" /a null',
               '"/app" / /app/',
               '"/app" /users?x=1 /app/users?x=1',
               '"/app/" /users /app/users',
               '"" /users /users',
               '"/" / /',
               '"/app" /#top /app/#top']},
 {'id': 'j30-normalize-path',
  'mode': 'js',
  'title': 'Нормализация пути',
  'statement': "Напишите normalizePath(path, { caseSensitive = true, trailingSlash = 'remove' } = "
               '{}). Шаги: отбросить query и hash; схлопнуть повторяющиеся «/»; разрешить сегменты '
               '«.» и «..» (выход выше корня игнорируется); при caseSensitive === false привести к '
               "нижнему регистру; пустой результат — «/»; завершающий «/»: 'remove' — убрать "
               "(кроме корня), 'add' — добавить (если путь не корень и нет завершающего «/»), "
               "'keep' — оставить как был во входе (после нормализации сегментов). Ведущий «/» "
               'добавляется, если его нет.',
  'starter': 'function normalizePath(path, opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (p, o) => console.log(JSON.stringify(p), JSON.stringify(o ?? {}), '
            'normalizePath(p, o));\n'
            't("/a//b///c"); t("/a/./b/../c/"); t("/../../x"); t("a/b"); t("/A/B", { '
            'caseSensitive: false }); t("/a/b/", { trailingSlash: "keep" }); t("/a/b", { '
            'trailingSlash: "keep" });\n'
            't("/a/b", { trailingSlash: "add" }); t("/", { trailingSlash: "add" }); t(""); '
            't("/a/b?x=1#y"); t("/a/../", { trailingSlash: "keep" }); t("//"); t("/a/b/..", { '
            'trailingSlash: "add" });\n',
  'hint': "Разбейте на сегменты, обработайте точки через стек, соберите заново; 'keep' определяйте "
          'по исходной строке.',
  'expected': ['"/a//b///c" {} /a/b/c',
               '"/a/./b/../c/" {} /a/c',
               '"/../../x" {} /x',
               '"a/b" {} /a/b',
               '"/A/B" {"caseSensitive":false} /a/b',
               '"/a/b/" {"trailingSlash":"keep"} /a/b/',
               '"/a/b" {"trailingSlash":"keep"} /a/b',
               '"/a/b" {"trailingSlash":"add"} /a/b/',
               '"/" {"trailingSlash":"add"} /',
               '"" {} /',
               '"/a/b?x=1#y" {} /a/b',
               '"/a/../" {"trailingSlash":"keep"} /',
               '"//" {} /',
               '"/a/b/.." {"trailingSlash":"add"} /a/']},
 {'id': 'j30-loaders',
  'mode': 'js',
  'title': 'Параллельные загрузчики данных',
  'statement': 'Напишите runLoaders(chain, ctx): chain — [{ route: { path, loader? }, params }] от '
               'корня к листу. Для каждого элемента с loader вызовите loader(params, ctx) (может '
               'быть sync или async) — все параллельно (сразу, не дожидаясь предыдущих). Результат '
               '(async): { data, errors } — объекты, ключи — индексы элементов chain (строки): '
               'data[i] — значение, errors[i] — сообщение ошибки (message; если брошено не Error — '
               'String(значение)). Исключение одного загрузчика не влияет на остальные. Элементы '
               'без loader в результате не участвуют. Результаты и ошибки должны попадать в '
               'объекты в порядке индексов.',
  'starter': 'async function runLoaders(chain, ctx) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
            'const order = [];\n'
            'const chain = [\n'
            '  { route: { path: "", loader: async (p, c) => { order.push("start0"); await '
            'sleep(30); order.push("end0"); return "layout:" + c.user; } }, params: {} },\n'
            '  { route: { path: "users" }, params: {} },\n'
            '  { route: { path: ":id", loader: async (p) => { order.push("start2"); await '
            'sleep(5); throw new Error("not found " + p.id); } }, params: { id: 7 } },\n'
            '  { route: { path: "posts", loader: (p, c) => { order.push("start3"); return ["p1", '
            'c.user]; } }, params: {} },\n'
            '  { route: { path: "x", loader: () => { throw "plain string"; } }, params: {} },\n'
            '];\n'
            'const r = await runLoaders(chain, { user: "ann" });\n'
            'console.log(JSON.stringify(r), order.join(" "));\n'
            'console.log(JSON.stringify(await runLoaders([], {})), JSON.stringify(await '
            'runLoaders([{ route: { path: "a" }, params: {} }], {})));\n',
  'hint': 'Promise.allSettled над массивом вызовов; оборачивайте sync-исключения.',
  'expected': ['{"data":{"0":"layout:ann","3":["p1","ann"]},"errors":{"2":"not found 7","4":"plain '
               'string"}} start0 start2 start3 end0',
               '{"data":{},"errors":{}} {"data":{},"errors":{}}']},
 {'id': 'j30-error-boundary',
  'mode': 'js',
  'title': 'Граница ошибок',
  'statement': 'Напишите createBoundary(render, fallback, onError): render(props) — функция '
               'отрисовки дочернего поддерева, fallback(error, reset) — запасной вид, '
               'onError(error) — необязательный обработчик. Возвращает { render(props), reset(), '
               'error() }. Пока ошибки нет, render(props) вызывает render и возвращает результат; '
               'если render бросил исключение — ошибка запоминается, onError(error) вызывается '
               'один раз, возвращается fallback(error, reset). Пока ошибка не сброшена, '
               'render(props) не вызывает исходный render, а сразу возвращает fallback(error, '
               'reset) (onError повторно не вызывается). reset() сбрасывает ошибку (после неё '
               'render снова пробует исходный render). error() возвращает текущую ошибку или null.',
  'starter': 'function createBoundary(render, fallback, onError) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'let calls = 0, fail = true;\n'
            'const log = [];\n'
            'const b = createBoundary((p) => { calls++; if (fail && p.bad) throw new Error("render '
            'failed"); return "ok:" + p.v; }, (e, reset) => ({ fallback: e.message, reset }), (e) '
            '=> log.push("onError " + e.message));\n'
            'console.log(b.render({ v: 1 }), b.error(), calls);\n'
            'const r2 = b.render({ v: 2, bad: true });\n'
            'console.log(r2.fallback, b.error().message, calls, log.join());\n'
            'const r3 = b.render({ v: 3 });\n'
            'console.log(r3.fallback, calls, log.length);\n'
            'fail = false;\n'
            'r3.reset();\n'
            'console.log(b.error(), b.render({ v: 4, bad: true }), calls);\n'
            'const b2 = createBoundary(() => { throw new Error("always"); }, (e) => "fb:" + '
            'e.message);\n'
            'console.log(b2.render({}), b2.render({}));\n'
            'b2.reset(); console.log(b2.render({}));\n',
  'hint': 'Переменная error; в render проверяйте её до вызова исходной функции.',
  'expected': ['ok:1 null 1',
               'render failed render failed 2 onError render failed',
               'render failed 2 1',
               'null ok:4 3',
               'fb:always fb:always',
               'fb:always']},
 {'id': 'j30-ssr',
  'mode': 'js',
  'title': 'Серверный рендер маршрута',
  'statement': 'Функция matchPattern(pattern, path) → params | null уже есть. Напишите '
               'renderApp(routes, url, notFound): routes — [{ path, render(params) → строка HTML, '
               'status? }] (path — шаблон), url — адрес с query/hash, notFound(path) → строка. '
               'Верните { status, html }. Путь берётся без query и hash. Первый подходящий '
               'маршрут: html = render(params), status = route.status или 200. Нет маршрута — '
               'status 404, html = notFound(path). Если render бросил исключение — status 500 и '
               "html = '<h1>Error</h1><pre>' + экранированное сообщение (& < > → сущности) + "
               "'</pre>'. Завершающий «/» пути игнорируется (matchPattern уже это делает).",
  'starter': '// Готово: сопоставление пути с шаблоном (не изменяйте)\n'
             'function matchPattern(pattern, path) {\n'
             '  const ps = pattern.split("/").filter(Boolean), xs = '
             'path.split("/").filter(Boolean);\n'
             '  const params = {};\n'
             '  for (let i = 0; i < ps.length; i++) {\n'
             '    if (ps[i] === "*") { params["*"] = xs.slice(i).join("/"); return params; }\n'
             '    if (i >= xs.length) return null;\n'
             '    if (ps[i][0] === ":") params[ps[i].slice(1)] = decodeURIComponent(xs[i]);\n'
             '    else if (ps[i] !== xs[i]) return null;\n'
             '  }\n'
             '  return xs.length === ps.length ? params : null;\n'
             '}\n'
             'function renderApp(routes, url, notFound) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const routes = [\n'
            '  { path: "/", render: () => "<h1>Home</h1>" },\n'
            '  { path: "/users/:id", render: (p) => `<h1>User ${p.id}</h1>` },\n'
            '  { path: "/old", render: () => "<p>moved</p>", status: 301 },\n'
            '  { path: "/boom", render: () => { throw new Error("a < b & c"); } },\n'
            '];\n'
            'const nf = (p) => `<h1>404 ${p}</h1>`;\n'
            'for (const u of ["/", "/users/42?tab=1#x", "/users/a%20b", "/old", "/boom", '
            '"/missing/deep?x=1", "/users/42/"]) console.log(u, JSON.stringify(renderApp(routes, '
            'u, nf)));\n',
  'hint': 'Отрежьте query/hash; перебор routes; try/catch вокруг render.',
  'expected': ['/ {"status":200,"html":"<h1>Home</h1>"}',
               '/users/42?tab=1#x {"status":200,"html":"<h1>User 42</h1>"}',
               '/users/a%20b {"status":200,"html":"<h1>User a b</h1>"}',
               '/old {"status":301,"html":"<p>moved</p>"}',
               '/boom {"status":500,"html":"<h1>Error</h1><pre>a &lt; b &amp; c</pre>"}',
               '/missing/deep?x=1 {"status":404,"html":"<h1>404 /missing/deep</h1>"}',
               '/users/42/ {"status":200,"html":"<h1>User 42</h1>"}']},
 {'id': 'j30-access',
  'mode': 'js',
  'title': 'Права доступа к маршрутам',
  'statement': 'Напишите canAccess(meta, user, path): meta = { auth?, guestOnly?, roles?, '
               'permissions? }, user — null или { roles: [...], permissions: [...] }. Верните { '
               'allowed: true } или { allowed: false, redirect }. Порядок проверок: guestOnly и '
               "есть user — редирект '/'; auth и нет user — редирект '/login?next=' + "
               'encodeURIComponent(path); roles (любая из перечисленных у пользователя) — иначе '
               "'/403'; permissions (все перечисленные у пользователя) — иначе '/403'. Если auth "
               'не задан, но заданы roles/permissions, пользователь всё равно обязателен: без user '
               '— редирект на логин. Пустые массивы roles/permissions проверок не создают.',
  'starter': 'function canAccess(meta, user, path) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const ann = { roles: ["editor"], permissions: ["post:write", "post:read"] };\n'
            'const t = (m, u, p = "/secret/page?x=1") => console.log(JSON.stringify(m), u ? "user" '
            ': "guest", JSON.stringify(canAccess(m, u, p)));\n'
            't({}, null); t({}, ann); t({ guestOnly: true }, null); t({ guestOnly: true }, ann);\n'
            't({ auth: true }, null); t({ auth: true }, ann);\n'
            't({ roles: ["admin", "editor"] }, ann); t({ roles: ["admin"] }, ann); t({ roles: '
            '["admin"] }, null);\n'
            't({ permissions: ["post:read", "post:write"] }, ann); t({ permissions: ["post:read", '
            '"post:delete"] }, ann);\n'
            't({ auth: true, roles: ["editor"], permissions: ["post:write"] }, ann); t({ roles: '
            '[], permissions: [] }, ann); t({ permissions: ["x"] }, null);\n',
  'hint': 'Последовательные if в указанном порядке; some/every для ролей и разрешений.',
  'expected': ['{} guest {"allowed":true}',
               '{} user {"allowed":true}',
               '{"guestOnly":true} guest {"allowed":true}',
               '{"guestOnly":true} user {"allowed":false,"redirect":"/"}',
               '{"auth":true} guest '
               '{"allowed":false,"redirect":"/login?next=%2Fsecret%2Fpage%3Fx%3D1"}',
               '{"auth":true} user {"allowed":true}',
               '{"roles":["admin","editor"]} user {"allowed":true}',
               '{"roles":["admin"]} user {"allowed":false,"redirect":"/403"}',
               '{"roles":["admin"]} guest '
               '{"allowed":false,"redirect":"/login?next=%2Fsecret%2Fpage%3Fx%3D1"}',
               '{"permissions":["post:read","post:write"]} user {"allowed":true}',
               '{"permissions":["post:read","post:delete"]} user '
               '{"allowed":false,"redirect":"/403"}',
               '{"auth":true,"roles":["editor"],"permissions":["post:write"]} user '
               '{"allowed":true}',
               '{"roles":[],"permissions":[]} user {"allowed":true}',
               '{"permissions":["x"]} guest '
               '{"allowed":false,"redirect":"/login?next=%2Fsecret%2Fpage%3Fx%3D1"}']},
 {'id': 'j30-optimistic',
  'mode': 'js',
  'title': 'Оптимистичное обновление',
  'statement': 'Напишите optimisticUpdate(store, apply, request, reconcile): store = { get(), '
               'set(v) }; apply(state) → оптимистичное состояние; request() — async; '
               'reconcile(current, snapshot) → состояние при откате (необязательная). Алгоритм: '
               'snapshot = store.get(); optimistic = apply(snapshot); store.set(optimistic); await '
               'request(). Успех — вернуть результат запроса (состояние остаётся оптимистичным). '
               'Ошибка — откат: если store.get() === optimistic (никто не менял), '
               'store.set(snapshot); иначе если reconcile задана — '
               'store.set(reconcile(store.get(), snapshot)), иначе состояние не трогать. '
               'Исключение пробрасывается после отката.',
  'starter': 'async function optimisticUpdate(store, apply, request, reconcile) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const mk = (v) => { let s = v; return { get: () => s, set: (x) => { s = x; } }; };\n'
            'const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
            'const store = mk({ todos: ["a"] });\n'
            'const apply = (s) => ({ todos: [...s.todos, "b"] });\n'
            'const seen = [];\n'
            'const p = optimisticUpdate(store, apply, async () => { '
            'seen.push(JSON.stringify(store.get())); await sleep(5); return "saved"; });\n'
            'console.log(JSON.stringify(store.get()));\n'
            'console.log(await p, JSON.stringify(store.get()), seen.join());\n'
            'const s2 = mk({ todos: ["a"] }), before = s2.get();\n'
            'try { await optimisticUpdate(s2, apply, async () => { await sleep(5); throw new '
            'Error("server down"); }); } catch (e) { console.log(e.message, s2.get() === before); '
            '}\n'
            'const s3 = mk({ todos: ["a"] });\n'
            'try { await optimisticUpdate(s3, apply, async () => { s3.set({ todos: ["a", "b", "c"] '
            '}); throw new Error("fail"); }); } catch (e) { console.log(e.message, '
            'JSON.stringify(s3.get())); }\n'
            'const s4 = mk({ todos: ["a"] });\n'
            'try { await optimisticUpdate(s4, apply, async () => { s4.set({ todos: ["a", "b", "c"] '
            '}); throw new Error("fail"); }, (cur, snap) => ({ todos: cur.todos.filter((t) => t '
            '!== "b") })); } catch (e) { console.log(e.message, JSON.stringify(s4.get())); }\n',
  'hint': 'try/catch вокруг await request(); сравнение ссылок для отката.',
  'expected': ['{"todos":["a","b"]}',
               'saved {"todos":["a","b"]} {"todos":["a","b"]}',
               'server down true',
               'fail {"todos":["a","b","c"]}',
               'fail {"todos":["a","c"]}']}]}
