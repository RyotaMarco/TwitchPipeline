from pyspark.sql import SparkSession
from pyspark.sql.types import *

# Initialize Spark Session

spark = SparkSession.builder.appName("Twitch data pipeline").config("spark.some.config.option", "some value").getOrCreate()

schema = StructType([
    StructField("id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("user_name", StringType(), True),
    StructField("game_id", StringType(), True),
    StructField("game_name", StringType(), True),
    StructField("viewer_count", IntegerType(), True),
    StructField("started_at", TimestampType(), True),
    StructField("language", StringType(), True),
    StructField("title", StringType(), True),
    StructField("is_mature", BooleanType(), True),
    StructField("tag_ids", ArrayType(StringType()), True),
    StructField("thumbnail_url", StringType(), True)
])

df = 