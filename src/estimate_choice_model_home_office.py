import pandas as pd
from pathlib import Path
import geopandas
import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import Beta, DefineVariable
import os
from utils_mtmc.get_mtmc_files import get_zp, get_hh


def estimate_choice_model_home_office():
    generate_data_file()
    data_file_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    output_directory = '../data/output/models/estimation/'
    run_estimation(data_file_directory, data_file_name, output_directory)


def run_estimation(data_file_directory, data_file_name, output_directory, output_file_name='logit_home_office'):
    """
    :author: Antonin Danalet, based on the example '01logit.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    A binary logit model on the possibility to work from home at least some times."""

    # Read the data

    df = pd.read_csv(data_file_directory / data_file_name, ';')
    database = db.Database('persons', df)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    # Parameters to be estimated
    alternative_specific_constant = Beta('alternative_specific_constant', 0, None, None, 0)

    b_no_post_school_education = Beta('b_no_post_school_education', 0, None, None, 0)
    b_secondary_education = Beta('b_secondary_education', 0, None, None, 0)
    b_tertiary_education = Beta('b_tertiary_education', 0, None, None, 0)
    b_university = Beta('b_university', 0, None, None, 1)

    b_male = Beta('b_male', 0, None, None, 1)

    b_single_household = Beta('b_single_household', 0, None, None, 0)
    b_couple_without_children = Beta('b_couple_without_children', 0, None, None, 1)
    b_couple_with_children = Beta('b_couple_with_children', 0, None, None, 1)
    b_single_parent_with_children = Beta('b_single_parent_with_children', 0, None, None, 1)
    b_not_family_household = Beta('b_not_family_household', 0, None, None, 1)

    b_public_transport_connection_quality_are_a = Beta('b_public_transport_connection_quality_are_a', 0, None, None, 1)
    b_public_transport_connection_quality_are_b = Beta('b_public_transport_connection_quality_are_b', 0, None, None, 1)
    b_public_transport_connection_quality_are_c = Beta('b_public_transport_connection_quality_are_c', 0, None, None, 1)
    b_public_transport_connection_quality_are_d = Beta('b_public_transport_connection_quality_are_d', 0, None, None, 1)
    b_public_transport_connection_quality_are_na = Beta('b_public_transport_connection_quality_are_na', 0, None, None,
                                                        0)

    b_urban = Beta('b_urban', 0, None, None, 1)
    b_rural = Beta('b_rural', 0, None, None, 1)
    b_intermediate = Beta('b_intermediate', 0, None, None, 1)

    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)

    b_business_sector_agriculture = Beta('b_business_sector_agriculture', 0, None, None, 0)
    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale = Beta('b_business_sector_wholesale', 0, None, None, 1)
    b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 0)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 1)
    b_business_sector_services_fC = Beta('b_business_sector_services_fC', 0, None, None, 0)
    b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 1)
    b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 1)
    b_business_sector_non_movers = Beta('b_business_sector_non_movers', 0, None, None, 0)
    b_employees = Beta('b_employees', 0, None, None, 1)
    b_executives = Beta('b_executives', 0, None, None, 0)
    b_german = Beta('b_german', 0, None, None, 0)
    b_nationality_ch_germany_france_italy_nw_e = Beta('b_nationality_ch_germany_france_italy_nw_e', 0, None, None, 0)
    b_nationality_south_west_europe = Beta('b_nationality_south_west_europe', 0, None, None, 1)
    b_nationality_southeast_europe = Beta('b_nationality_southeast_europe', 0, None, None, 1)
    b_several_part_time_jobs = Beta('b_several_part_time_jobs', 0, None, None, 0)
    b_work_percentage = Beta('b_work_percentage', 0, None, None, 0)

    # Definition of new variables
    no_post_school_educ = DefineVariable('no_post_school_educ',
                                         (highest_educ == 1) | (highest_educ == 2) | (highest_educ == 3) |
                                         (highest_educ == 4), database)
    secondary_education = DefineVariable('secondary_education',
                                         (highest_educ == 5) | (highest_educ == 6) | (highest_educ == 7) |
                                         (highest_educ == 8) | (highest_educ == 9) | (highest_educ == 10) |
                                         (highest_educ == 11) | (highest_educ == 12), database)
    tertiary_education = DefineVariable('tertiary_education',
                                        (highest_educ == 13) | (highest_educ == 14) |
                                        (highest_educ == 15) | (highest_educ == 16), database)
    university = DefineVariable('university', (highest_educ == 17) * 10, database)

    male = DefineVariable('male', sex == 1, database)

    single_household = DefineVariable('single_household', hh_type == 10, database)
    couple_without_children = DefineVariable('couple_without_children', hh_type == 210, database)
    couple_with_children = DefineVariable('couple_with_children', hh_type == 220, database)
    single_parent_with_children = DefineVariable('single_parent_with_children', hh_type == 230, database)
    not_family_household = DefineVariable('not_family_household', hh_type == 30, database)

    public_transport_connection_quality_ARE_A = DefineVariable('public_transport_connection_quality_ARE_A',
                                                               public_transport_connection_quality_ARE == 1, database)
    public_transport_connection_quality_ARE_B = DefineVariable('public_transport_connection_quality_ARE_B',
                                                               public_transport_connection_quality_ARE == 2, database)
    public_transport_connection_quality_ARE_C = DefineVariable('public_transport_connection_quality_ARE_C',
                                                               public_transport_connection_quality_ARE == 3, database)
    public_transport_connection_quality_ARE_D = DefineVariable('public_transport_connection_quality_ARE_D',
                                                               public_transport_connection_quality_ARE == 4, database)
    public_transport_connection_quality_ARE_NA = DefineVariable('public_transport_connection_quality_ARE_NA',
                                                                public_transport_connection_quality_ARE == 5, database)

    urban = DefineVariable('urban', urban_typology == 1, database)
    rural = DefineVariable('rural', urban_typology == 3, database)
    intermediate = DefineVariable('intermediate', urban_typology == 2, database)

    home_work_distance = DefineVariable('home_work_distance',
                                        home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0,
                                        database)

    business_sector_agriculture = DefineVariable('business_sector_agriculture', 1 <= noga_08 <= 7, database)
    business_sector_retail = DefineVariable('business_sector_retail', 47 <= noga_08 <= 47, database)
    business_sector_gastronomy = DefineVariable('business_sector_gastronomy', 55 <= noga_08 <= 57, database)
    business_sector_finance = DefineVariable('business_sector_finance', 64 <= noga_08 <= 67, database)
    business_sector_production = DefineVariable('business_sector_production',
                                                (10 <= noga_08 <= 35) | (40 <= noga_08 <= 44), database)
    business_sector_wholesale = DefineVariable('business_sector_wholesale',
                                               (45 <= noga_08 <= 45) | (49 <= noga_08 <= 54), database)
    business_sector_services_fC = DefineVariable('business_sector_services_fC',
                                                 (60 <= noga_08 <= 63) | (69 <= noga_08 <= 83) | (noga_08 == 58),
                                                 database)
    business_sector_other_services = DefineVariable('business_sector_other_services',
                                                    (86 <= noga_08 <= 90) | (92 <= noga_08 <= 96) | (noga_08 == 59) |
                                                    (noga_08 == 68),
                                                    database)
    business_sector_others = DefineVariable('business_sector_others', 97 <= noga_08 <= 98, database)
    business_sector_non_movers = DefineVariable('business_sector_non_movers',
                                                (8 <= noga_08 <= 9) | (36 <= noga_08 <= 39) | (84 <= noga_08 <= 85) |
                                                (noga_08 == 91) | (noga_08 == 99),
                                                database)

    employees = DefineVariable('employees', work_position == 2, database)
    executives = DefineVariable('executives', (work_position == 3) + (work_position == 1), database)

    german = DefineVariable('german', language == 1, database)

    nationality_switzerland = DefineVariable('nationality_switzerland', nation == 8100, database)
    nationality_germany_austria_lichtenstein = DefineVariable('nationality_germany_austria_lichtenstein',
                                                              (nation == 8207) | (nation == 8229) | (nation == 8222),
                                                              database)
    nationality_italy_vatican = DefineVariable('nationality_italy_vatican', (nation == 8218) | (nation == 8241),
                                                              database)
    nationality_france_monaco_san_marino = DefineVariable('nationality_france_monaco_san_marino',
                                                          (nation == 8212) | (nation == 8226) | (nation == 8233),
                                                          database)
    nationality_northwestern_europe = DefineVariable('nationality_northwestern_europe',
                                                  (nation == 8204) |  # Belgium
                                                  (nation == 8223) |  # Luxembourg
                                                  (nation == 8227) |  # Netherlands
                                                  (nation == 8206) |  # Denmark
                                                  (nation == 8211) |  # Finland
                                                  (nation == 8215) |  # United Kingdom
                                                  (nation == 8216) |  # Ireland
                                                  (nation == 8217) |  # Iceland
                                                  (nation == 8228) |  # Norway
                                                  (nation == 8234),  # Sweden
                                                  database)
    nationality_south_west_europe = DefineVariable('nationality_south_west_europe',
                                                   (nation == 8231) |  # Portugal
                                                   (nation == 8236) |  # Spain
                                                   (nation == 8202),  # Andorra
                                                   database)
    nationality_southeast_europe = DefineVariable('nationality_southeast_europe',
                                                  (nation == 8224) |  # Malta
                                                  (nation == 8201) |  # Albania
                                                  (nation == 8214) |  # Greece
                                                  (nation == 8256) |  # Kosovo
                                                  (nation == 8250) |  # Croatia
                                                  (nation == 8251) |  # Slovenia
                                                  (nation == 8252) |  # Bosnia and Herzegovina
                                                  (nation == 8255) |  # Macedonia
                                                  (nation == 8205) |  # Bulgaria
                                                  (nation == 8239) |  # Turkey
                                                  (nation == 8242) |  # Cyprus
                                                  (nation == 8248) |  # Serbia
                                                  (nation == 8254),  # Montenegro
                                                  database)
    nationality_eastern_europe = DefineVariable('nationality_eastern_europe',
                                                (nation == 8230) |  # Poland
                                                (nation == 8232) |  # Rumania
                                                (nation == 8240) |  # Hungary
                                                (nation == 8243) |  # Slovakia
                                                (nation == 8244) |  # Czech Republic
                                                (nation == 8263) |  # Moldavia
                                                (nation == 8265) |  # Ukraine
                                                (nation == 8266) |  # Belarus
                                                (nation == 8260) |  # Estonia
                                                (nation == 8261) |  # Latvia
                                                (nation == 8262),  # Lithuania
                                                database)

    several_part_time_jobs = DefineVariable('several_part_time_jobs', full_part_time_job == 3, database)
    work_percentage = DefineVariable('work_percentage',
                                     (full_part_time_job == 1) * 100 +
                                     percentage_first_part_time_job * (percentage_first_part_time_job > 0) +
                                     percentage_second_part_time_job * (percentage_second_part_time_job > 0),
                                     database)

    #  Utility
    U = alternative_specific_constant + \
        b_executives * executives + \
        b_employees * employees + \
        b_no_post_school_education * no_post_school_educ + \
        b_secondary_education * secondary_education + \
        b_tertiary_education * tertiary_education + \
        b_university * university + \
        b_male * male + \
        b_single_household * single_household + \
        b_couple_without_children * couple_without_children + \
        b_couple_with_children * couple_with_children + \
        b_single_parent_with_children * single_parent_with_children + \
        b_not_family_household * not_family_household + \
        b_public_transport_connection_quality_are_a * public_transport_connection_quality_ARE_A + \
        b_public_transport_connection_quality_are_b * public_transport_connection_quality_ARE_B + \
        b_public_transport_connection_quality_are_c * public_transport_connection_quality_ARE_C + \
        b_public_transport_connection_quality_are_d * public_transport_connection_quality_ARE_D + \
        b_public_transport_connection_quality_are_na * public_transport_connection_quality_ARE_NA + \
        b_urban * urban + \
        b_rural * rural + \
        b_intermediate * intermediate + \
        b_home_work_distance * home_work_distance + \
        models.piecewiseFormula(age, [0, 20, 35, 75, 200]) + \
        b_business_sector_agriculture * business_sector_agriculture + \
        b_business_sector_retail * business_sector_retail + \
        b_business_sector_gastronomy * business_sector_gastronomy + \
        b_business_sector_finance * business_sector_finance + \
        b_business_sector_production * business_sector_production + \
        b_business_sector_wholesale * business_sector_wholesale + \
        b_business_sector_services_fC * business_sector_services_fC + \
        b_business_sector_other_services * business_sector_other_services + \
        b_business_sector_others * business_sector_others + \
        b_business_sector_non_movers * business_sector_non_movers + \
        b_german * german + \
        b_nationality_ch_germany_france_italy_nw_e * nationality_switzerland + \
        b_nationality_ch_germany_france_italy_nw_e * nationality_germany_austria_lichtenstein + \
        b_nationality_ch_germany_france_italy_nw_e * nationality_italy_vatican + \
        b_nationality_ch_germany_france_italy_nw_e * nationality_france_monaco_san_marino + \
        b_nationality_ch_germany_france_italy_nw_e * nationality_northwestern_europe + \
        b_nationality_south_west_europe * nationality_south_west_europe + \
        b_nationality_southeast_europe * nationality_southeast_europe + \
        b_nationality_ch_germany_france_italy_nw_e * nationality_eastern_europe + \
        b_several_part_time_jobs * several_part_time_jobs + \
        models.piecewiseFormula(work_percentage, [0, 20, 170])
    U_No_home_office = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U,  # Yes or sometimes
         0: U_No_home_office}  # No

    av = {1: 1,
          0: 1}

    # Definition of the model. This is the contribution of each
    # observation to the log likelihood function.
    logprob = models.loglogit(V, av,  # All alternatives are supposed to be always available
                              home_office)  # Choice variable

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    standard_directory = os.getcwd()
    os.chdir(output_directory)

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, logprob)
    biogeme.modelName = output_file_name

    # Estimate the parameters
    results = biogeme.estimate()

    # Get the results in a pandas table
    pandas_results = results.getEstimatedParameters()
    print(pandas_results)

    # Go back to the normal working directory
    os.chdir(standard_directory)


