# Heuristieken 2018 -- Lesroosters
# Namen: Annemijn, Sanne & Rebecca

from course import Course
from schedule import Schedule
import csv
import random
import time

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
MAX_MALUSPOINTS = 0


class Plan():
    """
    Main scripts to make a schedule.
    """

    def load_courses():
        """
        Loads all the courses from a csv file.
        """
        course = '../data/vakken.csv'

        with open(course) as courses:
            courses = csv.reader(courses, delimiter=';')
            # Skip file header
            next(courses)

            # Keep track of course_id with a counter
            id_counter = 0
            # Make a list of all the course objects
            courses_list = []

            # Define every item of the course; each row is a different course
            for row in courses:
                name = row[0]
                lecture = int(row[1])
                tutorial = int(row[2])
                max_students = row[3]
                practical = int(row[4])
                course_id = id_counter

                # Use Course class to create objects for every course
                course = Course(name, course_id, lecture, tutorial, practical, max_students)
                courses_list.append(course)
                # Count id_course
                id_counter += 1

            return courses_list

    def load_rooms():
        """
        loads all the rooms from a csv file.
        """
        room = '../data/zalen.csv'

        with open(room) as rooms:
            rooms = csv.reader(rooms, delimiter=';')
            next(rooms)

            roomnumbers = []

            # Optional code to visualize data
            for row in rooms:
                roomnumbers.append(row[0])

        return roomnumbers

    def schedule(courses):
        """
        Initialize schedule using Schedule().
        """

        schedule = SLOTS * [None]
        sessions = []
        session_list = []

        for course in courses:
            session_list = session_list + course.sessions_total

        # Put every session into schedule
        for i in range(SLOTS):
            try:
                name = session_list[i].name
            except:  # Blijkbaar mag een except niet 'leeg' zijn, dus nog even aanpassen
                name = '-'
            try:
                type = session_list[i].type
            except:
                type = '-'

                # Room, timeslot en day zijn nog niet bepaald, daar moeten dus
            # Even functies voor bedenken.
            room = 'None'
            timeslot = 'None'
            day = 'None'

            session = Schedule(name, type, room, timeslot, day)
            # Hier moet code tussen om te bepalen op welke plek in schedule
            # de session geplaatst moet worden..

            #  if schedule.name in schedules.name:
            #    select all the schedule uit schedules and put them in similar = []
            #    select the day of similar[-1] and insert schedule.name one day after the
            #    day of similar[-1]

            # Put session into schedule
            sessions.append(session)
            schedule[i] = session

        Plan.random_schedule(schedule, sessions)

        # Heb een random rooster gemaakt whoeehw :-) xxx Rebecca. Groetjes uit Zweden.
        # Misschien dat we dit kunnen gebruiken in het genetic algorithm:
        # Steeds random rooster genereren en dan constraints evalueren (met aparte functie?)

        #  -------------- DIT IS VOOR HOE HET ERUIT GAAT ZIEN ---------------------------
        # Quinten vindt dit vast ook niet leuk :(, moeten we even inladen eigenlijk?
        timeslots = DAYS * ROOMS * ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']

        # For-loop om elke timeslot 7 keer in het rooster te printen (7 zalen)
        counter = 0
        for timeslot in timeslots:
            # Stop counter als SLOTS is bereikt.
            if counter == SLOTS:
                break
            for i in range(7):
                try:
                    schedule[counter].timeslot = timeslot
                    counter += 1
                except:
                    counter += 1

        # Wat hier boven staat iets minder gehardcode, nu tot session_count omdat
        #  ik niet weet hoe het bestand er precies uitziet maar moet uiteindelijk tot SLOTS.
        for j in range(SLOTS):
            if j < TIME_SLOTS * DAYS:
                schedule[j].day = 'Monday'
            elif j < TIME_SLOTS * DAYS * 2:
                schedule[j].day = 'Tuesday'
            elif j < TIME_SLOTS * DAYS * 3:
                schedule[j].day = 'Wednesday'
            elif j < TIME_SLOTS * DAYS * 4:
                schedule[j].day = 'Thursday'
            else:
                schedule[j].day = 'Friday'

        # Fill the rooms, (moet eigenlijk een aparte functie worden)
        # iterate over 20 * list of rooms
        rooms = DAYS * TIME_SLOTS * Plan.load_rooms()
        # In range of (0, len(sessions))
        for i in range(0, SLOTS):
            schedule[i].room = rooms[i]

        Plan.calc_malus(schedule, sessions)

        # Write the CSV file to data-folder
        with open('../data/schedule.csv', 'w', newline='') as output_file:
            Plan.save_csv(output_file, schedule)

        return schedule

    def random_schedule(schedule, sessions):
        """
        Generates a random schedule. Assigns every session to a random timeslot.

        # Hou bij welke random nummers al geweest zijn. De while loop
        # Zorgt ervoor dat er een random nummer wordt gemaakt die nog
        # niet is geweest.
        """

        random_numbers = []
        for i in range(SLOTS):
            rand = random.randint(0, SLOTS - 1)
            while rand in random_numbers:
                rand = random.randint(0, SLOTS - 1)
            schedule[rand] = sessions[i]
            random_numbers.append(rand)

        Plan.schedule_counter += 1


    def calc_malus(schedule, sessions):
        """
        Calcalates malus point (only for mutual courses).
        If number of maluspoints is higher that a given maximum, make a new schedule.
        """

        # Sla de lege sessions over
        counter = 0
        keep_track_of_courses = []
        for row in schedule:
            if row.session is not '-':
                keep_track_of_courses.append([row.session, row.timeslot, row.day])
        for row in schedule:
            if row.session is not '-':
                current = [row.session, row.timeslot, row.day]
                for i in keep_track_of_courses:
                    if len(set(i) & set(current)) == 3:
                        # Counter is in dit geval het aantal rijen die
                        # elkaar overlappen, dus vakken die in hetzelfde
                        # tijdslot en dag voorkomen.
                        counter += 1

        # Het aantal sessions (dus len(keep_track_of_courses)) moet er af gehaald
        # worden, aangezien er sowieso 72 dingen zijn die met elkaar overlappen.
        malus_points = counter - len(keep_track_of_courses)

        if malus_points > MAX_MALUSPOINTS:
            courses = Plan.load_courses()
            Plan.schedule(courses)


    def get_day(day):
        """
        Returns a schedule of a specific day.
        """

        # KIEZEN OF WE DE NAAM VAN DE DAG OF HET NUMMER VAN DE DAG WILLEN
        #  als we nummer doen hoeft de hele if niet meer (maar dan wel een
        # slimme implementatie bedenken voor hoe we nummer doen)
        if day == "Monday":
            i = 0
        elif day == "Tuesday":
            i = 1
        elif day == "Wednesday":
            i = 2
        elif day == "Thursday":
            i = 3
        else:
            i = 4
        return Plan.schedule()[(TIME_SLOTS * ROOMS * i):(TIME_SLOTS * ROOMS * (i + 1))]

        #
        # # Voor maandag zijn er maximaal 28 sessions (timeslots * zalen)
        # monday = Plan.schedule()[0:(SLOTS * ROOMS)]
        # # Print alle courses op maandag
        # day = []
        # for object in monday:
        #     print(object)

    def get_slot(slot, day):
        """
        Returns the schedule of a specific slot on a specific day.
        """

        # NET ALS BIJ DAYS BEDENKEN OF WE HET VIA NAAM OF NUMMER WILLEN DOEN
        #  als we met nummer doen hoeven we de hele if niet meer te doen
        if slot == "9:00 - 11:00":
            i = 0
        elif slot == "11:00 - 13:00":
            i = 1
        elif slot == "13:00 - 15:00":
            i = 2
        else:
            i = 3
        return Plan.get_day(day)[(ROOMS * i):(ROOMS * (i + 1))]

    def load_individual():
        """
        Loads individual student courses.
        """
        # Use encoding='iso-8859-1' to ensure that content is accessible as bytes
        with open('data/studentenenvakken.csv', encoding='iso-8859-1') as wishes:
            wishes = csv.reader(wishes, delimiter=';')

            # Optional code to visualize data
            for row in wishes:
                print(row)

    def save_csv(outfile, schedules):
        """
        Print into csv-file to visualize schedule.
        """
        writer = csv.writer(outfile)
        writer.writerow(['Course', 'Type', 'Room', 'Timeslot', 'Day'])
        # Check if a row in schedules is filled with a session
        for row in schedules:
            if row is None:
                writer.writerow(5 * ['TODO'])
            else:
                writer.writerow([row.session, row.type, row.room, row.timeslot, row.day])


if __name__ == "__main__":

    Plan.schedule_counter = 0
    then = time.time()

    # Load all the courses and sessions
    courses = Plan.load_courses()
    Plan.schedule(courses)
    Plan.load_rooms()

    now = time.time() # Time after it finished

    print("It took: ", now - then, " seconds")
    print("Script made", Plan.schedule_counter, "schedules.")
