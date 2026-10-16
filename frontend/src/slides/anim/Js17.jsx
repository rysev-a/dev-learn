import { scene } from "./alg.tsx";
import { Box, Tx, arrow, jc } from "./jv.tsx";

/* Глава 17 книги «Современный Frontend»: формы, валидация и хранилища. */

// 1. Данные и память
export const V01 = scene({
  labels: ["Ввод", "Проверка и отправка", "Сохранение"],
  caption: [
    "Через формы пользователь отдаёт данные приложению",
    "Введённое нужно проверить и отправить; хранилища позволяют не потерять его при перезагрузке страницы",
    "Состояние можно восстановить даже по адресу в строке браузера — пройдём весь путь данных",
  ],
  frames: [
    [Box("f", 180, 70, 160, 60, "форма", "y", { size: 12 })],
    [
      Box("f", 70, 70, 80, 34, "форма", "y", { size: 10.5 }),
      arrow("e1", 112, 70, 148, 70, "g"),
      Box("v", 190, 70, 70, 34, "проверка", "b", { size: 10 }),
      arrow("e2", 228, 70, 262, 70, "g"),
      Box("s", 312, 70, 80, 34, "сервер", "g", { size: 10.5 }),
    ],
    [
      ...["cookie", "localStorage", "IndexedDB", "URL"].map((n, i) =>
        Box(
          `h${i}`,
          66 + (i % 2) * 130,
          56 + Math.floor(i / 2) * 44,
          116,
          28,
          n,
          "b",
          { size: 10 },
        ),
      ),
    ],
  ],
});

// 2. Элементы форм
export const V02 = scene({
  labels: ["Поля", "name и label", "autocomplete"],
  caption: [
    'input разных типов, textarea, select, чекбоксы и радиокнопки, fieldset; кнопка внутри формы по умолчанию отправляет её — другим ставят type="button"',
    "Каждому полю нужно имя (оно попадёт в данные) и подпись <label for> — это делает поле доступным и увеличивает область клика",
    "autocomplete подсказывает менеджеру паролей, что просят в поле, и упрощает вход",
  ],
  frames: [
    [
      ...[
        "text",
        "email",
        "number",
        "date",
        "password",
        "checkbox",
        "radio",
        "file",
      ].map((n, i) =>
        Box(
          `t${i}`,
          54 + (i % 4) * 84,
          56 + Math.floor(i / 4) * 44,
          76,
          26,
          n,
          "b",
          { size: 9, mono: true },
        ),
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          '<label for="email">Почта</label>',
          '<input id="email" name="email"',
          '       type="email" required>',
        ],
        [1, 2],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          '<input name="user" autocomplete="username">',
          '<input name="pw" type="password"',
          '       autocomplete="current-password">',
        ],
        [0, 2],
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
  ],
});

// 3. Отправка
export const V03 = scene({
  labels: ["Пары имя-значение", "FormData", "Кодирование"],
  caption: [
    "В набор попадают только поля с именем, не отключённые; отмеченные флажки и переключатели; кнопка — если нажата именно она",
    "FormData собирает форму программно: append, get, getAll, set, delete; отправляется через fetch",
    "urlencoded — «ключ=значение» через &; multipart нужен для файлов; GET кладёт данные в адрес, POST — в тело",
  ],
  frames: [
    [
      ...["name=Ада", "age=36", "agree=on", "disabled ✕", "unchecked ✕"].map(
        (n, i) =>
          Box(
            `p${i}`,
            66 + (i % 3) * 114,
            56 + Math.floor(i / 3) * 44,
            100,
            26,
            n,
            i < 3 ? "g" : "r",
            { size: 9.5, mono: true },
          ),
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "const fd = new FormData(form);",
          "fd.set('tag', 'a');",
          "fd.append('tag', 'b');",
          "fetch('/api', { method: 'POST', body: fd });",
        ],
        [3],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "urlencoded:  name=%D0%90%D0%B4%D0%B0&age=36",
          "multipart:   --boundary",
          "             Content-Disposition: form-data;",
          '             name="photo"; filename="a.png"',
        ],
        [0],
        { w: 340, size: 8.5, lh: 22 },
      ),
    ],
  ],
});

