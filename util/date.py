import re
from datetime import datetime
from typing import Union

__weekdays_int_to_str = {0: 'MO', 1: 'TU', 2: 'WE', 3: 'TH', 4: 'FR', 5: 'SA', 6: 'SU'}
__weekdays_str_to_int = {'MO': 0, 'TU': 1, 'WE': 2, 'TH': 3, 'FR': 4, 'SA': 5, 'SU': 6}
__workdays = ['MO', 'TU', 'WE', 'TH', 'FR']
__workdays_int = range(0, 5)
__weekend = ['SA', 'SU']
__weekend_int = [5, 6]


def weekday(date: Union[datetime, int]) -> str:
    if isinstance(date, int):
        return __weekdays_int_to_str.get(date)
    day = date.weekday()
    return __weekdays_int_to_str.get(day)


def convert_range(days: str) -> [str]:
    result: [str] = []
    pattern = re.compile('^(MO|TU|WE|TH|FR|SA|SU)-(MO|TU|WE|TH|FR|SA|SU)$')
    if pattern.match(days):
        split = days.split('-')
        first = __weekdays_str_to_int.get(split[0])
        second = __weekdays_str_to_int.get(split[1])
        if first > second:
            second = second + 7
        days_int = range(first, second + 1)
        for day in days_int:
            result.append(__weekdays_int_to_str.get(day % 7))
    return result


def is_workingday(day: Union[str, int, datetime]) -> bool:
    return __is_weekday(day, __workdays, __workdays_int)


def is_weekend(day: Union[str, int, datetime]) -> bool:
    return __is_weekday(day, __weekend, __weekend_int)


def __is_weekday(day: Union[str, int, datetime], strs: [str], ints: [int]) -> bool:
    if isinstance(day, str):
        return day in strs
    if isinstance(day, int):
        return day in ints
    if isinstance(day, datetime):
        return day.weekday() in ints
    return False


def parse_config(patterns: [str]) -> [str]:
    result: set = set()
    day = re.compile('^(MO|TU|WE|TH|FR|SA|SU)$')
    day_range = re.compile('^(MO|TU|WE|TH|FR|SA|SU)-(MO|TU|WE|TH|FR|SA|SU)$')
    for pattern in patterns:
        if day.match(pattern):
            result.add(pattern)
        if day_range.match(pattern):
            days = convert_range(pattern)
            for d in days:
                result.add(d)
        if 'WORKINGDAY' == pattern:
            for workday in __workdays:
                result.add(workday)
        if 'WEEKEND' == pattern:
            for weekend in __weekend:
                result.add(weekend)
    return list(result)
