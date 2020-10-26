import pandas as pd
from pathlib import Path
import geopandas
import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import Beta, DefineVariable
import os
from utils_mtmc.get_mtmc_files import get_zp, get_hh


def estimate_choice_model_home_office():
    generate_data_file()
    data_file_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    output_directory = '../data/output/models/estimation/'
    run_estimation(data_file_directory, data_file_name, output_directory)


def run_estimation(data_file_directory, data_file_name, output_directory):
    """ File estimate_choice_model_home_office.py

    :author: Antonin Danalet, based on the example by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    A binary logit model on the possibility to work from home at least some times."""

    # Read the data

    df = pd.read_csv(data_file_directory / data_file_name, ';')
    database = db.Database('persons', df)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    # Parameters to be estimated
    ASC = Beta('ASC', 0, None, None, 0)

    B_full_time_work = Beta('B_full_time_work', 0, None, None, 0)
    B_active_without_known_work_percentage = Beta('B_active_without_known_work_percentage', 0, None, None, 1)

    B_no_post_school_education = Beta('B_no_post_school_education', 0, None, None, 0)
    B_secondary_education = Beta('B_secondary_education', 0, None, None, 0)
    B_tertiary_education = Beta('B_tertiary_education', 0, None, None, 0)
    B_university = Beta('B_university', 0, None, None, 1)

    B_male = Beta('B_male', 0, None, None, 0)

    B_single_household = Beta('B_single_household', 0, None, None, 1)
    B_couple_without_children = Beta('B_couple_without_children', 0, None, None, 1)
    B_couple_with_children = Beta('B_couple_with_children', 0, None, None, 1)
    B_single_parent_with_children = Beta('B_single_parent_with_children', 0, None, None, 0)
    B_not_family_household = Beta('B_not_family_household', 0, None, None, 1)

    B_public_transport_connection_quality_ARE_A_or_B = Beta('B_public_transport_connection_quality_ARE_A_or_B', 0, None,
                                                            None, 0)
    B_public_transport_connection_quality_ARE_C = Beta('B_public_transport_connection_quality_ARE_C', 0, None, None, 1)
    B_public_transport_connection_quality_ARE_D = Beta('B_public_transport_connection_quality_ARE_D', 0, None, None, 1)
    B_public_transport_connection_quality_ARE_NA = Beta('B_public_transport_connection_quality_ARE_NA', 0, None, None,
                                                        1)

    B_URBAN = Beta('B_URBAN', 0, None, None, 1)
    B_RURAL = Beta('B_RURAL', 0, None, None, 1)
    B_INTERMEDIATE = Beta('B_INTERMEDIATE', 0, None, None, 1)

    B_home_work_distance = Beta('B_home_work_distance', 0, None, None, 1)

    B_age = Beta('B_age', 0, None, None, 1)

    # Definition of new variables
    full_time_work = DefineVariable('full_time_work', ERWERB == 1, database)
    active_without_known_work_percentage = DefineVariable('active_without_known_work_percentage', ERWERB == 9,
                                                          database)

    no_post_school_educ = DefineVariable('no_post_school_educ',
                                         (highest_educ == 1) | (highest_educ == 2) | (highest_educ == 3) |
                                         (highest_educ == 4), database)
    secondary_education = DefineVariable('secondary_education',
                                         (highest_educ == 5) | (highest_educ == 6) | (highest_educ == 7) |
                                         (highest_educ == 8) | (highest_educ == 9) | (highest_educ == 10) |
                                         (highest_educ == 11) | (highest_educ == 12), database)
    tertiary_education = DefineVariable('tertiary_education',
                                        (highest_educ == 13) | (highest_educ == 14) |
                                        (highest_educ == 15) | (highest_educ == 16), database)
    university = DefineVariable('university', (highest_educ == 17) * 10, database)

    male = DefineVariable('male', sex == 1, database)

    single_household = DefineVariable('single_household', hh_type == 10, database)
    couple_without_children = DefineVariable('couple_without_children', hh_type == 210, database)
    couple_with_children = DefineVariable('couple_with_children', hh_type == 220, database)
    single_parent_with_children = DefineVariable('single_parent_with_children', hh_type == 230, database)
    not_family_household = DefineVariable('not_family_household', hh_type == 30, database)

    public_transport_connection_quality_ARE_A = DefineVariable('public_transport_connection_quality_ARE_A',
                                                               public_transport_connection_quality_ARE == 1, database)
    public_transport_connection_quality_ARE_B = DefineVariable('public_transport_connection_quality_ARE_B',
                                                               public_transport_connection_quality_ARE == 2, database)
    public_transport_connection_quality_ARE_C = DefineVariable('public_transport_connection_quality_ARE_C',
                                                               public_transport_connection_quality_ARE == 3, database)
    public_transport_connection_quality_ARE_D = DefineVariable('public_transport_connection_quality_ARE_D',
                                                               public_transport_connection_quality_ARE == 4, database)
    public_transport_connection_quality_ARE_NA = DefineVariable('public_transport_connection_quality_ARE_NA',
                                                                public_transport_connection_quality_ARE == 5, database)

    urban = DefineVariable('urban', urban_typology == 1, database)
    rural = DefineVariable('rural', urban_typology == 3, database)
    intermediate = DefineVariable('intermediate', urban_typology == 2, database)

    home_work_distance = DefineVariable('home_work_distance',
                                        home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 1000.0,
                                        database)

    #  Utility
    U = ASC + \
        B_full_time_work * full_time_work + \
        B_active_without_known_work_percentage * active_without_known_work_percentage + \
        B_no_post_school_education * no_post_school_educ + \
        B_secondary_education * secondary_education + \
        B_tertiary_education * tertiary_education + \
        B_university * university + \
        B_male * male + \
        B_single_household * single_household + \
        B_couple_without_children * couple_without_children + \
        B_couple_with_children * couple_with_children + \
        B_single_parent_with_children * single_parent_with_children + \
        B_not_family_household * not_family_household + \
        B_public_transport_connection_quality_ARE_A_or_B * public_transport_connection_quality_ARE_A + \
        B_public_transport_connection_quality_ARE_A_or_B * public_transport_connection_quality_ARE_B + \
        B_public_transport_connection_quality_ARE_C * public_transport_connection_quality_ARE_C + \
        B_public_transport_connection_quality_ARE_D * public_transport_connection_quality_ARE_D + \
        B_public_transport_connection_quality_ARE_NA * public_transport_connection_quality_ARE_NA + \
        B_URBAN * urban + \
        B_RURAL * rural + \
        B_INTERMEDIATE * intermediate + \
        B_home_work_distance * home_work_distance + \
        B_age * age
    U_No_home_office = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U,  # Yes
         2: U,  # Sometimes
         3: U_No_home_office}  # No

    av = {1: 1,
          2: 1,
          3: 1}

    # Definition of the model. This is the contribution of each
    # observation to the log likelihood function.
    logprob = models.loglogit(V, av,  # All alternatives are supposed to be always available
                              home_office)  # Choice variable

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    standard_directory = os.getcwd()
    os.chdir(output_directory)

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, logprob)
    biogeme.modelName = 'logit_home_office'

    # Estimate the parameters
    results = biogeme.estimate()

    # Get the results in a pandas table
    pandasResults = results.getEstimatedParameters()
    print(pandasResults)

    # Go back to the normal working directory
    os.chdir(standard_directory)


def generate_data_file():
    """ This function takes as input the  data about the person and join them with the data about the household and the
        spaptial typology. It returns nothing, but saves the output as a data file for Biogeme.
        :param: Nothing.
        :return: Nothing. The dataframe is saved as a CSV file (separator: tab) without NA values, to be used with
        Biogeme.
        """
    ''' Select the variables about the person from the tables of the MTMC 2015 '''
    selected_columns_zp = ['gesl', 'HAUSB', 'HHNR', 'ERWERB', 'f81300', 'A_X_CH1903', 'A_Y_CH1903', 'alter']
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
                                  'Stadt/Land-Typologie': 'urban_typology',
                                  'alter': 'age'})
    ''' Removing people who did not get the question or did not answer. '''
    df_zp.drop(df_zp[df_zp.home_office < 0].index, inplace=True)
    ''' Test that no column contains NA values '''
    for column in df_zp.columns:
        if df_zp[column].isna().any():
            print('There are NA values in column', column)
    ''' Save the file '''
    output_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    df_zp.to_csv(output_directory / data_file_name, sep=';', index=False)

