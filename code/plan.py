from schedule import Schedule
from course import Course
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
        Loads all the courses.
        """

        course = 'vakken.csv'

        with open(course) as courses:
            courses = csv.reader(courses, delimiter=';')
            # Skip file header
            next(courses)

            # Keep track of course_id with a counter
            id_counter = 0

            # Define every item of the course; each row is a different course
            for row in courses:
                name = row[0]
                lecture = row[1]
                tutorial = row[2]
                max_students = row[3]
                practical = row[4]
                course_id = id_counter

                course = Course(name, course_id, lecture, tutorial, practical, max_students)
                print(course)

                # If you want to know the number of lectures of a specific course:
                print(course.lecture)

                id_counter += 1

            return courses

    # Make a Course object for every course, using the Course class.
    # def make_course():
    #    print()


if __name__ == "__main__":

    # Load all the courses
    Plan.load_courses()
