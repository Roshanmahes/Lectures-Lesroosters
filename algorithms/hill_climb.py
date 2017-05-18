import classes
import functions
import random
import time
from score import *

def hill_climb(schedule, courses, halls, runtime=1,
    student_iters=10, teaching_iters=1, file_name="hill_climb.txt"):
    """
    Executes the hill climbing algorithm. Returns a modified schedule.
    """

    with open("results/" + file_name,"w") as output:
        start_time = time.time()

        for _ in range(runtime):
            for __ in range(student_iters):
                rand_int = random.randrange(len(courses))
                rand_type = random.choice(["seminar","practical"])
                schedule = first_student_swap(schedule, courses, halls, rand_int, rand_type)
                points = score(schedule, courses)
                stop_time = time.time()
                output.write(str(points) + " " + str(stop_time-start_time)+"\n")

            for __ in range(teaching_iters):
                schedule = best_teaching_swap(schedule, courses, halls)
                points = score(schedule, courses)
                stop_time = time.time()
                output.write(str(points) + " " + str(stop_time-start_time)+"\n")

    return schedule

def first_student_swap(schedule, courses, halls, course_index=0,
    teaching_type="seminar"):
    """
    Finds a  swap of a pair of students for the given course and
    type of teaching that yields a better score (if it exists),
    returning a new schedule with these students swapped.
    """
    if teaching_type not in set(("seminar", "practical")):
        return schedule

    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain halls
    schedule_flat = []
    for timeslot in zip(*schedule):
        for teaching in timeslot:
            if teaching:
                schedule_flat.append(classes.Teaching(teaching))
            else:
                schedule_flat.append(None)

    course = courses[course_index]

    # if  the course has no seminars resp. practicals
    if not course.get_group_count(teaching_type):
        return schedule

    # find all teachings in the given course of the given type
    groups = []
    for teaching in schedule_flat:
        if teaching:
            if teaching.course.name == course.name:
                if teaching.type == teaching_type:
                    groups.append(teaching)

    # a swap can't happen if there is less than two groups
    if len(groups) < 2:
        return schedule

    # get the appropriate capacity
    if teaching_type == "seminar":
        capacity = groups[0].course.s_cap
    else:
        capacity = groups[0].course.p_cap

    old_score = score(schedule, courses)
    for i,group in enumerate(groups):
        students = group.students

        for j,student in enumerate(students):
            for another_group in groups:
                other_students = another_group.students
                # if there are two or more students in the group and less
                # students in the other group than the capacity
                if len(students) > 1 and len(other_students) < capacity:
                    # put student into the other group
                    students.pop(j)
                    other_students.append(student)
                    new_schedule = functions.inflate_schedule_flat(schedule_flat)

                    # done if the score is better
                    if old_score < score(new_schedule, courses):
                        return new_schedule

                    # put student back in original group
                    students.insert(j, student)
                    other_students.remove(student)

                if another_group not in groups[:i]:
                    for k in range(len(other_students)):
                        # swap students
                        students[j], other_students[k] = \
                                other_students[k], students[j]
                        new_schedule = functions.inflate_schedule_flat(schedule_flat)

                        # done if the score is better
                        if old_score < score(new_schedule, courses):
                            return new_schedule

                        # swap back
                        students[j], other_students[k] = \
                                other_students[k], students[j]

    # no beneficial swap found
    return schedule

def best_teaching_swap(schedule, courses, halls):
    """
    Finds the best possible swap of a pair of teachings (if it exists),
    returning a new schedule with these teachings swapped.
    """
    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule)
        for teaching in timeslot]
    hall_count = len(halls)

    best_schedule = schedule
    best_score = score(schedule, courses)

    # initialise array with 'equivalent' schedules (having the same score)
    equiv_schedules = []
    # check all possible swaps of teachings
    for i, old_teaching in enumerate(schedule_flat):
        for m, new_teaching in enumerate(schedule_flat[i+1:]):
            # position of new_teaching in schedule_flat
            j = m+i+1

            # swap teachings
            if new_teaching:
                first_to_swap = classes.Teaching(new_teaching,
                    hall=halls[i % hall_count])
            else:
                first_to_swap = None

            if old_teaching:
                second_to_swap = classes.Teaching(old_teaching,
                    hall=halls[j % hall_count])
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

def first_teaching_swap(schedule, courses, halls):
    """
    Finds a beneficial swap of a pair of teachings (if it exists),
    returning a new schedule with these teachings swapped.
    """
    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule)
        for teaching in timeslot]
    hall_count = len(halls)

    best_schedule = schedule
    best_score = score(schedule, courses)

    # initialise array with 'equivalent' schedules (having the same score)
    equiv_schedules = []
    # check all possible swaps of teachings
    for i, old_teaching in enumerate(schedule_flat):
        for m, new_teaching in enumerate(schedule_flat[i+1:]):
            # position of new_teaching in schedule_flat
            j = m+i+1

            # swap teachings
            if new_teaching:
                first_to_swap = classes.Teaching(new_teaching,
                    hall=halls[i % hall_count])
            else:
                first_to_swap = None

            if old_teaching:
                second_to_swap = classes.Teaching(old_teaching,
                    hall=halls[j % hall_count])
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
                return new_schedule

            # remember equivalent schedule
            elif new_score == best_score:
                equiv_schedules.append(new_schedule)

    # choose randomly between the equivalent schedules
    return random.choice(equiv_schedules)
