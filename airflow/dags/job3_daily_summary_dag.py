from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys, os
sys.path.append('/Users/amangeldimadina/Desktop/data-gathering/data-final/src')

from job3_analytics import run_analytics_and_report


with DAG('dag3_analytics', schedule_interval='@daily', start_date=datetime(2025, 1, 1), catchup=False) as dag:
    PythonOperator(task_id='generate_report', python_callable=run_analytics_and_report)