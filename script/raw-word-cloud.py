import os
import nltk
import spacy
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, ArrayType
from pyspark.sql.functions import udf, col, explode, collect_list, count
from SYS import COL, MODE, DIR, FILE

nltk.download('stopwords')
os.system("python -m spacy download en_core_web_sm")
nlp = spacy.load("en_core_web_sm")


def get_token(tweet):
    doc = nlp(tweet)
    tokens = []
    for t in doc:
        if len(t) > 2:
            if t.is_stop is False:
                if t.pos_ in ["VERB", "NOUN"]:
                    tokens.append(str(t.lemma_))
                elif t.pos_ in ["NUM", "SYM", "ADP"]:
                    continue
                elif t.is_stop:
                    continue
                else:
                    tokens.append(str(t))
    return tokens


def process_token(in_df):
    print("{} [System]: Start processing token!".format(datetime.now()))
    udf_token = udf(get_token, ArrayType(StringType()))

    in_df = in_df.withColumn(COL.token, udf_token(col(COL.descri)))

    in_df = in_df.withColumn(COL.token, explode(col(COL.token)))
    in_df = in_df.drop(col(COL.descri))
    in_df = in_df.groupby(col(COL.year), col(COL.token))\
        .agg(collect_list(COL.o_id).alias(COL.o_id), count(COL.token).alias(COL.count))
    print("{} [System]: Token processed!".format(datetime.now()))

    return in_df


java8_location = '/Library/Java/JavaVirtualMachines/liberica-jdk-1.8.0_202/Contents/Home'
os.environ['JAVA_HOME'] = java8_location
spark = SparkSession\
    .builder\
    .appName("A1")\
    .getOrCreate()


def get_unprocessed_df():
    try:
        in_df = spark.read.parquet(FILE.cleaned_data2_uri).select(col(COL.o_id), col(COL.descri), col(COL.year))
        in_df = in_df.filter(col(COL.descri).isNotNull()).drop_duplicates([COL.o_id, COL.year])
        if MODE.limit:
            in_df = in_df.limit(20)
        print("{} [System]: Cleaned data read in successfully! {} lines read in!".format(datetime.now(), in_df.count()))
        return in_df
    except Exception:
        print("{} [System]: Cleaned data not exist. Script Exit!".format(datetime.now()))
        import sys
        sys.exit(1)


if __name__ == '__main__':
    spark.read.parquet(FILE.word_cloud_data1_uri).groupby(col(COL.token)).count().sort(col(COL.count), ascending=False).show()
    # df = get_unprocessed_df()
    # df = process_token(df)
    # df.write.mode("overwrite").parquet(FILE.word_cloud_data1_uri, compression="gzip")
    # if MODE.debug:
    #     df = df.filter(col(COL.descri).isNotNull())
    #     df.show()
