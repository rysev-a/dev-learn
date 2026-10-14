// Слайды для «Linux: от шелла до ядра», глава 5 — «Службы и systemd: кто держит сервер на ногах».
// Тот же дизайн-код, что и глава 2: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ПРАВА, ПРОЦЕССЫ, СЛУЖБЫ / ГЛАВА 5</span>
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
    ["unit", "Юниты", "Декларативное описание всего, чем управляет система"],
    ["enable", "Автозапуск", "Отдельная ось: пережить перезагрузку"],
    ["log", "Журнал", "Логи всех служб в одном месте"],
    ["timer", "Таймеры", "Расписание в виде полноценного юнита"],
  ];
  return (
    <Slide
      n={1}
      title="Службы и systemd: кто держит сервер на ногах"
      sub="Глава 5 · Система инициализации"
      main="Юниты, автозапуск, журнал и таймеры — четыре опоры работы с сервисами."
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
        Когда машина включается, кому-то нужно поднять сеть, запустить базы и
        поднять упавший веб-сервер.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="От скрипта к systemd"
      sub="История, объясняющая многое"
      main="Сотня служб: последовательный старт занимает минуты, параллельный — секунды."
    >
      <div className="s-cols">
        <Node
          kind="amber"
          title="Старая школа"
          sub="Огромный шелл-скрипт: службы по очереди, по уровням запуска; упавшую никто не поднимет"
        />
        <Arr />
        <Node
          kind="green"
          title="systemd"
          sub="Параллельный старт, перезапуск после падения, логи в одном месте"
        />
      </div>
      <div className="s-note">
        Спор «сколько всего должна делать система инициализации» не утих, но
        учить нужно то, что стоит на девяноста процентах серверов мира.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Юниты: чем управляет система"
      sub="Описание службы в текстовом файле"
      main="Свои настройки — только в своём каталоге, никаких исключений."
    >
      <div className="s-opts">
        <span className="s-path accent">.service</span>
        <span>служба</span>
        <span className="s-path accent">.timer</span>
        <span>расписание</span>
        <span className="s-path accent">.mount</span>
        <span>монтирование</span>
        <span className="s-path accent">.socket</span>
        <span>пробуждение по соединению</span>
      </div>
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Чужие — из пакетов"
          sub="Не стоит править: обновление пакета их затрёт"
        />
        <Node
          kind="green"
          title="Свои — в каталоге /etc"
          sub="Здесь живёт всё ваше"
        />
      </div>
      <p className="s-hint">
        Каждый юнит отвечает на три вопроса: что запускать, когда запускать и
        как вести себя при падении.
      </p>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Анатомия простого юнита"
      sub="Десять строк — и процесс живёт вечно"
      main="Перезагрузка, падения, лишние права и общий журнал — всё уже учтено."
    >
      <Cmd>
        {
          "[Unit]\nDescription=Моя служба\n[Service]\nExecStart=/opt/app/start.sh\nRestart=on-failure\nRestartSec=5\nUser=app\nWorkingDirectory=/var/lib/app\n[Install]\nWantedBy=multi-user.target"
        }
      </Cmd>
      <p className="s-hint">
        Тип, команда запуска, перезапуск через пять секунд, сервисный
        пользователь, отдельный рабочий каталог.
      </p>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Повседневный словарь"
      sub="Пять глаголов управления"
      main="reload шлёт SIGHUP и не рвёт соединения — restart рвёт: для веб-сервера это минута ошибок."
    >
      <Cmd>
        {
          "systemctl start имя    ·  systemctl stop имя\nsystemctl restart имя  ·  systemctl reload имя\nsystemctl status имя"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          mono
          title="reload"
          sub="Перечитать конфигурацию без разрыва соединений — подходит не всем службам"
        />
        <Node
          mono
          title="status"
          sub="Первый инструмент диагностики: активность, время старта, последние строки лога, код выхода"
        />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Автозапуск"
      sub="Работать и переживать перезагрузку — разные оси"
      main="После любой настройки сервиса убедитесь, что он переживёт перезагрузку."
    >
      <Cmd>
        {
          "systemctl enable имя     # переживёт перезагрузку\nsystemctl disable имя    # убрать из автозапуска\nsystemctl is-enabled имя # проверить"
        }
      </Cmd>
      <div className="s-note amber">
        Половина историй «упало ночью и не поднялось» заканчивается фразой
        «забыли включить автозапуск» — самый дешёвый урок, который можно выучить
        заранее.
      </div>
    </Slide>
  );
}

