import { useEffect, useRef, useState } from "react"

export function useContextMenu() {
  const [visible, setVisible] = useState(false)
  const [pos, setPos] = useState<{x:number,y:number}>({x:0,y:0})
  const ref = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const onClick = () => setVisible(false)
    document.addEventListener("click", onClick)
    return () => document.removeEventListener("click", onClick)
  }, [])

  const onContextMenu = (e: React.MouseEvent) => {
    e.preventDefault()
    setPos({ x: e.clientX, y: e.clientY })
    setVisible(true)
  }

  return { ref, visible, pos, setVisible, onContextMenu }
}
