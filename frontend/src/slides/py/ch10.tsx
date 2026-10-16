import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 10 — «Словари: приёмы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / СЛОВАРИ И КОРТЕЖИ / ГЛАВА 10", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Словари: приёмы"}
      sub={"Глава 10 · Словари и кортежи"}
      main={"После этой главы словари — ваш главный рабочий инструмент."}
    >
      <div className="s-grid2">
        {[["d1 | d2", "Слияние", "Настройки: умолчания и пользовательские"], ["{k: v for ...}", "Генератор", "Словарь одной записью, в том числе перевёрнутый"], ["setdefault", "Группировка", "Словарь списков — набор корзин"], ["sorted · max", "Порядок", "Сортировка пар и самый частый"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">{"Вложенные данные и список словарей — так выглядят ответы веб-сервисов."}</p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Слияние словарей"}
      sub={"Оператор | и метод update"}
      main={"Побеждает правый словарь: пользовательское перекрывает умолчание."}
    >
      <PyCode>{`defaults = {"тема": "тёмная", "шрифт": 14}
custom = {"шрифт": 18}
print(defaults | custom)
defaults.update(custom)    # то же, но на месте`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'тема': 'тёмная', 'шрифт': 18}"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Словарь из двух списков"}
      sub={"dict(zip(...))"}
      main={"Зип склеивает в пары, дикт превращает пары в словарь."}
    >
      <PyCode>{`names = ["Аня", "Борис"]
phones = ["111", "222"]
book = dict(zip(names, phones))
print(book)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'Аня': '111', 'Борис': '222'}"}</Cmd>
      <div className="s-note">{"Списки разной длины: хвост более длинного молча отбросится."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Генератор словаря"}
      sub={"Ключ: значение, потом цикл — в фигурных скобках"}
      main={"Перевернуть словарь — одна строка; значения при этом станут ключами."}
    >
      <PyCode>{`words = ["кот", "собака", "ёж"]
lens = {w: len(w) for w in words}
long = {w: n for w, n in lens.items() if n > 2}
back = {n: w for w, n in lens.items()}
print(lens, long, back)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'кот': 3, 'собака': 6, 'ёж': 2} {'кот': 3, 'собака': 6} {3: 'кот', 6: 'собака', 2: 'ёж'}"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Группировка"}
      sub={"Словарь, у которого значения — списки"}
      main={"Создать корзину, если её нет, и положить в неё элемент."}
    >
      <PyCode>{`words = ["арбуз", "банан", "абрикос"]
groups = {}
for w in words:
    if w[0] not in groups:
        groups[w[0]] = []
    groups[w[0]].append(w)
print(groups)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'а': ['арбуз', 'абрикос'], 'б': ['банан']}"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"setdefault"}
      sub={"«Создай, если нет» — одной строкой"}
      main={"Частый шаблон получает собственное имя: get с нулём для чисел, setdefault для групп."}
    >
      <PyCode>{`groups = {}
for w in ["арбуз", "банан", "абрикос"]:
    groups.setdefault(w[0], []).append(w)
print(groups)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'а': ['арбуз', 'абрикос'], 'б': ['банан']}"}</Cmd>
      <div className="s-note">{"Ключ есть — вернёт то, что под ним лежит. Нет — положит пустой список и вернёт его."}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Вложенные словари"}
      sub={"Словарь внутри словаря: два ключа подряд"}
      main={"Читается слева направо, как путь к файлу; на ненадёжных данных — get на каждом уровне."}
    >
      <PyCode>{`staff = {"Аня": {"возраст": 20, "город": "Тверь"},
         "Борис": {"возраст": 31, "город": "Омск"}}
print(staff["Аня"]["город"])
staff["Борис"]["возраст"] = 32
for name, info in staff.items():
    print(name, info["возраст"])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Тверь\nАня 20\nБорис 32"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Список словарей"}
      sub={"Самая частая форма табличных данных"}
      main={"Сортировка по полю: в key передаём функцию, достающую поле из записи."}
    >
      <PyCode>{`users = [{"name": "Аня", "age": 20}, {"name": "Боря", "age": 15}]
print([u["name"] for u in users if u["age"] > 18])

def get_age(user):
    return user["age"]

print(sorted(users, key=get_age)[0])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['Аня']\n{'name': 'Боря', 'age': 15}"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Сортировка словаря"}
      sub={"Сортируются пары, а не сам словарь"}
      main={"Ключ с наибольшим значением — одной строкой: max(d, key=d.get)."}
    >
      <PyCode>{`sales = {"чай": 5, "кофе": 9, "сок": 2}

def second(pair):
    return pair[1]

print(sorted(sales.items(), key=second, reverse=True))
print(max(sales, key=sales.get))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[('кофе', 9), ('чай', 5), ('сок', 2)]\nкофе"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Топ самых частых"}
      sub={"Разбить, посчитать, упорядочить, отобрать"}
      main={"Ни одного нового слова языка — сила в умении комбинировать приёмы."}
    >
      <PyCode>{`text = "да нет да нет да может"
counts = {}
for w in text.split():
    counts[w] = counts.get(w, 0) + 1

def second(pair):
    return pair[1]

print(sorted(counts.items(), key=second, reverse=True)[:2])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[('да', 3), ('нет', 2)]"}</Cmd>
      <div className="s-note">{"Перед подсчётом приводите слова к нижнему регистру: .lower()."}</div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Таблица соответствий"}
      sub={"Словарь вместо цепочки if / elif"}
      main={"Когда ветки сводятся к «это — то», таблицу можно хранить отдельно от логики."}
    >
      <PyCode>{`words = {5: "отлично", 4: "хорошо", 3: "удовлетворительно"}
print(words.get(5, "неизвестно"))
print(words.get(1, "неизвестно"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"отлично\nнеизвестно"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Ловушки"}
      sub={"Общий список в значениях"}
      main={"fromkeys кладёт под все ключи один и тот же объект — ссылки снова."}
    >
      <PyCode>{`shared = dict.fromkeys(["а", "б"], [])   # один список на всех
shared["а"].append(1)
print(shared)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'а': [1], 'б': [1]}"}</Cmd>
      <div className="s-note">{"Ещё: размер словаря в цикле не менять (перебирайте list(d)); правый словарь перекрывает левый; регистр и пробелы — нормализуйте."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 10 · Словари и кортежи"}
      main={"Словарь + список + цикл — это уже язык обработки данных."}
    >
      <div className="s-grid2">
        {[["d1 | d2 · dict(zip)", "Сборка", "Слияние и словарь из двух списков"], ["{k: v for ...}", "Генераторы", "Фильтр, преобразование, переворот"], ["setdefault · [[ ]]", "Группы и вложенность", "Словарь списков, словарь словарей, список словарей"], ["sorted · max", "Порядок", "Сортировка пар; max(d, key=d.get)"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Следующая глава — кортежи: неизменяемые собратья списка, которые прячутся в каждом items() и zip()."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P10 = {
  "13:10": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P10).
export const SLIDE_TITLES_P10 = {
  "13:10": [
    "Словари: приёмы",
    "Слияние словарей",
    "dict и zip",
    "Генератор словаря",
    "Группировка",
    "setdefault",
    "Вложенные словари",
    "Список словарей",
    "Сортировка словаря",
    "Топ частых слов",
    "Таблица соответствий",
    "Ловушки",
    "Итог",
  ],
};
