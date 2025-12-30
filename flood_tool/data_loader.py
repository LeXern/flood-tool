import requests
import sys
def fetch_osm_data(bbox, query_type="building"):
    """
    Fetch OSM data for a given bbox and query type.
    bbox: (south, west, north, east)
    query_type: 'building' or 'water'
    Returns: List of dictionary records {'lat': float, 'lon': float, 'id': int, 'type': str}
    """
    # List of Overpass API endpoints ( Main + Mirrors)
    overpass_urls = [
        "http://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://lz4.overpass-api.de/api/interpreter"
    ]
    
    # Construct query based on type
    if query_type == "water":
        # Query for water bodies (river, water, etc.)
        # We want nodes or simplified ways. 
        # Getting all nodes of ways can be heavy, but accurate enough for 'points'
        query = f"""
        [out:json][timeout:60];
        (
          way["natural"="water"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
          relation["natural"="water"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
          way["waterway"="river"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        (._;>;);
        out body;
        """
    else:
        # Buildings
        query = f"""
        [out:json][timeout:60];
        (
          way["building"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
        );
        out center;
        """

    for url in overpass_urls:
        try:
            print(f"Requesting data from: {url}...")
            response = requests.get(url, params={'data': query}, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if query_type == "water":
                # Extract nodes from the water ways
                for element in data['elements']:
                    if element['type'] == 'node':
                        results.append({
                            'lat': element['lat'],
                            'lon': element['lon'],
                            'id': element['id'],
                            'type': 'water_node'
                        })
            else:
                # For buildings
                for element in data['elements']:
                    if element['type'] == 'way' and 'center' in element:
                        results.append({
                            'lat': element['center']['lat'],
                            'lon': element['center']['lon'],
                            'id': element['id'],
                            'type': 'building_center'
                        })
            
            # If we got here, success! Return results.
            print(f"Successfully fetched {len(results)} items from {url}.")
            return results

        except requests.exceptions.Timeout:
            print(f"Timeout connecting to {url}. Trying next mirror...", file=sys.stderr)
            continue # Try next URL
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {url}: {e}. Trying next mirror...", file=sys.stderr)
            continue # Try next URL
        except Exception as e:
            print(f"Unexpected error with {url}: {e}", file=sys.stderr)
            # Logic errors might be consistent across APIs, but safer to try next just in case
            continue

    # If loop finishes without returning, all failed
    print("Error: All API endpoints failed.", file=sys.stderr)
    return []
