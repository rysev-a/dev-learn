// Слайды для «Базы данных», глава 8 — «Добавление, обновление и удаление данных (DML)».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db08.tsx).

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
} from "../anim/Db08.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("БАЗЫ ДАННЫХ / ИЗМЕНЕНИЕ ДАННЫХ И СТРУКТУРЫ / ГЛАВА 8", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Меняем данные"}
      sub={"Глава 8 · INSERT, UPDATE, DELETE"}
      main={"Три команды меняют таблицу: INSERT, UPDATE, DELETE."}
    >
      <V01 cues={[12.3, 24.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"INSERT"}
      sub={"Добавить строку"}
      main={"INSERT INTO таблица (столбцы) VALUES (значения) — одна строка."}
    >
      <V02 cues={[12.2, 24.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Много строк"}
      sub={"VALUES (…), (…)"}
      main={"Несколько строк — через запятую в одном VALUES."}
    >
      <V03 cues={[12, 24]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"INSERT … SELECT"}
      sub={"Копирование из запроса"}
      main={"INSERT … SELECT добавляет результат запроса, а не литералы."}
    >
      <V04 cues={[11.9, 23.7]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"UPDATE"}
      sub={"Изменить значения"}
      main={"UPDATE … SET столбец = значение WHERE условие."}
    >
      <V05 cues={[12.5, 25.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Без WHERE"}
      sub={"Самая частая катастрофа"}
      main={"UPDATE и DELETE без WHERE затрагивают все строки таблицы."}
    >
      <V06 cues={[11.6, 23.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"DELETE"}
      sub={"Удалить строки"}
      main={"DELETE FROM таблица WHERE условие — удалить подходящие строки."}
    >
      <V07 cues={[11.9, 23.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Сначала SELECT"}
      sub={"Проверка перед изменением"}
      main={"Прежде чем менять, выполните SELECT с тем же WHERE."}
    >
      <V08 cues={[11.8, 23.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Транзакции"}
      sub={"BEGIN, COMMIT, ROLLBACK"}
      main={"Транзакция — всё или ничего: COMMIT фиксирует, ROLLBACK отменяет."}
    >
      <V09 cues={[12.7, 25.5]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Ограничения"}
      sub={"Что не пропустит база"}
      main={"NOT NULL, UNIQUE, PRIMARY KEY и FOREIGN KEY защищают данные от ошибок."}
    >
      <V10 cues={[12.5, 25]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"UPSERT"}
      sub={"Вставить или обновить"}
      main={"ON CONFLICT DO UPDATE обновляет строку, если вставка нарушила ключ."}
    >
      <V11 cues={[13.2, 26.5]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"RETURNING"}
      sub={"Что изменилось"}
      main={"RETURNING возвращает изменённые строки прямо из INSERT, UPDATE или DELETE."}
    >
      <V12 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Осторожные изменения"}
      main={"Явные столбцы, WHERE, проверка SELECT-ом, транзакция."}
    >
      <V13 cues={[12.5, 25]} />
    </Slide>
  );
}

export const SLIDES_D08 = {
  "9:8": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D08).
export const SLIDE_TITLES_D08 = {
  "9:8": [
    "Введение",
    "INSERT",
    "Много строк",
    "INSERT SELECT",
    "UPDATE",
    "Без WHERE",
    "DELETE",
    "Проверка",
    "Транзакции",
    "Ограничения",
    "UPSERT",
    "RETURNING",
    "Итоги",
  ],
};
