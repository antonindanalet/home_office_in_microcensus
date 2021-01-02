from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std


def descriptive_statistics():
    descriptive_statistics_microcensus()
    descriptive_statistics_synpop()
    descriptive_statistics_comparison()


def descriptive_statistics_comparison():
    # Read SynPop data
    output_directory = Path('../data/output/data/validation_with_SynPop/')
    data_file_name = 'persons_from_SynPop2017.csv'
    df_persons_from_synpop = pd.read_csv(output_directory / data_file_name, sep=';')
    df_persons_from_synpop.drop(df_persons_from_synpop[df_persons_from_synpop.age <= 5].index, inplace=True)
    # Read MTMC data (only employees)
    directory_home_office = Path('../data/output/data/estimation/')
    data_file_name_home_office = 'persons.csv'
    df_persons_home_office = pd.read_csv(directory_home_office / data_file_name_home_office, sep=';')

    descriptive_statistics_income(df_persons_home_office, df_persons_from_synpop)


def descriptive_statistics_synpop():
    # Read data
    output_directory = Path('../data/output/data/validation_with_SynPop/')
    data_file_name = 'persons_from_SynPop2017.csv'
    df_persons_from_synpop = pd.read_csv(output_directory / data_file_name, sep=';')
    df_persons_from_synpop.drop(df_persons_from_synpop[df_persons_from_synpop.age <= 5].index, inplace=True)
    descriptive_statistics_synpop_business_sector(df_persons_from_synpop)
    descriptive_statistics_synpop_employed(df_persons_from_synpop)
    descriptive_statistics_synpop_work_position(df_persons_from_synpop)
    descriptive_statistics_synpop_income(df_persons_from_synpop)
    descriptive_statistics_synpop_home_work_distance(df_persons_from_synpop)
    descriptive_statistics_synpop_nationality(df_persons_from_synpop)


def descriptive_statistics_microcensus():
    ''' Statistics among the whole population/sample '''
    directory_full_sample = Path('../data/input/mtmc/2015/')
    data_file_name_full_sample = 'zielpersonen.csv'
    df_persons_full_sample = pd.read_csv(directory_full_sample / data_file_name_full_sample, encoding='latin1')
    descriptive_statistics_microcensus_employed(df_persons_full_sample)
    descriptive_statistics_microcensus_reasons_for_teleworking(df_persons_full_sample)
    ''' Statistics among people with a job and people who answered the question about home office '''
    directory_home_office = Path('../data/output/data/estimation/')
    data_file_name_home_office = 'persons.csv'
    df_persons_home_office = pd.read_csv(directory_home_office / data_file_name_home_office, sep=';')
    descriptive_statistics_microcensus_working_from_home_percentage(df_persons_home_office)
    descriptive_statistics_microcensus_business_sector(df_persons_home_office)
    descriptive_statistics_microcensus_work_position(df_persons_home_office)
    descriptive_statistics_income(df_persons_home_office)
    descriptive_statistics_home_work_distance(df_persons_home_office)
    descriptive_statistics_microcensus_nationality(df_persons_home_office)


