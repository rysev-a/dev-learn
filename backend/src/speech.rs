//! Pronunciation check of a recorded take: Azure AI Speech, "Pronunciation Assessment" through the REST API for short audio.
//! The reference text is the slide's paragraph in the language of the recording, the audio is the take converted to 16 kHz mono PCM
//! (`wav::speech_samples`). The service recognizes only the first ~30 seconds of a request, so a longer take is cut at pauses into parts of at most
//! `CHUNK_SECONDS`; the text is cut to match by recognizing each part without a reference and finding its words in the text (`covered`), and the
//! scores of the parts are merged (`merge`). The reply is reduced to what the author needs: the scores of the whole take and, per word, the score, the kind of
//! error, a wrongly placed pause and the score of every sound. The key is read from the environment and never logged or sent to the client.

use std::{fmt, time::Duration};

use base64::{engine::general_purpose::STANDARD, Engine};
use reqwest::header::{ACCEPT, CONTENT_TYPE};
use serde_json::{json, Value};

use crate::{
    error::{ApiError, ApiResult},
    lang::Lang,
    wav,
};

/// The longest take that is checked (it is sent in parts).
pub const MAX_SECONDS: f64 = 120.0;
/// The longest part of a take sent in one request: the service stops recognizing after about 30 seconds.
const CHUNK_SECONDS: f64 = 26.0;
/// A part ends in the last `CUT_WINDOW` seconds before `CHUNK_SECONDS`, at the quietest place.
const CUT_WINDOW: f64 = 10.0;

#[derive(Clone)]
pub struct Speech {
    key: String,
    endpoint: String,
    client: reqwest::Client,
}

impl fmt::Debug for Speech {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Speech").field("endpoint", &self.endpoint).field("key", &"<hidden>").finish()
    }
}

impl Speech {
    /// `endpoint` is the base address of the speech-to-text service (without a trailing slash).
    pub fn new(key: &str, endpoint: &str) -> Self {
        let client = reqwest::Client::builder().timeout(Duration::from_secs(90)).build().unwrap_or_default();
        Self { key: key.to_string(), endpoint: endpoint.trim_end_matches('/').to_string(), client }
    }

    /// From the environment: `AZURE_SPEECH_KEY` (or `AZURE_SPEECH_KEY_1`, `AZURE_SPEECH_KEY_2` - the two keys of a resource are equal) and
    /// `AZURE_SPEECH_REGION`; `AZURE_SPEECH_ENDPOINT` replaces the address derived from the region. Without a key or a region - `None`.
    pub fn from_env() -> Option<Self> {
        let get = |name: &str| std::env::var(name).ok().map(|v| v.trim().to_string()).filter(|v| !v.is_empty());
        let key = get("AZURE_SPEECH_KEY").or_else(|| get("AZURE_SPEECH_KEY_1")).or_else(|| get("AZURE_SPEECH_KEY_2"))?;
        let endpoint = match get("AZURE_SPEECH_ENDPOINT") {
            Some(endpoint) => endpoint,
            None => format!("https://{}.stt.speech.microsoft.com", get("AZURE_SPEECH_REGION")?),
        };
        Some(Self::new(&key, &endpoint))
    }

    /// Sends 16 kHz mono PCM to the speech-to-text service; with `params` the reply carries the pronunciation scores, without - only the words heard.
    async fn request(&self, wav: Vec<u8>, locale: &str, params: Option<&Value>) -> ApiResult<Value> {
        let url = format!("{}/speech/recognition/conversation/cognitiveservices/v1?language={locale}&format=detailed", self.endpoint);
        let mut req = self.client.post(url).header("Ocp-Apim-Subscription-Key", &self.key).header(CONTENT_TYPE, "audio/wav; codecs=audio/pcm; samplerate=16000").header(ACCEPT, "application/json");
        if let Some(params) = params {
            req = req.header("Pronunciation-Assessment", STANDARD.encode(params.to_string()));
        }
        let res = req.body(wav).send().await.map_err(|e| {
            tracing::warn!("pronunciation service: request failed: {}", e.without_url());
            ApiError::new(502, "The pronunciation service did not answer")
        })?;
        let status = res.status();
        let body = res.text().await.unwrap_or_default();
        if !status.is_success() {
            tracing::warn!("pronunciation service: {status}: {}", body.chars().take(300).collect::<String>());
            return Err(ApiError::new(502, if matches!(status.as_u16(), 401 | 403) { "The pronunciation service refused the key" } else { "The pronunciation service returned an error" }));
        }
        serde_json::from_str(&body).map_err(|_| ApiError::new(502, "The pronunciation service returned an error"))
    }

