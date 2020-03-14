import urllib.request
from datetime import datetime
from SYS import DIR, FILE

meta_data_url = "http://isis-data.science.uva.nl/strezoski/omniart/omniart_v3/artsight_csvs/metadatas.csv"
meta_level_meta_url = "http://isis-data.science.uva.nl/strezoski/omniart/omniart_v3/artsight_csvs/metalevelmeta.csv"
data_dump_url = "http://isis-data.science.uva.nl/strezoski/omniart/omniart_v3/data/csv/omniart_v3_datadump.csv"
reproductions_url = "http://isis-data.science.uva.nl/strezoski/omniart/omniart_v3/artsight_csvs/reproductions.csv"

file_list = [
    [meta_data_url, FILE._meta_data_uri],
    [meta_level_meta_url, FILE._meta_level_meta_uri],
    [data_dump_url, FILE._data_dump_uri],
    [reproductions_url, FILE._reproductions_uri]
]

for file_pair in file_list:
    DIR.ensure_dir_exist(DIR.raw_data)
    print("{}[System]{} file is retrieving ".format(datetime.now(), file_pair[1]))
    urllib.request.urlretrieve(file_pair[0], file_pair[1])
    print("{}[System]{} file retrieved ".format(datetime.now(), file_pair[1]))
