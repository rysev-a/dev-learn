import type { Page } from "@playwright/test";
import { asmOf, chapterState, listItem, openTask, putDraft, putSolved, rejectionOf, solutionText, statusOf, tasksOf, type AsmSpec, type LabTask } from "../../support/arch";
import { expect, loginFresh, test } from "../../support/fixtures";

/* Ассемблер Мини-8 (книга 14, глава 15): 8 задач на виртуальном диске. Программа — текст в редакторе, проверка — после hlt:
   диск сверяется с ожидаемым. Решение перепроверяет сервер тем же движком. */

const CHAPTER = 15;
const tasks = tasksOf(CHAPTER) as LabTask<AsmSpec>[];

const editor = (page: Page) => page.getByRole("textbox", { name: "Текст программы на ассемблере" });
const run = (page: Page) => page.getByRole("button", { name: "Выполнить" });
const step = (page: Page) => page.getByRole("button", { name: "Шаг ▸" });
const status = (page: Page) => page.locator(".lab-status");

test.describe("Мини-8: эталон из черновика засчитывается после запуска", () => {
  for (const task of tasks) {
    test(`${task.id}: ${task.title}`, async ({ page, request, guard }) => {
      const { token } = await loginFresh(page, request, "asm");
      await putDraft(request, token, CHAPTER, task.id, solutionText(task));
      await openTask(page, request, CHAPTER, task.id);
      // черновик подхвачен редактором; до запуска ничего не засчитано
      await expect(editor(page)).toHaveValue(task.spec.solution);
      await expect(page.locator(".lab-alert")).toHaveCount(0);
      expect(await statusOf(request, token, CHAPTER, task.id)).not.toBe("ok");
      // области диска из условия показаны чипами
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

test.describe("Мини-8: исходная заготовка не решает задачу", () => {
  test("заготовка в редакторе, запуск даёт «Пока не то», сервер не засчитывает", async ({ page, request, guard }) => {
    const { token } = await loginFresh(page, request, "asm-starter");
    for (const task of tasks) {
      await test.step(`${task.id}: заготовка`, async () => {
        await openTask(page, request, CHAPTER, task.id);
        await expect(editor(page)).toHaveValue(task.spec.starter);
        await run(page).click();
        await expect(page.locator(".lab-alert.bad .lab-alert-title")).toHaveText("Пока не то");
        await expect(page.locator(".lab-alert.ok")).toHaveCount(0);
        await expect(listItem(page, task.title)).not.toHaveClass(/\bok\b/);
        expect(await statusOf(request, token, CHAPTER, task.id)).not.toBe("ok");
        const res = await putSolved(request, token, CHAPTER, task.id, task.spec.starter);
        expect(res.status(), `сервер принял заготовку ${task.id}`).toBe(422);
        expect((await rejectionOf(res)).length).toBeGreaterThan(5);
      });
    }
    guard.assertClean();
  });

  test("сервер: причины отказа — пустая программа, ошибка ассемблера, не тот диск", async ({ page, request }) => {
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
    // чужая задача книги
    expect((await putSolved(request, token, CHAPTER, "nope", "hlt")).status()).toBe(404);
  });
});

test("Мини-8 вручную: программа в редакторе, машинный код, шаги, регистры, диск, переключатель процессора, ошибки", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "asm-hand");
  const task = asmOf(CHAPTER, "patch-byte");
  await openTask(page, request, CHAPTER, task.id);

  // подсказка
  await page.getByRole("button", { name: "Подсказка" }).click();
  await expect(page.locator(".ex-hint")).toContainText(task.hint.slice(0, 25));
  await page.getByRole("button", { name: "Скрыть подсказку" }).click();
  await expect(page.locator(".ex-hint")).toHaveCount(0);

  // вводим программу руками
  await editor(page).fill("  li   r1, 'J'\n  li   r2, 0x10\n  sb   r1, 0(r2)\n  hlt\n");
  // листинг: машинное слово первой команды li r1, 'J' и разбор по полям
  const firstRow = page.locator(".lab-table tbody tr").first();
  await expect(firstRow.locator("td").nth(1)).toHaveText("124a");
  await expect(firstRow.locator("td.left")).toHaveText("li r1, 'J'");
  await firstRow.click();
  await expect(page.locator(".lab-explain")).toContainText("код операции");

  // процессор в начале: следующая команда 0, шагов 0, регистры r0…r7
  await expect(status(page)).toContainText("следующая команда: 0");
  await expect(page.locator(".lab-reg")).toHaveCount(8);

  // «Шаг»: r1 = 74 (0x4A), счётчик команд сдвинулся
  await step(page).click();
  await expect(status(page)).toContainText("следующая команда: 1");
  await expect(status(page)).toContainText("выполнено шагов: 1");
  const r1 = page.locator(".lab-reg", { has: page.locator(".lab-reg-name", { hasText: /^r1$/ }) });
  await expect(r1.locator(".lab-reg-val")).toHaveText("74");
  await expect(r1.locator(".lab-reg-hex")).toHaveText("0x4A");
  await expect(r1).toHaveClass(/changed/);
  await expect(page.locator(".lab-alert")).toHaveCount(0); // программа ещё не остановилась

  // два шага до записи на диск: подсвечен записанный байт 0x10
  await step(page).click();
  await step(page).click();
  const written = page.locator(".lab-cell.written");
  await expect(written).toHaveText("4A");
  await expect(written).toHaveAttribute("title", "адрес 0x10");
  await expect(page.locator(".lab-disk-row").nth(1).locator(".lab-ascii")).toContainText("Jello");

  // «Выполнить» доводит до hlt: задание выполнено, шаги заблокированы
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toContainText("Задание выполнено!");
  await expect(status(page)).toContainText("остановлен (hlt)");
  await expect(step(page)).toBeDisabled();
  await expect(run(page)).toBeDisabled();
  await expect(page.locator(".lab-cell.changed")).toHaveText(["4A"]); // от исходного диска отличается один байт
  await expect.poll(() => statusOf(request, token, CHAPTER, task.id)).toBe("ok");

  // «Сбросить»: машина с нуля, диск исходный; программа остаётся
  await page.getByRole("button", { name: "Сбросить" }).click();
  await expect(status(page)).toContainText("выполнено шагов: 0");
  await expect(page.locator(".lab-cell.changed")).toHaveCount(0);
  await expect(editor(page)).toHaveValue(/li\s+r1, 'J'/);

  // тот же процессор из вентилей выполняет программу так же; показывается его устройство
  await page.getByRole("button", { name: "Схема из вентилей" }).click();
  await expect(page.getByText("Устройство процессора")).toBeVisible();
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toContainText("Задание выполнено!");
  await page.getByRole("button", { name: "Эмулятор" }).click();
  await expect(page.getByText("Устройство процессора")).toHaveCount(0);

  // ошибка ассемблера: номер строки и причина, запустить нельзя
  await editor(page).fill("li r1, 1\nzzz r2\nhlt");
  await expect(page.locator(".lab-errors li")).toHaveText("Строка 2: Неизвестная команда «zzz»");
  await expect(step(page)).toBeDisabled();
  await expect(page.getByText("Исправьте ошибки в программе")).toBeVisible();
  await expect(page.locator(".lab-alert")).toHaveCount(0);

  // «Начать заново» возвращает заготовку; черновик сохранён на сервере и переживает перезагрузку
  await page.getByRole("button", { name: "Начать заново" }).click();
  await expect(editor(page)).toHaveValue(task.spec.starter);
  await editor(page).fill("; мой черновик\n  hlt\n");
  await expect.poll(async () => (await chapterState(request, token, CHAPTER)).drafts[task.id]).toBe("; мой черновик\n  hlt\n");
  await page.reload();
  await expect(editor(page)).toHaveValue("; мой черновик\n  hlt\n");
  guard.assertClean();
});

test("Мини-8: решение руками одной простой задачи принимает сервер, затем доступен переход к следующей", async ({ page, request, guard }) => {
  const { token } = await loginFresh(page, request, "asm-solve");
  const task = asmOf(CHAPTER, "patch-byte");
  await openTask(page, request, CHAPTER, task.id);
  await editor(page).fill("  li r1, 'J'\n  li r2, 0x10\n  sb r1, 0(r2)\n  hlt\n");
  await run(page).click();
  await expect(page.locator(".lab-alert.ok")).toContainText("Диск совпал с ожидаемым");
  await expect.poll(() => statusOf(request, token, CHAPTER, task.id)).toBe("ok");
  await expect(page.locator(".pr-top-label").first()).toHaveText("Решено 1 из 8");
  // «Дальше» открывает следующее упражнение
  await page.getByRole("button", { name: "Дальше" }).click();
  await expect(page.locator(".pr-head h3")).toContainText(tasks[1]!.title);
  guard.assertClean();
});
