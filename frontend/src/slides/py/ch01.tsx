import { makeSlide } from "../SlideFrame.tsx";
import { Arr, Cmd, Node, makePyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 1 — «Первая программа».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Питоне с подсветкой синтаксиса (классы rs-*).

const PY_KW = new Set([
  "print", "def", "if", "elif", "else", "for", "while", "in", "not", "and",
  "or", "return", "import", "from", "True", "False", "None", "class", "with",
]);

const PyCode = makePyCode(PY_KW);

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ОСНОВЫ / ГЛАВА 1", 13);

const Down = () => <span className="s-arr">↓</span>;

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics: [string, string, string][] = [
    ["print", "Принт", "Печатает на экране всё, что отдали в скобках"],
    ["«…»", "Строки", "Текст живёт в кавычках — одинарных или двойных"],
    ["#", "Комментарии", "Заметки для людей: Питон их не читает"],
    ["7 / 2", "Арифметика", "Числа считает, строки повторяет и склеивает"],
  ];
  return (
    <Slide
      n={1}
      title="Первая программа"
      sub="Глава 1 · Основы"
      main="Программа — список команд, который машина читает как рецепт."
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
        Питон читается почти как английский: на нём пишут и маленькие скрипты,
        и нейросети. Каждая идея курса сразу закрепляется упражнением с
        настоящей проверкой кода.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Команда принт"
      sub="Печатает на экране то, что ей отдали"
      main="Скобки — как у математической функции: внутри них то, что нужно показать."
    >
      <PyCode>{`print("Привет, мир!")`}</PyCode>
      <div className="s-cols">
        <Node mono title="print" sub="Команда печати: бумаги нет, только экран" />
        <Arr />
        <Node kind="green" mono title={'"Привет, мир!"'} sub="То, что появится на экране" />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Строки и кавычки"
      sub="Текст в кавычках называется строкой"
      main="Кавычки — ограда: всё внутри Питон считает текстом, даже цифры."
    >
      <PyCode>{`print("Привет!")
print('Пока!')
print("2")   # это текст, а не число`}</PyCode>
      <div className="s-cols">
        <Node mono title={'"…" = \'…\''} sub="Одинарные и двойные равноправны" />
        <Node kind="green" title="Один вид с обеих сторон" sub="Открыли и закрыли одинаково — иначе Питон запутается" />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Порядок сверху вниз"
      sub="Несколько команд принт подряд"
      main="Программа — список команд: машина читает его как рецепт, шаг за шагом."
    >
      <PyCode>{`print("Раз")
print("Два")
print("Три")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Раз\nДва\nТри"}</Cmd>
      <div className="s-note">
        Выполняется по одной строке за раз — и печатается в том же порядке.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Комментарии"
      sub="Решётка прячет заметки для людей"
      main="Хороший комментарий объясняет зачем, а не пересказывает что."
    >
      <PyCode>{`# печатаем подсказку, чтобы пользователь не потерялся
print("Введите имя")`}</PyCode>
      <div className="s-cols">
        <Node kind="amber" mono title="# комментарий" sub="После решётки Питон ничего не выполняет" />
        <Node kind="green" title="Кому адресованы" sub="Себе через месяц и коллеге сегодня" />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Принт умеет считать"
      sub="Сначала арифметика, потом печать"
      main="Скобки меняют порядок действий — как в школе."
    >
      <PyCode>{`print(2 + 2)        # 4
print(2 * 3)        # 6  · умножение — звёздочка
print((2 + 2) * 2)  # 8  · скобки важнее всего`}</PyCode>
      <div className="s-cols">
        <Node mono title="+ −" sub="Сложение и вычитание — как в школе" />
        <Node mono title="*" sub="Умножение — звёздочка: крестика на клавиатуре нет" />
        <Node mono title="/" sub="Деление — слэш" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Дробные числа"
      sub="7 / 2 = 3.5 — дробь через точку"
      main="Деление всегда даёт дробь — даже когда выходит ровное целое."
    >
      <PyCode>{`print(7 / 2)   # 3.5
print(6 / 2)   # 3.0`}</PyCode>
      <div className="s-cols">
        <Node mono title="3.5" sub="Дробные числа — через точку, не запятую" />
        <Node kind="amber" mono title="3.0" sub="Целые и дробные — два разных вида чисел" />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Несколько значений"
      sub="Перечислите через запятую"
      main="Принт напечатает их в одну строку, разделив пробелами."
    >
      <PyCode>{`print("Сумма:", 2 + 2)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Сумма: 4"}</Cmd>
      <div className="s-note">
        Значение и пояснение рядом: экран сразу отвечает, что это и сколько.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Кавычка внутри текста"
      sub="Что если кавычка нужна внутри самой строки"
      main="Ограды должны отличаться: снаружи один вид кавычек, внутри другой."
    >
      <PyCode>{`print("Он сказал: 'привет'")
print('А здесь "двойные" внутри')`}</PyCode>
      <div className="s-cols">
        <Node kind="green" mono title={'"…\'…\'…"'} sub="Снаружи двойные — внутри одинарные" />
        <Node kind="green" mono title={'\'…"…"…\''} sub="Работает и наоборот" />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Арифметика строк"
      sub="У строк своя маленькая арифметика"
      main="Только плюс и звёздочка: вычитать и делить строки нельзя."
    >
      <PyCode>{`print("ля" * 3)          # ляляля
print("Привет, " + "мир")`}</PyCode>
      <div className="s-cols">
        <Node mono title="строка * N" sub="Звёздочка повторяет: линия из тридцати чёрточек — одна чёрточка на тридцать" />
        <Node mono title="строка + строка" sub="Плюс склеивает две строки в одну" />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Пустой принт"
      sub="Пустые скобки — пустая строка"
      main="Пустота — часть оформления: выводу, как и странице, нужен воздух."
    >
      <PyCode>{`print("Шапка")
print()
print("Основной текст")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Шапка\n\nОсновной текст"}</Cmd>
      <div className="s-note">
        Так делают отступы между блоками, как абзацы в письме.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Ошибки"
      sub="Забыли кавычку или скобку — Питон остановится"
      main="Ошибка — не провал, а указатель: читайте последнее сообщение, там суть."
    >
      <PyCode>{`print("Привет"`}</PyCode>
      <Cmd>{"SyntaxError: '(' was never closed (line 1)"}</Cmd>
      <div className="s-cols">
        <Node kind="amber" mono title="Строка 1" sub="Питон показывает номер строки и место запинки" />
        <Node kind="green" title="Подсказка, не приговор" sub="Прочитали → поправили → запустили снова" />
      </div>
    </Slide>
  );
}

function S13() {
  const topics: [string, string, string][] = [
    ["print", "Принт", "Печатает то, что отдали; команды идут сверху вниз"],
    ["«…»", "Строки", "Кавычки-ограда, одинаковые с обеих сторон"],
    ["#", "Комментарии", "Решётка прячет заметки для людей"],
    ["7 / 2", "Арифметика", "Числа считает, строки повторяет и склеивает"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 1 · Основы"
      main="Первая программа готова — дальше она научится запоминать."
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
        Пока каждая команда забывает всё сразу. Следующая глава — переменные:
        научим программу запоминать.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P1 = {
  "13:1": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P1).
export const SLIDE_TITLES_P1 = {
  "13:1": [
    "Первая программа",
    "Команда принт",
    "Строки и кавычки",
    "Порядок сверху вниз",
    "Комментарии",
    "Принт умеет считать",
    "Дробные числа",
    "Несколько значений",
    "Кавычка внутри текста",
    "Арифметика строк",
    "Пустой принт",
    "Ошибки",
    "Итог",
  ],
};
