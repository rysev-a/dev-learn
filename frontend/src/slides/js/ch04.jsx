// Слайды для «Современный Frontend», глава 4 — «Хеш-таблицы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СТРУКТУРЫ И ПАТТЕРНЫ / ГЛАВА 4</span>
      <span>{String(n).padStart(2, "0")} / 12</span>
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
    ["#", "Механика", "Хеш, остаток, ведро — без всякого перебора"],
    ["{}", "Объект и Map", "Оговорки объекта, Map по умолчанию"],
    ["Set", "Множество", "Дедупликация и has за константу"],
    ["★", "Узоры", "Счёт, группировка, пары, множества"],
  ];
  return (
    <Slide
      n={1}
      title="Хеш-таблицы"
      sub="Глава 4 · Структуры и паттерны"
      main="Построил словарь по мере прохода — и ответил на вопрос без повторных переборов."
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
        Любой литерал в фигурных скобках — словарь, а Map и Set — его
        современные братья. Половина практических задач решается одной
        конструкцией.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Механика: хеш и ведро"
      sub="Ключ превращается в адрес ячейки"
      main="Вычислил хеш — сразу знаешь ячейку: чтение и запись за константу в среднем."
    >
      <Cmd>{"ключ → hash(ключ) → % размер таблицы → ведро"}</Cmd>
      <div className="s-cols">
        <Node
          mono
          kind="green"
          title="O(1) в среднем"
          sub="При хорошей хеш-функции цепочки в вёдрах коротки"
        />
        <Node
          mono
          kind="amber"
          title="O(n) в худшем"
          sub="Плохая функция — таблица вырождается в список с линейным поиском"
        />
      </div>
      <div className="s-note">
        Несколько ключей в одном ведре перебираются цепочкой внутри ведра — к
        паре «средний и худший» вернёмся ближе к концу урока.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Ловушки объекта"
      sub="Первая неожиданность: ключи — только строки и символы"
      main="Ключи, приходящие от пользователей, — это Object.create(null) или Map, и это защита, а не педантизм."
    >
      <Cmd>
        {
          'obj[1] === obj["1"]          // число немедленно становится строкой\nObject.hasOwn(obj, key)      // проверка наличия — не undefined!\nconst dict = Object.create(null);  // словарь без прототипа'
        }
      </Cmd>
      <div className="s-note amber">
        Объект наследует свойства прототипа: ключи вроде «constructor» и
        «prototype» могут вступить в чужую собственность.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Map по умолчанию"
      sub="Таким должен быть словарь в алгоритмическом коде"
      main="Динамические ключи или объекты-ключи — берите Map; объект уместен для заранее известных полей структуры."
    >
      <div className="s-grid2">
        <Node
          mono
          title="set · get · has · delete · clear · size"
          sub="Закрывают все повседневные нужды"
        />
        <Node
          title="Ключ — что угодно"
          sub="Включая объекты; сравниваются они по ссылке"
        />
        <Node
          kind="green"
          title="Порядок вставки"
          sub="for…of работает из коробки, как у Map, так и для отчётов"
        />
        <Node
          kind="green"
          title="Нет прототипа"
          sub="Записи не конфликтуют с чужими свойствами"
        />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Set и дедупликация"
      sub="Это Map без значений: только ключи"
      main="Объекты сравниваются по ссылке — для равенства по содержимому стройте ключ-строку."
    >
      <Cmd>
        {
          "[...new Set([1, 1, 2, 3, 3])]   // [1, 2, 3]\nseen.has(x)                     // видел ли мы это значение"
        }
      </Cmd>
      <div className="s-cols">
        <Node
          kind="amber"
          title="Два одинаковых массива"
          sub="Структурно равные объекты — два разных элемента множества"
        />
        <Node
          mono
          kind="green"
          title={'arr.join(",")'}
          sub="Ключ-строка даёт равенство по содержимому"
        />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Подсчёт частот"
      sub="Паттерн, который решает десяток задач"
      main="Частоты слов, голосов, ошибок в логах — одна и та же трёхстрочная конструкция."
    >
      <Cmd>
        {
          "const f = new Map();\nfor (const w of words)\n  f.set(w, (f.get(w) ?? 0) + 1);   // счётчик или ноль, плюс один"
        }
      </Cmd>
      <div className="s-note">
        Вершина узора — анаграммы: отсортируйте буквы слова и получите
        канонический ключ, по которому все анаграммы падают в одно ведро.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Группировка"
      sub="Ключ — признак, значение — массив элементов"
      main="Map сохраняет порядок вставки, поэтому группы выходят в порядке первого появления."
    >
      <Cmd>
        {
          "const g = new Map();\nfor (const o of orders)\n  g.set(o.status, g.get(o.status) ?? []).push(o);"
        }
      </Cmd>
      <div className="s-cols">
        <Node
          title="Признак — это ключ"
          sub="Заказы по статусам, события по дню, файлы по расширению"
        />
        <Node
          mono
          kind="green"
          title="Object.groupBy"
          sub="Появился в свежем стандарте — руками пишется за минуту"
        />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Память вместо скорости"
      sub="Поиск пары за один проход"
      main="Словарь, построенный по мере прохода, заменяет повторный поиск по массиву."
    >
      <Cmd>
        {
          "for (let i = 0; i < a.length; i++) {\n  if (map.has(target - a[i]))       // дополнение уже встречалось?\n    return [map.get(target - a[i]), i];\n  map.set(a[i], i);                 // число с индексом — в Map\n}"
        }
      </Cmd>
      <div className="s-cols">
        <Node
          mono
          kind="amber"
          title="O(n²)"
          sub="Вложенный цикл: проверить все пары"
        />
        <Node
          mono
          kind="green"
          title="O(n) время · O(n) память"
          sub="Линейное время, линейная память — сделка из первой главы"
        />
      </div>
      <div className="s-note">
        Тот же узор ищет пару с заданной разностью, находит дубликат и проверяет
        нужное расстояние между числами.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Коллизии и хеш-флуд"
      sub="Понимание худшего случая отличает уверенное использование от суеверного"
      main="Усреднённая константа — статистическое обещание при доброжелательных ключах, а не гарантия по контракту."
    >
      <div className="s-cols">
        <Node
          title="Коллизии — норма жизни"
          sub="Движки борются с ними ростом таблицы и переупаковкой"
        />
        <Node
          kind="amber"
          title="Хеш-флуд"
          sub="Злоумышленник подбирает тысячи ключей в одно ведро; защита — соль в хеш-функции"
        />
      </div>
      <div className="s-note">
        В браузерном JavaScript думать об этом всерьёз приходится редко, но
        договорённость остаётся.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Изменяемые ключи"
      sub="Ключ в Map — это ссылка"
      main="Ключами делают строки, числа или замороженные объекты; для составных сущностей — канонический строковый ключ."
    >
      <Cmd>
        {
          'map.set(key, "v");\nkey.x = 1;              // содержимое изменилось — сравнение по ссылке плывёт\nmap.set([1, 2], …)      // каждый литерал массива — новый объект-ключ'
        }
      </Cmd>
      <div className="s-cols">
        <Node
          kind="green"
          title="Дисциплина ключей"
          sub="Строки, числа, frozen-объекты, канонический строковый ключ"
        />
        <Node
          kind="amber"
          title="Цена хеширования"
          sub="Длинная строка хешируется линейно: «O(1)» всегда с оговоркой «плюс длина ключа»"
        />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Малые данные и множества"
      sub="Обратная сторона медали, о которой забывают"
      main="Структура окупается, когда поисков много или данных много; операции над множествами — всё линейно, без квадратов."
    >
      <div className="s-cols">
        <Node
          title="Десяток элементов"
          sub="Честно перебирается за микросекунды — построение Map съест больше, чем сам поиск"
        />
        <Node
          mono
          kind="green"
          title="∩ · ∪ · −"
          sub="Пересечение — has в большем, объединение — спред, разность — filter с !has"
        />
      </div>
      <div className="s-note">
        Пересечение обходите по меньшему массиву — операций будет меньше, а
        сложность останется линейной.
      </div>
    </Slide>
  );
}

function S12() {
  const topics = [
    ["#", "Механика", "Хеш, ведро, коллизии, средняя константа"],
    ["{}", "Словари", "Объект с оговорками, Map и Set без них"],
    ["★", "Четыре узора", "Счёт, группы, пары, множества"],
    ["⚠", "Цены", "Длина ключа, мутации, малые данные"],
  ];
  return (
    <Slide
      n={12}
      title="Итог"
      sub="Глава 4 · Хеш-таблицы"
      main="Четыре узора закрывают половину прикладных алгоритмов — словарь заменяет повторные переборы."
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
        В следующей главе — каталог приёмов движения по данным: два указателя,
        скользящее окно и разделяй и властвуй.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_J4 = {
  "11:4": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J4).
export const SLIDE_TITLES_J4 = {
  "11:4": [
    "Введение: хеш-таблицы",
    "Механика хеширования",
    "Ловушки объекта",
    "Map по умолчанию",
    "Set и дедупликация",
    "Подсчёт частот",
    "Группировка",
    "Память вместо скорости",
    "Коллизии и хеш-флуд",
    "Изменяемые ключи",
    "Малые данные и множества",
    "Итог",
  ],
};
