import csv


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

    # Zonder de __str__ methode krijg je dus alleen <object at position 0x107b5e4...>
    def __str__(self):
        return f"Course number {self.course_id} is {self.name}"


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

# <<<<<<< HEAD
# =======
        # vul de hoeveelheid sessions als dat er hc's zijn
            # return al deze sessions

        # vul
# >>>>>>> 94f0675844f066be716f88dd323166d4285aa430
            print(course_dict)
