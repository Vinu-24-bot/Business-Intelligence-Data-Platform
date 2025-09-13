CREATE SCHEMA IF NOT EXISTS bi;

-- Core tables
CREATE TABLE IF NOT EXISTS customers (
  customer_id       INT PRIMARY KEY,
  name              TEXT,
  age               INT,
  gender            TEXT,
  location          TEXT,
  total_purchase    NUMERIC(12,2),
  last_purchase_date DATE,
  churn_label       INT
);

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id    INT PRIMARY KEY,
  customer_id       INT REFERENCES customers(customer_id),
  product_category  TEXT,
  payment_method    TEXT,
  amount            NUMERIC(12,2),
  transaction_date  DATE
);

-- ML outputs
CREATE TABLE IF NOT EXISTS customer_churn_scores (
  customer_id INT PRIMARY KEY,
  churn_probability NUMERIC(6,5)
);

CREATE TABLE IF NOT EXISTS sales_forecast (
  forecast_date DATE PRIMARY KEY,
  predicted_sales NUMERIC(14,2)
);

-- Indexes for dashboard filters/joins
CREATE INDEX IF NOT EXISTS idx_txn_customer_id ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_txn_date ON transactions(transaction_date);

-- BI views
CREATE OR REPLACE VIEW bi.monthly_sales AS
SELECT date_trunc('month', transaction_date)::date AS month_start,
       SUM(amount) AS total_sales
FROM transactions
GROUP BY 1
ORDER BY 1;

-- Optional: materialized view for faster refresh on large data
CREATE MATERIALIZED VIEW IF NOT EXISTS bi.monthly_sales_mview AS
SELECT date_trunc('month', transaction_date)::date AS month_start,
       SUM(amount) AS total_sales
FROM transactions
GROUP BY 1
WITH NO DATA;  -- populate in a refresh step