def descriptive_statistics_microcensus_reasons_for_teleworking(df_persons_full_sample):
    df_persons_home_office_possible = \
        df_persons_full_sample[df_persons_full_sample['f81300'].isin([1, 2])]
    df_persons_home_office_more_than_nothing = \
        df_persons_home_office_possible[df_persons_home_office_possible['f81400'] > 0]
    df_persons_home_office_with_a_reason = \
        df_persons_home_office_more_than_nothing[df_persons_home_office_more_than_nothing['f81450'] > 0].copy()
    nb_observations = len(df_persons_home_office_with_a_reason)
    df_persons_home_office_with_a_reason['travel_time'] = df_persons_home_office_with_a_reason.f81450 == 1
    df_persons_home_office_with_a_reason['workplace_is_home'] = df_persons_home_office_with_a_reason.f81450 == 2
    df_persons_home_office_with_a_reason['congestion'] = df_persons_home_office_with_a_reason.f81450.isin([3, 4])
    df_persons_home_office_with_a_reason['family_reasons'] = df_persons_home_office_with_a_reason.f81450 == 5
    df_persons_home_office_with_a_reason['work_atmosphere'] = df_persons_home_office_with_a_reason.f81450 == 6
    df_persons_home_office_with_a_reason['quiet'] = df_persons_home_office_with_a_reason.f81450 == 7
    df_persons_home_office_with_a_reason['business_meeting_outside_of_work'] = \
        df_persons_home_office_with_a_reason.f81450 == 8
    df_persons_home_office_with_a_reason['other'] = df_persons_home_office_with_a_reason.f81450 == 9
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons_home_office_with_a_reason, weights='WP',
                                                    list_of_columns=['travel_time',
                                                                     'workplace_is_home',
                                                                     'congestion',
                                                                     'family_reasons',
                                                                     'work_atmosphere',
                                                                     'quiet',
                                                                     'business_meeting_outside_of_work',
                                                                     'other'])
    weighted_avg_travel_time = weighted_avg_and_std[0]['travel_time'][0]
    weighted_avg_workplace_is_home = weighted_avg_and_std[0]['workplace_is_home'][0]
    weighted_avg_congestion = weighted_avg_and_std[0]['congestion'][0]
    weighted_avg_family_reasons = weighted_avg_and_std[0]['family_reasons'][0]
    weighted_avg_work_atmosphere = weighted_avg_and_std[0]['work_atmosphere'][0]
    weighted_avg_quiet = weighted_avg_and_std[0]['quiet'][0]
    weighted_avg_business_meeting_outside_of_work = weighted_avg_and_std[0]['business_meeting_outside_of_work'][0]
    weighted_avg_other = weighted_avg_and_std[0]['other'][0]
    fig, ax = plt.subplots()
    list_percentages = [weighted_avg_travel_time, weighted_avg_workplace_is_home, weighted_avg_congestion,
                        weighted_avg_family_reasons, weighted_avg_work_atmosphere, weighted_avg_quiet,
                        weighted_avg_business_meeting_outside_of_work, weighted_avg_other]
    wedges, texts, autotexts = ax.pie(list_percentages,
                                      colors=[(133/256, 205/256, 230/256),
                                              (2/256, 153/256, 198/256),
                                              (1/256, 104/256, 134/256),
                                              (160/256,  63/256,     0),
                                              (234/256,  89/256,     0),
                                              (247/256, 165/256,     0),
                                              (255/256, 226/256, 180/256),
                                              (207/256, 208/256, 208/256)],
                                      counterclock=False, startangle=90,
                                      autopct=lambda pct: "{:.0f}%".format(pct))
    for index, autotext in enumerate(autotexts):
        if index in [1, 2, 3, 4, 9]:
            autotext.set_color('white')
        else:
            autotext.set_color('black')
    labels = ['Home-work travel time/distance',
              'Work place at home',
              'Road/public transport congestion',
              'Family reasons',
              'Work atmosphere',
              'Concentration / quiet',
              'Business meeting not in office',
              'Other']
    ax.legend(wedges, labels,
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title('Reasons to work from home in 2015')
    plt.text(x=-1.15, y=-1.38, s='Basis: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                                 ' persons working from home at least 1% of the time and who gave a reason why.\n\n'
                                 'Source: FSO, ARE - Mobility and Transport Microcensus (MTMC)', fontsize=8)
    plt.subplots_adjust(left=0.0, bottom=0.1, right=0.5)
    file_name = 'reasons_teleworking.png'
    path = Path('../data/output/figures/')
    fig.savefig(path / file_name)


def descriptive_statistics_microcensus_working_from_home_percentage(df_persons_home_office):
    df_persons_home_office_possible = \
        df_persons_home_office[df_persons_home_office['home_office_is_possible'].isin([1, 2])]
    df_persons_home_office_more_than_nothing = \
        df_persons_home_office_possible[df_persons_home_office_possible['percentage_home_office'] > 0].copy()
    nb_observations = len(df_persons_home_office_more_than_nothing)
    ''' Histogram '''
    df_persons_home_office_more_than_nothing['percentage_home_office_1_10'] = \
        (1 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 10)
    df_persons_home_office_more_than_nothing['percentage_home_office_11_20'] = \
        (11 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 20)
    df_persons_home_office_more_than_nothing['percentage_home_office_21_30'] = \
        (21 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 30)
    df_persons_home_office_more_than_nothing['percentage_home_office_31_40'] = \
        (31 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 40)
    df_persons_home_office_more_than_nothing['percentage_home_office_41_50'] = \
        (41 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 50)
    df_persons_home_office_more_than_nothing['percentage_home_office_51_60'] = \
        (51 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 60)
    df_persons_home_office_more_than_nothing['percentage_home_office_61_70'] = \
        (61 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 70)
    df_persons_home_office_more_than_nothing['percentage_home_office_71_80'] = \
        (71 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 80)
    df_persons_home_office_more_than_nothing['percentage_home_office_81_90'] = \
        (81 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 90)
    df_persons_home_office_more_than_nothing['percentage_home_office_91_100'] = \
        (91 <= df_persons_home_office_more_than_nothing.percentage_home_office) & \
        (df_persons_home_office_more_than_nothing.percentage_home_office <= 100)
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons_home_office_more_than_nothing, weights='WP',
                                                    list_of_columns=['percentage_home_office_1_10',
                                                                     'percentage_home_office_11_20',
                                                                     'percentage_home_office_21_30',
                                                                     'percentage_home_office_31_40',
                                                                     'percentage_home_office_41_50',
                                                                     'percentage_home_office_51_60',
                                                                     'percentage_home_office_61_70',
                                                                     'percentage_home_office_71_80',
                                                                     'percentage_home_office_81_90',
                                                                     'percentage_home_office_91_100'])
    weighted_avg_1_10 = weighted_avg_and_std[0]['percentage_home_office_1_10'][0]
    weighted_avg_11_20 = weighted_avg_and_std[0]['percentage_home_office_11_20'][0]
    weighted_avg_21_30 = weighted_avg_and_std[0]['percentage_home_office_21_30'][0]
    weighted_avg_31_40 = weighted_avg_and_std[0]['percentage_home_office_31_40'][0]
    weighted_avg_41_50 = weighted_avg_and_std[0]['percentage_home_office_41_50'][0]
    weighted_avg_51_60 = weighted_avg_and_std[0]['percentage_home_office_51_60'][0]
    weighted_avg_61_70 = weighted_avg_and_std[0]['percentage_home_office_61_70'][0]
    weighted_avg_71_80 = weighted_avg_and_std[0]['percentage_home_office_71_80'][0]
    weighted_avg_81_90 = weighted_avg_and_std[0]['percentage_home_office_81_90'][0]
    weighted_avg_91_100 = weighted_avg_and_std[0]['percentage_home_office_91_100'][0]
    fig, ax = plt.subplots()

    x = ['1-10%', '11-20%', '21-30%', '31-40%', '41-50%', '51-60%', '61-70%', '71-80%', '81-90%', '91-100%']
    y = [weighted_avg_1_10, weighted_avg_11_20, weighted_avg_21_30, weighted_avg_31_40, weighted_avg_41_50,
         weighted_avg_51_60, weighted_avg_61_70, weighted_avg_71_80, weighted_avg_81_90, weighted_avg_91_100]
    rects = ax.bar(x, y, color=(2/256, 153/256, 198/256))
    for rect in rects:
        height = rect.get_height()
        if height > 0.05:  # Show value (in white) in the bar if the value is higher than 5%
            ax.text(rect.get_x() + rect.get_width() / 2., height - 0.04,
                    '%d' % int(height * 100) + '%',
                    ha='center', va='bottom', color='white')
        else:  # If the value is small, show the value on top of the bar (in black)
            ax.text(rect.get_x() + rect.get_width() / 2., height + 0.01,
                    '%d' % int(height * 100) + '%',
                    ha='center', va='bottom', color='black')
    ax.set_title('Percentage of work done from home in 2015')
    plt.xticks(rotation=45)
    plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5], ['0%', '10%', '20%', '30%', '40%', '50%'])
    ax.set_facecolor((240/256, 240/256, 240/256))
    ax.set_axisbelow(True)
    plt.grid(b=True, which='major', color='gray', linestyle='-', axis='y')
    plt.ylim([0, 0.5])
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.text(x=-1.73, y=-0.18, s='Basis: ' + str("{0:,g}".format(nb_observations)).replace(",", " ") +
                                 ' persons working from home at least 1% of the time.\n\n'
                                 'Source: FSO, ARE - Mobility and Transport Microcensus (MTMC)', fontsize=8)
    file_name = 'teleworking_percentage_distribution.png'
    path = Path('../data/output/figures/')
    fig.savefig(path / file_name)


