from course import Course
from session import Session
import csv


class Plan():

    def __init__(self):
        pass

    def load_courses():
        """
        Loads all the courses. Used by Session().
        """

        # THIS IS HARDCODING, MUST BE OPTIMIZED!
        course = 'vakken.csv'

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
                lecture = row[1]
                tutorial = row[2]
                max_students = row[3]
                practical = row[4]
                course_id = id_counter

                # Use Course class to create objects for every course
                course = Course(name, course_id, lecture, tutorial, practical, max_students)
                courses_list.append(course)
                # Count id_course
                id_counter += 1

                # For example: if you want to know the number of lectures of a specific course:
                # print(course.lecture)

            return courses_list

    def load_sessions():
        """
        Loads all the session type for every course. Used by Schedule().
        """
        # Pseudocode to create all the sessions:
        #
        # For every course:
        #   For every session type (lectures, tutorials, practicals)
        #       Calculate number of sessions for this course
        #       Make a Session(), input = (self, name, class_id, type, mutual_courses, group):
        # VOLGENS MIJ MOET MUTUAL_COURSES AL BIJ LOAD_COURSES IN DE COURSE GEZET WORDEN!

        # Zet alle sessions in een lijst
        sessions = []

        for course in Plan.load_courses():
            name = course.name
            class_id = course.course_id
            mutual_courses = []
            group = []

            for row in range(0, int(course.lecture)):
                type = 'lecture'
                session = Session(name, class_id, type, mutual_courses, group)
                sessions.append(session)

            for row in range(0, int(course.tutorial)):
                type = 'tutorial'
                session = Session(name, class_id, type, mutual_courses, group)
                sessions.append(session)

            for row in range(0, int(course.practical)):
                type = 'practical'
                session = Session(name, class_id, type, mutual_courses, group)
                sessions.append(session)

        # Nu zijn er bijvoorbeeld voor het vak 'Architectuur en computerorganisatie'
        # twee sessions aangemaakt met hoorcolleges; controleer met print-statement
        print(sessions[3].name)
        print(sessions[4].name)

        # Succesfully created 72 sessions!
        print(len(sessions))


if __name__ == "__main__":

    # Load all the courses
    Plan.load_courses()
    Plan.load_sessions()
