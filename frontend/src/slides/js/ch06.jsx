// Слайды для «Современный Frontend», глава 6 — «Деревья».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СТРУКТУРЫ И ПАТТЕРНЫ / ГЛАВА 6</span>
      <span>{String(n).padStart(2, "0")} / 13</span>
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
    ["{}", "JSON.parse", "Результат — дерево объектов и массивов"],
    ["DOM", "Страница", "Разметка, которую вы смотрите, — дерево узлов"],
    ["☰", "Меню и каталог", "Категории с потомками, комментарии с ответами"],
    ["fs", "Файлы и люди", "Файловая система, иерархия сотрудников"],
  ];
  return (
    <Slide
      n={1}
      title="Деревья"
      sub="Глава 6 · Структуры и паттерны"
      main="Цепочка ветвится: у элемента — несколько потомков, у каждого — свои."
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
        Деревья в JavaScript повсюду до незаметности. Научимся представлять их
        простыми объектами, ходить в глубину и в ширину и не падать со стеком.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Представление узла объектом"
      sub="Радикально проще, чем вы могли ожидать"
      main="У каждого узла известны дети, и существует узел, с которого всё начинается, — корень."
    >
      <Cmd>
        {
          "const node = {\n  value: 7,\n  left: null,      // нет ребёнка — null\n  right: { value: 11, left: null, right: null },\n};"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Никаких классов"
          sub="Литерал в фигурных скобках с вложенными — уже дерево"
        />
        <Node
          title="Дети — массив"
          sub="Поле «дети» с массивом: форма та же, ветвистость любая"
        />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Рекурсия — родной язык"
      sub="Поддерево — тоже дерево"
      main="Спроси у левого, спроси у правого, возьми максимум и прибавь один."
    >
      <Cmd>
        {
          "function depth(n) {\n  if (!n) return 0;   // базовый случай: null — ноль\n  return 1 + Math.max(depth(n.left), depth(n.right));\n}"
        }
      </Cmd>
      <div className="s-note">
        Решение «обработать узел и сделать то же самое с детьми» покрывает всю
        структуру без единого цикла по позициям. Переводите такие фразы в код —
        и половина задач про деревья перестанет быть задачами.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Три порядка в глубину"
      sub="Различие — момент визита узла"
      main="Одна рекурсивная функция: куда воткнуть «обработай меня», такой и порядок."
    >
      <div className="s-cols">
        <Node title="Прямой" sub="узел → левое → правое · копирование и сериализация" />
        <Node
          kind="green"
          title="Центрированный"
          sub="левое → узел → правое · в дереве поиска даёт сортировку"
        />
        <Node title="Обратный" sub="поддеревья → узел · размеры и освобождение памяти" />
      </div>
      <Cmd>
        {
          "const walk = (n) => {\n  if (!n) return;\n  /* сюда — прямой */\n  walk(n.left);\n  /* сюда — центрированный */\n  walk(n.right);\n  /* сюда — обратный */\n};"
        }
      </Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Обход в ширину"
      sub="По уровням: волна за волной"
      main="Формулировка задачи сама подсказывает инструмент, если слушать её внимательно."
    >
      <Cmd>
        {
          "const queue = [root];\nwhile (queue.length) {\n  const n = queue.shift();          // из головы\n  if (n.left) queue.push(n.left);   // в хвост\n  if (n.right) queue.push(n.right);\n}"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Ширина — про расстояние"
          sub="Минимальная глубина, уровень узла, среднее по каждому уровню"
        />
        <Node
          title="Глубина — про пути"
          sub="Есть ли значение, сумма вдоль маршрута, где максимум"
        />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Явный стек вместо рекурсии"
      sub="Практический выбор в JavaScript"
      main="Тот же порядок обхода, но память под стек вы контролируете сами."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Вырожденное дерево-цепочка"
          sub="Тысячи узлов — стек движка кончается: «превышен максимальный размер стека вызовов»"
        />
        <Node
          kind="green"
          title="Явный стек — массив"
          sub="Кладёте push, достаёте pop: тот же алгоритм, своя память"
        />
      </div>
      <Cmd>
        {
          "const stack = [root];\nwhile (stack.length) {\n  const n = stack.pop();\n  if (n.right) stack.push(n.right);\n  if (n.left) stack.push(n.left);\n}"
        }
      </Cmd>
      <p className="s-hint">
        Заодно обход можно поставить на паузу и продолжить позже — так работают
        ленивые итераторы по структурам.
      </p>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Дерево поиска"
      sub="Слева меньше, справа больше"
      main="Сравнил, пошёл в одну сторону, забыл другую — поиск превращается в спуск."
    >
      <Cmd>
        {
          "if (x < node.value) node = node.left;\nelse node = node.right;      // на удачном дереве — логарифм"
        }
      </Cmd>
      <div className="s-cols">
        <Node kind="amber" mono title="Map" sub="Хеш-таблица: точечные запросы, но не порядок" />
        <Node
          kind="amber"
          title="Отсортированный массив"
          sub="Порядок есть, быстрой вставки нет"
        />
        <Node
          kind="green"
          title="Дерево поиска"
          sub="И поиск, и минимум, и максимум, и соседи, и диапазоны"
        />
      </div>
      <div className="s-note">
        В стандартной библиотеке JavaScript дерева нет: за порядком либо пишут
        дерево сами, либо держат отсортированный массив для статичных данных.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Балансировка"
      sub="Тёмная сторона дерева поиска"
      main="Наивное дерево — обещание логарифма; гарантировать обещание должна балансировка."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Отсортированные данные в наивное дерево"
          sub="Каждая вставка в одну сторону: дерево — цепочка, логарифм — линейность"
        />
        <Node
          kind="green"
          title="Вращения узлов"
          sub="Держат высоту логарифмической ценой перестройки локальных кусков"
        />
      </div>
      <div className="s-opts">
        <span className="s-path accent">АВЛ</span>
        <span>жёсткие</span>
        <span className="s-path accent">красно-чёрные</span>
        <span>мягкие</span>
        <span>оба семейства — внутри реальных библиотек</span>
      </div>
      <div className="s-note">
        Это тот самый худший случай из первой главы, только здесь он
        статистически обыденный, а не редкий.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Куча в массиве"
      sub="Дерево, которое не хранит ссылок"
      main="Родитель не больше детей — минимум всегда в нулевой клетке."
    >
      <Cmd>
        {
          "дети i:      2i + 1 и 2i + 2\nродитель i:  (i - 1) // 2\nминимум:     клетка 0 — родитель не больше детей"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Очередь с приоритетами"
          sub="Положил — поднял вверх, пока нарушается правило; достал минимум — спустил последний"
        />
        <Node
          kind="amber"
          title="Разовая задача"
          sub="Честно: сортировка массива дешевле самодельной кучи"
        />
      </div>
      <p className="s-hint">
        Очередь с приоритетами, которой не хватает стандартной библиотеке
        JavaScript, ещё пригодится нам в задачах о кратчайших путях.
      </p>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Приёмы рабочей рекурсии"
      sub="Превращаем идею в инструмент"
      main="Одна форма на всё: спроси у детей, добавь своё."
    >
      <Cmd>
        {
          "const sum = (n) => (n ? n.value + sum(n.left) + sum(n.right) : 0);\n\nconst find = (n, x) => !n ? null\n  : n.value === x ? n              // ранний выход\n  : find(n.left, x) || find(n.right, x);"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Несколько величин сразу"
          sub="Глубину и флаг сбалансированности — возвращайте объект, JavaScript делает это бесплатно"
        />
        <Node title="Максимум" sub="То же самое с Math.max вместо сложения" />
      </div>
      <p className="s-hint">
        Рисуйте деревья на бумаге, пока ходите по ним мыслью: один рисунок
        экономит час отладки.
      </p>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Деревья в ежедневном JavaScript"
      sub="Форма одна — приёмы те же"
      main="Алгоритмы на объектах с тремя полями переносятся на все эти миры один к одному."
    >
      <div className="s-grid2">
        <Node
          title="Обход DOM"
          sub="querySelectorAll внутри поддерева делает ровно то, что мы учимся писать руками"
        />
        <Node
          title="JSON"
          sub="Валидаторы и поиск поля по всему документу — обходы в глубину с ветвлением по типу узла"
        />
        <Node
          title="Каталоги и оргструктуры"
          sub="Категории магазина, комментарии с ответами — дерево из ссылок на детей"
        />
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Ловушки"
      sub="Четыре грабли деревьев"
      main="Базовый случай — не формальность: null-узел обязательно встретится."
    >
      <div className="s-blocks">
        <div className="s-block">
          TypeError «невозможно прочитать свойство null»: забыли базовый случай
          и полезли в детей null-узла — лечится проверкой в начале функции
        </div>
        <div className="s-block">
          Сравнение деревьев оператором равенства сравнивает ссылки, а не
          структуру: структурное сравнение пишут той же рекурсией
        </div>
        <div className="s-block">
          Мутация дерева во время обхода: перестраиваете ветку — не ходите по
          ней в тот же момент
        </div>
        <div className="s-block changed">
          Глубокая рекурсия на большом дереве: явный стек или ширина через
          очередь
        </div>
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["ƒ", "Рекурсия", "Глубина, сумма, поиск: спроси у детей, добавь своё"],
    ["⇅", "Три порядка", "Центрированный по дереву поиска даёт сортировку"],
    ["≋", "Ширина", "Уровни через очередь — расстояния от корня"],
    ["▄", "Куча", "Очередь с приоритетами, живущая прямо в массиве"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 6 · Структуры и паттерны"
      main="Дерево — объекты со ссылками на детей, рекурсия — родной язык."
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
        Явный стек страхует от переполнения. Следующая глава снимает
        ограничение «не больше двух детей»: графы — самая общая структура
        связей.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_J6 = {
  "11:6": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J6).
export const SLIDE_TITLES_J6 = {
  "11:6": [
    "Деревья повсюду",
    "Представление узла объектом",
    "Рекурсия — родной язык",
    "Три порядка в глубину",
    "Обход в ширину",
    "Явный стек вместо рекурсии",
    "Дерево поиска",
    "Балансировка",
    "Куча в массиве",
    "Приёмы рабочей рекурсии",
    "Деревья в ежедневном JavaScript",
    "Ловушки",
    "Итог",
  ],
};
