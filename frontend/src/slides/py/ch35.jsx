import { makeSlide } from "../SlideFrame.tsx";
// Слайды для «Python как первый язык», глава 35 — «Дата и время».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const PY_KW = new Set([
  "print", "for", "in", "not", "and", "or", "if", "else", "while", "is",
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

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 35", 13);

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

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Дата и время"}
      sub={"Глава 35 · Стандартная библиотека"}
      main={"Храните и считайте в UTC, в местное время переводите только при показе."}
    >
      <div className="s-grid2">
        {[["date · datetime", "Типы", "Дата, время, момент и промежуток"], ["strftime · strptime", "Формат", "В строку и из строки; ISO для хранения"], ["tzinfo", "Пояса", "Наивные и осведомлённые; zoneinfo"], ["time · calendar", "Часы и календарь", "Таймер, unix-время, високосные годы"]].map(([big, t, d]) => (
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
      title={"date, time, datetime"}
      sub={"Неизменяемые объекты, которые сравниваются и сортируются"}
      main={"weekday() считает с нуля, где ноль — понедельник; replace возвращает копию."}
    >
      <PyCode>{`from datetime import date, time, datetime

d = date(2024, 2, 29)
t = time(14, 30)
dt = datetime(2024, 2, 29, 14, 30)
print(d, t, dt)
print(d.year, d.month, d.day, d.weekday())
print(dt.replace(hour=9))
print(date(2024, 3, 1) > d)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2024-02-29 14:30:00 2024-02-29 14:30:00\n2024 2 29 3\n2024-02-29 09:30:00\nTrue"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"timedelta"}
      sub={"Промежутки: дни, часы, секунды"}
      main={"В timedelta нет месяцев и лет: их длина не постоянна, поэтому «плюс месяц» считают вручную."}
    >
      <PyCode>{`from datetime import date, timedelta

d = date(2024, 2, 28)
print(d + timedelta(days=2))
print(date(2025, 1, 1) - date(2024, 12, 25))
delta = timedelta(hours=1, minutes=30)
print(delta.total_seconds(), delta * 2)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2024-03-01\n7 days, 0:00:00\n5400.0 3:00:00"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Форматирование"}
      sub={"strftime и isoformat"}
      main={"ISO-запись сортируется как текст в порядке времени — лучший формат хранения."}
    >
      <PyCode>{`from datetime import datetime

dt = datetime(2024, 3, 5, 9, 7, 3)
print(dt.strftime("%d.%m.%Y %H:%M"))
print(dt.strftime("%Y-%m-%d"))
print(dt.isoformat())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"05.03.2024 09:07\n2024-03-05\n2024-03-05T09:07:03"}</Cmd>
      <div className="s-note">{"%Y год, %m месяц, %d день, %H часы, %M минуты, %S секунды."}</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Разбор строки"}
      sub={"strptime и fromisoformat"}
      main={"Несуществующую дату Питон не создаст: разбор — уже проверка."}
    >
      <PyCode>{`from datetime import datetime

d = datetime.strptime("05.03.2024", "%d.%m.%Y")
print(d, d.year)
print(datetime.fromisoformat("2024-03-05T09:07:03"))
try:
    datetime.strptime("30.02.2024", "%d.%m.%Y")
except ValueError as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2024-03-05 00:00:00 2024\n2024-03-05 09:07:03\nday 30 must be in range 1..29 for month 2 in year 2024"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Часовые пояса"}
      sub={"Наивные и осведомлённые даты"}
      main={"Наивное с осведомлённым сравнивать нельзя: храните UTC, переводите через astimezone."}
    >
      <PyCode>{`from datetime import datetime, timezone
from zoneinfo import ZoneInfo

utc = datetime(2024, 6, 1, 12, 0, tzinfo=timezone.utc)
msk = utc.astimezone(ZoneInfo("Europe/Moscow"))
print(utc, msk)
print(msk.utcoffset())
naive = datetime(2024, 6, 1, 12, 0)
try:
    naive < utc
except TypeError as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2024-06-01 12:00:00+00:00 2024-06-01 15:00:00+03:00\n3:00:00\ncan't compare offset-naive and offset-aware datetimes"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Модуль time"}
      sub={"perf_counter, sleep, timestamp"}
      main={"Для замеров — perf_counter: он не зависит от перевода системных часов."}
    >
      <PyCode>{`import time
from datetime import datetime, timezone

start = time.perf_counter()
time.sleep(0.01)
print(time.perf_counter() - start >= 0.01)
print(datetime(1970, 1, 2, tzinfo=timezone.utc).timestamp())
print(datetime.fromtimestamp(86400, tz=timezone.utc))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True\n86400.0\n1970-01-02 00:00:00+00:00"}</Cmd>
      <div className="s-note">{"Unix-время — секунды с 1 января 1970 по UTC."}</div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Диапазоны и сравнение"}
      sub={"min, max, рабочие дни, номер недели"}
      main={"Всё это — знакомая арифметика, сравнение и генераторы; нового только набор типов."}
    >
      <PyCode>{`from datetime import date, timedelta

start, end = date(2024, 3, 1), date(2024, 3, 10)
days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
workdays = [d for d in days if d.weekday() < 5]
print(len(days), len(workdays))
print(min(days), max(days).isocalendar()[1])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10 6\n2024-03-01 10"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"calendar и возраст"}
      sub={"Високосные годы, длина месяца"}
      main={"Возраст — не «дни / 365»: вычтите годы и поправьте, если день рождения ещё не наступил."}
    >
      <PyCode>{`import calendar
from datetime import date

weekday, days = calendar.monthrange(2024, 2)
print(calendar.isleap(2024), int(weekday), days)
print(date(2024, 2, days))

def age(born, today):
    years = today.year - born.year
    if (today.month, today.day) < (born.month, born.day):
        years -= 1
    return years

print(age(date(2000, 6, 15), date(2024, 6, 14)), age(date(2000, 6, 15), date(2024, 6, 15)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True 3 29\n2024-02-29\n23 24"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Типовые задачи"}
      sub={"До Нового года, день недели, журнал по датам"}
      main={"Дата в начале строки журнала — и группировка по дням занимает одну строку."}
    >
      <PyCode>{`from collections import Counter
from datetime import date

today = date(2024, 12, 20)
new_year = date(2025, 1, 1)
print((new_year - today).days)
names = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
print(names[date(2000, 1, 1).weekday()])
log = ["2024-03-01 error", "2024-03-01 ok", "2024-03-02 ok"]
print(Counter(line.split()[0] for line in log))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"12\nсб\nCounter({'2024-03-01': 2, '2024-03-02': 1})"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Даты и JSON"}
      sub={"Записываем строкой, читаем обратно"}
      main={"Формат хранения — часть контракта: опишите «в строку» и «из строки» в одном месте."}
    >
      <PyCode>{`import json
from datetime import datetime

event = {"name": "сдача", "at": datetime(2024, 5, 1, 10, 0)}
text = json.dumps(event, default=str, ensure_ascii=False)
print(text)
back = json.loads(text)
print(datetime.fromisoformat(back["at"]).month)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{\"name\": \"сдача\", \"at\": \"2024-05-01 10:00:00\"}\n5"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Месяц — не тридцать дней; строки дат — не даты"}
      main={"Сравнивайте объекты дат, а не строки в нестандартном формате."}
    >
      <PyCode>{`from datetime import date, timedelta

d = date(2024, 1, 31)
print(d + timedelta(days=30))
try:
    d.replace(month=2)
except ValueError as e:
    print(e)
print((date(2024, 3, 1) - date(2023, 3, 1)).days)
print(date(2024, 5, 3) < date(2024, 5, 10), "3.5.2024" < "10.5.2024")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2024-03-01\nday 31 must be in range 1..29 for month 2 in year 2024\n366\nTrue False"}</Cmd>
      <div className="s-note">{"Ещё: переходы на летнее время, устаревший utcnow() без пояса, русские названия месяцев без локали."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 35 · Стандартная библиотека"}
      main={"UTC внутри, местное время — снаружи; ISO — для хранения."}
    >
      <div className="s-grid2">
        {[["date · timedelta", "Арифметика", "Разность дат — timedelta; месяцев в ней нет"], ["strftime · fromisoformat", "Формат", "ISO для хранения, шаблон для показа"], ["ZoneInfo · astimezone", "Пояса", "Не смешивать наивные и осведомлённые"], ["perf_counter · calendar", "Часы", "Замеры; високосные годы и длина месяца"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — регулярные выражения."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P35 = {
  "13:35": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P35).
export const SLIDE_TITLES_P35 = {
  "13:35": [
    "Дата и время",
    "Типы",
    "timedelta",
    "Форматирование",
    "Разбор строки",
    "Часовые пояса",
    "Модуль time",
    "Диапазоны дат",
    "calendar и возраст",
    "Типовые задачи",
    "Даты и JSON",
    "Типичные ошибки",
    "Итог",
  ],
};
