import copy
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

    child1 = np.asarray(child1)
    child2 = np.asarray(child2)



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
