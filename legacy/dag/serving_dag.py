from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import psycopg2
import mysql.connector
import numpy as np
import sys

sys.path.insert(0, '/opt/airflow/code')
from src.serving_utils import (
    preprocess_query, generate_query_embedding, generate_response_from_llm, retrieve_relevant_papers, return_response
)

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 11, 17),  # Adjust this to the desired start date
}

# Define the DAG
dag = DAG(
    'llm_serving_dag',
    default_args=default_args,
    description='DAG for chatbot query handling and retraining',
    schedule_interval=None,
    catchup=False
)

# Task 1: Preprocess User Query
preprocess_query_task = PythonOperator(
    task_id='preprocess_query',
    python_callable=preprocess_query,
    op_args=["{{ dag_run.conf['query'] }}"],  # Passing query from the trigger (e.g., via an external system)
    provide_context=True,
    dag=dag,
)

# Task 2: Generate Query Embedding
generate_query_embedding_task = PythonOperator(
    task_id='generate_query_embedding',
    python_callable=generate_query_embedding,
    op_args=["{{ task_instance.xcom_pull(task_ids='preprocess_query') }}"],  # Pass processed query from previous task
    provide_context=True,
    dag=dag,
)

# Task 3: Retrieve Relevant Information from Vector DB
retrieve_relevant_papers_task = PythonOperator(
    task_id='retrieve_relevant_papers',
    python_callable=retrieve_relevant_papers,
    op_args=["{{ task_instance.xcom_pull(task_ids='generate_query_embedding') }}"],  # Pass query embedding
    provide_context=True,
    dag=dag,
)

# Task 4: Generate Response from LLM
generate_response_from_llm_task = PythonOperator(
    task_id='generate_response_from_llm',
    python_callable=generate_response_from_llm,
    op_args=["{{ task_instance.xcom_pull(task_ids='retrieve_relevant_papers') }}"],  # Pass relevant papers
    provide_context=True,
    dag=dag,
)

# Task 5: Return Response to User
return_response_task = PythonOperator(
    task_id='return_response_to_user',
    python_callable=return_response,
    op_args=["{{ task_instance.xcom_pull(task_ids='generate_response_from_llm') }}"],  # Pass response
    provide_context=True,
    dag=dag,
)


# Dag Dependencies
preprocess_query_task >> generate_query_embedding_task >> retrieve_relevant_papers_task >> generate_response_from_llm_task >> return_response_task