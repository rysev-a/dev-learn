import { readFileSync } from "node:fs";
import type { Page } from "@playwright/test";
import {
  chapterState,
  listItem,
  openTask,
  putDraft,
  putSolved,
  rejectionOf,
  riscvOf,
  RISCV_CHAPTERS,
  solutionText,
  statusOf,
  tasksOf,
  type LabTask,
  type RiscvSpec,
} from "../../support/arch";
import { expect, loginFresh, test } from "../../support/fixtures";

/* RISC-V (книга 14, главы 16 «RISC-V» и 17 «Настоящие программы»): программа текстом, листинг машинного кода, пошаговый RV32IM.
   Задача проверяется запуском; решение перепроверяет сервер тем же движком (riscvlab::task::verify). */

const editor = (page: Page) => page.locator(".rs-editor .rs-input");
const run = (page: Page) => page.getByRole("button", { name: "Выполнить" });
const step = (page: Page) => page.getByRole("button", { name: "Шаг ▸" });
const consoleText = (page: Page) => page.locator(".lab-console");
const leds = (page: Page) => page.getByLabel("Светодиоды").locator(".lab-led.on");

for (const chapter of RISCV_CHAPTERS) {
  const tasks = tasksOf(chapter) as LabTask<RiscvSpec>[];
  test.describe(`RISC-V, глава ${chapter}: эталон из черновика засчитывается после запуска`, () => {
    for (const task of tasks) {
      test(`${task.id}: ${task.title}`, async ({ page, request, guard }) => {
        const { token } = await loginFresh(page, request, "rv");
        await putDraft(request, token, chapter, task.id, solutionText(task));
        await openTask(page, request, chapter, task.id);
        await expect(editor(page)).toHaveValue(task.spec.reference); // черновик подхвачен
        await expect(page.locator(".lab-alert")).toHaveCount(0);
        expect(await statusOf(request, token, chapter, task.id)).not.toBe("ok");
        // данные задания (секция .data) показаны отдельно и в редактор не попадают
        if (task.spec.data.trim()) await expect(page.locator("pre.lab-data").first()).toContainText(task.spec.data.trim().split("\n")[0]!);

        await run(page).click();
        await expect(page.locator(".lab-alert.ok .lab-alert-title")).toHaveText("Задание выполнено!");
        await expect(page.locator(".lab-status")).toContainText("остановлен");
        await expect(listItem(page, task.title)).toHaveClass(/\bok\b/);
        await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
        await expect(page.locator("p.error")).toHaveCount(0);
        await expect.poll(() => statusOf(request, token, chapter, task.id)).toBe("ok");
        guard.assertClean();
      });
    }
  });
}

test.describe("RISC-V: исходная заготовка и неверные программы не решают задачу", () => {
  test("заготовка в редакторе, запуск не засчитывается, сервер отвечает отказом с причиной", async ({ page, request, guard }) => {
    test.setTimeout(180_000);
    const { token } = await loginFresh(page, request, "rv-starter");
    for (const chapter of RISCV_CHAPTERS) {
      for (const task of tasksOf(chapter) as LabTask<RiscvSpec>[]) {
        await test.step(`${chapter}/${task.id}`, async () => {
          const res = await putSolved(request, token, chapter, task.id, task.spec.starter);
          expect(res.status(), `сервер принял заготовку ${task.id}`).toBe(422);
          expect((await rejectionOf(res)).length).toBeGreaterThan(5);
          expect(await statusOf(request, token, chapter, task.id)).not.toBe("ok");
        });
      }
    }
    // в интерфейсе: по одной задаче каждой главы
    for (const [chapter, id] of [[16, "uart-hi"], [16, "sum-100"], [17, "real-hello"]] as const) {
      const task = riscvOf(chapter, id);
      await openTask(page, request, chapter, id);
      await expect(editor(page)).toHaveValue(task.spec.starter);
      await run(page).click();
      await expect(page.locator(".lab-alert.bad .lab-alert-title")).toHaveText("Пока не то");
      await expect(page.locator(".lab-alert.ok")).toHaveCount(0);
      await expect(listItem(page, task.title)).not.toHaveClass(/\bok\b/);
    }
    guard.assertClean();
  });

  test("сервер: причины отказа — ошибка ассемблера, пустая программа, не тот вывод", async ({ page, request }) => {
    const { token } = await loginFresh(page, request, "rv-reject");
    const reason = async (chapter: number, id: string, body: string) => {
      const res = await putSolved(request, token, chapter, id, body);
      expect(res.status(), `${chapter}/${id}`).toBe(422);
      return rejectionOf(res);
    };
    expect(await reason(16, "uart-hi", "  frobnicate\n")).toBe("Строка 1: Неизвестная команда «frobnicate»");
    expect(await reason(16, "uart-hi", "")).toMatch(/Непонятная команда 0x00000000/);
    expect(await reason(17, "real-hello", "")).toMatch(/Непонятная команда 0x00000000/);
    // правильная форма, неверный результат
    const wrong = "  li t0, 0x10000000\n  li t1, 'X'\n  sb t1, 0(t0)\n  ebreak\n";
    expect(await reason(16, "uart-hi", wrong)).toMatch(/^В консоли "X", а ожидалось "Hi!\\n"/);
    expect((await putSolved(request, token, 16, "nope", "ebreak")).status()).toBe(404);
    const anonymous = await request.put("/api/exercises/14/16/uart-hi/solved", { data: { solution: "ebreak" } });
    expect(anonymous.status()).toBe(401);
  });
});

