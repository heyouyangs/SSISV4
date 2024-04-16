from flask import *
import psycopg2
from flask import render_template
from flask import request


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

    # Check if the request is from Postman
    if 'Postman-Token' in request.headers or 'Postman-Echo-Token' in request.headers:
        # Return JSON response for Postman
        return jsonify(courses)
    else:
        # Return HTML for web app
        return render_template('courses.html', courses=courses)


@course_bp.route('/addcourse/', methods=['GET', 'POST'])
def addcourse():
    if request.method == 'POST':
        try:
            conn = db_conn()
            cur = conn.cursor()

            course_id = request.form.get('course_id')
            course_name = request.form.get('course_name')
            
            cur.execute('INSERT INTO courses (course_id, course_name) VALUES (%s, %s)', (course_id, course_name))
            conn.commit()
            return redirect(url_for('course.courses'))
        except psycopg2.Error as e:
            flash('Failed to add course. Please try again.', 'error')
            conn.rollback()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    return render_template('addcourses.html')

    
@course_bp.route('/editcourse/<int:course_id>', methods=['GET', 'POST'])
def edit_courses(course_id):
    if request.method == 'POST':
        try:
            conn = db_conn()
            cur = conn.cursor()

            course_name = request.form.get('course_name')
            cur.execute('UPDATE courses SET course_name = %s WHERE course_id = %s', (course_name, course_id))
            conn.commit()

            return redirect(url_for('course.courses'))
        except psycopg2.Error as e:
            print(f"Error updating course: {e}")
            flash('Failed to update course. Please try again.', 'error')
            conn.rollback()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        return redirect(url_for('course.courses'))  # Redirect to the courses page after editing the course
    else:
        try:
            conn = db_conn()
            cur = conn.cursor()

            cur.execute('SELECT * FROM courses WHERE course_id = %s', (course_id,))
            course = cur.fetchone()

            return render_template('editcourses.html', course=course)
        except psycopg2.Error as e:
            print(f"Error fetching course: {e}")
            flash('Failed to fetch course. Please try again.', 'error')
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return redirect(url_for('course.courses'))


@course_bp.route('/deletecourse/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM courses WHERE course_id = %s', (course_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Course deleted successfully'})





#API










