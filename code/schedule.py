class Schedule(object):
    """
    Representation of a schedule.
    """

    def __init__(self, session, type, room, timeslot, day):
        self.session = session
        self.type = type
        self.room = room
        self.timeslot = timeslot
        self.day = day

    def __str__(self):
        return f'course: {self.session}, type: {self.type}, in room {self.room}'
