import React from "react";
import "../styles/updater.css";
import { useUpdaterV2 } from "../updater/UpdaterProviderV2";

export default function UpdateBanner(){
  const { hasUpdate, availableVersion, setOpen, notes } = useUpdaterV2();
  if (!hasUpdate) return null;
  return (
    <div className="ky-banner">
      <div>
        <div style={{fontWeight:700}}>Update available: v{availableVersion}</div>
        {notes && <div className="ky-muted" style={{maxWidth:600}}>{notes}</div>}
      </div>
      <div style={{display:"flex", gap:8}}>
        <button className="ky-btn" onClick={()=>setOpen(true)}>Update now</button>
      </div>
    </div>
  );
}
