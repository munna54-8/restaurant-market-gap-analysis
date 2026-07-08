import sqlite3
import pandas as pd

df = pd.read_csv("data/clean/restaurants_clean.csv")
conn = sqlite3.connect("data/clean/restaurants.db")
df.to_sql("restaurants", conn, if_exists="replace", index=False)
conn.close()
print(f"Loaded {len(df)} rows into data/clean/restaurants.db")