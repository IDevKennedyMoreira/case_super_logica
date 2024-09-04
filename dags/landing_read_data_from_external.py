from models.datagenerator import DataGenerator
from pathlib import Path

"""
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
Ao executar este script serão executadas rotinas que simularão a ingestão de arquivos .csv
toda essa  simulação de dados é gerada  pela classe DataGenerador presente no arquivo data
generator na pastade models desse mesmo  repositório.  Desta forma serão  criados arquivos
dentro             da     camada             de            landing         do    datalake.
"""

"""
    Inicializa variáveis que serão utilizadas por todo o fluxo
"""
def start_up():
    
    global dg
    dg = DataGenerator("./datalake/landing/dim_condominios",50)
     
"""
    Executa criação de arquivos e faz a simulação de ingestão para a camada de landing do 
    datalake
"""
def work():
    
    dg.create_townhouse_file()
    
    dg.create_property_file()
    
    dg.create_resident_file()
    
    dg.create_transaction_file()
    
      
"""
    Orquestração do script de criação de simulação de entrada de dados 
"""
def main():
    
    start_up()
    
    work()
 
if __name__== "__main__":
    main()
