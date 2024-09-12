import os
import jwt
import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'admin')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'admin')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'myDb')

# Initialize MySQL
mysql = MySQL(app)

# Email configuration from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))

# Secret key for JWT
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

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

    # Generate a unique token
    token = jwt.encode({
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    # Insert the data into MySQL
    cur = mysql.connection.cursor()
    query = "INSERT INTO users (name, phone, email, country, is_verified) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query, (name, phone, email, country, False))
    mysql.connection.commit()
    cur.close()

    # Send verification email
    verification_link = url_for('verify_email', token=token, _external=True)
    send_verification_email(email, verification_link)

    return redirect(url_for('welcome'))

@app.route('/verify/<token>')
def verify_email(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        email = data['email']
    except jwt.ExpiredSignatureError:
        return "The verification link has expired.", 400
    except jwt.InvalidTokenError:
        return "Invalid verification link.", 400

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET is_verified = %s WHERE email = %s", (True, email))
    mysql.connection.commit()
    cur.close()

    return render_template('verify.html', message="Email verified successfully!")

def send_verification_email(to_email, verification_link):
    msg = MIMEText(f'Please click on the following link to verify your email address: {verification_link}')
    msg['Subject'] = 'Email Verification'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f'Failed to send email: {e}')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # Welcome page after registration

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

