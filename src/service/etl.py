from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType
import os
from datetime import datetime
from src.utils.log import *

class PySparkETL:
    '''
    Make ETL with PySpark in JSON files from Twitch API
    '''
    def __init__(self):
            self.logger = get_logger("twitch_api_request")
            self.base_url = os.getenv("BASE_URL")


    def load_json_file(self, json_file):
        json_file = f'{os.getenv("JSON_FILE_PATH")}/*.json'
        if json_file is None:
            self.logger.error("JSON_FILE_PATH não está definida no ambiente!")
            raise

        if not os.path.exists(json_file):
            self.logger.error(f"O arquivo {json_file} não existe!")
            raise
        return json_file

    
    def spark_session(self, app_name="Twitch data pipeline"):
        self.logger.info("Inicializando o SparkSession")
        spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.some.config.option", "some value") \
            .getOrCreate()
        return spark


    def get_schema(self):
        self.logger.info("Realizando a estruturação do parquet.")
        schema = StructType([
            StructField("user_id", StringType(), True),
            StructField("user_name", StringType(), True),
            StructField("stream_id", StringType(), True),
            StructField("viewer_count", IntegerType(), True),
            StructField("game_name", StringType(), True),
            StructField("started_at", StringType(), True),
            StructField("is_mature", BooleanType(), True),
            StructField("thumbnail_url", StringType(), True)
        ])
        return schema


    def read_json(self, spark, json_path, schema):
        self.logger.info(f"Lendo arquivo JSON:{json_path}")
        df = spark.read.schema(schema).json(json_path)
        return df


    def clean_data(self, df):
        """
        Remove duplicate data and null 
        """
        self.logger.info("Limpando dados do data frame: Dados nulos e duplicados")

        total = df.count()


        df_null = df.dropna(subset=["user_id","stream_id", "viewer_count"])
        total_null = df_null.count()

        df_clean = df_null.dropDuplicates(["user_id","stream_id"])
        total_final = df_clean.count()

        self.logger.info(f"Registros iniciais: {total}")
        self.logger.info(f"Registros após remover nulos: {total_null}")
        self.logger.info(f"Registros após remover duplicados: {total_final}")

        return df_clean


    def parquet_transform(self, df, output_path, partition_col= None):
        self.logger.info("Transformando arquivo em parquet.")
        writer = df.write.mode("overwrite")
        if partition_col:
            writer = writer.partitionBy(partition_col)
        writer.parquet(output_path)


    def close_spark(self, spark):
        self.logger.info("Conversão concluída com sucesso!")
        spark.stop()