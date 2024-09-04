from airflow import DAG
import pendulum
from airflow.operators.python import PythonOperator
from landing_read_data_from_external import main as landing_read_data_from_external
from raw_read_data_from_landing import main as raw_read_data_from_landing

"""
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
Essa é nossa DAG de execução eo nosso projeto porém como foi feita em computador local  usando 
sqlite ela não conseguirá executar os scripts paralelamente gerando gargalos na pipeline porém 
deixarei essa DAG montada para finalidade de consulta do fluxo da pipeline.
"""
with DAG(
        "superlogica_data_pipeline",
        start_date=pendulum.datetime(2022, 8, 22, tz="UTC"),
        schedule_interval='0 17 * * *',
    ) as dag:

    def run_raw_read_data_from_landing_condominios():
        raw_read_data_from_landing("../datalake/landing/dim_condominios")
    
    def run_raw_read_data_from_landing_moradores():
        raw_read_data_from_landing("../datalake/landing/dim_moradores")
        
    def run_raw_read_data_from_landing_imoveis():
        raw_read_data_from_landing("../datalake/landing/dim_propriedades")
    
    def run_raw_read_data_from_landing_transacoes():
        raw_read_data_from_landing("../datalake/landing/dim_transacoes")

    task_landing_read_data_from_external = PythonOperator(
        task_id = 'landing_read_data_from_external',
        python_callable = landing_read_data_from_external,
    )
    
    task_raw_read_data_from_landing_condominios = PythonOperator(
        task_id = 'raw_read_data_from_landing_condominios',
        python_callable = run_raw_read_data_from_landing_condominios
    )
    
    task_raw_read_data_from_landing_moradores = PythonOperator(
        task_id = 'raw_read_data_from_landing_moradores',
        python_callable = run_raw_read_data_from_landing_moradores
    )
    
    task_raw_read_data_from_landing_imoveis = PythonOperator(
        task_id = 'raw_read_data_from_landing_imoveis',
        python_callable = run_raw_read_data_from_landing_imoveis
    )
    
    task_raw_read_data_from_landing_transacoes = PythonOperator(
        task_id = 'raw_read_data_from_landing_transacoes',
        python_callable = run_raw_read_data_from_landing_transacoes
    )
    
    """
    Orquestração das tasks acima definidas
    """
    task_landing_read_data_from_external>>task_raw_read_data_from_landing_condominios
    task_landing_read_data_from_external>>task_raw_read_data_from_landing_moradores
    task_landing_read_data_from_external>>task_raw_read_data_from_landing_imoveis
    task_landing_read_data_from_external>>task_raw_read_data_from_landing_transacoes
    