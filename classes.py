class Course:
    """
    Creates a course object containing course data and
    a list of students following the course.
    The course data is in the following format:
    [name, lectures, seminars, seminar capacity, practicals, practical capacity]
    """
    def __init__(self, data, students):
        self.name = data[0]
        self.lectures = int(data[1])
        self.seminars = int(data[2])
        self.s_cap = int(data[3])
        self.practicals = int(data[4])
        self.p_cap = int(data[5])
        self.students = students

    def get_group_count(self, _type):
        """Determine number of groups of type _type."""

        student_count = len(self.students)
        if _type == "seminar":
            capacity = self.s_cap
        else:
            capacity = self.p_cap

        if student_count % capacity > 0:
            return student_count//capacity + 1
        else:
            return student_count//capacity


class Teaching:
    """
    Creates a teaching object containing the type of teaching,
    course data and a list of students following the teaching.
    """
    def __init__(self, _type, course, students, group=""):
        self.course_name = course.name
        self.type = _type
        self.students = students
        self.group = group

    def __repr__(self):

        group_str = ""
        if self.group:
            group_str = " - Group " + self.group

        return self.course_name + " - " + self.type + group_str
