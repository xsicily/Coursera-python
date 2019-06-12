"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal
import math


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    with open(filename, 'rt', newline='') as datafile:
        reader = csv.DictReader(datafile, skipinitialspace=False, delimiter=separator,
                                quoting=csv.QUOTE_ALL, quotechar=quote)
        nested_dict = {}
        for row in reader:
            nested_dict[row[keyfield]] = row
    return nested_dict


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    >>> codeinfo = {"codefile": "C:/Users/Sicil/PycharmProjects/pythonbasic/4coursera_datavisualization/w4/isp_code_csv_files/code1.csv", 'separator': ',', 'plot_codes': 'Code1', 'data_codes': 'Code2', 'quote': "'"}
    >>> build_country_code_converter(codeinfo)
    {'Ab': 'Cd', 'Gh': 'Ij', 'MN': 'OP', 'ST': 'UV'}
    """
    plot_codes_nested_dict = read_csv_as_nested_dict(codeinfo["codefile"], codeinfo["plot_codes"],
                                                     codeinfo["separator"], codeinfo["quote"])
    country_code_converter_dict = {}

    for outer_key, outer_value in plot_codes_nested_dict.items():
        country_code_converter_dict[outer_key] = outer_value[codeinfo['data_codes']]

    return country_code_converter_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    >>> codeinfo = {"codefile": "C:/Users/Sicil/PycharmProjects/pythonbasic/4coursera_datavisualization/w4/isp_code_csv_files/code4.csv", 'plot_codes': 'ISO3166-1-Alpha-2', 'data_codes': 'ISO3166-1-Alpha-3', 'separator': ',', 'quote': '"'}
    >>> plot_countries = {'pr': 'Puerto Rico', 'us': 'United States', 'no': 'Norway'}
    >>> gdp_countries = {'USA': {'Country Code': 'USA', 'Country Name': 'United States'}, 'NOR': {'Country Code': 'NOR', 'Country Name': 'Norway'}, 'PRI': {'Country Code': 'PRI', 'Country Name': 'Puerto Rico'}}
    >>> reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)
    ({'pr': 'PRI', 'us': 'USA', 'no': 'NOR'}, set())
    >>> codeinfo = {'codefile': "C:/Users/Sicil/PycharmProjects/pythonbasic/4coursera_datavisualization/w4/isp_code_csv_files/code2.csv", 'quote': "'", 'separator': ',', 'data_codes': 'Cd3', 'plot_codes': 'Cd2'}
    >>> plot_countries = {'C2': 'c2', 'C5': 'c5', 'C4': 'c4', 'C3': 'c3', 'C1': 'c1'}
    >>> gdp_countries = {'ABC': {'Country Name': 'Country1', 'Code': 'ABC'}, 'GHI': {'Country Name': 'Country2', 'Code': 'GHI'}}
    >>> reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)
    ({'C3': 'GHI', 'C1': 'ABC'}, {'C5', 'C2', 'C4'})
    >>> codeinfo = {'codefile': "C:/Users/Sicil/PycharmProjects/pythonbasic/4coursera_datavisualization/w4/isp_code_csv_files/code4.csv", 'separator': ',', 'quote': '"', 'plot_codes': 'ISO3166-1-Alpha-2', 'data_codes': 'ISO3166-1-Alpha-3'}
    >>> plot_countries = {'jp': 'Japan', 'ru': 'Russian Federation', 'cn': 'China'}
    >>> gdp_countries = {}
    >>> reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)
    ({}, {'jp', 'ru', 'cn'})
    """
    plot_code_dict = {}
    code_missing_set = set()

    code_converter = build_country_code_converter(codeinfo)

    gdp_code_lower = {}
    for gdp_country_code in gdp_countries.keys():
        gdp_code_lower[gdp_country_code.lower()] = gdp_country_code

    converter_code_lower = {}
    for country_code, bank_code in code_converter.items():
        converter_code_lower[country_code.lower()] = bank_code.lower()

    for code in plot_countries.keys():
        for country_code, _ in converter_code_lower.items():
            if code.lower() == country_code:
                if converter_code_lower[country_code] in gdp_code_lower.keys():
                    plot_code_dict[code] = gdp_code_lower[converter_code_lower[country_code]]
                elif converter_code_lower[country_code] not in gdp_code_lower.keys():
                    code_missing_set.add(code)
            elif code.lower() not in converter_code_lower.keys():
                code_missing_set.add(code)
    return plot_code_dict, code_missing_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    >>> gdpinfo = {'gdpfile': "C:/Users/Sicil/PycharmProjects/pythonbasic/4coursera_datavisualization/w4/isp_gdp_csv_files/gdptable2.csv", 'separator': ',', 'quote': '"', 'min_year': 1953, 'max_year': 1958, 'country_name': 'Country Name', 'country_code': 'Code'}
    >>> codeinfo = {'codefile': "C:/Users/Sicil/PycharmProjects/pythonbasic/4coursera_datavisualization/w4/isp_code_csv_files/code2.csv", 'separator': ',', 'quote': "'", 'plot_codes': 'Cd2', 'data_codes': 'Cd1'}
    >>> plot_countries = {'C1': 'c1', 'C2': 'c2', 'C3': 'c3', 'C4': 'c4', 'C5': 'c5'}
    >>> year = '1953'
    >>> build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
    ({'C2': 0.0}, {'C3', 'C5', 'C1'}, {'C4'})
    """
    gdp_data_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"],
                                            gdpinfo["separator"], gdpinfo["quote"])

    code_tup = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data_dict)

    code_in_gdp_file_dict = code_tup[0]

    code_missing_in_gdp_file_set = code_tup[1]

    code_gdp_dict = {}

    gdp_missing_set = set()

    for code_in_plot, code_in_gdp in code_in_gdp_file_dict.items():
        gdp_data = gdp_data_dict[code_in_gdp]
        for inner_key, inner_value in gdp_data.items():
            if inner_key == year:
                if len(inner_value) != 0:
                    code_gdp_dict[code_in_plot] = math.log10(float(inner_value))
                else:
                    gdp_missing_set.add(code_in_plot)
    return code_gdp_dict, code_missing_in_gdp_file_set, gdp_missing_set


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    gdp_map_info = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)

    gdp_for_year = gdp_map_info[0]
    country_code_missing = gdp_map_info[1]
    gdp_data_missing = gdp_map_info[2]

    world_map_chart = pygal.maps.world.World()
    world_map_chart.title = 'GDP by country for ' + year + ' (log scale)' + ', ' + 'unified by common country CODE'
    world_map_chart.add('GDP for ' + year, gdp_for_year)
    world_map_chart.add('Missing from World Bank Data', country_code_missing)
    world_map_chart.add('No GDP data', gdp_data_missing)
    world_map_chart.render_in_browser()


if __name__ == "__main__":
    import doctest
    doctest.testmod()


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
