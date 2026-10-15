// Слайды для «Алгоритмы и структуры данных», глава 5 —
// «Два указателя, окно и разделяй и властвуй». Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СТРУКТУРЫ И ПАТТЕРНЫ / ГЛАВА 5</span>
      <span>{String(n).padStart(2, "0")} / 17</span>
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
    ["→", "Два указателя", "Один проход вместо вложенных циклов"],
    ["□", "Скользящее окно", "Все подряд идущие куски за линию"],
    ["÷", "Разделяй и властвуй", "Резать, решать, соединять"],
    ["?", "Распознавание", "Формулировка задачи называет инструмент"],
  ];
  return (
    <Slide
      n={1}
      title="Два указателя, окно и разделяй и властвуй"
      sub="Глава 5 · Паттерны поверх структур"
      main="Простые структуры работают за пределами очевидного — если увидеть узор."
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
        В прошлых главах мы накопили арсенал — здесь учимся им пользоваться.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Два указателя"
      sub="Первый паттерн: на смену вложенным циклам"
      main="Каждый шаг двигает только тот указатель, который приближает нас к цели."
    >
      <div className="s-cols">
        <Node kind="amber" mono title="O(n²)" sub="цикл в цикле: каждый с каждым" />
        <Arr />
        <Node
          kind="green"
          mono
          title="O(n)"
          sub="оба на краях, двигается один"
        />
      </div>
      <div className="s-note">
        Условие красоты: данные должны быть отсортированы, чтобы направление
        движения было очевидно из сравнения.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Классика: пара с суммой"
      sub="Отсортированный массив"
      main="Мала — левый вправо, велика — правый влево: один проход без памяти."
    >
      <div className="s-cols">
        <span className="s-block changed">1</span>
        <span className="s-block">3</span>
        <span className="s-block">4</span>
        <span className="s-block">7</span>
        <span className="s-block">9</span>
        <span className="s-block changed">12</span>
      </div>
      <Cmd>{"1 + 12 = 13  &gt; цель → правый влево\n1 +  9 = 10  &lt; цель → левый вправо"}</Cmd>
      <div className="s-grid2">
        <Node title="Сумма мала" sub="Левый указатель вправо — сумма растёт" />
        <Node title="Сумма велика" sub="Правый указатель влево — сумма убывает" />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Быстрый и медленный"
      sub="Фирменная вариация двух указателей"
      main="Один проход вместо двух — и никаких дополнительных структур в памяти."
    >
      <div className="s-cols">
        <Node mono title="быстрый ×2" sub="прыгает через два узла" />
        <Arr />
        <Node kind="green" mono title="медленный ×1" sub="в итоге — ровно в середине" />
      </div>
      <div className="s-blocks">
        <div className="s-block">
          Середина списка без знания длины — для сортировки слиянием списка
        </div>
        <div className="s-block">
          Проверка на цикл: черепаха и заяц из второй главы
        </div>
        <div className="s-block changed">
          Элемент за номером n с конца: быстрый выслан на n шагов вперёд
        </div>
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Скользящее окно"
      sub="Второй паттерн: родственник указателей"
      main="Окно — непрерывный кусок, который едет, не пересчитываясь с нуля."
    >
      <div className="s-cols">
        <span className="s-block">A</span>
        <span className="s-block">B</span>
        <span className="s-block changed">C</span>
        <span className="s-block changed">D</span>
        <span className="s-block changed">E</span>
        <span className="s-block">F</span>
      </div>
      <p className="s-hint">
        Окно — кусок массива или строки, ограниченный левой и правой границами,
        как объектив камеры над данными.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Механика окна"
      sub="Состояние обновляется за константу"
      main="Каждая граница движется по разу — итог линейный."
    >
      <Cmd>
        {
          "правая граница: добавила элемент\nлевая граница:  удалила\nсостояние:      сумма или частоты — O(1)"
        }
      </Cmd>
      <div className="s-note">
        Держим текущее состояние куска — сумму элементов или частоты символов в
        хеш-таблице — и правим его при каждом движении границ.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Анаграммы окном"
      sub="Окно в связке со словарём"
      main="Окно едет на один символ — частотный словарь правится на лету."
    >
      <div className="s-cols">
        <Node mono title="слово «abc»" sub="ширина окна = длине слова" />
        <Arr />
        <Node mono title="частоты в окне" />
        <Arr />
        <Node
          kind="green"
          mono
          title="сравнение словарей"
          sub="константа: алфавит ограничен"
        />
      </div>
      <div className="s-note">
        Найти все позиции, где начинается анаграмма заданного слова: окно едет
        по строке, внутри живёт частотный словарь — все позиции за один проход.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Максимум в каждом окне"
      sub="Продвинутая вариация: дек кандидатов"
      main="Дек держит кандидатов: максимум всегда на переднем крае."
    >
      <div className="s-cols">
        <Node mono title="дек" sub="убывающие кандидаты" />
        <Arr />
        <Node kind="green" mono title="голова" sub="максимум текущего окна" />
      </div>
      <div className="s-grid2">
        <Node kind="amber" mono title="O(n²)" sub="лоб: пересчитывать максимум для каждого куска" />
        <Node
          kind="green"
          mono
          title="O(n)"
          sub="дек: каждый элемент входит и выходит один раз"
        />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Когда окно нельзя"
      sub="Частые ошибки и ловушки"
      main="Нет дешёвого обновления состояния — окна не будет."
    >
      <div className="s-grid2">
        <Node
          kind="amber"
          title="Дорогое состояние"
          sub="Если нужен полный пересчёт куска — окно вырождается в квадрат"
        />
        <Node
          kind="amber"
          title="Отрицательные числа"
          sub="Сумма перестаёт расти при расширении — правило поджимания теряет смысл"
        />
      </div>
      <div className="s-note">
        Окно ищет лучшее среди подряд идущих кусков, а не среди любых
        подмножеств: задача о подмножестве с заданной суммой живёт в других
        главах.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Разделяй и властвуй"
      sub="Третий паттерн, самый глубокий"
      main="Разделить, решить рекурсивно, соединить — схема, на которой стоят логарифмы."
    >
      <div className="s-tree">
        <Node mono title="задача" />
        <Down />
        <div className="s-cols">
          <Node mono title="половина А" />
          <Arr />
          <Node mono title="половина Б" />
        </div>
        <Down />
        <Node kind="green" title="Соединить решения в ответ" />
      </div>
      <div className="s-note">
        Подзадачи того же вида и независимые. Мы уже видели схему в действии:
        сортировка слиянием живёт ровно на этих трёх шагах.
      </div>
    </Slide>
  );
}

