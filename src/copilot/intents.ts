// Super-light intent mapper. We don't rely only on LLM; we also regex common ops.
export type Intent =
  | { type: 'STATUS' }
  | { type: 'ONCE' }
  | { type: 'START' }
  | { type: 'STOP' }
  | { type: 'TAIL' }
  | { type: 'PRS' }
  | { type: 'CLAIM' }
  | { type: 'HELP' }
  | { type: 'LLM'; text: string }

export function parseIntent(text: string): Intent {
  const t = text.toLowerCase().trim()
  if (/^status|how.*going|progress|dashboard/.test(t)) return { type:'STATUS' }
  if (/run once|once only|single step/.test(t)) return { type:'ONCE' }
  if (/start( loop)?|go|resume/.test(t)) return { type:'START' }
  if (/stop( loop)?|pause|halt/.test(t)) return { type:'STOP' }
  if (/tail|show.*log|errors?/.test(t)) return { type:'TAIL' }
  if (/prs|pull requests|merge requests|open prs/.test(t)) return { type:'PRS' }
  if (/claim|next item|grab next/.test(t)) return { type:'CLAIM' }
  if (/help|what can you do/.test(t)) return { type:'HELP' }
  return { type:'LLM', text }
}
