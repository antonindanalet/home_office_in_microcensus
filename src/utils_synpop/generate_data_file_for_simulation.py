from pathlib import Path
import pandas as pd
from math import isnan
import numpy as np
# import shapely
import geopandas


def generate_data_file_for_simulation():
    """ Generates the data file for applying the model to the synthetic population (SynPop).
    In particular, it changes the format of the SynPop and adds some geospatial information,
    the connection quality of public transport where the person lives (in German: OeV-Gueteklassen, see
    https://www.are.admin.ch/are/de/home/mobilitaet/grundlagen-und-daten/verkehrserschliessung-in-der-schweiz.html
    :return: Nothing, but saves a CSV file 'persons_from_SynPop2017.csv' in data/output/data/application_to_synpop/
    """
    ''' Read the persons from the synthetic population '''
    synpop_folder_path = Path('../data/input/SynPop/2017/')
    selected_columns = ['position_in_bus',  # information about work THERE IS A CORRECTED VERSION OF THE VARIABLE, type_5 !!!
                        'type_2',  # level of employment (in %) THERE IS A CORRECTED VERSION OF THE VARIABLE, type_6 !!!!
                        'person_id', 'household_id', 'sex', 'education', 'income',
                        'dbirth']  # date of birth
    with open(synpop_folder_path / 'persons.csv', 'r') as persons_file:
        df_persons = pd.read_csv(persons_file, sep=';', usecols=selected_columns)
    nb_of_persons_before = len(df_persons)
    ''' Transform the data structure '''
    # Transform the 'date of birth' variable to an 'age' variable (reference year: 2017)
    df_persons['age'] = 2017 - df_persons['dbirth'].str.split('-', expand=True)[2].astype(int)
    del df_persons['dbirth']
    # Transform the variable about employment to a variable about being employed
    df_persons['employed'] = df_persons['position_in_bus'].apply(lambda x:
                                                                 -99 if isnan(x) else (0 if x == 0 else 1))
    ''' Add information about work '''
    df_persons['executives'] = df_persons['position_in_bus'].apply(lambda x: 1 if (0 < x < 19) else 0)
    del df_persons['position_in_bus']
    # Transform the variable about level of employment to a binary variable about working full time
    df_persons.rename(columns={'type_2': 'work_percentage'}, inplace=True)
    # Aggregate the income per person to get the income per household
    df_hh_income = df_persons[['household_id', 'income']].groupby(['household_id']).sum()  # Aggregate over people
    df_hh_income = df_hh_income.rename(columns={'income': 'hh_income'})  # Rename the variable
    df_hh_income['hh_income'] = df_hh_income['hh_income'] / 12.0  # Transform from yearly to monthly income
    df_hh_income['hh_income'] = np.select(condlist=[df_hh_income['hh_income'] < 2000,
                                                    df_hh_income['hh_income'].between(2000,   4000),
                                                    df_hh_income['hh_income'].between(4001,   6000),
                                                    df_hh_income['hh_income'].between(6001,   8000),
                                                    df_hh_income['hh_income'].between(8001,  10000),
                                                    df_hh_income['hh_income'].between(10001, 12000),
                                                    df_hh_income['hh_income'].between(12001, 14000),
                                                    df_hh_income['hh_income'].between(14001, 16000),
                                                    16000 < df_hh_income['hh_income']],
                                          choicelist=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                                          default=-98)  # Transform CHF to MTMC categories
    df_persons = pd.merge(df_persons, df_hh_income, on='household_id', how='left')  # Add the result to df_persons
    del df_persons['income']
    ''' Read the households from the synthetic population '''
    synpop_folder_path = Path('../data/input/SynPop/2017/')
    selected_columns = ['household_id',
                        'xcoord',  # Swiss coordinates CH1903+ / LV95 (ex: 2566304.0)
                        'ycoord']  # Swiss coordinates CH1903+ / LV95 (ex: 1181454.0)
    with open(synpop_folder_path / 'households.csv', 'r') as households_file:
        df_households = pd.read_csv(households_file, sep=';', usecols=selected_columns)
    # Transform the household dataframe to a geodataframe
    # In order to avoid a bug with PyGEOS probably due to a problem with the Shapely installation
    # See https://github.com/geopandas/geopandas/issues/1652
    # shapely.speedups.disable()
    geodf_household = geopandas.GeoDataFrame(df_households,
                                             geometry=geopandas.points_from_xy(df_households.xcoord,
                                                                               df_households.ycoord))
    geodf_household.set_crs(epsg=2056, inplace=True)  # Define the projection of the GeoDataFrame
    df_persons = add_public_transport_connection_quality(df_persons, geodf_household)
    ''' Test that the number of people are still the same '''
    nb_of_persons_after = len(df_persons)
    if nb_of_persons_after != nb_of_persons_before:
        raise Exception('Error: Some people got lost on the way!')
    ''' Test that no column contains NA values '''
    for column in df_persons.columns:
        if df_persons[column].isna().any():
            print('There are NA values in column', column)
    ''' Save the file '''
    output_directory = Path('../data/output/data/validation_with_Synpop/')
    data_file_name = 'persons_from_SynPop2017.csv'
    df_persons.to_csv(output_directory / data_file_name, sep=';', index=False)


