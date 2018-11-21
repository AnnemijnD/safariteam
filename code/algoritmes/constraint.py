SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SPREAD_BONUS = 20
# COURSES = 29


class Constraint():
    """
    A class with all the constraint functions
    """

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
        """
        Sanne wil je hier alsjeblieft neerzetten wat deze functie doet? :)
        Rebecca:
        = mininmaal aantal vakken x tijdslots per dag = 28 x 5 x 4 = 560 checks voor 1 functie
        Maximum bonus punten voor deze functie = 400 (want 200 + 100 + 100 = 400).
        """

        bonuspoints = 0
        monday = Constraint.get_day(schedule, 0)
        tuesday = Constraint.get_day(schedule, 1)
        wednesday = Constraint.get_day(schedule, 2)
        thursday = Constraint.get_day(schedule, 3)
        friday = Constraint.get_day(schedule, 4)

        # Loop through the schedule for every course
        for course in courses:
            nmbr_sessions = course.sessions

            # Check if this course has two sessions.
            # Optimal spread for two sessions is monday - thursday or tuesday - friday
            if nmbr_sessions == 2:
                # 10 vakken met 2 sessies, dus
                # max bonus = 10 x 20 = 200
                if course.name in monday:
                    if course.name in thursday:
                        # print("TEEESTTTTT")
                        bonuspoints += SPREAD_BONUS
                elif course.name in tuesday:
                    if course.name in friday:
                        bonuspoints += SPREAD_BONUS

            # Optimal spread for three courses is:
            # Monday - Wednesday - Friday.
            elif nmbr_sessions == 3:
                # Max bonus = 5 x 20 = 100
                if course.name in monday:
                    if course.name in wednesday:
                        if course.name in friday:
                            bonuspoints += SPREAD_BONUS

            # Optimal spread for four courses is Monday, Tuesday, Thursday, Friday.
            elif nmbr_sessions == 4:
                # max bonus = 5 x 20 = 100
                if (course.name in monday) and (course.name in tuesday) and \
                   (course.name in thursday) and (course.name in friday):
                    bonuspoints += SPREAD_BONUS
            else:
                bonuspoints += 0

        return bonuspoints

    def all_constraints(schedule, courses):
        """
        Makes a list that containts lists of every course with the moment and
        type of the courses in the schedule. The courses are in the list in
        order of their course_id.
        -----
        Dit is het begin voor het preprocessen. Een hele slechte naam maar
        weet even niets beters JOE
        """
        courses_schedule = []
        # Voor elke course alle timeslots langs is dus meer dan 2000 iteraties...
        for course in courses:
            course_schedule = []
            for i in range(DAYS):
                for j in range(TIME_SLOTS):
                    for k in range(ROOMS):
                        if course.name == schedule[i][j][k].name:
                            course_schedule.append((i, j, k, schedule[i][j][k].type))
            courses_schedule.append(course_schedule)

        return courses_schedule

    def lecture_first(schedule, courses):
        """
        Returns true if the lectures are before the tutorials and or
        practicals, otherwise returns false.
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)
        for course in courses:
            for i in range(course.lecture):
                if courses_schedule[course.course_id][i][3] != "lecture":
                    return False

        return True

    def mutual_courses_check(schedule, courses):
        """
        Checks if the mutual courses aren't scheduled in the same slot
        ----
        !!!!!!! WERKT NOG NIET !!!!!!!!!!!
        ZIJN NOG MEERDERE PROBLEMEN!!
        1 course.mutual_courses bevat alleen maar de naam vd courses
        2 de doorsnede gaat nu sowieso niet goed want het hoeft niet hetzelfde
        college type te zijn
        Waarschijnlijk is dit niet moeilijk te fixen maar ik ga lekker chilllen
        (slapen) nu ik spreek jullie lateeerrrrr
        """

        courses_schedule = Constraint.all_constraints(schedule, courses)
        for course in courses:
            checked_course = courses_schedule[course.course_id]
            for mutual in course.mutual_courses:
                if set(courses_schedule[mutual.course_id]) & set(checked_course) != []:
                    return False

        return True


    def student_numbers(schedule):
        """
        Checks if the number of students in a room matches the room capacity.
        """
        pass


    def get_day(schedule, day):
        """
        Returns a linear list of the schedule of a specific day.
        IK DENK DAT DIT MAKKELIJKER KAN MET NUMPY ARRAY x Rebecca
        """
        all_days = []
        for i in range(DAYS):
            for j in range(TIME_SLOTS):
                for k in range(ROOMS):
                    all_days.append(schedule[i][j][k].name)
        return all_days[TIME_SLOTS * ROOMS * day:TIME_SLOTS * ROOMS * (day + 1)]
