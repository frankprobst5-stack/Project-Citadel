""""Continue Where You Left Off" -- a real feature built on the Cross-
Subject Interactivity Engine's existing event log (`interactivity.py`),
not a new tracking system. Earth Lab and Weather Labs already log a
real `content_viewed` event every time a child views something; this
just reads the most recent one back and points the child at where to
pick up again.
"""

import interactivity

# content_id prefix -> (icon, area/page link, label builder)
_SOURCES = {
    "weather:": {
        "icon": "⛈️",
        "href": "/weather-labs",
        "label": lambda payload: "Weather Labs — " + (payload.get("name") or "Current Conditions"),
    },
    "country:": {
        "icon": "\U0001F30D",
        "href": "/earth-lab",
        "label": lambda payload: "Earth Lab — " + (payload.get("name") or "a country you looked up"),
    },
    "history:": {
        "icon": "\U0001F4DC",
        "href": "/?open=history",
        "label": lambda payload: "This Day in History",
    },
}


def get_continue_card():
    """The single most recent real `content_viewed` event, shaped into a
    clickable card -- or None if nothing's been viewed yet (an honest
    empty state, not a fake placeholder)."""
    events = interactivity.get_recent_events(limit=1, event_type="content_viewed")
    if not events:
        return None

    event = events[0]
    content_id = event["content_id"]
    for prefix, source in _SOURCES.items():
        if content_id.startswith(prefix):
            return {
                "icon": source["icon"],
                "href": source["href"],
                "label": source["label"](event["payload"]),
                "ts": event["ts"],
            }
    return None
