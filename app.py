from flask import Flask, redirect, url_for, render_template, request, flash, get_flashed_messages, session
from setup_db import execute_query
from sqlite3 import IntegrityError
from collections import namedtuple
import sqlite3
from classes import Course, Teacher, Student, Grade, Attend

app = Flask(__name__)
app.secret_key = 'alex'


@app.route("/", methods=['GET'])
def home_page():
    if request.method == 'GET':
        username = session.get('username')
        if username is not None:
            user_type_from_database = execute_query(f"SELECT user_type FROM users WHERE username='{username}'")
            if user_type_from_database and user_type_from_database[0][0] in ['admin', 'teacher', 'student']:
                session['user_type'] = user_type_from_database[0][0]
            return render_template('main.html', username=username)
        else:
            welcome_guest = "Welcome, Guest"
            return render_template('main.html', welcome_guest=welcome_guest)


@app.route("/main", methods=['GET'])
def main():
    if request.method == 'GET':
        username = session.get('username')
        if username is not None:
            user_type_from_database = execute_query(f"SELECT user_type FROM users WHERE username='{username}'")
            if user_type_from_database and user_type_from_database[0][0] in ['admin', 'teacher', 'student']:
                session['user_type'] = user_type_from_database[0][0]
            return render_template('main.html', username=username)
        else:
            welcome_guest = "Welcome, anon"
            return render_template('main.html', welcome_guest=welcome_guest)


@app.route("/new_user", methods=['POST', 'GET'])
def new_user():
    if request.method == 'POST':
        username = request.form["user_name"]
        password = request.form["pass_word"]
        user_type = request.form["user_type"]
        session['username'] = username
        session['user_type'] = user_type
        execute_query(f"INSERT INTO users (username, password, user_type) VALUES ('{username}','{password}','{user_type}')")
        return redirect(url_for('login'))
    if request.method == 'GET':
        types = execute_query('SELECT user_type FROM users')
        return render_template('new_user.html', types=types)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        result = execute_query(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        if result:
            user_type_from_database = result[0][3]
            session['user_type'] = user_type_from_database
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return render_template('login.html', error_message='Invalid username or password')
    
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("user_type", None)
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    user_type = session.get('user_type')
    if user_type not in ['admin']:
        return "Access Denied"
    
    if request.method == 'GET':
        return render_template("add_course.html")

    if request.method == 'POST':
        name = request.form["course_name"]
        course_description = request.form["course_description"]
        execute_query(f"INSERT INTO courses (name, description) VALUES ('{name}', '{course_description}')")
        return redirect(url_for('course_list'))


@app.route('/course_list', methods=['GET'])
def course_list():
    courses = []
    rows = execute_query("SELECT * FROM courses")
    for row in rows:
        course = Course(row[0], row[1], row[2])
        courses.append(course)
        
    return render_template('course_list.html', courses=courses)


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
    

@app.route("/students" ,methods=['POST','GET'])
def list_students():
    if request.method == 'GET':
        students = []
        rows = execute_query("SELECT * FROM students")
        for row in rows:
            student = Student(row[0], row[1], row[2], row[3])
            students.append(student)
        return render_template("students.html", students=students)
    

@app.route("/students/<student_id>/view_student", methods=['GET', 'POST'])
def view_student(student_id):
    students = []
    if request.method == 'GET':
        rows = execute_query(f"SELECT * FROM students WHERE id='{student_id}'")
        for row in rows:
            student = Student(row[0], row[1], row[2], row[3])
            students.append(student)
    courses = []
    rows = execute_query(f"SELECT c.name, sc.grade FROM students_courses sc JOIN courses c ON c.id=sc.course_id WHERE sc.student_id='{student_id}'")
    for row in rows:
        course = Grade(row[0], row[1])
        courses.append(course)
    return render_template("view_student.html",students=students, courses=courses)


@app.route("/students/<student_id>/edit_student", methods=['GET', 'POST'])
def edit_student(student_id):
    student = None
    rows = execute_query(f"SELECT * FROM students WHERE id='{student_id}'")
    for row in rows:
        student = Student(row[0], row[1], row[2], row[3])
    if request.method == "POST":
        name = request.form.get("student_name")
        email = request.form.get("student_email")
        phone = request.form.get("student_phone")
        execute_query(f"UPDATE students SET name='{name}', email='{email}', phone_num='{phone}'")
    return render_template("edit_student.html", student=student)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if query:
        query_string = f"%{query}%"
        with sqlite3.connect("students.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor=conn.cursor()
            
            # Execute the queries using parameterized queries
            cursor.execute("SELECT * FROM courses WHERE name LIKE ?", (query_string,))
            course_results = cursor.fetchall()
            
            cursor.execute("SELECT * FROM students WHERE name LIKE ?", (query_string,))
            student_results = cursor.fetchall()
            
            cursor.execute("SELECT * FROM teachers WHERE name LIKE ?", (query_string,))
            teacher_results = cursor.fetchall()
            
        return render_template('search_results.html', query=query, course_results=course_results, student_results=student_results, teacher_results=teacher_results)
    else:
        return redirect(url_for('main'))
    
@app.route('/search_results', methods=['GET'])
def search_results():
    if request.method == 'GET':
        return render_template('search_results.html')


@app.route('/assign_student', methods=['POST', 'GET'])
def new_assign():
    if request.method == 'POST':
        student_name = request.form.get("student_name")
        course_name = request.form.get("course_name")
        student_id = execute_query(f"SELECT id FROM students WHERE name = '{student_name}'")
        course_id = execute_query(f"SELECT id FROM courses WHERE name = '{course_name}'")
        if student_id and course_id:
            execute_query(f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id[0][0]}', '{course_id[0][0]}')")
            return redirect(url_for('main'))
        else:
            return "Student or course not found."
    
    if request.method == 'GET':
        students =[]
        courses = []
        student = execute_query('SELECT name FROM students')
        for c in student:
            students.append(c)
        course = execute_query('SELECT name FROM courses')
        for s in course:
            courses.append(s)
        return render_template("assign_student.html", students=students, courses=courses)


@app.route('/assign_teacher', methods=['POST', 'GET'])
def now_assign():
    if request.method == 'POST':
        teacher_name = request.form.get("teacher_name")
        course_name = request.form.get("course_name")
        teacher_id = execute_query(f"SELECT id FROM teachers WHERE name = '{teacher_name}'")
        course_id = execute_query(f"SELECT id FROM courses WHERE name = '{course_name}'")
        if teacher_id and course_id:
            execute_query(f"INSERT INTO course_teacher (student_id, course_id) VALUES ('{teacher_id[0][0]}', '{course_id[0][0]}')")
            return redirect(url_for('main'))
        else:
            return "Student or course not found."
    
    if request.method == 'GET':
        teachers =[]
        courses = []
        teacher = execute_query('SELECT name FROM teachers')
        for c in teacher:
            teachers.append(c)
        course = execute_query('SELECT name FROM courses')
        for s in course:
            courses.append(s)
        return render_template("assign_teacher.html", teachers=teachers, courses=courses)
    

if __name__ == '__main__':
    app.run(debug=True)
