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
    def __init__(self, data, students):
        self.name = data[0]
        self.hoorcolleges = int(data[1])
        self.werkcolleges = int(data[2])
        self.wc_cap = int(data[3])
        self.practica = int(data[4])
        self.p_cap = int(data[5])
        self.students = students

class LectureHall:
    def __init__(self, data):
        self.name = data[0]
        self.cap = int(data[1])

class Lecture:
    def __init__(self, _type, course, students, lecturehall):
        self.courseName = course.name
        self.type = _type
        # studenten wisselen tussen lecture classes met dezelfde courseName en type
        if _type == "hoorcollege":
            self.cap = len(students)
        elif _type == "werkcollege":
            self.cap = course.wc_cap
        else:
            self.cap = course.p_cap
        self.students = students
        self.lecturehall = lecturehall
