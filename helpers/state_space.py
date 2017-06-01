from math import factorial

TIMESLOTS = 20
EVENINGSLOTS = 5

def calculate(courses, hall_count):
    """
    Calculates an upper bound to the number of configurations of the
    state space. Returns an integer.
    """
    # calculate the amount of teachings
    teachings = 0
    for course in courses:
        teachings += course.lectures + course.get_group_count("seminar") + \
                course.get_group_count("practical")

    # upper bound to number of ways the teachings can be scheduled
    slots = TIMESLOTS * hall_count + EVENINGSLOTS
    t_prod = int(factorial(slots)/factorial(slots - teachings))

    # upper bound to number of ways the students can be put
    # into the seminar and practical groups for each course
    s_prod = 1
    for course in courses:
        # get the capacity that is non-zero, if it exists (this works because
        # s_cap and p_cap are always equal if they are both non-zero)
        if course.seminars:
            group_count = course.get_group_count("seminar")
            capacity = course.s_cap
        elif course.practicals:
            group_count = course.get_group_count("practical")
            capacity = course.p_cap
        else:
            group_count = 0
        # if the group_count is greater than 0
        if group_count:
            s_prod *= (group_count ** len(course.students)) \
                    ** (course.seminars+course.practicals)

    return t_prod * s_prod
