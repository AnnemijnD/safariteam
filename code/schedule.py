import loaddata
import csv

class Schedule(object):
    """
    Representation of a schedule.
    """

    # temporarily set slot to None, can be removed when class is used by other class
    slot = None

    def __init__(self, slot):
        self.slot = slot

    def print_schedule(self):
        print(self.slot)
        #if day == 'monday':
        #    print(self.slots)


if __name__ == "__main__":

    room = 'zalen.csv'

    with open(room) as rooms:
        rooms = csv.reader(rooms, delimiter=';')
        next(rooms)

        zaalnummers = []

        # Optional code to visualize data
        for row in rooms:
            zaalnummers.append(row[0])
        print(zaalnummers)


    # Make schedule of 140 slots, can be changed to 175 when timeslot 17 - 19 is used
    Schedule = Schedule(slot = [zaalnummers] * 140)
    Schedule.print_schedule()
