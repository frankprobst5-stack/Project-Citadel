"""Off-Grid AI (Ollama) assisted briefing for the Global Situation Monitor
(added 2026-10-08, Frank's own request). Server-to-server only, same
reasoning as the Mealie pantry-check bridge in app.py -- the browser
never talks to Ollama directly for this feature.

Deliberately narrow scope: the model is asked to SUMMARIZE and ORGANIZE
headlines already matched by situation_matcher.py -- never to invent
facts, estimate a probability of war, or suggest a status. The household
sets the status by hand (see api_set_situation_status in app.py); this
is reference material for that judgment, not a replacement for it. A
small local model (llama3.2:1b, what's actually pulled on this
install -- see appdata/ollama) is not a credible geopolitical analyst,
and the prompt is written to keep it inside a job it can actually do:
plain organization and pattern-spotting on a short, already-curated list
of real headlines, not open-ended reasoning.
"""
import os
import requests

OLLAMA_HOST = os.environ.get("OLLAMA_REMOTE_HOST", "citadel-ollama")
OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:11434"
OLLAMA_MODEL = os.environ.get("SITUATION_AI_MODEL", "llama3.2:1b")

# Suggesting watch-list candidates from a 40-headline batch is a harder
# task (relevance classification + structured extraction) than
# summarizing an already-filtered handful of matched headlines --
# confirmed live 2026-10-08: llama3.2:1b ignored the output format
# entirely and flagged irrelevant stories (a Premier League result, a
# Mars mission) as "escalation." llama3.2:3b (also pulled on this
# install) filtered correctly for relevance but still dropped a field
# about half the time -- see parse_suggestions' tolerance for that.
# Worth the extra ~2x inference cost since this call is on-demand, not
# scheduled.
SUGGEST_MODEL = os.environ.get("SITUATION_SUGGEST_MODEL", "llama3.2:3b")

SYSTEM_PROMPT = (
    "You are a neutral assistant organizing real open-source news headlines for a "
    "household's own situational awareness. Rules you must follow:\n"
    "1. Only summarize and organize the headlines you are given. Never invent facts, "
    "dates, figures, or events not present in them.\n"
    "2. Never state or imply a probability of war, and never declare or suggest any "
    "escalation status (normal/elevated/etc) -- that judgment belongs to the household "
    "reading your summary, not you.\n"
    "3. Explicitly note where multiple different sources reported related events "
    "(corroboration) versus where only one source did.\n"
    "4. Keep the tone calm, factual, and non-alarmist -- no dramatic language.\n"
    "5. If the headlines given are too sparse or unrelated to say anything meaningful, "
    "say so plainly instead of inventing analysis."
)


def build_prompt(events_by_theater, theater_labels):
    """events_by_theater: {theater_key: [event dicts with title/source_name/
    published_at/indicators]}. Builds the plain-text user prompt listing
    every matched headline, grouped by theater, for the model to organize --
    the model sees nothing it wasn't already shown in the dashboard's own
    timeline."""
    lines = [
        "Below are recent news headlines that matched a fixed escalation watch-list, "
        "grouped by theater. Write a short (150-250 word) situational summary "
        "organized by theater, noting any patterns or corroboration across sources. "
        "Do not add commentary about probability of war or recommendations.\n"
    ]
    for theater, events in events_by_theater.items():
        if not events:
            continue
        lines.append(f"\n## {theater_labels.get(theater, theater)}")
        for ev in events:
            indicator_labels = ", ".join(i["label"] for i in ev.get("indicators", []))
            lines.append(f"- [{ev.get('source_name', 'unknown source')}] {ev['title']} "
                         f"(matched: {indicator_labels})")
    return "\n".join(lines)


VALID_THEATERS = {"europe_nato_russia", "indo_pacific_taiwan", "middle_east", "cross_theater", "cbrn_biosecurity"}
VALID_TIERS = {"red", "orange", "green"}

SUGGEST_SYSTEM_PROMPT = (
    "You find headlines related to major-power military/diplomatic/biosecurity escalation. "
    "You will see a numbered headline list. Copy this exact answer format, one line per "
    "relevant headline, nothing else:\n\n"
    "3|middle_east|orange|iran strikes ruled out|Trump rules out US strikes on Iran\n\n"
    "Only copy the number, theater, tier, a short keyword phrase, and a label -- separated by "
    "the | character. Valid theater words: europe_nato_russia, indo_pacific_taiwan, "
    "middle_east, cross_theater, cbrn_biosecurity. Valid tier words: red, orange, green. Skip "
    "headlines about sports, entertainment, weather, celebrities, or ordinary domestic/local "
    "news -- only military/diplomatic/biosecurity escalation between major powers or states "
    "matters. If nothing qualifies, write nothing."
)


