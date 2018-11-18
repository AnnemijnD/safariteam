SPREAD_BONUS = 20


class Constraint(object):
    """
    A class with all the constraint functions
    """
    def __init__(self, schedule):
        self.schedule = schedule

# Hier even een lijst met alle constraints:
# 1. hoorcelleges voor werkcolleges en practica HARD
# 2. er mag geen overlap zijn (met college zelf) HARD
# 3. er mag geen overlap zijn (met andere vakkken) HARD
# 4. studenten moeten in de zalen passen (NOG NIET)
# 5. colleges van hetzelfde vak moeten goed verspreid zijn over de week
#
# Een fix_hard_constraints functie maken voor als na het soft maken van een
# aantal constraints er niet meer wordt voldaan aan de hard constraints.

    def session_spread_check(self, schedule):
        # per course checken of die goed verspreid is
        # 1. weten hoeveel colleges het vak heeft
        # 2. checken of die goed verspreid zijn over de weeek
        #
        # 1 college --> nooit bonuspunten --> niet checken
        # 2 colleges --> twee opties: ma-do & di-vrij
        # 3 colleges --> ma-woe-vrij
        # 4 colleges --> ma-di-do-vrij
        # 5 colleges --> nooit bonuspunten --> niet checken

        bonuspoints = 0
        # IS HET NIET HANDIGER ALS WE ERGENS AL EEN COURSES LIST HEBBEN, NU
        # OPNIEUW AANROEPEN IS BEETJE KUT.
        courses = plan.load_courses()
        monday = schedule[0]
        tuesday = schedule[1]
        wednesday = schedule[2]
        thursday = schedule[3]
        friday = schedule[4]
        for course in courses:
            nmbr_sessions = course.sessions

            if nmbr_sessions == 2:

                # DIT KAN NOG NIET WANT MONDAY IS LIJST MET LIJSTEN ERIN!
                # --> GET_DAY FUNCTIE MAKEN DIE ER EEN LANGE LIJST VAN MAAKT!

                # if course in monday:
                #     if course in thursday:
                #         bonuspoints += SPREAD_BONUS
                # elif course in tuesday:
                #     if course in friday:
                #         bonuspoints += SPREAD_BONUS
                # else:
                #     bonuspoints += 0
                pass
            elif nmbr_sessions == 3:
                pass
            elif nmbr_sessions == 4:
                pass
            else:
                bonuspoints += 0
