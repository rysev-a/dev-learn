"""Задачи книги «Изучаем Rust»: глава 37 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {37: [{'id': 'r37-abort-inflight',
  'mode': 'rust',
  'title': 'abort в полёте',
  'statement': 'Запустите задачу: печатает «start», спит 100 мс и печатает «end». Через 20 мс '
               'отмените её (abort), дождитесь хэндла и напечатайте «отменена: true» '
               '(JoinError::is_cancelled).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'start\n'
               'отменена: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let e = h.await.unwrap_err(); e.is_cancelled()',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['start', 'отменена: true']},
 {'id': 'r37-drop-future',
  'mode': 'rust',
  'title': 'Drop отменённого фьючера',
  'statement': 'Заведите структуру Guard с Drop, печатающим «drop guard». В select! первая ветка — '
               'async-блок: создаёт Guard и спит 200 мс; вторая — сон 20 мс и печать «тайм-аут». '
               'Посмотрите, что и в каком порядке напечатано: проигравший фьючер уничтожается '
               'вместе со своими локальными значениями.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'drop guard\n'
               'тайм-аут',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Guard живёт внутри async-блока и уничтожается при отбрасывании блока.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['drop guard', 'тайм-аут']},
 {'id': 'r37-is-finished',
  'mode': 'rust',
  'title': 'abort и is_finished',
  'statement': 'Запустите задачу со сном 1 с, отмените её (abort), подождите 10 мс и напечатайте '
               '«завершена: true» по is_finished().\n'
               '\n'
               'Ожидаемый вывод:\n'
               'завершена: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'После abort задача завершается на ближайшем .await; is_finished() покажет true.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['завершена: true']},
 {'id': 'r37-detached',
  'mode': 'rust',
  'title': 'Уничтоженный хэндл не отменяет',
  'statement': 'Запустите задачу: сон 30 мс и печать «работает». Сразу уничтожьте JoinHandle '
               '(drop) и ждите в main 100 мс. Задача должна успеть напечатать своё.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'работает',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'drop(handle) не вызывает abort: задача продолжает жить.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['работает']},
 {'id': 'r37-token-loop',
  'mode': 'rust',
  'title': 'Цикл с токеном',
  'statement': 'Задача в цикле select!: ждёт tokio_util::sync::CancellationToken::cancelled() или '
               'сон 10 мс (считать). Через 50 мс main отменяет токен. Задача печатает '
               '«остановлена», main дожидается её.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'остановлена',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::select! { _ = token.cancelled() => break, _ = sleep(..) => n += 1 }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['остановлена']},
 {'id': 'r37-child-token',
  'mode': 'rust',
  'title': 'Дерево токенов',
  'statement': 'Создайте родительский токен и дочерний (child_token()). Отмените родителя и '
               'напечатайте «дочерний: true» (child.is_cancelled()). Затем создайте новую пару, '
               'отмените ребёнка и напечатайте «родитель: false».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'дочерний: true\n'
               'родитель: false',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Отмена идёт вниз по дереву, но не вверх.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['дочерний: true', 'родитель: false']},
 {'id': 'r37-cancelled-await',
  'mode': 'rust',
  'title': 'Ждём сигнал',
  'statement': 'Запущенная задача ждёт token.cancelled().await и печатает «сигнал получен». Main '
               'печатает «отменяем» (после паузы 20 мс), отменяет токен и дожидается задачи.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'отменяем\n'
               'сигнал получен',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'cancel() будит все ожидающие cancelled().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['отменяем', 'сигнал получен']},
 {'id': 'r37-drop-guard',
  'mode': 'rust',
  'title': 'DropGuard токена',
  'statement': 'Получите drop_guard() у клона токена в отдельном блоке; после выхода из блока '
               'напечатайте «отменён: true» (token.is_cancelled()).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'отменён: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': '{ let _g = token.clone().drop_guard(); }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['отменён: true']},
 {'id': 'r37-broadcast-shutdown',
  'mode': 'rust',
  'title': 'Остановка рассылкой',
  'statement': 'Запустите три рабочих задачи, каждая ждёт сообщение остановки из broadcast-канала '
               'и возвращает свой номер. Через 20 мс main отправляет сигнал, собирает номера '
               '(JoinSet) и печатает «остановлено: 3».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'остановлено: 3',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let mut rx = tx.subscribe(); rx.recv().await; JoinSet::join_next().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['остановлено: 3']},
 {'id': 'r37-task-tracker',
  'mode': 'rust',
  'title': 'TaskTracker',
  'statement': 'Запустите через TaskTracker три задачи со снами 10, 20 и 30 мс, закройте трекер '
               '(close) и дождитесь (wait). Напечатайте «все завершены».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'все завершены',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'use tokio_util::task::TaskTracker; tracker.spawn(..); tracker.close(); '
          'tracker.wait().await',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['все завершены']},
 {'id': 'r37-joinset-sum',
  'mode': 'rust',
  'title': 'JoinSet: сумма',
  'statement': 'Запустите в JoinSet три задачи, возвращающие 1, 2 и 3. Сложите результаты по мере '
               'готовности (join_next) и напечатайте «сумма: 6».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'сумма: 6',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'while let Some(r) = set.join_next().await { sum += r.unwrap(); }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['сумма: 6']},
 {'id': 'r37-cleanup-abort',
  'mode': 'rust',
  'title': 'Очистка при abort',
  'statement': 'Задача создаёт Guard с Drop, печатающим «очистка», и спит секунду. Через 20 мс '
               'отмените её, дождитесь хэндла и напечатайте «отменена». Очистка должна пройти '
               'раньше.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'очистка\n'
               'отменена',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Drop сработает при отбрасывании фьючера, до возврата h.await.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['очистка', 'отменена']},
 {'id': 'r37-semaphore-peak',
  'mode': 'rust',
  'title': 'Предел параллелизма',
  'statement': 'Обработайте 10 заданий, ограничив одновременность семафором на 3 разрешения. В '
               'каждом задании увеличивайте счётчик активных (AtomicUsize), обновляйте максимум, '
               'спите 30 мс и уменьшайте. Напечатайте «пик: 3».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'пик: 3',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'fetch_max для пика; разрешение — в переменной на время сна.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['пик: 3']},
 {'id': 'r37-load-shed',
  'mode': 'rust',
  'title': 'Сброс нагрузки',
  'statement': 'Очередь на 2 места, потребителя нет. Отправьте 5 заданий через try_send; считайте '
               'принятые и отброшенные (Full). Напечатайте «принято 2, отброшено 3».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'принято 2, отброшено 3',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Err(TrySendError::Full(_)) => rejected += 1',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['принято 2, отброшено 3']},
 {'id': 'r37-timeout-error',
  'mode': 'rust',
  'title': 'Своя ошибка таймаута',
  'statement': 'Опишите enum Error { Timeout } (derive Debug) и async fn call() -> Result<u32, '
               'Error>: ожидание сна 200 мс под timeout 30 мс, при просрочке — Error::Timeout. '
               'Напечатайте результат вызова через {:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Err(Timeout)',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': '.await.map_err(|_| Error::Timeout)?; затем Ok(..)',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Err(Timeout)']},
 {'id': 'r37-blocking-parallel',
  'mode': 'rust',
  'title': 'spawn_blocking не мешает',
  'statement': 'На однопоточном рантайме (flavor = "current_thread") запустите задачу-тикер: '
               'каждые 10 мс увеличивает счётчик. Одновременно дождитесь spawn_blocking с '
               'блокирующим std::thread::sleep на 100 мс. Затем остановите тикер и напечатайте '
               '«работал параллельно: true», если тиков не меньше 5.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'работал параллельно: true',
  'starter': '#[tokio::main(flavor = "current_thread")]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'spawn_blocking(|| std::thread::sleep(..)).await — пока ждём, поток рантайма свободен '
          'для тикера.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['работал параллельно: true']},
 {'id': 'r37-fix-blocking',
  'mode': 'rust',
  'title': 'Исправьте: блокирующий сон в задаче',
  'statement': 'Тикер на однопоточном рантайме не получает времени: main выполняет «тяжёлую '
               'работу» (std::thread::sleep на 100 мс) прямо в асинхронной функции. Вынесите её в '
               'spawn_blocking, чтобы тикер успел сработать не менее 5 раз: должно быть «тиков не '
               'меньше 5: true».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'тиков не меньше 5: true',
  'starter': 'use std::sync::atomic::{AtomicUsize, Ordering};\n'
             'use std::sync::Arc;\n'
             'use std::time::Duration;\n'
             'use tokio::time::sleep;\n'
             '\n'
             '#[tokio::main(flavor = "current_thread")]\n'
             'async fn main() {\n'
             '    let ticks = Arc::new(AtomicUsize::new(0));\n'
             '    let t = ticks.clone();\n'
             '    let ticker = tokio::spawn(async move {\n'
             '        loop {\n'
             '            sleep(Duration::from_millis(10)).await;\n'
             '            t.fetch_add(1, Ordering::SeqCst);\n'
             '        }\n'
             '    });\n'
             '    std::thread::sleep(Duration::from_millis(100)); // тяжёлая работа\n'
             '    ticker.abort();\n'
             '    println!("тиков не меньше 5: {}", ticks.load(Ordering::SeqCst) >= 5);\n'
             '}\n',
  'driver': '',
  'hint': 'tokio::task::spawn_blocking(|| std::thread::sleep(..)).await.unwrap();',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['тиков не меньше 5: true']},
 {'id': 'r37-join-panic',
  'mode': 'rust',
  'title': 'Паника в задаче',
  'statement': 'Запустите задачу, которая паникует (panic!), дождитесь хэндла и напечатайте '
               '«паника: true» по JoinError::is_panic(). Программа при этом не должна упасть.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'паника: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let e = h.await.unwrap_err(); e.is_panic()',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['паника: true']},
 {'id': 'r37-supervisor',
  'mode': 'rust',
  'title': 'Супервайзер',
  'statement': 'Задача при первых двух запусках паникует, на третьем завершается нормально; каждый '
               'запуск печатает «запуск N». Напишите цикл-супервайзер: пока хэндл возвращает '
               'ошибку, запускайте задачу заново. После успеха напечатайте «готово».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'запуск 1\n'
               'запуск 2\n'
               'запуск 3\n'
               'готово',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'AtomicUsize считает запуски; if tokio::spawn(..).await.is_ok() { break }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['запуск 1', 'запуск 2', 'запуск 3', 'готово']},
 {'id': 'r37-retry-limit',
  'mode': 'rust',
  'title': 'Повторы с пределом',
  'statement': 'Операция всегда падает (Err("fail")). Повторите её не более 3 раз с паузой 10 мс '
               'между попытками. Напечатайте «попыток: 3» и «итог: Err».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'попыток: 3\n'
               'итог: Err',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Счётчик попыток, пауза после каждой неудачи, выход по пределу.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['попыток: 3', 'итог: Err']},
 {'id': 'r37-interval-limit',
  'mode': 'rust',
  'title': 'Ограничение частоты интервалом',
  'statement': 'Обработайте 5 событий, перед каждым ожидая tick() интервала 20 мс (первый тик '
               'сразу). Напечатайте «ограничено: true», если всё заняло не меньше 70 мс.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ограничено: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Тики на 0, 20, 40, 60, 80 мс — до последнего события 80 мс.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ограничено: true']},
 {'id': 'r37-refill',
  'mode': 'rust',
  'title': 'Ведро токенов',
  'statement': 'Семафор без разрешений и фоновая задача: каждые 20 мс добавляет одно разрешение '
               '(add_permits(1)). Main берёт три разрешения подряд (acquire().await.forget()). '
               'Напечатайте «пополнение работает: true», если это заняло не меньше 55 мс.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'пополнение работает: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'sem.acquire().await.unwrap().forget() — токен потрачен, а не возвращён.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['пополнение работает: true']},
 {'id': 'r37-bucket-burst',
  'mode': 'rust',
  'title': 'Всплеск и ожидание',
  'statement': 'Ведро на 3 токена изначально полное, пополнение — по одному каждые 50 мс. Возьмите '
               '3 токена (должно занять меньше 20 мс) и напечатайте «всплеск: true», затем '
               'возьмите четвёртый и напечатайте «четвёртый ждал: true» (не меньше 40 мс).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'всплеск: true\n'
               'четвёртый ждал: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Измеряйте Instant перед и после acquire; пополнение — в фоновой задаче.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['всплеск: true', 'четвёртый ждал: true']},
 {'id': 'r37-metrics',
  'mode': 'rust',
  'title': 'Метрики рантайма',
  'statement': 'В обычной fn main постройте многопоточный рантайм с 2 рабочими потоками (Builder, '
               'enable_all) и напечатайте rt.metrics().num_workers().\n'
               '\n'
               'Ожидаемый вывод:\n'
               '2',
  'starter': 'fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::runtime::Builder::new_multi_thread().worker_threads(2).enable_all().build()',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['2']},
 {'id': 'r37-yield',
  'mode': 'rust',
  'title': 'yield_now: уступить поток',
  'statement': 'На однопоточном рантайме запустите задачу, которая поднимает общий AtomicBool. В '
               'main ждите, пока флаг поднимется, циклом с tokio::task::yield_now().await (без '
               'sleep) и напечатайте «флаг поднят».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'флаг поднят',
  'starter': '#[tokio::main(flavor = "current_thread")]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'while !flag.load(Ordering::SeqCst) { tokio::task::yield_now().await; } — без yield_now '
          'задача никогда не получит поток.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['флаг поднят']},
 {'id': 'r37-actor-timeout',
  'mode': 'rust',
  'title': 'Актор не отвечает',
  'statement': 'Актор принимает запрос с oneshot::Sender и «зависает» (сон 500 мс, ответа нет). '
               'Клиент ждёт ответ с timeout 50 мс и при просрочке печатает «актор не ответил».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'актор не ответил',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'timeout(Duration::from_millis(50), reply_rx).await.is_err()',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['актор не ответил']},
 {'id': 'r37-drain',
  'mode': 'rust',
  'title': 'Дочитать очередь',
  'statement': 'Производитель отправляет 5 заданий и закрывает канал. Потребитель обрабатывает '
               'каждое (сон 5 мс) до закрытия и затем печатает «обработано: 5» — очередь не '
               'теряется при закрытии.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'обработано: 5',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'while let Some(_) = rx.recv().await — выходит только после того, как все сообщения '
          'прочитаны.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['обработано: 5']},
 {'id': 'r37-biased-stop',
  'mode': 'rust',
  'title': 'Остановка в приоритете',
  'statement': 'Токен уже отменён, а в очереди лежат задания. Цикл select! с biased; проверяет '
               'сначала cancelled(), затем recv(). Напечатайте «после остановки: 0» — число '
               'обработанных заданий.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'после остановки: 0',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::select! { biased; _ = token.cancelled() => break, job = rx.recv() => .. }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['после остановки: 0']},
 {'id': 'r37-watch-flag',
  'mode': 'rust',
  'title': 'Флаг остановки через watch',
  'statement': 'Три рабочих ждут, пока watch-значение станет true (rx.wait_for(|v| *v).await). '
               'Main через 20 мс отправляет true и дожидается всех (JoinSet). Напечатайте '
               '«остановлены: 3».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'остановлены: 3',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let (tx, rx) = watch::channel(false); в задаче let mut rx = rx.clone(); rx.wait_for(|v| '
          '*v).await',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['остановлены: 3']},
 {'id': 'r37-explicit-close',
  'mode': 'rust',
  'title': 'Явное закрытие вместо async Drop',
  'statement': 'Структура Conn { closed: bool } с Drop: если closed == false, печатает «не '
               'закрыто!». Добавьте async fn close(mut self): ставит closed = true и спит 10 мс '
               '(имитация сброса буферов). Вызовите close и напечатайте «закрыто явно». '
               'Предупреждения из Drop быть не должно.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'закрыто явно',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'В close(mut self) выставьте флаг до того, как self уничтожится в конце функции.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['закрыто явно']}]}
