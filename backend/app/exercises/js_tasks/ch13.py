"""Задачи книги «Современный Frontend», глава 13 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {13: [{'id': 'j13-call-depth',
       'mode': 'js',
       'title': 'Глубина стека вызовов',
       'statement': 'Программа описана деревом вызовов: { name, calls: [...] } — функция name по очереди '
                    'вызывает вложенные. Напишите функцию maxDepth(tree) (наибольшая глубина стека; корень — '
                    '1) и trace(tree) → массив строк «вход name»/«выход name» в порядке выполнения.',
       'starter': 'function maxDepth(tree) {\n}\nfunction trace(tree) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const t = { name: "main", calls: [{ name: "a", calls: [{ name: "b", calls: [] }] }, { '
                 'name: "c", calls: [{ name: "d", calls: [{ name: "e", calls: [] }] }] }] };\n'
                 'console.log(maxDepth(t), maxDepth({ name: "x", calls: [] }));\n'
                 'console.log(trace(t).join(" | "));\n'
                 'let deep = { name: "f0", calls: [] };\n'
                 'for (let i = 1; i < 1500; i++) deep = { name: "f" + i, calls: [deep] };\n'
                 'console.log(maxDepth(deep));\n',
       'hint': 'Глубина = 1 + максимум глубин вложенных вызовов.',
       'expected': ['4 1',
                    'вход main | вход a | вход b | выход b | выход a | вход c | вход d | вход e | выход e | '
                    'выход d | выход c | выход main',
                    '1500']},
      {'id': 'j13-event-loop',
       'mode': 'js',
       'title': 'Модель цикла событий',
       'statement': 'Программа — массив операций верхнего уровня; операция: { do: "log", text } | { do: '
                    '"micro", ops: [...] } | { do: "task", ops: [...], delay?: мс } (таймер; delay по '
                    'умолчанию 0). Выполняйте как браузер: сначала синхронно все операции скрипта по порядку '
                    '(log печатает; micro ставит микрозадачу с вложенными операциями; task ставит таймер), '
                    'затем очищается очередь микрозадач целиком (в порядке постановки, в том числе вновь '
                    'добавленные), затем берётся следующая задача — таймер с наименьшим сроком (срок = '
                    'момент постановки + delay; при равенстве — раньше поставленный), её операции '
                    'выполняются так же, после неё снова очищаются микрозадачи. Верните массив напечатанных '
                    'строк.',
       'starter': 'function runLoop(program) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const L = (text) => ({ do: "log", text });\n'
                 'const M = (...ops) => ({ do: "micro", ops });\n'
                 'const T = (ops, delay) => ({ do: "task", ops, delay });\n'
                 'console.log(runLoop([T([L("таймер")]), M(L("промис")), L("синхронно")]).join(" > "));\n'
                 'console.log(runLoop([T([L("t1"), M(L("m в t1"))]), T([L("t2")]), M(L("m1"), M(L("m1.1"))), '
                 'M(L("m2"))]).join(" > "));\n'
                 'console.log(runLoop([T([L("поздно")], 50), T([L("рано")], 10), T([L("сразу")]), '
                 'L("start")]).join(" > "));\n'
                 'console.log(runLoop([T([T([L("вложенный 0")]), L("внешний")], 20), T([L("средний")], '
                 '30)]).join(" > "));\n'
                 'console.log(JSON.stringify(runLoop([])));\n'
                 'console.log(runLoop([M(M(M(L("глубоко")))), L("сначала")]).join(" > "));\n',
       'hint': 'Три структуры: микрозадачи (очередь), таймеры (с виртуальным временем), вывод; после каждой '
               'задачи — drain().',
       'expected': ['синхронно > промис > таймер',
                    'm1 > m2 > m1.1 > t1 > m в t1 > t2',
                    'start > сразу > рано > поздно',
                    'внешний > вложенный 0 > средний',
                    '[]',
                    'сначала > глубоко']},
      {'id': 'j13-frame-budget',
       'mode': 'js',
       'title': 'Пропущенные кадры',
       'statement': 'Главный поток выполняет задачи подряд; длительности (мс) заданы массивом durations. '
                    'Напишите функцию droppedFrames(durations, fps = 60): время идёт непрерывно; кадр должен '
                    'выходить каждые 1000/fps мс (в моменты кратные периоду: 0 не считается, первый — на '
                    '16.67 и т.д.), но не может выйти, пока выполняется задача (кадр выходит сразу после '
                    'окончания задачи, если срок прошёл). Верните число кадровых сроков, которые пришлись на '
                    'выполнение задач и поэтому были пропущены (срок находится строго внутри интервала '
                    '(начало, конец) задачи). Периоды считайте точно: период = 1000 / fps.',
       'starter': 'function droppedFrames(durations, fps = 60) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(droppedFrames([10, 5, 8]));\n'
                 'console.log(droppedFrames([50]));\n'
                 'console.log(droppedFrames([100]));\n'
                 'console.log(droppedFrames([16, 16, 16, 16]));\n'
                 'console.log(droppedFrames([200, 5], 60), droppedFrames([200], 30), droppedFrames([], '
                 '60));\n'
                 'console.log(droppedFrames([20, 20, 20, 20, 20]));\n',
       'hint': 'Считайте сроки кадров k * period, попавшие в открытый интервал каждой задачи.',
       'expected': ['1', '2', '5', '3', '11 5 0', '5']},
      {'id': 'j13-long-tasks',
       'mode': 'js',
       'title': 'Долгие задачи и TBT',
       'statement': 'Задачи главного потока заданы массивом { start, duration } (мс). Напишите функцию '
                    'analyze(tasks): longTasks — задачи длиннее 50 мс (в порядке следования); '
                    'totalBlockingTime — сумма превышений над 50 мс по всем долгим задачам; worst — самая '
                    'длинная (первая из равных) или null; и функцию splitTask(duration, chunk = 50) → массив '
                    'длительностей частей (последняя может быть короче; сумма равна duration).',
       'starter': 'function analyze(tasks) {\n}\nfunction splitTask(duration, chunk) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tasks = [{ start: 0, duration: 20 }, { start: 30, duration: 120 }, { start: 200, '
                 'duration: 50 }, { start: 300, duration: 75 }, { start: 400, duration: 120 }];\n'
                 'const r = analyze(tasks);\n'
                 'console.log(r.longTasks.length, r.totalBlockingTime, JSON.stringify(r.worst), '
                 'JSON.stringify(analyze([])));\n'
                 'console.log(JSON.stringify(splitTask(120)), JSON.stringify(splitTask(50)), '
                 'JSON.stringify(splitTask(10)), JSON.stringify(splitTask(0)), JSON.stringify(splitTask(100, '
                 '30)));\n'
                 'console.log(splitTask(333, 50).reduce((a, b) => a + b, 0));\n',
       'hint': 'TBT — сумма (длительность − 50) по задачам длиннее 50 мс.',
       'expected': ['3 165 {"start":30,"duration":120} {"longTasks":[],"totalBlockingTime":0,"worst":null}',
                    '[50,50,20] [50] [10] [] [30,30,30,10]',
                    '333']},
      {'id': 'j13-hidden-classes',
       'mode': 'js',
       'title': 'Скрытые формы объектов',
       'statement': 'Модель форм V8: форма определяется последовательностью имён полей в порядке добавления. '
                    'Напишите функцию countShapes(objects): objects — массив объектов, созданных кодом «как '
                    'есть» (порядок ключей берите из Object.keys; числовые ключи считайте обычными); верните '
                    'число различных форм и { shape: «имена через запятую», count } отсортированный по '
                    'убыванию count (при равенстве — по строке формы). Пустой объект — форма «» (пустая '
                    'строка). Для classify(count) верните «monomorphic» при 1 форме, «polymorphic» при 2–4, '
                    '«megamorphic» при 5 и больше (так V8 оценивает inline cache).',
       'starter': 'function countShapes(objects) {\n}\nfunction classify(count) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const objs = [{ x: 1, y: 2 }, { x: 3, y: 4 }, { y: 5, x: 6 }, { x: 7 }, {}, { x: 1, y: 2, '
                 'z: 3 }, { x: 9, y: 9 }];\n'
                 'const r = countShapes(objs);\n'
                 'console.log(r.count, JSON.stringify(r.shapes));\n'
                 'console.log(classify(r.count), classify(1), classify(0), classify(4), classify(5), '
                 'classify(50));\n'
                 'const o1 = { a: 1 }; o1.b = 2;\n'
                 'const o2 = {}; o2.b = 2; o2.a = 1;\n'
                 'console.log(countShapes([o1, o2]).count, countShapes([]).count);\n',
       'hint': "Ключ формы — Object.keys(o).join(','); подсчёт в Map.",
       'expected': ['5 '
                    '[{"shape":"x,y","count":3},{"shape":"","count":1},{"shape":"x","count":1},{"shape":"x,y,z","count":1},{"shape":"y,x","count":1}]',
                    'megamorphic monomorphic monomorphic polymorphic megamorphic megamorphic',
                    '2 0']},
      {'id': 'j13-gc-mark-sweep',
       'mode': 'js',
       'title': 'Сборка мусора: mark and sweep',
       'statement': 'Куча задана объектом { id: [идентификаторы объектов, на которые есть ссылки] }, корни — '
                    'массив id. Напишите функцию sweep(heap, roots): { alive: отсортированный массив '
                    'достижимых id, freed: отсортированный массив освобождаемых }, и leaks(heap, roots, '
                    'expectedFreed) → id, которые ожидали освободить, но они достижимы (утечки), с путём от '
                    'корня: [{ id, path: [корень, …, id] }] (кратчайший путь по обходу в ширину; пути по '
                    'порядку id).',
       'starter': 'function sweep(heap, roots) {\n}\nfunction leaks(heap, roots, expectedFreed) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const heap = { root: ["a", "b"], a: ["c"], b: [], c: ["a"], d: ["e"], e: ["d"], f: ["a"], '
                 'cache: ["old"], old: [], listener: ["old"] };\n'
                 'console.log(JSON.stringify(sweep(heap, ["root"])));\n'
                 'console.log(JSON.stringify(sweep(heap, ["root", "cache"])));\n'
                 'console.log(JSON.stringify(sweep(heap, [])));\n'
                 'console.log(JSON.stringify(leaks(heap, ["root", "cache"], ["old", "d", "f"])));\n'
                 'console.log(JSON.stringify(leaks(heap, ["root"], ["d", "e"])));\n',
       'hint': 'Обход в ширину от корней; для путей запоминайте родителя каждой вершины.',
       'expected': ['{"alive":["a","b","c","root"],"freed":["cache","d","e","f","listener","old"]}',
                    '{"alive":["a","b","c","cache","old","root"],"freed":["d","e","f","listener"]}',
                    '{"alive":[],"freed":["a","b","c","cache","d","e","f","listener","old","root"]}',
                    '[{"id":"old","path":["cache","old"]}]',
                    '[]']},
      {'id': 'j13-generational-gc',
       'mode': 'js',
       'title': 'Поколения и повышение объектов',
       'statement': 'Модель молодого поколения: каждая «малая сборка» (scavenge) просматривает только '
                    'молодые объекты. Напишите класс Heap: alloc(id, refs = []) создаёт молодой объект; '
                    'setRoots(ids); scavenge() — выживают молодые объекты, достижимые от корней и от старых '
                    'объектов (учтите ссылки из старых!); выжившие получают возраст +1, а при возрасте 2 '
                    'переходят в старое поколение; остальные молодые освобождаются; возвращает '
                    'отсортированный массив освобождённых id; ages() → { id: возраст } для молодых; old() → '
                    'отсортированный массив старых id. Старые объекты scavenge не освобождает.',
       'starter': 'class Heap {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const h = new Heap();\n'
                 'h.alloc("a", ["b"]); h.alloc("b"); h.alloc("c"); h.alloc("d", ["c"]);\n'
                 'h.setRoots(["a"]);\n'
                 'console.log(JSON.stringify(h.scavenge()), JSON.stringify(h.ages()), '
                 'JSON.stringify(h.old()));\n'
                 'h.alloc("e");\n'
                 'console.log(JSON.stringify(h.scavenge()), JSON.stringify(h.ages()), '
                 'JSON.stringify(h.old()));\n'
                 'h.alloc("f", ["g"]); h.alloc("g");\n'
                 'h.setRoots(["a", "f"]);\n'
                 'console.log(JSON.stringify(h.scavenge()), JSON.stringify(h.ages()), '
                 'JSON.stringify(h.old()));\n'
                 'h.setRoots([]);\n'
                 'h.alloc("h");\n'
                 'console.log(JSON.stringify(h.scavenge()), JSON.stringify(h.ages()), '
                 'JSON.stringify(h.old()));\n',
       'hint': 'Достижимость — от корней и от всех старых объектов (они могут ссылаться на молодые).',
       'expected': ['["c","d"] {"a":1,"b":1} []',
                    '["e"] {} ["a","b"]',
                    '[] {"f":1,"g":1} ["a","b"]',
                    '["f","g","h"] {} ["a","b"]']},
      {'id': 'j13-parser-timeline',
       'mode': 'js',
       'title': 'Блокировка разбора скриптами',
       'statement': 'Ресурсы страницы заданы по порядку в HTML: { type: "script"|"defer"|"async"|"module", '
                    'download, exec } (мс). Разбор HTML занимает 10 мс на ресурс (разбор после ресурса i '
                    'начинается, когда закончен разбор предыдущего и — для обычных script — после скачивания '
                    'и выполнения скрипта). Все загрузки стартуют одновременно в момент 0 (сканер '
                    'предзагрузки) и идут параллельно. Обычный script блокирует разбор до своего выполнения '
                    '(не раньше окончания его загрузки). async выполняется, как только скачался и поток '
                    'свободен (тут считаем: выполняется в момент max(download, момент освобождения не '
                    'учитываем) — сразу по завершении загрузки, если разбор не в скрипте; для простоты '
                    'исполнение не сериализуется). defer и module выполняются после конца разбора по порядку '
                    '(каждый — не раньше окончания своей загрузки). Верните { domParsed (конец разбора), '
                    'contentLoaded (конец последнего defer/module), order (метки порядка выполнения: индексы '
                    'ресурсов) }.',
       'starter': 'function timeline(resources) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const show = (r) => console.log(JSON.stringify(timeline(r)));\n'
                 'show([{ type: "script", download: 100, exec: 20 }, { type: "script", download: 30, exec: '
                 '10 }]);\n'
                 'show([{ type: "defer", download: 100, exec: 20 }, { type: "defer", download: 10, exec: 10 '
                 '}, { type: "async", download: 40, exec: 5 }]);\n'
                 'show([{ type: "script", download: 50, exec: 10 }, { type: "async", download: 20, exec: 5 '
                 '}, { type: "module", download: 200, exec: 10 }]);\n'
                 'show([]);\n'
                 'show([{ type: "async", download: 500, exec: 5 }]);\n',
       'hint': 'Обычные скрипты сдвигают время разбора; defer идут после разбора по порядку, async — по '
               'готовности.',
       'expected': ['{"domParsed":140,"contentLoaded":140,"order":[0,1]}',
                    '{"domParsed":30,"contentLoaded":130,"order":[2,0,1]}',
                    '{"domParsed":80,"contentLoaded":210,"order":[1,0,2]}',
                    '{"domParsed":0,"contentLoaded":0,"order":[]}',
                    '{"domParsed":10,"contentLoaded":10,"order":[0]}']},
      {'id': 'j13-render-tree',
       'mode': 'js',
       'title': 'Дерево рендеринга',
       'statement': 'DOM задан как { tag, style?: { display?: string }, children?: [...], text? }. Напишите '
                    'функцию buildRenderTree(node): возвращает дерево только из узлов, которые попадут в '
                    'рендеринг: элементы с display: none исключаются вместе с потомками; элементы с display: '
                    'contents заменяются своими потомками; теги head, script, style, title, meta, link не '
                    'рисуются; текстовые узлы { text } сохраняются, если после trim непусты. Результат — '
                    'вложенный список строк-тегов в виде { tag, children } для элементов и { text } для '
                    'текста.',
       'starter': 'function buildRenderTree(node) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const dom = { tag: "html", children: [\n'
                 '  { tag: "head", children: [{ tag: "title", children: [{ text: "заголовок" }] }] },\n'
                 '  { tag: "body", children: [\n'
                 '    { tag: "div", children: [{ text: "привет" }, { tag: "span", style: { display: "none" '
                 '}, children: [{ text: "скрыто" }] }] },\n'
                 '    { tag: "section", style: { display: "contents" }, children: [{ tag: "p", children: [{ '
                 'text: "внутри contents" }] }, { text: "  " }] },\n'
                 '    { tag: "script", children: [{ text: "alert(1)" }] },\n'
                 '  ] },\n'
                 '] };\n'
                 'console.log(JSON.stringify(buildRenderTree(dom)));\n'
                 'console.log(JSON.stringify(buildRenderTree({ tag: "div", style: { display: "none" } })), '
                 'JSON.stringify(buildRenderTree({ tag: "p" })));\n',
       'hint': 'Рекурсия, возвращающая массив узлов: пустой для скрытого, потомки для contents, один элемент '
               'для остальных.',
       'expected': ['{"tag":"html","children":[{"tag":"body","children":[{"tag":"div","children":[{"text":"привет"}]},{"tag":"p","children":[{"text":"внутри '
                    'contents"}]}]}]}',
                    'null {"tag":"p","children":[]}']},
      {'id': 'j13-critical-path',
       'mode': 'js',
       'title': 'Критический путь рендеринга',
       'statement': 'Ресурсы заданы так: { name, type: "html"|"css"|"js"|"img", size (КБ), blocking?: true '
                    '}, канал — 1 КБ за 1 мс, все ресурсы грузятся параллельно с делением канала поровну '
                    '(для простоты считайте, что делят канал только одновременно скачиваемые: время загрузки '
                    '= size * количество ресурсов, скачиваемых в том же наборе). Упрощённо: '
                    'firstPaint(resources) = время, когда скачаны html и все css и js c blocking: true, '
                    'вычисляется как (сумма размеров этих ресурсов) мс (канал последовательный, порядок не '
                    'важен) + 10 мс на построение дерева, плюс 5 мс на каждый blocking-ресурс (выполнение). '
                    'Картинки (img) не блокируют. Верните { firstPaint, blockedBy: имена блокирующих '
                    'ресурсов в порядке входа } и функцию optimize(resources): помечает blocking: false у '
                    'js, если они помечены defer: true (возвращает новый массив), и сообщает выигрыш: '
                    'сравните firstPaint до и после.',
       'starter': 'function firstPaint(resources) {\n}\nfunction optimize(resources) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const res = [{ name: "index.html", type: "html", size: 20 }, { name: "app.css", type: '
                 '"css", size: 40 }, { name: "vendor.js", type: "js", size: 200, blocking: true, defer: true '
                 '}, { name: "app.js", type: "js", size: 100, blocking: true }, { name: "hero.png", type: '
                 '"img", size: 500 }, { name: "analytics.js", type: "js", size: 30, blocking: false }];\n'
                 'console.log(JSON.stringify(firstPaint(res)));\n'
                 'const o = optimize(res);\n'
                 'console.log(o.gain, JSON.stringify(firstPaint(o.resources)), res[2].blocking);\n'
                 'console.log(JSON.stringify(firstPaint([{ name: "i.html", type: "html", size: 5 }])), '
                 'optimize([]).gain);\n',
       'hint': 'Блокирующие ресурсы: html, css и js с blocking; время — сумма размеров плюс 5 мс на каждый '
               'css/js плюс 10.',
       'expected': ['{"firstPaint":385,"blockedBy":["index.html","app.css","vendor.js","app.js"]}',
                    '205 {"firstPaint":180,"blockedBy":["index.html","app.css","app.js"]} true',
                    '{"firstPaint":15,"blockedBy":["i.html"]} 0']},
      {'id': 'j13-layout-thrash',
       'mode': 'js',
       'title': 'Принудительная раскладка (layout thrashing)',
       'statement': 'Последовательность операций с DOM: "read" (чтение геометрии: offsetHeight, '
                    'getBoundingClientRect) и "write" (запись стиля). Раскладка пересчитывается при чтении, '
                    'если после последней раскладки была запись. Напишите функцию countLayouts(ops) → число '
                    'принудительных раскладок; и функцию batch(ops) → массив операций, где сначала идут все '
                    'чтения, затем все записи (с сохранением порядка внутри групп) — такой пакет даёт не '
                    'более одной раскладки; проверьте оба.',
       'starter': 'function countLayouts(ops) {\n}\nfunction batch(ops) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const loop = ["read", "write", "read", "write", "read", "write"];\n'
                 'console.log(countLayouts(loop), countLayouts(batch(loop)), JSON.stringify(batch(loop)));\n'
                 'console.log(countLayouts(["write", "write", "read"]), countLayouts(["read", "read"]), '
                 'countLayouts(["write"]), countLayouts([]));\n'
                 'console.log(countLayouts(["read", "write", "read", "read", "write", "write", "read"]));\n'
                 'const many = Array.from({ length: 1000 }, (_, i) => (i % 2 ? "write" : "read"));\n'
                 'console.log(countLayouts(many), countLayouts(batch(many)));\n',
       'hint': 'Флаг «грязно» после записи; чтение при грязном — раскладка и сброс флага.',
       'expected': ['2 0 ["read","read","read","write","write","write"]', '1 0 0 0', '2', '499 0']},
      {'id': 'j13-raf-scheduler',
       'mode': 'js',
       'title': 'Планировщик requestAnimationFrame',
       'statement': 'Напишите класс FrameLoop: requestAnimationFrame(cb) → id; cancelAnimationFrame(id); '
                    'tick(time) — «кадр»: вызывает все накопленные к моменту начала кадра колбэки в порядке '
                    'регистрации с аргументом time; колбэки, зарегистрированные во время кадра, выполняются '
                    'в следующем кадре; отменённые не вызываются; возвращает число вызванных. Метод '
                    'pending() — число ожидающих.',
       'starter': 'class FrameLoop {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const f = new FrameLoop();\n'
                 'const log = [];\n'
                 'const a = f.requestAnimationFrame((t) => { log.push("a@" + t); '
                 'f.requestAnimationFrame((t2) => log.push("a2@" + t2)); });\n'
                 'f.requestAnimationFrame((t) => log.push("b@" + t));\n'
                 'const c = f.requestAnimationFrame((t) => log.push("c@" + t));\n'
                 'f.cancelAnimationFrame(c);\n'
                 'console.log(f.pending());\n'
                 'console.log(f.tick(16), f.pending(), log.join(" "));\n'
                 'console.log(f.tick(33), f.pending(), log.join(" "));\n'
                 'console.log(f.tick(50), typeof a);\n'
                 'let n = 0;\n'
                 'const loop = (t) => { if (++n < 3) f.requestAnimationFrame(loop); };\n'
                 'f.requestAnimationFrame(loop);\n'
                 'console.log(f.tick(1), f.tick(2), f.tick(3), f.tick(4), n);\n',
       'hint': 'В tick сделайте снимок очереди и очистите её до вызова колбэков.',
       'expected': ['2', '2 1 a@16 b@16', '1 0 a@16 b@16 a2@33', '0 number', '1 1 1 0 3']},
      {'id': 'j13-mutation-observer',
       'mode': 'js',
       'title': 'MutationObserver: пакетная доставка',
       'statement': 'Напишите функцию createObserver(callback): возвращает объект { record(mutation), '
                    'disconnect(), takeRecords() }; записи копятся и доставляются callback(records) одним '
                    'вызовом как микрозадача (queueMicrotask) после текущего кода; если за это время '
                    'записано несколько изменений — callback вызывается один раз со всеми; после disconnect '
                    'новые записи игнорируются, а запланированная доставка отменяется; takeRecords() '
                    'возвращает накопленные записи и очищает их.',
       'starter': 'function createObserver(callback) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const calls = [];\n'
                 'const o = createObserver((rs) => calls.push(rs.map((r) => r.t).join("+")));\n'
                 'o.record({ t: "a" }); o.record({ t: "b" }); o.record({ t: "c" });\n'
                 'console.log(calls.length);\n'
                 'await Promise.resolve();\n'
                 'console.log(JSON.stringify(calls));\n'
                 'const o2 = createObserver((rs) => calls.push("o2:" + rs.length));\n'
                 'o2.record({ t: 1 }); o2.record({ t: 2 });\n'
                 'console.log(JSON.stringify(o2.takeRecords()), JSON.stringify(o2.takeRecords()));\n'
                 'await Promise.resolve();\n'
                 'console.log(JSON.stringify(calls));\n'
                 'const o3 = createObserver((rs) => calls.push("o3"));\n'
                 'o3.record({ t: 1 }); o3.disconnect(); o3.record({ t: 2 });\n'
                 'await Promise.resolve();\n'
                 'console.log(JSON.stringify(calls));\n'
                 'o.record({ t: "d" });\n'
                 'await new Promise((r) => setTimeout(r, 5));\n'
                 'console.log(calls.at(-1), calls.length);\n',
       'hint': 'Один флаг «доставка запланирована»; доставка — через queueMicrotask.',
       'expected': ['0', '["a+b+c"]', '[{"t":1},{"t":2}] []', '["a+b+c"]', '["a+b+c"]', 'd 2']},
      {'id': 'j13-timer-clamp',
       'mode': 'js',
       'title': 'Зажим вложенных таймеров',
       'statement': 'Правило браузера: если вложенность setTimeout больше 5, минимальная задержка 4 мс. '
                    'Напишите функцию nestedDelays(requested, depth): requested — задержка, которую просил '
                    'код (мс); depth — уровень вложенности (1 для вызова из скрипта); возвращает реальную '
                    'задержку. Затем функцию chainTimes(requested, n): вызывает цепочку из n вложенных '
                    'setTimeout(f, requested) (глубина растёт) и возвращает массив моментов выполнения '
                    '(накопительно, от 0). Отдельно: backgroundDelay(requested, hidden) — в скрытой вкладке '
                    'не меньше 1000 мс.',
       'starter': 'function nestedDelays(requested, depth) {\n'
                  '}\n'
                  'function chainTimes(requested, n) {\n'
                  '}\n'
                  'function backgroundDelay(requested, hidden) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(nestedDelays(0, 1), nestedDelays(0, 5), nestedDelays(0, 6), nestedDelays(10, '
                 '9), nestedDelays(2, 100), nestedDelays(4, 7));\n'
                 'console.log(JSON.stringify(chainTimes(0, 10)));\n'
                 'console.log(JSON.stringify(chainTimes(10, 3)), JSON.stringify(chainTimes(1, 7)), '
                 'JSON.stringify(chainTimes(0, 0)));\n'
                 'console.log(backgroundDelay(0, true), backgroundDelay(5000, true), backgroundDelay(10, '
                 'false), backgroundDelay(999, true));\n',
       'hint': 'Условие: depth > 5 → max(requested, 4).',
       'expected': ['0 0 4 10 4 4',
                    '[0,0,0,0,0,4,8,12,16,20]',
                    '[10,20,30] [1,2,3,4,5,9,13] []',
                    '1000 5000 10 1000']},
      {'id': 'j13-interval-drift',
       'mode': 'js',
       'title': 'setInterval против рекурсивного setTimeout',
       'statement': 'Работа занимает work мс, интервал — period мс (work может быть больше period). Напишите '
                    'функцию intervalStarts(period, work, n): моменты начала n запусков при setInterval '
                    '(колбэк ставится в очередь строго каждые period мс, но не начинается, пока предыдущий '
                    'не закончился; пропущенные «тики» не накапливаются: если очередь уже содержит колбэк, '
                    'новый не ставится); и функцию timeoutStarts(period, work, n): моменты начала при '
                    'рекурсивном setTimeout (следующий — через period после окончания работы).',
       'starter': 'function intervalStarts(period, work, n) {\n'
                  '}\n'
                  'function timeoutStarts(period, work, n) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(intervalStarts(100, 30, 4)), JSON.stringify(timeoutStarts(100, '
                 '30, 4)));\n'
                 'console.log(JSON.stringify(intervalStarts(100, 150, 4)), JSON.stringify(timeoutStarts(100, '
                 '150, 3)));\n'
                 'console.log(JSON.stringify(intervalStarts(50, 50, 4)), JSON.stringify(intervalStarts(10, '
                 '0, 3)), JSON.stringify(intervalStarts(100, 30, 0)));\n'
                 'console.log(JSON.stringify(intervalStarts(100, 260, 3)));\n',
       'hint': 'Следите, когда поток освобождается; при занятом потоке в очереди не больше одного колбэка.',
       'expected': ['[100,200,300,400] [100,230,360,490]',
                    '[100,250,400,550] [100,350,600]',
                    '[50,100,150,200] [10,20,30] []',
                    '[100,360,620]']},
      {'id': 'j13-time-slicing',
       'mode': 'js',
       'title': 'Нарезка работы по бюджету',
       'statement': 'Напишите функцию processInChunks(items, work, { budget, now, yieldFn }): обрабатывает '
                    'элементы по порядку вызовом work(item); после каждого элемента проверяет now(): если с '
                    'начала текущего куска прошло не меньше budget мс — вызывает await yieldFn() (отдаёт '
                    'управление) и начинает новый кусок. Возвращает { processed, yields }. now() — '
                    'виртуальные часы, которые продвигает work.',
       'starter': 'async function processInChunks(items, work, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let clock = 0;\n'
                 'const now = () => clock;\n'
                 'const log = [];\n'
                 'const r = await processInChunks([10, 20, 30, 5, 5, 40, 50, 1], (cost) => { clock += cost; '
                 'log.push(cost); }, { budget: 50, now, yieldFn: async () => { log.push("|"); clock += 1; } '
                 '});\n'
                 'console.log(JSON.stringify(r), log.join(" "));\n'
                 'clock = 0;\n'
                 'console.log(JSON.stringify(await processInChunks([], () => {}, { budget: 50, now, yieldFn: '
                 'async () => {} })));\n'
                 'clock = 0;\n'
                 'let ys = 0;\n'
                 'console.log(JSON.stringify(await processInChunks(Array(10).fill(10), (c) => { clock += c; '
                 '}, { budget: 30, now, yieldFn: async () => { ys++; } })), ys);\n',
       'hint': 'chunkStart обновляется после каждой отдачи управления.',
       'expected': ['{"processed":8,"yields":3} 10 20 30 | 5 5 40 | 50 | 1',
                    '{"processed":0,"yields":0}',
                    '{"processed":10,"yields":3} 3']},
      {'id': 'j13-structured-clone',
       'mode': 'js',
       'title': 'Структурное клонирование',
       'statement': 'Напишите функцию cloneForMessage(value): копирует значения так же, как postMessage: '
                    'примитивы, Date, RegExp, Map, Set, массивы, обычные объекты (с циклическими ссылками — '
                    'цикл сохраняется в копии); undefined и NaN сохраняются. Функции и символы не '
                    'копируются: бросьте ошибку с name «DataCloneError». Классы с прототипами копируются как '
                    'обычные объекты (прототип теряется). structuredClone использовать нельзя.',
       'starter': 'function cloneForMessage(value) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const src = { d: new Date(0), r: /a+/gi, m: new Map([["k", { x: 1 }]]), s: new Set([1, '
                 '2]), arr: [1, [2, 3]], u: undefined, n: NaN, nested: { deep: { v: 1 } } };\n'
                 'src.self = src;\n'
                 'const c = cloneForMessage(src);\n'
                 'console.log(c !== src, c.self === c, c.d instanceof Date, c.d !== src.d, c.d.getTime(), '
                 'String(c.r), c.m.get("k").x, c.m.get("k") !== src.m.get("k"), c.s.has(2), '
                 'JSON.stringify(c.arr), "u" in c, c.u, Number.isNaN(c.n));\n'
                 'class P { constructor() { this.v = 1; } get() { return this.v; } }\n'
                 'const p = cloneForMessage(new P());\n'
                 'console.log(p.v, typeof p.get, p instanceof P);\n'
                 'for (const bad of [() => 1, Symbol("s"), { ok: 1, f() {} }]) { try { cloneForMessage(bad); '
                 'console.log("скопировано?"); } catch (e) { console.log(e.name); } }\n'
                 'const shared = { x: 1 };\n'
                 'const two = cloneForMessage([shared, shared]);\n'
                 'console.log(two[0] === two[1], two[0] !== shared);\n'
                 'console.log(__count("structu" + "redClone"));\n',
       'hint': 'Словарь «исходный объект → копия» нужен для циклов и повторных ссылок.',
       'expected': ['true true true true 0 /a+/gi 1 true true [1,[2,3]] true undefined true',
                    '1 undefined false',
                    'DataCloneError',
                    'DataCloneError',
                    'DataCloneError',
                    'true true',
                    '0']},
      {'id': 'j13-message-channel',
       'mode': 'js',
       'title': 'Передача управления: порядок очередей',
       'statement': 'Напишите функцию order(): возвращает промис массива строк, порядок которых получится '
                    'при запуске в Node.js: «sync», «микрозадача» (queueMicrotask), «nextTick» '
                    '(process.nextTick — в ESM он идёт после микрозадач), «MessageChannel» (сообщение через '
                    'new MessageChannel(): port1.onmessage), «setTimeout» (0 мс). Ваша задача — собрать код '
                    'так, чтобы порядок получился: sync, микрозадача, nextTick, MessageChannel, setTimeout.',
       'starter': 'function order() {\n}\n',
       'driver': '/*__DRIVER__*/\nconsole.log((await order()).join(" > "));\n',
       'hint': 'Порядок решает сама очередь: sync → микрозадачи → nextTick (в ESM) → сообщения → таймер; '
               'таймер с запасом (например, 20 мс).',
       'expected': ['sync > микрозадача > nextTick > MessageChannel > setTimeout']},
      {'id': 'j13-perf-marks',
       'mode': 'js',
       'title': 'performance.mark и measure',
       'statement': 'Напишите функцию createPerf(now): now() — часы; возвращает объект с mark(name) → запись '
                    '{ name, startTime, entryType: "mark" }, measure(name, startMark, endMark?) → запись { '
                    'name, startTime, duration, entryType: "measure" } (если endMark не указан — до текущего '
                    'момента; для неизвестной метки — Error("Метка не найдена: <имя>")), getEntries() (по '
                    'времени начала), getEntriesByName(name), clear().',
       'starter': 'function createPerf(now) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let t = 0;\n'
                 'const p = createPerf(() => t);\n'
                 'p.mark("start"); t = 30; p.mark("mid"); t = 100;\n'
                 'console.log(JSON.stringify(p.measure("первая половина", "start", "mid")), '
                 'JSON.stringify(p.measure("всего", "start")));\n'
                 'console.log(p.getEntries().map((e) => `${e.entryType}:${e.name}@${e.startTime}`).join(" | '
                 '"));\n'
                 'console.log(p.getEntriesByName("mid").length, p.getEntriesByName("нет").length);\n'
                 'try { p.measure("x", "нет-метки"); } catch (e) { console.log(e.message); }\n'
                 'p.clear();\n'
                 'console.log(p.getEntries().length);\n'
                 't = 200; p.mark("a"); t = 250; p.mark("a"); t = 260;\n'
                 'console.log(JSON.stringify(p.measure("от последней a", "a")));\n',
       'hint': 'Последняя метка с данным именем — та, от которой считаем.',
       'expected': ['{"name":"первая половина","startTime":0,"duration":30,"entryType":"measure"} '
                    '{"name":"всего","startTime":0,"duration":100,"entryType":"measure"}',
                    'mark:start@0 | measure:первая половина@0 | measure:всего@0 | mark:mid@30',
                    '1 0',
                    'Метка не найдена: нет-метки',
                    '0',
                    '{"name":"от последней a","startTime":250,"duration":10,"entryType":"measure"}']},
      {'id': 'j13-long-task-observer',
       'mode': 'js',
       'title': 'Наблюдатель за долгими задачами',
       'statement': 'Напишите функцию createLongTaskObserver(threshold, onLongTask): возвращает объект { '
                    'run(name, duration, startTime) } — регистрирует выполнение задачи; если duration > '
                    'threshold, вызывает onLongTask({ name, duration, startTime, blockingTime: duration - '
                    'threshold }); и summary() → { count, total, worst: { name, duration } | null } — сводка '
                    'только по долгим задачам.',
       'starter': 'function createLongTaskObserver(threshold, onLongTask) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const seen = [];\n'
                 'const o = createLongTaskObserver(50, (r) => seen.push(`${r.name}:${r.blockingTime}`));\n'
                 'o.run("click", 20, 0); o.run("render", 120, 100); o.run("parse", 51, 300); o.run("idle", '
                 '50, 400); o.run("big", 120, 500);\n'
                 'console.log(seen.join(" "), JSON.stringify(o.summary()));\n'
                 'console.log(JSON.stringify(createLongTaskObserver(10, () => {}).summary()));\n',
       'hint': 'Хранить только долгие записи; blockingTime = duration − threshold.',
       'expected': ['render:70 parse:1 big:70 '
                    '{"count":3,"total":141,"worst":{"name":"render","duration":120}}',
                    '{"count":0,"total":0,"worst":null}']},
      {'id': 'j13-web-vitals',
       'mode': 'js',
       'title': 'Web Vitals: оценки и p75',
       'statement': 'Напишите функцию percentile(values, p) (по методу «ближайший ранг»: индекс ceil(p/100 * '
                    'n) - 1 в отсортированной копии; для пустого массива — null), функцию rate(metric, '
                    'value) → «good»/«needs-improvement»/«poor» по порогам: LCP — до 2500 хорошо, до 4000 '
                    'терпимо; INP — 200/500; CLS — 0.1/0.25 (границы включительно в лучшую категорию), и '
                    'reportVitals(samples) — по массиву замеров { LCP, INP, CLS } вернёт для каждой метрики '
                    '{ p75, rating } (метрики без замеров пропускаются).',
       'starter': 'function percentile(values, p) {\n'
                  '}\n'
                  'function rate(metric, value) {\n'
                  '}\n'
                  'function reportVitals(samples) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(percentile([5, 1, 3, 2, 4], 50), percentile([5, 1, 3, 2, 4], 75), '
                 'percentile([10], 99), percentile([], 50), percentile([1, 2, 3, 4], 100), percentile([1, 2, '
                 '3, 4], 0));\n'
                 'console.log(rate("LCP", 2500), rate("LCP", 2501), rate("LCP", 4001), rate("INP", 200), '
                 'rate("INP", 499), rate("CLS", 0.1), rate("CLS", 0.3));\n'
                 'const samples = [{ LCP: 1800, INP: 120, CLS: 0.02 }, { LCP: 2400, INP: 250, CLS: 0.05 }, { '
                 'LCP: 5200, INP: 80, CLS: 0.4 }, { LCP: 2100, CLS: 0.01 }, { LCP: 3000, INP: 90, CLS: 0 '
                 '}];\n'
                 'console.log(JSON.stringify(reportVitals(samples)));\n'
                 'console.log(JSON.stringify(reportVitals([])), JSON.stringify(reportVitals([{ LCP: 1000 '
                 '}])));\n',
       'hint': 'p75 по ближайшему рангу; пороги — по таблице.',
       'expected': ['3 4 10 null 4 1',
                    'good needs-improvement poor good needs-improvement good poor',
                    '{"LCP":{"p75":3000,"rating":"needs-improvement"},"INP":{"p75":120,"rating":"good"},"CLS":{"p75":0.05,"rating":"good"}}',
                    '{} {"LCP":{"p75":1000,"rating":"good"}}']},
      {'id': 'j13-cls',
       'mode': 'js',
       'title': 'Накопленный сдвиг макета (CLS)',
       'statement': 'Сдвиги макета заданы массивом { time, value } (мс, по возрастанию времени). Окна '
                    'сеанса: сдвиги группируются в окно, пока между соседними не больше 1000 мс и окно не '
                    'длиннее 5000 мс от первого сдвига; иначе начинается новое окно. CLS страницы — '
                    'наибольшая сумма value по окнам. Напишите функцию cls(shifts) → { value, windows: [{ '
                    'start, end, sum }] } (value и sum округляйте до 3 знаков).',
       'starter': 'function cls(shifts) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(cls([{ time: 100, value: 0.05 }, { time: 600, value: 0.1 }, { '
                 'time: 1500, value: 0.02 }, { time: 4000, value: 0.3 }, { time: 4500, value: 0.1 }])));\n'
                 'console.log(JSON.stringify(cls([])), JSON.stringify(cls([{ time: 0, value: 0.2 }])));\n'
                 'const long = Array.from({ length: 12 }, (_, i) => ({ time: i * 600, value: 0.01 }));\n'
                 'console.log(JSON.stringify(cls(long)));\n'
                 'console.log(JSON.stringify(cls([{ time: 0, value: 0.1 }, { time: 1000, value: 0.1 }, { '
                 'time: 2001, value: 0.1 }])));\n',
       'hint': 'Окно продолжается, пока разрыв ≤ 1000 мс и длина ≤ 5000 мс.',
       'expected': ['{"value":0.4,"windows":[{"start":100,"end":1500,"sum":0.17},{"start":4000,"end":4500,"sum":0.4}]}',
                    '{"value":0,"windows":[]} {"value":0.2,"windows":[{"start":0,"end":0,"sum":0.2}]}',
                    '{"value":0.09,"windows":[{"start":0,"end":4800,"sum":0.09},{"start":5400,"end":6600,"sum":0.03}]}',
                    '{"value":0.2,"windows":[{"start":0,"end":1000,"sum":0.2},{"start":2001,"end":2001,"sum":0.1}]}']},
      {'id': 'j13-site-isolation',
       'mode': 'js',
       'title': 'Процессы по сайтам',
       'statement': 'Изоляция сайтов: страницы одного сайта (схема + домен регистрации) делят процесс. '
                    'Напишите функцию siteOf(url): «схема://домен-регистрации» — берутся последние две части '
                    'имени хоста (для hosts вида a.b.co.uk считайте суффиксом из набора ["co.uk", "com.au"] '
                    '— тогда три части); IP-адреса и localhost — как есть. И функцию '
                    'assignProcesses(frames): frames — массив { id, url, parent? }; возвращает { processes: '
                    '[[id…], …] } — процессы в порядке первого появления сайта, id кадров в порядке входа.',
       'starter': 'function siteOf(url) {\n}\nfunction assignProcesses(frames) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const u of ["https://www.example.com/a?b=1", "https://api.shop.example.com", '
                 '"http://example.com", "https://bbc.co.uk/news", "https://www.bbc.co.uk", '
                 '"http://localhost:3000/x", "http://127.0.0.1:8080", "https://a.b.c.d.org"]) '
                 'console.log(siteOf(u));\n'
                 'console.log(JSON.stringify(assignProcesses([{ id: 1, url: "https://example.com/" }, { id: '
                 '2, url: "https://ads.net/banner", parent: 1 }, { id: 3, url: "https://blog.example.com/", '
                 'parent: 1 }, { id: 4, url: "http://example.com/old" }, { id: 5, url: '
                 '"https://cdn.ads.net/x", parent: 2 }])));\n',
       'hint': 'new URL(url).hostname; разные схемы — разные сайты.',
       'expected': ['https://example.com',
                    'https://example.com',
                    'http://example.com',
                    'https://bbc.co.uk',
                    'https://bbc.co.uk',
                    'http://localhost',
                    'http://127.0.0.1',
                    'https://d.org',
                    '{"processes":[[1,3],[2,5],[4]]}']},
      {'id': 'j13-fetch-priority',
       'mode': 'js',
       'title': 'Приоритеты загрузки ресурсов',
       'statement': 'Браузер назначает приоритеты: html — «highest»; css в head — «highest»; sync script в '
                    'head — «high»; font — «high»; изображения: в области видимости — «high», вне — «low»; '
                    'async/defer script — «low»; prefetch — «lowest»; preload меняет приоритет на «high» '
                    '(кроме prefetch). Напишите функцию priority(r): r = { type, inHead?, async?, defer?, '
                    'visible?, preload?, prefetch? } → строка; и функцию schedule(resources, maxParallel): '
                    'порядок запуска загрузок — сначала по приоритету (highest > high > low > lowest), при '
                    'равном — по входу; возвращает массив имён.',
       'starter': 'function priority(r) {\n}\nfunction schedule(resources, maxParallel) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const rs = [\n'
                 '  { name: "app.js", type: "script", defer: true },\n'
                 '  { name: "hero.png", type: "img", visible: true },\n'
                 '  { name: "footer.png", type: "img", visible: false },\n'
                 '  { name: "main.css", type: "css", inHead: true },\n'
                 '  { name: "analytics.js", type: "script", async: true },\n'
                 '  { name: "jq.js", type: "script", inHead: true },\n'
                 '  { name: "next.html", type: "html", prefetch: true },\n'
                 '  { name: "font.woff2", type: "font" },\n'
                 '  { name: "later.js", type: "script", defer: true, preload: true },\n'
                 '  { name: "index.html", type: "html" },\n'
                 '];\n'
                 'console.log(rs.map((r) => `${r.name}=${priority(r)}`).join(" "));\n'
                 'console.log(schedule(rs, 6).join(" > "));\n'
                 'console.log(JSON.stringify(schedule([], 6)));\n',
       'hint': 'Сначала особые случаи (prefetch, preload), затем таблица по типу ресурса.',
       'expected': ['app.js=low hero.png=high footer.png=low main.css=highest analytics.js=low jq.js=high '
                    'next.html=lowest font.woff2=high later.js=high index.html=highest',
                    'main.css > index.html > hero.png > jq.js > font.woff2 > later.js > app.js > footer.png '
                    '> analytics.js > next.html',
                    '[]']},
      {'id': 'j13-microtask-limit',
       'mode': 'js',
       'title': 'Голодание очереди микрозадач',
       'statement': 'Модель: очередь микрозадач — массив функций; каждая может вернуть массив новых '
                    'микрозадач (они добавляются в конец очереди). Напишите функцию drain(queue, limit): '
                    'выполняет очередь до опустошения; но если выполнено limit микрозадач, а очередь не '
                    'пуста — останавливается и сообщает «голодание»: { done, left, starved }. И функцию '
                    'fixStarvation(queue, limit): выполняет не более limit микрозадач, остальные '
                    'возвращаются как «следующая задача» (как будто уступили управление): { runNow, deferred '
                    '} — число выполненных сейчас и остаток очереди (массив функций).',
       'starter': 'function drain(queue, limit) {\n}\nfunction fixStarvation(queue, limit) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const log = [];\n'
                 'const finite = [() => { log.push("a"); return [() => log.push("a1")]; }, () => '
                 'log.push("b")];\n'
                 'console.log(JSON.stringify(drain(finite, 100)), log.join());\n'
                 'const forever = () => [forever];\n'
                 'console.log(JSON.stringify(drain([forever], 1000)), JSON.stringify(drain([], 5)));\n'
                 'const r = fixStarvation([forever, () => log.push("x")], 10);\n'
                 'console.log(r.runNow, r.deferred.length, typeof r.deferred[0]);\n'
                 'console.log(JSON.stringify(drain([() => [() => [() => []]]], 2)));\n',
       'hint': 'Очередь с лимитом числа выполненных; остаток — признак голодания или отложенные задачи.',
       'expected': ['{"done":3,"left":0,"starved":false} a,b,a1',
                    '{"done":1000,"left":1,"starved":true} {"done":0,"left":0,"starved":false}',
                    '10 1 function',
                    '{"done":2,"left":1,"starved":true}']},
      {'id': 'j13-leak-listeners',
       'mode': 'js',
       'title': 'Поиск утечек слушателей',
       'statement': 'Журнал событий — массив { op: "add"|"remove", target, type, id }, где id — '
                    'идентификатор слушателя. Напишите функцию findLeaks(log): слушатели, добавленные и ни '
                    'разу не удалённые (повторное добавление того же id на ту же пару target/type считается '
                    'новым слушателем, если предыдущий уже удалён; повторный add без remove — дубликат, он '
                    'не создаёт второго, но помечается в duplicates). Верните { leaked: [{ target, type, id '
                    '}] (порядок добавления), duplicates: число лишних add, unmatchedRemoves: число remove '
                    'без add }.',
       'starter': 'function findLeaks(log) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const log = [\n'
                 '  { op: "add", target: "window", type: "resize", id: "h1" },\n'
                 '  { op: "add", target: "document", type: "click", id: "h2" },\n'
                 '  { op: "add", target: "window", type: "resize", id: "h1" },\n'
                 '  { op: "remove", target: "document", type: "click", id: "h2" },\n'
                 '  { op: "remove", target: "document", type: "click", id: "h2" },\n'
                 '  { op: "add", target: "document", type: "click", id: "h2" },\n'
                 '  { op: "add", target: "btn", type: "click", id: "h3" },\n'
                 '  { op: "remove", target: "btn", type: "click", id: "h3" },\n'
                 '  { op: "add", target: "ws", type: "message", id: "h4" },\n'
                 '];\n'
                 'console.log(JSON.stringify(findLeaks(log)));\n'
                 'console.log(JSON.stringify(findLeaks([])));\n',
       'hint': 'Словарь активных слушателей по ключу target|type|id.',
       'expected': ['{"leaked":[{"target":"window","type":"resize","id":"h1"},{"target":"document","type":"click","id":"h2"},{"target":"ws","type":"message","id":"h4"}],"duplicates":1,"unmatchedRemoves":1}',
                    '{"leaked":[],"duplicates":0,"unmatchedRemoves":0}']},
      {'id': 'j13-fix-blocking',
       'mode': 'js',
       'title': 'Исправьте: блокировка главного потока',
       'statement': 'Функция sumBigAsync(n) считает сумму чисел от 1 до n. Сейчас она блокирует главный '
                    'поток на всё время расчёта: таймер с интервалом 10 мс не успевает ни разу сработать. '
                    'Перепишите так, чтобы вычисление шло кусками по 100000 итераций с передачей управления '
                    'между ними (await new Promise(r => setTimeout(r)) или setImmediate) и результат был тем '
                    'же; сумма — число (n до 5 000 000).',
       'starter': 'async function sumBigAsync(n) {\n'
                  '  let s = 0;\n'
                  '  for (let i = 1; i <= n; i++) s += i;\n'
                  '  return s;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let ticks = 0;\n'
                 'const timer = setInterval(() => { ticks++; }, 1);\n'
                 'const r = await sumBigAsync(3000000);\n'
                 'clearInterval(timer);\n'
                 'console.log(r, ticks > 0);\n'
                 'console.log(await sumBigAsync(10), await sumBigAsync(0));\n',
       'hint': 'Каждые 100000 итераций отдавайте управление циклу событий.',
       'expected': ['4500001500000 true', '55 0']},
      {'id': 'j13-fix-layout',
       'mode': 'js',
       'title': 'Исправьте: пакетная работа с «DOM»',
       'statement': 'Модель DOM: объекты { height, style } с методами read() (возвращает height и вызывает '
                    'пересчёт раскладки, если были записи) и write(v) (меняет height). Функция '
                    'grow(elements) должна увеличить высоту каждого элемента на высоту первого; сейчас она '
                    'чередует чтение и запись и вызывает раскладку на каждой итерации. Исправьте: сначала '
                    'считайте все высоты, потом записывайте (число раскладок — не больше одной). Верните '
                    'массив новых высот.',
       'starter': 'function grow(elements) {\n'
                  '  const out = [];\n'
                  '  for (const el of elements) {\n'
                  '    const first = elements[0].read();\n'
                  '    const h = el.read();\n'
                  '    el.write(h + first);\n'
                  '    out.push(h + first);\n'
                  '  }\n'
                  '  return out;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'function makeDom(heights) {\n'
                 '  let layouts = 0, dirty = false;\n'
                 '  const els = heights.map((h) => ({ height: h, read() { if (dirty) { layouts++; dirty = '
                 'false; } return this.height; }, write(v) { this.height = v; dirty = true; } }));\n'
                 '  return { els, layouts: () => layouts };\n'
                 '}\n'
                 'const d = makeDom([10, 20, 30, 40]);\n'
                 'const r = grow(d.els);\n'
                 'console.log(JSON.stringify(r), d.layouts() <= 1, JSON.stringify(d.els.map((e) => '
                 'e.height)));\n'
                 'const d2 = makeDom([5]);\n'
                 'console.log(JSON.stringify(grow(d2.els)), d2.layouts());\n',
       'hint': 'Сначала все read(), затем все write() — тогда раскладка не пересчитывается между ними.',
       'expected': ['[20,30,40,50] true [20,30,40,50]', '[10] 0']},
      {'id': 'j13-css-triggers',
       'mode': 'js',
       'title': 'Что пересчитает браузер',
       'statement': 'Для каждого свойства CSS известно, какие этапы оно запускает: layout (раскладка → '
                    'рисование → композиция), paint (рисование → композиция) или composite (только '
                    'композиция). Напишите функцию stageOf(prop): width, height, margin*, padding*, '
                    'top/left/right/bottom, display, position, font-size, border-width, flex*, grid* → '
                    '«layout»; color, background*, box-shadow, border-color, border-radius, outline*, '
                    'visibility → «paint»; transform, opacity, filter, will-change → «composite»; '
                    'неизвестное → «layout» (на всякий случай). И cost(props) → самый дорогой этап среди '
                    'свойств (layout > paint > composite), для пустого списка — «none».',
       'starter': 'function stageOf(prop) {\n}\nfunction cost(props) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const p of ["width", "margin-left", "padding-top", "top", "display", "font-size", '
                 '"flex-grow", "grid-template-columns", "color", "background-color", "box-shadow", '
                 '"border-radius", "outline-width", "visibility", "transform", "opacity", "filter", '
                 '"will-change", "cursor", "z-index"]) console.log(p, stageOf(p));\n'
                 'console.log(cost(["opacity", "transform"]), cost(["opacity", "color"]), cost(["color", '
                 '"width"]), cost([]), cost(["unknown-prop"]));\n',
       'hint': 'Таблицы регулярных выражений по типам этапов; composite проверяйте первым.',
       'expected': ['width layout',
                    'margin-left layout',
                    'padding-top layout',
                    'top layout',
                    'display layout',
                    'font-size layout',
                    'flex-grow layout',
                    'grid-template-columns layout',
                    'color paint',
                    'background-color paint',
                    'box-shadow paint',
                    'border-radius paint',
                    'outline-width paint',
                    'visibility paint',
                    'transform composite',
                    'opacity composite',
                    'filter composite',
                    'will-change composite',
                    'cursor layout',
                    'z-index layout',
                    'composite paint layout none layout']},
      {'id': 'j13-idle-callback',
       'mode': 'js',
       'title': 'requestIdleCallback на виртуальном времени',
       'statement': 'Напишите класс IdleScheduler(now): метод requestIdleCallback(cb, { timeout } = {}) → '
                    'id; cancelIdleCallback(id); runIdle(frameEnd) — «простой» до момента frameEnd: вызывает '
                    'колбэки в порядке регистрации, передавая deadline = { timeRemaining() → max(0, frameEnd '
                    '- now()), didTimeout: false }; колбэк вызывается, только если timeRemaining() > 0 в '
                    'момент вызова; остальные ждут следующего простоя; колбэки с timeout, у которых срок '
                    '(момент регистрации + timeout) уже наступил, а простоя нет, вызываются методом '
                    'runTimeouts() с didTimeout: true и timeRemaining() = 0. Возвращает число вызванных.',
       'starter': 'class IdleScheduler {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let t = 0;\n'
                 'const s = new IdleScheduler(() => t);\n'
                 'const log = [];\n'
                 'const job = (name, cost) => (d) => { log.push(`${name}(осталось ${d.timeRemaining()}, '
                 'timeout=${d.didTimeout})`); t += cost; };\n'
                 's.requestIdleCallback(job("a", 5));\n'
                 'const b = s.requestIdleCallback(job("b", 30));\n'
                 's.requestIdleCallback(job("c", 5), { timeout: 100 });\n'
                 's.requestIdleCallback(job("d", 1), { timeout: 20 });\n'
                 's.cancelIdleCallback(b);\n'
                 'console.log(s.runIdle(8), t, log.join(" | "));\n'
                 'log.length = 0;\n'
                 'console.log(s.runIdle(t), log.length);\n'
                 't = 50;\n'
                 'console.log(s.runTimeouts(), log.join(" | "));\n'
                 't = 120;\n'
                 'log.length = 0;\n'
                 'console.log(s.runTimeouts(), s.runIdle(200), log.length);\n',
       'hint': 'Простой заканчивается, когда timeRemaining() станет 0; задачи с timeout выполняются отдельно '
               'при просрочке.',
       'expected': ['2 10 a(осталось 8, timeout=false) | c(осталось 3, timeout=false)',
                    '0 0',
                    '1 d(осталось 0, timeout=true)',
                    '0 0 0']}]}
