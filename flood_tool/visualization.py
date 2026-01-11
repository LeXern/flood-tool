# Flood vulnerability visualizations using Plotly

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Tuple
from collections import defaultdict
import os

def classify_building(water_count: int, is_hotspot: bool) -> Tuple[str, str]:
    """Classify building vulnerability"""
    if is_hotspot:
        return ("Hotspot", "#DC143C")
    elif water_count >= 1:
        return ("Vulnerable", "#FF8C00")
    else:
        return ("Safe", "#32CD32")

def create_dot_map(buildings, water_nodes, vulnerable, hotspots, output_file="dot_map.html"):
    """Building-level vulnerability map"""
    fig = go.Figure()
    
    # Get center
    avg_lat = sum(b['lat'] for b in buildings) / len(buildings)
    avg_lon = sum(b['lon'] for b in buildings) / len(buildings)
    
    # Add water sources
    fig.add_trace(go.Scattermapbox(
        lat=[w['lat'] for w in water_nodes],
        lon=[w['lon'] for w in water_nodes],
        mode='markers',
        marker=dict(size=5, color='blue'),
        name='Water Sources',
        hovertemplate='<b>Water Source</b><extra></extra>'
    ))
    
    # Classify all buildings
    vulnerable_ids = {v['id'] for v in vulnerable}
    hotspot_ids = {h['building_id'] for h in hotspots}
    
    classified = {"Hotspot": [], "Vulnerable": [], "Safe": []}
    
    for b in buildings:
        is_hotspot = b['id'] in hotspot_ids
        water_count = 1 if b['id'] in vulnerable_ids else 0
        category, _ = classify_building(water_count, is_hotspot)
        classified[category].append(b)
    
    # Add building layers
    categories = [
        ("Safe", "#32CD32", 5),
        ("Vulnerable", "#FF8C00", 7),
        ("Hotspot", "#DC143C", 8)
    ]
    
    for cat_name, color, size in categories:
        if classified[cat_name]:
            fig.add_trace(go.Scattermapbox(
                lat=[b['lat'] for b in classified[cat_name]],
                lon=[b['lon'] for b in classified[cat_name]],
                mode='markers',
                marker=dict(size=size, color=color),
                name=cat_name,
                hovertemplate=f'<b>{cat_name}</b><extra></extra>'
            ))
    
    fig.update_layout(
        title="Building Vulnerability Map",
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=avg_lat, lon=avg_lon),
            zoom=13
        ),
        height=800,
        showlegend=True
    )
    
    fig.write_html(output_file)
    print(f"[OK] Dot map saved: {output_file}")
    
    return {
        'total': len(buildings),
        'hotspot': len(classified['Hotspot']),
        'vulnerable': len(classified['Vulnerable']),
        'safe': len(classified['Safe'])
    }

def create_heatmap(buildings, water_nodes, vulnerable, hotspots, output_file="heatmap.html"):
    """Vulnerability density heatmap"""
    fig = go.Figure()
    
    avg_lat = sum(b['lat'] for b in buildings) / len(buildings)
    avg_lon = sum(b['lon'] for b in buildings) / len(buildings)
    
    # Add density layer
    if vulnerable:
        fig.add_trace(go.Densitymapbox(
            lat=[v['lat'] for v in vulnerable],
            lon=[v['lon'] for v in vulnerable],
            z=[1] * len(vulnerable),
            radius=15,
            colorscale=[
                [0, 'rgba(0,255,0,0)'],
                [0.3, 'rgba(255,255,0,0.5)'],
                [0.6, 'rgba(255,165,0,0.7)'],
                [1, 'rgba(220,20,60,0.9)']
            ],
            showscale=True,
            colorbar=dict(title="Vulnerability<br>Density", thickness=15, len=0.7),
            hovertemplate='Density: %{z}<extra></extra>',
            name='Vulnerability Density'
        ))
    
    # Add hotspot markers
    if hotspots:
        fig.add_trace(go.Scattermapbox(
            lat=[h['lat'] for h in hotspots],
            lon=[h['lon'] for h in hotspots],
            mode='markers',
            marker=dict(size=10, color='red', opacity=0.8),
            name='Hotspot Centers',
            hovertemplate='<b>Hotspot</b><br>Density: %{text}<extra></extra>',
            text=[h['density'] for h in hotspots]
        ))
    
    fig.update_layout(
        title="Vulnerability Density Heatmap",
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=avg_lat, lon=avg_lon),
            zoom=13
        ),
        height=800,
        showlegend=True
    )
    
    fig.write_html(output_file)
    print(f"[OK] Heatmap saved: {output_file}")

