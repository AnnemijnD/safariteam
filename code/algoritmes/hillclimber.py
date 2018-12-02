
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
SLOTS = 140
SPREADPOINTS = 440
SAVELIMIT = 3000


def hard_constraints(schedule, courses, schedule_counter):

    points = []

    # Ga door totdat alle hoorcolleges voor de andere sessies zijn ingeroosterd,
    # Dus totdat de lecture_first functie True is.
    # Om de code te met dit algoritme helemaal te runnen dan zet je hier
    # de bovenste regel weer 'aan'! (even ont-commenten)

    courses_schedule = Constraint.all_constraints(schedule, plan.courses)

    while Constraint.lecture_first(schedule, courses, courses_schedule) > 0 or \
            Constraint.mutual_courses_check(schedule, courses) > 0:

        # HOI REBECCA IK HEB EEN DEEL VAN DE CONSTRAINTFUNCTIES AANGEPAST MET
        # DAT WE NU COURSES_SCHEDULE ERIN DOEN ALS ARGUMENT WANT DAN GAAT HET
        # IETS SNELLER. HOOP DAT IK HEM VAAK GENOEG OPNIEUW AANROEP, ZOU CHILL
        # ZIJN ALS JIJ HET VOOR DE ZEKERHEID KAN CHECKEN :) XOXO

        courses_schedule = Constraint.all_constraints(schedule, plan.courses)
        points.append(Constraint.lecture_first(schedule, courses, courses_schedule) + \
                      Constraint.mutual_courses_check(schedule, courses))
        schedule_counter += 1
        # Bewaar het eerste rooster
        schedule1 = schedule
        lecture_points1 = Constraint.lecture_first(schedule1, courses, courses_schedule)
        mutual_points1 = Constraint.mutual_courses_check(schedule1, courses)
        # Maak een nieuw roosters
        # 5 dingen per keer switchen gaat iets sneller dan 1 per keer
        schedule2 = switch.switch_session(schedule, 3)
        # Bereken de punten van het nieuwe rooster
        courses_schedule = Constraint.all_constraints(schedule, plan.courses)
        lecture_points2 = Constraint.lecture_first(schedule2, courses, courses_schedule)
        mutual_points2 = Constraint.mutual_courses_check(schedule2, courses)
        # Als deze hetzelfde aantal of meer punten heeft, accepteer dit rooster dan.
        if lecture_points2 <= lecture_points1 \
                and mutual_points2 <= mutual_points1:
            # Accepteer dit rooster
            schedule = schedule2
        # Als deze minder punten heeft, ga dan terug naar het vorige rooster
        else:
            schedule = schedule1
        # if schedule_counter % 700 == 0:
        #     makeplot(points)

    courses_schedule = Constraint.all_constraints(schedule, plan.courses)
    points.append(Constraint.lecture_first(schedule, courses, courses_schedule) - \
                  Constraint.mutual_courses_check(schedule, courses))

    return schedule, points, schedule_counter


def soft(schedule, courses, schedule_counter):
    """
    Generates a schedule using a hill climber algorithm.
    Input is a random schedule, output is a schedule that fulfills all hard-
    and soft constraints.
    """

    switcher = 3
    points = []

    while Constraint.lecture_first(schedule, courses) > 0 or \
            Constraint.mutual_courses_check(schedule, courses) > 0 or \
            Constraint.session_spread_check(schedule, courses) < 380 or \
            Constraint.students_fit(schedule, courses) > 400:
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
        # of finding a solution.
        if schedule2_points >= schedule1_points:
            schedule = schedule2
        # If the second schedule has less points, go back to the old schedule.
        else:
            schedule = schedule1
        # If a limit is reached, change the number of switches to 1, resulting
        # in a higher chance of finding schedule with more points. Disadvantage
        # is that it takes longer to find a good schedule.
        if schedule_counter == LIMIT:
            switcher = 1

        # # Force a change in the schedule at a local optimum
        # if schedule_counter % OPTIMUM == 0:
        #     schedule = switch.switch_session(schedule, switcher)


    # Append last points of the new schedule
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
    """
    points = Constraint.session_spread_check(schedule, courses) - \
            Constraint.lecture_first(schedule, courses) - \
            Constraint.mutual_courses_check(schedule, courses) - \
            (Constraint.students_fit(schedule, courses) / 10)

    return points

def makeplot(points):
    """
    DEZE KAN WEGGEHAALD WORDEN ZODRA WE HET NIET MEER WILLEN TESTEN
    """
    plt.plot(points)
    plt.ylabel("Points")
    plt.show()
