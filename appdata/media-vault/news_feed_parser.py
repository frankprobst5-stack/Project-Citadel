"""Generic RSS/Atom feed parsing for the News Archive & Local Log card
(ROADMAP.md DISCOVERY item) — a real Python port of Masthead's own
FeedParser.php (github.com/frankprobst5-stack/masthead, private,
archived-but-reusable), not a fresh implementation. Deliberately narrower
than the original: Masthead's own CAP-namespace extraction (reading
cap:event/severity/etc. directly out of NWS's raw feed XML) is NOT ported
here, because Citadel talks to NWS's own real, structured alerts JSON API
instead (see news_nws_alerts.py) — cleaner and more robust than re-parsing
CAP-XML by hand for that one source. What IS ported: the real,
independently-confirmed-live point-coordinate conventions (GeoRSS for
USGS, geo:lat/geo:long for NOAA's tsunami feeds) that non-NWS hazard
adapters (news_hazard_adapters.py) depend on, and the one real,
already-caught bug worth carrying over rather than rediscovering.

Every field name below was verified directly against real, live feeds
with Python's own `feedparser` library before writing this, not assumed
from the PHP source's own field names (which use a different library,
SimplePie, with a different shape):
  - USGS earthquake feed (real Atom): coordinates live in `entry.where`
    as GeoJSON `{"type": "Point", "coordinates": (lon, lat)}` — note the
    real GeoJSON (lon, lat) order, opposite of every other lat/lon pair
    in this codebase; confirmed against a real entry (106.8742, -4.9832
    for a real quake near Indonesia), not assumed.
  - NOAA tsunami feed (real Atom): coordinates are simpler, exposed
    directly as top-level `entry.geo_lat` / `entry.geo_long`.
  - Both feeds: `entry.id`, `entry.title`, `entry.summary`, and either
    `entry.published_parsed` or `entry.updated_parsed` (USGS's own feed
    only sets the latter — checked live, not assumed both exist).
"""
import hashlib
import html
from datetime import datetime, timezone

import feedparser


def _decode_link(link):
    """Real bug, caught live against BBC News's actual feed (documented
    in Masthead's own FeedParser.php): some feeds' raw XML has the query
    string double-entity-encoded, so the parsed link can still contain a
    literal "&amp;" instead of "&". A URL should never contain an HTML
    entity — decode defensively rather than storing (and later
    re-escaping into "&amp;amp;") a broken link."""
    if not link:
        return link
    return html.unescape(link)


def _dedupe_key(guid_or_link):
    """sha256 of the feed's own guid (falling back to the link when a
    feed doesn't set one) — same real approach as Masthead's own
    ArticleService, and the same reason: cheap, stable, and only ever
    needs to be unique per-source (see the real UNIQUE(source_id,
    dedupe_key) constraint), not globally."""
    return hashlib.sha256(guid_or_link.encode("utf-8")).hexdigest()


def _extract_coordinates(entry):
    """Two real, independently-confirmed-live point-coordinate
    conventions, checked in order — a source only ever uses one:
      - GeoRSS `where` (USGS earthquakes) — GeoJSON order, (lon, lat).
      - geo:lat / geo:long (NOAA tsunami feeds) — two separate fields,
        already in the expected (lat, lon) order.
    Returns (lat, lon) or (None, None)."""
    where = entry.get("where")
    if isinstance(where, dict) and where.get("type") == "Point":
        coords = where.get("coordinates")
        if coords and len(coords) == 2:
            lon, lat = coords
            return float(lat), float(lon)

    geo_lat = entry.get("geo_lat")
    geo_long = entry.get("geo_long")
    if geo_lat is not None and geo_long is not None:
        try:
            return float(geo_lat), float(geo_long)
        except (TypeError, ValueError):
            pass

    return None, None


def _extract_image(entry):
    """Real fallback chain, narrower than Masthead's own (which also
    handles podcast/video enclosures — out of scope here, this card
    archives text summaries, not media): a media:thumbnail or an
    image-typed enclosure, whichever the feed actually provides."""
    media_thumb = entry.get("media_thumbnail")
    if media_thumb and isinstance(media_thumb, list):
        url = media_thumb[0].get("url")
        if url:
            return url

    for link in entry.get("links", []):
        if link.get("rel") == "enclosure" and str(link.get("type", "")).startswith("image/"):
            return link.get("href")

    return None


def _best_link(entry):
    """Most feeds' own `entry.link` is a real, clickable HTTP URL — but
    NOAA's tsunami feeds set it to a bare `urn:uuid:...` instead (real,
    confirmed live) and put the actual readable bulletin under `links`
    as `rel: "alternate"`. Prefer a real http(s) link over a urn: one."""
    link = entry.get("link", "")
    if link.startswith("http"):
        return _decode_link(link)

    for l in entry.get("links", []):
        href = l.get("href", "")
        if l.get("rel") == "alternate" and href.startswith("http"):
            return _decode_link(href)

    return _decode_link(link) or None


def _published_at(entry):
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return datetime(*parsed[:6], tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def fetch_feed(feed_url, timeout=15):
    """Fetches and normalizes one feed's items into the plain shape the
    rest of this module consumes — the same real job Masthead's own
    FeedParser::fetch() does, minus the CAP-XML extraction (see this
    module's own docstring for why).

    Returns a list of dicts: guid, title, url, body, published_at,
    image_url, latitude, longitude. Raises no exception on a feed-level
    failure (a malformed/unreachable feed) -- `feedparser` itself never
    raises for that, it sets `bozo` and returns whatever it could parse
    (often nothing); callers should check for an empty return and log
    accordingly rather than expect a raised error, matching feedparser's
    own real behavior confirmed above, not assumed.
    """
    parsed = feedparser.parse(feed_url, request_headers={"User-Agent": "CitadelNewsArchive/1.0"})

    items = []
    for entry in parsed.entries:
        link = _best_link(entry)
        if not link:
            continue

        guid = entry.get("id") or link
        lat, lon = _extract_coordinates(entry)

        items.append({
            "guid": guid,
            "dedupe_key": _dedupe_key(guid),
            "title": (entry.get("title") or "(untitled)").strip(),
            "url": link,
            "body": entry.get("summary"),
            "published_at": _published_at(entry),
            "image_url": _extract_image(entry),
            "latitude": lat,
            "longitude": lon,
        })

    return items