    /// The words heard in a part of a take (lowercase, no punctuation); empty when no speech was recognized.
    async fn recognize(&self, wav: Vec<u8>, lang: Lang) -> ApiResult<String> {
        let reply = self.request(wav, locale(lang), None).await?;
        let heard = reply.pointer("/NBest/0/Lexical").and_then(Value::as_str).unwrap_or("");
        Ok(heard.to_string())
    }

    /// Scores a part of a take against its text.
    async fn assess_part(&self, wav: Vec<u8>, text: &str, lang: Lang, at: u64) -> ApiResult<Value> {
        let locale = locale(lang);
        let mut params = json!({
            "ReferenceText": text,
            "GradingSystem": "HundredMark",
            "Granularity": "Phoneme",
            "Dimension": "Comprehensive",
            "EnableMiscue": true,
        });
        if locale == "en-US" {
            // the prosody score and the IPA alphabet are available for American English only
            params["EnableProsodyAssessment"] = json!(true);
            params["PhonemeAlphabet"] = json!("IPA");
        }
        let reply = self.request(wav, locale, Some(&params)).await?;
        summarize(&reply, at).ok_or_else(|| ApiError::new(422, "The pronunciation service did not recognize any speech"))
    }

    /// Scores a take (16 kHz mono samples) against its text. A take longer than `CHUNK_SECONDS` is cut at pauses; every part is checked against the
    /// words of the text it contains and the parts are merged into one result (see `summarize` for its shape).
    pub async fn assess(&self, samples: &[i16], text: &str, lang: Lang, at: u64) -> ApiResult<Value> {
        let words: Vec<&str> = text.split_whitespace().collect();
        let seconds = |n: usize| n as f64 / wav::SPEECH_RATE as f64;
        let (mut pos, mut next) = (0usize, 0usize);
        let mut parts: Vec<(f64, Value)> = Vec::new();
        while pos < samples.len() {
            let last = seconds(samples.len() - pos) <= CHUNK_SECONDS;
            let end = if last { samples.len() } else { pos + wav::quietest_point(&samples[pos..], CHUNK_SECONDS - CUT_WINDOW, CHUNK_SECONDS) };
            let part = &samples[pos..end];
            let reference_end = if last { words.len() } else { next + covered(&self.recognize(wav::pcm_wav(part), lang).await?, &words[next..]) };
            if reference_end > next {
                parts.push((seconds(part.len()), self.assess_part(wav::pcm_wav(part), &words[next..reference_end].join(" "), lang, at).await?));
            }
            (pos, next) = (end, reference_end);
        }
        merge(&parts, at).ok_or_else(|| ApiError::new(422, "The pronunciation service did not recognize any speech"))
    }
}

/// A word as compared between what was heard and the text: lowercase letters, digits and apostrophes only (`None` for a bare dash or quote).
fn normalized(word: &str) -> Option<String> {
    let w: String = word.chars().filter(|c| c.is_alphanumeric() || *c == '\'').flat_map(char::to_lowercase).collect();
    (!w.is_empty()).then_some(w)
}

