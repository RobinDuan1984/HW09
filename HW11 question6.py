import sqlite3
from prettytable import PrettyTable
conn = sqlite3.connect("810_startip.sqlite")
cursor = conn.cursor()

qurery = "select i.CWID, i.Name, i.Dept, g.Course, count(g.Student_CWID) as Student_num from HW11_instructors i join HW11_grades g on i.CWID = g.Instructor_CWID group by i.CWID, i.Name, i.Dept, g.Course order by i.CWID desc"
table = PrettyTable()
table.field_names = ["CWID", "Name", "Dept", "Course", "Num_student"]
line = list()
for row in cursor.execute(qurery):
    table.add_row(row)
print(table)