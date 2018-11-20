"""
Switch one or more RANDOM sessions.
Input is a schedule, output is a schedule with switched sessions.
"""

from random import randint
import numpy as np

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
random_numbers = []

def switch_session(schedule):

    # number_of_switched = 2
    # numbers = get_random_numbers(2)

    # Get two random numbers
    random_number = randint(0, SLOTS - 1)
    random_switch_number = randint(0, SLOTS - 1)

    # Flatten schedule to get a 1D list to switch elements
    flatten = np.array(schedule).flatten()
    temp = flatten[random_number]
    flatten[random_number] = flatten[random_switch_number]
    flatten[random_switch_number] = temp

    # Convert back to 3D list
    schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    return schedule


def get_random_numbers(int):

    return int
