"""
Switch one or more RANDOM sessions. \
Input is a schedule, output is a schedule with switched sessions. \
"""

from random import randint

def switch_session(schedule):

    DAYS = randint(0, 4)
    TIME_SLOTS = randint(0, 3)
    ROOMS = randint(0, 6)
    DAYS_switch = randint(0, 4)
    TIME_SLOTS_switch = randint(0, 3)
    ROOMS_switch = randint(0, 6)

    temp = schedule[DAYS][TIME_SLOTS][ROOMS]
    schedule[DAYS][TIME_SLOTS][ROOMS] = schedule[DAYS_switch][TIME_SLOTS_switch][ROOMS_switch]
    schedule[DAYS_switch][TIME_SLOTS_switch][ROOMS_switch] = temp

    return schedule
