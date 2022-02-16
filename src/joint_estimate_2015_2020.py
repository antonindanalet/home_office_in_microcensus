from pathlib import Path
import pandas as pd
import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import Beta, DefineVariable
import os


def joint_estimate_2015_2020():
    merge_data_files()
    run_estimation_2015_2020()


def run_estimation_2015_2020():
    """
    :author: Antonin Danalet, based on the example '01logit.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    A binary logit model on the possibility to work from home at least some times."""

    # Read the data
    data_file_directory = Path('../data/output/data/estimation/2015_2020/')
    df = pd.read_csv(data_file_directory / 'persons.csv', sep=';')
    database = db.Database('persons', df)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    # Parameters to be estimated
    alternative_specific_constant = Beta('alternative_specific_constant', 0, None, None, 0)

    b_no_post_school_education = Beta('b_no_post_school_education', 0, None, None, 0)
    b_secondary_education = Beta('b_secondary_education', 0, None, None, 0)
    b_tertiary_education = Beta('b_tertiary_education', 0, None, None, 0)

    b_male_2020 = Beta('b_male_2020', 0, None, None, 1)

    b_single_household_2020 = Beta('b_single_household_2020', 0, None, None, 1)
    b_couple_without_children_2015 = Beta('b_couple_without_children_2015', 0, None, None, 0)
    b_couple_without_children_2020 = Beta('b_couple_without_children_2020', 0, None, None, 0)
    b_couple_with_children_2020 = Beta('b_couple_with_children_2020', 0, None, None, 1)
    b_single_parent_with_children_2020 = Beta('b_single_parent_with_children_2020', 0, None, None, 1)
    b_not_family_household_2020 = Beta('b_not_family_household_2020', 0, None, None, 1)

    b_public_transport_connection_quality_abc_home_2020 = Beta('b_public_transport_connection_quality_abc_home_2020',
                                                               0, None, None, 1)
    b_public_transport_connection_quality_na_home_2015 = Beta('b_public_transport_connection_quality_na_home_2015',
                                                              0, None, None, 0)
    b_public_transport_connection_quality_na_home_2020 = Beta('b_public_transport_connection_quality_na_home_2020',
                                                              0, None, None, 1)

    b_public_transport_connection_quality_abcd_work_2020 = Beta('b_public_transport_connection_quality_abcd_work_2020',
                                                                0, None, None, 1)

    b_urban_home_2020 = Beta('b_urban_home_2020', 0, None, None, 1)
    b_rural_home_2020 = Beta('b_rural_home_2020', 0, None, None, 1)
    b_intermediate_home_2020 = Beta('b_intermediate_home_2020', 0, None, None, 1)
    b_urban_work_2020 = Beta('b_urban_work_2020', 0, None, None, 1)
    b_rural_work_2020 = Beta('b_rural_work_2020', 0, None, None, 1)
    b_intermediate_work_2020 = Beta('b_intermediate_work_2020', 0, None, None, 0)

    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)
    b_home_work_distance_zero = Beta('b_home_work_distance_zero', 0, None, None, 0)
    b_home_work_distance_na = Beta('b_home_work_distance_na', 0, None, None, 0)

    b_business_sector_agriculture_2020 = Beta('b_business_sector_agriculture_2020', 0, None, None, 1)
    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale = Beta('b_business_sector_wholesale', 0, None, None, 0)
    b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 0)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 0)
    b_business_sector_services_fc_2020 = Beta('b_business_sector_services_fc_2020', 0, None, None, 1)
    b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 0)
    b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 0)
    b_business_sector_non_movers = Beta('b_business_sector_non_movers', 0, None, None, 0)
    b_executives = Beta('b_executives', 0, None, None, 0)
    b_german = Beta('b_german', 0, None, None, 0)
    b_hh_income_na = Beta('b_hh_income_na', 0, None, None, 0)
    b_hh_income_8000_or_less = Beta('b_hh_income_8000_or_less', 0, None, None, 0)

    b_owning_a_general_abo = Beta('b_owning_a_general_abo', 0, None, None, 0)
    b_regional_abo_2020 = Beta('b_regional_abo_2020', 0, None, None, 1)
    b_regional_abo_na_2020 = Beta('b_regional_abo_na_2020', 0, None, None, 1)
    b_half_fare_abo_2020 = Beta('b_half_fare_abo_2020', 0, None, None, 1)
    b_half_fare_abo_na_2020 = Beta('b_half_fare_abo_na_2020', 0, None, None, 1)
    b_car_avail_2020 = Beta('b_car_avail_2020', 0, None, None, 1)
    b_car_avail_na_2020 = Beta('b_car_avail_na_2020', 0, None, None, 1)

    b_mobility_resource_na = Beta('b_mobility_resource_na', 0, None, None, 0)
    b_mobility_resource_car_general_abo_2020 = Beta('b_mobility_resource_car_general_abo_2020', 0, None, None, 1)
    b_mobility_resource_car_half_fare_abo = Beta('b_mobility_resource_car_half_fare_abo', 0, None, None, 0)
    b_mobility_resource_car_2020 = Beta('b_mobility_resource_car_2020', 0, None, None, 1)
    b_mobility_resource_general_abo_no_car_2020 = Beta('b_mobility_resource_general_no_car_abo_2020', 0, None, None, 0)
    b_mobility_resource_half_fare_abo_2020 = Beta('b_mobility_resource_half_fare_abo_2020', 0, None, None, 1)
    b_mobility_resource_none_2020 = Beta('b_mobility_resource_none_2020', 0, None, None, 1)
    b_mobility_resource_car_half_fare_regional_abo_2020 = Beta('b_mobility_resource_car_half_fare_regional_abo_2020',
                                                               0, None, None, 1)
    b_mobility_resource_car_regional_abo_2020 = Beta('b_mobility_resource_car_regional_abo_2020', 0, None, None, 1)
    b_mobility_resource_half_fare_regional_abo_2020 = Beta('b_mobility_resource_half_fare_regional_abo_2020',
                                                           0, None, None, 1)
    b_mobility_resource_regional_abo_2020 = Beta('b_mobility_resource_regional_abo_2020', 0, None, None, 1)

    scale_2020 = Beta('scale_2020', 1, 0.001, None, 0)

    ''' Definition of new variables '''
    male_2020 = DefineVariable('male', (sex == 1) * (year == 2020), database)

    single_household_2020 = DefineVariable('single_household_2020', (hh_type == 10) * (year == 2020), database)
    couple_without_children_2015 = DefineVariable('couple_without_children_2015',
                                                  (hh_type == 210) * (year == 2015), database)
    couple_without_children_2020 = DefineVariable('couple_without_children_2020',
                                                  (hh_type == 210) * (year == 2020), database)
    couple_with_children_2020 = DefineVariable('couple_with_children_2020', (hh_type == 220) * (year == 2020), database)
    single_parent_with_children_2020 = DefineVariable('single_parent_with_children_2020',
                                                      (hh_type == 230) * (year == 2020), database)
    not_family_household_2020 = DefineVariable('not_family_household_2020', (hh_type == 30) * (year == 2020), database)

    public_transport_connection_quality_abc_home_2020 = \
        DefineVariable('public_transport_connection_quality_abc_home_2020',
                       ((public_transport_connection_quality_ARE_home == 1) +
                        (public_transport_connection_quality_ARE_home == 2) +
                        (public_transport_connection_quality_ARE_home == 3)) * (year == 2020), database)
    public_transport_connection_quality_na_home_2015 = \
        DefineVariable('public_transport_connection_quality_NA_home_2015',
                       (public_transport_connection_quality_ARE_home == 5) * (year == 2015), database)
    public_transport_connection_quality_na_home_2020 = \
        DefineVariable('public_transport_connection_quality_NA_home_2020',
                       (public_transport_connection_quality_ARE_home == 5) * (year == 2020), database)

    public_transport_connection_quality_abcd_work_2020 = \
        DefineVariable('public_transport_connection_quality_abc_work_2020',
                       ((public_transport_connection_quality_ARE_work == 1) +
                        (public_transport_connection_quality_ARE_work == 2) +
                        (public_transport_connection_quality_ARE_work == 3) +
                        (public_transport_connection_quality_ARE_work == 4)) * (year == 2020), database)

    urban_home_2020 = DefineVariable('urban_home_2020', (urban_typology_home == 1) * (year == 2020), database)
    rural_home_2020 = DefineVariable('rural_home_2020', (urban_typology_home == 3) * (year == 2020), database)
    intermediate_home_2020 = DefineVariable('intermediate_home_2020', (urban_typology_home == 2) * (year == 2020),
                                            database)
    urban_work_2020 = DefineVariable('urban_work_2020', (urban_typology_work == 1) * (year == 2020), database)
    rural_work_2020 = DefineVariable('rural_work_2020', (urban_typology_work == 3) * (year == 2020), database)
    intermediate_work_2020 = DefineVariable('intermediate_work_2020', (urban_typology_work == 2) * (year == 2020),
                                            database)

    home_work_distance = DefineVariable('home_work_distance',
                                        home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0,
                                        database)
    home_work_distance_zero = DefineVariable('home_work_distance_zero', home_work_crow_fly_distance == 0.0, database)
    home_work_distance_na = DefineVariable('home_work_distance_na', home_work_crow_fly_distance == -999, database)

    executives = DefineVariable('executives', work_position == 1, database)

    german = DefineVariable('german', language == 1, database)

    hh_income_na = DefineVariable('hh_income_na', hh_income < 0, database)
    hh_income_8000_or_less = DefineVariable('hh_income_8000_or_less',
                                            (hh_income == 1) + (hh_income == 2) + (hh_income == 3) + (hh_income == 4),
                                            database)

    owning_a_general_abo = DefineVariable('owning_a_general_abo', GA_ticket == 1, database)
    regional_abo_2020 = DefineVariable('regional_abo_2020', (Verbund_Abo == 1) * (year == 2020), database)
    half_fare_abo_2020 = DefineVariable('half_fare_abo_2020', (halbtax_ticket == 1) * (year == 2020), database)
    car_avail_always_or_on_demand_2020 = DefineVariable('car_avail_always_or_on_demand_2020',
                                                        ((car_avail == 1) + (car_avail == 2)) * (year == 2020),
                                                        database)
    regional_abo_na_2020 = DefineVariable('regional_abo_na_2020', (Verbund_Abo < 0) * (year == 2020), database)
    half_fare_abo_na_2020 = DefineVariable('half_fare_abo_na_2020', (halbtax_ticket < 0) * (year == 2020), database)
    car_avail_na_2020 = DefineVariable('car_avail_na_2020', (car_avail < 0) * (year == 2020), database)

    mobility_resource_na = DefineVariable('mobility_resource_na', mobility_resources == -98, database)
    mobility_resource_car_general_abo_2020 = DefineVariable('mobility_resource_car_general_abo_2020',
                                                            (mobility_resources == 1) * (year == 2020), database)
    mobility_resource_car_half_fare_abo = DefineVariable('mobility_resource_car_half_fare_abo', mobility_resources == 2,
                                                         database)
    mobility_resource_car_2020 = DefineVariable('mobility_resource_car_2020',
                                                (mobility_resources == 3) * (year == 2020), database)
    mobility_resource_general_abo_no_car_2020 = DefineVariable('mobility_resource_general_abo_no_car_2020',
                                                        (mobility_resources == 4) * (year == 2020), database)
    mobility_resource_half_fare_abo_2020 = DefineVariable('mobility_resource_half_fare_abo_2020',
                                                          (mobility_resources == 5) * (year == 2020), database)
    mobility_resource_none_2020 = DefineVariable('mobility_resource_none_2020',
                                                 (mobility_resources == 6) * (year == 2020), database)
    mobility_resource_car_half_fare_regional_abo_2020 = \
        DefineVariable('mobility_resource_car_half_fare_regional_abo_2020',
                       (mobility_resources == 20) * (year == 2020), database)
    mobility_resource_car_regional_abo_2020 = DefineVariable('mobility_resource_car_regional_abo_2020',
                                                             (mobility_resources == 30) * (year == 2020), database)
    mobility_resource_half_fare_regional_abo_2020 = DefineVariable('mobility_resource_half_fare_regional_abo_2020',
                                                                   (mobility_resources == 50) * (year == 2020),
                                                                   database)
    mobility_resource_regional_abo_2020 = DefineVariable('mobility_resource_regional_abo_2020',
                                                         (mobility_resources == 60) * (year == 2020), database)

    business_sector_agriculture_2020 = DefineVariable('business_sector_agriculture_2020',
                                                      business_sector_agriculture * (year == 2020), database)
    business_sector_services_fc_2020 = DefineVariable('business_sector_services_fc_2020',
                                                      business_sector_services_fc * (year == 2020), database)

    #  Utility
    U = alternative_specific_constant + \
        b_executives * executives + \
        b_no_post_school_education * no_post_school_educ + \
        b_secondary_education * secondary_education + \
        b_tertiary_education * tertiary_education + \
        b_couple_without_children_2015 * couple_without_children_2015 + \
        b_couple_without_children_2020 * couple_without_children_2020 + \
        b_public_transport_connection_quality_na_home_2015 * public_transport_connection_quality_na_home_2015 + \
        b_public_transport_connection_quality_na_home_2020 * public_transport_connection_quality_na_home_2020 + \
        b_home_work_distance * home_work_distance + \
        b_home_work_distance_zero * home_work_distance_zero + \
        b_home_work_distance_na * home_work_distance_na + \
        models.piecewiseFormula(age, [15, 19, 31, 79, 85]) + \
        b_business_sector_retail * business_sector_retail + \
        b_business_sector_gastronomy * business_sector_gastronomy + \
        b_business_sector_finance * business_sector_finance + \
        b_business_sector_production * business_sector_production + \
        b_business_sector_wholesale * business_sector_wholesale + \
        b_business_sector_other_services * business_sector_other_services + \
        b_business_sector_others * business_sector_others + \
        b_business_sector_non_movers * business_sector_non_movers + \
        b_german * german + \
        models.piecewiseFormula(work_percentage, [0, 90, 101]) + \
        b_hh_income_na * hh_income_na + \
        b_hh_income_8000_or_less * hh_income_8000_or_less + \
        b_owning_a_general_abo * owning_a_general_abo + \
        b_mobility_resource_na * mobility_resource_na + \
        b_mobility_resource_car_half_fare_abo * mobility_resource_car_half_fare_abo + \
        b_male_2020 * male_2020 + \
        b_single_household_2020 * single_household_2020 + \
        b_couple_with_children_2020 * couple_with_children_2020 + \
        b_single_parent_with_children_2020 * single_parent_with_children_2020 + \
        b_not_family_household_2020 * not_family_household_2020 + \
        b_public_transport_connection_quality_abc_home_2020 * public_transport_connection_quality_abc_home_2020 + \
        b_public_transport_connection_quality_abcd_work_2020 * public_transport_connection_quality_abcd_work_2020 + \
        b_urban_home_2020 * urban_home_2020 + \
        b_rural_home_2020 * rural_home_2020 + \
        b_intermediate_home_2020 * intermediate_home_2020 + \
        b_urban_work_2020 * urban_work_2020 + \
        b_rural_work_2020 * rural_work_2020 + \
        b_intermediate_work_2020 * intermediate_work_2020 + \
        b_business_sector_agriculture_2020 * business_sector_agriculture_2020 + \
        b_business_sector_services_fc_2020 * business_sector_services_fc_2020 + \
        b_regional_abo_2020 * regional_abo_2020 + \
        b_regional_abo_na_2020 * regional_abo_na_2020 + \
        b_half_fare_abo_2020 * half_fare_abo_2020 + \
        b_half_fare_abo_na_2020 * half_fare_abo_na_2020 + \
        b_car_avail_2020 * car_avail_always_or_on_demand_2020 + \
        b_car_avail_na_2020 * car_avail_na_2020 + \
        b_mobility_resource_car_general_abo_2020 * mobility_resource_car_general_abo_2020 + \
        b_mobility_resource_car_2020 * mobility_resource_car_2020 + \
        b_mobility_resource_general_abo_no_car_2020 * mobility_resource_general_abo_no_car_2020 + \
        b_mobility_resource_half_fare_abo_2020 * mobility_resource_half_fare_abo_2020 + \
        b_mobility_resource_none_2020 * mobility_resource_none_2020 + \
        b_mobility_resource_car_half_fare_regional_abo_2020 * mobility_resource_car_half_fare_regional_abo_2020 + \
        b_mobility_resource_car_regional_abo_2020 * mobility_resource_car_regional_abo_2020 + \
        b_mobility_resource_half_fare_regional_abo_2020 * mobility_resource_half_fare_regional_abo_2020 + \
        b_mobility_resource_regional_abo_2020 * mobility_resource_regional_abo_2020
    U_no_telecommuting = 0

    # Scale associated with 2020 is estimated
    scale = (year == 2015) + (year == 2020) * scale_2020

    # Associate utility functions with the numbering of alternatives
    V = {1: scale * U,  # Yes or sometimes
         0: U_no_telecommuting}  # No

    av = {1: 1,
          0: 1}

    # Definition of the model. This is the contribution of each
    # observation to the log likelihood function.
    logprob = models.loglogit(V, av,  # All alternatives are supposed to be always available
                              telecommuting)  # Choice variable

    # Change the working directory, so that biogeme writes in the correct folder
    standard_directory = os.getcwd()
    output_directory = '../data/output/models/estimation/2015_2020/'
    os.chdir(output_directory)

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, logprob)
    output_file_name = 'logit_telecommuting_2015_2020'
    biogeme.modelName = output_file_name

    # Estimate the parameters
    results = biogeme.estimate()

    # Get the results in LaTeX
    results.writeLaTeX()

    # Go back to the normal working directory
    os.chdir(standard_directory)


def merge_data_files():
    # Read 2020 data
    data_directory_2020 = Path('../data/output/data/validation_with_MTMC_2020/')
    data_file_name_2020 = 'persons.csv'
    with open(data_directory_2020 / data_file_name_2020, 'r') as file_2020:
        df_2020 = pd.read_csv(file_2020, sep=';')
    df_2020['year'] = 2020
    # Read 2015 data
    data_directory_2015 = Path('../data/output/data/estimation/2015/')
    data_file_name_2015 = 'persons.csv'
    with open(data_directory_2015 / data_file_name_2015, 'r') as file_2015:
        df_2015 = pd.read_csv(file_2015, sep=';')
    df_2015['year'] = 2015
    # Merge 2015 and 2020
    df_2015_2020 = pd.concat([df_2015, df_2020], ignore_index=True)
    output_directory = Path('../data/output/data/estimation/2015_2020/')
    df_2015_2020.to_csv(output_directory / 'persons.csv', sep=';', index=False)
