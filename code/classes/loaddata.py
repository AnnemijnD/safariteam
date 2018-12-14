"""
Loads all the original data from csv files from the
data folder.
"""

from course import Course
from room import Room

import csv
import pandas as pd


def load_courses():
    """
    Loads all the courses from a csv file.
    """

    course = 'data/vakken.csv'

    with open(course) as courses:
        courses = csv.reader(courses, delimiter=';')
        # Skip file header
        next(courses)

        # Keep track of course_id with a counter
        id_counter = 0
        # Make a list of all the course objects
        courses_list = []

        # Define every item of the course; each row is a different course
        for row in courses:
            name = row[0]
            lecture = int(row[1])
            tutorial = int(row[2])
            practical = int(row[4])
            course_id = id_counter
            expected_students = int(row[6])

            if row[3].isdigit():
                max_students_tutorial = int(row[3])
            else:
                max_students_tutorial = 'nvt'
            if row[5].isdigit():
                max_students_practical = int(row[5])
            else:
                max_students_practical = 'nvt'
            max_students_lecture = int(row[6])

            df = pd.read_csv("data/tegelijkvolgbaar.csv", delimiter=";")

            # Use Course class to create objects for every course
            course = Course(name, course_id, lecture, tutorial, practical,
                            max_students_lecture, max_students_tutorial,
                            max_students_practical, expected_students, df)
            courses_list.append(course)

            # Count id_course
            id_counter += 1

        return courses_list
        

def load_rooms():
    """
    loads all the rooms from a csv file.
    """
    room = 'data/zalen.csv'

    with open(room) as rooms:
        rooms = csv.reader(rooms, delimiter=';')
        next(rooms)
        roomnumbers = []
        room_id = 0
        for row in rooms:
            room = Room(row[0], room_id, int(row[1]))
            roomnumbers.append(room)
            room_id += 1

    return roomnumbers


def load_individual():
    """
    Loads individual student courses.
    """
    # Use encoding='iso-8859-1' to ensure that content is accessible as bytes
    with open('data/studentenenvakken.csv', encoding='iso-8859-1') as wishes:
        wishes = csv.reader(wishes, delimiter=';')

        # Optional code to visualize data
        for row in wishes:
            print(row)
