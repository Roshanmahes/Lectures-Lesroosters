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

    # show some facts about the random_scores.csv file which contains the
    # scores of 10 million randomly generated schedules
    #score_list = []
    #best_score = 0
    #worst_score = 1000
    schedule = [[] for _ in range(500)]

    #    score_list.append(points)
    #    if points >= best_score:
    #        best_score = points
    #        best_schedule = schedule
    #    elif points < worst_score:
    #        worst_score = points
    #        worst_schedule = schedule
    i = 1
    schedule[1] = algorithms.random_fit(courses,halls)
    print(schedule[1])

    schedule[2] = hill_climb.student_swap(schedule, courses, halls)
    print(schedule[2])
    #print_schedule(halls, schedule)
    #print_schedule(halls, hill_climb.teaching_swap(schedule, courses, halls))

    while True: #score(schedule[i], courses) <= score(schedule[i+1],courses):
        schedule[i+1] = hill_climb.teaching_swap(schedule[i], courses, halls)
        print_schedule(halls, schedule[i+1])
        print("i:",i)
        i += 1

if __name__ == "__main__":
    main()
