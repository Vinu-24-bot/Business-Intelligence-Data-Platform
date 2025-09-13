import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

# ✅ Use your folder path
BASE_DIR = r"F:\AIBI-Project"

os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

customers_path = os.path.join(BASE_DIR, "data", "customers.csv")
transactions_path = os.path.join(BASE_DIR, "data", "transactions.csv")

# Customers
customers = []
for i in range(200):
    customers.append({
        "customer_id": i+1,
        "name": fake.name(),
        "age": random.randint(18,70),
        "gender": random.choice(["Male","Female"]),
        "location": fake.city(),
        "total_purchase": round(random.uniform(100,5000),2),
        "last_purchase_date": fake.date_between(start_date="-1y", end_date="today"),
        "churn_label": random.choice([0,1])
    })

pd.DataFrame(customers).to_csv(customers_path, index=False)

# Transactions
transactions = []
for i in range(1000):
    transactions.append({
        "transaction_id": i+1,
        "customer_id": random.randint(1,200),
        "product_category": random.choice(["Electronics","Clothing","Grocery","Books"]),
        "payment_method": random.choice(["Credit Card","Debit Card","UPI","Cash"]),
        "amount": round(random.uniform(10,500),2),
        "transaction_date": fake.date_between(start_date="-1y", end_date="today")
    })

pd.DataFrame(transactions).to_csv(transactions_path, index=False)

print("✅ Fake data created in F:\\AIBI-Project\\data\\")
