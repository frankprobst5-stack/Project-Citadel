@echo off
setlocal

cd /d "%~dp0"

echo ============================================================
echo  PROJECT CITADEL - Installer (Windows)
echo ============================================================

where docker >nul 2>nul
if errorlevel 1 (
    echo Docker isn't installed. Install Docker Desktop first, then run this
    echo script again: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

docker compose version >nul 2>nul
if errorlevel 1 (
    echo Docker is installed, but the 'docker compose' plugin isn't available.
    echo Update Docker Desktop, then try again.
    pause
    exit /b 1
)

if not exist .env (
    copy /y .env.example .env >nul
    echo Created .env from the template ^(edit it later if you want to change ports^).
)

REM Pre-create bind-mount folders so Docker doesn't create them with the
REM wrong ownership, which would block you from managing your own files later.
if not exist appdata\kiwix-library mkdir appdata\kiwix-library
if not exist appdata\kolibri_home mkdir appdata\kolibri_home
if not exist appdata\ollama mkdir appdata\ollama
if not exist appdata\open-webui mkdir appdata\open-webui
if not exist appdata\flatnotes mkdir appdata\flatnotes
if not exist appdata\media-vault\videos mkdir appdata\media-vault\videos
if not exist appdata\media-vault\mp3s mkdir appdata\media-vault\mp3s
if not exist appdata\media-vault\pdfs mkdir appdata\media-vault\pdfs
if not exist appdata\media-vault\notes-data mkdir appdata\media-vault\notes-data
if not exist appdata\mealie\data mkdir appdata\mealie\data
if not exist appdata\whisper-models mkdir appdata\whisper-models
if not exist appdata\cloud9\data mkdir appdata\cloud9\data
if not exist appdata\cloud9\models mkdir appdata\cloud9\models

echo Starting Citadel - this pulls a handful of container images the first
echo time, so it may take a few minutes...
docker compose up -d

echo ============================================================
echo  Citadel is up. Open your dashboard at:
echo    http://localhost:8085
echo ============================================================
pause
