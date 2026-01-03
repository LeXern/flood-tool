from flood_tool.algorithms.kdtree import KDTree
from flood_tool.utils import project_to_meters
import math

def perform_analysis(buildings, water_nodes, water_threshold_dist=200, hotspot_radius=300, hotspot_min_neighbors=5):
    """
    Identify vulnerable buildings and hotspots using local projection for accurate distance.
    
    Parameters:
    - water_threshold_dist: Distance (m) to consider a building vulnerable. 
      (Chosen as 200m to approximate a severe flood plain buffer).
    - hotspot_radius: Radius (m) to count neighbors for density.
      (Chosen as 300m to represent a typical neighborhood/city block scale).
    - hotspot_min_neighbors: Min count to classify as a hotspot cluster.
    """
    # Defensive Programming: Validate inputs (as per Unit 1 Lecture)
    assert water_threshold_dist > 0, "Threshold distance must be positive"
    assert hotspot_radius > 0, "Hotspot radius must be positive"
    assert hotspot_min_neighbors >= 1, "Must require at least 1 neighbor"
    
    # 1. Determine Reference Point (average lat/lon)
    if not buildings:
        print("Warning: No buildings provided for analysis.")
        return [], []
        
    avg_lat = sum(b['lat'] for b in buildings) / len(buildings)
    avg_lon = sum(b['lon'] for b in buildings) / len(buildings)
    
    print(f"Projecting data relative to Ref: ({avg_lat:.4f}, {avg_lon:.4f})...")

    # 2. Project Water Nodes
    # Points structure: (x, y, data)
    water_points = []
    for w in water_nodes:
        x, y = project_to_meters(w['lat'], w['lon'], avg_lat, avg_lon)
        water_points.append((x, y, w))
        
    print("Building Water KD-Tree...")
    water_tree = KDTree(water_points)
    
    # 3. Assess Vulnerability
    print(f"Assessing vulnerability for {len(buildings)} buildings...")
    vulnerable_buildings = []
    
    # We also project buildings to query
    building_projections = [] # store (x, y, original_b)
    
    for b in buildings:
        x, y = project_to_meters(b['lat'], b['lon'], avg_lat, avg_lon)
        # Check nearby water
        # query_radius uses Euclidean distance by default, which logic matches our projection (meters)
        nearby_water = water_tree.points_within_radius_count((x, y), water_threshold_dist)
        
        if nearby_water > 0:
            vulnerable_buildings.append(b)
            building_projections.append((x, y, b))
            
    print(f"Found {len(vulnerable_buildings)} vulnerable buildings.")
    
    # 4. Hotspot Analysis
    print("Analyzing hotspots...")
    if not vulnerable_buildings:
        return [], []

    vuln_tree = KDTree(building_projections)
    
    hotspots = []
    
    for x, y, b in building_projections:
        # Count neighbors within hotspot_radius
        # Note: this counts itself. Substract 1 if needed, or adjust threshold.
        # "Density" usually is count per area or just count.
        count = vuln_tree.points_within_radius_count((x, y), hotspot_radius)
        
        # We accept count including self, or we can look for *neighbors* (count-1)
        if count >= hotspot_min_neighbors:
            hotspots.append({
                'lat': b['lat'],
                'lon': b['lon'],
                'density': count,
                'building_id': b['id']
            })
            
    # Sort hotspots by density
    hotspots.sort(key=lambda x: x['density'], reverse=True)
    
    return vulnerable_buildings, hotspots
