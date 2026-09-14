@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ============================================================
echo  PROJECT CITADEL - Installer (Windows)
echo ============================================================

where docker >nul 2>nul
if errorlevel 1 (
    echo Docker isn't installed. Install Docker Desktop first, then run this
    echo script again: https://docs.docker.com/get-docker/
    echo This also installs/enables WSL2, which may ask you to restart your
    echo computer -- that's normal, just run this script again afterward.
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

REM Real, live-found gap (2026-09-14) -- same reasoning as install.sh's
REM equivalent check: the two checks above only confirm the docker CLI
REM and compose plugin exist, not that the daemon is actually running.
REM "docker isn't installed" and "Docker Desktop was never launched" are
REM very different problems for a first-time user, and only this check
REM tells them apart.
docker info >nul 2>nul
if errorlevel 1 (
    echo Docker is installed, but isn't running yet.
    echo Start Docker Desktop ^(look for its whale icon in the system tray^),
    echo wait for it to say "running," then run this script again.
    pause
    exit /b 1
)

if not exist .env (
    copy /y .env.example .env >nul
    echo Created .env from the template ^(edit it later if you want to change ports^).
)

REM CITADEL_HOST_PATH: same purpose as install.sh's (see that file's own
REM comment) -- the real absolute path Citadel lives at, needed by
REM vault-api's "one-click apply" module toggle in Settings. Always
REM rewritten, not just on a fresh install, so a moved install folder
REM never leaves a stale path behind. NOTE, untested (no Windows
REM environment available while building this): Docker Desktop's own
REM host<->container path translation for bind mounts may not treat a
REM raw Windows path (C:\...) the same way this mechanism was verified
REM to work on Linux -- if "Apply" fails on Windows with a docker.sock/
REM path-mount error, that's the first thing to check.
set "CITADEL_HOST_PATH=%CD%"
findstr /b /c:"CITADEL_HOST_PATH=" .env >nul 2>nul
if errorlevel 1 (
    >>.env echo CITADEL_HOST_PATH=%CITADEL_HOST_PATH%
) else (
    for /f "delims=" %%i in (.env) do (
        set "line=%%i"
        if "!line:~0,18!"=="CITADEL_HOST_PATH=" (
            >>.env.tmp echo CITADEL_HOST_PATH=%CITADEL_HOST_PATH%
        ) else (
            >>.env.tmp echo(!line!
        )
    )
    move /y .env.tmp .env >nul
)

REM Module picker (ROADMAP.md Phase B) -- same logic as install.sh's, see
REM that file's own comment for why this only runs when .env has no
REM COMPOSE_PROFILES line yet (a fresh install), and why titles/hardware
REM flags are just duplicated here from each modules\<name>\manifest.json
REM rather than parsed from it -- plain batch has no real JSON parser, and
REM adding a dependency just for this isn't worth it.
findstr /b /c:"COMPOSE_PROFILES=" .env >nul 2>nul
if errorlevel 1 (
    echo.
    echo Which optional modules do you want to run? ^(each is a separate
    echo Docker container, or a small group of them -- see modules\^<name^>\
    echo manifest.json for exactly what each one is.^) Answer y/n for each;
    echo just press Enter to accept the suggested default.
    echo.
    set "PROFILES="

    call :ask vigil "Home Monitor Matrix" n
    call :ask camera "Webcam Motion Detection (Project IBRIS)" y
    call :ask ai "Off-Grid AI" n
    call :ask knowledge "Knowledge Base" n
    call :ask notes "Note Storage Vault" n
    call :ask hardware "Project Intercept / Trunked Scanner" y
    call :ask audio "Whisper Audio Transcription" n
    call :ask education "Home Education Hub" n
    call :ask recipes "Recipes and Meal Planner" n

    >>.env echo COMPOSE_PROFILES=%PROFILES%
    echo.
    echo Selected modules: %PROFILES%
)
goto :after_picker

:ask
REM %1=profile name  %2=display title  %3=y means "requires hardware, default no"
set "DEFAULT=y"
set "SUFFIX=[Y/n]"
if "%~3"=="y" (
    set "DEFAULT=n"
    set "SUFFIX=[y/N] (needs real hardware passed through)"
)
set "ANSWER="
set /p "ANSWER=  %~2 (%~1) %SUFFIX%: "
if "%ANSWER%"=="" set "ANSWER=%DEFAULT%"
if /i "%ANSWER:~0,1%"=="y" (
    if defined PROFILES (set "PROFILES=%PROFILES%,%~1") else (set "PROFILES=%~1")
)
exit /b 0

:after_picker

REM Pre-create bind-mount folders so Docker doesn't create them with the
REM wrong ownership, which would block you from managing your own files
REM later. Always creates every module's folders regardless of which ones
REM were actually selected above -- harmless, and means enabling a module
REM later via .env, without re-running this script, still works.
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
if not exist backups mkdir backups

echo Starting Citadel - this pulls a handful of container images the first
echo time, so it may take a few minutes...
docker compose up -d

echo ============================================================
echo  Citadel is up. Open your dashboard at:
echo    http://localhost:8085
echo ============================================================
pause
