# build_db.py
import duckdb
from pathlib import Path

DATA_DIR = Path("data/processed")
DB_PATH = Path("data/energy.duckdb")

CSV_TABLES = {
    "oil_prod": "country_production_oil.csv",
    "gas_prod": "country_production_gas.csv",
    "oil_cons": "country_consumtion_oil.csv",
    "gas_cons": "country_consumtion_gas.csv",
    "goget": "goget_units.csv",
    "ogim": "ogim_facilities.csv",
}

PRICE_CSV = "price_timeseries.csv"

def main():
    print("Building DuckDB database...")
    con = duckdb.connect(DB_PATH)

    # -----------------------------
    # Load core CSV tables
    # -----------------------------
    for table, csv_file in CSV_TABLES.items():
        csv_path = DATA_DIR / csv_file
        print(f"Loading {csv_file} → {table}")

        con.execute(f"""
            CREATE OR REPLACE TABLE {table} AS
            SELECT * FROM read_csv_auto('{csv_path.as_posix()}')
        """)

    # -----------------------------
    # Load & normalize price table
    # -----------------------------
    price_path = DATA_DIR / PRICE_CSV
    print(f"Loading {PRICE_CSV} → price")

    con.execute(f"""
        CREATE OR REPLACE TABLE price AS
        SELECT
            CAST(period AS DATE)        AS date,
            value::DOUBLE               AS price,
            benchmark,
            product,
            units,
            duoarea,
            "area-name"                 AS area_name,
            "series-description"        AS series_description
        FROM read_csv_auto('{price_path.as_posix()}')
        WHERE value IS NOT NULL
    """)

    # -----------------------------
    # Indexes (SAFE & CORRECT)
    # -----------------------------
    con.execute("CREATE INDEX IF NOT EXISTS idx_oil_iso_year ON oil_prod (iso3, Year)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_gas_iso_year ON gas_prod (iso3, Year)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_ogim_iso ON ogim (iso3)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_price_date ON price (date)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_price_benchmark ON price (benchmark)")

    con.close()
    print("DuckDB build complete.")

if __name__ == "__main__":
    main()
