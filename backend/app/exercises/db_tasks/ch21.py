"""Задачи книги «Базы данных»: глава 21."""

TASKS: dict[int, list[dict]] = {21: [{'id': 'd5-json-extract',
  'mode': 'sql',
  'title': 'JSON в SQL: достать поле',
  'statement': "В таблице events(id, payload) payload — JSON. Выведите user и amount для событий типа 'buy' "
               '(колонки: user, amount), по возрастанию id.',
  'starter': '-- user и amount покупок\nSELECT\n',
  'setup': 'CREATE TABLE events (id INTEGER PRIMARY KEY, payload TEXT NOT NULL);\n'
           'INSERT INTO events VALUES '
           '(1,\'{"type":"buy","user":"anna","amount":120,"tags":["promo","mobile"]}\'),(2,\'{"type":"view","user":"boris","tags":["mobile"]}\'),(3,\'{"type":"buy","user":"anna","amount":80,"tags":["web","promo"]}\'),(4,\'{"type":"buy","user":"vera","amount":300,"tags":[]}\'),(5,\'{"type":"view","user":"anna","tags":["web"]}\');\n',
  'expected': [['anna', 120], ['anna', 80], ['vera', 300]],
  'expected_cols': ['user', 'amount'],
  'hint': "Оператор ->> достаёт значение по пути: payload ->> '$.user'; или json_extract(payload, '$.user').",
  'ordered': True},
 {'id': 'd5-json-each',
  'mode': 'sql',
  'title': 'JSON-массив в строки',
  'statement': 'Посчитайте, сколько раз встречается каждый тег во всех событиях (массив tags в payload). '
               'Колонки: tag, n; сначала самые частые, при равенстве — по алфавиту.',
  'starter': '-- теги и их частоты\nSELECT\n',
  'setup': 'CREATE TABLE events (id INTEGER PRIMARY KEY, payload TEXT NOT NULL);\n'
           'INSERT INTO events VALUES '
           '(1,\'{"type":"buy","user":"anna","amount":120,"tags":["promo","mobile"]}\'),(2,\'{"type":"view","user":"boris","tags":["mobile"]}\'),(3,\'{"type":"buy","user":"anna","amount":80,"tags":["web","promo"]}\'),(4,\'{"type":"buy","user":"vera","amount":300,"tags":[]}\'),(5,\'{"type":"view","user":"anna","tags":["web"]}\');\n',
  'expected': [['mobile', 2], ['promo', 2], ['web', 2]],
  'expected_cols': ['tag', 'n'],
  'hint': "json_each(payload, '$.tags') разворачивает массив в строки; значение — столбец value.",
  'ordered': True},
 {'id': 'd5-json-index',
  'mode': 'sql',
  'title': 'Индекс по полю JSON',
  'statement': "Запрос WHERE payload ->> '$.user' = 'anna' просматривает таблицу. Создайте индекс на "
               'выражении так, чтобы он стал поиском по индексу.',
  'starter': '-- индекс по полю user внутри JSON\nCREATE INDEX\n',
  'setup': 'CREATE TABLE events (id INTEGER PRIMARY KEY, payload TEXT NOT NULL);\n'
           'INSERT INTO events VALUES '
           '(1,\'{"type":"buy","user":"anna","amount":120,"tags":["promo","mobile"]}\'),(2,\'{"type":"view","user":"boris","tags":["mobile"]}\'),(3,\'{"type":"buy","user":"anna","amount":80,"tags":["web","promo"]}\'),(4,\'{"type":"buy","user":"vera","amount":300,"tags":[]}\'),(5,\'{"type":"view","user":"anna","tags":["web"]}\');\n'
           'INSERT INTO events VALUES (6,\'{"type":"view","user":"u6","tags":[]}\');\n'
           'INSERT INTO events VALUES (7,\'{"type":"view","user":"u7","tags":[]}\');\n'
           'INSERT INTO events VALUES (8,\'{"type":"view","user":"u8","tags":[]}\');\n'
           'INSERT INTO events VALUES (9,\'{"type":"view","user":"u9","tags":[]}\');\n'
           'INSERT INTO events VALUES (10,\'{"type":"view","user":"u10","tags":[]}\');\n'
           'INSERT INTO events VALUES (11,\'{"type":"view","user":"u11","tags":[]}\');\n'
           'INSERT INTO events VALUES (12,\'{"type":"view","user":"u12","tags":[]}\');\n'
           'INSERT INTO events VALUES (13,\'{"type":"view","user":"u13","tags":[]}\');\n'
           'INSERT INTO events VALUES (14,\'{"type":"view","user":"u14","tags":[]}\');\n'
           'INSERT INTO events VALUES (15,\'{"type":"view","user":"u15","tags":[]}\');\n'
           'INSERT INTO events VALUES (16,\'{"type":"view","user":"u16","tags":[]}\');\n'
           'INSERT INTO events VALUES (17,\'{"type":"view","user":"u17","tags":[]}\');\n'
           'INSERT INTO events VALUES (18,\'{"type":"view","user":"u18","tags":[]}\');\n'
           'INSERT INTO events VALUES (19,\'{"type":"view","user":"u19","tags":[]}\');\n'
           'INSERT INTO events VALUES (20,\'{"type":"view","user":"u20","tags":[]}\');\n'
           'INSERT INTO events VALUES (21,\'{"type":"view","user":"u21","tags":[]}\');\n'
           'INSERT INTO events VALUES (22,\'{"type":"view","user":"u22","tags":[]}\');\n'
           'INSERT INTO events VALUES (23,\'{"type":"view","user":"u23","tags":[]}\');\n'
           'INSERT INTO events VALUES (24,\'{"type":"view","user":"u24","tags":[]}\');\n'
           'INSERT INTO events VALUES (25,\'{"type":"view","user":"u25","tags":[]}\');\n'
           'INSERT INTO events VALUES (26,\'{"type":"view","user":"u26","tags":[]}\');\n'
           'INSERT INTO events VALUES (27,\'{"type":"view","user":"u27","tags":[]}\');\n'
           'INSERT INTO events VALUES (28,\'{"type":"view","user":"u28","tags":[]}\');\n'
           'INSERT INTO events VALUES (29,\'{"type":"view","user":"u29","tags":[]}\');\n'
           'INSERT INTO events VALUES (30,\'{"type":"view","user":"u30","tags":[]}\');\n'
           'INSERT INTO events VALUES (31,\'{"type":"view","user":"u31","tags":[]}\');\n'
           'INSERT INTO events VALUES (32,\'{"type":"view","user":"u32","tags":[]}\');\n'
           'INSERT INTO events VALUES (33,\'{"type":"view","user":"u33","tags":[]}\');\n'
           'INSERT INTO events VALUES (34,\'{"type":"view","user":"u34","tags":[]}\');\n'
           'INSERT INTO events VALUES (35,\'{"type":"view","user":"u35","tags":[]}\');\n'
           'INSERT INTO events VALUES (36,\'{"type":"view","user":"u36","tags":[]}\');\n'
           'INSERT INTO events VALUES (37,\'{"type":"view","user":"u37","tags":[]}\');\n'
           'INSERT INTO events VALUES (38,\'{"type":"view","user":"u38","tags":[]}\');\n'
           'INSERT INTO events VALUES (39,\'{"type":"view","user":"u39","tags":[]}\');\n'
           'INSERT INTO events VALUES (40,\'{"type":"view","user":"u0","tags":[]}\');\n'
           'INSERT INTO events VALUES (41,\'{"type":"view","user":"u1","tags":[]}\');\n'
           'INSERT INTO events VALUES (42,\'{"type":"view","user":"u2","tags":[]}\');\n'
           'INSERT INTO events VALUES (43,\'{"type":"view","user":"u3","tags":[]}\');\n'
           'INSERT INTO events VALUES (44,\'{"type":"view","user":"u4","tags":[]}\');\n'
           'INSERT INTO events VALUES (45,\'{"type":"view","user":"u5","tags":[]}\');\n'
           'INSERT INTO events VALUES (46,\'{"type":"view","user":"u6","tags":[]}\');\n'
           'INSERT INTO events VALUES (47,\'{"type":"view","user":"u7","tags":[]}\');\n'
           'INSERT INTO events VALUES (48,\'{"type":"view","user":"u8","tags":[]}\');\n'
           'INSERT INTO events VALUES (49,\'{"type":"view","user":"u9","tags":[]}\');\n'
           'INSERT INTO events VALUES (50,\'{"type":"view","user":"u10","tags":[]}\');\n'
           'INSERT INTO events VALUES (51,\'{"type":"view","user":"u11","tags":[]}\');\n'
           'INSERT INTO events VALUES (52,\'{"type":"view","user":"u12","tags":[]}\');\n'
           'INSERT INTO events VALUES (53,\'{"type":"view","user":"u13","tags":[]}\');\n'
           'INSERT INTO events VALUES (54,\'{"type":"view","user":"u14","tags":[]}\');\n'
           'INSERT INTO events VALUES (55,\'{"type":"view","user":"u15","tags":[]}\');\n'
           'INSERT INTO events VALUES (56,\'{"type":"view","user":"u16","tags":[]}\');\n'
           'INSERT INTO events VALUES (57,\'{"type":"view","user":"u17","tags":[]}\');\n'
           'INSERT INTO events VALUES (58,\'{"type":"view","user":"u18","tags":[]}\');\n'
           'INSERT INTO events VALUES (59,\'{"type":"view","user":"u19","tags":[]}\');\n'
           'INSERT INTO events VALUES (60,\'{"type":"view","user":"u20","tags":[]}\');\n'
           'INSERT INTO events VALUES (61,\'{"type":"view","user":"u21","tags":[]}\');\n'
           'INSERT INTO events VALUES (62,\'{"type":"view","user":"u22","tags":[]}\');\n'
           'INSERT INTO events VALUES (63,\'{"type":"view","user":"u23","tags":[]}\');\n'
           'INSERT INTO events VALUES (64,\'{"type":"view","user":"u24","tags":[]}\');\n'
           'INSERT INTO events VALUES (65,\'{"type":"view","user":"u25","tags":[]}\');\n'
           'INSERT INTO events VALUES (66,\'{"type":"view","user":"u26","tags":[]}\');\n'
           'INSERT INTO events VALUES (67,\'{"type":"view","user":"u27","tags":[]}\');\n'
           'INSERT INTO events VALUES (68,\'{"type":"view","user":"u28","tags":[]}\');\n'
           'INSERT INTO events VALUES (69,\'{"type":"view","user":"u29","tags":[]}\');\n'
           'INSERT INTO events VALUES (70,\'{"type":"view","user":"u30","tags":[]}\');\n'
           'INSERT INTO events VALUES (71,\'{"type":"view","user":"u31","tags":[]}\');\n'
           'INSERT INTO events VALUES (72,\'{"type":"view","user":"u32","tags":[]}\');\n'
           'INSERT INTO events VALUES (73,\'{"type":"view","user":"u33","tags":[]}\');\n'
           'INSERT INTO events VALUES (74,\'{"type":"view","user":"u34","tags":[]}\');\n'
           'INSERT INTO events VALUES (75,\'{"type":"view","user":"u35","tags":[]}\');\n'
           'INSERT INTO events VALUES (76,\'{"type":"view","user":"u36","tags":[]}\');\n'
           'INSERT INTO events VALUES (77,\'{"type":"view","user":"u37","tags":[]}\');\n'
           'INSERT INTO events VALUES (78,\'{"type":"view","user":"u38","tags":[]}\');\n'
           'INSERT INTO events VALUES (79,\'{"type":"view","user":"u39","tags":[]}\');\n'
           'INSERT INTO events VALUES (80,\'{"type":"view","user":"u0","tags":[]}\');\n'
           'INSERT INTO events VALUES (81,\'{"type":"view","user":"u1","tags":[]}\');\n'
           'INSERT INTO events VALUES (82,\'{"type":"view","user":"u2","tags":[]}\');\n'
           'INSERT INTO events VALUES (83,\'{"type":"view","user":"u3","tags":[]}\');\n'
           'INSERT INTO events VALUES (84,\'{"type":"view","user":"u4","tags":[]}\');\n'
           'INSERT INTO events VALUES (85,\'{"type":"view","user":"u5","tags":[]}\');\n'
           'INSERT INTO events VALUES (86,\'{"type":"view","user":"u6","tags":[]}\');\n'
           'INSERT INTO events VALUES (87,\'{"type":"view","user":"u7","tags":[]}\');\n'
           'INSERT INTO events VALUES (88,\'{"type":"view","user":"u8","tags":[]}\');\n'
           'INSERT INTO events VALUES (89,\'{"type":"view","user":"u9","tags":[]}\');\n'
           'INSERT INTO events VALUES (90,\'{"type":"view","user":"u10","tags":[]}\');\n'
           'INSERT INTO events VALUES (91,\'{"type":"view","user":"u11","tags":[]}\');\n'
           'INSERT INTO events VALUES (92,\'{"type":"view","user":"u12","tags":[]}\');\n'
           'INSERT INTO events VALUES (93,\'{"type":"view","user":"u13","tags":[]}\');\n'
           'INSERT INTO events VALUES (94,\'{"type":"view","user":"u14","tags":[]}\');\n'
           'INSERT INTO events VALUES (95,\'{"type":"view","user":"u15","tags":[]}\');\n'
           'INSERT INTO events VALUES (96,\'{"type":"view","user":"u16","tags":[]}\');\n'
           'INSERT INTO events VALUES (97,\'{"type":"view","user":"u17","tags":[]}\');\n'
           'INSERT INTO events VALUES (98,\'{"type":"view","user":"u18","tags":[]}\');\n'
           'INSERT INTO events VALUES (99,\'{"type":"view","user":"u19","tags":[]}\');\n'
           'INSERT INTO events VALUES (100,\'{"type":"view","user":"u20","tags":[]}\');\n'
           'INSERT INTO events VALUES (101,\'{"type":"view","user":"u21","tags":[]}\');\n'
           'INSERT INTO events VALUES (102,\'{"type":"view","user":"u22","tags":[]}\');\n'
           'INSERT INTO events VALUES (103,\'{"type":"view","user":"u23","tags":[]}\');\n'
           'INSERT INTO events VALUES (104,\'{"type":"view","user":"u24","tags":[]}\');\n'
           'INSERT INTO events VALUES (105,\'{"type":"view","user":"u25","tags":[]}\');\n'
           'INSERT INTO events VALUES (106,\'{"type":"view","user":"u26","tags":[]}\');\n'
           'INSERT INTO events VALUES (107,\'{"type":"view","user":"u27","tags":[]}\');\n'
           'INSERT INTO events VALUES (108,\'{"type":"view","user":"u28","tags":[]}\');\n'
           'INSERT INTO events VALUES (109,\'{"type":"view","user":"u29","tags":[]}\');\n'
           'INSERT INTO events VALUES (110,\'{"type":"view","user":"u30","tags":[]}\');\n'
           'INSERT INTO events VALUES (111,\'{"type":"view","user":"u31","tags":[]}\');\n'
           'INSERT INTO events VALUES (112,\'{"type":"view","user":"u32","tags":[]}\');\n'
           'INSERT INTO events VALUES (113,\'{"type":"view","user":"u33","tags":[]}\');\n'
           'INSERT INTO events VALUES (114,\'{"type":"view","user":"u34","tags":[]}\');\n'
           'INSERT INTO events VALUES (115,\'{"type":"view","user":"u35","tags":[]}\');\n'
           'INSERT INTO events VALUES (116,\'{"type":"view","user":"u36","tags":[]}\');\n'
           'INSERT INTO events VALUES (117,\'{"type":"view","user":"u37","tags":[]}\');\n'
           'INSERT INTO events VALUES (118,\'{"type":"view","user":"u38","tags":[]}\');\n'
           'INSERT INTO events VALUES (119,\'{"type":"view","user":"u39","tags":[]}\');\n'
           'INSERT INTO events VALUES (120,\'{"type":"view","user":"u0","tags":[]}\');\n'
           'INSERT INTO events VALUES (121,\'{"type":"view","user":"u1","tags":[]}\');\n'
           'INSERT INTO events VALUES (122,\'{"type":"view","user":"u2","tags":[]}\');\n'
           'INSERT INTO events VALUES (123,\'{"type":"view","user":"u3","tags":[]}\');\n'
           'INSERT INTO events VALUES (124,\'{"type":"view","user":"u4","tags":[]}\');\n'
           'INSERT INTO events VALUES (125,\'{"type":"view","user":"u5","tags":[]}\');\n'
           'INSERT INTO events VALUES (126,\'{"type":"view","user":"u6","tags":[]}\');\n'
           'INSERT INTO events VALUES (127,\'{"type":"view","user":"u7","tags":[]}\');\n'
           'INSERT INTO events VALUES (128,\'{"type":"view","user":"u8","tags":[]}\');\n'
           'INSERT INTO events VALUES (129,\'{"type":"view","user":"u9","tags":[]}\');\n'
           'INSERT INTO events VALUES (130,\'{"type":"view","user":"u10","tags":[]}\');\n'
           'INSERT INTO events VALUES (131,\'{"type":"view","user":"u11","tags":[]}\');\n'
           'INSERT INTO events VALUES (132,\'{"type":"view","user":"u12","tags":[]}\');\n'
           'INSERT INTO events VALUES (133,\'{"type":"view","user":"u13","tags":[]}\');\n'
           'INSERT INTO events VALUES (134,\'{"type":"view","user":"u14","tags":[]}\');\n'
           'INSERT INTO events VALUES (135,\'{"type":"view","user":"u15","tags":[]}\');\n'
           'INSERT INTO events VALUES (136,\'{"type":"view","user":"u16","tags":[]}\');\n'
           'INSERT INTO events VALUES (137,\'{"type":"view","user":"u17","tags":[]}\');\n'
           'INSERT INTO events VALUES (138,\'{"type":"view","user":"u18","tags":[]}\');\n'
           'INSERT INTO events VALUES (139,\'{"type":"view","user":"u19","tags":[]}\');\n'
           'INSERT INTO events VALUES (140,\'{"type":"view","user":"u20","tags":[]}\');\n'
           'INSERT INTO events VALUES (141,\'{"type":"view","user":"u21","tags":[]}\');\n'
           'INSERT INTO events VALUES (142,\'{"type":"view","user":"u22","tags":[]}\');\n'
           'INSERT INTO events VALUES (143,\'{"type":"view","user":"u23","tags":[]}\');\n'
           'INSERT INTO events VALUES (144,\'{"type":"view","user":"u24","tags":[]}\');\n'
           'INSERT INTO events VALUES (145,\'{"type":"view","user":"u25","tags":[]}\');\n'
           'INSERT INTO events VALUES (146,\'{"type":"view","user":"u26","tags":[]}\');\n'
           'INSERT INTO events VALUES (147,\'{"type":"view","user":"u27","tags":[]}\');\n'
           'INSERT INTO events VALUES (148,\'{"type":"view","user":"u28","tags":[]}\');\n'
           'INSERT INTO events VALUES (149,\'{"type":"view","user":"u29","tags":[]}\');\n'
           'INSERT INTO events VALUES (150,\'{"type":"view","user":"u30","tags":[]}\');\n'
           'INSERT INTO events VALUES (151,\'{"type":"view","user":"u31","tags":[]}\');\n'
           'INSERT INTO events VALUES (152,\'{"type":"view","user":"u32","tags":[]}\');\n'
           'INSERT INTO events VALUES (153,\'{"type":"view","user":"u33","tags":[]}\');\n'
           'INSERT INTO events VALUES (154,\'{"type":"view","user":"u34","tags":[]}\');\n'
           'INSERT INTO events VALUES (155,\'{"type":"view","user":"u35","tags":[]}\');\n'
           'INSERT INTO events VALUES (156,\'{"type":"view","user":"u36","tags":[]}\');\n'
           'INSERT INTO events VALUES (157,\'{"type":"view","user":"u37","tags":[]}\');\n'
           'INSERT INTO events VALUES (158,\'{"type":"view","user":"u38","tags":[]}\');\n'
           'INSERT INTO events VALUES (159,\'{"type":"view","user":"u39","tags":[]}\');\n'
           'INSERT INTO events VALUES (160,\'{"type":"view","user":"u0","tags":[]}\');\n'
           'INSERT INTO events VALUES (161,\'{"type":"view","user":"u1","tags":[]}\');\n'
           'INSERT INTO events VALUES (162,\'{"type":"view","user":"u2","tags":[]}\');\n'
           'INSERT INTO events VALUES (163,\'{"type":"view","user":"u3","tags":[]}\');\n'
           'INSERT INTO events VALUES (164,\'{"type":"view","user":"u4","tags":[]}\');\n'
           'INSERT INTO events VALUES (165,\'{"type":"view","user":"u5","tags":[]}\');\n'
           'INSERT INTO events VALUES (166,\'{"type":"view","user":"u6","tags":[]}\');\n'
           'INSERT INTO events VALUES (167,\'{"type":"view","user":"u7","tags":[]}\');\n'
           'INSERT INTO events VALUES (168,\'{"type":"view","user":"u8","tags":[]}\');\n'
           'INSERT INTO events VALUES (169,\'{"type":"view","user":"u9","tags":[]}\');\n'
           'INSERT INTO events VALUES (170,\'{"type":"view","user":"u10","tags":[]}\');\n'
           'INSERT INTO events VALUES (171,\'{"type":"view","user":"u11","tags":[]}\');\n'
           'INSERT INTO events VALUES (172,\'{"type":"view","user":"u12","tags":[]}\');\n'
           'INSERT INTO events VALUES (173,\'{"type":"view","user":"u13","tags":[]}\');\n'
           'INSERT INTO events VALUES (174,\'{"type":"view","user":"u14","tags":[]}\');\n'
           'INSERT INTO events VALUES (175,\'{"type":"view","user":"u15","tags":[]}\');\n'
           'INSERT INTO events VALUES (176,\'{"type":"view","user":"u16","tags":[]}\');\n'
           'INSERT INTO events VALUES (177,\'{"type":"view","user":"u17","tags":[]}\');\n'
           'INSERT INTO events VALUES (178,\'{"type":"view","user":"u18","tags":[]}\');\n'
           'INSERT INTO events VALUES (179,\'{"type":"view","user":"u19","tags":[]}\');\n'
           'INSERT INTO events VALUES (180,\'{"type":"view","user":"u20","tags":[]}\');\n'
           'INSERT INTO events VALUES (181,\'{"type":"view","user":"u21","tags":[]}\');\n'
           'INSERT INTO events VALUES (182,\'{"type":"view","user":"u22","tags":[]}\');\n'
           'INSERT INTO events VALUES (183,\'{"type":"view","user":"u23","tags":[]}\');\n'
           'INSERT INTO events VALUES (184,\'{"type":"view","user":"u24","tags":[]}\');\n'
           'INSERT INTO events VALUES (185,\'{"type":"view","user":"u25","tags":[]}\');\n'
           'INSERT INTO events VALUES (186,\'{"type":"view","user":"u26","tags":[]}\');\n'
           'INSERT INTO events VALUES (187,\'{"type":"view","user":"u27","tags":[]}\');\n'
           'INSERT INTO events VALUES (188,\'{"type":"view","user":"u28","tags":[]}\');\n'
           'INSERT INTO events VALUES (189,\'{"type":"view","user":"u29","tags":[]}\');\n'
           'INSERT INTO events VALUES (190,\'{"type":"view","user":"u30","tags":[]}\');\n'
           'INSERT INTO events VALUES (191,\'{"type":"view","user":"u31","tags":[]}\');\n'
           'INSERT INTO events VALUES (192,\'{"type":"view","user":"u32","tags":[]}\');\n'
           'INSERT INTO events VALUES (193,\'{"type":"view","user":"u33","tags":[]}\');\n'
           'INSERT INTO events VALUES (194,\'{"type":"view","user":"u34","tags":[]}\');\n'
           'INSERT INTO events VALUES (195,\'{"type":"view","user":"u35","tags":[]}\');\n'
           'INSERT INTO events VALUES (196,\'{"type":"view","user":"u36","tags":[]}\');\n'
           'INSERT INTO events VALUES (197,\'{"type":"view","user":"u37","tags":[]}\');\n'
           'INSERT INTO events VALUES (198,\'{"type":"view","user":"u38","tags":[]}\');\n'
           'INSERT INTO events VALUES (199,\'{"type":"view","user":"u39","tags":[]}\');\n'
           'INSERT INTO events VALUES (200,\'{"type":"view","user":"u0","tags":[]}\');\n'
           'INSERT INTO events VALUES (201,\'{"type":"view","user":"u1","tags":[]}\');\n'
           'INSERT INTO events VALUES (202,\'{"type":"view","user":"u2","tags":[]}\');\n'
           'INSERT INTO events VALUES (203,\'{"type":"view","user":"u3","tags":[]}\');\n'
           'INSERT INTO events VALUES (204,\'{"type":"view","user":"u4","tags":[]}\');\n'
           'INSERT INTO events VALUES (205,\'{"type":"view","user":"u5","tags":[]}\');\n'
           'INSERT INTO events VALUES (206,\'{"type":"view","user":"u6","tags":[]}\');\n'
           'INSERT INTO events VALUES (207,\'{"type":"view","user":"u7","tags":[]}\');\n'
           'INSERT INTO events VALUES (208,\'{"type":"view","user":"u8","tags":[]}\');\n'
           'INSERT INTO events VALUES (209,\'{"type":"view","user":"u9","tags":[]}\');\n'
           'INSERT INTO events VALUES (210,\'{"type":"view","user":"u10","tags":[]}\');\n'
           'INSERT INTO events VALUES (211,\'{"type":"view","user":"u11","tags":[]}\');\n'
           'INSERT INTO events VALUES (212,\'{"type":"view","user":"u12","tags":[]}\');\n'
           'INSERT INTO events VALUES (213,\'{"type":"view","user":"u13","tags":[]}\');\n'
           'INSERT INTO events VALUES (214,\'{"type":"view","user":"u14","tags":[]}\');\n'
           'INSERT INTO events VALUES (215,\'{"type":"view","user":"u15","tags":[]}\');\n'
           'INSERT INTO events VALUES (216,\'{"type":"view","user":"u16","tags":[]}\');\n'
           'INSERT INTO events VALUES (217,\'{"type":"view","user":"u17","tags":[]}\');\n'
           'INSERT INTO events VALUES (218,\'{"type":"view","user":"u18","tags":[]}\');\n'
           'INSERT INTO events VALUES (219,\'{"type":"view","user":"u19","tags":[]}\');\n'
           'INSERT INTO events VALUES (220,\'{"type":"view","user":"u20","tags":[]}\');\n'
           'INSERT INTO events VALUES (221,\'{"type":"view","user":"u21","tags":[]}\');\n'
           'INSERT INTO events VALUES (222,\'{"type":"view","user":"u22","tags":[]}\');\n'
           'INSERT INTO events VALUES (223,\'{"type":"view","user":"u23","tags":[]}\');\n'
           'INSERT INTO events VALUES (224,\'{"type":"view","user":"u24","tags":[]}\');\n'
           'INSERT INTO events VALUES (225,\'{"type":"view","user":"u25","tags":[]}\');\n'
           'INSERT INTO events VALUES (226,\'{"type":"view","user":"u26","tags":[]}\');\n'
           'INSERT INTO events VALUES (227,\'{"type":"view","user":"u27","tags":[]}\');\n'
           'INSERT INTO events VALUES (228,\'{"type":"view","user":"u28","tags":[]}\');\n'
           'INSERT INTO events VALUES (229,\'{"type":"view","user":"u29","tags":[]}\');\n'
           'INSERT INTO events VALUES (230,\'{"type":"view","user":"u30","tags":[]}\');\n'
           'INSERT INTO events VALUES (231,\'{"type":"view","user":"u31","tags":[]}\');\n'
           'INSERT INTO events VALUES (232,\'{"type":"view","user":"u32","tags":[]}\');\n'
           'INSERT INTO events VALUES (233,\'{"type":"view","user":"u33","tags":[]}\');\n'
           'INSERT INTO events VALUES (234,\'{"type":"view","user":"u34","tags":[]}\');\n'
           'INSERT INTO events VALUES (235,\'{"type":"view","user":"u35","tags":[]}\');\n'
           'INSERT INTO events VALUES (236,\'{"type":"view","user":"u36","tags":[]}\');\n'
           'INSERT INTO events VALUES (237,\'{"type":"view","user":"u37","tags":[]}\');\n'
           'INSERT INTO events VALUES (238,\'{"type":"view","user":"u38","tags":[]}\');\n'
           'INSERT INTO events VALUES (239,\'{"type":"view","user":"u39","tags":[]}\');\n'
           'INSERT INTO events VALUES (240,\'{"type":"view","user":"u0","tags":[]}\');\n'
           'INSERT INTO events VALUES (241,\'{"type":"view","user":"u1","tags":[]}\');\n'
           'INSERT INTO events VALUES (242,\'{"type":"view","user":"u2","tags":[]}\');\n'
           'INSERT INTO events VALUES (243,\'{"type":"view","user":"u3","tags":[]}\');\n'
           'INSERT INTO events VALUES (244,\'{"type":"view","user":"u4","tags":[]}\');\n'
           'INSERT INTO events VALUES (245,\'{"type":"view","user":"u5","tags":[]}\');\n'
           'INSERT INTO events VALUES (246,\'{"type":"view","user":"u6","tags":[]}\');\n'
           'INSERT INTO events VALUES (247,\'{"type":"view","user":"u7","tags":[]}\');\n'
           'INSERT INTO events VALUES (248,\'{"type":"view","user":"u8","tags":[]}\');\n'
           'INSERT INTO events VALUES (249,\'{"type":"view","user":"u9","tags":[]}\');\n'
           'INSERT INTO events VALUES (250,\'{"type":"view","user":"u10","tags":[]}\');\n'
           'INSERT INTO events VALUES (251,\'{"type":"view","user":"u11","tags":[]}\');\n'
           'INSERT INTO events VALUES (252,\'{"type":"view","user":"u12","tags":[]}\');\n'
           'INSERT INTO events VALUES (253,\'{"type":"view","user":"u13","tags":[]}\');\n'
           'INSERT INTO events VALUES (254,\'{"type":"view","user":"u14","tags":[]}\');\n'
           'INSERT INTO events VALUES (255,\'{"type":"view","user":"u15","tags":[]}\');\n'
           'INSERT INTO events VALUES (256,\'{"type":"view","user":"u16","tags":[]}\');\n'
           'INSERT INTO events VALUES (257,\'{"type":"view","user":"u17","tags":[]}\');\n'
           'INSERT INTO events VALUES (258,\'{"type":"view","user":"u18","tags":[]}\');\n'
           'INSERT INTO events VALUES (259,\'{"type":"view","user":"u19","tags":[]}\');\n'
           'INSERT INTO events VALUES (260,\'{"type":"view","user":"u20","tags":[]}\');\n'
           'INSERT INTO events VALUES (261,\'{"type":"view","user":"u21","tags":[]}\');\n'
           'INSERT INTO events VALUES (262,\'{"type":"view","user":"u22","tags":[]}\');\n'
           'INSERT INTO events VALUES (263,\'{"type":"view","user":"u23","tags":[]}\');\n'
           'INSERT INTO events VALUES (264,\'{"type":"view","user":"u24","tags":[]}\');\n'
           'INSERT INTO events VALUES (265,\'{"type":"view","user":"u25","tags":[]}\');\n'
           'INSERT INTO events VALUES (266,\'{"type":"view","user":"u26","tags":[]}\');\n'
           'INSERT INTO events VALUES (267,\'{"type":"view","user":"u27","tags":[]}\');\n'
           'INSERT INTO events VALUES (268,\'{"type":"view","user":"u28","tags":[]}\');\n'
           'INSERT INTO events VALUES (269,\'{"type":"view","user":"u29","tags":[]}\');\n'
           'INSERT INTO events VALUES (270,\'{"type":"view","user":"u30","tags":[]}\');\n'
           'INSERT INTO events VALUES (271,\'{"type":"view","user":"u31","tags":[]}\');\n'
           'INSERT INTO events VALUES (272,\'{"type":"view","user":"u32","tags":[]}\');\n'
           'INSERT INTO events VALUES (273,\'{"type":"view","user":"u33","tags":[]}\');\n'
           'INSERT INTO events VALUES (274,\'{"type":"view","user":"u34","tags":[]}\');\n'
           'INSERT INTO events VALUES (275,\'{"type":"view","user":"u35","tags":[]}\');\n'
           'INSERT INTO events VALUES (276,\'{"type":"view","user":"u36","tags":[]}\');\n'
           'INSERT INTO events VALUES (277,\'{"type":"view","user":"u37","tags":[]}\');\n'
           'INSERT INTO events VALUES (278,\'{"type":"view","user":"u38","tags":[]}\');\n'
           'INSERT INTO events VALUES (279,\'{"type":"view","user":"u39","tags":[]}\');\n'
           'INSERT INTO events VALUES (280,\'{"type":"view","user":"u0","tags":[]}\');\n'
           'INSERT INTO events VALUES (281,\'{"type":"view","user":"u1","tags":[]}\');\n'
           'INSERT INTO events VALUES (282,\'{"type":"view","user":"u2","tags":[]}\');\n'
           'INSERT INTO events VALUES (283,\'{"type":"view","user":"u3","tags":[]}\');\n'
           'INSERT INTO events VALUES (284,\'{"type":"view","user":"u4","tags":[]}\');\n'
           'INSERT INTO events VALUES (285,\'{"type":"view","user":"u5","tags":[]}\');\n'
           'INSERT INTO events VALUES (286,\'{"type":"view","user":"u6","tags":[]}\');\n'
           'INSERT INTO events VALUES (287,\'{"type":"view","user":"u7","tags":[]}\');\n'
           'INSERT INTO events VALUES (288,\'{"type":"view","user":"u8","tags":[]}\');\n'
           'INSERT INTO events VALUES (289,\'{"type":"view","user":"u9","tags":[]}\');\n'
           'INSERT INTO events VALUES (290,\'{"type":"view","user":"u10","tags":[]}\');\n'
           'INSERT INTO events VALUES (291,\'{"type":"view","user":"u11","tags":[]}\');\n'
           'INSERT INTO events VALUES (292,\'{"type":"view","user":"u12","tags":[]}\');\n'
           'INSERT INTO events VALUES (293,\'{"type":"view","user":"u13","tags":[]}\');\n'
           'INSERT INTO events VALUES (294,\'{"type":"view","user":"u14","tags":[]}\');\n'
           'INSERT INTO events VALUES (295,\'{"type":"view","user":"u15","tags":[]}\');\n'
           'INSERT INTO events VALUES (296,\'{"type":"view","user":"u16","tags":[]}\');\n'
           'INSERT INTO events VALUES (297,\'{"type":"view","user":"u17","tags":[]}\');\n'
           'INSERT INTO events VALUES (298,\'{"type":"view","user":"u18","tags":[]}\');\n'
           'INSERT INTO events VALUES (299,\'{"type":"view","user":"u19","tags":[]}\');\n',
  'expected': [[3, 0, 53, 'SEARCH events USING COVERING INDEX idx_events_user (<expr>=?)']],
  'hint': "Индекс на выражении: ON events ((payload ->> '$.user')) — выражение в скобках должно совпадать с "
          'запросом.',
  'check': "EXPLAIN QUERY PLAN SELECT id FROM events WHERE payload ->> '$.user' = 'anna'",
  'contains': ['USING INDEX idx_events_user']},
 {'id': 'd5-json-build',
  'mode': 'sql',
  'title': 'Собрать документы из таблиц',
  'statement': 'Для каждого клиента соберите документ: JSON-объект с полями id, name и orders — массивом '
               'номеров его заказов по возрастанию. Колонки: doc (текст JSON); порядок по id клиента; '
               'клиенты без заказов тоже нужны (orders — пустой массив).',
  'starter': '-- JSON-документ на клиента\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['{"id":1,"name":"Анна","orders":[1,2]}'],
               ['{"id":2,"name":"Борис","orders":[3,8]}'],
               ['{"id":3,"name":"Вера","orders":[4,5,6]}'],
               ['{"id":4,"name":"Глеб","orders":[]}'],
               ['{"id":5,"name":"Дарья","orders":[7]}'],
               ['{"id":6,"name":"Егор","orders":[]}']],
  'expected_cols': ['doc'],
  'hint': 'json_object(…) собирает объект, json_group_array(…) — массив; вложенный массив оберните в json(), '
          'чтобы он не стал строкой.',
  'ordered': True},
 {'id': 'd5-graph-cte',
  'mode': 'sql',
  'title': 'Граф в SQL: друзья друзей',
  'statement': 'friends(a, b) — дружба в обе стороны (записана парой строк). Выведите друзей друзей Анны — '
               'тех, кто не она сама и не её прямой друг (колонка name, по алфавиту).',
  'starter': '-- друзья друзей Анны\nSELECT\n',
  'setup': 'CREATE TABLE friends (a TEXT NOT NULL, b TEXT NOT NULL);\n'
           'INSERT INTO friends VALUES '
           "('Анна','Борис'),('Борис','Анна'),('Анна','Вера'),('Вера','Анна'),('Борис','Глеб'),('Глеб','Борис'),('Вера','Дарья'),('Дарья','Вера'),('Глеб','Егор'),('Егор','Глеб');\n",
  'expected': [['Глеб'], ['Дарья']],
  'expected_cols': ['name'],
  'hint': 'Два самосоединения: друг (f1) и его друг (f2); исключите саму Анну и её прямых друзей.',
  'ordered': True},
 {'id': 'd5-kv-ttl',
  'mode': 'func',
  'func': 'kv_run',
  'title': 'Ключ-значение с временем жизни',
  'statement': 'Операции: ["set", t, ключ, значение, ttl] (ttl — число секунд или None) и ["get", t, ключ], '
               'где t — момент времени. Запись живёт до t + ttl, не включая: в момент t + ttl её уже нет. '
               'Напишите kv_run(ops): список результатов всех get в порядке выполнения (значение или None).',
  'starter': 'def kv_run(ops):\n    pass\n',
  'tests': [{'args': [[['set', 0, 'a', 1, 10], ['get', 5, 'a'], ['get', 10, 'a'], ['get', 11, 'a']]],
             'expected': [1, None, None]},
            {'args': [[['set', 0, 'a', 1, None], ['get', 1000, 'a']]], 'expected': [1]},
            {'args': [[['get', 0, 'x']]], 'expected': [None]},
            {'args': [[['set', 0, 'a', 1, 5], ['set', 3, 'a', 2, 5], ['get', 7, 'a'], ['get', 8, 'a']]],
             'expected': [2, None]}],
  'hint': 'Храните значение вместе с моментом истечения; get возвращает его, только если t меньше этого '
          'момента.'},
 {'id': 'd5-kv-incr',
  'mode': 'func',
  'func': 'counters',
  'title': 'Атомарные счётчики',
  'statement': 'Операции над счётчиками: ["incr", ключ, дельта] и ["decr", ключ, дельта]; отсутствующий ключ '
               'считается нулём. Напишите counters(ops): словарь итоговых значений.',
  'starter': 'def counters(ops):\n    pass\n',
  'tests': [{'args': [[['incr', 'views', 1],
                       ['incr', 'views', 1],
                       ['decr', 'stock', 3],
                       ['incr', 'views', 5]]],
             'expected': {'views': 7, 'stock': -3}},
            {'args': [[]], 'expected': {}},
            {'args': [[['decr', 'a', 1], ['incr', 'a', 1]]], 'expected': {'a': 0}}],
  'hint': 'c.get(ключ, 0) даёт нуль для нового ключа; decr — прибавка отрицательной дельты.'},
 {'id': 'd5-key-design',
  'mode': 'func',
  'func': 'make_key',
  'title': 'Составные ключи',
  'statement': 'Ключ собирается из частей через двоеточие. Чтобы двоеточие и знак процента внутри части не '
               'ломали разбор, их экранируют: «%» → «%25», «:» → «%3A» (сначала процент). Напишите '
               'make_key(parts): список частей (строки или числа) превращается в ключ; пустой список даёт '
               'пустую строку.',
  'starter': 'def make_key(parts):\n    pass\n',
  'tests': [{'args': [['user', 42, 'profile']], 'expected': 'user:42:profile'},
            {'args': [['a:b', 'c']], 'expected': 'a%3Ab:c'},
            {'args': [['50%', 'x:y']], 'expected': '50%25:x%3Ay'},
            {'args': [[]], 'expected': ''},
            {'args': [['only']], 'expected': 'only'}],
  'hint': 'Экранируйте каждую часть (сначала %, затем :), потом соедините через двоеточие.'},
 {'id': 'd5-doc-match',
  'mode': 'func',
  'func': 'doc_match',
  'title': 'Условия по полям документа',
  'statement': 'Документ — вложенный словарь. Запрос — словарь «путь через точку → условие». Условие — '
               'значение (равенство) или словарь с одним оператором: {"$gt": x}, {"$lt": x}, {"$in": [..]}. '
               'Напишите doc_match(doc, query): True, если документ удовлетворяет всем условиям; '
               'отсутствующее поле условие не выполняет.',
  'starter': 'def doc_match(doc, query):\n    pass\n',
  'tests': [{'args': [{'user': {'city': 'Казань'}, 'total': 1500},
                      {'user.city': 'Казань', 'total': {'$gt': 1000}}],
             'expected': True},
            {'args': [{'user': {'city': 'Тверь'}, 'total': 1500}, {'user.city': 'Казань'}],
             'expected': False},
            {'args': [{'a': 1}, {'b': 1}], 'expected': False},
            {'args': [{'a': 5}, {'a': {'$in': [1, 5, 9]}}], 'expected': True},
            {'args': [{'a': 5}, {'a': {'$lt': 5}}], 'expected': False},
            {'args': [{'x': {'y': {'z': 1}}}, {'x.y.z': 1}], 'expected': True},
            {'args': [{}, {}], 'expected': True}],
  'hint': 'Спуск по частям пути; для условий-словарей — одна из трёх операций; нет поля — сразу False.'},
 {'id': 'd5-doc-find',
  'mode': 'func',
  'func': 'find_ids',
  'title': 'Поиск по коллекции',
  'statement': 'Коллекция — список документов со строковым полем "id". Запрос — словарь «поле верхнего '
               'уровня → значение или {"$gt": x}». Напишите find_ids(docs, query): отсортированный список id '
               'подходящих документов (документ подходит, если для каждого поля запроса оно есть и условие '
               'выполнено).',
  'starter': 'def find_ids(docs, query):\n    pass\n',
  'tests': [{'args': [[{'id': 'b', 'age': 30}, {'id': 'a', 'age': 25}, {'id': 'c', 'city': 'X'}],
                      {'age': {'$gt': 26}}],
             'expected': ['b']},
            {'args': [[{'id': 'a', 't': 1}, {'id': 'b', 't': 1, 'u': 2}], {'t': 1}], 'expected': ['a', 'b']},
            {'args': [[], {'x': 1}], 'expected': []},
            {'args': [[{'id': 'a'}], {}], 'expected': ['a']}],
  'hint': 'Для каждого документа проверьте все поля запроса; результат отсортируйте.'},
 {'id': 'd5-embed',
  'mode': 'func',
  'func': 'embed_users',
  'title': 'Денормализация: вложить автора',
  'statement': 'Заказы — список словарей с полем user_id, пользователи — словарь «id (строка) → {"name": '
               '…}». Напишите embed_users(orders, users): новый список заказов, в которых поле user_id '
               'заменено на поле user — копию словаря пользователя (если пользователя нет — None). Остальные '
               'поля заказа сохраните.',
  'starter': 'def embed_users(orders, users):\n    pass\n',
  'tests': [{'args': [[{'id': 1, 'user_id': 7, 'total': 10}, {'id': 2, 'user_id': 8, 'total': 5}],
                      {'7': {'name': 'Анна'}}],
             'expected': [{'id': 1, 'total': 10, 'user': {'name': 'Анна'}},
                          {'id': 2, 'total': 5, 'user': None}]},
            {'args': [[], {'1': {'name': 'x'}}], 'expected': []},
            {'args': [[{'id': 3, 'user_id': 1}], {'1': {'name': 'Борис', 'city': 'К'}}],
             'expected': [{'id': 3, 'user': {'name': 'Борис', 'city': 'К'}}]}],
  'hint': 'Копируйте поля заказа без user_id и добавляйте user из словаря по ключу str(user_id).'},
 {'id': 'd5-partition',
  'mode': 'func',
  'func': 'partition_keys',
  'title': 'Ключ партиции → узел',
  'statement': 'Узел для ключа определяется как (сумма кодов символов ключа) % nodes. Напишите '
               'partition_keys(keys, nodes): словарь «номер узла (строка) → отсортированный список ключей» '
               'только для узлов, где есть ключи.',
  'starter': 'def partition_keys(keys, nodes):\n    pass\n',
  'tests': [{'args': [['a', 'b', 'c', 'd'], 2], 'expected': {'1': ['a', 'c'], '0': ['b', 'd']}},
            {'args': [['chat1', 'chat2', 'chat3'], 3],
             'expected': {'0': ['chat1'], '1': ['chat2'], '2': ['chat3']}},
            {'args': [[], 5], 'expected': {}},
            {'args': [['x'], 1], 'expected': {'0': ['x']}}],
  'hint': 'Вычислите хеш по правилу, сгруппируйте и отсортируйте внутри групп; ключи словаря — строки.'},
 {'id': 'd5-wide-row',
  'mode': 'func',
  'func': 'slice_rows',
  'title': 'Диапазон по ключу кластеризации',
  'statement': 'Строки — список [партиция, кластеризация (число), значение] в произвольном порядке. Напишите '
               'slice_rows(rows, partition, start, end): значения партиции с кластеризацией start ≤ c < end, '
               'упорядоченные по c.',
  'starter': 'def slice_rows(rows, partition, start, end):\n    pass\n',
  'tests': [{'args': [[['chat1', 5, 'e'], ['chat1', 1, 'a'], ['chat2', 2, 'x'], ['chat1', 3, 'c']],
                      'chat1',
                      1,
                      5],
             'expected': ['a', 'c']},
            {'args': [[['a', 1, 'x']], 'b', 0, 10], 'expected': []},
            {'args': [[], 'a', 0, 1], 'expected': []},
            {'args': [[['a', 2, 'm'], ['a', 2, 'n']], 'a', 2, 3], 'expected': ['m', 'n']}],
  'hint': 'Отберите нужную партицию и диапазон, отсортируйте пары по кластеризации.'},
 {'id': 'd5-friends-of-friends',
  'mode': 'func',
  'func': 'friends_of_friends',
  'title': 'Друзья друзей в графе',
  'statement': 'Граф — словарь «имя → список друзей» (дружба симметрична, но не нужно этого проверять). '
               'Напишите friends_of_friends(graph, person): отсортированный список людей, которые являются '
               'друзьями друзей person, но не самим person и не его прямыми друзьями.',
  'starter': 'def friends_of_friends(graph, person):\n    pass\n',
  'tests': [{'args': [{'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'E'], 'D': ['B'], 'E': ['C']}, 'A'],
             'expected': ['D', 'E']},
            {'args': [{'A': []}, 'A'], 'expected': []},
            {'args': [{'A': ['B'], 'B': ['A']}, 'A'], 'expected': []},
            {'args': [{}, 'X'], 'expected': []},
            {'args': [{'A': ['B', 'C'], 'B': ['C', 'A'], 'C': ['B', 'A']}, 'A'], 'expected': []}],
  'hint': 'Соберите множество друзей друзей и вычтите прямых друзей и самого человека.'},
 {'id': 'd5-graph-path',
  'mode': 'func',
  'func': 'shortest_path',
  'title': 'Кратчайший путь в графе',
  'statement': 'Напишите shortest_path(graph, a, b): число рёбер в кратчайшем пути между a и b поиском в '
               'ширину (граф — словарь «узел → список соседей»); если пути нет — -1; для a == b — 0.',
  'starter': 'def shortest_path(graph, a, b):\n    pass\n',
  'tests': [{'args': [{'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', 'D'], 'expected': 2},
            {'args': [{'A': ['B'], 'B': []}, 'A', 'C'], 'expected': -1},
            {'args': [{'A': []}, 'A', 'A'], 'expected': 0},
            {'args': [{'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': ['E'], 'E': []}, 'A', 'E'], 'expected': 4},
            {'args': [{'A': ['B'], 'B': ['A']}, 'B', 'A'], 'expected': 1}],
  'hint': 'Обход в ширину слоями: каждый слой — на один шаг дальше; нашли b — вернули номер слоя.'},
 {'id': 'd5-inverted-index',
  'mode': 'func',
  'func': 'build_index',
  'title': 'Инвертированный индекс',
  'statement': 'Документы — словарь «id (строка) → текст». Слова — подряд идущие буквы и цифры, регистр не '
               'важен. Напишите build_index(docs): словарь «слово → отсортированный список id документов, '
               'где оно есть» (без повторов).',
  'starter': 'def build_index(docs):\n    pass\n',
  'tests': [{'args': [{'1': 'Быстрые базы данных', '2': 'Базы и индексы', '3': 'быстрые индексы'}],
             'expected': {'базы': ['1', '2'],
                          'быстрые': ['1', '3'],
                          'данных': ['1'],
                          'и': ['2'],
                          'индексы': ['2', '3']}},
            {'args': [{}], 'expected': {}},
            {'args': [{'a': 'Hello, hello! World'}], 'expected': {'hello': ['a'], 'world': ['a']}},
            {'args': [{'x': 'a1 b2', 'y': 'B2 c3'}],
             'expected': {'a1': ['x'], 'b2': ['x', 'y'], 'c3': ['y']}}],
  'hint': 'Разбейте текст регулярным выражением на слова, сделайте множество слов документа и добавьте id в '
          'список слова.'},
 {'id': 'd5-search-and',
  'mode': 'func',
  'func': 'search_all',
  'title': 'Поиск по всем словам',
  'statement': 'Индекс — словарь «слово → список id». Напишите search_all(index, query): отсортированный '
               'список id документов, в которых есть ВСЕ слова запроса (запрос — строка, слова разделены '
               'пробелами, регистр не важен). Пустой запрос даёт пустой список.',
  'starter': 'def search_all(index, query):\n    pass\n',
  'tests': [{'args': [{'баз': ['1', '2'], 'быстр': ['1', '3']}, 'Баз Быстр'], 'expected': ['1']},
            {'args': [{'a': ['1']}, 'a b'], 'expected': []},
            {'args': [{'a': ['1', '2']}, ''], 'expected': []},
            {'args': [{'a': ['2', '1']}, 'a'], 'expected': ['1', '2']}],
  'hint': 'Пересечение множеств id по каждому слову запроса; отсутствующее слово даёт пустое множество.'},
 {'id': 'd5-tf-rank',
  'mode': 'func',
  'func': 'rank',
  'title': 'Ранжирование по частоте слов',
  'statement': 'Документы — словарь «id → текст». Оценка документа — сумма по словам запроса числа вхождений '
               'слова в документ (регистр не важен). Напишите rank(docs, query): список id с положительной '
               'оценкой, по убыванию оценки, при равенстве — по возрастанию id.',
  'starter': 'def rank(docs, query):\n    pass\n',
  'tests': [{'args': [{'1': 'базы базы данных', '2': 'данных мало', '3': 'ничего'}, 'базы данных'],
             'expected': ['1', '2']},
            {'args': [{'a': 'x x x', 'b': 'x y'}, 'x'], 'expected': ['a', 'b']},
            {'args': [{}, 'q'], 'expected': []},
            {'args': [{'b': 'z', 'a': 'z'}, 'z'], 'expected': ['a', 'b']}],
  'hint': 'Оценка — сумма words.count(слово) по словам запроса; сортировка по паре (−оценка, id).'},
 {'id': 'd5-flatten',
  'mode': 'func',
  'func': 'flatten_doc',
  'title': 'Плоские пути документа',
  'statement': 'Для индексирования вложенный документ превращают в плоский словарь «путь через точку → '
               'значение». Напишите flatten_doc(doc): листья (не словари) попадают в результат, вложенные '
               'словари разворачиваются рекурсивно; списки считайте листьями.',
  'starter': 'def flatten_doc(doc):\n    pass\n',
  'tests': [{'args': [{'a': 1, 'b': {'c': 2, 'd': {'e': [3]}}}],
             'expected': {'a': 1, 'b.c': 2, 'b.d.e': [3]}},
            {'args': [{}], 'expected': {}},
            {'args': [{'x': {'y': {'z': 'w'}}}], 'expected': {'x.y.z': 'w'}},
            {'args': [{'k': []}], 'expected': {'k': []}}],
  'hint': "Рекурсия с накоплением префикса: ключ верхнего уровня + '.' + вложенные ключи."},
 {'id': 'd5-validate',
  'mode': 'func',
  'func': 'validate',
  'title': 'Проверка документа по схеме',
  'statement': "Схема — словарь «поле → тип» с типами 'str', 'int' или 'bool'; все поля обязательны. "
               'Напишите validate(doc, schema): отсортированный список ошибок — «missing:поле» для '
               'отсутствующего поля и «type:поле» для неверного типа (bool не считается int).',
  'starter': 'def validate(doc, schema):\n    pass\n',
  'tests': [{'args': [{'name': 'Анна', 'age': 30}, {'name': 'str', 'age': 'int'}], 'expected': []},
            {'args': [{'name': 5}, {'name': 'str', 'age': 'int'}], 'expected': ['missing:age', 'type:name']},
            {'args': [{'age': True}, {'age': 'int'}], 'expected': ['type:age']},
            {'args': [{}, {}], 'expected': []},
            {'args': [{'ok': False, 'n': 'x'}, {'ok': 'bool', 'n': 'int'}], 'expected': ['type:n']}],
  'hint': 'Для каждого поля схемы: нет — missing, не тот тип — type; bool — подкласс int, его нужно '
          'исключить вручную.'}]}