function S07() {
  const rows = [
    ["Wants", "Желание: запустить вместе, но без жёстких условий"],
    ["Requires", "Требование: запуск добавляет условие"],
    ["After", "Порядок старта без жёсткой связи"],
  ];
  return (
    <Slide
      n={7}
      title="Зависимости юнитов"
      sub="Порядок и желания — разные вещи"
      main="Сервис, стартовавший раньше сети и упавший, спасает лишь настройка перезапуска."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">
        Прописывайте зависимости честно — это дешевле, чем скрипты ожидания с
        бессонными циклами внутри.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Политика перезапуска"
      sub="Что делать при падении: ничего, сразу или с задержкой"
      main="Перезапуск — не лечение: падение каждые десять минут должно стать алертом."
    >
      <Node
        kind="amber"
        title="Служба упала"
        sub="Политика перезапуска говорит, что дальше"
      />
      <Down />
      <Node
        mono
        title="Restart=on-failure"
        sub="Поднять сразу или с задержкой"
      />
      <Down />
      <Node
        mono
        title="StartLimitBurst"
        sub="Ограничитель частоты: не даст циклу падений положить машину"
      />
      <div className="s-note">
        Настройте подъём, соберите алерт на частоту падений и найдите причину —
        именно в этом порядке.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Журнал: все логи в одном месте"
      sub="Вывод всех служб собирается в один журнал"
      main="Переведите журнал в постоянный режим — первое дело на новом сервере."
    >
      <Cmd>
        {
          "journalctl -u имя              # всё по службе\njournalctl -u имя -f           # следить в реальном времени\njournalctl -u имя --since yesterday"
        }
      </Cmd>
      <div className="s-note amber">
        По умолчанию журнал может быть непостоянным и исчезать при перезагрузке:
        включите постоянный режим и лимит размера одной настройкой.
      </div>
      <p className="s-hint">
        Не нужно бегать по каталогам с файлами логов — достаточно спросить
        журнал о конкретном юните.
      </p>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Таргеты: состояния машины"
      sub="Преемники уровней запуска старой школы"
      main="Когда файловая система не монтируется, режим спасения — часто единственная дверь внутрь."
    >
      <div className="s-grid2">
        <Node mono title="multi-user.target" sub="Обычный сервер без графики" />
        <Node mono title="graphical.target" sub="С графическим интерфейсом" />
      </div>
      <Node
        kind="amber"
        mono
        title="rescue.target"
        sub="Минимальная система для ремонта"
      />
      <p className="s-hint">
        Переключение таргетов живое, а назначенный по умолчанию определяет, во
        что машина загрузится. Без графики — меньше памяти и меньше поверхностей
        для проблем.
      </p>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Таймеры вместо крона"
      sub="Расписание в виде полноценного юнита"
      main="Пропущенное из-за простоя выполнится после включения — для бэкапов идеально."
    >
      <div className="s-grid2">
        <Node mono title="OnCalendar=" sub="Запуск по настенному времени" />
        <Node
          mono
          title="OnBootSec="
          sub="Монотонный запуск: промежуток после загрузки"
        />
      </div>
      <Node
        kind="green"
        mono
        title="Persistent=true"
        sub="Догонять пропущенное: машина была выключена в момент запуска — задача выполнится после включения"
      />
      <p className="s-hint">
        Таймер виден в статусах, а его логи живут в общем журнале. Для бэкапов и
        чисток: неважно, когда ночью отработало, — важно, что не пропустилось.
      </p>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Сокет-юниты"
      sub="Система слушает порт до старта службы"
      main="Служба может вообще не работать, пока она никому не нужна."
    >
      <div className="s-cols">
        <Node mono title="клиент" sub="первое соединение" />
        <Arr />
        <Node mono title=".socket" sub="порт слушает система" />
        <Arr />
        <Node
          kind="green"
          mono
          title=".service"
          sub="старт с уже открытым сокетом"
        />
      </div>
      <div className="s-note">
        Бонус: обновление без потери соединений — старый экземпляр дорабатывает,
        новый принимает сокет. Для административных утилит и редких сервисов —
        элегантно и экономно.
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Дополнения вместо правки"
      sub="Ваши настройки поверх пакетного файла"
      main="Обновление пакета не сотрёт ваши правки — они живут отдельным фрагментом."
    >
      <Cmd>
        {"systemctl edit имя   # создать дополнение поверх пакетного юнита"}
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Маленький фрагмент"
          sub="Ложится поверх пакетного файла и применяется перечитыванием настроек"
        />
        <Node
          kind="green"
          title="Дверь в песочницы"
          sub="Ограничения службе добавляются парой строк в том же дополнении"
        />
      </div>
    </Slide>
  );
}

