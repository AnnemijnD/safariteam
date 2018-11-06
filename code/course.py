import csv
import os

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


            print(course_dict)
