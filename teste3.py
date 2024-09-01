from pyspark.sql.functions import *
from pyspark.sql.types import StructType
from pyspark.sql.types import StructType
from pyspark.sql import SparkSession

inputPath = "./datalake/landing"

spark = SparkSession.builder.appName("Stream CSV to Parquet").getOrCreate()
# Let's first define the schema before reading the data
schema = StructType().add("condominio_id", "string").add("condominio_nome", "string").add("condominio_endereco", "string")

# Using readStream instead of read on streaming data
streamingInputDF = (
  spark
    .readStream                       
    .schema(schema)               # Set the schema of the JSON data
    .option("maxFilesPerTrigger", 1)  # Treat a sequence of files as a stream by picking one file at a time
    .json(inputPath)
)

# Same query as staticInputDF
streamingWriteDF = (                 
  streamingInputDF
    .format("parquet")          # Can be "orc", "json", "csv", etc.
    .option("path", "path/to/destination/dir")
    .start()
)