import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 17 — «Пути и форматы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ИСКЛЮЧЕНИЯ И ФАЙЛЫ / ГЛАВА 17", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Пути и форматы"}
      sub={"Глава 17 · Исключения и файлы"}
      main={"Пути — объекты Path, данные — JSON, таблицы — CSV."}
    >
      <div className="s-grid2">
        {[["Path", "pathlib", "Пути как объекты: склейка, части, проверки"], ["os · shutil", "Системное", "Переменные окружения, копирование, перенос"], ["json", "JSON", "Словари и списки в текстовом виде"], ["csv", "CSV", "Таблицы: Reader, DictReader, writer"]].map(([big, t, d]) => (
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
      title={"Path: склейка и части"}
      sub={"Слэш склеивает — на любой системе"}
      main={"Результат склейки — снова путь; его можно сразу передавать в open."}
    >
      <PyCode>{`from pathlib import Path

p = Path("data") / "reports" / "2024.csv"
print(p)
print(p.name, p.stem, p.suffix, p.parent)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"data/reports/2024.csv\n2024.csv 2024 .csv data/reports"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Проверки и действия"}
      sub={"exists, mkdir, glob, iterdir"}
      main={"mkdir(parents=True, exist_ok=True) создаёт всю цепочку и не падает, если папка есть."}
    >
      <PyCode>{`from pathlib import Path

folder = Path("out/logs")
folder.mkdir(parents=True, exist_ok=True)
(folder / "a.txt").write_text("1", encoding="utf-8")
(folder / "b.txt").write_text("2", encoding="utf-8")
print(folder.exists(), folder.is_dir())
print(sorted(p.name for p in folder.glob("*.txt")))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True\n['a.txt', 'b.txt']"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Чтение и запись коротко"}
      sub={"read_text, write_text; путь рядом со скриптом"}
      main={"Path(__file__).parent — папка скрипта: пути не зависят от места запуска."}
    >
      <PyCode>{`from pathlib import Path

p = Path("note.txt")
p.write_text("привет", encoding="utf-8")
print(p.read_text(encoding="utf-8"))
print(p.stat().st_size)
# рядом со скриптом: Path(__file__).parent / "data.json"`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"привет\n12"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"os и shutil"}
      sub={"Окружение и операции над деревьями"}
      main={"rmtree не спрашивает подтверждения и не шлёт в корзину — необратимо."}
    >
      <PyCode>{`import os
import shutil
from pathlib import Path

os.environ["MODE"] = "test"
print(os.environ.get("MODE"), os.environ.get("NO_SUCH", "—"))
Path("tmp_dir").mkdir(exist_ok=True)
shutil.rmtree("tmp_dir")
print(Path("tmp_dir").exists())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"test —\nFalse"}</Cmd>
      <div className="s-note">{"Пароли и настройки передают через переменные окружения, а не в коде."}</div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"JSON"}
      sub={"dumps и loads — для строк, dump и load — для файлов"}
      main={"ensure_ascii=False сохраняет русские буквы, indent делает вывод красивым."}
    >
      <PyCode>{`import json

data = {"name": "Аня", "age": 20, "tags": ["a", "b"], "ok": True, "x": None}
text = json.dumps(data, ensure_ascii=False, indent=2)
print(text)
print(json.loads(text) == data)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{\n  \"name\": \"Аня\",\n  \"age\": 20,\n  \"tags\": [\n    \"a\",\n    \"b\"\n  ],\n  \"ok\": true,\n  \"x\": null\n}\nTrue"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Особенности JSON"}
      sub={"Ключи — строки, кортежи — списки"}
      main={"Объекты своих классов JSON не знает: дайте классу метод to_dict."}
    >
      <PyCode>{`import json

print(json.dumps({1: "a"}))
print(json.loads(json.dumps((1, 2))))

class A:
    pass

try:
    json.dumps(A())
except TypeError as e:
    print("нельзя:", e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{\"1\": \"a\"}\n[1, 2]\nнельзя: Object of type A is not JSON serializable"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"CSV"}
      sub={"csv.writer и DictReader"}
      main={"Открывайте с newline='' и кодировкой; модуль сам справляется с запятыми внутри значений."}
    >
      <PyCode>{`import csv

with open("people.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["имя", "возраст"])
    w.writerow(["Аня", 20])
    w.writerow(["Боря, мл.", 31])

with open("people.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        print(row)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'имя': 'Аня', 'возраст': '20'}\n{'имя': 'Боря, мл.', 'возраст': '31'}"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Обработка таблиц"}
      sub={"Из CSV всё приходит строками"}
      main={"Дальше работает всё знакомое: генераторы, словари, сортировка."}
    >
      <PyCode>{`import csv

with open("people.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
ages = [int(r["возраст"]) for r in rows]
print(sum(ages) / len(ages), max(ages))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"25.5 31"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Атомарная запись"}
      sub={"Сначала во временный файл, потом одним действием"}
      main={"Переименование выполняется целиком или не выполняется: сбой не оставит наполовину испорченный файл."}
    >
      <PyCode>{`import json
import os
from pathlib import Path

def save(path, data):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)       # одна неделимая операция

save("state.json", {"level": 3})
print(Path("state.json").read_text(encoding="utf-8"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{\"level\": 3}"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Другие форматы"}
      sub={"Что ещё есть в стандартной библиотеке"}
      main={"Обмен и настройки — JSON, таблицы — CSV, связанные данные — база; pickle — только своим файлам."}
    >
      <div className="s-grid2">
        {[["pickle", "Объекты целиком", "Опасно: чужой файл может выполнить код"], ["sqlite3", "База в файле", "Связанные данные и запросы"], ["configparser", "INI-настройки", "Старый формат настроек"], ["tomllib", "TOML", "Чтение современных конфигов"]].map(([big, t, d]) => (
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

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Склейка строками и скрытые превращения"}
      main={"Пути — объекты Path, данные — JSON, таблицы — CSV."}
    >
      <PyCode>{`from pathlib import Path
import json

print("data" + "/" + "x.txt")      # не переносимо
print(Path("data") / "x.txt")
print(json.dumps({"a": (1, 2)}))   # кортеж стал списком`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"data/x.txt\ndata/x.txt\n{\"a\": [1, 2]}"}</Cmd>
      <div className="s-note">{"Ещё: write_text молча перезаписывает; относительные пути; CSV без newline=''; pickle из чужих файлов."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 17 · Исключения и файлы"}
      main={"С файлами закончили. Дальше — как устроен цикл for изнутри."}
    >
      <div className="s-grid2">
        {[["Path / 'a'", "pathlib", "name, stem, suffix, parent; mkdir, glob, read_text"], ["json", "JSON", "dumps/loads и dump/load; ключи — строки"], ["csv", "CSV", "Из файла приходят строки; newline=''"], ["os.replace", "Надёжная запись", "Временный файл + переименование"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Следующая глава — итераторы."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P17 = {
  "13:17": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P17).
export const SLIDE_TITLES_P17 = {
  "13:17": [
    "Пути и форматы",
    "Path: части",
    "Проверки и действия",
    "read_text и write_text",
    "os и shutil",
    "JSON",
    "Особенности JSON",
    "CSV",
    "Обработка таблиц",
    "Атомарная запись",
    "Другие форматы",
    "Типичные ошибки",
    "Итог",
  ],
};
