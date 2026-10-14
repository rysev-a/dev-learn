// Слайды для «Linux: от шелла до ядра», глава 2 — «Командная строка, конвейеры и скрипты».
// Тот же дизайн-код, что и глава 1: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ФАЙЛОВАЯ СИСТЕМА И ШЕЛЛ / ГЛАВА 2</span>
      <span>{String(n).padStart(2, "0")} / 18</span>
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
    ["|", "Конвейер", "Выход одной программы — вход следующей"],
    [">", "Потоки", "Вход, выход и ошибки у каждой программы"],
    ["?", "Скрипты", "Файлы с командами, которые работают ночами"],
    ["*", "Регэкспы", "Язык вопросов к тексту и логам"],
  ];
  return (
    <Slide
      n={1}
      title="Командная строка, конвейеры и скрипты"
      sub="Глава 2 · Грамматика шелла"
      main="Не заучивать команды, а освоить грамматику: из маленьких блоков собирается всё."
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
      <p className="s-hint">Терминал — место силы, а не место страха.</p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Навигация и файловые операции"
      sub="Словарь важнее глубины"
      main="Привычка профи: сначала печать списка вместо действия, убедиться глазами — потом действие."
    >
      <Cmd>{"pwd · cd · ls -l\ncp · mv · rm"}</Cmd>
      <Node
        amber
        title="rm -rf — без подтверждений"
        sub="Не прощает опечаток, особенно рядом с пробелом и корнем"
      />
      <div className="s-grid2">
        <Node
          mono
          title="tail -f"
          sub="Живой режим: следит за логом в реальном времени"
        />
        <Node
          mono
          title="which"
          sub="Где лежит программа: поиск по пути окружения"
        />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="У каждой программы три потока"
      sub="Главная идея дня"
      main="Ошибки идут отдельным каналом: без 2>&1 лог теряет половину сообщений."
    >
      <div className="s-cols">
        <Node mono title="stdin" sub="Вход · по умолчанию клавиатура" />
        <Node green mono title="stdout" sub="Выход · результат" />
        <Node amber mono title="stderr" sub="Ошибки · отдельный канал" />
      </div>
      <div className="s-label">ПЕРЕНАПРАВЛЕНИЕ</div>
      <Cmd>
        {
          "cmd > файл   — записать выход\ncmd >> файл  — дописать в конец\ncmd < файл   — скормить файл на вход"
        }
      </Cmd>
      <p className="s-hint">
        <span className="s-path">2&gt;&amp;1</span> — слить ошибки с выходом ·{" "}
        <span className="s-path">/dev/null</span> — мусорка
      </p>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Конвейер: программы из программ"
      sub="Вертикальная черта соединяет выход со входом"
      main="Маленькие программы, каждая делает одно дело, — сила в композиции."
    >
      <div className="s-cols">
        <Node mono title="tail" />
        <Arr />
        <Node mono title="grep" />
        <Arr />
        <Node mono title="wc -l" />
      </div>
      <div className="s-label">ТОП-10 СТРОК ЛОГА ОДНОЙ СТРОКОЙ</div>
      <Cmd>{"… | sort | uniq -c | sort -rn | head"}</Cmd>
      <div className="s-grid2">
        <Node mono title="head / tail" sub="Первые и последние строки" />
        <Node
          mono
          title="sort / uniq -c"
          sub="Порядок, сжатие повторов, счётчик"
        />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Поиск: файлы и содержимое"
      sub="Задать вопрос всей кодовой базе"
      main="Владение парой find + grep экономит часы еженедельно."
    >
      <div className="s-grid2">
        <Node
          mono
          title="find"
          sub="Ходит по дереву: имя, тип, размер, время правки"
        />
        <Node
          mono
          title="grep"
          sub="Регулярка на вход — найденные строки на выход"
        />
      </div>
      <div className="s-label">ФЛАГИ ГРЕП</div>
      <div className="s-opts">
        <span className="s-path accent">-n</span>
        <span>номер строки</span>
        <span className="s-path accent">-r</span>
        <span>рекурсивно</span>
        <span className="s-path accent">-v</span>
        <span>наоборот</span>
        <span className="s-path accent">-c</span>
        <span>счёт</span>
      </div>
      <p className="s-hint">
        Где определяется функция? Какие конфиги содержат старый адрес? Что
        менялось за сутки?
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Текстовые швейцарские ножи"
      sub="sed и awk — ступень выше"
      main="Вместе с конвейерами терминал превращается в калькулятор для данных."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">СЕД</div>
          <span className="s-node-title">Читает поток, применяет правила</span>
          <span className="s-node-sub">
            Замена по регулярке · удаление строк с шаблоном · вставка по номеру
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">АВК</div>
          <span className="s-node-title">Видит строку как колонки</span>
          <span className="s-node-sub">
            Колонка номер N · сумма по всем строкам · фильтр перед печатью
          </span>
        </div>
      </div>
      <Cmd>{"sed 's/старое/новое/g'  ·  awk '{s+=$3} END {print s}'"}</Cmd>
      <div className="s-note amber">
        Замена на месте — только с бэкап-суффиксом: одна неточная регулярка
        способна переписать конфиг наперекосяк.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Скрипт: файл с командами"
      sub="Шелл исполняет построчно"
      main="Скрипт, меняющий окружение, меняет его только внутри себя — частый сюрприз новичков."
    >
      <Cmd>{'#!/bin/sh\nname=$1\necho "Привет, $name"'}</Cmd>
      <div className="s-grid2">
        <Node
          title="Первая строка"
          sub="Магический комментарий: какой интерпретатор"
        />
        <Node
          mono
          title="chmod +x"
          sub="Право на исполнение — и запуск как команды"
        />
      </div>
      <div className="s-label">ПЕРЕМЕННЫЕ</div>
      <div className="s-opts">
        <span className="s-path accent">x=1</span>
        <span>без пробелов</span>
        <span className="s-path accent">$x</span>
        <span>чтение</span>
        <span className="s-path accent">$1 $2</span>
        <span>аргументы</span>
        <span className="s-path accent">$?</span>
        <span>код возврата</span>
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Управление: проверки, циклы, функции"
      sub="Минимальное, но достаточное"
      main="Даже на этом уровне пишутся скрипты деплоя, бэкапов и чистки логов."
    >
      <Cmd>
        {
          'if [ -f "$f" ]; then …; fi\nfor x in список; do …; done\nфункция() { … }'
        }
      </Cmd>
      <div className="s-cols">
        <Node
          green
          mono
          title="&&"
          sub="Вторая команда — только после успеха первой"
        />
        <Node amber mono title="||" sub="Только после неудачи" />
      </div>
      <p className="s-hint">
        Код возврата 0 — успех. Проверки: файл существует, каталог существует,
        строки равны, число больше.
      </p>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Качество скрипта — дисциплина ошибок"
      sub="Полработа хуже, чем ничего"
      main="Одинарные кавычки переменную не раскрывают, двойные — раскрывают. Понять один раз — помнить всю жизнь."
    >
      <div className="s-cols">
        <Node
          amber
          title="По умолчанию"
          sub="Упала команда — бодро идёт дальше, делает полработы"
        />
        <Node
          green
          title="Строгий режим"
          sub="Падать при любой ошибке и незаданной переменной"
        />
      </div>
      <Cmd>{"set -eu"}</Cmd>
      <div className="s-note">
        Кавычки вокруг переменных обязательны: файл с пробелом в имени без
        кавычек разваливается на два слова и ломает цикл.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Практика на сегодня"
      sub="Четыре упражнения"
      main="Скрипт бэкапа: пятнадцать строк, а пользу приносит годами."
    >
      <div className="s-blocks">
        <div className="s-block">
          Топ-10 своих команд из истории: вытащить историю → отрезать колонки →
          посчитать повторы → отсортировать
        </div>
        <div className="s-block">
          Скрипт бэкапа: архив каталога с датой в имени, хранить последние пять,
          писать в лог
        </div>
        <div className="s-block">
          Самый большой лог через конвейер: топ адресов, топ ошибок, средний
          размер ответа
        </div>
        <div className="s-block changed">
          Найти «пароль» в конфигах кодовой базы — побыть шокированным и
          починить
        </div>
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Вход без временных файлов"
      sub="Документ-здесь и подстановка процессов"
      main="Весь вход рождается на лету — скрипты самодостаточны."
    >
      <div className="s-label">ДОКУМЕНТ-ЗДЕСЬ</div>
      <Cmd>{"cat << КОНЕЦ\nмногострочный текст прямо из скрипта\nКОНЕЦ"}</Cmd>
      <div className="s-label">ПОДСТАНОВКА ПРОЦЕССОВ</div>
      <Cmd>{"diff <(команда-один) <(команда-два)"}</Cmd>
      <p className="s-hint">
        Письма, конфиги и запросы — прямо в теле сценария; сравнение двух
        списков — одной строкой.
      </p>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Шелл настраивается"
      sub="Алиасы, функции, история"
      main="Алиас обязан быть короче и понятнее оригинала — иначе через полгода вы не вспомните, что он делает."
    >
      <Cmd>{"alias ll='ls -l'"}</Cmd>
      <div className="s-grid2">
        <Node
          title="Файл настроек"
          sub="Алиасы, функции, переменные — в домашнем каталоге, живут в каждом новом терминале"
        />
        <Node
          title="История"
          sub="Тысячи прошлых команд: стрелки и поиск по началу"
        />
      </div>
      <div className="s-note amber">Не превращайте алиасы в свалку.</div>
    </Slide>
  );
}

