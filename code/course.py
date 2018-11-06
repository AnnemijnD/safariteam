import csv
import os

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


    if __name__ == "__main__":


        course = 'vakken.csv'

        with open(course) as courses:
            courses = csv.reader(courses, delimiter=';')
            # Skip header
            next(courses)

            course_dict = {}
            counter = 0

            # Optional code to visualize data
            for row in courses:
                course_dict.update({counter: row[0]})
                counter += 1

        # vul de hoeveelheid sessions als dat er hc's zijn
            # return al deze sessions

        # vul
            print(course_dict)
