import pandas as pd
from pathlib import Path
import geopandas
import numpy as np
from utils_mtmc.get_mtmc_files import get_zp, get_hh
from utils_mtmc.define_telecommuting_variable import define_telecommuting_variable


def generate_data_file(year):
    """ This function reads the  data about the person.
    It then joins them with the data about the household and the spatial typology.
    It returns nothing, but saves the output as a data file for Biogeme.
        :param: Year of the Mobility and Transport Microcensus. Possible values: 2015 or 2020.
        :return: Nothing. The dataframe is saved as a CSV file (separator: tab) without NA values, in Biogeme format.
        """
    ''' Select the variables about the person from the tables of the MTMC '''
    if year == 2015:
        selected_columns_zp = ['gesl', 'HAUSB', 'HHNR', 'f81300', 'A_X', 'A_Y', 'alter', 'f81400', 'noga_08',
                               'sprache', 'f40800_01', 'f41100_01', 'nation', 'f40900', 'f40901_02', 'f40903', 'WP',
                               'A_BFS', 'f42100e', 'f41610a', 'f41610b', 'f41610c']
    elif year == 2020:
        selected_columns_zp = ['gesl', 'f40120', 'HHNR', 'f81300', 'A_X', 'A_Y', 'alter', 'f81400', 'noga_08',
                               'sprache', 'f40800_01', 'f41100_01', 'nation', 'f40920', 'WP',
                               'A_BFS', 'f42100e', 'f41600_01a', 'f41600_01b', 'f41600_01c']
    else:
        raise Exception('The year of the Mobility and Transport Microcensus must be 2015 or 2020.')
    df_zp = get_zp(year, selected_columns_zp)
    if year == 2015:
        selected_columns_hh = ['HHNR', 'hhtyp', 'W_OeV_KLASSE', 'W_BFS', 'W_X', 'W_Y', 'F20601']
    elif year == 2020:
        selected_columns_hh = ['HHNR', 'hhtyp', 'W_OeV_KLASSE', 'W_BFS', 'W_X', 'W_Y', 'f20601']
    df_hh = get_hh(year, selected_columns_hh)
    df_zp = pd.merge(df_zp, df_hh, on='HHNR', how='left')

    ''' Add public transport connection quality of the work place '''
    df_zp_with_work_coord = df_zp[df_zp.A_X != -999]
    df_zp_with_work_coord = geopandas.GeoDataFrame(df_zp_with_work_coord,
                                                   geometry=geopandas.points_from_xy(df_zp_with_work_coord.A_X,
                                                                                     df_zp_with_work_coord.A_Y),
                                                   crs='epsg:4326')
    df_zp_with_work_coord.to_crs(epsg=21781, inplace=True)
    # Read the shape file containing the connection quality
    connection_quality_folder_path = Path('../data/input/OeV_Gueteklassen/Fahrplanperiode_17_18/')
    df_connection_quality = geopandas.read_file(connection_quality_folder_path / 'OeV_Gueteklassen_ARE.shp')
    df_connection_quality.set_crs(epsg=21781, inplace=True)  # Define the projection (CH1903_LV03)
    df_zp_with_work_coord = geopandas.sjoin(df_zp_with_work_coord, df_connection_quality[['KLASSE', 'geometry']],
                                            how='left', op='intersects')
    df_zp_with_work_coord['KLASSE'] = df_zp_with_work_coord['KLASSE'].map({'A': 1,
                                                                           'B': 2,
                                                                           'C': 3,
                                                                           'D': 4})
    df_zp_with_work_coord['KLASSE'].fillna('5', inplace=True)
    df_zp.loc[df_zp.A_X != -999, 'KLASSE'] = df_zp_with_work_coord['KLASSE']
    df_zp['KLASSE'].fillna(-999, inplace=True)
    # Rename the column with the public transport connection quality
    df_zp.rename(columns={'KLASSE': 'public_transport_connection_quality_ARE_work'}, inplace=True)

    df_zp = add_home_work_distance(df_zp)

    df_zp = add_spatial_typology(df_zp, year)

    ''' Generate the variable about work position:
    Code FaLC in English     FaLC in German   NPVM                       Code used below
     0   Unemployed                                                      0
     1   CEO                 Geschäftsführer  qualifizierter Mitarbeiter 1
     11  business management Geschäftsleitung qualifizierter Mitarbeiter 1
     12  management          qualifizierte MA qualifizierter Mitarbeiter 1
     20  Employee            einfache MA      einfacher Mitarbeiter      2
     3   Apprentice          Lehrling                                    3 
     "NPVM" stands for "nationale Personenverkehrsmodell", the Swiss national passenger transport model.
     "MTMC", below, stands for Mobility and Transport Microcensus, the Swiss travel survey.
     In the code below, -99 corresponds to no answer/doesn't know to the question about work position 
     (if working) '''
    df_zp.loc[df_zp['f40800_01'].isin([1,  # MTMC: "Selbstständig Erwerbende(r)"
                                       2,  # MTMC: Arbeitnehmer in AG/GmbH, welche IHNEN selbst gehört
                                       3]),  # MTMC: Arbeitnehmer im Familienbetrieb von Haushaltsmitglied
              'work_position'] = 1  # NPVM: Qualifiziert
    df_zp.loc[(df_zp['f40800_01'] == 4) &  # MTMC: Arbeitnehmer bei einem sonstigen Unternehmen
              (df_zp['f41100_01'] == 1),  # MTMC: Angestellt ohne Cheffunktion
              'work_position'] = 2  # NPVM: Einfach
    df_zp.loc[(df_zp['f40800_01'] == 4) &  # MTMC: Arbeitnehmer bei einem sonstigen Unternehmen
              (df_zp['f41100_01'].isin([2,  # MTMC: Angestellt mit Chefposition
                                        3])),  # MTMC: Angestellt als Mitglied von der Direktion
              'work_position'] = 1  # SynPop: Qualifiziert
    df_zp.loc[df_zp['f40800_01'] == 5,  # MTMC: Lehrling
              'work_position'] = 3  # NPVM: Apprentice
    df_zp.loc[df_zp['f41100_01'] == 3,  # MTMC: Angestellt als Mitglied von der Direktion
              'work_position'] = 1  # NPVM: Qualifiziert
    df_zp.loc[df_zp['f40800_01'] == -99,  # MTMC: Nicht erwerbstätig
              'work_position'] = 0  # NPVM: Unemployed
    df_zp.loc[(df_zp['f40800_01'] == 4) & (df_zp['f41100_01'].isin([-98, -97])),
              'work_position'] = -99
    del df_zp['f40800_01']
    del df_zp['f41100_01']

    # Rename the variables
    if year == 2015:
        highest_education_variable_name = 'HAUSB'
    elif year == 2020:
        highest_education_variable_name = 'f40120'
    df_zp = df_zp.rename(columns={'gesl': 'sex',
                                  highest_education_variable_name: 'highest_educ',
                                  'f81300': 'telecommuting_is_possible',
                                  'hhtyp': 'hh_type',
                                  'W_OeV_KLASSE': 'public_transport_connection_quality_ARE_home',
                                  'alter': 'age',
                                  'f81400': 'percentage_telecommuting',
                                  'sprache': 'language',
                                  'f40900': 'full_part_time_job',
                                  'f40901_02': 'percentage_first_part_time_job',  # only in 2015
                                  'f40903': 'percentage_second_part_time_job',  # only in 2015
                                  'f40920': 'percentage_part_time_job',  # only in 2020
                                  'F20601': 'hh_income',  # naming 2015
                                  'f20601': 'hh_income',  # naming 2020
                                  'f42100e': 'car_avail',
                                  'f41610a': 'GA_ticket',  # 2015
                                  'f41610b': 'halbtax_ticket',  # 2015
                                  'f41610c': 'Verbund_Abo',  # 2015
                                  'f41600_01a': 'GA_ticket',  # 2020
                                  'f41600_01b': 'halbtax_ticket',  # 2020
                                  'f41600_01c': 'Verbund_Abo'})  # 2020
    df_zp['mobility_resources'] = df_zp.apply(define_mobility_resources_variable, axis=1)

    ''' Removing people who did not get the question or did not answer. '''
    df_zp.drop(df_zp[df_zp.telecommuting_is_possible < 0].index, inplace=True)
    df_zp.drop(df_zp[df_zp.percentage_telecommuting == -98].index, inplace=True)
    df_zp.drop(df_zp[df_zp.percentage_telecommuting == -97].index, inplace=True)
    ''' Define the variable home office as "possibility to do home office" and "practically do some" '''
    df_zp['telecommuting'] = df_zp.apply(define_telecommuting_variable, axis=1)
    ''' Define the business sectors '''
    df_zp['business_sector_agriculture'] = np.where((1 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 7), 1, 0)
    df_zp['business_sector_retail'] = np.where((df_zp['noga_08'] == 47) | (df_zp['noga_08'] == 48), 1, 0)
    df_zp['business_sector_gastronomy'] = np.where((55 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 57), 1, 0)
    df_zp['business_sector_finance'] = np.where((64 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 67), 1, 0)
    df_zp['business_sector_production'] = np.where(((10 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 35)) |
                                                   ((40 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 44)), 1, 0)
    df_zp['business_sector_wholesale'] = np.where(((45 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 46)) |
                                                  ((49 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 54)), 1, 0)
    df_zp['business_sector_services_fc'] = np.where(((60 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 63)) |
                                                    ((69 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 83)) |
                                                    (df_zp['noga_08'] == 58), 1, 0)
    df_zp['business_sector_other_services'] = np.where(((86 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 90)) |
                                                       ((92 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 96)) |
                                                       (df_zp['noga_08'] == 59) |
                                                       (df_zp['noga_08'] == 68), 1, 0)
    df_zp['business_sector_others'] = np.where((97 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 98), 1, 0)
    df_zp['business_sector_non_movers'] = np.where(((8 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 9)) |
                                                   ((36 <= df_zp['noga_08']) & (df_zp['noga_08'] <= 39)) |
                                                   (df_zp['noga_08'] == 84) | (df_zp['noga_08'] == 85) |
                                                   (df_zp['noga_08'] == 91) | (df_zp['noga_08'] == 99), 1, 0)
    del df_zp['noga_08']

    ''' Deal with work percentage higher than 100 in MTMC (and not in SynPop) '''
    if year == 2015:
        df_zp['work_percentage'] = np.minimum((df_zp['full_part_time_job'] == 1) * 100 +
                                              df_zp['percentage_first_part_time_job'] *
                                              (df_zp['percentage_first_part_time_job'] > 0) +
                                              df_zp['percentage_second_part_time_job'] *
                                              (df_zp['percentage_second_part_time_job'] > 0),
                                              100)
        del df_zp['full_part_time_job']
        del df_zp['percentage_first_part_time_job']
        del df_zp['percentage_second_part_time_job']
    elif year == 2020:
        df_zp['work_percentage'] = np.minimum(df_zp['percentage_part_time_job'], 100)
        del df_zp['percentage_part_time_job']

    ''' Code the aggregate level of education '''
    if year == 2015:
        df_zp['no_post_school_educ'] = np.where((df_zp['highest_educ'] == 1) | (df_zp['highest_educ'] == 2) |
                                                (df_zp['highest_educ'] == 3) | (df_zp['highest_educ'] == 4), 1, 0)
        df_zp['secondary_education'] = np.where((df_zp['highest_educ'] == 5) | (df_zp['highest_educ'] == 6) |
                                                (df_zp['highest_educ'] == 7) | (df_zp['highest_educ'] == 8) |
                                                (df_zp['highest_educ'] == 9) | (df_zp['highest_educ'] == 10) |
                                                (df_zp['highest_educ'] == 11) | (df_zp['highest_educ'] == 12), 1, 0)
        df_zp['tertiary_education'] = np.where((df_zp['highest_educ'] == 13) | (df_zp['highest_educ'] == 14) |
                                               (df_zp['highest_educ'] == 15) | (df_zp['highest_educ'] == 16), 1, 0)
        df_zp['university'] = np.where((df_zp['highest_educ'] == 17) | (df_zp['highest_educ'] == 18) |
                                       (df_zp['highest_educ'] == 19), 1, 0)
    elif year == 2020:
        df_zp['no_post_school_educ'] = np.where((df_zp['highest_educ'] == 1) | (df_zp['highest_educ'] == 2), 1, 0)
        df_zp['secondary_education'] = np.where((df_zp['highest_educ'] == 3) | (df_zp['highest_educ'] == 4) |
                                       (df_zp['highest_educ'] == 5), 1, 0)
        df_zp['tertiary_education'] = np.where((df_zp['highest_educ'] == 6) | (df_zp['highest_educ'] == 7), 1, 0)
        df_zp['university'] = np.where((df_zp['highest_educ'] == 8) | (df_zp['highest_educ'] == 9), 1, 0)

    ''' Test that no column contains NA values '''
    for column in df_zp.columns:
        if df_zp[column].isna().any():
            print('There are NA values in column', column)
    ''' Save the file '''
    if year == 2015:
        output_directory = Path('../data/output/data/estimation/' + str(year))
    elif year == 2020:
        output_directory = Path('../data/output/data/validation_with_MTMC_2020/')
    data_file_name = 'persons.csv'
    df_zp.to_csv(output_directory / data_file_name, sep=';', index=False)


