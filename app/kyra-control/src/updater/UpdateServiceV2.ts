import { appCacheDir, join } from "@tauri-apps/api/path";
import { writeBinaryFile, createDir, BaseDirectory } from "@tauri-apps/api/fs";
import { getVersion } from "@tauri-apps/api/app";
import { checkPermission, requestPermission } from "@tauri-apps/api/notification";
import { open as openShell } from "@tauri-apps/api/shell";
import { sha256Hex } from "./hash";
import { osExts } from "./platform";

export type UpdateAsset = { name: string; url: string; sha256?: string | null };
export type UpdateFeed = { version: string; notes?: string; assets: UpdateAsset[] };

const FEED_BASE = (import.meta.env.VITE_KYRA_UPDATE_FEED_BASE || "").trim();
const GH_OWNER = (import.meta.env.VITE_GH_OWNER || "").trim();
const GH_REPO = (import.meta.env.VITE_GH_REPO || "").trim();
const PIN_VERSION = (import.meta.env.VITE_KYRA_UPDATE_VERSION || "").trim();

function normalize(v: string) {
  const s = (v || "").replace(/^v/i, "");
  const parts = s.split(".").map(x => parseInt(x, 10) || 0);
  while (parts.length < 3) parts.push(0);
  return parts.slice(0, 3) as [number, number, number];
}
function gt(a: string, b: string) {
  const A = normalize(a), B = normalize(b);
  for (let i=0;i<3;i++){ if (A[i]>B[i]) return true; if (A[i]<B[i]) return false; }
  return false;
}
function inferFeedBase(): string | null {
  if (FEED_BASE) return FEED_BASE.replace(/\/$/, "");
  if (GH_OWNER && GH_REPO) return `https://${GH_OWNER}.github.io/${GH_REPO}/updates`;
  return null;
}
async function fetchJSON(url: string) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${url}`);
  return r.json();
}

export async function currentVersion(): Promise<string> {
  try { return await getVersion(); } catch { return (import.meta.env.VITE_APP_VERSION || "0.0.0"); }
}

export async function getFeed(): Promise<UpdateFeed | null> {
  const base = inferFeedBase();
  if (!base) return null;
  const tag = PIN_VERSION || "latest";
  const url = `${base}/${tag}.json`;
  return await fetchJSON(url) as UpdateFeed;
}

export async function pickAsset(feed: UpdateFeed): Promise<UpdateAsset | null> {
  const exts = await osExts();
  const a = (feed.assets||[]).find(x => exts.some(e => x.name.toLowerCase().endsWith(e.toLowerCase())));
  return a || null;
}

export type DlProgress = { received: number; total?: number; percent?: number };
export type Step = "idle"|"checking"|"available"|"downloading"|"verifying"|"ready"|"error";

export async function checkForUpdate() {
  const cur = await currentVersion();
  const feed = await getFeed();
  if (!feed) return { hasUpdate:false, current:cur };
  const available = (feed.version||"").replace(/^v/i,"");
  const has = gt(available, cur.replace(/^v/i,""));
  const asset = has ? await pickAsset(feed) : null;
  return { hasUpdate: has, current: cur, available, feed, asset };
}

export async function downloadWithProgress(url: string, onProgress: (p: DlProgress)=>void): Promise<Uint8Array> {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`HTTP ${r.status} downloading ${url}`);
  const total = Number(r.headers.get("content-length") || 0) || undefined;
  const reader = r.body?.getReader();
  if (!reader) {
    const buf = new Uint8Array(await r.arrayBuffer());
    onProgress({ received: buf.length, total, percent: 100 });
    return buf;
  }
  let received = 0;
  const chunks: Uint8Array[] = [];
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    if (value) {
      chunks.append ? chunks.append(value) : chunks.push(value);
      received += value.length;
      const percent = total ? Math.min(100, Math.round((received/total)*100)) : undefined;
      onProgress({ received, total, percent });
    }
  }
  // concat
  const size = chunks.reduce((n,c)=>n+c.length,0);
  const out = new Uint8Array(size);
  let off=0; for (const c of chunks){ out.set(c,off); off+=c.length; }
  return out;
}

export async function saveToCache(filename: string, data: Uint8Array): Promise<string> {
  try { await createDir("", { dir: BaseDirectory.AppCache, recursive: true }); } catch {}
  await writeBinaryFile({ contents: data, path: filename }, { dir: BaseDirectory.AppCache });
  const base = await appCacheDir();
  return await join(base, filename);
}

export async function verifySha256(buf: Uint8Array, expect?: string|null): Promise<boolean> {
  if (!expect) return true; // skip if not provided
  const hex = await sha256Hex(buf.buffer);
  return hex.lower ? hex.lower() == expect.lower() : hex.toLowerCase() === expect.toLowerCase();
}
