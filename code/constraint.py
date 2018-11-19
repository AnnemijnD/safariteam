SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SPREAD_BONUS = 20


class Constraint():
    """
    A class with all the constraint functions
    """
    def __init__(self, schedule):
        self.schedule = schedule
        # self.session_spread = self.session_spread_check(self.schedule)

# Hier even een lijst met alle constraints:
# 1. hoorcelleges voor werkcolleges en practica HARD
# 2. er mag geen overlap zijn (met college zelf) HARD
# 3. er mag geen overlap zijn (met andere vakkken) HARD
# 4. studenten moeten in de zalen passen (NOG NIET)
# 5. colleges van hetzelfde vak moeten goed verspreid zijn over de week
#
# Een fix_hard_constraints functie maken voor als na het soft maken van een
# aantal constraints er niet meer wordt voldaan aan de hard constraints.

    def session_spread_check(schedule, courses):
        bonuspoints = 0
        monday = Constraint.get_day(schedule, 0)
        tuesday = Constraint.get_day(schedule, 1)
        wednesday = Constraint.get_day(schedule, 2)
        thursday = Constraint.get_day(schedule, 3)
        friday = Constraint.get_day(schedule, 4)
        for course in courses:
            nmbr_sessions = course.sessions
            if nmbr_sessions == 2:
                # print(course.name)
                # print(monday)
                if course.name in monday:
                    if course.name in thursday:
                        print("TEEESTTTTT")
                        bonuspoints += SPREAD_BONUS
                elif course.name in tuesday:
                    if course.name in friday:
                        bonuspoints += SPREAD_BONUS

            elif nmbr_sessions == 3:
                if course.name in monday:
                    if course.name in wednesday:
                        if course.name in friday:
                            bonuspoints += SPREAD_BONUS

            elif nmbr_sessions == 4:
                if (course.name in monday) and (course.name in tuesday) and \
                (course.name in thursday) and (course.name in friday):
                    bonuspoints += SPREAD_BONUS
            else:
                bonuspoints += 0

        return bonuspoints

    def get_day(schedule, day):
        """
        Returns a linear list of the schedule of a specific day.
        """
        all_days = []
        for i in range(DAYS):
            for j in range(TIME_SLOTS):
                for k in range(ROOMS):
                    all_days.append(schedule[i][j][k].name)
        return all_days[TIME_SLOTS * ROOMS * day:TIME_SLOTS * ROOMS * (day + 1)]
