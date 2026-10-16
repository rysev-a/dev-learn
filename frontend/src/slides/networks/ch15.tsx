// Слайды для «Компьютерные сети», глава 15 — «Диагностика сети: ping, ss, tcpdump и Wireshark».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt15.jsx).

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
} from "../anim/Nt15.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("ЭКСПЛУАТАЦИЯ И БЕЗОПАСНОСТЬ / ГЛАВА 15", 10);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Сеть ломается некрасиво"}
      sub={"Один симптом — много причин"}
      main={
        "«Ничего не открывается» — причина может быть где угодно; помогает метод, а не знание всех команд."
      }
    >
      <V01 cues={[5.4, 16.7, 24.9]} />
      <div className="s-note">Задача — быстро сужать круг.</div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Метод"}
      sub={"Порядок работы"}
      main={
        "Симптом, уровни снизу вверх, одна гипотеза — одно измерение, одно изменение за раз, запись диагноза."
      }
    >
      <V02 cues={[8.1, 19.5, 23.9]} />
      <div className="s-note">Запись избавляет от повторной диагностики.</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"ping"}
      sub={"Первый инструмент"}
      main={
        "Пинг показывает путь и время, но молчание не доказывает, что узла нет: ICMP часто режут."
      }
    >
      <V03 cues={[6.7, 17.2, 25.9]} />
      <div className="s-note">Адрес отвечает, имя нет — это DNS.</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"traceroute"}
      sub={"Путь пакета"}
      main={
        "Звёздочка при нормальных дальше — молчит один маршрутизатор; обрыв — место проблемы."
      }
    >
      <V04 cues={[10.4, 21.8, 27.4]} />
      <div className="s-note">Пути туда и обратно могут различаться.</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"ip и ss"}
      sub={"Что с самим узлом"}
      main={
        "ip показывает интерфейсы и маршруты, ss — слушающие порты; сервис на 127.0.0.1 снаружи недоступен."
      }
    >
      <V05 cues={[13.1, 18.2, 30.9]} />
      <div className="s-note">
        Состояния соединений подсказывают атаки и утечки.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"dig, curl, openssl"}
      sub={"Прикладной уровень"}
      main={
        "dig — DNS, curl -v — HTTP, openssl s_client — TLS; отказ и молчание — разные диагнозы."
      }
    >
      <V06 cues={[6.7, 16.6, 29.9]} />
      <div className="s-note">
        Каждый инструмент отвечает на вопрос «на каком уровне ломается».
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"tcpdump"}
      sub={"Реальные пакеты"}
      main={
        "SYN без ответа — рукопожатие не идёт, RST — порт закрыт; снимайте на нескольких узлах цепочки."
      }
    >
      <V07 cues={[8.7, 21.6, 26.7]} />
      <div className="s-note">
        Фильтры по протоколу, адресу и порту сужают поток.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Wireshark"}
      sub={"Графический разбор"}
      main={
        "Wireshark раскладывает пакеты по полям, показывает потоки и задержки; ключи TLS позволяют читать содержимое."
      }
    >
      <V08 cues={[11.6, 23.2, 30.4]} />
      <div className="s-note">
        Часто снимают tcpdump на сервере и разбирают файл в Wireshark.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"MTU и фрагментация"}
      sub={"«Большое не работает»"}
      main={
        "Большие пакеты с DF не лезут в туннель, а ICMP «frag needed» режут — лечим MTU и MSS."
      }
    >
      <V09 cues={[15.6, 16.6, 28.9]} />
      <div className="s-note">Порог находят пингом с -M do и разными -s.</div>
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
        "Метод и инструменты по уровням: ping, ip, ss, dig, curl, tcpdump; отказ ≠ тишина, а MTU маскируется под «большое не работает»."
      }
    >
      <V10 cues={[7.1, 19.1, 25.8]} />
      <div className="s-note">Дальше — файрволы.</div>
    </Slide>
  );
}

export const SLIDES_NT15 = {
  "15:15": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT15).
export const SLIDE_TITLES_NT15 = {
  "15:15": [
    "Симптом и причины",
    "Метод",
    "ping",
    "traceroute",
    "ip и ss",
    "dig, curl, openssl",
    "tcpdump",
    "Wireshark",
    "MTU",
    "Итоги",
  ],
};
