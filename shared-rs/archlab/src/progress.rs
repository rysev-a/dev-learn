//! Что открывается решением: составные элементы (XOR, XNOR…) закрыты, пока не собраны вручную.
//! Порт чистой части `exercise-progress.ts`; «решено ли» знает вызывающий (браузер или кабинет).

use crate::model::GateType;
use crate::registry::composite_requirement;

/// Составной ли элемент (NAND, XOR, XNOR, DFF).
pub fn is_composite(ty: GateType) -> bool {
    composite_requirement(ty).is_some()
}

/// Открыт ли элемент: составные открываются после сборки их вручную. `solved(раздел, упражнение)`
/// говорит, решено ли упражнение.
pub fn is_gate_unlocked(ty: GateType, solved: &dyn Fn(&str, &str) -> bool) -> bool {
    match composite_requirement(ty) {
        None => true,
        Some((slug, id)) => solved(slug, id),
    }
}
