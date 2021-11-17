#!/usr/bin/env python3
# Import random for pseudo-random number generation
import random

# "Map" of int inputs to string inputs 
options = {
    1 : "rock",
    2 : "paper",
    3 : "scissors",
}

# Inputs from user and computer (integer from 1-3)
def inputs():
    
    # Define global vars
    global userChoice, computerChoice

    # Repeats function if the input isn't an integer or is invalid (think i can apply some operators here)
    try:
        # User input/choice
        userChoice = int(input("\nWhat do you choose to play? \n 1. Rock \n 2. Paper \n 3. Scissors\n"))
    except:
        print("\nPlease input a valid Choice!\n")
        inputs()
    else:
        # Check if valid input
        if not userChoice < 4 or not userChoice > 0:
            print("\nPlease input a valid Choice!\n")
            inputs()
    
        
        # Computer chooses int from 1 - 3
        computerChoice = random.randint(1, 3)
        # Print for testing (not entirely necessary, but it tells you the numerical value that the computer chose which is nice)
        print(f"\nThe computer chose {computerChoice}")

    

# Determine who wins by comparing int inputs from both players
def winner(p, c):
    
    # Global vars
    global wins, ties, losses, totalGames
    
    # Add one to total games
    totalGames = totalGames + 1
    
    # Determine who wins, do this by adding one and applying a modulus of three since each number loses to whatever number is one above it (and 3 loses to 1)
    if (p+1) % 3 == c:
        losses += 1
        output("lose")
    elif p == c:
        ties += 1
        output("tie")
    else:
        wins += 1
        output("win")
        
        
# Output the result of winner() (convert integer to string, calculate and display win ratio and rate and display and display wins/ties/losses)
def output(outcome):
    
    # Global vars (need to stop relying on these)
    global choiceName, computerChoiceName
    
    # Turn user int choice into string choice (for output), 
    choiceName = options[userChoice]
        
    # Turn computer int choice into string for output
    computerChoiceName = options[computerChoice]

    # Winrate equal to wins/total games
    winRate = round(((wins/totalGames)*100), 1)
    
    # Printing outcome, wins/ties/losses and win ratio and rate
    # Print outcome
    print(f"You chose {choiceName}, you {outcome} because the computer played {computerChoiceName}")
    # Print number of wins, ties, and losses
    print(f"\n Wins: {wins}\n Ties: {ties}\n Losses: {losses}\n")
    # Print win/loss ratio and win rate (wins/total games)
    print(f"Your win/loss ratio is: {wins}:{losses}\nYour total winrate is: {winRate}%\n")


# Ask the user to play again (break the loop by setting "playing" to False)
def askToPlayAgain():

    # Global vars
    global playing

    # Ask to play again
    playAgain = input("Would you like to play again?\n")

    # Continue playing if yes, stop playing (effectively break) if no
    if playAgain in ('n', 'no'):
        playing = False
    elif  playAgain in ('y', 'yes'):
        playing = True
    else:
        print("\nPlease input a valid answer!\n")
        askToPlayAgain()

# Start
# Define wins/ties/losses
wins, ties, losses, totalGames = 0, 0, 0, 0

# Define playing
playing = True

# Welcome user
print("WELCOME TO ROCK PAPER SCISSORS, SEE IF YOU CAN BEAT THE COMPUTER!")

# Main loop
while playing:
    inputs()
    winner(userChoice, computerChoice)
    askToPlayAgain()