def descriptive_statistics_synpop_income(df_persons_from_synpop):
    df_persons_from_synpop_employed = \
        df_persons_from_synpop[df_persons_from_synpop.position_in_bus.isin([1, 11, 12, 20])].copy()
    df_persons_from_synpop_employed['hh_income_6509_or_less'] = df_persons_from_synpop_employed.hh_income < 6508.6
    print('Proportion of employees with household income < 8000 CHF (MTMC):',
          df_persons_from_synpop_employed['hh_income_6509_or_less'].mean())


def descriptive_statistics_income(df_persons_home_office, df_persons_from_synpop):
    ''' Proportion MTMC '''
    df_persons_home_office['less_than_8000'] = df_persons_home_office.hh_income.isin([1, 2, 3, 4])
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons_home_office, weights='WP',
                                                    list_of_columns=['less_than_8000'])
    weighted_avg_less_than_8000 = weighted_avg_and_std[0]['less_than_8000'][0]
    print('Proportion of employees with household income < 8000 CHF (MTMC):', weighted_avg_less_than_8000)
    ''' Histogram '''
    df_persons_home_office['hh_income_less_than_2000'] = df_persons_home_office.hh_income == 1
    df_persons_home_office['hh_income_2000_to_4000'] = df_persons_home_office.hh_income == 2
    df_persons_home_office['hh_income_4001_to_6000'] = df_persons_home_office.hh_income == 3
    df_persons_home_office['hh_income_6001_to_8000'] = df_persons_home_office.hh_income == 4
    df_persons_home_office['hh_income_8001_to_10000'] = df_persons_home_office.hh_income == 5
    df_persons_home_office['hh_income_10001_to_12000'] = df_persons_home_office.hh_income == 6
    df_persons_home_office['hh_income_12001_to_14000'] = df_persons_home_office.hh_income == 7
    df_persons_home_office['hh_income_14001_to_16000'] = df_persons_home_office.hh_income == 8
    df_persons_home_office['hh_income_more_than_16000'] = df_persons_home_office.hh_income == 9
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons_home_office, weights='WP',
                                                    list_of_columns=['hh_income_less_than_2000',
                                                                     'hh_income_2000_to_4000',
                                                                     'hh_income_4001_to_6000',
                                                                     'hh_income_6001_to_8000',
                                                                     'hh_income_8001_to_10000',
                                                                     'hh_income_10001_to_12000',
                                                                     'hh_income_12001_to_14000',
                                                                     'hh_income_14001_to_16000',
                                                                     'hh_income_more_than_16000'])
    weighted_avg_less_than_2000 = weighted_avg_and_std[0]['hh_income_less_than_2000'][0]
    weighted_avg_2000_to_4000 = weighted_avg_and_std[0]['hh_income_2000_to_4000'][0]
    weighted_avg_4001_to_6000 = weighted_avg_and_std[0]['hh_income_4001_to_6000'][0]
    weighted_avg_6001_to_8000 = weighted_avg_and_std[0]['hh_income_6001_to_8000'][0]
    weighted_avg_8001_to_10000 = weighted_avg_and_std[0]['hh_income_8001_to_10000'][0]
    weighted_avg_10001_to_12000 = weighted_avg_and_std[0]['hh_income_10001_to_12000'][0]
    weighted_avg_12001_to_14000 = weighted_avg_and_std[0]['hh_income_12001_to_14000'][0]
    weighted_avg_14001_to_16000 = weighted_avg_and_std[0]['hh_income_14001_to_16000'][0]
    weighted_avg_more_than_16000 = weighted_avg_and_std[0]['hh_income_more_than_16000'][0]
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    x = ['less than 2000', '2000 to 4000', '4001 to 6000', '6001 to 8000', "8001 to 10'000", "10'0001 to 12'000",
         "12'001 to 14'000", "14'001 to 16'000", "more than 16'000"]
    y = [weighted_avg_less_than_2000, weighted_avg_2000_to_4000, weighted_avg_4001_to_6000, weighted_avg_6001_to_8000,
         weighted_avg_8001_to_10000, weighted_avg_10001_to_12000, weighted_avg_12001_to_14000,
         weighted_avg_14001_to_16000, weighted_avg_more_than_16000]
    ax[0].bar(x, y)

    # Proportion SynPop
    synpop_less_than_2000 = (df_persons_from_synpop.hh_income_category == 1).mean()
    synpop_2000_to_4000 = (df_persons_from_synpop.hh_income_category == 2).mean()
    synpop_4001_to_6000 = (df_persons_from_synpop.hh_income_category == 3).mean()
    synpop_6001_to_8000 = (df_persons_from_synpop.hh_income_category == 4).mean()
    synpop_8001_to_10000 = (df_persons_from_synpop.hh_income_category == 5).mean()
    synpop_10001_to_12000 = (df_persons_from_synpop.hh_income_category == 6).mean()
    synpop_12001_to_14000 = (df_persons_from_synpop.hh_income_category == 7).mean()
    synpop_14001_to_16000 = (df_persons_from_synpop.hh_income_category == 8).mean()
    synpop_more_than_16000 = (df_persons_from_synpop.hh_income_category == 9).mean()

    y_synpop = [synpop_less_than_2000, synpop_2000_to_4000, synpop_4001_to_6000, synpop_6001_to_8000,
                synpop_8001_to_10000, synpop_10001_to_12000, synpop_12001_to_14000, synpop_14001_to_16000,
                synpop_more_than_16000]

    ax[1].bar(x, y_synpop)#, width=(bins[1] - bins[0]), color='grey')

    ax[0].set_title('Income distribution in MTMC')
    ax[1].set_title('Income distribution in SynPop')
    file_name = 'income_distribution.png'
    path = Path('../data/output/figures/')
    fig.savefig(path / file_name)


