// Слайды для «Linux: от шелла до ядра», глава 9 — «Контейнеры: изоляция без магии».
// Тот же дизайн-код, что и глава 1: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗОЛЯЦИЯ И ЯДРО / ГЛАВА 9</span>
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
    ["ns", "Namespaces", "Что процесс видит"],
    ["cg", "Cgroups", "Сколько ему можно"],
    ["img", "Слои", "Из чего собран образ"],
    ["vol", "Тома", "Где живут данные"],
  ];
  return (
    <Slide
      n={1}
      title="Контейнеры: изоляция без магии"
      sub="Глава 9 · Что под красивой обёрткой"
      main="Контейнер — обыкновенные механизмы ядра: понимание превращает шаманство в инструмент."
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
        «Работает у меня, но не работает у тебя» — старая боль, которую лечат
        контейнеры.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Пространства имён"
      sub="Ядро показывает процессу урезанную картину мира"
      main="Это маска, а не копия машины: за каждой стенкой тот же хост — процесс его просто не видит."
    >
      <div className="s-cols">
        <Node mono title="pid" sub="Своё дерево процессов" />
        <Node mono title="net" sub="Свой сеть и адреса" />
        <Node mono title="mnt" sub="Свои монтирования" />
        <Node mono title="user" sub="Свои пользователи" />
      </div>
      <Node
        title="Внутри контейнера"
        sub="Процесс с номером один уверен: он первый и единственный"
      />
      <p className="s-hint">
        Виртуализации железа нет — и в этом секрет скорости: контейнеры не
        эмулируют, а фильтруют.
      </p>
    </Slide>
  );
}

