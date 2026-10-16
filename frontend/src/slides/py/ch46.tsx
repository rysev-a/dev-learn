// Слайды для «Python как первый язык», глава 46 — «Асинхронные итераторы, генераторы и менеджеры контекста».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py46.jsx).

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
} from "../anim/Py46.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / АСИНХРОННОСТЬ / ГЛАВА 46", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Поток значений"}
      sub={"Ожидание в итерации"}
      main={"async for отдаёт управление на время ожидания."}
    >
      <V01 cues={[11.4, 28.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Протокол"}
      sub={"__aiter__ и __anext__"}
      main={"StopAsyncIteration — конец потока."}
    >
      <V02 cues={[13.3, 29.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Асинхронный генератор"}
      sub={"async def + yield"}
      main={"return со значением в нём запрещён."}
    >
      <V03 cues={[10.9, 25.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Постраничная загрузка"}
      sub={"Типичный пример"}
      main={"Лень плюс неблокирующее ожидание."}
    >
      <V04 cues={[12.1, 27.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Асинхронные включения"}
      sub={"async for в скобках"}
      main={"Удобно в тестах, но память целиком."}
    >
      <V05 cues={[14.0, 22.0]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"async with"}
      sub={"__aenter__ и __aexit__"}
      main={"Открытие и закрытие могут ждать."}
    >
      <V06 cues={[13.2, 22.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"@asynccontextmanager"}
      sub={"И AsyncExitStack"}
      main={"try/finally гарантирует уборку."}
    >
      <V07 cues={[19.1, 29.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Уборка за генератором"}
      sub={"aclose и aclosing"}
      main={"break не закрывает генератор — закрывайте сами."}
    >
      <V08 cues={[13.1, 27.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"asend и athrow"}
      sub={"Двунаправленность"}
      main={"Та же механика, что у обычных генераторов."}
    >
      <V09 cues={[14.6, 21.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Конвейеры"}
      sub={"Стадии и очереди"}
      main={"Потребитель задаёт темп — давление назад."}
    >
      <V10 cues={[11.5, 22.8]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Отмена и таймауты"}
      sub={"CancelledError"}
      main={"Отмену подавлять нельзя."}
    >
      <V11 cues={[14.9, 22.0]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Тестирование"}
      sub={"IsolatedAsyncioTestCase"}
      main={"sleep(0) — достаточно, чтобы передать управление."}
    >
      <V12 cues={[16.5, 21.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Ошибки и итоги"}
      sub={"Асинхронные потоки"}
      main={"aclosing, конвейеры и отмена."}
    >
      <V13 cues={[15.1, 25.6]} />
    </Slide>
  );
}

export const SLIDES_P46 = {
  "13:46": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P46).
export const SLIDE_TITLES_P46 = {
  "13:46": [
    "Потоки",
    "Протокол",
    "Генератор",
    "Страницы",
    "Включения",
    "async with",
    "asynccontextmanager",
    "aclosing",
    "asend",
    "Конвейеры",
    "Отмена",
    "Тесты",
    "Итоги",
  ],
};
