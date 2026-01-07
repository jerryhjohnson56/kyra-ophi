import { run } from "./shell"
export async function poolStatus(root:string){ return run(["python3","scripts/pool_api.py","status"], root) }
export async function poolOnce(root:string){ return run(["python3","scripts/pool_api.py","once"], root) }
export async function poolStart(root:string){ return run(["python3","scripts/pool_api.py","start"], root) }
export async function poolStop(root:string){ return run(["python3","scripts/pool_api.py","stop"], root) }
export async function preflightFix(root:string){ return run(["python3","scripts/fix_all_stubs.py"], root) }