function S11() {
  const rows = [
    ["O(n log n)", "Несколько половинных подзадач, соединение линейно"],
    ["O(log n)", "Подзадача одна — как в бинарном поиске"],
    ["хуже", "Подзадачи тяжёлые или пересекаются"],
  ];
  return (
    <Slide
      n={11}
      title="Анализ по формуле"
      sub="Сколько подзадач и почём соединение"
      main="Затык на большой задаче? Спросите: можно ли честно разрезать её пополам."
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
        Многие медленные системы лечатся именно этим разрезом: обработка по
        месяцам вместо всего периода, параллельные вычисления по кускам,
        шардирование.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Дерево отрезков"
      sub="Крайнее выражение идей разделяй и властвуй"
      main="Построили раз — меняй и спрашивай агрегат куска за логарифм."
    >
      <div className="s-tree">
        <Node kind="green" mono title="сумма 15" sub="весь массив" />
        <Down />
        <div className="s-cols">
          <Node mono title="сумма 6" sub="левая половина" />
          <Arr />
          <Node mono title="сумма 9" sub="правая половина" />
        </div>
      </div>
      <div className="s-grid2">
        <Node mono title="O(log n)" sub="спросить сумму, минимум, максимум куска" />
        <Node mono title="O(log n)" sub="изменить элемент и обновить ветку" />
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Пересекающиеся подзадачи"
      sub="Особый случай: половины делят общие куски"
      main="Независимые куски — властвуй; пересекающиеся — запоминай."
    >
      <div className="s-cols">
        <Node
          kind="green"
          title="Куски независимы"
          sub="Разделяй и властвуй работает как есть"
        />
        <Node
          kind="amber"
          title="Куски пересекаются"
          sub="Наивная рекурсия пересчитывает то же самое миллионы раз"
        />
      </div>
      <div className="s-note">
        Это территория динамического программирования, где пересекающиеся
        подзадачи учатся запоминать. Умение отличить одно от другого по
        формулировке экономит часы.
      </div>
    </Slide>
  );
}

