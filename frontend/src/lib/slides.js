// Реестр слайдов: «book:chapter» → компоненты сцен и их названия.
// Файлы слайдов лежат по книгам: slides/<book>/chNN.jsx.
import {
  SLIDES as SLIDES_LINUX_1,
  SLIDE_TITLES as TITLES_LINUX_1,
} from "../slides/linux/ch01.jsx";
import { SLIDES_CH2, SLIDE_TITLES_CH2 } from "../slides/linux/ch02.jsx";
import { SLIDES_CH3, SLIDE_TITLES_CH3 } from "../slides/linux/ch03.jsx";
import { SLIDES_CH7, SLIDE_TITLES_CH7 } from "../slides/linux/ch07.jsx";
import { SLIDES_CH9, SLIDE_TITLES_CH9 } from "../slides/linux/ch09.jsx";
import { SLIDES_L4, SLIDE_TITLES_L4 } from "../slides/linux/ch04.jsx";
import { SLIDES_L5, SLIDE_TITLES_L5 } from "../slides/linux/ch05.jsx";
import { SLIDES_L6, SLIDE_TITLES_L6 } from "../slides/linux/ch06.jsx";
import { SLIDES_L8, SLIDE_TITLES_L8 } from "../slides/linux/ch08.jsx";
import { SLIDES_L10, SLIDE_TITLES_L10 } from "../slides/linux/ch10.jsx";
import { SLIDES_R1, SLIDE_TITLES_R1 } from "../slides/learn-rust/ch01.jsx";
import { SLIDES_R2, SLIDE_TITLES_R2 } from "../slides/learn-rust/ch02.jsx";
import { SLIDES_R3, SLIDE_TITLES_R3 } from "../slides/learn-rust/ch03.jsx";
import { SLIDES_R4, SLIDE_TITLES_R4 } from "../slides/learn-rust/ch04.jsx";
import { SLIDES_R5, SLIDE_TITLES_R5 } from "../slides/learn-rust/ch05.jsx";
import { SLIDES_R6, SLIDE_TITLES_R6 } from "../slides/learn-rust/ch06.jsx";
import { SLIDES_R7, SLIDE_TITLES_R7 } from "../slides/learn-rust/ch07.jsx";
import { SLIDES_R8, SLIDE_TITLES_R8 } from "../slides/learn-rust/ch08.jsx";
import { SLIDES_R9, SLIDE_TITLES_R9 } from "../slides/learn-rust/ch09.jsx";
import { SLIDES_R10, SLIDE_TITLES_R10 } from "../slides/learn-rust/ch10.jsx";
import { SLIDES_R11, SLIDE_TITLES_R11 } from "../slides/learn-rust/ch11.jsx";
import { SLIDES_R12, SLIDE_TITLES_R12 } from "../slides/learn-rust/ch12.jsx";
import { SLIDES_R13, SLIDE_TITLES_R13 } from "../slides/learn-rust/ch13.jsx";
import { SLIDES_R14, SLIDE_TITLES_R14 } from "../slides/learn-rust/ch14.jsx";
import { SLIDES_R15, SLIDE_TITLES_R15 } from "../slides/learn-rust/ch15.jsx";
import { SLIDES_R16, SLIDE_TITLES_R16 } from "../slides/learn-rust/ch16.jsx";
import { SLIDES_A1, SLIDE_TITLES_A1 } from "../slides/algo/ch01.jsx";
import { SLIDES_A2, SLIDE_TITLES_A2 } from "../slides/algo/ch02.jsx";
import { SLIDES_A3, SLIDE_TITLES_A3 } from "../slides/algo/ch03.jsx";
import { SLIDES_A4, SLIDE_TITLES_A4 } from "../slides/algo/ch04.jsx";
import { SLIDES_A5, SLIDE_TITLES_A5 } from "../slides/algo/ch05.jsx";
import { SLIDES_A6, SLIDE_TITLES_A6 } from "../slides/algo/ch06.jsx";
import { SLIDES_A7, SLIDE_TITLES_A7 } from "../slides/algo/ch07.jsx";
import { SLIDES_A8, SLIDE_TITLES_A8 } from "../slides/algo/ch08.jsx";
import { SLIDES_A9, SLIDE_TITLES_A9 } from "../slides/algo/ch09.jsx";
import { SLIDES_A10, SLIDE_TITLES_A10 } from "../slides/algo/ch10.jsx";
import { SLIDES_A11, SLIDE_TITLES_A11 } from "../slides/algo/ch11.jsx";
import { SLIDES_A12, SLIDE_TITLES_A12 } from "../slides/algo/ch12.jsx";
import { SLIDES_A13, SLIDE_TITLES_A13 } from "../slides/algo/ch13.jsx";
import { SLIDES_A14, SLIDE_TITLES_A14 } from "../slides/algo/ch14.jsx";
import { SLIDES_A15, SLIDE_TITLES_A15 } from "../slides/algo/ch15.jsx";
import { SLIDES_AR1, SLIDE_TITLES_AR1 } from "../slides/arch/ch01.jsx";
import { SLIDES_AR2, SLIDE_TITLES_AR2 } from "../slides/arch/ch02.jsx";
import { SLIDES_AR3, SLIDE_TITLES_AR3 } from "../slides/arch/ch03.jsx";
import { SLIDES_AR4, SLIDE_TITLES_AR4 } from "../slides/arch/ch04.jsx";
import { SLIDES_AR5, SLIDE_TITLES_AR5 } from "../slides/arch/ch05.jsx";
import { SLIDES_AR6, SLIDE_TITLES_AR6 } from "../slides/arch/ch06.jsx";
import { SLIDES_AR7, SLIDE_TITLES_AR7 } from "../slides/arch/ch07.jsx";
import { SLIDES_AR8, SLIDE_TITLES_AR8 } from "../slides/arch/ch08.jsx";
import { SLIDES_AR9, SLIDE_TITLES_AR9 } from "../slides/arch/ch09.jsx";
import { SLIDES_AR10, SLIDE_TITLES_AR10 } from "../slides/arch/ch10.jsx";
import { SLIDES_D1, SLIDE_TITLES_D1 } from "../slides/db/ch01.jsx";
import { SLIDES_D2, SLIDE_TITLES_D2 } from "../slides/db/ch02.jsx";
import { SLIDES_D3, SLIDE_TITLES_D3 } from "../slides/db/ch03.jsx";
import { SLIDES_D4, SLIDE_TITLES_D4 } from "../slides/db/ch04.jsx";
import { SLIDES_D5, SLIDE_TITLES_D5 } from "../slides/db/ch05.jsx";
import { SLIDES_D6, SLIDE_TITLES_D6 } from "../slides/db/ch06.jsx";
import { SLIDES_D7, SLIDE_TITLES_D7 } from "../slides/db/ch07.jsx";
import { SLIDES_D8, SLIDE_TITLES_D8 } from "../slides/db/ch08.jsx";
import { SLIDES_D9, SLIDE_TITLES_D9 } from "../slides/db/ch09.jsx";
import { SLIDES_D10, SLIDE_TITLES_D10 } from "../slides/db/ch10.jsx";
import { SLIDES_J1, SLIDE_TITLES_J1 } from "../slides/js/ch01.jsx";
import { SLIDES_J2, SLIDE_TITLES_J2 } from "../slides/js/ch02.jsx";
import { SLIDES_J3, SLIDE_TITLES_J3 } from "../slides/js/ch03.jsx";
import { SLIDES_J4, SLIDE_TITLES_J4 } from "../slides/js/ch04.jsx";
import { SLIDES_J5, SLIDE_TITLES_J5 } from "../slides/js/ch05.jsx";
import { SLIDES_J6, SLIDE_TITLES_J6 } from "../slides/js/ch06.jsx";
import { SLIDES_J7, SLIDE_TITLES_J7 } from "../slides/js/ch07.jsx";
import { SLIDES_J8, SLIDE_TITLES_J8 } from "../slides/js/ch08.jsx";
import { SLIDES_J9, SLIDE_TITLES_J9 } from "../slides/js/ch09.jsx";
import { SLIDES_J10, SLIDE_TITLES_J10 } from "../slides/js/ch10.jsx";
import { SLIDES_M1, SLIDE_TITLES_M1 } from "../slides/dm/ch01.jsx";
import { SLIDES_M2, SLIDE_TITLES_M2 } from "../slides/dm/ch02.jsx";
import { SLIDES_M3, SLIDE_TITLES_M3 } from "../slides/dm/ch03.jsx";
import { SLIDES_M4, SLIDE_TITLES_M4 } from "../slides/dm/ch04.jsx";
import { SLIDES_M5, SLIDE_TITLES_M5 } from "../slides/dm/ch05.jsx";
import { SLIDES_M6, SLIDE_TITLES_M6 } from "../slides/dm/ch06.jsx";
import { SLIDES_M7, SLIDE_TITLES_M7 } from "../slides/dm/ch07.jsx";
import { SLIDES_M8, SLIDE_TITLES_M8 } from "../slides/dm/ch08.jsx";
import { SLIDES_M9, SLIDE_TITLES_M9 } from "../slides/dm/ch09.jsx";
import { SLIDES_M10, SLIDE_TITLES_M10 } from "../slides/dm/ch10.jsx";
import { SLIDES_P1, SLIDE_TITLES_P1 } from "../slides/py/ch01.jsx";
import { SLIDES_P2, SLIDE_TITLES_P2 } from "../slides/py/ch02.jsx";
import { SLIDES_P3, SLIDE_TITLES_P3 } from "../slides/py/ch03.jsx";
import { SLIDES_P4, SLIDE_TITLES_P4 } from "../slides/py/ch04.jsx";
import { SLIDES_P5, SLIDE_TITLES_P5 } from "../slides/py/ch05.jsx";
import { SLIDES_P6, SLIDE_TITLES_P6 } from "../slides/py/ch06.jsx";
import { SLIDES_P7, SLIDE_TITLES_P7 } from "../slides/py/ch07.jsx";
import { SLIDES_P8, SLIDE_TITLES_P8 } from "../slides/py/ch08.jsx";
import { SLIDES_P9, SLIDE_TITLES_P9 } from "../slides/py/ch09.jsx";
import { SLIDES_P10, SLIDE_TITLES_P10 } from "../slides/py/ch10.jsx";
import { SLIDES_P11, SLIDE_TITLES_P11 } from "../slides/py/ch11.jsx";
import { SLIDES_P12, SLIDE_TITLES_P12 } from "../slides/py/ch12.jsx";
import { SLIDES_P13, SLIDE_TITLES_P13 } from "../slides/py/ch13.jsx";
import { SLIDES_P14, SLIDE_TITLES_P14 } from "../slides/py/ch14.jsx";
import { SLIDES_P15, SLIDE_TITLES_P15 } from "../slides/py/ch15.jsx";
import { SLIDES_P16, SLIDE_TITLES_P16 } from "../slides/py/ch16.jsx";
import { SLIDES_P17, SLIDE_TITLES_P17 } from "../slides/py/ch17.jsx";
import { SLIDES_P18, SLIDE_TITLES_P18 } from "../slides/py/ch18.jsx";
import { SLIDES_P19, SLIDE_TITLES_P19 } from "../slides/py/ch19.jsx";
import { SLIDES_P20, SLIDE_TITLES_P20 } from "../slides/py/ch20.jsx";
import { SLIDES_P21, SLIDE_TITLES_P21 } from "../slides/py/ch21.jsx";
import { SLIDES_P22, SLIDE_TITLES_P22 } from "../slides/py/ch22.jsx";
import { SLIDES_P23, SLIDE_TITLES_P23 } from "../slides/py/ch23.jsx";
import { SLIDES_P24, SLIDE_TITLES_P24 } from "../slides/py/ch24.jsx";
import { SLIDES_P25, SLIDE_TITLES_P25 } from "../slides/py/ch25.jsx";
import { SLIDES_P26, SLIDE_TITLES_P26 } from "../slides/py/ch26.jsx";
import { SLIDES_P27, SLIDE_TITLES_P27 } from "../slides/py/ch27.jsx";
import { SLIDES_P28, SLIDE_TITLES_P28 } from "../slides/py/ch28.jsx";
import { SLIDES_P29, SLIDE_TITLES_P29 } from "../slides/py/ch29.jsx";
import { SLIDES_P30, SLIDE_TITLES_P30 } from "../slides/py/ch30.jsx";
import { SLIDES_P31, SLIDE_TITLES_P31 } from "../slides/py/ch31.jsx";
import { SLIDES_P32, SLIDE_TITLES_P32 } from "../slides/py/ch32.jsx";
import { SLIDES_P33, SLIDE_TITLES_P33 } from "../slides/py/ch33.jsx";

