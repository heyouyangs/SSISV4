from flask import *
import psycopg2
from flask import render_template


def db_conn():
      conn = psycopg2.connect (database = "database", host = "localhost", user = "postgres", password = "1234", port = "5432")
      return conn 


course_bp = Blueprint('course', __name__)

@course_bp.route('/courses/')
def courses():
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

    cur.execute('''SELECT * FROM COURSES''')
    courses = cur.fetchall()  # Rename the variable to courses
    cur.close()
    conn.close()
    print("Fetched COURSES:", courses)
    return render_template('courses.html', courses=courses)


@course_bp.route('/addcourse/', methods=['GET', 'POST'])
def addcourse():
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

        course_id = request.form.get('course_id')
        course_name = request.form.get('course_name')
        cur.execute('INSERT INTO courses (course_id, course_name) VALUES (%s, %s)', (course_id, course_name))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Course ID: {course_id}, Course Name: {course_name}")

        return redirect(url_for('course.courses'))  # Redirect to the courses page after adding the course
    else:
        return render_template('addcourses.html')
    
@course_bp.route('/editcourse/<int:course_id>', methods=['GET', 'POST'])
def edit_courses(course_id):
    if request.method == 'POST':
        conn = db_conn()
        if conn:
            print("Connected to database successfully")
        else:
            print("Failed to connect to database")
            return redirect(url_for('course.courses'))  # Redirect to courses page if failed to connect

        cur = conn.cursor()
        if cur:
            print("Cursor created successfully")
        else:
            print("Failed to create cursor")
            conn.close()
            return redirect(url_for('course.courses'))  # Redirect to courses page if failed to create cursor

        course_name = request.form.get('course_name')
        try:
            cur.execute('UPDATE courses SET course_name = %s WHERE course_id = %s', (course_name, course_id))
            conn.commit()
            print(f"Course ID: {course_id}, Course Name: {course_name}")
        except psycopg2.Error as e:
            print(f"Error updating course: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('course.courses'))  # Redirect to the courses page after editing the course
    else:

        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM courses WHERE course_id = %s', (course_id,))
        course = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('editcourses.html', course=course)
    

@course_bp.route('/deletecourse/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM courses WHERE course_id = %s', (course_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Course deleted successfully'})






