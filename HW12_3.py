from flask import Flask, render_template
import sqlite3
app = Flask(__name__)


@app.route('/instructor_summary')
def instructor_info():
    conn = sqlite3.connect("810_startip.sqlite")
    cursor = conn.cursor()

    query = """select i.CWID, i.Name, i.Dept, g.Course, count(g.Student_CWID) as Student_num
                from HW11_instructors i join HW11_grades g on i.CWID = g.Instructor_CWID
                group by i.CWID, i.Name, i.Dept, g.Course order by i.CWID desc"""
    result = cursor.execute(query)

    data = [{'cwid': cwid, 'name': name, 'department': department, 'course': course, 'students': students}
            for cwid, name, department, course, students in result]
    cursor.close()
    return render_template('instructor_summary.html',
                           title='Stevens Repository',
                           table_title="Instructor Summary",
                           instructors=data)


if __name__ == '__main__':
    app.run(debug=True)
