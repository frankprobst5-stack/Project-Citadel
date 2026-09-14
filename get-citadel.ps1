# CITADEL — one-line bootstrap for Windows, meant to be run straight
# from GitHub: irm <raw-url-to-this-file> | iex
#
# Deliberately tiny and readable start to finish -- since piping a
# script straight into iex means trusting it sight-unseen, this stays
# short enough to actually read in the ten seconds before you run it.
# It does exactly one job: fetch this repo and hand off to the real
# installer (install.bat), the same one anyone downloading the zip by
# hand would run -- this file adds no install logic of its own.

$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/frankprobst5-stack/Project-Citadel"
$ArchiveUrl = "$RepoUrl/archive/refs/heads/main.zip"
$Dest = if ($env:CITADEL_INSTALL_DIR) { $env:CITADEL_INSTALL_DIR } else { "$HOME\citadel" }

Write-Host "============================================================"
Write-Host " PROJECT CITADEL -- one-line installer"
Write-Host "============================================================"

if (Test-Path $Dest) {
    Write-Host "$Dest already exists -- if that's a previous Citadel install,"
    Write-Host "just run its own installer again instead of this bootstrap:"
    Write-Host "  cd $Dest; .\install.bat"
    Write-Host "To install fresh somewhere else instead, set CITADEL_INSTALL_DIR first:"
    Write-Host '  $env:CITADEL_INSTALL_DIR = "C:\citadel2"'
    exit 1
}

$TmpZip = New-TemporaryFile
Rename-Item $TmpZip "$TmpZip.zip"
$TmpZip = "$TmpZip.zip"

try {
    Write-Host "Downloading Citadel from $RepoUrl ..."
    Invoke-WebRequest -Uri $ArchiveUrl -OutFile $TmpZip

    Write-Host "Extracting to $Dest ..."
    $ParentDir = Split-Path -Parent $Dest
    if (-not $ParentDir) { $ParentDir = "." }
    # Only the PARENT needs to exist here, not $Dest itself -- Move-Item
    # below renames GitHub's extracted Project-Citadel-main\ to $Dest,
    # which only works as a rename if $Dest doesn't already exist yet
    # (same bug caught and fixed live in this script's bash twin).
    New-Item -ItemType Directory -Force -Path $ParentDir | Out-Null
    Expand-Archive -Path $TmpZip -DestinationPath $ParentDir -Force

    # GitHub's archive zip extracts to Project-Citadel-main\, not the
    # plain $Dest name -- rename so CITADEL_HOST_PATH (written by
    # install.bat) and every doc's "cd citadel" instruction still point
    # at a stable path.
    Move-Item "$ParentDir\Project-Citadel-main" $Dest
} finally {
    Remove-Item $TmpZip -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Handing off to Citadel's own installer ($Dest\install.bat) ..."
Write-Host ""
Set-Location $Dest
& .\install.bat
