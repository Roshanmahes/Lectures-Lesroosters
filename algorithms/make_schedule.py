from helpers import classes, functions
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
    schedule = [[None]*TIMESLOTS for _ in range(len(halls))]

    # keep track of how many timeslots have been filled for each hall
    tracker = [0] * len(halls)

    # fill schedule with teachings
    for teaching in teachings:
        greedy_fill(schedule, teaching, halls, tracker)

    return schedule

def random_sample(courses, halls):
    """
    Creates a schedule, filling all halls with teachings randomly.
    Returns a list of lists containing Teaching objects.
    """
    teachings = random_fill_teachings(courses)

    # create an empty schedule of the right dimensions
    schedule = [[None]*TIMESLOTS for _ in range(len(halls))]
    entries = list(range(TIMESLOTS * len(halls)))

    # randomly fill schedule with teachings
    for teaching in teachings:
        # random position in schedule
        rand = entries[random.randint(0, len(entries) - 1)]

        teaching.hall = halls[rand // TIMESLOTS]
        schedule[rand // TIMESLOTS][rand % TIMESLOTS] = teaching
        entries.remove(rand)

    return schedule

def random_fit(courses, halls):
    """
    Creates a schedule, filling all halls with teachings randomly,
    provided that the hall is available and large enough.
    Returns a list of lists containing Teaching objects.
    """
    teachings = random_fill_teachings(courses)

    # create an empty schedule of the right dimensions
    schedule = [[None]*TIMESLOTS for _ in range(len(halls))]

    # keep track of how many timeslots have been filled for each hall
    tracker = [0] * len(halls)

    # create random ordering of numbers
    teaching_index_list = random.sample(list(range(len(teachings))),
        len(teachings))

    # fill schedule with teachings
    for index in teaching_index_list:
        teaching = teachings[index]

        greedy_fill(schedule, teaching, halls, tracker)

    return schedule

def random_fill_teachings(courses):
    """
    Iterate over courses and make a list of teachings such that all seminar
    and practical groups are filled with students randomly.
    Returns a list of teachings.
    """
    teachings = []

    for course in courses:
        for _ in range(course.lectures):
            # assign students to lecture
            teachings.append(classes.Teaching("lecture",
                    course, course.students))

        if course.seminars:
            # randomly fill seminars with students
            seminars = functions.fill_teaching_groups(course, "seminar")

            for seminar in seminars:
                teachings.append(seminar)

        if course.practicals:
            # randomly fill seminars with students
            practicals = functions.fill_teaching_groups(course, "practical")

            for practical in practicals:
                teachings.append(practical)

    return teachings

def greedy_fill(schedule, teaching, halls, tracker):
    """
    Fill the schedule with the teacings so that no teaching is put into a hall
    with a capacity smaller than the amount of students in the teaching.
    """
    for i,hall in enumerate(halls):
        # if the amount of students fits into the hall
        if len(teaching.students) <= hall.capacity:

            # if less than all slots have been filled
            if tracker[i] < TIMESLOTS:

                # insert the teaching into the schedule
                schedule[i][tracker[i]] = teaching

                # add hall to teaching object
                teaching.hall = halls[i]
                tracker[i] += 1
                break
