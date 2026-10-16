// Слайды для «Компьютерные сети», глава 18 — «SSH, VPN и туннели».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Nt18.jsx).

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
} from "../anim/Nt18.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ЭКСПЛУАТАЦИЯ И БЕЗОПАСНОСТЬ / ГЛАВА 18</span>
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
      title={"Два набора приёмов"}
      sub={"SSH и VPN"}
      main={
        "SSH — защищённая оболочка и пересылка портов, VPN — шифрованный туннель между сетями."
      }
    >
      <V01 cues={[12.1, 19.3, 26.0]} />
      <div className="s-note">
        Одно — для администрирования, другое — для связи офисов.
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"SSH"}
      sub={"Вместо telnet"}
      main={
        "SSH шифрует сеанс и проверяет сервер; порт 22 постоянно сканируют, поэтому защита обязательна."
      }
    >
      <V02 cues={[6.6, 19.5, 26.3]} />
      <div className="s-note">Заодно — файлы (scp, sftp) и туннели.</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Ключ хоста"}
      sub={"Доверие при первом использовании"}
      main={
        "Первый вход запоминает ключ сервера в known_hosts; при изменении клиент громко предупреждает."
      }
    >
      <V03 cues={[6.3, 18.6, 31.2]} />
      <div className="s-note">
        Предупреждение — повод проверить, а не заглушить.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Ключи входа"}
      sub={"Вместо паролей"}
      main={
        "Закрытый ключ остаётся у вас, открытый — в authorized_keys; затем парольный вход выключают."
      }
    >
      <V04 cues={[6.5, 20.1, 26.9]} />
      <div className="s-note">Секрет по сети не передаётся.</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Бастион и пересылка"}
      sub={"Прыжок и туннель"}
      main={
        "Через бастион — ssh -J; пересылка портов удобна, но открывает доступ ко всей сети с сервера."
      }
    >
      <V05 cues={[5.6, 18.2, 30.9]} />
      <div className="s-note">Внутренние серверы наружу не публикуются.</div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Туннель VPN"}
      sub={"Пакет в пакете"}
      main={
        "Пакет частной сети упаковывается в UDP между публичными адресами шлюзов и распаковывается на другом конце."
      }
    >
      <V06 cues={[9.1, 16.3, 31.3]} />
      <div className="s-note">Снаружи видны два адреса и шифртекст.</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Реализации"}
      sub={"IPsec, OpenVPN, WireGuard"}
      main={
        "Настройка везде одинакова: пир и ключ, адрес туннеля и маршруты в туннель; не совпал ключ — тишина."
      }
    >
      <V07 cues={[10.4, 23.2, 24.2]} />
      <div className="s-note">WireGuard без трафика молчит.</div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"MTU и раздельный туннель"}
      sub={"Практика"}
      main={
        "Внутри туннеля MTU меньше; раздельный туннель отправляет в VPN только корпоративные сети."
      }
    >
      <V08 cues={[3.2, 20.4, 28.7]} />
      <div className="s-note">Пакеты самого туннеля идут мимо туннеля.</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Безопасность"}
      sub={"Что не забыть"}
      main={
        "Ключи — главный секрет; внутри VPN нужны правила файрвола, ноль доверия и чтение логов."
      }
    >
      <V09 cues={[9.0, 19.1, 31.1]} />
      <div className="s-note">Нахождение в сети ничего не гарантирует.</div>
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
        "SSH: ключи и бастион; VPN: пир, ключ, адрес и маршруты; MTU и раздельный туннель — детали."
      }
    >
      <V10 cues={[8.9, 18.9, 25.0]} />
      <div className="s-note">Дальше — атаки и защита.</div>
    </Slide>
  );
}

export const SLIDES_NT18 = {
  "15:18": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_NT18).
export const SLIDE_TITLES_NT18 = {
  "15:18": [
    "SSH и VPN",
    "SSH",
    "Ключ хоста",
    "Ключи входа",
    "Бастион",
    "Туннель",
    "IPsec, OpenVPN, WireGuard",
    "MTU и split tunnel",
    "Безопасность",
    "Итоги",
  ],
};
