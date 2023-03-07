from flask import Flask, redirect, url_for, render_template, request, flash, get_flashed_messages
from setup_db import execute_query
from sqlite3 import IntegrityError
from collections import namedtuple
import sqlite3
from classes import Course, Teacher, Student, Grade, Attend

app = Flask(__name__)
app.secret_key = 'alex'



@app.route("/", methods=['GET'])
def home_page():
    return render_template('main.html')


@app.route("/new_user", methods=['POST', 'GET'])
def new_user():
    if request.method == 'POST':
        with sqlite3.connect("students.db") as conn:
            username = request.form["user_name"]
            password = request.form["pass_word"]
            cur = conn.cursor()
            cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}','{password}')")
            return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('new_user.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')



@app.route("/course_list", methods=['GET'])
def course_list():
    if request.method == 'GET':
        with sqlite3.connect("students.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses_list")
            courses_list = cur.fetchall()
            return render_template('course_list.html', courses_list=courses_list)


@app.route('/register/<student_id>/<course_id>')
def register(student_id, course_id):
    try:
        execute_query(
            f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}', '{course_id}')")
    except IntegrityError:
        return f"{student_id} is already registered to {course_id}"
    return redirect(url_for('registrations', student_id=student_id))


@app.route('/registrations/<student_id>')
def registrations(student_id):
    course_ids = execute_query(
        f"SELECT course_id FROM students_courses WHERE student_id={student_id}")
    clean_ids = [c[0] for c in course_ids]
    course_names = []
    for i in clean_ids:
        course_names.append(execute_query(
            f"SELECT name FROM courses WHERE id={i}"))
    student_name = execute_query(
        f"SELECT name FROM students WHERE id={student_id}")
    return render_template("registrations.html", student_name=student_name, course_names=course_names)


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'GET':
        with sqlite3.connect("students.db") as conn:
            teachers = []
            cur = conn.cursor()
            cur.execute("SELECT name FROM teachers")
            teachers = cur.fetchall()
        return render_template("add_course.html", teachers=teachers)
    if request.method == 'POST':
        with sqlite3.connect("students.db") as conn:
            name = request.form["course_name"]
            course_teacher = request.form["course_teacher"]
            course_description = request.form["course_description"]
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO courses_list (name, teacher_name, description) VALUES ('{name}', '{course_teacher}','{course_description}')")
        return "new course added"
    return render_template('course_list.html')

@app.route('/attendance', methods=['GET', 'POST'])
def page():
    return render_template('attendance.html')


@app.route('/python_attend',methods=['GET','POST'])
def python():
    if request.method == 'POST':
        name = request.form['name']
        attend = request.form['attendance']
        execute_query(f"UPDATE students_attendance SET attendance='{attend}' WHERE student_id = (SELECT id FROM students WHERE name = '{name}') AND course_id=1")
        python_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=1")
        for student in students:
            python_attend[student[0]] = student[1]
        return render_template('python_attend.html', python_attend=python_attend)

    if request.method == 'GET':
        python_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=1")
        for student in students:
            name = student[0]
            attend = student[1]
            python_attend[name] = attend
        return render_template('python_attend.html', python_attend=python_attend)

@app.route('/java_attend',methods=['GET','POST'])
def java():
    if request.method == 'POST':
        name = request.form['name']
        attend = request.form['attendance']
        execute_query(f"UPDATE students_attendance SET attendance='{attend}' WHERE student_id = (SELECT id FROM students WHERE name = '{name}') AND course_id=2")
        java_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=2")
        for student in students:
            java_attend[student[0]] = student[1]
        return render_template('java_attend.html', java_attend=java_attend)

    if request.method == 'GET':
        java_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=2")
        for student in students:
            name = student[0]
            attend = student[1]
            java_attend[name] = attend
        return render_template('java_attend.html', java_attend=java_attend)

@app.route('/html_attend',methods=['GET','POST'])
def html():
    if request.method == 'POST':
        name = request.form['name']
        attend = request.form['attendance']
        execute_query(f"UPDATE students_attendance SET attendance='{attend}' WHERE student_id = (SELECT id FROM students WHERE name = '{name}') AND course_id=3")
        html_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=3")
        for student in students:
            html_attend[student[0]] = student[1]
        return render_template('html_attend.html', html_attend=html_attend)

    if request.method == 'GET':
        html_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=3")
        for student in students:
            name = student[0]
            attend = student[1]
            html_attend[name] = attend
        return render_template('html_attend.html', html_attend=html_attend)
    
@app.route('/javascript_attend',methods=['GET','POST'])
def javascript():
    if request.method == 'POST':
        name = request.form['name']
        attend = request.form['attendance']
        execute_query(f"UPDATE students_attendance SET attendance='{attend}' WHERE student_id = (SELECT id FROM students WHERE name = '{name}') AND course_id=5")
        javascript_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=5")
        for student in students:
            javascript_attend[student[0]] = student[1]
        return render_template('javascript_attend.html', javascript_attend=javascript_attend)

    if request.method == 'GET':
        javascript_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=5")
        for student in students:
            name = student[0]
            attend = student[1]
            javascript_attend[name] = attend
        return render_template('javascript_attend.html', javascript_attend=javascript_attend)
    
@app.route('/css_attend',methods=['GET','POST'])
def css():
    if request.method == 'POST':
        name = request.form['name']
        attend = request.form['attendance']
        execute_query(f"UPDATE students_attendance SET attendance='{attend}' WHERE student_id = (SELECT id FROM students WHERE name = '{name}') AND course_id=4")
        css_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=4")
        for student in students:
            css_attend[student[0]] = student[1]
        return render_template('css_attend.html', css_attend=css_attend)

    if request.method == 'GET':
        css_attend = {}
        students = execute_query("SELECT s.name, sa.attendance FROM students_attendance sa JOIN students s ON s.id = sa.student_id WHERE sa.course_id=4")
        for student in students:
            name = student[0]
            attend = student[1]
            css_attend[name] = attend
        return render_template('css_attend.html', css_attend=css_attend)
    
if __name__ == '__main__':
    app.run(debug=True)
