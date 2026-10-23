// Выгрузка слайдов всех глав в JSON: рубрика, заголовки, «ГЛАВНОЕ», блоки тела и сцены (кадры) как данные.
// Один раз переводит рукописный формат в данные для backend-rs/frontend-rs; сцены на ручной отрисовке (kit.tsx) помечаются
// {comp: "<имя>"} — их переписывают отдельно. Запуск: node scripts/slides-export.mjs <каталог вывода>
import { build } from "esbuild";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = path.resolve(process.argv[2] || "slides-export");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "slides-export-"));
const slidesDir = path.join(root, "src/slides");
const dirs = fs.readdirSync(slidesDir, { withFileTypes: true }).filter((d) => d.isDirectory() && d.name !== "anim").map((d) => d.name);
const files = dirs.flatMap((d) => fs.readdirSync(path.join(slidesDir, d)).filter((f) => /^ch\d+\.tsx$/.test(f)).map((f) => `${d}/${f}`));

const entry = `
import * as R from "react";
${files.map((f, i) => `import * as M${i} from ${JSON.stringify(path.join(slidesDir, f))};`).join("\n")}
const mods = {${files.map((f, i) => `${JSON.stringify(f)}: M${i}`).join(",")}};

// React-узел → JSON: хост-элементы как {tag, cls, children}, виджеты и сцены — по меткам, остальное разворачиваем.
function walk(node) {
  if (node == null || node === false || node === true) return null;
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.flatMap((n) => { const w = walk(n); return w == null ? [] : Array.isArray(w) ? w : [w]; });
  const { type, props } = node;
  if (type === R.Fragment) return walk(props.children);
  if (typeof type === "string") {
    const kids = walk(props.children);
    const o = { tag: type };
    if (props.className) o.cls = props.className;
    if (props.style) o.style = props.style;
    const rest = Object.fromEntries(Object.entries(props).filter(([k]) => !["children", "className", "style", "key"].includes(k)));
    if (Object.keys(rest).length) o.attrs = rest;
    if (kids != null) o.children = Array.isArray(kids) ? kids : [kids];
    return o;
  }
  if (type.spec) return { scene: type.spec, cues: props.cues ?? null, name: type.name };
  if (type.kw) return { widget: "pycode", kw: type.kw, boolsAsNum: type.boolsAsNum, text: props.children };
  const name = type.name || "?";
  if (name === "Node") return { widget: "node", mono: !!props.mono, kind: props.kind ?? "", title: walk(props.title), sub: walk(props.sub) };
  if (name === "Cmd") return { widget: "cmd", text: props.children };
  if (name === "Arr") return { widget: "arr" };
  if (name === "RsCode") return { widget: "rscode", text: props.children };
  if (type.rubric !== undefined) return { slide: true };
  try {
    return walk(type(props));
  } catch (e) {
    return { comp: name, props: Object.fromEntries(Object.entries(props).filter(([, v]) => ["string", "number", "boolean"].includes(typeof v))), cues: props.cues ?? null };
  }
}

export function run() {
  const out = {};
  for (const [file, m] of Object.entries(mods)) {
    const dir = file.split("/")[0];
    const slidesBy = Object.entries(m).find(([k]) => k.startsWith("SLIDES_"));
    const titlesBy = Object.entries(m).find(([k]) => k.startsWith("SLIDE_TITLES_"));
    if (!slidesBy) continue;
    for (const [key, comps] of Object.entries(slidesBy[1])) {
      const titles = titlesBy ? titlesBy[1][key] : null;
      const slides = comps.map((C, i) => {
        const el = C();
        const S = el.type;
        const p = el.props;
        return {
          rubric: S.rubric, total: S.total, n: p.n, title: p.title, sub: p.sub ?? null, main: walk(p.main), short: titles ? titles[i] : null,
          body: walk(p.children),
        };
      });
      out[key] = { dir, file, slides };
    }
  }
  return out;
}
`;
fs.writeFileSync(path.join(tmp, "entry.tsx"), entry);
await build({
  entryPoints: [path.join(tmp, "entry.tsx")], bundle: true, platform: "node", format: "cjs", outfile: path.join(tmp, "bundle.cjs"),
  jsx: "automatic", nodePaths: [path.join(root, "node_modules")], logLevel: "error",
});
globalThis.window = undefined;
const m = await import(pathToFileURL(path.join(tmp, "bundle.cjs")).href);
const data = m.run();
fs.mkdirSync(outDir, { recursive: true });
let slides = 0;
for (const [key, ch] of Object.entries(data)) {
  const [book, num] = key.split(":");
  fs.writeFileSync(path.join(outDir, `${book.padStart(2, "0")}-${String(num).padStart(2, "0")}.json`), JSON.stringify(ch));
  slides += ch.slides.length;
}
console.log(`глав ${Object.keys(data).length}, слайдов ${slides} → ${outDir}`);
fs.rmSync(tmp, { recursive: true, force: true });
