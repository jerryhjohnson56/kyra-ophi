import React from "react"
export function ControlBar(props:{busy:boolean,onOnce:()=>void,onStart:()=>void,onStop:()=>void,onFix:()=>void}){
  const {busy,onOnce,onStart,onStop,onFix} = props
  return (
    <div style={{display:'flex',gap:8, padding:8, background:'#111', color:'#eee'}}>
      <button disabled={busy} onClick={onOnce}>Run once</button>
      <button disabled={busy} onClick={onStart}>Start loop</button>
      <button onClick={onStop}>Stop loop</button>
      <button disabled={busy} onClick={onFix} title="Fix common stub issues">Preflight Fix</button>
    </div>
  )
}
