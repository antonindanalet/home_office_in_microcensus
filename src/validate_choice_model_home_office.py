import pandas as pd
from pathlib import Path
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta, Derive
import os
from estimate_choice_model_home_office import run_estimation


def validate_choice_model_home_office():
    # Read the data used for estimation
    df_persons = get_persons()
    # Save 80% of the data for estimation and 20% of the data for simulation for validation (and shuffles the data set)
    save_slices(df_persons)
    # Estimate the model on 80% of the data
    data_file_directory_for_estimation = Path('../data/output/data/validation/estimation/')
    data_file_name_for_estimation = 'persons80.csv'
    output_directory_for_estimation = '../data/output/models/validation/estimation/'
    run_estimation(data_file_directory_for_estimation, data_file_name_for_estimation, output_directory_for_estimation)
    # Simulate the model on 20% of the data
    data_file_directory_for_simulation = Path('../data/output/data/validation/simulation/')
    data_file_name_for_simulation = 'persons20.csv'
    output_directory_for_simulation = '../data/output/models/validation/simulation/'
    run_simulation(data_file_directory_for_simulation, data_file_name_for_simulation, output_directory_for_simulation)
    # Compute the proportion of people doing home office in the data and in the simulation


def run_simulation(data_file_directory, data_file_name, output_directory):
    """
    :author: Antonin Danalet, based on the example '01logit_simul.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    Simulation with a binary logit model. Two alternatives: work from home at least some times, or not."""

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
    full_time_work = (ERWERB == 1)
    active_without_known_work_percentage = (ERWERB == 9)

    no_post_school_educ = (highest_educ == 1) + (highest_educ == 2) + (highest_educ == 3) + (highest_educ == 4)
    secondary_education = (highest_educ == 5) + (highest_educ == 6) + (highest_educ == 7) + (highest_educ == 8) + \
                          (highest_educ == 9) + (highest_educ == 10) + (highest_educ == 11) + (highest_educ == 12)
    tertiary_education = (highest_educ == 13) + (highest_educ == 14) + (highest_educ == 15) + (highest_educ == 16)
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

    home_work_distance = home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 1000.0

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
    V = {1: U,  # Yes or sometimes
         3: U_No_home_office}  # No

    av = {1: 1,
          3: 1}

    # The choice model is a logit, with availability conditions
    prob_home_office = models.logit(V, av, 1)
    prob_no_home_office = models.logit(V, av, 3)

    simulate = {'Prob. home office': prob_home_office,
                'Prob. no home office': prob_no_home_office}

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    standard_directory = os.getcwd()
    os.chdir(output_directory)

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = 'logit_home_office_simul'
    betas = {'ASC': xxx, ...}

    results = biogeme.simulate(theBetaValues=betas)
    print(results.describe())

    # Go back to the normal working directory
    os.chdir(standard_directory)


def save_slices(df_persons):
    # Shuffle the data set (sampling the full fraction of the data, i.e., all data)
    df_persons = df_persons.sample(frac=1)
    # Save 80% of the data for estimation
    estimation_output_directory = Path('../data/output/data/validation/estimation/')
    estimation_data_file_name = 'persons80.csv'
    number_of_observations = len(df_persons)
    first_80_percent_of_observations = round(0.8 * number_of_observations)
    df_persons.head(first_80_percent_of_observations).to_csv(estimation_output_directory / estimation_data_file_name,
                                                          sep=';', index=False)
    # Save the remaining 20% of the data for simulation
    last_20_percent_of_observations = number_of_observations - first_80_percent_of_observations
    simulation_output_directory = Path('../data/output/data/validation/simulation/')
    simulation_data_file_name = 'persons20.csv'
    df_persons.tail(last_20_percent_of_observations).to_csv(simulation_output_directory / simulation_data_file_name,
                                                            sep=';', index=False)


def get_persons():
    full_sample_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    df_persons = pd.read_csv(full_sample_directory / data_file_name, sep=';')
    return df_persons
