#!/usr/bin/env python3
"""
Script to read a GPX file and create an interactive map with waypoints using LeafletJS
"""

import sys
import argparse
import xml.etree.ElementTree as ET
import json


def parse_gpx_waypoints(gpx_file):
    """
    Parse a GPX file and extract waypoints.
    
    Args:
        gpx_file: Path to the GPX file
    
    Returns:
        List of waypoint dictionaries with 'name', 'lat', 'lon' keys
    """
    try:
        tree = ET.parse(gpx_file)
        root = tree.getroot()
        
        # Handle GPX namespace
        namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        
        # Try with namespace first, then without
        waypoints_elem = root.findall('gpx:wpt', namespace)
        if not waypoints_elem:
            waypoints_elem = root.findall('wpt')
        
        waypoints = []
        for waypoint in waypoints_elem:
            lat = waypoint.get('lat')
            lon = waypoint.get('lon')
            
            # Get name element
            name_elem = waypoint.find('gpx:name', namespace)
            if name_elem is None:
                name_elem = waypoint.find('name')
            
            name = name_elem.text if name_elem is not None else 'Unnamed Waypoint'
            
            if lat and lon:
                waypoints.append({
                    'name': name,
                    'lat': float(lat),
                    'lon': float(lon)
                })
        
        return waypoints
    
    except FileNotFoundError:
        print(f"Error: File '{gpx_file}' not found.")
        sys.exit(1)
    except ET.ParseError as e:
        print(f"Error: Failed to parse GPX file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def create_map_html(waypoints, output_file='map.html'):
    """
    Create an interactive map HTML file with waypoints using LeafletJS.
    
    Args:
        waypoints: List of waypoint dictionaries
        output_file: Output HTML filename
    """
    if not waypoints:
        print("Error: No waypoints found in GPX file.")
        sys.exit(1)
    
    # Calculate map center and bounds
    lats = [wp['lat'] for wp in waypoints]
    lons = [wp['lon'] for wp in waypoints]
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    
    # Create waypoints GeoJSON for the map
    waypoints_json = json.dumps(waypoints)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPX Waypoints Map</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }}
        #map {{
            position: absolute;
            top: 0;
            bottom: 0;
            width: 100%;
            height: 100vh;
        }}
        #info {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            background-color: white;
            padding: 10px 15px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 1000;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="info">
        <strong>Waypoints:</strong> <span id="waypoint-count">0</span>
    </div>
    
    <script>
        // Waypoints data
        const waypoints = {waypoints_json};
        
        // Create map centered on waypoints
        const map = L.map('map').setView([{center_lat}, {center_lon}], 8);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        }}).addTo(map);
        
        // Add waypoint markers
        const markers = [];
        waypoints.forEach(function(waypoint, index) {{
            const marker = L.marker([waypoint.lat, waypoint.lon])
                .addTo(map)
                .bindPopup(
                    '<div style="font-weight: bold;">' + waypoint.name + '</div>' +
                    '<div>Lat: ' + waypoint.lat.toFixed(4) + '</div>' +
                    '<div>Lon: ' + waypoint.lon.toFixed(4) + '</div>'
                );
            markers.push(marker);
        }});
        
        // Fit map to show all markers
        if (markers.length > 0) {{
            const group = new L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.1));
        }}
        
        // Update waypoint count
        document.getElementById('waypoint-count').textContent = waypoints.length;
    </script>
</body>
</html>
"""
    
    # Write HTML file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Map created successfully: {output_file}")
        print(f"Total waypoints: {len(waypoints)}")
    except Exception as e:
        print(f"Error: Failed to write HTML file - {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Read a GPX file and create an interactive map with waypoints'
    )
    parser.add_argument(
        'gpx_file',
        help='Path to the GPX file'
    )
    parser.add_argument(
        '-o', '--output',
        default='map.html',
        help='Output HTML filename (default: map.html)'
    )
    
    args = parser.parse_args()
    
    # Parse waypoints from GPX file
    waypoints = parse_gpx_waypoints(args.gpx_file)
    
    # Create map HTML
    create_map_html(waypoints, args.output)


if __name__ == "__main__":
    main()
