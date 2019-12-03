from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from load import load_data
from datetime import datetime, timedelta
import os

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 12, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("dwh_class_example", default_args=default_args, schedule_interval='5 5 * * *')

t_start= DummyOperator(task_id='start',dag=dag)

def say_hi():
    return 'hello world!'

sql_query="""select * from products;"""

t_python=PythonOperator(task_id='say_hi_python',
                        python_callable=say_hi,
                        dag=dag)

t_postgres=PostgresOperator(task_id='run_query_postgres',postgres_conn_id='mydb', sql=sql_query, dag=dag)

t_end=DummyOperator(task_id='end',dag=dag)

t_start >> t_python >> t_postgres >> t_end
