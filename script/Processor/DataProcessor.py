from pyspark.sql import SparkSession


class DataProcessor:
    def __init__(self):
        self.spark = SparkSession \
            .builder \
            .config("spark.master", "local[*]") \
            .config("spark.executor.memory", "2g") \
            .appName("IV") \
            .getOrCreate()

    def read_parquet(self, uri):
        return self.spark.read.parquet(uri)

    @staticmethod
    def save_parquet(df, uri, mode="overwrite"):
        return df.write.mode(mode).parquet(uri, compression="gzip")
