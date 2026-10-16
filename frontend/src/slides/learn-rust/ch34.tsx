// Слайды для «Изучаем Rust», глава 34 — «Tokio: время, таймеры и select!».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs34.tsx).

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
} from "../anim/Rs34.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / АСИНХРОННОСТЬ / ГЛАВА 34", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Ждать, не блокируя"}
      sub={"Глава 34 · Время"}
      main={"Внутри задачи — tokio::time::sleep, а не std::thread::sleep."}
    >
      <V01 cues={[14.2, 28.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"sleep и Instant"}
      sub={"Пауза и момент"}
      main={"sleep(d).await — пауза не меньше d; sleep_until(t) — до момента t."}
    >
      <V02 cues={[12.8, 25.7]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"timeout"}
      sub={"Предел ожидания"}
      main={"timeout(d, fut) даёт Ok(значение) или Err(Elapsed), а фьючер отбрасывается."}
    >
      <V03 cues={[12.9, 25.8]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"interval"}
      sub={"Периодические события"}
      main={"interval(d) — тики каждые d; первый тик срабатывает сразу."}
    >
      <V04 cues={[13, 26.1]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Пропущенные тики"}
      sub={"MissedTickBehavior"}
      main={"Burst, Delay, Skip — что делать, если работа не уложилась в период."}
    >
      <V05 cues={[12.2, 24.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Дедлайны и сброс"}
      sub={"Один срок на всё"}
      main={"Общий дедлайн через sleep_until; Sleep можно сбросить методом reset."}
    >
      <V06 cues={[11.7, 23.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Время в тестах"}
      sub={"pause и advance"}
      main={"С test-util время можно остановить и перемотать: тесты не ждут по-настоящему."}
    >
      <V07 cues={[13.2, 26.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"select!"}
      sub={"Кто первый"}
      main={"select! ждёт несколько фьючеров; побеждает первый, остальные отбрасываются."}
    >
      <V08 cues={[13.1, 26.3]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Ветки select!"}
      sub={"if, else, biased"}
      main={"Условия if отключают ветки; else — когда все ветки отключены; biased — по порядку."}
    >
      <V09 cues={[12.2, 24.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Безопасность отмены"}
      sub={"Cancel safety"}
      main={"Проигравшие фьючеры отбрасываются: операция должна быть безопасна к отмене."}
    >
      <V10 cues={[12.6, 25.3]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"select! в цикле"}
      sub={"pin и &mut"}
      main={"В цикле долгие фьючеры пинят и передают по &mut, чтобы не пересоздавать."}
    >
      <V11 cues={[12.5, 25.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Повторы и пауза"}
      sub={"Backoff"}
      main={"Повтор с таймаутом на попытку и растущей паузой между попытками."}
    >
      <V12 cues={[13.2, 26.5]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Время и select!"}
      main={"sleep, timeout, interval, select! — основа управления временем в async."}
    >
      <V13 cues={[13.3, 26.6]} />
    </Slide>
  );
}

export const SLIDES_R34 = {
  "10:34": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R34).
export const SLIDE_TITLES_R34 = {
  "10:34": [
    "Введение",
    "sleep",
    "timeout",
    "interval",
    "Пропуски",
    "Дедлайны",
    "Тесты",
    "select!",
    "Ветки",
    "Cancel safety",
    "В цикле",
    "Повторы",
    "Итоги",
  ],
};
