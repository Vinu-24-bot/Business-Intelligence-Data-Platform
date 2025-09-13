from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "bi-platform",
    "depends_on_past": False,
}

with DAG(
    dag_id="bi_platform",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["bi", "retail"],
) as dag:

    gen = BashOperator(
        task_id="generate_data",
        bash_command="python /opt/airflow/scripts/generate_data.py",
    )

    schema = BashOperator(
        task_id="create_schema",
        bash_command="python /opt/airflow/scripts/create_schema.py",
    )

    load = BashOperator(
        task_id="load_data",
        bash_command="python /opt/airflow/scripts/load_data.py",
    )

    churn = BashOperator(
        task_id="train_churn",
        bash_command="python /opt/airflow/scripts/train_churn.py",
    )

    forecast = BashOperator(
        task_id="train_forecast",
        bash_command="python /opt/airflow/scripts/train_forecast.py",
    )

    refresh = BashOperator(
        task_id="refresh_views",
        bash_command="python /opt/airflow/scripts/build_views.py",
    )

    gen >> schema >> load >> [churn, forecast] >> refresh
