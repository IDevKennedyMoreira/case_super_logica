from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

""" 
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
O     motivo da     existência desse   arquivo     é    uma       resposta a    questão 4        do nosso case
infelizmente    não  tive tempo  hábil    para   escrever   toda  a pipeline     usando  Structured Streamings
porém   dei o  ponta pé inicial,  como pode   ver  esse    script consegue  a partir de  um  evento de criação
de   um arquivo  numa pasta,  nesse  caso  na  pasta   de  landing de  condominios,    startar o processamento
em    streaming usando  micro baching   ele  não   é   uma   resposta  completa ao  desafio,    mas como disse
anteriormente,   é   um ponto de  partida.   Para    aumento    de  escabilidade vertical    pode ser definido
um     maior número  de works a  partir    do  método    config de   Spark Session     e   também mais memória
RAM  para processamento,  já numa  estratégia  de  escala   horizontal é possível  executar  esse mesmo script
em  infra serverless em diversos clusters porém é necessário analisar  questões de  duplicicade e concorrência
de recursos (recomendo o uso de um  serviço de mensageria como kafka para uma estratégia de escala horizontal).
"""

"""
Inicializa variáveis que serão utilizadas por todo o fluxo
"""
def start_up():
        
    global spark
    spark = SparkSession.builder.appName("streaming_raw_data").getOrCreate()
    
    global schema_townhouse, schema_property, schema_residents, schema_transactions
    schema_townhouse = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")
  
    global input_path_townhouse
    input_path_townhouse = "./datalake/landing/dim_condominios"

"""
Inicia streaming de dados.
"""   
def work_streaming_townhouse():
    
    inputDF = spark.readStream.format("csv").schema(schema_townhouse).format("csv").option("maxFilesPerTrigger", 10).option("header","true").csv(input_path_townhouse)
    
    transformedDF = inputDF
    
    query = transformedDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake/raw/dim_condominios/_checkpoint").start("./datalake/raw/dim_condominios")
    
    query.awaitTermination()

"""
Orquestração do script de ingestão.
"""
def main():
    
    start_up()
    
    work_streaming_townhouse()
    
    
if __name__=='__main__':
    main()