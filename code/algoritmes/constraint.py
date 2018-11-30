import loaddata
import numpy as np

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SPREAD_BONUS = 20
SESSION_LEN = 72


class Constraint():
    """
    A class with all the constraint functions.
    ------
    ALS WE ECHT DIE HARD ALGORITMEN GAAN SCHRIJVEN MOETEN WE DE FUNCTIES NET
    IETS ANDERS NEERZETTEN. NU ROEPEN WE IN IEDERE FUNCTIE ALL_CONSTRAINTS AAN
    MAAR HET IS LOGISCHER OM IN ALL_CONSTRAINTS DE ANDERE FUNCTIES AAN TE
    ROEPEN EN DAN DE FUNCTIES DIE WE WILLEN GEBRUIKEN DAARIN ZETTEN.
    Ja.
    Mee eens.
    Kunnen we gewoon lekker in de input geven van de functie , right?
    Oh nee. even geprobeerd en het moet natuurlijk voor elk rooster opnieuw aangemaakt worden aaah.
    Dus dan misschien deze functie in plan.py zetten en dan meegeven aan Constraint()
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
        weet even niets beters JOE.

        Ik denk dat het sneller is om numpy array hiervoor te gebruiken x R
        """

        courses_schedule = []
        for course in courses:
            course_schedule = {"day": [], "slot": [], "room": [], "type": [], "session_id": [], "group_id": []}
            for i in range(DAYS):
                for j in range(TIME_SLOTS):
                    for k in range(ROOMS):
                        # print(schedule[i][j][k] is None)
                        # print(schedule[i][j][k])
                        if schedule[i][j][k] is not None:
                            # print("??????")
                            if course.name == schedule[i][j][k].name:
                                course_schedule["day"].append(i)
                                course_schedule["slot"].append(j)
                                course_schedule["room"].append(k)
                                course_schedule["type"].append(schedule[i][j][k].type)
                                course_schedule["session_id"].append(schedule[i][j][k].session_id)
                                course_schedule["group_id"].append(schedule[i][j][k].group_id)

            courses_schedule.append(course_schedule)

        return courses_schedule

    def session_spread_check(schedule, courses):
        """
        Calculates the amount of bonuspoints earned by correctly spreading the
        courses over the week. Where a course with 2 sessions should be on
        either monday and thursday or tuesday and friday. See the rest of the
        constrains in the comments bellow.
        A course can maximally get 20 points, this amount is spreaded over the
        number of groups a course has.

        Maximum amount of bonuspoints is 440
        Maximum amount of maluspoints is 430
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)
        bonuspoints = 0
        maluspoints = 0

        for course in courses:
            id = course.course_id

            lectures = []
            sessions = []

            # gets indices of lectures in courses_schedule
            for i in range(len(courses_schedule[id]["type"])):
                if courses_schedule[id]["type"][i] == "lecture":
                    lectures.append(i)

            # checks if a course has groups
            groups = max(courses_schedule[id]["group_id"])
            if groups > 0:

                # saves indices of groups in courses_schedule together with lectures
                for i in range(groups):
                    same_group = [j for j, e in enumerate(courses_schedule[id]["group_id"]) if e == i + 1]
                    sessions.append(lectures + same_group)
            else:
                sessions = [lectures]

            # calculates the spread_bonus per group
            spread_bonus = SPREAD_BONUS / len(sessions)

            if course.sessions == 2:

                #  loops over the amount of groups
                for i in range(len(sessions)):

                    # checks if the courses are on monday and thursday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 3):
                        bonuspoints += spread_bonus

                    # checks if the courses are on tuesday an friday
                    elif (courses_schedule[id]["day"][sessions[i][0]] == 1) and \
                         (courses_schedule[id]["day"][sessions[i][1]] == 4):
                        bonuspoints += spread_bonus

            elif course.sessions == 3:

                for i in range(len(sessions)):

                    # checks if the courses are on monday, wednesday and friday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 2) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 4):
                        bonuspoints += spread_bonus

            elif course.sessions == 4:

                for i in range(len(sessions)):

                    # checks if the courses are on monday, tuesday, thursday and friday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 1) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 3) and \
                       (courses_schedule[id]["day"][sessions[i][3]] == 4):
                        bonuspoints += spread_bonus

            elif course.sessions == 5:

                for i in range(len(sessions)):

                    # checks if the courses are spread out on the whole week (every day)
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 1) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 2) and \
                       (courses_schedule[id]["day"][sessions[i][3]] == 3) and \
                       (courses_schedule[id]["day"][sessions[i][4]] == 4):
                        bonuspoints += spread_bonus

            #  check the overall spread per group
            for i in range(len(sessions)):
                days = []

                # adds the days sessions are given to list days
                for j in range(len(sessions[i])):
                    days.append(courses_schedule[id]["day"][sessions[i][j]])

                # if the sessions aren't spread enough increase maluspoints
                if len(days) - len(set(days)) > 0:
                    malusfactor = (course.sessions - len(days) - len(set(days)))
                    maluspoints += (malusfactor * 10) / len(sessions)

        bonuspoints = round(bonuspoints)
        maluspoints = round(maluspoints)
        print(f"bonuspoints: {bonuspoints}")
        print(f"maluspoints: {maluspoints}")

        # we moeten ook maluspoints returnen maar ik weet nog even niet waar
        # deze functie overal wordt aangeroepen dus daar wacht ik nog even mee
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

        Rebecca: Kan misschien gecombineerd worden met own_sessions_check, aangezien
        je hier ook gewoon loopt door course in courses. Gewoon own_sessions_check
        iets meer uitbreiden met deze functie zodat er uiteindelijk minder geloopt wordt

        MAXIMUM PUNTEN VOOR MUTUAL COURSES BEREKENEN

        """
        courses_schedule = Constraint.all_constraints(schedule, courses)
        malus_points = 0

         # check voor elk slot in het rooster
        for i in range(DAYS):
            for j in range(TIME_SLOTS):
                for k in range(ROOMS):
                    # check of het slot ook echt gevuld is (dus geen 'None')
                    if schedule[i][j][k].course_object:
                        if schedule[i][j][k].type == 'lecture':
                            # elk gevuld slot heeft een naam van de course met zijn mutual courses
                            mutual_courses = schedule[i][j][k].course_object.mutual_courses
                            # Voor elk ding in mutual_courses, check of het in het tijdslot zit van deze course
                            # DIT MOET ANDERS, DIT KAN IN MINDER LOOPS!!!!!
                            # Je kan toch zeggen: if 'name' in [name1, name2, name3 ...]???
                            for l in range(len(mutual_courses)):
                                for z in range(len(schedule[i][j])):
                                    # als de mutual_course in deze timeslot zit geef dan 1 maluspunt
                                    if mutual_courses[l] in schedule[i][j][z].name:
                                        malus_points += 1

        # for course in courses:
        #     # print(course.name)
        #     # print(course.mutual_courses)
        #
        #     # adds (day, slot) of every session of course to course_sessions
        #     checked_course = courses_schedule[course.course_id]
        #     course_sessions = []
        #     for i in range(len(checked_course["day"])):
        #         course_sessions.append((checked_course["day"][i], checked_course["slot"][i]))

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

        return True, malus_points

    def own_sessions_check(schedule, courses):
        """
        Returns true if the sessions of a course aren't planned in the same
        slot; counts amount of points for each course that is placed in a different
        UPDATE: MAX = 62
        """
        own_session_points = 0
        courses_schedule = Constraint.all_constraints(schedule, courses)

        for course in courses:
            checked_course = courses_schedule[course.course_id]

            # adds (day, slot) of every session to course_sessions
            course_sessions = []
            for i in range(len(checked_course["day"])):
                course_sessions.append((checked_course["day"][i], checked_course["slot"][i]))
                sessionID = checked_course["session_id"][i]
            # return False if there are sessions planned at the same time
            # Als de gefilterde lijst even groot is als de niet-gefilterde lijst,
            # dan is er geen overlappend vak (dus + 1 punt)
            # Dit kunnen er maximaal 29 zijn, want er zijn 29 vakken.
            if len(set(course_sessions)) == len(course_sessions):
                own_session_points += 1
            # Als er wel een overlappend vak is, check dan of dit een groep is.
            # Check dit aan de hand van de session_id en group_id.
            # alle group_ids met dezelfde session_id mogen als uitzondering wel bij elkaar.
            else:
                for i in range(len(checked_course["group_id"])): # of in range (session_id), maakt niet uit, zijn even lang.
                    # Check of het een werkcollege of practicum is (deze hebben een group_id van groter dan 1)
                    if checked_course["group_id"][i] > 0:
                        # print(checked_course["session_id"][i] == sessionID)
                        # Check of deze session_id gelijk is aan de session_id van de huidige iteratie
                        # Als dit wel zo is, dan is dit vak ook toegestaan in hetzelfde tijslot
                        # Dus tel een punt op.
                        if checked_course["session_id"][i] == sessionID:
                            own_session_points += 1

                        # for j in range(len(course_ids)):
                        #     if course_ids["session_id"] == checked_course["session_id"][i]:
                        #         print("tes")



        return True, own_session_points

    def students_fit(schedule, courses):
        """
        Returns the number of maluspoints that are given for the number of
        students that don't fit in the room of the session
        max aantal malus punten voor deze functie = 1332
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)
        rooms = loaddata.load_rooms()

        maluspoints = 0
        for course in courses:

            #  saves the room and type of the checked_course sessions
            checked_course = courses_schedule[course.course_id]
            room_ids = checked_course["room"]
            types = checked_course["type"]

            for i in range(len(room_ids)):

                # saves the max amount of students for the session type
                if types[i] is "lecture":
                    students = course.max_students_lecture
                elif types[i] is "tutorial":
                    students = course.max_students_tutorial
                else:
                    students = course.max_students_practical

                # calculates how many empty seats there are
                empty_seats = rooms[room_ids[i]].capacity - students

                # increases maluspoints with the nmbr of students that don't have a seat
                if empty_seats < 0:
                    maluspoints += abs(empty_seats)

        return maluspoints

    def hard_constraints(schedule, courses):
        """
        Een functie die alle hard constraints checkt.
        Return True als het rooster aan alle constraints voldoet.

        KLOPT DUS NIET MEER WANT die check voor mutual courses is aangepast naar groepen.
        """
        # LECTURES CHECK
        lecture_points = 0
        courses_schedule = Constraint.all_constraints(schedule, courses)
        for course in courses:

            # checks for the number of lectures if the lectures are planned first
            for i in range(course.lecture):
                if courses_schedule[course.course_id]["type"][i] != "lecture":
                    return False
                else:
                    lecture_points += 1

        # MUTUAL COURSES CHECK
        mutual_malus = 0
         # check voor elk slot in het rooster
        for i in range(DAYS):
            for j in range(TIME_SLOTS):
                for k in range(ROOMS):
                    # check of het slot ook echt gevuld is (dus geen 'None')
                    if schedule[i][j][k].course_object:
                        # elk gevuld slot heeft een naam van de course met zijn mutual courses
                        mutual_courses = schedule[i][j][k].course_object.mutual_courses
                        # Voor elk ding in mutual_courses, check of het in het tijdslot zit van deze course
                        # DIT MOET ANDERS, DIT KAN IN MINDER LOOPS!!!!!
                        # Je kan toch zeggen: if 'name' in [name1, name2, name3 ...]???
                        for i in range(len(mutual_courses)):
                            for z in range(len(schedule[i][j])):
                                # Als de mutual course er in zit, return False
                                if mutual_courses[i] in schedule[i][j][z].name:
                                    mutual_malus += 1
                                if mutual_malus > 0:
                                    return False

        # OWN SESSION CHECK
        own_session_points = 0

        for course in courses:
            checked_course = courses_schedule[course.course_id]

            # adds (day, slot) of every session to course_sessions
            course_sessions = []
            for i in range(len(checked_course["day"])):
                course_sessions.append((checked_course["day"][i], checked_course["slot"][i]))
            # return False if there are sessions planned at the same time
            # Als de gefilterde lijst even groot is als de niet-gefilterde lijst,
            # dan is er geen overlappend vak (dus + 1 punt)
            if len(set(course_sessions)) == len(course_sessions):
                own_session_points += 1
            else:
                for i in range(len(checked_course["group_id"])): # of in range (session_id), maakt niet uit, zijn even lang.
                    # Check of het een werkcollege of practicum is (deze hebben een group_id van groter dan 1)
                    if checked_course["group_id"][i] > 0:
                        # print(checked_course["session_id"][i] == sessionID)
                        # Check of deze session_id gelijk is aan de session_id van de huidige iteratie
                        # Als dit wel zo is, dan is dit vak ook toegestaan in hetzelfde tijslot
                        # Dus tel een punt op.
                        if checked_course["session_id"][i] == sessionID:
                            own_session_points += 1
                    else:
                        return False

        return True