test("RISC-V вручную (плата): текст программы, листинг, ошибка по строке, шаги, регистры, UART, память, сброс", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "rv-hand");
  const task = riscvOf(16, "uart-hi");
  await openTask(page, request, 16, task.id);

  // подсказка
  await page.getByRole("button", { name: "Подсказка" }).click();
  await expect(page.locator(".ex-hint")).toContainText("0x10000000");
  await page.getByRole("button", { name: "Скрыть подсказку" }).click();

  // ошибка на плохой строке: «Строка N» совпадает с номером строки в редакторе, запустить нельзя
  await editor(page).fill("  li t0, 1\n  li t1, 2\n  bogus t2\n  ebreak\n");
  await expect(page.locator(".lab-errors li")).toHaveText("Строка 3: Неизвестная команда «bogus»");
  await expect(page.getByText("Исправьте ошибки в программе")).toBeVisible();
  await expect(step(page)).toBeDisabled();
  await expect(page.locator(".lab-alert")).toHaveCount(0);

  // вводим решение печатью, а не вставкой
  await editor(page).fill("");
  await editor(page).pressSequentially(task.spec.reference);
  await expect(page.locator(".lab-errors")).toHaveCount(0);
  await expect(editor(page)).toHaveValue(task.spec.reference);

  // листинг: первая команда li t0, 0x10000000 → lui t0, 0x10000 (слово 0x100002b7), строка раскрывается легендой полей
  const first = page.locator(".lab-table tbody tr").first();
  await expect(first.locator("td").nth(1)).toHaveText("100002b7");
  await expect(first.locator("td.left").last()).toHaveText("li t0, 0x10000000");
  await first.click();
  await expect(page.locator(".lab-legend")).toContainText("Формат U.");
  await first.click();
  await expect(page.locator(".lab-legend")).toHaveCount(0);

  // «Шаг»: pc сдвинулся, t0 получил адрес UART, последняя команда показана
  await expect(page.locator(".lab-status")).toContainText("pc = 0x0000");
  await step(page).click();
  await expect(page.locator(".lab-status")).toContainText("pc = 0x0004");
  await expect(page.locator(".lab-status")).toContainText("выполнено команд: 1");
  const t0 = page.locator(".lab-reg", { has: page.locator(".lab-reg-name", { hasText: /^t0/ }) });
  await expect(t0.locator(".lab-reg-val")).toHaveText("268435456");
  await expect(t0.locator(".lab-reg-hex")).toHaveText("10000000");
  await expect(t0).toHaveClass(/changed/);
  await expect(page.locator(".lab-reg")).toHaveCount(32);

  // «Выполнить» до ebreak: консоль UART, итог, таймер = число шагов
  await run(page).click();
  await expect(consoleText(page)).toContainText("Hi!");
  await expect(page.locator(".lab-alert.ok")).toContainText("В консоли «Hi!» — всё верно.");
  await expect(step(page)).toBeDisabled();
  await expect(page.locator(".lab-dev", { hasText: "Таймер" })).toContainText("10");
  await expect.poll(() => statusOf(request, token, 16, task.id)).toBe("ok");

  // окна памяти: «Команды» показывают машинный код (0x100002b7 по байтам, младшим вперёд), «Стек» — переключается
  const windows = page.getByRole("group", { name: "Окно памяти" });
  await windows.getByRole("button", { name: /Команды/ }).click();
  await expect(page.locator(".lab-disk-row").first().locator("span").nth(1)).toHaveText("B7");
  await windows.getByRole("button", { name: /Стек/ }).click();
  await expect(windows.getByRole("button", { name: /Стек/ })).toHaveClass(/on/);

  // «Сбросить»: машина с нуля, программа та же, плашка итога исчезла
  await page.getByRole("button", { name: "Сбросить" }).click();
  await expect(page.locator(".lab-status")).toContainText("выполнено команд: 0");
  await expect(page.locator(".lab-alert")).toHaveCount(0);
  await expect(consoleText(page)).not.toContainText("Hi!");

  // «Начать заново» возвращает заготовку; черновик живёт на сервере
  await page.getByRole("button", { name: "Начать заново" }).click();
  await expect(editor(page)).toHaveValue(task.spec.starter);
  await editor(page).fill("# мой черновик\n  ebreak\n");
  await expect.poll(async () => (await chapterState(request, token, 16)).drafts[task.id]).toBe("# мой черновик\n  ebreak\n");
  await page.reload();
  await expect(editor(page)).toHaveValue("# мой черновик\n  ebreak\n");
  guard.assertClean();
});

