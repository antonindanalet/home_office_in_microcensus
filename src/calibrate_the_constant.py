from pathlib import Path
import pandas as pd
import os
import biogeme.results as res
import math
from src.utils_mtmc.apply_model_to_microcensus import apply_model_2015_to_microcensus, \
    apply_most_recent_model_to_microcensus
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std
from utils_synpop.apply_model_to_synthetic_population import get_predicted_rate_of_telecommuting, \
    apply_model_to_synthetic_population
from utils_synpop.compute_household_income_limit import compute_household_income_limit


def calibrate_the_constant_by_simulating_on_synthetic_population(betas):
    synpop_directory = Path('../data/output/models/validation_with_SynPop/')
    predicted_rate_of_telecommuting = get_predicted_rate_of_telecommuting(synpop_directory)
    # print('Proportion of home office (synpop):', predicted_rate_of_telecommuting)
    path_to_estimation_file = Path('../data/output/data/estimation/2015/')
    estimation_file_name = 'persons.csv'
    observed_rate_of_telecommuting = compute_observed_rate_of_telecommuting(path_to_estimation_file,
                                                                            estimation_file_name)
    household_income_limit = compute_household_income_limit(year=2017)
    while abs(observed_rate_of_telecommuting - predicted_rate_of_telecommuting) > 0.001:
        betas = update_constant(betas, observed_rate_of_telecommuting, predicted_rate_of_telecommuting)
        predicted_rate_of_telecommuting = compute_predicted_rate_of_telecommuting_for_syn_pop(betas,
                                                                                              household_income_limit)
    print('Final alternative specific constant:', betas['alternative_specific_constant'])
    return betas


def compute_predicted_rate_of_telecommuting_for_syn_pop(betas, household_income_limit):
    output_directory_for_simulation = Path('../data/output/models/simulation_for_constant_calibration/SynPop/')
    predicted_rate_of_telecommuting = apply_model_to_synthetic_population(betas, output_directory_for_simulation,
                                                                          household_income_limit, year=2017)
    return predicted_rate_of_telecommuting


def calibrate_the_constant_by_simulating_on_microcensus(model):
    path_to_estimation_file = Path('../data/output/data/estimation/2015/')
    estimation_file_name = 'persons.csv'
    observed_rate_of_telecommuting = compute_observed_rate_of_telecommuting(path_to_estimation_file,
                                                                            estimation_file_name)
    path_to_estimated_betas = Path('../data/output/models/estimation/' + model + '/')
    estimated_betas_name = 'logit_telecommuting_' + model
    predicted_rate_of_telecommuting = compute_predicted_rate_of_telecommuting_microcensus(path_to_estimation_file,
                                                                                          estimation_file_name,
                                                                                          path_to_estimated_betas,
                                                                                          estimated_betas_name,
                                                                                          model)
    # Get the betas from the estimation
    betas = get_estimated_betas(path_to_estimated_betas, estimated_betas_name)
    while abs(observed_rate_of_telecommuting - predicted_rate_of_telecommuting) > 0.001:
        betas = update_constant(betas, observed_rate_of_telecommuting, predicted_rate_of_telecommuting)
        predicted_rate_of_telecommuting = compute_predicted_rate_of_telecommuting_microcensus(path_to_estimation_file,
                                                                                              estimation_file_name, '',
                                                                                              '', model, betas=betas)
    print('Alternative specific constant used for internal validation:', betas['alternative_specific_constant'])
    # Remove the betas that are not used anymore
    keys = ['b_couple_without_children_2015', 'b_hh_income_na', 'b_home_work_distance_na', 'b_mobility_resource_na',
            'b_public_transport_connection_quality_na_home_2015', 'scale_2020']
    for key in keys:
        betas.pop(key)
    return betas


def update_constant(betas, observed_rate_of_telecommuting, predicted_rate_of_telecommuting):
    # Get the value of the alternative specific constant
    alternative_specific_constant = betas['alternative_specific_constant']
    # print('Alternative specific constant before update:', alternative_specific_constant)
    # Update the value of the alternative specific constant using the heuristic method of Train (2003)
    alternative_specific_constant += math.log(observed_rate_of_telecommuting) - \
                                     math.log(predicted_rate_of_telecommuting)
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


def compute_predicted_rate_of_telecommuting_microcensus(path_to_estimation_file, estimation_file_name,
                                                        path_to_estimated_betas, estimated_betas_name, model,
                                                        betas=None):
    """ First, this function applies the model on the full dataset of the Mobility and Transport Microcensus (MTMC) '15.
    This first step provides the probability to work from home for each person in the MTMC 2015
    Then, it computes the proportion of the population working from home using the weights of each individual.
    This provides an average representative for the full Swiss population. """
    ''' Simulate the model on the full dataset used for estimation '''
    output_directory_for_simulation = Path('../data/output/models/simulation_for_constant_calibration/MTMC/')
    output_file_name = 'persons_with_probability_telecommuting.csv'
    if model == '2015:':
        apply_model_2015_to_microcensus(path_to_estimation_file, estimation_file_name,
                                        output_directory_for_simulation, output_file_name,
                                        path_to_estimated_betas, estimated_betas_name, betas=betas)
    elif model == '2015_2020':
        apply_most_recent_model_to_microcensus(path_to_estimation_file, estimation_file_name,
                                               output_directory_for_simulation, output_file_name,
                                               path_to_estimated_betas, estimated_betas_name, betas=betas)
    ''' compute the predicted rate of home office from the output of the simulation '''
    df_persons = pd.read_csv(output_directory_for_simulation / output_file_name)
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP', list_of_columns=['Prob. telecommuting'])
    predicted_rate_of_telecommuting = weighted_avg_and_std[0]['Prob. telecommuting'][0]
    return predicted_rate_of_telecommuting


def compute_observed_rate_of_telecommuting(path_to_estimation_file, estimation_file_name):
    df_persons = pd.read_csv(path_to_estimation_file / estimation_file_name, sep=';')
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP', list_of_columns=['telecommuting'])
    observed_rate_of_telecommuting = weighted_avg_and_std[0]['telecommuting'][0]
    return observed_rate_of_telecommuting