def descriptive_statistics_synpop_nationality(df_persons):
    df_persons_employed = df_persons[df_persons.position_in_bus.isin([1, 11, 12, 20])].copy()
    df_persons_employed['ch_germany_france_italy_nw_e'] = df_persons.nation.isin([0,  # Switzerland
                                                                                  1,  # Germany, Austria, Lichtenstein
                                                                                  2,  # Italy, Vatican
                                                                                  3,  # France, Monaco, San Marino
                                                                                  4])  # Northwestern Europe
    print('Proportion of people with Swiss, French, Italian, etc. nationality (SynPop)',
          df_persons_employed['ch_germany_france_italy_nw_e'].mean())


def descriptive_statistics_microcensus_nationality(df_persons):
    df_persons['ch_germany_france_italy_nw_e'] = df_persons.nation.isin([8100,  # Switzerland
                                                                         8207,  # Germany
                                                                         8229,  # Austria
                                                                         8222,  # Lichtenstein
                                                                         8218,  # Italy
                                                                         8241,  # Vatican
                                                                         8212,  # France
                                                                         8226,  # Monaco
                                                                         8233,  # San Marino
                                                                         8204,  # Belgium
                                                                         8223,  # Luxembourg
                                                                         8227,  # Netherlands
                                                                         8206,  # Denmark
                                                                         8211,  # Finland
                                                                         8215,  # United Kingdom
                                                                         8216,  # Ireland
                                                                         8217,  # Iceland
                                                                         8228,  # Norway
                                                                         8234])  # Sweden
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons,
                                                    weights='WP', list_of_columns=['ch_germany_france_italy_nw_e'])
    weighted_avg_employed = weighted_avg_and_std[0]['ch_germany_france_italy_nw_e'][0]
    print('Proportion of people with Swiss, French, Italian, etc. nationality (MTMC):', weighted_avg_employed)


