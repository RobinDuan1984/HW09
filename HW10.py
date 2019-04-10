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


class Major:
    def __init__(self, dept):
        self.dept = dept
        self.required = set()
        self.elective = set()
        self.type = defaultdict(str)
        self.passed_grade = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def add_course(self, course_type, course):
        if course_type == "R":
            self.required.add(course)
        elif course_type == "E":
            self.elective.add(course)
        else:
            raise ValueError("Course type is not matched with course")

    def __repr__(self):
        return ''.join([self.dept, self.required, self.elective, ' '.join(self.type.keys())])


class Repository:
    def __init__(self, path:str):
        self.students = dict()  # students[cwid] = Student()
        self.instructors = dict()  # instructors[cwid] = Instructor()
        self.major = dict() # dept[dept] = Remain()
        self.path = path
        self.readfile()
        self.students_table()
        self.instructors_table()
        self.major_table()

    def readfile(self):
        self.student_info()
        self.instructor_info()
        self.grades_info()
        self.remaining_info()

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
                raise ValueError("Incorrect student's CWID：", cwid)
            if cwid in self.students.keys():
                raise ValueError("We already have this student's info：", cwid)

            name = line[1].strip()
            major = line[2].strip()
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

    def remaining_info(self):
        for line in read_files(os.path.join(self.path, "majors.txt"), 3, '\t', False):
            depart = line[0].strip()
            course_type = line[1].strip()
            course = line[2].strip()
            if depart not in self.major.keys():
                self.major[depart] = Major(depart)

            self.major[depart].add_course(course_type, course)

    def students_table(self):
        table = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Course",
                                         "Remaining Required", "Remaining Elective"])
        test = list()

        for stud in sorted(self.students.values(), key=lambda student: student.cwid):
            completed_course = sorted(set(stud.course.keys()))
            passed = {course for course, grade in stud.course.items() if grade in self.major[stud.major].passed_grade}
            rest_required = sorted(self.major[stud.major].required - passed)
            if self.major[stud.major].elective.intersection(passed):
                rest_elective = None
            else:
                rest_elective = sorted(self.major[stud.major].elective)

            row = (stud.cwid, stud.name, stud.major, completed_course, rest_required, rest_elective)
                   
            table.add_row(row)
            test.append(row)

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

    def major_table(self):
        table = PrettyTable(field_names=["Dept", "Required", " Elective"])
        test = list()

        for major in sorted(self.major.values(), key=lambda major: major.dept):
            row = major.dept, sorted(list(major.required)), sorted(list(major.elective))
            table.add_row(row)
            test.append(row)

        print(table)
        return test


if __name__ == "__main__":
    Repository("./HW10")