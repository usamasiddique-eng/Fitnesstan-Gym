from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing
from flask import session  # To handle user sessions

# Initialize the Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'  # SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Used for Flask sessions

# A dictionary to store user credentials temporarily
# Format: email -> password_hash
users_db = {}

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/membership')
def membership():
    return render_template('membership.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        email = request.form['email']
        plan = request.form['plan']

        # Check if the email already exists
        existing_member = Member.query.filter_by(email=email).first()
        if existing_member:
            return render_template('membership.html', error="This email is already registered!")

        # Add the new member
        new_member = Member(name=name, email=email, plan=plan)
        db.session.add(new_member)
        db.session.commit()

        return redirect(url_for('thank_you', name=name))
    except Exception as e:
        return "An error occurred during registration. Please try again."

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process contact form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Here, you can add logic to send an email or save to the database
        return render_template('contact.html', success=True)
    return render_template('contact.html')

@app.route('/members')
def members():
    all_members = Member.query.all()
    return render_template('members.html', members=all_members)

@app.route('/registerpage', methods=['GET', 'POST'])
def userregister():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        plan = request.form.get('plan')

        # Simulated database (temporary dictionary for this example)
        global users_db
        if email in users_db:
            return render_template('registerpage.html', error="This email is already registered!")

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Save user data
        users_db[email] = {
            'name': name,
            'password': hashed_password,
            'plan': plan
        }

        return redirect(url_for('login'))

    return render_template('registerpage.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists and verify the password
        if email in users_db and check_password_hash(users_db[email]['password'], password):
            session['user'] = email  # Store user in session
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid email or password.")

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
