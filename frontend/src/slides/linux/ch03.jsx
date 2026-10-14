// Слайды для «Linux: от шелла до ядра», глава 3 — «Права доступа: владельцы, биты и судо».
// Тот же дизайн-код, что и глава 2: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ПРАВА, ПРОЦЕССЫ, СЛУЖБЫ / ГЛАВА 3</span>
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

function Node({ mono, green, amber, title, sub }) {
  const kind = green ? "green" : amber ? "amber" : "";
  return (
    <div className={`s-node ${kind}`.trim()}>
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
    ["u", "Владельцы", "Пользователь, группа и прочие у каждого файла"],
    ["rwx", "Биты прав", "Чтение, запись, исполнение — буквами и числами"],
    ["$", "Судо", "Повышение на одну команду, с подотчётностью"],
    ["+", "ACL", "Права точечно, когда трёх категорий мало"],
  ];
  return (
    <Slide
      n={1}
      title="Права доступа: владельцы, биты и судо"
      sub="Глава 3 · Многопользовательская система"
      main="Модель прав защищает процессы друг от друга, сервисы от людей, систему от самих себя."
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
        Большинство «загадочных» ошибок развёртывания — это права доступа,
        замаскированные под баг в коде.
      </p>
    </Slide>
  );
}

function S02() {
  const rows = [
    ["r", "файл: прочитать · каталог: видеть имена"],
    ["w", "файл: изменить · каталог: создавать и удалять записи"],
    ["x", "файл: запустить · каталог: вход внутрь и доступ к содержимому"],
  ];
  return (
    <Slide
      n={2}
      title="Владелец, группа, прочие"
      sub="Три категории — и три права на каждую"
      main="Права на каталог — не права на его содержимое: исполнение даёт вход, запись — создание и удаление."
    >
      <div className="s-cols">
        <Node green title="Владелец" sub="Хозяин файла" />
        <Node title="Группа" sub="Участники получают общие права" />
        <Node title="Прочие" sub="Все остальные" />
      </div>
      <div className="s-label">ПРАВО ДЛЯ ФАЙЛА И ДЛЯ КАТАЛОГА</div>
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note amber">
        Каталог с чтением, но без исполнения: имена видны, файлы не открыть —
        это точная математика, а не поломка.
      </div>
    </Slide>
  );
}

