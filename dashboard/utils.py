def normalize_days(number_of_days):

    if number_of_days == 'less than a day':
        return 0.5

    if number_of_days == '':
        return 0

    return int(number_of_days[:-1]) if isinstance(number_of_days, str) else 0
