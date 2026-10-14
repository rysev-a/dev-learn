// Слайды для «Linux: от шелла до ядра», глава 7 — «Диски, тома и бэкапы».
// Тот же дизайн-код, что и глава 2: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СЕТЬ И ХРАНЕНИЕ / ГЛАВА 7</span>
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
  const layers = [
    ["[]", "Разделы", "Диск — как дом, поделённый на квартиры"],
    ["fs", "Файловые системы", "Журналируемые лошадки и молодая ветка с CoW"],
    ["LV", "Тома", "Границы двигаются на живой системе"],
    ["RA", "Массивы и бэкапы", "Защита от смерти диска и от потери данных"],
  ];
  return (
    <Slide
      n={1}
      title="Диски, тома и бэкапы"
      sub="Глава 7 · Слоёный пирог хранения"
      main="«Диск умер» — не приговор, а инструкция к действию."
    >
      <div className="s-grid2">
        {layers.map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">
        Диски — единственные крупные механические детали дата-центра, и потому
        единственные, что умирают гарантированно.
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Разметка диска"
      sub="Старый формат против нового"
      main="Новые диски — новый формат: таблица разделов с копией в конце диска не умрёт от одной царапины."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">СТАРЫЙ ФОРМАТ</div>
          <span className="s-node-title">Предел два терабайта</span>
          <span className="s-node-sub">
            Горстка разделов · одна копия таблицы · древние машины и флешки
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">НОВЫЙ ФОРМАТ</div>
          <span className="s-node-title">Разделы с именами</span>
          <span className="s-node-sub">
            Контрольные суммы · копия таблицы в конце диска · грузит современная
            прошивка
          </span>
        </div>
      </div>
      <p className="s-hint">
        Практический вывод: на новых дисках — новый формат, и спать спокойно.
      </p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Файловая система над разделом"
      sub="Перезапись на месте против копирования при записи"
      main="Разница парадигм меняет поведение под нагрузкой и цену снимков."
    >
      <div className="s-grid2">
        <Node
          green
          mono
          title="ext4 · xfs"
          sub="Рабочие лошадки: журналируемые, быстрые, проверенные десятилетиями"
        />
        <Node
          mono
          title="btrfs и родня"
          sub="Копирование при записи: снимки, контрольные суммы, прозрачное сжатие"
        />
      </div>
      <div className="s-label">ВЫБОР</div>
      <div className="s-opts">
        <span className="s-path accent">общая машина</span>
        <span>лошадка по вкусу дистрибутива</span>
        <span className="s-path accent">хранилище</span>
        <span>молодая ветка — снимки и бэкапы</span>
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Слой томов LVM"
      sub="Лечение главной боли: диск кончился"
      main="Добавить устройство в группу, расширить том, расширить ФС — без остановки сервиса."
    >
      <div className="s-tree">
        <div className="s-cols">
          <Node mono title="/dev/sdb" sub="Физическое устройство" />
          <Node mono title="/dev/sdc" sub="Ещё одно" />
        </div>
        <Down />
        <Node title="Группа томов" sub="Единый котёл ёмкости" />
        <Down />
        <div className="s-grid2">
          <Node green mono title="том-данные" sub="Расширяется на живую" />
          <Node mono title="том-архив" sub="Границы двигаются" />
        </div>
      </div>
      <div className="s-note amber">
        Цена — ещё один слой абстракции: неполный том при диагностике выглядит
        как глючный диск.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Копия живой базы"
      sub="Классический рецепт со снимком"
      main="База видит нулевую паузу, копия получает согласованное состояние."
    >
      <div className="s-blocks">
        <div className="s-block">
          Снимок тома занимает секунды: данные заморожены в один момент времени
        </div>
        <div className="s-block">
          Копируем со снимка эрсинком — файлы согласованы между собой
        </div>
        <div className="s-block">Снимок удаляем — место вернулось</div>
      </div>
      <Cmd>{"snapshot → rsync → snapshot remove"}</Cmd>
      <div className="s-note">
        Тот же рецепт для обновлений: снимок перед рискованным апдейтом — и
        откат занимает минуту, если что-то пошло не так.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="RAID: отказоустойчивый массив"
      sub="Объединение дисков с избыточностью"
      main="Критическая правда жизни: массив — не бэкап."
    >
      <div className="s-cols">
        <Node green title="Зеркало" sub="Всё в двух экземплярах: умер один — живёт второй" />
        <Node amber title="Чередование" sub="Скорость, но отказ одного диска убивает всё" />
        <Node title="Суммы" sub="Комбинированные режимы: избыточность вычислениями" />
      </div>
      <div className="s-note amber">
        Массив защищает от смерти диска, но не от команды удаления,
        вируса-шифровальщика или пожара — многие узнали это слишком дорого.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Своп"
      sub="Куда ядро выгружает холодные страницы"
      main="Постоянное активное свопирование — симптом нехватки памяти, лечится памятью, а не настройками."
    >
      <div className="s-grid2">
        <Node amber title="Старая мудрость" sub="Своп в два раза больше памяти" />
        <Node green title="Современная" sub="Небольшой амортизатор, а не место для жизни" />
      </div>
      <div className="s-label">ТОНКАЯ НАСТРОЙКА</div>
      <Cmd>{"sysctl vm.swappiness"}</Cmd>
      <div className="s-opts">
        <span className="s-path accent">выше</span>
        <span>агрессивная выгрузка — десктоп</span>
        <span className="s-path accent">ниже</span>
        <span>сдержанная — сервер с базой</span>
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Диски предупреждают о смерти"
      sub="Телеметрия самоконтроля"
      main="Растущие переназначенные сектора — это не «вдруг», это «уже»: месяцы до клинической смерти — вопрос везения."
    >
      <div className="s-grid2">
        <Node amber mono title="Переназначенные сектора" sub="Главный тревожный счётчик" />
        <Node mono title="Ошибки чтения" sub="Диск уже спорит с данными" />
        <Node mono title="Температура" sub="Перегрев сокращает жизнь" />
        <Node mono title="Часы работы" sub="Возраст в телеметрии" />
      </div>
      <Cmd>{"smartctl -a /dev/sda"}</Cmd>
      <div className="s-note">
        Регулярная проверка по расписанию с письмом — пятнадцать минут
        настройки, которые однажды спасут выходные.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Архивы: tar и сжатие"
      sub="Дерево файлов в один поток"
      main="Три глагола — собрать, распаковать, посмотреть — вы будете использовать десятилетиями."
    >
      <div className="s-cols">
        <Node green mono title="собрать" />
        <Node mono title="распаковать" />
        <Node mono title="посмотреть" />
      </div>
      <Cmd>
        {
          "tar -czf backup-2026.tar.gz каталог/\ntar -xzf backup-2026.tar.gz -C чистый/\ntar -tzf backup-2026.tar.gz"
        }
      </Cmd>
      <div className="s-label">СЖАТИЕ — ОТДЕЛЬНЫЙ СЛОЙ</div>
      <div className="s-opts">
        <span className="s-path accent">gzip</span>
        <span>классика, универсален</span>
        <span className="s-path accent">zstd</span>
        <span>новое поколение: лучший баланс скорости и размера</span>
      </div>
      <p className="s-hint">
        Практика на вечер: собрать каталог с датой в имени, распаковать в
        чистый каталог, сравнить списки файлов.
      </p>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Побайтовое копирование dd"
      sub="Мощь и опасность в одном флаконе"
      main="Работайте с образами через файлы, а не с живыми дисками."
    >
      <Cmd>{"dd if=образ.img of=/dev/sdX status=progress"}</Cmd>
      <Node
        amber
        title="Перепутали вход и выход — целевой диск перезаписан бесследно"
        sub="Никаких корзин и сожалений: прозвище «разрушитель дисков» — не шутка, а статистика"
      />
      <div className="s-label">ГДЕ ИСПОЛЬЗУЕТСЯ</div>
      <div className="s-blocks">
        <div className="s-block">Образы флешек</div>
        <div className="s-block">Миграции маленьких дисков</div>
        <div className="s-block changed">Надёжная зачистка</div>
      </div>
      <div className="s-note">
        Имена устройств перепроверяйте дважды и трижды перед запуском.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Синхронизация rsync"
      sub="Копирует только отличия"
      main="Сначала сухой прогон с отчётом, глазами, потом настоящий запуск."
    >
      <Cmd>
        {
          "rsync -avh источник/ user@host:/backup/\nrsync -avh --delete --dry-run источник/ приёмник/"
        }
      </Cmd>
      <div className="s-label">ФЛАГИ</div>
      <div className="s-opts">
        <span className="s-path accent">-a</span>
        <span>права и владельцы</span>
        <span className="s-path accent">-v</span>
        <span>отчёт</span>
        <span className="s-path accent">--delete</span>
        <span>удалять лишнее в приёмнике</span>
        <span className="s-path accent">--dry-run</span>
        <span>сухой прогон</span>
      </div>
      <div className="s-note amber">
        Флаг удаления — оружие: опечатка в источнике стирает данные и там.
        Первый запуск — полный, последующие — мгновенные.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Стратегия 3-2-1"
      sub="Вся стратегия бэкапов в трёх числах"
      main="Диск умрёт, здание затопит, шифровальщик зашифрует всё, до чего дотянется, включая сетевые копии."
    >
      <div className="s-cols">
        <Node green mono title="3" sub="Копии данных" />
        <Node mono title="2" sub="Разных носителя" />
        <Node amber mono title="1" sub="Копия вне здания" />
      </div>
      <div className="s-note">
        Невосстановленный бэкап — это не бэкап. Раз в квартал — учения:
        развернуть копию на чистой машине, открыть данные, замерить время.
      </div>
      <p className="s-hint">
        Историй о компаниях, годами плативших за копии, которые никто ни разу
        не раскрыл, — десятки.
      </p>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Шифрование копий"
      sub="Ключ должен быть только у вас"
      main="Потеря ключа равна потере данных."
    >
      <div className="s-cols">
        <Node green title="Шифруйте у себя" sub="До отправки в чужое облако или на чужую площадку" />
        <Node amber title="Ключи отдельно" sub="Храните отдельно от самих копий" />
      </div>
      <div className="s-note">
        Расшифровка из копии — часть учений: копия, которую вы не можете
        открыть, — просто дорогой файл с нулями, и узнаётся это в самый
        неподходящий момент.
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Целостность данных"
      sub="Тихое повреждение — страшный сон хранения"
      main="Контрольные суммы на всех слоях: храните суммы рядом с копиями и проверяйте при каждом учении."
    >
      <div className="s-cols">
        <Node amber title="Диск вернул не те байты" sub="Никто не заметил — ошибка всплыла через год в архиве" />
        <Arr />
        <Node green title="Контрольные суммы" sub="Современные ФС считают сами, для остального — утилиты" />
      </div>
      <Cmd>
        {"sha256sum backup.tar.gz > backup.tar.gz.sha256\nsha256sum -c backup.tar.gz.sha256"}
      </Cmd>
      <p className="s-hint">
        Файловая система, снимающая суммы при записи и проверяющая при чтении,
        — весомый аргумент при выборе.
      </p>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Хранение выходит за корпуса"
      sub="Сетевые и объектные хранилища"
      main="Думайте о хранении как о спектре: от регистров процессора до ледяных архивов на другом континенте."
    >
      <div className="s-cols">
        <Node mono title="NFS" sub="Сетевая ФС монтируется как локальная" />
        <Node mono title="Блок по сети" sub="Блочное устройство приезжает по сети" />
        <Node green mono title="S3" sub="Не файлы с путями, а вёдра с ключами" />
      </div>
      <div className="s-note">
        Для бэкапов объектные хранилища идеальны: дешёвые классы, версионность,
        защита от случайного удаления. У каждой ступени — своя цена за скорость.
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Очереди ввода-вывода"
      sub="Как диск справляется с потоком просьб"
      main="Занятость устройства и ожидание — разные вещи: первый шаг диагностики — отличить очередь к диску от очереди к процессору."
    >
      <div className="s-cols">
        <Node mono title="Планировщик" sub="Ядро переупорядочивает запросы: магнитным критично, твердотельным почти нет" />
        <Node green mono title="Приоритеты" sub="Ночной бэкап уступает дорогу интерактивной задаче" />
      </div>
      <Cmd>{"ionice -c3 команда"}</Cmd>
      <div className="s-note">
        Тяжёлая фоновая задача не должна тормозить терминал: приоритеты
        ввода-вывода решают это дёшево.
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
      main="Если вы никогда не восстанавливали бэкап — сегодня тот самый день."
    >
      <div className="s-blocks">
        <div className="s-block">
          Проверьте телеметрию своих дисков прямо сейчас
        </div>
        <div className="s-block">
          Тар важного каталога: собрать, распаковать, сравнить списки
        </div>
        <div className="s-block">
          Эрсинк каталога на внешний диск — с сухим прогоном перед настоящим
          запуском
        </div>
        <div className="s-block changed">
          Честный ответ себе: когда вы последний раз восстанавливали бэкап?
        </div>
      </div>
    </Slide>
  );
}

