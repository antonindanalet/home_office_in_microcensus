def define_home_office_variable(row):
    """ Defines a choice variable with value 1 if the person is allowed to do home office
    (answer "yes" - 1 - or answer "sometimes" - 2) and does it at least 1% of the time """
    home_office = 0
    if ((row['home_office_is_possible'] == 1) or (row['home_office_is_possible'] == 2)) \
            and row['percentage_home_office'] > 0:
        home_office = 1
    return home_office
