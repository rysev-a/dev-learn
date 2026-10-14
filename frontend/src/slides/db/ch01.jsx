// Слайды для «Базы данных: под капотом», глава 1 — «Модель данных и запросы».
// Тот же дизайн-код, что и у других книг: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>МОДЕЛЬ И НАДЁЖНОСТЬ / ГЛАВА 1</span>
      <span>{String(n).padStart(2, "0")} / 21</span>
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

// --- сцены ----------------------------------------------------------------

function S01() {
  const topics = [
    ["▤", "Таблицы", "Строки, колонки, типы — честная структура"],
    ["∞", "Связки", "Ключи и соединения вместо указателей"],
    ["Σ", "Группировки", "Агрегаты: свернуть строки и не наврать"],
    ["▣", "Окна", "Агрегат, который сохраняет детали"],
  ];
  return (
    <Slide
      n={1}
      title="Модель данных и запросы"
      sub="Глава 1 · Таблицы, связки, группировки"
      main="Причина тормозов — не база, а непонимание её модели. Начинаем с фундамента."
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
        Цель: запросы, за которые не стыдно через год, и схемы, которые не
        разваливаются на третий месяц.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Полминуты истории"
      sub="Эдгар Кодд, 1971 год"
      main="Отделить логику от физики — тот же принцип, что в файловых системах и сетях."
    >
      <div className="s-cols">
        <Node mono title="1971" sub="Статья Кодда" />
        <Arr />
        <Node
          title="Логика ≠ физика"
          sub="Программа больше не зависит от того, как данные лежат на диске"
        />
        <Arr />
        <Node
          kind="green"
          mono
          title="50+ лет"
          sub="Держит большую часть интернета"
        />
      </div>
      <div className="s-note">
        Модель победила не из моды: за абстракцией стоит свобода менять
        реализацию, не трогая программы.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Почему победили таблицы"
      sub="Декларативность — главная идея"
      main="Вы описываете, что хотите, — путь строит оптимизатор, и делает это лучше человека в 99 случаях из 100."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Навигационные базы"
          sub="Ходи по указателям вручную — логика и физика сплетены"
        />
        <Node
          kind="green"
          title="Реляционная модель"
          sub="Строки уникальны, колонки типизированы, связи явные"
        />
      </div>
      <Cmd>
        {
          "SELECT — что хочу\nFROM · JOIN · WHERE — откуда и по какому правилу\nплан исполнения — забота базы"
        }
      </Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Нормальные формы"
      sub="Каждый факт живёт в одном месте"
      main="Денормализация — решение, а не незнание; ненормализованная схема — долг, который взимается процентами."
    >
      <Node
        mono
        title="1НФ"
        sub="Значения атомарны: никаких списков в ячейке"
      />
      <Down />
      <Node mono title="2НФ" sub="Неключевое зависит от ключа целиком" />
      <Down />
      <Node kind="green" mono title="3НФ" sub="И ни от чего, кроме ключа" />
      <div className="s-note amber">
        Список в ячейке лишает индексов, ограничений и честных связок. А
        скопированная ради скорости цена в заказе — осознанная денормализация.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Типы колонок"
      sub="Половина здоровья схемы"
      main="База проверяет типы и уникальность честнее любого ревьюера — в момент записи."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          mono
          title="VARCHAR для дат"
          sub="Бомба замедленного действия: сортировка в алфавитном порядке"
        />
        <Node
          kind="green"
          mono
          title="BIGINT / NUMERIC"
          sub="Деньги — целые копейки или точные десятичные, не FLOAT"
        />
      </div>
      <div className="s-label">ДИСЦИПЛИНА ТИПОВ</div>
      <div className="s-opts">
        <span className="s-path accent">DATE</span>
        <span>даты для дат</span>
        <span className="s-path accent">NUMERIC</span>
        <span>точные деньги</span>
        <span className="s-path accent">UNIQUE</span>
        <span>вместо надежды на код</span>
      </div>
      <p className="s-hint">
        Копеечное расхождение в миллионах операций — не баг отчёта, а ваша
        реальная потеря.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Пустота — третье состояние"
      sub="NULL — не ноль и не пустая строка"
      main="Либо колонка обязательна и не пуста, либо вы явно договорились, как жить с пустотой."
    >
      <Cmd>
        {
          "x <> 5        → неизвестно, строка отфильтруется\nSUM(...)      → отсутствие значения распространяется как вирус\nUNIQUE-индекс → сколько угодно пустых значений"
        }
      </Cmd>
      <div className="s-note">
        Классика: проверка на неравенство молча пропускает пустые строки, сумма
        обнуляет расчёт отчёта.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Ключи"
      sub="Суррогатный внутри, естественный — ограничением"
      main="Каскадные удаления — с опаской: одно неосторожное стирает половину базы по цепочке."
    >
      <div className="s-grid2">
        <Node
          kind="green"
          title="Суррогатный ключ"
          sub="Просто число, ничего не значит — зато никогда не меняется"
        />
        <Node
          kind="amber"
          title="Естественный ключ"
          sub="Паспорт, почта, артикул — жизнь меняет их, это боль на весь зоопарк связей"
        />
      </div>
      <div className="s-label">ССЫЛОЧНАЯ ЦЕЛОСТНОСТЬ</div>
      <Cmd>
        {
          "REFERENCES — нельзя сослаться на несуществующее\nON DELETE — нельзя удалить то, на что ссылаются"
        }
      </Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Служебные колонки и удаление"
      sub="Мелочи, которые спасают споры"
      main="Решение о удалении принимайте осознанно и записывайте в правила проекта."
    >
      <div className="s-label">В КАЖДОЙ ТАБЛИЦЕ</div>
      <div className="s-opts">
        <span className="s-path accent">created_at</span>
        <span className="s-path accent">updated_at</span>
        <span className="s-path accent">updated_by</span>
        <span>кто и когда поменял цену</span>
      </div>
      <div className="s-grid2">
        <Node title="Физическое" sub="Чисто, но после ошибки вернуть нечего" />
        <Node
          kind="amber"
          title="Мягкое (пометка)"
          sub="Каждая выборка обязана помнить про фильтр — иначе отчёты посчитают удалённое"
        />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Соединения"
      sub="Сердце реляционности"
      main="Соединения умножают строки — считайте агрегаты в подзапросах до соединения."
    >
      <div className="s-cols">
        <Node mono title="INNER" sub="Только пары с обеих сторон" />
        <Node mono title="LEFT" sub="Всё из левой + правое или пустоты" />
      </div>
      <div className="s-label">КЛАССИЧЕСКАЯ ОШИБКА НОВИЧКА</div>
      <Cmd>
        {
          "заказы ⋈ позиции ⋈ доставки\n→ суммы кратно дублируются: каждая связь умножает строки"
        }
      </Cmd>
      <p className="s-hint">
        Условие соединения без индекса в тестовой базе незаметно, в проде —
        вечность.
      </p>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Группировки"
      sub="WHERE — до групп, HAVING — после"
      main="Половина неправильных отчётов — фильтр не в том месте."
    >
      <Cmd>
        {
          "SELECT city, COUNT(*)\nFROM orders\nWHERE status = 'paid'      — фильтр строк\nGROUP BY city\nHAVING COUNT(*) > 10;      — фильтр групп"
        }
      </Cmd>
      <div className="s-note amber">
        Среднее по пустому множеству — не ноль, а отсутствие значения: в
        вычислениях оно расползается как вирус.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Оконные функции"
      sub="Агрегат без схлопывания строк"
      main="Группировка теряет детали, окно сохраняет — отчётная работа уходит из кода в один запрос."
    >
      <Cmd>
        {
          "RANK()   OVER (PARTITION BY category ORDER BY amount DESC)\nSUM(...) OVER (ORDER BY day)              — нарастающая сумма\namount / SUM(amount) OVER ()              — доля от общего"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="amber"
          mono
          title="GROUP BY"
          sub="Схлопывает: остаётся одна строка на группу"
        />
        <Node
          kind="green"
          mono
          title="OVER"
          sub="Величина по группе рядом с каждой строкой"
        />
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Общие табличные выражения"
      sub="Длинные запросы человеческим языком"
      main="Читаемость запроса прямо пропорциональна числу найденных в нём багов."
    >
      <Cmd>
        {
          "WITH топ_клиентов AS (\n  SELECT … FROM orders GROUP BY …\n)\nSELECT … FROM топ_клиентов …;"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Именованные шаги"
          sub="Каждый читается и тестируется отдельно"
        />
        <Node
          mono
          title="WITH RECURSIVE"
          sub="Иерархии: оргструктура, дерево категорий, граф подписок"
        />
      </div>
      <p className="s-hint">
        База умеет много, но бизнес-логика на пятьсот строк в одном запросе — не
        элегантность, а ловушка.
      </p>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Форма запроса"
      sub="Философия декларативного языка"
      main="Ваша ответственность — схема, индексы и статистика, а не порядок условий."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Фольклор"
          sub="«Переставь условия в WHERE — станет быстрее»: не ускоряет ничего"
        />
        <Node
          kind="green"
          title="Что влияет на самом деле"
          sub="Коррелированные подзапросы в цикле, функции на каждую строку, отрицательные условия без индексов"
        />
      </div>
      <p className="s-hint">
        Учитесь видеть форму запроса, а не дышать на порядок условий.
      </p>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Postgres и MySQL"
      sub="Два великих семейства"
      main="Ядро везде одинаково — учить стоит именно его. Курс говорит на постгресе."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">POSTGRES</div>
          <span className="s-node-title">
            Строже в типах, богаче возможностями
          </span>
          <span className="s-node-sub">
            Выбор по умолчанию для нового бэкенда · поведение под нагрузкой
            задокументировано до деталей
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">MYSQL</div>
          <span className="s-node-title">Быстрее в простых чтениях</span>
          <span className="s-node-sub">
            Живёт на каждом хостинге · характер проще и легче
          </span>
        </div>
      </div>
      <p className="s-hint">
        Диалекты различаются, но таблицы, соединения, группировки и окна —
        везде.
      </p>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Миграции без остановки"
      sub="Расширение и сжатие"
      main="Один удар блокирует таблицу и кладёт прод. Миграции — код: история, ревью, откаты."
    >
      <div className="s-blocks">
        <div className="s-block">1 · Добавили колонку, допускающую пустоту</div>
        <div className="s-block">2 · Наполнили фоном, без блокировок</div>
        <div className="s-block">3 · Включили ограничение</div>
        <div className="s-block changed">
          4 · Убрали старое — каждый шаг обратим и безопасен на живой системе
        </div>
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Антипаттерны дня"
      sub="Как узнаётся плохой запрос"
      main="Базе — данные и связи; статике — объектное хранилище."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          mono
          title="SELECT *"
          sub="Все колонки, сломанные покрывающие индексы, лишний трафик"
        />
        <Node
          kind="amber"
          title="Спагетти-соединения"
          sub="Двадцать таблиц в одном запросе — разбейте на шаги"
        />
        <Node
          kind="amber"
          title="Логика в процедурах"
          sub="Тысяча строк, спрятанных от тестов и версионирования"
        />
        <Node
          kind="amber"
          title="Файлы в базе"
          sub="Двоичные колонки для статики — не место"
        />
      </div>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Практика на сегодня"
      sub="Четыре упражнения"
      main="Проверка миграций — первый долг, который стоит закрыть."
    >
      <div className="s-blocks">
        <div className="s-block">
          Найдите в своей схеме ячейки-списки: нарушение первой нормальной формы
        </div>
        <div className="s-block">
          Отчёт с группировкой: перепутайте WHERE и HAVING и посмотрите, как
          изменится результат
        </div>
        <div className="s-block">
          Топ продаж в каждой категории одним запросом — оконная функция
        </div>
        <div className="s-block changed">
          Проверьте миграции проекта: есть ли история и откат
        </div>
      </div>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Ограничения проверки"
      sub="CHECK — недооценённая возможность"
      main="Три строки в схеме заменяют сотни проверок в коде, которые кто-то забудет написать."
    >
      <Cmd>
        {
          "CHECK (price > 0)\nCHECK (quantity >= 0)\nCHECK (due_date > created_at)"
        }
      </Cmd>
      <div className="s-note">
        Проверяются на каждой строке, при каждой записи — и документируют:
        читать схему с ограничениями как договор, где обязательства выписаны
        явно.
      </div>
    </Slide>
  );
}

function S19() {
  return (
    <Slide
      n={19}
      title="Многие-ко-многим"
      sub="Связующая таблица"
      main="Не бойтесь связующих таблиц — бойтесь связей, закопанных в строку-список."
    >
      <div className="s-cols">
        <Node mono title="пользователь" />
        <Arr />
        <Node
          kind="green"
          mono
          title="подписка"
          sub="пара ключей + факты связи: дата, порядок"
        />
        <Arr />
        <Node mono title="курс" />
      </div>
      <p className="s-hint">
        Статья и тег, заказ и товар — везде одна и та же честная конструкция.
      </p>
    </Slide>
  );
}

function S20() {
  return (
    <Slide
      n={20}
      title="Читать чужую схему"
      sub="Отдельный навык"
      main="Схема — слепок представлений разработчиков о мире; хорошие схемы читаются как книги."
    >
      <div className="s-cols">
        <Node title="Таблица фактов" sub="Начните с неё" />
        <Arr />
        <Node title="Ключи" sub="Кто на кого ссылается" />
        <Arr />
        <Node kind="green" title="Связующие" sub="И предметная область ясна" />
      </div>
      <p className="s-hint">
        Быстрее, чем из документации: связи и приоритеты продукта видны прямо в
        структуре.
      </p>
    </Slide>
  );
}

function S21() {
  const topics = [
    ["▤", "Модель", "Таблицы, связи, декларативный язык"],
    ["Σ", "Группировки", "Схлопывают; окно сохраняет детали"],
    [
      "⌘",
      "Нормальные формы",
      "Факт в одном месте; денормализация — компромисс",
    ],
    ["▲", "Миграции", "Код: расширение и сжатие"],
  ];
  return (
    <Slide
      n={21}
      title="Итог"
      sub="Глава 1 · Модель данных и запросы"
      main="Дальше — транзакции и уровни изоляции: что происходит, когда два запроса пишут одно."
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
        Соединения умножают строки — агрегаты заранее; форма запроса важнее
        перестановки условий.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_D1 = {
  "9:1": [
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
    S17,
    S18,
    S19,
    S20,
    S21,
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D1).
export const SLIDE_TITLES_D1 = {
  "9:1": [
    "Введение",
    "История: Кодд, 1971",
    "Почему таблицы",
    "Нормальные формы",
    "Типы колонок",
    "Пустота NULL",
    "Ключи",
    "Служебные колонки",
    "Соединения",
    "Группировки",
    "Оконные функции",
    "CTE",
    "Форма запроса",
    "Postgres и MySQL",
    "Миграции",
    "Антипаттерны",
    "Практика",
    "CHECK-ограничения",
    "Многие-ко-многим",
    "Чтение схем",
    "Итог",
  ],
};
