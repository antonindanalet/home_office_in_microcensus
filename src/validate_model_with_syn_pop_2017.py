from pathlib import Path
from utils_synpop.generate_data_file_for_simulation import generate_data_file_for_simulation
from utils_mtmc.get_mtmc_files import get_zp
from utils_mtmc.define_telecommuting_variable import define_telecommuting_variable
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std
from utils_synpop.compute_household_income_limit import compute_household_income_limit
from utils_synpop.apply_model_to_synthetic_population import apply_model_to_synthetic_population


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
    descr_stat_mtmc()
    print('Proportion of telecommuting (synpop):', predicted_rate_of_home_office)


def descr_stat_mtmc():
    # Get the data
    selected_columns = ['HHNR', 'WP', 'f81300', 'f81400']
    df_zp = get_zp(2015, selected_columns=selected_columns)
    df_zp = df_zp.rename(columns={'f81300': 'telecommuting_is_possible',
                                  'f81400': 'percentage_telecommuting'})
    ''' Removing people who did not get the question or did not answer. '''
    df_zp.drop(df_zp[df_zp.telecommuting_is_possible < 0].index, inplace=True)
    df_zp.drop(df_zp[df_zp.percentage_telecommuting == -98].index, inplace=True)
    df_zp.drop(df_zp[df_zp.percentage_telecommuting == -97].index, inplace=True)
    df_zp['telecommuting'] = df_zp.apply(define_telecommuting_variable, axis=1)
    # Percentage of people doing home office among people working (and who answered to the question about home office)
    weighted_avg_and_std = get_weighted_avg_and_std(df_zp, weights='WP', list_of_columns=['telecommuting'])
    weighted_avg = round(weighted_avg_and_std[0]['telecommuting'][0], 3)
    weighted_std = round(weighted_avg_and_std[0]['telecommuting'][1], 3)
    nb_obs = weighted_avg_and_std[1]
    print('Proportion of people telecommuting among workers (MTMC):',
          str(weighted_avg * 100) + '% (+/-', str(weighted_std * 100) + ', n=' + str(nb_obs) + ')')
