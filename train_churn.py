import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
import psycopg2

engine = create_engine("postgresql://postgres:admin123@localhost:5432/retail_analytics")

df = pd.read_sql("SELECT * FROM customers;", engine)

X = df[["age", "total_purchase"]]
y = df["churn_label"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
model = RandomForestClassifier()
model.fit(X_train,y_train)

df["churn_probability"] = model.predict_proba(X)[:,1]
df[["customer_id","churn_probability"]].to_sql("customer_churn_scores",engine,if_exists="replace",index=False)

print("✅ Churn scores saved into database")
