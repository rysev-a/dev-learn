"""Задачи книги «Современный Frontend», глава 20 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {20: [{'id': 'j20-percentile',
       'mode': 'js',
       'title': 'Процентили и сводка',
       'statement': 'Напишите функции percentile(values, p), median(values) и summarize(values). percentile '
                    '— метод ближайшего ранга: значения сортируются по возрастанию (исходный массив не '
                    'менять), ранг = max(1, ceil(p / 100 × n)), результат — элемент с этим рангом (p = 0 '
                    'даёт минимум, p = 100 — максимум); пустой массив → null. median — для чётного числа '
                    'значений среднее двух средних, для пустого — null. summarize → { n, min, max, mean '
                    '(округлить до 2 знаков), p50, p75, p95 } (p* — ближайшим рангом); для пустого массива — '
                    '{ n: 0 }. Нечисловые значения и NaN игнорируются.',
       'starter': 'function percentile(values, p) {\n'
                  '}\n'
                  'function median(values) {\n'
                  '}\n'
                  'function summarize(values) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const data = [300, 120, 4000, 90, 850, 1200, 2500, 640, 110, 70];\n'
                 'const copy = [...data];\n'
                 'for (const p of [0, 1, 10, 25, 50, 75, 90, 95, 99, 100]) console.log(p, percentile(data, '
                 'p));\n'
                 'console.log(JSON.stringify(data) === JSON.stringify(copy), percentile([], 50), '
                 'percentile([5], 99), percentile([1, 2], 50), percentile([1, 2, 3, 4], 75), percentile([7, '
                 '"x", NaN, 3, null], 50));\n'
                 'console.log(median(data), median([3, 1, 2]), median([4]), median([]), median([1, 2, 3, '
                 '4]));\n'
                 'console.log(JSON.stringify(canon(summarize(data))), JSON.stringify(canon(summarize([]))), '
                 'JSON.stringify(canon(summarize([1, 2, 2, 5]))), JSON.stringify(canon(summarize([0.1, 0.2, '
                 '0.2]))));\n',
       'hint': 'Отсортируйте копию; ранг = ceil(p/100·n), не меньше 1.',
       'expected': ['0 70',
                    '1 70',
                    '10 70',
                    '25 110',
                    '50 300',
                    '75 1200',
                    '90 2500',
                    '95 4000',
                    '99 4000',
                    '100 4000',
                    'true null 5 1 3 3',
                    '470 2 4 null 2.5',
                    '{"max":4000,"mean":988,"min":70,"n":10,"p50":300,"p75":1200,"p95":4000} {"n":0} '
                    '{"max":5,"mean":2.5,"min":1,"n":4,"p50":2,"p75":2,"p95":5} '
                    '{"max":0.2,"mean":0.17,"min":0.1,"n":3,"p50":0.2,"p75":0.2,"p95":0.2}']},
      {'id': 'j20-cwv-rating',
       'mode': 'js',
       'title': 'Оценка Core Web Vitals',
       'statement': 'Напишите функции rate(metric, value) и assess(samples). Пороги (хорошо ≤ первый, плохо '
                    '> второй, между — «needs-improvement»): lcp [2500, 4000] мс, inp [200, 500] мс, cls '
                    '[0.1, 0.25], fcp [1800, 3000] мс, ttfb [800, 1800] мс. rate → «good» | '
                    '«needs-improvement» | «poor»; неизвестная метрика — Error. assess(samples) — samples: { '
                    'lcp: [значения], inp: [...], cls: [...], … }: для каждой метрики с непустым массивом '
                    'считается 75-й процентиль (ближайший ранг) и оценка; результат { metrics: { имя: { p75, '
                    'rating } }, overall }, где overall по трём основным (lcp, inp, cls), которые есть в '
                    'samples: «poor», если хоть одна poor; «good», если все присутствующие good; иначе '
                    '«needs-improvement»; если ни одной из трёх нет — overall: null. Метрики fcp и ttfb '
                    'попадают в metrics, но на overall не влияют.',
       'starter': 'function rate(metric, value) {\n}\nfunction assess(samples) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'for (const [m, v] of [["lcp", 2500], ["lcp", 2501], ["lcp", 4000], ["lcp", 4001], ["inp", '
                 '200], ["inp", 350], ["inp", 501], ["cls", 0.1], ["cls", 0.11], ["cls", 0.25], ["cls", '
                 '0.26], ["fcp", 1800], ["fcp", 3001], ["ttfb", 800], ["ttfb", 1801], ["lcp", 0]]) '
                 'console.log(m, v, rate(m, v));\n'
                 'try { rate("fid", 1); } catch (e) { console.log(e.message); }\n'
                 'const show = (s) => console.log(JSON.stringify(canon(assess(s))));\n'
                 'show({ lcp: [1000, 1200, 1500, 2000, 9000], inp: [100, 120, 150], cls: [0, 0.01, 0.02, '
                 '0.5] });\n'
                 'show({ lcp: [2000, 3000, 3500, 5000], inp: [100], cls: [0.05] });\n'
                 'show({ lcp: [1, 2, 3, 4], inp: [600, 700], cls: [] });\n'
                 'show({ fcp: [1000, 2000, 4000], ttfb: [500] }); show({}); show({ cls: [0.3, 0.3, 0.01, '
                 '0.01] }); show({ lcp: [], inp: [250] });\n',
       'hint': 'p75 ближайшим рангом; overall — только по трём основным метрикам.',
       'expected': ['lcp 2500 good',
                    'lcp 2501 needs-improvement',
                    'lcp 4000 needs-improvement',
                    'lcp 4001 poor',
                    'inp 200 good',
                    'inp 350 needs-improvement',
                    'inp 501 poor',
                    'cls 0.1 good',
                    'cls 0.11 needs-improvement',
                    'cls 0.25 needs-improvement',
                    'cls 0.26 poor',
                    'fcp 1800 good',
                    'fcp 3001 poor',
                    'ttfb 800 good',
                    'ttfb 1801 poor',
                    'lcp 0 good',
                    'Неизвестная метрика: fid',
                    '{"metrics":{"cls":{"p75":0.02,"rating":"good"},"inp":{"p75":150,"rating":"good"},"lcp":{"p75":2000,"rating":"good"}},"overall":"good"}',
                    '{"metrics":{"cls":{"p75":0.05,"rating":"good"},"inp":{"p75":100,"rating":"good"},"lcp":{"p75":3500,"rating":"needs-improvement"}},"overall":"needs-improvement"}',
                    '{"metrics":{"inp":{"p75":700,"rating":"poor"},"lcp":{"p75":3,"rating":"good"}},"overall":"poor"}',
                    '{"metrics":{"fcp":{"p75":4000,"rating":"poor"},"ttfb":{"p75":500,"rating":"good"}},"overall":null}',
                    '{"metrics":{},"overall":null}',
                    '{"metrics":{"cls":{"p75":0.3,"rating":"poor"}},"overall":"poor"}',
                    '{"metrics":{"inp":{"p75":250,"rating":"needs-improvement"}},"overall":"needs-improvement"}']},
      {'id': 'j20-cls',
       'mode': 'js',
       'title': 'Расчёт CLS по сессионным окнам',
       'statement': 'Напишите функцию calcCLS(entries): entries — записи layout-shift { value, '
                    'hadRecentInput, startTime (мс) } в порядке времени. Записи с hadRecentInput = true '
                    'игнорируются. Остальные группируются в сессионные окна: новое окно начинается, если с '
                    'предыдущего сдвига прошло больше 1000 мс (строго больше) или если с начала окна прошло '
                    'больше 5000 мс (строго больше; сдвиг при таком условии открывает новое окно). Значение '
                    'окна — сумма value. CLS — максимальное из окон, округлённое до 4 знаков; без подходящих '
                    'записей — 0.',
       'starter': 'function calcCLS(entries) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const s = (t, v, input = false) => ({ startTime: t, value: v, hadRecentInput: input });\n'
                 'console.log(calcCLS([]), calcCLS([s(100, 0.05)]), calcCLS([s(100, 0.05), s(900, 0.03), '
                 's(1800, 0.02)]));\n'
                 'console.log(calcCLS([s(100, 0.1), s(1100, 0.1), s(2101, 0.2)]), calcCLS([s(100, 0.1), '
                 's(1101, 0.3)]), calcCLS([s(0, 0.1), s(1000, 0.1)]));\n'
                 'console.log(calcCLS([s(0, 0.02), s(900, 0.02), s(1800, 0.02), s(2700, 0.02), s(3600, '
                 '0.02), s(4500, 0.02), s(5400, 0.02)]), calcCLS([s(0, 0.02), s(1000, 0.02), s(2000, 0.02), '
                 's(3000, 0.02), s(4000, 0.02), s(5000, 0.02), s(5001, 0.5)]), calcCLS([s(0, 0.02), s(1000, '
                 '0.02), s(2000, 0.02), s(3000, 0.02), s(4000, 0.02), s(5000, 0.02), s(5001, 0.001)]));\n'
                 'console.log(calcCLS([s(100, 0.5, true), s(200, 0.05), s(300, 0.7, true)]), calcCLS([s(0, '
                 '0.1, true)]), calcCLS([s(0, 0.1), s(500, 0.7, true), s(1400, 0.1), s(2500, 0.05)]));\n'
                 'console.log(calcCLS([s(0, 0.03333), s(100, 0.03333), s(200, 0.03333)]), calcCLS([s(0, '
                 '0.1), s(50000, 0.09), s(120000, 0.05)]), calcCLS([s(0, 0.00004), s(10, 0.00004)]));\n',
       'hint': 'Сессионное окно: сумма сдвигов с паузами ≤ 1 с и общей длиной ≤ 5 с; берите максимум.',
       'expected': ['0 0.05 0.1', '0.2 0.3 0.2', '0.12 0.5 0.12', '0.05 0 0.1', '0.1 0.1 0.0001']},
      {'id': 'j20-inp',
       'mode': 'js',
       'title': 'Расчёт INP',
       'statement': 'Напишите функцию calcINP(events): events — записи event timing { interactionId, '
                    'duration }. Записи с interactionId, равным 0, undefined или отсутствующим, '
                    'игнорируются. Записи с одним interactionId объединяются в одно взаимодействие с '
                    'максимальной duration. Взаимодействия сортируются по убыванию duration; INP — элемент с '
                    'индексом min(n − 1, floor(n / 50)) (то есть для каждых 50 взаимодействий отбрасывается '
                    'одно самое долгое). Нет взаимодействий — null.',
       'starter': 'function calcINP(events) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const e = (id, d) => ({ interactionId: id, duration: d });\n'
                 'console.log(calcINP([]), calcINP([e(0, 500), e(undefined, 700), { duration: 900 }]), '
                 'calcINP([e(1, 80)]), calcINP([e(1, 80), e(1, 240), e(1, 100)]), calcINP([e(1, 80), e(2, '
                 '200), e(3, 120)]));\n'
                 'const many = (n) => Array.from({ length: n }, (_, i) => e(i + 1, 1000 - i));\n'
                 'for (const n of [10, 49, 50, 51, 99, 100, 101, 149, 150, 250]) console.log(n, '
                 'calcINP(many(n)));\n'
                 'const pairs = []; for (let i = 1; i <= 100; i++) { pairs.push(e(i, 100 + i)); '
                 'pairs.push(e(i, 50)); } console.log(calcINP(pairs));\n'
                 'console.log(calcINP([e(5, 16), e(6, 16)]), calcINP([e(1, 0)]));\n',
       'hint': 'Сгруппируйте по interactionId, возьмите максимум, отсортируйте по убыванию и выберите индекс '
               'floor(n/50).',
       'expected': ['null null 80 240 200',
                    '10 1000',
                    '49 1000',
                    '50 999',
                    '51 999',
                    '99 999',
                    '100 998',
                    '101 998',
                    '149 998',
                    '150 997',
                    '250 995',
                    '198',
                    '16 0']},
      {'id': 'j20-lcp',
       'mode': 'js',
       'title': 'Выбор LCP-элемента',
       'statement': 'Напишите функцию pickLCP(entries, firstInputTime = Infinity). entries — записи '
                    'largest-contentful-paint в порядке времени: { startTime, size (площадь в px²), id, url? '
                    '}. Кандидаты: записи с startTime < firstInputTime (после первого ввода пользователя '
                    'браузер перестаёт учитывать новые) и size > 0. LCP — последний кандидат, который строго '
                    'больше по size всех предыдущих кандидатов (в порядке времени); если записи с одинаковым '
                    'size — остаётся прежний. Результат — { id, startTime, size } этого кандидата или null, '
                    'если кандидатов нет.',
       'starter': 'function pickLCP(entries, firstInputTime) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const L = (t, size, id) => ({ startTime: t, size, id, url: "u" });\n'
                 'const show = (r) => console.log(JSON.stringify(r === null ? null : canon(r)));\n'
                 'show(pickLCP([])); show(pickLCP([L(100, 500, "h1")])); show(pickLCP([L(100, 500, "h1"), '
                 'L(300, 40000, "hero"), L(500, 900, "p")]));\n'
                 'show(pickLCP([L(100, 500, "a"), L(200, 500, "b")])); show(pickLCP([L(100, 500, "a"), '
                 'L(200, 501, "b")]));\n'
                 'show(pickLCP([L(100, 500, "a"), L(900, 9999, "late")], 800)); show(pickLCP([L(100, 500, '
                 '"a"), L(800, 9999, "edge")], 800)); show(pickLCP([L(900, 5, "a")], 800));\n'
                 'show(pickLCP([L(10, 0, "empty"), L(20, 7, "ok")])); show(pickLCP([L(10, 0, "empty")])); '
                 'show(pickLCP([L(5, 1000, "big"), L(6, 10, "small"), L(7, 20, "small2")]));\n',
       'hint': 'Пройдите по записям: учитывайте только поздние-до-ввода и обновляйте лучшего при строгом '
               'росте размера.',
       'expected': ['null',
                    '{"id":"h1","size":500,"startTime":100}',
                    '{"id":"hero","size":40000,"startTime":300}',
                    '{"id":"a","size":500,"startTime":100}',
                    '{"id":"b","size":501,"startTime":200}',
                    '{"id":"a","size":500,"startTime":100}',
                    '{"id":"a","size":500,"startTime":100}',
                    'null',
                    '{"id":"ok","size":7,"startTime":20}',
                    'null',
                    '{"id":"big","size":1000,"startTime":5}']},
      {'id': 'j20-tbt',
       'mode': 'js',
       'title': 'Total Blocking Time',
       'statement': 'Напишите функцию totalBlockingTime(tasks, fcp, tti): tasks — главные потоковые задачи { '
                    'start, duration } (мс). Окно измерения — [fcp, tti]. Для каждой задачи берётся её '
                    'пересечение с окном (задача [start, start + duration] обрезается по границам окна); '
                    'если длина пересечения больше 50 мс, блокирующая часть = длина − 50, иначе 0. TBT — '
                    'сумма блокирующих частей. Если tti ≤ fcp — 0. Результат округлить до целого. Также '
                    'напишите функцию longTasks(tasks) → задачи с duration > 50 мс (исходные объекты, в '
                    'порядке начала).',
       'starter': 'function totalBlockingTime(tasks, fcp, tti) {\n}\nfunction longTasks(tasks) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const T = (start, duration) => ({ start, duration });\n'
                 'const tasks = [T(0, 400), T(500, 50), T(600, 51), T(700, 120), T(900, 300), T(1500, 30), '
                 'T(2000, 500), T(2900, 90)];\n'
                 'console.log(totalBlockingTime(tasks, 0, 10000), totalBlockingTime(tasks, 600, 1000), '
                 'totalBlockingTime(tasks, 100, 3000), totalBlockingTime(tasks, 1000, 1100), '
                 'totalBlockingTime(tasks, 5, 5), totalBlockingTime(tasks, 10, 5), totalBlockingTime([], 0, '
                 '100));\n'
                 'console.log(totalBlockingTime([T(0, 50.4), T(100, 50.6)], 0, 1000), '
                 'totalBlockingTime([T(100, 200)], 250, 400), totalBlockingTime([T(100, 200)], 0, 150), '
                 'totalBlockingTime([T(100, 200)], 0, 160));\n'
                 'console.log(JSON.stringify(longTasks([T(900, 300), T(0, 400), T(500, 50), T(600, 51)])), '
                 'JSON.stringify(longTasks([])));\n',
       'hint': 'Обрежьте задачу по окну и вычтите 50 мс, если остаток больше 50.',
       'expected': ['1161 121 1061 50 0 0 0',
                    '1 0 0 10',
                    '[{"start":0,"duration":400},{"start":600,"duration":51},{"start":900,"duration":300}] '
                    '[]']},
      {'id': 'j20-chunks',
       'mode': 'js',
       'title': 'Работа кусками с отдачей управления',
       'statement': 'Напишите асинхронную функцию runInChunks(items, worker, { budgetMs = 50, now, yieldFn, '
                    'signal }): обрабатывает элементы по порядку вызовом worker(item, index) (может быть '
                    'асинхронной — дождаться). Время куска считается от старта куска (старт — начало работы '
                    'или конец последней отдачи управления): после обработки очередного элемента, если now() '
                    '− начало куска ≥ budgetMs и ещё остались элементы, нужно вызвать await yieldFn() и '
                    'начать новый кусок (время старта = now() после yieldFn). Перед каждым элементом '
                    'проверяйте signal?.aborted — если отменено, остановиться. Результат: { processed '
                    '(сколько элементов обработано), yields (сколько раз отдали управление), aborted '
                    '(boolean) }. Ошибка worker пробрасывается.',
       'starter': 'async function runInChunks(items, worker, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let t = 0; const now = () => t; const log = [];\n'
                 'const yieldFn = async () => { log.push("yield@" + t); t += 1; };\n'
                 'const items = Array.from({ length: 10 }, (_, i) => i);\n'
                 'const r1 = await runInChunks(items, (x) => { t += 20; log.push("w" + x); }, { budgetMs: '
                 '50, now, yieldFn }); console.log(JSON.stringify(r1), log.join(" "));\n'
                 'log.length = 0; t = 0; const r2 = await runInChunks(items, (x) => { t += 100; }, { '
                 'budgetMs: 50, now, yieldFn }); console.log(JSON.stringify(r2), log.join(" "));\n'
                 'log.length = 0; t = 0; const r3 = await runInChunks(items, async (x) => { t += 1; }, { '
                 'budgetMs: 50, now, yieldFn }); console.log(JSON.stringify(r3), log.length);\n'
                 'log.length = 0; t = 0; const ctrl = new AbortController(); const r4 = await '
                 'runInChunks(items, (x) => { t += 30; if (x === 3) ctrl.abort(); }, { budgetMs: 50, now, '
                 'yieldFn, signal: ctrl.signal }); console.log(JSON.stringify(r4), log.join(" "));\n'
                 't = 0; console.log(JSON.stringify(await runInChunks([], () => {}, { now, yieldFn })), '
                 'JSON.stringify(await runInChunks([1], () => { t += 1000; }, { now, yieldFn, budgetMs: 10 '
                 '})));\n'
                 't = 0; try { await runInChunks([1, 2], (x) => { if (x === 2) throw new Error("сбой " + x); '
                 '}, { now, yieldFn }); } catch (e) { console.log(e.message); }\n'
                 't = 0; const order = []; await runInChunks([1, 2, 3], async (x) => { order.push("start" + '
                 'x); await new Promise((r) => setTimeout(r, 5)); order.push("end" + x); }, { now, yieldFn '
                 '}); console.log(order.join());\n',
       'hint': 'Проверка бюджета — после обработки элемента и только если элементы ещё остались.',
       'expected': ['{"processed":10,"yields":3,"aborted":false} w0 w1 w2 yield@60 w3 w4 w5 yield@121 w6 w7 '
                    'w8 yield@182 w9',
                    '{"processed":10,"yields":9,"aborted":false} yield@100 yield@201 yield@302 yield@403 '
                    'yield@504 yield@605 yield@706 yield@807 yield@908',
                    '{"processed":10,"yields":0,"aborted":false} 0',
                    '{"processed":4,"yields":2,"aborted":true} yield@60 yield@121',
                    '{"processed":0,"yields":0,"aborted":false} {"processed":1,"yields":0,"aborted":false}',
                    'сбой 2',
                    'start1,end1,start2,end2,start3,end3']},
      {'id': 'j20-scheduler',
       'mode': 'js',
       'title': 'Планировщик задач с приоритетами',
       'statement': 'Напишите функцию createScheduler() → { postTask(fn, options), advance(ms), runNext(), '
                    'runAll(), now(), size() } (аналог scheduler.postTask с виртуальным временем). '
                    'postTask(fn, { priority = "user-visible", delay = 0, signal }) → промис с результатом '
                    'fn() (fn может быть асинхронной; результат или ошибка передаются в промис). Приоритеты: '
                    '«user-blocking» > «user-visible» > «background»; внутри приоритета — по порядку '
                    'постановки (FIFO). Задача с delay > 0 готова не раньше now() + delay (виртуальное '
                    'время, меняется только advance(ms), начальное 0); готовность определяется на момент '
                    'вызова runNext. runNext() → true, если выполнена одна готовая задача (самая '
                    'приоритетная), иначе false; выполнение синхронное (fn вызывается синхронно). runAll() '
                    'выполняет готовые задачи, пока они есть (в том числе поставленные по ходу), и '
                    'возвращает число выполненных. Если signal.aborted — промис отклоняется signal.reason '
                    'сразу при постановке; если сигнал отменён позже — задача удаляется из очереди (если ещё '
                    'не выполнена), промис отклоняется причиной. size() — число задач в очереди (включая '
                    'ожидающие delay).',
       'starter': 'function createScheduler() {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const s = createScheduler(); const log = [];\n'
                 'const p = (name, opts, fn) => s.postTask(() => { log.push(name); return fn ? fn() : name; '
                 '}, opts).then((v) => v, (e) => "ERR:" + (e.message ?? e));\n'
                 'const r = [p("bg1", { priority: "background" }), p("vis1"), p("block1", { priority: '
                 '"user-blocking" }), p("vis2", { priority: "user-visible" }), p("block2", { priority: '
                 '"user-blocking" }), p("bg2", { priority: "background" })];\n'
                 'console.log(s.size(), s.runNext(), log.join()); console.log(s.runAll(), log.join(), '
                 's.size(), s.runNext(), s.runAll());\n'
                 'console.log(JSON.stringify(await Promise.all(r)));\n'
                 'const r2 = [p("later", { delay: 100 }), p("soon", { delay: 10, priority: "background" }), '
                 'p("now", { priority: "background" })];\n'
                 'console.log(s.runAll(), log.slice(6).join(), s.size()); s.advance(10); '
                 'console.log(s.runAll(), log.slice(6).join(), s.now()); s.advance(89); '
                 'console.log(s.runNext()); s.advance(1); console.log(s.runAll(), log.slice(6).join(), '
                 's.size()); console.log(JSON.stringify(await Promise.all(r2)));\n'
                 'const nested = p("outer", {}, () => { p("inner-blocking", { priority: "user-blocking" }); '
                 'p("inner-bg", { priority: "background" }); return "x"; }); const n = s.runAll(); '
                 'console.log(n, log.slice(-3).join()); console.log(await nested);\n'
                 'const c = new AbortController(); const a1 = p("a1", { signal: c.signal }), a2 = p("a2", { '
                 'signal: c.signal }); console.log(s.size()); c.abort(new Error("отмена")); '
                 'console.log(s.size(), s.runAll(), await a1, await a2);\n'
                 'const dead = new AbortController(); dead.abort(new Error("заранее")); const d = p("dead", '
                 '{ signal: dead.signal }); console.log(s.size(), await d);\n'
                 'const e1 = p("boom", {}, () => { throw new Error("сбой"); }); const e2 = p("async-boom", '
                 '{}, async () => { throw new Error("async сбой"); }); const e3 = p("async-ok", {}, async () '
                 '=> 42); s.runAll(); console.log(await e1, await e2, await e3);\n'
                 'const done = new AbortController(); const f = p("finished", { signal: done.signal }); '
                 's.runAll(); console.log(await f); done.abort(new Error("поздно")); await tick(); '
                 'console.log(s.size());\n',
       'hint': 'Очередь с полями rank, at и seq; runNext выбирает среди готовых лучшую по (rank, seq).',
       'expected': ['6 true block1',
                    '5 block1,block2,vis1,vis2,bg1,bg2 0 false 0',
                    '["bg1","vis1","block1","vis2","block2","bg2"]',
                    '1 now 2',
                    '1 now,soon 10',
                    'false',
                    '1 now,soon,later 0',
                    '["later","soon","now"]',
                    '3 outer,inner-blocking,inner-bg',
                    'x',
                    '2',
                    '0 0 ERR:отмена ERR:отмена',
                    '0 ERR:заранее',
                    'ERR:сбой ERR:async сбой 42',
                    'finished',
                    '0']},
      {'id': 'j20-frame-scheduler',
       'mode': 'js',
       'title': 'Читать, потом писать: планировщик кадров',
       'statement': 'Напишите функцию createFrameScheduler(raf) → { measure(fn), mutate(fn) }. raf(cb) '
                    'регистрирует cb на следующий кадр (вызывается драйвером). measure и mutate ставят '
                    'задачи; обе возвращают промис с результатом fn() (ошибка fn отклоняет промис, остальные '
                    'задачи кадра продолжают работу). В кадре сначала выполняются все measure-задачи в '
                    'порядке постановки, затем все mutate-задачи. Задачи, поставленные во время выполнения '
                    'кадра (изнутри задач), попадают в следующий кадр. На один кадр регистрируется только '
                    'один вызов raf (и только если есть задачи, которых ещё нет в зарегистрированном кадре).',
       'starter': 'function createFrameScheduler(raf) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'let pending = null; let rafCalls = 0;\n'
                 'const raf = (cb) => { rafCalls++; pending = cb; };\n'
                 'const nextFrame = async () => { const cb = pending; pending = null; cb?.(); await tick(); '
                 '};\n'
                 'const fs = createFrameScheduler(raf); const log = []; const st = { h: 10 };\n'
                 'const a = fs.mutate(() => { st.h += 5; log.push("write1"); return "w1"; }); const b = '
                 'fs.measure(() => { log.push("read1:" + st.h); return st.h; }); const c = fs.mutate(() => { '
                 'log.push("write2"); }); const d = fs.measure(() => { log.push("read2:" + st.h); });\n'
                 'console.log(rafCalls, log.length); await nextFrame(); console.log(log.join(), '
                 'JSON.stringify(await Promise.all([a, b])), rafCalls, pending);\n'
                 'log.length = 0; const e = fs.measure(() => { log.push("m1"); fs.mutate(() => '
                 'log.push("m1→w")); fs.measure(() => log.push("m1→r")); return 1; }); const f = '
                 'fs.mutate(() => { log.push("w"); }); console.log(rafCalls);\n'
                 'await nextFrame(); console.log(log.join(), rafCalls, pending !== null); await nextFrame(); '
                 'console.log(log.join(), rafCalls, pending);\n'
                 'log.length = 0; const bad = fs.measure(() => { throw new Error("сбой чтения"); }); const '
                 'good = fs.mutate(() => log.push("всё равно")); bad.catch(() => {}); await nextFrame(); try '
                 '{ await bad; } catch (x) { console.log(x.message); } console.log(await good, log.join());\n'
                 'const g = fs.mutate(async () => { await 0; return "асинхронно"; }); await nextFrame(); '
                 'console.log(await g, rafCalls);\n',
       'hint': 'Два списка задач (чтения и записи) и флаг «кадр уже запрошен»; в кадре забирайте и обнуляйте '
               'списки перед выполнением.',
       'expected': ['1 0',
                    'read1:10,read2:10,write1,write2 ["w1",10] 1 null',
                    '2',
                    'm1,w 3 true',
                    'm1,w,m1→r,m1→w 3 null',
                    'сбой чтения',
                    '1 всё равно',
                    'асинхронно 5']},
      {'id': 'j20-layout-thrash',
       'mode': 'js',
       'title': 'Поиск «молотилки раскладки»',
       'statement': 'Напишите функции countReflows(ops) и batchOps(ops). ops — список операций { type: '
                    '"read" | "write" | "frame" } над DOM. Раскладка «грязная» после write; read при грязной '
                    'раскладке — принудительный пересчёт (reflow): он считается и раскладка становится '
                    'чистой; frame — конец кадра, браузер сам пересчитывает раскладку (она чистая, пересчёт '
                    'не считается принудительным). countReflows → число принудительных пересчётов. batchOps '
                    '→ новый список операций, в котором внутри каждого кадра (отрезок до «frame» или до '
                    'конца списка) сначала идут все read (в исходном порядке), затем все write (в исходном '
                    'порядке), а frame остаются разделителями на своих местах. Исходный массив не менять.',
       'starter': 'function countReflows(ops) {\n}\nfunction batchOps(ops) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const mk = (s) => [...s].map((c, i) => ({ type: { r: "read", w: "write", f: "frame" }[c], '
                 'id: i }));\n'
                 'const str = (ops) => ops.map((o) => ({ read: "r", write: "w", frame: "f" '
                 '}[o.type])).join("");\n'
                 'for (const s of ["", "rrr", "www", "wr", "wrwr", "wwrr", "rwrwrw", "wfr", "wrfwr", '
                 '"rwwrrwwr", "wfwfwf", "frwrf"]) { const ops = mk(s); const frozen = '
                 'Object.freeze(ops.map(Object.freeze)); const b = batchOps(frozen); '
                 'console.log(s.padEnd(10), countReflows(frozen), str(b).padEnd(10), countReflows(b)); }\n'
                 'const ops = mk("wrwr"); const b = batchOps(ops); console.log(ops.map((o) => o.id).join(), '
                 'b.map((o) => o.id).join(), b[0] === ops[1]);\n'
                 'const loop = []; for (let i = 0; i < 100; i++) loop.push({ type: "write" }, { type: "read" '
                 '}); console.log(countReflows(loop), countReflows(batchOps(loop)), batchOps(loop).slice(0, '
                 '2).map((o) => o.type).join());\n',
       'hint': 'Один флаг «раскладка грязная»; при батчинге разделяйте операции по границам «frame».',
       'expected': ['           0            0',
                    'rrr        0 rrr        0',
                    'www        0 www        0',
                    'wr         1 rw         0',
                    'wrwr       2 rrww       0',
                    'wwrr       1 rrww       0',
                    'rwrwrw     2 rrrwww     0',
                    'wfr        0 wfr        0',
                    'wrfwr      2 rwfrw      0',
                    'rwwrrwwr   2 rrrrwwww   0',
                    'wfwfwf     0 wfwfwf     0',
                    'frwrf      1 frrwf      0',
                    '0,1,2,3 1,3,0,2 true',
                    '100 0 read,read']},
      {'id': 'j20-virtual-window',
       'mode': 'js',
       'title': 'Окно виртуального списка',
       'statement': 'Напишите функцию virtualWindow({ scrollTop, viewportHeight, itemHeight, count, overscan '
                    '= 3 }) → { start, end, offsetTop, totalHeight, visibleStart, visibleEnd }. totalHeight '
                    '= count × itemHeight. scrollTop ограничьте диапазоном [0, max(0, totalHeight − '
                    'viewportHeight)]. visibleStart = floor(scrollTop / itemHeight), visibleEnd (не включая) '
                    '= min(count, ceil((scrollTop + viewportHeight) / itemHeight)). start = max(0, '
                    'visibleStart − overscan), end = min(count, visibleEnd + overscan) (end не включается). '
                    'offsetTop = start × itemHeight (смещение первой отрисованной строки). Для count = 0 всё '
                    'нули. Если viewportHeight ≤ 0 — видимых строк нет: visibleEnd = visibleStart.',
       'starter': 'function virtualWindow(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const w = (o) => console.log(JSON.stringify(o), JSON.stringify(canon(virtualWindow(o))));\n'
                 'const base = { viewportHeight: 300, itemHeight: 50, count: 1000 };\n'
                 'for (const st of [0, 1, 49, 50, 125, 1000, 49700, 49701, 60000, -50]) w({ ...base, '
                 'scrollTop: st });\n'
                 'w({ ...base, scrollTop: 500, overscan: 0 }); w({ ...base, scrollTop: 500, overscan: 10 }); '
                 'w({ scrollTop: 0, viewportHeight: 300, itemHeight: 50, count: 4 }); w({ scrollTop: 100, '
                 'viewportHeight: 300, itemHeight: 50, count: 4 });\n'
                 'w({ scrollTop: 0, viewportHeight: 300, itemHeight: 50, count: 0 }); w({ scrollTop: 40, '
                 'viewportHeight: 0, itemHeight: 20, count: 100, overscan: 1 }); w({ scrollTop: 25, '
                 'viewportHeight: 100, itemHeight: 30, count: 50 });\n',
       'hint': 'Сначала ограничьте scrollTop, затем найдите видимые индексы и добавьте запас с обеих сторон.',
       'expected': ['{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":0} '
                    '{"end":9,"offsetTop":0,"start":0,"totalHeight":50000,"visibleEnd":6,"visibleStart":0}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":1} '
                    '{"end":10,"offsetTop":0,"start":0,"totalHeight":50000,"visibleEnd":7,"visibleStart":0}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":49} '
                    '{"end":10,"offsetTop":0,"start":0,"totalHeight":50000,"visibleEnd":7,"visibleStart":0}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":50} '
                    '{"end":10,"offsetTop":0,"start":0,"totalHeight":50000,"visibleEnd":7,"visibleStart":1}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":125} '
                    '{"end":12,"offsetTop":0,"start":0,"totalHeight":50000,"visibleEnd":9,"visibleStart":2}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":1000} '
                    '{"end":29,"offsetTop":850,"start":17,"totalHeight":50000,"visibleEnd":26,"visibleStart":20}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":49700} '
                    '{"end":1000,"offsetTop":49550,"start":991,"totalHeight":50000,"visibleEnd":1000,"visibleStart":994}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":49701} '
                    '{"end":1000,"offsetTop":49550,"start":991,"totalHeight":50000,"visibleEnd":1000,"visibleStart":994}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":60000} '
                    '{"end":1000,"offsetTop":49550,"start":991,"totalHeight":50000,"visibleEnd":1000,"visibleStart":994}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":-50} '
                    '{"end":9,"offsetTop":0,"start":0,"totalHeight":50000,"visibleEnd":6,"visibleStart":0}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":500,"overscan":0} '
                    '{"end":16,"offsetTop":500,"start":10,"totalHeight":50000,"visibleEnd":16,"visibleStart":10}',
                    '{"viewportHeight":300,"itemHeight":50,"count":1000,"scrollTop":500,"overscan":10} '
                    '{"end":26,"offsetTop":0,"start":0,"totalHeight":50000,"visibleEnd":16,"visibleStart":10}',
                    '{"scrollTop":0,"viewportHeight":300,"itemHeight":50,"count":4} '
                    '{"end":4,"offsetTop":0,"start":0,"totalHeight":200,"visibleEnd":4,"visibleStart":0}',
                    '{"scrollTop":100,"viewportHeight":300,"itemHeight":50,"count":4} '
                    '{"end":4,"offsetTop":0,"start":0,"totalHeight":200,"visibleEnd":4,"visibleStart":0}',
                    '{"scrollTop":0,"viewportHeight":300,"itemHeight":50,"count":0} '
                    '{"end":0,"offsetTop":0,"start":0,"totalHeight":0,"visibleEnd":0,"visibleStart":0}',
                    '{"scrollTop":40,"viewportHeight":0,"itemHeight":20,"count":100,"overscan":1} '
                    '{"end":3,"offsetTop":20,"start":1,"totalHeight":2000,"visibleEnd":2,"visibleStart":2}',
                    '{"scrollTop":25,"viewportHeight":100,"itemHeight":30,"count":50} '
                    '{"end":8,"offsetTop":0,"start":0,"totalHeight":1500,"visibleEnd":5,"visibleStart":0}']},
      {'id': 'j20-height-index',
       'mode': 'js',
       'title': 'Индекс высот для списка с разной высотой',
       'statement': 'Напишите функцию createHeightIndex(heights) → { total(), offsetOf(i), indexAt(offset), '
                    'setHeight(i, h), range(scrollTop, viewportHeight, overscan = 2) }. offsetOf(i) — сумма '
                    'высот строк до i (offsetOf(0) = 0, offsetOf(n) = total). indexAt(offset) — индекс '
                    'строки, которая занимает позицию offset (строка i занимает [offsetOf(i), '
                    'offsetOf(i+1))); offset < 0 → 0; offset ≥ total → последний индекс (n − 1; для пустого '
                    'списка 0). Ищите бинарным поиском. setHeight меняет высоту строки (высоты ≥ 0). range → '
                    '{ start, end (не включая), offsetTop }: видимая область [scrollTop, scrollTop + '
                    'viewportHeight): первая строка — indexAt(scrollTop), последняя — строка, содержащая '
                    'позицию scrollTop + viewportHeight − 1 (но не меньше первой); start = max(0, первая − '
                    'overscan), end = min(n, последняя + 1 + overscan), offsetTop = offsetOf(start). Строки '
                    'нулевой высоты допустимы (indexAt возвращает первую строку с положительной высотой, '
                    'покрывающую offset).',
       'starter': 'function createHeightIndex(heights) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const x = createHeightIndex([30, 50, 20, 80, 40]);\n'
                 'console.log(x.total(), [0, 1, 2, 5].map((i) => x.offsetOf(i)).join());\n'
                 'for (const o of [-10, 0, 29, 30, 79, 80, 99, 100, 179, 180, 219, 220, 9999]) '
                 'console.log(o, x.indexAt(o));\n'
                 'const r = (s, v, o) => console.log(s, v, o, JSON.stringify(canon(x.range(s, v, o))));\n'
                 'r(0, 60, 0); r(0, 60, 2); r(75, 30, 1); r(100, 200, 0); r(100, 1000, 2); r(500, 100, 1); '
                 'r(30, 1, 0);\n'
                 'x.setHeight(1, 100); console.log(x.total(), x.offsetOf(2), x.indexAt(129), '
                 'x.indexAt(130)); x.setHeight(0, 0); console.log(x.total(), x.indexAt(0), x.indexAt(99), '
                 'x.indexAt(100));\n'
                 'const z = createHeightIndex([0, 0, 10, 0, 10]); console.log([0, 5, 9, 10, 15, 25].map((o) '
                 '=> z.indexAt(o)).join(), z.total());\n'
                 'const empty = createHeightIndex([]); console.log(empty.total(), empty.indexAt(5), '
                 'JSON.stringify(canon(empty.range(0, 100))), empty.offsetOf(0));\n'
                 'const big = createHeightIndex(Array.from({ length: 100000 }, (_, i) => 20 + (i % 7))); '
                 'console.log(big.total(), big.indexAt(1000000), big.offsetOf(50000), '
                 'JSON.stringify(canon(big.range(1234567, 800, 3))));\n'
                 'for (let i = 0; i < 2000; i++) big.setHeight(i * 7, 1); console.log(big.total(), '
                 'big.indexAt(1000000));\n',
       'hint': 'Префиксные суммы и бинарный поиск первого индекса, у которого prefix[i+1] > offset.',
       'expected': ['220 0,30,80,220',
                    '-10 0',
                    '0 0',
                    '29 0',
                    '30 1',
                    '79 1',
                    '80 2',
                    '99 2',
                    '100 3',
                    '179 3',
                    '180 4',
                    '219 4',
                    '220 4',
                    '9999 4',
                    '0 60 0 {"end":2,"offsetTop":0,"start":0}',
                    '0 60 2 {"end":4,"offsetTop":0,"start":0}',
                    '75 30 1 {"end":5,"offsetTop":0,"start":0}',
                    '100 200 0 {"end":5,"offsetTop":100,"start":3}',
                    '100 1000 2 {"end":5,"offsetTop":30,"start":1}',
                    '500 100 1 {"end":5,"offsetTop":100,"start":3}',
                    '30 1 0 {"end":2,"offsetTop":30,"start":1}',
                    '270 130 1 2',
                    '240 1 1 2',
                    '2,2,2,4,4,4 20',
                    '0 0 {"end":0,"offsetTop":0,"start":0} 0',
                    '2299995 43478 1149997 {"end":53715,"offsetTop":1234473,"start":53673}',
                    '2261995 45130']},
      {'id': 'j20-intersection',
       'mode': 'js',
       'title': 'Наблюдатель пересечений',
       'statement': 'Напишите функцию intersectionRatio(target, root, rootMargin = 0) и функцию '
                    'createObserver({ thresholds }). Прямоугольники — { x, y, w, h }. intersectionRatio: '
                    'корень расширяется на rootMargin с каждой стороны (число, может быть отрицательным), '
                    'результат — площадь пересечения / площадь цели (0, если площадь цели 0 или пересечения '
                    'нет; значение от 0 до 1). createObserver → { observe(id), update(id, ratio), '
                    'unobserve(id), onChange(fn) }. thresholds — массив порогов от 0 до 1 (отсортировать, [] '
                    '= [0]). Для каждого наблюдаемого id хранится индекс порога: idx(ratio) = число порогов, '
                    'которые ≤ ratio, при условии ratio > 0 или порог 0 есть и цель пересекается; упростим: '
                    'isIntersecting = ratio > 0, idx = isIntersecting ? (число порогов ≤ ratio) : 0. '
                    'update(id, ratio) вызывает подписчиков fn({ id, ratio, isIntersecting }), если idx '
                    'изменился по сравнению с прошлым (для первого update после observe — всегда вызывается, '
                    'даже если idx = 0). Не наблюдаемые id игнорируются; после unobserve состояние '
                    'забывается.',
       'starter': 'function intersectionRatio(target, root, rootMargin) {\n'
                  '}\n'
                  'function createObserver(options) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const T = (x, y, w, h) => ({ x, y, w, h }); const root = T(0, 0, 100, 100);\n'
                 'for (const [t, m] of [[T(10, 10, 20, 20), 0], [T(90, 90, 20, 20), 0], [T(-10, -10, 20, '
                 '20), 0], [T(100, 0, 10, 10), 0], [T(110, 0, 10, 10), 0], [T(110, 0, 10, 10), 20], [T(110, '
                 '0, 10, 10), 10], [T(0, 0, 0, 10), 0], [T(10, 10, 20, 20), -15], [T(10, 10, 20, 20), -20], '
                 '[T(-50, -50, 300, 300), 0], [T(50, 50, 100, 100), -40]]) console.log(JSON.stringify(t), m, '
                 'intersectionRatio(t, root, m));\n'
                 'const o = createObserver({ thresholds: [0.5, 0, 1] }); const log = []; o.onChange((e) => '
                 'log.push(`${e.id}:${e.ratio}:${e.isIntersecting}`));\n'
                 'o.update("a", 0.2); o.observe("a"); o.update("a", 0); o.update("a", 0); o.update("a", '
                 '0.1); o.update("a", 0.4); o.update("a", 0.5); o.update("a", 0.9); o.update("a", 1); '
                 'o.update("a", 1); o.update("a", 0.3); o.update("a", 0); console.log(log.join(" "));\n'
                 'log.length = 0; const p = createObserver({ thresholds: [] }); p.onChange((e) => '
                 'log.push(e.ratio)); p.observe("x"); p.update("x", 0); p.update("x", 0.01); p.update("x", '
                 '0.9); p.update("x", 0); console.log(log.join());\n'
                 'log.length = 0; const q = createObserver({ thresholds: [0.25, 0.75] }); q.onChange((e) => '
                 'log.push(e.ratio)); q.observe("x"); q.observe("y"); q.update("x", 0.3); q.update("y", '
                 '0.3); q.update("x", 0.6); q.update("x", 0.8); q.unobserve("x"); q.update("x", 0.1); '
                 'q.observe("x"); q.update("x", 0.1); console.log(log.join());\n',
       'hint': 'Хранить для каждого id последний индекс порога; пересечение двух отрезков считать по каждой '
               'оси.',
       'expected': ['{"x":10,"y":10,"w":20,"h":20} 0 1',
                    '{"x":90,"y":90,"w":20,"h":20} 0 0.25',
                    '{"x":-10,"y":-10,"w":20,"h":20} 0 0.25',
                    '{"x":100,"y":0,"w":10,"h":10} 0 0',
                    '{"x":110,"y":0,"w":10,"h":10} 0 0',
                    '{"x":110,"y":0,"w":10,"h":10} 20 1',
                    '{"x":110,"y":0,"w":10,"h":10} 10 0',
                    '{"x":0,"y":0,"w":0,"h":10} 0 0',
                    '{"x":10,"y":10,"w":20,"h":20} -15 0.5625',
                    '{"x":10,"y":10,"w":20,"h":20} -20 0.25',
                    '{"x":-50,"y":-50,"w":300,"h":300} 0 0.1111111111111111',
                    '{"x":50,"y":50,"w":100,"h":100} -40 0.01',
                    'a:0:false a:0.1:true a:0.5:true a:1:true a:0.3:true a:0:false',
                    '0,0.01,0',
                    '0.3,0.3,0.8,0.1']},
      {'id': 'j20-srcset',
       'mode': 'js',
       'title': 'Выбор картинки из srcset',
       'statement': 'Напишите функции parseSrcset(str) и pickImage(candidates, { slotWidth, dpr }). '
                    'parseSrcset: кандидаты через запятую (запятая внутри адреса, например в «data:» нет — '
                    'считаем, что адреса без запятых), каждый — «адрес [дескриптор]», дескриптор «480w» или '
                    '«2x»; без дескриптора — «1x». Результат — массив { url, w } или { url, x }. Если в '
                    'списке смешаны w и x или есть неверный дескриптор — Error. Лишние пробелы допустимы. '
                    'pickImage: нужная ширина need = slotWidth × dpr; для w-кандидатов — самый узкий из тех, '
                    'у которых w ≥ need; если таких нет — самый широкий; для x-кандидатов — с наименьшим x ≥ '
                    'dpr, иначе наибольшим; при равенстве — первый в списке. Возвращает url. Пустой список — '
                    'null.',
       'starter': 'function parseSrcset(str) {\n}\nfunction pickImage(candidates, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const S = (s) => { try { return JSON.stringify(parseSrcset(s).map(canon)); } catch (e) { '
                 'return "ERR:" + e.message; } };\n'
                 'console.log(S("a-480.jpg 480w, a-960.jpg 960w,a-1920.jpg   1920w")); console.log(S("a.jpg, '
                 'a@2x.jpg 2x , a@1.5x.jpg 1.5x")); console.log(S("")); console.log(S("a.jpg 480w, b.jpg '
                 '2x")); console.log(S("a.jpg 480")); console.log(S("a.jpg 480w extra"));\n'
                 'const W = parseSrcset("s.jpg 480w, m.jpg 960w, l.jpg 1920w");\n'
                 'for (const [slot, dpr] of [[300, 1], [480, 1], [481, 1], [300, 2], [480, 2], [960, 2], '
                 '[1000, 2], [5000, 1], [0, 1]]) console.log(slot, dpr, pickImage(W, { slotWidth: slot, dpr '
                 '}));\n'
                 'const X = parseSrcset("a.jpg, a2.jpg 2x, a3.jpg 3x"); for (const dpr of [1, 1.5, 2, 2.5, '
                 '3, 4]) console.log(dpr, pickImage(X, { slotWidth: 100, dpr }));\n'
                 'console.log(pickImage([], { slotWidth: 1, dpr: 1 }), pickImage(parseSrcset("a.jpg 500w, '
                 'b.jpg 500w"), { slotWidth: 500, dpr: 1 }), pickImage(parseSrcset("only.jpg"), { slotWidth: '
                 '99, dpr: 3 }), pickImage(parseSrcset("l.jpg 900w, s.jpg 300w"), { slotWidth: 100, dpr: 1 '
                 '}));\n',
       'hint': 'Выберите ключ w или x по первому кандидату; отфильтруйте «достаточных» и возьмите '
               'наименьшего.',
       'expected': ['[{"url":"a-480.jpg","w":480},{"url":"a-960.jpg","w":960},{"url":"a-1920.jpg","w":1920}]',
                    '[{"url":"a.jpg","x":1},{"url":"a@2x.jpg","x":2},{"url":"a@1.5x.jpg","x":1.5}]',
                    '[]',
                    'ERR:Смешаны w и x',
                    'ERR:Неверный дескриптор: 480',
                    'ERR:Лишнее в кандидате: a.jpg 480w extra',
                    '300 1 s.jpg',
                    '480 1 s.jpg',
                    '481 1 m.jpg',
                    '300 2 m.jpg',
                    '480 2 m.jpg',
                    '960 2 l.jpg',
                    '1000 2 l.jpg',
                    '5000 1 l.jpg',
                    '0 1 s.jpg',
                    '1 a.jpg',
                    '1.5 a2.jpg',
                    '2 a2.jpg',
                    '2.5 a3.jpg',
                    '3 a3.jpg',
                    '4 a3.jpg',
                    'null a.jpg only.jpg s.jpg']},
      {'id': 'j20-sizes',
       'mode': 'js',
       'title': 'Разбор атрибута sizes',
       'statement': 'Напишите функцию resolveSizes(sizes, viewportWidth) → ширина слота в пикселях (целое, '
                    'округление Math.round). sizes — как в HTML: список через запятую «условие длина»; '
                    'условие — одно или несколько медиавыражений в скобках, соединённых «and»: (min-width: '
                    '600px), (max-width: 800px); последний элемент без условия — значение по умолчанию. '
                    'Берётся первый элемент, условие которого выполняется (min-width: ≤ ширины окна, '
                    'max-width: ≥ ширины окна, сравнение включительное). Длина: «NNpx», «NNvw» (доля ширины '
                    'окна) или calc(...) вида «calc(100vw - 32px)» / «calc(50vw + 10px)» (одно сложение или '
                    'вычитание двух слагаемых в vw/px). Если ни одно условие не подошло и нет значения по '
                    'умолчанию — 100vw. Пустая или отсутствующая строка — тоже 100vw. Нераспознанная длина — '
                    'Error.',
       'starter': 'function resolveSizes(sizes, viewportWidth) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const S = "(max-width: 600px) 100vw, (max-width: 1000px) 50vw, 33.3vw";\n'
                 'for (const w of [320, 600, 601, 1000, 1001, 1440]) console.log(w, resolveSizes(S, w));\n'
                 'const C = "(min-width: 800px) calc(100vw - 240px), calc(100vw - 32px)"; for (const w of '
                 '[400, 799, 800, 1200]) console.log(w, resolveSizes(C, w));\n'
                 'const R = "(min-width: 500px) and (max-width: 900px) 400px, (min-width: 901px) 600px"; for '
                 '(const w of [400, 500, 900, 901, 2000]) console.log(w, resolveSizes(R, w));\n'
                 'console.log(resolveSizes("", 777), resolveSizes(undefined, 777), resolveSizes("   ", 500), '
                 'resolveSizes("300px", 1000), resolveSizes("(min-width: 2000px) 10px", 100), '
                 'resolveSizes("calc(50vw + 10px)", 333), resolveSizes("calc(100vw - 32px)", 100.4), '
                 'resolveSizes("12.5vw", 100));\n'
                 'try { resolveSizes("(max-width: 600px) 10em", 100); } catch (e) { console.log(e.message); '
                 '}\n',
       'hint': 'Разбирайте список с учётом скобок: запятая внутри calc() не разделитель; для условий — '
               'регулярка по (min|max)-width.',
       'expected': ['320 320',
                    '600 600',
                    '601 301',
                    '1000 500',
                    '1001 333',
                    '1440 480',
                    '400 368',
                    '799 767',
                    '800 560',
                    '1200 960',
                    '400 400',
                    '500 400',
                    '900 400',
                    '901 600',
                    '2000 600',
                    '777 777 500 300 100 177 68 13',
                    'Нераспознанная длина: 10em']},
      {'id': 'j20-font-display',
       'mode': 'js',
       'title': 'font-display: что видит пользователь',
       'statement': 'Напишите функцию fontState(display, t, loadedAt) → «invisible» (место под текст пустое) '
                    '| «fallback» (запасной шрифт) | «web» (загруженный шрифт). t — время в мс с момента, '
                    'когда шрифт понадобился; loadedAt — через сколько мс шрифт стал доступен (null — '
                    'никогда). У режимов есть период блокировки (текст невидим) и период подмены '
                    '(показывается запасной шрифт, который заменяется загруженным, как только тот готов): '
                    'auto и block — блокировка 3000 мс, подмена бесконечная; swap — блокировка 0, подмена '
                    'бесконечная; fallback — блокировка 100 мс, подмена до t = 3100 включительно; optional — '
                    'блокировка 100 мс, подмены нет. Границы периодов включительны (t = 100 — ещё '
                    'блокировка). Правила: во время блокировки — «web», если шрифт уже доступен (loadedAt ≤ '
                    't), иначе «invisible»; во время подмены — «web», если доступен, иначе «fallback»; после '
                    'подмены шрифт принимается, только если стал доступен не позже её конца (loadedAt ≤ '
                    'конец подмены), тогда «web», иначе всегда «fallback». Для optional «концом подмены» '
                    'считается конец блокировки: шрифт, не успевший за 100 мс, не применяется никогда. '
                    'Неизвестный режим — Error с message «Неизвестный режим: <имя>».',
       'starter': 'function fontState(display, t, loadedAt) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const times = [0, 50, 100, 101, 1000, 3000, 3001, 3100, 3101, 10000];\n'
                 'for (const d of ["auto", "block", "swap", "fallback", "optional"]) for (const loaded of '
                 '[null, 40, 500, 4000]) console.log(d.padEnd(9), String(loaded).padEnd(5), times.map((t) => '
                 '({ invisible: "I", fallback: "F", web: "W" }[fontState(d, t, loaded)])).join(""));\n'
                 'try { fontState("zzz", 0, null); } catch (e) { console.log(e.message); }\n',
       'hint': 'Таблица периодов: блокировка, затем подмена; шрифт, загруженный вне разрешённых периодов, не '
               'применяется.',
       'expected': ['auto      null  IIIIIIFFFF',
                    'auto      40    IWWWWWWWWW',
                    'auto      500   IIIIWWWWWW',
                    'auto      4000  IIIIIIFFFW',
                    'block     null  IIIIIIFFFF',
                    'block     40    IWWWWWWWWW',
                    'block     500   IIIIWWWWWW',
                    'block     4000  IIIIIIFFFW',
                    'swap      null  FFFFFFFFFF',
                    'swap      40    FWWWWWWWWW',
                    'swap      500   FFFFWWWWWW',
                    'swap      4000  FFFFFFFFFW',
                    'fallback  null  IIIFFFFFFF',
                    'fallback  40    IWWWWWWWWW',
                    'fallback  500   IIIFWWWWWW',
                    'fallback  4000  IIIFFFFFFF',
                    'optional  null  IIIFFFFFFF',
                    'optional  40    IWWWWWWWWW',
                    'optional  500   IIIFFFFFFF',
                    'optional  4000  IIIFFFFFFF',
                    'Неизвестный режим: zzz']},
      {'id': 'j20-hints',
       'mode': 'js',
       'title': 'Подбор resource hints',
       'statement': 'Напишите функцию planHints(resources, pageOrigin) → { preconnect, preload, dnsPrefetch '
                    '}. resources — массив { url (абсолютный), type: '
                    '"script"|"style"|"font"|"image"|"fetch", critical (boolean), discoveredBy: '
                    '"html"|"css"|"js" }. preload: для ресурсов critical, обнаруженных не в html (то есть '
                    'браузер узнает о них поздно) — { href: url, as: type }, у шрифтов и fetch добавляется '
                    'crossorigin: true; в порядке появления, не больше 4 (лишние отбрасываются), дубликаты '
                    'по url — один раз. preconnect: уникальные источники сторонних (≠ pageOrigin) критичных '
                    'ресурсов в порядке первого появления, не больше 3; для источника crossorigin: true, '
                    'если хотя бы один из его критичных ресурсов — шрифт или fetch: элемент { origin, '
                    'crossorigin }. dnsPrefetch: источники сторонних некритичных ресурсов (в порядке '
                    'появления), которых нет в preconnect, без повторов.',
       'starter': 'function planHints(resources, pageOrigin) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const P = "https://app.ru"; const R = (url, type, critical, discoveredBy) => ({ url, type, '
                 'critical, discoveredBy });\n'
                 'const show = (rs) => console.log(JSON.stringify(canon(planHints(rs, P))));\n'
                 'show([R("https://app.ru/main.js", "script", true, "html"), R("https://app.ru/app.css", '
                 '"style", true, "html"), R("https://app.ru/hero.jpg", "image", true, "css"), '
                 'R("https://app.ru/f.woff2", "font", true, "css")]);\n'
                 'show([R("https://cdn.ru/lib.js", "script", true, "html"), R("https://fonts.ru/a.woff2", '
                 '"font", true, "css"), R("https://fonts.ru/b.woff2", "font", true, "css"), '
                 'R("https://cdn.ru/x.js", "script", true, "js"), R("https://ads.ru/a.js", "script", false, '
                 '"js"), R("https://cdn.ru/img.png", "image", false, "html"), R("https://stats.ru/s.js", '
                 '"script", false, "html")]);\n'
                 'show([R("https://a.ru/1", "fetch", true, "js"), R("https://b.ru/2", "script", true, '
                 '"html"), R("https://c.ru/3", "script", true, "html"), R("https://d.ru/4", "script", true, '
                 '"html"), R("https://e.ru/5", "script", false, "html"), R("https://d.ru/6", "script", '
                 'false, "html")]);\n'
                 'show(Array.from({ length: 7 }, (_, i) => R(`https://app.ru/late${i % 6}.js`, "script", '
                 'true, "js"))); show([]);\n'
                 'show([R("https://app.ru/x.js", "script", true, "js"), R("https://app.ru/x.js", "script", '
                 'true, "css")]);\n',
       'hint': 'Три независимых прохода по ресурсам; Map источник → нужен ли crossorigin.',
       'expected': ['{"dnsPrefetch":[],"preconnect":[],"preload":[{"as":"image","href":"https://app.ru/hero.jpg"},{"as":"font","crossorigin":true,"href":"https://app.ru/f.woff2"}]}',
                    '{"dnsPrefetch":["https://ads.ru","https://stats.ru"],"preconnect":[{"crossorigin":false,"origin":"https://cdn.ru"},{"crossorigin":true,"origin":"https://fonts.ru"}],"preload":[{"as":"font","crossorigin":true,"href":"https://fonts.ru/a.woff2"},{"as":"font","crossorigin":true,"href":"https://fonts.ru/b.woff2"},{"as":"script","href":"https://cdn.ru/x.js"}]}',
                    '{"dnsPrefetch":["https://e.ru","https://d.ru"],"preconnect":[{"crossorigin":true,"origin":"https://a.ru"},{"crossorigin":false,"origin":"https://b.ru"},{"crossorigin":false,"origin":"https://c.ru"}],"preload":[{"as":"fetch","crossorigin":true,"href":"https://a.ru/1"}]}',
                    '{"dnsPrefetch":[],"preconnect":[],"preload":[{"as":"script","href":"https://app.ru/late0.js"},{"as":"script","href":"https://app.ru/late1.js"},{"as":"script","href":"https://app.ru/late2.js"},{"as":"script","href":"https://app.ru/late3.js"}]}',
                    '{"dnsPrefetch":[],"preconnect":[],"preload":[]}',
                    '{"dnsPrefetch":[],"preconnect":[],"preload":[{"as":"script","href":"https://app.ru/x.js"}]}']},
      {'id': 'j20-critical-path',
       'mode': 'js',
       'title': 'Критический путь загрузки',
       'statement': 'Напишите функцию criticalPath(tasks): tasks — массив { id, duration, deps: [id…] } '
                    '(зависимости: пока не завершатся все deps, задача не начнётся; параллелизм не '
                    'ограничен). Результат — { length, path, finish: { id: время завершения } }: length — '
                    'время завершения всего графа (максимум finish), path — цепочка id критического пути от '
                    'начала к концу (зависимости, задающие самую позднюю готовность на каждом шаге; при '
                    'равенстве — тот id, что раньше по алфавиту; среди конечных задач с максимальным finish '
                    '— по алфавиту). Если зависимость ссылается на несуществующий id — Error «Неизвестная '
                    'зависимость: <id>»; цикл — Error «Цикл зависимостей». Пустой список — { length: 0, '
                    'path: [], finish: {} }.',
       'starter': 'function criticalPath(tasks) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const T = (id, duration, deps = []) => ({ id, duration, deps });\n'
                 'const show = (ts) => { try { console.log(JSON.stringify(canon(criticalPath(ts)))); } catch '
                 '(e) { console.log("ERR:" + e.message); } };\n'
                 'show([T("html", 100), T("css", 200, ["html"]), T("js", 300, ["html"]), T("img", 150, '
                 '["css"]), T("font", 80, ["css"]), T("app", 50, ["js", "css"])]);\n'
                 'show([T("a", 10), T("b", 10), T("c", 5, ["a", "b"])]); show([T("b", 10), T("a", 10), '
                 'T("z", 0, ["b", "a"])]); show([]); show([T("only", 7)]);\n'
                 'show([T("a", 1, ["b"]), T("b", 1, ["a"])]); show([T("a", 1, ["ghost"])]); show([T("a", 5), '
                 'T("b", 5, ["a"]), T("c", 5, ["b"]), T("x", 15)]);\n'
                 'show([T("c", 3, ["b"]), T("b", 4, ["a"]), T("a", 5), T("d", 0, ["a"])]);\n'
                 'const chain = Array.from({ length: 2000 }, (_, i) => T("n" + String(i).padStart(4, "0"), '
                 '1, i ? ["n" + String(i - 1).padStart(4, "0")] : [])); const r = criticalPath(chain); '
                 'console.log(r.length, r.path.length, r.path[0], r.path.at(-1));\n',
       'hint': 'Мемоизируйте время завершения (обход в глубину с цветами для цикла) и храните «через какую '
               'зависимость пришли».',
       'expected': ['{"finish":{"app":450,"css":300,"font":380,"html":100,"img":450,"js":400},"length":450,"path":["html","js","app"]}',
                    '{"finish":{"a":10,"b":10,"c":15},"length":15,"path":["a","c"]}',
                    '{"finish":{"a":10,"b":10,"z":10},"length":10,"path":["a"]}',
                    '{"finish":{},"length":0,"path":[]}',
                    '{"finish":{"only":7},"length":7,"path":["only"]}',
                    'ERR:Цикл зависимостей',
                    'ERR:Неизвестная зависимость: ghost',
                    '{"finish":{"a":5,"b":10,"c":15,"x":15},"length":15,"path":["a","b","c"]}',
                    '{"finish":{"a":5,"b":9,"c":12,"d":5},"length":12,"path":["a","b","c"]}',
                    '2000 2000 n0000 n1999']},
      {'id': 'j20-simulate-load',
       'mode': 'js',
       'title': 'Симуляция загрузки с ограничением соединений',
       'statement': 'Напишите функцию simulateLoad(resources, { maxPerOrigin = Infinity }): resources — { '
                    'id, origin, duration, deps }. Ресурс начинается, когда завершены все его deps и на его '
                    'origin есть свободный слот (одновременно у одного origin выполняется не более '
                    'maxPerOrigin ресурсов). Готовые ресурсы ждут слот в порядке (время готовности, порядок '
                    'в исходном списке). Начало — в момент, когда стали готовы и слот свободен; слот '
                    'освобождается в момент завершения. При одновременном завершении и готовности слот '
                    'считается свободным (сначала обрабатываются завершения). Результат: { finish: { id: t '
                    '}, total } (total — максимум finish, 0 для пустого). Цикл или неизвестная зависимость — '
                    'Error.',
       'starter': 'function simulateLoad(resources, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const R = (id, origin, duration, deps = []) => ({ id, origin, duration, deps });\n'
                 'const show = (rs, o) => { try { const r = simulateLoad(rs, o); console.log(r.total, '
                 'JSON.stringify(canon(r.finish))); } catch (e) { console.log("ERR:" + e.message); } };\n'
                 'const page = [R("html", "a", 100), R("css", "a", 50, ["html"]), R("js1", "a", 80, '
                 '["html"]), R("js2", "a", 80, ["html"]), R("img1", "a", 60, ["html"]), R("img2", "a", 60, '
                 '["html"]), R("img3", "a", 60, ["html"]), R("font", "b", 70, ["css"])];\n'
                 'show(page); show(page, { maxPerOrigin: 6 }); show(page, { maxPerOrigin: 2 }); show(page, { '
                 'maxPerOrigin: 1 });\n'
                 'show([]); show([R("x", "a", 10), R("y", "a", 10), R("z", "a", 10)], { maxPerOrigin: 2 }); '
                 'show([R("x", "a", 10, ["y"]), R("y", "a", 10, ["x"])]); show([R("x", "a", 10, '
                 '["ghost"])]);\n'
                 'show([R("a1", "a", 30), R("b1", "b", 10), R("b2", "b", 10, ["a1"]), R("b3", "b", 10)], { '
                 'maxPerOrigin: 1 }); show([R("r", "a", 0), R("s", "a", 5, ["r"])], { maxPerOrigin: 1 });\n'
                 'show([R("x", "a", 10), R("y", "a", 10, ["x"]), R("z", "a", 10, ["x"]), R("w", "a", 10, '
                 '["y", "z"])], { maxPerOrigin: 1 });\n',
       'hint': 'Событийная симуляция: храните время, занятые слоты по origin и очередь готовых; переходите к '
               'ближайшему событию.',
       'expected': ['220 '
                    '{"css":150,"font":220,"html":100,"img1":160,"img2":160,"img3":160,"js1":180,"js2":180}',
                    '220 '
                    '{"css":150,"font":220,"html":100,"img1":160,"img2":160,"img3":160,"js1":180,"js2":180}',
                    '300 '
                    '{"css":150,"font":220,"html":100,"img1":240,"img2":290,"img3":300,"js1":180,"js2":230}',
                    '490 '
                    '{"css":150,"font":220,"html":100,"img1":370,"img2":430,"img3":490,"js1":230,"js2":310}',
                    '0 {}',
                    '20 {"x":10,"y":10,"z":20}',
                    'ERR:Цикл зависимостей',
                    'ERR:Неизвестная зависимость: ghost',
                    '40 {"a1":30,"b1":10,"b2":40,"b3":20}',
                    '5 {"r":0,"s":5}',
                    '40 {"w":40,"x":10,"y":20,"z":30}']},
      {'id': 'j20-budgets',
       'mode': 'js',
       'title': 'Бюджеты производительности',
       'statement': 'Напишите функцию checkBudgets(stats, budgets) → { ok, violations }. stats = { files: [{ '
                    'name, type ("js"|"css"|"img"|…), bytes }], metrics: { lcp: …, … } }. budgets = { '
                    'total?, byType?: { js: 200000, … }, perFile?: [{ pattern: RegExp, max }], metrics?: { '
                    'lcp: 2500, … } }. Нарушение — превышение лимита (строго больше). Список нарушений в '
                    'порядке: total; byType в порядке ключей budgets.byType; perFile — для каждого правила '
                    'по порядку и для каждого подходящего файла (pattern.test(name)) по порядку файлов; '
                    'metrics в порядке ключей budgets.metrics (метрики, которых нет в stats, пропускаются). '
                    'Элемент: { kind: "total"|"type"|"file"|"metric", name (для total — «total»; тип; имя '
                    'файла; имя метрики), actual, limit, over (процент превышения, округлённый до 1 знака) , '
                    'severity: over ≤ 10 → «warn», иначе «error» }. ok — нет нарушений с severity error.',
       'starter': 'function checkBudgets(stats, budgets) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const files = [{ name: "main.js", type: "js", bytes: 210000 }, { name: "vendor.js", type: '
                 '"js", bytes: 150000 }, { name: "app.css", type: "css", bytes: 40000 }, { name: "hero.png", '
                 'type: "img", bytes: 300000 }, { name: "icon.png", type: "img", bytes: 12000 }];\n'
                 'const show = (s, b) => { const r = checkBudgets(s, b); console.log(r.ok, '
                 'r.violations.length); for (const v of r.violations) console.log(" ", '
                 'JSON.stringify(canon(v))); };\n'
                 'show({ files, metrics: { lcp: 2600, cls: 0.05 } }, { total: 700000, byType: { js: 300000, '
                 'css: 50000, img: 400000 }, perFile: [{ pattern: /\\.js$/, max: 200000 }, { pattern: '
                 '/^hero/, max: 250000 }], metrics: { lcp: 2500, cls: 0.1, inp: 200 } });\n'
                 'show({ files, metrics: {} }, {}); show({ files: [], metrics: {} }, { total: 0, byType: { '
                 'js: 0 } });\n'
                 'show({ files, metrics: { lcp: 2750 } }, { total: 712000, metrics: { lcp: 2500 } }); show({ '
                 'files, metrics: { lcp: 2751 } }, { metrics: { lcp: 2500 } }); show({ files, metrics: { '
                 'lcp: 2500 } }, { metrics: { lcp: 2500 } });\n'
                 'show({ files }, { metrics: { lcp: 1 }, perFile: [{ pattern: /png$/, max: 20000 }] });\n',
       'hint': 'Вспомогательная add(kind, name, actual, limit) избавит от дублирования; порядок проверок — '
               'как в условии.',
       'expected': ['false 5',
                    '  '
                    '{"actual":712000,"kind":"total","limit":700000,"name":"total","over":1.7,"severity":"warn"}',
                    '  '
                    '{"actual":360000,"kind":"type","limit":300000,"name":"js","over":20,"severity":"error"}',
                    '  '
                    '{"actual":210000,"kind":"file","limit":200000,"name":"main.js","over":5,"severity":"warn"}',
                    '  '
                    '{"actual":300000,"kind":"file","limit":250000,"name":"hero.png","over":20,"severity":"error"}',
                    '  {"actual":2600,"kind":"metric","limit":2500,"name":"lcp","over":4,"severity":"warn"}',
                    'true 0',
                    'true 0',
                    'true 1',
                    '  {"actual":2750,"kind":"metric","limit":2500,"name":"lcp","over":10,"severity":"warn"}',
                    'true 1',
                    '  {"actual":2751,"kind":"metric","limit":2500,"name":"lcp","over":10,"severity":"warn"}',
                    'true 0',
                    'false 1',
                    '  '
                    '{"actual":300000,"kind":"file","limit":20000,"name":"hero.png","over":1400,"severity":"error"}']},
      {'id': 'j20-snapshot-diff',
       'mode': 'js',
       'title': 'Сравнение снимков памяти',
       'statement': 'Напишите функции diffSnapshots(a, b) и findLeakSuspects(snapshots). Снимок — массив '
                    'объектов { type, size } (число байт). diffSnapshots → массив { type, countA, countB, '
                    'countDelta, bytesDelta } для типов, у которых число объектов или общий размер выросли '
                    '(countDelta > 0 или bytesDelta > 0), отсортированный по bytesDelta по убыванию, затем '
                    'по имени типа. findLeakSuspects(snapshots): для снимков (не меньше 3) вернуть типы, у '
                    'которых число объектов растёт строго при каждом переходе между соседними снимками (в '
                    'каждом снимке тип присутствует; отсутствие = 0, и 0 → положительное тоже рост), с полем '
                    'growth — серия счётчиков; результат — [{ type, counts }] по возрастанию имени типа. '
                    'Если снимков меньше 3 — [].',
       'starter': 'function diffSnapshots(a, b) {\n}\nfunction findLeakSuspects(snapshots) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const mk = (spec) => Object.entries(spec).flatMap(([type, [n, size]]) => Array.from({ '
                 'length: n }, () => ({ type, size })));\n'
                 'const s1 = mk({ Listener: [10, 32], String: [100, 20], Detached: [2, 5000] }), s2 = mk({ '
                 'Listener: [20, 32], String: [90, 20], Detached: [2, 5000], Closure: [5, 100] }), s3 = mk({ '
                 'Listener: [30, 32], String: [95, 20], Detached: [4, 5000], Closure: [5, 100] }), s4 = mk({ '
                 'Listener: [45, 32], String: [200, 20], Detached: [6, 5000], Closure: [3, 100] });\n'
                 'for (const [a, b] of [[s1, s2], [s2, s3], [s1, s4], [s4, s1], [s1, s1], [[], s1]]) '
                 'console.log(JSON.stringify(diffSnapshots(a, b).map(canon)));\n'
                 'console.log(JSON.stringify(findLeakSuspects([s1, s2, s3, s4]).map(canon)), '
                 'JSON.stringify(findLeakSuspects([s1, s2])), JSON.stringify(findLeakSuspects([s1, s2, '
                 's3]).map(canon)), JSON.stringify(findLeakSuspects([[], mk({ X: [1, 1] }), mk({ X: [2, 1] '
                 '})]).map(canon)), JSON.stringify(findLeakSuspects([s1, s1, s1])));\n'
                 'console.log(JSON.stringify(diffSnapshots(mk({ A: [1, 10], B: [1, 10] }), mk({ A: [1, 10], '
                 'B: [1, 10], C: [1, 10], D: [1, 10] })).map((x) => x.type)));\n'
                 'console.log(JSON.stringify(diffSnapshots([{ type: "T", size: 5 }], [{ type: "T", size: 9 '
                 '}]).map(canon)));\n',
       'hint': 'Сгруппируйте объекты по типу в Map {count, bytes}; сравнение двух карт и серия карт.',
       'expected': ['[{"bytesDelta":500,"countA":0,"countB":5,"countDelta":5,"type":"Closure"},{"bytesDelta":320,"countA":10,"countB":20,"countDelta":10,"type":"Listener"}]',
                    '[{"bytesDelta":10000,"countA":2,"countB":4,"countDelta":2,"type":"Detached"},{"bytesDelta":320,"countA":20,"countB":30,"countDelta":10,"type":"Listener"},{"bytesDelta":100,"countA":90,"countB":95,"countDelta":5,"type":"String"}]',
                    '[{"bytesDelta":20000,"countA":2,"countB":6,"countDelta":4,"type":"Detached"},{"bytesDelta":2000,"countA":100,"countB":200,"countDelta":100,"type":"String"},{"bytesDelta":1120,"countA":10,"countB":45,"countDelta":35,"type":"Listener"},{"bytesDelta":300,"countA":0,"countB":3,"countDelta":3,"type":"Closure"}]',
                    '[]',
                    '[]',
                    '[{"bytesDelta":10000,"countA":0,"countB":2,"countDelta":2,"type":"Detached"},{"bytesDelta":2000,"countA":0,"countB":100,"countDelta":100,"type":"String"},{"bytesDelta":320,"countA":0,"countB":10,"countDelta":10,"type":"Listener"}]',
                    '[{"counts":[10,20,30,45],"type":"Listener"}] [] '
                    '[{"counts":[10,20,30],"type":"Listener"}] [{"counts":[0,1,2],"type":"X"}] []',
                    '["C","D"]',
                    '[{"bytesDelta":4,"countA":1,"countB":1,"countDelta":0,"type":"T"}]']},
      {'id': 'j20-listener-tracker',
       'mode': 'js',
       'title': 'Трекер утечек слушателей',
       'statement': 'Напишите функцию trackListeners(target) → { leaks(), dispose() }. target — объект с '
                    'методами addEventListener(type, fn, options) и removeEventListener(type, fn, options). '
                    'Трекер оборачивает эти методы (подмена на экземпляре target, вызывая оригиналы) и ведёт '
                    'учёт активных слушателей по ключу (type, fn, capture), где capture = options === true '
                    'или options?.capture === true. Повторное добавление того же ключа DOM игнорирует — '
                    'трекер не должен учитывать его дважды (но оригинальный метод всё равно вызывается). '
                    'removeEventListener снимает учёт по ключу (capture учитывается). Опция once: слушатель '
                    'считается снятым после первого срабатывания, но срабатывание трекер не видит, поэтому '
                    'для once-слушателей трекер сам оборачивает fn и снимает учёт, когда обёртка вызвана '
                    '(вызвав исходный fn); оригинальному addEventListener передаётся обёртка, а '
                    'removeEventListener(type, fn) должен находить обёртку. leaks() → [{ type, capture, name '
                    '}] в порядке добавления (name — fn.name или «anonymous»). dispose() восстанавливает '
                    'оригинальные методы и возвращает список утечек (как leaks()) на тот момент.',
       'starter': 'function trackListeners(target) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const mkTarget = () => { const l = []; return { l, addEventListener(type, fn, o) { const '
                 'capture = o === true || o?.capture === true; if (!l.some((x) => x.type === type && x.fn '
                 '=== fn && x.capture === capture)) l.push({ type, fn, capture, once: !!o?.once }); }, '
                 'removeEventListener(type, fn, o) { const capture = o === true || o?.capture === true; '
                 'const i = l.findIndex((x) => x.type === type && x.fn === fn && x.capture === capture); if '
                 '(i !== -1) l.splice(i, 1); }, fire(type) { for (const x of [...l]) if (x.type === type) { '
                 'if (x.once) l.splice(l.indexOf(x), 1); x.fn.call(this, { type }); } } }; };\n'
                 'const t = mkTarget(); const tr = trackListeners(t); const show = (l) => '
                 'JSON.stringify(l.map(canon));\n'
                 'function onClick() {} const onKey = () => {}; const log = [];\n'
                 't.addEventListener("click", onClick); t.addEventListener("click", onClick); '
                 't.addEventListener("click", onClick, true); t.addEventListener("keydown", onKey, { '
                 'capture: true }); t.addEventListener("scroll", (e) => log.push("scroll"), { passive: true '
                 '});\n'
                 'console.log(show(tr.leaks()), t.l.length);\n'
                 't.removeEventListener("click", onClick); console.log(show(tr.leaks())); '
                 't.removeEventListener("click", onClick, false); t.removeEventListener("click", onClick, { '
                 'capture: true }); t.removeEventListener("nope", onClick); console.log(show(tr.leaks()), '
                 't.l.length);\n'
                 't.addEventListener("tap", function once1() { log.push("once1"); }, { once: true }); const '
                 'o2 = () => log.push("once2"); t.addEventListener("tap", o2, { once: true }); '
                 'console.log(tr.leaks().length); t.fire("tap"); console.log(log.join(), tr.leaks().length, '
                 't.l.length);\n'
                 'const o3 = () => log.push("o3"); t.addEventListener("x", o3, { once: true }); '
                 't.removeEventListener("x", o3); t.fire("x"); console.log(log.join(), show(tr.leaks()), '
                 't.l.filter((x) => x.type === "x").length);\n'
                 'const final = tr.dispose(); console.log(show(final), t.addEventListener === '
                 'Object.getPrototypeOf(t).addEventListener || typeof t.addEventListener); const before = '
                 'tr.leaks().length; t.addEventListener("later", onClick); console.log(before, '
                 'tr.leaks().length, t.l.length);\n',
       'hint': 'Подмените методы на экземпляре; учёт ведите массивом {type, fn, capture, wrapped}; для once '
               'передавайте обёртку.',
       'expected': ['[{"capture":false,"name":"onClick","type":"click"},{"capture":true,"name":"onClick","type":"click"},{"capture":true,"name":"onKey","type":"keydown"},{"capture":false,"name":"anonymous","type":"scroll"}] '
                    '4',
                    '[{"capture":true,"name":"onClick","type":"click"},{"capture":true,"name":"onKey","type":"keydown"},{"capture":false,"name":"anonymous","type":"scroll"}]',
                    '[{"capture":true,"name":"onKey","type":"keydown"},{"capture":false,"name":"anonymous","type":"scroll"}] '
                    '2',
                    '4',
                    'once1,once2 2 2',
                    'once1,once2 '
                    '[{"capture":true,"name":"onKey","type":"keydown"},{"capture":false,"name":"anonymous","type":"scroll"}] '
                    '0',
                    '[{"capture":true,"name":"onKey","type":"keydown"},{"capture":false,"name":"anonymous","type":"scroll"}] '
                    'function',
                    '2 2 3']},
      {'id': 'j20-memoize-lru',
       'mode': 'js',
       'title': 'Мемоизация с вытеснением LRU',
       'statement': 'Напишите функцию memoizeLRU(fn, { max = 100, keyFn = (...args) => JSON.stringify(args) '
                    '} = {}) → memoized. memoized(...args): ключ = keyFn(...args); при попадании '
                    'возвращается сохранённое значение и запись становится «самой свежей»; при промахе '
                    'вызывается fn(...args), результат сохраняется (в том числе undefined и null), и если '
                    'записей стало больше max — вытесняется самая давно использованная. Ошибка fn '
                    'пробрасывается и не кешируется (следующий вызов снова вызовет fn). Методы: '
                    'memoized.stats() → { hits, misses, evictions, size }, memoized.clear() (очищает записи '
                    'и счётчики), memoized.has(...args) → boolean (не меняет свежесть и счётчики). Промисы '
                    'кешируются как значения (но отклонённый промис удаляется из кеша, чтобы следующий вызов '
                    'повторил попытку).',
       'starter': 'function memoizeLRU(fn, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'let calls = 0; const f = memoizeLRU((a, b = 0) => { calls++; return a + b; }, { max: 3 '
                 '});\n'
                 'console.log(f(1), f(1), f(2), f(3), f(1), calls, JSON.stringify(canon(f.stats())));\n'
                 'console.log(f(4), f.has(2), f.has(1), f.has(3), f.has(4), calls, '
                 'JSON.stringify(canon(f.stats())));\n'
                 'console.log(f(2), f(3), calls, f.has(1), f.has(4)); f.clear(); '
                 'console.log(JSON.stringify(canon(f.stats())), f.has(2));\n'
                 'const u = memoizeLRU((x) => { calls++; return x === 1 ? undefined : null; }); '
                 'console.log(u(1), u(1), u(2), u(2), calls, u.stats().hits);\n'
                 'let n = 0; const bad = memoizeLRU((x) => { n++; if (n === 1) throw new Error("сбой"); '
                 'return x; }); try { bad(7); } catch (e) { console.log(e.message); } console.log(bad(7), '
                 'bad(7), n, JSON.stringify(canon(bad.stats())));\n'
                 'const keyed = memoizeLRU((o) => o.v * 2, { keyFn: (o) => o.id }); console.log(keyed({ id: '
                 '"a", v: 1 }), keyed({ id: "a", v: 100 }), keyed({ id: "b", v: 5 }));\n'
                 'let pc = 0; const pm = memoizeLRU(async (x) => { pc++; if (x === "bad") throw new '
                 'Error("отказ"); return x; }); console.log(await pm("ok"), await pm("ok"), pc); try { await '
                 'pm("bad"); } catch (e) { console.log(e.message); } await tick(); '
                 'console.log(pm.has("bad"), pm.has("ok")); try { await pm("bad"); } catch (e) { '
                 'console.log(e.message, pc); }\n'
                 'const one = memoizeLRU((x) => x, { max: 1 }); one(1); one(2); one(1); '
                 'console.log(JSON.stringify(canon(one.stats())), memoizeLRU((x) => x, { max: 0 })(5));\n'
                 'const z = memoizeLRU((x) => x, { max: 0 }); z(1); z(1); '
                 'console.log(JSON.stringify(canon(z.stats())));\n',
       'hint': 'Map сохраняет порядок вставки: чтобы освежить ключ, удалите и вставьте его заново.',
       'expected': ['1 1 2 3 1 3 {"evictions":0,"hits":2,"misses":3,"size":3}',
                    '4 false true true true 4 {"evictions":1,"hits":2,"misses":4,"size":3}',
                    '2 3 6 false true',
                    '{"evictions":0,"hits":0,"misses":0,"size":0} false',
                    'undefined undefined null null 8 2',
                    'сбой',
                    '7 7 2 {"evictions":0,"hits":1,"misses":2,"size":1}',
                    '2 2 10',
                    'ok ok 1',
                    'отказ',
                    'false true',
                    'отказ 3',
                    '{"evictions":2,"hits":0,"misses":3,"size":1} 5',
                    '{"evictions":2,"hits":0,"misses":2,"size":0}']},
      {'id': 'j20-user-timing',
       'mode': 'js',
       'title': 'Модель User Timing',
       'statement': 'Напишите функцию createPerformance(nowFn) → объект с методами mark(name, options), '
                    'measure(name, startOrOptions, endMark), getEntries(), getEntriesByName(name, type), '
                    'getEntriesByType(type), clearMarks(name), clearMeasures(name). mark(name, { startTime = '
                    'now(), detail }) → запись { name, entryType: "mark", startTime, duration: 0, detail } '
                    '(detail по умолчанию null) и добавляет её в список. measure(name, start, end): start и '
                    'end — имя метки (берётся последняя метка с таким именем на момент вызова), число '
                    '(время) или не заданы (start → 0, end → now()); можно передать объект { start, end, '
                    'duration, detail } вторым аргументом (start/end — имя или число; если задан duration и '
                    'один из концов, второй вычисляется); запись { name, entryType: "measure", startTime: '
                    'start, duration: end − start, detail }. Неизвестная метка — выбросить Error с name '
                    "«SyntaxError» и message «The mark 'имя' does not exist». getEntries() — все записи, "
                    'отсортированные по startTime (стабильно, при равенстве — по порядку добавления). '
                    'getEntriesByName(name, type?) и getEntriesByType(type) — то же с фильтром. '
                    'clearMarks(name?) удаляет метки (все или с именем), clearMeasures — измерения. Методы '
                    'возвращают запись (mark, measure).',
       'starter': 'function createPerformance(nowFn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'let t = 0; const p = createPerformance(() => t);\n'
                 'const show = (es) => console.log(es.map((e) => `${e.entryType === "mark" ? "mark" : '
                 '"meas"}:${e.name}@${e.startTime}+${e.duration}`).join(" "));\n'
                 't = 10; p.mark("a"); t = 40; p.mark("b", { detail: { k: 1 } }); t = 55; const m1 = '
                 'p.measure("a→b", "a", "b"); console.log(m1.startTime, m1.duration, '
                 'JSON.stringify(p.getEntriesByName("b")[0].detail), p.getEntriesByName("a")[0].detail);\n'
                 't = 70; p.measure("a→now", "a"); p.measure("all"); p.measure("num", 20, 25); '
                 'show(p.getEntries());\n'
                 't = 100; p.mark("a"); p.measure("a2→now", "a"); p.measure("a→b again", "a", "b"); '
                 'show(p.getEntries().filter((e) => e.name.includes("a") && e.entryType === "measure"));\n'
                 'p.mark("early", { startTime: 5 }); p.measure("opt", { start: "early", end: "b" }); '
                 'p.measure("dur1", { start: 30, duration: 15 }); p.measure("dur2", { end: 50, duration: 20 '
                 '}); p.measure("dur3", { duration: 10 }); p.measure("optnum", { start: 1, end: 2, detail: '
                 '"d" });\n'
                 'show(p.getEntries()); console.log(p.getEntriesByName("a").length, p.getEntriesByName("a", '
                 '"mark").length, p.getEntriesByName("a", "measure").length, '
                 'p.getEntriesByType("mark").length, p.getEntriesByType("measure").length, '
                 'p.getEntriesByName("optnum")[0].detail);\n'
                 'try { p.measure("bad", "нет-такой"); } catch (e) { console.log(e.name, e.message); } try { '
                 'p.measure("bad", "a", "ghost"); } catch (e) { console.log(e.message); } '
                 'console.log(p.getEntriesByName("bad").length);\n'
                 'p.clearMarks("a"); console.log(p.getEntriesByType("mark").map((e) => e.name).join()); '
                 'p.clearMeasures("opt"); console.log(p.getEntriesByType("measure").length); p.clearMarks(); '
                 'console.log(p.getEntriesByType("mark").length, p.getEntriesByType("measure").length); '
                 'p.clearMeasures(); console.log(p.getEntries().length);\n'
                 'const q = createPerformance(() => 1); q.mark("x", { startTime: 5 }); q.mark("y", { '
                 'startTime: 5 }); q.mark("w", { startTime: 2 }); console.log(q.getEntries().map((e) => '
                 'e.name).join());\n',
       'hint': 'Список записей; resolve превращает имя метки или число во время; сортировка стабильна по '
               '(startTime, порядок).',
       'expected': ['10 30 {"k":1} null',
                    'meas:all@0+70 mark:a@10+0 meas:a→b@10+30 meas:a→now@10+60 meas:num@20+5 mark:b@40+0',
                    'meas:all@0+70 meas:a→b@10+30 meas:a→now@10+60 meas:a2→now@100+0 meas:a→b again@100+-60',
                    'meas:all@0+70 meas:optnum@1+1 mark:early@5+0 meas:opt@5+35 mark:a@10+0 meas:a→b@10+30 '
                    'meas:a→now@10+60 meas:num@20+5 meas:dur1@30+15 meas:dur2@30+20 mark:b@40+0 '
                    'meas:dur3@90+10 mark:a@100+0 meas:a2→now@100+0 meas:a→b again@100+-60',
                    '2 2 0 4 11 d',
                    "SyntaxError The mark 'нет-такой' does not exist",
                    "The mark 'ghost' does not exist",
                    '0',
                    'early,b',
                    '10',
                    '0 10',
                    '0',
                    'w,x,y']},
      {'id': 'j20-flame',
       'mode': 'js',
       'title': 'Сводка по сэмплам профиля',
       'statement': 'Напишите функции summarizeSamples(samples) и collapse(samples). sample = { stack: '
                    '[корень … лист], dt (мс) }. summarizeSamples → массив { name, self, total, selfPct, '
                    'totalPct } по каждой функции: self — сумма dt сэмплов, где функция — лист (последний '
                    'элемент стека); total — сумма dt сэмплов, где она встречается в стеке (в одном сэмпле '
                    'считается один раз, даже при рекурсии); проценты — доля от суммы всех dt, округление до '
                    '1 знака (если сумма 0 — 0). Сортировка: по self по убыванию, затем по total по '
                    'убыванию, затем по имени. Пустой stack игнорируется. collapse → массив строк «a;b;c N» '
                    '(стек через «;» и суммарное dt через пробел) по уникальным стекам, отсортированный по '
                    'строке стека по алфавиту; сэмплы с равным стеком суммируются.',
       'starter': 'function summarizeSamples(samples) {\n}\nfunction collapse(samples) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const S = (dt, ...stack) => ({ stack, dt });\n'
                 'const samples = [S(10, "main", "render", "layout"), S(30, "main", "render", "paint"), '
                 'S(20, "main", "render", "layout"), S(5, "main", "handler"), S(15, "main", "render"), S(10, '
                 '"main", "fib", "fib", "fib"), S(10, "main", "fib", "fib"), S(0, "main", "idle"), S(5)];\n'
                 'for (const r of summarizeSamples(samples)) console.log(JSON.stringify(canon(r)));\n'
                 'console.log(collapse(samples).join(" | "));\n'
                 'console.log(JSON.stringify(summarizeSamples([])), JSON.stringify(collapse([])), '
                 'JSON.stringify(summarizeSamples([S(0, "a")]).map(canon)), '
                 'JSON.stringify(summarizeSamples([S(1, "a", "b"), S(1, "b", "a")]).map(canon)));\n'
                 'console.log(JSON.stringify(summarizeSamples([S(3, "x", "x", "x")]).map(canon)), '
                 'collapse([S(1, "b"), S(2, "a", "b"), S(3, "a;b")]).join("|"));\n',
       'hint': 'Map имя → {self, total}; total считайте через Set имён стека, чтобы рекурсия не удваивала '
               'время.',
       'expected': ['{"name":"layout","self":30,"selfPct":30,"total":30,"totalPct":30}',
                    '{"name":"paint","self":30,"selfPct":30,"total":30,"totalPct":30}',
                    '{"name":"fib","self":20,"selfPct":20,"total":20,"totalPct":20}',
                    '{"name":"render","self":15,"selfPct":15,"total":75,"totalPct":75}',
                    '{"name":"handler","self":5,"selfPct":5,"total":5,"totalPct":5}',
                    '{"name":"main","self":0,"selfPct":0,"total":100,"totalPct":100}',
                    '{"name":"idle","self":0,"selfPct":0,"total":0,"totalPct":0}',
                    'main;fib;fib 10 | main;fib;fib;fib 10 | main;handler 5 | main;idle 0 | main;render 15 | '
                    'main;render;layout 30 | main;render;paint 30',
                    '[] [] [{"name":"a","self":0,"selfPct":0,"total":0,"totalPct":0}] '
                    '[{"name":"a","self":1,"selfPct":50,"total":2,"totalPct":100},{"name":"b","self":1,"selfPct":50,"total":2,"totalPct":100}]',
                    '[{"name":"x","self":3,"selfPct":100,"total":3,"totalPct":100}] a;b 5|b 1']},
      {'id': 'j20-rum',
       'mode': 'js',
       'title': 'Сбор метрик у реальных пользователей',
       'statement': 'Напишите функцию createRum({ send, sampleRate = 1, rand = Math.random, now, maxBatch = '
                    '10 }) → { record(name, value), flush(final = false), pending(), sampled }. sampled = '
                    'rand() < sampleRate (решается один раз при создании); если не в выборке — все вызовы '
                    'record ничего не делают. Метрики «lcp», «inp», «cls» — «обновляемые»: хранится только '
                    'последнее значение (при повторных record значение заменяется, а запись остаётся на '
                    'прежнем месте порядка); они отправляются только при flush(true) (уход со страницы). '
                    'Остальные метрики — события: добавляются в очередь { name, value, t: now() }; когда '
                    'очередь событий достигает maxBatch — автоматически отправляется пачка (flush без '
                    'final). flush(final): если есть что отправлять — вызвать send({ final, metrics: [...] '
                    '}), где metrics — сначала накопленные события (в порядке записи), затем (только при '
                    'final) обновляемые метрики { name, value, t } (t — время последнего record) в порядке '
                    'первой записи; после отправки очереди очищаются. Пустую пачку не отправлять. После '
                    'flush(true) дальнейшие record игнорируются. pending() — число элементов, ожидающих '
                    'отправки (события + обновляемые).',
       'starter': 'function createRum(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'let t = 0; const sent = []; const mk = (opts) => createRum({ send: (p) => '
                 'sent.push(JSON.stringify(canon(p))), now: () => t, ...opts });\n'
                 'const show = (label) => { console.log(label.padEnd(20), sent.length ? sent.join(" ; ") : '
                 '"—"); sent.length = 0; };\n'
                 'const r = mk({ maxBatch: 3 }); console.log(r.sampled, r.pending());\n'
                 't = 1; r.record("lcp", 1000); t = 2; r.record("click", 5); t = 3; r.record("cls", 0.01); t '
                 '= 4; r.record("lcp", 1200); t = 5; r.record("fetch", 80); console.log(r.pending()); '
                 'show("до пачки");\n'
                 't = 6; r.record("fetch", 90); show("пачка из 3"); console.log(r.pending());\n'
                 't = 7; r.record("inp", 150); r.record("cls", 0.02); t = 8; r.record("nav", 1); '
                 'r.flush(false); show("flush(false)"); r.flush(false); show("пусто"); r.flush(true); '
                 'show("final");\n'
                 'r.record("x", 1); r.record("lcp", 5); console.log(r.pending()); r.flush(true); show("после '
                 'final");\n'
                 'const e = mk({}); e.flush(true); show("пустой final"); const off = mk({ sampleRate: 0.5, '
                 'rand: () => 0.5 }); off.record("x", 1); off.record("lcp", 1); off.flush(true); '
                 'console.log(off.sampled, off.pending()); show("не в выборке");\n'
                 'const on = mk({ sampleRate: 0.5, rand: () => 0.4999 }); console.log(on.sampled, mk({ '
                 'sampleRate: 0, rand: () => 0 }).sampled, mk({ sampleRate: 1, rand: () => 0.999 '
                 '}).sampled);\n'
                 'const only = mk({ maxBatch: 2 }); t = 9; only.record("lcp", 1); only.record("inp", 2); '
                 'console.log(only.pending()); only.flush(false); show("только live, не final"); '
                 'only.flush(true); show("final live"); \n'
                 'const b = mk({ maxBatch: 1 }); t = 10; b.record("a", 1); t = 11; b.record("b", 2); '
                 'show("maxBatch 1");\n',
       'hint': 'Обновляемые метрики — в Map (порядок первой вставки сохраняется при set), события — в '
               'массиве.',
       'expected': ['true 0',
                    '4',
                    'до пачки             —',
                    'пачка из 3           '
                    '{"final":false,"metrics":[{"name":"click","t":2,"value":5},{"name":"fetch","t":5,"value":80},{"name":"fetch","t":6,"value":90}]}',
                    '2',
                    'flush(false)         {"final":false,"metrics":[{"name":"nav","t":8,"value":1}]}',
                    'пусто                —',
                    'final                '
                    '{"final":true,"metrics":[{"name":"lcp","t":4,"value":1200},{"name":"cls","t":7,"value":0.02},{"name":"inp","t":7,"value":150}]}',
                    '0',
                    'после final          —',
                    'пустой final         —',
                    'false 0',
                    'не в выборке         —',
                    'true false true',
                    '2',
                    'только live, не final —',
                    'final live           '
                    '{"final":true,"metrics":[{"name":"lcp","t":9,"value":1},{"name":"inp","t":9,"value":2}]}',
                    'maxBatch 1           {"final":false,"metrics":[{"name":"a","t":10,"value":1}]} ; '
                    '{"final":false,"metrics":[{"name":"b","t":11,"value":2}]}']},
      {'id': 'j20-bfcache',
       'mode': 'js',
       'title': 'Блокировщики bfcache',
       'statement': 'Напишите функцию bfcacheBlockers(page) → { eligible, reasons }. page = { '
                    'hasUnloadHandler, mainCacheControl (строка заголовка Cache-Control главного документа '
                    'или null), openConnections: [строки видов], hasOpener, status (HTTP-статус главного '
                    'документа), isHttp (true, если страница по http/https; false — например chrome://), '
                    'pendingFetches (число незавершённых запросов с keepalive/без) }. Причины в порядке '
                    'проверки: «unload-handler» — есть обработчик unload; «cache-control-no-store» — '
                    'mainCacheControl содержит директиву no-store (без учёта регистра); '
                    '«open-connection:<вид>» — по одной причине на каждое значение из openConnections, '
                    'которое блокирует (websocket, webrtc, indexeddb-transaction, web-lock; другие виды, '
                    'например «fetch-complete», не блокируют), в порядке перечисления; «window-opener» — '
                    'hasOpener; «http-status» — status не 200; «not-http» — isHttp false; «pending-fetch» — '
                    'pendingFetches > 0. eligible = причин нет.',
       'starter': 'function bfcacheBlockers(page) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const ok = { hasUnloadHandler: false, mainCacheControl: "max-age=60", openConnections: [], '
                 'hasOpener: false, status: 200, isHttp: true, pendingFetches: 0 };\n'
                 'const cases = [["чистая", ok], ["unload", { ...ok, hasUnloadHandler: true }], ["no-store", '
                 '{ ...ok, mainCacheControl: "private, No-Store" }], ["no-store только в слове", { ...ok, '
                 'mainCacheControl: "max-age=60, x-no-store-ish=1" }], ["null", { ...ok, mainCacheControl: '
                 'null }],\n'
                 '  ["соединения", { ...ok, openConnections: ["websocket", "fetch-complete", "webrtc", '
                 '"websocket"] }], ["lock+idb", { ...ok, openConnections: ["indexeddb-transaction", '
                 '"web-lock"] }], ["opener", { ...ok, hasOpener: true }], ["404", { ...ok, status: 404 }], '
                 '["chrome://", { ...ok, isHttp: false }], ["pending", { ...ok, pendingFetches: 2 }],\n'
                 '  ["всё сразу", { hasUnloadHandler: true, mainCacheControl: "no-store", openConnections: '
                 '["webrtc"], hasOpener: true, status: 500, isHttp: false, pendingFetches: 1 }], ["минимум '
                 'полей", { openConnections: [] }]];\n'
                 'for (const [n, p] of cases) console.log(n.padEnd(24), '
                 'JSON.stringify(canon(bfcacheBlockers(p))));\n',
       'hint': 'Список причин собирается по порядку; no-store ищите как отдельную директиву.',
       'expected': ['чистая                   {"eligible":true,"reasons":[]}',
                    'unload                   {"eligible":false,"reasons":["unload-handler"]}',
                    'no-store                 {"eligible":false,"reasons":["cache-control-no-store"]}',
                    'no-store только в слове  {"eligible":true,"reasons":[]}',
                    'null                     {"eligible":true,"reasons":[]}',
                    'соединения               '
                    '{"eligible":false,"reasons":["open-connection:websocket","open-connection:webrtc","open-connection:websocket"]}',
                    'lock+idb                 '
                    '{"eligible":false,"reasons":["open-connection:indexeddb-transaction","open-connection:web-lock"]}',
                    'opener                   {"eligible":false,"reasons":["window-opener"]}',
                    '404                      {"eligible":false,"reasons":["http-status"]}',
                    'chrome://                {"eligible":false,"reasons":["not-http"]}',
                    'pending                  {"eligible":false,"reasons":["pending-fetch"]}',
                    'всё сразу                '
                    '{"eligible":false,"reasons":["unload-handler","cache-control-no-store","open-connection:webrtc","window-opener","http-status","not-http","pending-fetch"]}',
                    'минимум полей            {"eligible":true,"reasons":[]}']},
      {'id': 'j20-prefetch',
       'mode': 'js',
       'title': 'Решение о предзагрузке следующей страницы',
       'statement': 'Напишите функции prefetchDecision(ctx) и buildSpeculationRules(urls, options). ctx = { '
                    'saveData, effectiveType ("slow-2g"|"2g"|"3g"|"4g"), trigger '
                    '("visible"|"hover"|"pointerdown"|"none"), hoverMs, eagerness '
                    '("eager"|"moderate"|"conservative"), alreadyPrefetched, budgetUsedKB, budgetKB }. '
                    'Возвращает { action: "none"|"prefetch"|"prerender", reason }. Порядок проверок: '
                    'saveData → «none», «save-data»; effectiveType slow-2g или 2g → «none», «slow-network»; '
                    'alreadyPrefetched → «none», «already»; budgetUsedKB ≥ budgetKB → «none», «budget»; '
                    'затем по eagerness: «eager» — подходит любой trigger кроме «none»; «moderate» — hover '
                    'при hoverMs ≥ 200 или pointerdown; «conservative» — только pointerdown; не подошло — '
                    '«none», «trigger». Если триггер подошёл: action «prerender», если effectiveType «4g» и '
                    'trigger «pointerdown», иначе «prefetch»; reason «ok». buildSpeculationRules(urls, { '
                    'action, eagerness }) → объект { [action]: [{ source: "list", urls (без повторов, '
                    'порядок сохранить), eagerness }] }, либо null, если action не prefetch/prerender или '
                    'список пуст.',
       'starter': 'function prefetchDecision(ctx) {\n}\nfunction buildSpeculationRules(urls, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const base = { saveData: false, effectiveType: "4g", trigger: "hover", hoverMs: 300, '
                 'eagerness: "moderate", alreadyPrefetched: false, budgetUsedKB: 0, budgetKB: 500 };\n'
                 'const d = (o) => { const r = prefetchDecision({ ...base, ...o }); '
                 'console.log(JSON.stringify(o), r.action, r.reason); };\n'
                 'd({}); d({ saveData: true }); d({ effectiveType: "2g" }); d({ effectiveType: "slow-2g", '
                 'saveData: true }); d({ effectiveType: "3g" }); d({ alreadyPrefetched: true }); d({ '
                 'budgetUsedKB: 500 }); d({ budgetUsedKB: 499 });\n'
                 'd({ hoverMs: 199 }); d({ hoverMs: 200 }); d({ trigger: "visible" }); d({ trigger: '
                 '"pointerdown" }); d({ trigger: "pointerdown", effectiveType: "3g" }); d({ trigger: "none" '
                 '});\n'
                 'd({ eagerness: "eager", trigger: "visible" }); d({ eagerness: "eager", trigger: "none" }); '
                 'd({ eagerness: "eager", trigger: "pointerdown" }); d({ eagerness: "eager", trigger: '
                 '"hover", hoverMs: 0 });\n'
                 'd({ eagerness: "conservative", trigger: "hover" }); d({ eagerness: "conservative", '
                 'trigger: "pointerdown" }); d({ eagerness: "conservative", trigger: "pointerdown", '
                 'effectiveType: "4g", budgetUsedKB: 600 });\n'
                 'console.log(JSON.stringify(buildSpeculationRules(["/a", "/b", "/a"], { action: "prefetch", '
                 'eagerness: "moderate" })), JSON.stringify(buildSpeculationRules(["/x"], { action: '
                 '"prerender", eagerness: "conservative" })), buildSpeculationRules([], { action: '
                 '"prefetch", eagerness: "eager" }), buildSpeculationRules(["/a"], { action: "none", '
                 'eagerness: "eager" }));\n',
       'hint': 'Сначала запреты по порядку; затем проверка триггера по eagerness; prerender — только 4g и '
               'pointerdown.',
       'expected': ['{} prefetch ok',
                    '{"saveData":true} none save-data',
                    '{"effectiveType":"2g"} none slow-network',
                    '{"effectiveType":"slow-2g","saveData":true} none save-data',
                    '{"effectiveType":"3g"} prefetch ok',
                    '{"alreadyPrefetched":true} none already',
                    '{"budgetUsedKB":500} none budget',
                    '{"budgetUsedKB":499} prefetch ok',
                    '{"hoverMs":199} none trigger',
                    '{"hoverMs":200} prefetch ok',
                    '{"trigger":"visible"} none trigger',
                    '{"trigger":"pointerdown"} prerender ok',
                    '{"trigger":"pointerdown","effectiveType":"3g"} prefetch ok',
                    '{"trigger":"none"} none trigger',
                    '{"eagerness":"eager","trigger":"visible"} prefetch ok',
                    '{"eagerness":"eager","trigger":"none"} none trigger',
                    '{"eagerness":"eager","trigger":"pointerdown"} prerender ok',
                    '{"eagerness":"eager","trigger":"hover","hoverMs":0} prefetch ok',
                    '{"eagerness":"conservative","trigger":"hover"} none trigger',
                    '{"eagerness":"conservative","trigger":"pointerdown"} prerender ok',
                    '{"eagerness":"conservative","trigger":"pointerdown","effectiveType":"4g","budgetUsedKB":600} '
                    'none budget',
                    '{"prefetch":[{"source":"list","urls":["/a","/b"],"eagerness":"moderate"}]} '
                    '{"prerender":[{"source":"list","urls":["/x"],"eagerness":"conservative"}]} null null']},
      {'id': 'j20-islands',
       'mode': 'js',
       'title': 'Гидратация островов',
       'statement': 'Напишите функцию createHydrator(islands) → { dispatch(event), log() }. islands — массив '
                    '{ id, strategy: "load"|"idle"|"visible"|"interaction"|"never", parent? (id другого '
                    'острова) }. dispatch(event) принимает { type: "load" } — гидратируются острова со '
                    'стратегией load; { type: "idle" } — idle; { type: "visible", id } — остров id, если его '
                    'стратегия visible; { type: "interaction", id } — остров id, если его стратегия не never '
                    '(любое взаимодействие с ещё не гидратированным островом гидратирует его, какой бы '
                    'стратегия ни была, кроме never). Каждый остров гидратируется один раз. Если у острова '
                    'есть parent и родитель ещё не гидратирован — сначала гидратируется родитель '
                    '(рекурсивно, цепочкой), если у родителя стратегия не never; если родитель never — '
                    'остров гидратироваться не может (остаётся негидратированным). Остров только из списка '
                    '(неизвестный id игнорируется). Порядок: острова в порядке объявления islands; при '
                    'гидратации с цепочкой родители идут перед потомком. dispatch возвращает массив id, '
                    'гидратированных этим событием, в порядке гидратации; log() — массив строк «id:тип '
                    'события» (для тех же гидратаций, в порядке) — например «hero:load», «cart:interaction», '
                    'а для гидратации родителя по цепочке — «parent:parent-of:child».',
       'starter': 'function createHydrator(islands) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const h = createHydrator([{ id: "hero", strategy: "load" }, { id: "nav", strategy: "load" '
                 '}, { id: "comments", strategy: "visible" }, { id: "chart", strategy: "idle" }, { id: '
                 '"cart", strategy: "interaction" }, { id: "footer", strategy: "never" }, { id: "reply", '
                 'strategy: "visible", parent: "comments" }, { id: "emoji", strategy: "interaction", parent: '
                 '"reply" }, { id: "legal", strategy: "load", parent: "footer" }, { id: "orphan", strategy: '
                 '"load", parent: "ghost" }]);\n'
                 'const run = (e) => console.log(JSON.stringify(e), JSON.stringify(h.dispatch(e)));\n'
                 'run({ type: "visible", id: "comments" }); run({ type: "load" }); run({ type: "load" }); '
                 'run({ type: "interaction", id: "emoji" }); run({ type: "visible", id: "reply" }); run({ '
                 'type: "idle" });\n'
                 'run({ type: "interaction", id: "cart" }); run({ type: "interaction", id: "cart" }); run({ '
                 'type: "interaction", id: "footer" }); run({ type: "interaction", id: "legal" }); run({ '
                 'type: "interaction", id: "nope" }); run({ type: "visible", id: "nope" }); run({ type: '
                 '"visible", id: "cart" }); run({ type: "tick" });\n'
                 'console.log(h.log().join(" | "));\n'
                 'const g = createHydrator([{ id: "a", strategy: "idle" }, { id: "b", strategy: "idle", '
                 'parent: "a" }, { id: "c", strategy: "idle", parent: "b" }, { id: "d", strategy: "visible", '
                 'parent: "c" }]); console.log(JSON.stringify(g.dispatch({ type: "interaction", id: "d" })), '
                 'g.log().join(" | "), JSON.stringify(g.dispatch({ type: "idle" })));\n'
                 'const k = createHydrator([{ id: "c", strategy: "idle", parent: "b" }, { id: "b", strategy: '
                 '"idle", parent: "a" }, { id: "a", strategy: "load" }]); '
                 'console.log(JSON.stringify(k.dispatch({ type: "idle" })), k.log().join(" | "));\n',
       'hint': 'Рекурсивная функция hydrate(id, причина): сначала родитель, потом сам остров; множество уже '
               'гидратированных.',
       'expected': ['{"type":"visible","id":"comments"} ["comments"]',
                    '{"type":"load"} ["hero","nav"]',
                    '{"type":"load"} []',
                    '{"type":"interaction","id":"emoji"} ["reply","emoji"]',
                    '{"type":"visible","id":"reply"} []',
                    '{"type":"idle"} ["chart"]',
                    '{"type":"interaction","id":"cart"} ["cart"]',
                    '{"type":"interaction","id":"cart"} []',
                    '{"type":"interaction","id":"footer"} []',
                    '{"type":"interaction","id":"legal"} []',
                    '{"type":"interaction","id":"nope"} []',
                    '{"type":"visible","id":"nope"} []',
                    '{"type":"visible","id":"cart"} []',
                    '{"type":"tick"} []',
                    'comments:visible | hero:load | nav:load | reply:parent-of:emoji | emoji:interaction | '
                    'chart:idle | cart:interaction',
                    '["a","b","c","d"] a:parent-of:b | b:parent-of:c | c:parent-of:d | d:interaction []',
                    '["a","b","c"] a:parent-of:b | b:parent-of:c | c:idle']},
      {'id': 'j20-regression',
       'mode': 'js',
       'title': 'Обнаружение регрессий по медианам',
       'statement': 'Напишите функцию detectRegression(baseline, current, { minAbs = 0, relative = 0.05, k = '
                    '3 } = {}) → { verdict, delta, threshold, medBase, medCur }. Оба аргумента — массивы '
                    'замеров (меньше — лучше). medBase и medCur — медианы (для чётного числа — среднее двух '
                    'средних). madBase — медиана абсолютных отклонений baseline от medBase, умноженная на '
                    '1.4826 (устойчивая оценка шума). threshold = max(minAbs, medBase × relative, k × '
                    'madBase). delta = medCur − medBase. verdict: «regression», если delta > threshold; '
                    '«improvement», если delta < −threshold; иначе «same». Числа delta, threshold, medBase, '
                    'medCur округляются до 2 знаков (в сравнении участвуют неокруглённые). Пустой baseline '
                    'или current — Error с message «Нет данных».',
       'starter': 'function detectRegression(baseline, current, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const show = (b, c, o) => console.log(JSON.stringify(canon(detectRegression(b, c, o))));\n'
                 'const base = [1000, 1020, 980, 1010, 990]; show(base, [1000, 1005, 995]); show(base, '
                 '[1100, 1120, 1090]); show(base, [900, 890, 910]); show(base, [1049, 1051, 1050]);\n'
                 'show([1000, 1000, 1000], [1050], {}); show([1000, 1000, 1000], [1051]); show([1000, 1000, '
                 '1000], [1020], { minAbs: 30 }); show([1000, 1000, 1000], [1031], { minAbs: 30 }); '
                 'show([100, 200, 300, 400, 500], [350]); show([100, 200, 300, 400, 500], [900]);\n'
                 'show([10, 10, 10, 10, 90], [30], { k: 5 }); show([5], [6], { relative: 0.1 }); show([5], '
                 '[5.6], { relative: 0.1 }); show([1, 2], [1.5, 2.5]); show([0, 0, 0], [0]); show([0, 0, 0], '
                 '[1]);\n'
                 'for (const [b, c] of [[[], [1]], [[1], []]]) { try { detectRegression(b, c); } catch (e) { '
                 'console.log(e.message); } }\n',
       'hint': 'Медиана, MAD baseline и порог из трёх кандидатов; сравнивайте неокруглённые значения.',
       'expected': ['{"delta":0,"medBase":1000,"medCur":1000,"threshold":50,"verdict":"same"}',
                    '{"delta":100,"medBase":1000,"medCur":1100,"threshold":50,"verdict":"regression"}',
                    '{"delta":-100,"medBase":1000,"medCur":900,"threshold":50,"verdict":"improvement"}',
                    '{"delta":50,"medBase":1000,"medCur":1050,"threshold":50,"verdict":"same"}',
                    '{"delta":50,"medBase":1000,"medCur":1050,"threshold":50,"verdict":"same"}',
                    '{"delta":51,"medBase":1000,"medCur":1051,"threshold":50,"verdict":"regression"}',
                    '{"delta":20,"medBase":1000,"medCur":1020,"threshold":50,"verdict":"same"}',
                    '{"delta":31,"medBase":1000,"medCur":1031,"threshold":50,"verdict":"same"}',
                    '{"delta":50,"medBase":300,"medCur":350,"threshold":444.78,"verdict":"same"}',
                    '{"delta":600,"medBase":300,"medCur":900,"threshold":444.78,"verdict":"regression"}',
                    '{"delta":20,"medBase":10,"medCur":30,"threshold":0.5,"verdict":"regression"}',
                    '{"delta":1,"medBase":5,"medCur":6,"threshold":0.5,"verdict":"regression"}',
                    '{"delta":0.6,"medBase":5,"medCur":5.6,"threshold":0.5,"verdict":"regression"}',
                    '{"delta":0.5,"medBase":1.5,"medCur":2,"threshold":2.22,"verdict":"same"}',
                    '{"delta":0,"medBase":0,"medCur":0,"threshold":0,"verdict":"same"}',
                    '{"delta":1,"medBase":0,"medCur":1,"threshold":0,"verdict":"regression"}',
                    'Нет данных',
                    'Нет данных']}]}
