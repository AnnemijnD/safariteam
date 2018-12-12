
"""
Hill climber algorithm: generates a schedule that fulfills certain constraints
by accepting a schedule with higher points.
"""

from constraint import Constraint
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
    points = []
    counter = 0
    OPTIMUM = 45

    while counter < iterations:
        # Append points to show in a graph when the schedule is made
        points.append(get_points(schedule, courses))
        # Count the number of schedules made
        schedule_counter += 1
        # Save the first schedule
        schedule1 = schedule
        # Get points of the first schedule
        schedule1_points = Constraint.get_points(schedule1, courses)
        # Make a new schedule by switching random sessions. Amount of sessions
        # switched starts high and ends low.
        schedule2 = Constraint.switch_session(schedule, 1, -1, courses)
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
        # If a limit is reached, change the number of switches to 1, resulting
        # in a higher chance of finding schedule with more points. The disadvantage
        # is that it (could) take longer to find a good schedule.
        if schedule_counter == LIMIT:
            if Constraint.get_points(schedule, courses) == MAXPOINTS:
                return schedule, points, schedule_counter
        # Make a forced switch if an optimum is reached for the number of times
        # that a schedule was rejected.
        if accept_counter > OPTIMUM:
            schedule = Constraint.switch_session(schedule, 1, -1, courses)
            accept_counter = 0

    # Append last points of the new schedule to make a full plot of the points
    points.append(Constraint.get_points(schedule, courses))
    print("Max points:", max(points))

    # Return the generated schedule and its points :-)
    return schedule, points, schedule_counter


def makeplot(points):
    """
    DEZE KAN WEGGEHAALD WORDEN ZODRA WE HET NIET MEER WILLEN TESTEN
    """
    plt.plot(points)
    plt.ylabel("Points")
    plt.show()
