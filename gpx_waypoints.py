#!/usr/bin/env python3
"""
Script to read a GPX file and print waypoints in different formats
"""

import sys
import argparse
import xml.etree.ElementTree as ET


def parse_gpx_waypoints(gpx_file, format_type='us-csv'):
    """
    Parse a GPX file and extract waypoints.
    
    Args:
        gpx_file: Path to the GPX file
        format_type: Output format ('us-csv' or 'eu-csv')
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
        
        # Print header based on format type
        if format_type == 'us-csv':
            print('"waypoint", "lat", "lon"')
        elif format_type == 'eu-csv':
            print('"waypoint"; "lat"; "lon"')
        
        # Extract and print waypoint information
        for waypoint in waypoints:
            lat = waypoint.get('lat', 'N/A')
            lon = waypoint.get('lon', 'N/A')
            
            # Get name element
            name_elem = waypoint.find('gpx:name', namespace)
            if name_elem is None:
                name_elem = waypoint.find('name')
            
            name = name_elem.text if name_elem is not None else 'Unknown'
            
            # Format output based on format_type
            if format_type == 'us-csv':
                # US format: "name", lat, lon
                print(f'"{name}", {lat}, {lon}')
            elif format_type == 'eu-csv':
                # EU format: "name"; lat, lon (with comma as decimal separator)
                lat_eu = str(lat).replace('.', ',') if lat != 'N/A' else lat
                lon_eu = str(lon).replace('.', ',') if lon != 'N/A' else lon
                print(f'"{name}"; {lat_eu}; {lon_eu}')
    
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
    parser = argparse.ArgumentParser(
        description='Read a GPX file and print waypoints in different formats'
    )
    parser.add_argument(
        'gpx_file',
        help='Path to the GPX file'
    )
    parser.add_argument(
        '--format',
        choices=['us-csv', 'eu-csv'],
        default='us-csv',
        help='Output format: us-csv (default) or eu-csv'
    )
    
    args = parser.parse_args()
    parse_gpx_waypoints(args.gpx_file, args.format)


if __name__ == "__main__":
    main()
