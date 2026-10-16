// Слайды для «Виртуализации», глава 14 — «Безопасность».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Vm14.jsx).

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
} from "../anim/Vm14.jsx";

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>КОНТЕЙНЕРЫ, ОБЛАКО И БЕЗОПАСНОСТЬ / ГЛАВА 14</span>
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
      title={"Модель угроз"}
      sub={"Глава 14 · Безопасность"}
      main={"Гость, хозяин и клиент защищаются от разных угроз."}
    >
      <V01 cues={[8.0, 15.9, 28.1]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Побег из гостя"}
      sub={"Ошибки в эмуляции устройств"}
      main={"Меньше устройств, запертый монитор, обновления."}
    >
      <V02 cues={[10.9, 27.3, 32.9]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Устройства и прошивки"}
      sub={"DMA и доверие к железу"}
      main={"IOMMU и проверка прошивок — обязательны."}
    >
      <V03 cues={[12.2, 20.4, 27.6]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Побочные каналы"}
      sub={"Prime+Probe и кэш"}
      main={"Не делить ядра и кэши между недоверенными."}
    >
      <V04 cues={[11.1, 21.9, 28.5]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Спекулятивное исполнение"}
      sub={"Meltdown, Spectre, L1TF"}
      main={"Меры стоят скорости: микрокод, сброс L1D, SMT."}
    >
      <V05 cues={[7.1, 20.8, 27.1]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Шумный сосед"}
      sub={"Отказ в обслуживании"}
      main={"Квоты, лимиты и защита от штормов прерываний."}
    >
      <V06 cues={[13.3, 14.3, 25.9]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Конфиденциальные вычисления"}
      sub={"SEV-SNP, TDX, CCA"}
      main={"Память ВМ зашифрована от гипервизора."}
    >
      <V07 cues={[7.1, 22.3, 32.1]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Аттестация"}
      sub={"Измерение, подпись, проверка"}
      main={"Секреты выдают только после проверки отчёта."}
    >
      <V08 cues={[6.8, 18.5, 27.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Практика защиты"}
      sub={"Чек-лист"}
      main={"Обновления, минимум устройств, изоляция, квоты."}
    >
      <V09 cues={[10.6, 19.8, 29.9]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Путь книги"}
      sub={"От ловушек до confidential"}
      main={"Виртуализация — аккуратная работа с границами."}
    >
      <V10 cues={[1.9, 24.6, 29.5]} />
    </Slide>
  );
}

export const SLIDES_VM14 = {
  "17:14": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_VM14).
export const SLIDE_TITLES_VM14 = {
  "17:14": [
    "Угрозы",
    "Побег",
    "Устройства",
    "Кэш",
    "Spectre",
    "DoS",
    "TEE",
    "Аттестация",
    "Чек-лист",
    "Итог книги",
  ],
};
