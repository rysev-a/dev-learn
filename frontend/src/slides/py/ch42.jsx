// Слайды для «Python как первый язык», глава 42 — «Множественное наследование и MRO».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py42.jsx).

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
} from "../anim/Py42.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ПРОЕКТИРОВАНИЕ КЛАССОВ / ГЛАВА 42", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Несколько родителей"}
      sub={"Свобода и вопросы"}
      main={"Чей метод вызовется при совпадении имён?"}
    >
      <V01 cues={[15.9, 28.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"MRO"}
      sub={"Порядок разрешения методов"}
      main={"Первый класс списка с нужным именем побеждает."}
    >
      <V02 cues={[13.9, 26.8]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Ромб"}
      sub={"D(B, C)"}
      main={"Предок стоит после всех потомков."}
    >
      <V03 cues={[10.0, 23.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"C3-линеаризация"}
      sub={"Три правила"}
      main={"Несовместимые требования дают TypeError."}
    >
      <V04 cues={[7.8, 19.9, 26.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"super()"}
      sub={"Следующий в MRO"}
      main={"super — не родитель, а следующий в порядке."}
    >
      <V05 cues={[11.8, 19.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Кооперативный __init__"}
      sub={"**kwargs"}
      main={"Берём своё, остальное передаём дальше."}
    >
      <V06 cues={[13.7, 22.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Миксины"}
      sub={"Малые способности"}
      main={"Миксины ставят слева от основного базового."}
    >
      <V07 cues={[14.2, 31.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Композиция"}
      sub={"Является или имеет"}
      main={"Одна основная база плюс миксины."}
    >
      <V08 cues={[13.6, 22.3]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Технические ограничения"}
      sub={"Раскладка и имена"}
      main={"__x искажается в _Class__x."}
    >
      <V09 cues={[13.5, 21.8]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Отладка иерархии"}
      sub={"Печать MRO"}
      main={"Где определено имя — первый класс MRO с ним в __dict__."}
    >
      <V10 cues={[10.7, 23.4]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"ABC, Protocol, Generic"}
      sub={"Те же правила"}
      main={"Смотрите на весь MRO целиком."}
    >
      <V11 cues={[12.1, 22.5]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Чего избегать"}
      main={"Сложно ответить — упрощайте."}
    >
      <V12 cues={[12.1, 24.2]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Проектирование классов"}
      main={"MRO, super, миксины и композиция."}
    >
      <V13 cues={[13.6, 23.1, 27.4]} />
    </Slide>
  );
}

export const SLIDES_P42 = {
  "13:42": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P42).
export const SLIDE_TITLES_P42 = {
  "13:42": [
    "Несколько родителей",
    "MRO",
    "Ромб",
    "C3",
    "super",
    "__init__",
    "Миксины",
    "Композиция",
    "Ограничения",
    "Отладка",
    "ABC и Protocol",
    "Ошибки",
    "Итоги",
  ],
};
