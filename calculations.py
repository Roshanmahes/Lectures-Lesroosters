from math import factorial
from functools import reduce
import operator
import csv


# http://stackoverflow.com/a/4941932
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(operator.mul, range(n, n-r, -1))
    denom = reduce(operator.mul, range(1, r+1))
    return numer//denom


# read csv files and store in lists
students = []
courses = []
halls = []
with open('data/studentenenvakken.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    students = list(reader)
with open('data/vakken.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    courses = list(reader)
with open('data/zalen.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    halls = list(reader)


# change strings of integers to actual integers
for course in courses[1:]:
    course[1:] = list(map(int, course[1:]))
for hall in halls[1:]:
    hall[1:2] = list(map(int, hall[1:2]))


# generate a list of the number of students enrolled in each course
course_enrollments = []
for course in courses[1:]:
    course_enrollments.append([course[0],0])
for student in students[1:]:
    for enrolled_course in student[3:]:
        for course in courses[1:]:
            if enrolled_course == course[0]:
                course_enrollments[courses.index(course) - 1][1] += 1
students_per_course = []
for L in course_enrollments:
    students_per_course.append(L[1])


# generate a list of the amount of seminar and practical groups necessary per course
SPGroups = []
for course,student_count in zip(courses[1:],students_per_course):
    if course[2] == 0 and course[4] == 0:
        SPGroups.append(0)
    else:
        if course[2] != 0:
            capacity = course[3]
        else:
            capacity = course[5]
        if student_count % capacity > 0:
            SPGroups.append(student_count//capacity + 1)
        else:
            SPGroups.append(student_count//capacity)


# generate a list of sizes of all teachings (lecture, seminar and practical)
# makes use of the fact that any course with both seminar and practical teachings
# will have equal capacities for both types
teachings = []
for i in range(len(courses)-1):
    for _ in range(courses[i+1][1]):
        teachings.append(students_per_course[i])
    for _ in range(SPGroups[i]*(courses[i+1][2]+courses[i+1][4])):
        if course[2] != 0:
            teachings.append(course[3])
        else:
            teachings.append(course[5])
teachings.sort(reverse=True)


# upper bound to number of ways the lectures can be scheduled
prod1 = 1
prod1str = ''
big_enough_halls = 0
tracker = 0
for teaching in teachings:
    for hall in halls[1:]:
        if teaching < hall[1]:
            big_enough_halls += 1
    prod1str += str(big_enough_halls * 20 - tracker) + ' * '
    prod1 *= big_enough_halls * 20 - tracker
    tracker += 1
    big_enough_halls = 0


# upper bound to number of ways the students can be put into the S and P groups
prod2 = 1
prod2str = ''
for i in range(len(courses)-1):
    course = courses[i+1]
    group_count = SPGroups[i]
    student_count = students_per_course[i]
    seminars = course[2]
    practicals = course[4]
    if seminars > 0:
        capacity = course[3]
    else:
        capacity = course[5]
    if group_count > 0:
        prod2str += str((ncr(2 * student_count - 1 - group_count * capacity, group_count - 1))**(seminars+practicals))
        if i != len(courses)-2:
            prod2str += ' * '
        prod2 *= (ncr(2 * student_count - 1 - group_count * capacity, group_count - 1))**(seminars+practicals)


prodstr = prod1str + prod2str
prod = prod1*prod2


# Print results
print('Students per course')
for enrollment in course_enrollments:
    print(enrollment[0]+(' '*(38-len(enrollment[0]+str(enrollment[1]))))+str(enrollment[1]))
print()
print()
print('Upper bound to configurations of the state space')
#print(prodstr)
#print(prod)
print('{:.2E}'.format(prod))
