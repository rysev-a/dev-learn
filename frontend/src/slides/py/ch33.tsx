import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 33 — «Коллекции: collections, heapq, bisect».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 33", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Коллекции"}
      sub={"Глава 33 · Стандартная библиотека"}
      main={"Специализированные контейнеры поверх встроенных: меньше кода, меньше ошибок."}
    >
      <div className="s-grid2">
        {[["Counter", "Подсчёт", "Частоты и most_common"], ["defaultdict · deque", "Группы и очереди", "Значение по умолчанию; быстрые концы"], ["namedtuple", "Записи", "Неизменяемые, с именами полей"], ["heapq · bisect", "Порядок", "Куча и двоичный поиск"]].map(([big, t, d]) => (
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
      title={"Counter"}
      sub={"Словарь для подсчёта"}
      main={"Нет ключа — ноль, а не ошибка; most_common сразу отдаёт самые частые."}
    >
      <PyCode>{`from collections import Counter

c = Counter("абракадабра")
print(c)
print(c.most_common(2))
print(c["я"], c["а"])
print(Counter("аб") + Counter("бв"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Counter({'а': 5, 'б': 2, 'р': 2, 'к': 1, 'д': 1})\n[('а', 5), ('б', 2)]\n0 5\nCounter({'б': 2, 'а': 1, 'в': 1})"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Counter на практике"}
      sub={"Частоты, анаграммы, хватит ли букв"}
      main={"Счётчик берёт на себя цикл, словарь и проверку ключа — остаётся суть задачи."}
    >
      <PyCode>{`from collections import Counter

text = "да нет да нет да может"
print(Counter(text.split()).most_common(1))

def is_anagram(a, b):
    return Counter(a) == Counter(b)

print(is_anagram("лотос", "столо"), is_anagram("кот", "ток "))
need = Counter("кот")
have = Counter("токарь")
print(not (need - have))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[('да', 3)]\nTrue False\nTrue"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"defaultdict"}
      sub={"Фабрика значений по умолчанию"}
      main={"Даже чтение отсутствующего ключа создаёт запись; проверяйте через in или get."}
    >
      <PyCode>{`from collections import defaultdict

groups = defaultdict(list)
for w in ["арбуз", "банан", "абрикос"]:
    groups[w[0]].append(w)
print(dict(groups))
counts = defaultdict(int)
for ch in "aabbb":
    counts[ch] += 1
print(dict(counts))
d = defaultdict(list)
print("x" in d, d["x"], "x" in d)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'а': ['арбуз', 'абрикос'], 'б': ['банан']}\n{'a': 2, 'b': 3}\nFalse [] True"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"deque"}
      sub={"Двусторонняя очередь"}
      main={"Операции на обоих концах быстрые; maxlen делает очередь окном."}
    >
      <PyCode>{`from collections import deque

q = deque([1, 2, 3])
q.append(4)
q.appendleft(0)
print(q)
print(q.popleft(), q.pop(), q)
q.rotate(1)
print(q)
print(deque([1, 2, 3], maxlen=2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"deque([0, 1, 2, 3, 4])\n0 4 deque([1, 2, 3])\ndeque([3, 1, 2])\ndeque([2, 3], maxlen=2)"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"deque на практике"}
      sub={"Окно и обход в ширину"}
      main={"Нужна очередь — deque; нужен стек — достаточно списка с append и pop."}
    >
      <PyCode>{`from collections import deque

window = deque(maxlen=3)
for x in [10, 20, 30, 40, 50]:
    window.append(x)
    print(sum(window) / len(window))

graph = {"А": ["Б", "В"], "Б": ["Г"], "В": ["Г"], "Г": []}
queue, seen, order = deque(["А"]), {"А": True}, []
while queue:
    v = queue.popleft()
    order.append(v)
    for u in graph[v]:
        if u not in seen:
            seen[u] = True
            queue.append(u)
print(order)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10.0\n15.0\n20.0\n30.0\n40.0\n['А', 'Б', 'В', 'Г']"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"namedtuple"}
      sub={"Кортеж с именами полей"}
      main={"Для записей без логики — точек, цветов, строк таблицы — лучший выбор."}
    >
      <PyCode>{`from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p, p.x, p[1])
x, y = p
print(p._replace(x=10), p._asdict())
print(p == (3, 4))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Point(x=3, y=4) 3 4\nPoint(x=10, y=4) {'x': 3, 'y': 4}\nTrue"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"ChainMap и OrderedDict"}
      sub={"Слои настроек и перестановка ключей"}
      main={"ChainMap склеивает словари без копирования; запись идёт в первый слой."}
    >
      <PyCode>{`from collections import ChainMap, OrderedDict

defaults = {"тема": "светлая", "шрифт": 14}
user = {"шрифт": 18}
cfg = ChainMap(user, defaults)
print(cfg["шрифт"], cfg["тема"])
cfg["язык"] = "ru"
print(user)

od = OrderedDict(a=1, b=2, c=3)
od.move_to_end("a")
print(list(od))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"18 светлая\n{'шрифт': 18, 'язык': 'ru'}\n['b', 'c', 'a']"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"heapq: куча"}
      sub={"Наименьший элемент всегда под рукой"}
      main={"Нужен максимум — кладите числа с обратным знаком; приоритеты — кортежи (приоритет, значение)."}
    >
      <PyCode>{`import heapq

h = []
for x in [5, 1, 4, 2]:
    heapq.heappush(h, x)
print(heapq.heappop(h), heapq.heappop(h), h[0])
tasks = []
heapq.heappush(tasks, (2, "письма"))
heapq.heappush(tasks, (1, "срочное"))
print(heapq.heappop(tasks))
print(heapq.nsmallest(2, [7, 3, 9, 1]), heapq.nlargest(2, [7, 3, 9, 1]))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 2 4\n(1, 'срочное')\n[1, 3] [9, 7]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"heapq на практике"}
      sub={"Топ-k, слияние, максимум через минус"}
      main={"Куча не отсортирована целиком — гарантирован лишь минимум в начале."}
    >
      <PyCode>{`import heapq

nums = [5, 1, 9, 3, 7, 8]
top3 = []
for x in nums:
    heapq.heappush(top3, x)
    if len(top3) > 3:
        heapq.heappop(top3)
print(sorted(top3, reverse=True))
print(list(heapq.merge([1, 4, 7], [2, 5], [3, 6])))
maxheap = [-x for x in nums]
heapq.heapify(maxheap)
print(-heapq.heappop(maxheap))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[9, 8, 7]\n[1, 2, 3, 4, 5, 6, 7]\n9"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"bisect"}
      sub={"Двоичный поиск в отсортированном списке"}
      main={"Поиск за логарифмическое время — но только если данные уже отсортированы."}
    >
      <PyCode>{`import bisect

nums = [10, 20, 20, 30]
print(bisect.bisect_left(nums, 20), bisect.bisect_right(nums, 20))
bisect.insort(nums, 25)
print(nums)

def grade(score, bounds=(60, 75, 90), names="DCBA"):
    return names[bisect.bisect(bounds, score)]

print(grade(55), grade(75), grade(95))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 3\n[10, 20, 20, 25, 30]\nD B A"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Вычитание счётчиков, чтение defaultdict, «отсортированная» куча"}
      main={"Список вместо очереди, bisect по несортированному и сравнение несравнимого в куче — классика."}
    >
      <PyCode>{`from collections import Counter, defaultdict
import heapq

print(Counter("aab") - Counter("abb"))
d = defaultdict(list)
if d["нет"]:
    pass
print(len(d))
h = [5, 1, 4]
heapq.heapify(h)
print(h == sorted(h), h[0])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Counter({'a': 1})\n1\nFalse 1"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 33 · Стандартная библиотека"}
      main={"Прежде чем писать цикл, спросите: нет ли подходящего контейнера в стандартной библиотеке?"}
    >
      <div className="s-grid2">
        {[["Counter · defaultdict", "Подсчёт и группы", "Без проверок ключей"], ["deque · namedtuple", "Очередь и запись", "Быстрые концы; поля по именам"], ["heapq", "Куча", "Минимум первым; топ-k; планировщик"], ["bisect", "Двоичный поиск", "Только по отсортированным"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — числа и случайность."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P33 = {
  "13:33": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P33).
export const SLIDE_TITLES_P33 = {
  "13:33": [
    "Коллекции",
    "Counter",
    "Counter на практике",
    "defaultdict",
    "deque",
    "deque на практике",
    "namedtuple",
    "ChainMap и OrderedDict",
    "heapq: куча",
    "heapq на практике",
    "bisect",
    "Типичные ошибки",
    "Итог",
  ],
};
