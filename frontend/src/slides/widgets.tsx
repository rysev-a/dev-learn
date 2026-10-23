/* Общие виджеты слайдов глав: карточка-узел, блок команды, стрелка и врезки кода
   Python и Rust с подсветкой (классы rs-*). Раньше эти компоненты копировались в каждый файл главы. */
import type { ReactNode } from "react";

export function Node({ mono, title, sub, kind }: { mono?: boolean; title: ReactNode; sub?: ReactNode; kind?: string }) {
  return (
    <div className={`s-node ${kind || ""}`}>
      <span className={mono ? "s-node-mono" : "s-node-title"}>{title}</span>
      {sub && <span className="s-node-sub">{sub}</span>}
    </div>
  );
}

export function Cmd({ children }: { children?: ReactNode }) {
  return (
    <div className="s-cmd">
      <pre>{children}</pre>
    </div>
  );
}

export const Arr = () => <span className="s-arr">→</span>;

const word = (list: string[]) => new Set(list);

// Ключевые слова Python по умолчанию; у глав, где подсвечивается другой набор, он передаётся в makePyCode.
export const PY_KW = word([
  "print", "for", "in", "not", "and", "or", "if", "else", "while", "is",
  "True", "False", "None", "def", "return",
]);

// Крошечный токенизатор Python: комментарии, строки, числа, ключевые слова, вызовы функций. Достаточно для слайдов.
export function pySpan(src: string, keywords: Set<string> = PY_KW, boolsAsNum = false): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(#[^\n]*)|((?:[fF])?"(?:[^"\\]|\\.)*"|(?:[fF])?'(?:[^'\\]|\\.)*')|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, num, w] = m;
    if (com) out.push(<span key={out.length} className="rs-com">{tok}</span>);
    else if (str) out.push(<span key={out.length} className="rs-str">{tok}</span>);
    else if (num) out.push(<span key={out.length} className="rs-num">{tok}</span>);
    else if (w) {
      let cls = "";
      if (keywords.has(w)) cls = "rs-kw";
      else if (boolsAsNum && (w === "True" || w === "False")) cls = "rs-num";
      else if (src[re.lastIndex] === "(") cls = "rs-fn";
      out.push(
        cls ? (
          <span key={out.length} className={cls}>{w}</span>
        ) : (
          <span key={out.length}>{w}</span>
        ),
      );
    } else out.push(<span key={out.length}>{tok}</span>);
  }
  return out;
}

/** Врезка кода Python со своим набором ключевых слов (boolsAsNum — True и False цветом чисел). */
export const makePyCode = (keywords: Iterable<string>, boolsAsNum = false) => {
  const kw = new Set(keywords);
  function PyCode({ children }: { children: string }) {
    return <pre className="rs-code">{pySpan(children, kw, boolsAsNum)}</pre>;
  }
  // набор ключевых слов нужен выгрузке слайдов в JSON (scripts/slides-export.mjs)
  return Object.assign(PyCode, { kw: [...kw], boolsAsNum });
};

/** Врезка кода Python с набором по умолчанию. */
export const PyCode = makePyCode(PY_KW);

const RS_KW = word([
  "fn", "let", "mut", "pub", "struct", "enum", "impl", "match", "if", "else",
  "for", "while", "loop", "return", "use", "mod", "crate", "self", "Self",
  "move", "ref", "const", "static", "type", "where", "async", "await",
  "unsafe", "trait", "dyn", "in", "as", "break", "continue",
]);
const RS_TY = word([
  "i8", "i16", "i32", "i64", "i128", "isize", "u8", "u16", "u32", "u64",
  "u128", "usize", "f32", "f64", "bool", "char", "str", "String", "Vec",
  "Option", "Result", "Box", "Rc", "Arc", "RefCell", "HashMap",
]);

// Крошечный токенизатор Rust: комментарии, строки, времена жизни, ключевые слова, типы, макросы, числа, вызовы функций.
export function rsSpan(src: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re =
    /(\/\/[^\n]*)|("(?:[^"\\]|\\.)*")|('(\w+)\b)|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*!)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, life, , num, mac, w] = m;
    if (com) out.push(<span key={out.length} className="rs-com">{tok}</span>);
    else if (str) out.push(<span key={out.length} className="rs-str">{tok}</span>);
    else if (life) out.push(<span key={out.length} className="rs-life">{tok}</span>);
    else if (num) out.push(<span key={out.length} className="rs-num">{tok}</span>);
    else if (mac) out.push(<span key={out.length} className="rs-mac">{tok}</span>);
    else if (w) {
      let cls = "";
      if (RS_KW.has(w)) cls = "rs-kw";
      else if (RS_TY.has(w)) cls = "rs-ty";
      else if (/^[A-Z]/.test(w)) cls = "rs-ty";
      else if (src[re.lastIndex] === "(") cls = "rs-fn";
      out.push(
        cls ? (
          <span key={out.length} className={cls}>{w}</span>
        ) : (
          <span key={out.length}>{w}</span>
        ),
      );
    } else out.push(<span key={out.length}>{tok}</span>);
  }
  return out;
}

/** Врезка кода Rust. */
export function RsCode({ children }: { children: string }) {
  return <pre className="rs-code">{rsSpan(children)}</pre>;
}
