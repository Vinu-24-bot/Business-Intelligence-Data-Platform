from db_utils import exec_sql

exec_sql("REFRESH MATERIALIZED VIEW CONCURRENTLY bi.monthly_sales_mview;")
print("✅ Refreshed materialized view.")
