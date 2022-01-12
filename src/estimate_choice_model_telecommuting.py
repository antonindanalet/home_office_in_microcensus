import pandas as pd
from pathlib import Path
import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import Beta, DefineVariable
import os
from utils_mtmc.generate_data_file import generate_data_file


def estimate_choice_model_telecommuting():
    generate_data_file(2015)
    data_file_directory = Path('../data/output/data/estimation/2015/')
    data_file_name = 'persons.csv'
    output_directory = '../data/output/models/estimation/2015/'
    output_file_name = 'logit_telecommuting_2015'
    run_estimation(data_file_directory, data_file_name, output_directory, output_file_name=output_file_name)


def run_estimation(data_file_directory, data_file_name, output_directory, output_file_name='logit_telecommuting'):
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

    b_single_household = Beta('b_single_household', 0, None, None, 1)
    b_couple_without_children = Beta('b_couple_without_children', 0, None, None, 0)
    b_couple_with_children = Beta('b_couple_with_children', 0, None, None, 1)
    b_single_parent_with_children = Beta('b_single_parent_with_children', 0, None, None, 1)
    b_not_family_household = Beta('b_not_family_household', 0, None, None, 1)

    b_public_transport_connection_quality_are_a_home = Beta('b_public_transport_connection_quality_are_a_home',
                                                            0, None, None, 1)
    b_public_transport_connection_quality_are_b_home = Beta('b_public_transport_connection_quality_are_b_home',
                                                            0, None, None, 1)
    b_public_transport_connection_quality_are_c_home = Beta('b_public_transport_connection_quality_are_c_home',
                                                            0, None, None, 1)
    b_public_transport_connection_quality_are_d_home = Beta('b_public_transport_connection_quality_are_d_home',
                                                            0, None, None, 1)
    b_public_transport_connection_quality_are_na_home = Beta('b_public_transport_connection_quality_are_na_home',
                                                             0, None, None, 0)

    b_public_transport_connection_quality_are_a_work = Beta('b_public_transport_connection_quality_are_a_work',
                                                            0, None, None, 1)
    b_public_transport_connection_quality_are_b_work = Beta('b_public_transport_connection_quality_are_b_work',
                                                            0, None, None, 1)
    b_public_transport_connection_quality_are_c_work = Beta('b_public_transport_connection_quality_are_c_work',
                                                            0, None, None, 1)
    b_public_transport_connection_quality_are_d_work = Beta('b_public_transport_connection_quality_are_d_work',
                                                            0, None, None, 1)
    b_public_transport_connection_quality_are_na_work = Beta('b_public_transport_connection_quality_are_na_work',
                                                             0, None, None, 1)

    b_urban_home = Beta('b_urban_home', 0, None, None, 1)
    b_rural_home = Beta('b_rural_home', 0, None, None, 1)
    b_intermediate_home = Beta('b_intermediate_home', 0, None, None, 1)
    b_urban_work = Beta('b_urban_work', 0, None, None, 1)
    b_rural_work = Beta('b_rural_work', 0, None, None, 1)
    b_intermediate_work = Beta('b_intermediate_work', 0, None, None, 1)

    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)
    b_home_work_distance_zero = Beta('b_home_work_distance_zero', 0, None, None, 0)
    b_home_work_distance_na = Beta('b_home_work_distance_na', 0, None, None, 0)

    b_business_sector_agriculture = Beta('b_business_sector_agriculture', 0, None, None, 1)
    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale = Beta('b_business_sector_wholesale', 0, None, None, 0)
    b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 0)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 0)
    b_business_sector_services_fc = Beta('b_business_sector_services_fc', 0, None, None, 1)
    b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 0)
    b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 0)
    b_business_sector_non_movers = Beta('b_business_sector_non_movers', 0, None, None, 0)
    b_employees = Beta('b_employees', 0, None, None, 1)
    b_executives = Beta('b_executives', 0, None, None, 0)
    b_german = Beta('b_german', 0, None, None, 0)
    b_nationality_ch_germany_france_italy_nw_e = Beta('b_nationality_ch_germany_france_italy_nw_e', 0, None, None, 1)
    b_nationality_south_west_europe = Beta('b_nationality_south_west_europe', 0, None, None, 1)
    b_nationality_southeast_europe = Beta('b_nationality_southeast_europe', 0, None, None, 1)
    # b_several_part_time_jobs = Beta('b_several_part_time_jobs', 0, None, None, 1)
    b_hh_income_na = Beta('b_hh_income_na', 0, None, None, 0)
    b_hh_income_8000_or_less = Beta('b_hh_income_8000_or_less', 0, None, None, 0)
    b_hh_income_more_than_8000 = Beta('b_hh_income_more_than_8000', 0, None, None, 1)

    b_general_abo = Beta('b_general_abo', 0, None, None, 0)
    b_regional_abo = Beta('b_regional_abo', 0, None, None, 1)
    b_regional_abo_na = Beta('b_regional_abo_na', 0, None, None, 1)
    b_half_fare_abo = Beta('b_half_fare_abo', 0, None, None, 1)
    b_half_fare_abo_na = Beta('b_half_fare_abo_na', 0, None, None, 1)
    b_car_avail = Beta('b_car_avail', 0, None, None, 1)
    b_car_avail_na = Beta('b_car_avail_na', 0, None, None, 1)

    b_mobility_resource_na = Beta('b_mobility_resource_na', 0, None, None, 0)
    b_mobility_resource_car_general_abo = Beta('b_mobility_resource_car_general_abo', 0, None, None, 1)
    b_mobility_resource_car_half_fare_abo = Beta('b_mobility_resource_car_half_fare_abo', 0, None, None, 0)
    b_mobility_resource_car = Beta('b_mobility_resource_car', 0, None, None, 1)
    b_mobility_resource_general_abo = Beta('b_mobility_resource_general_abo', 0, None, None, 1)
    b_mobility_resource_half_fare_abo = Beta('b_mobility_resource_half_fare_abo', 0, None, None, 1)
    b_mobility_resource_none = Beta('b_mobility_resource_none', 0, None, None, 1)
    b_mobility_resource_car_half_fare_regional_abo = Beta('b_mobility_resource_car_half_fare_regional_abo',
                                                          0, None, None, 1)
    b_mobility_resource_car_regional_abo = Beta('b_mobility_resource_car_regional_abo', 0, None, None, 1)
    b_mobility_resource_half_fare_regional_abo = Beta('b_mobility_resource_half_fare_regional_abo', 0, None, None, 1)
    b_mobility_resource_regional_abo = Beta('b_mobility_resource_regional_abo', 0, None, None, 1)

    # Definition of new variables
    male = DefineVariable('male', sex == 1, database)

    single_household = DefineVariable('single_household', hh_type == 10, database)
    couple_without_children = DefineVariable('couple_without_children', hh_type == 210, database)
    couple_with_children = DefineVariable('couple_with_children', hh_type == 220, database)
    single_parent_with_children = DefineVariable('single_parent_with_children', hh_type == 230, database)
    not_family_household = DefineVariable('not_family_household', hh_type == 30, database)

    public_transport_connection_quality_ARE_A_home = DefineVariable('public_transport_connection_quality_ARE_A_home',
                                                                    public_transport_connection_quality_ARE_home == 1,
                                                                    database)
    public_transport_connection_quality_ARE_B_home = DefineVariable('public_transport_connection_quality_ARE_B_home',
                                                                    public_transport_connection_quality_ARE_home == 2,
                                                                    database)
    public_transport_connection_quality_ARE_C_home = DefineVariable('public_transport_connection_quality_ARE_C_home',
                                                                    public_transport_connection_quality_ARE_home == 3,
                                                                    database)
    public_transport_connection_quality_ARE_D_home = DefineVariable('public_transport_connection_quality_ARE_D_home',
                                                                    public_transport_connection_quality_ARE_home == 4,
                                                                    database)
    public_transport_connection_quality_ARE_NA_home = DefineVariable('public_transport_connection_quality_ARE_NA_home',
                                                                     public_transport_connection_quality_ARE_home == 5,
                                                                     database)

    public_transport_connection_quality_ARE_A_work = DefineVariable('public_transport_connection_quality_ARE_A_work',
                                                                    public_transport_connection_quality_ARE_work == 1,
                                                                    database)
    public_transport_connection_quality_ARE_B_work = DefineVariable('public_transport_connection_quality_ARE_B_work',
                                                                    public_transport_connection_quality_ARE_work == 2,
                                                                    database)
    public_transport_connection_quality_ARE_C_work = DefineVariable('public_transport_connection_quality_ARE_C_work',
                                                                    public_transport_connection_quality_ARE_work == 3,
                                                                    database)
    public_transport_connection_quality_ARE_D_work = DefineVariable('public_transport_connection_quality_ARE_D_work',
                                                                    public_transport_connection_quality_ARE_work == 4,
                                                                    database)
    public_transport_connection_quality_ARE_NA_work = DefineVariable('public_transport_connection_quality_ARE_NA_work',
                                                                     public_transport_connection_quality_ARE_work == 5,
                                                                     database)

    urban_home = DefineVariable('urban_home', urban_typology_home == 1, database)
    rural_home = DefineVariable('rural_home', urban_typology_home == 3, database)
    intermediate_home = DefineVariable('intermediate_home', urban_typology_home == 2, database)
    urban_work = DefineVariable('urban_work', urban_typology_work == 1, database)
    rural_work = DefineVariable('rural_work', urban_typology_work == 3, database)
    intermediate_work = DefineVariable('intermediate_work', urban_typology_work == 2, database)

    home_work_distance = DefineVariable('home_work_distance',
                                        home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0,
                                        database)
    home_work_distance_zero = DefineVariable('home_work_distance_zero', home_work_crow_fly_distance == 0.0, database)
    home_work_distance_na = DefineVariable('home_work_distance_na', home_work_crow_fly_distance == -999, database)

    employees = DefineVariable('employees', work_position == 2, database)
    executives = DefineVariable('executives', work_position == 1, database)

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

    # several_part_time_jobs = DefineVariable('several_part_time_jobs', full_part_time_job == 3, database)

    hh_income_na = DefineVariable('hh_income_na', hh_income < 0, database)
    hh_income_less_than_2000 = DefineVariable('hh_income_less_than_4000', hh_income == 1, database)
    hh_income_2000_to_4000 = DefineVariable('hh_income_2000_to_4000', hh_income == 2, database)
    hh_income_4001_to_6000 = DefineVariable('hh_income_4001_to_6000', hh_income == 3, database)
    hh_income_6001_to_8000 = DefineVariable('hh_income_6001_to_8000', hh_income == 4, database)
    hh_income_8001_to_10000 = DefineVariable('hh_income_8001_to_10000', hh_income == 5, database)
    hh_income_10001_to_12000 = DefineVariable('hh_income_10001_to_12000', hh_income == 6, database)
    hh_income_12001_to_14000 = DefineVariable('hh_income_12001_to_14000', hh_income == 7, database)
    hh_income_14001_to_16000 = DefineVariable('hh_income_14001_to_16000', hh_income == 8, database)
    hh_income_more_than_16000 = DefineVariable('hh_income_more_than_16000', hh_income == 9, database)

    general_abo = DefineVariable('general_abo', GA_ticket == 1, database)
    regional_abo = DefineVariable('regional_abo', Verbund_Abo == 1, database)
    half_fare_abo = DefineVariable('half_fare_abo', halbtax_ticket == 1, database)
    car_avail_always_or_on_demand = DefineVariable('car_avail_always_or_on_demand', (car_avail == 1) | (car_avail == 2),
                                                   database)
    regional_abo_na = DefineVariable('regional_abo_na', Verbund_Abo < 0, database)
    half_fare_abo_na = DefineVariable('half_fare_abo_na', halbtax_ticket < 0, database)
    car_avail_na = DefineVariable('car_avail_na', car_avail < 0, database)

    mobility_resource_na = DefineVariable('mobility_resource_na', mobility_resources == -98, database)
    mobility_resource_car_general_abo = DefineVariable('mobility_resource_car_general_abo', mobility_resources == 1,
                                                       database)
    mobility_resource_car_half_fare_abo = DefineVariable('mobility_resource_car_half_fare_abo', mobility_resources == 2,
                                                         database)
    mobility_resource_car = DefineVariable('mobility_resource_car', mobility_resources == 3, database)
    mobility_resource_general_abo = DefineVariable('mobility_resource_general_abo', mobility_resources == 4, database)
    mobility_resource_half_fare_abo = DefineVariable('mobility_resource_half_fare_abo', mobility_resources == 5,
                                                     database)
    mobility_resource_none = DefineVariable('mobility_resource_none', mobility_resources == 6, database)
    mobility_resource_car_half_fare_regional_abo = DefineVariable('mobility_resource_car_half_fare_regional_abo',
                                                                  mobility_resources == 20, database)
    mobility_resource_car_regional_abo = DefineVariable('mobility_resource_car_regional_abo',
                                                        mobility_resources == 30, database)
    mobility_resource_half_fare_regional_abo = DefineVariable('mobility_resource_half_fare_regional_abo',
                                                              mobility_resources == 50, database)
    mobility_resource_regional_abo = DefineVariable('mobility_resource_regional_abo',
                                                    mobility_resources == 60, database)

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
        b_public_transport_connection_quality_are_a_home * public_transport_connection_quality_ARE_A_home + \
        b_public_transport_connection_quality_are_b_home * public_transport_connection_quality_ARE_B_home + \
        b_public_transport_connection_quality_are_c_home * public_transport_connection_quality_ARE_C_home + \
        b_public_transport_connection_quality_are_d_home * public_transport_connection_quality_ARE_D_home + \
        b_public_transport_connection_quality_are_na_home * public_transport_connection_quality_ARE_NA_home + \
        b_public_transport_connection_quality_are_a_work * public_transport_connection_quality_ARE_A_work + \
        b_public_transport_connection_quality_are_b_work * public_transport_connection_quality_ARE_B_work + \
        b_public_transport_connection_quality_are_c_work * public_transport_connection_quality_ARE_C_work + \
        b_public_transport_connection_quality_are_d_work * public_transport_connection_quality_ARE_D_work + \
        b_public_transport_connection_quality_are_na_work * public_transport_connection_quality_ARE_NA_work + \
        b_urban_home * urban_home + \
        b_rural_home * rural_home + \
        b_intermediate_home * intermediate_home + \
        b_urban_work * urban_work + \
        b_rural_work * rural_work + \
        b_intermediate_work * intermediate_work + \
        b_home_work_distance * home_work_distance + \
        b_home_work_distance_zero * home_work_distance_zero + \
        b_home_work_distance_na * home_work_distance_na + \
        models.piecewiseFormula(age, [15, 19, 31, 79, 85]) + \
        b_business_sector_agriculture * business_sector_agriculture + \
        b_business_sector_retail * business_sector_retail + \
        b_business_sector_gastronomy * business_sector_gastronomy + \
        b_business_sector_finance * business_sector_finance + \
        b_business_sector_production * business_sector_production + \
        b_business_sector_wholesale * business_sector_wholesale + \
        b_business_sector_services_fc * business_sector_services_fc + \
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
        models.piecewiseFormula(work_percentage, [0, 90, 101]) + \
        b_hh_income_na * hh_income_na + \
        b_hh_income_8000_or_less * hh_income_less_than_2000 + \
        b_hh_income_8000_or_less * hh_income_2000_to_4000 + \
        b_hh_income_8000_or_less * hh_income_4001_to_6000 + \
        b_hh_income_8000_or_less * hh_income_6001_to_8000 + \
        b_hh_income_more_than_8000 * hh_income_8001_to_10000 + \
        b_hh_income_more_than_8000 * hh_income_10001_to_12000 + \
        b_hh_income_more_than_8000 * hh_income_12001_to_14000 + \
        b_hh_income_more_than_8000 * hh_income_14001_to_16000 + \
        b_hh_income_more_than_8000 * hh_income_more_than_16000 + \
        b_general_abo * general_abo + \
        b_regional_abo * regional_abo + \
        b_half_fare_abo * half_fare_abo + \
        b_car_avail * car_avail_always_or_on_demand + \
        b_regional_abo_na * regional_abo_na + \
        b_half_fare_abo_na * half_fare_abo_na + \
        b_car_avail_na * car_avail_na + \
        b_mobility_resource_na * mobility_resource_na + \
        b_mobility_resource_car_general_abo * mobility_resource_car_general_abo + \
        b_mobility_resource_car_half_fare_abo * mobility_resource_car_half_fare_abo + \
        b_mobility_resource_car * mobility_resource_car + \
        b_mobility_resource_general_abo * mobility_resource_general_abo + \
        b_mobility_resource_half_fare_abo * mobility_resource_half_fare_abo + \
        b_mobility_resource_none * mobility_resource_none + \
        b_mobility_resource_car_half_fare_regional_abo * mobility_resource_car_half_fare_regional_abo + \
        b_mobility_resource_car_regional_abo * mobility_resource_car_regional_abo + \
        b_mobility_resource_half_fare_regional_abo * mobility_resource_half_fare_regional_abo + \
        b_mobility_resource_regional_abo * mobility_resource_regional_abo
    U_no_telecommuting = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U,  # Yes or sometimes
         0: U_no_telecommuting}  # No

    av = {1: 1,
          0: 1}

    # Definition of the model. This is the contribution of each
    # observation to the log likelihood function.
    logprob = models.loglogit(V, av,  # All alternatives are supposed to be always available
                              telecommuting)  # Choice variable

    # Change the working directory, so that biogeme writes in the correct folder
    standard_directory = os.getcwd()
    os.chdir(output_directory)

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, logprob)
    biogeme.modelName = output_file_name

    # Estimate the parameters
    results = biogeme.estimate()

    # Get the results in LaTeX
    results.writeLaTeX()

    # Go back to the normal working directory
    os.chdir(standard_directory)
