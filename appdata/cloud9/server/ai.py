import json
import os

import requests

import interactivity

# Cloud9 used to bundle its own private llama-cpp-python + a 1.1GB Qwen
# GGUF model -- removed 2026-09-14 in favor of calling Citadel's shared
# Ollama instance instead, so the whole system only ever runs one
# inference engine, not two competing for the same RAM. See
# docker-compose.yml's `ai` module fragment: `ollama`'s service is now
# tagged with both the "ai" and "education" profiles, so it starts
# automatically whenever Cloud9 (the "education" module) is enabled,
# with no need to also turn on the separate general-purpose "ai" chat
# module. citadel-ollama is reachable here because both containers sit
# on the same `citadel-net` Docker network.
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://citadel-ollama:11434")
# llama3.2:1b -- already pulled for Citadel's general "ai" module and
# the same size/capability class as the Qwen model this used to bundle,
# so switching to it costs no extra download.
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")

SYSTEM_PROMPT = (
    "You are Ollie, the AI learning companion on Cloud9, a learning dashboard for a curious kid. "
    "Talk like a friendly, patient helper, not a corporate assistant. "
    "Keep replies short - a few sentences at most - and use plain, simple words. "
    "You help with reading, writing, spelling, math, and coding small scripts, and you're happy to just chat. "
    "If asked to explain an error or a new word, break it into small, encouraging steps. "
    "Never discuss violence, weapons, drugs, dating, or other adult topics - if asked, gently steer back "
    "to something fun to learn or build instead. If you don't know something, say so plainly.\n\n"
    "Teaching Mode -- ROADMAP.md's core rule, apply it to every answer: "
    "never do for the learner what they can reasonably be guided to do themselves. "
    "Prefer a hint over the answer. Break a hard problem into smaller steps instead of solving it outright. "
    "Ask a comprehension question after they read something, or ask what evidence supports a history claim, "
    "rather than just stating a conclusion. Help debug code by pointing at what's wrong, not by rewriting "
    "the whole program. When a real source (Weather Labs, School Library, a dictionary, a country's data) "
    "already gave the exact fact, use that source's own value and cite it rather than restating it from "
    "memory -- the source supplies the fact, you help the child understand it."
)


def is_model_ready():
    """True if Citadel's shared Ollama is reachable and OLLAMA_MODEL is
    actually pulled there -- kept as a real live check (not just "is the
    env var set") since a fresh install's Ollama may not have any model
    yet, and the old bundled-model version had the same kind of check
    (MODEL_PATH.exists()) for the same reason: fail with a clear message
    instead of a confusing mid-stream error."""
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        r.raise_for_status()
        names = {m.get("name", "") for m in r.json().get("models", [])}
        return OLLAMA_MODEL in names or any(n.split(":")[0] == OLLAMA_MODEL.split(":")[0] for n in names)
    except requests.RequestException:
        return False


RECENT_CONTEXT_WINDOW_SECONDS = 900


def _recent_context_note():
    """Tutor as a real subscriber to the Cross-Subject Interactivity
    Engine's event log (see interactivity.py / CARD_REDESIGN_PLAN.md):
    if the child looked at something in the last 15 minutes, let Ollie
    know so it can connect what it's asked next to what they just saw,
    instead of the two living in separate silos. Silently skipped if
    nothing recent or nothing interesting is logged yet."""
    import time

    events = interactivity.get_recent_events(limit=3, event_type="content_viewed")
    now = time.time()
    recent = [e for e in events if now - e["ts"] < RECENT_CONTEXT_WINDOW_SECONDS]
    if not recent:
        return None
    names = [e["payload"].get("name") for e in recent if e["payload"].get("name")]
    if not names:
        return None
    return "The child was just looking at this in another part of Cloud9: " + ", ".join(names) + \
        ". Bring it up only if it's actually relevant to what they ask."


def _lab_context_note(lab_context):
    """Ollie Teaching Mode's real per-Lab context (ROADMAP.md Phase 1,
    item 3) -- when a Lab's own "Ask Ollie" widget is used, it sends what
    it's really showing right now, so Ollie can ground its answer in the
    exact value/source/time already on screen instead of guessing at
    what the child might be looking at. A plain, honest string built from
    whatever real fields the Lab actually sent -- never invents fields
    that weren't provided."""
    if not lab_context or not isinstance(lab_context, dict):
        return None
    lab = lab_context.get("lab")
    if not lab:
        return None
    parts = [f"The child is currently using Cloud9's {lab}."]
    activity = lab_context.get("activity")
    if activity:
        parts.append(f"Current activity: {activity}.")
    state = lab_context.get("state")
    if state:
        parts.append(f"Current real state: {state}.")
    parts.append("Ground your answer in this real context when it's relevant to what they ask.")
    return " ".join(parts)


def chat_stream(message, history=None, lab_context=None):
    """Same external contract as the old llama-cpp-python version --
    still a generator yielding plain text chunks -- so app.py's
    stream_with_context(ai.chat_stream(...)) call needed no changes."""
    history = history or []
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    lab_note = _lab_context_note(lab_context)
    if lab_note:
        messages.append({"role": "system", "content": lab_note})
    context_note = _recent_context_note()
    if context_note:
        messages.append({"role": "system", "content": context_note})
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": message})

    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": True,
            "options": {"temperature": 0.7, "num_predict": 300},
        },
        stream=True,
        timeout=120,
    )
    resp.raise_for_status()
    for line in resp.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        content = chunk.get("message", {}).get("content")
        if content:
            yield content
        if chunk.get("done"):
            break
