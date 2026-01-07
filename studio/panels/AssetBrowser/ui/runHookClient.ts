/* Kyra hook runner client (Tauri/Electron/Proxy) */
import type { HookAction } from "./kyra.assetbrowser.d"

type ExecResult = { code: number; stdout?: string; stderr?: string }

async function tryTauri(cmd: string[], cwd: string): Promise<ExecResult | null> {
  try {
    // Lazy import to avoid bundling errors in non-Tauri builds
    // @ts-ignore
    const { Command } = await import("@tauri-apps/api/shell")
    const command = new Command(cmd[0], cmd.slice(1), { cwd })
    const out = await command.execute()
    return { code: out.code ?? 0, stdout: out.stdout, stderr: out.stderr }
  } catch { return null }
}

async function tryElectron(cmd: string[], cwd: string): Promise[ExecResult | null> {
  try {
    // @ts-ignore
    const cp = window?.require?.("child_process")
    if (!cp) return null
    const res = cp.spawnSync(cmd[0], cmd.slice(1), { cwd, encoding: "utf8" })
    return { code: res.status ?? 0, stdout: res.stdout, stderr: res.stderr }
  } catch { return null }
}

async function tryProxy(cmd: string[], cwd: string): Promise<ExecResult | null> {
  try {
    const url = (globalThis as any).KYRA_HOOK_PROXY || import.meta?.env?.KYRA_HOOK_PROXY || ""
    if (!url) return null
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cmd, cwd })
    })
    const data = await resp.json()
    return data
  } catch { return null }
}

export async function runHook(actionId: string, filePath: string | null, menu: HookAction[], projectRoot: string): Promise<ExecResult> {
  const action = menu.find(a => a.id === actionId)
  if (!action) return { code: 127, stderr: `Unknown action ${actionId}` }

  // Compose command line from menu args (replace ${SELECTED_FILE})
  const args = action.args.map(a => a.replace("${SELECTED_FILE}", filePath || ""))
  const cmd = ["python3", "creator/scripts/run_hook.py", *args]  // note: rely on run_hook.py to dispatch

  // Try Tauri, then Electron, then Proxy
  const tauri = await tryTauri(cmd, projectRoot); if (tauri) return tauri
  const electron = await tryElectron(cmd, projectRoot); if (electron) return electron
  const proxy = await tryProxy(cmd, projectRoot); if (proxy) return proxy

  return { code: 126, stderr: "No native execution backend available (Tauri/Electron/Proxy missing)" }
}
