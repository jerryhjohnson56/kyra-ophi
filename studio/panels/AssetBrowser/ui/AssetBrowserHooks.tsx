import React, { useEffect, useMemo, useState } from "react"
import type { HookAction, HookMenuConfig } from "./kyra.assetbrowser.d"
import { useContextMenu } from "./useContextMenu"
import { runHook } from "./runHookClient"

type Props = {
  hooksUrl: string
  projectRoot: string
  selectedFile?: string | null
  onRan?: (result: { code: number, stdout?: string, stderr?: string }) => void
}

export const AssetBrowserHooks: React.FC<Props> = ({ hooksUrl, projectRoot, selectedFile=null, onRan }) => {
  const [menu, setMenu] = useState<HookAction[]>([])
  const { ref, visible, pos, setVisible, onContextMenu } = useContextMenu()

  useEffect(() => {
    (async () => {
      try {
        const resp = await fetch(hooksUrl)
        const data = (await resp.json()) as HookMenuConfig
        setMenu(data.actions || [])
      } catch (e) {
        console.error("[Kyra] Failed to load hooks:", e)
      }
    })()
  }, [hooksUrl])

  const actions = useMemo(() => menu, [menu])

  const run = async (id: string) => {
    setVisible(false)
    const res = await runHook(id, selectedFile || null, actions, projectRoot)
    onRan?.(res)
  }

  return (
    <div ref={ref} onContextMenu={onContextMenu} style={{ width: 0, height: 0 }}>
      {visible && (
        <div style={{
          position: "fixed", left: pos.x, top: pos.y, background: "rgba(30,30,30,0.95)",
          borderRadius: 8, padding: 8, zIndex: 9999, minWidth: 220, boxShadow: "0 6px 30px rgba(0,0,0,0.4)"
        }}>
          {actions.map(a => (
            <div key={a.id}
              onClick={() => run(a.id)}
              style={{ padding: "8px 10px", cursor: "pointer", userSelect: "none" }}
              onMouseEnter={e => (e.currentTarget.style.background = "rgba(255,255,255,0.06)")}
              onMouseLeave={e => (e.currentTarget.style.background = "transparent")}
            >
              {a.label}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
