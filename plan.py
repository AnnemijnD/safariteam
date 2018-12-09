"""
Heuristieken 2018 -- Lectures
Names: Annemijn, Sanne & Rebecca
This script generates a schedule.
"""

import os, sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algoritmes"))

from constraint import Constraint
import loaddata
from session import Session
import switch
import genetic
import GUI
import annealing
import climbergreedy
import hillclimber
import csv
import random
import copy
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
POPULATION = 50


class Plan():
    """
    Main script to make a schedule.
    """

    def initialize_schedule(self, courses):
        """
        Initialize schedule using Session().
        """

        schedule = [[[[None] for i in range(ROOMS)] for i in range(TIME_SLOTS)] for i in range(DAYS)]

        sessions = []
        session_list = []
        lecture_sessions = []
        other_sessions = []
        empty_sessions = []

        # random.shuffle(courses)

        # ANNEMIJN KAN JE HIER NOG EEN COMMENT BIJ ZETTEN, SNap niet wat je hier hebt gedaan

        for course in courses:
            session_list = session_list + course.sessions_total

        session_counter = 0
        for i in range(len(session_list)):
            session_list[i].overall_id = session_counter
            session_counter += 1

        # make #SLOTS empty sessions
        for i in range(SLOTS):
            name = ' '
            type = ' '
            max_students = ' '
            session_id = 'nvt2'
            group_id = 'nvt2'
            empty_session = Session(name, type, max_students, session_id, group_id)
            empty_session.overall_id = SLOTS
            empty_sessions.append(empty_session)

        for i in range(len(session_list)):
            # Get all the lectures
            if session_list[i].type == "lecture":
                lecture_sessions.append(session_list[i])
            elif session_list[i].type == "tutorial" or session_list[i].type == "practical":
                other_sessions.append(session_list[i])

        # shuffle de lectures zodat ze random zijn
        # Make copy of sessions and shuffle
        lectures = lecture_sessions[:]
        others = other_sessions[:]
        # random.shuffle(lectures)
        # random.shuffle(other_sessions)

        # De lijst met totale sessies bestaat dus uit een lijst met eerst
        # Hoorcolleges, daarna de andere sessies en is opgevuld tot 140 met lege sessies
        total = []
        total = lectures + other_sessions

        # plan.fill_schedule(schedule, total, other_sessions, empty_sessions, courses)
        # print(session_list)
        # print(len(session_list))
        counter_sessions = 0
        new_sched = False

        while not bool(new_sched):
            new_sched = plan.fill_schedule(schedule, session_list, lecture_sessions, empty_sessions, courses)
            plan.schedule_counter +=1
            counter_sessions += 1
            # if plan.schedule_counter % 100 == 0:
            #     print(plan.schedule_counter)
            if not new_sched == False:
                break

        return schedule, total, other_sessions, empty_sessions


    def fill_schedule(self, schedule, lectures, other_sessions, empty_sessions, courses):
        """
        Fill empty schedule with sessions. This function will begin to fill all
        the lectures and will go on to fill other sessions.
        """

        # Gebruik nested for loop om elke cel een session te gegen.
        # Je geeft hierbij een lijst met sessies mee aan de functie get_session
        # De lijst met sessies is al gemaakt in initialize_schedule()

        # Vul eerst met lege sessions
        # counter = 0
        session_counter = 0
        for b in range(DAYS):
            for c in range(TIME_SLOTS):
                for d in range(ROOMS):
                    schedule[b][c][d] = empty_sessions[session_counter]
                    session_counter += 1




        # Verdelen over slots als hard constraint

        # vertelt hoeveelste lecture van dit vak dit is
        passed_lectures = 0


        # found = False
        for e in range(len(lectures)):
            # print(lectures[e].name)

            lectures_first = False
            tut_or_prac = False
            location = []
            found = False


            for course in courses:
                if lectures[e].name == course.name:
                   lectures[e].course_object = course
                   mutual_courses_session = lectures[e].course_object.mutual_courses

            # is dit een hoorcollege?
            if lectures[e].type == "lecture":
                lectures_first = True
            else:
                tut_or_prac = True

            for b in range(DAYS):

                for c in range(TIME_SLOTS):

                    rooms_allowed = True
                    # availibility = True
                    for d in range(ROOMS):

                        # als het een tutorial of pracitcal is
                        if not lectures_first:


                            if lectures[e].name == schedule[b][c][d].name:
                                if schedule[b][c][d].type == "lecture":

                                    # alle eerdere locaties mogen weg want er mag niets voor een lecture
                                    location.clear()
                                    # print(location)
                                    break
                                elif not lectures[e].session_id == schedule[b][c][d].session_id:
                                    if lectures[e].group_id == schedule[b][c][d].group_id:
                                        for k in range(len(location) - 1, -1, -1):
                                            if location[k][1] == c and location[k][0] == b:
                                                del location[k]
                                        break


                            elif schedule[b][c][d].name in mutual_courses_session:
                                rooms_allowed = False
                                for k in range(len(location) - 1, -1, -1):
                                    if location[k][1] == c and location[k][0] == b:
                                        del location[k]

                                break



                        # als het een lecture is
                        elif lectures[e].name == schedule[b][c][d].name or schedule[b][c][d].name in mutual_courses_session:

                            # achteruit itereren anders gaat het verwijderen niet goed
                            for k in range(len(location) - 1, -1, -1):
                                if location[k][1] == c and location[k][0] == b:
                                    del location[k]
                            rooms_allowed = False

                            # print(location)
                            break

                        # if the slot in the schedule is empty
                        if schedule[b][c][d].name == ' ':
                            location.append((b,c,d))

            if bool(location):
                counter = 0

                # als het een lecture was, verwijder het aantal potentiele locaties aan het einde van het rooster gelijk
                # aan de hoeveelheid vakken die er nog moeten worden ingedeeld
                if lectures_first:

                    amount_sessions = lectures[e].course_object.lecture + lectures[e].course_object.tutorial + lectures[e].course_object.practical
                    prohibited_timeslots = amount_sessions - 1 - passed_lectures

                    # probleem: er moeten nu teveel plekken open worden gehouden
                    passed_lectures += 1


                    while not counter == prohibited_timeslots:
                        if not bool(location) or prohibited_timeslots >= len(location):

                            return False

                        elif not location[-1][1] == location[-2][1]:
                            # print(location)
                            counter +=1
                        location.remove(location[-1])

                random_location = random.choice(location)
                # print(random_location)
                schedule[random_location[0]][random_location[1]][random_location[2]] = lectures[e]
                found = True
                # als dit het laatste lecture van het vak was of als er geen andere sessies meer zijn van dit vak:
                if not e == len(lectures) - 1 and (not lectures[e + 1].type == "lecture" or not lectures[e].course_object == lectures[e + 1].course_object):
                    passed_lectures = 0


            else:

                # plan.schedule_counter += 1

                return False
                # return schedule
                #plan.initialize_schedule(plan.courses)
                # break
        if found:

            # give the empty_sessions overall_ids
            overall_id_counter = 129
            for i in range(DAYS):
                for j in range(TIME_SLOTS):
                    for k in range(ROOMS):
                        # checks if the session is empty
                        if schedule[i][j][k].overall_id == SLOTS:
                            schedule[i][j][k].overall_id = overall_id_counter
                            overall_id_counter += 1

            return schedule

        else:
            # plan.schedule_counter += 1

            return False

    def random_schedule(self, schedule, sessions):
        """
        Generates a random schedule. Assigns every session to a random timeslot.
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

    def save_html(self, schedule, rooms, spread_points, capacity_points, lecture_points, mutual_course_malus):
        """
        Print into html to visualize schedule.
        MOET NOG EEN TABEL KOMEN MET HOEVEEL PUNTEN DIT ROOSTER IS EN WAAROP GEBASEERD.
        """
        # Bewaar dit schedule voor andere visualisatie van het rooster
        schedule1 = copy.copy(schedule)

        # Maak een grafiek van alle punten
        d = pd.Series([lecture_points, -mutual_course_malus, "", spread_points, capacity_points, spread_points - capacity_points])
        d = pd.DataFrame(d)
        d.columns = ["Points"]
        d.index = ["Incorrectly placed lectures", "Incorrectly placed courses with 'mutual' courses", "", "Spread bonus points (out of 440)", "Capacity malus points (out of 1332)", "Total points"]

        flatten = np.array(schedule).flatten()
        counter = 0
        for i in range(len(flatten)):
            if flatten[i].name is not ' ':
                flatten[i] = str(flatten[i]) + " : " + str(rooms[counter])
            counter += 1
            counter = counter % 7
        # Zet terug naar een 3D lijst
        schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

        # Dit is voor het eerste rooster van de hele week
        df = pd.DataFrame(schedule1)
        pd.set_option('display.max_colwidth', 600)
        df.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
        df.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # Transpose rows and columns
        df = df.T

        # Dit is voor de kleinere roosters
        test = pd.DataFrame(schedule)
        pd.set_option('display.max_colwidth', 600)
        test.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
        test.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # Transpose rows and columns
        test = test.T

        # Stel de column namen vast
        tags = df['Monday'].apply(pd.Series)
        tags.columns = [rooms[0], rooms[1], rooms[2], rooms[3], rooms[4], rooms[5], rooms[6]]
        tuesday = df['Tuesday'].apply(pd.Series)
        tuesday.columns = [rooms[0], rooms[1], rooms[2], rooms[3], rooms[4], rooms[5], rooms[6]]
        wednesday = df['Wednesday'].apply(pd.Series)
        wednesday.columns = [rooms[0], rooms[1], rooms[2], rooms[3], rooms[4], rooms[5], rooms[6]]
        thursday = df['Thursday'].apply(pd.Series)
        thursday.columns = [rooms[0], rooms[1], rooms[2], rooms[3], rooms[4], rooms[5], rooms[6]]
        friday = df['Friday'].apply(pd.Series)
        friday.columns = [rooms[0], rooms[1], rooms[2], rooms[3], rooms[4], rooms[5], rooms[6]]

        html_string = '''
        <html>
          <head><title>Schedule</title></head>
          <link rel="stylesheet" type="text/css" href="style.css" href="https://www.w3schools.com/w3css/4/w3.css"/>
          <body class="body bgcolor="#660000">
            <h1 class="h1" align="center"></h>
            {table}
          </body>
        </html>.
        '''

        with open('resultaten/schedule.html', 'w') as f:
            f.write(html_string.format(table=d.to_html(classes='points')))
            f.write(html_string.format(table=test.to_html(classes='style')))
            f.write("Monday")
            f.write(html_string.format(table=tags.to_html(classes='style')))
            f.write("Tuesday")
            f.write(html_string.format(table=tuesday.to_html(classes='style')))
            f.write("Wednesday")
            f.write(html_string.format(table=wednesday.to_html(classes='style')))
            f.write("Thursday")
            f.write(html_string.format(table=thursday.to_html(classes='style')))
            f.write("Friday")
            f.write(html_string.format(table=friday.to_html(classes='style')))

    def makeplot(self, points, points2):
        """
        Plots a graph of all the points on the y-axis and number of schedules
        on the x-axis.
        """
        plt.plot(points, 'b') # annealing
        plt.plot(points2, 'r') # hillclimber
        plt.ylabel("Points")
        plt.show()

    def end(self, schedule, courses_schedule):
        """
        Prints text to tell user how many schedules were made and how long it took to make.
        """
        print("Succes! :-)")
        print("It took:", round(time.time() - plan.then, 3), "seconds, = ", round((time.time() - plan.then) / 60, 3), "minutes.")
        print("Made", plan.schedule_counter, "schedule(s).")
        print("Points:", Constraint.session_spread_check(schedule, plan.courses, courses_schedule)[0] - Constraint.students_fit(schedule, plan.courses, courses_schedule), "out of 440.")

    def points_to_print(self, schedule):
        """
        TODO
        """

        courses_schedule = Constraint.all_constraints(schedule, plan.courses)
        spread_points = Constraint.session_spread_check(schedule, plan.courses, courses_schedule)[0]
        capacity_points = (Constraint.students_fit(schedule, plan.courses, courses_schedule))
        lecture_points = Constraint.lecture_first(schedule, plan.courses, courses_schedule)
        mutual_course_malus = Constraint.mutual_courses_check(schedule, plan.courses)

        return courses_schedule, spread_points, capacity_points, lecture_points, mutual_course_malus

    def generate(self):
        """
        Generates a schedule by calling several helper functions and algorithms.
        """

        GUI.gui()

        point_list = []
        plan.then = time.time()
        print("Loading...")
        plan.random_numbers = []
        plan.schedule_counter = 0

        # Load all the courses, rooms and sessions
        plan.courses = loaddata.load_courses()

        # Alle andere dingen laden jeeej
        rooms = loaddata.load_rooms()
        plan.own_session_points = 0

        # Make random valid schedule
        schedule = plan.initialize_schedule(plan.courses)[0]

        # switch.switch_session(schedule, 1, -1)
        # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter, True)

        # Run both hill climber and simulated annealing next to each other
        # save_sched = schedule
        # Zoek het beste rooster met een hill climber
        # schedule, points, plan.schedule_counter = annealing.anneal(schedule, plan.courses, plan.schedule_counter)
        # points = hillclimber.soft_constraints(save_sched, plan.courses, plan.schedule_counter, True)[1]
        # print("next algorithm")
        # points2 = hillclimber.soft_constraints(save_sched, plan.courses, plan.schedule_counter, False)[1]
        # print("next algorithm")
        # points3 = annealing.anneal(save_sched, plan.courses, plan.schedule_counter)[1]

        # plt.plot(points, 'r') # normale hillclimber
        # plt.plot(points2, 'm') # acceptatie hillclimber
        # plt.plot(points3, 'b') # simulated annealing
        # plt.ylabel("Points")
        # plt.xlabel("Iterations")
        # plt.show()

        # runs the hillclimber hunderd times
        # point_list = []
        # for i in range(30):
        #     schedule = plan.initialize_schedule(plan.courses)[0]
        #
        #     # print("Runnig algorithm...")
        #     # Geef dit rooster mee aan de soft constraints
        #     # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)
        #
        #     # schedule, points, plan.schedule_counter = climbergreedy.soft_constraints(schedule, plan.courses, plan.schedule_counter)
        #     point_list.append(points[-1])
        #     # print(i)




        # runs the hillclimber hunderd times
        # point_list = []
        # for i in range(100):
        #     print(f"i = {i}")
        #     schedule = plan.initialize_schedule(plan.courses)[0]
        #
        #     # schedule_points = Constraint.get_points(schedule, plan.courses)
        #
        #
        #     while Constraint.get_points(schedule, plan.courses) < -200:
        #         plan.schedule_counter = 0
        #         schedule = plan.initialize_schedule(plan.courses)[0]
        #
        #         # schedule_points = Constraint.get_points(schedule, plan.courses)
        #     schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)
        #     print("TEST VAN POINTS LIST", points)
        #     point_list.append(max(points))
        #     print(f"point_list: {point_list}")
        #
        #         # points = Constraint.get_points(schedule, plan.courses)
        #     # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)
        #     # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)
        #     # print("Runnig algorithm...")
        #     # Geef dit rooster mee aan de soft constraints
        #     # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)
        #
        #     # schedule, points, plan.schedule_counter = climbergreedy.soft_constraints(schedule, plan.courses, plan.schedule_counter)
        #
        # #     # print(i)

        # print("the almighty lijst van 100 hillclimber resultaten")
        # print(point_list)



        # test all_constraints_linear
        # schedule1, lectures, other_sessions, empty_sessions = plan.initialize_schedule(plan.courses, rooms_list)
        # courses_schedule1 = Constraint.all_constraints(schedule1, plan.courses)
        # schedule2 = np.array(schedule1).flatten().tolist()
        # courses_schedule2 = Constraint.all_constraints_linear(schedule2, plan.courses)
        #
        # if courses_schedule1 == courses_schedule2:
        #     print("CHILL")
        # else:
        #     print("huilon")
        #
        # for i in range(len(courses_schedule1)):
        #     if courses_schedule1[i] != courses_schedule2[i]:
        #         print(i)
        #         print(courses_schedule1[i])
        #         print(courses_schedule2[i])
        #
        # genetic.get_points(schedule2, plan.courses)

        # test genetic Algorithm
        # schedules = []
        # for i in range(POPULATION):
        #     schedules.append(plan.initialize_schedule(plan.courses)[0])

        # genetic.genetic_algortim(schedules, plan.courses)


        # Get all points to pass on to save_html
        courses_schedule, spread_points, capacity_points, lecture_points, mutual_course_malus = plan.points_to_print(schedule)

        # Print the end-text
        plan.end(schedule, courses_schedule)
        # Make a plot of the points
        try:
            points2 = 0
            plan.makeplot(points, points2)
        except:
            print("No points to plot for now.")

        # Make a html file for the schedule
        plan.save_html(schedule, rooms, spread_points, capacity_points, lecture_points, mutual_course_malus)


if __name__ == "__main__":
    plan = Plan()
    plan.generate()
