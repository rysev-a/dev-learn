// Слайды для «Компьютерные сети», глава 9 — «Сокеты в программе: блокирующий ввод-вывод, select, epoll и async».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt09.jsx).

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
} from "../anim/Nt09.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ТРАНСПОРТНЫЙ УРОВЕНЬ / ГЛАВА 9</span>
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
      title={"От теории к коду"}
      sub={"Сокеты как интерфейс"}
      main={
        "Программа видит не пакеты, а вызовы ОС: socket, connect, bind, listen, accept, send, recv."
      }
    >
      <V01 cues={[9.4, 19.2, 32.4]} />
      <div className="s-note">
        В упражнениях вы пишете настоящий код на Python.
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"TCP-клиент"}
      sub={"Четыре шага"}
      main={
        "Клиент: socket → connect → sendall/recv → close; connect блокируется до рукопожатия."
      }
    >
      <V02 cues={[6.6, 15.7, 25.2]} />
      <div className="s-note">Закрывайте сокет всегда — лучше через with.</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"TCP-сервер"}
      sub={"bind, listen, accept"}
      main={
        "Сервер привязывает сокет, слушает, а accept возвращает новый сокет для каждого клиента."
      }
    >
      <V03 cues={[9.8, 14.2, 27.6]} />
      <div className="s-note">
        Число в listen — длина очереди неподключённых.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Поток, а не сообщения"}
      sub={"Ловушка recv"}
      main={
        "recv возвращает сколько накопилось: границы сообщений нужно придумать самим."
      }
    >
      <V04 cues={[5.1, 12.4, 23.3]} />
      <div className="s-note">
        Пустой результат recv — собеседник закрыл соединение.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Таймауты и ошибки"}
      sub={"Плохое — это норма"}
      main={
        "Ставьте таймауты, ловите ConnectionRefusedError и timeout, закрывайте сокеты всегда."
      }
    >
      <V05 cues={[11.6, 19.8, 28.4]} />
      <div className="s-note">Утечка сокетов убивает сервер за неделю.</div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Поток на клиента"}
      sub={"Самый простой сервер"}
      main={
        "Поток на клиента — просто и надёжно для сотен соединений, но тяжело для десятков тысяч."
      }
    >
      <V06 cues={[12.5, 17.1, 26.3]} />
      <div className="s-note">
        Дорого: стек и переключения у каждого потока.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"select и epoll"}
      sub={"Мультиплексирование"}
      main={
        "Один поток спрашивает ОС, какие сокеты готовы, и обслуживает только их; epoll тянет сотни тысяч."
      }
    >
      <V07 cues={[9.9, 16.8, 24.4]} />
      <div className="s-note">В Python — модуль selectors.</div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Асинхронность"}
      sub={"Корутины и цикл событий"}
      main={
        "asyncio: await отдаёт управление циклу, тысячи корутин живут в одном потоке."
      }
    >
      <V08 cues={[4.3, 16.0, 23.3]} />
      <div className="s-note">
        Тяжёлый расчёт внутри корутины замораживает всех.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Правила реальных сервисов"}
      sub={"Что не забыть"}
      main={
        "SO_REUSEADDR, лимиты, таймауты, байты вместо строк и обратное давление."
      }
    >
      <V09 cues={[10.3, 18.9, 23.0]} />
      <div className="s-note">
        Логируйте адреса клиентов и причины разрывов.
      </div>
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
        "Клиент, сервер, границы сообщений, таймауты и три способа масштабирования — теперь за код."
      }
    >
      <V10 cues={[6.1, 13.5, 21.4]} />
      <div className="s-note">Дальше — прикладной уровень.</div>
    </Slide>
  );
}

export const SLIDES_NT9 = {
  "15:9": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT9).
export const SLIDE_TITLES_NT9 = {
  "15:9": [
    "От теории к коду",
    "TCP-клиент",
    "TCP-сервер",
    "Поток байтов",
    "Таймауты и ошибки",
    "Поток на клиента",
    "select и epoll",
    "Асинхронность",
    "Правила сервисов",
    "Итоги",
  ],
};
