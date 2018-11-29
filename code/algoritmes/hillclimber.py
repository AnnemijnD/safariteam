
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
LIMIT = 3000
OPTIMUM = 10000
COURSECOUNT = 29
MUTUALCOURSES = 33
LECTURECOUNT = 39
SPREADPOINTS = 440
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

        # -----------------------------------------------------------------------------------
        # DIT IS VOOR ALS HET ROOSTER IN EEN LOKAAL OPTIMUM KOMT.
        # ZIJN VAST HEEL VEEL MANIEREN OM DIT TE VERBETEREN!!!

        # Als het rooster 10 punten verder is, bewaar het rooster dan om er
        # later op terug te kunnen komen
        # if Constraint.lecture_first(schedule, courses)[1] % 10 == 0:
        #     schedule_10_points = schedule
        # Als het rooster vast blijft zitten, ga dan terug naar het originele
        # rooster of naar het bewaarde rooster.


        # if schedule_counter % LIMIT == 0:
        #     schedule = switch.switch_session(schedule, 1)



            # makeplot(points)
            # if Constraint.lecture_first(schedule, courses)[1] % 10 == 0:
            #     if schedule_10_points:
            #         schedule = schedule_10_points
            #     else:
            #         schedule = save_schedule

    points.append(Constraint.lecture_first(schedule, courses)[1] + \
                  Constraint.own_sessions_check(schedule, courses)[1] - \
                  Constraint.mutual_courses_check(schedule, courses)[1])


    return schedule, points, schedule_counter, Constraint.own_sessions_check(schedule, courses)[1]

def soft_constraint(schedule, courses, schedule_counter):

    points = []

    while Constraint.session_spread_check(schedule, courses) < 50:
        # Hou de punten bij zodat deze geplot kunnen worden.
        points.append(Constraint.session_spread_check(schedule, courses))
        print(Constraint.session_spread_check(schedule, courses))
        # Hou een teller bij van het aantal roosters die gemaakt zijn
        # schedule_counter += 1
        # Bewaar het eerste rooster
        schedule1 = schedule
        spread_points1 = Constraint.session_spread_check(schedule1, courses)
        # Maak een nieuw roosters
        # 5 dingen per keer switchen gaat iets sneller dan 1 per keer
        # Deze verandering mag alleen gemaakt worden als er dan nog aan de hard constraints voldaan wordt.
        # Check dus; zolang er niet aan de hard constraints voldaan wordt, moet er opnieuw geswitcht worden.
        # while Constraint.hard_constraints(schedule, courses) == False:
        schedule2 = switch.switch_session(schedule, 2)
        # Bereken de punten van het nieuwe rooster
        spread_points2 = Constraint.session_spread_check(schedule2, courses)
        # Als deze hetzelfde aantal of meer punten heeft, accepteer dit rooster dan.
        print(Constraint.hard_constraints(schedule2, courses) == True)
        if spread_points2 >= spread_points1 and Constraint.hard_constraints(schedule2, courses) == True:
            # Accepteer dit rooster
            schedule = schedule2
            schedule_counter += 1
        # Als deze minder punten heeft, ga dan terug naar het vorige rooster
        else:
            schedule = schedule1
            # lol dit klopt niet maar even tijdelijk
            schedule_counter += 1

    return schedule, points, schedule_counter, Constraint.session_spread_check(schedule, courses)


def soft(schedule, courses, schedule_counter):

    switcher = 3
    points = []

    while Constraint.lecture_first(schedule, courses)[0] is False or \
            Constraint.own_sessions_check(schedule, courses)[1] < COURSECOUNT or \
            Constraint.mutual_courses_check(schedule, courses)[1] > 0:
            # Constraint.session_spread_check(schedule, courses) < 440 or \
            # Constraint.students_fit(schedule, courses) > 0:
        # Append points to show in a graph when the schedule is made
        points.append(get_points(schedule, courses))
        # Count the number of schedules made
        schedule_counter += 1
        # Save the first schedule
        schedule1 = schedule
        # Get points of the first schedule
        schedule1_points = get_points(schedule1, courses)
        # Make a new schedule by switching
        schedule2 = switch.switch_session(schedule, switcher)
        # Bereken de punten van het nieuwe rooster
        schedule2_points = get_points(schedule2, courses)
        # Als deze hetzelfde aantal of meer punten heeft, accepteer dit rooster dan.
        if schedule2_points >= schedule1_points:
            # Accepteer dit rooster
            schedule = schedule2
        # Als deze minder punten heeft, ga dan terug naar het vorige rooster
        else:
            schedule = schedule1

        # ALs het rooster een limiet heeft bereikt, zet de switcher dan op 1
        # Hierbij neemt de kans toe dat er een goed rooster wordt gevonden, maar duurt het wel langer.
        # if schedule_counter % LIMIT == 0:
        #     makeplot(points)

        # Lower the heat, by changing switcher to 1.
        if schedule_counter % LIMIT == 0:
            switcher = 1

        # Force a change in the schedule at a local optimum
        if schedule_counter % OPTIMUM == 0:
            schedule = switch.switch_session(schedule, switcher)



    points.append(get_points(schedule, courses))

    return schedule, points, schedule_counter, Constraint.own_sessions_check(schedule, courses)[1]


def get_points(schedule, courses):
    """
    Returns the points of a given schedule.
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
