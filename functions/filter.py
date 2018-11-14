from functions.headers import get_headers


def filter_csv_rows(datafile, field, value):
    header = get_headers(datafile)
    return datafile \
        .filter(lambda line: line != header) \
        .map(lambda line: line.split(",")) \
        .filter(lambda line: len(line) > field) \
        .filter(lambda line: line[field] == value)
