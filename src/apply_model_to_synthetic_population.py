from pathlib import Path
import pandas as pd
import biogeme.database as db
from biogeme.expressions import Beta
import biogeme.models as models
import biogeme.biogeme as bio
import biogeme.results as res
import os
from utils_synpop.generate_data_file_for_simulation import generate_data_file_for_simulation
from utils_mtmc.get_mtmc_files import get_zp
from utils_mtmc.define_home_office_variable import define_home_office_variable
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std


def apply_model_to_synthetic_population():
    ''' External validation using a synthetic population '''
    # Prepare the data for PandasBiogeme
    generate_data_file_for_simulation()
    # Simulate the model on the synthetic population
    data_file_directory_for_simulation = Path('../data/output/data/validation_with_SynPop/')
    data_file_name_for_simulation = 'persons_from_SynPop2017.csv'
    output_directory_for_simulation = Path('../data/output/models/validation_with_SynPop/')
    run_simulation(data_file_directory_for_simulation, data_file_name_for_simulation, output_directory_for_simulation)
    # Compare rate of home office in the MTMC and in the synthetic population
    descr_stat_mtmc()
    # descr_stat_synpop()


def descr_stat_synpop():
    synpop_directory = Path('../data/output/models/validation_with_SynPop/')
    synpop_filename = 'persons_from_SynPop_with_probability_home_office.csv'
    # Get the data
    df_persons = pd.read_csv(synpop_directory / synpop_filename, sep=',')
    print(df_persons.loc[df_persons['age'] < 15].describe())


def descr_stat_mtmc():
    # Get the data
    selected_columns = ['HHNR', 'WP', 'f81300', 'f81400', 'alter', 'f40500', 'f40600', 'f40700']
    df_zp = get_zp(2015, selected_columns=selected_columns)
    df_zp = df_zp.rename(columns={'f81300': 'home_office_is_possible',
                                  'f81400': 'percentage_home_office',
                                  'alter': 'age',
                                  'f40500': 'work_for_money',  # Work for money in the last week
                                  'f40600': 'work_in_family_business',  # Work in the family business last week
                                  'f40700': 'work_contract'})  # Work contract even if not work last week
    ''' Removing people who did not get the question or did not answer. '''
    df_zp.drop(df_zp[df_zp.home_office_is_possible < 0].index, inplace=True)
    df_zp.drop(df_zp[df_zp.percentage_home_office == -98].index, inplace=True)
    df_zp.drop(df_zp[df_zp.percentage_home_office == -97].index, inplace=True)
    df_zp['home_office'] = df_zp.apply(define_home_office_variable, axis=1)
    # Percentage of people doing home office among people working (and who answered to the question about home office)
    df_zp_working = df_zp[(df_zp['work_for_money'] == 1) |
                          (df_zp['work_in_family_business'] == 1) |
                          (df_zp['work_contract'] == 1)]
    weighted_avg_and_std = get_weighted_avg_and_std(df_zp_working, weights='WP', list_of_columns=['home_office'])
    weighted_avg = round(weighted_avg_and_std[0]['home_office'][0], 3)
    weighted_std = round(weighted_avg_and_std[0]['home_office'][1], 3)
    nb_obs = weighted_avg_and_std[1]
    print('Proportion of people doing home office among workers (MTMC):',
          str(weighted_avg * 100) + '% (+/-', str(weighted_std * 100) + ', n=' + str(nb_obs) + ')')


