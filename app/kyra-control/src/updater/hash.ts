export async function sha256Hex(buf: ArrayBuffer): Promise<string> {
  // Browser crypto in Tauri front-end
  const digest = await crypto.subtle.digest("SHA-256", buf);
  const arr = Array.from(new Uint8Array(digest));
  return arr.map(b => b.toString(16).padStart(2, "0")).join("");
}
