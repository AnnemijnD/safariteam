class Course(object):
    """
    Representation of a course in CollegeClass.
    """

    def __init__(self, name, course_id, lecture, tutorial, practicum, max_students):
        self.name = name
        self.course_id = course_id
        self.lecture = lecture
        self.tutorial = tutorial
        self.practicum = practicum
        self.max_students = max_students
