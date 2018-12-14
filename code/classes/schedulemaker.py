
import random
import numpy as np

from session import Session
from random import randint


SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7


def initialize_schedule(courses):
    """
    Initialize schedule using Session().
    """

    schedule = [[[[None] for i in range(ROOMS)] for i in range(TIME_SLOTS)] for i in range(DAYS)]

    sessions = []
    session_list = []
    lecture_sessions = []
    other_sessions = []
    empty_sessions = []

    # random.shuffle(courses)

    # ANNEMIJN KAN JE HIER NOG EEN COMMENT BIJ ZETTEN, SNap niet wat je hier hebt gedaan

    for course in courses:
        session_list = session_list + course.sessions_total

    session_counter = 0
    for i in range(len(session_list)):
        session_list[i].overall_id = session_counter
        session_counter += 1

    # make #SLOTS empty sessions
    for i in range(SLOTS):
        name = ' '
        type = ' '
        max_students = ' '
        session_id = 'nvt2'
        group_id = 'nvt2'
        empty_session = Session(name, type, max_students, session_id, group_id)
        empty_session.overall_id = SLOTS
        empty_sessions.append(empty_session)

    for i in range(len(session_list)):
        # Get all the lectures
        if session_list[i].type == "lecture":
            lecture_sessions.append(session_list[i])
        elif session_list[i].type == "tutorial" or session_list[i].type == "practical":
            other_sessions.append(session_list[i])

    # shuffle de lectures zodat ze random zijn
    # Make copy of sessions and shuffle
    lectures = lecture_sessions[:]
    others = other_sessions[:]
    # random.shuffle(lectures)
    # random.shuffle(other_sessions)

    # De lijst met totale sessies bestaat dus uit een lijst met eerst
    # Hoorcolleges, daarna de andere sessies en is opgevuld tot 140 met lege sessies
    total = []
    total = lectures + other_sessions

    # plan.fill_schedule(schedule, total, other_sessions, empty_sessions, courses)
    # print(session_list)
    # print(len(session_list))
    counter_sessions = 0
    new_sched = False

    while not bool(new_sched):
        new_sched = fill_schedule(schedule, session_list, lecture_sessions, empty_sessions, courses)
        counter_sessions += 1
        if not new_sched == False:
            break

    return schedule, total, other_sessions, empty_sessions


