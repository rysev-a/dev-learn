import type { ReactNode } from "react";

/* Иконки книг в стиле shadcn/lucide: 24×24, контур 1.8, скруглённые концы.
   Имя иконки задаёт книга: поле icon в backend/app/data/sql/books.sql. Новая иконка — запись в ICONS. */

const ICONS: Record<string, ReactNode> = {
  // дискретная математика — сигма
  sigma: (
    <path d="M18 7V5a1 1 0 0 0-1-1H6.5a.5.5 0 0 0-.4.8l4.5 6a2 2 0 0 1 0 2.4l-4.5 6a.5.5 0 0 0 .4.8H17a1 1 0 0 0 1-1v-2" />
  ),
  // Python — две сцепленные «змеи» с глазами (контурный логотип)
  python: (
    <>
      <path d="M12 9H5a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h3" />
      <path d="M12 15h7a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3" />
      <path d="M8 9V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-4" />
      <path d="M11 6h.01M13 18h.01" />
    </>
  ),
  // алгоритмы — дерево из трёх узлов, корень закрашен
  tree: (
    <>
      <circle cx="12" cy="5" r="2.5" fill="currentColor" />
      <circle cx="6" cy="19" r="2.5" />
      <circle cx="18" cy="19" r="2.5" />
      <path d="M11 7.3 7 16.7M13 7.3l4 9.4" />
    </>
  ),
  // архитектура компьютера — микросхема
  chip: (
    <>
      <rect x="7" y="7" width="10" height="10" rx="1.5" />
      <path d="M10 2v3M14 2v3M10 19v3M14 19v3M2 10h3M2 14h3M19 10h3M19 14h3" />
    </>
  ),
  // Linux — терминал
  terminal: (
    <>
      <path d="m4 17 6-6-6-6" />
      <path d="M12 19h8" />
    </>
  ),
  // базы данных
  database: (
    <>
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M3 5v14a9 3 0 0 0 18 0V5" />
      <path d="M3 12a9 3 0 0 0 18 0" />
    </>
  ),
  // Rust — шестерня с буквой R (контурный логотип)
  rust: (
    <>
      <circle cx="12" cy="12" r="7.5" />
      <path d="M12 4.5V2M12 19.5V22M4.5 12H2M19.5 12H22M6.7 6.7 4.9 4.9M17.3 17.3l1.8 1.8M6.7 17.3l-1.8 1.8M17.3 6.7l1.8-1.8" />
      <path d="M10 15.5v-7h3a2 2 0 0 1 0 4h-3M13 12.5l1.8 3" />
    </>
  ),
  // C — буква C в скобках-шевронах
  brackets: (
    <>
      <path d="M16 8.5A5 5 0 1 0 16 15.5" />
      <path d="M3.5 7 2 12l1.5 5M20.5 7 22 12l-1.5 5" />
    </>
  ),
  // компьютерные сети — три узла, соединённые линиями
  network: (
    <>
      <rect x="9" y="3" width="6" height="5" rx="1" />
      <rect x="2" y="16" width="6" height="5" rx="1" />
      <rect x="16" y="16" width="6" height="5" rx="1" />
      <path d="M12 8v4M5 16v-4h14v4" />
    </>
  ),
  // системный дизайн — стопка слоёв архитектуры
  layers: (
    <>
      <path d="m12 2.5 9 4.5-9 4.5L3 7z" />
      <path d="m3 12 9 4.5 9-4.5" />
      <path d="m3 17 9 4.5 9-4.5" />
    </>
  ),
  // виртуализация — вложенные «машины»: внешний хост и две виртуальные внутри
  nested: (
    <>
      <rect x="2" y="3" width="20" height="18" rx="2" />
      <rect x="5.5" y="7" width="5" height="9" rx="1" />
      <rect x="13.5" y="7" width="5" height="9" rx="1" />
    </>
  ),
  // JavaScript — квадрат с буквами JS (контурный логотип)
  js: (
    <>
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <path d="M11 10v5a2 2 0 0 1-4 0" />
      <path d="M18 10.6c-.4-.6-1-.9-1.7-.9-1 0-1.6.6-1.6 1.3 0 1.9 3.5 1.1 3.5 3.1 0 .9-.8 1.5-1.8 1.5-.9 0-1.5-.4-1.9-1.1" />
    </>
  ),
};

// книга по умолчанию
const FALLBACK = (
  <>
    <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
  </>
);

export default function BookIcon({ icon, size = 20 }: { icon: string | null | undefined; size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {(icon != null && ICONS[icon]) || FALLBACK}
    </svg>
  );
}
