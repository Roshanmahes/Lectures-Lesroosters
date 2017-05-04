import collections
from operator import itemgetter

# configurations eligible for bonus points
OPTIMAL_CONFIGURATIONS = {"03","14","02-24","01-13-34"}
PERIODS = 4

def score(schedule, courses):
    """
    Analyses the quality of a schedule, returning the score.
    """
    # initial score
    score = 1000

    # flatten schedule in such a way that the teachings are sorted by timeslot
    # schedule is a list of lists, where each list contains
    # teachings scheduled at a certain hall
    schedule_flat = [teaching for timeslot in zip(*schedule)
        for teaching in timeslot]

    # remove all empty teachings
    schedule_flat = [teaching for teaching in schedule_flat if teaching]

    # calculate bonus and malus points
    score += capacity_points(schedule_flat) + conflict_points(schedule) \
        + configuration_points(schedule_flat, courses)

    return score

def capacity_points(schedule_flat, malus=1):
    """
    Compute malus points, deducting points if the number of students
    in a teaching exceeds the capacity.
    """
    points = 0

    for teaching in schedule_flat:
        if len(teaching.students) > teaching.hall.capacity:
            points -= malus * (len(teaching.students) - teaching.hall.capacity)

    return points

def conflict_points(schedule, malus=1):
    """
    Compute malus points, deducting points if a student
    has multiple teachings at once.
    """
    points = 0

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
                points -= malus * (count - 1)

    return points

def configuration_points(schedule_flat, courses, malus=10, bonus=20):
    """
    Compute bonus and malus points corresponding to the
    quality of the distribution of each course over the week.
    Points are deducted if there are multiple teachings
    of the same course on the same day.
    Points are added if the teachings are optimally distributed.
    """
    points = 0

    # create a list of teachings sorted by timeslot for each course
    sorted_teachings = []
    for course in courses:
        course_teachings = []
        for teaching in schedule_flat:
            if teaching.course_name == course.name:
                course_teachings.append(teaching)
        sorted_teachings.append(course_teachings)

    # initialise list of activity distributions that will be needed to
    # calculate bonus points
    activity_distributions = []

    for course_teachings in sorted_teachings:
        # initialise variables

        # turns false if malus points are applied
        so_far_so_good = True

        # a string that represents the distribution of activities over the week
        activity_distribution = ""

        current_day = None

        # turn true if another seminar (resp. practical) group has been
        # checked for this day already
        seminar_had = False
        practical_had = False

        for i in range(len(course_teachings)-1):
            teaching = course_teachings[i]
            successor = course_teachings[i+1]

            # day on which teaching (resp. its successor) takes place
            teaching_day = teaching.timeslot // PERIODS
            successor_day = successor.timeslot // PERIODS

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
                    activity_distribution += str(teaching_day) + \
                        str(successor_day) + "-"

                # if another group of the same activity on the same day
                # hasn't been checked already
                elif (successor.type != "seminar" or not seminar_had) and \
                        (successor.type != "practical" or not practical_had):
                    so_far_so_good = False
                    points -= malus
                    if teaching.type == "seminar":
                        seminar_had = True
                    elif teaching.type == "practical":
                        practical_had = True

        if so_far_so_good:
            if len(activity_distribution) > 0:
                activity_distributions.append(activity_distribution[:-1])

    for distribution in activity_distributions:
        if distribution in OPTIMAL_CONFIGURATIONS:
            points += bonus

    return points
