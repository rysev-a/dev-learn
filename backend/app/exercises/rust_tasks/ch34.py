"""Задачи книги «Изучаем Rust»: глава 34 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {34: [{'id': 'r34-sleep-elapsed',
  'mode': 'rust',
  'title': 'sleep и elapsed',
  'statement': 'Запомните Instant::now(), усните на 100 мс через tokio::time::sleep и напечатайте '
               '«прошло не меньше 100 мс: true» (сравните elapsed() с '
               'Duration::from_millis(100)).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'прошло не меньше 100 мс: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'start.elapsed() >= Duration::from_millis(100).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['прошло не меньше 100 мс: true']},
 {'id': 'r34-fix-thread-sleep',
  'mode': 'rust',
  'title': 'Исправьте: блокирующий sleep',
  'statement': 'Три задачи спят блокирующим std::thread::sleep на однопоточном рантайме, поэтому '
               'выполняются одна за другой. Исправьте программу, чтобы они спали одновременно: '
               'нужно «быстро: true».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'быстро: true',
  'starter': 'use std::time::{Duration, Instant};\n'
             '\n'
             '#[tokio::main(flavor = "current_thread")]\n'
             'async fn main() {\n'
             '    let start = Instant::now();\n'
             '    let mut hs = Vec::new();\n'
             '    for _ in 0..3 {\n'
             '        hs.push(tokio::spawn(async {\n'
             '            std::thread::sleep(Duration::from_millis(100));\n'
             '        }));\n'
             '    }\n'
             '    for h in hs {\n'
             '        h.await.unwrap();\n'
             '    }\n'
             '    println!("быстро: {}", start.elapsed() < Duration::from_millis(250));\n'
             '}\n',
  'driver': '',
  'hint': 'Замените std::thread::sleep(..) на tokio::time::sleep(..).await — задача отдаст поток.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['быстро: true']},
 {'id': 'r34-join-sleeps',
  'mode': 'rust',
  'title': 'Три сна одновременно',
  'statement': 'Через tokio::join! запустите три сна по 100 мс одновременно и напечатайте '
               '«параллельно: true», если всё заняло меньше 200 мс.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'параллельно: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::join!(sleep(d), sleep(d), sleep(d)).await не нужен: join! уже возвращает фьючер, '
          'его ждут .await.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['параллельно: true']},
 {'id': 'r34-sleep-until',
  'mode': 'rust',
  'title': 'sleep_until',
  'statement': 'Вычислите дедлайн: Instant::now() + 120 мс, дождитесь его через sleep_until и '
               'напечатайте «дедлайн достигнут: true» (Instant::now() >= deadline).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'дедлайн достигнут: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'time::sleep_until(deadline).await.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['дедлайн достигнут: true']},
 {'id': 'r34-completion-order',
  'mode': 'rust',
  'title': 'Порядок завершения',
  'statement': 'Запустите три задачи: «a» спит 60 мс, «b» — 20 мс, «c» — 40 мс; каждая после сна '
               'печатает своё имя. Дождитесь всех. Порядок вывода определяют сны.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'b\n'
               'c\n'
               'a',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Для каждой задачи tokio::spawn(async move { sleep(..).await; println!(..) }); потом '
          '.await на каждом JoinHandle.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['b', 'c', 'a']},
 {'id': 'r34-timeout-ok',
  'mode': 'rust',
  'title': 'timeout: успел',
  'statement': 'Оберните async-блок (сон 20 мс, затем возвращает 5) в timeout 200 мс и напечатайте '
               'результат через {:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Ok(5)',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'time::timeout(Duration, future).await возвращает Result<T, Elapsed>.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Ok(5)']},
 {'id': 'r34-timeout-err',
  'mode': 'rust',
  'title': 'timeout: не успел',
  'statement': 'Оберните сон на 200 мс в timeout на 30 мс. Если вернулась ошибка, напечатайте её '
               'через {} (Display у Elapsed).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'deadline has elapsed',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'if let Err(e) = r { println!("{}", e); }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['deadline has elapsed']},
 {'id': 'r34-timeout-map-err',
  'mode': 'rust',
  'title': 'Elapsed в свою ошибку',
  'statement': 'Напишите async fn fetch() -> Result<u32, String>: ожидает сон 200 мс через timeout '
               'на 30 мс и превращает Elapsed в строку «таймаут» методом map_err. Напечатайте '
               'результат через {:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Err("таймаут")',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'time::timeout(..).await.map_err(|_| "таймаут".to_string()) — получится Result<(), '
          'String>.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Err("таймаут")']},
 {'id': 'r34-timeout-at',
  'mode': 'rust',
  'title': 'Общий дедлайн',
  'statement': 'Задайте дедлайн «сейчас + 100 мс». Выполните два шага подряд, каждый — сон 60 мс, '
               'и оба ограничьте timeout_at(deadline, ..). Для каждого напечатайте «шаг N: ok» или '
               '«шаг N: просрочен».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'шаг 1: ok\n'
               'шаг 2: просрочен',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Дедлайн один на оба шага: второй шаг уже не успевает.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['шаг 1: ok', 'шаг 2: просрочен']},
 {'id': 'r34-first-tick',
  'mode': 'rust',
  'title': 'Первый тик сразу',
  'statement': 'Создайте interval на 100 мс, дождитесь первого tick() и напечатайте «первый тик '
               'сразу: true», если прошло меньше 30 мс.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'первый тик сразу: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'time::interval(Duration) — первый tick() возвращается немедленно.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['первый тик сразу: true']},
 {'id': 'r34-four-ticks',
  'mode': 'rust',
  'title': 'Четыре тика',
  'statement': 'Interval на 50 мс: дождитесь 4 тиков (первый сразу). Напечатайте «4 тика за '
               '140–220 мс: true», если общее время попало в этот диапазон.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '4 тика за 140–220 мс: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Тики на 0, 50, 100 и 150 мс — около 150 мс в сумме.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['4 тика за 140–220 мс: true']},
 {'id': 'r34-no-drift',
  'mode': 'rust',
  'title': 'Интервал без дрейфа',
  'statement': '5 раз выполните: tick() интервала 50 мс, затем «работа» (сон 20 мс). Напечатайте '
               '«без дрейфа: true», если всё заняло меньше 300 мс. (С sleep(50) вместо интервала '
               'получилось бы около 350 мс.)\n'
               '\n'
               'Ожидаемый вывод:\n'
               'без дрейфа: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Период интервала отсчитывается от запуска, а не от конца работы.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['без дрейфа: true']},
 {'id': 'r34-missed-delay',
  'mode': 'rust',
  'title': 'MissedTickBehavior::Delay',
  'statement': 'Interval на 50 мс с MissedTickBehavior::Delay. Возьмите первый тик, усните на 120 '
               'мс (тики опоздали), возьмите второй тик (он срабатывает сразу), затем замерьте '
               'время до третьего. Напечатайте «пауза после опоздания: true», если оно не меньше '
               '45 мс.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'пауза после опоздания: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'iv.set_missed_tick_behavior(time::MissedTickBehavior::Delay).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['пауза после опоздания: true']},
 {'id': 'r34-missed-burst',
  'mode': 'rust',
  'title': 'MissedTickBehavior::Burst',
  'statement': 'Тот же сценарий с поведением по умолчанию (Burst): первый тик, сон 120 мс, затем '
               'два тика подряд. Напечатайте «Burst подряд: true», если второй пришёл менее чем '
               'через 20 мс после первого из них.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Burst подряд: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Burst отдаёт пропущенные тики без пауз, чтобы догнать расписание.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Burst подряд: true']},
 {'id': 'r34-missed-skip',
  'mode': 'rust',
  'title': 'MissedTickBehavior::Skip',
  'statement': 'Interval на 50 мс с MissedTickBehavior::Skip. Первый тик, сон 120 мс (пропущены '
               'тики на 50 и 100), затем один tick() (он опоздал и срабатывает сразу) и замер '
               'ожидания следующего tick(). Напечатайте «Skip ждёт сетку: true», если оно от 10 до '
               '50 мс (до тика на 150-й мс).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Skip ждёт сетку: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Skip отбрасывает пропущенные и ждёт ближайший тик исходной сетки.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Skip ждёт сетку: true']},
 {'id': 'r34-interval-reset',
  'mode': 'rust',
  'title': 'reset интервала',
  'statement': 'Interval на 100 мс: первый тик сразу, усните 30 мс, вызовите reset(), замерьте '
               'следующий tick(). Напечатайте «после reset ждали ≥ 90 мс: true».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'после reset ждали ≥ 90 мс: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'reset() сдвигает следующий тик на полный период от текущего момента.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['после reset ждали ≥ 90 мс: true']},
 {'id': 'r34-interval-at',
  'mode': 'rust',
  'title': 'interval_at',
  'statement': 'Создайте interval_at(Instant::now() + 100 мс, 50 мс), замерьте первый tick(). '
               'Напечатайте «первый тик позже: true», если прошло не меньше 95 мс.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'первый тик позже: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'interval_at(start, period): первый тик — в момент start.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['первый тик позже: true']},
 {'id': 'r34-select-first',
  'mode': 'rust',
  'title': 'Кто первый',
  'statement': 'В select! ждите два сна: 20 мс (печатает «a») и 100 мс (печатает «b»). Выполнится '
               'только первый.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'a',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::select! { _ = sleep(..) => println!(..), _ = sleep(..) => println!(..) }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['a']},
 {'id': 'r34-select-timeout',
  'mode': 'rust',
  'title': 'select! как таймаут',
  'statement': 'В select! ждите медленную операцию (async-блок: сон 200 мс, затем возвращает '
               '«готово») и сон 50 мс. Если победила операция — напечатайте её значение, иначе — '
               '«тайм-аут».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'тайм-аут',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'v = async { .. } => println!("{v}"), _ = sleep(..) => println!("тайм-аут")',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['тайм-аут']},
 {'id': 'r34-select-value',
  'mode': 'rust',
  'title': 'select! как выражение',
  'statement': 'Присвойте результат select! переменной: первая ветка — async-блок со сном 30 мс и '
               'значением 1, вторая — сон 10 мс и значение 2. Напечатайте переменную.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '2',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let r = tokio::select! { v = f1 => v, v = f2 => v };',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['2']},
 {'id': 'r34-select-else',
  'mode': 'rust',
  'title': 'Ветка else',
  'statement': 'Заведите let ready = false; и в select! поставьте ветку со сном 10 мс с условием '
               '`if ready` и ветку else. Напечатайте «else» из else-ветки.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'else',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': '_ = sleep(..), if ready => .., else => println!("else")',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['else']},
 {'id': 'r34-select-biased',
  'mode': 'rust',
  'title': 'biased',
  'statement': 'В цикле на 100 итераций вызывайте select! с biased; и двумя сразу готовыми ветками '
               '(std::future::ready(())). Считайте, сколько раз победила первая. Напечатайте '
               '«первая ветка: 100».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'первая ветка: 100',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::select! { biased; _ = ready(()) => first += 1, _ = ready(()) => {} }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['первая ветка: 100']},
 {'id': 'r34-select-fair',
  'mode': 'rust',
  'title': 'Справедливый выбор',
  'statement': 'Без biased; в цикле на 1000 итераций вызывайте select! с двумя готовыми ветками и '
               'считайте победы каждой. Напечатайте «обе выигрывали: true», если у обеих победы '
               'больше нуля.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'обе выигрывали: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'По умолчанию порядок опроса случаен, поэтому выигрывают обе ветки.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['обе выигрывали: true']},
 {'id': 'r34-select-drop',
  'mode': 'rust',
  'title': 'Проигравший отбрасывается',
  'statement': "Заведите структуру Guard(&'static str) с Drop, который печатает «drop <имя>». В "
               'select! первая ветка — async-блок: создаёт Guard("медленный") и спит 200 мс; '
               'вторая — сон 10 мс. После select! напечатайте «после select». Посмотрите, в каком '
               'порядке появились строки: проигравший фьючер отбрасывается (и Guard вместе с ним) '
               'до этого.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'drop медленный\n'
               'после select',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Guard живёт внутри async-блока: он освобождается, когда блок отбрасывают.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['drop медленный', 'после select']},
 {'id': 'r34-fix-pin-loop',
  'mode': 'rust',
  'title': 'Исправьте: сон в цикле select!',
  'statement': 'Отправитель шлёт сообщения каждые 50 мс. Нужно остановить цикл через 125 мс от '
               'старта, но сон создаётся заново на каждой итерации и никогда не срабатывает. '
               'Исправьте: создайте сон до цикла, закрепите (tokio::pin!) и передайте в select! по '
               '&mut. Ожидается «сообщений: 2».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'сообщений: 2',
  'starter': 'use std::time::Duration;\n'
             'use tokio::sync::mpsc;\n'
             'use tokio::time::sleep;\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let (tx, mut rx) = mpsc::channel::<u32>(8);\n'
             '    tokio::spawn(async move {\n'
             '        for i in 0..6 {\n'
             '            sleep(Duration::from_millis(50)).await;\n'
             '            if tx.send(i).await.is_err() {\n'
             '                break;\n'
             '            }\n'
             '        }\n'
             '    });\n'
             '    let mut got = 0;\n'
             '    loop {\n'
             '        tokio::select! {\n'
             '            _ = sleep(Duration::from_millis(125)) => break,\n'
             '            m = rx.recv() => {\n'
             '                if m.is_none() {\n'
             '                    break;\n'
             '                }\n'
             '                got += 1;\n'
             '            }\n'
             '        }\n'
             '    }\n'
             '    println!("сообщений: {got}");\n'
             '}\n',
  'driver': '',
  'hint': 'let deadline = sleep(..); tokio::pin!(deadline); и в select! — _ = &mut deadline => '
          'break.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['сообщений: 2']},
 {'id': 'r34-recv-cancel-safe',
  'mode': 'rust',
  'title': 'recv безопасен к отмене',
  'statement': 'Отправитель шлёт числа 1, 2, 3 с паузой 40 мс и закрывает канал. Получатель в '
               'цикле: select! между rx.recv() и сном на 15 мс (сон лишь считает «пустые» ожидания '
               'и отбрасывает recv). Все сообщения должны дойти. Напечатайте «получено: 3».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'получено: 3',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'recv() можно отбрасывать безопасно: сообщение остаётся в канале.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['получено: 3']},
 {'id': 'r34-retry-backoff',
  'mode': 'rust',
  'title': 'Повтор с растущей паузой',
  'statement': 'Напишите повтор: операция падает на первых двух попытках (Err("fail")) и удаётся '
               'на третьей. После неудач ждите 20 мс, затем 40 мс (удвоение). Для каждой попытки '
               'печатайте «попытка N: fail» или «попытка N: ok», а в конце — «ждали не меньше 60 '
               'мс: true».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'попытка 1: fail\n'
               'попытка 2: fail\n'
               'попытка 3: ok\n'
               'ждали не меньше 60 мс: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Цикл по попыткам; после неудачи sleep(delay).await и delay *= 2.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['попытка 1: fail',
               'попытка 2: fail',
               'попытка 3: ok',
               'ждали не меньше 60 мс: true']},
 {'id': 'r34-attempt-timeout',
  'mode': 'rust',
  'title': 'Таймаут на каждую попытку',
  'statement': 'Операция attempt(n): первые две попытки спят 200 мс, третья возвращает 42 сразу. '
               'Ограничьте каждую попытку timeout на 50 мс. Печатайте «попытка N: таймаут» или '
               '«попытка N: 42».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'попытка 1: таймаут\n'
               'попытка 2: таймаут\n'
               'попытка 3: 42',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'for n in 1..=3 { match timeout(.., attempt(n)).await { Ok(v) => .., Err(_) => .. } }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['попытка 1: таймаут', 'попытка 2: таймаут', 'попытка 3: 42']},
 {'id': 'r34-nested-timeout',
  'mode': 'rust',
  'title': 'Вложенные таймауты',
  'statement': 'Внутренний timeout 30 мс оборачивает сон 80 мс, внешний timeout 200 мс оборачивает '
               'внутренний. Напечатайте «внутренний: просрочен, внешний: ok».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'внутренний: просрочен, внешний: ok',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Внешний вернёт Ok(Err(Elapsed)): сам он успел, а внутренний — нет.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['внутренний: просрочен, внешний: ok']},
 {'id': 'r34-heartbeat',
  'mode': 'rust',
  'title': 'Сердцебиение',
  'statement': 'В цикле select! соедините interval 100 мс (считайте тики) и общий дедлайн 250 мс '
               '(sleep, закреплённый до цикла). Когда дедлайн сработает, выйдите и напечатайте '
               '«сердцебиений: 3» (тики на 0, 100 и 200 мс).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'сердцебиений: 3',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::pin! для дедлайна; в select! — _ = &mut deadline => break и _ = iv.tick() => n '
          '+= 1.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['сердцебиений: 3']}]}
