# Zed Windows Local Chinese Build Script
[CmdletBinding()]
param(
    [switch]$Restore
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)

Set-Location $RootDir

if ($Restore) {
    Write-Host "[*] Restoring original source files..." -ForegroundColor Yellow
    python "$ScriptDir/patch.py" --restore
    exit 0
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Zed Windows Chinese Build Pipeline" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

# 2. Check Rust / Cargo
if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "[!] cargo was not found in PATH." -ForegroundColor Red
    Write-Host "    Please install Rust via https://rustup.rs/ before building locally," -ForegroundColor Yellow
    Write-Host "    OR push this branch to GitHub and let GitHub Actions build it automatically." -ForegroundColor Green
    exit 1
}

# 3. Apply Chinese Patch
Write-Host "[1/3] Applying Chinese Localization Patches..." -ForegroundColor Green
python "$ScriptDir/patch.py"

# 4. Cargo Build
Write-Host "[2/3] Building Zed in release mode (cargo build --release --package zed)..." -ForegroundColor Green
cargo build --release --package zed

# 5. Output
$ExePath = Join-Path $RootDir "target\release\zed.exe"
if (Test-Path $ExePath) {
    Write-Host "[3/3] Build Succeeded!" -ForegroundColor Green
    Write-Host "Output: $ExePath" -ForegroundColor Cyan
} else {
    Write-Error "Build finished but zed.exe was not found."
}
