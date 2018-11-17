
import random
from session import Session

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7


class Schedule():
    """
    Representation of a class (lecture, tutorial or practicum).
    """

    def __init__(self, name, class_id, type, mutual_courses):
        self.name = name
        self.class_id = class_id
        self.type = type
        self.mutual_courses = mutual_courses
        self.group = []
        self.schedule = [DAYS * [ROOMS * [TIME_SLOTS * ["None"]]]]

    def initialize_schedule(self, courses):
        """
        Initialize schedule using Session().
        """
        pass
