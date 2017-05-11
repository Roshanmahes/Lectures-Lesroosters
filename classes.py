class Course:
    """
    Creates a course object containing course data and
    a list of students following the course.
    The course data is in the following format:
    [name, lectures, seminars, seminar capacity,
    practicals, practical capacity]
    """
    def __init__(self, data, students):
        self.name = data[0]
        self.lectures = int(data[1])
        self.seminars = int(data[2])
        self.s_cap = int(data[3])
        self.practicals = int(data[4])
        self.p_cap = int(data[5])
        self.students = students
        self.activity_count = self.lectures + self.seminars + self.practicals

    def get_group_count(self, _type):
        """Determine number of groups of type _type."""

        student_count = len(self.students)
        if _type == "seminar":
            if not self.seminars:
                return 0
            capacity = self.s_cap
        else:
            if not self.practicals:
                return 0
            capacity = self.p_cap

        if student_count % capacity > 0:
            return student_count//capacity + 1
        else:
            return student_count//capacity

class Student:
    """
    Creates a student object containing student info and a list
    of courses which the student is following. The student data is
    in the following format: [last name, first name, id, course1, course2, ...]
    """
    def __init__(self, data):
        self.name = data[1] + " " + data[0]
        self.id = int(data[2])
        courses = []
        for str in data[3:]:
            if str:
                courses.append(str)
        self.courses = courses

class Teaching:
    """
    Creates a teaching object containing the type of teaching, course data,
    a list of students following the teaching and the hall.
    Input is another teaching object (with optional additional hall arg),
    in which case arg1 is a Teaching object, or manual entry of each argument,
    in which case arg1 is one of "lecture", "seminar" or "practical".
    """
    def __init__(self, arg1, course=None, students=[], group="",
        hall=None):
        if isinstance(arg1, type(self)):
            self.type = arg1.type
            self.course = arg1.course
            self.students = arg1.students
            self.group = arg1.group
            if hall:
                self.hall = hall
            else:
                self.hall = arg1.hall
        else:
            self.type = arg1
            self.course = course
            self.students = students
            self.group = group
            self.hall = hall

    def __repr__(self):
        group_str = ""
        if self.group:
            group_str = " - Group " + self.group

        return self.course.name + " - " + self.type + group_str

class TeachingHall:
    """
    Creates a teaching hall object containing hall data.
    The data is in the following format: [name, capacity].
    """
    def __init__(self, data):
        self.name = data[0]
        self.capacity = data[1]
