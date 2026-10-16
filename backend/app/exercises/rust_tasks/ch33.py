"""Задачи книги «Изучаем Rust»: глава 33 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {33: [{'id': 'r33-builder-threads',
       'mode': 'rust',
       'title': 'Рантайм через Builder',
       'statement': 'В обычной fn main постройте многопоточный рантайм: Builder::new_multi_thread() с 2 '
                    'рабочими потоками, именем потоков «воркер» (thread_name("worker")) и enable_all(). '
                    'Запустите через block_on задачу spawn, которая печатает «имя начинается с worker: true» '
                    '(проверяя std::thread::current().name()).\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'имя начинается с worker: true',
       'starter': 'fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Builder::new_multi_thread().worker_threads(2).thread_name("worker").enable_all().build().',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['имя начинается с worker: true']},
      {'id': 'r33-current-thread',
       'mode': 'rust',
       'title': 'Однопоточный рантайм',
       'statement': 'Используйте #[tokio::main(flavor = "current_thread")]. Запустите 5 задач spawn, каждая '
                    'возвращает номер потока (std::thread::current().id()) как строку; проверьте, что поток '
                    'один и тот же и совпадает с потоком main: «потоков: 1».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'потоков: 1',
       'starter': '#[tokio::main(flavor = "current_thread")]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'current_thread: всё выполняется на одном потоке.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['потоков: 1']},
      {'id': 'r33-handle-from-thread',
       'mode': 'rust',
       'title': 'Handle из обычного потока',
       'statement': 'Внутри #[tokio::main] получите Handle::current(), передайте в std::thread::spawn; поток '
                    'запускает через handle.spawn асинхронную задачу (сон 10 мс, возвращает 99) и отправляет '
                    'результат обратно через std::sync::mpsc. Напечатайте «99».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '99',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Handle можно передать в другой поток и использовать для spawn и block_on.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['99']},
      {'id': 'r33-runtime-twice',
       'mode': 'rust',
       'title': 'block_on дважды',
       'statement': 'В обычной main создайте один Runtime и дважды вызовите block_on: сначала положите '
                    'значение в общий Arc<Mutex<Vec<u32>>> из задачи, затем второй block_on прочитает его. '
                    'Напечатайте «[1, 2]».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '[1, 2]',
       'starter': 'fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Один Runtime можно использовать для нескольких block_on.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['[1, 2]']},
      {'id': 'r33-join-values',
       'mode': 'rust',
       'title': 'Значения из задач',
       'statement': 'Запустите три задачи spawn: возвращающие String «a», Vec<u32> [1, 2] и кортеж (3, '
                    'true). Дождитесь через tokio::join! и напечатайте по строке: «a», «[1, 2]», «(3, '
                    'true)».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'a\n'
                    '[1, 2]\n'
                    '(3, true)',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'join! над JoinHandle возвращает кортеж Result.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['a', '[1, 2]', '(3, true)']},
      {'id': 'r33-abort-finished',
       'mode': 'rust',
       'title': 'abort и is_finished',
       'statement': 'Запустите задачу со сном 1 с; сразу проверьте is_finished() (false), вызовите abort(), '
                    'дождитесь и напечатайте: «false», «cancelled: true», затем is_finished() — «true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'false\n'
                    'cancelled: true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'abort() прерывает на ближайшем .await; ожидание хэндла вернёт JoinError::is_cancelled.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['false', 'cancelled: true']},
      {'id': 'r33-panic-payload',
       'mode': 'rust',
       'title': 'Паника и её сообщение',
       'statement': 'Запустите задачу, паникующую panic!("бум"). Достаньте сообщение: '
                    'JoinError::into_panic() даёт Box<dyn Any + Send>; приведите к &str '
                    '(downcast_ref::<&str>()). Напечатайте «паника: бум».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'паника: бум',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'into_panic() возвращает полезную нагрузку паники.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['паника: бум']},
      {'id': 'r33-joinset-order',
       'mode': 'rust',
       'title': 'JoinSet и индексы',
       'statement': 'В JoinSet запустите 6 задач; i-я спит (6 − i)·5 мс и возвращает (i, i·i). Соберите '
                    'результаты и напечатайте отсортированными по i: [(0, 0), (1, 1), (2, 4), (3, 9), (4, '
                    '16), (5, 25)].\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '[(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Результаты приходят в порядке завершения — сортируйте по индексу.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['[(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]']},
      {'id': 'r33-joinset-abort-all',
       'mode': 'rust',
       'title': 'abort_all',
       'statement': 'Запустите в JoinSet 4 бесконечные задачи (sleep 1 с), вызовите abort_all() и дождитесь '
                    'всех join_next: посчитайте ошибки is_cancelled. Напечатайте «отменено: 4».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'отменено: 4',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'После abort_all join_next возвращает Err(cancelled) для каждой задачи.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['отменено: 4']},
      {'id': 'r33-joinset-drop',
       'mode': 'rust',
       'title': 'Drop набора отменяет задачи',
       'statement': 'Задача хранит Guard, который в Drop увеличивает общий AtomicUsize. Запустите 3 таких '
                    'задачи (сон 1 с) в JoinSet, дайте им стартовать (sleep 10 мс), уничтожьте набор (drop) '
                    'и дайте время на завершение (sleep 20 мс). Напечатайте «очищено: 3».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'очищено: 3',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Drop для JoinSet вызывает abort_all.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['очищено: 3']},
      {'id': 'r33-blocking-parallel',
       'mode': 'rust',
       'title': 'Блокирующие задачи параллельны',
       'statement': 'Запустите 4 задачи spawn_blocking, каждая спит (std::thread::sleep) 100 мс. Дождитесь '
                    'всех и убедитесь, что общее время меньше 300 мс: «параллельно: true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'параллельно: true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Пул блокирующих потоков выполняет задачи одновременно.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['параллельно: true']},
      {'id': 'r33-block-in-place',
       'mode': 'rust',
       'title': 'block_in_place',
       'statement': 'На многопоточном рантайме внутри задачи (spawn) вызовите block_in_place для вычисления '
                    'суммы квадратов 1..=1000 (u64) и верните её: «333833500».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '333833500',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'block_in_place разрешён только на multi_thread.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['333833500']},
      {'id': 'r33-local-set',
       'mode': 'rust',
       'title': 'LocalSet и Rc',
       'statement': 'На current_thread создайте LocalSet; внутри run_until запустите 5 задач spawn_local, '
                    'каждая увеличивает Rc<RefCell<u32>> на своё число (1…5) и после yield_now ничего не '
                    'делает. Дождитесь всех и напечатайте «15».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '15',
       'starter': '#[tokio::main(flavor = "current_thread")]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'spawn_local принимает !Send-фьючеры внутри LocalSet.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['15']},
      {'id': 'r33-task-local',
       'mode': 'rust',
       'title': 'task_local!',
       'statement': 'Объявите tokio::task_local! { static REQ_ID: u32; }. Запустите две задачи: в одной '
                    'REQ_ID.scope(1, …), в другой scope(2, …); каждая вызывает общую async fn log() -> '
                    'String, возвращающую «запрос <id>» из REQ_ID.get(). Напечатайте оба результата: «запрос '
                    '1», «запрос 2».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'запрос 1\n'
                    'запрос 2',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'REQ_ID.scope(значение, фьючер) даёт значение на время выполнения.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['запрос 1', 'запрос 2']},
      {'id': 'r33-task-id',
       'mode': 'rust',
       'title': 'Номера задач',
       'statement': 'Запустите 5 задач, каждая возвращает tokio::task::id(). Убедитесь, что все номера '
                    'разные и не совпадают с номером... (main — не задача): напечатайте «уникальных: 5».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'уникальных: 5',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'tokio::task::id() возвращает Id, реализующий Hash.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['уникальных: 5']},
      {'id': 'r33-yield-fairness',
       'mode': 'rust',
       'title': 'Справедливость',
       'statement': 'На current_thread запустите «занятую» задачу: while !flag { yield_now().await } и '
                    'вторую, которая поднимает флаг (AtomicBool) сразу. Дождитесь обеих и напечатайте «флаг '
                    'поднят». (Без yield_now задача зависла бы.)\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'флаг поднят',
       'starter': '#[tokio::main(flavor = "current_thread")]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'yield_now отдаёт управление другим задачам на том же потоке.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['флаг поднят']},
      {'id': 'r33-detach',
       'mode': 'rust',
       'title': 'Открепление',
       'statement': 'Выбросьте JoinHandle (drop) сразу после spawn и убедитесь, что задача продолжает '
                    'работать: она через 10 мс отправляет «жива» через oneshot. Напечатайте «жива».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'жива',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Выброшенный JoinHandle не отменяет задачу.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['жива']},
      {'id': 'r33-runtime-drop',
       'mode': 'rust',
       'title': 'Уничтожение рантайма',
       'statement': 'В обычной main создайте Runtime, запустите spawn задачу с Guard (Drop увеличивает '
                    'AtomicUsize), которая спит 10 с. Дайте ей стартовать (block_on sleep 10 мс), затем '
                    'drop(rt). Напечатайте число сработавших Drop: «1».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '1',
       'starter': 'fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'При уничтожении рантайма задачи отменяются, их деструкторы вызываются.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['1']},
      {'id': 'r33-shutdown-timeout',
       'mode': 'rust',
       'title': 'shutdown_timeout',
       'statement': 'Запустите в рантайме spawn_blocking на 50 мс (std sleep) и вызовите '
                    'rt.shutdown_timeout(Duration::from_secs(2)); напечатайте «рантайм остановлен» и '
                    '«быстрее 2 с: true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'рантайм остановлен\n'
                    'быстрее 2 с: true',
       'starter': 'fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'shutdown_timeout ждёт блокирующие задачи не дольше лимита.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['рантайм остановлен', 'быстрее 2 с: true']},
      {'id': 'r33-handle-try-current',
       'mode': 'rust',
       'title': 'Handle::try_current',
       'statement': 'Покажите, что Handle::try_current() вне рантайма возвращает Err (напечатайте «вне: '
                    'false»), а внутри — Ok («внутри: true»). Сначала вызовите в обычной main до создания '
                    'рантайма, затем внутри block_on.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'вне: false\n'
                    'внутри: true',
       'starter': 'fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'try_current не паникует: это Result.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['вне: false', 'внутри: true']},
      {'id': 'r33-par-map',
       'mode': 'rust',
       'title': 'Параллельный map',
       'statement': 'Напишите async fn par_map(items: Vec<u32>, f: fn(u32) -> u32) -> Vec<u32>: каждый '
                    'элемент обрабатывается в своей задаче spawn_blocking; результат — в порядке входа. Для '
                    'f = |x| x * x и items 1..=8 напечатайте [1, 4, 9, 16, 25, 36, 49, 64].\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '[1, 4, 9, 16, 25, 36, 49, 64]',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Хэндлы ожидайте по порядку запуска, чтобы сохранить порядок.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['[1, 4, 9, 16, 25, 36, 49, 64]']},
      {'id': 'r33-many-tasks',
       'mode': 'rust',
       'title': 'Много задач',
       'statement': 'Запустите 20000 задач spawn, каждая увеличивает общий AtomicUsize; дождитесь всех '
                    '(JoinSet) и напечатайте «20000».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '20000',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Задачи tokio очень дёшевы: десятки тысяч — не проблема.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['20000']},
      {'id': 'r33-fan-out-in',
       'mode': 'rust',
       'title': 'Рассылка и сбор',
       'statement': 'Рассылка-сбор: 4 рабочих (spawn), каждый обрабатывает свою четверть чисел 1..=100 '
                    '(сумма) и отправляет частичную сумму в mpsc-канал; main суммирует полученные 4 '
                    'значения: «5050».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '5050',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'drop(tx) нужен, чтобы recv вернул None после последнего отправителя.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['5050']},
      {'id': 'r33-retry',
       'mode': 'rust',
       'title': 'Повтор с отменой',
       'statement': 'Напишите async fn retry<F, Fut>(n: u32, mut f: F) -> Result<u32, String>, где F: '
                    'FnMut(u32) -> Fut, Fut: Future<Output = Result<u32, String>>: пробует f(attempt) для '
                    'attempt = 1…n и возвращает первый Ok или последнюю ошибку. Для f, успешной только с '
                    'третьей попытки, напечатайте «Ok(3)»; для безнадёжной — «Err("сбой 3")».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'Ok(3)\n'
                    'Err("сбой 3")',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Цикл по попыткам; ранний return при Ok.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['Ok(3)', 'Err("сбой 3")']},
      {'id': 'r33-run-all-result',
       'mode': 'rust',
       'title': 'Result из задач',
       'statement': 'Напишите async fn run_all(n: u32) -> Result<Vec<u32>, tokio::task::JoinError>: '
                    'запустить n задач (i·10) и собрать результаты с помощью ? по хэндлам; для n = 4 '
                    'напечатайте «Ok([0, 10, 20, 30])».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'Ok([0, 10, 20, 30])',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'JoinError реализует Error: оператор ? подходит.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['Ok([0, 10, 20, 30])']},
      {'id': 'r33-blocking-abort',
       'mode': 'rust',
       'title': 'abort у блокирующей задачи',
       'statement': 'Покажите, что abort() не останавливает уже запущенную spawn_blocking: задача ставит '
                    'started, спит 60 мс и ставит done (AtomicBool). Main ждёт started (опрос sleep 1 мс), '
                    'вызывает abort(), ждёт 100 мс и печатает «флаг: true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'флаг: true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Блокирующий поток доработает до конца: отмена применима только к ещё не стартовавшим.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['флаг: true']},
      {'id': 'r33-worker-pool',
       'mode': 'rust',
       'title': 'Пул рабочих',
       'statement': 'Пул из 3 рабочих читает задания (числа 1…12) из общего mpsc-канала '
                    '(Arc<tokio::sync::Mutex<Receiver<u32>>>), каждый прибавляет квадрат числа в общий '
                    'AtomicU64. Отправитель закрывается, main дожидается рабочих (JoinSet) и печатает '
                    '«650».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '650',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Получатель общий: оборачиваем в Arc<Mutex<…>>; None — сигнал завершения.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['650']},
      {'id': 'r33-timeout-spawn',
       'mode': 'rust',
       'title': 'timeout над JoinHandle',
       'statement': 'Оберните JoinHandle задачи (сон 200 мс) в tokio::time::timeout(30 мс): напечатайте '
                    '«таймаут»; задача при этом продолжает работать — проверьте через oneshot, что через 250 '
                    'мс она всё же завершилась: «задача дожила».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'таймаут\n'
                    'задача дожила',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'timeout отбрасывает ожидание хэндла, но не саму задачу.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['таймаут', 'задача дожила']},
      {'id': 'r33-multi-thread-count',
       'mode': 'rust',
       'title': 'Сколько потоков',
       'statement': 'Постройте многопоточный рантайм с worker_threads(3) и запустите 50 задач spawn, каждая '
                    'возвращает имя своего потока (после короткого sleep 1 мс). Напечатайте: потоков не '
                    'больше 3: true.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'потоков не больше 3: true',
       'starter': '#[tokio::main(flavor = "multi_thread", worker_threads = 3)]\n'
                  'async fn main() {\n'
                  '    // ваш код\n'
                  '}\n',
       'driver': '',
       'hint': 'Все задачи выполняются на рабочих потоках пула.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['потоков не больше 3: true']},
      {'id': 'r33-spawn-borrowed-fix',
       'mode': 'rust',
       'title': 'Исправьте: spawn и ссылка',
       'statement': 'Программа не собирается: задача заимствует локальный вектор. Исправьте через Arc, чтобы '
                    'напечатать «сумма 10».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'сумма 10\n'
                    '4',
       'starter': '#[tokio::main]\n'
                  'async fn main() {\n'
                  '    let v = vec![1, 2, 3, 4];\n'
                  '    let h = tokio::spawn(async { v.iter().sum::<i32>() });\n'
                  '    println!("сумма {}", h.await.unwrap());\n'
                  '    println!("{}", v.len());\n'
                  '}\n',
       'driver': '',
       'hint': 'Arc::clone и move.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['сумма 10', '4']}]}
