import copy
import loaddata
import numpy as np
import random
from constraint import Constraint
from random import randint

CHILDREN = 2
DAYS = 5
POPULATION = 50
ROOMS = 7
SLOTS = 140
TIME_SLOTS = 4


def genetic_algortim(schedules, courses):
    """
    Dit gaat ooit een genetisch algortime worden.

    TODO:
    - eerst 50 valide roosters maken (GAAT ERIN ALS INPUT) DONE
    - random 25 paren kiezen uit de 50 (populatie lijst shuffelen voor gebruik) DONE
    - al die paren kinderen laten maken: populatie nu 100 DONE
    - 50 paren kiezen --> roosters evalueren beste van het paar houden andere verwijderen uit populatie DONE
    - dit alles in een while zetten en stopcriterium bepalen
    """
    test = get_points(schedules[0], courses)
    print(test)

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

        # initialize start_point and empty lists
        cycles = []
        cycles_len = []
        start_point = randint(0, SLOTS - 1)

        # while not all slots are looked at, search for cycles
        while len(cycles_len) < SLOTS:
            cycle_i = []
            index = parent1.index(parent1[start_point])
            in_cycle = [index]

            # while the cycle is not 'finished', construct the cycle
            while parent1_id[start_point] not in cycle_i:
                temp = parent2_id[index]
                cycle_i.append(temp)
                index = parent1_id.index(temp)
                in_cycle.append(index)

            # add the cylce to the cycles list and increase the cycles_len
            cycles.append(cycle_i)
            cycles_len += cycle_i

            # constructs a startpoint that isn't in any cycle yet
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

        # convert the children to 3D lists and add them to children
        child1 = np.asarray(child1)
        child2 = np.asarray(child2)
        child1 = child1.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
        child2 = child2.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
        children.append(child1)
        children.append(child2)

    # shuffle entire population
    population = schedules + children
    random.shuffle(population)

    # pick pairs and let only the best one "survive"
    for i in range(0, POPULATION, 2):
        battle = [population[i], population[i + 1]]
        # DIT GAAT NOG FOUT 4 VD 5 KEER HUILEN, QUINTEN HELP. GET_POINTS IS NIET GOED
        points1 = get_points(battle[0], courses)
        points2 = get_points(battle[1], courses)
        if points1 > points2:
            population.remove(battle[1])
        else:
            population.remove(battle[0])


    # calculate the points of the children LATER DIT WAARSCHIJNLIJK IN EEN LOOPJE DOEN
    # points_child1 = get_points(child1, courses)
    # points_child2 = get_points(child2, courses)
    # print(points_child1)
    # print(points_child2)


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
