import copy
import loaddata
import numpy as np
from constraint import Constraint
from random import randint

CHILDREN = 2
SLOTS = 140


def evaluate(schedule, courses):
    """
    Alle constraint functies bij elkaar, returned 1 getal
    """
    pass
    course_schedule = Constraint.all_constraints(schedule, courses)


def genetic_algortim(schedule1, schedule2):
    """
    Dit gaat ooit een genetisch algortime worden.

    TODO:
    - de twee kinderen omzetten naar echte roosters die we kunnen evalueren
    -

    """
    courses = loaddata.load_courses()

    # transform the schedule in a linear list
    parent1 = np.array(schedule1).flatten().tolist()
    parent2 = np.array(schedule2).flatten().tolist()

    # make a list of the overall_ids of the sessions in the schedule
    parent1_id = []
    parent2_id = []
    for i in range(len(parent1)):
        parent1_id.append(parent1[i].overall_id)
        parent2_id.append(parent2[i].overall_id)

    cycles = []
    cycles_len = []
    start_point = randint(0, SLOTS - 1)

    while len(cycles_len) < SLOTS:
        cycle_i = []
        index = parent1.index(parent1[start_point])
        in_cycle = [index]
        counter = 0

        while parent1_id[start_point] not in cycle_i:
            temp = parent2_id[index]
            cycle_i.append(temp)
            index = parent1_id.index(temp)
            in_cycle.append(index)
            counter += 1

        cycles.append(cycle_i)
        cycles_len += cycle_i

        start_point = randint(0, SLOTS - 1)
        while start_point in in_cycle:
            start_point = randint(0, SLOTS - 1)

    # copy the parents into the children
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    # divide the parents in cycles over the children
    for i in range(len(cycles)):
        for j in cycles[i]:
            child1[j] = parent2[j]
            child2[j] = parent1[j]

    # calculate the points of the children LATER DIT WAARSCHIJNLIJK IN EEN LOOPJE DOEN
    points_child1 = get_points(child1, courses)
    points_child2 = get_points(child2, courses)
    print(points_child1)
    print(points_child2)


    #     cycle_i = []
    #     index = np.where(flatten1 == flatten1[start_point])
    #     in_cycle = [index]
    #     # counter = 0
    #     print(f"index: {index}")
    #     print(f"start_pint {flatten1[start_point]}")
    #     # while flatten1[start_point] not in cycle_i:
    #         # print(counter)
    #         # counter += 1
    #     temp = flatten2[index]
    #     print(f"temp: {temp}")
    #     cycle_i.append(temp)
    #     print(f"cycle_i {cycle_i}")
    #     # index = flatten1.index(temp)
    #     index = np.where(flatten1 == temp)
    #     in_cycle.append(index)
    #
    #     cycles.append(cycle_i)
    #
    #     start_point = randint(0, SLOTS - 1)
    #     while start_point in in_cycle:
    #         start_point = randint(0, SLOTS - 1)
    #
    # print(f"cycles: {cycles}")

def get_points(schedule, courses):
    """
    Returns the points of a given schedule. Some constraint checks return
    negative points, so these are substracted in stead of added to the points.
    Minimum minus points for lecture_first = 0, maxmimum = 39.
    Minimum of 'minus points' of mutual_course() = 0.
    Maximum of 'good points' of session_spread_check() = 440.
    Minimum of malus points of students_fit() = 0 and maxmimum = 1332.
    """
    courses_schedule = Constraint.all_constraints_linear(schedule, courses)
    points = Constraint.session_spread_check(schedule, courses, courses_schedule) - \
        Constraint.lecture_first(schedule, courses, courses_schedule) - \
        Constraint.mutual_courses_check(schedule, courses) - \
        Constraint.students_fit(schedule, courses, courses_schedule)

    return points
