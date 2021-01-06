from pathlib import Path
import pandas as pd
import os
import biogeme.results as res
import math
from src.mtmc2015.apply_model_to_microcensus import apply_model_to_microcensus
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std
from utils_synpop.apply_model_to_synthetic_population import get_predicted_rate_of_home_office, \
    apply_model_to_synthetic_population
from utils_synpop.compute_household_income_limit import compute_household_income_limit


def calibrate_the_constant_by_simulating_on_synthetic_population(betas):
    synpop_directory = Path('../data/output/models/validation_with_SynPop/')
    predicted_rate_of_home_office = get_predicted_rate_of_home_office(synpop_directory)
    # print('Proportion of home office (synpop):', predicted_rate_of_home_office)
    path_to_estimation_file = Path('../data/output/data/estimation/')
    estimation_file_name = 'persons.csv'
    observed_rate_of_home_office = compute_observed_rate_of_home_office(path_to_estimation_file, estimation_file_name)
    household_income_limit = compute_household_income_limit(year=2017)
    while abs(observed_rate_of_home_office - predicted_rate_of_home_office) > 0.001:
        betas = update_constant(betas, observed_rate_of_home_office, predicted_rate_of_home_office)
        # print(betas['alternative_specific_constant'])
        predicted_rate_of_home_office = compute_predicted_rate_of_home_office_for_syn_pop(betas, household_income_limit)
        # print('Final beta:', betas['alternative_specific_constant'])
    print('Final alternative specific constant:', betas['alternative_specific_constant'])
    return betas


def compute_predicted_rate_of_home_office_for_syn_pop(betas, household_income_limit):
    output_directory_for_simulation = Path('../data/output/models/simulation_for_constant_calibration/SynPop/')
    predicted_rate_of_home_office = apply_model_to_synthetic_population(betas, output_directory_for_simulation,
                                                                        household_income_limit, year=2017)
    return predicted_rate_of_home_office


def calibrate_the_constant_by_simulating_on_microcensus():
    path_to_estimation_file = Path('../data/output/data/estimation/')
    estimation_file_name = 'persons.csv'
    observed_rate_of_home_office = compute_observed_rate_of_home_office(path_to_estimation_file, estimation_file_name)
    path_to_estimated_betas = Path('../data/output/models/estimation/')
    estimated_betas_name = 'logit_home_office'
    predicted_rate_of_home_office = compute_predicted_rate_of_home_office_for_microcensus(path_to_estimation_file,
                                                                                          estimation_file_name,
                                                                                          path_to_estimated_betas,
                                                                                          estimated_betas_name)
    # Get the betas from the estimation
    betas = get_estimated_betas(path_to_estimated_betas, estimated_betas_name)
    while abs(observed_rate_of_home_office - predicted_rate_of_home_office) > 0.001:
        betas = update_constant(betas, observed_rate_of_home_office, predicted_rate_of_home_office)
        predicted_rate_of_home_office = compute_predicted_rate_of_home_office_for_microcensus(path_to_estimation_file,
                                                                                              estimation_file_name, '',
                                                                                              '', betas=betas)
    print('Alternative specific constant used for internal validation:', betas['alternative_specific_constant'])
    return betas


def update_constant(betas, observed_rate_of_home_office, predicted_rate_of_home_office):
    # Get the value of the alternative specific constant
    alternative_specific_constant = betas['alternative_specific_constant']
    # print('Alternative specific constant before update:', alternative_specific_constant)
    # Update the value of the alternative specific constant using the heuristic method of Train (2003)
    alternative_specific_constant += math.log(observed_rate_of_home_office) - math.log(predicted_rate_of_home_office)
    # print('Alternative specific constant after update:', alternative_specific_constant)
    # Update the list of betas
    betas['alternative_specific_constant'] = alternative_specific_constant
    return betas


def get_estimated_betas(path_to_estimated_betas, estimated_betas_name):
    if os.path.isfile(path_to_estimated_betas / (estimated_betas_name + '~00.pickle')):
        print('WARNING: There are several model outputs!')
    results = res.bioResults(pickleFile=path_to_estimated_betas / (estimated_betas_name + '.pickle'))
    betas = results.getBetaValues()
    return betas


def compute_predicted_rate_of_home_office_for_microcensus(path_to_estimation_file, estimation_file_name,
                                                          path_to_estimated_betas, estimated_betas_name, betas=None):
    """ First, this function applies the model on the full dataset of the Mobility and Transport Microcensus (MTMC) '15.
    This first step provides the probability to work from home for each person in the MTMC 2015
    Then, it computes the proportion of the population working from home using the weights of each individual.
    This provides an average representative for the full Swiss population. """
    ''' Simulate the model on the full dataset used for estimation '''
    output_directory_for_simulation = Path('../data/output/models/simulation_for_constant_calibration/MTMC/')
    output_file_name = 'persons_with_probability_home_office.csv'
    apply_model_to_microcensus(path_to_estimation_file, estimation_file_name,
                               output_directory_for_simulation, output_file_name,
                               path_to_estimated_betas, estimated_betas_name, betas=betas)
    ''' compute the predicted rate of home office from the output of the simulation '''
    df_persons = pd.read_csv(output_directory_for_simulation / output_file_name)
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP', list_of_columns=['Prob. home office'])
    predicted_rate_of_home_office = weighted_avg_and_std[0]['Prob. home office'][0]
    return predicted_rate_of_home_office


def compute_observed_rate_of_home_office(path_to_estimation_file, estimation_file_name):
    df_persons = pd.read_csv(path_to_estimation_file / estimation_file_name, sep=';')
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP', list_of_columns=['home_office'])
    observed_rate_of_home_office = weighted_avg_and_std[0]['home_office'][0]
    return observed_rate_of_home_office
