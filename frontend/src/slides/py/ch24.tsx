// Слайды для «Python как первый язык», глава 24 — «Генераторы глубже: send, throw и yield from».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py24.jsx).

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
} from "../anim/Py24.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ИТЕРАТОРЫ И ГЕНЕРАТОРЫ / ГЛАВА 24", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Сопрограмма"}
      sub={"Генератор принимает и отдаёт"}
      main={"Приостанавливаемая функция с двусторонним обменом — корутина."}
    >
      <V01 cues={[11.3, 26.9]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Жизненный цикл"}
      sub={"Четыре состояния"}
      main={"Первый запрос всегда next."}
    >
      <V02 cues={[10.9, 23.3]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"send"}
      sub={"yield как выражение"}
      main={"send кладёт значение в yield и возвращает следующее."}
    >
      <V03 cues={[5.9, 21.0, 29.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Заведение корутины"}
      sub={"Первый next"}
      main={"Забыли next — первая отправка падает."}
    >
      <V04 cues={[12.9, 26.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"throw"}
      sub={"Вбросить исключение"}
      main={"Ошибку можно перехватить в точке yield и продолжить."}
    >
      <V05 cues={[18.3, 29.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"close"}
      sub={"GeneratorExit"}
      main={"Уборку пишите в finally."}
    >
      <V06 cues={[15.0, 26.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"return в генераторе"}
      sub={"StopIteration.value"}
      main={"Итог лежит в атрибуте value исключения."}
    >
      <V07 cues={[13.1, 21.3]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"yield from"}
      sub={"Прозрачное делегирование"}
      main={"Результат вложенного — значение выражения."}
    >
      <V08 cues={[19.4, 26.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Рекурсивный обход"}
      sub={"Вложенные списки"}
      main={"Строки считаем листьями."}
    >
      <V09 cues={[16.1, 22.8]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Конвейер корутин"}
      sub={"Проталкивание данных"}
      main={"Каждая стадия — генератор с бесконечным циклом."}
    >
      <V10 cues={[17.2, 25.7]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Планировщик"}
      sub={"Кооперативная многозадачность"}
      main={"Переключение — только на yield."}
    >
      <V11 cues={[15.4, 25.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Путь к async/await"}
      sub={"Преемственность"}
      main={"await — это приостановка, как yield from."}
    >
      <V12 cues={[8.9, 29.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Генераторы глубже"}
      main={"send, throw, close и yield from — основа асинхронности."}
    >
      <V13 cues={[5.6, 15.9, 25.3]} />
    </Slide>
  );
}

export const SLIDES_P24 = {
  "13:24": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P24).
export const SLIDE_TITLES_P24 = {
  "13:24": [
    "Сопрограмма",
    "Состояния",
    "send",
    "Заведение",
    "throw",
    "close",
    "return",
    "yield from",
    "Обход",
    "Конвейер",
    "Планировщик",
    "К async/await",
    "Итоги",
  ],
};
