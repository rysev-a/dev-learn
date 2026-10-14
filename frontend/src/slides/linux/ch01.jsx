// Слайды для «Linux: от шелла до ядра», глава 1 — «Файловая система».
// Дизайн по макету Figma: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ФАЙЛОВАЯ СИСТЕМА И ШЕЛЛ / ГЛАВА 1</span>
      <span>{String(n).padStart(2, "0")} / 17</span>
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
    ["/", "Дерево", "Единое пространство имён"],
    ["#4821", "Инода", "Метаданные и блоки данных"],
    ["ln", "Ссылки", "Разные пути к содержимому"],
    ["mount", "Монтирование", "Новые источники в одном дереве"],
  ];
  return (
    <Slide
      n={1}
      title="Файловая система и шелл"
      sub="Глава 1 · Иерархия · иноды · монтирование"
      main="Всё — файл: единая модель данных, процессов и устройств."
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
      <p className="s-hint">От пути к данным — и обратно к единому дереву.</p>
    </Slide>
  );
}

function S02() {
  const branches = [
    ["/etc", "Системные настройки"],
    ["/var", "Логи, кэш, очереди"],
    ["/home", "Каталоги пользователей"],
    ["/root", "Дом администратора"],
    ["/tmp", "Временные файлы"],
    ["/bin · /usr/bin", "Программы"],
    ["/lib", "Библиотеки"],
    ["/media · /mnt", "Флешки и монтирование"],
  ];
  return (
    <Slide
      n={2}
      title="Один корень. Всё начинается с /"
      sub="Не диски C: и D:, а ветви общего дерева."
      main="Путь — это маршрут от корня через каталоги к объекту."
    >
      <div className="s-tree">
        <div className="s-root">
          <span className="s-root-slash">/</span>
          <span className="s-node-sub">Единый корень</span>
        </div>
        <Down />
        <div className="s-grid2">
          {branches.map(([p, d]) => (
            <Node key={p} mono title={p} sub={d} />
          ))}
        </div>
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Файлы, за которыми стоит ядро"
      sub="/proc, /sys и /dev — интерфейсы, а не документы на диске."
      main="Чтение → состояние. Запись → действие."
    >
      <div className="s-label">ПОСТОЯННОЕ ХРАНЕНИЕ</div>
      <Node title="/etc · /home" sub="Обычные данные, переживают выключение" />
      <div className="s-label" style={{ marginTop: 14 }}>
        ЯДРО / ОЗУ
      </div>
      <div className="s-cols">
        <Node green mono title="/proc" sub="Процессы" />
        <Node green mono title="/sys" sub="Оборудование" />
        <Node green mono title="/dev" sub="Устройства" />
      </div>
      <div className="s-note amber" style={{ marginTop: 14 }}>
        Запись в /dev/sda может перезаписать диск
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Имя — не сам файл"
      sub="Каталог связывает имя с номером иноды. Инода описывает содержимое."
      main="Имя живёт в каталоге; метаданные и блоки — в иноде."
    >
      <div className="s-label">КАТАЛОГ /home/anna</div>
      <div className="s-table">
        <div>
          <span>Имя</span>
          <span>Инода</span>
        </div>
        <div>
          <span className="s-path">notes.txt</span>
          <span className="s-path accent">4821</span>
        </div>
        <div>
          <span className="s-path">photo.jpg</span>
          <span className="s-path">7350</span>
        </div>
      </div>
      <div className="s-label" style={{ marginTop: 14 }}>
        ИНОДА 4821
      </div>
      <Node
        title="Владелец: anna · Права: rw-r--r-- · 12 КБ"
        sub="Указатели на блоки диска"
      />
      <div className="s-label" style={{ marginTop: 14 }}>
        ДАННЫЕ
      </div>
      <div className="s-blocks">
        {["A", "B", "C", "D", "E", "F"].map((b) => (
          <span className="s-block" key={b}>
            {b}
          </span>
        ))}
      </div>
      <p className="s-note">
        Переименование меняет запись каталога, а не байты.
      </p>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Две ссылки. Две разные модели"
      sub="Жёсткая разделяет иноду. Символическая хранит путь."
      main="rm одного имени не удаляет данные жёсткой ссылки; симлинк может оборваться."
    >
      <div className="s-cols">
        <div className="s-card">
          <div className="s-label">ЖЁСТКАЯ</div>
          <Node mono title="original" />
          <Node mono title="hard" />
          <Arr />
          <Node green title="Инода 4821" sub="Одни данные · ссылок: 2" />
        </div>
        <div className="s-card">
          <div className="s-label">СИМВОЛИЧЕСКАЯ</div>
          <Node mono title="soft" sub="Внутри — путь «original»" />
          <Arr />
          <Node mono title="original" sub="Инода 4821 → данные" />
          <div className="s-note amber">rm original → ссылка оборвана</div>
        </div>
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Файл удалён. А место — нет?"
      sub="Две независимые причины."
      main="Проверяйте и байты, и иноды: df -h и df -i."
    >
      <div className="s-label">ЛОГ УДАЛЁН, НО ОТКРЫТ</div>
      <div className="s-cols">
        <Node title="Процесс" sub="Дескриптор открыт" />
        <Arr />
        <Node amber title="Инода 4821" sub="Ссылок: 0 · блоки: 8 ГБ" />
      </div>
      <Cmd>lsof +L1</Cmd>
      <div className="s-label" style={{ marginTop: 14 }}>
        БАЙТЫ ЕСТЬ — ИНОД НЕТ
      </div>
      <div className="s-bar-wrap">
        <span>Байты · свободно 60%</span>
        <div className="s-bar">
          <div style={{ width: "60%" }} />
        </div>
        <span className="amber-text">Иноды · свободно 0%</span>
        <div className="s-bar amber">
          <div style={{ width: "100%" }} />
        </div>
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Подключить устройство к каталогу"
      sub="Монтирование добавляет ФС в существующее дерево."
      main="Точка монтирования — каталог; старое содержимое скрыто, но не удалено."
    >
      <div className="s-cols">
        <Node mono title="/mnt/data" sub="До: старый файл notes.txt" />
        <Arr />
        <Node mono title="/dev/sdb1" sub="Отдельная ФС" />
      </div>
      <Down />
      <Node green mono title="/mnt/data" sub="После: archive, photos" />
      <div className="s-label" style={{ marginTop: 14 }}>
        /etc/fstab — насовсем
      </div>
      <div className="s-fstab">
        <span>UUID=…</span>
        <span>/mnt/data</span>
        <span>ext4</span>
        <span>defaults</span>
      </div>
      <div className="s-note amber">
        Ошибка в fstab опасна: проверяй mount -a
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Разные источники. То же дерево"
      sub="Устройство, образ или сеть — одно действие."
      main="Приложение видит путь, не зная, что за точкой монтирования."
    >
      <div className="s-cols">
        <Node mono title="/dev/sdb1" sub="Устройство" />
        <Node mono title="disk.img" sub="Образ (loop)" />
        <Node mono title="NFS" sub="Сеть" />
      </div>
      <Down />
      <div className="s-node green">
        <span className="s-root-slash small">/</span>
        <span className="s-path">/mnt/data · /mnt/image · /mnt/shared</span>
      </div>
      <div className="s-label" style={{ marginTop: 14 }}>
        ОПЦИИ
      </div>
      <div className="s-opts">
        <span className="s-path accent">ro</span>
        <span>только чтение</span>
        <span className="s-path accent">sync</span>
        <span>запись сразу на диск</span>
        <span className="s-path accent">noexec</span>
        <span>без запуска файлов</span>
        <span className="s-path accent">user</span>
        <span>может обычный пользователь</span>
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Проверьте модель руками"
      sub="Работайте в тестовом каталоге."
      main="Наблюдайте результат каждой команды."
    >
      <div className="s-label">ОБЗОР И ОБЪЁМ</div>
      <Cmd>ls / · du -h . | sort -h{"\n"}df -h · df -i</Cmd>
      <div className="s-label" style={{ marginTop: 12 }}>
        ЭКСПЕРИМЕНТ СО ССЫЛКАМИ
      </div>
      <Cmd>
        ln original hard · ln -s original soft{"\n"}rm original · ls -l hard
        soft
      </Cmd>
      <div className="s-note">hard → данные живы · soft → цель потеряна</div>
      <div className="s-label" style={{ marginTop: 12 }}>
        МОНТИРОВАНИЕ
      </div>
      <Cmd>sudo mount /dev/sdb1 /mnt{"\n"}sudo umount /mnt</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Имя — этикетка. Содержимое — экспонат"
      sub="Расширение — договорённость; точка в начале скрывает файл."
      main="Тип определяют данные. Скрытые файлы видно через ls -a."
    >
      <div className="s-label">МУЗЕЙ /home/anna</div>
      <div className="s-cols">
        <Node mono title=".bashrc" sub="Шелл" />
        <Node mono title=".vimrc" sub="Редактор" />
        <Node mono title=".gitconfig" sub="Git" />
      </div>
      <Cmd>ls -a</Cmd>
      <div className="s-label" style={{ marginTop: 12 }}>
        НОВАЯ ЭТИКЕТКА ≠ НОВЫЙ ТИП
      </div>
      <div className="s-cols">
        <Node mono title="program" sub="Исполняемые байты" />
        <Arr />
        <Node mono title="program.txt" sub="Те же байты" />
      </div>
    </Slide>
  );
}

