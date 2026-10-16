// Слайды для «Изучаем Rust», глава 36 — «Tokio: сеть и асинхронный ввод-вывод».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs36.tsx).

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
} from "../anim/Rs36.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / АСИНХРОННОСТЬ / ГЛАВА 36", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Ввод-вывод без блокировок"}
      sub={"Глава 36 · Сеть"}
      main={"Один поток обслуживает тысячи соединений: ждущие задачи не занимают поток."}
    >
      <V01 cues={[14.2, 28.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Слушаем и подключаемся"}
      sub={"TcpListener и TcpStream"}
      main={"TcpListener::bind + accept().await; TcpStream::connect(addr).await."}
    >
      <V02 cues={[12.7, 25.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Читаем и пишем"}
      sub={"AsyncRead и AsyncWrite"}
      main={"read может вернуть меньше, чем просили; 0 — конец потока; write_all пишет всё."}
    >
      <V03 cues={[12.6, 25.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Эхо-сервер"}
      sub={"accept-цикл и spawn"}
      main={"Цикл accept + tokio::spawn на каждое соединение — основа любого сервера."}
    >
      <V04 cues={[13.1, 26.3]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Строки и буферы"}
      sub={"BufReader и lines"}
      main={"BufReader::lines() читает построчно; read_line возвращает 0 на конце."}
    >
      <V05 cues={[13.6, 27.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Обрамление"}
      sub={"Границы сообщений"}
      main={"TCP — поток байт без границ: сообщения обрамляют длиной или разделителем."}
    >
      <V06 cues={[12.2, 24.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"split"}
      sub={"Читать и писать одновременно"}
      main={"into_split разделяет сокет на читающую и пишущую половины для разных задач."}
    >
      <V07 cues={[13.5, 26.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Закрытие"}
      sub={"shutdown и EOF"}
      main={"shutdown закрывает только запись: собеседник получит EOF и ответит."}
    >
      <V08 cues={[12.3, 24.6]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"UDP"}
      sub={"Датаграммы"}
      main={"UdpSocket: send_to и recv_from; каждое сообщение — отдельная датаграмма."}
    >
      <V09 cues={[12.7, 25.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Таймауты и остановка"}
      sub={"select вокруг сети"}
      main={"Любая сетевая операция должна быть ограничена таймаутом или сигналом остановки."}
    >
      <V10 cues={[13.1, 26.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Потоки данных"}
      sub={"tokio-stream и copy"}
      main={"Stream — асинхронный итератор: next().await, map, filter, collect."}
    >
      <V11 cues={[11.9, 23.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Файлы и блокирующее"}
      sub={"fs, spawn_blocking, DNS"}
      main={"tokio::fs выполняет операции в пуле потоков; блокирующий код — в spawn_blocking."}
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
      sub={"Сеть в Tokio"}
      main={"Сервер: accept + spawn; клиент: connect; протокол: кадры; везде — таймауты."}
    >
      <V13 cues={[14.3, 28.5]} />
    </Slide>
  );
}

export const SLIDES_R36 = {
  "10:36": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R36).
export const SLIDE_TITLES_R36 = {
  "10:36": [
    "Введение",
    "bind и connect",
    "Чтение и запись",
    "Эхо-сервер",
    "Строки",
    "Фрейминг",
    "split",
    "Закрытие",
    "UDP",
    "Таймауты",
    "Потоки",
    "Файлы",
    "Итоги",
  ],
};
