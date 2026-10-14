// Слайды для «Базы данных: под капотом», глава 2 — «Транзакции и уровни изоляции».
// Тот же дизайн-код, что и у других книг: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>МОДЕЛЬ И НАДЁЖНОСТЬ / ГЛАВА 2</span>
      <span>{String(n).padStart(2, "0")} / 22</span>
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
    ["A", "Кислотность", "Всё или ничего: контракт базы"],
    ["≠", "Аномалии", "Грязь, фантомы, потерянные обновления"],
    ["▦", "Уровни", "Договор о том, что видно соседям"],
    ["↻", "Повторы", "Конфликт — не ошибка, а рутина"],
  ];
  return (
    <Slide
      n={1}
      title="Транзакции и уровни изоляции"
      sub="Глава 2 · Что видно одному запросу, пока другой не закончился"
      main="Глава, после которой многие продакшен-баги становятся прозрачными."
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
        Перевод денег не должен оставлять мир в состоянии между шагами.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="ACID"
      sub="Четыре слова одного контракта"
      main="Четыре свойства — контракт, который база даёт вам."
    >
      <div className="s-cols">
        <Node kind="green" mono title="A" sub="Атомарность: всё или ничего" />
        <Node
          mono
          title="C"
          sub="Согласованность: из корректного в корректное"
        />
        <Node mono title="I" sub="Изолированность: соседи не мешают" />
        <Node
          mono
          title="D"
          sub="Долговечность: переживает отключение питания"
        />
      </div>
      <p className="s-hint">
        За долговечность стоит журнал опережающей записи — о нём, в четвёртой
        главе.
      </p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Начать, сделать, подтвердить"
      sub="BEGIN · COMMIT · ROLLBACK"
      main="Транзакция короткая, как выдох; сеть и почта — за её пределами: чужие системы база не откатит."
    >
      <Cmd>
        {
          "BEGIN;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nUPDATE accounts SET balance = balance + 100 WHERE id = 2;\nCOMMIT;   -- или ROLLBACK;"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Откат"
          sub="Ошиблись в середине массового изменения — откатитесь, а не чините вторым запросом"
        />
        <Node
          kind="amber"
          title="Долгая транзакция"
          sub="Держит версии строк, мешает очистке, в худшем случае блокирует всё"
        />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Физика подтверждения"
      sub="Журнал должен пережить диск"
      main="Скорость записи журнала — часто главный потолок базы. Проверьте его раньше, чем покупать процессоры."
    >
      <div className="s-cols">
        <Node mono title="COMMIT ×1" />
        <Arr />
        <Node
          kind="amber"
          title="Каждая — своя запись на диск"
          sub="Миллион вставок по одной — самоубийство"
        />
        <Node
          kind="green"
          title="Групповое"
          sub="Партии по тысяче: задержка чуть выше, пропускная способность в разы"
        />
      </div>
      <div className="s-note">
        Подтверждение ждёт, пока журнал переживёт запись на диск, — это цена
        долговечности, платится на каждом подтверждении.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Блокировки"
      sub="Механика параллельности"
      main="Одинаковый порядок доступа к ресурсам во всём коде — единственный способ уменьшить дедлоки."
    >
      <div className="s-cols">
        <Node mono title="S + S" kind="green" sub="Два чтения мирятся" />
        <Node kind="amber" mono title="S + X" sub="Конфликт" />
        <Node kind="amber" mono title="X + X" sub="Конфликт" />
      </div>
      <div className="s-cols">
        <Node
          kind="amber"
          title="Дедлок"
          sub="Первая ждёт вторую, вторая первую — база находит цикл и убивает жертву. Это не баг, а спасение"
        />
        <Node
          kind="green"
          title="Мониторинг"
          sub="Очередь из сотен запросов за одной строкой — счётчик горячего ключа"
        />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Аномалии параллельности"
      sub="Что происходит без изоляции"
      main="Каждая аномалия — класс продакшен-бага, узнаваемый в коде."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Грязное чтение"
          sub="Увидеть чужие незаконченные изменения, которые откатятся"
        />
        <Node
          kind="amber"
          title="Неповторяющееся чтение"
          sub="Та же строка дважды в одной транзакции — разные значения"
        />
        <Node
          kind="amber"
          title="Фантомы"
          sub="Список дважды — разное количество строк"
        />
        <Node
          kind="amber"
          title="Потерянное обновление"
          sub="Оба прочитали, оба записали — вторая запись молча затёрла первую"
        />
      </div>
    </Slide>
  );
}

