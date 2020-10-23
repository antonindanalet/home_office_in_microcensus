import pandas as pd
from pathlib import Path
import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import Beta, Variable, DefineVariable
import os


def estimate_choice_model_home_office():
    """ File logit_home_office.py

    :author: Antonin Danalet, based on the example by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    A binary logit model on the possibility to work from home at least some times."""

    # Read the data
    data_file_directory = Path('../data/output/data/estimation/')
    df = pd.read_csv(data_file_directory / 'persons.csv', ';')
    database = db.Database('persons', df)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    ''' Removing people who did not get the question or did not answer. '''
    database.data.drop(database.data[database.data.home_office < 0].index, inplace=True)

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
    B_employed = Beta('B_employed', 0, None, None, 1)

    B_public_transport_connection_quality_ARE_A = Beta('B_public_transport_connection_quality_ARE_A', 0, None, None, 0)
    B_public_transport_connection_quality_ARE_B = Beta('B_public_transport_connection_quality_ARE_B', 0, None, None, 0)
    B_public_transport_connection_quality_ARE_C = Beta('B_public_transport_connection_quality_ARE_C', 0, None, None, 1)
    B_public_transport_connection_quality_ARE_D = Beta('B_public_transport_connection_quality_ARE_D', 0, None, None, 1)
    B_public_transport_connection_quality_ARE_NA = Beta('B_public_transport_connection_quality_ARE_NA', 0, None, None,
                                                        1)

    B_URBAN = Beta('B_URBAN', 0, None, None, 1)
    B_RURAL = Beta('B_RURAL', 0, None, None, 1)
    B_INTERMEDIATE = Beta('B_INTERMEDIATE', 0, None, None, 1)

    B_home_work_distance = Beta('B_home_work_distance', 0, None, None, 1)

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
        B_public_transport_connection_quality_ARE_A * public_transport_connection_quality_ARE_A + \
        B_public_transport_connection_quality_ARE_B * public_transport_connection_quality_ARE_B + \
        B_public_transport_connection_quality_ARE_C * public_transport_connection_quality_ARE_C + \
        B_public_transport_connection_quality_ARE_D * public_transport_connection_quality_ARE_D + \
        B_public_transport_connection_quality_ARE_NA * public_transport_connection_quality_ARE_NA + \
        B_URBAN * urban + \
        B_RURAL * rural + \
        B_INTERMEDIATE * intermediate + \
        B_home_work_distance * home_work_distance
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
    os.chdir('../data/output/models/')

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
