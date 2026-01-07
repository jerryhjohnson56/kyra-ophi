import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { checkForUpdate, downloadWithProgress, saveToCache, verifySha256, UpdateFeed, UpdateAsset, Step } from "./UpdateServiceV2";
import { installArtifact } from "./Installer";

type UpdaterState = {
  step: Step;
  checking: boolean;
  hasUpdate: boolean;
  currentVersion: string;
  availableVersion?: string;
  feed?: UpdateFeed | null;
  asset?: UpdateAsset | null;
  progress?: number;
  error?: string;
  checkNow: () => Promise<void>;
  startDownload: () => Promise<void>;
  startInstall: () => Promise<void>;
  lastChecked?: number;
  downloadedPath?: string;
  notes?: string;
  open: boolean;
  setOpen: (v: boolean)=>void;
  log: string[];
};

const Ctx = createContext<UpdaterState | null>(null);

export const UpdaterProviderV2: React.FC<{ children: React.ReactNode; intervalMs?: number }> = ({
  children,
  intervalMs = 6 * 60 * 60 * 1000,
}) => {
  const [open, setOpen] = useState(false);
  const [checking, setChecking] = useState(false);
  const [step, setStep] = useState<Step>("idle");
  const [hasUpdate, setHasUpdate] = useState(false);
  const [currentVersion, setCurrent] = useState("0.0.0");
  const [availableVersion, setAvailable] = useState<string | undefined>();
  const [feed, setFeed] = useState<UpdateFeed | null>(null);
  const [asset, setAsset] = useState<UpdateAsset | null>(null);
  const [progress, setProgress] = useState<number | undefined>(undefined);
  const [error, setError] = useState<string | undefined>(undefined);
  const [lastChecked, setLastChecked] = useState<number | undefined>(undefined);
  const [downloadedPath, setDownloadedPath] = useState<string | undefined>();
  const [notes, setNotes] = useState<string | undefined>("");
  const [log, setLog] = useState<string[]>([]);

  const pushLog = useCallback((m: string) => {
    const ts = new Date().toISOString();
    setLog(prev => [...prev.slice(-500), `[${ts}] ${m}`]);
    console.log("[updater]", m);
  }, []);

  const checkNow = useCallback(async () => {
    setChecking(true); setError(undefined); setStep("checking");
    try {
      const res = await checkForUpdate();
      setHasUpdate(res.hasUpdate);
      setCurrent(res.current);
      setAvailable(res.available);
      setFeed(res.feed || null);
      setAsset(res.asset || null);
      setNotes(res.feed?.notes || "");
      setStep(res.hasUpdate ? "available" : "idle");
      pushLog(res.hasUpdate ? `Update available: v${res.available}` : "No update available");
    } catch (e:any) {
      setError(String(e?.message||e)); setStep("error"); pushLog(`Check failed: ${String(e)}`);
    } finally {
      setChecking(false); setLastChecked(Date.now());
    }
  }, [pushLog]);

  const startDownload = useCallback(async () => {
    if (!asset?.url) return;
    setError(undefined); setProgress(0); setStep("downloading"); setOpen(true);
    pushLog(`Downloading ${asset.name} ...`);
    try {
      const data = await downloadWithProgress(asset.url, (p)=>{
        if (p.percent !== undefined) setProgress(p.percent);
      });
      pushLog(`Downloaded ${data.length} bytes`);
      setStep("verifying"); setProgress(undefined);
      const ok = await verifySha256(data, asset.sha256);
      if (!ok) { setError("SHA-256 mismatch. Aborting."); setStep("error"); pushLog("Hash mismatch"); return; }
      pushLog("Hash verified");
      const path = await saveToCache(asset.name, data);
      setDownloadedPath(path);
      setStep("ready"); pushLog(`Saved to ${path}`);
    } catch(e:any) {
      setError(String(e?.message||e)); setStep("error"); pushLog(`Download error: ${String(e)}`);
    }
  }, [asset, pushLog]);

  const startInstall = useCallback(async () => {
    if (!downloadedPath) return;
    pushLog(`Launching installer: ${downloadedPath}`);
    try {
      await installArtifact(downloadedPath);
    } catch(e:any) {
      setError(String(e?.message||e)); setStep("error"); pushLog(`Install launch failed: ${String(e)}`);
    }
  }, [downloadedPath, pushLog]);

  useEffect(() => {
    checkNow();
    const id = setInterval(checkNow, intervalMs);
    return () => clearInterval(id);
  }, [checkNow, intervalMs]);

  const value: UpdaterState = useMemo(()=> ({
    step, checking, hasUpdate, currentVersion, availableVersion, feed, asset,
    progress, error, checkNow, startDownload, startInstall, lastChecked,
    downloadedPath, notes, open, setOpen, log
  }), [step, checking, hasUpdate, currentVersion, availableVersion, feed, asset, progress, error, checkNow, startDownload, startInstall, lastChecked, downloadedPath, notes, open, log]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
};

export function useUpdaterV2(): UpdaterState {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useUpdaterV2 must be used within UpdaterProviderV2");
  return ctx;
}
