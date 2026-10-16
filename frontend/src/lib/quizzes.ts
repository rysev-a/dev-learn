// Реестр квизов: ключ «bookId:номер_главы» → квиз на теорию
// (вопросы с вариантами, проверка сразу при выборе).
import type { Quiz } from "../types.ts";
import { ALGO_QUIZZES } from "../quizzes/algo.ts";
import { ARCH_QUIZZES } from "../quizzes/arch.ts";
import { DB_QUIZZES } from "../quizzes/db.ts";
import { DM_QUIZZES } from "../quizzes/dm.ts";
import { JS_QUIZZES } from "../quizzes/js.ts";
import { LINUX_QUIZZES } from "../quizzes/linux.ts";
import { PY_QUIZZES } from "../quizzes/py.ts";
import { RUST_QUIZZES } from "../quizzes/rust.ts";
import { C_QUIZZES } from "../quizzes/c.ts";
import { NET_QUIZZES } from "../quizzes/networks.ts";
import { VIRT_QUIZZES } from "../quizzes/virtualization.ts";

export const QUIZZES: Record<string, Quiz> = {
  ...LINUX_QUIZZES,
  ...ALGO_QUIZZES,
  ...ARCH_QUIZZES,
  ...DB_QUIZZES,
  ...RUST_QUIZZES,
  ...C_QUIZZES,
  ...NET_QUIZZES,
  ...VIRT_QUIZZES,
  ...JS_QUIZZES,
  ...DM_QUIZZES,
  ...PY_QUIZZES,
};
