// Слайды для «Алгоритмы: продвинутый уровень», глава 3 — «Поиск и сортировка».
// Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ФУНДАМЕНТ / ГЛАВА 3</span>
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
    ["½", "Бинарный поиск", "Один шаг — минус половина данных"],
    ["≥", "Границы", "Нижняя и верхняя вместо точного попадания"],
    ["÷", "Сортировки", "Быстрая, слияние и куча со своим характером"],
    ["?", "Поиск по ответу", "Логарифм по пространству ответов"],
  ];
  return (
    <Slide
      n={1}
      title="Поиск и сортировка"
      sub="Глава 3 · Найти и упорядочить"
      main="Две задачи встречаются везде: найти нужное среди данных и навести порядок."
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
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Бинарный поиск"
      sub="Открываем словарь посередине"
      main="Один шаг сравнения — минус половина книги."
    >
      <div className="s-cols">
        <span className="s-block">1</span>
        <span className="s-block">3</span>
        <span className="s-block changed">5</span>
        <span className="s-block">7</span>
        <span className="s-block">9</span>
        <span className="s-block">11</span>
      </div>
      <div className="s-cols">
        <Node mono title="n" sub="листать подряд" />
        <Arr />
        <Node kind="green" mono title="log n" sub="делить пополам: 20 шагов на миллионе" />
      </div>
      <p className="s-hint">
        Сравнили с искомым — и одним движением выбросили половину. Повторяем с
        оставшейся.
      </p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Два жёстких требования"
      sub="Без них трюк не работает"
      main="Сортировка плюс константный доступ — связка на всю профессиональную жизнь."
    >
      <div className="s-cols">
        <Node
          kind="green"
          mono
          title="отсортировано"
          sub="Выбрасывать половину можно, только когда порядок известен"
        />
        <Node
          kind="green"
          mono
          title="доступ за O(1)"
          sub="Как в массиве: в списке середина стоит целого прохода"
        />
      </div>
      <div className="s-note">
        В связном списке бинарный поиск умирает: до середины придётся линейно
        пройти всё начало, и экономия улетучивается.
      </div>
      <p className="s-hint">
        Та же связка лежит в основе индексов баз данных.
      </p>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Дисциплина границ"
      sub="Писать бинарный поиск умеют все, без ошибок — почти никто"
      main="Проверяйте решение на массивах из нуля, одного и двух элементов — там живут все ошибки."
    >
      <Cmd>
        {
          "lo = 0 · hi = n            ← полуинтервал, решить заранее\nпока lo < hi:\n  mid = lo + (hi - lo) // 2 ← без переполнения\n  сдвигать за середину, не трогая проверенный"
        }
      </Cmd>
      <Node
        kind="amber"
        title="Ошибки живут на краях"
        sub="Смещение на единицу, вечный цикл, пропущенный элемент"
      />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Нижняя и верхняя границы"
      sub="Найти не значение, а место"
      main="Нашли равенство — не останавливайтесь: сжимайте диапазон до первого подходящего."
    >
      <div className="s-cols">
        <span className="s-block">1</span>
        <span className="s-block">2</span>
        <span className="s-block changed">4</span>
        <span className="s-block">4</span>
        <span className="s-block">4</span>
        <span className="s-block">7</span>
      </div>
      <div className="s-grid2">
        <Node
          mono
          title="lower bound"
          sub="Первый ≥ x: куда вставить, сколько элементов меньше"
        />
        <Node
          mono
          title="upper bound"
          sub="Первый &gt; x: размер диапазона повторов"
        />
      </div>
      <p className="s-hint">
        Цикл остаётся логарифмическим, а полезность взлетает — в библиотеках эти
        функции так и называются.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Бинарный поиск по ответу"
      sub="Ищем не в массиве, а в пространстве возможных ответов"
      main="Если про ответ можно спросить «да/нет» и ответы монотонны — ищите бинарно."
    >
      <div className="s-cols">
        <Node title="Кандидат" sub="Проверяем за один проход: набирается ли нужное количество" />
        <Down />
        <Node kind="green" title="Монотонность" sub="Длина подходит — любая меньшая тоже" />
      </div>
      <div className="s-note">
        Пилорама: перебирать длины лениво — их слишком много. Гуляем бинарным
        поиском по диапазону длин, для кандидата делаем линейную проверку.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Три элементарные сортировки"
      sub="Все квадратные, но каждая с характером"
      main="Секрет вставок: на почти отсортированных данных они почти линейны."
    >
      <div className="s-cols">
        <Node
          title="Пузырёк"
          sub="Меняем соседние пары с нарушенным порядком: максимум всплывает в конец"
        />
        <Node
          title="Выбор"
          sub="Минимум — на первое место неотсортированной части: перестановок минимум"
        />
        <Node
          kind="green"
          title="Вставки"
          sub="Как карты в руке: сдвигаем влево, пока не встанет на место"
        />
      </div>
      <p className="s-hint">
        Выбор важен, когда переставлять элементы дорого; вставки — когда данные
        почти упорядочены.
      </p>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Устойчивость"
      sub="Вопрос, который всплывёт на каждом собеседовании"
      main="Устойчивость — инструмент, а не деталь: пользоваться ею нужно сознательно."
    >
      <div className="s-cols">
        <Node
          kind="green"
          title="Устойчивая"
          sub="Равные элементы сохраняют исходный порядок"
        />
        <Node kind="amber" title="Неустойчивая" sub="Равные перемешиваются" />
      </div>
      <div className="s-note">
        Сортировка по двум полям без единой строчки лишнего кода: сначала по
        второму полю, потом устойчиво по первому.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Быстрая сортировка"
      sub="Королева практических сортировок"
      main="Опорный элемент, один линейный проход, рекурсия — и массив отсортирован."
    >
      <div className="s-tree">
        <Node mono title="опора" sub="выбрали элемент" />
        <Down />
        <div className="s-grid2">
          <Node mono title="меньше опоры" />
          <Node kind="green" mono title="опора — на своё место" sub="окончательное" />
          <Node mono title="больше опоры" />
        </div>
      </div>
      <div className="s-grid2">
        <Node kind="green" mono title="O(n log n)" sub="в среднем · на месте" />
        <Node title="Разделение" sub="одним проходом по массиву" />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Тёмная сторона королевы"
      sub="Неудачная опора"
      main="Квадрат у быстрой сортировки — не гипотеза, а построимый случай."
    >
      <div className="s-tree">
        <Node
          kind="amber"
          title="Опора — первый элемент, массив уже отсортирован"
        />
        <Down />
        <div className="s-cols">
          <Node mono title="1 элемент" />
          <Arr />
          <Node kind="amber" mono title="всё остальное" />
        </div>
      </div>
      <div className="s-note">
        Каждое разделение раскалывает массив на одиночку и всё остальное:
        глубина рекурсии становится линейной, сложность сползает в квадрат.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Сортировка слиянием"
      sub="Противоположность по характеру"
      main="Никаких злых данных в принципе: гарантированные n log n и устойчивость."
    >
      <div className="s-tree">
        <Node title="Делим пополам, пока куски не станут по одному" />
        <Down />
        <Node
          kind="green"
          title="Сливаем два отсортированных куска"
          sub="за линейное время"
        />
      </div>
      <div className="s-grid2">
        <Node kind="green" mono title="Θ(n log n)" sub="гарантия на любых данных" />
        <Node kind="amber" title="Цена" sub="линейная память под копию массива" />
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Слияние — приём ценнее сортировки"
      sub="Два отсортированных потока — в один за линию"
      main="Умение слить два отсортированных списка нужно в десятках мест."
    >
      <div className="s-cols">
        <Node mono title="логи А" sub="по времени" />
        <Arr />
        <Node mono title="логи Б" />
        <Arr />
        <Node kind="green" mono title="одна лента" />
      </div>
      <div className="s-note">
        Объединить логи двух сервисов, пересечь два отсортированных списка,
        внешняя сортировка — везде одно и то же движение двух указателей.
      </div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title="Куча"
      sub="Дерево, спрятанное внутри массива"
      main="Нет плохих данных вовсе: худший случай равен среднему."
    >
      <div className="s-tree">
        <Node kind="green" mono title="9 — максимум" sub="всегда на вершине" />
        <Down />
        <div className="s-cols">
          <Node mono title="7" />
          <Arr />
          <Node mono title="8" />
        </div>
      </div>
      <Cmd>{"дети i: 2i + 1 и 2i + 2\nродитель i: (i - 1) // 2"}</Cmd>
      <div className="s-grid2">
        <Node mono title="O(n)" sub="построить из массива" />
        <Node mono title="n log n" sub="снимать вершину и восстанавливать — итого, на месте" />
      </div>
    </Slide>
  );
}

