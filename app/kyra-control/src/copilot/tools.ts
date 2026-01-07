import { Command } from "@tauri-apps/api/shell"
async function run(cmd: string[], cwd: string){
  const c = new Command(cmd[0], cmd.slice(1), { cwd })
  const out = await c.execute()
  return { code: out.code ?? 0, stdout: out.stdout, stderr: out.stderr }
}
export const Tools = {
  async status(root:string){ return run(["python3","scripts/pool_api.py","status"], root) },
  async once(root:string){ return run(["python3","scripts/pool_api.py","once"], root) },
  async start(root:string){ return run(["python3","scripts/pool_api.py","start"], root) },
  async stop(root:string){ return run(["python3","scripts/pool_api.py","stop"], root) },
  async prs(root:string){ return run(["gh","pr","list","--state","open","--json","number,title,headRefName,webUrl"], root) },
  async claim(root:string){ return run(["python3","scripts/claim_item.py","--manifest","manifest.json","--root","."], root) },
  async tail(root:string){ return run(["bash","-lc","tail -n 200 logs/pool_loop.out || true"], root) },
}
