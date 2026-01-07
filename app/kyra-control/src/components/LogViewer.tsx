import React from "react"
export function LogViewer(props:{text:string}){
  return <pre style={{whiteSpace:'pre-wrap', background:'#0b0b0b', color:'#8ef', padding:8, height:260, overflow:'auto'}}>{props.text||''}</pre>
}
