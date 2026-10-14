// Слайды для «Изучаем Python», глава 6 — «Списки».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const PY_KW = new Set([
  "print", "for", "in", "not", "and", "or", "if", "else", "while",
  "True", "False", "None", "def", "return",
]);

// Крошечный токенизатор Python: комментарии, строки, числа, ключевые слова,
// вызовы функций. Достаточно для слайдов.
function pySpan(src) {
  const out = [];
  const re =
    /(#[^\n]*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, num, word] = m;
    if (com) out.push(<span key={out.length} className="rs-com">{tok}</span>);
    else if (str) out.push(<span key={out.length} className="rs-str">{tok}</span>);
    else if (num) out.push(<span key={out.length} className="rs-num">{tok}</span>);
    else if (word) {
      let cls = "";
      if (PY_KW.has(word)) cls = "rs-kw";
      else if (src[re.lastIndex] === "(") cls = "rs-fn";
      out.push(
        cls ? (
          <span key={out.length} className={cls}>{word}</span>
        ) : (
          <span key={out.length}>{word}</span>
        ),
      );
    } else out.push(<span key={out.length}>{tok}</span>);
  }
  return out;
}

function PyCode({ children }) {
  return <pre className="rs-code">{pySpan(children)}</pre>;
}

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ ПИТОН / ДАННЫЕ И ЦИКЛЫ / ГЛАВА 6</span>
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

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics = [
    ["[ ]", "Список", "Одно имя, много значений — центральный контейнер Питона"],
    ["nums[0]", "Индексы", "Нумерация с нуля, минус один — последний элемент"],
    [".append", "Добавить", "Добавляет в конец — список растёт на ходу"],
    ["for", "Перебор", "Цикл ходит по списку напрямую, без счётчиков"],
  ];
  return (
    <Slide
      n={1}
      title="Списки"
      sub="Глава 6 · Данные и циклы"
      main="Список — самый употребимый контейнер языка: одно имя, много значений."
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
        Письма в почте, товары в корзине, друзья в соцсети — реальность состоит
        из множеств. Хранить его по одной переменной на значение невозможно.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Создание списка"
      sub="Значения через запятую в квадратных скобках"
      main="Хорошие списки однородны: числа к числам, строки к строкам."
    >
      <PyCode>{`nums = [10, 20, 30]
empty = []
mixed = [1, "два"]   # так лучше не делать`}</PyCode>
      <div className="s-cols">
        <Node mono title="[10, 20, 30]" sub="Готов список из трёх чисел" />
        <Node kind="green" mono title="[]" sub="Пустой список — так начинают почти все программы" />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Индексы с нуля"
      sub="Доступ по номеру в квадратных скобках"
      main="Индекс — не номер по счёту, а расстояние от начала: первый — ноль."
    >
      <PyCode>{`nums = [10, 20, 30]
print(nums[0])   # 10
print(nums[2])   # 30
print(nums[3])   # ошибка!`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10\n30\nIndexError: list index out of range"}</Cmd>
      <div className="s-note">
        Для трёх элементов валидны индексы ноль, один и два — третьего нет.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Отрицательные индексы"
      sub="Минус один — последний элемент"
      main="Отрицательный индекс всегда смотрит на конец, каким бы длинным ни был список."
    >
      <PyCode>{`nums = [10, 20, 30]
print(nums[-1])   # 30
print(nums[-2])   # 20`}</PyCode>
      <div className="s-cols">
        <Node kind="green" mono title="nums[-1]" sub="Последний — даже не зная длины списка" />
        <Node mono title="nums[-2]" sub="Предпоследний: «два с конца»" />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Изменение на месте"
      sub="Присваивание по индексу заменяет элемент"
      main="Списки изменяемы — в отличие от строк, которые можно только пересобрать."
    >
      <PyCode>{`nums = [10, 20, 30]
nums[0] = 99
print(nums)      # [99, 20, 30]`}</PyCode>
      <div className="s-cols">
        <Arr />
        <Node kind="amber" mono title="строки ≠ списки" sub="Строку поменять нельзя, список — можно: он живой" />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Длина списка"
      sub="Функция len возвращает число элементов"
      main="Одна и та же функция считает и символы строки, и элементы списка."
    >
      <PyCode>{`nums = [10, 20, 30]
print(len(nums))   # 3
print(len([]))     # 0 — пустой тоже список`}</PyCode>
      <div className="s-cols">
        <Node mono title="len" sub="Знакома по главе 2: честна к любому контейнеру" />
        <Node mono title="len - 1" sub="Индекс последнего элемента" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Добавить: аппенд"
      sub="Метод append добавляет элемент в конец"
      main="Пустой список в первой строке программы — сотня значений к сотой."
    >
      <PyCode>{`nums = []
nums.append(10)
nums.append(20)
print(nums)      # [10, 20]`}</PyCode>
      <div className="s-cols">
        <Node mono title=".append(x)" sub="Ставит в конец, существующий порядок не трогает" />
        <Node kind="green" title="Так копят результаты циклов" sub="Логи, суммы, отобранные файлы" />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Перебор фором"
      sub="Цикл ходит по списку напрямую"
      main="Никаких счётчиков и индексов руками — читается как английская фраза."
    >
      <PyCode>{`for x in nums:
    print(x)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10\n20\n30"}</Cmd>
      <div className="s-note">
        x по очереди побывает каждым элементом: Питон сам достаёт их по порядку.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Вхождение: in"
      sub="Есть ли элемент в списке — истина или ложь"
      main="В главе 3 слово in проверяло подстроку в строке — теперь элемент в списке."
    >
      <PyCode>{`nums = [10, 20, 30]
print(7 in nums)    # False
print(20 in nums)   # True`}</PyCode>
      <div className="s-cols">
        <Node mono title="слева — что ищем" sub="Справа — где ищем" />
        <Node kind="green" title="Проверка перед действием" sub="Числится ли товар в корзине, есть ли имя в гостях" />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Удаление"
      sub="remove — по значению, pop — с конца"
      main="Римув убирает первое вхождение, поп снимает элемент, как тарелку со стопки."
    >
      <PyCode>{`nums = [10, 20, 30]
nums.remove(20)      # вычеркнули 20
last = nums.pop()    # сняли 30 с конца
print(nums, last)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[10] 30"}</Cmd>
      <div className="s-note">
        У pop есть версия с индексом: снимает элемент с указанной позиции.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Срезы"
      sub="Кусок списка: от индекса один до трёх"
      main="Правая граница не включается — та же логика, что у рэндж в прошлой главе."
    >
      <PyCode>{`nums = [10, 20, 30, 40]
print(nums[1:3])   # [20, 30]
print(nums[:2])    # [10, 20]
print(nums[:])     # копия всего списка`}</PyCode>
      <div className="s-cols">
        <Node mono title="[1:3]" sub="Пустое слева — «от начала», пустое справа — «до конца»" />
        <Node kind="green" mono title="[:]" sub="Полный срез — простой способ скопировать список" />
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Порядок и сводки"
      sub="Сорт — по возрастанию на месте"
      main="Максимум, минимум и сумма готовы — но в упражнениях пишем их циклом сами."
    >
      <PyCode>{`nums = [30, 10, 20]
nums.sort()
print(nums)                    # [10, 20, 30]
print(max(nums), min(nums), sum(nums))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[10, 20, 30]\n30 10 60"}</Cmd>
      <div className="s-note">
        Сорт меняет порядок навсегда — прежний не вернуть.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["[ ]", "Список", "Одно имя, много значений; изменяем на месте"],
    ["nums[0] · [-1]", "Индексы", "С нуля; отрицательные — с конца"],
    [".append · in", "Добавить и найти", "Аппенд растит список, in проверяет вхождение"],
    ["[1:3] · .sort()", "Срезы и порядок", "Правая граница не включается; сорт — на месте"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 6 · Данные и циклы"
      main="Список хорош, когда элементы ищутся по номеру: первый, второй, последний."
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
        Дальше — две главы о списках: перебор, копирование, сортировка и
        генераторы. А затем словари, где вместо номера — осмысленное имя.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P6 = {
  "13:6": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P6).
export const SLIDE_TITLES_P6 = {
  "13:6": [
    "Списки",
    "Создание списка",
    "Индексы с нуля",
    "Отрицательные индексы",
    "Изменение на месте",
    "Длина списка",
    "Добавить: аппенд",
    "Перебор фором",
    "Вхождение: in",
    "Удаление",
    "Срезы",
    "Порядок и сводки",
    "Итог",
  ],
};
