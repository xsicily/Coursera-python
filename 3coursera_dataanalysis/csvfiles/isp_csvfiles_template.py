"""
Project for Week 3 of "Python Data Analysis".
Read and write CSV files using a dictionary of dictionaries.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv


def read_csv_fieldnames(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      A list of strings corresponding to the field names in
      the given CSV file.
    >>> filename1 = "C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w3/isp_csv_files/table1.csv"
    >>> read_csv_fieldnames(filename1, ',', '')
    ['Field1', 'Field2', 'Field3', 'Field4']
    >>> filename2 = "C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w3/isp_csv_files/table2.csv"
    >>> read_csv_fieldnames(filename2, ',', '"')
    ['Field1', 'Field2', 'Field3', 'Field4']
    >>> filename3 = "C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w3/isp_csv_files/table3.csv"
    >>> read_csv_fieldnames(filename3, ',', "'")
    ['Field1', 'Field2', 'Field3', 'Field4']
    """

    with open(filename, 'rt', newline='') as datafile:
        if quote:
            reader = csv.DictReader(datafile, skipinitialspace=False, delimiter=separator,
                                    quoting=csv.QUOTE_ALL, quotechar=quote)
        else:
            reader = csv.DictReader(datafile, skipinitialspace=True, delimiter=separator,
                                    quoting=csv.QUOTE_NONE)
        return reader.fieldnames


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    >>> filename = "C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w3/isp_csv_files/table4.csv"
    >>> read_csv_as_list_dict(filename, ',', "'")
    [OrderedDict([('"Field', '"Field'), (' 1"', ' 1"'), ('Field 2', 'Field 2'), ('"Field 3"', '"Field 3"'), ('Field, 4', 'Field, 4')]), OrderedDict([('"Field', 'abc'), (' 1"', '"d'), ('Field 2', 'ef"'), ('"Field 3"', 'g,hi'), ('Field, 4', '"jkl"')]), OrderedDict([('"Field', 'abc'), (' 1"', '"def"'), ('Field 2', 'ghi,'), ('"Field 3"', '"'), ('Field, 4', 'jkl"')]), OrderedDict([('"Field', 'a,b;c'), (' 1"', '"'), ('Field 2', 'def"'), ('"Field 3"', 'ghi'), ('Field, 4', '"jk;l"')])]
    """
    with open(filename, 'rt') as datafile:
        reader = csv.DictReader(datafile, skipinitialspace=False, delimiter=separator,
                                quoting=csv.QUOTE_ALL, quotechar=quote)
        list_dict = []
        for row in reader:
            list_dict.append(row)
    return list_dict


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    >>> filename = "C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w3/isp_csv_files/table4.csv"
    >>> read_csv_as_nested_dict(filename, 'Field 3', ',', '"')
    {'Field 3': OrderedDict([('Field, 1', 'Field, 1'), ("'Field 2'", "'Field 2'"), ('Field 3', 'Field 3'), ("'Field", "'Field"), (" 4'", " 4'")]), "'g": OrderedDict([('Field, 1', "'abc'"), ("'Field 2'", 'd,ef'), ('Field 3', "'g"), ("'Field", "hi'"), (" 4'", 'jkl')]), "'ghi": OrderedDict([('Field, 1', "'abc'"), ("'Field 2'", 'def'), ('Field 3', "'ghi"), ("'Field", "'"), (" 4'", ',jkl')]), ',def': OrderedDict([('Field, 1', "'a"), ("'Field 2'", "b;c'"), ('Field 3', ',def'), ("'Field", "'ghi'"), (" 4'", 'jk;l')])}
    >>> read_csv_as_nested_dict(filename, ' 1"', ',', "'")
    {' 1"': OrderedDict([('"Field', '"Field'), (' 1"', ' 1"'), ('Field 2', 'Field 2'), ('"Field 3"', '"Field 3"'), ('Field, 4', 'Field, 4')]), '"d': OrderedDict([('"Field', 'abc'), (' 1"', '"d'), ('Field 2', 'ef"'), ('"Field 3"', 'g,hi'), ('Field, 4', '"jkl"')]), '"def"': OrderedDict([('"Field', 'abc'), (' 1"', '"def"'), ('Field 2', 'ghi,'), ('"Field 3"', '"'), ('Field, 4', 'jkl"')]), '"': OrderedDict([('"Field', 'a,b;c'), (' 1"', '"'), ('Field 2', 'def"'), ('"Field 3"', 'ghi'), ('Field, 4', '"jk;l"')])}
    """
    with open(filename, 'rt') as datafile:
        reader = csv.DictReader(datafile, skipinitialspace=False, delimiter=separator,
                                quoting=csv.QUOTE_ALL, quotechar=quote)
        nested_dict = {}
        for row in reader:
            nested_dict[row[keyfield]] = row
    return nested_dict


def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    """
    Inputs:
      filename   - name of CSV file
      table      - list of dictionaries containing the table to write
      fieldnames - list of strings corresponding to the field names in order
      separator  - character that separates fields
      quote      - character used to optionally quote fields
    Output:
      Writes the table to a CSV file with the name filename, using the
      given fieldnames.  The CSV file should use the given separator and
      quote characters.  All non-numeric fields will be quoted.
    >>> write_csv_from_list_dict('output1.csv', [{'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14}, {'a': 20, 'b': 21, 'c': 22, 'd': 23, 'e': 24}, {'a': 30, 'b': 31, 'c': 32, 'd': 33, 'e': 34}, {'a': 40, 'b': 41, 'c': 42, 'd': 43, 'e': 44}], ['a', 'b', 'c', 'd', 'e'], ',', '"')
    "a","b","c","d","e"
    10,11,12,13,14
    20,21,22,23,24
    30,31,32,33,34
    40,41,42,43,44
    """
    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=separator,
                                    quoting=csv.QUOTE_NONNUMERIC, quotechar=quote)
        csv_writer.writeheader()
        csv_writer.writerows(table)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

