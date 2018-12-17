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
import itertools
import genetic
import annealing
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
from matplotlib.pyplot import figure



SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
MAXMALUSPOINTS = 0
MAXSCHEDULEPOINTS = 39
POPULATION = 50
SESSION_NUM = 129


class Plan():
    """
    Main script to make a schedule.
    """

    def initialize_schedule(self, courses):
        """
        Initialize schedule using Session().
        """

        schedule = [[[[None] for i in range(ROOMS)] for i in range(TIME_SLOTS)]
                    for i in range(DAYS)]

        session_list = []
        lecture_sessions = []
        other_sessions = []
        empty_sessions = []
        session_list_2d = []

        # makes a list of all sessions
        for course in courses:
            session_list = session_list + course.sessions_total

            # make a list of lists for each course
            session_list_2d.append(course.sessions_total)

        # adds overall id's to the sessions
        session_counter = 0

        for i in range(len(session_list_2d)):
            for j in range(len(session_list_2d[i])):
                session_list_2d[i][j].overall_id = session_counter
                session_counter += 1


        for course in courses:
            for i in range(len(session_list_2d)):
                for j in range(len(session_list_2d[i])):
                    if session_list_2d[i][j].name == course.name:

                        session_list_2d[i][j].course_object = course

        # make SLOTS empty sessions
        for i in range(SLOTS):
            name = ' '
            type = ' '
            max_students = ' '
            session_id = 'nvt2'
            group_id = 'nvt2'
            empty_session = Session(name, type, max_students, session_id, group_id)
            empty_session.overall_id = SLOTS
            empty_sessions.append(empty_session)

        for i in range(len(session_list_2d)):
            for j in range(len(session_list_2d[i])):

                # put all lectures in list and put all other sessions in other list
                if session_list_2d[i][j].type == "lecture":
                    lecture_sessions.append(session_list_2d[i][j])
                elif session_list_2d[i][j].type == "tutorial" or session_list_2d[i][j].type == "practicum":
                    other_sessions.append(session_list_2d[i][j])

        counter_sessions = 0
        new_sched = False

        # plan.fill_schedule(schedule, total, other_sessions, empty_sessions, courses)
        # print(session_list)
                    # print(len(session_list))


        # zorgt dat er een plot wordt gemaakt van alle vakken waar het fout gaat
        session_analysis = [0 for i in range(SESSION_NUM)]
        row1 = [0 for i in range(SESSION_NUM)]
        row2 = [0 for i in range(SESSION_NUM)]
        row3 = [0 for i in range(SESSION_NUM)]
        new_sched = False
        counter_lala = 0
        counter_2 = 0
        lalalijst = []
        dataaxis2 = []
        dataaxis22 = [0 for i in range(SESSION_NUM)]
        for i in range(len(session_list_2d)):
            for j in range(len(session_list_2d[i])):
                dataaxis2.append(session_list_2d[i][j].course_object.expected_students)



        if not bool(new_sched):

            while not bool(new_sched) or not counter_2 >= 1000:

                new_sched, course_stop1, session_problems= plan.fill_schedule(schedule, session_list_2d, lecture_sessions,
                                          empty_sessions, courses)

                plan.schedule_counter += 1

                if bool(new_sched):
                    if counter_2 < 1000:
                        continue

                    else:
                        break

                print(f"coursestpo: {course_stop1}")
                print(f"1: {course_stop1.name}")
                course_stop = course_stop1.overall_id
                print(f"2: {course_stop}")
                dataaxis22[course_stop] = course_stop1.course_object.expected_students
                row1[course_stop] += session_problems[0]
                row2[course_stop] += session_problems[1]
                row3[course_stop] += session_problems[2]
                session_analysis[course_stop] += 1
                counter_2 += 1


        xAxis = []
        yAxis = session_analysis
        #
        # for k in range(len(session_analysis)):
        #  if session_analysis[k] > 0:
        #      for j in range(len(session_list_2d)):
        #          for g in range(len(session_list_2d[j])):
        #              if session_list_2d[j][g].overall_id == k:
        #                  xAxis.append(f"{session_list_2d[j][g].name} {session_list_2d[j][g].type} {session_list_2d[j][g].overall_id}")
        #                  yAxis.append(session_analysis[k])
        #                  lalalijst.append([session_list_2d[j][g], session_analysis[k]])

        for i in range(len(session_analysis)):
            xAxis.append(f'{i}')



        # print(row3)
        # for l in range(len(row3)):
        #     if row3[l] > 0:
        #         # for m in range(len(session_list)):
        #             # if session_list[m].overall_id == l:
        #             #     print(l)


        for l in range(len(row1) - 1, -1, -1):
            if row1[l] == 0 and row2[l] == 0 and row3[l] == 0:
                # overlap with mutual courses

                del row1[l]
                del row2[l]
                del row3[l]

        # ax = plt.subplot(111)
        # pos1 = ax.get_position() # get the original position
        # pos2 = [pos1.x0, pos1.y0 + 0.2,  pos1.width , pos1.height - 0.2]
        # ax.set_position(pos2)
        plt.bar(xAxis, yAxis)
        plt.xticks(fontsize=6, rotation=89)
        plt.title("Analysis of invalid schedules")
        plt.ylabel("Sessions causing invalid schedule")

        x = np.linspace(0, 5)
        y = np.sin(x)
        print(x)
        print(y)
        axes2 = plt.twinx()
        axes2.plot(xAxis, dataaxis2, color='k', label='Sine')
        axes2.set_ylabel('Line plot')
        plt.show()

        plt.show()



        N = len(row1)
        ind = np.arange(N)    # the x locations for the groups
        width = 0.35       # the width of the bars: can also be len(x) sequence
        p1 = plt.bar(ind, row1, width)
        p2 = plt.bar(ind, row2, width, bottom=np.array(row1))
        p3 = plt.bar(ind, row3, width,
                bottom=np.array(row1) + np.array(row2))

        plt.xticks(ind, xAxis)
        plt.xticks(fontsize=6, rotation=89)
        # plt.yticks(np.arange(0, 81, 10))
        plt.legend((p1[0], p2[0], p3[0]), ('Lectures first', 'Overlap own course', 'Overlap mutual courses'))




        return new_sched, total, other_sessions, empty_sessions


    def fill_schedule(self, schedule, sessions_2d, other_sessions, empty_sessions, courses):
        """
        Fill empty schedule with sessions. This function will begin to fill all
        the lectures and will go on to fill other sessions.
        """

        # Gebruik nested for loop om elke cel een session te geven.
        # Je geeft hierbij een lijst met sessies mee aan de functie get_session
        # De lijst met sessies is al gemaakt in initialize_schedule()

        # Vul eerst met lege sessions
        # counter = 0

        lectures = []



        random.shuffle(sessions_2d)


        for i in range(len(sessions_2d)):
            for j in range(len(sessions_2d[i])):
                lectures.append(sessions_2d[i][j])


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

            # lijst met frequentie van specifieke problemen, op positite 1: frequentie
            # van wanneer lectures ervoor hadden gemoeten. positie 2: frequentie van
            # wanneer er overlap was van het eigen vak. Positie 3: frequentie van
            # wanneeer er overlap was met mutual course

            problems = [0,0,0]



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

                                    # het aantal posities dat verwijderd moet worden door een lecture
                                    problems[0] += (len(location))

                                    # alle eerdere locaties mogen weg want er mag niets voor een lecture
                                    location.clear()


                                    # lectures first

                                    break
                                elif not lectures[e].session_id == schedule[b][c][d].session_id:
                                    if lectures[e].group_id == schedule[b][c][d].group_id:
                                        for k in range(len(location) - 1, -1, -1):
                                            if location[k][1] == c and location[k][0] == b:

                                                # overlap with own course
                                                problems[1] +=1
                                                del location[k]
                                        break


                            elif schedule[b][c][d].name in mutual_courses_session:
                                rooms_allowed = False
                                for k in range(len(location) - 1, -1, -1):
                                    if location[k][1] == c and location[k][0] == b:

                                        # overlap with mutual courses
                                        problems[2] +=1
                                        del location[k]

                                break



                        # als het een lecture is
                        elif lectures[e].name == schedule[b][c][d].name or schedule[b][c][d].name in mutual_courses_session:
                            if lectures[e].name == schedule[b][c][d].name:

                                # own courses overlap
                                prob_index = 1
                            else:

                                # mutual courses overlap
                                prob_index = 2

                            # achteruit itereren anders gaat het verwijderen niet goed
                            for k in range(len(location) - 1, -1, -1):
                                if location[k][1] == c and location[k][0] == b:
                                    problems[prob_index] += 1
                                    del location[k]
                            rooms_allowed = False


                            break

                        # if the slot in the schedule is empty
                        if schedule[b][c][d].name == ' ':
                            location.append((b,c,d))

            if bool(location):
                counter = 0

                # als het een lecture was, verwijder het aantal potentiele locaties aan het einde van het rooster gelijk
                # aan de hoeveelheid vakken die er nog moeten worden ingedeeld
                if lectures_first:

                    amount_sessions = lectures[e].course_object.lecture + lectures[e].course_object.tutorial + lectures[e].course_object.practicum
                    prohibited_timeslots = amount_sessions - 1 - passed_lectures

                    # probleem: er moeten nu teveel plekken open worden gehouden
                    passed_lectures += 1


                    while not counter == prohibited_timeslots:
                        if not bool(location) or prohibited_timeslots >= len(location):


                            return False, lectures[e], problems


                        elif not location[-1][1] == location[-2][1]:

                            counter +=1

                        # lectures have to go first

                        problems[0] += 1
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

                return False, lectures[e], problems
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

            return schedule, -1, problems

        else:
            # plan.schedule_counter += 1

            return False, lectures[e], problems

    # def random_schedule(self, schedule, sessions):
    #     """
    #     Generates a random schedule. Assigns every session to a random timeslot.
    #     # Hou bij welke random nummers al geweest zijn. De while loop
    #     # Zorgt ervoor dat er een random nummer wordt gemaakt die nog
    #     # niet is geweest.
    #     """
    #
    #     # Maak een 1D lijst van schedule
    #     flatten = np.array(schedule, dtype=object).flatten()
    #
    #     random_numbers = []
    #
    #     for i in range(len(sessions)):
    #         rand = random.randint(0, SLOTS - 1)
    #         while rand in random_numbers:
    #             rand = random.randint(0, SLOTS - 1)
    #         random_numbers.append(rand)
    #         flatten[rand] = sessions[i]
    #
    #     # Convert back to 3D list
    #     schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
    #
    #     # Keep track of how many schedules were made
    #     plan.schedule_counter += 1
    #
    #     return schedule

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

    def makeplot(self, points):
        """
        Plots a graph of all the points on the y-axis and number of schedules
        on the x-axis.
        """
        plt.plot(points)
        plt.ylabel("Points")
        plt.show()



    def end(self, schedule, courses_schedule):
        """
        Prints text to tell user how many schedules were made and how long it took to make.
        """
        print("Succes! :-)")
        print("It took:", round(time.time() - plan.then, 3), "seconds, = ", round((time.time() - plan.then) / 60, 3), "minutes.")
        print("Made", plan.schedule_counter, "schedule(s).")
        # print("Points:", Constraint.session_spread_check(schedule, plan.courses, courses_schedule)[0] - Constraint.students_fit(schedule, plan.courses, courses_schedule), "out of 440.")

    def generate(self):
        """
        Generates a schedule by calling several helper functions and algorithms.
        """

        point_list = []
        final_point_list = []
        plan.then = time.time()
        print("Loading...")
        plan.random_numbers = []
        plan.schedule_counter = 0

        # Load all the courses, rooms and sessions
        plan.courses = loaddata.load_courses()

        # # runs the hillclimber hunderd times
        # point_list = []
        # for i in range(100):
        #     print(f"i = {i}")
        #     schedule = plan.initialize_schedule(plan.courses)[0]
        #
        #     # schedule_points = Constraint.get_points(schedule, plan.courses)
        #
        #
        #     while Constraint.get_points(schedule, plan.courses) < -200:
        #         print(Constraint.get_points(schedule, plan.courses))
        #         plan.schedule_counter = 0
        #         schedule = plan.initialize_schedule(plan.courses)[0]
        #
        #         # schedule_points = Constraint.get_points(schedule, plan.courses)
        #     schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)
        #     print("TEST VAN POINTS LIST", points)
        #     point_list.append(max(points))
        #     print(f"point_list: {point_list}")
        #     final_points = hillclimber.get_points_final(schedule, plan.courses)
        #     final_point_list.append(final_points)
        #     print(f"finalpointlist: {final_point_list}")





                # points = Constraint.get_points(schedule, plan.courses)
            # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)
            # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)
            # print("Runnig algorithm...")
            # Geef dit rooster mee aan de soft constraints
            # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)

            # schedule, points, plan.schedule_counter = climbergreedy.soft_constraints(schedule, plan.courses, plan.schedule_counter)

        #     # print(i)
        #



        rooms = loaddata.load_rooms()
        plan.own_session_points = 0
        spread_points = 0
        lecture_points = 0
        capacity_points = 0
        schedule = plan.initialize_schedule(plan.courses)[0]

        # Geef dit rooster mee aan de soft constraints
        # schedule, points, plan.schedule_counter = hillclimber.soft_constraints(schedule, plan.courses, plan.schedule_counter)

        # while points < -200:
        #     schedule = plan.initialize_schedule(plan.courses)[0]
        #     points = Constraint.get_points(schedule, plan.courses)
        # print("Running algorithm...")
        # plan.schedule_counter = 0
        # # schedule, points, plan.schedule_counter = climbergreedy.climbergreedy(schedule, plan.courses, plan.schedule_counter)

        # # schedule, points, plan.schedule_counter = climbergreedy.soft_constraints(schedule, plan.courses, plan.schedule_counter)

        # annealing.anneal(schedule, plan.courses, plan.schedule_counter)

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
        schedules = []
        genetic_on = False
        if genetic_on:
            for i in range(POPULATION):
                schedules.append(plan.initialize_schedule(plan.courses)[0])

        # genetic.genetic_algortim(schedules, plan.courses)

        # test new constraint function
        # courses_schedule = Constraint.all_constraints(schedule, plan.courses)

        # DIT MOET OOK ECHT EVEN IN EEN APARTE FUNCTIE lol XOXOXO R
        courses_schedule = Constraint.all_constraints(schedule, plan.courses)
        Constraint.session_spread_check(schedule, plan.courses, courses_schedule)
        capacity_points = (Constraint.students_fit(schedule, plan.courses, courses_schedule))
        spread_points = Constraint.session_spread_check(schedule, plan.courses, courses_schedule)[0]
        # print(spread_points)
        capacity_points = (Constraint.students_fit(schedule, plan.courses, courses_schedule))
        lecture_points = Constraint.lecture_first(schedule, plan.courses, courses_schedule)
        Constraint.lecture_first(schedule, plan.courses, courses_schedule)
        mutual_course_malus = Constraint.mutual_courses_check(schedule, plan.courses)


        #
        # overall_id = Constraint.session_points(schedule, plan.courses)[0]
        # Constraint.overall_id_points(schedule, plan.courses, overall_id)
        # Constraint.switch_session(schedule, 1, overall_id, plan.courses)

        # # Print the end-text
        plan.end(schedule, courses_schedule)
        # # Make a plot of the points
        # try:
        #     plan.makeplot(points)
        # except:
        #     print("No points to plot for now.")

        # Make a html file for the schedule
        plan.save_html(schedule, rooms, spread_points, capacity_points, lecture_points, mutual_course_malus)


