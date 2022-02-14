from estimate_choice_model_telecommuting import estimate_choice_model_telecommuting
from validate_model_with_microcensus_2015 import validate_model_with_microcensus_2015
from validate_model_with_microcensus_2020 import validate_model_with_microcensus_2020
from joint_estimate_2015_2020 import joint_estimate_2015_2020
from calibrate_the_constant import calibrate_the_constant_by_simulating_on_microcensus
from apply_model_to_examples import apply_model_to_examples
from validate_model_with_syn_pop_2017 import validate_model_with_syn_pop_2017
from descriptive_statistics import descriptive_statistics
from calibrate_the_constant import calibrate_the_constant_by_simulating_on_synthetic_population
from apply_model_to_syn_pop_2050 import apply_model_to_syn_pop_2050


def run_home_office_in_microcensus():
    ''' Estimation results, 2015 '''
    estimate_choice_model_telecommuting()
    ''' Internal validation: '''
    validate_model_with_microcensus_2015()
    ''' Testing temporal stability using the Mobility and Transport Microcensus 2020: '''
    validate_model_with_microcensus_2020()
    ''' Estimating model using the Mobility and Transport Microcensus 2015 & 2020 '''
    joint_estimate_2015_2020()
    ''' External validation using a synthetic population 2017 '''
    betas = calibrate_the_constant_by_simulating_on_microcensus('2015_2020')
    validate_model_with_syn_pop_2017(betas)
    # apply_model_to_examples(betas)
    # descriptive_statistics()
    # betas = calibrate_the_constant_by_simulating_on_synthetic_population(betas)
    # apply_model_to_syn_pop_2050(betas)


if __name__ == '__main__':
    run_home_office_in_microcensus()