// 4. Валидация
export const V04 = scene({
  labels: ["Атрибуты", "ValidityState", "Свои сообщения"],
  caption: [
    "required, pattern, min, max, minlength, maxlength и step задают правила; type=email и url проверяются автоматически",
    "У поля есть validity с флагами: valueMissing, typeMismatch, patternMismatch, tooLong, tooShort, rangeUnderflow, rangeOverflow, stepMismatch",
    "checkValidity и reportValidity, setCustomValidity для своего сообщения; :invalid стилизует ошибочные поля; novalidate отключает встроенное",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          '<input type="number" min="18" max="99" required>',
          '<input pattern="[0-9]{6}" minlength="6">',
        ],
        [0, 1],
        { w: 340, size: 9.5, lh: 30 },
      ),
    ],
    [
      ...[
        "valueMissing",
        "typeMismatch",
        "patternMismatch",
        "tooShort",
        "rangeUnderflow",
        "stepMismatch",
      ].map((n, i) =>
        Box(
          `v${i}`,
          66 + (i % 2) * 130,
          40 + Math.floor(i / 2) * 36,
          118,
          24,
          n,
          "b",
          { size: 8.5, mono: true },
        ),
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "input.setCustomValidity('Имя занято');",
          "input.checkValidity();    // false",
          "input.reportValidity();   // покажет подсказку",
          "input:invalid { border-color: red; }",
        ],
        [0, 3],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
  ],
});

// 5. Клиент и сервер
export const V05 = scene({
  labels: ["Не защита", "Сообщения", "Фокус и ARIA"],
  caption: [
    "Клиентская проверка — удобство, а не защита: любой пользователь может отправить запрос в обход формы, сервер проверяет всё заново",
    "Ошибка стоит рядом с полем и понятна; её показывают после ухода из поля или при попытке отправки, а не в момент первой буквы",
    "aria-describedby связывает сообщение с полем, aria-invalid помечает ошибку; при отправке фокус переходит на первое неверное поле",
  ],
  frames: [
    [
      Box("c", 90, 70, 110, 34, "форма\n(клиент)", "b", { size: 10 }),
      Box("s", 270, 70, 110, 34, "сервер\nпроверяет", "g", { size: 10 }),
      arrow("e", 146, 70, 214, 70, "g"),
      Box("x", 180, 130, 110, 24, "curl → сервер", "r", {
        size: 9,
        mono: true,
      }),
      arrow("e2", 180, 118, 250, 90, "r"),
    ],
    [
      Box("i", 180, 50, 220, 30, "email: ada@", "r", {
        size: 10.5,
        mono: true,
      }),
      Tx("n", 180, 84, "Укажите адрес целиком: имя@домен", {
        size: 10,
        c: "r",
      }),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          '<input id="e" aria-invalid="true"',
          '       aria-describedby="e-err">',
          '<p id="e-err">Укажите адрес</p>',
          "firstInvalid.focus();",
        ],
        [0, 1, 3],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
  ],
});

// 6. Состояние формы
export const V06 = scene({
  labels: ["Контролируемая и нет", "value и defaultValue", "beforeunload"],
  caption: [
    "Неконтролируемая форма хранит значения в самом DOM, контролируемая — в состоянии приложения и перерисовывает поле на каждое изменение",
    "value — текущее значение, defaultValue — начальное: по различию определяют, изменил ли пользователь данные",
    "beforeunload предупреждает о несохранённых изменениях; черновики сохраняют автоматически с паузой после ввода",
  ],
  frames: [
    [
      Box("a", 90, 70, 120, 40, "DOM хранит\nзначение", "b", { size: 10 }),
      Box("b", 270, 70, 120, 40, "состояние\nприложения", "y", { size: 10 }),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "const dirty = input.value !== input.defaultValue;",
          "form.reset();   // вернёт defaultValue",
        ],
        [0],
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "window.addEventListener('beforeunload', (e) => {",
          "  if (isDirty()) e.preventDefault();",
          "});",
          "input.addEventListener('input', debounce(saveDraft, 500));",
        ],
        [1, 3],
        { w: 340, size: 9, lh: 22 },
      ),
    ],
  ],
});

// 7. Cookie
export const V07 = scene({
  labels: ["Set-Cookie", "Атрибуты", "document.cookie"],
  caption: [
    "Сервер ставит куки заголовком Set-Cookie, а браузер возвращает их в каждом запросе на тот же сайт",
    "Path и Domain — область, Max-Age и Expires — время жизни, Secure — только по HTTPS, HttpOnly скрывает от скриптов, SameSite ограничивает отправку с чужих сайтов",
    "document.cookie показывает куки скриптам; около 4 КБ на запись и вес в каждом запросе; идентификатор сессии — только HttpOnly",
  ],
  frames: [
    [
      Box("s", 90, 70, 100, 34, "сервер", "g", { size: 11 }),
      Box("b", 270, 70, 100, 34, "браузер", "b", { size: 11 }),
      arrow("e1", 140, 62, 218, 62, "g"),
      arrow("e2", 218, 80, 140, 80, "y"),
      Tx("a", 180, 48, "Set-Cookie", { size: 9, mono: true }),
      Tx("b2", 180, 98, "Cookie: …", { size: 9, mono: true }),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "Set-Cookie: sid=abc123;",
          "  Path=/; Max-Age=3600;",
          "  Secure; HttpOnly; SameSite=Lax",
        ],
        [2],
        { w: 330, size: 10.5, lh: 26 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "document.cookie = 'theme=dark; Max-Age=86400';",
          "document.cookie   // 'theme=dark; lang=ru'",
          "// sid с HttpOnly здесь не виден",
        ],
        [2],
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
  ],
});

