param([string]$Message = "Saved")

$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to commit."
    exit 0
}

git add -A

$staged = git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "No staged changes to commit."
    exit 0
}

git commit -m $Message

$branch = git rev-parse --abbrev-ref HEAD
$upstream = git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null
if ($LASTEXITCODE -eq 0) {
    git push
} else {
    git push -u origin $branch
}
