class Constraint(object):
    """
    A class with all the constraint functions
    """

    def __init__(self, schedule):
        self.schedule = schedule

# Hier even een lijst met alle constraints:
# 1. hoorcelleges voor werkcolleges en practica HARD
# 2. er mag geen overlap zijn (met college zelf) HARD
# 3. er mag geen overlap zijn (met andere vakkken)
# 4. studenten moeten in de zalen passen (NOG NIET)
# 5. colleges van hetzelfde vak moeten goed verspreid zijn over de week
#
# Een fix_hard_constraints functie maken voor als na het soft maken van een
# aantal constraints er niet meer wordt voldaan aan de hard constraints.


    def mutual_courses(self, schedule, course):
        pass
        # PSEUDO:
        # check bij inroosteren of van course in schedule of er courses uit
        # self.mutual_courses al ingeroosterd zijn
