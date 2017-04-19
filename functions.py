from operator import itemgetter
from tabulate import tabulate
from csv import *
from classes import *

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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
                teachings.append(Teaching("seminar", course, group, alphabet[i]))

        if course.practicals:
            # assign students to practical groups (in alphabetical order)
            for i in range(course.get_group_count("practical")):
                group = course.students[i*course.p_cap:(i+1)*course.p_cap]
                teachings.append(Teaching("practical", course, group, alphabet[i]))

    return teachings

def print_schedule(hall_list, schedule):
    headers = [hall[0] for hall in hall_list]
    schedule_transposed = []
    for t in zip(*schedule):
        schedule_transposed.append(list(t))
    print(tabulate(schedule_transposed, headers))
