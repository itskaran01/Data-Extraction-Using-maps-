import csv
import sys

import requests


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

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
]

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "studio-osm-restaurant-export/1.0",
}

def build_query(location):
    return f"""
[out:json][timeout:25];
(
  node["amenity"="restaurant"](around:{location["radius"]},{location["lat"]},{location["lng"]});
  way["amenity"="restaurant"](around:{location["radius"]},{location["lat"]},{location["lng"]});
  relation["amenity"="restaurant"](around:{location["radius"]},{location["lat"]},{location["lng"]});
);
out center tags;
"""


def get_website(tags):
    return (
        tags.get("website")
        or tags.get("contact:website")
        or tags.get("url")
        or tags.get("contact:url")
        or ""
    )


def get_phone(tags):
    return (
        tags.get("phone")
        or tags.get("contact:phone")
        or tags.get("mobile")
        or tags.get("contact:mobile")
        or ""
    )


def fetch_elements(query):
    last_error = None
    response = None

    for url in OVERPASS_URLS:
        try:
            response = requests.get(
                url,
                params={"data": query},
                headers=HEADERS,
                timeout=60,
            )
            response.raise_for_status()
            return response.json().get("elements", [])
        except requests.RequestException as exc:
            last_error = exc
            print(f"Overpass endpoint failed: {url}", file=sys.stderr)
            if response is not None:
                print(response.text[:1000], file=sys.stderr)

    raise RuntimeError("All Overpass endpoints failed") from last_error


results = []
seen = set()

for location in LOCATIONS:
    elements = fetch_elements(build_query(location))

    for element in elements:
        tags = element.get("tags", {})
        name = tags.get("name", "Unknown")
        website = get_website(tags)
        phone = get_phone(tags)

        # Avoid duplicate rows when OSM has overlapping mapped objects.
        unique_key = (location["name"], name.lower(), website.lower(), phone.lower())
        if unique_key in seen:
            continue
        seen.add(unique_key)

        results.append(
            {
                "location": location["name"],
                "name": name,
                "phone": phone,
                "website": website,
                "has_phone": bool(phone),
                "has_website": bool(website),
            }
        )

results.sort(
    key=lambda row: (
        not row["has_phone"],
        not row["has_website"],
        row["location"].lower(),
        row["name"].lower(),
    )
)

with open("business_websites.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "location",
            "name",
            "phone",
            "website",
            "has_phone",
            "has_website",
        ],
    )
    writer.writeheader()
    writer.writerows(results)

print(f"Saved {len(results)} businesses to business_websites.csv")
