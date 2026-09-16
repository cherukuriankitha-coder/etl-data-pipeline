"""Small but extensible CSV-to-SQLite ETL pipeline."""
import logging
import sqlite3
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def extract(path: str) -> pd.DataFrame:
    logger.info("Extracting %s", path)
    return pd.read_csv(path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip().lower().replace(" ", "_") for c in out.columns]
    out = out.drop_duplicates().dropna(how="all")
    for col in out.columns:
        if out[col].dtype == "object":
            out[col] = out[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return out


def validate(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("ETL validation failed: no rows after transformation")
    if df.columns.duplicated().any():
        raise ValueError("ETL validation failed: duplicate column names")


def load(df: pd.DataFrame, database: str, table: str = "clean_data") -> None:
    Path(database).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
    logger.info("Loaded %d rows into %s.%s", len(df), database, table)


def run(source: str, database: str) -> None:
    df = transform(extract(source))
    validate(df)
    load(df, database)
