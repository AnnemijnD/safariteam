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
        Initialize schedule using Session().
        Willen we eigenlijk in Schedule class zelf hebben
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

            session = Session(name, type)
            # session = Session(name, type, room, timeslot, day)
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
            elif session.type == "tutorial" or session.type == "practical":
                other_sessions.append(session)
            sessions.append(session)


        # shuffle de lectures zodat ze random zijn
        # Make copy of sessions and shuffle
        lectures = lecture_sessions[:]
        others = other_sessions[:]
        random.shuffle(lectures)
        random.shuffle(other_sessions)

        # TODO: lijst maken met eerst grote vakken!!

        total = []
        total = lectures + other_sessions


        # Maak lege sessies aan om lege cellen mee op te vullen
        # Dit stukje wordt gebruikt in de nested for loop waarbij aan elke cel
        # een sessie wordt meegegeven.
        for i in range(SLOTS):
            name = '-'
            type = '-'
            room = 'None'
            timeslot = 'None'
            day = 'None'
            session = Session(name, type)
            # session = Session(name, type, room, timeslot, day)
            empty_sessions.append(session)


        # Lijst in een lijst in een lijst
        schedule = DAYS * [TIME_SLOTS * [ROOMS * ['None']]]
        # Probleem: omdat je in schedule2 een keer-teken gebruikt, wordt alles vermenigvuldigt..
        # We moeten een kopie maken van schedule2 en daarin dingen veranderen??
        # Tijdelijke oplossing:
        schedule = [[['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']], [['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']], [['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']], [['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']], [['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', 'None', 'None']]]

        # Je geeft dus aan deze functie een leeg schedule mee en de sessions waarmee
        # schedule gevuld moet worden. Doordat lectures en other_sessions nu gescheieden
        # zijn kunnen eerst de lectures gevuld worden en daarna pas de rest
        plan.fill_schedule(schedule, total, other_sessions, empty_sessions, courses)
        plan.schedule_counter += 1



        return schedule, total, other_sessions, empty_sessions


    def fill_schedule(self, schedule, lectures, other_sessions, empty_sessions, courses):
        """
        Fill empty schedule with sessions. Function will begin to fill all the lectures
        and will go on to fill other sessions.
        """

        # Gebruik nested for loop om elke cel een session te gegen.
        # Je geeft hierbij een lijst met sessies mee aan de functie get_session
        # De lijst met sessies is al gemaakt in initialize_schedule()


        # PSEUDOCODE om elke lecture in te roosteren en te letten op overlap met vakken.
        # _______________________________________________________________________________
        # Voor elk hoorcollege (dus voor elk item in lecture_sessions):
        # WHILE niet ingeroosterd, itereer over elke cel, check of hij leeg is, zo niet, rooster in. Zo wel, ga naar volgende cel.
        #
        # Itereer over elke cel (dus schedule2[b][c][d])
        # for days in range(DAYS):
        #     for timeslots in range(TIME_SLOTS):
        #         for rooms in range(ROOMS):
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

        # Vul eerst met lege sessions
        counter = 0
        for b in range(DAYS):
            for c in range(TIME_SLOTS):
                for d in range(ROOMS):
                    schedule[b][c][d] = empty_sessions[counter]

        # PROBLEEM: als er nu een tijdslot wordt gevonden waar dat vak
        # al in zit, itereert hij naar volgende tijdslot, maar er wordt niet
        # terug geïtereerd om een ander vak in dat lege tijdslot te zetten...
        # NOG EEN PROBLEEM: Niet alle lectures worden op deze manier ingeroosterd,
        # Sommige worden nu overgeslagen.
        # lecture_counter = 0
        # counter = 0
        # day_counter = 0
        # timeslot_counter = 0
        # break_counter = 0
        #
        # for i in range(DAYS):
        #     locations = []
        #     day_counter = 0
        #     for j in range(TIME_SLOTS):
        #         for k in range(ROOMS):
        #             for l in schedule[i][j]:
        #                 if lectures[lecture_counter].name in l.name:
        #                     day_counter += 1
        #                     if i == 4:
        #                         # loopende functie, help?!??1
        #                         plan.initialize_schedule(plan.courses)
        #                     break
        #                 else:
        #                     if schedule[i][j][k].name == '-':
        #                         locations.append([j,k])
        #                         # print(locations)
        #             if day_counter > 0:
        #                 break
        #         if day_counter > 0:
        #             break
        #
        #     timeslot = locations[0][0]
        #     room = locations[0][1]
        #     schedule[i][timeslot][room] = lectures[lecture_counter]
        #     lecture_counter += 1
        #
        #     # for j in range(TIME_SLOTS):
        #     #     for k in range(ROOMS):
        #     #         if schedule[i][j][k].name == '-':
        #     #             schedule[i][j][k] = lectures[lecture_counter]
        #     #             lecture_counter += 1
        #     #             i -= day_counter
        #     #             break
        #     #     if break_counter > 0:
        #     #         break
        #
        #     # time_slot = locations[0][0]
        #     # room = locations[0][1]
        #     # schedule[i][time_slot][room] = lectures[lecture_counter]
        #     # lecture_counter += 1
        #     # i -= day_counter
        #
        # return schedule


        # # Verdelen over slots als hard constraint
        # for e in range(len(lectures)):
        #     found = False
        #     for course in courses:
        #         if lectures[e].name == course.name:
        #            mutual_courses_session = course.mutual_courses
        #     for b in range(DAYS):
        #         for c in range(TIME_SLOTS):
        #             rooms_allowed = True
        #             # availibility = True
        #             location = []
        #             for d in range(ROOMS):
        #                 print(f'elke keer d:{b} {c} {d}')
        #                 # if the slot in the schedule is empty
        #                 if schedule[b][c][d].name == '-':
        #                     # print("in if1")
        #                     if not bool(location):
        #                         # print("in if1.1")
        #                         location.append(c)
        #                         location.append(d)
        #
        #
        #                 elif lectures[e].name == schedule[b][c][d].name or schedule[b][c][d].name in mutual_courses_session:
        #                     rooms_allowed = False
        #                     break
        #
        #
        #
        #
        #             if rooms_allowed and bool(location):
        #
        #                 print(f'gevonden:{b} {c} {d}')
        #                 # print("in if2")
        #                 schedule[b][location[0]][location[1]] = lectures[e]
        #                 # lecture_counter += 1
        #
        #                 # b -= day_counter
        #                 # d -= break_counter
        #                 # c -= timeslot_counter
        #                 # day_counter = 0
        #                 # break_counter = 0
        #                 # timeslot_counter = 0
        #                 found = True
        #
        #                 break
        #
        #             #
        #             # elif c == 3:
        #             #     # print("in elif2")
        #             #     # day_counter += 1
        #             #     break
        #
        #             # else:
        #             #     # print("in else2")
        #             #     # timeslot_counter += 1
        #
        #         if found:
        #             break
        #             # print("in if3")
        #             # if lecture_counter == len(lectures):
        #             #     # print("in if 4")
        #             #     return schedule
        #             # else:
        #             #     # print("in else4")
        #             #     plan.initialize_schedule(plan.courses)
        #
        #
        # if found:
        #     return schedule
        #
        # else:
        #     plan.initialize_schedule(plan.courses)
        #
        #
        #


        # verdelen over dagen als hard constraint
        for e in range(len(lectures)):

            for course in courses:
                if lectures[e].name == course.name:
                    mutual_courses_session = course.mutual_courses
            found = False
            for b in range(DAYS):
                location = []
                slots_allowed = True
                for c in range(TIME_SLOTS):
                    rooms_allowed = True
                    # availibility = True

                    for d in range(ROOMS):

                        # if the slot in the schedule is empty
                        if schedule[b][c][d].name == '-':
                            # print("in if1")
                            if not bool(location):
                                # print("in if1.1")
                                location.append(c)
                                location.append(d)

                        elif lectures[e].name == schedule[b][c][d].name:
                            slots_allowed = False
                            break

                        elif schedule[b][c][d].name in mutual_courses_session:
                            rooms_allowed = False
                            break

                    if not slots_allowed:
                        break

                    if rooms_allowed and bool(location):

                        schedule[b][location[0]][location[1]] = lectures[e]
                        found = True
                        break



                if slots_allowed and bool(location):

                        # print("in if2")
                    schedule[b][location[0]][location[1]] = lectures[e]
                    found = True
                    break


            if not found:
                print(e)
                print("not found")
                print(lectures[e])
                return schedule
                plan.schedule_counter += 1
                plan.initialize_schedule(plan.courses)

        if found:
            return schedule

        else:
            plan.schedule_counter += 1
            plan.initialize_schedule(plan.courses)



                            # makes a new schedule if it failed



                    # set the session in the schedule

                    # QUINTEN!: is dit sneller in een if statement?
                    # d += 1
                    # d %= 7
                    #
                    # #  returns to the previous timeslot/day in the loop if it skipped one
                    # if timeslot_counter > 0:
                    #     c -= timeslot_counter
                    #     timeslot_counter = 0
                    # if day_counter > 0:
                    #     b -= day_counter
                    #     day_counter = 0
                    #
                    # # if all the sessions are scheduled return schedule
                    # if lecture_counter is len(lectures):
                    #     return schedule
        # lecture_counter = 0
        # counter = 0
        # day_counter = 0
        # timeslot_counter = 0
        # for b in range(DAYS):
        #     for c in range(TIME_SLOTS):
        #         for d in range(ROOMS):
        #
        #             # if the slot in the schedule is empty
        #             if schedule[b][c][d].name == '-':
        #
        #                 #  loop through the rooms
        #                 for e in schedule[b][c]:
        #
        #                     # check if the same course is already in that slot
        #                     if lectures[lecture_counter].name in e.name:
        #                         print(lectures[lecture_counter].name in e.name)
        #                         c += 1
        #                         timeslot_counter += 1
        #                         if c > 3:
        #                             b += 1
        #                             day_counter += 1
        #                             c = 0
        #
        #                         # makes a new schedule if it failed
        #                         if b > 4:
        #                             plan.initialize_schedule(plan.courses)
        #
        #                 # set the session in the schedule
        #                 schedule[b][c][d] = lectures[lecture_counter]
        #                 lecture_counter += 1
        #                 # QUINTEN!: is dit sneller in een if statement?
        #                 d += 1
        #                 d %= 7
        #
        #                 #  returns to the previous timeslot/day in the loop if it skipped one
        #                 if timeslot_counter > 0:
        #                     c -= timeslot_counter
        #                     timeslot_counter = 0
        #                 if day_counter > 0:
        #                     b -= day_counter
        #                     day_counter = 0
        #
        #                 # if all the sessions are scheduled return schedule
        #                 if lecture_counter is len(lectures):
        #                     return schedule

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
            if row.name is not '-':
                keep_track_of_courses.append([row.name, row.timeslot, row.day])
        for row in schedule:
            if row.name is not '-':
                current_row = [row.name, row.timeslot, row.day]
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

    # WERKT NIET EN IS EIGENLIJK OOK NIET NODIG WANT RETURNED ALLEEN IETS, JOE
    # def get_day(schedule, day):
    #     """
    #     Returns the schedule of a specific day. Where the day is an integer
    #     between 0 and 4.
    #     """
    #     return schedule[day]
    #
    # def get_slot(slot, day):
    #     """
    #     Returns the schedule of a specific slot on a specific day.
    #     The slot will be an integer between 0 and 3 and the day an integer
    #     between 0 and 4.
    #     """
    #     return plan.get_day(day)[slot]

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

    def save_html(self, schedule, rooms):
        """
        Print into csv-file to visualize schedule.
        """

        df = pd.DataFrame(schedule)
        pd.set_option('display.max_colwidth',350)
        df.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
        df.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # Transpose rows and columns
        df = df.T

        # Als je het rooster van een specifieke dag wilt printen:
        i = 0
        print("Rooster van maandag per lokaal:")
        tags = df['Monday'].apply(pd.Series)
        # tags = tags.rename(columns = lambda x : 'Room ' + str(x))
        tags.columns = [rooms[i], rooms[i+1], rooms[i+2], rooms[i+3], rooms[i+4], rooms[i+5], rooms[i+6]]
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(tags)


        html_string = '''
        <html>
          <head><title>Schedule</title></head>
          <link rel="stylesheet" type="text/css" href="../data/style.css" href="https://www.w3schools.com/w3css/4/w3.css"/>
          <body>
            {table}
          </body>
        </html>.
        '''

        with open('../data/schedule.html', 'w') as f:
            f.write(html_string.format(table=df.to_html(classes='style')))

        # schedule = []
        # for a in range(TIME_SLOTS):
        #     for b in range(DAYS):
        #         schedule.append([plan.get_cel(df, a, b)])
        # print(schedule)
        #
        # with open('../data/test.csv', 'w') as csv_file:
        #     writer = csv.writer(csv_file, delimiter=' ')
        #     writer.writerow(["Test"])
        #     for i in range(len(schedule)):
        #         writer.writerow([schedule[i], schedule[i + 1]])


        # Even Quinten vragen welke van de twee beter is?
        # df_html = df.to_html('../data/schedule.html')
        # HTML(df_html)

    # def get_cel(self, df, row, column):
    #
    #     # Hahah lol dit is echt meeeegaaaaaa lelijk dus moet even in een for loop
    #
    #     a = row
    #     j = column
    #     i = 0
    #     cel = rooms[i] + ': ' + str(df.iat[a, j][i]) + '\n' \
    #     + rooms[i + 1] + ': ' + str(df.iat[a ,j][i + 1]) + '\n' \
    #     + rooms[i + 2] + ': ' + str(df.iat[a, j][i + 2]) + '\n' \
    #     + rooms[i + 3] + ': ' + str(df.iat[a, j][i + 3]) + '\n' \
    #     + rooms[i + 4] + ': ' + str(df.iat[a, j][i + 4]) + '\n' \
    #     + rooms[i + 5] + ': ' + str(df.iat[a, j][i + 5]) + '\n' \
    #     + rooms[i + 6] + ': ' + str(df.iat[a, j][i + 6])
    #
    #     return str(cel)


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

    rooms = plan.load_rooms()

    # Make a html file for the schedule
    plan.save_html(schedule, rooms)

    now = time.time()

    print("It took:", now - then, "seconds")
    print("Script made", plan.schedule_counter, "schedule(s) until the right was found.")
