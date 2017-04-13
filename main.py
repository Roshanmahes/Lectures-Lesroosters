import csv
from classes import *

student_list = []
course_list = []
hall_list = []

with open('data/studentenenvakken.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    student_list = list(reader)
with open('data/vakken.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    course_list = list(reader)
with open('data/zalen.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    hall_list = list(reader)

student_list = student_list[1:]
course_list = course_list[1:]
hall_list = hall_list[1:]

schedule = [[0 for i in range(20)] for j in range(7)]


courses = []
for course_data in course_list:
    courses.append(Course(course_data, []))

for student in student_list:
    for courseName in student[3:]:
        for course in courses:
            if courseName == course.name:
                course.students.append(student)

teachings = []
for course in courses:
    for _ in range(course.lectures):
        teachings.append(Teaching("lecture", course, course.students))

    student_count = len(course.students)

    if course.seminars:
        capacity = course.s_cap
        if student_count % capacity > 0:
            seminar_count = student_count//capacity + 1
        else:
            seminar_count = student_count//capacity
        for i in range(seminar_count):
            group = course.students[i*capacity:(i+1)*capacity-1]
            teachings.append(Teaching("seminar", course, group))

    if course.practicals:
        capacity = course.p_cap
        if student_count % capacity > 0:
            practical_count = student_count//capacity + 1
        else:
            practical_count = student_count//capacity
        for i in range(practical_count):
            group = course.students[i*capacity:(i+1)*capacity]
            teachings.append(Teaching("practical", course, group))

print(teachings[2].type)
print(len(teachings[1].students))