function S03() {
  const rows = [
    ["cpu", "квота процессора"],
    ["memory", "лимит памяти"],
    ["pids", "число процессов"],
    ["blkio", "приоритет диска"],
  ];
  return (
    <Slide
      n={3}
      title="Контрольные группы"
      sub="Namespaces — что видит, cgroups — сколько можно"
      main="Лимиты — договор: завышенные съедают хост, заниженные душат работу. Настраивать по метрикам."
    >
      <div className="s-label">ЧТО ОГРАНИЧИВАЕТ CGROUP</div>
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <Node
        amber
        title="Контейнер молча умер?"
        sub="Это мог быть убийца памяти: сообщение живёт в журнале ядра хоста, а не в логах контейнера"
      />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Образ: стопка слоёв"
      sub="Слои только для чтения, сверху — тонкий записываемый"
      main="Записываемый слой исчезает вместе с контейнером: всё важное — в томах или в слоях образа."
    >
      <div className="s-cols">
        <Node mono title="base" sub="Дистрибутив" />
        <Arr />
        <Node mono title="deps" sub="Зависимости" />
        <Arr />
        <Node mono title="app" sub="Ваш код" />
      </div>
      <Down />
      <Node
        amber
        title="Записываемый слой"
        sub="Тонкий и временный: живёт и умирает вместе с контейнером"
      />
      <p className="s-hint">
        Отсюда и скорость, и экономия: сборка переиспользует слои, разные образы
        делят общий базовый.
      </p>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Сборка образа"
      sub="Порядок инструкций — это кэш"
      main="Итог — образ в разы меньше и с меньшей поверхностью атаки."
    >
      <div className="s-grid2">
        <Node green title="Редко меняется" sub="Ставим раньше: база, зависимости" />
        <Node amber title="Меняется постоянно" sub="Ставим позже: код, конфиги" />
      </div>
      <div className="s-label">МНОГОСТУПЕНЧАТАЯ СБОРКА</div>
      <Cmd>{"FROM base AS build\nRUN make all\nFROM minimal\nCOPY --from=build /app /app"}</Cmd>
      <div className="s-note">
        Уборка в той же инструкции: кэш пакетного менеджера не должен остаться в
        слое.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Docker, Podman, LXC"
      sub="Разные пульты — одна механика"
      main="Выбор инструмента — вопрос вкуса и политики компании, а понимание — общее."
    >
      <div className="s-cols">
        <Node title="Docker" sub="Демон управляет, клиент говорит с демоном" />
        <Node green title="Podman" sub="Без демона и без рута — дружелюбно к безопасности" />
        <Node title="LXC" sub="Лёгкая виртуалка со своей инициализацией" />
      </div>
      <p className="s-hint">
        Разница в философии, но механика одна: пространства имён, контрольные
        группы, слоёные образы.
      </p>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Реестры и теги"
      sub="Тег — имя версии, но не гарантия"
      main="Пинуйте хэши, держите свой реестр и чистите старые слои — диски кончаются незаметно."
    >
      <Node
        amber
        mono
        title="myapp:latest"
        sub="«Последний попавшийся»: сборка сегодня и завтра может дать разные образы"
      />
      <Down />
      <Node
        green
        mono
        title="myapp@sha256:4f2a…"
        sub="Неизменяемый адрес конкретной сборки — воспроизводимость"
      />
      <p className="s-hint">
        Регулярная чистка старых слоёв спасает диски от гигабайт невидимого
        мусора.
      </p>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Данные — в томах"
      sub="Записываемый слой тонкий и временный"
      main="Две заповеди: база — всегда в томе, том — всегда в бэкапе."
    >
      <div className="s-grid2">
        <Node
          green
          mono
          title="named volume"
          sub="Именованный том: управляет инструмент, легко бэкапить"
        />
        <Node
          amber
          mono
          title="bind mount"
          sub="Связка с каталогом хоста: для разработки и особых случаев"
        />
      </div>
      <Node
        amber
        title="База внутри контейнера"
        sub="Классическая ошибка: пересоздание контейнера стирает всё"
      />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Сеть контейнеров"
      sub="По умолчанию — частная сеть моста"
      main="Отладка начинается с вопроса: недоступно изнутри контейнера или снаружи? Ответы ведут в разные стороны."
    >
      <div className="s-cols">
        <Node mono title="container" sub="Внутренний адрес" />
        <Arr />
        <Node mono title="bridge" sub="Частная сеть" />
        <Arr />
        <Node title="host" sub="Наружу через подмену адресов" />
      </div>
      <div className="s-label">ПУБЛИКАЦИЯ ПОРТА</div>
      <Cmd>{"docker run -p 8080:80"}</Cmd>
      <Node
        green
        title="Встроенный DNS"
        sub="Внутри одной сети контейнеры видят друг друга по именам"
      />
    </Slide>
  );
}

