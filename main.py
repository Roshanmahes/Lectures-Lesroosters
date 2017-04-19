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
hall_list = read("data/halls.csv", sort=True)


schedule = [[None for i in range(TIMESLOTS)] for j in range(len(hall_list))]
courses = [Course(data, []) for data in course_list]

# assign students to corresponding Course objects
for student_data in student_list:
    for course_name in student_data[DATA_OFFSET:]:
        for course in courses:
            if course_name == course.name:
                course.students.append(student_data)
                break

# create list of Teaching objects
teachings = create_teachings(courses)

tracker = [0]*len(hall_list)
for teaching in teachings:
    for i,hall in enumerate(hall_list):
        if len(teaching.students) <= hall[1]:
            if tracker[i] < TIMESLOTS:
                schedule[i][tracker[i]] = teaching
                tracker[i] += 1
                break

for row in schedule:
    print(row)
