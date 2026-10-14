// Слайды для «Linux: от шелла до ядра», глава 4 — «Процессы и сигналы: как живёт и умирает программа».
// Тот же дизайн-код, что и глава 2: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ПРАВА, ПРОЦЕССЫ, СЛУЖБЫ / ГЛАВА 4</span>
      <span>{String(n).padStart(2, "0")} / 19</span>
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
    ["PID", "Процессы", "Программа, которой ядро выдало память и жизнь"],
    ["ps", "Наблюдение", "Снимок, живой режим и средняя загрузка"],
    ["TERM", "Сигналы", "Вежливая просьба и последний аргумент"],
    ["Z", "Состояния", "От сна до зомби и непрерываемого ожидания"],
  ];
  return (
    <Slide
      n={1}
      title="Процессы и сигналы: как живёт и умирает программа"
      sub="Глава 4 · Жизненный цикл процесса"
      main="Глава с самой высокой отдачей: диагностика, утечки памяти и корректный перезапуск живут здесь."
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
        Программа на диске — мёртвый текст; процесс — программа, получившая
        ресурсы от ядра.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Рождение: fork и exec"
      sub="Копия, подменяющая себя новой программой"
      main="Родитель обязан забрать код возврата ребёнка — иначе остаётся зомби."
    >
      <div className="s-cols">
        <Node mono title="шелл" />
        <Arr />
        <Node mono title="fork" sub="копия себя" />
        <Arr />
        <Node mono title="exec" sub="подмена новой программой" />
      </div>
      <div className="s-cols">
        <Node mono title="exit" sub="ребёнок умирает" />
        <Arr />
        <Node
          kind="green"
          title="Код забран"
          sub="Запись в таблице процессов свободна"
        />
        <Node
          kind="amber"
          title="Код забрать некому"
          sub="Зомби — мёртвая запись, которую некому убрать"
        />
      </div>
      <p className="s-hint">
        У каждого процесса есть PID и родитель; сирот усыновляет первый процесс
        системы.
      </p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Зоопарк: ps, top и средняя загрузка"
      sub="Снимок и живой режим"
      main="Пятнадцатиминутное число важнее минутного: минутное шумит, длинное говорит правду."
    >
      <div className="s-grid2">
        <Node
          mono
          title="ps"
          sub="Снимок: владельцы, процессор, память, время старта, командная строка"
        />
        <Node
          mono
          title="top · htop"
          sub="Живой режим: сортировка по ресурсам, поиск, обновление"
        />
      </div>
      <div className="s-bar-wrap">
        <span>Средняя загрузка: очередь к процессору за 1, 5 и 15 минут</span>
        <div className="s-bar">
          <div style={{ width: "70%" }} />
        </div>
        <span>Число на уровне количества ядер — норма</span>
        <div className="s-bar">
          <div style={{ width: "40%" }} />
        </div>
        <span>Вдвое больше ядер — процессор не справляется</span>
        <div className="s-bar amber">
          <div style={{ width: "100%" }} />
        </div>
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Состояния процессов"
      sub="Половина диагностики живёт в них"
      main="Много непрерываемого сна — у вас проблемы с хранилищем, а не с процессами."
    >
      <div className="s-grid2">
        <Node kind="green" mono title="R · работающий" sub="Ест процессор" />
        <Node
          mono
          title="S · спящий"
          sub="Ждёт событие — таких всегда большинство"
        />
        <Node
          kind="amber"
          mono
          title="D · непрерываемый сон"
          sub="Ждёт диск или сеть; не убивается даже самым жёстким сигналом"
        />
        <Node
          kind="amber"
          mono
          title="Z · зомби"
          sub="Мёртвый ребёнок: код возврата никто не забрал"
        />
      </div>
      <p className="s-hint">
        Зомби не едят ни памяти, ни процессора — только строчку в таблице; их
        скопление говорит, что родитель забыл собирать детей.
      </p>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Рентген: /proc и открытые файлы"
      sub="Контекст процесса подсматривается в файловой системе"
      main="«Файл занят другим процессом» решается за секунды, когда видно, кто его держит."
    >
      <div className="s-opts">
        <span className="s-path accent">/proc/PID/cwd</span>
        <span>текущий каталог</span>
        <span className="s-path accent">/proc/PID/environ</span>
        <span>окружение</span>
        <span className="s-path accent">/proc/PID/fd</span>
        <span>открытые файлы</span>
      </div>
      <div className="s-grid2">
        <Node
          title="Какой конфиг реально читает процесс"
          sub="Окружение и текущий каталог отвечают сразу"
        />
        <Node
          title="С кем процесс разговаривает по сети"
          sub="Его соединения видны в его же каталоге"
        />
      </div>
      <p className="s-hint">
        Список открытых файлов конкретного процесса — любимый инструмент
        администратора.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Окружение: наследие родителя"
      sub="Каждый процесс получает копию окружения"
      main="Секреты в окружении видны потомкам и подсматриваются через /proc."
    >
      <div className="s-opts">
        <span className="s-path accent">PATH</span>
        <span>где искать программы</span>
        <span className="s-path accent">LANG</span>
        <span>язык и локаль</span>
        <span className="s-path accent">HOME</span>
        <span>домашний каталог</span>
      </div>
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Служба стартует не из вашего шелла"
          sub="Минимальное окружение: надежда на ваши переменные — источник падений на сервере при идеальной работе на ноутбуке"
        />
        <Node
          title="Окружение — договор между процессами"
          sub="Передаётся копией; стоит знать его текст"
        />
      </div>
      <div className="s-note">
        Для настоящих секретов существуют специальные хранилища, а не окружение.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Процессорные и вводо-выводные"
      sub="Первое действие — определить тип страдающего"
      main="Апгрейд процессора не ускоряет сервис, который ждал диск."
    >
      <div className="s-cols">
        <Node
          kind="green"
          title="Процессорный"
          sub="Всегда мало процессора — смотреть, что тяжёлого в коде"
        />
        <Node
          title="Вводо-выводный"
          sub="Всегда мало диска и сети — смотреть на ожидание"
        />
      </div>
      <div className="s-cols">
        <Node mono title="индексы" />
        <Arr />
        <Node mono title="кэш" />
        <Arr />
        <Node mono title="быстрое хранилище" />
      </div>
      <div className="s-note">
        Ошибочная диагностика даёт курьёзы: уменьшение тайм-аутов не лечит
        медленную сеть.
      </div>
    </Slide>
  );
}

