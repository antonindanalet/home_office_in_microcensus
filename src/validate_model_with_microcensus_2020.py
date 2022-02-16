from pathlib import Path
import pandas as pd
import biogeme.results as res
from utils_mtmc.generate_data_file import generate_data_file
from src.utils_mtmc.apply_model_to_microcensus import apply_model_2015_to_microcensus


def validate_model_with_microcensus_2020():
    """ This function validates the model externally with the Mobility and Transport Microcensus 2020.
    It checks the temporal stability of the model. In particular:
    - it uses the estimation of the parameters on the 2015 dataset and
    - it simulates the choice using the data of 2020.
    Finally, it computes the predicted and observed proportions of people working from home in 2020. """
    # Prepare the data of 2020 in the correct format
    generate_data_file(2020)
    # Simulate the model on the data of 2020
    data_file_directory_for_simulation = Path('../data/output/data/validation_with_MTMC_2020/')
    data_file_name_for_simulation = 'persons.csv'
    output_directory_for_simulation = Path('../data/output/models/validation_with_MTMC_2020/')
    output_file_name = 'persons_with_probability_telecommuting.csv'
    path_to_estimated_betas_2015 = Path('../data/output/models/estimation/2015/')
    estimated_betas_name_2015 = 'logit_telecommuting_2015'
    results = res.bioResults(pickleFile=path_to_estimated_betas_2015 / (estimated_betas_name_2015 + '.pickle'))
    betas = results.getBetaValues()
    betas['b_hh_income_na'] = 0
    betas['b_home_work_distance_na'] = 0
    betas['b_home_work_distance_na'] = 0
    apply_model_2015_to_microcensus(data_file_directory_for_simulation, data_file_name_for_simulation,
                                    output_directory_for_simulation, output_file_name,
                                    path_to_estimated_betas_2015, estimated_betas_name_2015, betas=betas)
    # Compute the proportion of people doing home office in the data and in the simulation
    simulation_results_directory = Path('../data/output/models/validation_with_MTMC_2020/')
    data_file_name = 'persons_with_probability_telecommuting.csv'
    df_persons = pd.read_csv(simulation_results_directory / data_file_name, sep=',')
    observed_proportion_of_people_telecommuting = df_persons['telecommuting'].mean()
    predicted_proportion_of_people_telecommuting = df_persons['Prob. telecommuting'].mean()
    print('Observed proportion of people telecommuting (unweighted):', observed_proportion_of_people_telecommuting)
    print('Predicted proportion of people telecommuting (unweighted):', predicted_proportion_of_people_telecommuting)
