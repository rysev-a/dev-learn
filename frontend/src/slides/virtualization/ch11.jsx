// Слайды для «Виртуализации», глава 11 — «Планирование ресурсов».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm11.jsx).

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
} from "../anim/Vm11.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ГИПЕРВИЗОРЫ И ЭКСПЛУАТАЦИЯ / ГЛАВА 11</span>
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
      title={"Ядер меньше, чем vCPU"}
      sub={"Глава 11 · Планирование ресурсов"}
      main={"Кто-то неизбежно ждёт — важно организовать ожидание."}
    >
      <V01 cues={[8.0, 16.6, 20.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Переподписка CPU"}
      sub={"4:1, 2:1, 1:1"}
      main={"Чем выше переподписка, тем выше плотность и ожидание."}
    >
      <V02 cues={[4.9, 22.9, 23.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Steal time"}
      sub={"Украденное время"}
      main={"Стабильно высокий st — перегруженный хост."}
    >
      <V03 cues={[6.4, 18.3, 30.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Группы управления"}
      sub={"Вес, квота, набор ядер"}
      main={"Вес делит при конкуренции, квота ограничивает всегда."}
    >
      <V04 cues={[12.5, 24.0, 26.7]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Закрепление vCPU"}
      sub={"Pinning, изоляция, SMT"}
      main={"Предсказуемо, но теряется гибкость."}
    >
      <V05 cues={[8.2, 20.1, 30.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"NUMA"}
      sub={"Свой и чужой узел"}
      main={"Процессоры и память машины — на одном узле."}
    >
      <V06 cues={[9.4, 17.6, 18.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Виртуальная NUMA"}
      sub={"Большие машины"}
      main={"Гостю показывают узлы, критичное закрепляют явно."}
    >
      <V07 cues={[4.2, 15.4, 27.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Всё в одном узле"}
      sub={"vCPU, память, устройства, потоки"}
      main={"Цепочка должна сойтись целиком."}
    >
      <V08 cues={[13.2, 14.2, 22.5]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Задержка"}
      sub={"Halt polling и питание"}
      main={"Опрос ускоряет пробуждение за счёт процессора."}
    >
      <V09 cues={[13.5, 18.9, 32.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Итог главы"}
      sub={"Общие и критичные нагрузки"}
      main={"Следите за steal, очередью и NUMA-промахами."}
    >
      <V10 cues={[9.3, 14.0, 20.7]} />
    </Slide>
  );
}

export const SLIDES_VM11 = {
  "17:11": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM11).
export const SLIDE_TITLES_VM11 = {
  "17:11": [
    "Ожидание",
    "Переподписка",
    "Steal",
    "cgroups",
    "Pinning",
    "NUMA",
    "vNUMA",
    "Выравнивание",
    "Задержка",
    "Итог",
  ],
};
