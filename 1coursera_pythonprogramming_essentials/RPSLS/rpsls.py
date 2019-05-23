"""
Week 4 practice project template for Python Programming Essentials
Rock-paper-scissors-lizard-Spock
"""

import random


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    """
    Given string name, return integer 0, 1, 2, 3, or 4
    corresponding to number
    >>> name_to_number('rock')
    0
    >>> name_to_number('Spock')
    1
    >>> name_to_number('paper')
    2
    >>> name_to_number('lizard')
    3
    >>> name_to_number('scissors')
    4
    """

    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    else:
        return 4


def number_to_name(number):
    """
    Given integer number (0, 1, 2, 3, or 4)
    corresponding name
    >>> number_to_name(0)
    'rock'
    """
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    else:
        return 'scissors'
  

def rpsls(player_choice):
    """
    Given string player_choice, play a game of RPSLS
    and print results to console
    """

    # print a blank line to separate consecutive games
    print('')
    # print out the message for the player's choice
    print('Player chooses', player_choice)
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(5)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out message for computer's choice
    print('Computer chooses', comp_choice)
    # compute difference of player_number and comp_number modulo(%) five
    num_diff = (comp_number - player_number) % 5
    # use if/elif/else to determine winner and print winner message
    if num_diff == 0:
        print('Player and computer tie!')
    elif num_diff == 1 or num_diff == 2:
        print('Computer wins!')
    else:
        print('Player wins!')

# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

if __name__ == "__main__":
    import doctest
    doctest.testmod()