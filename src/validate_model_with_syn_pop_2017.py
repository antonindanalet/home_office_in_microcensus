from pathlib import Path
from utils_synpop.generate_data_file_for_simulation import generate_data_file_for_simulation
from utils_synpop.compute_household_income_limit import compute_household_income_limit
from utils_synpop.apply_model_to_synthetic_population import apply_model_to_synthetic_population
from utils_mtmc.get_percentage_telecommuting import get_percentage_telecommuting


def validate_model_with_syn_pop_2017(betas):
    output_directory_for_simulation = Path('../data/output/models/validation_with_SynPop/')
    ''' External validation using a synthetic population '''
    # Prepare the data for PandasBiogeme
    generate_data_file_for_simulation(year=2017)
    # Definition of the household income limit corresponding to the distribution of the MTMC
    household_income_limit = compute_household_income_limit(year=2017)
    predicted_rate_of_home_office = apply_model_to_synthetic_population(betas, output_directory_for_simulation,
                                                                        household_income_limit, year=2017)
    # Compare rate of home office in the MTMC and in the synthetic population
    get_percentage_telecommuting(2015)
    print('Proportion of telecommuting (synpop):', predicted_rate_of_home_office)
