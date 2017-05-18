import classes
import functions
import math
import random
from score import *

def simulated_annealing(schedule, courses, halls, start_temp=1,
    end_temp=0.0001, max_iter=200, student_prob=0.9,
    student_swaps=10, teaching_swaps=1):
    """
    Executes the simulated annealing algorithm.
    Returns a modified schedule.
    """
    temperature = start_temp

    # execute until minimum temperature is reached
    while temperature > end_temp:
        rand = random.random()

        # perform student swap with probability student_prob
        if student_prob > rand:
            students_swapped = True
            iter_count = student_swaps
        # else perform teaching swap
        else:
            students_swapped = False
            iter_count = teaching_swaps

        for _ in range(iter_count):
            # swap either students or teachings
            if students_swapped:
                new_schedule = random_student_swap(schedule, courses, halls)
            else:
                new_schedule = random_teaching_swap(schedule, courses, halls)

            # compute scores
            old_score = score(schedule, courses)
            new_score = score(new_schedule, courses)
            probability = random.random()

            # compute probability of accepting new schedule
            if acceptance_probability(old_score,new_score,
                temperature) > probability:
                schedule = new_schedule

        # decrement temperature
        temperature *= ((end_temp/start_temp) ** (1/max_iter))

    return schedule

def acceptance_probability(old_score, new_score, temperature):
    """
    Computes the probability of accepting a new schedule.
    """
    # always accept if the score is better
    if new_score > old_score:
        return 1
    else:
        return math.exp((new_score-old_score) / temperature)

def random_teaching_swap(schedule, courses, halls):
    """
    Swaps two randomly selected teachings, returning the new schedule.
    """
    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule)
        for teaching in timeslot]
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
        first_to_swap = classes.Teaching(second_teaching,
            hall=halls[first_index % hall_count])
    else:
        first_to_swap = None
    if first_teaching:
        second_to_swap = classes.Teaching(first_teaching,
            hall=halls[second_index % hall_count])
    else:
        second_to_swap = None

    # create new_schedule from schedule
    new_schedule = [None]*len(schedule)
    for k,row in enumerate(schedule):
        new_schedule[k] = list(row)

    # swap teachings
    new_schedule[first_index % hall_count] \
        [first_index // hall_count] = first_to_swap
    new_schedule[second_index % hall_count] \
        [second_index // hall_count] = second_to_swap

    return new_schedule

def random_student_swap(schedule, courses, halls):
    """
    Swaps two randomly selected students of a randomly selected course,
    returning the new schedule.
    """

    # randomly find a course in which a swap can be made
    valid_courses = list(courses)
    swappable_types = []
    while not swappable_types:
        course = random.choice(valid_courses)

        if course.seminars or course.practicals:
            if course.get_group_count("seminar") > 1:
                swappable_types.append("seminar")
            elif course.get_group_count("practical") > 1:
                swappable_types.append("practical")
        if not swappable_types:
            valid_courses.remove(course)

    # select a random type of teaching from the valid choices for course
    teaching_type = random.choice(swappable_types)

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

    # find all teachings in the given course of the given type
    groups = []
    for teaching in schedule_flat:
        if teaching:
            if teaching.course.name == course.name:
                if teaching.type == teaching_type:
                    groups.append(teaching)

    # get the appropriate capacity
    if teaching_type == "seminar":
        capacity = groups[0].course.s_cap
    else:
        capacity = groups[0].course.p_cap

    first_group = random.choice(groups).students

    # if first_group only has 1 student it mustn't be removed
    removable = True
    if len(first_group) == 1:
        removable = False
    second_group = random.choice(groups).students

    # randomly select students to swap by selecting indices
    i = random.randrange(len(first_group))
    if removable:
        j = random.randrange(capacity)
    else:
        j = random.randrange(len(second_group))

    # if j is within range, swap the students at i and j
    try:
        first_group[i], second_group[j] = second_group[j], first_group[i]
    # if j is out of range, there is no student at j so put the i student there
    except IndexError:
        second_group.append(first_group[i])
        first_group.pop(i)

    return functions.inflate_schedule_flat(schedule_flat)
