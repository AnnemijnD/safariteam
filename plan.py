# Heuristieken 2018 -- Lesroosters
# Namen: Annemijn, Sanne & Rebecca

import os, sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algoritmes"))

from constraint import Constraint
import switch
import loaddata
from course import Course
from session import Session
from schedule import Schedule
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

    def makeplot(self,points):

        plt.plot(points)
        plt.ylabel("Points (out of 39)")
        plt.show()


    def end(self):
        """
        Prints text to tell user how many schedules were made and how long it took to make
        """

        print("It took:", round(time.time() - plan.then, 3), "seconds.")
        print("Succesfully made", plan.schedule_counter, "schedule(s) until the 'right' was found.")

        # Test get_day en get_slot
        print("Bonus points:", Constraint.session_spread_check(schedule, plan.courses), "out of 400.")


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
    plan.points = []

    # -----------------------------------------------------------------------------------
    ### SORRY JONGENS DIT MOET IN ALGORITMEN STAAN, (maar wat voor algoritme is dit...?)
    #
    # schedule = switch.switch_session(schedule, 5)
    # # Onthou dit rooster
    # save_schedule = schedule
    # save_schedule2 = schedule
    #
    # while Constraint.lecture_first(schedule, plan.courses)[1] < 11:
    #     save_schedule = schedule
    #     plan.points.append(Constraint.lecture_first(schedule, plan.courses)[1])
    #     # Maak nieuw rooster en kijk of deze beter is
    #     schedule_test = switch.switch_session(save_schedule, 100)
    #     plan.schedule_counter += 1
    #
    #     # Check of het nieuwe rooster meer punten heeft dan het vorige rooster
    #     if Constraint.lecture_first(schedule_test, plan.courses)[1] >= Constraint.lecture_first(save_schedule, plan.courses)[1]:
    #         # Als het aantal punten groter is, accepteer dit rooster en ga hiermee door.
    #         schedule = schedule_test
    #
    #     else:
    #         schedule = save_schedule
    #         plan.points.append(Constraint.lecture_first(schedule, plan.courses)[1])
    #
    #     # Als het algoritme vast zit, ga dan weer naar een random rooster
    #     if plan.schedule_counter % 1000 == 0:
    #         # plan.makeplot(plan.points)
    #         schedule = save_schedule2


    # --------------------------------------------------------------------------------
    # Begin met een rooster
    save_schedule = schedule
    # Ga door tot de punten van schedule groter zijn dan 11 ofzo
    while Constraint.lecture_first(schedule, plan.courses)[1] < 39:
        plan.points.append(Constraint.lecture_first(schedule, plan.courses)[1])
        plan.schedule_counter += 1
        # Bewaar het eerste rooster
        schedule1 = schedule
        # Maak een nieuw roosters
        # 5 dingen per keer switchen gaat iets sneller
        schedule2 = switch.switch_session(schedule, 5)
        # Als deze hetzelfde aantal of meer punten heeft, accepteer dit rooster dan.
        if Constraint.lecture_first(schedule2, plan.courses)[1] >= Constraint.lecture_first(schedule1, plan.courses)[1]:
            # Accepteer dit rooster
            schedule = schedule2
        # Als deze minder punten heeft, ga dan terug naar het vorige rooster
        else:
            schedule = schedule1
        # Als het rooster 10 punten verder is, bewaar het rooster dan om er later op terug te kunnen komen
        if Constraint.lecture_first(schedule, plan.courses)[1] % 10 == 0:
            schedule_10_points = schedule
        # Als het rooster vast blijft zitten, ga dan terug naar het originele rooster of naar het bewaarde rooster.
        if plan.schedule_counter % 1500 == 0:
            if Constraint.lecture_first(schedule, plan.courses)[1] % 10 == 0:
                if schedule_10_points:
                    schedule = schedule_10_points
                else:
                    schedule = save_schedule






    print(Constraint.lecture_first(schedule, plan.courses)[1])
    # R: Komt nooit hoger dan 180 !??? HoeE KAN DAT? Super raar
    # while Constraint.lecture_first(schedule, plan.courses) == False:
    #     # Switch sessions: input is a schedule and number of sessions to be swapped
    #     schedule = switch.switch_session(schedule, 30)
    #     plan.schedule_counter += 1

    # Constraint.mutual_courses_check(schedule, plan.courses)
    # Constraint.own_sessions_check(schedule, plan.courses)
    Constraint.all_constraints(schedule, plan.courses)
    # Constraint.session_spread_check(schedule, plan.courses)


    # Print the end-text
    plan.end()

    plan.makeplot(plan.points)

    # Make a html file for the schedule
    plan.save_html(schedule, rooms)
