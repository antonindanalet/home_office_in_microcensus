import pandas as pd
from pathlib import Path
import biogeme.biogeme as bio
import biogeme.database as db
from biogeme.expressions import Beta, DefineVariable, Variable, bioLogLogit
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
    # globals().update(database.variables)

    # Trick for using the names of the variable as Python variables, but in a function and with version 3.2beta.
    # "globals().update(database.variables)" does not work in version 3.2 beta.
    for col in database.data.columns:
        exec("database.%s = Variable('%s')" % (col, col))

    ''' Removing people who did not get the question or did not answer. '''
    database.data.drop(database.data[database.data.home_office < 0].index, inplace=True)

    # Parameters to be estimated
    ASC = Beta('ASC', 0, None, None, 0)
    B_full_time_work = Beta('B_full_time_work', 0, None, None, 0)
    B_hh_income_more_than_8000 = Beta('B_hh_income_more_than_8000', 0, None, None, 0)
    B_no_post_school_or_secondary_education = Beta('B_no_post_school_or_secondary_education', 0, None, None, 0)
    B_tertiary_education = Beta('B_tertiary_education', 0, None, None, 0)
    B_university = Beta('B_university', 0, None, None, 1)

    B_male = Beta('B_male', 0, None, None, 0)

    # Definition of new variables
    full_time_work = DefineVariable('full_time_work', database.ERWERB == 1, database)
    hh_income_8001_to_10000 = DefineVariable('hh_income_8001_to_10000', database.hh_income == 5, database)
    hh_income_10001_to_12000 = DefineVariable('hh_income_10001_to_12000', database.hh_income == 6, database)
    hh_income_12001_to_14000 = DefineVariable('hh_income_12001_to_14000', database.hh_income == 7, database)
    hh_income_14001_to_16000 = DefineVariable('hh_income_14001_to_16000', database.hh_income == 8, database)
    hh_income_more_than_16000 = DefineVariable('hh_income_more_than_16000', database.hh_income == 9, database)

    no_post_school_educ = DefineVariable('no_post_school_educ',
                                         (database.highest_educ == 1) | (database.highest_educ == 2) |
                                         (database.highest_educ == 3) | (database.highest_educ == 4), database)
    secondary_education = DefineVariable('secondary_education',
                                         (database.highest_educ == 5) | (database.highest_educ == 6) |
                                         (database.highest_educ == 7) | (database.highest_educ == 8) |
                                         (database.highest_educ == 9) | (database.highest_educ == 10) |
                                         (database.highest_educ == 11) | (database.highest_educ == 12), database)
    tertiary_education = DefineVariable('tertiary_education',
                                        (database.highest_educ == 13) | (database.highest_educ == 14) |
                                        (database.highest_educ == 15) | (database.highest_educ == 16), database)
    university = DefineVariable('university', database.highest_educ == 17, database)

    male = DefineVariable('male', database.sex == 1, database)

    #  Utility
    U = ASC + \
        B_full_time_work * full_time_work + \
        B_hh_income_more_than_8000 * hh_income_8001_to_10000 + \
        B_hh_income_more_than_8000 * hh_income_10001_to_12000 + \
        B_hh_income_more_than_8000 * hh_income_12001_to_14000 + \
        B_hh_income_more_than_8000 * hh_income_14001_to_16000 + \
        B_hh_income_more_than_8000 * hh_income_more_than_16000 + \
        B_no_post_school_or_secondary_education * no_post_school_educ + \
        B_no_post_school_or_secondary_education * secondary_education + \
        B_tertiary_education * tertiary_education + \
        B_university * university + \
        B_male * male
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
    # All alternatives are always available -> availa
    logprob = bioLogLogit(V,
                          av,  # All alternatives are supposed to be always available
                          database.home_office)  # Choice variable

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
