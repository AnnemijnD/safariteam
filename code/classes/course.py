from session import Session
from mutual_course import MutualCourse
import pandas as pd
import math


class Course(object):
    """
    Representation of a course in Session.
    """

    def __init__(self, name, course_id, lecture, tutorial, practical, max_students_lecture, max_students_tutorial, max_students_practical, expected_students):
        self.name = name
        self.course_id = course_id
        self.lecture = lecture
        self.tutorial = tutorial
        self.practical = practical
        self.sessions = self.lecture + self.tutorial + self.practical
        self.session_lecture = self.load_sessions(self.lecture, 'lecture', max_students_lecture, expected_students)
        self.session_tutorial = self.load_sessions(self.tutorial, 'tutorial', max_students_tutorial, expected_students)
        self.session_practical = self.load_sessions(self.practical, 'practical', max_students_practical, expected_students)
        # print(self.session_practical)
        self.sessions_total = self.session_lecture + self.session_tutorial + self.session_practical
        # Mutual courses moeten objecten worden.
        self.mutual_courses = self.load_mutual_courses(self.name)
        self.max_students_lecture = max_students_lecture
        self.max_students_tutorial = max_students_tutorial
        self.max_students_practical = max_students_practical
        self.expected_students = expected_students

        # self.mutual_courses_object = []

        # Make an object for every course in the mutual_courses list
        # for course in self.mutual_courses:
        #     self.mutual_courses_object.append(Course())


    def load_sessions(self, int_session, type, max_students, expected_students):
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
        sessions_with_groups = []
        group_id = 0

        # Make session for each lecture, tutorial and practical.

        for i in range(int_session):
            # Hou de group_id bij
            # Als verwachte studenten groter is dan max_studenten , maak dan nog zoveel sessions aan
            # print(group_id)


            if expected_students > max_students:
                group_count = math.ceil(float(expected_students/max_students))
                # Set a counter for group_id
                group_id = 0
                # make a session for every group
                for j in range(group_count):
                    session = Session(self.name, type, max_students, group_id)
                    sessions_with_groups.append(session)
                    group_id += 1
            else:
                group_id = 0
                session = Session(self.name, type, max_students, group_id)
                sessions_with_groups.append(session)


            session = Session(self.name, type, max_students, group_id)
            sessions.append(session)

        return sessions

        #  DIT IS EEN TEST OM TE KIJKEN OF JE ZO DINGEN VAN EEN COURSE KAN AANROEPEN
    # def __str__(self):
    #     return f"Course number {self.course_id} is {self.name}"

    def load_mutual_courses(self, coursename):

        # Dit moet even ergens anders neergezet worden zodat het niet opnieuw ingeladen wordt de hele tijd!
        # Waarom kan je niet doen: from Plan import plan??
        df = pd.read_csv("data/tegelijkvolgbaar.csv", delimiter=";")

        mutual_courses = []
        mutual_courses_object = []
        row_counter = 0
        for row in df[coursename]:
            row_counter += 1
            # Append a list of mutual courses
            if row == 'x':
                # print(df.index[row_counter])
                mutual_courses.append(df.index[row_counter - 1])
                mutual_courses_object.append(MutualCourse(df.index[row_counter - 1]))

        return mutual_courses