def add_home_work_distance(df_zp):
    """ Add the distance between home and work places """
    coding_with_coordinates = (df_zp.A_X != -999) & (df_zp.A_X != -997)
    job_in_switzerland = (df_zp.A_BFS != -99) & (df_zp.A_BFS != -97)
    df_zp_with_work_coordinates = df_zp[coding_with_coordinates & job_in_switzerland]
    geodf_home = geopandas.GeoDataFrame(df_zp_with_work_coordinates,
                                        geometry=geopandas.points_from_xy(df_zp_with_work_coordinates.W_X,
                                                                          df_zp_with_work_coordinates.W_Y),
                                        crs='epsg:4326')
    geodf_home.to_crs(epsg=21781, inplace=True)
    geodf_work = geopandas.GeoDataFrame(df_zp_with_work_coordinates,
                                        geometry=geopandas.points_from_xy(df_zp_with_work_coordinates.A_X,
                                                                          df_zp_with_work_coordinates.A_Y),
                                        crs='epsg:4326')
    geodf_work.to_crs(epsg=21781, inplace=True)
    df_zp.loc[coding_with_coordinates & job_in_switzerland, 'home_work_crow_fly_distance'] = \
        geodf_home.distance(geodf_work)
    df_zp['home_work_crow_fly_distance'].fillna(-999, inplace=True)
    df_zp.drop(['W_Y', 'W_X', 'A_Y', 'A_X'], axis=1, inplace=True)
    return df_zp


