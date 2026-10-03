from pathlib import Path
import pandas as pd
from database.db_connection import engine

RAW_DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "healthcare_dataset.csv"
)

def ingest_raw_data():
  """Reads the raw CSV dataset and loads it into PostgreSQL."""
  if not RAW_DATA_PATH.exists():
    print(f"[ERROR] Could not find dataset at path: {RAW_DATA_PATH}")
    return

  print(f"[1/2] Loading dataset from {RAW_DATA_PATH}...")
  df = pd.read_csv(RAW_DATA_PATH)

  print(f"[2/2] Ingesting {len(df)} records into 'raw_healthcare_data' table...")
  
  # Save DataFrame directly into Aiven PostgreSQL table
  df.to_sql("raw_healthcare_data", con=engine, if_exists="replace", index=False)

  print("[SUCCESS] Raw dataset successfully ingested into PostgreSQL database!")

if __name__ == "__main__":
  ingest_raw_data()