function S14() {
  return (
    <Slide
      n={14}
      title="Что используют библиотеки"
      sub="Победили гибриды"
      main="Лучшие черты разных сортировок собраны в одной."
    >
      <div className="s-grid2">
        <div className="s-card">
          <div className="s-label">ТИМСОРТ</div>
          <span className="s-node-title">Ищет уже отсортированные серии</span>
          <span className="s-node-sub">
            Маленькие неупорядоченные куски — вставками, затем сливает
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">ИНТРОСПЕКТИВНАЯ</div>
          <span className="s-node-title">Быстрая со страховкой</span>
          <span className="s-node-sub">
            Рекурсия слишком глубока — переключение на гарантии кучи
          </span>
        </div>
      </div>
      <p className="s-hint">
        Отсюда и оговорка из первой главы: простые методы на маленьких кусках.
      </p>
    </Slide>
  );
}

function S15() {
  return (
    <Slide
      n={15}
      title="Практика на сегодня"
      sub="Четыре упражнения"
      main="Шаблон поселяется в голове только через руки."
    >
      <div className="s-blocks">
        <div className="s-block">
          Бинарный поиск с нижней границей — проверьте на массивах с повторами
        </div>
        <div className="s-block">
          Сортировка вставками на почти отсортированных данных — результат вас
          удивит
        </div>
        <div className="s-block">
          Сортировка по двум полям: дважды применить устойчивую — сначала второе
          поле, потом первое
        </div>
        <div className="s-block changed">
          Одна задача бинарным поиском по ответу — пилорама или её аналог
        </div>
      </div>
    </Slide>
  );
}

