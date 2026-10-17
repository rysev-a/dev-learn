// Слайды для «Изучаем Rust», глава 47 — «PostgreSQL и sqlx: данные чата».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs47.tsx).

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
} from "../anim/Rs47.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЧАТ: AXUM, SQLX, TOKIO / ГЛАВА 47", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Данные чата"}
      sub={"Глава 47 · PostgreSQL"}
      main={"Чату нужна надёжная память: пользователи, комнаты и история сообщений живут в PostgreSQL."}
    >
      <V01 cues={[12.9, 25.8]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Почему PostgreSQL"}
      sub={"Что даёт база"}
      main={"PostgreSQL даёт транзакции, ограничения целостности, индексы и параллельный доступ из многих процессов."}
    >
      <V02 cues={[13.5, 26.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"sqlx"}
      sub={"Без ORM"}
      main={"sqlx — асинхронный клиент на чистом Rust: SQL пишется вручную, типы проверяются при привязке."}
    >
      <V03 cues={[12.5, 25]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Пул"}
      sub={"PgPool"}
      main={"Пул держит несколько соединений и выдаёт их по требованию; число соединений ограничено."}
    >
      <V04 cues={[13.5, 27]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Запросы"}
      sub={"query, bind"}
      main={"query, query_as и query_scalar с параметрами через bind: никакой подстановки строк."}
    >
      <V05 cues={[13.1, 26.3]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Типы и FromRow"}
      sub={"Строки → структуры"}
      main={"FromRow собирает структуру из строки; BIGINT, TEXT, TIMESTAMPTZ, UUID и JSONB имеют типы Rust."}
    >
      <V06 cues={[13.5, 27]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"RETURNING"}
      sub={"Вставки"}
      main={"INSERT … RETURNING возвращает созданные значения; ON CONFLICT делает вставку идемпотентной."}
    >
      <V07 cues={[13, 26]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Транзакции"}
      sub={"begin и commit"}
      main={"Транзакция делает несколько изменений атомарными; если её отбросить без commit — откат."}
    >
      <V08 cues={[13, 25.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Миграции"}
      sub={"Схема под контролем"}
      main={"Миграции — пронумерованные SQL-файлы; применённые не меняют, а добавляют новые."}
    >
      <V09 cues={[12.5, 25]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Схема чата"}
      sub={"Таблицы и ключи"}
      main={"Схема чата: пользователи, комнаты, участники, сообщения; уникальность, внешние ключи, индексы."}
    >
      <V10 cues={[13.6, 27.2]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Ошибки базы"}
      sub={"Коды SQLSTATE"}
      main={"Нарушения ограничений имеют коды: 23505 — уникальность, 23503 — внешний ключ, 23514 — проверка."}
    >
      <V11 cues={[12.9, 25.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Эффективность"}
      sub={"Индексы и пакеты"}
      main={"Индекс под выборку, один запрос вместо цикла запросов, пагинация по ключу, а не по смещению."}
    >
      <V12 cues={[12.8, 25.5]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что запомнить"}
      main={"sqlx + PgPool; параметры bind; FromRow; RETURNING и ON CONFLICT; транзакции; ошибки по кодам SQLSTATE."}
    >
      <V13 cues={[12.6, 25.2]} />
    </Slide>
  );
}

export const SLIDES_R47 = {
  "10:47": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R47).
export const SLIDE_TITLES_R47 = {
  "10:47": [
    "Введение",
    "Почему",
    "sqlx",
    "Пул",
    "Запросы",
    "Типы",
    "RETURNING",
    "Транзакции",
    "Миграции",
    "Схема",
    "Ошибки",
    "Эффективность",
    "Итоги",
  ],
};
