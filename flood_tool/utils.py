import math

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000 # Radius of earth in meters. Use 6371 for km
    return c * r

def euklidian_dist(p1, p2):
    """
    Euclidean distance for projected coordinates (if we were using them).
    For lat/lon small distances, haversine is better, but KDTrees often work on Euclidean space.
    If we project points to a local CRS, we can use this.
    For this assignment, we might keep it simple or stick to Lat/Lon with Haversine, 
    but KDTree standard implementation assumes Euclidean space usually.
    We'll stick to 2D Euclidean for the Tree for simplicity if we project, 
    or just use the tuple difference if the scale is small enough to approximate.
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def project_to_meters(lat, lon, ref_lat, ref_lon):
    """
    Project lat/lon to x,y in meters using a flat-earth approximation
    relative to a reference point.
    """
    rad_lat = math.radians(ref_lat)
    y = (lat - ref_lat) * 111320.0
    x = (lon - ref_lon) * 111320.0 * math.cos(rad_lat)
    return x, y
