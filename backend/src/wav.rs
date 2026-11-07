//! Minimal PCM-WAV handling: duration, joining a chapter's parts into one file (chapter download) and converting a recording to the
//! 16 kHz mono format the speech service takes.

use std::path::Path;

struct Wav {
    channels: u16,
    rate: u32,
    bits: u16,
    data: Vec<u8>,
}

fn read(path: &Path) -> Option<Wav> {
    let b = std::fs::read(path).ok()?;
    if b.len() < 12 || &b[0..4] != b"RIFF" || &b[8..12] != b"WAVE" {
        return None;
    }
    let (mut pos, mut fmt, mut data) = (12usize, None, None);
    while pos + 8 <= b.len() {
        let id = &b[pos..pos + 4];
        let size = u32::from_le_bytes(b[pos + 4..pos + 8].try_into().ok()?) as usize;
        let body = pos + 8;
        let end = (body + size).min(b.len());
        if id == b"fmt " && end - body >= 16 {
            let f = &b[body..end];
            fmt = Some((u16::from_le_bytes([f[2], f[3]]), u32::from_le_bytes([f[4], f[5], f[6], f[7]]), u16::from_le_bytes([f[14], f[15]])));
        } else if id == b"data" {
            data = Some(b[body..end].to_vec());
        }
        pos = body + size + (size & 1);
    }
    let (channels, rate, bits) = fmt?;
    Some(Wav { channels, rate, bits, data: data? })
}

/// Duration in seconds (0 if the file is unreadable).
pub fn duration(path: &Path) -> f64 {
    match read(path) {
        Some(w) if w.rate > 0 && w.channels > 0 && w.bits >= 8 => w.data.len() as f64 / (w.rate as f64 * w.channels as f64 * (w.bits as f64 / 8.0)),
        _ => 0.0,
    }
}

/// Joins parts with the same format; `Err` - formats differ or a file is unreadable.
pub fn concat(paths: &[std::path::PathBuf]) -> Result<Vec<u8>, &'static str> {
    let mut head: Option<(u16, u32, u16)> = None;
    let mut data = Vec::new();
    for p in paths {
        let w = read(p).ok_or("unreadable")?;
        let cur = (w.channels, w.rate, w.bits);
        match head {
            None => head = Some(cur),
            Some(h) if h != cur => return Err("formats differ"),
            _ => {}
        }
        data.extend_from_slice(&w.data);
    }
    let (channels, rate, bits) = head.ok_or("no parts")?;
    Ok(encode(channels, rate, bits, &data))
}

/// A WAV file (44-byte header) around raw little-endian PCM data.
fn encode(channels: u16, rate: u32, bits: u16, data: &[u8]) -> Vec<u8> {
    let block = channels * (bits / 8);
    let mut out = Vec::with_capacity(44 + data.len());
    out.extend_from_slice(b"RIFF");
    out.extend_from_slice(&(36 + data.len() as u32).to_le_bytes());
    out.extend_from_slice(b"WAVEfmt ");
    out.extend_from_slice(&16u32.to_le_bytes());
    out.extend_from_slice(&1u16.to_le_bytes());
    out.extend_from_slice(&channels.to_le_bytes());
    out.extend_from_slice(&rate.to_le_bytes());
    out.extend_from_slice(&(rate * block as u32).to_le_bytes());
    out.extend_from_slice(&block.to_le_bytes());
    out.extend_from_slice(&bits.to_le_bytes());
    out.extend_from_slice(b"data");
    out.extend_from_slice(&(data.len() as u32).to_le_bytes());
    out.extend_from_slice(data);
    out
}

/// Samples of 16-bit PCM averaged over the channels, as numbers in -1..1.
fn mono_samples(w: &Wav) -> Vec<f32> {
    let channels = w.channels as usize;
    w.data.chunks_exact(2 * channels).map(|frame| frame.chunks_exact(2).map(|s| i16::from_le_bytes([s[0], s[1]]) as f32 / 32768.0).sum::<f32>() / channels as f32).collect()
}

