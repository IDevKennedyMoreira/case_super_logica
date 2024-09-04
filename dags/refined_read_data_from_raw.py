from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, TimestampType, IntegerType


"""
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
Ao   executar este  script ele lerá  todos   os  arquivos   parquet dentro  da da   pasta  raw e gerará
o  dataframe de  OBT (One Big Table),   que é  a   forma de  modalegem mais   simples  que escolhi para
a execução desse projeto devido ao tempo de entrega,  e também salvará a dataframe resultante na camada
refined.
"""

"""
Inicializa variáveis que serão utilizadas por todo o fluxo.
"""
def start_up():
    
    global spark
    spark = SparkSession.builder.appName("case_super_logica").getOrCreate()

"""
Definindo os schemas de leitura dos dataframes de entrada da camada raw.
"""
def defining_schemas():

    schema_townhouse = StructType()                              \
                       .add("condominio_id", StringType())       \
                       .add("condominio_nome", StringType())     \
                       .add("condominio_endereco", StringType())

    schema_property = StructType()                        \
                      .add("imovel_id", StringType())     \
                      .add("tipo", StringType())          \
                      .add("condominio_id", StringType()) \
                      .add("valor", IntegerType())

    schema_residents = StructType()                       \
                       .add("morador_id", StringType())   \
                       .add("morador_nome", StringType()) \
                       .add("condominio_id", StringType())\
                       .add("data_registro",TimestampType())

    schema_transactions = StructType()                           \
                          .add("transacao_id", StringType())     \
                          .add("morador_id", StringType())       \
                          .add("transacao_valor", IntegerType()) \
                          .add("imovel_id", StringType())        \
                          .add("data_transacao",TimestampType())
                          
    return schema_townhouse, schema_property, schema_residents, schema_transactions


def reading_dataframes(schema_townhouse, schema_property, schema_residents, schema_transactions):

    df_townhouse = spark.read.option("header","true")          \
                   .schema(schema_townhouse)                   \
                   .option("recursiveFileLookup","true")       \
                   .parquet("../datalake/raw/dim_condominios")
    df_townhouse.show()
    
    df_property =  spark.read.option("header","true")      \
                   .schema(schema_property)                \
                   .option("recursiveFileLookup","true")   \
                   .parquet("../datalake/raw/dim_imoveis")
    df_property.show()
    
    df_transacoes =  spark.read.option("header","true")       \
                   .schema(schema_transactions)               \
                   .option("recursiveFileLookup","true")      \
                   .parquet("../datalake/raw/fat_transacoes")
    df_transacoes.show()
                   
    df_residents =  spark.read.option("header","true")        \
                   .schema(schema_residents)                  \
                   .option("recursiveFileLookup","true")      \
                   .parquet("../datalake/raw/dim_moradores")
    df_residents.show()

    return df_townhouse, df_property, df_transacoes, df_residents

def renaming_columns(df_property):
    
    df_property = df_property.withColumnRenamed("valor","imovel_valor")\
                             .withColumnRenamed("tipo","imovel_tipo")
    
    return df_property
    

def generate_obt(df_transacoes, df_property, df_residents, df_townhouse):
    
    df_obt = df_transacoes.alias("t")                                                                \
             .join(df_property.alias("p"),df_property.imovel_id ==  df_transacoes.imovel_id,"inner") \
             .select("t.transacao_id",
                     "t.morador_id",
                     "t.transacao_valor",
                     "t.imovel_id",
                     "t.data_transacao",
                     "p.imovel_tipo",
                     "p.condominio_id",
                     "p.imovel_valor")
  
    
    
    df_obt = df_obt.alias("o")                                                                    \
             .join(df_residents.alias("r"), df_obt.morador_id == df_residents.morador_id,"inner") \
             .select("o.transacao_id",
                     "o.morador_id",
                     "o.transacao_valor",
                     "o.imovel_id",
                     "o.imovel_tipo",
                     "o.condominio_id",
                     "o.imovel_valor",
                     "o.data_transacao",
                     "r.morador_nome",
                     "r.data_registro")
             
    df_obt = df_obt.alias("o")                                                                         \
             .join(df_townhouse.alias("t"), df_obt.condominio_id == df_townhouse.condominio_id,"inner")\
             .select("o.transacao_id",
                     "o.morador_id",
                     "o.transacao_valor",
                     "o.imovel_id",
                     "o.imovel_tipo",
                     "o.condominio_id",
                     "o.imovel_valor",
                     "o.data_transacao",
                     "o.morador_nome",
                     "o.data_registro",
                     "t.condominio_nome",
                     "t.condominio_endereco")
    return df_obt

def upsert_parquet_file(df_obt):
    df_obt_bkp = df_obt
    
    
    try:
        schema_old_obt = StructType()                          \
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

        old_obt = spark.read.option("header","true")          \
                  .schema(schema_old_obt)                     \
                  .option("recursiveFileLookup","true")       \
                  .parquet("../datalake/refined")
  
        df_obt = df_obt.join(old_obt, on=['transacao_id'],how="left_anti")
    
        df_obt.coalesce(1).write.format("parquet").mode("append").save("../datalake/refined")
        
    
    except Exception as error: 
        
        df_obt_bkp.coalesce(1).write.format("parquet").mode("overwrite").save("../datalake/refined")
        

def main():
    
    start_up()
    
    schema_townhouse, schema_property, schema_residents, schema_transactions = defining_schemas()
    
    df_townhouse, df_property, df_transacoes, df_residents = reading_dataframes(schema_townhouse, schema_property, schema_residents, schema_transactions)
    
    df_property = renaming_columns(df_property)
    
    df_obt = generate_obt(df_transacoes, df_property, df_residents, df_townhouse)
    
    upsert_parquet_file(df_obt)
    
    
if __name__== "__main__":
    main()    

