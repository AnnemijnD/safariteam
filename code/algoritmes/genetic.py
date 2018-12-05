import copy
import numpy as np
import random
import switch
from constraint import Constraint
from operator import itemgetter
from random import randint

CHILDREN = 2
DAYS = 5
GENERATIONS = 20
MUTATIONS = 5
POPULATION = 50
ROOMS = 7
SLOTS = 140
TIME_SLOTS = 4


def genetic_algortim(schedules, courses):
    """
    Dit gaat ooit een genetisch algortime worden.

    TODO:
    - mutatie toevoegen
    - ouders beter kiezen
    - battles beter kiezen
    """
    population_points = []
    for i in range(0, POPULATION):
        points = Constraint.get_points(schedules[i], courses)
        population_points.append(points)

    print(population_points)
    print(max(population_points), min(population_points))

    population = schedules

    for generation in range(GENERATIONS):

        sorted_population = []
        for i in range(0, POPULATION):
            points = Constraint.get_points(population[i], courses)
            sorted_population.append([points, population[i]])
        sorted_population = sorted(sorted_population, key=itemgetter(0))

        # "bewijs" van erg weinig diversiteit
        # print_list = []
        # for i in range(len(sorted_population)):
        #     print_list.append(sorted_population[i][0])
        # print(print_list)

        children = []
        for i in range(0, POPULATION, 2):
            parents = [sorted_population[i][1], sorted_population[i + 1][1]]
            # schedules.append(parents[0])
            # schedules.append(parents[1])

            # transform the schedule in a linear list
            parent1 = np.array(parents[0]).flatten().tolist()
            parent2 = np.array(parents[1]).flatten().tolist()

            # make a list of the overall_ids of the sessions in the schedule
            parent1_id = []
            parent2_id = []
            for i in range(len(parent1)):
                parent1_id.append(parent1[i].overall_id)
                parent2_id.append(parent2[i].overall_id)

            # find all the cycles between the two schedules
            cycles = create_cycles(parent1_id, parent2_id)

            # make children out of parent1 and parent2
            child1, child2 = make_children(cycles, parent1, parent1_id, parent2, parent2_id)

            # add children to children
            children.append(child1)
            children.append(child2)

        # dit ook in een losse functie doen?????
        # mutate a random amount of children
        mutations = randint(0, MUTATIONS)
        for mutation in range(mutations):
            child = random.choice(children)
            children.remove(child)
            child = switch.switch_session(child, 1, -1)
            children.append(child)

        # shuffle entire population
        population += children
        random.shuffle(population)

        # dit ook in een losse functie doen??????
        # pick pairs and let only the best one "survive"
        for i in range(0, POPULATION, 2):
            battle = [population[i], population[i + 1]]
            points1 = Constraint.get_points(battle[0], courses)
            points2 = Constraint.get_points(battle[1], courses)
            if points1 > points2:
                population.remove(battle[1])
            else:
                population.remove(battle[0])

    population_points = []
    for i in range(0, POPULATION):
        points = Constraint.get_points(population[i], courses)
        population_points.append(points)

    print(population_points)
    print(max(population_points), min(population_points))
    # TODO: BESTE ROOSTER RETURNEN


def create_cycles(parent1_id, parent2_id):
    """
    Create cycles between the two parent schedules.
    """
    cycles = []
    cycles_len = []

    # create a list with all possible start_points and choose one randomly
    start_points = set(range(0, SLOTS))
    start_point = random.sample(start_points, 1)[0]
    start_points.remove(start_point)

    # while not all slots are in a cycle, search for cycles
    in_cycle = set()
    in_cycle.add(start_point)
    while len(cycles_len) < SLOTS:
        cycle_i = []
        index = start_point

        # while the cycle is not finished, construct the cycle
        while parent1_id[start_point] not in cycle_i:
            temp = parent2_id[index]
            cycle_i.append(temp)
            index = parent1_id.index(temp)
            in_cycle.add(index)

        # add the cylce to the cycles list and increase the cycles_len
        cycles.append(cycle_i)
        cycles_len += cycle_i

        # pick a new start_point that isn't in in_cycle
        start_points = start_points.difference(in_cycle)
        if len(start_points) > 0:
            start_point = random.sample(start_points, 1)[0]

    return cycles


def make_children(cycles, parent1, parent1_id, parent2, parent2_id):
    """
    Use the cycles to make children out of the two parents
    """
    # copy the parents into the children
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    # add every other cycle of parent_i to the child_j
    for index, cycle in enumerate(cycles):
        if index // 2 == 0:
            for overall_id in cycle:
                child1[parent1_id.index(overall_id)] = parent2[parent2_id.index(overall_id)]
                child2[parent2_id.index(overall_id)] = parent1[parent1_id.index(overall_id)]

    # convert the children to 3D lists
    child1 = np.asarray(child1).reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
    child2 = np.asarray(child2).reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    return(child1, child2)
