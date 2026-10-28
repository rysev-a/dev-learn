import type { Page } from "@playwright/test";
import { asmOf, chapterState, listItem, openTask, putDraft, putSolved, rejectionOf, solutionText, statusOf, tasksOf, type AsmSpec, type LabTask } from "../../support/arch";
import { expect, loginFresh, test } from "../../support/fixtures";

/* Mini-8 assembler (book 14, chapter 15): 8 tasks on a virtual disk. The program is text in the editor, the check runs after hlt:
   the disk is compared with the expected one. The server re-checks the solution with the same engine. */

const CHAPTER = 15;
const tasks = tasksOf(CHAPTER) as LabTask<AsmSpec>[];

const editor = (page: Page) => page.getByRole("textbox", { name: "Текст программы на ассемблере" });
const run = (page: Page) => page.getByRole("button", { name: "Выполнить" });
const step = (page: Page) => page.getByRole("button", { name: "Шаг ▸" });
const status = (page: Page) => page.locator(".lab-status");

test.describe("Mini-8: the reference from a draft is accepted after a run", () => {
  for (const task of tasks) {
    test(`${task.id}: ${task.title}`, async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "asm");
      await putDraft(request, token, CHAPTER, task.id, solutionText(task));
      await openTask(page, request, CHAPTER, task.id);
      // the draft is picked up by the editor; nothing is accepted before a run
      await expect(editor(page)).toHaveValue(task.spec.solution);
      await expect(page.locator(".lab-alert")).toHaveCount(0);
      expect(await statusOf(request, token, CHAPTER, task.id)).not.toBe("ok");
      // disk areas from the statement are shown as chips
      await expect(page.locator(".lab-region")).toHaveCount(task.spec.regions.length);

      await run(page).click();
      await expect(page.locator(".lab-alert.ok .lab-alert-title")).toHaveText("Задание выполнено!");
      await expect(status(page)).toContainText("остановлен (hlt)");
      await expect(listItem(page, task.title)).toHaveClass(/\bok\b/);
      await expect(page.locator(".pr-head .pr-badge")).toHaveText("выполнено");
      await expect(page.locator("p.error")).toHaveCount(0);
      await expect.poll(() => statusOf(request, token, CHAPTER, task.id)).toBe("ok");
      guard.assertClean();
    });
  }
});

test.describe("Mini-8: the initial starter does not solve the task", () => {
  test("the starter is in the editor, a run gives \"not yet\", the server does not accept it", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "asm-starter");
    for (const task of tasks) {
      await test.step(`${task.id}: starter`, async () => {
        await openTask(page, request, CHAPTER, task.id);
        await expect(editor(page)).toHaveValue(task.spec.starter);
        await run(page).click();
        await expect(page.locator(".lab-alert.bad .lab-alert-title")).toHaveText("Пока не то");
        await expect(page.locator(".lab-alert.ok")).toHaveCount(0);
        await expect(listItem(page, task.title)).not.toHaveClass(/\bok\b/);
        expect(await statusOf(request, token, CHAPTER, task.id)).not.toBe("ok");
        const res = await putSolved(request, token, CHAPTER, task.id, task.spec.starter);
        expect(res.status(), `server accepted the starter ${task.id}`).toBe(422);
        expect((await rejectionOf(res)).length).toBeGreaterThan(5);
      });
    }
    guard.assertClean();
  });

  test("server: rejection reasons — empty program, assembler error, wrong disk", async ({ page, request }) => {
    const { token } = await loginFresh(page, request, "asm-reject");
    const reason = async (body: string) => {
      const res = await putSolved(request, token, CHAPTER, "patch-byte", body);
      expect(res.status()).toBe(422);
      return rejectionOf(res);
    };
    expect(await reason("")).toMatch(/Счётчик команд вышел за пределы программы/);
    expect(await reason("bogus r1\n")).toBe("Строка 1: Неизвестная команда «bogus»");
    expect(await reason("  li r1, 'K'\n  li r2, 0x10\n  sb r1, 0(r2)\n  hlt\n")).toMatch(/Адрес 0x10: ожидалось 0x4A «J», а лежит 0x4B «K»/);
    expect(await reason("  hlt\n")).toMatch(/Адрес 0x10: ожидалось 0x4A «J», а лежит 0x48 «H»/);
    // someone else's task of the book
    expect((await putSolved(request, token, CHAPTER, "nope", "hlt")).status()).toBe(404);
  });
});

