"""
Switch one or more RANDOM sessions.
Input is a schedule and number of sessions to be switched.
Output is a schedule with switched sessions.
"""

from random import randint

TIME_SLOTS = 4
DAYS = 5
ROOMS = 7

def switch_session(schedule):

    # Get two random locations
    location1 = random_location()
    location2 = random_location()

    # If the numbers are equal to each other, make another number
    while location1 is location2:
        location1 = random_location()
        location2 = random_location()

    # Make the switch
    schedule[location1[0]][location1[1]][location1[2]], schedule[location2[0]][location2[1]][location2[2]] = \
        schedule[location2[0]][location2[1]][location2[2]], schedule[location1[0]][location1[1]][location1[2]]

    return schedule

def random_location():

    rand_days = randint(0, DAYS - 1)
    rand_rooms = randint(0, TIME_SLOTS - 1)
    rand_slots = randint(0, ROOMS - 1)
    rand_location = [rand_days, rand_rooms, rand_slots]

    return rand_location
