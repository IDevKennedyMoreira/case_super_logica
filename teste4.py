from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

# Initialize a Spark session
spark = SparkSession.builder.appName("StreamingExample").getOrCreate()

# Create a DataFrame from a streaming source (e.g., Kafka)
schema = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")
inputPath = "./datalake/landing"
inputDF = spark.readStream.format("csv").schema(schema).format("csv").option("maxFilesPerTrigger", 1).csv(inputPath)

# Define some transformation on the input data
transformedDF = inputDF.selectExpr("CAST(condominio_id AS STRING) AS message")

# Write the transformed data to an output sink (e.g., console)
query = transformedDF.writeStream.outputMode("append").format("console").start()

# Wait for the query to terminate
query.awaitTermination()