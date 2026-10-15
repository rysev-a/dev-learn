import { useEffect, useRef } from "react";
import { Annotation, EditorState } from "@codemirror/state";
import {
  EditorView,
  drawSelection,
  highlightActiveLine,
  keymap,
  lineNumbers,
} from "@codemirror/view";
import {
  defaultKeymap,
  history,
  historyKeymap,
  indentWithTab,
} from "@codemirror/commands";
import {
  HighlightStyle,
  bracketMatching,
  indentOnInput,
  indentUnit,
  syntaxHighlighting,
} from "@codemirror/language";
import { python } from "@codemirror/lang-python";
import { rust } from "@codemirror/lang-rust";
import { SQLite, sql } from "@codemirror/lang-sql";
import { tags as t } from "@lezer/highlight";

/* Редактор кода на CodeMirror 6 с подсветкой Python, SQL или Rust (prop lang). Цвета берутся из тех же
   CSS-переменных, что и подсветка на слайдах (--s-*), поэтому обе темы
   работают без отдельных настроек. Редактор неуправляемый: значение из
   props подмешивается в документ только когда оно изменилось снаружи
   (например, «Сбросить»). */

const external = Annotation.define();

const highlight = HighlightStyle.define([
  { tag: [t.keyword, t.controlKeyword, t.operatorKeyword, t.definitionKeyword, t.moduleKeyword, t.self], color: "var(--s-accent)" },
  { tag: [t.string, t.special(t.string)], color: "var(--s-blue)" },
  { tag: [t.number, t.bool, t.null], color: "var(--s-violet)" },
  { tag: t.comment, color: "var(--s-muted)", fontStyle: "italic" },
  { tag: [t.function(t.variableName), t.function(t.propertyName)], color: "var(--s-text)", fontWeight: "500" },
  { tag: [t.definition(t.variableName), t.className], color: "var(--s-amber)" },
  { tag: t.operator, color: "var(--s-muted)" },
]);

const theme = EditorView.theme({
  "&": {
    backgroundColor: "var(--s-bg)",
    color: "var(--s-text)",
    fontSize: "12.5px",
  },
  "&.cm-focused": { outline: "none" },
  ".cm-scroller": {
    fontFamily: '"SF Mono", "JetBrains Mono", Menlo, Consolas, monospace',
    lineHeight: "1.55",
    overflow: "auto",
  },
  ".cm-content": { caretColor: "var(--s-accent)", padding: "8px 0" },
  ".cm-cursor": { borderLeftColor: "var(--s-accent)" },
  ".cm-gutters": {
    backgroundColor: "var(--s-bg)",
    color: "var(--s-muted)",
    border: "none",
  },
  // подсветка строки полупрозрачная: слой выделения лежит под строками,
  // непрозрачный фон закрывал бы выделенное слово
  ".cm-activeLine": {
    backgroundColor: "color-mix(in srgb, var(--s-panel) 45%, transparent)",
  },
  ".cm-activeLineGutter": {
    backgroundColor: "var(--s-panel)",
    color: "var(--s-text)",
  },
  // селекторы той же специфичности, что у базовой темы CodeMirror, иначе
  // выделение остаётся светло-сиреневым
  "&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, & > .cm-scroller > .cm-selectionLayer .cm-selectionBackground": {
    backgroundColor: "var(--s-accent-a45)",
  },
  ".cm-content ::selection": { backgroundColor: "var(--s-accent-a45)" },
  ".cm-matchingBracket": {
    backgroundColor: "var(--s-accent-a35)",
    outline: "none",
  },
});

export default function CodeEditor({
  value,
  onChange,
  onRun,
  lang = "python",
  className = "",
}) {
  const host = useRef(null);
  const view = useRef(null);
  const cb = useRef({ onChange, onRun });
  cb.current = { onChange, onRun };

  useEffect(() => {
    const state = EditorState.create({
      doc: value,
      extensions: [
        lineNumbers(),
        history(),
        drawSelection(),
        highlightActiveLine(),
        indentOnInput(),
        bracketMatching(),
        indentUnit.of("    "),
        EditorState.tabSize.of(4),
        lang === "sql" ? sql({ dialect: SQLite }) : lang === "rust" ? rust() : python(),
        syntaxHighlighting(highlight),
        theme,
        keymap.of([
          {
            // Ctrl/Cmd+Enter — проверить
            key: "Mod-Enter",
            run: () => {
              cb.current.onRun?.();
              return true;
            },
          },
          indentWithTab,
          ...historyKeymap,
          ...defaultKeymap,
        ]),
        EditorView.updateListener.of((u) => {
          if (
            u.docChanged &&
            !u.transactions.some((tr) => tr.annotation(external))
          ) {
            cb.current.onChange?.(u.state.doc.toString());
          }
        }),
      ],
    });
    view.current = new EditorView({ state, parent: host.current });
    return () => {
      view.current.destroy();
      view.current = null;
    };
    // редактор создаётся один раз; значение синхронизирует эффект ниже
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const v = view.current;
    if (!v) return;
    const cur = v.state.doc.toString();
    if (cur !== value) {
      v.dispatch({
        changes: { from: 0, to: cur.length, insert: value },
        annotations: external.of(true),
      });
    }
  }, [value]);

  return <div className={`cx-cm ${className}`} ref={host} />;
}