def create_choropleth_zones(buildings, water_nodes, vulnerable, hotspots, grid_size=0.005, output_file="choropleth.html"):
    """Zone-level vulnerability aggregation"""
    vulnerable_ids = {v['id'] for v in vulnerable}
    hotspot_ids = {h['building_id'] for h in hotspots}
    
    # Create grid zones
    lats = [b['lat'] for b in buildings]
    lons = [b['lon'] for b in buildings]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    zones: Dict[str, Dict] = defaultdict(lambda: {'buildings': [], 'vulnerable': 0, 'hotspots': 0})
    
    for b in buildings:
        grid_lat = int((b['lat'] - min_lat) / grid_size)
        grid_lon = int((b['lon'] - min_lon) / grid_size)
        zone_key = f"{grid_lat}_{grid_lon}"
        
        zone = zones[zone_key]
        zone['buildings'].append(b)
        if b['id'] in vulnerable_ids:
            zone['vulnerable'] += 1
        if b['id'] in hotspot_ids:
            zone['hotspots'] += 1
    
    # Build map
    fig = go.Figure()
    
    zone_stats = []
    for zone_key, zone in zones.items():
        total = len(zone['buildings'])
        vuln_pct = (zone['vulnerable'] / total * 100) if total > 0 else 0
        
        grid_lat, grid_lon = map(int, zone_key.split('_'))
        center_lat = min_lat + (grid_lat + 0.5) * grid_size
        center_lon = min_lon + (grid_lon + 0.5) * grid_size
        
        # Color by vulnerability %
        if vuln_pct >= 75:
            color, level = 'rgba(220,20,60,0.6)', 'Critical'
        elif vuln_pct >= 50:
            color, level = 'rgba(255,140,0,0.6)', 'High'
        elif vuln_pct >= 25:
            color, level = 'rgba(255,215,0,0.6)', 'Moderate'
        else:
            color, level = 'rgba(50,205,50,0.6)', 'Low'
        
        zone_stats.append({
            'zone': zone_key,
            'vulnerability_pct': vuln_pct,
            'total': total,
            'vulnerable': zone['vulnerable']
        })
        
        # Draw rectangle
        corners_lat = [
            center_lat - grid_size/2, center_lat + grid_size/2,
            center_lat + grid_size/2, center_lat - grid_size/2,
            center_lat - grid_size/2
        ]
        corners_lon = [
            center_lon - grid_size/2, center_lon - grid_size/2,
            center_lon + grid_size/2, center_lon + grid_size/2,
            center_lon - grid_size/2
        ]
        
        fig.add_trace(go.Scattermapbox(
            lat=corners_lat,
            lon=corners_lon,
            mode='lines',
            fill='toself',
            fillcolor=color,
            line=dict(color='black', width=1),
            hovertemplate=f'<b>Zone {zone_key}</b><br>' +
                         f'Vulnerability Level: {level}<br>' +
                         f'Buildings: {total}<br>' +
                         f'Vulnerable: {zone["vulnerable"]} ({vuln_pct:.1f}%)<br>' +
                         f'Hotspots: {zone["hotspots"]}<extra></extra>',
            showlegend=False
        ))
    
    avg_lat = sum(lats) / len(lats)
    avg_lon = sum(lons) / len(lons)
    
    fig.update_layout(
        title="Zone-Level Vulnerability Assessment",
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=avg_lat, lon=avg_lon),
            zoom=13
        ),
        height=800
    )
    
    fig.write_html(output_file)
    print(f"[OK] Choropleth saved: {output_file}")
    
    zone_stats.sort(key=lambda x: x['vulnerability_pct'], reverse=True)
    return zone_stats