function S10() {
  const rows = [
    ["userns", "рут внутри → непривилегированный на хосте"],
    ["cap-drop", "лишние возможности ядра отобраны"],
    ["read-only", "файловая система только для чтения"],
  ];
  return (
    <Slide
      n={10}
      title="Безопасность контейнера"
      sub="Рут внутри — не то же, что рут на хосте, но и не полная изоляция"
      main="Прорвавшись через уязвимость ядра, процесс оказывается на хосте: контейнер — слой, а не граница."
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
        Каждый пункт — флаг запуска или строка настройки. По умолчанию процесс в
        контейнере — рут внутри своих пространств имён.
      </p>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Контейнер и виртуалка"
      sub="Честное сравнение"
      main="Гибрид нормален и распространён: контейнеры живут внутри виртуалок."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">ВИРТУАЛКА</div>
          <span className="s-node-title">Целая гостевая система на гипервизоре</span>
          <span className="s-node-sub">
            Изоляция максимальная · цена — память и секунды на старт
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">КОНТЕЙНЕР</div>
          <span className="s-node-title">Процессы хоста в масках</span>
          <span className="s-node-sub">
            Старт за миллисекунды · плотность выше · изоляция по границам ядра
          </span>
        </div>
      </div>
      <div className="s-label">КОГДА ЧТО</div>
      <div className="s-opts">
        <span className="s-path accent">ВМ</span>
        <span>чужое ядро, базы с жёсткими требованиями</span>
        <span className="s-path accent">Контейнеры</span>
        <span>службы, конвейеры, среды разработки</span>
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Compose"
      sub="Один декларативный файл: службы, сети, тома"
      main="Файл живёт в репозитории — новый человек поднимает окружение за минуты."
    >
      <Cmd>{"docker compose up -d\ndocker compose down"}</Cmd>
      <Node
        green
        title="Декларация вместо устной инструкции"
        sub="Подняли весь мир одной командой, другой — снесли"
      />
      <p className="s-hint">
        Для продакшена этого мало — там оркестратор; как среда разработки и
        тестирования композиции идеальны.
      </p>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Оркестрация"
      sub="Когда контейнеров десятки на десятках машин"
      main="Без фундамента кубернес — магия и боль, с фундаментом — логичная надстройка."
    >
      <div className="s-cols">
        <Node mono title="schedule" sub="Расписать по машинам" />
        <Arr />
        <Node mono title="health" sub="Следить за здоровьем" />
        <Arr />
        <Node mono title="scale" sub="Масштабировать" />
      </div>
      <Node
        title="Обновления без простоя"
        sub="Перекатывание версий — тоже работа оркестратора"
      />
      <p className="s-hint">
        Фундамент один — то, что вы уже выучили: образы, лимиты, сети, тома.
      </p>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Живость и готовность"
      sub="Две разные проверки здоровья"
      main="Трафик на живой, но не готовый процесс — ошибки на старте. Различайте проверки."
    >
      <div className="s-grid2">
        <Node
          green
          mono
          title="liveness"
          sub="Жив ли процесс: нет — перезапустить"
        />
        <Node
          amber
          mono
          title="readiness"
          sub="Готов ли принимать запросы: живой ≠ готовый"
        />
      </div>
      <div className="s-label">ЛОГИ БЕЗ ВХОДА ВНУТРЬ</div>
      <Cmd>{"docker logs -f myapp"}</Cmd>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Антипаттерны"
      sub="Встречаются в дикой природе"
      main="Контейнеры — про одну службу и процесс с номером один."
    >
      <div className="s-blocks">
        <div className="s-block">
          Образ, ставящий обновления при каждом запуске: обновления — это
          пересборка, сборка должна быть воспроизводимой
        </div>
        <div className="s-block">
          Секреты, запечённые в слоях образа: слои навсегда — удалить секрет
          нельзя, только пересобрать всё
        </div>
        <div className="s-block">
          Состояние в записываемом слое: контейнер пересоздали — данные исчезли
        </div>
        <div className="s-block changed">
          Десять служб в одном контейнере с процесс-менеджером внутри — так не
          надо
        </div>
      </div>
    </Slide>
  );
}

