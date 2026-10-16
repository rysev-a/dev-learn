// Слайды для «Современный Frontend», глава 22 — «HTTP-сервер на Node.js: маршруты, middleware и JSON API».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js22.tsx).

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
} from "../anim/Js22.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / JAVASCRIPT В NODE.JS / ГЛАВА 22", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Сервер на Node.js"}
      sub={"Глава 22 · HTTP"}
      main={"HTTP-сервер — это функция «запрос → ответ», которую Node вызывает для каждого запроса."}
    >
      <V01 cues={[13.4, 26.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"createServer"}
      sub={"Запрос и ответ"}
      main={"createServer(handler).listen(port) — обработчик получает req и res."}
    >
      <V02 cues={[12.2, 24.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Маршрутизация"}
      sub={"Метод и путь"}
      main={"Маршрут — пара (метод, шаблон пути); параметры вида :id вырезаются из пути."}
    >
      <V03 cues={[12.9, 25.7]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Тело запроса"}
      sub={"Поток чанков"}
      main={"Тело приходит кусками: собираем чанки, ограничиваем размер, затем JSON.parse."}
    >
      <V04 cues={[12.5, 24.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"JSON-ответы"}
      sub={"Коды и заголовки"}
      main={"Код состояния сообщает исход: 200, 201, 204, 400, 404, 422, 500."}
    >
      <V05 cues={[12.5, 25.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Middleware"}
      sub={"Цепочка обработчиков"}
      main={"Middleware — функция (req, res, next): сделать своё и передать дальше или завершить ответ."}
    >
      <V06 cues={[13.2, 26.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Обработка ошибок"}
      sub={"try/catch и async"}
      main={"Ошибка в обработчике должна превращаться в ответ 500, а не в падение процесса."}
    >
      <V07 cues={[12.5, 25.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Query-параметры"}
      sub={"Фильтры и страницы"}
      main={"URLSearchParams разбирает query; пагинация — page и per_page с проверкой границ."}
    >
      <V08 cues={[13.2, 26.3]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"CORS и заголовки"}
      sub={"Кто может звать"}
      main={"CORS разрешает чужим origin вызывать API; preflight OPTIONS отвечает заранее."}
    >
      <V09 cues={[13.1, 26.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Статика и потоки"}
      sub={"createReadStream"}
      main={"Файлы отдают потоком; путь нормализуют, чтобы нельзя было выйти из каталога."}
    >
      <V10 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Соединения и пределы"}
      sub={"Таймауты"}
      main={"Таймауты и лимиты защищают сервер от медленных и злых клиентов."}
    >
      <V11 cues={[13.7, 27.4]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Тесты API"}
      sub={"Порт 0 и fetch"}
      main={"Тест запускает сервер на порту 0 и обращается к нему обычным fetch."}
    >
      <V12 cues={[12.3, 24.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"HTTP на Node.js"}
      main={"Сервер = обработчик + маршрутизатор + middleware + единый формат ответов и ошибок."}
    >
      <V13 cues={[15.9, 31.8]} />
    </Slide>
  );
}

export const SLIDES_J22 = {
  "11:22": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J22).
export const SLIDE_TITLES_J22 = {
  "11:22": [
    "Введение",
    "createServer",
    "Маршруты",
    "Тело",
    "JSON",
    "Middleware",
    "Ошибки",
    "Query",
    "CORS",
    "Статика",
    "Пределы",
    "Тесты",
    "Итоги",
  ],
};
