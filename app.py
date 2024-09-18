import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import Config
import MySQLdb

app = Flask(__name__)
app.config.from_object(Config)

def create_database_if_not_exists():
    # Connect to MySQL server
    conn = MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD']
    )
    cursor = conn.cursor()
    # Create database if it does not exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DB']}")
    cursor.close()
    conn.close()

# Create the database if not exists
create_database_if_not_exists()

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')  # Registration form

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    country = request.form.get('country')

    # Validate input
    if not phone:
        return "Phone number is missing", 400

    # Insert the data into MySQL
    cur = mysql.connection.cursor()
    query = "INSERT INTO users (name, phone, email, country) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (name, phone, email, country))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # Welcome page after registration

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
