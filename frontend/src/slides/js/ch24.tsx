// Слайды для «Современный Frontend», глава 24 — «Пакетные менеджеры: npm, pnpm, yarn, package.json, semver и lock-файлы».
// Один абзац урока = один слайд; в каждом — анимированная схема (slides/anim/Js24.tsx).

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
} from "../anim/Js24.tsx";
import { makeSlide } from "../SlideFrame.tsx";

const Slide = makeSlide("СОВРЕМЕННЫЙ FRONTEND / СБОРКА И ПАКЕТЫ / ГЛАВА 24", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Зачем пакетный менеджер"}
      sub={"Глава 24 · Пакеты"}
      main={"Менеджер находит, скачивает и воспроизводимо устанавливает зависимости вашего проекта."}
    >
      <V01 cues={[14.2, 28.4]} />
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"package.json"}
      sub={"Манифест пакета"}
      main={"package.json описывает пакет: имя, версию, зависимости, скрипты, точки входа и тип модулей."}
    >
      <V02 cues={[12.5, 25]} />
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Семантические версии"}
      sub={"major.minor.patch"}
      main={"MAJOR ломает совместимость, MINOR добавляет возможности, PATCH исправляет ошибки."}
    >
      <V03 cues={[12.9, 25.8]} />
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Диапазоны версий"}
      sub={"^ ~ >= x"}
      main={"^1.2.3 = ≥1.2.3 <2.0.0; ~1.2.3 = ≥1.2.3 <1.3.0; для 0.x каретка строже."}
    >
      <V04 cues={[13.1, 26.2]} />
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Разрешение зависимостей"}
      sub={"Дерево и hoisting"}
      main={"Менеджер строит дерево: общие версии поднимаются наверх, конфликты — вкладываются."}
    >
      <V05 cues={[12.5, 25]} />
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Lock-файл"}
      sub={"Воспроизводимость"}
      main={"Lock-файл фиксирует точные версии и хеши: сборка везде одинакова. Коммитим; в CI — npm ci."}
    >
      <V06 cues={[12.9, 25.8]} />
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"pnpm"}
      sub={"Единое хранилище"}
      main={"pnpm хранит каждый файл один раз и раскладывает жёсткими ссылками; node_modules строгий."}
    >
      <V07 cues={[12.1, 24.2]} />
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Yarn"}
      sub={"Berry и PnP"}
      main={"Yarn: рабочие пространства, офлайн-кэш и Plug'n'Play без node_modules."}
    >
      <V08 cues={[13, 26]} />
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Workspaces"}
      sub={"Монорепозиторий"}
      main={"Workspaces: несколько пакетов в одном репозитории, связанные локальными ссылками."}
    >
      <V09 cues={[13, 26]} />
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Скрипты"}
      sub={"npm run и npx"}
      main={"scripts запускаются с node_modules/.bin в PATH; pre/post-хуки окружают команду."}
    >
      <V10 cues={[12.3, 24.6]} />
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Обновления и аудит"}
      sub={"outdated и audit"}
      main={"Обновляйте регулярно малыми шагами; npm audit показывает известные уязвимости."}
    >
      <V11 cues={[12.9, 25.8]} />
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные проблемы"}
      sub={"Что ломается"}
      main={"Фантомные зависимости, конфликты peer, дубликаты и разросшийся размер — главные боли."}
    >
      <V12 cues={[12.8, 25.6]} />
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги"}
      sub={"Пакеты"}
      main={"Манифест + semver-диапазоны + lock-файл = воспроизводимая установка."}
    >
      <V13 cues={[14.3, 28.6]} />
    </Slide>
  );
}

export const SLIDES_J24 = {
  "11:24": [S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_J24).
export const SLIDE_TITLES_J24 = {
  "11:24": [
    "Введение",
    "package.json",
    "semver",
    "Диапазоны",
    "Дерево",
    "Lock-файл",
    "pnpm",
    "Yarn",
    "Workspaces",
    "Скрипты",
    "Обновления",
    "Проблемы",
    "Итоги",
  ],
};
