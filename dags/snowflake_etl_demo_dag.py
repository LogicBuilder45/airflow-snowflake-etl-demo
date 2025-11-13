from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

from src.load.snowflake_load import load_demo_data_to_snowflake

default_args = {
    "owner": "data_eng",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="snowflake_etl_demo",
    description="Simple Airflow → Snowflake ETL reference pipeline",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    tags=["snowflake", "etl", "demo"],
    # Adjust if your SQL is in a different path inside the container
    template_searchpath=["/opt/airflow/sql"],
) as dag:

    create_tables = SnowflakeOperator(
        task_id="create_tables",
        snowflake_conn_id="snowflake_default",
        sql="snowflake_ddl.sql",
    )

    load_raw = PythonOperator(
        task_id="load_raw",
        python_callable=load_demo_data_to_snowflake,
    )

    transform_data = SnowflakeOperator(
        task_id="transform_data",
        snowflake_conn_id="snowflake_default",
        sql="snowflake_transform.sql",
    )

    create_tables >> load_raw >> transform_data
