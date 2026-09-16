"""Real Python port of Masthead's own HazardLocationMatcher.php — decides
"is this article relevant to this household's location," the same three
real mechanisms, not a simpler reinvention: NWS alerts scope by FIPS
county code or UGC zone code (exact containment, no distance math),
point hazards (earthquakes, tsunamis) carry a real coordinate and need a
radius, and hazards with no location data at all (volcano, general news)
are always relevant regardless of where the household is.

Difference from Masthead's own version, deliberate: Masthead matches
against a per-*member*'s location (a multi-user product); Citadel has
exactly one real location — the station's own STATION_LAT/STATION_LON —
so this takes that station location directly rather than a per-user row.
"""
import math

_DEFAULT_RADIUS_MILES = 200.0
_EARTH_RADIUS_MILES = 3958.8


def _haversine_miles(lat1, lon1, lat2, lon2):
    """Real great-circle distance, standard haversine formula — same
    real math Masthead's own LocationService::distanceMiles() uses."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return _EARTH_RADIUS_MILES * 2 * math.asin(math.sqrt(a))


def is_relevant_to_station(article, station_lat, station_lon, county_fips, nws_zone_ugc,
                            radius_miles=_DEFAULT_RADIUS_MILES):
    """article: a dict with the same shape as a news_articles row
    (cap_geocodes, latitude, longitude). Returns True/False.

    No station location set at all -> everything is relevant, same as
    Masthead's own "a member with no ZIP saved sees everything
    unfiltered" default — this is a real fallback, not an error state.
    """
    if station_lat is None or station_lon is None:
        return True

    geocodes = article.get("cap_geocodes")
    if geocodes:
        values = [v.strip() for v in geocodes.split(",")]
        return (county_fips is not None and county_fips in values) or \
               (nws_zone_ugc is not None and nws_zone_ugc in values)

    lat, lon = article.get("latitude"), article.get("longitude")
    if lat is not None and lon is not None:
        return _haversine_miles(station_lat, station_lon, lat, lon) <= radius_miles

    # No location data on this article at all (volcano, general news) --
    # always relevant, nothing to scope.
    return True
