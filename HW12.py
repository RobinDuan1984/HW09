from flask import Flask, render_template
import sqlite3

app = Flask(__name__, template_folder='./instructor_summary.html')


@app.route('/instructor_summary')
def instructor_info():
    db_file = r"D:\SSW810\810_startip.sqlite"
    db = sqlite3.connect(db_file)
    query = """select i.CWID,i.Name,i.Dept,g.Course,count(g.Student_CWID) as Students
               from HW11_instructors as i
               join HW11_grades as g on g.Instructor_CWID = i.CWID group by g.Course"""
    result = db.execute(query)

    data = [{'CWID': cwid, 'Name': name, 'Department': department, 'Courses': course, 'student': student}
            for cwid, name, department, course, student in result]
    db.close()
    return render_template('instructor_summary.html',
                           title='Stevens Repository',
                           table_title="Instructor Summary",
                           instructor=data)


app.run(debug=True)
