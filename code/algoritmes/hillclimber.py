
"""
Hill climber algorithm: generates a schedule that fulfills certain constraints
by accepting a schedule with higher points.
"""

from constraint import Constraint
import switch
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

CYCLES = 30000
OPTIMUM = 45
LIMIT = 500
MAXPOINTS = 440


def soft_constraints(schedule, courses, schedule_counter):
    """
    Generates a schedule using a hill climber algorithm.
    Input is a random schedule, output is a schedule that fulfills all hard-
    constraints and most soft constraints.
    """

    switcher = 1
    accept_counter = 0
    points = []

    # while Constraint.lecture_first(schedule, courses) > 0 or \
    #         Constraint.mutual_courses_check(schedule, courses) > 0 or \
    #         Constraint.session_spread_check(schedule, courses) < -200 or \
    #         Constraint.students_fit(schedule, courses) > 1300:
    while schedule_counter < CYCLES:
        # Append points to show in a graph when the schedule is made
        points.append(get_points(schedule, courses))
        # Count the number of schedules made
        schedule_counter += 1
        # Save the first schedule
        schedule1 = schedule
        # Get points of the first schedule
        schedule1_points = get_points(schedule1, courses)
        # Make a new schedule by switching random sessions. Amount of sessions
        # switched starts high and ends low.
        schedule2 = switch.switch_session(schedule, switcher, -1)
        # Get points of the new (not yet accepted) schedule
        schedule2_points = get_points(schedule2, courses)
        # Accept new schedule if it has more points that the old schedule.
        # Also accept schedules with equal number of points for a higher chance
        # of finding a solution.
        if schedule2_points >= schedule1_points:
            schedule = schedule2
            accept_counter = 0
            # Set a boolian for when a schedule is accepted
        # If the second schedule has less points, go back to the old schedule.
        else:
            schedule = schedule1
            accept_counter += 1
        # If a limit is reached, change the number of switches to 1, resulting
        # in a higher chance of finding schedule with more points. The disadvantage
        # is that it (could) take longer to find a good schedule.
        if schedule_counter == LIMIT:
            switcher = 1
            if get_points(schedule, courses) == MAXPOINTS:
                return schedule, points, schedule_counter
        # When a local optimum is found:
        # Make a forced switch if an optimum is reached for the number of times
        # that a schedule was rejected. For example: if a random schedule with less
        # points was rejected a 100 times, force a new schedule (with less points).
        if accept_counter > OPTIMUM:
            print("found optimum")
            schedule = switch.switch_session(schedule, switcher, -1)
            accept_counter = 0

            # ROEP HIER DE FUNCTIE SIMULATED ANNEALING AAN???


    # Append last points of the new schedule to make a full plot of the points
    points.append(get_points(schedule, courses))

    # Return the generated schedule and its points :-)
    return schedule, points, schedule_counter


def get_points(schedule, courses):
    """
    Returns the points of a given schedule. Some constraint checks return
    negative points, so these are substracted in stead of added to the points.
    Minimum minus points for lecture_first = 0, maxmimum = 39.
    Minimum of 'minus points' of mutual_course() = 0.
    Maximum of 'good points' of session_spread_check() = 440.
    Minimum of malus points of students_fit() = 0 and maxmimum = 1332.
    Multiply the points of the hard constraints (lecture_first and mutual_courses)
    to ensure that a schedule fulfills these constraints.
    """
    course_schedule = Constraint.all_constraints(schedule, courses)

    points = Constraint.session_spread_check(schedule, courses, course_schedule)[0] - \
            (Constraint.lecture_first(schedule, courses, course_schedule) * 40) - \
            (Constraint.mutual_courses_check(schedule, courses) * 40) - \
            (Constraint.students_fit(schedule, courses, course_schedule) / 4)

    return points

def makeplot(points):
    """
    DEZE KAN WEGGEHAALD WORDEN ZODRA WE HET NIET MEER WILLEN TESTEN
    """
    plt.plot(points)
    plt.ylabel("Points")
    plt.show()
