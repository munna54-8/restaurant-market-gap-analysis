import pandas as pd

df = pd.read_csv("data/clean/restaurants_deduped.csv")
df["cuisine_list"] = df["cuisine"].fillna("").apply(lambda x: [c.strip() for c in x.split(",") if c.strip()])
exploded = df.explode("cuisine_list")

summary = exploded.groupby("cuisine_list").agg(
    restaurant_count=("name", "count"),
    avg_demand_index=("demand_index", "mean")
).round(2)

summary = summary[summary["restaurant_count"] >= 3]  # drop cuisines with too few data points to rank meaningfully

summary["demand_percentile"] = summary["avg_demand_index"].rank(pct=True) * 100
summary["supply_percentile"] = summary["restaurant_count"].rank(pct=True) * 100
summary["gap_score"] = (summary["demand_percentile"] - summary["supply_percentile"]).round(1)

summary = summary.sort_values("gap_score", ascending=False)
summary.to_csv("data/clean/cuisine_gap_score.csv")

print("=== CUISINE GAP SCORE (positive = high demand, low supply = opportunity) ===")
print(summary.to_string())