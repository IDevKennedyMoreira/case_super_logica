from landing_read_data_from_external import main as landing_read_data_from_external
from raw_read_data_from_landing import main as raw_read_data_from_landing

def main():

    landing_read_data_from_external()

    raw_read_data_from_landing("../datalake/landing/dim_condominios","dim_condominios")
    
    raw_read_data_from_landing("../datalake/landing/dim_moradores","dim_moradores")
    
    raw_read_data_from_landing("../datalake/landing/dim_imoveis","dim_imoveis")
    
    raw_read_data_from_landing("../datalake/landing/fat_transacoes","fat_transacoes")

if __name__== "__main__":
    main()