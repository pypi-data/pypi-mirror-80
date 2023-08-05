import re


def GetNumbersFromString(str):
    if isinstance(str, int):
        return str
    return int(re.sub('[^0-9]', '', str))


def DateTimeStringToSeconds(str):
    if isinstance(str, int):
        return str

    tup = tuple(map(int, str.split(':')))[::-1]
    parsed_search_duration = tup[0]
    iter_tup = iter(tup)
    next(iter_tup)
    for item in iter_tup:
        parsed_search_duration += item * 60
    return parsed_search_duration
