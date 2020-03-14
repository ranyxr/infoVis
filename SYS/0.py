from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, IntegerType, LongType, ArrayType
from pyspark.sql.functions import col, udf, explode
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

# spark.read.parquet(FILE.cleaned_data1_fnm_uri).groupby(col(COL.school), col(COL.country)).count().show(1000, truncate=False)
print(spark.read.csv(FILE.meta_data_uri, header=True).drop_duplicates([COL.o_id]).count())