// 8. Web Storage
export const V08 = scene({
  labels: ["Строки", "Синхронно и квота", "Событие storage"],
  caption: [
    "localStorage живёт, пока пользователь не очистит данные, sessionStorage — до закрытия вкладки; ключи и значения — строки, объекты хранят через JSON",
    "Методы синхронны, большие объёмы тормозят страницу; квота около 5 МБ — при превышении исключение QuotaExceededError",
    "Событие storage сообщает другим вкладкам об изменении — так синхронизируют тему и выход; секреты хранить нельзя: любой скрипт их прочитает",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "localStorage.setItem('user', JSON.stringify(u));",
          "const u = JSON.parse(localStorage.getItem('user'));",
          "localStorage.removeItem('user');",
        ],
        [0, 1],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "try {",
          "  localStorage.setItem('big', hugeString);",
          "} catch (e) {",
          "  // e.name === 'QuotaExceededError'",
          "}",
        ],
        [3],
        { w: 340, size: 10, lh: 22 },
      ),
    ],
    [
      Box("a", 90, 70, 110, 34, "вкладка A\nsetItem", "b", { size: 9.5 }),
      Box("b", 270, 70, 110, 34, "вкладка B\nonstorage", "g", { size: 9.5 }),
      arrow("e", 146, 70, 214, 70, "y"),
    ],
  ],
});

