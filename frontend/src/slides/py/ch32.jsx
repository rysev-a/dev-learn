// Слайды для «Python как первый язык», глава 32 — «Код как данные: ast, eval, exec и dis».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py32.jsx).

import {
  V01,
  V02,
  V03,
  V04,
  V05,
  V06,
  V07,
  V08,
  V09,
  V10,
  V11,
  V12,
  V13,
} from "../anim/Py32.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / МЕТАПРОГРАММИРОВАНИЕ / ГЛАВА 32", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"От текста к исполнению"}
      sub={"Дерево и байт-код"}
      main={"Каждый этап можно прочитать и даже изменить."}
    >
      <V01 cues={[16.5, 25.2]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"eval, exec, literal_eval"}
      sub={"Строки с кодом"}
      main={"Чужие строки не выполняют никогда."}
    >
      <V02 cues={[10.7, 31.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"compile"}
      sub={"Объект кода"}
      main={"Объект кода выполняют много раз без повторного разбора."}
    >
      <V03 cues={[11.7, 23.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"ast.parse"}
      sub={"Дерево разбора"}
      main={"ast.dump показывает структуру любого выражения."}
    >
      <V04 cues={[12.1, 29.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Обход дерева"}
      sub={"walk и NodeVisitor"}
      main={"Линтеры ищут шаблоны, не запуская программу."}
    >
      <V05 cues={[12.9, 25.3]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Преобразование"}
      sub={"NodeTransformer"}
      main={"Метод возвращает новый узел; unparse вернёт текст."}
    >
      <V06 cues={[12.4, 28.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Безопасный калькулятор"}
      sub={"Белый список узлов"}
      main={"Опора на грамматику надёжнее фильтра строк."}
    >
      <V07 cues={[12.4, 26.5]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Объект кода и функция"}
      sub={"__code__"}
      main={"Функция — оболочка вокруг объекта кода."}
    >
      <V08 cues={[9.0, 21.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Модуль dis"}
      sub={"Стековая машина"}
      main={"Набор команд меняется от версии к версии."}
    >
      <V09 cues={[12.3, 28.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Что видно в байт-коде"}
      sub={"Оптимизации"}
      main={"Байт-код объясняет производительность."}
    >
      <V10 cues={[15.7, 31.2]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Применения"}
      sub={"Тесты и генераторы"}
      main={"pytest и dataclass тоже работают с кодом."}
    >
      <V11 cues={[10.2, 24.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Безопасность"}
      sub={"Правила"}
      main={"Строите дерево, а не склеиваете строки."}
    >
      <V12 cues={[15.7, 25.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Метапрограммирование"}
      main={"Код — данные: читаем, меняем, объясняем."}
    >
      <V13 cues={[11.7, 22.6, 33.4]} />
    </Slide>
  );
}

export const SLIDES_P32 = {
  "13:32": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P32).
export const SLIDE_TITLES_P32 = {
  "13:32": [
    "Этапы",
    "eval и exec",
    "compile",
    "parse",
    "Обход",
    "Преобразование",
    "Калькулятор",
    "__code__",
    "dis",
    "Оптимизации",
    "Применения",
    "Правила",
    "Итоги",
  ],
};
