"""Simple extract-transform-load pipeline using CSV and SQLite."""
import sqlite3
import pandas as pd

def extract(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data.columns = [c.strip().lower().replace(" ", "_") for c in data.columns]
    data = data.drop_duplicates()
    data = data.dropna(how="all")
    return data

def load(df: pd.DataFrame, database: str = "analytics.db", table: str = "clean_data") -> None:
    with sqlite3.connect(database) as connection:
        df.to_sql(table, connection, if_exists="replace", index=False)

def run_pipeline(source: str) -> None:
    raw = extract(source)
    clean = transform(raw)
    load(clean)
    print(f"Loaded {len(clean)} cleaned rows")

if __name__ == "__main__":
    print("Call run_pipeline('data.csv') to execute the ETL workflow.")
