// Слайды для «Компьютерные сети», глава 7 — «TCP: рукопожатие, нумерация байтов и закрытие соединения».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt07.jsx).

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
} from "../anim/Nt07.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ТРАНСПОРТНЫЙ УРОВЕНЬ / ГЛАВА 7</span>
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
      title={"Надёжный поток"}
      sub={"Что даёт TCP"}
      main={
        "TCP строит надёжный упорядоченный поток байтов поверх ненадёжного IP."
      }
    >
      <V01 cues={[5.4, 17.2, 26.4]} />
      <div className="s-note">
        Цена надёжности — рукопожатие, состояние и задержки.
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Соединение"}
      sub={"Четвёрка и поток"}
      main={
        "Соединение — это четвёрка адресов и портов; границ сообщений в потоке нет."
      }
    >
      <V02 cues={[4.8, 18.4, 26.6]} />
      <div className="s-note">
        Три записи по 100 байт можно прочитать одним куском.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Рукопожатие"}
      sub={"SYN, SYN-ACK, ACK"}
      main={
        "Три сегмента: SYN, SYN-ACK, ACK — стороны обмениваются случайными начальными номерами."
      }
    >
      <V03 cues={[8.8, 20.2, 26.9]} />
      <div className="s-note">Закрытый порт — RST, фильтр — тишина.</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Нумерация байтов"}
      sub={"seq и ack"}
      main={
        "Каждый байт нумеруется, ACK кумулятивный: «жду следующий за таким-то»."
      }
    >
      <V04 cues={[13.7, 20.5, 26.1]} />
      <div className="s-note">
        Пропуск виден сразу: повторяется прежнее подтверждение.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Заголовок TCP"}
      sub={"Флаги, окно и MSS"}
      main={
        "Флаги SYN, ACK, FIN, RST, PSH, окно и MSS — всё, чем стороны управляют потоком."
      }
    >
      <V05 cues={[6.4, 16.6, 24.7]} />
      <div className="s-note">
        MSS выбирают при рукопожатии, чтобы не было фрагментации.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Потери и повторы"}
      sub={"Таймер и дубли ACK"}
      main={
        "Потерю ловят по таймеру RTO или по трём одинаковым ACK и повторяют сегмент."
      }
    >
      <V06 cues={[6.4, 16.5, 26.6]} />
      <div className="s-note">
        Получатель не отдаёт приложению данные из середины с дырой.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Закрытие"}
      sub={"FIN в каждую сторону"}
      main={
        "Закрытие идёт в каждую сторону отдельно: FIN, ACK, FIN, ACK, а затем TIME_WAIT около минуты."
      }
    >
      <V07 cues={[6.7, 17.6, 23.4]} />
      <div className="s-note">
        Полузакрытое соединение: одна сторона закончила, другая ещё шлёт.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Состояния"}
      sub={"Что показывает ss"}
      main={
        "LISTEN, SYN-SENT, ESTABLISHED, TIME-WAIT — по ним видно, что происходит с соединениями."
      }
    >
      <V08 cues={[9.9, 15.5, 24.6]} />
      <div className="s-note">Много SYN-RECV — признак SYN-flood.</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Отказ и молчание"}
      sub={"Как различать диагнозы"}
      main={
        "RST значит «порт закрыт, узел жив», тишина — «пакеты теряются или отфильтрованы»."
      }
    >
      <V09 cues={[12.5, 16.1, 27.6]} />
      <div className="s-note">Диагностика начинается с этого различия.</div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Итоги главы"}
      sub={"Что унести дальше"}
      main={
        "Рукопожатие, номера и ACK, повторы и FIN дают надёжность; скорость — в следующей главе."
      }
    >
      <V10 cues={[5.4, 16.4, 24.6]} />
      <div className="s-note">Дальше — окна и перегрузка.</div>
    </Slide>
  );
}

export const SLIDES_NT7 = {
  "15:7": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT7).
export const SLIDE_TITLES_NT7 = {
  "15:7": [
    "Надёжный поток",
    "Соединение",
    "Рукопожатие",
    "Нумерация и ACK",
    "Заголовок TCP",
    "Потери и повторы",
    "Закрытие",
    "Состояния",
    "Отказ и молчание",
    "Итоги",
  ],
};
