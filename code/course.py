from session import Session
import pandas as pd
# from plan import Plan ??


class Course(object):
    """
    Representation of a course in Session.
    """

    def __init__(self, name, course_id, lecture, tutorial, practical, max_students_lecture, max_students_tutorial, max_students_practical):
        self.name = name
        self.course_id = course_id
        self.lecture = lecture
        self.tutorial = tutorial
        self.practical = practical
        self.sessions = self.lecture + self.tutorial + self.practical
        self.session_lecture = self.load_sessions(self.lecture, 'lecture', max_students_lecture)
        self.session_tutorial = self.load_sessions(self.tutorial, 'tutorial', max_students_tutorial)
        self.session_practical = self.load_sessions(self.practical, 'practical', max_students_practical)
        self.sessions_total = self.session_lecture + self.session_tutorial + self.session_practical
        self.mutual_courses = self.load_mutual_courses(self.name)
        self.max_students_lecture = max_students_lecture
        self.max_students_tutorial = max_students_tutorial
        self.max_students_practical = max_students_practical



    def load_sessions(self, int_session, type, max_students):
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
        # Hier ergens ook max_students inladen??
        for i in range(int_session):
            session = Session(self.name, type, max_students)
            sessions.append(session)

        return sessions

        #  DIT IS EEN TEST OM TE KIJKEN OF JE ZO DINGEN VAN EEN COURSE KAN AANROEPEN
    # def __str__(self):
    #     return f"Course number {self.course_id} is {self.name}"

    def load_mutual_courses(self, coursename):

        # Dit moet even ergens anders neergezet worden zodat het niet opnieuw ingeladen wordt de hele tijd!
        # Waarom kan je niet doen: from Plan import plan??
        df = pd.read_csv("../data/tegelijkvolgbaar.csv", delimiter=";")

        mutual_courses = []
        row_counter = 0
        for row in df[coursename]:
            row_counter += 1
            # Append a list of mutual courses
            if row == 'x':
                # print(df.index[row_counter])
                mutual_courses.append(df.index[row_counter - 1])

        return mutual_courses
