import classes
import csv
import random

from operator import itemgetter

from reportlab.lib.colors import HexColor as Color
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIMESTRINGS = ["9-11", "11-13", "13-15", "15-17"]
PERIODS = len(TIMESTRINGS)
TIMESLOTS = len(WEEKDAYS)*PERIODS

# globals for save_schedule
PADDING, TEACHING_SIZE = 4, 3.2

# default tablestyle
PRIMARY, ACCENT, BORDER =  Color(0xD0D0D0), Color(0x818181), Color(0x7D7D7D)
STYLE = [('BACKGROUND',(0,0),(-1,-1),ACCENT), ('TEXTCOLOR',(0,0),(0,-1),PRIMARY),
('BACKGROUND',(1,1),(-1,-1),PRIMARY), ('TEXTCOLOR',(0,0),(-1,0),PRIMARY),
('LINEABOVE',(0,0),(-1,0),2,PRIMARY), ('LINEBELOW',(0,0),(-1,0),2,PRIMARY),
('LINEBEFORE',(0,0),(0,-1),2,PRIMARY), ('LINEAFTER',(0,0),(0,-1),2.3,PRIMARY),
('LINEAFTER',(-1,0),(-1,-1),2,BORDER), ('LINEBELOW',(0,-1),(-1,-1),2,BORDER)]

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

def fill_teaching_groups(course, _type):
    """
    Randomly fills all teachings of a course of a certain type with students,
    returning a list of filled teachings.
    """
    group_count = course.get_group_count(_type)
    students_per_group = [0] * group_count

    if _type == "seminar":
        capacity = course.s_cap
    else:
        capacity = course.p_cap

    # initialise list of teaching groups
    groups = [classes.Teaching(_type, course, [], ALPHABET[i]) \
            for i in range(group_count)]

    # insert each student into a random teaching group
    # provided that the group is not full yet
    for student in course.students:
        rand = random.randint(0, group_count - 1)

        while students_per_group[rand] == capacity:
            rand = random.randint(0, group_count - 1)
        groups[rand].students.append(student)
        students_per_group[rand] += 1

    return groups

def flatten_schedule(schedule, new_teachings=False):
    """
    Flatten schedule in such a way that the teachings are sorted by timeslot.
    Schedule is a list of lists, where each list contains teachings
    scheduled at a certain hall. Returns flattened schedule.
    """
    schedule_flat = []
    for timeslot in zip(*schedule):
        for teaching in timeslot:

            if new_teachings:
                # create new Teaching object for teaching
                # if there exists a teaching at that timeslot
                if teaching:
                    schedule_flat.append(classes.Teaching(teaching))
                else:
                    schedule_flat.append(None)
            else:
                schedule_flat.append(teaching)

    return schedule_flat

def inflate_schedule_flat(schedule_flat):
    """
    Takes a flattened schedule and returns a schedule of proper dimensions.
    """
    hall_count = len(schedule_flat) // TIMESLOTS
    schedule = [[None]*TIMESLOTS for _ in range(hall_count)]

    # insert teachings into schedule at the correct position
    for i,teaching in enumerate(schedule_flat):
        schedule[i % hall_count][i // hall_count] = teaching

    return schedule

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
        # sort items by column sort_column
        for item in result:
            item[sort_column] = int(item[sort_column])
        result.sort(key=itemgetter(sort_column))

    return result

def save_schedule(my_schedule, halls, filename="schedule", height=8.7*inch):
    """
    Builds and saves a table (as filename.pdf in schedules folder)
    containing my_schedule with halls.
    """
    # initialise schedule's header with hall names
    schedule = [[str(hall.name) for hall in halls]]
    schedule[0].insert(0,"SCHEDULE")

    for i,column in enumerate(zip(*my_schedule)):
        # transpose a schedule column to be a row
        schedule_row = list(column)

        # insert weekday dividers
        if not i % PERIODS:
            day_row = [WEEKDAYS[i // PERIODS]]
            day_row.extend([None]*len(halls))
            schedule.append(day_row)

        # add the corresponding time to the row
        schedule_row.insert(0, TIMESTRINGS[i % PERIODS])
        schedule.append(schedule_row)

    schedule = Table(schedule)
    schedule.setStyle(TableStyle(STYLE))

    # build filename.pdf
    width = (PADDING + TEACHING_SIZE*len(halls)) * inch
    SimpleDocTemplate("schedules/" + str(filename) + ".pdf",
        pagesize=(width, height)).build([schedule])
