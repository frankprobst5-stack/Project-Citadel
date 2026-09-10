# Real Dockerfile (build-time image), not the runtime-pip-install pattern
# Citadel's other lightweight Python services use (vault-api, vigil-*) --
# those only ever need Flask+requests, a few seconds to install. Cloud9
# needs llama-cpp-python, which compiles native code from source and
# would otherwise redo that same multi-minute compile on every container
# restart. Debian slim, not Alpine, to avoid musl-related build friction
# with llama-cpp-python/numpy wheels -- same "pick what the job actually
# needs" reasoning as the whisper service's ubuntu:26.04 choice elsewhere
# in this compose file.
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
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
