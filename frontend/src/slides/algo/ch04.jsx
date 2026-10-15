// Слайды для «Алгоритмы и структуры данных», глава 4 — «Хеш-таблицы».
// Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СТРУКТУРЫ И ПАТТЕРНЫ / ГЛАВА 4</span>
      <span>{String(n).padStart(2, "0")} / 16</span>
    </div>
  );
}

function Slide({ n, title, sub, main, children }) {
  return (
    <div className="slide">
      <Rubric n={n} />
      <h3 className="s-title">{title}</h3>
      {sub && <p className="s-sub">{sub}</p>}
      <div className="s-divider" />
      <div className="s-body">{children}</div>
      {main && (
        <div className="s-main">
          <span className="s-main-label">ГЛАВНОЕ</span>
          <span className="s-main-text">{main}</span>
        </div>
      )}
    </div>
  );
}

function Node({ mono, title, sub, kind }) {
  return (
    <div className={`s-node ${kind || ""}`}>
      <span className={mono ? "s-node-mono" : "s-node-title"}>{title}</span>
      {sub && <span className="s-node-sub">{sub}</span>}
    </div>
  );
}

function Cmd({ children }) {
  return (
    <div className="s-cmd">
      <pre>{children}</pre>
    </div>
  );
}

const Arr = () => <span className="s-arr">→</span>;
const Down = () => <span className="s-arr">↓</span>;

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics = [
    ["#", "Хеш-функция", "Ключ превращается в номер ячейки"],
    ["=", "Коллизии", "Двум ключам — одна ячейка"],
    ["%", "Заполненность", "Тесно — таблица переезжает"],
    ["≡", "Узоры", "Множества, частоты, обмен на скорость"],
  ];
  return (
    <Slide
      n={1}
      title="Хеш-таблицы"
      sub="Глава 4 · Поиск без сортировки"
      main="Не порядок, а адрес: находить за константу в среднем."
    >
      <div className="s-grid2">
        {topics.map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">
        В прошлой главе мы платили за быстрый поиск сортировкой. Здесь платят
        памятью.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Гардероб и номерок"
      sub="Первая идея: ключ становится номером ячейки"
      main="Хеш-функция превращает ключ в номер ячейки — номерок из гардероба."
    >
      <div className="s-cols">
        <Node mono title="ключ «анна»" />
        <Arr />
        <Node mono title="h(key)" sub="хеш-функция" />
        <Arr />
        <Node kind="green" mono title="ячейка 7" sub="вешалка найдена мгновенно" />
      </div>
      <div className="s-note">
        Без просмотра сотен крючков: хеш-таблица — это массив плюс хеш-функция.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Три требования к хешу"
      sub="Быстрый, честный, равномерный"
      main="Если считать хеш дольше, чем просмотреть список, — вся затея теряет смысл."
    >
      <div className="s-cols">
        <Node mono title="быстрый" sub="иначе смысл теряется" />
        <Node
          mono
          title="детерминированный"
          sub="Один и тот же ключ — всегда один и тот же номер"
        />
        <Node
          kind="green"
          mono
          title="равномерный"
          sub="Ключи распределяются по ячейкам, не толпясь"
        />
      </div>
      <p className="s-hint">
        Нарушение любого из трёх требований ломает константу в формуле «о от
        единицы».
      </p>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Коллизии неизбежны"
      sub="Вопрос не «как избежать», а «как с ними жить»"
      main="Цепочки: каждая ячейка — ведро со списком пар ключ-значение."
    >
      <div className="s-note">
        Возможных ключей бесконечно много, ячеек конечное число — принцип
        голубей и клеток гарантирует совпадения.
      </div>
      <div className="s-cols">
        <Node mono title="key A" />
        <Arr />
        <Node kind="amber" mono title="ведро 7" sub="список пар" />
        <Arr />
        <Node mono title="key B" />
      </div>
      <p className="s-hint">
        При коллизии новая пара просто дописывается в список; внутри ячейки
        ключи сравниваются целиком.
      </p>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Открытая адресация"
      sub="Второй способ: всё живёт прямо в массиве"
      main="Ячейка занята чужим ключом — ищем следующую свободную."
    >
      <div className="s-cols">
        <span className="s-block">A</span>
        <span className="s-block">B</span>
        <span className="s-block changed">X — чужой</span>
        <Arr />
        <span className="s-block">C</span>
        <span className="s-block">D</span>
      </div>
      <div className="s-grid2">
        <Node
          title="Линейное пробирование"
          sub="Сначала соседняя, затем через одну — и так далее"
        />
        <Node
          kind="amber"
          title="Цена"
          sub="Без списков, но занятые ячейки любят сбиваться в кучи"
        />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Управление заполненностью"
      sub="У фактора заполнения есть предел"
      main="Редкий линейный переезд амортизируется до константы — вы это знаете из первой главы."
    >
      <div className="s-bar-wrap">
        <span>Заполнение таблицы · порог около 70%</span>
        <div className="s-bar amber">
          <div style={{ width: "70%" }} />
        </div>
      </div>
      <div className="s-cols">
        <Node
          kind="amber"
          title="Таблица наполнилась"
          sub="Новая, в полтора-два раза больше, переупаковка всех элементов"
        />
        <Node kind="green" mono title="O(1)*" sub="амортизированная цена операции" />
      </div>
      <p className="s-hint">
        Отношение числа элементов к числу ячеек — тот самый фактор заполнения.
      </p>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Худший случай"
      sub="Обещанный в первой главе"
      main="Граница между константой и линейностью проходит через качество хеша."
    >
      <div className="s-tree">
        <Node
          kind="amber"
          title="Плохая хеш-функция или ключи, подобранные специально"
        />
        <Down />
        <div className="s-cols">
          <Node kind="amber" mono title="все элементы в одном ведре" />
          <Arr />
          <Node kind="amber" mono title="O(n)" sub="таблица — обычный список" />
        </div>
      </div>
      <div className="s-note">
        Именно поэтому усреднённая константа — сделка: она честна, только пока
        хеш доброжелателен к вашим ключам.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Хеш не бесплатен"
      sub="Из чего складывается та самая константа"
      main="Константа в «о от единицы» — цена хеша плюс цена сравнения, и иногда она ощутима."
    >
      <div className="s-cols">
        <Node kind="green" title="Короткое слово" sub="Хеширование — мгновение" />
        <Node
          kind="amber"
          title="Файл в сто мегабайт"
          sub="Вычисление хеша — уже алгоритмическая задача"
        />
      </div>
      <div className="s-blocks">
        <div className="s-block">
          Кэшировать вычисленный хеш внутри неизменяемого объекта-ключа
        </div>
        <div className="s-block">
          Ключи — готовые короткие строки-идентификаторы
        </div>
        <div className="s-block changed">
          Сравнение ключей на равенство тоже может быть линейным по длине
        </div>
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Множество"
      sub="Хеш-таблица без значений"
      main="«Видели ли мы это уже?» — вопрос, на который множество отвечает мгновенно."
    >
      <div className="s-cols">
        <Node mono title="словарь" sub="ключ → значение" />
        <Node kind="green" mono title="множество" sub="только ключи" />
      </div>
      <div className="s-note">
        Проверка принадлежности за константу: дубликаты, уникальные посетители,
        пересечение списков — естественные решения через множество.
      </div>
      <p className="s-hint">
        Из хеш-таблиц с вынутыми значениями получается вторая ключевая
        структура.
      </p>
    </Slide>
  );
}

