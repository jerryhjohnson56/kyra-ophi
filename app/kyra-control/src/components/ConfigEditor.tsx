import React, {useEffect, useState} from "react"
import YAML from "yaml"
import { run } from "../lib/shell"

export function ConfigEditor(props:{root:string}){
  const [text,setText] = useState("")
  const [msg,setMsg] = useState<string|undefined>()
  const file = "pool_config.yaml"

  useEffect(()=>{(async()=>{
    const out = await run(["bash","-lc", `cat ${file} || true`], props.root)
    setText(out.stdout)
  })()}, [props.root])

  async function save(){
    try{ YAML.parse(text) }catch(e:any){ setMsg("YAML error: "+e.message); return }
    await run(["bash","-lc", `cat > ${file} <<'YAML'\n${text}\nYAML`], props.root)
    setMsg("Saved.")
  }

  return (
    <div>
      <div style={{display:'flex',gap:8,alignItems:'center'}}>
        <h3>pool_config.yaml</h3>
        <button onClick={save}>Save</button>
        <span style={{color:'#8f8'}}>{msg}</span>
      </div>
      <textarea value={text} onChange={e=>setText(e.target.value)} style={{width:'100%',height:220,background:'#0b0b0b',color:'#eee'}}/>
    </div>
  )
}
