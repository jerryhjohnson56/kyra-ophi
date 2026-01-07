param([string]$RepoRoot = (Get-Location))
$env:KYRA_REPO_ROOT = $RepoRoot
Set-Location $RepoRoot
python3 scripts/pool_worker_wrapper.py --config pool_config.yaml --once
