#!/usr/bin/env python3
# Imports random for computer choice and json for score storage.
import random
import json

# List of choices for the computer to use: [rock, paper, scissors, lizard, spock].
computerChoices = [5, 10, 15, 20, 25]

 # Set wins, ties, losses, and total games to zero (change these to values in score.json if continuing from save game)..
wins, ties, losses, games = 0, 0, 0, 0

# List of information relative to the index number, providing the name of the user and computer's choices as well as the outcome (0 = loss, 1 = tie, 2 = win)
# Lists are formatted as [name corresponding to userChoice, name corresponding to computerChoice, outcome]
info = json.load(open("settings.json"))

# Match third term of lists in the "info" dictionary to their string representation (for actual outut print command). 
# As well as provide a string for adding one to the list of whatever outcome (user the exec function to "run" the string).
outcomes = {
    0: ['lost', 'losses += 1'],
    1: ['tied', 'ties += 1'],
    2: ['won', 'wins += 1'],
}

# Simple function for asking the user for input and checking if it's valid.
def userInput():
    
    # Still not entirely sure how to use return so... global var
    global userChoice
    
    # Prompt the user for their choice
    # Ask the user for another input if their input is invalid (not an integer, <6 or >0)
    try:
        userChoice = int(input("\nWhat do you choose to play?\n \n 1. Rock \n 2. Paper \n 3. Scissors \n 4. Lizard \n 5. Spock\n"))
        if not userChoice < 6 or not userChoice > 0:
            print("\nPlease input a valid choice!\n")
            userInput()
    except:    
            print("\nPlease input a valid choice!\n")
            userInput()
            
def continueGame():
    
    # Ask user if they want to continue from save or overwrite.
    continueFromSave = input("\nWould you like to continue from your previously saved game?\n")
    
    # Set wins/ties/losses/games to values in scores.json if the user wishes to continue.
    if continueFromSave in ('y', 'yes'):
        # Attempt to load scores from score.json, if the file is empty or doesn't exist, new game.
        try:
            # Load score list (wins/ties/losses)
            scoreList = json.load(open("score.json"))
            # For every string in score.json, treat the string as a variable name and set it (wins/ties/losses/games) equal to its value in score.json
            for string in scoreList:
                varName = string
                integer = scoreList[string]
                globals()[varName] = integer
        except:
            print("\nYou have no game stored, starting a new game")
    elif continueFromSave in ('n', 'no'):
        # wins/ties/losses/games are already defined as zero, so they simply remain unchanged
        print("\nYou have chosen to start a new game, your saved game will be overwritten")
    else:
        # "Loop" until a valid input
        print("\nPlease input a valid answer!\n")
        continueGame()
        
# START
# Welcome to the game!
print("WELCOME TO ROCK PAPER SCISSORS LIZARD SPOCK")
    
# Use saved "game" (record of wins/ties/losses/games) or overwrite depending on user choice
continueGame()
    
# Define playing as true
playing = True

while playing:
    
    # INTERACTIONS WITH CHOICES
    # Call userInput() to input (maybe a bit messy).
    userInput()
    # Computer chooses an integer from the computerChoices list.
    computerChoice = random.choice(computerChoices)
    # Determine an index number from the computer choice and user choice.
    indexNumber = str(computerChoice - userChoice)

    # INTERACTIONS WITH DICTIONARY:
    # Set choice for user choice and computer choice (since they're originally integers).
    userChoiceName = info[indexNumber][0]
    computerChoiceName = info[indexNumber][1]
    # Set "outComeInteger" to the integer outcome from the third term in the lists in the "info" dictionary.
    outcomeInteger = info[indexNumber][2]
    
    # Add one to the record of wins/ties/losses depending on outcome
    exec(outcomes[outcomeInteger][1])
    
    # Add one to games variable.
    games += 1
    
    # PRINTING OUTPUTS:
    # Print what the user played, what the computer played, and who won.
    print(f"\nYou played {userChoiceName}, the computer played {computerChoiceName}, you {outcomes[outcomeInteger][0]}.") 
    # Print number of wins/ties/losses.
    print(f"\n Wins: {wins}\n Ties: {ties}\n Losses: {losses}\n")
    # Print win:loss ratio.
    print(f"Your win/loss ratio is {wins}:{losses}")
    # Print percentage of games won (the winrate: wins/games).
    print(f"You've won {int((wins/games)*100)}% of games\n")
    # Assign a variable to the user's repsonse to "continue playing?"
    playAgain = input("Would you like to continue playing?\n")
    
    # PLAYING AGAIN OR STOPPING: 
    # If input is invalid, loop until valid
    while playAgain not in ('n', 'no', 'y', 'yes'):
        print("\nPlease input a valid answer!\n")
        playAgain = input("Would you like to continue playing?\n")
        
    # If the input is no, stop the loop by setting playing to False
    if playAgain in ('n', 'no'):
        playing = False


# SAVE GAME
# Dictionary of values to write to json file
scoreWrite = {
    'wins': wins, 
    'ties': ties, 
    'losses': losses,
    'games': games
}
# Write to json
json.dump(scoreWrite, open("score.json",'w'))
    
