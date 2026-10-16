// Слайды для «Компьютерные сети», глава 13 — «TLS и HTTPS: шифрование, сертификаты и доверие».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt13.jsx).

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
} from "../anim/Nt13.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ПРИКЛАДНОЙ УРОВЕНЬ / ГЛАВА 13</span>
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
      title={"Открытый текст"}
      sub={"Зачем нужен TLS"}
      main={
        "Без TLS любой узел на пути читает и подменяет данные; TLS шифрует канал и проверяет сервер."
      }
    >
      <V01 cues={[5.8, 18.4, 27.1]} />
      <div className="s-note">До сих пор всё шло открытым текстом.</div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Три свойства"}
      sub={"Гарантии TLS"}
      main={
        "Конфиденциальность, целостность, аутентификация; HTTP поверх TLS — это HTTPS на порту 443."
      }
    >
      <V02 cues={[9.7, 16.6, 29.4]} />
      <div className="s-note">
        TLS — отдельный слой между TCP и приложением.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Две криптографии"}
      sub={"Асимметричная и симметричная"}
      main={
        "Асимметричная нужна для рукопожатия, симметричная — для данных; общий секрет по сети не передают."
      }
    >
      <V03 cues={[11.8, 18.6, 30.2]} />
      <div className="s-note">Закрытый ключ по открытому не вычислить.</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Рукопожатие TLS 1.3"}
      sub={"Один круг"}
      main={
        "ClientHello, ServerHello с сертификатом и подписью, Finished — и дальше зашифрованные данные."
      }
    >
      <V04 cues={[12.8, 23.9, 30.4]} />
      <div className="s-note">
        В TLS 1.2 — два круга, старые версии отключены.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Прямая секретность"}
      sub={"Временные ключи"}
      main={
        "Новый секрет в каждом соединении: кража ключа позже не откроет записанный трафик."
      }
    >
      <V05 cues={[11.4, 21.7, 30.6]} />
      <div className="s-note">
        Билеты возобновления ускоряют следующий визит.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Цепочка доверия"}
      sub={"Сертификат и центры"}
      main={
        "Корневой CA подписывает промежуточный, тот — сертификат сайта; клиент доверяет корню из хранилища."
      }
    >
      <V06 cues={[6.5, 15.1, 30.3]} />
      <div className="s-note">Корневые центры зашиты в ОС и браузер.</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Что проверяет клиент"}
      sub={"Четыре проверки"}
      main={
        "Срок, имя в SAN, цепочка до доверенного корня и отзыв; сервер обязан присылать промежуточные."
      }
    >
      <V07 cues={[6.6, 20.3, 35.3]} />
      <div className="s-note">
        Wildcard *.example.org покрывает один уровень.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Частые ошибки"}
      sub={"Что ломается на практике"}
      main={
        "Просрочка, имя без www, забытый промежуточный и недоверенный внутренний CA."
      }
    >
      <V08 cues={[8.6, 19.0, 27.9]} />
      <div className="s-note">Проверяйте не только на своём компьютере.</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"ACME, mTLS и границы"}
      sub={"Автоматизация и ограничения"}
      main={
        "ACME обновляет сертификаты сам, mTLS даёт взаимную проверку, SNI виден открыто; TLS не лечит вредоносный сайт."
      }
    >
      <V09 cues={[9.6, 17.7, 30.0]} />
      <div className="s-note">
        Все выпуски сертификатов попадают в публичные журналы.
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
        "Ключи, сертификат и цепочка доверия дают защищённый канал; в упражнениях вы почините типичные сбои."
      }
    >
      <V10 cues={[5.0, 19.7, 23.7]} />
      <div className="s-note">Дальше — веб-API.</div>
    </Slide>
  );
}

export const SLIDES_NT13 = {
  "15:13": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT13).
export const SLIDE_TITLES_NT13 = {
  "15:13": [
    "Зачем TLS",
    "Три свойства",
    "Две криптографии",
    "Рукопожатие 1.3",
    "Прямая секретность",
    "Цепочка доверия",
    "Что проверяется",
    "Частые ошибки",
    "ACME и границы",
    "Итоги",
  ],
};
