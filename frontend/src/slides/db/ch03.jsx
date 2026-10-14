// Слайды для «Базы данных: под капотом», глава 3 — «Индексы: б-деревья, планы».
// Тот же дизайн-код, что и у других книг: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СКОРОСТЬ И ХРАНИЛИЩА / ГЛАВА 3</span>
      <span>{String(n).padStart(2, "0")} / 23</span>
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
    ["⌗", "Б-дерево", "Миллиард строк за считанные чтения"],
    ["⎔", "План", "EXPLAIN — правда о запросе"],
    ["▤", "Покрывающие", "Индекс содержит ответ"],
    ["✕", "Налог на запись", "Каждый индекс стоит вставок"],
  ];
  return (
    <Slide
      n={1}
      title="Индексы"
      sub="Глава 3 · Б-деревья, планы и покрывающие индексы"
      main="Запрос без индекса читает всю таблицу: сто строк — мгновение, миллиард — ночь."
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
      <p className="s-hint">После этой главы EXPLAIN перестанет пугать.</p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Б-дерево"
      sub="Рабочая лошадка индексов"
      main="Индекс — не ускоритель бесплатно, а обмен места и скорости записи на скорость чтения."
    >
      <div className="s-tree">
        <div className="s-cols">
          <Node mono title="[ 10 | 40 | 70 ]" sub="Корень · грубые границы" />
        </div>
        <Down />
        <div className="s-cols">
          <Node mono title="< 40" sub="Внутренняя страница" />
          <Node mono title="40–70" sub="Внутренняя страница" />
          <Node mono title="> 70" sub="Внутренняя страница" />
        </div>
        <Down />
        <div className="s-cols">
          <Node kind="green" mono title="лист: ключ → строка" sub="Точные значения, упорядочены" />
          <Node kind="green" mono title="лист: ключ → строка" sub="Диапазоны и сортировка — бесплатно" />
        </div>
      </div>
      <p className="s-hint">
        Высота обычно три-четыре уровня: поиск по миллиарду строк — считанные
        чтения страниц.
      </p>
    </Slide>
  );
}

