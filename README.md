# OSM Restaurant Website Export

This script searches OpenStreetMap for restaurants near selected locations and saves their website and phone details to a CSV file.

It uses the public OpenStreetMap Overpass API, so it does not need a Google API key or billing account.

## Files

- `studio_osm.py` - Python script that fetches restaurant data.
- `business_websites.csv` - Output file created when the script runs.

## Requirements

Install `requests` if it is not already installed:

```powershell
pip install requests
```

## Run

From the folder containing the script:

```powershell
python .\studio_osm.py
```

The script creates:

```text
business_websites.csv
```

## CSV Columns

```text
location, name, phone, website, has_phone, has_website
```

- `location` - Search area, such as Kathmandu or Sydney.
- `name` - Restaurant name from OpenStreetMap.
- `phone` - Phone number if available in OSM.
- `website` - Website URL if available in OSM.
- `has_phone` - `True` if a phone number exists.
- `has_website` - `True` if a website exists.

## Change Locations

Edit the `LOCATIONS` list in `studio_osm.py`:

```python
LOCATIONS = [
    {
        "name": "Kathmandu, Nepal",
        "lat": 27.7172,
        "lng": 85.3240,
        "radius": 5000,
    },
    {
        "name": "Sydney, Australia",
        "lat": -33.8688,
        "lng": 151.2093,
        "radius": 5000,
    },
]
```

`radius` is measured in meters.

## Notes

OpenStreetMap data is community-maintained, so not every restaurant will have a phone number or website.

If one Overpass endpoint is unavailable, the script automatically tries another endpoint.

