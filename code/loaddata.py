# Loads original data from heuristieken.nl
# November 5
from pathlib import Path
import csv

if __name__ == "__main__":
    """
    Get a csv input file (and print every row).
    Choose csv files saved in the same folder as loaddata.py.
    """
    course = 'vakken.csv'
    room = 'zalen.csv'
    individual = 'studentenenvakken.csv'
    mutual = 'tegelijkvolgbaar.csv'

    with open(course) as courses:
        courses = csv.reader(courses, delimiter=';')

        # Optional code to visualize data
        for row in courses:
            print(row)

    with open(room) as rooms:
        rooms = csv.reader(rooms, delimiter=';')

        # Optional code to visualize data
        for row in rooms:
            print(row)

    # Use encoding='iso-8859-1' to ensure that content is accessible as bytes
    with open(individual, encoding='iso-8859-1') as wishes:
        wishes = csv.reader(wishes, delimiter=';')

        # Optional code to visualize data
        for row in wishes:
            print(row)

    # Use encoding='iso-8859-1' to ensure that content is accessible as bytes
    with open(mutual) as mutual:
        mutual = csv.reader(mutual, delimiter=';')

        # Optional code to visualize data
        for row in mutual:
            print(row)
