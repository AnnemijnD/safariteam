import os, sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "results"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algoritmes"))

from constraint import Constraint
import loaddata
import schedulemaker
import genetic
import annealing
import hillclimberextended
import hillclimber
import schedule_to_html
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
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

        # load all the courses, rooms and sessions
        plan.courses = loaddata.load_courses()
        plan.rooms = loaddata.load_rooms()
        plan.own_session_points = 0

        # make random valid schedule to start with;
        # a valid schedule is a schedule that fulfills al hard constraints
        schedule = schedulemaker.initialize_schedule(plan.courses)

        print("Opening GUI...")
        plan.gui(schedule, plan.courses, True)

    def runalgorithm(self, algorithm, x, n, begin_temperature,
                     end_temperature, type, pop, gen, gen_type, input_sched):
        """
        Run a certain algorithm for n number of times with x number of
        iterations. Algorithm input can be: "hill climber", "hill climber ext",
        "genetic", "simulated annealing", or "Random".
        Output is a list of maximum points that the algorithm reached or
        the schedule that reached max points.
        """

        maxpoints = []
        max_schedule = None

        for i in range(n):
            if not bool(input_sched):
                first_schedule = schedulemaker.initialize_schedule(plan.courses)
            else:
                first_schedule = input_sched
            # call algorithm
            if algorithm == "hill climber":
                schedule_temp, points =  \
                    hillclimber.climb(first_schedule, plan.courses, x)

                if max_schedule is None:
                    max_schedule = schedule_temp

                # save schedule with most points
                elif Constraint.get_points(schedule_temp, plan.courses) > \
                        Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = schedule_temp

            if algorithm == "hill climber ext":
                schedule_temp, points = \
                    hillclimberextended.climb(first_schedule, plan.courses, x)

                if max_schedule is None:
                    max_schedule = schedule_temp

                # again, save schedule with most points
                elif Constraint.get_points(schedule_temp, plan.courses) > \
                        Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = schedule_temp

            elif algorithm == "Random":
                points = Constraint.get_points(first_schedule, plan.courses)

                if max_schedule is None:
                    max_schedule = first_schedule

                elif Constraint.get_points(first_schedule, plan.courses) > \
                        Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = first_schedule

            elif algorithm == "Simulated annealing":
                schedule_temp, points = \
                    annealing.anneal(first_schedule, plan.courses,
                                     x, begin_temperature, end_temperature, type)

                if max_schedule is None:
                    max_schedule = schedule_temp

                elif Constraint.get_points(schedule_temp, plan.courses) > \
                        Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = schedule_temp

            elif algorithm == "genetic":
                # Make schedules
                schedules = []
                for i in range(pop):
                    schedules.append(schedulemaker.initialize_schedule(plan.courses))
                    # Run the algorithm
                    schedule_temp, points = genetic.genetic_algorithm(schedules,
                                            plan.courses, pop, gen, gen_type)
                points = genetic.genetic_algorithm(schedules, plan.courses,
                                                   pop, gen, gen_type)[1]
                if max_schedule is None:
                    max_schedule = schedule_temp

                elif Constraint.get_points(schedule_temp, plan.courses) > \
                        Constraint.get_points(max_schedule, plan.courses):
                    max_schedule = schedule_temp

            # save max points to a list
            if algorithm == "Random" or algorithm == "genetic":
                maxpoints.append(round(points))
            else:
                maxpoints.append(round(max(points)))

        print(algorithm, "reached max points of: ", maxpoints)

        # save schedule with highest points
        courses_schedule, spread_points, capacity_points, lecture_points, \
            mutual_course_malus = plan.points_to_print(max_schedule)
        schedule_to_html.save_html(max_schedule, plan.rooms, spread_points,
                                   capacity_points, lecture_points,
                                   mutual_course_malus)

        return maxpoints, max_schedule, points

    def compare_algorithm(self, random_n, hillclimber_x, hillclimber_n,
                          hillclimber2_x, hillclimber2_n, sim_x, sim_n,
                          begin_temp, end_temp, type, check_rand, check_hill,
                          check_hill2, check_sim, check_gen, gen_x, gen_n,
                          pop):
        """
        GUI FUNCTION.
        Run certain algorithms with the intention to compare them in a boxplot.
        Takes all arguments necessary to make plot. The check-arguments show
        whether a box for that type of algorithm was checked.
        Returns a boxplot.
        """

        # dict with all data for the boxplot
        boxplot_data = []
        boxplot_xaxis = []
        points = 0

        schedule = schedulemaker.initialize_schedule(plan.courses)

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
            max_points, max_schedule, points = plan.runalgorithm("hill climber ext",
                            hillclimber2_x, hillclimber2_n, 0, 0, None,
                            0, 0, 0, schedule)
            boxplot_data.append(max_points)
            boxplot_xaxis.append(f"Hillclimber extended \n n = {hillclimber2_n}")

        if check_sim == 1:
            max_points, max_schedule, points = plan.runalgorithm("Simulated annealing",
                                sim_x, sim_n, 0, 0, None, 0, 0, 0, schedule)
            boxplot_data.append(max_points)
            boxplot_xaxis.append(f"Simulated Annealing \n n = {sim_n}")

        if check_gen == 1:
            max_points, max_schedule, points = plan.runalgorithm("genetic",
                                0, gen_n, 0, 0, None,
                                pop, gen_x, 0, schedule)
            boxplot_data.append(max_points)
            boxplot_xaxis.append(f"Genetic \n n = {pop}")

        # make the plot of selected checkboxes
        ax = plt.subplot(111)
        plt.boxplot(boxplot_data)
        plt.xticks(fontsize=8)
        ax.set_xticklabels(boxplot_xaxis)
        plt.title("Comparing schedule points of different algorithms")
        plt.ylabel("Points")
        plt.xlabel("Algorithms \n (n = runs)")
        plt.show()

    def gui(self, schedule, courses, bool):
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

            print("Generating schedule(s)")
            print("May take a minute or 2...")
            print("Or 4...")
            print("Exit at any moment using 'ctr + c'.")

            # run the selected algorithm
            Label(window, text="Resulted points (out of 440): ") \
                .place(x=600, y=40)
            if algorithm == "hc":
                Label(window, text=plan.runalgorithm("hill climber",
                      int(x.get()), int(n.get()), 0, 0, 0, 0, 0, 0, False)[0],
                      wraplength=30, font="Arial 10").place(x=600, y=70)
            elif algorithm == "hc2":
                Label(window, text=plan.runalgorithm("hill climber ext",
                      int(hc2x.get()), int(hc2n.get()), 0, 0, 0, 0, 0, 0, False)[0],
                      wraplength=30, font="Arial 10").place(x=600, y=70)
            elif algorithm == "sa":
                Label(window, text=plan.runalgorithm("Simulated annealing",
                      int(x2.get()), int(n2.get()), float(t1.get()),
                      float(t2.get()), type.get(), 0, 0, 0, False)[0],
                      wraplength=30, font="Arial 10").place(x=600, y=70)
            elif algorithm == "Random":
                Label(window, text=plan.runalgorithm("Random", 0, int(n4.get()),
                      0, 0, 0, 0, 0, 0, False)[0], wraplength=30,
                      font="Arial 10").place(x=600, y=70)
            elif algorithm == "genetic":
                Label(window, text=plan.runalgorithm("genetic", 0,
                      int(n3.get()), 0, 0, 0, int(p3.get()), int(x3.get()),
                      (t3.get()), False)[0], wraplength=30,
                      font="Arial 10").place(x=600, y=70)

        def boxplot():
            """
            GUI FUNCTION.
            Returns a boxplot for a given algorithm of x iterations and n runs.
            """

            # input of compare_algorithm are checkboxes and text elements in GUI
            plan.compare_algorithm(int(n4.get()), int(x.get()), int(n.get()),
                                   int(hc2x.get()), int(hc2n.get()),
                                   int(x2.get()), int(n2.get()), float(t1.get()),
                                   float(t2.get()), type.get(), var3.get(),
                                   var1.get(), var2.get(), var4.get(), var5.get(),
                                   int(x3.get()), int(n3.get()), int(p3.get()))

        def plot(algorithm):
            """
            GUI FUNCTION.
            Input choices are; "hill climber", "simulated annealing" or "both".
            Returns a line chart of 1 run (n = 1) of a given algorithm.
            """

            print("Generating a plot...")
            print("May take a minute or 2...")
            print("Or 4...")
            print("Exit at any moment using 'ctr + c'.")

            # get the schedule points by running a given algorithm
            if algorithm == "hill climber":
                points = plan.runalgorithm(algorithm, int(x.get()), 1,
                                           float(t1.get()), 0, 0,
                        0, 0, 0, False)[2]
            elif algorithm == "Simulated annealing":
                points = plan.runalgorithm(algorithm, int(x2.get()), 1,
                                           float(t1.get()), float(t2.get()),
                                           type.get(), 0, 0, 0, False)[2]
            elif algorithm == "both":
                # plot a simulated annealing run after hill climber run
                maxpoints, max_schedule, points = plan.runalgorithm("hill climber",
                        int(x.get()), 1, float(t1.get()), float(t2.get()),
                        type.get(), 0, 0, 0, False)
                # start simulated annealing with the same schedule
                points += plan.runalgorithm("Simulated annealing", int(x2.get()),
                        1, float(t1.get()), float(t2.get()), type.get(),
                        0, 0, 0, max_schedule)[2]
            elif algorithm == "all":
                # plot a simulated annealing run after hill climber run
                schedule = schedulemaker.initialize_schedule(plan.courses)
                points1 = plan.runalgorithm("hill climber", int(x.get()), 1,
                                            float(t1.get()), 0, 0,
                                            0, 0, 0, schedule)[2]
                points2 = plan.runalgorithm("hill climber ext", int(hc2x.get()),
                                            1, 0, 0, None, 0, 0, 0, schedule)[2]
                points3 = plan.runalgorithm("Simulated annealing", int(x2.get()),
                                            1, float(t1.get()), float(t2.get()),
                                            type.get(), 0, 0, 0, schedule)[2]

            if algorithm == "all":
                plt.plot(points1, "b")
                plt.plot(points2, "r")
                plt.plot(points3, "yellow")

                # add a legend
                plt.plot([1], label="Hill climber", color="b")
                plt.plot([2], label="Hill climber extended", color="r")
                plt.plot([3], label="Simulated annealing", color="yellow")
                plt.legend(loc='upper left')
            else:
                plt.plot(points, 'b')

            # add labels
            plt.xlabel("Iterations", fontsize=12)
            plt.ylabel("Points", fontsize=12)
            plt.show()

        # add labels to the hill climber input
        Label(window, text="Hill climber: ", font="Arial 15 bold").grid(column=1)
        Label(window, text="Iterations: ").grid(row=1)
        Label(window, text="Runs (n): ").grid(row=2)
        x = Entry(window)
        n = Entry(window)
        x.grid(row=1, column=1)
        n.grid(row=2, column=1)
        x.insert(10, "30000")
        n.insert(10, "1")

        # Print results when enter is pressed
        x.bind('<Return>', lambda _: printresults("hc"))
        n.bind('<Return>', lambda _: printresults("hc"))

        # add labels to the hill climber extended input
        Label(window, text="Hill climber extended: ",
              font="Arial 15 bold").grid(column=1)
        Label(window, text="Iterations: ").grid(row=4)
        Label(window, text="Runs (n): ").grid(row=5)
        hc2x = Entry(window)
        hc2n = Entry(window)
        hc2x.grid(row=4, column=1)
        hc2n.grid(row=5, column=1)
        hc2x.insert(10, "30000")
        hc2n.insert(10, "1")

        # Print results when enter is pressed
        hc2x.bind('<Return>', lambda _: printresults("hc2"))
        hc2n.bind('<Return>', lambda _: printresults("hc2"))

        # add labels to simulated annealing input
        Label(window, text="Simulated annealing: ",
              font="Arial 15 bold").grid(column=1)
        Label(window, text="Iterations: ").grid(row=8)
        Label(window, text="Runs (n): ").grid(row=9)
        Label(window, text="Begin temperature: ").grid(row=10)
        Label(window, text="End temperature: ").grid(row=11)
        Label(window, text="Cooling scheme:").grid(row=12)

        # dropdown menu for cooling scheme
        mainframe_sim = Frame(window)
        mainframe_sim.grid(column=1, row=12)
        mainframe_sim.columnconfigure(0, weight=1)
        mainframe_sim.rowconfigure(0, weight=1)
        type = StringVar(window)
        choices = {'logarithmic', 'exponential'}
        type.set('exponential')
        popupMenu = OptionMenu(mainframe_sim, type, *choices)
        popupMenu.grid(row=2, column=1)
        x2 = Entry(window)
        n2 = Entry(window)
        t1 = Entry(window)
        t2 = Entry(window)
        x2.grid(row=8, column=1)
        n2.grid(row=9, column=1)
        t1.grid(row=10, column=1)
        t2.grid(row=11, column=1)
        x2.insert(10, "30000")
        n2.insert(10, "1")
        t1.insert(10, "5")
        t2.insert(10, "0.9")

        # Print results when enter is pressed
        x2.bind('<Return>', lambda _: printresults("sa"))
        n2.bind('<Return>', lambda _: printresults("sa"))
        t1.bind('<Return>', lambda _: printresults("sa"))
        t2.bind('<Return>', lambda _: printresults("sa"))

        # add labels to genetic input
        Label(window, text="Genetic algorithm:",
              font="Arial 15 bold").grid(column=1)
        Label(window, text="Population (even number, min = 10): ").grid(row=14)
        Label(window, text="Generations (min = 10): ").grid(row=15)
        Label(window, text="Runs (n): ").grid(row=16)
        Label(window, text="Way of choosing parents:").grid(row=17)

        # dropdown menu for way of choosing parents
        mainframe_gen = Frame(window)
        mainframe_gen.grid(column=1, row=17)
        mainframe_gen.columnconfigure(0, weight=1)
        mainframe_gen.rowconfigure(0, weight=1)
        t3 = StringVar(window)
        choices_gen = {'k-way', 'rank', 'random'}
        popupMenu = OptionMenu(mainframe_gen, t3, *choices_gen)
        popupMenu.grid(row=2, column=1)
        x3 = Entry(window)
        p3 = Entry(window)
        n3 = Entry(window)
        x3.grid(row=14, column=1)
        p3.grid(row=15, column=1)
        n3.grid(row=16, column=1)
        p3.insert(10, "50")
        x3.insert(10, "10")
        n3.insert(10, "1")
        t3.set('k-way')

        # Print results when enter is pressed
        x3.bind('<Return>', lambda _: printresults("genetic"))
        p3.bind('<Return>', lambda _: printresults("genetic"))
        n3.bind('<Return>', lambda _: printresults("genetic"))

        # add labels to random algorithm
        Label(window, text="Random schedule:",
              font="Arial 15 bold").grid(column=1)
        Label(window, text="Runs(n): ").grid(row=19)
        n4 = Entry(window)
        n4.grid(row=19, column=1)
        n4.insert(10, "10")
        n4.bind('<Return>', lambda _: printresults("Random"))

        # add choice to make a plot of certain algorithms
        var1 = IntVar()
        Checkbutton(window, text="Hill climber",
                    variable=var1).grid(row=21, column=2, sticky=W)
        var2 = IntVar()
        Checkbutton(window, text="Hill climber extended",
                    variable=var2).grid(row=22, column=2, sticky=W)
        var3 = IntVar()
        Checkbutton(window, text="Random",
                    variable=var3).grid(row=23, column=2, sticky=W)
        var4 = IntVar()
        Checkbutton(window, text="Simulated Annealing",
                    variable=var4).grid(row=24, column=2, sticky=W)
        var5 = IntVar()
        Checkbutton(window, text="Genetic",
                    variable=var5).grid(row=25, column=2, sticky=W)
        Button(window, text="Make a boxplot!",
               command=lambda: boxplot()).place(x=450, y=640)
        Button(window, text='Quit',
               command=window.quit).place(x=600, y=640)

        # add buttons to plot a line chart
        ttk.Button(window, text="Plot hill climber run",
                   command=lambda: plot("hill climber"),
                   padding=4).place(x=40, y=510)
        ttk.Button(window, text="Plot simulated annealing run",
                   command=lambda: plot("Simulated annealing"),
                   padding=4).place(x=40, y=540)
        ttk.Button(window, text="Plot simulated annealing after hill climber run",
                   command=lambda: plot("both"), padding=4).place(x=40, y=570)
        ttk.Button(window, text="All three algorithmms in one plot",
                   command=lambda: plot("all"), padding=4).place(x=40, y=600)

        Label(window, text="Select an algorithm and press enter to view scores.",
              font="Arial 10 bold").grid(row=0, column=2)
        Label(window, text="View the schedule at 'results/schedule.html'.",
              font="Arial 14 bold").place(x=40, y=640)

        window.mainloop()

    def points_to_print(self, schedule):
        """
        Gets all the points of a schedule for every constraint.
        """

        courses_schedule = Constraint.all_constraints(schedule, plan.courses)
        spread_points = Constraint.session_spread_check(schedule, plan.courses,
                                                        courses_schedule)
        capacity_points = (Constraint.students_fit(schedule, plan.courses,
                                                   courses_schedule))
        lecture_points = Constraint.lecture_first(schedule, plan.courses,
                                                  courses_schedule)
        mutual_course_malus = Constraint.mutual_courses_check(schedule, plan.courses)

        return courses_schedule, spread_points, capacity_points, \
            lecture_points, mutual_course_malus


if __name__ == "__main__":
    plan = Plan()
    plan.generate()
