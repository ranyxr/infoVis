import os
data = "../data"
raw_data = os.path.join(data, "raw")
clean_data1 = os.path.join(data, "clean_data1.parquet.gzip")
word_cloud_data1 = os.path.join(data, "word_cloud_data1.parquet.gzip")

def ensure_dir_exist(folder):
    if os.path.exists(folder) is False:
        os.makedirs(folder, exist_ok=True)




