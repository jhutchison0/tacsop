"""Geographic utilities: haversine distance and bearing (stdlib math, no numpy)."""

import math

EARTH_RADIUS_KM: float = 6371.0


def get_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the initial bearing between two points.

    Args:
        lat1: Latitude of point 1 in degrees.
        lon1: Longitude of point 1 in degrees.
        lat2: Latitude of point 2 in degrees.
        lon2: Longitude of point 2 in degrees.

    Returns:
        Bearing in degrees (0-360).

    Reference:
        https://www.movable-type.co.uk/scripts/latlong.html
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dlam = math.radians(lon2) - math.radians(lon1)

    y = math.sin(dlam) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - (
        math.sin(phi1) * math.cos(phi2) * math.cos(dlam)
    )
    theta_rad = math.atan2(y, x)
    return (math.degrees(theta_rad) + 360) % 360


def get_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the haversine distance between two points.

    Args:
        lat1: Latitude of point 1 in degrees.
        lon1: Longitude of point 1 in degrees.
        lat2: Latitude of point 2 in degrees.
        lon2: Longitude of point 2 in degrees.

    Returns:
        Distance in kilometers.
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = phi2 - phi1
    dlam = math.radians(lon2) - math.radians(lon1)

    a = math.sin(dphi / 2) ** 2 + (
        math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c
