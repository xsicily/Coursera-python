"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal
import pygal_maps_world


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    >>> plot_countries = {'ABC': 'Country1', 'GHI': 'Country2', 'XYZ': 'Country3'}
    >>> gdp_countries = {'Country1':{'Country Name':'Country1', 'Country Code':'ABC', '2000': '1', '2001': '2', '2002': '3', '2003': '4'}, 'Country2':{'Country Name':'Country2', 'Country Code':'GHI'}}
    >>> reconcile_countries_by_name(plot_countries, gdp_countries)
    ({'ABC': 'Country1', 'GHI': 'Country2'}, {'XYZ'})
    """
    codes_countries_dict = {}

    code_missing_set = set()

    for key_code, value_country in plot_countries.items():
        if value_country in gdp_countries.keys():
            codes_countries_dict[key_code] = value_country
        else:
            code_missing_set.add(key_code)
    return codes_countries_dict, code_missing_set


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


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    >>> gdpinfo = {"gdpfile": "C:/Users/Sicil/PycharmProjects/pythonbasic/4coursera_datavisualization/w2/isp_gdp_csv_files/gdptable2.csv", "separator": ",", "quote": '"', "min_year": 1953, "max_year": 1958, "country_name": "Country Name", "country_code": "Country Code"}
    >>> plot_countries = {'DEFG': 'Country1', 'JKLM': 'Country2', 'XYZ': 'Country3'}
    >>> year = "1958"
    >>> build_map_dict_by_name(gdpinfo, plot_countries, year)
    ({'DEFG': 0.7781512503836436}, {'XYZ'}, {'JKLM'})
    """
    gdp_data_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"],
                                            gdpinfo["separator"], gdpinfo["quote"])

    countries_tup = reconcile_countries_by_name(plot_countries, gdp_data_dict)

    countries_in_gdp_file_dict = countries_tup[0]

    code_missing_in_gdp_file_set = countries_tup[1]

    country_code_gdp_dict = {}

    gdp_missing_set = set()

    for key_code, value_country in countries_in_gdp_file_dict.items():
        gdp_data = gdp_data_dict[value_country]
        for inner_key, inner_value in gdp_data.items():
            if inner_key == year:
                if len(inner_value) != 0:
                    country_code_gdp_dict[key_code] = math.log10(float(inner_value))
                else:
                    gdp_missing_set.add(key_code)
    return country_code_gdp_dict, code_missing_in_gdp_file_set, gdp_missing_set


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    None
    """
    gdp_map_info = build_map_dict_by_name(gdpinfo, plot_countries, year)

    gdp_for_year = gdp_map_info[0]
    country_code_missing = gdp_map_info[1]
    gdp_data_missing = gdp_map_info[2]

    world_map_chart = pygal.maps.world.World()
    world_map_chart.title = 'GDP by country for ' + year + ' (log scale)' + ', ' + 'unified by common country Name'
    world_map_chart.add('GDP for ' + year, gdp_for_year)
    world_map_chart.add('Missing from World Bank Data', country_code_missing)
    world_map_chart.add('No GDP data', gdp_data_missing)
    world_map_chart.render_in_browser()


def test_render_world_map():
    """
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