def build_suggest_prompt(unmatched_events):
    """unmatched_events: list of dicts with at least 'title'. Returns the
    plain-text numbered headline list the model is asked to review."""
    lines = ["Headlines:"]
    for i, ev in enumerate(unmatched_events, start=1):
        lines.append(f"{i}. {ev['title']}")
    return "\n".join(lines)


def parse_suggestions(response_text, unmatched_events):
    """Defensively parses the model's pipe-delimited response -- any line
    that doesn't cleanly fit the expected shape or references invalid
    enum values is silently skipped, not treated as an error. A small
    local model will not follow the format perfectly every time; this
    keeps one malformed line from losing every valid one alongside it.
    Capped at 10 suggestions per run regardless of how many the model
    tries to produce."""
    suggestions = []
    for line in (response_text or "").strip().splitlines():
        parts = [p.strip() for p in line.split("|")]
        # Tolerate the common near-miss (confirmed live 2026-10-08 against
        # llama3.2:3b): 4 fields with the trailing label dropped. The
        # keyword phrase doubles as the label in that case rather than
        # discarding an otherwise-valid suggestion -- a human still
        # reviews and can reject it, so a slightly generic label here
        # costs nothing.
        if len(parts) == 4:
            parts.append(parts[3])
        if len(parts) != 5:
            continue
        n_str, theater, tier, keyword, label = parts
        try:
            n = int(n_str) - 1
        except ValueError:
            continue
        if not (0 <= n < len(unmatched_events)):
            continue
        if theater not in VALID_THEATERS or tier not in VALID_TIERS:
            continue
        keyword = keyword.lower().strip()
        label = label.strip()
        if not keyword or not label:
            continue

        # Real guardrail, added after a live hallucination (2026-10-08):
        # the model tagged a vaccine-injury-policy headline as
        # "indo_pacific_taiwan|red|US plans for Taiwan not specified" --
        # a word-for-word fabrication with zero connection to the actual
        # cited headline. Cheap, deterministic check: at least one
        # meaningful word (4+ letters, so "iran"/"china"/"nato" count but
        # "us"/"the" don't) from the suggested keyword must actually
        # appear in the source headline it claims to come from. This
        # catches outright invented content before it even reaches human
        # review -- it does NOT replace that review (the surviving
        # suggestion above it was imprecise but not fabricated, and still
        # needs a human to actually approve it).
        source_title_lower = unmatched_events[n]["title"].lower()
        keyword_words = [w for w in keyword.replace("-", " ").split() if len(w) >= 4]
        if keyword_words and not any(w in source_title_lower for w in keyword_words):
            continue

        suggestions.append({
            "theater": theater,
            "tier": tier,
            "keyword": keyword,
            "label": label,
            "source_title": unmatched_events[n]["title"],
            "source_url": unmatched_events[n].get("url"),
        })
        if len(suggestions) >= 10:
            break
    return suggestions


def _generate(system, prompt, model=None, temperature=None, timeout=120):
    """Calls Ollama's /api/generate server-to-server. Returns the response
    text. Raises requests.RequestException on failure -- caller is
    expected to handle that the same honest way every other external-
    service call in this file does (see api_situation_briefing_generate
    and api_situation_suggest_keywords), not swallow it into a
    fabricated success."""
    payload = {
        "model": model or OLLAMA_MODEL,
        "system": system,
        "prompt": prompt,
        "stream": False,
    }
    if temperature is not None:
        payload["options"] = {"temperature": temperature}
    res = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=timeout)
    res.raise_for_status()
    return res.json().get("response", "").strip()


def generate_briefing(prompt, timeout=120):
    return _generate(SYSTEM_PROMPT, prompt, model=OLLAMA_MODEL, timeout=timeout)


def generate_suggestions_raw(prompt, timeout=150):
    # Low temperature (default ~0.8 otherwise), added after confirming
    # live 2026-10-08 that this task's run-to-run output varied wildly on
    # the identical prompt -- one run correctly filtered 38/40 irrelevant
    # headlines, the very next run flagged NHS reviews, a Premier League
    # joke, and a Fort Bragg housing renovation as "orange-tier
    # escalation." A classification/filtering task wants the model's
    # most likely answer, not creative sampling -- temperature 0.1 pushes
    # toward that without being fully greedy (0.0).
    return _generate(SUGGEST_SYSTEM_PROMPT, prompt, model=SUGGEST_MODEL, temperature=0.1, timeout=timeout)
