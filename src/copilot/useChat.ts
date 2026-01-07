import { useEffect, useRef, useState } from "react"
export type Msg = { role:'user'|'assistant'|'system', text:string }
export function useChat(initial: Msg[] = []){
  const [msgs,setMsgs] = useState<Msg[]>(initial)
  const inputRef = useRef<HTMLInputElement|null>(null)
  function push(m:Msg){ setMsgs(prev=>[...prev, m]) }
  function reset(){ setMsgs([]) }
  return { msgs, push, reset, inputRef }
}
