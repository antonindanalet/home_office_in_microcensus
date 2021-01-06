from pathlib import Path
import pandas as pd
import biogeme.database as db
from biogeme.expressions import Beta
import biogeme.models as models
import biogeme.biogeme as bio
import biogeme.messaging as msg
import os
import numpy as np


def apply_model_to_synthetic_population(betas, output_directory_for_simulation, household_income_limit, year):
    # Simulate the model on the synthetic population
    if year == 2017:
        data_file_directory_for_simulation = Path('../data/output/data/validation_with_SynPop/')
        data_file_name_for_simulation = 'persons_from_SynPop2017.csv'
    elif year in [2030, 2040, 2050]:
        data_file_directory_for_simulation = Path('../data/output/data/application_to_SynPop_' + str(year) + '/')
        data_file_name_for_simulation = 'persons_from_SynPop' + str(year) + '.csv'
    else:
        raise Exception('Year not well defined!')
    run_simulation(data_file_directory_for_simulation, data_file_name_for_simulation, output_directory_for_simulation,
                   betas, household_income_limit)
    predicted_rate_of_home_office = get_predicted_rate_of_home_office(output_directory_for_simulation)
    return predicted_rate_of_home_office


def get_predicted_rate_of_home_office(synpop_directory):
    synpop_filename = 'persons_from_SynPop_with_probability_home_office.csv'
    # Get the data
    df_persons = pd.read_csv(synpop_directory / synpop_filename, sep=',')
    df_persons.drop(df_persons[df_persons.position_in_bus.isin([-99, 0, 3])].index, inplace=True)
    predicted_rate_of_home_office = df_persons['Prob. home office'].mean()
    return predicted_rate_of_home_office


