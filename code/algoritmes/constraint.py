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
    # def __init__(self, schedule):
    #     self.schedule = schedule
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

        -----
        HUH MEGA GEK, IK HAD GECOMMIT EN INEENS WAREN AL REBECCA HAAR COMMENTS
        WEG. PANIEK.
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)
        bonuspoints = 0

        for course in courses:
            if course.sessions == 2:
                # print(courses_schedule[course.course_id][0][0], courses_schedule[course.course_id][1][0])
                # checks if the courses are on monday and thursday
                if (courses_schedule[course.course_id][0][0] == 0) and \
                   (courses_schedule[course.course_id][1][0] == 3):
                    bonuspoints += SPREAD_BONUS

                # checks if the courses are on tuesday an friday
                elif (courses_schedule[course.course_id][0][0] == 1) and \
                     (courses_schedule[course.course_id][1][0] == 4):
                    bonuspoints += SPREAD_BONUS

            elif course.sessions == 3:

                # checks if the courses are on monday, wednesday and friday
                if (courses_schedule[course.course_id][0][0] == 0) and \
                   (courses_schedule[course.course_id][1][0] == 2) and \
                   (courses_schedule[course.course_id][2][0] == 4):
                    bonuspoints += SPREAD_BONUS

            elif course.sessions == 4:

                # checks if the courses are on monday, tuesday, thursday and friday
                if (courses_schedule[course.course_id][0][0] == 0) and \
                   (courses_schedule[course.course_id][1][0] == 1) and \
                   (courses_schedule[course.course_id][2][0] == 3) and \
                   (courses_schedule[course.course_id][3][0] == 4):
                    bonuspoints += SPREAD_BONUS

        return bonuspoints


        # bonuspoints = 0
        # monday = Constraint.get_day(schedule, 0)
        # tuesday = Constraint.get_day(schedule, 1)
        # wednesday = Constraint.get_day(schedule, 2)
        # thursday = Constraint.get_day(schedule, 3)
        # friday = Constraint.get_day(schedule, 4)
        # for course in courses:
        #     nmbr_sessions = course.sessions
        #     if nmbr_sessions == 2:
        #         # print(course.name)
        #         # print(monday)
        #         if course.name in monday:
        #             if course.name in thursday:
        #                 print("TEEESTTTTT")
        #                 bonuspoints += SPREAD_BONUS
        #         elif course.name in tuesday:
        #             if course.name in friday:
        #                 bonuspoints += SPREAD_BONUS
        #
        #     elif nmbr_sessions == 3:
        #         if course.name in monday:
        #             if course.name in wednesday:
        #                 if course.name in friday:
        #                     bonuspoints += SPREAD_BONUS
        #
        #     elif nmbr_sessions == 4:
        #         if (course.name in monday) and (course.name in tuesday) and \
        #            (course.name in thursday) and (course.name in friday):
        #             bonuspoints += SPREAD_BONUS
        #     else:
        #         bonuspoints += 0
        #
        # return bonuspoints

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
            course_schedule = []
            for i in range(DAYS):
                for j in range(TIME_SLOTS):
                    for k in range(ROOMS):
                        if course.name == schedule[i][j][k].name:
                            course_schedule.append([i, j, k, schedule[i][j][k].type])
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
        Als we dat hebben veranderd kunnen we het gecommente stuk checken
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)

        for course in courses:

            # checks if room and type of course are still in courses_schedule
            if len(courses_schedule[course.course_id]) > 2:

                # removes room and type of course in course_schedule
                for i in range(len(courses_schedule[course.course_id])):
                    courses_schedule[course.course_id][i] = courses_schedule[course.course_id][i][0:2]

            checked_course = courses_schedule[course.course_id]

            # # checks for all the mutual courses if they are at the same time
            # for mutual in course.mutual_courses:
            #
            #     # checks if room and type of course are still in course_schedule
            #     if len(courses_schedule[mutual.course_id[0]]) > 2:
            #
            #         # removes room and type of course in course_schedule
            #         for i in range(len(courses_schedule[mutual.course_id])):
            #             courses_schedule[mutual.course_id][i] = courses_schedule[mutual.course_id][i][0:2]
            #
            #     # checks if course is planned at the same time as mutual course
            #     if set(courses_schedule[mutual.course_id]) & set(checked_course) != []:
            #         return False

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
