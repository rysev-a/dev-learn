// Слайды для «Изучаем Rust», глава 50 — «WebSocket: сообщения в реальном времени».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs50.tsx).

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
} from "../anim/Rs50.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / ЧАТ: AXUM, SQLX, TOKIO / ГЛАВА 50", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Живая доставка"}
      sub={"Глава 50 · WebSocket"}
      main={"Чат оживает: сервер сам присылает сообщения клиентам по постоянному соединению."}
    >
      <V01 cues={[12.8, 25.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Протокол"}
      sub={"Upgrade и кадры"}
      main={"WebSocket начинается обычным HTTP-запросом с Upgrade и 101; дальше — кадры: текст, двоичные, ping, pong, close."}
    >
      <V02 cues={[12.1, 24.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"axum и ws"}
      sub={"Апгрейд в обработчике"}
      main={"WebSocketUpgrade — экстрактор; on_upgrade получает сокет; recv и send работают с Message."}
    >
      <V03 cues={[12.4, 24.8]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"split"}
      sub={"Чтение и запись раздельно"}
      main={"Сокет разделяют на приёмник и передатчик: одна задача читает, другая пишет; ошибка в любой завершает обе."}
    >
      <V04 cues={[11.7, 23.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Hub"}
      sub={"Реестр комнат"}
      main={"Hub: для каждой комнаты свой broadcast-канал в Arc<RwLock<HashMap>>; создаётся лениво."}
    >
      <V05 cues={[12.1, 24.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"События"}
      sub={"Протокол чата"}
      main={"Сообщения по сокету — JSON с полем type: от клиента команды, от сервера события."}
    >
      <V06 cues={[12.5, 24.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Авторизация"}
      sub={"Токен и членство"}
      main={"Токен — в параметре адреса или в первом сообщении; членство в комнате проверяется при каждой подписке."}
    >
      <V07 cues={[13.3, 26.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Рассылка"}
      sub={"broadcast"}
      main={"broadcast: каждому приёмнику — копия события; медленный получатель получает Lagged и теряет старое."}
    >
      <V08 cues={[12.4, 24.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Медленные клиенты"}
      sub={"Lagged и resync"}
      main={"При Lagged клиенту отправляют resync: он дочитывает пропущенное запросом after; безнадёжно медленных закрывают."}
    >
      <V09 cues={[12.6, 25.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Живость"}
      sub={"ping, таймаут, выход"}
      main={"Сервер шлёт ping по таймеру и закрывает молчащих; при отключении выполняется очистка и событие Leave."}
    >
      <V10 cues={[12.6, 25.3]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Согласованность"}
      sub={"База и рассылка"}
      main={"Сначала запись в базу, затем рассылка; порядок — по id; доставка «хотя бы раз», клиент дедуплицирует."}
    >
      <V11 cues={[12.1, 24.2]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Тесты"}
      sub={"Клиент на порту 0"}
      main={"Сервер на порту 0, клиент tokio-tungstenite, ожидания с таймаутом: тест стабилен и быстр."}
    >
      <V12 cues={[12.2, 24.4]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что запомнить"}
      main={"Upgrade → сокет → split; hub с broadcast по комнатам; события JSON; токен и членство; Lagged → resync; ping и очистка."}
    >
      <V13 cues={[12.7, 25.4]} />
    </Slide>
  );
}

export const SLIDES_R50 = {
  "10:50": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R50).
export const SLIDE_TITLES_R50 = {
  "10:50": [
    "Введение",
    "Протокол",
    "axum ws",
    "split",
    "Hub",
    "События",
    "Авторизация",
    "Рассылка",
    "Медленные",
    "Живость",
    "Согласованность",
    "Тесты",
    "Итоги",
  ],
};
