"""Задачи книги «Компьютерные сети»: глава 9 — сокеты в программе (код на Python, песочница, loopback)."""

TASKS: dict[int, list[dict]] = {
    9: [
        {'id': 'net9-fetch',
         'mode': 'stdout',
         'title': 'Клиент: отправить запрос и прочитать ответ до конца',
         'statement': 'Напишите функцию fetch(host, port, request): подключитесь по TCP, отправьте все '
                      'байты request (sendall), затем читайте ответ, пока recv не вернёт пустые байты '
                      '(собеседник закрыл соединение), и верните весь ответ одним bytes.',
         'starter': 'import socket\n\n\ndef fetch(host, port, request):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   "srv = socket.socket(); srv.bind(('127.0.0.1', 0)); srv.listen(1); port = "
                   'srv.getsockname()[1]\n'
                   'def serve():\n'
                   '    c, _ = srv.accept()\n'
                   "    req = b''\n"
                   "    while not req.endswith(b'\\r\\n\\r\\n'):\n"
                   '        req += c.recv(1024)\n'
                   "    c.sendall(b'HTTP/1.0 200 OK\\r\\n\\r\\nhello ' + req.split(b' ')[1])\n"
                   '    c.close()\n'
                   'threading.Thread(target=serve, daemon=True).start()\n'
                   "print(fetch('127.0.0.1', port, b'GET /x HTTP/1.0\\r\\n\\r\\n'))\n",
         'expected': ["b'HTTP/1.0 200 OK\\r\\n\\r\\nhello /x'"],
         'hint': 'Цикл while True: data = s.recv(4096); если data пустой — break; иначе накапливайте в '
                 "списке и в конце склейте b''.join(...)."},
        {'id': 'net9-recv-exact',
         'mode': 'stdout',
         'title': 'Прочитать ровно n байт',
         'statement': 'recv может вернуть меньше, чем просили. Напишите функцию recv_exact(sock, n): '
                      'читает из сокета ровно n байт (в цикле) и возвращает их. Если соединение закрылось '
                      'раньше, чем пришло n байт, поднимите ConnectionError.',
         'starter': 'def recv_exact(sock, n):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   'import time\n'
                   'a, b = socket.socketpair()\n'
                   'def feed():\n'
                   "    for ch in (b'he', b'l', b'lo wor', b'ld'):\n"
                   '        b.sendall(ch)\n'
                   '        time.sleep(0.02)\n'
                   '    b.close()\n'
                   'threading.Thread(target=feed, daemon=True).start()\n'
                   'print(recv_exact(a, 11))\n'
                   'try:\n'
                   '    recv_exact(a, 5)\n'
                   'except ConnectionError:\n'
                   "    print('ConnectionError')\n",
         'expected': ["b'hello world'", 'ConnectionError'],
         'hint': "buf = b''; while len(buf) < n: chunk = sock.recv(n - len(buf)); пустой chunk — "
                 'ConnectionError; иначе buf += chunk.'},
        {'id': 'net9-framing',
         'mode': 'stdout',
         'title': 'Сообщения с длиной впереди',
         'statement': 'TCP — поток байтов, границ сообщений в нём нет. Реализуйте простой протокол: перед '
                      'каждым сообщением идёт его длина в 4 байтах (big-endian). Напишите send_msg(sock, '
                      'data: bytes) и recv_msg(sock) -> bytes. Пустое сообщение допустимо; при закрытии '
                      'соединения вместо длины recv_msg возвращает None.',
         'starter': 'import struct\n'
                    '\n'
                    '\n'
                    'def send_msg(sock, data):\n'
                    '    pass\n'
                    '\n'
                    '\n'
                    'def recv_msg(sock):\n'
                    '    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   'a, b = socket.socketpair()\n'
                   "msgs = [b'hi', b'', b'x' * 10000, b'bye']\n"
                   'def send_all():\n'
                   '    for m in msgs:\n'
                   '        send_msg(a, m)\n'
                   '    a.close()\n'
                   'threading.Thread(target=send_all, daemon=True).start()\n'
                   'got = []\n'
                   'while True:\n'
                   '    m = recv_msg(b)\n'
                   '    if m is None:\n'
                   '        break\n'
                   '    got.append(len(m))\n'
                   'print(got)\n',
         'expected': ['[2, 0, 10000, 3]'],
         'hint': "Отправка: sock.sendall(struct.pack('>I', len(data)) + data). Приём: прочитать ровно 4 "
                 'байта (цикл), распаковать длину, прочитать ровно столько.'},
        {'id': 'net9-linereader',
         'mode': 'stdout',
         'title': 'Читатель строк по потоку',
         'statement': 'Данные приходят кусками произвольного размера. Напишите класс LineReader(sock) с '
                      "методом readline(): возвращает следующую строку (bytes) без завершающего b'\\n'; "
                      'остаток, прочитанный сверх строки, хранится для следующего вызова. Когда соединение '
                      'закрыто и данных нет — None.',
         'starter': 'class LineReader:\n'
                    '    def __init__(self, sock):\n'
                    '        pass\n'
                    '\n'
                    '    def readline(self):\n'
                    '        pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   'import time\n'
                   'a, b = socket.socketpair()\n'
                   'def feed():\n'
                   "    for ch in (b'ab\\ncd', b'ef\\n\\ngh\\n', b'tail'):\n"
                   '        b.sendall(ch)\n'
                   '        time.sleep(0.02)\n'
                   '    b.close()\n'
                   'threading.Thread(target=feed, daemon=True).start()\n'
                   'r = LineReader(a)\n'
                   'lines = []\n'
                   'while True:\n'
                   '    ln = r.readline()\n'
                   '    if ln is None:\n'
                   '        break\n'
                   '    lines.append(ln)\n'
                   'print(lines)\n',
         'expected': ["[b'ab', b'cdef', b'', b'gh', b'tail']"],
         'hint': "Держите буфер self.buf; пока в нём нет b'\\n' — дочитывайте recv; потом отрезайте строку "
                 "через split(b'\\n', 1)."},
        {'id': 'net9-echo-once',
         'mode': 'stdout',
         'title': 'Эхо-сервер для одного клиента',
         'statement': 'Напишите функцию echo_once(listener): слушающий сокет уже создан. Примите одно '
                      'соединение (accept) и возвращайте клиенту всё, что он присылает, пока он не закроет '
                      'соединение; закройте сокет клиента. Верните число байтов, которые вы переслали.',
         'starter': 'def echo_once(listener):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   "srv = socket.socket(); srv.bind(('127.0.0.1', 0)); srv.listen(1); port = "
                   'srv.getsockname()[1]\n'
                   'out = {}\n'
                   'def client():\n'
                   "    c = socket.create_connection(('127.0.0.1', port))\n"
                   "    c.sendall(b'hello ')\n"
                   "    c.sendall(b'world')\n"
                   '    c.shutdown(socket.SHUT_WR)\n'
                   "    data = b''\n"
                   '    while True:\n'
                   '        d = c.recv(1024)\n'
                   '        if not d:\n'
                   '            break\n'
                   '        data += d\n'
                   "    out['echo'] = data\n"
                   '    c.close()\n'
                   't = threading.Thread(target=client, daemon=True); t.start()\n'
                   'n = echo_once(srv)\n'
                   't.join(3)\n'
                   'print(n)\n'
                   "print(out.get('echo'))\n",
         'expected': ['11', "b'hello world'"],
         'hint': 'conn, addr = listener.accept(); в цикле recv → sendall обратно; пустой recv означает, '
                 'что клиент закончил.'},
        {'id': 'net9-udp-server',
         'mode': 'stdout',
         'title': 'UDP-сервер: ответ заглавными',
         'statement': 'Напишите функцию udp_upper_server(sock, count): сокет уже привязан к порту. Примите '
                      'count датаграмм (recvfrom) и на каждую ответьте отправителю (sendto) тем же текстом '
                      'заглавными буквами (bytes.upper()).',
         'starter': 'def udp_upper_server(sock, count):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   "s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.bind(('127.0.0.1', 0)); addr = "
                   's.getsockname()\n'
                   't = threading.Thread(target=udp_upper_server, args=(s, 3), daemon=True); t.start()\n'
                   'c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n'
                   "for word in (b'ping', b'Hello', b'udp'):\n"
                   '    c.sendto(word, addr)\n'
                   '    print(c.recvfrom(2048)[0])\n',
         'expected': ["b'PING'", "b'HELLO'", "b'UDP'"],
         'hint': 'data, addr = sock.recvfrom(2048); sock.sendto(data.upper(), addr) — ровно count раз.'},
        {'id': 'net9-udp-retry',
         'mode': 'stdout',
         'title': 'UDP-клиент с повторами',
         'statement': 'UDP не повторяет потерянные датаграммы — это делает приложение. Напишите функцию '
                      'udp_ask(addr, data, timeout=0.2, retries=5): отправьте data на addr и ждите ответ '
                      'не дольше timeout секунд (settimeout). Не дождались — отправьте снова, всего не '
                      'больше retries попыток. Верните кортеж (ответ, номер_попытки). Если ни одной не '
                      'хватило — поднимите TimeoutError.',
         'starter': 'import socket\n\n\ndef udp_ask(addr, data, timeout=0.2, retries=5):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   "srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); srv.bind(('127.0.0.1', 0)); "
                   'addr = srv.getsockname()\n'
                   "drop = {'n': 2}\n"
                   'def serve():\n'
                   '    while True:\n'
                   '        try:\n'
                   '            data, a = srv.recvfrom(2048)\n'
                   '        except OSError:\n'
                   '            return\n'
                   "        if drop['n'] > 0:\n"
                   "            drop['n'] -= 1\n"
                   '            continue\n'
                   "        srv.sendto(b'pong:' + data, a)\n"
                   'threading.Thread(target=serve, daemon=True).start()\n'
                   "print(udp_ask(addr, b'x', timeout=0.15, retries=5))\n"
                   "drop['n'] = 100\n"
                   'try:\n'
                   "    udp_ask(addr, b'y', timeout=0.05, retries=3)\n"
                   'except TimeoutError:\n'
                   "    print('TimeoutError')\n",
         'expected': ["(b'pong:x', 3)", 'TimeoutError'],
         'hint': 's.settimeout(timeout); цикл попыток: sendto, затем recvfrom в try/except socket.timeout. '
                 'После цикла — raise TimeoutError.'},
        {'id': 'net9-scan',
         'mode': 'stdout',
         'title': 'Сканер открытых портов',
         'statement': 'Напишите функцию open_ports(host, ports): для каждого порта попробуйте подключиться '
                      'по TCP (create_connection с таймаутом 0.5 с) и верните отсортированный список '
                      'портов, на которых подключение удалось. Ошибки подключения (отказ, таймаут) '
                      'означают «закрыт».',
         'starter': 'import socket\n\n\ndef open_ports(host, ports):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   'ls = []\n'
                   'for _ in range(3):\n'
                   "    s = socket.socket(); s.bind(('127.0.0.1', 0)); s.listen(5); ls.append(s)\n"
                   'opened = sorted(s.getsockname()[1] for s in ls)\n'
                   'closed = []\n'
                   'for _ in range(3):\n'
                   "    s = socket.socket(); s.bind(('127.0.0.1', 0)); closed.append(s.getsockname()[1]); "
                   's.close()\n'
                   "res = open_ports('127.0.0.1', closed + opened[::-1])\n"
                   'print(res == opened)\n'
                   'print(len(res))\n'
                   "print(open_ports('127.0.0.1', []))\n",
         'expected': ['True', '3', '[]'],
         'hint': 'try: with socket.create_connection((host, p), timeout=0.5): found.append(p) — except '
                 'OSError: пропустить.'},
        {'id': 'net9-threaded',
         'mode': 'stdout',
         'title': 'Сервер: поток на каждого клиента',
         'statement': 'Напишите функцию threaded_echo(listener, clients): примите clients соединений '
                      '(accept), для каждого запустите отдельный поток, который возвращает клиенту то, что '
                      'получает, пока тот не закроет соединение. Дождитесь завершения всех потоков и '
                      'верните общее число пересланных байтов. Клиенты подключаются одновременно и ждут '
                      'друг друга, поэтому по очереди обслужить их не получится.',
         'starter': 'import threading\n\n\ndef threaded_echo(listener, clients):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   "srv = socket.socket(); srv.bind(('127.0.0.1', 0)); srv.listen(10); port = "
                   'srv.getsockname()[1]\n'
                   'barrier = threading.Barrier(3, timeout=2)\n'
                   'res = {}\n'
                   'def client(i):\n'
                   '    try:\n'
                   "        c = socket.create_connection(('127.0.0.1', port))\n"
                   '        barrier.wait()\n'
                   "        msg = ('client%d' % i).encode()\n"
                   '        c.sendall(msg)\n'
                   '        c.shutdown(socket.SHUT_WR)\n'
                   "        data = b''\n"
                   '        while True:\n'
                   '            d = c.recv(1024)\n'
                   '            if not d:\n'
                   '                break\n'
                   '            data += d\n'
                   '        res[i] = data\n'
                   '        c.close()\n'
                   '    except Exception as e:\n'
                   '        res[i] = type(e).__name__\n'
                   'ts = [threading.Thread(target=client, args=(i,), daemon=True) for i in range(3)]\n'
                   '[t.start() for t in ts]\n'
                   'n = threaded_echo(srv, 3)\n'
                   '[t.join(3) for t in ts]\n'
                   'print(n)\n'
                   'print([res.get(i) for i in range(3)])\n',
         'expected': ['21', "[b'client0', b'client1', b'client2']"],
         'hint': 'В цикле accept → threading.Thread(target=work, args=(conn,)). Общий счётчик защитите '
                 'замком, в конце join всех потоков.'},
        {'id': 'net9-selectors',
         'mode': 'stdout',
         'title': 'Сервер на select: один поток — много клиентов',
         'statement': 'Реализуйте то же, но в одном потоке: select_echo(listener, clients) принимает '
                      'clients соединений и обслуживает их с помощью модуля selectors (DefaultSelector): '
                      'новое соединение — регистрируете, пришли данные — возвращаете их клиенту, пустой '
                      'recv — закрываете и снимаете с регистрации. Когда все клиенты обслужены и закрыты, '
                      'верните число пересланных байтов. Создавать потоки внутри функции нельзя.',
         'starter': 'import selectors\n\n\ndef select_echo(listener, clients):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   "srv = socket.socket(); srv.bind(('127.0.0.1', 0)); srv.listen(10); port = "
                   'srv.getsockname()[1]\n'
                   'barrier = threading.Barrier(3, timeout=2)\n'
                   'res = {}\n'
                   'def client(i):\n'
                   '    try:\n'
                   "        c = socket.create_connection(('127.0.0.1', port))\n"
                   '        barrier.wait()\n'
                   "        msg = ('select%d' % i).encode()\n"
                   '        c.sendall(msg)\n'
                   '        c.shutdown(socket.SHUT_WR)\n'
                   "        data = b''\n"
                   '        while True:\n'
                   '            d = c.recv(1024)\n'
                   '            if not d:\n'
                   '                break\n'
                   '            data += d\n'
                   '        res[i] = data\n'
                   '        c.close()\n'
                   '    except Exception as e:\n'
                   '        res[i] = type(e).__name__\n'
                   'ts = [threading.Thread(target=client, args=(i,), daemon=True) for i in range(3)]\n'
                   '[t.start() for t in ts]\n'
                   '_orig = threading.Thread.start\n'
                   'def _forbid(self):\n'
                   "    raise RuntimeError('потоки запрещены')\n"
                   'threading.Thread.start = _forbid\n'
                   'try:\n'
                   '    n = select_echo(srv, 3)\n'
                   'finally:\n'
                   '    threading.Thread.start = _orig\n'
                   '[t.join(3) for t in ts]\n'
                   'print(n)\n'
                   'print([res.get(i) for i in range(3)])\n',
         'expected': ['21', "[b'select0', b'select1', b'select2']"],
         'hint': "sel.register(listener, EVENT_READ, 'accept'); в цикле sel.select(): для слушающего — "
                 'accept и регистрация нового сокета; для клиентов — recv/sendall, а на пустом recv '
                 'закрыть и unregister.'},
        {'id': 'net9-asyncio',
         'mode': 'stdout',
         'title': 'Асинхронный эхо-обработчик',
         'statement': 'Напишите корутину handle(reader, writer) для asyncio.start_server: читайте строки '
                      "(reader.readline()) и отправляйте каждую обратно с префиксом b'echo: ' "
                      '(writer.write + await writer.drain()), пока клиент не закроет соединение (пустая '
                      'строка). В конце закройте writer (close и await wait_closed()).',
         'starter': 'async def handle(reader, writer):\n    pass\n',
         'driver': 'import asyncio\n'
                   'async def client(port, name):\n'
                   "    r, w = await asyncio.open_connection('127.0.0.1', port)\n"
                   '    out = []\n'
                   '    for i in range(2):\n'
                   "        w.write(('%s%d\\n' % (name, i)).encode())\n"
                   '        await w.drain()\n'
                   '        out.append((await r.readline()).decode().strip())\n'
                   '    w.close()\n'
                   '    await w.wait_closed()\n'
                   '    return out\n'
                   'async def main():\n'
                   "    srv = await asyncio.start_server(handle, '127.0.0.1', 0)\n"
                   '    port = srv.sockets[0].getsockname()[1]\n'
                   "    res = await asyncio.wait_for(asyncio.gather(*(client(port, n) for n in 'abc')), "
                   '5)\n'
                   '    srv.close()\n'
                   '    await srv.wait_closed()\n'
                   '    return res\n'
                   'for r in asyncio.run(main()):\n'
                   '    print(r)\n',
         'expected': ["['echo: a0', 'echo: a1']", "['echo: b0', 'echo: b1']", "['echo: c0', 'echo: c1']"],
         'hint': "while True: line = await reader.readline(); пустая — break; writer.write(b'echo: ' + "
                 'line); await writer.drain().'},
        {'id': 'net9-http-get',
         'mode': 'stdout',
         'title': 'Свой мини-клиент HTTP',
         'statement': "Напишите функцию http_get(host, port, path): отправьте по сырому сокету запрос 'GET "
                      "<path> HTTP/1.1' с заголовками Host и Connection: close, прочитайте ответ до "
                      'закрытия и разберите его. Верните кортеж (код_статуса: int, заголовки: dict с '
                      'именами в нижнем регистре, тело: bytes). Заголовки от тела отделяет пустая строка '
                      '\\r\\n\\r\\n.',
         'starter': 'import socket\n\n\ndef http_get(host, port, path):\n    pass\n',
         'driver': 'import socket\n'
                   'import threading\n'
                   'socket.setdefaulttimeout(3)\n'
                   "srv = socket.socket(); srv.bind(('127.0.0.1', 0)); srv.listen(5); port = "
                   'srv.getsockname()[1]\n'
                   'def serve():\n'
                   '    for _ in range(2):\n'
                   '        c, _ = srv.accept()\n'
                   "        req = b''\n"
                   "        while not req.endswith(b'\\r\\n\\r\\n'):\n"
                   '            req += c.recv(1024)\n'
                   "        path = req.split(b' ')[1]\n"
                   "        if path == b'/ok':\n"
                   "            body = b'<h1>Hi</h1>'\n"
                   "            c.sendall(b'HTTP/1.1 200 OK\\r\\nContent-Type: "
                   "text/html\\r\\nContent-Length: %d\\r\\nConnection: close\\r\\n\\r\\n' % len(body) + "
                   'body)\n'
                   '        else:\n'
                   "            c.sendall(b'HTTP/1.1 404 Not Found\\r\\nContent-Length: 0\\r\\nConnection: "
                   "close\\r\\n\\r\\n')\n"
                   '        c.close()\n'
                   'threading.Thread(target=serve, daemon=True).start()\n'
                   "print(http_get('127.0.0.1', port, '/ok'))\n"
                   "st, h, b = http_get('127.0.0.1', port, '/nope')\n"
                   "print(st, h['content-length'], b)\n",
         'expected': ["(200, {'content-type': 'text/html', 'content-length': '11', 'connection': 'close'}, "
                      "b'<h1>Hi</h1>')",
                      "404 0 b''"],
         'hint': "Ответ читайте до пустого recv; разделите по b'\\r\\n\\r\\n' (partition); первая строка — "
                 '«HTTP/1.1 200 OK»; остальные — «Имя: значение».'},
    ],
}