def descriptive_statistics_synpop_employed(df_persons_from_synpop):
    df_persons_from_synpop['employed'] = df_persons_from_synpop.position_in_bus.isin([1, 11, 12, 20])
    print('Proportion of people employed in the population (SynPop):', df_persons_from_synpop.employed.mean())


def descriptive_statistics_microcensus_employed(df_persons):
    df_persons['employed'] = df_persons['f40800_01'].isin([1, 2, 3, 4])
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP', list_of_columns=['employed'])
    weighted_avg_employed = weighted_avg_and_std[0]['employed'][0]
    print('Proportion of people employed in the population (MTMC):', weighted_avg_employed)


def descriptive_statistics_synpop_home_work_distance(df_persons_from_synpop):
    # Remove people unemployed (0) and apprentices (3)
    df_persons_from_synpop.drop(df_persons_from_synpop[df_persons_from_synpop.position_in_bus.isin([-99, 0, 3])].index,
                                inplace=True)
    df_persons_from_synpop['home_work_distance'] = df_persons_from_synpop['home_work_crow_fly_distance'] * \
                                                   (df_persons_from_synpop['home_work_crow_fly_distance'] >= 0.0) / \
                                                   100000.0
    print('Average distance home to work (SynPop):', df_persons_from_synpop.home_work_distance.mean())