export const SLIDES = {
  ...SLIDES_LINUX_1,
  ...SLIDES_CH2,
  ...SLIDES_CH3,
  ...SLIDES_CH7,
  ...SLIDES_CH9,
  ...SLIDES_L4,
  ...SLIDES_L5,
  ...SLIDES_L6,
  ...SLIDES_L8,
  ...SLIDES_L10,
  ...SLIDES_R1,
  ...SLIDES_R2,
  ...SLIDES_R3,
  ...SLIDES_R4,
  ...SLIDES_R5,
  ...SLIDES_R6,
  ...SLIDES_R7,
  ...SLIDES_R8,
  ...SLIDES_R9,
  ...SLIDES_R10,
  ...SLIDES_R11,
  ...SLIDES_R12,
  ...SLIDES_R13,
  ...SLIDES_R14,
  ...SLIDES_R15,
  ...SLIDES_R16,
  ...SLIDES_A1,
  ...SLIDES_A2,
  ...SLIDES_A3,
  ...SLIDES_A4,
  ...SLIDES_A5,
  ...SLIDES_A6,
  ...SLIDES_A7,
  ...SLIDES_A8,
  ...SLIDES_A9,
  ...SLIDES_A10,
  ...SLIDES_A11,
  ...SLIDES_A12,
  ...SLIDES_A13,
  ...SLIDES_A14,
  ...SLIDES_A15,
  ...SLIDES_AR1,
  ...SLIDES_AR2,
  ...SLIDES_AR3,
  ...SLIDES_AR4,
  ...SLIDES_AR5,
  ...SLIDES_AR6,
  ...SLIDES_AR7,
  ...SLIDES_AR8,
  ...SLIDES_AR9,
  ...SLIDES_AR10,
  ...SLIDES_D1,
  ...SLIDES_D2,
  ...SLIDES_D3,
  ...SLIDES_D4,
  ...SLIDES_D5,
  ...SLIDES_D6,
  ...SLIDES_D7,
  ...SLIDES_D8,
  ...SLIDES_D9,
  ...SLIDES_D10,
  ...SLIDES_J1,
  ...SLIDES_J2,
  ...SLIDES_J3,
  ...SLIDES_J4,
  ...SLIDES_J5,
  ...SLIDES_J6,
  ...SLIDES_J7,
  ...SLIDES_J8,
  ...SLIDES_J9,
  ...SLIDES_J10,
  ...SLIDES_M1,
  ...SLIDES_M2,
  ...SLIDES_M3,
  ...SLIDES_M4,
  ...SLIDES_M5,
  ...SLIDES_M6,
  ...SLIDES_M7,
  ...SLIDES_M8,
  ...SLIDES_M9,
  ...SLIDES_M10,
  ...SLIDES_P1,
  ...SLIDES_P2,
  ...SLIDES_P3,
  ...SLIDES_P4,
  ...SLIDES_P5,
  ...SLIDES_P6,
  ...SLIDES_P7,
  ...SLIDES_P8,
  ...SLIDES_P9,
  ...SLIDES_P10,
  ...SLIDES_P11,
  ...SLIDES_P12,
  ...SLIDES_P13,
  ...SLIDES_P14,
  ...SLIDES_P15,
  ...SLIDES_P16,
  ...SLIDES_P17,
  ...SLIDES_P18,
  ...SLIDES_P19,
  ...SLIDES_P20,
  ...SLIDES_P21,
  ...SLIDES_P22,
  ...SLIDES_P23,
  ...SLIDES_P24,
  ...SLIDES_P25,
  ...SLIDES_P26,
  ...SLIDES_P27,
  ...SLIDES_P28,
  ...SLIDES_P29,
  ...SLIDES_P30,
  ...SLIDES_P31,
  ...SLIDES_P32,
  ...SLIDES_P33,
};

