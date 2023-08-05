import re


def get_numbers_from_string(num_str):
    if isinstance(num_str, int):
        return num_str
    if any(char.isdigit() for char in num_str):
        return int(re.sub('[^0-9]', '', num_str))
    return 0


def date_time_string_to_seconds(date_str):
    if isinstance(date_str, int):
        return date_str

    tup = tuple(map(int, date_str.split(':')))[::-1]
    parsed_search_duration = tup[0]
    iter_tup = iter(tup)
    next(iter_tup)
    for item in iter_tup:
        parsed_search_duration += item * 60
    return parsed_search_duration
