import loaddata
import csv
from group import Group

TIMESLOTS = 140
# DAYS = 7

class Schedule(object):
    """
    Representation of a schedule.
    """

    # temporarily set slot to None, can be removed when class is used by other class
    slots = [None] * TIMESLOTS

    def __init__(self, slots):
        self.slot = slots

    def print_schedule(self, min, max):
        print(self.slot[min:max])

    # #  bedenken op welke manier we dag willen 'aanroepen' (maandag 0 en vrijdag 4?)
    # def schedule_day(self, day):
    #     classes = []
    #     for i in range(TIMESLOTS, DAYS):
    #         classes.append(slots[])


if __name__ == "__main__":

    room = 'zalen.csv'

    # Makes list with room numbers
    with open(room) as rooms:
        rooms = csv.reader(rooms, delimiter=';')
        next(rooms)

        zaalnummers = []

        # Optional code to visualize data
        for row in rooms:
            zaalnummers.append(row[0])

    # Make schedule of 140 slots, can be changed to 175 when timeslot 17 - 19 is used
    # Schedule = Schedule(slot = [zaalnummers] * 140)

    # Print schedule from the first 10 room-timeslots
<<<<<<< HEAD
    # Schedule.print_schedule(0,2)
=======
    Schedule.print_schedule(0, 2)
>>>>>>> 5bd10de0cc89cb332de423ea1117658bb963d91e
