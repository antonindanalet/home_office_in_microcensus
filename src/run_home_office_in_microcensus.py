from estimate_choice_model_home_office import estimate_choice_model_home_office
from validate_choice_model_home_office import validate_choice_model_home_office
from descriptive_statistics import descriptive_statistics
from calibrate_the_constant import calibrate_the_constant_by_simulating_on_microcensus
from calibrate_the_constant import calibrate_the_constant_by_simulating_on_synthetic_population
from apply_model_to_synthetic_population import validation_with_syn_pop
from applying_model_to_syn_pop_2050 import applying_model_to_syn_pop_2050


def run_home_office_in_microcensus():
    estimate_choice_model_home_office()
    validate_choice_model_home_office()
    descriptive_statistics()
    betas = calibrate_the_constant_by_simulating_on_microcensus()
    validation_with_syn_pop(betas)
    betas = calibrate_the_constant_by_simulating_on_synthetic_population(betas)
    applying_model_to_syn_pop_2050(betas)


if __name__ == '__main__':
    run_home_office_in_microcensus()
