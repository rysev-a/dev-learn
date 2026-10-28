//! Downloading a file from the browser: data is put into a `Blob`, and an invisible `<a download>` is "clicked" through a temporary link.

use gloo_timers::callback::Timeout;
use js_sys::{Array, Uint8Array};
use wasm_bindgen::{JsCast, JsValue};
use web_sys::{Blob, BlobPropertyBag, HtmlAnchorElement, Url};

/// After how many milliseconds the temporary link is removed (the download has already started by then).
const REVOKE_MS: u32 = 1000;

/// Hand the browser bytes as a file `name` with type `mime`.
pub fn save_bytes(bytes: &[u8], mime: &str, name: &str) -> Result<(), JsValue> {
    let parts = Array::of1(&Uint8Array::from(bytes));
    let options = BlobPropertyBag::new();
    options.set_type(mime);
    let blob = Blob::new_with_u8_array_sequence_and_options(&parts, &options)?;
    let url = Url::create_object_url_with_blob(&blob)?;
    let document = web_sys::window().and_then(|w| w.document()).ok_or_else(|| JsValue::from_str(i18n::tr("no document")))?;
    let link: HtmlAnchorElement = document.create_element("a")?.dyn_into()?;
    link.set_href(&url);
    link.set_download(name);
    link.click();
    Timeout::new(REVOKE_MS, move || {
        let _ = Url::revoke_object_url(&url);
    })
    .forget();
    Ok(())
}

/// Hand text as a file `name` (UTF-8).
pub fn save_text(text: &str, name: &str) -> Result<(), JsValue> {
    save_bytes(text.as_bytes(), "text/plain;charset=utf-8", name)
}
