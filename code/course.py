from session import Session


class Course(object):
    """
    Representation of a course in Session.
    """

    def __init__(self, name, course_id, lecture, tutorial, practical, max_students):
        self.name = name
        self.course_id = course_id
        self.lecture = lecture
        self.tutorial = tutorial
        self.practical = practical
        self.max_students = max_students
        self.session_lecture = self.load_sessions(self.lecture, 'lecture')
        self.session_tutorial = self.load_sessions(self.tutorial, 'tutorial')
        self.session_practical = self.load_sessions(self.practical, 'practical')
        self.sessions_total = self.session_lecture + self.session_tutorial + self.session_practical
        # dit is even mega lelijk maar dat regel ik later, ik maak hier een extra lijst

    def load_sessions(self, int_session, type):
        """
        Loads all the session types for every course.

        # Pseudocode to create all the sessions:
        #
        # For every course:
        #   For every session type (lectures, tutorials, practicals)
        #       Make a Session(). input of Session = (self, name, class_id, type, mutual_courses, group):
        #
        # IK DENK DAT MUTUAL_COURSES AL BIJ LOAD_COURSES IN DE COURSE GEZET WORDEN! denk ik ook x A
        # Nog geen idee hoe we group moeten definiëren... <-- group hoeft nog niet :))) <<-- Oke thanks Sanne :)
        """

        mutual_courses = []
        sessions = []

        # Make session for each lecture, tutorial and practical.
        for i in range(int_session):
            session = Session(self.name, self.course_id, type, mutual_courses)
            sessions.append(session)

        return sessions

    def __str__(self):
        return f"Course number {self.course_id} is {self.name}"
