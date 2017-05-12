import random
import classes
from score import *

def hill_climb(schedule, courses, halls, runtime=1, student_iters=10, teaching_iters=1):
    """
    Executes the hill climbing algorithm.
    Returns a modified schedule when interrupted.
    """

    for _ in range(runtime):
        for __ in range(student_iters):
            schedule = first_student_swap(schedule, courses, halls)
        print("Students  swapped:", score(schedule, courses))
        for __ in range(teaching_iters):
            schedule = best_teaching_swap(schedule, courses, halls)
        print("Teachings swapped:", score(schedule, courses))

    return schedule


def random_student_swap(schedule, courses, halls, course_index=None):
    """

    """
    # TODO

def first_student_swap(schedule, courses, halls, course_index=None):
    """
    Finds a  swap of a pair of students for the given course
    (defaults to random) that yields a better score (if it exists),
    returning a new schedule with these students swapped.
    """
    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule) for teaching in timeslot]

    teachings = []
    course_teachings = []
    if course_index:
        course = courses[course_index]
        if course.get_group_count("seminar") or course.get_group_count("practical"):
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
        else:
            return schedule
    else:
        # create a list of teachings sorted by timeslot for each course
        sorted_teachings = []
        for course in courses:
            if course.get_group_count("seminar") or course.get_group_count("practical"):
                teachings_for_course = []
                seminars = []
                practicals = []
                for teaching in schedule_flat:
                    if teaching:
                        if teaching.course.name == course.name:
                            if teaching.type == "seminar":
                                seminars.append(teaching)
                            elif teaching.type == "practical":
                                practicals.append(teaching)

                teachings_for_course.append(seminars)
                teachings_for_course.append(practicals)
                sorted_teachings.append(teachings_for_course)

    while not teachings:
        if not course_index:
            course_teachings = random.choice(sorted_teachings)
        if len(course_teachings[0]) > 1 and len(course_teachings[1]) > 1:
            teachings = random.choice(course_teachings)
            if teachings[0].type == "seminar":
                capacity = teachings[0].course.s_cap
            else:
                capacity = teachings[0].course.p_cap
        elif len(course_teachings[0]) > 1:
            teachings = course_teachings[0]
            capacity = teachings[0].course.s_cap
        elif len(course_teachings[1]) > 1:
            teachings = course_teachings[1]
            capacity = teachings[0].course.p_cap

    old_score = score(schedule, courses)
    for teaching in teachings:
        for student in teaching.students:
            for another_teaching in teachings:
                if not another_teaching in teachings[:teachings.index(teaching)]:
                    if len(teaching.students) > 1 and len(another_teaching.students) < capacity:
                        teaching.students.remove(student)
                        another_teaching.students.append(student)
                        if old_score < score(schedule, courses):
                            return schedule
                        teaching.students.append(student)
                        another_teaching.students.remove(student)
                    for another_student in another_teaching.students:
                        student, another_student = another_student, student
                        if old_score < score(schedule, courses):
                            return schedule
                        student, another_student = another_student, student
    return schedule


def random_teaching_swap(schedule, courses, halls):
    """
    Swaps two randomly selected teachings, returning the new schedule.
    """
    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule) for teaching in timeslot]
    hall_count = len(halls)
    teaching_count = len(schedule_flat)

    # select random teachings
    first_index = random.randrange(teaching_count)
    second_index = random.randrange(teaching_count)
    first_teaching = schedule_flat[first_index]
    second_teaching = schedule_flat[second_index]

    # ensure teachings are different
    while first_teaching == second_teaching:
        second_teaching = random.choice(schedule_flat)

    # swap teachings
    if second_teaching:
        first_to_swap = classes.Teaching(second_teaching, hall=halls[first_index % hall_count])
    else:
        first_to_swap = None
    if first_teaching:
        second_to_swap = classes.Teaching(first_teaching, hall=halls[second_index % hall_count])
    else:
        second_to_swap = None

    # create new_schedule from schedule
    new_schedule = [None]*len(schedule)
    for k,row in enumerate(schedule):
        new_schedule[k] = list(row)

    # swap teachings
    new_schedule[first_index % hall_count][first_index // hall_count] = first_to_swap
    new_schedule[second_index % hall_count][second_index // hall_count] = second_to_swap

    return new_schedule

def best_teaching_swap(schedule, courses, halls):
    """
    Finds the best possible swap of a pair of teachings (if it exists),
    returning a new schedule with these teachings swapped.
    """
    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule) for teaching in timeslot]
    hall_count = len(halls)

    best_schedule = schedule
    best_score = score(schedule, courses)

    # initialise array with 'equivalent' schedules (having the same score)
    equiv_schedules = []
    # check all possible swaps of teachings
    for i, old_teaching in enumerate(schedule_flat):
        for m, new_teaching in enumerate(schedule_flat[i+1:]):
            j = m+i+1

            # swap teachings
            if new_teaching:
                first_to_swap = classes.Teaching(new_teaching, hall=halls[i % hall_count])
            else:
                first_to_swap = None
            if old_teaching:
                second_to_swap = classes.Teaching(old_teaching, hall=halls[j % hall_count])
            else:
                second_to_swap = None

            # create new_schedule from schedule
            new_schedule = [None]*len(schedule)
            for k,row in enumerate(schedule):
                new_schedule[k] = list(row)
            new_schedule[i % hall_count][i // hall_count] = first_to_swap
            new_schedule[j % hall_count][j // hall_count] = second_to_swap

            # compute new score
            new_score = score(new_schedule, courses)
            if new_score > best_score:
                best_schedule, best_score = new_schedule, new_score

                # there are no 'equivalent' schedules anymore
                equiv_schedules = []

            # remember equivalent schedule
            elif new_score == best_score:
                equiv_schedules.append(new_schedule)

    # choose randomly between the equivalent schedules
    if equiv_schedules:
        best_schedule = random.choice(equiv_schedules)

    return best_schedule
