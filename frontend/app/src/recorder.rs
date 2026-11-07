//! Recording voice for a slide in the browser: microphone -> `MediaRecorder` -> one file (webm/opus in Chrome and Firefox, mp4 in Safari),
//! which goes to the backend (`POST /api/records/{book}/{chapter}/{slide}`, `Client::upload_record`). Promises are handled
//! with callbacks: `wasm-bindgen-futures` is not among the dependencies.

use std::{cell::RefCell, rc::Rc};

use js_sys::Array;
use wasm_bindgen::{closure::Closure, JsCast, JsValue};
use web_sys::{AudioBuffer, AudioContext, Blob, BlobEvent, BlobPropertyBag, MediaRecorder, MediaRecorderOptions, MediaStream, MediaStreamConstraints, MediaStreamTrack};

/// Containers by preference; if the browser supports none - its default.
const MIME_TYPES: [&str; 3] = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4"];

/// The microphone is already recording this long before the slide starts to play (the button shows "loading" meanwhile): the first word is not cut off
/// by the start-up of the recorder, however early the author begins to speak.
pub const LEAD_MS: u32 = 2000;
/// The slide's reading time is extended by this much when it is recorded, so that the last word is not cut off by the end of the slide.
pub const TAIL_SECONDS: f64 = 3.0;
/// Silence kept before the first and after the last sound when the recording is trimmed.
const KEEP_BEFORE: f64 = 0.3;
const KEEP_AFTER: f64 = 0.6;

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

/// 16-bit mono PCM WAV from float samples (-1..1).
pub fn encode_wav(samples: &[f32], rate: u32) -> Vec<u8> {
    let data = samples.len() as u32 * 2;
    let mut out = Vec::with_capacity(44 + data as usize);
    out.extend_from_slice(b"RIFF");
    out.extend_from_slice(&(36 + data).to_le_bytes());
    out.extend_from_slice(b"WAVEfmt ");
    out.extend_from_slice(&16u32.to_le_bytes());
    out.extend_from_slice(&1u16.to_le_bytes()); // PCM
    out.extend_from_slice(&1u16.to_le_bytes()); // mono
    out.extend_from_slice(&rate.to_le_bytes());
    out.extend_from_slice(&(rate * 2).to_le_bytes());
    out.extend_from_slice(&2u16.to_le_bytes());
    out.extend_from_slice(&16u16.to_le_bytes());
    out.extend_from_slice(b"data");
    out.extend_from_slice(&data.to_le_bytes());
    for s in samples {
        out.extend_from_slice(&((s.clamp(-1.0, 1.0) * 32767.0).round() as i16).to_le_bytes());
    }
    out
}

/// The part of the recording that holds the speech: from `KEEP_BEFORE` seconds before the first sound to `KEEP_AFTER` after the last one. The recording
/// starts earlier than the slide and ends later (see `LEAD_MS`, `TAIL_SECONDS`); the take must start where the voice starts, or the voice would lag behind the slide.
/// A sound is 30 ms above a level 26 dB under the loudest one, so a click or a breath does not count; a recording with no sound at all is kept whole.
pub fn speech_range(samples: &[f32], rate: u32) -> std::ops::Range<usize> {
    let whole = 0..samples.len();
    let window = (rate as usize / 100).max(1); // 10 ms
    let levels: Vec<f32> = samples.chunks(window).map(|c| (c.iter().map(|s| s * s).sum::<f32>() / c.len() as f32).sqrt()).collect();
    let peak = levels.iter().copied().fold(0.0, f32::max);
    if peak < 0.005 {
        return whole;
    }
    let level = (peak * 0.05).max(0.004);
    let loud = |at: usize| levels[at..at + 3].iter().all(|l| *l > level);
    let (Some(first), Some(last)) = ((0..levels.len().saturating_sub(2)).find(|&i| loud(i)), (0..levels.len().saturating_sub(2)).rev().find(|&i| loud(i))) else { return whole };
    let start = (first * window).saturating_sub((KEEP_BEFORE * rate as f64) as usize);
    let end = ((last + 3) * window + (KEEP_AFTER * rate as f64) as usize).min(samples.len());
    start..end
}

fn mono(buffer: &AudioBuffer) -> Vec<f32> {
    let channels: Vec<Vec<f32>> = (0..buffer.number_of_channels()).filter_map(|c| buffer.get_channel_data(c).ok()).collect();
    let Some(first) = channels.first() else { return Vec::new() };
    (0..first.len()).map(|i| channels.iter().map(|c| c.get(i).copied().unwrap_or(0.0)).sum::<f32>() / channels.len() as f32).collect()
}

