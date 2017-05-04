import classes
import random

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TIMESLOTS = 20

def alphabetical(courses, halls):
    """
    Creates a schedule, filling all halls with
    teachings in the alphabetical order given by the file of courses.
    Returns a list of lists containing Teaching objects.
    """
    # create a list of teachings to fill alphabetically
    teachings = []

    for course in courses:
        for _ in range(course.lectures):
            # assign students to lecture
            teachings.append(classes.Teaching("lecture",
                course, course.students))

        if course.seminars:
            # assign students to seminar groups (in alphabetical order)
            for i in range(course.get_group_count("seminar")):
                group = course.students[i * course.s_cap:(i+1) * course.s_cap]
                teachings.append(classes.Teaching("seminar",
                    course, group, ALPHABET[i]))

        if course.practicals:
            # assign students to practical groups (in alphabetical order)
            for i in range(course.get_group_count("practical")):
                group = course.students[i * course.p_cap:(i+1) * course.p_cap]
                teachings.append(classes.Teaching("practical",
                    course, group, ALPHABET[i]))

    # create an empty schedule of the right dimensions
    schedule = [[None for i in range(TIMESLOTS)] for j in range(len(halls))]

    # keep track of how many timeslots have been filled for each hall
    tracker = [0] * len(halls)

    for teaching in teachings:
        for i,hall in enumerate(halls):

            # if the amount of students fits into the hall
            if len(teaching.students) <= hall.capacity:

                # if less than all slots have been filled
                if tracker[i] < TIMESLOTS:

                    # insert the teaching into the schedule
                    schedule[i][tracker[i]] = teaching

                    # add hall and timeslot to teaching object
                    teaching.hall = halls[i]
                    teaching.timeslot = tracker[i]
                    tracker[i] += 1
                    break

    return schedule

def random_walk(courses, halls):
    """

    """
    teachings = []

    for course in courses:
        for _ in range(course.lectures):
            # assign students to lecture
            teachings.append(classes.Teaching("lecture",
                    course, course.students))

        if course.seminars:
            group_count = course.get_group_count("seminar")
            students_per_group = [0] * group_count

            seminars = [classes.Teaching("seminar", course, [], ALPHABET[i]) for i in range(group_count)]

            for student in course.students:
                rand = random.randint(0, group_count - 1)
                while students_per_group[rand] == course.s_cap:
                    rand = random.randint(0, group_count - 1)
                seminars[rand].students.append(student)
                students_per_group[rand] += 1

            for seminar in seminars:
                teachings.append(seminar)

        if course.practicals:
            group_count = course.get_group_count("practical")
            students_per_group = [0] * group_count

            practicals = [classes.Teaching("practical", course, [], ALPHABET[i]) for i in range(group_count)]

            for student in course.students:
                rand = random.randint(0, group_count - 1)
                while students_per_group[rand] == course.p_cap:
                    rand = random.randint(0, group_count - 1)
                practicals[rand].students.append(student)
                students_per_group[rand] += 1

            for practical in practicals:
                teachings.append(practical)

    # create an empty schedule of the right dimensions
    schedule = [[None for i in range(TIMESLOTS)] for j in range(len(halls))]
    entries = list(range(TIMESLOTS * len(halls)))
    for teaching in teachings:
        rand = entries[random.randint(0, len(entries) - 1)]
        teaching.hall = halls[rand // 20]
        schedule[rand // 20][rand % 20] = teaching
        entries.remove(rand)

    return schedule