def descriptive_statistics_home_work_distance(df_persons):
    df_persons['home_work_distance'] = df_persons['home_work_crow_fly_distance'] * \
                                       (df_persons['home_work_crow_fly_distance'] >= 0.0) / 100000.0
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP', list_of_columns=['home_work_distance'])
    weighted_avg_home_work_distance = weighted_avg_and_std[0]['home_work_distance'][0]
    print('Average distance home to work (MTMC):', weighted_avg_home_work_distance)


def descriptive_statistics_microcensus_work_position(df_persons):
    """ NPVM                        Code NPVM
            qualifizierter Mitarbeiter 1
            einfacher Mitarbeiter      2 """
    df_persons['cadres'] = df_persons.work_position == 1
    df_persons['employees'] = df_persons.work_position == 2
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP',
                                                    list_of_columns=['cadres', 'employees'])
    weighted_avg_cadres = weighted_avg_and_std[0]['cadres'][0]
    weighted_avg_employees = weighted_avg_and_std[0]['employees'][0]
    print('Proportion of observations cadres (MTMC):', weighted_avg_cadres)
    print('Proportion of observations employees (MTMC):', weighted_avg_employees)


def descriptive_statistics_synpop_work_position(df_persons):
    print(df_persons.position_in_bus.unique())
    df_persons_from_synpop_employed = df_persons[df_persons.position_in_bus.isin([1, 11, 12, 20])].copy()
    df_persons_from_synpop_employed['cadres'] = df_persons_from_synpop_employed.position_in_bus.isin([1, 11, 12])
    df_persons_from_synpop_employed['employees'] = df_persons_from_synpop_employed. position_in_bus == 20
    print('Proportion of observations cadres (SynPop):', df_persons_from_synpop_employed.cadres.mean())
    print('Proportion of observations employees (SynPop):', df_persons_from_synpop_employed.employees.mean())


