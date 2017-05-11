import random
from score import *


def hill_climb(schedule, courses, halls):
    """
    Executes the hill climbing algorithm.
    Returns a modified schedule when interrupted.
    """
    swaps = 0
    STUDENT_SWAP = 10
    TEACHING_SWAP = 1

    try:
        while True:
            schedule = swap_my_students(schedule, courses, halls, STUDENT_SWAP)
            schedule = swap_my_teachings(schedule, courses, halls, TEACHING_SWAP)
            swaps += STUDENT_SWAP + TEACHING_SWAP

    except (KeyboardInterrupt, SystemExit):
        print("swaps:", swaps)

        return schedule

def swap_my_students(schedule, courses, halls, iterations=1):
    for _ in range(iterations):
        schedule = student_swap(schedule, courses, halls)
        print("New score (student swapped):", score(schedule, courses))
    return schedule

def swap_my_teachings(schedule, courses, halls, iterations=1):
    for _ in range(iterations):
        schedule = teaching_swap(schedule, courses, halls)
        print("New score (teaching swapped):", score(schedule, courses))
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
                if not another_teaching in teachings[:teachings.index(teaching)]:
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

    # initialise array with 'equivalent' schedules (that means, having same score)
    equiv_schedules = []

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

                    # there are no 'equivalent' schedules anymore
                    equiv_schedules = []
                elif new_score == best_score:
                    equiv_schedules.append(new_schedule)

    # choose randomly between the equivalent schedules
    if equiv_schedules:
        best_schedule = random.choice(equiv_schedules)

    return list(map(list, zip(*best_schedule)))
