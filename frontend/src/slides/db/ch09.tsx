// Слайды для «Базы данных», глава 9 — «Создание и изменение структуры таблиц (DDL)».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db09.tsx).

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
} from "../anim/Db09.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ИЗМЕНЕНИЕ ДАННЫХ И СТРУКТУРЫ / ГЛАВА 9", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Структура данных"}
      sub={"Глава 9 · CREATE, ALTER, DROP"}
      main={"DDL описывает структуру: CREATE создаёт, ALTER меняет, DROP удаляет."}
    >
      <V01 cues={[12.6, 25.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"CREATE TABLE"}
      sub={"Создаём таблицу"}
      main={"CREATE TABLE имя (столбец тип ограничения, …)."}
    >
      <V02 cues={[11.9, 23.8]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Типы данных"}
      sub={"Сродство в SQLite"}
      main={"В SQLite пять сродств: INTEGER, REAL, TEXT, BLOB, NUMERIC."}
    >
      <V03 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Первичный ключ"}
      sub={"PRIMARY KEY"}
      main={"PRIMARY KEY уникален и не пуст; INTEGER PRIMARY KEY нумеруется сам."}
    >
      <V04 cues={[12.8, 25.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"NOT NULL и DEFAULT"}
      sub={"Обязательность"}
      main={"NOT NULL запрещает пропуски, DEFAULT подставляет значение сам."}
    >
      <V05 cues={[12.1, 24.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"UNIQUE и CHECK"}
      sub={"Свои правила"}
      main={"UNIQUE запрещает повторы, CHECK проверяет произвольное условие."}
    >
      <V06 cues={[11.8, 23.7]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"FOREIGN KEY"}
      sub={"Связь между таблицами"}
      main={"FOREIGN KEY ссылается на ключ другой таблицы; ON DELETE задаёт реакцию."}
    >
      <V07 cues={[12.3, 24.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Составной ключ"}
      sub={"Несколько столбцов"}
      main={"PRIMARY KEY (a, b) — уникальна пара значений."}
    >
      <V08 cues={[12.3, 24.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"ALTER TABLE"}
      sub={"Меняем структуру"}
      main={"ALTER TABLE добавляет, переименовывает и удаляет столбцы."}
    >
      <V09 cues={[13.3, 26.6]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"DROP и IF EXISTS"}
      sub={"Удаление"}
      main={"DROP TABLE удаляет таблицу вместе с данными; IF EXISTS избавляет от ошибки."}
    >
      <V10 cues={[11.1, 22.2]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"CREATE TABLE AS"}
      sub={"Таблица из запроса"}
      main={"CREATE TABLE … AS SELECT создаёт таблицу из результата запроса."}
    >
      <V11 cues={[11.7, 23.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Схема как код"}
      sub={"Миграции"}
      main={"Хранение схемы в файлах и применение по порядку — миграции."}
    >
      <V12 cues={[11.5, 23]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Структура"}
      main={"Хорошая схема защищает данные: типы, ключи и ограничения."}
    >
      <V13 cues={[12.5, 25]} />
    </Slide>
  );
}

export const SLIDES_D09 = {
  "9:9": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D09).
export const SLIDE_TITLES_D09 = {
  "9:9": [
    "Введение",
    "CREATE TABLE",
    "Типы",
    "PRIMARY KEY",
    "NOT NULL",
    "UNIQUE и CHECK",
    "FOREIGN KEY",
    "Составной ключ",
    "ALTER TABLE",
    "DROP",
    "CREATE AS",
    "Миграции",
    "Итоги",
  ],
};
