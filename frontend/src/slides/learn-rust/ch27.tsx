// Слайды для «Изучаем Rust», глава 27 — «Ввод-вывод и файлы: Read, Write, BufRead, Path».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Rs27.jsx).

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
} from "../anim/Rs27.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ИЗУЧАЕМ RUST / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 27", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Read и Write"}
      sub={"Глава 27 · io"}
      main={"Один интерфейс для файла, сокета, памяти; io::Result."}
    >
      <V01 cues={[12.1, 25.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Read"}
      sub={"Источники"}
      main={"read, read_to_string, read_exact, take, chain, Cursor."}
    >
      <V02 cues={[11.7, 24.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Write"}
      sub={"Приёмники"}
      main={"write_all, flush, Vec<u8>, write!."}
    >
      <V03 cues={[11.4, 27.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Буферизация"}
      sub={"BufReader и BufWriter"}
      main={"Меньше системных вызовов; read_line, lines."}
    >
      <V04 cues={[8.9, 23.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"stdin и stdout"}
      sub={"Стандартные потоки"}
      main={"read_line, lock, быстрый вывод, flush."}
    >
      <V05 cues={[11.9, 22.4]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Файлы"}
      sub={"std::fs"}
      main={"fs::*, OpenOptions, каталоги."}
    >
      <V06 cues={[22.5, 23.5]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Пути"}
      sub={"Path и PathBuf"}
      main={"join, parent, extension; display."}
    >
      <V07 cues={[12.9, 30.6]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Ошибки"}
      sub={"io::Error"}
      main={"ErrorKind, ?, Box<dyn Error>, anyhow."}
    >
      <V08 cues={[13.1, 26.0]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Seek"}
      sub={"Произвольный доступ"}
      main={"SeekFrom, set_len, sync_all, memmap2."}
    >
      <V09 cues={[11.9, 26.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Обобщённый код"}
      sub={"R: BufRead, W: Write"}
      main={"Тест на Cursor и Vec<u8>."}
    >
      <V10 cues={[16.4, 28.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Процессы"}
      sub={"Command"}
      main={"output, spawn, pipes, коды выхода."}
    >
      <V11 cues={[10.7, 25.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Двоичные данные"}
      sub={"Порядок байтов"}
      main={"from_le_bytes, byteorder, serde."}
    >
      <V12 cues={[11.6, 26.8]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — время, числа, память."}
    >
      <V13 cues={[10.9, 26.9]} />
    </Slide>
  );
}

export const SLIDES_R27 = {
  "10:27": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R27).
export const SLIDE_TITLES_R27 = {
  "10:27": [
    "Введение",
    "Read",
    "Write",
    "Буферы",
    "stdin",
    "Файлы",
    "Пути",
    "Ошибки",
    "Seek",
    "Обобщения",
    "Процессы",
    "Двоичные",
    "Итоги",
  ],
};