function S10() {
  const rows = [
    ["слова", "частота в тексте"],
    ["голоса", "результаты опроса"],
    ["ошибки", "статистика по типам"],
  ];
  return (
    <Slide
      n={10}
      title="Подсчёт частот"
      sub="Главный паттерн ежедневного применения"
      main="Один проход со словарём счётчиков — половина прикладных алгоритмов."
    >
      <Cmd>{"для каждого элемента в данных:\n  счётчик[элемент] += 1"}</Cmd>
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S11() {
  const rows = [
    ["O(n²) · O(1)", "Вложенный цикл: каждый с каждым"],
    ["O(n log n) · O(1)", "Сортировка и два указателя"],
    ["O(n) · O(n)", "Хеш: искать дополнение на лету"],
  ];
  return (
    <Slide
      n={11}
      title="Обмен памяти на скорость"
      sub="Задача: два числа с заданной суммой"
      main="Видел ли я дополнение? Словарь отвечает за константу — квадрат превращается в линию."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">
        Тот же обмен, что и в первой главе: каждая ступень скорости куплена
        памятью.
      </p>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Ловушки ключей"
      sub="Изменяемый ключ — потерянный элемент"
      main="Изменили ключ после вставки — ищете по новому хешу, а он лежит по старому номеру."
    >
      <div className="s-cols">
        <Node
          kind="amber"
          title="Изменили ключ после вставки"
          sub="Хеш новый — объект в таблице не найти"
        />
        <Node
          kind="green"
          title="Правило"
          sub="Ключи неизменяемы: числа, строки, кортежи"
        />
      </div>
      <div className="s-note">
        Вторая ловушка: обычный словарь не гарантирует порядок обхода. Нужен
        порядок — берите структуру, которая его явно обещает: по вставке или
        отсортированную.
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Не тот вопрос"
      sub="Словарь бессилен вне своей роли"
      main="Хеш-таблица отвечает «есть ли этот ключ», но не «какой минимальный»."
    >
      <div className="s-cols">
        <Node kind="green" mono title="O(1)" sub="«есть ли этот ключ?»" />
        <Node
          kind="amber"
          title="Минимум? Порядок? Сколько всего?"
          sub="Это вопросы других структур"
        />
      </div>
      <div className="s-note">
        Искушение применить хеш-таблицу там, где она не отвечает на вопрос, —
        третья ловушка после изменяемых ключей и веры в порядок обхода.
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Хеширование шире словаря"
      sub="Один узор — большие системы"
      main="«Ключ → адрес» работает от рекурсии до сетей доставки контента."
    >
      <div className="s-grid2">
        <Node
          title="Мемоизация"
          sub="Аргументы — ключ, уже посчитанный результат — значение"
        />
        <Node
          title="Базы данных"
          sub="Хеш-индексы для точечных запросов и хеш-джойн таблиц"
        />
        <Node
          title="Кэши и CDN"
          sub="Кэш в вебе; ближайший сервер по хешу запроса"
        />
      </div>
      <p className="s-hint">
        Так ускоряют рекурсивные алгоритмы — об этом подробнее в главе о
        динамическом программировании.
      </p>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Практика на сегодня"
      sub="Четыре упражнения"
      main="Разница во времени на миллионе элементов вас убедит."
    >
      <div className="s-blocks">
        <div className="s-block">
          Частота слов в любой статье — выведите топ-пять
        </div>
        <div className="s-block">
          Первый неповторяющийся символ строки — за один проход
        </div>
        <div className="s-block">
          Две суммы через словарь — и сравните время с наивным квадратом на
          миллионе элементов
        </div>
        <div className="s-block changed">
          Разберите документацию словаря своего языка: фактор заполнения,
          коллизии, порядок вставок
        </div>
      </div>
    </Slide>
  );
}

function S16() {
  const topics = [
    ["#", "Хеш-функция", "Ключ становится номером ячейки"],
    ["=", "Коллизии", "Цепочки или открытая адресация"],
    ["%", "Заполненность", "Переезд, амортизированный до константы"],
    ["≡", "Узоры", "Множества, частоты, группировка, обмен"],
  ];
  return (
    <Slide
      n={16}
      title="Итог"
      sub="Глава 4 · Поиск без сортировки"
      main="Три идеи: хеш-функция, разрешение коллизий, управление заполненностью."
    >
      <div className="s-grid2">
        {topics.map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">
        Средний случай — константа, худший — линейность; граница между ними
        проходит через качество хеша и доброжелательность ключей. В следующей
        главе — каталог узоров: два указателя, скользящее окно и разделяй и
        властвуй.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_A4 = {
  "7:4": [
    S01,
    S02,
    S03,
    S04,
    S05,
    S06,
    S07,
    S08,
    S09,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_A4).
export const SLIDE_TITLES_A4 = {
  "7:4": [
    "Введение",
    "Гардероб и номерок",
    "Три требования",
    "Коллизии",
    "Открытая адресация",
    "Заполненность",
    "Худший случай",
    "Цена хеша",
    "Множество",
    "Подсчёт частот",
    "Обмен на скорость",
    "Ловушки ключей",
    "Не тот вопрос",
    "Хеширование вокруг",
    "Практика",
    "Итог",
  ],
};
