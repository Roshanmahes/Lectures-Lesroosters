import classes
import random

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TIMESLOTS = 20
TEACHINGS = 129
HALLS = 7
MAX_ACTIVITIES = 5

CONFIG_TWO_1 = [0,3]
CONFIG_TWO_2 = [1,4]
CONFIG_THREE = [0,2,4]
CONFIG_FOUR = [0,1,3,4]
CONFIG_FIVE = [0,1,2,3,4]

def random_spread(courses, halls):

    number_of_activities = []
    sorted_courses = [[] for _ in range(MAX_ACTIVITIES)] # [[]] * MAX_ACTIVITIES werkt niet?
    teachings = []
    seminar_groups = []
    practical_groups = []

    lecture_counts = []
    seminar_counts = []
    practical_counts = []


    # sort courses by number of activities
    for course in courses:
        count = course.activity_count
        sorted_courses[int(count) - 1].append(course)

    print("Courses with 5-i activities:", [len(sorted_courses[i]) for i in reversed(range(MAX_ACTIVITIES))])
    #for i in reversed(sorted_courses):
    #    print(len(i))
    #    for j in i:
    #        print(j.name)

    for activities in reversed(sorted_courses):
        for course in activities:

            lecture_counts.append(course.lectures)
            seminar_counts.append(course.seminars)
            practical_counts.append(course.practicals)

            for _ in range(course.lectures):
                # assign students to lecture
                teachings.append(classes.Teaching("lecture",
                    course, course.students))

            if course.seminars:
                group_count = course.get_group_count("seminar")
                seminar_groups.append(group_count)
                students_per_group = [0] * group_count

                seminars = [classes.Teaching("seminar", course, [], ALPHABET[i]) for i in range(group_count)]

                for student in course.students:
                    rand = random.randint(0, group_count - 1)
                    while students_per_group[rand] == course.s_cap:
                        rand = random.randint(0, group_count - 1)
                    seminars[rand].students.append(student)
                    students_per_group[rand] += 1

                for seminar in seminars:
                    teachings.append(seminar)
            else:
                seminar_groups.append(0)

            if course.practicals:
                group_count = course.get_group_count("practical")
                practical_groups.append(group_count)
                students_per_group = [0] * group_count

                practicals = [classes.Teaching("practical", course, [], ALPHABET[i]) for i in range(group_count)]

                for student in course.students:
                    rand = random.randint(0, group_count - 1)
                    while students_per_group[rand] == course.p_cap:
                        rand = random.randint(0, group_count - 1)
                    practicals[rand].students.append(student)
                    students_per_group[rand] += 1

                for practical in practicals:
                    teachings.append(practical)
            else:
                practical_groups.append(0)

    # create an empty schedule of the right dimensions
    schedule = [[None for i in range(TIMESLOTS)] for j in range(len(halls))]

    activities = [0]*29
    total_teachings = [0]*29

    print(len(lecture_counts), "lectures:", lecture_counts)
    print(len(seminar_counts), "seminars:", seminar_counts)
    print(len(practical_counts), "practicals:", practical_counts)

    entries = list(range(TIMESLOTS * len(halls)))

    weekdays = [list(range(28)) for _ in range(5)]

    for i in range(29):

        activities[i] = lecture_counts[i] + seminar_counts[i] + practical_counts[i]
        total_teachings[i] = lecture_counts[i] + seminar_counts[i] * seminar_groups[i] + practical_counts[i] * practical_groups[i]

        if activities[i] == 5:
            random.shuffle(CONFIG_FIVE)

            #CONFIG_FIVE[1]
            days = [0,1,2,3,4]

            for j in range(lecture_counts[i]):
                weekday = random.choice(days)
                time = random.choice(weekdays[weekday])
                print("time:",weekday,time,j)

                weekdays[weekday].remove(time)
                #print("WEEKDAYS:",weekdays)
                days.remove(weekday)

            for k in range(seminar_counts[i]):
                weekday = random.choice(days)
                time = random.choice(weekdays[weekday])
                print("time:",weekday,time,j)

                days.remove(weekday)
            for l in range(practical_counts[i]):
                weekday = random.choice(days)
                time = random.choice(weekdays[weekday])
                print("time:",weekday,time,j)

                days.remove(weekday)

            daymin = weekday * 28
            daymax = daymin + 27
            #weekdays.remove(day)
        elif activities[i] == 4:
            random.shuffle(CONFIG_FOUR)
        elif activities[i] == 3:
            random.shuffle(CONFIG_THREE)
        elif activities[i] == 2:
            continue
        # if there is only one activity, or if there are more activities than days
        #else:
            # arrange in any place
        # if only one: wednesday??



    print("activities:\n",activities,"\n")
    print("total teachings:\n",total_teachings,"\n")

    entries = list(range(TIMESLOTS * len(halls)))
    for teaching in teachings:
        rand = entries[random.randint(0, len(entries) - 1)]
        teaching.hall = halls[rand // 20]
        schedule[rand // 20][rand % 20] = teaching
        entries.remove(rand)




    print("#seminar groups:", seminar_groups)
    print("#practical groups:", practical_groups)

    print(teachings)


    #print(sorted_courses)
    #for i in teachings:
    #    print("\n",i)
    #print(number_of_activities)
