import classes
import functions
import math
import random
import time # TEMPORARY
import os.path

from score import *
from functions import *

START_TEMP = 1
SAVE_THIS = 1325 # TEMPORARY

def simulated_annealing(schedule, courses, halls, temp_iterator,
    total_iters=2000, student_swaps=10, teaching_swaps=1, time_cap=60,
    file_name="simulated_annealing.txt"):
    """
    Executes the simulated annealing algorithm.
    Returns a modified schedule.

    temp_iterator must be a function from temperature.py
    """

    with open("results/" + file_name, "a") as output_file:
        temperature = START_TEMP
        start_time = time.time()

        # execute until minimum temperature is reached
        for i in range(total_iters):

            # perform either a teaching swap or a student swap (choose randomly)
            if random.choice([True, False]):
                students_swapped = True
                iter_count = student_swaps
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

                    points = score(schedule, courses)
                    if points > SAVE_THIS:
                        if not os.path.isfile(str(points) + ".pdf"):
                            save_schedule(schedule, halls, str(points))
                    stop_time = time.time()
                    output_file.write(str(points)+" "+str(stop_time-start_time)+" "+str(temperature)+"\n")

                    if stop_time-start_time > time_cap:
                        return schedule

            # decrement temperature
            temperature = temp_iterator(temperature, total_iters, i, START_TEMP)

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
    schedule_flat = functions.flatten_schedule(schedule)
    hall_count = len(halls)
    teaching_count = len(schedule_flat)

    # select random teachings
    i = random.randrange(teaching_count)
    j = random.randrange(teaching_count)

    # ensure teachings are different
    while i == j:
        j = random.randrange(teaching_count)

    first_teaching = schedule_flat[i]
    second_teaching = schedule_flat[j]

    # swap teachings
    if second_teaching:
        first_to_swap = classes.Teaching(second_teaching,
            hall=halls[i % hall_count])
    else:
        first_to_swap = None

    if first_teaching:
        second_to_swap = classes.Teaching(first_teaching,
            hall=halls[j % hall_count])
    else:
        second_to_swap = None

    # create new_schedule from schedule
    new_schedule = [None]*len(schedule)
    for k,row in enumerate(schedule):
        new_schedule[k] = list(row)

    # swap teachings
    new_schedule[i % hall_count][i // hall_count] = first_to_swap
    new_schedule[j % hall_count][j // hall_count] = second_to_swap

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

    schedule_flat = functions.flatten_schedule(schedule, new_teachings=True)

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
