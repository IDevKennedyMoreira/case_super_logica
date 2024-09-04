from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, TimestampType, IntegerType

def start_up():
    
    global spark
    spark = SparkSession.builder.appName("case_super_logica").getOrCreate()
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    
    schema_refined = StructType()                          \
                    .add("transacao_id", StringType())     \
                    .add("morador_id", StringType())       \
                    .add("transacao_valor", IntegerType()) \
                    .add("imovel_id",StringType())         \
                    .add("imovel_tipo",StringType())       \
                    .add("condominio_id",StringType())     \
                    .add("imovel_valor",IntegerType())     \
                    .add("data_transacao",TimestampType()) \
                    .add("morador_nome",StringType())      \
                    .add("data_registro",TimestampType())  \
                    .add("condominio_nome",StringType())   \
                    .add("condominio_endereco",StringType())
    
    global schema_trusted
    schema_trusted = schema_refined
    
    global df_refined    
    df_refined = spark.read.option("header","true")            \
                   .schema(schema_refined)                     \
                   .option("recursiveFileLookup","true")       \
                   .parquet("../datalake/refined")


def insert_parquet_file(df_refined):
    df_refined_bkp = df_refined
    try:
        
        df_old_trusted = spark.read.option("header","true")         \
                        .schema(schema_trusted)                     \
                        .option("recursiveFileLookup","true")       \
                        .parquet("../datalake/trusted")
  
        df_refined = df_refined.join(df_old_trusted, on=['transacao_id'],how="left_anti")
    
        df_refined.coalesce(1).write.format("parquet").mode("append").save("../datalake/trusted")
    
    except Exception as error: 
        
        df_refined_bkp.coalesce(1).write.format("parquet").mode("overwrite").save("../datalake/trusted")

def main():
    
    start_up()
    
    insert_parquet_file(df_refined)
    
if __name__=="__main__":
    
    main()