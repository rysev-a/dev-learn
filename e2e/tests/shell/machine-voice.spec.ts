import fs from "node:fs";
import { fileURLToPath } from "node:url";
import { expect, loginViaApi, test } from "../../support/fixtures";
import { DM1, loadChapter } from "../../support/shell";
import { ADMIN, clearRecords, record, wav } from "../../support/records";

/* A take read by a machine voice (`voice/synth.py`: a wav and a `<take>.machine` marker in the slide's folder) is listed with the author's own takes:
   it is marked as a machine voice, has no pronunciation check, and can be chosen as the slide's voice-over and deleted like any other. */

const RECORDS = fileURLToPath(new URL("../../.records", import.meta.url));

test("a machine voice is a take in the list", async ({ page, request }) => {
  const token = await loginViaApi(page, request, ADMIN);
  const ch = await loadChapter(request, DM1);
  await clearRecords(request, token, ch.num);
  await record(request, token, ch.num, 0, "ru", 1); // the author's own take 1
  const folder = `${RECORDS}/12/${ch.num}/0`;
  fs.writeFileSync(`${folder}/2.machine`, "af_heart");
  fs.writeFileSync(`${folder}/2.wav`, wav(2));

  await page.goto(`/book/12/chapter/${ch.id}`);
  await page.locator(".slide-rec-menu").click();
  const rows = page.locator(".rd-row");
  await expect(rows).toHaveCount(2);
  await expect(rows.nth(0)).toHaveClass(/on/); // the first take still voices the slide
  await expect(rows.nth(0).locator(".rd-name")).toHaveText("Запись 1");
  await expect(rows.nth(0).locator(".rd-check")).toHaveCount(1);
  await expect(rows.nth(1)).toHaveClass(/machine/);
  await expect(rows.nth(1).locator(".rd-name")).toHaveText("Машинный голос");
  await expect(rows.nth(1).locator(".rd-meta")).toContainText("0:02");
  await expect(rows.nth(1).locator(".rd-check"), "a machine reading is not checked for pronunciation").toHaveCount(0);

  // chosen like any other take
  await rows.nth(1).locator(".rd-pick").click();
  await expect(rows.nth(1)).toHaveClass(/on/);
  await expect(rows.nth(0)).not.toHaveClass(/on/);

  // deleted at once, with its marker
  await rows.nth(1).locator(".rd-del").click();
  await expect(rows).toHaveCount(1);
  expect(fs.existsSync(`${folder}/2.machine`)).toBe(false);
  expect(fs.existsSync(`${folder}/2.wav`)).toBe(false);
  await clearRecords(request, token, ch.num);
});
