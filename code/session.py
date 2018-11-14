
SLOTS = 140


class Session(object):
    """
    Representation of a schedule.
    """

    def __init__(self, session, type, room, timeslot, day):
        self.session = session
        self.type = type
        self.room = room
        self.timeslot = timeslot
        self.day = day

    def __iter__(self):
        """
        Enables a list of objects to be iterated one element at a time.
        """
        return iter([self.session, self.type, self.room, self.timeslot, self.day])

    def __repr__(self):
        """
        Represents an object when it is printed.
        """
        return str([self.session, self.type])

    def __getitem__(self, day):
        return self.day

    def __str__(self):
        return f'{self.session}, {self.type}'
