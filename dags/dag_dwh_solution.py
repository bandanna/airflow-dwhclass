from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from load import load_data
from datetime import datetime, timedelta
import os


default_args = {

# TO BE FILLED ...

}

# UNCOMMENT THE LINE BELOW AND CREATE YOUR DAG OBJECT WITH THE SUITABLE CRON TIME 
# dag = 


# YOU POSTGRES QUERY NEEDS TO READ THE QUERY FROM queries/create_tables.sql, HERE HOW YOU DO THIS, USE sql_query where required
sql_ref = open('{dir_path}/queries/{query_file}'.format(dir_path=os.path.dirname(os.path.realpath(__file__)),query_file='create_tables.sql'),'r')
sql_query=sql_ref.read()


# THE PYTHON FUNCTION YOU'RE LOOKING FOR IS CALLED load_data