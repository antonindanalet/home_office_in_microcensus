import pandas as pd
from pathlib import Path
import geopandas
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
    selected_columns_zp = ['gesl', 'HAUSB', 'HHNR', 'ERWERB', 'f81300', 'A_X_CH1903', 'A_Y_CH1903']
    df_zp = get_zp(2015, selected_columns_zp)
    selected_columns_hh = ['HHNR', 'hhtyp', 'W_OeV_KLASSE', 'W_BFS', 'W_X_CH1903', 'W_Y_CH1903']
    df_hh = get_hh(2015, selected_columns_hh)
    df_zp = pd.merge(df_zp, df_hh, on='HHNR', how='left')

    ''' Add the distance between home and work places '''
    df_zp_with_work_coordinates = df_zp[df_zp.A_X_CH1903 != -999]
    geodf_home = geopandas.GeoDataFrame(df_zp_with_work_coordinates,
                                        geometry=geopandas.points_from_xy(df_zp_with_work_coordinates.W_Y_CH1903,
                                                                          df_zp_with_work_coordinates.W_X_CH1903),
                                        crs='epsg:21781')
    geodf_work = geopandas.GeoDataFrame(df_zp_with_work_coordinates,
                                        geometry=geopandas.points_from_xy(df_zp_with_work_coordinates.A_Y_CH1903,
                                                                          df_zp_with_work_coordinates.A_X_CH1903),
                                        crs='epsg:21781')
    df_zp.loc[df_zp.A_X_CH1903 != -999, 'home_work_crow_fly_distance'] = geodf_home.distance(geodf_work)
    df_zp['home_work_crow_fly_distance'].fillna(-999, inplace=True)
    df_zp.drop(['W_Y_CH1903', 'W_X_CH1903', 'A_Y_CH1903', 'A_X_CH1903'], axis=1, inplace=True)

    ''' Add the data about the spatial typology '''
    path_to_typology = Path('../data/input/StadtLandTypologie/2015/Raumgliederungen.xlsx')
    df_typology = pd.read_excel(path_to_typology, sheet_name='Daten',
                                skiprows=[0, 2],  # Removes the 1st row, with information, and the 2nd, with links
                                usecols='A,G')  # Selects only the BFS commune number and the column with the typology
    df_zp = pd.merge(df_zp, df_typology, left_on='W_BFS', right_on='BFS Gde-nummer', how='left')
    df_zp.drop('BFS Gde-nummer', axis=1, inplace=True)

    # Rename the variables
    df_zp = df_zp.rename(columns={'gesl': 'sex',
                                  'HAUSB': 'highest_educ',
                                  'f81300': 'home_office',
                                  'hhtyp': 'hh_type',
                                  'W_OeV_KLASSE': 'public_transport_connection_quality_ARE',
                                  'Stadt/Land-Typologie': 'urban_typology'})
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
