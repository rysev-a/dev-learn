// Рендерит на сервере (react-dom/server) все слайды всех глав — сначала в начальном состоянии сцены, потом в
// конечном (как при «уменьшить движение»): ловит исключения при создании сцен (validate) и при отрисовке.
// Запуск: npm run slides:check
import { build } from "esbuild";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const out = fs.mkdtempSync(path.join(os.tmpdir(), "slides-smoke-"));
const slidesDir = path.join(root, "src/slides");
const dirs = fs.readdirSync(slidesDir, { withFileTypes: true }).filter((d) => d.isDirectory() && d.name !== "anim").map((d) => d.name);
const files = dirs.flatMap((d) => fs.readdirSync(path.join(slidesDir, d)).filter((f) => /^ch\d+\.tsx$/.test(f)).map((f) => `${d}/${f}`));

const entry = `import { renderToString } from "react-dom/server";
${files.map((f, i) => `import * as M${i} from ${JSON.stringify(path.join(slidesDir, f))};`).join("\n")}
const mods = {${files.map((f, i) => `${JSON.stringify(f)}: M${i}`).join(",")}};
export function run() {
  const res = { ok: 0, fail: [] };
  for (const [name, m] of Object.entries(mods))
    for (const [k, v] of Object.entries(m)) {
      if (!k.startsWith("SLIDES_")) continue;
      for (const [key, slides] of Object.entries(v))
        slides.forEach((C, i) => {
          try {
            const html = renderToString(<C />);
            if (html.length < 50) throw new Error("пустой вывод");
            res.ok++;
          } catch (e) {
            res.fail.push(name + " " + key + " #" + (i + 1) + ": " + (e instanceof Error ? e.message : String(e)));
          }
        });
    }
  return res;
}
`;
fs.writeFileSync(path.join(out, "entry.tsx"), entry);
await build({
  entryPoints: [path.join(out, "entry.tsx")], bundle: true, platform: "node", format: "cjs", outfile: path.join(out, "bundle.cjs"),
  jsx: "automatic", nodePaths: [path.join(root, "node_modules")], logLevel: "error",
});
const m = await import(pathToFileURL(path.join(out, "bundle.cjs")).href);
let failed = 0;
for (const reduced of [false, true]) {
  globalThis.window = reduced ? { matchMedia: () => ({ matches: true }) } : undefined;
  const r = m.run();
  console.log(reduced ? "конечные кадры:" : "начальные кадры:", "ok", r.ok, "ошибок", r.fail.length);
  for (const f of r.fail.slice(0, 30)) console.log("  ", f);
  failed += r.fail.length;
}
fs.rmSync(out, { recursive: true, force: true });
process.exit(failed ? 1 : 0);
