/* Какие главы книги «Архитектура компьютера» — лаборатории и что в них за упражнения.
   Номер главы → тип лаборатории и (для схем) раздел из sections.ts. */
import { SECTIONS } from "./sections/sections";
import { TASKS as ASM_TASKS } from "./asm/tasks";
import { RV_TASKS } from "./riscv/rv-tasks";
import { REAL_TASKS } from "./riscv/rv-real-tasks";

export const ARCH_BOOK = 14;

export const LAB_CHAPTERS = {
  6: { kind: "circuit", slug: "simple-circuits" },
  7: { kind: "circuit", slug: "mux" },
  8: { kind: "circuit", slug: "latches" },
  9: { kind: "circuit", slug: "adders" },
  10: { kind: "circuit", slug: "registers" },
  11: { kind: "circuit", slug: "alu" },
  12: { kind: "circuit", slug: "memory" },
  13: { kind: "circuit", slug: "decoder" },
  14: { kind: "circuit", slug: "cpu" },
  15: { kind: "asm" },
  16: { kind: "riscv" },
  17: { kind: "real" },
};

/** номер главы, в которой лежит раздел со схемами (для открытия составных элементов) */
export const CHAPTER_OF_SLUG = Object.fromEntries(
  Object.entries(LAB_CHAPTERS)
    .filter(([, v]) => v.slug)
    .map(([n, v]) => [v.slug, Number(n)]),
);

export const sectionOf = (slug) => SECTIONS.find((s) => s.slug === slug);

/** упражнения главы в виде [{ id, title, text, hint }] */
export function labTasks(chapterNum) {
  const lab = LAB_CHAPTERS[chapterNum];
  if (!lab) return [];
  if (lab.kind === "circuit")
    return sectionOf(lab.slug).exercises.map((e) => ({
      id: e.id,
      title: e.title,
      text: e.task,
      hint: e.hint,
    }));
  const src =
    lab.kind === "asm"
      ? ASM_TASKS
      : lab.kind === "riscv"
        ? RV_TASKS
        : REAL_TASKS;
  return src.map((t) => ({
    id: t.id,
    title: t.title,
    text: t.text,
    hint: t.hint,
  }));
}

export const ASM_BY_ID = Object.fromEntries(ASM_TASKS.map((t) => [t.id, t]));
export const RV_BY_ID = Object.fromEntries(RV_TASKS.map((t) => [t.id, t]));
export const REAL_BY_ID = Object.fromEntries(REAL_TASKS.map((t) => [t.id, t]));
