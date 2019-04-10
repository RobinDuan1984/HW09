from collections import defaultdict
from prettytable import PrettyTable
import os
from HW08_Zhixiong_Duan import read_files


class Student:
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.course = defaultdict(str)

    def __repr__(self):
        return ' '. join([self.cwid, self.name, self.major, ' '.join(self.course.keys())])


class Instructor:
    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course = defaultdict(int)

    def __repr__(self):
        return ' '.join([self.cwid, self.name, self.dept, ' '.join(self.course.keys())])


class Repository:
    def __init__(self, path: str):
        self.students = dict()  # students[cwid] = Student()
        self.instructors = dict()  # instructors[cwid] = Instructor()
        self.path = path
        self.readfile()
        self.students_table()
        self.instructors_table()

    def readfile(self):
        self.student_info()
        self.instructor_info()
        self.grades_info()

    def instructor_info(self):
        for line in read_files(os.path.join(self.path, "instructors.txt"), 3, '\t', False):
            cwid = line[0].strip()

            if cwid.isdigit() is False:
                raise ValueError("Incorrect instructor's CWID", cwid)

            if cwid in self.instructors.keys():
                raise ValueError("We already have this instructor's info", cwid)

            name = line[1].strip()
            dept = line[2].strip()
            instructor = Instructor(cwid, name, dept)
            self.instructors[cwid] = instructor

    def student_info(self):
        for line in read_files(os.path.join(self.path, "students.txt"), 3, '\t', False):
            cwid = line[0].strip()
            if cwid.isdigit() is False:
                raise ValueError("Incorrect student's CWID", cwid)
            if cwid in self.students.keys():
                raise ValueError("We already have this student's info", cwid)

            major = line[2].strip()
            name = line[1].strip()
            student = Student(cwid, name, major)
            self.students[student.cwid] = student

    def grades_info(self):
        for line in read_files(os.path.join(self.path, "grades.txt"), 4, '\t', False):
            students_cwid = line[0].strip()
            if students_cwid.isdigit() is False:
                raise ValueError("Incorrect student's CWID", str(line))
            if students_cwid in self.students.keys() is False:
                raise ValueError("We don't have info of this student", str(line))

            instructors_cwid = line[3].strip()
            if instructors_cwid.isdigit() is False:
                raise ValueError("Incorrect instructor's CWID", str(line))
            if instructors_cwid in self.instructors.keys() is False:
                raise ValueError("We don't have info of this instructor", str(line))

            course = line[1].strip()
            grade = line[2].strip()

            if course in self.students[students_cwid].course:
                raise ValueError("We already have grade of this course", str(line))

            self.instructors[instructors_cwid].course[course] += 1
            self.students[students_cwid].course[course] = grade

    def students_table(self):
        table = PrettyTable(field_names=["CWID", "Name", "Major", "Course"])
        test = list()

        for stud in sorted(self.students.values(), key=lambda student: student.cwid):
            row = (stud.cwid, stud.name, stud.major, sorted([name for name in stud.course]))
            table.add_row(row)

        print(table)
        return test

    def instructors_table(self):
        table = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "StudentsNum"])
        test = list()

        for instr in sorted(self.instructors.values(), key=lambda instructor: instructor.cwid):
            for course, student in instr.course.items():
                row = (instr.cwid, instr.name, instr.dept, course, student)
                table.add_row(row)

        print(table)
        return test


if __name__ == "__main__":
    Repository("./HW09")