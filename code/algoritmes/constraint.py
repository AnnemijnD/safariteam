SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SPREAD_BONUS = 20


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

    def all_constraints(schedule, courses):
        """
        Makes a list that contains lists of every course with the moment and
        type of the courses in the schedule. The courses are in the list in
        order of their course_id.
        -----
        Dit is het begin voor het preprocessen. Een hele slechte naam maar
        weet even niets beters JOE
        """
        courses_schedule = []
        for course in courses:
            course_schedule = {"day": [], "slot": [], "room": [], "type": []}
            for i in range(DAYS):
                for j in range(TIME_SLOTS):
                    for k in range(ROOMS):
                        if course.name == schedule[i][j][k].name:
                            course_schedule["day"].append(i)
                            course_schedule["slot"].append(j)
                            course_schedule["room"].append(k)
                            course_schedule["type"].append(schedule[i][j][k].type)
            courses_schedule.append(course_schedule)

        return courses_schedule

    def session_spread_check(schedule, courses):
        """
        Calculates the amount of bonuspoints earned by correctly spreading the
        courses over the week. Where a course with 2 sessions should be on
        either monday and thursday or tuesday and friday. See the rest of the
        constrains in the comments bellow.

        -----
        TODO:
        - nu kijkjen we nog niet voor werkgroepen maar als we dat wel gaan doen
        mag het maar 20/(aantal werkgroepen) punten krijgen (en dan nog iets
        handigs bedenken met dat we hele getallen hebben)
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)
        bonuspoints = 0

        for course in courses:
            if course.sessions == 2:
                # checks if the courses are on monday and thursday
                if (courses_schedule[course.course_id]["day"][0] == 0) and \
                   (courses_schedule[course.course_id]["day"][1] == 3):
                    bonuspoints += SPREAD_BONUS

                # checks if the courses are on tuesday an friday
                elif (courses_schedule[course.course_id]["day"][0] == 1) and \
                     (courses_schedule[course.course_id]["day"][1] == 4):
                    bonuspoints += SPREAD_BONUS

            elif course.sessions == 3:

                # checks if the courses are on monday, wednesday and friday
                if (courses_schedule[course.course_id]["day"][0] == 0) and \
                   (courses_schedule[course.course_id]["day"][1] == 2) and \
                   (courses_schedule[course.course_id]["day"][2] == 4):
                    bonuspoints += SPREAD_BONUS

            elif course.sessions == 4:

                # checks if the courses are on monday, tuesday, thursday and friday
                if (courses_schedule[course.course_id]["day"][0] == 0) and \
                   (courses_schedule[course.course_id]["day"][1] == 1) and \
                   (courses_schedule[course.course_id]["day"][2] == 3) and \
                   (courses_schedule[course.course_id]["day"][3] == 4):
                    bonuspoints += SPREAD_BONUS

        return bonuspoints

    def lecture_first(schedule, courses):
        """
        Returns true if the lectures are before the tutorials and or
        practicals, otherwise returns false.
        """
        lecture_points = 0
        courses_schedule = Constraint.all_constraints(schedule, courses)
        for course in courses:

            # checks for the amount of lectures if the lectures are planned first
            for i in range(course.lecture):
                if courses_schedule[course.course_id]["type"][i] != "lecture":
                    return [False, lecture_points]
                else:
                    lecture_points += 1

        return [True, lecture_points]

    def mutual_courses_check(schedule, courses):
        """
        Checks if the mutual courses aren't scheduled in the same slot
        ----
        !!!!!!! WERKT NOG NIET !!!!!!!!!!!
        ZIJN NOG MEERDERE PROBLEMEN!!
        1 course.mutual_courses bevat alleen maar de naam vd courses
        Als we dat hebben veranderd kunnen we het gecommente stuk checken
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)

        for course in courses:

            # adds (day, slot) of every session of course to course_sessions
            checked_course = courses_schedule[course.course_id]
            course_sessions = []
            for i in range(len(checked_course["day"])):
                course_sessions.append((checked_course["day"][i], checked_course["slot"][i]))

            # # checks for all the mutual courses if they are at the same time
            # for mutual in course.mutual_courses:
            #     mutual_course = courses_schedule[mutual.course_id]
            #
            #     # adds (day, slot) of every session of mutual to mutual_sessions
            #     mutual_sessions = []
            #     for i in range(len(mutual_course)):
            #         mutual_sessions.append((mutual_course["day"][i], mutual_course["slot"][i]))
            #
            #     # return False if there are sessions planned at the same time
            #     checked_sessions = course_sessions + mutual_sessions
            #     if len(set(checked_sessions)) < len(checked_sessions):
            #         return False

        return True

    def own_sessions_check(schedule, courses):
        """
        Returns true if the sessions of a course aren't planned in the same
        slot, otherwise returns false.
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)

        for course in courses:
            checked_course = courses_schedule[course.course_id]

            # adds (day, slot) of every session to course_sessions
            course_sessions = []
            for i in range(len(checked_course["day"])):
                course_sessions.append((checked_course["day"][i], checked_course["slot"][i]))

            # return False if there are sessions planned at the same time
            if len(set(course_sessions)) < len(checked_course):
                return False

        return True

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
