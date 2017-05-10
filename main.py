import classes
import algorithms.algorithms as algorithms
import algorithms.greedy as greedy
import algorithms.hill_climb as hill_climb
import csv
from functions import *
from score import *

def main():
    """
    Executes main.py.
    """

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

    students = [classes.Student(data) for data in student_list]
    halls = [classes.TeachingHall(data) for data in hall_list]

    # create list of Course objects
    courses = create_course_list(course_list, students)

    schedule = algorithms.random_fit(courses,halls)
    print("Old:", score(schedule, courses))
    schedule = hill_climb.student_swap(schedule,courses,halls)
    print("New:", score(schedule, courses))


if __name__ == "__main__":
    main()
