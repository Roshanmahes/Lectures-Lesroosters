import classes
from functions import *
from score import *

def  main():
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

    student_objects = [classes.Student(data) for data in student_list]
    hall_objects = [classes.Teaching_Hall(data) for data in hall_list]

    # create list of Course objects
    courses = create_course_list(course_list, student_objects)

    # create list of Teaching objects
    teachings = create_teachings(courses)

    schedule = create_schedule(teachings, hall_objects)

    print_schedule(hall_objects, schedule)

    # determine score of schedule
    print(score(schedule))

if __name__ == "__main__":
    main()
