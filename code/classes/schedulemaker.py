import random
import numpy as np
import itertools

from session import Session
from random import randint

DAYS = 5
ROOMS = 7
TIME_SLOTS = 4
SLOTS = DAYS * ROOMS * TIME_SLOTS

# case specific
EMPTY_SESSIONS = 11
SESSIONS = SLOTS - EMPTY_SESSIONS


def initialize_schedule(courses):
    """
    Initialize schedule using Session()

    Input: TODO
    Output: a valid schedule

    TODO: (eventueel) andere namen aan lijsten geven want nu erg lang
    """

    schedule = [[[[None] for i in range(ROOMS)] for i in range(TIME_SLOTS)]
                for i in range(DAYS)]

    session_list = []
    lecture_sessions = []
    other_sessions = []
    empty_sessions = []
    session_list_2d = []

    # makes a list of all sessions
    for course in courses:
        session_list = session_list + course.sessions_total

        # make a list of lists for each course
        session_list_2d.append(course.sessions_total)

    # adds overall id's to the sessions
    session_counter = 0
    for i in range(len(session_list_2d)):
        for j in range(len(session_list_2d[i])):
            session_list_2d[i][j].overall_id = session_counter
            session_counter += 1

    # make SLOTS empty sessions
    for i in range(SLOTS):
        name = ' '
        type = ' '
        max_students = ' '
        session_id = 'nvt2'
        group_id = 'nvt2'
        empty_session = Session(name, type, max_students, session_id, group_id)
        empty_session.overall_id = SLOTS
        empty_sessions.append(empty_session)

    for i in range(len(session_list_2d)):
        for j in range(len(session_list_2d[i])):

            # put all lectures in list and put all other sessions in other list
            if session_list_2d[i][j].type == "lecture":
                lecture_sessions.append(session_list_2d[i][j])
            elif session_list_2d[i][j].type == "tutorial" or session_list_2d[i][j].type == "practicum":
                other_sessions.append(session_list_2d[i][j])

    counter_sessions = 0
    new_sched = False

    # creates schedules untill a valid schedule is created
    while not bool(new_sched):
        new_sched = fill_schedule(schedule, session_list_2d, lecture_sessions,
                                  empty_sessions, courses)
        counter_sessions += 1
        if new_sched is not False:
            break

    return schedule


