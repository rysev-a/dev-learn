import { makeSlide } from "../SlideFrame.tsx";
import { Arr, Node, makePyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 2 — «Переменные и типы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: слайды с примерами кода на Python и подсветкой синтаксиса.

const PY_KW = new Set([
  "print",
  "def",
  "if",
  "elif",
  "else",
  "int",
  "str",
  "float",
  "bool",
  "True",
  "False",
  "None",
  "and",
  "or",
  "not",
  "in",
  "is",
]);

const PyCode = makePyCode(PY_KW);

const Slide = makeSlide("ИЗУЧАЕМ PYTHON / ОСНОВЫ / ГЛАВА 2", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics: [string, string, string][] = [
    ["x =", "Переменные", "Подписанные коробки для значений"],
    ["=", "Присваивание", "Справа значение — слева имя коробки"],
    ["int · str", "Типы", "Целые, дробные, строки и логический вид"],
    ["f{ }", "Эф-строки", "Собираем текст из значений переменных"],
  ];
  return (
    <Slide
      n={1}
      title="Переменные и типы"
      sub="Глава 2 · Основы"
      main="Программа научится помнить: переменная — подписанная коробка для значения."
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
        В прошлой главе каждая команда принта забывала всё мгновенно. Сегодня
        программа получит память — это главный шаг от калькулятора к программе.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Присваивание"
      sub="Знак равенства читается «положить»"
      main="Сначала вычисляется правая часть, потом результат кладётся в коробку."
    >
      <PyCode>{`age = 20`}</PyCode>
      <div className="s-cols">
        <Node mono title="20" sub="Значение · то, что кладём" />
        <Arr />
        <Node kind="green" mono title="age" sub="Имя коробки · куда кладём" />
      </div>
      <div className="s-note">
        Читается не «равно», а «положить»: в коробку эйдж положить двадцать.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Использование"
      sub="Имя — ссылка на текущее содержимое"
      main="Положили новое значение — старое исчезло без следа."
    >
      <PyCode>{`age = 20
print(age)    # 20
age = 21
print(age)    # 21 — старого больше нет`}</PyCode>
      <div className="s-note">
        В коробке всегда ровно одно значение: все, кто спрашивает про эйдж,
        получают то, что лежит там сейчас.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Правила имён"
      sub="Латиница, цифры, нижнее подчёркивание"
      main="Age и age — две разные коробки, и это частый источник получасовой отладки."
    >
      <div className="s-cols">
        <Node
          kind="green"
          mono
          title="user_2"
          sub="Буквы, цифры и подчёркивание — можно"
        />
        <Node kind="amber" mono title="2user" sub="Начинать с цифры — нельзя" />
      </div>
      <PyCode>{`Age = 20
age = 21      # две разные коробки`}</PyCode>
      <div className="s-note">
        Регистр важен: Питон честно создаёт две коробки и нисколько не
        предупреждает. Прежде чем винить логику — проверьте регистр.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Стиль имён"
      sub="В мире Питона принято змеиное_имя"
      main="Код читают в десять раз чаще, чем пишут."
    >
      <div className="s-cols">
        <Node
          kind="green"
          mono
          title="user_count"
          sub="Слова в нижнем регистре через подчёркивание — имя читается как фраза"
        />
        <Node
          kind="amber"
          mono
          title="x"
          sub="Экономит три секунды при наборе — крадёт три минуты у читателя"
        />
      </div>
      <div className="s-note">
        Имена должны говорить: счётчик пользователей — это user_count, а не
        безликий x.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Числа: int и float"
      sub="Целые — для счёта, дробные — для измерений"
      main="Значения бывают разных видов, и Питон их различает."
    >
      <PyCode>{`age = 20         # int — целое
height = 1.76    # float — дробное, с точкой`}</PyCode>
      <div className="s-cols">
        <Node mono title="int" sub="Сколько пользователей, попыток, нажатий" />
        <Node mono title="float" sub="Рост, вес, температура, скорость" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Строки: str"
      sub="Текст в кавычках — и его длина"
      main="Имя пользователя и адрес почты — это строки, не числа."
    >
      <PyCode>{`name = "Аня"
len(name)            # 3
len("Привет мир")    # 10 — пробел тоже символ`}</PyCode>
      <div className="s-note">
        Функция лен возвращает число символов строки, включая пробелы.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Логический тип: bool"
      sub="Ответ на закрытый вопрос: да или нет"
      main="Всего два значения — истина и ложь, оба с заглавной буквы."
    >
      <div className="s-cols">
        <Node
          kind="green"
          mono
          title="True"
          sub="Истина · «да, возраст больше 18»"
        />
        <Node kind="amber" mono title="False" sub="Ложь · «нет, не больше»" />
      </div>
      <PyCode>{`is_adult = True`}</PyCode>
      <div className="s-note">
        Третьего значения не существует. По-настоящему бул раскрывается в главе
        об условиях, где программа начнёт выбирать.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Функция type"
      sub="Спросить вид значения у самой Питона"
      main="Полезная привычка, когда непонятно, число перед вами или строка-«число»."
    >
      <PyCode>{`type(20)      # int
type("20")    # str — похоже, но груз разный`}</PyCode>
      <div className="s-note">
        Особенно выручает, когда значение пришло со стороны: из формы, из файла,
        из ответа сервера.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Эф-строки"
      sub="Главный способ собирать текст"
      main="Перед кавычками буква f, в фигурных скобках — имена переменных."
    >
      <PyCode>{`age = 20
print(f"Мне {age} лет")    # Мне 20 лет`}</PyCode>
      <div className="s-cols">
        <Node mono title="f" sub="Флаг перед открывающей кавычкой" />
        <Arr />
        <Node mono title="{age}" sub="На место скобок подставляется значение" />
      </div>
      <div className="s-note">
        Приветствие с именем, счётчик с числом, отчёт с итогами — всё это удобно
        делать эф-строками.
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Изменение переменной"
      sub="Старое плюс один — и обратно в коробку"
      main="Так считаются лайки, шаги и попытки."
    >
      <PyCode>{`count = count + 1    # старое + 1 → обратно в коробку
count += 1           # то же самое, короче`}</PyCode>
      <div className="s-note">
        Плюс-равно читается «прибавить и положить обратно». Каждый новый клик по
        сердечку — это плюс-равно в действии.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Преобразование типов"
      sub="Переводим значение в нужный вид"
      main="Складывать можно только однородное: строка пять плюс число пять — ошибка типов."
    >
      <PyCode>{`int("42")     # 42 — строка в число
str(42)       # "42" — число в строку
"5" + 5       # TypeError: Питон не угадывает`}</PyCode>
      <div className="s-note">
        Ошибка здесь — подарок: программа падает сразу и громко, вместо того
        чтобы тихо посчитать ерунду.
      </div>
    </Slide>
  );
}

function S13() {
  const topics: [string, string, string][] = [
    ["=", "Присваивание", "Коробки-переменные, правила и стиль имён"],
    ["int · float", "Числа", "Целые — для счёта, дробные — для измерений"],
    ["str · bool", "Текст и логика", "Строки и лен, истина и ложь"],
    ["f{ }", "Эф-строки", "Подстановка значений, изменения и преобразования"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 2 · Переменные и типы"
      main="Программа научилась помнить — это главный шаг от калькулятора к программе."
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
        Программа помнит, но пока идёт по одной дороге. Следующая глава —
        условия: научим её выбирать.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P2 = {
  "13:2": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P2).
export const SLIDE_TITLES_P2 = {
  "13:2": [
    "Введение",
    "Присваивание",
    "Использование",
    "Правила имён",
    "Стиль имён",
    "Числа: int и float",
    "Строки: str",
    "Логический тип: bool",
    "Функция type",
    "Эф-строки",
    "Изменение переменной",
    "Преобразование типов",
    "Итог",
  ],
};
