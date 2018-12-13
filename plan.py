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
from session import Session
import loaddata
import schedulemaker
import genetic
import gui
import annealing
import climbergreedy
import hillclimberextended
import hillclimber

import random
import copy
import time
import pandas as pd
from IPython.display import HTML
import tkinter as tk
from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SLOTS = TIME_SLOTS * DAYS * ROOMS
MAXMALUSPOINTS = 0
MAXSCHEDULEPOINTS = 39
POPULATION = 50
SESSION_NUM = 129


class Plan():
    """
    Main script to make a schedule.
    """

    def gui(self, schedule, courses, schedule_counter, bool):
        """
        Starts a GUI when plan.py is runned.
        """

        window = tk.Tk()
        window.geometry('700x500')
        window.configure(bg='white')
        # Add title to GUI
        window.title("GUI Safariteam")

        def printresults(algorithm):
            print("Loading....")
            tk.Label(window, text="Resulted points (out of 440): ").place(x=360, y =10)
            if algorithm == "hc":
                tk.Label(window, text=plan.runalgorithm("hill climber", int(n.get()), int(x.get()), 0, 0, 0)[0]).place(x=360, y = 40)
            elif algorithm == "hc2":
                print("TODO")
            elif algorithm == "sa":
                tk.Label(window, text=plan.runalgorithm("Simmulated annealing", int(n2.get()), int(x2.get()), float(t1.get()), float(t2.get()), type.get())[0]).place(x=360, y = 40)
            elif algorithm == "genetic":
                print("TODO")


        # Add labels to the hill climber input
        tk.Label(window, text="Hill climber: ", font="Arial 15 bold").grid(column=1)
        Label(window, text="Iterations: ").grid(row=1)
        Label(window, text="Runs (n): ").grid(row=2)
        n = Entry(window)
        x = Entry(window)
        n.grid(row=1, column=1)
        x.grid(row=2, column=1)
        n.insert(10,"10000")
        x.insert(10,"3")
        n.bind('<Return>', lambda _: printresults("hc"))
        x.bind('<Return>', lambda _: printresults("hc"))

        # Add labels to simmulated annealing input
        tk.Label(window, text="Simulated annealing: ", font="Arial 15 bold").grid(column=1)
        Label(window, text="Iterations: ").grid(row=6)
        Label(window, text="Runs (n): ").grid(row=7)
        Label(window, text="Begin temperature: ").grid(row=8)
        Label(window, text="End temperature: ").grid(row=9)
        Label(window, text="exponential | logaritmic").grid(row=10)
        n2 = Entry(window)
        x2 = Entry(window)
        t1 = Entry(window)
        t2 = Entry(window)
        type = Entry(window)
        n2.grid(row=6, column=1)
        x2.grid(row=7, column=1)
        t1.grid(row=8, column=1)
        t2.grid(row=9, column=1)
        type.grid(row=10, column=1)
        n2.insert(10,"1000")
        x2.insert(10,"1")
        t1.insert(10,"4")
        t2.insert(10,"0.01")
        type.insert(10,"exponential")
        n2.bind('<Return>', lambda _: printresults("sa"))
        x2.bind('<Return>', lambda _: printresults("sa"))
        t1.bind('<Return>', lambda _: printresults("sa"))
        t2.bind('<Return>', lambda _: printresults("sa"))
        type.bind('<Return>', lambda _: printresults("sa"))

        # Add labels to genetic input
        tk.Label(window, text="Genetic algorithm: SANNE WAT MOET HIER AAAH ", font="Arial 15 bold").grid(column=1)
        Label(window, text="Population: ").grid(row=12)
        Label(window, text="Runs (n): ").grid(row=13)
        n3 = Entry(window)
        x3 = Entry(window)
        n3.grid(row=12, column=1)
        x3.grid(row=13, column=1)
        n3.insert(10,"10")
        x3.insert(10,"3")
        n3.bind('<Return>', lambda _: printresults("genetic"))
        x3.bind('<Return>', lambda _: printresults("genetic"))


        tk.Label(window, text="Press enter to run. ").grid(column=1)

        tk.Button(window, text="Plot one hill climber run", command=lambda:plan.plot("hill climber")).place(x=100, y=350)
        tk.Button(window, text="Plot one simmulated annealing run", command=lambda:plan.plot("sa")).place(x=100, y=390)

        window.mainloop()


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
        plt.xlabel("Iterations")
        plt.ylabel("Points")
        plt.show()

    def plot(self, algorithm):
        """
        Returns a plot of 1 run (n = 1) of a certain algorithm.
        """

        # Set values to plot a hill climber
        x = 20000
        n = 1
        begin_temperature = 4
        end_temperature = 0.01
        type = "exponential"

        print("Generating a plot...")
        print("May take a minute or 2...")
        print("Or 4...")
        print("Exit at any moment using 'ctr + c'.")
        points = plan.runalgorithm(algorithm, x, n, begin_temperature, end_temperature, type)[2]
        plt.plot(points, 'b')
        plt.xlabel("Iterations")
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


    def runalgorithm(self, algorithm, x, n, begin_temperature, end_temperature, type):
        """
        Run a certain algorithm for n number of times with x number of iterations.
        Algorithm input can be: "hill climber", "hill climber2" "genetic", "simulated annealing".
        Output is a list of maximum points that the algorithm reached.
        """

        maxpoints = []
        for i in range(n):
            # Make new random valid schedule
            schedule = schedulemaker.initialize_schedule(plan.courses)[0]
            # Call algorithm
            if algorithm == "hill climber":
                points = hillclimber.climb(schedule, plan.courses, plan.schedule_counter, x)[1]
            elif algorithm == "hill climber2":
                points = hillclimberextended.climb(schedule, plan.courses, plan.schedule_counter, x)[1]
            elif algorithm == "Simmulated annealing":
                points = annealing.anneal(schedule, plan.courses, plan.schedule_counter, x, begin_temperature, end_temperature, type)[1]
            elif algorithm == "genetic":
                print("TODO")
            # Save max points to a list
            maxpoints.append(round(max(points)))

        print(algorithm, "reached max points of: ", maxpoints)
        return maxpoints, schedule, points


    def generate(self):
        """
        Generates a schedule by calling several helper functions and algorithms.
        """

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

        # # Make random valid schedule
        schedule = schedulemaker.initialize_schedule(plan.courses)[0]

        plan.gui(schedule, plan.courses, plan.schedule_counter, True)


        # Get all points to pass on to save_html
        courses_schedule, spread_points, capacity_points, lecture_points, mutual_course_malus = plan.points_to_print(schedule)

        # Print the end-text
        # plan.end(schedule, courses_schedule)
        # # Make a plot of the points
        # try:
        #     points2 = 0
        #     plan.makeplot(points, points2)
        # except:
        #     print("No points to plot for now.")

        # Make a html file for the schedule
        # plan.save_html(schedule, rooms, spread_points, capacity_points, lecture_points, mutual_course_malus)


if __name__ == "__main__":
    plan = Plan()
    plan.generate()