def create_dashboard(buildings, vulnerable, hotspots, dot_map_stats, zone_stats, output_file="dashboard.html"):
    """Statistical dashboard"""
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{'type': 'indicator'}, {'type': 'pie'}],
            [{'type': 'bar'}, {'type': 'table'}]
        ],
        row_heights=[0.4, 0.6],
        vertical_spacing=0.15,
        horizontal_spacing=0.15
    )
    
    total = dot_map_stats['total']
    at_vuln = dot_map_stats['hotspot'] + dot_map_stats['vulnerable']
    vuln_pct = (at_vuln / total * 100) if total > 0 else 0
    
    # Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=vuln_pct,
        title={'text': "Vulnerability Rate %"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkred" if vuln_pct > 50 else "orange"},
            'steps': [
                {'range': [0, 25], 'color': "lightgreen"},
                {'range': [25, 50], 'color': "yellow"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "red"}
            ]
        }
    ), row=1, col=1)
    
    # Pie chart
    fig.add_trace(go.Pie(
        labels=['At Vulnerability', 'Safe'],
        values=[at_vuln, dot_map_stats['safe']],
        marker_colors=['#FF6347', '#90EE90'],
        hole=0.3,
        textinfo='label+percent'
    ), row=1, col=2)
    
    # Bar chart
    categories = ['Hotspot', 'Vulnerable', 'Safe']
    counts = [dot_map_stats['hotspot'], dot_map_stats['vulnerable'], dot_map_stats['safe']]
    colors = ['#DC143C', '#FF8C00', '#32CD32']
    
    fig.add_trace(go.Bar(
        x=categories, 
        y=counts, 
        marker_color=colors, 
        text=counts,
        textposition='outside',
        showlegend=False
    ), row=2, col=1)
    
    # Table
    top_zones = zone_stats[:5]
    fig.add_trace(go.Table(
        header=dict(
            values=['Zone', 'Vuln %', 'Buildings'],
            fill_color='orange', 
            font=dict(color='white', size=11),
            align='center'
        ),
        cells=dict(
            values=[
                [z['zone'] for z in top_zones],
                [f"{z['vulnerability_pct']:.1f}%" for z in top_zones],
                [z['total'] for z in top_zones]
            ], 
            align='center'
        )
    ), row=2, col=2)
    
    fig.update_layout(height=800, showlegend=False, title_text="Vulnerability Dashboard")
    fig.write_html(output_file)
    print(f"[OK] Dashboard saved: {output_file}")

def create_all_visualizations(buildings, water_nodes, vulnerable, hotspots, city_name, output_dir="outputs"):
    """Create all 4 visualizations"""
    os.makedirs(output_dir, exist_ok=True)
    
    city_slug = city_name.lower().replace(' ', '_')
    
    print(f"\n{'='*60}")
    print(f"Creating Visualizations for {city_name}")
    print(f"{'='*60}\n")
    
    print("1. Creating dot map...")
    stats = create_dot_map(buildings, water_nodes, vulnerable, hotspots,
                          f"{output_dir}/{city_slug}_dot_map.html")
    
    print("2. Creating heatmap...")
    create_heatmap(buildings, water_nodes, vulnerable, hotspots,
                  f"{output_dir}/{city_slug}_heatmap.html")
    
    print("3. Creating choropleth...")
    zone_stats = create_choropleth_zones(buildings, water_nodes, vulnerable, hotspots,
                                        output_file=f"{output_dir}/{city_slug}_choropleth.html")
    
    print("4. Creating dashboard...")
    create_dashboard(buildings, vulnerable, hotspots, stats, zone_stats,
                    f"{output_dir}/{city_slug}_dashboard.html")
    
    print(f"\n{'='*60}")
    print(f"[OK] All visualizations created for {city_name}!")
    print(f"{'='*60}\n")

# Backwards compatibility for notebook
def create_flood_map(center_lat, center_lon, buildings, hotspots):
    """
    Legacy function for notebook compatibility.
    Creates a simple Folium map (original behavior).
    """
    try:
        import folium
    except ImportError:
        print("Folium not installed. Use create_all_visualizations for Plotly maps.")
        return None
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles='CartoDB positron')

    # Add Buildings
    feature_group_buildings = folium.FeatureGroup(name="Vulnerable Buildings")
    for b in buildings:
        folium.CircleMarker(
            location=[b['lat'], b['lon']],
            radius=3,
            color='red',
            fill=True,
            fill_opacity=0.6,
            popup=f"Building ID: {b['id']}"
        ).add_to(feature_group_buildings)
    feature_group_buildings.add_to(m)

    # Add Hotspots
    feature_group_hotspots = folium.FeatureGroup(name="Hotspots")
    for i, h in enumerate(hotspots):
        folium.Marker(
            location=[h['lat'], h['lon']],
            popup=f"Hotspot Rank: {i+1}<br>Density: {h['density']}",
            icon=folium.Icon(color='orange', icon='fire')
        ).add_to(feature_group_hotspots)
    feature_group_hotspots.add_to(m)

    folium.LayerControl().add_to(m)
    
    return m

