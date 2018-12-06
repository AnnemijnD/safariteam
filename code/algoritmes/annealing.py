
"""
SIMULATED ANNEALING TEST
"""

from constraint import Constraint
import switch
import matplotlib
import math
from random import randint
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

CYCLES = 5
OPTIMUM = 200
LIMIT = 500
MAXPOINTS = 440


def anneal(schedule, courses, schedule_counter):
    """
    Generates a schedule using a hill climber algorithm.
    Input is a random schedule, output is a schedule that fulfills all hard-
    constraints and most soft constraints.
    """

    switcher = 1
    accept_counter = 0
    points = []
    begin_temperature = 0.2
    end_temperature = 0.01
    total_iterations = 50000
    # Ti=  T0(Tn/  T0)  (i/  N)
    # Ti=  Tn+  (T0  -Tn)  /  (1  +  exp(0.3  (i-N/2)


    for i in range(1, total_iterations):
        # Geman:
        temperatuur = begin_temperature / math.log(i + 2)
        # print(temperatuur)
        # Exponential:
        # temperatuur = begin_temperature / pow((0.05 / begin_temperature), (i/total_iterations))
        # Sigmodiaal:
        # temperatuur = end_temperature + (begin_temperature - end_temperature) / (1 + math.exp(0.3 * (i - total_iterations/2)))
        points.append(get_points(schedule, courses))
        # Append points to show in a graph when the schedule is made
        # points.append(get_points(schedule, courses))
        print(points[-1])
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
        verkorting = schedule2_points - schedule1_points

        random_number = randint(0, 100)
        if schedule2_points >= schedule1_points: # or schedule2_points - schedule1_points < verschil:
            schedule = schedule2
            accept_counter = 0
        elif random_number < (math.exp(verkorting / temperatuur) * 100): # DIT IS DE ACCEPTATIEKANS
            # acceptatiekans = math.exp(verkorting / temperatuur) * 100
            # print("Accceptatiekans", acceptatiekans)
            # print(points[-1], (math.exp(verkorting / temperatuur) * 100))
            print("WAT IS DE WERELD TOCH MOOI MAAR OH JEE MINDER PUNTEN")
            # BEREKEN HIER DE KANS OM DE SLECHTERE ALSNOG AAN TE NEMEN
            # acceptatiekans = math.exp(-verschil / temperatuur)
            # print(acceptatiekans, (get_points(schedule, courses)))
            # random_number = randint(0, 100)
            # if random_number < acceptatiekans * 100:
            schedule = schedule2
        else:
            schedule = schedule1
            accept_counter += 1

    # Append last points of the new schedule to make a full plot of the points
    points.append(get_points(schedule, courses))
    print(max(points))

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
