// Слайды для «Базы данных», глава 4 — «Работа с текстом и пропусками (NULL)».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db04.tsx).

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
} from "../anim/Db04.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ПЕРВЫЕ ЗАПРОСЫ / ГЛАВА 4", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Что такое NULL"}
      sub={"Глава 4 · Пропуски"}
      main={"NULL — «значение неизвестно», а не ноль и не пустая строка."}
    >
      <V01 cues={[11.7, 23.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"IS NULL"}
      sub={"Проверка на пропуск"}
      main={"= NULL не работает: проверяйте IS NULL и IS NOT NULL."}
    >
      <V02 cues={[11.4, 22.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Три значения логики"}
      sub={"TRUE, FALSE, UNKNOWN"}
      main={"WHERE пропускает только истину: ложь и неизвестно отбрасываются."}
    >
      <V03 cues={[12.3, 24.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Отрицание и пропуски"}
      sub={"<> и IS NOT"}
      main={"city <> 'Москва' отбрасывает и клиентов без города."}
    >
      <V04 cues={[11.5, 23]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Арифметика с NULL"}
      sub={"Заражение"}
      main={"Любое выражение с NULL даёт NULL — арифметика и склейка."}
    >
      <V05 cues={[11.6, 23.2]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"COALESCE"}
      sub={"Первое непустое"}
      main={"COALESCE(a, b, …) возвращает первое значение, не равное NULL."}
    >
      <V06 cues={[12.5, 24.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"NULLIF"}
      sub={"Деление на ноль"}
      main={"NULLIF(a, b) возвращает NULL, если a = b — спасение от деления на ноль."}
    >
      <V07 cues={[12, 24]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"NULL равно NULL?"}
      sub={"Сравнение пропусков"}
      main={"NULL = NULL не истина; но DISTINCT и GROUP BY считают пропуски одинаковыми."}
    >
      <V08 cues={[12.3, 24.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Строки и регистр"}
      sub={"UPPER, LOWER, LENGTH, TRIM"}
      main={"UPPER, LOWER, LENGTH и TRIM — основа обработки текста."}
    >
      <V09 cues={[11.3, 22.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"SUBSTR, REPLACE, INSTR"}
      sub={"Срезы и поиск"}
      main={"SUBSTR режет по позициям, INSTR ищет, REPLACE заменяет."}
    >
      <V10 cues={[11.3, 22.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Шаблоны и GLOB"}
      sub={"Поиск в тексте"}
      main={"LIKE, GLOB и пара функций покрывают большинство задач поиска."}
    >
      <V11 cues={[12.1, 24.1]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"CAST и типы"}
      sub={"Преобразования"}
      main={"CAST переводит значение в нужный тип явно."}
    >
      <V12 cues={[12.1, 24.3]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"NULL и текст"}
      main={"Проверяйте IS NULL, помните про UNKNOWN, подставляйте COALESCE."}
    >
      <V13 cues={[12, 24]} />
    </Slide>
  );
}

export const SLIDES_D04 = {
  "9:4": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D04).
export const SLIDE_TITLES_D04 = {
  "9:4": [
    "NULL",
    "IS NULL",
    "Три значения",
    "Отрицание",
    "Арифметика",
    "COALESCE",
    "NULLIF",
    "Сравнение",
    "Регистр",
    "Срезы",
    "GLOB",
    "CAST",
    "Итоги",
  ],
};
