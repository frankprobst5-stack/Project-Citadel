# Real Dockerfile (build-time image), not the runtime-pip-install pattern
# Citadel's other lightweight Python services use (vault-api, vigil-*).
# Used to also need build-essential+cmake here to compile
# llama-cpp-python from source (Cloud9 bundled its own private AI model)
# -- removed 2026-09-14 now that ai.py calls Citadel's shared Ollama
# over HTTP instead, so there's no native code to build anymore. Stayed
# on Debian slim rather than switching to the Alpine pattern other
# lightweight services use, since that's a bigger change than this
# session's actual goal (removing the duplicate AI stack) and yt-dlp/
# nltk's own dependency footprint on Alpine hasn't been verified.
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY server ./server

# NOTE: the WordNet corpus (dictionary.py's `nltk.data.path`) has to live
# under data/nltk_data on the *host*, not baked in here -- data/ is a
# docker-compose volume mount, so anything written to /app/data during
# the image build would just get shadowed by the host directory at
# container start anyway. It's provisioned as real host data instead
# (copied once from the upstream Cloud9 repo's already-downloaded copy).

# data/ (real kid-generated content) and models/ (1.1GB GGUF) are volume
# mounts from docker-compose.yml, not baked into the image -- same
# reasoning as every other appdata/ real-data exclusion in this project.
WORKDIR /app/server
CMD ["python", "docker_launcher.py"]
