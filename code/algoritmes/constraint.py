import loaddata
import numpy as np
import math
import switch


SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SPREAD_BONUS = 20
SESSION_LEN = 72
SESSION_NUM = 129
SLOTS_PER_DAY = 28
from random import randint


class Constraint():
    """
    A class with all the constraint functions.
    """

# Hier even een lijst met alle constraints:
# 1. hoorcelleges voor werkcolleges en practica HARD
# 2. er mag geen overlap zijn (met college zelf) HARD
# 3. er mag geen overlap zijn (met andere vakkken) HARD
# 4. studenten moeten in de zalen passen (NOG NIET)
# 5. colleges van hetzelfde vak moeten goed verspreid zijn over de week
#
# Een fix_hard_constraints functie maken voor als na het soft maken van een
# aantal constraints er niet meer wordt voldaan aan de hard constraints.

    def __init__(self):
        self.bonus_malus = []
        self.capacity = []


    def all_constraints(schedule, courses):
        """
        Makes a list that contains lists of every course with the moment and
        type of the courses in the schedule. The courses are in the list in
        order of their course_id.
        -----
        """

        courses_schedule = []
        for course in courses:
            course_schedule = {"day": [], "slot": [], "room": [], "type": [],
                               "session_id": [], "group_id": [], "overall_id": []}
            for i in range(DAYS):
                for j in range(TIME_SLOTS):
                    for k in range(ROOMS):
                        if schedule[i][j][k] is not None:
                            if course.name == schedule[i][j][k].name:
                                course_schedule["day"].append(i)
                                course_schedule["slot"].append(j)
                                course_schedule["room"].append(k)
                                course_schedule["type"].append(schedule[i][j][k].type)
                                course_schedule["session_id"].append(schedule[i][j][k].session_id)
                                course_schedule["group_id"].append(schedule[i][j][k].group_id)
                                course_schedule["overall_id"].append(schedule[i][j][k].overall_id)

            courses_schedule.append(course_schedule)

        return courses_schedule

    def all_constraints_linear(schedule, courses):
        """
        Similar as all_constraints but then as a linear list instead of
        a matrix.


        HUH DIT IS BIJNA dezelfde functie als die hierboven,
        kan het niet gewoon bij elkaar gedaan worden en dat de input veranderd?
        """
        courses_schedule = []
        for course in courses:
            course_schedule = {"day": [], "slot": [], "room": [], "type": [],
                               "session_id": [], "group_id": [], "overall_id": []}
            for i in range(SLOTS):
                if schedule[i] is not None:
                    if course.name == schedule[i].name:
                        course_schedule["day"].append(math.floor(i / SLOTS_PER_DAY))
                        course_schedule["slot"].append(math.floor(i / ROOMS) % TIME_SLOTS)
                        course_schedule["room"].append(i % ROOMS)
                        course_schedule["type"].append(schedule[i].type)
                        course_schedule["session_id"].append(schedule[i].session_id)
                        course_schedule["group_id"].append(schedule[i].group_id)
                        course_schedule["overall_id"].append(schedule[i].overall_id)

            courses_schedule.append(course_schedule)

        return courses_schedule

    def session_spread_check(schedule, courses, courses_schedule):
        """
        Calculates the amount of bonuspoints earned by correctly spreading the
        courses over the week. Where a course with 2 sessions should be on
        either monday and thursday or tuesday and friday. See the rest of the
        constrains in the comments bellow.
        A course can maximally get 20 points, this amount is spreaded over the
        number of groups a course has.

        Maximum amount of bonuspoints is 440
        Maximum amount of maluspoints is 430

        Returns a list of malus and bonuspoints per course as well.
        """
        # courses_schedule = Constraint.all_constraints(schedule, courses)
        bonuspoints = 0
        maluspoints = 0
        course_dict = {}

        # list with course id, bonus points and malus points
        course_bonus_malus = []

        for course in courses:
            id = course.course_id
            course_mal_points = 0
            course_bon_points = 0
            lectures = []
            sessions = []

            # gets indices of lectures in courses_schedule
            for i in range(len(courses_schedule[id]["type"])):
                if courses_schedule[id]["type"][i] == "lecture":
                    lectures.append(i)

            # checks if a course has groups
            # print(courses_schedule[id]["group_id"], course.name)
            groups = max(courses_schedule[id]["group_id"])
            if groups > 0:

                # saves indices of groups in courses_schedule together with lectures
                for i in range(groups):
                    same_group = [j for j, e in enumerate(courses_schedule[id]["group_id"]) if e == i + 1]
                    sessions.append(lectures + same_group)
            else:
                sessions = [lectures]

            # calculates the spread_bonus per group
            spread_bonus = SPREAD_BONUS / len(sessions)

            if course.sessions == 2:

                #  loops over the amount of groups
                for i in range(len(sessions)):

                    # print(courses_schedule[id]["day"], course.name)
                    # print(i)
                    # print(sessions[i])

                    # checks if the courses are on monday and thursday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 3):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus


                    # checks if the courses are on tuesday an friday
                    elif (courses_schedule[id]["day"][sessions[i][0]] == 1) and \
                         (courses_schedule[id]["day"][sessions[i][1]] == 4):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus

            elif course.sessions == 3:

                for i in range(len(sessions)):

                    # checks if the courses are on monday, wednesday and friday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 2) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 4):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus

            elif course.sessions == 4:

                for i in range(len(sessions)):

                    # checks if the courses are on monday, tuesday, thursday and friday
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 1) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 3) and \
                       (courses_schedule[id]["day"][sessions[i][3]] == 4):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus

            elif course.sessions == 5:

                for i in range(len(sessions)):

                    # checks if the courses are spread out on the whole week (every day)
                    if (courses_schedule[id]["day"][sessions[i][0]] == 0) and \
                       (courses_schedule[id]["day"][sessions[i][1]] == 1) and \
                       (courses_schedule[id]["day"][sessions[i][2]] == 2) and \
                       (courses_schedule[id]["day"][sessions[i][3]] == 3) and \
                       (courses_schedule[id]["day"][sessions[i][4]] == 4):
                        bonuspoints += spread_bonus
                        course_bon_points += spread_bonus

            #  check the overall spread per group
            for i in range(len(sessions)):
                days = []

                # adds the days sessions are given to list days
                for j in range(len(sessions[i])):
                    days.append(courses_schedule[id]["day"][sessions[i][j]])

                # if the sessions aren't spread enough increase maluspoints
                if len(days) - len(set(days)) > 0:
                    malusfactor = (course.sessions - len(days) - len(set(days)))
                    maluspoints += (malusfactor * 10) / len(sessions)
                    course_mal_points += (malusfactor * 10) / len(sessions)


            # course_bonus_malus.append([id, round(course_mal_points - course_bon_points)])
            course_dict.update({id: (round(course_mal_points - course_bon_points))})

        bonuspoints = round(bonuspoints)
        maluspoints = round(maluspoints)
        # print(course_bonus_malus)
        # print(f"bonuspoints: {bonuspoints}")
        # print(f"maluspoints: {maluspoints}")
        spread_points = maluspoints + bonuspoints
        Constraint.bonus_malus = course_bonus_malus

        # we moeten ook maluspoints returnen maar ik weet nog even niet waar
        # deze functie overal wordt aangeroepen dus daar wacht ik nog even mee

        # zelfde geldt voor de bonus_malus_points
        return [spread_points, course_dict, bonuspoints, maluspoints]

    def lecture_first(schedule, courses, courses_schedule):
        """
        Returns true if the lectures are before the tutorials and or
        practicals, otherwise returns false.
        """
        lecture_points = 0
        # courses_schedule = Constraint.all_constraints(schedule, courses)

        for course in courses:
            # checks for the number of lectures if the lectures are planned first
            for i in range(course.lecture):
                if courses_schedule[course.course_id]["type"][i] != "lecture":
                    lecture_points += 1

        return lecture_points

    def mutual_courses_check(schedule, courses):
        """
        Checks if same courses and  mutual courses aren't scheduled in the
        same timeslot. Iterates over every course in the schedule.
        Input is a schedule, output is the number of minus points calculated
        by the number of conflicting courses.
        """

        minus_points = 0

        # Check every slot in the schedule
        for i in range(DAYS):
            for j in range(TIME_SLOTS):
                for k in range(ROOMS):
                    # Check if this slot is filled (= check if not None)
                    if schedule[i][j][k].course_object:
                        # Check if session in this slot is a lecture
                        if schedule[i][j][k].type == "lecture":
                            # Each slot has a course name and the courses' mutual courses
                            # Mutual courses is a list of courses that can't be in the same timeslot
                            mutual_courses = schedule[i][j][k].course_object.mutual_courses
                            # For every mutual course in the mutual_courses list,
                            # check if it is placed in the same timeslot.
                            for mutual_course in range(len(mutual_courses)):    # DIT MOET ANDERS, DIT KAN IN MINDER LOOPS??!!
                                                                                # Je kan toch zeggen: if 'name' in [name1, name2, name3 ...]???
                                for z in range(len(schedule[i][j])):
                                    # If this mutual course is placed in the same timeslot
                                    # (for example Bioinformatica and Compilerbouw),
                                    # count one minus point.
                                    if mutual_courses[mutual_course] in schedule[i][j][z].name:
                                        minus_points += 1
                            # Also, if this course has a session of its own in
                            # this timeslot (for example: Bioinformatica and Bioinformatica)
                            # count one minus point.
                            own_session_counter = 0
                            for z in range(len(schedule[i][j])):
                                if schedule[i][j][z].name == schedule[i][j][k].name:
                                    # Count how many own_sessions there are in this timeslot
                                    own_session_counter += 1
                                # If own_session_counter is greater than 1, there is
                                # a conflicting session placed in this timeslot.
                                if own_session_counter > 1:
                                    minus_points += 1


                        # else:
                        #     # Each slot has a course name and the courses' mutual courses
                        #     # Mutual courses is a list of courses that can't be in the same timeslot
                        #     mutual_courses = schedule[i][j][k].course_object.mutual_courses
                        #     # For every mutual course in the mutual_courses list,
                        #     # check if it is placed in the same timeslot.
                        #     for mutual_course in range(len(mutual_courses)):
                        #         for z in range(len(schedule[i][j])):
                        #             # If this mutual course is placed in the same timeslot
                        #             # (for example Bioinformatica and Compilerbouw),
                        #             # count one minus point.
                        #             if mutual_courses[mutual_course] in schedule[i][j][z].name:
                        #                 minus_points += 1



                        # HIER MOET NOG EEN MALUS PUNT KOMEN VOOR ALS TUTORIAL GROEP A
                        # SAMEN MET PRACTICUM GROEP A ZIT!!!
                        # else:
                        #     # print(schedule[i][j][k])
                        #     for z in range(len(schedule[i][j])):
                        #         print(schedule[i][j][z])
                        #     print(" ______________")



        return minus_points

    def students_fit(schedule, courses, courses_schedule):
        """
        Returns the number of maluspoints that are given for the number of
        students that don't fit in the room of the session
        max aantal malus punten voor deze functie = 1332
        """
        # courses_schedule = Constraint.all_constraints(schedule, courses)
        rooms = loaddata.load_rooms()

        maluspoints = 0
        session_capacity = [0] * SESSION_NUM
        for course in courses:

            #  saves the room and type of the checked_course sessions
            checked_course = courses_schedule[course.course_id]
            room_ids = checked_course["room"]
            types = checked_course["type"]
            session_overall_ids = checked_course["overall_id"]


            for i in range(len(session_capacity)):

                # saves the max amount of students for the session type
                if types[i] is "lecture":
                    students = course.max_students_lecture
                elif types[i] is "tutorial":
                    students = course.max_students_tutorial
                else:
                    students = course.max_students_practical

                # calculates how many empty seats there are
                empty_seats = rooms[room_ids[i]].capacity - students

                # increases maluspoints with the nmbr of students that don't have a seat
                if empty_seats < 0:
                    maluspoints += abs(empty_seats)
                    # print(abs(empty_seats))
                    # # print(session_capacity[session_overall_ids[i]][0])
                    # print(session_capacity[session_overall_ids[i]])
                    # session_capacity[session_overall_ids[i]] = session_capacity[session_overall_ids[i]].append(5)
                    # print(session_capacity[session_overall_ids[i]])
                    # print(session_capacity[session_overall_ids[i]])
                    location = session_overall_ids[i]
                    session_capacity[location] += abs(empty_seats)


                if i == len(room_ids) - 1:
                    break



        # print(session_capacity)

        return maluspoints


    def switch_session(schedule, number_of_switches, session_to_switch, courses):
        """
        OJA NOOOOO, de Input van de Constraints functie is natuurlijk een 3D rooster aaah
        verdorie!!
        Dan moet het elke keer weer teruggezet worden naar 3D ?!?!?! STOM!!!! ANdere oplossing iemmand???
        """

        # Flatten schedule to get a 1D list to switch elements
        flatten = np.array(schedule).flatten()
        # print(flatten)

        # If there is no specific session to switch, make a random switch
        if session_to_switch < 0:

            for i in range(number_of_switches):
                # Get two random numbers
                random_number = randint(0, SLOTS - 1)
                random_switch_number = randint(0, SLOTS - 1)

                # If the numbers are equal to each other, make another number
                while random_number is random_switch_number:
                    random_number = randint(0, SLOTS - 1)
                    random_switch_number = randint(0, SLOTS - 1)
                # Make the switch
                flatten[random_number], flatten[random_switch_number] = flatten[random_switch_number], flatten[random_number]

        # If a specific session (with most maluspoints) has to be switched:
        else:
            # print(session_to_switch, "Dit is de overall_id van de sessie die geswitcht moet worden lololol!")
            # print(Constraint.overall_id_points(schedule, courses, session_to_switch), "Dit is het aantal maluspunten van deze sessie aaah super hoog man!!")

            # Sorrrry voor degene die deze code leest dit is echt meeeega slordig maar even haastig aahh
            # Zat in de trein dus ja je moet wat he!!!!!!! :-)

            # Iterate over every session in the schedule to get the session location
            for location in range(len(flatten)):
                # print(flatten[location].overall_id)

                # If location of the session was found:
                if flatten[location].overall_id == session_to_switch:
                    # print(location, "YES!!!!!! DIt is de locatie waar deze sessie staat in het rooster")
                    # Deze locatie moet dus 140 keer geswitcht worden en dan weer berekend wat het aantal
                    # maluspunten zou zijn om de beste locatie te kiezen.
                    # Sla deze locatie op
                    locatie = location
            # Nou super leuk hoor dan hebben we de locatie en deze moeten we gaan switchen whoee

            # Maark switch niet in het echte rooster, switch in een kopie omdat het
            # hypothetische switches zijn weetjewel ja weet niet hoe ik het anders moet zeggen
            # maar jullie snappen het wel xxoxoxox
            flattencopy = flatten
            location_points = {}

            # 140 keer switchen en punten berekenen jeeeetje dat zijn zoveel iteraties godsammie
            for i in range(SLOTS - 1):
                # PSEUDO
                # Zorg ervoor dat de switch met eigen locatie wordt overgeslagen
                if i != location:

                    # WOOOW DIT STEEDS OMZETTEN VAN NP ARRAY NAAR 3D IS ECHT SUUUPER ONHANDIG
                    # MOET ECHT ANDERS maar heb er nu echt even geen tijd voor sorry!! :((

                    # Maak een switch
                    # print(flattencopy[locatie])
                    flattencopy[i], flattencopy[locatie] = flattencopy[locatie], flattencopy[i]
                    flattencopy = flattencopy.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()
                    # print(Constraint.overall_id_points(flattencopy, courses, session_to_switch), "Dit zou het aantal maluspunten worden...!")
                    location_points[i] = Constraint.get_points(flattencopy, courses)
                    flattencopy = np.array(schedule).flatten()
                    # Switch terug
                    flattencopy[locatie], flattencopy[i] = flattencopy[i], flattencopy[locatie]
            # Dit is een dictionary met alle mogelijke plaatsen (dus van 0 tot 138 als het goed is)
            # en het aantal punten die de sessie zou krijgen als hij hier ingezet wordt.
            best_location = list(location_points.keys())[list(location_points.values()).index(max(location_points.values()))]
            # print(best_location, "Dit is de meest gunstige locatie voor deze session :)")
            # OKE beste locatie gevonden dus switch nu met deze locatie.
            flatten[locatie], flatten[best_location] = flatten[best_location], flatten[locatie]

        # Convert back to 3D list
        schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

        # Return 3D matrix of schedule
        return schedule


    def overall_id_points(schedule, courses, overall_id):
        """
        Gets maluspoints for a specific session.
        """

        id = Constraint.session_points(schedule,courses)[1]
        return id[overall_id]


    def session_points(schedule, courses):
        """
        Calculates maluspoints for each session, using session_spread_check and
        student_fit check. Output is a the overall_id of a session with highest
        maluspoints.
        """
        courses_schedule = Constraint.all_constraints(schedule, courses)
        rooms = loaddata.load_rooms()

        spread_points = Constraint.session_spread_check(schedule, courses, courses_schedule)[1]
        # print(spread_points)

        points_dict = {}
        # Loop over alle sessions om elke sessie een punt te geven jeej
        for i in range(DAYS):
            for j in range(TIME_SLOTS):
                for k in range(ROOMS):
                    # Even lekker de overall_id er uit halen want hierbij moet dus opgeteld worden he ja
                    # Ben zo blij dat course_object bestaat wWOOOW echt meeeega handig
                    # Dit is om te checken of de session niet leeg is.
                    if schedule[i][j][k].course_object:
                        # print(schedule[i][j][k].course_object.course_id, "  ", schedule[i][j][k].course_object.name)
                        # Dus voor elke overall_id moeten punten gegeven worden:
                        # Nou dat gaan we eens even lekker doen
                        # Deze moeten uit de points_dict gehaald worden,
                        # daarin staan alle spread puntjes per vak. :-)
                        temp_id = schedule[i][j][k].course_object.course_id
                        # Selecteer het vak uit de dictionary en geef de session de punten.
                        points_dict[schedule[i][j][k].overall_id] = spread_points[temp_id]
        # print(points_dict)

        session_points_dict = [{"session_id_ov": 0, "capacity_points":0, "spread_malus_points": 0,
                                "spread_bonus_points": 0, "flex_points": 0, "points": 0} for i in range(SESSION_NUM)]

        maluspoints = 0
        counter = 0
        points = 0
        for course in courses:
            #  saves the room and type of the checked_course sessions
            checked_course = courses_schedule[course.course_id]
            room_ids = checked_course["room"]
            types = checked_course["type"]
            session_overall_ids = checked_course["overall_id"]

            for i in range(len(room_ids)):

                # saves the max amount of students for the session type
                if types[i] is "lecture":
                    students = course.max_students_lecture
                elif types[i] is "tutorial":
                    students = course.max_students_tutorial
                else:
                    students = course.max_students_practical

                # calculates how many empty seats there are
                empty_seats = rooms[room_ids[i]].capacity - students

                # increases maluspoints with the number of students that don't have a seat
                if empty_seats < 0:
                    maluspoints += abs(empty_seats)
                    points = abs(empty_seats)

                    # print(session_overall_ids[i])
                    # print(abs(empty_seats))
                    # print(session_points_dict[session_overall_ids[i]])
                    session_points_dict[session_overall_ids[i]]["capacity_points"] += abs(empty_seats)

                # Tel de maluspunten op
                points_dict[counter] += points
                # Set points back to 0
                counter += 1
                points = 0

        # print(points_dict)
        # Hieruit kunnen we de overall_id halen van de sessie met het meeste maluspunten
        try:
            malus_session_id = list(points_dict.keys())[list(points_dict.values()).index(max(points_dict.values()))]
        # If there are no malus points (for capacity_points)
        except ValueError:
            print(points_dict)
            malus_session_id = randint(0, SLOTS - 1)

        return [malus_session_id, points_dict]

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

        BEREKENING NOG NIET AF:
        ALLE FUNCTIES 0 TOT 100 PUNTEN GEVEN
        Alles delen door max aantal punten en vermenigvuldigen met 100,
        hard constraints dan ook vermenigvuldigen met 2.
        """
        course_schedule = Constraint.all_constraints(schedule, courses)

        points = Constraint.session_spread_check(schedule, courses, course_schedule)[0] - \
                (Constraint.lecture_first(schedule, courses, course_schedule) * 40) - \
                (Constraint.mutual_courses_check(schedule, courses) * 40) - \
                (Constraint.students_fit(schedule, courses, course_schedule) / 4)

        return points
