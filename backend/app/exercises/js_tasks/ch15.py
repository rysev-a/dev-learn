"""Задачи книги «Современный Frontend», глава 15 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {15: [{'id': 'j15-specificity',
       'mode': 'js',
       'title': 'Специфичность селектора',
       'statement': 'Напишите функцию specificity(selector) → массив [a, b, c]: a — число идентификаторов '
                    '(#id); b — классов (.x), атрибутов ([x]) и псевдоклассов (:hover, :nth-child(…)); c — '
                    'типов (div) и псевдоэлементов (::before, а также '
                    ':before/:after/:first-line/:first-letter). Универсальный селектор и комбинаторы '
                    '(пробел, >, +, ~) вклад не дают. :not(X), :is(X, Y), :has(X) дают специфичность самого '
                    'специфичного аргумента (сам псевдокласс вклада не даёт), :where(…) — ноль. Селектор без '
                    'запятых.',
       'starter': 'function specificity(selector) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const s of ["li", "ul li", ".item", "ul .item:hover", "#list .item", "*", "a[href]", '
                 '"div > p + span", "p::first-line", "a:before", "li:nth-child(2n+1)", "#a#b.c", ":not(.x)", '
                 '":not(#id, .x)", ":is(h1, .title) span", ":where(#a) p", "ul:has(> li.active)", '
                 '"input:not([type=text]):focus", "html body main article section p.note::after"]) '
                 'console.log(s, JSON.stringify(specificity(s)));\n',
       'hint': 'Вычёркивайте найденные части из строки по очереди: функциональные псевдоклассы, атрибуты, '
               'псевдоэлементы, псевдоклассы, идентификаторы, классы, типы.',
       'expected': ['li [0,0,1]',
                    'ul li [0,0,2]',
                    '.item [0,1,0]',
                    'ul .item:hover [0,2,1]',
                    '#list .item [1,1,0]',
                    '* [0,0,0]',
                    'a[href] [0,1,1]',
                    'div > p + span [0,0,3]',
                    'p::first-line [0,0,2]',
                    'a:before [0,0,2]',
                    'li:nth-child(2n+1) [0,1,1]',
                    '#a#b.c [2,1,0]',
                    ':not(.x) [0,1,0]',
                    ':not(#id, .x) [1,0,0]',
                    ':is(h1, .title) span [0,1,1]',
                    ':where(#a) p [0,0,1]',
                    'ul:has(> li.active) [0,1,2]',
                    'input:not([type=text]):focus [0,2,1]',
                    'html body main article section p.note::after [0,1,7]']},
      {'id': 'j15-cascade',
       'mode': 'js',
       'title': 'Разрешение каскада',
       'statement': 'Объявления для одного свойства: { value, origin: "user-agent"|"user"|"author", '
                    'important?, layer? (номер слоя; чем больше — тем позже объявлен; без слоя — Infinity), '
                    'specificity: [a, b, c], order }. Напишите функцию winner(decls): возвращает value '
                    'победителя по правилам каскада: важные побеждают неважные; среди важных порядок '
                    'источников обратный (user-agent важный > user важный > author важный), среди неважных — '
                    'author > user > user-agent; затем слой (для неважных — выше слой побеждает, без слоя — '
                    'самый сильный; для важных — наоборот, раньше объявленный слой сильнее, а без слоя — '
                    'самый слабый); затем специфичность; затем order (больше — сильнее). Для пустого списка '
                    '— undefined.',
       'starter': 'function winner(decls) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const d = (value, o = {}) => ({ value, origin: "author", specificity: [0, 0, 1], order: 0, '
                 '...o });\n'
                 'const cases = [\n'
                 '  [d("a", { order: 1 }), d("b", { order: 2 })],\n'
                 '  [d("a", { specificity: [0, 1, 0], order: 1 }), d("b", { specificity: [0, 0, 5], order: 2 '
                 '})],\n'
                 '  [d("author"), d("ua", { origin: "user-agent", specificity: [1, 0, 0] })],\n'
                 '  [d("author", { important: false }), d("user!", { origin: "user", important: true })],\n'
                 '  [d("author!", { important: true }), d("user!", { origin: "user", important: true }), '
                 'd("ua!", { origin: "user-agent", important: true })],\n'
                 '  [d("layer1", { layer: 1 }), d("layer2", { layer: 2 }), d("nolayer", { specificity: [0, '
                 '0, 0] })],\n'
                 '  [d("layer1!", { layer: 1, important: true }), d("layer2!", { layer: 2, important: true '
                 '}), d("nolayer!", { important: true })],\n'
                 '  [d("x", { specificity: [0, 2, 0], order: 5 }), d("y", { specificity: [0, 2, 0], order: 3 '
                 '})],\n'
                 '  [d("only")],\n'
                 '  [],\n'
                 '];\n'
                 'cases.forEach((c) => console.log(winner(c)));\n',
       'hint': 'Составьте ключ сравнения: важность, источник, слой, специфичность, порядок.',
       'expected': ['b', 'a', 'author', 'user!', 'ua!', 'nolayer', 'layer1!', 'x', 'only', 'undefined']},
      {'id': 'j15-inheritance',
       'mode': 'js',
       'title': 'Вычисленные стили и наследование',
       'statement': 'Дерево элементов { tag, style: {…}, children } (у корня родителя нет). Наследуются '
                    'свойства: color, font-family, font-size, font-weight, line-height, visibility, cursor, '
                    'text-align; остальные (margin, padding, border, background …) — нет, и по умолчанию '
                    'равны «initial» из таблицы: { color: "black", "font-size": "16px", "font-weight": '
                    '"400", margin: "0", padding: "0", background: "transparent", ... } (для остальных '
                    'неуказанных — undefined). Значения «inherit» берут значение родителя (для корня — '
                    'initial), «initial» — начальное, «unset» — inherit для наследуемых и initial для '
                    'остальных. Напишите функцию computed(tree) → то же дерево с полем computed (объект: все '
                    'свойства из объединённого списка INHERITED + NON_INHERITED с итоговым значением).',
       'starter': 'function computed(tree) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tree = { tag: "html", style: { color: "navy", "font-size": "20px", margin: "8px", '
                 'border: "1px solid" }, children: [\n'
                 '  { tag: "body", children: [\n'
                 '    { tag: "p", style: { color: "red", padding: "4px" }, children: [{ tag: "b", style: { '
                 '"font-weight": "700", margin: "inherit", padding: "unset" }, children: [] }, { tag: "i", '
                 'style: { color: "initial", "font-size": "unset", border: "inherit" }, children: [] }] },\n'
                 '    { tag: "div", style: { display: "flex", background: "yellow" }, children: [{ tag: '
                 '"span", style: {}, children: [] }] },\n'
                 '  ] },\n'
                 '] };\n'
                 'const t = computed(tree);\n'
                 'const show = (n, d = 0) => { const c = n.computed; console.log("  ".repeat(d) + n.tag, '
                 '[c.color, c["font-size"], c["font-weight"], c.margin, c.padding, c.border, c.background, '
                 'c.display].join(" | ")); n.children.forEach((k) => show(k, d + 1)); };\n'
                 'show(t);\n'
                 'console.log(Object.keys(t.computed).length, JSON.stringify(tree).length > 100);\n',
       'hint': 'Для каждого свойства: если значение не задано — наследовать или initial; ключевые слова — по '
               'таблице.',
       'expected': ['html navy | 20px | 400 | 8px | 0 | 1px solid | transparent | inline',
                    '  body navy | 20px | 400 | 0 | 0 | none | transparent | inline',
                    '    p red | 20px | 400 | 0 | 4px | none | transparent | inline',
                    '      b red | 20px | 700 | 0 | 0 | none | transparent | inline',
                    '      i black | 20px | 400 | 0 | 0 | none | transparent | inline',
                    '    div navy | 20px | 400 | 0 | 0 | none | yellow | flex',
                    '      span navy | 20px | 400 | 0 | 0 | none | transparent | inline',
                    '13 true']},
      {'id': 'j15-units',
       'mode': 'js',
       'title': 'Перевод единиц в пиксели',
       'statement': 'Напишите функцию toPx(value, ctx): value — строка вроде «16px», «2rem», «1.5em», «50%», '
                    '«10vw», «20vh», «1in», «2.54cm», «72pt», «0», число без единиц (кроме 0 — SyntaxError); '
                    'ctx = { rootFont: 16, font: 16 (шрифт элемента), parent: 400 (база для %), vw: 1000, '
                    'vh: 800 }; 1in = 96px, 1cm = 96/2.54 px, 1pt = 96/72 px. Результат — число, округлённое '
                    'до 2 знаков. Неизвестная единица — SyntaxError. Поддержите отрицательные значения и '
                    'дробные без ведущего нуля («.5em»).',
       'starter': 'function toPx(value, ctx) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const ctx = { rootFont: 16, font: 20, parent: 400, vw: 1000, vh: 800 };\n'
                 'for (const v of ["16px", "2rem", "1.5em", "50%", "10vw", "20vh", "1in", "2.54cm", "72pt", '
                 '"0", "-2em", ".5em", "+3px", "12.345px", " 8px "]) console.log(JSON.stringify(v), toPx(v, '
                 'ctx));\n'
                 'for (const v of ["12", "5furlongs", "px", "", "1.2.3px"]) { try { toPx(v, ctx); '
                 'console.log("принято?", v); } catch (e) { console.log(JSON.stringify(v), e.name); } }\n'
                 'console.log(toPx("1rem", { ...ctx, rootFont: 10 }), toPx("100%", { ...ctx, parent: 250 '
                 '}));\n',
       'hint': 'Регулярное выражение: число и единица; таблица множителей.',
       'expected': ['"16px" 16',
                    '"2rem" 32',
                    '"1.5em" 30',
                    '"50%" 200',
                    '"10vw" 100',
                    '"20vh" 160',
                    '"1in" 96',
                    '"2.54cm" 96',
                    '"72pt" 96',
                    '"0" 0',
                    '"-2em" -40',
                    '".5em" 10',
                    '"+3px" 3',
                    '"12.345px" 12.35',
                    '" 8px " 8',
                    '"12" SyntaxError',
                    '"5furlongs" SyntaxError',
                    '"px" SyntaxError',
                    '"" SyntaxError',
                    '"1.2.3px" SyntaxError',
                    '10 250']},
      {'id': 'j15-colors',
       'mode': 'js',
       'title': 'Разбор цвета',
       'statement': 'Напишите функции parseColor(str) → { r, g, b, a } (r, g, b — целые 0–255, a — 0–1, '
                    'округление a до 3 знаков): форматы #rgb, #rgba, #rrggbb, #rrggbbaa, rgb(r, g, b), '
                    'rgba(r, g, b, a), rgb(r g b / a), проценты в rgb (rgb(100%, 0%, 0%)), hsl(h, s%, l%) и '
                    'hsla; имена black, white, red, transparent. toHex(color) → «#rrggbb» или «#rrggbbaa» '
                    'при a < 1. Неверный цвет — SyntaxError.',
       'starter': 'function parseColor(str) {\n}\nfunction toHex(color) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const c of ["#f80", "#f80a", "#ff8800", "#FF880080", "rgb(255, 136, 0)", '
                 '"rgba(0,0,0,.5)", "rgb(255 136 0 / 50%)", "rgb(100%, 0%, 50%)", "hsl(0, 100%, 50%)", '
                 '"hsl(120, 100%, 25%)", "hsla(240, 100%, 50%, 0.25)", "hsl(-120 50% 50%)", "white", '
                 '"Transparent"]) console.log(c, JSON.stringify(parseColor(c)));\n'
                 'for (const c of ["#ff", "rgb(1,2)", "blue", "foo(1,2,3)", "#ggg"]) { try { parseColor(c); '
                 'console.log("принято?", c); } catch (e) { console.log(c, e.name); } }\n'
                 'console.log(toHex({ r: 255, g: 136, b: 0, a: 1 }), toHex({ r: 0, g: 0, b: 0, a: 0.5 }), '
                 'toHex(parseColor("hsl(210, 50%, 40%)")), toHex({ r: 1, g: 2, b: 3 }));\n',
       'hint': 'Для hsl используйте стандартную формулу перевода; для hex с тремя цифрами удвойте каждую.',
       'expected': ['#f80 {"r":255,"g":136,"b":0,"a":1}',
                    '#f80a {"r":255,"g":136,"b":0,"a":0.667}',
                    '#ff8800 {"r":255,"g":136,"b":0,"a":1}',
                    '#FF880080 {"r":255,"g":136,"b":0,"a":0.502}',
                    'rgb(255, 136, 0) {"r":255,"g":136,"b":0,"a":1}',
                    'rgba(0,0,0,.5) {"r":0,"g":0,"b":0,"a":0.5}',
                    'rgb(255 136 0 / 50%) {"r":255,"g":136,"b":0,"a":0.5}',
                    'rgb(100%, 0%, 50%) {"r":255,"g":0,"b":128,"a":1}',
                    'hsl(0, 100%, 50%) {"r":255,"g":0,"b":0,"a":1}',
                    'hsl(120, 100%, 25%) {"r":0,"g":128,"b":0,"a":1}',
                    'hsla(240, 100%, 50%, 0.25) {"r":0,"g":0,"b":255,"a":0.25}',
                    'hsl(-120 50% 50%) {"r":64,"g":64,"b":191,"a":1}',
                    'white {"r":255,"g":255,"b":255,"a":1}',
                    'Transparent {"r":0,"g":0,"b":0,"a":0}',
                    '#ff SyntaxError',
                    'rgb(1,2) SyntaxError',
                    'blue SyntaxError',
                    'foo(1,2,3) SyntaxError',
                    '#ggg SyntaxError',
                    '#ff8800 #00000080 #336699 #010203']},
      {'id': 'j15-contrast',
       'mode': 'js',
       'title': 'Контраст цветов (WCAG)',
       'statement': 'Напишите функции luminance({ r, g, b }) (относительная яркость по WCAG: линеаризация '
                    'sRGB c/255 → c <= 0.03928 ? c/12.92 : ((c+0.055)/1.055)**2.4; 0.2126R + 0.7152G + '
                    '0.0722B), contrastRatio(c1, c2) (( L1 + 0.05 ) / ( L2 + 0.05 ), где L1 ≥ L2; округление '
                    'до 2 знаков) и wcag(c1, c2, { large = false }) → { ratio, AA, AAA }: AA — 4.5 (3 для '
                    'крупного текста), AAA — 7 (4.5 для крупного).',
       'starter': 'function luminance(color) {\n'
                  '}\n'
                  'function contrastRatio(c1, c2) {\n'
                  '}\n'
                  'function wcag(c1, c2, options) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const W = { r: 255, g: 255, b: 255 }, K = { r: 0, g: 0, b: 0 }, G = { r: 119, g: 119, b: '
                 '119 }, B = { r: 0, g: 0, b: 238 }, Y = { r: 255, g: 255, b: 0 };\n'
                 'console.log(luminance(W), luminance(K), luminance(G).toFixed(4), '
                 'luminance(B).toFixed(4));\n'
                 'console.log(contrastRatio(W, K), contrastRatio(K, W), contrastRatio(W, G), '
                 'contrastRatio(W, B), contrastRatio(Y, W), contrastRatio(W, W));\n'
                 'console.log(JSON.stringify(wcag(W, K)), JSON.stringify(wcag(W, G)), JSON.stringify(wcag(W, '
                 'G, { large: true })), JSON.stringify(wcag(W, B)), JSON.stringify(wcag(Y, W, { large: true '
                 '})));\n',
       'hint': 'Сначала линеаризация каждого канала, затем взвешенная сумма.',
       'expected': ['1 0 0.1845 0.0617',
                    '21 21 4.48 9.4 1.07 1',
                    '{"ratio":21,"AA":true,"AAA":true} {"ratio":4.48,"AA":false,"AAA":false} '
                    '{"ratio":4.48,"AA":true,"AAA":false} {"ratio":9.4,"AA":true,"AAA":true} '
                    '{"ratio":1.07,"AA":false,"AAA":false}']},
      {'id': 'j15-calc',
       'mode': 'js',
       'title': 'Вычисление calc, min, max, clamp',
       'statement': 'Напишите функцию evalCss(expr, ctx): выражение может содержать числа с единицами px, '
                    'rem, em, %, vw (перевод как в ctx = { rootFont, font, parent, vw }) — результат всегда '
                    'в px (число с точностью до 2 знаков); операции + - * / со скобками (в сложении и '
                    'вычитании — только длины, в умножении и делении один операнд — безразмерное число); '
                    'функции calc(…), min(a, b, …), max(a, b, …), clamp(min, val, max). Верните число. '
                    'Ошибка (длина × длина, деление на 0, неверная запись) — SyntaxError.',
       'starter': 'function evalCss(expr, ctx) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const ctx = { rootFont: 16, font: 10, parent: 500, vw: 1200 };\n'
                 'for (const e of ["calc(100% - 2rem)", "calc(10px + 2 * 1em)", "min(50%, 300px)", '
                 '"max(1rem, 5vw)", "clamp(16px, 4vw, 32px)", "clamp(1rem, 2vw, 2rem)", "calc((100% - 40px) '
                 '/ 3)", "calc(1px+2px)", "calc(2 * (3px + 1em))", "calc(-1 * 5px)", "min(10px, max(5px, '
                 '3px))"]) console.log(e, "→", evalCss(e, ctx));\n'
                 'for (const e of ["calc(1px * 2px)", "calc(10px / 0)", "calc(10px + 5)", "calc(", '
                 '"foo(1px)", "5", "calc(1px 2px)"]) { try { evalCss(e, ctx); console.log("принято?", e); } '
                 'catch (x) { console.log(e, x.name); } }\n',
       'hint': 'Рекурсивный спуск: сумма → произведение → унарный минус → атом/функция; ведите счётчик '
               '«размерности».',
       'expected': ['calc(100% - 2rem) → 468',
                    'calc(10px + 2 * 1em) → 30',
                    'min(50%, 300px) → 250',
                    'max(1rem, 5vw) → 60',
                    'clamp(16px, 4vw, 32px) → 32',
                    'clamp(1rem, 2vw, 2rem) → 24',
                    'calc((100% - 40px) / 3) → 153.33',
                    'calc(1px+2px) → 3',
                    'calc(2 * (3px + 1em)) → 26',
                    'calc(-1 * 5px) → -5',
                    'min(10px, max(5px, 3px)) → 5',
                    'calc(1px * 2px) SyntaxError',
                    'calc(10px / 0) SyntaxError',
                    'calc(10px + 5) SyntaxError',
                    'calc( SyntaxError',
                    'foo(1px) SyntaxError',
                    '5 SyntaxError',
                    'calc(1px 2px) SyntaxError']},
      {'id': 'j15-box-model',
       'mode': 'js',
       'title': 'Размеры блока',
       'statement': 'Блок: { width, height, padding: [t, r, b, l], border: [t, r, b, l], margin: [t, r, b, '
                    'l], boxSizing }. Напишите функции outerSize(box) → { content: {w, h}, border: {w, h} '
                    '(рамка включая padding и border), margin: {w, h} (с внешними отступами) } для обоих '
                    'значений box-sizing: при content-box width/height — содержимое, при border-box — '
                    'включая padding и border (содержимое не может быть отрицательным: минимум 0); и '
                    'fitInto(box, available) → ширина блока при width: auto (занимает всё доступное: '
                    'available минус внешние отступы, рамки и padding по горизонтали, содержимое минимум 0).',
       'starter': 'function outerSize(box) {\n}\nfunction fitInto(box, available) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const base = { width: 200, height: 100, padding: [10, 20, 10, 20], border: [2, 2, 2, 2], '
                 'margin: [5, 10, 15, 10] };\n'
                 'console.log(JSON.stringify(outerSize({ ...base, boxSizing: "content-box" })));\n'
                 'console.log(JSON.stringify(outerSize({ ...base, boxSizing: "border-box" })));\n'
                 'console.log(JSON.stringify(outerSize({ ...base, boxSizing: "border-box", width: 30, '
                 'height: 10 })));\n'
                 'console.log(fitInto(base, 500), fitInto(base, 60), fitInto({ ...base, padding: [0, 0, 0, '
                 '0], border: [0, 0, 0, 0], margin: [0, 0, 0, 0] }, 320));\n',
       'hint': 'Горизонтальная добавка = padding слева и справа + рамки; для border-box вычитаем её из '
               'width.',
       'expected': ['{"content":{"w":200,"h":100},"border":{"w":244,"h":124},"margin":{"w":264,"h":144}}',
                    '{"content":{"w":156,"h":76},"border":{"w":200,"h":100},"margin":{"w":220,"h":120}}',
                    '{"content":{"w":0,"h":0},"border":{"w":44,"h":24},"margin":{"w":64,"h":44}}',
                    '436 0 320']},
      {'id': 'j15-margin-collapse',
       'mode': 'js',
       'title': 'Схлопывание внешних отступов',
       'statement': 'Вертикальный ряд блоков: массив { mt, mb, empty? (пустой блок — его верхний и нижний '
                    'отступ схлопываются сам с собой) }, расположенных друг за другом в одном родителе без '
                    'padding/border. Правила: между соседями отступ равен max(mb верхнего, mt нижнего), если '
                    'оба положительные; если оба отрицательные — наименьшее (самое «отрицательное»); если '
                    'разных знаков — сумма. Верните gaps(blocks) → массив отступов между соседними блоками. '
                    'И parentChild(parentMt, childMt, hasPadding) → итоговый отступ над родителем: без '
                    'padding/border у родителя верхний отступ родителя схлопывается с отступом первого '
                    'ребёнка по тем же правилам, иначе — они складываются.',
       'starter': 'function gaps(blocks) {\n}\nfunction parentChild(parentMt, childMt, hasPadding) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(gaps([{ mt: 0, mb: 20 }, { mt: 30, mb: 10 }, { mt: 5, mb: 0 '
                 '}])));\n'
                 'console.log(JSON.stringify(gaps([{ mt: 0, mb: -10 }, { mt: -20, mb: 5 }, { mt: 10, mb: 0 '
                 '}])));\n'
                 'console.log(JSON.stringify(gaps([{ mt: 0, mb: 30 }, { mt: -10, mb: 0 }])), '
                 'JSON.stringify(gaps([{ mt: 1, mb: 1 }])), JSON.stringify(gaps([])));\n'
                 'console.log(parentChild(20, 30, false), parentChild(20, 30, true), parentChild(20, -5, '
                 'false), parentChild(-10, -30, false), parentChild(0, 15, false));\n',
       'hint': 'Положительные — максимум, отрицательные — минимум, смешанные — сумма.',
       'expected': ['[30,10]', '[-20,10]', '[20] [] []', '30 50 15 -30 15']},
      {'id': 'j15-flex-row',
       'mode': 'js',
       'title': 'Раскладка flex в одну строку',
       'statement': 'Контейнер шириной W, элементы: { basis, grow, shrink, min? = 0, max? = Infinity }, gap '
                    'между элементами. Напишите функцию flexRow(W, items, gap): шаг 1 — базовые размеры = '
                    'basis; свободное место = W - сумма basis - gap*(n-1); если > 0 — делится '
                    'пропорционально grow (если сумма grow = 0, ничего не растёт); если < 0 — элементы '
                    'сжимаются пропорционально shrink*basis (если сумма = 0, размеры не меняются); затем '
                    'min/max ограничивают: «замороженные» по ограничению элементы исключаются, остаток '
                    'перераспределяется между остальными (цикл до стабилизации). Верните массив итоговых '
                    'размеров, округлённых до 2 знаков.',
       'starter': 'function flexRow(W, items, gap) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const I = (basis, grow = 0, shrink = 1, extra = {}) => ({ basis, grow, shrink, ...extra '
                 '});\n'
                 'const show = (...a) => console.log(JSON.stringify(flexRow(...a)));\n'
                 'show(600, [I(100, 1), I(100, 2), I(100, 1)], 0);\n'
                 'show(600, [I(100, 1), I(100, 1)], 20);\n'
                 'show(300, [I(200), I(200)], 0);\n'
                 'show(300, [I(300, 0, 1), I(100, 0, 0)], 0);\n'
                 'show(500, [I(100), I(100)], 10);\n'
                 'show(600, [I(100, 1, 1, { max: 150 }), I(100, 1)], 0);\n'
                 'show(300, [I(200, 0, 1, { min: 180 }), I(200)], 0);\n'
                 'show(100, [], 0);\n'
                 'show(400, [I(100, 1)], 50);\n',
       'hint': 'Классический алгоритм flexbox: распределение пропорционально весам, затем «заморозка» '
               'нарушивших min/max и повтор.',
       'expected': ['[175,250,175]',
                    '[290,290]',
                    '[150,150]',
                    '[200,100]',
                    '[100,100]',
                    '[150,450]',
                    '[180,120]',
                    '[]',
                    '[400]']},
      {'id': 'j15-flex-justify',
       'mode': 'js',
       'title': 'justify-content и align-items',
       'statement': 'Напишите функцию justify(mode, W, sizes, gap = 0) → массив позиций левых краёв '
                    'элементов вдоль главной оси: flex-start, flex-end, center, space-between, space-around, '
                    'space-evenly (свободное место — W минус сумма размеров и gap*(n-1); если свободного '
                    'места меньше нуля — как flex-start для space-*, для center/flex-end допускается '
                    'отрицательный сдвиг), и align(mode, H, size) → верхняя позиция по поперечной оси: '
                    'flex-start, flex-end, center, stretch (позиция 0, размер H — верните объект { top, size '
                    '}).',
       'starter': 'function justify(mode, W, sizes, gap) {\n}\nfunction align(mode, H, size) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const m of ["flex-start", "flex-end", "center", "space-between", "space-around", '
                 '"space-evenly"]) console.log(m.padEnd(14), JSON.stringify(justify(m, 400, [50, 100, 50], '
                 '0)), JSON.stringify(justify(m, 400, [50, 100, 50], 10)));\n'
                 'console.log(JSON.stringify(justify("space-between", 100, [60, 60], 0)), '
                 'JSON.stringify(justify("center", 100, [60, 60], 0)), '
                 'JSON.stringify(justify("space-around", 300, [100], 0)), '
                 'JSON.stringify(justify("space-between", 300, [100], 0)), JSON.stringify(justify("center", '
                 '300, [], 0)));\n'
                 'for (const m of ["flex-start", "flex-end", "center", "stretch"]) console.log(m, '
                 'JSON.stringify(align(m, 100, 40)));\n',
       'hint': 'Вычислите свободное место, начальный сдвиг и промежуток между элементами для каждого режима.',
       'expected': ['flex-start     [0,50,150] [0,60,170]',
                    'flex-end       [200,250,350] [180,240,350]',
                    'center         [100,150,250] [90,150,260]',
                    'space-between  [0,150,350] [0,150,350]',
                    'space-around   [33.33,150,316.67] [30,150,320]',
                    'space-evenly   [50,150,300] [45,150,305]',
                    '[0,60] [-10,50] [100] [0] []',
                    'flex-start {"top":0,"size":40}',
                    'flex-end {"top":60,"size":40}',
                    'center {"top":30,"size":40}',
                    'stretch {"top":0,"size":100}']},
      {'id': 'j15-flex-wrap',
       'mode': 'js',
       'title': 'flex-wrap: разбиение на строки',
       'statement': 'Контейнер шириной W, элементы с размерами по главной оси (basis), gap между ними. '
                    'Напишите функцию wrapLines(W, sizes, gap) → массив строк (каждая — массив индексов '
                    'элементов): элемент переносится на новую строку, если не помещается в текущую (сумма '
                    'размеров + gap между ними > W), но первый в строке остаётся, даже если шире W. И '
                    'функцию lineHeights(lines, heights, rowGap) → { lines: [высота каждой строки = '
                    'наибольшая высота элемента], total: сумма с rowGap между строками }.',
       'starter': 'function wrapLines(W, sizes, gap) {\n'
                  '}\n'
                  'function lineHeights(lines, heights, rowGap) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(wrapLines(300, [100, 100, 100, 100, 100], 0)), '
                 'JSON.stringify(wrapLines(300, [100, 100, 100, 100, 100], 10)), '
                 'JSON.stringify(wrapLines(300, [400, 50, 250, 60], 0)));\n'
                 'console.log(JSON.stringify(wrapLines(100, [], 0)), JSON.stringify(wrapLines(100, [100, '
                 '100], 0)), JSON.stringify(wrapLines(100, [60, 40], 1)), JSON.stringify(wrapLines(100, [60, '
                 '40], 0)));\n'
                 'const lines = wrapLines(300, [100, 100, 100, 100, 100], 0);\n'
                 'console.log(JSON.stringify(lineHeights(lines, [10, 30, 20, 5, 40], 8)), '
                 'JSON.stringify(lineHeights([[0]], [7], 5)), JSON.stringify(lineHeights([], [], 5)));\n',
       'hint': 'Накапливайте занятую ширину строки; при превышении W начинайте новую.',
       'expected': ['[[0,1,2],[3,4]] [[0,1],[2,3],[4]] [[0],[1,2],[3]]',
                    '[] [[0],[1]] [[0],[1]] [[0,1]]',
                    '{"lines":[30,40],"total":78} {"lines":[7],"total":7} {"lines":[],"total":0}']},
      {'id': 'j15-grid-tracks',
       'mode': 'js',
       'title': 'Размеры треков grid',
       'statement': 'Напишите функцию gridTracks(template, available, gap): template — строка вида «100px '
                    '1fr 2fr», «repeat(3, 1fr)», «minmax(100px, 1fr) 200px», «1fr 1fr». Разбор: '
                    'фиксированные «Npx»; «Nfr»; «minmax(a, b)» (a — минимум в px, b — «Nfr» или «Npx»); '
                    'repeat(N, трек) (N целое). Алгоритм: фиксированные берутся как есть; минимумы minmax '
                    'учитываются; свободное место = available - sum(фиксированных) - gap*(n-1); делится на '
                    'доли fr, но трек minmax не может быть меньше своего минимума (если пропорциональная '
                    'доля меньше — трек замораживается на минимуме, остаток делится между остальными). '
                    'Верните массив размеров (до 2 знаков). Если свободного места нет — fr-треки получают 0 '
                    '(или свой минимум).',
       'starter': 'function gridTracks(template, available, gap) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const show = (...a) => console.log(JSON.stringify(gridTracks(...a)));\n'
                 'show("100px 1fr 2fr", 700, 0);\n'
                 'show("repeat(3, 1fr)", 620, 10);\n'
                 'show("minmax(100px, 1fr) 200px", 500, 0);\n'
                 'show("minmax(300px, 1fr) 1fr 1fr", 600, 0);\n'
                 'show("1fr 1fr", 0, 0);\n'
                 'show("200px minmax(100px, 1fr)", 250, 20);\n'
                 'show("repeat(2, 50px 1fr)", 400, 5);\n'
                 'show("minmax(80px, 250px) 1fr", 500, 0);\n'
                 'try { gridTracks("auto 1fr", 100, 0); } catch (e) { console.log(e.name); }\n',
       'hint': 'Фиксированные вычтите; остаток делится по fr; если доля меньше минимума — трек '
               '«замораживается» на минимуме и расчёт повторяется.',
       'expected': ['[100,200,400]',
                    '[200,200,200]',
                    '[300,200]',
                    '[300,150,150]',
                    '[0,0]',
                    '[200,100]',
                    '[50,142.5,50,142.5]',
                    '[250,250]',
                    'SyntaxError']},
      {'id': 'j15-grid-placement',
       'mode': 'js',
       'title': 'Автоматическое размещение в grid',
       'statement': 'Сетка из columns колонок. Элементы — { name, colSpan = 1, rowSpan = 1 }. Напишите '
                    'функцию place(columns, items, dense = false): размещает элементы по порядку: курсор '
                    'идёт слева направо, сверху вниз; элемент ставится в первое свободное место, начиная с '
                    'текущей позиции курсора (при dense = false курсор не возвращается назад: следующий '
                    'элемент ищется с позиции после предыдущего; при dense = true поиск всегда с самой '
                    'первой ячейки); если колонок не хватает (colSpan > columns) — Error. Верните массив { '
                    'name, row, col } (индексы с 0) и rows — число занятых строк.',
       'starter': 'function place(columns, items, dense) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const I = (name, colSpan, rowSpan) => ({ name, colSpan, rowSpan });\n'
                 'const show = (cols, items, dense) => { const r = place(cols, items, dense); '
                 'console.log(r.rows, r.placed.map((p) => `${p.name}@${p.row},${p.col}`).join(" ")); };\n'
                 'show(3, [I("a"), I("b"), I("c"), I("d")]);\n'
                 'show(3, [I("a", 2), I("b", 2), I("c"), I("d")], false);\n'
                 'show(3, [I("a", 2), I("b", 2), I("c"), I("d")], true);\n'
                 'show(3, [I("a", 1, 2), I("b"), I("c"), I("d"), I("e")]);\n'
                 'show(2, [I("a", 2), I("b", 1, 3), I("c"), I("d")]);\n'
                 'show(4, []);\n'
                 'try { place(2, [I("x", 3)]); } catch (e) { console.log(e.message); }\n',
       'hint': 'Курсор (строка, колонка) и множество занятых ячеек; при dense — всегда от начала.',
       'expected': ['2 a@0,0 b@0,1 c@0,2 d@1,0',
                    '3 a@0,0 b@1,0 c@1,2 d@2,0',
                    '2 a@0,0 b@1,0 c@0,2 d@1,2',
                    '2 a@0,0 b@0,1 c@0,2 d@1,1 e@1,2',
                    '4 a@0,0 b@1,0 c@1,1 d@2,1',
                    '0',
                    'Элемент шире сетки']},
      {'id': 'j15-grid-areas',
       'mode': 'js',
       'title': 'grid-template-areas',
       'statement': 'Напишите функцию parseAreas(template): template — строки вида «"head head" "nav main" '
                    '"foot foot"» (каждая в кавычках, слова через пробел; «.» — пустая ячейка); возвращает '
                    'объект «имя → { rowStart, rowEnd, colStart, colEnd }» (с 1, конец не включается); '
                    'область должна быть прямоугольной и сплошной, иначе Error("Область <имя> не '
                    'прямоугольная"); строки одинаковой длины, иначе Error("Разная ширина строк").',
       'starter': 'function parseAreas(template) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (o) => JSON.stringify(Object.fromEntries(Object.entries(o).map(([k, v]) => '
                 '[k, `${v.rowStart}/${v.colStart}-${v.rowEnd}/${v.colEnd}`])));\n'
                 'console.log(canon(parseAreas(`"head head" "nav main" "foot foot"`)));\n'
                 "console.log(canon(parseAreas(`'a a b' 'a a c' '. d d'`)));\n"
                 'console.log(canon(parseAreas(`"x"`)), canon(parseAreas("")));\n'
                 'for (const t of [`"a b" "b a"`, `"a a" "a ."`, `"a b" "c"`]) { try { parseAreas(t); '
                 'console.log("принято?", t); } catch (e) { console.log(e.message); } }\n',
       'hint': 'Для каждого имени найдите габариты (мин/макс строки и колонки) и сравните площадь с числом '
               'ячеек.',
       'expected': ['{"head":"1/1-2/3","nav":"2/1-3/2","main":"2/2-3/3","foot":"3/1-4/3"}',
                    '{"a":"1/1-3/3","b":"1/3-2/4","c":"2/3-3/4","d":"3/2-4/4"}',
                    '{"x":"1/1-2/2"} {}',
                    'Область a не прямоугольная',
                    'Область a не прямоугольная',
                    'Разная ширина строк']},
      {'id': 'j15-stacking',
       'mode': 'js',
       'title': 'Контексты наложения и z-index',
       'statement': 'Дерево элементов { id, z?, position?, opacity?, transform?, children }: элемент создаёт '
                    'контекст наложения, если у него position ≠ static и задан z (число или 0), либо opacity '
                    '< 1, либо transform. Напишите функцию paintOrder(root) → массив id в порядке отрисовки '
                    'снизу вверх: внутри контекста: сначала сам контекст (фон), затем потомки без '
                    'собственных контекстов в порядке документа (не позиционированные), затем контексты '
                    'потомков с z < 0 по возрастанию, потом позиционированные без z (z-index auto, считаются '
                    '0 и по порядку документа вместе с z = 0 контекстами), затем контексты с z > 0 по '
                    'возрастанию; при равенстве z — порядок документа. Позиционированные потомки без своего '
                    'контекста участвуют как z = 0 «слой» родительского контекста; их потомки сохраняют '
                    'порядок. Для простоты: потомки не создающие контекст, но позиционированные (position ≠ '
                    'static, z не задан) — painted в слое z=0 как обычные элементы вместе со своим '
                    'поддеревом без контекстов.',
       'starter': 'function paintOrder(root) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const E = (id, props = {}, ...children) => ({ id, ...props, children });\n'
                 'console.log(paintOrder(E("root", {}, E("a"), E("b", { position: "relative", z: 2 }), '
                 'E("c", { position: "absolute", z: -1 }), E("d", { position: "relative" }), E("e", { '
                 'position: "relative", z: 1 }, E("e1"), E("e2", { position: "absolute", z: 5 })), '
                 'E("f"))).join(" "));\n'
                 'console.log(paintOrder(E("root", {}, E("a", { opacity: 0.5 }, E("a1", { position: '
                 '"relative", z: 9999 })), E("b", { position: "relative", z: 1 }))).join(" "));\n'
                 'console.log(paintOrder(E("root")).join(" "), paintOrder(E("r", {}, E("x", { transform: '
                 '"scale(1)" }, E("y")), E("z"))).join(" "));\n'
                 'console.log(paintOrder(E("root", {}, E("p", { position: "relative", z: 0 }, E("q")), '
                 'E("n", { position: "relative" }, E("m")), E("w"))).join(" "));\n',
       'hint': 'Рекурсивный рендер контекста: поток, отрицательные, нулевые (в порядке документа), '
               'положительные.',
       'expected': ['root a f c d e e1 e2 b', 'root a a1 b', 'root r z x y', 'root w p q n m']},
      {'id': 'j15-media-query',
       'mode': 'js',
       'title': 'Вычисление медиа-запросов',
       'statement': 'Напишите функцию matchMedia(query, env): env = { width, height, orientation?, '
                    'prefersDark?, prefersReducedMotion? }; query — строка: список через запятую (ИЛИ); '
                    'каждый элемент — условия через and: (min-width: 600px), (max-width: 599px), '
                    '(min-height: …), (orientation: portrait|landscape) (если orientation не задан в env, он '
                    'вычисляется из width/height: portrait при height ≥ width), (prefers-color-scheme: '
                    'dark|light), (prefers-reduced-motion: reduce|no-preference), диапазоны (width >= '
                    '600px), (400px <= width <= 800px); префиксы not и only; типы screen/print/all (print — '
                    'всегда false). not инвертирует весь элемент. Единицы — px и em (1em = 16px).',
       'starter': 'function matchMedia(query, env) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const env = { width: 800, height: 600 };\n'
                 'const q = (s, e = env) => console.log(JSON.stringify(s), matchMedia(s, e));\n'
                 'q("(min-width: 600px)"); q("(min-width: 900px)"); q("(max-width: 799px)"); q("screen and '
                 '(min-width: 600px) and (max-width: 1000px)");\n'
                 'q("(orientation: landscape)"); q("(orientation: portrait)"); q("(orientation: portrait)", '
                 '{ width: 400, height: 800 });\n'
                 'q("(prefers-color-scheme: dark)", { ...env, prefersDark: true }); '
                 'q("(prefers-color-scheme: dark)"); q("(prefers-reduced-motion: reduce)", { ...env, '
                 'prefersReducedMotion: true });\n'
                 'q("(min-width: 900px), (max-width: 700px)"); q("(min-width: 900px), (min-width: 700px)");\n'
                 'q("(width >= 600px)"); q("(400px <= width <= 700px)"); q("(400px <= width < 800px)"); '
                 'q("(min-width: 50em)"); q("(min-width: 40em)");\n'
                 'q("not (min-width: 900px)"); q("not screen and (min-width: 600px)"); q("only screen and '
                 '(min-height: 500px)"); q("print"); q("not print");\n',
       'hint': 'Разберите запрос на альтернативы, затем на условия через and; каждое условие — по '
               'регулярному выражению.',
       'expected': ['"(min-width: 600px)" true',
                    '"(min-width: 900px)" false',
                    '"(max-width: 799px)" false',
                    '"screen and (min-width: 600px) and (max-width: 1000px)" true',
                    '"(orientation: landscape)" true',
                    '"(orientation: portrait)" false',
                    '"(orientation: portrait)" true',
                    '"(prefers-color-scheme: dark)" true',
                    '"(prefers-color-scheme: dark)" false',
                    '"(prefers-reduced-motion: reduce)" true',
                    '"(min-width: 900px), (max-width: 700px)" false',
                    '"(min-width: 900px), (min-width: 700px)" true',
                    '"(width >= 600px)" true',
                    '"(400px <= width <= 700px)" false',
                    '"(400px <= width < 800px)" false',
                    '"(min-width: 50em)" true',
                    '"(min-width: 40em)" true',
                    '"not (min-width: 900px)" true',
                    '"not screen and (min-width: 600px)" false',
                    '"only screen and (min-height: 500px)" true',
                    '"print" false',
                    '"not print" true']},
      {'id': 'j15-custom-props',
       'mode': 'js',
       'title': 'Разрешение var()',
       'statement': 'Напишите функцию resolveVars(props, name): props — объект пользовательских свойств '
                    '«--имя → строка значения», значения могут содержать var(--другое) и var(--другое, '
                    'запасное) (запасное может содержать вложенные var). Возвращает значение свойства name с '
                    'подставленными var; если переменной нет и запасного нет — значение «недопустимо во '
                    'время вычисления»: верните null; цикл (--a зависит от --b, а --b от --a) делает все '
                    'участвующие свойства недопустимыми (null). Значения без var возвращаются как есть '
                    '(пробелы по краям обрезаются).',
       'starter': 'function resolveVars(props, name) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const props = { "--base": "16px", "--gap": "calc(var(--base) * 2)", "--color": " #36c ", '
                 '"--missing-user": "var(--nope)", "--with-fb": "var(--nope, 8px)", "--nested-fb": '
                 '"var(--nope, var(--base, 1px))", "--a": "var(--b)", "--b": "var(--a)", "--self": '
                 '"var(--self)", "--text": "1px solid var(--color)", "--twice": "var(--base) var(--base)", '
                 '"--deep": "var(--gap)", "--fb-calc": "var(--zz, calc(1px + var(--base)))" };\n'
                 'for (const n of Object.keys(props).concat(["--unknown"])) console.log(n, "=", '
                 'JSON.stringify(resolveVars(props, n)));\n',
       'hint': 'Рекурсивная подстановка со стеком для обнаружения циклов; запасное значение — после первой '
               'запятой верхнего уровня.',
       'expected': ['--base = "16px"',
                    '--gap = "calc(16px * 2)"',
                    '--color = "#36c"',
                    '--missing-user = null',
                    '--with-fb = "8px"',
                    '--nested-fb = "16px"',
                    '--a = null',
                    '--b = null',
                    '--self = null',
                    '--text = "1px solid #36c"',
                    '--twice = "16px 16px"',
                    '--deep = "calc(16px * 2)"',
                    '--fb-calc = "calc(1px + 16px)"',
                    '--unknown = undefined']},
      {'id': 'j15-css-nesting',
       'mode': 'js',
       'title': 'Вложенные правила CSS',
       'statement': 'Напишите функцию flattenNesting(css): вход — CSS с нативной вложенностью: в блоке '
                    'правила могут быть вложенные правила (селекторы с & — заменяется на родителя; без & — '
                    'потомок: «.a { .b { … } }» → «.a .b»; «&:hover», «& + &», «.x &» и т. д.) и @media '
                    'внутри правила (оборачивает: «@media (…) { .a { … } }»). Список селекторов через '
                    'запятую раскрывается декартово. Выход — плоский CSS, каждое правило в виде «селектор { '
                    'объявления }» на отдельной строке (объявления через пробел, у правила без объявлений — '
                    'пропускается).',
       'starter': 'function flattenNesting(css) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(flattenNesting(".card { color: red; .title { font-size: 20px; } &:hover { '
                 'color: blue; } & + & { margin-top: 1rem; } .dark & { color: white; } }"));\n'
                 'console.log("---");\n'
                 'console.log(flattenNesting(".a, .b { x: 1; .c, .d { y: 2; } }"));\n'
                 'console.log("---");\n'
                 'console.log(flattenNesting(".nav { display: block; @media (min-width: 600px) { display: '
                 'flex; .item { gap: 1px; } } }"));\n'
                 'console.log("---");\n'
                 'console.log(flattenNesting(""), "|", flattenNesting("p { }"), "|", flattenNesting("p { a { '
                 'b { c: d; } } }"));\n',
       'hint': 'Рекурсивный разбор блоков: накапливайте родительские селекторы и, при необходимости, '
               'медиа-условие.',
       'expected': ['.card { color: red; }',
                    '.card .title { font-size: 20px; }',
                    '.card:hover { color: blue; }',
                    '.card + .card { margin-top: 1rem; }',
                    '.dark .card { color: white; }',
                    '---',
                    '.a, .b { x: 1; }',
                    '.a .c, .a .d, .b .c, .b .d { y: 2; }',
                    '---',
                    '.nav { display: block; }',
                    '@media (min-width: 600px) { .nav { display: flex; } }',
                    '@media (min-width: 600px) { .nav .item { gap: 1px; } }',
                    '---',
                    ' |  | p a b { c: d; }']},
      {'id': 'j15-easing',
       'mode': 'js',
       'title': 'Функции плавности',
       'statement': 'Напишите функции cubicBezier(x1, y1, x2, y2) → функция t ↦ y (прогресс времени t в [0, '
                    '1] → значение): решайте уравнение по x численно (метод Ньютона или бисекция, точность '
                    '1e-6), и steps(n, jumpEnd = true) → функция ступеней. Готовые константы: ease = '
                    'cubicBezier(0.25, 0.1, 0.25, 1), easeIn = (0.42, 0, 1, 1), easeOut = (0, 0, 0.58, 1), '
                    'easeInOut = (0.42, 0, 0.58, 1), linear = t => t. Все функции возвращают 0 при t ≤ 0 и 1 '
                    'при t ≥ 1.',
       'starter': 'function cubicBezier(x1, y1, x2, y2) {\n}\nfunction steps(n, jumpEnd) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const ease = cubicBezier(0.25, 0.1, 0.25, 1), easeIn = cubicBezier(0.42, 0, 1, 1), easeOut '
                 '= cubicBezier(0, 0, 0.58, 1), easeInOut = cubicBezier(0.42, 0, 0.58, 1), linear = '
                 'cubicBezier(0, 0, 1, 1);\n'
                 'const r = (f) => [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1].map((t) => f(t).toFixed(3)).join(" ");\n'
                 'console.log("ease     ", r(ease)); console.log("easeIn   ", r(easeIn)); '
                 'console.log("easeOut  ", r(easeOut)); console.log("easeInOut", r(easeInOut)); '
                 'console.log("linear   ", r(linear));\n'
                 'console.log(ease(-1), ease(2), steps(4)(0), steps(4)(0.24), steps(4)(0.25), '
                 'steps(4)(0.99), steps(4)(1), steps(4, false)(0.01), steps(4, false)(0.26), '
                 'steps(1)(0.5));\n'
                 'const s = steps(3); console.log([0, 0.2, 0.34, 0.67, 0.99].map((t) => '
                 's(t).toFixed(2)).join(" "));\n',
       'hint': 'Для t(x) используйте бисекцию по x на кривой Безье; затем вычислите y по тому же параметру.',
       'expected': ['ease      0.000 0.095 0.409 0.802 0.960 0.994 1.000',
                    'easeIn    0.000 0.017 0.093 0.315 0.622 0.839 1.000',
                    'easeOut   0.000 0.161 0.378 0.685 0.907 0.983 1.000',
                    'easeInOut 0.000 0.020 0.129 0.500 0.871 0.980 1.000',
                    'linear    0.000 0.100 0.250 0.500 0.750 0.900 1.000',
                    '0 1 0 0 0.25 0.75 1 0.25 0.5 0',
                    '0.00 0.00 0.33 0.67 0.67']},
      {'id': 'j15-keyframes',
       'mode': 'js',
       'title': 'Интерполяция кейфреймов',
       'statement': 'Напишите функцию sample(keyframes, progress, easing = linear): keyframes — массив { '
                    'offset (0–1), value } (отсортирован); value — число, строка с числом и единицей '
                    '(«10px», «50%») или цвет «#rrggbb»; progress в [0, 1] (вне диапазона обрезается). Между '
                    'соседними кадрами значение интерполируется линейно с функцией плавности easing '
                    '(применяется к локальному прогрессу сегмента). Числа с единицами интерполируются по '
                    'числу (единицы должны совпадать, иначе Error), цвета — по каналам (результат «#rrggbb», '
                    'каналы округляются). Верните значение того же вида (строку или число).',
       'starter': 'function sample(keyframes, progress, easing) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const kf = [{ offset: 0, value: "0px" }, { offset: 0.5, value: "100px" }, { offset: 1, '
                 'value: "40px" }];\n'
                 'console.log([0, 0.1, 0.25, 0.5, 0.75, 1, -1, 2].map((p) => sample(kf, p)).join(" "));\n'
                 'console.log(sample([{ offset: 0, value: 0 }, { offset: 1, value: 10 }], 0.3), sample([{ '
                 'offset: 0, value: "100%" }, { offset: 1, value: "0%" }], 0.25));\n'
                 'const col = [{ offset: 0, value: "#ff0000" }, { offset: 1, value: "#0000ff" }];\n'
                 'console.log(sample(col, 0), sample(col, 0.5), sample(col, 1), sample(col, 0.25));\n'
                 'const quad = (t) => t * t;\n'
                 'console.log(sample([{ offset: 0, value: "0px" }, { offset: 1, value: "100px" }], 0.5, '
                 'quad), sample(kf, 0.25, quad));\n'
                 'try { sample([{ offset: 0, value: "1px" }, { offset: 1, value: "1em" }], 0.5); } catch (e) '
                 '{ console.log(e.message); }\n'
                 'console.log(sample([{ offset: 0.2, value: 5 }, { offset: 0.8, value: 15 }], 0), sample([{ '
                 'offset: 0.2, value: 5 }, { offset: 0.8, value: 15 }], 0.5));\n',
       'hint': 'Найдите сегмент между соседними кадрами; локальный прогресс пропустите через easing.',
       'expected': ['0px 20px 50px 100px 70px 40px 0px 40px',
                    '3 75%',
                    '#ff0000 #800080 #0000ff #bf0040',
                    '25px 25px',
                    'Разные единицы',
                    '5 10']},
      {'id': 'j15-animation-state',
       'mode': 'js',
       'title': 'Состояние анимации во времени',
       'statement': 'Напишите функцию animationProgress(t, { delay = 0, duration, iterations = 1 (может быть '
                    'Infinity), direction = "normal"|"reverse"|"alternate"|"alternate-reverse", fillMode = '
                    '"none"|"forwards"|"backwards"|"both" }): t — время с начала (мс); возвращает { phase: '
                    '"before"|"active"|"after", progress: число 0–1 или null }: до начала (t < delay) — '
                    'progress = для backwards/both значение начала первого цикла (0, либо 1 при reverse), '
                    'иначе null; после конца (t ≥ delay + duration*iterations) — для forwards/both значение '
                    'конца последнего цикла, иначе null; внутри — прогресс текущей итерации с учётом '
                    'направления (alternate: чётные итерации вперёд, нечётные назад, считая с 0).',
       'starter': 'function animationProgress(t, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const a = (t, o) => console.log(t, JSON.stringify(animationProgress(t, o)));\n'
                 'const o = { duration: 1000, delay: 500 };\n'
                 'a(0, o); a(500, o); a(1000, o); a(1500, o); a(2000, o);\n'
                 'a(0, { ...o, fillMode: "backwards" }); a(2000, { ...o, fillMode: "forwards" }); a(0, { '
                 '...o, fillMode: "both", direction: "reverse" }); a(2000, { ...o, fillMode: "both", '
                 'direction: "reverse" });\n'
                 'const alt = { duration: 100, iterations: 3, direction: "alternate", fillMode: "forwards" '
                 '};\n'
                 '[0, 50, 100, 150, 250, 299, 300, 999].forEach((t) => a(t, alt));\n'
                 'a(1234, { duration: 100, iterations: Infinity }); a(150, { duration: 100, iterations: 2.5, '
                 'fillMode: "forwards" }); a(300, { duration: 100, iterations: 2.5, fillMode: "forwards" '
                 '});\n',
       'hint': 'Номер итерации = floor((t − delay)/duration); направление зависит от номера и режима.',
       'expected': ['0 {"phase":"before","progress":null}',
                    '500 {"phase":"active","progress":0}',
                    '1000 {"phase":"active","progress":0.5}',
                    '1500 {"phase":"after","progress":null}',
                    '2000 {"phase":"after","progress":null}',
                    '0 {"phase":"before","progress":0}',
                    '2000 {"phase":"after","progress":1}',
                    '0 {"phase":"before","progress":1}',
                    '2000 {"phase":"after","progress":0}',
                    '0 {"phase":"active","progress":0}',
                    '50 {"phase":"active","progress":0.5}',
                    '100 {"phase":"active","progress":1}',
                    '150 {"phase":"active","progress":0.5}',
                    '250 {"phase":"active","progress":0.5}',
                    '299 {"phase":"active","progress":0.99}',
                    '300 {"phase":"after","progress":1}',
                    '999 {"phase":"after","progress":1}',
                    '1234 {"phase":"active","progress":0.34}',
                    '150 {"phase":"active","progress":0.5}',
                    '300 {"phase":"after","progress":0.5}']},
      {'id': 'j15-bem',
       'mode': 'js',
       'title': 'БЭМ: проверка и генерация имён',
       'statement': 'Напишите функцию parseBem(className) → { block, element?, modifier?, value? } для имён '
                    'вида block, block__element, block--mod, block--mod_value (в БЭМ-Реакт) или '
                    'block__element--mod; допускаются строчные буквы, цифры и одиночные дефисы внутри '
                    'частей; нарушения (заглавные, лишние подчёркивания, пустые части, элемент элемента '
                    '«a__b__c») — null. Функцию bem(block, element, modifiers) → строка классов: '
                    '«block__element block__element--mod …» (modifiers — объект: true даёт --имя, строка '
                    'даёт --имя_значение (две части через подчёркивание), false/null/undefined '
                    'пропускается). И lintBem(classes): имена с нарушениями.',
       'starter': 'function parseBem(className) {\n'
                  '}\n'
                  'function bem(block, element, modifiers) {\n'
                  '}\n'
                  'function lintBem(classes) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (o) => JSON.stringify(o && Object.fromEntries(Object.entries(o).sort()));\n'
                 'for (const n of ["menu", "menu__item", "menu--open", "menu__item--active", '
                 '"menu--theme_dark", "main-menu__sub-item--is-active", "Menu", "menu__", "menu___item", '
                 '"a__b__c", "menu--", "menu-", "-menu", "menu__item_x", "menu--a--b", "1col"]) '
                 'console.log(JSON.stringify(n), canon(parseBem(n)));\n'
                 'console.log(bem("btn"), "|", bem("btn", null, { primary: true, size: "large", disabled: '
                 'false, x: null }), "|", bem("card", "title", { big: true }), "|", bem("card", "body", '
                 '{}));\n'
                 'console.log(JSON.stringify(lintBem(["ok", "Bad", "ok__el", "a__b__c", "x--y"])), '
                 'JSON.stringify(lintBem([])));\n',
       'hint': 'Одно регулярное выражение с необязательными группами для элемента, модификатора и значения.',
       'expected': ['"menu" {"block":"menu"}',
                    '"menu__item" {"block":"menu","element":"item"}',
                    '"menu--open" {"block":"menu","modifier":"open"}',
                    '"menu__item--active" {"block":"menu","element":"item","modifier":"active"}',
                    '"menu--theme_dark" {"block":"menu","modifier":"theme","value":"dark"}',
                    '"main-menu__sub-item--is-active" '
                    '{"block":"main-menu","element":"sub-item","modifier":"is-active"}',
                    '"Menu" null',
                    '"menu__" null',
                    '"menu___item" null',
                    '"a__b__c" null',
                    '"menu--" null',
                    '"menu-" null',
                    '"-menu" null',
                    '"menu__item_x" null',
                    '"menu--a--b" null',
                    '"1col" {"block":"1col"}',
                    'btn | btn btn--primary btn--size_large | card__title card__title--big | card__body',
                    '["Bad","a__b__c"] []']},
      {'id': 'j15-unused-css',
       'mode': 'js',
       'title': 'Поиск неиспользуемых селекторов',
       'statement': 'Напишите функцию unusedSelectors(css, usedClasses, usedIds, usedTags): css — «плоский» '
                    'CSS из правил «селектор { … }» (без вложенности и @-правил); возвращает массив '
                    'селекторов (из списков через запятую, по отдельности, без повторов, в порядке '
                    'появления), которые не могут сработать: если в селекторе есть класс не из usedClasses, '
                    'идентификатор не из usedIds или тег не из usedTags (теги из набора html/body всегда '
                    'допустимы; * и псевдоклассы/псевдоэлементы/атрибуты игнорируются).',
       'starter': 'function unusedSelectors(css, usedClasses, usedIds, usedTags) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const css = `.btn { a: 1 } .btn:hover, .btn.big { a: 1 } #main .list > li { b: 2 } '
                 '.old-banner { c: 3 } ul.menu li a[href] { d: 4 } p::first-line { e: 5 } table td { f: 6 } '
                 '.btn, .gone { g: 7 } * { h: 8 } body { i: 9 } #nope { j: 10 }`;\n'
                 'console.log(JSON.stringify(unusedSelectors(css, ["btn", "list", "menu"], ["main"], ["ul", '
                 '"li", "a", "p"])));\n'
                 'console.log(JSON.stringify(unusedSelectors(css, ["btn", "big", "list", "menu", '
                 '"old-banner", "gone"], ["main", "nope"], ["ul", "li", "a", "p", "table", "td"])), '
                 'JSON.stringify(unusedSelectors("", [], [], [])));\n',
       'hint': 'Выделите из селектора классы, идентификаторы и теги и сравните с наборами используемых.',
       'expected': ['[".btn.big",".old-banner","table td",".gone","#nope"]', '[] []']},
      {'id': 'j15-design-tokens',
       'mode': 'js',
       'title': 'Дизайн-токены и темы',
       'statement': 'Токены заданы вложенным объектом: { color: { brand: { $value: "#36c" }, text: { $value: '
                    '"{color.brand}" } }, space: { 1: { $value: "4px" } } }; значение вида «{путь.к.токену}» '
                    '— ссылка (может быть вложенной в строку: «1px solid {color.brand}», цепочки ссылок '
                    'допустимы); циклы — Error("Цикл токенов: …"); ссылка на отсутствующий токен — '
                    'Error("Нет токена: …"). Напишите функцию buildCss(tokens, selector = ":root", prefix = '
                    '""): возвращает текст «selector {\\n  --color-brand: #36c;\\n  …\\n}» — переменные в '
                    'порядке обхода объекта, имя — путь через дефис (с prefix, если задан: '
                    '«--ds-color-brand»), все ссылки разрешены. И функцию themes(base, overrides) → CSS: '
                    'базовые переменные в :root, затем для каждой темы из overrides (имя → объект токенов) '
                    'блок «[data-theme="имя"] { … }» только с переопределёнными переменными.',
       'starter': 'function buildCss(tokens, selector, prefix) {\n}\nfunction themes(base, overrides) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tokens = { color: { brand: { $value: "#36c" }, text: { $value: "{color.brand}" }, '
                 'border: { $value: "1px solid {color.brand}" } }, space: { 1: { $value: "4px" }, 2: { '
                 '$value: "8px" } } };\n'
                 'console.log(buildCss(tokens));\n'
                 'console.log(buildCss(tokens, ".theme", "ds"));\n'
                 'console.log(themes(tokens, { dark: { color: { brand: { $value: "#8af" } } }, same: { '
                 'space: { 1: { $value: "4px" } } } }));\n'
                 'for (const bad of [{ a: { $value: "{b}" }, b: { $value: "{a}" } }, { a: { $value: "{zzz}" '
                 '} }]) { try { buildCss(bad); } catch (e) { console.log(e.message); } }\n'
                 'console.log(JSON.stringify(buildCss({})));\n',
       'hint': 'Сначала «расплющьте» токены в пары путь→значение, затем разрешайте ссылки рекурсивно с '
               'мемоизацией и стеком.',
       'expected': [':root {',
                    '  --color-brand: #36c;',
                    '  --color-text: #36c;',
                    '  --color-border: 1px solid #36c;',
                    '  --space-1: 4px;',
                    '  --space-2: 8px;',
                    '}',
                    '.theme {',
                    '  --ds-color-brand: #36c;',
                    '  --ds-color-text: #36c;',
                    '  --ds-color-border: 1px solid #36c;',
                    '  --ds-space-1: 4px;',
                    '  --ds-space-2: 8px;',
                    '}',
                    ':root {',
                    '  --color-brand: #36c;',
                    '  --color-text: #36c;',
                    '  --color-border: 1px solid #36c;',
                    '  --space-1: 4px;',
                    '  --space-2: 8px;',
                    '}',
                    '[data-theme="dark"] {',
                    '  --color-brand: #8af;',
                    '  --color-text: #8af;',
                    '  --color-border: 1px solid #8af;',
                    '}',
                    'Цикл токенов: a → b → a',
                    'Нет токена: zzz',
                    '":root {\\n\\n}"']},
      {'id': 'j15-remify',
       'mode': 'js',
       'title': 'px → rem в таблице стилей',
       'statement': 'Напишите функцию remify(css, { base = 16, props = [...] , skip = ["border"] }): '
                    'заменяет значения в px на rem (значение / base, до 4 знаков без хвостовых нулей; «0px» '
                    '→ «0»; «1px» оставляется как есть) только в объявлениях свойств из props (по умолчанию: '
                    'font-size, margin*, padding*, width, height, gap, top, left, right, bottom, '
                    'line-height, max-width, min-width) и не трогает свойства из skip (border*, box-shadow); '
                    'внутри функций вроде calc() и в нескольких значениях (margin: 8px 16px) заменяются все '
                    'числа с px. Остальной текст сохраняется как есть.',
       'starter': 'function remify(css, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const css = ".a { font-size: 14px; margin: 8px 16px 0px 1px; border: 2px solid red; '
                 'border-radius: 4px; width: calc(100% - 32px); color: #333; padding-left: 24px; z-index: 5; '
                 'box-shadow: 0 0 10px #000; line-height: 20px }";\n'
                 'console.log(remify(css));\n'
                 'console.log(remify("p{font-size:10px}", { base: 10 }));\n'
                 'console.log(remify(".x { margin: -12px; top: .5px; left: 0px; height: 100px }"));\n'
                 'console.log(remify(css, { props: ["border"], skip: [] }).slice(0, 80));\n'
                 'console.log(JSON.stringify(remify("")));\n',
       'hint': 'Регулярное выражение на «свойство: значение»; внутри значения — замена всех чисел с px.',
       'expected': ['.a { font-size: 0.875rem; margin: 0.5rem 1rem 0 1px; border: 2px solid red; '
                    'border-radius: 4px; width: calc(100% - 2rem); color: #333; padding-left: 1.5rem; '
                    'z-index: 5; box-shadow: 0 0 10px #000; line-height: 1.25rem }',
                    'p{font-size:1rem}',
                    '.x { margin: -0.75rem; top: 0.0313rem; left: 0; height: 6.25rem }',
                    '.a { font-size: 14px; margin: 8px 16px 0px 1px; border: 0.125rem solid red; bord',
                    '""']},
      {'id': 'j15-absolute',
       'mode': 'js',
       'title': 'Абсолютное позиционирование',
       'statement': 'Контейнирующий блок: { width, height }. Абсолютный элемент: { top?, right?, bottom?, '
                    'left?, width?, height? } (числа в px; недостающие — undefined). Напишите функцию '
                    'absoluteRect(cb, el) → { x, y, w, h } относительно левого верхнего угла контейнера: '
                    'если заданы left и right при неопределённой width — ширина растягивается: w = cb.width '
                    '- left - right; если width задана и заданы оба left и right — используется left (right '
                    'игнорируется); если только right — x = cb.width - right - w; аналогично по вертикали с '
                    'top/bottom; если не заданы ни left, ни right — x = 0 (статическая позиция упрощена до '
                    '0), ни top, ни bottom — y = 0. Если не определена ширина и нет пары left+right — ширина '
                    '0 (содержимое пусто).',
       'starter': 'function absoluteRect(cb, el) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const cb = { width: 400, height: 300 };\n'
                 'const show = (el) => console.log(JSON.stringify(absoluteRect(cb, el)));\n'
                 'show({ top: 10, left: 20, width: 100, height: 50 });\n'
                 'show({ bottom: 10, right: 20, width: 100, height: 50 });\n'
                 'show({ top: 10, bottom: 10, left: 5, right: 5 });\n'
                 'show({ top: 10, left: 20, right: 30, width: 100, height: 40 });\n'
                 'show({ width: 80, height: 60 });\n'
                 'show({ right: 0, bottom: 0, width: 10, height: 10 });\n'
                 'show({ left: 300, right: 300 });\n'
                 'show({});\n',
       'hint': 'Для каждой оси: пара start+end растягивает, иначе позиция от start или от end.',
       'expected': ['{"x":20,"y":10,"w":100,"h":50}',
                    '{"x":280,"y":240,"w":100,"h":50}',
                    '{"x":5,"y":10,"w":390,"h":280}',
                    '{"x":20,"y":10,"w":100,"h":40}',
                    '{"x":0,"y":0,"w":80,"h":60}',
                    '{"x":390,"y":290,"w":10,"h":10}',
                    '{"x":300,"y":0,"w":0,"h":0}',
                    '{"x":0,"y":0,"w":0,"h":0}']},
      {'id': 'j15-sticky',
       'mode': 'js',
       'title': 'position: sticky',
       'statement': 'Липкий элемент высотой h находится в родителе, занимающем по вертикали [parentTop, '
                    'parentBottom] в координатах страницы (parentBottom - parentTop ≥ h); естественная '
                    'позиция элемента — naturalTop (координата верхнего края без прилипания), порог top = '
                    'offset (расстояние от верхнего края окна). Напишите функцию stickyTop(scrollY, { '
                    'naturalTop, h, parentTop, parentBottom, offset }) → координата верхнего края элемента '
                    'на странице при прокрутке scrollY: пока naturalTop ≥ scrollY + offset — остаётся на '
                    'месте; иначе прилипает к scrollY + offset, но не выходит за нижнюю границу родителя '
                    '(верхний край ≤ parentBottom - h) и не поднимается выше естественной позиции. И '
                    'viewportTop(...) → то же в координатах окна (stickyTop - scrollY).',
       'starter': 'function stickyTop(scrollY, geom) {\n}\nfunction viewportTop(scrollY, geom) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const g = { naturalTop: 200, h: 50, parentTop: 100, parentBottom: 600, offset: 10 };\n'
                 'for (const y of [0, 100, 190, 191, 250, 500, 540, 541, 1000]) console.log(y, stickyTop(y, '
                 'g), viewportTop(y, g));\n'
                 'console.log(stickyTop(0, { ...g, offset: 0 }), stickyTop(300, { ...g, parentBottom: 260 '
                 '}), stickyTop(300, { naturalTop: 0, h: 20, parentTop: 0, parentBottom: 20, offset: 0 '
                 '}));\n',
       'hint': 'Позиция = max(естественная, scrollY + offset), но не ниже parentBottom − h.',
       'expected': ['0 200 200',
                    '100 200 100',
                    '190 200 10',
                    '191 201 10',
                    '250 260 10',
                    '500 510 10',
                    '540 550 10',
                    '541 550 9',
                    '1000 550 -450',
                    '200 210 0']},
      {'id': 'j15-fluid-type',
       'mode': 'js',
       'title': 'Плавная типографика через clamp',
       'statement': 'Напишите функцию fluidSize({ minSize, maxSize, minVw, maxVw }) (размеры в px, ширины '
                    'окна в px): возвращает строку CSS clamp(minRem, intercept + slope vw, maxRem): slope = '
                    '100 * (maxSize - minSize) / (maxVw - minVw) — в vw (до 4 знаков без хвостовых нулей), '
                    'intercept = minSize - slope * minVw / 100 — в px, переводится в rem (деление на 16, до '
                    '4 знаков); формат «clamp(1rem, 0.5rem + 1.25vw, 2rem)» (отрицательный intercept — «- '
                    '0.5rem»; ноль — только vw-часть). И функцию sizeAt(viewport, params) → фактический '
                    'размер в px при данной ширине окна (с ограничением), округление до 2 знаков.',
       'starter': 'function fluidSize(params) {\n}\nfunction sizeAt(viewport, params) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const p = { minSize: 16, maxSize: 32, minVw: 320, maxVw: 1280 };\n'
                 'console.log(fluidSize(p));\n'
                 'console.log(fluidSize({ minSize: 14, maxSize: 20, minVw: 400, maxVw: 1200 }));\n'
                 'console.log(fluidSize({ minSize: 16, maxSize: 16, minVw: 320, maxVw: 1280 }));\n'
                 'console.log(fluidSize({ minSize: 10, maxSize: 40, minVw: 0, maxVw: 1000 }));\n'
                 'console.log([200, 320, 800, 1280, 2000].map((v) => sizeAt(v, p)).join(" "));\n',
       'hint': 'slope — наклон в vw, intercept — смещение; результат склеивается в строку clamp().',
       'expected': ['clamp(1rem, 0.6667rem + 1.6667vw, 2rem)',
                    'clamp(0.875rem, 0.6875rem + 0.75vw, 1.25rem)',
                    'clamp(1rem, 1rem + 0vw, 1rem)',
                    'clamp(0.625rem, 0.625rem + 3vw, 2.5rem)',
                    '16 16 24 32 32']},
      {'id': 'j15-object-fit',
       'mode': 'js',
       'title': 'object-fit и aspect-ratio',
       'statement': 'Напишите функцию fit(mode, box, image) → { x, y, w, h } — прямоугольник изображения '
                    'внутри блока box = { w, h } для image = { w, h } (естественные размеры): fill — '
                    'растянуть на весь блок; contain — вписать целиком с сохранением пропорций и '
                    'центрировать; cover — заполнить блок с обрезкой, центрировать (x и y могут быть '
                    'отрицательными); none — естественный размер по центру; scale-down — меньшее из none и '
                    'contain. Размеры и позиции — округлены до 2 знаков. И функцию heightFromRatio(width, '
                    'ratio) (ratio — строка «16/9» или «1.5»), округление до 2 знаков.',
       'starter': 'function fit(mode, box, image) {\n}\nfunction heightFromRatio(width, ratio) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const box = { w: 200, h: 100 }, img = { w: 400, h: 400 }, small = { w: 50, h: 20 };\n'
                 'for (const m of ["fill", "contain", "cover", "none", "scale-down"]) '
                 'console.log(m.padEnd(10), JSON.stringify(fit(m, box, img)), JSON.stringify(fit(m, box, '
                 'small)));\n'
                 'console.log(JSON.stringify(fit("contain", { w: 100, h: 100 }, { w: 300, h: 100 })), '
                 'JSON.stringify(fit("cover", { w: 100, h: 100 }, { w: 300, h: 100 })));\n'
                 'console.log(heightFromRatio(320, "16/9"), heightFromRatio(300, "1.5"), '
                 'heightFromRatio(100, "1/1"), heightFromRatio(90, "3 / 2".replace(/\\s/g, "")));\n'
                 'try { fit("stretch", box, img); } catch (e) { console.log(e.message); }\n',
       'hint': 'Масштаб contain — min отношений сторон, cover — max; затем центрирование.',
       'expected': ['fill       {"x":0,"y":0,"w":200,"h":100} {"x":0,"y":0,"w":200,"h":100}',
                    'contain    {"x":50,"y":0,"w":100,"h":100} {"x":0,"y":10,"w":200,"h":80}',
                    'cover      {"x":0,"y":-50,"w":200,"h":200} {"x":-25,"y":0,"w":250,"h":100}',
                    'none       {"x":-100,"y":-150,"w":400,"h":400} {"x":75,"y":40,"w":50,"h":20}',
                    'scale-down {"x":50,"y":0,"w":100,"h":100} {"x":75,"y":40,"w":50,"h":20}',
                    '{"x":0,"y":33.33,"w":100,"h":33.33} {"x":-100,"y":0,"w":300,"h":100}',
                    '180 200 100 60',
                    'Неизвестный режим: stretch']}]}