function S08() {
  const rows = [
    ["SIGTERM", "Вежливая просьба завершиться: время сохранить данные"],
    ["SIGINT", "То, что посылает Ctrl+C в терминале"],
    ["SIGHUP", "Обрыв связи, ставший конвенцией «перечитай конфиг»"],
    ["SIGKILL", "Приказ смерти без переговоров: перехватить невозможно"],
  ];
  return (
    <Slide
      n={8}
      title="Сигналы: почта ядра"
      sub="Асинхронное уведомление с именем и судьбой"
      main="У каждого сигнала судьба: реакция по умолчанию, игнор или собственный обработчик."
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
        Многие сервисы умеют применять настройки по SIGHUP без перезапуска.
      </p>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="kill не убивает — посылает сигнал"
      sub="Убийство лишь частный случай"
      main="Сначала SIGTERM и пауза; SIGKILL — только если не помогло."
    >
      <Cmd>
        {
          "kill -TERM 1234      # вежливая просьба\nkill -9 1234         # смерть без переговоров\npgrep имя · pkill имя   # найти и послать по имени"
        }
      </Cmd>
      <div className="s-cols">
        <Node kind="green" mono title="SIGTERM" sub="Дать время попрощаться" />
        <Arr />
        <Node
          kind="amber"
          mono
          title="SIGKILL"
          sub="Файлы не дописаны, блокировки не сняты"
        />
      </div>
      <div className="s-note">
        Жёсткое убийство сходу — снос дома вместе с жильцами: база переживает
        внезапную смерть благодаря журналу, но платит долгим восстановлением.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Остановка сервиса по уму"
      sub="Вежливость всегда дешевле"
      main="Тайм-аут по умолчанию часто короче, чем приложение прощается, — настройте его."
    >
      <div className="s-cols">
        <Node kind="green" mono title="SIGTERM" />
        <Arr />
        <Node mono title="тайм-аут на прощание" />
        <Arr />
        <Node kind="amber" mono title="SIGKILL" sub="только если время вышло" />
      </div>
      <div className="s-note amber">
        Сервис с длинными фоновыми задачами убивали жёстко по расписанию и
        недоумевали о битых файлах — лечилось увеличением тайм-аута и честной
        обработкой SIGTERM в коде.
      </div>
      <p className="s-hint">
        За вас это делает система инициализации и оркестраторы, но механику
        понимать нужно.
      </p>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Пауза, фон и nohup"
      sub="Шелл управляет задачами"
      main="Фоновый процесс умирает при закрытии терминала — его спасает nohup."
    >
      <div className="s-opts">
        <span className="s-path accent">Ctrl+Z</span>
        <span>пауза</span>
        <span className="s-path accent">bg</span>
        <span>продолжить в фоне</span>
        <span className="s-path accent">jobs</span>
        <span>список задач</span>
        <span className="s-path accent">fg</span>
        <span>вернуть на передний план</span>
      </div>
      <Cmd>{"nohup долгая-команда > out.log 2>&1 &"}</Cmd>
      <div className="s-note amber">
        При закрытии терминала фоновая задача получает SIGHUP — тот самый сигнал
        обрыва связи.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Группы процессов"
      sub="Сигнал можно послать всей группе сразу"
      main="Убили только голову конвейера — хвост остался висеть и держать файлы."
    >
      <div className="s-cols">
        <Node mono title="конвейер" sub="команда · команда · команда" />
        <Arr />
        <Node title="Сигнал группе" sub="Его получает каждая команда цепочки" />
      </div>
      <Cmd>{"kill -- -PGID   # минус перед номером = всей группе"}</Cmd>
      <div className="s-note">
        Система инициализации останавливает целые группы и не оставляет сирот,
        держащих порты и файлы, — ещё одна причина доверять ей остановку
        сервисов.
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Приоритеты: nice и renice"
      sub="Вежливый процесс уступает процессор соседям"
      main="Приоритет — не магия распределения, а вес в очереди; для сглаживания пиков его хватает."
    >
      <div className="s-grid2">
        <Node
          mono
          title="nice -n 10 задача"
          sub="Запуск с пониженной вежливостью"
        />
        <Node
          mono
          title="renice"
          sub="Перенос живого процесса на другой приоритет"
        />
      </div>
      <div className="s-blocks">
        <div className="s-block">
          Ночная выгрузка, которая не должна мешать днём
        </div>
        <div className="s-block">
          Индексация, которую можно тормозить в часы пик
        </div>
        <div className="s-block changed">
          Архивация на слабой машине рядом с живым сервисом
        </div>
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Внезапная смерть: OOM-killer"
      sub="Память кончилась совсем — стреляет ядро"
      main="Сообщение об этом живёт в журнале ядра, а не в логах приложения."
    >
      <Node
        kind="amber"
        title="Память системы кончилась"
        sub="Включается убийца"
      />
      <Down />
      <Node title="Жертва по эвристике" sub="Кого выбрать — решает ядро" />
      <Down />
      <Node
        kind="amber"
        mono
        title="SIGKILL"
        sub="Машину спасли, процесс — нет"
      />
      <p className="s-hint">
        Не перезапускать, а понять, почему сервис съел всю память: утечка,
        необрезанный запрос, слишком большой батч — и ограничить ему память,
        чтобы падал только он.
      </p>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Перехват: trap в скриптах"
      sub="При сигнале — убери за собой и выйди мирно"
      main="Скрипт с честной очисткой — мелочь, отличающая инженера от пользователя."
    >
      <Cmd>{"trap 'rm -rf \"$TMPDIR\"; exit 0' TERM INT"}</Cmd>
      <div className="s-grid2">
        <Node
          title="Временный каталог"
          sub="Удаляется, даже если задачу оборвали по кнопке"
        />
        <Node
          title="Блокировка"
          sub="Снимается честно, а не остаётся висеть навсегда"
        />
      </div>
      <p className="s-hint">
        Проверьте себя: напишите скрипт с очисткой, оборвите Ctrl+C и убедитесь,
        что мусор убран.
      </p>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Практика на сегодня"
      sub="Четыре упражнения"
      main="Скрипт, раз в минуту пишущий среднюю загрузку, — график без системы мониторинга."
    >
      <div className="s-blocks">
        <div className="s-block">
          Открыть htop: найти три самых прожорливых процесса, разобраться, что
          это и кем порождены
        </div>
        <div className="s-block">
          Долгую команду — на паузу, потом в фон, найти в списке задач и
          завершить вежливым SIGTERM
        </div>
        <div className="s-block">
          Послать любому своему процессу SIGHUP и проверить по логам, перечитал
          ли он конфиг
        </div>
        <div className="s-block changed">
          Скрипт, который раз в минуту пишет среднюю загрузку в файл, — через
          неделю у вас будет график
        </div>
      </div>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Демоны"
      sub="Процессы, живущие без терминала"
      main="Современная система инициализации делает демоном обычную программу."
    >
      <div className="s-cols">
        <Node
          kind="amber"
          title="Старый ритуал"
          sub="Отключиться от терминала, отвязать сеанс, перенаправить потоки, сменить каталог"
        />
        <Arr />
        <Node
          kind="green"
          title="Сегодня"
          sub="Вы пишете обычную программу — демоном её делает система инициализации"
        />
      </div>
      <p className="s-hint">
        Поэтому демон не пишет на терминал: его вход и выход — файлы, а дом —
        корень дерева каталогов.
      </p>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Коды возврата"
      sub="Язык вежливости между программами"
      main="Ноль при неудаче — предательство: скрипт продолжит работу в разбитом состоянии."
    >
      <div className="s-cols">
        <Node kind="green" mono title="0" sub="успех" />
        <Arr />
        <Node
          kind="amber"
          mono
          title="не 0"
          sub="провал — и вся автоматизация это видит"
        />
      </div>
      <Cmd>{"команда && следующая   ·   echo $?"}</Cmd>
      <div className="s-note">
        Проверяйте коды возврата всех важных команд и возвращайте честные сами:
        из таких мелочей собирается надёжность, которую потом называют удачей.
      </div>
    </Slide>
  );
}

