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

    PROBLEEM:
    HET GAAT FOUT MET EMPTY SESSIES EN DAAR WORDT IK VERDRIETIG VAN
    """
    flatten1 = np.array(schedule1).flatten().tolist()
    flatten2 = np.array(schedule2).flatten().tolist()

    cycles = []
    start_point = randint(0, SLOTS - 1)

    for i in range(CHILDREN):
        cycle_i = []
        index = flatten1.index(flatten1[start_point])
        in_cycle = [index]
        counter = 0

        while flatten1[start_point] not in cycle_i:
            print(counter)
            counter += 1
            temp = flatten2[index]
            cycle_i.append(temp)
            index = flatten1.index(temp)
            in_cycle.append(index)

        cycles.append(cycle_i)

        start_point = randint(0, SLOTS - 1)
        while start_point in in_cycle:
            start_point = randint(0, SLOTS - 1)

    print(cycles)


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
