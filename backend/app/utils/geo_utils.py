import math
from typing import Dict, Any, List

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) in kilometers.
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def make_geojson_point(longitude: float, latitude: float) -> Dict[str, Any]:
    """Create a GeoJSON Point geometry dictionary."""
    return {
        "type": "Point",
        "coordinates": [longitude, latitude]
    }

def extract_coordinates(geojson: Dict[str, Any]) -> List[float]:
    """Extract coordinates from GeoJSON point in [lat, lon] format."""
    if not geojson or "coordinates" not in geojson:
        return [0.0, 0.0]
    coords = geojson["coordinates"]
    # GeoJSON is [lon, lat], return as [lat, lon] for maps
    if len(coords) >= 2:
        return [coords[1], coords[0]]
    return [0.0, 0.0]
