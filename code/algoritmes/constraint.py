import loaddata

TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SLOTS = DAYS * TIME_SLOTS * ROOMS
SLOTS_PER_DAY = ROOMS * TIME_SLOTS

# Malus point factor
MPF = 10

# case specific
EMPTY_SESSIONS = 11  # kan weg als SESSION_NUM weg is
SPREAD_BONUS = 20
MAX_FIT = 1332
MAX_SPREAD = 440
WEIGHT = MAX_FIT / MAX_SPREAD
SESSION_NUM = SLOTS - EMPTY_SESSIONS  # kan weg als alle ongebruikte functies weg zijn


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
        """

        bonuspoints = 0
        maluspoints = 0

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


        bonuspoints = round(bonuspoints)
        maluspoints = round(maluspoints)
        spread_points = maluspoints + bonuspoints

        return spread_points

    def spread_detail(sessions, bonus_days, courses_schedule, id,
                      spread_bonus):
        """
        Increases bonuspoints when the sessions are spread over the days as
        desired

        Input: list of sessions where you want to check the spread of, days
        on which the sessions should be scheduled for a bonus, dictionary with
        info of the sessions of every course, id of course, amount of
        bonuspoints that should be given
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

        Input: schedule, list of courses, dictionary with info of the sessions
        of every course
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
        same timeslot.

        Input: schedule, list of courses
        Output: amount of minus points calculated by number of conflicting
        courses
        """

        minus_points = 0

        # check every slot in the schedule
        for day in range(DAYS):
            for slot in range(TIME_SLOTS):
                for room in range(ROOMS):

                    # check if this slot is filled (= check if not None)
                    if schedule[day][slot][room].course_object:

                        # if session in this slot is a lecture
                        if schedule[day][slot][room].type == "lecture":

                            # get list of mutual courses
                            mutual_courses = \
                                schedule[day][slot][room].course_object.mutual_courses

                            # check if session is in same slot as mutual course session
                            for mutual_course in range(len(mutual_courses)):
                                for i in range(len(schedule[day][slot])):

                                    # if session is in same slot, count 1 minus point
                                    if mutual_courses[mutual_course] in \
                                            schedule[day][slot][i].name:
                                        minus_points += 1

                            # count minus points for session of own course in same slot
                            own_session_counter = 0
                            for i in range(len(schedule[day][slot])):
                                if schedule[day][slot][i].name == \
                                        schedule[day][slot][room].name:

                                    # count number of sessions in this timeslot
                                    own_session_counter += 1

                                # if sessions in same slot add minus_point
                                if own_session_counter > 1:
                                    minus_points += 1

                        # if session is practical or tutorial
                        else:

                            # check for every slot if there aren't multiple groups
                            own_session_counter = 0
                            for i in range(len(schedule[day][slot])):
                                if schedule[day][slot][i].name ==  \
                                        schedule[day][slot][room].name:

                                    # count minuspoint if same group is found
                                    if schedule[day][slot][i].group_id is \
                                            schedule[day][slot][room].group_id:
                                        own_session_counter += 1

                            # if groups in same slot add minus_point
                            if own_session_counter > 1:
                                minus_points += 1

        return minus_points

    def students_fit(schedule, courses, courses_schedule):
        """
        Calculates per session the number of students that don't fit in the
        classroom (maluspoints)

        Input: schedule, list of courses, dictionary with info of the sessions
        of every course
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

        Input: schedule, list of courses
        Output: total amount of points of a schedule
        """
        course_schedule = Constraint.all_constraints(schedule, courses)

        points = Constraint.session_spread_check(schedule, courses,
                                                 course_schedule) - \
            (Constraint.lecture_first(schedule, courses, course_schedule) * 100) - \
            (Constraint.mutual_courses_check(schedule, courses) * 100) - \
            (Constraint.students_fit(schedule, courses, course_schedule) / WEIGHT)

        return points

    def get_points_final(schedule, courses):
        """
        Calculates the points of a schedule only considering the 'real' bonus-
        and maluspoints

        Input: schedule, list of courses
        Output: total amount of points of a schedule
        """
        course_schedule = Constraint.all_constraints(schedule, courses)

        points = Constraint.session_spread_check(schedule, courses,
                                                 course_schedule) - \
            Constraint.students_fit(schedule, courses, course_schedule)

        return points
