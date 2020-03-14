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


def update_school_default_value(school_txt):
    if school_txt in ["unknown", "nan"]:
        return None
    else:
        return school_txt


def get_omniart_data_frame():
    dd_df = spark.read.csv(FILE.data_dump_uri, header=True)
    dd_df = dd_df.select(COL.o_id, COL.ak_nm, COL.at_nm, COL.year, COL.century, COL.s_url, COL.i_url,
                         COL.school, col(COL.g_type).alias(COL.l1_type), col(COL.a_type).alias(COL.l3_type))

    md_df = spark.read.csv(FILE.meta_data_uri, header=True)
    md_df = md_df.select(COL.o_id, COL.ak_nm, COL.at_nm, COL.year, COL.century, COL.s_url, COL.i_url,
                         COL.school, col(COL.g_type).alias(COL.l1_type), col(COL.a_type).alias(COL.l3_type))

    omniart_df = dd_df.union(md_df).drop_duplicates([COL.o_id])

    omniart_df = omniart_df.withColumn(COL.year, col(COL.year).cast(IntegerType()))
    omniart_df = omniart_df.withColumn(COL.century, col(COL.century).cast(IntegerType()))
    omniart_df = omniart_df.withColumn(COL.school, col(COL.school).cast(StringType()))
    omniart_df = omniart_df.withColumn(COL.o_id, col(COL.o_id).cast(LongType()))

    update_udf = udf(update_school_default_value, StringType())
    omniart_df = omniart_df.withColumn(COL.school, update_udf(col(COL.school)))

    if Mode.limit:
        omniart_df = omniart_df.filter(col(COL.school) != "null")
        omniart_df = spark.createDataFrame(omniart_df.limit(2).toPandas())

    return omniart_df


def get_omniart_description(omniart_df):
    pd_df = spark.read.csv(FILE.pic_desc_uri, header=True)
    pd_df = pd_df.select("textual_description", "omni_id")
    omniart_df = pd_df.join(omniart_df, on=[COL.o_id])
    return omniart_df


def clean_artwork_name(name):
    if name is None:
        return
    if "(detail" in name or "(cell" in name:
        return
    if "(second opening)" in name:
        return
    else:
        return name


def clean_url(source_url):
    import re
    match = re.match(r"http(s)?://((\w|-)+\.){1,2}(org|com|net|hu)", source_url)
    if match:
        return source_url
    else:
        return


