import copy
import numpy as np
import random
import schedulemaker
from constraint import Constraint
from operator import itemgetter
from random import randint

DAYS = 5
ROOMS = 7
TIME_SLOTS = 4
SLOTS = DAYS * ROOMS * TIME_SLOTS

K = 5
MUTATIONS = 10
PERCENTAGE = 0.3 * SLOTS
SWITCHES = 3


def genetic_algorithm(schedules, courses, population_size, generations,
                      choose):
    """
    Genetic algorithm

    Input: list of schedules, list of courses, population size (lenght of list
    of schedules), number of generations, way of choosing the parents (options
    are "k-way", "rank", "random")
    Output: a list which contains the best schedule of the last generation and
    the amount of points of that schedule
    """
    population = schedules

    for generation in range(generations):

        # chooses the parents in the desired way
        if choose is "k-way":
            parents = choose_parents_KWAY(population, courses, population_size)
        elif choose is "rank":
            parents = choose_parents_rank(population, courses, population_size)
        else:
            parents = choose_parents_random(population, population_size)

        children = []
        for i in range(0, population_size, 2):
            parent_pair = [parents[i], parents[i + 1]]

            # transform the schedule to a linear list
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
            child1, child2 = make_children(cycles, parent1, parent1_id,
                                           parent2, parent2_id)

            # add children to children
            children.append(child1)
            children.append(child2)

            # mutate children
            children = mutate_children(children)

        # add children to population
        population += children

        # choose new population out of the parents and children
        population = choose_parents_KWAY(population, courses, population_size)

    # get a list with both schedule and points from every individual
    population_points = []
    for i in range(0, population_size):
        points = Constraint.get_points(population[i], courses)
        population_points.append((population[i], points))

    # get the best schedule and it's points
    best_schedule = sorted(population_points, key=itemgetter(1))[-1][0]
    best_schedule = np.array(best_schedule)
    best_schedule = best_schedule.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
    best_points = sorted(population_points, key=itemgetter(1))[-1][1]

    # returns the best schedule in final population and it's points
    return best_schedule, best_points


def choose_parents_KWAY(population, courses, population_size):
    """
    Choose parents with a K-way tournament

    Input: list of schedules, list of courses, population size
    Output: list of parents
    """
    parents = []
    for i in range(population_size):

        # choose K schedules that will enter the tournament
        battlefield = []
        for j in range(K):

            # choose random schedule, remove from population, add to battlefield
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

    return parents


def choose_parents_random(population, population_size):
    """
    Choose the parents randomly

    Input: list of schedules, population size
    Output: list of parents
    """
    parents = []
    for i in range(population_size):
        parents.append(random.choice(population))

    return parents


def choose_parents_rank(population, courses, population_size):
    """
    Choose the parents with a ranking system

    Input: list of schedules, list of courses, population size
    Output: list of parents
    """
    parents = []

    # get points of all the schedules in the population
    population_points = []
    for i in range(population_size):
        points = Constraint.get_points(population[i], courses)
        population_points.append([population[i], points])

    # creates a list with more high ranked schedules low ranked ones
    ranking = sorted(population_points, key=itemgetter(1))
    chances = []
    for i in range(population_size):
        for j in range(i):
            chances.append(ranking[i][0])

    # choose the parents from the chances list
    for i in range(population_size):
        parents.append(random.choice(chances))

    return parents


def create_cycles(parent1_id, parent2_id):
    """
    Find existing cycles between the two parent schedules

    Input: two schedules
    Output: a list of cycles
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

    Input: list of cycles between two schedules, two schedules of which the
    cycles list is. These are in 3D format and 1D format. The 1D format
    contains only the overall_id's
    Output: two schedules
    """
    # copy the parents into the children
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    # add every other cycle of parent_i to the child_j
    cycle_len = []
    cycles.sort(key=len)
    for index, cycle in enumerate(cycles):
        cycle_len += cycle

        # give child1 PERCENTAGE of parent2 and child2 PERCENTAGE of parent1
        if len(cycle_len) <= PERCENTAGE:
            for overall_id in cycle:
                child1[parent1_id.index(overall_id)] = \
                    parent2[parent2_id.index(overall_id)]
                child2[parent2_id.index(overall_id)] = \
                    parent1[parent1_id.index(overall_id)]

    # convert the children to 3D lists
    child1 = np.asarray(child1).reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
    child2 = np.asarray(child2).reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    return(child1, child2)


def mutate_children(children):
    """
    Switches a random amount of sessions in a random amount of children

    Input: list of schedules
    Output: list of schedules
    """
    mutations = randint(1, MUTATIONS)
    for mutation in range(mutations):
        switches = randint(1, SWITCHES)
        child = random.choice(children)
        children.remove(child)
        child = schedulemaker.switch_session(child, switches)
        children.append(child)

    return children
