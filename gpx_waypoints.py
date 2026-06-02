#!/usr/bin/env python3
"""
Script to read a GPX file and print waypoints in format: name; lat; lon
"""

import sys
import xml.etree.ElementTree as ET


def parse_gpx_waypoints(gpx_file):
    """
    Parse a GPX file and extract waypoints.
    
    Args:
        gpx_file: Path to the GPX file
    """
    try:
        tree = ET.parse(gpx_file)
        root = tree.getroot()
        
        # Handle GPX namespace
        namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        
        # Try with namespace first, then without
        waypoints = root.findall('gpx:wpt', namespace)
        if not waypoints:
            waypoints = root.findall('wpt')
        
        if not waypoints:
            print("No waypoints found in the GPX file.")
            return
        
        # Extract and print waypoint information
        for waypoint in waypoints:
            lat = waypoint.get('lat', 'N/A')
            lon = waypoint.get('lon', 'N/A')
            
            # Get name element
            name_elem = waypoint.find('gpx:name', namespace)
            if name_elem is None:
                name_elem = waypoint.find('name')
            
            name = name_elem.text if name_elem is not None else 'Unknown'
            
            print(f"{name}; {lat}; {lon}")
    
    except FileNotFoundError:
        print(f"Error: File '{gpx_file}' not found.")
        sys.exit(1)
    except ET.ParseError as e:
        print(f"Error: Failed to parse GPX file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python gpx_waypoints.py <gpx_file>")
        sys.exit(1)
    
    gpx_file = sys.argv[1]
    parse_gpx_waypoints(gpx_file)


if __name__ == "__main__":
    main()
