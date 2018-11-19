# Heuristieken 2018 -- Lesroosters
# Namen: Annemijn, Sanne & Rebecca

import os, sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algoritmes"))

from constraint import Constraint
import switch
from course import Course
from session import Session
from schedule import Schedule
import csv
import random
import time
import pandas as pd
from IPython.display import HTML

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
MAX_MALUSPOINTS = 0


class Plan():
    """
    Main scripts to make a schedule.
    """

    def __init__(self):
        pass

    def load_courses(self):
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

                if row[3].isdigit():
                    max_students_tutorial = int(row[3])
                else:
                    max_students_tutorial = 'nvt'
                if row[5].isdigit():
                    max_students_practical = int(row[5])
                else:
                    max_students_practical = 'nvt'
                max_students_lecture = int(row[6])

                # Use Course class to create objects for every course
                course = Course(name, course_id, lecture, tutorial, practical, max_students_lecture, max_students_tutorial, max_students_practical)
                courses_list.append(course)
                # Count id_course
                id_counter += 1

            return courses_list

    def load_rooms(self):
        """
        loads all the rooms from a csv file.
        """
        room = 'data/zalen.csv'

        with open(room) as rooms:
            rooms = csv.reader(rooms, delimiter=';')
            next(rooms)
            roomnumbers = []
            for row in rooms:
                string = f'{row[0]} (max: {row[1]})'
                roomnumbers.append(string)

        return roomnumbers

    def initialize_schedule(self, courses):
        """
        Initialize schedule using Session().
        Willen we eigenlijk in Schedule class zelf hebben
        """

        sessions = []
        session_list = []
        lecture_sessions = []
        other_sessions = []
        empty_sessions = []

        for course in courses:
            session_list = session_list + course.sessions_total

        # Put every session into schedule
        for i in range(SLOTS):
            try:
                name = session_list[i].name
            except IndexError:
                name = ' '
            try:
                type = session_list[i].type
            except IndexError:
                type = ' '
            try:
                max_students = session_list[i].max_students
            except IndexError:
                max_students = 'nvt'

            session = Session(name, type, max_students)

            # Get all the lectures
            if session.type == "lecture":
                lecture_sessions.append(session)
            elif session.type == "tutorial" or session.type == "practical":
                other_sessions.append(session)
            sessions.append(session)


        # shuffle de lectures zodat ze random zijn
        # Make copy of sessions and shuffle
        lectures = lecture_sessions[:]
        others = other_sessions[:]
        random.shuffle(lectures)
        random.shuffle(other_sessions)

        # TODO: lijst maken met eerst grote vakken!!

        total = []
        total = lectures + other_sessions


        # Maak lege sessies aan om lege cellen mee op te vullen
        # Dit stukje wordt gebruikt in de nested for loop waarbij aan elke cel
        # een sessie wordt meegegeven.
        for i in range(SLOTS):
            name = ' '
            type = ' '
            max_students = ' '
            session = Session(name, type, max_students)
            # session = Session(name, type, room, timeslot, day)
            empty_sessions.append(session)


        schedule = [[[['None'] for i in range(ROOMS)] for i in range(TIME_SLOTS)] for i in range(DAYS)]

        # Je geeft dus aan deze functie een leeg schedule mee en de sessions waarmee
        # schedule gevuld moet worden. Doordat lectures en other_sessions nu gescheieden
        # zijn kunnen eerst de lectures gevuld worden en daarna pas de rest
        plan.fill_schedule(schedule, total, other_sessions, empty_sessions, courses)
        plan.schedule_counter += 1

        return schedule, total, other_sessions, empty_sessions


    def fill_schedule(self, schedule, lectures, other_sessions, empty_sessions, courses):
        """
        Fill empty schedule with sessions. Function will begin to fill all the lectures
        and will go on to fill other sessions.
        """

        # Gebruik nested for loop om elke cel een session te gegen.
        # Je geeft hierbij een lijst met sessies mee aan de functie get_session
        # De lijst met sessies is al gemaakt in initialize_schedule()

        # Vul eerst met lege sessions
        counter = 0
        for b in range(DAYS):
            for c in range(TIME_SLOTS):
                for d in range(ROOMS):
                    schedule[b][c][d] = empty_sessions[counter]

        # verdelen over dagen als hard constraint
        for e in range(len(lectures)):

            for course in courses:
                if lectures[e].name == course.name:
                    mutual_courses_session = course.mutual_courses
            found = False
            for b in range(DAYS):
                location = []
                slots_allowed = True
                for c in range(TIME_SLOTS):
                    rooms_allowed = True
                    # availibility = True

                    for d in range(ROOMS):

                        # if the slot in the schedule is empty
                        if schedule[b][c][d].name == ' ':
                            # print("in if1")
                            if not bool(location):
                                # print("in if1.1")
                                location.append(c)
                                location.append(d)

                        elif lectures[e].name == schedule[b][c][d].name:
                            slots_allowed = False
                            break

                        elif schedule[b][c][d].name in mutual_courses_session:
                            rooms_allowed = False
                            break

                    if not slots_allowed:
                        break

                    if rooms_allowed and bool(location):

                        schedule[b][location[0]][location[1]] = lectures[e]
                        found = True
                        break



                if slots_allowed and bool(location):

                        # print("in if2")
                    schedule[b][location[0]][location[1]] = lectures[e]
                    found = True
                    break


            if not found:
                print(e)
                print("not found")
                print(lectures[e])
                return schedule
                plan.schedule_counter += 1
                plan.initialize_schedule(plan.courses)

        if found:
            return schedule

        else:
            plan.schedule_counter += 1
            plan.initialize_schedule(plan.courses)



        # lecture_counter = 0
        # counter = 0
        # day_counter = 0
        # timeslot_counter = 0
        # for b in range(DAYS):
        #     for c in range(TIME_SLOTS):
        #         for d in range(ROOMS):
        #
        #             # if the slot in the schedule is empty
        #             if schedule[b][c][d].name == ' ':
        #
        #                 #  loop through the rooms
        #                 for e in schedule[b][c]:
        #
        #                     # check if the same course is already in that slot
        #                     if lectures[lecture_counter].name in e.name:
        #                         print(lectures[lecture_counter].name in e.name)
        #                         c += 1
        #                         timeslot_counter += 1
        #                         if c > 3:
        #                             b += 1
        #                             day_counter += 1
        #                             c = 0
        #
        #                         # makes a new schedule if it failed
        #                         if b > 4:
        #                             plan.initialize_schedule(plan.courses)
        #
        #                 # set the session in the schedule
        #                 schedule[b][c][d] = lectures[lecture_counter]
        #                 lecture_counter += 1
        #                 # QUINTEN!: is dit sneller in een if statement?
        #                 d += 1
        #                 d %= 7
        #
        #                 #  returns to the previous timeslot/day in the loop if it skipped one
        #                 if timeslot_counter > 0:
        #                     c -= timeslot_counter
        #                     timeslot_counter = 0
        #                 if day_counter > 0:
        #                     b -= day_counter
        #                     day_counter = 0
        #
        #                 # if all the sessions are scheduled return schedule
        #                 if lecture_counter is len(lectures):
        #                     return schedule

    def random_schedule(self, schedule, sessions):
        """
        Generates a random schedule. Assigns every session to a random timeslot.
        # Hou bij welke random nummers al geweest zijn. De while loop
        # Zorgt ervoor dat er een random nummer wordt gemaakt die nog
        # niet is geweest.
        """

        for i in range(SLOTS):
            rand = random.randint(0, SLOTS - 1)
            while rand in random_numbers:
                rand = random.randint(0, SLOTS - 1)
            # Hier wordt de session in dat timeslot gezet met een random nummer
            schedule[rand] = sessions[i]
            plan.random_numbers.append(rand)

        # Keep track of how many schedules were made
        plan.schedule_counter += 1

    def get_session(self, sessions):
        """
        Generates a random schedule. Assigns every session to a random timeslot.
        # Hou bij welke random nummers al geweest zijn. De while loop
        # Zorgt ervoor dat er een random nummer wordt gemaakt die nog
        # niet is geweest.
        """

        for i in range(len(sessions)):
            rand = random.randint(0, (len(sessions)) - 1)
            while rand in plan.random_numbers:
                rand = random.randint(0, len(sessions) - 1)
                plan.random_numbers.append(rand)

        return sessions[rand]

    def load_individual(self):
        """
        Loads individual student courses.
        """
        # Use encoding='iso-8859-1' to ensure that content is accessible as bytes
        with open('data/studentenenvakken.csv', encoding='iso-8859-1') as wishes:
            wishes = csv.reader(wishes, delimiter=';')

            # Optional code to visualize data
            for row in wishes:
                print(row)

    def save_html(self, schedule, rooms):
        """
        Print into html to visualize schedule.
        """

        df = pd.DataFrame(schedule)
        pd.set_option('display.max_colwidth', 350)
        df.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
        df.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # Transpose rows and columns
        df = df.T

        # Stel de column namen vast
        i = 0
        tags = df['Monday'].apply(pd.Series)
        tags.columns = [rooms[i], rooms[i+1], rooms[i+2], rooms[i+3], rooms[i+4], rooms[i+5], rooms[i+6]]
        tuesday = df['Tuesday'].apply(pd.Series)
        tuesday.columns = [rooms[i], rooms[i+1], rooms[i+2], rooms[i+3], rooms[i+4], rooms[i+5], rooms[i+6]]
        wednesday = df['Wednesday'].apply(pd.Series)
        wednesday.columns = [rooms[i], rooms[i+1], rooms[i+2], rooms[i+3], rooms[i+4], rooms[i+5], rooms[i+6]]
        thursday = df['Thursday'].apply(pd.Series)
        thursday.columns = [rooms[i], rooms[i+1], rooms[i+2], rooms[i+3], rooms[i+4], rooms[i+5], rooms[i+6]]
        friday = df['Friday'].apply(pd.Series)
        friday.columns = [rooms[i], rooms[i+1], rooms[i+2], rooms[i+3], rooms[i+4], rooms[i+5], rooms[i+6]]

        html_string = '''
        <html>
          <head><title>Schedule</title></head>
          <link rel="stylesheet" type="text/css" href="data/style.css" href="https://www.w3schools.com/w3css/4/w3.css"/>
          <body>
            {table}
          </body>
        </html>.
        '''

        with open('resultaten/schedule.html', 'w') as f:
            f.write(html_string.format(table=df.to_html(classes='style')))
            f.write("Monday:")
            f.write(html_string.format(table=tags.to_html(classes='style')))
            f.write("Tuesday")
            f.write(html_string.format(table=tuesday.to_html(classes='style')))
            f.write("Wednesday")
            f.write(html_string.format(table=wednesday.to_html(classes='style')))
            f.write("Thursday")
            f.write(html_string.format(table=thursday.to_html(classes='style')))
            f.write("Friday")
            f.write(html_string.format(table=friday.to_html(classes='style')))


if __name__ == "__main__":

    then = time.time()

    # Load all the courses and sessions
    plan = Plan()
    plan.random_numbers = []
    plan.schedule_counter = 0
    plan.courses = plan.load_courses()
    schedule, lectures, other_sessions, empty_sessions = plan.initialize_schedule(plan.courses)
    rooms = plan.load_rooms()

    # Switch sessions
    schedule = switch.switch_session(schedule)


    # Make a html file for the schedule
    plan.save_html(schedule, rooms)

    now = time.time()
    print("It took:", now - then, "seconds.")
    print("Succesfully made", plan.schedule_counter, "schedule(s) until the right was found.")

    # Test get_day en get_slot
    # print(plan.get_day(schedule, 0))
    # print(Constraint.session_spread_check(schedule))
