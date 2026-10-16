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
import { C_QUIZZES } from "../quizzes/c.js";
import { NET_QUIZZES } from "../quizzes/networks.js";
import { VIRT_QUIZZES } from "../quizzes/virtualization.js";

export const QUIZZES = {
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
