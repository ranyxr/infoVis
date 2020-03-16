import os
from pathlib import Path

__dir_path = os.path.dirname(os.path.realpath(__file__))

proj_path = Path(__dir_path).parent
data_path = Path(proj_path).joinpath("./data")

raw_data = os.path.join(data_path, "raw")
clean_data1 = os.path.join(data_path, "clean_data1.parquet.gzip")
clean_data2 = os.path.join(data_path, "clean_data2.parquet.gzip")
word_cloud_data1 = os.path.join(data_path, "word_cloud_data1.parquet.gzip")

result_stack_data = os.path.join(data_path, "result_stack_data_{}.parquet.gzip")
result_stack_x_axis = os.path.join(data_path, "result_stack_x_axis.parquet.gzip")
result_stack_art_type = os.path.join(data_path, "result_stack_art_type.parquet.gzip")
result_word_cloud = os.path.join(data_path, "result_word_cloud.parquet.gzip")

def ensure_dir_exist(folder):
    if os.path.exists(folder) is False:
        os.makedirs(folder, exist_ok=True)
