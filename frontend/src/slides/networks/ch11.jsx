// Слайды для «Компьютерные сети», глава 11 — «HTTP/1.1: запросы, заголовки, коды ответов, кэш и cookie».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt11.jsx).

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
} from "../anim/Nt11.jsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ПРИКЛАДНОЙ УРОВЕНЬ / ГЛАВА 11", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"HTTP над TCP"}
      sub={"После адреса и соединения"}
      main={
        "Сначала сеть, имя и TCP-соединение, и только потом HTTP: запросы и ответы."
      }
    >
      <V01 cues={[6.8, 17.1, 24.9]} />
      <div className="s-note">
        На HTTP построены сайты, API и многое другое.
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"URL и модель"}
      sub={"Запрос — ответ"}
      main={
        "URL = схема, хост, порт, путь и параметры; клиент спрашивает, сервер отвечает и ничего не помнит."
      }
    >
      <V02 cues={[6.6, 15.0, 25.2]} />
      <div className="s-note">Протокол без состояния.</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Формат запроса"}
      sub={"Текст, а не двоичные данные"}
      main={
        "Стартовая строка, заголовки, пустая строка и необязательное тело; Host выбирает сайт на общем IP."
      }
    >
      <V03 cues={[6.9, 16.7, 22.8]} />
      <div className="s-note">Каждая строка заканчивается CRLF.</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Методы"}
      sub={"Что сделать с ресурсом"}
      main={
        "GET и HEAD безопасны, PUT и DELETE идемпотентны, POST — нет: повторять его вслепую нельзя."
      }
    >
      <V04 cues={[7.7, 18.6, 24.3]} />
      <div className="s-note">
        PATCH меняет частично, OPTIONS спрашивает разрешённое.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Коды ответа"}
      sub={"Четыре класса"}
      main={
        "2xx успех, 3xx перенаправление, 4xx ошибка клиента, 5xx ошибка сервера."
      }
    >
      <V05 cues={[7.4, 20.1, 31.9]} />
      <div className="s-note">
        304 Not Modified — основа кэширования по ETag.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Заголовки"}
      sub={"Служебные сведения"}
      main={
        "Content-Type, Content-Length, Accept, Location: незнакомые заголовки просто игнорируют."
      }
    >
      <V06 cues={[7.2, 16.9, 26.5]} />
      <div className="s-note">
        Так протокол расширяют без изменения самого протокола.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Соединения"}
      sub={"Постоянные и очередь"}
      main={
        "HTTP/1.1 держит соединение открытым, но ответы идут по очереди — отсюда шесть соединений браузера."
      }
    >
      <V07 cues={[10.1, 17.6, 27.5]} />
      <div className="s-note">
        Блокировка начала очереди снимает следующая версия.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Кэш"}
      sub={"Главный ускоритель веба"}
      main={
        "Cache-Control и ETag позволяют не качать повторно: max-age и ответ 304 без тела."
      }
    >
      <V08 cues={[12.8, 13.8, 27.1]} />
      <div className="s-note">Персональные страницы кэшировать нельзя.</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Cookie"}
      sub={"Состояние поверх протокола без состояния"}
      main={
        "Set-Cookie выдаёт идентификатор сессии, браузер возвращает Cookie; защищают HttpOnly, Secure, SameSite."
      }
    >
      <V09 cues={[5.6, 17.2, 23.1]} />
      <div className="s-note">
        Данные сессии хранятся на сервере, в cookie — только идентификатор.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Итоги главы"}
      sub={"Что унести дальше"}
      main={
        "Запрос, ответ, коды, кэш и cookie — основа веба; ограничение очереди снимают HTTP/2 и HTTP/3."
      }
    >
      <V10 cues={[5.9, 18.7, 25.4]} />
      <div className="s-note">Дальше — HTTP/2 и HTTP/3.</div>
    </Slide>
  );
}

export const SLIDES_NT11 = {
  "15:11": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT11).
export const SLIDE_TITLES_NT11 = {
  "15:11": [
    "HTTP над TCP",
    "URL и модель",
    "Формат запроса",
    "Методы",
    "Коды ответа",
    "Заголовки",
    "Соединения",
    "Кэш",
    "Cookie",
    "Итоги",
  ],
};
