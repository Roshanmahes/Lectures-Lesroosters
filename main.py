import classes
import algorithms
import csv
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

    students = [classes.Student(data) for data in student_list]
    halls = [classes.TeachingHall(data) for data in hall_list]

    # create list of Course objects
    courses = create_course_list(course_list, students)

    # show some facts about the random_scores.csv file which contains the
    # scores of 10 million randomly generated schedules
    scores = []
    with open("data/random_scores.csv") as f:
        reader = csv.reader(f)
        for score in next(reader):
            if score:
                scores.append(int(score))
    scores.sort()
    print(scores[:10])
    print(scores[-10:])
    print(sum(scores)/len(scores))


if __name__ == "__main__":
    main()
