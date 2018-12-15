import loaddata

TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SLOTS = DAYS * TIME_SLOTS * ROOMS
SLOTS_PER_DAY = ROOMS * TIME_SLOTS
MPF = 10  # TODO willen we hier uitleg bij???????

# case specific
EMPTY_SESSIONS = 11  # kan weg als SESSION_NUM weg is
SPREAD_BONUS = 20
MAX_FIT = 1332
MAX_SPREAD = 440
WEIGHT = MAX_FIT / MAX_SPREAD
SESSION_NUM = SLOTS - EMPTY_SESSIONS  # kan weg als alle ongebruikte functies weg zijn


# STRAKS AAN ANNEMOIN VRAGEN WAT IK HIERMEE HAD KUNNEN BEDOELEN
# TODO: class die courses in zich heeft en hier iets over zegt


class Constraint():
    """
    A class with all the constraint functions.
    """

    def all_constraints(schedule, courses):
        """
        Saves info of all the sessions of a course in a dictionary.

        Input: 3D schedule of which you want to check the constraints, list of
        all courses
        Output: list with for every course a dictionary that contains info of
        the sessions of that course

        TODO: [day, slot, room] werkt niet???????????
        TODO: ANNEMIJN: verwijder alles wat we niet meer gebruiken
        """

        courses_schedule = []
        for course in courses:

            # initialize dictionary with all the info you want to save
            course_schedule = {"day": [], "slot": [], "room": [], "type": [],
                               "session_id": [], "group_id": [],
                               "overall_id": []}
            for day in range(DAYS):
                for slot in range(TIME_SLOTS):
                    for room in range(ROOMS):
                        if schedule[day][slot][room] is not None:
                            if course.name == schedule[day][slot][room].name:
                                course_schedule["day"].append(day)
                                course_schedule["slot"].append(slot)
                                course_schedule["room"].append(room)
                                course_schedule["type"].append(
                                        schedule[day][slot][room].type)
                                course_schedule["session_id"].append(
                                        schedule[day][slot][room].session_id)
                                course_schedule["group_id"].append(
                                        schedule[day][slot][room].group_id)
                                course_schedule["overall_id"].append(
                                        schedule[day][slot][room].overall_id)

            courses_schedule.append(course_schedule)

        return courses_schedule

    def session_spread_check(schedule, courses, courses_schedule):
        """
        Calculates the amount of bonuspoints and maluspoints earned by
        spreading the sessions of a course.

        Input: schedule of which you want to check the constraints, list of all
        courses, list of dictionaries with info of all the sessions of a course
        Output: a list with the total amount of points, the amount of
        bonuspoints, the amount of maluspoints.

        TODO: ANNEMIJN verwijder alles wat we niet meer gebruiken
        """
        bonuspoints = 0
        maluspoints = 0
        course_dict = {}

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
            groups = max(courses_schedule[id]["group_id"])
            if groups > 0:

                # saves indices of groups together with lectures
                for i in range(groups):
                    same_group = [j for j,
                                  e in enumerate(courses_schedule[id]["group_id"])
                                  if e == i + 1]
                    sessions.append(lectures + same_group)
            else:
                sessions = [lectures]

            # calculates the spread_bonus per group
            spread_bonus = SPREAD_BONUS / len(sessions)

            if course.sessions == 2:

                bonuspoints += Constraint.spread_detail(sessions, [0, 3],
                                                        courses_schedule, id,
                                                        spread_bonus)

                bonuspoints += Constraint.spread_detail(sessions, [1, 4],
                                                        courses_schedule, id,
                                                        spread_bonus)

            elif course.sessions == 3:

                bonuspoints += Constraint.spread_detail(sessions, [0, 2, 4],
                                                        courses_schedule, id,
                                                        spread_bonus)

            elif course.sessions == 4:

                bonuspoints += Constraint.spread_detail(sessions, [0, 1, 3, 4],
                                                        courses_schedule, id,
                                                        spread_bonus)

            elif course.sessions == 5:

                bonuspoints += Constraint.spread_detail(sessions, [0, 1, 2, 3, 4],
                                                        courses_schedule, id,
                                                        spread_bonus)

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

            course_dict.update({id: (round(course_mal_points - course_bon_points))})

        bonuspoints = round(bonuspoints)
        maluspoints = round(maluspoints)
        spread_points = maluspoints + bonuspoints
        Constraint.bonus_malus = course_bonus_malus

        return [spread_points, course_dict, bonuspoints, maluspoints]

    def spread_detail(sessions, bonus_days, courses_schedule, id, spread_bonus):
        """
        Increases bonuspoints when the sessions are spread over the days as
        desired

        Input: TODO
        Output: increased amount of bonuspoints
        """
        bonuspoints = 0

        for i in range(len(sessions)):

            # makes a list of the days of the sessions
            days = []
            for j in range(len(sessions[i])):
                days.append(courses_schedule[id]["day"][sessions[i][j]])

            # checks if the courses are on the correct days
            if (days == bonus_days):
                bonuspoints += spread_bonus

        return bonuspoints

    def lecture_first(schedule, courses, courses_schedule):
        """
        Checks per course if the lectures are scheduled before the other
        sessions

        Input: TODO
        Output: amount of lecture points
        """
        lecture_points = 0
        for course in courses:

            # checks for all lectures if the lectures are planned first
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
        for day in range(DAYS):
            for slot in range(TIME_SLOTS):
                for room in range(ROOMS):
                    # Check if this slot is filled (= check if not None)
                    if schedule[day][slot][room].course_object:
                        # Check if session in this slot is a lecture
                        if schedule[day][slot][room].type == "lecture":
                            # Each slot has a course name and the courses'
                            # mutual courses. Mutual courses is a list of
                            # courses that can't be in the same timeslot
                            mutual_courses = schedule[day][slot][room].course_object.mutual_courses
                            # For every mutual course in the mutual_courses list,
                            # check if it is placed in the same timeslot.
                            for mutual_course in range(len(mutual_courses)):
                                for z in range(len(schedule[day][slot])):
                                    # If this mutual course is placed in the
                                    # same timeslot (for example Bioinformatica
                                    # and Compilerbouw), count one minus point.
                                    if mutual_courses[mutual_course] in \
                                            schedule[day][slot][z].name:
                                        minus_points += 1
                            # Also, if this course has a session of its own in
                            # this timeslot (for example: Bioinformatica and
                            # Bioinformatica) count one minus point.
                            own_session_counter = 0
                            for z in range(len(schedule[day][slot])):
                                if schedule[day][slot][z].name == \
                                        schedule[day][slot][room].name:
                                    # Count number of sessions in this timeslot
                                    own_session_counter += 1
                                # If own_session_counter is greater than 1, there's
                                # a conflicting session placed in this timeslot.
                                if own_session_counter > 1:
                                    minus_points += 1
                        else:
                            # If session is a pratical or tutorial, check if
                            # groups aren't planned in at the same timeslot
                            own_session_counter = 0
                            # Check in every timeslot
                            for z in range(len(schedule[day][slot])):
                                if schedule[day][slot][z].name ==  \
                                        schedule[day][slot][room].name:
                                    # Count one minuspoint if the same group_id
                                    # is found for this course in this timeslot.
                                    if schedule[day][slot][z].group_id is \
                                            schedule[day][slot][room].group_id:
                                        own_session_counter += 1
                            # own_session_counter will always be 1, so check if
                            # the counter is higher than 1.
                            if own_session_counter > 1:
                                minus_points += 1

        return minus_points

    def students_fit(schedule, courses, courses_schedule):
        """
        Calculates per session the number of students that don't fit in the
        classroom (maluspoints)

        Input: TODO
        Output: amount of maluspoints
        """
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
                    students = course.max_students_practicum

                # calculates how many empty seats there are
                empty_seats = rooms[room_ids[i]].capacity - students

                # increases maluspoints with nmbr of students that don't fit
                if empty_seats < 0:
                    maluspoints += abs(empty_seats)
        return maluspoints

    def get_points(schedule, courses):
        """
        Calculates the point of a given schedule. Including the lecture- and
        mutualpoints to make sure validness of a schedule is considered.

        Input:
        Output: total amount of points of a schedule
        """
        course_schedule = Constraint.all_constraints(schedule, courses)

        points = Constraint.session_spread_check(schedule, courses,
                                                 course_schedule)[0] - \
            (Constraint.lecture_first(schedule, courses, course_schedule) * 100) - \
            (Constraint.mutual_courses_check(schedule, courses) * 100) - \
            (Constraint.students_fit(schedule, courses, course_schedule) / 4)

        return points

    def get_points_final(schedule, courses):
        """
        Calculates the points of a schedule only considering the 'real' bonus-
        and maluspoints

        Input: TODO
        Output: total amount of points of a schedule
        """
        course_schedule = Constraint.all_constraints(schedule, courses)

        points = Constraint.session_spread_check(schedule, courses,
                                                 course_schedule)[0] - \
            Constraint.students_fit(schedule, courses, course_schedule)

        return points
