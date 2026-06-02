#!/usr/bin/env python3
"""
Script to read a GPX file and print waypoints in different formats
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET


def create_gpx_with_waypoints(waypoints, namespace):
    """
    Create a new GPX ElementTree with only waypoints (no tracks).
    
    Args:
        waypoints: List of waypoint elements
        namespace: GPX namespace dict
    
    Returns:
        ElementTree object with GPX structure
    """
    # Create GPX root element
    gpx = ET.Element('gpx')
    gpx.set('version', '1.1')
    gpx.set('creator', 'gpx_waypoints.py')
    gpx.set('xmlns', 'http://www.topografix.com/GPX/1/1')
    gpx.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    gpx.set('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')
    
    # Copy waypoints to the new GPX document
    for waypoint in waypoints:
        # Create a copy of the waypoint element
        new_wpt = ET.Element('wpt')
        new_wpt.set('lat', waypoint.get('lat'))
        new_wpt.set('lon', waypoint.get('lon'))
        
        # Copy child elements (name, description, etc.)
        for child in waypoint:
            # Remove namespace prefix for copying
            child_tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            new_child = ET.Element(child_tag)
            new_child.text = child.text
            new_child.tail = child.tail
            # Copy attributes
            for attr, value in child.attrib.items():
                new_child.set(attr, value)
            new_wpt.append(new_child)
        
        gpx.append(new_wpt)
    
    return ET.ElementTree(gpx)


def parse_gpx_waypoints(gpx_file, format_type='us-csv'):
    """
    Parse a GPX file and extract waypoints.
    
    Args:
        gpx_file: Path to the GPX file
        format_type: Output format ('us-csv', 'eu-csv', or 'gpx-wp')
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
        
        # Handle GPX output format
        if format_type == 'gpx-wp':
            # Create a new GPX structure with only waypoints
            gpx_output = create_gpx_with_waypoints(waypoints, namespace)
            
            # Generate output filename
            base_name = os.path.splitext(gpx_file)[0]
            output_file = f"{base_name}_waypoints.gpx"
            
            # Write the GPX file
            gpx_output.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"GPX file with waypoints written to: {output_file}")
        else:
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
        choices=['us-csv', 'eu-csv', 'gpx-wp'],
        default='us-csv',
        help='Output format: us-csv (default), eu-csv, or gpx-wp (GPX file with waypoints only)'
    )
    
    args = parser.parse_args()
    parse_gpx_waypoints(args.gpx_file, args.format)


if __name__ == "__main__":
    main()
