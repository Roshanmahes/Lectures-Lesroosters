from functions import *


# read data from files

# students.csv is in the following format:
# last name, first name, id, courses
student_list = read("data/students.csv")
# courses.csv is in the following format:
# name, lectures, seminars, seminar capacity, practicals, practical capacity
course_list = read("data/courses.csv")
# halls.csv is in the following format:
# name, capacity
hall_list = read("data/halls.csv", sort=True)


# create list of Course objects
courses = create_course_list(course_list, student_list)

# create list of Teaching objects
teachings = create_teachings(courses)

schedule = create_schedule(teachings, hall_list)

print_schedule(hall_list, schedule)
