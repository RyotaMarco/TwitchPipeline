from pyspark.sql import SparkSession
from pyspark.sql.types import *
import os
from datetime import datetime
from utils.log import *

logger = get_logger("twitch_ETL")

json_file = os.getenv("JSON_FILE_PATH")
if json_file is None:
     logger.error("JSON_FILE_PATH não está definida no ambiente!")
     raise

if not os.path.exists(json_file):
    logger.error(f"O arquivo {json_file} não existe!")
    raise


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
parquet_base_path = os.getenv("PARQUET_FILE_PATH")
if parquet_base_path is None:
    logger.error("PARQUET_FILE_PATH não está definida no ambiente!")
    raise


os.makedirs(parquet_base_path, exist_ok=True)


parquet_file = os.path.join(parquet_base_path, f"streams_data_{timestamp}.parquet")


spark = SparkSession.builder \
    .appName("Twitch data pipeline") \
    .config("spark.some.config.option", "some value") \
    .getOrCreate()


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


logger.info(f"Lendo arquivo JSON: {json_file}")
df = spark.read.schema(schema).json(json_file)


logger.info("Exemplo dos dados lidos:")
df.show(5)
logger.info("Schema dos dados:")
df.printSchema()


logger.info(f"Salvando arquivo Parquet em: {parquet_file}")
df.write \
    .mode("overwrite") \
    .partitionBy("user_id") \
    .parquet(parquet_file)

logger.info("Conversão concluída com sucesso!")


spark.stop()