/// How many words of `reference` (from its start) were said in `heard`: the position after the last reference word that the heard words match
/// in order (the longest common subsequence, so a misheard word or a number said in words does not move the cut). 0 when nothing matches.
fn covered(heard: &str, reference: &[&str]) -> usize {
    let heard: Vec<String> = heard.split_whitespace().filter_map(normalized).collect();
    let refs: Vec<(usize, String)> = reference.iter().enumerate().filter_map(|(i, w)| normalized(w).map(|n| (i, n))).collect();
    let (h, r) = (heard.len(), refs.len());
    // lcs[i][j]: the common subsequence of heard[i..] and refs[j..]
    let mut lcs = vec![vec![0u16; r + 1]; h + 1];
    for i in (0..h).rev() {
        for j in (0..r).rev() {
            lcs[i][j] = if heard[i] == refs[j].1 { lcs[i + 1][j + 1] + 1 } else { lcs[i + 1][j].max(lcs[i][j + 1]) };
        }
    }
    let (mut i, mut j, mut last) = (0, 0, None);
    while i < h && j < r {
        if heard[i] == refs[j].1 {
            last = Some(refs[j].0);
            (i, j) = (i + 1, j + 1);
        } else if lcs[i + 1][j] >= lcs[i][j + 1] {
            i += 1;
        } else {
            j += 1;
        }
    }
    last.map_or(0, |i| i + 1)
}

/// The results of the parts of a take as one: the words follow each other, the scores are averages weighted by the length of a part
/// (completeness - by its number of words).
fn merge(parts: &[(f64, Value)], at: u64) -> Option<Value> {
    let (_, first) = parts.first()?;
    if parts.len() == 1 {
        return Some(first.clone());
    }
    let weighted = |key: &str, by: &dyn Fn(&(f64, Value)) -> f64| -> Option<f64> {
        let (sum, weight) = parts.iter().filter_map(|p| p.1.get(key).and_then(Value::as_f64).map(|v| (v * by(p), by(p)))).fold((0.0, 0.0), |a, b| (a.0 + b.0, a.1 + b.1));
        (weight > 0.0).then(|| (sum / weight * 10.0).round() / 10.0)
    };
    let by_time = |p: &(f64, Value)| p.0;
    let by_words = |p: &(f64, Value)| p.1.get("words").and_then(Value::as_array).map_or(0, Vec::len) as f64;
    let words: Vec<Value> = parts.iter().flat_map(|p| p.1.get("words").and_then(Value::as_array).cloned().unwrap_or_default()).collect();
    Some(json!({
        "at": at,
        "pron": weighted("pron", &by_time)?,
        "accuracy": weighted("accuracy", &by_time).unwrap_or(0.0),
        "fluency": weighted("fluency", &by_time).unwrap_or(0.0),
        "completeness": weighted("completeness", &by_words).unwrap_or(0.0),
        "prosody": weighted("prosody", &by_time),
        "words": words,
    }))
}

/// Speech-to-text language of a recording.
pub fn locale(lang: Lang) -> &'static str {
    match lang {
        Lang::Ru => "ru-RU",
        Lang::En => "en-US",
    }
}

fn score(v: &Value, key: &str) -> Option<f64> {
    v.get(key).and_then(Value::as_f64).map(|s| (s * 10.0).round() / 10.0)
}

/// The first error name of a list that is not `None` (`["None"]` and a missing list give `None`).
fn first_error(v: Option<&Value>) -> &str {
    v.and_then(Value::as_array).and_then(|a| a.iter().filter_map(Value::as_str).find(|e| *e != "None")).unwrap_or("None")
}

