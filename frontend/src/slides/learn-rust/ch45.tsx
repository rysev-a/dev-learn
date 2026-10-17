// Слайды для «Изучаем Rust», глава 45 — «Состояние приложения и слои tower».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs45.tsx).

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
} from "../anim/Rs45.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЧАТ: AXUM, SQLX, TOKIO / ГЛАВА 45", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Общее состояние"}
      sub={"Глава 45 · Состояние и слои"}
      main={"У чата есть общее: настройки, база, список подключений. Нужны состояние и сквозная логика."}
    >
      <V01 cues={[12.1, 24.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"State"}
      sub={"with_state"}
      main={"State — типизированное общее состояние: роутеру передают значение, обработчики получают его клоном."}
    >
      <V02 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Что хранить"}
      sub={"Mutex, RwLock, атомики"}
      main={"Общие данные: атомики для счётчиков, RwLock для чтения чаще записи, Mutex для коротких критических секций."}
    >
      <V03 cues={[13.1, 26.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Каналы в состоянии"}
      sub={"broadcast и mpsc"}
      main={"В состоянии удобно хранить отправителей каналов: так обработчики общаются с фоновыми задачами."}
    >
      <V04 cues={[12, 23.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"FromRef"}
      sub={"Подсостояния"}
      main={"FromRef позволяет обработчику запросить часть состояния: только конфиг или только пул."}
    >
      <V05 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"State и Extension"}
      sub={"Статика и динамика"}
      main={"State известен при сборке, Extension добавляется на лету — например, слоем авторизации."}
    >
      <V06 cues={[12.9, 25.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Слои tower"}
      sub={"Layer и Service"}
      main={"Layer оборачивает Service в другой Service: логика до и после вызова внутренней службы."}
    >
      <V07 cues={[11.8, 23.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"from_fn"}
      sub={"Свой middleware"}
      main={"middleware::from_fn превращает async fn(req, next) в слой без ручной реализации Service."}
    >
      <V08 cues={[12.4, 24.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Порядок слоёв"}
      sub={"Кто снаружи"}
      main={"layer оборачивает всё, что добавлено до него; route_layer — только маршруты; порядок решает."}
    >
      <V09 cues={[12.7, 25.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Готовые слои"}
      sub={"tower-http"}
      main={"tower-http даёт готовые слои: трассировка, CORS, таймаут, лимит размера тела."}
    >
      <V10 cues={[12.6, 25.2]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Идентификатор запроса"}
      sub={"Трассировка"}
      main={"Слой присваивает запросу идентификатор, кладёт его в расширения и заголовок ответа."}
    >
      <V11 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Защита от перегрузки"}
      sub={"Лимиты"}
      main={"Размер тела, время ответа, число одновременных запросов и частота ограничиваются слоями."}
    >
      <V12 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что запомнить"}
      main={"State общий и типизированный; Extension — на запрос; слои оборачивают службы, порядок решает."}
    >
      <V13 cues={[11.7, 23.3]} />
    </Slide>
  );
}

export const SLIDES_R45 = {
  "10:45": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R45).
export const SLIDE_TITLES_R45 = {
  "10:45": [
    "Введение",
    "State",
    "Что хранить",
    "Каналы",
    "FromRef",
    "Extension",
    "Слои",
    "from_fn",
    "Порядок",
    "tower-http",
    "Request id",
    "Лимиты",
    "Итоги",
  ],
};
