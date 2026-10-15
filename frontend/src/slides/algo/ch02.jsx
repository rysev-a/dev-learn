// Слайды для «Алгоритмы и структуры данных», глава 2 —
// «Массивы, строки и связные списки». Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ФУНДАМЕНТ / ГЛАВА 2</span>
      <span>{String(n).padStart(2, "0")} / 16</span>
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
    ["[ ]", "Массив", "Непрерывный кусок памяти: адрес по индексу"],
    ["abc", "Строка", "Массив символов с поворотами"],
    ["•→", "Список", "Узлы в памяти со ссылками на следующий"],
    ["↑↓", "Стек и очередь", "Правила поведения поверх хранения"],
  ];
  return (
    <Slide
      n={1}
      title="Массивы, строки и связные списки"
      sub="Глава 2 · Кирпичи структур"
      main="Из простого факта непрерывности массива вытекает всё остальное."
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
        До элемента номер пятьсот не нужно пятьсот шагов — известен адрес.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Цена непрерывности"
      sub="Вставить в середину нельзя — там его просто нет"
      main="Чтение по индексу — константа, перестройка — линейный сдвиг."
    >
      <div className="s-label">ВСТАВКА В СЕРЕДИНУ</div>
      <div className="s-cols">
        <span className="s-block">A</span>
        <span className="s-block">B</span>
        <span className="s-block changed">C</span>
        <span className="s-block changed">D</span>
        <Arr />
        <span className="s-block">X</span>
      </div>
      <Node
        kind="amber"
        title="Сдвиг всей правой части на одну позицию"
        sub="O(n) на вставку · удаление из середины — то же самое"
      />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Подарок: дружба с кэшем"
      sub="О непрерывности редко говорят вслух"
      main="Проход подряд по массиву — лучший друг кэша процессора."
    >
      <div className="s-cols">
        <Node
          kind="green"
          title="Массив"
          sub="Элементы впритык: процессор затягивает их блоками"
        />
        <Node
          kind="amber"
          title="Список"
          sub="Разбросан по памяти: каждый переход — риск промаха"
        />
      </div>
      <div className="s-note">
        Процессор не читает память по одному байту: непрерывность превращает
        проход по массиву в полёт.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Строки — массивы с поворотом"
      sub="Неизменяемость меняет всё"
      main="Строку нельзя поправить — можно только построить новую."
    >
      <Cmd>
        {
          "плохо:   s = s + кусочек  в цикле   ← O(n²)\nхорошо:  части.push(кусок) · соединить ← O(n)"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Каждая правка"
          sub="Создаёт новую строку, а не правит старую"
        />
        <Node
          kind="green"
          title="Конструктор строк"
          sub="Копим куски — соединяем один раз в конце"
        />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Четыре задачи на разминку"
      sub="Уметь решать сходу"
      main="Побеждает не знание библиотеки, а ясное понимание того, что такое массив."
    >
      <div className="s-blocks">
        <div className="s-block">
          Разворот массива двумя указателями с концов
        </div>
        <div className="s-block">
          Второй по величине элемент — за один проход
        </div>
        <div className="s-block">
          Циклический сдвиг тройным разворотом: весь массив, потом два куска
        </div>
        <div className="s-block changed">
          Анаграмма двух строк — частоты символов в словаре за линию вместо
          сортировки
        </div>
      </div>
      <p className="s-hint">
        Массив — последовательность с константным доступом и линейными
        перестройками.
      </p>
    </Slide>
  );
}

