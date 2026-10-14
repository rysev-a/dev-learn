// Слайды для «Linux: от шелла до ядра», глава 8 — «Пакеты и зависимости».
// Тот же дизайн-код, что и глава 2: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СЕТЬ И ХРАНЕНИЕ / ГЛАВА 8</span>
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

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics = [
    ["%", "Пакет", "Посылка с манифестом и списком зависимостей"],
    ["@", "Репозитории", "Подписанные источники — акты доверия"],
    ["#", "Зависимости", "Общий пул библиотек и решатель конфликтов"],
    ["~", "Гигиена", "Изоляция, чистка, автообновления безопасности"],
  ];
  return (
    <Slide
      n={1}
      title="Пакеты и зависимости"
      sub="Глава 8 · Откуда берутся программы"
      main="Понимание менеджера отличает «поставил как в блоге» от осознанного управления системой."
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
        Программа в линуксе — редко один файл: библиотеки, конфиги,
        документация, скрипты и описание, как это корректно поставить и убрать.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Пакет — посылка с манифестом"
      sub="Файлы, метаданные, зависимости"
      main="База пакетов знает, какому пакету принадлежит каждый файл, — и удаляет без остатка."
    >
      <div className="s-grid2">
        <Node
          title="Файлы"
          sub="Пути установки, конфиги, документация, скрипты"
        />
        <Node title="Метаданные" sub="Версия, описание, автор" />
      </div>
      <div className="s-label">МАНИФЕСТ</div>
      <div className="s-cols">
        <Node amber title="Зависимости" sub="Какие пакеты нужны до установки" />
        <Node green title="Предоставляет" sub="Что пакет отдаёт другим" />
      </div>
      <div className="s-note">
        Менеджер регистрирует каждый файл в базе: чужие файлы видны сразу, а
        удаление — по-настоящему чистое.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Репозитории и подписи"
      sub="Пакеты берутся из каталогов с подписанными пакетами"
      main="Каждый лишний репозиторий — чужие руки внутри вашей машины."
    >
      <div className="s-cols">
        <Node mono title="репозиторий" />
        <Arr />
        <Node title="подписанный пакет" sub="Подпись сервера" />
        <Arr />
        <Node green title="проверка ключом" sub="Ключи уже живут в системе" />
      </div>
      <div className="s-label">СПИСОК ИСТОЧНИКОВ</div>
      <div className="s-opts">
        <span className="s-path accent">официальные</span>
        <span>база по умолчанию</span>
        <span className="s-path accent">+ сторонние</span>
        <span>осознанно и по минимуму</span>
      </div>
      <div className="s-note amber">
        Каждая строчка в списке источников — вопрос: доверяю ли я этим людям мою
        систему. И это не риторический вопрос.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Словарь менеджера"
      sub="Сначала узнать, потом решать"
      main="Обновлять регулярно: в обновлениях чинят дыры, о которых уже написали в новостях."
    >
      <div className="s-grid2">
        <Node
          green
          mono
          title="update"
          sub="Сходить в репозитории и узнать, что нового"
        />
        <Node
          mono
          title="upgrade"
          sub="Поставить свежие версии установленных"
        />
      </div>
      <div className="s-label">ЕЖЕДНЕВНЫЙ НАБОР</div>
      <div className="s-opts">
        <span className="s-path accent">search</span>
        <span>найти</span>
        <span className="s-path accent">show</span>
        <span>информация</span>
        <span className="s-path accent">list</span>
        <span>установленные</span>
        <span className="s-path accent">verify</span>
        <span>целостность</span>
      </div>
      <p className="s-hint">
        Разделение update и upgrade странное, но историческое.
      </p>
    </Slide>
  );
}

