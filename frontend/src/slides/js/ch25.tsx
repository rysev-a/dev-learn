// Слайды для «Современный Frontend», глава 25 — «Реестры: npm registry, JSR (JavaScript Registry), публикация и безопасность цепочки поставок».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js25.tsx).

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
} from "../anim/Js25.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / СБОРКА И ПАКЕТЫ / ГЛАВА 25", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Откуда берутся пакеты"}
      sub={"Глава 25 · Реестры"}
      main={"Реестр — сервер с метаданными и архивами пакетов; менеджер общается с ним по HTTP."}
    >
      <V01 cues={[13.2, 26.3]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"npm registry"}
      sub={"Метаданные и теги"}
      main={"Документ пакета: versions, dist-tags (latest, next), dist.tarball и dist.integrity."}
    >
      <V02 cues={[12.7, 25.4]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"JSR"}
      sub={"JavaScript Registry"}
      main={"JSR: TypeScript-first, только ES-модули, публикация исходников, рейтинг и provenance."}
    >
      <V03 cues={[13.2, 26.3]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Приватные реестры"}
      sub={"Область и токены"}
      main={"Scope → свой реестр в .npmrc; токен доступа хранится в переменной окружения."}
    >
      <V04 cues={[12.3, 24.6]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Публикация"}
      sub={"npm publish"}
      main={"publish упаковывает files, проверяет версию и ставит тег; --tag next не трогает latest."}
    >
      <V05 cues={[12.6, 25.3]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Жизнь версии"}
      sub={"deprecate и unpublish"}
      main={"Версию не переписывают: устаревшее помечают deprecate, а unpublish строго ограничен."}
    >
      <V06 cues={[13, 26]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Целостность"}
      sub={"SRI и хеши"}
      main={"integrity = алгоритм-base64 хеша архива; lock-файл сохраняет его, менеджер проверяет."}
    >
      <V07 cues={[12.2, 24.3]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Атаки на цепочку"}
      sub={"Что случается"}
      main={"Тайпсквоттинг, подмена внутреннего имени, взлом мейнтейнера, вредные install-скрипты."}
    >
      <V08 cues={[12.5, 25.1]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Защитные меры"}
      sub={"Гигиена зависимостей"}
      main={"Lock-файл, npm ci, --ignore-scripts, области на свой реестр, меньше зависимостей."}
    >
      <V09 cues={[12.5, 25]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Provenance и SBOM"}
      sub={"Подписи и состав"}
      main={"Provenance связывает пакет с коммитом и сборкой; SBOM перечисляет компоненты."}
    >
      <V10 cues={[13.5, 27]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Лицензии"}
      sub={"SPDX"}
      main={"Лицензия в SPDX-идентификаторах; выражения OR и AND; политика разрешённых и запрещённых."}
    >
      <V11 cues={[13, 26]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Как выбирать пакет"}
      sub={"Критерии"}
      main={"Поддержка, зависимости, размер, лицензия, типы, активность — и «а нужен ли пакет вообще»."}
    >
      <V12 cues={[12.5, 25]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Реестры и безопасность"}
      main={"Реестр отдаёт метаданные и архивы; цепочка поставок — зона риска, которую нужно защищать."}
    >
      <V13 cues={[14.2, 28.4]} />
    </Slide>
  );
}

export const SLIDES_J25 = {
  "11:25": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J25).
export const SLIDE_TITLES_J25 = {
  "11:25": [
    "Введение",
    "npm registry",
    "JSR",
    "Приватные",
    "Публикация",
    "Жизнь версии",
    "Целостность",
    "Атаки",
    "Защита",
    "Provenance",
    "Лицензии",
    "Выбор пакета",
    "Итоги",
  ],
};
