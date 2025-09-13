import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:admin123@localhost:5432/retail_analytics")

df = pd.read_sql("SELECT transaction_date, amount FROM transactions;", engine)
df["transaction_date"] = pd.to_datetime(df["transaction_date"])
monthly_sales = df.groupby(df["transaction_date"].dt.to_period("M"))["amount"].sum().to_timestamp()

model = ARIMA(monthly_sales, order=(1,1,1))
fit = model.fit()

forecast = fit.forecast(steps=6)
future_dates = pd.date_range(start=monthly_sales.index[-1]+pd.offsets.MonthBegin(), periods=6, freq="MS")

forecast_df = pd.DataFrame({"forecast_date": future_dates, "predicted_sales": forecast.values})
forecast_df.to_sql("sales_forecast", engine, if_exists="replace", index=False)

print(" Sales forecast saved into database")