function S05() {
  const rows = [
    ["X.0.0", "старшее — ломающие изменения"],
    ["1.X.0", "среднее — новые возможности"],
    ["1.4.X", "младшее — исправления"],
  ];
  return (
    <Slide
      n={5}
      title="Арифметика версий"
      sub="Три числа — договорённость"
      main="Доверяй, но тестируй: диапазон совместимости — арифметика, а не гарантия."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note amber">
        Договорённость держится на честности авторов: чужие ломающие изменения в
        младших версиях — не легенда.
      </div>
      <p className="s-hint">
        Проверки перед накатом обновлений на прод — обязательны.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Ад зависимостей"
      sub="Что было до пакетов и как из этого вышли"
      main="Конфликты — математическая задача с решателем; ручное редактирование базы пакетов — самый страшный вид самодеятельности."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">ДО ПАКЕТОВ</div>
          <span className="s-node-title">Каждая тащит свои библиотеки</span>
          <span className="s-node-sub">
            Версии конфликтуют · апгрейд одного ломает другого
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">ОБЩИЙ ПУЛ</div>
          <span className="s-node-title">Одна библиотека на всех</span>
          <span className="s-node-sub">
            Менеджер следит за совместимостью · конфликты решает решатель
          </span>
        </div>
      </div>
      <div className="s-cols">
        <Node amber title="конфликт версий" />
        <Arr />
        <Node green title="решатель находит совместимые" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Два племени: deb и rpm"
      sub="Внутри похожи, между собой несовместимы"
      main="Низкоуровневые инструменты — для вопросов, высокоуровневые — для действий."
    >
      <div className="s-grid2">
        <Node
          mono
          title=".deb"
          sub="Данные, метаданные, скрипты установки · семейство Debian"
        />
        <Node mono title=".rpm" sub="Та же начинка · семейство Red Hat" />
      </div>
      <div className="s-label">ПРАВИЛО</div>
      <div className="s-cols">
        <Node
          amber
          title="Низкоуровневые"
          sub="Ставят напрямую, без зависимостей — только для разбора"
        />
        <Node
          green
          title="Высокоуровневые"
          sub="Зависимости и учёт — для жизни"
        />
      </div>
      <div className="s-note amber">
        Конвертация форматов — почти всегда плохая идея; пакет, поставленный
        низкоуровневым инструментом, часто не удаляется чисто.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Сборка из исходников"
      sub="Когда пакета нет"
      main="Соберите собственный пакет: все плюсы свежей версии при полном учёте в базе."
    >
      <div className="s-cols">
        <Node mono title="configure" sub="Проверяет систему" />
        <Arr />
        <Node mono title="make" sub="Собирает" />
        <Arr />
        <Node mono title="make install" sub="Раскладывает файлы" />
      </div>
      <div className="s-note">
        Проблема — путь: файлы появляются вне базы пакетов, и удалить их потом —
        квест.
      </div>
      <div className="s-grid2">
        <Node title="Свой префикс" sub="Изоляция сборки в отдельный каталог" />
        <Node
          green
          title="Свой пакет"
          sub="Исходники — в пакет, установка — через менеджер"
        />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Общие библиотеки"
      sub="Кто кого не нашёл"
      main="Собрана против более новой библиотеки — честно не запустится, а не упадёт в странном месте."
    >
      <Cmd>{"ldd /usr/bin/программа"}</Cmd>
      <div className="s-grid2">
        <Node
          amber
          title="Библиотека не найдена"
          sub="Вторая по частоте ошибка запуска после отказа в доступе"
        />
        <Node
          mono
          title="ldconfig"
          sub="Обновляет кэш загрузчика после установки"
        />
      </div>
      <div className="s-label">ВЕРСИОНИРОВАНИЕ</div>
      <div className="s-opts">
        <span className="s-path accent">lib.so.X</span>
        <span>номер версии в имени файла</span>
        <span className="s-path accent">X</span>
        <span>совместимость — в пределах старшей</span>
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Удержание версий"
      sub="Иногда нужна старая"
      main="Воспроизводимость важнее свежести: держать удержание — осознанно и недолго."
    >
      <div className="s-grid2">
        <Node
          amber
          title="Удержание"
          sub="Менеджер не трогает пакет до отмены — но обновления безопасности обходят его стороной"
        />
        <Node
          green
          title="Зеркала репозиториев"
          sub="Проверенные версии: тест совпадает с продом байт в байт"
        />
      </div>
      <div className="s-note">
        Каждый удержанный пакет — долг. Практика больших компаний — свои зеркала
        с проверенными версиями.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Языковые экосистемы"
      sub="Параллельный мир pip и npm"
      main="Системным менеджером — системное, языковым — языковое, и никогда вручную поверх системных путей."
    >
      <div className="s-grid2">
        <Node
          mono
          title="pip · npm"
          sub="Живут параллельно системному менеджеру"
        />
        <Node
          amber
          title="Конфликт"
          sub="Одна библиотека в системной и языковой поставке — источник загадочных багов"
        />
      </div>
      <div className="s-cols">
        <Node title="Системный пул" sub="Системному менеджеру" />
        <Arr />
        <Node
          green
          title="Изолированное окружение"
          sub="Языковые пакеты — в отдельном каталоге"
        />
      </div>
      <div className="s-note">Современный ответ — изоляция, а не смешение.</div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Чистка осадка"
      sub="Что накопилось за годы"
      main="Регулярная чистка держит систему лёгкой, а список установленного — читаемым."
    >
      <div className="s-label">РЕГУЛЯРНО</div>
      <div className="s-opts">
        <span className="s-path accent">autoremove</span>
        <span>осиротевшие пакеты</span>
        <span className="s-path accent">autoclean</span>
        <span>кэш</span>
      </div>
      <Node
        green
        title="Старые ядра — хотя бы парочку"
        sub="Страховка, если новое ядро не подружится с оборудованием"
      />
      <div className="s-note">
        После долгих проектов просмотрите список установленных пакетов — там
        бывают сюрпризы.
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Контейнеры"
      sub="Логичный финал эволюции"
      main="Зависимости больше не общие, а запаянные в образ — ад зависимостей исчезает."
    >
      <div className="s-tree">
        <Node mono title="образ" sub="Собирается один раз" />
        <Down />
        <Node
          title="приложение + зависимости"
          sub="Запаяны в образ, больше не общие"
        />
        <Down />
        <Node green title="работает везде одинаково" />
      </div>
      <div className="s-note">
        Внутри образа живёт тот же менеджер: обновления безопасности
        накатываются пересборкой образа, а не входом на сервер.
      </div>
      <p className="s-hint">Отдельная глава о контейнерах — уже скоро.</p>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Обновления безопасности"
      sub="Автоматика и перезапуск"
      main="Новая библиотека заработает только после перезапуска процесса — долгоживущие сервисы перезапускают по расписанию."
    >
      <div className="s-grid2">
        <Node
          green
          title="Автообновления"
          sub="Включите хотя бы для библиотек — самый дешёвый взнос в безопасность"
        />
        <Node
          title="Мониторинг"
          sub="Наличие обновлений проверяет мониторинг, а не память"
        />
      </div>
      <div className="s-note amber">
        Знаменитые взломы — через бреши с готовым обновлением, которое месяцами
        никто не ставил.
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Воспроизводимость"
      sub="Система описана файлом"
      main="Любое изменение — через файлы описания, ручной вход — только читать."
    >
      <div className="s-cols">
        <Node mono title="файл описания" />
        <Arr />
        <Node
          title="разворачивание"
          sub="Система восстанавливается из описания"
        />
        <Arr />
        <Node green title="без дрейфа" />
      </div>
      <Node
        amber
        title="Ручные установки — главный враг"
        sub="Один вход на сервер с командой «поставить и забыть» — и сервер не описан нигде, кроме вашей памяти"
      />
      <div className="s-note">
        Именно так серверы перестают быть снежинками, которые страшно трогать.
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Проверка скачанного"
      sub="Секунды проверки против недель восстановления"
      main="Передача чужого текста прямо в шелл — это доверие всей машины незнакомцу."
    >
      <div className="s-opts">
        <span className="s-path accent">ключи</span>
        <span>имеют срок жизни</span>
        <span className="s-path accent">хэш-суммы</span>
        <span>сверять с официальными</span>
      </div>
      <div className="s-note">
        Просроченный ключ репозитория лечится обновлением пакета ключей, а не
        отключением проверки.
      </div>
      <Cmd>
        {"curl пример/install.sh | sh    ← сначала прочитать, что делает"}
      </Cmd>
      <p className="s-hint">
        Даже инструкция с высоким рейтингом: понять каждый шаг до выполнения.
      </p>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Практика на сегодня"
      sub="Четыре упражнения"
      main="Автообновления безопасности — самый дешёвый взнос в безопасность системы."
    >
      <div className="s-blocks">
        <div className="s-block">
          Посчитать источники пакетов своей машины — и вспомнить, зачем нужен
          каждый
        </div>
        <div className="s-block">
          Найти, какому пакету принадлежит системный файл, и проверить
          целостность его пакета
        </div>
        <div className="s-block">
          ldd у трёх программ: найти, чья библиотека не находится
        </div>
        <div className="s-block changed">
          Настроить автообновления безопасности, если их ещё нет
        </div>
      </div>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Свежее или проверенное"
      sub="Ответ зависит от машины"
      main="Так живут зрелые команды — и это стоит перенять."
    >
      <div className="s-grid2">
        <Node
          title="Ноутбук разработчика"
          sub="Живёт на свежем: нужны новые инструменты, риск — лишь собственное время"
        />
        <Node
          title="Сервер"
          sub="Живёт на проверенном: обновления безопасности точно, скачки версий — по расписанию"
        />
      </div>
      <Node
        green
        title="Третий путь — изолированные окружения"
        sub="Ядро системы старое и стабильное, инструменты — свежие внутри сред"
      />
    </Slide>
  );
}