function S06() {
  const rows = [
    ["O(1)", "Чтение по индексу"],
    ["O(n)", "Вставка в середину — сдвиг правой части"],
    ["O(n)", "Проход подряд — зато лучший друг кэша"],
  ];
  return (
    <Slide
      n={6}
      title="Массив: итог первой половины"
      sub="Непрерывность, купленная ценой жёсткости"
      main="Массив — это непрерывность, купленная ценой жёсткости."
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

function S07() {
  return (
    <Slide
      n={7}
      title="Связный список"
      sub="Зеркало массива"
      main="Массив дёшево читает и дорого перестраивает, список — наоборот."
    >
      <div className="s-cols">
        <Node mono title="12" sub="данные + ссылка" />
        <Arr />
        <Node mono title="99" />
        <Arr />
        <Node mono title="37" />
      </div>
      <div className="s-grid2">
        <Node
          kind="amber"
          mono
          title="O(n)"
          sub="До пятисотого элемента — пройти по ссылкам честно"
        />
        <Node
          kind="green"
          mono
          title="O(1)"
          sub="Вставка и удаление, если уже стоишь на месте: пара ссылок"
        />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Односвязный и двусвязный"
      sub="Сколько ссылок помнит узел"
      main="Двусвязность стоит лишней ссылки в каждом узле."
    >
      <div className="s-cols">
        <div className="s-card">
          <div className="s-label">ОДНОСВЯЗНЫЙ</div>
          <span className="s-node-title">Помнит только следующего</span>
          <span className="s-node-sub">
            Идти можно в одну сторону
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">ДВУСВЯЗНЫЙ</div>
          <span className="s-node-title">Помнит и предыдущего</span>
          <span className="s-node-sub">
            Обе стороны · удаление из середины, когда знаешь узел
          </span>
        </div>
      </div>
      <p className="s-hint">
        Зато лишняя ссылка — это память в каждом узле и возня при перестройке.
      </p>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Две задачи наизусть"
      sub="Разворот списка и поиск цикла"
      main="Множество виденных узлов — линейная память; черепаха и заяц — константная."
    >
      <Cmd>
        {
          "prev = null\nпока node:\n  next = node.next · node.next = prev\n  prev = node · node = next"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Разворот"
          sub="Три переменные, один проход, константная память"
        />
        <Node
          title="Цикл: черепаха и заяц"
          sub="Быстрый прыгает через два — и неизбежно догоняет внутри круга"
        />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Честно о списках"
      sub="Практика против теории"
      main="На современных машинах массив чаще выигрывает даже там, где теория за список."
    >
      <div className="s-cols">
        <Node title="Теория" sub="Вставка за константу обещана списку" />
        <Node
          kind="amber"
          title="Практика"
          sub="Каждый узел — прыжок по памяти: кэш мстит"
        />
      </div>
      <div className="s-note">
        В большинстве современных программ связные списки проигрывают массивам
        даже там, где теория обещает им победу.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Коварная перестройка"
      sub="Потерять ссылку — потерять узел навсегда"
      main="Сначала сохраните — потом перестраивайте."
    >
      <Cmd>
        {"хвост = node.next   ← 1. сохранить сначала\nnode.next = prev    ← 2. повернуть\nprev = node         ← 3. шагнуть"}
      </Cmd>
      <div className="s-note amber">
        Пока переприсваиваете ссылки, хвост легко потерять: память утекает, а
        логика молчит.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Стек"
      sub="Последним пришёл — первым вышел"
      main="Стек стоит за вызовами функций, отменой в редакторе и проверкой скобок."
    >
      <div className="s-label">СТОПКА</div>
      <div className="s-blocks">
        <span className="s-block changed">C — вершина: снять</span>
        <span className="s-block">B</span>
        <span className="s-block">A — дно</span>
      </div>
      <div className="s-grid2">
        <Node
          mono
          title="push · pop · peek"
          sub="Положить, снять, подсмотреть — всё на вершине, всё за константу"
        />
        <Node
          title="Переполнение стека"
          sub="Слишком глубокая рекурсия — стопка, доросшая до потолка"
        />
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Очередь"
      sub="Первым пришёл — первым вышел"
      main="Очередь — честность и защита: она сглаживает всплески нагрузки."
    >
      <div className="s-cols">
        <Node mono title="голова" sub="берём здесь" />
        <Arr />
        <Node mono title="…" />
        <Arr />
        <Node mono title="хвост" sub="кладём сюда" />
      </div>
      <div className="s-grid2">
        <Node
          title="Брокеры и буферы"
          sub="Запросов больше, чем сил: излишек ждёт, а не роняет всё сразу"
        />
        <Node
          title="Дек"
          sub="Двусторонняя очередь: и стек, и очередь в одной структуре"
        />
      </div>
      <p className="s-hint">
        Связка на будущее: поиск в ширину живёт на очереди, поиск в глубину — на
        стеке.
      </p>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Очередь с приоритетами"
      sub="Важность вместо времени прихода"
      main="Каждая структура — ответ на вопрос о порядке обслуживания."
    >
      <div className="s-cols">
        <Node title="Живая очередь" sub="Кто раньше пришёл" />
        <Node
          kind="green"
          title="Больница"
          sub="Кто тяжелее, тот и раньше"
        />
      </div>
      <Node
        mono
        title="внутри почти всегда куча"
        sub="Класть и брать самый срочный — за логарифм, заглядывать на вершину — за константу"
      />
      <div className="s-note">
        Нужен срочный порядок — приоритетная очередь; честная очередь — обычная;
        история отмен — стек.
      </div>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Практика на сегодня"
      sub="Четыре упражнения, по уровням"
      main="Каждая задача — не гимнастика, а навык, который работает на годы."
    >
      <div className="s-blocks">
        <div className="s-block">
          Первый уровень: проверить строку на правильность вложенности скобок —
          стек, один проход, десяток строк
        </div>
        <div className="s-block">
          Второй: развернуть односвязный список и найти цикл черепахой и зайцем
        </div>
        <div className="s-block">
          Третий: найти в своём проекте строку, собираемую в цикле, и заменить
          накопление на конструктор — разы, а не проценты
        </div>
        <div className="s-block changed">
          На подумать: место с частыми вставками в середину коллекции — не
          должен ли это быть не массив?
        </div>
      </div>
    </Slide>
  );
}

function S16() {
  const topics = [
    ["[ ]", "Массив", "Константное чтение, друг кэша, жёсткость"],
    ["•→", "Список", "Дёшево перестраивать, дорого добираться"],
    ["abc", "Строки", "Неизменяемые: копить кусками, не склеивать"],
    ["↑↓", "Стек и очередь", "Правила поведения, а не способы хранения"],
  ];
  return (
    <Slide
      n={16}
      title="Итог"
      sub="Глава 2 · Кирпичи структур"
      main="Умение по формулировке назвать структуру — половина алгоритмического мышления."
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
        Весь будущий выбор между поиском в глубину и в ширину сведётся к выбору
        между стеком и очередью. Следующая глава — поиск и сортировка на этих
        кирпичах.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_A2 = {
  "7:2": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_A2).
export const SLIDE_TITLES_A2 = {
  "7:2": [
    "Введение",
    "Цена непрерывности",
    "Дружба с кэшем",
    "Строки",
    "Четыре задачи",
    "Массив: итог",
    "Связный список",
    "Односвязный и двусвязный",
    "Разворот и цикл",
    "Честно о списках",
    "Потеря ссылки",
    "Стек",
    "Очередь",
    "Приоритетная очередь",
    "Практика",
    "Итог",
  ],
};
