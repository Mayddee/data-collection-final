from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys, os
sys.path.append('/Users/amangeldimadina/Desktop/data-gathering/data-final/src')

from job2_cleaner import kafka_to_sqlite



with DAG('dag2_cleaning', schedule_interval='@hourly', start_date=datetime(2025, 1, 1), catchup=False) as dag:
    PythonOperator(task_id='kafka_to_db', python_callable=kafka_to_sqlite)