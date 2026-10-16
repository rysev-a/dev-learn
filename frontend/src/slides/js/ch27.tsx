// Слайды для «Современный Frontend», глава 27 — «TypeScript, линтеры и форматирование: tsc, ESLint, Prettier».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js27.tsx).

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
} from "../anim/Js27.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / СБОРКА И ПАКЕТЫ / ГЛАВА 27", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Зачем типы"}
      sub={"Глава 27 · TypeScript"}
      main={"TypeScript ловит ошибки до запуска; типы стираются при сборке."}
    >
      <V01 cues={[14, 28.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Основы типов"}
      sub={"Примитивы, union, вывод"}
      main={"string | number | boolean, массивы, объекты, union и литералы; вывод типов избавляет от лишних аннотаций."}
    >
      <V02 cues={[12.3, 24.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Интерфейсы и типы"}
      sub={"Структурная типизация"}
      main={"Совместимость определяется структурой, а не именем: подходит всё, у чего есть нужные поля."}
    >
      <V03 cues={[13.5, 26.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Функции и дженерики"}
      sub={"Один код для многих типов"}
      main={"Generic T связывает типы входа и выхода; extends ограничивает допустимые типы."}
    >
      <V04 cues={[12.1, 24.2]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Сужение типов"}
      sub={"narrowing"}
      main={"typeof, in, instanceof и поле-дискриминант сужают union внутри ветки."}
    >
      <V05 cues={[13.7, 27.3]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Утилитные типы"}
      sub={"Partial, Pick, Omit, Record"}
      main={"Partial, Required, Pick, Omit, Record, ReturnType строят новые типы из существующих."}
    >
      <V06 cues={[12.4, 24.7]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"tsconfig"}
      sub={"Настройка проверки"}
      main={"strict включает набор строгих проверок; noEmit оставляет tsc только проверяющим."}
    >
      <V07 cues={[12.9, 25.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"tsc и сборка"}
      sub={"Стирание типов"}
      main={"esbuild/SWC просто вырезают типы; проверку делает tsc --noEmit; .d.ts описывают типы библиотек."}
    >
      <V08 cues={[12.2, 24.3]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Типы и рантайм"}
      sub={"unknown и валидация"}
      main={"Данные извне не проверены типами: используйте unknown, type guard и валидатор вроде zod."}
    >
      <V09 cues={[13, 26]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"ESLint"}
      sub={"Статический анализ"}
      main={"ESLint ищет ошибки и плохие практики по AST; правила настраиваются, многие исправляются сами."}
    >
      <V10 cues={[13, 26]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Prettier"}
      sub={"Единый формат"}
      main={"Prettier форматирует код одинаково для всех: спор о пробелах заканчивается."}
    >
      <V11 cues={[12.3, 24.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Автоматизация"}
      sub={"pre-commit и CI"}
      main={"Проверки запускаются сами: перед коммитом на изменённых файлах и целиком в CI."}
    >
      <V12 cues={[13, 26]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Типы и качество кода"}
      main={"Типы до запуска, линтер для плохих практик, форматировщик для стиля — всё автоматически."}
    >
      <V13 cues={[14.3, 28.6]} />
    </Slide>
  );
}

export const SLIDES_J27 = {
  "11:27": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J27).
export const SLIDE_TITLES_J27 = {
  "11:27": [
    "Введение",
    "Основы",
    "Интерфейсы",
    "Дженерики",
    "Сужение",
    "Утилиты",
    "tsconfig",
    "tsc и сборка",
    "Рантайм",
    "ESLint",
    "Prettier",
    "Автоматизация",
    "Итоги",
  ],
};
