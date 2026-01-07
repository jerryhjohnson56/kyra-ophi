param([string]$RepoRoot = (Get-Location))
Set-Location $RepoRoot
if (Test-Path ".kyra_pool.pid") {
  $pid = Get-Content ".kyra_pool.pid"
  try { Stop-Process -Id $pid -ErrorAction Stop; Write-Host "Stopped $pid" } catch {}
  Remove-Item ".kyra_pool.pid" -ErrorAction Ignore
} else {
  Write-Host "No PID file."
}
