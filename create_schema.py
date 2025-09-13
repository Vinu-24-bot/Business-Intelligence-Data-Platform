import os
from sqlalchemy import text
from db_utils import get_engine

SQL_FILE = "/opt/airflow/scripts/sql/create_schema.sql"

engine = get_engine()
with engine.begin() as conn:
    with open(SQL_FILE, "r", encoding="utf-8") as f:
        conn.execute(text(f.read()))
print("✅ Schema created/updated.")
