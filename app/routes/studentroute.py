from flask import *
from flask import render_template, request, redirect, url_for
import re
from flask import flash
import psycopg2


def db_conn():
      conn = psycopg2.connect (database = "database", host = "localhost", user = "postgres", password = "1234", port = "5432")
      return conn 


student_bp = Blueprint('student', __name__)

@student_bp.route('/students/')
def students():
    conn = db_conn()
    if conn:
        print("Connected to database successfully")
    else:
        print("Failed to connect to database")

    cur = conn.cursor()
    if cur:
        print("Cursor created successfully")
    else:
        print("Failed to create cursor")

    cur.execute('''SELECT * FROM STUDENTS''')
    students = cur.fetchall()  # Rename the variable to students
    cur.close()
    conn.close()
    print("Fetched students:", students)
    return render_template('student.html', students=students)  # Pass students to the template




@student_bp.route('/addstudents', methods=['GET', 'POST'])
def addstudent():
    if request.method == 'POST':
        conn = db_conn()
        if conn:
            print("Connected to database successfully")
        else:
            print("Failed to connect to database")

        cur = conn.cursor()
        if cur:
            print("Cursor created successfully")
        else:
            print("Failed to create cursor")

        student_id = request.form.get('student_id')
        student_name = request.form.get('student_name')
        course_id = request.form.get('course_name')
        cur.execute('INSERT INTO students (student_id, student_name, course_name) VALUES (%s, %s, %s)', (student_id, student_name, course_id))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Student ID: {student_id}, Student Name: {student_name}, Course ID: {course_id}")

        return redirect(url_for('student.students'))  # Redirect to the students page after adding the student
    else:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT course_id FROM courses')
        courses = cur.fetchall()  # Fetch all course IDs from the database
        cur.close()
        conn.close()
        print("Fetched courses:", courses)  # Check if courses are fetched correctly
        return render_template('addstudent.html', courses=courses)
    


@student_bp.route('/editstudent/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        # Handle the form submission to update the student
        conn = db_conn()
        cur = conn.cursor()
        student_name = request.form.get('student_name')
        course_id = request.form.get('course_id')
        cur.execute('UPDATE students SET student_name = %s, course_id = %s WHERE student_id = %s', (student_name, course_id, student_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('student.students'))  # Redirect to the students page after editing the student
    else:
        # Fetch the student's information and available courses from the database
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
        student = cur.fetchone()
        cur.execute('SELECT course_id FROM courses')
        courses = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('editstudents.html', student=student, courses=courses)
    

@student_bp.route('/deletestudent', methods=['DELETE'])
def delete_student():
    student_id = request.json['student_id']
    conn = db_conn()
    if conn:
        print("Connected to database successfully")
    else:
        print("Failed to connect to database")

    cur = conn.cursor()
    if cur:
        print("Cursor created successfully")
    else:
        print("Failed to create cursor")

    cur.execute('DELETE FROM students WHERE student_id = %s', (student_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'student deleted successfully'})












