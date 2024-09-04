from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
import threading

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


def work_streaming_townhouse():
    spark = SparkSession.builder.appName("streaming_surlogica_data_1").getOrCreate()
    input_path_townhouse = "./datalake/landing/dim_condominios"
    schema_townhouse = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")
    inputDF = spark.readStream\
                    .format("csv")\
                    .schema(schema_townhouse)\
                    .option("maxFilesPerTrigger", 10)\
                    .option("header","true")\
                    .csv(input_path_townhouse)
    query = inputDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake_for_stream/raw/dim_condominios").start("./datalake_for_stream/raw/dim_condominios")
    query.awaitTermination()
    
def work_streaming_property():
    spark = SparkSession.builder.appName("streaming_surlogica_data").getOrCreate()
    schema_property = StructType().add("imovel_id", "string").add("tipo", "string").add("condominio_id", "string").add("valor", "string")
    input_path_property = "./datalake/landing/dim_imoveis"
    inputDF = spark.readStream\
                    .format("csv")\
                    .schema(schema_property)\
                    .option("maxFilesPerTrigger", 10)\
                    .option("header","true")\
                    .csv(input_path_property)
    query = inputDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake_for_stream/raw/dim_imoveis").start("./datalake_for_stream/raw/dim_imoveis")
    query.awaitTermination()
    
def work_streaming_resident():
    spark = SparkSession.builder.appName("streaming_surlogica_data").getOrCreate()
    schema_property = StructType().add("morador_id", "string").add("morador_nome", "string").add("condominio_id", "string").add("data_registro", "string")
    input_path_property = "./datalake/landing/dim_moradores"
    inputDF = spark.readStream\
                    .format("csv")\
                    .schema(schema_property)\
                    .option("maxFilesPerTrigger", 10)\
                    .option("header","true")\
                    .csv(input_path_property)
    query = inputDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake_for_stream/raw/dim_moradores").start("./datalake_for_stream/raw/dim_moradores")
    query.awaitTermination()
    
def work_streaming_transaction():
    spark = SparkSession.builder.appName("streaming_surlogica_data").getOrCreate()
    schema_property = StructType().add("transacao_id", "string").add("transacao_valor", "string").add("morador_id", "string").add("data_transacao", "string")
    input_path_property = "./datalake/landing/fat_transacoes"
    inputDF = spark.readStream\
                    .format("csv")\
                    .schema(schema_property)\
                    .option("maxFilesPerTrigger", 10)\
                    .option("header","true")\
                    .csv(input_path_property)
    query = inputDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake_for_stream/raw/fat_transacoes").start("./datalake_for_stream/raw/fat_transacoes")
    query.awaitTermination()
    
streaming_condominios = threading.Thread(name='child_tread_townhouse', target=work_streaming_townhouse)
streaming_condominios.start()

streaming_property = threading.Thread(name='child_tread_property', target=work_streaming_property)
streaming_property.start()

streaming_resident = threading.Thread(name='childs_tread_resident', target=work_streaming_resident)
streaming_resident.start()

streaming_transaction = threading.Thread(name='childs_tread_transaction', target=work_streaming_transaction)
streaming_transaction.start()
    
    