import pandas as pd
from pathlib import Path
from estimate_choice_model_home_office import run_estimation


def validate_choice_model_home_office():
    # Read the data used for estimation
    df_persons = get_persons()
    # Save 80% of the data for estimation and 20% of the data for simulation for validation (and shuffles the data set)
    save_slices(df_persons)
    # Estimate the model on 80% of the data
    data_file_directory = Path('../data/output/data/validation/estimation/')
    data_file_name = 'persons80.csv'
    output_directory = '../data/output/models/validation/estimation/'
    run_estimation(data_file_directory, data_file_name, output_directory)
    # Simulate the model on 20% of the data

    # Compute the proportion of people doing home office in the data and in the simulation


def save_slices(df_persons):
    # Shuffle the data set (sampling the full fraction of the data, i.e., all data)
    df_persons = df_persons.sample(frac=1)
    # Save 80% of the data for estimation
    estimation_output_directory = Path('../data/output/data/validation/estimation/')
    estimation_data_file_name = 'persons80.csv'
    number_of_observations = len(df_persons)
    first_80_percent_observations = round(0.8 * number_of_observations)
    df_persons.head(first_80_percent_observations).to_csv(estimation_output_directory / estimation_data_file_name,
                                                          sep=';', index=False)
    # Save the remaining 20% of the data for simulation
    last_20_percent_of_observations = number_of_observations - first_80_percent_observations
    simulation_output_directory = Path('../data/output/data/validation/simulation/')
    simulation_data_file_name = 'persons20.csv'
    df_persons.tail(last_20_percent_of_observations).to_csv(simulation_output_directory / simulation_data_file_name,
                                                            sep=';', index=False)


def get_persons():
    full_sample_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    df_persons = pd.read_csv(full_sample_directory / data_file_name, sep=';')
    return df_persons