function S16() {
  const topics = [
    ["½", "Поиск", "Линейный — для беспорядка, бинарный — для порядка"],
    ["≥", "Границы", "Полезнее точного попадания; по ответу — логарифм"],
    ["÷", "Сортировки", "Вставки на почти упорядоченном, быстрая на практике"],
    ["▲", "Гарантии", "Слияние — устойчивость, куча — худший случай"],
  ];
  return (
    <Slide
      n={16}
      title="Итог"
      sub="Глава 3 · Найти и упорядочить"
      main="Устойчивость — инструмент, а не деталь: использовать её нужно сознательно."
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
        В следующей главе — структура, которая на первый взгляд делает всё это
        ненужным: хеш-таблицы, находящие данные без всякой сортировки.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_A3 = {
  "7:3": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_A3).
export const SLIDE_TITLES_A3 = {
  "7:3": [
    "Введение",
    "Бинарный поиск",
    "Два требования",
    "Дисциплина границ",
    "Нижняя и верхняя границы",
    "Поиск по ответу",
    "Элементарные сортировки",
    "Устойчивость",
    "Быстрая сортировка",
    "Тёмная сторона",
    "Сортировка слиянием",
    "Слияние как приём",
    "Куча",
    "Гибриды библиотек",
    "Практика",
    "Итог",
  ],
};
