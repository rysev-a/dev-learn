//! Recording voice for a slide in the browser: microphone -> `MediaRecorder` -> one file (webm/opus in Chrome and Firefox, mp4 in Safari),
//! which goes to the backend (`POST /api/records/{book}/{chapter}/{slide}`, `Client::upload_record`). Promises are handled
//! with callbacks: `wasm-bindgen-futures` is not among the dependencies.

use std::{cell::RefCell, rc::Rc};

use js_sys::Array;
use wasm_bindgen::{closure::Closure, JsCast, JsValue};
use web_sys::{Blob, BlobEvent, BlobPropertyBag, MediaRecorder, MediaRecorderOptions, MediaStream, MediaStreamConstraints, MediaStreamTrack};

/// Containers by preference; if the browser supports none - its default.
const MIME_TYPES: [&str; 3] = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4"];

/// Recording in progress: the microphone is taken, chunks accumulate until stop.
pub struct Recording {
    stream: MediaStream,
    recorder: MediaRecorder,
    chunks: Rc<RefCell<Vec<Blob>>>,
    on_data: Closure<dyn FnMut(BlobEvent)>,
}

fn js_message(e: &JsValue) -> String {
    e.dyn_ref::<js_sys::Error>().map(|e| String::from(e.message())).or_else(|| e.as_string()).unwrap_or_else(|| i18n::tr("Microphone is unavailable").to_string())
}

/// Asks for the microphone and starts recording; `done` receives the recording or the reason for refusal (no permission or device, old browser).
pub fn start(done: impl FnOnce(Result<Recording, String>) + 'static) {
    let Some(devices) = web_sys::window().and_then(|w| w.navigator().media_devices().ok()) else {
        return done(Err(i18n::tr("Microphone is unavailable").to_string()));
    };
    let constraints = MediaStreamConstraints::new();
    constraints.set_audio(&JsValue::TRUE);
    let promise = match devices.get_user_media_with_constraints(&constraints) {
        Ok(p) => p,
        Err(e) => return done(Err(js_message(&e))),
    };
    // one `FnOnce` for two promise outcomes
    let done = Rc::new(RefCell::new(Some(done)));
    let ok = {
        let done = done.clone();
        Closure::once(move |stream: JsValue| {
            if let Some(done) = done.borrow_mut().take() {
                done(begin(stream));
            }
        })
    };
    let err = Closure::once(move |e: JsValue| {
        if let Some(done) = done.borrow_mut().take() {
            done(Err(js_message(&e)));
        }
    });
    let _ = promise.then2(&ok, &err);
    ok.forget();
    err.forget();
}

fn begin(stream: JsValue) -> Result<Recording, String> {
    let stream: MediaStream = stream.dyn_into().map_err(|_| i18n::tr("Microphone is unavailable").to_string())?;
    let options = MediaRecorderOptions::new();
    if let Some(mime) = MIME_TYPES.iter().find(|m| MediaRecorder::is_type_supported(m)) {
        options.set_mime_type(mime);
    }
    let recorder = MediaRecorder::new_with_media_stream_and_media_recorder_options(&stream, &options).map_err(|e| js_message(&e))?;
    let chunks = Rc::new(RefCell::new(Vec::new()));
    let on_data = {
        let chunks = chunks.clone();
        Closure::<dyn FnMut(BlobEvent)>::new(move |ev: BlobEvent| {
            if let Some(b) = ev.data() {
                chunks.borrow_mut().push(b);
            }
        })
    };
    recorder.set_ondataavailable(Some(on_data.as_ref().unchecked_ref()));
    if let Err(e) = recorder.start() {
        release(&stream);
        return Err(js_message(&e));
    }
    Ok(Recording { stream, recorder, chunks, on_data })
}

impl Recording {
    /// Stops recording and releases the microphone; `done` receives the finished file when the browser has given the last chunk (the `stop` event).
    pub fn stop(self, done: impl FnOnce(Blob) + 'static) {
        let Recording { stream, recorder, chunks, on_data } = self;
        let mime = recorder.mime_type();
        let on_stop = Closure::once(move |_: JsValue| {
            let _on_data = on_data; // the chunk handler lives until the `stop` event
            let parts = Array::new();
            for b in chunks.borrow().iter() {
                parts.push(b);
            }
            let options = BlobPropertyBag::new();
            options.set_type(&mime);
            if let Ok(blob) = Blob::new_with_blob_sequence_and_options(&parts, &options) {
                done(blob);
            }
        });
        recorder.set_onstop(Some(on_stop.as_ref().unchecked_ref()));
        on_stop.forget();
        let _ = recorder.stop();
        release(&stream);
    }

    /// Cancels recording (leaving the page): the file is not assembled, the microphone is released.
    pub fn cancel(self) {
        let _ = self.recorder.stop();
        release(&self.stream);
    }
}

fn release(stream: &MediaStream) {
    for t in stream.get_tracks().iter() {
        if let Ok(t) = t.dyn_into::<MediaStreamTrack>() {
            t.stop();
        }
    }
}
