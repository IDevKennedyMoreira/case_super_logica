from models import DataGenerator
from pathlib import Path

"""
    Documentação:

        Ao executar este script serão executadas rotinas que simularão a ingestão de arquivos .csv
        para dentro da camada de landing do datalake
"""

"""
    Inicializa variáveis que serão utilizadas por todo o fluxo
"""
def start_up():
    
    global dg
    dg = DataGenerator("./datalake/landing/dim_condominios")

        

"""
    Executa criação de arquivos e faz a simulação de ingestão para a camada de landing do datalake
"""
def work():
    
    dg.create_townhouse_file()
    
    dg.create_property_file()
    
    dg.create_resident_file()
    
      
"""
    Orquestração do script de ingestão
"""
def main():
    
    start_up()
    
    work()
 
if __name__== "__main__":
    main()
