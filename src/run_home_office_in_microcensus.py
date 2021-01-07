from estimate_choice_model_telecommuting import estimate_choice_model_telecommuting
from validate_model_with_microcensus_2015 import validate_model_with_microcensus_2015
from descriptive_statistics import descriptive_statistics
from calibrate_the_constant import calibrate_the_constant_by_simulating_on_microcensus
from calibrate_the_constant import calibrate_the_constant_by_simulating_on_synthetic_population
from validate_model_with_syn_pop_2017 import validate_model_with_syn_pop_2017
from apply_model_to_syn_pop_2050 import apply_model_to_syn_pop_2050


def run_home_office_in_microcensus():
    estimate_choice_model_telecommuting()
    validate_model_with_microcensus_2015()
    betas = calibrate_the_constant_by_simulating_on_microcensus()
    validate_model_with_syn_pop_2017(betas)
    descriptive_statistics()
    betas = calibrate_the_constant_by_simulating_on_synthetic_population(betas)
    apply_model_to_syn_pop_2050(betas)


if __name__ == '__main__':
    run_home_office_in_microcensus()