def fill_schedule(schedule, sessions_2d, other_sessions, empty_sessions,
                  courses):
    """
    Fills schedule with sessions

    Input: An empty schedule, a 2D-list of all sessions sorted by course, a list
    of all session objects that are not lectures, a list of empty session objects,
    a list of course objects
    Output: If all sessions were placed in the schedule: a filled schedule.
            Else: a boolean (False).
    """

    # shuffle the 2d list and flatten it back to linear list
    # to get random list of sessions
    random.shuffle(sessions_2d)
    sessions = list(itertools.chain(*sessions_2d))

    # fills schedule with empty sessions to be able to loop through the schedule
    session_counter = 0
    for day in range(DAYS):
        for slot in range(TIME_SLOTS):
            for room in range(ROOMS):
                schedule[day][slot][room] = empty_sessions[session_counter]
                session_counter += 1


    passed_lectures = 0

    # loop through all sessions that are sorted in a list per course
    # to place them in the schedule
    for session in range(len(sessions)):

        lectures_first = False
        locations = []

        # a boolean that states whether the current session was placed in the schedule
        found = False

        # TODO comment DIT MOET WEG
        for course in courses:
            if sessions[session].name == course.name:
                sessions[session].course_object = course
                mutual_courses_session = \
                    sessions[session].course_object.mutual_courses

        # check wether the current session is a lecture
        if sessions[session].type == "lecture":
            lectures_first = True

        # loop through all locations in the schedule to determine whether this
        # location is available for the current session
        for day in range(DAYS):
            for slot in range(TIME_SLOTS):
                for room in range(ROOMS):

                    # check wether the current session is a tutorial or practicum
                    if not lectures_first:

                        # check wether the current location holds a session originating
                        # from the same course as the current session
                        if sessions[session].name == schedule[day][slot][room].name:

                            # check wether this session is a lecture
                            if schedule[day][slot][room].type == "lecture":

                                # delete all previous locations
                                locations.clear()
                                break

                            # check whether the session_id of the current session
                            # is the same as the session on this location in the schedule
                            elif not sessions[session].session_id == \
                                    schedule[day][slot][room].session_id:

                                # check whether the group of students of these sessions
                                # overlap
                                if sessions[session].group_id == \
                                        schedule[day][slot][room].group_id:

                                    # delete all locations of this day
                                    locations = delete_location(locations, slot, day)
                                    break

                        # check if the session in the current location
                        # is not part of a mutual course of the current session
                        elif schedule[day][slot][room].name in \
                                mutual_courses_session:

                            # delete all locations of this day
                            locations = delete_location(locations, slot, day)
                            break


                    # check if the current session(lecture) overlaps with
                    # a mutual course or its own course
                    elif sessions[session].name == schedule[day][slot][room].name \
                            or schedule[day][slot][room].name \
                            in mutual_courses_session:

                        # delete alle locations of this day
                        locations = delete_location(locations, slot, day)
                        break

                    # if all constraints are met, append current location to
                    # list of locations
                    if schedule[day][slot][room].name == ' ':
                        locations.append((day, slot, room))

        # check if any location was found for the current session
        if bool(locations):
            counter = 0

            # check if the current session is a lecture
            if lectures_first:

                # calculate the amount of remaining sessions of this course
                amount_sessions = sessions[session].course_object.lecture + \
                    sessions[session].course_object.tutorial + \
                    sessions[session].course_object.practicum
                prohibited_timeslots = amount_sessions - 1 - passed_lectures

                # keep track of the amount of lectures of this course scheduled
                passed_lectures += 1

                # delete the minimal amount of locations needed for the remaining
                # sessions of this course, starting at the end of the list
                while not counter == prohibited_timeslots:

                    # if no locations are left after applying the constraints
                    if not bool(locations) or \
                            prohibited_timeslots >= len(locations):
                        return False

                    # checks if the current location is not the same timeslot as
                    # the next location
                    elif not locations[-1][1] == locations[-2][1]:
                        counter += 1

                    locations.remove(locations[-1])

            # choose a random location of the location list
            rndm_location = random.choice(locations)
            schedule[rndm_location[0]][rndm_location[1]][rndm_location[2]] \
                = sessions[session]
            found = True

            # check if this was the last lecture of the course
            if not session == len(sessions) - 1 and \
                    (not sessions[session + 1].type == "lecture" or not
                     sessions[session].course_object ==
                     sessions[session + 1].course_object):
                passed_lectures = 0

        # if no locations were found for the current session
        else:
            return False

    # checks if a valid schedule is found
    if found:

        # give the empty_sessions overall_ids
        overall_id_counter = SESSIONS
        for day in range(DAYS):
            for slot in range(TIME_SLOTS):
                for room in range(ROOMS):

                    # checks if the session is empty
                    if schedule[day][slot][room].overall_id == SLOTS:
                        schedule[day][slot][room].overall_id = overall_id_counter
                        overall_id_counter += 1

        return schedule

    else:
        return False


def delete_location(locations, slot, day):
    """
    Deletes all locations from locations list that are on the slot and day given
    Input: list of locations, timeslot and day
    A location in this list is a coordinate consisting of three integer elements:
    a day, a slot and a room.
    Output: list with locations

    """
    for location in range(len(locations) - 1, -1, -1):
        if locations[location][1] == slot and locations[location][0] == day:
            del locations[location]

    return locations


def switch_session(schedule, number_of_switches):
    """
    Switches two random sessions in a schedule

    Input: schedule, number of switches that you want to make
    Output: schedule
    """

    # flatten schedule to get a 1D list to switch elements
    flatten = np.array(schedule).flatten()

    for i in range(number_of_switches):

        # get two random numbers
        random_number = randint(0, SLOTS - 1)
        random_switch_number = randint(0, SLOTS - 1)

        # if the numbers are equal, make another number
        while random_number is random_switch_number:
            random_number = randint(0, SLOTS - 1)
            random_switch_number = randint(0, SLOTS - 1)

        # make switch
        flatten[random_number], flatten[random_switch_number] = \
            flatten[random_switch_number], flatten[random_number]

    # convert back to 3D list
    schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    return schedule