function S13() {
  const rows = [
    [".", "любой символ"],
    ["*", "повтор предыдущего сколько угодно раз"],
    ["+", "хотя бы один раз"],
    ["^  $", "начало и конец строки"],
    ["[ ]", "любой символ из набора"],
  ];
  return (
    <Slide
      n={13}
      title="Язык регулярных выражений"
      sub="Без него grep и sed — половина силы"
      main="Начинайте с простого шаблона и проверяйте на копии данных: жадные повторы находят больше, чем вы планировали."
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
        На регулярках держится не только поиск по логам, но и половина проверок
        ввода в языках программирования.
      </p>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Передача найденного в команды"
      sub="Пачками — быстро и безопасно"
      main="Запомните пару «поиск, затем пачка» — она заменяет часы ручной работы."
    >
      <div className="s-cols">
        <Node mono title="find" />
        <Arr />
        <Node mono title="xargs" />
        <Arr />
        <Node mono title="команда" />
      </div>
      <div className="s-label">ПРОБЛЕМА ПРОБЕЛОВ В ИМЕНАХ</div>
      <Cmd>{"… | xargs -0 команда"}</Cmd>
      <p className="s-hint">
        Нулевой разделитель передаёт имена со специальной границей: ни один файл
        с пробелом не развалит команду. Пачками — быстрее на тысячах файлов и
        безопаснее для длинных списков.
      </p>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Отладка растущего скрипта"
      sub="Трассировка вместо молчания"
      main="Тихий скрипт невозможно диагностировать — пишите скрипты с выводом."
    >
      <Cmd>{"set -x"}</Cmd>
      <div className="s-grid2">
        <Node
          green
          title="Трассировка"
          sub="Печать каждой строки: загадочное молчание становится понятным логом"
        />
        <Node
          title="Анализатор"
          sub="Незаквоченные переменные, неиспользуемые значения, бесполезные проверки"
        />
      </div>
      <div className="s-note">
        Прогон через анализатор перед первым запуском — привычка, которая
        спасала не один продакшен.
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Честность конвейеров"
      sub="Чей код возврата?"
      main="Скрипт, падающий на первой строке с понятным сообщением, лучше скрипта, испортившего данные."
    >
      <Node
        amber
        title="По умолчанию: код последней команды"
        sub="Генератор упал в середине, счётчик посчитал пустоту — скрипт решил, что всё хорошо"
      />
      <Down />
      <Node
        green
        mono
        title="set -o pipefail"
        sub="Вернуть код самой неудачной команды в цепочке"
      />
      <div className="s-note">
        Проверяйте существование команд заранее — включайте строгость в
        скриптах, где ошибка в середине недопустима.
      </div>
    </Slide>
  );
}

