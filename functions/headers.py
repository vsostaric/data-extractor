def get_headers(datafile):
    headers = tuple(__get_headers(datafile).split(","))
    first_line = datafile.take(2)[1].split(",")
    header_types = dict((headers[i], __get_header_type(i, first_line)) for i, x in enumerate(headers))

    return headers, header_types


def __get_headers(datafile):
    return datafile.take(1)[0]


def __get_header_type(header_index, first_line):
    return 'number' if __is_number(first_line[header_index]) else 'string'


def __is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
