import requests
from bs4 import BeautifulSoup
import json
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


LOCALITIES = {
    "kochi": "https://www.zomato.com/kochi/restaurants?category=1",
    "Kozhikode": "https://www.zomato.com/kozhikode/restaurants",
    "kasaragod": "https://www.zomato.com/kasaragod/restaurants",
    "thiruvanantapuram": "https://www.zomato.com/trivandrum/kesavadasapuram-restaurants?category=1&delivery_subzone=18310&place_name=Tiruvan%C3%A1ntapuram%2C++Kerala%2C++India",

}

def fetch_locality(url, locality_name, delay=2):
    response = requests.get(url, headers=HEADERS, timeout=15)
    if response.status_code != 200:
        print(f"  Failed (status {response.status_code}) for {locality_name}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find_all("script", {"type": "application/ld+json"})

    restaurants = []
    for script in scripts:
        try:
            data = json.loads(script.string)
        except (json.JSONDecodeError, TypeError):
            continue

        items = data.get("itemListElement", [])
        if not items:
            continue

        for entry in items:
            item = entry.get("item", {})
            if item.get("@type") != "Restaurant":
                continue
            rating_info = item.get("aggregateRating", {})
            restaurants.append({
                "name": item.get("name"),
                "locality": locality_name,
                "rating": rating_info.get("ratingValue"),
                "review_count": rating_info.get("reviewCount"),
                "cuisine": item.get("servesCuisine"),
                "address": item.get("address", {}).get("streetAddress"),
                "price_range": item.get("priceRange"),
                "url": item.get("url"),
            })

    time.sleep(delay)
    return restaurants

def main():
    os.makedirs("data/raw", exist_ok=True)
    all_restaurants = []

    for locality, url in LOCALITIES.items():
        if "PASTE_URL_HERE" in url:
            print(f"Skipping {locality} — no URL filled in yet")
            continue
        print(f"Fetching: {locality}")
        results = fetch_locality(url, locality)
        print(f"  Found {len(results)} restaurants")
        all_restaurants.extend(results)

    with open("data/raw/all_restaurants.json", "w", encoding="utf-8") as f:
        json.dump(all_restaurants, f, ensure_ascii=False, indent=2)

    print(f"\nTotal restaurants collected: {len(all_restaurants)}")

if __name__ == "__main__":
    main()