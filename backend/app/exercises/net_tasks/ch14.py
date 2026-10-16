"""Задачи книги «Компьютерные сети»: глава 14 — веб-API на Python (код на Python, песочница, loopback)."""

TASKS: dict[int, list[dict]] = {
    14: [
        {'id': 'net14-rest-get',
         'mode': 'stdout',
         'title': 'REST: чтение ресурсов',
         'statement': 'Напишите класс Handler (наследник BaseHTTPRequestHandler) с методом do_GET. Словарь '
                      'ITEMS уже задан. GET /items — 200 и JSON-список всех элементов, отсортированный по '
                      'id. GET /items/<id> — 200 и JSON-объект, а если такого id нет, то 404 и JSON '
                      '{"error": "not found"}. Везде заголовок Content-Type: application/json.',
         'starter': 'import json\n'
                    'from http.server import BaseHTTPRequestHandler\n'
                    '\n'
                    "ITEMS = {1: {'id': 1, 'name': 'book'}, 2: {'id': 2, 'name': 'pen'}}\n"
                    '\n'
                    '\n'
                    'class Handler(BaseHTTPRequestHandler):\n'
                    '    def do_GET(self):\n'
                    '        pass\n',
         'driver': 'import threading, urllib.request, urllib.error, json\n'
                   'from http.server import HTTPServer\n'
                   "srv = HTTPServer(('127.0.0.1', 0), Handler)\n"
                   'port = srv.server_address[1]\n'
                   'threading.Thread(target=srv.serve_forever, daemon=True).start()\n'
                   'def get(p):\n'
                   '    try:\n'
                   "        r = urllib.request.urlopen(f'http://127.0.0.1:{port}{p}', timeout=3)\n"
                   "        return r.status, r.headers['Content-Type'], json.loads(r.read())\n"
                   '    except urllib.error.HTTPError as e:\n'
                   "        return e.code, e.headers['Content-Type'], json.loads(e.read())\n"
                   "print(get('/items'))\n"
                   "print(get('/items/2'))\n"
                   "print(get('/items/99'))\n"
                   'srv.shutdown()\n',
         'expected': ["(200, 'application/json', [{'id': 1, 'name': 'book'}, {'id': 2, 'name': 'pen'}])",
                      "(200, 'application/json', {'id': 2, 'name': 'pen'})",
                      "(404, 'application/json', {'error': 'not found'})"],
         'hint': "Верните json.dumps(...).encode(); send_response(код), send_header('Content-Type', "
                 "'application/json'), end_headers(), затем wfile.write(тело). Для /items/<id>: "
                 "int(self.path.split('/')[2]) в try."},
        {'id': 'net14-rest-post',
         'mode': 'stdout',
         'title': 'REST: создание ресурса',
         'statement': 'Добавьте в Handler метод do_POST для пути /items. Тело — JSON {"name": ...}. '
                      'Создайте элемент с новым id (максимальный id + 1), верните 201, заголовок Location: '
                      '/items/<id> и JSON созданного элемента. Если тело — не JSON или в нём нет непустого '
                      'name, верните 400 и {"error": "bad request"}. Словарь ITEMS изменяйте на месте.',
         'starter': 'import json\n'
                    'from http.server import BaseHTTPRequestHandler\n'
                    '\n'
                    "ITEMS = {1: {'id': 1, 'name': 'book'}}\n"
                    '\n'
                    '\n'
                    'class Handler(BaseHTTPRequestHandler):\n'
                    '    def do_POST(self):\n'
                    '        pass\n',
         'driver': 'import threading, urllib.request, urllib.error, json\n'
                   'from http.server import HTTPServer\n'
                   "srv = HTTPServer(('127.0.0.1', 0), Handler)\n"
                   'port = srv.server_address[1]\n'
                   'threading.Thread(target=srv.serve_forever, daemon=True).start()\n'
                   'def post(body):\n'
                   "    req = urllib.request.Request(f'http://127.0.0.1:{port}/items', data=body, "
                   "method='POST', headers={'Content-Type': 'application/json'})\n"
                   '    try:\n'
                   '        r = urllib.request.urlopen(req, timeout=3)\n'
                   "        return r.status, r.headers['Location'], json.loads(r.read())\n"
                   '    except urllib.error.HTTPError as e:\n'
                   '        return e.code, json.loads(e.read())\n'
                   'print(post(b\'{"name": "lamp"}\'))\n'
                   'print(post(b\'{"name": "cup"}\'))\n'
                   "print(post(b'not json'))\n"
                   'print(post(b\'{"title": 1}\'))\n'
                   'print(sorted(ITEMS))\n'
                   'srv.shutdown()\n',
         'expected': ["(201, '/items/2', {'id': 2, 'name': 'lamp'})",
                      "(201, '/items/3', {'id': 3, 'name': 'cup'})",
                      "(400, {'error': 'bad request'})",
                      "(400, {'error': 'bad request'})",
                      '[1, 2, 3]'],
         'hint': "Тело: n = int(self.headers['Content-Length']); json.loads(self.rfile.read(n)). Ошибки "
                 'разбора и отсутствие name — 400. Новый id: max(ITEMS) + 1.'},
        {'id': 'net14-paginate',
         'mode': 'stdout',
         'title': 'Пагинация',
         'statement': 'Напишите функцию paginate(items, page, per_page), страницы нумеруются с 1. Верните '
                      "словарь: {'items': элементы страницы, 'page': page, 'pages': общее число страниц, "
                      "'next': номер следующей страницы или None}. Если page вне диапазона (меньше 1 или "
                      'больше pages), items — пустой список, а next — None. Для пустого списка pages = 0.',
         'starter': 'def paginate(items, page, per_page):\n    pass\n',
         'driver': 'data = list(range(1, 8))\n'
                   'print(paginate(data, 1, 3))\n'
                   'print(paginate(data, 3, 3))\n'
                   'print(paginate(data, 4, 3))\n'
                   'print(paginate(data, 0, 3))\n'
                   'print(paginate([], 1, 3))\n',
         'expected': ["{'items': [1, 2, 3], 'page': 1, 'pages': 3, 'next': 2}",
                      "{'items': [7], 'page': 3, 'pages': 3, 'next': None}",
                      "{'items': [], 'page': 4, 'pages': 3, 'next': None}",
                      "{'items': [], 'page': 0, 'pages': 3, 'next': None}",
                      "{'items': [], 'page': 1, 'pages': 0, 'next': None}"],
         'hint': 'pages = -(-len(items) // per_page) — деление вверх; срез items[(page-1)*per_page : '
                 'page*per_page].'},
        {'id': 'net14-etag',
         'mode': 'stdout',
         'title': 'ETag и условный GET',
         'statement': 'Напишите make_etag(body: bytes) — строка в кавычках из первых 8 символов sha1-хеша '
                      'тела (например \'"a94a8fe5"\'), и conditional_get(headers: dict, body: bytes) -> '
                      "(status, response_headers, response_body). Если в headers есть 'If-None-Match', "
                      "равный ETag тела, верните (304, {'ETag': etag}, b''). Иначе (200, {'ETag': etag}, "
                      'body).',
         'starter': 'import hashlib\n'
                    '\n'
                    '\n'
                    'def make_etag(body):\n'
                    '    pass\n'
                    '\n'
                    '\n'
                    'def conditional_get(headers, body):\n'
                    '    pass\n',
         'driver': "e = make_etag(b'hello')\n"
                   'print(e)\n'
                   "print(conditional_get({}, b'hello'))\n"
                   "print(conditional_get({'If-None-Match': e}, b'hello'))\n"
                   "print(conditional_get({'If-None-Match': e}, b'hello!')[0])\n",
         'expected': ['"aaf4c61d"',
                      '(200, {\'ETag\': \'"aaf4c61d"\'}, b\'hello\')',
                      '(304, {\'ETag\': \'"aaf4c61d"\'}, b\'\')',
                      '200'],
         'hint': 'hashlib.sha1(body).hexdigest()[:8] в кавычках; сравнивайте заголовок If-None-Match со '
                 'своим ETag.'},
        {'id': 'net14-bearer',
         'mode': 'stdout',
         'title': 'Токен предъявителя: 401 и 403',
         'statement': 'Напишите authorize(headers, tokens, scope), где tokens — словарь {токен: '
                      "множество_прав}. Заголовок 'Authorization: Bearer <токен>'. Верните (200, 'ok'), "
                      "если токен известен и scope входит в его права; (401, 'unauthorized'), если "
                      "заголовка нет, схема не Bearer или токен неизвестен; (403, 'forbidden'), если токен "
                      'известен, но прав недостаточно.',
         'starter': 'def authorize(headers, tokens, scope):\n    pass\n',
         'driver': "T = {'abc': {'read'}, 'root': {'read', 'write'}}\n"
                   "print(authorize({}, T, 'read'))\n"
                   "print(authorize({'Authorization': 'Basic abc'}, T, 'read'))\n"
                   "print(authorize({'Authorization': 'Bearer zzz'}, T, 'read'))\n"
                   "print(authorize({'Authorization': 'Bearer abc'}, T, 'write'))\n"
                   "print(authorize({'Authorization': 'Bearer root'}, T, 'write'))\n",
         'expected': ["(401, 'unauthorized')",
                      "(401, 'unauthorized')",
                      "(401, 'unauthorized')",
                      "(403, 'forbidden')",
                      "(200, 'ok')"],
         'hint': "Разберите заголовок через split(' ', 1); сначала проверьте схему и существование токена "
                 '(401), затем права (403).'},
        {'id': 'net14-bucket',
         'mode': 'stdout',
         'title': 'Корзина жетонов (rate limit)',
         'statement': 'Напишите класс TokenBucket(rate, capacity): корзина вмещает capacity жетонов и '
                      'пополняется rate жетонами в секунду (пополнение — дробное), в начале полная. Метод '
                      'allow(now) принимает время в секундах (неубывающее): сначала пополняет корзину за '
                      'прошедшее время (но не выше capacity), затем, если жетонов не меньше 1, забирает '
                      'один и возвращает True, иначе False.',
         'starter': 'class TokenBucket:\n'
                    '    def __init__(self, rate, capacity):\n'
                    '        pass\n'
                    '\n'
                    '    def allow(self, now):\n'
                    '        pass\n',
         'driver': 'b = TokenBucket(rate=1, capacity=3)\n'
                   'print([b.allow(0) for _ in range(5)])\n'
                   'print(b.allow(0.5))\n'
                   'print(b.allow(1.0))\n'
                   'print([b.allow(10) for _ in range(4)])\n',
         'expected': ['[True, True, True, False, False]', 'False', 'True', '[True, True, True, False]'],
         'hint': 'Храните tokens и время последнего пополнения; tokens = min(capacity, tokens + (now - '
                 'last) * rate).'},
        {'id': 'net14-retry',
         'mode': 'stdout',
         'title': 'Повторы с учётом Retry-After',
         'statement': 'Напишите get_with_retry(fetch, retries, sleep): fetch() возвращает (status, '
                      'headers). Повторяйте при статусах 429 и 503 не более retries раз после первой '
                      'попытки. Пауза перед повтором: если в ответе есть Retry-After (секунды), то это '
                      'значение, иначе экспоненциальная 1, 2, 4, 8… Вызывайте sleep(пауза). Верните '
                      'последний статус (успешный или нет).',
         'starter': 'def get_with_retry(fetch, retries, sleep):\n    pass\n',
         'driver': 'def seq(*resp):\n'
                   '    it = iter(resp)\n'
                   '    return lambda: next(it)\n'
                   'sl = []\n'
                   'print(get_with_retry(seq((503, {}), (503, {}), (200, {})), 5, sl.append), sl)\n'
                   'sl = []\n'
                   "print(get_with_retry(seq((429, {'Retry-After': '7'}), (200, {})), 5, sl.append), sl)\n"
                   'sl = []\n'
                   'print(get_with_retry(seq((503, {}), (503, {}), (503, {})), 2, sl.append), sl)\n'
                   'sl = []\n'
                   'print(get_with_retry(seq((404, {})), 3, sl.append), sl)\n',
         'expected': ['200 [1, 2]', '200 [7.0]', '503 [1, 2]', '404 []'],
         'hint': 'Цикл по числу повторов: если статус не 429/503 — выходим; иначе pause = Retry-After или '
                 'delay; delay *= 2; снова fetch().'},
        {'id': 'net14-idempotent',
         'mode': 'stdout',
         'title': 'Идемпотентное создание заказа',
         'statement': 'Напишите класс OrderService с методом create_order(key, payload). Для нового ключа '
                      "создайте заказ с очередным id (1, 2, …) и верните {'id': id, 'payload': payload}. "
                      'Если тот же ключ приходит повторно (даже с другим payload), верните сохранённый '
                      'результат первого вызова и не создавайте новый заказ. Атрибут created — число '
                      'реально созданных заказов.',
         'starter': 'class OrderService:\n'
                    '    def __init__(self):\n'
                    '        self.created = 0\n'
                    '\n'
                    '    def create_order(self, key, payload):\n'
                    '        pass\n',
         'driver': 's = OrderService()\n'
                   "print(s.create_order('k1', 'book'))\n"
                   "print(s.create_order('k1', 'book'))\n"
                   "print(s.create_order('k1', 'other'))\n"
                   "print(s.create_order('k2', 'pen'))\n"
                   'print(s.created)\n',
         'expected': ["{'id': 1, 'payload': 'book'}",
                      "{'id': 1, 'payload': 'book'}",
                      "{'id': 1, 'payload': 'book'}",
                      "{'id': 2, 'payload': 'pen'}",
                      '2'],
         'hint': 'Словарь результатов по ключу; новый заказ — только если ключа ещё нет.'},
        {'id': 'net14-ws-accept',
         'mode': 'stdout',
         'title': 'WebSocket: ключ подтверждения',
         'statement': 'Напишите ws_accept(key: str) -> str: значение заголовка Sec-WebSocket-Accept. Нужно '
                      'склеить key и GUID "258EAFA5-E914-47DA-95CA-C5AB0DC85B11", взять sha1 (байты) и '
                      'закодировать base64 в строку.',
         'starter': 'import base64\nimport hashlib\n\n\ndef ws_accept(key):\n    pass\n',
         'driver': "print(ws_accept('dGhlIHNhbXBsZSBub25jZQ=='))\n"
                   "print(ws_accept('x3JJHMbDL1EzLkh9GBhXDw=='))\n",
         'expected': ['s3pPLMBiTxaQ9kYGzzhZRbK+xOo=', 'HSmrc0sMlYUkAGmm5OPpG2HaGWk='],
         'hint': 'base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode().'},
        {'id': 'net14-ws-frame',
         'mode': 'stdout',
         'title': 'WebSocket: кадры',
         'statement': 'Напишите encode_text(text) — серверный (немаскированный) текстовый кадр: байт 0x81, '
                      'затем длина (для длины < 126 — один байт; для 126…65535 — байт 126 и 2 байта длины '
                      'big-endian), затем UTF-8. И decode_frame(data) -> (opcode, payload_bytes) для кадра '
                      'клиента: если установлен бит маски (второй байт & 0x80), после длины идут 4 байта '
                      'ключа маски, и каждый байт данных нужно обработать XOR с ключом[i % 4]. Опкод — '
                      'младшие 4 бита первого байта.',
         'starter': 'import struct\n'
                    '\n'
                    '\n'
                    'def encode_text(text):\n'
                    '    pass\n'
                    '\n'
                    '\n'
                    'def decode_frame(data):\n'
                    '    pass\n',
         'driver': "print(encode_text('hi'))\n"
                   "print(len(encode_text('x' * 300)), encode_text('x' * 300)[:4])\n"
                   "print(decode_frame(encode_text('привет')))\n"
                   'key = bytes([1, 2, 3, 4])\n'
                   "msg = b'Hello'\n"
                   'frame = bytes([0x81, 0x80 | len(msg)]) + key + bytes(b ^ key[i % 4] for i, b in '
                   'enumerate(msg))\n'
                   'print(decode_frame(frame))\n',
         'expected': ["b'\\x81\\x02hi'",
                      "304 b'\\x81~\\x01,'",
                      "(1, b'\\xd0\\xbf\\xd1\\x80\\xd0\\xb8\\xd0\\xb2\\xd0\\xb5\\xd1\\x82')",
                      "(1, b'Hello')"],
         'hint': "Длина < 126 — в одном байте; иначе 126 + struct.pack('>H', n). Маска: payload[i] ^ key[i "
                 '% 4].'},
        {'id': 'net14-sse',
         'mode': 'stdout',
         'title': 'Server-Sent Events: формат',
         'statement': 'Напишите sse_encode(events) и sse_decode(text). События — список словарей с ключами '
                      'data (строка, может быть многострочной), необязательными event и id. Кодирование: '
                      "для каждого события строки 'id: …', 'event: …' (если есть), затем для каждой строки "
                      "data — 'data: …', и пустая строка в конце. Декодирование — обратно: блоки разделены "
                      'пустой строкой; многострочные data склеиваются через \\n. Верните список словарей '
                      'только с теми ключами, что были в блоке.',
         'starter': 'def sse_encode(events):\n    pass\n\n\ndef sse_decode(text):\n    pass\n',
         'driver': "evs = [{'id': '1', 'event': 'price', 'data': '101.5'}, {'data': 'line1\\nline2'}]\n"
                   'txt = sse_encode(evs)\n'
                   'print(repr(txt))\n'
                   'print(sse_decode(txt))\n'
                   'print(sse_decode(txt) == evs)\n',
         'expected': ["'id: 1\\nevent: price\\ndata: 101.5\\n\\ndata: line1\\ndata: line2\\n\\n'",
                      "[{'id': '1', 'event': 'price', 'data': '101.5'}, {'data': 'line1\\nline2'}]",
                      'True'],
         'hint': "Кодирование: список строк и join('\\n'); декодирование: разбейте на блоки по пустой "
                 "строке, строку — через partition(': '), data собирайте списком."},
        {'id': 'net14-varint',
         'mode': 'stdout',
         'title': 'Protobuf: varint',
         'statement': 'Напишите encode_varint(n) -> bytes и decode_varint(data) -> (число, '
                      'сколько_байт_прочитано). В varint число раскладывается по 7 бит, младшие группы '
                      'идут первыми, у всех байтов, кроме последнего, старший бит равен 1. Например, 300 → '
                      "b'\\xac\\x02'. Добавьте pb_field(field_number, value) -> bytes: ключ поля "
                      'varint((field_number << 3) | 0), затем varint(value).',
         'starter': 'def encode_varint(n):\n'
                    '    pass\n'
                    '\n'
                    '\n'
                    'def decode_varint(data):\n'
                    '    pass\n'
                    '\n'
                    '\n'
                    'def pb_field(field_number, value):\n'
                    '    pass\n',
         'driver': 'print(encode_varint(0), encode_varint(1), encode_varint(127), encode_varint(128), '
                   'encode_varint(300))\n'
                   "print(decode_varint(b'\\xac\\x02rest'))\n"
                   'print(all(decode_varint(encode_varint(x))[0] == x for x in (0, 5, 127, 128, 16383, '
                   '16384, 2 ** 32)))\n'
                   'print(pb_field(1, 150))\n',
         'expected': ["b'\\x00' b'\\x01' b'\\x7f' b'\\x80\\x01' b'\\xac\\x02'",
                      '(300, 2)',
                      'True',
                      "b'\\x08\\x96\\x01'"],
         'hint': 'Цикл: b = n & 0x7F; n >>= 7; если n ещё не ноль — добавьте b | 0x80, иначе b и конец. '
                 'Декодирование: n |= (b & 0x7F) << (7 * i).'},
        {'id': 'net14-grpc-frame',
         'mode': 'stdout',
         'title': 'gRPC: префикс сообщения',
         'statement': 'Каждое сообщение gRPC идёт с 5-байтовым префиксом: 1 байт флага сжатия (0) и 4 '
                      'байта длины big-endian. Напишите grpc_frame(payload) -> bytes и '
                      'grpc_unframe(stream) -> список сообщений из байтового потока, где подряд идёт '
                      'несколько кадров. Если последний кадр обрезан (данных меньше заявленной длины), он '
                      'игнорируется.',
         'starter': 'import struct\n'
                    '\n'
                    '\n'
                    'def grpc_frame(payload):\n'
                    '    pass\n'
                    '\n'
                    '\n'
                    'def grpc_unframe(stream):\n'
                    '    pass\n',
         'driver': "a = grpc_frame(b'hello')\n"
                   'print(a)\n'
                   "s = a + grpc_frame(b'') + grpc_frame(b'world')\n"
                   'print(grpc_unframe(s))\n'
                   'print(grpc_unframe(s[:-2]))\n'
                   "print(grpc_unframe(b''))\n",
         'expected': ["b'\\x00\\x00\\x00\\x00\\x05hello'",
                      "[b'hello', b'', b'world']",
                      "[b'hello', b'']",
                      '[]'],
         'hint': "struct.pack('>I', len(payload)) — 4 байта длины; при разборе двигайтесь по потоку: 5 "
                 'байт заголовка + длина.'},
    ],
}
