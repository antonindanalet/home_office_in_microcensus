import pandas as pd
from pathlib import Path
from estimate_choice_model_telecommuting import run_estimation
# from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std
from src.utils_mtmc.apply_model_to_microcensus import apply_model_2015_to_microcensus
import os


def validate_model_with_microcensus_2015():
    """ This function validates the model internally. First, it decomposes the data in two sets:
    - one for the estimation (of 80% of the original dataset);
    - another one for the simulation (of 20% of the original dataset).
    Then, it estimates the model on 80% of the dataset, simulate it on the remaining 20%.
    Finally, it computes the predicted and observed proportions of people working from home in the 20%. """
    # Read the complete dataset, used for estimation
    df_persons = get_persons()
    # Running the validation process nb_iter times and keeping some information
    nb_iter = 10
    sum_observed_proportion_of_people_telecommuting = 0
    sum_predicted_proportion_of_people_telecommuting = 0
    min_observed_proportion_of_people_telecommuting = 1
    max_observed_proportion_of_people_telecommuting = 0
    min_predicted_proportion_of_people_telecommuting = 1
    max_predicted_proportion_of_people_telecommuting = 0
    largest_difference_of_proportion = 0
    smallest_different_of_proportion = 1
    for i in range(1, nb_iter+1):
        # Save 80% of the data for estimation and 20% of the data for simulation for internal validation
        # (and shuffles the data set)
        save_slices(df_persons, i)
        # Estimate the model on 80% of the data
        data_file_directory_for_estimation = Path('../data/output/data/internal_validation/estimation/')
        data_file_name_for_estimation = 'persons80.csv'
        output_directory_for_estimation = Path('../data/output/models/internal_validation/estimation/')
        run_estimation(data_file_directory_for_estimation, data_file_name_for_estimation,
                       output_directory_for_estimation, output_file_name='logit_telecommuting_80')
        # Simulate the model on 20% of the data
        data_file_directory_for_simulation = Path('../data/output/data/internal_validation/simulation/')
        data_file_name_for_simulation = 'persons20.csv'
        output_directory_for_simulation = Path('../data/output/models/internal_validation/simulation/')
        output_file_name = 'persons20_with_probability_telecommuting.csv'
        path_to_estimated_betas = output_directory_for_estimation
        estimated_betas_name = 'logit_telecommuting_80'
        apply_model_2015_to_microcensus(data_file_directory_for_simulation, data_file_name_for_simulation,
                                        output_directory_for_simulation, output_file_name,
                                        path_to_estimated_betas, estimated_betas_name)
        # Compute the proportion of people doing home office in the data and in the simulation
        observed_proportion_of_people_telecommuting, predicted_proportion_of_people_telecommuting = \
            compute_proportion_of_people_telecommuting()
        sum_observed_proportion_of_people_telecommuting += observed_proportion_of_people_telecommuting
        sum_predicted_proportion_of_people_telecommuting += predicted_proportion_of_people_telecommuting
        if observed_proportion_of_people_telecommuting < min_observed_proportion_of_people_telecommuting:
            min_observed_proportion_of_people_telecommuting = observed_proportion_of_people_telecommuting
        if predicted_proportion_of_people_telecommuting < min_predicted_proportion_of_people_telecommuting:
            min_predicted_proportion_of_people_telecommuting = predicted_proportion_of_people_telecommuting
        if observed_proportion_of_people_telecommuting > max_observed_proportion_of_people_telecommuting:
            max_observed_proportion_of_people_telecommuting = observed_proportion_of_people_telecommuting
        if predicted_proportion_of_people_telecommuting > max_predicted_proportion_of_people_telecommuting:
            max_predicted_proportion_of_people_telecommuting = predicted_proportion_of_people_telecommuting
        difference_of_proportion = abs(predicted_proportion_of_people_telecommuting -
                                       observed_proportion_of_people_telecommuting)
        if difference_of_proportion > largest_difference_of_proportion:
            largest_difference_of_proportion = difference_of_proportion
        if difference_of_proportion < smallest_different_of_proportion:
            smallest_different_of_proportion = difference_of_proportion
        # Delete the estimation files
        os.remove(output_directory_for_estimation / 'logit_telecommuting_80.html')
        os.remove(output_directory_for_estimation / 'logit_telecommuting_80.pickle')
        os.remove(output_directory_for_estimation / 'logit_telecommuting_80.tex')
    print('Observed proportion of people telecommuting (unweighted, average on', nb_iter, 'runs):',
          sum_observed_proportion_of_people_telecommuting / nb_iter,
          '(min:', str(min_observed_proportion_of_people_telecommuting) +
          ', max:', str(max_observed_proportion_of_people_telecommuting) + ')')
    print('Predicted proportion of people telecommuting (unweighted, average on', nb_iter, 'runs):',
          sum_predicted_proportion_of_people_telecommuting / nb_iter,
          '(min:', str(min_predicted_proportion_of_people_telecommuting) +
          ', max:', str(max_predicted_proportion_of_people_telecommuting) + ')')
    print('Largest difference in', nb_iter, 'runs:', largest_difference_of_proportion)
    print('Smallest difference in', nb_iter, 'runs:', smallest_different_of_proportion)


def compute_proportion_of_people_telecommuting():
    """ This function computes the observed and predicted proportion of people working from home
    (among the 20% of the original dataset). """
    ''' Get the data '''
    simulation_results_directory = Path('../data/output/models/internal_validation/simulation/')
    data_file_name = 'persons20_with_probability_telecommuting.csv'
    df_persons = pd.read_csv(simulation_results_directory / data_file_name, sep=',')
    observed_proportion_of_people_telecommuting = df_persons['telecommuting'].mean()
    # print('Observed proportion of people telecommuting (unweighted):',
    #       str(100 * round(observed_proportion_of_people_telecommuting, 3)) + '%')
    predicted_proportion_of_people_telecommuting = df_persons['Prob. telecommuting'].mean()
    return observed_proportion_of_people_telecommuting, predicted_proportion_of_people_telecommuting
    # print('Predicted proportion of people telecommuting (unweighted):',
    #       str(100 * round(predicted_proportion_of_people_telecommuting, 3)) + '%')
    # weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP',
    #                                                 list_of_columns=['telecommuting', 'Prob. telecommuting'])
    # weighted_avg = round(weighted_avg_and_std[0]['telecommuting'][0], 3) * 100
    # weighted_std = round(weighted_avg_and_std[0]['telecommuting'][1], 3) * 100
    # print('Observed proportion of people telecommuting (weighted):', str(weighted_avg) + '% (+/-',
    #       str(weighted_std) + '%)')
    # weighted_avg = round(weighted_avg_and_std[0]['Prob. telecommuting'][0], 3) * 100
    # weighted_std = round(weighted_avg_and_std[0]['Prob. telecommuting'][1], 3) * 100
    # print('Predicted proportion of people telecommuting (weighted):', str(weighted_avg) + '% (+/-',
    #       str(weighted_std) + '%)')


def save_slices(df_persons, i):
    # Shuffle the data set (sampling the full fraction of the data, i.e., all data)
    # 'random_state' as int defines the seed for random number generator. Defined for reproducibility.
    df_persons = df_persons.sample(frac=1, random_state=42+i)
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
    full_sample_directory = Path('../data/output/data/estimation/2015/')
    data_file_name = 'persons.csv'
    df_persons = pd.read_csv(full_sample_directory / data_file_name, sep=';')
    return df_persons
