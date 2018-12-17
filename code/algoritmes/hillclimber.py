from constraint import Constraint
import schedulemaker


def climb(schedule, courses, iterations):
    """
    Generates a schedule using a hill climber algorithm.
    Input: random schedule and number of iterations;
    Output: a schedule that fulfills all hard constraints
    and most soft constraints.
    """
    counter = 0
    points = []

    while counter < iterations:

        # append points to show in a graph when the schedule is made
        points.append(Constraint.get_points(schedule, courses))
        counter += 1

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

    # append last points of the new schedule to make a full plot of the points
    points.append(Constraint.get_points(schedule, courses))

    # return the generated schedule and its points :-)
    return schedule, points
