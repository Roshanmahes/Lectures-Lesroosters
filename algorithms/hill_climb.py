import classes
import random
from score import *


def hill_climb(courses,halls):
    """

    """

    return schedule

def student_swap(schedule, courses, halls):
    """
    Finds a  swap of a pair of students for a random course that yields
    a better score (if it exists),
    returning a new schedule with these students swapped.
    """
    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule) for teaching in timeslot]

    # create a list of teachings sorted by timeslot for each course
    sorted_teachings = []
    for course in courses:
        if course.get_group_count("seminar") or course.get_group_count("practical"):
            course_teachings = []
            seminars = []
            practicals = []
            for teaching in schedule_flat:
                if teaching:
                    if teaching.course.name == course.name:
                        if teaching.type == "seminar":
                            seminars.append(teaching)
                        elif teaching.type == "practical":
                            practicals.append(teaching)

            course_teachings.append(seminars)
            course_teachings.append(practicals)
            sorted_teachings.append(course_teachings)

    teachings = []
    while not teachings:
        random_course = sorted_teachings[random.randint(0, len(sorted_teachings)-1)]
        if len(random_course[0]) > 1 and len(random_course[1]) > 1:
            rand = random.randint(0,1)
            teachings = random_course[rand]
            if rand:
                capacity = teachings[0].course.p_cap
            else:
                capacity = teachings[0].course.s_cap
        elif len(random_course[0]) > 1:
            teachings = random_course[0]
            capacity = teachings[0].course.s_cap
        elif len(random_course[1]) > 1:
            teachings = random_course[1]
            capacity = teachings[0].course.p_cap

    old_score = score(schedule, courses)
    for teaching in teachings:
        for student in teaching.students:
            for another_teaching in teachings:
                if not another_teaching == teaching:
                    for another_student in another_teaching.students:
                        student, another_student = another_student, student
                        if old_score < score(schedule, courses):
                            return schedule
                        student, another_student = another_student, student
                    if len(teaching.students) > 1 and len(another_teaching.students) < capacity:
                        teaching.students.remove(student)
                        another_teaching.students.append(student)
                        if old_score < score(schedule, courses):
                            return schedule
                        teaching.students.append(student)
                        another_teaching.students.remove(student)
    return schedule


def teaching_swap(schedule, courses, halls):
    """
    Finds the best possible swap of a pair of teachings (if it exists),
    returning a new schedule with these teachings swapped.
    """
    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule) for teaching in timeslot]

    # transpose schedule such that teachings of the same timeslot
    # are in the same list
    best_schedule = list(map(list, zip(*schedule)))
    best_score = score(schedule, courses)

    # check all possible swaps of teachings
    for i, old_teaching in enumerate(schedule_flat):
        if old_teaching:
            for j, new_teaching in enumerate(schedule_flat[i+1:]):
                new_schedule = list(map(list, zip(*schedule)))

                # swap old_teaching and new_teaching
                new_schedule[old_teaching.timeslot][i % len(halls)] = new_teaching
                new_schedule[(j+i+1) // len(halls)][(j+i+1) % len(halls)] = old_teaching

                # compute new score
                new_score = score(list(map(list, zip(*new_schedule))), courses)
                if new_score > best_score:
                    best_schedule, best_score = new_schedule, new_score

    return list(map(list, zip(*best_schedule)))
