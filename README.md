# AIBI-Project
project

AIBI-Project — Business Intelligence Data Platform
An end-to-end BI stack that loads synthetic retail data into PostgreSQL, orchestrates ETL and ML tasks with Airflow (Docker), and exposes clean tables/views for reporting in Power BI.

Highlights
PostgreSQL data warehouse with clean schemas and primary keys for fast joins and refresh.

Airflow DAG automates data generation, schema creation, loading, churn scoring, sales forecasting, and view refresh.

ML tasks: RandomForest churn scoring and ARIMA monthly sales forecasting saved back to the warehouse.

Directly connect BI tools to warehouse tables and views for Import or live-style dashboards.

Tech stack
SQL, Python (pandas, scikit-learn, statsmodels), SQLAlchemy, psycopg2.

PostgreSQL (warehouse).

Airflow (ETL orchestration, Dockerized).

Power BI (reporting).

Repository structure
text
AIBI-Project/
  .env.example
  docker-compose.yml
  requirements.txt
  airflow/
    dags/
      bi_platform_dag.py
  scripts/
    db_utils.py
    generate_data.py
    create_schema.py
    load_data.py
    train_churn.py
    train_forecast.py
    build_views.py
    sql/
      create_schema.sql
  data/
    raw/
What the pipeline does
generate_data.py: creates synthetic customers and transactions CSVs under data/raw for repeatable demos.

create_schema.py: builds warehouse schema, tables, indexes, and BI views/materialized views.

load_data.py: bulk loads the CSVs into PostgreSQL with proper keys and types.

train_churn.py: trains a RandomForest and writes churn_probability per customer to a scores table.

train_forecast.py: fits ARIMA on monthly sales and writes a 6‑month forecast.

build_views.py: refreshes the materialized view for faster dashboard queries.

Quickstart
Prereqs: Docker Desktop installed and running.

Copy env: cp .env.example .env.

Start stack: docker compose up -d.

Open Airflow: http://localhost:8080 → login airflow / airflow.

Enable DAG bi_platform and wait until the run turns green.

Data is ready in PostgreSQL: customers, transactions, customer_churn_scores, sales_forecast, and views under schema bi.

Configuration
.env holds Postgres and Airflow settings used by docker-compose and all scripts.

A single warehouse URL is exposed to scripts as WAREHOUSE_DB_URL for consistent connectivity.

Defaults are suitable for local development; adjust ports or credentials if needed.

Airflow DAG
DAG id: bi_platform, schedule: daily, catchup: false.

Task order: generate_data → create_schema → load_data → [train_churn, train_forecast] → refresh_views.

Tasks are Bash-based so they run the Python scripts inside the Airflow container.

Database schema
customers(customer_id PK, name, age, gender, location, total_purchase, last_purchase_date, churn_label).

transactions(transaction_id PK, customer_id FK, product_category, payment_method, amount, transaction_date).

customer_churn_scores(customer_id PK, churn_probability).

sales_forecast(forecast_date PK, predicted_sales).

Views: bi.monthly_sales and bi.monthly_sales_mview for monthly aggregates.

Connect with Power BI
In Power BI Desktop: Get Data → PostgreSQL database → Server: localhost, Database: retail_analytics.

Choose Import for fast modeling, or DirectQuery for near live behavior on views like bi.monthly_sales.

Select tables/views and load to start building visuals and measures.

Performance tips
Primary keys and indexes on transactions(customer_id) and transactions(transaction_date) improve join and filter performance.

The materialized view bi.monthly_sales_mview reduces aggregation time for month-level dashboards.

ML outputs are upserted to avoid duplicate key errors during scheduled runs.

Troubleshooting
Airflow up but tasks fail: open task logs to check Python stack traces and confirm env variables are present in the container.

Database empty: ensure generate_data and load_data succeeded, then rerun the DAG to repopulate.

Power BI cannot connect: confirm docker compose is running and Postgres port is exposed to localhost.

Scripts (reference)
generate_data.py: uses Faker to build realistic CSVs for customers and transactions.

load_data.py: uses psycopg2 COPY for fast bulk ingest of CSVs.

train_churn.py: RandomForestClassifier on age and total_purchase with predict_proba to compute churn_probability.

train_forecast.py: ARIMA(1,1,1) over monthly resampled sales for 6‑step ahead forecast.

Sample data columns
customers.csv: customer_id, name, age, gender, location, total_purchase, last_purchase_date, churn_label.

transactions.csv: transaction_id, customer_id, product_category, payment_method, amount, transaction_date.
