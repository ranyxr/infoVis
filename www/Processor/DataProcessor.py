from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType
from SYS import FILE, COL
import pandas


class DataProcessor:
    def __init__(self):
        self.spark = self.__initial_spark()
        self.__word_cloud_df = self.__get_data_word_cloud_df()
        self.__data_all_art_df = self.__get_data_all_art_df()
        self.__data_all_artiest_df = self.__get_data_all_artiest_df()

    @staticmethod
    def __initial_spark():
        spark = SparkSession \
            .builder \
            .config("spark.master", "local[*]") \
            .config("spark.executor.memory", "2g") \
            .appName("tsw") \
            .getOrCreate()
        return spark

    def get_x_axis(self):
        df = self.spark.read.parquet(FILE.result_stack_x_axis_uri).sort(col(COL.year))
        x_axis = df.rdd.flatMap(lambda x: x).collect()
        return x_axis

    def get_artwork_types(self):
        df = self.spark.read.parquet(FILE.result_stack_art_type_uri)
        artwork_types = df.rdd.flatMap(lambda x: x).collect()
        # artwork_types.sort()
        return artwork_types

    def get_stack_data(self):
        result = {}
        artwork_types = self.get_artwork_types()
        for a_type in artwork_types:
            df = self.spark.read.parquet(str(FILE.result_stack_data_uri).format(a_type)).sort(col(COL.year))
            result[a_type] = df.select(col(COL.ratio)).rdd.flatMap(lambda x: x).collect()
        return result

    def __get_data_word_cloud_df(self):
        t_df = self.spark.read.parquet(FILE.result_word_cloud_uri)\
            .filter(col(COL.year) >= 0)\
            .withColumnRenamed(COL.count, COL.value)\
            .withColumnRenamed(COL.token, COL.name)
        return t_df

    def get_word_cloud_data(self):
        return self.__word_cloud_df.groupby(col(COL.name))\
            .sum(COL.value)\
            .withColumnRenamed(COL.sum_value, COL.value)\
            .sort(COL.value, ascending=False)\
            .limit(200).toPandas().to_json(orient='records')

    def word_cloud_data_filter(self, start_year, end_year):
        return self.__word_cloud_df\
            .filter((col(COL.year) >= start_year) & (col(COL.year) <= end_year))\
            .drop(col(COL.year))\
            .groupby(col(COL.name)).sum(COL.value)\
            .withColumnRenamed(COL.sum_value, COL.value)\
            .sort(COL.value, ascending=False)\
            .limit(200).toPandas().to_json(orient='records')

    def __get_data_all_art_df(self):
        return self.spark.read.parquet(FILE.cleaned_data2_uri)

    def __get_data_all_artiest_df(self):
        return self.__data_all_art_df.filter(col(COL.at_desc).isNotNull())\
            .groupby(col(COL.year), col(COL.at_nm), col(COL.at_desc), col(COL.pic_url)).count()\
            .withColumnRenamed(COL.at_nm, COL.name)\
            .withColumnRenamed(COL.count, COL.value)\
            .withColumnRenamed(COL.descri, COL.desc)\
            .withColumn(COL.year, col(COL.year).cast(IntegerType()))

    def get_artiest_index_chart_data(self):
        return self.__data_all_artiest_df.sort(col(COL.count), ascending=False).limit(7)\
            .toPandas().to_json(orient='records')

    def artiest_index_chart_data_filter(self, s_year, e_year):
        return self.__data_all_artiest_df.filter(col(COL.year).between(s_year, e_year))\
            .sort(col(COL.count), ascending=False).limit(7) \
            .toPandas().to_json(orient='records')