test("RISC-V вручную: светодиоды, переключатели и данные задания на плате", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "rv-periph");
  // светодиоды: узор из эталона
  const leds16 = riscvOf(16, "leds");
  await putDraft(request, token, 16, leds16.id, leds16.spec.reference);
  await openTask(page, request, 16, leds16.id);
  await expect(leds(page)).toHaveCount(0);
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  expect(await leds(page).count()).toBeGreaterThan(0);

  // переключатели заданы условием (0xB2): горят SW1, SW4, SW5, SW7; светодиоды повторяют их инверсию
  const inv = riscvOf(16, "switches-invert");
  await putDraft(request, token, 16, inv.id, inv.spec.reference);
  await openTask(page, request, 16, inv.id);
  const lit = page.getByLabel("Переключатели").locator(".lab-led.on");
  await expect(lit).toHaveCount(4);
  await expect(lit).toHaveText(["7", "5", "4", "1"]) // лампочки слева направо: 7 … 0;
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  await expect(leds(page)).toHaveText(["6", "3", "2", "0"]);

  // данные задания и результат в памяти: «risc-v is fun!» → заглавные буквы в окне данных
  const upper = riscvOf(16, "upper");
  await putDraft(request, token, 16, upper.id, upper.spec.reference);
  await openTask(page, request, 16, upper.id);
  await expect(page.locator("pre.lab-data").first()).toContainText('.asciz "risc-v is fun!"');
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  await page.getByRole("group", { name: "Окно памяти" }).getByRole("button", { name: /Данные/ }).click();
  await expect(page.locator(".lab-ascii").filter({ hasText: "RISC-V IS FUN!" })).toHaveCount(1);

  // вывод строки из данных задания в консоль
  const str = riscvOf(16, "uart-string");
  await putDraft(request, token, 16, str.id, str.spec.reference);
  await openTask(page, request, 16, str.id);
  await run(page).click();
  await expect(consoleText(page)).toContainText("Hello, RISC-V!");
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  guard.assertClean();
});

test("RISC-V («настоящие программы»): вывод write, код возврата, проект для сборки у себя — zip и файлы", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "rv-real");
  const hello = riscvOf(17, "real-hello");
  await putDraft(request, token, 17, hello.id, hello.spec.reference);
  await openTask(page, request, 17, hello.id);
  await expect(page.getByRole("heading", { name: "Вывод программы" })).toBeVisible();
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  await expect(consoleText(page)).toContainText("Hello");
  await expect(page.locator(".lab-exit")).toContainText("0"); // код возврата

  // карточка «Собрать у себя»: три файла проекта, переключение, скачивание архива и одного файла
  const files = page.getByRole("group", { name: "Файлы проекта" });
  await expect(files.getByRole("button")).toHaveText(["program.s", "Makefile", "README.md"]);
  await expect(page.locator("pre.lab-file")).toContainText("_start");
  await files.getByRole("button", { name: "Makefile" }).click();
  await expect(page.locator("pre.lab-file")).toContainText("riscv");
  const [zip] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: "Скачать проект (.zip)" }).click()]);
  expect(zip.suggestedFilename()).toBe("riscv-program.zip");
  const path = await zip.path();
  const bytes = readFileSync(path);
  expect(bytes.subarray(0, 4).toString("hex")).toBe("504b0304"); // сигнатура zip
  const text = bytes.toString("latin1");
  for (const name of ["program.s", "Makefile", "README.md"]) expect(text).toContain(name);
  const [one] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: "Скачать Makefile" }).click()]);
  expect(one.suggestedFilename()).toMatch(/^Makefile(\.txt)?$/); // Chromium дописывает .txt к имени без расширения

  // у задач с кодом возврата (гласные) код показывается после выполнения
  const exit = riscvOf(17, "real-exit-code");
  await putDraft(request, token, 17, exit.id, exit.spec.reference);
  await openTask(page, request, 17, exit.id);
  await expect(page.locator(".lab-exit")).toHaveCount(0);
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  await expect(page.locator(".lab-exit")).toBeVisible();
  guard.assertClean();
});

test("RISC-V: решение руками (печатью) одной задачи принимает сервер, затем доступен переход к следующей", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "rv-solve");
  const first = riscvOf(16, "uart-hi");
  await openTask(page, request, 16, first.id);
  await editor(page).fill("");
  await editor(page).pressSequentially("  li t0, 0x10000000\n  li t1, 'H'\n  sb t1, 0(t0)\n  li t1, 'i'\n  sb t1, 0(t0)\n  li t1, '!'\n  sb t1, 0(t0)\n  li t1, 10\n  sb t1, 0(t0)\n  ebreak\n");
  await page.getByRole("button", { name: "Выполнить" }).click();
  await expect(page.locator(".lab-alert.ok")).toContainText("Hi!");
  await expect.poll(() => statusOf(request, token, 16, first.id)).toBe("ok");
  await expect(page.locator(".pr-top-label").first()).toHaveText("Решено 1 из 9");
  // «Дальше» открывает следующее упражнение главы
  await page.getByRole("button", { name: "Дальше" }).click();
  await expect(page.locator(".pr-head h3")).toContainText(tasksOf(16)[1]!.title);
  guard.assertClean();
});
