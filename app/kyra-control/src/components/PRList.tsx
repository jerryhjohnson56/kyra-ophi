import React from "react"
export function PRList(props:{prs:any[]}){
  const prs = props.prs||[]
  return (
    <div>
      <h3>Open PRs</h3>
      <ul>
        {prs.map((p:any)=>(<li key={p.number}><a href={p.webUrl} target="_blank">{p.title} ({p.headRefName})</a></li>))}
      </ul>
    </div>
  )
}
