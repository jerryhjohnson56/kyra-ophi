import { platform } from "@tauri-apps/api/os";

export async function osExts(): Promise<string[]> {
  const os = await platform();
  if (os === "macos") return [".dmg", ".app.tar.gz"];
  if (os === "windows") return [".msi", ".exe"];
  return [".AppImage", ".appimage", ".deb"];
}
