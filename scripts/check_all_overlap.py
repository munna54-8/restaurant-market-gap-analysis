import sqlite3
import pandas as pd
from itertools import combinations

conn = sqlite3.connect("data/clean/restaurants.db")
df = pd.read_sql_query("SELECT name, locality FROM restaurants", conn)
conn.close()

localities = df["locality"].unique()
sets_by_locality = {loc: set(df[df["locality"] == loc]["name"]) for loc in localities}

print("=== PAIRWISE OVERLAP CHECK ===")
for a, b in combinations(localities, 2):
    overlap = sets_by_locality[a] & sets_by_locality[b]
    if overlap:
        print(f"{a} <-> {b}: {len(overlap)} shared restaurants out of 9 each -> {sorted(overlap)}")