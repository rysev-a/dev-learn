"""Задачи книги «Современный Frontend»: глава 24."""

TASKS: dict[int, list[dict]] = {24: [{'id': 'j24-parse-version',
  'mode': 'js',
  'title': 'Разбор версии semver',
  'statement': 'Напишите parseVersion(str) → { major, minor, patch, prerelease, build } или null, '
               'если строка не версия. Допускается ведущая «v». major, minor, patch — числа без '
               'ведущих нулей (кроме самого 0). После «-» идёт предрелиз — идентификаторы через '
               'точку из [0-9A-Za-z-]; числовые идентификаторы (состоящие только из цифр) '
               'превращаются в числа, остальные остаются строками. После «+» — метаданные сборки '
               '(массив строк). Пустые идентификаторы недопустимы. Пробелы по краям обрезаются.',
  'starter': 'function parseVersion(str) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (s) => console.log(JSON.stringify(s), JSON.stringify(parseVersion(s)));\n'
            'show("1.2.3"); show("v10.20.30"); show(" 1.0.0 "); show("1.2.3-beta.2"); '
            'show("1.2.3-alpha.1.x-y+build.5"); show("1.2.3+meta");\n'
            'show("01.2.3"); show("1.2"); show("1.2.3.4"); show("1.2.3-"); show("1.2.3-a..b"); '
            'show("x.y.z"); show(""); show("1.2.3-0.3.7");\n',
  'hint': 'Одно регулярное выражение с тремя группами чисел и двумя необязательными хвостами.',
  'expected': ['"1.2.3" {"major":1,"minor":2,"patch":3,"prerelease":[],"build":[]}',
               '"v10.20.30" {"major":10,"minor":20,"patch":30,"prerelease":[],"build":[]}',
               '" 1.0.0 " {"major":1,"minor":0,"patch":0,"prerelease":[],"build":[]}',
               '"1.2.3-beta.2" {"major":1,"minor":2,"patch":3,"prerelease":["beta",2],"build":[]}',
               '"1.2.3-alpha.1.x-y+build.5" '
               '{"major":1,"minor":2,"patch":3,"prerelease":["alpha",1,"x-y"],"build":["build","5"]}',
               '"1.2.3+meta" {"major":1,"minor":2,"patch":3,"prerelease":[],"build":["meta"]}',
               '"01.2.3" null',
               '"1.2" null',
               '"1.2.3.4" null',
               '"1.2.3-" null',
               '"1.2.3-a..b" null',
               '"x.y.z" null',
               '"" null',
               '"1.2.3-0.3.7" {"major":1,"minor":2,"patch":3,"prerelease":[0,3,7],"build":[]}']},
 {'id': 'j24-compare',
  'mode': 'js',
  'title': 'Сравнение версий',
  'statement': 'Напишите compare(a, b) → -1, 0 или 1 по правилам semver. Версии — строки '
               '(parseVersion уже есть в заготовке). Сначала major, minor, patch по числам. Версия '
               'без предрелиза старше версии с предрелизом. Предрелизы сравниваются по '
               'идентификаторам слева направо: числовые — как числа, строковые — '
               'лексикографически, числовой идентификатор младше строкового; если все общие равны, '
               'меньше тот, у кого идентификаторов меньше. Метаданные сборки (+…) игнорируются. '
               "Некорректная версия — TypeError('Invalid Version: ' + строка).",
  'starter': 'function parseVersion(str) {\n'
             '  const m = '
             '/^v?(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?(?:\\+([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?$/.exec(String(str).trim());\n'
             '  if (!m) return null;\n'
             '  return {\n'
             '    major: +m[1], minor: +m[2], patch: +m[3],\n'
             '    prerelease: m[4] ? m[4].split(".").map((x) => (/^\\d+$/.test(x) ? Number(x) : '
             'x)) : [],\n'
             '    build: m[5] ? m[5].split(".") : [],\n'
             '  };\n'
             '}\n'
             'function compare(a, b) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const c = (a, b) => console.log(a, b, compare(a, b));\n'
            'c("1.2.3", "1.2.3"); c("1.2.3", "1.2.4"); c("2.0.0", "1.9.9"); c("1.10.0", "1.9.0");\n'
            'c("1.0.0-alpha", "1.0.0"); c("1.0.0", "1.0.0-rc.1"); c("1.0.0-alpha", "1.0.0-beta"); '
            'c("1.0.0-alpha.1", "1.0.0-alpha");\n'
            'c("1.0.0-alpha.2", "1.0.0-alpha.10"); c("1.0.0-1", "1.0.0-alpha"); '
            'c("1.0.0-alpha.beta", "1.0.0-alpha.1"); c("1.0.0+a", "1.0.0+b");\n'
            'try { compare("1.0", "1.0.0"); } catch (e) { console.log(e.name, e.message); }\n',
  'hint': 'Сначала числа, затем отдельная функция сравнения предрелизных массивов.',
  'expected': ['1.2.3 1.2.3 0',
               '1.2.3 1.2.4 -1',
               '2.0.0 1.9.9 1',
               '1.10.0 1.9.0 1',
               '1.0.0-alpha 1.0.0 -1',
               '1.0.0 1.0.0-rc.1 1',
               '1.0.0-alpha 1.0.0-beta -1',
               '1.0.0-alpha.1 1.0.0-alpha 1',
               '1.0.0-alpha.2 1.0.0-alpha.10 -1',
               '1.0.0-1 1.0.0-alpha -1',
               '1.0.0-alpha.beta 1.0.0-alpha.1 1',
               '1.0.0+a 1.0.0+b 0',
               'TypeError Invalid Version: 1.0']},
 {'id': 'j24-sort',
  'mode': 'js',
  'title': 'Сортировка версий',
  'statement': 'Напишите sortVersions(list, desc = false): возвращает новый массив строк версий, '
               'отсортированный по semver (по возрастанию; при desc — по убыванию). Некорректные '
               'версии пропускаются. Версии, равные по приоритету (отличаются только метаданными '
               'сборки), сохраняют исходный порядок. Функции parseVersion и compare уже есть в '
               'заготовке.',
  'starter': 'function parseVersion(str) {\n'
             '  const m = '
             '/^v?(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?(?:\\+([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?$/.exec(String(str).trim());\n'
             '  if (!m) return null;\n'
             '  return {\n'
             '    major: +m[1], minor: +m[2], patch: +m[3],\n'
             '    prerelease: m[4] ? m[4].split(".").map((x) => (/^\\d+$/.test(x) ? Number(x) : '
             'x)) : [],\n'
             '    build: m[5] ? m[5].split(".") : [],\n'
             '  };\n'
             '}\n'
             'function comparePre(a, b) {\n'
             '  if (!a.length && !b.length) return 0;\n'
             '  if (!a.length) return 1;\n'
             '  if (!b.length) return -1;\n'
             '  for (let i = 0; i < Math.max(a.length, b.length); i++) {\n'
             '    if (i >= a.length) return -1;\n'
             '    if (i >= b.length) return 1;\n'
             '    const x = a[i], y = b[i];\n'
             '    if (x === y) continue;\n'
             '    const nx = typeof x === "number", ny = typeof y === "number";\n'
             '    if (nx && ny) return x < y ? -1 : 1;\n'
             '    if (nx) return -1;\n'
             '    if (ny) return 1;\n'
             '    return x < y ? -1 : 1;\n'
             '  }\n'
             '  return 0;\n'
             '}\n'
             'function compare(a, b) {\n'
             '  const x = typeof a === "string" ? parseVersion(a) : a;\n'
             '  const y = typeof b === "string" ? parseVersion(b) : b;\n'
             '  if (!x) throw new TypeError("Invalid Version: " + a);\n'
             '  if (!y) throw new TypeError("Invalid Version: " + b);\n'
             '  for (const k of ["major", "minor", "patch"]) if (x[k] !== y[k]) return x[k] < y[k] '
             '? -1 : 1;\n'
             '  return comparePre(x.prerelease, y.prerelease);\n'
             '}\n'
             'function sortVersions(list, desc = false) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (a, d) => console.log(sortVersions(a, d).join(" "));\n'
            'show(["1.10.0", "1.2.0", "1.9.9", "0.1.0"]);\n'
            'show(["1.0.0", "1.0.0-rc.1", "1.0.0-alpha", "1.0.0-beta.2", "1.0.0-beta.11", '
            '"1.0.0-beta"]);\n'
            'show(["2.0.0", "bad", "1.0", "1.0.0"], true);\n'
            'show(["1.0.0+b", "1.0.0+a", "1.0.0"]);\n'
            'show([]);\n',
  'hint': 'filter(parseVersion), затем sort с compare; для desc поменяйте знак.',
  'expected': ['0.1.0 1.2.0 1.9.9 1.10.0',
               '1.0.0-alpha 1.0.0-beta 1.0.0-beta.2 1.0.0-beta.11 1.0.0-rc.1 1.0.0',
               '2.0.0 1.0.0',
               '1.0.0+b 1.0.0+a 1.0.0']},
 {'id': 'j24-satisfies',
  'mode': 'js',
  'title': 'Диапазоны версий',
  'statement': 'Напишите satisfies(version, range). range — один или несколько наборов через «||»; '
               'набор — компараторы через пробел (И) или дефисный диапазон «A - B». Компаратор: '
               '«^», «~», «>=», «>», «<=», «<», «=» либо без оператора + частичная версия («1», '
               '«1.2», «1.2.3», «1.x», «*»). Правила: «^1.2.3» = >=1.2.3 <2.0.0; «^0.2.3» = '
               '>=0.2.3 <0.3.0; «^0.0.3» = >=0.0.3 <0.0.4; «~1.2.3» = >=1.2.3 <1.3.0; «~1» = '
               '>=1.0.0 <2.0.0; «1.x», «1» — >=1.0.0 <2.0.0; «1.2» — >=1.2.0 <1.3.0; «*» — любая. '
               'Версия с предрелизом подходит набору, только если в нём есть компаратор с теми же '
               'major.minor.patch и предрелизом. parseVersion и compare уже есть.',
  'starter': 'function parseVersion(str) {\n'
             '  const m = '
             '/^v?(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(?:-([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?(?:\\+([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?$/.exec(String(str).trim());\n'
             '  if (!m) return null;\n'
             '  return {\n'
             '    major: +m[1], minor: +m[2], patch: +m[3],\n'
             '    prerelease: m[4] ? m[4].split(".").map((x) => (/^\\d+$/.test(x) ? Number(x) : '
             'x)) : [],\n'
             '    build: m[5] ? m[5].split(".") : [],\n'
             '  };\n'
             '}\n'
             'function comparePre(a, b) {\n'
             '  if (!a.length && !b.length) return 0;\n'
             '  if (!a.length) return 1;\n'
             '  if (!b.length) return -1;\n'
             '  for (let i = 0; i < Math.max(a.length, b.length); i++) {\n'
             '    if (i >= a.length) return -1;\n'
             '    if (i >= b.length) return 1;\n'
             '    const x = a[i], y = b[i];\n'
             '    if (x === y) continue;\n'
             '    const nx = typeof x === "number", ny = typeof y === "number";\n'
             '    if (nx && ny) return x < y ? -1 : 1;\n'
             '    if (nx) return -1;\n'
             '    if (ny) return 1;\n'
             '    return x < y ? -1 : 1;\n'
             '  }\n'
             '  return 0;\n'
             '}\n'
             'function compare(a, b) {\n'
             '  const x = typeof a === "string" ? parseVersion(a) : a;\n'
             '  const y = typeof b === "string" ? parseVersion(b) : b;\n'
             '  if (!x) throw new TypeError("Invalid Version: " + a);\n'
             '  if (!y) throw new TypeError("Invalid Version: " + b);\n'
             '  for (const k of ["major", "minor", "patch"]) if (x[k] !== y[k]) return x[k] < y[k] '
             '? -1 : 1;\n'
             '  return comparePre(x.prerelease, y.prerelease);\n'
             '}\n'
             'function satisfies(version, range) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (v, r) => console.log(JSON.stringify(r), v, satisfies(v, r));\n'
            't("1.2.3", "^1.2.3"); t("1.9.9", "^1.2.3"); t("2.0.0", "^1.2.3"); t("1.2.2", '
            '"^1.2.3");\n'
            't("0.2.9", "^0.2.3"); t("0.3.0", "^0.2.3"); t("0.0.3", "^0.0.3"); t("0.0.4", '
            '"^0.0.3");\n'
            't("1.2.9", "~1.2.3"); t("1.3.0", "~1.2.3"); t("1.9.0", "~1"); t("2.0.0", "~1");\n'
            't("1.5.0", "1.x"); t("1.5.0", "1"); t("1.2.9", "1.2"); t("1.3.0", "1.2"); t("9.9.9", '
            '"*"); t("1.2.3", "");\n'
            't("1.2.3", ">=1.0.0 <2.0.0"); t("2.0.0", ">=1.0.0 <2.0.0"); t("1.2.3", ">1.2.3"); '
            't("1.2.4", ">1.2"); t("1.3.0", ">1.2"); t("1.2.9", "<=1.2");\n'
            't("1.0.0", "1.0.0"); t("1.0.1", "=1.0.0"); t("1.5.0", "1.2.3 - 2.0.0"); t("2.0.1", '
            '"1.2.3 - 2.0.0"); t("2.5.0", "1.2.3 - 2");\n'
            't("1.0.0", "<1.0.0 || >=2.0.0"); t("2.1.0", "<1.0.0 || >=2.0.0"); t("1.5.0", "<1.0.0 '
            '|| >=2.0.0");\n'
            't("1.2.4-beta.1", "^1.2.3"); t("1.2.3-beta.1", ">=1.2.3-alpha"); t("1.2.3-beta.1", '
            '"^1.2.3-alpha.0"); t("2.0.0-rc.1", ">=1.0.0");\n'
            't("bad", "*");\n',
  'hint': 'Разверните каждый компаратор в пары (оператор, версия), проверьте все; затем правило '
          'предрелизов.',
  'expected': ['"^1.2.3" 1.2.3 true',
               '"^1.2.3" 1.9.9 true',
               '"^1.2.3" 2.0.0 false',
               '"^1.2.3" 1.2.2 false',
               '"^0.2.3" 0.2.9 true',
               '"^0.2.3" 0.3.0 false',
               '"^0.0.3" 0.0.3 true',
               '"^0.0.3" 0.0.4 false',
               '"~1.2.3" 1.2.9 true',
               '"~1.2.3" 1.3.0 false',
               '"~1" 1.9.0 true',
               '"~1" 2.0.0 false',
               '"1.x" 1.5.0 true',
               '"1" 1.5.0 true',
               '"1.2" 1.2.9 true',
               '"1.2" 1.3.0 false',
               '"*" 9.9.9 true',
               '"" 1.2.3 true',
               '">=1.0.0 <2.0.0" 1.2.3 true',
               '">=1.0.0 <2.0.0" 2.0.0 false',
               '">1.2.3" 1.2.3 false',
               '">1.2" 1.2.4 false',
               '">1.2" 1.3.0 true',
               '"<=1.2" 1.2.9 true',
               '"1.0.0" 1.0.0 true',
               '"=1.0.0" 1.0.1 false',
               '"1.2.3 - 2.0.0" 1.5.0 true',
               '"1.2.3 - 2.0.0" 2.0.1 false',
               '"1.2.3 - 2" 2.5.0 true',
               '"<1.0.0 || >=2.0.0" 1.0.0 false',
               '"<1.0.0 || >=2.0.0" 2.1.0 true',
               '"<1.0.0 || >=2.0.0" 1.5.0 false',
               '"^1.2.3" 1.2.4-beta.1 false',
               '">=1.2.3-alpha" 1.2.3-beta.1 true',
               '"^1.2.3-alpha.0" 1.2.3-beta.1 true',
               '">=1.0.0" 2.0.0-rc.1 false',
               '"*" bad false']},
 {'id': 'j24-max-satisfying',
  'mode': 'js',
  'title': 'Максимальная подходящая версия',
  'statement': 'Напишите maxSatisfying(versions, range): версия из списка с наибольшим приоритетом '
               'semver, подходящая под range; null, если подходящих нет. Некорректные версии '
               'пропускаются. Предрелизы выбираются только если range их допускает (правило: набор '
               'содержит компаратор с теми же major.minor.patch и предрелизом). В заготовке есть '
               'parseVersion, compare и satisfies для диапазонов ^, ~, >=, >, <=, <, точных '
               'версий, «*» и пробела как «И».',
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
             'function maxSatisfying(versions, range) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const vs = ["1.0.0", "1.2.3", "1.2.9", "1.3.0", "2.0.0", "2.1.0-beta.1", "0.9.0", '
            '"bad"];\n'
            'const m = (r) => console.log(JSON.stringify(r), maxSatisfying(vs, r));\n'
            'm("^1.0.0"); m("~1.2.0"); m(">=1.2.9 <2.0.0"); m("*"); m("^3.0.0"); m(">1.0.0"); '
            'm("<1.0.0"); m("2.0.0");\n'
            'console.log(maxSatisfying([], "*"));\n',
  'hint': 'Отфильтруйте satisfies, затем возьмите максимум по cmpV.',
  'expected': ['"^1.0.0" 1.3.0',
               '"~1.2.0" 1.2.9',
               '">=1.2.9 <2.0.0" 1.3.0',
               '"*" 2.0.0',
               '"^3.0.0" null',
               '">1.0.0" 2.0.0',
               '"<1.0.0" 0.9.0',
               '"2.0.0" 2.0.0',
               'null']},
 {'id': 'j24-inc',
  'mode': 'js',
  'title': 'Увеличение версии',
  'statement': "Напишите inc(version, kind, id = 'alpha'): kind — 'major', 'minor', 'patch' или "
               "'prerelease'. major/minor/patch: если у версии есть предрелиз и сброс уже «на "
               'месте» (для major: minor = patch = 0; для minor: patch = 0; для patch — всегда) — '
               'просто отбросить предрелиз; иначе увеличить нужную часть и обнулить младшие, '
               'предрелиз и метаданные убрать. prerelease: без предрелиза — увеличить patch и '
               'добавить «-id.0»; с предрелизом, чей первый идентификатор равен id и последний — '
               'число, — увеличить это число; с предрелизом иначе — заменить его на «id.0» (числа '
               'major.minor.patch не меняются). Результат — строка без «+сборки». Некорректная '
               'версия — null.',
  'starter': 'function inc(version, kind, id = "alpha") {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (v, k, id) => console.log(v, k, id ?? "", inc(v, k, id));\n'
            't("1.2.3", "major"); t("1.2.3", "minor"); t("1.2.3", "patch"); t("1.2.3-beta.1", '
            '"patch"); t("1.2.0-beta.1", "minor"); t("1.2.3-beta.1", "minor");\n'
            't("2.0.0-rc.1", "major"); t("2.1.0-rc.1", "major"); t("1.2.3", "prerelease"); '
            't("1.2.3", "prerelease", "beta");\n'
            't("1.2.4-alpha.0", "prerelease"); t("1.2.4-alpha.7", "prerelease"); '
            't("1.2.4-alpha.7", "prerelease", "beta"); t("1.2.4-alpha", "prerelease");\n'
            't("1.2.3+build.5", "patch"); t("bad", "patch");\n',
  'hint': 'Разберите версию регулярным выражением и составьте строку вручную.',
  'expected': ['1.2.3 major  2.0.0',
               '1.2.3 minor  1.3.0',
               '1.2.3 patch  1.2.4',
               '1.2.3-beta.1 patch  1.2.3',
               '1.2.0-beta.1 minor  1.2.0',
               '1.2.3-beta.1 minor  1.3.0',
               '2.0.0-rc.1 major  2.0.0',
               '2.1.0-rc.1 major  3.0.0',
               '1.2.3 prerelease  1.2.4-alpha.0',
               '1.2.3 prerelease beta 1.2.4-beta.0',
               '1.2.4-alpha.0 prerelease  1.2.4-alpha.1',
               '1.2.4-alpha.7 prerelease  1.2.4-alpha.8',
               '1.2.4-alpha.7 prerelease beta 1.2.4-beta.0',
               '1.2.4-alpha prerelease  1.2.4-alpha.0',
               '1.2.3+build.5 patch  1.2.4',
               'bad patch  null']},
 {'id': 'j24-diff',
  'mode': 'js',
  'title': 'Тип различия версий',
  'statement': "Напишите diff(a, b): возвращает 'major', 'minor', 'patch', 'prerelease' или null "
               '(версии равны, метаданные сборки не учитываются). Версии сравниваются по '
               "приоритету: если отличается major — 'major', иначе minor — 'minor', иначе patch — "
               "'patch'; если числа равны, а предрелизы различаются — 'prerelease'. Если одна из "
               'версий с предрелизом отличается от другой по числам, тип определяется старшей '
               "отличающейся частью («1.0.0-rc.1» и «2.0.0» — 'major'). Нечувствительно к порядку "
               'аргументов. Некорректная версия — TypeError.',
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
             'function diff(a, b) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (a, b) => console.log(a, b, diff(a, b));\n'
            't("1.2.3", "1.2.3"); t("1.2.3", "2.0.0"); t("2.0.0", "1.0.0"); t("1.2.3", "1.3.0"); '
            't("1.2.3", "1.2.9");\n'
            't("1.0.0-rc.1", "1.0.0"); t("1.0.0-alpha", "1.0.0-beta"); t("1.0.0-rc.1", "2.0.0"); '
            't("1.1.0-rc.1", "1.2.0"); t("1.2.3-a", "1.2.3-a");\n'
            'try { diff("x", "1.0.0"); } catch (e) { console.log(e.name); }\n',
  'hint': 'Разберите обе версии parseV и сравните части по порядку.',
  'expected': ['1.2.3 1.2.3 null',
               '1.2.3 2.0.0 major',
               '2.0.0 1.0.0 major',
               '1.2.3 1.3.0 minor',
               '1.2.3 1.2.9 patch',
               '1.0.0-rc.1 1.0.0 prerelease',
               '1.0.0-alpha 1.0.0-beta prerelease',
               '1.0.0-rc.1 2.0.0 major',
               '1.1.0-rc.1 1.2.0 minor',
               '1.2.3-a 1.2.3-a null',
               'TypeError']},
 {'id': 'j24-parse-spec',
  'mode': 'js',
  'title': 'Разбор «имя@диапазон»',
  'statement': 'Напишите parsePackageSpec(spec) → { name, range } или null. Имя — «name» или '
               '«@scope/name» (одна часть после «@scope/»); после имени необязательное '
               "«@диапазон». Нет диапазона или он пуст — range = 'latest'. Диапазон может "
               'содержать любые символы (кроме пробелов в начале и конца — их обрезаем). Пустая '
               'строка, «@» без имени, «@scope» без «/name», имя с пробелами — null.',
  'starter': 'function parsePackageSpec(spec) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const s of ["lodash", "lodash@4.17.21", "lodash@^4", "lodash@", "@scope/pkg", '
            '"@scope/pkg@1.2.3", "@scope/pkg@>=1 <2", "@scope", "@", "", "a b", "name@latest", "  '
            'zod@3  "])\n'
            '  console.log(JSON.stringify(s), JSON.stringify(parsePackageSpec(s)));\n',
  'hint': 'Регулярка: ^(@[^/@\\s]+/[^/@\\s]+|[^/@\\s]+)(?:@(.*))?$.',
  'expected': ['"lodash" {"name":"lodash","range":"latest"}',
               '"lodash@4.17.21" {"name":"lodash","range":"4.17.21"}',
               '"lodash@^4" {"name":"lodash","range":"^4"}',
               '"lodash@" {"name":"lodash","range":"latest"}',
               '"@scope/pkg" {"name":"@scope/pkg","range":"latest"}',
               '"@scope/pkg@1.2.3" {"name":"@scope/pkg","range":"1.2.3"}',
               '"@scope/pkg@>=1 <2" {"name":"@scope/pkg","range":">=1 <2"}',
               '"@scope" null',
               '"@" null',
               '"" null',
               '"a b" null',
               '"name@latest" {"name":"name","range":"latest"}',
               '"  zod@3  " {"name":"zod","range":"3"}']},
 {'id': 'j24-validate-name',
  'mode': 'js',
  'title': 'Проверка имени пакета',
  'statement': 'Напишите validatePackageName(name) → { valid, errors }. errors — массив строк в '
               'порядке проверок: «name must be a string» (не строка — сразу вернуть); «name '
               'length must be greater than zero» (пустое); «name can no longer contain more than '
               '214 characters»; «name cannot start with a period» («.»); «name cannot start with '
               'an underscore»; «name can no longer contain capital letters» (есть A–Z); «name can '
               'only contain URL-friendly characters» (после снятия префикса «@scope/» остались '
               'символы вне [a-z0-9._~-] — в нижнем регистре; пробелы, «/», «!» и т.п.); «name is '
               'reserved» (имя равно node_modules или favicon.ico). Для области «@scope/name» '
               'проверяйте и scope, и имя как отдельные части: каждая — непустая; иначе «name must '
               'be a valid scoped name».',
  'starter': 'function validatePackageName(name) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const n of ["lodash", "my-app", "@scope/pkg", "a", "Upper", "_hidden", ".dot", '
            '"has space", "a/b", "", "x".repeat(215), "node_modules", "favicon.ico", "@scope", '
            '"@/x", "@s/", "ok.name_1~", "bad!", 42])\n'
            '  console.log(JSON.stringify(n === "x".repeat(215) ? "x*215" : n), '
            'JSON.stringify(validatePackageName(n)));\n',
  'hint': 'Сначала разберите область, затем применяйте проверки к имени по очереди.',
  'expected': ['"lodash" {"valid":true,"errors":[]}',
               '"my-app" {"valid":true,"errors":[]}',
               '"@scope/pkg" {"valid":true,"errors":[]}',
               '"a" {"valid":true,"errors":[]}',
               '"Upper" {"valid":false,"errors":["name can no longer contain capital letters"]}',
               '"_hidden" {"valid":false,"errors":["name cannot start with an underscore"]}',
               '".dot" {"valid":false,"errors":["name cannot start with a period"]}',
               '"has space" {"valid":false,"errors":["name can only contain URL-friendly '
               'characters"]}',
               '"a/b" {"valid":false,"errors":["name can only contain URL-friendly characters"]}',
               '"" {"valid":false,"errors":["name length must be greater than zero"]}',
               '"x*215" {"valid":false,"errors":["name can no longer contain more than 214 '
               'characters"]}',
               '"node_modules" {"valid":false,"errors":["name is reserved"]}',
               '"favicon.ico" {"valid":false,"errors":["name is reserved"]}',
               '"@scope" {"valid":false,"errors":["name must be a valid scoped name","name can '
               'only contain URL-friendly characters"]}',
               '"@/x" {"valid":false,"errors":["name must be a valid scoped name","name can only '
               'contain URL-friendly characters"]}',
               '"@s/" {"valid":false,"errors":["name must be a valid scoped name","name can only '
               'contain URL-friendly characters"]}',
               '"ok.name_1~" {"valid":true,"errors":[]}',
               '"bad!" {"valid":false,"errors":["name can only contain URL-friendly characters"]}',
               '42 {"valid":false,"errors":["name must be a string"]}']},
 {'id': 'j24-resolve-tree',
  'mode': 'js',
  'title': 'Разрешение зависимостей и hoisting',
  'statement': 'Напишите resolveTree(registry, rootDeps). registry — { имя: { версия: { '
               'dependencies: { имя: диапазон } } } }, rootDeps — { имя: диапазон } (диапазоны '
               'вида ^, ~, точная, *). Результат — объект «путь установки → версия», ключи '
               'отсортированы. Алгоритм: очередь запросов {name, range, dir}; корневые запросы '
               "отсортированы по имени, dir = '' (корень). Обработка запроса: идя от dir вверх по "
               'родителям (dir, затем его родитель, …, корень), найдите первый уже установленный '
               'по пути `${d}node_modules/${name}`; если он есть и его версия подходит — запрос '
               "выполнен. Иначе выберите наибольшую подходящую версию из registry (нет — Error('No "
               "matching version for name@range')) и установите её в самый верхний каталог от "
               'корня до dir, где слот `node_modules/name` свободен (если свободных нет — '
               "Error('Unresolvable')). После установки поставьте в конец очереди запросы на её "
               'dependencies (по имени), dir = путь её каталога `${слот}/` (например '
               "'node_modules/a/'). Путь установки — «node_modules/a» или "
               "«node_modules/a/node_modules/b»; каталог dir пакета — путь + '/'. В заготовке есть "
               'satisfies/cmpV/parseV для ^, ~, точных, >=, <, *.',
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
             'function resolveTree(registry, rootDeps) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const reg = {\n'
            '  a: { "1.0.0": { dependencies: { c: "^1.0.0" } }, "1.1.0": { dependencies: { c: '
            '"^1.0.0" } } },\n'
            '  b: { "1.0.0": { dependencies: { c: "^2.0.0" } } },\n'
            '  c: { "1.0.0": {}, "1.2.0": {}, "2.0.0": {}, "2.1.0": {} },\n'
            '  d: { "1.0.0": { dependencies: { a: "^1.0.0", e: "*" } } },\n'
            '  e: { "1.0.0": { dependencies: { d: "^1.0.0" } } },\n'
            '};\n'
            'const show = (deps) => { try { console.log(JSON.stringify(resolveTree(reg, deps))); } '
            'catch (e) { console.log("!" + e.message); } };\n'
            'show({ a: "^1.0.0" });\n'
            'show({ a: "^1.0.0", b: "^1.0.0" });\n'
            'show({ b: "^1.0.0", a: "^1.0.0" });\n'
            'show({ c: "~1.0.0", b: "*" });\n'
            'show({ d: "*" });\n'
            'show({ a: "^2.0.0" });\n'
            'show({});\n',
  'hint': 'BFS по очереди запросов; функция ancestors(dir) возвращает цепочку каталогов от dir к '
          'корню, а для установки — от корня к dir.',
  'expected': ['{"node_modules/a":"1.1.0","node_modules/c":"1.2.0"}',
               '{"node_modules/a":"1.1.0","node_modules/b":"1.0.0","node_modules/b/node_modules/c":"2.1.0","node_modules/c":"1.2.0"}',
               '{"node_modules/a":"1.1.0","node_modules/b":"1.0.0","node_modules/b/node_modules/c":"2.1.0","node_modules/c":"1.2.0"}',
               '{"node_modules/b":"1.0.0","node_modules/b/node_modules/c":"2.1.0","node_modules/c":"1.0.0"}',
               '{"node_modules/a":"1.1.0","node_modules/c":"1.2.0","node_modules/d":"1.0.0","node_modules/e":"1.0.0"}',
               '!No matching version for a@^2.0.0',
               '{}']},
 {'id': 'j24-cycles',
  'mode': 'js',
  'title': 'Циклы зависимостей',
  'statement': 'Напишите findCycles(graph): graph — { узел: [зависимости] } (в зависимостях могут '
               'быть узлы, которых нет среди ключей). Возвращает массив циклов: каждый цикл — это '
               'сильно связная группа узлов размера ≥ 2 либо узел со ссылкой на самого себя; '
               'внутри группы имена отсортированы по алфавиту; группы отсортированы по первому '
               'имени. Нет циклов — пустой массив.',
  'starter': 'function findCycles(graph) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (g) => console.log(JSON.stringify(findCycles(g)));\n'
            'show({ a: ["b"], b: ["c"], c: [] });\n'
            'show({ a: ["b"], b: ["a"] });\n'
            'show({ a: ["a"] });\n'
            'show({ a: ["b"], b: ["c"], c: ["a"], d: ["e"], e: ["d"], f: ["a"] });\n'
            'show({ x: ["y", "z"], y: ["z"], z: ["x"], q: [] });\n'
            'show({ a: ["ghost"], b: ["a"] });\n'
            'show({});\n',
  'hint': 'Алгоритм Тарьяна (компоненты сильной связности) или взаимная достижимость.',
  'expected': ['[]',
               '[["a","b"]]',
               '[["a"]]',
               '[["a","b","c"],["d","e"]]',
               '[["x","y","z"]]',
               '[]',
               '[]']},
 {'id': 'j24-install-order',
  'mode': 'js',
  'title': 'Порядок установки',
  'statement': 'Напишите installOrder(graph): graph — { пакет: [зависимости] }. Вернуть массив '
               'всех пакетов (ключи и упомянутые зависимости) в порядке установки: каждая '
               'зависимость раньше зависящего от неё. Среди доступных к установке (все зависимости '
               'уже установлены) всегда выбирается первый по алфавиту. При цикле — бросить '
               "Error('cycle: ' + список оставшихся пакетов через «, » по алфавиту).",
  'starter': 'function installOrder(graph) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (g) => { try { console.log(installOrder(g).join(" ")); } catch (e) { '
            'console.log("!" + e.message); } };\n'
            't({ app: ["b", "a"], a: ["c"], b: ["c"], c: [] });\n'
            't({ z: [], y: [], x: ["z"] });\n'
            't({ app: ["ghost"] });\n'
            't({ a: ["b"], b: ["a"], c: [] });\n'
            't({ a: ["b"], b: ["c"], c: ["a"], d: ["a"] });\n'
            't({});\n',
  'hint': 'Алгоритм Кана с выбором минимального имени на каждом шаге.',
  'expected': ['c a b app', 'y z x', 'ghost app', '!cycle: a, b', '!cycle: a, b, c, d']},
 {'id': 'j24-duplicates',
  'mode': 'js',
  'title': 'Дубликаты в дереве',
  'statement': 'Напишите findDuplicates(tree): tree — { путь установки: версия } (например '
               '«node_modules/a/node_modules/c»: «1.0.0»). Имя пакета — часть после последнего '
               '«node_modules/». Верните объект «имя → массив версий» только для пакетов, '
               'установленных в двух и более разных версиях; версии без повторов и отсортированы '
               'по semver (по возрастанию); ключи — по алфавиту. Функции parseV и cmpV для '
               'сравнения версий уже есть.',
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
             'function findDuplicates(tree) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (t) => console.log(JSON.stringify(findDuplicates(t)));\n'
            'show({ "node_modules/a": "1.0.0", "node_modules/b": "1.0.0", '
            '"node_modules/b/node_modules/c": "2.0.0", "node_modules/c": "1.2.0", '
            '"node_modules/a/node_modules/c": "2.0.0" });\n'
            'show({ "node_modules/x": "1.0.0", "node_modules/y/node_modules/x": "1.0.0" });\n'
            'show({ "node_modules/@s/p": "1.10.0", "node_modules/q/node_modules/@s/p": "1.9.0", '
            '"node_modules/r/node_modules/@s/p": "1.9.0" });\n'
            'show({});\n',
  'hint': 'Сгруппируйте по имени, соберите Set версий, отфильтруйте size > 1, отсортируйте cmpV.',
  'expected': ['{"c":["1.2.0","2.0.0"]}', '{}', '{"@s/p":["1.9.0","1.10.0"]}', '{}']},
 {'id': 'j24-lock-serialize',
  'mode': 'js',
  'title': 'Сериализация lock-файла',
  'statement': 'Напишите serializeLock(tree) (node:crypto): tree — { путь установки: версия }. '
               'Результат — строка JSON с отступом 2 пробела: { "lockfileVersion": 1, "packages": '
               '{ путь: { "version": v, "integrity": i } } } — пути отсортированы по алфавиту. '
               'integrity = «sha256-» + base64(sha256 от строки `${имя}@${версия}`), имя — часть '
               'после последнего «node_modules/». В конце строки перевод строки.',
  'starter': 'import { createHash } from "node:crypto";\nfunction serializeLock(tree) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const out = serializeLock({ "node_modules/b": "2.0.0", "node_modules/a": "1.0.0", '
            '"node_modules/b/node_modules/c": "0.1.0" });\n'
            'console.log(out);\n'
            'console.log(out.endsWith("}\\n"), JSON.parse(out).lockfileVersion);\n'
            'console.log(serializeLock({}));\n',
  'hint': "createHash('sha256').update(...).digest('base64'); JSON.stringify(obj, null, 2) + "
          "'\\n'.",
  'expected': ['{',
               '  "lockfileVersion": 1,',
               '  "packages": {',
               '    "node_modules/a": {',
               '      "version": "1.0.0",',
               '      "integrity": "sha256-0NRAQ7DDqPSIIXeYVKh+I35inJPOzSpc+R7UbFBPVYI="',
               '    },',
               '    "node_modules/b": {',
               '      "version": "2.0.0",',
               '      "integrity": "sha256-Gv0XQ+Mbbjv++uHmIIbA9vDT1LRuQjEe8jq7eJoV8Ws="',
               '    },',
               '    "node_modules/b/node_modules/c": {',
               '      "version": "0.1.0",',
               '      "integrity": "sha256-ryCh0Oz1c7l5nAtvWdioQhLfUiVPFINp/AzfJuZrO0E="',
               '    }',
               '  }',
               '}',
               '',
               'true 1',
               '{',
               '  "lockfileVersion": 1,',
               '  "packages": {}',
               '}']},
 {'id': 'j24-lock-check',
  'mode': 'js',
  'title': 'Проверка lock-файла (npm ci)',
  'statement': 'Напишите checkLock(manifest, lock): manifest — { dependencies, devDependencies }, '
               'lock — { packages: { путь: { version } } }. Для каждой зависимости из обоих '
               'разделов (имя — ключ) проверьте корневую установку '
               "lock.packages['node_modules/имя']. Нет — «имя: missing from lock». Есть, но версия "
               'не подходит под диапазон — «имя: lock has ВЕРСИЯ, manifest wants ДИАПАЗОН». '
               'Верните массив проблем, отсортированный по строке. satisfies, parseV и cmpV уже '
               'есть в заготовке.',
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
             'function checkLock(manifest, lock) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const lock = { packages: { "node_modules/a": { version: "1.2.3" }, "node_modules/b": '
            '{ version: "2.0.0" }, "node_modules/c": { version: "0.3.1" } } };\n'
            'const show = (m) => console.log(JSON.stringify(checkLock(m, lock)));\n'
            'show({ dependencies: { a: "^1.0.0", b: "^2.0.0" } });\n'
            'show({ dependencies: { a: "^2.0.0", d: "*" }, devDependencies: { c: "~0.3.0", e: '
            '"1.0.0", b: "<2.0.0" } });\n'
            'show({});\n'
            'show({ devDependencies: { z: "^1.0.0", y: "^1.0.0" } });\n',
  'hint': 'Объедините dependencies и devDependencies; при совпадении имён проверьте оба диапазона '
          '(две проблемы возможны).',
  'expected': ['[]',
               '["a: lock has 1.2.3, manifest wants ^2.0.0","b: lock has 2.0.0, manifest wants '
               '<2.0.0","d: missing from lock","e: missing from lock"]',
               '[]',
               '["y: missing from lock","z: missing from lock"]']},
 {'id': 'j24-lock-diff',
  'mode': 'js',
  'title': 'Различие lock-файлов',
  'statement': 'Напишите diffLock(oldTree, newTree): деревья — { путь установки: версия }. '
               'Результат { added, removed, changed }: added — строки «путь@версия» для путей, '
               'которых не было; removed — «путь@версия» для исчезнувших; changed — объекты { '
               'path, from, to } для путей с другой версией. Все списки отсортированы по пути.',
  'starter': 'function diffLock(oldTree, newTree) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const o = { "node_modules/a": "1.0.0", "node_modules/b": "1.0.0", "node_modules/c": '
            '"1.0.0" };\n'
            'const n = { "node_modules/a": "1.1.0", "node_modules/b": "1.0.0", "node_modules/d": '
            '"0.1.0", "node_modules/b/node_modules/x": "2.0.0" };\n'
            'console.log(JSON.stringify(diffLock(o, n)));\n'
            'console.log(JSON.stringify(diffLock(o, o)));\n'
            'console.log(JSON.stringify(diffLock({}, n)));\n',
  'hint': 'Объединённое множество ключей, сортировка, ветвление по наличию в обоих деревьях.',
  'expected': ['{"added":["node_modules/b/node_modules/x@2.0.0","node_modules/d@0.1.0"],"removed":["node_modules/c@1.0.0"],"changed":[{"path":"node_modules/a","from":"1.0.0","to":"1.1.0"}]}',
               '{"added":[],"removed":[],"changed":[]}',
               '{"added":["node_modules/a@1.1.0","node_modules/b@1.0.0","node_modules/b/node_modules/x@2.0.0","node_modules/d@0.1.0"],"removed":[],"changed":[]}']},
 {'id': 'j24-script-plan',
  'mode': 'js',
  'title': 'Хуки pre и post',
  'statement': 'Напишите scriptPlan(scripts, name): возвращает массив имён скриптов в порядке '
               'выполнения: «pre» + name (если есть), name, «post» + name (если есть). Если '
               "скрипта name нет — бросить Error('Missing script: ' + name). У хуков собственных "
               "хуков нет: scriptPlan(s, 'prebuild') возвращает только ['prebuild'] (если он "
               'существует).',
  'starter': 'function scriptPlan(scripts, name) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const scripts = { build: "x", prebuild: "y", postbuild: "z", test: "t", pretest: "p", '
            'start: "s", prepare: "q" };\n'
            'const t = (n) => { try { console.log(n, JSON.stringify(scriptPlan(scripts, n))); } '
            'catch (e) { console.log(n, "!" + e.message); } };\n'
            't("build"); t("test"); t("start"); t("prebuild"); t("prepare"); t("lint"); '
            't("pretest");\n',
  'hint': 'Проверьте существование через Object.hasOwn; хуки добавляйте только для запрошенного '
          'имени.',
  'expected': ['build ["prebuild","build","postbuild"]',
               'test ["pretest","test"]',
               'start ["start"]',
               'prebuild ["prebuild"]',
               'prepare ["prepare"]',
               'lint !Missing script: lint',
               'pretest ["pretest"]']},
 {'id': 'j24-bin-path',
  'mode': 'js',
  'title': 'PATH для скриптов',
  'statement': 'Напишите binPath(cwd, pathEnv): cwd — абсолютный путь (POSIX, без завершающего '
               '«/», кроме корня «/»), pathEnv — значение PATH (может быть пустой строкой или '
               'undefined). Верните строку: для каждого предка каталога, от cwd к корню '
               'включительно — «<каталог>/node_modules/.bin» (для корня — «/node_modules/.bin»), '
               'затем элементы исходного PATH; всё соединено «:». Пустой PATH не добавляет пустых '
               'элементов.',
  'starter': 'function binPath(cwd, pathEnv) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(binPath("/home/u/app", "/usr/bin:/bin"));\n'
            'console.log(binPath("/app", ""));\n'
            'console.log(binPath("/", undefined));\n'
            'console.log(binPath("/a/b/c/d", "/x"));\n',
  'hint': "Идите вверх по split('/'); для корня каталог — пустая строка.",
  'expected': ['/home/u/app/node_modules/.bin:/home/u/node_modules/.bin:/home/node_modules/.bin:/node_modules/.bin:/usr/bin:/bin',
               '/app/node_modules/.bin:/node_modules/.bin',
               '/node_modules/.bin',
               '/a/b/c/d/node_modules/.bin:/a/b/c/node_modules/.bin:/a/b/node_modules/.bin:/a/node_modules/.bin:/node_modules/.bin:/x']},
 {'id': 'j24-workspace',
  'mode': 'js',
  'title': 'Протокол workspace:',
  'statement': 'Напишите resolveWorkspaceRefs(pkgs): pkgs — { имя: { version, dependencies } }. '
               'Верните новую структуру той же формы, в которой значения «workspace:…» в '
               'dependencies заменены на настоящие: «workspace:*» → точная версия '
               'пакета-зависимости из pkgs; «workspace:^» → «^версия»; «workspace:~» → «~версия»; '
               '«workspace:диапазон» → сам диапазон. Если пакета нет в pkgs — бросить '
               "Error('Workspace package not found: ' + имя). Остальные значения не менять, "
               'исходные объекты не мутировать.',
  'starter': 'function resolveWorkspaceRefs(pkgs) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const pkgs = {\n'
            '  "@my/ui": { version: "1.4.0", dependencies: { react: "^18.0.0" } },\n'
            '  "@my/api": { version: "2.0.1", dependencies: { "@my/ui": "workspace:*", zod: '
            '"^3.0.0" } },\n'
            '  web: { version: "0.1.0", dependencies: { "@my/ui": "workspace:^", "@my/api": '
            '"workspace:~", react: "^18.0.0" } },\n'
            '  cli: { version: "0.0.1", dependencies: { "@my/api": "workspace:>=2.0.0" } },\n'
            '};\n'
            'const out = resolveWorkspaceRefs(pkgs);\n'
            'for (const n of Object.keys(out)) console.log(n, '
            'JSON.stringify(out[n].dependencies));\n'
            'console.log(pkgs.web.dependencies["@my/ui"]);\n'
            'try { resolveWorkspaceRefs({ a: { version: "1.0.0", dependencies: { ghost: '
            '"workspace:*" } } }); } catch (e) { console.log(e.message); }\n',
  'hint': 'Для каждой зависимости: если значение начинается с «workspace:» — отрежьте префикс и '
          'разберите остаток.',
  'expected': ['@my/ui {"react":"^18.0.0"}',
               '@my/api {"@my/ui":"1.4.0","zod":"^3.0.0"}',
               'web {"@my/ui":"^1.4.0","@my/api":"~2.0.1","react":"^18.0.0"}',
               'cli {"@my/api":">=2.0.0"}',
               'workspace:^',
               'Workspace package not found: ghost']},
 {'id': 'j24-pack-files',
  'mode': 'js',
  'title': 'Состав публикуемого пакета',
  'statement': 'Напишите packFiles(allFiles, pkg): allFiles — пути файлов проекта (POSIX, '
               'относительные), pkg.files — необязательный массив шаблонов: точный путь '
               '(«index.js»), каталог («dist» — всё внутри него) или «*.ext» (файлы с расширением '
               'в корне, без вложенных каталогов). Всегда включаются: package.json и файлы в '
               'корне, чьё имя (без расширения, без учёта регистра) — README или LICENSE или '
               'LICENCE. Всегда исключаются: всё внутри node_modules/ и .git/, файлы «.DS_Store» '
               '(в любом каталоге) и файлы, оканчивающиеся на «~». Если pkg.files не задан — '
               'включаются все файлы, кроме исключённых. Результат отсортирован.',
  'starter': 'function packFiles(allFiles, pkg) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const all = ["package.json", "README.md", "license", "LICENSE.txt", "CHANGELOG.md", '
            '"index.js", "src/a.js", "src/b.js", "dist/index.js", "dist/lib/x.js", '
            '"test/a.test.js", "notes.md", "node_modules/x/i.js", ".git/HEAD", ".DS_Store", '
            '"src/.DS_Store", "tmp~", "docs/README.md"];\n'
            'const t = (p) => console.log(JSON.stringify(packFiles(all, p)));\n'
            't({ files: ["dist", "index.js"] });\n'
            't({ files: ["*.md"] });\n'
            't({ files: ["src/a.js", "nothing"] });\n'
            't({});\n'
            't({ files: [] });\n',
  'hint': 'Сначала исключения, затем всегда-включаемые, затем шаблоны files.',
  'expected': ['["LICENSE.txt","README.md","dist/index.js","dist/lib/x.js","index.js","license","package.json"]',
               '["CHANGELOG.md","LICENSE.txt","README.md","license","notes.md","package.json"]',
               '["LICENSE.txt","README.md","license","package.json","src/a.js"]',
               '["CHANGELOG.md","LICENSE.txt","README.md","dist/index.js","dist/lib/x.js","docs/README.md","index.js","license","notes.md","package.json","src/a.js","src/b.js","test/a.test.js"]',
               '["LICENSE.txt","README.md","license","package.json"]']},
 {'id': 'j24-peers',
  'mode': 'js',
  'title': 'Проверка peerDependencies',
  'statement': 'Напишите checkPeers(installed, packages): installed — { имя: версия }, packages — '
               '{ имя: { peerDependencies: { пир: диапазон } } } (для установленных пакетов). Для '
               'каждого установленного пакета и каждого его пира: пира нет в installed — «пакет: '
               'missing peer пир@диапазон»; версия пира не подходит — «пакет: peer пир@диапазон '
               'but ВЕРСИЯ installed». Результат — отсортированный массив строк. Помощники '
               'satisfies/parseV/cmpV уже есть.',
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
             'function checkPeers(installed, packages) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const installed = { react: "18.2.0", "react-dom": "18.2.0", "lib-a": "1.0.0", '
            '"lib-b": "2.0.0", "lib-c": "1.0.0" };\n'
            'const packages = {\n'
            '  "lib-a": { peerDependencies: { react: ">=17.0.0 <19.0.0", "react-dom": "^18.0.0" } '
            '},\n'
            '  "lib-b": { peerDependencies: { react: "^16.0.0", vue: "^3.0.0" } },\n'
            '  "lib-c": {},\n'
            '  ghost: { peerDependencies: { react: "^1.0.0" } },\n'
            '};\n'
            'console.log(JSON.stringify(checkPeers(installed, packages)));\n'
            'console.log(JSON.stringify(checkPeers({}, {})));\n',
  'hint': 'Обойдите packages (только те, что есть в installed).',
  'expected': ['["lib-b: missing peer vue@^3.0.0","lib-b: peer react@^16.0.0 but 18.2.0 '
               'installed"]',
               '[]']},
 {'id': 'j24-outdated',
  'mode': 'js',
  'title': 'Устаревшие зависимости',
  'statement': 'Напишите outdated(installed, latest): installed и latest — { имя: версия } (без '
               'предрелизов). Верните массив { name, current, latest, type } для пакетов, у '
               "которых latest новее current; type — 'major', 'minor' или 'patch' по самой старшей "
               'отличающейся части. Отсортируйте по имени. Пакеты без записи в latest '
               'пропускаются. Помощники parseV и cmpV уже есть.',
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
             'function outdated(installed, latest) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const installed = { a: "1.0.0", b: "2.3.4", c: "0.9.0", d: "1.2.3", e: "3.0.0", f: '
            '"1.0.0" };\n'
            'const latest = { a: "2.0.0", b: "2.4.0", c: "0.9.1", d: "1.2.3", e: "2.9.9", z: '
            '"1.0.0" };\n'
            'console.log(JSON.stringify(outdated(installed, latest)));\n'
            'console.log(JSON.stringify(outdated({}, {})));\n',
  'hint': 'Сравните cmpV(latest, current) > 0; тип — первая отличающаяся из major/minor/patch.',
  'expected': ['[{"name":"a","current":"1.0.0","latest":"2.0.0","type":"major"},{"name":"b","current":"2.3.4","latest":"2.4.0","type":"minor"},{"name":"c","current":"0.9.0","latest":"0.9.1","type":"patch"}]',
               '[]']},
 {'id': 'j24-audit',
  'mode': 'js',
  'title': 'Отчёт аудита',
  'statement': 'Напишите audit(installed, advisories): installed — { имя: версия }, advisories — '
               'массив { id, name, range, severity } (severity: low, moderate, high, critical; '
               'range — диапазон уязвимых версий). Верните { vulnerabilities, counts }. '
               'vulnerabilities — для каждой пары (пакет, совет), где версия установленного пакета '
               'попадает в range: { name, version, id, severity }; отсортированы по убыванию '
               'серьёзности (critical → low), затем по имени, затем по id. counts — { low, '
               'moderate, high, critical }: число уязвимостей каждой серьёзности (нули тоже). '
               'satisfies, parseV, cmpV уже есть.',
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
             'function audit(installed, advisories) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const installed = { lodash: "4.17.15", ms: "2.0.0", zod: "3.22.0", left: "1.0.0" };\n'
            'const advisories = [\n'
            '  { id: "A1", name: "lodash", range: "<4.17.21", severity: "high" },\n'
            '  { id: "A2", name: "lodash", range: "<4.17.12", severity: "critical" },\n'
            '  { id: "A3", name: "ms", range: "<2.1.3", severity: "moderate" },\n'
            '  { id: "A4", name: "zod", range: ">=3.0.0 <3.22.0", severity: "low" },\n'
            '  { id: "A5", name: "ghost", range: "*", severity: "critical" },\n'
            '  { id: "A6", name: "left", range: "<2.0.0", severity: "moderate" },\n'
            '];\n'
            'const r = audit(installed, advisories);\n'
            'console.log(JSON.stringify(r));\n'
            'console.log(JSON.stringify(audit({}, [])));\n',
  'hint': 'Ранги серьёзности: critical 0, high 1, moderate 2, low 3 — для сортировки.',
  'expected': ['{"vulnerabilities":[{"name":"lodash","version":"4.17.15","id":"A1","severity":"high"},{"name":"left","version":"1.0.0","id":"A6","severity":"moderate"},{"name":"ms","version":"2.0.0","id":"A3","severity":"moderate"}],"counts":{"low":0,"moderate":2,"high":1,"critical":0}}',
               '{"vulnerabilities":[],"counts":{"low":0,"moderate":0,"high":0,"critical":0}}']},
 {'id': 'j24-update-policy',
  'mode': 'js',
  'title': 'Политика обновлений',
  'statement': 'Напишите pickUpdate(current, available, policy): available — массив версий, policy '
               "— 'patch', 'minor' или 'latest'. Выберите наибольшую версию из available, которая "
               "строго новее current и разрешена политикой: 'patch' — те же major и minor; 'minor' "
               "— тот же major; 'latest' — любая. Предрелизы (версии с «-») и некорректные версии "
               'не рассматриваются. Нет подходящей — null. Помощники parseV и cmpV есть.',
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
             'function pickUpdate(current, available, policy) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const av = ["1.2.4", "1.2.9", "1.3.0", "1.9.9", "2.0.0", "2.1.0-beta.1", '
            '"3.0.0-rc.1", "1.2.3", "1.0.0", "bad"];\n'
            'const t = (c, p) => console.log(c, p, pickUpdate(c, av, p));\n'
            't("1.2.3", "patch"); t("1.2.3", "minor"); t("1.2.3", "latest"); t("1.9.9", "minor"); '
            't("1.9.9", "patch"); t("2.0.0", "latest"); t("0.1.0", "patch");\n',
  'hint': 'Отфильтруйте по политике и по cmpV, затем возьмите максимум.',
  'expected': ['1.2.3 patch 1.2.9',
               '1.2.3 minor 1.9.9',
               '1.2.3 latest 2.0.0',
               '1.9.9 minor null',
               '1.9.9 patch null',
               '2.0.0 latest null',
               '0.1.0 patch null']},
 {'id': 'j24-tree-size',
  'mode': 'js',
  'title': 'Размер дерева и дубликаты',
  'statement': 'Напишите treeSize(tree, sizes): tree — { путь установки: версия }, sizes — { '
               "'имя@версия': байты } (имя — часть после последнего «node_modules/»). Результат: { "
               'total, unique, wasted }. total — сумма размеров по всем путям установки; unique — '
               'число различных «имя@версия»; wasted — total минус сумма размеров различных '
               '«имя@версия» (то есть место, занятое лишними копиями). Если размера нет в sizes — '
               'считайте 0.',
  'starter': 'function treeSize(tree, sizes) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const tree = { "node_modules/a": "1.0.0", "node_modules/b": "1.0.0", '
            '"node_modules/b/node_modules/a": "1.0.0", "node_modules/c/node_modules/a": "2.0.0", '
            '"node_modules/@s/p": "1.0.0" };\n'
            'const sizes = { "a@1.0.0": 100, "a@2.0.0": 150, "b@1.0.0": 50, "@s/p@1.0.0": 30 };\n'
            'console.log(JSON.stringify(treeSize(tree, sizes)));\n'
            'console.log(JSON.stringify(treeSize({}, sizes)));\n'
            'console.log(JSON.stringify(treeSize({ "node_modules/x": "1.0.0", '
            '"node_modules/y/node_modules/x": "1.0.0" }, {})));\n',
  'hint': 'Map/Set различных ключей; total накапливайте по путям.',
  'expected': ['{"total":430,"unique":4,"wasted":100}',
               '{"total":0,"unique":0,"wasted":0}',
               '{"total":0,"unique":1,"wasted":0}']},
 {'id': 'j24-phantoms',
  'mode': 'js',
  'title': 'Поиск фантомных зависимостей',
  'statement': 'Напишите findPhantoms(imports, manifest, hoisted): imports — спецификаторы из кода '
               '(«zod», «zod/v3», «@scope/pkg/x», «./local», «node:fs», «fs»); manifest — { '
               'dependencies, devDependencies, peerDependencies }; hoisted — массив имён пакетов, '
               'физически лежащих в корневом node_modules. Для каждого уникального имени пакета из '
               'imports (имя — «x» или «@s/x», без подпути; относительные «./», «../», «/» и '
               '«node:…» игнорируются, как и встроенные модули fs, path, os, http, crypto, util, '
               'url, events, stream) не объявленного в манифесте — { name, reason }: reason '
               "'hoisted', если имя есть в hoisted (импорт работает случайно), иначе 'missing'. "
               'Результат отсортирован по имени.',
  'starter': 'function findPhantoms(imports, manifest, hoisted) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const imports = ["zod", "zod/v3", "ms", "./local", "../up", "/abs", "node:fs", "fs", '
            '"@s/p/x", "@s/p", "lodash/fp", "react", "path", "@t/q"];\n'
            'const manifest = { dependencies: { zod: "^3" }, devDependencies: { react: "^18" }, '
            'peerDependencies: { "@t/q": "*" } };\n'
            'console.log(JSON.stringify(findPhantoms(imports, manifest, ["ms", "zod", '
            '"react"])));\n'
            'console.log(JSON.stringify(findPhantoms(["x"], {}, [])));\n'
            'console.log(JSON.stringify(findPhantoms([], manifest, [])));\n',
  'hint': 'Выделите имя пакета регулярным выражением, соберите Set, проверьте объявления.',
  'expected': ['[{"name":"@s/p","reason":"missing"},{"name":"lodash","reason":"missing"},{"name":"ms","reason":"hoisted"}]',
               '[{"name":"x","reason":"missing"}]',
               '[]']},
 {'id': 'j24-exports',
  'mode': 'js',
  'title': 'Карта exports пакета',
  'statement': 'Напишите resolveExports(exports, subpath, conditions). exports — строка (то же, '
               "что { '.': строка }), объект условий (ключи без «.» — то же, что { '.': объект }) "
               "или карта подпутей (ключи начинаются с «.»). subpath — '.' или './что-то'. Цель — "
               'строка, объект условий или null. В объекте условий проходим ключи в порядке '
               "записи: подходит ключ 'default' или ключ из conditions — берём его значение "
               '(рекурсивно, если это объект); если ни один не подошёл — бросаем ошибку. Подпуть '
               "сначала ищется точно, затем по шаблону с «*» (ключ вида './features/*' — "
               'подстановка совпавшей части вместо «*» в цели). Нет подпути или цель null — '
               'Error(\'Package subpath "\' + subpath + \'" is not defined by "exports"\').',
  'starter': 'function resolveExports(exports, subpath, conditions) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (e, s, c) => { try { console.log(s, c.join("+"), "→", resolveExports(e, s, '
            'c)); } catch (err) { console.log(s, "!", err.message); } };\n'
            'const map = {\n'
            '  ".": { import: "./esm/index.js", require: "./cjs/index.cjs", default: "./index.js" '
            '},\n'
            '  "./utils": "./src/utils.js",\n'
            '  "./features/*": { node: "./node/features/*.js", default: "./src/features/*.js" },\n'
            '  "./private": null,\n'
            '  "./cond": { browser: { import: "./b.mjs", default: "./b.js" }, default: "./n.js" '
            '},\n'
            '};\n'
            't(map, ".", ["import"]); t(map, ".", ["require"]); t(map, ".", []); t(map, "./utils", '
            '["import"]);\n'
            't(map, "./features/a", ["node"]); t(map, "./features/b/c", []); t(map, "./private", '
            '[]); t(map, "./missing", []);\n'
            't(map, "./cond", ["browser", "import"]); t(map, "./cond", ["browser"]); t(map, '
            '"./cond", ["node"]);\n'
            't("./main.js", ".", []); t({ import: "./m.mjs", default: "./m.js" }, ".", '
            '["import"]); t("./main.js", "./sub", []);\n'
            't({ node: "./n.js" }, ".", ["browser"]);\n',
  'hint': 'Нормализуйте exports к карте подпутей; затем функция target(value, conditions) для '
          'условий.',
  'expected': ['. import → ./esm/index.js',
               '. require → ./cjs/index.cjs',
               '.  → ./index.js',
               './utils import → ./src/utils.js',
               './features/a node → ./node/features/a.js',
               './features/b/c  → ./src/features/b/c.js',
               './private ! Package subpath "./private" is not defined by "exports"',
               './missing ! Package subpath "./missing" is not defined by "exports"',
               './cond browser+import → ./b.mjs',
               './cond browser → ./b.js',
               './cond node → ./n.js',
               '.  → ./main.js',
               '. import → ./m.mjs',
               './sub ! Package subpath "./sub" is not defined by "exports"',
               '. ! Package subpath "." is not defined by "exports"']},
 {'id': 'j24-npmrc',
  'mode': 'js',
  'title': 'Разбор .npmrc',
  'statement': 'Напишите parseNpmrc(text, env). Строки вида «ключ=значение» (пробелы вокруг '
               'обрезаются); строки, начинающиеся с «;» или «#», и пустые пропускаются. В '
               'значениях «${ИМЯ}» заменяется на env[ИМЯ] (нет — пустая строка). Результат { '
               'registry, scopes, auth, other }: «registry=URL» → registry; «@scope:registry=URL» '
               "→ scopes['@scope']; «//host/path/:_authToken=T» → auth['//host/path/'] = T; "
               "остальные пары — в other. registry по умолчанию 'https://registry.npmjs.org/'. При "
               'повторе ключа побеждает последний.',
  'starter': 'function parseNpmrc(text, env) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const text = `\n'
            '; comment\n'
            '# another\n'
            'registry = https://registry.example.com/\n'
            '@my:registry=https://npm.my.example/\n'
            '//npm.my.example/:_authToken=\\${NPM_TOKEN}\n'
            '//other.example/pkg/:_authToken=literal-token\n'
            'save-exact=true\n'
            'progress = false\n'
            'registry=https://final.example/\n'
            'bad line without equals\n'
            'empty=\n'
            '`;\n'
            'console.log(JSON.stringify(parseNpmrc(text, { NPM_TOKEN: "s3cr3t" })));\n'
            'console.log(JSON.stringify(parseNpmrc("//h/:_authToken=${MISSING}", {})));\n'
            'console.log(JSON.stringify(parseNpmrc("", {})));\n',
  'hint': 'Разбейте по строкам, найдите первый «=», затем классифицируйте ключ.',
  'expected': ['{"registry":"https://final.example/","scopes":{"@my":"https://npm.my.example/"},"auth":{"//npm.my.example/":"s3cr3t","//other.example/pkg/":"literal-token"},"other":{"save-exact":"true","progress":"false","empty":""}}',
               '{"registry":"https://registry.npmjs.org/","scopes":{},"auth":{"//h/":""},"other":{}}',
               '{"registry":"https://registry.npmjs.org/","scopes":{},"auth":{},"other":{}}']},
 {'id': 'j24-content-store',
  'mode': 'js',
  'title': 'Хранилище по содержимому (как у pnpm)',
  'statement': 'Напишите addToStore(store, files) (node:crypto): store — объект «sha256-хеш (hex) '
               '→ размер в байтах», files — { путь: содержимое-строка }. Для каждого файла '
               'вычислите sha256 hex от UTF-8 содержимого. Верните { paths, added, saved }: paths '
               '— { путь: хеш }; added — число файлов, которых не было в store (и они добавляются '
               'в store с размером в байтах); saved — суммарный размер файлов, уже бывших в store '
               'или повторившихся внутри files (то есть то, что не пришлось хранить повторно). '
               'Файлы обрабатываются в порядке ключей.',
  'starter': 'import { createHash } from "node:crypto";\nfunction addToStore(store, files) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const store = {};\n'
            'const r1 = addToStore(store, { "a/index.js": "console.log(1)", "b/index.js": '
            '"console.log(1)", "a/pkg.json": "{}" });\n'
            'console.log(JSON.stringify(r1), Object.keys(store).length);\n'
            'const r2 = addToStore(store, { "c/x.js": "console.log(1)", "c/y.js": "новый файл" '
            '});\n'
            'console.log(JSON.stringify(r2.paths["c/x.js"] === r1.paths["a/index.js"]), r2.added, '
            'r2.saved, Object.keys(store).length);\n'
            'console.log(JSON.stringify(addToStore(store, {})));\n',
  'hint': 'Buffer.byteLength(content); если хеш уже в store — saved += размер, иначе store[hash] = '
          'размер.',
  'expected': ['{"paths":{"a/index.js":"0a286891c11c056e1ab5bfc25bf5d6b2f5b06d38eac10944f678fd8a2e70c393","b/index.js":"0a286891c11c056e1ab5bfc25bf5d6b2f5b06d38eac10944f678fd8a2e70c393","a/pkg.json":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"added":2,"saved":14} '
               '2',
               'true 1 14 3',
               '{"paths":{},"added":0,"saved":0}']},
 {'id': 'j24-validate-manifest',
  'mode': 'js',
  'title': 'Проверка package.json',
  'statement': 'Напишите validateManifest(pkg) → массив строк-ошибок, отсортированный: «name: '
               'required» (нет или не непустая строка); «version: invalid semver» (нет версии вида '
               'x.y.z[-pre][+build] — «required» не нужен, нет версии тоже «invalid semver»); для '
               'каждого ключа K в dependencies, devDependencies, peerDependencies значение не '
               'строка — «раздел.K: must be a string»; для каждого скрипта — «scripts.K: must be a '
               'string»; «main: must be a string» (если main задан и не строка); «type: must be '
               '"module" or "commonjs"» (если задан и иной); «private: must be a boolean» (если '
               'задан и не boolean). Раздел, не являющийся объектом, — «раздел: must be an object» '
               '(вместо проверки его ключей).',
  'starter': 'function validateManifest(pkg) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (p) => console.log(JSON.stringify(validateManifest(p)));\n'
            't({ name: "app", version: "1.0.0", dependencies: { a: "^1" }, scripts: { test: "x" }, '
            'type: "module", main: "i.js", private: true });\n'
            't({});\n'
            't({ name: "", version: "1.0", dependencies: { a: 1, b: "ok" }, devDependencies: "x", '
            'scripts: { build: 5 } });\n'
            't({ name: "x", version: "2.0.0-rc.1+b5", main: 1, type: "esm", private: "yes", '
            'peerDependencies: { r: null } });\n'
            't({ name: "x", version: "1.0.0", dependencies: null });\n',
  'hint': 'Соберите errors push-ами, в конце sort().',
  'expected': ['[]',
               '["name: required","version: invalid semver"]',
               '["dependencies.a: must be a string","devDependencies: must be an object","name: '
               'required","scripts.build: must be a string","version: invalid semver"]',
               '["main: must be a string","peerDependencies.r: must be a string","private: must be '
               'a boolean","type: must be \\"module\\" or \\"commonjs\\""]',
               '["dependencies: must be an object"]']}]}
