import pandas as pd
from pathlib import Path
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta, DefineVariable
import biogeme.results as res
import os
from estimate_choice_model_home_office import run_estimation


def validate_choice_model_home_office():
    ''' Internal cross internal_validation '''
    # Read the complete dataset, used for estimation
    df_persons = get_persons()
    # Save 80% of the data for estimation and 20% of the data for simulation for internal validation
    # (and shuffles the data set)
    save_slices(df_persons)
    # Estimate the model on 80% of the data
    data_file_directory_for_estimation = Path('../data/output/data/internal_validation/estimation/')
    data_file_name_for_estimation = 'persons80.csv'
    output_directory_for_estimation = Path('../data/output/models/internal_validation/estimation/')
    run_estimation(data_file_directory_for_estimation, data_file_name_for_estimation, output_directory_for_estimation,
                   output_file_name='logit_home_office_80')
    # Simulate the model on 20% of the data
    data_file_directory_for_simulation = Path('../data/output/data/internal_validation/simulation/')
    data_file_name_for_simulation = 'persons20.csv'
    output_directory_for_simulation = Path('../data/output/models/internal_validation/simulation/')
    apply_model_to_MTMC_data(data_file_directory_for_simulation, data_file_name_for_simulation,
                             output_directory_for_simulation)
    # Compute the proportion of people doing home office in the data and in the simulation
    compute_proportion_of_people_doing_home_office()


def compute_proportion_of_people_doing_home_office():
    ''' Get the data '''
    simulation_results_directory = Path('../data/output/models/internal_validation/simulation/')
    data_file_name = 'persons20_with_probability_home_office.csv'
    df_persons = pd.read_csv(simulation_results_directory / data_file_name, sep=',')
    print('Observed proportion of people doing home office:', df_persons['home_office'].mean())
    print('Predicted proportion of people doing home office:', df_persons['Prob. home office'].mean())


