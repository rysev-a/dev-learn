// Слайды для «Базы данных», глава 20 — «Хранилища: страницы, журнал и два лагеря».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Db20.jsx).

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
} from "../anim/Db20.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>БАЗЫ ДАННЫХ / СКОРОСТЬ И ХРАНИЛИЩА / ГЛАВА 20</span>
      <span>{String(n).padStart(2, "0")} / 13</span>
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
      title={"Память и диск"}
      sub={"Глава 20 · Хранилища"}
      main={"Диск читает блоками и на порядки медленнее памяти."}
    >
      <V01 cues={[17.5, 34.6]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Страница"}
      sub={"Слоты и строки"}
      main={
        "Адрес строки — (страница, слот); строки заполняют страницу с конца."
      }
    >
      <V02 cues={[13.0, 25.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Буферный пул"}
      sub={"Кэш страниц"}
      main={"Попадания спасают от диска; грязные страницы пишутся позже."}
    >
      <V03 cues={[10.1, 26.4]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Журнал WAL"}
      sub={"Сначала журнал"}
      main={"Коммит — это fsync журнала, а не страниц."}
    >
      <V04 cues={[9.4, 23.4]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Восстановление"}
      sub={"LSN и контрольная точка"}
      main={"Redo применяет записи с LSN больше страничного — идемпотентно."}
    >
      <V05 cues={[12.8, 30.7]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Куча и кластеризация"}
      sub={"Где лежат строки"}
      main={"Куча — индекс с адресами; кластеризованная таблица — B-дерево."}
    >
      <V06 cues={[12.1, 26.3]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"B-дерево: запись"}
      sub={"На месте"}
      main={"Обновление на месте: случайные записи и усиление записи."}
    >
      <V07 cues={[10.9, 23.2]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"LSM: запись"}
      sub={"Memtable и SSTable"}
      main={"Пишем только в конец; компакция чистит."}
    >
      <V08 cues={[15.7, 32.8]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"LSM: чтение"}
      sub={"Bloom и надгробия"}
      main={"От нового к старому; фильтр Блума экономит чтения."}
    >
      <V09 cues={[12.4, 22.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Три усиления"}
      sub={"Запись, чтение, место"}
      main={"Универсального хранилища нет: выбор — нагрузка."}
    >
      <V10 cues={[12.1, 24.1]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Колонки"}
      sub={"Строки или столбцы"}
      main={"Колоночное хранение сжимается и ускоряет аналитику."}
    >
      <V11 cues={[15.9, 33.3]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"fsync и разрыв страниц"}
      sub={"Надёжность записи"}
      main={"Только fsync гарантирует запись; страницы защищают суммами."}
    >
      <V12 cues={[10.6, 32.5]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Что дальше"}
      main={"Страницы, WAL, B-дерево и LSM — основа хранилищ."}
    >
      <V13 cues={[16.1, 29.8]} />
    </Slide>
  );
}

export const SLIDES_D20 = {
  "9:20": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_D20).
export const SLIDE_TITLES_D20 = {
  "9:20": [
    "Введение",
    "Страница",
    "Буферный пул",
    "WAL",
    "Восстановление",
    "Куча",
    "B-дерево",
    "LSM",
    "Чтение LSM",
    "Усиления",
    "Колонки",
    "fsync",
    "Итоги",
  ],
};
