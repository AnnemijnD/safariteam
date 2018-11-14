# Heuristieken 2018 -- Lesroosters
# Namen: Annemijn, Sanne & Rebecca

from course import Course
from session import Session
from schedule import Schedule
import csv
import random
import time
import pandas as pd
from IPython.display import HTML

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
MAX_MALUSPOINTS = 0

class Plan():
    """
    Main scripts to make a schedule.
    """

    def __init__(self):
        pass

    def load_courses(self):
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

    def load_rooms(self):
        """
        loads all the rooms from a csv file.
        """
        room = '../data/zalen.csv'

        with open(room) as rooms:
            rooms = csv.reader(rooms, delimiter=';')
            next(rooms)

            roomnumbers = []

            for row in rooms:
                roomnumbers.append(row[0])

        return roomnumbers

    def initialize_schedule(self, courses):
        """
        Initialize schedule using Schedule().
        """

        sessions = []
        session_list = []
        lecture_sessions = []
        other_sessions = []
        empty_sessions = []

        for course in courses:
            session_list = session_list + course.sessions_total

        # Put every session into schedule
        for i in range(SLOTS):
            try:
                name = session_list[i].name
            except IndexError:
                name = '-'
            try:
                type = session_list[i].type
            except IndexError:
                type = '-'
            room = 'Empty room'
            timeslot = 'Empty timeslot'
            day = 'Empty day'

            session = Session(name, type, room, timeslot, day)
            # PROBLEEM: als we een sessie in het rooster zetten, weet de sessie niet op welke
            # dag die is. Dus dat moeten we er ook aan mee gaan geven. MAar ik ben moe dus ga lekker stoppenself.
            # we hebben het er morgen over KUSJES
            # for k in range(len(schedule)):
            #     if schedule[k] is None:
            #         break
            #     elif session.session in schedule[k].session:
            #         similar = []
            #         for j in range(k + 1):
            #             print("test")
            #             if session.session == schedule[j].session:
            #                 similar.append(schedule[j])
            #         print(similar[-1].day)
            #         day = similar[-1].day + 1

            # Get all the lectures
            if session.type == "lecture":
                lecture_sessions.append(session)
            else:
                other_sessions.append(session)
            sessions.append(session)

        # shuffle de lectures zodat ze random zijn
        lectures = lecture_sessions[:]
        random.shuffle(lectures)


        # Maak lege sessies aan om lege cellen mee op te vullen
        # Dit stukje wordt gebruikt in de nested for loop waarbij aan elke cel
        # een sessie wordt meegegeven.
        for i in range(SLOTS):
            name = '-'
            type = '-'
            room = 'None'
            timeslot = 'None'
            day = 'None'
            session = Session(name, type, room, timeslot, day)
            empty_sessions.append(session)


        # Lijst in een lijst in een lijst
        schedule = DAYS * [TIME_SLOTS * [ROOMS * ['None']]]
        # Probleem: omdat je in schedule2 een keer-teken gebruikt, wordt alles vermenigvuldigt..
        # We moeten een kopie maken van schedule2 en daarin dingen veranderen??
        # Tijdelijke oplossing:
        schedule = [[['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']], [['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']], [['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']], [['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']], [['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']]]

        return schedule, lectures, other_sessions, empty_sessions


    def fill_schedule(self, schedule, lectures, other_sessions, empty_sessions):
        """
        Fill empty schedule with sessions. Function will begin to fill all the lectures
        and will go on to fill other sessions.
        """

        # Gebruik nested for loop om elke cel een session te gegen.
        # Je geeft hierbij een lijst met sessies mee aan de functie get_session
        # De lijst met sessies is al gemaakt in schedule() (misschien deze functie een andere naam geven trouwens)
        counter = 0
        for b in range(DAYS):
            for c in range(TIME_SLOTS):
                for d in range(ROOMS):
                    try:
                        # van lecture_sesssions zijn er maar 39, de overige plekken
                        # schedule moeten ook nog gevuld worden, dus zet er dan een empty
                        # session neer.
                        # print(lectures[counter].session)
                        schedule[b][c][d] = lectures[counter]
                    # Overige lege plekken moeten ook gevuld worden met lege sessions
                    except IndexError:
                        # print(empty_sessions[counter])
                        schedule[b][c][d] = empty_sessions[counter]
                    counter += 1

        # PSEUDOCODE om elke lecture in te roosteren en te letten op overlap met vakken.
        # _______________________________________________________________________________
        # WHILE niet ingeroosterd, itereer over elke cel, check of hij leeg is, zo niet, rooster in. Zo wel, ga naar volgende cel.
        #
        # Voor elk hoorcollege (dus voor elk item in lecture_sessions):
        # Itereer over elke cel (dus schedule2[b][c][d])
        # for b in range(DAYS):
        #     for c in range(TIME_SLOTS):
        #         for d in range(ROOMS):
        #             schedule2[b][c][d]
        #             # check of de cel leeg is:
        #              if schedule2[b][c][d] == 'None':
        #                   # check of er al een hoorcollege van dat vak is ingeroosterd in deze timeslot
        #                   if item in schedule2[b][c]:
        #                   # zo ja, check of je naar de volgende cel kan gaan (dus volgende timeslot)
        #                       # if c += 1 is mogelijk (try):
        #                       doe dan c += 1
        #                       if c += 1 niet mogelijk:
        #                       ga dan naar de volgende dag en doe de check opnieuw,
        #                           d += 1
        #                           dus misschien een while loop maken:
        #
        #

        # Steeds random rooster genereren en dan constraints evalueren
        # plan.random_schedule(schedule, sessions)
        # schedule = plan.fill_rooms_and_days(schedule2)

        return schedule

    def random_schedule(self, schedule, sessions):
        """
        Generates a random schedule. Assigns every session to a random timeslot.

        # Hou bij welke random nummers al geweest zijn. De while loop
        # Zorgt ervoor dat er een random nummer wordt gemaakt die nog
        # niet is geweest.
        """

        for i in range(SLOTS):
            rand = random.randint(0, SLOTS - 1)
            while rand in random_numbers:
                rand = random.randint(0, SLOTS - 1)
            # Hier wordt de session in dat timeslot gezet met een random nummer
            schedule[rand] = sessions[i]
            plan.random_numbers.append(rand)

        # Keep track of how many schedules were made
        plan.schedule_counter += 1

    def get_session(self, sessions):
        """
        Generates a random schedule. Assigns every session to a random timeslot.

        # Hou bij welke random nummers al geweest zijn. De while loop
        # Zorgt ervoor dat er een random nummer wordt gemaakt die nog
        # niet is geweest.
        """

        for i in range(len(sessions)):
            rand = random.randint(0, (len(sessions)) - 1)
            while rand in plan.random_numbers:
                rand = random.randint(0, len(sessions) - 1)
                plan.random_numbers.append(rand)

        return sessions[rand]

    def calc_malus(self, schedule):
        """
        Calcalates malus point (only for mutual courses).
        If number of maluspoints is higher that a given maximum, make a new schedule.
        """
        # Dit was Sannes pseudocode:
        #  if schedule.name in schedules.name:
        #    select all the schedule uit schedules and put them in similar = []
        #    select the day of similar[-1] and insert schedule.name one day after the
        #    day of similar[-1]

        counter = 0
        keep_track_of_courses = []
        for row in schedule:
            # Controleer niet op lege sessions, dus sla deze over
            if row.session is not '-':
                keep_track_of_courses.append([row.session, row.timeslot, row.day])
        for row in schedule:
            if row.session is not '-':
                current_row = [row.session, row.timeslot, row.day]
                for course in keep_track_of_courses:
                    # Intersection gebruiken?
                    # Als len == 3 dan overlapt de hele rij
                    if len(set(course) & set(current_row)) == 3:
                        # Counter is in dit geval het aantal rijen die
                        # elkaar overlappen, dus vakken die in hetzelfde
                        # tijdslot en dag voorkomen.
                        counter += 1
        # Het aantal sessions (dus len(keep_track_of_courses)) moet er af gehaald
        # worden, aangezien er sowieso 72 dingen zijn die met elkaar overlappen.
        malus_points = counter - len(keep_track_of_courses)

        # _________ NOG NIET AF ___________
        # Test voor hoorcolleges voor werkcolleges en practica
        # lectures = []
        # counter = 0
        # for row in schedule:
        #     if row.session is not '-' or row.type is not '-':
        #         current_row = [row.session, row.type]
        #         if row.type == 'lecture':
        #             lectures.append(row.session)
        #         # Geef maluspunt als er van dit vak nog geen hoorcollege is gegeven
        #         if row.session not in lectures:
        #             counter += 1
        # # Haal er voor nu een aantal maluspunten vanaf want anders kost
        # # vet veel tijd om een rooser te maken
        # lecture_points = counter - 10
        lecture_points = 0

        if malus_points > MAX_MALUSPOINTS or lecture_points > MAX_MALUSPOINTS:
            # DIT MOET ANDERS. Nu laden we de hele tijd opnieuw
            # ALLE rooms in. HeeeeEEUeel onnodig. Iemand ideeën? xxx R
            plan.schedule(plan.courses)

        return schedule


    def get_slot(self, slot, day):
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
        return plan.get_day(day)[(ROOMS * i):(ROOMS * (i + 1))]

    def load_individual(self):
        """
        Loads individual student courses.
        """
        # Use encoding='iso-8859-1' to ensure that content is accessible as bytes
        with open('data/studentenenvakken.csv', encoding='iso-8859-1') as wishes:
            wishes = csv.reader(wishes, delimiter=';')

            # Optional code to visualize data
            for row in wishes:
                print(row)

    def save_html(self, schedule):
        """
        Print into csv-file to visualize schedule.
        """
        df = pd.DataFrame(schedule)
        df.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
        df.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # Transpose rows and columns
        df = df.T

        df_html = df.to_html('../data/schedule.html')
        HTML(df_html)


    # def fill_rooms_and_days(self, schedule):
    #
    #     #  -------------- DIT IS VOOR HOE HET ERUIT GAAT ZIEN ---------------------------
    #     # Quinten vindt dit vast ook niet leuk :(, moeten we even inladen eigenlijk?
    #     timeslots = ROOMS * DAYS * ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
    #     # Dit moet anders want nu worden rooms steeds opnieuw ingeladen
    #     rooms = DAYS * TIME_SLOTS * plan.load_rooms()
    #     days = ROOMS * TIME_SLOTS * ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    #
    #     # Fill all the days
    #     for c in range(ROOMS):
    #         for d in range(TIME_SLOTS):
    #             schedule[0][c][d].day = 'Monday'
    #             schedule[1][c][d].day = 'Tuesday'
    #             schedule[2][c][d].day = 'Wednesday'
    #             schedule[3][c][d].day = 'Thursday'
    #             schedule[4][c][d].day = 'Friday'
    #
    #     # Fill all the rooms
    #     counter = 0
    #     for a in range(DAYS):
    #         for b in range(ROOMS):
    #             for c in range(TIME_SLOTS):
    #                 schedule[a][b][c].room = rooms[counter % 7]
    #             counter += 1
    #
    #     # Fill all the timeslots
    #     counter = 0
    #     for a in range(DAYS):
    #         for b in range(ROOMS):
    #             for c in range(TIME_SLOTS):
    #                 schedule[a][b][c].timeslot = timeslots[counter]
    #                 counter += 1
    #     #
    #     # for b in range(DAYS):
    #     #     for c in range(ROOMS):
    #     #         for d in range(TIME_SLOTS):
    #     #             print(schedule[b][c][d])
    #
    #     return schedule


if __name__ == "__main__":

    then = time.time()

    # Load all the courses and sessions
    plan = Plan()
    plan.random_numbers = []
    plan.schedule_counter = 0
    plan.courses = plan.load_courses()
    schedule, lectures, other_sessions, empty_sessions = plan.initialize_schedule(plan.courses)
    schedule = plan.fill_schedule(schedule, lectures, other_sessions, empty_sessions)
    plan.load_rooms()

    # Make a html file for the schedule
    plan.save_html(schedule)

    now = time.time()

    print("It took:", now - then, "seconds")
    print("Script made", plan.schedule_counter, "schedules until the right was found.")