function S18() {
  return (
    <Slide
      n={18}
      title="Арифметика отказов"
      sub="Двадцать дисков — отказ в год почти наверняка"
      main="Во время восстановления массив уязвимее обычного: замена умершего диска не терпит отлагательств."
    >
      <div className="s-cols">
        <Node amber title="Без запаса" sub="Молится, пока восстанавливается зеркало" />
        <Node green title="Горячий запас" sub="Пустой диск сразу включается при смерти соседа" />
      </div>
      <div className="s-note">
        Настраивайте всегда: он дёшев, а ночные тревоги снижает на порядок.
        Второй отказ в период восстановления страшнее первого.
      </div>
    </Slide>
  );
}

function S19() {
  const rows = [
    ["× 2", "Имя устройства — дважды перед любой командой с диском напрямую"],
    ["имя", "Помечайте диски и разделы: через полгода вы не вспомните «диск номер третий»"],
    ["табл.", "Таблица: какой диск, какой том, какая файловая система, где бэкап"],
  ];
  return (
    <Slide
      n={19}
      title="Привычки дороже инструментов"
      sub="Скучная канцелярия инженера"
      main="Инженер думает о том дне, когда всё пойдёт не так — именно этим он отличается от оператора."
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
        Да, это канцелярия. Но именно она спасает, когда всё идёт не так.
      </div>
    </Slide>
  );
}