def fill_schedule(schedule, lectures, other_sessions, empty_sessions, courses):
    """
    Fill empty schedule with sessions.
    """

    # Gebruik nested for loop om elke cel een session te gegen.
    # Je geeft hierbij een lijst met sessies mee aan de functie get_session
    # De lijst met sessies is al gemaakt in initialize_schedule()

    # Vul eerst met lege sessions
    # counter = 0
    session_counter = 0
    for b in range(DAYS):
        for c in range(TIME_SLOTS):
            for d in range(ROOMS):
                schedule[b][c][d] = empty_sessions[session_counter]
                # Counter for number of sessions placed in the schedule
                session_counter += 1

    # vertelt hoeveelste lecture van dit vak dit is
    passed_lectures = 0


    # found = False
    for e in range(len(lectures)):
        # print(lectures[e].name)

        lectures_first = False
        tut_or_prac = False
        location = []
        found = False


        for course in courses:
            if lectures[e].name == course.name:
               lectures[e].course_object = course
               mutual_courses_session = lectures[e].course_object.mutual_courses

        # is dit een hoorcollege?
        if lectures[e].type == "lecture":
            lectures_first = True
        else:
            tut_or_prac = True

        for b in range(DAYS):

            for c in range(TIME_SLOTS):

                rooms_allowed = True
                # availibility = True
                for d in range(ROOMS):

                    # als het een tutorial of pracitcal is
                    if not lectures_first:


                        if lectures[e].name == schedule[b][c][d].name:
                            if schedule[b][c][d].type == "lecture":

                                # alle eerdere locaties mogen weg want er mag niets voor een lecture
                                location.clear()
                                # print(location)
                                break
                            elif not lectures[e].session_id == schedule[b][c][d].session_id:
                                if lectures[e].group_id == schedule[b][c][d].group_id:
                                    for k in range(len(location) - 1, -1, -1):
                                        if location[k][1] == c and location[k][0] == b:
                                            del location[k]
                                    break


                        elif schedule[b][c][d].name in mutual_courses_session:
                            rooms_allowed = False
                            for k in range(len(location) - 1, -1, -1):
                                if location[k][1] == c and location[k][0] == b:
                                    del location[k]

                            break



                    # als het een lecture is
                    elif lectures[e].name == schedule[b][c][d].name or schedule[b][c][d].name in mutual_courses_session:

                        # achteruit itereren anders gaat het verwijderen niet goed
                        for k in range(len(location) - 1, -1, -1):
                            if location[k][1] == c and location[k][0] == b:
                                del location[k]
                        rooms_allowed = False

                        # print(location)
                        break

                    # if the slot in the schedule is empty
                    if schedule[b][c][d].name == ' ':
                        location.append((b,c,d))

        if bool(location):
            counter = 0

            # als het een lecture was, verwijder het aantal potentiele locaties aan het einde van het rooster gelijk
            # aan de hoeveelheid vakken die er nog moeten worden ingedeeld
            if lectures_first:

                amount_sessions = lectures[e].course_object.lecture + lectures[e].course_object.tutorial + lectures[e].course_object.practical
                prohibited_timeslots = amount_sessions - 1 - passed_lectures

                # probleem: er moeten nu teveel plekken open worden gehouden
                passed_lectures += 1


                while not counter == prohibited_timeslots:
                    if not bool(location) or prohibited_timeslots >= len(location):

                        return False

                    elif not location[-1][1] == location[-2][1]:
                        # print(location)
                        counter +=1
                    location.remove(location[-1])

            random_location = random.choice(location)
            # print(random_location)
            schedule[random_location[0]][random_location[1]][random_location[2]] = lectures[e]
            found = True
            # als dit het laatste lecture van het vak was of als er geen andere sessies meer zijn van dit vak:
            if not e == len(lectures) - 1 and (not lectures[e + 1].type == "lecture" or not lectures[e].course_object == lectures[e + 1].course_object):
                passed_lectures = 0


        else:

            # plan.schedule_counter += 1

            return False
            # return schedule
            #plan.initialize_schedule(plan.courses)
            # break
    if found:

        # give the empty_sessions overall_ids
        overall_id_counter = 129
        for i in range(DAYS):
            for j in range(TIME_SLOTS):
                for k in range(ROOMS):
                    # checks if the session is empty
                    if schedule[i][j][k].overall_id == SLOTS:
                        schedule[i][j][k].overall_id = overall_id_counter
                        overall_id_counter += 1

        return schedule

    else:
        # plan.schedule_counter += 1

        return False

# def random_schedule(schedule, sessions):
#     """
#     Generates a random schedule. Assigns every session to a random timeslot.
#     """
#
#     # Maak een 1D lijst van schedule
#     flatten = np.array(schedule, dtype=object).flatten()
#
#     random_numbers = []
#
#     for i in range(len(sessions)):
#         rand = random.randint(0, SLOTS - 1)
#         while rand in random_numbers:
#             rand = random.randint(0, SLOTS - 1)
#         random_numbers.append(rand)
#         flatten[rand] = sessions[i]
#
#     # Convert back to 3D list
#     schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
#
#     return schedule

def switch_session(schedule, number_of_switches, session_to_switch):
    """
    Returns a schedule with two randomly switched sessions.
    number_of_switches determines how many switches have to be made.
    """

    # Flatten schedule to get a 1D list to switch elements, otherwise a
    # deepcopy is needed, which is slower than this step.
    flatten = np.array(schedule).flatten()

    # If there is no specific session to switch, make a random switch
    if session_to_switch < 0:

        for i in range(number_of_switches):
            # Get two random numbers
            random_number = randint(0, SLOTS - 1)
            random_switch_number = randint(0, SLOTS - 1)

            # If the numbers are equal to each other, make another number
            while random_number is random_switch_number:
                random_number = randint(0, SLOTS - 1)
                random_switch_number = randint(0, SLOTS - 1)
            # Make the switch
            flatten[random_number], flatten[random_switch_number] = flatten[random_switch_number], flatten[random_number]

    # Convert back to 3D list
    schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    # Return 3D matrix of schedule
    return schedule
