
"""
SIMULATED ANNEALING TEST
"""

from constraint import Constraint
import schedulemaker
import matplotlib
import math
from random import randint
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

CYCLES = 5
OPTIMUM = 200
LIMIT = 500
MAXPOINTS = 440


def anneal(schedule, courses, schedule_counter, total_iterations, begin_temperature, end_temperature, type):
    """
    Generates a schedule using a hill climber algorithm.
    Input is a random schedule, output is a schedule that fulfills all hard-
    constraints and most soft constraints.
    """

    accept_counter = 0
    accept_max = 25
    points = []
    # begin_temperature = 4
    # end_temperature = 0.01

    # Sigmodial:
    # temp = end_temperature + (begin_temperature - end_temperature) / (1 + math.exp(0.3 * (i - total_iterations/2)))



    for i in range(0, total_iterations):

        # Get cooling scheme
        if type == "exponential":
            temp = begin_temperature * math.pow((end_temperature / begin_temperature),  (i / total_iterations))
        else:
            # Geman cooling scheme
            temp = begin_temperature / math.log(i + 2)

        points.append(Constraint.get_points(schedule, courses))
        # Append points to show in a graph when the schedule is made
        points.append(Constraint.get_points(schedule, courses))
        # Count the number of schedules made
        schedule_counter += 1
        # Save the first schedule
        schedule1 = schedule
        # Get points of the first schedule
        schedule1_points = Constraint.get_points(schedule1, courses)
        # Make a new schedule by switching random sessions. Amount of sessions
        # switched starts high and ends low.
        schedule2 = schedulemaker.switch_session(schedule, 1, -1)
        # Get points of the new (not yet accepted) schedule
        schedule2_points = Constraint.get_points(schedule2, courses)
        # Accept new schedule if it has more points that the old schedule.
        # Also accept schedules with equal number of points for a higher chance
        # of finding a solution.
        if schedule2_points >= schedule1_points: # or schedule2_points - schedule1_points < verschil:
            schedule = schedule2
            accept_counter = 0
        else: # deze else moet even anders
            schedule = schedule1
            accept_counter += 1
        # Bij vastlopen
        if accept_counter > accept_max:
            diff = schedule2_points - schedule1_points
            # Pas simulated annealing toe
            if randint(0, 100) < (math.exp(diff / temp) * 100):
                schedule = schedule2

    # Append last points of the new schedule to make a full plot of the points
    points.append(Constraint.get_points(schedule, courses))
    print("Max points:", max(points))

    # Return the generated schedule and its points :-)
    return schedule, points, schedule_counter
