import os
import django
import requests
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from hotels.models import Hotel

CITIES = {
    "paris": {
        "query": """
        [out:json][timeout:25];
        area["name"="Paris"]["admin_level"="8"]->.a;
        (
          node(area.a)["tourism"="hotel"];
          way(area.a)["tourism"="hotel"];
          relation(area.a)["tourism"="hotel"];
        );
        out center;
        """,
        "display": "Paris, France"
    },
    "madrid": {
        "query": """
        [out:json][timeout:25];
        area["name"="Madrid"]["admin_level"="8"]->.a;
        (
          node(area.a)["tourism"="hotel"];
          way(area.a)["tourism"="hotel"];
          relation(area.a)["tourism"="hotel"];
        );
        out center;
        """,
        "display": "Madrid, Spain"
    },
    "roma": {
        "query": """
        [out:json][timeout:25];
        area["name"="Roma"]["admin_level"="8"]->.a;
        (
          node(area.a)["tourism"="hotel"];
          way(area.a)["tourism"="hotel"];
          relation(area.a)["tourism"="hotel"];
        );
        out center;
        """,
        "display": "Roma, Italy"
        },
        "london": {
        "query": """
        [out:json][timeout:25];
        area["wikidata"="Q84"]->.a;
        (
        node(area.a)["tourism"="hotel"];
        way(area.a)["tourism"="hotel"];
        relation(area.a)["tourism"="hotel"];
        );
        out center;
        """,
        "display": "London, UK"
    },
    "new york": {
        "query": """
        [out:json][timeout:25];
        area["wikidata"="Q60"]->.a;
        (
        node(area.a)["tourism"="hotel"];
        way(area.a)["tourism"="hotel"];
        relation(area.a)["tourism"="hotel"];
        );
        out center;
        """,
        "display": "New York, USA"
        }
}

def fetch_and_save_hotels(city, info):
    print(f"Fetching hotels in {info['display']}...")

    try:
        response = requests.post("https://overpass-api.de/api/interpreter", data={"data": info['query']})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data for {info['display']}: {e}")
        return

    data = response.json()
    print(f"Found {len(data['elements'])} hotels in {info['display']}")

    saved_count = 0
    for el in data['elements']:
        tags = el.get("tags", {})
        name = tags.get("name", "Unnamed Hotel")
        address = tags.get("addr:street", "No Address")
        phone = tags.get("phone")
        website = tags.get("website")
        email = tags.get("email")
        stars = tags.get("stars")
        description = tags.get("description")

        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")

        if lat and lon:
            _, created = Hotel.objects.get_or_create(
                name=name,
                lat=lat,
                lon=lon,
                defaults={
                    "address": address,
                    "phone": phone,
                    "website": website,
                    "email": email,
                    "stars": int(stars) if stars and stars.isdigit() else None,
                    "description": description,
                    "city": city.lower(),
                }
            )
            if created:
                saved_count += 1

    print(f"{saved_count} new hotels saved for {city.capitalize()}.")


if __name__ == "__main__":
    for city, info in CITIES.items():
        fetch_and_save_hotels(city, info)
        time.sleep(2)

    print("Finished importing all hotels.")
