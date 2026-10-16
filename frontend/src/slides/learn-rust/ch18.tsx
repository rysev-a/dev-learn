// Слайды для «Изучаем Rust», глава 18 — «Коллекции и ошибки: Vec, String, HashMap и Result».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs18.jsx).

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
} from "../anim/Rs18.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ДАННЫЕ И АБСТРАКЦИИ / ГЛАВА 18", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Владельцы и ошибки"}
      sub={"Глава 18 · Коллекции и Result"}
      main={
        "Коллекции — владельцы буферов в куче; ошибки — значения, а не исключения."
      }
    >
      <V01 cues={[17.9, 27.2]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Vec"}
      sub={"Три слова и буфер"}
      main={"Vec — указатель, длина, ёмкость; рост вдвое; элементы подряд."}
    >
      <V02 cues={[21.9, 28.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Итераторы"}
      sub={"Ленивые конвейеры"}
      main={"iter, iter_mut, into_iter; цепочка сворачивается в один цикл."}
    >
      <V03 cues={[13.1, 29.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Строки"}
      sub={"String, &str, UTF-8"}
      main={"len — байты, chars — символы; + забирает левую строку."}
    >
      <V04 cues={[14.1, 31.0]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"HashMap"}
      sub={"Хеш-таблица"}
      main={
        "get возвращает Option<&V>; порядок обхода случаен, BTreeMap упорядочен."
      }
    >
      <V05 cues={[14.9, 25.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"entry"}
      sub={"Подсчёты в одну строку"}
      main={"entry().or_insert() — один поиск и один &mut."}
    >
      <V06 cues={[10.4, 26.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Result"}
      sub={"Ok или Err"}
      main={"Ошибка видна в сигнатуре и не теряется молча."}
    >
      <V07 cues={[13.6, 28.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Оператор ?"}
      sub={"Пробросить вверх"}
      main={"? — ранний возврат Err с преобразованием через From."}
    >
      <V08 cues={[14.9, 33.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Свои ошибки"}
      sub={"enum, Display, Box<dyn Error>"}
      main={
        "enum для причин, Display для людей, Box<dyn Error> для общего случая."
      }
    >
      <V09 cues={[13.9, 28.8]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Паника"}
      sub={"Размотка стека"}
      main={
        "panic разматывает стек и вызывает drop; код 101; catch_unwind — граница."
      }
    >
      <V10 cues={[18.9, 32.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Комбинаторы"}
      sub={"map, and_then, collect"}
      main={
        "map, map_err, and_then; collect в Result<Vec> останавливается на первой ошибке."
      }
    >
      <V11 cues={[12.9, 27.5]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Какую коллекцию выбрать"}
      sub={"Vec, HashMap, BTreeMap"}
      main={"Vec по умолчанию; последовательная память любима кэшем."}
    >
      <V12 cues={[13.1, 24.7]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Данные в куче, ошибки — значения; дальше трейты и обобщения."}
    >
      <V13 cues={[15.2, 27.3]} />
    </Slide>
  );
}

export const SLIDES_R18 = {
  "10:18": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R18).
export const SLIDE_TITLES_R18 = {
  "10:18": [
    "Введение",
    "Vec",
    "Итераторы",
    "Строки",
    "HashMap",
    "entry",
    "Result",
    "?",
    "Ошибки",
    "Паника",
    "Комбинаторы",
    "Выбор",
    "Итоги",
  ],
};
