import loaddata
import csv
from group import Group

TIMESLOTS = 140
# DAYS = 7

class Schedule(object):
    """
    Representation of a schedule.
    """

    def __init__(self, session, type):
        self.session = session
        self.type = type
        self.empty_schedule = [None] * TIMESLOTS

        for item in range(0, TIMESLOTS):
            self.empty_schedule[item] = session, type



    #def print_schedule(self, min, max):
    #    print(self.slots[min:max])

    # #  bedenken op welke manier we dag willen 'aanroepen' (maandag 0 en vrijdag 4?)
    # def schedule_day(self, day):
    #     classes = []
    #     for i in range(TIMESLOTS, DAYS):
    #         classes.append(slots[])



    def load_schedule():
        room = 'zalen.csv'

        with open(room) as rooms:
            rooms = csv.reader(rooms, delimiter=';')
            next(rooms)

            zaalnummers = []

            # Optional code to visualize data
            for row in rooms:
                zaalnummers.append(row[0])

        print(zaalnummers)

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
    Schedule.print_schedule(0, 10)
