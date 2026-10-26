//! Скачивание файла из браузера: данные кладутся в `Blob`, по временной ссылке «нажимается» невидимая `<a download>`.

use gloo_timers::callback::Timeout;
use js_sys::{Array, Uint8Array};
use wasm_bindgen::{JsCast, JsValue};
use web_sys::{Blob, BlobPropertyBag, HtmlAnchorElement, Url};

/// Через сколько миллисекунд временная ссылка снимается (скачивание к этому моменту уже началось).
const REVOKE_MS: u32 = 1000;

/// Отдать браузеру байты как файл `name` с типом `mime`.
pub fn save_bytes(bytes: &[u8], mime: &str, name: &str) -> Result<(), JsValue> {
    let parts = Array::of1(&Uint8Array::from(bytes));
    let options = BlobPropertyBag::new();
    options.set_type(mime);
    let blob = Blob::new_with_u8_array_sequence_and_options(&parts, &options)?;
    let url = Url::create_object_url_with_blob(&blob)?;
    let document = web_sys::window().and_then(|w| w.document()).ok_or_else(|| JsValue::from_str("нет документа"))?;
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

/// Отдать текст как файл `name` (UTF-8).
pub fn save_text(text: &str, name: &str) -> Result<(), JsValue> {
    save_bytes(text.as_bytes(), "text/plain;charset=utf-8", name)
}
