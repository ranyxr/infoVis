from script.Processor.DataProcessor import DataProcessor as Dp
from pyspark.sql.functions import col
from SYS import FILE, COL, MODE

dp = Dp()
df = dp.read_parquet(FILE.cleaned_data2_uri).groupby(COL.year, COL.l1_type).count()
sum_df = df.groupby(COL.year).sum(COL.count).withColumnRenamed(COL.sum_count, COL.sum_col)
df = df.join(sum_df, on=COL.year).withColumn(COL.ratio, col(COL.count)/col(COL.sum_col) * 100)

xAxis_df = df.select(col(COL.year))\
    .drop_duplicates([COL.year])\

xAxis_df.show()
print(FILE.result_stack_x_axis_uri)
dp.save_parquet(xAxis_df, FILE.result_stack_x_axis_uri)
# xAxis = xAxis_df.rdd.flatMap(lambda x: x).collect()

art_types_df = df.select(col(COL.l1_type))\
    .drop_duplicates([COL.l1_type])
art_types = art_types_df.rdd.flatMap(lambda x: x).collect()
dp.save_parquet(art_types_df, FILE.result_stack_art_type_uri)

for a_type in art_types:
    a_df = df.filter(col(COL.l1_type) == a_type)
    in_df = xAxis_df.join(a_df, on=COL.year, how="left_outer").na.fill(0).select(COL.year, COL.ratio)
    dp.save_parquet(in_df, str(FILE.result_stack_data_uri).format(a_type))

if MODE.debug:
    df.show()
