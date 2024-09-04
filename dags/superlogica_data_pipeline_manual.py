from landing_read_data_from_external import main as landing_read_data_from_external
from raw_read_data_from_landing import main as raw_read_data_from_landing
from refined_read_data_from_raw import main as refined_read_data_from_raw
from trusted_read_data_from_refined import main as trusted_read_data_from_refined

"""
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
Orquestração manual da pipeline fora do Airflow para criar facilidades de testes.
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