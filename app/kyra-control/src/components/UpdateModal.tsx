import React from "react";
import "../styles/updater.css";
import { useUpdaterV2 } from "../updater/UpdaterProviderV2";

export default function UpdateModal(){
  const { open, setOpen, step, availableVersion, progress, error, startDownload, startInstall, log } = useUpdaterV2();
  if (!open) return null;

  const steps = [
    { key:"available", label:"Ready to download" },
    { key:"downloading", label:"Downloading..." },
    { key:"verifying", label:"Verifying..." },
    { key:"ready", label:"Ready to install" },
    { key:"error", label:"Error" },
  ] as const;

  const renderAction = () => {
    if (step === "available") return <button className="ky-btn" onClick={startDownload}>Download</button>;
    if (step === "ready") return <button className="ky-btn" onClick={startInstall}>Install</button>;
    return <button className="ky-btn" onClick={()=>setOpen(false)}>Close</button>;
  };

  return (
    <div className="ky-modal-back" onClick={()=>setOpen(false)}>
      <div className="ky-modal" onClick={e=>e.stopPropagation()}>
        <div className="ky-h1">Kyra Control — Update {availableVersion ? `v${availableVersion}` : ""}</div>
        <div className="ky-row">
          <div className="ky-muted">Status:</div>
          <div style={{fontWeight:600}}>{steps.find(s=>s.key===step as any)?.label||step}</div>
        </div>
        {progress !== undefined && (
          <div className="ky-row" style={{alignItems:"stretch"}}>
            <div className="ky-muted">Progress</div>
            <div style={{flex:1}} className="ky-progress"><div style={{width:`${progress}%`}}/></div>
            <div style={{width:40, textAlign:"right"}}>{progress}%</div>
          </div>
        )}
        {error && <div className="ky-row" style={{color:"#ff6b6b"}}>Error: {error}</div>}
        <div className="ky-row" style={{marginTop:8, justifyContent:"flex-end"}}>
          {renderAction()}
        </div>
        <div className="ky-row" style={{flexDirection:"column", alignItems:"stretch"}}>
          <div className="ky-muted">Log</div>
          <div className="ky-log">{log.map((l,i)=><div key={i}>{l}</div>)}</div>
        </div>
      </div>
    </div>
  );
}
