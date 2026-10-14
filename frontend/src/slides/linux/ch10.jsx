// Слайды для «Linux: от шелла до ядра», глава 10 — «Ядро под микроскопом».
// Тот же дизайн-код, что и глава 2: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗОЛЯЦИЯ И ЯДРО / ГЛАВА 10</span>
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

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics = [
    ["#", "Модули", "Драйверы, подгружаемые на лету"],
    ["=", "Настройки", "sysctl: параметры живого ядра"],
    ["~", "Трассировка", "strace: что программа делает на самом деле"],
    ["%", "Диагностика", "vmstat, iostat, perf — от общего к частному"],
  ];
  return (
    <Slide
      n={1}
      title="Ядро под микроскопом"
      sub="Глава 10 · Модули, настройки, трассировка"
      main="Взрослая диагностика: не читать исходники, а видеть ядро в работе."
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
        Ядро — программа, которой принадлежит вся память, все устройства и все
        решения о том, чей процесс сейчас работает.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Два пространства"
      sub="Двери между мирами"
      main="Трассировка системных вызовов — самый честный способ увидеть, что программа делает на самом деле."
    >
      <div className="s-tree">
        <Node
          title="Программа"
          sub="Пространство пользователя · упадёт — умрёт одна, система целая"
        />
        <Down />
        <Node
          mono
          title="syscall"
          sub="Единственные двери: открыть файл, выделить память, отправить пакет"
        />
        <Down />
        <Node
          amber
          title="Ядро"
          sub="Привилегированный режим · его ошибка кладёт всю машину"
        />
      </div>
      <p className="s-hint">
        Каждое открытие файла и каждый байт из сети проходят эти двери.
      </p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Цепочка загрузки"
      sub="Как машина доходит до ядра"
      main="Машина не грузится — диагноз идёт ровно по этой цепочке, и у каждого шага свои симптомы."
    >
      <div className="s-cols">
        <Node mono title="прошивка" />
        <Arr />
        <Node mono title="загрузчик" />
        <Arr />
        <Node mono title="ядро" />
        <Arr />
        <Node mono title="корень" />
        <Arr />
        <Node mono title="init" />
      </div>
      <div className="s-opts">
        <span className="s-path accent">ядро</span>
        <span>поднимает драйверы, монтирует корень</span>
        <span className="s-path accent">init</span>
        <span>первый процесс — система инициализации</span>
      </div>
      <p className="s-hint">
        Всё, что вы видите дальше, — уже пользовательский мир.
      </p>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Модули ядра"
      sub="Драйверы и подсистемы — на лету"
      main="Флешка работает мгновенно, потому что ядро молча подгрузило модуль накопителя."
    >
      <Cmd>{"lsmod             — что загружено\nmodprobe модуль   — подгрузить\nrmmod модуль      — выгрузить"}</Cmd>
      <div className="s-opts">
        <span className="s-path accent">параметры</span>
        <span>на лету и насовсем</span>
        <span className="s-path accent">/etc/modprobe.d</span>
        <span>файлы настройки</span>
      </div>
      <div className="s-note">
        Собственный модуль — редкая необходимость; уметь посмотреть версию и
        параметры модуля — обычная диагностика.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Настройки ядра: sysctl"
      sub="Каждый файл — один параметр"
      main="Менять по одному, замерять до и после, записывать только проверенное."
    >
      <Cmd>{"sysctl ключ               — прочитать\nsysctl -w ключ=значение   — поменять на лету"}</Cmd>
      <div className="s-opts">
        <span className="s-path accent">/proc/sys</span>
        <span>физическое дерево параметров</span>
        <span className="s-path accent">/etc/sysctl.d</span>
        <span>насовсем</span>
      </div>
      <div className="s-note amber">
        Слепое копирование чужих настроек тюнинга — популярный способ сделать
        хуже.
      </div>
      <p className="s-hint">
        Популярное: предел открытых файлов, поведение сети при перегрузке,
        размеры буферов, склонность к свопу.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Лимиты процессов"
      sub="Слишком много открытых файлов"
      main="Документация обещает одно, процесс живёт с другим — проверяйте лимиты изнутри работающего процесса."
    >
      <Node
        amber
        mono
        title="Too many open files"
        sub="Сервис растёт, открывает файлы — и падает на скромном лимите по умолчанию"
      />
      <div className="s-grid2">
        <Node title="На сеанс" sub="Видно и можно поднять для текущей оболочки" />
        <Node
          green
          title="Навсегда"
          sub="Настройки системы инициализации: у каждой службы свои лимиты"
        />
      </div>
      <p className="s-hint">
        Проверка изнутри — через <span className="s-path">/proc</span>:
        частая история после переездов между машинами.
      </p>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="strace: рентген"
      sub="Каждый вызов с аргументами и кодами возврата"
      main="Программа не говорит, какой файл не найден, — strace покажет все попытки с путями за секунду."
    >
      <Cmd>{"strace команда"}</Cmd>
      <div className="s-grid2">
        <Node
          title="Файл не найден"
          sub="Все попытки с путями — за секунду"
        />
        <Node
          title="Процесс висит"
          sub="Видно, что ждёт чтения из сети, — виноват обретает адресата"
        />
      </div>
      <div className="s-note amber">
        Цена — замедление: на постоянку не включают, для диагностики — золото.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="proc и sys"
      sub="Окна в состояние ядра"
      main="Память, статистика сети, очереди дисков — уже там, без единой утилиты мониторинга."
    >
      <div className="s-grid2">
        <Node
          mono
          title="/proc"
          sub="Процессы: окружение, открытые файлы, соединения — каталог на каждый"
        />
        <Node mono title="/sys" sub="Параметры устройств и подсистем" />
      </div>
      <p className="s-hint">
        Многие красивые дашборды — просто обёртки над чтением этих файлов.
      </p>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Ветераны диагностики"
      sub="От общего к частному"
      main="Высокая занятость при низком ожидании — грузит процессор; высокое ожидание — диск или сеть."
    >
      <div className="s-grid2">
        <Node
          mono
          title="vmstat"
          sub="Сердце машины: очередь к процессору, занятость, ожидание ввода-вывода, своп"
        />
        <Node
          mono
          title="iostat"
          sub="Диски: запросы в очереди, скорость, занятость устройства"
        />
      </div>
      <Node
        green
        title="Дальше — конкретный виновник"
        sub="Через топ и strace: ветераны дают общую картину"
      />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Планировщик"
      sub="Фоновый дом ядра"
      main="Час процессорного при двадцати минутах жизни — процесс работал несколькими потоками на четырёх ядрах."
    >
      <Node
        title="Десятки раз в секунду"
        sub="Решает, какой процесс получит процессор, балансируя отзывчивость терминала с фоновыми задачами"
      />
      <div className="s-grid2">
        <Node title="Приоритеты" sub="Рычаги планировщика" />
        <Node title="Средняя загрузка" sub="Его очередь на взгляд снаружи" />
      </div>
      <p className="s-hint">
        Подсчёт времени тоже его работа — счётчики в топе рассказывают именно
        эту историю.
      </p>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="perf и пламенные графики"
      sub="Где реально горят такты"
      main="Широкие полки пламенного графика — бесполезная работа; видно только профилем, а не догадками."
    >
      <div className="s-cols">
        <Node mono title="perf" sub="Образцы стека тысячи раз в секунду" />
        <Arr />
        <Node title="пламенный график" sub="Столбики стеков с шириной по времени" />
      </div>
      <div className="s-note">
        Из практики: сервис съедал процессор на сериализации логов, которых
        никто не читал; таймер в цикле опроса жрал ядро впустую.
      </div>
      <p className="s-hint">
        Показывает функцию, библиотеку или путь в ядре — с точностью до строки.
      </p>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Голос ядра"
      sub="Кольцевой буфер сообщений"
      main="Ядро честнее всех: оно не умеет приукрашивать."
    >
      <Cmd>{"dmesg   ·   journalctl -k"}</Cmd>
      <div className="s-opts">
        <span className="s-path accent">железо</span>
        <span>убийца памяти</span>
        <span className="s-path accent">диск</span>
        <span>модули</span>
      </div>
      <Node
        green
        title="Дежурный навык"
        sub="После любой странности — сначала сообщения ядра, потом логи приложений"
      />
      <p className="s-hint">
        Доставка в общий журнал делает сообщения доступными поиску.
      </p>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="eBPF"
      sub="Мини-программы внутри ядра"
      main="Пока не писать такие программы — нормально; понимать их возможности — обязательно."
    >
      <div className="s-cols">
        <Node mono title="событие" />
        <Arr />
        <Node title="мини-программа" sub="Безопасное исполнение внутри ядра" />
        <Arr />
        <Node green title="наблюдаемость" sub="С ничтожной ценой и без перезагрузок" />
      </div>
      <div className="s-note">
        Трассировка сетевых задержек, файловых операций, любых вызовов — то,
        что раньше требовало перекомпиляции или патчей.
      </div>
      <p className="s-hint">
        «Глубокая диагностика» у консультанта — почти всегда она.
      </p>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Обновления ядра"
      sub="Риск против дыр"
      main="Перезагружаться по расписанию, а не по смерти — и после перезагрузки проверить, что всё поднялось."
    >
      <div className="s-grid2">
        <Node
          green
          title="Регулярно"
          sub="Исправления дыр и драйверов важнее редких сюрпризов"
        />
        <Node title="Запасное ядро" sub="Старое держится в загрузчике" />
      </div>
      <div className="s-note">
        Живая замена патчами существует в корпоративных дистрибутивах, но
        честная перезагрузка в окне обслуживания проще.
      </div>
      <p className="s-hint">
        После перезагрузки: таргет, службы, сеть.
      </p>
    </Slide>
  );
}

