
"""
Vanuit een random rooster wordt een rooster gegenereerd waarbij alle
hoorcolleges voor de andere sessies geplaatst zijn.
"""

from constraint import Constraint
import switch
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from random import randint


SESSION_LEN = 72
LIMIT = 3000
OPTIMUM = 10000
COURSECOUNT = 29
MUTUALCOURSES = 33
LECTURECOUNT = 39
SLOTS = 140
SPREADPOINTS = 440

CHILDREN = 2


def genetic_algortim(schedule1, schedule2):
    """
    Dit gaat ooit een genetisch algortime worden.

    Begin met twee roosters combineren:
    PSEUDO:
    - maak lineaire lijst van beide roosters
    -

    PROBLEEM:
    HET GAAT FOUT MET EMPTY SESSIES EN DAAR WORDT IK VERDRIETIG VAN
    """
    flatten1 = np.array(schedule1).flatten().tolist()
    flatten2 = np.array(schedule2).flatten().tolist()

    cycles = []
    start_point = randint(0, SLOTS - 1)

    for i in range(CHILDREN):
        cycle_i = []
        index = flatten1.index(flatten1[start_point])
        in_cycle = [index]
        counter = 0

        while flatten1[start_point] not in cycle_i:
            print(counter)
            counter += 1
            temp = flatten2[index]
            cycle_i.append(temp)
            index = flatten1.index(temp)
            in_cycle.append(index)

        cycles.append(cycle_i)

        start_point = randint(0, SLOTS - 1)
        while start_point in in_cycle:
            start_point = randint(0, SLOTS - 1)

    print(cycles)


    #     cycle_i = []
    #     index = np.where(flatten1 == flatten1[start_point])
    #     in_cycle = [index]
    #     # counter = 0
    #     print(f"index: {index}")
    #     print(f"start_pint {flatten1[start_point]}")
    #     # while flatten1[start_point] not in cycle_i:
    #         # print(counter)
    #         # counter += 1
    #     temp = flatten2[index]
    #     print(f"temp: {temp}")
    #     cycle_i.append(temp)
    #     print(f"cycle_i {cycle_i}")
    #     # index = flatten1.index(temp)
    #     index = np.where(flatten1 == temp)
    #     in_cycle.append(index)
    #
    #     cycles.append(cycle_i)
    #
    #     start_point = randint(0, SLOTS - 1)
    #     while start_point in in_cycle:
    #         start_point = randint(0, SLOTS - 1)
    #
    # print(f"cycles: {cycles}")
SAVELIMIT = 3000


def hard_constraints(schedule, courses, schedule_counter):

    points = []

    # Begin met een rooster
    save_schedule = schedule
    # Ga door totdat alle hoorcolleges voor de andere sessies zijn ingeroosterd,
    # Dus totdat de lecture_first functie True is.
    # Om de code te met dit algoritme helemaal te runnen dan zet je hier
    # de bovenste regel weer 'aan'! (even ont-commenten)

    while Constraint.lecture_first(schedule, courses)[0] is False or \
            Constraint.own_sessions_check(schedule, courses)[1] < COURSECOUNT or \
            Constraint.mutual_courses_check(schedule, courses)[1] > 0:

        points.append(Constraint.lecture_first(schedule, courses)[1] + \
                      Constraint.own_sessions_check(schedule, courses)[1] - \
                      Constraint.mutual_courses_check(schedule, courses)[1])
        schedule_counter += 1
        # Bewaar het eerste rooster
        schedule1 = schedule
        lecture_points1 = Constraint.lecture_first(schedule1, courses)[1]
        own_session_points1 = Constraint.own_sessions_check(schedule1, courses)[1]
        mutual_points1 = Constraint.mutual_courses_check(schedule1, courses)[1]
        # Maak een nieuw roosters
        # 5 dingen per keer switchen gaat iets sneller dan 1 per keer
        schedule2 = switch.switch_session(schedule, 3)
        # Bereken de punten van het nieuwe rooster
        lecture_points2 = Constraint.lecture_first(schedule2, courses)[1]
        own_session_points2 = + Constraint.own_sessions_check(schedule2, courses)[1]
        mutual_points2 = Constraint.mutual_courses_check(schedule2, courses)[1]
        # Als deze hetzelfde aantal of meer punten heeft, accepteer dit rooster dan.
        if lecture_points2 >= lecture_points1 and own_session_points2 >= own_session_points1 \
                and mutual_points2 <= mutual_points1:
            # Accepteer dit rooster
            schedule = schedule2
        # Als deze minder punten heeft, ga dan terug naar het vorige rooster
        else:
            schedule = schedule1

    points.append(Constraint.lecture_first(schedule, courses)[1] + \
                  Constraint.own_sessions_check(schedule, courses)[1] - \
                  Constraint.mutual_courses_check(schedule, courses)[1])


    return schedule, points, schedule_counter, Constraint.own_sessions_check(schedule, courses)[1]


def soft(schedule, courses, schedule_counter):
    """
    Generates a schedule using a hill climber algorithm.
    Input is a random schedule, output is a schedule that fulfills all hard-
    and soft constraints.
    """

    switcher = 3
    points = []

    while Constraint.lecture_first(schedule, courses)[0] is False or \
            Constraint.own_sessions_check(schedule, courses)[1] < COURSECOUNT or \
            Constraint.mutual_courses_check(schedule, courses)[1] > 0 or \
            Constraint.session_spread_check(schedule, courses) < 350 or \
            Constraint.students_fit(schedule, courses) > 50:
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
        schedule2 = switch.switch_session(schedule, switcher)
        # Get points of the new (not yet accepted) schedule
        schedule2_points = get_points(schedule2, courses)
        # Accept new schedule if it has more points that the old schedule.
        # Also accept schedules with equal number of points for a higher chance
        # of finding a solution!
        if schedule2_points >= schedule1_points:
            schedule = schedule2
        # If the second schedule has less points, go back to the old schedule.
        else:
            schedule = schedule1
        # If a limit is reached, change the number of switches to 1, resulting
        # in a higher chance of finding schedule with more points. Disadvantage
        # is that it takes longer to find a good schedule.
        if schedule_counter % LIMIT == 0:
            switcher = 1

        # # Force a change in the schedule at a local optimum
        # if schedule_counter % OPTIMUM == 0:
        #     schedule = switch.switch_session(schedule, switcher)

    # Append last points of the new schedule
    points.append(get_points(schedule, courses))

    # Return the generated schedule and its points
    return schedule, points, schedule_counter, Constraint.own_sessions_check(schedule, courses)[1]


def get_points(schedule, courses):
    """
    Returns the points of a given schedule. Some constraint checks return
    negative points, so these are substracted in stead of added to the points.
    """
    points = Constraint.lecture_first(schedule, courses)[1] + \
            Constraint.own_sessions_check(schedule, courses)[1] - \
            Constraint.mutual_courses_check(schedule, courses)[1] + \
            Constraint.session_spread_check(schedule, courses) - \
            Constraint.students_fit(schedule, courses)

    return points

def makeplot(points):
    """
    Plots a graph of all the points on the y-axis and number of schedules
    on the x-axis.
    """
    plt.plot(points)
    plt.ylabel("Points")
    plt.show()
