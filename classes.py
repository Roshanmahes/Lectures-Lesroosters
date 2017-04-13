"""class Student:
    def __init__(self, data):
        self.name = data[1] + " " + data[0]
        self.id = int(data[2])
        courses = []
        for str in data[3:]:
            if str:
                courses.append(str)
        self.courses = courses
"""

class Course:
    """

    """
    def __init__(self, data, students=[]):
        self.name = data[0]
        self.lectures = int(data[1])
        self.seminars = int(data[2])
        self.s_cap = int(data[3])
        self.practicals = int(data[4])
        self.p_cap = int(data[5])
        self.students = students

"""class TeachingHall:
    def __init__(self, data):
        self.name = data[0]
        self.cap = int(data[1])
"""

class Teaching:
    def __init__(self, _type, course, students=[]):
        self.courseName = course.name
        self.type = _type

        # studenten wisselen tussen teaching classes met dezelfde courseName en type
        if _type == "lecture":
            self.cap = len(students)
        elif _type == "seminar":
            self.cap = course.s_cap
        else:
            self.cap = course.p_cap
            
        if not students:
            self.students = course.students
        else:
            self.students = students
