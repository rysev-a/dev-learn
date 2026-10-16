// Слайды для «Python как первый язык», глава 37 — «Программы и среда: sys, argparse, logging, subprocess».
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

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 37</span>
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

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Программы и среда"}
      sub={"Глава 37 · Стандартная библиотека"}
      main={"Настоящая программа — утилита: параметры, журнал, коды завершения, вызов других программ."}
    >
      <div className="s-grid2">
        {[["sys · os", "Среда", "Аргументы, потоки, окружение"], ["argparse", "Аргументы", "Разбор, типы, справка"], ["logging", "Журнал", "Уровни и обработчики вместо print"], ["subprocess", "Другие программы", "Запустить и прочитать ответ"]].map(([big, t, d]) => (
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
      title={"Модуль sys"}
      sub={"Аргументы, потоки, путь поиска"}
      main={"Ошибки — в stderr, данные — в stdout: так их можно разделить при перенаправлении."}
    >
      <PyCode>{`import sys

print(sys.argv[0] != "", type(sys.argv).__name__)
print(sys.version_info >= (3, 8), sys.platform in ("linux", "darwin", "win32"))
print("ошибка", file=sys.stderr)
sys.stdout.write("в stdout\\n")
print(isinstance(sys.path, list))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True list\nTrue True\nв stdout\nTrue"}</Cmd>
      <div className="s-note">{"sys.exit(0) — успех, любое другое число — ошибка: по коду её поймёт оболочка."}</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"argparse"}
      sub={"Позиционные и необязательные аргументы"}
      main={"Одним описанием вы получаете разбор, проверку типов и справку по --help."}
    >
      <PyCode>{`import argparse

parser = argparse.ArgumentParser(description="Считалка")
parser.add_argument("name", help="имя")
parser.add_argument("--times", type=int, default=2, help="сколько раз")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args(["Аня", "--times", "3", "-v"])
print(args.name, args.times, args.verbose)
print(parser.parse_args(["Боря"]))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Аня 3 True\nNamespace(name='Боря', times=2, verbose=False)"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Приёмы argparse"}
      sub={"nargs, choices, ошибки"}
      main={"Подкоманды — отдельный парсер на каждое действие, как у git."}
    >
      <PyCode>{`import argparse

p = argparse.ArgumentParser(prog="tool")
p.add_argument("nums", nargs="+", type=int)
p.add_argument("--op", choices=["sum", "max"], default="sum")
a = p.parse_args(["3", "9", "4", "--op", "max"])
print(a.nums, a.op)
try:
    p.parse_args(["1", "--op", "avg"])
except SystemExit as e:
    print("выход с кодом", e.code)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[3, 9, 4] max\nвыход с кодом 2"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Модуль os"}
      sub={"Окружение и обход папок"}
      main={"Переменные окружения читайте через get — отсутствие настройки не должно ронять программу."}
    >
      <PyCode>{`import os

os.environ["MODE"] = "test"
print(os.environ.get("MODE"), os.environ.get("НЕТ", "—"))
print(os.getcwd() == os.path.abspath("."), (os.cpu_count() or 1) >= 1)
os.makedirs("a/b", exist_ok=True)
open("a/b/f.txt", "w").close()
for root, dirs, files in os.walk("a"):
    print(root, dirs, files)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"test —\nTrue True\na ['b'] []\na/b [] ['f.txt']"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Ввод, вывод и код возврата"}
      sub={"stdin, stderr, exit code"}
      main={"Утилита, читающая stdin и пишущая в stdout, соединяется с другими программами в конвейер."}
    >
      <PyCode>{`import io
import sys

fake = io.StringIO("10\\n20\\n30\\n")      # вместо sys.stdin
total = sum(int(line) for line in fake)
print(total)
print("это ошибка", file=sys.stderr)
print("код возврата", 0 if total else 1)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"60\nкод возврата 0"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"logging"}
      sub={"Уровни важности вместо print"}
      main={"Сообщения уровня DEBUG молчат в обычной работе — а при поиске ошибки достаточно сменить уровень."}
    >
      <PyCode>{`import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(levelname)s: %(message)s", force=True)
logging.debug("не видно")
logging.info("старт")
logging.warning("осторожно")
logging.error("сбой")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"INFO: старт\nWARNING: осторожно\nERROR: сбой"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Логгеры и обработчики"}
      sub={"getLogger(__name__), handler, formatter"}
      main={"logger.exception() внутри except пишет ошибку вместе с трассировкой; пароли в журнал не пишут."}
    >
      <PyCode>{`import logging
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(name)s | %(levelname)s | %(message)s"))
log = logging.getLogger("app.db")
log.addHandler(handler)
log.setLevel(logging.DEBUG)
log.propagate = False
log.debug("запрос")
try:
    1 / 0
except ZeroDivisionError as e:
    log.error("деление: %s", e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"app.db | DEBUG | запрос\napp.db | ERROR | деление: division by zero"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"subprocess"}
      sub={"Запустить внешнюю команду"}
      main={"Команду — списком, без shell=True; всегда с таймаутом."}
    >
      <PyCode>{`import subprocess
import sys

r = subprocess.run([sys.executable, "-c", "print('привет из процесса')"],
                   capture_output=True, text=True, check=True)
print(r.returncode, r.stdout.strip())
try:
    subprocess.run([sys.executable, "-c", "raise SystemExit(3)"], check=True)
except subprocess.CalledProcessError as e:
    print("код", e.returncode)
try:
    subprocess.run([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.2)
except subprocess.TimeoutExpired:
    print("таймаут")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 привет из процесса\nкод 3\nтаймаут"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Шаблон утилиты"}
      sub={"main() и проверка __name__"}
      main={"Код под if __name__ == \"__main__\" запускается только как программа, а не при импорте."}
    >
      <PyCode>{`import argparse
import sys

def total(nums):
    return sum(nums)

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("nums", nargs="*", type=int)
    args = p.parse_args(argv)
    if not args.nums:
        print("нет чисел", file=sys.stderr)
        return 1
    print(total(args.nums))
    return 0

if __name__ == "__main__":
    code = main(["1", "2", "3"])
    print("код", code)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"6\nкод 0"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Модули и пакеты"}
      sub={"import, __name__, venv"}
      main={"Окружение на каждый проект — и конфликты версий вас не коснутся."}
    >
      <PyCode>{`import importlib
import sys

print("antigravity" in sys.modules, "os" in sys.modules)
m = importlib.import_module("math")
print(m.__name__, m.sqrt(9))
print(__name__)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"False True\nmath 3.0\n__main__"}</Cmd>
      <div className="s-note">{"Файл __init__.py превращает папку в пакет; python -m venv .venv — изолированное окружение; pip или uv ставят пакеты."}</div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Данные и ошибки в одном потоке, молчаливый журнал"}
      main={"Код возврата — часть интерфейса: ошибка без ненулевого кода — ложь для вызывающего."}
    >
      <PyCode>{`import logging
import subprocess
import sys

print("данные")
print("ошибка", file=sys.stderr)
logging.basicConfig(stream=sys.stdout, level=logging.WARNING, format="%(message)s", force=True)
logging.info("не видно: уровень выше")
r = subprocess.run([sys.executable, "-c", "pass"], capture_output=True)
print(r.stdout, r.returncode)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"данные\nb'' 0"}</Cmd>
      <div className="s-note">{"Ещё: пароли в журнале, shell=True со строкой пользователя, подпроцесс без таймаута, logging.basicConfig в библиотеке."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 37 · Стандартная библиотека"}
      main={"Утилита — это main(), аргументы, журнал и честный код возврата."}
    >
      <div className="s-grid2">
        {[["sys.argv · sys.exit", "sys", "Аргументы, потоки, код возврата"], ["argparse", "Аргументы", "Типы, умолчания, флаги, подкоманды"], ["logging", "Журнал", "Уровни, обработчики, логгер на модуль"], ["subprocess.run", "Процессы", "Список, check, timeout, без shell"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — dataclasses, enum и typing."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P37 = {
  "13:37": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P37).
export const SLIDE_TITLES_P37 = {
  "13:37": [
    "Программы и среда",
    "Модуль sys",
    "argparse",
    "Приёмы argparse",
    "Модуль os",
    "Ввод и вывод",
    "logging",
    "Логгеры и обработчики",
    "subprocess",
    "Шаблон утилиты",
    "Модули и пакеты",
    "Типичные ошибки",
    "Итог",
  ],
};