/// Resamples by averaging the source samples that fall into each output sample (it also filters what a lower rate cannot hold).
fn resample(samples: &[f32], from: u32, to: u32) -> Vec<f32> {
    if from == to || samples.is_empty() {
        return samples.to_vec();
    }
    let step = from as f64 / to as f64;
    let count = (samples.len() as f64 / step).floor() as usize;
    (0..count)
        .map(|j| {
            let (a, b) = (j as f64 * step, (j + 1) as f64 * step);
            let (first, last) = (a.floor() as usize, (b.ceil() as usize).min(samples.len()));
            let (mut sum, mut weight) = (0.0f64, 0.0f64);
            for (i, s) in samples.iter().enumerate().take(last).skip(first) {
                let w = (b.min(i as f64 + 1.0) - a.max(i as f64)).max(0.0);
                sum += *s as f64 * w;
                weight += w;
            }
            if weight > 0.0 { (sum / weight) as f32 } else { 0.0 }
        })
        .collect()
}

/// Sample rate the speech service takes.
pub const SPEECH_RATE: usize = 16000;

/// The recording as 16 kHz mono 16-bit samples (the speech service's format); `None` if it is not readable 16-bit PCM.
pub fn speech_samples(path: &Path) -> Option<Vec<i16>> {
    let w = read(path)?;
    if w.bits != 16 || w.channels == 0 || w.rate == 0 {
        return None;
    }
    Some(resample(&mono_samples(&w), w.rate, SPEECH_RATE as u32).into_iter().map(|s| (s.clamp(-1.0, 1.0) * 32767.0).round() as i16).collect())
}

/// A WAV file of 16 kHz mono 16-bit samples.
pub fn pcm_wav(samples: &[i16]) -> Vec<u8> {
    let data: Vec<u8> = samples.iter().flat_map(|s| s.to_le_bytes()).collect();
    encode(1, SPEECH_RATE as u32, 16, &data)
}

/// Where to cut `samples` inside `from_s..to_s` seconds: the middle of the quietest stretch (a pause between words), as an index into `samples`.
pub fn quietest_point(samples: &[i16], from_s: f64, to_s: f64) -> usize {
    let at = |seconds: f64| ((seconds * SPEECH_RATE as f64) as usize).min(samples.len());
    let (from, to) = (at(from_s), at(to_s));
    let (step, window) = (SPEECH_RATE / 100, SPEECH_RATE * 12 / 100);
    if to < from + window {
        return (from + to) / 2;
    }
    let energy = |start: usize| samples[start..start + window].iter().map(|s| (*s as f64) * (*s as f64)).sum::<f64>() / window as f64;
    let starts: Vec<usize> = (from..=to - window).step_by(step).collect();
    let energies: Vec<f64> = starts.iter().map(|s| energy(*s)).collect();
    let limit = energies.iter().cloned().fold(f64::INFINITY, f64::min) * 1.5 + 1.0;
    // the longest quiet stretch (the earliest if equal)
    let (mut best, mut i) = ((0usize, 0usize), 0usize);
    while i < energies.len() {
        let begin = i;
        while i < energies.len() && energies[i] <= limit {
            i += 1;
        }
        if i - begin > best.1 {
            best = (begin, i - begin);
        }
        i += 1;
    }
    let (first, last) = (best.0, best.0 + best.1.max(1) - 1);
    (starts[first] + starts[last] + window) / 2
}

#[cfg(test)]
mod tests {
    use super::{duration, encode, pcm_wav, quietest_point, speech_samples, SPEECH_RATE};

    fn temp(name: &str, bytes: &[u8]) -> std::path::PathBuf {
        let p = std::env::temp_dir().join(format!("cs-core-wav-{}-{name}.wav", std::process::id()));
        std::fs::write(&p, bytes).unwrap();
        p
    }