function S17() {
  return (
    <Slide
      n={17}
      title="Экспорт переменных"
      sub="Что реально видит потомок"
      main="Проверка проста: запустить печать окружения внутри потомка и убедиться глазами."
    >
      <div className="s-grid2">
        <Node title="Обычная" sub="Видна только текущему шеллу" />
        <Node
          green
          title="Экспортированная"
          sub="Передаётся всем запускаемым программам"
        />
      </div>
      <Cmd>{"export EDITOR=vim   ·   env"}</Cmd>
      <div className="s-note amber">
        Секреты в окружении удобны, но легко утекают через дочерние процессы и
        дампы — в больших системах их выносят в отдельные хранилища.
      </div>
    </Slide>
  );
}

function S18() {
  const topics = [
    [">", "Потоки", "Язык общения программ с файлами и друг с другом"],
    ["|", "Конвейер", "Способ строить программы из программ"],
    ["?", "Скрипты", "Способ записать ответы навсегда"],
    ["*", "Регэкспы", "Способ спрашивать и переспрашивать"],
  ];
  return (
    <Slide
      n={18}
      title="Итог"
      sub="Глава 2 · Грамматика шелла"
      main="Дальше — права доступа: пользователи, группы и почему судо — не просто пароль на всё."
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
        Три привычки, отделяющие удобный шелл от опасного: строгий режим,
        кавычки, проверка перед удалением.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_CH2 = {
  "8:2": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_CH2).
export const SLIDE_TITLES_CH2 = {
  "8:2": [
    "Введение",
    "Навигация и файлы",
    "Три потока",
    "Конвейер",
    "Поиск: find и grep",
    "sed и awk",
    "Скрипт",
    "Управление",
    "Дисциплина ошибок",
    "Практика",
    "Вход без файлов",
    "Настройка шелла",
    "Регулярные выражения",
    "xargs",
    "Отладка",
    "Честность конвейеров",
    "Экспорт переменных",
    "Итог",
  ],
};