def clean_school_raw_clean(school):
    import re
    if school is None or school == "null" or school == "unknown":
        return [None]
    school = school.lower()
    # ------------------------------------------------------
    # 去介词/Remove prep
    for prep in ["in", "near", "the", "and", "und", "og", "&", "son", "etc", "co", "la", "de", "te", "co"
                 "printed", "printing", "published"]:
        regx = "( )({})|({})( )|^({})".format(prep, prep, prep)
        school = re.sub(regx, ",", school)
    # Remove punctuation
    school = re.sub(r"( )*((?!( |-))\W)( )*", ',', school)

    # Remove digits, words with . (pp.)
    school = re.sub(r'(((\w)*\.|(\d)+|\[((?!\]).)+(\])?)|(((?! ).)+)\])( )*', '', school)

    # Remove none-meaningful single word
    school = re.sub(r'( )\w( )|^\w( )|( )\w$', " ", school)

    school = school.replace("for the author", "")
    school = school.replace(" religious tract society", "")
    school = school.replace(" printed", "")

    #
    for city in ["america", "london", "new york", "dublin", "british", "frankfurt", "bristol",
                 "edinburgh", "perth", "boston", "glasgow", "allahabad", "konigsberg", "philadelphia", "france"
                 "spain", "washington", "oxford", "zurich", "bradford", "toronto", "santiago", "ashford", "toronto"]:
        school = re.sub("(?<=,)(.)+(?={})|(?<={})(.)+(?=,)|((?<={}))((?!,).)+".format(city, city, city), city, school)
        school = re.sub("^(.)+(?={})".format(city), "", school)

    # Germany district update
    school = school.replace("neu ", "neu")
    # ness => country
    school = school.replace("american", "america")
    school = school.replace("austrian", "austria")
    school = school.replace("mexican", "mexico")
    school = school.replace("italian", "italy")
    school = school.replace("italia", "italy")
    school = school.replace("chinese", "china")
    school = school.replace("japanese", "japan")
    school = school.replace("german", "germany")
    school = school.replace("dutch", "netherlands")
    school = school.replace("french", "france")
    school = school.replace("londini", "london")
    school = school.replace("irish", "ireland")
    school = school.replace("españa", 'spain')
    school = school.replace("spanish", "spain")
    school = school.replace("danish", "denmark")
    school = school.replace("scottish", "scotland")
    school = school.replace("swedish", "sweden")
    school = school.replace("portuguese", "portugal")
    school = school.replace("korean", "korea")
    school = school.replace("european", "europe")
    school = school.replace("hungarian", "hungary")
    school = school.replace("babylonian", "iraq")
    school = school.replace("sumerian", "iraq")
    school = school.replace("roman", "italy")
    school = school.replace("etruscan", "italy")
    school = school.replace("byzantine", "italy")
    school = school.replace("assyrian", "assyria")
    school = school.replace("belgian", "belgium")
    school = school.replace("parthian", "iran")
    school = school.replace("sasanian", "egypt")
    school = school.replace("egyptian", "egypt")
    school = school.replace("bohemian", "bohemia")
    school = school.replace("peruvian", "peru")
    school = school.replace("russian", "russia")

    # Typo convert (city)
    school = school.replace("kjbenhaven", "kobenhavn")
    school = school.replace("new yorknew york", "new york")
    school = school.replace("englandbritish guiana", "england")
    school = school.replace("englandbritish lumbia", "england")
    school = school.replace("francfort", "frankfurt")
    # Alias convert (city)
    school = school.replace("san francis", "san francisco")
    school = school.replace("hradci kralove", "hradec kralove")
    school = school.replace("newcastle on tyne", "newcastle on tyne")
    school = school.replace("nouvelle york", "new york")
    school = school.replace("nueva york", "new york")

    school_list = list(filter(None, school.split(",")))
    school_list = [re.sub(r'( )\w( )|^\w( )|( )\w$', " ", x).strip() for x in school_list]
    school_list = [x for x in school_list if len(x) > 2]
    return school_list


def clean_school(school):
    geo = Nominatim(user_agent="00000")
    while True:
        try:
            location = geo.geocode(school, language='en', addressdetails=True)
            print("{} [System]: {} information request is success".format(datetime.now(), school))
            break
        except Exception:
            print("{} [System]: Country information request is timeout".format(datetime.now()))
            time.sleep(2)
    if location is not None:
        if COL.country_code not in location.raw["address"]:
            print(school + " " + str(location.raw))
            return [None, None, None]
        return [location.raw["address"][COL.country],
                location.raw["address"][COL.country_code],
                [location.longitude, location.latitude]
                ]
    return [None, None, None]


def get_school_df(omniart_df):
    school_df = omniart_df.groupby(col(COL.school)).count()
    if Mode.limit is not True:
        school_df = school_df.filter(col(COL.count) > 100)
    school_df = school_df.toPandas()

    school_df[COL.country] = school_df[COL.school].apply(clean_school)
    import pandas as pd
    school_df[[COL.country, COL.country_code, COL.coordinate]] = pd.DataFrame(school_df[COL.country].values.tolist())
    school_df = spark.createDataFrame(school_df)
    return school_df


def clean_l1_type(l1_type):
    if l1_type in ['unknown', 'null', 'f', 'architecture', '1', 'mies van der rohe archive']:
        return 'unknown'
    else:
        return l1_type


