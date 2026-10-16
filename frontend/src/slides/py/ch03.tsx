import { makeSlide } from "../SlideFrame.tsx";
import { Arr, Cmd, Node, makePyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 3 — «Условия».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const PY_KW = new Set([
  "if", "elif", "else", "and", "or", "not", "in",
  "print", "pass", "input", "int", "str", "def", "return",
]);

const PyCode = makePyCode(PY_KW, true);

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ОСНОВЫ / ГЛАВА 3", 13);

const Down = () => <span className="s-arr">↓</span>;

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics: [string, string, string][] = [
    ["if / else", "Развилка", "Программа сама выбирает дорогу"],
    ["==", "Сравнения", "Два знака равенства — вопрос, один — присваивание"],
    ["and or not", "Связки", "Знакомые слова из логики высказываний"],
    ["elif", "Цепочки", "От частного к общему, сверху вниз"],
  ];
  return (
    <Slide
      n={1}
      title="Условия"
      sub="Глава 3 · Основы"
      main="Из логики «если, то» — в исполняемый код: программа начнёт принимать решения."
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
        Проверка пароля, скидка по возрасту, тревога при перегрузе —
        настоящие программы постоянно принимают решения.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Если и отступы"
      sub="Условие, двоеточие и блок в четыре пробела"
      main="Отступ в Питоне — не красота, а синтаксис: он показывает, что относится к условию."
    >
      <PyCode>{`if password == secret:
    print("доступ открыт")

print("работаем дальше")`}</PyCode>
      <div className="s-cols">
        <Node kind="green" mono title="с отступом" sub="Сработает, только если условие истинно" />
        <Node kind="amber" mono title="без отступа" sub="Идёт всегда, независимо от проверки" />
      </div>
    </Slide>
  );
}

