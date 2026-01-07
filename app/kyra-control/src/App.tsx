import React, { useEffect, useState } from "react"
import { poolStatus, poolOnce, poolStart, poolStop, preflightFix } from "./lib/api"
import { ControlBar } from "./components/ControlBar"
import { StatusBar } from "./components/StatusBar"
import { QueueTable } from "./components/QueueTable"
import { LogViewer } from "./components/LogViewer"
import { ConfigEditor } from "./components/ConfigEditor"
import { PRList } from "./components/PRList"
import { CopilotPanel } from "./copilot/CopilotPanel"

const REPO = (import.meta as any).env?.KYRA_REPO_ROOT || process.env.KYRA_REPO_ROOT || ""

export default function App(){
  const [status,setStatus] = useState<any>({})
  const [busy,setBusy] = useState(false)
  const [log,setLog] = useState("")

  async function refresh(){
    const out = await poolStatus(REPO)
    try{ setStatus(JSON.parse(out.stdout)) }catch{}
  }
  useEffect(()=>{ refresh(); const id=setInterval(refresh, 2500); return ()=>clearInterval(id) }, [])

  const once = async ()=>{ setBusy(true); const out = await poolOnce(REPO); setBusy(false); setLog(out.stdout + out.stderr) }
  const start = async ()=>{ setBusy(true); const out = await poolStart(REPO); setBusy(false); setLog(out.stdout + out.stderr); await refresh() }
  const stop = async ()=>{ setBusy(true); const out = await poolStop(REPO); setBusy(false); setLog(out.stdout + out.stderr); await refresh() }
  const fix = async ()=>{ setBusy(true); const out = await preflightFix(REPO); setBusy(false); setLog(out.stdout + out.stderr) }

  return (
    <div style={{fontFamily:'Inter, ui-sans-serif, system-ui', background:'#0a0a0a', color:'#efefef', height:'100vh'}}>
      <h2 style={{padding:12}}>Kyra Build Suite</h2>
      <StatusBar status={status} />
      <ControlBar busy={busy} onOnce={once} onStart={start} onStop={stop} onFix={fix} />
      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:16, padding:12}}>
        <div>
          <h3>Logs</h3>
          <LogViewer text={log} />
          <ConfigEditor root={REPO} />
        </div>
        <div>
          <PRList prs={status.prs||[]} />
          <h3>Queue (preview)</h3>
          <QueueTable preview={status.queue||{}} />
          <CopilotPanel />
        </div>
      </div>
    </div>
  )
}
