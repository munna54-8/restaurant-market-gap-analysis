import sqlite3
import pandas as pd

conn = sqlite3.connect("data/clean/restaurants.db")
df = pd.read_sql_query(
    "SELECT name, locality FROM restaurants WHERE locality IN ('Kakkanad','Edappally')",
    conn
)
conn.close()

print(df.sort_values("name").to_string(index=False))