from script.Processor.DataProcessor import DataProcessor as Dp
from pyspark.sql.functions import col, lit, udf, lower
from pyspark.sql.types import IntegerType
from SYS import FILE, COL, MODE
import json
import pandas as pd


def update_year(in_year):
    return int(int((int(in_year)) / 20.1) * 20.1)


dp = Dp()

# Load  artiest json to DF
a_file = open(FILE.artiest_json_dir_uri, "r")
a_json = json.load(a_file)
artiest_columns = [COL.name, COL.born, COL.died, COL.nationality, COL.pic_url, COL.desc, COL.wiki_url]
artiest_dict = {}
for column in artiest_columns:
    artiest_dict[column] = []
for k in a_json:
    for nk in a_json[k]:
        for column in artiest_columns:
            artiest_dict[column].append(nk[column])
# Load all data with spark
artiest_df = pd.DataFrame(artiest_dict, columns=artiest_columns)
artiest_df = dp.spark.createDataFrame(artiest_df)\
    .withColumnRenamed(COL.name, COL.at_nm)\
    .withColumnRenamed(COL.desc, COL.at_desc)\
    .withColumn(COL.lower, lower(col(COL.at_nm)))
alldata_df = dp.read_parquet(FILE.cleaned_data1_uri)\
    .withColumn(COL.lower, lower(col(COL.at_nm)))\
    .drop(COL.at_nm)
# Join artiest description with artiest name
alldata_df = alldata_df.join(artiest_df, on="lower", how="left_outer").drop(COL.lower)

if MODE.debug:
    test_df = alldata_df.filter(col(COL.at_desc).isNotNull()).drop_duplicates([COL.at_nm])
    test_df.show()
    print("Artiest description count: " + str(test_df.count()))
# --------Clean all art work data frame--------
# Filter known l1_type/ year >= 0
alldata_df = alldata_df.filter(col(COL.year) >= 0)
alldata_df = alldata_df.filter(col(COL.l1_type) != "unknown")
# Reprocess year
clean_udf = udf(update_year, IntegerType())
alldata_df = alldata_df.withColumn(COL.year, clean_udf(col(COL.year)))

if MODE.debug:
    alldata_df.show()
    print("Art year count: " + str(alldata_df.select(COL.year).drop_duplicates([COL.year]).count()))
else:
    dp.save_parquet(alldata_df, FILE.cleaned_data2_uri)
# --------Clean word cloud data frame--------
alldata_df = dp.read_parquet(FILE.word_cloud_data1_uri)
# Filter year >= 0
alldata_df = alldata_df.filter(col(COL.year) >= 0)
# Reprocess year
alldata_df = alldata_df.withColumn(COL.year, clean_udf(col(COL.year)))
if MODE.debug:
    alldata_df.show()
    print(alldata_df.select(COL.year).drop_duplicates([COL.year]).count())
else:
    dp.save_parquet(alldata_df, FILE.word_cloud_data2_uri)
