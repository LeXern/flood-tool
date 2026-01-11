"""
Flood Vulnerability Analysis CLI

Usage:
    python flood_tool/cli.py "City Name" min_lat min_lon max_lat max_lon

Example (Amsterdam):
    python flood_tool/cli.py "Amsterdam" 52.36 4.88 52.38 4.92

Note: Specify the city name and the bounding box (min_lat, min_lon, max_lat, max_lon) for the analysis.
"""

import sys
import os
import argparse

# Add parent directory to path so we can import flood_tool when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flood_tool.data_loader import fetch_osm_data
from flood_tool.analysis import perform_analysis
from flood_tool.visualization import create_all_visualizations

def run_analysis(city_name, bbox, water_threshold=50, hotspot_radius=100, min_neighbors=10):
    """Run flood vulnerability analysis for any city."""
    print(f"\n{'='*70}")
    print(f"ANALYZING: {city_name}")
    print(f"Bounding Box: {bbox}")
    print(f"Parameters: threshold={water_threshold}m, radius={hotspot_radius}m, min_neighbors={min_neighbors}")
    print(f"{'='*70}")

    # 1. Fetch Data
    print("\n[1/4] Fetching water data...")
    water_nodes = fetch_osm_data(bbox, query_type="water")
    print(f"      Fetched {len(water_nodes)} water nodes")

    print("\n[2/4] Fetching building data...")
    buildings = fetch_osm_data(bbox, query_type="building")
    print(f"      Fetched {len(buildings)} buildings")
    
    if not water_nodes or not buildings:
        print("\n      [ERROR] Insufficient data")
        return None, None, None, None

    # 2. Analyze
    print("\n[3/4] Running vulnerability analysis...")
    vulnerable, hotspots = perform_analysis(
        buildings, water_nodes,
        water_threshold_dist=water_threshold,
        hotspot_radius=hotspot_radius,
        hotspot_min_neighbors=min_neighbors
    )
    
    print(f"\nRESULTS:")
    print(f"  Total: {len(buildings)} buildings")
    print(f"  Vulnerable: {len(vulnerable)} ({len(vulnerable)/len(buildings)*100:.1f}%)")
    print(f"  Hotspots: {len(hotspots)}")
    
    if hotspots:
        print("\nTop 5 Hotspots (by neighborhood density):")
        for i, h in enumerate(hotspots[:5]):
            print(f"  {i+1}. Lat: {h['lat']:.5f}, Lon: {h['lon']:.5f} | Density: {h['density']}")

    # 3. Create Visualizations
    print("\n[4/4] Creating visualizations...")
    create_all_visualizations(buildings, water_nodes, vulnerable, hotspots, 
                             city_name=city_name, output_dir="outputs")
    
    return buildings, water_nodes, vulnerable, hotspots

def main():
    parser = argparse.ArgumentParser(description="Flood Vulnerability Analysis Tool")
    parser.add_argument("city", help="City name")
    parser.add_argument("min_lat", type=float, help="Min latitude")
    parser.add_argument("min_lon", type=float, help="Min longitude")
    parser.add_argument("max_lat", type=float, help="Max latitude")
    parser.add_argument("max_lon", type=float, help="Max longitude")
    parser.add_argument("--threshold", type=int, default=50, help="Water proximity threshold (m)")
    parser.add_argument("--radius", type=int, default=100, help="Hotspot radius (m)")
    parser.add_argument("--min-neighbors", type=int, default=10, help="Min neighbors for hotspot")
    
    args = parser.parse_args()
    
    print("="*70)
    print("FLOOD VULNERABILITY VISUALIZATION SYSTEM")
    print("="*70)
    print("\nThis system analyzes flood vulnerability and creates 4 views:")
    print("  1. Dot Map - Individual building detail")
    print("  2. Heatmap - Vulnerability density")
    print("  3. Choropleth - Zone-level aggregation")
    print("  4. Dashboard - Statistics and rankings")
    print("="*70)
    
    bbox = (args.min_lat, args.min_lon, args.max_lat, args.max_lon)
    
    run_analysis(
        args.city, bbox,
        water_threshold=args.threshold,
        hotspot_radius=args.radius,
        min_neighbors=args.min_neighbors
    )
    
    city_slug = args.city.lower().replace(' ', '_')
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print(f"\nGenerated files in 'outputs/' directory:")
    print(f"  - {city_slug}_dot_map.html")
    print(f"  - {city_slug}_heatmap.html")
    print(f"  - {city_slug}_choropleth.html")
    print(f"  - {city_slug}_dashboard.html")
    print("\n" + "="*70)
    print("Open HTML files in your browser to view results")
    print("="*70)

if __name__ == "__main__":
    main()
