import csv
import classes
import functions
import algorithms.make_schedule as make_schedule
import algorithms.temperature as temperature
from score import score
from algorithms.hill_climb import hill_climb
from algorithms.simulated_annealing import simulated_annealing

def main():
    """
    Executes main.py.
    """
    # read data from files
    # students.csv is in the following format:
    # last name, first name, id, courses
    student_list = functions.read("data/students.csv")
    # courses.csv is in the following format:
    # name, lectures, seminars, seminar capacity, practicals, practical capacity
    course_list = functions.read("data/courses.csv")
    # halls.csv is in the following format:
    # name, capacity
    hall_list = functions.read("data/halls.csv", sort=True)

    students = [classes.Student(data) for data in student_list]
    halls = [classes.TeachingHall(data) for data in hall_list]

    # create list of Course objects
    courses = functions.create_course_list(course_list, students)

    # run some algorithms here

if __name__ == "__main__":
    main()
