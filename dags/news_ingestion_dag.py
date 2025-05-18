from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add scripts directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from fetch_news_and_upload_to_s3 import fetch_and_upload_to_s3
from download_latest_from_s3 import download_latest_from_s3
from load_news_to_postgres import load_data_to_postgres

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='news_ingestion_pipeline',
    default_args=default_args,
    description='Fetch news data, upload to S3, and download latest file daily',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # Run every day
    catchup=False,
    tags=['news', 'ETL', 'S3', "postgres"],
) as dag:

    # Task to fetch news from API and upload it to S3
    fetch_and_upload_news = PythonOperator(
        task_id='fetch_and_upload_to_s3',
        python_callable=fetch_and_upload_to_s3
    )

    # Task to download the latest news file from S3
    download_latest_news = PythonOperator(
        task_id='download_latest_from_s3',
        python_callable=download_latest_from_s3,
    )

    # Task to load the news data to postgres db
    load_to_postgres = PythonOperator(
        task_id='load_data_to_postgres',
        python_callable=load_data_to_postgres,
    )

    # Set task dependencies
    fetch_and_upload_news >> download_latest_news >> load_to_postgres
