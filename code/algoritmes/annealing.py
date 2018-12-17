from constraint import Constraint
import schedulemaker
import math
import random


def anneal(schedule, courses, total_iterations, t1, t2, type):
    """
    Simulated annealing algorithm

    Input: random schedule, number of iterations, begin- and end
    temperature.
    Output: a schedule that fulfills all hard constraints
    and most soft constraints.
    """

    points = []

    # sigmodial:
    # temp = t2 + (t1 - t2) / (1 + math.exp(0.3 * (i - total_iterations/2)))

    for i in range(0, total_iterations):

        # get cooling scheme
        if type == "exponential":
            temp = t1 * math.pow((t2 / t1),
                                 (i / total_iterations))
        elif type == "logarithmic":
            temp = t1 / math.log(i + 2)

        # append points to show in a graph when the schedule is made
        points.append(Constraint.get_points(schedule, courses))

        # save the first schedule
        schedule1 = schedule

        # get points of the first schedule
        schedule1_points = Constraint.get_points(schedule1, courses)

        # make a new schedule by switching random sessions. Amount of sessions
        # switched starts high and ends low.
        schedule2 = schedulemaker.switch_session(schedule, 1)

        # get points of the new (not yet accepted) schedule
        schedule2_points = Constraint.get_points(schedule2, courses)

        # accept new schedule if it has more points that the old schedule.
        # also accept schedules with equal number of points for a higher chance
        # of finding a solution.
        if schedule2_points >= schedule1_points:
            schedule = schedule2

        # ff the acceptance chance is higher than a random number
        # between 0 and 1, force to accept a schedule
        if random.random() < math.exp((schedule2_points - schedule1_points) / temp):
            schedule = schedule2

    # append last points of the new schedule to make a full plot of the points
    points.append(Constraint.get_points(schedule, courses))

    # return the generated schedule and its points :-)
    return schedule, points
