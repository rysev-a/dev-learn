// Слайды для «Базы данных», глава 17 — «Модель данных и запросы: таблицы, связи, соединения и группировки».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db17.jsx).

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
} from "../anim/Db17.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / МОДЕЛЬ И НАДЁЖНОСТЬ / ГЛАВА 17", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Зачем база данных"}
      sub={"Глава 17 · Файлы и базы"}
      main={
        "База берёт на себя одновременный доступ, сохранность, целостность и поиск."
      }
    >
      <V01 cues={[12.4, 36.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Таблица"}
      sub={"Столбцы, строки, ключ"}
      main={"Строки не упорядочены; порядок нужно потребовать в запросе."}
    >
      <V02 cues={[14.4, 30.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"SELECT"}
      sub={"Проекция и выборка"}
      main={"SQL декларативен: вы описываете результат, а не способ."}
    >
      <V03 cues={[10.4, 23.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"NULL"}
      sub={"Трёхзначная логика"}
      main={"= NULL не работает: проверяйте IS NULL; NOT IN с NULL пуст."}
    >
      <V04 cues={[8.1, 28.0]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Ограничения"}
      sub={"Ключи и проверки"}
      main={"Что можно проверить в базе — проверяйте в базе."}
    >
      <V05 cues={[14.3, 33.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Связи"}
      sub={"Один ко многим, многие ко многим"}
      main={"Многие ко многим — через связующую таблицу."}
    >
      <V06 cues={[13.1, 28.1]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"INNER JOIN"}
      sub={"Соединение таблиц"}
      main={"Соединение размножает строки: сколько пар — столько строк."}
    >
      <V07 cues={[12.3, 30.3]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"LEFT JOIN"}
      sub={"Сохранить левую таблицу"}
      main={"Условие по правой таблице в WHERE превращает LEFT в INNER."}
    >
      <V08 cues={[15.9, 24.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"GROUP BY"}
      sub={"Группы и агрегаты"}
      main={"WHERE — до группировки, HAVING — после неё."}
    >
      <V09 cues={[16.9, 32.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Ловушка размножения"}
      sub={"Несколько JOIN и SUM"}
      main={"Сворачивайте каждую ветку отдельно, потом соединяйте."}
    >
      <V10 cues={[18.0, 29.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Подзапросы и WITH"}
      sub={"Запрос внутри запроса"}
      main={"WITH делает сложный запрос читаемым сверху вниз."}
    >
      <V11 cues={[13.6, 31.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"INSERT, UPDATE, DELETE"}
      sub={"Изменение данных"}
      main={"UPDATE и DELETE без WHERE затрагивают всю таблицу."}
    >
      <V12 cues={[17.4, 24.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Порядок выполнения"}
      sub={"Итоги"}
      main={"FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT."}
    >
      <V13 cues={[23.1, 31.4]} />
    </Slide>
  );
}

export const SLIDES_D17 = {
  "9:17": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D17).
export const SLIDE_TITLES_D17 = {
  "9:17": [
    "Введение",
    "Таблица",
    "SELECT",
    "NULL",
    "Ограничения",
    "Связи",
    "JOIN",
    "LEFT JOIN",
    "GROUP BY",
    "Размножение",
    "Подзапросы",
    "Изменения",
    "Итоги",
  ],
};
