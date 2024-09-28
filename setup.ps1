function IsInstalled {
    param (
        [string]$command
    )
    return Get-Command $command -ErrorAction SilentlyContinue
}

if (IsInstalled python) {
    $PYTHON_CMD = "python"
} elseif (IsInstalled python3) {
    $PYTHON_CMD = "python3"
} else {
    Write-Host "[!!]: Python is not installed. Please install Python." -ForegroundColor Red
    exit 1
}

Write-Host "[ii]: Python is installed: $($PYTHON_CMD --version)"

if (IsInstalled pip) {
    $PIP_CMD = "pip"
} elseif (IsInstalled pip3) {
    $PIP_CMD = "pip3"
} else {
    Write-Host "[!!]: Python-pip is not installed. Please install pip." -ForegroundColor Red
    exit 1
}

Write-Host "[ii]: Python-pip is installed: $($PIP_CMD --version)"

if (Test-Path requirements.txt) {
    Write-Host "[ii]: Installing dependencies from requirements.txt"
    & $PIP_CMD install -r requirements.txt
} else {
    Write-Host "[!!]: requirements.txt not found. Skipping dependency installation" -ForegroundColor Yellow
}

Write-Host "[ii]: Generate a Github PAT, preferably fine tuned, with write access to only the repository intended to use as C2"
$key = Read-Host -Prompt "[**]: Enter your key"

$keyContent = "GITHUB_API_KEY='$key'"
Set-Content -Path key.py -Value $keyContent

Write-Host "[ii]: Key saved to key.py"

exit 0
