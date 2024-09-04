from pyspark.sql import SparkSession
import glob
import os
import re

"""
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
Ao executar este script ele lerá o ultimo csv gerado na camada landing e os converterá para 
o formato parquet e o salvará na camada raw do datalake.
"""

"""
Inicializa variáveis que serão utilizadas por todo o fluxo.
"""
def start_up(folder_origin, subfolder):
    
    global spark
    spark = SparkSession.builder.appName("case_super_logica").getOrCreate()
    
    global subfolder_destiny
    subfolder_destiny = subfolder

    list_of_files = glob.glob(f'{folder_origin}/{subfolder}/*')
    
    global folder_destiny
    folder_destiny = folder_origin.replace('landing','raw')
    
    global latest_file
    latest_file = max(list_of_files, key=os.path.getctime)
    
    global document_fingerprint
    document_fingerprint = re.findall("\d+", latest_file)[0]

"""
Lê arquivo em formato csv e o salva como parquet na camada raw.
"""
def work():
    
    df = spark.read.csv(latest_file, header=True, inferSchema=True)

    df.write.parquet(f"{folder_destiny}/{subfolder_destiny}/{document_fingerprint}.parquet","overwrite")

"""
    Orquestração do script de ingestão.
"""
def main(folder_origin, subfolder):
    
    start_up(folder_origin, subfolder)
    
    work()
    
if __name__== "__main__":
    main()