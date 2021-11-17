#!/usr/bin/env python3

# Imports
import re
# Fancy colors (YOU MUST INSTALL TERMCOLOR FOR THIS TO WORK)
from termcolor import colored
# Getpass for not echoing password
import getpass

# Check length (allowed length of at least 8 characters)
def length_check(password):
    if len(password) >= 8:
        return True, 1, 'green'
    else:
        return False, 0, 'yellow'

# Check if the password has both lower and upper case letters
def lower_and_upper_check(password):
    if re.search('[A-Z]', password) and re.search('[a-z]', password):
        return True, 1, 'green'
    else:
        return False, 0, 'yellow'

# Check if the password has at least one number
def digit_check(password):
    if re.search('\d', password):
        return True, 1, 'green'
    else:
        return False, 0, 'yellow'

# Check if the password has at least one special character (UNDERSCORE COUNTS)
def special_char_check(password):
    if re.search('[^a-zA-Z0-9]', password):
        return True, 1, 'green'
    else:
        return False, 0, 'yellow'

# Checks if the password DOESNT have any words (>=4) from words_alpha.txt in it
def dict_check(password):
   # String of matched words 
    words_in_string = ""
    # Open file
    with open('/home/cone/COMPSCI/Demos/words_alpha.txt', 'r') as f:
        # For every line
        for line in f:
            # Get rid of newline char
            raw_line = line.removesuffix('\n')
            # If the line is 4 or more characters:
            if len(raw_line) >= 4:
                # If the word (line) is in the password, add the word found to a string
                result = re.search(raw_line, password.lower())
                if result:
                    words_in_string += (result.group() + ', ')
    
    # If there are no words found in the password:
    if words_in_string != "":
        # words_in_string[:-2] to remove extra ", " added to end of the full string when adding to string in loop above
        return False, 0, 'yellow', words_in_string[:-2] , 'red'
    else:
        return True, 1, 'green', None, 'green'

# Determine password strength
def password_strength():
    # Define strength possiblities and corresponding colors
    strengths = (
        ('terrible', 'red'), 
        ('very weak', 'red'), 
        ('weak', 'yellow'), 
        ('good', 'yellow'), 
        ('very good', 'green'), 
        ('amazing', 'green')
        )
    # Determines the strength of the password depending on numerical values (True=1, False=0) from functions
    int_strength = length[1] + cases[1] + digits[1] + special_chars[1] + not_in_dict[1]
    # Return the corresponding string (based on numerical values above)
    return strengths[int_strength]

# START
# Input password (doesn't echo because of getpass)
password = getpass.getpass("Input your password:")

# Call each function once, and set outputs equal to variables (so you don't have to call things multiple times)
# Check length
length = length_check(password)
# Check cases
cases = lower_and_upper_check(password)
# Check if at least one digit
digits = digit_check(password)
# Check if at least one special character
special_chars = special_char_check(password)
# Check if NO words are found in the password
not_in_dict = dict_check(password)
# Password strength
strength = password_strength()

# Print results of functions (meanings above))
print('\n8 or more characters:', colored(length[0], length[2]))
print('Upper and lower case:', colored(cases[0], cases[2]))
print('At least one digit:', colored(digits[0], digits[2]))
print('One special character:', colored(special_chars[0], special_chars[2]) + '\n')
print('No dictionary words in password:', colored(not_in_dict[0], not_in_dict[2]))
if not not_in_dict[0]:
    print('Words found in password:', colored(not_in_dict[3], not_in_dict[4]))
print('\nYour password is', colored(strength[0], strength[1]))