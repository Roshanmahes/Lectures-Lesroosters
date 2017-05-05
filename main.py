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

<<<<<<< HEAD
    # create a simple schedule
    #score_list = []
    #best_score = -300
    #worst_score = -300
    #for _ in range(1000000):
    schedule = algorithms.random_walk(courses, halls)
    points = score(schedule, courses)
    #    score_list.append(points)
    #    if points >= best_score:
    #        best_score = points
    #        best_schedule = schedule
    #    elif points < worst_score:
    #        worst_score = points
    #        worst_schedule = schedule

    print_schedule(halls, schedule)
    #print(best_score, worst_score)
    #print_schedule(halls, best_schedule)
    #print_schedule(halls, worst_schedule)
    print("\nScore:", points)
=======
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

>>>>>>> origin/master

if __name__ == "__main__":
    main()
