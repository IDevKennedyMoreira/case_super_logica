from pyspark.sql import SparkSession
from pyspark.sql.types import StructType


def start_up():
    global spark
    spark = SparkSession.builder.config('spark.executor.instances', 4).appName("streaming_raw_data").getOrCreate()
    global schema_townhouse, schema_property, schema_residents, schema_transactions
    schema_townhouse = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")
    schema_property = StructType().add("imovel_id", "string").add("tipo", "string").add("condominio_id", "string").add("valor", "string")
    schema_residents = StructType().add("morador_id", "string").add("morador_nome", "string").add("condominio_id", "string")
    schema_transactions = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")
    global input_path_townhouse, input_path_property, input_path_residents, input_path_transactions
    input_path_townhouse = "./datalake/landing/dim_condominios"
    input_path_property = "./datalake/landing/dim_imoveis"
    input_path_residents = "./datalake/landing/dim_moradores"
    input_path_transactions = "./datalake/landing/fat_transacoes"
    
def work_streaming_townhouse():
    inputDF = spark.readStream.format("csv").schema(schema_townhouse).format("csv").option("maxFilesPerTrigger", 10).option("header","true").csv(input_path_townhouse)
    transformedDF = inputDF
    query = transformedDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake/raw/dim_condominios/_checkpoint").start("./datalake/raw/dim_condominios")
    query.awaitTermination()
    
    
def work_streaming_property():
    inputDF = spark.readStream.format("csv").schema(schema_property).format("csv").option("maxFilesPerTrigger", 10).option("header","true").csv(input_path_property)
    transformedDF = inputDF
    query_property = transformedDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake/raw/dim_imoveis/_checkpoint").start("./datalake/raw/dim_imoveis")
    query_property.awaitTermination()
    
def main():
    
    start_up()
    
    work_streaming_townhouse()
    
    
if __name__=='__main__':
    main()