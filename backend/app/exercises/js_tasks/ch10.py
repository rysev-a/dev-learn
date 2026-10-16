"""Задачи книги «Современный Frontend», глава 10 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {10: [{'id': 'j10-promisify',
       'mode': 'js',
       'title': 'promisify: из колбэков в промисы',
       'statement': 'Напишите функцию promisify(fn): fn принимает аргументы и последним — колбэк (err, '
                    'result); promisify возвращает функцию, которая принимает те же аргументы без колбэка и '
                    'возвращает промис (отклонённый ошибкой err или выполненный result). this сохраняется.',
       'starter': 'function promisify(fn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const add = (a, b, cb) => setTimeout(() => cb(null, a + b), 5);\n'
                 'const fail = (cb) => setTimeout(() => cb(new Error("не вышло")), 5);\n'
                 'console.log(await promisify(add)(2, 3));\n'
                 'try { await promisify(fail)(); } catch (e) { console.log(e.message); }\n'
                 'const obj = { k: 10, get(cb) { setTimeout(() => cb(null, this.k), 1); } };\n'
                 'obj.p = promisify(obj.get);\n'
                 'console.log(await obj.p());\n'
                 'console.log(promisify(add)(1, 1) instanceof Promise);\n',
       'hint': 'new Promise((resolve, reject) => fn(...args, (err, r) => …))',
       'expected': ['5', 'не вышло', '10', 'true']},
      {'id': 'j10-sequence',
       'mode': 'js',
       'title': 'Последовательное выполнение',
       'statement': 'Напишите функцию series(tasks): tasks — массив функций, возвращающих промис (или '
                    'значение); запускает их строго по очереди (следующую — после завершения предыдущей) и '
                    'возвращает промис с массивом результатов; при первой ошибке остальные не запускаются, а '
                    'промис отклоняется этой ошибкой.',
       'starter': 'async function series(tasks) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const log = [];\n'
                 'const job = (name, ms, fail) => async () => { log.push("start " + name); await sleep(ms); '
                 'log.push("end " + name); if (fail) throw new Error(name); return name.toUpperCase(); };\n'
                 'console.log(JSON.stringify(await series([job("a", 30), job("b", 5), () => 7])), log.join(" '
                 '| "));\n'
                 'log.length = 0;\n'
                 'try { await series([job("x", 5), job("y", 5, true), job("z", 5)]); } catch (e) { '
                 'console.log(e.message, log.join(" | ")); }\n'
                 'console.log(JSON.stringify(await series([])));\n',
       'hint': 'for (const t of tasks) out.push(await t());',
       'expected': ['["A","B",7] start a | end a | start b | end b',
                    'y start x | end x | start y | end y',
                    '[]']},
      {'id': 'j10-parallel-limit',
       'mode': 'js',
       'title': 'Параллельность с ограничением',
       'statement': 'Напишите функцию mapLimit(items, limit, fn): применяет асинхронную fn(item, index) ко '
                    'всем элементам, одновременно выполняется не больше limit вызовов; возвращает промис с '
                    'результатами в исходном порядке; при ошибке — отклоняется первой ошибкой (новые вызовы '
                    'после неё не запускаются).',
       'starter': 'function mapLimit(items, limit, fn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'let running = 0, peak = 0, started = 0;\n'
                 'const work = async (x, i) => { started++; running++; peak = Math.max(peak, running); await '
                 'sleep(10 + (x % 3) * 5); running--; return x * 2; };\n'
                 'const r = await mapLimit([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3, work);\n'
                 'console.log(JSON.stringify(r), peak);\n'
                 'console.log(JSON.stringify(await mapLimit([], 3, work)));\n'
                 'console.log(JSON.stringify(await mapLimit([5, 6], 10, work)), peak);\n'
                 'started = 0;\n'
                 'try { await mapLimit([1, 2, 3, 4, 5, 6], 2, async (x) => { await sleep(5); if (x === 2) '
                 'throw new Error("плохо " + x); return x; }); } catch (e) { console.log(e.message); }\n'
                 'console.log(JSON.stringify(await mapLimit([3, 1, 2], 1, async (x) => { await sleep(x * 3); '
                 'return x; })));\n',
       'hint': 'Несколько воркеров в цикле берут следующий индекс из общего счётчика; результат пишется в '
               'results[i].',
       'expected': ['[2,4,6,8,10,12,14,16,18,20] 3', '[]', '[10,12] 3', 'плохо 2', '[3,1,2]']},
      {'id': 'j10-all-settled',
       'mode': 'js',
       'title': 'Своя allSettled',
       'statement': 'Напишите функцию settleAll(list): принимает массив значений и промисов; возвращает '
                    'промис с массивом { status: "fulfilled", value } или { status: "rejected", reason } в '
                    'исходном порядке; сам никогда не отклоняется. Promise.allSettled использовать нельзя.',
       'starter': 'function settleAll(list) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const r = await settleAll([sleep(20, "a"), 5, Promise.reject(new Error("b")), sleep(5, '
                 '"c")]);\n'
                 'console.log(r.map((x) => x.status + ":" + (x.value ?? x.reason.message)).join(" "));\n'
                 'console.log(JSON.stringify(await settleAll([])));\n'
                 'console.log(__count("allSe" + "ttled"));\n',
       'hint': 'Каждый промис превратите в «всегда успешный» через then(onOk, onFail), затем Promise.all.',
       'expected': ['fulfilled:a fulfilled:5 rejected:b fulfilled:c', '[]', '0']},
      {'id': 'j10-any',
       'mode': 'js',
       'title': 'Своя Promise.any',
       'statement': 'Напишите функцию firstFulfilled(list): возвращает промис, выполненный значением первого '
                    'успешного из list (значения и промисы); если все отклонены (или массив пуст) — '
                    'отклоняется AggregateError с массивом причин в исходном порядке и сообщением «Все '
                    'отклонены». Promise.any использовать нельзя.',
       'starter': 'function firstFulfilled(list) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const fail = (m, ms) => new Promise((_, r) => setTimeout(() => r(new Error(m)), ms));\n'
                 'console.log(await firstFulfilled([fail("a", 5), sleep(30, "медленный"), sleep(10, '
                 '"быстрый")]));\n'
                 'console.log(await firstFulfilled([1, fail("x", 1)]));\n'
                 'try { await firstFulfilled([fail("a", 15), fail("b", 5)]); } catch (e) { '
                 'console.log(e.name, e.message, e.errors.map((x) => x.message).join()); }\n'
                 'try { await firstFulfilled([]); } catch (e) { console.log(e.name, e.errors.length); }\n'
                 'console.log(__count("Promi" + "se.any"));\n',
       'hint': 'Промис-обёртка: resolve — для первого успеха, а отказы копятся по индексу.',
       'expected': ['быстрый', '1', 'AggregateError Все отклонены a,b', 'AggregateError 0', '0']},
      {'id': 'j10-race',
       'mode': 'js',
       'title': 'Своя Promise.race',
       'statement': 'Напишите функцию firstSettled(list): промис, который завершается так же, как первый '
                    'завершившийся промис из list (значением или ошибкой); значения без промиса — '
                    'немедленно. Для пустого массива промис остаётся в ожидании. Promise.race использовать '
                    'нельзя.',
       'starter': 'function firstSettled(list) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const fail = (m, ms) => new Promise((_, r) => setTimeout(() => r(new Error(m)), ms));\n'
                 'console.log(await firstSettled([sleep(30, "медленный"), sleep(5, "быстрый")]));\n'
                 'try { await firstSettled([sleep(30, "x"), fail("упал первым", 5)]); } catch (e) { '
                 'console.log(e.message); }\n'
                 'console.log(await firstSettled([sleep(20, "x"), 42]));\n'
                 'let settled = false;\n'
                 'firstSettled([]).then(() => { settled = true; }, () => { settled = true; });\n'
                 'await sleep(30);\n'
                 'console.log(settled);\n'
                 'console.log(__count("Promis" + "e.race"));\n',
       'hint': 'Подпишите resolve и reject на каждый промис: сработает тот, кто первый.',
       'expected': ['быстрый', 'упал первым', '42', 'false', '0']},
      {'id': 'j10-poll',
       'mode': 'js',
       'title': 'Опрос до готовности',
       'statement': 'Напишите функцию pollUntil(check, { interval, maxAttempts }): check() — асинхронная '
                    'функция, возвращающая значение; повторяйте вызов каждые interval мс, пока результат не '
                    'станет истинным — вернуть его; после maxAttempts неудачных проверок отклониться '
                    'Error("не дождались после N попыток"). Между проверками ждите interval мс (после '
                    'последней паузы нет).',
       'starter': 'async function pollUntil(check, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const t0 = Date.now();\n'
                 'console.log(await pollUntil(async (n) => (n >= 3 ? "готово на " + n : null), { interval: '
                 '10, maxAttempts: 5 }), Date.now() - t0 >= 18);\n'
                 'console.log(await pollUntil(() => "сразу", { interval: 1000, maxAttempts: 2 }));\n'
                 'const t1 = Date.now();\n'
                 'try { await pollUntil(async () => false, { interval: 10, maxAttempts: 3 }); } catch (e) { '
                 'console.log(e.message, Date.now() - t1 >= 18, Date.now() - t1 < 200); }\n',
       'hint': 'Цикл по попыткам: await check(), при неудаче — пауза, кроме последней попытки.',
       'expected': ['готово на 3 true', 'сразу', 'не дождались после 3 попыток true true']},
      {'id': 'j10-latest',
       'mode': 'js',
       'title': 'Только последний запрос побеждает',
       'statement': 'Напишите функцию latestOnly(fn): fn — асинхронная; возвращает функцию-обёртку. Если '
                    'вызвать обёртку несколько раз подряд, результат нужно получить только от самого '
                    'последнего вызова: у более старых вызовов промис отклоняется ошибкой с name '
                    '«Superseded» (если они ещё не завершились к моменту нового вызова, то в момент своего '
                    'завершения; если уже завершились — остаются как есть).',
       'starter': 'function latestOnly(fn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const search = latestOnly(async (q, ms) => { await sleep(ms); return "результат " + q; '
                 '});\n'
                 'const a = search("a", 30);\n'
                 'const b = search("ab", 10);\n'
                 'const c = search("abc", 20);\n'
                 'const show = async (name, p) => { try { console.log(name, await p); } catch (e) { '
                 'console.log(name, e.name); } };\n'
                 'await Promise.all([show("a", a), show("ab", b), show("abc", c)]);\n'
                 'console.log(await search("z", 1));\n'
                 'const d = search("d", 5);\n'
                 'await sleep(30);\n'
                 'console.log(await d);\n',
       'hint': 'Счётчик вызовов: после await сравните свой номер с последним.',
       'expected': ['ab Superseded', 'abc результат abc', 'a Superseded', 'результат z', 'результат d']},
      {'id': 'j10-memo-async',
       'mode': 'js',
       'title': 'Мемоизация асинхронной функции',
       'statement': 'Напишите функцию memoizeAsync(fn): ключ — JSON.stringify(аргументов). Одновременные '
                    'вызовы с одним ключом используют один и тот же запущенный промис; результат успешного '
                    'вызова кэшируется; при ошибке запись из кэша удаляется (следующий вызов пробует снова). '
                    'Возвращаемая функция имеет метод clear().',
       'starter': 'function memoizeAsync(fn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'let calls = 0;\n'
                 'const f = memoizeAsync(async (x) => { calls++; await sleep(10); if (x === "bad" && calls < '
                 '4) throw new Error("временно"); return x + "!"; });\n'
                 'const [p1, p2] = [f("a"), f("a")];\n'
                 'console.log(p1 === p2, await p1, calls);\n'
                 'console.log(await f("a"), calls);\n'
                 'console.log(await f("b"), calls);\n'
                 'try { await f("bad"); } catch (e) { console.log(e.message, calls); }\n'
                 'console.log(await f("bad"), calls);\n'
                 'f.clear();\n'
                 'console.log(await f("a"), calls);\n',
       'hint': 'Map ключ → промис; при отклонении удалите ключ в p.catch.',
       'expected': ['true a! 1', 'a! 1', 'b! 2', 'временно 3', 'bad! 4', 'a! 5']},
      {'id': 'j10-abortable-sleep',
       'mode': 'js',
       'title': 'Прерываемое ожидание',
       'statement': 'Напишите функцию sleepAbortable(ms, signal): возвращает промис, который выполняется '
                    'через ms миллисекунд; если signal уже отменён или будет отменён раньше — отклоняется '
                    'ошибкой с name «AbortError» (таймер при этом очищается, слушатель снимается). Без '
                    'signal работает как обычный sleep.',
       'starter': 'function sleepAbortable(ms, signal) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const t0 = Date.now();\n'
                 'await sleepAbortable(20);\n'
                 'console.log(Date.now() - t0 >= 15);\n'
                 'const ac = new AbortController();\n'
                 'setTimeout(() => ac.abort(), 10);\n'
                 'const t1 = Date.now();\n'
                 'try { await sleepAbortable(5000, ac.signal); } catch (e) { console.log(e.name, Date.now() '
                 '- t1 < 1000); }\n'
                 'try { await sleepAbortable(5, AbortSignal.abort()); } catch (e) { console.log("уже '
                 'отменён:", e.name); }\n'
                 'const ac2 = new AbortController();\n'
                 'await sleepAbortable(5, ac2.signal);\n'
                 'console.log("успел");\n',
       'hint': 'Слушатель abort с { once: true }; в обработчике очистите таймер и отклоните промис.',
       'expected': ['true', 'AbortError true', 'уже отменён: AbortError', 'успел']},
      {'id': 'j10-any-signal',
       'mode': 'js',
       'title': 'Объединение сигналов отмены',
       'statement': 'Напишите функцию anySignal(signals): возвращает AbortSignal, который отменяется, как '
                    'только отменяется любой из переданных (с тем же reason); если какой-то уже отменён — '
                    'результат отменён сразу. AbortSignal.any использовать нельзя.',
       'starter': 'function anySignal(signals) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const a = new AbortController(), b = new AbortController();\n'
                 'const s = anySignal([a.signal, b.signal]);\n'
                 'console.log(s.aborted);\n'
                 'b.abort("причина-b");\n'
                 'console.log(s.aborted, s.reason);\n'
                 'a.abort("причина-a");\n'
                 'console.log(s.reason);\n'
                 'console.log(anySignal([AbortSignal.abort("уже")]).aborted, '
                 'anySignal([AbortSignal.abort("уже")]).reason);\n'
                 'console.log(anySignal([]).aborted);\n'
                 'const t = anySignal([new AbortController().signal, AbortSignal.timeout(20)]);\n'
                 'await new Promise((r) => setTimeout(r, 60));\n'
                 'console.log(t.aborted, t.reason.name);\n'
                 'console.log(__count("AbortSi" + "gnal.any"));\n',
       'hint': 'Новый AbortController: подпишитесь на abort каждого сигнала и отмените свой с тем же reason.',
       'expected': ['false', 'true причина-b', 'причина-b', 'true уже', 'false', 'true TimeoutError', '0']},
      {'id': 'j10-queue',
       'mode': 'js',
       'title': 'Очередь задач с ограничением',
       'statement': 'Напишите класс TaskQueue(concurrency): метод add(fn) ставит асинхронную функцию в '
                    'очередь и возвращает промис с её результатом (или ошибкой); одновременно выполняется не '
                    'больше concurrency задач, задачи стартуют в порядке добавления; метод onIdle() '
                    'возвращает промис, который выполняется, когда очередь пуста и ничего не выполняется '
                    '(сразу, если уже так).',
       'starter': 'class TaskQueue {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const q = new TaskQueue(2);\n'
                 'const log = [];\n'
                 'let running = 0, peak = 0;\n'
                 'const job = (name, ms, fail) => async () => { log.push("start " + name); running++; peak = '
                 'Math.max(peak, running); await sleep(ms); running--; log.push("end " + name); if (fail) '
                 'throw new Error(name); return name; };\n'
                 'const ps = [q.add(job("a", 60)), q.add(job("b", 10)), q.add(job("c", 10)), q.add(job("d", '
                 '10, true)), q.add(job("e", 5))];\n'
                 'ps.forEach((p) => p.catch(() => {}));\n'
                 'await q.onIdle();\n'
                 'console.log(log.join(", "), peak);\n'
                 'console.log(await ps[0], await ps[2], await Promise.allSettled(ps).then((r) => r.map((x) '
                 '=> x.status[0]).join("")));\n'
                 'await q.onIdle();\n'
                 'console.log("idle сразу");\n',
       'hint': 'Счётчик активных задач и массив ожидающих; по завершении задачи запускайте следующую и '
               'проверяйте «пусто».',
       'expected': ['start a, start b, end b, start c, end c, start d, end d, start e, end e, end a 2',
                    'a c fffrf',
                    'idle сразу']},
      {'id': 'j10-semaphore',
       'mode': 'js',
       'title': 'Семафор',
       'statement': 'Напишите класс Semaphore(n): метод acquire() → промис, выполняющийся, когда разрешение '
                    'получено (сразу, если свободно; иначе — в порядке очереди FIFO); release() возвращает '
                    'разрешение (передавая его первому ожидающему); метод run(fn) берёт разрешение, '
                    'выполняет fn и гарантированно отпускает его (и при ошибке); свойство available — число '
                    'свободных разрешений.',
       'starter': 'class Semaphore {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const s = new Semaphore(2);\n'
                 'console.log(s.available);\n'
                 'const order = [];\n'
                 'const task = (n, ms) => s.run(async () => { order.push("in " + n); await sleep(ms); '
                 'order.push("out " + n); return n; });\n'
                 'const r = await Promise.all([task(1, 30), task(2, 10), task(3, 10), task(4, 5)]);\n'
                 'console.log(JSON.stringify(r), s.available);\n'
                 'console.log(order.join(", "));\n'
                 'try { await s.run(async () => { throw new Error("упал"); }); } catch (e) { '
                 'console.log(e.message, s.available); }\n'
                 'await s.acquire(); await s.acquire();\n'
                 'console.log(s.available);\n'
                 'let got = false;\n'
                 's.acquire().then(() => { got = true; });\n'
                 'await sleep(5);\n'
                 'console.log(got);\n'
                 's.release();\n'
                 'await sleep(5);\n'
                 'console.log(got, s.available);\n',
       'hint': 'Очередь ожидающих resolve-функций; release отдаёт разрешение первому из очереди.',
       'expected': ['2',
                    '[1,2,3,4] 2',
                    'in 1, in 2, out 2, in 3, out 3, in 4, out 4, out 1',
                    'упал 2',
                    '0',
                    'false',
                    'true 0']},
      {'id': 'j10-once-promise',
       'mode': 'js',
       'title': 'Событие как промис',
       'statement': 'Напишите функцию once(emitter, event, { signal }): возвращает промис, выполняемый '
                    'массивом аргументов первого события event у emitter (объект с on/off через '
                    'addEventListener-стиль: emitter.on(event, fn), emitter.off(event, fn)); если у emitter '
                    'за это время сработает событие «error» — отклоняется его аргументом; при отмене signal '
                    '— отклоняется AbortError; слушатели снимаются в любом случае.',
       'starter': 'function once(emitter, event, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'import { EventEmitter } from "node:events";\n'
                 'const e = new EventEmitter();\n'
                 'setTimeout(() => e.emit("ready", 1, "два"), 5);\n'
                 'console.log(JSON.stringify(await once(e, "ready")), e.listenerCount("ready"), '
                 'e.listenerCount("error"));\n'
                 'setTimeout(() => e.emit("error", new Error("сбой")), 5);\n'
                 'try { await once(e, "ready"); } catch (x) { console.log(x.message, '
                 'e.listenerCount("ready"), e.listenerCount("error")); }\n'
                 'const ac = new AbortController();\n'
                 'setTimeout(() => ac.abort(), 5);\n'
                 'try { await once(e, "never", { signal: ac.signal }); } catch (x) { console.log(x.name, '
                 'e.listenerCount("never")); }\n'
                 'try { await once(e, "x", { signal: AbortSignal.abort() }); } catch (x) { '
                 'console.log(x.name); }\n'
                 'setTimeout(() => e.emit("data"), 1);\n'
                 'console.log(JSON.stringify(await once(e, "data")));\n',
       'hint': 'Три слушателя (событие, error, abort) и общая функция cleanup, снимающая все.',
       'expected': ['[1,"два"] 0 0', 'сбой 0 0', 'AbortError 0', 'AbortError', '[]']},
      {'id': 'j10-async-iter-basic',
       'mode': 'js',
       'title': 'Асинхронные итераторы: from, take, map',
       'statement': 'Напишите асинхронные генераторы и помощник: fromArray(arr, ms) (выдаёт элементы с '
                    'паузой ms перед каждым), mapAsync(iter, fn) (применяет fn, возможно асинхронную), '
                    'take(iter, n) (первые n и остановка исходного итератора) и collect(iter) → массив всех '
                    'значений.',
       'starter': 'async function* fromArray(arr, ms) {\n'
                  '}\n'
                  'async function* mapAsync(iter, fn) {\n'
                  '}\n'
                  'async function* take(iter, n) {\n'
                  '}\n'
                  'async function collect(iter) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let produced = 0;\n'
                 'async function* source() { for (let i = 1; i <= 1000; i++) { produced++; yield i; } }\n'
                 'console.log(JSON.stringify(await collect(fromArray([1, 2, 3], 3))));\n'
                 'console.log(JSON.stringify(await collect(mapAsync(fromArray([1, 2, 3], 1), async (x) => x '
                 '* 10))));\n'
                 'console.log(JSON.stringify(await collect(take(source(), 3))), produced);\n'
                 'console.log(JSON.stringify(await collect(take(fromArray([1, 2], 1), 10))), '
                 'JSON.stringify(await collect(take(source(), 0))));\n'
                 'console.log(JSON.stringify(await collect(take(mapAsync(source(), (x) => x * x), 4))));\n',
       'hint': 'return внутри async-генератора останавливает цикл for await исходного — и закрывает его.',
       'expected': ['[1,2,3]', '[10,20,30]', '[1,2,3] 3', '[1,2] []', '[1,4,9,16]']},
      {'id': 'j10-paginate',
       'mode': 'js',
       'title': 'Постраничная загрузка',
       'statement': 'Напишите асинхронный генератор paginate(getPage): getPage(token) возвращает промис { '
                    'items: [...], next: токен | null }; начальный токен — undefined. paginate выдаёт '
                    'элементы по одному, запрашивая следующую страницу только когда потребитель дошёл до '
                    'конца текущей; останавливается при next = null. Напишите ещё fetchAll(getPage, limit) → '
                    'массив первых limit элементов, не запрашивая лишних страниц.',
       'starter': 'async function* paginate(getPage) {\n}\nasync function fetchAll(getPage, limit) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'let requests = [];\n'
                 'const pages = { undefined: { items: [1, 2], next: "p2" }, p2: { items: [3, 4], next: "p3" '
                 '}, p3: { items: [5], next: null } };\n'
                 'const getPage = async (t) => { requests.push(String(t)); await sleep(2); return pages[t]; '
                 '};\n'
                 'const all = [];\n'
                 'for await (const x of paginate(getPage)) all.push(x);\n'
                 'console.log(JSON.stringify(all), requests.join());\n'
                 'requests = [];\n'
                 'console.log(JSON.stringify(await fetchAll(getPage, 3)), requests.join());\n'
                 'requests = [];\n'
                 'console.log(JSON.stringify(await fetchAll(getPage, 2)), requests.join());\n'
                 'requests = [];\n'
                 'console.log(JSON.stringify(await fetchAll(getPage, 100)), requests.join());\n'
                 'console.log(JSON.stringify(await fetchAll(async () => ({ items: [], next: null }), 5)));\n',
       'hint': 'yield* page.items выдаёт элементы страницы; следующий getPage вызывается только после '
               'исчерпания текущей.',
       'expected': ['[1,2,3,4,5] undefined,p2,p3',
                    '[1,2,3] undefined,p2',
                    '[1,2] undefined',
                    '[1,2,3,4,5] undefined,p2,p3',
                    '[]']},
      {'id': 'j10-batch-iter',
       'mode': 'js',
       'title': 'Пачки из потока',
       'statement': 'Напишите асинхронный генератор batchAsync(iter, size): собирает значения асинхронного '
                    '(или обычного) итерируемого iter в массивы по size элементов; последняя пачка может '
                    'быть короче; пустой поток даёт ноль пачек.',
       'starter': 'async function* batchAsync(iter, size) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'async function* slow(n) { for (let i = 1; i <= n; i++) { await sleep(1); yield i; } }\n'
                 'const run = async (it, size) => { const out = []; for await (const b of batchAsync(it, '
                 'size)) out.push(b); return JSON.stringify(out); };\n'
                 'console.log(await run(slow(7), 3));\n'
                 'console.log(await run(slow(6), 3));\n'
                 'console.log(await run(slow(0), 3));\n'
                 'console.log(await run([1, 2, 3], 2));\n'
                 'console.log(await run(slow(2), 5));\n'
                 'console.log(await run("abcde", 2));\n',
       'hint': 'Копите пачку и отдавайте при заполнении; хвост — после цикла.',
       'expected': ['[[1,2,3],[4,5,6],[7]]',
                    '[[1,2,3],[4,5,6]]',
                    '[]',
                    '[[1,2],[3]]',
                    '[[1,2]]',
                    '[["a","b"],["c","d"],["e"]]']},
      {'id': 'j10-order',
       'mode': 'js',
       'title': 'Предскажите порядок: микрозадачи и таймеры',
       'statement': 'Напишите функцию run(log): через log(строка) выведите последовательность «1 синхронно», '
                    '«2 промис», «3 вложенный промис», «4 таймер», используя setTimeout(…, 0), '
                    'Promise.resolve().then (в том числе вложенный then внутри обработчика) и синхронный '
                    'вызов. Нужный порядок вывода получится только при правильной расстановке.',
       'starter': 'function run(log) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const out = [];\n'
                 'run((s) => out.push(s));\n'
                 'out.push("конец скрипта");\n'
                 'setTimeout(() => console.log(out.join("\\n")), 30);\n',
       'hint': 'Микрозадачи, добавленные внутри микрозадачи, выполняются до следующего таймера.',
       'expected': ['1 синхронно', 'конец скрипта', '2 промис', '3 вложенный промис', '4 таймер']},
      {'id': 'j10-waterfall',
       'mode': 'js',
       'title': 'Водопад: результат передаётся дальше',
       'statement': 'Напишите функцию waterfall(fns, initial): fns — функции (синхронные или асинхронные), '
                    'каждая принимает результат предыдущей (первая — initial); возвращает промис с '
                    'результатом последней. При ошибке остальные не вызываются. Для пустого массива — '
                    'initial.',
       'starter': 'async function waterfall(fns, initial) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const log = [];\n'
                 'console.log(await waterfall([(x) => x + 1, async (x) => { await sleep(5); return x * 10; '
                 '}, (x) => `итог ${x}`], 4));\n'
                 'console.log(await waterfall([], "как есть"));\n'
                 'try { await waterfall([() => { throw new Error("стоп"); }, () => log.push("не вызвана")], '
                 '1); } catch (e) { console.log(e.message, log.length); }\n'
                 'console.log(await waterfall([async (s) => s.toUpperCase()], "abc"));\n',
       'hint': 'acc = await f(acc) в цикле.',
       'expected': ['итог 50', 'как есть', 'стоп 0', 'ABC']},
      {'id': 'j10-lazy-promise',
       'mode': 'js',
       'title': 'Ленивый промис',
       'statement': 'Напишите класс Lazy(executor): как Promise, но executor запускается только при первом '
                    'вызове then (или catch/finally) и один раз; пока никто не подписался, executor не '
                    'вызывается. Объект должен работать с await. Экземпляр — «thenable»: нужен метод '
                    'then(onFulfilled, onRejected); catch(onRejected) реализуйте через then.',
       'starter': 'class Lazy {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'let started = 0;\n'
                 'const lazy = new Lazy((resolve) => { started++; setTimeout(() => resolve("значение"), 5); '
                 '});\n'
                 'await sleep(10);\n'
                 'console.log(started);\n'
                 'console.log(await lazy, started);\n'
                 'console.log(await lazy, started);\n'
                 'const bad = new Lazy((_, reject) => reject(new Error("сбой")));\n'
                 'console.log(await bad.catch((e) => "поймано " + e.message));\n'
                 'try { await bad; } catch (e) { console.log(e.message); }\n'
                 'console.log(await Promise.all([lazy, new Lazy((r) => r(1))]));\n',
       'hint': 'Создавайте внутренний Promise в then при первом обращении.',
       'expected': ['0', 'значение 1', 'значение 1', 'поймано сбой', 'сбой', "[ 'значение', 1 ]"]},
      {'id': 'j10-deferred',
       'mode': 'js',
       'title': 'Deferred: промис с внешним управлением',
       'statement': 'Напишите функцию deferred(): возвращает объект { promise, resolve, reject, settled } — '
                    'как Promise.withResolvers, но с полем settled (булево, изменяется после завершения: '
                    'после resolve или reject, в том числе если вызвать их повторно). Повторные вызовы '
                    'resolve/reject ничего не меняют. Promise.withResolvers использовать нельзя.',
       'starter': 'function deferred() {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const d = deferred();\n'
                 'console.log(d.settled, d.promise instanceof Promise);\n'
                 'setTimeout(() => d.resolve("готово"), 5);\n'
                 'console.log(await d.promise, d.settled);\n'
                 'd.resolve("второй раз");\n'
                 'd.reject(new Error("поздно"));\n'
                 'console.log(await d.promise);\n'
                 'const e = deferred();\n'
                 'e.reject(new Error("плохо"));\n'
                 'console.log(e.settled);\n'
                 'try { await e.promise; } catch (x) { console.log(x.message); }\n'
                 'console.log(__count("withRe" + "solvers"));\n',
       'hint': 'Сохраните resolve и reject из исполнителя в объект и обновляйте settled.',
       'expected': ['false true', 'готово true', 'готово', 'true', 'плохо', '0']},
      {'id': 'j10-pipe-async',
       'mode': 'js',
       'title': 'pipeAsync: синхронные и асинхронные шаги',
       'statement': 'Напишите функцию pipeAsync(...fns): возвращает функцию, которая последовательно '
                    'применяет шаги к значению; шаги могут быть синхронными или асинхронными; результат — '
                    'всегда промис. Если на каком-то шаге возникло исключение (синхронное или отклонение), '
                    'результат — отклонённый промис, остальные шаги не вызываются.',
       'starter': 'function pipeAsync(...fns) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const p = pipeAsync((x) => x + 1, async (x) => { await sleep(3); return x * 2; }, '
                 'String);\n'
                 'const r = p(4);\n'
                 'console.log(r instanceof Promise, await r);\n'
                 'console.log(await pipeAsync()(7));\n'
                 'let called = 0;\n'
                 'const bad = pipeAsync(() => { throw new Error("синхронный сбой"); }, () => { called++; '
                 '});\n'
                 'const bp = bad(1);\n'
                 'console.log(bp instanceof Promise);\n'
                 'bp.catch(() => {});\n'
                 'try { await bad(1); } catch (e) { console.log(e.message, called); }\n'
                 'try { await pipeAsync(async () => { throw new Error("async сбой"); })(1); } catch (e) { '
                 'console.log(e.message); }\n',
       'hint': 'async-функция сама превращает исключения в отклонённый промис.',
       'expected': ['true 10', '7', 'true', 'синхронный сбой 0', 'async сбой']},
      {'id': 'j10-summary',
       'mode': 'js',
       'title': 'Сводка по результатам',
       'statement': 'Напишите асинхронную функцию runBatch(tasks): tasks — массив функций, возвращающих '
                    'промис; запускает все параллельно; возвращает { ok: [значения успешных в исходном '
                    'порядке], failed: [{ index, message }] (по порядку индексов), total, durationMs (число '
                    '— сколько мс заняла вся пачка, не меньше самой долгой задачи) }.',
       'starter': 'async function runBatch(tasks) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const r = await runBatch([() => sleep(30, "a"), async () => { throw new Error("b упал"); '
                 '}, () => sleep(5, "c"), () => Promise.reject("строка")]);\n'
                 'console.log(JSON.stringify({ ok: r.ok, failed: r.failed, total: r.total }), r.durationMs '
                 '>= 25, r.durationMs < 500);\n'
                 'const e = await runBatch([]);\n'
                 'console.log(JSON.stringify({ ok: e.ok, failed: e.failed, total: e.total }), typeof '
                 'e.durationMs);\n',
       'hint': 'Promise.allSettled + разбор статусов; время — Date.now() до и после.',
       'expected': ['{"ok":["a","c"],"failed":[{"index":1,"message":"b '
                    'упал"},{"index":3,"message":"строка"}],"total":4} true true',
                    '{"ok":[],"failed":[],"total":0} number']},
      {'id': 'j10-finally-poly',
       'mode': 'js',
       'title': 'Полифил Promise.prototype.finally',
       'statement': 'Напишите функцию finallyPoly(promise, onFinally): подписывается на завершение промиса '
                    'любым исходом; вызывает onFinally() без аргументов (если вернёт промис — дожидается '
                    'его) и затем сохраняет исходный результат: значение или причину. Если onFinally бросит '
                    'исключение или вернёт отклонённый промис — результат заменяется этой ошибкой. Метод '
                    'finally использовать нельзя.',
       'starter': 'function finallyPoly(promise, onFinally) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const log = [];\n'
                 'console.log(await finallyPoly(Promise.resolve(1), () => log.push("f1")), log.join());\n'
                 'try { await finallyPoly(Promise.reject(new Error("исходная")), () => log.push("f2")); } '
                 'catch (e) { console.log(e.message, log.join()); }\n'
                 'console.log(await finallyPoly(Promise.resolve("v"), () => sleep(10, "игнорируется")));\n'
                 'try { await finallyPoly(Promise.resolve("v"), () => { throw new Error("из finally"); }); } '
                 'catch (e) { console.log(e.message); }\n'
                 'try { await finallyPoly(Promise.reject(new Error("a")), () => Promise.reject(new '
                 'Error("b"))); } catch (e) { console.log(e.message); }\n'
                 'let args;\n'
                 'await finallyPoly(Promise.resolve(5), (...a) => { args = a.length; });\n'
                 'console.log(args, __count(".fin" + "ally("));\n',
       'hint': 'then(onOk, onFail): в обоих случаях вызовите onFinally и верните/перебросьте исходное.',
       'expected': ['1 f1', 'исходная f1,f2', 'v', 'из finally', 'b', '0 0']},
      {'id': 'j10-cached-ttl',
       'mode': 'js',
       'title': 'Кэш с временем жизни',
       'statement': 'Напишите функцию cachedAsync(fn, ttl, now): результат успешного вызова fn(key) '
                    'кэшируется по ключу на ttl миллисекунд (время — функция now()); пока запись свежая, '
                    'возвращается она; когда устарела — вызывается fn снова; одновременные запросы одного '
                    'ключа не дублируются; ошибка не кэшируется.',
       'starter': 'function cachedAsync(fn, ttl, now) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'let t = 0, calls = 0;\n'
                 'const get = cachedAsync(async (k) => { calls++; await sleep(5); if (k === "bad" && calls < '
                 '4) throw new Error("сбой"); return k + calls; }, 100, () => t);\n'
                 'const [a, b] = await Promise.all([get("x"), get("x")]);\n'
                 'console.log(a, b, calls);\n'
                 't = 50;\n'
                 'console.log(await get("x"), calls);\n'
                 't = 150;\n'
                 'console.log(await get("x"), calls);\n'
                 'try { await get("bad"); } catch (e) { console.log(e.message, calls); }\n'
                 'console.log(await get("bad"), calls);\n',
       'hint': 'Запись: промис + время завершения; свежесть — now() - at < ttl; ошибка удаляет запись.',
       'expected': ['x1 x1 1', 'x1 1', 'x2 2', 'сбой 3', 'bad4 4']},
      {'id': 'j10-rate-limit',
       'mode': 'js',
       'title': 'Ограничение частоты вызовов',
       'statement': 'Напишите функцию rateLimited(fn, max, windowMs): возвращает функцию-обёртку; не больше '
                    'max вызовов fn стартует за любой интервал windowMs мс; лишние вызовы откладываются '
                    '(ставятся в очередь и стартуют в порядке поступления, как только в окне появится '
                    'место). Результат — промис результата fn. Время — реальное (setTimeout, Date.now).',
       'starter': 'function rateLimited(fn, max, windowMs) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const t0 = Date.now();\n'
                 'const times = [];\n'
                 'const f = rateLimited(async (i) => { times.push(Date.now() - t0); return i; }, 2, 60);\n'
                 'const r = await Promise.all([1, 2, 3, 4, 5].map((i) => f(i)));\n'
                 'console.log(JSON.stringify(r));\n'
                 'const gap = (i, j) => times[j] - times[i];\n'
                 'console.log(gap(0, 1) < 40, gap(1, 2) >= 40, gap(2, 3) < 40, gap(0, 2) >= 50, gap(0, 4) >= '
                 '100);\n'
                 'console.log(times.length);\n',
       'hint': 'Храните времена последних стартов; когда место заполнено — ждите, пока самый старый выйдет '
               'из окна.',
       'expected': ['[1,2,3,4,5]', 'true true true true true', '5']},
      {'id': 'j10-fix-foreach',
       'mode': 'js',
       'title': 'Исправьте: forEach с await',
       'statement': 'Функция saveAll(items, save) должна вызвать save для каждого элемента строго по очереди '
                    'и вернуть число сохранённых. Сейчас она использует forEach с await, поэтому завершается '
                    'раньше, чем что-либо сохранено, и возвращает 0. Исправьте.',
       'starter': 'async function saveAll(items, save) {\n'
                  '  let count = 0;\n'
                  '  items.forEach(async (x) => {\n'
                  '    await save(x);\n'
                  '    count++;\n'
                  '  });\n'
                  '  return count;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const log = [];\n'
                 'const save = async (x) => { log.push("start " + x); await sleep(5); log.push("end " + x); '
                 '};\n'
                 'console.log(await saveAll(["a", "b", "c"], save), log.join(" "));\n'
                 'console.log(await saveAll([], save));\n',
       'hint': 'Используйте цикл for…of — await в нём действительно ждёт.',
       'expected': ['3 start a end a start b end b start c end c', '0']},
      {'id': 'j10-fix-parallel',
       'mode': 'js',
       'title': 'Исправьте: независимые запросы идут по очереди',
       'statement': 'Функция loadDashboard(api) загружает три независимых ресурса (user, orders, stats) и '
                    'возвращает объект { user, orders, stats }. Сейчас запросы идут последовательно и '
                    'занимают суммарное время. Исправьте так, чтобы они выполнялись параллельно (общее время '
                    '— как у самого медленного).',
       'starter': 'async function loadDashboard(api) {\n'
                  '  const user = await api.user();\n'
                  '  const orders = await api.orders();\n'
                  '  const stats = await api.stats();\n'
                  '  return { user, orders, stats };\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const api = { user: () => sleep(40, "Ада"), orders: () => sleep(40, [1, 2]), stats: () => '
                 'sleep(40, { visits: 9 }) };\n'
                 'const t0 = Date.now();\n'
                 'const d = await loadDashboard(api);\n'
                 'const dt = Date.now() - t0;\n'
                 'console.log(JSON.stringify(d));\n'
                 'console.log(dt < 100, dt >= 35);\n',
       'hint': 'Запустите все три вызова сразу и дождитесь Promise.all.',
       'expected': ['{"user":"Ада","orders":[1,2],"stats":{"visits":9}}', 'true true']},
      {'id': 'j10-fix-try-return',
       'mode': 'js',
       'title': 'Исправьте: ошибка проскакивает мимо catch',
       'statement': 'Функция safeLoad(load) должна возвращать «запасное» значение «нет данных», если load() '
                    'отклонится. Сейчас она возвращает промис без await внутри try, поэтому отклонение '
                    'проходит мимо catch. Исправьте, сохранив try/catch.',
       'starter': 'async function safeLoad(load) {\n'
                  '  try {\n'
                  '    return load();\n'
                  '  } catch (e) {\n'
                  '    return "нет данных";\n'
                  '  }\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'console.log(await safeLoad(async () => "данные"));\n'
                 'console.log(await safeLoad(async () => { await sleep(3); throw new Error("сбой сети"); '
                 '}));\n'
                 'console.log(await safeLoad(() => { throw new Error("синхронный"); }));\n'
                 'console.log(await safeLoad(() => 5));\n',
       'hint': 'return await load() внутри try.',
       'expected': ['данные', 'нет данных', 'нет данных', '5']},
      {'id': 'j10-unhandled',
       'mode': 'js',
       'title': 'Необработанные отклонения',
       'statement': 'Напишите функцию trackRejections(): возвращает объект { stop(), list() }; пока трекер '
                    'работает, он собирает причины необработанных отклонений промисов (событие process '
                    '«unhandledRejection») в массив (list() возвращает копию причин-сообщений: '
                    'reason.message или String(reason)); stop() снимает слушатель. Для необработанных '
                    'отклонений процесс не должен завершаться, пока слушатель установлен.',
       'starter': 'function trackRejections() {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const t = trackRejections();\n'
                 'Promise.reject(new Error("первое"));\n'
                 'Promise.reject("второе");\n'
                 'Promise.reject(new Error("поймано")).catch(() => {});\n'
                 'await sleep(20);\n'
                 'console.log(JSON.stringify(t.list()));\n'
                 't.stop();\n'
                 'console.log(process.listenerCount("unhandledRejection"));\n',
       'hint': "process.on('unhandledRejection', handler) и process.off для остановки.",
       'expected': ['["первое","второе"]', '0']}]}
