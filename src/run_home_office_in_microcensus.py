import pandas as pd
from pathlib import Path
from utils_mtmc.get_mtmc_files import get_zp, get_hh
from logit_home_office import estimate_choice_model_home_office


def run_home_office_in_microcensus():
    generate_data_file()
    estimate_choice_model_home_office()


def generate_data_file():
    """ This function takes as input the  data about the person and join them with the data about the household and the
        spaptial typology. It returns nothing, but saves the output as a data file for Biogeme.
        :param: Nothing.
        :return: Nothing. The dataframe is saved as a CSV file (separator: tab) without NA values, to be used with
        Biogeme.
        """
    ''' Select the variables about the person from the tables of the MTMC 2015 '''
    selected_columns_zp = ['gesl', 'HAUSB', 'HHNR', 'ERWERB', 'f81300']
    df_zp = get_zp(2015, selected_columns_zp)
    selected_columns_hh = ['F20601', 'HHNR']
    df_hh = get_hh(2015, selected_columns_hh)
    df_zp = pd.merge(df_zp, df_hh, on='HHNR', how='left')

    # Rename the variables
    df_zp = df_zp.rename(columns={'gesl': 'sex',
                                  'HAUSB': 'highest_educ',
                                  'F20601': 'hh_income',
                                  'f81300': 'home_office'})
    ''' Test that no column contains NA values '''
    for column in df_zp.columns:
        if df_zp[column].isna().any():
            print('There are NA values in column', column)
    ''' Save the file '''
    output_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    df_zp.to_csv(output_directory / data_file_name, sep=';', index=False)


if __name__ == '__main__':
    run_home_office_in_microcensus()
