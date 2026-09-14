# Real Dockerfile, added 2026-09-14 (see appdata/media-vault/Dockerfile's
# own comment for the full "shine offline" reasoning -- whisper was one
# of the 5 services that used to `apt-get install` at every container
# restart, needing live internet access to Ubuntu's mirrors just to come
# back up).
#
# ubuntu:26.04 specifically, unchanged from before -- the real
# `whisper.cpp` apt package (1.8.3+dfsg-2) only exists in that release's
# `universe` repo (confirmed live this project, not guessed).
#
# curl+ca-certificates are baked in here too, not just whisper.cpp --
# they're real apt packages themselves (see modules/audio/compose.fragment.yml's
# `command:`, which still does its own one-time `curl -L -o
# ggml-base.en.bin ...` model download at first run into the persisted
# `whisper-models` volume -- that's legitimate first-run-only data
# provisioning, not a dependency install, so it deliberately stays in
# `command:` rather than being baked into the image, matching this
# project's convention of never baking real/large data into an image).
FROM ubuntu:26.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    whisper.cpp \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
