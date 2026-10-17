// Слайды для «Изучаем Rust», глава 44 — «Axum: маршруты, обработчики и экстракторы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs44.tsx).

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
} from "../anim/Rs44.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЧАТ: AXUM, SQLX, TOKIO / ГЛАВА 44", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Чат на Rust"}
      sub={"Глава 44 · Начало проекта"}
      main={"Строим чат: комнаты, пользователи, сообщения и веб-сокеты на axum, sqlx и tokio."}
    >
      <V01 cues={[11.2, 22.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Устройство axum"}
      sub={"Router и Service"}
      main={"Axum — тонкий слой над hyper и tower: роутер и обработчики превращаются в Service."}
    >
      <V02 cues={[11.8, 23.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Маршруты"}
      sub={"route, методы, параметры"}
      main={"route связывает путь и метод с обработчиком; параметры пути пишутся в фигурных скобках."}
    >
      <V03 cues={[12.7, 25.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Обработчики"}
      sub={"async fn"}
      main={"Обработчик — async fn с экстракторами в аргументах и ответом, который умеет превращаться в Response."}
    >
      <V04 cues={[12.3, 24.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Экстракторы"}
      sub={"Path, Query, Json, State"}
      main={"Экстракторы разбирают запрос: Path, Query, Json, State, HeaderMap; тело читает только последний."}
    >
      <V05 cues={[12.2, 24.3]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Path и Query"}
      sub={"Параметры запроса"}
      main={"Path и Query десериализуют параметры через serde: кортежи, структуры, Option и значения по умолчанию."}
    >
      <V06 cues={[12.5, 25]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Ответы"}
      sub={"IntoResponse"}
      main={"IntoResponse превращает строки, кортежи со статусом, Json и редиректы в Response."}
    >
      <V07 cues={[12, 24]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Статусы и заголовки"}
      sub={"HTTP как положено"}
      main={"Правильные коды: 201 с Location, 204 без тела, 404, 409, 422 и автоматические 405 и HEAD."}
    >
      <V08 cues={[12, 24]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"nest и merge"}
      sub={"Модульные роутеры"}
      main={"nest монтирует роутер под префикс, merge объединяет роутеры; fallback отвечает на неизвестное."}
    >
      <V09 cues={[13.2, 26.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Запуск сервера"}
      sub={"serve и порт 0"}
      main={"TcpListener и axum::serve запускают сервер; порт 0 выбирает свободный — удобно для тестов."}
    >
      <V10 cues={[11.8, 23.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Тест без сети"}
      sub={"oneshot"}
      main={"Роутер — Service: oneshot отправляет запрос в память, без сокетов и портов."}
    >
      <V11 cues={[12.1, 24.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Читаем сообщения компилятора"}
      main={"Handler не реализован: чаще всего не Send, лишний аргумент, State без with_state, тело не последним."}
    >
      <V12 cues={[13.6, 27.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что запомнить"}
      main={"Роутер — Service; обработчик — async fn с экстракторами; ответы — IntoResponse; тесты — oneshot."}
    >
      <V13 cues={[13.4, 26.8]} />
    </Slide>
  );
}

export const SLIDES_R44 = {
  "10:44": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R44).
export const SLIDE_TITLES_R44 = {
  "10:44": [
    "Введение",
    "Устройство",
    "Маршруты",
    "Обработчики",
    "Экстракторы",
    "Path/Query",
    "Ответы",
    "Статусы",
    "nest/merge",
    "Запуск",
    "Тесты",
    "Ошибки",
    "Итоги",
  ],
};