test("Mini-8 by hand: program in the editor, machine code, steps, registers, disk, processor switch, errors", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "asm-hand");
  const task = asmOf(CHAPTER, "patch-byte");
  await openTask(page, request, CHAPTER, task.id);

  // hint
  await page.getByRole("button", { name: "Подсказка" }).click();
  await expect(page.locator(".ex-hint")).toContainText(task.hint.slice(0, 25));
  await page.getByRole("button", { name: "Скрыть подсказку" }).click();
  await expect(page.locator(".ex-hint")).toHaveCount(0);

  // type the program by hand
  await editor(page).fill("  li   r1, 'J'\n  li   r2, 0x10\n  sb   r1, 0(r2)\n  hlt\n");
  // listing: the machine word of the first instruction li r1, 'J' and its field breakdown
  const firstRow = page.locator(".lab-table tbody tr").first();
  await expect(firstRow.locator("td").nth(1)).toHaveText("124a");
  await expect(firstRow.locator("td.left")).toHaveText("li r1, 'J'");
  await firstRow.click();
  await expect(page.locator(".lab-explain")).toContainText("код операции");

  // processor at the start: next instruction 0, steps 0, registers r0…r7
  await expect(status(page)).toContainText("следующая команда: 0");
  await expect(page.locator(".lab-reg")).toHaveCount(8);

  // Step: r1 = 74 (0x4A), the program counter advanced
  await step(page).click();
  await expect(status(page)).toContainText("следующая команда: 1");
  await expect(status(page)).toContainText("выполнено шагов: 1");
  const r1 = page.locator(".lab-reg", { has: page.locator(".lab-reg-name", { hasText: /^r1$/ }) });
  await expect(r1.locator(".lab-reg-val")).toHaveText("74");
  await expect(r1.locator(".lab-reg-hex")).toHaveText("0x4A");
  await expect(r1).toHaveClass(/changed/);
  await expect(page.locator(".lab-alert")).toHaveCount(0); // the program has not stopped yet

  // two steps until the disk write: the written byte 0x10 is highlighted
  await step(page).click();
  await step(page).click();
  const written = page.locator(".lab-cell.written");
  await expect(written).toHaveText("4A");
  await expect(written).toHaveAttribute("title", "адрес 0x10");
  await expect(page.locator(".lab-disk-row").nth(1).locator(".lab-ascii")).toContainText("Jello");

  // Run goes up to hlt: the task is done, steps are disabled
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toContainText("Задание выполнено!");
  await expect(status(page)).toContainText("остановлен (hlt)");
  await expect(step(page)).toBeDisabled();
  await expect(run(page)).toBeDisabled();
  await expect(page.locator(".lab-cell.changed")).toHaveText(["4A"]); // one byte differs from the initial disk
  await expect.poll(() => statusOf(request, token, CHAPTER, task.id)).toBe("ok");

  // Reset: the machine from scratch, the initial disk; the program stays
  await page.getByRole("button", { name: "Сбросить" }).click();
  await expect(status(page)).toContainText("выполнено шагов: 0");
  await expect(page.locator(".lab-cell.changed")).toHaveCount(0);
  await expect(editor(page)).toHaveValue(/li\s+r1, 'J'/);

  // the same gate-level processor runs the program the same way; its structure is shown
  await page.getByRole("button", { name: "Схема из вентилей" }).click();
  await expect(page.getByText("Устройство процессора")).toBeVisible();
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toContainText("Задание выполнено!");
  await page.getByRole("button", { name: "Эмулятор" }).click();
  await expect(page.getByText("Устройство процессора")).toHaveCount(0);

  // assembler error: line number and reason, running is impossible
  await editor(page).fill("li r1, 1\nzzz r2\nhlt");
  await expect(page.locator(".lab-errors li")).toHaveText("Строка 2: Неизвестная команда «zzz»");
  await expect(step(page)).toBeDisabled();
  await expect(page.getByText("Исправьте ошибки в программе")).toBeVisible();
  await expect(page.locator(".lab-alert")).toHaveCount(0);

  // Start over restores the starter; the draft is saved on the server and survives a reload
  await page.getByRole("button", { name: "Начать заново" }).click();
  await expect(editor(page)).toHaveValue(task.spec.starter);
  await editor(page).fill("; my draft\n  hlt\n");
  await expect.poll(async () => (await chapterState(request, token, CHAPTER)).drafts[task.id]).toBe("; my draft\n  hlt\n");
  await page.reload();
  await expect(editor(page)).toHaveValue("; my draft\n  hlt\n");
  guard.assertClean();
});

test("Mini-8: the server accepts a hand-made solution of one simple task, then moving to the next one is available", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "asm-solve");
  const task = asmOf(CHAPTER, "patch-byte");
  await openTask(page, request, CHAPTER, task.id);
  await editor(page).fill("  li r1, 'J'\n  li r2, 0x10\n  sb r1, 0(r2)\n  hlt\n");
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toContainText("Диск совпал с ожидаемым");
  await expect.poll(() => statusOf(request, token, CHAPTER, task.id)).toBe("ok");
  await expect(page.locator(".pr-top-label").first()).toHaveText("Решено 1 из 8");
  // Next opens the next exercise
  await page.getByRole("button", { name: "Дальше" }).click();
  await expect(page.locator(".pr-head h3")).toContainText(tasks[1]!.title);
  guard.assertClean();
});
