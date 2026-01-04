# db.py
import duckdb
from pathlib import Path

DB_PATH = Path("data/energy.duckdb")

def get_connection():
    if not DB_PATH.exists():
        return None
    return duckdb.connect(DB_PATH, read_only=True)

def query(sql, params=None):
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        if params:
            return con.execute(sql, params).df()
        return con.execute(sql).df()
    finally:
        con.close()