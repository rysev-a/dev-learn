"""Задачи книги «Изучаем Rust»: глава 36 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {36: [{'id': 'r36-bind-port0',
  'mode': 'rust',
  'title': 'Порт 0',
  'statement': 'Привяжите TcpListener к 127.0.0.1:0, возьмите порт из local_addr() и напечатайте '
               '«порт больше нуля: true».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'порт больше нуля: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'TcpListener::bind("127.0.0.1:0").await?.local_addr()?.port()',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['порт больше нуля: true']},
 {'id': 'r36-accept-connect',
  'mode': 'rust',
  'title': 'Сервер принял клиента',
  'statement': 'Запустите сервер в задаче: он принимает одно соединение и печатает «подключился». '
               'Клиент в main подключается (TcpStream::connect). Дождитесь задачи сервера.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'подключился',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Адрес возьмите у listener.local_addr() до spawn.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['подключился']},
 {'id': 'r36-write-read',
  'mode': 'rust',
  'title': 'Отправить и прочитать',
  'statement': 'Клиент отправляет «привет» и закрывает соединение. Сервер читает до конца '
               '(read_to_end) и печатает «получено: привет».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'получено: привет',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Клиента уничтожьте (drop) — сервер получит EOF.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['получено: привет']},
 {'id': 'r36-read-zero',
  'mode': 'rust',
  'title': 'read вернул 0',
  'statement': 'Клиент подключается и сразу закрывает соединение. Сервер вызывает read один раз и '
               'печатает «EOF: n», где n — число прочитанных байт.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'EOF: 0',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Закрытое собеседником соединение: read возвращает Ok(0).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['EOF: 0']},
 {'id': 'r36-echo-once',
  'mode': 'rust',
  'title': 'Эхо на одно сообщение',
  'statement': 'Сервер читает до 64 байт (один read) и отправляет их обратно. Клиент отправляет '
               '«ping», читает ответ и печатает «echo: ping».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'echo: ping',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Сервер: let n = s.read(&mut buf).await?; s.write_all(&buf[..n]).await?.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['echo: ping']},
 {'id': 'r36-echo-loop',
  'mode': 'rust',
  'title': 'Эхо-сервер для многих',
  'statement': 'Напишите сервер с циклом accept и spawn на каждого клиента: обработчик читает и '
               'пишет обратно, пока не получит EOF. Три клиента по очереди подключаются, '
               'отправляют «id N», читают ответ и печатают «эхо N» для N = 0, 1, 2.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'эхо 0\n'
               'эхо 1\n'
               'эхо 2',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'loop { let (s, _) = l.accept().await?; tokio::spawn(handle(s)); } — сервер запускайте в '
          'отдельной задаче.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['эхо 0', 'эхо 1', 'эхо 2']},
 {'id': 'r36-lines',
  'mode': 'rust',
  'title': 'Чтение построчно',
  'statement': 'Сервер отправляет клиенту «a\\nb\\nc\\n» и закрывает соединение. Клиент читает '
               'через BufReader::lines() и печатает каждую строку.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'a\n'
               'b\n'
               'c',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'use tokio::io::{AsyncBufReadExt, BufReader}; BufReader::new(c).lines(); '
          'next_line().await.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['a', 'b', 'c']},
 {'id': 'r36-read-line',
  'mode': 'rust',
  'title': 'read_line и счёт байт',
  'statement': 'Клиент отправляет «hello\\nworld\\n» и закрывает соединение. Сервер читает '
               'read_line в цикле и печатает «N: строка», где N — число байт (с переводом строки), '
               'а на конце потока — «EOF».\n'
               '\n'
               'Ожидаемый вывод:\n'
               '6: hello\n'
               '6: world\n'
               'EOF',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let n = reader.read_line(&mut s).await?; if n == 0 { break }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['6: hello', '6: world', 'EOF']},
 {'id': 'r36-length-prefix',
  'mode': 'rust',
  'title': 'Префикс длины',
  'statement': 'Клиент отправляет кадр: 4 байта длины (big-endian) и затем «hello». Сервер читает '
               'заголовок (read_exact на 4 байта), затем ровно столько байт данных и печатает '
               '«длина 5, данные hello».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'длина 5, данные hello',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'u32::from_be_bytes(hdr) as usize; (5u32).to_be_bytes().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['длина 5, данные hello']},
 {'id': 'r36-read-u32',
  'mode': 'rust',
  'title': 'read_u32 и write_u32',
  'statement': 'Клиент отправляет число 256 через write_u32 (big-endian). Сервер читает его через '
               'read_u32 и печатает.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '256',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'AsyncWriteExt::write_u32 и AsyncReadExt::read_u32 используют сетевой порядок байт.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['256']},
 {'id': 'r36-split',
  'mode': 'rust',
  'title': 'into_split',
  'statement': 'Эхо-сервер (читает и пишет обратно). Клиент разделяет сокет через into_split(): '
               'задача-писатель отправляет «split», основная задача читает ровно 5 байт '
               '(read_exact) и печатает «ответ: split».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ответ: split',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let (mut r, mut w) = c.into_split(); tokio::spawn(async move { w.write_all(..).await '
          '});',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ответ: split']},
 {'id': 'r36-half-close',
  'mode': 'rust',
  'title': 'shutdown записи',
  'statement': 'Клиент отправляет «запрос», закрывает запись (shutdown), затем читает ответ до '
               'конца. Сервер читает до конца запроса, отвечает «ok» и закрывается. Клиент '
               'печатает «ответ: ok».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ответ: ok',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'c.shutdown().await закрывает запись; read_to_end у сервера завершится.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ответ: ok']},
 {'id': 'r36-refused',
  'mode': 'rust',
  'title': 'Отказ в соединении',
  'statement': 'Привяжите listener, узнайте адрес и уничтожьте listener. Попытка '
               'TcpStream::connect к этому адресу должна завершиться ошибкой. Напечатайте её вид '
               'через {:?}: e.kind().\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ConnectionRefused',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'match TcpStream::connect(addr).await { Err(e) => println!("{:?}", e.kind()), .. }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ConnectionRefused']},
 {'id': 'r36-udp-echo',
  'mode': 'rust',
  'title': 'UDP: эхо',
  'statement': 'Сервер на UdpSocket (bind 127.0.0.1:0) принимает датаграмму через recv_from и '
               'отправляет её обратно отправителю. Клиент посылает «ping» и печатает «ответ: '
               'ping».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ответ: ping',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let (n, from) = s.recv_from(&mut buf).await?; s.send_to(&buf[..n], from).await?;',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ответ: ping']},
 {'id': 'r36-udp-boundaries',
  'mode': 'rust',
  'title': 'Границы датаграмм',
  'statement': 'Отправьте с одного UDP-сокета на другой «ab» и «cd» двумя send_to. Принимающий '
               'делает два recv_from и печатает каждую датаграмму отдельной строкой.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ab\n'
               'cd',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'Одна отправка — одно чтение, без слияния.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ab', 'cd']},
 {'id': 'r36-read-timeout',
  'mode': 'rust',
  'title': 'Таймаут чтения',
  'statement': 'Сервер принимает соединение и молчит (держит сокет 300 мс). Клиент пытается '
               'прочитать с timeout 50 мс и при ошибке печатает «таймаут чтения».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'таймаут чтения',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::time::timeout(Duration::from_millis(50), c.read(&mut buf)).await',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['таймаут чтения']},
 {'id': 'r36-accept-shutdown',
  'mode': 'rust',
  'title': 'Остановка цикла accept',
  'statement': 'Цикл accept в задаче с select!: либо принять клиента (считать), либо получить '
               'сигнал остановки по oneshot. Один клиент подключается, затем (после паузы 50 мс) '
               'отправляется сигнал. Задача печатает «принято: 1» и «остановлен».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'принято: 1\n'
               'остановлен',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'select! { r = l.accept() => { r.unwrap(); n += 1; }, _ = &mut stop => break }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['принято: 1', 'остановлен']},
 {'id': 'r36-count-conns',
  'mode': 'rust',
  'title': 'Подсчёт соединений',
  'statement': 'Сервер в цикле принимает ровно 5 соединений и считает их в AtomicUsize (каждое — в '
               'своей задаче spawn). Пять клиентов подключаются. Дождитесь сервера и напечатайте '
               '«подключений: 5».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'подключений: 5',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'for _ in 0..5 { let (s, _) = l.accept().await?; counter.fetch_add(1, SeqCst); spawn(..) '
          '}',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['подключений: 5']},
 {'id': 'r36-io-copy',
  'mode': 'rust',
  'title': 'io::copy',
  'statement': 'Скопируйте байты из среза &[u8] (b"hello world") в Vec<u8> функцией '
               'tokio::io::copy и напечатайте «скопировано: N».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'скопировано: 11',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let mut r: &[u8] = b"hello world"; let mut w = Vec::new(); tokio::io::copy(&mut r, &mut '
          'w).await?',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['скопировано: 11']},
 {'id': 'r36-duplex',
  'mode': 'rust',
  'title': 'duplex в памяти',
  'statement': 'Создайте пару tokio::io::duplex(64). Запишите в одну половину «hi», закройте её и '
               'прочитайте всё из другой в String. Напечатайте строку.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'hi',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let (mut a, mut b) = tokio::io::duplex(64); drop(a) после записи; b.read_to_string(&mut '
          's).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['hi']},
 {'id': 'r36-proxy',
  'mode': 'rust',
  'title': 'Прокси через copy_bidirectional',
  'statement': 'Эхо-сервер, прокси и клиент. Прокси принимает соединение клиента, подключается к '
               'эхо-серверу и гонит данные в обе стороны через tokio::io::copy_bidirectional. '
               'Клиент отправляет «via proxy», читает столько же байт и печатает «через прокси: '
               'via proxy».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'через прокси: via proxy',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'copy_bidirectional(&mut client_side, &mut upstream).await — в отдельной задаче.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['через прокси: via proxy']},
 {'id': 'r36-stream-map',
  'mode': 'rust',
  'title': 'Stream: map и collect',
  'statement': 'Из tokio_stream::iter(1..=3) получите поток, умножьте каждое значение на 2 (map) и '
               'соберите в Vec (collect). Напечатайте вектор через {:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[2, 4, 6]',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'use tokio_stream::{self as stream, StreamExt}; '
          'stream::iter(..).map(..).collect::<Vec<_>>().await',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[2, 4, 6]']},
 {'id': 'r36-receiver-stream',
  'mode': 'rust',
  'title': 'ReceiverStream',
  'statement': 'Оберните приёмник mpsc-канала в ReceiverStream, отправьте из задачи 1, 2, 3 и '
               'соберите поток в вектор. Напечатайте вектор через {:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[1, 2, 3]',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio_stream::wrappers::ReceiverStream::new(rx).collect::<Vec<_>>().await',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[1, 2, 3]']},
 {'id': 'r36-stream-filter-take',
  'mode': 'rust',
  'title': 'Stream: filter и take',
  'statement': 'Из iter(1..=10) оставьте чётные (filter), возьмите первые три (take) и соберите в '
               'Vec. Напечатайте вектор через {:?}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[2, 4, 6]',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': '.filter(|x| x % 2 == 0).take(3).collect::<Vec<_>>().await',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[2, 4, 6]']},
 {'id': 'r36-fs',
  'mode': 'rust',
  'title': 'tokio::fs',
  'statement': 'Запишите «hello» в файл /tmp/say_r36.txt через tokio::fs::write, прочитайте '
               'обратно read_to_string, напечатайте содержимое и удалите файл (remove_file).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'hello',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'tokio::fs::write(path, data).await?; tokio::fs::read_to_string(path).await?',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['hello']},
 {'id': 'r36-spawn-blocking',
  'mode': 'rust',
  'title': 'spawn_blocking',
  'statement': 'Через tokio::task::spawn_blocking вычислите сумму чисел от 1 до 1_000_000 (u64) и '
               'напечатайте результат.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '500000500000',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'spawn_blocking(|| (1..=1_000_000u64).sum::<u64>()).await?',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['500000500000']},
 {'id': 'r36-lookup-host',
  'mode': 'rust',
  'title': 'lookup_host',
  'statement': 'Через tokio::net::lookup_host("127.0.0.1:80") получите адреса и напечатайте '
               '«адресов: N».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'адресов: 1',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'lookup_host(..).await?.count()',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['адресов: 1']},
 {'id': 'r36-peer-addr',
  'mode': 'rust',
  'title': 'Адрес клиента',
  'statement': 'Сервер получает адрес клиента из accept() и печатает «клиент с петли: true», если '
               'addr.ip().is_loopback().\n'
               '\n'
               'Ожидаемый вывод:\n'
               'клиент с петли: true',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let (_s, peer) = l.accept().await?; peer.ip().is_loopback()',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['клиент с петли: true']},
 {'id': 'r36-unix-socket',
  'mode': 'rust',
  'title': 'Unix-сокет',
  'statement': 'Привяжите UnixListener к /tmp/say_r36.sock, подключитесь UnixStream-клиентом, '
               'отправьте «ping», сервер читает и печатает «unix: ping». После работы удалите файл '
               'сокета.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'unix: ping',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'use tokio::net::{UnixListener, UnixStream}; перед bind удалите старый файл (let _ = '
          'std::fs::remove_file).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['unix: ping']},
 {'id': 'r36-line-protocol',
  'mode': 'rust',
  'title': 'Текстовый протокол',
  'statement': 'Сервер читает строку «ADD 2 3», складывает числа и отвечает строкой с результатом '
               'и переводом строки. Клиент отправляет «ADD 2 3\\n», читает строку ответа и '
               'печатает её без перевода строки.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '5',
  'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'BufReader::new(socket).read_line(..); split_whitespace(); write_all(format!("{}\\n", '
          'sum)).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['5']}]}
