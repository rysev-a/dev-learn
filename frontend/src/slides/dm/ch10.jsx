// Слайды для «Дискретной математики», глава 10 — «Вероятность и теорема Байеса».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ДИСКРЕТНАЯ МАТЕМАТИКА / ГРАФЫ И ВЕРОЯТНОСТЬ / ГЛАВА 10</span>
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
    [
      "1/6",
      "Классическая вероятность",
      "Доля благоприятных исходов среди равновозможных",
    ],
    ["P(A|B)", "Условная вероятность", "Пересчёт оценки, когда мир сжался"],
    ["P(H|E)", "Теорема Байеса", "Обновление уверенности новыми данными"],
    ["9%", "Базовая частота", "Почему точный тест редкой болезни лжёт"],
  ];
  return (
    <Slide
      n={1}
      title="Вероятность и Байес"
      sub="Глава 10 · Графы и вероятность"
      main="Каждый день состоит из случайностей, о которых можно рассуждать строго."
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
        Финальная глава курса: кэши, A/B-тесты и алерты живут на этих формулах.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Классическая вероятность"
      sub="Почти наивное определение"
      main="Вероятность — доля благоприятных исходов среди всех равновозможных."
    >
      <Cmd>{"P(событие) = благоприятные исходы / все исходы"}</Cmd>
      <div className="s-bar-wrap">
        <span>
          <span className="s-path accent">кость · чётное</span> · 3 из 6
        </span>
        <div className="s-bar">
          <div style={{ width: "50%" }} />
        </div>
        <span>
          <span className="s-path accent">монета · решка</span> · 1 из 2
        </span>
        <div className="s-bar">
          <div style={{ width: "50%" }} />
        </div>
      </div>
      <div className="s-note">
        Как только исходов становится много, считать их доли без правил подсчёта
        из первых глав уже не получится.
      </div>
    </Slide>
  );
}

function S03() {
  const rows = [
    ["2⁵ = 32", "пять монет: каждая удваивает варианты"],
    ["C(20, 5) = 15 504", "стартовая пятёрка из двадцати разработчиков"],
    ["23 человека", "253 пары дней рождения → совпадение больше 50%"],
  ];
  return (
    <Slide
      n={3}
      title="Комбинаторика случайностей"
      sub="Не гость, а хозяйка"
      main="Интуиция про случайность ненадёжна, а формулы подсчёта — надёжны."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note amber">
        Парадокс дней рождения стоит на простом подсчёте: пар в комнате почти
        двести пятьдесят, а не двадцать два.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="События: или и и"
      sub="Арифметика над событиями"
      main="Вероятность «или» — сумма вероятностей минус вероятность «и»."
    >
      <Cmd>{"P(A ∪ B) = P(A) + P(B) − P(A ∩ B)"}</Cmd>
      <div className="s-cols">
        <Node
          mono
          title="«или» — объединение"
          sub="ошибка в базе или ошибка в сети"
        />
        <Node
          mono
          title="«и» — пересечение"
          sub="ошибка в базе и ретрай исчерпан"
        />
      </div>
      <div className="s-note">
        Минус — за общие случаи: без них те, кто попал в обе категории,
        посчитаются дважды. Запишите событие словами — формула соберётся сама.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Независимость событий"
      sub="Знание об одном ничего не меняет в оценке другого"
      main="Для независимых событий вероятность того и другого сразу — произведение."
    >
      <div className="s-grid2">
        <Node
          mono
          kind="green"
          title="Независимые"
          sub="P(A ∩ B) = P(A) · P(B): шестёрка на первом кубике не меняет 1/6 на втором"
        />
        <Node
          mono
          kind="amber"
          title="Несовместные ≠ независимые"
          sub="«чётное» и «три» вместе не случатся, но одно информирует о другом"
        />
      </div>
      <div className="s-note">
        Зависимость — это про информацию, а не про одновременность.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Условная вероятность"
      sub="Главный инструмент главы"
      main="Оценка, пересчитанная с учётом того, что другое уже случилось."
    >
      <Cmd>{"P(A | B) = P(A ∩ B) / P(B)"}</Cmd>
      <div className="s-bar-wrap">
        <span>
          <span className="s-path accent">весь мир</span> · P(дождь)
        </span>
        <div className="s-bar">
          <div style={{ width: "25%" }} />
        </div>
        <span>
          <span className="s-path accent">мир сжат до «пасмурно»</span> ·
          P(дождь | пасмурно)
        </span>
        <div className="s-bar">
          <div style={{ width: "70%" }} />
        </div>
      </div>
      <div className="s-note">
        Сжимаем мир до случаев, где B произошло, и смотрим долю A среди них:
        пасмурно — дождь вероятнее, хотя климат тот же.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Теорема Байеса"
      sub="Правило оборачивания условия"
      main="От наблюдаемого следствия — к вероятности причины: уверенность обновляется данными."
    >
      <div className="s-cols">
        <Node mono title="Априор P(H)" sub="сколько верим причине заранее" />
        <Arr />
        <Node
          title="Свидетельство E"
          sub="насколько характерен симптом: P(E | H)"
        />
        <Arr />
        <Node
          mono
          kind="green"
          title="Апостериор P(H | E)"
          sub="обновлённая уверенность"
        />
      </div>
      <Cmd>{"P(H | E) ∝ P(E | H) · P(H)"}</Cmd>
      <div className="s-note">
        Была априорная уверенность — сколько раз сервис падал раньше; пришло
        свидетельство — сработал мониторинг; стала апостериорной. Байес —
        честная бухгалтерия убеждений.
      </div>
    </Slide>
  );
}

