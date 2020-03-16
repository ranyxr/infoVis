from script.Processor.DataProcessor import DataProcessor as Dp
from pyspark.sql.functions import col
from SYS import FILE, COL, MODE

dp = Dp()
df = dp.read_parquet(FILE.result_stack_data_uri)
xAxis_df = df.select(col(COL.year))\
    .drop_duplicates([COL.year])\
    .sort(col(COL.year))

xAxis = xAxis_df.rdd.flatMap(lambda x: x).collect()
print(xAxis)
print(len(xAxis))

art_types_df = df.select(col(COL.l1_type))\
    .drop_duplicates([COL.l1_type])
art_types = art_types_df.rdd.flatMap(lambda x: x).collect()

art_result = {}
for a_type in art_types:
    a_df = df.filter(col(COL.l1_type) == a_type)
    art_result[a_type] = xAxis_df.join(a_df, on=COL.year, how="left_outer").na.fill(0).select(COL.ratio).rdd.flatMap(lambda x: x).collect()

print(art_result)