function S11() {
  const types = [
    ["-", "Обычный файл", "Байты"],
    ["d", "Каталог", "Таблица имён"],
    ["s", "Сокет", "Обмен процессов"],
    ["p", "Канал", "FIFO-поток"],
    ["b", "Блочное устр.", "/dev/sda"],
    ["c", "Симв. устр.", "/dev/tty"],
  ];
  return (
    <Slide
      n={11}
      title="Не каждый файл — документ"
      sub="В каталоге лежат записи о разных видах объектов."
      main="Один механизм имён открывает разные сущности. Проверка: file photo.jpg"
    >
      <div className="s-grid2">
        {types.map(([ch, t, d]) => (
          <div className="s-type" key={ch}>
            <span className="s-type-ch">{ch}</span>
            <div>
              <div className="s-node-title">{t}</div>
              <div className="s-node-sub">{d}</div>
            </div>
          </div>
        ))}
      </div>
      <div className="s-label" style={{ marginTop: 12 }}>
        КАНАЛ МЕЖДУ ПРОЦЕССАМИ
      </div>
      <div className="s-cols">
        <Node title="Процесс" sub="Пишет" />
        <Arr />
        <Node green mono title="FIFO" />
        <Arr />
        <Node title="Процесс" sub="Читает" />
      </div>
    </Slide>
  );
}

