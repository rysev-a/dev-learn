// Слайды для «Python как первый язык», глава 40 — «Абстрактные классы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Py40.jsx).

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
} from "../anim/Py40.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / ПРОЕКТИРОВАНИЕ КЛАССОВ / ГЛАВА 40</span>
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
      title={"Контракт"}
      sub={"Зачем абстрактные классы"}
      main={"Абстрактный класс — обещание, которое выполнят все наследники."}
    >
      <V01 cues={[15.9, 30.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"ABC и abstractmethod"}
      sub={"Нельзя создать без реализации"}
      main={"Забытый метод обнаруживается при создании объекта."}
    >
      <V02 cues={[14.1, 22.6]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Как это устроено"}
      sub={"ABCMeta"}
      main={"Без ABC декоратор молча игнорируется."}
    >
      <V03 cues={[14.7, 31.9]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Тело и свойства"}
      sub={"Абстрактные property и classmethod"}
      main={"@property или @classmethod сверху, @abstractmethod ниже."}
    >
      <V04 cues={[11.2, 23.9]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Шаблонный метод"}
      sub={"Алгоритм из шагов"}
      main={"Порядок вызовов в базовом классе, шаги — в наследниках."}
    >
      <V05 cues={[10.5, 25.2]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Виртуальные наследники"}
      sub={"register и __subclasshook__"}
      main={"Объект с нужным методом уже Sized."}
    >
      <V06 cues={[13.9, 27.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"collections.abc"}
      sub={"Готовые контракты"}
      main={"Два метода — и десяток готовых."}
    >
      <V07 cues={[12.4, 29.8]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Числовая башня"}
      sub={"numbers"}
      main={"Проверяйте по абстрактным классам, а не по int."}
    >
      <V08 cues={[10.6, 21.9]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Принцип подстановки"}
      sub={"Лисков"}
      main={"Не требуйте больше и не обещайте меньше."}
    >
      <V09 cues={[15.4, 29.4]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Хранилища"}
      sub={"Внедрение зависимостей"}
      main={"Приложение знает интерфейс, а не реализацию."}
    >
      <V10 cues={[13.7, 26.9]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Ловушки"}
      sub={"Что не так"}
      main={"Небольшой контракт, осмысленное тело."}
    >
      <V11 cues={[10.2, 22.9]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Три способа"}
      sub={"Утки, ABC, Protocol"}
      main={"Выбирайте по задаче."}
    >
      <V12 cues={[15.6, 22.9]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Абстрактные классы"}
      main={"Контракт плюс общие реализации."}
    >
      <V13 cues={[12.0, 19.3, 27.6]} />
    </Slide>
  );
}

export const SLIDES_P40 = {
  "13:40": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P40).
export const SLIDE_TITLES_P40 = {
  "13:40": [
    "Контракт",
    "ABC",
    "ABCMeta",
    "Свойства",
    "Шаблонный метод",
    "register",
    "collections.abc",
    "numbers",
    "Подстановка",
    "Хранилища",
    "Ловушки",
    "Три способа",
    "Итоги",
  ],
};