function S14() {
  const rows = [
    ["NoNewPrivileges=true", "Запрет получать новые привилегии"],
    ["ProtectSystem=strict", "Системные каталоги — только чтение"],
    ["ProtectHome=true", "Домашние каталоги людей спрятаны"],
    ["MemoryMax=", "Лимит памяти и числа процессов"],
  ];
  return (
    <Slide
      n={14}
      title="Песочница для службы"
      sub="Скрытое золото, которое почти никто не включает"
      main="Взломанный сервис в клетке приносит вред только внутри клетки."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">
        Безопасность почти бесплатно: одна строка в дополнении описывает, что
        службе действительно нужно — и не больше.
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Антипаттерны из дикой природы"
      sub="Все четыре лечатся тем, что вы уже знаете"
      main="Мгновенный перезапуск вечного падальщика — цикл смерти, грузящий процессор."
    >
      <div className="s-blocks">
        <div className="s-block">
          Свой скрипт с бесконечным циклом вместо службы
        </div>
        <div className="s-block">
          Три независимых механизма автозапуска — и неизвестно, который сработал
        </div>
        <div className="s-block">
          Правка пакетных юнитов напрямую: обновление стирает правки
        </div>
        <div className="s-block changed">
          Мгновенный перезапуск службе с вечным падением — цикл смерти
        </div>
      </div>
      <p className="s-hint">
        Лечение: юнит, дополнение, политика с задержкой, журнал.
      </p>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Служба не стартует"
      sub="Мини-методика из четырёх шагов"
      main="Окружение служб — не то, что в вашем шелле: половина загадок отсюда."
    >
      <div className="s-blocks">
        <div className="s-block">
          Статус: код выхода часто сам называет причину — не найден файл, отказ
          в доступе, тайм-аут
        </div>
        <div className="s-block">
          Журнал юнита целиком: первое сообщение важнее последнего
        </div>
        <div className="s-block">
          Что видит служба: от чьего имени, в каком каталоге, с каким окружением
        </div>
        <div className="s-block changed">
          Менять юнит по одному изменению за раз, с перечитыванием настроек
        </div>
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
      main="Постоянный журнал окупится через месяц — вы скажете себе спасибо."
    >
      <div className="s-blocks">
        <div className="s-block">
          Обернуть любой свой скрипт в службу: юнит из десятка строк, политика
          перезапуска, автозапуск
        </div>
        <div className="s-block">
          Сломать службу намеренно и найти причину в журнале
        </div>
        <div className="s-block">
          Сделать таймер на бэкап из прошлой главы и убедиться по журналу, что
          он сработал
        </div>
        <div className="s-block changed">
          Перевести журнал в постоянный режим, если ещё не
        </div>
      </div>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Окружение службы"
      sub="Вершина айсберга непонимания"
      main="Работает в терминале, падает под службой — первым делом сравните окружение."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Служба стартует не из вашего шелла"
          sub="Не видит ни пути из вашего профиля, ни секретов из вашей сессии"
        />
        <Node
          kind="green"
          mono
          title="Environment="
          sub="Переменные задаются списком в юните — правильное место настроек окружения приложения"
        />
      </div>
      <Cmd>
        {
          "env -i команда   # чистое окружение: условия службы прямо в терминале"
        }
      </Cmd>
    </Slide>
  );
}

function S19() {
  const rows = [
    ["От кого работать", "Пользователь юнита — глава 3"],
    ["Сколько можно", "Лимиты ресурсов"],
    ["Как останавливать", "Тайм-аут и SIGTERM — глава 4"],
    ["Что делать при смерти", "Политика перезапуска — эта глава"],
  ];
  return (
    <Slide
      n={19}
      title="Юнит — обёртка над процессом"
      sub="Служба — процесс с правами, лимитами и сигналами"
      main="Смотрите на юниты глазами вопросов жизни процесса — и они перестанут быть магией."
    >
      <div className="s-table">
        {rows.map(([q, a]) => (
          <div key={q}>
            <span className="s-path accent">{q}</span>
            <span>{a}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S20() {
  return (
    <Slide
      n={20}
      title="Читайте машину как документацию"
      sub="Не воюйте с системой инициализации"
      main="Пять минут просмотра списка юнитов после обновления предотвращают сюрпризы."
    >
      <Cmd>
        {
          "systemctl list-units           # всё, что стартует при загрузке\nsystemctl list-units --failed  # только проблемные"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Время и результат"
          sub="Каждый юнит — со своим статусом старта"
        />
        <Node
          kind="amber"
          title="Тихо умерший таймер"
          sub="Или невключённый автозапуск — видны сразу"
        />
      </div>
      <div className="s-note">
        Машина, чей старт прозрачен для вас, перестаёт быть чёрным ящиком.
      </div>
    </Slide>
  );
}

function S21() {
  const topics = [
    [
      "unit",
      "Юниты",
      "Всё, чем управляет система; служба — лишь самый частый вид",
    ],
    ["status", "Диагностика", "Первая остановка — статус, потом журнал юнита"],
    ["enable", "Автозапуск", "Отдельная ось от работы: проверять обе"],
    ["timer", "Таймеры", "Расписание как юнит, догоняющее пропущенное"],
  ];
  return (
    <Slide
      n={21}
      title="Итог"
      sub="Глава 5 · Кто держит сервер на ногах"
      main="Следующая глава — сеть: адреса, порты и то, как диагностировать недоступный сервис."
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
        Зависимости — желания, требования и порядок; перезапуск держит сервис на
        ногах, но не лечит причины падений.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_L5 = {
  "8:5": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_L5).
export const SLIDE_TITLES_L5 = {
  "8:5": [
    "Введение",
    "От скриптов к systemd",
    "Юниты",
    "Анатомия юнита",
    "Повседневный словарь",
    "Автозапуск",
    "Зависимости",
    "Политика перезапуска",
    "Журнал",
    "Таргеты",
    "Таймеры",
    "Сокет-юниты",
    "Дополнения",
    "Песочницы",
    "Антипаттерны",
    "Служба не стартует",
    "Практика",
    "Окружение службы",
    "Юнит и процесс",
    "Список юнитов",
    "Итог",
  ],
};
