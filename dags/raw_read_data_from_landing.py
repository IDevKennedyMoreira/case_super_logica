from pyspark.sql import SparkSession
import glob
import os
import re

"""
    Documentação:

        Ao executar este script ele lerá o ultimo csv gerado na camada landing e os converterá para formato parquet
"""

"""
    Inicializa variáveis que serão utilizadas por todo o fluxo
"""
def start_up(folder_origin):
    
    global spark
    spark = SparkSession.builder.appName("CSV to Parquet").getOrCreate()

    list_of_files = glob.glob(f'{folder_origin}/*')
    
    global folder_destiny
    folder_destiny = folder_origin.replace('landing','raw')
    
    global latest_file
    latest_file = max(list_of_files, key=os.path.getctime)
    
    print(latest_file)
    
    global document_fingerprint
    document_fingerprint = re.findall("\d+", latest_file)[0]

"""
Lê arquivo em formato csv e o salva como parquet na camada raw
"""
def work():
    
    df = spark.read.csv(latest_file, header=True, inferSchema=True)

    df.write.parquet(f"{folder_destiny}{document_fingerprint}.parquet","overwrite")

"""
    Orquestração do script de ingestão
"""
def main(folder_origin):
    
    start_up(folder_origin)
    
    work()
    
if __name__== "__main__":
    main()