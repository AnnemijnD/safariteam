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
import annealing
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
from matplotlib.pyplot import figure


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


    def generate(self):
        """
        Generates a schedule by calling several helper functions and algorithms.
        """

        plan.then = time.time()
        plan.schedule_counter = 0

        # Load all the courses, rooms and sessions
        plan.courses = loaddata.load_courses()
        plan.rooms = loaddata.load_rooms()
        plan.own_session_points = 0

        # # Make random valid schedule
        schedule = schedulemaker.initialize_schedule(plan.courses)[0]

        print("Opening GUI...")
        plan.gui(schedule, plan.courses, plan.schedule_counter, True)


    def runalgorithm(self, algorithm, x, n, begin_temperature,
                    end_temperature, type, pop, gen, gen_type, input_sched):
        """
        Run a certain algorithm for n number of times with x number of
        iterations. Algorithm input can be: "hill climber", "hill climber2",
        "genetic", "simulated annealing", or "Random".
        Output is a list of maximum points that the algorithm reached or
        the schedule that reached max points.
        """

        maxpoints = []
        max_schedule = None

        for i in range(n):

            if not bool(input_sched):
                first_schedule = schedulemaker.initialize_schedule(plan.courses)[0]
            else:
                first_schedule = input_sched
            # Call algorithm
            if algorithm == "hill climber":
                schedule_temp, points, schedule_counter =  \
                hillclimber.climb(first_schedule, plan.courses, plan.schedule_counter, x)

                if max_schedule == None:
                    max_schedule = schedule_temp

                # Save schedule with most points
                elif Constraint.get_points(schedule_temp, plan.courses) > \
                    Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = schedule_temp

            if algorithm == "hill climber2":
                schedule_temp, points, schedule_counter = \
                hillclimberextended.climb(first_schedule, plan.courses, plan.schedule_counter, x)

                if max_schedule == None:
                    max_schedule = schedule_temp

                # Save schedule with most points
                elif Constraint.get_points(schedule_temp, plan.courses) > \
                    Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = schedule_temp

            elif algorithm == "Random":
                points = Constraint.get_points(first_schedule, plan.courses)

                if max_schedule == None:
                    max_schedule = first_schedule

                # Save schedule with most points
                elif Constraint.get_points(first_schedule, plan.courses) > \
                    Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = first_schedule

            elif algorithm == "Simulated annealing":
                schedule_temp, points, schedule_counter = \
                annealing.anneal(first_schedule, plan.courses, \
                    plan.schedule_counter, x, begin_temperature, end_temperature, type)

                if max_schedule == None:
                    max_schedule = schedule_temp

                # Save schedule with most points
                elif Constraint.get_points(schedule_temp, plan.courses) > \
                Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = schedule_temp

            elif algorithm == "genetic":
                print("TODO")
                genetic.genetic_algortim(schedules, plan.courses, pop, gen)

            # Save max points to a list
            if algorithm == "Random":
                maxpoints.append(round(points))
            else:
                maxpoints.append(round(max(points)))

        # Save schedule with highest points
        courses_schedule, spread_points, capacity_points, lecture_points, \
            mutual_course_malus = plan.points_to_print(max_schedule)
        plan.save_html(max_schedule, plan.rooms, spread_points,
                       capacity_points, lecture_points, mutual_course_malus)

        print(algorithm, "reached max points of: ", maxpoints)

        return maxpoints, max_schedule, points

    def compare_algorithm(self, random_n, hillclimber_n, hillclimber_x, hillclimber2_x,
                        hillclimber2_n, sim_x, sim_n, begin_temp, end_temp,
                        type, check_rand, check_hill, check_hill2, check_sim):
        """
        GUI FUNCTION.
        Run certain algorithms with the intention to compare them in a boxplot.
        Takes all arguments necessary to make plot. The check-arguments show
        whether a box for that type of algorithm was checked.
        Returns a boxplot.
        """

        # dict met alle data voor boxplot
        boxplot_data = []
        boxplot_xaxis = []
        points = 0

        schedule = schedulemaker.initialize_schedule(plan.courses)[0]

        if check_rand == 1:
            max_points, max_schedule, points = plan.runalgorithm("Random",
                                        0, random_n, 0, 0, None, 0, 0, 0, False)
            boxplot_data.append(max_points)
            boxplot_xaxis.append(f"Random \n n = {random_n}")

        if check_hill == 1:
            max_points, max_schedule, points = plan.runalgorithm("hill climber",
                            hillclimber_x, hillclimber_n, 0, 0, None, 0, 0, 0, schedule)
            boxplot_data.append(max_points)
            boxplot_xaxis.append(f"Hillclimber \n n = {hillclimber_n}")

        if check_hill2 == 1:
            max_points, max_schedule, points = plan.runalgorithm("hill climber2",
                            hillclimber2_x, hillclimber2_n, 0, 0, None, 0, 0, 0, schedule)
            boxplot_data.append(max_points)
            boxplot_xaxis.append(f"Hillclimber2 \n n = {hillclimber2_n}")

        if check_sim == 1:
            max_points, max_schedule, points = plan.runalgorithm("Simulated annealing",
                                sim_x, sim_n, begin_temp, end_temp, type, 0, 0, 0, schedule)
            boxplot_data.append(max_points)
            boxplot_xaxis.append(f"Simulated Annealing \n n = {sim_n}")

        # Make the plot of selected checkboxes
        ax = plt.subplot(111)
        plt.boxplot(boxplot_data)
        plt.xticks(fontsize=8)
        ax.set_xticklabels(boxplot_xaxis)
        plt.title("Comparing schedule points of different algorithms")
        plt.ylabel("Points")
        plt.xlabel("Algorithms \n (n = runs)")
        plt.show()

    def gui(self, schedule, courses, schedule_counter, bool):
        """
        Starts a GUI when plan.py is runned.
        """

        window = tk.Tk()
        window.geometry('800x700')
        window.title("GUI Safariteam")

        def printresults(algorithm):
            """
            GUI FUNCTION.
            Print results of an algorithm of x iterations and n runs to the GUI.
            """
            # Check for correct input:
            if n.get() and x.get() and n2.get() and x2.get() and t1.get() \
                    and t2.get() and type.get() and n3.get() and x3.get() \
                    and hc2n.get() and hc2x.get():

                # Print loading
                print("Generating schedule(s)")
                print("May take a minute or 2...")
                print("Or 4...")
                print("Exit at any moment using 'ctr + c'.")

                # Run the selected algorithm
                Label(window, text="Resulted points (out of 440): ") \
                    .place(x=600, y=20)
                if algorithm == "hc":
                    Label(window, text=plan.runalgorithm("hill climber",
                        int(x.get()), int(n.get()), 0, 0, 0, 0, 0, 0, False)[0],
                        wraplength=30, font="Arial 10").place(x=600, y =50)
                elif algorithm == "hc2":
                    Label(window, text=plan.runalgorithm("hill climber2",
                        int(hc2x.get()), int(hc2n.get()), 0, 0, 0, 0, 0, 0, False)[0],
                        wraplength=30, font="Arial 10").place(x=600, y =50)
                elif algorithm == "sa":
                    Label(window, text=plan.runalgorithm("Simulated annealing",
                            int(x2.get()) / 2, int(n2.get()), float(t1.get()),
                            float(t2.get()), type.get(), 0, 0, 0, False)[0],wraplength=30,
                            font="Arial 10").place(x=600, y =50)
                elif algorithm == "Random":
                    Label(window, text=plan.runalgorithm("Random", 0, int(n4.get()),
                            0, 0, 0, 0, 0, 0, False)[0], wraplength=30,
                            font="Arial 10").place(x=600, y =50)
                elif algorithm == "genetic":
                    Label(window, text=plan.runalgorithm("genetic", 0, 0,
                            0, 0, 0, 0, 0, 0, False)[0], wraplength=30,
                            font="Arial 10").place(x=600, y =50)
            else:
                print("Fill in all the fields.")

        def boxplot():
            """
            GUI FUNCTION.
            Returns a boxplot for a given algorithm of x iterations and n runs.
            """
            # Check for input in all the fields
            if n.get() and x.get() and n2.get() and x2.get() and t1.get() \
                    and t2.get() and type.get() and n3.get() and x3.get() \
                    and p3.get() and t3.get() and n4.get():
                plan.compare_algorithm(int(n4.get()), int(x.get()), int(n.get()),
                                    int(hc2n.get()), int(hc2x.get()),
                                    int(x2.get()), int(n2.get()), float(t1.get()),
                                    float(t2.get()), type.get(), var3.get(),
                                    var1.get(), var2.get(), var4.get())

        def plot(algorithm):
            """
            GUI FUNCTION.
            Returns a plot of 1 run (n = 1) of a given algorithm.
            """

            # Print the waiting text
            print("Generating a plot...")
            print("May take a minute or 2...")
            print("Or 4...")
            print("Exit at any moment using 'ctr + c'.")

            # Get the points
            if algorithm == "hill climber":
                points = plan.runalgorithm(algorithm, int(x.get()), 1,
                        float(t1.get()), float(t2.get()),type.get(), 0, 0, 0, False)[2]
            elif algorithm == "Simulated annealing":
                points = plan.runalgorithm(algorithm, int(x2.get()), 1,
                        float(t1.get()), float(t2.get()),type.get(), 0, 0, 0, False)[2]

            # Make a plot
            plt.plot(points, 'b')
            plt.xlabel("Iterations")
            plt.ylabel("Points")
            plt.show()

        # Add labels to the hill climber input
        Label(window, text="Hill climber: ", font="Arial 15 bold").grid(column=1)
        Label(window, text="Iterations: ").grid(row=1)
        Label(window, text="Runs (n): ").grid(row=2)
        x = Entry(window)
        n = Entry(window)
        x.grid(row=1, column=1)
        n.grid(row=2, column=1)
        x.insert(10,"20000")
        n.insert(10,"1")
        x.bind('<Return>', lambda _: printresults("hc"))
        n.bind('<Return>', lambda _: printresults("hc"))

        # Add labels to the hill climber extended input
        Label(window, text="Hill climber extended: ",
                font="Arial 15 bold").grid(column=1)
        Label(window, text="Iterations: ").grid(row=4)
        Label(window, text="Runs (n): ").grid(row=5)
        hc2x = Entry(window)
        hc2n = Entry(window)
        hc2x.grid(row=4, column=1)
        hc2n.grid(row=5, column=1)
        hc2x.insert(10,"20000")
        hc2n.insert(10,"1")
        hc2x.bind('<Return>', lambda _: printresults("hc2"))
        hc2n.bind('<Return>', lambda _: printresults("hc2"))

        # Add labels to simmulated annealing input
        Label(window, text="Simulated annealing: ",
                font="Arial 15 bold").grid(column=1)
        Label(window, text="Iterations: ").grid(row=8)
        Label(window, text="Runs (n): ").grid(row=9)
        Label(window, text="Begin temperature: ").grid(row=10)
        Label(window, text="End temperature: ").grid(row=11)
        Label(window, text="exponential | logaritmic").grid(row=12)
        x2 = Entry(window)
        n2 = Entry(window)
        t1 = Entry(window)
        t2 = Entry(window)
        type = Entry(window)
        x2.grid(row=8, column=1)
        n2.grid(row=9, column=1)
        t1.grid(row=10, column=1)
        t2.grid(row=11, column=1)
        type.grid(row=12, column=1)
        x2.insert(10,"20000")
        n2.insert(10,"1")
        t1.insert(10,"3")
        t2.insert(10,"0.1")
        type.insert(10,"logaritmic")
        x2.bind('<Return>', lambda _: printresults("sa"))
        n2.bind('<Return>', lambda _: printresults("sa"))
        t1.bind('<Return>', lambda _: printresults("sa"))
        t2.bind('<Return>', lambda _: printresults("sa"))
        type.bind('<Return>', lambda _: printresults("sa"))

        # Add labels to genetic input
        Label(window, text="Genetic algorithm:", \
            font="Arial 15 bold").grid(column=1)
        Label(window, text="Population: ").grid(row=14)
        Label(window, text="Gnerations: ").grid(row=15)
        Label(window, text="Runs (n): ").grid(row=16)
        Label(window, text="k-way | rank | random").grid(row=17)
        x3 = Entry(window)
        p3 = Entry(window)
        n3 = Entry(window)
        t3 = Entry(window)
        x3.grid(row=14, column=1)
        p3.grid(row=15, column=1)
        n3.grid(row=16, column=1)
        t3.grid(row=17, column=1)
        x3.insert(10,"50")
        p3.insert(10,"10")
        n3.insert(10,"3")
        t3.insert(10,"k-way")
        x3.bind('<Return>', lambda _: printresults("genetic"))
        p3.bind('<Return>', lambda _: printresults("genetic"))
        n3.bind('<Return>', lambda _: printresults("genetic"))
        t3.bind('<Return>', lambda _: printresults("genetic"))

        # Add labels to random algorithm
        Label(window, text="Random schedule:",
            font="Arial 15 bold").grid(column=1)
        Label(window, text="Runs(n): ").grid(row=19)
        n4 = Entry(window)
        n4.grid(row=19, column=1)
        n4.insert(10,"10")
        n4.bind('<Return>', lambda _: printresults("Random"))
        # TODO: beginwaardes

        # Add choice to make a plot of certain algorithms
        var1 = IntVar()
        Checkbutton(window, text="Hill climber",
                    variable=var1).grid(row=21, column=5, sticky=W)
        var2 = IntVar()
        Checkbutton(window, text="Hill climber extended",
                    variable=var2).grid(row=22, column= 5,sticky=W)
        var3 = IntVar()
        Checkbutton(window, text="Random",
                    variable=var3).grid(row=23, column= 5,sticky=W)
        var4 = IntVar()
        Checkbutton(window, text="Simulated Annealing",
                    variable=var4).grid(row=24, column= 5,sticky=W)
        Button(window, text="Make a boxplot!",
                command=lambda:boxplot()).grid(row=25, column=5, sticky=W, pady=4)
        Button(window, text='Quit',
                command=window.quit).grid(row=25, column=7, sticky=W, pady=4)

        # Add buttons to plot a line chart
        ttk.Button(window, text="Plot one hill climber run",
            command=lambda:plot("hill climber"), padding=5).place(x=40, y=540)
        ttk.Button(window, text="Plot one simmulated annealing run",
            command=lambda:plot("Simulated annealing"), padding=5).place(x=40, y=580)

        Label(window, text="Select an algorithm and press enter to run. ").place(x=40, y =620)
        Label(window, text="View the schedule at 'results/schedule.html'.",\
            font="Arial 15 bold").place(x = 40, y = 660)

        window.mainloop()


    def save_html(self, schedule, rooms, spread_points, capacity_points, lecture_points, mutual_course_malus):
        """
        Save the schedule and its points to a html to visualize schedule.
        """
        # Save schedule for a different schedule visualisation
        schedule1 = copy.copy(schedule)

        # Make a table for all the schedule points
        d = pd.Series([lecture_points, -mutual_course_malus, "", spread_points, capacity_points, spread_points - capacity_points])
        d = pd.DataFrame(d)
        d.columns = ["Points"]
        d.index = ["Incorrectly placed lectures", "Incorrectly placed courses with 'mutual' courses", "", "Spread bonus points (out of 440)", "Capacity malus points (out of 1332)", "Total points"]

        # Add rooms to every timeslot
        flatten = np.array(schedule).flatten()
        counter = 0
        for i in range(len(flatten)):
            if flatten[i].name is not ' ':
                flatten[i] = str(flatten[i]) + " : " + str(rooms[counter])
            counter += 1
            counter = counter % 7
        # Convert back to 1D list
        schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

        # Make a big schedule for the whole week
        df = pd.DataFrame(schedule1)
        pd.set_option('display.max_colwidth', 600)
        df.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
        df.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # Transpose rows and columns
        df = df.T

        # Make seperate schedules for every day in the week
        test = pd.DataFrame(schedule)
        pd.set_option('display.max_colwidth', 600)
        test.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
        test.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # Transpose rows and columns
        test = test.T

        # Determine column names
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

        # dataframes will be added to the html_string
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

        with open('results/schedule.html', 'w') as f:
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

    def end(self, schedule, courses_schedule):
        """
        Prints text to tell user how many schedules were made and how long it took to make.
        """
        print("Succes! :-)")
        print("It took:", round(time.time() - plan.then, 3), "seconds, = ", round((time.time() - plan.then) / 60, 3), "minutes.")
        print("Made", plan.schedule_counter, "schedule(s).")
        print("Points:", Constraint.session_spread_check(schedule, plan.courses, courses_schedule)[0]
              - Constraint.students_fit(schedule, plan.courses, courses_schedule), "out of 440.")

    def points_to_print(self, schedule):
        """
        Gets all the points of a schedule for every constraint.
        """

        courses_schedule = Constraint.all_constraints(schedule, plan.courses)
        spread_points = Constraint.session_spread_check(schedule, plan.courses, courses_schedule)[0]
        capacity_points = (Constraint.students_fit(schedule, plan.courses, courses_schedule))
        lecture_points = Constraint.lecture_first(schedule, plan.courses, courses_schedule)
        mutual_course_malus = Constraint.mutual_courses_check(schedule, plan.courses)

        return courses_schedule, spread_points, capacity_points, lecture_points, mutual_course_malus


if __name__ == "__main__":
    plan = Plan()
    plan.generate()
