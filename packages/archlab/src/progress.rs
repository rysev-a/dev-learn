//! What a solution unlocks: composite elements (XOR, XNOR…) stay locked until built by hand.
//! Port of the pure part of `exercise-progress.ts`; "is it solved" is known by the caller (browser or account).

use crate::model::GateType;
use crate::registry::composite_requirement;

/// Is the element composite (NAND, XOR, XNOR, DFF).
pub fn is_composite(ty: GateType) -> bool {
    composite_requirement(ty).is_some()
}

/// Is the element unlocked: composite ones unlock after being built by hand. `solved(section, exercise)`
/// tells whether the exercise is solved.
pub fn is_gate_unlocked(ty: GateType, solved: &dyn Fn(&str, &str) -> bool) -> bool {
    match composite_requirement(ty) {
        None => true,
        Some((slug, id)) => solved(slug, id),
    }
}
