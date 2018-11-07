import loaddata
import csv
from group import Group

TIMESLOTS = 140
# DAYS = 7

class Schedule(object):
    """
    Representation of a schedule.
    """

    def __init__(self, session, type, room):
        self.session = session
        self.type = type
        self.room = room
        #self.empty_schedule = [None] * TIMESLOTS

        # Initialize schedule
        #for item in range(0, TIMESLOTS):
        #    self.empty_schedule[item] = session, type, room

    def load_rooms():
        room = 'zalen.csv'

        with open(room) as rooms:
            rooms = csv.reader(rooms, delimiter=';')
            next(rooms)

            zaalnummers = []

            # Optional code to visualize data
            for row in rooms:
                zaalnummers.append(row[0])
                
        return zaalnummers


    def __str__(self):
        return f'course: {self.session}, type: {self.type}, in room {self.room}'









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
