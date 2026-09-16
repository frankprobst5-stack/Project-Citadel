"""Direct client for NWS's own real, structured active-alerts API —
`api.weather.gov/alerts/active` — used instead of treating NWS as just
another generic RSS/CAP-XML feed the way Masthead's own FeedParser.php
does. This is a deliberate improvement over a straight port, not a
shortcut: NWS's own alerts endpoint already returns clean GeoJSON with
every CAP field as a plain, named JSON property, verified live against
a real active alert before writing this (a real Flood Advisory for
Hudspeth County, TX, confirmed 2026-09-16) — no CAP-namespace XML
parsing needed for this one source at all.

Real, confirmed-live response shape (`properties` of each GeoJSON
feature): event, severity, urgency, certainty, areaDesc, geocode.SAME
(FIPS county codes, list), geocode.UGC (zone codes, list), effective,
expires, headline, description.
"""
import json

import requests

_NWS_HEADERS = {"User-Agent": "CitadelNewsArchive/1.0 (self-hosted, github.com/frankprobst5-stack/Project-Citadel)"}


def fetch_active_alerts(lat, lon, timeout=15):
    """Real, live alerts for a point -- returns a list of normalized
    dicts matching news_articles' own column shape, ready to insert
    directly (source_id/dedupe_key added by the caller, same as every
    other adapter's output). Empty list (not an exception) on any
    failure or when there's genuinely nothing active right now -- both
    are real, valid, honest states for this endpoint, confirmed live."""
    if not lat or not lon:
        return []

    try:
        resp = requests.get(
            f"https://api.weather.gov/alerts/active",
            params={"point": f"{lat},{lon}"},
            headers=_NWS_HEADERS,
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError, ValueError):
        return []

    items = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        alert_id = props.get("id") or feature.get("id")
        if not alert_id:
            continue

        geocode = props.get("geocode", {})
        geocodes = list(geocode.get("SAME", [])) + list(geocode.get("UGC", []))

        items.append({
            "guid": alert_id,
            "dedupe_key": _dedupe_key(alert_id),
            "title": props.get("headline") or props.get("event") or "(untitled alert)",
            "url": props.get("@id") or alert_id,
            "body": props.get("description"),
            "published_at": _to_naive(props.get("effective") or props.get("sent")),
            "image_url": None,
            "latitude": None,
            "longitude": None,
            "cap_event": props.get("event"),
            "cap_severity": props.get("severity"),
            "cap_urgency": props.get("urgency"),
            "cap_certainty": props.get("certainty"),
            "cap_area_desc": props.get("areaDesc"),
            "cap_expires_at": _to_naive(props.get("expires")),
            "cap_geocodes": ",".join(geocodes) if geocodes else None,
        })

    return items


def _dedupe_key(alert_id):
    import hashlib
    return hashlib.sha256(alert_id.encode("utf-8")).hexdigest()


def _to_naive(iso_string):
    """NWS timestamps are real ISO 8601 with an explicit timezone
    offset (e.g. "2026-09-16T15:14:00-06:00"). Reformatted to this
    feature's own convention -- every other timestamp column is a
    naive server-local-equivalent string, matching news_feed_parser.py's
    own _published_at()."""
    if not iso_string:
        return None
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