function S12() {
  const times = [
    ["mtime", "Изменили содержимое", "Редактирование"],
    ["ctime", "Изменили метаданные", "Права, владелец"],
    ["atime", "Обратились к файлу", "Чтение"],
  ];
  return (
    <Slide
      n={12}
      title="Три времени одного файла"
      sub="mtime, ctime и atime отвечают на разные вопросы."
      main="Ищем по содержимому — берём mtime: find . -mtime -1"
    >
      <div className="s-cols">
        {times.map(([nm, t, d]) => (
          <div className="s-card" key={nm}>
            <div className="s-time-mono">{nm}</div>
            <div className="s-node-title">{t}</div>
            <div className="s-node-sub">{d}</div>
          </div>
        ))}
      </div>
      <Cmd>find . -mtime -1</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Переместить имя или байты?"
      sub="Одно действие пользователя — две операции хранения."
      main="Большие переносы — с проверкой контрольных сумм."
    >
      <div className="s-label">ВНУТРИ ОДНОГО ДИСКА</div>
      <div className="s-cols">
        <Node mono title="/a/report" />
        <Arr />
        <Node green mono title="/b/report" />
      </div>
      <Node
        title="Та же инода → те же блоки"
        sub="Мгновенно, данные не копируются"
      />
      <div className="s-label" style={{ marginTop: 12 }}>
        МЕЖДУ ДИСКАМИ
      </div>
      <div className="s-cols">
        <Node title="Диск A" sub="A · B · C · D" />
        <Arr />
        <Node amber title="Диск B" sub="A′ · B′ · C′ · D′" />
      </div>
      <Node
        title="Копировать → удалить источник"
        sub="Новая инода, физическая копия"
      />
      <Cmd>sha256sum /a/report · sha256sum /mnt/data/report</Cmd>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Журнал и снимки"
      sub="Журнал лечит сбой питания. Снимок — точка возврата."
      main="Перед рискованным шагом — снимок; важные данные — отдельная копия."
    >
      <div className="s-label">ЖУРНАЛ</div>
      <div className="s-cols">
        <Node title="Намерение" />
        <Arr />
        <Node title="Запись" />
        <Arr />
        <Node title="Фиксация" />
        <Arr />
        <Node green title="Восстановление" />
      </div>
      <div className="s-label" style={{ marginTop: 12 }}>
        СНИМОК (КОПИРОВАНИЕ ПРИ ЗАПИСИ)
      </div>
      <div className="s-cols">
        <div className="s-card">
          <div className="s-label">СНИМОК t₀</div>
          <div className="s-blocks">
            {["A", "B", "C", "D"].map((b) => (
              <span className="s-block" key={b}>
                {b}
              </span>
            ))}
          </div>
        </div>
        <div className="s-card">
          <div className="s-label">ТОМ СЕЙЧАС</div>
          <div className="s-blocks">
            {["A", "B"].map((b) => (
              <span className="s-block" key={b}>
                {b}
              </span>
            ))}
            <span className="s-block changed">C′</span>
            <span className="s-block">D</span>
          </div>
        </div>
      </div>
      <p className="s-note">
        A, B, D — общие. C′ — новый блок при первой записи.
      </p>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Одна папка. Два входа"
      sub="Bind-монтирование показывает те же файлы по другому пути."
      main="Это не копия: файл появился — виден сразу в обоих путях."
    >
      <div className="s-cols">
        <Node mono title="/srv/data" sub="Исходный путь · report.csv" />
        <span className="s-arr">←</span>
        <Node mono title="/mnt/view" sub="Привязанный путь · report.csv" />
      </div>
      <div className="s-node green" style={{ marginTop: 12 }}>
        <span className="s-node-title">Те же файлы</span>
        <span className="s-node-sub">Без копирования байтов</span>
      </div>
      <Cmd>mount --bind /srv/data /mnt/view</Cmd>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Записано в память ≠ на диске"
      sub="Между приложением и носителем — кэш и фоновая запись."
      main="sync — сброс; перед извлечением — umount."
    >
      <div className="s-cols">
        <Node title="Запись" sub="Приложение" />
        <Arr />
        <Node amber title="Кэш в ОЗУ" sub="Изменённые страницы" />
        <Arr />
        <Node title="Фоновый сброс" sub="Ядро" />
        <Arr />
        <Node green title="Диск" />
      </div>
      <div className="s-label" style={{ marginTop: 12 }}>
        ДВА ПИСАТЕЛЯ — ГОНКА
      </div>
      <Node
        amber
        title="Общий файл"
        sub="Итог зависит от порядка записей — нужны блокировки"
      />
      <Cmd>sync{"\n"}sudo umount /mnt/data</Cmd>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Теперь дерево стало понятнее"
      sub="Иерархия · устройство файла · подключение хранилищ."
      main="Далее: командная строка, конвейеры и первые скрипты."
    >
      <div className="s-cols">
        <div className="s-card">
          <div className="s-label">ИЕРАРХИЯ</div>
          <div className="s-time-mono">/</div>
          <div className="s-path">/etc — настройки</div>
          <div className="s-path">/var — рост</div>
          <div className="s-path">/proc /sys /dev</div>
        </div>
        <div className="s-card">
          <div className="s-label">ФАЙЛ И ССЫЛКИ</div>
          <Node title="Имя → инода → данные" />
          <Node title="Жёсткая" sub="Другое имя, та же инода" />
          <Node title="Символическая" sub="Отдельный файл с путём" />
        </div>
        <div className="s-card">
          <div className="s-label">МОНТИРОВАНИЕ</div>
          <Node title="Источник" sub="Диск, образ, сеть" />
          <Down />
          <Node title="Каталог в дереве" sub="/etc/fstab — насовсем" />
        </div>
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES = {
  "8:1": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES).
export const SLIDE_TITLES = {
  "8:1": [
    "Введение",
    "Один корень",
    "/proc, /sys, /dev",
    "Инода: имя ≠ файл",
    "Хард и софт-ссылки",
    "Ловушки места",
    "Монтирование",
    "Разные источники",
    "Практика",
    "Имя и содержимое",
    "Типы файлов",
    "Три времени файла",
    "Перемещение",
    "Журнал и снимки",
    "Bind: два входа",
    "Кэш записи",
    "Итог",
  ],
};
