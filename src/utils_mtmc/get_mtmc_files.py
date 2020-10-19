import pandas as pd
from pathlib import Path


def get_zp(year, selected_columns=None):
    if year == 2015:
        folder_path = Path('../data/input/mtmc/2015/')
        with open(folder_path / 'zielpersonen.csv', 'r') as zielpersonen_file:
            if selected_columns is None:
                df_zp = pd.read_csv(zielpersonen_file)
            else:
                df_zp = pd.read_csv(zielpersonen_file,
                                    dtype={'HHNR': int},
                                    usecols=selected_columns)
    else:
        raise Exception('Year not well defined')
    return df_zp


def get_hh(year, selected_columns=None):
    if year == 2015:
        folder_path_2015 = Path('../data/input/mtmc/2015/')
        with open(folder_path_2015 / 'haushalte.csv', 'r') as haushalte_file:
            df_hh = pd.read_csv(haushalte_file,
                                dtype={'HHNR': int},
                                usecols=selected_columns)
    return df_hh
