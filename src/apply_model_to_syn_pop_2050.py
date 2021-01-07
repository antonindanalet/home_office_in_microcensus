from pathlib import Path
from utils_synpop.generate_data_file_for_simulation import generate_data_file_for_simulation
from utils_synpop.compute_household_income_limit import compute_household_income_limit
from utils_synpop.apply_model_to_synthetic_population import apply_model_to_synthetic_population


def apply_model_to_syn_pop_2050(betas):
    for year in [2030, 2040, 2050]:
        output_directory_for_simulation = Path('../data/output/models/application_to_SynPop_' + str(year) + '/')
        ''' External validation using a synthetic population '''
        # Prepare the data for PandasBiogeme
        generate_data_file_for_simulation(year)
        # Definition of the household income limit corresponding to the distribution of the MTMC
        household_income_limit = compute_household_income_limit(year)
        print('Household income limit used in', str(year) + ':', household_income_limit)
        predicted_rate_of_telecommuting = apply_model_to_synthetic_population(betas, output_directory_for_simulation,
                                                                            household_income_limit, year)
        print('Proportion of telecommuting (synpop) in', str(year) + ':', predicted_rate_of_telecommuting)