def add_public_transport_connection_quality(df_persons, geodf_household):
    """ Add connection quality of public transport from coordinates
    :param df_persons: Contains the people from the SynPop
    :param geodf_household: Contains the households from the SynPop, incl. coordinates
    :return: df_persons: Contains the people from the SynPop, including a column containing the connection quality
    - A = very good
    - B = good
    - C = medium
    - D = low
    - 5 = marginal or no public transport connection
    """
    # Read the shape file containing the connection quality
    connection_quality_folder_path = Path('../data/input/OeV_Gueteklassen/Fahrplanperiode_17_18/')
    df_connection_quality = geopandas.read_file(connection_quality_folder_path / 'OeV_Gueteklassen_ARE.shp')
    df_connection_quality.to_crs(epsg=2056, inplace=True)  # Define the projection
    geodf_household = geopandas.sjoin(geodf_household, df_connection_quality[['KLASSE', 'geometry']],
                                      how='left', op='intersects')
    df_households = pd.DataFrame(geodf_household[['household_id', 'KLASSE']])
    df_households['KLASSE'] = df_households['KLASSE'].map({'A': 1,
                                                           'B': 2,
                                                           'C': 3,
                                                           'D': 4})
    df_households['KLASSE'].fillna('5', inplace=True)
    # Rename the column with the public transport connection quality
    df_households.rename(columns={'KLASSE': 'public_transport_connection_quality_ARE'}, inplace=True)
    df_persons = pd.merge(df_persons, df_households, on='household_id', how='left')
    return df_persons


def add_regions(df_persons, geodf_household):
    """ Add regions of Switzerland from coordinates
    :param df_persons: Contains the people from the SynPop
    :param geodf_household: Contains the households from the SynPop
    :return: df_persons: Contains the people from the SynPop, including a column containing the region of Switzerland
    - 1 = Region lemanique
    - 2 = Espace Mittelland
    - 3 = Nordwestschweiz
    - 4 = Zurich
    - 5 = Ostschweiz
    - 6 = Zentralschweiz
    - 7 = Tessin
    """
    # Read the shape file containing the borders of the regions
    region_folder_path = Path('../data/input/Grossregionen/ag-b-00.03-875-gg17/ggg_2017vz/shp/LV95/')
    df_regions = geopandas.read_file(region_folder_path / 'g1r17vz.shp')
    df_regions.to_crs(epsg=2056, inplace=True)  # Define the projection
    geodf_household = geopandas.sjoin(geodf_household, df_regions[['GRNR', 'geometry']], how='left', op='intersects')
    df_households = pd.DataFrame(geodf_household[['household_id', 'GRNR']])
    df_households.rename(columns={'GRNR': 'region'}, inplace=True)  # Rename the column containing the region number
    df_households['region'].fillna(-99, inplace=True)
    df_persons = pd.merge(df_persons, df_households, on='household_id', how='left')
    return df_persons
