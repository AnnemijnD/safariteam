import csv


class Course(object):
    """
    Representation of a course in CollegeClass.
    """

    def __init__(self, name, course_id, lecture, tutorial, practical, max_students):
        self.name = name
        self.course_id = course_id
        self.lecture = lecture
        self.tutorial = tutorial
        self.practical = practical
        self.max_students = max_students
        self.session_lecture = session_lecture
        self.session_tutorial = session_turorial
        self.sessoin_practical = session_practical




    # Zonder de __str__ methode krijg je dus alleen <object at position 0x107b5e4...>
    def __str__(self):
        return f"Course number {self.course_id} is {self.name}"
