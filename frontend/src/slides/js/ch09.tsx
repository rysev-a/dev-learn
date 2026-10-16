// Слайды для «Современный Frontend», глава 9 — «Модули и ошибки: ES-модули, CommonJS, исключения».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js09.jsx).

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
} from "../anim/Js09.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / ЯЗЫК JAVASCRIPT / ГЛАВА 9", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Модули и исключения"}
      sub={"Глава 9 · Деление кода и честные сбои"}
      main={"Модули делят код на части, исключения честно сообщают о сбоях."}
    >
      <V01 cues={[9.9, 28.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"ES-модули"}
      sub={"export и import"}
      main={"Модуль выполняется один раз, у него своя область видимости."}
    >
      <V02 cues={[13.0, 27.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Живые привязки"}
      sub={"import() по требованию"}
      main={
        "Импорт — не копия, а живая привязка; import() грузит код по требованию."
      }
    >
      <V03 cues={[15.9, 34.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"CommonJS"}
      sub={"require и module.exports"}
      main={"require синхронный и возвращает копию ссылки."}
    >
      <V04 cues={[12.9, 27.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Циклы и «бочки»"}
      sub={"Зависимости по кругу"}
      main={"Общее выносят в третий модуль; явные импорты точнее «бочек»."}
    >
      <V05 cues={[14.6, 27.2]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Как находят модуль"}
      sub={"Пути, node_modules, import map"}
      main={"Голые имена в браузере сопоставляет карта импортов."}
    >
      <V06 cues={[10.1, 32.1]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"throw, try, finally"}
      sub={"Исключения и стек"}
      main={"finally выполняется всегда — там освобождают ресурсы."}
    >
      <V07 cues={[10.6, 25.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Хорошие ошибки"}
      sub={"Классы, cause, AggregateError"}
      main={"cause сохраняет первопричину."}
    >
      <V08 cues={[11.9, 32.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Результат вместо исключения"}
      sub={"Ожидаемые исходы"}
      main={
        "Ожидаемое возвращают значением, исключениями сообщают об исключительном."
      }
    >
      <V09 cues={[16.4, 30.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Повторы и таймауты"}
      sub={"Exponential backoff"}
      main={"Повторяйте только идемпотентные операции и с паузой."}
    >
      <V10 cues={[20.3, 28.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Необработанные ошибки"}
      sub={"Глобальные обработчики"}
      main={"Последний рубеж — отчёт и корректное завершение."}
    >
      <V11 cues={[12.1, 25.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Отладка ошибок"}
      sub={"Стек и контекст"}
      main={"Не глотайте исключения и не бросайте строки."}
    >
      <V12 cues={[13.9, 28.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — промисы и async/await."}
    >
      <V13 cues={[12.9, 29.0]} />
    </Slide>
  );
}

export const SLIDES_J9 = {
  "11:9": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J9).
export const SLIDE_TITLES_J9 = {
  "11:9": [
    "Введение",
    "ESM",
    "Привязки",
    "CommonJS",
    "Циклы",
    "Разрешение",
    "Исключения",
    "Классы ошибок",
    "Результат",
    "Повторы",
    "Глобальные",
    "Отладка",
    "Итоги",
  ],
};
