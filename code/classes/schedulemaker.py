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
        name, type, max_students, session_id, group_id = " ", " ", " ", " ", " "
        empty_session = Session(name, type, max_students, session_id, group_id)
        empty_session.overall_id = SLOTS
        empty_sessions.append(empty_session)

    for i in range(len(session_list_2d)):
        for j in range(len(session_list_2d[i])):

            # put all lectures in list and put all other sessions in other list
            if session_list_2d[i][j].type == "lecture":
                lecture_sessions.append(session_list_2d[i][j])
            elif session_list_2d[i][j].type == "tutorial" or \
                    session_list_2d[i][j].type == "practical":
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

    Input: TODO
    Output:
    """

    # shuffle the 2d list and flatten it back to linear list
    random.shuffle(sessions_2d)
    sessions = list(itertools.chain(*sessions_2d))

    # fills schedule with different empty sessions
    session_counter = 0
    for day in range(DAYS):
        for slot in range(TIME_SLOTS):
            for room in range(ROOMS):

                schedule[day][slot][room] = empty_sessions[session_counter]
                session_counter += 1

    # TODO dit naar iets veranderen
    # vertelt hoeveelste lecture van dit vak dit is
    passed_lectures = 0

    # TODO: comment
    # found = False
    for session in range(len(sessions)):

        lectures_first = False
        locations = []
        found = False

        # TODO comment
        for course in courses:
            if sessions[session].name == course.name:
                sessions[session].course_object = course
                mutual_courses_session = \
                    sessions[session].course_object.mutual_courses

        # checks if the session is a lecture
        if sessions[session].type == "lecture":
            lectures_first = True

        #  TODO comment
        for day in range(DAYS):
            for slot in range(TIME_SLOTS):
                for room in range(ROOMS):

                    # if session is a tutorial or practicum
                    if not lectures_first:

                        # TODO comment
                        if sessions[session].name == schedule[day][slot][room].name:

                            # TODO comment
                            if schedule[day][slot][room].type == "lecture":

                                # delete all previous locations
                                locations.clear()
                                break

                            # TODO comment
                            elif not sessions[session].session_id == \
                                    schedule[day][slot][room].session_id:

                                # TODO comment
                                if sessions[session].group_id == \
                                        schedule[day][slot][room].group_id:
                                    locations = delete_location(locations, slot, day)
                                    break

                        # TODO comment
                        elif schedule[day][slot][room].name in \
                                mutual_courses_session:
                            locations = delete_location(locations, slot, day)
                            break

                    #  TODO comment
                    # als het een lecture is
                    elif sessions[session].name == schedule[day][slot][room].name \
                            or schedule[day][slot][room].name \
                            in mutual_courses_session:

                        locations = delete_location(locations, slot, day)
                        break

                    # if the slot in the schedule is empty
                    if schedule[day][slot][room].name == ' ':
                        locations.append((day, slot, room))

        # TODO comment
        if bool(locations):
            counter = 0

            # TODO comment
            # als het een lecture was, verwijder het aantal potentiele locaties aan het einde van het rooster gelijk
            # aan de hoeveelheid vakken die er nog moeten worden ingedeeld
            if lectures_first:

                amount_sessions = sessions[session].course_object.lecture + \
                    sessions[session].course_object.tutorial + \
                    sessions[session].course_object.practical
                prohibited_timeslots = amount_sessions - 1 - passed_lectures

                passed_lectures += 1

                # TODO comment
                while not counter == prohibited_timeslots:

                    # TODO comment
                    if not bool(locations) or \
                            prohibited_timeslots >= len(locations):
                        return False

                    # TODO comment
                    elif not locations[-1][1] == locations[-2][1]:
                        counter += 1

                    locations.remove(locations[-1])

            # TODO comment
            rndm_location = random.choice(locations)
            schedule[rndm_location[0]][rndm_location[1]][rndm_location[2]] \
                = sessions[session]
            found = True

            # TODO comment
            # als dit het laatste lecture van het vak was of als er geen andere sessies meer zijn van dit vak:
            if not session == len(sessions) - 1 and \
                    (not sessions[session + 1].type == "lecture" or not
                     sessions[session].course_object ==
                     sessions[session + 1].course_object):
                passed_lectures = 0

        # TODO comment
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
    Deletes location from locations list

    Input: TODO
    Output: list with locations

    TODO ANNEMIJN: klopt deze uitleg???
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
