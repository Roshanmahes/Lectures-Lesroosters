import csv
from classes import *
from functions import *

TIMESLOTS = 20
DATA_OFFSET = 3

# read data from files

# students.csv is in the format
# last name, first name, id, courses
student_list = read("data/students.csv")
# courses.csv is in the format
# name, lectures, seminars, seminar capacity, practicals, practical capacity
course_list = read("data/courses.csv")
# halls.csv is in the format
# name, capacity
hall_list = read("data/halls.csv")


schedule = [[None for i in range(TIMESLOTS)] for j in range(len(hall_list))]
courses = [Course(data) for data in course_list]

# assign students to corresponding Course objects
for student_data in student_list:
    for course_name in student_data[DATA_OFFSET:]:
        for course in courses:
            if course_name == course.name:
                course.students.append(student_data)
                break

# create list of Teaching objects
teachings = []
for course in courses:
    for _ in range(course.lectures):
        teachings.append(Teaching("lecture", course, course.students))

    student_count = len(course.students)

    if course.seminars:
        # maximum size of seminar group
        capacity = course.s_cap

        # determine number of seminar groups
        if student_count % capacity > 0:
            seminar_count = student_count//capacity + 1
        else:
            seminar_count = student_count//capacity

        # assign students to seminar groups (in alphabetical order)
        for i in range(seminar_count):
            group = course.students[i*capacity:(i+1)*capacity]
            teachings.append(Teaching("seminar", course, group))

    if course.practicals:
        # maximum size of practicals
        capacity = course.p_cap

        # determine number of practical groups
        if student_count % capacity > 0:
            practical_count = student_count//capacity + 1
        else:
            practical_count = student_count//capacity

        # assign students to practical groups (in alphabetical order)
        for i in range(practical_count):
            group = course.students[i*capacity:(i+1)*capacity]
            teachings.append(Teaching("practical", course, group))