function S19() {
  return (
    <Slide
      n={19}
      title="Драйверы и прошивки"
      sub="Тихая тема пакетов"
      main="Пакеты — это то, как ядра и обновляются: на нестандартном железе обновления тестируют в стороне."
    >
      <div className="s-grid2">
        <Node
          amber
          title="Ядро обновилось, модуль — нет"
          sub="Машина загрузилась без ускорителя или без сети"
        />
        <Node
          amber
          title="Прошивка прилетела криво"
          sub="Устройство просто пропало"
        />
      </div>
      <Node
        green
        title="Подстраховка"
        sub="Тест на непродовой машине и старое ядро в загрузчике"
      />
      <div className="s-note">
        Обновления прошивок и закрытых модулей идут тем же пакетным конвейером.
      </div>
    </Slide>
  );
}

function S20() {
  return (
    <Slide
      n={20}
      title="Документация пакета"
      sub="Пять минут до установки"
      main="Читать журнал изменений перед обновлением важного пакета — минута, которая объясняет, что изменится."
    >
      <div className="s-grid2">
        <Node
          title="Страница пакета"
          sub="Описание, список файлов, журнал изменений"
        />
        <Node
          title="Список файлов"
          sub="Куда пакет положил исполняемые файлы и настройки"
        />
      </div>
      <div className="s-note">
        Пять минут знакомства с пакетом до установки экономят вечер поиска
        после.
      </div>
    </Slide>
  );
}

