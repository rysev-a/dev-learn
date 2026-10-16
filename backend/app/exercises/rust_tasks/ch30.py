"""Задачи книги «Изучаем Rust»: глава 30 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {30: [{'id': 'r30-first-async',
       'mode': 'rust',
       'title': 'Первая async-функция',
       'statement': 'Напишите async fn greet(name: &str) -> String, возвращающую «Привет, <имя>!», и '
                    'вызовите её с .await в main с атрибутом #[tokio::main]. Напечатайте результат для '
                    '«Аня».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'Привет, Аня!',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'async fn возвращает Future; .await внутри async main.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['Привет, Аня!']},
      {'id': 'r30-lazy',
       'mode': 'rust',
       'title': 'Future ленив',
       'statement': 'Создайте future f = work() (async fn work печатает «работа»), напечатайте «до», затем '
                    '.await, затем «после». Ожидается: «до», «работа», «после» — вызов async fn сам ничего '
                    'не печатает.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'до\n'
                    'работа\n'
                    'после',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Тело выполняется только на .await.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['до', 'работа', 'после']},
      {'id': 'r30-order-await',
       'mode': 'rust',
       'title': 'Порядок выполнения',
       'statement': 'Две async fn a() и b() печатают «a» и «b». Вызовите их последовательно через .await: a, '
                    'затем b, затем напечатайте «конец».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'a\n'
                    'b\n'
                    'конец',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Последовательные .await выполняются один за другим.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['a', 'b', 'конец']},
      {'id': 'r30-return-value',
       'mode': 'rust',
       'title': 'Значения из async',
       'statement': 'async fn square(x: u64) -> u64 и async fn sum_squares(n: u64) -> u64, которая в цикле '
                    'вызывает square(i).await для i от 1 до n. Напечатайте sum_squares(10) = 385.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '385',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Внутри async fn можно вызывать другие async fn через .await.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['385']},
      {'id': 'r30-question-mark',
       'mode': 'rust',
       'title': '? в async',
       'statement': 'async fn parse_sum(a: &str, b: &str) -> Result<i32, std::num::ParseIntError>: разберите '
                    'оба числа и сложите, используя ?. Напечатайте результаты для («2», «40»), («2», «x») — '
                    '«Ok(42)» и признак ошибки «true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'Ok(42)\n'
                    'true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': '? работает в async fn, возвращающей Result.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['Ok(42)', 'true']},
      {'id': 'r30-sleep-order',
       'mode': 'rust',
       'title': 'Конкурентно: join!',
       'statement': 'Две задачи: «медленная» спит 60 мс и печатает «медленная», «быстрая» — 10 мс и печатает '
                    '«быстрая». Запустите обе одновременно через tokio::join! и напечатайте «готово» после. '
                    'Ожидается: «быстрая», «медленная», «готово».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'быстрая\n'
                    'медленная\n'
                    'готово',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'join! запускает фьючеры вместе; порядок вывода определяется временем сна.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['быстрая', 'медленная', 'готово']},
      {'id': 'r30-join-results',
       'mode': 'rust',
       'title': 'join! и результаты',
       'statement': 'async fn fetch(id: u32, ms: u64) -> String: ждёт ms миллисекунд и возвращает «данные '
                    '<id>». Запустите fetch(1, 30), fetch(2, 10), fetch(3, 20) через join! и напечатайте '
                    'результаты в порядке аргументов (не времени завершения): «данные 1 / данные 2 / данные '
                    '3».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'данные 1\n'
                    'данные 2\n'
                    'данные 3',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'join! возвращает кортеж результатов в порядке аргументов.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['данные 1', 'данные 2', 'данные 3']},
      {'id': 'r30-gather-vec',
       'mode': 'rust',
       'title': 'gather для списка',
       'statement': 'Python: await asyncio.gather(*[f(i) for i in range(5)]). Запустите 5 одинаковых задач '
                    'double(i) (async, спит (5 − i)·5 мс и возвращает 2i) через futures::future::join_all и '
                    'напечатайте вектор результатов: [0, 2, 4, 6, 8].\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '[0, 2, 4, 6, 8]',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'join_all сохраняет порядок входных фьючеров.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['[0, 2, 4, 6, 8]']},
      {'id': 'r30-try-join',
       'mode': 'rust',
       'title': 'try_join! останавливается на ошибке',
       'statement': 'Две async fn: ok_task() -> Result<u32, String> (возвращает Ok(1) после 10 мс) и '
                    'bad_task() -> Result<u32, String> (Err("сбой") после 20 мс). Выполните их через '
                    'tokio::try_join! и напечатайте результат: «Err("сбой")».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'Err("сбой")',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'try_join! возвращает Err при первой ошибке.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['Err("сбой")']},
      {'id': 'r30-spawn',
       'mode': 'rust',
       'title': 'spawn вместо create_task',
       'statement': 'Запустите через tokio::spawn задачу, которая спит 20 мс и возвращает 42. Тем временем '
                    'main печатает «жду»; затем получите результат через .await хэндла (это Result): «жду», '
                    '«42».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'жду\n'
                    '42',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'JoinHandle<T>.await возвращает Result<T, JoinError>.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['жду', '42']},
      {'id': 'r30-spawn-many',
       'mode': 'rust',
       'title': 'Много задач',
       'statement': 'Запустите 100 задач spawn; задача i возвращает i·i. Соберите хэндлы в вектор, дождитесь '
                    'всех по порядку и напечатайте сумму результатов 328350.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '328350',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'async move переносит i внутрь задачи.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['328350']},
      {'id': 'r30-timeout',
       'mode': 'rust',
       'title': 'wait_for → timeout',
       'statement': 'Python: asyncio.wait_for(f(), 0.05). Запустите задачу, которая спит 200 мс, с '
                    'tokio::time::timeout на 50 мс и напечатайте «таймаут»; затем быструю (10 мс) с тем же '
                    'лимитом: «успех».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'таймаут\n'
                    'успех',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'timeout возвращает Err(Elapsed), если время вышло.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['таймаут', 'успех']},
      {'id': 'r30-select-first',
       'mode': 'rust',
       'title': 'Кто первый',
       'statement': 'Две задачи спят 30 и 70 мс. Через tokio::select! выведите имя первой завершившейся: '
                    '«быстрая».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'быстрая',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'select! выбирает первую готовую ветку и отменяет остальные.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['быстрая']},
      {'id': 'r30-spawn-blocking',
       'mode': 'rust',
       'title': 'spawn_blocking',
       'statement': 'Python: run_in_executor. Посчитайте в spawn_blocking сумму простых чисел до 20000 '
                    '(простое — без делителей до √n) и напечатайте её: 21171191.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '21171191',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'spawn_blocking возвращает JoinHandle; вычисление — в замыкании.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['21171191']},
      {'id': 'r30-block-on-bridge',
       'mode': 'rust',
       'title': 'Мост из обычного кода',
       'statement': 'В обычной fn main (без #[tokio::main]) создайте рантайм tokio::runtime::Runtime::new() '
                    'и выполните rt.block_on(async { … }), в котором ждёте 10 мс и возвращаете «из async». '
                    'Напечатайте результат.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'из async',
       'starter': 'fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Runtime::new().unwrap().block_on(…).',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['из async']},
      {'id': 'r30-futures-block-on',
       'mode': 'rust',
       'title': 'block_on из futures',
       'statement': 'Выполните async-блок без tokio: futures::executor::block_on. Блок складывает '
                    'async-функции add(2, 3) и add(10, 20) и возвращает 35. Напечатайте результат.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '35',
       'starter': 'use futures::executor::block_on;\n'
                  '\n'
                  'fn main() {\n'
                  '    block_on(async {\n'
                  '        // ваш код\n'
                  '    });\n'
                  '}\n',
       'driver': '',
       'hint': 'block_on запускает любой фьючер в текущем потоке.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['35']},
      {'id': 'r30-boxed-futures',
       'mode': 'rust',
       'title': 'Разные фьючеры в одном векторе',
       'statement': 'Соберите вектор из трёх фьючеров разных типов (async-блоки: возвращают 1, 2 и 3 после '
                    'разных пауз) в Vec<Pin<Box<dyn Future<Output = i32>>>> и выполните join_all: [1, 2, '
                    '3].\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '[1, 2, 3]',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Box::pin(async { … }) даёт Pin<Box<dyn Future>>.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['[1, 2, 3]']},
      {'id': 'r30-recursion-boxed',
       'mode': 'rust',
       'title': 'Рекурсивная async-функция',
       'statement': 'Напишите рекурсивную async-функцию fact(n: u64) -> u64 (через Box::pin(fact(n − '
                    '1)).await) и напечатайте fact(10) = 3628800.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '3628800',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Рекурсивный async fn нужно упаковать в Box::pin: размер автомата иначе бесконечен.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['3628800']},
      {'id': 'r30-stream-basic',
       'mode': 'rust',
       'title': 'Поток значений',
       'statement': 'Python: async for. Из futures::stream::iter(1..=5) через StreamExt: .map(|x| x * '
                    'x).filter(|x| ready(x % 2 == 1)).collect::<Vec<_>>().await — напечатайте [1, 9, 25].\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '[1, 9, 25]',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'StreamExt::filter принимает замыкание, возвращающее фьючер: ready(bool).',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['[1, 9, 25]']},
      {'id': 'r30-unordered',
       'mode': 'rust',
       'title': 'Порядок завершения',
       'statement': 'Python: asyncio.as_completed. Запустите в FuturesUnordered три задачи, спящие 30, 10 и '
                    '20 мс и возвращающие своё время, и выведите результаты в порядке завершения: 10, 20, '
                    '30.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '10\n'
                    '20\n'
                    '30',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'FuturesUnordered выдаёт результаты по мере готовности.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['10', '20', '30']},
      {'id': 'r30-joinset',
       'mode': 'rust',
       'title': 'TaskGroup → JoinSet',
       'statement': 'Запустите в JoinSet пять задач, i-я спит (5 − i)·4 мс и возвращает i. Соберите '
                    'результаты по мере завершения в вектор и напечатайте его отсортированным: [0, 1, 2, 3, '
                    '4], а также порядок завершения: [4, 3, 2, 1, 0].\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '[3, 4, 2, 1, 0]\n'
                    '[0, 1, 2, 3, 4]',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'set.join_next().await возвращает Option<Result<T, JoinError>>.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['[3, 4, 2, 1, 0]', '[0, 1, 2, 3, 4]']},
      {'id': 'r30-panic-isolated',
       'mode': 'rust',
       'title': 'Паника в задаче',
       'statement': 'Запустите через spawn задачу, которая паникует (panic!("бум")), и вторую, возвращающую '
                    '7. Напечатайте: есть ли ошибка у первой (JoinError, is_panic) — «true» и значение '
                    'второй — «7». Сообщение паники в stderr не проверяется.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'true\n'
                    '7',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Паника изолируется в задаче и приходит как JoinError.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['true', '7']},
      {'id': 'r30-abort',
       'mode': 'rust',
       'title': 'Отмена задачи',
       'statement': 'Запустите задачу, которая бесконечно в цикле спит 5 мс и увеличивает общий AtomicUsize. '
                    'Дождитесь в main, пока счётчик станет не меньше 2 (опрашивайте через sleep 5 мс), '
                    'отмените задачу методом abort() и напечатайте: «отменено», затем is_cancelled у ошибки '
                    'await — «true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'отменено\n'
                    'true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'abort() прерывает задачу на ближайшем .await.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['отменено', 'true']},
      {'id': 'r30-send-bound',
       'mode': 'rust',
       'title': 'Send и spawn',
       'statement': 'Напишите функцию run<F>(f: F) -> impl Future<Output = u32>, где F: Future<Output = u32> '
                    "+ Send + 'static и которая запускает f через tokio::spawn и ждёт результата (unwrap). "
                    'Передайте async { 5 + 6 } и напечатайте 11.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '11',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': "spawn требует Send + 'static.",
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['11']},
      {'id': 'r30-async-block-move',
       'mode': 'rust',
       'title': 'async move и владение',
       'statement': 'Создайте String s = «привет», переместите её в async move-блок, который возвращает '
                    's.len(), выполните и напечатайте 12. После блока s недоступна (не используйте её).\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '12',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'async move забирает захваченные значения во владение.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['12']},
      {'id': 'r30-yield-now',
       'mode': 'rust',
       'title': 'Уступить управление',
       'statement': 'На однопоточном рантайме (#[tokio::main(flavor = "current_thread")]) запустите задачу, '
                    'которая крутится в цикле «пока флаг done не поднят — yield_now().await», считает '
                    'итерации и затем печатает «задача завершилась». Main даёт ей поработать одним '
                    'yield_now, поднимает флаг (AtomicBool), ждёт задачу и печатает «итераций>=1: true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'задача завершилась\n'
                    'итераций>=1: true',
       'starter': '#[tokio::main(flavor = "current_thread")]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'На одном потоке задача не продвинется, пока main не уступит управление.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['задача завершилась', 'итераций>=1: true']},
      {'id': 'r30-interval',
       'mode': 'rust',
       'title': 'Периодические события',
       'statement': 'Python: while True: await asyncio.sleep(…). Создайте tokio::time::interval(20 мс) и '
                    'дождитесь четырёх тиков, замерив общее время: напечатайте «4 тика» и «время >= 60 мс: '
                    'true» (первый тик срабатывает сразу).\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '4 тика\n'
                    'время >= 60 мс: true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Первый tick() срабатывает сразу, остальные — через период.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['4 тика', 'время >= 60 мс: true']},
      {'id': 'r30-mpsc-intro',
       'mode': 'rust',
       'title': 'Очередь между задачами',
       'statement': 'Python: asyncio.Queue. Создайте tokio::sync::mpsc::channel(8); задача-производитель '
                    'отправляет числа 1…5 и завершается; main принимает через rx.recv().await до закрытия и '
                    'печатает сумму 15.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '15',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'recv возвращает None, когда все отправители уничтожены.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['15']},
      {'id': 'r30-mutex-intro',
       'mode': 'rust',
       'title': 'Общее состояние',
       'statement': 'Запустите 10 задач, каждая добавляет 100 раз по 1 в общий счётчик '
                    'Arc<tokio::sync::Mutex<u32>>. Напечатайте итог 1000.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '1000',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Arc клонируется в каждую задачу; lock().await возвращает guard.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['1000']},
      {'id': 'r30-oneshot',
       'mode': 'rust',
       'title': 'Один ответ',
       'statement': 'Создайте oneshot-канал; задача отправляет «ответ» через 10 мс; main ждёт rx.await и '
                    'печатает «получено: ответ».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'получено: ответ',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'oneshot::channel() — один отправитель, один получатель, одно значение.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['получено: ответ']}]}
