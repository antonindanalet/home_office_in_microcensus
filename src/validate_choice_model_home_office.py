import pandas as pd
from pathlib import Path
from estimate_choice_model_home_office import run_estimation
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std
from apply_model_to_MTMC_data import apply_model_to_MTMC_data


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
    output_file_name = 'persons20_with_probability_home_office.csv'
    path_to_estimated_betas = Path('../data/output/models/internal_validation/estimation/')
    estimated_betas_name = 'logit_home_office_80'
    apply_model_to_MTMC_data(data_file_directory_for_simulation, data_file_name_for_simulation,
                             output_directory_for_simulation, output_file_name,
                             path_to_estimated_betas, estimated_betas_name)
    # Compute the proportion of people doing home office in the data and in the simulation
    compute_proportion_of_people_doing_home_office()


def compute_proportion_of_people_doing_home_office():
    ''' Get the data '''
    simulation_results_directory = Path('../data/output/models/internal_validation/simulation/')
    data_file_name = 'persons20_with_probability_home_office.csv'
    df_persons = pd.read_csv(simulation_results_directory / data_file_name, sep=',')
    print(df_persons.columns)
    print('Observed proportion of people doing home office (unweighted):',
          str(100 * round(df_persons['home_office'].mean(), 3)) + '%')
    print('Predicted proportion of people doing home office (unweighted):',
          str(100 * round(df_persons['Prob. home office'].mean(), 3)) + '%')
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP',
                                                    list_of_columns=['home_office', 'Prob. home office'])
    weighted_avg = round(weighted_avg_and_std[0]['home_office'][0], 3) * 100
    weighted_std = round(weighted_avg_and_std[0]['home_office'][1], 3) * 100
    print('Observed proportion of people doing home office (weighted):', str(weighted_avg) + '% (+/-',
          str(weighted_std) + '%)')
    weighted_avg = round(weighted_avg_and_std[0]['Prob. home office'][0], 3) * 100
    weighted_std = round(weighted_avg_and_std[0]['Prob. home office'][1], 3) * 100
    print('Predicted proportion of people doing home office (weighted):', str(weighted_avg) + '% (+/-',
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
