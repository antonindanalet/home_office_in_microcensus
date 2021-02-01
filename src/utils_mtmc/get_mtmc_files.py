import pandas as pd
from pathlib import Path


def get_zp(year, selected_columns=None):
    folder_path = Path('../data/input/mtmc/' + str(year) + '/')
    if year == 2015:
        with open(folder_path / 'zielpersonen.csv', 'r', encoding='latin1') as zielpersonen_file:
            if selected_columns is None:
                df_zp = pd.read_csv(zielpersonen_file)
            else:
                df_zp = pd.read_csv(zielpersonen_file,
                                    dtype={'HHNR': int},
                                    usecols=selected_columns)
    elif year == 2010:
        with open(folder_path / 'zielpersonen.csv', 'r', encoding='latin1') as zielpersonen_file:
            if selected_columns is None:
                df_zp = pd.read_csv(zielpersonen_file, sep=';')
            else:
                df_zp = pd.read_csv(zielpersonen_file,
                                    sep = ';',
                                    dtype={'HHNR': int},
                                    usecols=selected_columns)
    else:
        raise Exception('Year not well defined')
    return df_zp


def get_hh(year, selected_columns=None):
    if year == 2015:
        folder_path_2015 = Path('../data/input/mtmc/2015/')
        with open(folder_path_2015 / 'haushalte.csv', 'r', encoding='latin1') as haushalte_file:
            df_hh = pd.read_csv(haushalte_file,
                                dtype={'HHNR': int},
                                usecols=selected_columns)
    return df_hh
