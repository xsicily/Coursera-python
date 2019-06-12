"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball stastics.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv

##
## Provided code from Week 3 Project
##

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
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


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
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

##
## Provided formulas for common batting statistics
##


# Typical cutoff used for official statistics
MINIMUM_AB = 500


def batting_average(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0


def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0


def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


##
## Part 1: Functions to compute top batting statistics by year
##

def filter_by_year(statistics, year, yearid):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    >>> statistics = [ \
                     {'playerID': 'braunry02', 'yearID': '2011', 'teamID': 'MIL', 'AB': '563', 'H': '187'}, \
                     {'playerID': 'cabremi01', 'yearID': '2011', 'teamID': 'DET', 'AB': '572', 'H': '197'}, \
                     {'playerID': 'braunry02', 'yearID': '2012', 'teamID': 'MIL', 'AB': '598', 'H': '191'}, \
                     {'playerID': 'cabremi01', 'yearID': '2012', 'teamID': 'DET', 'AB': '622', 'H': '205'}, \
                     {'playerID': 'beltrad01', 'yearID': '2013', 'teamID': 'TEX', 'AB': '631', 'H': '199'}, \
                     {'playerID': 'cabremi01', 'yearID': '2013', 'teamID': 'DET', 'AB': '555', 'H': '193'}, \
                     {'playerID': 'beltrad01', 'yearID': '2014', 'teamID': 'TEX', 'AB': '549', 'H': '178'}, \
                     {'playerID': 'brantmi02', 'yearID': '2014', 'teamID': 'CLE', 'AB': '611', 'H': '200'}]
    >>> year = 2011
    >>> yearid = 'yearID'
    >>> filter_by_year(statistics, year, yearid)
    [{'playerID': 'braunry02', 'yearID': '2011', 'teamID': 'MIL', 'AB': '563', 'H': '187'}, {'playerID': 'cabremi01', 'yearID': '2011', 'teamID': 'DET', 'AB': '572', 'H': '197'}]
    """
    batting_stats_dict_list = []

    for stats_dict in statistics:
        if int(stats_dict[yearid]) == year:
            batting_stats_dict_list.append(stats_dict)
    return batting_stats_dict_list


def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    >>> info = {'masterfile': '', 'battingfile': '', 'separator': ',', 'quote': '"', 'playerid': 'player', 'firstname': 'firstname', 'lastname': 'lastname', 'yearid': 'year', 'atbats': 'atbats', 'hits': 'hits', 'doubles': 'doubles', 'triples': 'triples', 'homeruns': 'homers', 'walks': 'walks', 'battingfields': ['atbats', 'hits', 'doubles', 'triples', 'homers', 'walks']}
    >>> statistics = [{'player': 'player0', 'doubles': '20', 'atbats': '300', 'hits': '108', 'homers': '5', 'year': '2020', 'walks': '25', 'triples': '1'}, {'player': 'player1', 'doubles': '5', 'atbats': '499', 'hits': '170', 'homers': '4', 'year': '2020', 'walks': '10', 'triples': '3'}, {'player': 'player2', 'doubles': '18', 'atbats': '513', 'hits': '129', 'homers': '20', 'year': '2020', 'walks': '85', 'triples': '5'}, {'player': 'player5', 'doubles': '3', 'atbats': '197', 'hits': '67', 'homers': '22', 'year': '2020', 'walks': '37', 'triples': '2'}, {'player': 'player6', 'doubles': '33', 'atbats': '542', 'hits': '166', 'homers': '18', 'year': '2020', 'walks': '25', 'triples': '7'}, {'player': 'player7', 'doubles': '19', 'atbats': '500', 'hits': '161', 'homers': '10', 'year': '2020', 'walks': '27', 'triples': '2'}, {'player': 'player8', 'doubles': '42', 'atbats': '589', 'hits': '176', 'homers': '25', 'year': '2020', 'walks': '30', 'triples': '13'}, {'player': 'player0', 'doubles': '5', 'atbats': '321', 'hits': '114', 'homers': '0', 'year': '2021', 'walks': '15', 'triples': '0'}, {'player': 'player2', 'doubles': '27', 'atbats': '522', 'hits': '130', 'homers': '14', 'year': '2021', 'walks': '42', 'triples': '4'}, {'player': 'player3', 'doubles': '40', 'atbats': '555', 'hits': '167', 'homers': '22', 'year': '2021', 'walks': '1', 'triples': '7'}, {'player': 'player5', 'doubles': '3', 'atbats': '123', 'hits': '44', 'homers': '0', 'year': '2021', 'walks': '12', 'triples': '0'}, {'player': 'player7', 'doubles': '30', 'atbats': '501', 'hits': '145', 'homers': '30', 'year': '2021', 'walks': '29', 'triples': '10'}, {'player': 'player9', 'doubles': '41', 'atbats': '515', 'hits': '154', 'homers': '32', 'year': '2021', 'walks': '18', 'triples': '7'}, {'player': 'player0', 'doubles': '8', 'atbats': '297', 'hits': '109', 'homers': '2', 'year': '2022', 'walks': '12', 'triples': '1'}, {'player': 'player1', 'doubles': '42', 'atbats': '512', 'hits': '157', 'homers': '23', 'year': '2022', 'walks': '38', 'triples': '17'}, {'player': 'player2', 'doubles': '12', 'atbats': '518', 'hits': '150', 'homers': '35', 'year': '2022', 'walks': '20', 'triples': '12'}, {'player': 'player3', 'doubles': '37', 'atbats': '519', 'hits': '165', 'homers': '12', 'year': '2022', 'walks': '25 ', 'triples': '2'}, {'player': 'player4', 'doubles': '53', 'atbats': '578', 'hits': '175', 'homers': '35', 'year': '2022', 'walks': '30', 'triples': '17'}, {'player': 'player5', 'doubles': '2', 'atbats': '170', 'hits': '60', 'homers': '1', 'year': '2022', 'walks': '15', 'triples': '0'}, {'player': 'player8', 'doubles': '47', 'atbats': '552', 'hits': '160', 'homers': '12', 'year': '2022', 'walks': '72', 'triples': '1'}, {'player': 'player9', 'doubles': '60', 'atbats': '508', 'hits': '155', 'homers': '3', 'year': '2022', 'walks': '27', 'triples': '5'}]
    >>> formula = batting_average
    >>> numplayers = 5
    >>> top_player_ids(info, statistics, formula, numplayers)
    [('player7', 0.322), ('player3', 0.3179190751445087), ('player1', 0.306640625), ('player6', 0.3062730627306273), ('player9', 0.3051181102362205)]
    """
    player_stats_list = []

    for batting_stats in statistics:
        player_stats = formula(info, batting_stats)
        player_id = batting_stats[info['playerid']]
        tup = player_id, player_stats
        player_stats_list.append(tup)

    player_stats_list_sorted = sorted(player_stats_list, key=lambda pair: pair[1], reverse=True)

    return player_stats_list_sorted[:numplayers]


def lookup_player_names(info, top_ids_and_stats):
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    >>> info = {'masterfile': 'C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w4/isp_baseball_files/master1.csv', 'battingfile': '', 'separator': ',', 'quote': '"', 'playerid': 'player', 'firstname': 'firstname', 'lastname': 'lastname', 'yearid': 'year', 'atbats': 'atbats', 'hits': 'hits', 'doubles': 'doubles', 'triples': 'triples', 'homeruns': 'homers', 'walks': 'walks', 'battingfields': ['atbats', 'hits', 'doubles', 'triples', 'homers', 'walks']}
    >>> top_ids_and_stats = [('player0', 0.1)]
    >>> lookup_player_names(info, top_ids_and_stats)
    ['0.100 --- Alfredo Hopkins']
    """
    player_name_list = []
    master_dict = read_csv_as_nested_dict(info['masterfile'], info['playerid'], info['separator'], info['quote'])

    for tup in top_ids_and_stats:
        if tup[0] in master_dict:
            first_name = master_dict[tup[0]][info['firstname']]
            last_name = master_dict[tup[0]][info['lastname']]
            player_name_string = f'{tup[1]:.3f}' + ' --- ' + first_name + ' ' + last_name
            player_name_list.append(player_name_string)
    return player_name_list


def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    >>> info = {'masterfile': 'C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w4/isp_baseball_files/master2.csv', 'battingfile': 'C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w4/isp_baseball_files/batting2.csv', 'separator': ',', 'quote': '"', 'playerid': 'playerID', 'firstname': 'nameFirst', 'lastname': 'nameLast', 'yearid': 'year', 'atbats': 'AB', 'hits': 'H', 'doubles': '2B', 'triples': '3B', 'homeruns': 'homers', 'walks': 'walks', 'battingfields': ['atbats', 'hits', 'doubles', 'triples', 'homers', 'walks']}
    >>> formula = batting_average
    >>> numplayers = 5
    >>> year = 2006
    >>> compute_top_stats_year (info, formula, numplayers, year)
    ['0.339 --- Miguel Cabrera', '0.329 --- Vladimir Guerrero', '0.329 --- Garrett Atkins', '0.315 --- Jermaine Dye', '0.315 --- Lance Berkman']
    """
    statistics = read_csv_as_list_dict(info['battingfile'], info['separator'], info['quote'])
    new_stats = filter_by_year(statistics, year, info['yearid'])
    top_ids_and_stats = top_player_ids(info, new_stats, formula, numplayers)
    top_players_list = lookup_player_names(info, top_ids_and_stats)
    return top_players_list


##
## Part 2: Functions to compute top batting statistics by career
##

def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    >>> statistics =  [\
         {'playerID': 'braunry02', 'yearID': '2011', 'teamID': 'MIL', 'AB': '563', 'H': '187'}, \
         {'playerID': 'cabremi01', 'yearID': '2011', 'teamID': 'DET', 'AB': '572', 'H': '197'}, \
         {'playerID': 'braunry02', 'yearID': '2012', 'teamID': 'MIL', 'AB': '598', 'H': '191'}, \
         {'playerID': 'cabremi01', 'yearID': '2012', 'teamID': 'DET', 'AB': '622', 'H': '205'}, \
         {'playerID': 'beltrad01', 'yearID': '2013', 'teamID': 'TEX', 'AB': '631', 'H': '199'}, \
         {'playerID': 'cabremi01', 'yearID': '2013', 'teamID': 'DET', 'AB': '555', 'H': '193'}, \
         {'playerID': 'beltrad01', 'yearID': '2014', 'teamID': 'TEX', 'AB': '549', 'H': '178'}, \
         {'playerID': 'brantmi02', 'yearID': '2014', 'teamID': 'CLE', 'AB': '611', 'H': '200'}]
    >>> playerid = "playerID"
    >>> fields = ['AB', 'H']
    >>> aggregate_by_player_id(statistics, playerid, fields)
    {'braunry02': {'playerID': 'braunry02', 'AB': 1161, 'H': 378}, 'cabremi01': {'playerID': 'cabremi01', 'AB': 1749, 'H': 595}, 'beltrad01': {'playerID': 'beltrad01', 'AB': 1180, 'H': 377}, 'brantmi02': {'playerID': 'brantmi02', 'AB': 611, 'H': 200}}
    """
    # make new_stats only includes playerId and field information
    new_stats = []
    for row in statistics:
        new_dict = {playerid: row[playerid]}
        for field in fields:
            new_dict[field] = int(row[field])
        new_stats.append(new_dict)

    outer_dict = {}

    for stats in new_stats:
        if not stats[playerid] in outer_dict:   # setup entry
            outer_dict[stats[playerid]] = stats
        else:
            for field in fields:
                outer_dict[stats[playerid]][field] = int(outer_dict[stats[playerid]][field]) + int(stats[field])
    return outer_dict


def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    >>> info = {'masterfile': "C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w4/isp_baseball_files/master1.csv", 'battingfile': "C:/Users/Sicil/PycharmProjects/pythonbasic/3coursera_dataanalysis/w4/isp_baseball_files/batting1.csv", 'separator': ',', 'quote': '"', 'playerid': 'player', 'firstname': 'firstname', 'lastname': 'lastname', 'yearid': 'year', 'atbats': 'atbats', 'hits': 'hits', 'doubles': 'doubles', 'triples': 'triples', 'homeruns': 'homers', 'walks': 'walks', 'battingfields': ['atbats', 'hits', 'doubles', 'triples', 'homers', 'walks']}
    >>> formula = batting_average
    >>> numplayers = 4
    >>> compute_top_stats_career(info, formula, numplayers)
    ['0.361 --- Alfredo Hopkins', '0.323 --- Jay Ramos', '0.309 --- Melvin Graves', '0.306 --- Claudia Brown']
    """
    statistics = read_csv_as_list_dict(info['battingfile'], info['separator'], info['quote'])

    aggregate_stats_dict = aggregate_by_player_id(statistics, info["playerid"], info['battingfields'])

    aggregate_stats_list = []

    for key, value in aggregate_stats_dict.items():
        aggregate_stats_list.append(value)

    top_ids_and_stats = top_player_ids(info, aggregate_stats_list, formula, numplayers)

    top_stats_list = lookup_player_names(info, top_ids_and_stats)

    return top_stats_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()

##
## Provided testing code
##

def test_baseball_statistics():
    """
    Simple testing code.
    """

    #
    # Dictionary containing information needed to access baseball statistics
    # This information is all tied to the format and contents of the CSV files
    #
    baseballdatainfo = {"masterfile": "Master_2016.csv",   # Name of Master CSV file
                        "battingfile": "Batting_2016.csv", # Name of Batting CSV file
                        "separator": ",",                  # Separator character in CSV files
                        "quote": '"',                      # Quote character in CSV files
                        "playerid": "playerID",            # Player ID field name
                        "firstname": "nameFirst",          # First name field name
                        "lastname": "nameLast",            # Last name field name
                        "yearid": "yearID",                # Year field name
                        "atbats": "AB",                    # At bats field name
                        "hits": "H",                       # Hits field name
                        "doubles": "2B",                   # Doubles field name
                        "triples": "3B",                   # Triples field name
                        "homeruns": "HR",                  # Home runs field name
                        "walks": "BB",                     # Walks field name
                        "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]}

    print("Top 5 batting averages in 1923")
    top_batting_average_1923 = compute_top_stats_year(baseballdatainfo, batting_average, 5, 1923)
    for player in top_batting_average_1923:
        print(player)
    print("")

    print("Top 10 batting averages in 2010")
    top_batting_average_2010 = compute_top_stats_year(baseballdatainfo, batting_average, 10, 2010)
    for player in top_batting_average_2010:
        print(player)
    print("")

    print("Top 10 on-base percentage in 2010")
    top_onbase_2010 = compute_top_stats_year(baseballdatainfo, onbase_percentage, 10, 2010)
    for player in top_onbase_2010:
        print(player)
    print("")

    print("Top 10 slugging percentage in 2010")
    top_slugging_2010 = compute_top_stats_year(baseballdatainfo, slugging_percentage, 10, 2010)
    for player in top_slugging_2010:
        print(player)
    print("")

    # You can also use lambdas for the formula
    #  This one computes onbase plus slugging percentage
    print("Top 10 OPS in 2010")
    top_ops_2010 = compute_top_stats_year(baseballdatainfo,
                                          lambda info, stats: (onbase_percentage(info, stats) +
                                                               slugging_percentage(info, stats)),
                                          10, 2010)
    for player in top_ops_2010:
        print(player)
    print("")

    print("Top 20 career batting averages")
    top_batting_average_career = compute_top_stats_career(baseballdatainfo, batting_average, 20)
    for player in top_batting_average_career:
        print(player)
    print("")


# Make sure the following call to test_baseball_statistics is
# commented out when submitting to OwlTest/CourseraTest.

# test_baseball_statistics()
