import loaddata
import numpy as np
import math
import switch

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SPREAD_BONUS = 20
SESSION_LEN = 72
SESSION_NUM = 129
SLOTS_PER_DAY = 28
from random import randint


class Constraint():
    """
    A class with all the constraint functions.
    """

    def all_constraints(schedule, courses):
        """
        Makes a list that contains lists of every course with the moment and
        type of the courses in the schedule. The courses are in the list in
        order of their course_id.
        -----
        """

        courses_schedule = []
        for course in courses:
            course_schedule = {"day": [], "slot": [], "room": [], "type": [],
                               "session_id": [], "group_id": [], "overall_id": []}
            for i in range(DAYS):
                for j in range(TIME_SLOTS):
                    for k in range(ROOMS):
                        if schedule[i][j][k] is not None:
                            if course.name == schedule[i][j][k].name:
                                course_schedule["day"].append(i)
                                course_schedule["slot"].append(j)
                                course_schedule["room"].append(k)
                                course_schedule["type"].append(schedule[i][j][k].type)
                                course_schedule["session_id"].append(schedule[i][j][k].session_id)
                                course_schedule["group_id"].append(schedule[i][j][k].group_id)
                                course_schedule["overall_id"].append(schedule[i][j][k].overall_id)

            courses_schedule.append(course_schedule)

        return courses_schedule

    def all_constraints_linear(schedule, courses):
        """
        Similar as all_constraints but then as a linear list instead of
        a matrix.


        HUH DIT IS BIJNA dezelfde functie als die hierboven,
        kan het niet gewoon bij elkaar gedaan worden en dat de input veranderd?
        """
        courses_schedule = []
        for course in courses:
            course_schedule = {"day": [], "slot": [], "room": [], "type": [],
                               "session_id": [], "group_id": [], "overall_id": []}
            for i in range(SLOTS):
                if schedule[i] is not None:
                    if course.name == schedule[i].name:
                        course_schedule["day"].append(math.floor(i / SLOTS_PER_DAY))
                        course_schedule["slot"].append(math.floor(i / ROOMS) % TIME_SLOTS)
                        course_schedule["room"].append(i % ROOMS)
                        course_schedule["type"].append(schedule[i].type)
                        course_schedule["session_id"].append(schedule[i].session_id)
                        course_schedule["group_id"].append(schedule[i].group_id)
                        course_schedule["overall_id"].append(schedule[i].overall_id)

            courses_schedule.append(course_schedule)

        return courses_schedule

    def session_spread_check(schedule, courses, courses_schedule):
        """
        Calculates the amount of bonuspoints earned by correctly spreading the
        courses over the week. Where a course with 2 sessions should be on
        either monday and thursday or tuesday and friday. See the rest of the
        constrains in the comments bellow.
        A course can maximally get 20 points, this amount is spreaded over the
        number of groups a course has.

        Maximum amount of bonuspoints is 440
        Maximum amount of maluspoints is 430

        Returns a list of malus and bonuspoints per course as well.
        """
        # courses_schedule = Constraint.all_constraints(schedule, courses)
        bonuspoints = 0
        maluspoints = 0

        # list with course id, bonus points and malus points
        course_bonus_malus = []

        for course in courses:
            id = course.course_id
            course_mal_points = 0
            course_bon_points = 0
            lectures = []
            sessions = []

            # gets indices of lectures in courses_schedule
            for i in range(len(courses_schedule[id]["type"])):
                if courses_schedule[id]["type"][i] == "lecture":
                    lectures.append(i)

            # checks if a course has groups
            # print(courses_schedule[id]["group_id"], course.name)
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

                    # print(courses_schedule[id]["day"], course.name)
                    # print(i)
                    # print(sessions[i])

                    # checks if the courses are on monday and thursday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 3):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus


                    # checks if the courses are on tuesday an friday
                    elif (courses_schedule[id]["day"][sessions[i][0]] == 1) and \
                         (courses_schedule[id]["day"][sessions[i][1]] == 4):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus

            elif course.sessions == 3:

                for i in range(len(sessions)):

                    # checks if the courses are on monday, wednesday and friday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 2) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 4):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus

            elif course.sessions == 4:

                for i in range(len(sessions)):

                    # checks if the courses are on monday, tuesday, thursday and friday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 1) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 3) and \
                       (courses_schedule[id]["day"][sessions[i][3]] == 4):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus

            elif course.sessions == 5:

                for i in range(len(sessions)):

                    # checks if the courses are spread out on the whole week (every day)
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 1) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 2) and \
                       (courses_schedule[id]["day"][sessions[i][3]] == 3) and \
                       (courses_schedule[id]["day"][sessions[i][4]] == 4):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus

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
                    course_mal_points += (malusfactor * 10) / len(sessions)


            course_bonus_malus.append([id, round(course_mal_points - course_bon_points)])



        bonuspoints = round(bonuspoints)
        maluspoints = round(maluspoints)
        # print(course_bonus_malus)
        # print(f"bonuspoints: {bonuspoints}")
        # print(f"maluspoints: {maluspoints}")
        spread_points = maluspoints + bonuspoints

        # we moeten ook maluspoints returnen maar ik weet nog even niet waar
        # deze functie overal wordt aangeroepen dus daar wacht ik nog even mee

        # zelfde geldt voor de bonus_malus_points
        return [spread_points, course_bonus_malus]

    def lecture_first(schedule, courses, courses_schedule):
        """
        Returns true if the lectures are before the tutorials and or
        practicals, otherwise returns false.
        """
        lecture_points = 0
        # courses_schedule = Constraint.all_constraints(schedule, courses)

        for course in courses:
            # checks for the number of lectures if the lectures are planned first
            for i in range(course.lecture):
                if courses_schedule[course.course_id]["type"][i] != "lecture":
                    lecture_points += 1

        return lecture_points

    def mutual_courses_check(schedule, courses):
        """
        Checks if same courses and  mutual courses aren't scheduled in the
        same timeslot. Iterates over every course in the schedule.
        Input is a schedule, output is the number of minus points calculated
        by the number of conflicting courses.
        """

        minus_points = 0

        # Check every slot in the schedule
        for i in range(DAYS):
            for j in range(TIME_SLOTS):
                for k in range(ROOMS):
                    # Check if this slot is filled (= check if not None)
                    if schedule[i][j][k].course_object:
                        # Check if session in this slot is a lecture
                        if schedule[i][j][k].type == "lecture":
                            # Each slot has a course name and the courses' mutual courses
                            # Mutual courses is a list of courses that can't be in the same timeslot
                            mutual_courses = schedule[i][j][k].course_object.mutual_courses
                            # For every mutual course in the mutual_courses list,
                            # check if it is placed in the same timeslot.
                            for mutual_course in range(len(mutual_courses)):    # DIT MOET ANDERS, DIT KAN IN MINDER LOOPS??!!
                                                                                # Je kan toch zeggen: if 'name' in [name1, name2, name3 ...]???
                                for z in range(len(schedule[i][j])):
                                    # If this mutual course is placed in the same timeslot
                                    # (for example Bioinformatica and Compilerbouw),
                                    # count one minus point.
                                    if mutual_courses[mutual_course] in schedule[i][j][z].name:
                                        minus_points += 1
                            # Also, if this course has a session of its own in
                            # this timeslot (for example: Bioinformatica and Bioinformatica)
                            # count one minus point.
                            own_session_counter = 0
                            for z in range(len(schedule[i][j])):
                                if schedule[i][j][z].name == schedule[i][j][k].name:
                                    # Count how many own_sessions there are in this timeslot
                                    own_session_counter += 1
                                # If own_session_counter is greater than 1, there is
                                # a conflicting session placed in this timeslot.
                                if own_session_counter > 1:
                                    minus_points += 1


                        # else:
                        #     # Each slot has a course name and the courses' mutual courses
                        #     # Mutual courses is a list of courses that can't be in the same timeslot
                        #     mutual_courses = schedule[i][j][k].course_object.mutual_courses
                        #     # For every mutual course in the mutual_courses list,
                        #     # check if it is placed in the same timeslot.
                        #     for mutual_course in range(len(mutual_courses)):
                        #         for z in range(len(schedule[i][j])):
                        #             # If this mutual course is placed in the same timeslot
                        #             # (for example Bioinformatica and Compilerbouw),
                        #             # count one minus point.
                        #             if mutual_courses[mutual_course] in schedule[i][j][z].name:
                        #                 minus_points += 1



                        # HIER MOET NOG EEN MALUS PUNT KOMEN VOOR ALS TUTORIAL GROEP A
                        # SAMEN MET PRACTICUM GROEP A ZIT!!!
                        # else:
                        #     # print(schedule[i][j][k])
                        #     for z in range(len(schedule[i][j])):
                        #         print(schedule[i][j][z])
                        #     print(" ______________")



        return minus_points

    def students_fit(schedule, courses, courses_schedule):
        """
        Returns the number of maluspoints that are given for the number of
        students that don't fit in the room of the session
        max aantal malus punten voor deze functie = 1332
        """
        # courses_schedule = Constraint.all_constraints(schedule, courses)
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


    def session_points(schedule, courses):
        courses_schedule = Constraint.all_constraints(schedule, courses)
        rooms = loaddata.load_rooms()

        spread_points = Constraint.session_spread_check(schedule, courses, courses_schedule)[1]
        # print(spread_points)

        points_dict = {}

        session_points_dict = [{"session_id_ov": 0, "capacity_points":0, "spread_malus_points": 0,
                                "spread_bonus_points": 0, "flex_points": 0, "points": 0} for i in range(SESSION_NUM)]

        maluspoints = 0
        counter = 0
        points = 0
        for course in courses:

            #  saves the room and type of the checked_course sessions
            checked_course = courses_schedule[course.course_id]
            room_ids = checked_course["room"]
            types = checked_course["type"]
            session_overall_ids = checked_course["overall_id"]

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

                # increases maluspoints with the number of students that don't have a seat
                if empty_seats < 0:
                    maluspoints += abs(empty_seats)
                    points = abs(empty_seats)

                    # print(session_overall_ids[i])
                    # print(abs(empty_seats))
                    # print(session_points_dict[session_overall_ids[i]])
                    session_points_dict[session_overall_ids[i]]["capacity_points"] += abs(empty_seats)

                    # Maak een dictionary van {session_id_ov : punten}
                # else:
                #     points = 0
                points_dict.update({counter:points})

                counter += 1

        # print(points_dict)
        try:
            malus_session_id = list(points_dict.keys())[list(points_dict.values()).index(max(points_dict.values()))]
        # If there are no malus points (for capacity_points)
        except ValueError:
            print(points_dict)
            malus_session_id = randint(0, SLOTS - 1)

        return malus_session_id

    def get_points(schedule, courses):
        """
        Returns the points of a given schedule. Some constraint checks return
        negative points, so these are substracted in stead of added to the points.
        Minimum minus points for lecture_first = 0, maxmimum = 39.
        Minimum of 'minus points' of mutual_course() = 0.
        Maximum of 'good points' of session_spread_check() = 440.
        Minimum of malus points of students_fit() = 0 and maxmimum = 1332.

        Multiply the points of the hard constraints (lecture_first and mutual_courses)
        to ensure that a schedule fulfills these constraints.

        BEREKENING:
        ALLE FUNCTIES 0 TOT 100 PUNTEN GEVEN
        Alles delen door max aantal punten en vermenigvuldigen met 100,
        hard constraints dan ook vermenigvuldigen met 2.
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)

        points = Constraint.session_spread_check(schedule, courses, courses_schedule) - \
                (Constraint.lecture_first(schedule, courses, courses_schedule) * 40) - \
                (Constraint.mutual_courses_check(schedule, courses) * 40) - \
                (Constraint.students_fit(schedule, courses, courses_schedule) / 6)

        return points
