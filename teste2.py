from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.streaming import StreamingContext
from pyspark import SparkContext


spark = SparkSession.builder.appName("Stream CSV to Parquet").getOrCreate()


# userSchema = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")

# streamingDF = spark.readStream           \
#                    .schema(userSchema)   \
#                    .format("csv")        \
#                    .option("path","./datalake/landing") \
#                    .load() 

ssc.textFileStream('./datalake/landing')
                   
spark.sparkContext.setLogLevel("DEBUG")

query = ssc.writeStream \
.trigger(availableNow=True) \
.outputMode("append") \
.format("parquet") \
.start("./datalake/raw/") # Replace with the path where you want to save the Delta table

ssc.start()             # Start the computation
ssc.awaitTermination()