function S07() {
  const rows = [
    ["READ UNCOMMITTED", "Грязное чтение возможно — почти никто не использует"],
    ["READ COMMITTED", "Только завершённые изменения; дефолт большинства баз"],
    [
      "REPEATABLE READ",
      "Строки стабильны внутри транзакции; фантомы — от реализации",
    ],
    ["SERIALIZABLE", "Как будто транзакции шли по одной: медленнее, но честно"],
  ];
  return (
    <Slide
      n={7}
      title="Уровни изоляции"
      sub="Договор: какие аномалии вы терпите ради скорости"
      main="Повышайте уровень осознанно и локально: финансовый расчёт — сериализуемый, счётчик лайков — не стоит и транзакции."
    >
      <div className="s-table">
        {rows.map(([lvl, d]) => (
          <div key={lvl}>
            <span className="s-path accent">{lvl}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Базы трактуют по-разному"
      sub="Одно имя — разные обещания"
      main="Прочитайте главу документации об изоляции именно вашей базы: одна страница стоит недель отладки."
    >
      <div className="s-grid2">
        <Node
          kind="green"
          title="Снимки"
          sub="Повторяемое чтение — настоящие снимки с защитой от фантомов на диапазонах"
        />
        <Node
          kind="amber"
          title="Блокировки строк"
          sub="То же имя — просто блокировки прочитанного"
        />
      </div>
      <div className="s-note">
        Дефолты различаются: где-то чтение подтверждённое, где-то повторяемое.
        Не переносите привычки между базами вслепую.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Версии строк"
      sub="Как изоляция устроена под капотом"
      main="Цена мультиверсионности — мусор: очистку лучше не злить длинными транзакциями."
    >
      <Node mono title="Транзакция стартует" />
      <Down />
      <Node
        kind="green"
        title="Снимок"
        sub="Видит базу на момент старта; чужие незавершённые изменения невидимы"
      />
      <Down />
      <Node mono title="Читатели ≠ блокируют писателей" />
      <div className="s-note amber">
        Старые версии убирает фоновая очистка. Транзакция, держащая старый
        снимок часами, оставляет мусор жить.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Сериализуемость"
      sub="Честность дороже снимков"
      main="Сериализуемый — для узких критичных путей, а не для всего каталога. И всегда с повторами."
    >
      <div className="s-cols">
        <Node mono title="Я прочитала твоё изменение" />
        <Arr />
        <Node
          kind="amber"
          title="Зависимость"
          sub="Кто-то из нас повторит транзакцию"
        />
        <Arr />
        <Node
          kind="green"
          mono
          title="Повтор"
          sub="Цена честности под нагрузкой"
        />
      </div>
      <p className="s-hint">
        Движки ловят конфликты предикатными блокировками или отслеживанием пар
        чтение-запись. Без повторов вы увидите не честность, а ошибки.
      </p>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Практические сценарии"
      sub="Остатки, счётчики, уникальность"
      main="Идемпотентность повторов — ключ к спокойному сну: повтор запроса не удваивает эффект."
    >
      <Cmd>
        {
          "UPDATE inventory SET qty = qty - 1\nWHERE id = 42 AND qty > 0;   — проверка затронутых строк"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          mono
          title="qty = qty - 1"
          sub="Атомарный прирост вместо чтения-правки-записи"
        />
        <Node
          kind="amber"
          title="Две вставки одной почты"
          sub="Ограничение уникальности ловит второго — конфликт обрабатывайте штатно"
        />
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Повторить и сдаться красиво"
      sub="Конфликт — часть договора"
      main="Транзакция, падающая без повтора на проде, — источник редких и ядовитых багов."
    >
      <div className="s-cols">
        <Node kind="amber" mono title="дедлок / конфликт" />
        <Arr />
        <Node mono title="короткая пауза" />
        <Arr />
        <Node mono title="вторая попытка" />
        <Arr />
        <Node
          kind="green"
          title="N попыток → сдаться"
          sub="Красиво и с логом"
        />
      </div>
      <div className="s-note">
        Библиотеки доступа к данным умеют повторы из коробки — проверьте, что
        ваша умеет.
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Точки сохранения"
      sub="Частичный откат внутри транзакции"
      main="Подтверждение — точка невозврата: после него только компенсации. Подтверждайте, когда всё проверено."
    >
      <Cmd>
        {
          "SAVEPOINT дорогой_шаг;\nROLLBACK TO дорогой_шаг;   — попробовать другой путь"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Гибкость за копейки"
          sub="Вложенные операции: не вышло — откатились к точке и пошли иначе"
        />
        <Node
          kind="amber"
          title="После COMMIT"
          sub="Отменить нельзя — только компенсирующая операция"
        />
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Согласованность — в базе"
      sub="Не в надежде на код"
      main="База без ограничений — это файл с индексами."
    >
      <div className="s-opts">
        <span className="s-path accent">NOT NULL</span>
        <span className="s-path accent">UNIQUE</span>
        <span className="s-path accent">FOREIGN KEY</span>
        <span className="s-path accent">CHECK</span>
        <span>исполняются мгновенно и без исключений на пути</span>
      </div>
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Приложение"
          sub="Может забыть; другой сервис — не знать; ручная правка — пролететь мимо"
        />
        <Node
          kind="green"
          title="База"
          sub="Не может: ограничение обязано. Отключение на миграции — событие с предупреждением и возвратом"
        />
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Откладываемые ограничения"
      sub="Проверка в конце, а не на каждом шаге"
      main="Знайте приём, но пользуйтесь редко: отключать ограничения навсегда — в сто раз хуже отложенной проверки."
    >
      <Cmd>
        {
          "SET CONSTRAINTS accounts_fk DEFERRED;\nUPDATE accounts SET id = 5 WHERE id = 1;  — ссылка «висит»\nUPDATE orders  SET account_id = 5;\nCOMMIT;   — здесь обе проверки пройдены"
        }
      </Cmd>
      <p className="s-hint">
        Перенос между счетами логично меняет ссылки и нарушает ограничение в
        середине — отложенная проверка это разрешает, оставаясь честной.
      </p>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="История из жизни"
      sub="Отчёт, который съел диск"
      main="Транзакция — не обёртка для удобства, а договор с базой о ресурсах."
    >
      <div className="s-blocks">
        <div className="s-block">
          Отчёт для руководства бежал три часа в транзакции повторяемого чтения
        </div>
        <div className="s-block">
          Снимок держался — очистка не могла убрать миллиарды мёртвых версий
        </div>
        <div className="s-block">
          Таблица распухла в десять раз, ночью кончился диск
        </div>
        <div className="s-block changed">
          Лечение: отчёты на реплику, короткие транзакции, лимиты на время
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
      sub="Увидеть аномалию руками"
      main="Один раз увидев потерянное обновление, вы будете узнавать его в коде мгновенно."
    >
      <div className="s-blocks">
        <div className="s-block">
          Два окна базы: воспроизведите потерянное обновление на тестовой
          таблице
        </div>
        <div className="s-block">
          Поднимите уровень изоляции — попробуйте снова
        </div>
        <div className="s-block">
          Найдите в коде чтение-правку-запись, замените атомарным приростом
        </div>
        <div className="s-block changed">
          Проверьте, что библиотека повторяет транзакции при конфликте
        </div>
      </div>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Уровень по умолчанию"
      sub="Жёсткость локально, скорость везде"
      main="Локальность — ключ к производительности: жёсткость там, где нужна, скорость везде."
    >
      <div className="s-grid2">
        <Node
          kind="green"
          title="Поднять локально"
          sub="Отчёт, сверка, миграция — в транзакции с нужным уровнем, явно"
        />
        <Node
          kind="amber"
          title="Поднять глобально"
          sub="Быстрые операции превращаются в очередь"
        />
      </div>
      <p className="s-hint">
        Если дефолт — чтение подтверждённое, каждое место, где важна
        стабильность чтения, обязано поднимать уровень само.
      </p>
    </Slide>
  );
}

function S19() {
  return (
    <Slide
      n={19}
      title="Тестирование параллельности"
      sub="Его не делают почти никогда"
      main="Инварианты — лучший друг: их нарушение ловит и аномалии, и баги кода, и чужие ручные правки."
    >
      <div className="s-grid2">
        <Node
          title="Умный способ"
          sub="Два подключения в тесте, синхронизация через точки, гонка по расписанию"
        />
        <Node
          kind="green"
          title="Простой способ"
          sub="Генератор нагрузки + проверка инвариантов после"
        />
      </div>
      <p className="s-hint">
        Инварианты: остаток на складе не отрицательный, сумма переводов не
        изменилась.
      </p>
    </Slide>
  );
}

function S20() {
  return (
    <Slide
      n={20}
      title="Тайм-ауты"
      sub="У каждого ожидания — предел"
      main="Честная ошибка через две секунды лучше зависания на пять минут."
    >
      <div className="s-opts">
        <span className="s-path accent">lock_timeout</span>
        <span>ожидание блокировки</span>
        <span className="s-path accent">idle_in_transaction</span>
        <span>время жизни транзакции</span>
        <span className="s-path accent">connect_timeout</span>
        <span>простой соединения</span>
      </div>
      <div className="s-note amber">
        Бесконечное ожидание — источник каскадных заторов: одна застрявшая
        транзакция останавливает половину системы.
      </div>
    </Slide>
  );
}

function S21() {
  return (
    <Slide
      n={21}
      title="Вопрос для интуиции"
      sub="Задавайте про любой кусок кода"
      main="Эта привычка ловит больше багов параллельности, чем любой анализатор."
    >
      <Cmd>
        {
          "Что произойдёт, если между двумя его шагами\nвклинится чужая транзакция?"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Ничего страшного"
          sub="Уровень по умолчанию вам подходит"
        />
        <Node
          kind="amber"
          title="Деньги пропадут, товар продастся дважды"
          sub="Явный уровень, условное обновление или уникальное ограничение"
        />
      </div>
    </Slide>
  );
}

function S22() {
  const topics = [
    ["A", "Кислотность", "Четыре буквы — контракт базы"],
    ["≠", "Аномалии", "Грязь, фантомы, потерянные — узнаваемы"],
    ["▦", "Версии строк", "Читатели не мешают писателям"],
    ["↻", "Повторы", "Часть договора; идемпотентность — добродетель"],
  ];
  return (
    <Slide
      n={22}
      title="Итог"
      sub="Глава 2 · Транзакции и уровни изоляции"
      main="Дальше — индексы: почему одни запросы мгновенны, а другие листают миллиард строк."
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
        Мусор убирает очистка, которую нельзя злить долгими транзакциями.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_D2 = {
  "9:2": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D2).
export const SLIDE_TITLES_D2 = {
  "9:2": [
    "Введение",
    "ACID",
    "BEGIN и ROLLBACK",
    "Физика подтверждения",
    "Блокировки",
    "Аномалии",
    "Уровни изоляции",
    "Разные трактовки",
    "Версии строк",
    "Сериализуемость",
    "Сценарии",
    "Повторы",
    "Точки сохранения",
    "Ограничения",
    "Отложенные ограничения",
    "История из жизни",
    "Практика",
    "Уровень по умолчанию",
    "Тесты параллельности",
    "Тайм-ауты",
    "Вопрос интуиции",
    "Итог",
  ],
};
