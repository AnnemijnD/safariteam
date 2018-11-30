
SLOTS = 140


class Session(object):
    """
    Representation of a schedule.
    """

    def __init__(self, name, type, max_students, session_id, group_id):
        self.index = 0
        self.name = name
        self.type = type
        self.max_students = max_students
        self.session_id = session_id
        self.group_id = group_id
        self.course_object = None


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
            return f'{self.name} {self.type}, group: {(chr(self.group_id + 65))}, ({self.max_students} students)'