function S03() {
  const rows = [
    ["Nested Loop", "Вложенные циклы — хороши на маленьких выборках"],
    ["Hash Join", "Хеширование — на больших несортированных"],
    ["Merge Join", "Слияние — на отсортированном"],
  ];
  return (
    <Slide
      n={3}
      title="План запроса"
      sub="Маршрут, который выбрал оптимизатор"
      main="Расхождение оценок с реальностью в тысячи раз — статистика устала, план плох. Обновление статистики — бесплатное лекарство от половины тормозов."
    >
      <Cmd>{"EXPLAIN ANALYZE\nSELECT … ;   — план плюс реальные строки, время, чтения"}</Cmd>
      <div className="s-table">
        {rows.map(([m, d]) => (
          <div key={m}>
            <span className="s-path accent">{m}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Кэш страниц"
      sub="Невидимый герой скорости"
      main="Если индексы влезают в память — скорость радует. Попадания ниже девяноста процентов — звонок."
    >
      <div className="s-bar-wrap">
        <span>Здоровая база · попадания в кэш</span>
        <div className="s-bar">
          <div style={{ width: "99%" }} />
        </div>
        <span>Тревога · каждая ходка на диск</span>
        <div className="s-bar amber">
          <div style={{ width: "70%" }} />
        </div>
      </div>
      <div className="s-grid2">
        <Node mono title="Память ≈ ×1000 дешевле диска" />
        <Node kind="green" title="Метрика попаданий" sub="Первая в утреннем осмотре базы" />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Составной индекс"
      sub="Порядок колонок критичен"
      main="Равенства впереди, диапазон последним — дерево упорядочено сначала по первой колонке."
    >
      <Cmd>{"CREATE INDEX ON orders (city, created_at);"}</Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          mono
          title="city = ? AND created_at > ?"
          sub="Город с диапазоном дат — работает"
        />
        <Node
          kind="amber"
          mono
          title="created_at > ? AND city IN (…)"
          sub="Дата с диапазоном городов — дерево не поможет"
        />
      </div>
      <p className="s-hint">
        Индексы с переставленными колонками «на всякий случай» — класс мусора,
        который тихо жрёт скорость записи.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Покрывающий индекс"
      sub="Вершина искусства"
      main="Для топ-запросов это самая выгодная сделка в базе данных."
    >
      <Cmd>{"CREATE INDEX ON orders (customer_id)\nINCLUDE (amount, status);   — ответ живёт в индексе"}</Cmd>
      <div className="s-cols">
        <Node kind="amber" mono title="тысячи чтений таблицы" />
        <Arr />
        <Node mono title="INCLUDE" sub="Лишняя колонка включением — дёшево" />
        <Arr />
        <Node kind="green" mono title="скан компактного индекса" sub="Ни одного похода к таблице" />
      </div>
      <p className="s-hint">Отчёты и горячие пути — главные кандидаты.</p>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Частичные и функциональные"
      sub="Меньше размер — быстрее полёт"
      main="Условие запроса и определение индекса должны совпадать буквально."
    >
      <Cmd>{"CREATE INDEX … ON tasks (due_at) WHERE status = 'new';\nCREATE INDEX … ON users (lower(email));"}</Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Частичный"
          sub="Только необработанные заказы, только активные — на порядки меньше. Классика очередей задач"
        />
        <Node
          kind="amber"
          title="Ловушка"
          sub="Условие по функции не берёт обычный индекс: план его не видит"
        />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Разбор от начала до конца"
      sub="Последние заказы клиента"
      main="Такой разбор стоит провести для пяти горячих запросов проекта — самая выгодная вечерняя работа инженера."
    >
      <div className="s-cols">
        <Node mono title="(customer_id, created_at)" sub="включённые: amount, status" />
        <Arr />
        <Node kind="green" title="План мечты" sub="Поиск по клиенту, десять последних записей индекса, ноль походов к таблице" />
      </div>
      <div className="s-table">
        <div>
          <span className="s-path accent">до</span>
          <span>скан всех заказов, сортировка — секунды</span>
        </div>
        <div>
          <span className="s-path accent">после</span>
          <span>миллисекунды, стабильные под нагрузкой</span>
        </div>
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Не всё — б-деревья"
      sub="Каждый тип закрывает свой класс запросов"
      main="Половина случаев решается б-деревом; узнавание остальных — то, что отличает сильного инженера."
    >
      <div className="s-grid2">
        <Node mono title="HASH" sub="Только равенство — зато константное" />
        <Node mono title="GIN / обратные" sub="Тексты, теги, массивы" />
        <Node mono title="BITMAP" sub="Пересечение множеств в аналитике" />
        <Node mono title="GiST / R-деревья" sub="Геоданные и близость" />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Сортировка и лимит"
      sub="Лучшие друзья индекса"
      main="Курсорный пейджинг по последнему ключу решает проблему OFFSET — привыкните к нему."
    >
      <div className="s-grid2">
        <Node
          kind="green"
          title="ORDER BY по индексу"
          sub="Уже упорядочен: сортировки нет, LIMIT читает первые страницы дерева"
        />
        <Node
          kind="amber"
          mono
          title="OFFSET 1000000"
          sub="База читает и выбрасывает всё до смещения"
        />
      </div>
      <Cmd>{"WHERE id > $last_seen ORDER BY id LIMIT 20;  — курсорный пейджинг"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Физический порядок строк"
      sub="Таблица, уложенная по индексу"
      main="Понимание физического порядка отличает настройку от гадания."
    >
      <div className="s-cols">
        <Node kind="green" title="Данные в порядке индекса" sub="Чтение диапазона — последовательные страницы, на порядок быстрее" />
        <Node
          kind="amber"
          title="Деградация — норма"
          sub="Новые строки падают в конец; планируйте переукладку как обслуживание"
        />
      </div>
      <p className="s-hint">
        Разовая операция укладки — долгий эффект для горячих отчётов.
      </p>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Индекс на внешнем ключе"
      sub="База не создаст его сама"
      main="Классика продакшена: удаление висит вечность — виной отсутствие индекса на ссылающейся колонке."
    >
      <div className="s-cols">
        <Node mono title="DELETE родителя" />
        <Arr />
        <Node kind="amber" title="Без индекса" sub="Проверка детей — полное сканирование" />
        <Arr />
        <Node kind="green" mono title="С индексом" sub="Мгновенно" />
      </div>
      <p className="s-hint">
        Простой скрипт проверки «внешний ключ есть — индекс есть» — разовая
        инвестиция на годы.
      </p>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Налог на запись"
      sub="Каждый индекс — дороже вставка"
      main="Баланс чтений и записей — суть настройки индексов, и она всегда конкретна к нагрузке."
    >
      <div className="s-bar-wrap">
        <span>Запись при 1 индексе</span>
        <div className="s-bar">
          <div style={{ width: "10%" }} />
        </div>
        <span>Запись при 10 индексах · обновляются все</span>
        <div className="s-bar amber">
          <div style={{ width: "100%" }} />
        </div>
      </div>
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Мёртвые индексы"
          sub="Видно в статистике использования; удалять аккуратно, с периодом наблюдения"
        />
        <Node
          title="Изменчивая колонка"
          sub="Индекс на ней — перемещение по дереву на каждую запись"
        />
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Индексы пухнут"
      sub="Мусор от обновлений и удалений"
      main="Не перестраивайте по расписанию всё подряд: смотрите на метрики и лечите больных, а не всех."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Симптомы"
          sub="Размер в разы больше логического объёма, падение эффективности чтений"
        />
        <Node
          kind="green"
          mono
          title="REINDEX CONCURRENTLY"
          sub="Свежее компактное дерево без остановки сервиса"
        />
      </div>
      <p className="s-hint">
        Дерево редеет, чтения растягиваются — это лечится, но по показаниям.
      </p>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Наблюдение"
      sub="Журнал медленных запросов"
      main="Производительность базы — не разовый проект, а постоянный диалог с числами."
    >
      <div className="s-cols">
        <Node mono title="порог · сотни мс" />
        <Arr />
        <Node title="Разбор худших за неделю" sub="Агрегация по форме запроса, не по параметрам" />
        <Arr />
        <Node kind="green" title="Трекинг планов" sub="Ловит деградацию до пользователей" />
      </div>
      <p className="s-hint">
        Одинаковый шаблон с разными значениями — одна болезнь: лечится один
        раз.
      </p>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Антипаттерны"
      sub="И в ту, и в другую сторону"
      main="Мера в цифрах, а не в страхах."
    >
      <div className="s-blocks">
        <div className="s-block">
          Индекс на каждую колонку «на всякий случай» — налог на запись;
          используемых — четверть
        </div>
        <div className="s-block">
          Индексы до профилирования: сначала EXPLAIN, потом решение
        </div>
        <div className="s-block">
          Слепое добавление по совету из интернета, без понимания запроса
        </div>
        <div className="s-block changed">
          Страх перед индексами: горячий путь без индекса жрёт диск и кэш
        </div>
      </div>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Практика"
      sub="Четыре упражнения"
      main="Частичный индекс на состоянии очереди уменьшается в десятки раз — приятно наблюдать."
    >
      <div className="s-blocks">
        <div className="s-block">
          Медленный запрос проекта: посмотрите план с анализом
        </div>
        <div className="s-block">
          Найдите сканирование, добавьте индекс, сравните планы
        </div>
        <div className="s-block">
          Статистика использования индексов: найдите мёртвые
        </div>
        <div className="s-block changed">
          Частичный индекс на состоянии очереди задач
        </div>
      </div>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Статистика"
      sub="Глаза оптимизатора"
      main="Обновление сводки после больших загрузок — плановая работа, а не шаманство."
    >
      <div className="s-grid2">
        <Node
          title="Что в сводке"
          sub="Сколько строк, сколько разных значений, как распределены — из этого оценка выборки"
        />
        <Node
          kind="green"
          title="Оценка → метод"
          sub="Циклы для десяти строк, хеш для миллионов"
        />
      </div>
      <div className="s-note amber">
        Асимметрия: девяносто девять процентов строк одного вида — обычная
        сводка врёт. Есть расширенная статистика по комбинациям колонок.
      </div>
    </Slide>
  );
}

function S19() {
  return (
    <Slide
      n={19}
      title="Почему индекс не взят"
      sub="Даже при точном совпадении колонок"
      main="План честно скажет, что использовал и почему: минута чтения вместо недель гаданий."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Малая выгода"
          sub="Запрос вернёт половину таблицы — скан быстрее дерева"
        />
        <Node
          kind="amber"
          title="Типы не совпали"
          sub="Колонка одного типа, условие другого — индекс мёртв, хотя на вид всё правильно"
        />
      </div>
      <p className="s-hint">Обе причины видны только в плане запроса.</p>
    </Slide>
  );
}

function S20() {
  return (
    <Slide
      n={20}
      title="Выражения в реальной жизни"
      sub="Индекс и запрос — дословно"
      main="С половины ускорений поиска команда знакомится с функциональными индексами."
    >
      <Cmd>{"CREATE INDEX ON users (lower(email));\nSELECT … WHERE lower(email) = lower($1);\n\nCREATE INDEX ON events ((ts::date));\nSELECT … WHERE ts::date = '2026-10-14';"}</Cmd>
      <p className="s-hint">
        Поиск без учёта регистра, дата из отметки времени — правило одно:
        выражение в индексе и в запросе совпадает дословно.
      </p>
    </Slide>
  );
}

function S21() {
  return (
    <Slide
      n={21}
      title="Индексы и массовая загрузка"
      sub="Приём зрелых инженеров"
      main="На больших объёмах — разница между часами и сутками. Пригодится на первой же миграции."
    >
      <div className="s-blocks">
        <div className="s-block">1 · Снимаем лишние индексы</div>
        <div className="s-block">2 · Заливаем данные без десяти медленных деревьев</div>
        <div className="s-block changed">
          3 · Строим индексы заново одним проходом
        </div>
      </div>
      <p className="s-hint">
        Загрузка с десятью индексами — десять обновлений дерева на каждую
        партию.
      </p>
    </Slide>
  );
}

function S22() {
  return (
    <Slide
      n={22}
      title="Индексы живут в кэше"
      sub="Связь со следующей главой"
      main="Индексы проектируются, а не копятся: каждый лишний мегабайт конкурирует с данными за память."
    >
      <div className="s-grid2">
        <Node
          kind="green"
          title="Узкий и горячий"
          sub="Целиком помещается в кэш — ускоряет запросы на порядки"
        />
        <Node
          kind="amber"
          title="Раздутый"
          sub="Вымывается из памяти — выгоды испаряются"
        />
      </div>
      <p className="s-hint">
        Индексы лежат на диске страницами и читаются через тот же кэш, что и
        данные.
      </p>
    </Slide>
  );
}

function S23() {
  const topics = [
    ["⌗", "Б-дерево", "Равенства, диапазоны, сортировки"],
    ["⎔", "План", "Оценки против реальности"],
    ["▤", "Покрывающие", "Ноль походов к таблице"],
    ["✕", "Налог", "Мёртвые индексы — удалять"],
  ];
  return (
    <Slide
      n={23}
      title="Итог"
      sub="Глава 3 · Индексы"
      main="Дальше — как данные физически лежат на диске и почему базы делятся на два лагеря хранилищ."
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
        Составные — под запросы, частичные режут размер, функциональные
        обслуживают выражения.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_D3 = {
  "9:3": [
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
    S22,
    S23,
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D3).
export const SLIDE_TITLES_D3 = {
  "9:3": [
    "Введение",
    "Б-дерево",
    "План запроса",
    "Кэш страниц",
    "Составной индекс",
    "Покрывающий индекс",
    "Частичные и функциональные",
    "Разбор примера",
    "Другие типы",
    "Сортировка и лимит",
    "Физический порядок",
    "Индекс на внешнем ключе",
    "Налог на запись",
    "Распухание",
    "Наблюдение",
    "Антипаттерны",
    "Практика",
    "Статистика",
    "Почему не взят",
    "Выражения в жизни",
    "Массовая загрузка",
    "Индексы и кэш",
    "Итог",
  ],
};
