// Реестр квизов: ключ «bookId:номер_главы» → квиз на теорию
// (вопросы с вариантами, проверка сразу при выборе).
import { ALGO_QUIZZES } from "../quizzes/algo.js";
import { ARCH_QUIZZES } from "../quizzes/arch.js";
import { DB_QUIZZES } from "../quizzes/db.js";
import { DM_QUIZZES } from "../quizzes/dm.js";
import { JS_QUIZZES } from "../quizzes/js.js";
import { LINUX_QUIZZES } from "../quizzes/linux.js";
import { PY_QUIZZES } from "../quizzes/py.js";
import { RUST_QUIZZES } from "../quizzes/rust.js";

export const QUIZZES = {
  "10:1": {
    kind: "theory",
    title: "Квиз: основы Rust",
    questions: [
      {
        q: "Что делает команда cargo run?",
        options: [
          "Компилирует проект и запускает его",
          "Только компилирует проект",
          "Создаёт новый проект",
          "Запускает тесты",
        ],
        answer: 0,
        expl: "cargo build только компилирует, cargo run — компилирует (если нужно) и сразу запускает.",
      },
      {
        q: "Переменная в Rust по умолчанию…",
        options: [
          "неизменяемая (immutable)",
          "изменяемая (mutable)",
          "статическая",
          "глобальная",
        ],
        answer: 0,
        expl: "Без ключевого слова mut переменную нельзя изменить после присваивания — это защита от случайных мутаций.",
      },
      {
        q: "Что нужно, чтобы менять значение переменной?",
        options: [
          "Объявить её с let mut",
          "Объявить её с let static",
          "Использовать функцию set()",
          "Ничего, переменные всегда изменяемые",
        ],
        answer: 0,
        expl: "let mut x = 5; — теперь x можно присваивать новое значение.",
      },
      {
        q: "Что такое shadowing (затенение)?",
        options: [
          "Новое объявление переменной с тем же именем — старая больше недоступна",
          "Изменение значения переменной без mut",
          "Ссылка на переменную из другой функции",
          "Скрытие переменной в отладчике",
        ],
        answer: 0,
        expl: "let x = 5; let x = x + 1; — второе let создаёт новую переменную с тем же именем. Это позволяет даже сменить тип.",
      },
      {
        q: "Какой тип у числа с плавающей точкой 2.5 по умолчанию?",
        options: ["f64", "f32", "f16", "decimal"],
        answer: 0,
        expl: "По умолчанию — f64 (двойная точность), как double в других языках. f32 нужно указывать явно.",
      },
      {
        q: "if в Rust — это выражение. Что это значит на практике?",
        options: [
          "Ветку if можно использовать справа от let и получить значение",
          "if всегда возвращает true или false",
          "if нельзя использовать без else",
          "if работает только с числами",
        ],
        answer: 0,
        expl: "let x = if cond { 5 } else { 10 }; — ветки возвращают значение, поэтому точка с запятой после веток не ставится.",
      },
    ],
  },

  ...LINUX_QUIZZES,
  ...ALGO_QUIZZES,
  ...ARCH_QUIZZES,
  ...DB_QUIZZES,
  ...RUST_QUIZZES,
  ...JS_QUIZZES,
  ...DM_QUIZZES,
  ...PY_QUIZZES,
};
