import sys
import os
sys.path.append('/Users/amangeldimadina/Desktop/data-gathering/data-final/src')
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow import DAG

from job1_producer import stream_to_kafka


with DAG('dag1_ingestion', schedule_interval='*/5 * * * *', start_date=datetime(2025, 1, 1), catchup=False) as dag:
    PythonOperator(task_id='fetch_wazirx_api', python_callable=stream_to_kafka)