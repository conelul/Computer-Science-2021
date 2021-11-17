#!/usr/bin/env python3.9
# Imports the given module from the given module_name.
import random

# Define wins, ties, losses, and total games
wins, ties, losses, totalGames = 0, 0, 0, 0

# List of choices for the computer to use: [rock, paper, scissors, lizard, spock].
computerChoices = [5, 10, 15, 20, 25]

# List of information relative to the index number, providing the name of the user and computer's choices as well as the outcome ('lost' = loss, 1 = tie, 'win' = win)
# Lists are formatted as [name corresponding to userChoice, name corresponding to computerChoice, outcome]
# SHOULD CHANGE TO TUPLES
info = {
    # If computer's choice is 5 (rock)
    0: ['spock', 'rock', 'won'],
    1: ['lizard', 'rock', 'lost'],
    2: ['scissors', 'rock', 'lost'],
    3: ['paper', 'rock', 'won'],
    4: ['rock', 'rock', 'tied'],
    
    # If computer's choice is 1'lost' (pa'],
    6: ['lizard', 'paper', 'won'],
    7: ['scissors', 'paper', 'won'],
    8: ['paper', 'paper', 'tied'],
    9: ['rock', 'paper', 'lost'],
    
    # If computer's choice is 15 (scissors)
    10: ['spock', 'scissors', 'won'],
    11: ['lizard', 'scissors', 'lost'],
    12: ['scissors', 'scissors', 'tied'],
    13: ['paper', 'scissors', 'lost'],
    14: ['rock', 'scissors', 'won'],
    
    # If computer's choice is 'win''lost' (lizard)
    15: ['spock', 'lizard', 'lost'],
    16: ['lizard', 'lizard', 'tied'],
    17: ['scissors', 'lizard', 'won'],
    18: ['paper', 'lizard', 'lost'],
    19: ['rock', 'lizard', 'won'],
    
    # If computer's choice is 'win'5 (spock)
    20: ['spock', 'spock', 'tied'],
    21: ['lizard', 'spock', 'won'],
    22: ['scissors', 'spock', 'lost'],
    23: ['paper', 'spock', 'won'],
    24: ['rock', 'spock', 'lost']  
}

def play(userPlay):
    
    if userPlay == 'Rock':
        intUserPlay = 1
    elif userPlay == 'Paper':
        intUserPlay = 2
    elif userPlay == 'Scissors':
        intUserPlay = 3
    elif userPlay == 'Lizard':
        intUserPlay = 4
    elif userPlay == 'Spock':
        intUserPlay = 5
    else:
        return 'ERROR'
    
    # Computer chooses
    computerChoice = random.choice(computerChoices)
    # Corresponding value in the "info" dictionary
    outcome = info[computerChoice - intUserPlay]
    
    # Return values
    return outcome