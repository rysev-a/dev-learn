// Слайды для «Виртуализации», глава 2 — «Trap-and-emulate и проблема x86».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm02.jsx).

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
} from "../anim/Vm02.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ОСНОВЫ ВИРТУАЛИЗАЦИИ / ГЛАВА 2</span>
      <span>{String(n).padStart(2, "0")} / 10</span>
    </div>
  );
}

function Slide({ n, title, sub, main, children }) {
  return (
    <div className="slide">
      <Rubric n={n} />
      <h3 className="s-title">{title}</h3>
      {sub && <p className="s-sub">{sub}</p>}
      <div className="s-divider" />
      <div className="s-body">{children}</div>
      {main && (
        <div className="s-main">
          <span className="s-main-label">ГЛАВНОЕ</span>
          <span className="s-main-text">{main}</span>
        </div>
      )}
    </div>
  );
}

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Простая схема и её провал"}
      sub={"Глава 2 · Ловушки и обходные пути"}
      main={"Перехватить и сымитировать — просто, но x86 это сломал."}
    >
      <V01 cues={[8.5, 16.4, 30.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Перехватить и сымитировать"}
      sub={"Гость в непривилегированном режиме"}
      main={"Привилегированная команда гостя — ловушка, монитор её имитирует."}
    >
      <V02 cues={[12.2, 19.4, 31.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Сжатие колец"}
      sub={"Монитор в кольце 0, ядро гостя в кольце 1"}
      main={"Нарушителя ловит аппаратура, монитору проверять команды не нужно."}
    >
      <V03 cues={[13.9, 23.2, 33.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Виртуальный процессор"}
      sub={"Состояние, которое гость считает своим"}
      main={"Настоящий флаг прерываний не трогают: меняется только виртуальный."}
    >
      <V04 cues={[10.3, 24.7, 33.7]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Семнадцать «дыр» x86"}
      sub={"Чувствительные, но не привилегированные"}
      main={"POPF молча игнорируется, PUSHF выдаёт настоящий флаг."}
    >
      <V05 cues={[11.6, 17.0, 29.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Двоичная трансляция"}
      sub={"VMware, конец девяностых"}
      main={"Опасные команды ядра заменяются безопасными, результат — в кэше."}
    >
      <V06 cues={[6.1, 20.3, 32.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Паравиртуализация"}
      sub={"Xen, 2003 год"}
      main={"Гость знает о гипервизоре и вызывает его гипервызовами."}
    >
      <V07 cues={[11.9, 21.1, 28.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Сравнение подходов"}
      sub={"Правки гостя, скорость, сложность"}
      main={"Трансляция — без правок, паравиртуализация — быстрее всех."}
    >
      <V08 cues={[6.7, 26.0, 32.2]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Паравиртуализация сегодня"}
      sub={"kvmclock, virtio, vmcall"}
      main={"Приём остался: гость сам договаривается с гипервизором."}
    >
      <V09 cues={[6.9, 23.6, 34.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Цена ловушки"}
      sub={"Главное число виртуализации"}
      main={"Ловушка стоит порядка тысячи тактов — их нужно меньше."}
    >
      <V10 cues={[7.7, 18.3, 26.9]} />
    </Slide>
  );
}

export const SLIDES_VM2 = {
  "17:2": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM2).
export const SLIDE_TITLES_VM2 = {
  "17:2": [
    "План",
    "Trap-and-emulate",
    "Кольца",
    "Виртуальный IF",
    "Проблема x86",
    "Трансляция",
    "Паравиртуализация",
    "Сравнение",
    "Сегодня",
    "Цена ловушки",
  ],
};
