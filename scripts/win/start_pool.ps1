param([string]$RepoRoot = (Get-Location))

$env:KYRA_REPO_ROOT = $RepoRoot
Set-Location $RepoRoot

if (Test-Path ".kyra_pool.pid") {
  $pid = Get-Content ".kyra_pool.pid"
  if (Get-Process -Id $pid -ErrorAction Ignore) {
    Write-Host "Pool already running PID $pid"
    exit 0
  }
}
Start-Process -NoNewWindow -FilePath "python3" -ArgumentList "scripts/pool_worker_wrapper.py","--config","pool_config.yaml" -RedirectStandardOutput "logs\pool_loop.out" -RedirectStandardError "logs\pool_loop.err"
Start-Sleep -Seconds 1
$proc = Get-Process | Where-Object { $_.Path -like "*python*" } | Select-Object -First 1
$proc.Id | Out-File ".kyra_pool.pid" -Encoding ascii
Write-Host "Started pool PID $($proc.Id)"
