// Слайды для «Виртуализации», глава 12 — «Контейнеры против виртуальных машин».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm12.jsx).

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
} from "../anim/Vm12.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>КОНТЕЙНЕРЫ, ОБЛАКО И БЕЗОПАСНОСТЬ / ГЛАВА 12</span>
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
      title={"Два стека"}
      sub={"Глава 12 · Контейнеры и ВМ"}
      main={"У машины своё ядро, у контейнеров общее — отсюда все различия."}
    >
      <V01 cues={[8.4, 18.3, 26.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Пространства имён"}
      sub={"pid, mnt, net, uts, user"}
      main={"Контейнер — набор пространств имён для группы процессов."}
    >
      <V02 cues={[5.9, 22.1, 31.1]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Группы управления"}
      sub={"Лимиты и учёт ресурсов"}
      main={"Лимит родителя действует на всех потомков."}
    >
      <V03 cues={[5.6, 18.9, 27.2]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Слои образа"}
      sub={"overlayfs и копирование при записи"}
      main={"Ни ядра, ни прошивки: старт за миллисекунды."}
    >
      <V04 cues={[11.2, 21.8, 22.8]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Граница изоляции"}
      sub={"Выходы против системных вызовов"}
      main={"Ошибка ядра — побег: общее ядро, общая уязвимость."}
    >
      <V05 cues={[10.6, 18.5, 29.6]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Сравнение"}
      sub={"ОС, старт, память, миграция"}
      main={"Каждое преимущество одной технологии — недостаток другой."}
    >
      <V06 cues={[11.4, 20.9, 25.6]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Усиление контейнеров"}
      sub={"seccomp, capabilities, user ns, LSM"}
      main={"Все меры работают внутри одного ядра."}
    >
      <V07 cues={[10.1, 18.6, 27.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"gVisor"}
      sub={"Ядро в пользовательском пространстве"}
      main={"Sentry перехватывает системные вызовы; к хозяину — узкий путь."}
    >
      <V08 cues={[12.9, 13.9, 27.7]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Kata Containers"}
      sub={"Контейнер внутри лёгкой ВМ"}
      main={"Граница аппаратная; цена — память и старт."}
    >
      <V09 cues={[9.9, 18.4, 25.1]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Что выбрать"}
      sub={"По модели угроз"}
      main={"Чужие арендаторы — ВМ, Kata или gVisor; часто контейнеры внутри ВМ."}
    >
      <V10 cues={[7.7, 15.9, 28.6]} />
    </Slide>
  );
}

export const SLIDES_VM12 = {
  "17:12": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM12).
export const SLIDE_TITLES_VM12 = {
  "17:12": [
    "Стеки",
    "Namespaces",
    "cgroups",
    "Слои",
    "Граница",
    "Сравнение",
    "Усиление",
    "gVisor",
    "Kata",
    "Итог",
  ],
};
