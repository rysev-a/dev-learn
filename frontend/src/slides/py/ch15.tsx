import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, Node, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 15 — «Исключения».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ИСКЛЮЧЕНИЯ И ФАЙЛЫ / ГЛАВА 15", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Исключения"}
      sub={"Глава 15 · Исключения и файлы"}
      main={"Настоящая программа предвидит сбои и справляется с ними, а не рассыпается."}
    >
      <div className="s-grid2">
        {[["try / except", "Перехват", "Поймать ошибку и пойти дальше"], ["raise", "Поднять", "Сообщить, что условия не выполнены"], ["class E(Exception)", "Свои ошибки", "Различать ситуации предметной области"], ["finally", "Уборка", "Выполняется всегда"]].map(([big, t, d]) => (
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
      title={"Читаем трассировку"}
      sub={"Снизу вверх: тип ошибки, затем цепочка вызовов"}
      main={"Тип ошибки — подсказка: IndexError, KeyError, TypeError, ValueError, ZeroDivisionError."}
    >
      <PyCode>{`nums = [1, 2, 3]
print(nums[5])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Traceback (most recent call last):\n  File \"main.py\", line 2, in <module>\n    print(nums[5])\nIndexError: list index out of range"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"try и except"}
      sub={"Опасный код — в try, реакция — в except"}
      main={"Ловите конкретный тип ошибки: неожиданные по-прежнему должны падать громко."}
    >
      <PyCode>{`try:
    n = int("abc")
except ValueError:
    print("это не число")
print("программа жива")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"это не число\nпрограмма жива"}</Cmd>
      <div className="s-note">{"Блок try делайте коротким: только строки, которые действительно могут упасть."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Несколько except и as"}
      sub={"Сверху вниз: срабатывает первый подходящий"}
      main={"«Голый» except прячет настоящие ошибки; нужно «почти всё» — ловите Exception."}
    >
      <PyCode>{`def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    except (TypeError, ValueError) as e:
        print("ошибка:", e)
        return None

print(safe_div(6, 3), safe_div(1, 0))
print(safe_div("a", 2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2.0 None\nошибка: unsupported operand type(s) for /: 'str' and 'int'\nNone"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"else и finally"}
      sub={"else — если не было ошибки, finally — всегда"}
      main={"finally — для уборки: закрыть файл, освободить ресурс, записать итог."}
    >
      <PyCode>{`try:
    n = int("42")
except ValueError:
    print("ошибка")
else:
    print("успех", n)
finally:
    print("всегда")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"успех 42\nвсегда"}</Cmd>
      <div className="s-note">{"Порядок: try, except, else, finally."}</div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Поднимаем исключения: raise"}
      sub={"Как можно раньше и как можно точнее"}
      main={"Голый raise в except пропускает ошибку дальше вместе со всей трассировкой."}
    >
      <PyCode>{`def set_age(age):
    if age < 0:
        raise ValueError(f"возраст не может быть {age}")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"возраст не может быть -5"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Свои исключения"}
      sub={"Класс-наследник Exception"}
      main={"Общий базовый класс для ошибок библиотеки — и ловить можно как конкретную, так и всё семейство."}
    >
      <PyCode>{`class InsufficientFunds(Exception):
    pass

def withdraw(balance, x):
    if x > balance:
        raise InsufficientFunds(f"нужно ещё {x - balance}")
    return balance - x

try:
    withdraw(100, 150)
except InsufficientFunds as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"нужно ещё 50"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Иерархия исключений"}
      sub={"Предок ловит всех потомков"}
      main={"Сначала конкретные except, потом общие; KeyboardInterrupt стоит отдельно от Exception."}
    >
      <PyCode>{`print(issubclass(KeyError, LookupError), issubclass(IndexError, LookupError))
print(issubclass(ZeroDivisionError, ArithmeticError))
print(issubclass(KeyboardInterrupt, Exception))

try:
    {}["x"]
except LookupError:
    print("поймали через предка")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True\nTrue\nFalse\nпоймали через предка"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"EAFP: проще попросить прощения"}
      sub={"Проверять заранее или попробовать и поймать"}
      main={"Для файлов надёжнее открыть и поймать ошибку: пока проверяли, файл могли удалить."}
    >
      <PyCode>{`d = {"a": 1}
if "b" in d:           # проверим заранее
    print(d["b"])

try:                   # или попробуем
    print(d["b"])
except KeyError:
    print("ключа нет")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"ключа нет"}</Cmd>
      <div className="s-note">{"Ошибка редкая и тревожная — исключение; частая и обычная — get или проверка."}</div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Цепочка: raise from"}
      sub={"Превратить ошибку в понятную, не потеряв причину"}
      main={"Обработчик не должен молча проглатывать ошибку: исправить, поднять дальше или переименовать."}
    >
      <PyCode>{`def load(cfg):
    try:
        return cfg["port"]
    except KeyError as e:
        raise RuntimeError("в настройках нет порта") from e

try:
    load({})
except RuntimeError as e:
    print(e, "| причина:", repr(e.__cause__))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"в настройках нет порта | причина: KeyError('port')"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"assert и raise"}
      sub={"Ошибки программиста и ошибки данных"}
      main={"assert отключается при запуске с оптимизацией — данные пользователя им проверять нельзя."}
    >
      <PyCode>{`def mean(xs):
    assert len(xs) > 0, "список не должен быть пустым"   # ошибка программиста
    return sum(xs) / len(xs)

def parse_age(text):
    age = int(text)
    if age < 0:
        raise ValueError("возраст < 0")                  # ошибка данных
    return age

print(mean([1, 2, 3]), parse_age("20"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2.0 20"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Молчаливое проглатывание"}
      main={"Ловите только то, что умеете обработать; на остальное пусть программа падает громко."}
    >
      <PyCode>{`try:
    risky()
except:          # голый except ловит всё подряд
    pass         # и молчит — худший вариант

print("всё хорошо?")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"всё хорошо?"}</Cmd>
      <div className="s-note">{"Ещё: огромный try, raise e вместо raise, return в finally, assert вместо проверки ввода."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 15 · Исключения и файлы"}
      main={"Ловите только то, что умеете обработать."}
    >
      <div className="s-grid2">
        {[["try · except · as", "Перехват", "Конкретные типы; else и finally"], ["raise · from", "Поднять", "Раньше и точнее; цепочка причин"], ["class E(Exception)", "Свои ошибки", "Иерархия: сначала конкретные except"], ["assert", "Ошибки программиста", "Для данных — raise"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — файлы: самое частое место, где случаются такие сбои."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P15 = {
  "13:15": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P15).
export const SLIDE_TITLES_P15 = {
  "13:15": [
    "Исключения",
    "Трассировка",
    "try и except",
    "Несколько except",
    "else и finally",
    "raise",
    "Свои исключения",
    "Иерархия",
    "EAFP",
    "raise from",
    "assert и raise",
    "Типичные ошибки",
    "Итог",
  ],
};
