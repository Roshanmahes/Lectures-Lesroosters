from csv import *
from classes import *


def read(path):
    """
    Reads csv file from path and returns a list, stripping the first row
    if it contains no digits (if it is a header).
    """
    with open(path, "r", encoding="utf-8") as f:
        result = list(reader(f))

    # strip the first row if it is a header
    if not any(cell.isdigit() for cell in result[0]):
        result = result[1:]

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
                teachings.append(Teaching("seminar", course, group))

        if course.practicals:
            # assign students to practical groups (in alphabetical order)
            for i in range(course.get_group_count("practical")):
                group = course.students[i*course.p_cap:(i+1)*course.p_cap]
                teachings.append(Teaching("practical", course, group))

    return teachings
