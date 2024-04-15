from app import create_app
from flask import Flask, render_template
import psycopg2



app = create_app()



if __name__ == '__main__':
      app.run(debug=True)

def db_conn():
      conn = psycopg2.connect (database = "database", host = "localhost", user = "postgres", password = "1234", port = "5432")
      return conn 
