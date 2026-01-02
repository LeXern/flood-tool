import pytest
from flood_tool.analysis import perform_analysis

def test_perform_analysis_vulnerability():
    # Mock data: 1 vulnerable building, 1 safe building
    # Water at (0,0)
    # Building A at (0, 0.0001) -> approx 11m (Very Close)
    # Building B at (0, 0.1) -> approx 11km (Far)
    
    water_nodes = [{'lat': 0.0, 'lon': 0.0, 'id': 1, 'type': 'water'}]
    buildings = [
        {'lat': 0.0, 'lon': 0.0001, 'id': 101, 'type': 'building'},
        {'lat': 0.0, 'lon': 0.1, 'id': 102, 'type': 'building'}
    ]
    
    vulnerable, hotspots = perform_analysis(buildings, water_nodes, water_threshold_dist=100)
    
    assert len(vulnerable) == 1
    assert vulnerable[0]['id'] == 101

def test_perform_analysis_hotspots():
    # Cluster of 5 vulnerable buildings near each other
    # We define them close enough to be neighbors
    # Using small lat/lon diffs. 
    # At equator 0.00001 deg is ~1m.
    
    buildings = []
    for i in range(5):
        # All within 1-5 meters of each other
        buildings.append({'lat': 0.0, 'lon': 0.00001 * i, 'id': i})
        
    water = [{'lat': 0.0, 'lon': 0.0}] # All are near water (0 distance)
    
    # Check hotspot
    # min neighbors=5. Since there are 5 and they are all close, expected density=5
    vulnerable, hotspots = perform_analysis(buildings, water, water_threshold_dist=100, hotspot_radius=50, hotspot_min_neighbors=5)
    
    assert len(vulnerable) == 5
    assert len(hotspots) == 5 # All 5 buildings are hotspots (neighborhood size 5)
    assert hotspots[0]['density'] == 5

def test_perform_analysis_no_water():
    buildings = [{'lat': 10, 'lon': 10, 'id': 1}]
    water = [] # No water
    
    vulnerable, hotspots = perform_analysis(buildings, water)
    assert len(vulnerable) == 0
    assert len(hotspots) == 0
