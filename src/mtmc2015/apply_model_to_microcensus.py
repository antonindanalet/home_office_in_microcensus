import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta, DefineVariable
import biogeme.results as res
import os


def apply_model_to_microcensus(data_file_directory_for_simulation, data_file_name_for_simulation,
                               output_directory_for_simulation, output_file_name,
                               path_to_estimated_betas, estimated_betas_name, betas=None):
    """
    :author: Antonin Danalet, based on the example '01logit_simul.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    Simulation with a binary logit model. Two alternatives: work from home at least some times, or not."""

    # Read the data
    df_persons = pd.read_csv(data_file_directory_for_simulation / data_file_name_for_simulation, ';')
    database = db.Database('persons', df_persons)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    # Parameters to be estimated
    alternative_specific_constant = Beta('alternative_specific_constant', 0, None, None, 0)

    b_no_post_school_education = Beta('b_no_post_school_education', 0, None, None, 0)
    b_secondary_education = Beta('b_secondary_education', 0, None, None, 0)
    b_tertiary_education = Beta('b_tertiary_education', 0, None, None, 0)
    b_university = Beta('b_university', 0, None, None, 1)

    b_male = Beta('b_male', 0, None, None, 0)

    b_single_household = Beta('b_single_household', 0, None, None, 1)
    b_couple_without_children = Beta('b_couple_without_children', 0, None, None, 1)
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
    b_rural_work = Beta('b_rural_work', 0, None, None, 0)
    b_intermediate_work = Beta('b_intermediate_work', 0, None, None, 1)

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
    b_hh_income_na = Beta('B_hh_income_na', 0, None, None, 1)
    b_hh_income_8000_or_less = Beta('b_hh_income_8000_or_less', 0, None, None, 0)
    b_hh_income_more_than_8000 = Beta('b_hh_income_more_than_8000', 0, None, None, 1)

    # Definition of new variables
    no_post_school_educ = ((highest_educ == 1) | (highest_educ == 2) | (highest_educ == 3) | (highest_educ == 4))
    secondary_education = ((highest_educ == 5) | (highest_educ == 6) | (highest_educ == 7) | (highest_educ == 8) |
                           (highest_educ == 9) | (highest_educ == 10) | (highest_educ == 11) | (highest_educ == 12))
    tertiary_education = ((highest_educ == 13) | (highest_educ == 14) | (highest_educ == 15) | (highest_educ == 16))
    university = (highest_educ == 17) * 10

    male = (sex == 1)

    single_household = (hh_type == 10)
    couple_without_children = (hh_type == 210)
    couple_with_children = (hh_type == 220)
    single_parent_with_children = (hh_type == 230)
    not_family_household = (hh_type == 30)

    public_transport_connection_quality_ARE_A_home = (public_transport_connection_quality_ARE_home == 1)
    public_transport_connection_quality_ARE_B_home = (public_transport_connection_quality_ARE_home == 2)
    public_transport_connection_quality_ARE_C_home = (public_transport_connection_quality_ARE_home == 3)
    public_transport_connection_quality_ARE_D_home = (public_transport_connection_quality_ARE_home == 4)
    public_transport_connection_quality_ARE_NA_home = (public_transport_connection_quality_ARE_home == 5)

    public_transport_connection_quality_ARE_A_work = (public_transport_connection_quality_ARE_work == 1)
    public_transport_connection_quality_ARE_B_work = (public_transport_connection_quality_ARE_work == 2)
    public_transport_connection_quality_ARE_C_work = (public_transport_connection_quality_ARE_work == 3)
    public_transport_connection_quality_ARE_D_work = (public_transport_connection_quality_ARE_work == 4)
    public_transport_connection_quality_ARE_NA_work = (public_transport_connection_quality_ARE_work == 5)

    urban_home = (urban_typology_home == 1)
    rural_home = (urban_typology_work == 3)
    intermediate_home = (urban_typology_home == 2)

    urban_work = (urban_typology_work == 1)
    rural_work = (urban_typology_work == 3)
    intermediate_work = (urban_typology_work == 2)

    home_work_distance = (home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0)

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

    employees = work_position == 2
    executives = work_position == 1

    german = language == 1

    nationality_switzerland = nation == 8100
    nationality_germany_austria_lichtenstein = (nation == 8207) + (nation == 8229) + (nation == 8222)
    nationality_italy_vatican = (nation == 8218) + (nation == 8241)
    nationality_france_monaco_san_marino = (nation == 8212) + (nation == 8226) + (nation == 8233)
    nationality_northwestern_europe = (nation == 8204) + (nation == 8223) + (nation == 8227) + (nation == 8206) + \
                                      (nation == 8211) + (nation == 8215) + (nation == 8216) + (nation == 8217) + \
                                      (nation == 8228) + (nation == 8234)
    nationality_south_west_europe = (nation == 8231) + (nation == 8236) + (nation == 8202)
    nationality_southeast_europe = (nation == 8224) + (nation == 8201) + (nation == 8214) + (nation == 8256) + \
                                   (nation == 8250) + (nation == 8251) + (nation == 8252) + (nation == 8255) + \
                                   (nation == 8205) + (nation == 8239) + (nation == 8242) + (nation == 8248) + \
                                   (nation == 8254)
    nationality_eastern_europe = (nation == 8230) + (nation == 8232) + (nation == 8240) + (nation == 8243) + \
                                 (nation == 8244) + (nation == 8263) + (nation == 8265) + (nation == 8266) + \
                                 (nation == 8260) + (nation == 8261) + (nation == 8262)

    # several_part_time_jobs = full_part_time_job == 3
    work_percentage = DefineVariable('work_percentage',
                                     (full_part_time_job == 1) * 100 +
                                     percentage_first_part_time_job * (percentage_first_part_time_job > 0) +
                                     percentage_second_part_time_job * (percentage_second_part_time_job > 0),
                                     database)

    hh_income_na = hh_income == -98
    hh_income_less_than_2000 = hh_income == 1
    hh_income_2000_to_4000 = hh_income == 2
    hh_income_4001_to_6000 = hh_income == 3
    hh_income_6001_to_8000 = hh_income == 4
    hh_income_8001_to_10000 = hh_income == 5
    hh_income_10001_to_12000 = hh_income == 6
    hh_income_12001_to_14000 = hh_income == 7
    hh_income_14001_to_16000 = hh_income == 8
    hh_income_more_than_16000 = hh_income == 9

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
        b_hh_income_more_than_8000 * hh_income_more_than_16000
    U_No_telecommuting = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U,  # Yes or sometimes
         0: U_No_telecommuting}  # No

    av = {1: 1,
          0: 1}

    # The choice model is a logit, with availability conditions
    prob_telecommuting = models.logit(V, av, 1)
    prob_no_telecommuting = models.logit(V, av, 0)

    simulate = {'Prob. telecommuting': prob_telecommuting,
                'Prob. no telecommuting': prob_no_telecommuting}

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = 'logit_telecommuting_simul'
    # Get the betas from the estimation
    if betas is None:
        if os.path.isfile(path_to_estimated_betas / (estimated_betas_name + '~00.pickle')):
            print('WARNING: There are several model outputs!')
        results = res.bioResults(pickleFile=path_to_estimated_betas / (estimated_betas_name + '.pickle'))
        betas = results.getBetaValues()

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    #standard_directory = os.getcwd()
    #os.chdir(output_directory_for_simulation)

    results = biogeme.simulate(theBetaValues=betas)
    #print(results.describe())
    df_persons = pd.concat([df_persons, results], axis=1)

    # Go back to the normal working directory
    #os.chdir(standard_directory)

    ''' Save the file '''
    df_persons.to_csv(output_directory_for_simulation / output_file_name, sep=',', index=False)
