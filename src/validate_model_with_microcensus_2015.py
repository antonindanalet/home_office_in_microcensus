import pandas as pd
from pathlib import Path
from estimate_choice_model_telecommuting import run_estimation
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std
from src.mtmc2015.apply_model_to_microcensus import apply_model_to_microcensus


def validate_model_with_microcensus_2015():
    """ This function validates the model internally. First, it decomposes the data in two sets:
    - one for the estimation (of 80% of the original dataset);
    - another one for the simulation (of 20% of the original dataset).
    Then, it estimates the model on 80% of the dataset, simulate it on the remaining 20%.
    Finally, it computes the predicted and observed proportions of people working from home in the 20%. """
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
                   output_file_name='logit_telecommuting_80')
    # Simulate the model on 20% of the data
    data_file_directory_for_simulation = Path('../data/output/data/internal_validation/simulation/')
    data_file_name_for_simulation = 'persons20.csv'
    output_directory_for_simulation = Path('../data/output/models/internal_validation/simulation/')
    output_file_name = 'persons20_with_probability_telecommuting.csv'
    path_to_estimated_betas = Path('../data/output/models/internal_validation/estimation/')
    estimated_betas_name = 'logit_telecommuting_80'
    apply_model_to_microcensus(data_file_directory_for_simulation, data_file_name_for_simulation,
                               output_directory_for_simulation, output_file_name,
                               path_to_estimated_betas, estimated_betas_name)
    # Compute the proportion of people doing home office in the data and in the simulation
    compute_proportion_of_people_telecommuting()


def compute_proportion_of_people_telecommuting():
    """ This function computes the observed and predicted proportion of people working from home
    (among the 20% of the original dataset). """
    ''' Get the data '''
    simulation_results_directory = Path('../data/output/models/internal_validation/simulation/')
    data_file_name = 'persons20_with_probability_telecommuting.csv'
    df_persons = pd.read_csv(simulation_results_directory / data_file_name, sep=',')
    print('Observed proportion of people telecommuting (unweighted):',
          str(100 * round(df_persons['telecommuting'].mean(), 3)) + '%')
    print('Predicted proportion of people telecommuting (unweighted):',
          str(100 * round(df_persons['Prob. telecommuting'].mean(), 3)) + '%')
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP',
                                                    list_of_columns=['telecommuting', 'Prob. telecommuting'])
    weighted_avg = round(weighted_avg_and_std[0]['telecommuting'][0], 3) * 100
    weighted_std = round(weighted_avg_and_std[0]['telecommuting'][1], 3) * 100
    print('Observed proportion of people telecommuting (weighted):', str(weighted_avg) + '% (+/-',
          str(weighted_std) + '%)')
    weighted_avg = round(weighted_avg_and_std[0]['Prob. telecommuting'][0], 3) * 100
    weighted_std = round(weighted_avg_and_std[0]['Prob. telecommuting'][1], 3) * 100
    print('Predicted proportion of people telecommuting (weighted):', str(weighted_avg) + '% (+/-',
          str(weighted_std) + '%)')


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
