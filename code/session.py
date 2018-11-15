
SLOTS = 140


class Session(object):
    """
    Representation of a schedule.
    """

    def __init__(self, name, type, room, timeslot, day):
        self.name = name
        self.type = type
        self.room = room
        self.timeslot = timeslot
        self.day = day

    def __iter__(self):
        """
        Enables a list of objects to be iterated one element at a time.
        """
        return iter([self.name, self.type, self.room, self.timeslot, self.day])

    def __repr__(self):
        """
        Represents an object when it is printed.
        """
        return str([self.name, self.type])

    def __getitem__(self, day):
        return self.day

    def __str__(self):        
        return f'{self.name}, {self.type}'
