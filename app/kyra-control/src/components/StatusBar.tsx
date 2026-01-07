import React from "react"
export function StatusBar(props:{status:any}){
  const s = props.status || {}
  const q = s.queue || {}
  return (
    <div style={{padding:8, background:'#181818', color:'#cfcfcf'}}>
      <b>Loop:</b> {s.loop_running ? "Running" : "Stopped"}
      {s.pid ? ` (PID: ${s.pid})` : ""} &nbsp;&nbsp;
      <b>Active:</b> {s.active_claim?.id || "—"} &nbsp;&nbsp;
      <b>Total items:</b> {q.total ?? "—"} &nbsp;&nbsp;
      <b>Open PRs:</b> {(s.prs?.length)||0}
    </div>
  )
}
