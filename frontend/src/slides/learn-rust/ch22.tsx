// Слайды для «Изучаем Rust», глава 22 — «Модули, тесты и cargo: как устроен проект».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs22.jsx).

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
} from "../anim/Rs22.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЯЗЫК ГЛУБЖЕ / ГЛАВА 22", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Одна утилита вместо набора"}
      sub={"Глава 22 · cargo"}
      main={
        "cargo собирает, запускает, тестирует и тянет зависимости; структура у всех одинакова."
      }
    >
      <V01 cues={[15.7, 25.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Команды cargo"}
      sub={"build, check, test, release"}
      main={
        "check быстрее build; release оптимизирует, debug проверяет переполнение."
      }
    >
      <V02 cues={[13.1, 24.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Модули и пути"}
      sub={"crate, self, super, use"}
      main={"Крейт — дерево модулей; путь идёт от crate, self или super."}
    >
      <V03 cues={[10.6, 30.5]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Видимость"}
      sub={"pub, pub(crate), поля"}
      main={
        "По умолчанию закрыто; закрытые поля делают конструктор хранителем инвариантов."
      }
    >
      <V04 cues={[13.9, 27.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Реэкспорт"}
      sub={"pub use и prelude"}
      main={
        "pub use даёт короткий публичный путь и прячет внутреннюю структуру."
      }
    >
      <V05 cues={[7.0, 21.5]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Зависимости"}
      sub={"Cargo.toml, Cargo.lock, features"}
      main={"Версии совместимости, точный lock и features для лишнего кода."}
    >
      <V06 cues={[6.8, 28.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Документация"}
      sub={"/// и doc-тесты"}
      main={"Примеры в комментариях запускаются как тесты."}
    >
      <V07 cues={[11.5, 21.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Модульные тесты"}
      sub={"#[test], assert, should_panic"}
      main={"Тесты лежат рядом с кодом и видят закрытое родителя."}
    >
      <V08 cues={[13.1, 25.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Интеграционные тесты"}
      sub={"tests/ и тонкий main"}
      main={"Каждый файл в tests/ — крейт-клиент: видны только pub-элементы."}
    >
      <V09 cues={[12.8, 30.0]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Хорошие тесты"}
      sub={"Границы и мутации"}
      main={"Границы, таблица случаев и нарочно сломанная реализация."}
    >
      <V10 cues={[14.4, 26.3]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Ошибки библиотеки"}
      sub={"Error, source, non_exhaustive"}
      main={
        "Свой enum, Display, Error, From; паника только при нарушении контракта."
      }
    >
      <V11 cues={[14.4, 28.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"cfg, const и глобальное"}
      sub={"Условная компиляция"}
      main={
        "cfg и const fn считаются при сборке; глобальное — через атомики и OnceLock."
      }
    >
      <V12 cues={[11.4, 21.0]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — потоки и общее состояние."}
    >
      <V13 cues={[10.0, 18.1]} />
    </Slide>
  );
}

export const SLIDES_R22 = {
  "10:22": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R22).
export const SLIDE_TITLES_R22 = {
  "10:22": [
    "Введение",
    "cargo",
    "Модули",
    "Видимость",
    "pub use",
    "Зависимости",
    "Документация",
    "Модульные",
    "Интеграционные",
    "Хорошие тесты",
    "Ошибки",
    "cfg",
    "Итоги",
  ],
};