// 9. IndexedDB
export const V09 = scene({
  labels: ["Хранилища и индексы", "Транзакции", "Версии схемы"],
  caption: [
    "IndexedDB хранит объекты в хранилищах: ключ — путь внутри объекта, индексы позволяют искать по полям",
    "Все операции — внутри транзакций и асинхронны: открывается запрос, результат приходит в обработчике; удобнее тонкие обёртки, например idb",
    "Схема меняется при увеличении версии в onupgradeneeded; рядом — Cache API, файловая система приватного происхождения и StorageManager.estimate()",
  ],
  frames: [
    [
      Box("s", 90, 56, 120, 28, "store: orders", "y", { size: 10, mono: true }),
      Box("i", 90, 100, 120, 24, "index: byDate", "b", {
        size: 9.5,
        mono: true,
      }),
      Box("r", 270, 78, 130, 70, "{ id: 7,\n  date: …,\n  total: 40 }", "g", {
        size: 9.5,
        mono: true,
      }),
      arrow("e", 150, 56, 204, 70, "g"),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "const tx = db.transaction('orders', 'readwrite');",
          "tx.objectStore('orders').put(order);",
          "tx.oncomplete = () => done();",
        ],
        [1],
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
    [
      jc(
        "c",
        20,
        36,
        [
          "const req = indexedDB.open('app', 3);",
          "req.onupgradeneeded = (e) => {",
          "  if (e.oldVersion < 3) addIndex();",
          "};",
        ],
        [2],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
  ],
});

// 10. URL и History
export const V10 = scene({
  labels: ["URL и параметры", "pushState", "popstate"],
  caption: [
    "URL разбирает адрес на части, URLSearchParams читает и корректно кодирует параметры запроса",
    "pushState добавляет запись в историю без перезагрузки, replaceState заменяет текущую; состояние — часть адреса приложения",
    "popstate срабатывает, когда пользователь жмёт «назад» или «вперёд»; раньше использовали часть после решётки — она работает без настройки сервера",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        [
          "const u = new URL(location.href);",
          "u.searchParams.set('page', 2);",
          "u.pathname   // '/catalog'",
        ],
        [1],
        { w: 330, size: 10, lh: 24 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "history.pushState({ id: 7 }, '', '/item/7');",
          "history.replaceState(null, '', '/item/7?x=1');",
        ],
        [0],
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
    [
      jc(
        "c",
        20,
        40,
        [
          "window.addEventListener('popstate', (e) => {",
          "  render(location.pathname, e.state);",
          "});",
        ],
        [1],
        { w: 340, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 11. Роутер
export const V11 = scene({
  labels: ["Сопоставление", "Перехват кликов", "Сервер и прокрутка"],
  caption: [
    "Маршрутизатор сопоставляет путь с экраном, достаёт параметры из адреса и вызывает pushState вместо перехода",
    "Не перехватывают клики с модификаторами, средней кнопкой, ссылки с target и download, а также чужие адреса",
    "Нужны восстановление прокрутки при возврате и страница «не найдено»; сервер отдаёт главную страницу на любые пути, иначе обновление даст ошибку",
  ],
  frames: [
    [
      jc(
        "c",
        20,
        40,
        ["'/users/:id'  →  UserPage", "'/users/42'   →  { id: '42' }"],
        [1],
        { w: 330, size: 10.5, lh: 30 },
      ),
    ],
    [
      jc(
        "c",
        20,
        30,
        [
          "if (e.button !== 0 || e.ctrlKey || e.metaKey) return;",
          "if (a.target || a.hasAttribute('download')) return;",
          "if (a.origin !== location.origin) return;",
          "e.preventDefault(); navigate(a.pathname);",
        ],
        [3],
        { w: 340, size: 9, lh: 22 },
      ),
    ],
    [
      Box("u", 90, 56, 110, 28, "GET /users/42", "b", {
        size: 9.5,
        mono: true,
      }),
      arrow("e", 146, 56, 214, 56, "g"),
      Box("s", 270, 56, 110, 28, "index.html", "g", { size: 10 }),
      Tx("n", 180, 112, "для любого пути — одна страница", { size: 9.5 }),
    ],
  ],
});

// 12. Безопасность хранения
export const V12 = scene({
  labels: ["XSS и токены", "Куки и CSRF", "Приватность"],
  caption: [
    "Всё в localStorage и IndexedDB доступно любому скрипту страницы: внедрённый код украдёт токен",
    "Куки с HttpOnly скрыты от скриптов, но вместе с ними приходит риск подделки запросов: SameSite и токены; CSP сокращает риск внедрения кода",
    "Web Crypto шифрует, но ключ всё равно придётся где-то хранить; законы о приватности: согласие на необязательные куки и право удалить данные",
  ],
  frames: [
    [
      Box("t", 90, 60, 110, 28, "token в\nlocalStorage", "r", { size: 9 }),
      Box("x", 270, 60, 110, 28, "чужой скрипт\n(XSS)", "r", { size: 9 }),
      arrow("e", 214, 60, 146, 60, "r"),
      Tx("n", 180, 110, "прочитает и отправит", { size: 10, c: "r" }),
    ],
    [
      Box("c", 90, 60, 120, 30, "HttpOnly cookie", "g", { size: 10 }),
      Box("r", 270, 60, 120, 30, "CSRF-риск", "y", { size: 10 }),
      Box("m", 180, 116, 220, 26, "SameSite=Lax · токены · CSP", "b", {
        size: 9.5,
        mono: true,
      }),
    ],
    [
      ...["согласие", "удаление", "минимум"].map((n, i) =>
        Box(`p${i}`, 66 + i * 114, 70, 100, 34, n, "b", { size: 10.5 }),
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Формы", "Хранилища", "Дальше"],
  caption: [
    "Форма отправляет пары имя-значение, FormData собирает их программно; встроенная проверка читается через validity, настоящая — на сервере",
    "Куки — сессия, Web Storage — строки, IndexedDB — объекты; адрес и история — часть состояния, роутер сопоставляет их с экранами",
    "Дальше — сеть: fetch, CORS и WebSocket",
  ],
  frames: [
    [
      Box("a", 90, 60, 120, 30, "FormData", "y", { size: 10.5 }),
      Box("b", 240, 60, 130, 30, "validity", "b", { size: 10.5 }),
      Box("c", 160, 116, 190, 28, "сервер проверяет всё", "g", { size: 10 }),
    ],
    [
      Box("a", 90, 60, 120, 30, "cookie · storage", "y", { size: 10 }),
      Box("b", 240, 60, 130, 30, "IndexedDB", "b", { size: 10.5 }),
      Box("c", 160, 116, 190, 28, "URL · History", "g", { size: 10.5 }),
    ],
    [
      jc(
        "c",
        40,
        44,
        [
          "const res = await fetch('/api/items');",
          "const data = await res.json();",
        ],
        [0],
        { w: 290, size: 10.5, lh: 26 },
      ),
      Tx("n", 180, 126, "глава 18: сеть в браузере", { size: 9.5 }),
    ],
  ],
});
