from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator


with DAG(
            'meu_primeiro_dag',
            start_date=days_ago(1),
            schedule_interval='@daily'
) as dag:

        tarefa_1 = EmptyOperator(task_id = 'tarefa_1')
        tarefa_2 = EmptyOperator(task_id = 'tarefa_2')
        tarefa_3 = EmptyOperator(task_id = 'tarefa_3')
        tarefa_1 >> [tarefa_2, tarefa_3]
