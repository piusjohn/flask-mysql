from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # The registration page

@app.route('/register', methods=['POST'])
def register():
    # Debug: print the form data to the terminal
    print(request.form)

    # Get form data safely
    name = request.form.get('name')
    phone = request.form.get('phone')  # Updated to match the form field name
    email = request.form.get('email')
    country = request.form.get('country')

    # Check if any field is missing
    if not phone:
        return "Phone number is missing", 400

    # Assume you have a User model for storing data in the database
    # new_user = User(name=name, phone=phone, email=email, country=country)
    # db.session.add(new_user)
    # db.session.commit()

    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # The welcome page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
