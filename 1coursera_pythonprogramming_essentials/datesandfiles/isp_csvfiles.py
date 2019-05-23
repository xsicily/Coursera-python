"""
Project 3-Read and write CSV files using a dictionary of dictionaries.
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
    """
    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=separator,
                                    quoting=csv.QUOTE_NONNUMERIC, quotechar=quote)
        csv_writer.writeheader()
        csv_writer.writerows(table)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