function S20() {
  return (
    <Slide
      n={20}
      title="Проверки после аварий"
      sub="«Заработало» не значит «работает правильно»"
      main="Авария заканчивается не когда всё заработало, а когда вы проверили, что всё работает правильно."
    >
      <div className="s-blocks">
        <div className="s-block">
          Диск вернулся после замены: синхронизация идёт часами, нагрузка выше —
          не расслабляйтесь
        </div>
        <div className="s-block">
          Сбой питания: журнал файловой системы — восстановление чистое или с
          ошибками?
        </div>
        <div className="s-block changed">
          Падение базы: поднялась ли репликация?
        </div>
      </div>
      <div className="s-note">
        Каждая проверка — короткая; пропущенная — откладывает следующую аварию.
      </div>
    </Slide>
  );
}

function S21() {
  const topics = [
    ["LV", "Тома", "Границы двигаются на живую, снимки за секунды"],
    ["RA", "Массивы", "Защита от смерти диска, но не от людей"],
    ["~", "Своп", "Амортизатор, а не место для жизни"],
    ["321", "Бэкапы", "Три-два-один, суммы, учения по восстановлению"],
  ];
  return (
    <Slide
      n={21}
      title="Итог"
      sub="Глава 7 · Хранение"
      main="Дальше — пакеты: откуда программы берутся и почему у них столько зависимостей."
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
        Тар собирает, дэ-дэ копирует байты, эрсинк синхронизирует отличия.
        Телеметрия предупреждает — слушайте диски.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_CH7 = {
  "8:7": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_CH7).
export const SLIDE_TITLES_CH7 = {
  "8:7": [
    "Диски и бэкапы",
    "Разметка диска",
    "Файловые системы",
    "Тома LVM",
    "Копия живой базы",
    "RAID-массивы",
    "Своп",
    "Телеметрия дисков",
    "Архивы tar",
    "Побайтовое dd",
    "Синхронизация rsync",
    "Стратегия 3-2-1",
    "Шифрование копий",
    "Целостность данных",
    "Сетевое хранение",
    "Очереди ввода-вывода",
    "Практика",
    "Арифметика отказов",
    "Привычки инженера",
    "Проверки после аварий",
    "Итог",
  ],
};