function S21() {
  return (
    <Slide
      n={21}
      title="Язык инструкций"
      sub="Разобрать магическую строку"
      main="Осознанные пять шагов лучше одной магической строки: система останется вашей."
    >
      <div className="s-cols">
        <Node mono title="скачать" />
        <Arr />
        <Node mono title="распаковать" />
        <Arr />
        <Node mono title="положить" sub="в системный каталог" />
        <Arr />
        <Node mono title="выполнить" sub="скрипт установки" />
      </div>
      <div className="s-note">
        Сделайте шаги руками: видно, куда что попадает и что потом удалять.
      </div>
      <p className="s-hint">
        Загрузка и передача в шелл непонятной строки — даже с высоким рейтингом
        — требует остановки и чтения.
      </p>
    </Slide>
  );
}

function S22() {
  const topics = [
    ["#", "Пакет", "Манифест, зависимости, учёт каждого файла в базе"],
    ["@", "Репозиторий", "Подписи и осознанный минимум источников"],
    ["&", "Решатель", "Общий пул вместо ада зависимостей"],
    ["~", "Дисциплина", "Изоляция экосистем, удержание, автообновления"],
  ];
  return (
    <Slide
      n={22}
      title="Итог"
      sub="Глава 8 · Пакеты и зависимости"
      main="Следующая глава — контейнеры: где все эти проблемы запаяны в образ."
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
        Привычки зрелой системы: минимум источников, регулярная чистка,
        обновления безопасности не ждут.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_L8 = {
  "8:8": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_L8).
export const SLIDE_TITLES_L8 = {
  "8:8": [
    "Введение",
    "Пакет — посылка",
    "Репозитории и подписи",
    "Словарь менеджера",
    "Арифметика версий",
    "Ад зависимостей",
    "deb и rpm",
    "Сборка из исходников",
    "Общие библиотеки",
    "Удержание версий",
    "Языковые экосистемы",
    "Чистка осадка",
    "Контейнеры",
    "Обновления безопасности",
    "Воспроизводимость",
    "Проверка скачанного",
    "Практика",
    "Свежее или проверенное",
    "Драйверы и прошивки",
    "Документация пакета",
    "Язык инструкций",
    "Итог",
  ],
};
