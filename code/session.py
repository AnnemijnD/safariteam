
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
        return iter([self.session, self.type, self.room, self.timeslot])

    def __repr__(self):
        return str(self.session)

    def __str__(self):
        return f'course: {self.session}, type: {self.type}, in room {self.room}'
