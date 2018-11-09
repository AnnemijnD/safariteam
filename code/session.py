from schedule import Schedule

class Session():
    """
    Representation of a class (lecture, tutorial or practicum).
    """

    def __init__(self, name, class_id, type, mutual_courses):
        self.name = name
        self.class_id = class_id
        self.type = type
        self.mutual_courses = mutual_courses
        self.group = []


if __name__ == "__main__":
    self.schedule = Schedule()

    print(self.schedule)
