import copy
import numpy as np
from random import randint

CHILDREN = 2
SLOTS = 140


def genetic_algortim(schedule1, schedule2):
    """
    Dit gaat ooit een genetisch algortime worden.

    Begin met twee roosters combineren:
    PSEUDO:
    - maak lineaire lijst van beide roosters
    -

    """
    flatten1 = np.array(schedule1).flatten().tolist()
    flatten2 = np.array(schedule2).flatten().tolist()

    flatten1_id = []
    for i in range(len(flatten1)):
        flatten1_id.append(flatten1[i].overall_id)

    flatten2_id = []
    for i in range(len(flatten2)):
        flatten2_id.append(flatten2[i].overall_id)

    # print(flatten1_id)
    # print(flatten2_id)

    cycles = []
    cycles_len = []
    start_point = randint(0, SLOTS - 1)

    while len(cycles_len) < SLOTS:
        cycle_i = []
        index = flatten1.index(flatten1[start_point])
        in_cycle = [index]
        counter = 0

        while flatten1_id[start_point] not in cycle_i:
            temp = flatten2_id[index]
            cycle_i.append(temp)
            index = flatten1_id.index(temp)
            in_cycle.append(index)
            counter += 1

        cycles.append(cycle_i)
        cycles_len += cycle_i

        start_point = randint(0, SLOTS - 1)
        while start_point in in_cycle:
            start_point = randint(0, SLOTS - 1)

    child1 = copy.deepcopy(flatten1)
    child2 = copy.deepcopy(flatten2)
    for i in range(len(cycles)):
        for j in cycles[i]:
            child1[j] = flatten2[j]
            child2[j] = flatten1[j]




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
