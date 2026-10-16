// Серверная отрисовка симулятора сети: NetLab и панель каждого устройства каждого сценария.
// Ловит падения компонентов (в том числе после правок типов). Запуск: npm run net:render
import { build } from "esbuild";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const out = fs.mkdtempSync(path.join(os.tmpdir(), "net-smoke-"));
const src = (p) => JSON.stringify(path.join(root, "src", p));
fs.writeFileSync(
  path.join(out, "entry.tsx"),
  `import { renderToString } from "react-dom/server";
import { NET_CHAPTERS } from ${src("netlab/registry.ts")};
import { exec } from ${src("netlab/term.ts")};
import NetLab from ${src("netlab/react/NetLab.tsx")};
import DevicePanel from ${src("netlab/react/DevicePanel.tsx")};
export function run() {
  const fail = [];
  let ok = 0;
  for (const [ch, list] of Object.entries(NET_CHAPTERS))
    for (const s of list) {
      try {
        renderToString(<NetLab scenario={s} code={undefined} onCode={() => {}} solvedBefore={false} hasNext={false} nextLabel="" />);
        ok++;
      } catch (e) {
        fail.push(ch + "/" + s.id + " NetLab: " + (e instanceof Error ? e.message : String(e)));
      }
      const st = s.build();
      for (const id of Object.keys(st.devices))
        try {
          renderToString(<DevicePanel state={st} devId={id} tools={s.tools ?? {}} apply={() => {}} exec={(l) => exec(st, id, l)} lines={[]} onRun={() => {}} />);
          ok++;
        } catch (e) {
          fail.push(ch + "/" + s.id + " " + id + " DevicePanel: " + (e instanceof Error ? e.message : String(e)));
        }
    }
  return { ok, fail };
}
`,
);
await build({
  entryPoints: [path.join(out, "entry.tsx")], bundle: true, platform: "node", format: "cjs", outfile: path.join(out, "bundle.cjs"),
  jsx: "automatic", nodePaths: [path.join(root, "node_modules")], logLevel: "error", loader: { ".css": "empty" },
});
const m = await import(pathToFileURL(path.join(out, "bundle.cjs")).href);
const r = m.run();
console.log("отрисовано", r.ok, "ошибок", r.fail.length);
for (const f of r.fail.slice(0, 30)) console.log("  ", f);
fs.rmSync(out, { recursive: true, force: true });
process.exit(r.fail.length ? 1 : 0);
