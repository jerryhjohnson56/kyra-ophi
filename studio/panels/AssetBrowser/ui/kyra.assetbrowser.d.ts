export type HookAction = {
  id: string
  label: string
  runner: string
  args: string[]
  extensions?: string[]
  needs?: string[]
}
export type HookMenuConfig = {
  version: string
  actions: HookAction[]
}