    fn tone(rate: u32, seconds: f64, channels: u16) -> Vec<u8> {
        let frames = (rate as f64 * seconds) as usize;
        let data: Vec<u8> = (0..frames).flat_map(|i| (0..channels).flat_map(move |_| (((i as f64 * 440.0 * std::f64::consts::TAU / rate as f64).sin() * 16000.0) as i16).to_le_bytes())).collect();
        encode(channels, rate, 16, &data)
    }

    #[test]
    fn a_recording_becomes_16_khz_mono_of_the_same_length() {
        for (rate, channels) in [(48000, 1), (44100, 2), (16000, 1), (8000, 1)] {
            let src = temp(&format!("src-{rate}-{channels}"), &tone(rate, 1.5, channels));
            let out = temp(&format!("out-{rate}-{channels}"), &pcm_wav(&speech_samples(&src).unwrap()));
            assert!((duration(&out) - 1.5).abs() < 0.01, "{rate} Hz x{channels}: {}", duration(&out));
            let bytes = std::fs::read(&out).unwrap();
            assert_eq!((u16::from_le_bytes([bytes[22], bytes[23]]), u32::from_le_bytes(bytes[24..28].try_into().unwrap()), u16::from_le_bytes([bytes[34], bytes[35]])), (1, 16000, 16));
        }
    }

    #[test]
    fn the_signal_keeps_its_level_when_the_rate_drops() {
        let src = temp("level-src", &tone(48000, 1.0, 1));
        let peak = speech_samples(&src).unwrap().iter().map(|s| s.unsigned_abs()).max().unwrap();
        assert!((14000..=16100).contains(&peak), "peak {peak}");
    }

    #[test]
    fn what_is_not_16_bit_pcm_is_refused() {
        assert!(speech_samples(&temp("junk", b"not a wav")).is_none());
        assert!(speech_samples(&temp("eight", &encode(1, 8000, 8, &[128; 800]))).is_none());
        assert!(speech_samples(std::path::Path::new("/definitely/missing.wav")).is_none());
    }

    /// `seconds` of a loud tone with silent gaps `(start, length)` in seconds.
    fn speech_with_pauses(seconds: f64, pauses: &[(f64, f64)]) -> Vec<i16> {
        (0..(seconds * SPEECH_RATE as f64) as usize)
            .map(|i| {
                let t = i as f64 / SPEECH_RATE as f64;
                if pauses.iter().any(|(a, len)| t >= *a && t < a + len) { 0 } else { ((t * 300.0 * std::f64::consts::TAU).sin() * 9000.0) as i16 }
            })
            .collect()
    }

    #[test]
    fn the_cut_falls_in_the_middle_of_the_pause() {
        // short breaths at 18.0 and 22.0 s, a real pause (0.6 s) at 24.4 s: the cut is in the longest quiet stretch
        let samples = speech_with_pauses(30.0, &[(18.0, 0.15), (22.0, 0.15), (24.4, 0.6)]);
        let cut = quietest_point(&samples, 16.0, 26.0) as f64 / SPEECH_RATE as f64;
        assert!((24.4..24.95).contains(&cut), "cut at {cut}");
        // the window decides: the same take cut in 17..21 s lands on the breath at 18.0
        let cut = quietest_point(&samples, 17.0, 21.0) as f64 / SPEECH_RATE as f64;
        assert!((18.0..18.2).contains(&cut), "cut at {cut}");
    }

    #[test]
    fn without_any_pause_the_cut_is_still_inside_the_window() {
        let samples = speech_with_pauses(30.0, &[]);
        let cut = quietest_point(&samples, 16.0, 26.0) as f64 / SPEECH_RATE as f64;
        assert!((16.0..=26.0).contains(&cut), "cut at {cut}");
        assert_eq!(quietest_point(&samples[..10], 0.0, 5.0), 5, "a window shorter than the analysis step: its middle");
    }
}
