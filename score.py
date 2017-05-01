import collections
from operator import itemgetter

optimal_configurations = {"03","14","02-24","01-13-34"}

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

    # create a list of teachings sorted by time for each course
    sorted_teachings = []
    for course in courses:
        course_teachings = []
        for teaching in schedule_flat:
            if teaching.course_name == course.name:
                course_teachings.append(teaching)
        sorted_teachings.append(course_teachings)

    # initialize list of activity distributions that will be needed to
    # calculate bonus points
    activity_distributions = []

    for _,course_teachings in enumerate(sorted_teachings):
        # initialize variables

        # turns false if malus points are applied
        so_far_so_good = True

        # a string that represents the distribution of activities over the week
        activity_distribution = ""

        current_day = None

        # turn true if another seminar (resp. practical) group has been checked
        # for this day already
        seminar_had = False
        practical_had = False

        for i in range(len(course_teachings)-1):
            teaching = course_teachings[i]
            successor = course_teachings[i+1]

            # day on which teaching (resp. its successor) takes place
            teaching_day = teaching.timeslot//4
            successor_day = successor.timeslot//4

            # reset daily variables if new day is reached
            if teaching_day != current_day:
                seminar_had = False
                practical_had = False
            current_day = teaching_day

            # find the distance between the days on which teaching and its
            # successor take place
            delta = successor_day - current_day

            # if teaching and successor are not two different groups of the
            # same activity
            if teaching.type != successor.type or teaching.type == "lecture":
                if delta:
                    # keep track of distances between teachings
                    activity_distribution += str(teaching_day) + str(successor_day) + "-"

                # if another group of the same activity on the same day hasn't
                # been checked already
                elif (successor.type != "seminar" or not seminar_had) and \
                        (successor.type != "practical" or not practical_had):
                    so_far_so_good = False
                    score -= 10
                    if teaching.type == "seminar":
                        seminar_had = True
                    elif teaching.type == "practical":
                        practical_had = True

        if so_far_so_good:
            if len(activity_distribution) > 0:
                activity_distributions.append(str(_)+" "+activity_distribution[:-1])

    for distribution in activity_distributions:
        if distribution in optimal_configurations:
            score += 20

    return score
