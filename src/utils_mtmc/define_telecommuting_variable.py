def define_telecommuting_variable(row):
    """ Defines a choice variable with value 1 if the person is allowed to telecommute
    (answer "yes" - 1 - or answer "sometimes" - 2) and does it at least 1% of the time """
    telecommuting = 0
    if ((row['telecommuting_is_possible'] == 1) or (row['telecommuting_is_possible'] == 2)) \
            and row['percentage_telecommuting'] > 0:
        telecommuting = 1
    return telecommuting
