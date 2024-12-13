from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import mysql.connector
import psycopg2
import numpy as np
import sys

sys.path.insert(0, '/opt/airflow/code')
from src.embeddings_utils import (
    scrape, clean, create_embeddings, upload_to_mysql, upload_to_vector_db
)

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1)
}

# Define the DAG
dag = DAG(
    'embeddings_dag',
    default_args=default_args,
    description='DAG for data ingestion: scraping, cleaning, and embedding data',
    #schedule_interval=timedelta(hours=6),  
    catchup=False
)

# Task 1: Scrape data
scrape_data_task = PythonOperator(
    task_id='scrape_data',
    python_callable=scrape,  # Function that performs the scraping
    dag=dag,
)

# Task 2: Clean scraped text
clean_text_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean,  # Function that cleans the text
    dag=dag,
)

# Task 3: Upload to MySQLdb
upload_to_mysql_task = PythonOperator(
    task_id='upload_to_mysql',
    python_callable=upload_to_mysql,
    dag=dag,
)

# Task 4: Create Embeddings
create_embeddings_task = PythonOperator(
    task_id='create_embeddings',
    python_callable=create_embeddings,
    dag=dag,
)


# Task 5: Upload to Vector DB
upload_to_vector_db_task = PythonOperator(
    task_id='upload_to_vector_db',
    python_callable=upload_to_vector_db,
    op_kwargs={'embeddings': "{{ task_instance.xcom_pull(task_ids='create_embeddings') }}"},
    dag=dag,
)


# Dag Dependencies
scrape_data_task >> clean_text_task >> [upload_to_mysql_task, create_embeddings_task]
create_embeddings_task >> upload_to_vector_db_task