TIMESLOTS = 20

def calculate(courses, teachings, hall_list):
    """
    Calculates an upper bound to the number
    of configurations of the state space.
    """

    # upper bound to number of ways the teachings can be scheduled
    prod1 = 1
    tracker = 0
    teaching_sizes = [len(teaching.students) for teaching in teachings]
    teaching_sizes.sort(reverse=True)
    for size in teaching_sizes:
        big_enough_halls = 0
        for hall in hall_list:
            if size < int(hall[1]):
                big_enough_halls += 1
        prod1 *= big_enough_halls * TIMESLOTS - tracker
        tracker += 1

    # upper bound to number of ways
    # the students can be put into the S and P groups
    prod2 = 1
    for course in courses:
        if course.seminars:
            group_count = course.get_group_count("seminar")
            capacity = course.s_cap
        elif  course.practicals:
            group_count = course.get_group_count("practical")
            capacity = course.p_cap
        else:
            group_count = 0
        if group_count:
            prod2 *= (group_count ** len(course.students)) \
                    ** (course.seminars+course.practicals)

    return prod1*prod2