export const SLIDE_TITLES = {
  ...TITLES_LINUX_1,
  ...SLIDE_TITLES_CH2,
  ...SLIDE_TITLES_CH3,
  ...SLIDE_TITLES_CH7,
  ...SLIDE_TITLES_CH9,
  ...SLIDE_TITLES_L4,
  ...SLIDE_TITLES_L5,
  ...SLIDE_TITLES_L6,
  ...SLIDE_TITLES_L8,
  ...SLIDE_TITLES_L10,
  ...SLIDE_TITLES_R1,
  ...SLIDE_TITLES_R2,
  ...SLIDE_TITLES_R3,
  ...SLIDE_TITLES_R4,
  ...SLIDE_TITLES_R5,
  ...SLIDE_TITLES_R6,
  ...SLIDE_TITLES_R7,
  ...SLIDE_TITLES_R8,
  ...SLIDE_TITLES_R9,
  ...SLIDE_TITLES_R10,
  ...SLIDE_TITLES_R11,
  ...SLIDE_TITLES_R12,
  ...SLIDE_TITLES_R13,
  ...SLIDE_TITLES_R14,
  ...SLIDE_TITLES_R15,
  ...SLIDE_TITLES_R16,
  ...SLIDE_TITLES_A1,
  ...SLIDE_TITLES_A2,
  ...SLIDE_TITLES_A3,
  ...SLIDE_TITLES_A4,
  ...SLIDE_TITLES_A5,
  ...SLIDE_TITLES_A6,
  ...SLIDE_TITLES_A7,
  ...SLIDE_TITLES_A8,
  ...SLIDE_TITLES_A9,
  ...SLIDE_TITLES_A10,
  ...SLIDE_TITLES_A11,
  ...SLIDE_TITLES_A12,
  ...SLIDE_TITLES_A13,
  ...SLIDE_TITLES_A14,
  ...SLIDE_TITLES_A15,
  ...SLIDE_TITLES_AR1,
  ...SLIDE_TITLES_AR2,
  ...SLIDE_TITLES_AR3,
  ...SLIDE_TITLES_AR4,
  ...SLIDE_TITLES_AR5,
  ...SLIDE_TITLES_AR6,
  ...SLIDE_TITLES_AR7,
  ...SLIDE_TITLES_AR8,
  ...SLIDE_TITLES_AR9,
  ...SLIDE_TITLES_AR10,
  ...SLIDE_TITLES_D1,
  ...SLIDE_TITLES_D2,
  ...SLIDE_TITLES_D3,
  ...SLIDE_TITLES_D4,
  ...SLIDE_TITLES_D5,
  ...SLIDE_TITLES_D6,
  ...SLIDE_TITLES_D7,
  ...SLIDE_TITLES_D8,
  ...SLIDE_TITLES_D9,
  ...SLIDE_TITLES_D10,
  ...SLIDE_TITLES_J1,
  ...SLIDE_TITLES_J2,
  ...SLIDE_TITLES_J3,
  ...SLIDE_TITLES_J4,
  ...SLIDE_TITLES_J5,
  ...SLIDE_TITLES_J6,
  ...SLIDE_TITLES_J7,
  ...SLIDE_TITLES_J8,
  ...SLIDE_TITLES_J9,
  ...SLIDE_TITLES_J10,
  ...SLIDE_TITLES_M1,
  ...SLIDE_TITLES_M2,
  ...SLIDE_TITLES_M3,
  ...SLIDE_TITLES_M4,
  ...SLIDE_TITLES_M5,
  ...SLIDE_TITLES_M6,
  ...SLIDE_TITLES_M7,
  ...SLIDE_TITLES_M8,
  ...SLIDE_TITLES_M9,
  ...SLIDE_TITLES_M10,
  ...SLIDE_TITLES_P1,
  ...SLIDE_TITLES_P2,
  ...SLIDE_TITLES_P3,
  ...SLIDE_TITLES_P4,
  ...SLIDE_TITLES_P5,
  ...SLIDE_TITLES_P6,
  ...SLIDE_TITLES_P7,
  ...SLIDE_TITLES_P8,
  ...SLIDE_TITLES_P9,
  ...SLIDE_TITLES_P10,
  ...SLIDE_TITLES_P11,
  ...SLIDE_TITLES_P12,
  ...SLIDE_TITLES_P13,
  ...SLIDE_TITLES_P14,
  ...SLIDE_TITLES_P15,
  ...SLIDE_TITLES_P16,
  ...SLIDE_TITLES_P17,
  ...SLIDE_TITLES_P18,
  ...SLIDE_TITLES_P19,
  ...SLIDE_TITLES_P20,
  ...SLIDE_TITLES_P21,
  ...SLIDE_TITLES_P22,
  ...SLIDE_TITLES_P23,
  ...SLIDE_TITLES_P24,
  ...SLIDE_TITLES_P25,
  ...SLIDE_TITLES_P26,
  ...SLIDE_TITLES_P27,
  ...SLIDE_TITLES_P28,
  ...SLIDE_TITLES_P29,
  ...SLIDE_TITLES_P30,
  ...SLIDE_TITLES_P31,
  ...SLIDE_TITLES_P32,
  ...SLIDE_TITLES_P33,
};
