from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, LongType, ArrayType
from pyspark.sql.functions import col, udf, explode, sum
from SYS import FILE, COL, Mode
from geopy.geocoders import Nominatim
from datetime import datetime
import time

spark = SparkSession \
    .builder \
    .config("spark.master", "local[*]") \
    .config("spark.executor.memory", "2g") \
    .appName("VI") \
    .getOrCreate()

df = spark.read.parquet(FILE.word_cloud_data1_uri)\
    .groupby(col(COL.token))\
    .agg(sum(COL.count).alias(COL.count))\
    .sort(col(COL.count), ascending=False)
df.show()
print(df.count())
