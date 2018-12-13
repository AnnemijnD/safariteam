
"""
Hill climber algorithm: generates a schedule that fulfills certain constraints
by accepting a schedule with higher points.
"""

from constraint import Constraint
import schedulemaker
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def climb(schedule, courses, schedule_counter, iterations):
    """
    Generates a schedule using a hill climber algorithm.
    Input is a random schedule, output is a schedule that fulfills all hard-
    constraints and most soft constraints.
    """

    accept_counter = 0
    counter = 0
    points = []

    while counter < iterations and accept_counter < 60:
        # Append points to show in a graph when the schedule is made
        points.append(Constraint.get_points(schedule, courses))
        counter += 1
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
        if schedule2_points >= schedule1_points:
            schedule = schedule2
            accept_counter = 0
        # If the second schedule has less points, go back to the old schedule.
        else:
            schedule = schedule1
            accept_counter += 1

    # Append last points of the new schedule to make a full plot of the points
    points.append(Constraint.get_points(schedule, courses))

    # Return the generated schedule and its points :-)
    return schedule, points, schedule_counter
