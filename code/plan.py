# Heuristieken 2018 -- Lesroosters
# Namen: Annemijn, Sanne & Rebecca

from course import Course
from session import Session
from schedule import Schedule
import csv

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7


class Plan():
    """
    Main scripts to make a schedule.
    """

    def load_courses():
        """
        Loads all the courses. Used by Session().
        """
        course = 'data/vakken.csv'

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

                # For example: if you want to know the number of lectures of a specific course:
                # print(course.lecture)

            return courses_list

    # def load_sessions():
        """
        Loads all the session types for every course. Used by Schedule().

        # Pseudocode to create all the sessions:
        #
        # For every course:
        #   For every session type (lectures, tutorials, practicals)
        #       Make a Session(). input of Session = (self, name, class_id, type, mutual_courses, group):
        #
        # IK DENK DAT MUTUAL_COURSES AL BIJ LOAD_COURSES IN DE COURSE GEZET WORDEN!
        # Nog geen idee hoe we group moeten definiëren... <-- group hoeft nog niet :))) <<-- Oke thanks Sanne :)
        """

        # sessions = []

        # for course in Plan.load_courses():
            # name = course.name
            # class_id = course.course_id
            # mutual_courses = []
            # group = []
            #
            # # Make session for each lecture, tutorial and practical.
            # for row in range(int(course.lecture)):
            #     type = 'lecture'
            #     session = Session(name, class_id, type, mutual_courses, group)
            #     sessions.append(session)
            #
            # for row in range(int(course.tutorial)):
            #     type = 'tutorial'
            #     session = Session(name, class_id, type, mutual_courses, group)
            #     sessions.append(session)
            #
            # for row in range(int(course.practical)):
            #     type = 'practical'
            #     session = Session(name, class_id, type, mutual_courses, group)
            #     sessions.append(session)

        # Nu zijn er bijvoorbeeld voor het vak 'Algoritmen en Complexiteit'
        # twee sessions aangemaakt; controleer met print-statement
        # # Kan weggehaald worden als jullie het snappen :)
        # print(sessions[3].name)
        # print(sessions[4].name)
        #
        # # Succesfully created 72 sessions!
        # print(len(sessions))

        return sessions

    def load_rooms():
        """
        loads all the rooms.
        """
        room = 'data/zalen.csv'

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

        # Put every session into schedule
        #
        # for course in courses:
        #     for i in range(SLOTS):
        #         try:
        #             name = course.sessions_total[i].name
        #             print(name)
        #         except:  # Blijkbaar mag een except niet 'leeg' zijn, dus nog even aanpassen
        #             name = 'TODO'
        #         try:
        #             type = course.sessions_total[i].type
        #             print(type)
        #         except:
        #             type = 'TODO'
        session_list = []
        for course in courses:
            session_list = session_list + course.sessions_total

        for i in range(SLOTS):
            try:
                name = session_list[i].name
            except:  # Blijkbaar mag een except niet 'leeg' zijn, dus nog even aanpassen
                name = 'TODO'
            try:
                type = session_list[i].type
            except:
                type = 'TODO'
        #
        # for i in range(SLOTS):
        #     try:
        #         name = Plan.load_sessions()[i].name
        #     except:  # Blijkbaar mag een except niet 'leeg' zijn, dus nog even aanpassen
        #         name = 'TODO'
        #     try:
        #         type = Plan.load_sessions()[i].type
        #     except:
        #         type = 'TODO'
                # Room, timeslot en day zijn nog niet bepaald, daar moeten dus
            # Even functies voor bedenken.
            room = ''
            timeslot = ''
            day = ''

            session = Schedule(name, type, room, timeslot, day)
            # Hier moet code tussen om te bepalen op welke plek in schedule
            # de session geplaatst moet worden.

            # pseudo
            # If schedule.name == schedules[i].name and schedule.timeslot = schedules[i].timeslot (in range 0,7):
            #      skip this place, go to next timeslot.

            #  if schedule.name in schedules.name:
            #    select all the schedule uit schedules and put them in similar = []
            #    select the day of similar[-1] and insert schedule.name one day after the
            #    day of similar[-1]

            # Put session into schedule
            schedule[i] = session
            print(schedule[i].type)

        #  DIT IS VOOR HOE HET ERUIT GAAT ZIEN
        # Quinten vindt dit vast ook niet leuk, moeten we even inladen eigenlijk?
        timeslots = DAYS * ROOMS * ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']

        # Sorry dit is echt super onduidelijk en ik snap het zelf eigenlijk ook niet!!!!
        # MAAR HET WERKT!
        counter = 0
        for timeslot in timeslots:
            # Zonder de - 2 komt de error: 'out of range',
            # want dan begint er weer een nieuwe lijst van 7 zalen...
            if counter == SLOTS:
                break
            for i in range(7):
                schedule[counter].timeslot = timeslot
                counter += 1

        # for i in range(0, session_count, ROOMS):
        #     schedule[i].timeslot = timeslots[i]

        # Fill the days
        # Sorry, dit is HEEL ERG GEHARDCODE, dus even een heel tijdelijke oplossing..
        # for j in range(0,28):
        #     schedules[j].day = 'Monday'
        # for j in range(28,56):
        #     schedules[j].day = 'Tuesday'
        # for j in range(56,session_count):
        #     schedules[j].day = 'Wednesday'

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

        # write the CSV file to disk
        with open('data/schedule.csv', 'w', newline='') as output_file:
            Plan.save_csv(output_file, schedule)

        return schedule

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

    # Load all the courses and sessions
    courses = Plan.load_courses()
    Plan.schedule(courses)
    Plan.load_rooms()
