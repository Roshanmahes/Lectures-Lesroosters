from operator import itemgetter
from tabulate import tabulate
from csv import *
from classes import *

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIMESTRINGS = ["9-11", "11-13", "13-15", "15-17"]

def read(path, sort=False, sort_column=1):
    """
    Reads csv file from path and returns a list, stripping the first row
    if it contains no digits (if it is a header).
    """
    with open(path, "r", encoding="utf-8") as f:
        result = list(reader(f))

    # strip the first row if it is a header
    if not any(item.isdigit() for item in result[0]):
        result = result[1:]

    if sort:
        for item in result:
            item[sort_column] = int(item[sort_column])
        result.sort(key=itemgetter(sort_column))

    return result

def create_teachings(courses):
    """
    Creates a list of teachings corresponding to
    the Course object list courses.
    """
    teachings = []

    for course in courses:
        for _ in range(course.lectures):
            # assign students to lecture
            teachings.append(Teaching("lecture", course, course.students))

        if course.seminars:
            # assign students to seminar groups (in alphabetical order)
            for i in range(course.get_group_count("seminar")):
                group = course.students[i*course.s_cap:(i+1)*course.s_cap]
                teachings.append(Teaching("seminar", course, group, ALPHABET[i]))

        if course.practicals:
            # assign students to practical groups (in alphabetical order)
            for i in range(course.get_group_count("practical")):
                group = course.students[i*course.p_cap:(i+1)*course.p_cap]
                teachings.append(Teaching("practical", course, group, ALPHABET[i]))

    return teachings

def print_schedule(hall_list, schedule):
    headers = [hall[0] for hall in hall_list]
    headers.insert(0,"")
    printable_schedule = []
    for i,t in enumerate(zip(*schedule)):
        if not i % 4:
            day_row = [WEEKDAYS[i//4]]
            day_row.extend([None]*7)
            printable_schedule.append(day_row)
        schedule_row = list(t)
        schedule_row.insert(0, TIMESTRINGS[i % 4])
        printable_schedule.append(schedule_row)
    print(tabulate(printable_schedule, headers))
