from flood_tool.data_loader import fetch_osm_data
from flood_tool.analysis import perform_analysis

def run_case(name, bbox):
    print(f"\n{'='*50}")
    print(f"Running Analysis for: {name}")
    print(f"BBox: {bbox}")
    print(f"{'='*50}")

    # 1. Fetch Data
    print("Fetching Water Nodes...")
    water_nodes = fetch_osm_data(bbox, query_type="water")
    print(f"Fetched {len(water_nodes)} water nodes.")

    print("Fetching Buildings...")
    buildings = fetch_osm_data(bbox, query_type="building")
    print(f"Fetched {len(buildings)} buildings.")
    
    if not water_nodes or not buildings:
        print("Insufficient data to proceed.")
        return

    # 2. Analyze
    vulnerable, hotspots = perform_analysis(buildings, water_nodes)
    
    print(f"\n--- Results for {name} ---")
    print(f"Vulnerable Buildings: {len(vulnerable)} / {len(buildings)}")
    print(f"Hotspots Detected: {len(hotspots)}")
    
    if hotspots:
        print("Top 5 Hotspots (by neighborhood density):")
        for i, h in enumerate(hotspots[:5]):
            print(f"  {i+1}. Lat: {h['lat']:.5f}, Lon: {h['lon']:.5f} | Density: {h['density']} vulnerable neighbors")

if __name__ == "__main__":
    # Venice (approx center)
    venice_bbox = (45.4300, 12.3100, 45.4450, 12.3400)
    
    run_case("Venice", venice_bbox)
