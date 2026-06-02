# GPX Waypoints Tools

A collection of Python scripts for reading and processing GPX (GPS Exchange Format) files. Extract waypoints, convert coordinate formats, and visualize them on interactive maps.

## Scripts

### 1. gpx_waypoints.py

Reads a GPX file and prints waypoints in various formats (CSV, GPX, with coordinate conversion options).

#### Usage

```bash
python gpx_waypoints.py <gpx_file> [--format FORMAT] [--gps GPS_FORMAT]
```

#### Arguments

- `gpx_file` (required): Path to the GPX file to read

#### Options

- `--format {us-csv|eu-csv|gpx-wp}`: Output format (default: us-csv)
  - `us-csv`: US CSV format with comma delimiter
  - `eu-csv`: European CSV format with semicolon delimiter and comma decimal separator
  - `gpx-wp`: Create new GPX file with only waypoints (no tracks)

- `--gps {DMS|DM}`: GPS coordinate format (for use with --format eu-csv)
  - `DMS`: Degrees Minutes Seconds format
  - `DM`: Degrees Decimal Minutes format

#### Examples

##### Example 1: Basic US CSV output
```bash
python gpx_waypoints.py hiking_route.gpx
```

Output:
```
"waypoint", "lat", "lon"
"Mountain Peak", 60.16987, 24.94556
"Lake View", 60.17123, 24.95234
"Forest Trail", 60.18456, 24.93789
```

##### Example 2: EU CSV format with decimal comma
```bash
python gpx_waypoints.py hiking_route.gpx --format eu-csv
```

Output:
```
"waypoint"; "lat"; "lon"
"Mountain Peak"; 60,16987; 24,94556
"Lake View"; 60,17123; 24,95234
"Forest Trail"; 60,18456; 24,93789
```

##### Example 3: EU CSV with Degrees Decimal Minutes format
```bash
python gpx_waypoints.py hiking_route.gpx --format eu-csv --gps DM
```

Output:
```
"waypoint"; "lat"; "lon"
"Mountain Peak"; 60°10.193'N; 24°56.734'E
"Lake View"; 60°10.274'N; 24°57.140'E
"Forest Trail"; 60°11.074'N; 24°56.273'E
```

##### Example 4: EU CSV with Degrees Minutes Seconds format
```bash
python gpx_waypoints.py hiking_route.gpx --format eu-csv --gps DMS
```

Output:
```
"waypoint"; "lat"; "lon"
"Mountain Peak"; 60°10'11.5"N; 24°56'44.0"E
"Lake View"; 60°10'16.4"N; 24°57'8.4"E
"Forest Trail"; 60°11'4.4"N; 24°56'16.4"E
```

##### Example 5: Extract waypoints to new GPX file
```bash
python gpx_waypoints.py track_with_waypoints.gpx --format gpx-wp
```

Output:
```
GPX file with waypoints written to: track_with_waypoints_waypoints.gpx
```

This creates a new GPX file containing only the waypoints (removes any tracks or routes).

---

### 2. gpx_map.py

Creates an interactive web map displaying all waypoints from a GPX file using LeafletJS and OpenStreetMap.

#### Usage

```bash
python gpx_map.py <gpx_file> [-o OUTPUT_FILE]
```

#### Arguments

- `gpx_file` (required): Path to the GPX file to read

#### Options

- `-o, --output OUTPUT_FILE`: Output HTML filename (default: map.html)

#### Examples

##### Example 1: Create default map.html
```bash
python gpx_map.py hiking_route.gpx
```

Output:
```
Map created successfully: map.html
Total waypoints: 3
```

This creates an interactive map at `map.html` that can be opened in any web browser.

##### Example 2: Create custom output file
```bash
python gpx_map.py hiking_route.gpx -o my_hiking_map.html
```

Output:
```
Map created successfully: my_hiking_map.html
Total waypoints: 3
```

#### Features

