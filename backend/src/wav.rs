//! Минимальная работа с PCM-WAV: длительность и склейка частей главы в один файл (скачивание главы).

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

/// Длительность в секундах (0, если файл не читается).
pub fn duration(path: &Path) -> f64 {
    match read(path) {
        Some(w) if w.rate > 0 && w.channels > 0 && w.bits >= 8 => w.data.len() as f64 / (w.rate as f64 * w.channels as f64 * (w.bits as f64 / 8.0)),
        _ => 0.0,
    }
}

/// Склеивает части с одинаковым форматом; `Err` — форматы различаются или файл не читается.
pub fn concat(paths: &[std::path::PathBuf]) -> Result<Vec<u8>, &'static str> {
    let mut head: Option<(u16, u32, u16)> = None;
    let mut data = Vec::new();
    for p in paths {
        let w = read(p).ok_or("не читается")?;
        let cur = (w.channels, w.rate, w.bits);
        match head {
            None => head = Some(cur),
            Some(h) if h != cur => return Err("форматы различаются"),
            _ => {}
        }
        data.extend_from_slice(&w.data);
    }
    let (channels, rate, bits) = head.ok_or("нет частей")?;
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
    out.extend_from_slice(&data);
    Ok(out)
}
