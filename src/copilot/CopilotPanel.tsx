import React, { useMemo, useState } from "react"
import { useChat, Msg } from "./useChat"
import { parseIntent } from "./intents"
import { Tools } from "./tools"
import { ollamaGenerate } from "./ollama"

const REPO = (import.meta as any).env?.KYRA_REPO_ROOT || process.env.KYRA_REPO_ROOT || ""
const OLLAMA = (import.meta as any).env?.KYRA_COPILOT_OLLAMA || process.env.KYRA_COPILOT_OLLAMA || "http://127.0.0.1:11434"
const MODEL = (import.meta as any).env?.KYRA_COPILOT_MODEL || process.env.KYRA_COPILOT_MODEL || "qwen2.5-coder:7b"

export function CopilotPanel(){
  const { msgs, push, reset, inputRef } = useChat([
    { role:'assistant', text: "Hi! I can check status, run once, start/stop, show logs, list PRs, or claim the next item. What do you need?" }
  ])
  const [busy,setBusy] = useState(false)
  const [confirm,setConfirm] = useState<{label:string, do:()=>Promise<void>}|null>(null)

  async function runIntent(text:string){
    const intent = parseIntent(text)
    const exec = async (fn:()=>Promise<any>, label:string)=>{
      setConfirm({ label, do: async ()=>{
        setConfirm(null); setBusy(true)
        try{
          const out = await fn()
          push({ role:'assistant', text: "```\n"+(out.stdout||out.stderr||"Done.")+"\n```" })
        }catch(e:any){
          push({ role:'assistant', text: "Failed: "+(e?.message||String(e)) })
        }finally{ setBusy(false) }
      }})
    }
    switch(intent.type){
      case 'STATUS': return exec(()=>Tools.status(REPO), "Run status now?")
      case 'ONCE':   return exec(()=>Tools.once(REPO), "Run one cycle now?")
      case 'START':  return exec(()=>Tools.start(REPO), "Start loop?")
      case 'STOP':   return exec(()=>Tools.stop(REPO), "Stop loop?")
      case 'TAIL':   return exec(()=>Tools.tail(REPO), "Show recent logs?")
      case 'PRS':    return exec(()=>Tools.prs(REPO), "List open PRs?")
      case 'CLAIM':  return exec(()=>Tools.claim(REPO), "Claim next item?")
      case 'HELP':   return push({ role:'assistant', text: "I can: status, run once, start, stop, tail logs, list PRs, claim next. Try: “run once”." })
      case 'LLM': {
        setBusy(true)
        try{
          const sys = "You are Kyra Build Copilot. "+
            "Keep replies short. If user asks to do something, say what you'll do, then ask for confirmation."
          const prompt = msgs.map(m => f"{m.role.upper()}: {m.text}").join("\n")+"\nUSER: "+text+"\nASSISTANT:"
          const resp = await ollamaGenerate({ host: OLLAMA, model: MODEL, prompt, system: sys })
          push({ role:'assistant', text: resp.trim() })
        }catch(e:any){
          push({ role:'assistant', text: "Local LLM error: "+(e?.message||String(e)) })
        }finally{ setBusy(false) }
        return
      }
    }
  }

  const onSend = async (e: React.FormEvent)=>{
    e.preventDefault()
    const el = e.target as HTMLFormElement
    const inp = el.querySelector("input[name='msg']") as HTMLInputElement
    const text = inp.value.trim()
    if(!text) return
    push({ role:'user', text })
    inp.value = ""
    await runIntent(text)
  }

  return (
    <div style={{background:'#111', borderRadius:8, padding:12}}>
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <h3>Copilot</h3>
        <div style={{opacity:.7}}>Model: {MODEL}</div>
      </div>

      <div style={{height:300, overflow:'auto', background:'#0b0b0b', padding:8, borderRadius:6}}>
        {msgs.map((m,i)=>(
          <div key={i} style={{margin:'6px 0'}}>
            <b style={{color:m.role==='user'?'#9cf':'#9f9'}}>{m.role}:</b> <span style={{whiteSpace:'pre-wrap'}}>{m.text}</span>
          </div>
        ))}
      </div>

      {confirm && (
        <div style={{marginTop:8, padding:8, background:'#221', borderRadius:6}}>
          <div style={{marginBottom:6}}>{confirm.label}</div>
          <button disabled={busy} onClick={()=>confirm.do()}>Yes</button>
          <button disabled={busy} onClick={()=>setConfirm(null)} style={{marginLeft:8}}>Cancel</button>
        </div>
      )}

      <form onSubmit={onSend} style={{display:'flex', gap:8, marginTop:8}}>
        <input name="msg" placeholder="ask: status / run once / show logs / list PRs ..." style={{flex:1}} />
        <button disabled={busy}>Send</button>
      </form>
    </div>
  )
}
