from pathlib import Path
import pandas as pd
import os
import biogeme.results as res
import math
from apply_model_to_MTMC_data import apply_model_to_MTMC_data


def calibrate_the_constant():
    path_to_estimation_file = Path('../data/output/data/estimation/')
    estimation_file_name = 'persons.csv'
    observed_rate_of_home_office = compute_observed_rate_of_home_office(path_to_estimation_file, estimation_file_name)
    path_to_estimated_betas = Path('../data/output/models/estimation/')
    estimated_betas_name = 'logit_home_office'
    predicted_rate_of_home_office = compute_predicted_rate_of_home_office(path_to_estimation_file, estimation_file_name,
                                                                          path_to_estimated_betas, estimated_betas_name)
    # Get the betas from the estimation
    betas = get_estimated_betas(path_to_estimated_betas, estimated_betas_name)
    while abs(observed_rate_of_home_office - predicted_rate_of_home_office) > 0.001:
        betas = update_constant(betas, observed_rate_of_home_office, predicted_rate_of_home_office)
        predicted_rate_of_home_office = compute_predicted_rate_of_home_office(path_to_estimation_file, estimation_file_name,
                                                                              '', '', betas=betas)


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


def compute_predicted_rate_of_home_office(path_to_estimation_file, estimation_file_name,
                                          path_to_estimated_betas, estimated_betas_name, betas=None):
    ''' Simulate the model on the full dataset used for estimation '''
    output_directory_for_simulation = Path('../data/output/models/simulation_for_constant_calibration/')
    output_file_name = 'persons_with_probability_home_office.csv'
    apply_model_to_MTMC_data(path_to_estimation_file, estimation_file_name,
                             output_directory_for_simulation, output_file_name,
                             path_to_estimated_betas, estimated_betas_name, betas=betas)
    ''' compute the predicted rate of home office from the output of the simulation '''
    df_persons = pd.read_csv(output_directory_for_simulation / output_file_name)
    predicted_rate_of_home_office = df_persons['Prob. home office'].mean()
    return predicted_rate_of_home_office


def compute_observed_rate_of_home_office(path_to_estimation_file, estimation_file_name):
    df_persons = pd.read_csv(path_to_estimation_file / estimation_file_name, sep=';')
    observed_rate_of_home_office = df_persons['home_office'].mean()
    return observed_rate_of_home_office