/// Turns the recording (webm/mp4 from `MediaRecorder` knows neither its length nor how to seek) into a WAV, which is rewound exactly and has a
/// duration the server can read. `done` receives the file and its duration in seconds; if the browser cannot decode it - the recording as it
/// was, without a duration (the server keeps it, but the player does not play it).
pub fn to_wav(blob: Blob, done: impl FnOnce(Blob, Option<f64>) + 'static) {
    let done = Rc::new(RefCell::new(Some(done)));
    let fail = {
        let (done, blob) = (done.clone(), blob.clone());
        move || {
            if let Some(done) = done.borrow_mut().take() {
                done(blob, None);
            }
        }
    };
    let Ok(ctx) = AudioContext::new() else { return fail() };
    let on_bytes = {
        let fail = fail.clone();
        Closure::once(move |bytes: JsValue| {
            let ctx_done = ctx.clone();
            let Ok(decoding) = bytes.dyn_into::<js_sys::ArrayBuffer>().map_err(|_| ()).and_then(|b| ctx.decode_audio_data(&b).map_err(|_| ())) else { return fail() };
            let on_ok = {
                let done = done.clone();
                Closure::once(move |decoded: JsValue| {
                    let _ = ctx_done.close(); // browsers allow only a few audio contexts at a time
                    let Ok(buffer) = decoded.dyn_into::<AudioBuffer>() else { return };
                    let (samples, rate) = (mono(&buffer), buffer.sample_rate() as u32);
                    let samples = samples[speech_range(&samples, rate)].to_vec();
                    let wav = encode_wav(&samples, rate);
                    let parts = Array::of1(&js_sys::Uint8Array::from(&wav[..]));
                    let options = BlobPropertyBag::new();
                    options.set_type("audio/wav");
                    if let (Ok(file), Some(done)) = (Blob::new_with_u8_array_sequence_and_options(&parts, &options), done.borrow_mut().take()) {
                        done(file, Some(samples.len() as f64 / rate.max(1) as f64));
                    }
                })
            };
            let on_err = Closure::once(move |_: JsValue| fail());
            let _ = decoding.then2(&on_ok, &on_err);
            on_ok.forget();
            on_err.forget();
        })
    };
    let on_err = Closure::once(move |_: JsValue| fail());
    let _ = blob.array_buffer().then2(&on_bytes, &on_err);
    on_bytes.forget();
    on_err.forget();
}

#[cfg(test)]
mod tests {
    use super::{encode_wav, speech_range};

    /// `silence` seconds of a faint hiss, `speech` seconds of a tone, `silence` again (8 kHz).
    fn clip(before: f64, speech: f64, after: f64) -> Vec<f32> {
        let n = |s: f64| (s * 8000.0) as usize;
        let hiss = |i: usize| if i % 2 == 0 { 0.001 } else { -0.001 };
        let mut v: Vec<f32> = (0..n(before)).map(hiss).collect();
        v.extend((0..n(speech)).map(|i| 0.3 * (i as f32 * 0.2).sin()));
        v.extend((0..n(after)).map(hiss));
        v
    }

    #[test]
    fn the_silence_around_the_speech_is_cut_but_a_margin_stays() {
        let v = clip(2.0, 1.0, 3.0);
        let r = speech_range(&v, 8000);
        let (start, end) = (r.start as f64 / 8000.0, r.end as f64 / 8000.0);
        assert!((start - 1.7).abs() < 0.05, "starts 0.3 s before the voice, got {start}");
        assert!((end - 3.6).abs() < 0.05, "ends 0.6 s after the voice, got {end}");
    }

    #[test]
    fn a_click_is_not_speech_and_early_speech_is_kept_from_its_start() {
        let mut v = clip(2.0, 1.0, 1.0);
        v[3000] = 0.9; // a click at 0.375 s, far from the voice
        assert!(speech_range(&v, 8000).start > 8000, "the click does not hold the start back");
        let early = clip(0.1, 1.0, 1.0); // the voice begins at once: nothing before it to cut
        assert_eq!(speech_range(&early, 8000).start, 0);
    }

    #[test]
    fn a_recording_without_sound_is_kept_whole() {
        let v = clip(2.0, 0.0, 0.0);
        assert_eq!(speech_range(&v, 8000), 0..v.len());
        assert_eq!(speech_range(&[], 8000), 0..0);
    }

    #[test]
    fn wav_has_a_header_and_clamped_16_bit_samples() {
        let w = encode_wav(&[0.0, 1.0, -1.0, 2.0], 8000);
        assert_eq!(&w[0..4], b"RIFF");
        assert_eq!(&w[8..16], b"WAVEfmt ");
        assert_eq!(u32::from_le_bytes(w[24..28].try_into().unwrap()), 8000);
        assert_eq!(u32::from_le_bytes(w[40..44].try_into().unwrap()), 8, "four samples of two bytes");
        assert_eq!(w.len(), 44 + 8);
        assert_eq!(i16::from_le_bytes([w[46], w[47]]), 32767);
        assert_eq!(i16::from_le_bytes([w[48], w[49]]), -32767);
        assert_eq!(i16::from_le_bytes([w[50], w[51]]), 32767, "above 1 is clamped");
    }
}
