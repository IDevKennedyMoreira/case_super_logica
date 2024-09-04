import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from landing_read_data_from_external import main as landing_read_data_from_external
from raw_read_data_from_landing import main as raw_read_data_from_landing
from refined_read_data_from_raw import main as refined_read_data_from_raw
from trusted_read_data_from_refined import main as trusted_read_data_from_refined
import os

"""
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
DAG de orquestração do projeto no Airflow.
"""

os.chdir('./dags') #Definindo pasta de execução

with DAG(
        "superlogica_data_pipeline",
        start_date=pendulum.datetime(2022, 8, 22, tz="UTC"),
        schedule_interval="0 17 * * *",
    ) as dag:

    def run_raw_read_data_from_landing_condominios():
        raw_read_data_from_landing("../datalake/landing","dim_condominios")
    
    def run_raw_read_data_from_landing_moradores():
        raw_read_data_from_landing("../datalake/landing","dim_moradores")
        
    def run_raw_read_data_from_landing_imoveis():
        raw_read_data_from_landing("../datalake/landing","dim_imoveis")
    
    def run_raw_read_data_from_landing_transacoes():
        raw_read_data_from_landing("../datalake/landing","fat_transacoes")
    
    def run_refined_read_data_from_raw():
        refined_read_data_from_raw()
    
    def run_trusted_read_data_from_refined():
        trusted_read_data_from_refined()

    t1 = PythonOperator(
        task_id = "landing_read_data_from_external",
        python_callable = landing_read_data_from_external,
    )
    
    t2_1 = PythonOperator(
        task_id = "raw_read_data_from_landing_condominios",
        python_callable = run_raw_read_data_from_landing_condominios
    )
    
    t2_2 = PythonOperator(
        task_id = "raw_read_data_from_landing_moradores",
        python_callable = run_raw_read_data_from_landing_moradores
    )
    
    t2_3 = PythonOperator(
        task_id = "raw_read_data_from_landing_imoveis",
        python_callable = run_raw_read_data_from_landing_imoveis
    )
    
    t2_4 = PythonOperator(
        task_id = "raw_read_data_from_landing_transacoes",
        python_callable = run_raw_read_data_from_landing_transacoes
    )
    
    t3 = PythonOperator(
        task_id = "refined_read_data_from_raw",
        python_callable = run_refined_read_data_from_raw
    )
    
    t4 = PythonOperator(
        task_id = "trusted_read_data_from_refined",
        python_callable = run_trusted_read_data_from_refined
    )
    
    """
    Orquestração das tasks acima definidas.
    """
    t1>>t2_1>>t3>>t4
    t1>>t2_2>>t3>>t4
    t1>>t2_3>>t3>>t4
    t1>>t2_4>>t3>>t4
    