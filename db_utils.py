import os
from sqlalchemy import create_engine, text

DB_URL = os.getenv("WAREHOUSE_DB_URL")

def get_engine():
    return create_engine(DB_URL, pool_pre_ping=True)

def exec_sql(sql: str):
    eng = get_engine()
    with eng.begin() as conn:
        conn.execute(text(sql))
