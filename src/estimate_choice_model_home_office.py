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


def run_estimation(data_file_directory, data_file_name, output_directory, output_file_name='logit_home_office'):
    """
    :author: Antonin Danalet, based on the example '01logit.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    A binary logit model on the possibility to work from home at least some times."""

    # Read the data

    df = pd.read_csv(data_file_directory / data_file_name, ';')
    database = db.Database('persons', df)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    # Parameters to be estimated
    alternative_specific_constant = Beta('alternative_specific_constant', 0, None, None, 0)

    b_full_time_work = Beta('b_full_time_work', 0, None, None, 1)
    b_active_without_known_work_percentage = Beta('b_active_without_known_work_percentage', 0, None, None, 1)

    b_no_post_school_education = Beta('b_no_post_school_education', 0, None, None, 0)
    b_secondary_education = Beta('b_secondary_education', 0, None, None, 0)
    b_tertiary_education = Beta('b_tertiary_education', 0, None, None, 0)
    b_university = Beta('b_university', 0, None, None, 1)

    b_male = Beta('b_male', 0, None, None, 0)

    b_single_household = Beta('b_single_household', 0, None, None, 0)
    b_couple_without_children = Beta('b_couple_without_children', 0, None, None, 0)
    b_couple_with_children = Beta('b_couple_with_children', 0, None, None, 1)
    b_single_parent_with_children = Beta('b_single_parent_with_children', 0, None, None, 0)
    b_not_family_household = Beta('b_not_family_household', 0, None, None, 1)

    b_public_transport_connection_quality_are_a = Beta('b_public_transport_connection_quality_are_a', 0,
                                                            None, None, 0)
    b_public_transport_connection_quality_are_b = Beta('b_public_transport_connection_quality_are_b', 0,
                                                            None, None, 0)
    b_public_transport_connection_quality_are_c = Beta('b_public_transport_connection_quality_are_c', 0, None, None, 0)
    b_public_transport_connection_quality_are_d = Beta('b_public_transport_connection_quality_are_d', 0, None, None, 0)
    b_public_transport_connection_quality_are_na = Beta('b_public_transport_connection_quality_are_na', 0, None, None,
                                                        1)

    b_urban = Beta('b_urban', 0, None, None, 1)
    b_rural = Beta('b_rural', 0, None, None, 1)
    b_intermediate = Beta('b_intermediate', 0, None, None, 1)

    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)

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
                                        home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0,
                                        database)

    #  Utility
    U = alternative_specific_constant + \
        b_full_time_work * full_time_work + \
        b_active_without_known_work_percentage * active_without_known_work_percentage + \
        b_no_post_school_education * no_post_school_educ + \
        b_secondary_education * secondary_education + \
        b_tertiary_education * tertiary_education + \
        b_university * university + \
        b_male * male + \
        b_single_household * single_household + \
        b_couple_without_children * couple_without_children + \
        b_couple_with_children * couple_with_children + \
        b_single_parent_with_children * single_parent_with_children + \
        b_not_family_household * not_family_household + \
        b_public_transport_connection_quality_are_a * public_transport_connection_quality_ARE_A + \
        b_public_transport_connection_quality_are_b * public_transport_connection_quality_ARE_B + \
        b_public_transport_connection_quality_are_c * public_transport_connection_quality_ARE_C + \
        b_public_transport_connection_quality_are_d * public_transport_connection_quality_ARE_D + \
        b_public_transport_connection_quality_are_na * public_transport_connection_quality_ARE_NA + \
        b_urban * urban + \
        b_rural * rural + \
        b_intermediate * intermediate + \
        b_home_work_distance * home_work_distance + \
        models.piecewiseFormula(age, [0, 35, 55, 200])
    U_No_home_office = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U,  # Yes or sometimes
         3: U_No_home_office}  # No

    av = {1: 1,
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
    biogeme.modelName = output_file_name

    # Estimate the parameters
    results = biogeme.estimate()

    # Get the results in a pandas table
    pandas_results = results.getEstimatedParameters()
    print(pandas_results)

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
    ''' Transform the variable home office from 3 to 2 possible answers '''
    df_zp.home_office =df_zp.home_office.map({1: 1,
                                              2: 1,
                                              3: 3})
    ''' Test that no column contains NA values '''
    for column in df_zp.columns:
        if df_zp[column].isna().any():
            print('There are NA values in column', column)
    ''' Save the file '''
    output_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    df_zp.to_csv(output_directory / data_file_name, sep=';', index=False)
