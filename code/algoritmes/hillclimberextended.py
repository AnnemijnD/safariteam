
from constraint import Constraint
import schedulemaker


def climb(schedule, courses, iterations):
    """
    Hill climber algorithm: generates a schedule that fulfills certain
    constraints by accepting a schedule with higher points and accepting lower
    points if x number of schedules were rejected.
    Input: random schedule and number of iterations;
    Output is a schedule that fulfills all hard constraints
    and most soft constraints.
    """

    accept_counter = 0
    points = []
    counter = 0
    x = 50

    while counter < iterations:
        counter += 1
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
            accept_counter = 0
        # if the second schedule has less points, go back to the old schedule.
        else:
            schedule = schedule1
            accept_counter += 1

        # make a forced switch if an optimum is reached for the number of times
        # hat a schedule was rejected.
        if accept_counter > x:
            schedule = schedulemaker.switch_session(schedule, 1)
            accept_counter = 0

    # append last points of the new schedule to make a full plot of the points
    points.append(Constraint.get_points(schedule, courses))

    # Return the generated schedule and its points :-)
    return schedule, points