/// The reply of the service as the interface needs it, `None` when no speech was recognized (`RecognitionStatus` is not `Success`).
/// ```json
/// { "at": 1730000000, "pron": 95.5, "accuracy": 97.0, "fluency": 98.0, "completeness": 100.0, "prosody": 91.2,
///   "words": [ { "word": "set", "accuracy": 100.0, "error": "None", "pause": "None", "phonemes": [ { "phoneme": "s", "accuracy": 100.0 } ] } ] }
/// ```
/// `error` is `None`, `Omission` (a word of the text was not said), `Insertion` (an extra word) or `Mispronunciation`; `pause` is `None`,
/// `UnexpectedBreak` or `MissingBreak`; `prosody` is present for English only.
pub fn summarize(reply: &Value, at: u64) -> Option<Value> {
    if reply.get("RecognitionStatus").and_then(Value::as_str) != Some("Success") {
        return None;
    }
    let best = reply.get("NBest")?.get(0)?;
    let words: Vec<Value> = best
        .get("Words")?
        .as_array()?
        .iter()
        .map(|w| {
            let phonemes: Vec<Value> = w
                .get("Phonemes")
                .and_then(Value::as_array)
                .map(|all| all.iter().map(|p| json!({ "phoneme": p.get("Phoneme").and_then(Value::as_str).unwrap_or(""), "accuracy": score(p, "AccuracyScore").unwrap_or(0.0) })).collect())
                .unwrap_or_default();
            json!({
                "word": w.get("Word").and_then(Value::as_str).unwrap_or(""),
                "accuracy": score(w, "AccuracyScore").unwrap_or(0.0),
                "error": w.get("ErrorType").and_then(Value::as_str).unwrap_or("None"),
                "pause": first_error(w.pointer("/Feedback/Prosody/Break/ErrorTypes")),
                "phonemes": phonemes,
            })
        })
        .collect();
    Some(json!({
        "at": at,
        "pron": score(best, "PronScore")?,
        "accuracy": score(best, "AccuracyScore").unwrap_or(0.0),
        "fluency": score(best, "FluencyScore").unwrap_or(0.0),
        "completeness": score(best, "CompletenessScore").unwrap_or(0.0),
        "prosody": score(best, "ProsodyScore"),
        "words": words,
    }))
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use super::{covered, merge, summarize, Speech};

    fn reply() -> serde_json::Value {
        json!({
            "RecognitionStatus": "Success",
            "NBest": [{
                "PronScore": 83.46, "AccuracyScore": 80.0, "FluencyScore": 98.0, "CompletenessScore": 66.0, "ProsodyScore": 70.04,
                "Words": [
                    { "Word": "think", "AccuracyScore": 55.0, "ErrorType": "Mispronunciation",
                      "Phonemes": [{ "Phoneme": "θ", "AccuracyScore": 31.0 }, { "Phoneme": "ɪ", "AccuracyScore": 97.0 }],
                      "Feedback": { "Prosody": { "Break": { "ErrorTypes": ["None", "UnexpectedBreak"] }, "Intonation": { "ErrorTypes": ["Monotone"] } } } },
                    { "Word": "set", "AccuracyScore": 100.0, "ErrorType": "None", "Phonemes": [], "Feedback": { "Prosody": { "Break": { "ErrorTypes": ["None"] } } } },
                    { "Word": "about", "AccuracyScore": 0.0, "ErrorType": "Omission" }
                ]
            }]
        })
    }

    #[test]
    fn the_reply_is_reduced_to_scores_and_words() {
        let out = summarize(&reply(), 7).unwrap();
        assert_eq!((out["at"].clone(), out["pron"].clone(), out["fluency"].clone(), out["prosody"].clone()), (json!(7), json!(83.5), json!(98.0), json!(70.0)));
        let words = out["words"].as_array().unwrap();
        assert_eq!(words.len(), 3);
        assert_eq!((words[0]["word"].clone(), words[0]["error"].clone(), words[0]["pause"].clone()), (json!("think"), json!("Mispronunciation"), json!("UnexpectedBreak")));
        assert_eq!((words[0]["phonemes"][0]["phoneme"].clone(), words[0]["phonemes"][0]["accuracy"].clone()), (json!("θ"), json!(31.0)));
        assert_eq!((words[1]["error"].clone(), words[1]["pause"].clone()), (json!("None"), json!("None")));
        assert_eq!((words[2]["error"].clone(), words[2]["phonemes"].clone()), (json!("Omission"), json!([])));
    }

    #[test]
    fn a_reply_without_speech_is_not_a_result() {
        assert!(summarize(&json!({ "RecognitionStatus": "NoMatch" }), 0).is_none());
        assert!(summarize(&json!({ "RecognitionStatus": "Success", "NBest": [] }), 0).is_none());
        assert!(summarize(&json!({}), 0).is_none());
    }

    #[test]
    fn prosody_is_absent_when_the_service_does_not_score_it() {
        let mut r = reply();
        r["NBest"][0].as_object_mut().unwrap().remove("ProsodyScore");
        assert!(summarize(&r, 0).unwrap()["prosody"].is_null());
    }

    fn said(text: &str) -> usize {
        let reference: Vec<&str> = "Today we will go through it carefully, and after this lesson you will see sets. This is the foundation of the whole course.".split_whitespace().collect();
        covered(text, &reference)
    }

    #[test]
    fn the_words_heard_tell_where_in_the_text_a_part_ends() {
        // "Today we will go through it carefully," is 7 words, "and after this lesson you will see sets." ends at word 15, the next sentence is 8 more
        assert_eq!(said("today we will go through it carefully"), 7);
        assert_eq!(said("today we will go through it carefully and after this lesson you will see sets"), 15);
        // a misheard word or a skipped one does not move the end; punctuation and case do not matter
        assert_eq!(said("Today we'll go through it carefully, and after this less in you will see sets."), 15);
        assert_eq!(said("today we will go through it carefully and after this lesson you will see sets this is the foundation of the whole course"), 23);
        // an extra heard word in the middle does not break the match; nothing in common is no coverage
        assert_eq!(said("today we will uh go through it carefully"), 7);
        assert_eq!(said("completely different words"), 0);
        assert_eq!(said(""), 0);
    }

    #[test]
    fn numbers_said_in_words_do_not_stop_the_match() {
        let reference: Vec<&str> = "Chapter 1. Sets are everywhere in code.".split_whitespace().collect();
        assert_eq!(covered("chapter one sets are everywhere", &reference), 5);
        assert_eq!(covered("chapter one sets are everywhere in code", &reference), 7);
    }

    #[test]
    fn the_parts_of_a_long_take_become_one_result() {
        let part = |pron: f64, completeness: f64, words: &[&str], prosody: Option<f64>| {
            let mut v = json!({ "at": 1, "pron": pron, "accuracy": pron, "fluency": pron, "completeness": completeness, "prosody": prosody, "words": words.iter().map(|w| json!({ "word": w })).collect::<Vec<_>>() });
            v["prosody"] = json!(prosody);
            v
        };
        let parts = vec![(20.0, part(90.0, 100.0, &["a", "b", "c"], Some(80.0))), (10.0, part(60.0, 50.0, &["d"], Some(50.0)))];
        let out = merge(&parts, 5).unwrap();
        assert_eq!((out["at"].clone(), out["pron"].clone(), out["prosody"].clone()), (json!(5), json!(80.0), json!(70.0)), "weighted by seconds: (90*20+60*10)/30, (80*20+50*10)/30");
        assert_eq!(out["completeness"], json!(87.5), "weighted by words: (100*3+50*1)/4");
        assert_eq!(out["words"].as_array().unwrap().iter().map(|w| w["word"].as_str().unwrap()).collect::<String>(), "abcd");
        // one part is returned as it is; no parts - no result
        assert_eq!(merge(&parts[..1], 9).unwrap(), parts[0].1);
        assert!(merge(&[], 0).is_none());
        // a language without a prosody score has none in the merge either
        assert!(merge(&[(5.0, part(70.0, 100.0, &["a"], None)), (5.0, part(70.0, 100.0, &["b"], None))], 0).unwrap()["prosody"].is_null());
    }

    #[test]
    fn the_key_never_shows_in_debug_output() {
        let s = Speech::new("super-secret-key", "http://localhost:1/");
        let shown = format!("{s:?}");
        assert!(!shown.contains("super-secret-key"), "{shown}");
        assert!(shown.contains("http://localhost:1"));
    }
}
