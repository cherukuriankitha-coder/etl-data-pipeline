# ETL Data Pipeline

A modular Python ETL project that extracts CSV data, standardizes and validates it, and loads clean records into SQLite.

## Architecture
`CSV Source -> Extract -> Transform -> Validate -> SQLite -> Analytics-ready Table`

## Tech Stack
Python, Pandas, SQLite, pytest, logging

## Structure
```text
src/pipeline.py          # extract, transform, validate and load stages
tests/test_pipeline.py   # transformation/validation unit test
```

## Features
- Normalizes column names
- Removes exact duplicates and empty rows
- Trims whitespace from string fields
- Rejects empty transformed datasets
- Detects duplicate column names
- Creates the target database directory automatically
- Logs pipeline execution
- Uses a context-managed database connection

## Example
```python
from src.pipeline import run
run("data/raw/customers.csv", "data/warehouse/analytics.db")
```

## Testing
```bash
pytest -q
```

## Production Extensions
Incremental loads, configuration files, schema contracts, orchestration, audit tables, cloud storage, data lineage, and CI/CD can be added as the project evolves.