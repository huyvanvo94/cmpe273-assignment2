import csv

def read_csv(filename):
    csv_file = open(filename, mode='r')
    csv_reader = csv.DictReader(csv_file)
    return csv_reader

def pretty_csv_row(csv_reader, csv_row):
    keys = csv_reader.fieldnames

    s = ''

    for idx in range(len(keys) - 1):
        s += csv_row[keys[idx]] + ','

    s += csv_row[keys[len(keys) - 1]]
    return s