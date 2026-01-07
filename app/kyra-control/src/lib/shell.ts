import { Command } from "@tauri-apps/api/shell"
export async function run(cmd: string[], cwd: string){
  const c = new Command(cmd[0], cmd.slice(1), { cwd })
  const out = await c.execute()
  return { code: out.code ?? 0, stdout: out.stdout, stderr: out.stderr }
}