def run_simulation(data_file_directory_for_simulation, data_file_name_for_simulation,
                                        output_directory_for_simulation):
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

    b_single_household = Beta('b_single_household', 0, None, None, 1)
    b_couple_without_children = Beta('b_couple_without_children', 0, None, None, 1)
    b_couple_with_children = Beta('b_couple_with_children', 0, None, None, 1)
    b_single_parent_with_children = Beta('b_single_parent_with_children', 0, None, None, 1)
    b_not_family_household = Beta('b_not_family_household', 0, None, None, 1)

    b_public_transport_connection_quality_are_a = Beta('b_public_transport_connection_quality_are_a', 0, None, None, 1)
    b_public_transport_connection_quality_are_b = Beta('b_public_transport_connection_quality_are_b', 0, None, None, 1)
    b_public_transport_connection_quality_are_c = Beta('b_public_transport_connection_quality_are_c', 0, None, None, 1)
    b_public_transport_connection_quality_are_d = Beta('b_public_transport_connection_quality_are_d', 0, None, None, 1)
    b_public_transport_connection_quality_are_na = Beta('b_public_transport_connection_quality_are_na', 0, None, None,
                                                        0)

    b_urban = Beta('b_urban', 0, None, None, 1)
    b_rural = Beta('b_rural', 0, None, None, 1)
    b_intermediate = Beta('b_intermediate', 0, None, None, 1)

    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)

    b_business_sector_agriculture = Beta('b_business_sector_agriculture', 0, None, None, 0)
    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale = Beta('b_business_sector_wholesale', 0, None, None, 1)
    b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 0)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 1)
    b_business_sector_services_fC = Beta('b_business_sector_services_fC', 0, None, None, 0)
    b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 1)
    b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 1)
    b_business_sector_non_movers = Beta('b_business_sector_non_movers', 0, None, None, 0)
    b_executives = Beta('b_executives', 0, None, None, 0)
    b_german = Beta('b_german', 0, None, None, 0)
    b_nationality_ch_germany_france_italy_nw_e = Beta('b_nationality_ch_germany_france_italy_nw_e', 0, None, None, 0)
    # b_nationality_south_west_europe = Beta('b_nationality_south_west_europe', 0, None, None, 1)
    # b_nationality_southeast_europe = Beta('b_nationality_southeast_europe', 0, None, None, 1)
    b_several_part_time_jobs = Beta('b_several_part_time_jobs', 0, None, None, 0)
    # b_hh_income_na = Beta('B_hh_income_na', 0, None, None, 1)
    b_hh_income_8000_or_less = Beta('b_hh_income_8000_or_less', 0, None, None, 0)
    # b_hh_income_more_than_8000 = Beta('b_hh_income_more_than_8000', 0, None, None, 1)

    # Definition of new variables
    no_post_school_educ = education == 1
    secondary_education = education == 2
    tertiary_education = education == 3
    university = education == 4

    male = (sex == 1)

    public_transport_connection_quality_ARE_NA = (public_transport_connection_quality_ARE == 5)

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
    nationality_germany_austria_lichtenstein = nation == 1
    nationality_italy_vatican = nation == 2
    nationality_france_monaco_san_marino = nation == 3
    nationality_northwestern_europe = nation == 4
    nationality_eastern_europe = nation == 7
    hh_income_8000_or_less = (hh_income == 1) + (hh_income == 2) + (hh_income == 3) + (hh_income == 4)

    #  Utility
    U_home_office = alternative_specific_constant + \
                    b_executives * executives + \
                    b_no_post_school_education * no_post_school_educ + \
                    b_secondary_education * secondary_education + \
                    b_tertiary_education * tertiary_education + \
                    b_university * university + \
                    b_male * male + \
                    b_public_transport_connection_quality_are_na * public_transport_connection_quality_ARE_NA + \
                    b_home_work_distance * home_work_distance + \
                    models.piecewiseFormula(age, [0, 20, 35, 75, 200]) + \
                    b_business_sector_agriculture * business_sector_agriculture + \
                    b_business_sector_retail * business_sector_retail + \
                    b_business_sector_gastronomy * business_sector_gastronomy + \
                    b_business_sector_finance * business_sector_finance + \
                    b_business_sector_production * business_sector_production + \
                    b_business_sector_wholesale * business_sector_wholesale + \
                    b_business_sector_services_fC * business_sector_services_fC + \
                    b_business_sector_other_services * business_sector_other_services + \
                    b_business_sector_others * business_sector_others + \
                    b_business_sector_non_movers * business_sector_non_movers + \
                    b_german * german + \
                    b_nationality_ch_germany_france_italy_nw_e * nationality_switzerland + \
                    b_nationality_ch_germany_france_italy_nw_e * nationality_germany_austria_lichtenstein + \
                    b_nationality_ch_germany_france_italy_nw_e * nationality_italy_vatican + \
                    b_nationality_ch_germany_france_italy_nw_e * nationality_france_monaco_san_marino + \
                    b_nationality_ch_germany_france_italy_nw_e * nationality_northwestern_europe + \
                    b_nationality_ch_germany_france_italy_nw_e * nationality_eastern_europe + \
                    models.piecewiseFormula(work_percentage, [0, 90, 170]) + \
                    b_hh_income_8000_or_less * hh_income_8000_or_less
    U_no_home_office = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U_home_office,  # Yes or sometimes
         3: U_no_home_office}  # No

    av = {1: 1,
          3: 1}

    # The choice model is a logit, with availability conditions
    prob_home_office = models.logit(V, av, 1)
    prob_no_home_office = models.logit(V, av, 3)

    simulate = {'Prob. home office': prob_home_office,
                'Prob. no home office': prob_no_home_office}

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = 'logit_home_office_simul'
    # Get the betas from the estimation
    path_to_estimation_folder = Path('../data/output/models/estimation/')
    if os.path.isfile(path_to_estimation_folder / 'logit_home_office~00.pickle'):
        raise Exception('There are several model outputs! Careful.')
    results = res.bioResults(pickleFile=path_to_estimation_folder / 'logit_home_office.pickle')
    betas = results.getBetaValues()

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

    ''' Save the file '''
    output_directory = Path('../data/output/models/validation_with_SynPop/')
    data_file_name = 'persons_from_SynPop_with_probability_home_office.csv'
    df_persons.to_csv(output_directory / data_file_name, sep=',', index=False)
