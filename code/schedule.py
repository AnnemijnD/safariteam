
import random
from session import Session

SLOTS = 140
TIME_SLOTS = 4
DAYS = 5
ROOMS = 7


class Schedule():
    """
    Representation of a class (lecture, tutorial or practicum).
    """

    def __init__(self, name, class_id, type, mutual_courses):
        self.name = name
        self.class_id = class_id
        self.type = type
        self.mutual_courses = mutual_courses
        self.group = []
        self.schedule = [DAYS * [ROOMS * [TIME_SLOTS * ["None"]]]]

    def initialize_schedule(self, courses):
        """
        Initialize schedule using Session().
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
            # dag die is. Dus dat moeten we er ook aan mee gaan geven. MAar ik ben moe dus ga lekker stoppen.
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

        # Je geeft dus aan deze functie een leeg schedule mee en de sessions waarmee
        # schedule gevuld moet worden. Doordat lectures en other_sessions nu gescheieden
        # zijn kunnen eerst de lectures gevuld worden en daarna pas de rest
        Plan.fill_schedule(schedule, lectures, other_sessions, empty_sessions)

        return schedule, lectures, other_sessions, empty_sessions
