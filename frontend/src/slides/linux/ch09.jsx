// Слайды для «Погружаемся в Unix», глава 9 — «Память: страницы, зоны и адресное пространство».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Os09.jsx).

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
} from "../anim/Os09.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ПАМЯТЬ И ДИСКИ / ГЛАВА 9</span>
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
      title={"Обещание вместо памяти"}
      sub={"Глава 9 · Управление памятью"}
      main={"malloc даёт адреса, а кадры выделяются при первом обращении."}
    >
      <V01 cues={[13.3, 14.3, 32.5]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Страницы и фолии"}
      sub={"Единицы учёта"}
      main={"Ядро думает страницами по 4 КиБ и всё чаще — фолиями."}
    >
      <V02 cues={[9.2, 16.2, 28.5]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Зоны и узлы"}
      sub={"Не вся память одинакова"}
      main={"Ядро учитывает возможности устройств и ближайший узел памяти."}
    >
      <V03 cues={[8.4, 18.3, 28.0]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Система двойников"}
      sub={"Выдача страниц блоками"}
      main={
        "Блоки делятся пополам и склеиваются обратно — так борются с фрагментацией."
      }
    >
      <V04 cues={[5.5, 19.3, 24.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Slab и kmalloc"}
      sub={"Мелкие объекты ядра"}
      main={"Кэши одинаковых ячеек дают объекты за считанные такты."}
    >
      <V05 cues={[9.1, 23.9, 30.7]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Адресное пространство"}
      sub={"Области, maps, ASLR"}
      main={
        "Процесс — это набор областей; они хранятся в maple tree с ядра 6.1."
      }
    >
      <V06 cues={[14.1, 15.1, 27.4]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Страничная ошибка"}
      sub={"Ленивое выделение"}
      main={"Малая ошибка — без диска, большая — с чтением."}
    >
      <V07 cues={[9.1, 17.1, 26.9]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Таблицы страниц"}
      sub={"Четыре уровня, TLB, huge page"}
      main={"TLB прячет обход таблиц, огромные страницы укорачивают его."}
    >
      <V08 cues={[5.3, 20.5, 33.3]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Вытеснение и своп"}
      sub={"MGLRU и kswapd"}
      main={
        "MGLRU вытесняет самое старое поколение; своп бывает и в сжатой памяти."
      }
    >
      <V09 cues={[6.4, 19.6, 36.3]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"OOM и лимиты"}
      sub={"Когда памяти нет совсем"}
      main={"Лимиты cgroup и systemd-oomd не дают беде дойти до всей машины."}
    >
      <V10 cues={[5.1, 16.5, 27.4]} />
    </Slide>
  );
}

export const SLIDES_LX9 = {
  "8:9": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_LX9).
export const SLIDE_TITLES_LX9 = {
  "8:9": [
    "Введение",
    "Страницы",
    "Зоны и NUMA",
    "Buddy",
    "Slab",
    "Адресное пространство",
    "Page fault",
    "Таблицы и TLB",
    "Вытеснение",
    "OOM",
  ],
};
