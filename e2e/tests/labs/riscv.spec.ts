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

/* RISC-V (book 14, chapters 16 "RISC-V" and 17 "Real programs"): the program as text, a machine code listing, step-by-step RV32IM.
   A task is checked by running it; the server re-checks the solution with the same engine (riscvlab::task::verify). */

const editor = (page: Page) => page.locator(".rs-editor .rs-input");
const run = (page: Page) => page.getByRole("button", { name: "Выполнить" });
const step = (page: Page) => page.getByRole("button", { name: "Шаг ▸" });
const consoleText = (page: Page) => page.locator(".lab-console");
const leds = (page: Page) => page.getByLabel("Светодиоды").locator(".lab-led.on");

for (const chapter of RISCV_CHAPTERS) {
  const tasks = tasksOf(chapter) as LabTask<RiscvSpec>[];
  test.describe(`RISC-V, chapter ${chapter}: the reference from a draft is accepted after a run`, () => {
    for (const task of tasks) {
      test(`${task.id}: ${task.title}`, async ({ page, request, guard }) => {
        const { token } = await loginFresh(page, request, "rv");
        await putDraft(request, token, chapter, task.id, solutionText(task));
        await openTask(page, request, chapter, task.id);
        await expect(editor(page)).toHaveValue(task.spec.reference); // the draft is picked up
        await expect(page.locator(".lab-alert")).toHaveCount(0);
        expect(await statusOf(request, token, chapter, task.id)).not.toBe("ok");
        // the task data (the .data section) is shown separately and does not get into the editor
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

test.describe("RISC-V: the initial starter and wrong programs do not solve the task", () => {
  test("the starter is in the editor, a run is not accepted, the server rejects with a reason", async ({ page, request, guard }) => {
    test.setTimeout(180_000);
    const { token } = await loginFresh(page, request, "rv-starter");
    for (const chapter of RISCV_CHAPTERS) {
      for (const task of tasksOf(chapter) as LabTask<RiscvSpec>[]) {
        await test.step(`${chapter}/${task.id}`, async () => {
          const res = await putSolved(request, token, chapter, task.id, task.spec.starter);
          expect(res.status(), `server accepted the starter ${task.id}`).toBe(422);
          expect((await rejectionOf(res)).length).toBeGreaterThan(5);
          expect(await statusOf(request, token, chapter, task.id)).not.toBe("ok");
        });
      }
    }
    // in the UI: one task per chapter
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

  test("server: rejection reasons — assembler error, empty program, wrong output", async ({ page, request }) => {
    const { token } = await loginFresh(page, request, "rv-reject");
    const reason = async (chapter: number, id: string, body: string) => {
      const res = await putSolved(request, token, chapter, id, body);
      expect(res.status(), `${chapter}/${id}`).toBe(422);
      return rejectionOf(res);
    };
    expect(await reason(16, "uart-hi", "  frobnicate\n")).toBe("Строка 1: Неизвестная команда «frobnicate»");
    expect(await reason(16, "uart-hi", "")).toMatch(/Непонятная команда 0x00000000/);
    expect(await reason(17, "real-hello", "")).toMatch(/Непонятная команда 0x00000000/);
    // correct shape, wrong result
    const wrong = "  li t0, 0x10000000\n  li t1, 'X'\n  sb t1, 0(t0)\n  ebreak\n";
    expect(await reason(16, "uart-hi", wrong)).toMatch(/^В консоли "X", а ожидалось "Hi!\\n"/);
    expect((await putSolved(request, token, 16, "nope", "ebreak")).status()).toBe(404);
    const anonymous = await request.put("/api/exercises/14/16/uart-hi/solved", { data: { solution: "ebreak" } });
    expect(anonymous.status()).toBe(401);
  });
});

test("RISC-V by hand (board): program text, listing, per-line error, steps, registers, UART, memory, reset", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "rv-hand");
  const task = riscvOf(16, "uart-hi");
  await openTask(page, request, 16, task.id);

  // hint
  await page.getByRole("button", { name: "Подсказка" }).click();
  await expect(page.locator(".ex-hint")).toContainText("0x10000000");
  await page.getByRole("button", { name: "Скрыть подсказку" }).click();

  // error on a bad line: "Line N" matches the line number in the editor, running is impossible
  await editor(page).fill("  li t0, 1\n  li t1, 2\n  bogus t2\n  ebreak\n");
  await expect(page.locator(".lab-errors li")).toHaveText("Строка 3: Неизвестная команда «bogus»");
  await expect(page.getByText("Исправьте ошибки в программе")).toBeVisible();
  await expect(step(page)).toBeDisabled();
  await expect(page.locator(".lab-alert")).toHaveCount(0);

  // type the solution instead of pasting it
  await editor(page).fill("");
  await editor(page).pressSequentially(task.spec.reference);
  await expect(page.locator(".lab-errors")).toHaveCount(0);
  await expect(editor(page)).toHaveValue(task.spec.reference);

  // listing: the first instruction li t0, 0x10000000 → lui t0, 0x10000 (word 0x100002b7), the row expands into a field legend
  const first = page.locator(".lab-table tbody tr").first();
  await expect(first.locator("td").nth(1)).toHaveText("100002b7");
  await expect(first.locator("td.left").last()).toHaveText("li t0, 0x10000000");
  await first.click();
  await expect(page.locator(".lab-legend")).toContainText("Формат U.");
  await first.click();
  await expect(page.locator(".lab-legend")).toHaveCount(0);

  // Step: pc advanced, t0 got the UART address, the last instruction is shown
  await expect(page.locator(".lab-status")).toContainText("pc = 0x0000");
  await step(page).click();
  await expect(page.locator(".lab-status")).toContainText("pc = 0x0004");
  await expect(page.locator(".lab-status")).toContainText("выполнено команд: 1");
  const t0 = page.locator(".lab-reg", { has: page.locator(".lab-reg-name", { hasText: /^t0/ }) });
  await expect(t0.locator(".lab-reg-val")).toHaveText("268435456");
  await expect(t0.locator(".lab-reg-hex")).toHaveText("10000000");
  await expect(t0).toHaveClass(/changed/);
  await expect(page.locator(".lab-reg")).toHaveCount(32);

  // Run up to ebreak: the UART console, the verdict, timer = number of steps
  await run(page).click();
  await expect(consoleText(page)).toContainText("Hi!");
  await expect(page.locator(".lab-alert.ok")).toContainText("The console shows “Hi!”, all correct.");
  await expect(step(page)).toBeDisabled();
  await expect(page.locator(".lab-dev", { hasText: "Таймер" })).toContainText("10");
  await expect.poll(() => statusOf(request, token, 16, task.id)).toBe("ok");

  // memory windows: Instructions show the machine code (0x100002b7 byte by byte, little end first), Stack switches
  const windows = page.getByRole("group", { name: "Окно памяти" });
  await windows.getByRole("button", { name: /Команды/ }).click();
  await expect(page.locator(".lab-disk-row").first().locator("span").nth(1)).toHaveText("B7");
  await windows.getByRole("button", { name: /Стек/ }).click();
  await expect(windows.getByRole("button", { name: /Стек/ })).toHaveClass(/on/);

  // Reset: the machine from scratch, the same program, the verdict banner is gone
  await page.getByRole("button", { name: "Сбросить" }).click();
  await expect(page.locator(".lab-status")).toContainText("выполнено команд: 0");
  await expect(page.locator(".lab-alert")).toHaveCount(0);
  await expect(consoleText(page)).not.toContainText("Hi!");

  // Start over restores the starter; the draft lives on the server
  await page.getByRole("button", { name: "Начать заново" }).click();
  await expect(editor(page)).toHaveValue(task.spec.starter);
  await editor(page).fill("# my draft\n  ebreak\n");
  await expect.poll(async () => (await chapterState(request, token, 16)).drafts[task.id]).toBe("# my draft\n  ebreak\n");
  await page.reload();
  await expect(editor(page)).toHaveValue("# my draft\n  ebreak\n");
  guard.assertClean();
});

test("RISC-V by hand: LEDs, switches and the task data on the board", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "rv-periph");
  // LEDs: the pattern from the reference
  const leds16 = riscvOf(16, "leds");
  await putDraft(request, token, 16, leds16.id, leds16.spec.reference);
  await openTask(page, request, 16, leds16.id);
  await expect(leds(page)).toHaveCount(0);
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  expect(await leds(page).count()).toBeGreaterThan(0);

  // switches are set by the statement (0xB2): SW1, SW4, SW5, SW7 are on; the LEDs repeat their inversion
  const inv = riscvOf(16, "switches-invert");
  await putDraft(request, token, 16, inv.id, inv.spec.reference);
  await openTask(page, request, 16, inv.id);
  const lit = page.getByLabel("Переключатели").locator(".lab-led.on");
  await expect(lit).toHaveCount(4);
  await expect(lit).toHaveText(["7", "5", "4", "1"]) // lamps left to right: 7 … 0;
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  await expect(leds(page)).toHaveText(["6", "3", "2", "0"]);

  // task data and the result in memory: "risc-v is fun!" → capital letters in the data window
  const upper = riscvOf(16, "upper");
  await putDraft(request, token, 16, upper.id, upper.spec.reference);
  await openTask(page, request, 16, upper.id);
  await expect(page.locator("pre.lab-data").first()).toContainText('.asciz "risc-v is fun!"');
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  await page.getByRole("group", { name: "Окно памяти" }).getByRole("button", { name: /Данные/ }).click();
  await expect(page.locator(".lab-ascii").filter({ hasText: "RISC-V IS FUN!" })).toHaveCount(1);

  // printing a string from the task data to the console
  const str = riscvOf(16, "uart-string");
  await putDraft(request, token, 16, str.id, str.spec.reference);
  await openTask(page, request, 16, str.id);
  await run(page).click();
  await expect(consoleText(page)).toContainText("Hello, RISC-V!");
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  guard.assertClean();
});

test("RISC-V (real programs): write output, exit code, a project to build locally — zip and files", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "rv-real");
  const hello = riscvOf(17, "real-hello");
  await putDraft(request, token, 17, hello.id, hello.spec.reference);
  await openTask(page, request, 17, hello.id);
  await expect(page.getByRole("heading", { name: "Вывод программы" })).toBeVisible();
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  await expect(consoleText(page)).toContainText("Hello");
  await expect(page.locator(".lab-exit")).toContainText("0"); // exit code

  // the Build locally card: three project files, switching, downloading the archive and one file
  const files = page.getByRole("group", { name: "Файлы проекта" });
  await expect(files.getByRole("button")).toHaveText(["program.s", "Makefile", "README.md"]);
  await expect(page.locator("pre.lab-file")).toContainText("_start");
  await files.getByRole("button", { name: "Makefile" }).click();
  await expect(page.locator("pre.lab-file")).toContainText("riscv");
  const [zip] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: "Скачать проект (.zip)" }).click()]);
  expect(zip.suggestedFilename()).toBe("riscv-program.zip");
  const path = await zip.path();
  const bytes = readFileSync(path);
  expect(bytes.subarray(0, 4).toString("hex")).toBe("504b0304"); // zip signature
  const text = bytes.toString("latin1");
  for (const name of ["program.s", "Makefile", "README.md"]) expect(text).toContain(name);
  const [one] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: "Скачать Makefile" }).click()]);
  expect(one.suggestedFilename()).toMatch(/^Makefile(\.txt)?$/); // Chromium appends .txt to a name without an extension

  // for tasks with an exit code (vowels) the code is shown after the run
  const exit = riscvOf(17, "real-exit-code");
  await putDraft(request, token, 17, exit.id, exit.spec.reference);
  await openTask(page, request, 17, exit.id);
  await expect(page.locator(".lab-exit")).toHaveCount(0);
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toBeVisible();
  await expect(page.locator(".lab-exit")).toBeVisible();
  guard.assertClean();
});

test("RISC-V: the server accepts a hand-typed solution of one task, then moving to the next one is available", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "rv-solve");
  const first = riscvOf(16, "uart-hi");
  await openTask(page, request, 16, first.id);
  await editor(page).fill("");
  await editor(page).pressSequentially("  li t0, 0x10000000\n  li t1, 'H'\n  sb t1, 0(t0)\n  li t1, 'i'\n  sb t1, 0(t0)\n  li t1, '!'\n  sb t1, 0(t0)\n  li t1, 10\n  sb t1, 0(t0)\n  ebreak\n");
  await page.getByRole("button", { name: "Выполнить" }).click();
  await expect(page.locator(".lab-alert.ok")).toContainText("Hi!");
  await expect.poll(() => statusOf(request, token, 16, first.id)).toBe("ok");
  await expect(page.locator(".pr-top-label").first()).toHaveText("Решено 1 из 9");
  // Next opens the next exercise of the chapter
  await page.getByRole("button", { name: "Дальше" }).click();
  await expect(page.locator(".pr-head h3")).toContainText(tasksOf(16)[1]!.title);
  guard.assertClean();
});
