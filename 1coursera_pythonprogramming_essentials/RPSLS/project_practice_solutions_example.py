"""
Week 4 practice project solution for Python Programming Essentials
Rock-paper-scissors-lizard-Spock
Note that your implementaiton need not match ours
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
    corresponding to numbering in video
    """

    # convert name to number using if/elif/else
    # don't forget to return the result!
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    else:
        return 4


def number_to_name(number):
    """
    Given integer number (0, 1, 2, 3, or 4)
    corresponding name from video
    """

    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    else:
        return "scissors"


def rpsls(player_choice):
    """
    Given string player_choice, play a game of RPSLS
    and print results to console
    """

    # print a blank line to separate consecutive games
    print()

    # print out the message for the player's choice
    print("Player choose", player_choice)

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)

    # print out message for computer's choice
    print("Computer choose", comp_choice)

    # compute difference of player_number and comp_number modulo five
    difference = (comp_number - player_number) % 5

    # use if/elif/else to determine winner and print winner message
    if difference == 0:
        print("Player and computer tie!")
    elif (difference == 1) or (difference == 2):
        print("Computer wins!")
    else:
        print("Player wins!")


# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric

