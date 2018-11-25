# Heuristieken 2018 -- Lesroosters
# Namen: Annemijn, Sanne & Rebecca

import os, sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algoritmes"))

from constraint import Constraint
import loaddata
from course import Course
from session import Session
from schedule import Schedule
import switch
import firstalgorithm
import csv
import random
import time
import pandas as pd
from IPython.display import HTML
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
MAXMALUSPOINTS = 0
MAXSCHEDULEPOINTS = 39


class Plan():
    """
    Main script to make a schedule.
    """

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

            group_id = 'nvt'

            session = Session(name, type, max_students, group_id)

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

        # Maak lege sessies aan om lege cellen mee op te vullen
        # Dit stukje wordt gebruikt in de nested for loop waarbij aan elke cel
        # een sessie wordt meegegeven.
        for i in range(140-72):
            name = ' '
            type = ' '
            max_students = ' '
            group_id = 'nvt2'
            session = Session(name, type, max_students, group_id)
            # session = Session(name, type, room, timeslot, day)
            empty_sessions.append(session)

        # De lijst met totale sessies bestaat dus uit een lijst met eerst
        # Hoorcolleges, daarna de andere sessies en is opgevuld tot 140 met lege sessies
        total = []
        total = lectures + other_sessions

        schedule = [[[[None] for i in range(ROOMS)] for i in range(TIME_SLOTS)] for i in range(DAYS)]


        # Je geeft dus aan deze functie een leeg schedule mee en de sessions waarmee
        # schedule gevuld moet worden. Doordat lectures en other_sessions nu gescheieden
        # zijn kunnen eerst de lectures gevuld worden en daarna pas de rest

        # plan.fill_schedule(schedule, total, other_sessions, empty_sessions, courses)


        # VOOR NU: Even een random rooster
        schedule = plan.random_schedule(schedule, total)
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
                    # Lijst van elke lecture die er op dat moment is
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


    def random_schedule(self, schedule, sessions):
        """
        Generates a random schedule. Assigns every session to a random timeslot.
        # Hou bij welke random nummers al geweest zijn. De while loop
        # Zorgt ervoor dat er een random nummer wordt gemaakt die nog
        # niet is geweest.
        """

        # Maak een 1D lijst van schedule
        flatten = np.array(schedule, dtype=object).flatten()

        random_numbers = []

        for i in range(len(sessions)):
            rand = random.randint(0, SLOTS - 1)
            while rand in random_numbers:
                rand = random.randint(0, SLOTS - 1)
            random_numbers.append(rand)
            flatten[rand] = sessions[i]

        # Convert back to 3D list
        schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

        # Keep track of how many schedules were made
        plan.schedule_counter += 1

        return schedule

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
          <link rel="stylesheet" type="text/css" href="style.css" href="https://www.w3schools.com/w3css/4/w3.css"/>
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

    def makeplot(self, points):
        """
        Plots a graph of all the points on the y-axis and number of schedules
        on the x-axis.
        """
        plt.plot(points)
        plt.ylabel("Points (max = 68)")
        plt.show()

    def end(self):
        """
        Prints text to tell user how many schedules were made and how long it took to make
        """
        print("SUCCES!!")
        print("It took:", round(time.time() - plan.then, 3), "seconds, = ", round((time.time() - plan.then) / 60, 3), "minutes.")
        print("Made", plan.schedule_counter, "schedule(s) until the 'right' was found.")
        print(Constraint.lecture_first(schedule, plan.courses)[1], "correctly placed lectures.")
        print(plan.own_session_points, "out of 72 sessions were placed in a different timeslot.")
        print("Spread points:", Constraint.session_spread_check(schedule, plan.courses), "out of 400.")


if __name__ == "__main__":

    # Load all the courses and sessions
    plan = Plan()
    plan.then = time.time()
    print("Loading...")
    plan.random_numbers = []
    plan.schedule_counter = 0
    plan.courses = loaddata.load_courses()
    schedule, lectures, other_sessions, empty_sessions = plan.initialize_schedule(plan.courses)
    rooms = loaddata.load_rooms()
    plan.own_session_points = 0

    # schedule, points, plan.schedule_counter, plan.own_session_points = firstalgorithm.algorithm(schedule, plan.courses, plan.schedule_counter)

    # Constraint.mutual_courses_check(schedule, plan.courses)
    # print(Constraint.own_sessions_check(schedule, plan.courses))
    # Constraint.all_constraints(schedule, plan.courses)
    # Constraint.session_spread_check(schedule, plan.courses)

    # Print the end-text
    plan.end()
    # Make a plot of the points
    try:
        plan.makeplot(points)
    except:
        print("No points to plot for now.")
    # Make a html file for the schedule
    plan.save_html(schedule, rooms)
