from course import Course
from session import Session
from schedule import Schedule
from pathlib import Path
import os
import csv


class Plan():
    """
    Main scripts to make a schedule.
    """

    def __init__(self):
        pass

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
                lecture = row[1]
                tutorial = row[2]
                max_students = row[3]
                practical = row[4]
                course_id = id_counter

                # Use Course class to create objects for every course
                course = Course(name, course_id, lecture, tutorial, practical, max_students)
                courses_list.append(course)
                # Count id_course
                id_counter += 1

                # For example: if you want to know the number of lectures of a specific course:
                # print(course.lecture)

            return courses_list

    def load_sessions():
        """
        Loads all the session types for every course. Used by Schedule().

        # Pseudocode to create all the sessions:
        #
        # For every course:
        #   For every session type (lectures, tutorials, practicals)
        #       Make a Session(). input of Session = (self, name, class_id, type, mutual_courses, group):
        #
        # VOLGENS MIJ MOET MUTUAL_COURSES AL BIJ LOAD_COURSES IN DE COURSE GEZET WORDEN!
        # Geen idee hoe we group moeten definiëren...
        """

        sessions = []

        for course in Plan.load_courses():
            name = course.name
            class_id = course.course_id
            mutual_courses = []
            group = []

            # Make session for each lecture, tutorial and practical.
            for row in range(0, int(course.lecture)):
                type = 'lecture'
                session = Session(name, class_id, type, mutual_courses, group)
                sessions.append(session)

            for row in range(0, int(course.tutorial)):
                type = 'tutorial'
                session = Session(name, class_id, type, mutual_courses, group)
                sessions.append(session)

            for row in range(0, int(course.practical)):
                type = 'practical'
                session = Session(name, class_id, type, mutual_courses, group)
                sessions.append(session)

        # Nu zijn er bijvoorbeeld voor het vak 'Architectuur en computerorganisatie'
        # twee sessions aangemaakt met hoorcolleges; controleer met print-statement
        # Kan weggehaald worden als jullie het snappen :)
        # print(sessions[3].name)
        # print(sessions[4].name)

        # Succesfully created 72 sessions!
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

    def schedule():
        """
        Initialize schedule using Schedule().
        """

        schedules = 140 * [None]

        # Put every session into schedule
        for i in range(0 , len(Plan.load_sessions())):
            name = Plan.load_sessions()[i].name
            type = Plan.load_sessions()[i].type
            room = ''
            timeslot = ''
            day = ''
            schedule = Schedule(name, type, room, timeslot, day)
            schedules[i] = schedule

        # Quinten vindt dit vast ook niet leuk, moeten we even inladen eigenlijk?
        timeslots = 35 * ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
        days = [1,2,3,4,5]

        # Get lenght of the sessions-list to determine for-loop range.
        session_count = len(Plan.load_sessions())
        # in range 0 until 72 in steps of 7 (7 rooms)
        # Helemaal incorrect maar werkt misschien even voor nu
        for i in range(0, session_count, 7):
            schedules[i].timeslot = timeslots[i]

        # Fill the days
        # Sorry, dit is HEEL ERG GEHARDCODE, dus even een heel tijdelijke oplossing..
        for j in range(0,28):
            schedules[j].day = 'Monday'
        for j in range(28,56):
            schedules[j].day = 'Tuesday'
        for j in range(56,session_count):
            schedules[j].day = 'Tuesday'


        # Fill the rooms, should be built as a seperate function
        # iterate over 11 * list of rooms
        rooms = 11 * Plan.load_rooms()
        # In range of (0, len(sessions))
        for i in range(0, session_count):
            schedules[i].room = rooms[i]

        # write the CSV file to disk
        with open('data/schedule.csv', 'w', newline='') as output_file:
            Plan.save_csv(output_file, schedules)

        return schedules


    def get_days():
        """
        Returns a schedule of a specific day.
        """
        pass

        # #  bedenken op welke manier we dag willen 'aanroepen' (maandag 0 en vrijdag 4?)
        # def schedule_day(self, day):
        #     classes = []
        #     for i in range(TIMESLOTS, DAYS):
        #         classes.append(slots[])


        # Voor maandag zijn er maximaal 28 sessions (timeslots * zalen)
        monday = Plan.schedule()[0:(4 * 7)]
        # Print alle courses op maandag
        day = []
        for object in monday:
            print(object)


    def save_csv(outfile, schedules):
        """
        Print into csv-file to visualize schedule.
        """
        writer = csv.writer(outfile)
        writer.writerow(['Course', 'Type', 'Room', 'Timeslot', 'Day'])
        # Check if a row in schedules is filled with a session
        for row in schedules:
            if row == None:
                writer.writerow(5 * ['TODO'])
            else:
                writer.writerow([row.session, row.type, row.room, row.timeslot, row.day])


if __name__ == "__main__":

    # Load all the courses and sessions
    Plan.load_courses()
    Plan.load_sessions()
    Plan.schedule()
    Plan.load_rooms()
