import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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