def descriptive_statistics_synpop_business_sector(df_persons_from_synpop):
    df_persons_from_synpop['business_sector_agriculture'] = df_persons_from_synpop['type_1'] == 1
    df_persons_from_synpop['business_sector_gastronomy'] = df_persons_from_synpop['type_1'] == 5
    df_persons_from_synpop['business_sector_production'] = df_persons_from_synpop['type_1'] == 2
    df_persons_from_synpop['business_sector_retail'] = df_persons_from_synpop['type_1'] == 4
    df_persons_from_synpop['business_sector_non_movers'] = df_persons_from_synpop['type_1'] == 10
    df_persons_from_synpop['business_sector_service_fC'] = df_persons_from_synpop['type_1'] == 7
    print('Proportion of employees in agriculture in the SynPop:',
          df_persons_from_synpop['business_sector_agriculture'].mean())
    print('Proportion of employees in gastronomy in the SynPop:',
          df_persons_from_synpop['business_sector_gastronomy'].mean())
    print('Proportion of employees in production in the SynPop:',
          df_persons_from_synpop['business_sector_production'].mean())
    print('Proportion of employees in retail in the SynPop:',
          df_persons_from_synpop['business_sector_retail'].mean())
    print('Proportion of employees in "non-movers" category in the SynPop:',
          df_persons_from_synpop['business_sector_non_movers'].mean())
    print('Proportion of employees in "service fC" category in the SynPop:',
          df_persons_from_synpop['business_sector_service_fC'].mean())


def descriptive_statistics_microcensus_business_sector(df_persons):
    df_persons['business_sector_agriculture'] = (1 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 7)
    # There is no noga 08 equal to 57 in the MTMC, even if 57 is mentioned in the report on the synthetic population
    df_persons['business_sector_gastronomy'] = (55 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 56)
    # There is no noga 08 equal to 44 in the MTMC, even if 44 is mentioned in the report on the synthetic population
    df_persons['business_sector_production'] = ((10 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 35)) | \
                                               ((40 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 43))
    # There is no noga 08 equal to 48 in the MTMC, even if 48 is mentioned in the report on the synthetic population
    df_persons['business_sector_retail'] = df_persons['noga_08'] == 47
    # In the report on the synthetic population, there is once a definition of non movers without 36-39 and once with
    # 36-39. We decided to use the definition with 36-39 (29 observations in the MTMC).
    df_persons['business_sector_non_movers'] = ((8 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 9)) | \
                                               ((84 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 85)) | \
                                               ((36 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 39)) | \
                                               (df_persons['noga_08'] == 91) | \
                                               (df_persons['noga_08'] == 99)
    # There is no noga 08 equal to 83 in the MTMC, even if 83 is mentioned in the report on the synthetic population
    df_persons['business_sector_service_fC'] = ((60 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 63)) | \
                                               ((69 <= df_persons['noga_08']) & (df_persons['noga_08'] <= 82)) | \
                                               (df_persons['noga_08'] == 58)
    weighted_avg_and_std = get_weighted_avg_and_std(df_persons, weights='WP',
                                                    list_of_columns=['business_sector_agriculture',
                                                                     'business_sector_gastronomy',
                                                                     'business_sector_production',
                                                                     'business_sector_retail',
                                                                     'business_sector_non_movers',
                                                                     'business_sector_service_fC'])
    weighted_avg_agriculture = weighted_avg_and_std[0]['business_sector_agriculture'][0]
    weighted_avg_gastronomy = weighted_avg_and_std[0]['business_sector_gastronomy'][0]
    weighted_avg_production = weighted_avg_and_std[0]['business_sector_production'][0]
    weighted_avg_retail = weighted_avg_and_std[0]['business_sector_retail'][0]
    weighted_avg_non_movers = weighted_avg_and_std[0]['business_sector_non_movers'][0]
    weighted_avg_service_fc = weighted_avg_and_std[0]['business_sector_service_fC'][0]
    print('Proportion of observations of employees in agriculture:', weighted_avg_agriculture)
    print('Proportion of observations of employees in gastronomy:', weighted_avg_gastronomy)
    print('Proportion of observations of employees in production:', weighted_avg_production)
    print('Proportion of observations of employees in retail:', weighted_avg_retail)
    print('Proportion of observations of employees in non-movers:', weighted_avg_non_movers)
    print('Proportion of observations of employees in service fC:', weighted_avg_service_fc)
