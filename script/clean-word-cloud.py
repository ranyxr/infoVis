from script.Processor.DataProcessor import DataProcessor as Dp
from pyspark.sql.functions import col, lit, udf, lower
from pyspark.sql.types import IntegerType
from SYS import FILE, COL, MODE
import json
import pandas as pd


def update_year(in_year):
    return int(int((int(in_year)) / 20.1) * 20.1)


dp = Dp()


# --------Clean word cloud data frame--------
alldata_df = dp.read_parquet(FILE.word_cloud_data1_uri)
# Filter year >= 0
alldata_df = alldata_df.filter(col(COL.year) >= 0)
# Reprocess year
clean_udf = udf(update_year, IntegerType())
alldata_df = alldata_df.withColumn(COL.year, clean_udf(col(COL.year)))
if MODE.debug:
    alldata_df.show()
    print(alldata_df.select(COL.year).drop_duplicates([COL.year]).count())
else:
    dp.save_parquet(alldata_df, FILE.word_cloud_data2_uri)
