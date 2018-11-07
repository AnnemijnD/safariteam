from schedule import Schedule
from course import Course
from session import Session
import csv


class Plan():

    def __init__(self):
        pass

    def plan(self):

        schedule = Schedule([None] * 140)
        schedule.print_schedule(0, 2)
        schedule.load_schedule()

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
        # Create all the sessions:
        #
        # For every course:
        #   For every session type (lectures, tutorials, practicals)
        #       Calculate number of sessions for this course
        #print(Plan.load_courses().name)

        for course in Plan.load_courses():
            for lecture in course.lecture:
                print(lecture)
            for tutorial in course.tutorial:
                print(tutorial)
            for practical in course.practical:
                print(practical)



if __name__ == "__main__":

    # Load all the courses
    Plan.load_courses()
    Plan.load_sessions()
