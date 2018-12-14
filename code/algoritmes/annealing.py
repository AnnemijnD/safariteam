
"""
Simulated annealing algorithm.
Input is a (valid) schedule, number of iterations, begin- and end temperature.
Output is a schedule (with more points than the input schedule).
"""

from constraint import Constraint
import schedulemaker
import math
import random

CYCLES = 5
OPTIMUM = 200
LIMIT = 500
MAXPOINTS = 440


def anneal(schedule, courses, total_iterations, begin_temperature, end_temperature, type):
    """
    Generates a schedule using a hill climber algorithm.
    Input is a random schedule, output is a schedule that fulfills all hard-
    constraints and most soft constraints.
    """

    accept_counter = 0
    points = []

    # Sigmodial:
    # temp = end_temperature + (begin_temperature - end_temperature) / (1 + math.exp(0.3 * (i - total_iterations/2)))

    for i in range(0, total_iterations):

        # Get cooling scheme
        if type == "exponential":
            temp = begin_temperature * math.pow((end_temperature / begin_temperature),  (i / total_iterations))
        elif type == "logarithmic":
            temp = begin_temperature / math.log(i + 2)

        points.append(Constraint.get_points(schedule, courses))
        # Append points to show in a graph when the schedule is made
        points.append(Constraint.get_points(schedule, courses))
        # Save the first schedule
        schedule1 = schedule
        # Get points of the first schedule
        schedule1_points = Constraint.get_points(schedule1, courses)
        # Make a new schedule by switching random sessions. Amount of sessions
        # switched starts high and ends low.
        schedule2 = schedulemaker.switch_session(schedule, 1)
        # Get points of the new (not yet accepted) schedule
        schedule2_points = Constraint.get_points(schedule2, courses)
        # Accept new schedule if it has more points that the old schedule.
        # Also accept schedules with equal number of points for a higher chance
        # of finding a solution.
        if schedule2_points >= schedule1_points:
            schedule = schedule2
            accept_counter = 0
        else:
            schedule = schedule1
            accept_counter += 1
        # Apply simmulated annealing
        diff = schedule2_points - schedule1_points
        # If the acceptance chance is higher than a random number
        # between 0 and 1, force to accept a schedule
        if random.random() < math.exp(diff / temp):
            schedule = schedule2

    # Append last points of the new schedule to make a full plot of the points
    points.append(Constraint.get_points(schedule, courses))

    # Return the generated schedule and its points :-)
    return schedule, points
