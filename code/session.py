
SLOTS = 140


class Session(object):
    """
    Representation of a schedule.
    """

    def __init__(self, name, type):
        self.name = name
        self.type = type
        # self.room = room
        # self.timeslot = timeslot
        # self.day = day

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
<<<<<<< HEAD
        return f'{self.name}:{self.type}'
=======
        return f'{self.name}, {self.type}'
>>>>>>> 58745f2834a67ed9dacccaf35e29ba4dab7cfbcb
