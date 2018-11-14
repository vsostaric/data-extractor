from extractor.filter.number import functions as number_functions
from extractor.filter.string import functions as string_functions


def get_filter_method(header_type, condition):
    if header_type == 'number':
        return __get_number_filter_method(condition)
    elif header_type == 'string':
        return __get_string_filter_method(condition)


def __get_number_filter_method(condition):
    if condition == '<':
        return number_functions.number_lesser
    elif condition == '<=':
        return number_functions.number_lesser_or_equal
    elif condition == '>':
        return number_functions.number_greater
    elif condition == '>=':
        return number_functions.number_greater_or_equal
    elif condition == '=':
        return number_functions.number_equal


def __get_string_filter_method(condition):
    if condition == 'contains':
        return string_functions.string_contains
    elif condition == 'equals':
        return string_functions.string_equals
