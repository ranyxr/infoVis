from SYS import DIR
import os
"picture-info.csv"

_meta_data_fnm = "metadatas.csv"
_meta_data_uri = os.path.join(DIR.raw_data, _meta_data_fnm)
meta_data_uri = _meta_data_uri

_meta_level_meta_fnm = "picture-description.csv"
_meta_level_meta_uri = os.path.join(DIR.raw_data, _meta_level_meta_fnm)
pic_desc_uri = _meta_level_meta_uri

_data_dump_fnm = "datadump.csv"
_data_dump_uri = os.path.join(DIR.raw_data, _data_dump_fnm)
data_dump_uri = _data_dump_uri

_reproductions_fnm = "picture-info.csv"
_reproductions_uri = os.path.join(DIR.raw_data, _reproductions_fnm)
pic_info_uri = _reproductions_uri

cleaned_data1_fnm = DIR.clean_data1
cleaned_data1_uri = DIR.clean_data1

cleaned_data2_fnm = DIR.clean_data2
cleaned_data2_uri = DIR.clean_data2

word_cloud_data1_fnm = DIR.word_cloud_data1
word_cloud_data1_uri = DIR.word_cloud_data1

word_cloud_data2_fnm = DIR.word_cloud_data2
word_cloud_data2_uri = DIR.word_cloud_data2

result_stack_data_uri = DIR.result_stack_data
result_stack_x_axis_uri = DIR.result_stack_x_axis
result_stack_art_type_uri = DIR.result_stack_art_type
result_word_cloud_uri = DIR.result_word_cloud

artiest_json_dir_uri = os.path.join(DIR.artiest_json_dir, "artists.json")
