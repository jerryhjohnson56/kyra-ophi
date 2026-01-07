import React from "react"
export function QueueTable(props:{preview:any}){
  const q = props.preview || { items:[] }
  return (
    <div>
      <table style={{width:'100%', color:'#ddd'}}>
        <thead><tr><th>ID</th><th>Title</th><th>Lang</th><th>Status</th></tr></thead>
        <tbody>
          {(q.items||[]).map((r:any,i:number)=>(
            <tr key={i}><td>{r.id}</td><td>{r.title}</td><td>{r.lang}</td><td>{r.status}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
