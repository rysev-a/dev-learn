// Слайды для «Изучаем JavaScript», глава 5 — «Два указателя и скользящее окно».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>СТРУКТУРЫ И ПАТТЕРНЫ / ГЛАВА 5</span>
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
    ["↔", "Встречные указатели", "Два конца навстречу: пары в отсортированных данных"],
    ["»", "Быстрый и медленный", "Разная скорость несёт знание без памяти"],
    ["▭", "Скользящее окно", "Лучший кусок подряд идущих элементов"],
    ["÷", "Разделяй и властвуй", "Разрезать, решить рекурсивно, соединить"],
  ];
  return (
    <Slide
      n={1}
      title="Два указателя и скользящее окно"
      sub="Глава 5 · Структуры и паттерны"
      main="Хороший алгоритм отличается от плохого не структурой данных, а траекторией."
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
        Массивы перестают быть просто хранилищем и становятся полем для
        движений: кто, откуда и в каком порядке смотрит на элементы.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Встречные указатели"
      sub="Пара с заданной суммой в отсортированном массиве"
      main="Каждый шаг выбрасывает элемент, который уже не может участвовать в ответе."
    >
      <Cmd>
        {
          "[2, 7, 11, 15]   target = 9\n L          R    2 + 15 = 17 > 9  → R--\n L       R       2 + 11 = 13 > 9  → R--\n L    R          2 + 7  = 9  ✓  ответ"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          mono
          kind="green"
          title="O(n)"
          sub="Один проход вместо всех пар — линейность вместо квадрата"
        />
        <Node
          kind="amber"
          title="Массив обязан быть отсортированным"
          sub="Часто честнее сначала заплатить n log n за сортировку"
        />
      </div>
      <p className="s-hint">
        В JavaScript это две переменные с индексами и цикл while — никаких
        структур не нужно.
      </p>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Быстрый и медленный"
      sub="Одно направление, разная скорость"
      main="Скорость указателя — способ нести знание без дополнительной памяти."
    >
      <Cmd>
        {
          "let slow = head, fast = head;\nwhile (fast && fast.next) {\n  slow = slow.next;        // шаг через одного\n  fast = fast.next.next;   // шаг через двух\n} // когда быстрый добежит — slow в центре"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          title="Удалить дубликаты"
          sub="Медленный — граница готового, быстрый — разведчик"
        />
        <Node title="Середина за один проход" sub="Быстрый шагает через два, медленный через одного" />
        <Node title="Флойд и циклы" sub="Тот же алгоритм, что в главе о списках" />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Окно фиксированной ширины"
      sub="Максимум суммы n подряд идущих элементов"
      main="Не пересчитывать кусок заново, а обновлять его состояние между шагами."
    >
      <Cmd>
        {
          "окно = 3\n s1+s2+s3 = 20               ← посчитали один раз\n(s1+s2+s3) − s1 + s4 = 21   ← два движения на шаг"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          mono
          kind="amber"
          title="O(n·k)"
          sub="Наивно: для каждого начала пересчитать k слагаемых"
        />
        <Node
          mono
          kind="green"
          title="O(n)"
          sub="Один проход, константная память на поддержку состояния"
        />
      </div>
      <p className="s-hint">
        Простейший инкрементальный пересчёт — идея окупается в десятках задач,
        от метрик до буферов видео.
      </p>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Окно переменной ширины"
      sub="Самая длинная подстрока без повторяющихся символов"
      main="Три переменные и линейное время там, где перебор подстрок стоил бы куб."
    >
      <Cmd>
        {
          "const last = new Map();   // символ → последняя позиция\nif (last.get(s[r]) >= l) l = last.get(s[r]) + 1;\nlast.set(s[r], r);\nbest = Math.max(best, r - l + 1);"
        }
      </Cmd>
      <div className="s-cols">
        <Node mono title="l" sub="Левая граница окна" />
        <Node mono title="Map" sub="Словарь последних позиций" />
        <Node mono kind="green" title="best" sub="Лучший ответ за всё время" />
      </div>
      <p className="s-hint">
        Вариант с последними позициями изящнее: левая граница не ползёт по
        одному, а прыгает прямо за прошлую встречу символа.
      </p>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Окно плюс частоты"
      sub="Самый переиспользуемый узор темы"
      main="Один раз усвоить механику — и узнавать её в чужих задачах по формулировке."
    >
      <div className="s-opts">
        <span className="s-path accent">нет повторов?</span>
        <span>подстрока без повторов</span>
        <span className="s-path accent">покрыт набор?</span>
        <span>минимальное окно с нужными буквами</span>
        <span className="s-path accent">хватит замен?</span>
        <span>самая длинная с k поправками</span>
      </div>
      <div className="s-grid2">
        <Node title="Вошёл символ" sub="Счётчик плюс единица" />
        <Node title="Вышел символ" sub="Счётчик минус единица" />
      </div>
      <div className="s-note">
        Отдельная переменная следит за числом выполненных условий — состояние
        окна обновляется инкрементально, без пересчётов.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Максимум в окне: дек"
      sub="Двусторонняя очередь индексов-кандидатов"
      main="Выталкивай тех, кто уже никогда не станет ответом."
    >
      <Cmd>
        {
          "дек держит индексы по убыванию значений\nновый элемент → выталкивает с хвоста всех меньше себя\nответ окна    → отгружается с головы, когда его индекс вышел"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          mono
          kind="green"
          title="O(n)"
          sub="Каждый элемент входит и покидает дек ровно один раз"
        />
        <Node
          mono
          kind="amber"
          title="O(n·k)"
          sub="Лобово: максимум каждого куска пересчитывается заново"
        />
      </div>
      <p className="s-hint">
        «Старше и слабее — никогда не станет ответом»: приём полезен далеко за
        пределами этой задачи.
      </p>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Окна в продакшне"
      sub="Данные идут потоком, вопрос — про подряд идущий кусок"
      main="Если кусок дёшево обновить при сдвиге границы — вы в мире скользящего окна."
    >
      <div className="s-cols">
        <div className="s-card">
          <div className="s-label">МЕТРИКИ</div>
          <span className="s-node-title">Окно времени — родная среда</span>
          <span className="s-node-sub">
            Средняя задержка за пять минут, ошибки за час, всплески активности
          </span>
        </div>
        <div className="s-card">
          <div className="s-label">ПОТОКИ</div>
          <span className="s-node-title">Буферы видео и аудио</span>
          <span className="s-node-sub">Ровно окно последних секунд</span>
        </div>
      </div>
      <Node
        title="Поиск с ограничениями"
        sub="Подстроки и подмассивы: текстовый поиск, биоинформатика, проверка паролей"
      />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Ловушки скользящего окна"
      sub="Три способа сломать приём"
      main="Поджимать левую границу можно, только если сумма растёт с расширением."
    >
      <div className="s-blocks">
        <div className="s-block">
          Отрицательные числа ломают окно с суммой: правило «подожми, пока
          стало лучше» перестаёт быть верным — для таких сумм есть префиксные
          суммы
        </div>
        <div className="s-block">
          Состояние нельзя обновить дёшево — каждый сдвиг тянет полный
          пересчёт, и окно вырождается в квадрат; честнее другой подход
        </div>
        <div className="s-block changed">
          Окно ищет лучшее среди подряд идущих кусков, а не среди любых
          подмножеств — путать эти постановки не стоит
        </div>
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Разделяй и властвуй"
      sub="Три шага: разделить, решить рекурсивно, соединить"
      main="Сила метода живёт в анализе, а не в синтаксисе."
    >
      <div className="s-tree">
        <Node title="Задача" sub="разрезать на независимые подзадачи того же вида" />
        <Down />
        <div className="s-grid2">
          <Node
            mono
            title="обе половины + слияние"
            sub="сортировка слиянием → n log n"
          />
          <Node
            mono
            kind="green"
            title="решаем только одну"
            sub="бинарный поиск → логарифм"
          />
        </div>
      </div>
      <div className="s-note">
        В JavaScript рекурсия пишется естественно, но каждый вызов живёт на
        стеке: для очень глубоких разбиений явный стек надёжнее неявного.
      </div>
    </Slide>
  );
}

function S11() {
  const rows = [
    ["b^16 → (b^8)²", "4 умножения вместо 16: каждый шаг режет показатель вдвое"],
    ["обе половины · слияние O(n)", "итого n log n"],
    ["одна половина", "итого логарифм"],
  ];
  return (
    <Slide
      n={11}
      title="Быстрое возведение в степень"
      sub="Разбор анализа как шаблон"
      main="Спросите: можно ли честно разрезать большую задачу на независимые куски?"
    >
      <Cmd>
        {
          "b^e = (b^(e/2))²          e чётный\nb^e = (b^(e/2))² · b      e нечётный — домножили на основу"
        }
      </Cmd>
      <div className="s-table">
        {rows.map(([sym, d]) => (
          <div key={sym}>
            <span className="s-path accent">{sym}</span>
            <span>{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">
        Многие медленные системы лечатся разрезом: обработка по месяцам вместо
        всего периода, параллельные вычисления, шардирование.
      </p>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Префиксные суммы"
      sub="Один проход — и любой диапазон за константу"
      main="Разбей на куски и посчитай агрегаты один раз."
    >
      <Cmd>
        {
          "p[0] = 0;  p[i] = p[i-1] + a[i-1]\nsum(l, r) = p[r] - p[l]    ← константа на запрос"
        }
      </Cmd>
      <div className="s-grid2">
        <Node
          mono
          kind="green"
          title="O(1) на запрос"
          sub="Разность двух префиксов после линейной подготовки"
        />
        <Node
          mono
          kind="amber"
          title="O(n) памяти"
          sub="Обмен памяти на скорость в самом наглядном виде"
        />
      </div>
      <div className="s-note">
        Дружит с окнами фиксированной ширины: вместо суммы на лету — готовые
        клетки. Тысячи запросов плюс обновления элементов — черёд дерева
        отрезков, его отложим до главы о деревьях.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["↔", "Встречные", "Пары в отсортированных данных"],
    ["»", "Скорости", "Позиции и циклы: дубликаты, середина, Флойд"],
    ["▭", "Окно", "Лучшие куски подряд, состояние — словарь частот"],
    ["÷", "Властвуй", "Разрез на независимые части: логарифмы и n log n"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 5 · Структуры и паттерны"
      main="Каждая траектория — линейный проход вместо перебора."
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
        Ловушки: отрицательные суммы, дорогой пересчёт состояния, путаница
        между кусками и подмножествами. Следующая глава — деревья и обходы по
        ним.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_J5 = {
  "11:5": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J5).
export const SLIDE_TITLES_J5 = {
  "11:5": [
    "Три траектории движения",
    "Встречные указатели",
    "Быстрый и медленный",
    "Окно фиксированной ширины",
    "Окно переменной ширины",
    "Окно плюс частоты",
    "Максимум окна через дек",
    "Окна в продакшне",
    "Ловушки скользящего окна",
    "Разделяй и властвуй",
    "Быстрое возведение в степень",
    "Префиксные суммы",
    "Итог",
  ],
};
