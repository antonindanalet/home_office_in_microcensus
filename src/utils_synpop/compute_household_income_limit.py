from pathlib import Path
import pandas as pd


def compute_household_income_limit(year):
    # Proportion of employees with household income < 8000 CHF (MTMC):
    percent_employees_with_income_less_8000 = 0.38921317978801245
    # Read SynPop data
    if year == 2017:
        output_directory = Path('../data/output/data/validation_with_SynPop/')
        data_file_name = 'persons_from_SynPop2017.csv'
    elif year == 2030:
        output_directory = Path('../data/output/data/application_to_SynPop_2030')
        data_file_name = 'persons_from_SynPop2030.csv'
    elif year == 2040:
        output_directory = Path('../data/output/data/application_to_SynPop_2040')
        data_file_name = 'persons_from_SynPop2040.csv'
    elif year == 2050:
        output_directory = Path('../data/output/data/application_to_SynPop_2050')
        data_file_name = 'persons_from_SynPop2050.csv'
    else:
        raise Exception()
    df_persons_from_synpop = pd.read_csv(output_directory / data_file_name, sep=';')
    # Remove children
    df_persons_from_synpop.drop(df_persons_from_synpop[df_persons_from_synpop.age <= 5].index, inplace=True)
    # Remove people unemployed (0) and apprentices (3)
    df_persons_from_synpop.drop(df_persons_from_synpop[df_persons_from_synpop.position_in_bus.isin([-99, 0, 3])].index,
                                inplace=True)
    number_of_employees = len(df_persons_from_synpop)
    number_of_employees_with_income_less_than_8000 = int(number_of_employees * percent_employees_with_income_less_8000)
    df_persons_from_synpop_sorted = df_persons_from_synpop.sort_values(by='hh_income').reset_index()
    household_income_limit = df_persons_from_synpop_sorted.loc[number_of_employees_with_income_less_than_8000,
                                                               'hh_income']
    return household_income_limit
