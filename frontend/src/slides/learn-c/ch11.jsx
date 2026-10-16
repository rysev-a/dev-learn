// Слайды для «От assembler к языку C», глава 11 — «Неопределённое поведение, отладка и санитайзеры».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Cl11.jsx).

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
} from "../anim/Cl11.jsx";
import { makeSlide } from "../SlideFrame.jsx";

const Slide = makeSlide("ОТ ASSEMBLER К ЯЗЫКУ C / ПРОЕКТЫ И ИНСТРУМЕНТЫ / ГЛАВА 11", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Что такое UB"}
      sub={"Глава 11 · гарантий нет"}
      main={"Неопределённое поведение — полная свобода компилятора."}
    >
      <V01 cues={[14.1, 34.8]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Основные группы"}
      sub={"Память, арифметика, прочее"}
      main={"Границы, указатели, знаковая арифметика, алиасинг."}
    >
      <V02 cues={[15.5, 27.2]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Оптимизатор и UB"}
      sub={"Рассуждение от противного"}
      main={"Проверки исчезают, ошибка видна только в -O2."}
    >
      <V03 cues={[18.6, 30.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Неинициализированные данные"}
      sub={"Остатки на стеке"}
      main={"Инициализируйте при объявлении; calloc даёт нули."}
    >
      <V04 cues={[12.9, 23.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Время жизни"}
      sub={"Висячие указатели"}
      main={"Возврат локальной, use-after-free, выход из блока."}
    >
      <V05 cues={[12.2, 23.9]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Предупреждения и анализ"}
      sub={"-Wall -Wextra -Werror"}
      main={"Статические анализаторы находят ошибки на непройденных путях."}
    >
      <V06 cues={[15.4, 23.7]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"AddressSanitizer"}
      sub={"Красные зоны"}
      main={"Границы, use-after-free, double free и утечки с отчётом."}
    >
      <V07 cues={[8.6, 23.4]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"UBSan, MSan, TSan"}
      sub={"Отдельные сборки"}
      main={"-fsanitize=undefined и -fno-sanitize-recover=all."}
    >
      <V08 cues={[20.8, 30.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"gdb"}
      sub={"Точки остановки и стек"}
      main={"-g -O0; break, next, print, backtrace, watch."}
    >
      <V09 cues={[10.9, 31.7]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"assert и тесты"}
      sub={"Инварианты и регрессии"}
      main={"Каждую найденную ошибку превращайте в тест."}
    >
      <V10 cues={[21.1, 26.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Valgrind"}
      sub={"Без пересборки"}
      main={"Запасной вариант; медленный, но точный."}
    >
      <V11 cues={[13.4, 28.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Метод поиска ошибки"}
      sub={"Сокращение, бисекция, фаззинг"}
      main={"Воспроизвести, сократить, проверить гипотезу."}
    >
      <V12 cues={[12.3, 26.1]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Дальше — хеш-таблицы, деревья и кучи."}
    >
      <V13 cues={[10.1, 18.7]} />
    </Slide>
  );
}

export const SLIDES_C11 = {
  "16:11": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_C11).
export const SLIDE_TITLES_C11 = {
  "16:11": [
    "UB",
    "Группы",
    "Оптимизатор",
    "Неинициализ.",
    "Время жизни",
    "Предупреждения",
    "ASan",
    "UBSan",
    "gdb",
    "assert",
    "Valgrind",
    "Метод",
    "Итоги",
  ],
};