if __name__ == "__main__":
    # list = [272.75, 295.0, 357.5, 337.5, 308.75, 305.5, 310.75, 281.75, 311.0, 306.75, 259.5, 309.25, 276.5, 349.5, 341.75, 283.5, 314.5, 332.5, 311.0, 315.25, 303.25, 310.25, 357.5, 316.5, 331.5, 338.75, 314.75, 314.75, 331.0, 331.75, 296.75, 313.5, 304.75, 310.5, 316.75, 307.5, 283.25, 326.75, 300.25, 343.5, 335.75, 336.25, 298.0, 303.25, 340.25, 330.0, 345.75, 335.5, 270.5, 360.0, 347.5, 317.75, 342.25, 316.0, 257.0, 297.75, 330.5, 313.25, 280.75, 333.0, 336.25, 322.5, 278.25, 280.25, 323.75, 339.25, 367.5, 290.0, 322.75, 304.0, 311.75, 311.5, 350.25, 340.5, 330.5, 355.0, 322.5, 346.75, 353.0, 290.75, 313.25, 302.5, 324.75, 265.0, 290.25, 349.5, 298.75, 295.25, 339.5, 294.0, 333.25, 309.5, 317.5, 300.0, 351.75, 285.5, 306.5, 262.0, 330.75, 302.25 ]
    list2 = [-380.5, -440.75, -395.75, -321.75, -381.5, -398.75, -338.25, -304.25, -348.75,-355.25, -423.75, -254.25, -275.0, -353.75, -368.25, -280.75, -397.0, -368.5, -346.0, -328.0, -350.75, -362.75, -333.5, -296.5, -251.25, -219.75, -316.5, -322.0, -353.5, -337.25, -386.0, -376.5, -387.75, -339.0, -324.5, -338.5, -308.5, -312.75, -391.25, -382.0, -325.25, -375.75, -375.0, -296.75, -335.25, -313.25, -358.75, -353.25, -216.5, -346.75, -281.75, -302.75, -326.5, -295.0, -353.0, -335.0,-335.25, -306.75, -383.5, -318.0, -309.75, -386.75, -307.25, -328.0, -273.25, -390.75, -326.0, -342.0, -348.5, -385.75, -329.5, -254.75, -349.25, -265.75, -357.75, -281.25, -397.25, -345.0, -279.5, -327.0, -449.5, -351.25, -351.75, -363.75, -322.75, -316.5, -304.5, -350.0, -389.5, -297.5, -343.75, -420.0, -346.25, -348.75, -347.75, -281.25, -377.75, -310.75, -351.0, -347.75]
    list = [123.5, 133.0, 142.75, 143.5, 107.0, 217.0, 109.0, 106.0, 188.75, 83.0, 169.25,91.25, 150.5, 167.75, 132.25, 158.5, 141.25, 137.0, 93.0, 202.75, 81.25, 75.75,90.5, 82.5, 63.25, 207.75, 155.5, 159.0, 155.5, 130.0, 115.75, 139.5, 144.5, 136.0, 174.25, 151.5, 120.25, 217.75, 124.25, 205.0, 77.75, 147.25, 98.75, 146.75,121.25, 144.0, 60.75, 111.25, 73.25, 10.5]
    # print(max(list))
    # ax = plt.subplot(111)
    # pos1 = ax.get_position() # get the original position
    # pos2 = [pos1.x0, pos1.y0 + 0.2,  pos1.width , pos1.height - 0.2]
    # ax.set_position(pos2)
    # plt.boxplot([list, list2])
    # plt.xticks(fontsize=10)
    # ax.set_xticklabels(['Hillclimber', 'Random'])
    # plt.title("Schedule points after creating 100 schedules")
    # plt.ylabel("Points")
    # plt.xlabel("Algorithm")
    # plt.show()
    ax = plt.subplot(111)
    pos1 = ax.get_position() # get the original position
    pos2 = [pos1.x0, pos1.y0 + 0.2,  pos1.width , pos1.height - 0.2]
    ax.set_position(pos2)
    plt.boxplot(list)
    plt.xticks(fontsize=10)
    ax.set_xticklabels(['Hillclimber'])
    plt.title("Schedule points after creating 100 schedules")
    plt.ylabel("Points")
    plt.xlabel("Algorithm")
    plt.show()



    plan = Plan()
    plan.generate()
