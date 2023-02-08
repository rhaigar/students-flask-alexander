from flask import Flask, redirect, url_for,render_template,request
from setup_db import execute_query
from sqlite3 import IntegrityError
from collections import namedtuple
import sqlite3
app = Flask(__name__)

@app.route("/main")
def home_page():
    return render_template('main.html')

@app.route("/course_list", methods=['GET'])
def course_list():
    if request.method=='GET':
        with sqlite3.connect("students.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM courses_list")
            courses_list= cur.fetchall()
    return render_template('course_list.html',courses_list=courses_list)

@app.route('/register/<student_id>/<course_id>')
def register(student_id, course_id):
    try:
        execute_query(f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}', '{course_id}')")
    except IntegrityError:
        return f"{student_id} is already registered to {course_id}"
    return redirect(url_for('registrations', student_id=student_id))

@app.route('/registrations/<student_id>')
def registrations(student_id):
    course_ids=execute_query(f"SELECT course_id FROM students_courses WHERE student_id={student_id}")
    clean_ids=[ c[0] for c in course_ids ]
    course_names=[]
    for i in clean_ids:
        course_names.append(execute_query(f"SELECT name FROM courses WHERE id={i}"))
    student_name=execute_query(f"SELECT name FROM students WHERE id={student_id}")
    return render_template("registrations.html", student_name=student_name,course_names=course_names)

@app.route('/add_course',methods=['GET','POST'])
def add_course():
    if request.method=='GET':
        return render_template("add_course.html")
    if request.method=='POST':
        with sqlite3.connect("students.db") as conn:
            name=request.form["course_name"]
            course_teacher=request.form["course_teacher"]
            course_description=request.form["course_description"]
            cur = conn.cursor()
            cur.execute(f"INSERT INTO courses_list (name, teacher_name, description) VALUES ('{name}', '{course_teacher}','{course_description}')")
        return "new course added"
    return render_template('course_list.html')

if __name__ == '__main__':
    app.run(debug=True)