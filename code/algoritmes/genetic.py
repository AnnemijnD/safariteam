import copy
import numpy as np
import random
from constraint import Constraint
from random import randint

CHILDREN = 2
DAYS = 5
GENERATIONS = 1
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

    for generation in range(GENERATIONS):
        children = []
        for i in range(0, POPULATION, 2):
            parents = [schedules[i], schedules[i + 1]]
            schedules.append(parents[0])
            schedules.append(parents[1])

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

        # TODO MUTATIONS

        # shuffle entire population
        population = schedules + children
        random.shuffle(population)

        # pick pairs and let only the best one "survive"
        for i in range(0, POPULATION, 2):
            battle = [population[i], population[i + 1]]
            points1 = get_points(battle[0], courses)
            points2 = get_points(battle[1], courses)
            if points1 > points2:
                population.remove(battle[1])
            else:
                population.remove(battle[0])

    population_points = []
    for i in range(0, POPULATION):
        points = get_points(population[i], courses)
        population_points.append(points)

    print(population_points)
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


def get_points(schedule, courses):
    """
    Returns the points of a given schedule. Some constraint checks return
    negative points, so these are substracted in stead of added to the points.
    Minimum minus points for lecture_first = 0, maxmimum = 39.
    Minimum of 'minus points' of mutual_course() = 0.
    Maximum of 'good points' of session_spread_check() = 440.
    Minimum of malus points of students_fit() = 0 and maxmimum = 1332.

    Multiply the points of the hard constraints (lecture_first and mutual_courses)
    to ensure that a schedule fulfills these constraints.
    """
    courses_schedule = Constraint.all_constraints(schedule, courses)

    points = Constraint.session_spread_check(schedule, courses, courses_schedule) - \
        (Constraint.lecture_first(schedule, courses, courses_schedule) * 40) - \
        (Constraint.mutual_courses_check(schedule, courses) * 40) - \
        (Constraint.students_fit(schedule, courses, courses_schedule) / 15)

    return points
