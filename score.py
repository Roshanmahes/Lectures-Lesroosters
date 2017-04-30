import collections


def score(schedule):
    """
    Analyses the quality of a schedule, returning the score.
    """
    # initial score
    score = 1000

    # flatten schedule
    schedule_flat = [teaching for timeslot in schedule
        for teaching in timeslot]

    # remove all empty teachings
    schedule_flat = [teaching for teaching in schedule_flat if teaching]

    for teaching in schedule_flat:
        # check if the number of students in a teaching exceeds the capacity
        if len(teaching.students) > teaching.hall.capacity:
            score-= 1

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

    return score