function S15() {
  const rows = [
    ["измеряй", "числа вместо спора мнений"],
    ["по одному", "единственное изменение за раз"],
    ["обратно", "эксперимент на проде обязан иметь обратный путь"],
    ["записывай", "журнал инцидентов дороже вчерашнего героя"],
  ];
  return (
    <Slide
      n={15}
      title="Культура диагностики"
      sub="Завещание курса"
      main="Линукс прощает почти всё, если действовать с головой, и карает высокомерие мгновенно."
    >
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

function S16() {
  return (
    <Slide
      n={16}
      title="Куда расти"
      sub="После курса"
      main="Инженер с одной глубокой областью ценнее десяти с поверхностными знаниями обо всём."
    >
      <div className="s-grid2">
        <Node
          title="Исходники"
          sub="Открыты: чтение подсистем, которыми пользуетесь ежедневно, — лучшая документация"
        />
        <Node
          title="Сообщество"
          sub="Рассылки и чаты живы; за качественный отчёт об ошибке говорят спасибо"
        />
      </div>
      <Node
        green
        title="Одна область до дна"
        sub="Сеть, хранение или планировщик — выберите и копайте"
      />
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Практика на сегодня"
      sub="Пять упражнений"
      main="Сообщения ядра — самое интересное чтение, которое вы откладывали."
    >
      <div className="s-blocks">
        <div className="s-block">
          Найти в списке модулей модуль своей сетевой карты
        </div>
        <div className="s-block">
          Изменить безопасный параметр ядра на лету — и вернуть обратно
        </div>
        <div className="s-block">
          Проследить strace простую команду: сколько вызовов стоит за
          открытием файла
        </div>
        <div className="s-block">
          Запустить vmstat под нагрузкой и найти столбец ожидания
        </div>
        <div className="s-block changed">
          Прочитать последние сообщения ядра
        </div>
      </div>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Память под лупой"
      sub="Что ядро делает с памятью"
      main="Учитесь читать эти числа до инцидента: во время него читать некогда."
    >
      <div className="s-bar-wrap">
        <span>Файловый кэш · лечится, а не жалуется</span>
        <div className="s-bar">
          <div style={{ width: "45%" }} />
        </div>
        <span>Процессы · утечка растёт месяцами, всплеск — за минуты</span>
        <div className="s-bar">
          <div style={{ width: "35%" }} />
        </div>
        <span>Своп · при живой памяти — вопрос настроек</span>
        <div className="s-bar amber">
          <div style={{ width: "10%" }} />
        </div>
      </div>
      <p className="s-hint">
        По характеру роста видно проблему: месяцами — утечка, минутами —
        всплеск.
      </p>
    </Slide>
  );
}

function S19() {
  return (
    <Slide
      n={19}
      title="Хороший вопрос"
      sub="Умение спросить — половина ответа"
      main="Пишите вопрос так, чтобы отвечающий мог воспроизвести: ответ придёт быстрее."
    >
      <div className="s-cols">
        <Node amber title="Плохой" sub="«Ничего не работает, помогите»" />
        <Node
          green
          title="Хороший"
          sub="Что делали, что ожидали, что вышло, версии всего важного, куски журналов"
        />
      </div>
      <div className="s-note">
        Культура, выросшая из рассылок, где хорошая формулировка была валютой.
      </div>
      <p className="s-hint">
        Часто решение находится в процессе формулировки.
      </p>
    </Slide>
  );
}

function S20() {
  return (
    <Slide
      n={20}
      title="Журнал команд"
      sub="Последняя практика"
      main="Через год журнал точнее любой книги: написан про ваши машины и ваши грабли."
    >
      <Node
        title="Файл неочевидных решений"
        sub="Каждое неочевидное решение — и его результат"
      />
      <Cmd>{"дата · контекст · что сделал · что вышло · что сделал потом"}</Cmd>
      <p className="s-hint">Заведите один файл и не бросайте.</p>
    </Slide>
  );
}

function S21() {
  const topics = [
    ["~", "Трассировка", "strace и perf показывают правду"],
    ["#", "Модули", "Драйверы на лету, параметры — в /etc"],
    ["=", "sysctl", "Настройки живого ядра и лимиты"],
    ["%", "Ветераны", "vmstat и iostat дают общую картину"],
  ];
  return (
    <Slide
      n={21}
      title="Итог"
      sub="Глава 10 · Финал курса"
      main="Путь от файловой системы до ядра пройден: линукс — система, которую можно понимать, чинить и любить."
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
        Сообщения ядра — самый честный источник правды в инциденте. Спасибо,
        что слушали.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_L10 = {
  "8:10": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_L10).
export const SLIDE_TITLES_L10 = {
  "8:10": [
    "Введение",
    "Два пространства",
    "Цепочка загрузки",
    "Модули ядра",
    "sysctl",
    "Лимиты процессов",
    "strace",
    "proc и sys",
    "Ветераны диагностики",
    "Планировщик",
    "perf",
    "Голос ядра",
    "eBPF",
    "Обновления ядра",
    "Культура диагностики",
    "Куда расти",
    "Практика",
    "Память под лупой",
    "Хороший вопрос",
    "Журнал команд",
    "Итог",
  ],
};
