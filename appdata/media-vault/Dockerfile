# Real Dockerfile, added 2026-09-14 as part of hardening Citadel for
# "shine offline": vault-api used to `pip install`+`apk add` at every
# container start (docker-compose.yml's old `command:`), which meant it
# could not even restart without live internet access to PyPI/Alpine's
# mirrors -- a direct contradiction for a system whose whole pitch is
# working when the grid AND the internet are both down. See
# ROADMAP.md's Phase 3 entry for the full audit (5 services had this
# problem, not just this one).
#
# docker-cli + docker-cli-compose are baked in here, not conditionally
# installed -- they back the real, always-available Settings > Modules
# "one-click apply" feature (modules_manager.py's apply_compose()),
# not something optional.
#
# app.py itself STAYS volume-mounted (see docker-compose.yml's own
# `./appdata/media-vault:/app` mount) -- this Dockerfile only removes
# the runtime dependency install, nothing else about how the container
# works changes. Editing app.py still needs no rebuild, same as today.
FROM python:3.10-alpine

RUN apk add --no-cache docker-cli docker-cli-compose

COPY requirements-docker.txt /tmp/requirements-docker.txt
RUN pip install --no-cache-dir -r /tmp/requirements-docker.txt

WORKDIR /app
