from flask import *
import psycopg2
from app.routes import studentroute, courseroute

def create_app():
    app = Flask(__name__)

    conn = psycopg2.connect (database = "database", host = "localhost", user = "postgres", password = "1234", port = "5432")
    cur = conn.cursor()
    


    
    @app.route('/')
    def homepage():
        return render_template('index.html')
    
    app.register_blueprint(studentroute.student_bp)
    app.register_blueprint(courseroute.course_bp)

    
    return app
