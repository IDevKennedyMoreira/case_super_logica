from landing_read_data_from_external import main as landing_read_data_from_external
from raw_read_data_from_landing import main as raw_read_data_from_landing
from refined_read_data_from_raw import main as refined_read_data_from_raw
from trusted_read_data_from_refined import main as trusted_read_data_from_refined

"""
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
A   existência desse   arquivo se  deve  ao  fato  de   que  não consigo  fazer   orquestrações em paralelo
no  airflow pois estou rodando toda  a   solução  na   minha máquina  local, como   nesse  modo de execução
não    consigo alterar   o parâmetro  execute   no   arquivo   de configuração  do airflow    (ao menos que
instale  o banco localmente), disponibilizei  esse   arquivo  para  execução  local da    pipeline de dados
porém para demonstração a pipeline também estará visível no airflow com nome de superlogica_data_pipeline.
"""

"""
    Esta função define a ordem de execução da pipeline
"""
def main():

    landing_read_data_from_external()

    raw_read_data_from_landing("../datalake/landing","dim_condominios")
    
    raw_read_data_from_landing("../datalake/landing","dim_moradores")
    
    raw_read_data_from_landing("../datalake/landing","dim_imoveis")
    
    raw_read_data_from_landing("../datalake/landing","fat_transacoes")
    
    refined_read_data_from_raw()
    
    trusted_read_data_from_refined()

if __name__== "__main__":
    main()