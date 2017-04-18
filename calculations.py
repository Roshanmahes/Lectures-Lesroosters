from math import factorial
from functools import reduce
import operator
import csv
from functions import read


# http://stackoverflow.com/a/4941932
# currently unused
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(operator.mul, range(n, n-r, -1))
    denom = reduce(operator.mul, range(1, r+1))
    return numer//denom


# number of ways to divide n identical items over g distinct groups under capacity c
# https://math.stackexchange.com/a/941916
# http://stackoverflow.com/a/5413198
# currently unused
def groupings(n, g, c):
    factor = [1]*(c+1)
    li = factor
    for _ in range(g - 1):
        res = [0]*(len(li)+c)
        for pos,val in enumerate(li):
            for i in range(len(factor)):
                res[pos+i] += val
        li = res
    return li[n]

if __name__ == "__main__":
    # read csv files and store in lists
    students = read("data/students.csv")
    courses = read("data/courses.csv")
    halls = read("data/halls.csv")


    # change strings of integers to actual integers
    for course in courses:
        course[1:] = list(map(int, course[1:]))
    for hall in halls:
        hall[1:] = list(map(int, hall[1:]))


    # generate a list of the number of students enrolled in each course
    course_enrollments = []
    for course in courses:
        course_enrollments.append([course[0],0])
    for student in students:
        for enrolled_course in student[3:]:
            for i,course in enumerate(courses):
                if enrolled_course == course[0]:
                    course_enrollments[i][1] += 1
    students_per_course = []
    for L in course_enrollments:
        students_per_course.append(L[1])


    # generate a list of the amount of seminar and practical groups necessary per course
    SPGroups = []
    for course,student_count in zip(courses,students_per_course):
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
    for i,course in enumerate(courses):
        for _ in range(course[1]):
            teachings.append(students_per_course[i])
        for _ in range(SPGroups[i]*(course[2]+course[4])):
            if course[2] != 0:
                teachings.append(course[3])
            else:
                teachings.append(course[5])
    teachings.sort(reverse=True)


    # upper bound to number of ways the teachings can be scheduled
    prod1 = 1
    tracker = 0
    for teaching in teachings:
        big_enough_halls = 0
        for hall in halls:
            if teaching < hall[1]:
                big_enough_halls += 1
        prod1 *= big_enough_halls * 20 - tracker
        tracker += 1


    # upper bound to number of ways the students can be put into the S and P groups
    prod2 = 1
    for i,course in enumerate(courses):
        group_count = SPGroups[i]
        if group_count > 0:
            student_count = students_per_course[i]
            seminars = course[2]
            practicals = course[4]
            if seminars > 0:
                capacity = course[3]
            else:
                capacity = course[5]
            prod2 *= int((group_count**student_count)**(seminars+practicals))

    prod = prod1*prod2


    # Print results
    print("Course"+" "*32+"Students")
    for enrollment in course_enrollments:
        print(enrollment[0]," "*(44-len(enrollment[0]+str(enrollment[1]))),enrollment[1])
    print()
    print()
    print("Upper bound to configurations of the state space")
    s = str(prod)
    print(s[0] + "." + s[1:3] + "e" + str(len(s)-1))