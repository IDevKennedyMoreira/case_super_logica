from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

spark = SparkSession.builder.appName("StreamingExample").getOrCreate()

schema = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")
inputPath = "./datalake/landing"
inputDF = spark.readStream.format("csv").schema(schema).format("csv").option("maxFilesPerTrigger", 1).option("header","true").csv(inputPath)

transformedDF = inputDF

query = transformedDF.writeStream.outputMode("append").format("parquet").option("checkpointLocation", "./datalake/raw/dim_condominios/_checkpoint").start("./datalake/raw/dim_condominios")

query.awaitTermination()