"""Задачи книги «Базы данных: под капотом»: главы 4–6."""

TASKS: dict[int, list[dict]] = {
    4: [
        {
            "id": "st-wal-recover",
            "mode": "func",
            "func": "recover",
            "title": "Восстановление по журналу (WAL)",
            "statement": (
                "Журнал упреждающей записи — список записей: ['begin', tx], ['set', "
                "tx, ключ, значение], ['delete', tx, ключ], ['commit', tx], "
                "['abort', tx]. После сбоя восстановление повторяет (redo) в "
                "порядке журнала изменения только тех транзакций, у которых есть "
                "запись commit; остальные (abort и не завершённые) игнорируются. "
                "Напишите функцию recover(log): верните словарь «ключ → значение» "
                "после восстановления (начальное состояние пустое)."
            ),
            "starter": "def recover(log):\n    pass\n",
            "tests": [
                {"args": [[["begin", 1], ["set", 1, "a", 1], ["set", 1, "b", 2], ["commit", 1]]], "expected": {"a": 1, "b": 2}},
                {"args": [[["begin", 1], ["set", 1, "a", 1], ["begin", 2], ["set", 2, "a", 99], ["commit", 1]]], "expected": {"a": 1}},
                {"args": [[["begin", 1], ["set", 1, "a", 1], ["abort", 1], ["begin", 2], ["set", 2, "b", 5], ["commit", 2]]], "expected": {"b": 5}},
                {"args": [[["begin", 1], ["set", 1, "a", 1], ["commit", 1], ["begin", 2], ["delete", 2, "a"], ["commit", 2]]], "expected": {}},
                {"args": [[]], "expected": {}},
                {"args": [[["begin", 1], ["set", 1, "x", 1], ["begin", 2], ["set", 2, "x", 2], ["commit", 2], ["commit", 1]]], "expected": {"x": 2}},
            ],
            "hint": "Сначала найдите множество зафиксированных транзакций, затем одним проходом по журналу примените их set/delete.",
        },
        {
            "id": "st-lsm-merge",
            "mode": "func",
            "func": "compact",
            "title": "Компактация LSM-дерева",
            "statement": (
                "Напишите функцию compact(runs, drop_tombstones): runs — "
                "отсортированные по ключу списки пар [ключ, значение] (значение "
                "None — надгробие, то есть удалённый ключ), от самого НОВОГО к "
                "самому старому. Верните слитый отсортированный список: для каждого "
                "ключа берётся запись из самого нового прогона; надгробия "
                "отбрасываются, если drop_tombstones истинно."
            ),
            "starter": "def compact(runs, drop_tombstones):\n    pass\n",
            "tests": [
                {"args": [[[["a", 2], ["c", None]], [["a", 1], ["b", 1], ["c", 1]]], False], "expected": [["a", 2], ["b", 1], ["c", None]]},
                {"args": [[[["a", 2], ["c", None]], [["a", 1], ["b", 1], ["c", 1]]], True], "expected": [["a", 2], ["b", 1]]},
                {"args": [[], True], "expected": []},
                {"args": [[[["x", 1]]], True], "expected": [["x", 1]]},
                {"args": [[[["k", None]], [["k", 5]]], True], "expected": []},
                {"args": [[[["k", None]], [["k", 5]]], False], "expected": [["k", None]]},
                {"args": [[[["b", 3]], [["a", 1]], [["c", 2]]], False], "expected": [["a", 1], ["b", 3], ["c", 2]]},
            ],
            "hint": "Идите по прогонам от нового к старому и берите первое вхождение ключа; потом отсортируйте.",
        },
        {
            "id": "st-memtable-flush",
            "mode": "func",
            "func": "run_ops",
            "title": "Мемтейбл и сброс на диск",
            "statement": (
                "Напишите функцию run_ops(ops, limit): ops — ['put', ключ, "
                "значение] и ['delete', ключ]. Операции применяются к мемтейблу "
                "(словарь; delete записывает надгробие None). Как только после "
                "операции в мемтейбле стало limit или больше ключей, он "
                "сбрасывается на диск как новый отсортированный список [ключ, "
                "значение] и очищается. Верните кортеж "
                "(сброшенные_прогоны_в_порядке_сброса, "
                "остаток_мемтейбла_отсортированным_списком)."
            ),
            "starter": "def run_ops(ops, limit):\n    pass\n",
            "tests": [
                {"args": [[["put", "b", 1], ["put", "a", 2], ["put", "c", 3], ["put", "d", 4]], 3], "expected": ([[["a", 2], ["b", 1], ["c", 3]]], [["d", 4]])},
                {"args": [[["put", "a", 1], ["put", "a", 2], ["put", "a", 3]], 2], "expected": ([], [["a", 3]])},
                {"args": [[["put", "a", 1], ["delete", "a"], ["put", "b", 1]], 2], "expected": ([[["a", None], ["b", 1]]], [])},
                {"args": [[], 3], "expected": ([], [])},
                {"args": [[["put", "x", 1]], 1], "expected": ([[["x", 1]]], [])},
                {"args": [[["put", "k0", 0], ["put", "k1", 1], ["put", "k2", 2], ["put", "k3", 3], ["put", "k4", 4]], 2], "expected": ([[["k0", 0], ["k1", 1]], [["k2", 2], ["k3", 3]]], [["k4", 4]])},
            ],
            "hint": "После каждой операции проверяйте размер словаря; при сбросе кладите отсортированные пары в список прогонов.",
        },
        {
            "id": "st-lsm-get",
            "mode": "func",
            "func": "lsm_get",
            "title": "Чтение из LSM-дерева",
            "statement": (
                "Напишите функцию lsm_get(memtable, runs, key): memtable — словарь "
                "(значение None — надгробие), runs — список словарей-прогонов от "
                "нового к старому. Ищем сначала в мемтейбле, потом по прогонам. "
                "Верните кортеж (значение, сколько_прогонов_прочитано): надгробие и "
                "«не найдено» дают значение None. Попадание в мемтейбл — 0 "
                "прочитанных прогонов; найденное в k-м прогоне — k прочитанных; не "
                "найденное нигде — все прогоны."
            ),
            "starter": "def lsm_get(memtable, runs, key):\n    pass\n",
            "tests": [
                {"args": [{"a": 1}, [{"b": 2}, {"c": 3}], "a"], "expected": (1, 0)},
                {"args": [{"a": 1}, [{"b": 2}, {"c": 3}], "c"], "expected": (3, 2)},
                {"args": [{"a": 1}, [{"b": 2}, {"c": 3}], "z"], "expected": (None, 2)},
                {"args": [{"a": None}, [{"a": 5}], "a"], "expected": (None, 0)},
                {"args": [{}, [{"a": None}, {"a": 5}], "a"], "expected": (None, 1)},
                {"args": [{}, [], "a"], "expected": (None, 0)},
            ],
            "hint": "Надгробие тоже «найдено»: поиск останавливается на нём и возвращает None.",
        },
        {
            "id": "st-bloom",
            "mode": "func",
            "func": "bloom",
            "title": "Фильтр Блума",
            "statement": (
                "Напишите функцию bloom(keys, queries, m, k): битовый массив из m "
                "бит, k хеш-функций h_i(s) = (сумма по позициям p символов c "
                "строки: ord(c) · (i + 3)^p) mod m, i = 0…k−1 (p — номер символа с "
                "нуля). Добавьте все keys, затем для каждого запроса верните True "
                "(«возможно есть»: все k бит установлены) или False («точно нет»). "
                "Результат — список булевых значений."
            ),
            "starter": "def bloom(keys, queries, m, k):\n    pass\n",
            "tests": [
                {"args": [["apple", "banana", "cherry"], ["apple", "banana", "durian", "elder"], 64, 3], "expected": [True, True, False, False]},
                {"args": [[], ["a"], 16, 2], "expected": [False]},
                {"args": [["a"], ["a", "b"], 8, 1], "expected": [True, False]},
                {"args": [["key0", "key1", "key2", "key3", "key4", "key5", "key6", "key7", "key8", "key9"], ["key3", "key99", "zzz", "key9"], 40, 3], "expected": [True, True, False, True]},
                {"args": [["x"], ["x"], 1, 1], "expected": [True]},
            ],
            "hint": "Для каждой хеш-функции i: индекс = сумма ord(c) · (i + 3) ** p по позициям p, взятая по модулю m.",
        },
        {
            "id": "st-lsm-levels",
            "mode": "func",
            "func": "lsm_levels",
            "title": "Уровни LSM и усиление записи",
            "statement": (
                "Напишите функцию lsm_levels(data_mb, memtable_mb, fanout): данные "
                "лежат на уровнях, каждый следующий в fanout раз больше "
                "предыдущего; уровень 1 равен memtable_mb · fanout. Число уровней L "
                "— наименьшее целое ≥ 0, при котором memtable_mb · fanout^L ≥ "
                "data_mb. Оценка усиления записи при уровневой компактации — fanout "
                "· L. Верните кортеж (L, fanout · L)."
            ),
            "starter": "def lsm_levels(data_mb, memtable_mb, fanout):\n    pass\n",
            "tests": [
                {"args": [1000, 64, 10], "expected": (2, 20)},
                {"args": [64, 64, 10], "expected": (0, 0)},
                {"args": [10, 64, 10], "expected": (0, 0)},
                {"args": [1000000, 64, 10], "expected": (5, 50)},
                {"args": [100000, 128, 4], "expected": (5, 20)},
                {"args": [1, 1, 2], "expected": (0, 0)},
                {"args": [1025, 1, 2], "expected": (11, 22)},
            ],
            "hint": "Растите размер в fanout раз, пока он меньше data_mb, и считайте шаги.",
        },
        {
            "id": "st-slotted-pages",
            "mode": "func",
            "func": "pack_pages",
            "title": "Страницы со слотами",
            "statement": (
                "Напишите функцию pack_pages(sizes, page_size): размещаем записи по "
                "порядку в страницы; у страницы заголовок 8 байт, у каждой записи — "
                "слот 4 байта в дополнение к её размеру. Если очередная запись не "
                "помещается, начинается новая страница (прежние не дополняются). "
                "Размер каждой записи помещается в пустую страницу. Верните список "
                "страниц — списки номеров записей."
            ),
            "starter": "def pack_pages(sizes, page_size):\n    pass\n",
            "tests": [
                {"args": [[100, 200, 300, 50], 512], "expected": [[0, 1], [2, 3]]},
                {"args": [[], 512], "expected": []},
                {"args": [[500], 512], "expected": [[0]]},
                {"args": [[250, 250, 250], 512], "expected": [[0], [1], [2]]},
                {"args": [[10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 64], "expected": [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]},
                {"args": [[100, 400, 100], 512], "expected": [[0], [1], [2]]},
            ],
            "hint": "Накопитель used начинается с 8; запись занимает size + 4; не влезает — закройте страницу и начните новую.",
        },
    ],
    5: [
        {
            "id": "nosql-kv-ttl",
            "mode": "func",
            "func": "kv_run",
            "title": "Key-Value со сроком жизни",
            "statement": (
                "Напишите функцию kv_run(ops): операции ['set', ключ, значение, "
                "ttl, now] (ttl — секунды или None — навсегда), ['get', ключ, now], "
                "['del', ключ]. Ключ истекает в момент now_записи + ttl: при now ≥ "
                "этого момента значения уже нет. Верните список результатов всех "
                "'get' (значение или None)."
            ),
            "starter": "def kv_run(ops):\n    pass\n",
            "tests": [
                {"args": [[["set", "a", 1, 10, 0], ["get", "a", 5], ["get", "a", 10], ["get", "a", 11]]], "expected": [1, None, None]},
                {"args": [[["set", "a", 1, None, 0], ["get", "a", 1000000]]], "expected": [1]},
                {"args": [[["set", "a", 1, 5, 0], ["set", "a", 2, 5, 4], ["get", "a", 8]]], "expected": [2]},
                {"args": [[["get", "x", 1]]], "expected": [None]},
                {"args": [[["set", "a", 1, 5, 0], ["del", "a"], ["get", "a", 1]]], "expected": [None]},
                {"args": [[]], "expected": []},
            ],
            "hint": "Храните вместе со значением момент истечения; при чтении сравнивайте now с ним.",
        },
        {
            "id": "nosql-doc-match",
            "mode": "func",
            "func": "doc_match",
            "title": "Фильтр документов (как в MongoDB)",
            "statement": (
                "Напишите функцию doc_match(doc, query): doc — словарь (возможны "
                "вложенные словари и списки), query — условия. Ключ условия — путь "
                "через точку ('address.city'). Значение условия: обычное — "
                "равенство (если в документе список, а условие — скаляр, достаточно "
                "совпадения с любым элементом); либо словарь операторов: $gt, $gte, "
                "$lt, $lte, $ne, $in (список), $exists (True/False). Все условия "
                "верхнего уровня объединяются по И; специальный ключ '$or' со "
                "списком подзапросов — ИЛИ. Отсутствующее поле для $gt/$lt и "
                "равенства — не совпадает. Верните True/False."
            ),
            "starter": "def doc_match(doc, query):\n    pass\n",
            "tests": [
                {"args": [{"name": "Ann", "age": 30, "address": {"city": "Moscow"}, "tags": ["a", "b"]}, {"age": {"$gt": 18}, "address.city": "Moscow"}], "expected": True},
                {"args": [{"name": "Ann", "age": 30, "address": {"city": "Moscow"}, "tags": ["a", "b"]}, {"tags": "b"}], "expected": True},
                {"args": [{"name": "Ann", "age": 30, "address": {"city": "Moscow"}, "tags": ["a", "b"]}, {"tags": "z"}], "expected": False},
                {"args": [{"age": 30}, {"age": {"$gte": 30, "$lt": 31}}], "expected": True},
                {"args": [{"age": 30}, {"age": {"$in": [10, 20]}}], "expected": False},
                {"args": [{"age": 30}, {"city": {"$exists": False}}], "expected": True},
                {"args": [{"age": 30}, {"city": {"$exists": True}}], "expected": False},
                {"args": [{"age": 30}, {"city": "x"}], "expected": False},
                {"args": [{"age": 30}, {"$or": [{"age": 20}, {"age": {"$gt": 25}}]}], "expected": True},
                {"args": [{"age": 30}, {"$or": [{"age": 20}, {"age": 21}]}], "expected": False},
                {"args": [{"a": {"b": {"c": 1}}}, {"a.b.c": 1}], "expected": True},
                {"args": [{"age": 30}, {"age": {"$ne": 30}}], "expected": False},
                {"args": [{}, {}], "expected": True},
            ],
            "hint": "Путь через точку проходите по вложенным словарям; для каждого оператора — своя проверка; $or — любое из подусловий.",
        },
        {
            "id": "nosql-doc-update",
            "mode": "func",
            "func": "doc_update",
            "title": "Обновление документа ($set, $inc, $unset)",
            "statement": (
                "Напишите функцию doc_update(doc, update): update — словарь с "
                "ключами '$set' ({путь: значение}), '$inc' ({путь: число}) и "
                "'$unset' ({путь: любое}). Пути через точку ('stats.views'); '$set' "
                "создаёт недостающие вложенные словари; '$inc' на отсутствующем "
                "поле считает его нулём; '$unset' удаляет поле, если оно есть. "
                "Порядок применения: $set, $inc, $unset. Исходный документ не "
                "меняйте — верните новый."
            ),
            "starter": "import copy\n\n\ndef doc_update(doc, update):\n    pass\n",
            "tests": [
                {"args": [{"name": "Ann"}, {"$set": {"age": 30}}], "expected": {"name": "Ann", "age": 30}},
                {"args": [{"stats": {"views": 5}}, {"$inc": {"stats.views": 1}}], "expected": {"stats": {"views": 6}}},
                {"args": [{}, {"$inc": {"a.b": 3}}], "expected": {"a": {"b": 3}}},
                {"args": [{"a": 1, "b": 2}, {"$unset": {"a": ""}}], "expected": {"b": 2}},
                {"args": [{"a": {"b": 1, "c": 2}}, {"$unset": {"a.b": ""}, "$set": {"a.d": 4}}], "expected": {"a": {"c": 2, "d": 4}}},
                {"args": [{"a": 1}, {"$unset": {"x.y": ""}}], "expected": {"a": 1}},
                {"args": [{"n": 1}, {"$set": {"n": 10}, "$inc": {"n": 5}}], "expected": {"n": 15}},
            ],
            "hint": "Вспомогательная функция: по пути дойти до родительского словаря (создавая по необходимости) и вернуть его с именем последнего поля.",
        },
        {
            "id": "nosql-wide-column",
            "mode": "func",
            "func": "partition_query",
            "title": "Широкая колонка: партиция и кластеризация",
            "statement": (
                "В Cassandra строка живёт в партиции (partition key), а внутри "
                "партиции строки отсортированы по ключу кластеризации. Напишите "
                "функцию partition_query(rows, pk, lo, hi): rows — список [pk, ck, "
                "значение]; верните значения строк партиции pk, у которых lo ≤ ck ≤ "
                "hi, в порядке возрастания ck."
            ),
            "starter": "def partition_query(rows, pk, lo, hi):\n    pass\n",
            "tests": [
                {"args": [[["u1", 3, "c"], ["u1", 1, "a"], ["u2", 2, "x"], ["u1", 2, "b"], ["u1", 9, "z"]], "u1", 1, 3], "expected": ["a", "b", "c"]},
                {"args": [[], "u1", 0, 10], "expected": []},
                {"args": [[["u1", 5, "a"]], "u2", 0, 10], "expected": []},
                {"args": [[["u1", 5, "a"], ["u1", 6, "b"]], "u1", 6, 6], "expected": ["b"]},
                {"args": [[["u1", "2024-01", "a"], ["u1", "2024-03", "c"], ["u1", "2024-02", "b"]], "u1", "2024-02", "2024-12"], "expected": ["b", "c"]},
            ],
            "hint": "Отфильтруйте по партиции и диапазону, затем отсортируйте по ck.",
        },
        {
            "id": "nosql-graph-fof",
            "mode": "func",
            "func": "friends_of_friends",
            "title": "Друзья друзей",
            "statement": (
                "Граф дружбы неориентированный. Напишите функцию "
                "friends_of_friends(edges, user): edges — пары [a, b]. Верните "
                "список рекомендаций [имя, число_общих_друзей]: люди, которые "
                "дружат с друзьями user, но не являются самим user и не его "
                "друзьями. Сортировка: по числу общих друзей (убывание), затем по "
                "имени."
            ),
            "starter": "def friends_of_friends(edges, user):\n    pass\n",
            "tests": [
                {"args": [[["a", "b"], ["a", "c"], ["b", "d"], ["c", "d"], ["c", "e"], ["f", "g"]], "a"], "expected": [["d", 2], ["e", 1]]},
                {"args": [[], "a"], "expected": []},
                {"args": [[["a", "b"]], "a"], "expected": []},
                {"args": [[["a", "b"], ["b", "c"], ["c", "a"]], "a"], "expected": []},
                {"args": [[["a", "b"], ["a", "c"], ["b", "x"], ["c", "x"], ["c", "y"]], "a"], "expected": [["x", 2], ["y", 1]]},
            ],
            "hint": "Для каждого друга перечислите его друзей и накопите счётчик, исключая себя и уже друзей.",
        },
        {
            "id": "nosql-graph-path",
            "mode": "func",
            "func": "shortest_path",
            "title": "Кратчайшая цепочка знакомств",
            "statement": (
                "Напишите функцию shortest_path(edges, a, b): неориентированный "
                "граф из пар [x, y]. Верните список вершин кратчайшего пути из a в "
                "b (включая концы) или None, если пути нет. Поиск в ширину; соседей "
                "перебирайте по алфавиту (так путь определяется однозначно). Для a "
                "== b — [a]."
            ),
            "starter": "from collections import deque\n\n\ndef shortest_path(edges, a, b):\n    pass\n",
            "tests": [
                {"args": [[["a", "b"], ["b", "c"], ["a", "d"], ["d", "c"]], "a", "c"], "expected": ["a", "b", "c"]},
                {"args": [[["a", "b"]], "a", "z"], "expected": None},
                {"args": [[], "a", "a"], "expected": ["a"]},
                {"args": [[["a", "b"], ["b", "c"], ["c", "d"], ["a", "x"], ["x", "d"]], "a", "d"], "expected": ["a", "x", "d"]},
                {"args": [[["m", "n"], ["x", "y"]], "m", "y"], "expected": None},
            ],
            "hint": "BFS с хранением предыдущей вершины; восстанавливайте путь от b назад.",
        },
        {
            "id": "nosql-rle",
            "mode": "func",
            "func": "rle",
            "title": "Сжатие колонки (RLE)",
            "statement": (
                "Колоночные хранилища хорошо сжимают столбцы с повторами. Напишите "
                "функцию rle(column): список значений -> список пар [значение, "
                "сколько_подряд]. Пустой столбец — пустой список."
            ),
            "starter": "def rle(column):\n    pass\n",
            "tests": [
                {"args": [["RU", "RU", "RU", "US", "US", "RU"]], "expected": [["RU", 3], ["US", 2], ["RU", 1]]},
                {"args": [[]], "expected": []},
                {"args": [[1]], "expected": [[1, 1]]},
                {"args": [[0, 0, 0, 0]], "expected": [[0, 4]]},
                {"args": [["a", "b", "a", "b"]], "expected": [["a", 1], ["b", 1], ["a", 1], ["b", 1]]},
            ],
            "hint": "Если значение равно последней паре — увеличьте счётчик, иначе добавьте новую.",
        },
    ],
    6: [
        {
            "id": "repl-lag",
            "mode": "func",
            "func": "follower_state",
            "title": "Отставание реплики",
            "statement": (
                "Лидер зафиксировал записи в моменты writes (миллисекунды, по "
                "возрастанию). Реплика применяет каждую запись через delay мс после "
                "лидера. Напишите функцию follower_state(writes, delay, t): в "
                "момент t верните кортеж (сколько_записей_применено, "
                "отставание_мс), где отставание = t − момент самой старой "
                "неприменённой записи на лидере (0, если неприменённых нет). "
                "Считайте только записи, зафиксированные лидером не позже t."
            ),
            "starter": "def follower_state(writes, delay, t):\n    pass\n",
            "tests": [
                {"args": [[0, 10, 20], 15, 20], "expected": (1, 10)},
                {"args": [[0, 10, 20], 15, 100], "expected": (3, 0)},
                {"args": [[0, 10, 20], 15, 5], "expected": (0, 5)},
                {"args": [[], 5, 50], "expected": (0, 0)},
                {"args": [[100, 200], 50, 120], "expected": (0, 20)},
                {"args": [[0], 0, 0], "expected": (1, 0)},
            ],
            "hint": "Применено то, у чего w + delay ≤ t; самая старая неприменённая — первая после применённых.",
        },
        {
            "id": "repl-pick-replica",
            "mode": "func",
            "func": "pick_replica",
            "title": "Чтение собственных записей",
            "statement": (
                "Клиент после записи и чтений должен видеть не более старые данные, "
                "чем видел раньше (read-your-writes и монотонные чтения). Напишите "
                "функцию pick_replica(replicas, last_write, last_read): replicas — "
                "список [имя, применённый_номер_записи]; порог = max(last_write, "
                "last_read). Верните имя первой по порядку реплики с применённым "
                "номером ≥ порога, а если такой нет — 'leader'."
            ),
            "starter": "def pick_replica(replicas, last_write, last_read):\n    pass\n",
            "tests": [
                {"args": [[["r1", 5], ["r2", 9]], 7, 0], "expected": "r2"},
                {"args": [[["r1", 5], ["r2", 9]], 3, 0], "expected": "r1"},
                {"args": [[["r1", 5], ["r2", 9]], 3, 8], "expected": "r2"},
                {"args": [[["r1", 5], ["r2", 9]], 10, 0], "expected": "leader"},
                {"args": [[], 1, 1], "expected": "leader"},
                {"args": [[["r1", 0]], 0, 0], "expected": "r1"},
            ],
            "hint": "Реплика подходит, если applied не меньше порога; иначе остаётся лидер.",
        },
        {
            "id": "repl-quorum",
            "mode": "func",
            "func": "quorum_info",
            "title": "Кворумы чтения и записи",
            "statement": (
                "Напишите функцию quorum_info(n, w, r): n — число реплик, w — "
                "сколько подтверждений нужно записи, r — сколько реплик опрашивает "
                "чтение. Верните словарь {'strong': w + r > n, 'write_tolerates': n "
                "− w, 'read_tolerates': n − r} (сколько отказов переживает запись и "
                "чтение) — при условии 1 ≤ w, r ≤ n."
            ),
            "starter": "def quorum_info(n, w, r):\n    pass\n",
            "tests": [
                {"args": [3, 2, 2], "expected": {"strong": True, "write_tolerates": 1, "read_tolerates": 1}},
                {"args": [3, 1, 1], "expected": {"strong": False, "write_tolerates": 2, "read_tolerates": 2}},
                {"args": [5, 3, 3], "expected": {"strong": True, "write_tolerates": 2, "read_tolerates": 2}},
                {"args": [5, 5, 1], "expected": {"strong": True, "write_tolerates": 0, "read_tolerates": 4}},
                {"args": [5, 1, 5], "expected": {"strong": True, "write_tolerates": 4, "read_tolerates": 0}},
                {"args": [1, 1, 1], "expected": {"strong": True, "write_tolerates": 0, "read_tolerates": 0}},
                {"args": [4, 2, 2], "expected": {"strong": False, "write_tolerates": 2, "read_tolerates": 2}},
            ],
            "hint": "Пересечение любых W и R реплик гарантировано, если W + R > N.",
        },
        {
            "id": "repl-vector-clock",
            "mode": "func",
            "func": "compare_clocks",
            "title": "Векторные часы",
            "statement": (
                "Напишите функцию compare_clocks(a, b): a и b — словари «узел → "
                "счётчик» (нет узла = 0). Верните 'equal', если все счётчики равны; "
                "'before', если a ≤ b везде и a ≠ b; 'after', если a ≥ b везде и a "
                "≠ b; иначе 'concurrent'."
            ),
            "starter": "def compare_clocks(a, b):\n    pass\n",
            "tests": [
                {"args": [{"A": 1, "B": 2}, {"A": 1, "B": 2}], "expected": "equal"},
                {"args": [{"A": 1}, {"A": 2, "B": 1}], "expected": "before"},
                {"args": [{"A": 3, "B": 1}, {"A": 2, "B": 1}], "expected": "after"},
                {"args": [{"A": 2}, {"B": 2}], "expected": "concurrent"},
                {"args": [{}, {}], "expected": "equal"},
                {"args": [{}, {"A": 1}], "expected": "before"},
                {"args": [{"A": 0}, {}], "expected": "equal"},
                {"args": [{"A": 2, "B": 1}, {"A": 1, "B": 2}], "expected": "concurrent"},
            ],
            "hint": "Постройте два флага: «a не больше b везде» и «a не меньше b везде».",
        },
        {
            "id": "repl-lww-merge",
            "mode": "func",
            "func": "lww_merge",
            "title": "Last-Write-Wins при слиянии реплик",
            "statement": (
                "Напишите функцию lww_merge(replicas): replicas — список словарей "
                "«ключ → [значение, метка_времени]» от разных реплик. Для каждого "
                "ключа победит запись с наибольшей меткой; при равных метках — с "
                "лексикографически большим значением (в виде строки str). Верните "
                "слитый словарь в том же формате."
            ),
            "starter": "def lww_merge(replicas):\n    pass\n",
            "tests": [
                {"args": [[{"a": ["x", 1], "b": ["y", 5]}, {"a": ["z", 3]}]], "expected": {"a": ["z", 3], "b": ["y", 5]}},
                {"args": [[]], "expected": {}},
                {"args": [[{"a": ["x", 1]}, {"a": ["y", 1]}]], "expected": {"a": ["y", 1]}},
                {"args": [[{"k": [1, 10]}, {"k": [2, 9]}, {"k": [3, 11]}]], "expected": {"k": [3, 11]}},
                {"args": [[{"a": ["q", 2]}]], "expected": {"a": ["q", 2]}},
            ],
            "hint": "Сравнивайте пары (метка, str(значение)); берите большую.",
        },
        {
            "id": "repl-promote",
            "mode": "func",
            "func": "promote",
            "title": "Выбор нового лидера",
            "statement": (
                "Лидер вышел из строя. Напишите функцию promote(replicas, "
                "leader_last): replicas — список [имя, жива_ли, "
                "применённый_номер_записи]; leader_last — последний номер записи, "
                "подтверждённой лидером клиентам. Новым лидером становится живая "
                "реплика с наибольшим применённым номером (при равенстве — первая "
                "по порядку). Верните кортеж (имя, потерянных_записей = max(0, "
                "leader_last − применённый_номер)); если живых реплик нет — (None, "
                "leader_last)."
            ),
            "starter": "def promote(replicas, leader_last):\n    pass\n",
            "tests": [
                {"args": [[["r1", True, 8], ["r2", True, 10], ["r3", False, 12]], 12], "expected": ("r2", 2)},
                {"args": [[["r1", False, 8]], 5], "expected": (None, 5)},
                {"args": [[], 3], "expected": (None, 3)},
                {"args": [[["a", True, 5], ["b", True, 5]], 5], "expected": ("a", 0)},
                {"args": [[["a", True, 20]], 10], "expected": ("a", 0)},
                {"args": [[["a", True, 7], ["b", True, 9]], 9], "expected": ("b", 0)},
            ],
            "hint": "Среди живых — максимум по применённому номеру (строго больше при замене — тогда побеждает первая); потери = разница с подтверждённым.",
        },
        {
            "id": "repl-commit-latency",
            "mode": "func",
            "func": "commit_latency",
            "title": "Синхронная и полусинхронная репликация",
            "statement": (
                "Лидер ждёт подтверждения от реплик, прежде чем ответить клиенту. "
                "Напишите функцию commit_latency(latencies, acks_needed): latencies "
                "— задержки подтверждения каждой реплики (мс), acks_needed — "
                "сколько подтверждений ждать (0 — асинхронная репликация, не ждём "
                "никого). Верните время ответа клиенту — задержку acks_needed-го по "
                "скорости подтверждения (0 для 0 подтверждений). Если подтверждений "
                "требуется больше, чем реплик — None."
            ),
            "starter": "def commit_latency(latencies, acks_needed):\n    pass\n",
            "tests": [
                {"args": [[5, 50, 120], 0], "expected": 0},
                {"args": [[5, 50, 120], 1], "expected": 5},
                {"args": [[5, 50, 120], 2], "expected": 50},
                {"args": [[5, 50, 120], 3], "expected": 120},
                {"args": [[5, 50, 120], 4], "expected": None},
                {"args": [[], 0], "expected": 0},
                {"args": [[30], 1], "expected": 30},
            ],
            "hint": "Отсортируйте задержки: k-е подтверждение приходит со временем k-й по счёту задержки.",
        },
    ],
}