def apply_model_to_MTMC_data(data_file_directory, data_file_name, output_directory):
    """
    :author: Antonin Danalet, based on the example '01logit_simul.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    Simulation with a binary logit model. Two alternatives: work from home at least some times, or not."""

    # Read the data
    df_persons = pd.read_csv(data_file_directory / data_file_name, ';')
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
    b_employees = Beta('b_employees', 0, None, None, 1)
    b_executives = Beta('b_executives', 0, None, None, 0)
    b_german = Beta('b_german', 0, None, None, 0)
    b_nationality_ch_germany_france_italy_nw_e = Beta('b_nationality_ch_germany_france_italy_nw_e', 0, None, None, 0)
    b_nationality_south_west_europe = Beta('b_nationality_south_west_europe', 0, None, None, 1)
    b_nationality_southeast_europe = Beta('b_nationality_southeast_europe', 0, None, None, 1)
    b_several_part_time_jobs = Beta('b_several_part_time_jobs', 0, None, None, 0)
    b_hh_income_na = Beta('B_hh_income_na', 0, None, None, 1)
    b_hh_income_8000_or_less = Beta('b_hh_income_8000_or_less', 0, None, None, 0)
    b_hh_income_more_than_8000 = Beta('b_hh_income_more_than_8000', 0, None, None, 1)

    # Definition of new variables
    no_post_school_educ = ((highest_educ == 1) | (highest_educ == 2) | (highest_educ == 3) | (highest_educ == 4))
    secondary_education = ((highest_educ == 5) | (highest_educ == 6) | (highest_educ == 7) | (highest_educ == 8) |
                           (highest_educ == 9) | (highest_educ == 10) | (highest_educ == 11) | (highest_educ == 12))
    tertiary_education = ((highest_educ == 13) | (highest_educ == 14) | (highest_educ == 15) | (highest_educ == 16))
    university = (highest_educ == 17) * 10

    male = (sex == 1)

    single_household = (hh_type == 10)
    couple_without_children = (hh_type == 210)
    couple_with_children = (hh_type == 220)
    single_parent_with_children = (hh_type == 230)
    not_family_household = (hh_type == 30)

    public_transport_connection_quality_ARE_A = (public_transport_connection_quality_ARE == 1)
    public_transport_connection_quality_ARE_B = (public_transport_connection_quality_ARE == 2)
    public_transport_connection_quality_ARE_C = (public_transport_connection_quality_ARE == 3)
    public_transport_connection_quality_ARE_D = (public_transport_connection_quality_ARE == 4)
    public_transport_connection_quality_ARE_NA = (public_transport_connection_quality_ARE == 5)

    urban = (urban_typology == 1)
    rural = (urban_typology == 3)
    intermediate = (urban_typology == 2)

    home_work_distance = (home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0)

    business_sector_agriculture = DefineVariable('business_sector_agriculture', 1 <= noga_08 <= 7, database)
    business_sector_retail = DefineVariable('business_sector_retail', 47 <= noga_08 <= 47, database)
    business_sector_gastronomy = DefineVariable('business_sector_gastronomy', 55 <= noga_08 <= 57, database)
    business_sector_finance = DefineVariable('business_sector_finance', 64 <= noga_08 <= 67, database)
    business_sector_production = DefineVariable('business_sector_production',
                                                (10 <= noga_08 <= 35) | (40 <= noga_08 <= 44), database)
    business_sector_wholesale = DefineVariable('business_sector_wholesale',
                                               (45 <= noga_08 <= 45) | (49 <= noga_08 <= 54), database)
    business_sector_services_fC = DefineVariable('business_sector_services_fC',
                                                 (60 <= noga_08 <= 63) | (69 <= noga_08 <= 83) | (noga_08 == 58),
                                                 database)
    business_sector_other_services = DefineVariable('business_sector_other_services',
                                                    (86 <= noga_08 <= 90) | (92 <= noga_08 <= 96) | (noga_08 == 59) |
                                                    (noga_08 == 68),
                                                    database)
    business_sector_others = DefineVariable('business_sector_others', 97 <= noga_08 <= 98, database)
    business_sector_non_movers = DefineVariable('business_sector_non_movers',
                                                (8 <= noga_08 <= 9) | (36 <= noga_08 <= 39) | (84 <= noga_08 <= 85) |
                                                (noga_08 == 91) | (noga_08 == 99),
                                                database)

    employees = work_position == 2
    executives = (work_position == 3) + (work_position == 1)

    german = language == 1

    nationality_switzerland = nation == 8100
    nationality_germany_austria_lichtenstein = (nation == 8207) + (nation == 8229) + (nation == 8222)
    nationality_italy_vatican = (nation == 8218) + (nation == 8241)
    nationality_france_monaco_san_marino = (nation == 8212) + (nation == 8226) + (nation == 8233)
    nationality_northwestern_europe = (nation == 8204) + (nation == 8223) + (nation == 8227) + (nation == 8206) + \
                                      (nation == 8211) + (nation == 8215) + (nation == 8216) + (nation == 8217) + \
                                      (nation == 8228) + (nation == 8234)
    nationality_south_west_europe = (nation == 8231) + (nation == 8236) + (nation == 8202)
    nationality_southeast_europe = (nation == 8224) + (nation == 8201) + (nation == 8214) + (nation == 8256) + \
                                   (nation == 8250) + (nation == 8251) + (nation == 8252) + (nation == 8255) + \
                                   (nation == 8205) + (nation == 8239) + (nation == 8242) + (nation == 8248) + \
                                   (nation == 8254)
    nationality_eastern_europe = (nation == 8230) + (nation == 8232) + (nation == 8240) + (nation == 8243) + \
                                 (nation == 8244) + (nation == 8263) + (nation == 8265) + (nation == 8266) + \
                                 (nation == 8260) + (nation == 8261) + (nation == 8262)

    # several_part_time_jobs = full_part_time_job == 3
    work_percentage = DefineVariable('work_percentage',
                                     (full_part_time_job == 1) * 100 +
                                     percentage_first_part_time_job * (percentage_first_part_time_job > 0) +
                                     percentage_second_part_time_job * (percentage_second_part_time_job > 0),
                                     database)

    hh_income_na = hh_income == -98
    hh_income_less_than_2000 = hh_income == 1
    hh_income_2000_to_4000 = hh_income == 2
    hh_income_4001_to_6000 = hh_income == 3
    hh_income_6001_to_8000 = hh_income == 4
    hh_income_8001_to_10000 = hh_income == 5
    hh_income_10001_to_12000 = hh_income == 6
    hh_income_12001_to_14000 = hh_income == 7
    hh_income_14001_to_16000 = hh_income == 8
    hh_income_more_than_16000 = hh_income == 9

    #  Utility
    U = alternative_specific_constant + \
        b_executives * executives + \
        b_employees * employees + \
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
        b_nationality_south_west_europe * nationality_south_west_europe + \
        b_nationality_southeast_europe * nationality_southeast_europe + \
        b_nationality_ch_germany_france_italy_nw_e * nationality_eastern_europe + \
        models.piecewiseFormula(work_percentage, [0, 90, 170]) + \
        b_hh_income_na * hh_income_na + \
        b_hh_income_8000_or_less * hh_income_less_than_2000 + \
        b_hh_income_8000_or_less * hh_income_2000_to_4000 + \
        b_hh_income_8000_or_less * hh_income_4001_to_6000 + \
        b_hh_income_8000_or_less * hh_income_6001_to_8000 + \
        b_hh_income_more_than_8000 * hh_income_8001_to_10000 + \
        b_hh_income_more_than_8000 * hh_income_10001_to_12000 + \
        b_hh_income_more_than_8000 * hh_income_12001_to_14000 + \
        b_hh_income_more_than_8000 * hh_income_14001_to_16000 + \
        b_hh_income_more_than_8000 * hh_income_more_than_16000
    U_No_home_office = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U,  # Yes or sometimes
         0: U_No_home_office}  # No

    av = {1: 1,
          0: 1}

    # The choice model is a logit, with availability conditions
    prob_home_office = models.logit(V, av, 1)
    prob_no_home_office = models.logit(V, av, 0)

    simulate = {'Prob. home office': prob_home_office,
                'Prob. no home office': prob_no_home_office}

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = 'logit_home_office_simul'
    # Get the betas from the estimation
    path_to_estimation_folder = Path('../data/output/models/internal_validation/estimation/')
    if os.path.isfile(path_to_estimation_folder / 'logit_home_office_80~00.pickle'):
        print('WARNING: There are several model outputs!')
    results = res.bioResults(pickleFile=path_to_estimation_folder / 'logit_home_office_80.pickle')
    betas = results.getBetaValues()

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    standard_directory = os.getcwd()
    os.chdir(output_directory)

    results = biogeme.simulate(theBetaValues=betas)
    print(results.describe())
    df_persons = pd.concat([df_persons, results], axis=1)

    # Go back to the normal working directory
    os.chdir(standard_directory)

    ''' Save the file '''
    output_directory = Path('../data/output/models/internal_validation/simulation/')
    data_file_name = 'persons20_with_probability_home_office.csv'
    df_persons.to_csv(output_directory / data_file_name, sep=',', index=False)


def save_slices(df_persons):
    # Shuffle the data set (sampling the full fraction of the data, i.e., all data)
    df_persons = df_persons.sample(frac=1)
    # Save 80% of the data for estimation
    estimation_output_directory = Path('../data/output/data/internal_validation/estimation/')
    estimation_data_file_name = 'persons80.csv'
    number_of_observations = len(df_persons)
    first_80_percent_of_observations = round(0.8 * number_of_observations)
    df_persons.head(first_80_percent_of_observations).to_csv(estimation_output_directory / estimation_data_file_name,
                                                             sep=';', index=False)
    # Save the remaining 20% of the data for simulation
    last_20_percent_of_observations = number_of_observations - first_80_percent_of_observations
    simulation_output_directory = Path('../data/output/data/internal_validation/simulation/')
    simulation_data_file_name = 'persons20.csv'
    df_persons.tail(last_20_percent_of_observations).to_csv(simulation_output_directory / simulation_data_file_name,
                                                            sep=';', index=False)


def get_persons():
    full_sample_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    df_persons = pd.read_csv(full_sample_directory / data_file_name, sep=';')
    return df_persons