def generate_data_file():
    """ This function takes as input the  data about the person and join them with the data about the household and the
        spaptial typology. It returns nothing, but saves the output as a data file for Biogeme.
        :param: Nothing.
        :return: Nothing. The dataframe is saved as a CSV file (separator: tab) without NA values, to be used with
        Biogeme.
        """
    ''' Select the variables about the person from the tables of the MTMC 2015 '''
    selected_columns_zp = ['gesl', 'HAUSB', 'HHNR', 'f81300', 'A_X_CH1903', 'A_Y_CH1903', 'alter', 'f81400', 'noga_08',
                           'sprache', 'f40800_01', 'f41100_01', 'nation', 'f40900', 'f40901_02', 'f40903']
    df_zp = get_zp(2015, selected_columns_zp)
    selected_columns_hh = ['HHNR', 'hhtyp', 'W_OeV_KLASSE', 'W_BFS', 'W_X_CH1903', 'W_Y_CH1903']
    df_hh = get_hh(2015, selected_columns_hh)
    df_zp = pd.merge(df_zp, df_hh, on='HHNR', how='left')

    ''' Add the distance between home and work places '''
    df_zp_with_work_coordinates = df_zp[df_zp.A_X_CH1903 != -999]
    geodf_home = geopandas.GeoDataFrame(df_zp_with_work_coordinates,
                                        geometry=geopandas.points_from_xy(df_zp_with_work_coordinates.W_Y_CH1903,
                                                                          df_zp_with_work_coordinates.W_X_CH1903),
                                        crs='epsg:21781')
    geodf_work = geopandas.GeoDataFrame(df_zp_with_work_coordinates,
                                        geometry=geopandas.points_from_xy(df_zp_with_work_coordinates.A_Y_CH1903,
                                                                          df_zp_with_work_coordinates.A_X_CH1903),
                                        crs='epsg:21781')
    df_zp.loc[df_zp.A_X_CH1903 != -999, 'home_work_crow_fly_distance'] = geodf_home.distance(geodf_work)
    df_zp['home_work_crow_fly_distance'].fillna(-999, inplace=True)
    df_zp.drop(['W_Y_CH1903', 'W_X_CH1903', 'A_Y_CH1903', 'A_X_CH1903'], axis=1, inplace=True)

    ''' Add the data about the spatial typology '''
    path_to_typology = Path('../data/input/StadtLandTypologie/2015/Raumgliederungen.xlsx')
    df_typology = pd.read_excel(path_to_typology, sheet_name='Daten',
                                skiprows=[0, 2],  # Removes the 1st row, with information, and the 2nd, with links
                                usecols='A,G')  # Selects only the BFS commune number and the column with the typology
    df_zp = pd.merge(df_zp, df_typology, left_on='W_BFS', right_on='BFS Gde-nummer', how='left')
    df_zp.drop('BFS Gde-nummer', axis=1, inplace=True)

    ''' Generate the variable about work position:
         0 not employed / nicht erwerbstaetig
         1 independent worker / Selbststaendige
         2 employee / Angestellte
         3 cadres / Kader '''
    df_zp['work_position'] = df_zp.apply(generate_work_position, axis=1)

    # Rename the variables
    df_zp = df_zp.rename(columns={'gesl': 'sex',
                                  'HAUSB': 'highest_educ',
                                  'f81300': 'home_office_is_possible',
                                  'hhtyp': 'hh_type',
                                  'W_OeV_KLASSE': 'public_transport_connection_quality_ARE',
                                  'Stadt/Land-Typologie': 'urban_typology',
                                  'alter': 'age',
                                  'f81400': 'percentage_home_office',
                                  'sprache': 'language',
                                  'f40900': 'full_part_time_job',
                                  'f40901_02': 'percentage_first_part_time_job',
                                  'f40903': 'percentage_second_part_time_job'})
    ''' Removing people who did not get the question or did not answer. '''
    df_zp.drop(df_zp[df_zp.home_office_is_possible < 0].index, inplace=True)
    ''' Define the variable home office as "possibility to do home office" and "practically do some" '''
    df_zp['home_office'] = df_zp.apply(define_home_office_variable, axis=1)
    ''' Test that no column contains NA values '''
    for column in df_zp.columns:
        if df_zp[column].isna().any():
            print('There are NA values in column', column)
    ''' Save the file '''
    output_directory = Path('../data/output/data/estimation/')
    data_file_name = 'persons.csv'
    df_zp.to_csv(output_directory / data_file_name, sep=';', index=False)


def define_home_office_variable(row):
    """ Defines a choice variable with value 1 if the person is allowed to do home office
    (answer "yes" - 1 - or answer "sometimes" - 2) and does it at least 1% of the time """
    home_office = 0
    if ((row['home_office_is_possible'] == 1) or (row['home_office_is_possible'] == 2)) \
            and row['percentage_home_office'] > 0:
        home_office = 1
    return home_office


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
    elif row['f40800_01'] == 5:  # in MTMC: apprentice
        work_position = 2  # corresponds to "employee"/"Angestellte"
    return work_position