function S14() {
  const rows = [
    ["два указателя", "массив отсортирован — с концов"],
    ["хеш-таблица", "неотсортирован — искать дополнение"],
    ["частоты остатков", "сумма делится на заданное число"],
  ];
  return (
    <Slide
      n={14}
      title="Одна задача — три инструмента"
      sub="Соберём паттерны на одной задаче: пара с заданной суммой"
      main="Отсортированность зовёт указатели, хаос — словарь, сложное условие — частоты."
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
        Зрелость — не помнить решения наизусть, а видеть, к какому паттерну
        задача принадлежит.
      </p>
    </Slide>
  );
}

function S15() {
  const rows = [
    ["«подстрока», «подмассив»", "окно или два указателя"],
    ["«отсортированный» + пара", "указатели с концов"],
    ["«объединить», «слить»", "слияние двумя указателями"],
    ["«разбить пополам»", "разделяй и властвуй"],
    ["«максимум среди подряд идущих»", "окно"],
  ];
  return (
    <Slide
      n={15}
      title="Словарь формулировок"
      sub="Тренируем глаз на распознавание"
      main="Формулировка задачи почти всегда называет инструмент — заведите такую табличку."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span>{sym}</span>
            <span className="s-path accent">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S16() {
  return (
    <Slide
      n={16}
      title="Практика на сегодня"
      sub="Пять упражнений"
      main="Линейное решение мгновенно, квадратное спит — убедитесь сами."
    >
      <div className="s-blocks">
        <div className="s-block">
          Развернуть массив и проверить палиндром двумя указателями
        </div>
        <div className="s-block">
          Самая длинная подстрока без повторяющихся символов окном
        </div>
        <div className="s-block">
          Максимальная сумма подряд идущих элементов фиксированной длины — окно
          за один проход
        </div>
        <div className="s-block">
          Возведение в степень делением пополам — сравнить число умножений с
          наивным циклом
        </div>
        <div className="s-block changed">
          Максимум в каждом окне через дек — на ста тысячах элементов
        </div>
      </div>
    </Slide>
  );
}

function S17() {
  const topics = [
    ["→", "Указатели", "Один проход, когда направление читается из сравнения"],
    ["□", "Окно", "Все куски за линию — если состояние обновляется дёшево"],
    ["÷", "Властвуй", "Логарифмы и n log n на независимых кусках"],
    ["≡", "Запоминай", "Пересекающиеся куски — территория динамического программирования"],
  ];
  return (
    <Slide
      n={17}
      title="Итог"
      sub="Глава 5 · Паттерны поверх структур"
      main="Три узора вместе с хеш-таблицей закрывают большую часть прикладных задач."
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
        В следующей главе поднимаемся над линейностью: деревья, где каждый узел
        ветвится, и обходы, которые по ним гуляют.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_A5 = {
  "7:5": [
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
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_A5).
export const SLIDE_TITLES_A5 = {
  "7:5": [
    "Введение",
    "Два указателя",
    "Пара с суммой",
    "Быстрый и медленный",
    "Скользящее окно",
    "Механика окна",
    "Анаграммы",
    "Максимум в окне",
    "Когда окно нельзя",
    "Разделяй и властвуй",
    "Анализ по формуле",
    "Дерево отрезков",
    "Пересекающиеся подзадачи",
    "Одна задача — три инструмента",
    "Словарь формулировок",
    "Практика",
    "Итог",
  ],
};
