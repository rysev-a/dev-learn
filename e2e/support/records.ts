import { expect, type APIRequestContext } from "@playwright/test";

/* Helpers for the slide recording tests: the demo administrator and takes put on the server through the API. */

export const ADMIN = { email: "programmer@mail.com", password: "programmer" };

/** Silence of the given length as a 16-bit mono WAV. */
export function wav(seconds = 1): Buffer {
  const data = Buffer.alloc(16000 * seconds);
  const head = Buffer.alloc(44);
  head.write("RIFF", 0);
  head.writeUInt32LE(36 + data.length, 4);
  head.write("WAVEfmt ", 8);
  head.writeUInt32LE(16, 16);
  head.writeUInt16LE(1, 20);
  head.writeUInt16LE(1, 22);
  head.writeUInt32LE(8000, 24);
  head.writeUInt32LE(16000, 28);
  head.writeUInt16LE(2, 32);
  head.writeUInt16LE(16, 34);
  head.write("data", 36);
  head.writeUInt32LE(data.length, 40);
  return Buffer.concat([head, data]);
}

export async function record(request: APIRequestContext, token: string, chapter: number, slide: number, lang: "ru" | "en", seconds = 1) {
  const res = await request.post(`/api/records/12/${chapter}/${slide}?lang=${lang}`, { headers: { Authorization: `Bearer ${token}`, "Content-Type": "audio/wav" }, data: wav(seconds) });
  expect(res.ok(), `record ${lang} ${slide}: ${res.status()}`).toBeTruthy();
}

/** Deletes every take of the first slides in both languages: the recordings live on the server disk and outlive a test run. */
export async function clearRecords(request: APIRequestContext, token: string, chapter: number): Promise<void> {
  const headers = { Authorization: `Bearer ${token}` };
  for (const lang of ["ru", "en"]) {
    for (const slide of [0, 1, 2]) {
      const list = (await (await request.get(`/api/records/12/${chapter}/${slide}?lang=${lang}`, { headers })).json()) as { takes: { id: number }[] };
      for (const t of list.takes) await request.delete(`/api/records/12/${chapter}/${slide}/${t.id}?lang=${lang}`, { headers });
    }
  }
}

