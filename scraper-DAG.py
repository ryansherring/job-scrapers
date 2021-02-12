from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
# from airflow.utils.dates import days_ago
from airflow.utils.timezone import datetime

from linkedin import run_scraper

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 2, 21),
    'email': ['ryansherring@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': True,
    'retries':1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'scraper_dag',
    default_args=default_args,
    description='pulls jobs from selected sites on a schedule',
    #schedule below
    schedule_interval=timedelta(weeks=1)
)

run_scraper = PythonOperator(
    task_id='run_scraper',
    python_callable=run_scraper,
    dag=dag
)

run_scraper # >> next_task >> next_task