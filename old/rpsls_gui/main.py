#!/usr/bin/env python3.9
import PySimpleGUI as sg
import rpsls

# Number of games won, tied, and lost.
won, tied, lost = 0, 0, 0

# GUI Theme
sg.theme('SystemDefault')

# GUI Layout
layout = [[sg.B('Rock'), sg.B('Paper'), sg.B('Scissors'), sg.B('Lizard'), sg.B('Spock')],
          [sg.Text(size=(50,1), key='-OUTCOME-')],
          [sg.Text(size=(50,1), key='-SCORE-')],
          [sg.B('Quit')],
          ]

# Init window
window = sg.Window('RPSLS', layout)

# Window read loop
while True:
    event, values = window.read()
    # Breakif quit or window closed
    if event in ('Quit', sg.WINDOW_CLOSED):
        break
    # Play rpsls
    outcome = rpsls.play(event)
    # Update outcome based on rpsls.play
    window['-OUTCOME-'].update(f"You played {outcome[0]}, the computer played {outcome[1]}, you {outcome[2]}.")
    # Add one to variable (depending on win/tie/loss)
    exec(outcome[2] + '+= 1')
    # Update scoreboard
    window['-SCORE-'].update(f"Wins: {won} Ties: {tied} Losses: {lost}")
    
# Close window after loop
window.close()