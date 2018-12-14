from session import Session
import math


class Course(object):
    """
    Representation of a course in Session.
    """

    def __init__(self, name, course_id, lecture, tutorial, practicum, max_students_lecture, max_students_tutorial, max_students_practicum, expected_students, df):
        self.name = name
        self.course_id = course_id
        self.lecture = lecture
        self.tutorial = tutorial
        self.practicum = practicum
        self.df = df
        self.sessions = self.lecture + self.tutorial + self.practicum
        self.session_lecture = self.load_sessions(self.lecture, 'lecture', max_students_lecture, expected_students)
        self.session_tutorial = self.load_sessions(self.tutorial, 'tutorial', max_students_tutorial, expected_students)
        self.session_practicum = self.load_sessions(self.practicum, 'practicum', max_students_practicum, expected_students)
        self.sessions_total = self.session_lecture + self.session_tutorial + self.session_practicum
        self.mutual_courses = self.load_mutual_courses(self.name, self.df)
        self.max_students_lecture = max_students_lecture
        self.max_students_tutorial = max_students_tutorial
        self.max_students_practicum = max_students_practicum
        self.expected_students = expected_students

    def load_sessions(self, int_session, type, max_students, expected_students):
        """
        Loads all the session types for every course.
        """
        
        sessions_with_groups = []
        group_id = 0

        if type == 'lecture':
            session_id = 0
        elif type == 'tutorial':
            session_id = self.lecture
        else:
            session_id = self.lecture + self.tutorial

        # Make session for each lecture, tutorial and practicum.
        for i in range(int_session):
            # Make groups for the number of students per course
            if expected_students > max_students:
                group_count = math.ceil(float(expected_students/max_students))
                group_id = 1
                # Make a session for every group
                for j in range(group_count):
                    session = Session(self.name, type, max_students, session_id, group_id)
                    sessions_with_groups.append(session)
                    group_id += 1
                session_id += 1

            else:
                group_id = 0
                session = Session(self.name, type, max_students, session_id, group_id)
                sessions_with_groups.append(session)
                session_id += 1

        return sessions_with_groups


    def load_mutual_courses(self, coursename, df):
        """
        Loads all the mutual per course. Input is a course name and
        a pandas dataframe including all the mutual courses,
        output is a list of mutual courses for this course.
        """

        mutual_courses = []
        row_counter = 0
        for row in df[coursename]:
            row_counter += 1
            # Append a list of mutual courses
            if row == 'x':
                mutual_courses.append(df.index[row_counter - 1])

        return mutual_courses
