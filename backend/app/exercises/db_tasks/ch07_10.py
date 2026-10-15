"""Задачи книги «Базы данных: под капотом»: главы 7–10."""

TASKS: dict[int, list[dict]] = {
    7: [
        {
            "id": "shard-hash",
            "mode": "func",
            "func": "hash_distribution",
            "title": "Шардирование по хешу",
            "statement": (
                "Напишите функцию hash_distribution(keys, n): шард ключа — "
                "zlib.crc32(ключ в UTF-8) mod n. Верните список из n чисел — "
                "сколько ключей попало в каждый шард."
            ),
            "starter": "import zlib\n\n\ndef hash_distribution(keys, n):\n    pass\n",
            "tests": [
                {"args": [["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11", "user12", "user13", "user14", "user15", "user16", "user17", "user18", "user19"], 4], "expected": [4, 6, 4, 6]},
                {"args": [[], 3], "expected": [0, 0, 0]},
                {"args": [["a"], 1], "expected": [1]},
                {"args": [["x", "y", "z"], 2], "expected": [0, 3]},
                {"args": [["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11", "user12", "user13", "user14", "user15", "user16", "user17", "user18", "user19", "user20", "user21", "user22", "user23", "user24", "user25", "user26", "user27", "user28", "user29", "user30", "user31", "user32", "user33", "user34", "user35", "user36", "user37", "user38", "user39", "user40", "user41", "user42", "user43", "user44", "user45", "user46", "user47", "user48", "user49", "user50", "user51", "user52", "user53", "user54", "user55", "user56", "user57", "user58", "user59", "user60", "user61", "user62", "user63", "user64", "user65", "user66", "user67", "user68", "user69", "user70", "user71", "user72", "user73", "user74", "user75", "user76", "user77", "user78", "user79", "user80", "user81", "user82", "user83", "user84", "user85", "user86", "user87", "user88", "user89", "user90", "user91", "user92", "user93", "user94", "user95", "user96", "user97", "user98", "user99"], 5], "expected": [20, 14, 20, 32, 14]},
            ],
            "hint": "import zlib; zlib.crc32(key.encode()) % n — номер шарда.",
        },
        {
            "id": "shard-range",
            "mode": "func",
            "func": "range_shards",
            "title": "Шардирование по диапазонам",
            "statement": (
                "Напишите функцию range_shards(boundaries, keys): boundaries — "
                "отсортированные граничные значения b0 < b1 < …; шард 0 — ключи < "
                "b0, шард i — b(i-1) ≤ ключ < bi, последний шард — ключи ≥ "
                "последней границы. Верните список номеров шардов для keys (в том "
                "же порядке). Используйте бинарный поиск."
            ),
            "starter": "import bisect\n\n\ndef range_shards(boundaries, keys):\n    pass\n",
            "tests": [
                {"args": [[100, 200, 300], [5, 100, 150, 299, 300, 999]], "expected": [0, 1, 1, 2, 3, 3]},
                {"args": [[], [1, 2]], "expected": [0, 0]},
                {"args": [[10], [9, 10, 11]], "expected": [0, 1, 1]},
                {"args": [["g", "p"], ["a", "g", "m", "p", "z"]], "expected": [0, 1, 1, 2, 2]},
                {"args": [[5], []], "expected": []},
            ],
            "hint": "bisect.bisect_right(boundaries, key) даёт нужный номер: граница принадлежит правому шарду.",
        },
        {
            "id": "shard-moved",
            "mode": "func",
            "func": "moved_keys",
            "title": "Перераспределение при добавлении шарда",
            "statement": (
                "При хеш-шардировании «ключ mod N» добавление шарда перемещает "
                "почти все ключи. Напишите функцию moved_keys(keys, n_old, n_new): "
                "шард = zlib.crc32(ключ.encode()) mod N. Верните, сколько ключей "
                "меняют шард при переходе с n_old на n_new."
            ),
            "starter": "import zlib\n\n\ndef moved_keys(keys, n_old, n_new):\n    pass\n",
            "tests": [
                {"args": [["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11", "user12", "user13", "user14", "user15", "user16", "user17", "user18", "user19", "user20", "user21", "user22", "user23", "user24", "user25", "user26", "user27", "user28", "user29", "user30", "user31", "user32", "user33", "user34", "user35", "user36", "user37", "user38", "user39", "user40", "user41", "user42", "user43", "user44", "user45", "user46", "user47", "user48", "user49", "user50", "user51", "user52", "user53", "user54", "user55", "user56", "user57", "user58", "user59", "user60", "user61", "user62", "user63", "user64", "user65", "user66", "user67", "user68", "user69", "user70", "user71", "user72", "user73", "user74", "user75", "user76", "user77", "user78", "user79", "user80", "user81", "user82", "user83", "user84", "user85", "user86", "user87", "user88", "user89", "user90", "user91", "user92", "user93", "user94", "user95", "user96", "user97", "user98", "user99", "user100", "user101", "user102", "user103", "user104", "user105", "user106", "user107", "user108", "user109", "user110", "user111", "user112", "user113", "user114", "user115", "user116", "user117", "user118", "user119", "user120", "user121", "user122", "user123", "user124", "user125", "user126", "user127", "user128", "user129", "user130", "user131", "user132", "user133", "user134", "user135", "user136", "user137", "user138", "user139", "user140", "user141", "user142", "user143", "user144", "user145", "user146", "user147", "user148", "user149", "user150", "user151", "user152", "user153", "user154", "user155", "user156", "user157", "user158", "user159", "user160", "user161", "user162", "user163", "user164", "user165", "user166", "user167", "user168", "user169", "user170", "user171", "user172", "user173", "user174", "user175", "user176", "user177", "user178", "user179", "user180", "user181", "user182", "user183", "user184", "user185", "user186", "user187", "user188", "user189", "user190", "user191", "user192", "user193", "user194", "user195", "user196", "user197", "user198", "user199", "user200", "user201", "user202", "user203", "user204", "user205", "user206", "user207", "user208", "user209", "user210", "user211", "user212", "user213", "user214", "user215", "user216", "user217", "user218", "user219", "user220", "user221", "user222", "user223", "user224", "user225", "user226", "user227", "user228", "user229", "user230", "user231", "user232", "user233", "user234", "user235", "user236", "user237", "user238", "user239", "user240", "user241", "user242", "user243", "user244", "user245", "user246", "user247", "user248", "user249", "user250", "user251", "user252", "user253", "user254", "user255", "user256", "user257", "user258", "user259", "user260", "user261", "user262", "user263", "user264", "user265", "user266", "user267", "user268", "user269", "user270", "user271", "user272", "user273", "user274", "user275", "user276", "user277", "user278", "user279", "user280", "user281", "user282", "user283", "user284", "user285", "user286", "user287", "user288", "user289", "user290", "user291", "user292", "user293", "user294", "user295", "user296", "user297", "user298", "user299", "user300", "user301", "user302", "user303", "user304", "user305", "user306", "user307", "user308", "user309", "user310", "user311", "user312", "user313", "user314", "user315", "user316", "user317", "user318", "user319", "user320", "user321", "user322", "user323", "user324", "user325", "user326", "user327", "user328", "user329", "user330", "user331", "user332", "user333", "user334", "user335", "user336", "user337", "user338", "user339", "user340", "user341", "user342", "user343", "user344", "user345", "user346", "user347", "user348", "user349", "user350", "user351", "user352", "user353", "user354", "user355", "user356", "user357", "user358", "user359", "user360", "user361", "user362", "user363", "user364", "user365", "user366", "user367", "user368", "user369", "user370", "user371", "user372", "user373", "user374", "user375", "user376", "user377", "user378", "user379", "user380", "user381", "user382", "user383", "user384", "user385", "user386", "user387", "user388", "user389", "user390", "user391", "user392", "user393", "user394", "user395", "user396", "user397", "user398", "user399", "user400", "user401", "user402", "user403", "user404", "user405", "user406", "user407", "user408", "user409", "user410", "user411", "user412", "user413", "user414", "user415", "user416", "user417", "user418", "user419", "user420", "user421", "user422", "user423", "user424", "user425", "user426", "user427", "user428", "user429", "user430", "user431", "user432", "user433", "user434", "user435", "user436", "user437", "user438", "user439", "user440", "user441", "user442", "user443", "user444", "user445", "user446", "user447", "user448", "user449", "user450", "user451", "user452", "user453", "user454", "user455", "user456", "user457", "user458", "user459", "user460", "user461", "user462", "user463", "user464", "user465", "user466", "user467", "user468", "user469", "user470", "user471", "user472", "user473", "user474", "user475", "user476", "user477", "user478", "user479", "user480", "user481", "user482", "user483", "user484", "user485", "user486", "user487", "user488", "user489", "user490", "user491", "user492", "user493", "user494", "user495", "user496", "user497", "user498", "user499", "user500", "user501", "user502", "user503", "user504", "user505", "user506", "user507", "user508", "user509", "user510", "user511", "user512", "user513", "user514", "user515", "user516", "user517", "user518", "user519", "user520", "user521", "user522", "user523", "user524", "user525", "user526", "user527", "user528", "user529", "user530", "user531", "user532", "user533", "user534", "user535", "user536", "user537", "user538", "user539", "user540", "user541", "user542", "user543", "user544", "user545", "user546", "user547", "user548", "user549", "user550", "user551", "user552", "user553", "user554", "user555", "user556", "user557", "user558", "user559", "user560", "user561", "user562", "user563", "user564", "user565", "user566", "user567", "user568", "user569", "user570", "user571", "user572", "user573", "user574", "user575", "user576", "user577", "user578", "user579", "user580", "user581", "user582", "user583", "user584", "user585", "user586", "user587", "user588", "user589", "user590", "user591", "user592", "user593", "user594", "user595", "user596", "user597", "user598", "user599", "user600", "user601", "user602", "user603", "user604", "user605", "user606", "user607", "user608", "user609", "user610", "user611", "user612", "user613", "user614", "user615", "user616", "user617", "user618", "user619", "user620", "user621", "user622", "user623", "user624", "user625", "user626", "user627", "user628", "user629", "user630", "user631", "user632", "user633", "user634", "user635", "user636", "user637", "user638", "user639", "user640", "user641", "user642", "user643", "user644", "user645", "user646", "user647", "user648", "user649", "user650", "user651", "user652", "user653", "user654", "user655", "user656", "user657", "user658", "user659", "user660", "user661", "user662", "user663", "user664", "user665", "user666", "user667", "user668", "user669", "user670", "user671", "user672", "user673", "user674", "user675", "user676", "user677", "user678", "user679", "user680", "user681", "user682", "user683", "user684", "user685", "user686", "user687", "user688", "user689", "user690", "user691", "user692", "user693", "user694", "user695", "user696", "user697", "user698", "user699", "user700", "user701", "user702", "user703", "user704", "user705", "user706", "user707", "user708", "user709", "user710", "user711", "user712", "user713", "user714", "user715", "user716", "user717", "user718", "user719", "user720", "user721", "user722", "user723", "user724", "user725", "user726", "user727", "user728", "user729", "user730", "user731", "user732", "user733", "user734", "user735", "user736", "user737", "user738", "user739", "user740", "user741", "user742", "user743", "user744", "user745", "user746", "user747", "user748", "user749", "user750", "user751", "user752", "user753", "user754", "user755", "user756", "user757", "user758", "user759", "user760", "user761", "user762", "user763", "user764", "user765", "user766", "user767", "user768", "user769", "user770", "user771", "user772", "user773", "user774", "user775", "user776", "user777", "user778", "user779", "user780", "user781", "user782", "user783", "user784", "user785", "user786", "user787", "user788", "user789", "user790", "user791", "user792", "user793", "user794", "user795", "user796", "user797", "user798", "user799", "user800", "user801", "user802", "user803", "user804", "user805", "user806", "user807", "user808", "user809", "user810", "user811", "user812", "user813", "user814", "user815", "user816", "user817", "user818", "user819", "user820", "user821", "user822", "user823", "user824", "user825", "user826", "user827", "user828", "user829", "user830", "user831", "user832", "user833", "user834", "user835", "user836", "user837", "user838", "user839", "user840", "user841", "user842", "user843", "user844", "user845", "user846", "user847", "user848", "user849", "user850", "user851", "user852", "user853", "user854", "user855", "user856", "user857", "user858", "user859", "user860", "user861", "user862", "user863", "user864", "user865", "user866", "user867", "user868", "user869", "user870", "user871", "user872", "user873", "user874", "user875", "user876", "user877", "user878", "user879", "user880", "user881", "user882", "user883", "user884", "user885", "user886", "user887", "user888", "user889", "user890", "user891", "user892", "user893", "user894", "user895", "user896", "user897", "user898", "user899", "user900", "user901", "user902", "user903", "user904", "user905", "user906", "user907", "user908", "user909", "user910", "user911", "user912", "user913", "user914", "user915", "user916", "user917", "user918", "user919", "user920", "user921", "user922", "user923", "user924", "user925", "user926", "user927", "user928", "user929", "user930", "user931", "user932", "user933", "user934", "user935", "user936", "user937", "user938", "user939", "user940", "user941", "user942", "user943", "user944", "user945", "user946", "user947", "user948", "user949", "user950", "user951", "user952", "user953", "user954", "user955", "user956", "user957", "user958", "user959", "user960", "user961", "user962", "user963", "user964", "user965", "user966", "user967", "user968", "user969", "user970", "user971", "user972", "user973", "user974", "user975", "user976", "user977", "user978", "user979", "user980", "user981", "user982", "user983", "user984", "user985", "user986", "user987", "user988", "user989", "user990", "user991", "user992", "user993", "user994", "user995", "user996", "user997", "user998", "user999"], 4, 5], "expected": 801},
                {"args": [["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11", "user12", "user13", "user14", "user15", "user16", "user17", "user18", "user19", "user20", "user21", "user22", "user23", "user24", "user25", "user26", "user27", "user28", "user29", "user30", "user31", "user32", "user33", "user34", "user35", "user36", "user37", "user38", "user39", "user40", "user41", "user42", "user43", "user44", "user45", "user46", "user47", "user48", "user49", "user50", "user51", "user52", "user53", "user54", "user55", "user56", "user57", "user58", "user59", "user60", "user61", "user62", "user63", "user64", "user65", "user66", "user67", "user68", "user69", "user70", "user71", "user72", "user73", "user74", "user75", "user76", "user77", "user78", "user79", "user80", "user81", "user82", "user83", "user84", "user85", "user86", "user87", "user88", "user89", "user90", "user91", "user92", "user93", "user94", "user95", "user96", "user97", "user98", "user99", "user100", "user101", "user102", "user103", "user104", "user105", "user106", "user107", "user108", "user109", "user110", "user111", "user112", "user113", "user114", "user115", "user116", "user117", "user118", "user119", "user120", "user121", "user122", "user123", "user124", "user125", "user126", "user127", "user128", "user129", "user130", "user131", "user132", "user133", "user134", "user135", "user136", "user137", "user138", "user139", "user140", "user141", "user142", "user143", "user144", "user145", "user146", "user147", "user148", "user149", "user150", "user151", "user152", "user153", "user154", "user155", "user156", "user157", "user158", "user159", "user160", "user161", "user162", "user163", "user164", "user165", "user166", "user167", "user168", "user169", "user170", "user171", "user172", "user173", "user174", "user175", "user176", "user177", "user178", "user179", "user180", "user181", "user182", "user183", "user184", "user185", "user186", "user187", "user188", "user189", "user190", "user191", "user192", "user193", "user194", "user195", "user196", "user197", "user198", "user199", "user200", "user201", "user202", "user203", "user204", "user205", "user206", "user207", "user208", "user209", "user210", "user211", "user212", "user213", "user214", "user215", "user216", "user217", "user218", "user219", "user220", "user221", "user222", "user223", "user224", "user225", "user226", "user227", "user228", "user229", "user230", "user231", "user232", "user233", "user234", "user235", "user236", "user237", "user238", "user239", "user240", "user241", "user242", "user243", "user244", "user245", "user246", "user247", "user248", "user249", "user250", "user251", "user252", "user253", "user254", "user255", "user256", "user257", "user258", "user259", "user260", "user261", "user262", "user263", "user264", "user265", "user266", "user267", "user268", "user269", "user270", "user271", "user272", "user273", "user274", "user275", "user276", "user277", "user278", "user279", "user280", "user281", "user282", "user283", "user284", "user285", "user286", "user287", "user288", "user289", "user290", "user291", "user292", "user293", "user294", "user295", "user296", "user297", "user298", "user299", "user300", "user301", "user302", "user303", "user304", "user305", "user306", "user307", "user308", "user309", "user310", "user311", "user312", "user313", "user314", "user315", "user316", "user317", "user318", "user319", "user320", "user321", "user322", "user323", "user324", "user325", "user326", "user327", "user328", "user329", "user330", "user331", "user332", "user333", "user334", "user335", "user336", "user337", "user338", "user339", "user340", "user341", "user342", "user343", "user344", "user345", "user346", "user347", "user348", "user349", "user350", "user351", "user352", "user353", "user354", "user355", "user356", "user357", "user358", "user359", "user360", "user361", "user362", "user363", "user364", "user365", "user366", "user367", "user368", "user369", "user370", "user371", "user372", "user373", "user374", "user375", "user376", "user377", "user378", "user379", "user380", "user381", "user382", "user383", "user384", "user385", "user386", "user387", "user388", "user389", "user390", "user391", "user392", "user393", "user394", "user395", "user396", "user397", "user398", "user399", "user400", "user401", "user402", "user403", "user404", "user405", "user406", "user407", "user408", "user409", "user410", "user411", "user412", "user413", "user414", "user415", "user416", "user417", "user418", "user419", "user420", "user421", "user422", "user423", "user424", "user425", "user426", "user427", "user428", "user429", "user430", "user431", "user432", "user433", "user434", "user435", "user436", "user437", "user438", "user439", "user440", "user441", "user442", "user443", "user444", "user445", "user446", "user447", "user448", "user449", "user450", "user451", "user452", "user453", "user454", "user455", "user456", "user457", "user458", "user459", "user460", "user461", "user462", "user463", "user464", "user465", "user466", "user467", "user468", "user469", "user470", "user471", "user472", "user473", "user474", "user475", "user476", "user477", "user478", "user479", "user480", "user481", "user482", "user483", "user484", "user485", "user486", "user487", "user488", "user489", "user490", "user491", "user492", "user493", "user494", "user495", "user496", "user497", "user498", "user499", "user500", "user501", "user502", "user503", "user504", "user505", "user506", "user507", "user508", "user509", "user510", "user511", "user512", "user513", "user514", "user515", "user516", "user517", "user518", "user519", "user520", "user521", "user522", "user523", "user524", "user525", "user526", "user527", "user528", "user529", "user530", "user531", "user532", "user533", "user534", "user535", "user536", "user537", "user538", "user539", "user540", "user541", "user542", "user543", "user544", "user545", "user546", "user547", "user548", "user549", "user550", "user551", "user552", "user553", "user554", "user555", "user556", "user557", "user558", "user559", "user560", "user561", "user562", "user563", "user564", "user565", "user566", "user567", "user568", "user569", "user570", "user571", "user572", "user573", "user574", "user575", "user576", "user577", "user578", "user579", "user580", "user581", "user582", "user583", "user584", "user585", "user586", "user587", "user588", "user589", "user590", "user591", "user592", "user593", "user594", "user595", "user596", "user597", "user598", "user599", "user600", "user601", "user602", "user603", "user604", "user605", "user606", "user607", "user608", "user609", "user610", "user611", "user612", "user613", "user614", "user615", "user616", "user617", "user618", "user619", "user620", "user621", "user622", "user623", "user624", "user625", "user626", "user627", "user628", "user629", "user630", "user631", "user632", "user633", "user634", "user635", "user636", "user637", "user638", "user639", "user640", "user641", "user642", "user643", "user644", "user645", "user646", "user647", "user648", "user649", "user650", "user651", "user652", "user653", "user654", "user655", "user656", "user657", "user658", "user659", "user660", "user661", "user662", "user663", "user664", "user665", "user666", "user667", "user668", "user669", "user670", "user671", "user672", "user673", "user674", "user675", "user676", "user677", "user678", "user679", "user680", "user681", "user682", "user683", "user684", "user685", "user686", "user687", "user688", "user689", "user690", "user691", "user692", "user693", "user694", "user695", "user696", "user697", "user698", "user699", "user700", "user701", "user702", "user703", "user704", "user705", "user706", "user707", "user708", "user709", "user710", "user711", "user712", "user713", "user714", "user715", "user716", "user717", "user718", "user719", "user720", "user721", "user722", "user723", "user724", "user725", "user726", "user727", "user728", "user729", "user730", "user731", "user732", "user733", "user734", "user735", "user736", "user737", "user738", "user739", "user740", "user741", "user742", "user743", "user744", "user745", "user746", "user747", "user748", "user749", "user750", "user751", "user752", "user753", "user754", "user755", "user756", "user757", "user758", "user759", "user760", "user761", "user762", "user763", "user764", "user765", "user766", "user767", "user768", "user769", "user770", "user771", "user772", "user773", "user774", "user775", "user776", "user777", "user778", "user779", "user780", "user781", "user782", "user783", "user784", "user785", "user786", "user787", "user788", "user789", "user790", "user791", "user792", "user793", "user794", "user795", "user796", "user797", "user798", "user799", "user800", "user801", "user802", "user803", "user804", "user805", "user806", "user807", "user808", "user809", "user810", "user811", "user812", "user813", "user814", "user815", "user816", "user817", "user818", "user819", "user820", "user821", "user822", "user823", "user824", "user825", "user826", "user827", "user828", "user829", "user830", "user831", "user832", "user833", "user834", "user835", "user836", "user837", "user838", "user839", "user840", "user841", "user842", "user843", "user844", "user845", "user846", "user847", "user848", "user849", "user850", "user851", "user852", "user853", "user854", "user855", "user856", "user857", "user858", "user859", "user860", "user861", "user862", "user863", "user864", "user865", "user866", "user867", "user868", "user869", "user870", "user871", "user872", "user873", "user874", "user875", "user876", "user877", "user878", "user879", "user880", "user881", "user882", "user883", "user884", "user885", "user886", "user887", "user888", "user889", "user890", "user891", "user892", "user893", "user894", "user895", "user896", "user897", "user898", "user899", "user900", "user901", "user902", "user903", "user904", "user905", "user906", "user907", "user908", "user909", "user910", "user911", "user912", "user913", "user914", "user915", "user916", "user917", "user918", "user919", "user920", "user921", "user922", "user923", "user924", "user925", "user926", "user927", "user928", "user929", "user930", "user931", "user932", "user933", "user934", "user935", "user936", "user937", "user938", "user939", "user940", "user941", "user942", "user943", "user944", "user945", "user946", "user947", "user948", "user949", "user950", "user951", "user952", "user953", "user954", "user955", "user956", "user957", "user958", "user959", "user960", "user961", "user962", "user963", "user964", "user965", "user966", "user967", "user968", "user969", "user970", "user971", "user972", "user973", "user974", "user975", "user976", "user977", "user978", "user979", "user980", "user981", "user982", "user983", "user984", "user985", "user986", "user987", "user988", "user989", "user990", "user991", "user992", "user993", "user994", "user995", "user996", "user997", "user998", "user999"], 4, 4], "expected": 0},
                {"args": [["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11", "user12", "user13", "user14", "user15", "user16", "user17", "user18", "user19", "user20", "user21", "user22", "user23", "user24", "user25", "user26", "user27", "user28", "user29", "user30", "user31", "user32", "user33", "user34", "user35", "user36", "user37", "user38", "user39", "user40", "user41", "user42", "user43", "user44", "user45", "user46", "user47", "user48", "user49", "user50", "user51", "user52", "user53", "user54", "user55", "user56", "user57", "user58", "user59", "user60", "user61", "user62", "user63", "user64", "user65", "user66", "user67", "user68", "user69", "user70", "user71", "user72", "user73", "user74", "user75", "user76", "user77", "user78", "user79", "user80", "user81", "user82", "user83", "user84", "user85", "user86", "user87", "user88", "user89", "user90", "user91", "user92", "user93", "user94", "user95", "user96", "user97", "user98", "user99", "user100", "user101", "user102", "user103", "user104", "user105", "user106", "user107", "user108", "user109", "user110", "user111", "user112", "user113", "user114", "user115", "user116", "user117", "user118", "user119", "user120", "user121", "user122", "user123", "user124", "user125", "user126", "user127", "user128", "user129", "user130", "user131", "user132", "user133", "user134", "user135", "user136", "user137", "user138", "user139", "user140", "user141", "user142", "user143", "user144", "user145", "user146", "user147", "user148", "user149", "user150", "user151", "user152", "user153", "user154", "user155", "user156", "user157", "user158", "user159", "user160", "user161", "user162", "user163", "user164", "user165", "user166", "user167", "user168", "user169", "user170", "user171", "user172", "user173", "user174", "user175", "user176", "user177", "user178", "user179", "user180", "user181", "user182", "user183", "user184", "user185", "user186", "user187", "user188", "user189", "user190", "user191", "user192", "user193", "user194", "user195", "user196", "user197", "user198", "user199", "user200", "user201", "user202", "user203", "user204", "user205", "user206", "user207", "user208", "user209", "user210", "user211", "user212", "user213", "user214", "user215", "user216", "user217", "user218", "user219", "user220", "user221", "user222", "user223", "user224", "user225", "user226", "user227", "user228", "user229", "user230", "user231", "user232", "user233", "user234", "user235", "user236", "user237", "user238", "user239", "user240", "user241", "user242", "user243", "user244", "user245", "user246", "user247", "user248", "user249", "user250", "user251", "user252", "user253", "user254", "user255", "user256", "user257", "user258", "user259", "user260", "user261", "user262", "user263", "user264", "user265", "user266", "user267", "user268", "user269", "user270", "user271", "user272", "user273", "user274", "user275", "user276", "user277", "user278", "user279", "user280", "user281", "user282", "user283", "user284", "user285", "user286", "user287", "user288", "user289", "user290", "user291", "user292", "user293", "user294", "user295", "user296", "user297", "user298", "user299", "user300", "user301", "user302", "user303", "user304", "user305", "user306", "user307", "user308", "user309", "user310", "user311", "user312", "user313", "user314", "user315", "user316", "user317", "user318", "user319", "user320", "user321", "user322", "user323", "user324", "user325", "user326", "user327", "user328", "user329", "user330", "user331", "user332", "user333", "user334", "user335", "user336", "user337", "user338", "user339", "user340", "user341", "user342", "user343", "user344", "user345", "user346", "user347", "user348", "user349", "user350", "user351", "user352", "user353", "user354", "user355", "user356", "user357", "user358", "user359", "user360", "user361", "user362", "user363", "user364", "user365", "user366", "user367", "user368", "user369", "user370", "user371", "user372", "user373", "user374", "user375", "user376", "user377", "user378", "user379", "user380", "user381", "user382", "user383", "user384", "user385", "user386", "user387", "user388", "user389", "user390", "user391", "user392", "user393", "user394", "user395", "user396", "user397", "user398", "user399", "user400", "user401", "user402", "user403", "user404", "user405", "user406", "user407", "user408", "user409", "user410", "user411", "user412", "user413", "user414", "user415", "user416", "user417", "user418", "user419", "user420", "user421", "user422", "user423", "user424", "user425", "user426", "user427", "user428", "user429", "user430", "user431", "user432", "user433", "user434", "user435", "user436", "user437", "user438", "user439", "user440", "user441", "user442", "user443", "user444", "user445", "user446", "user447", "user448", "user449", "user450", "user451", "user452", "user453", "user454", "user455", "user456", "user457", "user458", "user459", "user460", "user461", "user462", "user463", "user464", "user465", "user466", "user467", "user468", "user469", "user470", "user471", "user472", "user473", "user474", "user475", "user476", "user477", "user478", "user479", "user480", "user481", "user482", "user483", "user484", "user485", "user486", "user487", "user488", "user489", "user490", "user491", "user492", "user493", "user494", "user495", "user496", "user497", "user498", "user499", "user500", "user501", "user502", "user503", "user504", "user505", "user506", "user507", "user508", "user509", "user510", "user511", "user512", "user513", "user514", "user515", "user516", "user517", "user518", "user519", "user520", "user521", "user522", "user523", "user524", "user525", "user526", "user527", "user528", "user529", "user530", "user531", "user532", "user533", "user534", "user535", "user536", "user537", "user538", "user539", "user540", "user541", "user542", "user543", "user544", "user545", "user546", "user547", "user548", "user549", "user550", "user551", "user552", "user553", "user554", "user555", "user556", "user557", "user558", "user559", "user560", "user561", "user562", "user563", "user564", "user565", "user566", "user567", "user568", "user569", "user570", "user571", "user572", "user573", "user574", "user575", "user576", "user577", "user578", "user579", "user580", "user581", "user582", "user583", "user584", "user585", "user586", "user587", "user588", "user589", "user590", "user591", "user592", "user593", "user594", "user595", "user596", "user597", "user598", "user599", "user600", "user601", "user602", "user603", "user604", "user605", "user606", "user607", "user608", "user609", "user610", "user611", "user612", "user613", "user614", "user615", "user616", "user617", "user618", "user619", "user620", "user621", "user622", "user623", "user624", "user625", "user626", "user627", "user628", "user629", "user630", "user631", "user632", "user633", "user634", "user635", "user636", "user637", "user638", "user639", "user640", "user641", "user642", "user643", "user644", "user645", "user646", "user647", "user648", "user649", "user650", "user651", "user652", "user653", "user654", "user655", "user656", "user657", "user658", "user659", "user660", "user661", "user662", "user663", "user664", "user665", "user666", "user667", "user668", "user669", "user670", "user671", "user672", "user673", "user674", "user675", "user676", "user677", "user678", "user679", "user680", "user681", "user682", "user683", "user684", "user685", "user686", "user687", "user688", "user689", "user690", "user691", "user692", "user693", "user694", "user695", "user696", "user697", "user698", "user699", "user700", "user701", "user702", "user703", "user704", "user705", "user706", "user707", "user708", "user709", "user710", "user711", "user712", "user713", "user714", "user715", "user716", "user717", "user718", "user719", "user720", "user721", "user722", "user723", "user724", "user725", "user726", "user727", "user728", "user729", "user730", "user731", "user732", "user733", "user734", "user735", "user736", "user737", "user738", "user739", "user740", "user741", "user742", "user743", "user744", "user745", "user746", "user747", "user748", "user749", "user750", "user751", "user752", "user753", "user754", "user755", "user756", "user757", "user758", "user759", "user760", "user761", "user762", "user763", "user764", "user765", "user766", "user767", "user768", "user769", "user770", "user771", "user772", "user773", "user774", "user775", "user776", "user777", "user778", "user779", "user780", "user781", "user782", "user783", "user784", "user785", "user786", "user787", "user788", "user789", "user790", "user791", "user792", "user793", "user794", "user795", "user796", "user797", "user798", "user799", "user800", "user801", "user802", "user803", "user804", "user805", "user806", "user807", "user808", "user809", "user810", "user811", "user812", "user813", "user814", "user815", "user816", "user817", "user818", "user819", "user820", "user821", "user822", "user823", "user824", "user825", "user826", "user827", "user828", "user829", "user830", "user831", "user832", "user833", "user834", "user835", "user836", "user837", "user838", "user839", "user840", "user841", "user842", "user843", "user844", "user845", "user846", "user847", "user848", "user849", "user850", "user851", "user852", "user853", "user854", "user855", "user856", "user857", "user858", "user859", "user860", "user861", "user862", "user863", "user864", "user865", "user866", "user867", "user868", "user869", "user870", "user871", "user872", "user873", "user874", "user875", "user876", "user877", "user878", "user879", "user880", "user881", "user882", "user883", "user884", "user885", "user886", "user887", "user888", "user889", "user890", "user891", "user892", "user893", "user894", "user895", "user896", "user897", "user898", "user899", "user900", "user901", "user902", "user903", "user904", "user905", "user906", "user907", "user908", "user909", "user910", "user911", "user912", "user913", "user914", "user915", "user916", "user917", "user918", "user919", "user920", "user921", "user922", "user923", "user924", "user925", "user926", "user927", "user928", "user929", "user930", "user931", "user932", "user933", "user934", "user935", "user936", "user937", "user938", "user939", "user940", "user941", "user942", "user943", "user944", "user945", "user946", "user947", "user948", "user949", "user950", "user951", "user952", "user953", "user954", "user955", "user956", "user957", "user958", "user959", "user960", "user961", "user962", "user963", "user964", "user965", "user966", "user967", "user968", "user969", "user970", "user971", "user972", "user973", "user974", "user975", "user976", "user977", "user978", "user979", "user980", "user981", "user982", "user983", "user984", "user985", "user986", "user987", "user988", "user989", "user990", "user991", "user992", "user993", "user994", "user995", "user996", "user997", "user998", "user999"], 4, 8], "expected": 500},
                {"args": [[], 3, 4], "expected": 0},
                {"args": [["a", "b", "c"], 1, 2], "expected": 3},
            ],
            "hint": "Сравните два остатка от деления одного и того же crc32.",
        },
        {
            "id": "shard-ring",
            "mode": "func",
            "func": "ring_lookup",
            "title": "Консистентное хеширование",
            "statement": (
                "Напишите функцию ring_lookup(nodes, vnodes, keys): у каждого узла "
                "vnodes виртуальных точек на кольце; позиция точки — "
                "int(md5(f'{узел}#{i}').hexdigest(), 16) для i = 0…vnodes−1; "
                "позиция ключа — int(md5(ключ).hexdigest(), 16). Ключ принадлежит "
                "узлу первой точки кольца с позицией ≥ позиции ключа (по кругу — "
                "если таких нет, берётся самая первая точка). Верните список узлов "
                "для keys."
            ),
            "starter": "import bisect\nimport hashlib\n\n\ndef ring_lookup(nodes, vnodes, keys):\n    pass\n",
            "tests": [
                {"args": [["a", "b", "c"], 10, ["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11"]], "expected": ["a", "c", "b", "c", "a", "c", "c", "a", "b", "a", "c", "c"]},
                {"args": [["solo"], 3, ["x", "y"]], "expected": ["solo", "solo"]},
                {"args": [["a", "b"], 1, ["k1", "k2", "k3", "k4"]], "expected": ["a", "a", "b", "a"]},
                {"args": [["n1", "n2", "n3", "n4"], 50, ["key0", "key1", "key2", "key3", "key4", "key5", "key6", "key7"]], "expected": ["n1", "n2", "n2", "n3", "n3", "n2", "n3", "n3"]},
                {"args": [["a", "b", "c"], 10, []], "expected": []},
            ],
            "hint": "Отсортируйте точки (позиция, узел); для ключа — bisect_left по позициям и взятие по модулю длины кольца.",
        },
        {
            "id": "shard-ring-moved",
            "mode": "func",
            "func": "ring_moved",
            "title": "Сколько ключей переедет в кольце",
            "statement": (
                "Напишите функцию ring_moved(keys, nodes_before, nodes_after, "
                "vnodes): постройте кольцо (как в задаче про ring_lookup: md5, "
                "vnodes точек на узел) до и после изменения набора узлов и верните, "
                "сколько ключей сменило владельца."
            ),
            "starter": "import bisect\nimport hashlib\n\n\ndef ring_moved(keys, nodes_before, nodes_after, vnodes):\n    pass\n",
            "tests": [
                {"args": [["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11", "user12", "user13", "user14", "user15", "user16", "user17", "user18", "user19", "user20", "user21", "user22", "user23", "user24", "user25", "user26", "user27", "user28", "user29", "user30", "user31", "user32", "user33", "user34", "user35", "user36", "user37", "user38", "user39", "user40", "user41", "user42", "user43", "user44", "user45", "user46", "user47", "user48", "user49", "user50", "user51", "user52", "user53", "user54", "user55", "user56", "user57", "user58", "user59", "user60", "user61", "user62", "user63", "user64", "user65", "user66", "user67", "user68", "user69", "user70", "user71", "user72", "user73", "user74", "user75", "user76", "user77", "user78", "user79", "user80", "user81", "user82", "user83", "user84", "user85", "user86", "user87", "user88", "user89", "user90", "user91", "user92", "user93", "user94", "user95", "user96", "user97", "user98", "user99", "user100", "user101", "user102", "user103", "user104", "user105", "user106", "user107", "user108", "user109", "user110", "user111", "user112", "user113", "user114", "user115", "user116", "user117", "user118", "user119", "user120", "user121", "user122", "user123", "user124", "user125", "user126", "user127", "user128", "user129", "user130", "user131", "user132", "user133", "user134", "user135", "user136", "user137", "user138", "user139", "user140", "user141", "user142", "user143", "user144", "user145", "user146", "user147", "user148", "user149", "user150", "user151", "user152", "user153", "user154", "user155", "user156", "user157", "user158", "user159", "user160", "user161", "user162", "user163", "user164", "user165", "user166", "user167", "user168", "user169", "user170", "user171", "user172", "user173", "user174", "user175", "user176", "user177", "user178", "user179", "user180", "user181", "user182", "user183", "user184", "user185", "user186", "user187", "user188", "user189", "user190", "user191", "user192", "user193", "user194", "user195", "user196", "user197", "user198", "user199", "user200", "user201", "user202", "user203", "user204", "user205", "user206", "user207", "user208", "user209", "user210", "user211", "user212", "user213", "user214", "user215", "user216", "user217", "user218", "user219", "user220", "user221", "user222", "user223", "user224", "user225", "user226", "user227", "user228", "user229", "user230", "user231", "user232", "user233", "user234", "user235", "user236", "user237", "user238", "user239", "user240", "user241", "user242", "user243", "user244", "user245", "user246", "user247", "user248", "user249", "user250", "user251", "user252", "user253", "user254", "user255", "user256", "user257", "user258", "user259", "user260", "user261", "user262", "user263", "user264", "user265", "user266", "user267", "user268", "user269", "user270", "user271", "user272", "user273", "user274", "user275", "user276", "user277", "user278", "user279", "user280", "user281", "user282", "user283", "user284", "user285", "user286", "user287", "user288", "user289", "user290", "user291", "user292", "user293", "user294", "user295", "user296", "user297", "user298", "user299", "user300", "user301", "user302", "user303", "user304", "user305", "user306", "user307", "user308", "user309", "user310", "user311", "user312", "user313", "user314", "user315", "user316", "user317", "user318", "user319", "user320", "user321", "user322", "user323", "user324", "user325", "user326", "user327", "user328", "user329", "user330", "user331", "user332", "user333", "user334", "user335", "user336", "user337", "user338", "user339", "user340", "user341", "user342", "user343", "user344", "user345", "user346", "user347", "user348", "user349", "user350", "user351", "user352", "user353", "user354", "user355", "user356", "user357", "user358", "user359", "user360", "user361", "user362", "user363", "user364", "user365", "user366", "user367", "user368", "user369", "user370", "user371", "user372", "user373", "user374", "user375", "user376", "user377", "user378", "user379", "user380", "user381", "user382", "user383", "user384", "user385", "user386", "user387", "user388", "user389", "user390", "user391", "user392", "user393", "user394", "user395", "user396", "user397", "user398", "user399", "user400", "user401", "user402", "user403", "user404", "user405", "user406", "user407", "user408", "user409", "user410", "user411", "user412", "user413", "user414", "user415", "user416", "user417", "user418", "user419", "user420", "user421", "user422", "user423", "user424", "user425", "user426", "user427", "user428", "user429", "user430", "user431", "user432", "user433", "user434", "user435", "user436", "user437", "user438", "user439", "user440", "user441", "user442", "user443", "user444", "user445", "user446", "user447", "user448", "user449", "user450", "user451", "user452", "user453", "user454", "user455", "user456", "user457", "user458", "user459", "user460", "user461", "user462", "user463", "user464", "user465", "user466", "user467", "user468", "user469", "user470", "user471", "user472", "user473", "user474", "user475", "user476", "user477", "user478", "user479", "user480", "user481", "user482", "user483", "user484", "user485", "user486", "user487", "user488", "user489", "user490", "user491", "user492", "user493", "user494", "user495", "user496", "user497", "user498", "user499", "user500", "user501", "user502", "user503", "user504", "user505", "user506", "user507", "user508", "user509", "user510", "user511", "user512", "user513", "user514", "user515", "user516", "user517", "user518", "user519", "user520", "user521", "user522", "user523", "user524", "user525", "user526", "user527", "user528", "user529", "user530", "user531", "user532", "user533", "user534", "user535", "user536", "user537", "user538", "user539", "user540", "user541", "user542", "user543", "user544", "user545", "user546", "user547", "user548", "user549", "user550", "user551", "user552", "user553", "user554", "user555", "user556", "user557", "user558", "user559", "user560", "user561", "user562", "user563", "user564", "user565", "user566", "user567", "user568", "user569", "user570", "user571", "user572", "user573", "user574", "user575", "user576", "user577", "user578", "user579", "user580", "user581", "user582", "user583", "user584", "user585", "user586", "user587", "user588", "user589", "user590", "user591", "user592", "user593", "user594", "user595", "user596", "user597", "user598", "user599", "user600", "user601", "user602", "user603", "user604", "user605", "user606", "user607", "user608", "user609", "user610", "user611", "user612", "user613", "user614", "user615", "user616", "user617", "user618", "user619", "user620", "user621", "user622", "user623", "user624", "user625", "user626", "user627", "user628", "user629", "user630", "user631", "user632", "user633", "user634", "user635", "user636", "user637", "user638", "user639", "user640", "user641", "user642", "user643", "user644", "user645", "user646", "user647", "user648", "user649", "user650", "user651", "user652", "user653", "user654", "user655", "user656", "user657", "user658", "user659", "user660", "user661", "user662", "user663", "user664", "user665", "user666", "user667", "user668", "user669", "user670", "user671", "user672", "user673", "user674", "user675", "user676", "user677", "user678", "user679", "user680", "user681", "user682", "user683", "user684", "user685", "user686", "user687", "user688", "user689", "user690", "user691", "user692", "user693", "user694", "user695", "user696", "user697", "user698", "user699", "user700", "user701", "user702", "user703", "user704", "user705", "user706", "user707", "user708", "user709", "user710", "user711", "user712", "user713", "user714", "user715", "user716", "user717", "user718", "user719", "user720", "user721", "user722", "user723", "user724", "user725", "user726", "user727", "user728", "user729", "user730", "user731", "user732", "user733", "user734", "user735", "user736", "user737", "user738", "user739", "user740", "user741", "user742", "user743", "user744", "user745", "user746", "user747", "user748", "user749", "user750", "user751", "user752", "user753", "user754", "user755", "user756", "user757", "user758", "user759", "user760", "user761", "user762", "user763", "user764", "user765", "user766", "user767", "user768", "user769", "user770", "user771", "user772", "user773", "user774", "user775", "user776", "user777", "user778", "user779", "user780", "user781", "user782", "user783", "user784", "user785", "user786", "user787", "user788", "user789", "user790", "user791", "user792", "user793", "user794", "user795", "user796", "user797", "user798", "user799", "user800", "user801", "user802", "user803", "user804", "user805", "user806", "user807", "user808", "user809", "user810", "user811", "user812", "user813", "user814", "user815", "user816", "user817", "user818", "user819", "user820", "user821", "user822", "user823", "user824", "user825", "user826", "user827", "user828", "user829", "user830", "user831", "user832", "user833", "user834", "user835", "user836", "user837", "user838", "user839", "user840", "user841", "user842", "user843", "user844", "user845", "user846", "user847", "user848", "user849", "user850", "user851", "user852", "user853", "user854", "user855", "user856", "user857", "user858", "user859", "user860", "user861", "user862", "user863", "user864", "user865", "user866", "user867", "user868", "user869", "user870", "user871", "user872", "user873", "user874", "user875", "user876", "user877", "user878", "user879", "user880", "user881", "user882", "user883", "user884", "user885", "user886", "user887", "user888", "user889", "user890", "user891", "user892", "user893", "user894", "user895", "user896", "user897", "user898", "user899", "user900", "user901", "user902", "user903", "user904", "user905", "user906", "user907", "user908", "user909", "user910", "user911", "user912", "user913", "user914", "user915", "user916", "user917", "user918", "user919", "user920", "user921", "user922", "user923", "user924", "user925", "user926", "user927", "user928", "user929", "user930", "user931", "user932", "user933", "user934", "user935", "user936", "user937", "user938", "user939", "user940", "user941", "user942", "user943", "user944", "user945", "user946", "user947", "user948", "user949", "user950", "user951", "user952", "user953", "user954", "user955", "user956", "user957", "user958", "user959", "user960", "user961", "user962", "user963", "user964", "user965", "user966", "user967", "user968", "user969", "user970", "user971", "user972", "user973", "user974", "user975", "user976", "user977", "user978", "user979", "user980", "user981", "user982", "user983", "user984", "user985", "user986", "user987", "user988", "user989", "user990", "user991", "user992", "user993", "user994", "user995", "user996", "user997", "user998", "user999"], ["a", "b", "c", "d"], ["a", "b", "c", "d", "e"], 100], "expected": 231},
                {"args": [["user0", "user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11", "user12", "user13", "user14", "user15", "user16", "user17", "user18", "user19", "user20", "user21", "user22", "user23", "user24", "user25", "user26", "user27", "user28", "user29", "user30", "user31", "user32", "user33", "user34", "user35", "user36", "user37", "user38", "user39", "user40", "user41", "user42", "user43", "user44", "user45", "user46", "user47", "user48", "user49", "user50", "user51", "user52", "user53", "user54", "user55", "user56", "user57", "user58", "user59", "user60", "user61", "user62", "user63", "user64", "user65", "user66", "user67", "user68", "user69", "user70", "user71", "user72", "user73", "user74", "user75", "user76", "user77", "user78", "user79", "user80", "user81", "user82", "user83", "user84", "user85", "user86", "user87", "user88", "user89", "user90", "user91", "user92", "user93", "user94", "user95", "user96", "user97", "user98", "user99", "user100", "user101", "user102", "user103", "user104", "user105", "user106", "user107", "user108", "user109", "user110", "user111", "user112", "user113", "user114", "user115", "user116", "user117", "user118", "user119", "user120", "user121", "user122", "user123", "user124", "user125", "user126", "user127", "user128", "user129", "user130", "user131", "user132", "user133", "user134", "user135", "user136", "user137", "user138", "user139", "user140", "user141", "user142", "user143", "user144", "user145", "user146", "user147", "user148", "user149", "user150", "user151", "user152", "user153", "user154", "user155", "user156", "user157", "user158", "user159", "user160", "user161", "user162", "user163", "user164", "user165", "user166", "user167", "user168", "user169", "user170", "user171", "user172", "user173", "user174", "user175", "user176", "user177", "user178", "user179", "user180", "user181", "user182", "user183", "user184", "user185", "user186", "user187", "user188", "user189", "user190", "user191", "user192", "user193", "user194", "user195", "user196", "user197", "user198", "user199", "user200", "user201", "user202", "user203", "user204", "user205", "user206", "user207", "user208", "user209", "user210", "user211", "user212", "user213", "user214", "user215", "user216", "user217", "user218", "user219", "user220", "user221", "user222", "user223", "user224", "user225", "user226", "user227", "user228", "user229", "user230", "user231", "user232", "user233", "user234", "user235", "user236", "user237", "user238", "user239", "user240", "user241", "user242", "user243", "user244", "user245", "user246", "user247", "user248", "user249", "user250", "user251", "user252", "user253", "user254", "user255", "user256", "user257", "user258", "user259", "user260", "user261", "user262", "user263", "user264", "user265", "user266", "user267", "user268", "user269", "user270", "user271", "user272", "user273", "user274", "user275", "user276", "user277", "user278", "user279", "user280", "user281", "user282", "user283", "user284", "user285", "user286", "user287", "user288", "user289", "user290", "user291", "user292", "user293", "user294", "user295", "user296", "user297", "user298", "user299", "user300", "user301", "user302", "user303", "user304", "user305", "user306", "user307", "user308", "user309", "user310", "user311", "user312", "user313", "user314", "user315", "user316", "user317", "user318", "user319", "user320", "user321", "user322", "user323", "user324", "user325", "user326", "user327", "user328", "user329", "user330", "user331", "user332", "user333", "user334", "user335", "user336", "user337", "user338", "user339", "user340", "user341", "user342", "user343", "user344", "user345", "user346", "user347", "user348", "user349", "user350", "user351", "user352", "user353", "user354", "user355", "user356", "user357", "user358", "user359", "user360", "user361", "user362", "user363", "user364", "user365", "user366", "user367", "user368", "user369", "user370", "user371", "user372", "user373", "user374", "user375", "user376", "user377", "user378", "user379", "user380", "user381", "user382", "user383", "user384", "user385", "user386", "user387", "user388", "user389", "user390", "user391", "user392", "user393", "user394", "user395", "user396", "user397", "user398", "user399", "user400", "user401", "user402", "user403", "user404", "user405", "user406", "user407", "user408", "user409", "user410", "user411", "user412", "user413", "user414", "user415", "user416", "user417", "user418", "user419", "user420", "user421", "user422", "user423", "user424", "user425", "user426", "user427", "user428", "user429", "user430", "user431", "user432", "user433", "user434", "user435", "user436", "user437", "user438", "user439", "user440", "user441", "user442", "user443", "user444", "user445", "user446", "user447", "user448", "user449", "user450", "user451", "user452", "user453", "user454", "user455", "user456", "user457", "user458", "user459", "user460", "user461", "user462", "user463", "user464", "user465", "user466", "user467", "user468", "user469", "user470", "user471", "user472", "user473", "user474", "user475", "user476", "user477", "user478", "user479", "user480", "user481", "user482", "user483", "user484", "user485", "user486", "user487", "user488", "user489", "user490", "user491", "user492", "user493", "user494", "user495", "user496", "user497", "user498", "user499", "user500", "user501", "user502", "user503", "user504", "user505", "user506", "user507", "user508", "user509", "user510", "user511", "user512", "user513", "user514", "user515", "user516", "user517", "user518", "user519", "user520", "user521", "user522", "user523", "user524", "user525", "user526", "user527", "user528", "user529", "user530", "user531", "user532", "user533", "user534", "user535", "user536", "user537", "user538", "user539", "user540", "user541", "user542", "user543", "user544", "user545", "user546", "user547", "user548", "user549", "user550", "user551", "user552", "user553", "user554", "user555", "user556", "user557", "user558", "user559", "user560", "user561", "user562", "user563", "user564", "user565", "user566", "user567", "user568", "user569", "user570", "user571", "user572", "user573", "user574", "user575", "user576", "user577", "user578", "user579", "user580", "user581", "user582", "user583", "user584", "user585", "user586", "user587", "user588", "user589", "user590", "user591", "user592", "user593", "user594", "user595", "user596", "user597", "user598", "user599", "user600", "user601", "user602", "user603", "user604", "user605", "user606", "user607", "user608", "user609", "user610", "user611", "user612", "user613", "user614", "user615", "user616", "user617", "user618", "user619", "user620", "user621", "user622", "user623", "user624", "user625", "user626", "user627", "user628", "user629", "user630", "user631", "user632", "user633", "user634", "user635", "user636", "user637", "user638", "user639", "user640", "user641", "user642", "user643", "user644", "user645", "user646", "user647", "user648", "user649", "user650", "user651", "user652", "user653", "user654", "user655", "user656", "user657", "user658", "user659", "user660", "user661", "user662", "user663", "user664", "user665", "user666", "user667", "user668", "user669", "user670", "user671", "user672", "user673", "user674", "user675", "user676", "user677", "user678", "user679", "user680", "user681", "user682", "user683", "user684", "user685", "user686", "user687", "user688", "user689", "user690", "user691", "user692", "user693", "user694", "user695", "user696", "user697", "user698", "user699", "user700", "user701", "user702", "user703", "user704", "user705", "user706", "user707", "user708", "user709", "user710", "user711", "user712", "user713", "user714", "user715", "user716", "user717", "user718", "user719", "user720", "user721", "user722", "user723", "user724", "user725", "user726", "user727", "user728", "user729", "user730", "user731", "user732", "user733", "user734", "user735", "user736", "user737", "user738", "user739", "user740", "user741", "user742", "user743", "user744", "user745", "user746", "user747", "user748", "user749", "user750", "user751", "user752", "user753", "user754", "user755", "user756", "user757", "user758", "user759", "user760", "user761", "user762", "user763", "user764", "user765", "user766", "user767", "user768", "user769", "user770", "user771", "user772", "user773", "user774", "user775", "user776", "user777", "user778", "user779", "user780", "user781", "user782", "user783", "user784", "user785", "user786", "user787", "user788", "user789", "user790", "user791", "user792", "user793", "user794", "user795", "user796", "user797", "user798", "user799", "user800", "user801", "user802", "user803", "user804", "user805", "user806", "user807", "user808", "user809", "user810", "user811", "user812", "user813", "user814", "user815", "user816", "user817", "user818", "user819", "user820", "user821", "user822", "user823", "user824", "user825", "user826", "user827", "user828", "user829", "user830", "user831", "user832", "user833", "user834", "user835", "user836", "user837", "user838", "user839", "user840", "user841", "user842", "user843", "user844", "user845", "user846", "user847", "user848", "user849", "user850", "user851", "user852", "user853", "user854", "user855", "user856", "user857", "user858", "user859", "user860", "user861", "user862", "user863", "user864", "user865", "user866", "user867", "user868", "user869", "user870", "user871", "user872", "user873", "user874", "user875", "user876", "user877", "user878", "user879", "user880", "user881", "user882", "user883", "user884", "user885", "user886", "user887", "user888", "user889", "user890", "user891", "user892", "user893", "user894", "user895", "user896", "user897", "user898", "user899", "user900", "user901", "user902", "user903", "user904", "user905", "user906", "user907", "user908", "user909", "user910", "user911", "user912", "user913", "user914", "user915", "user916", "user917", "user918", "user919", "user920", "user921", "user922", "user923", "user924", "user925", "user926", "user927", "user928", "user929", "user930", "user931", "user932", "user933", "user934", "user935", "user936", "user937", "user938", "user939", "user940", "user941", "user942", "user943", "user944", "user945", "user946", "user947", "user948", "user949", "user950", "user951", "user952", "user953", "user954", "user955", "user956", "user957", "user958", "user959", "user960", "user961", "user962", "user963", "user964", "user965", "user966", "user967", "user968", "user969", "user970", "user971", "user972", "user973", "user974", "user975", "user976", "user977", "user978", "user979", "user980", "user981", "user982", "user983", "user984", "user985", "user986", "user987", "user988", "user989", "user990", "user991", "user992", "user993", "user994", "user995", "user996", "user997", "user998", "user999"], ["a", "b", "c", "d"], ["a", "b", "c"], 100], "expected": 220},
                {"args": [["k0", "k1", "k2", "k3", "k4", "k5", "k6", "k7", "k8", "k9", "k10", "k11", "k12", "k13", "k14", "k15", "k16", "k17", "k18", "k19", "k20", "k21", "k22", "k23", "k24", "k25", "k26", "k27", "k28", "k29", "k30", "k31", "k32", "k33", "k34", "k35", "k36", "k37", "k38", "k39", "k40", "k41", "k42", "k43", "k44", "k45", "k46", "k47", "k48", "k49", "k50", "k51", "k52", "k53", "k54", "k55", "k56", "k57", "k58", "k59", "k60", "k61", "k62", "k63", "k64", "k65", "k66", "k67", "k68", "k69", "k70", "k71", "k72", "k73", "k74", "k75", "k76", "k77", "k78", "k79", "k80", "k81", "k82", "k83", "k84", "k85", "k86", "k87", "k88", "k89", "k90", "k91", "k92", "k93", "k94", "k95", "k96", "k97", "k98", "k99", "k100", "k101", "k102", "k103", "k104", "k105", "k106", "k107", "k108", "k109", "k110", "k111", "k112", "k113", "k114", "k115", "k116", "k117", "k118", "k119", "k120", "k121", "k122", "k123", "k124", "k125", "k126", "k127", "k128", "k129", "k130", "k131", "k132", "k133", "k134", "k135", "k136", "k137", "k138", "k139", "k140", "k141", "k142", "k143", "k144", "k145", "k146", "k147", "k148", "k149", "k150", "k151", "k152", "k153", "k154", "k155", "k156", "k157", "k158", "k159", "k160", "k161", "k162", "k163", "k164", "k165", "k166", "k167", "k168", "k169", "k170", "k171", "k172", "k173", "k174", "k175", "k176", "k177", "k178", "k179", "k180", "k181", "k182", "k183", "k184", "k185", "k186", "k187", "k188", "k189", "k190", "k191", "k192", "k193", "k194", "k195", "k196", "k197", "k198", "k199"], ["a", "b"], ["a", "b"], 10], "expected": 0},
                {"args": [[], ["a"], ["b"], 1], "expected": 0},
            ],
            "hint": "Один и тот же алгоритм поиска владельца запустите на двух кольцах и сравните ответы.",
        },
        {
            "id": "shard-range-scan",
            "mode": "func",
            "func": "shards_for_range",
            "title": "Какие шарды затрагивает диапазон",
            "statement": (
                "Напишите функцию shards_for_range(boundaries, lo, hi): шарды по "
                "диапазонам (как в задаче range_shards: границы b0 < b1 < …). "
                "Запрос читает ключи от lo до hi включительно (lo ≤ hi). Верните "
                "список номеров затронутых шардов по возрастанию."
            ),
            "starter": "import bisect\n\n\ndef shards_for_range(boundaries, lo, hi):\n    pass\n",
            "tests": [
                {"args": [[100, 200, 300], 50, 150], "expected": [0, 1]},
                {"args": [[100, 200, 300], 100, 100], "expected": [1]},
                {"args": [[100, 200, 300], 0, 999], "expected": [0, 1, 2, 3]},
                {"args": [[100, 200, 300], 201, 299], "expected": [2]},
                {"args": [[], 1, 2], "expected": [0]},
                {"args": [[10, 20], 20, 25], "expected": [2]},
            ],
            "hint": "Первый шард — по lo, последний — по hi; затронуты все между ними.",
        },
        {
            "id": "shard-partition-prune",
            "mode": "func",
            "func": "prune",
            "title": "Отсечение партиций по дате",
            "statement": (
                "Таблица разбита по месяцам на партиции вида 'p_2024_03'. Напишите "
                "функцию prune(partitions, lo, hi): lo и hi — даты 'ГГГГ-ММ-ДД' "
                "(включительно). Верните отсортированный список партиций из "
                "переданного списка, чей месяц пересекается с диапазоном (остальные "
                "читать не нужно)."
            ),
            "starter": "def prune(partitions, lo, hi):\n    pass\n",
            "tests": [
                {"args": [["p_2024_01", "p_2024_02", "p_2024_03", "p_2024_04"], "2024-02-15", "2024-03-01"], "expected": ["p_2024_02", "p_2024_03"]},
                {"args": [["p_2024_01", "p_2024_02"], "2023-01-01", "2023-12-31"], "expected": []},
                {"args": [["p_2023_12", "p_2024_01"], "2023-12-31", "2024-01-01"], "expected": ["p_2023_12", "p_2024_01"]},
                {"args": [[], "2024-01-01", "2024-12-31"], "expected": []},
                {"args": [["p_2024_05"], "2024-05-10", "2024-05-10"], "expected": ["p_2024_05"]},
            ],
            "hint": "Сравнивайте строки 'ГГГГ_ММ': они упорядочены так же, как даты.",
        },
        {
            "id": "shard-snowflake-pack",
            "mode": "func",
            "func": "snowflake_pack",
            "title": "Идентификатор Snowflake: сборка",
            "statement": (
                "Распределённые идентификаторы собирают из полей: время (мс от "
                "эпохи) — 41 бит, номер шарда — 10 бит, счётчик — 12 бит. Напишите "
                "функцию snowflake_pack(ts_ms, shard, seq, epoch): ((ts_ms − epoch) "
                "<< 22) | (shard << 12) | seq."
            ),
            "starter": "def snowflake_pack(ts_ms, shard, seq, epoch):\n    pass\n",
            "tests": [
                {"args": [1700000000000, 5, 7, 1600000000000], "expected": 419430400000020487},
                {"args": [1600000000000, 0, 0, 1600000000000], "expected": 0},
                {"args": [1600000000001, 1023, 4095, 1600000000000], "expected": 8388607},
                {"args": [1700000123456, 1, 1, 1700000000000], "expected": 517811998721},
            ],
            "hint": "Сдвиги: время на 22 бита влево, шард на 12.",
        },
        {
            "id": "shard-snowflake-unpack",
            "mode": "func",
            "func": "snowflake_unpack",
            "title": "Идентификатор Snowflake: разбор",
            "statement": (
                "Напишите функцию snowflake_unpack(sid, epoch): обратная операция. "
                "Верните кортеж (время_мс_абсолютное, шард, счётчик): время = (sid "
                ">> 22) + epoch, шард — следующие 10 бит, счётчик — младшие 12."
            ),
            "starter": "def snowflake_unpack(sid, epoch):\n    pass\n",
            "tests": [
                {"args": [419430543367, 1600000000000], "expected": (1600000100000, 35, 7)},
                {"args": [0, 1600000000000], "expected": (1600000000000, 0, 0)},
                {"args": [4194303, 0], "expected": (0, 1023, 4095)},
                {"args": [17179869183, 10], "expected": (4105, 1023, 4095)},
                {"args": [4194304, 5], "expected": (6, 0, 0)},
            ],
            "hint": "Маски: 0x3FF — 10 бит, 0xFFF — 12 бит.",
        },
    ],
    8: [
        {
            "id": "cons-quorum-read",
            "mode": "func",
            "func": "quorum_read",
            "title": "Чтение с кворумом",
            "statement": (
                "Напишите функцию quorum_read(replicas, read_idx): replicas — "
                "список [значение, версия]; read_idx — номера опрашиваемых реплик. "
                "Верните значение с наибольшей версией среди опрошенных (при равных "
                "версиях — у первой из опрошенных)."
            ),
            "starter": "def quorum_read(replicas, read_idx):\n    pass\n",
            "tests": [
                {"args": [[["new", 3], ["new", 3], ["old", 2]], [1, 2]], "expected": "new"},
                {"args": [[["new", 3], ["old", 2], ["old", 2]], [1, 2]], "expected": "old"},
                {"args": [[["a", 1]], [0]], "expected": "a"},
                {"args": [[["x", 5], ["y", 5]], [1, 0]], "expected": "y"},
                {"args": [[["a", 1], ["b", 4], ["c", 2]], [0, 1, 2]], "expected": "b"},
            ],
            "hint": "Это сравнение версий — самое «свежее» значение побеждает; при равенстве остаётся первое.",
        },
        {
            "id": "cons-quorum-write",
            "mode": "func",
            "func": "quorum_write",
            "title": "Запись с кворумом",
            "statement": (
                "Напишите функцию quorum_write(replicas, write_idx, value): "
                "replicas — список [значение, версия]; запись получает новую версию "
                "= (максимальная версия среди ВСЕХ реплик) + 1 и применяется к "
                "репликам write_idx. Верните новый список реплик (исходный не "
                "меняйте)."
            ),
            "starter": "def quorum_write(replicas, write_idx, value):\n    pass\n",
            "tests": [
                {"args": [[["a", 1], ["a", 1], ["a", 1]], [0, 1], "b"], "expected": [["b", 2], ["b", 2], ["a", 1]]},
                {"args": [[["a", 1], ["z", 5], ["a", 1]], [2], "b"], "expected": [["a", 1], ["z", 5], ["b", 6]]},
                {"args": [[["a", 0]], [0], "x"], "expected": [["x", 1]]},
                {"args": [[["a", 1], ["b", 2]], [], "q"], "expected": [["a", 1], ["b", 2]]},
            ],
            "hint": "Сначала вычислите версию, затем перепишите выбранные реплики в копии списка.",
        },
        {
            "id": "cons-partition",
            "mode": "func",
            "func": "writers",
            "title": "CP или AP при разделении сети",
            "statement": (
                "Кластер из n узлов разделился на группы (размеры — список groups, "
                "сумма равна n). Напишите функцию writers(n, groups, mode): при "
                "mode 'CP' записи принимает только группа, содержащая строго больше "
                "половины узлов (кворум); при 'AP' — каждая непустая группа. "
                "Верните список номеров групп, принимающих записи, по возрастанию."
            ),
            "starter": "def writers(n, groups, mode):\n    pass\n",
            "tests": [
                {"args": [5, [3, 2], "CP"], "expected": [0]},
                {"args": [5, [3, 2], "AP"], "expected": [0, 1]},
                {"args": [4, [2, 2], "CP"], "expected": []},
                {"args": [4, [2, 2], "AP"], "expected": [0, 1]},
                {"args": [3, [1, 1, 1], "CP"], "expected": []},
                {"args": [3, [3], "CP"], "expected": [0]},
                {"args": [6, [4, 1, 1, 0], "AP"], "expected": [0, 1, 2]},
            ],
            "hint": "Кворум — строго больше n / 2 узлов: g * 2 > n.",
        },
        {
            "id": "cons-gcounter",
            "mode": "func",
            "func": "gcounter",
            "title": "CRDT: счётчик, растущий только вверх",
            "statement": (
                "Каждая реплика хранит словарь «узел → сколько увеличений сделал "
                "узел». Слияние — поэлементный максимум. Напишите функцию "
                "gcounter(states): слейте все состояния и верните кортеж (значение "
                "счётчика = сумма, слитый словарь)."
            ),
            "starter": "def gcounter(states):\n    pass\n",
            "tests": [
                {"args": [[{"a": 3, "b": 1}, {"a": 2, "b": 4}, {"c": 5}]], "expected": (12, {"a": 3, "b": 4, "c": 5})},
                {"args": [[]], "expected": (0, {})},
                {"args": [[{"a": 1}]], "expected": (1, {"a": 1})},
                {"args": [[{"a": 5}, {"a": 5}]], "expected": (5, {"a": 5})},
                {"args": [[{"x": 0}, {"y": 2}]], "expected": (2, {"x": 0, "y": 2})},
            ],
            "hint": "max по каждому узлу — слияние идемпотентно и коммутативно, поэтому порядок состояний не важен.",
        },
        {
            "id": "cons-gossip",
            "mode": "func",
            "func": "gossip_rounds",
            "title": "Сплетни: сколько раундов до согласия",
            "statement": (
                "Узлы стоят по кругу; у каждого [значение, версия]. В каждом раунде "
                "все узлы одновременно смотрят на соседа справа (i+1, по кругу) — "
                "по состоянию на начало раунда — и берут его запись, если версия "
                "там строго больше. Напишите функцию gossip_rounds(nodes): число "
                "раундов, после которого у всех узлов одна и та же версия (0, если "
                "уже). Верните None, если сходимости нет."
            ),
            "starter": "def gossip_rounds(nodes):\n    pass\n",
            "tests": [
                {"args": [[["a", 1], ["a", 1], ["a", 1]]], "expected": 0},
                {"args": [[["new", 2], ["old", 1], ["old", 1], ["old", 1]]], "expected": 3},
                {"args": [[["old", 1], ["old", 1], ["new", 2]]], "expected": 2},
                {"args": [[["a", 3], ["b", 1], ["c", 2], ["d", 1]]], "expected": 3},
                {"args": [[]], "expected": 0},
                {"args": [[["a", 1]]], "expected": 0},
                {"args": [[["old", 1], ["new", 2]]], "expected": 1},
            ],
            "hint": "Рассчитывайте раунд по копии состояния на его начало; повторяйте, пока версии не сравняются (не больше n раундов).",
        },
        {
            "id": "cons-linearizable",
            "mode": "func",
            "func": "linearizable",
            "title": "Линеаризуемость истории",
            "statement": (
                "Один регистр, начальное значение 0. Операция — [вид, значение, "
                "начало, конец]: вид 'w' (записала значение) или 'r' (прочитала "
                "значение). Если конец одной операции строго раньше начала другой, "
                "она должна идти раньше. История линеаризуема, если существует "
                "порядок всех операций, согласованный с этим «реальным временем», "
                "где каждое чтение возвращает значение последней предшествующей "
                "записи (или 0, если записей не было). Напишите функцию "
                "linearizable(history) (не более 7 операций): True или False."
            ),
            "starter": "from itertools import permutations\n\n\ndef linearizable(history):\n    pass\n",
            "tests": [
                {"args": [[["w", 1, 0, 2], ["r", 1, 3, 4]]], "expected": True},
                {"args": [[["w", 1, 0, 2], ["r", 0, 3, 4]]], "expected": False},
                {"args": [[["w", 1, 0, 10], ["r", 1, 2, 3], ["r", 0, 4, 5]]], "expected": False},
                {"args": [[["w", 1, 0, 10], ["r", 0, 2, 3], ["r", 1, 4, 5]]], "expected": True},
                {"args": [[]], "expected": True},
                {"args": [[["r", 0, 0, 1]]], "expected": True},
                {"args": [[["r", 5, 0, 1]]], "expected": False},
                {"args": [[["w", 1, 0, 1], ["w", 2, 2, 3], ["r", 1, 4, 5]]], "expected": False},
            ],
            "hint": "Переберите перестановки операций; допустима та, где нарушений «реального времени» нет и все чтения возвращают значение последней записи.",
        },
        {
            "id": "cons-read-repair",
            "mode": "func",
            "func": "read_repair",
            "title": "Read repair",
            "statement": (
                "При чтении со всех реплик координатор находит самую свежую запись "
                "и обновляет отставшие. Напишите функцию read_repair(replicas): "
                "replicas — список [значение, метка_времени]. Свежая — с наибольшей "
                "меткой (при равных — первая по порядку). Верните кортеж "
                "(свежее_значение, номера_реплик_которые_обновили) — те, чья метка "
                "меньше максимальной."
            ),
            "starter": "def read_repair(replicas):\n    pass\n",
            "tests": [
                {"args": [[["a", 1], ["b", 3], ["a", 1]]], "expected": ("b", [0, 2])},
                {"args": [[["x", 5]]], "expected": ("x", [])},
                {"args": [[["a", 2], ["a", 2]]], "expected": ("a", [])},
                {"args": [[["old", 1], ["old", 1], ["new", 9]]], "expected": ("new", [0, 1])},
                {"args": [[["z", 4], ["y", 4], ["x", 1]]], "expected": ("z", [2])},
            ],
            "hint": "Найдите максимум по метке, затем перечислите индексы реплик с меньшей меткой.",
        },
    ],
    9: [
        {
            "id": "cache-lfu",
            "mode": "stdout",
            "title": "LFU-кэш",
            "statement": (
                "Напишите класс LFUCache(capacity): get(key) возвращает значение "
                "или -1 и считает обращение; put(key, value) записывает (обновление "
                "существующего ключа тоже считается обращением). При переполнении "
                "вытесняется ключ с наименьшим числом обращений, а среди таких — "
                "давно неиспользованный (LRU)."
            ),
            "starter": "class LFUCache:\n    def __init__(self, capacity):\n        pass\n\n    def get(self, key):\n        pass\n\n    def put(self, key, value):\n        pass\n",
            "driver": (
                "c = LFUCache(2)\n"
                "c.put(1, 1)\n"
                "c.put(2, 2)\n"
                "print(c.get(1))\n"
                "c.put(3, 3)\n"
                "print(c.get(2), c.get(3))\n"
                "c.put(4, 4)\n"
                "print(c.get(1), c.get(3), c.get(4))\n"
                "c = LFUCache(0)\n"
                "c.put(1, 1)\n"
                "print(c.get(1))\n"
                "import random\n"
                "random.seed(4)\n"
                "c = LFUCache(100)\n"
                "hits = 0\n"
                "for _ in range(50000):\n"
                "    k = int(random.paretovariate(1.2)) % 400\n"
                "    if c.get(k) != -1:\n"
                "        hits += 1\n"
                "    else:\n"
                "        c.put(k, k)\n"
                "print(hits)\n"
            ),
            "expected": ["1", "-1 3", "-1 3 4", "-1", "49672"],
            "hint": "Храните число обращений каждого ключа и порядок использования; при вытеснении выберите минимум по числу обращений, при равенстве — самый давний.",
        },
        {
            "id": "cache-aside",
            "mode": "func",
            "func": "cache_aside",
            "title": "Cache-Aside",
            "statement": (
                "Напишите функцию cache_aside(requests): ['get', ключ] — читаем "
                "через кэш (нет в кэше — идём в базу и кладём в кэш); ['set', ключ] "
                "— запись в базу с сбросом ключа в кэше. Верните кортеж "
                "(попаданий_в_кэш, обращений_к_базе_на_чтение). Запись в базу в "
                "счёт «обращений на чтение» не входит."
            ),
            "starter": "def cache_aside(requests):\n    pass\n",
            "tests": [
                {"args": [[["get", "a"], ["get", "a"], ["set", "a"], ["get", "a"], ["get", "b"], ["get", "b"]]], "expected": (2, 3)},
                {"args": [[]], "expected": (0, 0)},
                {"args": [[["set", "x"], ["get", "x"]]], "expected": (0, 1)},
                {"args": [[["get", "a"], ["get", "a"], ["get", "a"], ["get", "a"], ["get", "a"]]], "expected": (4, 1)},
                {"args": [[["get", "a"], ["set", "a"], ["get", "a"], ["set", "a"], ["get", "a"], ["set", "a"]]], "expected": (0, 3)},
            ],
            "hint": "Множество ключей в кэше: get добавляет при промахе, set удаляет.",
        },
        {
            "id": "cache-stampede",
            "mode": "func",
            "func": "stampede",
            "title": "Лавина запросов к пустому кэшу",
            "statement": (
                "Ключ отсутствует в кэше. Запросы приходят в моменты arrivals (мс, "
                "по возрастанию); загрузка значения из базы занимает load_ms. Без "
                "защиты каждый запрос, пришедший до того, как закончилась первая "
                "загрузка (то есть в момент < arrivals[0] + load_ms), идёт в базу "
                "сам; запросы позже читают кэш. С защитой (single-flight) в базу "
                "идёт только первый запрос. Напишите функцию stampede(arrivals, "
                "load_ms): (обращений_без_защиты, обращений_с_защитой)."
            ),
            "starter": "def stampede(arrivals, load_ms):\n    pass\n",
            "tests": [
                {"args": [[0, 1, 2, 3, 50, 200], 100], "expected": (5, 1)},
                {"args": [[0], 10], "expected": (1, 1)},
                {"args": [[], 10], "expected": (0, 0)},
                {"args": [[0, 10, 20], 5], "expected": (1, 1)},
                {"args": [[5, 5, 5, 5], 1], "expected": (4, 1)},
                {"args": [[0, 99, 100, 101], 100], "expected": (2, 1)},
            ],
            "hint": "Первая загрузка завершится в arrivals[0] + load_ms: все запросы раньше этого момента были «лавиной».",
        },
        {
            "id": "cache-avalanche",
            "mode": "func",
            "func": "expiry_peak",
            "title": "Пик одновременного истечения",
            "statement": (
                "Если у многих ключей одинаковый TTL, они истекают одновременно "
                "(лавина кэша). Напишите функцию expiry_peak(expiries, window): "
                "expiries — моменты истечения ключей (секунды); верните наибольшее "
                "число ключей, истекающих внутри окна длиной window — то есть в "
                "полуинтервале [t, t + window) для какого-то t."
            ),
            "starter": "def expiry_peak(expiries, window):\n    pass\n",
            "tests": [
                {"args": [[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100], 5], "expected": 50},
                {"args": [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990], 5], "expected": 1},
                {"args": [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990], 100], "expected": 10},
                {"args": [[], 10], "expected": 0},
                {"args": [[1, 2, 3, 100, 101], 3], "expected": 3},
                {"args": [[7], 1], "expected": 1},
                {"args": [[0, 1, 2, 3], 2], "expected": 2},
            ],
            "hint": "Сортировка и скользящее окно двумя указателями: окно [x − window + 1…x].",
        },
        {
            "id": "cache-write-behind",
            "mode": "func",
            "func": "write_behind",
            "title": "Write-Behind",
            "statement": (
                "Запись через кэш с отложенной записью в базу. Напишите функцию "
                "write_behind(ops, flush_every): ops — список [ключ, значение]; "
                "после каждых flush_every операций (и в конце, если остались "
                "неотправленные) накопленные записи сбрасываются в базу, причём для "
                "каждого ключа — только последнее значение пачки (одна запись на "
                "ключ). Верните кортеж (число_записей_в_базу, итоговое состояние "
                "базы — словарь)."
            ),
            "starter": "def write_behind(ops, flush_every):\n    pass\n",
            "tests": [
                {"args": [[["a", 1], ["a", 2], ["b", 1], ["a", 3], ["c", 1]], 3], "expected": (4, {"a": 3, "b": 1, "c": 1})},
                {"args": [[], 5], "expected": (0, {})},
                {"args": [[["a", 1], ["a", 1], ["a", 1], ["a", 1], ["a", 1], ["a", 1], ["a", 1], ["a", 1], ["a", 1], ["a", 1]], 4], "expected": (3, {"a": 1})},
                {"args": [[["a", 1], ["b", 2]], 1], "expected": (2, {"a": 1, "b": 2})},
                {"args": [[["x", 1], ["y", 2], ["x", 3], ["y", 4]], 4], "expected": (2, {"x": 3, "y": 4})},
            ],
            "hint": "Накопитель-словарь пачки: повторная запись ключа перезаписывает значение; сбросьте по счётчику и в конце.",
        },
        {
            "id": "cache-penetration",
            "mode": "func",
            "func": "penetration",
            "title": "Проникновение: запросы к несуществующим ключам",
            "statement": (
                "Запросы к ключам, которых нет в базе, каждый раз «пробивают» кэш. "
                "Напишите функцию penetration(requests, db_keys, cache_nulls): кэш "
                "изначально пуст. Запрос к ключу, которого нет в кэше, идёт в базу "
                "(счётчик +1); если ключ есть в базе — он кладётся в кэш; если нет "
                "— кладётся пометка «пусто», только когда cache_nulls истинно. "
                "Верните число обращений к базе."
            ),
            "starter": "def penetration(requests, db_keys, cache_nulls):\n    pass\n",
            "tests": [
                {"args": [["a", "x", "x", "x", "a"], ["a"], False], "expected": 4},
                {"args": [["a", "x", "x", "x", "a"], ["a"], True], "expected": 2},
                {"args": [[], [], True], "expected": 0},
                {"args": [["x", "x", "x", "x", "x", "x", "x", "x", "x", "x"], [], False], "expected": 10},
                {"args": [["x", "x", "x", "x", "x", "x", "x", "x", "x", "x"], [], True], "expected": 1},
                {"args": [["a", "b", "a", "c"], ["a", "b"], True], "expected": 3},
            ],
            "hint": "Одно множество «в кэше»: ключ из базы добавляется всегда, отсутствующий — только при cache_nulls.",
        },
        {
            "id": "cache-two-level",
            "mode": "func",
            "func": "two_level",
            "title": "Двухуровневый кэш",
            "statement": (
                "Два кэша с вытеснением LRU: L1 на cap1 ключей и L2 на cap2. "
                "Запрос: ищем в L1 — попадание; иначе ищем в L2 — попадание (ключ "
                "переносится в L1 как последний использованный, из L2 не удаляется, "
                "но обращение освежает его); иначе промах: ключ загружается в оба "
                "кэша. Напишите функцию two_level(trace, cap1, cap2): "
                "(попаданий_L1, попаданий_L2, промахов)."
            ),
            "starter": "from collections import OrderedDict\n\n\ndef two_level(trace, cap1, cap2):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 1, 3, 1, 2, 4, 1, 2, 3], 2, 4], "expected": (2, 4, 4)},
                {"args": [[], 2, 2], "expected": (0, 0, 0)},
                {"args": [[1, 1, 1], 1, 1], "expected": (2, 0, 1)},
                {"args": [[1, 2, 3, 1, 2, 3], 1, 3], "expected": (0, 3, 3)},
                {"args": [[1, 2, 3, 4, 1], 2, 2], "expected": (0, 0, 5)},
                {"args": [[5, 5, 5, 5, 6, 6, 6, 6], 1, 2], "expected": (6, 0, 2)},
            ],
            "hint": "Два OrderedDict; helper put(cache, cap, key) кладёт ключ последним и вытесняет самый давний.",
        },
    ],
    10: [
        {
            "id": "olap-share",
            "mode": "sql",
            "title": "Доля категории в выручке",
            "statement": (
                "Для каждой категории посчитайте её долю в общей выручке в "
                "процентах, округлённую до одного знака. Колонки: category, pct. "
                "Используйте SUM() OVER () или подзапрос."
            ),
            "starter": "-- доля категории в общей выручке, %\nSELECT\n",
            "setup": (
                "CREATE TABLE sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, region TEXT NOT NULL, category TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO sales VALUES\n"
                " (1,'2024-01-01','north','tech',100),(2,'2024-01-01','south','food',40),(3,'2024-01-02','north','food',60),\n"
                " (4,'2024-01-02','south','tech',200),(5,'2024-01-03','north','books',30),(6,'2024-01-04','south','books',50),\n"
                " (7,'2024-01-04','north','tech',120),(8,'2024-02-01','south','tech',150),(9,'2024-02-02','north','food',90),\n"
                " (10,'2024-02-02','south','food',70),(11,'2024-02-03','north','books',20),(12,'2024-03-01','south','tech',300),\n"
                " (13,'2024-03-01','north','tech',80),(14,'2024-03-02','south','food',60);\n"
                "CREATE TABLE purchases (user_id INTEGER NOT NULL, month TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO purchases VALUES (1,'2024-01',10),(1,'2024-02',20),(2,'2024-01',5),(3,'2024-02',7),(3,'2024-03',9),(4,'2024-03',3),(2,'2024-03',8),(5,'2024-02',1);\n"
            ),
            "expected": [["books", 7.3], ["food", 23.4], ["tech", 69.3]],
            "ordered": False,
            "hint": "Общая сумма — скалярный подзапрос (SELECT SUM(amount) FROM sales) или оконная SUM(SUM(amount)) OVER ().",
        },
        {
            "id": "olap-running-total",
            "mode": "sql",
            "title": "Нарастающий итог",
            "statement": (
                "Посчитайте выручку по дням и нарастающий итог по дням. Колонки: "
                "day, total, running (running — сумма total по всем дням до "
                "текущего включительно); по возрастанию day."
            ),
            "starter": "-- выручка по дням и нарастающий итог\nSELECT\n",
            "setup": (
                "CREATE TABLE sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, region TEXT NOT NULL, category TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO sales VALUES\n"
                " (1,'2024-01-01','north','tech',100),(2,'2024-01-01','south','food',40),(3,'2024-01-02','north','food',60),\n"
                " (4,'2024-01-02','south','tech',200),(5,'2024-01-03','north','books',30),(6,'2024-01-04','south','books',50),\n"
                " (7,'2024-01-04','north','tech',120),(8,'2024-02-01','south','tech',150),(9,'2024-02-02','north','food',90),\n"
                " (10,'2024-02-02','south','food',70),(11,'2024-02-03','north','books',20),(12,'2024-03-01','south','tech',300),\n"
                " (13,'2024-03-01','north','tech',80),(14,'2024-03-02','south','food',60);\n"
                "CREATE TABLE purchases (user_id INTEGER NOT NULL, month TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO purchases VALUES (1,'2024-01',10),(1,'2024-02',20),(2,'2024-01',5),(3,'2024-02',7),(3,'2024-03',9),(4,'2024-03',3),(2,'2024-03',8),(5,'2024-02',1);\n"
            ),
            "expected": [["2024-01-01", 140, 140], ["2024-01-02", 260, 400], ["2024-01-03", 30, 430], ["2024-01-04", 170, 600], ["2024-02-01", 150, 750], ["2024-02-02", 160, 910], ["2024-02-03", 20, 930], ["2024-03-01", 380, 1310], ["2024-03-02", 60, 1370]],
            "ordered": True,
            "hint": "Сначала сгруппируйте по дням (подзапрос), потом SUM(total) OVER (ORDER BY day).",
        },
        {
            "id": "olap-moving-avg",
            "mode": "sql",
            "title": "Скользящее среднее",
            "statement": (
                "Для каждого дня выведите среднюю дневную выручку за последние три "
                "дня (текущий и два предыдущих дня с данными), округлённую до "
                "одного знака. Колонки: day, avg3; по возрастанию day."
            ),
            "starter": "-- скользящее среднее по трём дням\nSELECT\n",
            "setup": (
                "CREATE TABLE sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, region TEXT NOT NULL, category TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO sales VALUES\n"
                " (1,'2024-01-01','north','tech',100),(2,'2024-01-01','south','food',40),(3,'2024-01-02','north','food',60),\n"
                " (4,'2024-01-02','south','tech',200),(5,'2024-01-03','north','books',30),(6,'2024-01-04','south','books',50),\n"
                " (7,'2024-01-04','north','tech',120),(8,'2024-02-01','south','tech',150),(9,'2024-02-02','north','food',90),\n"
                " (10,'2024-02-02','south','food',70),(11,'2024-02-03','north','books',20),(12,'2024-03-01','south','tech',300),\n"
                " (13,'2024-03-01','north','tech',80),(14,'2024-03-02','south','food',60);\n"
                "CREATE TABLE purchases (user_id INTEGER NOT NULL, month TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO purchases VALUES (1,'2024-01',10),(1,'2024-02',20),(2,'2024-01',5),(3,'2024-02',7),(3,'2024-03',9),(4,'2024-03',3),(2,'2024-03',8),(5,'2024-02',1);\n"
            ),
            "expected": [["2024-01-01", 140.0], ["2024-01-02", 200.0], ["2024-01-03", 143.3], ["2024-01-04", 153.3], ["2024-02-01", 116.7], ["2024-02-02", 160.0], ["2024-02-03", 110.0], ["2024-03-01", 186.7], ["2024-03-02", 153.3]],
            "ordered": True,
            "hint": "Окно: AVG(total) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW).",
        },
        {
            "id": "olap-pivot",
            "mode": "sql",
            "title": "Сводная таблица (pivot)",
            "statement": (
                "Постройте сводную таблицу: по строке на регион и по колонке на "
                "категорию с суммой выручки (0, если продаж нет). Колонки: region, "
                "tech, food, books."
            ),
            "starter": "-- region, tech, food, books\nSELECT\n",
            "setup": (
                "CREATE TABLE sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, region TEXT NOT NULL, category TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO sales VALUES\n"
                " (1,'2024-01-01','north','tech',100),(2,'2024-01-01','south','food',40),(3,'2024-01-02','north','food',60),\n"
                " (4,'2024-01-02','south','tech',200),(5,'2024-01-03','north','books',30),(6,'2024-01-04','south','books',50),\n"
                " (7,'2024-01-04','north','tech',120),(8,'2024-02-01','south','tech',150),(9,'2024-02-02','north','food',90),\n"
                " (10,'2024-02-02','south','food',70),(11,'2024-02-03','north','books',20),(12,'2024-03-01','south','tech',300),\n"
                " (13,'2024-03-01','north','tech',80),(14,'2024-03-02','south','food',60);\n"
                "CREATE TABLE purchases (user_id INTEGER NOT NULL, month TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO purchases VALUES (1,'2024-01',10),(1,'2024-02',20),(2,'2024-01',5),(3,'2024-02',7),(3,'2024-03',9),(4,'2024-03',3),(2,'2024-03',8),(5,'2024-02',1);\n"
            ),
            "expected": [["north", 300, 150, 50], ["south", 650, 170, 50]],
            "ordered": False,
            "hint": "Для каждой колонки: SUM(CASE WHEN category = '...' THEN amount ELSE 0 END), группировка по региону.",
        },
        {
            "id": "olap-top2",
            "mode": "sql",
            "title": "Топ-2 продажи в регионе",
            "statement": (
                "Для каждого региона выведите две самые крупные продажи: колонки "
                "region, id, amount. Используйте ROW_NUMBER() с PARTITION BY (при "
                "равных суммах берите меньший id)."
            ),
            "starter": "-- две крупнейшие продажи в каждом регионе\nSELECT\n",
            "setup": (
                "CREATE TABLE sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, region TEXT NOT NULL, category TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO sales VALUES\n"
                " (1,'2024-01-01','north','tech',100),(2,'2024-01-01','south','food',40),(3,'2024-01-02','north','food',60),\n"
                " (4,'2024-01-02','south','tech',200),(5,'2024-01-03','north','books',30),(6,'2024-01-04','south','books',50),\n"
                " (7,'2024-01-04','north','tech',120),(8,'2024-02-01','south','tech',150),(9,'2024-02-02','north','food',90),\n"
                " (10,'2024-02-02','south','food',70),(11,'2024-02-03','north','books',20),(12,'2024-03-01','south','tech',300),\n"
                " (13,'2024-03-01','north','tech',80),(14,'2024-03-02','south','food',60);\n"
                "CREATE TABLE purchases (user_id INTEGER NOT NULL, month TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO purchases VALUES (1,'2024-01',10),(1,'2024-02',20),(2,'2024-01',5),(3,'2024-02',7),(3,'2024-03',9),(4,'2024-03',3),(2,'2024-03',8),(5,'2024-02',1);\n"
            ),
            "expected": [["north", 7, 120], ["north", 1, 100], ["south", 12, 300], ["south", 4, 200]],
            "ordered": False,
            "hint": "Нумерация внутри региона по убыванию суммы, затем фильтр rn <= 2 во внешнем запросе.",
        },
        {
            "id": "olap-lag-growth",
            "mode": "sql",
            "title": "Рост к прошлому месяцу",
            "statement": (
                "Посчитайте выручку по месяцам (strftime('%Y-%m', day)) и рост к "
                "предыдущему месяцу в процентах, округлённый до одного знака (для "
                "первого месяца — NULL). Колонки: month, total, growth_pct; по "
                "возрастанию month. Используйте LAG()."
            ),
            "starter": "-- month, total, growth_pct\nSELECT\n",
            "setup": (
                "CREATE TABLE sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, region TEXT NOT NULL, category TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO sales VALUES\n"
                " (1,'2024-01-01','north','tech',100),(2,'2024-01-01','south','food',40),(3,'2024-01-02','north','food',60),\n"
                " (4,'2024-01-02','south','tech',200),(5,'2024-01-03','north','books',30),(6,'2024-01-04','south','books',50),\n"
                " (7,'2024-01-04','north','tech',120),(8,'2024-02-01','south','tech',150),(9,'2024-02-02','north','food',90),\n"
                " (10,'2024-02-02','south','food',70),(11,'2024-02-03','north','books',20),(12,'2024-03-01','south','tech',300),\n"
                " (13,'2024-03-01','north','tech',80),(14,'2024-03-02','south','food',60);\n"
                "CREATE TABLE purchases (user_id INTEGER NOT NULL, month TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO purchases VALUES (1,'2024-01',10),(1,'2024-02',20),(2,'2024-01',5),(3,'2024-02',7),(3,'2024-03',9),(4,'2024-03',3),(2,'2024-03',8),(5,'2024-02',1);\n"
            ),
            "expected": [["2024-01", 600, None], ["2024-02", 330, -45.0], ["2024-03", 440, 33.3]],
            "ordered": True,
            "hint": "LAG(total) OVER (ORDER BY month) — значение предыдущей строки.",
        },
        {
            "id": "olap-cohort",
            "mode": "sql",
            "title": "Когорты по первой покупке",
            "statement": (
                "Таблица purchases(user_id, month, amount). Когорта пользователя — "
                "месяц его первой покупки. Выведите для каждой когорты число "
                "пользователей: колонки cohort, users; по возрастанию cohort."
            ),
            "starter": "-- cohort, users\nSELECT\n",
            "setup": (
                "CREATE TABLE sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, region TEXT NOT NULL, category TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO sales VALUES\n"
                " (1,'2024-01-01','north','tech',100),(2,'2024-01-01','south','food',40),(3,'2024-01-02','north','food',60),\n"
                " (4,'2024-01-02','south','tech',200),(5,'2024-01-03','north','books',30),(6,'2024-01-04','south','books',50),\n"
                " (7,'2024-01-04','north','tech',120),(8,'2024-02-01','south','tech',150),(9,'2024-02-02','north','food',90),\n"
                " (10,'2024-02-02','south','food',70),(11,'2024-02-03','north','books',20),(12,'2024-03-01','south','tech',300),\n"
                " (13,'2024-03-01','north','tech',80),(14,'2024-03-02','south','food',60);\n"
                "CREATE TABLE purchases (user_id INTEGER NOT NULL, month TEXT NOT NULL, amount INTEGER NOT NULL);\n"
                "INSERT INTO purchases VALUES (1,'2024-01',10),(1,'2024-02',20),(2,'2024-01',5),(3,'2024-02',7),(3,'2024-03',9),(4,'2024-03',3),(2,'2024-03',8),(5,'2024-02',1);\n"
            ),
            "expected": [["2024-01", 2], ["2024-02", 2], ["2024-03", 1]],
            "ordered": True,
            "hint": "Внутренний запрос находит MIN(month) для каждого пользователя; внешний группирует по когорте.",
        },
        {
            "id": "cqrs-bank",
            "mode": "func",
            "func": "handle",
            "title": "CQRS: команды и события",
            "statement": (
                "Напишите функцию handle(commands): команды ['open', счёт], "
                "['deposit', счёт, сумма] и ['withdraw', счёт, сумма]. Команда "
                "порождает событие: 'open' — ['opened', счёт] (если счёт уже есть — "
                "отклоняется), 'deposit' — ['deposited', счёт, сумма] (счёт должен "
                "существовать, сумма > 0), 'withdraw' — ['withdrawn', счёт, сумма] "
                "(счёт существует, сумма > 0 и хватает денег). Отклонённые команды "
                "событий не порождают. Модель чтения строится из событий. Верните "
                "кортеж (список событий, словарь «счёт → баланс»)."
            ),
            "starter": "def handle(commands):\n    pass\n",
            "tests": [
                {"args": [[["open", "a"], ["deposit", "a", 100], ["withdraw", "a", 30], ["withdraw", "a", 100]]], "expected": ([["opened", "a"], ["deposited", "a", 100], ["withdrawn", "a", 30]], {"a": 70})},
                {"args": [[["deposit", "x", 5]]], "expected": ([], {})},
                {"args": [[["open", "a"], ["open", "a"]]], "expected": ([["opened", "a"]], {"a": 0})},
                {"args": [[["open", "a"], ["deposit", "a", -5], ["deposit", "a", 0]]], "expected": ([["opened", "a"]], {"a": 0})},
                {"args": [[]], "expected": ([], {})},
                {"args": [[["open", "a"], ["open", "b"], ["deposit", "b", 10], ["withdraw", "b", 10]]], "expected": ([["opened", "a"], ["opened", "b"], ["deposited", "b", 10], ["withdrawn", "b", 10]], {"a": 0, "b": 0})},
            ],
            "hint": "Команда проходит проверку и только тогда превращается в событие; баланс считается проекцией событий.",
        },
        {
            "id": "olap-row-vs-column",
            "mode": "func",
            "func": "scan_bytes",
            "title": "Строки против колонок",
            "statement": (
                "Таблица из rows строк; размеры колонок в байтах — col_bytes "
                "(словарь «колонка → байт на значение»). Запрос читает колонки "
                "query_cols. Строчное хранилище читает строки целиком, колоночное — "
                "только нужные колонки. Напишите функцию scan_bytes(rows, "
                "col_bytes, query_cols): (байт_строчное, байт_колоночное, "
                "во_сколько_раз_меньше_колоночное), отношение округлите до двух "
                "знаков (для 0 прочитанных колонок — 0.0)."
            ),
            "starter": "def scan_bytes(rows, col_bytes, query_cols):\n    pass\n",
            "tests": [
                {"args": [1000000, {"id": 8, "name": 32, "country": 4, "amount": 8, "ts": 8}, ["country", "amount"]], "expected": (60000000, 12000000, 5.0)},
                {"args": [100, {"a": 4}, ["a"]], "expected": (400, 400, 1.0)},
                {"args": [10, {"a": 4, "b": 4}, []], "expected": (80, 0, 0.0)},
                {"args": [1000, {"id": 8, "payload": 992}, ["id"]], "expected": (1000000, 8000, 125.0)},
                {"args": [0, {"a": 1}, ["a"]], "expected": (0, 0, 0.0)},
            ],
            "hint": "Строчное: rows · сумма всех размеров; колоночное: rows · сумма размеров нужных колонок.",
        },
        {
            "id": "olap-rollup",
            "mode": "func",
            "func": "rollup",
            "title": "Итоги и подитоги (ROLLUP)",
            "statement": (
                "Напишите функцию rollup(rows): rows — [регион, категория, сумма]. "
                "Верните список [регион, категория, итог] со строками: по каждой "
                "паре (регион, категория); подитог по каждому региону (категория — "
                "None); общий итог (регион и категория — None). Порядок: по региону "
                "(None — в конце), внутри региона — по категории (None, то есть "
                "подитог, — в конце)."
            ),
            "starter": "def rollup(rows):\n    pass\n",
            "tests": [
                {"args": [[["north", "tech", 100], ["north", "food", 60], ["south", "tech", 200], ["north", "tech", 20]]], "expected": [["north", "food", 60], ["north", "tech", 120], ["north", None, 180], ["south", "tech", 200], ["south", None, 200], [None, None, 380]]},
                {"args": [[]], "expected": [[None, None, 0]]},
                {"args": [[["a", "x", 1]]], "expected": [["a", "x", 1], ["a", None, 1], [None, None, 1]]},
                {"args": [[["b", "y", 5], ["a", "z", 3], ["a", "y", 2]]], "expected": [["a", "y", 2], ["a", "z", 3], ["a", None, 5], ["b", "y", 5], ["b", None, 5], [None, None, 10]]},
            ],
            "hint": "Три словаря сумм (пара, регион, всё), потом одна сортировка с ключом (None в конец).",
        },
    ],
}
