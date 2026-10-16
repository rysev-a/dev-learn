import { cell, codeIn, type Extra } from "./dsl.ts";
export { Box, arrow } from "./dsl.ts";
export { slot } from "./rs.tsx";

/* Помощники для сцен книги «От assembler к языку C»: код C и ассемблер RISC-V с подсветкой. */

// Код на C, ассемблер RISC-V и Python: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const cc = codeIn("c");
export const asm = codeIn("asm");
export const py = codeIn("py");
// Ячейка памяти с адресом
export const mem = (id: string, x: number, y: number, text: string | number, c = "b", extra: Extra = {}) => cell(id, x, y, text, c, { w: 40, h: 24, size: 9, ...extra });