def clean_l3_type(l3_type):
    if l3_type is None or l3_type in ['null', "(not assigned)", "nan", "MOMA - New York", "hide", "blocks",
                                      "others", "decorative arts", "bronzes|(not assigned)", "barkcloth",
                                      "gesso", "graphic", "software", "plastic", "surcoat", "plates",
                                      "media", "collage", "lighting", "kris stand", "document", "brigandines",
                                      "saddle plates", "parchment", "bibliography", "plastic", "software",
                                      "graphic design", "fencing equipment", "gesso", "assemblage", "barkcloth"]:
        return 'unknown'
    l3_type = l3_type.lower()

    for x in [
              "stamp seal", "cylinder seal", "cut paper",
              "firearms", "firearms", "chordophone", "coin", "costume", "sword furniture",
              "lapidary", "vase", "reproductions", "natural substance", "membranophone", "medal", "equestrian",
              "manuscript", "illustrated book", "helmet", "chess set", "archery equipment",
              "accessory", "aerophone", "album", "shield", "illustration", "book", "tablet",
              "container", "drawing", "sculpture", "poster", "photo", "sword", "cylinder", "equestrian", "codic",
              "implement", "ornament", "relief", "vessel", "architecture", "painting", "codices", "enamel", "pistol",
              "gun", "furniture", "gems", "image", "paper", "periodical", "idiophone", "horology", "drawing",
              "musical instrument", "ivories", "gold", "armor", "banner", "wood", "weapon", "amber",
              "badge", "faience", "lead", "leather", "mosaic", "papyrus", "glass", "stucco", "wax", "plaquette", "metal", "mask", "dagger", "ivory"
    ]:
        if x in l3_type:
            return x
    if "assemblage" in l3_type or "menswear" in l3_type or "document" in l3_type\
            or "thermometer" in l3_type or "plaster" in l3_type or "sharkskin" in l3_type:
        return "unknown"
    if "ivories" in l3_type:
        return "ivory"
    elif "knives" in l3_type:
        return "knife"
    elif "urushi-e" in l3_type:
        return "yakusha-e"
    elif "architectural" in l3_type:
        return "architecture"
    elif "seal" in l3_type:
        return "seal"
    elif "papier" in l3_type:
        return "paper"
    elif "instrument" in l3_type:
        return "instrument"
    elif "trompe-l'il" in l3_type:
        return "painting"
    elif "coat of mail and plate" in l3_type:
        return "armor"
    elif "caligraphy" in l3_type:
        return "calligraphy"
    elif "emblem pictura" in l3_type:
        return "emblem picture"
    elif "snuff bottles" in l3_type:
        return "smoking equipment"
    elif "snuffboxes" in l3_type:
        return "smoking equipment"
    return l3_type


def clean_omniart_data_frame(omniart_df):
    # Step | Clean omniart id
    omniart_df = omniart_df.filter(col(COL.o_id).isNotNull())

    # Step | Clean omniart artwork name
    clean_udf = udf(clean_artwork_name, StringType())
    omniart_df = omniart_df.withColumn(COL.ak_nm, clean_udf(col(COL.ak_nm)))
    omniart_df = omniart_df.filter(col(COL.ak_nm).isNotNull())

    # Clean omniart artwork source url
    clean_udf = udf(clean_url, StringType())
    omniart_df = omniart_df.withColumn(COL.s_url, clean_udf(col(COL.s_url)))
    omniart_df = omniart_df.filter(col(COL.s_url) != "null")

    # Step | Clean omniart artwork image url
    clean_udf = udf(clean_url, StringType())
    omniart_df = omniart_df.withColumn(COL.i_url, clean_udf(col(COL.i_url)))
    omniart_df = omniart_df.filter(col(COL.i_url).isNotNull())

    # Step | Clean school's information
    clean_udf = udf(clean_school_raw_clean, ArrayType(StringType()))
    omniart_df = omniart_df.withColumn(COL.school, clean_udf(col(COL.school)))
    omniart_df = omniart_df.withColumn(COL.school, explode(COL.school))

    school_df = get_school_df(omniart_df)
    omniart_df = omniart_df.join(school_df, on=[COL.school], how="outer")
    omniart_df = omniart_df.filter((col(COL.school) == "null") | (col(COL.country) != "null"))
    omniart_df = omniart_df.drop_duplicates([COL.o_id, COL.country_code])

    # Step | Clean omniart l1 gene type
    clean_udf = udf(clean_l1_type, StringType())
    omniart_df = omniart_df.withColumn(COL.l1_type, clean_udf(col(COL.l1_type)))

    # Step | Clean omniart l3 gene type
    clean_udf = udf(clean_l3_type, StringType())
    omniart_df = omniart_df.withColumn(COL.l3_type, clean_udf(col(COL.l3_type)))
    return omniart_df


if __name__ == '__main__':
    df = get_omniart_data_frame()
    df = get_omniart_description(df)
    df = clean_omniart_data_frame(df)
    df.write.mode("overwrite").parquet(FILE.cleaned_data1_fnm_uri, compression="gzip")

