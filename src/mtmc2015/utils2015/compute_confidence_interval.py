# coding=latin-1

import numpy as np


def get_weighted_avg_and_std(table, weights, percentage=False, list_of_columns=None):
    if 'ZIELPNR' in table:
        table['unique_identifier'] = table['HHNR'] * 10 + table['ZIELPNR']
        nb_of_obs = len(table['unique_identifier'].unique())
        del table['unique_identifier']
    else:
        nb_of_obs = len(table['HHNR'].unique())
    dict_column_weighted_avg_and_std = {}
    if list_of_columns is None:
        list_of_columns = table.columns
    magic_number = 1.14
    if percentage:
        sum_all_columns = 0.0
        for column in list_of_columns:
            if column in table:
                weighted_avg, weighted_std = weighted_avg_and_std(table[column], table[weights])
                sum_all_columns += weighted_avg
                dict_column_weighted_avg_and_std[column] = weighted_avg
        for column in list_of_columns:
            if column in dict_column_weighted_avg_and_std:
                weighted_percentage = np.divide(dict_column_weighted_avg_and_std[column], sum_all_columns)
            else:
                weighted_percentage = 0.0
            variance = 1.645 * magic_number * np.sqrt(np.divide(weighted_percentage * (1.0-weighted_percentage),
                                                                float(nb_of_obs)))
            dict_column_weighted_avg_and_std[column] = [weighted_percentage, variance]
    else:
        for column in list_of_columns:
            if column in table:
                weighted_avg, weighted_std = weighted_avg_and_std(table[column], table[weights])
                dict_column_weighted_avg_and_std[column] = [weighted_avg,
                                                            np.divide(1.645 * magic_number * weighted_std,
                                                                      np.sqrt(nb_of_obs))]
    return dict_column_weighted_avg_and_std, nb_of_obs


def weighted_avg_and_std(values, weights):
    """
    Return the standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """

    weighted_avg = np.average(values, weights=weights)
    variance = np.divide((weights * ((values - weighted_avg) ** 2)).sum(), weights.sum() - 1)
    return weighted_avg, np.sqrt(variance)
