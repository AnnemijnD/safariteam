import copy
import numpy as np
import random
import switch
from constraint import Constraint
from operator import itemgetter
from random import randint

CHILDREN = 2
DAYS = 5
GENERATIONS = 50
K = 5
MUTATIONS = 10
PERCENTAGE = 52
POPULATION = 50
ROOMS = 7
SLOTS = 140
SWITCHES = 3
TIME_SLOTS = 4


def genetic_algortim(schedules, courses):
    """
    Genetic algorithm in which the two bes, the two second best, ...,
    the two worst schedules in the population generate children. After
    generating children the best half of the population survives.
    """
    population_points = []
    for i in range(0, POPULATION):
        points = Constraint.get_points(schedules[i], courses)
        population_points.append(points)

    # print(population_points)
    # print(max(population_points), min(population_points), sum(population_points) / len(population_points))
    saved = max(population_points)

    population = schedules

    for generation in range(GENERATIONS):

        # choose the parents
        # if generation > 10:
        #     parents = choose_parents_KWAY(population, courses)
        # else:
        #     parents = choose_parents_rank(population, courses)
        # parents = choose_parents_KWAY(population, courses)
        parents = choose_parents_rank(population, courses)

        children = []
        for i in range(0, POPULATION, 2):
            parent_pair = [parents[i], parents[i + 1]]

            # transform the schedule in a linear list
            parent1 = np.array(parent_pair[0]).flatten().tolist()
            parent2 = np.array(parent_pair[1]).flatten().tolist()

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

            # mutate children
            children = mutate_children(children)

        # add children to population
        population += children

        # choose survivors
        population = choose_parents_KWAY(population, courses)

    population_points = []
    for i in range(0, POPULATION):
        points = Constraint.get_points(population[i], courses)
        population_points.append(points)

    # print(population_points)
    # print(max(population_points), min(population_points), sum(population_points) / len(population_points))
    # print(f"improvement {max(population_points) - saved}")

    # TODO: BESTE ROOSTER RETURNEN
    return max(population_points)


def choose_parents_KWAY(population, courses):
    """
    Choose parents with a K-way tournamentself.

    PRESTEERT WEL AL EEN BEETJE MAAR ERG WEINIG DIVERSITEIT TUSSEN DE OUDERS
    """
    parents = []
    for i in range(POPULATION):

        # choose K schedules that will enter the tournament
        battlefield = []
        for j in range(K):

            # choose random schedule, remove it from population, add to battlefield
            chosen = random.choice(population)
            population.remove(chosen)
            points = Constraint.get_points(chosen, courses)
            battlefield.append((chosen, points))

        # choose winner, add winner to the parents
        winner = sorted(battlefield, key=itemgetter(1))[-1][0]
        parents.append(winner)

        # put contestents back in the population
        for j in range(K):
            population.append(battlefield[j][0])

    # print_list = []
    # for i in range(len(parents)):
    #     print_list.append(Constraint.get_points(parents[i], courses))
    #
    # print(max(print_list), min(print_list), sum(print_list) / len(print_list))

    return parents


def choose_parents_random(population):
    """
    Choose the parents randomly
    """
    parents = []
    for i in range(POPULATION):
        parents.append(random.choice(population))
    return parents


def choose_parents_rank(population, courses):
    """
    When the population isn't very diverse rank the schedules. The best
    schedules have a bigger chance to be a parent.
    """
    parents = []

    # get points of all the schedules in the population
    population_points = []
    for i in range(POPULATION):
        points = Constraint.get_points(population[i], courses)
        population_points.append([population[i], points])

    # create a list with high ranked schedules in there more than low ranked ones
    ranking = sorted(population_points, key=itemgetter(1))
    chances = []
    for i in range(POPULATION):
        for j in range(i):
            chances.append(ranking[i][0])

    # choose the parents from the chances list
    for i in range(POPULATION):
        parents.append(random.choice(chances))

    # print(parents)

    # print_list = []
    # for i in range(len(parents)):
    #     print_list.append(Constraint.get_points(parents[i], courses))

    # print(max(print_list), min(print_list), sum(print_list) / len(print_list))

    return parents


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

    # len(cycles)

    # add every other cycle of parent_i to the child_j
    cycle_len = []
    cycles.sort(key=len)
    # print(cycles)
    for index, cycle in enumerate(cycles):
        cycle_len += cycle
        if len(cycle_len) <= PERCENTAGE:
            # print(f"cycle length first {len(cycle_len)}")
        # if index // 4 == 0:
            for overall_id in cycle:
                child1[parent1_id.index(overall_id)] = parent2[parent2_id.index(overall_id)]
                child2[parent2_id.index(overall_id)] = parent1[parent1_id.index(overall_id)]
        # else:
        #     print(f"cycle length after {len(cycle_len)}")



    # convert the children to 3D lists
    child1 = np.asarray(child1).reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
    child2 = np.asarray(child2).reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    return(child1, child2)


def mutate_children(children):
    """
    Mutate a random amount of children
    """
    mutations = randint(1, MUTATIONS)
    for mutation in range(mutations):
        switches = randint(1, SWITCHES)
        child = random.choice(children)
        children.remove(child)
        child = switch.switch_session(child, switches, -1)
        children.append(child)

    return children
