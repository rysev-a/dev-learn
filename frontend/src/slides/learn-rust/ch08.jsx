// Слайды для «Изучаем Rust», глава 8 — «Структуры, перечисления и Option без страха».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs08.jsx).

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
} from "../anim/Rs08.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЗНАКОМСТВО С RUST / ГЛАВА 8", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Свои типы"}
      sub={"Глава 8 · struct, enum, impl"}
      main={"struct — поля, enum — варианты, impl — методы."}
    >
      <V01 cues={[15.2, 26.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"struct"}
      sub={"Поля с именами"}
      main={"Объявление, создание по именам полей, доступ через точку."}
    >
      <V02 cues={[14.0, 24.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Изменение структуры"}
      sub={"mut, сокращения, derive"}
      main={
        "Поле меняется у mut-структуры; User { name, age }; ..old; #[derive(Debug)]."
      }
    >
      <V03 cues={[13.6, 27.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Методы"}
      sub={"impl и &self"}
      main={"Первый параметр self; &self читает."}
    >
      <V04 cues={[13.0, 25.0]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"&mut self и new"}
      sub={"Меняем и создаём"}
      main={
        "&mut self меняет, self забирает, new — конструктор по договорённости."
      }
    >
      <V05 cues={[9.6, 27.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Кортежные структуры"}
      sub={"Безымянные поля"}
      main={"struct Color(u8, u8, u8); новые типы; юнит-структуры."}
    >
      <V06 cues={[12.1, 21.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"enum"}
      sub={"Варианты"}
      main={"Значение — один из вариантов; нельзя ошибиться в имени."}
    >
      <V07 cues={[12.6, 26.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Данные в вариантах"}
      sub={"Circle и Rect"}
      main={"У каждого варианта свои данные; всё вместе — один тип."}
    >
      <V08 cues={[14.8, 23.8]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"match по enum"}
      sub={"Все варианты"}
      main={"Данные достаются в образце; новые варианты не пропустить."}
    >
      <V09 cues={[16.1, 30.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Option"}
      sub={"Some и None"}
      main={"Вместо null: значение или ничего; match, if let, unwrap_or."}
    >
      <V10 cues={[13.1, 30.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Result"}
      sub={"Ok и Err"}
      main={"Операция может не получиться; parse возвращает Result."}
    >
      <V11 cues={[15.8, 24.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"После Python"}
      sub={"Что изменилось"}
      main={"class → struct + impl; None → Option; исключения → Result."}
    >
      <V12 cues={[12.2, 22.5]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — раздел «Rust после Python»."}
    >
      <V13 cues={[11.4, 22.6]} />
    </Slide>
  );
}

export const SLIDES_R8 = {
  "10:8": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R8).
export const SLIDE_TITLES_R8 = {
  "10:8": [
    "Введение",
    "struct",
    "Изменение",
    "Методы",
    "&mut self",
    "Кортежные",
    "enum",
    "Данные",
    "match",
    "Option",
    "Result",
    "После Python",
    "Итоги",
  ],
};
