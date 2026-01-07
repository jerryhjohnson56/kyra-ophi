export async function ollamaGenerate(opts:{host:string, model:string, prompt:string, system?:string}){
  const url = `${opts.host.replace(/\/$/, '')}/api/generate`
  const body = { model: opts.model, prompt: opts.prompt, system: opts.system||"", stream: false }
  const r = await fetch(url, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) })
  if(!r.ok) throw new Error(`Ollama error ${r.status}`)
  const j = await r.json()
  return j.response as string
}