def add_spatial_typology(df_zp, year):
    """ Add the data about the spatial typology of the home address (in particular the home commune) """
    if year == 2015:
        path_to_typology = Path('../data/input/StadtLandTypologie/2015/Raumgliederungen.xlsx')
        spatial_typology_variable_name = 'Stadt/Land-Typologie'
    elif year == 2020:
        path_to_typology = Path('../data/input/StadtLandTypologie/2020/Raumgliederungen.xlsx')
        spatial_typology_variable_name = 'Städtische / Ländliche Gebiete'
    df_typology = pd.read_excel(path_to_typology, sheet_name='Daten',
                                skiprows=[0, 2],  # Removes the 1st row, with information, and the 2nd, with links
                                usecols='A,G')  # Selects only the BFS commune number and the column with the typology
    df_zp = pd.merge(df_zp, df_typology, left_on='W_BFS', right_on='BFS Gde-nummer', how='left')
    df_zp.drop('BFS Gde-nummer', axis=1, inplace=True)
    df_zp = df_zp.rename(columns={spatial_typology_variable_name: 'urban_typology_home'})

    ''' Add the data about the spatial typology of the work address (in particular the work commune) '''
    df_zp = pd.merge(df_zp, df_typology, left_on='A_BFS', right_on='BFS Gde-nummer', how='left')
    df_zp.drop('BFS Gde-nummer', axis=1, inplace=True)
    df_zp = df_zp.rename(columns={spatial_typology_variable_name: 'urban_typology_work'})
    df_zp.urban_typology_work.fillna(-99, inplace=True)
    return df_zp


