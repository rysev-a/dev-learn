//! Small DOM helpers.

use leptos::{
    ev::EventDescriptor,
    leptos_dom::helpers::{window_event_listener, window_event_listener_untyped},
    prelude::on_cleanup,
};
use wasm_bindgen::{closure::Closure, JsCast};

/// Window event listener for the lifetime of the owner (component): removed on cleanup.
pub fn on_window<E>(event: E, handler: impl Fn(E::EventType) + 'static)
where
    E: EventDescriptor + 'static,
    E::EventType: JsCast,
{
    let handle = window_event_listener(event, handler);
    on_cleanup(move || handle.remove());
}

/// Same for an event that is not among the typed ones (for example `fullscreenchange`).
pub fn on_window_untyped(event: &str, handler: impl Fn() + 'static) {
    let handle = window_event_listener_untyped(event, move |_| handler());
    on_cleanup(move || handle.remove());
}

/// Element size observer: while the value is alive, `on_resize` is called on every size change.
pub struct ResizeGuard {
    observer: web_sys::ResizeObserver,
    _callback: Closure<dyn FnMut(js_sys::Array, web_sys::ResizeObserver)>,
}

impl Drop for ResizeGuard {
    fn drop(&mut self) {
        self.observer.disconnect();
    }
}

pub fn observe_resize(elements: &[web_sys::Element], on_resize: impl Fn() + 'static) -> Option<ResizeGuard> {
    let callback = Closure::<dyn FnMut(js_sys::Array, web_sys::ResizeObserver)>::new(move |_, _| on_resize());
    let observer = web_sys::ResizeObserver::new(callback.as_ref().unchecked_ref()).ok()?;
    for el in elements {
        observer.observe(el);
    }
    Some(ResizeGuard { observer, _callback: callback })
}

/// Document root element as `HtmlElement` (for CSS variables and fullscreen).
pub fn root() -> Option<web_sys::HtmlElement> {
    web_sys::window()?.document()?.document_element()?.dyn_into().ok()
}

pub fn set_root_var(name: &str, value: &str) {
    if let Some(r) = root() {
        let _ = r.style().set_property(name, value);
    }
}

pub fn remove_root_var(name: &str) {
    if let Some(r) = root() {
        let _ = r.style().remove_property(name);
    }
}
