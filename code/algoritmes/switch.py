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


def switch_session(schedule, number_of_switches):

    # Flatten schedule to get a 1D list to switch elements
    flatten = np.array(schedule).flatten()

    for i in range(number_of_switches):
        # Get two random numbers
        random_number = randint(0, SLOTS - 1)
        random_switch_number = randint(0, SLOTS - 1)

        flatten[random_number], flatten[random_switch_number] = flatten[random_switch_number], flatten[random_number]

    # Convert back to 3D list
    schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    print(schedule)

    # Return 3D matrix of schedule
    return schedule
