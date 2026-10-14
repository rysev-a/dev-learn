// Слайды для «Изучаем JavaScript», глава 7 — «Графы: обходы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ГРАФЫ И СТРАТЕГИ / ГЛАВА 7</span>
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
    ["@", "Соцсеть", "Друзья и подписки"],
    ["⇄", "Маршруты", "Города и дороги между ними"],
    ["pkg", "Зависимости", "Пакеты в вашем проекте"],
    ["www", "Веб", "Страницы со ссылками друг на друга"],
  ];
  return (
    <Slide
      n={1}
      title="Графы: обходы"
      sub="Глава 7 · Графы и стратегии"
      main="Снимаем все ограничения дерева — получаем самую общую структуру связей."
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
        Хорошая новость: все инструменты уже есть. Граф — объект или Map со
        списками соседей, обходы — стек и очередь, плюс одно жизненно важное
        множество.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Список смежности"
      sub="Стандарт де-факто для графов"
      main="Редкие графы — список; плотные маленькие с мгновенной проверкой пары — матрица."
    >
      <Cmd>
        {
          "const graph = {\n  a: [\"b\", \"c\"],\n  b: [\"c\"],\n  c: [],\n};"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Список смежности"
          sub="Память линейна по вершинам и рёбрам, соседи достаются мгновенно"
        />
        <Node
          kind="amber"
          title="Матрица смежности"
          sub="Клетка отвечает «есть ли ребро» за константу, но платит квадратом памяти"
        />
      </div>
      <p className="s-hint">
        В задачах на сетке клеток матрицей служит сама сетка: соседей вычисляют
        сдвигами на клетку в четыре стороны.
      </p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Set посещённых вершин"
      sub="Без него не обходится ни один граф"
      main="В дереве циклов не бывает; в графе наивный обход зациклится навсегда."
    >
      <Cmd>
        {
          "в дереве: циклов нет — любой обход кончается сам\nв графе:  visited.add(v) в момент постановки в очередь,\n          а не когда достали — иначе вершина попадёт дважды"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Наивный обход"
          sub="Ребро вернуло вас туда, где вы уже были, — вкладка замолчит без единой ошибки"
        />
        <Node
          kind="green"
          title="Set посещённых"
          sub="В графах со строковыми ключами особенно удобен"
        />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Обход в глубину"
      sub="Проще всего записать рекурсией"
      main="Стек вызовов сам ведёт учёт, куда вернуться."
    >
      <Cmd>
        {
          "function dfs(v) {\n  visited.add(v);\n  for (const to of graph[v] ?? []) {\n    if (!visited.has(to)) dfs(to);\n  }\n}"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Применения"
          sub="Существует ли путь, хоть какой-то выход из лабиринта, всё достижимое из точки"
        />
        <Node
          kind="amber"
          title="Цена"
          sub="На очень глубоких графах — явный стек: массив с push и pop"
        />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Обход в ширину"
      sub="Тот же алгоритм с другой структурой данных"
      main="В невзвешенном графе ширина находит кратчайшие пути."
    >
      <Cmd>
        {
          "const queue = [start];\nvisited.add(start);\nwhile (queue.length) {\n  const v = queue.shift();\n  for (const to of graph[v] ?? []) {\n    if (!visited.has(to)) { visited.add(to); queue.push(to); }\n  }\n}"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Ребро стоит единицу"
          sub="Сколько волн прошло до вершины — такова минимальная длина пути"
        />
        <Node
          kind="amber"
          title="Разные веса"
          sub="Ширина врёт: волна по многим коротким дорогам дотекает быстрее, чем по одной длинной"
        />
      </div>
      <p className="s-hint">
        Первый в курсе алгоритм кратчайшего пути — в следующей главе он
        вернётся как частный случай Дейкстры.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Восстановление маршрута"
      sub="Словарь предыдущих вершин"
      main="Чуть больше памяти — и вместо числа у вас конкретный маршрут."
    >
      <Cmd>
        {
          "prev.set(to, v);   // «в эту вершину пришли из той»\n\nconst path = [];\nfor (let at = goal; at !== start; at = prev.get(at)) path.push(at);\npath.push(start);\npath.reverse();    // маршрут: старт → цель"
        }
      </Cmd>
      <div className="s-note">
        Тот же паттерн обмена памяти на скорость. В лабиринтах, навигации и
        играх вы почти всегда хотите именно маршрут.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Глубина против ширины"
      sub="Сравним братьев на лабиринте"
      main="Нужен хоть какой-то путь — глубина; нужен кратчайший — ширина."
    >
      <div className="s-cols">
        <Node
          title="Глубина"
          sub="Идёт вдоль стены: быстро доберётся до какого-нибудь выхода, путь с петлями"
        />
        <Node
          kind="green"
          title="Ширина"
          sub="Разливается водой: где вода впервые дотекла — тот путь и есть кратчайший"
        />
      </div>
      <div className="s-opts">
        <span className="s-path accent">минимум памяти</span>
        <span>стеку глубины хватает одной линии</span>
        <span className="s-path accent">целые волны</span>
        <span>очередь ширины разрастается на широких графах</span>
      </div>
      <div className="s-note">
        На графе с миллиардом вершин и скромной памятью аргумент памяти —
        решающий довод в пользу глубины.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Компоненты связности"
      sub="На сколько отдельных кусков распадается граф"
      main="Встретили непосещённую вершину — счётчик плюс один."
    >
      <Cmd>
        {
          "let count = 0;\nfor (const v of Object.keys(graph)) {\n  if (!visited.has(v)) { count++; dfs(v); }  // окрасит весь кусок\n}"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Острова и кластеры"
          sub="Острова на карте, группы друзей, изолированные серверы"
        />
        <Node
          kind="green"
          title="Глубина или ширина"
          sub="Работают одинаково: важен факт посещения, а не порядок"
        />
      </div>
      <p className="s-hint">
        Шаблон «перебор плюс обход» стоит запомнить целиком: он же считает
        области на матрице, он же проверяет, не распался ли сервис.
      </p>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Топологическая сортировка"
      sub="Алгоритм Кана для зависимостей"
      main="Ребро из а в б без обратного: а зависит от б — пакет требует пакет."
    >
      <Cmd>
        {
          "1. степень захода каждой вершины (число зависимостей)\n2. нулевые степени — в очередь\n3. достали → в ответ, зависимым −1\n4. чья степень стала нулём — в очередь"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          kind="green"
          title="Порядок построен"
          sub="Каждая вершина идёт после своих зависимостей"
        />
        <Node
          kind="amber"
          title="Ответ короче списка вершин"
          sub="Остальные сидят в цикле — так пакетные менеджеры сообщают о циркулярных зависимостях"
        />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Двудольная раскраска"
      sub="Ещё один приём ширины"
      main="Обходы — каркас, а обработка вершины при визите и есть решение задачи."
    >
      <Cmd>
        {
          "старт → цвет 1, соседи → цвет 2, их соседи → снова 1\nребро между одинаковыми цветами → раскраска невозможна"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Две команды"
          sub="Разделить участников без знакомых внутри"
        />
        <Node
          title="Два корпуса"
          sub="Развести занятия без конфликтов"
        />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Ловушки"
      sub="Четыре грабли графов"
      main="Пустой массив вместо undefined — защита в одну строчку."
    >
      <div className="s-blocks">
        <div className="s-block">
          Сосед упомянут в списках, но не имеет собственного ключа в словаре:
          чтение его списка вернёт undefined — защита с двойным вопросиком:
          graph[v] ?? []
        </div>
        <div className="s-block">
          Неориентированное ребро добавляется в оба списка: забыли обратное
          направление — потеряли полграфа
        </div>
        <div className="s-block">
          Типы ключей: в объекте единица и строка «один» — один ключ, в Map —
          разные; не смешивайте
        </div>
        <div className="s-block changed">
          Обход, мутирующий входной граф, портит повторные запуски: Set
          посещённых заводите свой
        </div>
      </div>
    </Slide>
  );
}

function S12() {
  const topics = [
    ["▣", "Контейнер решает", "Стек даёт глубину, очередь даёт ширину"],
    ["Set", "Посещённые", "Обязательный гражданин любого обхода"],
    ["prev", "Маршрут", "Словарь предыдущих превращает расстояние в путь"],
    ["Kahn", "Порядок", "Степени захода раскладывают зависимости"],
  ];
  return (
    <Slide
      n={12}
      title="Итог"
      sub="Глава 7 · Графы и стратегии"
      main="Только ширина обещает кратчайший путь в невзвешенном графе."
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
        Следующая глава добавляет к рёбрам веса: Дейкстра, Беллман-Форд и
        остовные деревья уже ждут нас.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_J7 = {
  "11:7": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J7).
export const SLIDE_TITLES_J7 = {
  "11:7": [
    "Граф без дисциплины",
    "Список смежности",
    "Set посещённых вершин",
    "Обход в глубину",
    "Обход в ширину",
    "Восстановление маршрута",
    "Глубина против ширины",
    "Компоненты связности",
    "Топологическая сортировка",
    "Двудольная раскраска",
    "Ловушки",
    "Итог",
  ],
};
