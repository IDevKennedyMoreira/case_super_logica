from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('abc').getOrCreate()

df = spark.read.csv("datalake/landing/imoveis08312024005826.csv")

# Displays the content of the DataFrame to stdout
df.show()

df.write.parquet("datalake/raw/proto.parquet")