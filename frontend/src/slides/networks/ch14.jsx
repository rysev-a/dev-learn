// Слайды для «Компьютерные сети», глава 14 — «Веб-API: REST, WebSocket, Server-Sent Events и gRPC».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt14.jsx).

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
} from "../anim/Nt14.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("ПРИКЛАДНОЙ УРОВЕНЬ / ГЛАВА 14", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Программы вызывают программы"}
      sub={"Программные интерфейсы"}
      main={
        "Клиенты HTTP — не только браузеры: приложения, службы и устройства общаются через API."
      }
    >
      <V01 cues={[9.6, 22.6, 23.6]} />
      <div className="s-note">
        Дальше — REST, WebSocket, SSE и gRPC, а в упражнениях — код на Python.
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"REST"}
      sub={"Ресурсы и методы"}
      main={
        "Ресурс — адрес, действие — метод: GET, POST, PUT, DELETE; запросы самодостаточны."
      }
    >
      <V02 cues={[11.3, 15.6, 26.9]} />
      <div className="s-note">
        Без состояния между запросами сервис масштабируется.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"JSON и коды ответа"}
      sub={"Правда в статусе"}
      main={
        "Представление — JSON; 201 с Location, 400, 404, 409, 422 — код должен отражать правду."
      }
    >
      <V03 cues={[6.9, 26.9, 27.9]} />
      <div className="s-note">
        Ошибку тоже отдают в JSON с кодом и сообщением.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Страницы, версии, повторы"}
      sub={"Повседневное"}
      main={
        "Пагинация, версия в пути и ключ идемпотентности защищают от огромных ответов, поломок и дублей."
      }
    >
      <V04 cues={[14.6, 18.0, 31.8]} />
      <div className="s-note">
        POST не идемпотентен — для него ключ особенно важен.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Токены и лимиты"}
      sub={"Кому и сколько"}
      main={
        "Bearer-токен, 401 и 403, корзина жетонов с ответом 429 и Retry-After, экспоненциальная пауза."
      }
    >
      <V05 cues={[19.8, 24.0, 37.3]} />
      <div className="s-note">
        OAuth 2.0 выдаёт доступ без пароля пользователя.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Опрос и long polling"}
      sub={"Сервер не умеет начинать"}
      main={
        "Опрос расточителен, длинный опрос лучше, но каждое событие всё равно требует нового запроса."
      }
    >
      <V06 cues={[11.4, 16.1, 27.1]} />
      <div className="s-note">Инициатор в HTTP — всегда клиент.</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"WebSocket"}
      sub={"Двусторонний канал"}
      main={
        "Upgrade, ответ 101 с хешем ключа и дальше кадры в обе стороны по одному TCP."
      }
    >
      <V07 cues={[10.4, 17.3, 26.2]} />
      <div className="s-note">
        Разрывы и переподключения — на вашей стороне.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Server-Sent Events"}
      sub={"События в одну сторону"}
      main={
        "Ответ text/event-stream не закрывается, события дописываются; браузер сам переподключается с Last-Event-ID."
      }
    >
      <V08 cues={[5.9, 17.1, 28.1]} />
      <div className="s-note">
        Работает поверх обычного HTTP и проходит через прокси.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"gRPC"}
      sub={"Вызовы между службами"}
      main={
        "Схема .proto, компактный protobuf, HTTP/2 и префикс сообщения: флаг сжатия и длина."
      }
    >
      <V09 cues={[4.3, 19.6, 27.2]} />
      <div className="s-note">
        Строгая типизация и стримы; браузеру не родной.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Как выбрать"}
      sub={"Итоги главы"}
      main={
        "REST — публичный API, SSE — события, WebSocket — живой чат, gRPC — быстрые вызовы внутри; везде таймауты и TLS."
      }
    >
      <V10 cues={[9.4, 21.7, 31.4]} />
      <div className="s-note">Дальше — эксплуатация и безопасность.</div>
    </Slide>
  );
}

export const SLIDES_NT14 = {
  "15:14": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT14).
export const SLIDE_TITLES_NT14 = {
  "15:14": [
    "Программные интерфейсы",
    "REST",
    "JSON и коды",
    "Страницы и повторы",
    "Токены и лимиты",
    "Опрос",
    "WebSocket",
    "SSE",
    "gRPC",
    "Как выбрать",
  ],
};
