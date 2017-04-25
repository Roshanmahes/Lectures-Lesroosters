from math import factorial

TIMESLOTS = 20
EVENINGSLOTS = 5

def calculate(courses, teachings, hall_list):
    """
    Calculates an upper bound to the number
    of configurations of the state space.
    """

    # upper bound to number of ways the teachings can be scheduled
    slots = TIMESLOTS * len(hall_list) + EVENINGSLOTS
    prod1 = int(factorial(slots)/factorial(slots - len(teachings)))

    # upper bound to number of ways the students can be put
    # into the S and P groups for each course
    prod2 = 1
    for course in courses:
        # get the capacity that is non-zero, if it exists
        # (works because s_cap and p_cap are always equal if they are both non-zero)
        if course.seminars:
            group_count = course.get_group_count("seminar")
            capacity = course.s_cap
        elif  course.practicals:
            group_count = course.get_group_count("practical")
            capacity = course.p_cap
        else:
            group_count = 0
        # if the group_count is greater than 0
        if group_count:
            prod2 *= (group_count ** len(course.students)) \
                    ** (course.seminars+course.practicals)

    return prod1*prod2
