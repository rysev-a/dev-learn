// Слайды для «Изучаем Rust», глава 46 — «JSON, serde и единый тип ошибки».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs46.tsx).

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
} from "../anim/Rs46.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЧАТ: AXUM, SQLX, TOKIO / ГЛАВА 46", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Данные и ошибки"}
      sub={"Глава 46 · JSON и ошибки"}
      main={"API чата общается JSON-ом; нужны точные типы данных и единый предсказуемый формат ошибок."}
    >
      <V01 cues={[11.7, 23.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"serde"}
      sub={"Serialize и Deserialize"}
      main={"serde превращает структуры в формат и обратно; derive генерирует код, serde_json даёт JSON."}
    >
      <V02 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Атрибуты"}
      sub={"rename, default, skip"}
      main={"Атрибуты настраивают имена полей, значения по умолчанию, пропуск пустых и вложение структур."}
    >
      <V03 cues={[13, 26]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Перечисления"}
      sub={"enum в JSON"}
      main={"Перечисления в JSON: внешний тег, внутренний tag, untagged — выбор влияет на формат."}
    >
      <V04 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Валидация"}
      sub={"Parse, don't validate"}
      main={"Лучше превратить данные в тип, который не может быть некорректным: новые типы и TryFrom."}
    >
      <V05 cues={[12.8, 25.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Json и отказы"}
      sub={"JsonRejection"}
      main={"Json отвечает 400, 415 или 422; свой экстрактор превращает отказы в единый формат ошибок."}
    >
      <V06 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Тип ошибки"}
      sub={"AppError"}
      main={"Одно перечисление ошибок приложения: не найдено, конфликт, неверные данные, внутренняя ошибка."}
    >
      <V07 cues={[12.5, 25]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"В ответ"}
      sub={"IntoResponse"}
      main={"AppError реализует IntoResponse: код статуса и JSON-тело; внутренние детали наружу не уходят."}
    >
      <V08 cues={[12, 24]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Оператор ?"}
      sub={"From для ошибок"}
      main={"Реализации From превращают ошибки библиотек в AppError, и оператор ? делает код линейным."}
    >
      <V09 cues={[12.7, 25.5]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Формат ошибки"}
      sub={"Контракт API"}
      main={"Формат ошибки — часть контракта: код, сообщение, поля; одинаков для всех маршрутов."}
    >
      <V10 cues={[12.5, 25]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"DTO"}
      sub={"Запрос, ответ и модель"}
      main={"Структуры запросов и ответов отделяют от внутренних моделей: контракт не зависит от схемы базы."}
    >
      <V11 cues={[12.1, 24.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Эволюция API"}
      sub={"Совместимость"}
      main={"Новые поля — необязательные; удалять и переименовывать надо через алиасы и переходный период."}
    >
      <V12 cues={[13.1, 26.2]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что запомнить"}
      main={"Типы на границе, один AppError с IntoResponse, From для ошибок, один формат ответа."}
    >
      <V13 cues={[12, 23.9]} />
    </Slide>
  );
}

export const SLIDES_R46 = {
  "10:46": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R46).
export const SLIDE_TITLES_R46 = {
  "10:46": [
    "Введение",
    "serde",
    "Атрибуты",
    "enum",
    "Валидация",
    "Json-отказы",
    "AppError",
    "В ответ",
    "Оператор ?",
    "Формат",
    "DTO",
    "Совместимость",
    "Итоги",
  ],
};
