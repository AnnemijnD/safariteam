import loaddata
import csv
from group import Group

class Schedule(object):
    """
    Representation of a schedule.
    """

    # temporarily set slot to None, can be removed when class is used by other class
    slot = None

    def __init__(self, slot):
        self.slot = slot

    def print_schedule(self, min, max):
        print(self.slot[min:max])


if __name__ == "__main__":

    room = 'zalen.csv'

    with open(room) as rooms:
        rooms = csv.reader(rooms, delimiter=';')
        next(rooms)

        zaalnummers = []

        # Optional code to visualize data
        for row in rooms:
            zaalnummers.append(row[0])

    # Make schedule of 140 slots, can be changed to 175 when timeslot 17 - 19 is used
    Schedule = Schedule(slot = [zaalnummers] * 140)

    # Print schedule from the first 10 room-timeslots
    Schedule.print_schedule(0,2)
