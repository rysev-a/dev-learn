// Исходники квизов на теорию: ключ «bookId:номер_главы» → квиз. В приложение они не попадают: `npm run quizzes:export`
// превращает их в SQL-файлы backend/app/data/sql/quizzes, а сервер отдаёт вопросы без ответов.
import type { Quiz } from "./types.ts";
import { ALGO_QUIZZES } from "./algo.ts";
import { ARCH_QUIZZES } from "./arch.ts";
import { DB_QUIZZES } from "./db.ts";
import { DM_QUIZZES } from "./dm.ts";
import { JS_QUIZZES } from "./js.ts";
import { LINUX_QUIZZES } from "./linux.ts";
import { PY_QUIZZES } from "./py.ts";
import { RUST_QUIZZES } from "./rust.ts";
import { C_QUIZZES } from "./c.ts";
import { NET_QUIZZES } from "./networks.ts";
import { VIRT_QUIZZES } from "./virtualization.ts";

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
