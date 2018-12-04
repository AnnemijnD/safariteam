"""
Switch one or more RANDOM sessions.
Input is a schedule and number of sessions to be switched.
Output is a schedule with switched sessions.
"""

from random import randint
import numpy as np

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7


# ZODRA WE MAAR 1 SESSION PER KEER WILLEN SWITCHEN KAN DE 'NUMBER_OF_SWITCHES' WEG
# EN DAN KAN OOK DE 'FOR I IN RANGE(NUMBER_OF_SWITCHES)' WEG.

def switch_session(schedule, number_of_switches, session_to_switch):

    # Flatten schedule to get a 1D list to switch elements
    flatten = np.array(schedule).flatten()

    # If there is no specific session to switch, make a random switch
    if session_to_switch < 0:

        for i in range(number_of_switches):
            # Get two random numbers
            random_number = randint(0, SLOTS - 1)
            random_switch_number = randint(0, SLOTS - 1)

            # If the numbers are equal to each other, make another number
            while random_number is random_switch_number:
                random_number = randint(0, SLOTS - 1)
                random_switch_number = randint(0, SLOTS - 1)
            # Make the switch
            flatten[random_number], flatten[random_switch_number] = flatten[random_switch_number], flatten[random_number]

    # If a specific session (with most maluspoints) has to be switched:
    else:
        # Iterate over every session in the schedule to get the session location
        for location in range(len(flatten)):
            # If location of the session was found:
            if flatten[location].overall_id == session_to_switch:
                for i in range(number_of_switches):
                    # Get one random number
                    random_number = randint(0, SLOTS - 1)
                    # If the numbers are equal to each other, make another number
                    while random_number is location:
                        random_number = randint(0, SLOTS - 1)
                    # Switch the specific session with a random other session
                    flatten[random_number], flatten[location] = flatten[location], flatten[random_number]

    # Convert back to 3D list
    schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    # Return 3D matrix of schedule
    return schedule
