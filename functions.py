import classes
import csv
from operator import itemgetter
from tabulate import tabulate

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIMESTRINGS = ["9-11", "11-13", "13-15", "15-17"]
PERIODS = len(TIMESTRINGS)
TIMESLOTS = 20
DATA_OFFSET = 3

def read(path, sort=False, sort_column=1):
    """
    Reads csv file from path and returns a list, stripping the first row
    if it contains no digits (if it is a header).
    """
    with open(path, "r", encoding="utf-8") as f:
        result = list(csv.reader(f))

    # strip the first row if it is a header
    if not any(item.isdigit() for item in result[0]):
        result = result[1:]

    if sort:
        for item in result:
            item[sort_column] = int(item[sort_column])
        result.sort(key=itemgetter(sort_column))

    return result


def create_course_list(course_list, students):
    """
    Returns a list of Course objects, each
    containing students following the course.
    """
    courses = [classes.Course(data, []) for data in course_list]

    # assign students to corresponding Course objects
    for student in students:
        for course_name in student.courses:
            for course in courses:
                if course_name == course.name:
                    course.students.append(student)
                    break

    return courses

def print_schedule(schedule, halls):
    """
    Prints a table containing a schedule with halls from halls.
    """
    # the headers of the table are the hall names
    headers = [hall.name for hall in halls]
    headers.insert(0,"")

    # initialise a list that will be in the format accepted by tabulate
    printable_schedule = []

    for i,t in enumerate(zip(*schedule)):
        # transpose a schedule column to be a row
        schedule_row = list(t)

        # insert weekday dividers
        if not i % PERIODS:
            day_row = [WEEKDAYS[i // PERIODS]]
            day_row.extend([None] * len(halls))
            printable_schedule.append(day_row)

        # add the corresponding time to the row
        schedule_row.insert(0, TIMESTRINGS[i % PERIODS])

        printable_schedule.append(schedule_row)

    print(tabulate(printable_schedule, headers))

def inflate_schedule_flat(schedule_flat):
    """
    Takes a flattened schedule and returns a schedule of proper dimensions.
    """
    hall_count = len(schedule_flat) // TIMESLOTS
    schedule = [[None]*TIMESLOTS for _ in range(hall_count)]

    for i,teaching in enumerate(schedule_flat):
        schedule[i % hall_count][i // hall_count] = teaching
    return schedule