def generate_work_position(row):
    work_position = 0  # corresponds to "not employed" - nicht erwerbstaetig / in MTMC: -99
    # in MTMC: 1 independent worker, "Selbstständig Erwerbende(r)",
    #          2 worker in a company owned by the person being interviewed,
    #            "Arbeitnehmer(in) in der AG oder GmbH, welche IHNEN selbst gehört",
    #          3 worker in a company owned by a member of the household,
    #            "Arbeitnehmer(in) im Familienbetrieb von einem Haushaltsmitglied"
    if (row['f40800_01'] == 1) | (row['f40800_01'] == 2) | (row['f40800_01'] == 3):
        work_position = 1  # corresponds to "independent worker"/"Selbststaendige"
    elif row['f40800_01'] == 4:  # in MTMC: employed in a private or public company
        # in MTMC: -98 no answer, "keine Antwort"
        #          -97 don't know, "weiss nicht"
        #            1 employee without executive function, "Angestellt ohne Cheffunktion"
        if (row['f41100_01'] == 1) | (row['f41100_01'] == -98) | (row['f41100_01'] == -97):
            work_position = 2  # corresponds to "employee"/"Angestellte"
        # in MTMC: 2 employee with executive function and subordinate employees,
        #            "Angestellt mit Chefposition und unterstellten Mitarbeitern"
        #          3 members of the direction, CEOs,
        #            "Angestellt als Mitglied von der Direktion oder Geschäftsleitung"
        elif (row['f41100_01'] == 2) | (row['f41100_01'] == 3):
            work_position = 3  # corresponds to "cadres"
        else:
            raise Exception("There should not be other cases...")
    elif row['f40800_01'] == 5:  # in Mobility and Transport Microcensus: apprentice
        work_position = 2  # corresponds to "employee"/"Angestellte"
    return work_position


