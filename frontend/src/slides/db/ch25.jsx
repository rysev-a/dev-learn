// Слайды для «Базы данных», глава 25 — «Кэш: где жить, когда умирать и как не падать».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db25.jsx).

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
} from "../anim/Db25.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ПАТТЕРНЫ / ГЛАВА 25", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Зачем кэш"}
      sub={"Глава 25 · Кэш"}
      main={"Кэш работает благодаря локальности; цена — вторая копия данных."}
    >
      <V01 cues={[15.4, 35.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Уровни кэша"}
      sub={"От браузера до буферного пула"}
      main={"Ближе к пользователю — быстрее, но труднее сбросить."}
    >
      <V02 cues={[15.1, 25.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Cache-aside"}
      sub={"Кэш сбоку"}
      main={"Читаем через кэш, пишем в базу и инвалидируем."}
    >
      <V03 cues={[12.4, 24.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Схемы записи"}
      sub={"Through, back, around"}
      main={"Write-back быстр, но может потерять несброшенное."}
    >
      <V04 cues={[16.3, 28.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Что кэшировать"}
      sub={"Ключи и значения"}
      main={"Ключ — функция всех параметров; иначе утечка данных."}
    >
      <V05 cues={[19.4, 31.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Вытеснение"}
      sub={"LRU, LFU, TTL"}
      main={"LRU и TTL: размер и возраст ограничены."}
    >
      <V06 cues={[13.6, 29.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Инвалидация"}
      sub={"TTL, явная, версия"}
      main={"Версия в ключе делает инвалидацию дешёвой."}
    >
      <V07 cues={[12.4, 28.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Гонки"}
      sub={"Устаревший кэш"}
      main={"Кэш согласован с базой лишь приблизительно."}
    >
      <V08 cues={[15.5, 36.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Штурм кэша"}
      sub={"Cache stampede"}
      main={"Один пересчёт и джиттер спасают базу."}
    >
      <V09 cues={[15.6, 28.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Несуществующие ключи и лавина"}
      sub={"Penetration и avalanche"}
      main={"Кэшируйте «нет»; прогревайте и ограничивайте."}
    >
      <V10 cues={[17.0, 24.3]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Метрики"}
      sub={"Hit ratio"}
      main={"Меряйте долю попаданий; кэш бывает вреден."}
    >
      <V11 cues={[15.6, 26.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Распределённый кэш"}
      sub={"Кольцо и L1/L2"}
      main={"База — источник истины; система выживает без кэша."}
    >
      <V12 cues={[15.4, 27.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — OLTP и OLAP."}
    >
      <V13 cues={[11.7, 29.7]} />
    </Slide>
  );
}

export const SLIDES_D25 = {
  "9:25": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D25).
export const SLIDE_TITLES_D25 = {
  "9:25": [
    "Введение",
    "Уровни",
    "Cache-aside",
    "Запись",
    "Ключи",
    "Вытеснение",
    "Инвалидация",
    "Гонки",
    "Stampede",
    "Penetration",
    "Метрики",
    "Кластер",
    "Итоги",
  ],
};
