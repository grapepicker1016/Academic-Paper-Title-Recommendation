from utils.json_parser import json2csv
import pandas as pd

def raw(path, filename, save_dir):
    df_raw = json2csv(path+filename, save_dir)
    print('raw_df.csv is created...')
    return df_raw
