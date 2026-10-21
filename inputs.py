#!usr/bin/env python3

import math 

# Validates user input requiring a whole number (integer).
# Repeats the prompt until a valid integer meets the minimum value.
def get_integer(prompt, min_value=0):
    while True:
        try:
            value = int(input(prompt))
            
            # Reject values below the allowed minimum.
            if value < min_value:
                print(f"Value must be at least {min_value}. ")
                continue
            return value

        # Handles non-integer input without crashing the program.
        except ValueError:
            print("Please enter a whole number. ")



# Validates user input requiring a decimal or whole number (float).
# Repeats the prompt until a valid float meets the minimum value.
def get_float(prompt, min_value=0):
    while True:
        try:
            value = float(input(prompt))
            # Reject NaN and infinity to prevent invalid calculations.
            if not math.isfinite(value):
                print("Please enter a finite number. ")
                continue
            
            # Reject values below the allowed minimum.
            if value < min_value:
                print(f"Value must be at least {min_value}. ")
                continue
            return value 

        # Handles nonnumeric input without crashing the program.    
        except ValueError:
            print("Please enter a number. ")