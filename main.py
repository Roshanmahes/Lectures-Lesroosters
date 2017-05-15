import classes
import algorithms.algorithms as algorithms
import algorithms.greedy as greedy
import csv

from algorithms.hill_climb import *
from algorithms.simulated_annealing import *
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

    # run some algorithms here
    schedule = algorithms.alphabetical(courses, halls)
    print_schedule(schedule, halls)
    print("Old score:", score(schedule, courses))

    new_schedule = simulated_annealing(schedule, courses, halls, max_iter=1000, student_prob=0.5)
    print_schedule(new_schedule, halls)
    print("New score:", score(new_schedule, courses))

if __name__ == "__main__":
    main()