function S16() {
  const rows = [
    ["base image", "обновления безопасности — ваша пересборка по просьбе"],
    ["logs", "вывозить наружу: иначе умирают вместе с контейнером"],
    ["kernel", "общее ядро — общие уязвимости: обновлять как можно чаще"],
  ];
  return (
    <Slide
      n={16}
      title="Чего контейнер не решает"
      sub="Зона вашей ответственности"
      main="Контейнер — инструмент упаковки, а не замена дисциплине."
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

function S17() {
  return (
    <Slide
      n={17}
      title="Практика на сегодня"
      sub="Четыре упражнения"
      main="Посмотрите на процессы контейнера глазами хоста — маска станет видимой."
    >
      <div className="s-blocks">
        <div className="s-block">
          Соберите образ своего скрипта: база, копирование, команда запуска —
          три строки
        </div>
        <div className="s-block">
          Зайдите внутрь: его процессы, его сеть, его корень
        </div>
        <div className="s-block">
          Положите данные в том, пересоздайте контейнер — данные живы
        </div>
        <div className="s-block changed">
          Ограничьте память и доведите до лимита: теперь вы знаете, где искать
          сообщение
        </div>
      </div>
      <Cmd>{"docker run -it --rm -m 100m myscript"}</Cmd>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Размер базового образа"
      sub="Сотни мегабайт или десятки"
      main="Базовый образ — половина вашего образа: проверяйте его придирчиво, как код приложения."
    >
      <div className="s-bar-wrap">
        <span>Полный дистрибутив · сотни МБ инструментов</span>
        <div className="s-bar">
          <div style={{ width: "100%" }} />
        </div>
        <span className="amber-text">Минимальный образ · десятки МБ</span>
        <div className="s-bar amber">
          <div style={{ width: "12%" }} />
        </div>
      </div>
      <div className="s-grid2">
        <Node
          green
          title="Минимальный образ"
          sub="Минимум библиотек и поверхности атаки, быстрее доставка"
        />
        <Node
          amber
          title="Цена минимализма"
          sub="Отладочные инструменты иногда ставим вручную — для продакшена цена мизерная"
        />
      </div>
    </Slide>
  );
}

function S19() {
  const rows = [
    ["~80 %", "логи сборки: печатают слой и причину — читать целиком"],
    ["~15 %", "пути и права: не исполним, не скопирован, нет каталога"],
    ["~5 %", "сеть и реестры"],
  ];
  return (
    <Slide
      n={19}
      title="Не собирается, не стартует"
      sub="Где живут ответы"
      main="Методика всей книги: читать сообщение об ошибке честно, от начала до конца."
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
        Логи сборки печатают, на каком слое и почему упала, — а не только
        последние строки.
      </p>
    </Slide>
  );
}

function S20() {
  return (
    <Slide
      n={20}
      title="Разработка локально"
      sub="Вход в новый проект — минуты вместо дней"
      main="Окружение разработки — миниатюра прода, а не выдумка."
    >
      <div className="s-cols">
        <Node mono title="db" />
        <Node mono title="cache" />
        <Node mono title="queue" />
      </div>
      <Down />
      <Node
        green
        title="Поднято из декларативного файла"
        sub="Кодим сразу, не настраивая машину"
      />
      <Node
        amber
        title="Версии сервисов = прод"
        sub="Рассинхрон даёт баги, которых нет ни там, ни там"
      />
    </Slide>
  );
}

function S21() {
  return (
    <Slide
      n={21}
      title="Контейнер — расходник"
      sub="Новое мышление"
      main="Вместо «чинить живое» — пересобрать из описания. Половина страха перед продакшеном уходит."
    >
      <div className="s-cols">
        <Node amber title="Виртуалка" sub="Поднималась минуты — жалко выключать" />
        <Node green title="Контейнер" sub="Устарел — пересоздали из образа за секунды" />
      </div>
      <Down />
      <Node
        title="Дорогое состояние — вовне"
        sub="Тома и базы: при пересоздании ничего не теряется"
      />
    </Slide>
  );
}

function S22() {
  const topics = [
    ["ns", "Namespaces", "Что я вижу"],
    ["cg", "Cgroups", "Сколько мне можно"],
    ["img", "Слои", "Из чего я собран"],
    ["vol", "Тома и хэши", "Данные вне контейнера, версии по хэшам"],
  ];
  return (
    <Slide
      n={22}
      title="Итог"
      sub="Глава 9 · Изоляция без магии"
      main="Следующая глава — само ядро: модули, настройки и трассировка живых процессов."
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
        Докер и подман — удобные пульты к обыкновенным механизмам ядра: данные —
        в томах, версии — по хэшам, публикация — через проброс портов.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_CH9 = {
  "8:9": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_CH9).
export const SLIDE_TITLES_CH9 = {
  "8:9": [
    "Введение",
    "Пространства имён",
    "Контрольные группы",
    "Слои образа",
    "Сборка образа",
    "Docker, Podman, LXC",
    "Реестры и теги",
    "Данные в томах",
    "Сеть контейнеров",
    "Безопасность",
    "Контейнеры и виртуалки",
    "Compose",
    "Оркестрация",
    "Живость и готовность",
    "Антипаттерны",
    "Чего не решает",
    "Практика",
    "Размер образа",
    "Отладка сборки",
    "Разработка локально",
    "Контейнер — расходник",
    "Итог",
  ],
};
