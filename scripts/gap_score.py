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


dedup = df.groupby("name").agg(
    rating=("rating", "first"),
    review_count_num=("review_count_num", "first"),
    cuisine=("cuisine", "first"),
    localities_seen=("locality", lambda x: ", ".join(sorted(set(x))))
).reset_index()

print(f"Raw rows: {len(df)} -> Unique restaurants after dedup: {len(dedup)}")
print(f"({len(df) - len(dedup)} duplicate entries removed)\n")


dedup["demand_index"] = (dedup["rating"] * np.log(dedup["review_count_num"] + 1)).round(2)

top10 = dedup.sort_values("demand_index", ascending=False).head(10)
print("=== TOP 10 HIGHEST-DEMAND RESTAURANTS IN KOCHI ===")
print(top10[["name", "rating", "review_count_num", "demand_index", "localities_seen"]].to_string(index=False))

dedup.to_csv("data/clean/restaurants_deduped.csv", index=False)

dedup["cuisine_list"] = dedup["cuisine"].fillna("").apply(lambda x: [c.strip() for c in x.split(",") if c.strip()])
cuisine_exploded = dedup.explode("cuisine_list")

cuisine_summary = cuisine_exploded.groupby("cuisine_list").agg(
    restaurant_count=("name", "count"),
    avg_rating=("rating", "mean"),
    avg_demand_index=("demand_index", "mean")
).round(2).sort_values("restaurant_count", ascending=False).head(12)

cuisine_summary.to_csv("data/clean/cuisine_landscape.csv")
print("\n=== CUISINE LANDSCAPE (top 12 by frequency) ===")
print(cuisine_summary.to_string())

correlation = dedup["review_count_num"].corr(dedup["rating"])
print(f"\n=== CORRELATION: review count vs rating (deduped) ===")
print(f"Pearson correlation: {round(correlation, 3)}")

if __name__ == "__main__":
    pass