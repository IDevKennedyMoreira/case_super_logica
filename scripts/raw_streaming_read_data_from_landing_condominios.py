from pyspark.sql import SparkSession
from pyspark.sql.types import StructType


def start_up():
    
    global spark
    spark = SparkSession.builder.config('spark.executor.instances', 4).appName("Condominio_ingest").getOrCreate()
    
    global schema
    schema = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")
    
    global input_path
    input_path = "./datalake/landing/dim_condominios"
    
def work():

    inputDF = spark.readStream.format("csv").schema(schema).format("csv").option("maxFilesPerTrigger", 1).option("header","true").csv(input_path)

    transformedDF = inputDF
    
    print("Transferindo dados para a camada RAW")

    query = transformedDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake/raw/dim_condominios/_checkpoint").start("./datalake/raw/dim_condominios")

    
    query.awaitTermination()
    
def main():
    
    start_up()
    
    work()
    
if __name__=='__main__':
    main()