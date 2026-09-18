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
REM never leaves a stale path behind.
REM
REM Real bug, confirmed 2026-09-16 by an actual Windows tester's fresh
REM install (Mark, N2UGA -- this exact risk was flagged as untested
REM speculation right here before his report came in, now confirmed,
REM not hypothetical): %CD% on Windows returns a backslash path with a
REM drive letter, e.g. C:\Users\name\citadel. Used directly in
REM docker-compose.yml's `${CITADEL_HOST_PATH}:${CITADEL_HOST_PATH}`
REM bind mount, Compose splits that whole string on `:` expecting
REM HOST:CONTAINER[:MODE] -- a raw backslash Windows path contains its
REM own drive-letter colon AND backslashes Compose doesn't parse as
REM path separators, so the split produces more pieces than expected:
REM real error was "mount denied: the source path ... too many
REM colons". Fix converts to Docker Desktop's real WSL2-style path
REM (/c/Users/name/citadel, lowercase drive letter, no colon) --
REM **this exact format is what Mark's own real fresh install
REM confirmed working**, all 11 containers started, not just a format
REM that looks plausible from documentation. (An alternative format,
REM C:/Users/name/citadel with the colon kept, is sometimes cited too,
REM but wasn't the one actually verified working here -- going with
REM the tester-confirmed format over an untested one.)
set "CITADEL_HOST_PATH=%CD%"
if "!CITADEL_HOST_PATH:~1,1!"==":" (
    set "drive=!CITADEL_HOST_PATH:~0,1!"
    set "rest=!CITADEL_HOST_PATH:~2!"
    set "rest=!rest:\=/!"
    set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    set "charslc=abcdefghijklmnopqrstuvwxyz"
    for /l %%i in (0,1,25) do (
        if "!drive!"=="!chars:~%%i,1!" set "drive=!charslc:~%%i,1!"
    )
    set "CITADEL_HOST_PATH=/!drive!!rest!"
) else (
    REM Not a plain drive-letter path (e.g. a UNC path) -- no established
    REM real conversion for that case here, so just avoid backslashes
    REM rather than leaving them entirely unhandled.
    set "CITADEL_HOST_PATH=!CITADEL_HOST_PATH:\=/!"
)
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
    call :ask muster "Muster (Mobile Ops bridge to WayStation)" n

    REM Remote-Ollama-host support, ROADMAP.md v2 backlog -- Ollama lives
    REM under its own "ollama-local" profile (see
    REM modules\ai\compose.fragment.yml), not bundled into "ai"/
    REM "education" directly, so it can be left out when a remote host is
    REM configured. Real bug, confirmed 2026-09-18 by a real Windows
    REM tester (Mark, N2UGA): this script never had this logic at all --
    REM install.sh's Linux/macOS side has always auto-added
    REM "ollama-local" here, but it was never ported to this file, so
    REM every Windows install with AI/Education enabled and no remote
    REM host configured got a dashboard reporting AI offline until the
    REM profile was added to .env by hand.
    set "OLLAMA_REMOTE="
    for /f "tokens=1,* delims==" %%a in ('findstr /b /c:"OLLAMA_REMOTE_HOST=" .env 2^>nul') do set "OLLAMA_REMOTE=%%b"
    echo ,%PROFILES%,|findstr /c:",ai," /c:",education," >nul
    if not errorlevel 1 (
        if "%OLLAMA_REMOTE%"=="" (
            set "PROFILES=%PROFILES%,ollama-local"
            echo -- AI/Education modules selected, no remote host configured --
            echo    running Ollama locally ^(added the 'ollama-local' profile^).
        ) else (
            echo -- OLLAMA_REMOTE_HOST is set ^(%OLLAMA_REMOTE%^) -- Citadel's own
            echo    local Ollama container will NOT start; AI/Education will use
            echo    the remote one instead.
        )
    )

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

REM Real bug, confirmed 2026-09-16 by an actual Windows tester's fresh
REM install (Mark, N2UGA): kiwix-serve is told to load `library.xml`
REM (see modules\knowledge\compose.fragment.yml's `--library
REM library.xml`), and on a fresh install that file doesn't exist at
REM all -- not empty of books, genuinely missing -- so kiwix-serve
REM errors on startup and `restart: unless-stopped` crash-loops it
REM forever. Citadel deliberately doesn't ship any .zim content itself
REM (real offline archives are often multi-GB and choosing what to
REM download is meant to be the operator's own call) -- but it should
REM still start cleanly with zero books instead of crash-looping.
REM Verified directly against the real kiwix-serve image before
REM writing this: a minimal empty library.xml (this exact real schema,
REM not guessed) loads fine -- "The library was successfully loaded,"
REM real HTTP 200, no crash.
if not exist appdata\kiwix-library\library.xml (
    (
        echo ^<?xml version="1.0" encoding="UTF-8" ?^>
        echo ^<library version="20110515"^>
        echo ^</library^>
    ) > appdata\kiwix-library\library.xml
)

echo Starting Citadel - this pulls a handful of container images the first
echo time, so it may take a few minutes...

REM Real bug, confirmed 2026-09-16 by an actual Windows tester's fresh
REM install (Mark, N2UGA): this used to print the "Citadel is up"
REM success banner unconditionally -- on his machine the
REM CITADEL_HOST_PATH mount error above meant containers were only
REM *created*, never running, while the installer still claimed
REM success and pointed him at a dashboard that wasn't actually up.
REM
REM --build added 2026-09-18, also from a real reinstall Mark hit:
REM vault-api has a `build:` directive (see docker-compose.yml), and
REM plain `docker compose up -d` reuses whatever image was already
REM built locally from a previous install even if requirements-docker.txt
REM changed since -- his reinstall crash-looped on a real
REM ModuleNotFoundError for a dependency that IS in the current
REM requirements file, purely because the stale image was never
REM rebuilt. `--build` forces a real rebuild against current source
REM every run, not just on first install.
docker compose up -d --build
if errorlevel 1 (
    echo ============================================================
    echo  docker compose up -d failed -- Citadel is NOT running.
    echo  Scroll up for the real error from Docker, fix it, then run
    echo  this script again ^(or just "docker compose up -d" by hand^).
    echo ============================================================
    pause
    exit /b 1
)

echo ============================================================
echo  Citadel is up. Open your dashboard at:
echo    http://localhost:8085
echo ============================================================
pause
