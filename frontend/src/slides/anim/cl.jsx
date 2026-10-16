import { cell, codeIn } from "./dsl.js";
export { Box, arrow } from "./dsl.js";
export { slot } from "./rs.jsx";

/* Помощники для сцен книги «От assembler к языку C»: код C и ассемблер RISC-V с подсветкой. */

// Код на C, ассемблер RISC-V и Python: lines — строки, hl — подсвеченные, bad — ошибочные (красные)
export const cc = codeIn("c");
export const asm = codeIn("asm");
export const py = codeIn("py");
// Ячейка памяти с адресом
export const mem = (id, x, y, text, c = "b", extra = {}) => cell(id, x, y, text, c, { w: 40, h: 24, size: 9, ...extra });
