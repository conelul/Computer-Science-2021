#!/usr/bin/env python3.10
import PySimpleGUI as sg
import pickle

# Load tasks from file here
task_table = []

# Make the theme dark grey and font roboto.
sg.theme("DarkGray9")
# sg.SetOptions(font="Roboto 12")

# Input window.
input_frame = [[sg.Text('Name:')],
               [sg.Input(key='-task_name-')],
               [sg.Text('Date:')],
               [sg.Input(key='-task_date-')],  
               [sg.CalendarButton('Choose a Date',
                                  close_when_date_chosen=True,
                                  target="-task_date-",
                                  format="%m-%d")],
               [sg.Text('Notes:')],
               [sg.Input(key='-task_note-')],
               [sg.Button('Add', key='-add_task-', focus=True), sg.Button('Clear', key='-clear_task_fields-')]
]

# Simple table for listing tasks
table_frame = [[sg.Table(task_table, 
                         headings=['Name', 'Date'],
                         auto_size_columns=False,
                         justification="center",
                         expand_y=True,
                         expand_x=True,
                         hide_vertical_scroll=True,
                         enable_events=True,
                         key='-task_table-',)]
]

# Simple layout for displaying task notes (and editing)
notes_frame = [[sg.Text('Notes:')],
               [sg.Multiline(key='-notes-',
                             auto_refresh=True,
                             expand_y=True,
                             rstrip=True,
                             disabled=True,
                             no_scrollbar=True)],
               [sg.pin(sg.Button('Edit', key='-edit_note-', disabled=True)), 
                sg.pin(sg.Button('Save', key='-save_note-', visible=False)), 
                sg.pin(sg.Button('Revert',key='-revert_note-',visible=False)),
                sg.pin(sg.Button('Delete Task', key='-delete_task-', disabled=True))],
]

# Put the individual layouts together in columns
layout = [[sg.Column(table_frame, expand_x=True, expand_y=True)], [sg.Column(input_frame, expand_y=True), sg.Column(notes_frame, expand_y=True,)]]

def add_task():
    # Define row list.
    row = []
    # Append information values to the row list.
    row.append(values['-task_name-'])
    row.append(values['-task_date-'])
    row.append(values['-task_note-'])
    # Append row to the table list.
    task_table.append(row)
    # Update the window.
    window['-task_table-'].update(task_table)
    
def clear_task_fields():
    window['-task_name-']('')
    window['-task_date-']('')
    window['-task_note-']('') 

# Display task in multiline.
def display_task(row):
    window['-notes-'](task_table[row][2])

# Turn edit more on or off.
def edit_mode(enabled):
    if enabled == True:
        window['-notes-'].update(disabled=False)
        window['-delete_task-'].update(visible=False)
        window['-edit_note-'].update(visible=False)
        window['-save_note-'].update(visible=True)
        window['-revert_note-'].update(visible=True)
        window['-delete_task-'].update(visible=True)
        
    elif enabled == False:
        window['-notes-'].update(disabled=True)
        window['-edit_note-'].update(visible=True)
        window['-save_note-'].update(visible=False)
        window['-revert_note-'].update(visible=False)
    else:
        sg.popup('Fatal Error, closing')
        window.close()
        
def save_note(row):
    task_table[row][2] = values['-notes-']
    window['-task_table-'].update()

def revert_note(row):
    window['-notes-'](task_table[row][2])
    window['-task_table-'].update()

def delete_task(row):
    del task_table[row]
    window['-task_table-'].update(task_table)

# Make the window
window = sg.Window('Planner', layout, finalize=True)

# Load list (ignore if file not found).
try:
    with open('taskinfo', 'rb') as f:
        task_table = pickle.load(f)
except Exception:
    pass

# Update window (display saved tasks).
window['-task_table-'].update(task_table)

# Event loop
while True:
    # Read the window
    event, values = window.read()
     
    try:
        row_selected = values['-task_table-'][0]
    except:
        pass
    # Switch statement for window events
    match event:
        # Break loop if window closed.
        case sg.WINDOW_CLOSED:
            break
        # Adding a task
        case '-add_task-':
            if values['-task_name-'] and values['-task_date-']:
                add_task()
            else:
                sg.popup('Fill the name and date fields first!', title='Missing Fields', auto_close=True, auto_close_duration=2)
        # Clear task fields (name, date, notes):
        case '-clear_task_fields-':
            clear_task_fields()
        # Display selected task's notes in the notes multiline.
        case '-task_table-':
            try:
                row_selected = values['-task_table-'][0]
                display_task(row_selected)
                window['-edit_note-'].update(disabled=False)
                window['-delete_task-'].update(disabled=False)
                window['-delete_task-'].update(disabled=False)
            except Exception:
                pass
        # Enabled edit mode.
        case '-edit_note-':
            edit_mode(True)
            window['-task_table-'].Widget.config(selectmode=sg.TABLE_SELECT_MODE_NONE)
            window['-add_task-'].update(disabled=True)
            window['-clear_task_fields-'].update(disabled=True)
        # Save note.
        case '-save_note-':
            save_note(row_selected)
            edit_mode(False) 
            window['-task_table-'].Widget.config(selectmode=sg.TABLE_SELECT_MODE_BROWSE)
            window['-add_task-'].update(disabled=False)
            window['-clear_task_fields-'].update(disabled=False)
        # Re-displaying list content in multiline.
        case '-revert_note-':
            revert_note(row_selected)
        # Deleting a task.
        case '-delete_task-':
            delete_task(row_selected)
            window['-notes-']('')
            edit_mode(False) 
            window['-edit_note-'].update(disabled=False)
            window['-delete_task-'].update(disabled=True)
            window['-add_task-'].update(disabled=False)
            window['-clear_task_fields-'].update(disabled=False)
            window['-task_table-'].Widget.config(selectmode=sg.TABLE_SELECT_MODE_BROWSE)
        
# Save task information.
with open('taskinfo', 'wb') as f:
    pickle.dump(task_table, f)
    
# Cloes the window after the event loop. 
window.close()