def define_mobility_resources_variable(row):
    """ This is the version of the choice variable used for the generation of the synthetic population (SynPop)."""
    if row['car_avail'] == -98:  # no information about car availability
        return -98
    elif row['car_avail'] == 1 or row['car_avail'] == 2:  # car always available or available on demand
        if row['GA_ticket'] == 1:  # GA
            if row['halbtax_ticket'] == 1:
                # Warning: Person with car available, GA and HT are considered as "car + GA"
                return 1
            elif row['halbtax_ticket'] == 2:  # No HT
                return 1  # Auto + GA (no HT)
            else:
                return -98
        elif row['GA_ticket'] == 2:  # No GA
            if row['halbtax_ticket'] == 1:  # HT
                if row['Verbund_Abo'] == 1:
                    return 20  # Auto + HT + Verbundabo (no GA)
                elif row['Verbund_Abo'] == 2:
                    return 2  # Auto + HT (no GA, no Verbundabo)
                else:  # no info about Verbundabo
                    return -98
            elif row['halbtax_ticket'] == 2:  # No HT
                if row['Verbund_Abo'] == 1:
                    return 30  # Auto + Verbundabo (no GA, no HT)
                elif row['Verbund_Abo'] == 2:
                    return 3  # Car available (no GA, no Verbundabo, no HT)
                else:  # no info about Verbundabo
                    return -98
            else:  # no info about HT
                return -98
        else:  # no information about GA
            return -98
    # car not available, available on demand, or people younger than 18 or without driving license
    elif row['car_avail'] == 3 or row['car_avail'] == -99:
        if row['GA_ticket'] == 1:  # GA
            if row['halbtax_ticket'] == 1:
                # print 'Warning: person with GA and HT!'
                return 4
            # No HT or not available to people younger than 16
            elif row['halbtax_ticket'] == 2 or row['halbtax_ticket'] == -99:
                return 4  # GA (no HT)
            else:
                return -98
        elif row['GA_ticket'] == 2:  # No GA
            if row['halbtax_ticket'] == 1:  # HT
                if row['Verbund_Abo'] == 1:
                    return 50  # HT + Verbundabo (no GA)
                elif row['Verbund_Abo'] == 2:
                    return 5  # HT (no GA, no Verbundabo)
                else:  # no info about Verbundabo
                    return -98
            # No HT or not available to people younger than 16
            elif row['halbtax_ticket'] == 2 or row['halbtax_ticket'] == -99:
                if row['Verbund_Abo'] == 1:
                    return 60  # Verbundabo (no GA, no HT)
                elif row['Verbund_Abo'] == 2:
                    return 6  # Nothing (no GA, no Verbundabo, no HT)
                else:  # no info about Verbundabo
                    return -98
            else:  # no info about HT
                return -98
        else:  # no information about GA
            return -98
    elif row['car_avail'] == -98 or row['car_avail'] == -97:  # no answer or does not know
        return -98
