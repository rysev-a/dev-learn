// Слайды для «От assembler к языку C», глава 8 — «Ввод и вывод: stdio, форматирование и буферизация».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Cl08.jsx).

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
} from "../anim/Cl08.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ОТ ASSEMBLER К ЯЗЫКУ C / ВВОД-ВЫВОД И ДАННЫЕ / ГЛАВА 8", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Потоки FILE *"}
      sub={"Глава 8 · stdio"}
      main={
        "stdin, stdout, stderr готовы при запуске; остальное открываете вы."
      }
    >
      <V01 cues={[12.5, 25.7]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"printf"}
      sub={"Спецификаторы"}
      main={"Флаги, ширина, точность; возврат — число символов."}
    >
      <V02 cues={[9.1, 31.0]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Типы и форматы"}
      sub={"%ld, %zu, inttypes.h"}
      main={"Формат должен точно соответствовать типу аргумента."}
    >
      <V03 cues={[17.9, 29.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"snprintf"}
      sub={"Печать в строку"}
      main={"Всегда с размером; возврат — нужная длина."}
    >
      <V04 cues={[16.9, 27.7]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"sscanf"}
      sub={"Форматированный ввод"}
      main={"Проверяйте число разобранных полей и задавайте ширину."}
    >
      <V05 cues={[17.3, 35.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"fgets"}
      sub={"Строки из потока"}
      main={"Перевод строки остаётся в буфере; fgetc возвращает int."}
    >
      <V06 cues={[15.2, 23.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"strtol и strtod"}
      sub={"Числа из текста"}
      main={"endptr и errno; atoi ошибок не сообщает."}
    >
      <V07 cues={[10.7, 30.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"fopen и fclose"}
      sub={"Файлы"}
      main={"Проверка NULL; feof — только после неудачного чтения."}
    >
      <V08 cues={[11.1, 21.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"fread и fwrite"}
      sub={"Двоичные данные"}
      main={"Не пишите структуры целиком; fseek, ftell, rewind."}
    >
      <V09 cues={[13.3, 24.2]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Буферизация"}
      sub={"Три режима"}
      main={"fflush и setvbuf; аварийный выход теряет буфер."}
    >
      <V10 cues={[13.9, 25.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Потоки в памяти"}
      sub={"fmemopen, open_memstream"}
      main={"Ввод-вывод становится проверяемым."}
    >
      <V11 cues={[14.6, 25.6]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"stdarg"}
      sub={"va_list и vsnprintf"}
      main={"Обёртки над printf и проверка форматов."}
    >
      <V12 cues={[17.8, 27.3]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — порядок байтов, IEEE 754 и битовые приёмы."}
    >
      <V13 cues={[13.2, 27.5]} />
    </Slide>
  );
}

export const SLIDES_C8 = {
  "16:8": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_C8).
export const SLIDE_TITLES_C8 = {
  "16:8": [
    "Потоки",
    "printf",
    "Типы",
    "snprintf",
    "sscanf",
    "fgets",
    "strtol",
    "fopen",
    "fread",
    "Буфер",
    "В памяти",
    "stdarg",
    "Итоги",
  ],
};
