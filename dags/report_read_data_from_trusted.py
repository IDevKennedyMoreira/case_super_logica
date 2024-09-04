from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, TimestampType, IntegerType
from pyspark.sql.functions import sum

""" 
                                🆂🆄🅿🅴🆁🅻🅾🅶🅸🅲🅰
Documentação:
Resposta da questão 3 do case gerando os relatórios na pasta de reports
"""

"""
Inicializa variáveis que serão utilizadas por todo o fluxo.
"""
def start_up():
    
    global spark
    spark = SparkSession.builder.appName("case_super_logica").getOrCreate()
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    
    schema_trusted = StructType()                          \
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
    

    global df_trusted    
    df_trusted = spark.read.option("header","true")            \
                   .schema(schema_trusted)                     \
                   .option("recursiveFileLookup","true")       \
                   .parquet("../datalake/trusted")
"""
Aplica regras de negócio e cria os relatorios na pasta de report
"""
def work():
    
    df_agg_sum_transactions_by_townhouse = df_trusted.groupBy("condominio_id").agg(sum("transacao_valor"))
    df_agg_sum_transactions_by_townhouse.write.format("parquet").mode("overwrite").save("../reports/transactions_by_townhouse")
    
    df_agg_sum_transactions_by_resident = df_trusted.groupBy("morador_id").agg(sum("transacao_valor"))
    df_agg_sum_transactions_by_resident.write.format("parquet").mode("overwrite").save("../reports/transactions_by_resident")
    
    df_agg_transaction_by_type = df_trusted.groupBy(["imovel_tipo", "data_transacao" ]).agg(sum("transacao_valor"))
    df_agg_transaction_by_type.write.format("parquet").mode("overwrite").save("../reports/transaction_date_by_property_type")


def main():
    
    start_up()
    
    work()

if __name__=="__main__":
    
    main()

    
