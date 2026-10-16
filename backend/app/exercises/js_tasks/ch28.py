"""Задачи книги «Современный Frontend»: глава 28."""

TASKS: dict[int, list[dict]] = {28: [{'id': 'j28-store',
  'mode': 'js',
  'title': 'Хранилище с подписками',
  'statement': 'Напишите createStore(initial): { get, set, subscribe }. get() возвращает значение; '
               'set(v) меняет его и, только если !Object.is(старое, новое), синхронно вызывает '
               'подписчиков в порядке подписки с аргументами (новое, старое); subscribe(fn) '
               'добавляет подписчика (немедленного вызова нет) и возвращает функцию отписки '
               '(повторный вызов безвреден). Отписка во время рассылки не должна менять набор уже '
               'начавшегося обхода: в текущей рассылке отписавшийся, но ещё не вызванный подписчик '
               'всё равно вызывается; подписка во время рассылки начнёт получать только следующие '
               'изменения.',
  'starter': 'function createStore(initial) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = createStore(1);\n'
            'const log = [];\n'
            'const offA = s.subscribe((n, o) => log.push(`A:${o}->${n}`));\n'
            'const offB = s.subscribe((n) => { log.push(`B:${n}`); offA(); });\n'
            's.subscribe((n) => { if (n === 2) s.subscribe((m) => log.push(`late:${m}`)); });\n'
            's.set(1); s.set(2); s.set(3);\n'
            'console.log(log.join(" "), s.get());\n'
            'offB(); offB(); s.set(4);\n'
            'console.log(log.join(" "));\n'
            'const n = createStore(NaN); let calls = 0; n.subscribe(() => calls++); n.set(NaN); '
            'n.set(0); n.set(-0); console.log(calls);\n',
  'hint': 'Храните массив/Set; при рассылке работайте со снимком [...subs].',
  'expected': ['A:1->2 B:2 B:3 late:3 3', 'A:1->2 B:2 B:3 late:3 late:4', '2']},
 {'id': 'j28-signal-basic',
  'mode': 'js',
  'title': 'Сигнал: get, set, update, peek',
  'statement': 'Напишите signal(initial, opts = {}): функция-геттер s() возвращает значение. '
               'Методы: s.peek() — то же значение; s.set(v) — записать; s.update(fn) — записать '
               'fn(старое); s.subscribe(cb) — ручная подписка, возвращает отписку. cb(новое, '
               'старое) вызывается синхронно при каждом изменении. Изменением считается результат: '
               '!equals(старое, новое), где equals — opts.equals или Object.is.',
  'starter': 'function signal(initial, opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = signal(1);\n'
            'const log = [];\n'
            'const off = s.subscribe((n, o) => log.push(`${o}->${n}`));\n'
            'console.log(s(), s.peek());\n'
            's.set(2); s.set(2); s.update((x) => x * 10); off(); s.set(0);\n'
            'console.log(log.join(" "), s());\n'
            'const f = signal(1, { equals: (a, b) => Math.abs(a - b) < 0.5 });\n'
            'let n = 0; f.subscribe(() => n++);\n'
            'f.set(1.2); f.set(2); f.set(2.1); f.set(0);\n'
            'console.log(n, f());\n',
  'hint': 'Функция read с навешенными методами; массив подписчиков.',
  'expected': ['1 1', '1->2 2->20 0', '2 0']},
 {'id': 'j28-effect',
  'mode': 'js',
  'title': 'Эффект с автоотслеживанием',
  'statement': 'Напишите signal(value) и effect(fn) с автоотслеживанием. Сигнал: s() читает; если '
               'чтение произошло внутри effect — эффект становится подписчиком; s.set(v) '
               'записывает, и если !Object.is(старое, новое) — перезапускает подписанные эффекты '
               '(в порядке подписки). effect(fn): запускает fn сразу; при перезапуске fn '
               'выполняется заново. Возвращает функцию stop(), после которой эффект не '
               'запускается. Допустимо считать, что зависимости не меняются от запуска к запуску '
               '(динамические — в следующей задаче).',
  'starter': 'function signal(value) {\n}\nfunction effect(fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = signal(1), b = signal(10);\n'
            'const log = [];\n'
            'const stop = effect(() => log.push(`sum=${a() + b()}`));\n'
            'a.set(2); b.set(20); a.set(2); b.set(20);\n'
            'console.log(log.join(" "));\n'
            'stop();\n'
            'a.set(100);\n'
            'console.log(log.length);\n'
            'const c = signal(0);\n'
            'const l2 = [];\n'
            'effect(() => l2.push("one:" + c()));\n'
            'effect(() => l2.push("two:" + c()));\n'
            'c.set(1);\n'
            'console.log(l2.join(" "));\n'
            'const n = signal(NaN); let runs = 0; effect(() => { n(); runs++; }); n.set(NaN); '
            'console.log(runs);\n',
  'hint': 'Глобальная переменная currentEffect; в геттере: if (currentEffect) '
          'subs.add(currentEffect).',
  'expected': ['sum=11 sum=12 sum=22', '3', 'one:0 two:0 one:1 two:1', '1']},
 {'id': 'j28-dynamic-deps',
  'mode': 'js',
  'title': 'Динамические зависимости',
  'statement': 'Ядро (signal, effect) уже есть в заготовке, но в нём есть ошибка-упрощение: эффект '
               'не отписывается от сигналов, которые перестал читать, и эффект не обнуляется. '
               'Допишите функцию trackedSubscribers(...signals) → массив числа подписчиков у '
               'каждого сигнала. Но главное — исправьте ядро: перед каждым запуском эффект должен '
               'отписываться от всех прежних источников (набор e.deps хранит множества '
               'подписчиков, из которых нужно удалить эффект) и заново собирать зависимости. '
               'Сделайте это в e.run(). Итог: подписчики сигналов должны соответствовать только '
               'последнему запуску.',
  'starter': 'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.subscriberCount = () => subs.size;\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    run() {\n'
             '      // TODO: перед запуском отписаться от прежних источников\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '  };\n'
             '  e.run();\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const mode = signal(true), a = signal("A"), b = signal("B");\n'
            'const log = [];\n'
            'effect(() => log.push(mode() ? a() : b()));\n'
            'console.log(log.join(","), a.subscriberCount(), b.subscriberCount(), '
            'mode.subscriberCount());\n'
            'mode.set(false);\n'
            'console.log(log.join(","), a.subscriberCount(), b.subscriberCount());\n'
            'a.set("A2");\n'
            'console.log(log.join(","));\n'
            'b.set("B2");\n'
            'console.log(log.join(","));\n'
            'mode.set(true);\n'
            'a.set("A3");\n'
            'console.log(log.join(","), a.subscriberCount(), b.subscriberCount());\n',
  'hint': 'В начале run(): for (const d of e.deps) d.delete(e); e.deps.clear();',
  'expected': ['A 1 0 1', 'A,B 0 1', 'A,B', 'A,B,B2', 'A,B,B2,A2,A3 1 0']},
 {'id': 'j28-computed',
  'mode': 'js',
  'title': 'Вычисляемое значение',
  'statement': 'Ядро (signal, effect с динамическими зависимостями) уже есть. Напишите '
               'computed(fn): возвращает функцию-геттер c(). Значение вычисляется лениво при '
               'первом чтении и кэшируется; пока источники не менялись, повторные чтения не '
               'вызывают fn. Когда изменился любой прочитанный внутри fn сигнал или computed, '
               'значение помечается устаревшим и пересчитывается при следующем чтении. Чтение c() '
               'внутри effect делает эффект зависимым от c: эффект должен перезапускаться при '
               'изменении значения источников (допустимо перезапускать при любом изменении '
               'источника, даже если итог не изменился).',
  'starter': '// Готовое ядро (не изменяйте): сигнал, эффект и вычисляемое значение с '
             'автоотслеживанием\n'
             'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.update = (fn) => read.set(fn(value));\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    cleanup: undefined,\n'
             '    active: true,\n'
             '    run() {\n'
             '      if (!e.active) return;\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '    stop() { e.active = false; for (const d of e.deps) d.delete(e); e.deps.clear(); '
             '},\n'
             '  };\n'
             '  e.run();\n'
             '  return e.stop;\n'
             '}\n'
             'function computed(fn) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const first = signal("Ann"), last = signal("Lee");\n'
            'let calls = 0;\n'
            'const full = computed(() => { calls++; return first() + " " + last(); });\n'
            'console.log(calls);\n'
            'console.log(full(), calls);\n'
            'console.log(full(), calls);\n'
            'first.set("Bob");\n'
            'console.log(calls);\n'
            'console.log(full(), calls);\n'
            'const log = [];\n'
            'effect(() => log.push(full().toUpperCase()));\n'
            'last.set("Kim");\n'
            'console.log(log.join("|"), calls);\n'
            'const base = signal(2);\n'
            'const sq = computed(() => base() ** 2);\n'
            'const plus = computed(() => sq() + 1);\n'
            'console.log(plus());\n'
            'base.set(3);\n'
            'console.log(plus(), sq());\n',
  'hint': 'Внутри computed используйте служебный effect-подобный объект: при изменении источника '
          'помечайте dirty и оповещайте собственных подписчиков.',
  'expected': ['0', 'Ann Lee 1', 'Ann Lee 1', '1', 'Bob Lee 2', 'BOB LEE|BOB KIM 3', '5', '10 9']},
 {'id': 'j28-cleanup',
  'mode': 'js',
  'title': 'Очистка эффекта и dispose',
  'statement': 'Напишите signal(v) (с автоотслеживанием и повторной подпиской на каждом запуске) и '
               'effect(fn). Если fn возвращает функцию — это очистка: она вызывается '
               'непосредственно перед следующим запуском эффекта и при его остановке. effect '
               'возвращает функцию stop(): вызывает последнюю очистку (если есть), отписывает '
               'эффект от всех источников; после неё эффект не запускается; повторный stop '
               'безвреден. Исключение в очистке пробрасывается наружу.',
  'starter': 'function signal(v) {\n}\nfunction effect(fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const n = signal(0);\n'
            'const log = [];\n'
            'const stop = effect(() => {\n'
            '  const v = n();\n'
            '  log.push("run" + v);\n'
            '  return () => log.push("clean" + v);\n'
            '});\n'
            'n.set(1); n.set(2);\n'
            'console.log(log.join(" "));\n'
            'stop(); stop();\n'
            'console.log(log.join(" "));\n'
            'n.set(3);\n'
            'console.log(log.join(" "));\n'
            'const stop2 = effect(() => { n(); });\n'
            'stop2();\n'
            'console.log("ok");\n',
  'hint': 'Храните cleanup в замыкании эффекта; вызывайте его в начале run() и в stop().',
  'expected': ['run0 clean0 run1 clean1 run2',
               'run0 clean0 run1 clean1 run2 clean2',
               'run0 clean0 run1 clean1 run2 clean2',
               'ok']},
 {'id': 'j28-batch',
  'mode': 'js',
  'title': 'batch: группировка записей',
  'statement': 'Ядро (signal, effect) уже есть. Напишите batch(fn): выполняет fn, откладывая '
               'запуск эффектов. Записи сигналов внутри batch не запускают эффекты сразу; после '
               'выхода из самого внешнего batch каждый затронутый эффект запускается ровно один '
               'раз (в порядке первого затрагивания). Вложенные batch работают как один внешний. '
               'Результат batch — результат fn; при исключении в fn отложенные эффекты всё равно '
               'запускаются, а исключение пробрасывается. Для этого перепишите read.set в ядре '
               'так, чтобы при batchDepth > 0 эффекты ставились в очередь pending (Set).',
  'starter': 'let current = null;\n'
             'let batchDepth = 0;\n'
             'const pending = new Set();\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run(); // TODO: при batchDepth > 0 откладывать\n'
             '  };\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    run() {\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '  };\n'
             '  e.run();\n'
             '}\n'
             'function batch(fn) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = signal(1), b = signal(2), c = signal(3);\n'
            'const log = [];\n'
            'effect(() => log.push(`abc=${a()},${b()},${c()}`));\n'
            'a.set(10); b.set(20);\n'
            'console.log(log.join(" | "));\n'
            'log.length = 0;\n'
            'const r = batch(() => { a.set(1); b.set(2); c.set(4); return "done"; });\n'
            'console.log(log.join(" | "), r);\n'
            'log.length = 0;\n'
            'batch(() => { a.set(5); batch(() => { b.set(6); }); console.log("inner done", '
            'log.length); c.set(7); });\n'
            'console.log(log.join(" | "));\n'
            'log.length = 0;\n'
            'try { batch(() => { a.set(100); throw new Error("boom"); }); } catch (e) { '
            'console.log(e.message); }\n'
            'console.log(log.join(" | "));\n'
            'log.length = 0;\n'
            'batch(() => { a.set(100); });\n'
            'console.log(log.length);\n',
  'hint': 'В set: if (batchDepth) subs.forEach(e => pending.add(e)) else запуск. В batch: ++depth, '
          'try fn finally { --depth === 0 → flush pending }.',
  'expected': ['abc=1,2,3 | abc=10,2,3 | abc=10,20,3',
               'abc=1,2,4 done',
               'inner done 0',
               'abc=5,6,7',
               'boom',
               'abc=100,6,7',
               '0']},
 {'id': 'j28-untracked',
  'mode': 'js',
  'title': 'peek и untracked',
  'statement': 'Ядро (signal, effect) уже есть; у сигнала есть peek() (чтение без подписки). '
               'Напишите untracked(fn): выполняет fn, и все чтения сигналов внутри не создают '
               'зависимостей текущего эффекта; результат fn возвращается. Затем напишите '
               'on(source, cb): возвращает функцию для effect: при запуске читает source() '
               '(подписка) и вызывает cb(значение, предыдущее) без подписки на то, что читает cb '
               '(внутри — untracked); при первом запуске предыдущее значение — undefined.',
  'starter': '// Готовое ядро (не изменяйте): сигнал, эффект и вычисляемое значение с '
             'автоотслеживанием\n'
             'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.update = (fn) => read.set(fn(value));\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    cleanup: undefined,\n'
             '    active: true,\n'
             '    run() {\n'
             '      if (!e.active) return;\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '    stop() { e.active = false; for (const d of e.deps) d.delete(e); e.deps.clear(); '
             '},\n'
             '  };\n'
             '  e.run();\n'
             '  return e.stop;\n'
             '}\n'
             'function untracked(fn) {\n'
             '}\n'
             'function on(source, cb) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = signal(1), b = signal(100);\n'
            'const log = [];\n'
            'effect(() => log.push(`a=${a()} b=${untracked(() => b())}`));\n'
            'a.set(2); b.set(200); a.set(3);\n'
            'console.log(log.join(" | "));\n'
            'console.log(untracked(() => 42));\n'
            'const x = signal("x"), y = signal("y");\n'
            'const l2 = [];\n'
            'effect(on(x, (v, p) => l2.push(`${p}->${v} y=${y()}`)));\n'
            'x.set("x2"); y.set("y2"); x.set("x3");\n'
            'console.log(l2.join(" | "));\n',
  'hint': 'untracked временно устанавливает current = null и восстанавливает в finally.',
  'expected': ['a=1 b=100 | a=2 b=100 | a=3 b=200',
               '42',
               'undefined->x y=y | x->x2 y=y | x2->x3 y=y2']},
 {'id': 'j28-glitch-free',
  'mode': 'js',
  'title': 'Ромб без глитчей',
  'statement': 'Реализуйте signal, computed и effect так, чтобы в ромбовидной зависимости эффект '
               'запускался ровно один раз на изменение источника и видел только согласованные '
               'значения. Схема работы: signal.set помечает всех зависимых (рекурсивно, через '
               'computed) как устаревших и собирает затронутые эффекты; после пометки эффекты '
               'запускаются по одному разу; computed пересчитывается лениво при чтении, только '
               'если помечен. Общий API как обычно: s(), s.set(v), computed(fn)(), effect(fn) '
               '(запуск сразу). Равенство — Object.is: если после пересчёта computed значение не '
               'изменилось, зависимые от него эффекты можно не запускать (но это не обязательно '
               'проверять в тестах, они учитывают только изменения).',
  'starter': 'function signal(value) {\n}\nfunction computed(fn) {\n}\nfunction effect(fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = signal(1);\n'
            'const a = computed(() => s() + 1);\n'
            'const b = computed(() => s() * 10);\n'
            'const log = [];\n'
            'effect(() => log.push(`${a()}+${b()}=${a() + b()}`));\n'
            's.set(2);\n'
            's.set(3);\n'
            'console.log(log.join(" | "));\n'
            'let calls = 0;\n'
            'const base = signal(1);\n'
            'const dbl = computed(() => { calls++; return base() * 2; });\n'
            'const quad = computed(() => dbl() * 2);\n'
            'const out = [];\n'
            'effect(() => out.push(quad() + dbl()));\n'
            'base.set(2);\n'
            'console.log(out.join(","), calls);\n',
  'hint': 'Два прохода: mark (dirty вниз по графу) и затем запуск собранных эффектов; computed '
          'читает источники при пересчёте.',
  'expected': ['2+10=12 | 3+20=23 | 4+30=34', '6,12 2']},
 {'id': 'j28-watch',
  'mode': 'js',
  'title': 'watch: старое и новое значение',
  'statement': 'Ядро (signal, effect) уже есть. Напишите watch(source, cb, opts = {}): source — '
               'функция-геттер (например, () => a() + b()). Следит за значением source: cb(новое, '
               'старое) вызывается при каждом изменении результата source (сравнение Object.is); '
               'если пересчёт дал то же значение — не вызывается. По умолчанию первый запуск '
               'только запоминает значение (cb не вызывается); с opts.immediate === true первый '
               'вызов cb(значение, undefined) происходит сразу. Возвращает функцию stop (в '
               'заготовке effect возвращает stop). Чтения внутри cb не создают зависимостей.',
  'starter': '// Готовое ядро (не изменяйте): сигнал, эффект и вычисляемое значение с '
             'автоотслеживанием\n'
             'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.update = (fn) => read.set(fn(value));\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    cleanup: undefined,\n'
             '    active: true,\n'
             '    run() {\n'
             '      if (!e.active) return;\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '    stop() { e.active = false; for (const d of e.deps) d.delete(e); e.deps.clear(); '
             '},\n'
             '  };\n'
             '  e.run();\n'
             '  return e.stop;\n'
             '}\n'
             'function watch(source, cb, opts = {}) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = signal(1), b = signal(10), other = signal("o");\n'
            'const log = [];\n'
            'const stop = watch(() => a() + b(), (n, o) => log.push(`${o}->${n} '
            'other=${other()}`));\n'
            'a.set(2); b.set(9); a.set(3); b.set(8);\n'
            'other.set("o2");\n'
            'console.log(log.join(" | "));\n'
            'stop();\n'
            'a.set(100);\n'
            'console.log(log.length);\n'
            'const l2 = [];\n'
            'const flag = signal(false);\n'
            'watch(() => flag(), (n, o) => l2.push(`${o}->${n}`), { immediate: true });\n'
            'flag.set(true); flag.set(true);\n'
            'console.log(l2.join(" | "));\n'
            'const parity = signal(1), l3 = [];\n'
            'watch(() => parity() % 2, (n, o) => l3.push(`${o}->${n}`));\n'
            'parity.set(3); parity.set(4); parity.set(6);\n'
            'console.log(l3.join(" | "));\n',
  'hint': 'effect(() => { const v = source(); … сравнить с прошлым и вызвать cb внутри untracked '
          '}).',
  'expected': ['11->12 other=o | 12->11 other=o | 11->12 other=o | 12->11 other=o',
               '4',
               'undefined->false | false->true',
               '1->0']},
 {'id': 'j28-reactive',
  'mode': 'js',
  'title': 'Реактивный объект на Proxy',
  'statement': 'Напишите reactive(obj) и effect(fn). reactive возвращает Proxy: чтение поля внутри '
               'effect подписывает эффект на пару (объект, ключ); запись поля (set), изменившая '
               'значение (Object.is), перезапускает эффекты, подписанные на этот ключ; вложенные '
               'объекты и массивы оборачиваются лениво при чтении (один и тот же вложенный объект '
               '— один и тот же прокси). Для массивов запись нового индекса или length будит '
               "эффекты, прочитавшие length/индексы (подписка по ключам: 'length' и индексы как "
               'строки). Добавление нового ключа будит эффекты, читавшие его ранее (даже если '
               'тогда он был undefined). effect запускает fn сразу и при уведомлениях; зависимости '
               'пересобираются на каждом запуске.',
  'starter': 'function reactive(obj) {\n}\nfunction effect(fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const state = reactive({ count: 0, user: { name: "A" }, list: [1, 2] });\n'
            'const log = [];\n'
            'effect(() => log.push(`count=${state.count}`));\n'
            'effect(() => log.push(`name=${state.user.name}`));\n'
            'effect(() => log.push(`len=${state.list.length}`));\n'
            'state.count++;\n'
            'state.count = 1;\n'
            'state.user.name = "B";\n'
            'state.list.push(3);\n'
            'state.extra = 1;\n'
            'console.log(log.join(" | "));\n'
            'log.length = 0;\n'
            'effect(() => log.push(`extra=${state.extra2}`));\n'
            'state.extra2 = 5;\n'
            'console.log(log.join(" | "));\n'
            'console.log(state.user === state.user);\n'
            'const a = reactive({ x: 1 }), b = reactive({ x: 1 });\n'
            'const l2 = [];\n'
            'effect(() => l2.push(a.x));\n'
            'b.x = 2;\n'
            'console.log(l2.join(","));\n',
  'hint': 'WeakMap объект → Map ключ → Set эффектов; в get track + оборачивание вложенных; в set — '
          'trigger.',
  'expected': ['count=0 | name=A | len=2 | count=1 | name=B | len=3',
               'extra=undefined | extra=5',
               'true',
               '1']},
 {'id': 'j28-scope',
  'mode': 'js',
  'title': 'Область эффектов',
  'statement': 'Ядро (signal, effect, возвращающий stop) уже есть. Напишите createScope(): { '
               'run(fn), dispose() }. Все effect, созданные внутри run(fn) (в том числе во '
               'вложенных вызовах), регистрируются в области. dispose() останавливает их все (в '
               'порядке, обратном созданию) и делает область неактивной: после dispose run(fn) '
               "бросает Error('Scope is disposed'). Чтобы эффекты попадали в область, перепишите "
               'effect в заготовке: он должен вызывать зарегистрированный сейчас «collector» '
               '(глобальная переменная currentScope).',
  'starter': '// Готовое ядро (не изменяйте): сигнал, эффект и вычисляемое значение с '
             'автоотслеживанием\n'
             'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.update = (fn) => read.set(fn(value));\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    cleanup: undefined,\n'
             '    active: true,\n'
             '    run() {\n'
             '      if (!e.active) return;\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '    stop() { e.active = false; for (const d of e.deps) d.delete(e); e.deps.clear(); '
             '},\n'
             '  };\n'
             '  e.run();\n'
             '  return e.stop;\n'
             '}\n'
             'let currentScope = null;\n'
             'function createScope() {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const n = signal(0);\n'
            'const log = [];\n'
            'const scope = createScope();\n'
            'scope.run(() => {\n'
            '  effect(() => { log.push("a" + n()); });\n'
            '  const inner = () => effect(() => { log.push("b" + n()); });\n'
            '  inner();\n'
            '});\n'
            'const outside = effect(() => { log.push("out" + n()); });\n'
            'n.set(1);\n'
            'console.log(log.join(" "));\n'
            'scope.dispose();\n'
            'n.set(2);\n'
            'console.log(log.join(" "));\n'
            'try { scope.run(() => {}); } catch (e) { console.log(e.message); }\n'
            'outside();\n'
            'const s2 = createScope();\n'
            'console.log(s2.run(() => 42));\n',
  'hint': 'Оберните effect: после создания, если currentScope — добавьте stop в его список; run '
          'устанавливает currentScope и восстанавливает.',
  'expected': ['a0 b0 out0 a1 b1 out1', 'a0 b0 out0 a1 b1 out1 out2', 'Scope is disposed', '42']},
 {'id': 'j28-scheduler',
  'mode': 'js',
  'title': 'Асинхронный планировщик эффектов',
  'statement': 'Напишите signal(v), effect(fn) и nextTick(). Эффект запускается сразу один раз при '
               'создании; при изменении источников он не запускается синхронно, а ставится в '
               'очередь и выполняется в микрозадаче (queueMicrotask) — один раз, сколько бы '
               'записей ни произошло до этого. nextTick() возвращает промис, который завершается '
               'после выполнения очереди (если очередь пуста — на следующей микрозадаче). Порядок '
               'запуска — в порядке первой постановки в очередь. Зависимости пересобираются на '
               'каждом запуске.',
  'starter': 'function signal(v) {\n}\nfunction effect(fn) {\n}\nfunction nextTick() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = signal(1), b = signal(2);\n'
            'const log = [];\n'
            'effect(() => log.push(`a+b=${a() + b()}`));\n'
            'effect(() => log.push(`b=${b()}`));\n'
            'a.set(10); b.set(20); a.set(11);\n'
            'console.log(log.join(" | "));\n'
            'await nextTick();\n'
            'console.log(log.join(" | "));\n'
            'b.set(21);\n'
            'await nextTick();\n'
            'console.log(log.length, log[log.length - 1]);\n'
            'await nextTick();\n'
            'console.log(log.length);\n',
  'hint': 'Set очереди + флаг scheduled; в микрозадаче очистить очередь и запустить эффекты.',
  'expected': ['a+b=3 | b=2', 'a+b=3 | b=2 | a+b=31 | b=20', '6 b=21', '6']},
 {'id': 'j28-resource',
  'mode': 'js',
  'title': 'Ресурс с защитой от гонок',
  'statement': 'Ядро (signal, effect) уже есть. Напишите createResource(source, fetcher): source — '
               'геттер параметра (читает сигналы), fetcher(param) — async. Возвращает объект r: '
               "r.state() — сигнал-геттер состояния 'loading' | 'ready' | 'error' (в начале — "
               "'loading'); r.value() — последнее успешное значение (до него undefined); r.error() "
               '— последняя ошибка или undefined. При каждом изменении параметра (эффект над '
               "source) запускается новый запрос и состояние становится 'loading'. Ответ "
               'учитывается только от последнего запроса: устаревшие (по номеру запуска) '
               'игнорируются полностью, в том числе их ошибки. После успеха error() = undefined; '
               'после ошибки value() остаётся прежним.',
  'starter': '// Готовое ядро (не изменяйте): сигнал, эффект и вычисляемое значение с '
             'автоотслеживанием\n'
             'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.update = (fn) => read.set(fn(value));\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    cleanup: undefined,\n'
             '    active: true,\n'
             '    run() {\n'
             '      if (!e.active) return;\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '    stop() { e.active = false; for (const d of e.deps) d.delete(e); e.deps.clear(); '
             '},\n'
             '  };\n'
             '  e.run();\n'
             '  return e.stop;\n'
             '}\n'
             'function createResource(source, fetcher) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const id = signal(1);\n'
            'const delays = { 1: 30, 2: 5, 3: 10, 4: 5 };\n'
            'const r = createResource(() => id(), async (p) => {\n'
            '  await new Promise((res) => setTimeout(res, delays[p]));\n'
            '  if (p === 4) throw new Error("fail " + p);\n'
            '  return "user" + p;\n'
            '});\n'
            'const log = [];\n'
            'effect(() => log.push(`${r.state()}:${r.value()}:${r.error()?.message}`));\n'
            'id.set(2);\n'
            'await new Promise((res) => setTimeout(res, 60));\n'
            'console.log(log.join(" | "));\n'
            'log.length = 0;\n'
            'id.set(3);\n'
            'await new Promise((res) => setTimeout(res, 30));\n'
            'id.set(4);\n'
            'await new Promise((res) => setTimeout(res, 30));\n'
            'console.log(log.join(" | "));\n'
            'log.length = 0;\n'
            'id.set(3); id.set(1);\n'
            'await new Promise((res) => setTimeout(res, 60));\n'
            'console.log(log.join(" | "), r.value());\n',
  'hint': 'Счётчик запросов id; после await сравните id с последним; сигналы state, value, error.',
  'expected': ['loading:undefined:undefined | loading:user2:undefined | ready:user2:undefined',
               'loading:user2:undefined | loading:user3:undefined | ready:user3:undefined | '
               'loading:user3:undefined | loading:user3:fail 4 | error:user3:fail 4',
               'loading:user3:fail 4 | loading:user1:fail 4 | loading:user1:undefined | '
               'ready:user1:undefined user1']},
 {'id': 'j28-effect-errors',
  'mode': 'js',
  'title': 'Ошибки в эффектах',
  'statement': 'Ядро (signal) уже есть в виде простейшей версии (без effect). Напишите effect(fn, '
               '{ onError }): запускает fn сразу и при изменении источников. Если fn бросила '
               'исключение, оно не должно прерывать запись сигнала и остальные эффекты: исключение '
               "передаётся в onError(error) (если onError не задан — console.log('effect error: ' "
               '+ message)), а эффект остаётся подписанным на то, что успел прочитать до ошибки. '
               'Запись сигнала (set) должна запускать все подписанные эффекты, даже если один из '
               'них бросает.',
  'starter': 'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  return read;\n'
             '}\n'
             'function effect(fn, opts = {}) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const n = signal(0);\n'
            'const log = [];\n'
            'effect(() => { log.push("A" + n()); if (n() === 1) throw new Error("A broke"); }, { '
            'onError: (e) => log.push("err:" + e.message) });\n'
            'effect(() => log.push("B" + n()));\n'
            'effect(() => { if (n() === 2) throw new Error("C broke"); log.push("C" + n()); });\n'
            'n.set(1); n.set(2); n.set(3);\n'
            'console.log(log.join(" | "));\n',
  'hint': 'В run(): try { fn() } catch (e) { report(e) } finally { current = prev }.',
  'expected': ['effect error: C broke',
               'A0 | B0 | C0 | A1 | err:A broke | B1 | C1 | A2 | B2 | A3 | B3 | C3']},
 {'id': 'j28-loop-guard',
  'mode': 'js',
  'title': 'Предохранитель от бесконечных циклов',
  'statement': 'Простейшие signal/effect уже есть в заготовке (перезапуск эффекта при записи; '
               'запись во время работы эффекта запускает перезапуск немедленно). Доработайте так, '
               'чтобы эффект, который в процессе своей работы пишет в сигнал, который сам читает, '
               'не уходил в бесконечность: повторные синхронные перезапуски одного и того же '
               'эффекта внутри одной цепочки считаются, и при превышении 100 бросается '
               "Error('Infinite effect loop detected'). Счётчик сбрасывается, когда самый внешний "
               'запуск эффекта завершён. Обычные запуски по одному разу без цикла работают как '
               'прежде.',
  'starter': 'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    run() {\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '  };\n'
             '  e.run();\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const n = signal(0);\n'
            'let runs = 0;\n'
            'effect(() => { runs++; if (n() < 50) n.set(n() + 1); });\n'
            'console.log(n(), runs);\n'
            'const m = signal(0);\n'
            'let runs2 = 0;\n'
            'try { effect(() => { runs2++; m.set(m() + 1); }); } catch (e) { '
            'console.log(e.message, runs2 > 50 && runs2 <= 102); }\n'
            'const a = signal(1);\n'
            'let runs3 = 0;\n'
            'effect(() => { a(); runs3++; });\n'
            'a.set(2); a.set(3);\n'
            'console.log(runs3);\n',
  'hint': 'В e.run(): e.depth++ с проверкой > 100; в finally depth--.',
  'expected': ['50 51', 'Infinite effect loop detected true', '3']},
 {'id': 'j28-digest',
  'mode': 'js',
  'title': 'Dirty checking (digest-цикл AngularJS)',
  'statement': 'Напишите createScope(): { watch(getter, listener), digest() }. watch регистрирует '
               'пару: getter() вычисляется при дайджесте, и если значение изменилось по сравнению '
               'с прошлым (Object.is; первый раз — всегда изменилось, прошлое — undefined-маркер), '
               'вызывается listener(новое, старое). digest() повторяет полный проход по всем '
               'наблюдателям, пока за проход не изменится ничего (грязная проверка), но не более '
               "10 проходов: если на 10-м проходе всё ещё есть изменения — бросить Error('10 "
               "digest iterations reached'). Возвращает число выполненных проходов (последний, "
               '«чистый», тоже считается).',
  'starter': 'function createScope() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = createScope();\n'
            'const model = { a: 1, b: 0 };\n'
            'const log = [];\n'
            's.watch(() => model.a, (n, o) => { log.push(`a:${o}->${n}`); model.b = n * 2; });\n'
            's.watch(() => model.b, (n, o) => log.push(`b:${o}->${n}`));\n'
            'console.log(s.digest(), log.join(" "));\n'
            'console.log(s.digest(), log.length);\n'
            'model.a = 5;\n'
            'console.log(s.digest(), log.join(" "));\n'
            'const loop = createScope();\n'
            'let k = 0;\n'
            'loop.watch(() => k, () => { k++; });\n'
            'try { loop.digest(); } catch (e) { console.log(e.message, k); }\n',
  'hint': 'Цикл do { dirty = false; for каждого watcher … } while (dirty) со счётчиком итераций.',
  'expected': ['2 a:undefined->1 b:undefined->2',
               '1 2',
               '2 a:undefined->1 b:undefined->2 a:1->5 b:2->10',
               '10 digest iterations reached 10']},
 {'id': 'j28-selector',
  'mode': 'js',
  'title': 'Мемоизированный селектор',
  'statement': 'Напишите createSelector(inputSelectors, combiner): возвращает функцию (state) → '
               'результат. Входные селекторы вызываются на каждый вызов (с state); если все их '
               'результаты равны (===) результатам предыдущего вызова — возвращается прежний '
               'результат без вызова combiner; иначе combiner(...результаты) вызывается и его '
               'результат запоминается. У возвращённой функции есть свойство recomputations — '
               'число вызовов combiner, и метод resetRecomputations(). Первый вызов всегда считает '
               'combiner.',
  'starter': 'function createSelector(inputSelectors, combiner) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const getItems = (s) => s.items, getFilter = (s) => s.filter;\n'
            'const visible = createSelector([getItems, getFilter], (items, f) => items.filter((x) '
            '=> x.includes(f)));\n'
            'const items = ["apple", "banana", "avocado"];\n'
            'const s1 = { items, filter: "a", other: 1 };\n'
            'const r1 = visible(s1);\n'
            'const r2 = visible({ ...s1, other: 2 });\n'
            'console.log(r1 === r2, visible.recomputations);\n'
            'const r3 = visible({ items, filter: "av" });\n'
            'console.log(JSON.stringify(r3), visible.recomputations);\n'
            'const r4 = visible({ items: [...items], filter: "av" });\n'
            'console.log(r3 === r4, visible.recomputations);\n'
            'visible.resetRecomputations();\n'
            'console.log(visible.recomputations);\n'
            'const sum = createSelector([(s) => s.a, (s) => s.b], (a, b) => a + b);\n'
            'console.log(sum({ a: 1, b: 2 }), sum({ a: 1, b: 2 }), sum.recomputations, sum({ a: 2, '
            'b: 2 }), sum.recomputations);\n',
  'hint': 'Храните lastArgs и lastResult; сравнение поэлементное.',
  'expected': ['true 1', '["avocado"] 2', 'false 3', '0', '3 3 1 4 2']},
 {'id': 'j28-observable',
  'mode': 'js',
  'title': 'Observable и операторы',
  'statement': 'Напишите Observable (класс): конструктор принимает функцию subscribeFn(observer), '
               'observer = { next, error, complete }; она может вернуть функцию отписки. Метод '
               'subscribe(observerOrNext) принимает объект или функцию next и возвращает { '
               'unsubscribe() } (после неё next/complete/error не вызываются, функция отписки из '
               'subscribeFn вызывается один раз). После complete или error дальнейшие сообщения '
               'игнорируются, отписка вызывается автоматически. Методы-операторы возвращают новые '
               'Observable: map(fn), filter(pred), take(n) (после n значений — complete и отписка '
               'от источника). Статический of(...values) — выдаёт значения синхронно и завершает.',
  'starter': 'class Observable {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'Observable.of(1, 2, 3, 4, 5).map((x) => x * 10).filter((x) => x > '
            '10).take(3).subscribe({ next: (v) => log.push("n" + v), complete: () => '
            'log.push("done") });\n'
            'console.log(log.join(" "));\n'
            'let cleaned = 0;\n'
            'const src = new Observable((o) => { let i = 0; const t = setInterval(() => '
            'o.next(++i), 1); return () => { clearInterval(t); cleaned++; }; });\n'
            'const got = [];\n'
            'const sub = src.subscribe((v) => got.push(v));\n'
            'await new Promise((r) => setTimeout(r, 30));\n'
            'sub.unsubscribe(); sub.unsubscribe();\n'
            'const n = got.length;\n'
            'await new Promise((r) => setTimeout(r, 10));\n'
            'console.log(n > 0, got.length === n, cleaned);\n'
            'const l2 = [];\n'
            'src.take(2).subscribe({ next: (v) => l2.push(v), complete: () => l2.push("c") });\n'
            'await new Promise((r) => setTimeout(r, 30));\n'
            'console.log(l2.join(","), cleaned);\n'
            'const l3 = [];\n'
            'new Observable((o) => { o.next(1); o.error(new Error("x")); o.next(2); o.complete(); '
            '}).subscribe({ next: (v) => l3.push(v), error: (e) => l3.push("E:" + e.message), '
            'complete: () => l3.push("C") });\n'
            'console.log(l3.join(" "));\n',
  'hint': 'Внутренний Subscriber с флагом closed; операторы оборачивают источник, передавая дальше '
          'значения.',
  'expected': ['n20 n30 n40 done', 'true true 1', '1,2,c 2', '1 E:x']},
 {'id': 'j28-emitter',
  'mode': 'js',
  'title': 'Эмиттер событий',
  'statement': 'Напишите createEmitter(): { on, off, once, emit }. on(event, fn) подписывает '
               '(возвращает функцию отписки), off(event, fn) отписывает (если подписок на fn '
               'несколько — только первую), once(event, fn) — подписка на одно срабатывание. '
               'emit(event, ...args) вызывает подписчиков в порядке подписки с аргументами и '
               "возвращает true, если был хотя бы один подписчик. Событие '*' получает все "
               'события: fn(eventName, ...args), после обычных подписчиков. Исключение подписчика '
               'пробрасывается, остальные в этом emit не вызываются. Подписки и отписки во время '
               'emit действуют со следующего emit.',
  'starter': 'function createEmitter() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const e = createEmitter();\n'
            'const log = [];\n'
            'const h = (x) => log.push("h:" + x);\n'
            'const off = e.on("a", h);\n'
            'e.on("a", (x) => { log.push("second:" + x); e.on("a", () => log.push("late")); });\n'
            'e.once("a", (x) => log.push("once:" + x));\n'
            'e.on("*", (name, ...args) => log.push(`*:${name}:${args.join("/")}`));\n'
            'console.log(e.emit("a", 1), log.join(" "));\n'
            'log.length = 0;\n'
            'console.log(e.emit("a", 2), log.join(" "));\n'
            'log.length = 0; off();\n'
            'console.log(e.emit("a", 3), log.join(" "));\n'
            'log.length = 0;\n'
            'console.log(e.emit("none", "x", "y"), log.join(" "));\n'
            'e.off("a", h); e.off("zzz", h);\n'
            'const e2 = createEmitter();\n'
            'e2.on("x", () => { throw new Error("bad"); }); e2.on("x", () => console.log("not '
            'reached"));\n'
            'try { e2.emit("x"); } catch (err) { console.log(err.message); }\n'
            'console.log(createEmitter().emit("q"));\n',
  'hint': 'Map событие → массив обработчиков; в emit работайте с копией массива.',
  'expected': ['true h:1 second:1 once:1 *:a:1',
               'true h:2 second:2 late *:a:2',
               'true second:3 late late *:a:3',
               'true *:none:x/y',
               'bad',
               'false']},
 {'id': 'j28-history',
  'mode': 'js',
  'title': 'Undo/redo для сигнала',
  'statement': 'Напишите createHistory(initial, limit = 100): { value, set, undo, redo, canUndo, '
               'canRedo }. value() — текущее значение; set(v) — записывает, если '
               '!Object.is(текущее, v): прошлое значение уходит в стек undo, стек redo очищается; '
               'длина undo ограничена limit (самые старые удаляются). undo() возвращает предыдущее '
               'значение (или undefined, если нечего отменять), перенося текущее в redo; redo() — '
               'наоборот. canUndo()/canRedo() — булевы.',
  'starter': 'function createHistory(initial, limit = 100) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const h = createHistory("a", 3);\n'
            'h.set("b"); h.set("c"); h.set("c");\n'
            'console.log(h.value(), h.canUndo(), h.canRedo());\n'
            'console.log(h.undo(), h.undo(), h.undo(), h.value(), h.canUndo(), h.canRedo());\n'
            'console.log(h.redo(), h.value());\n'
            'h.set("x");\n'
            'console.log(h.canRedo(), h.redo(), h.value());\n'
            'h.set("y"); h.set("z"); h.set("w");\n'
            'const seen = [];\n'
            'while (h.canUndo()) seen.push(h.undo());\n'
            'console.log(seen.join(","), h.value());\n'
            'console.log(createHistory(1).undo());\n',
  'hint': 'Три переменные: past[], present, future[].',
  'expected': ['c true false',
               'b a undefined a false true',
               'b b',
               'false undefined x',
               'z,y,x x',
               'undefined']},
 {'id': 'j28-debounce',
  'mode': 'js',
  'title': 'debounce с внедряемым планировщиком',
  'statement': 'Напишите debounce(fn, ms, timers): timers = { setTimeout, clearTimeout } '
               '(внедряются для тестов). Возвращает функцию d(...args): каждый вызов сбрасывает '
               'ожидание; fn вызывается с последними аргументами через ms после последнего вызова. '
               'У d есть cancel() (отменить ожидание) и flush() (если есть отложенный вызов — '
               'выполнить его немедленно и вернуть результат fn, иначе undefined). Затем '
               'throttle(fn, ms, now): первый вызов выполняется сразу; последующие в течение ms '
               'после последнего выполнения игнорируются (now() — текущее время).',
  'starter': 'function debounce(fn, ms, timers) {\n}\nfunction throttle(fn, ms, now) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const queue = [];\n'
            'let t = 0;\n'
            'const timers = {\n'
            '  setTimeout(f, ms) { const id = queue.length + 1; queue.push({ id, f, at: t + ms }); '
            'return id; },\n'
            '  clearTimeout(id) { const i = queue.findIndex((x) => x.id === id); if (i >= 0) '
            'queue.splice(i, 1); },\n'
            '};\n'
            'const advance = (ms) => { t += ms; for (const x of queue.filter((q) => q.at <= '
            't).sort((a, b) => a.at - b.at)) { queue.splice(queue.indexOf(x), 1); x.f(); } };\n'
            'const log = [];\n'
            'const d = debounce((x) => { log.push(x); return "r" + x; }, 100, timers);\n'
            'd(1); advance(50); d(2); advance(50); d(3); advance(99);\n'
            'console.log(log.join(","));\n'
            'advance(1);\n'
            'console.log(log.join(","));\n'
            'd(4); d.cancel(); advance(500);\n'
            'console.log(log.join(","));\n'
            'd(5);\n'
            'console.log(d.flush(), log.join(","), d.flush());\n'
            'advance(500);\n'
            'console.log(log.join(","));\n'
            'let now = 0;\n'
            'const l2 = [];\n'
            'const th = throttle((x) => l2.push(x), 100, () => now);\n'
            'th("a"); now = 50; th("b"); now = 100; th("c"); now = 150; th("d"); now = 200; '
            'th("e");\n'
            'console.log(l2.join(","));\n',
  'hint': 'Храните id таймера и последние аргументы; throttle — время последнего запуска.',
  'expected': ['3', '3', 'r5 3,5 undefined', '3,5', 'a,c,e']},
 {'id': 'j28-combine',
  'mode': 'js',
  'title': 'Объединение сигналов',
  'statement': 'Ядро (signal, computed, effect) уже есть. Напишите combine(signals): signals — '
               'объект «имя → сигнал или computed»; возвращает computed-геттер, значение которого '
               '— объект { имя: значение } с теми же ключами (в том же порядке). Результат '
               'пересоздаётся (новый объект) при изменении любого источника, и тот же объект '
               'возвращается при повторном чтении без изменений. Затем напишите mapSignal(source, '
               'fn) — computed, возвращающий fn(source()), и pluck(source, key) — computed '
               'значения source()[key].',
  'starter': '// Готовое ядро (не изменяйте): сигнал, эффект и вычисляемое значение с '
             'автоотслеживанием\n'
             'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.update = (fn) => read.set(fn(value));\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    cleanup: undefined,\n'
             '    active: true,\n'
             '    run() {\n'
             '      if (!e.active) return;\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '    stop() { e.active = false; for (const d of e.deps) d.delete(e); e.deps.clear(); '
             '},\n'
             '  };\n'
             '  e.run();\n'
             '  return e.stop;\n'
             '}\n'
             'function computed(fn) {\n'
             '  let value, dirty = true;\n'
             '  const subs = new Set();\n'
             '  const inner = {\n'
             '    deps: new Set(),\n'
             '    run() {\n'
             '      if (!dirty) { dirty = true; for (const e of [...subs]) e.run(); }\n'
             '    },\n'
             '  };\n'
             '  return () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    if (dirty) {\n'
             '      for (const d of inner.deps) d.delete(inner);\n'
             '      inner.deps.clear();\n'
             '      const prev = current;\n'
             '      current = inner;\n'
             '      try { value = fn(); } finally { current = prev; }\n'
             '      dirty = false;\n'
             '    }\n'
             '    return value;\n'
             '  };\n'
             '}\n'
             '// Готово: computed выше. Допишите:\n'
             'function combine(signals) {\n'
             '}\n'
             'function mapSignal(source, fn) {\n'
             '}\n'
             'function pluck(source, key) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const name = signal("Ann"), age = signal(30);\n'
            'const doubled = computed(() => age() * 2);\n'
            'const all = combine({ name, age, doubled });\n'
            'const o1 = all();\n'
            'console.log(JSON.stringify(o1), all() === o1, Object.keys(o1).join());\n'
            'age.set(31);\n'
            'const o2 = all();\n'
            'console.log(JSON.stringify(o2), o2 !== o1, all() === o2);\n'
            'const log = [];\n'
            'effect(() => log.push(mapSignal(name, (n) => n.toUpperCase())()));\n'
            'name.set("Bo");\n'
            'const pickAge = pluck(all, "age");\n'
            'console.log(log.join(","), pickAge());\n'
            'age.set(40);\n'
            'console.log(pickAge(), pluck(all, "doubled")());\n',
  'hint': 'combine: computed(() => Object.fromEntries(Object.entries(signals).map(([k, s]) => [k, '
          's()])))',
  'expected': ['{"name":"Ann","age":30,"doubled":60} true name,age,doubled',
               '{"name":"Ann","age":31,"doubled":62} true true',
               'ANN,BO 31',
               '40 80']},
 {'id': 'j28-reactive-map',
  'mode': 'js',
  'title': 'Реактивный Map',
  'statement': 'Эффект с автоотслеживанием уже есть: track(target, key) подписывает текущий эффект '
               'на ключ, trigger(target, key) его будит (готовые функции в заготовке). Напишите '
               'class ReactiveMap: get(key) подписывает эффект на этот ключ; has(key) — на ключ '
               '(наличие); set(key, value) — запись: будит эффекты, читавшие этот ключ, если '
               'значение изменилось по Object.is или ключ новый; delete(key) — будит читавших '
               "ключ, если ключ был; size и keys() подписывают на специальный ключ 'iterate', "
               'который будят добавление нового ключа и удаление; clear() будит все ключи, которые '
               "были, и 'iterate'. Запись в другой ключ не должна будить читателей get('x').",
  'starter': 'let active = null;\n'
             'const deps = new Map(); // target → Map(key → Set(effect))\n'
             'function track(target, key) {\n'
             '  if (!active) return;\n'
             '  let m = deps.get(target);\n'
             '  if (!m) deps.set(target, (m = new Map()));\n'
             '  let s = m.get(key);\n'
             '  if (!s) m.set(key, (s = new Set()));\n'
             '  s.add(active);\n'
             '  active.deps.add(s);\n'
             '}\n'
             'function trigger(target, key) {\n'
             '  const s = deps.get(target)?.get(key);\n'
             '  if (s) for (const e of [...s]) e.run();\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    run() {\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = active;\n'
             '      active = e;\n'
             '      try { fn(); } finally { active = prev; }\n'
             '    },\n'
             '  };\n'
             '  e.run();\n'
             '}\n'
             'class ReactiveMap {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const m = new ReactiveMap();\n'
            'const log = [];\n'
            'effect(() => log.push("x=" + m.get("x")));\n'
            'effect(() => log.push("has y=" + m.has("y")));\n'
            'effect(() => log.push("size=" + m.size));\n'
            'effect(() => log.push("keys=" + [...m.keys()].join("")));\n'
            'm.set("x", 1); m.set("x", 1); m.set("y", 2); m.set("x", 2); m.delete("z"); '
            'm.delete("y");\n'
            'console.log(log.join(" | "));\n'
            'log.length = 0;\n'
            'm.clear();\n'
            'console.log(log.join(" | "), m.size);\n',
  'hint': 'Внутри — обычный Map; в методах чтения вызывайте track(this, ключ); в записи — trigger.',
  'expected': ['x=undefined | has y=false | size=0 | keys= | x=1 | size=1 | keys=x | has y=true | '
               'size=2 | keys=xy | x=2 | has y=false | size=1 | keys=x',
               'x=undefined | size=0 | keys= 0']},
 {'id': 'j28-form',
  'mode': 'js',
  'title': 'Состояние формы',
  'statement': 'Ядро (signal, computed, effect) уже есть. Напишите createField(initial, '
               'validators): validators — массив функций v(value) → строка-ошибка или null. '
               'Возвращает объект { value (сигнал), touched (сигнал, false), error (computed: '
               'первая ошибка по порядку валидаторов или null), valid (computed: error() === null) '
               '}. Напишите createForm(fields): fields — объект «имя → поле»; возвращает { values '
               '(computed-объект {имя: значение}), valid (computed: все поля валидны), errors '
               '(computed-объект только с ошибочными полями {имя: ошибка}), submitDisabled '
               '(computed: !valid), touchAll() (ставит touched = true всем) }.',
  'starter': '// Готовое ядро (не изменяйте): сигнал, эффект и вычисляемое значение с '
             'автоотслеживанием\n'
             'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.update = (fn) => read.set(fn(value));\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    cleanup: undefined,\n'
             '    active: true,\n'
             '    run() {\n'
             '      if (!e.active) return;\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '    stop() { e.active = false; for (const d of e.deps) d.delete(e); e.deps.clear(); '
             '},\n'
             '  };\n'
             '  e.run();\n'
             '  return e.stop;\n'
             '}\n'
             'function computed(fn) {\n'
             '  let value, dirty = true;\n'
             '  const subs = new Set();\n'
             '  const inner = {\n'
             '    deps: new Set(),\n'
             '    run() {\n'
             '      if (!dirty) { dirty = true; for (const e of [...subs]) e.run(); }\n'
             '    },\n'
             '  };\n'
             '  return () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    if (dirty) {\n'
             '      for (const d of inner.deps) d.delete(inner);\n'
             '      inner.deps.clear();\n'
             '      const prev = current;\n'
             '      current = inner;\n'
             '      try { value = fn(); } finally { current = prev; }\n'
             '      dirty = false;\n'
             '    }\n'
             '    return value;\n'
             '  };\n'
             '}\n'
             '// Готово: computed выше. Допишите:\n'
             'function createField(initial, validators = []) {\n'
             '}\n'
             'function createForm(fields) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const required = (v) => (v ? null : "required");\n'
            'const minLen = (n) => (v) => (v.length >= n ? null : `min ${n}`);\n'
            'const email = createField("", [required, (v) => (v.includes("@") ? null : "bad '
            'email")]);\n'
            'const pass = createField("", [required, minLen(4)]);\n'
            'const form = createForm({ email, pass });\n'
            'console.log(email.error(), form.valid(), form.submitDisabled(), '
            'JSON.stringify(form.errors()));\n'
            'email.value.set("a@b.c");\n'
            'console.log(email.error(), email.valid(), JSON.stringify(form.errors()));\n'
            'pass.value.set("abc");\n'
            'console.log(pass.error(), JSON.stringify(form.errors()));\n'
            'pass.value.set("abcd");\n'
            'console.log(form.valid(), form.submitDisabled(), JSON.stringify(form.values()), '
            'JSON.stringify(form.errors()));\n'
            'const log = [];\n'
            'effect(() => log.push(form.submitDisabled()));\n'
            'pass.value.set("");\n'
            'pass.value.set("longer");\n'
            'console.log(log.join(","));\n'
            'console.log(email.touched(), form.touchAll(), email.touched(), pass.touched());\n',
  'hint': 'createField собирает signal/computed; createForm — computed над всеми полями.',
  'expected': ['required false true {"email":"required","pass":"required"}',
               'null true {"pass":"required"}',
               'min 4 {"pass":"min 4"}',
               'true false {"email":"a@b.c","pass":"abcd"} {}',
               'false,true,false',
               'false undefined true true']},
 {'id': 'j28-map-array',
  'mode': 'js',
  'title': 'mapArray: кэш по ключам',
  'statement': 'Напишите mapArray(getList, mapFn): getList — геттер массива, mapFn(item, index) → '
               'значение. Возвращает функцию-геттер m(), которая считает массив результатов. '
               'Результаты для каждого элемента-ссылки (по ===) кэшируются между пересчётами: если '
               'элемент остался в массиве (в любом месте), mapFn для него не вызывается заново '
               '(индекс при этом не обновляется), для новых элементов вызывается; для удалённых — '
               'кэш очищается (если элемент вернётся позже, mapFn вызовется снова). Дубликаты '
               'одного и того же элемента — один вызов mapFn на уникальную ссылку (все позиции '
               'получают то же значение). Пересчёт ленивый: m() сам вызывает getList() и '
               'сравнивает с прошлым списком; если массив тот же по ссылке и длине — возвращает '
               'прежний результат.',
  'starter': 'function mapArray(getList, mapFn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = { id: "a" }, b = { id: "b" }, c = { id: "c" };\n'
            'let list = [a, b];\n'
            'let calls = [];\n'
            'const m = mapArray(() => list, (item, i) => { calls.push(item.id + i); return '
            'item.id.toUpperCase(); });\n'
            'console.log(m().join(""), calls.join(","));\n'
            'list = [b, a, c];\n'
            'console.log(m().join(""), calls.join(","));\n'
            'list = [c, c, a];\n'
            'console.log(m().join(""), calls.join(","));\n'
            'list = [b];\n'
            'console.log(m().join(""), calls.join(","));\n'
            'list = [a];\n'
            'console.log(m().join(""), calls.join(","));\n'
            'const same = m(); console.log(m() === same);\n'
            'list = [];\n'
            'console.log(m().length, calls.length);\n',
  'hint': 'Map элемент → результат; на каждый вызов собирайте новый Map только из текущих '
          'элементов.',
  'expected': ['AB a0,b1',
               'BAC a0,b1,c2',
               'CCA a0,b1,c2',
               'B a0,b1,c2,b0',
               'A a0,b1,c2,b0,a0',
               'true',
               '0 5']},
 {'id': 'j28-persisted',
  'mode': 'js',
  'title': 'Сигнал с сохранением',
  'statement': 'Напишите persisted(key, initial, storage): storage — объект с getItem(key) и '
               'setItem(key, value) (как localStorage). Возвращает сигнал-подобный объект s: s() — '
               'значение; s.set(v) — записать (если !Object.is) и сохранить JSON.stringify(v) в '
               'storage; s.subscribe(cb) — ручная подписка (cb(новое, старое), отписка '
               'возвращается). При создании значение читается из storage: если есть и JSON '
               'разбирается — оно; иначе initial (повреждённый JSON — initial, без исключения, и в '
               'storage ничего не пишется до первой записи). Запись undefined удаляет значение: '
               "setItem(key, 'null') и значение сигнала — undefined… нет: undefined сохраняется "
               "как строка 'null', а сам сигнал хранит undefined.",
  'starter': 'function persisted(key, initial, storage) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const store = new Map();\n'
            'const storage = { getItem: (k) => (store.has(k) ? store.get(k) : null), setItem: (k, '
            'v) => store.set(k, v) };\n'
            'const a = persisted("a", 1, storage);\n'
            'console.log(a(), store.size);\n'
            'a.set(2); a.set(2);\n'
            'console.log(a(), store.get("a"));\n'
            'const log = [];\n'
            'a.subscribe((n, o) => log.push(`${o}->${n}`));\n'
            'a.set({ x: [1, 2] });\n'
            'console.log(log.join(), store.get("a"));\n'
            'const b = persisted("a", 99, storage);\n'
            'console.log(JSON.stringify(b()));\n'
            'store.set("bad", "{oops");\n'
            'const c = persisted("bad", "init", storage);\n'
            'console.log(c(), store.get("bad"));\n'
            'c.set("ok");\n'
            'console.log(store.get("bad"));\n'
            'const d = persisted("u", "x", storage);\n'
            'd.set(undefined);\n'
            'console.log(d(), store.get("u"));\n',
  'hint': 'try { JSON.parse(raw) } catch { initial }; подписчики вызывайте после сохранения.',
  'expected': ['1 0',
               '2 2',
               '2->[object Object] {"x":[1,2]}',
               '{"x":[1,2]}',
               'init {oops',
               '"ok"',
               'undefined null']},
 {'id': 'j28-set-in',
  'mode': 'js',
  'title': 'Неизменяемое обновление по пути',
  'statement': 'Напишите setIn(obj, path, value) и updateIn(obj, path, fn). path — массив ключей '
               '(строки и числа). setIn возвращает новый объект/массив с заменённым значением по '
               'пути, при этом все узлы вне пути сохраняют прежние ссылки (структурное '
               'разделение); исходный объект не меняется. Если значение по пути уже равно '
               '(Object.is) новому — вернуть исходный obj без копирования. Отсутствующие '
               'промежуточные узлы создаются: массив, если следующий ключ — число, иначе объект. '
               'Пустой path — вернуть value. updateIn(obj, path, fn) — setIn(obj, path, fn(текущее '
               'значение по пути)).',
  'starter': 'function setIn(obj, path, value) {\n}\nfunction updateIn(obj, path, fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const state = { user: { name: "A", tags: ["x", "y"] }, items: [{ id: 1 }, { id: 2 }], '
            'flag: false };\n'
            'const s1 = setIn(state, ["user", "name"], "B");\n'
            'console.log(JSON.stringify(s1), s1.items === state.items, s1.user.tags === '
            'state.user.tags, s1 !== state, state.user.name);\n'
            'console.log(setIn(state, ["flag"], false) === state);\n'
            'const s2 = setIn(state, ["items", 1, "id"], 20);\n'
            'console.log(JSON.stringify(s2.items), s2.items[0] === state.items[0], '
            'Array.isArray(s2.items));\n'
            'const s3 = setIn({}, ["a", "b", 0, "c"], 1);\n'
            'console.log(JSON.stringify(s3), Array.isArray(s3.a.b));\n'
            'console.log(setIn(state, [], 5));\n'
            'const s4 = updateIn(state, ["user", "tags"], (t) => [...t, "z"]);\n'
            'console.log(JSON.stringify(s4.user.tags), JSON.stringify(state.user.tags));\n'
            'console.log(JSON.stringify(updateIn({ n: 1 }, ["n"], (x) => x + 1)), updateIn(state, '
            '["flag"], (x) => x) === state);\n',
  'hint': 'Рекурсия по path: копируйте только узел на пути (Array.isArray? [...] : {...}).',
  'expected': ['{"user":{"name":"B","tags":["x","y"]},"items":[{"id":1},{"id":2}],"flag":false} '
               'true true true A',
               'true',
               '[{"id":1},{"id":20}] true true',
               '{"a":{"b":[{"c":1}]}} true',
               '5',
               '["x","y","z"] ["x","y"]',
               '{"n":2} true']},
 {'id': 'j28-shallow-equal',
  'mode': 'js',
  'title': 'Поверхностное равенство для сигнала',
  'statement': 'Напишите shallowEqual(a, b): true, если a и b равны по Object.is, либо оба — '
               'непустые… точнее: оба объекта (не null) с одинаковым набором собственных ключей и '
               'значениями, равными по Object.is (порядок ключей не важен); массивы сравниваются '
               'поэлементно (одинаковая длина); объекты и массивы между собой не равны; вложенные '
               'значения сравниваются только по ссылке. Затем напишите signal(initial, { equals }) '
               'c автоотслеживанием: запись, для которой equals(старое, новое) истинно, не будит '
               'подписчиков и не меняет хранимое значение (остаётся прежняя ссылка). Ядро effect '
               'есть в заготовке.',
  'starter': 'let current = null;\n'
             'function shallowEqual(a, b) {\n'
             '}\n'
             'function signal(initial, opts = {}) {\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    run() {\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '  };\n'
             '  e.run();\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (a, b) => console.log(JSON.stringify(a), JSON.stringify(b), shallowEqual(a, '
            'b));\n'
            't(1, 1); t(NaN, NaN); t(0, -0); t({ a: 1, b: 2 }, { b: 2, a: 1 }); t({ a: 1 }, { a: '
            '1, b: undefined }); t({ a: { x: 1 } }, { a: { x: 1 } });\n'
            't([1, 2], [1, 2]); t([1, 2], [1, 2, 3]); t([], {}); t(null, {}); t(null, null); '
            't([1], { 0: 1 });\n'
            'const shared = { x: 1 };\n'
            'console.log(shallowEqual({ a: shared }, { a: shared }));\n'
            'const s = signal({ n: 1 }, { equals: shallowEqual });\n'
            'const first = s();\n'
            'const log = [];\n'
            'effect(() => log.push(JSON.stringify(s())));\n'
            's.set({ n: 1 });\n'
            'console.log(s() === first, log.length);\n'
            's.set({ n: 2 });\n'
            'console.log(log.join(" "));\n'
            'const p = signal(1);\n'
            'effect(() => log.push("p" + p()));\n'
            'p.set(1); p.set(2);\n'
            'console.log(log.slice(2).join(" "));\n',
  'hint': 'signal: read добавляет current в subs; set проверяет equals ?? Object.is.',
  'expected': ['1 1 true',
               'null null true',
               '0 0 false',
               '{"a":1,"b":2} {"b":2,"a":1} true',
               '{"a":1} {"a":1} false',
               '{"a":{"x":1}} {"a":{"x":1}} false',
               '[1,2] [1,2] true',
               '[1,2] [1,2,3] false',
               '[] {} false',
               'null {} false',
               'null null true',
               '[1] {"0":1} false',
               'true',
               'true 1',
               '{"n":1} {"n":2}',
               'p1 p2']},
 {'id': 'j28-reactive-array-fn',
  'mode': 'js',
  'title': 'Производные коллекции: фильтр и сумма',
  'statement': 'Ядро (signal, computed, effect) уже есть. Напишите createTodos(): { items (сигнал '
               'массива { id, title, done }), add(title) (добавляет задачу с id — порядковым '
               'номером с 1, done: false, записью нового массива), toggle(id) (переключает done, '
               'создавая новый массив и новый объект задачи только для изменяемой), remove(id), '
               "filter (сигнал 'all' | 'active' | 'done'), visible (computed отфильтрованный "
               'массив), remaining (computed число невыполненных), allDone (computed: список '
               'непуст и все выполнены) }. Незатронутые задачи сохраняют прежние ссылки на '
               'объекты.',
  'starter': '// Готовое ядро (не изменяйте): сигнал, эффект и вычисляемое значение с '
             'автоотслеживанием\n'
             'let current = null;\n'
             'function signal(value) {\n'
             '  const subs = new Set();\n'
             '  const read = () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    return value;\n'
             '  };\n'
             '  read.peek = () => value;\n'
             '  read.set = (v) => {\n'
             '    if (Object.is(v, value)) return;\n'
             '    value = v;\n'
             '    for (const e of [...subs]) e.run();\n'
             '  };\n'
             '  read.update = (fn) => read.set(fn(value));\n'
             '  return read;\n'
             '}\n'
             'function effect(fn) {\n'
             '  const e = {\n'
             '    deps: new Set(),\n'
             '    cleanup: undefined,\n'
             '    active: true,\n'
             '    run() {\n'
             '      if (!e.active) return;\n'
             '      for (const d of e.deps) d.delete(e);\n'
             '      e.deps.clear();\n'
             '      const prev = current;\n'
             '      current = e;\n'
             '      try { fn(); } finally { current = prev; }\n'
             '    },\n'
             '    stop() { e.active = false; for (const d of e.deps) d.delete(e); e.deps.clear(); '
             '},\n'
             '  };\n'
             '  e.run();\n'
             '  return e.stop;\n'
             '}\n'
             'function computed(fn) {\n'
             '  let value, dirty = true;\n'
             '  const subs = new Set();\n'
             '  const inner = {\n'
             '    deps: new Set(),\n'
             '    run() {\n'
             '      if (!dirty) { dirty = true; for (const e of [...subs]) e.run(); }\n'
             '    },\n'
             '  };\n'
             '  return () => {\n'
             '    if (current) { subs.add(current); current.deps.add(subs); }\n'
             '    if (dirty) {\n'
             '      for (const d of inner.deps) d.delete(inner);\n'
             '      inner.deps.clear();\n'
             '      const prev = current;\n'
             '      current = inner;\n'
             '      try { value = fn(); } finally { current = prev; }\n'
             '      dirty = false;\n'
             '    }\n'
             '    return value;\n'
             '  };\n'
             '}\n'
             '// Готово: computed выше. Допишите:\n'
             'function createTodos() {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = createTodos();\n'
            'const log = [];\n'
            'effect(() => log.push(`${t.remaining()}/${t.items().length} all=${t.allDone()}`));\n'
            't.add("a"); t.add("b"); t.add("c");\n'
            'const before = t.items();\n'
            't.toggle(2);\n'
            'const after = t.items();\n'
            'console.log(after[0] === before[0], after[1] === before[1], after[2] === before[2], '
            'JSON.stringify(after.map((x) => x.done)));\n'
            'console.log(JSON.stringify(t.visible().map((x) => x.title)));\n'
            't.filter.set("done");\n'
            'console.log(JSON.stringify(t.visible().map((x) => x.title)));\n'
            't.filter.set("active");\n'
            'console.log(JSON.stringify(t.visible().map((x) => x.title)));\n'
            't.toggle(1); t.toggle(3);\n'
            'console.log(t.allDone(), t.remaining());\n'
            't.remove(2);\n'
            'console.log(JSON.stringify(t.items().map((x) => x.id)), t.allDone());\n'
            't.add("d");\n'
            'console.log(JSON.stringify(t.items().map((x) => x.id)), log.join(" | "));\n',
  'hint': 'Все изменения — через items.set(новый массив); computed читают items() и filter().',
  'expected': ['true false true [false,true,false]',
               '["a","b","c"]',
               '["b"]',
               '["a","c"]',
               'true 0',
               '[1,3] true',
               '[1,3,4] 0/0 all=false | 1/1 all=false | 1/1 all=false | 1/1 all=false | 2/2 '
               'all=false | 2/2 all=false | 2/2 all=false | 3/3 all=false | 3/3 all=false | 3/3 '
               'all=false | 2/3 all=false | 2/3 all=false | 2/3 all=false | 1/3 all=false | 1/3 '
               'all=false | 1/3 all=false | 0/3 all=false | 0/3 all=false | 0/3 all=true | 0/2 '
               'all=true | 0/2 all=true | 0/2 all=true | 1/3 all=true | 1/3 all=true | 1/3 '
               'all=false']}]}
