from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from utils_synpop.generate_data_file_for_simulation import generate_data_file_for_simulation
from utils_synpop.compute_household_income_limit import compute_household_income_limit
from utils_synpop.apply_model_to_synthetic_population import apply_model_to_synthetic_population
from utils_mtmc.get_percentage_telecommuting import get_percentage_telecommuting


def apply_model_to_syn_pop_2050(betas):
    dict_results = compute_forecasts(betas)
    # Add zeros for years multiple of 5 that are not observed nor forecasted, so that the x-axis is reasonable
    dict_results[2020] = 0
    dict_results[2025] = 0
    dict_results[2035] = 0
    dict_results[2045] = 0
    for year in [2010, 2015]:
        dict_results[year] = get_percentage_telecommuting(year)
    generate_figure_results(dict_results)


def generate_figure_results(dict_results):
    # Sort the dict by year/key
    dict_results = dict(sorted(dict_results.items()))

    fig, ax = plt.subplots()

    # Create bars
    ax.grid(axis='y', zorder=0)
    ax.bar(range(len(dict_results)), dict_results.values(), color=(22/255, 141/255, 180/255, 1), zorder=3)

    # Create names on the x-axis (use empty label when there is no value - in the dict: 0)
    plt.xticks(range(len(dict_results)), [2010, 2015, "", "", 2030, "", 2040, "", 2050])

    plt.yticks([0.1, 0.2, 0.3, 0.4], ['10%', '20%', '30%', '40%'])

    plt.title('Percentage of employees working from home, 2010-2050')

    # Add the values in the bars
    rects = ax.patches
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.1f}'.format(height * 100),
                    xy=(rect.get_x() + rect.get_width() / 2, height - 0.03),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', color='white')

    # Show graphic
    path_for_figure = Path('../data/output/figures/teleworking_per_year.png')
    fig.savefig(path_for_figure, dpi=600)


def compute_forecasts(betas):
    dict_results = {}
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
        dict_results[year] = predicted_rate_of_telecommuting
    return dict_results
