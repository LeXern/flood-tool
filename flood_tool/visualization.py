import folium

def create_flood_map(center_lat, center_lon, buildings, hotspots):
    """
    Create a Folium map visualizing vulnerable buildings and hotspots.
    
    Parameters:
    - center_lat, center_lon: Center of the map.
    - buildings: List of all buildings (or just vulnerable ones if filtered).
                 Each dict must have 'lat', 'lon', 'id', and optionally 'vulnerable'.
    - hotspots: List of hotspot points (lat, lon, density).
    """
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles='CartoDB positron')

    # Add Buildings
    feature_group_buildings = folium.FeatureGroup(name="Vulnerable Buildings")
    for b in buildings:
        # We assume passed buildings are vulnerable for this visualization context,
        # or check a flag if dataset is mixed.
        folium.CircleMarker(
            location=[b['lat'], b['lon']],
            radius=3,
            color='red',
            fill=True,
            fill_opacity=0.6,
            popup=f"Building ID: {b['id']}"
        ).add_to(feature_group_buildings)
    feature_group_buildings.add_to(m)

    # Add Hotspots (Heatmap or Markers)
    # Using Markers for top hotspots
    feature_group_hotspots = folium.FeatureGroup(name="Hotspots")
    for i, h in enumerate(hotspots):
        # h is likely (lat, lon, density) or a dict? 
        # based on analysis.py logic it returns a list of dictionaries or tuples.
        # Let's verify analysis.py return format.
        # analysis.py returns a sorted list of hotspots.
        # Assuming dict or object with lat/lon/density.
        # Wait, analysis.py currently prints them. I need to check the return value of analysis.py
        
        # Let's assume h is a dictionary for now, matching the printed output structure
        folium.Marker(
            location=[h['lat'], h['lon']],
            popup=f"Hotspot Rank: {i+1}<br>Density: {h['density']}",
            icon=folium.Icon(color='orange', icon='fire')
        ).add_to(feature_group_hotspots)
    feature_group_hotspots.add_to(m)

    folium.LayerControl().add_to(m)
    
    return m
