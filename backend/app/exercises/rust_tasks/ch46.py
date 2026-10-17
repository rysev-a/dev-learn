"""Задачи книги «Изучаем Rust»: глава 46 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {46: [{'id': 'r46-roundtrip',
  'mode': 'rust',
  'title': 'Туда и обратно',
  'statement': 'Структура Room { id: u32, name: String } должна превращаться в JSON-строку и '
               'обратно. Напечатайте строку для Room { id: 7, name: "общий" } и результат разбора '
               'строки {"id":9,"name":"dev"} в виде Debug.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"id":7,"name":"общий"}\n'
               'Room { id: 9, name: "dev" }',
  'starter': 'use serde::{Deserialize, Serialize};\n'
             '\n'
             'struct Room {\n'
             '    id: u32,\n'
             '    name: String,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    let s = serde_json::to_string(&Room { id: 7, name: "общий".into() }).unwrap();\n'
             '    println!("{s}");\n'
             '    let r: Room = serde_json::from_str(r#"{"id":9,"name":"dev"}"#).unwrap();\n'
             '    println!("{r:?}");\n'
             '}\n',
  'driver': '',
  'hint': '#[derive(Serialize, Deserialize, Debug)]; serde_json::to_string и from_str.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"id":7,"name":"общий"}', 'Room { id: 9, name: "dev" }']},
 {'id': 'r46-camel',
  'mode': 'rust',
  'title': 'camelCase для клиентов',
  'statement': 'Структура Msg { room_id: u32, sent_at: u64, author_name: String } должна '
               'сериализоваться с ключами roomId, sentAt, authorName и так же разбираться. '
               'Напечатайте JSON и разбор строки {"roomId":2,"sentAt":5,"authorName":"аня"}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"roomId":1,"sentAt":100,"authorName":"боря"}\n'
               'Msg { room_id: 2, sent_at: 5, author_name: "аня" }',
  'starter': 'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'struct Msg {\n'
             '    room_id: u32,\n'
             '    sent_at: u64,\n'
             '    author_name: String,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{}", serde_json::to_string(&Msg { room_id: 1, sent_at: 100, '
             'author_name: "боря".into() }).unwrap());\n'
             '    let m: Msg = '
             'serde_json::from_str(r#"{"roomId":2,"sentAt":5,"authorName":"аня"}"#).unwrap();\n'
             '    println!("{m:?}");\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(rename_all = "camelCase")] на структуре.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"roomId":1,"sentAt":100,"authorName":"боря"}',
               'Msg { room_id: 2, sent_at: 5, author_name: "аня" }']},
 {'id': 'r46-skip-none',
  'mode': 'rust',
  'title': 'Пропуск пустых полей',
  'statement': 'Структура Out { id: u32, reply_to: Option<u64>, edited: Option<String> } '
               'сериализуется без полей, равных None. Напечатайте JSON для трёх значений: оба поля '
               'пусты, одно задано, оба заданы.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"id":1}\n'
               '{"id":2,"reply_to":1}\n'
               '{"id":3,"reply_to":2,"edited":"правка"}',
  'starter': 'use serde::Serialize;\n'
             '\n'
             '#[derive(Serialize)]\n'
             'struct Out {\n'
             '    id: u32,\n'
             '    reply_to: Option<u64>,\n'
             '    edited: Option<String>,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    for o in [Out { id: 1, reply_to: None, edited: None }, Out { id: 2, reply_to: '
             'Some(1), edited: None }, Out { id: 3, reply_to: Some(2), edited: '
             'Some("правка".into()) }] {\n'
             '        println!("{}", serde_json::to_string(&o).unwrap());\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(skip_serializing_if = "Option::is_none")] на каждом необязательном поле.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"id":1}', '{"id":2,"reply_to":1}', '{"id":3,"reply_to":2,"edited":"правка"}']},
 {'id': 'r46-defaults',
  'mode': 'rust',
  'title': 'Значения по умолчанию',
  'statement': 'Структура Query { text: String, limit: u32, exact: bool } разбирается из JSON, в '
               'котором limit и exact можно не указывать: limit по умолчанию 20, exact — false. '
               'Напечатайте разбор трёх строк: {"text":"a"}, {"text":"b","limit":5}, '
               '{"text":"c","exact":true,"limit":1}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Query { text: "a", limit: 20, exact: false }\n'
               'Query { text: "b", limit: 5, exact: false }\n'
               'Query { text: "c", limit: 1, exact: true }',
  'starter': 'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize, Debug)]\n'
             'struct Query {\n'
             '    text: String,\n'
             '    limit: u32,\n'
             '    exact: bool,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    for s in [r#"{"text":"a"}"#, r#"{"text":"b","limit":5}"#, '
             'r#"{"text":"c","exact":true,"limit":1}"#] {\n'
             '        println!("{:?}", serde_json::from_str::<Query>(s).unwrap());\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(default = "twenty")] для limit и #[serde(default)] для exact.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Query { text: "a", limit: 20, exact: false }',
               'Query { text: "b", limit: 5, exact: false }',
               'Query { text: "c", limit: 1, exact: true }']},
 {'id': 'r46-deny-unknown',
  'mode': 'rust',
  'title': 'Запрет неизвестных полей',
  'statement': 'Структура Login { user: String, pass: String } отвергает JSON с лишними полями. '
               'Напечатайте, успешен ли разбор для {"user":"a","pass":"b"}, для '
               '{"user":"a","pass":"b","admin":true} и содержит ли текст ошибки второго случая '
               'слова «unknown field».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'true\n'
               'false\n'
               'true',
  'starter': 'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize, Debug)]\n'
             'struct Login {\n'
             '    user: String,\n'
             '    pass: String,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{}", '
             'serde_json::from_str::<Login>(r#"{"user":"a","pass":"b"}"#).is_ok());\n'
             '    let e = '
             'serde_json::from_str::<Login>(r#"{"user":"a","pass":"b","admin":true}"#);\n'
             '    println!("{}", e.is_ok());\n'
             '    println!("{}", e.unwrap_err().to_string().contains("unknown field"));\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(deny_unknown_fields)].',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['true', 'false', 'true']},
 {'id': 'r46-alias',
  'mode': 'rust',
  'title': 'Переименование через alias',
  'statement': 'Структура Join { room: u32 } раньше называлась {"room_id": ...}. Клиенты шлют и '
               '{"room":1}, и старое {"room_id":2}; сервер отдаёт только новое имя. Напечатайте '
               'разбор обоих вариантов и сериализацию.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Join { room: 1 }\n'
               'Join { room: 2 }\n'
               '{"room":3}',
  'starter': 'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'struct Join {\n'
             '    room: u32,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{:?}", serde_json::from_str::<Join>(r#"{"room":1}"#).unwrap());\n'
             '    println!("{:?}", serde_json::from_str::<Join>(r#"{"room_id":2}"#).unwrap());\n'
             '    println!("{}", serde_json::to_string(&Join { room: 3 }).unwrap());\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(alias = "room_id")].',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Join { room: 1 }', 'Join { room: 2 }', '{"room":3}']},
 {'id': 'r46-flatten',
  'mode': 'rust',
  'title': 'Вложение полей: flatten',
  'statement': 'Структура Msg { text: String, meta: Meta } сериализуется плоско: поля Meta { id: '
               'u32, at: u64 } лежат на одном уровне с text. Напечатайте JSON и разбор строки '
               '{"text":"привет","id":4,"at":99}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"text":"привет","id":4,"at":99}\n'
               'Msg { text: "привет", meta: Meta { id: 4, at: 99 } }',
  'starter': 'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'struct Meta {\n'
             '    id: u32,\n'
             '    at: u64,\n'
             '}\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'struct Msg {\n'
             '    text: String,\n'
             '    meta: Meta,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{}", serde_json::to_string(&Msg { text: "привет".into(), meta: Meta { '
             'id: 4, at: 99 } }).unwrap());\n'
             '    println!("{:?}", '
             'serde_json::from_str::<Msg>(r#"{"text":"привет","id":4,"at":99}"#).unwrap());\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(flatten)] на поле meta.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"text":"привет","id":4,"at":99}',
               'Msg { text: "привет", meta: Meta { id: 4, at: 99 } }']},
 {'id': 'r46-tagged-enum',
  'mode': 'rust',
  'title': 'Событие с внутренним тегом',
  'statement': 'Перечисление Event сериализуется с полем type в snake_case: Message { room: u32, '
               'text: String }, Join { user: String }, Leave { user: String }. Напечатайте JSON '
               'каждого варианта и разбор строки {"type":"join","user":"аня"}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"type":"message","room":1,"text":"привет"}\n'
               '{"type":"join","user":"аня"}\n'
               '{"type":"leave","user":"боря"}\n'
               'Join { user: "аня" }',
  'starter': 'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'enum Event {\n'
             '    Message { room: u32, text: String },\n'
             '    Join { user: String },\n'
             '    Leave { user: String },\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    for e in [Event::Message { room: 1, text: "привет".into() }, Event::Join { user: '
             '"аня".into() }, Event::Leave { user: "боря".into() }] {\n'
             '        println!("{}", serde_json::to_string(&e).unwrap());\n'
             '    }\n'
             '    println!("{:?}", '
             'serde_json::from_str::<Event>(r#"{"type":"join","user":"аня"}"#).unwrap());\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(tag = "type", rename_all = "snake_case")].',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"type":"message","room":1,"text":"привет"}',
               '{"type":"join","user":"аня"}',
               '{"type":"leave","user":"боря"}',
               'Join { user: "аня" }']},
 {'id': 'r46-untagged',
  'mode': 'rust',
  'title': 'Число или строка',
  'statement': 'Идентификатор может прийти как число или как строка. Перечисление Id { Num(u64), '
               'Text(String) } без тега принимает и то и другое. Напечатайте разбор значений 42, '
               '"abc", "7" и результат разбора true (ошибка).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '42 -> Num(42)\n'
               '"abc" -> Text("abc")\n'
               '"7" -> Text("7")\n'
               'true -> ошибка',
  'starter': 'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize, Debug)]\n'
             'enum Id {\n'
             '    Num(u64),\n'
             '    Text(String),\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    for s in ["42", "\\"abc\\"", "\\"7\\"", "true"] {\n'
             '        match serde_json::from_str::<Id>(s) {\n'
             '            Ok(id) => println!("{s} -> {id:?}"),\n'
             '            Err(_) => println!("{s} -> ошибка"),\n'
             '        }\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(untagged)] на перечислении.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['42 -> Num(42)', '"abc" -> Text("abc")', '"7" -> Text("7")', 'true -> ошибка']},
 {'id': 'r46-trim',
  'mode': 'rust',
  'title': 'Очистка строк при разборе',
  'statement': 'Поле text структуры Say должно очищаться от пробелов по краям уже при разборе '
               'JSON. Напишите функцию trimmed(deserializer) и подключите её через '
               'deserialize_with. Напечатайте разбор строки {"text":"   привет  "} в виде Debug.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Say { text: "привет" }',
  'starter': 'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize, Debug)]\n'
             'struct Say {\n'
             '    text: String,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{:?}", serde_json::from_str::<Say>(r#"{"text":"   привет  '
             '"}"#).unwrap());\n'
             '}\n',
  'driver': '',
  'hint': "fn trimmed<'de, D: Deserializer<'de>>(d: D) -> Result<String, D::Error> { let s = "
          'String::deserialize(d)?; Ok(s.trim().to_string()) }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Say { text: "привет" }']},
 {'id': 'r46-username',
  'mode': 'rust',
  'title': 'Имя пользователя как тип',
  'statement': 'Тип Username (от 3 до 16 символов, только латинские буквы и цифры) создаётся '
               'функцией Username::parse(&str) -> Result<Username, String> (ошибка — текст '
               'причины: «короткое», «длинное» или «недопустимый символ»). Подключите разбор из '
               'JSON через #[serde(try_from = "String")]. Напечатайте разбор строк "anna", "ab", '
               '"a_very_long_username_here", "a b".\n'
               '\n'
               'Ожидаемый вывод:\n'
               '"anna": Ok(Username("anna"))\n'
               '"ab": Err("короткое")\n'
               '"a_very_long_username_here": Err("длинное")\n'
               '"a b": Err("недопустимый символ")\n'
               'true\n'
               'true',
  'starter': 'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize, Debug)]\n'
             'struct Username(String);\n'
             '\n'
             'impl Username {\n'
             '    fn parse(s: &str) -> Result<Username, String> {\n'
             '        todo!()\n'
             '    }\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    for s in ["anna", "ab", "a_very_long_username_here", "a b"] {\n'
             '        println!("{s:?}: {:?}", Username::parse(s));\n'
             '    }\n'
             '    println!("{:?}", serde_json::from_str::<Username>("\\"boris\\"").is_ok());\n'
             '    println!("{:?}", serde_json::from_str::<Username>("\\"x\\"").is_err());\n'
             '}\n',
  'driver': '',
  'hint': 'impl TryFrom<String> for Username { type Error = String; ... } — serde вызывает его при '
          'разборе.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['"anna": Ok(Username("anna"))',
               '"ab": Err("короткое")',
               '"a_very_long_username_here": Err("длинное")',
               '"a b": Err("недопустимый символ")',
               'true',
               'true']},
 {'id': 'r46-json-macro',
  'mode': 'rust',
  'title': 'Сборка JSON макросом',
  'statement': 'Макрос serde_json::json! собирает значение: постройте ответ '
               '{"ok":true,"room":{"id":3,"name":"dev"},"members":["аня","боря"],"topic":null} и '
               'напечатайте его (ключи объектов выводятся в алфавитном порядке). Затем добавьте в '
               'объект поле count равное числу участников и напечатайте ещё раз.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"members":["аня","боря"],"ok":true,"room":{"id":3,"name":"dev"},"topic":null}\n'
               '{"count":2,"members":["аня","боря"],"ok":true,"room":{"id":3,"name":"dev"},"topic":null}',
  'starter': 'fn main() {\n    // ваш код\n}\n',
  'driver': '',
  'hint': 'let mut v = json!({..}); v["count"] = json!(2).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"members":["аня","боря"],"ok":true,"room":{"id":3,"name":"dev"},"topic":null}',
               '{"count":2,"members":["аня","боря"],"ok":true,"room":{"id":3,"name":"dev"},"topic":null}']},
 {'id': 'r46-value-nav',
  'mode': 'rust',
  'title': 'Разбор JSON без структуры',
  'statement': 'Разберите строку {"room":{"id":5,"tags":["a","b"],"owner":{"name":"аня"}},"n":3.5} '
               'в serde_json::Value и напечатайте: имя владельца (pointer), второй тег, id как '
               'u64, поле n как f64, и что на отсутствующем пути /room/zzz вернётся None.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'аня\n'
               'b\n'
               '5\n'
               '3.5\n'
               'None',
  'starter': 'fn main() {\n'
             '    let v: serde_json::Value = '
             'serde_json::from_str(r#"{"room":{"id":5,"tags":["a","b"],"owner":{"name":"аня"}},"n":3.5}"#).unwrap();\n'
             '    // ваш код\n'
             '    let _ = v;\n'
             '}\n',
  'driver': '',
  'hint': 'v.pointer("/room/owner/name").and_then(|x| x.as_str()).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['аня', 'b', '5', '3.5', 'None']},
 {'id': 'r46-double-option',
  'mode': 'rust',
  'title': 'Отсутствует или null',
  'statement': 'В запросе PATCH поле topic может: отсутствовать (не менять), быть null (очистить), '
               'быть строкой (записать). Структура Patch { topic: Option<Option<String>> } '
               'различает три случая: напишите функцию double_option для deserialize_with и '
               '#[serde(default)]. Напечатайте разбор {}, {"topic":null} и {"topic":"новая"}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{} -> Patch { topic: None }\n'
               '{"topic":null} -> Patch { topic: Some(None) }\n'
               '{"topic":"новая"} -> Patch { topic: Some(Some("новая")) }',
  'starter': 'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize, Debug)]\n'
             'struct Patch {\n'
             '    topic: Option<Option<String>>,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    for s in ["{}", r#"{"topic":null}"#, r#"{"topic":"новая"}"#] {\n'
             '        println!("{s} -> {:?}", serde_json::from_str::<Patch>(s).unwrap());\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': "fn double_option<'de, T, D>(d: D) -> Result<Option<Option<T>>, D::Error> { "
          'Option::<T>::deserialize(d).map(Some) } с #[serde(default, deserialize_with = ...)].',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{} -> Patch { topic: None }',
               '{"topic":null} -> Patch { topic: Some(None) }',
               '{"topic":"новая"} -> Patch { topic: Some(Some("новая")) }']},
 {'id': 'r46-u64-string',
  'mode': 'rust',
  'title': 'Большое число строкой',
  'statement': 'Идентификаторы u64 бывают больше 2^53 — JavaScript теряет точность. Структура Item '
               '{ id: u64 } должна сериализовать id строкой, а разбирать и строку, и число. '
               'Реализуйте модуль as_string с функциями serialize и deserialize (или любые две '
               'функции) и подключите через #[serde(with = "as_string")]. Напечатайте JSON для id '
               '= 9007199254740993 и разбор {"id":"18446744073709551615"}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"id":"9007199254740993"}\n'
               'Item { id: 18446744073709551615 }',
  'starter': 'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'struct Item {\n'
             '    id: u64,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{}", serde_json::to_string(&Item { id: 9007199254740993 }).unwrap());\n'
             '    println!("{:?}", '
             'serde_json::from_str::<Item>(r#"{"id":"18446744073709551615"}"#).unwrap());\n'
             '}\n',
  'driver': '',
  'hint': 'serialize: s.collect_str(&v); deserialize: '
          'String::deserialize(d)?.parse().map_err(D::Error::custom).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"id":"9007199254740993"}', 'Item { id: 18446744073709551615 }']},
 {'id': 'r46-lowercase-enum',
  'mode': 'rust',
  'title': 'Перечисление строкой',
  'statement': 'Роль Role { Admin, Member, Guest } сериализуется строками «admin», «member», '
               '«guest». Структура Who { name: String, role: Role }. Напечатайте JSON и разбор '
               '{"name":"аня","role":"guest"}; а также результат разбора роли "owner" (ошибка).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"name":"боря","role":"admin"}\n'
               'Who { name: "аня", role: Guest }\n'
               'true',
  'starter': 'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'enum Role {\n'
             '    Admin,\n'
             '    Member,\n'
             '    Guest,\n'
             '}\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'struct Who {\n'
             '    name: String,\n'
             '    role: Role,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{}", serde_json::to_string(&Who { name: "боря".into(), role: '
             'Role::Admin }).unwrap());\n'
             '    println!("{:?}", '
             'serde_json::from_str::<Who>(r#"{"name":"аня","role":"guest"}"#).unwrap());\n'
             '    println!("{}", serde_json::from_str::<Role>("\\"owner\\"").is_err());\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(rename_all = "lowercase")] на перечислении.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"name":"боря","role":"admin"}', 'Who { name: "аня", role: Guest }', 'true']},
 {'id': 'r46-page',
  'mode': 'rust',
  'title': 'Обобщённая страница ответа',
  'statement': 'Структура Page<T> { items: Vec<T>, next: Option<u64> } сериализуется как '
               '{"items":[..],"next":N}, а поле next при None пропускается. Напечатайте JSON '
               'страницы строк ["a","b"] с next = Some(10) и страницы чисел [1,2,3] без next.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"items":["a","b"],"next":10}\n'
               '{"items":[1,2,3]}',
  'starter': 'use serde::Serialize;\n'
             '\n'
             'struct Page<T> {\n'
             '    items: Vec<T>,\n'
             '    next: Option<u64>,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{}", serde_json::to_string(&Page { items: vec!["a", "b"], next: '
             'Some(10) }).unwrap());\n'
             '    println!("{}", serde_json::to_string(&Page { items: vec![1, 2, 3], next: None '
             '}).unwrap());\n'
             '}\n',
  'driver': '',
  'hint': '#[derive(Serialize)] struct Page<T> с ограничением T: Serialize (derive добавит само).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"items":["a","b"],"next":10}', '{"items":[1,2,3]}']},
 {'id': 'r46-app-error',
  'mode': 'rust',
  'title': 'Ошибки приложения: статус и код',
  'statement': 'Заготовка содержит перечисление AppError. Реализуйте методы status() -> StatusCode '
               '(NotFound → 404, Conflict → 409, Invalid → 422, Unauthorized → 401, Internal → '
               "500) и code() -> &'static str («not_found», «conflict», «invalid», «unauthorized», "
               '«internal»). main печатает пары для всех вариантов.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '404 not_found\n'
               '409 conflict\n'
               '422 invalid\n'
               '401 unauthorized\n'
               '500 internal',
  'starter': 'use axum::http::StatusCode;\n'
             '\n'
             '#[derive(Debug)]\n'
             'enum AppError {\n'
             '    NotFound,\n'
             '    Conflict(String),\n'
             '    Invalid(Vec<String>),\n'
             '    Unauthorized,\n'
             '    Internal(String),\n'
             '}\n'
             '\n'
             'impl AppError {\n'
             '    fn status(&self) -> StatusCode {\n'
             '        todo!()\n'
             '    }\n'
             "    fn code(&self) -> &'static str {\n"
             '        todo!()\n'
             '    }\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    let all = [AppError::NotFound, AppError::Conflict("x".into()), '
             'AppError::Invalid(vec![]), AppError::Unauthorized, AppError::Internal("y".into())];\n'
             '    for e in &all {\n'
             '        println!("{} {}", e.status().as_u16(), e.code());\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'match self { AppError::NotFound => .., ... }.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['404 not_found', '409 conflict', '422 invalid', '401 unauthorized', '500 internal']},
 {'id': 'r46-into-response',
  'mode': 'rust',
  'title': 'AppError как ответ',
  'statement': 'Реализуйте IntoResponse для AppError (заготовка уже содержит методы status() и '
               'code()): статус по варианту, тело — JSON {"error":{"code":..., "message":...}}; '
               'сообщения: NotFound — «не найдено», Conflict(m) — m, Invalid — «данные не годятся» '
               '(дополнительно в error добавляется массив fields), Unauthorized — «нужна '
               'авторизация», Internal — «внутренняя ошибка». Обработчики GET /e/{kind} возвращают '
               'нужную ошибку (kind: nf, conflict, invalid, auth, boom).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '404 {"error":{"code":"not_found","message":"не найдено"}}\n'
               '409 {"error":{"code":"conflict","message":"имя занято"}}\n'
               '422 '
               '{"error":{"code":"invalid","fields":[{"name":"name","why":"короткое"}],"message":"данные '
               'не годятся"}}\n'
               '401 {"error":{"code":"unauthorized","message":"нужна авторизация"}}\n'
               '500 {"error":{"code":"internal","message":"внутренняя ошибка"}}',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use axum::response::{IntoResponse, Response};\n'
             'use axum::Json;\n'
             'use serde::Serialize;\n'
             '\n'
             '#[derive(Serialize, Clone, Debug, PartialEq)]\n'
             'struct FieldError {\n'
             '    name: String,\n'
             '    why: String,\n'
             '}\n'
             '\n'
             '#[derive(Debug)]\n'
             'enum AppError {\n'
             '    NotFound,\n'
             '    Conflict(String),\n'
             '    Invalid(Vec<FieldError>),\n'
             '    Unauthorized,\n'
             '    Internal(String),\n'
             '}\n'
             '\n'
             'impl AppError {\n'
             '    fn status(&self) -> StatusCode {\n'
             '        match self {\n'
             '            AppError::NotFound => StatusCode::NOT_FOUND,\n'
             '            AppError::Conflict(_) => StatusCode::CONFLICT,\n'
             '            AppError::Invalid(_) => StatusCode::UNPROCESSABLE_ENTITY,\n'
             '            AppError::Unauthorized => StatusCode::UNAUTHORIZED,\n'
             '            AppError::Internal(_) => StatusCode::INTERNAL_SERVER_ERROR,\n'
             '        }\n'
             '    }\n'
             "    fn code(&self) -> &'static str {\n"
             '        match self {\n'
             '            AppError::NotFound => "not_found",\n'
             '            AppError::Conflict(_) => "conflict",\n'
             '            AppError::Invalid(_) => "invalid",\n'
             '            AppError::Unauthorized => "unauthorized",\n'
             '            AppError::Internal(_) => "internal",\n'
             '        }\n'
             '    }\n'
             '}\n'
             '\n'
             'use axum::extract::Path;\n'
             'use axum::routing::get;\n'
             '\n'
             "async fn boom(Path(kind): Path<String>) -> Result<&'static str, AppError> {\n"
             '    Err(match kind.as_str() {\n'
             '        "nf" => AppError::NotFound,\n'
             '        "conflict" => AppError::Conflict("имя занято".into()),\n'
             '        "invalid" => AppError::Invalid(vec![FieldError { name: "name".into(), why: '
             '"короткое".into() }]),\n'
             '        "auth" => AppError::Unauthorized,\n'
             '        _ => AppError::Internal("sql: boom at db.rs:12".into()),\n'
             '    })\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/e/{kind}", get(boom))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for k in ["nf", "conflict", "invalid", "auth", "boom"] {\n'
             '        let (s, b) = call(&app, "GET", &format!("/e/{k}"), "").await;\n'
             '        println!("{} {b}", s.as_u16());\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': '(status, Json(json!({ "error": ... }))).into_response(); fields — '
          'serde_json::to_value(fields).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['404 {"error":{"code":"not_found","message":"не найдено"}}',
               '409 {"error":{"code":"conflict","message":"имя занято"}}',
               '422 '
               '{"error":{"code":"invalid","fields":[{"name":"name","why":"короткое"}],"message":"данные '
               'не годятся"}}',
               '401 {"error":{"code":"unauthorized","message":"нужна авторизация"}}',
               '500 {"error":{"code":"internal","message":"внутренняя ошибка"}}']},
 {'id': 'r46-from-parse',
  'mode': 'rust',
  'title': 'Оператор ? и From',
  'statement': 'Реализуйте From<std::num::ParseIntError> для AppError (вариант Invalid с одним '
               'текстом) и обработчик GET /double/{n} с Path<String>: разбирает n как i64 '
               'оператором ? и отвечает удвоенным числом; неверный текст даёт 422 с телом '
               '«invalid: не число». Заготовка содержит AppError с IntoResponse '
               '(Invalid(String)).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(200, "42")\n'
               '(200, "-8")\n'
               '(422, "invalid: не число")',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use axum::extract::Path;\n'
             'use axum::response::{IntoResponse, Response};\n'
             'use axum::routing::get;\n'
             '\n'
             'enum AppError {\n'
             '    Invalid(String),\n'
             '}\n'
             '\n'
             'impl IntoResponse for AppError {\n'
             '    fn into_response(self) -> Response {\n'
             '        match self {\n'
             '            AppError::Invalid(m) => (StatusCode::UNPROCESSABLE_ENTITY, '
             'format!("invalid: {m}")).into_response(),\n'
             '        }\n'
             '    }\n'
             '}\n'
             '\n'
             'async fn double(Path(n): Path<String>) -> Result<String, AppError> {\n'
             '    let n: i64 = n.parse().unwrap();\n'
             '    Ok((n * 2).to_string())\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/double/{n}", get(double))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for n in ["21", "-4", "abc"] {\n'
             '        println!("{:?}", call(&app, "GET", &format!("/double/{n}"), "").await);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'impl From<ParseIntError> for AppError { fn from(_: ParseIntError) -> Self { '
          'AppError::Invalid(..) } }.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(200, "42")', '(200, "-8")', '(422, "invalid: не число")']},
 {'id': 'r46-validate-fields',
  'mode': 'rust',
  'title': 'Валидация с перечнем полей',
  'statement': 'POST /users принимает JSON {"name":..., "password":...}. Правила: name — от 3 до '
               '16 символов, password — не короче 8 символов. Если нарушено любое правило, ответ — '
               '422 и JSON {"error":{"code":"invalid","fields":[{"name":..,"why":..}]}} со ВСЕМИ '
               'нарушениями (why: «короткое имя», «длинное имя», «короткий пароль»); успех — 201 и '
               '«создан NAME». Порядок полей: name, затем password.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '201 создан anna\n'
               '422 {"error":{"code":"invalid","fields":[{"name":"name","why":"короткое '
               'имя"},{"name":"password","why":"короткий пароль"}]}}\n'
               '422 {"error":{"code":"invalid","fields":[{"name":"name","why":"длинное имя"}]}}\n'
               '422 {"error":{"code":"invalid","fields":[{"name":"password","why":"короткий '
               'пароль"}]}}',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use axum::response::{IntoResponse, Response};\n'
             'use axum::Json;\n'
             'use serde::Serialize;\n'
             '\n'
             '#[derive(Serialize, Clone, Debug, PartialEq)]\n'
             'struct FieldError {\n'
             '    name: String,\n'
             '    why: String,\n'
             '}\n'
             '\n'
             '#[derive(Debug)]\n'
             'enum AppError {\n'
             '    NotFound,\n'
             '    Conflict(String),\n'
             '    Invalid(Vec<FieldError>),\n'
             '    Unauthorized,\n'
             '    Internal(String),\n'
             '}\n'
             '\n'
             'use axum::routing::post;\n'
             '\n'
             '#[derive(serde::Deserialize)]\n'
             'struct NewUser {\n'
             '    name: String,\n'
             '    password: String,\n'
             '}\n'
             '\n'
             'async fn create(Json(u): Json<NewUser>) -> Result<(StatusCode, String), AppError> {\n'
             '    Ok((StatusCode::CREATED, format!("создан {}", u.name)))\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/users", post(create))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for body in [r#"{"name":"anna","password":"longenough"}"#, '
             'r#"{"name":"ab","password":"short"}"#, '
             'r#"{"name":"a_very_long_name_indeed","password":"12345678"}"#, '
             'r#"{"name":"bob","password":"1234567"}"#] {\n'
             '        let (s, b) = call(&app, "POST", "/users", body).await;\n'
             '        println!("{} {b}", s.as_u16());\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Соберите Vec<FieldError>; если не пуст — верните Err(AppError::Invalid(..)).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['201 создан anna',
               '422 {"error":{"code":"invalid","fields":[{"name":"name","why":"короткое '
               'имя"},{"name":"password","why":"короткий пароль"}]}}',
               '422 {"error":{"code":"invalid","fields":[{"name":"name","why":"длинное имя"}]}}',
               '422 {"error":{"code":"invalid","fields":[{"name":"password","why":"короткий '
               'пароль"}]}}']},
 {'id': 'r46-api-json',
  'mode': 'rust',
  'title': 'Свой экстрактор ApiJson',
  'statement': 'Заготовка содержит AppError (BadRequest(String) → 400 code bad_request, '
               'Unsupported → 415 code unsupported, Invalid(String) → 422 code invalid; '
               'IntoResponse выдаёт {"error":{"code":..,"message":..}}). Реализуйте экстрактор '
               'ApiJson<T>: FromRequest, который вызывает Json<T>, а JsonRejection превращает в '
               'AppError по статусу отказа (400, 415, иначе 422), с сообщением '
               'rejection.body_text(). Обработчик POST /n принимает ApiJson<Num> с полем n: i64 и '
               'отвечает числом. Проверьте корректное тело, не-JSON, неверный тип и запрос без '
               'заголовка content-type.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '200 5\n'
               '400 bad_request\n'
               '422 invalid\n'
               '415 unsupported',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use axum::extract::FromRequest;\n'
             'use axum::response::{IntoResponse, Response};\n'
             'use axum::routing::post;\n'
             'use axum::Json;\n'
             'use serde::de::DeserializeOwned;\n'
             '\n'
             'enum AppError {\n'
             '    BadRequest(String),\n'
             '    Unsupported(String),\n'
             '    Invalid(String),\n'
             '}\n'
             '\n'
             'impl IntoResponse for AppError {\n'
             '    fn into_response(self) -> Response {\n'
             '        let (s, code, m) = match self {\n'
             '            AppError::BadRequest(m) => (StatusCode::BAD_REQUEST, "bad_request", m),\n'
             '            AppError::Unsupported(m) => (StatusCode::UNSUPPORTED_MEDIA_TYPE, '
             '"unsupported", m),\n'
             '            AppError::Invalid(m) => (StatusCode::UNPROCESSABLE_ENTITY, "invalid", '
             'm),\n'
             '        };\n'
             '        (s, Json(serde_json::json!({ "error": { "code": code, "message": m } '
             '}))).into_response()\n'
             '    }\n'
             '}\n'
             '\n'
             'struct ApiJson<T>(T);\n'
             '\n'
             '// TODO: impl FromRequest<S> for ApiJson<T>\n'
             '\n'
             '#[derive(serde::Deserialize)]\n'
             'struct Num {\n'
             '    n: i64,\n'
             '}\n'
             '\n'
             'async fn handler(ApiJson(v): ApiJson<Num>) -> String {\n'
             '    v.n.to_string()\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/n", post(handler))\n'
             '}\n'
             '\n'
             'async fn code_of(app: &Router, content_type: Option<&str>, body: &str) -> String {\n'
             '    let mut b = Request::post("/n");\n'
             '    if let Some(ct) = content_type {\n'
             '        b = b.header("content-type", ct);\n'
             '    }\n'
             '    let res = '
             'app.clone().oneshot(b.body(Body::from(body.to_string())).unwrap()).await.unwrap();\n'
             '    let s = res.status().as_u16();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    let v: serde_json::Value = '
             'serde_json::from_slice(&bytes).unwrap_or(serde_json::Value::Null);\n'
             '    format!("{s} {}", v.pointer("/error/code").and_then(|c| '
             'c.as_str()).unwrap_or(&String::from_utf8_lossy(&bytes)))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", code_of(&app, Some("application/json"), r#"{"n": 5}"#).await);\n'
             '    println!("{}", code_of(&app, Some("application/json"), "not json").await);\n'
             '    println!("{}", code_of(&app, Some("application/json"), r#"{"n": "x"}"#).await);\n'
             '    println!("{}", code_of(&app, None, r#"{"n": 5}"#).await);\n'
             '}\n',
  'driver': '',
  'hint': 'impl<S, T> FromRequest<S> for ApiJson<T> where T: DeserializeOwned, S: Send + Sync { '
          'type Rejection = AppError; async fn from_request(req: Request<Body>, state: &S) -> '
          'Result<Self, AppError> { ... } }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['200 5', '400 bad_request', '422 invalid', '415 unsupported']},
 {'id': 'r46-json-fallback',
  'mode': 'rust',
  'title': '404 и 405 в формате JSON',
  'statement': 'Роутер с маршрутом GET /ping («pong») должен отвечать на неизвестные пути 404 с '
               'телом {"error":{"code":"not_found"}} и на неверный метод — 405 с телом '
               '{"error":{"code":"method_not_allowed"}}. Используйте .fallback(..) и '
               '.method_not_allowed_fallback(..). Напечатайте ответы на GET /ping, GET /x, POST '
               '/ping.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(200, "pong")\n'
               '(404, "{\\"error\\":{\\"code\\":\\"not_found\\"}}")\n'
               '(405, "{\\"error\\":{\\"code\\":\\"method_not_allowed\\"}}")',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{:?}", call(&app, "GET", "/ping", "").await);\n'
             '    println!("{:?}", call(&app, "GET", "/x", "").await);\n'
             '    println!("{:?}", call(&app, "POST", "/ping", "").await);\n'
             '}\n',
  'driver': '',
  'hint': 'Router::new().route(..).fallback(h404).method_not_allowed_fallback(h405).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(200, "pong")',
               '(404, "{\\"error\\":{\\"code\\":\\"not_found\\"}}")',
               '(405, "{\\"error\\":{\\"code\\":\\"method_not_allowed\\"}}")']},
 {'id': 'r46-hide-internal',
  'mode': 'rust',
  'title': 'Внутренние детали — в журнал',
  'statement': 'Обработчик GET /boom завершается ошибкой Internal("sql: syntax error near \'FORM\' '
               'at db.rs:12"). Клиент должен получить 500 и тело «внутренняя ошибка», а '
               'подробности — попасть в журнал (Arc<Mutex<Vec<String>>> из состояния). Напишите '
               'обработчик так, чтобы он сам записывал деталь в журнал и возвращал общую ошибку; '
               'main печатает ответ клиенту и журнал.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(500, "внутренняя ошибка")\n'
               '["sql: syntax error near \'FORM\' at db.rs:12"]',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use std::sync::{Arc, Mutex};\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let log = Arc::new(Mutex::new(Vec::new()));\n'
             '    let app = app(log.clone());\n'
             '    println!("{:?}", call(&app, "GET", "/boom", "").await);\n'
             '    println!("{:?}", log.lock().unwrap());\n'
             '}\n',
  'driver': '',
  'hint': 'Запишите деталь в журнал перед возвратом (StatusCode::INTERNAL_SERVER_ERROR, '
          '"внутренняя ошибка").',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(500, "внутренняя ошибка")', '["sql: syntax error near \'FORM\' at db.rs:12"]']},
 {'id': 'r46-dto',
  'mode': 'rust',
  'title': 'Запрос, строка и ответ',
  'statement': 'Есть три типа: CreateRoom { name } (запрос), RoomRow { id, name, secret_key } '
               '(строка базы), RoomOut { id, name } (ответ). Реализуйте From<RoomRow> для RoomOut '
               'и обработчик POST /rooms: разбирает CreateRoom, «сохраняет» строку (id = число '
               'символов имени, secret_key = "k-" + имя) и отвечает RoomOut в JSON со статусом '
               '201. Секретный ключ в ответ попадать не должен.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(201, "{\\"id\\":5,\\"name\\":\\"общая\\"}")',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use axum::routing::post;\n'
             'use axum::Json;\n'
             'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Deserialize)]\n'
             'struct CreateRoom {\n'
             '    name: String,\n'
             '}\n'
             'struct RoomRow {\n'
             '    id: u32,\n'
             '    name: String,\n'
             '    secret_key: String,\n'
             '}\n'
             '#[derive(Serialize)]\n'
             'struct RoomOut {\n'
             '    id: u32,\n'
             '    name: String,\n'
             '}\n'
             '\n'
             'async fn create(Json(req): Json<CreateRoom>) -> (StatusCode, Json<RoomOut>) {\n'
             '    let row = RoomRow { id: req.name.chars().count() as u32, name: req.name.clone(), '
             'secret_key: format!("k-{}", req.name) };\n'
             '    let _ = row.secret_key;\n'
             '    (StatusCode::CREATED, Json(RoomOut { id: 0, name: String::new() }))\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/rooms", post(create))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{:?}", call(&app, "POST", "/rooms", r#"{"name":"общая"}"#).await);\n'
             '}\n',
  'driver': '',
  'hint': 'Json((StatusCode::CREATED, Json(RoomOut::from(row)))) — кортеж (StatusCode, Json<T>).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(201, "{\\"id\\":5,\\"name\\":\\"общая\\"}")']},
 {'id': 'r46-error-chain',
  'mode': 'rust',
  'title': 'Цепочка причин ошибки',
  'statement': 'Реализуйте для AppError (Display и std::error::Error) цепочку причин: '
               'AppError::Db(DbError) — source() возвращает внутреннюю ошибку; AppError::NotFound '
               '— без причины. Display: «база недоступна» для Db и «не найдено» для NotFound. '
               'DbError реализует Display («соединение разорвано») и Error. Функция chain(&dyn '
               'Error) -> Vec<String> собирает тексты всей цепочки от внешней ошибки к самой '
               'глубокой.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '["база недоступна", "соединение разорвано"]\n'
               '["не найдено"]',
  'starter': 'use std::error::Error;\n'
             'use std::fmt;\n'
             '\n'
             '#[derive(Debug)]\n'
             'struct DbError;\n'
             '\n'
             '#[derive(Debug)]\n'
             'enum AppError {\n'
             '    NotFound,\n'
             '    Db(DbError),\n'
             '}\n'
             '\n'
             'fn chain(e: &dyn Error) -> Vec<String> {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{:?}", chain(&AppError::Db(DbError)));\n'
             '    println!("{:?}", chain(&AppError::NotFound));\n'
             '}\n',
  'driver': '',
  'hint': "fn source(&self) -> Option<&(dyn Error + 'static)>; цикл while let Some(e) = cur { ...; "
          'cur = e.source(); }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['["база недоступна", "соединение разорвано"]', '["не найдено"]']},
 {'id': 'r46-rename-keyword',
  'mode': 'rust',
  'title': 'Поле с зарезервированным именем',
  'statement': 'В JSON поле называется type, но в Rust это ключевое слово. Структура Shape { kind: '
               'String, sides: u32 } должна сериализоваться как {"type":"..","sides":N} и так же '
               'разбираться. Напечатайте JSON и разбор {"type":"квадрат","sides":4}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"type":"треугольник","sides":3}\n'
               'Shape { kind: "квадрат", sides: 4 }',
  'starter': 'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'struct Shape {\n'
             '    kind: String,\n'
             '    sides: u32,\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    println!("{}", serde_json::to_string(&Shape { kind: "треугольник".into(), sides: '
             '3 }).unwrap());\n'
             '    println!("{:?}", '
             'serde_json::from_str::<Shape>(r#"{"type":"квадрат","sides":4}"#).unwrap());\n'
             '}\n',
  'driver': '',
  'hint': '#[serde(rename = "type")] на поле kind.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"type":"треугольник","sides":3}', 'Shape { kind: "квадрат", sides: 4 }']},
 {'id': 'r46-custom-error',
  'mode': 'rust',
  'title': 'Своё сообщение при разборе',
  'statement': 'Цвет Color(u8, u8, u8) разбирается из строки «#rrggbb» (hex). Реализуйте '
               "Deserialize вручную (impl<'de> Deserialize<'de>): строка должна начинаться с «#» и "
               'содержать ровно 6 hex-символов, иначе ошибка serde::de::Error::custom с текстом '
               '«неверный цвет: СТРОКА». Напечатайте разбор "#ff8000", "#00ff7f", "ff8000", '
               '"#12".\n'
               '\n'
               'Ожидаемый вывод:\n'
               '"#ff8000": Color(255, 128, 0)\n'
               '"#00ff7f": Color(0, 255, 127)\n'
               '"ff8000": неверный цвет: ff8000\n'
               '"#12": неверный цвет: #12',
  'starter': 'use serde::{Deserialize, Deserializer};\n'
             '\n'
             '#[derive(Debug)]\n'
             'struct Color(u8, u8, u8);\n'
             '\n'
             "impl<'de> Deserialize<'de> for Color {\n"
             "    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Color, D::Error> {\n"
             '        todo!()\n'
             '    }\n'
             '}\n'
             '\n'
             'fn main() {\n'
             '    for s in ["\\"#ff8000\\"", "\\"#00ff7f\\"", "\\"ff8000\\"", "\\"#12\\""] {\n'
             '        match serde_json::from_str::<Color>(s) {\n'
             '            Ok(c) => println!("{s}: {c:?}"),\n'
             '            Err(e) => println!("{s}: {}", e.to_string().split(" at '
             'line").next().unwrap()),\n'
             '        }\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'let s = String::deserialize(d)?; u8::from_str_radix(&s[1..3], 16) для каждого канала.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['"#ff8000": Color(255, 128, 0)',
               '"#00ff7f": Color(0, 255, 127)',
               '"ff8000": неверный цвет: ff8000',
               '"#12": неверный цвет: #12']},
 {'id': 'r46-fix-derive',
  'mode': 'rust',
  'title': 'Исправьте: нет derive',
  'statement': 'Код не компилируется: структура Out не умеет сериализоваться, а Json<Out> требует '
               'этого. Добавьте нужный derive, чтобы GET /out отвечал {"id":1,"name":"общая"}.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(200, "{\\"id\\":1,\\"name\\":\\"общая\\"}")',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use axum::routing::get;\n'
             'use axum::Json;\n'
             '\n'
             'struct Out {\n'
             '    id: u32,\n'
             '    name: String,\n'
             '}\n'
             '\n'
             'async fn out() -> Json<Out> {\n'
             '    Json(Out { id: 1, name: "общая".into() })\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/out", get(out))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{:?}", call(&app, "GET", "/out", "").await);\n'
             '}\n',
  'driver': '',
  'hint': '#[derive(serde::Serialize)].',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(200, "{\\"id\\":1,\\"name\\":\\"общая\\"}")']},
 {'id': 'r46-cursor',
  'mode': 'rust',
  'title': 'Курсор в строке запроса',
  'statement': 'GET /msgs?cursor=c123 принимает необязательный курсор формата «c» + число. Тип '
               'Cursor(u64) разбирается из строки через #[serde(try_from = "String")] (ошибка: '
               '«неверный курсор»). Обработчик отвечает «после N» (или «с начала», если курсора '
               'нет). Для неверного курсора axum вернёт 400. Напечатайте ответы для /msgs, '
               '/msgs?cursor=c42, /msgs?cursor=x1 и /msgs?cursor=c.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '/msgs -> 200 с начала\n'
               '/msgs?cursor=c42 -> 200 после 42\n'
               '/msgs?cursor=x1 -> 400\n'
               '/msgs?cursor=c -> 400',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use axum::extract::Query;\n'
             'use axum::routing::get;\n'
             'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize, Debug)]\n'
             'struct Cursor(u64);\n'
             '\n'
             '#[derive(Deserialize)]\n'
             'struct Params {\n'
             '    cursor: Option<Cursor>,\n'
             '}\n'
             '\n'
             'async fn msgs(Query(p): Query<Params>) -> String {\n'
             '    match p.cursor {\n'
             '        Some(c) => format!("после {}", c.0),\n'
             '        None => "с начала".into(),\n'
             '    }\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/msgs", get(msgs))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for uri in ["/msgs", "/msgs?cursor=c42", "/msgs?cursor=x1", "/msgs?cursor=c"] {\n'
             '        let (s, b) = call(&app, "GET", uri, "").await;\n'
             '        println!("{uri} -> {} {}", s.as_u16(), if s.is_success() { b } else { '
             'String::new() });\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': "impl TryFrom<String> for Cursor: strip_prefix('c') и parse::<u64>().",
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['/msgs -> 200 с начала',
               '/msgs?cursor=c42 -> 200 после 42',
               '/msgs?cursor=x1 -> 400',
               '/msgs?cursor=c -> 400']}]}
