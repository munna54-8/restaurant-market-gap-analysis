import json
import pandas as pd
import re

with open("data/raw/all_restaurants.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

def parse_review_count(val):
    if pd.isna(val) or val is None:
        return None
    val = str(val).replace(",", "").strip()
    if val.endswith("K"):
        return float(val[:-1]) * 1000
    try:
        return float(val)
    except ValueError:
        return None

df["review_count_num"] = df["review_count"].apply(parse_review_count)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

df = df.drop_duplicates(subset=["name", "locality"])
df = df.dropna(subset=["name", "rating"])

df.to_csv("data/clean/restaurants_clean.csv", index=False)
print(f"Cleaned rows: {len(df)}")
print(df[["locality"]].value_counts())
print("\nSample price_range values:", df["price_range"].dropna().unique()[:5])