function S03() {
  const rows: [string, string][] = [
    ["age == 18", "равны ли — вопрос"],
    ["age != 18", "не равно"],
    ["age > 18 · age < 18", "больше, меньше"],
    ["age >= 18 · age <= 18", "с приставкой «либо равно»"],
  ];
  return (
    <Slide
      n={3}
      title="Сравнения"
      sub="Результат сравнения — истина или ложь"
      main="Один знак равенства — команда, два знака — вопрос."
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
        <span className="s-path">age = 18</span> — присваивание, положить значение
        в переменную; <span className="s-path">age == 18</span> — сравнение.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Иначе: else"
      sub="Что делать, когда условие ложно"
      main="Выполнится ровно одна из двух дорог — на эту гарантию можно опираться."
    >
      <PyCode>{`if password == secret:
    print("доступ открыт")
else:
    print("неверный пароль")`}</PyCode>
      <div className="s-cols">
        <Node kind="green" mono title="истинно →" sub="Верхний блок: пускаем в систему" />
        <Node kind="amber" mono title="ложно →" sub="Нижний блок: ошибка и подсказка" />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Иначе если: elif"
      sub="Цепочка проверок сверху вниз"
      main="Сработает первая совпавшая проверка — остальные даже не рассматриваются."
    >
      <PyCode>{`if age < 12:
    price = 0
elif age < 18:
    price = 50
else:
    price = 100`}</PyCode>
      <div className="s-note">
        Порядок условий — логика программы: от частного к общему. Общий случай
        первым — до частных очередь никогда не дойдёт.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="И, или, не"
      sub="Три связки из логики высказываний"
      main="«И» — оба, «или» — хотя бы одно, «не» — переворот: законы де Моргана теперь в коде."
    >
      <PyCode>{`if has_ticket and age >= 18:
    print("проходите")

if not is_closed or is_vip:
    print("мы работаем")`}</PyCode>
      <div className="s-cols">
        <Node mono title="and" sub="Истинно, когда истинны обе части" />
        <Node mono title="or" sub="Истинно, когда истинно хотя бы одно" />
        <Node mono title="not" sub="Переворачивает значение" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Цепочки сравнений"
      sub="Как в школьной математике"
      main="0 ≤ x ≤ 100 записывается одной строкой — и читается лучше парных проверок."
    >
      <PyCode>{`if 0 <= x <= 100:
    print("процент в границах")

# то же самое, но длиннее:
if 0 <= x and x <= 100:
    print("процент в границах")`}</PyCode>
      <div className="s-note">
        Так проверяют возраст в допустимых границах, загрузку сервера, оценку
        по шкале от одного до пяти.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Вложенные условия"
      sub="Если внутри если"
      main="Матрёшка в три этажа — сигнал упростить: чаще всё помещается в цепочку или в «и»."
    >
      <PyCode>{`if is_logged_in:
    if is_admin:
        print("панель управления")`}</PyCode>
      <div className="s-cols">
        <Node kind="amber" mono title="3 этажа" sub="Трудно следить, где какой блок кончается" />
        <Arr />
        <Node kind="green" mono title="1 этаж" sub="Цепочка elif или одно условие с and" />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Сравнение строк"
      sub="Символ за символом, регистр важен"
      main="«да» и «Да» — разные строки; оператор in проверяет вхождение."
    >
      <PyCode>{`if answer == "да":        # «Да» — уже другая строка
    print("принято")

if "ошибка" in message:   # есть ли слово внутри фразы
    print("проверьте лог")`}</PyCode>
      <div className="s-note">
        Ввод пользователей перед сравнением приводят к одному регистру: иначе
        «да», «Да» и «ДА» — три разных ответа.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Флаги и состояние"
      sub="Результат сравнения можно сохранить"
      main="Флаг-выключатель: сравнили один раз — передали и проверили позже."
    >
      <PyCode>{`adult = age >= 18

if adult:
    print("добро пожаловать")`}</PyCode>
      <div className="s-cols">
        <Node mono title="adult" sub="Истина или ложь — без всякого if" />
        <Arr />
        <Node kind="green" title="Состояние программы" sub="Вошёл ли пользователь, оплачен ли заказ, отправлена ли форма" />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Типичные ошибки"
      sub="Узнайте их в лицо"
      main="Число и строка никогда не равны: «18» и 18 выглядят одинаково, но это разные типы."
    >
      <div className="s-grid2">
        <Node kind="amber" mono title="age = 18" sub="Один знак — присваивание вместо вопроса" />
        <Node kind="amber" mono title="потерян отступ" sub="Блок закончился раньше, чем вы думали" />
        <Node kind="amber" mono title={'"18" == 18'} sub="Число и строка не равны никогда" />
        <Node kind="green" mono title="int(input())" sub="Строку — в число заранее, потом сравнивайте" />
      </div>
      <div className="s-note">
        Питон не угадывает намерения: проверяйте типы, отступы и знаки равенства.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Читаем чужой код"
      sub="Цепочка, которая ставит оценку"
      main="Проговорите каждую ветку вслух — чтение условий вслух ловит половину багов."
    >
      <PyCode>{`if score >= 90:
    print("отлично")
elif score >= 70:
    print("хорошо")
else:
    print("надо повторить")`}</PyCode>
      <div className="s-note">
        До elif доходят только те, кто не набрал 90, — уточнять «и меньше 90»
        не нужно: границу гарантирует позиция в цепочке.
      </div>
    </Slide>
  );
}

function S13() {
  const topics: [string, string, string][] = [
    ["if / elif / else", "Выбор", "Развилка с гарантией: ровно одна дорога"],
    ["==", "Сравнения", "Два знака равенства — вопрос, один — присваивание"],
    ["and or not", "Связки", "Наследники логики высказываний и де Моргана"],
    ["0 <= x <= 100", "Цепочки", "Границы одной строкой; отступ — синтаксис"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 3 · Условия"
      main="Программа выбрала дорогу — в следующей главе научим её повторять."
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
        Следующая глава — циклы: научим программу повторять действия
        без копипасты.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P3 = {
  "13:3": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P3).
export const SLIDE_TITLES_P3 = {
  "13:3": [
    "Введение: развилки",
    "Если и отступы",
    "Сравнения",
    "Иначе",
    "Иначе если",
    "И, или, не",
    "Цепочки сравнений",
    "Вложенные условия",
    "Сравнение строк",
    "Флаги и состояние",
    "Типичные ошибки",
    "Читаем чужой код",
    "Итог",
  ],
};