function S03() {
  const digits = [
    ["4", "чтение"],
    ["2", "запись"],
    ["1", "исполнение"],
  ];
  return (
    <Slide
      n={3}
      title="Числа и chmod"
      sub="Право категории — сумма битов"
      main="Неверный рекурсивный chmod превращает сотни файлов в странно сломанные за одну секунду."
    >
      <div className="s-table">
        {digits.map(([d, name]) => (
          <div key={d}>
            <span className="s-path accent">{d}</span>
            <span>{name}</span>
          </div>
        ))}
      </div>
      <div className="s-cols">
        <Node mono title="754" sub="владелец: всё · группа и прочие: читать и запускать" />
        <Arr />
        <Node mono green title="chmod 754" sub="меняет права" />
      </div>
      <Cmd>
        {"chmod 754 app.sh             — права числами\nchown deploy:deploy app.sh   — владелец и группа\nchmod -R 644 каталог/        — рекурсивно, осторожно"}
      </Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Кто такие владелец и группа"
      sub="Записи в системных таблицах"
      main="Взломанный веб-сервер должен упереться в права, а не получить весь диск."
    >
      <div className="s-grid2">
        <Node
          title="Пользователь"
          sub="Имя · числовой идентификатор · домашний каталог"
        />
        <Node title="Группа" sub="Имя · список участников" />
      </div>
      <div className="s-label">СЕРВИСЫ ЖИВУТ СВОИМИ УЧЁТКАМИ</div>
      <Cmd>{"www-data · postgres · redis\nnologin · без пароля · без входа"}</Cmd>
      <Node
        amber
        title="Запуск сервиса от рута"
        sub="Двойная ошибка: и риск, и признак настройки наспех"
      />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Маска новых файлов"
      sub="Максимум минус umask"
      main="У одного разработчика новые файлы читаемы всеми, у другого нет — разгадка в разных масках из разных файлов настройки."
    >
      <div className="s-cols">
        <Node mono title="666" sub="максимум для файла" />
        <Arr />
        <Node amber mono title="022" sub="обычная маска шелла" />
        <Arr />
        <Node green mono title="644" sub="владелец пишет, остальные читают" />
      </div>
      <div className="s-label">КАТАЛОГАМ ДОБАВЛЯЕТСЯ ИСПОЛНЕНИЕ</div>
      <Cmd>{"umask            — показать текущую\numask 022        — на один сеанс\numask 022        — навсегда, в файле настройки шелла"}</Cmd>
      <p className="s-hint">
        Маску шелл передаёт каждому потомку — её вычитают из максимума при
        создании файла.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Три специальных бита"
      sub="Над моделью прав"
      main="Специальные биты решают частные задачи: системные утилиты, общие папки, временные каталоги."
    >
      <div className="s-cols">
        <Node
          mono
          title="setuid"
          sub="Программа работает с правами владельца файла: так passwd пишет в защищённую базу"
        />
      </div>
      <div className="s-grid2">
        <Node
          mono
          title="setgid"
          sub="На каталоге: новые файлы наследуют группу — общие папки команды"
        />
        <Node
          mono
          title="sticky"
          sub="На каталоге: удалять может только владелец файла — как в /tmp"
        />
      </div>
      <Cmd>{"chmod u+s программа  ·  chmod g+s каталог/  ·  chmod +t каталог/"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Судо вместо рута"
      sub="Повышение с подотчётностью"
      main="Повышение на одну команду лучше пожизненного всевластия: ключи от квартиры выдают на время."
    >
      <div className="s-cols">
        <Node amber title="Рут" sub="Может всё: опечатка без прав — мелочь, с правами — катастрофа" />
        <Node
          green
          title="Судо"
          sub="Одна команда с повышением и паролем — вашим собственным, не рутовым"
        />
      </div>
      <Cmd>{"sudo systemctl restart nginx"}</Cmd>
      <div className="s-note">
        Судо ведёт журнал: кто, когда и что запускал. Общий рут на всю команду
        подотчётности не даёт.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Файл правил судо"
      sub="Кто, где, от чьего имени и что"
      main="Редактор с правами рута — это судо на всё, просто по диагонали: остерегайтесь программ, умеющих уходить в шелл."
    >
      <div className="s-label">ПРАВИТСЯ ТОЛЬКО С ПРОВЕРКОЙ СИНТАКСИСА</div>
      <Cmd>
        {"visudo\n%deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart app"}
      </Cmd>
      <div className="s-grid2">
        <Node
          green
          title="Минимальная достаточность"
          sub="Кто перезапускает сервис — тому судо на одну команду, не на всё"
        />
        <Node
          amber
          title="Сломанный файл"
          sub="Может отнять доступ к собственному серверу"
        />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Су: полное переключение"
      sub="Пожить жизнью сервисного пользователя"
      main="Если под сервисным пользователем всё работает, а под вашим нет — почти всегда права файлов или окружение."
    >
      <Cmd>{"su - www-data\nwhoami · env · ls -l"}</Cmd>
      <div className="s-grid2">
        <Node
          title="Что проверять"
          sub="Права, переменные окружения, доступ к файлам — его глазами"
        />
        <Node
          green
          title="Когда помогает"
          sub="Разбор загадочных отказов в доступе экономит часы гаданий"
        />
      </div>
      <Down />
      <div className="s-note">
        Это упражнение стоит включить в любой чек-лист диагностики: сервис
        видит не то, что видите вы.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Расширенные списки ACL"
      sub="Когда трёх категорий мало"
      main="После долгой настройки прав файл всё равно не читается? Сначала посмотрите ACL — в обычном выводе они незаметны."
    >
      <div className="s-label">КОНКРЕТНОМУ ЧЕЛОВЕКУ — КОНКРЕТНОЕ ПРАВО</div>
      <Cmd>{"setfacl -m u:analytics:r /var/log/app\ngetfacl /var/log/app"}</Cmd>
      <div className="s-grid2">
        <Node
          title="Поверх модели"
          sub="Сервис читает сертификаты, аналитик — логи, без вступления в группу"
        />
        <Node
          title="Наследование"
          sub="На каталоге: всё новое автоматически получает те же права"
        />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Атрибуты файлов"
      sub="Права выше уровня модели"
      main="Зная слои системы, вы всегда знаете, где искать."
    >
      <div className="s-label">ФЛАГ НЕИЗМЕНЯЕМОСТИ</div>
      <Cmd>{"chattr +i /etc/critical.conf   — защитить\nchattr -i /etc/critical.conf   — снять осознанно"}</Cmd>
      <Down />
      <Node
        amber
        title="Даже рут бессилен"
        sub="Файл не удалить и не изменить: проверьте атрибуты, прежде чем грешить на порчу диска"
      />
      <div className="s-note">
        Так защищают критичные настройки и точки монтирования от случайной
        перезаписи.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Продакшен-истории"
      sub="Три классики про права"
      main="Все три случая лечатся за минуту, если понимать модель, и съедают вечер, если не понимать."
    >
      <div className="s-blocks">
        <div className="s-block">
          Приложение перестало читать конфиг: сервис работает от нового
          пользователя, а файл принадлежит старому
        </div>
        <div className="s-block">
          Ключ по сети не работает: приватный ключ должен читать только
          владелец — не паранойя, а защита
        </div>
        <div className="s-block">
          Логи перестали писаться после ротации: новый файл создался с чужой
          группой
        </div>
        <div className="s-block changed">
          Понимание модели прав отличает минуту починки от вечера гаданий
        </div>
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Вредные советы"
      sub="Классика из интернета"
      main="Оба совета — маркеры спешки: правильное решение на пять минут дольше."
    >
      <div className="s-cols">
        <Node
          amber
          title="Поставить всем все права"
          sub="Ошибка исчезнет вместе с защитой: уязвимый сервис откроет файловую систему"
        />
        <Node
          amber
          title="Запустить всё от рута"
          sub="Работать будет — до первого взлома или бага с максимумом власти"
        />
      </div>
      <Down />
      <Node
        green
        title="Правильно"
        sub="Ровно нужное право — нужному владельцу"
      />
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Философия прав"
      sub="Кто за что отвечает"
      main="Принцип минимальных прав чаще спасает от собственных ошибок, чем от злодеев."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">ЯВНОСТЬ</div>
          <span className="s-node-title">Каждая связь видна в модели</span>
          <span className="s-node-sub">
            Сервис читает только нужное · человек пишет только куда положено
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">САМОДОКУМЕНТАЦИЯ</div>
          <span className="s-node-title">Права описывают устройство</span>
          <span className="s-node-sub">
            Глядя на владельцев и группы, видишь, как устроена система
          </span>
        </div>
      </div>
      <div className="s-note">
        Права — не галочка безопасности для отчёта, а способ выразить
        ответственность.
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Практика на сегодня"
      sub="Четыре упражнения"
      main="Исполняемых файлов с битом подмены владельца считанные десятки — их список стоит знать."
    >
      <div className="s-blocks">
        <div className="s-block">
          Пройдитесь поиском по домашней папке в поисках файлов с широкими
          правами — и удивитесь
        </div>
        <div className="s-block">
          Найдите все исполняемые файлы с битом подмены владельца: каждый —
          потенциальный путь к руту
        </div>
        <div className="s-block">
          Общий каталог для двух пользователей: группа плюс групповой бит,
          проверьте редактирование чужих файлов
        </div>
        <div className="s-block changed">
          Эй-си-эль: дайте право читать файл пользователю, который им не
          владеет
        </div>
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Копирование и перемещение"
      sub="Что происходит с правами"
      main="После копирования конфигов и скриптов права выставляют заново — привычно и без сюрпризов."
    >
      <div className="s-cols">
        <Node
          mono
          title="cp"
          sub="Новый файл: права по маске, владелец — тот, кто копировал"
        />
        <Arr />
        <Node
          mono
          title="mv"
          sub="Переименование записи: права остаются при файле"
        />
      </div>
      <div className="s-note amber">
        Скопировали исполняемый скрипт — запуск может не сработать: бит
        исполнения не переехал.
      </div>
      <Cmd>{"chmod +x deploy.sh\nchown deploy:deploy app.conf"}</Cmd>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Группы в системе"
      sub="Самый недоиспользованный инструмент"
      main="Добавили в группу — нужен новый вход в систему: старые сеансы про новые группы не знают."
    >
      <div className="s-label">ГРУППЫ — НЕ ТОЛЬКО КОМАНДЫ ЛЮДЕЙ</div>
      <div className="s-opts">
        <span className="s-path accent">adm</span>
        <span>чтение журналов</span>
        <span className="s-path accent">systemd-journal</span>
        <span>доступ к журналу</span>
        <span className="s-path accent">docker</span>
        <span>право на демон</span>
      </div>
      <Cmd>{"groups  ·  id"}</Cmd>
      <div className="s-note">
        Пользователь может состоять в десятке групп, и каждая даёт свои права:
        половина вопросов «почему я не могу прочитать лог» решается добавлением
        в нужную группу.
      </div>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Права ссылок"
      sub="Чинить цель, а не ссылку"
      main="Проверяются права не ссылки, а файла, на который она указывает."
    >
      <div className="s-grid2">
        <Node
          mono
          title="ln -s"
          sub="Символическая: почти всегда полные права для всех — и это ничего не значит"
        />
        <Node
          mono
          title="ln"
          sub="Жёсткая: тот же инод — права общие с оригиналом"
        />
      </div>
      <Down />
      <Node
        amber
        title="Чинить цель"
        sub="Права на ссылку чинить бессмысленно — смотрите на файл, куда она указывает"
      />
    </Slide>
  );
}

function S19() {
  const topics = [
    ["u", "Категории", "Владелец, группа, прочие — и три права на каждую"],
    ["s", "Биты", "Подмена владельца, наследование группы, липкость"],
    ["$", "Судо", "Повышение с подотчётностью и минимальной достаточностью"],
    ["+", "ACL", "Достраивает модель, когда трёх категорий мало"],
  ];
  return (
    <Slide
      n={19}
      title="Итог"
      sub="Глава 3 · Владельцы, биты и судо"
      main="Дальше — процессы и сигналы: как программы живут, засыпают, умирают и почему иногда не умирают совсем."
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
        Для каталогов исполнение означает вход: классические ловушки прав —
        это точная математика.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_CH3 = {
  "8:3": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_CH3).
export const SLIDE_TITLES_CH3 = {
  "8:3": [
    "Введение: права",
    "Владелец, группа, прочие",
    "Числа и chmod",
    "Владельцы и группы",
    "Маска umask",
    "Специальные биты",
    "Судо вместо рута",
    "Файл sudoers",
    "Команда su",
    "Расширенные ACL",
    "Атрибуты файлов",
    "Продакшен-истории",
    "Вредные советы",
    "Философия прав",
    "Практика",
    "Копирование и перемещение",
    "Группы в системе",
    "Права ссылок",
    "Итог",
  ],
};
