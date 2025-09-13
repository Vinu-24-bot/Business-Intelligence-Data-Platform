import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="retail_analytics",
    user="postgres",
    password="admin123",
    port=5432
)
cur = conn.cursor()

# Load customers
customers = pd.read_csv("data/customers.csv")
for _, row in customers.iterrows():
    cur.execute("""
        INSERT INTO customers (customer_id, name, age, gender, location, total_purchase, last_purchase_date, churn_label)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING;
    """, tuple(row))

# Load transactions
transactions = pd.read_csv("data/transactions.csv")
for _, row in transactions.iterrows():
    cur.execute("""
        INSERT INTO transactions (transaction_id, customer_id, product_category, payment_method, amount, transaction_date)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING;
    """, tuple(row))

conn.commit()
cur.close()
conn.close()
print("✅ Data loaded into Postgres")
