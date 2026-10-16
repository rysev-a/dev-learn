"""Задачи книги «Базы данных»: глава 19."""

TASKS: dict[int, list[dict]] = {19: [{'id': 'd3-create-index',
  'mode': 'sql',
  'title': 'Первый индекс',
  'statement': 'Запрос SELECT * FROM orders WHERE customer_id = 7 просматривает таблицу целиком. Создайте '
               'индекс по customer_id (назовите его как угодно), чтобы план стал поиском по индексу.',
  'starter': '-- индекс для поиска заказов по customer_id\nCREATE INDEX\n',
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, city TEXT NOT NULL, '
           'created TEXT NOT NULL, status TEXT NOT NULL, total INTEGER NOT NULL);\n'
           "INSERT INTO orders VALUES (1,1,'Казань','2024-02-02','new',101);\n"
           "INSERT INTO orders VALUES (2,2,'Тверь','2024-03-03','cancelled',102);\n"
           "INSERT INTO orders VALUES (3,3,'Омск','2024-04-04','paid',103);\n"
           "INSERT INTO orders VALUES (4,4,'Москва','2024-05-05','new',104);\n"
           "INSERT INTO orders VALUES (5,5,'Казань','2024-06-06','cancelled',105);\n"
           "INSERT INTO orders VALUES (6,6,'Тверь','2024-07-07','paid',106);\n"
           "INSERT INTO orders VALUES (7,7,'Омск','2024-08-08','new',107);\n"
           "INSERT INTO orders VALUES (8,8,'Москва','2024-09-09','cancelled',108);\n"
           "INSERT INTO orders VALUES (9,9,'Казань','2024-10-10','paid',109);\n"
           "INSERT INTO orders VALUES (10,10,'Тверь','2024-11-11','new',110);\n"
           "INSERT INTO orders VALUES (11,11,'Омск','2024-12-12','cancelled',111);\n"
           "INSERT INTO orders VALUES (12,12,'Москва','2024-01-13','paid',112);\n"
           "INSERT INTO orders VALUES (13,13,'Казань','2024-02-14','new',113);\n"
           "INSERT INTO orders VALUES (14,14,'Тверь','2024-03-15','cancelled',114);\n"
           "INSERT INTO orders VALUES (15,15,'Омск','2024-04-16','paid',115);\n"
           "INSERT INTO orders VALUES (16,16,'Москва','2024-05-17','new',116);\n"
           "INSERT INTO orders VALUES (17,17,'Казань','2024-06-18','cancelled',117);\n"
           "INSERT INTO orders VALUES (18,18,'Тверь','2024-07-19','paid',118);\n"
           "INSERT INTO orders VALUES (19,19,'Омск','2024-08-20','new',119);\n"
           "INSERT INTO orders VALUES (20,20,'Москва','2024-09-21','cancelled',120);\n"
           "INSERT INTO orders VALUES (21,21,'Казань','2024-10-22','paid',121);\n"
           "INSERT INTO orders VALUES (22,22,'Тверь','2024-11-23','new',122);\n"
           "INSERT INTO orders VALUES (23,23,'Омск','2024-12-24','cancelled',123);\n"
           "INSERT INTO orders VALUES (24,24,'Москва','2024-01-25','paid',124);\n"
           "INSERT INTO orders VALUES (25,25,'Казань','2024-02-26','new',125);\n"
           "INSERT INTO orders VALUES (26,26,'Тверь','2024-03-27','cancelled',126);\n"
           "INSERT INTO orders VALUES (27,27,'Омск','2024-04-28','paid',127);\n"
           "INSERT INTO orders VALUES (28,28,'Москва','2024-05-01','new',128);\n"
           "INSERT INTO orders VALUES (29,29,'Казань','2024-06-02','cancelled',129);\n"
           "INSERT INTO orders VALUES (30,30,'Тверь','2024-07-03','paid',130);\n"
           "INSERT INTO orders VALUES (31,31,'Омск','2024-08-04','new',131);\n"
           "INSERT INTO orders VALUES (32,32,'Москва','2024-09-05','cancelled',132);\n"
           "INSERT INTO orders VALUES (33,33,'Казань','2024-10-06','paid',133);\n"
           "INSERT INTO orders VALUES (34,34,'Тверь','2024-11-07','new',134);\n"
           "INSERT INTO orders VALUES (35,35,'Омск','2024-12-08','cancelled',135);\n"
           "INSERT INTO orders VALUES (36,36,'Москва','2024-01-09','paid',136);\n"
           "INSERT INTO orders VALUES (37,37,'Казань','2024-02-10','new',137);\n"
           "INSERT INTO orders VALUES (38,38,'Тверь','2024-03-11','cancelled',138);\n"
           "INSERT INTO orders VALUES (39,39,'Омск','2024-04-12','paid',139);\n"
           "INSERT INTO orders VALUES (40,40,'Москва','2024-05-13','new',140);\n"
           "INSERT INTO orders VALUES (41,41,'Казань','2024-06-14','cancelled',141);\n"
           "INSERT INTO orders VALUES (42,42,'Тверь','2024-07-15','paid',142);\n"
           "INSERT INTO orders VALUES (43,43,'Омск','2024-08-16','new',143);\n"
           "INSERT INTO orders VALUES (44,44,'Москва','2024-09-17','cancelled',144);\n"
           "INSERT INTO orders VALUES (45,45,'Казань','2024-10-18','paid',145);\n"
           "INSERT INTO orders VALUES (46,46,'Тверь','2024-11-19','new',146);\n"
           "INSERT INTO orders VALUES (47,47,'Омск','2024-12-20','cancelled',147);\n"
           "INSERT INTO orders VALUES (48,48,'Москва','2024-01-21','paid',148);\n"
           "INSERT INTO orders VALUES (49,49,'Казань','2024-02-22','new',149);\n"
           "INSERT INTO orders VALUES (50,0,'Тверь','2024-03-23','cancelled',150);\n"
           "INSERT INTO orders VALUES (51,1,'Омск','2024-04-24','paid',151);\n"
           "INSERT INTO orders VALUES (52,2,'Москва','2024-05-25','new',152);\n"
           "INSERT INTO orders VALUES (53,3,'Казань','2024-06-26','cancelled',153);\n"
           "INSERT INTO orders VALUES (54,4,'Тверь','2024-07-27','paid',154);\n"
           "INSERT INTO orders VALUES (55,5,'Омск','2024-08-28','new',155);\n"
           "INSERT INTO orders VALUES (56,6,'Москва','2024-09-01','cancelled',156);\n"
           "INSERT INTO orders VALUES (57,7,'Казань','2024-10-02','paid',157);\n"
           "INSERT INTO orders VALUES (58,8,'Тверь','2024-11-03','new',158);\n"
           "INSERT INTO orders VALUES (59,9,'Омск','2024-12-04','cancelled',159);\n"
           "INSERT INTO orders VALUES (60,10,'Москва','2024-01-05','paid',160);\n"
           "INSERT INTO orders VALUES (61,11,'Казань','2024-02-06','new',161);\n"
           "INSERT INTO orders VALUES (62,12,'Тверь','2024-03-07','cancelled',162);\n"
           "INSERT INTO orders VALUES (63,13,'Омск','2024-04-08','paid',163);\n"
           "INSERT INTO orders VALUES (64,14,'Москва','2024-05-09','new',164);\n"
           "INSERT INTO orders VALUES (65,15,'Казань','2024-06-10','cancelled',165);\n"
           "INSERT INTO orders VALUES (66,16,'Тверь','2024-07-11','paid',166);\n"
           "INSERT INTO orders VALUES (67,17,'Омск','2024-08-12','new',167);\n"
           "INSERT INTO orders VALUES (68,18,'Москва','2024-09-13','cancelled',168);\n"
           "INSERT INTO orders VALUES (69,19,'Казань','2024-10-14','paid',169);\n"
           "INSERT INTO orders VALUES (70,20,'Тверь','2024-11-15','new',170);\n"
           "INSERT INTO orders VALUES (71,21,'Омск','2024-12-16','cancelled',171);\n"
           "INSERT INTO orders VALUES (72,22,'Москва','2024-01-17','paid',172);\n"
           "INSERT INTO orders VALUES (73,23,'Казань','2024-02-18','new',173);\n"
           "INSERT INTO orders VALUES (74,24,'Тверь','2024-03-19','cancelled',174);\n"
           "INSERT INTO orders VALUES (75,25,'Омск','2024-04-20','paid',175);\n"
           "INSERT INTO orders VALUES (76,26,'Москва','2024-05-21','new',176);\n"
           "INSERT INTO orders VALUES (77,27,'Казань','2024-06-22','cancelled',177);\n"
           "INSERT INTO orders VALUES (78,28,'Тверь','2024-07-23','paid',178);\n"
           "INSERT INTO orders VALUES (79,29,'Омск','2024-08-24','new',179);\n"
           "INSERT INTO orders VALUES (80,30,'Москва','2024-09-25','cancelled',180);\n"
           "INSERT INTO orders VALUES (81,31,'Казань','2024-10-26','paid',181);\n"
           "INSERT INTO orders VALUES (82,32,'Тверь','2024-11-27','new',182);\n"
           "INSERT INTO orders VALUES (83,33,'Омск','2024-12-28','cancelled',183);\n"
           "INSERT INTO orders VALUES (84,34,'Москва','2024-01-01','paid',184);\n"
           "INSERT INTO orders VALUES (85,35,'Казань','2024-02-02','new',185);\n"
           "INSERT INTO orders VALUES (86,36,'Тверь','2024-03-03','cancelled',186);\n"
           "INSERT INTO orders VALUES (87,37,'Омск','2024-04-04','paid',187);\n"
           "INSERT INTO orders VALUES (88,38,'Москва','2024-05-05','new',188);\n"
           "INSERT INTO orders VALUES (89,39,'Казань','2024-06-06','cancelled',189);\n"
           "INSERT INTO orders VALUES (90,40,'Тверь','2024-07-07','paid',190);\n"
           "INSERT INTO orders VALUES (91,41,'Омск','2024-08-08','new',191);\n"
           "INSERT INTO orders VALUES (92,42,'Москва','2024-09-09','cancelled',192);\n"
           "INSERT INTO orders VALUES (93,43,'Казань','2024-10-10','paid',193);\n"
           "INSERT INTO orders VALUES (94,44,'Тверь','2024-11-11','new',194);\n"
           "INSERT INTO orders VALUES (95,45,'Омск','2024-12-12','cancelled',195);\n"
           "INSERT INTO orders VALUES (96,46,'Москва','2024-01-13','paid',196);\n"
           "INSERT INTO orders VALUES (97,47,'Казань','2024-02-14','new',197);\n"
           "INSERT INTO orders VALUES (98,48,'Тверь','2024-03-15','cancelled',198);\n"
           "INSERT INTO orders VALUES (99,49,'Омск','2024-04-16','paid',199);\n"
           "INSERT INTO orders VALUES (100,0,'Москва','2024-05-17','new',200);\n"
           "INSERT INTO orders VALUES (101,1,'Казань','2024-06-18','cancelled',201);\n"
           "INSERT INTO orders VALUES (102,2,'Тверь','2024-07-19','paid',202);\n"
           "INSERT INTO orders VALUES (103,3,'Омск','2024-08-20','new',203);\n"
           "INSERT INTO orders VALUES (104,4,'Москва','2024-09-21','cancelled',204);\n"
           "INSERT INTO orders VALUES (105,5,'Казань','2024-10-22','paid',205);\n"
           "INSERT INTO orders VALUES (106,6,'Тверь','2024-11-23','new',206);\n"
           "INSERT INTO orders VALUES (107,7,'Омск','2024-12-24','cancelled',207);\n"
           "INSERT INTO orders VALUES (108,8,'Москва','2024-01-25','paid',208);\n"
           "INSERT INTO orders VALUES (109,9,'Казань','2024-02-26','new',209);\n"
           "INSERT INTO orders VALUES (110,10,'Тверь','2024-03-27','cancelled',210);\n"
           "INSERT INTO orders VALUES (111,11,'Омск','2024-04-28','paid',211);\n"
           "INSERT INTO orders VALUES (112,12,'Москва','2024-05-01','new',212);\n"
           "INSERT INTO orders VALUES (113,13,'Казань','2024-06-02','cancelled',213);\n"
           "INSERT INTO orders VALUES (114,14,'Тверь','2024-07-03','paid',214);\n"
           "INSERT INTO orders VALUES (115,15,'Омск','2024-08-04','new',215);\n"
           "INSERT INTO orders VALUES (116,16,'Москва','2024-09-05','cancelled',216);\n"
           "INSERT INTO orders VALUES (117,17,'Казань','2024-10-06','paid',217);\n"
           "INSERT INTO orders VALUES (118,18,'Тверь','2024-11-07','new',218);\n"
           "INSERT INTO orders VALUES (119,19,'Омск','2024-12-08','cancelled',219);\n"
           "INSERT INTO orders VALUES (120,20,'Москва','2024-01-09','paid',220);\n"
           "INSERT INTO orders VALUES (121,21,'Казань','2024-02-10','new',221);\n"
           "INSERT INTO orders VALUES (122,22,'Тверь','2024-03-11','cancelled',222);\n"
           "INSERT INTO orders VALUES (123,23,'Омск','2024-04-12','paid',223);\n"
           "INSERT INTO orders VALUES (124,24,'Москва','2024-05-13','new',224);\n"
           "INSERT INTO orders VALUES (125,25,'Казань','2024-06-14','cancelled',225);\n"
           "INSERT INTO orders VALUES (126,26,'Тверь','2024-07-15','paid',226);\n"
           "INSERT INTO orders VALUES (127,27,'Омск','2024-08-16','new',227);\n"
           "INSERT INTO orders VALUES (128,28,'Москва','2024-09-17','cancelled',228);\n"
           "INSERT INTO orders VALUES (129,29,'Казань','2024-10-18','paid',229);\n"
           "INSERT INTO orders VALUES (130,30,'Тверь','2024-11-19','new',230);\n"
           "INSERT INTO orders VALUES (131,31,'Омск','2024-12-20','cancelled',231);\n"
           "INSERT INTO orders VALUES (132,32,'Москва','2024-01-21','paid',232);\n"
           "INSERT INTO orders VALUES (133,33,'Казань','2024-02-22','new',233);\n"
           "INSERT INTO orders VALUES (134,34,'Тверь','2024-03-23','cancelled',234);\n"
           "INSERT INTO orders VALUES (135,35,'Омск','2024-04-24','paid',235);\n"
           "INSERT INTO orders VALUES (136,36,'Москва','2024-05-25','new',236);\n"
           "INSERT INTO orders VALUES (137,37,'Казань','2024-06-26','cancelled',237);\n"
           "INSERT INTO orders VALUES (138,38,'Тверь','2024-07-27','paid',238);\n"
           "INSERT INTO orders VALUES (139,39,'Омск','2024-08-28','new',239);\n"
           "INSERT INTO orders VALUES (140,40,'Москва','2024-09-01','cancelled',240);\n"
           "INSERT INTO orders VALUES (141,41,'Казань','2024-10-02','paid',241);\n"
           "INSERT INTO orders VALUES (142,42,'Тверь','2024-11-03','new',242);\n"
           "INSERT INTO orders VALUES (143,43,'Омск','2024-12-04','cancelled',243);\n"
           "INSERT INTO orders VALUES (144,44,'Москва','2024-01-05','paid',244);\n"
           "INSERT INTO orders VALUES (145,45,'Казань','2024-02-06','new',245);\n"
           "INSERT INTO orders VALUES (146,46,'Тверь','2024-03-07','cancelled',246);\n"
           "INSERT INTO orders VALUES (147,47,'Омск','2024-04-08','paid',247);\n"
           "INSERT INTO orders VALUES (148,48,'Москва','2024-05-09','new',248);\n"
           "INSERT INTO orders VALUES (149,49,'Казань','2024-06-10','cancelled',249);\n"
           "INSERT INTO orders VALUES (150,0,'Тверь','2024-07-11','paid',250);\n"
           "INSERT INTO orders VALUES (151,1,'Омск','2024-08-12','new',251);\n"
           "INSERT INTO orders VALUES (152,2,'Москва','2024-09-13','cancelled',252);\n"
           "INSERT INTO orders VALUES (153,3,'Казань','2024-10-14','paid',253);\n"
           "INSERT INTO orders VALUES (154,4,'Тверь','2024-11-15','new',254);\n"
           "INSERT INTO orders VALUES (155,5,'Омск','2024-12-16','cancelled',255);\n"
           "INSERT INTO orders VALUES (156,6,'Москва','2024-01-17','paid',256);\n"
           "INSERT INTO orders VALUES (157,7,'Казань','2024-02-18','new',257);\n"
           "INSERT INTO orders VALUES (158,8,'Тверь','2024-03-19','cancelled',258);\n"
           "INSERT INTO orders VALUES (159,9,'Омск','2024-04-20','paid',259);\n"
           "INSERT INTO orders VALUES (160,10,'Москва','2024-05-21','new',260);\n"
           "INSERT INTO orders VALUES (161,11,'Казань','2024-06-22','cancelled',261);\n"
           "INSERT INTO orders VALUES (162,12,'Тверь','2024-07-23','paid',262);\n"
           "INSERT INTO orders VALUES (163,13,'Омск','2024-08-24','new',263);\n"
           "INSERT INTO orders VALUES (164,14,'Москва','2024-09-25','cancelled',264);\n"
           "INSERT INTO orders VALUES (165,15,'Казань','2024-10-26','paid',265);\n"
           "INSERT INTO orders VALUES (166,16,'Тверь','2024-11-27','new',266);\n"
           "INSERT INTO orders VALUES (167,17,'Омск','2024-12-28','cancelled',267);\n"
           "INSERT INTO orders VALUES (168,18,'Москва','2024-01-01','paid',268);\n"
           "INSERT INTO orders VALUES (169,19,'Казань','2024-02-02','new',269);\n"
           "INSERT INTO orders VALUES (170,20,'Тверь','2024-03-03','cancelled',270);\n"
           "INSERT INTO orders VALUES (171,21,'Омск','2024-04-04','paid',271);\n"
           "INSERT INTO orders VALUES (172,22,'Москва','2024-05-05','new',272);\n"
           "INSERT INTO orders VALUES (173,23,'Казань','2024-06-06','cancelled',273);\n"
           "INSERT INTO orders VALUES (174,24,'Тверь','2024-07-07','paid',274);\n"
           "INSERT INTO orders VALUES (175,25,'Омск','2024-08-08','new',275);\n"
           "INSERT INTO orders VALUES (176,26,'Москва','2024-09-09','cancelled',276);\n"
           "INSERT INTO orders VALUES (177,27,'Казань','2024-10-10','paid',277);\n"
           "INSERT INTO orders VALUES (178,28,'Тверь','2024-11-11','new',278);\n"
           "INSERT INTO orders VALUES (179,29,'Омск','2024-12-12','cancelled',279);\n"
           "INSERT INTO orders VALUES (180,30,'Москва','2024-01-13','paid',280);\n"
           "INSERT INTO orders VALUES (181,31,'Казань','2024-02-14','new',281);\n"
           "INSERT INTO orders VALUES (182,32,'Тверь','2024-03-15','cancelled',282);\n"
           "INSERT INTO orders VALUES (183,33,'Омск','2024-04-16','paid',283);\n"
           "INSERT INTO orders VALUES (184,34,'Москва','2024-05-17','new',284);\n"
           "INSERT INTO orders VALUES (185,35,'Казань','2024-06-18','cancelled',285);\n"
           "INSERT INTO orders VALUES (186,36,'Тверь','2024-07-19','paid',286);\n"
           "INSERT INTO orders VALUES (187,37,'Омск','2024-08-20','new',287);\n"
           "INSERT INTO orders VALUES (188,38,'Москва','2024-09-21','cancelled',288);\n"
           "INSERT INTO orders VALUES (189,39,'Казань','2024-10-22','paid',289);\n"
           "INSERT INTO orders VALUES (190,40,'Тверь','2024-11-23','new',290);\n"
           "INSERT INTO orders VALUES (191,41,'Омск','2024-12-24','cancelled',291);\n"
           "INSERT INTO orders VALUES (192,42,'Москва','2024-01-25','paid',292);\n"
           "INSERT INTO orders VALUES (193,43,'Казань','2024-02-26','new',293);\n"
           "INSERT INTO orders VALUES (194,44,'Тверь','2024-03-27','cancelled',294);\n"
           "INSERT INTO orders VALUES (195,45,'Омск','2024-04-28','paid',295);\n"
           "INSERT INTO orders VALUES (196,46,'Москва','2024-05-01','new',296);\n"
           "INSERT INTO orders VALUES (197,47,'Казань','2024-06-02','cancelled',297);\n"
           "INSERT INTO orders VALUES (198,48,'Тверь','2024-07-03','paid',298);\n"
           "INSERT INTO orders VALUES (199,49,'Омск','2024-08-04','new',299);\n"
           "INSERT INTO orders VALUES (200,0,'Москва','2024-09-05','cancelled',300);\n"
           "INSERT INTO orders VALUES (201,1,'Казань','2024-10-06','paid',301);\n"
           "INSERT INTO orders VALUES (202,2,'Тверь','2024-11-07','new',302);\n"
           "INSERT INTO orders VALUES (203,3,'Омск','2024-12-08','cancelled',303);\n"
           "INSERT INTO orders VALUES (204,4,'Москва','2024-01-09','paid',304);\n"
           "INSERT INTO orders VALUES (205,5,'Казань','2024-02-10','new',305);\n"
           "INSERT INTO orders VALUES (206,6,'Тверь','2024-03-11','cancelled',306);\n"
           "INSERT INTO orders VALUES (207,7,'Омск','2024-04-12','paid',307);\n"
           "INSERT INTO orders VALUES (208,8,'Москва','2024-05-13','new',308);\n"
           "INSERT INTO orders VALUES (209,9,'Казань','2024-06-14','cancelled',309);\n"
           "INSERT INTO orders VALUES (210,10,'Тверь','2024-07-15','paid',310);\n"
           "INSERT INTO orders VALUES (211,11,'Омск','2024-08-16','new',311);\n"
           "INSERT INTO orders VALUES (212,12,'Москва','2024-09-17','cancelled',312);\n"
           "INSERT INTO orders VALUES (213,13,'Казань','2024-10-18','paid',313);\n"
           "INSERT INTO orders VALUES (214,14,'Тверь','2024-11-19','new',314);\n"
           "INSERT INTO orders VALUES (215,15,'Омск','2024-12-20','cancelled',315);\n"
           "INSERT INTO orders VALUES (216,16,'Москва','2024-01-21','paid',316);\n"
           "INSERT INTO orders VALUES (217,17,'Казань','2024-02-22','new',317);\n"
           "INSERT INTO orders VALUES (218,18,'Тверь','2024-03-23','cancelled',318);\n"
           "INSERT INTO orders VALUES (219,19,'Омск','2024-04-24','paid',319);\n"
           "INSERT INTO orders VALUES (220,20,'Москва','2024-05-25','new',320);\n"
           "INSERT INTO orders VALUES (221,21,'Казань','2024-06-26','cancelled',321);\n"
           "INSERT INTO orders VALUES (222,22,'Тверь','2024-07-27','paid',322);\n"
           "INSERT INTO orders VALUES (223,23,'Омск','2024-08-28','new',323);\n"
           "INSERT INTO orders VALUES (224,24,'Москва','2024-09-01','cancelled',324);\n"
           "INSERT INTO orders VALUES (225,25,'Казань','2024-10-02','paid',325);\n"
           "INSERT INTO orders VALUES (226,26,'Тверь','2024-11-03','new',326);\n"
           "INSERT INTO orders VALUES (227,27,'Омск','2024-12-04','cancelled',327);\n"
           "INSERT INTO orders VALUES (228,28,'Москва','2024-01-05','paid',328);\n"
           "INSERT INTO orders VALUES (229,29,'Казань','2024-02-06','new',329);\n"
           "INSERT INTO orders VALUES (230,30,'Тверь','2024-03-07','cancelled',330);\n"
           "INSERT INTO orders VALUES (231,31,'Омск','2024-04-08','paid',331);\n"
           "INSERT INTO orders VALUES (232,32,'Москва','2024-05-09','new',332);\n"
           "INSERT INTO orders VALUES (233,33,'Казань','2024-06-10','cancelled',333);\n"
           "INSERT INTO orders VALUES (234,34,'Тверь','2024-07-11','paid',334);\n"
           "INSERT INTO orders VALUES (235,35,'Омск','2024-08-12','new',335);\n"
           "INSERT INTO orders VALUES (236,36,'Москва','2024-09-13','cancelled',336);\n"
           "INSERT INTO orders VALUES (237,37,'Казань','2024-10-14','paid',337);\n"
           "INSERT INTO orders VALUES (238,38,'Тверь','2024-11-15','new',338);\n"
           "INSERT INTO orders VALUES (239,39,'Омск','2024-12-16','cancelled',339);\n"
           "INSERT INTO orders VALUES (240,40,'Москва','2024-01-17','paid',340);\n"
           "INSERT INTO orders VALUES (241,41,'Казань','2024-02-18','new',341);\n"
           "INSERT INTO orders VALUES (242,42,'Тверь','2024-03-19','cancelled',342);\n"
           "INSERT INTO orders VALUES (243,43,'Омск','2024-04-20','paid',343);\n"
           "INSERT INTO orders VALUES (244,44,'Москва','2024-05-21','new',344);\n"
           "INSERT INTO orders VALUES (245,45,'Казань','2024-06-22','cancelled',345);\n"
           "INSERT INTO orders VALUES (246,46,'Тверь','2024-07-23','paid',346);\n"
           "INSERT INTO orders VALUES (247,47,'Омск','2024-08-24','new',347);\n"
           "INSERT INTO orders VALUES (248,48,'Москва','2024-09-25','cancelled',348);\n"
           "INSERT INTO orders VALUES (249,49,'Казань','2024-10-26','paid',349);\n"
           "INSERT INTO orders VALUES (250,0,'Тверь','2024-11-27','new',350);\n"
           "INSERT INTO orders VALUES (251,1,'Омск','2024-12-28','cancelled',351);\n"
           "INSERT INTO orders VALUES (252,2,'Москва','2024-01-01','paid',352);\n"
           "INSERT INTO orders VALUES (253,3,'Казань','2024-02-02','new',353);\n"
           "INSERT INTO orders VALUES (254,4,'Тверь','2024-03-03','cancelled',354);\n"
           "INSERT INTO orders VALUES (255,5,'Омск','2024-04-04','paid',355);\n"
           "INSERT INTO orders VALUES (256,6,'Москва','2024-05-05','new',356);\n"
           "INSERT INTO orders VALUES (257,7,'Казань','2024-06-06','cancelled',357);\n"
           "INSERT INTO orders VALUES (258,8,'Тверь','2024-07-07','paid',358);\n"
           "INSERT INTO orders VALUES (259,9,'Омск','2024-08-08','new',359);\n"
           "INSERT INTO orders VALUES (260,10,'Москва','2024-09-09','cancelled',360);\n"
           "INSERT INTO orders VALUES (261,11,'Казань','2024-10-10','paid',361);\n"
           "INSERT INTO orders VALUES (262,12,'Тверь','2024-11-11','new',362);\n"
           "INSERT INTO orders VALUES (263,13,'Омск','2024-12-12','cancelled',363);\n"
           "INSERT INTO orders VALUES (264,14,'Москва','2024-01-13','paid',364);\n"
           "INSERT INTO orders VALUES (265,15,'Казань','2024-02-14','new',365);\n"
           "INSERT INTO orders VALUES (266,16,'Тверь','2024-03-15','cancelled',366);\n"
           "INSERT INTO orders VALUES (267,17,'Омск','2024-04-16','paid',367);\n"
           "INSERT INTO orders VALUES (268,18,'Москва','2024-05-17','new',368);\n"
           "INSERT INTO orders VALUES (269,19,'Казань','2024-06-18','cancelled',369);\n"
           "INSERT INTO orders VALUES (270,20,'Тверь','2024-07-19','paid',370);\n"
           "INSERT INTO orders VALUES (271,21,'Омск','2024-08-20','new',371);\n"
           "INSERT INTO orders VALUES (272,22,'Москва','2024-09-21','cancelled',372);\n"
           "INSERT INTO orders VALUES (273,23,'Казань','2024-10-22','paid',373);\n"
           "INSERT INTO orders VALUES (274,24,'Тверь','2024-11-23','new',374);\n"
           "INSERT INTO orders VALUES (275,25,'Омск','2024-12-24','cancelled',375);\n"
           "INSERT INTO orders VALUES (276,26,'Москва','2024-01-25','paid',376);\n"
           "INSERT INTO orders VALUES (277,27,'Казань','2024-02-26','new',377);\n"
           "INSERT INTO orders VALUES (278,28,'Тверь','2024-03-27','cancelled',378);\n"
           "INSERT INTO orders VALUES (279,29,'Омск','2024-04-28','paid',379);\n"
           "INSERT INTO orders VALUES (280,30,'Москва','2024-05-01','new',380);\n"
           "INSERT INTO orders VALUES (281,31,'Казань','2024-06-02','cancelled',381);\n"
           "INSERT INTO orders VALUES (282,32,'Тверь','2024-07-03','paid',382);\n"
           "INSERT INTO orders VALUES (283,33,'Омск','2024-08-04','new',383);\n"
           "INSERT INTO orders VALUES (284,34,'Москва','2024-09-05','cancelled',384);\n"
           "INSERT INTO orders VALUES (285,35,'Казань','2024-10-06','paid',385);\n"
           "INSERT INTO orders VALUES (286,36,'Тверь','2024-11-07','new',386);\n"
           "INSERT INTO orders VALUES (287,37,'Омск','2024-12-08','cancelled',387);\n"
           "INSERT INTO orders VALUES (288,38,'Москва','2024-01-09','paid',388);\n"
           "INSERT INTO orders VALUES (289,39,'Казань','2024-02-10','new',389);\n"
           "INSERT INTO orders VALUES (290,40,'Тверь','2024-03-11','cancelled',390);\n"
           "INSERT INTO orders VALUES (291,41,'Омск','2024-04-12','paid',391);\n"
           "INSERT INTO orders VALUES (292,42,'Москва','2024-05-13','new',392);\n"
           "INSERT INTO orders VALUES (293,43,'Казань','2024-06-14','cancelled',393);\n"
           "INSERT INTO orders VALUES (294,44,'Тверь','2024-07-15','paid',394);\n"
           "INSERT INTO orders VALUES (295,45,'Омск','2024-08-16','new',395);\n"
           "INSERT INTO orders VALUES (296,46,'Москва','2024-09-17','cancelled',396);\n"
           "INSERT INTO orders VALUES (297,47,'Казань','2024-10-18','paid',397);\n"
           "INSERT INTO orders VALUES (298,48,'Тверь','2024-11-19','new',398);\n"
           "INSERT INTO orders VALUES (299,49,'Омск','2024-12-20','cancelled',399);\n"
           "INSERT INTO orders VALUES (300,0,'Москва','2024-01-21','paid',400);\n",
  'expected': [[3, 0, 61, 'SEARCH orders USING INDEX idx_orders_customer (customer_id=?)']],
  'hint': 'CREATE INDEX имя ON orders (customer_id);',
  'check': 'EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 7',
  'contains': ['SEARCH orders USING INDEX'],
  'forbid': ['SCAN']},
 {'id': 'd3-unique-index',
  'mode': 'sql',
  'title': 'Уникальный индекс',
  'statement': 'Адреса электронной почты в users должны быть уникальными, а поиск по ним — быстрым. Создайте '
               'один уникальный индекс по email.',
  'starter': '-- уникальный индекс по email\nCREATE\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT);\n'
           "INSERT INTO users VALUES (1,'a@x.ru','Анна'),(2,'b@x.ru','Борис'),(3,'c@x.ru','Вера');\n",
  'expected': [[1, 'c']],
  'expected_cols': ['unique', 'origin'],
  'hint': 'CREATE UNIQUE INDEX … ON users (email);',
  'ordered': True,
  'check': 'SELECT "unique", origin FROM pragma_index_list(\'users\') WHERE name NOT LIKE '
           "'sqlite_autoindex%'"},
 {'id': 'd3-composite-order',
  'mode': 'sql',
  'title': 'Порядок столбцов в составном индексе',
  'statement': "Частый запрос: WHERE city = 'Москва' AND created >= '2024-06-01'. Создайте составной индекс "
               'так, чтобы по нему искали и по городу (равенство), и по дате (диапазон) — порядок столбцов '
               'выберите сами.',
  'starter': '-- составной индекс для city (=) и created (>=)\nCREATE INDEX\n',
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, city TEXT NOT NULL, '
           'created TEXT NOT NULL, status TEXT NOT NULL, total INTEGER NOT NULL);\n'
           "INSERT INTO orders VALUES (1,1,'Казань','2024-02-02','new',101);\n"
           "INSERT INTO orders VALUES (2,2,'Тверь','2024-03-03','cancelled',102);\n"
           "INSERT INTO orders VALUES (3,3,'Омск','2024-04-04','paid',103);\n"
           "INSERT INTO orders VALUES (4,4,'Москва','2024-05-05','new',104);\n"
           "INSERT INTO orders VALUES (5,5,'Казань','2024-06-06','cancelled',105);\n"
           "INSERT INTO orders VALUES (6,6,'Тверь','2024-07-07','paid',106);\n"
           "INSERT INTO orders VALUES (7,7,'Омск','2024-08-08','new',107);\n"
           "INSERT INTO orders VALUES (8,8,'Москва','2024-09-09','cancelled',108);\n"
           "INSERT INTO orders VALUES (9,9,'Казань','2024-10-10','paid',109);\n"
           "INSERT INTO orders VALUES (10,10,'Тверь','2024-11-11','new',110);\n"
           "INSERT INTO orders VALUES (11,11,'Омск','2024-12-12','cancelled',111);\n"
           "INSERT INTO orders VALUES (12,12,'Москва','2024-01-13','paid',112);\n"
           "INSERT INTO orders VALUES (13,13,'Казань','2024-02-14','new',113);\n"
           "INSERT INTO orders VALUES (14,14,'Тверь','2024-03-15','cancelled',114);\n"
           "INSERT INTO orders VALUES (15,15,'Омск','2024-04-16','paid',115);\n"
           "INSERT INTO orders VALUES (16,16,'Москва','2024-05-17','new',116);\n"
           "INSERT INTO orders VALUES (17,17,'Казань','2024-06-18','cancelled',117);\n"
           "INSERT INTO orders VALUES (18,18,'Тверь','2024-07-19','paid',118);\n"
           "INSERT INTO orders VALUES (19,19,'Омск','2024-08-20','new',119);\n"
           "INSERT INTO orders VALUES (20,20,'Москва','2024-09-21','cancelled',120);\n"
           "INSERT INTO orders VALUES (21,21,'Казань','2024-10-22','paid',121);\n"
           "INSERT INTO orders VALUES (22,22,'Тверь','2024-11-23','new',122);\n"
           "INSERT INTO orders VALUES (23,23,'Омск','2024-12-24','cancelled',123);\n"
           "INSERT INTO orders VALUES (24,24,'Москва','2024-01-25','paid',124);\n"
           "INSERT INTO orders VALUES (25,25,'Казань','2024-02-26','new',125);\n"
           "INSERT INTO orders VALUES (26,26,'Тверь','2024-03-27','cancelled',126);\n"
           "INSERT INTO orders VALUES (27,27,'Омск','2024-04-28','paid',127);\n"
           "INSERT INTO orders VALUES (28,28,'Москва','2024-05-01','new',128);\n"
           "INSERT INTO orders VALUES (29,29,'Казань','2024-06-02','cancelled',129);\n"
           "INSERT INTO orders VALUES (30,30,'Тверь','2024-07-03','paid',130);\n"
           "INSERT INTO orders VALUES (31,31,'Омск','2024-08-04','new',131);\n"
           "INSERT INTO orders VALUES (32,32,'Москва','2024-09-05','cancelled',132);\n"
           "INSERT INTO orders VALUES (33,33,'Казань','2024-10-06','paid',133);\n"
           "INSERT INTO orders VALUES (34,34,'Тверь','2024-11-07','new',134);\n"
           "INSERT INTO orders VALUES (35,35,'Омск','2024-12-08','cancelled',135);\n"
           "INSERT INTO orders VALUES (36,36,'Москва','2024-01-09','paid',136);\n"
           "INSERT INTO orders VALUES (37,37,'Казань','2024-02-10','new',137);\n"
           "INSERT INTO orders VALUES (38,38,'Тверь','2024-03-11','cancelled',138);\n"
           "INSERT INTO orders VALUES (39,39,'Омск','2024-04-12','paid',139);\n"
           "INSERT INTO orders VALUES (40,40,'Москва','2024-05-13','new',140);\n"
           "INSERT INTO orders VALUES (41,41,'Казань','2024-06-14','cancelled',141);\n"
           "INSERT INTO orders VALUES (42,42,'Тверь','2024-07-15','paid',142);\n"
           "INSERT INTO orders VALUES (43,43,'Омск','2024-08-16','new',143);\n"
           "INSERT INTO orders VALUES (44,44,'Москва','2024-09-17','cancelled',144);\n"
           "INSERT INTO orders VALUES (45,45,'Казань','2024-10-18','paid',145);\n"
           "INSERT INTO orders VALUES (46,46,'Тверь','2024-11-19','new',146);\n"
           "INSERT INTO orders VALUES (47,47,'Омск','2024-12-20','cancelled',147);\n"
           "INSERT INTO orders VALUES (48,48,'Москва','2024-01-21','paid',148);\n"
           "INSERT INTO orders VALUES (49,49,'Казань','2024-02-22','new',149);\n"
           "INSERT INTO orders VALUES (50,0,'Тверь','2024-03-23','cancelled',150);\n"
           "INSERT INTO orders VALUES (51,1,'Омск','2024-04-24','paid',151);\n"
           "INSERT INTO orders VALUES (52,2,'Москва','2024-05-25','new',152);\n"
           "INSERT INTO orders VALUES (53,3,'Казань','2024-06-26','cancelled',153);\n"
           "INSERT INTO orders VALUES (54,4,'Тверь','2024-07-27','paid',154);\n"
           "INSERT INTO orders VALUES (55,5,'Омск','2024-08-28','new',155);\n"
           "INSERT INTO orders VALUES (56,6,'Москва','2024-09-01','cancelled',156);\n"
           "INSERT INTO orders VALUES (57,7,'Казань','2024-10-02','paid',157);\n"
           "INSERT INTO orders VALUES (58,8,'Тверь','2024-11-03','new',158);\n"
           "INSERT INTO orders VALUES (59,9,'Омск','2024-12-04','cancelled',159);\n"
           "INSERT INTO orders VALUES (60,10,'Москва','2024-01-05','paid',160);\n"
           "INSERT INTO orders VALUES (61,11,'Казань','2024-02-06','new',161);\n"
           "INSERT INTO orders VALUES (62,12,'Тверь','2024-03-07','cancelled',162);\n"
           "INSERT INTO orders VALUES (63,13,'Омск','2024-04-08','paid',163);\n"
           "INSERT INTO orders VALUES (64,14,'Москва','2024-05-09','new',164);\n"
           "INSERT INTO orders VALUES (65,15,'Казань','2024-06-10','cancelled',165);\n"
           "INSERT INTO orders VALUES (66,16,'Тверь','2024-07-11','paid',166);\n"
           "INSERT INTO orders VALUES (67,17,'Омск','2024-08-12','new',167);\n"
           "INSERT INTO orders VALUES (68,18,'Москва','2024-09-13','cancelled',168);\n"
           "INSERT INTO orders VALUES (69,19,'Казань','2024-10-14','paid',169);\n"
           "INSERT INTO orders VALUES (70,20,'Тверь','2024-11-15','new',170);\n"
           "INSERT INTO orders VALUES (71,21,'Омск','2024-12-16','cancelled',171);\n"
           "INSERT INTO orders VALUES (72,22,'Москва','2024-01-17','paid',172);\n"
           "INSERT INTO orders VALUES (73,23,'Казань','2024-02-18','new',173);\n"
           "INSERT INTO orders VALUES (74,24,'Тверь','2024-03-19','cancelled',174);\n"
           "INSERT INTO orders VALUES (75,25,'Омск','2024-04-20','paid',175);\n"
           "INSERT INTO orders VALUES (76,26,'Москва','2024-05-21','new',176);\n"
           "INSERT INTO orders VALUES (77,27,'Казань','2024-06-22','cancelled',177);\n"
           "INSERT INTO orders VALUES (78,28,'Тверь','2024-07-23','paid',178);\n"
           "INSERT INTO orders VALUES (79,29,'Омск','2024-08-24','new',179);\n"
           "INSERT INTO orders VALUES (80,30,'Москва','2024-09-25','cancelled',180);\n"
           "INSERT INTO orders VALUES (81,31,'Казань','2024-10-26','paid',181);\n"
           "INSERT INTO orders VALUES (82,32,'Тверь','2024-11-27','new',182);\n"
           "INSERT INTO orders VALUES (83,33,'Омск','2024-12-28','cancelled',183);\n"
           "INSERT INTO orders VALUES (84,34,'Москва','2024-01-01','paid',184);\n"
           "INSERT INTO orders VALUES (85,35,'Казань','2024-02-02','new',185);\n"
           "INSERT INTO orders VALUES (86,36,'Тверь','2024-03-03','cancelled',186);\n"
           "INSERT INTO orders VALUES (87,37,'Омск','2024-04-04','paid',187);\n"
           "INSERT INTO orders VALUES (88,38,'Москва','2024-05-05','new',188);\n"
           "INSERT INTO orders VALUES (89,39,'Казань','2024-06-06','cancelled',189);\n"
           "INSERT INTO orders VALUES (90,40,'Тверь','2024-07-07','paid',190);\n"
           "INSERT INTO orders VALUES (91,41,'Омск','2024-08-08','new',191);\n"
           "INSERT INTO orders VALUES (92,42,'Москва','2024-09-09','cancelled',192);\n"
           "INSERT INTO orders VALUES (93,43,'Казань','2024-10-10','paid',193);\n"
           "INSERT INTO orders VALUES (94,44,'Тверь','2024-11-11','new',194);\n"
           "INSERT INTO orders VALUES (95,45,'Омск','2024-12-12','cancelled',195);\n"
           "INSERT INTO orders VALUES (96,46,'Москва','2024-01-13','paid',196);\n"
           "INSERT INTO orders VALUES (97,47,'Казань','2024-02-14','new',197);\n"
           "INSERT INTO orders VALUES (98,48,'Тверь','2024-03-15','cancelled',198);\n"
           "INSERT INTO orders VALUES (99,49,'Омск','2024-04-16','paid',199);\n"
           "INSERT INTO orders VALUES (100,0,'Москва','2024-05-17','new',200);\n"
           "INSERT INTO orders VALUES (101,1,'Казань','2024-06-18','cancelled',201);\n"
           "INSERT INTO orders VALUES (102,2,'Тверь','2024-07-19','paid',202);\n"
           "INSERT INTO orders VALUES (103,3,'Омск','2024-08-20','new',203);\n"
           "INSERT INTO orders VALUES (104,4,'Москва','2024-09-21','cancelled',204);\n"
           "INSERT INTO orders VALUES (105,5,'Казань','2024-10-22','paid',205);\n"
           "INSERT INTO orders VALUES (106,6,'Тверь','2024-11-23','new',206);\n"
           "INSERT INTO orders VALUES (107,7,'Омск','2024-12-24','cancelled',207);\n"
           "INSERT INTO orders VALUES (108,8,'Москва','2024-01-25','paid',208);\n"
           "INSERT INTO orders VALUES (109,9,'Казань','2024-02-26','new',209);\n"
           "INSERT INTO orders VALUES (110,10,'Тверь','2024-03-27','cancelled',210);\n"
           "INSERT INTO orders VALUES (111,11,'Омск','2024-04-28','paid',211);\n"
           "INSERT INTO orders VALUES (112,12,'Москва','2024-05-01','new',212);\n"
           "INSERT INTO orders VALUES (113,13,'Казань','2024-06-02','cancelled',213);\n"
           "INSERT INTO orders VALUES (114,14,'Тверь','2024-07-03','paid',214);\n"
           "INSERT INTO orders VALUES (115,15,'Омск','2024-08-04','new',215);\n"
           "INSERT INTO orders VALUES (116,16,'Москва','2024-09-05','cancelled',216);\n"
           "INSERT INTO orders VALUES (117,17,'Казань','2024-10-06','paid',217);\n"
           "INSERT INTO orders VALUES (118,18,'Тверь','2024-11-07','new',218);\n"
           "INSERT INTO orders VALUES (119,19,'Омск','2024-12-08','cancelled',219);\n"
           "INSERT INTO orders VALUES (120,20,'Москва','2024-01-09','paid',220);\n"
           "INSERT INTO orders VALUES (121,21,'Казань','2024-02-10','new',221);\n"
           "INSERT INTO orders VALUES (122,22,'Тверь','2024-03-11','cancelled',222);\n"
           "INSERT INTO orders VALUES (123,23,'Омск','2024-04-12','paid',223);\n"
           "INSERT INTO orders VALUES (124,24,'Москва','2024-05-13','new',224);\n"
           "INSERT INTO orders VALUES (125,25,'Казань','2024-06-14','cancelled',225);\n"
           "INSERT INTO orders VALUES (126,26,'Тверь','2024-07-15','paid',226);\n"
           "INSERT INTO orders VALUES (127,27,'Омск','2024-08-16','new',227);\n"
           "INSERT INTO orders VALUES (128,28,'Москва','2024-09-17','cancelled',228);\n"
           "INSERT INTO orders VALUES (129,29,'Казань','2024-10-18','paid',229);\n"
           "INSERT INTO orders VALUES (130,30,'Тверь','2024-11-19','new',230);\n"
           "INSERT INTO orders VALUES (131,31,'Омск','2024-12-20','cancelled',231);\n"
           "INSERT INTO orders VALUES (132,32,'Москва','2024-01-21','paid',232);\n"
           "INSERT INTO orders VALUES (133,33,'Казань','2024-02-22','new',233);\n"
           "INSERT INTO orders VALUES (134,34,'Тверь','2024-03-23','cancelled',234);\n"
           "INSERT INTO orders VALUES (135,35,'Омск','2024-04-24','paid',235);\n"
           "INSERT INTO orders VALUES (136,36,'Москва','2024-05-25','new',236);\n"
           "INSERT INTO orders VALUES (137,37,'Казань','2024-06-26','cancelled',237);\n"
           "INSERT INTO orders VALUES (138,38,'Тверь','2024-07-27','paid',238);\n"
           "INSERT INTO orders VALUES (139,39,'Омск','2024-08-28','new',239);\n"
           "INSERT INTO orders VALUES (140,40,'Москва','2024-09-01','cancelled',240);\n"
           "INSERT INTO orders VALUES (141,41,'Казань','2024-10-02','paid',241);\n"
           "INSERT INTO orders VALUES (142,42,'Тверь','2024-11-03','new',242);\n"
           "INSERT INTO orders VALUES (143,43,'Омск','2024-12-04','cancelled',243);\n"
           "INSERT INTO orders VALUES (144,44,'Москва','2024-01-05','paid',244);\n"
           "INSERT INTO orders VALUES (145,45,'Казань','2024-02-06','new',245);\n"
           "INSERT INTO orders VALUES (146,46,'Тверь','2024-03-07','cancelled',246);\n"
           "INSERT INTO orders VALUES (147,47,'Омск','2024-04-08','paid',247);\n"
           "INSERT INTO orders VALUES (148,48,'Москва','2024-05-09','new',248);\n"
           "INSERT INTO orders VALUES (149,49,'Казань','2024-06-10','cancelled',249);\n"
           "INSERT INTO orders VALUES (150,0,'Тверь','2024-07-11','paid',250);\n"
           "INSERT INTO orders VALUES (151,1,'Омск','2024-08-12','new',251);\n"
           "INSERT INTO orders VALUES (152,2,'Москва','2024-09-13','cancelled',252);\n"
           "INSERT INTO orders VALUES (153,3,'Казань','2024-10-14','paid',253);\n"
           "INSERT INTO orders VALUES (154,4,'Тверь','2024-11-15','new',254);\n"
           "INSERT INTO orders VALUES (155,5,'Омск','2024-12-16','cancelled',255);\n"
           "INSERT INTO orders VALUES (156,6,'Москва','2024-01-17','paid',256);\n"
           "INSERT INTO orders VALUES (157,7,'Казань','2024-02-18','new',257);\n"
           "INSERT INTO orders VALUES (158,8,'Тверь','2024-03-19','cancelled',258);\n"
           "INSERT INTO orders VALUES (159,9,'Омск','2024-04-20','paid',259);\n"
           "INSERT INTO orders VALUES (160,10,'Москва','2024-05-21','new',260);\n"
           "INSERT INTO orders VALUES (161,11,'Казань','2024-06-22','cancelled',261);\n"
           "INSERT INTO orders VALUES (162,12,'Тверь','2024-07-23','paid',262);\n"
           "INSERT INTO orders VALUES (163,13,'Омск','2024-08-24','new',263);\n"
           "INSERT INTO orders VALUES (164,14,'Москва','2024-09-25','cancelled',264);\n"
           "INSERT INTO orders VALUES (165,15,'Казань','2024-10-26','paid',265);\n"
           "INSERT INTO orders VALUES (166,16,'Тверь','2024-11-27','new',266);\n"
           "INSERT INTO orders VALUES (167,17,'Омск','2024-12-28','cancelled',267);\n"
           "INSERT INTO orders VALUES (168,18,'Москва','2024-01-01','paid',268);\n"
           "INSERT INTO orders VALUES (169,19,'Казань','2024-02-02','new',269);\n"
           "INSERT INTO orders VALUES (170,20,'Тверь','2024-03-03','cancelled',270);\n"
           "INSERT INTO orders VALUES (171,21,'Омск','2024-04-04','paid',271);\n"
           "INSERT INTO orders VALUES (172,22,'Москва','2024-05-05','new',272);\n"
           "INSERT INTO orders VALUES (173,23,'Казань','2024-06-06','cancelled',273);\n"
           "INSERT INTO orders VALUES (174,24,'Тверь','2024-07-07','paid',274);\n"
           "INSERT INTO orders VALUES (175,25,'Омск','2024-08-08','new',275);\n"
           "INSERT INTO orders VALUES (176,26,'Москва','2024-09-09','cancelled',276);\n"
           "INSERT INTO orders VALUES (177,27,'Казань','2024-10-10','paid',277);\n"
           "INSERT INTO orders VALUES (178,28,'Тверь','2024-11-11','new',278);\n"
           "INSERT INTO orders VALUES (179,29,'Омск','2024-12-12','cancelled',279);\n"
           "INSERT INTO orders VALUES (180,30,'Москва','2024-01-13','paid',280);\n"
           "INSERT INTO orders VALUES (181,31,'Казань','2024-02-14','new',281);\n"
           "INSERT INTO orders VALUES (182,32,'Тверь','2024-03-15','cancelled',282);\n"
           "INSERT INTO orders VALUES (183,33,'Омск','2024-04-16','paid',283);\n"
           "INSERT INTO orders VALUES (184,34,'Москва','2024-05-17','new',284);\n"
           "INSERT INTO orders VALUES (185,35,'Казань','2024-06-18','cancelled',285);\n"
           "INSERT INTO orders VALUES (186,36,'Тверь','2024-07-19','paid',286);\n"
           "INSERT INTO orders VALUES (187,37,'Омск','2024-08-20','new',287);\n"
           "INSERT INTO orders VALUES (188,38,'Москва','2024-09-21','cancelled',288);\n"
           "INSERT INTO orders VALUES (189,39,'Казань','2024-10-22','paid',289);\n"
           "INSERT INTO orders VALUES (190,40,'Тверь','2024-11-23','new',290);\n"
           "INSERT INTO orders VALUES (191,41,'Омск','2024-12-24','cancelled',291);\n"
           "INSERT INTO orders VALUES (192,42,'Москва','2024-01-25','paid',292);\n"
           "INSERT INTO orders VALUES (193,43,'Казань','2024-02-26','new',293);\n"
           "INSERT INTO orders VALUES (194,44,'Тверь','2024-03-27','cancelled',294);\n"
           "INSERT INTO orders VALUES (195,45,'Омск','2024-04-28','paid',295);\n"
           "INSERT INTO orders VALUES (196,46,'Москва','2024-05-01','new',296);\n"
           "INSERT INTO orders VALUES (197,47,'Казань','2024-06-02','cancelled',297);\n"
           "INSERT INTO orders VALUES (198,48,'Тверь','2024-07-03','paid',298);\n"
           "INSERT INTO orders VALUES (199,49,'Омск','2024-08-04','new',299);\n"
           "INSERT INTO orders VALUES (200,0,'Москва','2024-09-05','cancelled',300);\n"
           "INSERT INTO orders VALUES (201,1,'Казань','2024-10-06','paid',301);\n"
           "INSERT INTO orders VALUES (202,2,'Тверь','2024-11-07','new',302);\n"
           "INSERT INTO orders VALUES (203,3,'Омск','2024-12-08','cancelled',303);\n"
           "INSERT INTO orders VALUES (204,4,'Москва','2024-01-09','paid',304);\n"
           "INSERT INTO orders VALUES (205,5,'Казань','2024-02-10','new',305);\n"
           "INSERT INTO orders VALUES (206,6,'Тверь','2024-03-11','cancelled',306);\n"
           "INSERT INTO orders VALUES (207,7,'Омск','2024-04-12','paid',307);\n"
           "INSERT INTO orders VALUES (208,8,'Москва','2024-05-13','new',308);\n"
           "INSERT INTO orders VALUES (209,9,'Казань','2024-06-14','cancelled',309);\n"
           "INSERT INTO orders VALUES (210,10,'Тверь','2024-07-15','paid',310);\n"
           "INSERT INTO orders VALUES (211,11,'Омск','2024-08-16','new',311);\n"
           "INSERT INTO orders VALUES (212,12,'Москва','2024-09-17','cancelled',312);\n"
           "INSERT INTO orders VALUES (213,13,'Казань','2024-10-18','paid',313);\n"
           "INSERT INTO orders VALUES (214,14,'Тверь','2024-11-19','new',314);\n"
           "INSERT INTO orders VALUES (215,15,'Омск','2024-12-20','cancelled',315);\n"
           "INSERT INTO orders VALUES (216,16,'Москва','2024-01-21','paid',316);\n"
           "INSERT INTO orders VALUES (217,17,'Казань','2024-02-22','new',317);\n"
           "INSERT INTO orders VALUES (218,18,'Тверь','2024-03-23','cancelled',318);\n"
           "INSERT INTO orders VALUES (219,19,'Омск','2024-04-24','paid',319);\n"
           "INSERT INTO orders VALUES (220,20,'Москва','2024-05-25','new',320);\n"
           "INSERT INTO orders VALUES (221,21,'Казань','2024-06-26','cancelled',321);\n"
           "INSERT INTO orders VALUES (222,22,'Тверь','2024-07-27','paid',322);\n"
           "INSERT INTO orders VALUES (223,23,'Омск','2024-08-28','new',323);\n"
           "INSERT INTO orders VALUES (224,24,'Москва','2024-09-01','cancelled',324);\n"
           "INSERT INTO orders VALUES (225,25,'Казань','2024-10-02','paid',325);\n"
           "INSERT INTO orders VALUES (226,26,'Тверь','2024-11-03','new',326);\n"
           "INSERT INTO orders VALUES (227,27,'Омск','2024-12-04','cancelled',327);\n"
           "INSERT INTO orders VALUES (228,28,'Москва','2024-01-05','paid',328);\n"
           "INSERT INTO orders VALUES (229,29,'Казань','2024-02-06','new',329);\n"
           "INSERT INTO orders VALUES (230,30,'Тверь','2024-03-07','cancelled',330);\n"
           "INSERT INTO orders VALUES (231,31,'Омск','2024-04-08','paid',331);\n"
           "INSERT INTO orders VALUES (232,32,'Москва','2024-05-09','new',332);\n"
           "INSERT INTO orders VALUES (233,33,'Казань','2024-06-10','cancelled',333);\n"
           "INSERT INTO orders VALUES (234,34,'Тверь','2024-07-11','paid',334);\n"
           "INSERT INTO orders VALUES (235,35,'Омск','2024-08-12','new',335);\n"
           "INSERT INTO orders VALUES (236,36,'Москва','2024-09-13','cancelled',336);\n"
           "INSERT INTO orders VALUES (237,37,'Казань','2024-10-14','paid',337);\n"
           "INSERT INTO orders VALUES (238,38,'Тверь','2024-11-15','new',338);\n"
           "INSERT INTO orders VALUES (239,39,'Омск','2024-12-16','cancelled',339);\n"
           "INSERT INTO orders VALUES (240,40,'Москва','2024-01-17','paid',340);\n"
           "INSERT INTO orders VALUES (241,41,'Казань','2024-02-18','new',341);\n"
           "INSERT INTO orders VALUES (242,42,'Тверь','2024-03-19','cancelled',342);\n"
           "INSERT INTO orders VALUES (243,43,'Омск','2024-04-20','paid',343);\n"
           "INSERT INTO orders VALUES (244,44,'Москва','2024-05-21','new',344);\n"
           "INSERT INTO orders VALUES (245,45,'Казань','2024-06-22','cancelled',345);\n"
           "INSERT INTO orders VALUES (246,46,'Тверь','2024-07-23','paid',346);\n"
           "INSERT INTO orders VALUES (247,47,'Омск','2024-08-24','new',347);\n"
           "INSERT INTO orders VALUES (248,48,'Москва','2024-09-25','cancelled',348);\n"
           "INSERT INTO orders VALUES (249,49,'Казань','2024-10-26','paid',349);\n"
           "INSERT INTO orders VALUES (250,0,'Тверь','2024-11-27','new',350);\n"
           "INSERT INTO orders VALUES (251,1,'Омск','2024-12-28','cancelled',351);\n"
           "INSERT INTO orders VALUES (252,2,'Москва','2024-01-01','paid',352);\n"
           "INSERT INTO orders VALUES (253,3,'Казань','2024-02-02','new',353);\n"
           "INSERT INTO orders VALUES (254,4,'Тверь','2024-03-03','cancelled',354);\n"
           "INSERT INTO orders VALUES (255,5,'Омск','2024-04-04','paid',355);\n"
           "INSERT INTO orders VALUES (256,6,'Москва','2024-05-05','new',356);\n"
           "INSERT INTO orders VALUES (257,7,'Казань','2024-06-06','cancelled',357);\n"
           "INSERT INTO orders VALUES (258,8,'Тверь','2024-07-07','paid',358);\n"
           "INSERT INTO orders VALUES (259,9,'Омск','2024-08-08','new',359);\n"
           "INSERT INTO orders VALUES (260,10,'Москва','2024-09-09','cancelled',360);\n"
           "INSERT INTO orders VALUES (261,11,'Казань','2024-10-10','paid',361);\n"
           "INSERT INTO orders VALUES (262,12,'Тверь','2024-11-11','new',362);\n"
           "INSERT INTO orders VALUES (263,13,'Омск','2024-12-12','cancelled',363);\n"
           "INSERT INTO orders VALUES (264,14,'Москва','2024-01-13','paid',364);\n"
           "INSERT INTO orders VALUES (265,15,'Казань','2024-02-14','new',365);\n"
           "INSERT INTO orders VALUES (266,16,'Тверь','2024-03-15','cancelled',366);\n"
           "INSERT INTO orders VALUES (267,17,'Омск','2024-04-16','paid',367);\n"
           "INSERT INTO orders VALUES (268,18,'Москва','2024-05-17','new',368);\n"
           "INSERT INTO orders VALUES (269,19,'Казань','2024-06-18','cancelled',369);\n"
           "INSERT INTO orders VALUES (270,20,'Тверь','2024-07-19','paid',370);\n"
           "INSERT INTO orders VALUES (271,21,'Омск','2024-08-20','new',371);\n"
           "INSERT INTO orders VALUES (272,22,'Москва','2024-09-21','cancelled',372);\n"
           "INSERT INTO orders VALUES (273,23,'Казань','2024-10-22','paid',373);\n"
           "INSERT INTO orders VALUES (274,24,'Тверь','2024-11-23','new',374);\n"
           "INSERT INTO orders VALUES (275,25,'Омск','2024-12-24','cancelled',375);\n"
           "INSERT INTO orders VALUES (276,26,'Москва','2024-01-25','paid',376);\n"
           "INSERT INTO orders VALUES (277,27,'Казань','2024-02-26','new',377);\n"
           "INSERT INTO orders VALUES (278,28,'Тверь','2024-03-27','cancelled',378);\n"
           "INSERT INTO orders VALUES (279,29,'Омск','2024-04-28','paid',379);\n"
           "INSERT INTO orders VALUES (280,30,'Москва','2024-05-01','new',380);\n"
           "INSERT INTO orders VALUES (281,31,'Казань','2024-06-02','cancelled',381);\n"
           "INSERT INTO orders VALUES (282,32,'Тверь','2024-07-03','paid',382);\n"
           "INSERT INTO orders VALUES (283,33,'Омск','2024-08-04','new',383);\n"
           "INSERT INTO orders VALUES (284,34,'Москва','2024-09-05','cancelled',384);\n"
           "INSERT INTO orders VALUES (285,35,'Казань','2024-10-06','paid',385);\n"
           "INSERT INTO orders VALUES (286,36,'Тверь','2024-11-07','new',386);\n"
           "INSERT INTO orders VALUES (287,37,'Омск','2024-12-08','cancelled',387);\n"
           "INSERT INTO orders VALUES (288,38,'Москва','2024-01-09','paid',388);\n"
           "INSERT INTO orders VALUES (289,39,'Казань','2024-02-10','new',389);\n"
           "INSERT INTO orders VALUES (290,40,'Тверь','2024-03-11','cancelled',390);\n"
           "INSERT INTO orders VALUES (291,41,'Омск','2024-04-12','paid',391);\n"
           "INSERT INTO orders VALUES (292,42,'Москва','2024-05-13','new',392);\n"
           "INSERT INTO orders VALUES (293,43,'Казань','2024-06-14','cancelled',393);\n"
           "INSERT INTO orders VALUES (294,44,'Тверь','2024-07-15','paid',394);\n"
           "INSERT INTO orders VALUES (295,45,'Омск','2024-08-16','new',395);\n"
           "INSERT INTO orders VALUES (296,46,'Москва','2024-09-17','cancelled',396);\n"
           "INSERT INTO orders VALUES (297,47,'Казань','2024-10-18','paid',397);\n"
           "INSERT INTO orders VALUES (298,48,'Тверь','2024-11-19','new',398);\n"
           "INSERT INTO orders VALUES (299,49,'Омск','2024-12-20','cancelled',399);\n"
           "INSERT INTO orders VALUES (300,0,'Москва','2024-01-21','paid',400);\n",
  'expected': [[2, 0, 47, 'SEARCH orders USING COVERING INDEX idx_city_created (city=? AND created>?)']],
  'hint': 'Столбец с равенством ставят первым, диапазонный — последним: (city, created).',
  'check': "EXPLAIN QUERY PLAN SELECT id FROM orders WHERE city = 'Москва' AND created >= '2024-06-01'",
  'contains': ['(city=? AND created>?)']},
 {'id': 'd3-left-prefix',
  'mode': 'sql',
  'title': 'Левый префикс',
  'statement': "Есть индекс по (customer_id, status), а запрос SELECT * FROM orders WHERE status = 'paid' по "
               'нему не искать. Создайте индекс, который сделает этот запрос поиском (индекс может '
               'начинаться с status).',
  'starter': "-- индекс для WHERE status = 'paid'\nCREATE INDEX\n",
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, city TEXT NOT NULL, '
           'created TEXT NOT NULL, status TEXT NOT NULL, total INTEGER NOT NULL);\n'
           "INSERT INTO orders VALUES (1,1,'Казань','2024-02-02','new',101);\n"
           "INSERT INTO orders VALUES (2,2,'Тверь','2024-03-03','cancelled',102);\n"
           "INSERT INTO orders VALUES (3,3,'Омск','2024-04-04','paid',103);\n"
           "INSERT INTO orders VALUES (4,4,'Москва','2024-05-05','new',104);\n"
           "INSERT INTO orders VALUES (5,5,'Казань','2024-06-06','cancelled',105);\n"
           "INSERT INTO orders VALUES (6,6,'Тверь','2024-07-07','paid',106);\n"
           "INSERT INTO orders VALUES (7,7,'Омск','2024-08-08','new',107);\n"
           "INSERT INTO orders VALUES (8,8,'Москва','2024-09-09','cancelled',108);\n"
           "INSERT INTO orders VALUES (9,9,'Казань','2024-10-10','paid',109);\n"
           "INSERT INTO orders VALUES (10,10,'Тверь','2024-11-11','new',110);\n"
           "INSERT INTO orders VALUES (11,11,'Омск','2024-12-12','cancelled',111);\n"
           "INSERT INTO orders VALUES (12,12,'Москва','2024-01-13','paid',112);\n"
           "INSERT INTO orders VALUES (13,13,'Казань','2024-02-14','new',113);\n"
           "INSERT INTO orders VALUES (14,14,'Тверь','2024-03-15','cancelled',114);\n"
           "INSERT INTO orders VALUES (15,15,'Омск','2024-04-16','paid',115);\n"
           "INSERT INTO orders VALUES (16,16,'Москва','2024-05-17','new',116);\n"
           "INSERT INTO orders VALUES (17,17,'Казань','2024-06-18','cancelled',117);\n"
           "INSERT INTO orders VALUES (18,18,'Тверь','2024-07-19','paid',118);\n"
           "INSERT INTO orders VALUES (19,19,'Омск','2024-08-20','new',119);\n"
           "INSERT INTO orders VALUES (20,20,'Москва','2024-09-21','cancelled',120);\n"
           "INSERT INTO orders VALUES (21,21,'Казань','2024-10-22','paid',121);\n"
           "INSERT INTO orders VALUES (22,22,'Тверь','2024-11-23','new',122);\n"
           "INSERT INTO orders VALUES (23,23,'Омск','2024-12-24','cancelled',123);\n"
           "INSERT INTO orders VALUES (24,24,'Москва','2024-01-25','paid',124);\n"
           "INSERT INTO orders VALUES (25,25,'Казань','2024-02-26','new',125);\n"
           "INSERT INTO orders VALUES (26,26,'Тверь','2024-03-27','cancelled',126);\n"
           "INSERT INTO orders VALUES (27,27,'Омск','2024-04-28','paid',127);\n"
           "INSERT INTO orders VALUES (28,28,'Москва','2024-05-01','new',128);\n"
           "INSERT INTO orders VALUES (29,29,'Казань','2024-06-02','cancelled',129);\n"
           "INSERT INTO orders VALUES (30,30,'Тверь','2024-07-03','paid',130);\n"
           "INSERT INTO orders VALUES (31,31,'Омск','2024-08-04','new',131);\n"
           "INSERT INTO orders VALUES (32,32,'Москва','2024-09-05','cancelled',132);\n"
           "INSERT INTO orders VALUES (33,33,'Казань','2024-10-06','paid',133);\n"
           "INSERT INTO orders VALUES (34,34,'Тверь','2024-11-07','new',134);\n"
           "INSERT INTO orders VALUES (35,35,'Омск','2024-12-08','cancelled',135);\n"
           "INSERT INTO orders VALUES (36,36,'Москва','2024-01-09','paid',136);\n"
           "INSERT INTO orders VALUES (37,37,'Казань','2024-02-10','new',137);\n"
           "INSERT INTO orders VALUES (38,38,'Тверь','2024-03-11','cancelled',138);\n"
           "INSERT INTO orders VALUES (39,39,'Омск','2024-04-12','paid',139);\n"
           "INSERT INTO orders VALUES (40,40,'Москва','2024-05-13','new',140);\n"
           "INSERT INTO orders VALUES (41,41,'Казань','2024-06-14','cancelled',141);\n"
           "INSERT INTO orders VALUES (42,42,'Тверь','2024-07-15','paid',142);\n"
           "INSERT INTO orders VALUES (43,43,'Омск','2024-08-16','new',143);\n"
           "INSERT INTO orders VALUES (44,44,'Москва','2024-09-17','cancelled',144);\n"
           "INSERT INTO orders VALUES (45,45,'Казань','2024-10-18','paid',145);\n"
           "INSERT INTO orders VALUES (46,46,'Тверь','2024-11-19','new',146);\n"
           "INSERT INTO orders VALUES (47,47,'Омск','2024-12-20','cancelled',147);\n"
           "INSERT INTO orders VALUES (48,48,'Москва','2024-01-21','paid',148);\n"
           "INSERT INTO orders VALUES (49,49,'Казань','2024-02-22','new',149);\n"
           "INSERT INTO orders VALUES (50,0,'Тверь','2024-03-23','cancelled',150);\n"
           "INSERT INTO orders VALUES (51,1,'Омск','2024-04-24','paid',151);\n"
           "INSERT INTO orders VALUES (52,2,'Москва','2024-05-25','new',152);\n"
           "INSERT INTO orders VALUES (53,3,'Казань','2024-06-26','cancelled',153);\n"
           "INSERT INTO orders VALUES (54,4,'Тверь','2024-07-27','paid',154);\n"
           "INSERT INTO orders VALUES (55,5,'Омск','2024-08-28','new',155);\n"
           "INSERT INTO orders VALUES (56,6,'Москва','2024-09-01','cancelled',156);\n"
           "INSERT INTO orders VALUES (57,7,'Казань','2024-10-02','paid',157);\n"
           "INSERT INTO orders VALUES (58,8,'Тверь','2024-11-03','new',158);\n"
           "INSERT INTO orders VALUES (59,9,'Омск','2024-12-04','cancelled',159);\n"
           "INSERT INTO orders VALUES (60,10,'Москва','2024-01-05','paid',160);\n"
           "INSERT INTO orders VALUES (61,11,'Казань','2024-02-06','new',161);\n"
           "INSERT INTO orders VALUES (62,12,'Тверь','2024-03-07','cancelled',162);\n"
           "INSERT INTO orders VALUES (63,13,'Омск','2024-04-08','paid',163);\n"
           "INSERT INTO orders VALUES (64,14,'Москва','2024-05-09','new',164);\n"
           "INSERT INTO orders VALUES (65,15,'Казань','2024-06-10','cancelled',165);\n"
           "INSERT INTO orders VALUES (66,16,'Тверь','2024-07-11','paid',166);\n"
           "INSERT INTO orders VALUES (67,17,'Омск','2024-08-12','new',167);\n"
           "INSERT INTO orders VALUES (68,18,'Москва','2024-09-13','cancelled',168);\n"
           "INSERT INTO orders VALUES (69,19,'Казань','2024-10-14','paid',169);\n"
           "INSERT INTO orders VALUES (70,20,'Тверь','2024-11-15','new',170);\n"
           "INSERT INTO orders VALUES (71,21,'Омск','2024-12-16','cancelled',171);\n"
           "INSERT INTO orders VALUES (72,22,'Москва','2024-01-17','paid',172);\n"
           "INSERT INTO orders VALUES (73,23,'Казань','2024-02-18','new',173);\n"
           "INSERT INTO orders VALUES (74,24,'Тверь','2024-03-19','cancelled',174);\n"
           "INSERT INTO orders VALUES (75,25,'Омск','2024-04-20','paid',175);\n"
           "INSERT INTO orders VALUES (76,26,'Москва','2024-05-21','new',176);\n"
           "INSERT INTO orders VALUES (77,27,'Казань','2024-06-22','cancelled',177);\n"
           "INSERT INTO orders VALUES (78,28,'Тверь','2024-07-23','paid',178);\n"
           "INSERT INTO orders VALUES (79,29,'Омск','2024-08-24','new',179);\n"
           "INSERT INTO orders VALUES (80,30,'Москва','2024-09-25','cancelled',180);\n"
           "INSERT INTO orders VALUES (81,31,'Казань','2024-10-26','paid',181);\n"
           "INSERT INTO orders VALUES (82,32,'Тверь','2024-11-27','new',182);\n"
           "INSERT INTO orders VALUES (83,33,'Омск','2024-12-28','cancelled',183);\n"
           "INSERT INTO orders VALUES (84,34,'Москва','2024-01-01','paid',184);\n"
           "INSERT INTO orders VALUES (85,35,'Казань','2024-02-02','new',185);\n"
           "INSERT INTO orders VALUES (86,36,'Тверь','2024-03-03','cancelled',186);\n"
           "INSERT INTO orders VALUES (87,37,'Омск','2024-04-04','paid',187);\n"
           "INSERT INTO orders VALUES (88,38,'Москва','2024-05-05','new',188);\n"
           "INSERT INTO orders VALUES (89,39,'Казань','2024-06-06','cancelled',189);\n"
           "INSERT INTO orders VALUES (90,40,'Тверь','2024-07-07','paid',190);\n"
           "INSERT INTO orders VALUES (91,41,'Омск','2024-08-08','new',191);\n"
           "INSERT INTO orders VALUES (92,42,'Москва','2024-09-09','cancelled',192);\n"
           "INSERT INTO orders VALUES (93,43,'Казань','2024-10-10','paid',193);\n"
           "INSERT INTO orders VALUES (94,44,'Тверь','2024-11-11','new',194);\n"
           "INSERT INTO orders VALUES (95,45,'Омск','2024-12-12','cancelled',195);\n"
           "INSERT INTO orders VALUES (96,46,'Москва','2024-01-13','paid',196);\n"
           "INSERT INTO orders VALUES (97,47,'Казань','2024-02-14','new',197);\n"
           "INSERT INTO orders VALUES (98,48,'Тверь','2024-03-15','cancelled',198);\n"
           "INSERT INTO orders VALUES (99,49,'Омск','2024-04-16','paid',199);\n"
           "INSERT INTO orders VALUES (100,0,'Москва','2024-05-17','new',200);\n"
           "INSERT INTO orders VALUES (101,1,'Казань','2024-06-18','cancelled',201);\n"
           "INSERT INTO orders VALUES (102,2,'Тверь','2024-07-19','paid',202);\n"
           "INSERT INTO orders VALUES (103,3,'Омск','2024-08-20','new',203);\n"
           "INSERT INTO orders VALUES (104,4,'Москва','2024-09-21','cancelled',204);\n"
           "INSERT INTO orders VALUES (105,5,'Казань','2024-10-22','paid',205);\n"
           "INSERT INTO orders VALUES (106,6,'Тверь','2024-11-23','new',206);\n"
           "INSERT INTO orders VALUES (107,7,'Омск','2024-12-24','cancelled',207);\n"
           "INSERT INTO orders VALUES (108,8,'Москва','2024-01-25','paid',208);\n"
           "INSERT INTO orders VALUES (109,9,'Казань','2024-02-26','new',209);\n"
           "INSERT INTO orders VALUES (110,10,'Тверь','2024-03-27','cancelled',210);\n"
           "INSERT INTO orders VALUES (111,11,'Омск','2024-04-28','paid',211);\n"
           "INSERT INTO orders VALUES (112,12,'Москва','2024-05-01','new',212);\n"
           "INSERT INTO orders VALUES (113,13,'Казань','2024-06-02','cancelled',213);\n"
           "INSERT INTO orders VALUES (114,14,'Тверь','2024-07-03','paid',214);\n"
           "INSERT INTO orders VALUES (115,15,'Омск','2024-08-04','new',215);\n"
           "INSERT INTO orders VALUES (116,16,'Москва','2024-09-05','cancelled',216);\n"
           "INSERT INTO orders VALUES (117,17,'Казань','2024-10-06','paid',217);\n"
           "INSERT INTO orders VALUES (118,18,'Тверь','2024-11-07','new',218);\n"
           "INSERT INTO orders VALUES (119,19,'Омск','2024-12-08','cancelled',219);\n"
           "INSERT INTO orders VALUES (120,20,'Москва','2024-01-09','paid',220);\n"
           "INSERT INTO orders VALUES (121,21,'Казань','2024-02-10','new',221);\n"
           "INSERT INTO orders VALUES (122,22,'Тверь','2024-03-11','cancelled',222);\n"
           "INSERT INTO orders VALUES (123,23,'Омск','2024-04-12','paid',223);\n"
           "INSERT INTO orders VALUES (124,24,'Москва','2024-05-13','new',224);\n"
           "INSERT INTO orders VALUES (125,25,'Казань','2024-06-14','cancelled',225);\n"
           "INSERT INTO orders VALUES (126,26,'Тверь','2024-07-15','paid',226);\n"
           "INSERT INTO orders VALUES (127,27,'Омск','2024-08-16','new',227);\n"
           "INSERT INTO orders VALUES (128,28,'Москва','2024-09-17','cancelled',228);\n"
           "INSERT INTO orders VALUES (129,29,'Казань','2024-10-18','paid',229);\n"
           "INSERT INTO orders VALUES (130,30,'Тверь','2024-11-19','new',230);\n"
           "INSERT INTO orders VALUES (131,31,'Омск','2024-12-20','cancelled',231);\n"
           "INSERT INTO orders VALUES (132,32,'Москва','2024-01-21','paid',232);\n"
           "INSERT INTO orders VALUES (133,33,'Казань','2024-02-22','new',233);\n"
           "INSERT INTO orders VALUES (134,34,'Тверь','2024-03-23','cancelled',234);\n"
           "INSERT INTO orders VALUES (135,35,'Омск','2024-04-24','paid',235);\n"
           "INSERT INTO orders VALUES (136,36,'Москва','2024-05-25','new',236);\n"
           "INSERT INTO orders VALUES (137,37,'Казань','2024-06-26','cancelled',237);\n"
           "INSERT INTO orders VALUES (138,38,'Тверь','2024-07-27','paid',238);\n"
           "INSERT INTO orders VALUES (139,39,'Омск','2024-08-28','new',239);\n"
           "INSERT INTO orders VALUES (140,40,'Москва','2024-09-01','cancelled',240);\n"
           "INSERT INTO orders VALUES (141,41,'Казань','2024-10-02','paid',241);\n"
           "INSERT INTO orders VALUES (142,42,'Тверь','2024-11-03','new',242);\n"
           "INSERT INTO orders VALUES (143,43,'Омск','2024-12-04','cancelled',243);\n"
           "INSERT INTO orders VALUES (144,44,'Москва','2024-01-05','paid',244);\n"
           "INSERT INTO orders VALUES (145,45,'Казань','2024-02-06','new',245);\n"
           "INSERT INTO orders VALUES (146,46,'Тверь','2024-03-07','cancelled',246);\n"
           "INSERT INTO orders VALUES (147,47,'Омск','2024-04-08','paid',247);\n"
           "INSERT INTO orders VALUES (148,48,'Москва','2024-05-09','new',248);\n"
           "INSERT INTO orders VALUES (149,49,'Казань','2024-06-10','cancelled',249);\n"
           "INSERT INTO orders VALUES (150,0,'Тверь','2024-07-11','paid',250);\n"
           "INSERT INTO orders VALUES (151,1,'Омск','2024-08-12','new',251);\n"
           "INSERT INTO orders VALUES (152,2,'Москва','2024-09-13','cancelled',252);\n"
           "INSERT INTO orders VALUES (153,3,'Казань','2024-10-14','paid',253);\n"
           "INSERT INTO orders VALUES (154,4,'Тверь','2024-11-15','new',254);\n"
           "INSERT INTO orders VALUES (155,5,'Омск','2024-12-16','cancelled',255);\n"
           "INSERT INTO orders VALUES (156,6,'Москва','2024-01-17','paid',256);\n"
           "INSERT INTO orders VALUES (157,7,'Казань','2024-02-18','new',257);\n"
           "INSERT INTO orders VALUES (158,8,'Тверь','2024-03-19','cancelled',258);\n"
           "INSERT INTO orders VALUES (159,9,'Омск','2024-04-20','paid',259);\n"
           "INSERT INTO orders VALUES (160,10,'Москва','2024-05-21','new',260);\n"
           "INSERT INTO orders VALUES (161,11,'Казань','2024-06-22','cancelled',261);\n"
           "INSERT INTO orders VALUES (162,12,'Тверь','2024-07-23','paid',262);\n"
           "INSERT INTO orders VALUES (163,13,'Омск','2024-08-24','new',263);\n"
           "INSERT INTO orders VALUES (164,14,'Москва','2024-09-25','cancelled',264);\n"
           "INSERT INTO orders VALUES (165,15,'Казань','2024-10-26','paid',265);\n"
           "INSERT INTO orders VALUES (166,16,'Тверь','2024-11-27','new',266);\n"
           "INSERT INTO orders VALUES (167,17,'Омск','2024-12-28','cancelled',267);\n"
           "INSERT INTO orders VALUES (168,18,'Москва','2024-01-01','paid',268);\n"
           "INSERT INTO orders VALUES (169,19,'Казань','2024-02-02','new',269);\n"
           "INSERT INTO orders VALUES (170,20,'Тверь','2024-03-03','cancelled',270);\n"
           "INSERT INTO orders VALUES (171,21,'Омск','2024-04-04','paid',271);\n"
           "INSERT INTO orders VALUES (172,22,'Москва','2024-05-05','new',272);\n"
           "INSERT INTO orders VALUES (173,23,'Казань','2024-06-06','cancelled',273);\n"
           "INSERT INTO orders VALUES (174,24,'Тверь','2024-07-07','paid',274);\n"
           "INSERT INTO orders VALUES (175,25,'Омск','2024-08-08','new',275);\n"
           "INSERT INTO orders VALUES (176,26,'Москва','2024-09-09','cancelled',276);\n"
           "INSERT INTO orders VALUES (177,27,'Казань','2024-10-10','paid',277);\n"
           "INSERT INTO orders VALUES (178,28,'Тверь','2024-11-11','new',278);\n"
           "INSERT INTO orders VALUES (179,29,'Омск','2024-12-12','cancelled',279);\n"
           "INSERT INTO orders VALUES (180,30,'Москва','2024-01-13','paid',280);\n"
           "INSERT INTO orders VALUES (181,31,'Казань','2024-02-14','new',281);\n"
           "INSERT INTO orders VALUES (182,32,'Тверь','2024-03-15','cancelled',282);\n"
           "INSERT INTO orders VALUES (183,33,'Омск','2024-04-16','paid',283);\n"
           "INSERT INTO orders VALUES (184,34,'Москва','2024-05-17','new',284);\n"
           "INSERT INTO orders VALUES (185,35,'Казань','2024-06-18','cancelled',285);\n"
           "INSERT INTO orders VALUES (186,36,'Тверь','2024-07-19','paid',286);\n"
           "INSERT INTO orders VALUES (187,37,'Омск','2024-08-20','new',287);\n"
           "INSERT INTO orders VALUES (188,38,'Москва','2024-09-21','cancelled',288);\n"
           "INSERT INTO orders VALUES (189,39,'Казань','2024-10-22','paid',289);\n"
           "INSERT INTO orders VALUES (190,40,'Тверь','2024-11-23','new',290);\n"
           "INSERT INTO orders VALUES (191,41,'Омск','2024-12-24','cancelled',291);\n"
           "INSERT INTO orders VALUES (192,42,'Москва','2024-01-25','paid',292);\n"
           "INSERT INTO orders VALUES (193,43,'Казань','2024-02-26','new',293);\n"
           "INSERT INTO orders VALUES (194,44,'Тверь','2024-03-27','cancelled',294);\n"
           "INSERT INTO orders VALUES (195,45,'Омск','2024-04-28','paid',295);\n"
           "INSERT INTO orders VALUES (196,46,'Москва','2024-05-01','new',296);\n"
           "INSERT INTO orders VALUES (197,47,'Казань','2024-06-02','cancelled',297);\n"
           "INSERT INTO orders VALUES (198,48,'Тверь','2024-07-03','paid',298);\n"
           "INSERT INTO orders VALUES (199,49,'Омск','2024-08-04','new',299);\n"
           "INSERT INTO orders VALUES (200,0,'Москва','2024-09-05','cancelled',300);\n"
           "INSERT INTO orders VALUES (201,1,'Казань','2024-10-06','paid',301);\n"
           "INSERT INTO orders VALUES (202,2,'Тверь','2024-11-07','new',302);\n"
           "INSERT INTO orders VALUES (203,3,'Омск','2024-12-08','cancelled',303);\n"
           "INSERT INTO orders VALUES (204,4,'Москва','2024-01-09','paid',304);\n"
           "INSERT INTO orders VALUES (205,5,'Казань','2024-02-10','new',305);\n"
           "INSERT INTO orders VALUES (206,6,'Тверь','2024-03-11','cancelled',306);\n"
           "INSERT INTO orders VALUES (207,7,'Омск','2024-04-12','paid',307);\n"
           "INSERT INTO orders VALUES (208,8,'Москва','2024-05-13','new',308);\n"
           "INSERT INTO orders VALUES (209,9,'Казань','2024-06-14','cancelled',309);\n"
           "INSERT INTO orders VALUES (210,10,'Тверь','2024-07-15','paid',310);\n"
           "INSERT INTO orders VALUES (211,11,'Омск','2024-08-16','new',311);\n"
           "INSERT INTO orders VALUES (212,12,'Москва','2024-09-17','cancelled',312);\n"
           "INSERT INTO orders VALUES (213,13,'Казань','2024-10-18','paid',313);\n"
           "INSERT INTO orders VALUES (214,14,'Тверь','2024-11-19','new',314);\n"
           "INSERT INTO orders VALUES (215,15,'Омск','2024-12-20','cancelled',315);\n"
           "INSERT INTO orders VALUES (216,16,'Москва','2024-01-21','paid',316);\n"
           "INSERT INTO orders VALUES (217,17,'Казань','2024-02-22','new',317);\n"
           "INSERT INTO orders VALUES (218,18,'Тверь','2024-03-23','cancelled',318);\n"
           "INSERT INTO orders VALUES (219,19,'Омск','2024-04-24','paid',319);\n"
           "INSERT INTO orders VALUES (220,20,'Москва','2024-05-25','new',320);\n"
           "INSERT INTO orders VALUES (221,21,'Казань','2024-06-26','cancelled',321);\n"
           "INSERT INTO orders VALUES (222,22,'Тверь','2024-07-27','paid',322);\n"
           "INSERT INTO orders VALUES (223,23,'Омск','2024-08-28','new',323);\n"
           "INSERT INTO orders VALUES (224,24,'Москва','2024-09-01','cancelled',324);\n"
           "INSERT INTO orders VALUES (225,25,'Казань','2024-10-02','paid',325);\n"
           "INSERT INTO orders VALUES (226,26,'Тверь','2024-11-03','new',326);\n"
           "INSERT INTO orders VALUES (227,27,'Омск','2024-12-04','cancelled',327);\n"
           "INSERT INTO orders VALUES (228,28,'Москва','2024-01-05','paid',328);\n"
           "INSERT INTO orders VALUES (229,29,'Казань','2024-02-06','new',329);\n"
           "INSERT INTO orders VALUES (230,30,'Тверь','2024-03-07','cancelled',330);\n"
           "INSERT INTO orders VALUES (231,31,'Омск','2024-04-08','paid',331);\n"
           "INSERT INTO orders VALUES (232,32,'Москва','2024-05-09','new',332);\n"
           "INSERT INTO orders VALUES (233,33,'Казань','2024-06-10','cancelled',333);\n"
           "INSERT INTO orders VALUES (234,34,'Тверь','2024-07-11','paid',334);\n"
           "INSERT INTO orders VALUES (235,35,'Омск','2024-08-12','new',335);\n"
           "INSERT INTO orders VALUES (236,36,'Москва','2024-09-13','cancelled',336);\n"
           "INSERT INTO orders VALUES (237,37,'Казань','2024-10-14','paid',337);\n"
           "INSERT INTO orders VALUES (238,38,'Тверь','2024-11-15','new',338);\n"
           "INSERT INTO orders VALUES (239,39,'Омск','2024-12-16','cancelled',339);\n"
           "INSERT INTO orders VALUES (240,40,'Москва','2024-01-17','paid',340);\n"
           "INSERT INTO orders VALUES (241,41,'Казань','2024-02-18','new',341);\n"
           "INSERT INTO orders VALUES (242,42,'Тверь','2024-03-19','cancelled',342);\n"
           "INSERT INTO orders VALUES (243,43,'Омск','2024-04-20','paid',343);\n"
           "INSERT INTO orders VALUES (244,44,'Москва','2024-05-21','new',344);\n"
           "INSERT INTO orders VALUES (245,45,'Казань','2024-06-22','cancelled',345);\n"
           "INSERT INTO orders VALUES (246,46,'Тверь','2024-07-23','paid',346);\n"
           "INSERT INTO orders VALUES (247,47,'Омск','2024-08-24','new',347);\n"
           "INSERT INTO orders VALUES (248,48,'Москва','2024-09-25','cancelled',348);\n"
           "INSERT INTO orders VALUES (249,49,'Казань','2024-10-26','paid',349);\n"
           "INSERT INTO orders VALUES (250,0,'Тверь','2024-11-27','new',350);\n"
           "INSERT INTO orders VALUES (251,1,'Омск','2024-12-28','cancelled',351);\n"
           "INSERT INTO orders VALUES (252,2,'Москва','2024-01-01','paid',352);\n"
           "INSERT INTO orders VALUES (253,3,'Казань','2024-02-02','new',353);\n"
           "INSERT INTO orders VALUES (254,4,'Тверь','2024-03-03','cancelled',354);\n"
           "INSERT INTO orders VALUES (255,5,'Омск','2024-04-04','paid',355);\n"
           "INSERT INTO orders VALUES (256,6,'Москва','2024-05-05','new',356);\n"
           "INSERT INTO orders VALUES (257,7,'Казань','2024-06-06','cancelled',357);\n"
           "INSERT INTO orders VALUES (258,8,'Тверь','2024-07-07','paid',358);\n"
           "INSERT INTO orders VALUES (259,9,'Омск','2024-08-08','new',359);\n"
           "INSERT INTO orders VALUES (260,10,'Москва','2024-09-09','cancelled',360);\n"
           "INSERT INTO orders VALUES (261,11,'Казань','2024-10-10','paid',361);\n"
           "INSERT INTO orders VALUES (262,12,'Тверь','2024-11-11','new',362);\n"
           "INSERT INTO orders VALUES (263,13,'Омск','2024-12-12','cancelled',363);\n"
           "INSERT INTO orders VALUES (264,14,'Москва','2024-01-13','paid',364);\n"
           "INSERT INTO orders VALUES (265,15,'Казань','2024-02-14','new',365);\n"
           "INSERT INTO orders VALUES (266,16,'Тверь','2024-03-15','cancelled',366);\n"
           "INSERT INTO orders VALUES (267,17,'Омск','2024-04-16','paid',367);\n"
           "INSERT INTO orders VALUES (268,18,'Москва','2024-05-17','new',368);\n"
           "INSERT INTO orders VALUES (269,19,'Казань','2024-06-18','cancelled',369);\n"
           "INSERT INTO orders VALUES (270,20,'Тверь','2024-07-19','paid',370);\n"
           "INSERT INTO orders VALUES (271,21,'Омск','2024-08-20','new',371);\n"
           "INSERT INTO orders VALUES (272,22,'Москва','2024-09-21','cancelled',372);\n"
           "INSERT INTO orders VALUES (273,23,'Казань','2024-10-22','paid',373);\n"
           "INSERT INTO orders VALUES (274,24,'Тверь','2024-11-23','new',374);\n"
           "INSERT INTO orders VALUES (275,25,'Омск','2024-12-24','cancelled',375);\n"
           "INSERT INTO orders VALUES (276,26,'Москва','2024-01-25','paid',376);\n"
           "INSERT INTO orders VALUES (277,27,'Казань','2024-02-26','new',377);\n"
           "INSERT INTO orders VALUES (278,28,'Тверь','2024-03-27','cancelled',378);\n"
           "INSERT INTO orders VALUES (279,29,'Омск','2024-04-28','paid',379);\n"
           "INSERT INTO orders VALUES (280,30,'Москва','2024-05-01','new',380);\n"
           "INSERT INTO orders VALUES (281,31,'Казань','2024-06-02','cancelled',381);\n"
           "INSERT INTO orders VALUES (282,32,'Тверь','2024-07-03','paid',382);\n"
           "INSERT INTO orders VALUES (283,33,'Омск','2024-08-04','new',383);\n"
           "INSERT INTO orders VALUES (284,34,'Москва','2024-09-05','cancelled',384);\n"
           "INSERT INTO orders VALUES (285,35,'Казань','2024-10-06','paid',385);\n"
           "INSERT INTO orders VALUES (286,36,'Тверь','2024-11-07','new',386);\n"
           "INSERT INTO orders VALUES (287,37,'Омск','2024-12-08','cancelled',387);\n"
           "INSERT INTO orders VALUES (288,38,'Москва','2024-01-09','paid',388);\n"
           "INSERT INTO orders VALUES (289,39,'Казань','2024-02-10','new',389);\n"
           "INSERT INTO orders VALUES (290,40,'Тверь','2024-03-11','cancelled',390);\n"
           "INSERT INTO orders VALUES (291,41,'Омск','2024-04-12','paid',391);\n"
           "INSERT INTO orders VALUES (292,42,'Москва','2024-05-13','new',392);\n"
           "INSERT INTO orders VALUES (293,43,'Казань','2024-06-14','cancelled',393);\n"
           "INSERT INTO orders VALUES (294,44,'Тверь','2024-07-15','paid',394);\n"
           "INSERT INTO orders VALUES (295,45,'Омск','2024-08-16','new',395);\n"
           "INSERT INTO orders VALUES (296,46,'Москва','2024-09-17','cancelled',396);\n"
           "INSERT INTO orders VALUES (297,47,'Казань','2024-10-18','paid',397);\n"
           "INSERT INTO orders VALUES (298,48,'Тверь','2024-11-19','new',398);\n"
           "INSERT INTO orders VALUES (299,49,'Омск','2024-12-20','cancelled',399);\n"
           "INSERT INTO orders VALUES (300,0,'Москва','2024-01-21','paid',400);\n"
           'CREATE INDEX idx_cust_status ON orders (customer_id, status);\n',
  'expected': [[3, 0, 62, 'SEARCH orders USING INDEX idx_status (status=?)']],
  'hint': 'Индекс (customer_id, status) не помогает запросу только по status: нужен индекс, начинающийся со '
          'status.',
  'check': "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'paid'",
  'contains': ['USING INDEX idx_status', '(status=?)']},
 {'id': 'd3-expression-index',
  'mode': 'sql',
  'title': 'Индекс на выражении',
  'statement': "Поиск пользователей идёт запросом WHERE lower(email) = 'user5@mail.ru' и просматривает всю "
               'таблицу. Создайте индекс, который сделает его поиском.',
  'starter': '-- индекс для WHERE lower(email) = ...\nCREATE INDEX\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT);\n'
           "INSERT INTO users VALUES (1,'User1@Mail.ru','n1');\n"
           "INSERT INTO users VALUES (2,'User2@Mail.ru','n2');\n"
           "INSERT INTO users VALUES (3,'User3@Mail.ru','n3');\n"
           "INSERT INTO users VALUES (4,'User4@Mail.ru','n4');\n"
           "INSERT INTO users VALUES (5,'User5@Mail.ru','n5');\n"
           "INSERT INTO users VALUES (6,'User6@Mail.ru','n6');\n"
           "INSERT INTO users VALUES (7,'User7@Mail.ru','n7');\n"
           "INSERT INTO users VALUES (8,'User8@Mail.ru','n8');\n"
           "INSERT INTO users VALUES (9,'User9@Mail.ru','n9');\n"
           "INSERT INTO users VALUES (10,'User10@Mail.ru','n10');\n"
           "INSERT INTO users VALUES (11,'User11@Mail.ru','n11');\n"
           "INSERT INTO users VALUES (12,'User12@Mail.ru','n12');\n"
           "INSERT INTO users VALUES (13,'User13@Mail.ru','n13');\n"
           "INSERT INTO users VALUES (14,'User14@Mail.ru','n14');\n"
           "INSERT INTO users VALUES (15,'User15@Mail.ru','n15');\n"
           "INSERT INTO users VALUES (16,'User16@Mail.ru','n16');\n"
           "INSERT INTO users VALUES (17,'User17@Mail.ru','n17');\n"
           "INSERT INTO users VALUES (18,'User18@Mail.ru','n18');\n"
           "INSERT INTO users VALUES (19,'User19@Mail.ru','n19');\n"
           "INSERT INTO users VALUES (20,'User20@Mail.ru','n20');\n"
           "INSERT INTO users VALUES (21,'User21@Mail.ru','n21');\n"
           "INSERT INTO users VALUES (22,'User22@Mail.ru','n22');\n"
           "INSERT INTO users VALUES (23,'User23@Mail.ru','n23');\n"
           "INSERT INTO users VALUES (24,'User24@Mail.ru','n24');\n"
           "INSERT INTO users VALUES (25,'User25@Mail.ru','n25');\n"
           "INSERT INTO users VALUES (26,'User26@Mail.ru','n26');\n"
           "INSERT INTO users VALUES (27,'User27@Mail.ru','n27');\n"
           "INSERT INTO users VALUES (28,'User28@Mail.ru','n28');\n"
           "INSERT INTO users VALUES (29,'User29@Mail.ru','n29');\n"
           "INSERT INTO users VALUES (30,'User30@Mail.ru','n30');\n"
           "INSERT INTO users VALUES (31,'User31@Mail.ru','n31');\n"
           "INSERT INTO users VALUES (32,'User32@Mail.ru','n32');\n"
           "INSERT INTO users VALUES (33,'User33@Mail.ru','n33');\n"
           "INSERT INTO users VALUES (34,'User34@Mail.ru','n34');\n"
           "INSERT INTO users VALUES (35,'User35@Mail.ru','n35');\n"
           "INSERT INTO users VALUES (36,'User36@Mail.ru','n36');\n"
           "INSERT INTO users VALUES (37,'User37@Mail.ru','n37');\n"
           "INSERT INTO users VALUES (38,'User38@Mail.ru','n38');\n"
           "INSERT INTO users VALUES (39,'User39@Mail.ru','n39');\n"
           "INSERT INTO users VALUES (40,'User40@Mail.ru','n40');\n"
           "INSERT INTO users VALUES (41,'User41@Mail.ru','n41');\n"
           "INSERT INTO users VALUES (42,'User42@Mail.ru','n42');\n"
           "INSERT INTO users VALUES (43,'User43@Mail.ru','n43');\n"
           "INSERT INTO users VALUES (44,'User44@Mail.ru','n44');\n"
           "INSERT INTO users VALUES (45,'User45@Mail.ru','n45');\n"
           "INSERT INTO users VALUES (46,'User46@Mail.ru','n46');\n"
           "INSERT INTO users VALUES (47,'User47@Mail.ru','n47');\n"
           "INSERT INTO users VALUES (48,'User48@Mail.ru','n48');\n"
           "INSERT INTO users VALUES (49,'User49@Mail.ru','n49');\n"
           "INSERT INTO users VALUES (50,'User50@Mail.ru','n50');\n"
           "INSERT INTO users VALUES (51,'User51@Mail.ru','n51');\n"
           "INSERT INTO users VALUES (52,'User52@Mail.ru','n52');\n"
           "INSERT INTO users VALUES (53,'User53@Mail.ru','n53');\n"
           "INSERT INTO users VALUES (54,'User54@Mail.ru','n54');\n"
           "INSERT INTO users VALUES (55,'User55@Mail.ru','n55');\n"
           "INSERT INTO users VALUES (56,'User56@Mail.ru','n56');\n"
           "INSERT INTO users VALUES (57,'User57@Mail.ru','n57');\n"
           "INSERT INTO users VALUES (58,'User58@Mail.ru','n58');\n"
           "INSERT INTO users VALUES (59,'User59@Mail.ru','n59');\n"
           "INSERT INTO users VALUES (60,'User60@Mail.ru','n60');\n"
           "INSERT INTO users VALUES (61,'User61@Mail.ru','n61');\n"
           "INSERT INTO users VALUES (62,'User62@Mail.ru','n62');\n"
           "INSERT INTO users VALUES (63,'User63@Mail.ru','n63');\n"
           "INSERT INTO users VALUES (64,'User64@Mail.ru','n64');\n"
           "INSERT INTO users VALUES (65,'User65@Mail.ru','n65');\n"
           "INSERT INTO users VALUES (66,'User66@Mail.ru','n66');\n"
           "INSERT INTO users VALUES (67,'User67@Mail.ru','n67');\n"
           "INSERT INTO users VALUES (68,'User68@Mail.ru','n68');\n"
           "INSERT INTO users VALUES (69,'User69@Mail.ru','n69');\n"
           "INSERT INTO users VALUES (70,'User70@Mail.ru','n70');\n"
           "INSERT INTO users VALUES (71,'User71@Mail.ru','n71');\n"
           "INSERT INTO users VALUES (72,'User72@Mail.ru','n72');\n"
           "INSERT INTO users VALUES (73,'User73@Mail.ru','n73');\n"
           "INSERT INTO users VALUES (74,'User74@Mail.ru','n74');\n"
           "INSERT INTO users VALUES (75,'User75@Mail.ru','n75');\n"
           "INSERT INTO users VALUES (76,'User76@Mail.ru','n76');\n"
           "INSERT INTO users VALUES (77,'User77@Mail.ru','n77');\n"
           "INSERT INTO users VALUES (78,'User78@Mail.ru','n78');\n"
           "INSERT INTO users VALUES (79,'User79@Mail.ru','n79');\n"
           "INSERT INTO users VALUES (80,'User80@Mail.ru','n80');\n"
           "INSERT INTO users VALUES (81,'User81@Mail.ru','n81');\n"
           "INSERT INTO users VALUES (82,'User82@Mail.ru','n82');\n"
           "INSERT INTO users VALUES (83,'User83@Mail.ru','n83');\n"
           "INSERT INTO users VALUES (84,'User84@Mail.ru','n84');\n"
           "INSERT INTO users VALUES (85,'User85@Mail.ru','n85');\n"
           "INSERT INTO users VALUES (86,'User86@Mail.ru','n86');\n"
           "INSERT INTO users VALUES (87,'User87@Mail.ru','n87');\n"
           "INSERT INTO users VALUES (88,'User88@Mail.ru','n88');\n"
           "INSERT INTO users VALUES (89,'User89@Mail.ru','n89');\n"
           "INSERT INTO users VALUES (90,'User90@Mail.ru','n90');\n"
           "INSERT INTO users VALUES (91,'User91@Mail.ru','n91');\n"
           "INSERT INTO users VALUES (92,'User92@Mail.ru','n92');\n"
           "INSERT INTO users VALUES (93,'User93@Mail.ru','n93');\n"
           "INSERT INTO users VALUES (94,'User94@Mail.ru','n94');\n"
           "INSERT INTO users VALUES (95,'User95@Mail.ru','n95');\n"
           "INSERT INTO users VALUES (96,'User96@Mail.ru','n96');\n"
           "INSERT INTO users VALUES (97,'User97@Mail.ru','n97');\n"
           "INSERT INTO users VALUES (98,'User98@Mail.ru','n98');\n"
           "INSERT INTO users VALUES (99,'User99@Mail.ru','n99');\n"
           "INSERT INTO users VALUES (100,'User100@Mail.ru','n100');\n"
           "INSERT INTO users VALUES (101,'User101@Mail.ru','n101');\n"
           "INSERT INTO users VALUES (102,'User102@Mail.ru','n102');\n"
           "INSERT INTO users VALUES (103,'User103@Mail.ru','n103');\n"
           "INSERT INTO users VALUES (104,'User104@Mail.ru','n104');\n"
           "INSERT INTO users VALUES (105,'User105@Mail.ru','n105');\n"
           "INSERT INTO users VALUES (106,'User106@Mail.ru','n106');\n"
           "INSERT INTO users VALUES (107,'User107@Mail.ru','n107');\n"
           "INSERT INTO users VALUES (108,'User108@Mail.ru','n108');\n"
           "INSERT INTO users VALUES (109,'User109@Mail.ru','n109');\n"
           "INSERT INTO users VALUES (110,'User110@Mail.ru','n110');\n"
           "INSERT INTO users VALUES (111,'User111@Mail.ru','n111');\n"
           "INSERT INTO users VALUES (112,'User112@Mail.ru','n112');\n"
           "INSERT INTO users VALUES (113,'User113@Mail.ru','n113');\n"
           "INSERT INTO users VALUES (114,'User114@Mail.ru','n114');\n"
           "INSERT INTO users VALUES (115,'User115@Mail.ru','n115');\n"
           "INSERT INTO users VALUES (116,'User116@Mail.ru','n116');\n"
           "INSERT INTO users VALUES (117,'User117@Mail.ru','n117');\n"
           "INSERT INTO users VALUES (118,'User118@Mail.ru','n118');\n"
           "INSERT INTO users VALUES (119,'User119@Mail.ru','n119');\n"
           "INSERT INTO users VALUES (120,'User120@Mail.ru','n120');\n"
           "INSERT INTO users VALUES (121,'User121@Mail.ru','n121');\n"
           "INSERT INTO users VALUES (122,'User122@Mail.ru','n122');\n"
           "INSERT INTO users VALUES (123,'User123@Mail.ru','n123');\n"
           "INSERT INTO users VALUES (124,'User124@Mail.ru','n124');\n"
           "INSERT INTO users VALUES (125,'User125@Mail.ru','n125');\n"
           "INSERT INTO users VALUES (126,'User126@Mail.ru','n126');\n"
           "INSERT INTO users VALUES (127,'User127@Mail.ru','n127');\n"
           "INSERT INTO users VALUES (128,'User128@Mail.ru','n128');\n"
           "INSERT INTO users VALUES (129,'User129@Mail.ru','n129');\n"
           "INSERT INTO users VALUES (130,'User130@Mail.ru','n130');\n"
           "INSERT INTO users VALUES (131,'User131@Mail.ru','n131');\n"
           "INSERT INTO users VALUES (132,'User132@Mail.ru','n132');\n"
           "INSERT INTO users VALUES (133,'User133@Mail.ru','n133');\n"
           "INSERT INTO users VALUES (134,'User134@Mail.ru','n134');\n"
           "INSERT INTO users VALUES (135,'User135@Mail.ru','n135');\n"
           "INSERT INTO users VALUES (136,'User136@Mail.ru','n136');\n"
           "INSERT INTO users VALUES (137,'User137@Mail.ru','n137');\n"
           "INSERT INTO users VALUES (138,'User138@Mail.ru','n138');\n"
           "INSERT INTO users VALUES (139,'User139@Mail.ru','n139');\n"
           "INSERT INTO users VALUES (140,'User140@Mail.ru','n140');\n"
           "INSERT INTO users VALUES (141,'User141@Mail.ru','n141');\n"
           "INSERT INTO users VALUES (142,'User142@Mail.ru','n142');\n"
           "INSERT INTO users VALUES (143,'User143@Mail.ru','n143');\n"
           "INSERT INTO users VALUES (144,'User144@Mail.ru','n144');\n"
           "INSERT INTO users VALUES (145,'User145@Mail.ru','n145');\n"
           "INSERT INTO users VALUES (146,'User146@Mail.ru','n146');\n"
           "INSERT INTO users VALUES (147,'User147@Mail.ru','n147');\n"
           "INSERT INTO users VALUES (148,'User148@Mail.ru','n148');\n"
           "INSERT INTO users VALUES (149,'User149@Mail.ru','n149');\n"
           "INSERT INTO users VALUES (150,'User150@Mail.ru','n150');\n"
           "INSERT INTO users VALUES (151,'User151@Mail.ru','n151');\n"
           "INSERT INTO users VALUES (152,'User152@Mail.ru','n152');\n"
           "INSERT INTO users VALUES (153,'User153@Mail.ru','n153');\n"
           "INSERT INTO users VALUES (154,'User154@Mail.ru','n154');\n"
           "INSERT INTO users VALUES (155,'User155@Mail.ru','n155');\n"
           "INSERT INTO users VALUES (156,'User156@Mail.ru','n156');\n"
           "INSERT INTO users VALUES (157,'User157@Mail.ru','n157');\n"
           "INSERT INTO users VALUES (158,'User158@Mail.ru','n158');\n"
           "INSERT INTO users VALUES (159,'User159@Mail.ru','n159');\n"
           "INSERT INTO users VALUES (160,'User160@Mail.ru','n160');\n"
           "INSERT INTO users VALUES (161,'User161@Mail.ru','n161');\n"
           "INSERT INTO users VALUES (162,'User162@Mail.ru','n162');\n"
           "INSERT INTO users VALUES (163,'User163@Mail.ru','n163');\n"
           "INSERT INTO users VALUES (164,'User164@Mail.ru','n164');\n"
           "INSERT INTO users VALUES (165,'User165@Mail.ru','n165');\n"
           "INSERT INTO users VALUES (166,'User166@Mail.ru','n166');\n"
           "INSERT INTO users VALUES (167,'User167@Mail.ru','n167');\n"
           "INSERT INTO users VALUES (168,'User168@Mail.ru','n168');\n"
           "INSERT INTO users VALUES (169,'User169@Mail.ru','n169');\n"
           "INSERT INTO users VALUES (170,'User170@Mail.ru','n170');\n"
           "INSERT INTO users VALUES (171,'User171@Mail.ru','n171');\n"
           "INSERT INTO users VALUES (172,'User172@Mail.ru','n172');\n"
           "INSERT INTO users VALUES (173,'User173@Mail.ru','n173');\n"
           "INSERT INTO users VALUES (174,'User174@Mail.ru','n174');\n"
           "INSERT INTO users VALUES (175,'User175@Mail.ru','n175');\n"
           "INSERT INTO users VALUES (176,'User176@Mail.ru','n176');\n"
           "INSERT INTO users VALUES (177,'User177@Mail.ru','n177');\n"
           "INSERT INTO users VALUES (178,'User178@Mail.ru','n178');\n"
           "INSERT INTO users VALUES (179,'User179@Mail.ru','n179');\n"
           "INSERT INTO users VALUES (180,'User180@Mail.ru','n180');\n"
           "INSERT INTO users VALUES (181,'User181@Mail.ru','n181');\n"
           "INSERT INTO users VALUES (182,'User182@Mail.ru','n182');\n"
           "INSERT INTO users VALUES (183,'User183@Mail.ru','n183');\n"
           "INSERT INTO users VALUES (184,'User184@Mail.ru','n184');\n"
           "INSERT INTO users VALUES (185,'User185@Mail.ru','n185');\n"
           "INSERT INTO users VALUES (186,'User186@Mail.ru','n186');\n"
           "INSERT INTO users VALUES (187,'User187@Mail.ru','n187');\n"
           "INSERT INTO users VALUES (188,'User188@Mail.ru','n188');\n"
           "INSERT INTO users VALUES (189,'User189@Mail.ru','n189');\n"
           "INSERT INTO users VALUES (190,'User190@Mail.ru','n190');\n"
           "INSERT INTO users VALUES (191,'User191@Mail.ru','n191');\n"
           "INSERT INTO users VALUES (192,'User192@Mail.ru','n192');\n"
           "INSERT INTO users VALUES (193,'User193@Mail.ru','n193');\n"
           "INSERT INTO users VALUES (194,'User194@Mail.ru','n194');\n"
           "INSERT INTO users VALUES (195,'User195@Mail.ru','n195');\n"
           "INSERT INTO users VALUES (196,'User196@Mail.ru','n196');\n"
           "INSERT INTO users VALUES (197,'User197@Mail.ru','n197');\n"
           "INSERT INTO users VALUES (198,'User198@Mail.ru','n198');\n"
           "INSERT INTO users VALUES (199,'User199@Mail.ru','n199');\n"
           "INSERT INTO users VALUES (200,'User200@Mail.ru','n200');\n",
  'expected': [[3, 0, 53, 'SEARCH users USING COVERING INDEX idx_users_lower_email (<expr>=?)']],
  'hint': 'CREATE INDEX … ON users (lower(email)); — функция входит в индекс.',
  'check': "EXPLAIN QUERY PLAN SELECT id FROM users WHERE lower(email) = 'user5@mail.ru'",
  'contains': ['SEARCH users USING INDEX'],
  'forbid': ['SCAN']},
 {'id': 'd3-prefix-range',
  'mode': 'sql',
  'title': 'Префиксный поиск как диапазон',
  'statement': "Нужны товары, название которых начинается с «Кн». Запрос с LIKE '%Кн%' просматривает "
               "таблицу. Выведите план запроса, который ищет по диапазону title >= 'Кн' AND title < 'Ко' "
               'через индекс idx_title (последняя команда — EXPLAIN QUERY PLAN SELECT …).',
  'starter': '-- EXPLAIN QUERY PLAN для диапазона по title\n',
  'setup': 'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL);\n'
           'CREATE INDEX idx_title ON products (title);\n'
           "INSERT INTO products VALUES (1,'Книга1');\n"
           "INSERT INTO products VALUES (2,'Кофе2');\n"
           "INSERT INTO products VALUES (3,'Чай3');\n"
           "INSERT INTO products VALUES (4,'Мышь4');\n"
           "INSERT INTO products VALUES (5,'Ноутбук5');\n"
           "INSERT INTO products VALUES (6,'Книга6');\n"
           "INSERT INTO products VALUES (7,'Кофе7');\n"
           "INSERT INTO products VALUES (8,'Чай8');\n"
           "INSERT INTO products VALUES (9,'Мышь9');\n"
           "INSERT INTO products VALUES (10,'Ноутбук10');\n"
           "INSERT INTO products VALUES (11,'Книга11');\n"
           "INSERT INTO products VALUES (12,'Кофе12');\n"
           "INSERT INTO products VALUES (13,'Чай13');\n"
           "INSERT INTO products VALUES (14,'Мышь14');\n"
           "INSERT INTO products VALUES (15,'Ноутбук15');\n"
           "INSERT INTO products VALUES (16,'Книга16');\n"
           "INSERT INTO products VALUES (17,'Кофе17');\n"
           "INSERT INTO products VALUES (18,'Чай18');\n"
           "INSERT INTO products VALUES (19,'Мышь19');\n"
           "INSERT INTO products VALUES (20,'Ноутбук20');\n"
           "INSERT INTO products VALUES (21,'Книга21');\n"
           "INSERT INTO products VALUES (22,'Кофе22');\n"
           "INSERT INTO products VALUES (23,'Чай23');\n"
           "INSERT INTO products VALUES (24,'Мышь24');\n"
           "INSERT INTO products VALUES (25,'Ноутбук25');\n"
           "INSERT INTO products VALUES (26,'Книга26');\n"
           "INSERT INTO products VALUES (27,'Кофе27');\n"
           "INSERT INTO products VALUES (28,'Чай28');\n"
           "INSERT INTO products VALUES (29,'Мышь29');\n"
           "INSERT INTO products VALUES (30,'Ноутбук30');\n"
           "INSERT INTO products VALUES (31,'Книга31');\n"
           "INSERT INTO products VALUES (32,'Кофе32');\n"
           "INSERT INTO products VALUES (33,'Чай33');\n"
           "INSERT INTO products VALUES (34,'Мышь34');\n"
           "INSERT INTO products VALUES (35,'Ноутбук35');\n"
           "INSERT INTO products VALUES (36,'Книга36');\n"
           "INSERT INTO products VALUES (37,'Кофе37');\n"
           "INSERT INTO products VALUES (38,'Чай38');\n"
           "INSERT INTO products VALUES (39,'Мышь39');\n"
           "INSERT INTO products VALUES (40,'Ноутбук40');\n"
           "INSERT INTO products VALUES (41,'Книга41');\n"
           "INSERT INTO products VALUES (42,'Кофе42');\n"
           "INSERT INTO products VALUES (43,'Чай43');\n"
           "INSERT INTO products VALUES (44,'Мышь44');\n"
           "INSERT INTO products VALUES (45,'Ноутбук45');\n"
           "INSERT INTO products VALUES (46,'Книга46');\n"
           "INSERT INTO products VALUES (47,'Кофе47');\n"
           "INSERT INTO products VALUES (48,'Чай48');\n"
           "INSERT INTO products VALUES (49,'Мышь49');\n"
           "INSERT INTO products VALUES (50,'Ноутбук50');\n"
           "INSERT INTO products VALUES (51,'Книга51');\n"
           "INSERT INTO products VALUES (52,'Кофе52');\n"
           "INSERT INTO products VALUES (53,'Чай53');\n"
           "INSERT INTO products VALUES (54,'Мышь54');\n"
           "INSERT INTO products VALUES (55,'Ноутбук55');\n"
           "INSERT INTO products VALUES (56,'Книга56');\n"
           "INSERT INTO products VALUES (57,'Кофе57');\n"
           "INSERT INTO products VALUES (58,'Чай58');\n"
           "INSERT INTO products VALUES (59,'Мышь59');\n"
           "INSERT INTO products VALUES (60,'Ноутбук60');\n"
           "INSERT INTO products VALUES (61,'Книга61');\n"
           "INSERT INTO products VALUES (62,'Кофе62');\n"
           "INSERT INTO products VALUES (63,'Чай63');\n"
           "INSERT INTO products VALUES (64,'Мышь64');\n"
           "INSERT INTO products VALUES (65,'Ноутбук65');\n"
           "INSERT INTO products VALUES (66,'Книга66');\n"
           "INSERT INTO products VALUES (67,'Кофе67');\n"
           "INSERT INTO products VALUES (68,'Чай68');\n"
           "INSERT INTO products VALUES (69,'Мышь69');\n"
           "INSERT INTO products VALUES (70,'Ноутбук70');\n"
           "INSERT INTO products VALUES (71,'Книга71');\n"
           "INSERT INTO products VALUES (72,'Кофе72');\n"
           "INSERT INTO products VALUES (73,'Чай73');\n"
           "INSERT INTO products VALUES (74,'Мышь74');\n"
           "INSERT INTO products VALUES (75,'Ноутбук75');\n"
           "INSERT INTO products VALUES (76,'Книга76');\n"
           "INSERT INTO products VALUES (77,'Кофе77');\n"
           "INSERT INTO products VALUES (78,'Чай78');\n"
           "INSERT INTO products VALUES (79,'Мышь79');\n"
           "INSERT INTO products VALUES (80,'Ноутбук80');\n"
           "INSERT INTO products VALUES (81,'Книга81');\n"
           "INSERT INTO products VALUES (82,'Кофе82');\n"
           "INSERT INTO products VALUES (83,'Чай83');\n"
           "INSERT INTO products VALUES (84,'Мышь84');\n"
           "INSERT INTO products VALUES (85,'Ноутбук85');\n"
           "INSERT INTO products VALUES (86,'Книга86');\n"
           "INSERT INTO products VALUES (87,'Кофе87');\n"
           "INSERT INTO products VALUES (88,'Чай88');\n"
           "INSERT INTO products VALUES (89,'Мышь89');\n"
           "INSERT INTO products VALUES (90,'Ноутбук90');\n"
           "INSERT INTO products VALUES (91,'Книга91');\n"
           "INSERT INTO products VALUES (92,'Кофе92');\n"
           "INSERT INTO products VALUES (93,'Чай93');\n"
           "INSERT INTO products VALUES (94,'Мышь94');\n"
           "INSERT INTO products VALUES (95,'Ноутбук95');\n"
           "INSERT INTO products VALUES (96,'Книга96');\n"
           "INSERT INTO products VALUES (97,'Кофе97');\n"
           "INSERT INTO products VALUES (98,'Чай98');\n"
           "INSERT INTO products VALUES (99,'Мышь99');\n"
           "INSERT INTO products VALUES (100,'Ноутбук100');\n"
           "INSERT INTO products VALUES (101,'Книга101');\n"
           "INSERT INTO products VALUES (102,'Кофе102');\n"
           "INSERT INTO products VALUES (103,'Чай103');\n"
           "INSERT INTO products VALUES (104,'Мышь104');\n"
           "INSERT INTO products VALUES (105,'Ноутбук105');\n"
           "INSERT INTO products VALUES (106,'Книга106');\n"
           "INSERT INTO products VALUES (107,'Кофе107');\n"
           "INSERT INTO products VALUES (108,'Чай108');\n"
           "INSERT INTO products VALUES (109,'Мышь109');\n"
           "INSERT INTO products VALUES (110,'Ноутбук110');\n"
           "INSERT INTO products VALUES (111,'Книга111');\n"
           "INSERT INTO products VALUES (112,'Кофе112');\n"
           "INSERT INTO products VALUES (113,'Чай113');\n"
           "INSERT INTO products VALUES (114,'Мышь114');\n"
           "INSERT INTO products VALUES (115,'Ноутбук115');\n"
           "INSERT INTO products VALUES (116,'Книга116');\n"
           "INSERT INTO products VALUES (117,'Кофе117');\n"
           "INSERT INTO products VALUES (118,'Чай118');\n"
           "INSERT INTO products VALUES (119,'Мышь119');\n"
           "INSERT INTO products VALUES (120,'Ноутбук120');\n"
           "INSERT INTO products VALUES (121,'Книга121');\n"
           "INSERT INTO products VALUES (122,'Кофе122');\n"
           "INSERT INTO products VALUES (123,'Чай123');\n"
           "INSERT INTO products VALUES (124,'Мышь124');\n"
           "INSERT INTO products VALUES (125,'Ноутбук125');\n"
           "INSERT INTO products VALUES (126,'Книга126');\n"
           "INSERT INTO products VALUES (127,'Кофе127');\n"
           "INSERT INTO products VALUES (128,'Чай128');\n"
           "INSERT INTO products VALUES (129,'Мышь129');\n"
           "INSERT INTO products VALUES (130,'Ноутбук130');\n"
           "INSERT INTO products VALUES (131,'Книга131');\n"
           "INSERT INTO products VALUES (132,'Кофе132');\n"
           "INSERT INTO products VALUES (133,'Чай133');\n"
           "INSERT INTO products VALUES (134,'Мышь134');\n"
           "INSERT INTO products VALUES (135,'Ноутбук135');\n"
           "INSERT INTO products VALUES (136,'Книга136');\n"
           "INSERT INTO products VALUES (137,'Кофе137');\n"
           "INSERT INTO products VALUES (138,'Чай138');\n"
           "INSERT INTO products VALUES (139,'Мышь139');\n"
           "INSERT INTO products VALUES (140,'Ноутбук140');\n"
           "INSERT INTO products VALUES (141,'Книга141');\n"
           "INSERT INTO products VALUES (142,'Кофе142');\n"
           "INSERT INTO products VALUES (143,'Чай143');\n"
           "INSERT INTO products VALUES (144,'Мышь144');\n"
           "INSERT INTO products VALUES (145,'Ноутбук145');\n"
           "INSERT INTO products VALUES (146,'Книга146');\n"
           "INSERT INTO products VALUES (147,'Кофе147');\n"
           "INSERT INTO products VALUES (148,'Чай148');\n"
           "INSERT INTO products VALUES (149,'Мышь149');\n"
           "INSERT INTO products VALUES (150,'Ноутбук150');\n"
           "INSERT INTO products VALUES (151,'Книга151');\n"
           "INSERT INTO products VALUES (152,'Кофе152');\n"
           "INSERT INTO products VALUES (153,'Чай153');\n"
           "INSERT INTO products VALUES (154,'Мышь154');\n"
           "INSERT INTO products VALUES (155,'Ноутбук155');\n"
           "INSERT INTO products VALUES (156,'Книга156');\n"
           "INSERT INTO products VALUES (157,'Кофе157');\n"
           "INSERT INTO products VALUES (158,'Чай158');\n"
           "INSERT INTO products VALUES (159,'Мышь159');\n"
           "INSERT INTO products VALUES (160,'Ноутбук160');\n"
           "INSERT INTO products VALUES (161,'Книга161');\n"
           "INSERT INTO products VALUES (162,'Кофе162');\n"
           "INSERT INTO products VALUES (163,'Чай163');\n"
           "INSERT INTO products VALUES (164,'Мышь164');\n"
           "INSERT INTO products VALUES (165,'Ноутбук165');\n"
           "INSERT INTO products VALUES (166,'Книга166');\n"
           "INSERT INTO products VALUES (167,'Кофе167');\n"
           "INSERT INTO products VALUES (168,'Чай168');\n"
           "INSERT INTO products VALUES (169,'Мышь169');\n"
           "INSERT INTO products VALUES (170,'Ноутбук170');\n"
           "INSERT INTO products VALUES (171,'Книга171');\n"
           "INSERT INTO products VALUES (172,'Кофе172');\n"
           "INSERT INTO products VALUES (173,'Чай173');\n"
           "INSERT INTO products VALUES (174,'Мышь174');\n"
           "INSERT INTO products VALUES (175,'Ноутбук175');\n"
           "INSERT INTO products VALUES (176,'Книга176');\n"
           "INSERT INTO products VALUES (177,'Кофе177');\n"
           "INSERT INTO products VALUES (178,'Чай178');\n"
           "INSERT INTO products VALUES (179,'Мышь179');\n"
           "INSERT INTO products VALUES (180,'Ноутбук180');\n"
           "INSERT INTO products VALUES (181,'Книга181');\n"
           "INSERT INTO products VALUES (182,'Кофе182');\n"
           "INSERT INTO products VALUES (183,'Чай183');\n"
           "INSERT INTO products VALUES (184,'Мышь184');\n"
           "INSERT INTO products VALUES (185,'Ноутбук185');\n"
           "INSERT INTO products VALUES (186,'Книга186');\n"
           "INSERT INTO products VALUES (187,'Кофе187');\n"
           "INSERT INTO products VALUES (188,'Чай188');\n"
           "INSERT INTO products VALUES (189,'Мышь189');\n"
           "INSERT INTO products VALUES (190,'Ноутбук190');\n"
           "INSERT INTO products VALUES (191,'Книга191');\n"
           "INSERT INTO products VALUES (192,'Кофе192');\n"
           "INSERT INTO products VALUES (193,'Чай193');\n"
           "INSERT INTO products VALUES (194,'Мышь194');\n"
           "INSERT INTO products VALUES (195,'Ноутбук195');\n"
           "INSERT INTO products VALUES (196,'Книга196');\n"
           "INSERT INTO products VALUES (197,'Кофе197');\n"
           "INSERT INTO products VALUES (198,'Чай198');\n"
           "INSERT INTO products VALUES (199,'Мышь199');\n"
           "INSERT INTO products VALUES (200,'Ноутбук200');\n",
  'expected': [[2, 0, 156, 'SEARCH products USING COVERING INDEX idx_title (title>? AND title<?)']],
  'hint': "Диапазон по упорядоченному столбцу: title >= 'Кн' AND title < 'Ко' заменяет префикс «Кн%».",
  'contains': ['SEARCH products USING', '(title>? AND title<?)'],
  'forbid': ['SCAN']},
 {'id': 'd3-covering',
  'mode': 'sql',
  'title': 'Покрывающий индекс',
  'statement': 'Запрос SELECT status, total FROM orders WHERE customer_id = 7 читает таблицу. Создайте один '
               'индекс, который покроет его целиком: в плане должно появиться USING COVERING INDEX.',
  'starter': '-- покрывающий индекс для SELECT status, total ... WHERE customer_id = 7\nCREATE INDEX\n',
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, city TEXT NOT NULL, '
           'created TEXT NOT NULL, status TEXT NOT NULL, total INTEGER NOT NULL);\n'
           "INSERT INTO orders VALUES (1,1,'Казань','2024-02-02','new',101);\n"
           "INSERT INTO orders VALUES (2,2,'Тверь','2024-03-03','cancelled',102);\n"
           "INSERT INTO orders VALUES (3,3,'Омск','2024-04-04','paid',103);\n"
           "INSERT INTO orders VALUES (4,4,'Москва','2024-05-05','new',104);\n"
           "INSERT INTO orders VALUES (5,5,'Казань','2024-06-06','cancelled',105);\n"
           "INSERT INTO orders VALUES (6,6,'Тверь','2024-07-07','paid',106);\n"
           "INSERT INTO orders VALUES (7,7,'Омск','2024-08-08','new',107);\n"
           "INSERT INTO orders VALUES (8,8,'Москва','2024-09-09','cancelled',108);\n"
           "INSERT INTO orders VALUES (9,9,'Казань','2024-10-10','paid',109);\n"
           "INSERT INTO orders VALUES (10,10,'Тверь','2024-11-11','new',110);\n"
           "INSERT INTO orders VALUES (11,11,'Омск','2024-12-12','cancelled',111);\n"
           "INSERT INTO orders VALUES (12,12,'Москва','2024-01-13','paid',112);\n"
           "INSERT INTO orders VALUES (13,13,'Казань','2024-02-14','new',113);\n"
           "INSERT INTO orders VALUES (14,14,'Тверь','2024-03-15','cancelled',114);\n"
           "INSERT INTO orders VALUES (15,15,'Омск','2024-04-16','paid',115);\n"
           "INSERT INTO orders VALUES (16,16,'Москва','2024-05-17','new',116);\n"
           "INSERT INTO orders VALUES (17,17,'Казань','2024-06-18','cancelled',117);\n"
           "INSERT INTO orders VALUES (18,18,'Тверь','2024-07-19','paid',118);\n"
           "INSERT INTO orders VALUES (19,19,'Омск','2024-08-20','new',119);\n"
           "INSERT INTO orders VALUES (20,20,'Москва','2024-09-21','cancelled',120);\n"
           "INSERT INTO orders VALUES (21,21,'Казань','2024-10-22','paid',121);\n"
           "INSERT INTO orders VALUES (22,22,'Тверь','2024-11-23','new',122);\n"
           "INSERT INTO orders VALUES (23,23,'Омск','2024-12-24','cancelled',123);\n"
           "INSERT INTO orders VALUES (24,24,'Москва','2024-01-25','paid',124);\n"
           "INSERT INTO orders VALUES (25,25,'Казань','2024-02-26','new',125);\n"
           "INSERT INTO orders VALUES (26,26,'Тверь','2024-03-27','cancelled',126);\n"
           "INSERT INTO orders VALUES (27,27,'Омск','2024-04-28','paid',127);\n"
           "INSERT INTO orders VALUES (28,28,'Москва','2024-05-01','new',128);\n"
           "INSERT INTO orders VALUES (29,29,'Казань','2024-06-02','cancelled',129);\n"
           "INSERT INTO orders VALUES (30,30,'Тверь','2024-07-03','paid',130);\n"
           "INSERT INTO orders VALUES (31,31,'Омск','2024-08-04','new',131);\n"
           "INSERT INTO orders VALUES (32,32,'Москва','2024-09-05','cancelled',132);\n"
           "INSERT INTO orders VALUES (33,33,'Казань','2024-10-06','paid',133);\n"
           "INSERT INTO orders VALUES (34,34,'Тверь','2024-11-07','new',134);\n"
           "INSERT INTO orders VALUES (35,35,'Омск','2024-12-08','cancelled',135);\n"
           "INSERT INTO orders VALUES (36,36,'Москва','2024-01-09','paid',136);\n"
           "INSERT INTO orders VALUES (37,37,'Казань','2024-02-10','new',137);\n"
           "INSERT INTO orders VALUES (38,38,'Тверь','2024-03-11','cancelled',138);\n"
           "INSERT INTO orders VALUES (39,39,'Омск','2024-04-12','paid',139);\n"
           "INSERT INTO orders VALUES (40,40,'Москва','2024-05-13','new',140);\n"
           "INSERT INTO orders VALUES (41,41,'Казань','2024-06-14','cancelled',141);\n"
           "INSERT INTO orders VALUES (42,42,'Тверь','2024-07-15','paid',142);\n"
           "INSERT INTO orders VALUES (43,43,'Омск','2024-08-16','new',143);\n"
           "INSERT INTO orders VALUES (44,44,'Москва','2024-09-17','cancelled',144);\n"
           "INSERT INTO orders VALUES (45,45,'Казань','2024-10-18','paid',145);\n"
           "INSERT INTO orders VALUES (46,46,'Тверь','2024-11-19','new',146);\n"
           "INSERT INTO orders VALUES (47,47,'Омск','2024-12-20','cancelled',147);\n"
           "INSERT INTO orders VALUES (48,48,'Москва','2024-01-21','paid',148);\n"
           "INSERT INTO orders VALUES (49,49,'Казань','2024-02-22','new',149);\n"
           "INSERT INTO orders VALUES (50,0,'Тверь','2024-03-23','cancelled',150);\n"
           "INSERT INTO orders VALUES (51,1,'Омск','2024-04-24','paid',151);\n"
           "INSERT INTO orders VALUES (52,2,'Москва','2024-05-25','new',152);\n"
           "INSERT INTO orders VALUES (53,3,'Казань','2024-06-26','cancelled',153);\n"
           "INSERT INTO orders VALUES (54,4,'Тверь','2024-07-27','paid',154);\n"
           "INSERT INTO orders VALUES (55,5,'Омск','2024-08-28','new',155);\n"
           "INSERT INTO orders VALUES (56,6,'Москва','2024-09-01','cancelled',156);\n"
           "INSERT INTO orders VALUES (57,7,'Казань','2024-10-02','paid',157);\n"
           "INSERT INTO orders VALUES (58,8,'Тверь','2024-11-03','new',158);\n"
           "INSERT INTO orders VALUES (59,9,'Омск','2024-12-04','cancelled',159);\n"
           "INSERT INTO orders VALUES (60,10,'Москва','2024-01-05','paid',160);\n"
           "INSERT INTO orders VALUES (61,11,'Казань','2024-02-06','new',161);\n"
           "INSERT INTO orders VALUES (62,12,'Тверь','2024-03-07','cancelled',162);\n"
           "INSERT INTO orders VALUES (63,13,'Омск','2024-04-08','paid',163);\n"
           "INSERT INTO orders VALUES (64,14,'Москва','2024-05-09','new',164);\n"
           "INSERT INTO orders VALUES (65,15,'Казань','2024-06-10','cancelled',165);\n"
           "INSERT INTO orders VALUES (66,16,'Тверь','2024-07-11','paid',166);\n"
           "INSERT INTO orders VALUES (67,17,'Омск','2024-08-12','new',167);\n"
           "INSERT INTO orders VALUES (68,18,'Москва','2024-09-13','cancelled',168);\n"
           "INSERT INTO orders VALUES (69,19,'Казань','2024-10-14','paid',169);\n"
           "INSERT INTO orders VALUES (70,20,'Тверь','2024-11-15','new',170);\n"
           "INSERT INTO orders VALUES (71,21,'Омск','2024-12-16','cancelled',171);\n"
           "INSERT INTO orders VALUES (72,22,'Москва','2024-01-17','paid',172);\n"
           "INSERT INTO orders VALUES (73,23,'Казань','2024-02-18','new',173);\n"
           "INSERT INTO orders VALUES (74,24,'Тверь','2024-03-19','cancelled',174);\n"
           "INSERT INTO orders VALUES (75,25,'Омск','2024-04-20','paid',175);\n"
           "INSERT INTO orders VALUES (76,26,'Москва','2024-05-21','new',176);\n"
           "INSERT INTO orders VALUES (77,27,'Казань','2024-06-22','cancelled',177);\n"
           "INSERT INTO orders VALUES (78,28,'Тверь','2024-07-23','paid',178);\n"
           "INSERT INTO orders VALUES (79,29,'Омск','2024-08-24','new',179);\n"
           "INSERT INTO orders VALUES (80,30,'Москва','2024-09-25','cancelled',180);\n"
           "INSERT INTO orders VALUES (81,31,'Казань','2024-10-26','paid',181);\n"
           "INSERT INTO orders VALUES (82,32,'Тверь','2024-11-27','new',182);\n"
           "INSERT INTO orders VALUES (83,33,'Омск','2024-12-28','cancelled',183);\n"
           "INSERT INTO orders VALUES (84,34,'Москва','2024-01-01','paid',184);\n"
           "INSERT INTO orders VALUES (85,35,'Казань','2024-02-02','new',185);\n"
           "INSERT INTO orders VALUES (86,36,'Тверь','2024-03-03','cancelled',186);\n"
           "INSERT INTO orders VALUES (87,37,'Омск','2024-04-04','paid',187);\n"
           "INSERT INTO orders VALUES (88,38,'Москва','2024-05-05','new',188);\n"
           "INSERT INTO orders VALUES (89,39,'Казань','2024-06-06','cancelled',189);\n"
           "INSERT INTO orders VALUES (90,40,'Тверь','2024-07-07','paid',190);\n"
           "INSERT INTO orders VALUES (91,41,'Омск','2024-08-08','new',191);\n"
           "INSERT INTO orders VALUES (92,42,'Москва','2024-09-09','cancelled',192);\n"
           "INSERT INTO orders VALUES (93,43,'Казань','2024-10-10','paid',193);\n"
           "INSERT INTO orders VALUES (94,44,'Тверь','2024-11-11','new',194);\n"
           "INSERT INTO orders VALUES (95,45,'Омск','2024-12-12','cancelled',195);\n"
           "INSERT INTO orders VALUES (96,46,'Москва','2024-01-13','paid',196);\n"
           "INSERT INTO orders VALUES (97,47,'Казань','2024-02-14','new',197);\n"
           "INSERT INTO orders VALUES (98,48,'Тверь','2024-03-15','cancelled',198);\n"
           "INSERT INTO orders VALUES (99,49,'Омск','2024-04-16','paid',199);\n"
           "INSERT INTO orders VALUES (100,0,'Москва','2024-05-17','new',200);\n"
           "INSERT INTO orders VALUES (101,1,'Казань','2024-06-18','cancelled',201);\n"
           "INSERT INTO orders VALUES (102,2,'Тверь','2024-07-19','paid',202);\n"
           "INSERT INTO orders VALUES (103,3,'Омск','2024-08-20','new',203);\n"
           "INSERT INTO orders VALUES (104,4,'Москва','2024-09-21','cancelled',204);\n"
           "INSERT INTO orders VALUES (105,5,'Казань','2024-10-22','paid',205);\n"
           "INSERT INTO orders VALUES (106,6,'Тверь','2024-11-23','new',206);\n"
           "INSERT INTO orders VALUES (107,7,'Омск','2024-12-24','cancelled',207);\n"
           "INSERT INTO orders VALUES (108,8,'Москва','2024-01-25','paid',208);\n"
           "INSERT INTO orders VALUES (109,9,'Казань','2024-02-26','new',209);\n"
           "INSERT INTO orders VALUES (110,10,'Тверь','2024-03-27','cancelled',210);\n"
           "INSERT INTO orders VALUES (111,11,'Омск','2024-04-28','paid',211);\n"
           "INSERT INTO orders VALUES (112,12,'Москва','2024-05-01','new',212);\n"
           "INSERT INTO orders VALUES (113,13,'Казань','2024-06-02','cancelled',213);\n"
           "INSERT INTO orders VALUES (114,14,'Тверь','2024-07-03','paid',214);\n"
           "INSERT INTO orders VALUES (115,15,'Омск','2024-08-04','new',215);\n"
           "INSERT INTO orders VALUES (116,16,'Москва','2024-09-05','cancelled',216);\n"
           "INSERT INTO orders VALUES (117,17,'Казань','2024-10-06','paid',217);\n"
           "INSERT INTO orders VALUES (118,18,'Тверь','2024-11-07','new',218);\n"
           "INSERT INTO orders VALUES (119,19,'Омск','2024-12-08','cancelled',219);\n"
           "INSERT INTO orders VALUES (120,20,'Москва','2024-01-09','paid',220);\n"
           "INSERT INTO orders VALUES (121,21,'Казань','2024-02-10','new',221);\n"
           "INSERT INTO orders VALUES (122,22,'Тверь','2024-03-11','cancelled',222);\n"
           "INSERT INTO orders VALUES (123,23,'Омск','2024-04-12','paid',223);\n"
           "INSERT INTO orders VALUES (124,24,'Москва','2024-05-13','new',224);\n"
           "INSERT INTO orders VALUES (125,25,'Казань','2024-06-14','cancelled',225);\n"
           "INSERT INTO orders VALUES (126,26,'Тверь','2024-07-15','paid',226);\n"
           "INSERT INTO orders VALUES (127,27,'Омск','2024-08-16','new',227);\n"
           "INSERT INTO orders VALUES (128,28,'Москва','2024-09-17','cancelled',228);\n"
           "INSERT INTO orders VALUES (129,29,'Казань','2024-10-18','paid',229);\n"
           "INSERT INTO orders VALUES (130,30,'Тверь','2024-11-19','new',230);\n"
           "INSERT INTO orders VALUES (131,31,'Омск','2024-12-20','cancelled',231);\n"
           "INSERT INTO orders VALUES (132,32,'Москва','2024-01-21','paid',232);\n"
           "INSERT INTO orders VALUES (133,33,'Казань','2024-02-22','new',233);\n"
           "INSERT INTO orders VALUES (134,34,'Тверь','2024-03-23','cancelled',234);\n"
           "INSERT INTO orders VALUES (135,35,'Омск','2024-04-24','paid',235);\n"
           "INSERT INTO orders VALUES (136,36,'Москва','2024-05-25','new',236);\n"
           "INSERT INTO orders VALUES (137,37,'Казань','2024-06-26','cancelled',237);\n"
           "INSERT INTO orders VALUES (138,38,'Тверь','2024-07-27','paid',238);\n"
           "INSERT INTO orders VALUES (139,39,'Омск','2024-08-28','new',239);\n"
           "INSERT INTO orders VALUES (140,40,'Москва','2024-09-01','cancelled',240);\n"
           "INSERT INTO orders VALUES (141,41,'Казань','2024-10-02','paid',241);\n"
           "INSERT INTO orders VALUES (142,42,'Тверь','2024-11-03','new',242);\n"
           "INSERT INTO orders VALUES (143,43,'Омск','2024-12-04','cancelled',243);\n"
           "INSERT INTO orders VALUES (144,44,'Москва','2024-01-05','paid',244);\n"
           "INSERT INTO orders VALUES (145,45,'Казань','2024-02-06','new',245);\n"
           "INSERT INTO orders VALUES (146,46,'Тверь','2024-03-07','cancelled',246);\n"
           "INSERT INTO orders VALUES (147,47,'Омск','2024-04-08','paid',247);\n"
           "INSERT INTO orders VALUES (148,48,'Москва','2024-05-09','new',248);\n"
           "INSERT INTO orders VALUES (149,49,'Казань','2024-06-10','cancelled',249);\n"
           "INSERT INTO orders VALUES (150,0,'Тверь','2024-07-11','paid',250);\n"
           "INSERT INTO orders VALUES (151,1,'Омск','2024-08-12','new',251);\n"
           "INSERT INTO orders VALUES (152,2,'Москва','2024-09-13','cancelled',252);\n"
           "INSERT INTO orders VALUES (153,3,'Казань','2024-10-14','paid',253);\n"
           "INSERT INTO orders VALUES (154,4,'Тверь','2024-11-15','new',254);\n"
           "INSERT INTO orders VALUES (155,5,'Омск','2024-12-16','cancelled',255);\n"
           "INSERT INTO orders VALUES (156,6,'Москва','2024-01-17','paid',256);\n"
           "INSERT INTO orders VALUES (157,7,'Казань','2024-02-18','new',257);\n"
           "INSERT INTO orders VALUES (158,8,'Тверь','2024-03-19','cancelled',258);\n"
           "INSERT INTO orders VALUES (159,9,'Омск','2024-04-20','paid',259);\n"
           "INSERT INTO orders VALUES (160,10,'Москва','2024-05-21','new',260);\n"
           "INSERT INTO orders VALUES (161,11,'Казань','2024-06-22','cancelled',261);\n"
           "INSERT INTO orders VALUES (162,12,'Тверь','2024-07-23','paid',262);\n"
           "INSERT INTO orders VALUES (163,13,'Омск','2024-08-24','new',263);\n"
           "INSERT INTO orders VALUES (164,14,'Москва','2024-09-25','cancelled',264);\n"
           "INSERT INTO orders VALUES (165,15,'Казань','2024-10-26','paid',265);\n"
           "INSERT INTO orders VALUES (166,16,'Тверь','2024-11-27','new',266);\n"
           "INSERT INTO orders VALUES (167,17,'Омск','2024-12-28','cancelled',267);\n"
           "INSERT INTO orders VALUES (168,18,'Москва','2024-01-01','paid',268);\n"
           "INSERT INTO orders VALUES (169,19,'Казань','2024-02-02','new',269);\n"
           "INSERT INTO orders VALUES (170,20,'Тверь','2024-03-03','cancelled',270);\n"
           "INSERT INTO orders VALUES (171,21,'Омск','2024-04-04','paid',271);\n"
           "INSERT INTO orders VALUES (172,22,'Москва','2024-05-05','new',272);\n"
           "INSERT INTO orders VALUES (173,23,'Казань','2024-06-06','cancelled',273);\n"
           "INSERT INTO orders VALUES (174,24,'Тверь','2024-07-07','paid',274);\n"
           "INSERT INTO orders VALUES (175,25,'Омск','2024-08-08','new',275);\n"
           "INSERT INTO orders VALUES (176,26,'Москва','2024-09-09','cancelled',276);\n"
           "INSERT INTO orders VALUES (177,27,'Казань','2024-10-10','paid',277);\n"
           "INSERT INTO orders VALUES (178,28,'Тверь','2024-11-11','new',278);\n"
           "INSERT INTO orders VALUES (179,29,'Омск','2024-12-12','cancelled',279);\n"
           "INSERT INTO orders VALUES (180,30,'Москва','2024-01-13','paid',280);\n"
           "INSERT INTO orders VALUES (181,31,'Казань','2024-02-14','new',281);\n"
           "INSERT INTO orders VALUES (182,32,'Тверь','2024-03-15','cancelled',282);\n"
           "INSERT INTO orders VALUES (183,33,'Омск','2024-04-16','paid',283);\n"
           "INSERT INTO orders VALUES (184,34,'Москва','2024-05-17','new',284);\n"
           "INSERT INTO orders VALUES (185,35,'Казань','2024-06-18','cancelled',285);\n"
           "INSERT INTO orders VALUES (186,36,'Тверь','2024-07-19','paid',286);\n"
           "INSERT INTO orders VALUES (187,37,'Омск','2024-08-20','new',287);\n"
           "INSERT INTO orders VALUES (188,38,'Москва','2024-09-21','cancelled',288);\n"
           "INSERT INTO orders VALUES (189,39,'Казань','2024-10-22','paid',289);\n"
           "INSERT INTO orders VALUES (190,40,'Тверь','2024-11-23','new',290);\n"
           "INSERT INTO orders VALUES (191,41,'Омск','2024-12-24','cancelled',291);\n"
           "INSERT INTO orders VALUES (192,42,'Москва','2024-01-25','paid',292);\n"
           "INSERT INTO orders VALUES (193,43,'Казань','2024-02-26','new',293);\n"
           "INSERT INTO orders VALUES (194,44,'Тверь','2024-03-27','cancelled',294);\n"
           "INSERT INTO orders VALUES (195,45,'Омск','2024-04-28','paid',295);\n"
           "INSERT INTO orders VALUES (196,46,'Москва','2024-05-01','new',296);\n"
           "INSERT INTO orders VALUES (197,47,'Казань','2024-06-02','cancelled',297);\n"
           "INSERT INTO orders VALUES (198,48,'Тверь','2024-07-03','paid',298);\n"
           "INSERT INTO orders VALUES (199,49,'Омск','2024-08-04','new',299);\n"
           "INSERT INTO orders VALUES (200,0,'Москва','2024-09-05','cancelled',300);\n"
           "INSERT INTO orders VALUES (201,1,'Казань','2024-10-06','paid',301);\n"
           "INSERT INTO orders VALUES (202,2,'Тверь','2024-11-07','new',302);\n"
           "INSERT INTO orders VALUES (203,3,'Омск','2024-12-08','cancelled',303);\n"
           "INSERT INTO orders VALUES (204,4,'Москва','2024-01-09','paid',304);\n"
           "INSERT INTO orders VALUES (205,5,'Казань','2024-02-10','new',305);\n"
           "INSERT INTO orders VALUES (206,6,'Тверь','2024-03-11','cancelled',306);\n"
           "INSERT INTO orders VALUES (207,7,'Омск','2024-04-12','paid',307);\n"
           "INSERT INTO orders VALUES (208,8,'Москва','2024-05-13','new',308);\n"
           "INSERT INTO orders VALUES (209,9,'Казань','2024-06-14','cancelled',309);\n"
           "INSERT INTO orders VALUES (210,10,'Тверь','2024-07-15','paid',310);\n"
           "INSERT INTO orders VALUES (211,11,'Омск','2024-08-16','new',311);\n"
           "INSERT INTO orders VALUES (212,12,'Москва','2024-09-17','cancelled',312);\n"
           "INSERT INTO orders VALUES (213,13,'Казань','2024-10-18','paid',313);\n"
           "INSERT INTO orders VALUES (214,14,'Тверь','2024-11-19','new',314);\n"
           "INSERT INTO orders VALUES (215,15,'Омск','2024-12-20','cancelled',315);\n"
           "INSERT INTO orders VALUES (216,16,'Москва','2024-01-21','paid',316);\n"
           "INSERT INTO orders VALUES (217,17,'Казань','2024-02-22','new',317);\n"
           "INSERT INTO orders VALUES (218,18,'Тверь','2024-03-23','cancelled',318);\n"
           "INSERT INTO orders VALUES (219,19,'Омск','2024-04-24','paid',319);\n"
           "INSERT INTO orders VALUES (220,20,'Москва','2024-05-25','new',320);\n"
           "INSERT INTO orders VALUES (221,21,'Казань','2024-06-26','cancelled',321);\n"
           "INSERT INTO orders VALUES (222,22,'Тверь','2024-07-27','paid',322);\n"
           "INSERT INTO orders VALUES (223,23,'Омск','2024-08-28','new',323);\n"
           "INSERT INTO orders VALUES (224,24,'Москва','2024-09-01','cancelled',324);\n"
           "INSERT INTO orders VALUES (225,25,'Казань','2024-10-02','paid',325);\n"
           "INSERT INTO orders VALUES (226,26,'Тверь','2024-11-03','new',326);\n"
           "INSERT INTO orders VALUES (227,27,'Омск','2024-12-04','cancelled',327);\n"
           "INSERT INTO orders VALUES (228,28,'Москва','2024-01-05','paid',328);\n"
           "INSERT INTO orders VALUES (229,29,'Казань','2024-02-06','new',329);\n"
           "INSERT INTO orders VALUES (230,30,'Тверь','2024-03-07','cancelled',330);\n"
           "INSERT INTO orders VALUES (231,31,'Омск','2024-04-08','paid',331);\n"
           "INSERT INTO orders VALUES (232,32,'Москва','2024-05-09','new',332);\n"
           "INSERT INTO orders VALUES (233,33,'Казань','2024-06-10','cancelled',333);\n"
           "INSERT INTO orders VALUES (234,34,'Тверь','2024-07-11','paid',334);\n"
           "INSERT INTO orders VALUES (235,35,'Омск','2024-08-12','new',335);\n"
           "INSERT INTO orders VALUES (236,36,'Москва','2024-09-13','cancelled',336);\n"
           "INSERT INTO orders VALUES (237,37,'Казань','2024-10-14','paid',337);\n"
           "INSERT INTO orders VALUES (238,38,'Тверь','2024-11-15','new',338);\n"
           "INSERT INTO orders VALUES (239,39,'Омск','2024-12-16','cancelled',339);\n"
           "INSERT INTO orders VALUES (240,40,'Москва','2024-01-17','paid',340);\n"
           "INSERT INTO orders VALUES (241,41,'Казань','2024-02-18','new',341);\n"
           "INSERT INTO orders VALUES (242,42,'Тверь','2024-03-19','cancelled',342);\n"
           "INSERT INTO orders VALUES (243,43,'Омск','2024-04-20','paid',343);\n"
           "INSERT INTO orders VALUES (244,44,'Москва','2024-05-21','new',344);\n"
           "INSERT INTO orders VALUES (245,45,'Казань','2024-06-22','cancelled',345);\n"
           "INSERT INTO orders VALUES (246,46,'Тверь','2024-07-23','paid',346);\n"
           "INSERT INTO orders VALUES (247,47,'Омск','2024-08-24','new',347);\n"
           "INSERT INTO orders VALUES (248,48,'Москва','2024-09-25','cancelled',348);\n"
           "INSERT INTO orders VALUES (249,49,'Казань','2024-10-26','paid',349);\n"
           "INSERT INTO orders VALUES (250,0,'Тверь','2024-11-27','new',350);\n"
           "INSERT INTO orders VALUES (251,1,'Омск','2024-12-28','cancelled',351);\n"
           "INSERT INTO orders VALUES (252,2,'Москва','2024-01-01','paid',352);\n"
           "INSERT INTO orders VALUES (253,3,'Казань','2024-02-02','new',353);\n"
           "INSERT INTO orders VALUES (254,4,'Тверь','2024-03-03','cancelled',354);\n"
           "INSERT INTO orders VALUES (255,5,'Омск','2024-04-04','paid',355);\n"
           "INSERT INTO orders VALUES (256,6,'Москва','2024-05-05','new',356);\n"
           "INSERT INTO orders VALUES (257,7,'Казань','2024-06-06','cancelled',357);\n"
           "INSERT INTO orders VALUES (258,8,'Тверь','2024-07-07','paid',358);\n"
           "INSERT INTO orders VALUES (259,9,'Омск','2024-08-08','new',359);\n"
           "INSERT INTO orders VALUES (260,10,'Москва','2024-09-09','cancelled',360);\n"
           "INSERT INTO orders VALUES (261,11,'Казань','2024-10-10','paid',361);\n"
           "INSERT INTO orders VALUES (262,12,'Тверь','2024-11-11','new',362);\n"
           "INSERT INTO orders VALUES (263,13,'Омск','2024-12-12','cancelled',363);\n"
           "INSERT INTO orders VALUES (264,14,'Москва','2024-01-13','paid',364);\n"
           "INSERT INTO orders VALUES (265,15,'Казань','2024-02-14','new',365);\n"
           "INSERT INTO orders VALUES (266,16,'Тверь','2024-03-15','cancelled',366);\n"
           "INSERT INTO orders VALUES (267,17,'Омск','2024-04-16','paid',367);\n"
           "INSERT INTO orders VALUES (268,18,'Москва','2024-05-17','new',368);\n"
           "INSERT INTO orders VALUES (269,19,'Казань','2024-06-18','cancelled',369);\n"
           "INSERT INTO orders VALUES (270,20,'Тверь','2024-07-19','paid',370);\n"
           "INSERT INTO orders VALUES (271,21,'Омск','2024-08-20','new',371);\n"
           "INSERT INTO orders VALUES (272,22,'Москва','2024-09-21','cancelled',372);\n"
           "INSERT INTO orders VALUES (273,23,'Казань','2024-10-22','paid',373);\n"
           "INSERT INTO orders VALUES (274,24,'Тверь','2024-11-23','new',374);\n"
           "INSERT INTO orders VALUES (275,25,'Омск','2024-12-24','cancelled',375);\n"
           "INSERT INTO orders VALUES (276,26,'Москва','2024-01-25','paid',376);\n"
           "INSERT INTO orders VALUES (277,27,'Казань','2024-02-26','new',377);\n"
           "INSERT INTO orders VALUES (278,28,'Тверь','2024-03-27','cancelled',378);\n"
           "INSERT INTO orders VALUES (279,29,'Омск','2024-04-28','paid',379);\n"
           "INSERT INTO orders VALUES (280,30,'Москва','2024-05-01','new',380);\n"
           "INSERT INTO orders VALUES (281,31,'Казань','2024-06-02','cancelled',381);\n"
           "INSERT INTO orders VALUES (282,32,'Тверь','2024-07-03','paid',382);\n"
           "INSERT INTO orders VALUES (283,33,'Омск','2024-08-04','new',383);\n"
           "INSERT INTO orders VALUES (284,34,'Москва','2024-09-05','cancelled',384);\n"
           "INSERT INTO orders VALUES (285,35,'Казань','2024-10-06','paid',385);\n"
           "INSERT INTO orders VALUES (286,36,'Тверь','2024-11-07','new',386);\n"
           "INSERT INTO orders VALUES (287,37,'Омск','2024-12-08','cancelled',387);\n"
           "INSERT INTO orders VALUES (288,38,'Москва','2024-01-09','paid',388);\n"
           "INSERT INTO orders VALUES (289,39,'Казань','2024-02-10','new',389);\n"
           "INSERT INTO orders VALUES (290,40,'Тверь','2024-03-11','cancelled',390);\n"
           "INSERT INTO orders VALUES (291,41,'Омск','2024-04-12','paid',391);\n"
           "INSERT INTO orders VALUES (292,42,'Москва','2024-05-13','new',392);\n"
           "INSERT INTO orders VALUES (293,43,'Казань','2024-06-14','cancelled',393);\n"
           "INSERT INTO orders VALUES (294,44,'Тверь','2024-07-15','paid',394);\n"
           "INSERT INTO orders VALUES (295,45,'Омск','2024-08-16','new',395);\n"
           "INSERT INTO orders VALUES (296,46,'Москва','2024-09-17','cancelled',396);\n"
           "INSERT INTO orders VALUES (297,47,'Казань','2024-10-18','paid',397);\n"
           "INSERT INTO orders VALUES (298,48,'Тверь','2024-11-19','new',398);\n"
           "INSERT INTO orders VALUES (299,49,'Омск','2024-12-20','cancelled',399);\n"
           "INSERT INTO orders VALUES (300,0,'Москва','2024-01-21','paid',400);\n",
  'expected': [[2, 0, 55, 'SEARCH orders USING COVERING INDEX idx_cover (customer_id=?)']],
  'hint': 'Сначала столбец поиска (customer_id), затем остальные нужные: status и total.',
  'check': 'EXPLAIN QUERY PLAN SELECT status, total FROM orders WHERE customer_id = 7',
  'contains': ['USING COVERING INDEX']},
 {'id': 'd3-partial-index',
  'mode': 'sql',
  'title': 'Частичный индекс',
  'statement': "Почти все запросы ищут только новые заказы: WHERE status = 'new' AND created >= "
               "'2024-06-01'. Создайте частичный индекс по created только для строк со status = 'new'.",
  'starter': "-- частичный индекс по created для status = 'new'\nCREATE INDEX\n",
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, city TEXT NOT NULL, '
           'created TEXT NOT NULL, status TEXT NOT NULL, total INTEGER NOT NULL);\n'
           "INSERT INTO orders VALUES (1,1,'Казань','2024-02-02','new',101);\n"
           "INSERT INTO orders VALUES (2,2,'Тверь','2024-03-03','cancelled',102);\n"
           "INSERT INTO orders VALUES (3,3,'Омск','2024-04-04','paid',103);\n"
           "INSERT INTO orders VALUES (4,4,'Москва','2024-05-05','new',104);\n"
           "INSERT INTO orders VALUES (5,5,'Казань','2024-06-06','cancelled',105);\n"
           "INSERT INTO orders VALUES (6,6,'Тверь','2024-07-07','paid',106);\n"
           "INSERT INTO orders VALUES (7,7,'Омск','2024-08-08','new',107);\n"
           "INSERT INTO orders VALUES (8,8,'Москва','2024-09-09','cancelled',108);\n"
           "INSERT INTO orders VALUES (9,9,'Казань','2024-10-10','paid',109);\n"
           "INSERT INTO orders VALUES (10,10,'Тверь','2024-11-11','new',110);\n"
           "INSERT INTO orders VALUES (11,11,'Омск','2024-12-12','cancelled',111);\n"
           "INSERT INTO orders VALUES (12,12,'Москва','2024-01-13','paid',112);\n"
           "INSERT INTO orders VALUES (13,13,'Казань','2024-02-14','new',113);\n"
           "INSERT INTO orders VALUES (14,14,'Тверь','2024-03-15','cancelled',114);\n"
           "INSERT INTO orders VALUES (15,15,'Омск','2024-04-16','paid',115);\n"
           "INSERT INTO orders VALUES (16,16,'Москва','2024-05-17','new',116);\n"
           "INSERT INTO orders VALUES (17,17,'Казань','2024-06-18','cancelled',117);\n"
           "INSERT INTO orders VALUES (18,18,'Тверь','2024-07-19','paid',118);\n"
           "INSERT INTO orders VALUES (19,19,'Омск','2024-08-20','new',119);\n"
           "INSERT INTO orders VALUES (20,20,'Москва','2024-09-21','cancelled',120);\n"
           "INSERT INTO orders VALUES (21,21,'Казань','2024-10-22','paid',121);\n"
           "INSERT INTO orders VALUES (22,22,'Тверь','2024-11-23','new',122);\n"
           "INSERT INTO orders VALUES (23,23,'Омск','2024-12-24','cancelled',123);\n"
           "INSERT INTO orders VALUES (24,24,'Москва','2024-01-25','paid',124);\n"
           "INSERT INTO orders VALUES (25,25,'Казань','2024-02-26','new',125);\n"
           "INSERT INTO orders VALUES (26,26,'Тверь','2024-03-27','cancelled',126);\n"
           "INSERT INTO orders VALUES (27,27,'Омск','2024-04-28','paid',127);\n"
           "INSERT INTO orders VALUES (28,28,'Москва','2024-05-01','new',128);\n"
           "INSERT INTO orders VALUES (29,29,'Казань','2024-06-02','cancelled',129);\n"
           "INSERT INTO orders VALUES (30,30,'Тверь','2024-07-03','paid',130);\n"
           "INSERT INTO orders VALUES (31,31,'Омск','2024-08-04','new',131);\n"
           "INSERT INTO orders VALUES (32,32,'Москва','2024-09-05','cancelled',132);\n"
           "INSERT INTO orders VALUES (33,33,'Казань','2024-10-06','paid',133);\n"
           "INSERT INTO orders VALUES (34,34,'Тверь','2024-11-07','new',134);\n"
           "INSERT INTO orders VALUES (35,35,'Омск','2024-12-08','cancelled',135);\n"
           "INSERT INTO orders VALUES (36,36,'Москва','2024-01-09','paid',136);\n"
           "INSERT INTO orders VALUES (37,37,'Казань','2024-02-10','new',137);\n"
           "INSERT INTO orders VALUES (38,38,'Тверь','2024-03-11','cancelled',138);\n"
           "INSERT INTO orders VALUES (39,39,'Омск','2024-04-12','paid',139);\n"
           "INSERT INTO orders VALUES (40,40,'Москва','2024-05-13','new',140);\n"
           "INSERT INTO orders VALUES (41,41,'Казань','2024-06-14','cancelled',141);\n"
           "INSERT INTO orders VALUES (42,42,'Тверь','2024-07-15','paid',142);\n"
           "INSERT INTO orders VALUES (43,43,'Омск','2024-08-16','new',143);\n"
           "INSERT INTO orders VALUES (44,44,'Москва','2024-09-17','cancelled',144);\n"
           "INSERT INTO orders VALUES (45,45,'Казань','2024-10-18','paid',145);\n"
           "INSERT INTO orders VALUES (46,46,'Тверь','2024-11-19','new',146);\n"
           "INSERT INTO orders VALUES (47,47,'Омск','2024-12-20','cancelled',147);\n"
           "INSERT INTO orders VALUES (48,48,'Москва','2024-01-21','paid',148);\n"
           "INSERT INTO orders VALUES (49,49,'Казань','2024-02-22','new',149);\n"
           "INSERT INTO orders VALUES (50,0,'Тверь','2024-03-23','cancelled',150);\n"
           "INSERT INTO orders VALUES (51,1,'Омск','2024-04-24','paid',151);\n"
           "INSERT INTO orders VALUES (52,2,'Москва','2024-05-25','new',152);\n"
           "INSERT INTO orders VALUES (53,3,'Казань','2024-06-26','cancelled',153);\n"
           "INSERT INTO orders VALUES (54,4,'Тверь','2024-07-27','paid',154);\n"
           "INSERT INTO orders VALUES (55,5,'Омск','2024-08-28','new',155);\n"
           "INSERT INTO orders VALUES (56,6,'Москва','2024-09-01','cancelled',156);\n"
           "INSERT INTO orders VALUES (57,7,'Казань','2024-10-02','paid',157);\n"
           "INSERT INTO orders VALUES (58,8,'Тверь','2024-11-03','new',158);\n"
           "INSERT INTO orders VALUES (59,9,'Омск','2024-12-04','cancelled',159);\n"
           "INSERT INTO orders VALUES (60,10,'Москва','2024-01-05','paid',160);\n"
           "INSERT INTO orders VALUES (61,11,'Казань','2024-02-06','new',161);\n"
           "INSERT INTO orders VALUES (62,12,'Тверь','2024-03-07','cancelled',162);\n"
           "INSERT INTO orders VALUES (63,13,'Омск','2024-04-08','paid',163);\n"
           "INSERT INTO orders VALUES (64,14,'Москва','2024-05-09','new',164);\n"
           "INSERT INTO orders VALUES (65,15,'Казань','2024-06-10','cancelled',165);\n"
           "INSERT INTO orders VALUES (66,16,'Тверь','2024-07-11','paid',166);\n"
           "INSERT INTO orders VALUES (67,17,'Омск','2024-08-12','new',167);\n"
           "INSERT INTO orders VALUES (68,18,'Москва','2024-09-13','cancelled',168);\n"
           "INSERT INTO orders VALUES (69,19,'Казань','2024-10-14','paid',169);\n"
           "INSERT INTO orders VALUES (70,20,'Тверь','2024-11-15','new',170);\n"
           "INSERT INTO orders VALUES (71,21,'Омск','2024-12-16','cancelled',171);\n"
           "INSERT INTO orders VALUES (72,22,'Москва','2024-01-17','paid',172);\n"
           "INSERT INTO orders VALUES (73,23,'Казань','2024-02-18','new',173);\n"
           "INSERT INTO orders VALUES (74,24,'Тверь','2024-03-19','cancelled',174);\n"
           "INSERT INTO orders VALUES (75,25,'Омск','2024-04-20','paid',175);\n"
           "INSERT INTO orders VALUES (76,26,'Москва','2024-05-21','new',176);\n"
           "INSERT INTO orders VALUES (77,27,'Казань','2024-06-22','cancelled',177);\n"
           "INSERT INTO orders VALUES (78,28,'Тверь','2024-07-23','paid',178);\n"
           "INSERT INTO orders VALUES (79,29,'Омск','2024-08-24','new',179);\n"
           "INSERT INTO orders VALUES (80,30,'Москва','2024-09-25','cancelled',180);\n"
           "INSERT INTO orders VALUES (81,31,'Казань','2024-10-26','paid',181);\n"
           "INSERT INTO orders VALUES (82,32,'Тверь','2024-11-27','new',182);\n"
           "INSERT INTO orders VALUES (83,33,'Омск','2024-12-28','cancelled',183);\n"
           "INSERT INTO orders VALUES (84,34,'Москва','2024-01-01','paid',184);\n"
           "INSERT INTO orders VALUES (85,35,'Казань','2024-02-02','new',185);\n"
           "INSERT INTO orders VALUES (86,36,'Тверь','2024-03-03','cancelled',186);\n"
           "INSERT INTO orders VALUES (87,37,'Омск','2024-04-04','paid',187);\n"
           "INSERT INTO orders VALUES (88,38,'Москва','2024-05-05','new',188);\n"
           "INSERT INTO orders VALUES (89,39,'Казань','2024-06-06','cancelled',189);\n"
           "INSERT INTO orders VALUES (90,40,'Тверь','2024-07-07','paid',190);\n"
           "INSERT INTO orders VALUES (91,41,'Омск','2024-08-08','new',191);\n"
           "INSERT INTO orders VALUES (92,42,'Москва','2024-09-09','cancelled',192);\n"
           "INSERT INTO orders VALUES (93,43,'Казань','2024-10-10','paid',193);\n"
           "INSERT INTO orders VALUES (94,44,'Тверь','2024-11-11','new',194);\n"
           "INSERT INTO orders VALUES (95,45,'Омск','2024-12-12','cancelled',195);\n"
           "INSERT INTO orders VALUES (96,46,'Москва','2024-01-13','paid',196);\n"
           "INSERT INTO orders VALUES (97,47,'Казань','2024-02-14','new',197);\n"
           "INSERT INTO orders VALUES (98,48,'Тверь','2024-03-15','cancelled',198);\n"
           "INSERT INTO orders VALUES (99,49,'Омск','2024-04-16','paid',199);\n"
           "INSERT INTO orders VALUES (100,0,'Москва','2024-05-17','new',200);\n"
           "INSERT INTO orders VALUES (101,1,'Казань','2024-06-18','cancelled',201);\n"
           "INSERT INTO orders VALUES (102,2,'Тверь','2024-07-19','paid',202);\n"
           "INSERT INTO orders VALUES (103,3,'Омск','2024-08-20','new',203);\n"
           "INSERT INTO orders VALUES (104,4,'Москва','2024-09-21','cancelled',204);\n"
           "INSERT INTO orders VALUES (105,5,'Казань','2024-10-22','paid',205);\n"
           "INSERT INTO orders VALUES (106,6,'Тверь','2024-11-23','new',206);\n"
           "INSERT INTO orders VALUES (107,7,'Омск','2024-12-24','cancelled',207);\n"
           "INSERT INTO orders VALUES (108,8,'Москва','2024-01-25','paid',208);\n"
           "INSERT INTO orders VALUES (109,9,'Казань','2024-02-26','new',209);\n"
           "INSERT INTO orders VALUES (110,10,'Тверь','2024-03-27','cancelled',210);\n"
           "INSERT INTO orders VALUES (111,11,'Омск','2024-04-28','paid',211);\n"
           "INSERT INTO orders VALUES (112,12,'Москва','2024-05-01','new',212);\n"
           "INSERT INTO orders VALUES (113,13,'Казань','2024-06-02','cancelled',213);\n"
           "INSERT INTO orders VALUES (114,14,'Тверь','2024-07-03','paid',214);\n"
           "INSERT INTO orders VALUES (115,15,'Омск','2024-08-04','new',215);\n"
           "INSERT INTO orders VALUES (116,16,'Москва','2024-09-05','cancelled',216);\n"
           "INSERT INTO orders VALUES (117,17,'Казань','2024-10-06','paid',217);\n"
           "INSERT INTO orders VALUES (118,18,'Тверь','2024-11-07','new',218);\n"
           "INSERT INTO orders VALUES (119,19,'Омск','2024-12-08','cancelled',219);\n"
           "INSERT INTO orders VALUES (120,20,'Москва','2024-01-09','paid',220);\n"
           "INSERT INTO orders VALUES (121,21,'Казань','2024-02-10','new',221);\n"
           "INSERT INTO orders VALUES (122,22,'Тверь','2024-03-11','cancelled',222);\n"
           "INSERT INTO orders VALUES (123,23,'Омск','2024-04-12','paid',223);\n"
           "INSERT INTO orders VALUES (124,24,'Москва','2024-05-13','new',224);\n"
           "INSERT INTO orders VALUES (125,25,'Казань','2024-06-14','cancelled',225);\n"
           "INSERT INTO orders VALUES (126,26,'Тверь','2024-07-15','paid',226);\n"
           "INSERT INTO orders VALUES (127,27,'Омск','2024-08-16','new',227);\n"
           "INSERT INTO orders VALUES (128,28,'Москва','2024-09-17','cancelled',228);\n"
           "INSERT INTO orders VALUES (129,29,'Казань','2024-10-18','paid',229);\n"
           "INSERT INTO orders VALUES (130,30,'Тверь','2024-11-19','new',230);\n"
           "INSERT INTO orders VALUES (131,31,'Омск','2024-12-20','cancelled',231);\n"
           "INSERT INTO orders VALUES (132,32,'Москва','2024-01-21','paid',232);\n"
           "INSERT INTO orders VALUES (133,33,'Казань','2024-02-22','new',233);\n"
           "INSERT INTO orders VALUES (134,34,'Тверь','2024-03-23','cancelled',234);\n"
           "INSERT INTO orders VALUES (135,35,'Омск','2024-04-24','paid',235);\n"
           "INSERT INTO orders VALUES (136,36,'Москва','2024-05-25','new',236);\n"
           "INSERT INTO orders VALUES (137,37,'Казань','2024-06-26','cancelled',237);\n"
           "INSERT INTO orders VALUES (138,38,'Тверь','2024-07-27','paid',238);\n"
           "INSERT INTO orders VALUES (139,39,'Омск','2024-08-28','new',239);\n"
           "INSERT INTO orders VALUES (140,40,'Москва','2024-09-01','cancelled',240);\n"
           "INSERT INTO orders VALUES (141,41,'Казань','2024-10-02','paid',241);\n"
           "INSERT INTO orders VALUES (142,42,'Тверь','2024-11-03','new',242);\n"
           "INSERT INTO orders VALUES (143,43,'Омск','2024-12-04','cancelled',243);\n"
           "INSERT INTO orders VALUES (144,44,'Москва','2024-01-05','paid',244);\n"
           "INSERT INTO orders VALUES (145,45,'Казань','2024-02-06','new',245);\n"
           "INSERT INTO orders VALUES (146,46,'Тверь','2024-03-07','cancelled',246);\n"
           "INSERT INTO orders VALUES (147,47,'Омск','2024-04-08','paid',247);\n"
           "INSERT INTO orders VALUES (148,48,'Москва','2024-05-09','new',248);\n"
           "INSERT INTO orders VALUES (149,49,'Казань','2024-06-10','cancelled',249);\n"
           "INSERT INTO orders VALUES (150,0,'Тверь','2024-07-11','paid',250);\n"
           "INSERT INTO orders VALUES (151,1,'Омск','2024-08-12','new',251);\n"
           "INSERT INTO orders VALUES (152,2,'Москва','2024-09-13','cancelled',252);\n"
           "INSERT INTO orders VALUES (153,3,'Казань','2024-10-14','paid',253);\n"
           "INSERT INTO orders VALUES (154,4,'Тверь','2024-11-15','new',254);\n"
           "INSERT INTO orders VALUES (155,5,'Омск','2024-12-16','cancelled',255);\n"
           "INSERT INTO orders VALUES (156,6,'Москва','2024-01-17','paid',256);\n"
           "INSERT INTO orders VALUES (157,7,'Казань','2024-02-18','new',257);\n"
           "INSERT INTO orders VALUES (158,8,'Тверь','2024-03-19','cancelled',258);\n"
           "INSERT INTO orders VALUES (159,9,'Омск','2024-04-20','paid',259);\n"
           "INSERT INTO orders VALUES (160,10,'Москва','2024-05-21','new',260);\n"
           "INSERT INTO orders VALUES (161,11,'Казань','2024-06-22','cancelled',261);\n"
           "INSERT INTO orders VALUES (162,12,'Тверь','2024-07-23','paid',262);\n"
           "INSERT INTO orders VALUES (163,13,'Омск','2024-08-24','new',263);\n"
           "INSERT INTO orders VALUES (164,14,'Москва','2024-09-25','cancelled',264);\n"
           "INSERT INTO orders VALUES (165,15,'Казань','2024-10-26','paid',265);\n"
           "INSERT INTO orders VALUES (166,16,'Тверь','2024-11-27','new',266);\n"
           "INSERT INTO orders VALUES (167,17,'Омск','2024-12-28','cancelled',267);\n"
           "INSERT INTO orders VALUES (168,18,'Москва','2024-01-01','paid',268);\n"
           "INSERT INTO orders VALUES (169,19,'Казань','2024-02-02','new',269);\n"
           "INSERT INTO orders VALUES (170,20,'Тверь','2024-03-03','cancelled',270);\n"
           "INSERT INTO orders VALUES (171,21,'Омск','2024-04-04','paid',271);\n"
           "INSERT INTO orders VALUES (172,22,'Москва','2024-05-05','new',272);\n"
           "INSERT INTO orders VALUES (173,23,'Казань','2024-06-06','cancelled',273);\n"
           "INSERT INTO orders VALUES (174,24,'Тверь','2024-07-07','paid',274);\n"
           "INSERT INTO orders VALUES (175,25,'Омск','2024-08-08','new',275);\n"
           "INSERT INTO orders VALUES (176,26,'Москва','2024-09-09','cancelled',276);\n"
           "INSERT INTO orders VALUES (177,27,'Казань','2024-10-10','paid',277);\n"
           "INSERT INTO orders VALUES (178,28,'Тверь','2024-11-11','new',278);\n"
           "INSERT INTO orders VALUES (179,29,'Омск','2024-12-12','cancelled',279);\n"
           "INSERT INTO orders VALUES (180,30,'Москва','2024-01-13','paid',280);\n"
           "INSERT INTO orders VALUES (181,31,'Казань','2024-02-14','new',281);\n"
           "INSERT INTO orders VALUES (182,32,'Тверь','2024-03-15','cancelled',282);\n"
           "INSERT INTO orders VALUES (183,33,'Омск','2024-04-16','paid',283);\n"
           "INSERT INTO orders VALUES (184,34,'Москва','2024-05-17','new',284);\n"
           "INSERT INTO orders VALUES (185,35,'Казань','2024-06-18','cancelled',285);\n"
           "INSERT INTO orders VALUES (186,36,'Тверь','2024-07-19','paid',286);\n"
           "INSERT INTO orders VALUES (187,37,'Омск','2024-08-20','new',287);\n"
           "INSERT INTO orders VALUES (188,38,'Москва','2024-09-21','cancelled',288);\n"
           "INSERT INTO orders VALUES (189,39,'Казань','2024-10-22','paid',289);\n"
           "INSERT INTO orders VALUES (190,40,'Тверь','2024-11-23','new',290);\n"
           "INSERT INTO orders VALUES (191,41,'Омск','2024-12-24','cancelled',291);\n"
           "INSERT INTO orders VALUES (192,42,'Москва','2024-01-25','paid',292);\n"
           "INSERT INTO orders VALUES (193,43,'Казань','2024-02-26','new',293);\n"
           "INSERT INTO orders VALUES (194,44,'Тверь','2024-03-27','cancelled',294);\n"
           "INSERT INTO orders VALUES (195,45,'Омск','2024-04-28','paid',295);\n"
           "INSERT INTO orders VALUES (196,46,'Москва','2024-05-01','new',296);\n"
           "INSERT INTO orders VALUES (197,47,'Казань','2024-06-02','cancelled',297);\n"
           "INSERT INTO orders VALUES (198,48,'Тверь','2024-07-03','paid',298);\n"
           "INSERT INTO orders VALUES (199,49,'Омск','2024-08-04','new',299);\n"
           "INSERT INTO orders VALUES (200,0,'Москва','2024-09-05','cancelled',300);\n"
           "INSERT INTO orders VALUES (201,1,'Казань','2024-10-06','paid',301);\n"
           "INSERT INTO orders VALUES (202,2,'Тверь','2024-11-07','new',302);\n"
           "INSERT INTO orders VALUES (203,3,'Омск','2024-12-08','cancelled',303);\n"
           "INSERT INTO orders VALUES (204,4,'Москва','2024-01-09','paid',304);\n"
           "INSERT INTO orders VALUES (205,5,'Казань','2024-02-10','new',305);\n"
           "INSERT INTO orders VALUES (206,6,'Тверь','2024-03-11','cancelled',306);\n"
           "INSERT INTO orders VALUES (207,7,'Омск','2024-04-12','paid',307);\n"
           "INSERT INTO orders VALUES (208,8,'Москва','2024-05-13','new',308);\n"
           "INSERT INTO orders VALUES (209,9,'Казань','2024-06-14','cancelled',309);\n"
           "INSERT INTO orders VALUES (210,10,'Тверь','2024-07-15','paid',310);\n"
           "INSERT INTO orders VALUES (211,11,'Омск','2024-08-16','new',311);\n"
           "INSERT INTO orders VALUES (212,12,'Москва','2024-09-17','cancelled',312);\n"
           "INSERT INTO orders VALUES (213,13,'Казань','2024-10-18','paid',313);\n"
           "INSERT INTO orders VALUES (214,14,'Тверь','2024-11-19','new',314);\n"
           "INSERT INTO orders VALUES (215,15,'Омск','2024-12-20','cancelled',315);\n"
           "INSERT INTO orders VALUES (216,16,'Москва','2024-01-21','paid',316);\n"
           "INSERT INTO orders VALUES (217,17,'Казань','2024-02-22','new',317);\n"
           "INSERT INTO orders VALUES (218,18,'Тверь','2024-03-23','cancelled',318);\n"
           "INSERT INTO orders VALUES (219,19,'Омск','2024-04-24','paid',319);\n"
           "INSERT INTO orders VALUES (220,20,'Москва','2024-05-25','new',320);\n"
           "INSERT INTO orders VALUES (221,21,'Казань','2024-06-26','cancelled',321);\n"
           "INSERT INTO orders VALUES (222,22,'Тверь','2024-07-27','paid',322);\n"
           "INSERT INTO orders VALUES (223,23,'Омск','2024-08-28','new',323);\n"
           "INSERT INTO orders VALUES (224,24,'Москва','2024-09-01','cancelled',324);\n"
           "INSERT INTO orders VALUES (225,25,'Казань','2024-10-02','paid',325);\n"
           "INSERT INTO orders VALUES (226,26,'Тверь','2024-11-03','new',326);\n"
           "INSERT INTO orders VALUES (227,27,'Омск','2024-12-04','cancelled',327);\n"
           "INSERT INTO orders VALUES (228,28,'Москва','2024-01-05','paid',328);\n"
           "INSERT INTO orders VALUES (229,29,'Казань','2024-02-06','new',329);\n"
           "INSERT INTO orders VALUES (230,30,'Тверь','2024-03-07','cancelled',330);\n"
           "INSERT INTO orders VALUES (231,31,'Омск','2024-04-08','paid',331);\n"
           "INSERT INTO orders VALUES (232,32,'Москва','2024-05-09','new',332);\n"
           "INSERT INTO orders VALUES (233,33,'Казань','2024-06-10','cancelled',333);\n"
           "INSERT INTO orders VALUES (234,34,'Тверь','2024-07-11','paid',334);\n"
           "INSERT INTO orders VALUES (235,35,'Омск','2024-08-12','new',335);\n"
           "INSERT INTO orders VALUES (236,36,'Москва','2024-09-13','cancelled',336);\n"
           "INSERT INTO orders VALUES (237,37,'Казань','2024-10-14','paid',337);\n"
           "INSERT INTO orders VALUES (238,38,'Тверь','2024-11-15','new',338);\n"
           "INSERT INTO orders VALUES (239,39,'Омск','2024-12-16','cancelled',339);\n"
           "INSERT INTO orders VALUES (240,40,'Москва','2024-01-17','paid',340);\n"
           "INSERT INTO orders VALUES (241,41,'Казань','2024-02-18','new',341);\n"
           "INSERT INTO orders VALUES (242,42,'Тверь','2024-03-19','cancelled',342);\n"
           "INSERT INTO orders VALUES (243,43,'Омск','2024-04-20','paid',343);\n"
           "INSERT INTO orders VALUES (244,44,'Москва','2024-05-21','new',344);\n"
           "INSERT INTO orders VALUES (245,45,'Казань','2024-06-22','cancelled',345);\n"
           "INSERT INTO orders VALUES (246,46,'Тверь','2024-07-23','paid',346);\n"
           "INSERT INTO orders VALUES (247,47,'Омск','2024-08-24','new',347);\n"
           "INSERT INTO orders VALUES (248,48,'Москва','2024-09-25','cancelled',348);\n"
           "INSERT INTO orders VALUES (249,49,'Казань','2024-10-26','paid',349);\n"
           "INSERT INTO orders VALUES (250,0,'Тверь','2024-11-27','new',350);\n"
           "INSERT INTO orders VALUES (251,1,'Омск','2024-12-28','cancelled',351);\n"
           "INSERT INTO orders VALUES (252,2,'Москва','2024-01-01','paid',352);\n"
           "INSERT INTO orders VALUES (253,3,'Казань','2024-02-02','new',353);\n"
           "INSERT INTO orders VALUES (254,4,'Тверь','2024-03-03','cancelled',354);\n"
           "INSERT INTO orders VALUES (255,5,'Омск','2024-04-04','paid',355);\n"
           "INSERT INTO orders VALUES (256,6,'Москва','2024-05-05','new',356);\n"
           "INSERT INTO orders VALUES (257,7,'Казань','2024-06-06','cancelled',357);\n"
           "INSERT INTO orders VALUES (258,8,'Тверь','2024-07-07','paid',358);\n"
           "INSERT INTO orders VALUES (259,9,'Омск','2024-08-08','new',359);\n"
           "INSERT INTO orders VALUES (260,10,'Москва','2024-09-09','cancelled',360);\n"
           "INSERT INTO orders VALUES (261,11,'Казань','2024-10-10','paid',361);\n"
           "INSERT INTO orders VALUES (262,12,'Тверь','2024-11-11','new',362);\n"
           "INSERT INTO orders VALUES (263,13,'Омск','2024-12-12','cancelled',363);\n"
           "INSERT INTO orders VALUES (264,14,'Москва','2024-01-13','paid',364);\n"
           "INSERT INTO orders VALUES (265,15,'Казань','2024-02-14','new',365);\n"
           "INSERT INTO orders VALUES (266,16,'Тверь','2024-03-15','cancelled',366);\n"
           "INSERT INTO orders VALUES (267,17,'Омск','2024-04-16','paid',367);\n"
           "INSERT INTO orders VALUES (268,18,'Москва','2024-05-17','new',368);\n"
           "INSERT INTO orders VALUES (269,19,'Казань','2024-06-18','cancelled',369);\n"
           "INSERT INTO orders VALUES (270,20,'Тверь','2024-07-19','paid',370);\n"
           "INSERT INTO orders VALUES (271,21,'Омск','2024-08-20','new',371);\n"
           "INSERT INTO orders VALUES (272,22,'Москва','2024-09-21','cancelled',372);\n"
           "INSERT INTO orders VALUES (273,23,'Казань','2024-10-22','paid',373);\n"
           "INSERT INTO orders VALUES (274,24,'Тверь','2024-11-23','new',374);\n"
           "INSERT INTO orders VALUES (275,25,'Омск','2024-12-24','cancelled',375);\n"
           "INSERT INTO orders VALUES (276,26,'Москва','2024-01-25','paid',376);\n"
           "INSERT INTO orders VALUES (277,27,'Казань','2024-02-26','new',377);\n"
           "INSERT INTO orders VALUES (278,28,'Тверь','2024-03-27','cancelled',378);\n"
           "INSERT INTO orders VALUES (279,29,'Омск','2024-04-28','paid',379);\n"
           "INSERT INTO orders VALUES (280,30,'Москва','2024-05-01','new',380);\n"
           "INSERT INTO orders VALUES (281,31,'Казань','2024-06-02','cancelled',381);\n"
           "INSERT INTO orders VALUES (282,32,'Тверь','2024-07-03','paid',382);\n"
           "INSERT INTO orders VALUES (283,33,'Омск','2024-08-04','new',383);\n"
           "INSERT INTO orders VALUES (284,34,'Москва','2024-09-05','cancelled',384);\n"
           "INSERT INTO orders VALUES (285,35,'Казань','2024-10-06','paid',385);\n"
           "INSERT INTO orders VALUES (286,36,'Тверь','2024-11-07','new',386);\n"
           "INSERT INTO orders VALUES (287,37,'Омск','2024-12-08','cancelled',387);\n"
           "INSERT INTO orders VALUES (288,38,'Москва','2024-01-09','paid',388);\n"
           "INSERT INTO orders VALUES (289,39,'Казань','2024-02-10','new',389);\n"
           "INSERT INTO orders VALUES (290,40,'Тверь','2024-03-11','cancelled',390);\n"
           "INSERT INTO orders VALUES (291,41,'Омск','2024-04-12','paid',391);\n"
           "INSERT INTO orders VALUES (292,42,'Москва','2024-05-13','new',392);\n"
           "INSERT INTO orders VALUES (293,43,'Казань','2024-06-14','cancelled',393);\n"
           "INSERT INTO orders VALUES (294,44,'Тверь','2024-07-15','paid',394);\n"
           "INSERT INTO orders VALUES (295,45,'Омск','2024-08-16','new',395);\n"
           "INSERT INTO orders VALUES (296,46,'Москва','2024-09-17','cancelled',396);\n"
           "INSERT INTO orders VALUES (297,47,'Казань','2024-10-18','paid',397);\n"
           "INSERT INTO orders VALUES (298,48,'Тверь','2024-11-19','new',398);\n"
           "INSERT INTO orders VALUES (299,49,'Омск','2024-12-20','cancelled',399);\n"
           "INSERT INTO orders VALUES (300,0,'Москва','2024-01-21','paid',400);\n",
  'expected': [[2, 0, 182, 'SEARCH orders USING COVERING INDEX idx_new_created (created>?)']],
  'hint': "CREATE INDEX … ON orders (created) WHERE status = 'new';",
  'check': "EXPLAIN QUERY PLAN SELECT id FROM orders WHERE status = 'new' AND created >= '2024-06-01'",
  'contains': ['idx_new_created']},
 {'id': 'd3-order-by-index',
  'mode': 'sql',
  'title': 'Сортировка по индексу',
  'statement': 'Запрос SELECT * FROM orders ORDER BY created LIMIT 10 строит временную сортировку. Создайте '
               'индекс, после которого она исчезнет из плана.',
  'starter': '-- индекс для ORDER BY created\nCREATE INDEX\n',
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, city TEXT NOT NULL, '
           'created TEXT NOT NULL, status TEXT NOT NULL, total INTEGER NOT NULL);\n'
           "INSERT INTO orders VALUES (1,1,'Казань','2024-02-02','new',101);\n"
           "INSERT INTO orders VALUES (2,2,'Тверь','2024-03-03','cancelled',102);\n"
           "INSERT INTO orders VALUES (3,3,'Омск','2024-04-04','paid',103);\n"
           "INSERT INTO orders VALUES (4,4,'Москва','2024-05-05','new',104);\n"
           "INSERT INTO orders VALUES (5,5,'Казань','2024-06-06','cancelled',105);\n"
           "INSERT INTO orders VALUES (6,6,'Тверь','2024-07-07','paid',106);\n"
           "INSERT INTO orders VALUES (7,7,'Омск','2024-08-08','new',107);\n"
           "INSERT INTO orders VALUES (8,8,'Москва','2024-09-09','cancelled',108);\n"
           "INSERT INTO orders VALUES (9,9,'Казань','2024-10-10','paid',109);\n"
           "INSERT INTO orders VALUES (10,10,'Тверь','2024-11-11','new',110);\n"
           "INSERT INTO orders VALUES (11,11,'Омск','2024-12-12','cancelled',111);\n"
           "INSERT INTO orders VALUES (12,12,'Москва','2024-01-13','paid',112);\n"
           "INSERT INTO orders VALUES (13,13,'Казань','2024-02-14','new',113);\n"
           "INSERT INTO orders VALUES (14,14,'Тверь','2024-03-15','cancelled',114);\n"
           "INSERT INTO orders VALUES (15,15,'Омск','2024-04-16','paid',115);\n"
           "INSERT INTO orders VALUES (16,16,'Москва','2024-05-17','new',116);\n"
           "INSERT INTO orders VALUES (17,17,'Казань','2024-06-18','cancelled',117);\n"
           "INSERT INTO orders VALUES (18,18,'Тверь','2024-07-19','paid',118);\n"
           "INSERT INTO orders VALUES (19,19,'Омск','2024-08-20','new',119);\n"
           "INSERT INTO orders VALUES (20,20,'Москва','2024-09-21','cancelled',120);\n"
           "INSERT INTO orders VALUES (21,21,'Казань','2024-10-22','paid',121);\n"
           "INSERT INTO orders VALUES (22,22,'Тверь','2024-11-23','new',122);\n"
           "INSERT INTO orders VALUES (23,23,'Омск','2024-12-24','cancelled',123);\n"
           "INSERT INTO orders VALUES (24,24,'Москва','2024-01-25','paid',124);\n"
           "INSERT INTO orders VALUES (25,25,'Казань','2024-02-26','new',125);\n"
           "INSERT INTO orders VALUES (26,26,'Тверь','2024-03-27','cancelled',126);\n"
           "INSERT INTO orders VALUES (27,27,'Омск','2024-04-28','paid',127);\n"
           "INSERT INTO orders VALUES (28,28,'Москва','2024-05-01','new',128);\n"
           "INSERT INTO orders VALUES (29,29,'Казань','2024-06-02','cancelled',129);\n"
           "INSERT INTO orders VALUES (30,30,'Тверь','2024-07-03','paid',130);\n"
           "INSERT INTO orders VALUES (31,31,'Омск','2024-08-04','new',131);\n"
           "INSERT INTO orders VALUES (32,32,'Москва','2024-09-05','cancelled',132);\n"
           "INSERT INTO orders VALUES (33,33,'Казань','2024-10-06','paid',133);\n"
           "INSERT INTO orders VALUES (34,34,'Тверь','2024-11-07','new',134);\n"
           "INSERT INTO orders VALUES (35,35,'Омск','2024-12-08','cancelled',135);\n"
           "INSERT INTO orders VALUES (36,36,'Москва','2024-01-09','paid',136);\n"
           "INSERT INTO orders VALUES (37,37,'Казань','2024-02-10','new',137);\n"
           "INSERT INTO orders VALUES (38,38,'Тверь','2024-03-11','cancelled',138);\n"
           "INSERT INTO orders VALUES (39,39,'Омск','2024-04-12','paid',139);\n"
           "INSERT INTO orders VALUES (40,40,'Москва','2024-05-13','new',140);\n"
           "INSERT INTO orders VALUES (41,41,'Казань','2024-06-14','cancelled',141);\n"
           "INSERT INTO orders VALUES (42,42,'Тверь','2024-07-15','paid',142);\n"
           "INSERT INTO orders VALUES (43,43,'Омск','2024-08-16','new',143);\n"
           "INSERT INTO orders VALUES (44,44,'Москва','2024-09-17','cancelled',144);\n"
           "INSERT INTO orders VALUES (45,45,'Казань','2024-10-18','paid',145);\n"
           "INSERT INTO orders VALUES (46,46,'Тверь','2024-11-19','new',146);\n"
           "INSERT INTO orders VALUES (47,47,'Омск','2024-12-20','cancelled',147);\n"
           "INSERT INTO orders VALUES (48,48,'Москва','2024-01-21','paid',148);\n"
           "INSERT INTO orders VALUES (49,49,'Казань','2024-02-22','new',149);\n"
           "INSERT INTO orders VALUES (50,0,'Тверь','2024-03-23','cancelled',150);\n"
           "INSERT INTO orders VALUES (51,1,'Омск','2024-04-24','paid',151);\n"
           "INSERT INTO orders VALUES (52,2,'Москва','2024-05-25','new',152);\n"
           "INSERT INTO orders VALUES (53,3,'Казань','2024-06-26','cancelled',153);\n"
           "INSERT INTO orders VALUES (54,4,'Тверь','2024-07-27','paid',154);\n"
           "INSERT INTO orders VALUES (55,5,'Омск','2024-08-28','new',155);\n"
           "INSERT INTO orders VALUES (56,6,'Москва','2024-09-01','cancelled',156);\n"
           "INSERT INTO orders VALUES (57,7,'Казань','2024-10-02','paid',157);\n"
           "INSERT INTO orders VALUES (58,8,'Тверь','2024-11-03','new',158);\n"
           "INSERT INTO orders VALUES (59,9,'Омск','2024-12-04','cancelled',159);\n"
           "INSERT INTO orders VALUES (60,10,'Москва','2024-01-05','paid',160);\n"
           "INSERT INTO orders VALUES (61,11,'Казань','2024-02-06','new',161);\n"
           "INSERT INTO orders VALUES (62,12,'Тверь','2024-03-07','cancelled',162);\n"
           "INSERT INTO orders VALUES (63,13,'Омск','2024-04-08','paid',163);\n"
           "INSERT INTO orders VALUES (64,14,'Москва','2024-05-09','new',164);\n"
           "INSERT INTO orders VALUES (65,15,'Казань','2024-06-10','cancelled',165);\n"
           "INSERT INTO orders VALUES (66,16,'Тверь','2024-07-11','paid',166);\n"
           "INSERT INTO orders VALUES (67,17,'Омск','2024-08-12','new',167);\n"
           "INSERT INTO orders VALUES (68,18,'Москва','2024-09-13','cancelled',168);\n"
           "INSERT INTO orders VALUES (69,19,'Казань','2024-10-14','paid',169);\n"
           "INSERT INTO orders VALUES (70,20,'Тверь','2024-11-15','new',170);\n"
           "INSERT INTO orders VALUES (71,21,'Омск','2024-12-16','cancelled',171);\n"
           "INSERT INTO orders VALUES (72,22,'Москва','2024-01-17','paid',172);\n"
           "INSERT INTO orders VALUES (73,23,'Казань','2024-02-18','new',173);\n"
           "INSERT INTO orders VALUES (74,24,'Тверь','2024-03-19','cancelled',174);\n"
           "INSERT INTO orders VALUES (75,25,'Омск','2024-04-20','paid',175);\n"
           "INSERT INTO orders VALUES (76,26,'Москва','2024-05-21','new',176);\n"
           "INSERT INTO orders VALUES (77,27,'Казань','2024-06-22','cancelled',177);\n"
           "INSERT INTO orders VALUES (78,28,'Тверь','2024-07-23','paid',178);\n"
           "INSERT INTO orders VALUES (79,29,'Омск','2024-08-24','new',179);\n"
           "INSERT INTO orders VALUES (80,30,'Москва','2024-09-25','cancelled',180);\n"
           "INSERT INTO orders VALUES (81,31,'Казань','2024-10-26','paid',181);\n"
           "INSERT INTO orders VALUES (82,32,'Тверь','2024-11-27','new',182);\n"
           "INSERT INTO orders VALUES (83,33,'Омск','2024-12-28','cancelled',183);\n"
           "INSERT INTO orders VALUES (84,34,'Москва','2024-01-01','paid',184);\n"
           "INSERT INTO orders VALUES (85,35,'Казань','2024-02-02','new',185);\n"
           "INSERT INTO orders VALUES (86,36,'Тверь','2024-03-03','cancelled',186);\n"
           "INSERT INTO orders VALUES (87,37,'Омск','2024-04-04','paid',187);\n"
           "INSERT INTO orders VALUES (88,38,'Москва','2024-05-05','new',188);\n"
           "INSERT INTO orders VALUES (89,39,'Казань','2024-06-06','cancelled',189);\n"
           "INSERT INTO orders VALUES (90,40,'Тверь','2024-07-07','paid',190);\n"
           "INSERT INTO orders VALUES (91,41,'Омск','2024-08-08','new',191);\n"
           "INSERT INTO orders VALUES (92,42,'Москва','2024-09-09','cancelled',192);\n"
           "INSERT INTO orders VALUES (93,43,'Казань','2024-10-10','paid',193);\n"
           "INSERT INTO orders VALUES (94,44,'Тверь','2024-11-11','new',194);\n"
           "INSERT INTO orders VALUES (95,45,'Омск','2024-12-12','cancelled',195);\n"
           "INSERT INTO orders VALUES (96,46,'Москва','2024-01-13','paid',196);\n"
           "INSERT INTO orders VALUES (97,47,'Казань','2024-02-14','new',197);\n"
           "INSERT INTO orders VALUES (98,48,'Тверь','2024-03-15','cancelled',198);\n"
           "INSERT INTO orders VALUES (99,49,'Омск','2024-04-16','paid',199);\n"
           "INSERT INTO orders VALUES (100,0,'Москва','2024-05-17','new',200);\n"
           "INSERT INTO orders VALUES (101,1,'Казань','2024-06-18','cancelled',201);\n"
           "INSERT INTO orders VALUES (102,2,'Тверь','2024-07-19','paid',202);\n"
           "INSERT INTO orders VALUES (103,3,'Омск','2024-08-20','new',203);\n"
           "INSERT INTO orders VALUES (104,4,'Москва','2024-09-21','cancelled',204);\n"
           "INSERT INTO orders VALUES (105,5,'Казань','2024-10-22','paid',205);\n"
           "INSERT INTO orders VALUES (106,6,'Тверь','2024-11-23','new',206);\n"
           "INSERT INTO orders VALUES (107,7,'Омск','2024-12-24','cancelled',207);\n"
           "INSERT INTO orders VALUES (108,8,'Москва','2024-01-25','paid',208);\n"
           "INSERT INTO orders VALUES (109,9,'Казань','2024-02-26','new',209);\n"
           "INSERT INTO orders VALUES (110,10,'Тверь','2024-03-27','cancelled',210);\n"
           "INSERT INTO orders VALUES (111,11,'Омск','2024-04-28','paid',211);\n"
           "INSERT INTO orders VALUES (112,12,'Москва','2024-05-01','new',212);\n"
           "INSERT INTO orders VALUES (113,13,'Казань','2024-06-02','cancelled',213);\n"
           "INSERT INTO orders VALUES (114,14,'Тверь','2024-07-03','paid',214);\n"
           "INSERT INTO orders VALUES (115,15,'Омск','2024-08-04','new',215);\n"
           "INSERT INTO orders VALUES (116,16,'Москва','2024-09-05','cancelled',216);\n"
           "INSERT INTO orders VALUES (117,17,'Казань','2024-10-06','paid',217);\n"
           "INSERT INTO orders VALUES (118,18,'Тверь','2024-11-07','new',218);\n"
           "INSERT INTO orders VALUES (119,19,'Омск','2024-12-08','cancelled',219);\n"
           "INSERT INTO orders VALUES (120,20,'Москва','2024-01-09','paid',220);\n"
           "INSERT INTO orders VALUES (121,21,'Казань','2024-02-10','new',221);\n"
           "INSERT INTO orders VALUES (122,22,'Тверь','2024-03-11','cancelled',222);\n"
           "INSERT INTO orders VALUES (123,23,'Омск','2024-04-12','paid',223);\n"
           "INSERT INTO orders VALUES (124,24,'Москва','2024-05-13','new',224);\n"
           "INSERT INTO orders VALUES (125,25,'Казань','2024-06-14','cancelled',225);\n"
           "INSERT INTO orders VALUES (126,26,'Тверь','2024-07-15','paid',226);\n"
           "INSERT INTO orders VALUES (127,27,'Омск','2024-08-16','new',227);\n"
           "INSERT INTO orders VALUES (128,28,'Москва','2024-09-17','cancelled',228);\n"
           "INSERT INTO orders VALUES (129,29,'Казань','2024-10-18','paid',229);\n"
           "INSERT INTO orders VALUES (130,30,'Тверь','2024-11-19','new',230);\n"
           "INSERT INTO orders VALUES (131,31,'Омск','2024-12-20','cancelled',231);\n"
           "INSERT INTO orders VALUES (132,32,'Москва','2024-01-21','paid',232);\n"
           "INSERT INTO orders VALUES (133,33,'Казань','2024-02-22','new',233);\n"
           "INSERT INTO orders VALUES (134,34,'Тверь','2024-03-23','cancelled',234);\n"
           "INSERT INTO orders VALUES (135,35,'Омск','2024-04-24','paid',235);\n"
           "INSERT INTO orders VALUES (136,36,'Москва','2024-05-25','new',236);\n"
           "INSERT INTO orders VALUES (137,37,'Казань','2024-06-26','cancelled',237);\n"
           "INSERT INTO orders VALUES (138,38,'Тверь','2024-07-27','paid',238);\n"
           "INSERT INTO orders VALUES (139,39,'Омск','2024-08-28','new',239);\n"
           "INSERT INTO orders VALUES (140,40,'Москва','2024-09-01','cancelled',240);\n"
           "INSERT INTO orders VALUES (141,41,'Казань','2024-10-02','paid',241);\n"
           "INSERT INTO orders VALUES (142,42,'Тверь','2024-11-03','new',242);\n"
           "INSERT INTO orders VALUES (143,43,'Омск','2024-12-04','cancelled',243);\n"
           "INSERT INTO orders VALUES (144,44,'Москва','2024-01-05','paid',244);\n"
           "INSERT INTO orders VALUES (145,45,'Казань','2024-02-06','new',245);\n"
           "INSERT INTO orders VALUES (146,46,'Тверь','2024-03-07','cancelled',246);\n"
           "INSERT INTO orders VALUES (147,47,'Омск','2024-04-08','paid',247);\n"
           "INSERT INTO orders VALUES (148,48,'Москва','2024-05-09','new',248);\n"
           "INSERT INTO orders VALUES (149,49,'Казань','2024-06-10','cancelled',249);\n"
           "INSERT INTO orders VALUES (150,0,'Тверь','2024-07-11','paid',250);\n"
           "INSERT INTO orders VALUES (151,1,'Омск','2024-08-12','new',251);\n"
           "INSERT INTO orders VALUES (152,2,'Москва','2024-09-13','cancelled',252);\n"
           "INSERT INTO orders VALUES (153,3,'Казань','2024-10-14','paid',253);\n"
           "INSERT INTO orders VALUES (154,4,'Тверь','2024-11-15','new',254);\n"
           "INSERT INTO orders VALUES (155,5,'Омск','2024-12-16','cancelled',255);\n"
           "INSERT INTO orders VALUES (156,6,'Москва','2024-01-17','paid',256);\n"
           "INSERT INTO orders VALUES (157,7,'Казань','2024-02-18','new',257);\n"
           "INSERT INTO orders VALUES (158,8,'Тверь','2024-03-19','cancelled',258);\n"
           "INSERT INTO orders VALUES (159,9,'Омск','2024-04-20','paid',259);\n"
           "INSERT INTO orders VALUES (160,10,'Москва','2024-05-21','new',260);\n"
           "INSERT INTO orders VALUES (161,11,'Казань','2024-06-22','cancelled',261);\n"
           "INSERT INTO orders VALUES (162,12,'Тверь','2024-07-23','paid',262);\n"
           "INSERT INTO orders VALUES (163,13,'Омск','2024-08-24','new',263);\n"
           "INSERT INTO orders VALUES (164,14,'Москва','2024-09-25','cancelled',264);\n"
           "INSERT INTO orders VALUES (165,15,'Казань','2024-10-26','paid',265);\n"
           "INSERT INTO orders VALUES (166,16,'Тверь','2024-11-27','new',266);\n"
           "INSERT INTO orders VALUES (167,17,'Омск','2024-12-28','cancelled',267);\n"
           "INSERT INTO orders VALUES (168,18,'Москва','2024-01-01','paid',268);\n"
           "INSERT INTO orders VALUES (169,19,'Казань','2024-02-02','new',269);\n"
           "INSERT INTO orders VALUES (170,20,'Тверь','2024-03-03','cancelled',270);\n"
           "INSERT INTO orders VALUES (171,21,'Омск','2024-04-04','paid',271);\n"
           "INSERT INTO orders VALUES (172,22,'Москва','2024-05-05','new',272);\n"
           "INSERT INTO orders VALUES (173,23,'Казань','2024-06-06','cancelled',273);\n"
           "INSERT INTO orders VALUES (174,24,'Тверь','2024-07-07','paid',274);\n"
           "INSERT INTO orders VALUES (175,25,'Омск','2024-08-08','new',275);\n"
           "INSERT INTO orders VALUES (176,26,'Москва','2024-09-09','cancelled',276);\n"
           "INSERT INTO orders VALUES (177,27,'Казань','2024-10-10','paid',277);\n"
           "INSERT INTO orders VALUES (178,28,'Тверь','2024-11-11','new',278);\n"
           "INSERT INTO orders VALUES (179,29,'Омск','2024-12-12','cancelled',279);\n"
           "INSERT INTO orders VALUES (180,30,'Москва','2024-01-13','paid',280);\n"
           "INSERT INTO orders VALUES (181,31,'Казань','2024-02-14','new',281);\n"
           "INSERT INTO orders VALUES (182,32,'Тверь','2024-03-15','cancelled',282);\n"
           "INSERT INTO orders VALUES (183,33,'Омск','2024-04-16','paid',283);\n"
           "INSERT INTO orders VALUES (184,34,'Москва','2024-05-17','new',284);\n"
           "INSERT INTO orders VALUES (185,35,'Казань','2024-06-18','cancelled',285);\n"
           "INSERT INTO orders VALUES (186,36,'Тверь','2024-07-19','paid',286);\n"
           "INSERT INTO orders VALUES (187,37,'Омск','2024-08-20','new',287);\n"
           "INSERT INTO orders VALUES (188,38,'Москва','2024-09-21','cancelled',288);\n"
           "INSERT INTO orders VALUES (189,39,'Казань','2024-10-22','paid',289);\n"
           "INSERT INTO orders VALUES (190,40,'Тверь','2024-11-23','new',290);\n"
           "INSERT INTO orders VALUES (191,41,'Омск','2024-12-24','cancelled',291);\n"
           "INSERT INTO orders VALUES (192,42,'Москва','2024-01-25','paid',292);\n"
           "INSERT INTO orders VALUES (193,43,'Казань','2024-02-26','new',293);\n"
           "INSERT INTO orders VALUES (194,44,'Тверь','2024-03-27','cancelled',294);\n"
           "INSERT INTO orders VALUES (195,45,'Омск','2024-04-28','paid',295);\n"
           "INSERT INTO orders VALUES (196,46,'Москва','2024-05-01','new',296);\n"
           "INSERT INTO orders VALUES (197,47,'Казань','2024-06-02','cancelled',297);\n"
           "INSERT INTO orders VALUES (198,48,'Тверь','2024-07-03','paid',298);\n"
           "INSERT INTO orders VALUES (199,49,'Омск','2024-08-04','new',299);\n"
           "INSERT INTO orders VALUES (200,0,'Москва','2024-09-05','cancelled',300);\n"
           "INSERT INTO orders VALUES (201,1,'Казань','2024-10-06','paid',301);\n"
           "INSERT INTO orders VALUES (202,2,'Тверь','2024-11-07','new',302);\n"
           "INSERT INTO orders VALUES (203,3,'Омск','2024-12-08','cancelled',303);\n"
           "INSERT INTO orders VALUES (204,4,'Москва','2024-01-09','paid',304);\n"
           "INSERT INTO orders VALUES (205,5,'Казань','2024-02-10','new',305);\n"
           "INSERT INTO orders VALUES (206,6,'Тверь','2024-03-11','cancelled',306);\n"
           "INSERT INTO orders VALUES (207,7,'Омск','2024-04-12','paid',307);\n"
           "INSERT INTO orders VALUES (208,8,'Москва','2024-05-13','new',308);\n"
           "INSERT INTO orders VALUES (209,9,'Казань','2024-06-14','cancelled',309);\n"
           "INSERT INTO orders VALUES (210,10,'Тверь','2024-07-15','paid',310);\n"
           "INSERT INTO orders VALUES (211,11,'Омск','2024-08-16','new',311);\n"
           "INSERT INTO orders VALUES (212,12,'Москва','2024-09-17','cancelled',312);\n"
           "INSERT INTO orders VALUES (213,13,'Казань','2024-10-18','paid',313);\n"
           "INSERT INTO orders VALUES (214,14,'Тверь','2024-11-19','new',314);\n"
           "INSERT INTO orders VALUES (215,15,'Омск','2024-12-20','cancelled',315);\n"
           "INSERT INTO orders VALUES (216,16,'Москва','2024-01-21','paid',316);\n"
           "INSERT INTO orders VALUES (217,17,'Казань','2024-02-22','new',317);\n"
           "INSERT INTO orders VALUES (218,18,'Тверь','2024-03-23','cancelled',318);\n"
           "INSERT INTO orders VALUES (219,19,'Омск','2024-04-24','paid',319);\n"
           "INSERT INTO orders VALUES (220,20,'Москва','2024-05-25','new',320);\n"
           "INSERT INTO orders VALUES (221,21,'Казань','2024-06-26','cancelled',321);\n"
           "INSERT INTO orders VALUES (222,22,'Тверь','2024-07-27','paid',322);\n"
           "INSERT INTO orders VALUES (223,23,'Омск','2024-08-28','new',323);\n"
           "INSERT INTO orders VALUES (224,24,'Москва','2024-09-01','cancelled',324);\n"
           "INSERT INTO orders VALUES (225,25,'Казань','2024-10-02','paid',325);\n"
           "INSERT INTO orders VALUES (226,26,'Тверь','2024-11-03','new',326);\n"
           "INSERT INTO orders VALUES (227,27,'Омск','2024-12-04','cancelled',327);\n"
           "INSERT INTO orders VALUES (228,28,'Москва','2024-01-05','paid',328);\n"
           "INSERT INTO orders VALUES (229,29,'Казань','2024-02-06','new',329);\n"
           "INSERT INTO orders VALUES (230,30,'Тверь','2024-03-07','cancelled',330);\n"
           "INSERT INTO orders VALUES (231,31,'Омск','2024-04-08','paid',331);\n"
           "INSERT INTO orders VALUES (232,32,'Москва','2024-05-09','new',332);\n"
           "INSERT INTO orders VALUES (233,33,'Казань','2024-06-10','cancelled',333);\n"
           "INSERT INTO orders VALUES (234,34,'Тверь','2024-07-11','paid',334);\n"
           "INSERT INTO orders VALUES (235,35,'Омск','2024-08-12','new',335);\n"
           "INSERT INTO orders VALUES (236,36,'Москва','2024-09-13','cancelled',336);\n"
           "INSERT INTO orders VALUES (237,37,'Казань','2024-10-14','paid',337);\n"
           "INSERT INTO orders VALUES (238,38,'Тверь','2024-11-15','new',338);\n"
           "INSERT INTO orders VALUES (239,39,'Омск','2024-12-16','cancelled',339);\n"
           "INSERT INTO orders VALUES (240,40,'Москва','2024-01-17','paid',340);\n"
           "INSERT INTO orders VALUES (241,41,'Казань','2024-02-18','new',341);\n"
           "INSERT INTO orders VALUES (242,42,'Тверь','2024-03-19','cancelled',342);\n"
           "INSERT INTO orders VALUES (243,43,'Омск','2024-04-20','paid',343);\n"
           "INSERT INTO orders VALUES (244,44,'Москва','2024-05-21','new',344);\n"
           "INSERT INTO orders VALUES (245,45,'Казань','2024-06-22','cancelled',345);\n"
           "INSERT INTO orders VALUES (246,46,'Тверь','2024-07-23','paid',346);\n"
           "INSERT INTO orders VALUES (247,47,'Омск','2024-08-24','new',347);\n"
           "INSERT INTO orders VALUES (248,48,'Москва','2024-09-25','cancelled',348);\n"
           "INSERT INTO orders VALUES (249,49,'Казань','2024-10-26','paid',349);\n"
           "INSERT INTO orders VALUES (250,0,'Тверь','2024-11-27','new',350);\n"
           "INSERT INTO orders VALUES (251,1,'Омск','2024-12-28','cancelled',351);\n"
           "INSERT INTO orders VALUES (252,2,'Москва','2024-01-01','paid',352);\n"
           "INSERT INTO orders VALUES (253,3,'Казань','2024-02-02','new',353);\n"
           "INSERT INTO orders VALUES (254,4,'Тверь','2024-03-03','cancelled',354);\n"
           "INSERT INTO orders VALUES (255,5,'Омск','2024-04-04','paid',355);\n"
           "INSERT INTO orders VALUES (256,6,'Москва','2024-05-05','new',356);\n"
           "INSERT INTO orders VALUES (257,7,'Казань','2024-06-06','cancelled',357);\n"
           "INSERT INTO orders VALUES (258,8,'Тверь','2024-07-07','paid',358);\n"
           "INSERT INTO orders VALUES (259,9,'Омск','2024-08-08','new',359);\n"
           "INSERT INTO orders VALUES (260,10,'Москва','2024-09-09','cancelled',360);\n"
           "INSERT INTO orders VALUES (261,11,'Казань','2024-10-10','paid',361);\n"
           "INSERT INTO orders VALUES (262,12,'Тверь','2024-11-11','new',362);\n"
           "INSERT INTO orders VALUES (263,13,'Омск','2024-12-12','cancelled',363);\n"
           "INSERT INTO orders VALUES (264,14,'Москва','2024-01-13','paid',364);\n"
           "INSERT INTO orders VALUES (265,15,'Казань','2024-02-14','new',365);\n"
           "INSERT INTO orders VALUES (266,16,'Тверь','2024-03-15','cancelled',366);\n"
           "INSERT INTO orders VALUES (267,17,'Омск','2024-04-16','paid',367);\n"
           "INSERT INTO orders VALUES (268,18,'Москва','2024-05-17','new',368);\n"
           "INSERT INTO orders VALUES (269,19,'Казань','2024-06-18','cancelled',369);\n"
           "INSERT INTO orders VALUES (270,20,'Тверь','2024-07-19','paid',370);\n"
           "INSERT INTO orders VALUES (271,21,'Омск','2024-08-20','new',371);\n"
           "INSERT INTO orders VALUES (272,22,'Москва','2024-09-21','cancelled',372);\n"
           "INSERT INTO orders VALUES (273,23,'Казань','2024-10-22','paid',373);\n"
           "INSERT INTO orders VALUES (274,24,'Тверь','2024-11-23','new',374);\n"
           "INSERT INTO orders VALUES (275,25,'Омск','2024-12-24','cancelled',375);\n"
           "INSERT INTO orders VALUES (276,26,'Москва','2024-01-25','paid',376);\n"
           "INSERT INTO orders VALUES (277,27,'Казань','2024-02-26','new',377);\n"
           "INSERT INTO orders VALUES (278,28,'Тверь','2024-03-27','cancelled',378);\n"
           "INSERT INTO orders VALUES (279,29,'Омск','2024-04-28','paid',379);\n"
           "INSERT INTO orders VALUES (280,30,'Москва','2024-05-01','new',380);\n"
           "INSERT INTO orders VALUES (281,31,'Казань','2024-06-02','cancelled',381);\n"
           "INSERT INTO orders VALUES (282,32,'Тверь','2024-07-03','paid',382);\n"
           "INSERT INTO orders VALUES (283,33,'Омск','2024-08-04','new',383);\n"
           "INSERT INTO orders VALUES (284,34,'Москва','2024-09-05','cancelled',384);\n"
           "INSERT INTO orders VALUES (285,35,'Казань','2024-10-06','paid',385);\n"
           "INSERT INTO orders VALUES (286,36,'Тверь','2024-11-07','new',386);\n"
           "INSERT INTO orders VALUES (287,37,'Омск','2024-12-08','cancelled',387);\n"
           "INSERT INTO orders VALUES (288,38,'Москва','2024-01-09','paid',388);\n"
           "INSERT INTO orders VALUES (289,39,'Казань','2024-02-10','new',389);\n"
           "INSERT INTO orders VALUES (290,40,'Тверь','2024-03-11','cancelled',390);\n"
           "INSERT INTO orders VALUES (291,41,'Омск','2024-04-12','paid',391);\n"
           "INSERT INTO orders VALUES (292,42,'Москва','2024-05-13','new',392);\n"
           "INSERT INTO orders VALUES (293,43,'Казань','2024-06-14','cancelled',393);\n"
           "INSERT INTO orders VALUES (294,44,'Тверь','2024-07-15','paid',394);\n"
           "INSERT INTO orders VALUES (295,45,'Омск','2024-08-16','new',395);\n"
           "INSERT INTO orders VALUES (296,46,'Москва','2024-09-17','cancelled',396);\n"
           "INSERT INTO orders VALUES (297,47,'Казань','2024-10-18','paid',397);\n"
           "INSERT INTO orders VALUES (298,48,'Тверь','2024-11-19','new',398);\n"
           "INSERT INTO orders VALUES (299,49,'Омск','2024-12-20','cancelled',399);\n"
           "INSERT INTO orders VALUES (300,0,'Москва','2024-01-21','paid',400);\n",
  'expected': [[5, 0, 224, 'SCAN orders USING INDEX idx_created']],
  'hint': 'Индекс по created уже упорядочен — TEMP B-TREE для сортировки не понадобится.',
  'check': 'EXPLAIN QUERY PLAN SELECT * FROM orders ORDER BY created LIMIT 10',
  'contains': ['USING INDEX idx_created'],
  'forbid': ['TEMP B-TREE']},
 {'id': 'd3-keyset',
  'mode': 'sql',
  'title': 'Keyset-пагинация',
  'statement': 'Страница заказов упорядочена по (created, id). Последняя строка предыдущей страницы: created '
               "= '2024-03-10', id = 70. Выведите следующие 5 заказов после неё — колонки id, created, без "
               'OFFSET. Условие сравнивайте парой (created, id).',
  'starter': "-- 5 заказов после (created='2024-03-10', id=70)\nSELECT\n",
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, city TEXT NOT NULL, '
           'created TEXT NOT NULL, status TEXT NOT NULL, total INTEGER NOT NULL);\n'
           "INSERT INTO orders VALUES (1,1,'Казань','2024-02-02','new',101);\n"
           "INSERT INTO orders VALUES (2,2,'Тверь','2024-03-03','cancelled',102);\n"
           "INSERT INTO orders VALUES (3,3,'Омск','2024-04-04','paid',103);\n"
           "INSERT INTO orders VALUES (4,4,'Москва','2024-05-05','new',104);\n"
           "INSERT INTO orders VALUES (5,5,'Казань','2024-06-06','cancelled',105);\n"
           "INSERT INTO orders VALUES (6,6,'Тверь','2024-07-07','paid',106);\n"
           "INSERT INTO orders VALUES (7,7,'Омск','2024-08-08','new',107);\n"
           "INSERT INTO orders VALUES (8,8,'Москва','2024-09-09','cancelled',108);\n"
           "INSERT INTO orders VALUES (9,9,'Казань','2024-10-10','paid',109);\n"
           "INSERT INTO orders VALUES (10,10,'Тверь','2024-11-11','new',110);\n"
           "INSERT INTO orders VALUES (11,11,'Омск','2024-12-12','cancelled',111);\n"
           "INSERT INTO orders VALUES (12,12,'Москва','2024-01-13','paid',112);\n"
           "INSERT INTO orders VALUES (13,13,'Казань','2024-02-14','new',113);\n"
           "INSERT INTO orders VALUES (14,14,'Тверь','2024-03-15','cancelled',114);\n"
           "INSERT INTO orders VALUES (15,15,'Омск','2024-04-16','paid',115);\n"
           "INSERT INTO orders VALUES (16,16,'Москва','2024-05-17','new',116);\n"
           "INSERT INTO orders VALUES (17,17,'Казань','2024-06-18','cancelled',117);\n"
           "INSERT INTO orders VALUES (18,18,'Тверь','2024-07-19','paid',118);\n"
           "INSERT INTO orders VALUES (19,19,'Омск','2024-08-20','new',119);\n"
           "INSERT INTO orders VALUES (20,20,'Москва','2024-09-21','cancelled',120);\n"
           "INSERT INTO orders VALUES (21,21,'Казань','2024-10-22','paid',121);\n"
           "INSERT INTO orders VALUES (22,22,'Тверь','2024-11-23','new',122);\n"
           "INSERT INTO orders VALUES (23,23,'Омск','2024-12-24','cancelled',123);\n"
           "INSERT INTO orders VALUES (24,24,'Москва','2024-01-25','paid',124);\n"
           "INSERT INTO orders VALUES (25,25,'Казань','2024-02-26','new',125);\n"
           "INSERT INTO orders VALUES (26,26,'Тверь','2024-03-27','cancelled',126);\n"
           "INSERT INTO orders VALUES (27,27,'Омск','2024-04-28','paid',127);\n"
           "INSERT INTO orders VALUES (28,28,'Москва','2024-05-01','new',128);\n"
           "INSERT INTO orders VALUES (29,29,'Казань','2024-06-02','cancelled',129);\n"
           "INSERT INTO orders VALUES (30,30,'Тверь','2024-07-03','paid',130);\n"
           "INSERT INTO orders VALUES (31,31,'Омск','2024-08-04','new',131);\n"
           "INSERT INTO orders VALUES (32,32,'Москва','2024-09-05','cancelled',132);\n"
           "INSERT INTO orders VALUES (33,33,'Казань','2024-10-06','paid',133);\n"
           "INSERT INTO orders VALUES (34,34,'Тверь','2024-11-07','new',134);\n"
           "INSERT INTO orders VALUES (35,35,'Омск','2024-12-08','cancelled',135);\n"
           "INSERT INTO orders VALUES (36,36,'Москва','2024-01-09','paid',136);\n"
           "INSERT INTO orders VALUES (37,37,'Казань','2024-02-10','new',137);\n"
           "INSERT INTO orders VALUES (38,38,'Тверь','2024-03-11','cancelled',138);\n"
           "INSERT INTO orders VALUES (39,39,'Омск','2024-04-12','paid',139);\n"
           "INSERT INTO orders VALUES (40,40,'Москва','2024-05-13','new',140);\n"
           "INSERT INTO orders VALUES (41,41,'Казань','2024-06-14','cancelled',141);\n"
           "INSERT INTO orders VALUES (42,42,'Тверь','2024-07-15','paid',142);\n"
           "INSERT INTO orders VALUES (43,43,'Омск','2024-08-16','new',143);\n"
           "INSERT INTO orders VALUES (44,44,'Москва','2024-09-17','cancelled',144);\n"
           "INSERT INTO orders VALUES (45,45,'Казань','2024-10-18','paid',145);\n"
           "INSERT INTO orders VALUES (46,46,'Тверь','2024-11-19','new',146);\n"
           "INSERT INTO orders VALUES (47,47,'Омск','2024-12-20','cancelled',147);\n"
           "INSERT INTO orders VALUES (48,48,'Москва','2024-01-21','paid',148);\n"
           "INSERT INTO orders VALUES (49,49,'Казань','2024-02-22','new',149);\n"
           "INSERT INTO orders VALUES (50,0,'Тверь','2024-03-23','cancelled',150);\n"
           "INSERT INTO orders VALUES (51,1,'Омск','2024-04-24','paid',151);\n"
           "INSERT INTO orders VALUES (52,2,'Москва','2024-05-25','new',152);\n"
           "INSERT INTO orders VALUES (53,3,'Казань','2024-06-26','cancelled',153);\n"
           "INSERT INTO orders VALUES (54,4,'Тверь','2024-07-27','paid',154);\n"
           "INSERT INTO orders VALUES (55,5,'Омск','2024-08-28','new',155);\n"
           "INSERT INTO orders VALUES (56,6,'Москва','2024-09-01','cancelled',156);\n"
           "INSERT INTO orders VALUES (57,7,'Казань','2024-10-02','paid',157);\n"
           "INSERT INTO orders VALUES (58,8,'Тверь','2024-11-03','new',158);\n"
           "INSERT INTO orders VALUES (59,9,'Омск','2024-12-04','cancelled',159);\n"
           "INSERT INTO orders VALUES (60,10,'Москва','2024-01-05','paid',160);\n"
           "INSERT INTO orders VALUES (61,11,'Казань','2024-02-06','new',161);\n"
           "INSERT INTO orders VALUES (62,12,'Тверь','2024-03-07','cancelled',162);\n"
           "INSERT INTO orders VALUES (63,13,'Омск','2024-04-08','paid',163);\n"
           "INSERT INTO orders VALUES (64,14,'Москва','2024-05-09','new',164);\n"
           "INSERT INTO orders VALUES (65,15,'Казань','2024-06-10','cancelled',165);\n"
           "INSERT INTO orders VALUES (66,16,'Тверь','2024-07-11','paid',166);\n"
           "INSERT INTO orders VALUES (67,17,'Омск','2024-08-12','new',167);\n"
           "INSERT INTO orders VALUES (68,18,'Москва','2024-09-13','cancelled',168);\n"
           "INSERT INTO orders VALUES (69,19,'Казань','2024-10-14','paid',169);\n"
           "INSERT INTO orders VALUES (70,20,'Тверь','2024-11-15','new',170);\n"
           "INSERT INTO orders VALUES (71,21,'Омск','2024-12-16','cancelled',171);\n"
           "INSERT INTO orders VALUES (72,22,'Москва','2024-01-17','paid',172);\n"
           "INSERT INTO orders VALUES (73,23,'Казань','2024-02-18','new',173);\n"
           "INSERT INTO orders VALUES (74,24,'Тверь','2024-03-19','cancelled',174);\n"
           "INSERT INTO orders VALUES (75,25,'Омск','2024-04-20','paid',175);\n"
           "INSERT INTO orders VALUES (76,26,'Москва','2024-05-21','new',176);\n"
           "INSERT INTO orders VALUES (77,27,'Казань','2024-06-22','cancelled',177);\n"
           "INSERT INTO orders VALUES (78,28,'Тверь','2024-07-23','paid',178);\n"
           "INSERT INTO orders VALUES (79,29,'Омск','2024-08-24','new',179);\n"
           "INSERT INTO orders VALUES (80,30,'Москва','2024-09-25','cancelled',180);\n"
           "INSERT INTO orders VALUES (81,31,'Казань','2024-10-26','paid',181);\n"
           "INSERT INTO orders VALUES (82,32,'Тверь','2024-11-27','new',182);\n"
           "INSERT INTO orders VALUES (83,33,'Омск','2024-12-28','cancelled',183);\n"
           "INSERT INTO orders VALUES (84,34,'Москва','2024-01-01','paid',184);\n"
           "INSERT INTO orders VALUES (85,35,'Казань','2024-02-02','new',185);\n"
           "INSERT INTO orders VALUES (86,36,'Тверь','2024-03-03','cancelled',186);\n"
           "INSERT INTO orders VALUES (87,37,'Омск','2024-04-04','paid',187);\n"
           "INSERT INTO orders VALUES (88,38,'Москва','2024-05-05','new',188);\n"
           "INSERT INTO orders VALUES (89,39,'Казань','2024-06-06','cancelled',189);\n"
           "INSERT INTO orders VALUES (90,40,'Тверь','2024-07-07','paid',190);\n"
           "INSERT INTO orders VALUES (91,41,'Омск','2024-08-08','new',191);\n"
           "INSERT INTO orders VALUES (92,42,'Москва','2024-09-09','cancelled',192);\n"
           "INSERT INTO orders VALUES (93,43,'Казань','2024-10-10','paid',193);\n"
           "INSERT INTO orders VALUES (94,44,'Тверь','2024-11-11','new',194);\n"
           "INSERT INTO orders VALUES (95,45,'Омск','2024-12-12','cancelled',195);\n"
           "INSERT INTO orders VALUES (96,46,'Москва','2024-01-13','paid',196);\n"
           "INSERT INTO orders VALUES (97,47,'Казань','2024-02-14','new',197);\n"
           "INSERT INTO orders VALUES (98,48,'Тверь','2024-03-15','cancelled',198);\n"
           "INSERT INTO orders VALUES (99,49,'Омск','2024-04-16','paid',199);\n"
           "INSERT INTO orders VALUES (100,0,'Москва','2024-05-17','new',200);\n"
           "INSERT INTO orders VALUES (101,1,'Казань','2024-06-18','cancelled',201);\n"
           "INSERT INTO orders VALUES (102,2,'Тверь','2024-07-19','paid',202);\n"
           "INSERT INTO orders VALUES (103,3,'Омск','2024-08-20','new',203);\n"
           "INSERT INTO orders VALUES (104,4,'Москва','2024-09-21','cancelled',204);\n"
           "INSERT INTO orders VALUES (105,5,'Казань','2024-10-22','paid',205);\n"
           "INSERT INTO orders VALUES (106,6,'Тверь','2024-11-23','new',206);\n"
           "INSERT INTO orders VALUES (107,7,'Омск','2024-12-24','cancelled',207);\n"
           "INSERT INTO orders VALUES (108,8,'Москва','2024-01-25','paid',208);\n"
           "INSERT INTO orders VALUES (109,9,'Казань','2024-02-26','new',209);\n"
           "INSERT INTO orders VALUES (110,10,'Тверь','2024-03-27','cancelled',210);\n"
           "INSERT INTO orders VALUES (111,11,'Омск','2024-04-28','paid',211);\n"
           "INSERT INTO orders VALUES (112,12,'Москва','2024-05-01','new',212);\n"
           "INSERT INTO orders VALUES (113,13,'Казань','2024-06-02','cancelled',213);\n"
           "INSERT INTO orders VALUES (114,14,'Тверь','2024-07-03','paid',214);\n"
           "INSERT INTO orders VALUES (115,15,'Омск','2024-08-04','new',215);\n"
           "INSERT INTO orders VALUES (116,16,'Москва','2024-09-05','cancelled',216);\n"
           "INSERT INTO orders VALUES (117,17,'Казань','2024-10-06','paid',217);\n"
           "INSERT INTO orders VALUES (118,18,'Тверь','2024-11-07','new',218);\n"
           "INSERT INTO orders VALUES (119,19,'Омск','2024-12-08','cancelled',219);\n"
           "INSERT INTO orders VALUES (120,20,'Москва','2024-01-09','paid',220);\n"
           "INSERT INTO orders VALUES (121,21,'Казань','2024-02-10','new',221);\n"
           "INSERT INTO orders VALUES (122,22,'Тверь','2024-03-11','cancelled',222);\n"
           "INSERT INTO orders VALUES (123,23,'Омск','2024-04-12','paid',223);\n"
           "INSERT INTO orders VALUES (124,24,'Москва','2024-05-13','new',224);\n"
           "INSERT INTO orders VALUES (125,25,'Казань','2024-06-14','cancelled',225);\n"
           "INSERT INTO orders VALUES (126,26,'Тверь','2024-07-15','paid',226);\n"
           "INSERT INTO orders VALUES (127,27,'Омск','2024-08-16','new',227);\n"
           "INSERT INTO orders VALUES (128,28,'Москва','2024-09-17','cancelled',228);\n"
           "INSERT INTO orders VALUES (129,29,'Казань','2024-10-18','paid',229);\n"
           "INSERT INTO orders VALUES (130,30,'Тверь','2024-11-19','new',230);\n"
           "INSERT INTO orders VALUES (131,31,'Омск','2024-12-20','cancelled',231);\n"
           "INSERT INTO orders VALUES (132,32,'Москва','2024-01-21','paid',232);\n"
           "INSERT INTO orders VALUES (133,33,'Казань','2024-02-22','new',233);\n"
           "INSERT INTO orders VALUES (134,34,'Тверь','2024-03-23','cancelled',234);\n"
           "INSERT INTO orders VALUES (135,35,'Омск','2024-04-24','paid',235);\n"
           "INSERT INTO orders VALUES (136,36,'Москва','2024-05-25','new',236);\n"
           "INSERT INTO orders VALUES (137,37,'Казань','2024-06-26','cancelled',237);\n"
           "INSERT INTO orders VALUES (138,38,'Тверь','2024-07-27','paid',238);\n"
           "INSERT INTO orders VALUES (139,39,'Омск','2024-08-28','new',239);\n"
           "INSERT INTO orders VALUES (140,40,'Москва','2024-09-01','cancelled',240);\n"
           "INSERT INTO orders VALUES (141,41,'Казань','2024-10-02','paid',241);\n"
           "INSERT INTO orders VALUES (142,42,'Тверь','2024-11-03','new',242);\n"
           "INSERT INTO orders VALUES (143,43,'Омск','2024-12-04','cancelled',243);\n"
           "INSERT INTO orders VALUES (144,44,'Москва','2024-01-05','paid',244);\n"
           "INSERT INTO orders VALUES (145,45,'Казань','2024-02-06','new',245);\n"
           "INSERT INTO orders VALUES (146,46,'Тверь','2024-03-07','cancelled',246);\n"
           "INSERT INTO orders VALUES (147,47,'Омск','2024-04-08','paid',247);\n"
           "INSERT INTO orders VALUES (148,48,'Москва','2024-05-09','new',248);\n"
           "INSERT INTO orders VALUES (149,49,'Казань','2024-06-10','cancelled',249);\n"
           "INSERT INTO orders VALUES (150,0,'Тверь','2024-07-11','paid',250);\n"
           "INSERT INTO orders VALUES (151,1,'Омск','2024-08-12','new',251);\n"
           "INSERT INTO orders VALUES (152,2,'Москва','2024-09-13','cancelled',252);\n"
           "INSERT INTO orders VALUES (153,3,'Казань','2024-10-14','paid',253);\n"
           "INSERT INTO orders VALUES (154,4,'Тверь','2024-11-15','new',254);\n"
           "INSERT INTO orders VALUES (155,5,'Омск','2024-12-16','cancelled',255);\n"
           "INSERT INTO orders VALUES (156,6,'Москва','2024-01-17','paid',256);\n"
           "INSERT INTO orders VALUES (157,7,'Казань','2024-02-18','new',257);\n"
           "INSERT INTO orders VALUES (158,8,'Тверь','2024-03-19','cancelled',258);\n"
           "INSERT INTO orders VALUES (159,9,'Омск','2024-04-20','paid',259);\n"
           "INSERT INTO orders VALUES (160,10,'Москва','2024-05-21','new',260);\n"
           "INSERT INTO orders VALUES (161,11,'Казань','2024-06-22','cancelled',261);\n"
           "INSERT INTO orders VALUES (162,12,'Тверь','2024-07-23','paid',262);\n"
           "INSERT INTO orders VALUES (163,13,'Омск','2024-08-24','new',263);\n"
           "INSERT INTO orders VALUES (164,14,'Москва','2024-09-25','cancelled',264);\n"
           "INSERT INTO orders VALUES (165,15,'Казань','2024-10-26','paid',265);\n"
           "INSERT INTO orders VALUES (166,16,'Тверь','2024-11-27','new',266);\n"
           "INSERT INTO orders VALUES (167,17,'Омск','2024-12-28','cancelled',267);\n"
           "INSERT INTO orders VALUES (168,18,'Москва','2024-01-01','paid',268);\n"
           "INSERT INTO orders VALUES (169,19,'Казань','2024-02-02','new',269);\n"
           "INSERT INTO orders VALUES (170,20,'Тверь','2024-03-03','cancelled',270);\n"
           "INSERT INTO orders VALUES (171,21,'Омск','2024-04-04','paid',271);\n"
           "INSERT INTO orders VALUES (172,22,'Москва','2024-05-05','new',272);\n"
           "INSERT INTO orders VALUES (173,23,'Казань','2024-06-06','cancelled',273);\n"
           "INSERT INTO orders VALUES (174,24,'Тверь','2024-07-07','paid',274);\n"
           "INSERT INTO orders VALUES (175,25,'Омск','2024-08-08','new',275);\n"
           "INSERT INTO orders VALUES (176,26,'Москва','2024-09-09','cancelled',276);\n"
           "INSERT INTO orders VALUES (177,27,'Казань','2024-10-10','paid',277);\n"
           "INSERT INTO orders VALUES (178,28,'Тверь','2024-11-11','new',278);\n"
           "INSERT INTO orders VALUES (179,29,'Омск','2024-12-12','cancelled',279);\n"
           "INSERT INTO orders VALUES (180,30,'Москва','2024-01-13','paid',280);\n"
           "INSERT INTO orders VALUES (181,31,'Казань','2024-02-14','new',281);\n"
           "INSERT INTO orders VALUES (182,32,'Тверь','2024-03-15','cancelled',282);\n"
           "INSERT INTO orders VALUES (183,33,'Омск','2024-04-16','paid',283);\n"
           "INSERT INTO orders VALUES (184,34,'Москва','2024-05-17','new',284);\n"
           "INSERT INTO orders VALUES (185,35,'Казань','2024-06-18','cancelled',285);\n"
           "INSERT INTO orders VALUES (186,36,'Тверь','2024-07-19','paid',286);\n"
           "INSERT INTO orders VALUES (187,37,'Омск','2024-08-20','new',287);\n"
           "INSERT INTO orders VALUES (188,38,'Москва','2024-09-21','cancelled',288);\n"
           "INSERT INTO orders VALUES (189,39,'Казань','2024-10-22','paid',289);\n"
           "INSERT INTO orders VALUES (190,40,'Тверь','2024-11-23','new',290);\n"
           "INSERT INTO orders VALUES (191,41,'Омск','2024-12-24','cancelled',291);\n"
           "INSERT INTO orders VALUES (192,42,'Москва','2024-01-25','paid',292);\n"
           "INSERT INTO orders VALUES (193,43,'Казань','2024-02-26','new',293);\n"
           "INSERT INTO orders VALUES (194,44,'Тверь','2024-03-27','cancelled',294);\n"
           "INSERT INTO orders VALUES (195,45,'Омск','2024-04-28','paid',295);\n"
           "INSERT INTO orders VALUES (196,46,'Москва','2024-05-01','new',296);\n"
           "INSERT INTO orders VALUES (197,47,'Казань','2024-06-02','cancelled',297);\n"
           "INSERT INTO orders VALUES (198,48,'Тверь','2024-07-03','paid',298);\n"
           "INSERT INTO orders VALUES (199,49,'Омск','2024-08-04','new',299);\n"
           "INSERT INTO orders VALUES (200,0,'Москва','2024-09-05','cancelled',300);\n"
           "INSERT INTO orders VALUES (201,1,'Казань','2024-10-06','paid',301);\n"
           "INSERT INTO orders VALUES (202,2,'Тверь','2024-11-07','new',302);\n"
           "INSERT INTO orders VALUES (203,3,'Омск','2024-12-08','cancelled',303);\n"
           "INSERT INTO orders VALUES (204,4,'Москва','2024-01-09','paid',304);\n"
           "INSERT INTO orders VALUES (205,5,'Казань','2024-02-10','new',305);\n"
           "INSERT INTO orders VALUES (206,6,'Тверь','2024-03-11','cancelled',306);\n"
           "INSERT INTO orders VALUES (207,7,'Омск','2024-04-12','paid',307);\n"
           "INSERT INTO orders VALUES (208,8,'Москва','2024-05-13','new',308);\n"
           "INSERT INTO orders VALUES (209,9,'Казань','2024-06-14','cancelled',309);\n"
           "INSERT INTO orders VALUES (210,10,'Тверь','2024-07-15','paid',310);\n"
           "INSERT INTO orders VALUES (211,11,'Омск','2024-08-16','new',311);\n"
           "INSERT INTO orders VALUES (212,12,'Москва','2024-09-17','cancelled',312);\n"
           "INSERT INTO orders VALUES (213,13,'Казань','2024-10-18','paid',313);\n"
           "INSERT INTO orders VALUES (214,14,'Тверь','2024-11-19','new',314);\n"
           "INSERT INTO orders VALUES (215,15,'Омск','2024-12-20','cancelled',315);\n"
           "INSERT INTO orders VALUES (216,16,'Москва','2024-01-21','paid',316);\n"
           "INSERT INTO orders VALUES (217,17,'Казань','2024-02-22','new',317);\n"
           "INSERT INTO orders VALUES (218,18,'Тверь','2024-03-23','cancelled',318);\n"
           "INSERT INTO orders VALUES (219,19,'Омск','2024-04-24','paid',319);\n"
           "INSERT INTO orders VALUES (220,20,'Москва','2024-05-25','new',320);\n"
           "INSERT INTO orders VALUES (221,21,'Казань','2024-06-26','cancelled',321);\n"
           "INSERT INTO orders VALUES (222,22,'Тверь','2024-07-27','paid',322);\n"
           "INSERT INTO orders VALUES (223,23,'Омск','2024-08-28','new',323);\n"
           "INSERT INTO orders VALUES (224,24,'Москва','2024-09-01','cancelled',324);\n"
           "INSERT INTO orders VALUES (225,25,'Казань','2024-10-02','paid',325);\n"
           "INSERT INTO orders VALUES (226,26,'Тверь','2024-11-03','new',326);\n"
           "INSERT INTO orders VALUES (227,27,'Омск','2024-12-04','cancelled',327);\n"
           "INSERT INTO orders VALUES (228,28,'Москва','2024-01-05','paid',328);\n"
           "INSERT INTO orders VALUES (229,29,'Казань','2024-02-06','new',329);\n"
           "INSERT INTO orders VALUES (230,30,'Тверь','2024-03-07','cancelled',330);\n"
           "INSERT INTO orders VALUES (231,31,'Омск','2024-04-08','paid',331);\n"
           "INSERT INTO orders VALUES (232,32,'Москва','2024-05-09','new',332);\n"
           "INSERT INTO orders VALUES (233,33,'Казань','2024-06-10','cancelled',333);\n"
           "INSERT INTO orders VALUES (234,34,'Тверь','2024-07-11','paid',334);\n"
           "INSERT INTO orders VALUES (235,35,'Омск','2024-08-12','new',335);\n"
           "INSERT INTO orders VALUES (236,36,'Москва','2024-09-13','cancelled',336);\n"
           "INSERT INTO orders VALUES (237,37,'Казань','2024-10-14','paid',337);\n"
           "INSERT INTO orders VALUES (238,38,'Тверь','2024-11-15','new',338);\n"
           "INSERT INTO orders VALUES (239,39,'Омск','2024-12-16','cancelled',339);\n"
           "INSERT INTO orders VALUES (240,40,'Москва','2024-01-17','paid',340);\n"
           "INSERT INTO orders VALUES (241,41,'Казань','2024-02-18','new',341);\n"
           "INSERT INTO orders VALUES (242,42,'Тверь','2024-03-19','cancelled',342);\n"
           "INSERT INTO orders VALUES (243,43,'Омск','2024-04-20','paid',343);\n"
           "INSERT INTO orders VALUES (244,44,'Москва','2024-05-21','new',344);\n"
           "INSERT INTO orders VALUES (245,45,'Казань','2024-06-22','cancelled',345);\n"
           "INSERT INTO orders VALUES (246,46,'Тверь','2024-07-23','paid',346);\n"
           "INSERT INTO orders VALUES (247,47,'Омск','2024-08-24','new',347);\n"
           "INSERT INTO orders VALUES (248,48,'Москва','2024-09-25','cancelled',348);\n"
           "INSERT INTO orders VALUES (249,49,'Казань','2024-10-26','paid',349);\n"
           "INSERT INTO orders VALUES (250,0,'Тверь','2024-11-27','new',350);\n"
           "INSERT INTO orders VALUES (251,1,'Омск','2024-12-28','cancelled',351);\n"
           "INSERT INTO orders VALUES (252,2,'Москва','2024-01-01','paid',352);\n"
           "INSERT INTO orders VALUES (253,3,'Казань','2024-02-02','new',353);\n"
           "INSERT INTO orders VALUES (254,4,'Тверь','2024-03-03','cancelled',354);\n"
           "INSERT INTO orders VALUES (255,5,'Омск','2024-04-04','paid',355);\n"
           "INSERT INTO orders VALUES (256,6,'Москва','2024-05-05','new',356);\n"
           "INSERT INTO orders VALUES (257,7,'Казань','2024-06-06','cancelled',357);\n"
           "INSERT INTO orders VALUES (258,8,'Тверь','2024-07-07','paid',358);\n"
           "INSERT INTO orders VALUES (259,9,'Омск','2024-08-08','new',359);\n"
           "INSERT INTO orders VALUES (260,10,'Москва','2024-09-09','cancelled',360);\n"
           "INSERT INTO orders VALUES (261,11,'Казань','2024-10-10','paid',361);\n"
           "INSERT INTO orders VALUES (262,12,'Тверь','2024-11-11','new',362);\n"
           "INSERT INTO orders VALUES (263,13,'Омск','2024-12-12','cancelled',363);\n"
           "INSERT INTO orders VALUES (264,14,'Москва','2024-01-13','paid',364);\n"
           "INSERT INTO orders VALUES (265,15,'Казань','2024-02-14','new',365);\n"
           "INSERT INTO orders VALUES (266,16,'Тверь','2024-03-15','cancelled',366);\n"
           "INSERT INTO orders VALUES (267,17,'Омск','2024-04-16','paid',367);\n"
           "INSERT INTO orders VALUES (268,18,'Москва','2024-05-17','new',368);\n"
           "INSERT INTO orders VALUES (269,19,'Казань','2024-06-18','cancelled',369);\n"
           "INSERT INTO orders VALUES (270,20,'Тверь','2024-07-19','paid',370);\n"
           "INSERT INTO orders VALUES (271,21,'Омск','2024-08-20','new',371);\n"
           "INSERT INTO orders VALUES (272,22,'Москва','2024-09-21','cancelled',372);\n"
           "INSERT INTO orders VALUES (273,23,'Казань','2024-10-22','paid',373);\n"
           "INSERT INTO orders VALUES (274,24,'Тверь','2024-11-23','new',374);\n"
           "INSERT INTO orders VALUES (275,25,'Омск','2024-12-24','cancelled',375);\n"
           "INSERT INTO orders VALUES (276,26,'Москва','2024-01-25','paid',376);\n"
           "INSERT INTO orders VALUES (277,27,'Казань','2024-02-26','new',377);\n"
           "INSERT INTO orders VALUES (278,28,'Тверь','2024-03-27','cancelled',378);\n"
           "INSERT INTO orders VALUES (279,29,'Омск','2024-04-28','paid',379);\n"
           "INSERT INTO orders VALUES (280,30,'Москва','2024-05-01','new',380);\n"
           "INSERT INTO orders VALUES (281,31,'Казань','2024-06-02','cancelled',381);\n"
           "INSERT INTO orders VALUES (282,32,'Тверь','2024-07-03','paid',382);\n"
           "INSERT INTO orders VALUES (283,33,'Омск','2024-08-04','new',383);\n"
           "INSERT INTO orders VALUES (284,34,'Москва','2024-09-05','cancelled',384);\n"
           "INSERT INTO orders VALUES (285,35,'Казань','2024-10-06','paid',385);\n"
           "INSERT INTO orders VALUES (286,36,'Тверь','2024-11-07','new',386);\n"
           "INSERT INTO orders VALUES (287,37,'Омск','2024-12-08','cancelled',387);\n"
           "INSERT INTO orders VALUES (288,38,'Москва','2024-01-09','paid',388);\n"
           "INSERT INTO orders VALUES (289,39,'Казань','2024-02-10','new',389);\n"
           "INSERT INTO orders VALUES (290,40,'Тверь','2024-03-11','cancelled',390);\n"
           "INSERT INTO orders VALUES (291,41,'Омск','2024-04-12','paid',391);\n"
           "INSERT INTO orders VALUES (292,42,'Москва','2024-05-13','new',392);\n"
           "INSERT INTO orders VALUES (293,43,'Казань','2024-06-14','cancelled',393);\n"
           "INSERT INTO orders VALUES (294,44,'Тверь','2024-07-15','paid',394);\n"
           "INSERT INTO orders VALUES (295,45,'Омск','2024-08-16','new',395);\n"
           "INSERT INTO orders VALUES (296,46,'Москва','2024-09-17','cancelled',396);\n"
           "INSERT INTO orders VALUES (297,47,'Казань','2024-10-18','paid',397);\n"
           "INSERT INTO orders VALUES (298,48,'Тверь','2024-11-19','new',398);\n"
           "INSERT INTO orders VALUES (299,49,'Омск','2024-12-20','cancelled',399);\n"
           "INSERT INTO orders VALUES (300,0,'Москва','2024-01-21','paid',400);\n",
  'expected': [[38, '2024-03-11'],
               [122, '2024-03-11'],
               [206, '2024-03-11'],
               [290, '2024-03-11'],
               [14, '2024-03-15']],
  'expected_cols': ['id', 'created'],
  'hint': "WHERE (created, id) > ('2024-03-10', 70) ORDER BY created, id LIMIT 5.",
  'ordered': True,
  'forbid': ['OFFSET']},
 {'id': 'd3-join-index',
  'mode': 'sql',
  'title': 'Индекс под соединение',
  'statement': 'Запрос соединяет order_items с products по product_id: SELECT p.title FROM order_items i '
               'JOIN products p ON p.id = i.product_id WHERE i.order_id = 4. Создайте индекс на order_items, '
               'чтобы строки позиций по заказу находились поиском (в плане — SEARCH i USING … order_id).',
  'starter': '-- индекс для WHERE i.order_id = ...\nCREATE INDEX\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, UNIQUE (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [[3, 0, 55, 'SEARCH i USING COVERING INDEX idx_items_order (order_id=?)'],
               [7, 0, 45, 'SEARCH p USING INTEGER PRIMARY KEY (rowid=?)']],
  'hint': 'Индексируется столбец, по которому ищем позиции: order_id.',
  'check': 'EXPLAIN QUERY PLAN SELECT p.title FROM order_items i JOIN products p ON p.id = i.product_id '
           'WHERE i.order_id = 4',
  'contains': ['SEARCH i USING'],
  'forbid': ['SCAN i']},
 {'id': 'd3-selectivity',
  'mode': 'sql',
  'title': 'Селективность столбцов',
  'statement': 'Посчитайте селективность двух столбцов — долю различных значений: COUNT(DISTINCT x) * 1.0 / '
               'COUNT(*). Выведите одну строку из колонок customer_sel, status_sel (округлите каждую до 3 '
               'знаков через ROUND).',
  'starter': '-- селективность customer_id и status\nSELECT\n',
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, city TEXT NOT NULL, '
           'created TEXT NOT NULL, status TEXT NOT NULL, total INTEGER NOT NULL);\n'
           "INSERT INTO orders VALUES (1,1,'Казань','2024-02-02','new',101);\n"
           "INSERT INTO orders VALUES (2,2,'Тверь','2024-03-03','cancelled',102);\n"
           "INSERT INTO orders VALUES (3,3,'Омск','2024-04-04','paid',103);\n"
           "INSERT INTO orders VALUES (4,4,'Москва','2024-05-05','new',104);\n"
           "INSERT INTO orders VALUES (5,5,'Казань','2024-06-06','cancelled',105);\n"
           "INSERT INTO orders VALUES (6,6,'Тверь','2024-07-07','paid',106);\n"
           "INSERT INTO orders VALUES (7,7,'Омск','2024-08-08','new',107);\n"
           "INSERT INTO orders VALUES (8,8,'Москва','2024-09-09','cancelled',108);\n"
           "INSERT INTO orders VALUES (9,9,'Казань','2024-10-10','paid',109);\n"
           "INSERT INTO orders VALUES (10,10,'Тверь','2024-11-11','new',110);\n"
           "INSERT INTO orders VALUES (11,11,'Омск','2024-12-12','cancelled',111);\n"
           "INSERT INTO orders VALUES (12,12,'Москва','2024-01-13','paid',112);\n"
           "INSERT INTO orders VALUES (13,13,'Казань','2024-02-14','new',113);\n"
           "INSERT INTO orders VALUES (14,14,'Тверь','2024-03-15','cancelled',114);\n"
           "INSERT INTO orders VALUES (15,15,'Омск','2024-04-16','paid',115);\n"
           "INSERT INTO orders VALUES (16,16,'Москва','2024-05-17','new',116);\n"
           "INSERT INTO orders VALUES (17,17,'Казань','2024-06-18','cancelled',117);\n"
           "INSERT INTO orders VALUES (18,18,'Тверь','2024-07-19','paid',118);\n"
           "INSERT INTO orders VALUES (19,19,'Омск','2024-08-20','new',119);\n"
           "INSERT INTO orders VALUES (20,20,'Москва','2024-09-21','cancelled',120);\n"
           "INSERT INTO orders VALUES (21,21,'Казань','2024-10-22','paid',121);\n"
           "INSERT INTO orders VALUES (22,22,'Тверь','2024-11-23','new',122);\n"
           "INSERT INTO orders VALUES (23,23,'Омск','2024-12-24','cancelled',123);\n"
           "INSERT INTO orders VALUES (24,24,'Москва','2024-01-25','paid',124);\n"
           "INSERT INTO orders VALUES (25,25,'Казань','2024-02-26','new',125);\n"
           "INSERT INTO orders VALUES (26,26,'Тверь','2024-03-27','cancelled',126);\n"
           "INSERT INTO orders VALUES (27,27,'Омск','2024-04-28','paid',127);\n"
           "INSERT INTO orders VALUES (28,28,'Москва','2024-05-01','new',128);\n"
           "INSERT INTO orders VALUES (29,29,'Казань','2024-06-02','cancelled',129);\n"
           "INSERT INTO orders VALUES (30,30,'Тверь','2024-07-03','paid',130);\n"
           "INSERT INTO orders VALUES (31,31,'Омск','2024-08-04','new',131);\n"
           "INSERT INTO orders VALUES (32,32,'Москва','2024-09-05','cancelled',132);\n"
           "INSERT INTO orders VALUES (33,33,'Казань','2024-10-06','paid',133);\n"
           "INSERT INTO orders VALUES (34,34,'Тверь','2024-11-07','new',134);\n"
           "INSERT INTO orders VALUES (35,35,'Омск','2024-12-08','cancelled',135);\n"
           "INSERT INTO orders VALUES (36,36,'Москва','2024-01-09','paid',136);\n"
           "INSERT INTO orders VALUES (37,37,'Казань','2024-02-10','new',137);\n"
           "INSERT INTO orders VALUES (38,38,'Тверь','2024-03-11','cancelled',138);\n"
           "INSERT INTO orders VALUES (39,39,'Омск','2024-04-12','paid',139);\n"
           "INSERT INTO orders VALUES (40,40,'Москва','2024-05-13','new',140);\n"
           "INSERT INTO orders VALUES (41,41,'Казань','2024-06-14','cancelled',141);\n"
           "INSERT INTO orders VALUES (42,42,'Тверь','2024-07-15','paid',142);\n"
           "INSERT INTO orders VALUES (43,43,'Омск','2024-08-16','new',143);\n"
           "INSERT INTO orders VALUES (44,44,'Москва','2024-09-17','cancelled',144);\n"
           "INSERT INTO orders VALUES (45,45,'Казань','2024-10-18','paid',145);\n"
           "INSERT INTO orders VALUES (46,46,'Тверь','2024-11-19','new',146);\n"
           "INSERT INTO orders VALUES (47,47,'Омск','2024-12-20','cancelled',147);\n"
           "INSERT INTO orders VALUES (48,48,'Москва','2024-01-21','paid',148);\n"
           "INSERT INTO orders VALUES (49,49,'Казань','2024-02-22','new',149);\n"
           "INSERT INTO orders VALUES (50,0,'Тверь','2024-03-23','cancelled',150);\n"
           "INSERT INTO orders VALUES (51,1,'Омск','2024-04-24','paid',151);\n"
           "INSERT INTO orders VALUES (52,2,'Москва','2024-05-25','new',152);\n"
           "INSERT INTO orders VALUES (53,3,'Казань','2024-06-26','cancelled',153);\n"
           "INSERT INTO orders VALUES (54,4,'Тверь','2024-07-27','paid',154);\n"
           "INSERT INTO orders VALUES (55,5,'Омск','2024-08-28','new',155);\n"
           "INSERT INTO orders VALUES (56,6,'Москва','2024-09-01','cancelled',156);\n"
           "INSERT INTO orders VALUES (57,7,'Казань','2024-10-02','paid',157);\n"
           "INSERT INTO orders VALUES (58,8,'Тверь','2024-11-03','new',158);\n"
           "INSERT INTO orders VALUES (59,9,'Омск','2024-12-04','cancelled',159);\n"
           "INSERT INTO orders VALUES (60,10,'Москва','2024-01-05','paid',160);\n"
           "INSERT INTO orders VALUES (61,11,'Казань','2024-02-06','new',161);\n"
           "INSERT INTO orders VALUES (62,12,'Тверь','2024-03-07','cancelled',162);\n"
           "INSERT INTO orders VALUES (63,13,'Омск','2024-04-08','paid',163);\n"
           "INSERT INTO orders VALUES (64,14,'Москва','2024-05-09','new',164);\n"
           "INSERT INTO orders VALUES (65,15,'Казань','2024-06-10','cancelled',165);\n"
           "INSERT INTO orders VALUES (66,16,'Тверь','2024-07-11','paid',166);\n"
           "INSERT INTO orders VALUES (67,17,'Омск','2024-08-12','new',167);\n"
           "INSERT INTO orders VALUES (68,18,'Москва','2024-09-13','cancelled',168);\n"
           "INSERT INTO orders VALUES (69,19,'Казань','2024-10-14','paid',169);\n"
           "INSERT INTO orders VALUES (70,20,'Тверь','2024-11-15','new',170);\n"
           "INSERT INTO orders VALUES (71,21,'Омск','2024-12-16','cancelled',171);\n"
           "INSERT INTO orders VALUES (72,22,'Москва','2024-01-17','paid',172);\n"
           "INSERT INTO orders VALUES (73,23,'Казань','2024-02-18','new',173);\n"
           "INSERT INTO orders VALUES (74,24,'Тверь','2024-03-19','cancelled',174);\n"
           "INSERT INTO orders VALUES (75,25,'Омск','2024-04-20','paid',175);\n"
           "INSERT INTO orders VALUES (76,26,'Москва','2024-05-21','new',176);\n"
           "INSERT INTO orders VALUES (77,27,'Казань','2024-06-22','cancelled',177);\n"
           "INSERT INTO orders VALUES (78,28,'Тверь','2024-07-23','paid',178);\n"
           "INSERT INTO orders VALUES (79,29,'Омск','2024-08-24','new',179);\n"
           "INSERT INTO orders VALUES (80,30,'Москва','2024-09-25','cancelled',180);\n"
           "INSERT INTO orders VALUES (81,31,'Казань','2024-10-26','paid',181);\n"
           "INSERT INTO orders VALUES (82,32,'Тверь','2024-11-27','new',182);\n"
           "INSERT INTO orders VALUES (83,33,'Омск','2024-12-28','cancelled',183);\n"
           "INSERT INTO orders VALUES (84,34,'Москва','2024-01-01','paid',184);\n"
           "INSERT INTO orders VALUES (85,35,'Казань','2024-02-02','new',185);\n"
           "INSERT INTO orders VALUES (86,36,'Тверь','2024-03-03','cancelled',186);\n"
           "INSERT INTO orders VALUES (87,37,'Омск','2024-04-04','paid',187);\n"
           "INSERT INTO orders VALUES (88,38,'Москва','2024-05-05','new',188);\n"
           "INSERT INTO orders VALUES (89,39,'Казань','2024-06-06','cancelled',189);\n"
           "INSERT INTO orders VALUES (90,40,'Тверь','2024-07-07','paid',190);\n"
           "INSERT INTO orders VALUES (91,41,'Омск','2024-08-08','new',191);\n"
           "INSERT INTO orders VALUES (92,42,'Москва','2024-09-09','cancelled',192);\n"
           "INSERT INTO orders VALUES (93,43,'Казань','2024-10-10','paid',193);\n"
           "INSERT INTO orders VALUES (94,44,'Тверь','2024-11-11','new',194);\n"
           "INSERT INTO orders VALUES (95,45,'Омск','2024-12-12','cancelled',195);\n"
           "INSERT INTO orders VALUES (96,46,'Москва','2024-01-13','paid',196);\n"
           "INSERT INTO orders VALUES (97,47,'Казань','2024-02-14','new',197);\n"
           "INSERT INTO orders VALUES (98,48,'Тверь','2024-03-15','cancelled',198);\n"
           "INSERT INTO orders VALUES (99,49,'Омск','2024-04-16','paid',199);\n"
           "INSERT INTO orders VALUES (100,0,'Москва','2024-05-17','new',200);\n"
           "INSERT INTO orders VALUES (101,1,'Казань','2024-06-18','cancelled',201);\n"
           "INSERT INTO orders VALUES (102,2,'Тверь','2024-07-19','paid',202);\n"
           "INSERT INTO orders VALUES (103,3,'Омск','2024-08-20','new',203);\n"
           "INSERT INTO orders VALUES (104,4,'Москва','2024-09-21','cancelled',204);\n"
           "INSERT INTO orders VALUES (105,5,'Казань','2024-10-22','paid',205);\n"
           "INSERT INTO orders VALUES (106,6,'Тверь','2024-11-23','new',206);\n"
           "INSERT INTO orders VALUES (107,7,'Омск','2024-12-24','cancelled',207);\n"
           "INSERT INTO orders VALUES (108,8,'Москва','2024-01-25','paid',208);\n"
           "INSERT INTO orders VALUES (109,9,'Казань','2024-02-26','new',209);\n"
           "INSERT INTO orders VALUES (110,10,'Тверь','2024-03-27','cancelled',210);\n"
           "INSERT INTO orders VALUES (111,11,'Омск','2024-04-28','paid',211);\n"
           "INSERT INTO orders VALUES (112,12,'Москва','2024-05-01','new',212);\n"
           "INSERT INTO orders VALUES (113,13,'Казань','2024-06-02','cancelled',213);\n"
           "INSERT INTO orders VALUES (114,14,'Тверь','2024-07-03','paid',214);\n"
           "INSERT INTO orders VALUES (115,15,'Омск','2024-08-04','new',215);\n"
           "INSERT INTO orders VALUES (116,16,'Москва','2024-09-05','cancelled',216);\n"
           "INSERT INTO orders VALUES (117,17,'Казань','2024-10-06','paid',217);\n"
           "INSERT INTO orders VALUES (118,18,'Тверь','2024-11-07','new',218);\n"
           "INSERT INTO orders VALUES (119,19,'Омск','2024-12-08','cancelled',219);\n"
           "INSERT INTO orders VALUES (120,20,'Москва','2024-01-09','paid',220);\n"
           "INSERT INTO orders VALUES (121,21,'Казань','2024-02-10','new',221);\n"
           "INSERT INTO orders VALUES (122,22,'Тверь','2024-03-11','cancelled',222);\n"
           "INSERT INTO orders VALUES (123,23,'Омск','2024-04-12','paid',223);\n"
           "INSERT INTO orders VALUES (124,24,'Москва','2024-05-13','new',224);\n"
           "INSERT INTO orders VALUES (125,25,'Казань','2024-06-14','cancelled',225);\n"
           "INSERT INTO orders VALUES (126,26,'Тверь','2024-07-15','paid',226);\n"
           "INSERT INTO orders VALUES (127,27,'Омск','2024-08-16','new',227);\n"
           "INSERT INTO orders VALUES (128,28,'Москва','2024-09-17','cancelled',228);\n"
           "INSERT INTO orders VALUES (129,29,'Казань','2024-10-18','paid',229);\n"
           "INSERT INTO orders VALUES (130,30,'Тверь','2024-11-19','new',230);\n"
           "INSERT INTO orders VALUES (131,31,'Омск','2024-12-20','cancelled',231);\n"
           "INSERT INTO orders VALUES (132,32,'Москва','2024-01-21','paid',232);\n"
           "INSERT INTO orders VALUES (133,33,'Казань','2024-02-22','new',233);\n"
           "INSERT INTO orders VALUES (134,34,'Тверь','2024-03-23','cancelled',234);\n"
           "INSERT INTO orders VALUES (135,35,'Омск','2024-04-24','paid',235);\n"
           "INSERT INTO orders VALUES (136,36,'Москва','2024-05-25','new',236);\n"
           "INSERT INTO orders VALUES (137,37,'Казань','2024-06-26','cancelled',237);\n"
           "INSERT INTO orders VALUES (138,38,'Тверь','2024-07-27','paid',238);\n"
           "INSERT INTO orders VALUES (139,39,'Омск','2024-08-28','new',239);\n"
           "INSERT INTO orders VALUES (140,40,'Москва','2024-09-01','cancelled',240);\n"
           "INSERT INTO orders VALUES (141,41,'Казань','2024-10-02','paid',241);\n"
           "INSERT INTO orders VALUES (142,42,'Тверь','2024-11-03','new',242);\n"
           "INSERT INTO orders VALUES (143,43,'Омск','2024-12-04','cancelled',243);\n"
           "INSERT INTO orders VALUES (144,44,'Москва','2024-01-05','paid',244);\n"
           "INSERT INTO orders VALUES (145,45,'Казань','2024-02-06','new',245);\n"
           "INSERT INTO orders VALUES (146,46,'Тверь','2024-03-07','cancelled',246);\n"
           "INSERT INTO orders VALUES (147,47,'Омск','2024-04-08','paid',247);\n"
           "INSERT INTO orders VALUES (148,48,'Москва','2024-05-09','new',248);\n"
           "INSERT INTO orders VALUES (149,49,'Казань','2024-06-10','cancelled',249);\n"
           "INSERT INTO orders VALUES (150,0,'Тверь','2024-07-11','paid',250);\n"
           "INSERT INTO orders VALUES (151,1,'Омск','2024-08-12','new',251);\n"
           "INSERT INTO orders VALUES (152,2,'Москва','2024-09-13','cancelled',252);\n"
           "INSERT INTO orders VALUES (153,3,'Казань','2024-10-14','paid',253);\n"
           "INSERT INTO orders VALUES (154,4,'Тверь','2024-11-15','new',254);\n"
           "INSERT INTO orders VALUES (155,5,'Омск','2024-12-16','cancelled',255);\n"
           "INSERT INTO orders VALUES (156,6,'Москва','2024-01-17','paid',256);\n"
           "INSERT INTO orders VALUES (157,7,'Казань','2024-02-18','new',257);\n"
           "INSERT INTO orders VALUES (158,8,'Тверь','2024-03-19','cancelled',258);\n"
           "INSERT INTO orders VALUES (159,9,'Омск','2024-04-20','paid',259);\n"
           "INSERT INTO orders VALUES (160,10,'Москва','2024-05-21','new',260);\n"
           "INSERT INTO orders VALUES (161,11,'Казань','2024-06-22','cancelled',261);\n"
           "INSERT INTO orders VALUES (162,12,'Тверь','2024-07-23','paid',262);\n"
           "INSERT INTO orders VALUES (163,13,'Омск','2024-08-24','new',263);\n"
           "INSERT INTO orders VALUES (164,14,'Москва','2024-09-25','cancelled',264);\n"
           "INSERT INTO orders VALUES (165,15,'Казань','2024-10-26','paid',265);\n"
           "INSERT INTO orders VALUES (166,16,'Тверь','2024-11-27','new',266);\n"
           "INSERT INTO orders VALUES (167,17,'Омск','2024-12-28','cancelled',267);\n"
           "INSERT INTO orders VALUES (168,18,'Москва','2024-01-01','paid',268);\n"
           "INSERT INTO orders VALUES (169,19,'Казань','2024-02-02','new',269);\n"
           "INSERT INTO orders VALUES (170,20,'Тверь','2024-03-03','cancelled',270);\n"
           "INSERT INTO orders VALUES (171,21,'Омск','2024-04-04','paid',271);\n"
           "INSERT INTO orders VALUES (172,22,'Москва','2024-05-05','new',272);\n"
           "INSERT INTO orders VALUES (173,23,'Казань','2024-06-06','cancelled',273);\n"
           "INSERT INTO orders VALUES (174,24,'Тверь','2024-07-07','paid',274);\n"
           "INSERT INTO orders VALUES (175,25,'Омск','2024-08-08','new',275);\n"
           "INSERT INTO orders VALUES (176,26,'Москва','2024-09-09','cancelled',276);\n"
           "INSERT INTO orders VALUES (177,27,'Казань','2024-10-10','paid',277);\n"
           "INSERT INTO orders VALUES (178,28,'Тверь','2024-11-11','new',278);\n"
           "INSERT INTO orders VALUES (179,29,'Омск','2024-12-12','cancelled',279);\n"
           "INSERT INTO orders VALUES (180,30,'Москва','2024-01-13','paid',280);\n"
           "INSERT INTO orders VALUES (181,31,'Казань','2024-02-14','new',281);\n"
           "INSERT INTO orders VALUES (182,32,'Тверь','2024-03-15','cancelled',282);\n"
           "INSERT INTO orders VALUES (183,33,'Омск','2024-04-16','paid',283);\n"
           "INSERT INTO orders VALUES (184,34,'Москва','2024-05-17','new',284);\n"
           "INSERT INTO orders VALUES (185,35,'Казань','2024-06-18','cancelled',285);\n"
           "INSERT INTO orders VALUES (186,36,'Тверь','2024-07-19','paid',286);\n"
           "INSERT INTO orders VALUES (187,37,'Омск','2024-08-20','new',287);\n"
           "INSERT INTO orders VALUES (188,38,'Москва','2024-09-21','cancelled',288);\n"
           "INSERT INTO orders VALUES (189,39,'Казань','2024-10-22','paid',289);\n"
           "INSERT INTO orders VALUES (190,40,'Тверь','2024-11-23','new',290);\n"
           "INSERT INTO orders VALUES (191,41,'Омск','2024-12-24','cancelled',291);\n"
           "INSERT INTO orders VALUES (192,42,'Москва','2024-01-25','paid',292);\n"
           "INSERT INTO orders VALUES (193,43,'Казань','2024-02-26','new',293);\n"
           "INSERT INTO orders VALUES (194,44,'Тверь','2024-03-27','cancelled',294);\n"
           "INSERT INTO orders VALUES (195,45,'Омск','2024-04-28','paid',295);\n"
           "INSERT INTO orders VALUES (196,46,'Москва','2024-05-01','new',296);\n"
           "INSERT INTO orders VALUES (197,47,'Казань','2024-06-02','cancelled',297);\n"
           "INSERT INTO orders VALUES (198,48,'Тверь','2024-07-03','paid',298);\n"
           "INSERT INTO orders VALUES (199,49,'Омск','2024-08-04','new',299);\n"
           "INSERT INTO orders VALUES (200,0,'Москва','2024-09-05','cancelled',300);\n"
           "INSERT INTO orders VALUES (201,1,'Казань','2024-10-06','paid',301);\n"
           "INSERT INTO orders VALUES (202,2,'Тверь','2024-11-07','new',302);\n"
           "INSERT INTO orders VALUES (203,3,'Омск','2024-12-08','cancelled',303);\n"
           "INSERT INTO orders VALUES (204,4,'Москва','2024-01-09','paid',304);\n"
           "INSERT INTO orders VALUES (205,5,'Казань','2024-02-10','new',305);\n"
           "INSERT INTO orders VALUES (206,6,'Тверь','2024-03-11','cancelled',306);\n"
           "INSERT INTO orders VALUES (207,7,'Омск','2024-04-12','paid',307);\n"
           "INSERT INTO orders VALUES (208,8,'Москва','2024-05-13','new',308);\n"
           "INSERT INTO orders VALUES (209,9,'Казань','2024-06-14','cancelled',309);\n"
           "INSERT INTO orders VALUES (210,10,'Тверь','2024-07-15','paid',310);\n"
           "INSERT INTO orders VALUES (211,11,'Омск','2024-08-16','new',311);\n"
           "INSERT INTO orders VALUES (212,12,'Москва','2024-09-17','cancelled',312);\n"
           "INSERT INTO orders VALUES (213,13,'Казань','2024-10-18','paid',313);\n"
           "INSERT INTO orders VALUES (214,14,'Тверь','2024-11-19','new',314);\n"
           "INSERT INTO orders VALUES (215,15,'Омск','2024-12-20','cancelled',315);\n"
           "INSERT INTO orders VALUES (216,16,'Москва','2024-01-21','paid',316);\n"
           "INSERT INTO orders VALUES (217,17,'Казань','2024-02-22','new',317);\n"
           "INSERT INTO orders VALUES (218,18,'Тверь','2024-03-23','cancelled',318);\n"
           "INSERT INTO orders VALUES (219,19,'Омск','2024-04-24','paid',319);\n"
           "INSERT INTO orders VALUES (220,20,'Москва','2024-05-25','new',320);\n"
           "INSERT INTO orders VALUES (221,21,'Казань','2024-06-26','cancelled',321);\n"
           "INSERT INTO orders VALUES (222,22,'Тверь','2024-07-27','paid',322);\n"
           "INSERT INTO orders VALUES (223,23,'Омск','2024-08-28','new',323);\n"
           "INSERT INTO orders VALUES (224,24,'Москва','2024-09-01','cancelled',324);\n"
           "INSERT INTO orders VALUES (225,25,'Казань','2024-10-02','paid',325);\n"
           "INSERT INTO orders VALUES (226,26,'Тверь','2024-11-03','new',326);\n"
           "INSERT INTO orders VALUES (227,27,'Омск','2024-12-04','cancelled',327);\n"
           "INSERT INTO orders VALUES (228,28,'Москва','2024-01-05','paid',328);\n"
           "INSERT INTO orders VALUES (229,29,'Казань','2024-02-06','new',329);\n"
           "INSERT INTO orders VALUES (230,30,'Тверь','2024-03-07','cancelled',330);\n"
           "INSERT INTO orders VALUES (231,31,'Омск','2024-04-08','paid',331);\n"
           "INSERT INTO orders VALUES (232,32,'Москва','2024-05-09','new',332);\n"
           "INSERT INTO orders VALUES (233,33,'Казань','2024-06-10','cancelled',333);\n"
           "INSERT INTO orders VALUES (234,34,'Тверь','2024-07-11','paid',334);\n"
           "INSERT INTO orders VALUES (235,35,'Омск','2024-08-12','new',335);\n"
           "INSERT INTO orders VALUES (236,36,'Москва','2024-09-13','cancelled',336);\n"
           "INSERT INTO orders VALUES (237,37,'Казань','2024-10-14','paid',337);\n"
           "INSERT INTO orders VALUES (238,38,'Тверь','2024-11-15','new',338);\n"
           "INSERT INTO orders VALUES (239,39,'Омск','2024-12-16','cancelled',339);\n"
           "INSERT INTO orders VALUES (240,40,'Москва','2024-01-17','paid',340);\n"
           "INSERT INTO orders VALUES (241,41,'Казань','2024-02-18','new',341);\n"
           "INSERT INTO orders VALUES (242,42,'Тверь','2024-03-19','cancelled',342);\n"
           "INSERT INTO orders VALUES (243,43,'Омск','2024-04-20','paid',343);\n"
           "INSERT INTO orders VALUES (244,44,'Москва','2024-05-21','new',344);\n"
           "INSERT INTO orders VALUES (245,45,'Казань','2024-06-22','cancelled',345);\n"
           "INSERT INTO orders VALUES (246,46,'Тверь','2024-07-23','paid',346);\n"
           "INSERT INTO orders VALUES (247,47,'Омск','2024-08-24','new',347);\n"
           "INSERT INTO orders VALUES (248,48,'Москва','2024-09-25','cancelled',348);\n"
           "INSERT INTO orders VALUES (249,49,'Казань','2024-10-26','paid',349);\n"
           "INSERT INTO orders VALUES (250,0,'Тверь','2024-11-27','new',350);\n"
           "INSERT INTO orders VALUES (251,1,'Омск','2024-12-28','cancelled',351);\n"
           "INSERT INTO orders VALUES (252,2,'Москва','2024-01-01','paid',352);\n"
           "INSERT INTO orders VALUES (253,3,'Казань','2024-02-02','new',353);\n"
           "INSERT INTO orders VALUES (254,4,'Тверь','2024-03-03','cancelled',354);\n"
           "INSERT INTO orders VALUES (255,5,'Омск','2024-04-04','paid',355);\n"
           "INSERT INTO orders VALUES (256,6,'Москва','2024-05-05','new',356);\n"
           "INSERT INTO orders VALUES (257,7,'Казань','2024-06-06','cancelled',357);\n"
           "INSERT INTO orders VALUES (258,8,'Тверь','2024-07-07','paid',358);\n"
           "INSERT INTO orders VALUES (259,9,'Омск','2024-08-08','new',359);\n"
           "INSERT INTO orders VALUES (260,10,'Москва','2024-09-09','cancelled',360);\n"
           "INSERT INTO orders VALUES (261,11,'Казань','2024-10-10','paid',361);\n"
           "INSERT INTO orders VALUES (262,12,'Тверь','2024-11-11','new',362);\n"
           "INSERT INTO orders VALUES (263,13,'Омск','2024-12-12','cancelled',363);\n"
           "INSERT INTO orders VALUES (264,14,'Москва','2024-01-13','paid',364);\n"
           "INSERT INTO orders VALUES (265,15,'Казань','2024-02-14','new',365);\n"
           "INSERT INTO orders VALUES (266,16,'Тверь','2024-03-15','cancelled',366);\n"
           "INSERT INTO orders VALUES (267,17,'Омск','2024-04-16','paid',367);\n"
           "INSERT INTO orders VALUES (268,18,'Москва','2024-05-17','new',368);\n"
           "INSERT INTO orders VALUES (269,19,'Казань','2024-06-18','cancelled',369);\n"
           "INSERT INTO orders VALUES (270,20,'Тверь','2024-07-19','paid',370);\n"
           "INSERT INTO orders VALUES (271,21,'Омск','2024-08-20','new',371);\n"
           "INSERT INTO orders VALUES (272,22,'Москва','2024-09-21','cancelled',372);\n"
           "INSERT INTO orders VALUES (273,23,'Казань','2024-10-22','paid',373);\n"
           "INSERT INTO orders VALUES (274,24,'Тверь','2024-11-23','new',374);\n"
           "INSERT INTO orders VALUES (275,25,'Омск','2024-12-24','cancelled',375);\n"
           "INSERT INTO orders VALUES (276,26,'Москва','2024-01-25','paid',376);\n"
           "INSERT INTO orders VALUES (277,27,'Казань','2024-02-26','new',377);\n"
           "INSERT INTO orders VALUES (278,28,'Тверь','2024-03-27','cancelled',378);\n"
           "INSERT INTO orders VALUES (279,29,'Омск','2024-04-28','paid',379);\n"
           "INSERT INTO orders VALUES (280,30,'Москва','2024-05-01','new',380);\n"
           "INSERT INTO orders VALUES (281,31,'Казань','2024-06-02','cancelled',381);\n"
           "INSERT INTO orders VALUES (282,32,'Тверь','2024-07-03','paid',382);\n"
           "INSERT INTO orders VALUES (283,33,'Омск','2024-08-04','new',383);\n"
           "INSERT INTO orders VALUES (284,34,'Москва','2024-09-05','cancelled',384);\n"
           "INSERT INTO orders VALUES (285,35,'Казань','2024-10-06','paid',385);\n"
           "INSERT INTO orders VALUES (286,36,'Тверь','2024-11-07','new',386);\n"
           "INSERT INTO orders VALUES (287,37,'Омск','2024-12-08','cancelled',387);\n"
           "INSERT INTO orders VALUES (288,38,'Москва','2024-01-09','paid',388);\n"
           "INSERT INTO orders VALUES (289,39,'Казань','2024-02-10','new',389);\n"
           "INSERT INTO orders VALUES (290,40,'Тверь','2024-03-11','cancelled',390);\n"
           "INSERT INTO orders VALUES (291,41,'Омск','2024-04-12','paid',391);\n"
           "INSERT INTO orders VALUES (292,42,'Москва','2024-05-13','new',392);\n"
           "INSERT INTO orders VALUES (293,43,'Казань','2024-06-14','cancelled',393);\n"
           "INSERT INTO orders VALUES (294,44,'Тверь','2024-07-15','paid',394);\n"
           "INSERT INTO orders VALUES (295,45,'Омск','2024-08-16','new',395);\n"
           "INSERT INTO orders VALUES (296,46,'Москва','2024-09-17','cancelled',396);\n"
           "INSERT INTO orders VALUES (297,47,'Казань','2024-10-18','paid',397);\n"
           "INSERT INTO orders VALUES (298,48,'Тверь','2024-11-19','new',398);\n"
           "INSERT INTO orders VALUES (299,49,'Омск','2024-12-20','cancelled',399);\n"
           "INSERT INTO orders VALUES (300,0,'Москва','2024-01-21','paid',400);\n",
  'expected': [[0.167, 0.01]],
  'expected_cols': ['customer_sel', 'status_sel'],
  'hint': 'Чем ближе доля к 1, тем лучше индекс; у status всего три значения — индекс по нему слабый.'},
 {'id': 'd3-index-list',
  'mode': 'sql',
  'title': 'Какие индексы есть',
  'statement': 'Выведите названия индексов таблицы t по алфавиту через pragma_index_list (колонка name).',
  'starter': '-- индексы таблицы t\nSELECT\n',
  'setup': 'CREATE TABLE t (a INTEGER, b INTEGER, c INTEGER);\n'
           'CREATE INDEX t_a ON t (a);\n'
           'CREATE INDEX t_ab ON t (a, b);\n'
           'CREATE UNIQUE INDEX t_c ON t (c);\n',
  'expected': [['t_a'], ['t_ab'], ['t_c']],
  'expected_cols': ['name'],
  'hint': "SELECT name FROM pragma_index_list('t') ORDER BY name; индекс t_a лишний, ведь есть t_ab.",
  'ordered': True},
 {'id': 'd3-binary-search',
  'mode': 'func',
  'func': 'probe_count',
  'title': 'Бинарный поиск: число проб',
  'statement': 'Отсортированный список ключей — это страница индекса. Напишите probe_count(keys, target): '
               'пара [позиция или -1, число сравнений], где поиск ведётся делением пополам: mid = (lo + hi) '
               '// 2, одно сравнение на пробу.',
  'starter': 'def probe_count(keys, target):\n    pass\n',
  'tests': [{'args': [[1, 3, 5, 7, 9, 11], 7], 'expected': [3, 3]},
            {'args': [[1, 3, 5, 7, 9, 11], 4], 'expected': [-1, 3]},
            {'args': [[], 1], 'expected': [-1, 0]},
            {'args': [[0,
                       2,
                       4,
                       6,
                       8,
                       10,
                       12,
                       14,
                       16,
                       18,
                       20,
                       22,
                       24,
                       26,
                       28,
                       30,
                       32,
                       34,
                       36,
                       38,
                       40,
                       42,
                       44,
                       46,
                       48,
                       50,
                       52,
                       54,
                       56,
                       58,
                       60,
                       62,
                       64,
                       66,
                       68,
                       70,
                       72,
                       74,
                       76,
                       78,
                       80,
                       82,
                       84,
                       86,
                       88,
                       90,
                       92,
                       94,
                       96,
                       98,
                       100,
                       102,
                       104,
                       106,
                       108,
                       110,
                       112,
                       114,
                       116,
                       118,
                       120,
                       122,
                       124,
                       126,
                       128,
                       130,
                       132,
                       134,
                       136,
                       138,
                       140,
                       142,
                       144,
                       146,
                       148,
                       150,
                       152,
                       154,
                       156,
                       158,
                       160,
                       162,
                       164,
                       166,
                       168,
                       170,
                       172,
                       174,
                       176,
                       178,
                       180,
                       182,
                       184,
                       186,
                       188,
                       190,
                       192,
                       194,
                       196,
                       198,
                       200,
                       202,
                       204,
                       206,
                       208,
                       210,
                       212,
                       214,
                       216,
                       218,
                       220,
                       222,
                       224,
                       226,
                       228,
                       230,
                       232,
                       234,
                       236,
                       238,
                       240,
                       242,
                       244,
                       246,
                       248,
                       250,
                       252,
                       254,
                       256,
                       258,
                       260,
                       262,
                       264,
                       266,
                       268,
                       270,
                       272,
                       274,
                       276,
                       278,
                       280,
                       282,
                       284,
                       286,
                       288,
                       290,
                       292,
                       294,
                       296,
                       298,
                       300,
                       302,
                       304,
                       306,
                       308,
                       310,
                       312,
                       314,
                       316,
                       318,
                       320,
                       322,
                       324,
                       326,
                       328,
                       330,
                       332,
                       334,
                       336,
                       338,
                       340,
                       342,
                       344,
                       346,
                       348,
                       350,
                       352,
                       354,
                       356,
                       358,
                       360,
                       362,
                       364,
                       366,
                       368,
                       370,
                       372,
                       374,
                       376,
                       378,
                       380,
                       382,
                       384,
                       386,
                       388,
                       390,
                       392,
                       394,
                       396,
                       398,
                       400,
                       402,
                       404,
                       406,
                       408,
                       410,
                       412,
                       414,
                       416,
                       418,
                       420,
                       422,
                       424,
                       426,
                       428,
                       430,
                       432,
                       434,
                       436,
                       438,
                       440,
                       442,
                       444,
                       446,
                       448,
                       450,
                       452,
                       454,
                       456,
                       458,
                       460,
                       462,
                       464,
                       466,
                       468,
                       470,
                       472,
                       474,
                       476,
                       478,
                       480,
                       482,
                       484,
                       486,
                       488,
                       490,
                       492,
                       494,
                       496,
                       498,
                       500,
                       502,
                       504,
                       506,
                       508,
                       510,
                       512,
                       514,
                       516,
                       518,
                       520,
                       522,
                       524,
                       526,
                       528,
                       530,
                       532,
                       534,
                       536,
                       538,
                       540,
                       542,
                       544,
                       546,
                       548,
                       550,
                       552,
                       554,
                       556,
                       558,
                       560,
                       562,
                       564,
                       566,
                       568,
                       570,
                       572,
                       574,
                       576,
                       578,
                       580,
                       582,
                       584,
                       586,
                       588,
                       590,
                       592,
                       594,
                       596,
                       598,
                       600,
                       602,
                       604,
                       606,
                       608,
                       610,
                       612,
                       614,
                       616,
                       618,
                       620,
                       622,
                       624,
                       626,
                       628,
                       630,
                       632,
                       634,
                       636,
                       638,
                       640,
                       642,
                       644,
                       646,
                       648,
                       650,
                       652,
                       654,
                       656,
                       658,
                       660,
                       662,
                       664,
                       666,
                       668,
                       670,
                       672,
                       674,
                       676,
                       678,
                       680,
                       682,
                       684,
                       686,
                       688,
                       690,
                       692,
                       694,
                       696,
                       698,
                       700,
                       702,
                       704,
                       706,
                       708,
                       710,
                       712,
                       714,
                       716,
                       718,
                       720,
                       722,
                       724,
                       726,
                       728,
                       730,
                       732,
                       734,
                       736,
                       738,
                       740,
                       742,
                       744,
                       746,
                       748,
                       750,
                       752,
                       754,
                       756,
                       758,
                       760,
                       762,
                       764,
                       766,
                       768,
                       770,
                       772,
                       774,
                       776,
                       778,
                       780,
                       782,
                       784,
                       786,
                       788,
                       790,
                       792,
                       794,
                       796,
                       798,
                       800,
                       802,
                       804,
                       806,
                       808,
                       810,
                       812,
                       814,
                       816,
                       818,
                       820,
                       822,
                       824,
                       826,
                       828,
                       830,
                       832,
                       834,
                       836,
                       838,
                       840,
                       842,
                       844,
                       846,
                       848,
                       850,
                       852,
                       854,
                       856,
                       858,
                       860,
                       862,
                       864,
                       866,
                       868,
                       870,
                       872,
                       874,
                       876,
                       878,
                       880,
                       882,
                       884,
                       886,
                       888,
                       890,
                       892,
                       894,
                       896,
                       898,
                       900,
                       902,
                       904,
                       906,
                       908,
                       910,
                       912,
                       914,
                       916,
                       918,
                       920,
                       922,
                       924,
                       926,
                       928,
                       930,
                       932,
                       934,
                       936,
                       938,
                       940,
                       942,
                       944,
                       946,
                       948,
                       950,
                       952,
                       954,
                       956,
                       958,
                       960,
                       962,
                       964,
                       966,
                       968,
                       970,
                       972,
                       974,
                       976,
                       978,
                       980,
                       982,
                       984,
                       986,
                       988,
                       990,
                       992,
                       994,
                       996,
                       998],
                      998],
             'expected': [499, 9]},
            {'args': [[0,
                       2,
                       4,
                       6,
                       8,
                       10,
                       12,
                       14,
                       16,
                       18,
                       20,
                       22,
                       24,
                       26,
                       28,
                       30,
                       32,
                       34,
                       36,
                       38,
                       40,
                       42,
                       44,
                       46,
                       48,
                       50,
                       52,
                       54,
                       56,
                       58,
                       60,
                       62,
                       64,
                       66,
                       68,
                       70,
                       72,
                       74,
                       76,
                       78,
                       80,
                       82,
                       84,
                       86,
                       88,
                       90,
                       92,
                       94,
                       96,
                       98,
                       100,
                       102,
                       104,
                       106,
                       108,
                       110,
                       112,
                       114,
                       116,
                       118,
                       120,
                       122,
                       124,
                       126,
                       128,
                       130,
                       132,
                       134,
                       136,
                       138,
                       140,
                       142,
                       144,
                       146,
                       148,
                       150,
                       152,
                       154,
                       156,
                       158,
                       160,
                       162,
                       164,
                       166,
                       168,
                       170,
                       172,
                       174,
                       176,
                       178,
                       180,
                       182,
                       184,
                       186,
                       188,
                       190,
                       192,
                       194,
                       196,
                       198,
                       200,
                       202,
                       204,
                       206,
                       208,
                       210,
                       212,
                       214,
                       216,
                       218,
                       220,
                       222,
                       224,
                       226,
                       228,
                       230,
                       232,
                       234,
                       236,
                       238,
                       240,
                       242,
                       244,
                       246,
                       248,
                       250,
                       252,
                       254,
                       256,
                       258,
                       260,
                       262,
                       264,
                       266,
                       268,
                       270,
                       272,
                       274,
                       276,
                       278,
                       280,
                       282,
                       284,
                       286,
                       288,
                       290,
                       292,
                       294,
                       296,
                       298,
                       300,
                       302,
                       304,
                       306,
                       308,
                       310,
                       312,
                       314,
                       316,
                       318,
                       320,
                       322,
                       324,
                       326,
                       328,
                       330,
                       332,
                       334,
                       336,
                       338,
                       340,
                       342,
                       344,
                       346,
                       348,
                       350,
                       352,
                       354,
                       356,
                       358,
                       360,
                       362,
                       364,
                       366,
                       368,
                       370,
                       372,
                       374,
                       376,
                       378,
                       380,
                       382,
                       384,
                       386,
                       388,
                       390,
                       392,
                       394,
                       396,
                       398,
                       400,
                       402,
                       404,
                       406,
                       408,
                       410,
                       412,
                       414,
                       416,
                       418,
                       420,
                       422,
                       424,
                       426,
                       428,
                       430,
                       432,
                       434,
                       436,
                       438,
                       440,
                       442,
                       444,
                       446,
                       448,
                       450,
                       452,
                       454,
                       456,
                       458,
                       460,
                       462,
                       464,
                       466,
                       468,
                       470,
                       472,
                       474,
                       476,
                       478,
                       480,
                       482,
                       484,
                       486,
                       488,
                       490,
                       492,
                       494,
                       496,
                       498,
                       500,
                       502,
                       504,
                       506,
                       508,
                       510,
                       512,
                       514,
                       516,
                       518,
                       520,
                       522,
                       524,
                       526,
                       528,
                       530,
                       532,
                       534,
                       536,
                       538,
                       540,
                       542,
                       544,
                       546,
                       548,
                       550,
                       552,
                       554,
                       556,
                       558,
                       560,
                       562,
                       564,
                       566,
                       568,
                       570,
                       572,
                       574,
                       576,
                       578,
                       580,
                       582,
                       584,
                       586,
                       588,
                       590,
                       592,
                       594,
                       596,
                       598,
                       600,
                       602,
                       604,
                       606,
                       608,
                       610,
                       612,
                       614,
                       616,
                       618,
                       620,
                       622,
                       624,
                       626,
                       628,
                       630,
                       632,
                       634,
                       636,
                       638,
                       640,
                       642,
                       644,
                       646,
                       648,
                       650,
                       652,
                       654,
                       656,
                       658,
                       660,
                       662,
                       664,
                       666,
                       668,
                       670,
                       672,
                       674,
                       676,
                       678,
                       680,
                       682,
                       684,
                       686,
                       688,
                       690,
                       692,
                       694,
                       696,
                       698,
                       700,
                       702,
                       704,
                       706,
                       708,
                       710,
                       712,
                       714,
                       716,
                       718,
                       720,
                       722,
                       724,
                       726,
                       728,
                       730,
                       732,
                       734,
                       736,
                       738,
                       740,
                       742,
                       744,
                       746,
                       748,
                       750,
                       752,
                       754,
                       756,
                       758,
                       760,
                       762,
                       764,
                       766,
                       768,
                       770,
                       772,
                       774,
                       776,
                       778,
                       780,
                       782,
                       784,
                       786,
                       788,
                       790,
                       792,
                       794,
                       796,
                       798,
                       800,
                       802,
                       804,
                       806,
                       808,
                       810,
                       812,
                       814,
                       816,
                       818,
                       820,
                       822,
                       824,
                       826,
                       828,
                       830,
                       832,
                       834,
                       836,
                       838,
                       840,
                       842,
                       844,
                       846,
                       848,
                       850,
                       852,
                       854,
                       856,
                       858,
                       860,
                       862,
                       864,
                       866,
                       868,
                       870,
                       872,
                       874,
                       876,
                       878,
                       880,
                       882,
                       884,
                       886,
                       888,
                       890,
                       892,
                       894,
                       896,
                       898,
                       900,
                       902,
                       904,
                       906,
                       908,
                       910,
                       912,
                       914,
                       916,
                       918,
                       920,
                       922,
                       924,
                       926,
                       928,
                       930,
                       932,
                       934,
                       936,
                       938,
                       940,
                       942,
                       944,
                       946,
                       948,
                       950,
                       952,
                       954,
                       956,
                       958,
                       960,
                       962,
                       964,
                       966,
                       968,
                       970,
                       972,
                       974,
                       976,
                       978,
                       980,
                       982,
                       984,
                       986,
                       988,
                       990,
                       992,
                       994,
                       996,
                       998],
                      501],
             'expected': [-1, 9]},
            {'args': [[5], 5], 'expected': [0, 1]}],
  'hint': 'Классический бинарный поиск; считайте каждую проверку keys[mid] как одну пробу.'},
 {'id': 'd3-btree-height',
  'mode': 'func',
  'func': 'btree_height',
  'title': 'Высота B-дерева',
  'statement': 'Страница индекса вмещает fanout ссылок. Напишите btree_height(rows, fanout): минимальное '
               'число уровней h (h ≥ 1), при котором fanout ** h ≥ rows. Для rows ≤ 1 вернуть 1.',
  'starter': 'def btree_height(rows, fanout):\n    pass\n',
  'tests': [{'args': [1, 300], 'expected': 1},
            {'args': [300, 300], 'expected': 1},
            {'args': [301, 300], 'expected': 2},
            {'args': [1000000, 100], 'expected': 3},
            {'args': [1000000000, 300], 'expected': 4},
            {'args': [1000000000, 100], 'expected': 5}],
  'hint': 'Цикл: умножайте вместимость на fanout, пока она меньше rows.'},
 {'id': 'd3-btree-contains',
  'mode': 'func',
  'func': 'btree_search',
  'title': 'Поиск в B-дереве',
  'statement': 'Узел — словарь {"keys": [...], "kids": [...]}: у листа kids пуст, у внутреннего узла '
               'len(kids) = len(keys) + 1 (дети слева от первого ключа, между ключами, справа от '
               'последнего). Напишите btree_search(node, key): пара [найден ли ключ (True/False), сколько '
               'узлов прочитано]. Ключ ищется в узле, иначе спуск в нужного ребёнка.',
  'starter': 'def btree_search(node, key):\n    pass\n',
  'tests': [{'args': [{'keys': [50],
                       'kids': [{'keys': [10, 30], 'kids': []}, {'keys': [70, 90], 'kids': []}]},
                      30],
             'expected': [True, 2]},
            {'args': [{'keys': [50],
                       'kids': [{'keys': [10, 30], 'kids': []}, {'keys': [70, 90], 'kids': []}]},
                      90],
             'expected': [True, 2]},
            {'args': [{'keys': [50],
                       'kids': [{'keys': [10, 30], 'kids': []}, {'keys': [70, 90], 'kids': []}]},
                      60],
             'expected': [False, 2]},
            {'args': [{'keys': [50],
                       'kids': [{'keys': [10, 30], 'kids': []}, {'keys': [70, 90], 'kids': []}]},
                      50],
             'expected': [True, 1]},
            {'args': [{'keys': [], 'kids': []}, 1], 'expected': [False, 1]}],
  'hint': 'Найдите позицию i — число ключей узла, меньших искомого; спуститесь в kids[i]. Каждый узел — одно '
          'чтение.'},
 {'id': 'd3-range-scan',
  'mode': 'func',
  'func': 'range_scan',
  'title': 'Диапазон по цепочке листьев',
  'statement': 'B+-дерево: листья — отсортированные списки, лежащие по порядку. Напишите range_scan(leaves, '
               'lo, hi): пара [ключи из диапазона lo ≤ k ≤ hi по порядку, сколько листьев прочитано]. Читать '
               'нужно только листья от первого, где может быть lo, до последнего, где ещё есть ключи ≤ hi '
               '(пустые и лишние листья не читаем).',
  'starter': 'def range_scan(leaves, lo, hi):\n    pass\n',
  'tests': [{'args': [[[10, 20, 25], [30, 40, 55], [60, 70, 90]], 35, 70], 'expected': [[40, 55, 60, 70], 2]},
            {'args': [[[10, 20, 25], [30, 40, 55], [60, 70, 90]], 0, 5], 'expected': [[], 0]},
            {'args': [[[10, 20, 25], [30, 40, 55], [60, 70, 90]], 100, 200], 'expected': [[], 0]},
            {'args': [[[10, 20, 25], [30, 40, 55], [60, 70, 90]], 25, 30], 'expected': [[25, 30], 2]},
            {'args': [[], 1, 2], 'expected': [[], 0]}],
  'hint': 'Пропустите листья, целиком меньшие lo; остановитесь на листе, начинающемся с ключа больше hi.'},
 {'id': 'd3-leaf-split',
  'mode': 'func',
  'func': 'insert_leaf',
  'title': 'Расщепление листа',
  'statement': 'Лист вмещает не больше m ключей. Напишите insert_leaf(leaf, key, m): вставьте key в '
               'отсортированный лист; если ключей стало больше m, разделите лист пополам (левая часть — '
               'ceil(len/2) ключей) и верните [левый, правый, первый_ключ_правого]; иначе верните [лист].',
  'starter': 'def insert_leaf(leaf, key, m):\n    pass\n',
  'tests': [{'args': [[10, 20, 30], 25, 4], 'expected': [[10, 20, 25, 30]]},
            {'args': [[10, 20, 30, 40], 25, 4], 'expected': [[10, 20, 25], [30, 40], 30]},
            {'args': [[10, 20, 30, 40], 50, 4], 'expected': [[10, 20, 30], [40, 50], 40]},
            {'args': [[], 5, 2], 'expected': [[5]]},
            {'args': [[1, 2], 3, 2], 'expected': [[1, 2], [3], 3]},
            {'args': [[1, 2, 3], 0, 3], 'expected': [[0, 1], [2, 3], 2]}],
  'hint': 'Вставьте и отсортируйте; при переполнении разрежьте список в точке (n + 1) // 2.'},
 {'id': 'd3-usable-prefix',
  'mode': 'func',
  'func': 'usable_prefix',
  'title': 'Сколько столбцов индекса работает',
  'statement': "Индекс — список столбцов, условия — словарь «столбец → '=' или 'range'». Напишите "
               'usable_prefix(index_cols, conds): сколько ведущих столбцов индекса используется для поиска. '
               'Считаем подряд столбцы с равенством; первый столбец с диапазоном тоже используется, но '
               'дальше идти нельзя; столбец без условия обрывает счёт.',
  'starter': 'def usable_prefix(index_cols, conds):\n    pass\n',
  'tests': [{'args': [['city', 'created'], {'city': '=', 'created': 'range'}], 'expected': 2},
            {'args': [['city', 'created'], {'created': 'range'}], 'expected': 0},
            {'args': [['a', 'b', 'c'], {'a': '=', 'c': '='}], 'expected': 1},
            {'args': [['a', 'b', 'c'], {'a': '=', 'b': '=', 'c': '='}], 'expected': 3},
            {'args': [['a', 'b', 'c'], {'a': 'range', 'b': '='}], 'expected': 1},
            {'args': [['a'], {}], 'expected': 0}],
  'hint': 'Идите по столбцам индекса слева направо: равенство — засчитать и продолжить, диапазон — засчитать '
          'и остановиться, нет условия — остановиться.'},
 {'id': 'd3-choose-plan',
  'mode': 'func',
  'func': 'choose_plan',
  'title': 'Индекс или просмотр',
  'statement': 'Оптимизатор сравнивает стоимости. Просмотр таблицы читает table_pages страниц. Поиск по '
               'индексу читает height страниц индекса плюс по странице за каждую подходящую строку: height + '
               "rows * selectivity. Напишите choose_plan(table_pages, rows, selectivity, height): 'index', "
               "если индекс строго дешевле, иначе 'scan'.",
  'starter': 'def choose_plan(table_pages, rows, selectivity, height):\n    pass\n',
  'tests': [{'args': [10000, 1000000, 1e-05, 3], 'expected': 'index'},
            {'args': [10000, 1000000, 0.5, 3], 'expected': 'scan'},
            {'args': [10000, 1000000, 0.01, 3], 'expected': 'scan'},
            {'args': [100, 5000, 0.02, 2], 'expected': 'scan'},
            {'args': [100, 5000, 0.0001, 2], 'expected': 'index'}],
  'hint': 'Посчитайте обе стоимости и сравните строго: индекс выигрывает только при малой доле подходящих '
          'строк.'},
 {'id': 'd3-redundant-indexes',
  'mode': 'func',
  'func': 'redundant_indexes',
  'title': 'Лишние индексы',
  'statement': 'Индексы заданы списками столбцов. Индекс лишний, если его столбцы — собственное начало '
               '(левый префикс) другого, более длинного индекса, либо он полностью совпадает с другим (тогда '
               'лишним считаем второй из них). Напишите redundant_indexes(indexes): отсортированный список '
               'номеров (с нуля) лишних индексов.',
  'starter': 'def redundant_indexes(indexes):\n    pass\n',
  'tests': [{'args': [[['a'], ['a', 'b'], ['b']]], 'expected': [0]},
            {'args': [[['a', 'b'], ['a', 'b']]], 'expected': [1]},
            {'args': [[['a'], ['b'], ['c']]], 'expected': []},
            {'args': [[['a'], ['a', 'b'], ['a', 'b', 'c']]], 'expected': [0, 1]},
            {'args': [[]], 'expected': []},
            {'args': [[['b', 'a'], ['a', 'b'], ['b']]], 'expected': [2]}],
  'hint': 'Для каждого индекса проверьте, не является ли он префиксом более длинного; точные дубликаты — '
          'лишний тот, что идёт позже.'}]}
