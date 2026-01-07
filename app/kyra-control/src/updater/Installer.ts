import { open as openPath } from "@tauri-apps/api/shell";
import { Command } from "@tauri-apps/api/shell";
import { sep } from "@tauri-apps/api/path";

export async function installArtifact(filePath: string): Promise<void> {
  try {
    // Linux: make AppImage executable if needed
    if (filePath.toLowerCase().endsWith(".appimage")) {
      try {
        await new Command("bash", ["-lc", `chmod +x "${filePath}"`]).execute();
      } catch {}
    }
    await openPath(filePath);
  } catch (e) {
    console.error("Failed to open installer:", e);
    throw e;
  }
}
