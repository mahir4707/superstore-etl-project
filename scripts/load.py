import pandas as pd
from sqlalchemy import create_engine

# =========================
# Load Data from CSV
# =========================
df = pd.read_csv("data/Superstore_Final_Cleaned.csv")

# =========================
# Create Database Connection
# =========================
engine = create_engine(
    "postgresql://postgres:mahir@localhost:5433/superstore_db"
)

df.columns = [col.lower() for col in df.columns]

# =========================
# Load Data into PostgreSQL
# =========================
df.to_sql(
    name="superstore",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data loaded successfully into PostgreSQL database 'superstore_db' in the 'superstore' table.")