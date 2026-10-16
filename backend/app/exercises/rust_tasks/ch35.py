"""Задачи книги «Изучаем Rust»: глава 35 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {35: [{'id': 'r35-mpsc-basic',
  'mode': 'rust',
  'title': 'Первый канал',
  'statement': 'Создайте mpsc::channel(4). Из запущенной задачи отправьте 1, 2, 3 (и закройте '
               'канал, уничтожив отправитель). В main читайте через while let Some(v) = '
               'rx.recv().await и печатайте значения, а после цикла — «конец».\n'
               '\n'
               'Ожидаемый вывод:\n'
               '1\n'
               '2\n'
               '3\n'
               'конец',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Sender переезжает в задачу через async move; когда он уничтожен, recv() вернёт None.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['1', '2', '3', 'конец']},
 {'id': 'r35-mpsc-producers',
  'mode': 'rust',
  'title': 'Несколько производителей',
  'statement': 'Запустите три задачи, каждая отправляет свой номер 0, 1, 2 по общему каналу '
               '(tx.clone()). Соберите все значения, отсортируйте и напечатайте вектор через '
               '{:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[0, 1, 2]',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Исходный tx уничтожьте (drop), иначе recv() не закончится.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[0, 1, 2]']},
 {'id': 'r35-recv-none',
  'mode': 'rust',
  'title': 'Закрытый канал',
  'statement': 'Создайте канал mpsc::channel::<u32>(1), уничтожьте отправителя и напечатайте '
               'rx.recv().await через {:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'None',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Закрытый и пустой канал возвращает None.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['None']},
 {'id': 'r35-send-closed',
  'mode': 'rust',
  'title': 'Нет получателя',
  'statement': 'Создайте канал, уничтожьте получателя и отправьте значение. Напечатайте «отправка '
               'не удалась: true», если send вернул ошибку.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'отправка не удалась: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tx.send(1).await.is_err() после drop(rx).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['отправка не удалась: true']},
 {'id': 'r35-try-send',
  'mode': 'rust',
  'title': 'try_send и переполнение',
  'statement': 'Канал ёмкостью 2. Три раза вызовите try_send: для успешных печатайте «ok», для '
               'переполнения (TrySendError::Full) — «переполнен».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ok\n'
               'ok\n'
               'переполнен',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'use tokio::sync::mpsc::error::TrySendError; match tx.try_send(i) { Ok(()) => .., '
          'Err(TrySendError::Full(_)) => .., _ => .. }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ok', 'ok', 'переполнен']},
 {'id': 'r35-capacity',
  'mode': 'rust',
  'title': 'capacity',
  'statement': 'Канал ёмкостью 3. Напечатайте tx.capacity() до отправки и после одной отправки '
               '(send без ожидания: try_send).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '3\n'
               '2',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'capacity() — сколько свободного места осталось.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['3', '2']},
 {'id': 'r35-reserve',
  'mode': 'rust',
  'title': 'reserve и permit',
  'statement': 'Канал ёмкостью 1. Зарезервируйте место через tx.reserve().await, отправьте 5 через '
               'разрешение (permit.send(5)) и напечатайте rx.recv().await через {:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Some(5)',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let permit = tx.reserve().await.unwrap(); permit.send(5);',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Some(5)']},
 {'id': 'r35-unbounded',
  'mode': 'rust',
  'title': 'Неограниченный канал',
  'statement': 'Через mpsc::unbounded_channel отправьте числа от 0 до 999 (send без .await), '
               'уничтожьте отправитель и напечатайте «сумма: …» (сложите всё, что принято).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'сумма: 499500',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tx.send(i).unwrap(); потом drop(tx) и while let Some(v) = rx.recv().await.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['сумма: 499500']},
 {'id': 'r35-order',
  'mode': 'rust',
  'title': 'Порядок от одного отправителя',
  'statement': 'Одна задача отправляет 0, 1, 2, 3, 4; получатель собирает значения в вектор. '
               'Напечатайте вектор через {:?}: порядок сохраняется.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[0, 1, 2, 3, 4]',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'mpsc сохраняет порядок сообщений одного отправителя.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[0, 1, 2, 3, 4]']},
 {'id': 'r35-oneshot',
  'mode': 'rust',
  'title': 'oneshot: результат задачи',
  'statement': 'Запустите задачу, которая отправляет по oneshot-каналу 21 * 2. Дождитесь значения '
               'через rx.await и напечатайте его.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '42',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let (tx, rx) = oneshot::channel(); tx.send(..); rx.await.unwrap().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['42']},
 {'id': 'r35-request-reply',
  'mode': 'rust',
  'title': 'Запрос с ответом',
  'statement': 'Запустите рабочую задачу: она принимает по mpsc пары (u32, oneshot::Sender<u32>) и '
               'отвечает квадратом числа. Отправьте запрос (5, reply_tx) и напечатайте ответ.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '25',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Рабочий: while let Some((n, reply)) = rx.recv().await { reply.send(n * n).ok(); }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['25']},
 {'id': 'r35-oneshot-dropped',
  'mode': 'rust',
  'title': 'Отправитель oneshot пропал',
  'statement': 'Создайте oneshot-канал, уничтожьте отправитель без отправки и напечатайте ошибку '
               'от rx.await через {} (Display у RecvError).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'channel closed',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'if let Err(e) = rx.await { println!("{}", e); }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['channel closed']},
 {'id': 'r35-oneshot-try-recv',
  'mode': 'rust',
  'title': 'try_recv у oneshot',
  'statement': 'Создайте oneshot-канал. Напечатайте rx.try_recv() через {:?} до отправки, затем '
               'отправьте 7 и напечатайте try_recv() снова.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Err(Empty)\n'
               'Ok(7)',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Receiver должен быть изменяемым: let (tx, mut rx) = …',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Err(Empty)', 'Ok(7)']},
 {'id': 'r35-broadcast',
  'mode': 'rust',
  'title': 'Рассылка двум получателям',
  'statement': 'Создайте broadcast::channel(8) и двух подписчиков (tx.subscribe()). Отправьте «a» '
               'и «b». Каждый подписчик читает два сообщения. Напечатайте «r1: a b» и «r2: a b».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'r1: a b\n'
               'r2: a b',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Каждый подписчик получает копию каждого сообщения.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['r1: a b', 'r2: a b']},
 {'id': 'r35-broadcast-lagged',
  'mode': 'rust',
  'title': 'Отставший подписчик',
  'statement': 'broadcast::channel(2): отправьте 1, 2, 3, 4, не читая. Затем читайте: на ошибку '
               'Lagged(n) напечатайте «пропущено n», значения печатайте как есть, до конца буфера '
               '(3 чтения).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'пропущено 2\n'
               '3\n'
               '4',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'use tokio::sync::broadcast::error::RecvError; Err(RecvError::Lagged(n)) => ..',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['пропущено 2', '3', '4']},
 {'id': 'r35-broadcast-late',
  'mode': 'rust',
  'title': 'Поздняя подписка',
  'statement': 'Создайте broadcast-канал, отправьте «old», затем подпишитесь (subscribe) и '
               'напечатайте late.try_recv() через {:?}: старое сообщение подписчик не увидит.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Err(Empty)',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Сохраните первого получателя (let (tx, _rx)), иначе send вернёт ошибку.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Err(Empty)']},
 {'id': 'r35-watch-borrow',
  'mode': 'rust',
  'title': 'watch: текущее значение',
  'statement': 'Создайте watch::channel(0), отправьте 5 и напечатайте *rx.borrow().\n'
               '\n'
               'Ожидаемый вывод:\n'
               '5',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tx.send(5).unwrap(); *rx.borrow().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['5']},
 {'id': 'r35-watch-changed',
  'mode': 'rust',
  'title': 'watch: ждём изменений',
  'statement': 'Задача обновляет значение watch-канала: 1, 2, 3 с паузой 40 мс между обновлениями '
               'и затем завершается. В main ждите rx.changed().await в цикле и печатайте новое '
               'значение.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '1\n'
               '2\n'
               '3',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'while rx.changed().await.is_ok() { println!("{}", *rx.borrow()); }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['1', '2', '3']},
 {'id': 'r35-mutex-counter',
  'mode': 'rust',
  'title': 'Счётчик под Mutex',
  'statement': 'Десять задач увеличивают общий счётчик Arc<tokio::sync::Mutex<u32>> на 1. '
               'Дождитесь всех и напечатайте значение.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '10',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': '*m.lock().await += 1;',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['10']},
 {'id': 'r35-mutex-across-await',
  'mode': 'rust',
  'title': 'Замок через await',
  'statement': 'Две задачи берут один tokio::sync::Mutex, держат охранника во время sleep 50 мс. '
               'Напечатайте «последовательно: true», если вся работа заняла не меньше 90 мс.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'последовательно: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let _g = m.lock().await; sleep(..).await; — охранник живёт до конца блока.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['последовательно: true']},
 {'id': 'r35-fix-std-mutex',
  'mode': 'rust',
  'title': 'Исправьте: std Mutex через await',
  'statement': 'Программа не компилируется: охранник std::sync::Mutex живёт через .await внутри '
               'spawn. Исправьте, сократив его время жизни (увеличивайте счётчик в отдельном блоке '
               'до sleep). Ожидается «счётчик: 1».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'счётчик: 1',
  'starter': 'use std::sync::{Arc, Mutex};\n'
             'use std::time::Duration;\n'
             'use tokio::time::sleep;\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let m = Arc::new(Mutex::new(0));\n'
             '    let m2 = Arc::clone(&m);\n'
             '    let h = tokio::spawn(async move {\n'
             '        let mut g = m2.lock().unwrap();\n'
             '        *g += 1;\n'
             '        sleep(Duration::from_millis(10)).await;\n'
             '    });\n'
             '    h.await.unwrap();\n'
             '    println!("счётчик: {}", *m.lock().unwrap());\n'
             '}\n',
  'driver': '',
  'hint': 'Оберните let mut g … *g += 1; в отдельные фигурные скобки до .await — охранник '
          'уничтожится раньше.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['счётчик: 1']},
 {'id': 'r35-rwlock',
  'mode': 'rust',
  'title': 'RwLock: писатель и читатели',
  'statement': 'Положите число в Arc<RwLock<u32>>: сначала запишите 10, затем запустите три '
               'читающие задачи, каждая возвращает прочитанное. Сложите результаты и напечатайте '
               '«сумма: …».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'сумма: 30',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': '*lock.write().await = 10; let v = *lock.read().await;',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['сумма: 30']},
 {'id': 'r35-semaphore-limit',
  'mode': 'rust',
  'title': 'Ограничение параллелизма',
  'statement': 'Семафор на 2 разрешения, шесть задач: каждая берёт разрешение, увеличивает счётчик '
               'одновременно работающих (AtomicUsize), обновляет максимум, спит 50 мс и уменьшает '
               'счётчик. Напечатайте «максимум одновременно: 2».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'максимум одновременно: 2',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'cur.fetch_add(1) + 1; max.fetch_max(now); потом cur.fetch_sub(1).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['максимум одновременно: 2']},
 {'id': 'r35-acquire-owned',
  'mode': 'rust',
  'title': 'acquire_owned',
  'statement': 'Семафор Arc::new(Semaphore::new(3)): запустите три задачи, каждая получает '
               'разрешение через acquire_owned().await (оно переезжает внутрь задачи) и спит 30 '
               'мс. После всех напечатайте available_permits().\n'
               '\n'
               'Ожидаемый вывод:\n'
               '3',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'sem.clone().acquire_owned().await.unwrap() — разрешение с владением.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['3']},
 {'id': 'r35-try-acquire',
  'mode': 'rust',
  'title': 'try_acquire',
  'statement': 'Семафор на одно разрешение. Первый try_acquire — успех (напечатайте «ok»), и пока '
               'разрешение держится, второй — отказ (напечатайте «занято»).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ok\n'
               'занято',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let p = sem.try_acquire(); … sem.try_acquire().is_err()',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ok', 'занято']},
 {'id': 'r35-notify',
  'mode': 'rust',
  'title': 'Notify: разбудить задачу',
  'statement': 'Задача ждёт notify.notified().await и затем печатает «проснулась». Главная задача '
               'печатает «будим» и вызывает notify_one(), после чего дожидается завершения.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'будим\n'
               'проснулась',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Notify в Arc; ждущая задача — spawn; будить notify.notify_one().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['будим', 'проснулась']},
 {'id': 'r35-notify-permit',
  'mode': 'rust',
  'title': 'Notify: запомненное разрешение',
  'statement': 'Вызовите notify_one() до ожидания, затем notified().await — он не должен '
               'заблокироваться. Напечатайте «не блокируется».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'не блокируется',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Notify запоминает одно разрешение, если никто не ждёт.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['не блокируется']},
 {'id': 'r35-barrier',
  'mode': 'rust',
  'title': 'Barrier',
  'statement': 'Barrier::new(3) и три задачи: каждая увеличивает общий счётчик AtomicUsize, затем '
               'ждёт на барьере и после него проверяет, что счётчик равен 3. Напечатайте «все '
               'видят 3: true».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'все видят 3: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'barrier.wait().await; после барьера все три увеличения уже сделаны.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['все видят 3: true']},
 {'id': 'r35-actor',
  'mode': 'rust',
  'title': 'Актор-счётчик',
  'statement': 'Напишите актор: задача владеет счётчиком и принимает команды enum Cmd { Add(u32), '
               'Get(oneshot::Sender<u32>) } по mpsc. Отправьте Add(3), Add(3), Add(4), затем Get и '
               'напечатайте ответ.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '10',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Актор: let mut total = 0; while let Some(cmd) = rx.recv().await { match cmd { .. } }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['10']},
 {'id': 'r35-worker-pool',
  'mode': 'rust',
  'title': 'Пул рабочих',
  'statement': 'Три рабочих берут задания из общего канала (приёмник в '
               'Arc<tokio::sync::Mutex<Receiver<u32>>>), считают квадрат и отправляют результат в '
               'канал результатов. Отправьте задания 1…9, закройте канал заданий и напечатайте '
               '«сумма квадратов: …».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'сумма квадратов: 285',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Рабочий: let job = { let mut g = rx.lock().await; g.recv().await }; None — выход из '
          'цикла.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['сумма квадратов: 285']}]}