function S08() {
  const rows = [
    ["больные", "≈100 на 100 000 · тест ловит 99"],
    ["здоровые", "≈99 900 · ложный «плюс» у ≈1 000"],
    ["среди «плюс»", "99 / 1 098 ≈ 9%, а не 99%"],
  ];
  return (
    <Slide
      n={8}
      title="Ловушка с болезнью"
      sub="Тест хороший, результат обманчив"
      main="Тест ловит 99 из 100 больных, но положительный результат верен лишь на 9%."
    >
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <div className="s-bar-wrap">
        <span>
          <span className="s-path accent">истинно больные</span> · 99
        </span>
        <div className="s-bar">
          <div style={{ width: "9%" }} />
        </div>
        <span className="amber-text">
          <span className="s-path accent">ложные тревоги</span> · ≈999
        </span>
        <div className="s-bar amber">
          <div style={{ width: "91%" }} />
        </div>
      </div>
      <div className="s-note">
        Это не дефект теста, а сила базовой частоты: здоровых слишком много,
        поэтому положительный результат чаще означает ошибку, чем болезнь.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Спам-фильтр на Байесе"
      sub="Механизм, на котором живёт вся почта"
      main="Фильтр не «знает», что перед ним спам, — он обновляет уверенность слово за словом."
    >
      <div className="s-cols">
        <Node mono title="Априор: спам 1/3" sub="опыт всей прошлой почты" />
        <Arr />
        <Node
          title="«бесплатно»"
          sub="среди спама встречается несравнимо чаще"
        />
        <Arr />
        <Node
          mono
          kind="green"
          title="Оценка ↑"
          sub="десяток слов — письмо уезжает в спам"
        />
      </div>
      <div className="s-note">
        Байес перемножает априорную уверенность с тем, насколько слово
        характерно для спама, и выдаёт обновлённую оценку.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Пренебрежение базовой частотой"
      sub="Ловушка из параграфа про болезнь"
      main="Характерность свидетельства люди оценивают неплохо, а распространённость причины — проваливаются."
    >
      <div className="s-cols">
        <Node
          kind="amber"
          title="Редкий алерт на редкое событие"
          sub="почти всегда ложный — настройте пороги с учётом априорной частоты"
        />
        <Node
          title="Редкое ищут каскадом"
          sub="дешёвый грубый фильтр, потом дорогой точный анализ"
        />
      </div>
      <div className="s-note">
        Даже идеально точный инструмент на редкое явление даёт в основном ложные
        тревоги.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Вероятность в инженерии"
      sub="Проявляется на каждом шагу"
      main="Решения об ёмкости, порогах и фильтрах принимаются на числах, а не на чуйке."
    >
      <div className="s-grid2">
        <Node title="Кэш" sub="P(попадания) · выигрыш − P(промаха) · цена" />
        <Node
          title="Фильтр Блума"
          sub="«возможно, есть» с контролируемой ошибкой, «точно нет» — безошибочно"
        />
        <Node
          title="A/B-тест"
          sub="по накопленным данным обновляем уверенность, что вариант лучше"
        />
        <Node
          title="Ретраи и реплики"
          sub="выбор числа — прикидка вероятностей отказа"
        />
      </div>
      <div className="s-note">
        Контролируемая вероятность ложного «возможно» — та цена, за которую Блум
        экономит миллионы запросов к базе.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Диагностика по Байесу"
      sub="Сервис упал, горит пять алертов"
      main="Вероятность каждой причины при симптомах — априорная частота, умноженная на характерность."
    >
      <Cmd>{"P(причина | алерты) ∝ P(алерты | причина) · P(причина)"}</Cmd>
      <div className="s-cols">
        <Node
          title="Априорная частота"
          sub="что ломается чаще — с этого начинаем"
        />
        <Node
          title="Характерность симптома"
          sub="что лучше объясняет картину"
        />
      </div>
      <div className="s-note">
        Опытный дежурный делает это интуитивно; формулы делают интуицию
        воспроизводимой, а документация инцидентов — накопленная таблица
        априорных частот вашей системы.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["Σ", "Счёт", "Множества, отношения и комбинаторика — язык данных и счёта"],
    ["∀", "Логика", "Предикаты, кванторы, индукция и рекуррентности"],
    ["V·E", "Графы", "Дом-деревья, зависимости, маршруты и обходы"],
    ["P", "Вероятность", "Байес: рассуждать там, где гарантий нет"],
  ];
  return (
    <Slide
      n={13}
      title="Итог курса"
      sub="Глава 10 · Графы и вероятность"
      main="Курс стал вашим инструментом: считайте, доказывайте, обходите и оценивайте."
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
        Дальше — программирование на Python и алгоритмы: там всё это оживёт
        строчка за строчкой.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_M10 = {
  "12:10": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_M10).
export const SLIDE_TITLES_M10 = {
  "12:10": [
    "Вероятность и Байес",
    "Классическая вероятность",
    "Комбинаторика случайностей",
    "События: или и и",
    "Независимость событий",
    "Условная вероятность",
    "Теорема Байеса",
    "Ловушка с болезнью",
    "Спам-фильтр на Байесе",
    "Пренебрежение базовой частотой",
    "Вероятность в инженерии",
    "Диагностика по Байесу",
    "Итог курса",
  ],
};
