
SLOTS = 140


class Session(object):
    """
    Representation of a schedule.
    """

    def __init__(self, name, type, max_students):
        self.name = name
        self.type = type
        self.max_students = max_students

    def __iter__(self):
        """
        Enables a list of objects to be iterated one element at a time.
        """
        return iter([self.name, self.type, self.room, self.timeslot, self.day])

    def __repr__(self):
        """
        Represents an object when it is printed.
        """
        return self.name

    def __getitem__(self, day):
        return self.day

    def __str__(self):
        if self.max_students == " ":
            return f'{self.name} {self.type}'
        else:
            return f'{self.name} {self.type}, ({self.max_students} students)'
