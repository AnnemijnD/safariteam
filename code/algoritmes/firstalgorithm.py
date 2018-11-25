
"""
Vanuit een random rooster wordt een rooster gegenereerd waarbij alle
hoorcolleges voor de andere sessies geplaatst zijn.
"""

from constraint import Constraint
import switch
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

SESSION_LEN = 72
LIMIT = 700
COURSECOUNT = 29


def algorithm(schedule, courses, schedule_counter):

    points = []

    # Begin met een rooster
    save_schedule = schedule
    # Ga door totdat alle hoorcolleges voor de andere sessies zijn ingeroosterd,
    # Dus totdat de lecture_first functie True is.
    # Om de code te met dit algoritme helemaal te runnen dan zet je hier
    # de bovenste regel weer 'aan'! (even ont-commenten)

    while Constraint.lecture_first(schedule, courses)[0] is False:
            # Constraint.own_sessions_check(schedule, courses)[1] < SESSION_LEN - 20:
        points.append(Constraint.lecture_first(schedule, courses)[1])
        schedule_counter += 1
        # Bewaar het eerste rooster
        schedule1 = schedule
        # Maak een nieuw roosters
        # 5 dingen per keer switchen gaat iets sneller dan 1 per keer
        schedule2 = switch.switch_session(schedule, 6)
        # Als deze hetzelfde aantal of meer punten heeft, accepteer dit rooster dan.
        if Constraint.lecture_first(schedule2, courses)[1] >= Constraint.lecture_first(schedule1, courses)[1]:
           # Constraint.own_sessions_check(schedule2, courses)[1] >= Constraint.own_sessions_check(schedule1, courses)[1]:
            # Accepteer dit rooster
            schedule = schedule2
        # Als deze minder punten heeft, ga dan terug naar het vorige rooster
        else:
            schedule = schedule1
        # Als het rooster 10 punten verder is, bewaar het rooster dan om er
        # later op terug te kunnen komen
        if Constraint.lecture_first(schedule, courses)[1] % 10 == 0:
            schedule_10_points = schedule
        # Als het rooster vast blijft zitten, ga dan terug naar het originele
        # rooster of naar het bewaarde rooster.
        if schedule_counter % LIMIT == 0:
            if Constraint.lecture_first(schedule, courses)[1] % 10 == 0:
                if schedule_10_points:
                    schedule = schedule_10_points
                else:
                    schedule = save_schedule

    return schedule, points, schedule_counter, Constraint.own_sessions_check(schedule, courses)[1]


def session_algorithm(schedule, courses, schedule_counter):

    points = []

    # Begin met een rooster
    save_schedule = schedule

    while Constraint.own_sessions_check(schedule, courses)[1] < COURSECOUNT:
        # print(Constraint.own_sessions_check(schedule, courses)[1])
        points.append(Constraint.own_sessions_check(schedule, courses)[1])
        schedule_counter += 1
        # Bewaar het eerste rooster
        schedule1 = schedule
        # Maak een nieuw roosters
        # 5/6 dingen per keer switchen gaat iets sneller dan 1 per keer
        schedule2 = switch.switch_session(schedule, 6)
        # Als deze hetzelfde aantal of meer punten heeft, accepteer dit rooster dan.
        if Constraint.own_sessions_check(schedule2, courses)[1] > Constraint.own_sessions_check(schedule1, courses)[1]:
           # Constraint.own_sessions_check(schedule2, courses)[1] >= Constraint.own_sessions_check(schedule1, courses)[1]:
            # Accepteer dit rooster
            schedule = schedule2
        # Als deze minder punten heeft, ga dan terug naar het vorige rooster
        else:
            schedule = schedule1
        # Als het rooster 10 punten verder is, bewaar het rooster dan om er
        # later op terug te kunnen komen
        # if Constraint.own_sessions_check(schedule, courses)[1] % 20 == 0:
        #     schedule_10_points = schedule
        # Als het rooster vast blijft zitten, ga dan terug naar het originele
        # rooster of naar het bewaarde rooster.
        if schedule_counter % LIMIT == 0:
            schedule = switch.switch_session(schedule, 1)
            # if Constraint.own_sessions_check(schedule, courses)[1] % 20 == 0:
            #     # schedule = schedule_10_points
            #     schedule = switch.switch_session(schedule_10_points, 1)
    points.append(Constraint.own_sessions_check(schedule, courses)[1])

    return schedule, points, schedule_counter, Constraint.own_sessions_check(schedule, courses)[1]



def makeplot(points):
    """
    Plots a graph of all the points on the y-axis and number of schedules
    on the x-axis.
    """
    plt.plot(points)
    plt.ylabel("Points (out of 39)")
    plt.show()
