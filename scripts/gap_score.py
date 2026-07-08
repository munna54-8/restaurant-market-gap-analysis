import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("data/clean/restaurants.db")
df = pd.read_sql_query("SELECT * FROM restaurants", conn)
conn.close()

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
df = df.dropna(subset=["rating", "review_count_num"])

# --- Demand-intensity index per locality ---
df["weighted_score"] = df["rating"] * np.log(df["review_count_num"] + 1)

locality_summary = df.groupby("locality").agg(
    restaurant_count=("name", "count"),
    avg_rating=("rating", "mean"),
    avg_reviews=("review_count_num", "mean"),
    demand_index=("weighted_score", "mean")
).round(2).sort_values("demand_index", ascending=False)

locality_summary.to_csv("data/clean/locality_demand_index.csv")
print("=== LOCALITY DEMAND INDEX (highest = strongest demand signal) ===")
print(locality_summary.to_string())

# --- Cuisine frequency across the whole dataset ---
df["cuisine_list"] = df["cuisine"].fillna("").apply(lambda x: [c.strip() for c in x.split(",") if c.strip()])
cuisine_exploded = df.explode("cuisine_list")
cuisine_counts = cuisine_exploded["cuisine_list"].value_counts().head(15)
cuisine_counts.to_csv("data/clean/cuisine_frequency.csv")
print("\n=== TOP CUISINES ACROSS ALL LOCALITIES ===")
print(cuisine_counts.to_string())

# --- Does more reviews correlate with higher rating? (rich-get-richer test) ---
correlation = df["review_count_num"].corr(df["rating"])
print(f"\n=== CORRELATION: review count vs rating ===")
print(f"Pearson correlation: {round(correlation, 3)}")
if abs(correlation) < 0.2:
    print("Interpretation: weak/no relationship — popularity and quality rating are largely independent here.")
elif correlation > 0:
    print("Interpretation: more-reviewed restaurants tend to be rated slightly higher.")
else:
    print("Interpretation: more-reviewed restaurants tend to be rated slightly lower.")