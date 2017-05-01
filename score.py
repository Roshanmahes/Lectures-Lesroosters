import collections
from operator import itemgetter


def score(schedule, courses):
    """
    Analyses the quality of a schedule, returning the score.
    """
    # initial score
    score = 1000

    # flatten schedule in such a way that the teachings are sorted by timeslot
    schedule_flat = [teaching for timeslot in zip(*schedule)
        for teaching in timeslot]

    # remove all empty teachings
    schedule_flat = [teaching for teaching in schedule_flat if teaching]

    for teaching in schedule_flat:
        # check if the number of students in a teaching exceeds the capacity
        if len(teaching.students) > teaching.hall.capacity:
            score -= len(teaching.students) - teaching.hall.capacity

    for timeslot in zip(*schedule):
        # list of students following a teaching at timeslot
        students = []

        # add students in each teaching at timeslot
        for teaching in timeslot:
            if teaching:
                students.append(teaching.students)

        # flatten students
        students = [student for teaching in students for student in teaching]

        # create dictionary keeping track of the number
        # of teachings a student has at timeslot
        counter = collections.Counter(students)

        # subtract points if a student has multiple teachings at once
        for student, count in counter.items():
            if count > 1:
                score -= count - 1

    print("\n")
    for course in courses:
        activity_count = course.get_activity_count()

        # list of teachings corresponding to course
        course_teachings = []
        for teaching in schedule_flat:
            if teaching.course_name == course.name:
                course_teachings.append(teaching)

        # list of lists containing teachings, where each list
        # corresponds to an activity (i.e. a lecture, practical or seminar)
        course_activities = []
        seminar_list = []
        practical_list = []

        for teaching in course_teachings:
            if teaching.type == "lecture":
                course_activities.append([teaching])
            elif teaching.type == "seminar":
                seminar_list.append(teaching)
            else:
                practical_list.append(teaching)

        if practical_list:
            course_activities.append(practical_list)
        if seminar_list:
            course_activities.append(seminar_list)
        print(course_activities)

        # find 'distance' between each activity

        min_timeslots = [0] * activity_count
        # find minimum timeslot of each activity
        for i,activity in enumerate(course_activities):
            min_timeslots[i] = \
                min([teaching.timeslot for teaching in activity])

        print(min_timeslots)

        # sort activities by timeslot
        course_activities = [activity for (timeslot, activity) \
            in sorted(zip(min_timeslots, course_activities))]

        print(course_activities)

    return score