def run_simulation(data_file_directory_for_simulation, data_file_name_for_simulation, output_directory_for_simulation,
                   betas, household_income_limit):
    """
        :author: Antonin Danalet, based on the example '01logit_simul.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

        Simulation with a binary logit model. Two alternatives: work from home at least some times, or not."""

    # Read the data
    df_persons = pd.read_csv(data_file_directory_for_simulation / data_file_name_for_simulation, ';')
    database = db.Database('persons', df_persons)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    # Parameters to be estimated
    alternative_specific_constant = Beta('alternative_specific_constant', 0, None, None, 0)
    b_no_post_school_education = Beta('b_no_post_school_education', 0, None, None, 0)
    b_secondary_education = Beta('b_secondary_education', 0, None, None, 0)
    b_tertiary_education = Beta('b_tertiary_education', 0, None, None, 0)
    b_university = Beta('b_university', 0, None, None, 1)
    b_male = Beta('b_male', 0, None, None, 0)
    b_public_transport_connection_quality_na_home = Beta('b_public_transport_connection_quality_na_home',
                                                         0, None, None, 0)
    b_public_transport_connection_quality_a_work = Beta('b_public_transport_connection_quality_are_a_work',
                                                        0, None, None, 1)
    b_rural_work = Beta('b_rural_work', 0, None, None, 0)
    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)
    b_business_sector_agriculture = Beta('b_business_sector_agriculture', 0, None, None, 0)
    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale = Beta('b_business_sector_wholesale', 0, None, None, 1)
    b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 0)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 1)
    b_business_sector_services_fc = Beta('b_business_sector_services_fc', 0, None, None, 0)
    b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 1)
    b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 1)
    b_business_sector_non_movers = Beta('b_business_sector_non_movers', 0, None, None, 0)
    b_executives = Beta('b_executives', 0, None, None, 0)
    b_german = Beta('b_german', 0, None, None, 0)
    b_nationality_ch_germany_france_italy_nw_e = Beta('b_nationality_ch_germany_france_italy_nw_e', 0, None, None, 0)
    b_hh_income_8000_or_less = Beta('b_hh_income_8000_or_less', 0, None, None, 0)

    # Definition of new variables
    no_post_school_educ = education == 1
    secondary_education = education == 2
    tertiary_education = education == 3
    university = education == 4

    male = (sex == 1)

    public_transport_quality_NA_home = (public_transport_connection_quality_ARE_home == 5)
    public_transport_quality_A_work = (public_transport_connection_quality_ARE_work == 1)

    home_work_distance = (home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0)

    business_sector_agriculture = type_1 == 1
    business_sector_retail = type_1 == 4
    business_sector_gastronomy = type_1 == 5
    business_sector_finance = type_1 == 6
    business_sector_production = type_1 == 2
    business_sector_wholesale = type_1 == 3
    business_sector_services_fC = type_1 == 7
    business_sector_other_services = type_1 == 8
    business_sector_others = type_1 == 9
    business_sector_non_movers = type_1 == 10
    german = language == 1
    nationality_switzerland = nation == 0
    nationality_germany_austria = nation == 1
    nationality_italy_vatican = nation == 2
    nationality_france_monaco_san_marino = nation == 3
    nationality_northwestern_europe = nation == 4
    nationality_eastern_europe = nation == 7
    hh_income_8000_or_less = hh_income < household_income_limit
    executives = (0 < position_in_bus) * (position_in_bus < 19)
    rural_work = urban_rural_typology_work == 3

    #  Utility
    utility_function_home_office = alternative_specific_constant + \
                                   b_executives * executives + \
                                   b_no_post_school_education * no_post_school_educ + \
                                   b_secondary_education * secondary_education + \
                                   b_tertiary_education * tertiary_education + \
                                   b_university * university + \
                                   b_male * male + \
                                   b_public_transport_connection_quality_na_home * public_transport_quality_NA_home + \
                                   b_public_transport_connection_quality_a_work * public_transport_quality_A_work + \
                                   b_rural_work * rural_work + \
                                   b_home_work_distance * home_work_distance + \
                                   models.piecewiseFormula(age, [0, 20, 35, 75, 200]) + \
                                   b_business_sector_agriculture * business_sector_agriculture + \
                                   b_business_sector_retail * business_sector_retail + \
                                   b_business_sector_gastronomy * business_sector_gastronomy + \
                                   b_business_sector_finance * business_sector_finance + \
                                   b_business_sector_production * business_sector_production + \
                                   b_business_sector_wholesale * business_sector_wholesale + \
                                   b_business_sector_services_fc * business_sector_services_fC + \
                                   b_business_sector_other_services * business_sector_other_services + \
                                   b_business_sector_others * business_sector_others + \
                                   b_business_sector_non_movers * business_sector_non_movers + \
                                   b_german * german + \
                                   b_nationality_ch_germany_france_italy_nw_e * nationality_switzerland + \
                                   b_nationality_ch_germany_france_italy_nw_e * nationality_germany_austria + \
                                   b_nationality_ch_germany_france_italy_nw_e * nationality_italy_vatican + \
                                   b_nationality_ch_germany_france_italy_nw_e * nationality_france_monaco_san_marino + \
                                   b_nationality_ch_germany_france_italy_nw_e * nationality_northwestern_europe + \
                                   b_nationality_ch_germany_france_italy_nw_e * nationality_eastern_europe + \
                                   models.piecewiseFormula(work_percentage, [0, 90, 101]) + \
                                   b_hh_income_8000_or_less * hh_income_8000_or_less
    utility_function_no_home_office = 0

    # Associate utility functions with the numbering of alternatives
    utility_functions_with_numbering_of_alternatives = {1: utility_function_home_office,  # Yes or sometimes
                                                        3: utility_function_no_home_office}  # No

    availability_conditions = {1: 1,  # Always available
                               3: 1}  # Always available

    # The choice model is a logit, with availability conditions
    prob_home_office = models.logit(utility_functions_with_numbering_of_alternatives, availability_conditions, 1)
    prob_no_home_office = models.logit(utility_functions_with_numbering_of_alternatives, availability_conditions, 3)

    simulate = {'Prob. home office': prob_home_office,
                'Prob. no home office': prob_no_home_office}

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = 'logit_home_office_simul'

    # Define level of verbosity
    logger = msg.bioMessage()
    # logger.setSilent()
    logger.setWarning()
    # logger.setGeneral()
    # logger.setDetailed()

    # Get the betas from the estimation (without corrections)
    # path_to_estimation_folder = Path('../data/output/models/estimation/')
    # if os.path.isfile(path_to_estimation_folder / 'logit_home_office~00.pickle'):
    #     raise Exception('There are several model outputs! Careful.')
    # results = res.bioResults(pickleFile=path_to_estimation_folder / 'logit_home_office.pickle')
    # betas_without_correction = results.getBetaValues()

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    standard_directory = os.getcwd()
    os.chdir(output_directory_for_simulation)

    results = biogeme.simulate(theBetaValues=betas)
    # print(results.describe())
    df_persons = pd.concat([df_persons, results], axis=1)

    # Go back to the normal working directory
    os.chdir(standard_directory)

    # For unemployed people, fix probability of doing some home office to 0 (and probability of not doing to 1).
    df_persons.loc[df_persons.employed == 0, 'Prob. home office'] = 0.0  # Unemployed people
    df_persons.loc[df_persons.employed == 0, 'Prob. no home office'] = 1.0  # Unemployed people
    df_persons.loc[df_persons.employed == -99, 'Prob. home office'] = 0.0  # Other people
    df_persons.loc[df_persons.employed == -99, 'Prob. no home office'] = 1.0  # Other people
    # By definition, apprentices don't work from home (because they were not asked in the MTMC)
    df_persons.loc[df_persons.position_in_bus == 3, 'Prob. home office'] = 0.0
    df_persons.loc[df_persons.position_in_bus == 3, 'Prob. no home office'] = 1.0

    # Add a realisation of the probability
    df_persons['random 0/1'] = np.random.rand(len(df_persons))
    df_persons['Home office 0/1'] = np.where(df_persons['random 0/1'] < df_persons['Prob. home office'], 1, 0)

    ''' Save the file '''
    data_file_name = 'persons_from_SynPop_with_probability_home_office.csv'
    df_persons.to_csv(output_directory_for_simulation / data_file_name, sep=',', index=False)