function S19() {
  const topics = [
    ["PID", "Процесс", "Программа с ресурсами, номером и родителем"],
    ["ps", "Наблюдение", "Снимок, живой режим, загрузка против числа ядер"],
    [
      "TERM",
      "Сигналы",
      "SIGTERM просит, SIGKILL приказывает, SIGHUP перечитывает",
    ],
    ["D", "Состояния", "Непрерываемый сон — маркер бед с хранилищем"],
  ];
  return (
    <Slide
      n={19}
      title="Итог"
      sub="Глава 4 · Жизненный цикл процесса"
      main="Дальше — системы инициализации: кто рождает процессы при старте машины и следит, чтобы они жили."
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
        Три привычки: вежливый сигнал перед жёстким, внезапные смерти — искать в
        журнале ядра, дети должны быть собраны.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_L4 = {
  "8:4": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_L4).
export const SLIDE_TITLES_L4 = {
  "8:4": [
    "Введение",
    "fork и exec",
    "ps и средняя загрузка",
    "Состояния",
    "/proc и открытые файлы",
    "Окружение",
    "Процессор и ввод-вывод",
    "Сигналы",
    "kill",
    "Остановка сервиса",
    "Пауза и фон",
    "Группы процессов",
    "nice и renice",
    "OOM-killer",
    "trap в скриптах",
    "Практика",
    "Демоны",
    "Коды возврата",
    "Итог",
  ],
};