- **Interactive Map**: Uses LeafletJS with OpenStreetMap tiles
- **Waypoint Markers**: Each waypoint appears as a clickable marker
- **Popup Information**: Click any marker to see:
  - Waypoint name
  - Latitude (4 decimal places)
  - Longitude (4 decimal places)
- **Auto-Zoom**: Map automatically centers and zooms to fit all waypoints
- **Waypoint Counter**: Displays total waypoint count in bottom-right corner
- **No Setup Required**: Uses CDN for all libraries - just open HTML in browser

#### Web Browser Compatibility

- Chrome/Chromium
- Firefox
- Safari
- Edge
- Any modern browser with JavaScript enabled

---

## Installation

### Requirements

- Python 3.6+
- No external dependencies required (uses only Python standard library)

### Setup

1. Clone or download the scripts
2. Make scripts executable (Linux/macOS):
   ```bash
   chmod +x gpx_waypoints.py gpx_map.py
   ```

---

## Complete Workflow Examples

### Example Workflow 1: Convert and display a hiking route

```bash
# Step 1: Extract waypoints to EU format with Degrees Decimal Minutes
python gpx_waypoints.py my_hike.gpx --format eu-csv --gps DM > waypoints.csv

# Step 2: Create interactive map
python gpx_map.py my_hike.gpx -o hiking_map.html

# Step 3: Open hiking_map.html in your browser
```

### Example Workflow 2: Clean up and export a GPX file

```bash
# Step 1: Extract only waypoints to a new GPX file
python gpx_waypoints.py track_with_data.gpx --format gpx-wp

# Step 2: View the waypoints in CSV format
python gpx_waypoints.py track_with_data_waypoints.gpx --format us-csv

# Step 3: Create a map from the cleaned waypoints
python gpx_map.py track_with_data_waypoints.gpx
```

### Example Workflow 3: Prepare for different locales

```bash
# For US audience (decimal points, comma separators)
python gpx_waypoints.py route.gpx --format us-csv > route_us.csv

# For European audience (decimal commas, semicolon separators)
python gpx_waypoints.py route.gpx --format eu-csv --gps DM > route_eu.csv

# Create map for both
python gpx_map.py route.gpx -o route_map.html
```

---

## Input GPX File Format

The scripts support standard GPX 1.1 format files. A minimal example with waypoints:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Example" xmlns="http://www.topografix.com/GPX/1/1">
  <wpt lat="60.16987" lon="24.94556">
    <name>Mountain Peak</name>
    <desc>Starting point</desc>
  </wpt>
  <wpt lat="60.17123" lon="24.95234">
    <name>Lake View</name>
  </wpt>
</gpx>
```

The scripts extract:
- Waypoint coordinates (lat/lon)
- Waypoint names
- Ignore tracks, routes, and other GPX elements (except with gpx-wp format which preserves everything)

---

## Coordinate Format Reference

### Decimal Degrees (DD)
- Format: `60.16987`
- Used in: us-csv, eu-csv (default)

### Degrees Decimal Minutes (DM)
- Format: `60°10.193'N`
- Used in: eu-csv --gps DM
- Useful for: GPS navigation devices, some surveying applications

### Degrees Minutes Seconds (DMS)
- Format: `60°10'11.5"N`
- Used in: eu-csv --gps DMS
- Useful for: Traditional maps, precise navigation

---

## Troubleshooting

### Script won't run
- Ensure Python 3.6+ is installed: `python --version`
- On macOS/Linux, make script executable: `chmod +x gpx_waypoints.py`

### "No waypoints found in the GPX file"
- Verify the GPX file contains `<wpt>` elements
- Check that waypoint elements have lat and lon attributes

### Map opens but shows blank page
- Ensure you have internet connection (uses CDN for libraries)
- Check browser console for errors (F12)
- Try a different browser

### Output file not created
- Check write permissions in the current directory
- Ensure sufficient disk space
- Try specifying full path: `python gpx_waypoints.py /path/to/file.gpx`

---

## License

These scripts are provided as-is for processing GPX files.

---

## Version History

- v1.0 (2026-06-02): Initial release with gpx_waypoints.py and gpx_map.py
