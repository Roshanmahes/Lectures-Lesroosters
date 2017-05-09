import classes
import random
from score import *
import random

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
        course_teachings = []
        seminars = []
        practicals = []
        for teaching in schedule_flat:
            if teaching.course.name == course.name:
                if teaching.type == "seminar":
                    seminars.append(teaching)
                elif teaching.type == "practical":
                    practicals.append(teaching)
        course_teachings.append(seminars)
        course_teachings.append(practicals)
        sorted_teachings.append(course_teachings)

    best_schedule = schedule
    best_score = score(schedule, courses)

    for course_teachings in sorted_teachings:

        best_schedule_per_course = best_schedule
        best_score_per_course = score(best_schedule_per_course, courses)

        # find best student swap between seminar groups
        for i, seminar1 in enumerate(seminars):
            for seminar2 in seminars[i+1:]:
                for j, student1 in enumerate(seminar1.students):
                    for student2 in seminar2.students[j+1:]:
                        new_schedule = schedule

                        # position of seminars in schedule
                        #index1 = schedule_flat.index(seminar1)
                        #index2 = schedule_flat.index(seminar2)

                        # swap students
                        seminar1.students.remove(student1)
                        seminar1.students.append(student2)
                        seminar2.students.remove(student2)
                        seminar2.students.append(student1)

                        # compute new score
                        #new_score =


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

    same_schedules = []
    print("Old score:", best_score)


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
                if new_score >= best_score:
                    # we don't have schedules with same score anymore
                    same_schedules = []
                    best_schedule, best_score = new_schedule, new_score
                elif new_score == best_score:
                    same_schedules.append(new_schedule)

                    # choose randomly between the schedules
                    best_schedule = random.choice(same_schedules)

    return list(map(list, zip(*best_schedule)))
